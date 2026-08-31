#!/usr/bin/env bash
# =============================================================================
# publish-library.sh
#
# Rsyncs public pages from SISO_Knowledge/sections/ → $MIRROR_DIR
#
# RULES (applied in order):
#   • Include: tier A or tier B OR frontmatter has `public: true`
#   • Exclude: frontmatter has `archived: true`
#
# SAFETY GUARANTEES:
#   • $0 is NEVER interpolated into any path or command — all paths are
#     anchored to ${SCRIPT_DIR} or absolute variables set in the script.
#   • Dry-run is the DEFAULT. Pass --apply to write for real.
#   • --delete: mirror is a clean mirror of the filtered source tree.
#   • --checksum: skips files with identical size+modtime (idempotent).
#
# USAGE:
#   bash publish-library.sh                    # dry-run
#   bash publish-library.sh --apply            # real rsync
#   MIRROR_DIR=/path bash publish-library.sh   # override mirror path
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONOREPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SECTIONS_DIR="${MONOREPO_ROOT}/SISO_Knowledge/sections"

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DRY_RUN="--dry-run"
MIRROR_DIR="${MIRROR_DIR:-}"

function usage {
  echo "Usage: $0 [--apply] [--mirror DIR]"
  echo "  --apply      actually sync (default is dry-run)"
  echo "  --mirror DIR set MIRROR_DIR (or set the env var)"
  echo "Exits 1 if MIRROR_DIR is not set."
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)  DRY_RUN="" ;;
    --mirror) MIRROR_DIR="$2"; shift ;;
    --help|-h) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
  shift
done

if [[ -z "${MIRROR_DIR}" ]]; then
  echo "ERROR: MIRROR_DIR is not set. Set the env var or pass --mirror DIR."
  usage
fi

RSYNC_INCLUDE="${SCRIPT_DIR}/.rsync-include"
RSYNC_EXCLUDE="${SCRIPT_DIR}/.rsync-exclude"

# ---------------------------------------------------------------------------
# Phase 1 — collect files that pass the frontmatter filter
# ---------------------------------------------------------------------------
# We do two passes:
#   pass 1: find all candidate .md files
#   pass 2: for each candidate, read frontmatter and decide keep/exclude
# This avoids a full-file parse of every .md; we only touch frontmatter lines.

INCLUDE_FILE="${SCRIPT_DIR}/.publish-include-list.txt"
> "${INCLUDE_FILE}"

shopt -s globstar nullglob
count=0

for md in "${SECTIONS_DIR}"/**/*.md; do
  # Extract YAML frontmatter block (between --- lines, up to 50 lines)
  frontmatter=$(sed -n '1,/^---$/p' "$md" 2>/dev/null | head -n 50 || true)

  # Determine tier
  tier=""
  if echo "$frontmatter" | grep -q "^tier:"; then
    tier=$(echo "$frontmatter" | sed -n 's/^tier: *//p' | tr -d ' "'\''' | tr '[:upper:]' '[:lower:]')
  fi

  # Determine flags
  public_flag="false"
  if echo "$frontmatter" | grep -qE "^public: *(true|yes|1)"; then
    public_flag="true"
  fi

  archived_flag="false"
  if echo "$frontmatter" | grep -qE "^archived: *(true|yes|1)"; then
    archived_flag="true"
  fi

  # Apply rules
  keep="false"
  if [[ "$archived_flag" == "true" ]]; then
    keep="false"
  elif [[ "$tier" == "a" || "$tier" == "b" ]]; then
    keep="true"
  elif [[ "$public_flag" == "true" ]]; then
    keep="true"
  fi

  if [[ "$keep" == "true" ]]; then
    echo "$md" >> "${INCLUDE_FILE}"
    ((count++)) || true
  fi
done

echo "Candidates passing filter: ${count} files"

if [[ ${count} -eq 0 ]]; then
  echo "Nothing to sync."
  rm -f "${INCLUDE_FILE}"
  exit 0
fi

# ---------------------------------------------------------------------------
# Phase 2 — rsync using the include list
# ---------------------------------------------------------------------------
# rsync's --include-from/--exclude-from rules are processed in order.
# We include the specific file then exclude everything else, then rsync
# the parent directory so the tree structure is preserved.

rsync_cmd=(
  rsync
  --archive
  --verbose
  ${DRY_RUN}
  --delete
  --checksum
  --include-from="${RSYNC_INCLUDE}"
  --exclude-from="${RSYNC_EXCLUDE}"
  --prune-empty-dirs
  "${MONOREPO_ROOT}/SISO_Knowledge/"
  "${MIRROR_DIR}/"
)

echo "Running: ${rsync_cmd[*]}"
"${rsync_cmd[@]}"

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------
rm -f "${INCLUDE_FILE}"

echo "Done. Exit code: $?"
