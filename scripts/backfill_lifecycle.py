#!/usr/bin/env python3
"""
backfill_lifecycle.py — Apply lifecycle flags (archived / cold / pinned) to SISO Knowledge pages.

Spec §8 rules:
  - archived: true  if  (tier == 'C' AND score < 0.4)
                       OR (tier == 'C' AND extracted_at > 180d AND zero backlinks)
  - cold:     true  if  tier == 'C' AND extracted_at > 365d AND score < 0.2 AND zero backlinks
  - pinned:   false  (default; do NOT set to true here)

Requires backlinks.json from 1.C4.  Gracefully exits with warning if missing.

Dry-run by default; --apply writes changes via atomic temp-file swap.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Frontmatter parsing (python-frontmatter preferred, manual fallback)
# ---------------------------------------------------------------------------
try:
    import frontmatter

    HAS_FRONTMATTER = True
except ImportError:
    HAS_FRONTMATTER = False


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_content)."""
    if HAS_FRONTMATTER:
        post = frontmatter.loads(path.read_text(encoding="utf-8"))
        return dict(post), str(post)
    else:
        text = path.read_text(encoding="utf-8")
        m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            return {}, text
        fm_text = m.group(1)
        body = text[m.end() :]
        fm = {}
        for line in fm_text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"').strip("'")
        return fm, body


# ---------------------------------------------------------------------------
# Paths (relative to this file's location)
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
LIBRARY_ROOT = (SCRIPT_DIR / "..").resolve()               # SISO_Knowledge/
SECTIONS_DIR = LIBRARY_ROOT / "sections"
BACKLINKS_PATH = LIBRARY_ROOT / "_index" / "backlinks.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

TODAY = date.today()


def parse_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(value.strip("'\" "), fmt).date()
        except ValueError:
            pass
    return None


def days_old(d: date) -> int:
    return (TODAY - d).days


def backlink_count(page_id: str, backlinks: dict) -> int:
    """Return number of pages that link TO page_id."""
    return len(backlinks.get(page_id) or [])


def score_float(value) -> float:
    if value is None:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def atomic_write(path: Path, content: str) -> None:
    """Write via temp-file + rename for atomicity."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    with open(tmp, "r+b") as fh:
        os.fsync(fh.fileno())
    os.rename(tmp, path)


def walk_pages():
    """Yield (Path, frontmatter_dict) for every p_*.md under sections/."""
    for md_path in SECTIONS_DIR.rglob("p_*.md"):
        fm, _ = parse_frontmatter(md_path)
        yield md_path, fm


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def compute_flags(
    tier: str,
    score: float,
    extracted_at: Optional[date],
    bl_count: int,
) -> tuple[bool, bool]:
    """
    Returns (archived, cold) booleans per spec §8 rules.
    - archived: true  if  (tier C AND score < 0.4)  OR  (tier C AND age > 180d AND bl_count == 0)
    - cold:     true  if  tier C AND age > 365d AND score < 0.2 AND bl_count == 0
    """
    archived = False
    cold = False

    if tier == "C":
        age_days = days_old(extracted_at) if extracted_at else 9999

        if score < 0.4:
            archived = True
        elif age_days > 180 and bl_count == 0:
            archived = True

        if age_days > 365 and score < 0.2 and bl_count == 0:
            cold = True

    return archived, cold


def apply_page(md_path: Path, fm: dict, backlinks: dict, dry_run: bool) -> Optional[str]:
    """Apply lifecycle flags to a single page. Returns None if no change, else diff."""
    page_id = fm.get("id") or md_path.stem
    tier = str(fm.get("tier") or "").strip()
    score = score_float(fm.get("score"))
    extracted_at = parse_date(str(fm.get("extracted_at") or ""))
    bl_count = backlink_count(page_id, backlinks)

    archived, cold = compute_flags(tier, score, extracted_at, bl_count)

    current_archived = str(fm.get("archived") or "").lower() in ("true", "yes", "1")
    current_cold = str(fm.get("cold") or "").lower() in ("true", "yes", "1")

    # Default pinned to false (never set to true here)
    current_pinned_raw = fm.get("pinned")
    current_pinned = (
        str(current_pinned_raw).lower() in ("true", "yes", "1")
        if current_pinned_raw is not None
        else False
    )
    pinned = False  # spec: default false; this script never promotes to pinned

    if (
        archived == current_archived
        and cold == current_cold
        and pinned == current_pinned
    ):
        return None  # no change

    new_fm = dict(fm)
    new_fm["archived"] = "true" if archived else None
    new_fm["cold"] = "true" if cold else None
    new_fm["pinned"] = None  # never true from this script; clear if set by accident

    # Remove None-valued keys to keep frontmatter clean
    new_fm = {k: v for k, v in new_fm.items() if v is not None and v != "None"}

    diff = (
        f"  {md_path.relative_to(LIBRARY_ROOT)}\n"
        f"    tier={tier!r} score={score} age={days_old(extracted_at) if extracted_at else '?'}d "
        f"backlinks={bl_count}\n"
        f"    archived: {current_archived} → {archived}   cold: {current_cold} → {cold}"
    )

    if dry_run:
        return diff

    # Rebuild file with new frontmatter
    raw = md_path.read_text(encoding="utf-8")
    m = re.match(r"\A---\n.*?\n---\n", raw, re.DOTALL)
    if m:
        delim = m.group(0)
        body = raw[m.end() :]
        fm_lines = []
        for k, v in new_fm.items():
            if isinstance(v, list):
                v = json.dumps(v)
            fm_lines.append(f"{k}: {v}")
        fm_text = "\n".join(sorted(fm_lines))
        new_raw = f"---\n{fm_text}\n---\n{body}"
        atomic_write(md_path, new_raw)

    return diff


# ---------------------------------------------------------------------------
# Matrix reporting
# ---------------------------------------------------------------------------

def print_matrix(rows):
    """Print a summary table."""
    print(f"\n{'Page':<60} {'Tier':>4} {'Score':>6} {'Age(d)':>5} {'BL':>3} {'Archived':>8} {'Cold':>4}")
    print("-" * 100)
    for row in rows:
        print(
            f"{row['path']:<60} {row['tier']:>4} {row['score']!r:>6} "
            f"{row['age']:>5} {row['bl']:>3} {str(row['archived']):>8} {str(row['cold']):>4}"
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Backfill lifecycle flags (archived / cold / pinned).")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write changes (default is dry-run).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Cap number of pages processed (for sampling).",
    )
    args = parser.parse_args()

    dry_run = not args.apply
    mode_label = "DRY-RUN" if dry_run else "APPLY"

    # Load backlinks
    if BACKLINKS_PATH.exists():
        backlinks = json.loads(BACKLINKS_PATH.read_text(encoding="utf-8"))
        print(f"[{mode_label}] Loaded backlinks.json ({len(backlinks)} entries)", file=sys.stderr)
    else:
        backlinks = {}
        print(
            f"[{mode_label}] WARNING: backlinks.json not found at {BACKLINKS_PATH}. "
            "backlink counts will be 0. Run after 1.C4 completes for full accuracy.",
            file=sys.stderr,
        )

    # Scan pages
    changed = []
    matrix_rows = []

    for i, (md_path, fm) in enumerate(walk_pages()):
        if args.limit and i >= args.limit:
            break

        page_id = fm.get("id") or md_path.stem
        tier = str(fm.get("tier") or "").strip()
        score = score_float(fm.get("score"))
        extracted_at = parse_date(str(fm.get("extracted_at") or ""))
        bl_count = backlink_count(page_id, backlinks)
        archived, cold = compute_flags(tier, score, extracted_at, bl_count)

        rel_path = str(md_path.relative_to(LIBRARY_ROOT))
        matrix_rows.append(
            {
                "path": rel_path,
                "tier": tier,
                "score": f"{score:.2f}",
                "age": days_old(extracted_at) if extracted_at else -1,
                "bl": bl_count,
                "archived": archived,
                "cold": cold,
            }
        )

        diff = apply_page(md_path, fm, backlinks, dry_run)
        if diff:
            changed.append(diff)

    # Breakdown summary
    total = len(matrix_rows)
    archived_count = sum(1 for r in matrix_rows if r["archived"])
    cold_count = sum(1 for r in matrix_rows if r["cold"])

    print(f"\n[{mode_label}] Lifecycle Backfill — {total} pages scanned")
    print(f"  archived: {archived_count} ({100*archived_count/total:.1f}%)" if total else "  archived: 0 (n/a)")
    print(f"  cold:     {cold_count}     ({100*cold_count/total:.1f}%)" if total else "  cold:     0 (n/a)")
    print(f"  changed:  {len(changed)}")

    if changed:
        print(f"\n[{mode_label}] Changes:")
        for d in changed:
            print(d)

    if matrix_rows and (archived_count > 0 or cold_count > 0):
        print_matrix(matrix_rows[:50])  # show first 50 rows as sample

    if dry_run:
        print(f"\nNOTE: This was a dry run. Run with --apply to persist changes.")

    if args.apply:
        print(f"\n[{mode_label}] Done. {len(changed)} page(s) updated.")


if __name__ == "__main__":
    main()
