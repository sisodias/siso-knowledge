# Agent — YouTubeQueueAnalysis

## Quick Start
1. Read `identity.yaml` to initialize persona
2. Check `inbox/` for pending tasks
3. Review `memory/` for last known state
4. Execute extraction tasks in `workspace/`

## Library Context
This agent lives at `SISO_Knowledge/agents/YouTubeQueueAnalysis/` and feeds the SISO_Knowledge pipeline.
Owned by **LIBRARY_PM**.

## Memory
Uses file-based memory in `memory/` directory.

## Operational Rules
- Update `memory/` after every extraction batch
- Reference `.claude/rules/` before file modifications
- Use JSONL format in inbox/outbox for atomic operations

## Pipeline Output
Extractions go to `/tmp/youtube-ai-research/extracted/by_date/` — picked up by `pipelines/youtube/ingest.py`

## Status
Check `memory/` for current state
