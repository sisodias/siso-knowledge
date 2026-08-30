#!/usr/bin/env python3
"""Daily Digest Pipeline - Generate summary of new pages added to the library."""
import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta, date, timezone
from pathlib import Path

import yaml

LIB_PATH = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
INDEX_PATH = LIB_PATH / "_index"
MEMORY_PATH = LIB_PATH / "memory" / "daily_digest"


def get_last_run_date() -> str:
    """Get last run date from .last_run marker file."""
    marker_file = MEMORY_PATH / ".last_run"
    if marker_file.exists():
        return marker_file.read_text().strip()
    # Default to 7 days ago if no marker
    return (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")


def save_last_run_date(date: str):
    """Save last run date to marker file."""
    MEMORY_PATH.mkdir(parents=True, exist_ok=True)
    marker_file = MEMORY_PATH / ".last_run"
    marker_file.write_text(date)


def load_manifest() -> dict:
    """Load the page manifest."""
    manifest_path = INDEX_PATH / "_manifest.yaml"
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found at {manifest_path}")
        return {}
    with open(manifest_path) as f:
        return yaml.safe_load(f)


def filter_new_pages(pages: list, since_date: str) -> list:
    """Filter pages added since the given date."""
    since_dt = datetime.strptime(since_date, "%Y-%m-%d").date()
    new_pages = []
    for page in pages:
        extracted_at = page.get("extracted_at")
        if extracted_at:
            # Handle both date objects and strings
            if isinstance(extracted_at, date):
                if extracted_at >= since_dt:
                    new_pages.append(page)
            elif str(extracted_at) >= since_date:
                new_pages.append(page)
    return new_pages


def group_by_shelf(pages: list) -> dict:
    """Group pages by shelf path."""
    groups = defaultdict(list)
    for page in pages:
        shelf = page.get("shelf", "unknown")
        groups[shelf].append(page)
    return dict(groups)


def group_by_creator(pages: list) -> dict:
    """Group pages by creator."""
    groups = defaultdict(list)
    for page in pages:
        creator = page.get("creator", "Unknown")
        groups[creator].append(page)
    return dict(groups)


def count_by_tier(pages: list) -> dict:
    """Count pages by tier."""
    counts = defaultdict(int)
    for page in pages:
        tier = page.get("tier", "B")
        counts[tier] += 1
    return dict(counts)


def get_hot_topics(pages: list) -> list:
    """Get topics with most new pages."""
    shelf_counts = defaultdict(int)
    for page in pages:
        shelf = page.get("shelf", "unknown")
        # Extract topic from shelf path (last component)
        if shelf:
            topic = shelf.split("/")[-1]
            shelf_counts[topic] += 1

    # Sort by count descending
    sorted_topics = sorted(shelf_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_topics[:10]


def generate_digest(pages: list, date: str) -> str:
    """Generate markdown digest."""
    if not pages:
        return f"# Daily Digest - {date}\n\nNo new pages added today.\n"

    # Group data
    by_shelf = group_by_shelf(pages)
    by_creator = group_by_creator(pages)
    tier_counts = count_by_tier(pages)
    hot_topics = get_hot_topics(pages)

    # Build output
    lines = [
        f"# Daily Digest - {date}",
        "",
        f"## New Pages Today ({len(pages)})",
        ""
    ]

    # Tier summary
    tier_line = ", ".join(f"Tier {t}: {c}" for t, c in sorted(tier_counts.items()))
    lines.append(f"**Tiers:** {tier_line}")
    lines.append("")

    # By shelf/topic
    for shelf, shelf_pages in sorted(by_shelf.items(), key=lambda x: len(x[1]), reverse=True):
        count = len(shelf_pages)
        lines.append(f"### {shelf} ({count} new)")
        # List tier A pages first
        tier_a = [p for p in shelf_pages if p.get("tier") == "A"]
        tier_b = [p for p in shelf_pages if p.get("tier") != "A"]
        for p in tier_a + tier_b:
            tier_label = f"**Tier {p.get('tier', 'B')}**" if p.get("tier") == "A" else f"Tier {p.get('tier', 'B')}"
            title = p.get("title", "Untitled")
            creator = p.get("creator", "")
            creator_str = f" - {creator}" if creator else ""
            lines.append(f"- [{p['id']}] {title} ({tier_label}){creator_str}")
        lines.append("")

    # By creator
    if by_creator:
        lines.append("## By Creator")
        lines.append("")
        for creator, creator_pages in sorted(by_creator.items(), key=lambda x: len(x[1]), reverse=True):
            lines.append(f"- **{creator}**: {len(creator_pages)} pages")
        lines.append("")

    # Hot topics
    if hot_topics:
        lines.append("## Hot Topics")
        lines.append("")
        for i, (topic, count) in enumerate(hot_topics, 1):
            lines.append(f"{i}. {topic}: {count} pages")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()}Z")

    return "\n".join(lines)


def run_digest(date: str, since_days: int, dry_run: bool):
    """Run the digest pipeline."""
    # Determine date range
    if date:
        target_date = date
    else:
        target_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    since_date = (datetime.strptime(target_date, "%Y-%m-%d") - timedelta(days=since_days)).strftime("%Y-%m-%d")

    print(f"Generating digest for {target_date} (since {since_days} days: {since_date})")

    # Load manifest
    manifest = load_manifest()
    if not manifest:
        print("ERROR: Could not load manifest")
        return

    all_pages = manifest.get("pages", [])
    print(f"Total pages in manifest: {len(all_pages)}")

    # Filter new pages
    new_pages = filter_new_pages(all_pages, since_date)
    print(f"New pages since {since_date}: {len(new_pages)}")

    if dry_run:
        print("\n[DRY RUN] Would generate digest:")
        print(f"  - Date: {target_date}")
        print(f"  - Pages: {len(new_pages)}")
        return

    # Generate and save digest
    digest = generate_digest(new_pages, target_date)

    # Write digest file
    MEMORY_PATH.mkdir(parents=True, exist_ok=True)
    digest_file = MEMORY_PATH / f"{target_date}.md"
    digest_file.write_text(digest)
    print(f"Written: {digest_file}")

    # Update last run marker
    save_last_run_date(target_date)
    print(f"Updated last run marker: {target_date}")

    print(f"\nDigest generated successfully with {len(new_pages)} pages")


def main():
    parser = argparse.ArgumentParser(description="Generate daily digest of new pages")
    parser.add_argument("--date", type=str, default="",
                        help="Target date for digest (YYYY-MM-DD), default: today")
    parser.add_argument("--since", type=int, default=1,
                        help="Number of days to look back, default: 1")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be generated without writing")
    args = parser.parse_args()

    run_digest(args.date, args.since, args.dry_run)


if __name__ == "__main__":
    main()
