#!/usr/bin/env python3
"""
backfill_creator.py — Fill empty/null creator fields from source metadata.

Usage:
    python3 backfill_creator.py [--dry-run] [--apply]

Behaviour:
    - Dry-run is the default: prints counts and proposed changes, writes nothing.
    - --apply rewrites frontmatter via atomic temp-file swap.

Resolution rules (in priority order):
    1. source_video is a YouTube video ID (11-char base64url) -> lookup yt_channel_cache.json
    2. source_video URL contains github.com -> owner = creator
    3. source_video URL contains reddit.com -> subreddit = creator
    4. source_video URL contains youtube.com or youtu.be -> extract video ID -> lookup cache
    5. Otherwise: creator stays empty (no change)
"""

import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MONOREPO = Path("/Users/shaansisodia/SISO_Workspace")
SECTIONS_DIR = MONOREPO / "SISO_Knowledge" / "sections"
CACHE_FILE = MONOREPO / "SISO_Knowledge" / "_index" / "yt_channel_cache.json"
YT_VIDEO_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")
GH_URL_RE   = re.compile(r"github\.com[/:]([^/]+)/")
RD_URL_RE   = re.compile(r"(?:reddit\.com|old\.reddit\.com)/r/([^/]+)/")
YT_URL_RE   = re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})")
# ---------------------------------------------------------------------------

def load_cache() -> dict[str, str]:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as fh:
                return json.load(fh)  # video_id -> channel_name
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def extract_video_id(source_video: str) -> Optional[str]:
    """Return the 11-char YouTube video ID if source_video is a YT video ID or URL."""
    sv = source_video.strip()
    if YT_VIDEO_RE.match(sv):
        return sv
    m = YT_URL_RE.search(sv)
    if m:
        return m.group(1)
    return None


def resolve_creator(source_video: str, cache: dict[str, str]) -> Optional[str]:
    """
    Return the resolved creator string, or None if it cannot be resolved.
    Does NOT return "" — caller decides what to write.
    """
    sv = source_video.strip() if source_video else ""
    if not sv:
        return None

    # 1. YouTube video ID (bare) or extracted from URL -> channel cache
    video_id = extract_video_id(sv)
    if video_id and video_id in cache:
        return cache[video_id]

    # 2. GitHub URL -> owner
    m = GH_URL_RE.search(sv)
    if m:
        return m.group(1)

    # 3. Reddit URL -> subreddit
    m = RD_URL_RE.search(sv)
    if m:
        return m.group(1)

    # 4. YouTube URL but not in cache -> still try bare video ID (for --apply progress)
    if video_id:
        return None  # known but uncached

    return None


def read_frontmatter(path: Path) -> tuple[dict, str]:
    """Parse a page file. Returns (frontmatter_dict, body)."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            import yaml
            fm = yaml.safe_load(parts[1]) or {}
            return fm, parts[2]
    return {}, text


def write_frontmatter(path: Path, fm: dict, body: str) -> None:
    """Atomically rewrite a page file using a temp-file swap."""
    import yaml
    # Write to a temporary file in the same directory (same filesystem -> atomic rename)
    dir_fd, tmp_path = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.tmp.", suffix=".md"
    )
    try:
        with os.fdopen(dir_fd, "w", encoding="utf-8") as fh:
            fh.write("---\n")
            yaml.safe_dump(fm, fh, default_flow_style=False, sort_keys=False, allow_unicode=True)
            fh.write("---\n")
            fh.write(body)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def walk_pages() -> list[Path]:
    """Return sorted list of all p_*.md page files under SECTIONS_DIR."""
    pages: list[Path] = []
    for root, _, files in os.walk(SECTIONS_DIR):
        for fn in sorted(files):
            if fn.startswith("p_") and fn.endswith(".md"):
                pages.append(Path(root) / fn)
    return sorted(pages)


def get_creator(fm: dict) -> tuple[bool, str]:
    """
    Returns (key_exists, value).
    key_exists=True means the frontmatter has an explicit creator field
    (even if the value is empty string — do NOT overwrite).
    key_exists=False means the field is absent.
    """
    if "creator" not in fm:
        return False, ""
    return True, (fm["creator"] or "").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill creator field from source metadata.")
    parser.add_argument(
        "--dry-run", dest="dry_run", action="store_true",
        help="Print changes without writing (default when --apply is absent)"
    )
    parser.add_argument(
        "--apply", dest="apply", action="store_true",
        help="Actually rewrite frontmatter (default is dry-run)"
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Stop after N pages (for testing; 0 = unlimited)"
    )
    args = parser.parse_args()

    # Default to dry-run unless --apply is given
    dry_run = not args.apply

    cache = load_cache()

    pages = walk_pages()
    total = len(pages)
    stats = {
        "no_source_video": 0,
        "creator_already_filled": 0,
        "resolved_yt_cache": 0,
        "resolved_yt_uncached": 0,
        "resolved_gh": 0,
        "resolved_reddit": 0,
        "unresolved": 0,
        "written": 0,
    }
    proposed: list[tuple[Path, str, str]] = []  # (path, old_creator, new_creator)

    for idx, page_path in enumerate(pages):
        if args.limit and idx >= args.limit:
            break

        fm, body = read_frontmatter(page_path)
        creator_exists, current_creator = get_creator(fm)
        sv = fm.get("source_video", "")

        if creator_exists:
            stats["creator_already_filled"] += 1
            continue

        if not sv:
            stats["no_source_video"] += 1
            continue

        resolved = resolve_creator(str(sv), cache)
        if resolved:
            proposed.append((page_path, current_creator, resolved))
            video_id = extract_video_id(str(sv))
            if video_id and video_id in cache:
                stats["resolved_yt_cache"] += 1
            elif video_id:
                stats["resolved_yt_uncached"] += 1
            elif GH_URL_RE.search(str(sv)):
                stats["resolved_gh"] += 1
            elif RD_URL_RE.search(str(sv)):
                stats["resolved_reddit"] += 1
            else:
                stats["resolved_yt_cache"] += 1  # fallback bucket
        else:
            stats["unresolved"] += 1

    # ---------------------------------------------------------------------------
    # Output summary
    # ---------------------------------------------------------------------------
    print("=" * 60)
    print("backfill_creator.py — summary")
    print(f"  Mode        : {'DRY-RUN' if dry_run else 'APPLY'}")
    print(f"  Total pages : {total}")
    print(f"  Already filled     : {stats['creator_already_filled']}")
    print(f"  No source_video    : {stats['no_source_video']}")
    print(f"  Resolved YT (cache): {stats['resolved_yt_cache']}")
    print(f"  Resolved YT (uncached): {stats['resolved_yt_uncached']}")
    print(f"  Resolved GitHub    : {stats['resolved_gh']}")
    print(f"  Resolved Reddit    : {stats['resolved_reddit']}")
    print(f"  Unresolved         : {stats['unresolved']}")
    print(f"  Pages to change    : {len(proposed)}")
    print("=" * 60)

    if dry_run:
        print(f"\nDry-run: no files modified.")
        if proposed:
            print(f"\nTop 10 proposed changes:")
            for path, old, new in proposed[:10]:
                print(f"  {path.relative_to(MONOREPO)}: creator '{old}' -> '{new}'")
            if len(proposed) > 10:
                print(f"  ... and {len(proposed) - 10} more")
    else:
        # Apply mode: rewrite files
        import yaml
        written = 0
        for path, old_creator, new_creator in proposed:
            fm, body = read_frontmatter(path)
            fm["creator"] = new_creator
            try:
                write_frontmatter(path, fm, body)
                written += 1
            except Exception as exc:
                print(f"  ERROR writing {path}: {exc}")
        stats["written"] = written
        print(f"\nApply: {written} files updated.")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
