#!/usr/bin/env python3
"""Migrate YouTube research data to SISO_Library pages."""

import json
import yaml
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

LIB = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")
INDEX = Path("/Users/shaansisodia/SISO_Workspace/agent_os/agents/research/YouTubeQueueAnalysis/workspace/library_index.json")
EXTRACTED = Path("/tmp/youtube-ai-research/extracted/by_date/2026/03-March")

# Topic to shelf mapping
TOPIC_SHELF_MAP = {
    "agents": "sections/ai_research/bookcases/agents/shelves/multi_agent",
    "coding_agents": "sections/ai_research/bookcases/agents/shelves/code_agents",
    "llms": "sections/ai_research/bookcases/llms/shelves/reasoning",
    "rag": "sections/ai_research/bookcases/rag/shelves/retrieval",
    "claude_code": "sections/ai_research/bookcases/claude_code/shelves/patterns",
    "evals": "sections/ai_research/bookcases/evals/shelves/benchmarks",
    "infrastructure": "sections/infrastructure/bookcases/llm_serving/shelves/inference",
    "devops": "sections/infrastructure/bookcases/devops/shelves/ci_cd",
    "kubernetes": "sections/infrastructure/bookcases/kubernetes/shelves/patterns",
    "frontend": "sections/infrastructure/bookcases/frontend/shelves/web_agents",
    "css": "sections/infrastructure/bookcases/frontend/shelves/web_agents",
    "web_dev": "sections/infrastructure/bookcases/frontend/shelves/web_agents",
    "ecosystem": "sections/ecosystem/bookcases/opensource/shelves/models",
    "automation": "sections/product/bookcases/business_automation/shelves/automation",
}

def get_shelf(topics):
    """Get primary shelf from topics."""
    for topic in topics:
        if topic in TOPIC_SHELF_MAP:
            return TOPIC_SHELF_MAP[topic]
    return "sections/ai_research/bookcases/agents/shelves/multi_agent"  # default

def extract_key_insights(source_path):
    """Extract Key Insights bullets from source file."""
    try:
        content = Path(source_path).read_text()
        # Find Key Insights section
        match = re.search(r'\*\*Key Insights:\*\*\n(.*?)(?:\n\*\*|\Z)', content, re.DOTALL)
        if match:
            bullets = match.group(1).strip().split('\n')
            insights = []
            for bullet in bullets:
                bullet = bullet.strip().lstrip('- ')
                if bullet:
                    insights.append(bullet)
            return insights
    except Exception as e:
        print(f"Error reading {source_path}: {e}")
    return []

def detect_tags(insight):
    """Detect tags from insight text."""
    tags = []
    keywords = {
        "agent": "agents", "multi-agent": "agents", "coordination": "agents",
        "coding": "coding_agents", "code": "coding_agents", "dev": "coding_agents",
        "llm": "llms", "model": "llms", "gpt": "llms", "claude": "llms",
        "rag": "rag", "retrieval": "rag", "vector": "rag",
        "eval": "evals", "benchmark": "evals", "testing": "evals",
        "infrastructure": "infrastructure", "serving": "inference",
        "devops": "devops", "ci/cd": "devops", "deployment": "devops",
        "kubernetes": "kubernetes", "k8s": "kubernetes",
        "frontend": "frontend", "css": "css", "web": "web_dev",
        "open source": "ecosystem", "opensource": "ecosystem",
        "automation": "automation", "workflow": "automation"
    }
    insight_lower = insight.lower()
    for kw, tag in keywords.items():
        if kw in insight_lower and tag not in tags:
            tags.append(tag)
    return tags[:3] if tags else ["general"]

def main():
    # Load index
    with open(INDEX) as f:
        data = json.load(f)

    # Track counters
    shelf_counters = defaultdict(lambda: 1)
    video_to_book = {}
    book_counter = 1
    page_counter = 1
    manifest_pages = []

    # Process Tier A only
    tier_a = data['by_tier']['A']
    print(f"Processing {len(tier_a)} Tier A entries...")

    for idx, entry in enumerate(tier_a):
        video_id = entry['video_id']
        title = entry['title']
        creator = entry['creator']
        score = entry['score']
        topics = entry['topics']
        source_path = entry['source_path']
        extracted_at = entry['extracted_at']

        # Get shelf
        shelf_path = get_shelf(topics)
        shelf_name = Path(shelf_path).name
        shelf_dir = LIB / shelf_path

        # Ensure shelf directory exists
        shelf_dir.mkdir(parents=True, exist_ok=True)

        # Assign book_id
        book_id = f"b_{book_counter:03d}"
        video_to_book[video_id] = book_id
        book_counter += 1
        book_pages = []

        # Extract insights
        insights = extract_key_insights(source_path)
        if not insights:
            print(f"  Warning: No insights for {video_id}")
            continue

        print(f"  [{idx+1}/{len(tier_a)}] {video_id}: {len(insights)} insights -> {shelf_name}")

        for insight in insights:
            page_id = f"p_{page_counter:04d}"
            page_counter += 1

            # Create page title (first 80 chars)
            page_title = insight[:80] if len(insight) > 80 else insight

            # Extract date for frontmatter
            date_str = extracted_at[:10] if extracted_at else "2026-03-19"

            # Detect tags
            tags = detect_tags(insight)

            # Format page content
            # Bold the first sentence/claim
            sentences = insight.split('. ')
            if sentences:
                first_part = sentences[0]
                rest = '. '.join(sentences[1:]) if len(sentences) > 1 else ""
                if rest:
                    formatted_insight = f"**{first_part}.** {rest}"
                else:
                    formatted_insight = f"**{first_part}.**"

            # Infer "why it matters"
            why_matters = "This insight highlights an important trend or technique in AI development."

            content = f"""# {page_title}

{formatted_insight}

**Why it matters**: {why_matters}

**Source**: {creator} — {title}
"""

            # Write page file
            page_file = shelf_dir / f"{page_id}.md"
            page_file.write_text(content)

            # Track for book
            book_pages.append({
                "id": page_id,
                "title": page_title,
                "creator": creator.split('(')[0].strip() if '(' in creator else creator,
                "score": score
            })

            # Add to manifest
            manifest_pages.append({
                "id": page_id,
                "book_id": book_id,
                "title": page_title,
                "shelf": shelf_path,
                "creator": creator,
                "score": score,
                "tier": "A",
                "tags": tags,
                "links_to": [],
                "contradicts": None,
                "extracted_at": extracted_at
            })

            shelf_counters[shelf_path] += 1

        # Create book file
        book_file = LIB / "books" / f"{book_id}.md"
        book_file.parent.mkdir(parents=True, exist_ok=True)

        pages_list = "\n".join([f"- {p['id']}: {p['title']}" for p in book_pages])
        table = "\n".join([f"| {p['id']} | {p['title'][:50]} | {p['creator'][:20]} | {p['score']} |" for p in book_pages])

        book_content = f"""# Book: {title}
**Pages**: {len(book_pages)} | **Shelf**: {shelf_name} | **Updated**: 2026-03-19

## Page IDs
{pages_list}

## All Pages
| ID | Title | Creator | Score |
|----|-------|---------|-------|
{table}
"""
        book_file.write_text(book_content)

    # Update shelf.yaml files
    for shelf_path, count in shelf_counters.items():
        shelf_file = LIB / shelf_path / "shelf.yaml"
        if shelf_file.exists():
            with open(shelf_file) as f:
                shelf_data = yaml.safe_load(f)
            shelf_data['page_count'] = count
            with open(shelf_file, 'w') as f:
                yaml.dump(shelf_data, f, default_flow_style=False)
            print(f"Updated shelf: {shelf_path} -> {count} pages")

    # Update global manifest
    manifest_file = LIB / "_index" / "_manifest.yaml"
    manifest_data = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "pages": manifest_pages,
        "total_pages": len(manifest_pages),
        "by_shelf": {},
        "by_creator": {}
    }

    # Group by shelf
    for page in manifest_pages:
        shelf = page['shelf']
        if shelf not in manifest_data['by_shelf']:
            manifest_data['by_shelf'][shelf] = []
        manifest_data['by_shelf'][shelf].append(page['id'])

    with open(manifest_file, 'w') as f:
        yaml.dump(manifest_data, f, default_flow_style=False, sort_keys=False)

    print(f"\n=== Migration Complete ===")
    print(f"Total pages created: {len(manifest_pages)}")
    print(f"Total books created: {book_counter - 1}")
    print(f"Manifest updated: {manifest_file}")

if __name__ == "__main__":
    main()
