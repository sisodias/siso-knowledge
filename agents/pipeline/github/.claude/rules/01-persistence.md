# Rule: Persistent State Management

1. **File System is Truth:** Never rely on session memory. Always query `memory/` directory.

2. **Atomic Memory Updates:** After completing a task, append summary to `memory/journal.md` including:
   - Task ID
   - Outcome
   - Next Steps

3. **Context Rehydration:** On boot, if asked "Where were we?", read last entries in `memory/journal.md`.

4. **No Deletions:** Never delete from `memory/`. Move completed work to `memory/ARCHIVE/`.

5. **Status Updates:** Update `memory/state.json` when starting/finishing tasks.
