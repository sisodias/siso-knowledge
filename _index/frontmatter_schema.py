"""Frontmatter schema for SISO Library page documents.

Spec §4 — all existing + new fields. Dataclass for type-safe objects,
no external deps beyond the stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal, Optional


@dataclass
class RevisionEntry:
    """Single entry in the append-only revisions log."""
    at: str
    hash: str
    diff_summary: str


@dataclass
class Page:
    """Full frontmatter schema for a SISO Library page.

    All fields have sensible defaults — nullable on existing pages,
    populated on new ingests.
    """

    # ── Identity ────────────────────────────────────────────────────────────
    id: str = ""
    slug: Optional[str] = None
    book_id: Optional[str] = None

    # ── Content ─────────────────────────────────────────────────────────────
    title: Optional[str] = None
    shelf: Optional[str] = None
    creator: Optional[str] = None
    source_video: Optional[str] = None
    source_id: Optional[str] = None

    # ── Scoring ─────────────────────────────────────────────────────────────
    score: float = 7.0
    tier: Literal["A", "B", "C"] = "B"

    # ── Classification ─────────────────────────────────────────────────────
    tags: list[str] = field(default_factory=list)
    links_to: list[str] = field(default_factory=list)
    contradicts: Optional[str] = None

    # ── Extraction metadata ─────────────────────────────────────────────────
    extracted_at: Optional[str] = None
    first_extracted_at: Optional[str] = None

    # ── Versioning / dedup ───────────────────────────────────────────────────
    content_hash: Optional[str] = None
    version: int = 1
    supersedes: Optional[str] = None
    superseded_by: Optional[str] = None
    revisions: list[RevisionEntry] = field(default_factory=list)

    # ── Hub promotion ────────────────────────────────────────────────────────
    hub: bool = False
    hub_category: Optional[str] = None
    hub_featured: bool = False

    # ── Lifecycle flags ─────────────────────────────────────────────────────
    archived: bool = False
    cold: bool = False
    pinned: bool = False

    # ── Visuals ─────────────────────────────────────────────────────────────
    og_image: Optional[str] = None

    # ── Internal (populated at parse time, not from frontmatter) ─────────────
    content: str = ""
    _file: str = ""
