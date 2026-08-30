#!/usr/bin/env python3
"""
RedditQueueAnalysis agent - scraper runner.

Checks inbox for tasks, runs scraper, writes to pipeline inbox,
then runs ingest.py to add to SISO_Knowledge.

Usage:
    python3 agents/RedditQueueAnalysis/workspace/scraper_runner.py
    python3 agents/RedditQueueAnalysis/workspace/scraper_runner.py --dry-run
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge/agents/RedditQueueAnalysis")
INBOX_DIR = AGENT_DIR / "inbox"
WORKSPACE_DIR = AGENT_DIR / "workspace"
PIPELINE_DIR = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge/pipelines/reddit")
SCRAPER_SCRIPT = PIPELINE_DIR / "scraper.py"
INGEST_SCRIPT = PIPELINE_DIR / "ingest.py"


def load_pending_tasks() -> list[dict]:
    """Load pending tasks from inbox."""
    tasks = []
    for f in sorted(INBOX_DIR.glob("*.json")):
        try:
            task = json.loads(f.read_text())
            if task.get("status") == "pending":
                tasks.append(task)
        except Exception as e:
            print(f"WARNING: Failed to load {f}: {e}")
    return tasks


def mark_task_complete(task_id: str):
    """Mark task as complete in inbox."""
    for f in INBOX_DIR.glob("*.json"):
        try:
            task = json.loads(f.read_text())
            if task.get("id") == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write_text(json.dumps(task, indent=2))
                print(f"Marked {task_id} as completed")
                return
        except Exception:
            pass


def run_scraper(subreddits: list[str] = None, limit: int = 25, dry_run: bool = False):
    """Run the Reddit scraper."""
    cmd = [sys.executable, str(SCRAPER_SCRIPT)]
    if subreddits:
        for sub in subreddits:
            cmd.extend(["--sub", sub])
    cmd.extend(["--limit", str(limit)])

    print(f"Running: {' '.join(cmd)}")
    if dry_run:
        print("[DRY RUN] Would run scraper")
        return

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    return result.returncode == 0


def run_ingest(dry_run: bool = False):
    """Run the Reddit ingest script."""
    cmd = [sys.executable, str(INGEST_SCRIPT)]

    print(f"Running: {' '.join(cmd)}")
    if dry_run:
        print("[DRY RUN] Would run ingest")
        return

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="RedditQueueAnalysis scraper runner")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--skip-scraper", action="store_true", help="Skip scraper, only run ingest")
    parser.add_argument("--skip-ingest", action="store_true", help="Skip ingest, only run scraper")
    args = parser.parse_args()

    print("=== RedditQueueAnalysis Agent ===")

    # Load pending tasks
    tasks = load_pending_tasks()
    print(f"Found {len(tasks)} pending tasks")

    if not tasks:
        print("No pending tasks. Running default scrape...")

    # Determine subreddits and limit from tasks or use defaults
    subreddits = None
    limit = 25
    for task in tasks:
        if "subreddits" in task:
            subreddits = task["subreddits"]
        if "limit" in task:
            limit = task["limit"]

    # Run scraper
    if not args.skip_scraper:
        success = run_scraper(subreddits, limit, args.dry_run)
        if not success:
            print("ERROR: Scraper failed")
            return 1

    # Run ingest
    if not args.skip_ingest:
        success = run_ingest(args.dry_run)
        if not success:
            print("ERROR: Ingest failed")
            return 1

    # Mark tasks complete
    if not args.dry_run:
        for task in tasks:
            mark_task_complete(task.get("id", ""))

    print("\n=== Done ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
