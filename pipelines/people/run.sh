#!/bin/bash
set -e
cd "$(dirname "$0")/.."

echo "=== People Pipeline ==="

echo "1. Scraping Twitter for leaderboard handles..."
python3 pipelines/people/scraper.py

echo ""
echo "2. Ingesting insights to topic shelves..."
python3 pipelines/people/ingest.py

echo ""
echo "3. Scoring and updating tiers..."
python3 pipelines/people/scorer.py

echo ""
echo "4. Building profile pages..."
python3 pipelines/people/profile_builder.py

echo ""
echo "5. Rebuilding search index..."
python3 queries/rebuild_index.py

echo ""
echo "=== People Pipeline Complete ==="
