# Agent — RedditQueueAnalysis

## Quick Start
1. Read `identity.yaml` to initialize persona
2. Check `inbox/` for pending tasks
3. Run `workspace/scraper_runner.py` to fetch and ingest

## Library Context
This agent lives at `SISO_Library/agents/RedditQueueAnalysis/` and feeds the SISO_Library pipeline.
Owned by **LIBRARY_PM**.

## Pipeline
- Scrapes subreddits: LocalLLaMA, MachineLearning, AIagents, SideProject, artificial, technews
- Writes JSONL to `pipelines/reddit/inbox/`
- Runs `pipelines/reddit/ingest.py` to add to library

## Memory
Uses file-based memory in `memory/` directory.

## Status
Check `memory/` for current state
