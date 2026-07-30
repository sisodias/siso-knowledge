# SISO Knowledge

## Boundary status (2026-07-30)

This is **SISO Knowledge**: the system that acquires, curates, stores, indexes, relates, and retrieves knowledge. The evidence and completed outer-boundary migration live in [`../docs/siso-library-boundary-audit-2026-07-30.html`](../docs/siso-library-boundary-audit-2026-07-30.html).

`SISO_Knowledge` is the canonical path. The former `SISO_Library` compatibility name is retired; historical documents may retain it, but operational routes may not. Do not add new deployable apps, general agent-platform modules, or UI design-system source here. Knowledge-specific feeder/curator agents remain part of acquisition and curation; reusable agent capabilities belong to `../SISO_Agents/`.

## Public Great Library registry

`../Great_Library_of_SISO/` is the independent workspace-root checkout for the public Great Library registry and website. Start with its `AGENTS.md`, then `CURRENT_STATE.md`. It indexes SISO Knowledge but is not owned or nested by this repository.

## Structure: Library → Section → Bookcase → Shelf → Book → Page

| Level | Example |
|-------|---------|
| Library | SISO_Knowledge/ |
| Section | sections/ai_research/ |
| Bookcase | sections/ai_research/bookcases/agents/ |
| Shelf | sections/ai_research/bookcases/agents/shelves/multi_agent/ |
| Book | sections/ai_research/bookcases/agents/shelves/multi_agent/books/b_XXX.md |
| Page | sections/ai_research/bookcases/agents/shelves/multi_agent/pages/p_XXX.md |

## Pages are the atomic unit
Every page is one insight. Books are manifests linking to pages.

## Index (_index/)
Auto-generated card catalog — never edit manually:
- `_manifest.yaml` — every page in the library
- `by_creator.json` — creator → pages mapping
- `by_topic.json` — topic → pages mapping
- `by_tag.json` — tag → pages mapping
- `graph.json` — wikilink graph for D3 visualization
- `search.sqlite` — FTS5 full-text search

## Rebuild
Run `python queries/rebuild_index.py` to regenerate all indexes from page files.

## Graph
Open `graph/index.html` in a browser to see the interactive knowledge graph.

## Pipelines
Knowledge flows: raw source → pipeline → pages → index → graph + queries
