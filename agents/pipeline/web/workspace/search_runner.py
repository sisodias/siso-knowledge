#!/usr/bin/env python3
"""
WebQueueAnalysis agent: executes web searches and writes results to pipeline inbox.

Usage:
  python3 agents/WebQueueAnalysis/workspace/search_runner.py           # run inbox tasks
  python3 agents/WebQueueAnalysis/workspace/search_runner.py --dry-run
  python3 agents/WebQueueAnalysis/workspace/search_runner.py --query "AI agents 2026"
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")
AGENT_DIR = ROOT / "agents" / "WebQueueAnalysis"
INBOX_DIR = AGENT_DIR / "inbox"
PIPELINE_INBOX = ROOT / "pipelines" / "web" / "inbox"

# Add scripts to path for perplexity_search
SCRIPTS_DIR = ROOT / "agents" / "YouTubeQueueAnalysis" / ".claude" / "skills" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

DEFAULT_TOPICS = [
    "AI agents 2026",
    "new LLM frameworks",
    "agent benchmarks",
    "multi-agent systems",
    "autonomous agents research",
]


def load_inbox_tasks():
    """Load pending tasks from agent inbox."""
    tasks = []
    if not INBOX_DIR.exists():
        return tasks

    for f in INBOX_DIR.glob("*.json"):
        try:
            task = json.loads(f.read_text())
            tasks.append(task)
        except Exception as e:
            print(f"WARNING: Failed to load {f}: {e}")
    return tasks


def run_perplexity_search(query: str) -> dict | None:
    """Execute Perplexity search via the scripts module."""
    try:
        from perplexity_search import search
        result = search(query, model="perplexity/sonar-pro")
        return result
    except ImportError:
        # Fallback: try direct API call
        return fallback_search(query)


def fallback_search(query: str) -> dict | None:
    """Fallback search using direct OpenRouter API."""
    api_key = os.environ.get("PERPLEXITY_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: No API key found")
        return None

    import requests

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "perplexity/sonar-pro",
        "messages": [
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": query}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return {
            "content": result["choices"][0]["message"]["content"],
            "url": "",
        }
    except Exception as e:
        print(f"ERROR: Search failed: {e}")
        return None


def save_to_pipeline(result: dict, query: str):
    """Write search result to pipeline inbox."""
    PIPELINE_INBOX.mkdir(parents=True, exist_ok=True)

    entry = {
        "id": f"web#{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "source": "web",
        "source_name": "perplexity",
        "title": query,
        "content": result.get("content", ""),
        "url": result.get("url", ""),
        "creator": "WebQueueAnalysis",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "tags": ["web_search", "ai_research"],
    }

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_file = PIPELINE_INBOX / f"search_{date_str}.jsonl"

    with open(out_file, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"Saved: {entry['id']} -> {out_file.name}")
    return entry


def run_ingest():
    """Run the pipeline ingest script."""
    ingest_script = ROOT / "pipelines" / "web" / "ingest.py"
    print(f"\nRunning: python3 {ingest_script}")
    os.system(f"python3 {ingest_script}")


def process_task(task: dict, dry_run: bool = False):
    """Process a single search task."""
    query = task.get("query")
    if not query:
        print("WARNING: Task missing query field")
        return

    print(f"Processing: {query}")
    if dry_run:
        print(f"  [DRY] Would search for: {query}")
        return

    result = run_perplexity_search(query)
    if result:
        save_to_pipeline(result, query)
    else:
        print(f"  Search failed for: {query}")


def main():
    parser = argparse.ArgumentParser(description="WebQueueAnalysis search runner")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be searched")
    parser.add_argument("--query", type=str, help="Single search query")
    parser.add_argument("--batch", action="store_true", help="Run default batch topics")
    parser.add_argument("--ingest", action="store_true", help="Run ingest after searches")
    args = parser.parse_args()

    print("=== WebQueueAnalysis ===")

    if args.query:
        process_task({"query": args.query}, dry_run=args.dry_run)
    elif args.batch:
        for topic in DEFAULT_TOPICS:
            process_task({"query": topic}, dry_run=args.dry_run)
    else:
        # Default: process inbox tasks
        tasks = load_inbox_tasks()
        print(f"Found {len(tasks)} inbox tasks")

        for task in tasks:
            process_task(task, dry_run=args.dry_run)

    if args.ingest:
        run_ingest()


if __name__ == "__main__":
    main()
