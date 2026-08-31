#!/usr/bin/env python3
"""
Web scraper using Perplexity API (via OpenRouter) to search for AI/agent topics.

Usage:
  python3 pipelines/web/scraper.py --query "latest AI agent frameworks 2026"
  python3 pipelines/web/scraper.py --topics agents benchmarks
  python3 pipelines/web/scraper.py --batch
"""
import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Perplexity search via OpenRouter
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY", os.environ.get("OPENROUTER_API_KEY", ""))

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
INBOX_DIR = ROOT / "pipelines" / "web" / "inbox"
OUTBOX_DIR = ROOT / "pipelines" / "web" / "outbox"

# Default AI topics to search
DEFAULT_TOPICS = [
    "AI agents 2026",
    "new LLM frameworks",
    "agent benchmarks",
    "multi-agent systems",
    "Claude Code tools",
    "autonomous agents research",
]


def search_perplexity(query: str, model: str = "perplexity/sonar-pro") -> dict | None:
    """Run a Perplexity search and return structured results."""
    if not PERPLEXITY_API_KEY:
        print(f"ERROR: PERPLEXITY_API_KEY not set")
        return None

    import requests

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful research assistant. Provide detailed, accurate information with sources."},
            {"role": "user", "content": query}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return {
            "content": result["choices"][0]["message"]["content"],
            "model": model,
        }
    except Exception as e:
        print(f"ERROR: Search failed: {e}")
        return None


def save_result(query: str, result: dict, source: str = "perplexity"):
    """Save search result to inbox JSONL."""
    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    entry = {
        "id": f"web#{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "source": "web",
        "source_name": source,
        "title": query,
        "content": result.get("content", ""),
        "url": result.get("url", ""),
        "creator": "WebQueueAnalysis",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "tags": ["web_search", "ai_research"],
    }

    # Write to inbox with date-based filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    inbox_file = INBOX_DIR / f"search_{date_str}.jsonl"

    with open(inbox_file, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"Saved: {entry['id']} -> {inbox_file}")
    return entry


def run_searches(queries: list[str], model: str = "perplexity/sonar-pro"):
    """Run multiple searches."""
    for query in queries:
        print(f"\nSearching: {query}")
        result = search_perplexity(query, model)
        if result:
            save_result(query, result)
        else:
            print(f"  Skipped: search failed")


def batch_searches():
    """Run searches for default AI topics."""
    run_searches(DEFAULT_TOPICS)


def main():
    parser = argparse.ArgumentParser(description="Web scraper for AI research")
    parser.add_argument("--query", type=str, help="Single search query")
    parser.add_argument("--topics", nargs="+", help="Multiple search topics")
    parser.add_argument("--batch", action="store_true", help="Run default batch searches")
    parser.add_argument("--model", type=str, default="perplexity/sonar-pro",
                        choices=["perplexity/sonar-pro", "perplexity/sonar-reasoning-pro", "perplexity/sonar-deep-research"],
                        help="Perplexity model to use")
    args = parser.parse_args()

    if args.query:
        print(f"Running single query: {args.query}")
        result = search_perplexity(args.query, args.model)
        if result:
            save_result(args.query, result)
    elif args.topics:
        print(f"Running {len(args.topics)} topic searches")
        run_searches(args.topics, args.model)
    elif args.batch:
        print("Running batch searches")
        batch_searches()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
