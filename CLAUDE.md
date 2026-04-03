# SISO Library — Knowledge Base

## Structure: Library → Section → Bookcase → Shelf → Book → Page

| Level | Example |
|-------|---------|
| Library | SISO_Library/ |
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
