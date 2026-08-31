#!/usr/bin/env python3
"""Import a user-provided YouTube transcript export into the people video queue."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import DEFAULT_DB_PATH, DEFAULT_TRANSCRIPTS_DIR, PeopleVideoQueue, import_plugin_transcript  # noqa: E402
from registry import people_by_slug  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a Chrome-plugin YouTube transcript export")
    parser.add_argument("--file", type=Path, required=True, help="Transcript text/markdown file exported from the plugin")
    parser.add_argument("--video-url", required=True, help="YouTube video URL")
    parser.add_argument("--person", required=True, help="Person slug from pipelines/people/leaderboard.yaml")
    parser.add_argument("--title", default="", help="Video title, if known")
    parser.add_argument("--channel", default="", help="Channel name, if known")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_TRANSCRIPTS_DIR)
    args = parser.parse_args()

    people = people_by_slug()
    if args.person not in people:
        known = ", ".join(sorted(people)[:20])
        raise SystemExit(f"Unknown person slug: {args.person}. Examples: {known}")

    queue = PeopleVideoQueue(args.db)
    output_path = import_plugin_transcript(
        transcript_file=args.file,
        video_url=args.video_url,
        person=people[args.person],
        title=args.title,
        channel_name=args.channel,
        output_dir=args.output_dir,
        queue=queue,
    )
    print(f"Imported transcript: {output_path}")
    print(f"Queue stats: {queue.stats()}")


if __name__ == "__main__":
    main()
