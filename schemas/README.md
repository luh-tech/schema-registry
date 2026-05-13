# LuhTech Infrastructure Documentation Schema System

**Version:** 1.5.0  
**Status:** Phase 3 Complete - Template Architecture Migration  
**Date:** 2026-01-28  
**Principle:** No Shortcuts, Enterprise Excellence Always

---

## Overview

This schema system provides standardized infrastructure documentation for the LuhTech portfolio. Derived from Ectropy's production infrastructure (202KB infrastructure-catalog.json, 261KB decision-log.json, 153KB current-truth.json), these schemas enable:

- **MCP Server Governance** - Token-efficient AI agent access (97% reduction)
- **Portfolio Intelligence** - Aggregator-level visibility across 8 ventures
- **Accelerator Foundation** - Turnkey templates for new portfolio companies
- **Schema-First Architecture** - Generated models, CI enforcement, no drift
- **Cross-Repo Workflow Discovery** - Portfolio workflows referenced by $ref
- **Venture Extensions** - Explicit sharing control for venture-specific data
- **URN Identifiers & Graph System** - Cross-venture entity linking and graph queries
- **Feature Tracking** - Milestone-based development with ROI tracking (NEW)
- **Observability Pipeline** - Multi-destination metrics with failure handling (NEW)

---

## Schema Inventory

### Core Venture-Level Schemas

| Schema | Version | Size | Purpose |
|--------|---------|------|---------|
| `roadmap.schema.v3.3.json` | v3.3.0 | ~40KB | **LATEST** - Adds optional `provides` + `lifecyclePhases` on feature objects (requires/provides matching infrastructure) |
| `roadmap.schema.v3.2.json` | v3.2.0 | ~40KB | Adds required `scope` field on features (product/infrastructure/enterprise-tool/standard) |
| `roadmap.schema.v3.1.json` | v3.1.0 | ~40KB | Adds mission/vision/currentStage/overallProgress to venture block |
| `roadmap.schema.v2.2.json` | v2.2.0 | ~25KB | Venture roadmap with resources block, vendor-agnostic features |
| `roadmap.schema.v2.1.json` | v2.1.0 | ~19KB | Features array, releases tracking |
| `roadmap.schema.v2.json` | v2.0.0 | ~19KB | Venture roadmap, quarters, financials, milestones |
| `venture-summary.schema.json` | v1.0.0 | ~11KB | Investor pitch summary |
| `decision-log.schema.v2.json` | v2.0.0 | ~10KB | Enhanced ADR with voting, indexes, implementation tracking |
| `dependencies.schema.json` | v1.0.0 | ~5KB | Cross-venture dependencies |
| `boundaries.schema.json` | v1.0.0 | ~3KB | Fork configuration |
| `infrastructure-catalog.schema.json` | v1.1.0 | ~24KB | Service registry, environments, secrets, workflows |
| `tech-stack.schema.json` | v1.0.0 | ~17KB | Languages, frameworks, databases, architecture patterns |
| `evidence-session.schema.json` | v1.0.0 | ~12KB | Investigation tracking, evidence nodes, retention policies |
| `extensions.schema.v1.json` | v1.0.0 | ~2KB | Venture-specific extensions with share control |

### Newly Promoted Schemas (v1.5.0)

| Schema | Version | Size | Purpose |
|--------|---------|------|---------|
| `feature.schema.json` | v1.0.0 | ~10KB | **NEW** - Feature specifications with milestones, deliverables, ROI tracking |
| `interfaces.schema.json` | v1.0.0 | ~9KB | **NEW** - MCP tools, REST APIs, GraphQL resolvers, middleware specs |
| `workflow-registry.schema.json` | v1.0.0 | ~7KB | **NEW** - GitHub Actions workflow documentation and categorization |
| `metrics-pipeline.schema.json` | v1.0.0 | ~9KB | **NEW** - Metrics collection, failure handling, multi-destination reporting |
| `deployment-metrics.schema.json` | v1.0.0 | ~5KB | **NEW** - Watchtower deployment tracking per environment |
| `roadmap-business.schema.json` | v1.0.0 | ~9KB | **NEW** - Business roadmap: financials, team, competitive positioning |

### Portfolio-Level Schemas

| Schema | Version | Size | Purpose |
|--------|---------|------|---------|
| `portfolio/workflow-registry.schema.json` | v1.0.0 | ~11KB | Portfolio workflow definitions, transformers, deck types |
| `portfolio/brand.schema.json` | v1.0.0 | ~11KB | Brand assets, colors, typography |
| `portfolio/portfolio.schema.json` | v1.0.0 | ~16KB | Aggregated portfolio view |
| `portfolio/ip-assets.schema.json` | v1.0.0 | ~10KB | Intellectual property tracking |
| `portfolio/extensions-matrix.schema.v1.json` | v1.0.0 | ~2KB | Portfolio-level extension aggregation |
| `portfolio/portfolio-graph.schema.v1.json` | v1.0.0 | ~5KB | Portfolio-wide graph structure |

### Shared Building Blocks

| Schema | Version | Purpose |
|--------|---------|------------|
| `_enums/luhtech-enums.schema.v2.json` | v2.0.0 | Shared enumerations (ventureId, status, etc.) |
| `_definitions/definitions.schema.json` | v1.1.0 | Shared type definitions + URN/graph refs |
| `_definitions/graph.schema.json` | v1.0.0 | URN identifiers and graph metadata |

---

## New Schema Details (v1.5.0)

### feature.schema.json

Feature specifications with milestones, deliverables, and business value tracking.

- **JSON Schema Draft:** Draft-07
- **Use Cases:** Feature planning, milestone tracking, ROI estimation, pilot deployments
- **Template:** `templates/feature.json`
- **Key Features:**
  - Milestone tracking with completion criteria
  - Business value metrics (ROI, savings, incidents avoided)
  - Dependency management (schemas, services, features, external)
  - Graph metadata for AI navigation
  - Scenario-based ROI estimation

**Example Structure:**
```json
{
  "$schema": "https://schemas.luh.tech/feature.schema.json",
  "$id": "urn:luhtech:ectropy:feature:decision-lifecycle",
  "featureId": "decision-lifecycle",
  "name": "Decision Lifecycle",
  "status": "PRODUCTION",
  "priority": "CRITICAL",
  "milestones": [
    {
      "id": "M1",
      "name": "Schema Migration",
      "status": "COMPLETE",
      "deliverables": [".roadmap/schemas/decision.schema.json"]
    }
  ]
}
```

### interfaces.schema.json

MCP tool signatures, REST API endpoints, GraphQL resolvers, and middleware specifications.

- **JSON Schema Draft:** Draft-07
- **Use Cases:** API documentation, MCP tool definitions, event specifications
- **Template:** `templates/interfaces.json`
- **Key Features:**
  - MCP tool definitions with categories and parameters
  - REST API endpoint documentation
  - GraphQL resolver specifications
  - Middleware pipeline definitions
  - Event system documentation

**Example Structure:**
```json
{
  "$schema": "https://schemas.luh.tech/interfaces.schema.json",
  "mcpTools": {
    "totalCount": 39,
    "categories": [
      {
        "name": "decision-tools",
        "tools": [
          {
            "id": "create_decision",
            "description": "Create a new architectural decision record"
          }
        ]
      }
    ]
  }
}
```

### workflow-registry.schema.json

GitHub Actions workflow documentation and categorization following enterprise patterns.

- **JSON Schema Draft:** Draft-2020-12
- **Use Cases:** CI/CD documentation, workflow categorization, failure mode tracking
- **Template:** `templates/workflow-registry.json`
- **Key Features:**
  - Workflow categorization (ci, cd, validation, sync, monitoring)
  - Trigger documentation (push, pull_request, schedule, workflow_dispatch)
  - Dependency tracking between workflows
  - Failure mode documentation
  - Self-documenting with `meta.schemaFirst: true`

**Example Structure:**
```json
{
  "$schema": "https://schemas.luh.tech/workflow-registry.schema.json",
  "meta": {
    "schemaFirst": true,
    "version": "1.0.0"
  },
  "workflows": [
    {
      "id": "validate-roadmap",
      "name": "Validate Roadmap",
      "category": "validation",
      "path": ".github/workflows/validate-roadmap.yml"
    }
  ]
}
```

### metrics-pipeline.schema.json

Robust metrics collection with failure handling and multi-destination reporting.

- **JSON Schema Draft:** Draft-2020-12
- **Use Cases:** Observability configuration, metrics routing, failure recovery
- **Template:** `templates/metrics-pipeline.json`
- **Key Features:**
  - Multiple metric sources (github, notion, slides, health, custom)
  - Multiple destinations (notion, github-issues, slack, webhook)
  - Failure handling matrix with retry strategies
  - Scheduling with cron expressions
  - Metric transformations

**Example Structure:**
```json
{
  "$schema": "https://schemas.luh.tech/metrics-pipeline.schema.json",
  "sources": [
    {
      "id": "github-ci",
      "type": "github",
      "config": {
        "repository": "luh-tech/business-tools",
        "metrics": ["test-coverage", "build-status"]
      }
    }
  ],
  "destinations": [
    {
      "id": "notion-dashboard",
      "type": "notion",
      "config": {
        "pageId": "abc123"
      }
    }
  ]
}
```

### deployment-metrics.schema.json

Watchtower auto-deployment tracking with per-environment service status.

- **JSON Schema Draft:** Draft-2020-12
- **Use Cases:** Deployment monitoring, service health tracking, success rate analysis
- **Template:** `templates/deployment-metrics.json`
- **Key Features:**
  - Per-environment tracking (staging, production)
  - Service-level deployment status
  - Watchtower integration metrics
  - Historical deployment tracking
  - Success/failure rate calculations

**Example Structure:**
```json
{
  "$schema": "https://schemas.luh.tech/deployment-metrics.schema.json",
  "environments": {
    "production": {
      "services": [
        {
          "name": "mcp-server",
          "currentVersion": "1.2.0",
          "lastDeployment": "2026-01-28T00:00:00Z",
          "status": "healthy"
        }
      ]
    }
  }
}
```

### roadmap-business.schema.json

Business roadmap data including financials, team planning, and competitive positioning.

- **JSON Schema Draft:** Draft-07
- **Use Cases:** Investor materials, business planning, service tier definitions
- **Template:** `templates/roadmap-business.json`
- **Key Features:**
  - Financial projections (revenue, runway, burn rate)
  - Team growth planning
  - Competitive analysis
  - Service tier definitions
  - Market positioning

**Example Structure:**
```json
{
  "$schema": "https://schemas.luh.tech/roadmap-business.schema.json",
  "financials": {
    "currentMRR": 0,
    "projectedARR": 500000,
    "runway": "18 months"
  },
  "team": {
    "current": 1,
    "planned": 5,
    "keyHires": ["CTO", "Sales Lead"]
  },
  "serviceTiers": [
    {
      "name": "Starter",
      "price": 499,
      "features": ["Core analytics", "5 users"]
    }
  ]
}
```

---

## Schema Adoption Checklist

For each venture adopting the new schemas:

- [ ] Copy schema to `.roadmap/schemas/` (or reference from template repo)
- [ ] Create initial JSON file from template in `.roadmap/`
- [ ] Update `$id` URN with venture name
- [ ] Populate venture-specific data
- [ ] Add validation to CI workflow
- [ ] Document in venture's README

---

## URN Identifier System

### Purpose

Enable cross-venture entity linking, bidirectional graph traversal, and portfolio-wide graph queries. Based on Ectropy V3 production patterns.

### URN Format

```
urn:luhtech:{venture}:{nodeType}:{identifier}
```

### Examples

```
urn:luhtech:ectropy:file:roadmap
urn:luhtech:ectropy:decision:d-2026-01-01-database-ha-upgrade
urn:luhtech:ectropy:service:mcp-server
urn:luhtech:jobsitecontrol:milestone:ms-hardware-v1
urn:luhtech:holdings:venture:ectropy
```

### Node Types

| Type | Description |
|------|-------------|
| `venture` | Portfolio venture |
| `file` | Roadmap file |
| `milestone` | Project milestone |
| `decision` | ADR/decision record |
| `service` | Infrastructure service |
| `evidence` | Evidence session |
| `person` | Team member or stakeholder |
| `ip-asset` | Intellectual property |
| `dependency` | Dependency record |
| `phase` | Roadmap phase |
| `task` | Deliverable/task |
| `metric` | Business metric |
| `extension` | Venture extension |
| `feature` | Feature specification (NEW) |
| `interface` | API/MCP interface (NEW) |
| `workflow` | CI/CD workflow (NEW) |

### Edge Types

| Type | Description |
|------|-------------|
| `fork` | Fork relationship (with weight) |
| `depends-on` | Dependency relationship |
| `blocks` | Blocking relationship |
| `provides` | Provider relationship |
| `consumes` | Consumer relationship |
| `synergy` | Strategic synergy |
| `supersedes` | Decision supersession |
| `references` | General reference |
| `contains` | Parent-child containment |
| `owns` | Ownership relationship |
| `implements` | Implementation relationship |
| `relates-to` | General relationship |

---

## Architecture

### Schema Hierarchy

```
TIER 0: CANONICAL SCHEMAS (Single Source of Truth)
luh-tech/schema-registry/schemas/

├── VENTURE-LEVEL (Per-venture .roadmap/ files)
│   ├── roadmap.schema.v2.json
│   ├── venture-summary.schema.json
│   ├── dependencies.schema.json
│   ├── boundaries.schema.json
│   ├── decision-log.schema.v2.json
│   ├── infrastructure-catalog.schema.json
│   ├── tech-stack.schema.json
│   ├── evidence-session.schema.json
│   ├── extensions.schema.v1.json
│   ├── feature.schema.json              ← NEW (v1.5.0)
│   ├── interfaces.schema.json           ← NEW (v1.5.0)
│   ├── workflow-registry.schema.json    ← NEW (v1.5.0)
│   ├── metrics-pipeline.schema.json     ← NEW (v1.5.0)
│   ├── deployment-metrics.schema.json   ← NEW (v1.5.0)
│   └── roadmap-business.schema.json     ← NEW (v1.5.0)
│
├── PORTFOLIO-LEVEL (Cross-venture operations)
│   ├── portfolio/workflow-registry.schema.json
│   ├── portfolio/brand.schema.json
│   ├── portfolio/portfolio.schema.json
│   ├── portfolio/ip-assets.schema.json
│   ├── portfolio/extensions-matrix.schema.v1.json
│   └── portfolio/portfolio-graph.schema.v1.json
│
├── _enums/
│   ├── luhtech-enums.schema.json
│   └── luhtech-enums.schema.v2.json
│
└── _definitions/
    ├── definitions.schema.json
    └── graph.schema.json
```

---

## File Structure Per Venture

```
{venture}/.roadmap/
├── roadmap.json                    ← Business roadmap
├── venture-summary.json            ← Investor pitch data
├── dependencies.json               ← Cross-venture links
├── boundaries.json                 ← Fork configuration
├── decision-log.json               ← Architectural decisions (v2)
├── infrastructure-catalog.json     ← Service registry
├── tech-stack.json                 ← Technology documentation
├── extensions.json                 ← Venture-specific extensions
├── roadmap-business.json           ← Business roadmap (NEW)
├── workflow-registry.json          ← CI/CD documentation (NEW)
├── metrics-pipeline.json           ← Observability config (NEW)
├── deployment-metrics.json         ← Deployment tracking (NEW)
├── features/                       ← Feature specifications (NEW)
│   └── {feature-id}/
│       ├── FEATURE.json            ← Feature spec
│       └── interfaces.json         ← API definitions
└── evidence/                       ← Evidence sessions directory
    └── ...
```

### Portfolio Operations (LuhTech-business)

```
LuhTech-business/.roadmap/
├── portfolio.json                  ← Aggregated portfolio view
├── ip-assets.json                  ← IP tracking
├── extensions-matrix.json          ← Shared extensions from all ventures
└── portfolio-graph.json            ← Portfolio-wide graph
```

---

## Validation

### CI Pipeline Integration

Add to `.github/workflows/roadmap-ci.yml`:

```yaml
- name: Validate Roadmap Files
  run: |
    # Install ajv-cli
    npm install -g ajv-cli ajv-formats
    
    # Validate core files
    npx ajv validate -s schemas/roadmap.schema.v2.json -d .roadmap/roadmap.json --spec=draft7 -c ajv-formats
    
    # Validate new schemas (v1.5.0)
    npx ajv validate -s schemas/feature.schema.json -d .roadmap/features/*/FEATURE.json --spec=draft7 -c ajv-formats
    npx ajv validate -s schemas/interfaces.schema.json -d .roadmap/features/*/interfaces.json --spec=draft7 -c ajv-formats
    npx ajv validate -s schemas/workflow-registry.schema.json -d .roadmap/workflow-registry.json --spec=draft2020 -c ajv-formats
    npx ajv validate -s schemas/metrics-pipeline.schema.json -d .roadmap/metrics-pipeline.json --spec=draft2020 -c ajv-formats
    npx ajv validate -s schemas/deployment-metrics.schema.json -d .roadmap/deployment-metrics.json --spec=draft2020 -c ajv-formats
    npx ajv validate -s schemas/roadmap-business.schema.json -d .roadmap/roadmap-business.json --spec=draft7 -c ajv-formats
```

### Local Validation

```bash
# Install ajv-cli
npm install -g ajv-cli ajv-formats

# Validate feature specification
npx ajv validate -s schemas/feature.schema.json -d .roadmap/features/decision-lifecycle/FEATURE.json --spec=draft7 -c ajv-formats

# Validate interfaces
npx ajv validate -s schemas/interfaces.schema.json -d .roadmap/features/decision-lifecycle/interfaces.json --spec=draft7 -c ajv-formats

# Validate workflow registry
npx ajv validate -s schemas/workflow-registry.schema.json -d .roadmap/workflow-registry.json --spec=draft2020 -c ajv-formats

# Validate metrics pipeline
npx ajv validate -s schemas/metrics-pipeline.schema.json -d .roadmap/metrics-pipeline.json --spec=draft2020 -c ajv-formats

# Validate deployment metrics
npx ajv validate -s schemas/deployment-metrics.schema.json -d .roadmap/deployment-metrics.json --spec=draft2020 -c ajv-formats

# Validate business roadmap
npx ajv validate -s schemas/roadmap-business.schema.json -d .roadmap/roadmap-business.json --spec=draft7 -c ajv-formats
```

---

## Changelog

### v1.5.0 (2026-01-28)
- **NEW**: `feature.schema.json` v1.0.0
  - Feature specifications with milestones and deliverables
  - Business value tracking (ROI, savings, incidents avoided)
  - Scenario-based ROI estimation
  - Graph metadata for AI navigation
  - Template: `templates/feature.json`
- **NEW**: `interfaces.schema.json` v1.0.0
  - MCP tool definitions with categories
  - REST API endpoint documentation
  - GraphQL resolver specifications
  - Event system documentation
  - Template: `templates/interfaces.json`
- **NEW**: `workflow-registry.schema.json` v1.0.0
  - GitHub Actions workflow documentation
  - Workflow categorization (ci, cd, validation, sync, monitoring)
  - Dependency tracking between workflows
  - Failure mode documentation
  - Template: `templates/workflow-registry.json`
- **NEW**: `metrics-pipeline.schema.json` v1.0.0
  - Multi-source metrics collection
  - Multi-destination reporting
  - Failure handling matrix with retry strategies
  - Template: `templates/metrics-pipeline.json`
- **NEW**: `deployment-metrics.schema.json` v1.0.0
  - Per-environment deployment tracking
  - Watchtower integration metrics
  - Service health monitoring
  - Template: `templates/deployment-metrics.json`
- **NEW**: `roadmap-business.schema.json` v1.0.0
  - Financial projections
  - Team growth planning
  - Competitive analysis
  - Service tier definitions
  - Template: `templates/roadmap-business.json`
- All 6 schemas promoted from luhtech/Ectropy flagship venture
- All schemas generalized for portfolio-wide use
- All templates validated against schemas

### v1.4.0 (2026-01-14)
- **NEW**: `roadmap.schema.v2.2.json` v2.2.0
  - Added `resources` block (compute, storage, bandwidth, physical, personnel)
  - Added `schemaChangelog` to meta for version tracking
  - Added `inheritedFrom` field for cross-venture feature inheritance
  - Added `vendorEvaluation` for vendor-agnostic features
  - Added `subdomainPattern` for multi-tenant features
  - Added `notes` field for implementation notes
  - Added new feature categories: `hardware`, `mobile`, `marketplace`
  - Added `future` status for deferred features
  - **DEPRECATED**: `financials`, `team`, `competitive` (move to roadmap-business.json)
  - Added `resourceItem` definition for infrastructure planning

### v1.3.0 (2026-01-06)
- **NEW**: `_definitions/graph.schema.json` v1.0.0
  - URN identifier pattern: `urn:luhtech:{venture}:{nodeType}:{identifier}`
  - Graph metadata with bidirectional edges (inEdges/outEdges)
  - Node type enumeration (13 types)
  - Edge type enumeration (12 types)
  - Based on Ectropy V3 production patterns
- **NEW**: `portfolio/portfolio-graph.schema.v1.json` v1.0.0
  - Portfolio-wide graph aggregation
  - Pre-computed indexes (byType, byVenture, byEdgeType, adjacency)
  - Cross-venture relationship tracking
- **UPDATED**: `_definitions/definitions.schema.json` v1.1.0
  - Added URN and graphMetadata references
  - Added $id (URN) to person and organization definitions
  - Added syncStatus for V3 compatibility

### v1.2.0 (2026-01-06)
- **NEW**: `extensions.schema.v1.json` v1.0.0
- **NEW**: `portfolio/extensions-matrix.schema.v1.json` v1.0.0

### v1.1.0 (2025-12-12)
- **NEW**: `portfolio/workflow-registry.schema.json` v1.0.0
- **UPDATED**: `infrastructure-catalog.schema.json` v1.1.0

### v1.0.0 (2025-12-11)
- Initial release with core schemas

---

## Enterprise Excellence Checkpoint

✅ Schema-first architecture (not code-first)  
✅ Single source of truth (schema-registry)  
✅ Derived from proven system (Ectropy V3 production)  
✅ Comprehensive documentation  
✅ CI validation ready  
✅ Migration path documented  
✅ Backward compatible  
✅ Cross-repo reference pattern ($ref)  
✅ Self-documenting (meta.schemaFirst)  
✅ Extension system with explicit sharing  
✅ URN identifiers for entity linking  
✅ Bidirectional graph traversal  
✅ Portfolio-wide graph queries  
✅ Feature specifications with ROI tracking (NEW)  
✅ MCP/API interface documentation (NEW)  
✅ CI/CD workflow registry (NEW)  
✅ Metrics pipeline configuration (NEW)  
✅ Deployment tracking (NEW)  
✅ Business roadmap separation (NEW)  

**No shortcuts. Enterprise excellence always.**
