# Hooks

Bash scripts that run before/after Claude actions.

## Available Hooks

| Hook | When |
|------|------|
| pre-tool-use | Before a tool is executed |
| post-tool-use | After a tool executes |
| pre-command | Before a bash command |
| Stop | On conversation stop |
| Context | On context update |

## Format

```bash
#!/bin/bash
# Hook script
# Access $CLAUDE_DIR, $USER_DIR, etc.
```

## Examples

- Auto-lint after file writes
- Copy to inbox after completion
- Update memory on stop
