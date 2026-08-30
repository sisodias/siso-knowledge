#!/usr/bin/env python3
"""
SISO OS Integration Analyzer — scan library for patterns relevant to SISO OS architecture.

Reads pages from the library, finds GitHub repos and insights relevant to:
- Memory / context management
- Tool use / MCP
- Multi-agent orchestration
- Planning / reasoning
- Agent OS patterns
- Infrastructure (inference, serving)

Outputs integration opportunities to workspace/os_integrations.md

Usage:
    python3 heartbeat/os_insights.py
    python3 heartbeat/os_insights.py --limit 50
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
OUTPUT = ROOT / "agents" / "YouTubeQueueAnalysis" / "workspace" / "os_integrations.md"
PIPELINE_DIR = ROOT / "pipelines" / "shared"

# SISO OS relevant keywords per component
RELEVANCE_MAP = {
    "memory": ["mem0", "memgpt", "memory", "context", "persistent", "long-term", "short-term", "episodic"],
    "mcp": ["mcp", "model context protocol", "tool use", "tool calling", "server", "stdio"],
    "orchestration": ["orchestrat", "multi-agent", "planner", "coordinator", "delegat", "swarm", "crew"],
    "planning": ["planner", "planning", "goal", "task decomposition", "subtask", "hierarchical"],
    "inference": ["vllm", "ollama", "lmstudio", "inference", "serving", "quantization", "tgi"],
    "agent_os": ["agent os", "autonomous", "24/7", "persistent agent", "long-running", "daemon"],
    "rag": ["rag", "retrieval", "vector", "embeddings", "pinecone", "weaviate", "chroma"],
    "evals": ["eval", "benchmark", "test", "quality", "coverage"],
    "devops": ["ci_cd", "github actions", "deploy", "kubernetes", "docker", "helm"],
}

# Integration opportunity tiers
TIER_PATTERNS = {
    "critical": ["mcp", "tool use", "tool calling"],
    "high": ["memory", "persistent", "24/7", "agent os", "autonomous"],
    "medium": ["multi-agent", "orchestrat", "planner", "rag", "retrieval"],
    "low": ["eval", "benchmark", "ci_cd", "deploy"],
}


def scan_pages(limit: int = 0) -> list[dict]:
    """Scan pages, return relevant ones with metadata."""
    pages = []
    sections_dir = ROOT / "sections"

    for page_file in sections_dir.rglob("p_*.md"):
        if page_file.name in ["shelf.yaml", "bookcase.yaml", "_index.md"]:
            continue

        try:
            content = page_file.read_text()
        except:
            continue

        # Parse frontmatter
        if not content.startswith("---"):
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue

        try:
            import yaml
            fm = yaml.safe_load(parts[1]) or {}
        except:
            continue

        body = parts[2].strip()

        page = {
            "id": fm.get("id", page_file.stem),
            "title": fm.get("title", ""),
            "shelf": fm.get("shelf", ""),
            "creator": fm.get("creator", "Unknown"),
            "tier": fm.get("tier", "C"),
            "tags": fm.get("tags", []),
            "source": fm.get("source_video", ""),
            "content": body,
            "file": str(page_file.relative_to(ROOT)),
        }

        # Extract research content (between Research: and ---)
        research = ""
        research_match = re.search(r"\*\*Research:\*\*\s*(.+?)(?=\n---|\n\*\*Why)", parts[2], re.DOTALL)
        if research_match:
            research = research_match.group(1).strip()
        page["research"] = research

        pages.append(page)
        if limit > 0 and len(pages) >= limit:
            break

    return pages


def score_relevance(page: dict) -> dict:
    """Score a page for OS relevance. Returns dict of component -> score."""
    text = (
        page.get("title", "") + " " +
        page.get("research", "") + " " +
        page.get("content", "") + " " +
        " ".join(page.get("tags", []))
    ).lower()

    scores = {}
    for component, keywords in RELEVANCE_MAP.items():
        score = 0
        matched = []
        for kw in keywords:
            if kw.lower() in text:
                score += 1
                matched.append(kw)
        if score > 0:
            scores[component] = {"score": score, "matched": matched}

    return scores


def classify_opportunity(page: dict, relevance: dict) -> str:
    """Classify integration opportunity tier."""
    content = (page.get("research", "") + page.get("content", "")).lower()

    for tier, patterns in TIER_PATTERNS.items():
        for p in patterns:
            if p.lower() in content:
                return tier

    if relevance:
        return "low"
    return "skip"


def extract_integration_insight(page: dict) -> str:
    """Extract the key integration insight from a page."""
    research = page.get("research", "")
    if research:
        # Take first 300 chars of research as the insight
        return research[:300].strip() + ("..." if len(research) > 300 else "")

    # Fall back to content
    body = page.get("content", "")
    lines = [l.strip() for l in body.split("\n") if len(l.strip()) > 30]
    return " ".join(lines[:3])[:300]


def main():
    ap = argparse.ArgumentParser(description="Analyze library for SISO OS integration opportunities")
    ap.add_argument("--limit", type=int, default=0, help="Limit pages to scan (0=all)")
    ap.add_argument("--tier", type=str, default="critical,high,medium", help="Filter by opportunity tier")
    ap.add_argument("--output", type=str, default=str(OUTPUT), help="Output file")
    args = ap.parse_args()

    print(f"=== SISO OS Integration Analyzer ===")
    print(f"Scanning library...")

    pages = scan_pages(args.limit)
    print(f"Scanned {len(pages)} pages")

    # Score all pages
    opportunities = []
    for page in pages:
        relevance = score_relevance(page)
        if not relevance:
            continue

        tier = classify_opportunity(page, relevance)
        if tier == "skip":
            continue

        allowed = args.tier.split(",")
        if tier not in allowed:
            continue

        insight = extract_integration_insight(page)

        opportunities.append({
            **page,
            "relevance": relevance,
            "tier": tier,
            "insight": insight,
            "components": list(relevance.keys()),
        })

    # Sort by tier then by shelf
    tier_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    opportunities.sort(key=lambda x: (tier_order.get(x["tier"], 9), x["shelf"]))

    # Group by component
    by_component = defaultdict(list)
    for opp in opportunities:
        for comp in opp["components"]:
            by_component[comp].append(opp)

    # Generate output
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    output_lines = [
        f"# SISO OS Integration Opportunities",
        f"",
        f"Generated: {now} | Pages scanned: {len(pages)} | Opportunities found: {len(opportunities)}",
        f"",
        f"---",
        f"",
    ]

    for tier in ["critical", "high", "medium", "low"]:
        tier_opps = [o for o in opportunities if o["tier"] == tier]
        if not tier_opps:
            continue

        output_lines.append(f"## {tier.upper()} Priority Integrations ({len(tier_opps)})")
        output_lines.append("")

        for opp in tier_opps:
            source_label = "GitHub" if "github.com" in opp.get("source", "") else opp.get("creator", "Unknown")
            insight = opp["insight"].replace("\n", " ").strip()

            output_lines.append(f"### {opp['title']}")
            output_lines.append(f"**Tier**: {opp['tier']} | **Source**: {source_label} | **Shelf**: `{opp['shelf']}`")
            output_lines.append(f"**Components**: {', '.join(opp['components'])}")
            output_lines.append(f"**Insight**: {insight}")
            output_lines.append(f"**Tags**: {', '.join(opp.get('tags', []))}")
            if opp.get("source"):
                output_lines.append(f"**URL**: {opp['source']}")
            output_lines.append("")

    # Component summary
    output_lines.append("---")
    output_lines.append("")
    output_lines.append("## Component Summary")
    output_lines.append("")
    for comp in sorted(by_component.keys()):
        opps = by_component[comp]
        tier_counts = defaultdict(int)
        for o in opps:
            tier_counts[o["tier"]] += 1
        tiers = ", ".join(f"{t}:{c}" for t, c in sorted(tier_counts.items()))
        output_lines.append(f"- **{comp}**: {len(opps)} opportunities [{tiers}]")

    output_lines.append("")
    output_lines.append("---")
    output_lines.append(f"*Generated by os_insights.py | Source: SISO_Knowledge ({len(pages)} pages)*")

    output = "\n".join(output_lines)
    Path(args.output).write_text(output)

    print(f"\n=== Results ===")
    print(f"Opportunities found: {len(opportunities)}")
    for tier in ["critical", "high", "medium", "low"]:
        count = len([o for o in opportunities if o["tier"] == tier])
        if count:
            print(f"  {tier.upper()}: {count}")

    print(f"\nWritten: {args.output}")

    # Also show top opportunities
    print(f"\n=== Top 10 ===")
    for opp in opportunities[:10]:
        print(f"  [{opp['tier']}] {opp['title'][:60]} ({opp['creator']})")


if __name__ == "__main__":
    main()
