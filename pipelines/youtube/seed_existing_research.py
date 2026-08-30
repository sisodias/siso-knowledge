#!/usr/bin/env python3
"""Seed the people video queue from the existing local YouTube research DB."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import DEFAULT_DB_PATH, LEGACY_QUEUE_DB, LEGACY_TRANSCRIPTS_DIR, PeopleVideoQueue, seed_from_existing_queue  # noqa: E402
from registry import load_people, people_by_slug  # noqa: E402


def select_people(slugs: list[str], statuses: set[str]) -> list[dict]:
    people = load_people()
    if slugs:
        by_slug = people_by_slug(people)
        missing = [slug for slug in slugs if slug not in by_slug]
        if missing:
            raise ValueError(f"Unknown people slugs: {', '.join(missing)}")
        return [by_slug[slug] for slug in slugs]
    return [person for person in people if person.get("status") in statuses]


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed people video candidates from the local YouTube research queue")
    parser.add_argument("--person", action="append", default=[], help="Person slug to include; can be repeated")
    parser.add_argument("--status", action="append", default=["approved", "candidate", "maybe"], help="Status to include")
    parser.add_argument("--source-db", type=Path, default=LEGACY_QUEUE_DB)
    parser.add_argument("--transcripts-dir", type=Path, default=LEGACY_TRANSCRIPTS_DIR)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--limit-per-person", type=int, default=10)
    parser.add_argument("--no-replace-source", action="store_true", help="Keep previously seeded legacy rows")
    args = parser.parse_args()

    people = select_people(args.person, set(args.status))
    queue = PeopleVideoQueue(args.db)
    summary = seed_from_existing_queue(
        source_db=args.source_db,
        queue=queue,
        people=people,
        limit_per_person=args.limit_per_person,
        transcripts_dir=args.transcripts_dir,
        replace_existing_source=not args.no_replace_source,
    )
    print(json.dumps(summary, indent=2))
    print(f"Queue stats: {queue.stats()}")


if __name__ == "__main__":
    main()
