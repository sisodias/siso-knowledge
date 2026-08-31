#!/usr/bin/env python3
"""Import YouTube candidates from Firecrawl/Perplexity/search result JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import DEFAULT_DB_PATH, PeopleVideoQueue, import_search_results  # noqa: E402
from registry import people_by_slug  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Import YouTube candidates from search result JSON")
    parser.add_argument("--file", type=Path, required=True, help="Search results JSON file")
    parser.add_argument("--person", required=True, help="Person slug")
    parser.add_argument("--source", default="search_results", help="Source label for queue provenance")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    args = parser.parse_args()

    people = people_by_slug()
    if args.person not in people:
        raise SystemExit(f"Unknown person slug: {args.person}")
    payload = json.loads(args.file.read_text(encoding="utf-8"))

    queue = PeopleVideoQueue(args.db)
    imported = import_search_results(payload, people[args.person], queue=queue, source=args.source)
    print(f"Imported {len(imported)} YouTube candidates for {people[args.person]['name']}")
    for candidate in imported[:10]:
        print(f"- {candidate.video_id} | {candidate.title} | {candidate.url}")
    print(f"Queue stats: {queue.stats()}")


if __name__ == "__main__":
    main()
