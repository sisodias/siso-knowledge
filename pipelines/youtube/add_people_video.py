#!/usr/bin/env python3
"""Add a manual person-video candidate without importing a transcript yet."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import DEFAULT_DB_PATH, PeopleVideoQueue  # noqa: E402
from registry import people_by_slug  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a manual YouTube candidate for a person")
    parser.add_argument("--person", required=True, help="Person slug from pipelines/people/leaderboard.yaml")
    parser.add_argument("--video-url", required=True, help="YouTube URL")
    parser.add_argument("--title", default="", help="Video title, if known")
    parser.add_argument("--channel", default="", help="Channel name, if known")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    args = parser.parse_args()

    people = people_by_slug()
    if args.person not in people:
        raise SystemExit(f"Unknown person slug: {args.person}")

    queue = PeopleVideoQueue(args.db)
    candidate = queue.add_manual_video(
        person=people[args.person],
        video_url=args.video_url,
        title=args.title,
        channel_name=args.channel,
    )
    print(f"Queued {candidate.person_name}: {candidate.title} ({candidate.video_id})")
    print(f"Queue stats: {queue.stats()}")


if __name__ == "__main__":
    main()
