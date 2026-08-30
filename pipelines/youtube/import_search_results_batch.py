#!/usr/bin/env python3
"""Import all recognizable search result JSON files from a directory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import DEFAULT_DB_PATH, PeopleVideoQueue, import_search_result_files  # noqa: E402
from registry import people_by_slug  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Import person-slug*.json search result files")
    parser.add_argument("--dir", type=Path, default=ROOT / "pipelines" / "youtube" / "search_results")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--source", default="search_results_batch")
    args = parser.parse_args()

    files = sorted(args.dir.glob("*.json"))
    queue = PeopleVideoQueue(args.db)
    summary = import_search_result_files(files, people_by_slug(), queue=queue, source=args.source)
    print(json.dumps(summary, indent=2))
    print(f"Queue stats: {queue.stats()}")


if __name__ == "__main__":
    main()
