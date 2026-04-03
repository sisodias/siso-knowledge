#!/bin/bash
# Web pipeline runner - scrape web for AI research, then ingest to library
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== Web Pipeline ==="

# Step 1: Scrape web for new content
echo "Step 1: Scraping web..."
python3 "$SCRIPT_DIR/scraper.py" --batch

# Step 2: Ingest to library
echo "Step 2: Ingesting to library..."
python3 "$SCRIPT_DIR/ingest.py"

echo "=== Done ==="
