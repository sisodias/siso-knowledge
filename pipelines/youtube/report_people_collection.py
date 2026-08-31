#!/usr/bin/env python3
"""Write JSON and markdown status reports for person-centered YouTube collection."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import DEFAULT_DB_PATH, DEFAULT_REPORTS_DIR, PeopleVideoQueue, write_collection_report  # noqa: E402
from registry import load_people  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Report per-person YouTube collection status")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--candidate-limit", type=int, default=5)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_REPORTS_DIR / "people_collection_status.json")
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_REPORTS_DIR / "people_collection_status.md")
    args = parser.parse_args()

    people = load_people()
    queue = PeopleVideoQueue(args.db)
    summary = queue.collection_summary(people, candidate_limit=args.candidate_limit)
    write_collection_report(summary, args.json_output, args.markdown_output)

    totals = summary["totals"]
    print(f"Wrote JSON: {args.json_output}")
    print(f"Wrote markdown: {args.markdown_output}")
    print(
        "People: {people} | candidates: {with_candidates} | transcript-ready people: {with_transcripts}".format(
            **totals
        )
    )


if __name__ == "__main__":
    main()
