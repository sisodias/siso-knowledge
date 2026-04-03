#!/usr/bin/env python3
"""
Ingest Reddit research from RedditQueueAnalysis workspace into SISO_Library.

Reads inbox JSONL files, parses each Reddit post entry,
routes by domain to the appropriate shelf, creates pages via add_book.py,
and calls rebuild_index.py after the batch.

Usage:
    python3 pipelines/reddit/ingest.py         # ingest from inbox
    python3 pipelines/reddit/ingest.py --dry-run
    python3 pipelines/reddit/ingest.py --limit 10
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")
INBOX_DIR = ROOT / "pipelines" / "reddit" / "inbox"
OUTBOX_DIR = ROOT / "pipelines" / "reddit" / "outbox"
TRACKER_FILE = ROOT / "pipelines" / "reddit" / ".last_ingested"

sys.path.insert(0, str(ROOT / "pipelines"))
try:
    from shared.topic_router import route_to_shelf, detect_tags
except ImportError:
    # Fallback if topic_router not available
    def route_to_shelf(tags, title="", content=""):
        return "infrastructure/llm_serving/inference"
    def detect_tags(content):
        return []


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
        print(f"WARNING: Inbox directory not found: {INBOX_DIR}")
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
            except Exception as e:
                print(f"  WARNING: Failed to parse line: {e}")
    return entries


def route_post(entry: dict) -> str:
    """Determine the best shelf for a Reddit post entry."""
    combined = (
        entry.get("title", "") + " " +
        entry.get("content", "")
    ).lower()

    tags = detect_tags(combined)

    # Add subreddit as a tag signal
    sub = entry.get("subreddit", "").lower()
    if sub:
        tags.append(sub)

    return route_to_shelf(tags, entry.get("title", ""), combined)


def determine_tier(entry: dict) -> str:
    """Assign tier based on score and content length."""
    try:
        score = int(entry.get("score", 0))
    except ValueError:
        score = 0

    try:
        comments = int(entry.get("num_comments", 0))
    except ValueError:
        comments = 0

    content_len = len(entry.get("content", ""))

    # High engagement or substantial content = tier A
    if (score > 100 or comments > 50) and content_len > 200:
        return "A"
    elif score > 20 or comments > 10 or content_len > 100:
        return "B"
    return "C"


def ingest_entry(entry: dict, dry_run: bool = False) -> dict | None:
    """Create a library page for a single Reddit post entry."""
    sys.path.insert(0, str(ROOT / "queries"))
    try:
        from add_book import add_page, get_next_page_id, get_shelf_path
    except ImportError as e:
        print(f"  ERROR: Could not import add_book: {e}")
        return None

    post_id = entry.get("id", "")
    shelf = route_post(entry)
    shelf_path = get_shelf_path(shelf)
    if not shelf_path.exists():
        print(f"  WARNING: Shelf not found: {shelf}, using default")
        shelf = "infrastructure/llm_serving/inference"
        shelf_path = get_shelf_path(shelf)

    tier = determine_tier(entry)

    # Build content
    title = entry.get("title", "")
    url = entry.get("url", "")
    content = entry.get("content", "")
    author = entry.get("creator", "")
    subreddit = entry.get("subreddit", "")
    score = entry.get("score", 0)
    num_comments = entry.get("num_comments", 0)
    created_at = entry.get("created_at", "")

    content_text = f"**Title**: {title}\n\n"
    if content:
        content_text += f"**Content**: {content}\n\n"
    content_text += f"**Author**: {author}\n\n"
    content_text += f"**Subreddit**: r/{subreddit}\n\n"
    content_text += f"**Score**: {score}\n\n"
    content_text += f"**Comments**: {num_comments}\n\n"
    content_text += f"**Posted**: {created_at}\n\n"
    content_text += f"**Source**: [Reddit]({url})"

    tags = ["reddit", f"r/{subreddit}"] + entry.get("tags", [])[:3]

    if dry_run:
        print(f"  [DRY] {title[:50]}... -> {shelf} (tier {tier})")
        return None

    try:
        add_page(
            shelf=shelf,
            title=title[:200],  # truncate long titles
            content=content_text,
            creator=author,
            source_video=url,
            tags=",".join(tags),
            tier=tier,
            dry_run=False,
        )
    except Exception as e:
        print(f"  ERROR: Failed to add page: {e}")
        return None

    return {
        "id": post_id,
        "title": title[:50],
        "shelf": shelf,
        "tier": tier,
        "score": score,
    }


def main():
    parser = argparse.ArgumentParser(description="Ingest Reddit posts into SISO_Library")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be ingested")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of entries (0=all)")
    args = parser.parse_args()

    print(f"=== Reddit Ingest ===")
    print(f"Library: {ROOT}")

    entries = parse_inbox_jsonl()
    print(f"Found {len(entries)} entries in inbox")

    if not entries:
        print("No entries to ingest.")
        return

    # Filter out already-ingested
    tracker = load_tracker()
    before = len(entries)
    entries = [e for e in entries if e.get("id") not in tracker]
    print(f"New entries: {len(entries)} (already ingested: {before - len(entries)})")

    if args.limit > 0:
        entries = entries[:args.limit]

    if not entries:
        print("Nothing new to ingest.")
        return

    if args.dry_run:
        print("\n[DRY RUN] Would ingest:")
        for e in entries[:30]:
            shelf = route_post(e)
            title = e.get("title", "?")[:50]
            score = e.get("score", 0)
            print(f"  {title}... (score: {score}) -> {shelf}")
        return

    # Process entries
    created = []
    new_ids = set()
    for i, entry in enumerate(entries):
        post_id = entry.get("id", f"entry-{i}")
        title = entry.get("title", "?")[:30]
        print(f"[{i+1}/{len(entries)}] {title}...", end=" ")
        result = ingest_entry(entry, dry_run=False)
        if result:
            created.append(result)
            new_ids.add(post_id)
            print(f"OK -> {result['shelf']}")
        else:
            print("skipped")

    # Update tracker
    if new_ids:
        save_tracker(new_ids)
        print(f"\nUpdated tracker with {len(new_ids)} posts")

    print(f"\n=== Summary ===")
    print(f"Entries processed: {len(entries)}")
    print(f"Pages created:     {len(created)}")

    if created:
        print(f"\nRun: python3 queries/rebuild_index.py  # to update indexes")


if __name__ == "__main__":
    main()
