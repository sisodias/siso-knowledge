"""Single entrypoint parser for SISO Library markdown pages.

Usage:
    from frontmatter_parser import parse_page
    page = parse_page("/path/to/sections/ai_research/…/p_0667.md")
    print(page.id, page.tier)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Optional, Union

import yaml  # stdlib fallback; python_frontmatter preferred if available

from frontmatter_schema import Page, RevisionEntry

# Try to use python_frontmatter (preferred); fall back to stdlib yaml approach.
try:
    import python_frontmatter as _fm
    _USE_FM = True
except ImportError:
    _USE_FM = False


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _normalise_tags(value: Any) -> list[str]:
    """Normalise tags field to a flat list[str].

    Handles:
      - None          → []
      - list[str]     → returned as-is (deduplicated, preserving order)
      - str           → split on commas, strip whitespace, filter empty
      - anything else → stringified and wrapped in a list
    """
    if value is None:
        return []
    if isinstance(value, list):
        seen: set[str] = set()
        out: list[str] = []
        for item in value:
            if isinstance(item, str):
                s = item.strip()
                if s and s not in seen:
                    seen.add(s)
                    out.append(s)
        return out
    if isinstance(value, str):
        items = [x.strip() for x in value.split(",")]
        seen = set()
        out = []
        for s in items:
            if s and s not in seen:
                seen.add(s)
                out.append(s)
        return out
    # Fallback: coerce to string
    return [str(value)]


def _coerce_float(value: Any, default: float = 7.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_int(value: Any, default: int = 1) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes")
    return bool(value)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_page(path: Union[str, Path]) -> Page:
    """Parse a single SISO Library markdown page.

    Args:
        path: Absolute or relative path to a `p_*.md` file.

    Returns:
        A ``Page`` dataclass instance with all frontmatter fields normalised
        and defaults applied for missing keys.

    Raises:
        FileNotFoundError: The file does not exist.
        ValueError: No parsable frontmatter block found and no title could
            be extracted from the content.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Page file not found: {path}")

    raw = path.read_text()

    if _USE_FM:
        try:
            post = _fm.loads(raw)
        except Exception as exc:
            raise ValueError(f"Failed to parse frontmatter in {path}: {exc}") from exc
        meta: dict[str, Any] = dict(post.metadata) if post.metadata else {}
        body: str = post.content
    else:
        # Stdlib fallback: split on --- frontmatter delimiters
        meta = {}
        body = raw
        if raw.startswith("---"):
            parts = raw.split("---", 2)
            if len(parts) >= 3:
                try:
                    meta = yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError as exc:
                    raise ValueError(f"Failed to parse YAML frontmatter in {path}: {exc}") from exc
                body = parts[2].strip()

    # ── Normalise tags ──────────────────────────────────────────────────────
    meta["tags"] = _normalise_tags(meta.get("tags"))

    # ── Normalise list fields (keep as lists, empty default) ────────────────
    for key in ("links_to",):
        val = meta.get(key)
        if val is None or not isinstance(val, list):
            meta[key] = []

    # ── Normalise revisions ────────────────────────────────────────────────
    revisions_raw = meta.get("revisions")
    if revisions_raw and isinstance(revisions_raw, list):
        meta["revisions"] = [
            RevisionEntry(
                at=str(r.get("at", "")),
                hash=str(r.get("hash", "")),
                diff_summary=str(r.get("diff_summary", "")),
            )
            for r in revisions_raw
            if isinstance(r, dict)
        ]
    else:
        meta["revisions"] = []

    # ── Extract page ID from filename when missing from frontmatter ─────────
    if not meta.get("id"):
        match = re.search(r"(p_\d+)", path.name)
        if match:
            meta["id"] = match.group(1)

    # ── Extract title from first heading when missing from frontmatter ───────
    if not meta.get("title") and body:
        lines = body.strip().split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#"):
                meta["title"] = stripped.lstrip("#").strip()
                break

    # ── Apply defaults and coercions ───────────────────────────────────────
    score = meta.get("score")
    meta["score"] = _coerce_float(score, 7.0) if score is not None else 7.0

    if meta.get("tier") is None:
        meta["tier"] = "B"

    version = meta.get("version")
    meta["version"] = _coerce_int(version, 1) if version is not None else 1

    # Boolean flags default to False
    for key in ("hub", "hub_featured", "archived", "cold", "pinned"):
        meta[key] = _coerce_bool(meta.get(key), False)

    # ── Derive _file relative path ─────────────────────────────────────────
    lib_root = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
    try:
        meta["_file"] = str(path.relative_to(lib_root))
    except ValueError:
        meta["_file"] = str(path)

    # ── Attach body ─────────────────────────────────────────────────────────
    meta["content"] = body

    # ── Build and return Page instance ──────────────────────────────────────
    return Page(
        id=meta.get("id", ""),
        slug=meta.get("slug"),
        book_id=meta.get("book_id"),
        title=meta.get("title"),
        shelf=meta.get("shelf"),
        creator=meta.get("creator"),
        source_video=meta.get("source_video"),
        source_id=meta.get("source_id"),
        score=meta.get("score", 7.0),
        tier=meta.get("tier", "B"),
        tags=meta.get("tags", []),
        links_to=meta.get("links_to", []),
        contradicts=meta.get("contradicts"),
        extracted_at=meta.get("extracted_at"),
        first_extracted_at=meta.get("first_extracted_at"),
        content_hash=meta.get("content_hash"),
        version=meta.get("version", 1),
        supersedes=meta.get("supersedes"),
        superseded_by=meta.get("superseded_by"),
        revisions=meta.get("revisions", []),
        hub=meta.get("hub", False),
        hub_category=meta.get("hub_category"),
        hub_featured=meta.get("hub_featured", False),
        archived=meta.get("archived", False),
        cold=meta.get("cold", False),
        pinned=meta.get("pinned", False),
        og_image=meta.get("og_image"),
        content=meta.get("content", ""),
        _file=meta.get("_file", ""),
    )
