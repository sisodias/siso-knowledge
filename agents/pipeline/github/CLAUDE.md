# Agent — GitHubQueueAnalysis

## Quick Start
1. Read `identity.yaml` to initialize persona
2. Check `inbox/` for pending tasks
3. Review `memory/` for last known state
4. Execute research tasks in `workspace/`

## Library Context
This agent lives at `SISO_Knowledge/agents/GitHubQueueAnalysis/` and feeds the SISO_Knowledge pipeline.
Owned by **LIBRARY_PM**.

## Memory
Uses file-based memory in `memory/` directory.

## Operational Rules
- Update `memory/` after every research batch
- Reference `.claude/rules/` before file modifications
- Use JSONL format in inbox/outbox for atomic operations

## SISO_Knowledge Pipeline Integration

After completing research on a repo, write structured JSONL to the library pipeline inbox:

```bash
echo '{"repo":"owner/name","url":"https://github.com/owner/name","title":"Repo Name","description":"...","research":"...","stars":"12345"}' \
  >> /Users/shaansisodia/SISO_Workspace/SISO_Knowledge/pipelines/github/inbox/research.jsonl
```

Each JSONL line should contain: `repo`, `url`, `title`, `description`, `research`, `stars`.

The SISO_Knowledge pipeline (`pipelines/github/ingest.py`) picks up these entries every 4 hours.

## Status
Check `memory/` for current state
