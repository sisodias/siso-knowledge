# SISO_Knowledge Module Templates

Canonical definitions for every level of the library hierarchy. Instantiate these when creating new sections, bookcases, shelves, pages, or books.

## Levels

```
Section → Bookcase → Shelf → (Page | Book)
```

| Level | Template | Description |
|-------|----------|-------------|
| Section | `section/` | Top-level domain (e.g. ai_research) |
| Bookcase | `bookcase/` | Thematic grouping within a section |
| Shelf | `shelf/` | Topic-specific unit with pages and books |
| Page | `page/` | Atomic insight — one idea per page |
| Book | `book/` | Manifest of related pages |

## Usage

```bash
# Create a new section
cp -r module_templates/section sections/<section_name>

# Create a new bookcase
cp -r module_templates/bookcase sections/<section_name>/bookcases/<bookcase_name>

# Create a new shelf
cp -r module_templates/shelf sections/<section_name>/bookcases/<bookcase_name>/shelves/<shelf_name>
```

## Schema

- `*.yaml` — machine-readable schema (pipeline-readable)
- `_index.md` — human-readable overview
- `PAGE_TEMPLATE.md` / `BOOK_TEMPLATE.md` — content format

## Rules

1. Every level needs `*.yaml` + `_index.md` before it can accept content
2. Pages are created by `queries/add_book.py` — never by hand
3. Books are auto-generated from shelf page sets — never by hand
4. Never edit generated files (manifests, indexes, graph) — rebuild from source
