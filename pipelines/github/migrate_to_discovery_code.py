#!/usr/bin/env python3
"""
Migrate existing GitHub pages to discovery/code/repos shelf.
For each already-ingested GitHub page, create a second page in discovery/code/repos.
"""
import sys
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "queries"))
sys.path.insert(0, str(ROOT / "pipelines"))

import json
from add_book import add_page, get_next_page_id

GRAPH_PATH = ROOT / "_index" / "graph.json"
TRACKER = ROOT / "pipelines" / "github" / ".last_ingested"

def load_graph():
    if not GRAPH_PATH.exists():
        return []
    with open(GRAPH_PATH) as f:
        data = json.load(f)
    return data.get("nodes", [])

def main():
    nodes = load_graph()
    print(f"Total nodes in graph: {len(nodes)}")

    # Find GitHub-tagged nodes (excluding discovery/code)
    github_nodes = [
        n for n in nodes
        if "github" in n.get("tags", "") and "discovery/code" not in n.get("shelf", "")
    ]
    print(f"GitHub nodes (not already in discovery/code): {len(github_nodes)}")

    created = 0
    skipped = 0

    for i, node in enumerate(github_nodes):
        shelf = node.get("shelf", "")
        label = node.get("label", "")
        source_video = node.get("source_video", "")
        tags = node.get("tags", "")
        tier = node.get("tier", "C")

        # Skip if already in discovery/code
        if "discovery/code" in shelf:
            skipped += 1
            continue

        # Parse repo name from source_video URL
        if source_video and "github.com/" in source_video:
            repo = source_video.split("github.com/")[-1].replace(".git", "")
        else:
            repo = label.replace(" ", "-").lower()

        # Extract stars from score if available
        stars = node.get("score", 0)
        if stars:
            stars_str = f"{int(stars * 100):,}"
        else:
            stars_str = "0"

        # Build content
        content = f"**Repository**: [{repo}](https://github.com/{repo})\n\n"
        content += f"**Label**: {label}\n\n"
        content += f"**Stars (estimated)**: {stars_str}\n\n"
        content += f"**Original Shelf**: {shelf}\n\n"
        content += f"**Source**: [GitHub](https://github.com/{repo})"

        creator = node.get("creator", "GitHubQueueAnalysis")
        title = label or repo

        print(f"[{i+1}/{len(github_nodes)}] Creating: {title}...", end=" ")

        try:
            add_page(
                shelf="discovery/code/repos",
                title=title,
                content=content,
                creator=creator,
                source_video=source_video,
                tags="github,repository,discovery",
                tier=tier.replace("Tier ", ""),
                dry_run=False,
            )
            print("OK")
            created += 1
        except Exception as e:
            print(f"ERROR: {e}")

    print(f"\n=== Summary ===")
    print(f"Total github nodes: {len(github_nodes)}")
    print(f"Pages created: {created}")
    print(f"Skipped (already discovery/code): {skipped}")
    print(f"\nRun: python3 queries/rebuild_index.py")

if __name__ == "__main__":
    main()
