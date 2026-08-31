#!/usr/bin/env python3
"""Backfill slug and source_id fields for all pages.

slug       = kebab-case of title, truncated to 60 chars, deduped with -2 suffix on collision
source_id  = yt:<yt-id>  or  gh:<owner>/<repo>  or  null

Dry-run by default; --apply writes frontmatter changes.
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

import yaml

LIB_ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
YT_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")
GH_URL_RE = re.compile(r"^https?://github\.com/([^/]+)/([^/\s]+)/?")
GH_PATH_RE = re.compile(r"^([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+)$")


def to_kebab(title: str) -> str:
    """Convert title to a kebab-case slug."""
    # Normalize unicode (e.g. em dashes → hyphens, accents stripped)
    slug = unicodedata.normalize("NFKD", title)
    slug = slug.encode("ascii", "ignore").decode("ascii")
    # Lowercase, strip non-alphanumeric/non-hyphen, collapse spaces/hyphens
    slug = re.sub(r"[^a-z0-9 -]", "", slug.lower())
    slug = re.sub(r"[ -]+", "-", slug.strip())
    return slug[:60].rstrip("-")


def extract_source_id(source_video: str) -> str | None:
    """Return source_id string or None."""
    if not source_video:
        return None
    sv = source_video.strip()

    # YouTube URL
    m = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", sv)
    if m:
        return f"yt:{m.group(1)}"

    # Bare YouTube ID (11 chars)
    if YT_ID_RE.match(sv):
        return f"yt:{sv}"

    # GitHub URL
    m = GH_URL_RE.match(sv)
    if m:
        return f"gh:{m.group(1)}/{m.group(2)}"

    # Bare GitHub owner/repo path
    m = GH_PATH_RE.match(sv)
    if m:
        return f"gh:{m.group(1)}/{m.group(2)}"

    return None


def walk_pages():
    """Yield (page_file, shelf_key) for every p_*.md."""
    sections_dir = LIB_ROOT / "sections"
    if not sections_dir.exists():
        return
    for page_file in sections_dir.rglob("p_*.md"):
        if page_file.name in (
            "shelf.yaml",
            "bookcase.yaml",
            "_index.md",
            "section.yaml",
        ):
            continue
        rel = page_file.relative_to(sections_dir)
        # shelf key = section/bookcase/shelf (everything above "pages" / the file itself)
        parts = [p for p in rel.parts[:-1] if p != "pages"]
        shelf_key = "/".join(parts) if parts else "_root"
        yield page_file, shelf_key


def build_slug_map(pages):
    """Return {shelf_key: {slug: count}} for collision detection."""
    counter = {}
    for page_file, shelf_key in pages:
        try:
            text = page_file.read_text()
        except Exception:
            continue
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                fm = yaml.safe_load(parts[1]) or {}
            else:
                fm = {}
        else:
            fm = {}
        title = fm.get("title") or ""
        slug = to_kebab(title)
        counter.setdefault(shelf_key, {})
        counter[shelf_key][slug] = counter[shelf_key].get(slug, 0) + 1
    return counter


def main():
    parser = argparse.ArgumentParser(description="Backfill slug and source_id fields.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write changes. Without this flag runs dry-run.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Stop after N pages (for testing). Default 0 = all.",
    )
    args = parser.parse_args()

    pages = list(walk_pages())

    # Build slug collision map first
    slug_map = build_slug_map(pages)

    total = len(pages)
    stats = {
        "skipped_has_both": 0,
        "skipped_no_title": 0,
        "slug_added": 0,
        "source_id_added": 0,
        "both_added": 0,
        "no_change": 0,
        "errors": 0,
    }

    slug_counters = {shelf: {} for shelf in slug_map}

    for i, (page_file, shelf_key) in enumerate(pages, 1):
        if args.limit and i > args.limit:
            break

        try:
            text = page_file.read_text()
        except Exception as e:
            print(f"ERROR reading {page_file}: {e}", file=sys.stderr)
            stats["errors"] += 1
            continue

        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                fm = yaml.safe_load(parts[1]) or {}
                body = parts[2]
            else:
                fm = {}
                body = text
        else:
            fm = {}
            body = text

        title = fm.get("title") or ""
        if not title:
            stats["skipped_no_title"] += 1
            continue

        existing_slug = fm.get("slug")
        existing_source_id = fm.get("source_id")

        slug_needs_set = existing_slug is None
        source_id_needs_set = existing_source_id is None

        if not slug_needs_set and not source_id_needs_set:
            stats["no_change"] += 1
            continue

        new_slug = None
        new_source_id = None

        # Generate slug (deduped within shelf)
        if slug_needs_set:
            base_slug = to_kebab(title)
            # Ensure unique within shelf — reserve suffix space before truncation
            used = slug_counters[shelf_key]
            if base_slug in used:
                counter = used[base_slug] + 1
                used[base_slug] = counter
                suffix = f"-{counter}"
                max_base = 60 - len(suffix)
                trimmed = base_slug[:max_base].rstrip("-")
                new_slug = f"{trimmed}{suffix}"
            else:
                used[base_slug] = 1
                new_slug = base_slug

        # Generate source_id
        if source_id_needs_set:
            sv = fm.get("source_video")
            new_source_id = extract_source_id(sv)

        # Validate slug format
        if new_slug and not re.match(r"^[a-z0-9-]{1,60}$", new_slug):
            print(
                f"WARNING invalid slug '{new_slug}' for {page_file.name}, skipping slug",
                file=sys.stderr,
            )
            new_slug = None

        if not new_slug and not new_source_id:
            stats["no_change"] += 1
            continue

        changed = False
        if new_slug:
            fm["slug"] = new_slug
            changed = True
        if new_source_id:
            fm["source_id"] = new_source_id
            changed = True

        if changed:
            if new_slug and new_source_id:
                stats["both_added"] += 1
            elif new_slug:
                stats["slug_added"] += 1
            else:
                stats["source_id_added"] += 1

            if args.apply:
                frontmatter = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
                new_text = f"---\n{frontmatter}---\n{body}"
                page_file.write_text(new_text)

        if not args.apply:
            action = []
            if new_slug:
                action.append(f"slug={new_slug}")
            if new_source_id:
                action.append(f"source_id={new_source_id}")
            print(f"[DRY] {page_file.relative_to(LIB_ROOT)}: {', '.join(action)}")

    # Summary
    print(f"\n=== Summary ({'APPLIED' if args.apply else 'DRY-RUN'}) ===")
    print(f"Total pages scanned : {total}")
    print(f"  slug added         : {stats['slug_added']}")
    print(f"  source_id added    : {stats['source_id_added']}")
    print(f"  both added         : {stats['both_added']}")
    print(f"  no change (exist)  : {stats['no_change']}")
    print(f"  skipped (no title) : {stats['skipped_no_title']}")
    print(f"  errors             : {stats['errors']}")
    changed_total = (
        stats["slug_added"] + stats["source_id_added"] + stats["both_added"]
    )
    print(f"\nPages that would change: {changed_total}")


if __name__ == "__main__":
    main()
