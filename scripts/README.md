# SISO_Knowledge scripts

This directory contains one-shot maintenance scripts for the SISO Knowledge content pipeline.

## backfill_creator.py

Fills empty `creator` frontmatter fields using `source_video` metadata.

**Usage:**

```bash
# Dry-run (default) — prints what would change, no files written
python3 backfill_creator.py

# Apply changes for real
python3 backfill_creator.py --apply

# Limit to N pages (useful for spot-testing)
python3 backfill_creator.py --apply --limit 10
```

**Resolution rules (in priority order):**

| `source_video` shape | Resolution |
|---|---|
| Bare 11-char YouTube video ID (e.g. `nxuTVd7v7dg`) | Look up `yt_channel_cache.json` for channel name |
| `youtube.com/watch?v=…` or `youtu.be/…` URL | Extract video ID, then lookup cache |
| `github.com/owner/repo` URL | Set `creator = owner` |
| `reddit.com/r/subreddit/…` URL | Set `creator = r/subreddit` |
| Anything else / cache miss | Creator left empty |

**Cache file:** `_index/yt_channel_cache.json` — a JSON dict mapping video IDs to channel names. Created as `{}` if absent. The script tolerates a missing or empty cache gracefully (uncached YouTube IDs are counted but not written).

**Atomic writes:** When run with `--apply`, frontmatter is rewritten using a temp-file swap on the same filesystem to avoid partial writes.

**Exit codes:**

- 0 — completed (dry-run or apply)
- non-zero — error (file read/write failure, YAML parse error)
