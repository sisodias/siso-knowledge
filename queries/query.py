#!/usr/bin/env python3
"""Query SISO Knowledge."""
import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Optional

LIB_PATH = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")


def load_manifest() -> dict:
    """Load the page manifest."""
    manifest_path = LIB_PATH / "_index" / "_manifest.yaml"
    if not manifest_path.exists():
        return {"pages": [], "total_pages": 0}

    import yaml
    with open(manifest_path) as f:
        return yaml.safe_load(f) or {"pages": [], "total_pages": 0}


def search_fts(query_text: str, shelf: Optional[str] = None,
               tier: Optional[str] = None, limit: int = 10) -> list:
    """Search using FTS5 index."""
    db_path = LIB_PATH / "_index" / "search.sqlite"
    if not db_path.exists():
        return []

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    sql = "SELECT * FROM pages_fts WHERE pages_fts MATCH ?"
    params = [query_text]

    if shelf:
        sql += " AND shelf LIKE ?"
        params.append(f"{shelf}%")
    if tier:
        sql += " AND tier = ?"
        params.append(tier)

    sql += f" LIMIT {limit}"

    try:
        cursor = conn.execute(sql, params)
        results = [dict(row) for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        results = []

    conn.close()
    return results


def search_json(query_text: str, shelf: Optional[str] = None,
                tier: Optional[str] = None, limit: int = 10) -> list:
    """Search using JSON indexes as fallback."""
    manifest = load_manifest()
    pages = manifest.get("pages", [])

    q_lower = query_text.lower()
    results = []

    for page in pages:
        # Text search in title and content
        text = f"{page.get('title', '')} {page.get('content', '')} {page.get('tags', [])}".lower()
        if q_lower not in text:
            continue

        if shelf and not page.get("shelf", "").startswith(shelf):
            continue
        if tier and page.get("tier") != tier:
            continue

        results.append(page)
        if len(results) >= limit:
            break

    return results


def query(query_text: str, shelf: Optional[str] = None,
           tier: Optional[str] = None, limit: int = 10, format: str = "md"):
    """Search pages in SISO Knowledge."""
    # Try FTS5 first, fall back to JSON
    results = search_fts(query_text, shelf, tier, limit)
    if not results:
        results = search_json(query_text, shelf, tier, limit)

    if format == "json":
        print(json.dumps({
            "query": query_text,
            "results": results,
            "total": len(results)
        }, indent=2))
        return

    # Markdown output
    if not results:
        print(f'## Query: "{query_text}"')
        print("**Results**: 0 pages found")
        print("\nNo matching pages found. Try running `rebuild_index.py` first.")
        return

    print(f'## Query: "{query_text}"')
    print(f"**Results**: {len(results)} pages found (showing top {min(len(results), limit)})")
    print()

    for i, page in enumerate(results, 1):
        title = page.get("title", "Untitled")
        page_id = page.get("id", "?")
        page_shelf = page.get("shelf", "N/A")
        creator = page.get("creator", "Unknown")
        score = page.get("score", 0)
        tags = page.get("tags", [])
        content = page.get("content", "")[:150]

        print(f"{i}. **{title}** ({page_id})")
        print(f"   Shelf: {page_shelf} | Creator: {creator} | Score: {score}")
        if tags:
            print(f"   Tags: {', '.join(tags)}")
        if content:
            print(f"   {content}...")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Query SISO Knowledge",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python query.py "multi-agent systems"
  python query.py "multi-agent" --shelf ai_research/agents
  python query.py "multi-agent" --tier A --limit 5
  python query.py "multi-agent" --format json
        """
    )
    parser.add_argument("query", nargs="?", default="", help="Search query")
    parser.add_argument("--shelf", help="Filter by shelf path")
    parser.add_argument("--tier", choices=["A", "B", "C"], help="Filter by tier")
    parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--format", choices=["md", "json"], default="md",
                        help="Output format (default: md)")
    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        return

    query(args.query, args.shelf, args.tier, args.limit, args.format)


if __name__ == "__main__":
    main()
