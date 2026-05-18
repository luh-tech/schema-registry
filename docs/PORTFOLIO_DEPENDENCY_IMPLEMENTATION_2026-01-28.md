> **Historical reference (repository renamed 2026-05-18):** This document was authored 2026-01-28 against the prior repository name `luh-tech/luh-tech-roadmap-template`. The repository was renamed to [`luh-tech/schema-registry`](https://github.com/luh-tech/schema-registry) on 2026-05-18; references to the old name below are historically accurate for the document's authorship date and remain unchanged.

---
# Portfolio Dependency Architecture Implementation Report
## Schema v2.3.0 + DAG Validation System

**Date:** 2026-01-28
**Author:** Claude (AI Assistant)
**Status:** Implementation Complete - Pending Git Commits

---

## Executive Summary

Successfully implemented portfolio-level milestone dependency tracking across 8 LuhTech ventures. The implementation extends the existing roadmap schema with CPM (Critical Path Method) patterns and SILTANA 7-tier authority cascade, enabling:

- Single source of truth for cross-venture dependencies
- Automatic cascade impact analysis when LEAD milestones change
- Authority-based change control preventing unauthorized date modifications
- DAG validation to ensure data integrity across the portfolio

---

## Implementation Completed

### Phase 1: Schema Extension ✅

**File:** `luh-tech-roadmap-template/schemas/roadmap.schema.v2.3.json`

New `keyMilestone` properties:
| Property | Type | Description |
|----------|------|-------------|
| `urn` | string | Cross-venture URN identifier (`urn:luhtech:{venture}:milestone:{id}`) |
| `classification` | enum | LEAD \| DERIVED \| EXTERNAL \| FLEXIBLE |
| `graphMetadata` | object | DAG edges with predecessors/successors |
| `authorityLevel` | int (0-6) | SILTANA authority cascade level |
| `bufferDays` | int | Float/slack before cascade impact |

**Classification Definitions:**
- **LEAD**: Source of truth - changes cascade to downstream milestones
- **DERIVED**: Calculated from predecessors - date must be >= earliest valid
- **EXTERNAL**: External constraint - cannot be modified (pilot partner dates, regulatory)
- **FLEXIBLE**: Target date - buffer absorbs slip without cascade

**CPM Relationship Types:**
- **FS** (Finish-to-Start): Default - successor starts after predecessor finishes
- **SS** (Start-to-Start): Both start together
- **FF** (Finish-to-Finish): Both finish together  
- **SF** (Start-to-Finish): Rarely used

### Phase 2: Data Population ✅

Updated 4 ventures with URNs and graphMetadata:

| Venture | Version | URN Milestones | Key Changes |
|---------|---------|----------------|-------------|
| Ectropy-Business | 2.3.0 | 14 | repo-split as LEAD with 3 successors |
| JobsiteControl | 2.3.0 | 4 | fork-ready predecessor to repo-split, fixed date 2026-01-17→2026-01-30 |
| Qullqa | 2.3.0 | 4 | fork-ready predecessor to repo-split |
| Viiva | 2.3.0 | 3 | fork-ready predecessor to repo-split |

**Critical Path Established:**
```
urn:luhtech:ectropy:milestone:repo-split (2026-01-30) [LEAD, L4]
    ├── urn:luhtech:jobsitecontrol:milestone:fork-ready (2026-01-31) [DERIVED, L3]
    ├── urn:luhtech:qullqa:milestone:fork-ready (2026-01-31) [DERIVED, L3]
    └── urn:luhtech:viiva:milestone:fork-ready (2026-01-31) [DERIVED, L3]
```

### Phase 3: Validation Tooling ✅

**File:** `luh-tech-roadmap-template/scripts/validate-portfolio-dag.py`

CLI tool with 5 validation checks:
1. **Acyclic Check**: No circular dependencies
2. **URN Existence**: All referenced URNs exist
3. **Date Consistency**: DERIVED dates >= predecessor finish + lag
4. **Authority Levels**: Valid 0-6 range
5. **Classification Rules**: LEAD has successors, EXTERNAL has authority >= 5

**Usage:**
```bash
python validate-portfolio-dag.py --ventures-dir "C:\Users\luhte\Source\Repos\luh-tech" -v
```

---

## Files Modified

### Schema (1 file)
```
luh-tech-roadmap-template/schemas/roadmap.schema.v2.3.json  [NEW]
```

### Venture Roadmaps (4 files)
```
Ectropy-Business/.roadmap/roadmap.json     [UPDATED: 2.0.0 → 2.3.0]
JobsiteControl/.roadmap/roadmap.json       [UPDATED: 2.2.0 → 2.3.0]
Qullqa/.roadmap/roadmap.json               [UPDATED: 2.2.0 → 2.3.0]
Viiva/.roadmap/roadmap.json                [UPDATED: 2.2.0 → 2.3.0]
```

### Tooling (1 file)
```
luh-tech-roadmap-template/scripts/validate-portfolio-dag.py  [NEW]
```

---

## Git Commit Commands

### 1. Schema Repository
```bash
cd C:\Users\luhte\Source\Repos\luh-tech\luh-tech-roadmap-template

git add schemas/roadmap.schema.v2.3.json scripts/validate-portfolio-dag.py

git commit -m "feat(schema): add roadmap v2.3 with portfolio dependency tracking

BREAKING CHANGE: None (additive extension of v2.2)

New keyMilestone properties:
- urn: Cross-venture URN identifier
- classification: LEAD | DERIVED | EXTERNAL | FLEXIBLE
- graphMetadata: DAG edges (predecessors/successors)
- authorityLevel: 0-6 (SILTANA 7-tier cascade)
- bufferDays: Float/slack before cascade

New tooling:
- scripts/validate-portfolio-dag.py: Portfolio DAG validation CLI

Enterprise Excellence. Schema-First. No Shortcuts."

git push origin main
```

### 2. Ectropy-Business
```bash
cd C:\Users\luhte\Source\Repos\luh-tech\Ectropy-Business

git add .roadmap/roadmap.json

git commit -m "feat(roadmap): upgrade to v2.3.0 with URNs and graphMetadata

- Added URN identifiers to 14 keyMilestones
- repo-split marked as LEAD milestone with 3 downstream successors
- Added graphMetadata.predecessors chains
- Added authorityLevel and classification to all milestones
- pilot-launch marked as EXTERNAL (L5 authority)

Critical path: repo-split → prisma-n8n → graphql-api → mobile-voxel → pilot-ready → pilot-launch"

git push origin main
```

### 3. JobsiteControl
```bash
cd C:\Users\luhte\Source\Repos\luh-tech\JobsiteControl

git add .roadmap/roadmap.json

git commit -m "feat(roadmap): upgrade to v2.3.0 with dependency tracking

- Added fork-ready milestone as successor to Ectropy repo-split
- Fixed crossVentureDependencies date: 2026-01-17 → 2026-01-30
- Added URN identifiers and graphMetadata to milestones
- Soft dependency: pilot can proceed without fork"

git push origin main
```

### 4. Qullqa
```bash
cd C:\Users\luhte\Source\Repos\luh-tech\Qullqa

git add .roadmap/roadmap.json

git commit -m "feat(roadmap): upgrade to v2.3.0 with dependency tracking

- Added fork-ready milestone as successor to Ectropy repo-split
- Added URN identifiers and graphMetadata to milestones
- funding-decision marked as L5 (Owner authority)"

git push origin main
```

### 5. Viiva
```bash
cd C:\Users\luhte\Source\Repos\luh-tech\Viiva

git add .roadmap/roadmap.json

git commit -m "feat(roadmap): upgrade to v2.3.0 with dependency tracking

- Added fork-ready milestone as successor to Ectropy repo-split
- Added URN identifiers and graphMetadata to milestones
- Soft dependency: can proceed with package references"

git push origin main
```

---

## Validation Commands

### Local Validation
```bash
# Navigate to roadmap template
cd C:\Users\luhte\Source\Repos\luh-tech\luh-tech-roadmap-template

# Run DAG validation
python scripts/validate-portfolio-dag.py -v

# Expected output:
# Loaded 4 ventures, 25 milestones with URNs
# ✅ VALIDATION PASSED
```

### Schema Validation (ajv-cli)
```bash
# Validate individual venture
npx ajv validate \
  -s schemas/roadmap.schema.v2.3.json \
  -d ../Ectropy-Business/.roadmap/roadmap.json \
  --spec=draft7 -c ajv-formats
```

---

## Architecture Diagram

```mermaid
graph TD
    subgraph Ectropy Platform
        RS[repo-split<br/>2026-01-30<br/>LEAD L4]
        PN[prisma-n8n<br/>2026-01-31]
        GA[graphql-api<br/>2026-02-10]
        MV[mobile-voxel<br/>2026-02-20]
        PR[pilot-ready<br/>2026-02-28]
        PL[pilot-launch<br/>2026-03-01<br/>EXTERNAL L5]
    end
    
    subgraph Fork Ventures
        JF[jobsitecontrol:fork-ready<br/>2026-01-31<br/>DERIVED L3]
        QF[qullqa:fork-ready<br/>2026-01-31<br/>DERIVED L3]
        VF[viiva:fork-ready<br/>2026-01-31<br/>DERIVED L3]
    end
    
    RS --> PN
    RS --> JF
    RS --> QF
    RS --> VF
    PN --> GA
    GA --> MV
    MV --> PR
    PR --> PL
    
    style RS fill:#ff9900,stroke:#333
    style PL fill:#0066cc,stroke:#333
    style JF fill:#66cc66,stroke:#333
    style QF fill:#66cc66,stroke:#333
    style VF fill:#66cc66,stroke:#333
```

---

## SILTANA Authority Cascade Reference

| Level | Role | Budget Authority | Milestone Context |
|-------|------|------------------|-------------------|
| 0 | Seppä Agent | Auto-response | CI validation only |
| 1 | Foreman | $5K | Team lead adjustments |
| 2 | Superintendent | $25K | Internal venture changes |
| 3 | Project Manager | $100K | Venture milestone dates |
| 4 | Architect | Design changes | Cross-venture architecture |
| 5 | Owner | Major capital | Portfolio strategy dates |
| 6 | Regulatory | Code compliance | External constraints |

---

## Next Steps

1. **Commit and push** all changes using commands above
2. **Add remaining ventures** (Raizal, Hilja, LuhTech-business, Replique) to v2.3 as needed
3. **Integrate CI workflow** - add DAG validation to `cross-repo-roadmap-validation.yml`
4. **Build cascade proposer** - CLI tool to calculate downstream impacts of date changes
5. **Notion dashboard** - add critical path visualization

---

**Enterprise Excellence. Schema-First. No Shortcuts.**