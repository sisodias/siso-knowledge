#!/usr/bin/env python3
"""Shared loader and validation for the people knowledge registry."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
REGISTRY_FILE = ROOT / "pipelines" / "people" / "leaderboard.yaml"

DEFAULT_TIER_WEIGHTS = {
    "S": 4.0,
    "A": 3.0,
    "B": 2.0,
    "C": 1.0,
}

VALID_STATUSES = {"approved", "candidate", "maybe", "rejected"}
VALID_COLLECTION_MODES = {
    "direct-source-first",
    "social-first",
    "corpus-first",
    "manual-curation",
}


def slugify(value: str) -> str:
    """Create a stable ASCII slug from a person name."""
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def extract_handle(sources: list[dict[str, Any]]) -> str:
    """Return the first X/Twitter handle from a source list."""
    for source in sources:
        source_type = source.get("type", "")
        if source_type not in {"twitter", "x"}:
            continue
        url = source.get("url", "")
        match = re.search(r"(?:twitter\.com|x\.com)/@?([A-Za-z0-9_]+)", url)
        if match:
            return f"@{match.group(1)}"
        handle = source.get("handle")
        if handle:
            return handle if handle.startswith("@") else f"@{handle}"
    return ""


def load_registry(path: Path = REGISTRY_FILE) -> dict[str, Any]:
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    if "people" not in data:
        raise ValueError(f"{path} must contain a top-level 'people' list")
    return data


def normalize_person(person: dict[str, Any], tier_weights: dict[str, float]) -> dict[str, Any]:
    normalized = dict(person)
    name = normalized.get("name", "").strip()
    if not name:
        raise ValueError("Every registry entry must have a name")

    normalized.setdefault("slug", slugify(name))
    normalized.setdefault("status", "candidate")
    normalized.setdefault("line", "uncategorized")
    normalized.setdefault("role", normalized.get("title", ""))
    normalized.setdefault("topics", [])
    normalized.setdefault("sources", [])
    normalized.setdefault("collection_mode", "manual-curation")
    normalized.setdefault("tier", "B")
    normalized.setdefault("notes", "")

    if normalized["status"] not in VALID_STATUSES:
        raise ValueError(f"{name} has invalid status: {normalized['status']}")
    if normalized["collection_mode"] not in VALID_COLLECTION_MODES:
        raise ValueError(f"{name} has invalid collection_mode: {normalized['collection_mode']}")
    if not isinstance(normalized["topics"], list):
        raise ValueError(f"{name} topics must be a list")
    if not isinstance(normalized["sources"], list):
        raise ValueError(f"{name} sources must be a list")

    tier = normalized.get("tier", "B")
    normalized["weight"] = float(normalized.get("weight", tier_weights.get(tier, 2.0)))
    normalized["handle"] = normalized.get("handle") or extract_handle(normalized["sources"])
    normalized["title"] = normalized.get("title") or normalized.get("role", "")
    normalized["url"] = normalized.get("url") or (
        normalized["sources"][0].get("url", "") if normalized["sources"] else ""
    )
    return normalized


def load_people(path: Path = REGISTRY_FILE, include_rejected: bool = False) -> list[dict[str, Any]]:
    data = load_registry(path)
    tier_weights = {
        tier: float(config.get("weight", DEFAULT_TIER_WEIGHTS.get(tier, 2.0)))
        for tier, config in data.get("tiers", {}).items()
    }
    tier_weights = {**DEFAULT_TIER_WEIGHTS, **tier_weights}

    people = [normalize_person(person, tier_weights) for person in data["people"]]
    if not include_rejected:
        people = [person for person in people if person["status"] != "rejected"]

    slugs = [person["slug"] for person in people]
    duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
    if duplicates:
        raise ValueError(f"Duplicate people slugs: {', '.join(duplicates)}")

    return people


def people_by_slug(people: list[dict[str, Any]] | None = None) -> dict[str, dict[str, Any]]:
    people = people if people is not None else load_people()
    return {person["slug"]: person for person in people}


def people_with_social_handles(people: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    people = people if people is not None else load_people()
    return [person for person in people if person.get("handle")]
