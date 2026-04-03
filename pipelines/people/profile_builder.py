#!/usr/bin/env python3
"""
Build profile pages for each person in the leaderboard.

Reads all inbox entries for a person, sorts by engagement, takes top 20,
formats as markdown profile with frontmatter.

Usage:
    python3 pipelines/people/profile_builder.py
    python3 pipelines/people/profile_builder.py --dry-run
    python3 pipelines/people/profile_builder.py --person @swyx
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")
INBOX_DIR = ROOT / "pipelines" / "people" / "inbox"
PROFILE_SHELF = ROOT / "sections" / "people" / "bookcases" / "people" / "shelves" / "intelligence" / "pages"
LEADERBOARD_FILE = ROOT / "pipelines" / "people" / "leaderboard.yaml"
PROFILE_SHELF_STR = "people/people/intelligence"

sys.path.insert(0, str(ROOT / "queries"))
try:
    from add_book import get_next_page_id
except ImportError as e:
    print(f"ERROR: Could not import add_book: {e}")
    sys.exit(1)


def load_leaderboard() -> list[dict]:
    import yaml
    with open(LEADERBOARD_FILE) as f:
        data = yaml.safe_load(f)
    return data.get("people", [])


def person_id(handle: str) -> str:
    """Generate a URL-safe person ID."""
    return "people_" + handle.lstrip("@").replace("@", "")


def engagement_score(entry: dict) -> int:
    """Compute engagement score: likes + retweets*2 + replies*2."""
    likes = entry.get("likes", 0)
    retweets = entry.get("retweets", 0)
    replies = entry.get("replies", 0)
    return likes + retweets * 2 + replies * 2


def read_person_inbox(handle: str) -> list[dict]:
    """Read and parse inbox JSONL for a handle."""
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


def parse_prediction_status(content: str) -> tuple[str, str]:
    """Parse prediction status from page content. Returns (status, verdict)."""
    content_upper = content.upper()
    if "VALIDATED" in content_upper:
        match = re.search(r'Verdict:\s*VALIDATED\s*\(([^)]+)\)', content, re.IGNORECASE)
        verdict = match.group(1) if match else ""
        return "PREDICTION", f"VALIDATED ({verdict})" if verdict else "VALIDATED"
    if "CONTRADICTED" in content_upper:
        match = re.search(r'Verdict:\s*CONTRADICTED\s*\(?([^)]+)\)?', content, re.IGNORECASE)
        verdict = match.group(1) if match else ""
        return "PREDICTION", f"CONTRADICTED ({verdict})" if verdict else "CONTRADICTED"
    if any(kw in content_upper for kw in ["PREDICTION", "WILL", "BY 202", "FORECAST"]):
        return "PREDICTION", "OPEN"
    return "INSIGHT", ""


def build_profile_content(person: dict, entries: list[dict]) -> str:
    """Build the full markdown profile page for a person."""
    handle = person["handle"]
    name = person["name"]
    tier = person.get("tier", "B")
    bio = person.get("bio", "")
    topics = person.get("topics", [])
    follower_count = person.get("follower_count", 0)
    url = person.get("url", "")
    prediction_tracking = person.get("prediction_tracking", True)

    # Sort by engagement
    sorted_entries = sorted(entries, key=engagement_score, reverse=True)
    top_entries = sorted_entries[:20]

    # Build frontmatter
    insights_count = len(entries)
    prediction_count = sum(1 for e in entries if is_prediction(e.get("content", "")))

    frontmatter = f"""---
id: {person_id(handle)}
handle: "{handle}"
name: "{name}"
tier: {tier}
topics: [{", ".join(topics)}]
bio: "{bio}"
follower_count: {follower_count}
url: "{url}"
prediction_tracking: {str(prediction_tracking).lower()}
prediction_accuracy: 0
insights_count: {insights_count}
prediction_count: {prediction_count}
last_updated: "{datetime.utcnow().strftime("%Y-%m-%d")}"
---

"""

    # Top insights section
    content_parts = ["## Top Insights\n"]

    for i, entry in enumerate(top_entries, 1):
        title = entry.get("title", "")[:100]
        content = entry.get("content", "")
        likes = entry.get("likes", 0)
        retweets = entry.get("retweets", 0)
        replies = entry.get("replies", 0)
        created_at = entry.get("created_at", "")
        insights = entry.get("extracted_insights", [])

        status, verdict = parse_prediction_status(content)
        status_line = f"Status: **{status}**"
        if verdict:
            status_line += f" — Verdict: {verdict}"

        insight_block = f"""### Insight {i}: "{title}"

*{content[:200]}...*

**Engagement**: {likes} likes, {retweets} retweets, {replies} replies | **Date**: {created_at}
{status_line}
"""
        if insights:
            insight_block += "\n**Extracted Claims**:\n"
            for ins in insights:
                insight_block += f"- {ins}\n"

        content_parts.append(insight_block)

    # All insights chronological
    content_parts.append("\n---\n\n## All Insights (chronological)\n")
    chronological = sorted(entries, key=lambda e: e.get("created_at", ""), reverse=True)
    for entry in chronological[:50]:
        title = entry.get("title", "")[:80]
        content = entry.get("content", "")[:150]
        likes = entry.get("likes", 0)
        retweets = entry.get("retweets", 0)
        created_at = entry.get("created_at", "")
        status, verdict = parse_prediction_status(entry.get("content", ""))

        status_tag = f"[{status}]" if status == "PREDICTION" else ""
        verdict_tag = f" ({verdict})" if verdict else ""

        content_parts.append(
            f"- **{created_at}**: \"{title}\" — {likes} likes, {retweets} RTs {status_tag}{verdict_tag}\n"
        )

    return frontmatter + "\n".join(content_parts)


def is_prediction(content: str) -> bool:
    """Check if content contains prediction-like language."""
    content_lower = content.lower()
    prediction_keywords = ["will", "by 202", "by 203", "predict", "forecast", "expect", "should", "must", "going forward"]
    return any(kw in content_lower for kw in prediction_keywords)


def find_existing_profile_page(handle: str) -> Path | None:
    """Find existing profile page for a handle."""
    if not PROFILE_SHELF.exists():
        return None
    pid = person_id(handle)
    candidate = PROFILE_SHELF / f"{pid}.md"
    if candidate.exists():
        return candidate
    # Search by handle in content
    for f in PROFILE_SHELF.glob("*.md"):
        content = f.read_text()
        if f'handle: "{handle}"' in content or f"handle: '{handle}'" in content:
            return f
    return None


def upsert_profile_page(person: dict, entries: list[dict], dry_run: bool = False) -> dict | None:
    """Create or update a person's profile page."""
    handle = person["handle"]
    pid = person_id(handle)

    page_path = find_existing_profile_page(handle)
    page_id = page_path.stem if page_path else get_next_page_id()

    content = build_profile_content(person, entries)

    if dry_run:
        print(f"  [DRY] {handle} -> {pid}.md ({len(entries)} insights)")
        return None

    out_file = PROFILE_SHELF / f"{page_id}.md"
    out_file.write_text(content)
    print(f"  {handle} -> {out_file.name} ({len(entries)} insights)")

    return {"handle": handle, "page_id": page_id, "insights": len(entries)}


def main():
    parser = argparse.ArgumentParser(description="Build person profile pages")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be built")
    parser.add_argument("--person", type=str, help="Only build for specific handle (e.g. @swyx)")
    args = parser.parse_args()

    print("=== People Profile Builder ===")

    people = load_leaderboard()
    if args.person:
        people = [p for p in people if p["handle"] == args.person]
        if not people:
            print(f"Person {args.person} not found in leaderboard")
            return

    print(f"Building profiles for {len(people)} people")

    total_profiles = 0
    for person in people:
        handle = person["handle"]
        entries = read_person_inbox(handle)
        if not entries:
            print(f"  {handle}: no inbox entries, skipping")
            continue

        result = upsert_profile_page(person, entries, dry_run=args.dry_run)
        if result:
            total_profiles += 1

    print(f"\n=== Done: {total_profiles} profiles built ===")


if __name__ == "__main__":
    main()
