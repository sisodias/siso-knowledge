#!/usr/bin/env python3
"""Add a new page to the library."""
import argparse
import fcntl
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

LIB_PATH = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")
MANIFEST_LOCK_TIMEOUT = 60  # seconds


def get_next_page_id() -> str:
    """Get the next available page ID."""
    manifest_path = LIB_PATH / "_index" / "_manifest.yaml"
    if not manifest_path.exists():
        return "p_001"

    with open(manifest_path) as f:
        manifest = yaml.safe_load(f) or {}

    pages = manifest.get("pages", [])
    if not pages:
        return "p_001"

    # Find max ID
    max_id = 0
    for page in pages:
        page_id = page.get("id", "")
        match = re.search(r"p_(\d+)", page_id)
        if match:
            max_id = max(max_id, int(match.group(1)))

    return f"p_{max_id + 1:03d}"


def get_shelf_path(shelf: str) -> Path:
    """Convert shelf path to filesystem path."""
    # shelf format: ai_research/agents/multi_agent -> sections/ai_research/bookcases/agents/shelves/multi_agent/pages
    parts = shelf.split("/")
    if len(parts) >= 3:
        # section/bookcase/shelf
        return LIB_PATH / "sections" / parts[0] / "bookcases" / parts[1] / "shelves" / parts[2] / "pages"
    elif len(parts) == 2:
        # section/shelf (assuming single bookcase)
        return LIB_PATH / "sections" / parts[0] / "bookcases" / parts[1] / "pages"
    return LIB_PATH / "sections" / shelf / "pages"


def create_page(page_id: str, shelf: str, title: str, content: str,
                creator: str, source_video: str = "",
                tags: list = None, links_to: list = None,
                contradicts: Optional[str] = None, tier: str = "C") -> dict:
    """Create a page data structure."""
    tags = tags or []
    links_to = links_to or []

    page = {
        "id": page_id,
        "book_id": f"b_{page_id[2:]}",
        "shelf": shelf,
        "title": title,
        "creator": creator,
        "source_video": source_video,
        "score": 0.0,
        "tier": tier,
        "tags": tags,
        "links_to": links_to,
        "contradicts": contradicts,
        "extracted_at": datetime.utcnow().strftime("%Y-%m-%d")
    }

    # Build frontmatter via yaml.dump (handles quoting/escaping properly)
    fm_dict = {
        "id": page_id,
        "book_id": f"b_{page_id[2:]}",
        "shelf": shelf,
        "title": title,
        "creator": creator,
        "source_video": source_video,
        "score": 0.0,
        "tier": tier,
        "tags": tags,
        "links_to": links_to,
        "contradicts": contradicts,
        "extracted_at": datetime.utcnow().strftime("%Y-%m-%d"),
    }
    fm_text = yaml.dump(fm_dict, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Build markdown content
    md_content = f"""---
{fm_text}---

# {title}

{content}

**Why it matters**: [Add one sentence about why this insight matters]

**Source**: {creator} — {source_video or 'Unknown source'}
"""

    return page, md_content


def add_page(shelf: str, title: str, content: str,
             creator: str, source_video: str = "",
             tags: list = None, links_to: list = None,
             contradicts: Optional[str] = None, tier: str = "C",
             dry_run: bool = False):
    """Add a new page to the library."""
    # Validate shelf exists
    shelf_path = get_shelf_path(shelf)
    if not shelf_path.exists():
        print(f"Error: Shelf does not exist: {shelf}")
        print("\nAvailable shelves (use format: section/bookcase/shelf):")
        seen = set()
        for s in LIB_PATH.rglob("shelf.yaml"):
            rel = s.relative_to(LIB_PATH / "sections")
            # Convert to user-friendly: section/shelf (extract from bookcases/X/shelves/Y)
            parts = rel.parts
            if len(parts) >= 4 and parts[1] == "bookcases" and parts[3] == "shelves":
                friendly = f"{parts[0]}/{parts[2]}/{parts[4]}"
                if friendly not in seen:
                    print(f"  - {friendly}")
                    seen.add(friendly)
        return

    # Get next page ID
    page_id = get_next_page_id()
    print(f"Creating page: {page_id}")

    # Create page data and content
    page, md_content = create_page(
        page_id, shelf, title, content, creator, source_video,
        tags, links_to, contradicts, tier
    )

    if dry_run:
        print("\n[DRY RUN] Would create:")
        print(f"  File: {shelf_path / f'{page_id}.md'}")
        print(f"  Title: {title}")
        print(f"  Shelf: {shelf}")
        print(f"  Creator: {creator}")
        print(f"  Tags: {tags}")
        return

    # Write page file
    page_file = shelf_path / f"{page_id}.md"
    page_file.write_text(md_content)
    print(f"Created: {page_file.relative_to(LIB_PATH)}")

    # Update index incrementally
    update_manifest(page)
    print("Updated _manifest.yaml")

    # Note: For production, would also update book manifest and rebuild FTS
    print("\nNote: Run `rebuild_index.py` to fully update all indexes.")


def update_manifest(page: dict):
    """Incrementally update the manifest with file locking to prevent race conditions."""
    manifest_path = LIB_PATH / "_index" / "_manifest.yaml"
    lock_path = manifest_path.with_suffix(".lock")

    # Acquire exclusive lock with timeout
    lock_start = time.time()
    lock_file = open(lock_path, "w")
    while True:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except IOError:
            if time.time() - lock_start > MANIFEST_LOCK_TIMEOUT:
                lock_file.close()
                print(f"Error: Could not acquire lock on {manifest_path} after {MANIFEST_LOCK_TIMEOUT}s", file=sys.stderr)
                raise TimeoutError(f"Could not acquire lock on {manifest_path}")
            time.sleep(0.1)

    try:
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = yaml.safe_load(f) or {}
        else:
            manifest = {"pages": [], "total_pages": 0}

        manifest["pages"].append(page)
        manifest["total_pages"] = len(manifest["pages"])

        # Write to temp file first, then rename for atomicity
        temp_path = manifest_path.with_suffix(".tmp")
        with open(temp_path, "w") as f:
            yaml.dump(manifest, f, default_flow_style=False)
        temp_path.rename(manifest_path)
    finally:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()


def main():
    parser = argparse.ArgumentParser(
        description="Add a new page to the library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python add_book.py --shelf ai_research/agents/multi_agent \\
      --creator "Latent Space" --title "Multi-agent coordination patterns" \\
      --content "Agents can coordinate via..." --tags memory,serialization

  python add_book.py --shelf ai_research/llms/reasoning \\
      --creator "3Blue1Brown" --title "Chain of thought visualization" \\
      --content "Chain of thought shows..." --links-to p_001,p_015 --dry-run
        """
    )
    parser.add_argument("--shelf", required=True,
                        help="Shelf path (e.g., ai_research/agents/multi_agent)")
    parser.add_argument("--creator", required=True,
                        help="Content creator/source")
    parser.add_argument("--title", required=True,
                        help="Page title")
    parser.add_argument("--content", required=True,
                        help="Page content/insight")
    parser.add_argument("--source-video", default="",
                        help="Source video ID or URL")
    parser.add_argument("--tags", default="",
                        help="Comma-separated tags")
    parser.add_argument("--links-to", default="",
                        help="Comma-separated page IDs this links to")
    parser.add_argument("--contradicts", default=None,
                        help="Page ID this contradicts")
    parser.add_argument("--tier", choices=["A", "B", "C"], default="C",
                        help="Page tier (default: C)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be created without writing")
    args = parser.parse_args()

    # Parse tags and links
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    links_to = [l.strip() for l in args.links_to.split(",") if l.strip()]

    add_page(
        shelf=args.shelf,
        title=args.title,
        content=args.content,
        creator=args.creator,
        source_video=args.source_video,
        tags=tags,
        links_to=links_to,
        contradicts=args.contradicts,
        tier=args.tier,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
