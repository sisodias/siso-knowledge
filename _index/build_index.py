#!/usr/bin/env python3
"""Rebuild all indexes from page files."""
import argparse
import fcntl
import json
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

LIB_PATH = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
INDEX_PATH = LIB_PATH / "_index"
MANIFEST_LOCK_TIMEOUT = 30  # seconds for rebuild


def scan_pages() -> list:
    """Scan all page files in the library."""
    pages = []
    sections_dir = LIB_PATH / "sections"

    if not sections_dir.exists():
        return pages

    # Pages can be in either:
    # - sections/{section}/{bookcase}/shelves/{shelf}/pages/p_*.md (new structure)
    # - sections/{section}/shelves/{shelf}/pages/p_*.md (old structure)
    # - sections/{section}/{bookcase}/shelves/{shelf}/p_*.md (direct in shelf)
    for page_file in sections_dir.rglob("p_*.md"):
        # Skip if it's a shelf.yaml or bookcase.yaml or _index.md
        if page_file.name in ["shelf.yaml", "bookcase.yaml", "_index.md", "section.yaml"]:
            continue
        page = parse_page_file(page_file)
        if page:
            # Compute shelf path relative to sections
            try:
                rel_path = page_file.relative_to(sections_dir)
                # shelf is everything up to but not including the page file itself
                # Filter out "pages" directory from shelf path
                shelf_parts = [p for p in rel_path.parts[:-1] if p != "pages"]
                page["shelf"] = "/".join(shelf_parts)
            except ValueError:
                pass
            pages.append(page)

    return pages


def parse_page_file(path: Path) -> Optional[dict]:
    """Parse a single page file."""
    try:
        content = path.read_text()
    except Exception:
        return None

    # Extract frontmatter if present
    page = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2].strip()
            # Parse YAML frontmatter
            page = yaml.safe_load(frontmatter) or {}
            page["content"] = body
    else:
        # No frontmatter - extract what we can
        page["content"] = content
        # Extract title from first heading
        lines = content.strip().split("\n")
        if lines:
            title = lines[0].strip().lstrip("# ").strip()
            if title:
                page["title"] = title

    # Extract page ID from filename
    match = re.search(r'p_(\d+)', path.name)
    if match:
        page["id"] = f"p_{match.group(1)}"

    # Extract creator from content if not in frontmatter
    if "creator" not in page:
        for line in body.split("\n"):
            if "Source:" in line:
                page["creator"] = line.split("Source:")[-1].strip()
                break

    # Set defaults for missing fields
    page.setdefault("score", 7.0)
    page.setdefault("tier", "B")
    page.setdefault("tags", [])
    page.setdefault("links_to", [])
    page.setdefault("contradicts")
    page["_file"] = str(path.relative_to(LIB_PATH))

    return page


def build_by_creator(pages: list) -> dict:
    """Build creator index with aggregated stats per spec."""
    by_creator = {}

    for page in pages:
        creator = page.get("creator", "Unknown")

        if creator not in by_creator:
            by_creator[creator] = {
                "bookcase": "unknown",
                "page_count": 0,
                "avg_score": 0.0,
                "tier_a_count": 0,
                "pages": [],
                "topics": set()
            }

        creator_data = by_creator[creator]
        creator_data["page_count"] += 1
        creator_data["pages"].append(page["id"])

        # Add score
        creator_data["avg_score"] += page.get("score", 0)

        # Count tier A
        if page.get("tier") == "A":
            creator_data["tier_a_count"] += 1

        # Extract topic from shelf path
        shelf = page.get("shelf", "")
        if shelf:
            # Get the last part of the shelf path as topic
            topic = shelf.split("/")[-1] if "/" in shelf else shelf
            if topic:
                creator_data["topics"].add(topic)

    # Finalize averages and convert sets
    for creator, data in by_creator.items():
        if data["page_count"] > 0:
            data["avg_score"] = round(data["avg_score"] / data["page_count"], 1)
        data["topics"] = sorted(list(data["topics"]))
        # Convert bookcase from shelf path
        if data["topics"]:
            data["bookcase"] = data["topics"][0] if data["topics"] else "unknown"

    return by_creator


def build_by_topic(pages: list) -> dict:
    """Build topic index mapping topics to shelves per spec."""
    by_topic = {}

    for page in pages:
        shelf = page.get("shelf", "")
        if not shelf:
            continue

        # Extract topic from shelf path (last part)
        topic = shelf.split("/")[-1] if "/" in shelf else shelf

        if topic not in by_topic:
            by_topic[topic] = {
                "shelf_path": f"sections/{shelf}",
                "page_count": 0,
                "top_pages": [],
                "consensus_pages": [],
                "contradiction_pairs": []
            }

        topic_data = by_topic[topic]
        topic_data["page_count"] += 1

        # Track top pages by score
        topic_data["top_pages"].append({
            "id": page["id"],
            "score": page.get("score", 0)
        })

        # Track contradictions
        if page.get("contradicts"):
            topic_data["contradiction_pairs"].append({
                "source": page["id"],
                "target": page["contradicts"]
            })

    # Sort top pages by score and limit to 10
    for topic, data in by_topic.items():
        data["top_pages"] = sorted(data["top_pages"], key=lambda x: x["score"], reverse=True)[:10]

    return by_topic


def build_by_tag(pages: list) -> dict:
    """Build tag index per spec."""
    by_tag = {}

    for page in pages:
        tags = page.get("tags", [])
        # Infer tags from shelf if none provided
        if not tags:
            shelf = page.get("shelf", "")
            if shelf:
                topic = shelf.split("/")[-1] if "/" in shelf else shelf
                if topic:
                    tags = [topic]

        for tag in tags:
            if tag not in by_tag:
                by_tag[tag] = {"pages": [], "count": 0}

            by_tag[tag]["pages"].append(page["id"])
            by_tag[tag]["count"] += 1

    return by_tag


def build_graph(pages: list) -> dict:
    """Build graph from pages per spec."""
    nodes = []
    edges = []

    # Create lookup for valid page IDs
    page_ids = {p["id"] for p in pages}

    for page in pages:
        # Determine tier label
        tier = page.get("tier", "B")
        tier_label = f"Tier {tier}" if tier else "Tier B"

        # Truncate title for label
        title = page.get("title", "")
        label = title[:50] + "..." if len(title) > 50 else title

        # Get shelf for node (simplified)
        shelf = page.get("shelf", "")
        shelf_label = shelf.replace("sections/", "").replace("/bookcases/", "/").replace("/shelves/", "/") if shelf else "unknown"

        nodes.append({
            "id": page["id"],
            "label": label,
            "shelf": shelf_label,
            "tier": tier_label,
            "score": page.get("score", 0),
            "tags": page.get("tags", [])
        })

        # Add edges from links_to
        links_to = page.get("links_to", []) or []
        for target in links_to:
            if target in page_ids:  # Only add edge if target exists
                edges.append({
                    "source": page["id"],
                    "target": target,
                    "type": "links_to"
                })

        # Add contradiction edges
        contradicts = page.get("contradicts")
        if contradicts and contradicts in page_ids:
            edges.append({
                "source": page["id"],
                "target": contradicts,
                "type": "contradicts"
            })

    return {"nodes": nodes, "edges": edges}


def rebuild_fts(pages: list):
    """Rebuild FTS5 index - drop and recreate table."""
    db_path = INDEX_PATH / "search.sqlite"
    conn = sqlite3.connect(str(db_path))

    # Drop and recreate FTS table
    conn.execute("DROP TABLE IF EXISTS pages_fts")
    conn.execute("CREATE VIRTUAL TABLE pages_fts USING fts5(title, content, tags, creator, source_video)")

    for page in pages:
        # Extract source_video from content if available
        source_video = ""
        content = page.get("content", "")
        for line in content.split("\n"):
            if "Source:" in line:
                source_video = line.split("Source:")[-1].strip()
                break

        conn.execute("""
            INSERT INTO pages_fts (title, content, tags, creator, source_video)
            VALUES (?, ?, ?, ?, ?)
        """, (
            page.get("title", ""),
            page.get("content", ""),
            ",".join(page.get("tags", [])),
            page.get("creator", ""),
            source_video
        ))

    conn.commit()
    conn.close()


def build_manifest(pages: list) -> dict:
    """Build the manifest from pages."""
    # Group by shelf
    by_shelf = {}
    by_creator = {}

    for page in pages:
        shelf = page.get("shelf", "unknown")
        creator = page.get("creator", "Unknown")

        if shelf not in by_shelf:
            by_shelf[shelf] = []
        by_shelf[shelf].append(page["id"])

        if creator not in by_creator:
            by_creator[creator] = []
        by_creator[creator].append(page["id"])

    # Build page entries (without content for manifest)
    page_entries = []
    for page in pages:
        entry = {k: v for k, v in page.items() if k != "content"}
        page_entries.append(entry)

    return {
        "version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "pages": page_entries,
        "total_pages": len(pages),
        "by_shelf": by_shelf,
        "by_creator": by_creator
    }


def rebuild(dry_run: bool = False, fast: bool = False):
    """Rebuild all indexes from page files."""
    print(f"Scanning {LIB_PATH}/sections/...")

    pages = scan_pages()
    print(f"Found {len(pages)} pages")

    if not pages:
        print("ERROR: No pages found!")
        return

    if dry_run:
        print("\n[DRY RUN] Would rebuild:")
        print(f"  - _manifest.yaml ({len(pages)} pages)")
        print(f"  - by_creator.json")
        print(f"  - by_topic.json")
        print(f"  - by_tag.json")
        print(f"  - graph.json")
        if not fast:
            print(f"  - search.sqlite (FTS5)")
        return

    # Build indexes
    by_creator = build_by_creator(pages)
    by_topic = build_by_topic(pages)
    by_tag = build_by_tag(pages)
    graph = build_graph(pages)
    manifest = build_manifest(pages)

    # Write indexes with file locking for manifest
    print("Writing _manifest.yaml...")
    manifest_path = INDEX_PATH / "_manifest.yaml"
    lock_path = manifest_path.with_suffix(".lock")

    # Acquire exclusive lock with timeout
    lock_start = time.time()
    lock_file = open(lock_path, "w")
    while True:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except IOError:
            if time.time() - lock_start > MANIFEST_LOCK_TIMEOUT:
                lock_file.close()
                print(f"Error: Could not acquire lock on {manifest_path} after {MANIFEST_LOCK_TIMEOUT}s", file=sys.stderr)
                raise TimeoutError(f"Could not acquire lock on {manifest_path}")
            time.sleep(0.1)

    try:
        with open(manifest_path, "w") as f:
            yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True)
    finally:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()

    print("Writing by_creator.json...")
    with open(INDEX_PATH / "by_creator.json", "w") as f:
        json.dump(by_creator, f, indent=2)

    print("Writing by_topic.json...")
    with open(INDEX_PATH / "by_topic.json", "w") as f:
        json.dump(by_topic, f, indent=2)

    print("Writing by_tag.json...")
    with open(INDEX_PATH / "by_tag.json", "w") as f:
        json.dump(by_tag, f, indent=2)

    print("Writing graph.json...")
    with open(INDEX_PATH / "graph.json", "w") as f:
        json.dump(graph, f, indent=2)

    # Copy graph.json to graph/ for HTML
    graph_html_dir = LIB_PATH / "graph"
    if graph_html_dir.exists():
        print("Copying graph.json to graph/...")
        with open(graph_html_dir / "graph.json", "w") as f:
            json.dump(graph, f, indent=2)

    if not fast:
        print("Rebuilding search.sqlite (FTS5)...")
        rebuild_fts(pages)

    # Summary
    print("\n" + "="*50)
    print("Index rebuilt successfully!")
    print(f"  Total pages: {len(pages)}")
    print(f"  Creators: {len(by_creator)}")
    print(f"  Topics: {len(by_topic)}")
    print(f"  Tags: {len(by_tag)}")
    print(f"  Graph nodes: {len(graph['nodes'])}, edges: {len(graph['edges'])}")


def main():
    parser = argparse.ArgumentParser(
        description="Rebuild all indexes from page files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This is the "source of truth reset" — always safe to run.
Rebuilds: _manifest.yaml, by_creator.json, by_topic.json, by_tag.json,
          graph.json, search.sqlite

Examples:
  python rebuild_index.py              # Full rebuild
  python rebuild_index.py --dry-run    # Show what would change
  python rebuild_index.py --fast       # Skip FTS5 rebuild
        """
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would change without writing")
    parser.add_argument("--fast", action="store_true",
                        help="Skip FTS5 rebuild")
    args = parser.parse_args()

    rebuild(args.dry_run, args.fast)


if __name__ == "__main__":
    main()
