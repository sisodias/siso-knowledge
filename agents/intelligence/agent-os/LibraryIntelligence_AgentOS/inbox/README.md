# Agent OS Intelligence — Research Review Inbox

Heartbeat drops SISO OS integration opportunities here for review. Agent (or human) validates before any tasks get created.

## What belongs here

Research on topics relevant to SISO Agent OS:
- MCP tool frameworks and server implementations
- Memory layers (mem0, memgpt, persistent context)
- Multi-agent orchestration (swarm, crew, planner)
- Tool use and tool calling patterns
- Inference serving (vllm, ollama, lmstudio)
- Agent OS patterns (autonomous, 24/7, long-running)
- RAG and retrieval systems
- Evals and benchmarks for agents
- DevOps/CI-CD for agent deployments

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
  "status": "pending_review",
  "routed_to": "agent_os"
}
```

## Review Workflow

1. Read the JSON files in this inbox
2. For each, decide: **relevant to SISO Agent OS** or **not relevant**?
3. If relevant → create a feature spec in `workspace/`, then delete or rename this file
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
- `devops` — Deployment/ops
- `inference` — Model serving
- `planning` — Task decomposition
