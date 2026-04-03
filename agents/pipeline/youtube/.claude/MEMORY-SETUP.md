# Claude Mem Lite Setup

Multi-layer memory architecture for Agent OS.

## The 4 Memory Layers

| Layer | Path | Purpose |
|-------|------|---------|
| **Global** | `~/.claude-mem-lite/` | Cross-project wisdom |
| **Agent** | `{agent}/.claude/memory/` | This agent's brain |
| **Project** | `{project}/.claude/memory/` | Project-specific memory |
| **Task** | `{project}/.claude/memory/task.db` | Current task scratchpad |

## Setup for Agent

### 1. Install Dependencies

```bash
# In agent folder
npm install better-sqlite3
```

### 2. Configure Environment

Already set in `settings.json`:
```json
{
  "env": {
    "CLAUDE_MEM_DIR": "${agent_dir}/.claude/memory"
  }
}
```

### 3. Copy Hooks

```bash
cp /path/to/claude-mem-lite/hooks/hooks.json .claude/hooks/
```

## Database Location

After setup, the DB goes in:
```
.claude/memory/
├── journal.md
├── brain.md
├── goals.md
├── state.json
├── MEMORY.md
└── {agent-name}.db    ← Agent's memory DB
```

## Project Memory (When Agent Works on Project)

When agent `cd`s into a project:
```bash
export CLAUDE_MEM_DIR="$PROJECT_DIR/.claude/memory"
```

## Task Memory

For current task scratchpad:
- Location: `{project}/.claude/memory/task.db`
- Cleared on: git commit (via hook)
