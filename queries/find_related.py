#!/usr/bin/env python3
"""Find related pages in SISO Library."""
import argparse
import json
import yaml
from pathlib import Path

LIB = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")


def find_related(page_id=None, tag=None, creator=None, limit=20, format="md"):
    """Find related pages by page_id, tag, or creator."""
    manifest = LIB / "_index" / "_manifest.yaml"
    if not manifest.exists():
        print("No manifest found. Run rebuild_index.py first.")
        return

    data = yaml.safe_load(open(manifest))
    pages = data.get('pages', [])

    results = []
    if page_id:
        target = next((p for p in pages if p.get('id') == page_id), None)
        if not target:
            print(f"Page {page_id} not found")
            return

        # Find pages this page links to
        links_to = set(target.get('links_to', []) or [])
        # Find pages that link TO this page
        for p in pages:
            if page_id in (p.get('links_to', []) or []):
                links_to.add(p['id'])
        # Add contradiction
        if target.get('contradicts'):
            links_to.add(target['contradicts'])

        for p in pages:
            if p.get('id') in links_to:
                results.append({**p, 'relation': 'linked'})

        title = target.get('title', '')[:50]
        print(f"## Pages related to {page_id} ({title})")

    elif tag:
        results = [p for p in pages if tag in (p.get('tags', []) or [])]
        print(f"## Pages tagged '{tag}'")

    elif creator:
        results = [p for p in pages if creator.lower() in p.get('creator', '').lower()]
        print(f"## Pages by '{creator}'")

    else:
        print("Specify --page-id, --tag, or --creator")
        return

    if format == "json":
        print(json.dumps({"results": results, "count": len(results)}, indent=2))
        return

    print(f"**{len(results)} pages found**\n")

    for r in results[:limit]:
        page_id_out = r.get('id', '?')
        title = r.get('title', '')[:60]
        shelf = r.get('shelf', 'N/A')
        creator = r.get('creator', 'Unknown')
        score = r.get('score', 0)
        tags = ', '.join(r.get('tags', []) or [])

        print(f"**[{page_id_out}] {title}**")
        print(f"   Shelf: {shelf} | Creator: {creator} | Score: {score}")
        if tags:
            print(f"   Tags: {tags}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Find related pages in SISO Library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python find_related.py --page-id p_001
  python find_related.py --tag langchain
  python find_related.py --creator "Latent Space"
  python find_related.py --page-id p_001 --format json
        """
    )
    parser.add_argument("--page-id", help="Find pages linked to this page ID")
    parser.add_argument("--tag", help="Find pages with this tag")
    parser.add_argument("--creator", help="Find pages by this creator")
    parser.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument("--format", choices=["md", "json"], default="md",
                       help="Output format (default: md)")
    args = parser.parse_args()

    if not args.page_id and not args.tag and not args.creator:
        parser.print_help()
        return

    find_related(args.page_id, args.tag, args.creator, args.limit, args.format)


if __name__ == "__main__":
    main()
