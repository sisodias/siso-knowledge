# Library Intelligence Review Inbox

Heartbeat drops integration opportunities here for review. Human (or agent) validates before any tasks get created.

## Format

Each JSON file is one integration opportunity:

```json
{
  "type": "integration_review",
  "source": "os_insights",
  "timestamp": "2026-03-20T22:44:36",
  "tier": "critical",
  "title": "Mcp Use",
  "source_detail": "GitHub or YouTube/Latent Space/etc",
  "components": "mcp, devops",
  "insight": "The research insight...",
  "url": "https://github.com/...",
  "status": "pending_review"
}
```

## Review Workflow

1. Read the JSON files in this inbox
2. For each, decide: **relevant to SISO OS** or **not relevant**?
3. If relevant → create a task in the System DB using siso-tasks.py, then delete or rename this file
4. If not relevant → delete the file

## Tiers

- **critical**: MCP tool frameworks, directly applicable to SISO OS
- **high**: Memory, agent OS patterns
- **medium**: Multi-agent orchestration, RAG

## Components

- `mcp` — MCP server/tool frameworks
- `memory` — Memory layer for agents
- `orchestration` — Multi-agent coordination
- `agent_os` — Agent OS patterns
- `rag` — Knowledge retrieval
- `evals` — Testing/quality
