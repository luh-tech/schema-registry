> **Historical reference (repository renamed 2026-05-18):** This document was authored 2026-01-28 against the prior repository name `luh-tech/luh-tech-roadmap-template`. The repository was renamed to [`luh-tech/schema-registry`](https://github.com/luh-tech/schema-registry) on 2026-05-18; references to the old name below are historically accurate for the document's authorship date and remain unchanged.

---
# Next Agent Handoff: Portfolio DAG Integration & Venture Review
**Date:** 2026-01-28
**Phase:** Schema v2.3 Implementation Complete → DAG CI Integration → Venture Review

---

## LuhTech Holdings Overview

**Entity:** LuhTech Holdings - Construction technology portfolio company
**Founder/CEO:** Erik Luhtala
**Core Principle:** *Enterprise Excellence. Schema-First. No Shortcuts.*

### Portfolio (8 Ventures)

| Venture | Type | Status | Fork Parent | Code Reuse |
|---------|------|--------|-------------|------------|
| **Ectropy** | Platform | Active (65%) | — | Source |
| **JobsiteControl** | Hardware+SaaS | Planning | Ectropy | 60% |
| **Qullqa** | SaaS | Planning | Ectropy | 65% |
| **Viiva** | SaaS | Planning | Ectropy | 70% |
| **Hilja** | Hardware | Concept | JobsiteControl | 80% |
| **Raizal** | Marketplace | Planning | — | 40% |
| **Replique** | Research | Concept | — | 30% |
| **LuhTech-business** | Holdings Ops | Active | — | — |

### GitHub Organizations
- `luhtech` - Personal/legacy
- `luh-tech` - LuhTech Holdings (8 ventures) ← PRIMARY
- `ectropy-ai` - Future public org (post repo-split)

---

## Current State

### Just Completed: Schema v2.3.0 + DAG Validation

**New Schema Extensions** (`roadmap.schema.v2.3.json`):
```json
{
  "keyMilestone": {
    "urn": "urn:luhtech:{venture}:milestone:{id}",
    "classification": "LEAD | DERIVED | EXTERNAL | FLEXIBLE",
    "graphMetadata": {
      "predecessors": [{"milestoneUrn": "...", "relationshipType": "FS", "lagDays": 0, "blocking": true}],
      "successors": ["urn:luhtech:..."]
    },
    "authorityLevel": 0-6,
    "bufferDays": 0
  }
}
```

**SILTANA 7-Tier Authority Cascade:**
| Level | Role | Milestone Authority |
|-------|------|---------------------|
| 0 | Seppä Agent | CI validation only |
| 1 | Foreman | Team adjustments |
| 2 | Superintendent | Internal changes |
| 3 | Project Manager | Venture milestones |
| 4 | Architect | Cross-venture architecture |
| 5 | Owner | Portfolio strategy |
| 6 | Regulatory | External constraints |

**Validation Status:**
```
$ python scripts/validate-portfolio-dag.py -v
Loaded 8 ventures, 25 milestones with URNs
Milestones: 25 | Ventures: 4
Errors: 0 | Warnings: 0
✅ VALIDATION PASSED
```

**Active Dependency Graph:**
```
urn:luhtech:ectropy:milestone:repo-split (2026-01-30) [LEAD, L4]
    ├── urn:luhtech:jobsitecontrol:milestone:fork-ready (2026-01-31) [DERIVED]
    ├── urn:luhtech:qullqa:milestone:fork-ready (2026-01-31) [DERIVED]
    └── urn:luhtech:viiva:milestone:fork-ready (2026-01-31) [DERIVED]
```

### Ventures with URNs (v2.3.0)
- ✅ Ectropy-Business (14 milestones)
- ✅ JobsiteControl (4 milestones)
- ✅ Qullqa (4 milestones)
- ✅ Viiva (3 milestones)

### Ventures Pending URN Migration
- ⏳ Raizal (2 milestones, 0 URNs)
- ⏳ Hilja (1 milestone, 0 URNs)
- ⏳ LuhTech-business (4 milestones, 0 URNs)
- ⏳ Replique (1 milestone, 0 URNs)

---

## Critical Path & Dates

| Milestone | Date | Classification | Authority |
|-----------|------|----------------|-----------|
| Ectropy repo-split | 2026-01-30 | LEAD | L4 |
| Fork ventures ready | 2026-01-31 | DERIVED | L3 |
| Canadian Pilot Launch | 2026-03-01 | EXTERNAL | L5 |
| Pilot Validation | 2026-05-31 | FLEXIBLE | L4 |
| Pre-Seed Close | 2026-06-15 | FLEXIBLE | L5 |

---

## Next Steps (Priority Order)

### Phase 1: CI Integration (This Session)
1. **Add DAG validation to CI workflow**
   - File: `luh-tech-roadmap-template/.github/workflows/cross-repo-roadmap-validation.yml`
   - Add step: `python scripts/validate-portfolio-dag.py --json`
   - Fail CI if DAG errors detected

2. **Build cascade proposer CLI**
   - File: `scripts/propose-cascade-update.py`
   - Input: milestone URN + new date
   - Output: JSON proposal of all downstream impacts
   - Use for PR comment generation

### Phase 2: Complete URN Migration
3. **Upgrade remaining ventures to v2.3.0**
   - Raizal: Add URNs to 2 milestones
   - Hilja: Add URNs to 1 milestone, add predecessor to JobsiteControl
   - LuhTech-business: Add URNs to 4 milestones
   - Replique: Add URNs to 1 milestone

### Phase 3: Venture-by-Venture Review
4. **Resume systematic venture review**
   - Last completed: Viiva truth-up (2026-01-28)
   - Review each venture roadmap for:
     - Accurate status and metrics
     - Proper milestone dependencies
     - Realistic timelines
     - No fabricated data

---

## Key Files & Locations

```
luh-tech/
├── luh-tech-roadmap-template/
│   ├── schemas/
│   │   └── roadmap.schema.v2.3.json          # NEW: DAG schema
│   ├── scripts/
│   │   └── validate-portfolio-dag.py         # NEW: Validation CLI
│   └── docs/
│       └── PORTFOLIO_DEPENDENCY_IMPLEMENTATION_2026-01-28.md
├── Ectropy-Business/.roadmap/roadmap.json    # v2.3.0 with 14 URNs
├── JobsiteControl/.roadmap/roadmap.json      # v2.3.0 with 4 URNs
├── Qullqa/.roadmap/roadmap.json              # v2.3.0 with 4 URNs
├── Viiva/.roadmap/roadmap.json               # v2.3.0 with 3 URNs
├── Raizal/.roadmap/roadmap.json              # v2.2.0 - needs URNs
├── Hilja/.roadmap/roadmap.json               # v2.2.0 - needs URNs
├── LuhTech-business/.roadmap/roadmap.json    # v2.2.0 - needs URNs
└── Replique/.roadmap/roadmap.json            # v2.2.0 - needs URNs
```

---

## Validation Commands

```bash
# DAG validation (run from luh-tech-roadmap-template)
python scripts/validate-portfolio-dag.py -v

# Schema validation (single venture)
npx ajv validate \
  -s schemas/roadmap.schema.v2.3.json \
  -d ../Ectropy-Business/.roadmap/roadmap.json \
  --spec=draft7 -c ajv-formats

# All ventures schema check
for v in Ectropy-Business JobsiteControl Qullqa Viiva; do
  npx ajv validate -s schemas/roadmap.schema.v2.3.json -d ../$v/.roadmap/roadmap.json --spec=draft7 -c ajv-formats
done
```

---

## Constraints & Principles

1. **Schema-First**: All changes start with schema definition
2. **No Shortcuts**: No quick fixes - implement enterprise-grade solutions
3. **URN Pattern**: `urn:luhtech:{venture}:milestone:{identifier}`
4. **Authority Cascade**: Changes require appropriate authority level
5. **Backward Compatibility**: v2.3 extends v2.2 - no breaking changes
6. **Documentation**: Every change documented in changelogs

---

## Session Objective

**Primary Goal:** Fully integrate DAG validation into CI/CD and complete URN migration across all 8 ventures.

**Success Criteria:**
1. CI workflow runs DAG validation on every PR
2. All 8 ventures upgraded to v2.3.0 with URNs
3. Cross-venture dependencies properly linked
4. Cascade proposer operational for date change analysis

**Then:** Resume venture-by-venture review starting with Raizal.

---

*Enterprise Excellence. Schema-First. No Shortcuts.*