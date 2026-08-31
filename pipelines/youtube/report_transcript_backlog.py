#!/usr/bin/env python3
"""Write the prioritized list of queued videos that still need transcripts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import DEFAULT_DB_PATH, DEFAULT_REPORTS_DIR, PeopleVideoQueue, write_transcript_backlog  # noqa: E402
from registry import load_people  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Report videos that need Chrome-plugin transcript exports")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORTS_DIR / "transcript_backlog.md")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    queue = PeopleVideoQueue(args.db)
    rows = write_transcript_backlog(queue, load_people(), args.output, limit=args.limit)
    print(f"Wrote {len(rows)} transcript backlog rows: {args.output}")


if __name__ == "__main__":
    main()
