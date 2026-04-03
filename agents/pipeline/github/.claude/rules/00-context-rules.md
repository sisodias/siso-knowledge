# The 7 Rules

Based on Claude Context OS research — LLMs track 5-10 constraints before performance degrades.

1. **Do not mix unrelated contexts** in one session
2. **Write state to memory** — After meaningful work, write to `.claude/memory/journal.md`. Include: decisions, numbers, file paths, open items
3. **Before session end** — Write everything to `.claude/memory/journal.md`: decisions, numbers, questions, file paths, next actions
4. **When switching work types** — Write handoff in `.claude/memory/journal.md`, suggest new session
5. **Do not silently resolve open questions** — Mark them OPEN or ASSUMED in memory
6. **Do not bulk-read documents** — Process one at a time: read, summarize to memory, release before next
7. **Sub-agent returns must be structured** — Use output contracts, not free-form prose
