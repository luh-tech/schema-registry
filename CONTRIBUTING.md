# Contributing to schema-registry

> Implementation guide for the LuhTech venture `.roadmap/` directory structure

**Version:** 1.1.0  
**Last Updated:** December 9, 2025

## Overview

The `.roadmap/` template provides a **JSON-first documentation system** that enables:

- **Automated aggregation** across the LuhTech portfolio
- **Conflict detection** for resource allocation and dependencies
- **Slide generation** for investor pitches and accelerator reporting
- **Decision tracking** for governance and audit trails
- **Fork management** for ventures inheriting from Ectropy platform

## Nomenclature Guide

Before implementing, understand the naming conventions:

| Term | Meaning | Example |
|------|---------|---------|
| **luh-tech** | GitHub organization | `github.com/luh-tech` |
| **luh-tech templates** | Canonical templates for all ventures | `schema-registry` |
| **LuhTech** | The holding company venture | LuhTechnology Ventures |
| **Ectropy** | Flagship platform (template origin) | `ectropy.ai` |

**Key Principle:** Templates are named `luh-tech-*` because they serve **all ventures**, not just Ectropy. Ectropy is the reference implementation, but the templates are portfolio-wide infrastructure.

## Directory Structure

Every venture repository should contain:

```
{venture-repo}/
├── .roadmap/
│   ├── roadmap.json              # Primary 18-month roadmap
│   ├── venture-summary.json      # Investor-ready pitch data
│   ├── decision-log.json         # Key decisions with context
│   ├── dependencies.json         # Cross-venture dependencies
│   ├── boundaries.json           # Fork inheritance (forked repos only)
│   └── metrics/
│       ├── targets.json          # Success criteria definitions
│       └── {YYYY-MM}.json        # Monthly metric snapshots
│
├── docs/
│   ├── ROADMAP.md               # Human-readable (auto-generated)
│   └── VENTURE-SUMMARY.md       # One-pager (auto-generated)
│
└── .github/
    └── workflows/
        └── roadmap-sync.yml     # CI: validate + notify aggregator
```

## Schema Files

### 1. roadmap.json (Required)

Core roadmap with venture metadata, pitch, quarters, financials, team, and milestones.

**Schema**: `schemas/roadmap.schema.json`

**Key sections:**
- `identity` - Venture ID, name, type, architecture
- `pitch` - Tagline, problem, solution, market
- `quarters` - 6 quarters of objectives and milestones
- `financials` - Funding stage, runway, burn rate
- `team` - Current headcount and hiring plan

### 2. venture-summary.json (Required)

Investor-ready summary integrating with slide-generator.

**Schema**: `schemas/venture-summary.schema.json`

**Used by:**
- slide-generator for pitch deck automation
- Portfolio dashboards
- Accelerator reporting

### 3. decision-log.json (Required)

Structured decisions with context, alternatives, and rationale.

**Schema**: `schemas/decision-log.schema.json`

**Categories:**
- `architecture` - System design decisions
- `infrastructure` - Deployment and ops
- `api-design` - API contracts and versioning
- `governance` - Process and policy
- `business` - Strategy and partnerships
- `product` - Feature prioritization
- `team` - Hiring and organization
- `funding` - Investment and runway
- `legal` - Compliance and IP

### 4. dependencies.json (Required)

Cross-venture dependency tracking.

**Schema**: `schemas/dependencies.schema.json`

**Types:**
- `venture` - Depends on another venture's capability
- `template` - Uses shared template infrastructure
- `infrastructure` - Shared hosting/services
- `api` - API integration
- `data` - Data sharing
- `team` - Shared personnel
- `external` - Third-party dependencies

### 5. boundaries.json (Forked Repos Only)

Fork tracking with inherited/removed/added paths and upstream sync config.

**Schema**: `schemas/boundaries.schema.json`

**Required for:**
- JobsiteControl (forking Feb 2026)
- Qullqa (forking Mar 2026)
- Hilja (forking Apr 2026)

## Validation

### Local Validation

```bash
# Install ajv-cli
npm install -g ajv-cli

# Validate roadmap
ajv validate -s schemas/roadmap.schema.json -d .roadmap/roadmap.json

# Validate all files
for schema in roadmap venture-summary decision-log dependencies; do
  ajv validate -s schemas/${schema}.schema.json -d .roadmap/${schema}.json
done
```

### CI Validation

The `roadmap-sync.yml` workflow runs on every push to `.roadmap/`:

1. Validates JSON against schemas
2. Checks for required files
3. Notifies roadmap-aggregator of changes
4. Generates updated Markdown docs

## Integration

### roadmap-aggregator

```bash
# Pull all venture roadmaps
roadmap pull --all

# Validate specific venture
roadmap validate --venture ectropy

# Analyze cross-venture conflicts
roadmap analyze --conflicts

# Generate portfolio view
roadmap generate --format markdown
```

### slide-generator

Uses `venture-summary.json` for automated pitch deck generation:

```bash
# Generate investor deck
slide-generator generate --venture ectropy --type investor

# Uses brand config from Notion Venture Brands database
```

### n8n Workflows

Automated triggers on:
- `.roadmap/` file changes
- Gate milestone completion
- Dependency status updates
- Monthly metric collection due dates

## Best Practices

### 1. JSON as Source of Truth

- **Never edit generated Markdown** - Always update JSON
- Generated docs are for human reading only
- CI regenerates docs on every change

### 2. Quarterly Cadence

- Start of quarter: Update objectives and key results
- End of quarter: Record actual vs. planned
- Major milestones: Document as they complete

### 3. Decision Logging

- Log all architectural decisions
- Include alternatives considered
- Document rationale for future reference
- Link to relevant PRs or issues

### 4. Cross-Venture Coordination

- Check conflicts before major commitments
- Document dependencies from both sides
- Use `dependencies.json` for hard dependencies
- Use `decision-log.json` for coordination decisions

### 5. Fork Management

- Create `boundaries.json` immediately upon forking
- Document which paths are inherited vs. customized
- Configure upstream sync preferences
- Track divergence over time

## Migration Guide

### For New Ventures

1. **Create directory structure:**
   ```bash
   mkdir -p .roadmap/metrics
   ```

2. **Copy schemas for reference:**
   ```bash
   cp -r path/to/schema-registry/schemas .roadmap/
   ```

3. **Initialize from examples:**
   ```bash
   cp path/to/schema-registry/examples/*.json .roadmap/
   ```

4. **Customize for your venture:**
   - Update identity section with venture details
   - Populate pitch content
   - Define quarterly objectives
   - Document initial decisions

5. **Set up CI:**
   ```bash
   mkdir -p .github/workflows
   cp path/to/schema-registry/.github/workflows/roadmap-sync.yml .github/workflows/
   ```

### For Existing Ventures

1. Audit existing documentation (Notion, Google Docs)
2. Map content to schema structure
3. Migrate content to JSON files
4. Validate against schemas
5. Archive or redirect old documentation

## Venture Implementation Status

| Venture | `.roadmap/` | Validated | CI | Notes |
|---------|-------------|-----------|-----|-------|
| LuhTech (business-tools) | ✅ | ✅ | ⏳ | Reference implementation |
| Ectropy | ⏳ | — | — | Week 2 (Dec 16-20) |
| Raizal | ⏳ | — | — | After Ectropy |
| Replique | ⏳ | — | — | After Ectropy |
| JobsiteControl | ⏳ | — | — | Fork in Feb 2026 |
| Qullqa | ⏳ | — | — | Fork in Mar 2026 |
| Hilja | ⏳ | — | — | Fork in Apr 2026 |
| Viiva | ⏳ | — | — | R&D phase |

---

*Template maintained by LuhTech Enterprise Infrastructure*  
*Part of the luh-tech template system*
