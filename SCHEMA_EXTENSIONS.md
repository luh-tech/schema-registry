# LuhTech Schema Extension Pattern

**Version:** 1.0.0 | **Date:** 2026-02-26 | **Source:** Transform Fabric Architecture Strategy v2.0.0

## Purpose

Individual ventures can extend the canonical roadmap schema for domain-specific data needs. Extension fields are venture-local — they do not pollute the canonical template or the portfolio-level summary.

## The Core Rule

**Extension fields MUST live under `extensions.*`** — canonical field names are reserved.

```json
{
  "$schema": "urn:luhtech:schema:roadmap:v3.1",
  "venture": {
    "type": "IoT Platform",
    "mission": "...",
    "extensions": {
      "_ventureId": "jobsitecontrol",
      "_extensionSchemaVersion": "1.0.0",
      "hardwareComponents": [...],
      "meshNetworkTopology": {...},
      "pilotSiteData": {...}
    }
  }
}
```

## Creating a Venture Extension Schema

1. Copy `templates/venture-extension-schema.template.json` to your venture repo:
   ```
   <venture>/.roadmap/roadmap-local.schema.v1.0.json
   ```

2. Replace `{{VENTURE_ID}}` and `{{VENTURE_NAME}}` placeholders.

3. Add your domain-specific fields under the `extensions.properties` block.

4. Validate your roadmap.json against the local extension schema (not just the canonical one).

## Governance Rules

| Rule | Description |
|------|-------------|
| **Namespace** | Extension fields MUST live under `extensions.*`. Any field at the canonical level is reserved. |
| **Location** | Extension schemas live in the venture repo — NOT in `luh-tech-roadmap-template`. |
| **Transform isolation** | The canonical `venture-summary-full` transform ignores `extensions.*` fields. Extension data does not appear in portfolio-level summary unless an explicit venture-specific transform is registered. |
| **Venture-local transforms** | Ventures may register additional transforms (e.g., `jobsitecontrol-hardware-report.transform.v1.json`) that use extension fields to produce venture-specific outputs. |
| **Promotion pathway** | If an extension field proves useful across 3+ ventures, open a PR to promote it to the canonical schema. Extensions are incubators for future canonical fields. |

## Novel Data Flow

```
Venture creates novel data in extensions.*
  → Local schema validates it
  → Venture-local transform reads extension fields
  → Produces venture-specific outputs (custom slides, hardware manifest, local dashboards)
  → Canonical transform ignores extensions.*
  → venture-summary.json contains only canonical fields
  → Holdings sees a clean canonical view
```

This is the essential abstraction pattern for scaling: **ventures own their domain specificity; holdings owns the portfolio-level truth.**

## Promotion Pathway (extensions → canonical)

When an extension field is useful across 3+ ventures:

1. Open a PR to `luh-tech/luh-tech-roadmap-template` with the proposed canonical field.
2. The PR must include:
   - Schema change to `roadmap.schema.v3.x.json`
   - Migration guide for existing extension users
   - Evidence of use across 3+ ventures
3. Once merged, ventures should migrate from `extensions.<field>` → canonical location.
4. The old `extensions.<field>` can be retained for one schema version as a deprecated alias.

## Example: JobsiteControl Hardware Extension

```json
{
  "$id": "urn:luhtech:jobsitecontrol:schema:roadmap-local:v1.0",
  "allOf": [{ "$ref": "urn:luhtech:schema:roadmap:v3.1" }],
  "properties": {
    "extensions": {
      "type": "object",
      "properties": {
        "_ventureId": { "type": "string", "const": "jobsitecontrol" },
        "_extensionSchemaVersion": { "type": "string" },
        "hardwareComponents": { "type": "array" },
        "meshNetworkTopology": { "type": "object" },
        "pilotSiteData": { "type": "object" }
      }
    }
  }
}
```

## Schema Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-26 | Initial extension pattern documentation. Source: Transform Fabric Architecture v2.0.0, Section 7. |
