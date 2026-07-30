# SISO Knowledge

The durable knowledge-production system for SISO.

```text
source material
    ↓
pipelines + knowledge operators
    ↓
canonical pages and books
    ↓
indexes + graph + query tools
    ↓
Great Library and other consumers
```

## Current physical map

| Path | Responsibility | State |
| --- | --- | --- |
| `sections/`, `books/` | Canonical knowledge corpus | Source of truth |
| `pipelines/` | Source acquisition, normalization, scoring, and routing | Active; includes raw/state material still awaiting lifecycle separation |
| `agents/` | Knowledge feeders and chief-librarian operation | Knowledge-specific; not the reusable agent stack |
| `module_templates/` | Canonical corpus contracts | Authored source |
| `queries/`, `scripts/` | Add, query, rebuild, and maintenance operations | Authored source |
| `_index/`, `graph/` | Search and relationship projections | Generated; never hand-edit |
| `source-inventories/` | Preserved mixed historical source | Evidence-led staging |
| `research/` | Independent research-production Works | Foundry + Evidence Engines; separate Git histories |
| `apps/library-web/` | Legacy deployable web product | Independent Git checkout; extraction pending |
| `design-system/` | Shared UI system | Boundary exception; 746 dirty entries block safe filing |
| `memory/`, `.omc/` | Legacy/operator runtime state | Debt; not new source authority |

The public [Great Library of SISO](../Great_Library_of_SISO/README.md) is a workspace-root registry over SISO Works. It is not a parent folder for this repository and this repository is not its parent.

## Naming and compatibility

`SISO_Knowledge` is the canonical path. The old `SISO_Library` compatibility name was retired after active code and configuration checks found no consumers. Historical reports still mention the former name and remain valid evidence.

Run the route gate:

```bash
../scripts/migrate-siso-knowledge-paths.sh --check
```

See the [boundary audit](../docs/siso-library-boundary-audit-2026-07-30.html) for the reasoning and the [migration receipt](../docs/siso-knowledge-migration-2026-07-30.html) for what physically changed.

Current authority: [DOMAIN.html](DOMAIN.html) · `DOMAIN-MANIFEST.json` · `DATA-MANIFEST.json` · [MIGRATION-RECEIPT.html](MIGRATION-RECEIPT.html).
