#!/usr/bin/env python3
"""Download approved public-domain source texts into the local raw corpus."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.request import Request, urlopen

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))

from registry import load_people  # noqa: E402
from source_planner import build_source_plan  # noqa: E402

DEFAULT_RAW_SOURCE_DIR = ROOT / "pipelines" / "people" / "raw_sources"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_gutenberg_text_url(url: str) -> str:
    match = re.search(r"gutenberg\.org/ebooks/(\d+)", url)
    if not match:
        return ""
    return f"https://www.gutenberg.org/ebooks/{match.group(1)}.txt.utf-8"


def default_fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "SISO-Library-source-ingest/0.1"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def safe_filename(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "source"


def eligible_public_domain_targets(person: dict[str, Any]) -> list[dict[str, str]]:
    plan = build_source_plan(person)
    if plan["next_source_action"] == "rights_review_before_ingest":
        return []

    targets = []
    for target in plan["source_targets"]:
        if target["repository"] != "Project Gutenberg":
            continue
        if target["rights_status"] != "public_domain_source":
            continue
        text_url = build_gutenberg_text_url(target["url"])
        if not text_url:
            continue
        targets.append({**target, "text_url": text_url})
    return targets


def collect_public_domain_sources(
    people: list[dict[str, Any]],
    output_dir: Path = DEFAULT_RAW_SOURCE_DIR,
    fetcher: Callable[[str], str] = default_fetch,
    limit: int | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_sources: list[dict[str, Any]] = []

    for person in people:
        for target in eligible_public_domain_targets(person):
            if limit is not None and len(manifest_sources) >= limit:
                break

            person_dir = output_dir / person["slug"]
            person_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{safe_filename(target['title'])}.txt"
            local_path = person_dir / filename

            if local_path.exists():
                text = local_path.read_text(encoding="utf-8", errors="replace")
                downloaded = False
            else:
                text = fetcher(target["text_url"])
                local_path.write_text(text, encoding="utf-8")
                downloaded = True

            manifest_sources.append(
                {
                    "person_slug": person["slug"],
                    "person_name": person["name"],
                    "title": target["title"],
                    "repository": target["repository"],
                    "source_url": target["url"],
                    "download_url": target["text_url"],
                    "local_path": str(local_path),
                    "rights_status": target["rights_status"],
                    "retrieved_at": utc_now(),
                    "downloaded": downloaded,
                    "bytes": len(text.encode("utf-8")),
                    "notes": target.get("notes", ""),
                    "provenance_fields_required": [
                        "source_url",
                        "download_url",
                        "local_path",
                        "rights_status",
                        "retrieved_at",
                        "repository",
                        "title",
                    ],
                }
            )
        if limit is not None and len(manifest_sources) >= limit:
            break

    manifest = {
        "generated_at": utc_now(),
        "sources_count": len(manifest_sources),
        "output_dir": str(output_dir),
        "sources": manifest_sources,
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect approved public-domain people source texts")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    manifest = collect_public_domain_sources(load_people(), DEFAULT_RAW_SOURCE_DIR, limit=args.limit)
    print(f"Wrote {manifest['sources_count']} raw public-domain sources to {DEFAULT_RAW_SOURCE_DIR}")


if __name__ == "__main__":
    main()
