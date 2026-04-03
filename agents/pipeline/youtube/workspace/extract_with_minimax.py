#!/usr/bin/env python3
"""
extract_with_minimax.py - Extract insights from YouTube video transcripts using Minimax API

Usage:
    python scripts/extract_with_minimax.py --limit 10
    python scripts/extract_with_minimax.py --limit 5 --dry-run
    python scripts/extract_with_minimax.py --db database/queue.db
"""

import argparse
import os
import sys
import json
import yaml
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Try to import anthropic - install if needed
try:
    import anthropic
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "anthropic"])
    import anthropic


# Configuration
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY")
MINIMAX_BASE_URL = "https://api.minimax.io/anthropic"
DEFAULT_MODEL = "MiniMax-M2.5-highspeed"

# Extraction prompt template
EXTRACTION_PROMPT = """You are an AI expert analyzing YouTube videos about AI, LLMs, coding tools, and software development.

Analyze the following video transcript and extract:

1. **Video Title**: {title}
2. **Creator**: {creator}
3. **Summary** (2-3 sentences): What is this video about?
4. **Key Insights** (3-5 bullet points): The most important takeaways
5. **Tools & Technologies**: List all tools, frameworks, libraries mentioned
6. **Techniques**: Specific methods, patterns, or approaches explained
7. **Code Examples**: Any code snippets or tutorials discussed
8. **Resources**: Links, docs, or references mentioned
9. **Difficulty**: Beginner / Intermediate / Advanced
10. **Relevance Score** (1-10): How relevant is this to AI engineering?

Provide your response in markdown format.

Transcript:
{transcript}
"""


def get_minimax_client():
    """Create Minimax API client using Anthropic SDK."""
    if not MINIMAX_API_KEY:
        raise ValueError("MINIMAX_API_KEY environment variable not set")

    client = anthropic.Anthropic(
        api_key=MINIMAX_API_KEY,
        base_url=MINIMAX_BASE_URL
    )
    return client


def load_video_metadata(video_path: Path) -> dict:
    """Load video metadata from YAML file."""
    with open(video_path, 'r') as f:
        return yaml.safe_load(f)


def load_transcript_from_yaml(video_path: Path) -> str:
    """Load transcript from the video YAML file itself."""
    try:
        with open(video_path, 'r') as f:
            data = yaml.safe_load(f)

        # Try different structures
        if 'transcript' in data:
            if isinstance(data['transcript'], dict) and 'full_text' in data['transcript']:
                return data['transcript']['full_text']
            elif isinstance(data['transcript'], str):
                return data['transcript']

        # Try nested video + transcript
        if 'video' in data and isinstance(data['video'], dict):
            if 'transcript' in data['video']:
                if isinstance(data['video']['transcript'], dict) and 'full_text' in data['video']['transcript']:
                    return data['video']['transcript']['full_text']

        return None
    except Exception as e:
        print(f"    Warning: Could not parse YAML: {e}")
        return None


def get_videos_from_transcripts_folder(transcripts_dir: Path, limit: int = 10) -> list:
    """Get videos from transcripts folder that aren't already extracted."""
    if not transcripts_dir.exists():
        return []

    # Get list of already extracted
    repo_root = transcripts_dir.parent.parent
    extracted_dir = repo_root / "extracted" / "by_date"
    extracted_ids = set()
    if extracted_dir.exists():
        for f in extracted_dir.rglob("*.md"):
            extracted_ids.add(f.stem)

    videos = []
    for transcript_file in sorted(transcripts_dir.glob("*.txt")):
        video_id = transcript_file.stem
        if video_id not in extracted_ids:
            videos.append({
                'video_id': video_id,
                'channel_slug': 'unknown',
                'channel_name': 'Unknown',
                'title': f'Video {video_id}',
                'upload_date': None,
                'duration': None,
                'score': 0,
                'priority': 'P3',
                'transcript_path': str(transcript_file)
            })

    return videos[:limit]


def get_videos_from_db(db_path: Path, limit: int = 10) -> list:
    """Get videos from the SQLite database that have transcripts."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get videos that have transcripts (status = 'completed')
    cursor.execute("""
        SELECT video_id, channel_slug, channel_name, title, upload_date, duration, score, priority, transcript_path
        FROM video_queue
        WHERE status = 'completed' AND transcript_path IS NOT NULL AND transcript_path != ''
        ORDER BY priority, score DESC
        LIMIT ?
    """, (limit,))

    videos = cursor.fetchall()
    conn.close()

    return [dict(v) for v in videos]


def extract_insights(client: anthropic.Anthropic, title: str, creator: str, transcript: str, model: str = DEFAULT_MODEL) -> str:
    """Extract insights from transcript using Minimax API."""

    # Truncate transcript if too long (API limit is 204k tokens, but let's be safe)
    max_chars = 150000
    if len(transcript) > max_chars:
        transcript = transcript[:max_chars] + "\n\n[Transcript truncated...]"

    prompt = EXTRACTION_PROMPT.format(
        title=title,
        creator=creator,
        transcript=transcript
    )

    response = client.messages.create(
        model=model,
        max_tokens=8192,
        temperature=0.7,
        system="You are an expert AI research analyst.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Handle both thinking and text blocks in response
    result = []
    for block in response.content:
        if hasattr(block, 'text'):
            result.append(block.text)
    return "\n".join(result)


def save_extraction(output_dir: Path, video_id: str, metadata: dict, insights: str) -> Path:
    """Save extracted insights to file."""
    date = datetime.now()
    output_path = output_dir / str(date.year) / f"{date.month:02d}-{date.strftime('%B')}" / f"{video_id}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Handle nested metadata structure
    title = metadata.get('video', {}).get('title', metadata.get('title', 'Unknown'))
    creator_data = metadata.get('creator', {})
    if isinstance(creator_data, dict):
        creator = creator_data.get('name', 'Unknown')
    else:
        creator = str(creator_data)

    content = f"""---
video_id: {video_id}
title: {title}
creator: {creator}
extracted_at: {datetime.now().isoformat()}
---

{insights}
"""

    with open(output_path, 'w') as f:
        f.write(content)

    return output_path


def move_to_completed(pending_dir: Path, completed_dir: Path, video_id: str):
    """Move processed video from pending to completed."""
    pending_dir.mkdir(parents=True, exist_ok=True)

    src = pending_dir / f"{video_id}.yaml"
    dst = completed_dir / f"{video_id}.yaml"

    if src.exists():
        shutil.move(str(src), str(dst))


def find_transcript(transcript_path: str, sources_dir: Path) -> Path | None:
    """Find transcript file using multiple path strategies."""
    # Find repo root (go up from sources_dir until we find content/ or repo root)
    repo_root = sources_dir
    while repo_root.name != 'youtube-ai-research' and repo_root.parent != repo_root:
        if (repo_root / 'content').exists():
            break
        repo_root = repo_root.parent

    video_id = Path(transcript_path).stem

    # Strategy 1: Direct path
    p = Path(transcript_path)
    if p.exists():
        return p

    # Strategy 2: Relative to repo root (the whole path minus leading slash)
    if transcript_path.startswith('/'):
        relative = transcript_path[1:]
        p = repo_root / relative
        if p.exists():
            return p

    # Strategy 3: Strip known prefixes
    for prefix in ['/Users/youtube-pipeline/youtube-pipeline/', '/Users/youtube-pipeline/']:
        if transcript_path.startswith(prefix):
            relative = transcript_path[len(prefix):]
            p = repo_root / relative
            if p.exists():
                return p

    # Strategy 4: Extract video ID and search in common locations
    for pattern in repo_root.glob(f"content/transcripts/**/{video_id}.*"):
        return pattern
    for pattern in repo_root.glob(f"data/sources/**/{video_id}.*"):
        return pattern
    for pattern in repo_root.glob(f"**/{video_id}.*"):
        if pattern.suffix in ['.md', '.txt', '.yaml']:
            return pattern

    # Strategy 5: Also check database/transcripts folder
    db_transcripts = repo_root / "database" / "transcripts"
    if db_transcripts.exists():
        for pattern in db_transcripts.glob(f"{video_id}.*"):
            return pattern
        # Also search by video ID in txt files
        for f in db_transcripts.glob("*.txt"):
            if video_id in f.stem:
                return f

    return None


def process_video_from_db(video_data: dict, args) -> dict:
    """Process a single video from database entry."""
    video_id = video_data['video_id']
    channel_slug = video_data['channel_slug']
    title = video_data['title']
    creator = video_data['channel_name'] or channel_slug
    transcript_path = video_data['transcript_path']

    try:
        print(f"  Processing: {title[:50]}...")

        # Find transcript using multiple strategies
        transcript_full_path = find_transcript(transcript_path, args.sources_dir)

        if not transcript_full_path:
            print(f"  ⚠ Transcript not found: {transcript_path}")
            return {"video_id": video_id, "status": "no_transcript"}

        # Load transcript
        with open(transcript_full_path, 'r') as f:
            transcript = f.read()

        if not transcript:
            print(f"  ⚠ Empty transcript for {video_id}")
            return {"video_id": video_id, "status": "no_transcript"}

        if args.dry_run:
            print(f"  ✓ Would extract (dry-run)")
            return {"video_id": video_id, "status": "dry_run"}

        # Extract insights
        client = get_minimax_client()
        insights = extract_insights(client, title, creator, transcript, args.model)

        # Save extraction
        metadata = {'title': title, 'creator': creator, 'video_id': video_id}
        output_path = save_extraction(args.output_dir, video_id, metadata, insights)

        print(f"  ✓ Saved to {output_path}")

        return {"video_id": video_id, "status": "success", "output": str(output_path)}

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return {"video_id": video_id, "status": "error", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Extract insights from YouTube transcripts using Minimax API")
    parser.add_argument("--limit", type=int, default=10, help="Number of videos to process")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed without calling API")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Minimax model to use")
    parser.add_argument("--db", type=str, default="database/queue.db", help="Path to SQLite database")
    parser.add_argument("--sources-dir", type=str, default="data/sources", help="Directory with source videos")
    parser.add_argument("--output-dir", type=str, default="extracted/by_date", help="Output directory for extractions")
    parser.add_argument("--workers", type=int, default=3, help="Parallel workers")

    args = parser.parse_args()

    # Convert string paths to Path objects
    args.sources_dir = Path(args.sources_dir)
    args.output_dir = Path(args.output_dir)
    args.db_path = Path(args.db)

    # First check transcripts folder for new ones
    transcripts_dir = args.sources_dir.parent / "database" / "transcripts"
    videos = get_videos_from_transcripts_folder(transcripts_dir, args.limit)

    # Also check database for additional videos
    if len(videos) < args.limit and args.db_path.exists():
        db_videos = get_videos_from_db(args.db_path, args.limit)
        video_ids = {v['video_id'] for v in videos}
        for v in db_videos:
            if v['video_id'] not in video_ids and len(videos) < args.limit:
                videos.append(v)

    if not videos:
        print(f"No videos found")
        sys.exit(1)

    video_files = videos
    print(f"\nFound {len(videos)} videos to process")

    print(f"Model: {args.model}")
    print(f"Dry run: {args.dry_run}\n")

    # Process videos
    results = []
    if video_files and isinstance(video_files[0], dict):
        # Database mode
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(process_video_from_db, v, args): v for v in video_files}
            for future in as_completed(futures):
                results.append(future.result())
    else:
        # YAML mode (legacy)
        from functools import partial
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(process_video, vf, args): vf for vf in video_files}
            for future in as_completed(futures):
                results.append(future.result())

    # Summary
    success = sum(1 for r in results if r["status"] == "success")
    errors = sum(1 for r in results if r["status"] == "error")
    skipped = sum(1 for r in results if r["status"] == "no_transcript")

    print(f"\n{'='*50}")
    print(f"Results: {success} success, {errors} errors, {skipped} no transcript")


if __name__ == "__main__":
    main()
