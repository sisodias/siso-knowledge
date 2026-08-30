#!/usr/bin/env python3
"""
Ingest Twitter/X research from TwitterQueueAnalysis workspace into SISO_Knowledge.

Reads inbox JSONL files, parses each tweet entry, routes by domain to the
appropriate shelf, creates pages via add_book.py, and calls rebuild_index.py
after the batch.

Usage:
    python3 pipelines/twitter/ingest.py
    python3 pipelines/twitter/ingest.py --dry-run
    python3 pipelines/twitter/ingest.py --limit 10
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
INBOX_DIR = ROOT / "pipelines" / "twitter" / "inbox"
OUTBOX_DIR = ROOT / "pipelines" / "twitter" / "outbox"
TRACKER_FILE = ROOT / "pipelines" / "twitter" / ".last_ingested"

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
                entry = json.loads(line)
                entries.append(entry)
            except json.JSONDecodeError:
                pass
    return entries


def route_tweet(entry: dict) -> str:
    """Determine the best shelf for a tweet entry."""
    combined = (
        entry.get("title", "") + " " +
        entry.get("content", "") + " " +
        " ".join(entry.get("tags", []))
    ).lower()

    tags = detect_tags(combined)
    return route_to_shelf(tags, entry.get("title", ""), combined)


def determine_tier(entry: dict) -> str:
    """Assign tier based on engagement and content quality."""
    # Use engagement metrics if available
    likes = entry.get("likes", 0)
    retweets = entry.get("retweets", 0)
    replies = entry.get("replies", 0)
    engagement = likes + retweets * 2 + replies * 2

    content_len = len(entry.get("content", ""))

    if engagement > 1000 and content_len > 200:
        return "A"
    elif engagement > 100 or content_len > 100:
        return "B"
    return "C"


def ingest_entry(entry: dict, dry_run: bool = False) -> dict | None:
    """Create a library page for a single tweet entry."""
    sys.path.insert(0, str(ROOT / "queries"))
    try:
        from add_book import add_page, get_next_page_id, get_shelf_path
    except ImportError as e:
        print(f"  ERROR: Could not import add_book: {e}")
        return None

    shelf = route_tweet(entry)
    shelf_path = get_shelf_path(shelf)
    if not shelf_path.exists():
        print(f"  WARNING: Shelf not found: {shelf}")
        shelf = "discovery/social/twitter"
        shelf_path = get_shelf_path(shelf)

    tier = determine_tier(entry)

    # Build content
    title = entry.get("title", "")
    content = entry.get("content", "")
    url = entry.get("url", "")
    creator = entry.get("creator", "")
    created_at = entry.get("created_at", "")
    tags = entry.get("tags", [])

    full_content = f"**Tweet**: {content}\n\n"
    if creator:
        full_content += f"**Author**: {creator}\n"
    if created_at:
        full_content += f"**Date**: {created_at}\n"
    full_content += f"\n**Why it matters**: Twitter/X discussions provide real-time insights into AI trends and community sentiment.\n\n"
    full_content += f"**Source**: [Twitter/X]({url})"

    page_tags = ["twitter", "social_media"] + [shelf.split("/")[-1]]
    for t in tags:
        if t not in page_tags:
            page_tags.append(t)

    if dry_run:
        print(f"  [DRY] {title[:50]} -> {shelf}")
        print(f"        {content[:80]}...")
        return None

    add_page(
        shelf=shelf,
        title=title,
        content=full_content,
        creator=creator or "TwitterQueueAnalysis",
        source_video=url,
        tags=",".join(page_tags),
        tier=tier,
        dry_run=False,
    )

    return {
        "id": entry.get("id", ""),
        "shelf": shelf,
        "tier": tier,
    }


def main():
    parser = argparse.ArgumentParser(description="Ingest Twitter/X research into SISO_Knowledge")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be ingested")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of entries (0=all)")
    args = parser.parse_args()

    print(f"=== Twitter/X Ingest ===")
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
            shelf = route_tweet(e)
            print(f"  {e.get('title', '?')[:50]} -> {shelf}")
        return

    # Process entries
    created = []
    new_ids = set()
    for i, entry in enumerate(entries):
        entry_id = entry.get("id", f"entry-{i}")
        print(f"[{i+1}/{len(entries)}] {entry_id}...", end=" ")
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
