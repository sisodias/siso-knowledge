#!/usr/bin/env python3
"""
Reddit scraper - fetches hot posts from subreddits using Reddit JSON API.

Usage:
    python3 pipelines/reddit/scraper.py                    # fetch from all configured subs
    python3 pipelines/reddit/scraper.py --sub LocalLLaMA  # fetch from specific sub
    python3 pipelines/reddit/scraper.py --limit 10        # limit posts per sub
"""
import argparse
import json
import urllib.request
from datetime import datetime
from pathlib import Path

SUBREDDITS = ["LocalLLaMA", "MachineLearning", "AIagents", "SideProject", "artificial", "technews"]
ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")
INBOX_DIR = ROOT / "pipelines" / "reddit" / "inbox"


def fetch_subreddit(sub: str, limit: int = 25) -> list[dict]:
    """Fetch hot posts from a subreddit via Reddit JSON API."""
    url = f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}"

    headers = {
        "User-Agent": "SISO-Library-Reddit-Scraper/1.0"
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERROR: Failed to fetch r/{sub}: {e}")
        return []

    posts = []
    children = data.get("data", {}).get("children", [])

    for child in children:
        post = child.get("data", {})
        if not post:
            continue

        # Extract relevant fields
        created_utc = post.get("created_utc", 0)
        created_at = datetime.fromtimestamp(created_utc).strftime("%Y-%m-%d") if created_utc else ""

        posts.append({
            "id": f"reddit#{post.get('id', '')}",
            "source": "reddit",
            "title": post.get("title", ""),
            "content": post.get("selftext", "")[:2000] if post.get("selftext") else "",  # truncate long posts
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "creator": post.get("author", ""),
            "created_at": created_at,
            "subreddit": sub,
            "score": post.get("score", 0),
            "num_comments": post.get("num_comments", 0),
            "tags": extract_tags(post),
        })

    return posts


def extract_tags(post: dict) -> list[str]:
    """Extract tags from post metadata."""
    tags = []

    # Add subreddit as tag
    sub = post.get("subreddit", "").lower()
    if sub:
        tags.append(sub)

    # Check for link posts
    if post.get("is_self"):
        tags.append("text")
    if post.get("is_video"):
        tags.append("video")

    # Check for flairs
    flair = post.get("link_flair_text", "")
    if flair:
        tags.append(flair.lower().replace(" ", "_"))

    # Limit to 5 tags
    return tags[:5]


def write_jsonl(posts: list[dict], sub: str):
    """Write posts to inbox JSONL file."""
    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = INBOX_DIR / f"reddit_{sub.lower()}_{timestamp}.jsonl"

    with open(outfile, "w") as f:
        for post in posts:
            f.write(json.dumps(post) + "\n")

    print(f"  Wrote {len(posts)} posts to {outfile.name}")
    return outfile


def main():
    parser = argparse.ArgumentParser(description="Scrape Reddit for research content")
    parser.add_argument("--sub", type=str, help="Specific subreddit to scrape")
    parser.add_argument("--limit", type=int, default=25, help="Posts per subreddit")
    args = parser.parse_args()

    subreddits = [args.sub] if args.sub else SUBREDDITS

    print(f"=== Reddit Scraper ===")
    print(f"Subreddits: {', '.join(subreddits)}")
    print(f"Limit: {args.limit} posts each")

    total_posts = 0
    for sub in subreddits:
        print(f"\nFetching r/{sub}...")
        posts = fetch_subreddit(sub, args.limit)
        if posts:
            write_jsonl(posts, sub)
            total_posts += len(posts)
        else:
            print(f"  No posts fetched")

    print(f"\n=== Summary ===")
    print(f"Total posts: {total_posts}")


if __name__ == "__main__":
    main()
