#!/usr/bin/env python3
"""
Synthesize video insights into book-level pages.

Given a batch of pages from the same video/book shelf, writes a synthesized
book-level page that consolidates all insights. This becomes the parent book page.

Usage:
    python3 pipelines/youtube/synthesize.py
    python3 pipelines/youtube/synthesize.py --video-id dQw4w9WgXcQ
    python3 pipelines/youtube/synthesize.py --shelf ai_research/youtube/videos
    python3 pipelines/youtube/synthesize.py --dry-run
"""
import argparse
import json
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")
sys.path.insert(0, str(ROOT / "queries"))

from add_book import add_page, get_next_page_id, get_shelf_path


def find_video_pages(video_id: str) -> list[Path]:
    """Find all pages from a specific video."""
    pages_dir = ROOT / "sections"

    pages = []
    for page_file in pages_dir.rglob("p_*.md"):
        try:
            content = page_file.read_text()

            # Check if page is from this video
            if f'source_video: "{video_id}' in content:
                pages.append(page_file)
            elif f"source_video: '{video_id}" in content:
                pages.append(page_file)
            elif f"source_video: {video_id}" in content:
                pages.append(page_file)
        except Exception:
            continue

    return pages


def find_shelf_pages(shelf: str) -> list[Path]:
    """Find all pages in a shelf."""
    shelf_path = get_shelf_path(shelf)

    if not shelf_path.exists():
        return []

    return list(shelf_path.glob("p_*.md"))


def parse_page(path: Path) -> dict:
    """Parse a page file."""
    content = path.read_text()

    # Extract frontmatter
    if not content.startswith("---"):
        return {"id": path.stem, "content": content, "error": "no_frontmatter"}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {"id": path.stem, "content": content, "error": "invalid_frontmatter"}

    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except Exception:
        return {"id": path.stem, "content": content, "error": "yaml_error"}

    body = parts[2].strip()

    # Extract title from body
    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1) if title_match else path.stem

    return {
        "id": frontmatter.get("id", path.stem),
        "title": frontmatter.get("title", title),
        "shelf": frontmatter.get("shelf", ""),
        "creator": frontmatter.get("creator", ""),
        "source_video": frontmatter.get("source_video", ""),
        "tags": frontmatter.get("tags", []),
        "tier": frontmatter.get("tier", "C"),
        "content": body,
    }


def synthesize_video(video_id: str, pages: list[dict], dry_run: bool = False) -> dict:
    """Synthesize multiple pages from a video into a book page."""

    if not pages:
        return {"status": "no_pages", "message": "No pages to synthesize"}

    # Get common metadata from first page
    first = pages[0]
    creator = first.get("creator", "Unknown")
    shelf = first.get("shelf", "ai_research/youtube/videos")
    tags = first.get("tags", [])

    # Consolidate all insights
    all_insights = []
    for page in pages:
        # Extract insight content (skip title and source lines)
        content = page.get("content", "")
        lines = content.split("\n")

        insight_lines = []
        capture = False
        for line in lines:
            stripped = line.strip()

            # Skip title and source lines
            if stripped.startswith("# ") or stripped.startswith("**Source**"):
                continue

            # Skip "Why it matters" sections
            if stripped.startswith("**Why"):
                break

            if stripped and len(stripped) > 20:
                insight_lines.append(stripped)

        all_insights.extend(insight_lines)

    # Build book content
    video_title = pages[0].get("title", "Video").split(":")[0].strip()

    book_content = f"""# {video_title} — Full Analysis

## Summary
This page consolidates {len(pages)} key insights extracted from the video.

## Consolidated Insights

"""
    for i, insight in enumerate(all_insights[:20], 1):
        book_content += f"{i}. {insight}\n"

    if len(all_insights) > 20:
        book_content += f"\n*... and {len(all_insights) - 20} more insights*\n"

    # Add common tags
    video_tag = f"video_{video_id[:8]}"
    if video_tag not in tags:
        tags.append(video_tag)

    book_title = f"{video_title} — Book"

    if dry_run:
        print(f"  [DRY] Would create book: {book_title}")
        print(f"        Shelf: {shelf}")
        print(f"        Links to: {[p['id'] for p in pages]}")
        return {"status": "dry_run", "pages": len(pages)}

    try:
        # Create book page
        book_id = get_next_page_id()

        # Convert tags list to comma-separated string if needed
        if isinstance(tags, list):
            tags_str = ",".join(tags) if tags else ""
        else:
            tags_str = str(tags) if tags else ""

        # Use add_book module to create
        add_page(
            shelf=shelf,
            title=book_title,
            content=book_content,
            creator=creator,
            source_video=video_id,
            tags=tags_str,
            links_to=",".join([p["id"] for p in pages]),
            tier="B",
            dry_run=False,
        )

        return {
            "status": "success",
            "book_id": book_id,
            "pages": len(pages),
            "linked_pages": [p["id"] for p in pages],
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


def synthesize_shelf(shelf: str, dry_run: bool = False) -> dict:
    """Synthesize all videos in a shelf into books."""
    pages = find_shelf_pages(shelf)

    if not pages:
        return {"status": "no_pages", "message": f"No pages found in shelf: {shelf}"}

    # Group pages by video
    video_pages = {}
    for page_path in pages:
        page = parse_page(page_path)
        video_id = page.get("source_video", "")
        if not video_id:
            continue

        if video_id not in video_pages:
            video_pages[video_id] = []
        video_pages[video_id].append(page)

    print(f"Found {len(video_pages)} videos in shelf {shelf}")

    # Synthesize each video
    results = []
    for video_id, pages_list in video_pages.items():
        result = synthesize_video(video_id, pages_list, dry_run)
        results.append({"video_id": video_id, **result})

    success = sum(1 for r in results if r.get("status") == "success")

    return {
        "status": "completed",
        "videos_processed": len(video_ids := video_pages),
        "books_created": success,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Synthesize video pages into books")
    parser.add_argument("--video-id", type=str, default="",
                       help="Synthesize specific video")
    parser.add_argument("--shelf", type=str, default="",
                       help="Synthesize all videos in a shelf")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be created")
    args = parser.parse_args()

    print(f"=== YouTube Video Synthesizer ===")

    if args.video_id:
        print(f"Synthesizing video: {args.video_id}")
        pages = find_video_pages(args.video_id)
        print(f"Found {len(pages)} pages")

        if not pages:
            print("No pages found for this video.")
            return

        parsed = [parse_page(p) for p in pages]
        result = synthesize_video(args.video_id, parsed, args.dry_run)
        print(f"Result: {result}")

    elif args.shelf:
        print(f"Synthesizing shelf: {args.shelf}")
        result = synthesize_shelf(args.shelf, args.dry_run)
        print(f"Result: {result}")

    else:
        # Default: synthesize recent videos
        print("No --video-id or --shelf specified.")
        print("Looking for recent videos to synthesize...")

        # Find recent pages
        pages_dir = ROOT / "sections" / "ai_research" / "bookcases" / "youtube" / "shelves" / "videos" / "pages"

        if not pages_dir.exists():
            print(f"Pages directory not found: {pages_dir}")
            return

        recent_pages = sorted(pages_dir.glob("p_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:50]

        # Group by video
        video_pages = {}
        for page_path in recent_pages:
            page = parse_page(page_path)
            video_id = page.get("source_video", "")
            if video_id and video_id not in video_pages:
                video_pages[video_id] = []

            if video_id:
                video_pages[video_id].append(page)

        # Synthesize top 5 videos
        print(f"Found {len(video_pages)} videos")

        for video_id in list(video_pages.keys())[:5]:
            pages_list = video_pages[video_id]
            print(f"\nSynthesizing {video_id} ({len(pages_list)} pages)...")
            result = synthesize_video(video_id, pages_list, args.dry_run)
            print(f"  Result: {result.get('status')}")

    print(f"\nDone.")


if __name__ == "__main__":
    main()
