# External Dataset Freshness Schema

Generated: `2026-05-08`

## Core Rule

Do not confuse **upstream freshness** with **content coverage**.

A GitHub repo can be updated today while only containing old episodes. A static Hugging Face dataset can be stale but still contain very high-quality historical transcripts. A rolling official page can be current, but individual records still need episode publication dates.

## Lightweight Registry Fields

`external_datasets.yaml` keeps these flat fields for fast scanning:

- `observed_at`: when SISO inspected this candidate.
- `source_last_updated`: platform-visible updated date, e.g. GitHub `updated_at`, HF `lastModified`, or `rolling_site`.
- `data_coverage_start`: earliest source content covered when known.
- `data_coverage_end`: latest source content covered when known.
- `freshness_notes`: human-readable assessment.

## Full Import Manifest Shape

Every actual importer should emit a richer manifest:

```json
{
  "schema": "siso.people.import_manifest.v1",
  "generated_at": "2026-05-08T04:17:36Z",
  "dataset_id": "lenny-podcast-transcripts-chatprd",
  "dataset_snapshot": {
    "source_url": "https://github.com/ChatPRD/lennys-podcast-transcripts",
    "platform": "github",
    "observed_at": "2026-05-08T05:50:00Z",
    "upstream_created_at": "2026-01-14T03:16:58Z",
    "upstream_updated_at": "2026-05-08T05:47:38Z",
    "upstream_pushed_at": "2026-01-28T19:32:11Z",
    "revision": null,
    "license_observed": "personal_educational_use_in_readme"
  },
  "coverage": {
    "record_count": 269,
    "coverage_start_date": null,
    "coverage_end_date": null,
    "coverage_start_label": null,
    "coverage_end_label": null,
    "coverage_granularity": "episode",
    "coverage_confidence": "medium"
  },
  "record_date_fields": {
    "publication_date_field": "frontmatter.date",
    "episode_date_field": "frontmatter.date",
    "upload_date_field": "frontmatter.youtube_upload_date",
    "timestamp_fields": ["start", "end"],
    "source_url_field": "frontmatter.youtube_url"
  },
  "retrieval": {
    "retrieved_at": "2026-05-08T04:17:36Z",
    "retriever": "people-pipeline",
    "local_path": "/Users/shaansisodia/SISO_Workspace/SISO_Knowledge/pipelines/people/raw_sources/...",
    "bytes": 123456,
    "checksum_sha256": null
  },
  "freshness_assessment": {
    "class": "current_metadata_unknown_content",
    "reason": "GitHub metadata is current, but episode coverage range must be computed from transcript frontmatter.",
    "requires_recheck_after": "2026-06-07"
  }
}
```

## Platform Mapping

For GitHub datasets:

- `dataset_snapshot.upstream_created_at` = GitHub `created_at`
- `dataset_snapshot.upstream_updated_at` = GitHub `updated_at`
- `dataset_snapshot.upstream_pushed_at` = GitHub `pushed_at`
- add `revision` or `last_commit_sha` when cloning or importing files

For Hugging Face datasets:

- `dataset_snapshot.upstream_created_at` = HF `createdAt`
- `dataset_snapshot.upstream_updated_at` = HF `lastModified`
- `dataset_snapshot.revision` = pinned commit/revision if available
- capture `siblings`/file shard names in importer-specific metadata

For official transcript pages:

- `dataset_snapshot.upstream_updated_at` only if the page/feed exposes it
- `coverage.coverage_end_date` should come from episode publish date, not scrape date
- `record_date_fields` should list page selectors/feed fields such as `datePublished`, RSS `pubDate`, `episode_date`, or YouTube `uploadDate`

For Project Gutenberg / public-domain books:

- store catalog snapshot date
- store ebook release/update date if available
- store original publication year, edition year, translator, and editor when known

## Freshness Classes

- `current`: source metadata and content coverage are recent enough for current research.
- `rolling`: source updates continuously; per-record dates are required.
- `stale_but_useful`: old dataset but historically useful.
- `stale_partial`: old and incomplete relative to current target coverage.
- `static_corpus`: fixed book/archive corpus where recency is less important than edition/provenance.
- `unknown`: insufficient metadata; inspect before import.

## Importer Requirements

Every external importer should:

- emit an import manifest using the full schema above
- store source URL and upstream platform metadata
- store source-content dates separately from retrieval dates
- store local path, byte count, and checksum
- store license/rights fields per dataset and, when possible, per record
- preserve episode/video/book/page dates for downstream freshness ranking
