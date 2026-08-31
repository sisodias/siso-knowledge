#!/usr/bin/env python3
"""Export transcript-ready people videos into the existing extraction format."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import DEFAULT_DB_PATH, PeopleVideoQueue  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Export ready people videos to /tmp/youtube-prioritized.json")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--output", type=Path, default=Path("/tmp/youtube-prioritized.json"))
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--min-tier", choices=["A", "B", "C"], default="B")
    args = parser.parse_args()

    queue = PeopleVideoQueue(args.db)
    videos = queue.export_prioritized(args.output, limit=args.limit, min_tier=args.min_tier)
    print(f"Exported {len(videos)} transcript-ready videos to {args.output}")


if __name__ == "__main__":
    main()
