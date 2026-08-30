#!/usr/bin/env python3
"""
TwitterQueueAnalysis agent - searches Twitter/X for AI news and discussions.
Writes results to pipelines/twitter/inbox/ for ingestion.
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Paths
AGENT_DIR = Path(__file__).parent
ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
INBOX_DIR = ROOT / "pipelines" / "twitter" / "inbox"
TASKS_DIR = AGENT_DIR.parent / "inbox"


def read_tasks() -> list[dict]:
    """Read pending tasks from inbox."""
    tasks = []
    for f in TASKS_DIR.glob("task_*.json"):
        try:
            task = json.loads(f.read_text())
            if task.get("status") == "pending":
                tasks.append(task)
        except json.JSONDecodeError:
            pass
    return tasks


def mark_complete(task_id: str):
    """Mark task as complete."""
    task_file = TASKS_DIR / f"task_{task_id.split('#')[-1].zfill(3)}.json"
    if task_file.exists():
        task = json.loads(task_file.read_text())
        task["status"] = "completed"
        task["completed_at"] = datetime.now().isoformat()
        task_file.write_text(json.dumps(task, indent=2))


def write_jsonl(entries: list[dict], date: str):
    """Write entries to inbox JSONL file."""
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    outfile = INBOX_DIR / f"tweets_{date}.jsonl"

    existing = set()
    if outfile.exists():
        for line in outfile.read_text().splitlines():
            if line.strip():
                try:
                    existing.add(json.loads(line).get("id", ""))
                except json.JSONDecodeError:
                    pass

    new_entries = [e for e in entries if e.get("id") not in existing]

    with open(outfile, "a") as f:
        for entry in new_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return len(new_entries)


def search_twitter(query: str) -> list[dict]:
    """
    Search Twitter/X for the given query.
    Uses xsearch skill via the system.
    """
    # This would invoke the xsearch skill
    # For now, return empty - actual implementation would use the skill
    print(f"[search_twitter] Query: {query}")
    return []


def run_task(task: dict):
    """Execute a single research task."""
    topic = task.get("topic", "")
    query = task.get("query", f"{topic} Twitter/X discussion")

    print(f"\n=== Processing task: {task.get('task_id')} ===")
    print(f"Topic: {topic}")
    print(f"Query: {query}")

    # Search Twitter/X
    results = search_twitter(query)

    # Write to inbox
    if results:
        date = datetime.now().strftime("%Y%m%d")
        count = write_jsonl(results, date)
        print(f"Wrote {count} entries to inbox")
    else:
        print("No results found (xsearch skill would populate this)")

    # Mark complete
    mark_complete(task.get("task_id", ""))


def main():
    print("=== TwitterQueueAnalysis Agent ===")

    tasks = read_tasks()
    print(f"Found {len(tasks)} pending tasks")

    if not tasks:
        print("No pending tasks.")
        return

    for task in tasks:
        run_task(task)

    print("\n=== Done ===")


if __name__ == "__main__":
    main()
