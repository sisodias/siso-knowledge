"""FTS5 full-text search index builder for SISO Library.

Schema: pages virtual table with porter unicode61 tokenizer.
Skips pages with cold: true.
"""
import sqlite3
from pathlib import Path

INDEX_PATH = Path(__file__).parent


def build_fts_index(pages: list) -> None:
    """Build FTS5 search index from pages.

    Schema: CREATE VIRTUAL TABLE pages USING fts5(
        id UNINDEXED, slug UNINDEXED, title, creator, tags, body,
        tier UNINDEXED, score UNINDEXED, tokenize='porter unicode61'
    )
    Skips pages where cold: true.
    """
    db_path = INDEX_PATH / "search.sqlite"
    conn = sqlite3.connect(str(db_path))

    # Drop existing FTS table and recreate with correct schema
    conn.execute("DROP TABLE IF EXISTS pages")
    conn.execute("""
        CREATE VIRTUAL TABLE pages USING fts5(
            id UNINDEXED,
            slug UNINDEXED,
            title,
            creator,
            tags,
            body,
            tier UNINDEXED,
            score UNINDEXED,
            tokenize='porter unicode61'
        )
    """)

    inserted = 0
    for page in pages:
        # Skip cold pages
        if page.get("cold", False):
            continue

        # Join tags into comma-separated string for FTS
        tags_str = ",".join(page.get("tags", []) or [])

        conn.execute(
            """
            INSERT INTO pages (id, slug, title, creator, tags, body, tier, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                page.get("id", ""),
                page.get("slug", ""),
                page.get("title", ""),
                page.get("creator", ""),
                tags_str,
                page.get("content", ""),
                page.get("tier", ""),
                page.get("score", 0),
            ),
        )
        inserted += 1

    conn.commit()
    conn.close()
    print(f"FTS index built: {inserted} pages indexed")


if __name__ == "__main__":
    # Allow standalone testing
    import sys

    sys.path.insert(0, str(INDEX_PATH.parent))
    from build_index import scan_pages

    pages = scan_pages()
    print(f"Scanned {len(pages)} pages")
    build_fts_index(pages)
