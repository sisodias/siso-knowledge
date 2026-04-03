# Lab Intelligence — Research Review Inbox

Heartbeat drops Lab-relevant integration opportunities here for review.

## What belongs here

Research on topics relevant to SISO Internal Lab:
- UI experiments and prototypes
- Frontend/dashboard implementations
- React/Next.js explorations
- D3 visualizations
- Web dev patterns
- Visualization experiments

## Format

```json
{
  "type": "integration_review",
  "source": "os_insights",
  "timestamp": "2026-03-20T22:44:36",
  "tier": "medium",
  "title": "Dashboard Pattern",
  "source_detail": "YouTube",
  "components": "ui, frontend",
  "insight": "The insight...",
  "url": "https://...",
  "status": "pending_review",
  "routed_to": "lab"
}
```

## Review Workflow

1. Read JSON files in this inbox
2. Relevant to Lab experiments → create prototype spec in `workspace/`, then delete file
3. Not relevant → delete file

## Tiers

- **high**: Prototype-worthy
- **medium**: Interesting reference
- **low**: tangentially interesting
