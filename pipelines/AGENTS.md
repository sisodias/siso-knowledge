# Knowledge production pipelines

This directory owns acquisition, normalization, scoring, routing, and curation code.

- Git stores code, schemas, provenance contracts, and small synthetic fixtures.
- Corpora, transcripts, queues, provider exports, databases, logs, caches, and generated reports
  follow `../DATA-MANIFEST.json` and stay outside Git.
- Every acquired item preserves owner, source URL, rights/license status, retrieval time, and
  transformation provenance.
- `github/` is explicitly superseded by the Mac mini research lane; preserve it as reference
  until its reusable source is compared, but do not describe it as active.
- Commands must accept paths through arguments or environment variables; new personal absolute
  paths are rejected by the layout ratchet.
