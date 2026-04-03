# Inbox

Tasks assigned to this agent. Use JSONL format for atomic appends.

## Format
```json
{"id": "msg_001", "from": "agent-name", "type": "handoff", "instruction": "Task description"}
```

## Usage
- Check this folder for pending tasks
- Process tasks in order or by priority
- Move completed task files to `outbox/` when done
