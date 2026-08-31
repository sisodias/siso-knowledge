#!/usr/bin/env python3
"""
Ingest Web research from WebQueueAnalysis workspace into SISO_Knowledge.

Reads inbox JSONL files, parses each web search entry,
routes by domain to the appropriate shelf, creates pages via add_book.py,
and calls rebuild_index.py after the batch.

Usage:
  python3 pipelines/web/ingest.py         # ingest from inbox
  python3 pipelines/web/ingest.py --dry-run
  python3 pipelines/web/ingest.py --limit 5
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime

import yaml

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
INBOX_DIR = ROOT / "pipelines" / "web" / "inbox"
OUTBOX_DIR = ROOT / "pipelines" / "web" / "outbox"
TRACKER_FILE = ROOT / "pipelines" / "web" / ".last_ingested"

sys.path.insert(0, str(ROOT / "pipelines"))
from shared.topic_router import route_to_shelf, detect_tags


def load_tracker() -> set[str]:
    if not TRACKER_FILE.exists():
        return set()
    return set(TRACKER_FILE.read_text().strip().splitlines())


def save_tracker(ids: set[str]):
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = load_tracker()
    updated = existing | ids
    TRACKER_FILE.write_text("\n".join(sorted(updated)) + "\n")


def parse_inbox_jsonl() -> list[dict]:
    """Parse JSONL inbox files."""
    if not INBOX_DIR.exists():
        return []

    entries = []
    for f in sorted(INBOX_DIR.glob("*.jsonl")):
        for line in f.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                import json
                entry = json.loads(line)
                entries.append(entry)
            except Exception:
                pass
    return entries


def route_entry(entry: dict) -> str:
    """Determine the best shelf for a web search entry."""
    combined = (
        entry.get("title", "") + " " +
        entry.get("content", "") + " " +
        entry.get("description", "")
    ).lower()

    tags = detect_tags(combined)
    return route_to_shelf(tags, entry.get("title", ""), combined)


def determine_tier(entry: dict) -> str:
    """Assign tier based on content quality and source authority."""
    content_len = len(entry.get("content", ""))
    url = entry.get("url", "").lower()

    # High authority sources
    high_authority = ["arxiv.org", "github.com", "huggingface.co", "paperswithcode"]
    is_high_authority = any(domain in url for domain in high_authority)

    if is_high_authority and content_len > 500:
        return "A"
    elif content_len > 200:
        return "B"
    return "C"


def ingest_entry(entry: dict, dry_run: bool = False) -> dict | None:
    """Create a library page for a single web search entry."""
    sys.path.insert(0, str(ROOT / "queries"))
    try:
        from add_book import add_page, get_next_page_id, get_shelf_path
    except ImportError as e:
        print(f"  ERROR: Could not import add_book: {e}")
        return None

    shelf = route_entry(entry)
    shelf_path = get_shelf_path(shelf)
    if not shelf_path.exists():
        print(f"  WARNING: Shelf not found: {shelf}")
        shelf = "infrastructure/llm_serving/inference"
        shelf_path = get_shelf_path(shelf)

    tier = determine_tier(entry)

    # Build content
    title = entry.get("title", "")
    url = entry.get("url", "")
    content = entry.get("content", "")
    source = entry.get("source", "web")
    source_name = entry.get("source_name", "web")
    created_at = entry.get("created_at", datetime.now().strftime("%Y-%m-%d"))

    content_formatted = f"**Source**: [{source_name}]({url})\n\n"
    content_formatted += f"**Content**: {content}\n\n"
    content_formatted += f"**Why it matters**: Web-sourced research on AI agents and related topics.\n\n"
    content_formatted += f"**Found**: {created_at}"

    tags = ["web", "search", source_name]
    detected_tags = detect_tags(content.lower())
    tags.extend(detected_tags)

    if dry_run:
        print(f"  [DRY] {title} -> {shelf}")
        print(f"        {content[:80]}...")
        return None

    add_page(
        shelf=shelf,
        title=title,
        content=content_formatted,
        creator="WebQueueAnalysis",
        source_video=url,
        tags=",".join(set(tags)),
        tier=tier,
        dry_run=False,
    )

    return {
        "title": title,
        "shelf": shelf,
        "tier": tier,
        "source": source_name,
    }


def main():
    parser = argparse.ArgumentParser(description="Ingest Web research into SISO_Knowledge")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be ingested")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of entries (0=all)")
    args = parser.parse_args()

    print(f"=== Web Ingest ===")
    print(f"Library: {ROOT}")

    entries = parse_inbox_jsonl()
    print(f"Found {len(entries)} entries in inbox")

    # Filter out already-ingested
    if entries:
        tracker = load_tracker()
        before = len(entries)
        entries = [e for e in entries if e.get("id") not in tracker]
        print(f"New entries: {len(entries)} (already ingested: {before - len(entries)})")

    if args.limit > 0:
        entries = entries[:args.limit]

    if not entries:
        print("Nothing to ingest.")
        return

    if args.dry_run:
        print("\n[DRY RUN] Would ingest:")
        for e in entries[:30]:
            shelf = route_entry(e)
            print(f"  {e.get('title', '?')} -> {shelf}")
        return

    # Process entries
    created = []
    new_ids = set()
    for i, entry in enumerate(entries):
        entry_id = entry.get("id", f"entry-{i}")
        title = entry.get("title", entry_id)
        print(f"[{i+1}/{len(entries)}] {title}...", end=" ")
        result = ingest_entry(entry, dry_run=False)
        if result:
            created.append(result)
            new_ids.add(entry_id)
            print(f"OK -> {result['shelf']}")
        else:
            print("skipped")

    # Update tracker
    if new_ids:
        save_tracker(new_ids)
        print(f"\nUpdated tracker with {len(new_ids)} entries")

    print(f"\n=== Summary ===")
    print(f"Entries processed: {len(entries)}")
    print(f"Pages created:     {len(created)}")

    if created:
        print(f"\nRun: python3 queries/rebuild_index.py  # to update indexes")


if __name__ == "__main__":
    main()
