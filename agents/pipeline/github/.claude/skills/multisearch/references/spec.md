# Multi-Search — Definition of Done

## Success Criteria

1. All 3 searches run in parallel (not sequential)
2. Results from all sources aggregated
3. Cross-source insights identified
4. Any contradictions noted
5. Relevant URLs from each source

## Output Format

```json
{
  "query": "search terms",
  "web": { "summary": "...", "sources": [...] },
  "github": { "results": [...], "sources": [...] },
  "twitter": { "discussions": [...], "sources": [...] },
  "cross_source_insights": "...",
  "contradictions": "any conflicts between sources"
}
```

## Parallel Execution

- Use `Task` tool with `run_in_background: true`
- Launch all 3 agents simultaneously
- Wait for all to complete before synthesizing
