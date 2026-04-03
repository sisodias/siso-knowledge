# Rule: Persistent State Management

1. **File System is Truth:** Always query `memory/` directory, never session memory
2. **Atomic Memory Updates:** Append summaries to `memory/journal.md` after each pipeline run
3. **Context Rehydration:** Read last entries in `memory/journal.md` on boot
4. **No Deletions:** Move completed work to `memory/ARCHIVE/`
5. **Status Updates:** Update `memory/state.json` when starting/finishing tasks
