# Agent — WebQueueAnalysis

## Quick Start
1. Read `identity.yaml` to initialize persona
2. Check `inbox/` for pending search tasks
3. Execute searches via `workspace/search_runner.py`
4. Results go to `pipelines/web/inbox/`

## Pipeline
- Agent workspace: `agents/WebQueueAnalysis/workspace/`
- Pipeline inbox: `pipelines/web/inbox/`
- Ingest: `pipelines/web/ingest.py`

## Usage
```bash
# Run inbox tasks
python3 agents/WebQueueAnalysis/workspace/search_runner.py

# Run specific query
python3 agents/WebQueueAnalysis/workspace/search_runner.py --query "AI agents 2026"

# Run batch + ingest
python3 agents/WebQueueAnalysis/workspace/search_runner.py --batch --ingest
```
