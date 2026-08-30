#!/bin/bash
# Reddit Pipeline Runner
# Usage: ./run.sh [--scrape-only|--ingest-only]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="/Users/shaansisodia/SISO_Workspace/SISO_Knowledge"

cd "$ROOT"

SCRAPE_ONLY=false
INGEST_ONLY=false

for arg in "$@"; do
    case $arg in
        --scrape-only)
            SCRAPE_ONLY=true
            ;;
        --ingest-only)
            INGEST_ONLY=true
            ;;
    esac
done

echo "=== Reddit Pipeline ==="

if [ "$INGEST_ONLY" = false ]; then
    echo "[1/2] Scraping Reddit..."
    python3 "$SCRIPT_DIR/scraper.py" "$@"
fi

if [ "$SCRAPE_ONLY" = false ]; then
    echo "[2/2] Ingesting to Library..."
    python3 "$SCRIPT_DIR/ingest.py"
fi

echo "Done!"
