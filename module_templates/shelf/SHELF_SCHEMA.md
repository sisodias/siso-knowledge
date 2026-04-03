# Schema: Shelf

## Purpose
Topic-specific unit containing pages and books. Routing target — pages land here based on keyword matching.

## YAML Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Must be `"shelf"` |
| `name` | string | yes | Display name |
| `slug` | string | yes | URL-safe ID |
| `bookcase` | string | yes | Parent bookcase slug |
| `section` | string | yes | Parent section slug |
| `description` | string | yes | 1-2 sentences |
| `content_type` | enum | yes | `insights` \| `reference` \| `case_studies` \| `tutorials` |
| `routing_keywords` | list | yes | Keywords that route content here |
| `tier_targets` | dict | no | Desired tier distribution {A, B, C} |
| `score_range` | dict | no | Min/max score for auto-tiering |
| `owner` | string | yes | Agent that owns this shelf |
| `version` | string | yes | Schema version |

## File Structure

```
sections/{section}/bookcases/{bookcase}/shelves/{slug}/
├── _index.md
├── shelf.yaml
├── pages/
│   └── p_XXX.md
└── books/
    └── b_XXX.md
```
