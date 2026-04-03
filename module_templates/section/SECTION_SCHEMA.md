# Schema: Section

## Purpose
Top-level domain grouping. Examples: `ai_research`, `ecosystem`, `infrastructure`, `product`.

## YAML Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Must be `"section"` |
| `name` | string | yes | Display name |
| `slug` | string | yes | URL-safe ID (matches directory name) |
| `description` | string | yes | 1-2 sentences |
| `icon` | string | no | Emoji or icon |
| `color` | string | no | Hex color for graph |
| `order` | integer | no | Sidebar sort order |
| `bookcases` | list | yes | List of bookcase slugs |
| `owner` | string | yes | Agent that owns this section |
| `version` | string | yes | Schema version |

## File Structure

```
sections/
└── {slug}/
    ├── _index.md
    ├── section.yaml
    └── bookcases/
        └── {bookcase_slug}/
```

## Graph Color Reference

| Section | Color |
|---------|-------|
| ai_research | `#4285F4` |
| ecosystem | `#FB9900` |
| infrastructure | `#34A853` |
| product | `#9C27B0` |
