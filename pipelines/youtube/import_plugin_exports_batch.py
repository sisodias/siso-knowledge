#!/usr/bin/env python3
"""Import plugin transcript exports named person-slug__video-id__title.txt."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import (  # noqa: E402
    DEFAULT_DB_PATH,
    DEFAULT_PLUGIN_INBOX_DIR,
    DEFAULT_TRANSCRIPTS_DIR,
    PeopleVideoQueue,
    import_plugin_export_files,
)
from registry import people_by_slug  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Import Chrome-plugin transcript exports from the inbox")
    parser.add_argument("--dir", type=Path, default=DEFAULT_PLUGIN_INBOX_DIR)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_TRANSCRIPTS_DIR)
    args = parser.parse_args()

    files = sorted([*args.dir.glob("*.txt"), *args.dir.glob("*.md")])
    queue = PeopleVideoQueue(args.db)
    summary = import_plugin_export_files(files, people_by_slug(), output_dir=args.output_dir, queue=queue)
    print(json.dumps(summary, indent=2))
    print(f"Queue stats: {queue.stats()}")


if __name__ == "__main__":
    main()
