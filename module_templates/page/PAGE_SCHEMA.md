# Schema: Page

## Purpose
Atomic insight — one idea per page. The fundamental unit of the library.

## YAML Frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Auto: `p_XXX` |
| `book_id` | string | yes | Auto: `b_XXX` |
| `shelf` | string | yes | section/bookcase/shelf |
| `title` | string | yes | Atomic insight, max 200 chars |
| `creator` | string | yes | Content source |
| `source_video` | string | yes | YouTube ID, GitHub URL, or `"web"` |
| `score` | float | yes | 0.0–10.0 |
| `tier` | enum | yes | `A` \| `B` \| `C` |
| `tags` | list | yes | Auto-inferred + manual |
| `links_to` | list | no | Related page IDs |
| `contradicts` | string | no | Contradicting page ID |
| `extracted_at` | date | yes | ISO date |
| `ingested_by` | string | yes | Ingesting agent |
| `quality_notes` | string | no | Curator notes |

## Scoring

| Score | Tier | Meaning |
|-------|------|---------|
| 8.0–10.0 | A | Foundational, high-value |
| 5.0–7.9 | B | Useful, moderate |
| 0.0–4.9 | C | Minor, edge cases |

## Rules
1. One insight per page — never combine ideas
2. Title is a statement, not a question
3. Body is 50–500 words
4. Created by `queries/add_book.py`, never by hand
5. `links_to` populated by `concept_linker.py`
