#!/bin/bash
# Run daily digest and notification pipeline
# Usage: ./pipelines/run_daily.sh [--dry-run]

DRY_RUN=""
if [ "$1" = "--dry-run" ]; then
    DRY_RUN="--dry-run"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Running Daily Digest ==="
python3 pipelines/digest.py $DRY_RUN

echo ""
echo "=== Running Agent Notifications ==="
python3 pipelines/notify.py $DRY_RUN

echo ""
echo "=== Done ==="
