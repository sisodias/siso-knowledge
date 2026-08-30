#!/usr/bin/env python3
"""
Concept Linker — scan all library pages for shared tools/frameworks,
find cross-page concept relationships, and write links_to edges to
frontmatter. Then rebuild the graph so it has real edges.

Usage:
  python3 pipelines/youtube/concept_linker.py
  python3 pipelines/youtube/concept_linker.py --dry-run
  open graph/index.html   # see connected graph
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys_path_inserted = False

# Known tools we care about for linking
CONCEPT_KEYWORDS = [
    "claude code", "opencode", "codex", "aider", "cursor", "devin",
    "swe-agent", "swe agent", "openclaw", "clawdbot", "cloudbot",
    "langchain", "langgraph", "llamaindex", "crewai", "autogen",
    "autogenstudio", "mastra", "inngest",
    "vllm", "ollama", "lm studio", "lmstudio", "tensorrt", "tgi",
    "kubernetes", "k8s", "docker", "github actions", "gitlab ci",
    "playwright", "puppeteer", "selenium",
    "pinecone", "weaviate", "chroma", "qdrant", "milvus",
    "llama", "mistral", "phi", "gemma", "qwen", "deepseek",
    "claude", "gpt-4", "gpt-4o", "gemini",
    "react", "next.js", "nextjs",
    "mcp", "model context protocol",
    "mem0", "memgpt",
    "postgres", "postgresql", "redis",
]


def scan_pages() -> list[dict]:
    """Scan all p_*.md pages and return list of page dicts."""
    global sys_path_inserted
    if not sys_path_inserted:
        import sys
        sys.path.insert(0, str(ROOT / "queries"))
        sys_path_inserted = True

    from rebuild_index import scan_pages, parse_page_file

    pages = []
    sections_dir = ROOT / "sections"
    if not sections_dir.exists():
        return pages

    for page_file in sections_dir.rglob("p_*.md"):
        if page_file.name in ["shelf.yaml", "bookcase.yaml", "_index.md", "section.yaml"]:
            continue
        page = parse_page_file(page_file)
        if page:
            try:
                rel = page_file.relative_to(sections_dir)
                shelf_parts = [p for p in rel.parts[:-1] if p != "pages"]
                page["shelf"] = "/".join(shelf_parts)
            except ValueError:
                pass
            page["_path"] = page_file
            pages.append(page)

    return pages


def extract_concepts(page: dict) -> set[str]:
    """Extract known tool/framework concepts from a page."""
    content = (page.get("title", "") + " " + page.get("content", "")).lower()
    found = set()
    for concept in CONCEPT_KEYWORDS:
        pattern = r'\b' + re.escape(concept) + r'\b'
        if re.search(pattern, content):
            found.add(concept)
    return found


def find_related_pages(page: dict, all_pages: list[dict], top_n: int = 5) -> list[str]:
    """Find pages sharing the most concepts with this one."""
    page_concepts = page.get("_concepts", set())
    if not page_concepts:
        return []

    scores = []
    for other in all_pages:
        if other["id"] == page["id"]:
            continue
        other_concepts = other.get("_concepts", set())
        overlap = page_concepts & other_concepts
        if overlap:
            scores.append((other["id"], len(overlap), overlap))

    # Sort by overlap count descending
    scores.sort(key=lambda x: -x[1])
    return [s[0] for s in scores[:top_n]]


def main():
    parser = argparse.ArgumentParser(description="Link pages by shared concepts")
    parser.add_argument("--dry-run", action="store_true", help="Show links without writing")
    parser.add_argument("--min-overlap", type=int, default=1, help="Min shared concepts to link")
    parser.add_argument("--top-n", type=int, default=5, help="Max links per page")
    args = parser.parse_args()

    print("Scanning pages...")
    pages = scan_pages()
    print(f"Found {len(pages)} pages")

    # Extract concepts per page
    for page in pages:
        page["_concepts"] = extract_concepts(page)
        page["_links"] = find_related_pages(page, pages, args.top_n)

    # Count how many will get links
    pages_with_links = [p for p in pages if p["_links"]]
    print(f"Pages with concept links: {len(pages_with_links)}")

    if args.dry_run:
        print("\n[DRY RUN] Top concept links:")
        for page in pages_with_links[:20]:
            concepts = list(page["_concepts"])[:5]
            links = page["_links"][:3]
            print(f"  {page['id']} ({', '.join(concepts)}) -> {links}")
        return

    # Write links_to to page frontmatter
    updated = 0
    for page in pages:
        if not page["_links"]:
            continue

        path = page["_path"]
        content = path.read_text()

        # Update links_to in frontmatter
        links_to = page["_links"]

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm_text = parts[1]
                body = parts[2]

                try:
                    fm = yaml.safe_load(fm_text) or {}
                except Exception:
                    continue

                fm["links_to"] = links_to

                # Re-serialize
                fm_yaml = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
                new_content = f"---\n{fm_yaml}---\n{body}"
                path.write_text(new_content)
                updated += 1
        else:
            # No frontmatter — inject at top
            fm = {
                "id": page["id"],
                "links_to": links_to,
            }
            fm_yaml = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
            new_content = f"---\n{fm_yaml}---\n\n{content}"
            path.write_text(new_content)
            updated += 1

    print(f"Updated {updated} page files with concept links")

    # Rebuild graph.json from updated pages
    print("Rebuilding graph...")
    import sys
    sys.path.insert(0, str(ROOT / "queries"))
    from rebuild_index import rebuild
    rebuild(dry_run=False, fast=True)

    # Verify
    graph_path = ROOT / "_index" / "graph.json"
    if graph_path.exists():
        g = json.loads(graph_path.read_text())
        print(f"\nGraph: {len(g['nodes'])} nodes, {len(g['edges'])} edges")
        if g['edges']:
            print("Graph is LIVE — run: open graph/index.html")


if __name__ == "__main__":
    main()
