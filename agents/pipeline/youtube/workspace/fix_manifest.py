#!/usr/bin/env python3
"""Fix the manifest with the migration data."""

import json
import yaml
from pathlib import Path
from datetime import datetime

LIB = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")

# Re-scan created pages and rebuild manifest
pages = []
shelf_count = {}

# Scan all page files
for page_file in LIB.glob("sections/**/p_*.md"):
    page_id = page_file.stem
    content = page_file.read_text()

    # Extract title from first heading
    lines = content.split('\n')
    title = lines[0].lstrip('# ') if lines else page_id

    # Extract creator and source from "Source:" line
    creator = ""
    source_video = ""
    for line in lines:
        if line.startswith("**Source**: "):
            parts = line.replace("**Source**: ", "").split(" — ")
            if len(parts) >= 2:
                creator = parts[0]
                source_video = parts[1] if len(parts) > 1 else ""

    # Get shelf path
    shelf_path = str(page_file.parent.relative_to(LIB))
    if 'shelf.yaml' in [f.name for f in page_file.parent.iterdir()]:
        shelf_path = str(page_file.parent.relative_to(LIB))

    # Infer tags from title
    tags = []
    title_lower = title.lower()
    if 'agent' in title_lower: tags.append('agents')
    if 'code' in title_lower or 'coding' in title_lower: tags.append('coding_agents')
    if 'llm' in title_lower or 'model' in title_lower: tags.append('llms')
    if 'eval' in title_lower or 'benchmark' in title_lower: tags.append('evals')
    if 'rag' in title_lower or 'retrieval' in title_lower: tags.append('rag')
    if not tags: tags.append('general')

    # Build book_id from page_id (p_XXXX -> b_XXX)
    page_num = int(page_id.split('_')[1])
    book_num = (page_num // 10) + 1
    book_id = f"b_{book_num:03d}"

    pages.append({
        "id": page_id,
        "book_id": book_id,
        "title": title[:80],
        "shelf": shelf_path,
        "creator": creator,
        "score": 7.0,  # default
        "tier": "A",
        "tags": tags,
        "links_to": [],
        "contradicts": None,
        "extracted_at": "2026-03-19"
    })

    if shelf_path not in shelf_count:
        shelf_count[shelf_path] = []
    shelf_count[shelf_path].append(page_id)

print(f"Found {len(pages)} pages")

# Group by shelf
by_shelf = {}
for page in pages:
    shelf = page['shelf']
    if shelf not in by_shelf:
        by_shelf[shelf] = []
    by_shelf[shelf].append(page['id'])

# Write manifest
manifest = {
    "version": "1.0",
    "generated_at": datetime.now().isoformat(),
    "pages": pages,
    "total_pages": len(pages),
    "by_shelf": by_shelf,
    "by_creator": {}
}

manifest_file = LIB / "_index" / "_manifest.yaml"
with open(manifest_file, 'w') as f:
    yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

print(f"Manifest written to {manifest_file}")
print(f"Total pages: {len(pages)}")
