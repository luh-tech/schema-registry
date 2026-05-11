# Patent Schema Family (SBPA)

JSON Schema definitions for the **SBPA** (Spatially-Bound Provenance Architecture) patent portfolio infrastructure. These schemas describe the data model for tracking a patent portfolio, its provisional bundles, prior-art references, glossary terminology, and figure metadata — **not the inventions themselves**.

Owned by **LuhTech Holdings** (`luh-tech/LuhTech-business`). Promoted to the canonical registry at v1.0.0 on 2026-05-11.

## Schemas

| Schema | Purpose |
|--------|---------|
| [`portfolio`](portfolio.schema.json) | Top-level patent portfolio (SBPA umbrella + member provisionals) |
| [`provisional`](provisional.schema.json) | One provisional patent application (status lifecycle, filing-readiness gate) |
| [`manifest`](manifest.schema.json) | Per-provisional bundle manifest (decisions log, figures, glossary, prior-art references) |
| [`figure-sidecar`](figure-sidecar.schema.json) | Metadata sidecar for each patent figure asset |
| [`glossary`](glossary.schema.json) | Patent-family glossary structure |
| [`glossary-entry`](glossary-entry.schema.json) | Single glossary term with state (DEPRECATED, PATENT-OWNED, etc.) |
| [`prior-art-entry`](prior-art-entry.schema.json) | Prior-art reference with citation metadata |

## Dialect

All seven schemas declare `$schema: http://json-schema.org/draft-07/schema#` per LuhTech canonical standard (see `LUHTECH-PATENT-FOUNDATION-CORRECTIONS-2026-05-06.md` §6).

## Validation

Reference implementation in B-T at `scripts/validate-schemas.py` (uses `Draft7Validator` matching the declared dialect).

## Cross-references

- B-T patent foundation: `luh-tech/LuhTech-business/schemas/patent/`
- B-T decision-log canonical entry: `d-2026-05-05-patent-pipeline-foundation`
- B-T validator stabilization: `d-2026-05-11-patent-validator-stabilization`
