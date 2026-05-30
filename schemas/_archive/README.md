# schemas/_archive/

Deprecated schemas, retained for historical reference and instance-validation of
legacy data only. **Nothing here is canonical.** The registry (`schema-refs.json`)
does not point at these files.

## Lifecycle
A schema lands here when it is removed from `schema-refs.json`. Each archived file
carries a top-level `x-deprecation` block: `deprecated`, `deprecatedDate`,
`deprecationReason`, `supersededBy`, `archivedFrom`.

## Contents
- `venture-summary.schema.json` (v1) — derived-artifact schema, deprecated 2026-05-30.
- `venture-summary.schema.v2.0.json` (v2.0) — derived-artifact schema, deprecated 2026-05-30.
  Removed from registry at schema-refs v1.14.0. Consumers (dashboard-sync, dataroom-sync)
  migrating off per FU-VENTURE-SUMMARY-DOWNSTREAM-MIGRATION-1.

Enterprise Excellence. Schema-First. No Shortcuts.
