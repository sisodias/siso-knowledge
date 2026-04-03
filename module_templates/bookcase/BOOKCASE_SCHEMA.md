# Schema: Bookcase

## Purpose
Thematic grouping within a section. Examples: `agents`, `llms`, `rag` within `ai_research`.

## YAML Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Must be `"bookcase"` |
| `name` | string | yes | Display name |
| `slug` | string | yes | URL-safe ID |
| `section` | string | yes | Parent section slug |
| `description` | string | yes | 1-2 sentences |
| `shelves` | list | yes | List of shelf slugs |
| `auto_tags` | list | no | Tags auto-applied to all pages |
| `owner` | string | yes | Agent that owns this bookcase |
| `version` | string | yes | Schema version |

## File Structure

```
sections/{section}/bookcases/{slug}/
├── _index.md
├── bookcase.yaml
└── shelves/
    └── {shelf_slug}/
```
