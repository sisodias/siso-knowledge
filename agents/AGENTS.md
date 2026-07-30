# Knowledge operators

These are domain-specific feeder and curator operator definitions, not the reusable agent stack.

- Generic Skills, Runtime, Agent Zero, Brain, and Playbooks belong in `../../SISO_Agents/`.
- Operator definitions may stay with the Knowledge process they operate.
- Memories, inboxes, outboxes, heartbeats, logs, and workspaces are legacy mixed state; do not add
  more tracked runtime state. The layout gate ratchets today's debt.
- Several March 2026 identities contain stale path and schedule claims. Treat them as legacy until
  the referenced command and scheduler are directly verified.
- Eight central-skill symlinks are preserved compatibility debt; do not add another.
