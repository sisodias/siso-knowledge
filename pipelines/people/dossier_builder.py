#!/usr/bin/env python3
"""Build per-person knowledge dossiers from the registry and media queues."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import (  # noqa: E402
    DEFAULT_DB_PATH,
    PeopleVideoQueue,
    build_person_queries,
    next_collection_action,
    transcript_export_filename,
)
from registry import load_people  # noqa: E402
from source_planner import build_source_plan  # noqa: E402

DEFAULT_DOSSIER_DIR = ROOT / "pipelines" / "people" / "dossiers"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def video_counts(videos: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"candidate": 0, "transcript_ready": 0, "total": len(videos)}
    for video in videos:
        status = video.get("status", "candidate")
        if status == "transcript_ready":
            counts["transcript_ready"] += 1
        else:
            counts["candidate"] += 1
    return counts


def build_dossier(person: dict[str, Any], queue: PeopleVideoQueue, video_limit: int = 20) -> dict[str, Any]:
    videos = queue.list_candidates_for_person(person["slug"], limit=video_limit)
    counts = video_counts(videos)
    video_next_action = next_collection_action(counts["total"], counts["transcript_ready"])
    source_plan = build_source_plan(person)
    next_action = video_next_action if counts["total"] else source_plan["next_source_action"]
    search_queries = [] if person.get("collection_mode") == "corpus-first" else build_person_queries(person, limit=5)

    return {
        "generated_at": utc_now(),
        "name": person["name"],
        "slug": person["slug"],
        "status": person.get("status", "candidate"),
        "tier": person.get("tier", "B"),
        "line": person.get("line", ""),
        "role": person.get("role", ""),
        "collection_mode": person.get("collection_mode", ""),
        "topics": person.get("topics", []),
        "sources": person.get("sources", []),
        "notes": person.get("notes", ""),
        "next_action": next_action,
        "video_next_action": video_next_action,
        "search_queries": search_queries,
        "source_plan": {
            "source_strategy": source_plan["source_strategy"],
            "next_source_action": source_plan["next_source_action"],
            "source_counts": source_plan["source_counts"],
            "source_targets": source_plan["source_targets"][:5],
            "discovery_urls": source_plan["discovery_urls"][:5],
            "curation_notes": source_plan["curation_notes"],
        },
        "video_counts": counts,
        "videos": [
            {
                "video_id": video["video_id"],
                "title": video["title"],
                "url": video["url"],
                "channel_name": video.get("channel_name", ""),
                "priority": video.get("priority", ""),
                "score": video.get("score", 0),
                "status": video.get("status", "candidate"),
                "transcript_path": video.get("transcript_path", ""),
                "suggested_transcript_filename": transcript_export_filename(video)
                if video.get("status") != "transcript_ready"
                else "",
            }
            for video in videos
        ],
    }


def render_dossier_markdown(dossier: dict[str, Any]) -> str:
    lines = [
        f"# {dossier['name']}",
        "",
        f"- Slug: `{dossier['slug']}`",
        f"- Status: `{dossier['status']}`",
        f"- Tier: `{dossier['tier']}`",
        f"- Line: `{dossier['line']}`",
        f"- Role: {dossier['role']}",
        f"- Collection mode: `{dossier['collection_mode']}`",
        f"- Next action: `{dossier['next_action']}`",
        "",
        "## Topics",
        "",
    ]
    if dossier["topics"]:
        lines.extend(f"- {topic}" for topic in dossier["topics"])
    else:
        lines.append("- None yet")

    lines.extend(["", "## Sources", ""])
    if dossier["sources"]:
        for source in dossier["sources"]:
            label = source.get("type", "source")
            url = source.get("url", "")
            lines.append(f"- `{label}` {url}".rstrip())
    else:
        lines.append("- None yet")

    if dossier.get("notes"):
        lines.extend(["", "## Notes", "", dossier["notes"]])

    source_plan = dossier["source_plan"]
    lines.extend(
        [
            "",
            "## Source Plan",
            "",
            f"- Strategy: `{source_plan['source_strategy']}`",
            f"- Next source action: `{source_plan['next_source_action']}`",
            f"- Source targets: `{source_plan['source_counts']['targets']}`",
            "",
        ]
    )
    if source_plan["source_targets"]:
        for target in source_plan["source_targets"]:
            label = f"{target['repository']} / {target['type']}"
            lines.append(f"- `{label}` {target['title']}")
            if target["url"]:
                lines.append(f"  - URL: {target['url']}")
            lines.append(f"  - Rights: `{target['rights_status']}`")
    else:
        lines.append("- None yet")

    if source_plan["curation_notes"]:
        lines.extend(["", "### Curation Notes", ""])
        lines.extend(f"- {note}" for note in source_plan["curation_notes"])

    lines.extend(
        [
            "",
            "## YouTube Search Queries",
            "",
        ]
    )
    if dossier["search_queries"]:
        lines.extend(f"- {query}" for query in dossier["search_queries"])
    else:
        lines.append("- Skipped for this collection mode.")

    lines.extend(
        [
            "",
            "## Video Queue",
            "",
            f"- Video next action: `{dossier['video_next_action']}`",
            f"- Total queued: `{dossier['video_counts']['total']}`",
            f"- Transcript ready: `{dossier['video_counts']['transcript_ready']}`",
            f"- Needs transcript: `{dossier['video_counts']['candidate']}`",
            "",
        ]
    )

    if dossier["videos"]:
        for video in dossier["videos"]:
            lines.extend(
                [
                    f"### {video['title']}",
                    "",
                    f"- URL: {video['url']}",
                    f"- Channel: `{video['channel_name']}`",
                    f"- Status: `{video['status']}`",
                    f"- Priority: `{video['priority']}` | Score: `{video['score']}`",
                ]
            )
            if video["transcript_path"]:
                lines.append(f"- Transcript: `{video['transcript_path']}`")
            elif video["suggested_transcript_filename"]:
                lines.append(
                    "- Suggested transcript export: "
                    f"`pipelines/youtube/inbox/plugin_exports/{video['suggested_transcript_filename']}`"
                )
            lines.append("")
    else:
        lines.append("No videos queued yet.")

    return "\n".join(lines).rstrip() + "\n"


def write_dossiers(
    people: list[dict[str, Any]],
    queue: PeopleVideoQueue,
    output_dir: Path = DEFAULT_DOSSIER_DIR,
    video_limit: int = 20,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)

    dossiers = [build_dossier(person, queue, video_limit=video_limit) for person in people]
    for dossier in dossiers:
        (output_dir / f"{dossier['slug']}.json").write_text(
            json.dumps(dossier, indent=2) + "\n",
            encoding="utf-8",
        )
        (output_dir / f"{dossier['slug']}.md").write_text(
            render_dossier_markdown(dossier),
            encoding="utf-8",
        )

    index = {
        "generated_at": utc_now(),
        "people_count": len(dossiers),
        "people": [
            {
                "slug": dossier["slug"],
                "name": dossier["name"],
                "status": dossier["status"],
                "tier": dossier["tier"],
                "line": dossier["line"],
                "next_action": dossier["next_action"],
                "video_counts": dossier["video_counts"],
                "markdown_path": str(output_dir / f"{dossier['slug']}.md"),
                "json_path": str(output_dir / f"{dossier['slug']}.json"),
            }
            for dossier in dossiers
        ],
    }
    (output_dir / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (output_dir / "README.md").write_text(render_index_markdown(index), encoding="utf-8")
    return index


def render_index_markdown(index: dict[str, Any]) -> str:
    lines = [
        "# People Dossiers",
        "",
        f"Generated: `{index['generated_at']}`",
        f"People: `{index['people_count']}`",
        "",
    ]
    for person in index["people"]:
        counts = person["video_counts"]
        lines.append(
            f"- [{person['name']}]({Path(person['markdown_path']).name})"
            f" - `{person['next_action']}`"
            f" - videos `{counts['total']}` / transcripts `{counts['transcript_ready']}`"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    queue = PeopleVideoQueue(DEFAULT_DB_PATH)
    index = write_dossiers(load_people(), queue, DEFAULT_DOSSIER_DIR)
    print(f"Wrote {index['people_count']} dossiers to {DEFAULT_DOSSIER_DIR}")


if __name__ == "__main__":
    main()
