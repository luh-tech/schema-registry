# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-04-17

### Added
- `roadmap.schema.v3.3.json` — new T1 roadmap schema v3.3.0
  - Optional `provides: array[string]` on feature objects — capabilities the feature provides; each value references a capability id from `data/capabilities.json` in the business-tools monorepo
  - Optional `lifecyclePhases: array[integer 0-7]` on feature objects — RIBA Plan of Work 2020 stages the feature applies to; references phases from `data/lifecycle-phases.json`
  - Both fields default to empty array; neither is required
  - Source: requires/provides matching infrastructure in business-tools (commit 5bd5c4c3) — capabilities.json, challenges.json, lifecycle-phases.json
- `schema-refs.json` → v1.8.0, roadmap entry now points at v3.3

### Notes
- `xaasServices`, `xaasServicePrimary`, and `personaRelevance` continue to ride on `additionalProperties: true` and are intentionally NOT formalized in this revision. A future schema version may regularize them alongside. The asymmetry is deliberate: `provides`/`lifecyclePhases` got formal treatment because they power a new graph projection with well-defined coverage semantics; their cousins remain de-facto conventions until that same scrutiny reaches them.

## [Unreleased] - 2026-04-16

### Added
- `roadmap.schema.v3.2.json` — new T1 roadmap schema v3.2.0
  - Required `scope` field on feature objects (enum: `product`, `infrastructure`, `enterprise-tool`, `standard`)
  - Security-first default for ambiguous cases: `infrastructure`
  - Existing `category` field (topic/domain axis) remains unchanged
  - Source: ECTROPY-OPENCORE-STRATEGY-2026-04-16 Decision 1 — Phase A schema introduction
- `schema-refs.json` → v1.7.0, roadmap entry now points at v3.2

### Notes
- CHANGELOG was stale (no entries since v2.0.0). This entry documents today's change only; schema versions v2.2–v3.1 landed without CHANGELOG entries and are not backfilled here.
- Venture CI currently validates against v2 schemas via `ajv`. v3.2 constraint becomes enforceable once venture workflows are upgraded (separate future task).

## [2.0.0] - 2026-01-27

### Added

#### Reusable Workflow Enhancement
- **PHASE 3: Business Documentation** validation section in `roadmap-validate.yml`
- Validation for `roadmap-business.json` (business roadmap data)
- Validation for `workflow-registry.json` (CI/CD documentation)
- Validation for `metrics-pipeline.json` (observability configuration)
- Validation for `deployment-metrics.json` (Watchtower deployment tracking)
- Validation for `interfaces.json` (MCP tools and API definitions)
- Validation for `features/*.json` (feature specifications)
- Enhanced GitHub Actions summary with phase breakdown

#### Schema Promotion (6 new schemas from Ectropy)
- `feature.schema.json` - Feature specifications with milestones and ROI tracking
- `interfaces.schema.json` - MCP tools and API definitions
- `workflow-registry.schema.json` - CI/CD workflow documentation
- `metrics-pipeline.schema.json` - Observability and failure handling configuration
- `deployment-metrics.schema.json` - Watchtower deployment tracking
- `roadmap-business.schema.json` - Business roadmap with financials and team data

#### Templates
- `templates/roadmap-business.json` - Business roadmap template
- `templates/deployment-metrics.json` - Deployment metrics template
- `templates/workflow-registry.json` - Workflow registry template
- `templates/metrics-pipeline.json` - Metrics pipeline template
- `templates/feature.json` - Feature specification template
- `templates/interfaces.json` - Interfaces definition template

#### Phase 2 Infrastructure Validation
- Added `architecture.json` validation against `architecture-roadmap.schema.v1.json`
- Added `extensions.json` validation against `extensions.schema.v1.json`

### Changed
- Three-phase validation structure (Core → Infrastructure → Business)
- Enhanced summary output with validation phase breakdown
- All new validations are OPTIONAL (backwards compatible)

### Portfolio Impact
- All 8 ventures automatically inherit the enhanced validation
- Ectropy flagship venture is Phase 3 ready
- Other ventures show SKIP (not FAIL) for Phase 3 files

---

## [1.5.0] - 2026-01-27

### Added
- Venture schema rollout with `schema-refs.json` in all 8 ventures
- Comprehensive schema documentation in `schemas/README.md`
- `validate-schemas.yml` workflow template for ventures

### Changed
- Updated all venture `.roadmap/schema-refs.json` to reference v1.5.0

---

## [1.0.0] - Initial Release

### Added
- Core schema library (18 schemas)
- Roadmap schema v2 with quarterly structure
- Venture summary schema for pitch data
- Decision log schema for ADR tracking
- Dependencies and boundaries schemas
- Tech stack and infrastructure catalog schemas
- Reusable `roadmap-validate.yml` workflow
- Basic templates for venture spin-up

---

*Enterprise Excellence. Schema-First. No Shortcuts.*

*LuhTech Holdings*
