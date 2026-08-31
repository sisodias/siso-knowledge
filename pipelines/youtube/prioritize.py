#!/usr/bin/env python3
"""
Prioritize videos for extraction based on relevance score and recency.

This generates a prioritized list of videos (Tier A/B) from the extraction queue.

Usage:
    python3 pipelines/youtube/prioritize.py
    python3 pipelines/youtube/prioritize.py --min-tier B
    python3 pipelines/youtube/prioritize.py --output /tmp/prioritized.json
"""
import argparse
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
DB_PATH = Path("/Users/youtube-pipeline/youtube-pipeline/database/queue.db")
EXTRACT_DIR = Path("/tmp/youtube-ai-research/extracted/by_date")


def get_prioritized_videos(min_tier: str = "B", limit: int = 50) -> list[dict]:
    """Get prioritized videos from the database."""

    # Check if DB exists, if not use extracted files as source
    if not DB_PATH.exists():
        return get_prioritized_from_extracted(min_tier, limit)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get videos with transcripts, ordered by priority and score
    cursor.execute("""
        SELECT video_id, channel_slug, channel_name, title, upload_date,
               duration, score, priority, transcript_path
        FROM video_queue
        WHERE status = 'completed'
          AND transcript_path IS NOT NULL
          AND transcript_path != ''
        ORDER BY
            CASE priority
                WHEN 'P0' THEN 1
                WHEN 'P1' THEN 2
                WHEN 'P2' THEN 3
                WHEN 'P3' THEN 4
                ELSE 5
            END,
            score DESC
        LIMIT ?
    """, (limit * 2,))  # Get more to filter by tier

    videos = cursor.fetchall()
    conn.close()

    result = []
    tier_order = {"A": 1, "B": 2, "C": 3}

    # Filter already extracted
    extracted_ids = set()
    if EXTRACT_DIR.exists():
        for f in EXTRACT_DIR.rglob("*.md"):
            extracted_ids.add(f.stem)

    tier_counts = {"A": 0, "B": 0, "C": 0}
    min_tier_num = tier_order.get(min_tier, 2)

    for v in videos:
        video_id = v["video_id"]
        if video_id in extracted_ids:
            continue

        # Assign tier based on priority and score
        priority = v["priority"] or "P3"
        score = v["score"] or 0

        if priority in ["P0", "P1"] or score >= 8:
            tier = "A"
        elif priority == "P2" or score >= 5:
            tier = "B"
        else:
            tier = "C"

        if tier_order.get(tier, 3) > min_tier_num:
            continue

        if tier_counts[tier] >= limit:
            continue

        tier_counts[tier] += 1
        result.append({
            "video_id": video_id,
            "channel_slug": v["channel_slug"],
            "channel_name": v["channel_name"],
            "title": v["title"],
            "upload_date": v["upload_date"],
            "duration": v["duration"],
            "score": score,
            "priority": priority,
            "tier": tier,
            "transcript_path": v["transcript_path"],
        })

    return result[:limit]


def get_prioritized_from_extracted(min_tier: str = "B", limit: int = 50) -> list[dict]:
    """Fallback: get videos from extracted folder with mock priority."""
    if not EXTRACT_DIR.exists():
        print(f"WARNING: No extraction dir found at {EXTRACT_DIR}")
        return []

    # Get videos NOT yet extracted - look at sources
    sources_dir = Path("/tmp/youtube-ai-research/sources")
    if not sources_dir.exists():
        return []

    videos = []
    for yaml_file in sources_dir.rglob("*.yaml"):
        try:
            import yaml
            data = yaml.safe_load(yaml_file.read_text())
            if not data:
                continue

            video = data.get("video", {})
            video_id = video.get("video_id", yaml_file.stem)

            # Check if already extracted
            extracted_path = EXTRACT_DIR / f"{video_id}.md"
            if extracted_path.exists():
                continue

            title = video.get("title", "Unknown")
            creator = video.get("creator", {}).get("name", "Unknown")
            score = video.get("score", 5)

            # Assign tier
            if score >= 8:
                tier = "A"
            elif score >= 5:
                tier = "B"
            else:
                tier = "C"

            if tier in ["A", "B"] or min_tier == "C":
                videos.append({
                    "video_id": video_id,
                    "channel_slug": video.get("channel_slug", "unknown"),
                    "channel_name": creator,
                    "title": title,
                    "upload_date": video.get("upload_date"),
                    "duration": video.get("duration"),
                    "score": score,
                    "priority": "P2",
                    "tier": tier,
                    "transcript_path": str(yaml_file),
                })
        except Exception:
            continue

    return videos[:limit]


def save_prioritized(videos: list[dict], output_path: Path):
    """Save prioritized list to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "count": len(videos),
            "videos": videos
        }, f, indent=2)
    print(f"Saved {len(videos)} videos to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Prioritize videos for extraction")
    parser.add_argument("--min-tier", choices=["A", "B", "C"], default="B",
                       help="Minimum tier to include (default: B)")
    parser.add_argument("--limit", type=int, default=50,
                       help="Max videos to return (default: 50)")
    parser.add_argument("--output", type=str, default="/tmp/youtube-prioritized.json",
                       help="Output file path")
    args = parser.parse_args()

    print(f"=== YouTube Video Prioritizer ===")
    print(f"Min tier: {args.min_tier}, Limit: {args.limit}")

    videos = get_prioritized_videos(args.min_tier, args.limit)

    tier_counts = {"A": 0, "B": 0, "C": 0}
    for v in videos:
        tier_counts[v.get("tier", "C")] += 1

    print(f"Found {len(videos)} videos: {tier_counts['A']} A, {tier_counts['B']} B, {tier_counts['C']} C")

    # Print top 5
    print("\nTop videos:")
    for v in videos[:5]:
        print(f"  [{v['tier']}] {v['title'][:60]}... (score: {v.get('score', 0)})")

    save_prioritized(videos, Path(args.output))


if __name__ == "__main__":
    main()
