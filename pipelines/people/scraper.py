#!/usr/bin/env python3
"""
Scrape Twitter/X for leaderboard handles and output JSONL to inbox/.

Usage:
    python3 pipelines/people/scraper.py
    python3 pipelines/people/scraper.py --dry-run
"""
import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")
INBOX_DIR = ROOT / "pipelines" / "people" / "inbox"
LEADERBOARD_FILE = ROOT / "pipelines" / "people" / "leaderboard.yaml"
LAST_SCRAPED_FILE = ROOT / "pipelines" / "people" / ".last_scraped"

# Prediction-like language patterns
PREDICTION_PATTERNS = [
    r"\bwill\b", r"\bby\s+202\d\b", r"\bby\s+203\d\b",
    r"\b预测\b", r"\bforecast\b", r"\bexpect\b", r"\bpredict\b",
    r"\bin\s+\d+\s+years?\b", r"\bby\s+end\s+of\s+\d{4}\b",
    r"\bgoing\s+forward\b", r"\bAI\s+will\b", r"\bLLMs?\s+will\b",
    r"\bagents?\s+will\b", r"\bautonomous\b.*\bwill\b",
]


def load_leaderboard() -> list[dict]:
    """Load people from leaderboard.yaml."""
    import yaml
    with open(LEADERBOARD_FILE) as f:
        data = yaml.safe_load(f)
    return data.get("people", [])


def load_last_scraped() -> set[str]:
    """Load set of already-scraped tweet IDs."""
    if not LAST_SCRAPED_FILE.exists():
        return set()
    return set(LAST_SCRAPED_FILE.read_text().strip().splitlines())


def save_last_scraped(ids: set[str]):
    """Persist scraped tweet IDs."""
    LAST_SCRAPED_FILE.write_text("\n".join(sorted(ids)) + "\n")


def is_prediction(content: str) -> bool:
    """Check if content contains prediction-like language."""
    content_lower = content.lower()
    for pattern in PREDICTION_PATTERNS:
        if re.search(pattern, content_lower):
            return True
    return False


def extract_insights(content: str) -> list[str]:
    """Extract claim-like phrases from content."""
    insights = []
    sentences = re.split(r'[.!?\n]+', content)
    for sent in sentences:
        sent = sent.strip()
        if len(sent) > 30 and (is_prediction(sent) or any(kw in sent.lower() for kw in ["ai", "llm", "agent", "model", "will", "should", "must"])):
            insights.append(sent)
    return insights[:3]  # max 3 insights per tweet


def try_snscrape(handle: str, dry_run: bool = False) -> list[dict]:
    """Try snscrape first."""
    try:
        import snscrape.modules.twitter as sntwitter
    except ImportError:
        return []

    handle_clean = handle.lstrip("@")
    tweets = []
    scraped_ids = load_last_scraped()

    try:
        for i, tweet in enumerate(sntwitter.TwitterUserScraper(handle_clean).get_items()):
            if i >= 100:  # limit per run
                break

            tweet_id = str(tweet.id)
            likes = getattr(tweet, 'likeCount', 0) or 0
            retweets = getattr(tweet, 'retweetCount', 0) or 0
            replies = getattr(tweet, 'replyCount', 0) or 0

            # Skip already scraped
            if tweet_id in scraped_ids:
                continue

            content = tweet.content or ""
            engagement = likes + retweets * 2 + replies * 2

            # Keep if >5 likes OR prediction-like
            if engagement > 5 or is_prediction(content):
                entry = {
                    "id": tweet_id,
                    "title": content[:80] + ("..." if len(content) > 80 else ""),
                    "content": content,
                    "creator": handle,
                    "created_at": tweet.date.strftime("%Y-%m-%d") if hasattr(tweet, 'date') else "",
                    "likes": likes,
                    "retweets": retweets,
                    "replies": replies,
                    "tags": [],
                    "extracted_insights": extract_insights(content),
                }
                tweets.append(entry)
                scraped_ids.add(tweet_id)

    except Exception as e:
        print(f"  snscrape error for {handle}: {e}")

    if tweets:
        save_last_scraped(scraped_ids)

    return tweets


def try_web_scrape(handle: str, dry_run: bool = False) -> list[dict]:
    """Fallback: web scrape Twitter user page."""
    import requests

    handle_clean = handle.lstrip("@")
    url = f"https://x.com/{handle_clean}"
    tweets = []
    scraped_ids = load_last_scraped()

    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code != 200:
            print(f"  HTTP {resp.status_code} for {handle}")
            return []

        html = resp.text
        # Extract tweet IDs and content from Twitter's HTML
        tweet_blocks = re.findall(r'"tweetId":"(\d+)".*?"fullText":"([^"]+)"', html, re.DOTALL)

        for tweet_id, content in tweet_blocks[:50]:
            if tweet_id in scraped_ids:
                continue

            # Simple heuristic: keep high-engagement or prediction-like
            if is_prediction(content) or len(content) > 60:
                entry = {
                    "id": tweet_id,
                    "title": content[:80] + ("..." if len(content) > 80 else ""),
                    "content": content,
                    "creator": handle,
                    "created_at": datetime.utcnow().strftime("%Y-%m-%d"),
                    "likes": 0,
                    "retweets": 0,
                    "replies": 0,
                    "tags": [],
                    "extracted_insights": extract_insights(content),
                }
                tweets.append(entry)
                scraped_ids.add(tweet_id)

    except Exception as e:
        print(f"  web scrape error for {handle}: {e}")

    if tweets:
        save_last_scraped(scraped_ids)

    return tweets


def write_inbox_file(handle: str, entries: list[dict]):
    """Write JSONL entries to inbox file."""
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    handle_clean = handle.lstrip("@")
    out_file = INBOX_DIR / f"{handle_clean}.jsonl"

    # Append new entries (skip duplicates by ID)
    existing_ids = set()
    if out_file.exists():
        for line in out_file.read_text().splitlines():
            try:
                existing_ids.add(json.loads(line)["id"])
            except (json.JSONDecodeError, KeyError):
                pass

    new_entries = [e for e in entries if e["id"] not in existing_ids]
    if not new_entries:
        return 0

    with open(out_file, "a") as f:
        for entry in new_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return len(new_entries)


def main():
    parser = argparse.ArgumentParser(description="Scrape Twitter for leaderboard handles")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be scraped")
    args = parser.parse_args()

    print("=== People Scraper ===")
    people = load_leaderboard()
    print(f"Found {len(people)} people in leaderboard")

    total_written = 0
    for person in people:
        handle = person["handle"]
        print(f"\nScraping {handle}...", end=" ")

        if args.dry_run:
            print(f"[DRY] would scrape")
            continue

        # Try snscrape first
        entries = try_snscrape(handle, dry_run=args.dry_run)

        # Fallback to web scrape
        if not entries:
            print("snscrape failed, trying web...", end=" ")
            entries = try_web_scrape(handle, dry_run=args.dry_run)

        if entries:
            written = write_inbox_file(handle, entries)
            print(f"OK -> {len(entries)} tweets ({written} new)")
            total_written += written
        else:
            print("no new tweets")

    print(f"\n=== Done: {total_written} new entries written ===")


if __name__ == "__main__":
    main()
