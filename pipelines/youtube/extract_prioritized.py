#!/usr/bin/env python3
"""
Extract insights from prioritized videos and save to library as pages.

For each video in the prioritized list (Tier A/B from prioritize.py output),
runs insight extraction and saves individual pages per video to the library.

Usage:
    python3 pipelines/youtube/extract_prioritized.py
    python3 pipelines/youtube/extract_prioritized.py --input /tmp/youtube-prioritized.json
    python3 pipelines/youtube/extract_prioritized.py --dry-run
    python3 pipelines/youtube/extract_prioritized.py --workers 3
"""
import argparse
import json
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add to path for imports
ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "queries"))
sys.path.insert(0, str(ROOT / "pipelines"))

# Try to import anthropic for MiniMax API
try:
    import anthropic
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "anthropic"])
    import anthropic

from add_book import add_page, get_next_page_id, get_shelf_path
from shared.topic_router import route_to_shelf, detect_tags, extract_tools

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

PRIORITIZED_FILE = Path("/tmp/youtube-prioritized.json")
EXTRACT_DIR = Path("/tmp/youtube-ai-research/extracted/by_date")
LIB_PAGES_DIR = ROOT / "sections" / "ai_research" / "bookcases" / "youtube" / "shelves" / "videos" / "pages"


def get_minimax_client():
    """Create Minimax API client."""
    if not MINIMAX_API_KEY:
        raise ValueError("MINIMAX_API_KEY environment variable not set")

    return anthropic.Anthropic(
        api_key=MINIMAX_API_KEY,
        base_url=MINIMAX_BASE_URL
    )


def load_prioritized_list(input_path: Path) -> list[dict]:
    """Load prioritized video list from JSON."""
    if not input_path.exists():
        print(f"ERROR: Prioritized list not found: {input_path}")
        print("Run: python3 pipelines/youtube/prioritize.py first")
        sys.exit(1)

    with open(input_path) as f:
        data = json.load(f)
    return data.get("videos", [])


def find_transcript(video: dict) -> Path | None:
    """Find transcript file for a video."""
    transcript_path = video.get("transcript_path", "")

    if not transcript_path:
        return None

    # Try direct path
    p = Path(transcript_path)
    if p.exists():
        return p

    # Try relative to sources
    sources = Path("/tmp/youtube-ai-research/sources")
    if sources.exists():
        for pattern in sources.rglob(f"{video['video_id']}.*"):
            return pattern

    # Try transcripts folder
    transcripts = Path("/tmp/youtube-ai-research/database/transcripts")
    if transcripts.exists():
        for pattern in transcripts.glob(f"{video['video_id']}.*"):
            return pattern

    return None


def load_transcript(path: Path) -> str | None:
    """Load transcript from file."""
    try:
        content = path.read_text()

        # Try YAML first
        if path.suffix in [".yaml", ".yml"]:
            data = yaml.safe_load(content)
            if isinstance(data, dict):
                # Try nested structure
                if "transcript" in data:
                    return data["transcript"].get("full_text", str(data["transcript"]))
                if "video" in data and isinstance(data["video"], dict):
                    return data["video"].get("transcript", {}).get("full_text", "")

        return content
    except Exception as e:
        print(f"    Warning: Could not load transcript: {e}")
        return None


def extract_insights(client, title: str, creator: str, transcript: str, model: str = DEFAULT_MODEL) -> str:
    """Extract insights from transcript using MiniMax API."""

    # Truncate if too long
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
        messages=[{"role": "user", "content": prompt}]
    )

    result = []
    for block in response.content:
        if hasattr(block, 'text'):
            result.append(block.text)
    return "\n".join(result)


def parse_insights(body: str) -> list[str]:
    """Extract bullet points from extraction body."""
    import re
    insights = []
    capture = False

    for line in body.split("\n"):
        stripped = line.strip()

        if re.match(r"^#{1,3}\s*Key\s*Insights?", stripped, re.IGNORECASE):
            capture = True
            continue

        if capture and re.match(r"^#{1,3}\s*(Tools|Techniques|Code|Summary|Resources|Difficulty|Relevance)", stripped, re.IGNORECASE):
            break

        if capture:
            cleaned = re.sub(r"^[-*\d.)\s]+", "", stripped).strip()
            if cleaned and len(cleaned) > 15:
                insights.append(cleaned)

    return insights[:10]


def create_video_page(video: dict, insights_body: str, dry_run: bool = False) -> list[dict]:
    """Create library pages for video insights. Returns list of created pages."""
    video_id = video["video_id"]
    title = video["title"]
    creator = video.get("channel_name", video.get("channel_slug", "Unknown"))
    tier = video.get("tier", "C")

    # Auto-detect shelf from content
    tags = detect_tags(insights_body)
    tools = extract_tools(insights_body)
    shelf = route_to_shelf(tags, title, insights_body)

    insights = parse_insights(insights_body)
    if not insights:
        print(f"  Warning: No insights extracted for {video_id}")
        return []

    created = []

    for i, insight in enumerate(insights):
        insight_short = insight[:120] + "..." if len(insight) > 120 else insight
        page_title = f"{title}: Insight {i+1}"

        if dry_run:
            print(f"  [DRY] Would create: {shelf} | {insight_short[:60]}")
            continue

        try:
            add_page(
                shelf=shelf,
                title=insight_short,
                content=insight,
                creator=creator,
                source_video=video_id,
                tags=",".join(tags + [shelf.split("/")[-1]]),
                tier=tier,
                dry_run=False,
            )
            created.append({
                "video_id": video_id,
                "shelf": shelf,
                "insight": insight_short[:80],
            })
        except Exception as e:
            print(f"  Error creating page: {e}")

    return created


def process_video(video: dict, args) -> dict:
    """Process a single video."""
    video_id = video["video_id"]
    title = video["title"]
    creator = video.get("channel_name", "Unknown")

    try:
        # Find and load transcript
        transcript_path = find_transcript(video)
        if not transcript_path:
            print(f"  ⚠ No transcript found for {video_id}")
            return {"video_id": video_id, "status": "no_transcript"}

        transcript = load_transcript(transcript_path)
        if not transcript:
            print(f"  ⚠ Empty transcript for {video_id}")
            return {"video_id": video_id, "status": "empty_transcript"}

        if args.dry_run:
            print(f"  [DRY] Would extract: {title[:50]}...")
            return {"video_id": video_id, "status": "dry_run"}

        # Extract insights
        client = get_minimax_client()
        insights = extract_insights(client, title, creator, transcript, args.model)

        # Save extraction to temp file
        EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
        extraction_path = EXTRACT_DIR / f"{video_id}.md"
        extraction_path.write_text(f"""---
video_id: {video_id}
title: {title}
creator: {creator}
extracted_at: {datetime.now().isoformat()}
tier: {video.get('tier', 'C')}
---

{insights}
""")

        # Create library pages
        created = create_video_page(video, insights, dry_run=False)

        print(f"  ✓ Extracted {len(created)} pages from {video_id}")
        return {"video_id": video_id, "status": "success", "pages_created": len(created)}

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return {"video_id": video_id, "status": "error", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Extract insights from prioritized videos")
    parser.add_argument("--input", type=str, default=str(PRIORITIZED_FILE),
                       help="Prioritized list JSON file")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be processed")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL,
                       help="MiniMax model to use")
    parser.add_argument("--workers", type=int, default=2,
                       help="Parallel workers")
    parser.add_argument("--limit", type=int, default=0,
                       help="Limit videos to process (0=all)")
    args = parser.parse_args()

    print(f"=== Extract Prioritized Videos ===")
    print(f"Input: {args.input}")

    videos = load_prioritized_list(Path(args.input))
    print(f"Found {len(videos)} videos in priority list")

    if args.limit > 0:
        videos = videos[:args.limit]
        print(f"Limited to {args.limit} videos")

    # Check already extracted
    extracted_ids = set()
    if EXTRACT_DIR.exists():
        for f in EXTRACT_DIR.rglob("*.md"):
            extracted_ids.add(f.stem)

    to_process = [v for v in videos if v["video_id"] not in extracted_ids]
    skipped = len(videos) - len(to_process)
    print(f"To process: {len(to_process)} (already extracted: {skipped})")

    if not to_process:
        print("Nothing to process.")
        return

    # Process videos
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_video, v, args): v for v in to_process}
        for future in as_completed(futures):
            results.append(future.result())

    # Summary
    success = sum(1 for r in results if r["status"] == "success")
    errors = sum(1 for r in results if r["status"] == "error")
    no_transcript = sum(1 for r in results if r["status"] in ["no_transcript", "empty_transcript"])

    print(f"\n{'='*50}")
    print(f"Results: {success} success, {errors} errors, {no_transcript} no transcript")

    pages_created = sum(r.get("pages_created", 0) for r in results)
    print(f"Pages created: {pages_created}")


if __name__ == "__main__":
    main()
