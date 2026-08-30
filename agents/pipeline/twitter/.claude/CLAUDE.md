# .claude/CLAUDE.md — Agent Engine Config

This folder contains Claude Code native configurations.

## Structure

| Folder | Purpose |
|--------|---------|
| `settings.json` | Tool permissions, env vars |
| `rules/` | Behavioral constraints (loaded on boot) |
| `skills/` | Reusable task recipes (loaded on demand) |
| `commands/` | Custom slash commands |
| `agents/` | Subagent definitions |
| `hooks/` | Automation scripts |

## Skills

This agent uses the xsearch skill from `~/SISO_Knowledge/agents/YouTubeQueueAnalysis/.claude/skills/xsearch/`.
