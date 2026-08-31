#!/usr/bin/env python3
"""Create people-centered YouTube search plans and queue manual/API candidates."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))
sys.path.insert(0, str(ROOT / "pipelines" / "youtube"))

from acquisition import (  # noqa: E402
    DEFAULT_DB_PATH,
    DEFAULT_REPORTS_DIR,
    PeopleVideoQueue,
    VideoCandidate,
    build_person_queries,
    candidate_score,
    ensure_directories,
    write_query_plan,
)
from registry import load_people, people_by_slug  # noqa: E402

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


def youtube_get_json(url: str, params: dict[str, str]) -> dict:
    request_url = f"{url}?{urlencode(params)}"
    with urlopen(request_url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def discover_with_api(person: dict, queries: list[str], api_key: str, limit_per_person: int) -> list[VideoCandidate]:
    """Use the official YouTube Data API for discovery metadata."""
    candidates: dict[str, VideoCandidate] = {}

    for query in queries:
        search_payload = youtube_get_json(
            YOUTUBE_SEARCH_URL,
            {
                "key": api_key,
                "part": "snippet",
                "type": "video",
                "videoCaption": "any",
                "maxResults": str(min(10, limit_per_person)),
                "q": query,
            },
        )
        for item in search_payload.get("items", []):
            video_id = item.get("id", {}).get("videoId")
            snippet = item.get("snippet", {})
            if not video_id:
                continue
            score, priority = candidate_score(person, query, snippet.get("title", ""))
            existing = candidates.get(video_id)
            if existing and existing.score >= score:
                continue
            candidates[video_id] = VideoCandidate(
                video_id=video_id,
                person_slug=person["slug"],
                person_name=person["name"],
                title=snippet.get("title", video_id),
                url=f"https://www.youtube.com/watch?v={video_id}",
                channel_name=snippet.get("channelTitle", ""),
                channel_id=snippet.get("channelId", ""),
                published_at=snippet.get("publishedAt", ""),
                score=score,
                priority=priority,
                source="youtube_data_api",
                query=query,
            )

    if not candidates:
        return []

    video_ids = ",".join(candidates.keys())
    details = youtube_get_json(
        YOUTUBE_VIDEOS_URL,
        {
            "key": api_key,
            "part": "contentDetails,statistics",
            "id": video_ids,
        },
    )
    duration_by_id = {
        item["id"]: item.get("contentDetails", {}).get("duration", "")
        for item in details.get("items", [])
        if item.get("id")
    }

    enriched = []
    for candidate in candidates.values():
        duration = duration_by_id.get(candidate.video_id, "")
        notes = f"iso8601_duration={duration}" if duration else ""
        enriched.append(VideoCandidate(**{**candidate.__dict__, "notes": notes}))

    return sorted(enriched, key=lambda item: item.score, reverse=True)[:limit_per_person]


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
    parser = argparse.ArgumentParser(description="Discover or plan YouTube videos for people registry entries")
    parser.add_argument("--person", action="append", default=[], help="Person slug to include; can be repeated")
    parser.add_argument("--status", action="append", default=["approved", "candidate", "maybe"], help="Status to include")
    parser.add_argument("--limit-per-person", type=int, default=5)
    parser.add_argument("--dry-run", action="store_true", help="Only write the query plan; do not call YouTube API")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--plan-output", type=Path, default=DEFAULT_REPORTS_DIR / "person_video_queries.json")
    args = parser.parse_args()

    ensure_directories()
    people = select_people(args.person, set(args.status))
    plan = write_query_plan(people, args.plan_output, limit_per_person=args.limit_per_person)
    print(f"Wrote query plan for {plan['people_count']} people: {args.plan_output}")

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if args.dry_run or not api_key:
        reason = "--dry-run" if args.dry_run else "YOUTUBE_API_KEY not set"
        print(f"Discovery queue not populated ({reason}).")
        return

    queue = PeopleVideoQueue(args.db)
    queue.init()
    added = 0
    for person in people:
        queries = build_person_queries(person, limit=args.limit_per_person)
        for candidate in discover_with_api(person, queries, api_key, args.limit_per_person):
            queue.upsert_candidate(candidate)
            added += 1

    print(f"Queued {added} candidate videos in {args.db}")
    print(f"Queue stats: {queue.stats()}")


if __name__ == "__main__":
    main()
