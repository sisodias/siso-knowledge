# SISO Knowledge — agent guide

SISO Knowledge acquires, curates, stores, indexes, relates, and retrieves durable knowledge. It is an owning domain, not the public Great Library and not the reusable agent platform.

## Cold start

Read in this order:

1. `README.md` — current physical map and boundary rules.
2. `CLAUDE.md` — corpus hierarchy, generated-index contract, and commands.
3. `DOMAIN.html` — current human architecture, boundaries, exceptions, and debt.
4. `DOMAIN-MANIFEST.json` and `DATA-MANIFEST.json` — machine-readable placement and data contracts.
5. `MIGRATION-RECEIPT.html` — evidence-backed cleanup receipt.

## Filing rule

| Material | Home |
| --- | --- |
| Canonical pages, books, sections | `sections/`, `books/` |
| Knowledge acquisition and curation | `pipelines/`, knowledge-specific `agents/`, `scripts/` |
| Schemas and deterministic query/rebuild tools | `module_templates/`, `queries/` |
| Rebuildable discovery projections | `_index/`, `graph/` |
| Historical mixed source awaiting promotion | `source-inventories/` |
| Independent research-production Works | `research/` |
| Reusable agent capability | `../SISO_Agents/`, not here |
| Public Work registry and reading surface | `../Great_Library_of_SISO/`, not here |
| Deployable product or reusable UI system | Pending extraction; do not add another one here |

Knowledge-specific feeder and curator agents stay with the process they operate. Their presence under `agents/` does not make this an agent-platform repository.

## Current migration boundary

- Canonical checkout: `$SISO_WORKSPACE/SISO_Knowledge`.
- The former `SISO_Library` compatibility name was retired after active code/config checks passed.
- Historical documents may name it; operational routes must use `SISO_Knowledge`.
- Check route regressions with `../scripts/migrate-siso-knowledge-paths.sh --check`.
- Do not reorganize `sections/`, `_index/`, or `pipelines/` while Agency still consumes those subpaths.

## Repository boundaries

This checkout currently contains dirty work and independent nested Git repositories. Preserve their histories and changes:

- `apps/library-web/` — independent legacy knowledge web product; extraction pending.
- `design-system/` — independent UI system; extraction pending.
- `source-inventories/great-library-research-2025/` — clean historical collection; preserve verbatim.
- `research/siso-foundry/` — independent Research Work; dirty schema edit preserved during filing.
- `research/siso-evidence-engines/` — independent Research Work.

Boundary exceptions are explicit, not endorsements:

- `apps/library-web/` — dirty deployable product; future Agency filing, move currently blocked.
- `design-system/` — dirty shared UI system; not Knowledge, move currently blocked.

The legacy component paste-bank, obsolete workflow mirror, already-archived agent homes,
superseded `Section_Templates`, and stale `scrapers/` event design were reversibly filed in
`../_archive/siso-knowledge-boundary-2026-07-30/`.

The workspace-root `Great_Library_of_SISO/` is a separate clean public repository. Local nesting never defines public identity.

## Verification

```bash
../scripts/migrate-siso-knowledge-paths.sh --check
./scripts/check-layout.sh
python3 queries/query.py --help
(cd ../Great_Library_of_SISO && npm run verify)
```

Do not rebuild `_index/` merely to test a path migration: rebuilds write generated state. Run `python3 queries/rebuild_index.py` only for an intentional corpus/index change.
