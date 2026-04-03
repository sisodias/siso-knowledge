#!/usr/bin/env python3
"""
Ingest people insights from inbox JSONL files to topic shelves.

Reads leaderboard.yaml, reads inbox/{handle}.jsonl for each person,
routes insights to topic shelves, creates/updates profile pages.

Usage:
    python3 pipelines/people/ingest.py
    python3 pipelines/people/ingest.py --dry-run
    python3 pipelines/people/ingest.py --person @swyx
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")
INBOX_DIR = ROOT / "pipelines" / "people" / "inbox"
OUTBOX_DIR = ROOT / "pipelines" / "people" / "outbox"
LEADERBOARD_FILE = ROOT / "pipelines" / "people" / "leaderboard.yaml"
LAST_INGESTED_FILE = ROOT / "pipelines" / "people" / ".last_ingested"

sys.path.insert(0, str(ROOT / "pipelines"))
from shared.topic_router import route_to_shelf, detect_tags

sys.path.insert(0, str(ROOT / "queries"))
try:
    from add_book import add_page, get_next_page_id, get_shelf_path
except ImportError as e:
    print(f"ERROR: Could not import add_book: {e}")
    sys.exit(1)


def load_leaderboard() -> list[dict]:
    import yaml
    with open(LEADERBOARD_FILE) as f:
        data = yaml.safe_load(f)
    return data.get("people", [])


def load_last_ingested() -> set[str]:
    if not LAST_INGESTED_FILE.exists():
        return set()
    return set(LAST_INGESTED_FILE.read_text().strip().splitlines())


def save_last_ingested(ids: set[str]):
    LAST_INGESTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = load_last_ingested()
    updated = existing | ids
    LAST_INGESTED_FILE.write_text("\n".join(sorted(updated)) + "\n")


def read_person_inbox(handle: str) -> list[dict]:
    """Read JSONL inbox file for a handle."""
    handle_clean = handle.lstrip("@")
    inbox_file = INBOX_DIR / f"{handle_clean}.jsonl"
    if not inbox_file.exists():
        return []

    entries = []
    for line in inbox_file.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return entries


def route_insight(entry: dict) -> str:
    """Route an insight to the best topic shelf."""
    combined = (
        entry.get("title", "") + " " +
        entry.get("content", "") + " " +
        " ".join(entry.get("tags", [])) + " " +
        " ".join(entry.get("extracted_insights", []))
    ).lower()

    tags = detect_tags(combined)
    return route_to_shelf(tags, entry.get("title", ""), combined)


def create_insight_page(entry: dict, person: dict, shelf: str, dry_run: bool = False) -> dict | None:
    """Create a library page for a single insight."""
    title = entry.get("title", "Insight")
    content = entry.get("content", "")
    handle = person["handle"]
    name = person["name"]
    tier = person["tier"]
    likes = entry.get("likes", 0)
    retweets = entry.get("retweets", 0)
    replies = entry.get("replies", 0)
    created_at = entry.get("created_at", "")
    insights = entry.get("extracted_insights", [])
    url = entry.get("url", person.get("url", ""))

    # Format content
    full_content = f"**Quote**: {content}\n\n"
    full_content += f"**Author**: {name} ({handle}) — Tier {tier}\n"
    full_content += f"**Date**: {created_at}\n"
    full_content += f"**Engagement**: {likes} likes, {retweets} retweets, {replies} replies\n\n"
    if insights:
        full_content += f"**Extracted Insights**:\n"
        for insight in insights:
            full_content += f"- {insight}\n"
        full_content += "\n"
    full_content += f"**Source**: [Twitter/X]({url})"

    page_tags = ["people", "insight", f"tier_{tier.lower()}"] + person.get("topics", [])
    for t in entry.get("tags", []):
        if t not in page_tags:
            page_tags.append(t)

    if dry_run:
        print(f"  [DRY] {title[:50]} -> {shelf}")
        return None

    add_page(
        shelf=shelf,
        title=title,
        content=full_content,
        creator=f"{name} ({handle})",
        source_video=url,
        tags=",".join(page_tags),
        tier=tier,
        dry_run=False,
    )

    return {"id": entry.get("id", ""), "shelf": shelf}


def ingest_person(person: dict, dry_run: bool = False) -> dict:
    """Ingest all inbox entries for a single person."""
    handle = person["handle"]
    name = person["name"]
    print(f"\nIngesting {handle} ({name})...")

    entries = read_person_inbox(handle)
    if not entries:
        print(f"  No inbox entries for {handle}")
        return {"person": handle, "processed": 0, "created": 0}

    # Filter already-ingested
    tracker = load_last_ingested()
    new_entries = [e for e in entries if e.get("id", "") not in tracker]
    print(f"  {len(new_entries)} new entries (already ingested: {len(entries) - len(new_entries)})")

    if dry_run:
        for e in new_entries[:10]:
            shelf = route_insight(e)
            print(f"  [DRY] {e.get('title', '?')[:50]} -> {shelf}")
        return {"person": handle, "processed": 0, "created": 0}

    processed = 0
    created = 0
    new_ids = set()

    for i, entry in enumerate(new_entries):
        entry_id = entry.get("id", f"entry-{i}")
        shelf = route_insight(entry)
        result = create_insight_page(entry, person, shelf, dry_run=False)
        if result:
            created += 1
            new_ids.add(entry_id)
        processed += 1

    if new_ids:
        save_last_ingested(new_ids)

    return {"person": handle, "processed": processed, "created": created}


def main():
    parser = argparse.ArgumentParser(description="Ingest people insights to topic shelves")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be ingested")
    parser.add_argument("--person", type=str, help="Only ingest for a specific handle (e.g. @swyx)")
    parser.add_argument("--limit", type=int, default=0, help="Limit entries per person (0=all)")
    args = parser.parse_args()

    print("=== People Ingest ===")
    print(f"Library: {ROOT}")

    people = load_leaderboard()
    if args.person:
        people = [p for p in people if p["handle"] == args.person]
        if not people:
            print(f"Person {args.person} not found in leaderboard")
            return

    print(f"Processing {len(people)} people")

    total_created = 0
    for person in people:
        result = ingest_person(person, dry_run=args.dry_run)
        total_created += result["created"]

    print(f"\n=== Summary ===")
    print(f"People processed: {len(people)}")
    print(f"Pages created: {total_created}")

    if total_created > 0:
        print(f"\nRun: python3 queries/rebuild_index.py  # to update indexes")


if __name__ == "__main__":
    main()
