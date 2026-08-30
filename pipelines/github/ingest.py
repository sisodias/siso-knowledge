#!/usr/bin/env python3
"""
Ingest GitHub research from GitHubQueueAnalysis workspace into SISO_Knowledge.

Reads research-log.md (or inbox JSONL files), parses each repo entry,
routes by domain to the appropriate shelf, creates pages via add_book.py,
and calls rebuild_index.py after the batch.

Usage:
  python3 pipelines/github/ingest.py         # ingest from research-log.md
  python3 pipelines/github/ingest.py --dry-run
  python3 pipelines/github/ingest.py --inbox  # ingest from pipelines/github/inbox/
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
INBOX_DIR = ROOT / "pipelines" / "github" / "inbox"
OUTBOX_DIR = ROOT / "pipelines" / "github" / "outbox"
RESEARCH_LOG = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge/agents/GitHubQueueAnalysis/workspace/research-log.md")
TRACKER_FILE = ROOT / "pipelines" / "github" / ".last_ingested"

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


def parse_research_log(path: Path) -> list[dict]:
    """Parse research-log.md into structured repo entries."""
    if not path.exists():
        print(f"WARNING: research-log.md not found at {path}")
        return []

    content = path.read_text()

    entries = []

    # Split on --- dividers between entries
    chunks = re.split(r"\n---\n", content)

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk or chunk.startswith("# "):
            continue

        # Extract URL — look for github.com link (bold markdown adds ** before/after URL)
        url_match = re.search(r"https://github\.com/[\w\-]+/[\w\-]+", chunk)
        if not url_match:
            continue
        url = url_match.group(0)

        # Extract repo name from URL
        repo_name = url.replace("https://github.com/", "")

        # Extract description — between **Description:** and **Research:**
        desc_match = re.search(r"\*\*Description:\*\*\s*(.+?)\n", chunk, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else ""

        # Extract research findings — between **Research:** and --- or end
        research_match = re.search(r"\*\*Research:\*\*\s*(.+?)(?=\n---|\Z)", chunk, re.DOTALL)
        research = research_match.group(1).strip() if research_match else ""

        # Extract stars from the title line: ### owner/name (12345 stars)
        stars_match = re.search(r"###\s+[\w\-]+/[\w\-]+\s+\(([\d,]+)\s+stars?\)", chunk)
        stars = stars_match.group(1).replace(",", "") if stars_match else "0"

        # Extract title from repo name
        title = repo_name.split("/")[-1].replace("-", " ").replace("_", " ").title()

        if not research:
            continue

        entries.append({
            "repo": repo_name,
            "url": url,
            "title": title,
            "description": description,
            "research": research,
            "stars": stars,
        })

    return entries


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


def route_repo(entry: dict) -> str:
    """Determine the best shelf for a GitHub repo entry."""
    combined = (
        entry.get("title", "") + " " +
        entry.get("description", "") + " " +
        entry.get("research", "")
    ).lower()

    tags = detect_tags(combined)
    return route_to_shelf(tags, entry.get("title", ""), combined)


def determine_tier(entry: dict) -> str:
    """Assign tier based on star count and content quality."""
    try:
        stars = int(entry.get("stars", "0").replace(",", ""))
    except ValueError:
        stars = 0

    research_len = len(entry.get("research", ""))

    if stars > 10000 and research_len > 200:
        return "A"
    elif stars > 1000 or research_len > 100:
        return "B"
    return "C"


def ingest_entry(entry: dict, dry_run: bool = False) -> dict | None:
    """Create a library page for a single repo entry."""
    sys.path.insert(0, str(ROOT / "queries"))
    try:
        from add_book import add_page, get_next_page_id, get_shelf_path
    except ImportError as e:
        print(f"  ERROR: Could not import add_book: {e}")
        return None

    shelf = route_repo(entry)
    shelf_path = get_shelf_path(shelf)
    if not shelf_path.exists():
        print(f"  WARNING: Shelf not found: {shelf}")
        shelf = "infrastructure/llm_serving/inference"
        shelf_path = get_shelf_path(shelf)

    tier = determine_tier(entry)

    # Build content
    repo = entry.get("repo", "")
    url = entry.get("url", "")
    research = entry.get("research", "")
    description = entry.get("description", "")
    stars = entry.get("stars", "")

    content = f"**Repository**: [{repo}]({url})\n\n"
    if description:
        content += f"**Description**: {description}\n\n"
    if stars:
        content += f"**Stars**: {stars}\n\n"
    content += f"**Research**: {research}\n\n"
    content += f"**Why it matters**: This repo {'is highly starred' if int(stars.replace(',','')) > 5000 else 'provides relevant tooling'} in the AI agents ecosystem.\n\n"
    content += f"**Source**: [GitHub]({url})"

    tags = ["github", "repository", shelf.split("/")[-1]]

    if dry_run:
        print(f"  [DRY] {repo} ({stars} stars) -> {shelf}")
        print(f"        {research[:80]}...")
        return None

    add_page(
        shelf=shelf,
        title=entry.get("title", repo),
        content=content,
        creator="GitHubQueueAnalysis",
        source_video=url,
        tags=",".join(tags),
        tier=tier,
        dry_run=False,
    )

    # Also create a second page in discovery/code/repos shelf for GitHub pipeline
    discovery_content = f"**Repository**: [{repo}](https://github.com/{repo})\n\n"
    if description:
        discovery_content += f"**Description**: {description}\n\n"
    discovery_content += f"**Stars**: {stars}\n\n"
    if research:
        discovery_content += f"**Research**: {research}\n\n"
    discovery_content += f"**Why it matters**: "
    discovery_content += f"**Source**: [GitHub](https://github.com/{repo})"

    add_page(
        shelf="discovery/code/repos",
        title=entry.get("title", repo),
        content=discovery_content,
        creator="GitHubQueueAnalysis",
        source_video=url,
        tags="github,repository,discovery",
        tier=tier,
        dry_run=False,
    )

    return {
        "repo": repo,
        "shelf": shelf,
        "tier": tier,
        "stars": stars,
    }


def main():
    parser = argparse.ArgumentParser(description="Ingest GitHub research into SISO_Knowledge")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be ingested")
    parser.add_argument("--inbox", action="store_true", help="Ingest from inbox JSONL instead of research-log.md")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of entries (0=all)")
    args = parser.parse_args()

    print(f"=== GitHub Ingest ===")
    print(f"Library: {ROOT}")

    if args.inbox:
        entries = parse_inbox_jsonl()
        print(f"Found {len(entries)} entries in inbox")
    else:
        entries = parse_research_log(RESEARCH_LOG)
        print(f"Parsed {len(entries)} repo entries from research-log.md")

        # Filter out already-ingested
        if entries:
            tracker = load_tracker()
            before = len(entries)
            entries = [e for e in entries if e.get("repo") not in tracker]
            print(f"New entries: {len(entries)} (already ingested: {before - len(entries)})")

    if args.limit > 0:
        entries = entries[:args.limit]

    if not entries:
        print("Nothing to ingest.")
        return

    if args.dry_run:
        print("\n[DRY RUN] Would ingest:")
        for e in entries[:30]:
            shelf = route_repo(e)
            print(f"  {e.get('repo', '?')} ({e.get('stars', '?')} stars) -> {shelf}")
        return

    # Process entries
    created = []
    new_ids = set()
    for i, entry in enumerate(entries):
        repo = entry.get("repo", f"entry-{i}")
        print(f"[{i+1}/{len(entries)}] {repo}...", end=" ")
        result = ingest_entry(entry, dry_run=False)
        if result:
            created.append(result)
            new_ids.add(repo)
            print(f"OK -> {result['shelf']}")
        else:
            print("skipped")

    # Update tracker
    if new_ids:
        save_tracker(new_ids)
        print(f"\nUpdated tracker with {len(new_ids)} repos")

    print(f"\n=== Summary ===")
    print(f"Entries processed: {len(entries)}")
    print(f"Pages created:     {len(created)}")

    if created:
        print(f"\nRun: python3 queries/rebuild_index.py  # to update indexes")


if __name__ == "__main__":
    main()
