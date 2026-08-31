#!/usr/bin/env python3
"""Refresh the people YouTube queue, exports, and status reports in one command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")


def run_step(args: list[str]) -> None:
    print(f"\n$ {' '.join(args)}")
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the safe people YouTube collection setup")
    parser.add_argument("--limit-per-person", type=int, default=10)
    parser.add_argument("--query-limit", type=int, default=5)
    parser.add_argument("--export-limit", type=int, default=50)
    parser.add_argument("--min-tier", choices=["A", "B", "C"], default="C")
    args = parser.parse_args()

    run_step(
        [
            sys.executable,
            "pipelines/youtube/discover_people_videos.py",
            "--dry-run",
            "--limit-per-person",
            str(args.query_limit),
        ]
    )
    run_step(
        [
            sys.executable,
            "pipelines/youtube/seed_existing_research.py",
            "--limit-per-person",
            str(args.limit_per_person),
        ]
    )
    run_step(
        [
            sys.executable,
            "pipelines/youtube/import_search_results_batch.py",
            "--dir",
            "pipelines/youtube/search_results",
            "--source",
            "search_results_batch",
        ]
    )
    run_step([sys.executable, "pipelines/youtube/import_plugin_exports_batch.py"])
    run_step(
        [
            sys.executable,
            "pipelines/youtube/export_people_ready.py",
            "--min-tier",
            args.min_tier,
            "--limit",
            str(args.export_limit),
        ]
    )
    run_step([sys.executable, "pipelines/youtube/report_people_collection.py"])
    run_step([sys.executable, "pipelines/youtube/report_transcript_backlog.py"])
    run_step([sys.executable, "pipelines/people/source_planner.py"])
    run_step([sys.executable, "pipelines/people/source_ingest.py"])
    run_step([sys.executable, "pipelines/people/external_dataset_reporter.py"])
    run_step([sys.executable, "pipelines/people/dossier_builder.py"])


if __name__ == "__main__":
    main()
