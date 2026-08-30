#!/usr/bin/env python3
"""People-centered YouTube discovery, queueing, and transcript import helpers.

This module deliberately keeps three jobs separate:
- discover candidate videos with official metadata APIs or manual URLs
- import transcripts that the user has permission to collect
- export transcript-ready videos into the existing extraction pipeline
"""

from __future__ import annotations

import json
import re
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote_plus, urlparse

import yaml

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
PIPELINE_DIR = ROOT / "pipelines" / "youtube"
DEFAULT_DB_PATH = PIPELINE_DIR / "people_video_queue.sqlite"
DEFAULT_TRANSCRIPTS_DIR = PIPELINE_DIR / "transcripts"
DEFAULT_PLUGIN_INBOX_DIR = PIPELINE_DIR / "inbox" / "plugin_exports"
DEFAULT_REPORTS_DIR = PIPELINE_DIR / "reports"
LEGACY_YOUTUBE_RESEARCH_DIR = ROOT / "apps" / "library-web" / "data" / "youtube-research"
LEGACY_QUEUE_DB = LEGACY_YOUTUBE_RESEARCH_DIR / "database" / "queue.db"
LEGACY_TRANSCRIPTS_DIR = LEGACY_YOUTUBE_RESEARCH_DIR / "database" / "transcripts"

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
TIER_FROM_PRIORITY = {"P0": "A", "P1": "A", "P2": "B", "P3": "C"}
DIRECT_SOURCE_TERMS = {
    "interview",
    "keynote",
    "podcast",
    "lecture",
    "conversation",
    "fireside",
    "talk",
}
LOW_SIGNAL_TERMS = {
    "ambushed",
    "apocalypse",
    "changed everything",
    "exposed",
    "insane",
    "leak",
    "leaked",
    "loses cool",
    "reveals",
    "revealed",
    "shocked",
    "shocking",
    "shocks",
    "stuns",
    "stunned",
    "warning",
}
LOW_SIGNAL_CHANNELS = {
    "ai code king",
    "ai grid",
    "in the world of ai",
}


@dataclass(frozen=True)
class VideoCandidate:
    video_id: str
    person_slug: str
    person_name: str
    title: str
    url: str
    channel_name: str = ""
    channel_id: str = ""
    published_at: str = ""
    duration_seconds: int | None = None
    score: float = 0.0
    priority: str = "P3"
    source: str = "manual"
    query: str = ""
    transcript_path: str = ""
    status: str = "candidate"
    notes: str = ""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ensure_directories() -> None:
    for directory in [PIPELINE_DIR, DEFAULT_TRANSCRIPTS_DIR, DEFAULT_PLUGIN_INBOX_DIR, DEFAULT_REPORTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def extract_video_id(value: str) -> str | None:
    """Extract an 11-character YouTube video ID from a URL or bare ID."""
    if not value:
        return None

    value = value.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value

    parsed = urlparse(value)
    host = parsed.netloc.lower()
    path = parsed.path.strip("/")

    if "youtube.com" in host:
        query_id = parse_qs(parsed.query).get("v", [""])[0]
        if re.fullmatch(r"[A-Za-z0-9_-]{11}", query_id):
            return query_id

        parts = path.split("/")
        if parts and parts[0] in {"shorts", "embed", "live"} and len(parts) > 1:
            candidate = parts[1]
            if re.fullmatch(r"[A-Za-z0-9_-]{11}", candidate):
                return candidate

    if "youtu.be" in host:
        candidate = path.split("/")[0]
        if re.fullmatch(r"[A-Za-z0-9_-]{11}", candidate):
            return candidate

    match = re.search(r"(?:v=|/)([A-Za-z0-9_-]{11})(?:[?&/#]|$)", value)
    return match.group(1) if match else None


def extract_youtube_urls_from_text(value: str) -> list[str]:
    """Extract YouTube watch/short links from arbitrary search result text."""
    if not value:
        return []

    pattern = re.compile(
        r"https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/|embed/|live/)|youtu\.be/)[A-Za-z0-9_\-]{11}[^\s\])<]*"
    )
    urls: list[str] = []
    seen = set()
    for match in pattern.finditer(value):
        url = match.group(0).rstrip(".,;")
        video_id = extract_video_id(url)
        if not video_id or video_id in seen:
            continue
        seen.add(video_id)
        urls.append(url)
    return urls


def build_youtube_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def normalize_match_text(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def person_match_terms(person: dict[str, Any]) -> list[str]:
    terms = [person.get("name", ""), person.get("slug", "").replace("-", " ")]
    for source in person.get("sources", []):
        if source.get("type") == "youtube" and source.get("url"):
            terms.append(source["url"].rstrip("/").split("/")[-1].lstrip("@"))

    deduped = []
    seen = set()
    for term in terms:
        normalized = normalize_match_text(term)
        if len(normalized) < 4 or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
    return deduped


def record_matches_person(record: dict[str, Any], person: dict[str, Any]) -> bool:
    haystack = normalize_match_text(
        " ".join(
            [
                str(record.get("title", "")),
                str(record.get("channel_name", "")),
                str(record.get("channel_slug", "")),
            ]
        )
    )
    if not haystack:
        return False
    return any(term in haystack for term in person_match_terms(person))


def build_person_queries(person: dict[str, Any], limit: int = 8) -> list[str]:
    """Build high-signal YouTube search queries for a registry person."""
    name = person["name"]
    role = person.get("role", "")
    topics = [topic for topic in person.get("topics", []) if isinstance(topic, str)]

    query_templates = [
        f'"{name}" interview',
        f'"{name}" keynote',
        f'"{name}" podcast',
        f'"{name}" lecture',
    ]

    if person.get("slug") == "elon-musk":
        query_templates.extend(
            [
                '"Elon Musk" full interview',
                '"Elon Musk" Joe Rogan',
                '"Elon Musk" Lex Fridman',
                '"Elon Musk" Tesla AI Day',
                '"Elon Musk" Autonomy Day',
                '"Elon Musk" SpaceX update',
                '"Elon Musk" Starship presentation',
                '"Elon Musk" Neuralink presentation',
            ]
        )

    if role:
        query_templates.append(f'"{name}" {role.split(",")[0]} interview')

    for topic in topics[:4]:
        query_templates.append(f'"{name}" {topic}')

    for source in person.get("sources", []):
        if source.get("type") == "youtube" and source.get("url"):
            query_templates.append(f'"{name}" site:youtube.com {source["url"].rstrip("/").split("/")[-1]}')

    deduped: list[str] = []
    seen = set()
    for query in query_templates:
        normalized = " ".join(query.split())
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(normalized)
        if len(deduped) >= limit:
            break
    return deduped


def candidate_score(person: dict[str, Any], query: str, title: str = "") -> tuple[float, str]:
    """Assign a simple starting score and priority for candidate videos."""
    tier_weight = float(person.get("weight", 2.0))
    text = f"{query} {title}".lower()
    score = tier_weight * 2.0

    if "interview" in text:
        score += 1.5
    if "keynote" in text or "lecture" in text:
        score += 1.0
    if "podcast" in text:
        score += 0.7
    if person.get("status") == "approved":
        score += 0.8
    if person.get("status") == "maybe":
        score -= 1.0

    return round(score, 2), priority_from_score(score)


def priority_from_score(score: float) -> str:
    if score >= 8:
        return "P0"
    if score >= 6:
        return "P1"
    if score >= 4:
        return "P2"
    return "P3"


def source_quality_adjustment(record: dict[str, Any], person: dict[str, Any]) -> float:
    """Prefer first-party/direct long-form and down-rank recap/clickbait videos."""
    title = normalize_match_text(str(record.get("title", "")))
    channel = normalize_match_text(str(record.get("channel_name", "")))
    name = normalize_match_text(str(person.get("name", "")))
    adjustment = 0.0

    if any(term in title for term in DIRECT_SOURCE_TERMS):
        adjustment += 2.0
    if name and name in channel:
        adjustment += 2.0
    if any(term in title for term in LOW_SIGNAL_TERMS):
        adjustment -= 3.0
    if channel in LOW_SIGNAL_CHANNELS:
        adjustment -= 2.0
    if name and name not in title and name not in channel:
        adjustment -= 1.5
    return adjustment


class PeopleVideoQueue:
    """SQLite queue for person-anchored YouTube candidates and transcripts."""

    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)

    def connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def connection(self):
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init(self) -> None:
        with self.connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS people_video_queue (
                    video_id TEXT NOT NULL,
                    person_slug TEXT NOT NULL,
                    person_name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    channel_name TEXT DEFAULT '',
                    channel_id TEXT DEFAULT '',
                    published_at TEXT DEFAULT '',
                    duration_seconds INTEGER,
                    score REAL DEFAULT 0,
                    priority TEXT DEFAULT 'P3',
                    source TEXT DEFAULT 'manual',
                    query TEXT DEFAULT '',
                    transcript_path TEXT DEFAULT '',
                    status TEXT DEFAULT 'candidate',
                    notes TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (video_id, person_slug)
                );
                CREATE INDEX IF NOT EXISTS idx_people_video_status
                    ON people_video_queue(status, priority, score DESC);
                CREATE INDEX IF NOT EXISTS idx_people_video_person
                    ON people_video_queue(person_slug, score DESC);
                CREATE INDEX IF NOT EXISTS idx_people_video_transcript
                    ON people_video_queue(transcript_path);
                """
            )

    def upsert_candidate(self, candidate: VideoCandidate) -> None:
        self.init()
        now = utc_now()
        payload = asdict(candidate)
        with self.connection() as conn:
            conn.execute(
                """
                INSERT INTO people_video_queue (
                    video_id, person_slug, person_name, title, url, channel_name,
                    channel_id, published_at, duration_seconds, score, priority,
                    source, query, transcript_path, status, notes, created_at, updated_at
                ) VALUES (
                    :video_id, :person_slug, :person_name, :title, :url, :channel_name,
                    :channel_id, :published_at, :duration_seconds, :score, :priority,
                    :source, :query, :transcript_path, :status, :notes, :created_at, :updated_at
                )
                ON CONFLICT(video_id, person_slug) DO UPDATE SET
                    title=excluded.title,
                    url=excluded.url,
                    channel_name=excluded.channel_name,
                    channel_id=excluded.channel_id,
                    published_at=excluded.published_at,
                    duration_seconds=excluded.duration_seconds,
                    score=excluded.score,
                    priority=excluded.priority,
                    source=excluded.source,
                    query=excluded.query,
                    transcript_path=coalesce(nullif(excluded.transcript_path, ''), people_video_queue.transcript_path),
                    status=CASE
                        WHEN excluded.transcript_path != '' THEN excluded.status
                        ELSE people_video_queue.status
                    END,
                    notes=excluded.notes,
                    updated_at=excluded.updated_at
                """,
                {**payload, "created_at": now, "updated_at": now},
            )

    def add_manual_video(
        self,
        person: dict[str, Any],
        video_url: str,
        title: str = "",
        channel_name: str = "",
        source: str = "manual",
        query: str = "",
    ) -> VideoCandidate:
        video_id = extract_video_id(video_url)
        if not video_id:
            raise ValueError(f"Could not extract a YouTube video ID from: {video_url}")

        score, priority = candidate_score(person, query or video_url, title)
        candidate = VideoCandidate(
            video_id=video_id,
            person_slug=person["slug"],
            person_name=person["name"],
            title=title or video_id,
            url=build_youtube_url(video_id),
            channel_name=channel_name,
            score=score,
            priority=priority,
            source=source,
            query=query,
        )
        self.upsert_candidate(candidate)
        return candidate

    def mark_transcript_ready(self, video_id: str, person_slug: str, transcript_path: Path) -> None:
        self.init()
        with self.connection() as conn:
            conn.execute(
                """
                UPDATE people_video_queue
                SET transcript_path = ?, status = 'transcript_ready', updated_at = ?
                WHERE video_id = ? AND person_slug = ?
                """,
                (str(transcript_path), utc_now(), video_id, person_slug),
            )

    def stats(self) -> dict[str, int]:
        self.init()
        with self.connection() as conn:
            rows = conn.execute(
                "SELECT status, count(*) AS count FROM people_video_queue GROUP BY status"
            ).fetchall()
            total = conn.execute("SELECT count(*) AS count FROM people_video_queue").fetchone()["count"]
        stats = {row["status"]: int(row["count"]) for row in rows}
        stats["total"] = int(total)
        return stats

    def list_candidates_for_person(self, person_slug: str, limit: int = 10) -> list[dict[str, Any]]:
        self.init()
        with self.connection() as conn:
            rows = conn.execute(
                """
                SELECT * FROM people_video_queue
                WHERE person_slug = ?
                ORDER BY
                    CASE priority WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 WHEN 'P2' THEN 2 ELSE 3 END,
                    score DESC,
                    updated_at DESC
                LIMIT ?
                """,
                (person_slug, limit),
            ).fetchall()
        return [dict(row) for row in rows]

    def counts_for_person(self, person_slug: str) -> dict[str, int]:
        self.init()
        with self.connection() as conn:
            rows = conn.execute(
                """
                SELECT status, count(*) AS count
                FROM people_video_queue
                WHERE person_slug = ?
                GROUP BY status
                """,
                (person_slug,),
            ).fetchall()
        counts = {row["status"]: int(row["count"]) for row in rows}
        counts["total"] = sum(counts.values())
        counts["transcript_ready"] = counts.get("transcript_ready", 0)
        return counts

    def collection_summary(self, people: list[dict[str, Any]], candidate_limit: int = 5) -> dict[str, Any]:
        self.init()
        records = []
        totals = {
            "people": len(people),
            "with_candidates": 0,
            "with_transcripts": 0,
            "candidate_videos": 0,
            "transcript_ready_videos": 0,
        }

        for person in people:
            candidates = self.list_candidates_for_person(person["slug"], limit=candidate_limit)
            counts = self.counts_for_person(person["slug"])
            candidate_count = counts["total"]
            transcript_count = counts["transcript_ready"]

            if candidate_count:
                totals["with_candidates"] += 1
                totals["candidate_videos"] += candidate_count
            if transcript_count:
                totals["with_transcripts"] += 1
                totals["transcript_ready_videos"] += transcript_count

            records.append(
                {
                    "slug": person["slug"],
                    "name": person["name"],
                    "status": person.get("status", "candidate"),
                    "tier": person.get("tier", "B"),
                    "line": person.get("line", ""),
                    "collection_mode": person.get("collection_mode", ""),
                    "candidate_count": candidate_count,
                    "transcript_ready_count": transcript_count,
                    "shown_candidate_count": len(candidates),
                    "next_action": next_collection_action(candidate_count, transcript_count),
                    "top_queries": build_person_queries(person, limit=3),
                    "youtube_search_urls": [
                        f"https://www.youtube.com/results?search_query={quote_plus(query)}"
                        for query in build_person_queries(person, limit=3)
                    ],
                    "candidates": [
                        {
                            "video_id": candidate["video_id"],
                            "title": candidate["title"],
                            "url": candidate["url"],
                            "channel_name": candidate["channel_name"],
                            "score": candidate["score"],
                            "priority": candidate["priority"],
                            "status": candidate["status"],
                            "transcript_path": candidate["transcript_path"],
                        }
                        for candidate in candidates
                    ],
                }
            )

        return {"generated_at": utc_now(), "totals": totals, "people": records}

    def list_ready(self, limit: int = 50, min_tier: str = "B") -> list[dict[str, Any]]:
        self.init()
        max_priority = {"A": 1, "B": 2, "C": 3}[min_tier]
        with self.connection() as conn:
            rows = conn.execute(
                """
                SELECT * FROM people_video_queue
                WHERE status = 'transcript_ready'
                  AND transcript_path != ''
                ORDER BY
                    CASE priority WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 WHEN 'P2' THEN 2 ELSE 3 END,
                    score DESC,
                    updated_at DESC
                LIMIT ?
                """,
                (limit * 3,),
            ).fetchall()

        videos: list[dict[str, Any]] = []
        for row in rows:
            priority = row["priority"] or "P3"
            if PRIORITY_ORDER.get(priority, 3) > max_priority:
                continue
            videos.append(
                {
                    "video_id": row["video_id"],
                    "person_slug": row["person_slug"],
                    "person_name": row["person_name"],
                    "channel_slug": row["person_slug"],
                    "channel_name": row["channel_name"] or row["person_name"],
                    "title": row["title"],
                    "upload_date": row["published_at"],
                    "duration": row["duration_seconds"],
                    "score": row["score"],
                    "priority": priority,
                    "tier": TIER_FROM_PRIORITY.get(priority, "C"),
                    "transcript_path": row["transcript_path"],
                    "url": row["url"],
                }
            )
            if len(videos) >= limit:
                break
        return videos

    def export_prioritized(self, output_path: Path, limit: int = 50, min_tier: str = "B") -> list[dict[str, Any]]:
        videos = self.list_ready(limit=limit, min_tier=min_tier)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(
                {"generated_at": utc_now(), "count": len(videos), "videos": videos},
                indent=2,
            )
            + "\n"
        )
        return videos


def normalize_transcript_text(raw_text: str) -> str:
    text = raw_text.strip()
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def next_collection_action(candidate_count: int, transcript_count: int) -> str:
    if transcript_count:
        return "ready_for_extraction"
    if candidate_count:
        return "import_transcript"
    return "discover_candidates"


def safe_filename_part(value: str, max_len: int = 80) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    return value[:max_len].strip("-") or "untitled"


def transcript_export_filename(candidate: dict[str, Any]) -> str:
    title = safe_filename_part(candidate.get("title", candidate["video_id"]))
    return f"{candidate['person_slug']}__{candidate['video_id']}__{title}.txt"


def write_transcript_backlog(
    queue: PeopleVideoQueue,
    people: list[dict[str, Any]],
    output_path: Path,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Write a prioritized list of candidate videos that still need transcripts."""
    rows: list[dict[str, Any]] = []
    for person in people:
        for candidate in queue.list_candidates_for_person(person["slug"], limit=20):
            if candidate.get("status") == "transcript_ready":
                continue
            rows.append(candidate)

    rows.sort(
        key=lambda candidate: (
            PRIORITY_ORDER.get(candidate.get("priority", "P3"), 3),
            -float(candidate.get("score") or 0),
            candidate.get("person_name", ""),
        )
    )
    rows = rows[:limit]

    lines = [
        "# YouTube Transcript Collection Backlog",
        "",
        "Drop Chrome-plugin transcript exports into:",
        "",
        "`pipelines/youtube/inbox/plugin_exports/`",
        "",
        "Use the suggested filename exactly so the refresh runner can auto-import it.",
        "",
    ]

    for candidate in rows:
        filename = transcript_export_filename(candidate)
        lines.extend(
            [
                f"## {candidate['person_name']} - {candidate['title']}",
                "",
                f"- URL: {candidate['url']}",
                f"- Channel: `{candidate.get('channel_name', '')}`",
                f"- Priority: `{candidate.get('priority', '')}` | Score: `{candidate.get('score', '')}`",
                f"- Save transcript as: `pipelines/youtube/inbox/plugin_exports/{filename}`",
                "",
            ]
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return rows


def write_collection_report(summary: dict[str, Any], json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    totals = summary["totals"]
    lines = [
        "# People YouTube Collection Status",
        "",
        f"Generated: `{summary['generated_at']}`",
        "",
        "## Totals",
        "",
        f"- People tracked: `{totals['people']}`",
        f"- People with candidate videos: `{totals['with_candidates']}`",
        f"- People with transcript-ready videos: `{totals['with_transcripts']}`",
        f"- Candidate videos queued: `{totals['candidate_videos']}`",
        f"- Transcript-ready videos queued: `{totals['transcript_ready_videos']}`",
        "",
        "## People",
        "",
    ]

    for person in summary["people"]:
        lines.append(
            f"### {person['name']} (`{person['slug']}`) - {person['next_action']}"
        )
        lines.append(
            f"Status: `{person['status']}` | Tier: `{person['tier']}` | Line: `{person['line']}`"
        )
        lines.append(
            f"Candidates: `{person['candidate_count']}` | Transcript ready: `{person['transcript_ready_count']}`"
            f" | Showing: `{person['shown_candidate_count']}`"
        )
        if person["candidates"]:
            lines.append("")
            for candidate in person["candidates"][:5]:
                transcript_marker = " transcript" if candidate["status"] == "transcript_ready" else ""
                lines.append(
                    f"- [{candidate['title']}]({candidate['url']})"
                    f" - `{candidate['channel_name']}` `{candidate['priority']}` `{candidate['score']}`{transcript_marker}"
                )
        else:
            lines.append("")
            for query, url in zip(person["top_queries"], person["youtube_search_urls"], strict=False):
                lines.append(f"- Search: [{query}]({url})")
        lines.append("")

    markdown_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def import_plugin_transcript(
    transcript_file: Path,
    video_url: str,
    person: dict[str, Any],
    title: str = "",
    channel_name: str = "",
    output_dir: Path = DEFAULT_TRANSCRIPTS_DIR,
    queue: PeopleVideoQueue | None = None,
) -> Path:
    """Normalize a Chrome-plugin transcript export into extraction-ready YAML."""
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError(f"Could not extract a YouTube video ID from: {video_url}")

    transcript_file = Path(transcript_file)
    raw_text = transcript_file.read_text(encoding="utf-8")
    full_text = normalize_transcript_text(raw_text)
    if not full_text:
        raise ValueError(f"Transcript file is empty: {transcript_file}")

    person_dir = Path(output_dir) / person["slug"]
    person_dir.mkdir(parents=True, exist_ok=True)
    output_path = person_dir / f"{video_id}.yaml"

    data = {
        "video": {
            "video_id": video_id,
            "title": title or video_id,
            "url": build_youtube_url(video_id),
            "channel_name": channel_name,
            "person_slugs": [person["slug"]],
            "person_names": [person["name"]],
        },
        "transcript": {
            "source": "chrome_plugin_export",
            "imported_at": utc_now(),
            "source_file": str(transcript_file),
            "full_text": full_text,
        },
        "provenance": {
            "collection_policy": "manual_or_permissioned_transcript_import",
            "notes": "Imported from a user-provided transcript export; no video download performed.",
        },
    }
    output_path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8")

    active_queue = queue or PeopleVideoQueue()
    active_queue.init()
    candidate = active_queue.add_manual_video(
        person=person,
        video_url=video_url,
        title=title or video_id,
        channel_name=channel_name,
        source="chrome_plugin_export",
    )
    active_queue.mark_transcript_ready(candidate.video_id, person["slug"], output_path)
    return output_path


def parse_plugin_export_filename(path: Path, people_by_slug: dict[str, dict[str, Any]]) -> dict[str, str] | None:
    """Parse `{person_slug}__{video_id}__optional-title.txt` transcript exports."""
    path = Path(path)
    if path.suffix.lower() not in {".txt", ".md"}:
        return None

    parts = path.stem.split("__")
    if len(parts) < 2:
        return None

    person_slug = parts[0].strip()
    video_id = extract_video_id(parts[1].strip())
    if person_slug not in people_by_slug or not video_id:
        return None

    title = video_id
    if len(parts) >= 3 and parts[2].strip():
        title = " ".join(parts[2].replace("-", " ").replace("_", " ").split())

    return {
        "person_slug": person_slug,
        "video_id": video_id,
        "title": title,
    }


def import_plugin_export_files(
    files: list[Path],
    people_by_slug: dict[str, dict[str, Any]],
    output_dir: Path = DEFAULT_TRANSCRIPTS_DIR,
    queue: PeopleVideoQueue | None = None,
) -> dict[str, Any]:
    """Import transcript exports from the plugin inbox filename convention."""
    active_queue = queue or PeopleVideoQueue()
    summary: dict[str, Any] = {
        "files_seen": len(files),
        "files_processed": 0,
        "files_skipped": 0,
        "transcripts_imported": 0,
        "per_person": {},
        "skipped": [],
    }

    for file_path in files:
        parsed = parse_plugin_export_filename(Path(file_path), people_by_slug)
        if not parsed:
            summary["files_skipped"] += 1
            summary["skipped"].append(str(file_path))
            continue

        person = people_by_slug[parsed["person_slug"]]
        import_plugin_transcript(
            transcript_file=Path(file_path),
            video_url=build_youtube_url(parsed["video_id"]),
            person=person,
            title=parsed["title"],
            output_dir=output_dir,
            queue=active_queue,
        )
        summary["files_processed"] += 1
        summary["transcripts_imported"] += 1
        summary["per_person"][person["slug"]] = summary["per_person"].get(person["slug"], 0) + 1

    return summary


def iter_search_result_entries(payload: Any) -> list[dict[str, Any]]:
    """Return a flat list of entries from common search JSON shapes."""
    if isinstance(payload, list):
        return [entry for entry in payload if isinstance(entry, dict)]
    if not isinstance(payload, dict):
        return []

    data = payload.get("data", payload)
    if isinstance(data, list):
        return [entry for entry in data if isinstance(entry, dict)]
    if isinstance(data, dict):
        entries: list[dict[str, Any]] = []
        for key in ["web", "results", "items", "organic"]:
            value = data.get(key)
            if isinstance(value, list):
                entries.extend(entry for entry in value if isinstance(entry, dict))
        if entries:
            return entries
    return []


def import_search_results(
    payload: Any,
    person: dict[str, Any],
    queue: PeopleVideoQueue | None = None,
    source: str = "search_results",
) -> list[VideoCandidate]:
    """Queue YouTube video candidates from Firecrawl/Perplexity/search result JSON."""
    active_queue = queue or PeopleVideoQueue()
    active_queue.init()

    imported: list[VideoCandidate] = []
    seen_video_ids = set()
    for entry in iter_search_result_entries(payload):
        url = str(entry.get("url") or entry.get("link") or "")
        title = str(entry.get("title") or entry.get("name") or "")
        channel_name = str(entry.get("channel") or entry.get("channel_name") or entry.get("source") or "")
        text_parts = [
            url,
            title,
            str(entry.get("description") or ""),
            str(entry.get("snippet") or ""),
            str(entry.get("markdown") or ""),
            str(entry.get("content") or ""),
        ]
        candidate_urls = []
        if extract_video_id(url):
            candidate_urls.append(url)
        for found_url in extract_youtube_urls_from_text("\n".join(text_parts)):
            if found_url not in candidate_urls:
                candidate_urls.append(found_url)

        for candidate_url in candidate_urls:
            video_id = extract_video_id(candidate_url)
            if not video_id or video_id in seen_video_ids:
                continue
            seen_video_ids.add(video_id)
            candidate = active_queue.add_manual_video(
                person=person,
                video_url=candidate_url,
                title=title or video_id,
                channel_name=channel_name,
                source=source,
                query=str(entry.get("query") or ""),
            )
            imported.append(candidate)
    return imported


def infer_person_slug_from_search_file(path: Path, people_by_slug: dict[str, dict[str, Any]]) -> str | None:
    """Infer a person slug from a search result filename prefix."""
    stem = Path(path).stem
    matches = [slug for slug in people_by_slug if stem == slug or stem.startswith(f"{slug}-")]
    if not matches:
        return None
    return max(matches, key=len)


def import_search_result_files(
    files: list[Path],
    people_by_slug: dict[str, dict[str, Any]],
    queue: PeopleVideoQueue | None = None,
    source: str = "search_results_batch",
) -> dict[str, Any]:
    """Import all recognizable search result JSON files into the queue."""
    active_queue = queue or PeopleVideoQueue()
    summary: dict[str, Any] = {
        "files_seen": len(files),
        "files_processed": 0,
        "files_skipped": 0,
        "candidates_imported": 0,
        "per_person": {},
        "skipped": [],
    }

    for file_path in files:
        person_slug = infer_person_slug_from_search_file(Path(file_path), people_by_slug)
        if not person_slug:
            summary["files_skipped"] += 1
            summary["skipped"].append(str(file_path))
            continue
        payload = json.loads(Path(file_path).read_text(encoding="utf-8"))
        imported = import_search_results(
            payload,
            people_by_slug[person_slug],
            queue=active_queue,
            source=source,
        )
        summary["files_processed"] += 1
        summary["candidates_imported"] += len(imported)
        summary["per_person"][person_slug] = summary["per_person"].get(person_slug, 0) + len(imported)
    return summary


def resolve_existing_transcript_path(record: dict[str, Any], transcripts_dir: Path = LEGACY_TRANSCRIPTS_DIR) -> str:
    transcript_path = record.get("transcript_path") or ""
    if transcript_path and Path(transcript_path).exists():
        return transcript_path

    video_id = record.get("video_id", "")
    if video_id:
        for suffix in [".txt", ".md", ".yaml", ".yml"]:
            candidate = Path(transcripts_dir) / f"{video_id}{suffix}"
            if candidate.exists():
                return str(candidate)
    return ""


def candidate_from_existing_record(
    record: dict[str, Any],
    person: dict[str, Any],
    transcripts_dir: Path = LEGACY_TRANSCRIPTS_DIR,
) -> VideoCandidate:
    transcript_path = resolve_existing_transcript_path(record, transcripts_dir=transcripts_dir)
    score, priority = candidate_score(person, record.get("title", ""), record.get("title", ""))
    score = max(0.0, round(score + source_quality_adjustment(record, person), 2))
    priority = priority_from_score(score)
    status = "transcript_ready" if transcript_path else "candidate"
    return VideoCandidate(
        video_id=record["video_id"],
        person_slug=person["slug"],
        person_name=person["name"],
        title=record.get("title") or record["video_id"],
        url=build_youtube_url(record["video_id"]),
        channel_name=record.get("channel_name") or "",
        published_at=record.get("upload_date") or "",
        duration_seconds=record.get("duration"),
        score=score,
        priority=priority,
        source="existing_youtube_research_queue",
        query="local_metadata_match",
        transcript_path=transcript_path,
        status=status,
        notes=f"legacy_status={record.get('status', '')}; legacy_score={record.get('score', '')}",
    )


def seed_from_existing_queue(
    source_db: Path,
    queue: PeopleVideoQueue,
    people: list[dict[str, Any]],
    limit_per_person: int = 10,
    transcripts_dir: Path = LEGACY_TRANSCRIPTS_DIR,
    replace_existing_source: bool = True,
) -> dict[str, Any]:
    """Seed the people queue from an existing local YouTube research database."""
    source_db = Path(source_db)
    if not source_db.exists():
        raise FileNotFoundError(source_db)

    queue.init()
    if replace_existing_source:
        with queue.connection() as conn:
            conn.execute("DELETE FROM people_video_queue WHERE source = 'existing_youtube_research_queue'")

    source_conn = sqlite3.connect(source_db)
    source_conn.row_factory = sqlite3.Row
    try:
        rows = source_conn.execute(
            """
            SELECT video_id, channel_slug, channel_name, title, upload_date,
                   duration, score, priority, status, transcript_path
            FROM video_queue
            WHERE video_id IS NOT NULL
            """
        ).fetchall()
    finally:
        source_conn.close()

    normalized_rows = []
    for row in rows:
        record = dict(row)
        haystack = normalize_match_text(
            " ".join(
                [
                    str(record.get("title", "")),
                    str(record.get("channel_name", "")),
                    str(record.get("channel_slug", "")),
                ]
            )
        )
        normalized_rows.append((record, haystack))

    seeded = 0
    transcript_ready = 0
    per_person: dict[str, int] = {}

    for person in people:
        terms = person_match_terms(person)
        matches = []
        for record, haystack in normalized_rows:
            if any(term in haystack for term in terms):
                matches.append(candidate_from_existing_record(record, person, transcripts_dir=transcripts_dir))

        matches.sort(key=lambda item: (item.status != "transcript_ready", -item.score, item.title.lower()))
        for candidate in matches[:limit_per_person]:
            queue.upsert_candidate(candidate)
            seeded += 1
            if candidate.status == "transcript_ready":
                transcript_ready += 1
            per_person[person["slug"]] = per_person.get(person["slug"], 0) + 1

    return {
        "source_db": str(source_db),
        "people_scanned": len(people),
        "source_rows": len(rows),
        "seeded": seeded,
        "transcript_ready": transcript_ready,
        "matched_people": len(per_person),
        "per_person": per_person,
    }


def write_query_plan(people: list[dict[str, Any]], output_path: Path, limit_per_person: int = 8) -> dict[str, Any]:
    """Write search queries for people when no official YouTube API key is available."""
    ensure_directories()
    records = []
    for person in people:
        queries = build_person_queries(person, limit=limit_per_person)
        records.append(
            {
                "slug": person["slug"],
                "name": person["name"],
                "status": person.get("status", "candidate"),
                "tier": person.get("tier", "B"),
                "queries": queries,
                "youtube_search_urls": [
                    f"https://www.youtube.com/results?search_query={quote_plus(query)}"
                    for query in queries
                ],
            }
        )

    payload = {
        "generated_at": utc_now(),
        "people_count": len(records),
        "collection_policy": "Use official YouTube APIs for metadata when configured; import transcripts manually or with permission.",
        "people": records,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload
