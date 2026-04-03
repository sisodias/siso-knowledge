# Skills

Reusable task recipes. Claude loads these on-demand when needed.

## Pre-configured Skills

| Skill | Description |
|-------|-------------|
| gitsearch | Search GitHub for code, repos, issues, and PRs |
| websearch | Search the web using Perplexity Sonar via OpenRouter |
| xsearch | Search X (Twitter) for discussions and trends |
| multisearch | Run web, GitHub, and X searches in parallel |

## Adding More Skills

Add skill definitions as markdown files:
- `skill-name/SKILL.md` — Full skill definition

## Format

```yaml
---
name: skill_name
description: What the skill does
user-invocable: true
context: fork
agent: Explore
allowed-tools: Bash, Read
---

# Skill Name

$ARGUMENTS

## Your Task
...
```
