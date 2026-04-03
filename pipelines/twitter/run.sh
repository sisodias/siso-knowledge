#!/bin/bash
# Twitter pipeline runner
# Usage: ./run.sh [--dry-run] [--limit N]

cd "$(dirname "$0")"

DRY_RUN=""
LIMIT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        --limit)
            LIMIT="--limit $2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

python3 ingest.py $DRY_RUN $LIMIT
