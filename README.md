# luh-tech-roadmap-template

> JSON-first documentation system for LuhTech portfolio ventures

**Version:** 1.2.0  
**Last Updated:** December 9, 2025

## Overview

This template provides the standard `.roadmap/` directory structure for **all LuhTech ventures**. It enables:

- **Automated aggregation** - Portfolio-wide visibility via roadmap-aggregator CLI
- **Conflict detection** - Resource allocation and cross-venture dependency conflicts
- **Slide generation** - Investor-ready decks from venture-summary.json
- **Decision tracking** - Structured governance and audit trails
- **Fork management** - Track inheritance for platform forks (JobsiteControl, Qullqa, Hilja)

## Nomenclature

> **Important:** This is a **luh-tech template**, not an "ectropy template."

| Term | Meaning |
|------|---------|
| **luh-tech templates** | Canonical templates for all LuhTech portfolio ventures |
| **luh-tech** | GitHub organization containing shared infrastructure |
| **LuhTech** | The holding company venture (LuhTechnology Ventures) |
| **Ectropy** | The flagship platform venture (first to implement templates) |

Templates are developed and validated on Ectropy first, then propagated to all ventures. The naming `luh-tech-*` indicates these serve the entire portfolio, not just Ectropy.

## Quick Start

### 1. Create Directory Structure

```bash
mkdir -p .roadmap/metrics
```

### 2. Initialize Core Files

```bash
# Copy schemas for validation
cp -r path/to/luh-tech-roadmap-template/schemas .roadmap/

# Create from examples
cp path/to/luh-tech-roadmap-template/examples/roadmap.json .roadmap/
```

### 3. Customize for Your Venture

Edit `.roadmap/roadmap.json` with your venture's:
- Identity (id, name, type, architecture)
- Pitch content
- Quarterly roadmap
- Financials and team

### 4. Set Up CI Validation

```bash
cp path/to/luh-tech-roadmap-template/.github/workflows/roadmap-sync.yml .github/workflows/
```

## Schemas

### Roadmap Schema Versions

| Schema | Version | Purpose | Recommended |
|--------|---------|---------|-------------|
| `roadmap.schema.v2.json` | 2.0 | Full venture roadmap with meta, advanced features | ✅ **Use this** |
| `roadmap.schema.json` | 1.0 | Simplified roadmap (backwards compatible) | Legacy |

**Use v2 for new ventures.** The v2 schema matches the battle-tested format used across 6 existing venture roadmaps with support for:
- `meta` block (ventureId, ventureName, author, lastUpdated)
- `venture.platformProgress` and `currentPhase`
- `quarter.theme` for longer descriptions
- `advancedFeatures` (AR, robotics roadmaps)
- `competitive` positioning (competitors, moats)

### All Schemas

| Schema | Purpose | Required |
|--------|---------|----------|
| `roadmap.schema.v2.json` | 18-month venture roadmap (recommended) | Yes |
| `roadmap.schema.json` | Legacy roadmap format | No (v1 compat) |
| `venture-summary.schema.json` | Investor-ready pitch data | Yes |
| `decision-log.schema.json` | Decision tracking | Yes |
| `dependencies.schema.json` | Cross-venture dependencies | Yes |
| `boundaries.schema.json` | Fork tracking | Only for forks |
| `patent/*.schema.json` | Patent portfolio infrastructure (SBPA family — 7 schemas) | No (LuhTech IP only) |

## Directory Structure

```
.roadmap/
├── roadmap.json              # Primary roadmap (required)
├── venture-summary.json      # Pitch data (required)
├── decision-log.json         # Decisions (required)
├── dependencies.json         # Dependencies (required)
├── boundaries.json           # Fork tracking (if forked)
└── metrics/
    ├── targets.json          # Success criteria
    └── 2025-12.json          # Monthly snapshots
```

## Integration

### roadmap-aggregator

```bash
# Validate your roadmap
roadmap validate --venture your-venture

# Generate portfolio view
roadmap generate --format markdown
```

### slide-generator

Your `venture-summary.json` feeds directly into automated pitch deck generation with proper brand assets.

### n8n Workflows

Automated triggers for:
- Gate milestone notifications
- Dependency status updates
- Monthly metric collection

## Portfolio Ventures

| Venture | Type | Architecture | Status | Fork Source |
|---------|------|--------------|--------|-------------|
| Ectropy | Platform | Cloud-First | Active | — |
| JobsiteControl | Hardware | Edge-First | Active | Ectropy (Feb 2026) |
| Qullqa | SaaS | Cloud-First | Active | Ectropy (Mar 2026) |
| Hilja | Hardware | Edge-First | Active | Ectropy (Apr 2026) |
| Replique | API | API-Only | Active | — |
| Raizal | Marketplace | Cloud-First | Active | — |
| Viiva | Hardware | Edge-First | R&D | — |
| LuhTech | Platform | Hybrid | Active | — |

## Template Family

This template is part of the **luh-tech template system**:

| Template | Purpose | Status |
|----------|---------|--------|
| `luh-tech-roadmap-template` | Roadmap & documentation | ✅ Complete |
| `luh-tech-mcp-template` | Node.js MCP server | ⏳ Planned |
| `luh-tech-mcp-template-python` | Python MCP server | ⏳ Planned |
| `luh-tech-business-template` | CRM, n8n, billing | ⏳ Planned |

## Documentation

- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Complete implementation guide
- **[examples/](./examples/)** - Sample JSON files
- **[schemas/](./schemas/)** - JSON Schema definitions

## License

Proprietary - LuhTechnology Ventures

---

*Part of LuhTech Enterprise Infrastructure*
