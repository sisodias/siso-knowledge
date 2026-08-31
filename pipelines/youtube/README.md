# People YouTube Acquisition Pipeline

This folder now contains the safe front door for person-centered YouTube collection.

## What It Does

- Builds search plans for every person in `pipelines/people/leaderboard.yaml`.
- Optionally uses the official YouTube Data API for video metadata when `YOUTUBE_API_KEY` is set.
- Imports user-provided transcript exports from a Chrome transcript plugin.
- Exports transcript-ready videos into the existing `/tmp/youtube-prioritized.json` format used by `extract_prioritized.py`.

No bulk third-party video downloading is enabled here. Transcripts should come from manual/plugin exports, official APIs, public captions where permitted, or owned/permissioned media.

## Run It

Create or refresh the search plan:

```bash
python3 pipelines/youtube/discover_people_videos.py --dry-run
```

Run API-backed discovery after adding a YouTube Data API key:

```bash
YOUTUBE_API_KEY=... python3 pipelines/youtube/discover_people_videos.py
```

Seed candidates from the existing local YouTube research database:

```bash
python3 pipelines/youtube/seed_existing_research.py --limit-per-person 10
```

Add a manual candidate video:

```bash
python3 pipelines/youtube/add_people_video.py \
  --person bob-lazar \
  --video-url "https://www.youtube.com/watch?v=BEWz4SXfyCQ" \
  --title "Joe Rogan Experience #1315 - Bob Lazar & Jeremy Corbell" \
  --channel "PowerfulJRE"
```

Import candidates from Firecrawl/Perplexity/search JSON:

```bash
python3 pipelines/youtube/import_search_results.py \
  --file pipelines/youtube/search_results/bob-lazar.json \
  --person bob-lazar \
  --source firecrawl_search
```

Or import every `person-slug*.json` file in the search results folder:

```bash
python3 pipelines/youtube/import_search_results_batch.py
```

If Firecrawl is authenticated, one-off searches can be saved into that folder:

```bash
firecrawl search "Bob Lazar interview YouTube" \
  --limit 8 \
  -o pipelines/youtube/search_results/bob-lazar.json \
  --json
```

Import a transcript from the Chrome plugin:

```bash
python3 pipelines/youtube/import_plugin_transcript.py \
  --file pipelines/youtube/inbox/plugin_exports/example.txt \
  --video-url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --person bob-lazar \
  --title "Interview title" \
  --channel "Channel name"
```

Or drop transcript exports into the inbox using this filename convention:

```text
pipelines/youtube/inbox/plugin_exports/{person_slug}__{video_id}__{optional-title}.txt
```

Example:

```text
pipelines/youtube/inbox/plugin_exports/bob-lazar__BEWz4SXfyCQ__Joe-Rogan-Experience-1315.txt
```

Then import every inbox transcript:

```bash
python3 pipelines/youtube/import_plugin_exports_batch.py
```

Export videos that now have transcripts:

```bash
python3 pipelines/youtube/export_people_ready.py --min-tier C
```

Then run the existing extractor:

```bash
python3 pipelines/youtube/extract_prioritized.py --input /tmp/youtube-prioritized.json --dry-run
```

Refresh the safe setup end-to-end:

```bash
python3 pipelines/youtube/run_people_collection_setup.py
```

Write the collection status report:

```bash
python3 pipelines/youtube/report_people_collection.py
```

Write the transcript backlog:

```bash
python3 pipelines/youtube/report_transcript_backlog.py
```

Build per-person dossiers:

```bash
python3 pipelines/people/dossier_builder.py
```

Build non-YouTube source plans for corpus/direct/social/manual collection:

```bash
python3 pipelines/people/source_planner.py
```

Download approved public-domain Project Gutenberg source texts:

```bash
python3 pipelines/people/source_ingest.py
```

## Data Locations

- Query plan: `pipelines/youtube/reports/person_video_queries.json`
- Collection status: `pipelines/youtube/reports/people_collection_status.md`
- Transcript backlog: `pipelines/youtube/reports/transcript_backlog.md`
- People dossiers: `pipelines/people/dossiers/README.md`
- Source backlog: `pipelines/people/source_plans/source_backlog.md`
- Raw public-domain sources: `pipelines/people/raw_sources/manifest.json`
- Queue DB: `pipelines/youtube/people_video_queue.sqlite`
- Plugin transcript inbox: `pipelines/youtube/inbox/plugin_exports/`
- Normalized transcripts: `pipelines/youtube/transcripts/{person_slug}/{video_id}.yaml`
- Existing local YouTube research seed DB: `apps/library-web/data/youtube-research/database/queue.db`
