#!/usr/bin/env python3
"""
Ingest YouTube extractions into SISO_Knowledge.

Reads new .md files from /tmp/youtube-ai-research/extracted/by_date/,
skips already-ingested (tracked in .last_ingested),
creates one page per Key Insight via add_book.py,
and calls rebuild_index.py after the batch.

Usage:
  python3 pipelines/youtube/ingest.py         # ingest new files only
  python3 pipelines/youtube/ingest.py --all   # re-ingest everything (reset tracking)
  python3 pipelines/youtube/ingest.py --dry-run
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

# Add queries/ to path for add_book import
ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines"))

from shared.topic_router import route_to_shelf, detect_tags, extract_tools

EXTRACT_DIR = Path("/tmp/youtube-ai-research/extracted/by_date")
TRACKER_FILE = ROOT / "pipelines" / "youtube" / ".last_ingested"
OUTBOX_DIR = ROOT / "pipelines" / "youtube" / "outbox"


def load_tracker() -> set[str]:
    """Load set of already-ingested video IDs."""
    if not TRACKER_FILE.exists():
        return set()
    return set(TRACKER_FILE.read_text().strip().splitlines())


def save_tracker(ids: set[str]):
    """Append newly ingested IDs to tracker."""
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = load_tracker()
    updated = existing | ids
    TRACKER_FILE.write_text("\n".join(sorted(updated)) + "\n")


def find_extraction_files(all_files: bool = False) -> list[Path]:
    """Find all .md extraction files, newest first."""
    if not EXTRACT_DIR.exists():
        print(f"WARNING: Extraction dir not found: {EXTRACT_DIR}")
        return []

    files = sorted(EXTRACT_DIR.rglob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def parse_extraction(path: Path) -> dict | None:
    """Parse a YouTube extraction file into a structured dict."""
    try:
        content = path.read_text()
    except Exception as e:
        print(f"  ERROR reading {path.name}: {e}")
        return None

    # Split frontmatter
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    frontmatter_raw = parts[1]
    body = parts[2].strip()

    try:
        meta = yaml.safe_load(frontmatter_raw) or {}
    except Exception:
        return None

    video_id = meta.get("video_id", path.stem)
    title = meta.get("title", "")
    creator = meta.get("creator", "")
    extracted_at = meta.get("extracted_at", "")

    # Extract insights from body
    insights = _extract_insights(body)
    tools = extract_tools(body)
    tags = detect_tags(body)

    # Auto-assign shelf
    shelf = route_to_shelf(tags, title, body)

    # Determine tier based on content richness
    tier = "C"
    if len(insights) >= 5 and len(body) > 500:
        tier = "A"
    elif len(insights) >= 2:
        tier = "B"

    return {
        "video_id": video_id,
        "title": title,
        "creator": creator,
        "extracted_at": extracted_at,
        "body": body,
        "insights": insights,
        "tools": tools,
        "tags": tags,
        "shelf": shelf,
        "tier": tier,
    }


def _extract_insights(body: str) -> list[str]:
    """Extract bullet points / numbered insights from extraction body."""
    insights = []

    # Strategy 1: Look for Key Insights after table cells with inline bullets
    # Table format: "| Key Insights** | • bullet1<br>• bullet2 |"
    # Or inline: "Key Insights** | • bullet1 • bullet2"
    for line in body.split("\n"):
        if "Key Insights" in line and ("•" in line or "<br>" in line.lower()):
            # Split on bullet separators (• or <br>) and extract content after the marker
            parts = re.split(r"•|<br>", line, flags=re.IGNORECASE)
            for part in parts:
                part = part.strip().rstrip("|").strip()
                # Remove leading bullet marker
                part = re.sub(r"^[\s*\-•]+", "", part).strip()
                # Clean HTML
                part = re.sub(r"<[^>]+>", "", part).strip()
                # Skip header-like content
                if not part or len(part) < 15:
                    continue
                # Skip table separator lines (|---|---| etc)
                if re.match(r"^\s*\|[\s\-|:]*\|\s*$", part):
                    continue
                # Skip parts that are mostly pipes/dashes (table artifacts)
                stripped = re.sub(r"[\|\-\s]", "", part)
                if len(stripped) < 5:
                    continue
                if re.match(r"^\s*[\|\s]*(\*\*)?\s*Key Insights", part, re.IGNORECASE):
                    continue
                insights.append(part)
            if insights:
                return insights[:10]

    # Strategy 2: Standard markdown bullet list after Key Insights header
    lines = body.split("\n")
    capture = False
    for line in lines:
        stripped = line.strip()
        if re.match(r"^#{1,3}\s*Key\s*Insights?", stripped, re.IGNORECASE):
            capture = True
            continue
        if capture and re.match(r"^#{1,3}\s*(Tools|Techniques|Code|Summary|Resources|Difficulty|Relevance|Title|Creator)", stripped, re.IGNORECASE):
            break
        if capture:
            cleaned = re.sub(r"^[-*\u2022\u25e6\d.)\s]+", "", stripped)
            cleaned = cleaned.strip()
            # Skip table rows and markdown-pipe artifacts
            if not cleaned or len(cleaned) < 15:
                continue
            # Skip table rows (| col1 | col2 |)
            if cleaned.startswith("|") or re.match(r"^\s*\|", stripped):
                continue
            insights.append(cleaned)

    # Strategy 3: Fallback — grab all bullet lines
    if not insights:
        for line in body.split("\n"):
            stripped = line.strip()
            if re.match(r"^[-*\u2022\u25e6]\s", stripped):
                cleaned = stripped.lstrip("-*\u2022\u25e6 ").strip()
                if cleaned and len(cleaned) > 15:
                    insights.append(cleaned)

    # Final filter: remove anything that looks like a table row
    filtered = []
    for ins in insights:
        ins_stripped = ins.strip()
        if ins_stripped.startswith('|'):
            continue
        if re.match(r'^[\|\-\s]+$', ins_stripped):
            continue
        if re.match(r'^\s*\|[\s\-|:]*\|\s*$', ins_stripped):
            continue
        filtered.append(ins)
    
    return filtered[:10]


def _build_content(title: str, body: str, tools: list[str]) -> str:
    """Build page content from body."""
    # Use the body content as-is, trimmed
    content = body.strip()

    # If tools were found, add a brief footer
    if tools:
        tool_str = ", ".join(tools[:5])
        content += f"\n\n**Tools & Technologies**: {tool_str}"

    # Trim if too long (page content should be focused)
    if len(content) > 2000:
        content = content[:2000] + "\n\n*(truncated)*"

    return content


def ingest_file(path: Path, dry_run: bool = False) -> list[dict] | None:
    """Ingest a single extraction file. Returns list of pages created."""
    data = parse_extraction(path)
    if not data:
        return None

    if not data["insights"]:
        return None  # Skip files with no usable insights

    created = []

    # Import add_book dynamically to avoid polluting module scope
    sys.path.insert(0, str(ROOT / "queries"))
    try:
        from add_book import add_page, get_next_page_id, get_shelf_path
    except ImportError as e:
        print(f"  ERROR: Could not import add_book: {e}")
        return None

    for i, insight in enumerate(data["insights"]):
        # Skip table artifacts and empty insights
        if not insight.strip() or len(insight.strip()) < 10:
            continue
        if re.match(r"^\s*\|[\s\-|:]*\|?\s*$", insight):
            continue  # Skip table separators

        # Each insight gets its own page
        page_title = f"{data['title']}: Insight {i+1}"

        # Shorten title for page
        insight_short = insight[:120] + "..." if len(insight) > 120 else insight

        shelf_path = get_shelf_path(data["shelf"])
        if not shelf_path.exists():
            print(f"  WARNING: Shelf not found: {data['shelf']} — skipping")
            continue

        page_id = get_next_page_id()
        content = _build_content(data["title"], insight, data["tools"])

        tags = list(set(data["tags"] + [data["shelf"].split("/")[-1]]))

        if dry_run:
            print(f"  [DRY] Would create: {page_id} | {data['shelf']} | {insight_short[:60]}")
        else:
            add_page(
                shelf=data["shelf"],
                title=insight_short,
                content=content,
                creator=data["creator"],
                source_video=data["video_id"],
                tags=",".join(tags),
                tier=data["tier"],
                dry_run=False,
            )
            created.append({
                "page_id": page_id,
                "shelf": data["shelf"],
                "insight": insight_short[:80],
                "video_id": data["video_id"],
            })

    return created if not dry_run else []


def main():
    parser = argparse.ArgumentParser(description="Ingest YouTube extractions into SISO_Knowledge")
    parser.add_argument("--all", action="store_true", help="Re-ingest all files (ignore tracking)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be ingested")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of files to process (0=all)")
    args = parser.parse_args()

    print(f"=== YouTube Ingest ===")
    print(f"Extract dir: {EXTRACT_DIR}")
    print(f"Library:     {ROOT}")

    files = find_extraction_files()
    print(f"Found {len(files)} extraction files")

    if not args.all:
        tracker = load_tracker()
        files = [f for f in files if f.stem not in tracker]
        print(f"New files to process: {len(files)} (already ingested: {len(tracker)})")
    else:
        print("Mode: --all (re-ingesting everything)")

    if args.limit > 0:
        files = files[:args.limit]
        print(f"Limit: {args.limit} files")

    if not files:
        print("Nothing to ingest.")
        return

    if args.dry_run:
        print("\n[DRY RUN] Would ingest:")
        for f in files:
            data = parse_extraction(f)
            if data and data["insights"]:
                for i, ins in enumerate(data["insights"][:3]):
                    shelf = data["shelf"]
                    ins_short = ins[:60]
                    print(f"  {f.stem} -> {shelf} -> {ins_short}...")
        return

    # Process files
    total_created = 0
    new_ids = set()

    for i, path in enumerate(files):
        print(f"\n[{i+1}/{len(files)}] Processing: {path.name}")
        created = ingest_file(path, dry_run=False)
        if created:
            total_created += len(created)
            new_ids.add(path.stem)
            for c in created:
                print(f"  Created: {c['page_id']} on {c['shelf']}")
        else:
            print(f"  Skipped (no insights or parse error)")
            new_ids.add(path.stem)  # track skipped too so we don't re-process empty files

    # Update tracker
    if new_ids:
        save_tracker(new_ids)
        print(f"\nUpdated tracker with {len(new_ids)} files")

    print(f"\n=== Summary ===")
    print(f"Files processed: {len(files)}")
    print(f"Pages created:   {total_created}")

    if total_created > 0:
        print(f"\nRun: python3 queries/rebuild_index.py  # to update indexes")


if __name__ == "__main__":
    main()
