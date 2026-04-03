# LIBRARY_PM — Chief Librarian

## Quick Start
1. Read `identity.yaml` to initialize persona
2. Check `inbox/` for pending tasks
3. Review `memory/journal.md` for last known state
4. Execute pipeline tasks via `pipelines/shared/run.sh` or individual scripts

## Library Location
`/Users/shaansisodia/SISO_Workspace/SISO_Library/`

## Pipeline Scripts
- `pipelines/youtube/ingest.py` — ingest new YouTube extractions
- `pipelines/github/ingest.py` — ingest new GitHub research
- `pipelines/youtube/concept_linker.py` — add concept edges to graph
- `queries/rebuild_index.py` — rebuild all indexes
- `pipelines/shared/run.sh` — full pipeline (all of the above)

## Key Commands
```bash
# Run full pipeline
./pipelines/shared/run.sh

# Check graph health
python3 -c "import json; d=json.load(open('_index/graph.json')); print(f'nodes={len(d[\"nodes\"])}, edges={len(d[\"edges\"])}')"

# Open graph visualization
open graph/index.html
```

## Memory
File-based memory in `memory/` directory. Update after every pipeline run.

## Operational Rules
- Run concept_linker after every ingest batch
- Rebuild indexes after every concept_linker run
- Log pipeline runs in `memory/journal.md`
- Check empty shelves list in `memory/` before assigning tasks
