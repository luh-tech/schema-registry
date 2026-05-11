# PM (Project Management) Schemas

**Version:** 3.0.0  
**Last Updated:** 2026-01-06  
**Maintainer:** LuhTech Enterprise Infrastructure

## Overview

This directory contains JSON schemas for the Ectropy PM Core system - a voxel-based project management platform for construction. These schemas enable:

- **Voxel-attached decisions** - Decisions linked to 3D spatial locations
- **7-tier authority cascade** - Escalation from Field Worker to Regulatory
- **Consequence tracking** - Downstream effects of decisions
- **Schedule proposals** - 10-day look-ahead modifications
- **Inspection management** - Field inspections and regulatory approvals

## Schema Files

| Schema | Description | ID Pattern |
|--------|-------------|------------|
| `decision.schema.json` | PM decisions with voxel attachment | `DEC-YYYY-NNNN` |
| `voxel.schema.json` | 3D spatial containers | `VOX-{LOCATION}` |
| `consequence.schema.json` | Decision outcomes | `CONSQ-YYYY-NNNN` |
| `authority-level.schema.json` | 7-tier authority cascade | `pm-level-N` |
| `inspection.schema.json` | Field inspection records | `INSP-YYYY-NNNN` |
| `schedule-proposal.schema.json` | Schedule modifications | `PROP-YYYY-NNNN` |
| `participant.schema.json` | Project stakeholders | `{slug}` |

## URN Pattern

All PM entities follow the LuhTech URN pattern:

```
urn:luhtech:{project}:{nodeType}:{identifier}
```

**Examples:**
```
urn:luhtech:project-alpha:voxel:VOX-L2-MECH-047
urn:luhtech:project-alpha:pm-decision:DEC-2026-0001
urn:luhtech:project-alpha:consequence:CONSQ-2026-0001
urn:luhtech:project-alpha:inspection:INSP-2026-0001
urn:luhtech:project-alpha:participant:john-doe-pm
urn:luhtech:ectropy:authority-level:pm-level-3
```

## Authority Cascade

| Level | Name | Budget Limit | Variance | Schedule |
|-------|------|--------------|----------|----------|
| 0 | FIELD | $0 | 0" | 0 days |
| 1 | FOREMAN | $500 | 1/8" | 4 hours |
| 2 | SUPERINTENDENT | $5,000 | 1/4" | 1 day |
| 3 | PM | $50,000 | 1/2" | 1 week |
| 4 | ARCHITECT | Design | Visible | 2 weeks |
| 5 | OWNER | Project | Major | 1 month |
| 6 | REGULATORY | Code | Safety | Any |

## Graph Metadata

All entities include `graphMetadata` for bidirectional graph traversal:

```json
{
  "graphMetadata": {
    "inEdges": ["urn:luhtech:..."],
    "outEdges": ["urn:luhtech:..."],
    "edges": [
      {
        "from": "urn:luhtech:...",
        "to": "urn:luhtech:...",
        "type": "contains",
        "label": "Decision attached to voxel"
      }
    ]
  }
}
```

## PM-Specific Edge Types

| Edge Type | From | To | Description |
|-----------|------|-----|-------------|
| `contains` | Voxel | Decision | Decision attached to location |
| `triggers` | Decision | Consequence | Decision causes outcome |
| `proposes` | Decision | Schedule-Proposal | Decision requests change |
| `escalates-to` | Decision | Decision | Authority escalation |
| `validates` | Inspection | Decision | Inspection confirms decision |
| `authored-by` | Decision | Participant | Decision maker |
| `approved-by` | Decision | Participant | Approval authority |
| `affects` | Consequence | Voxel | Consequence impacts area |

## Related Schemas

- `_definitions/graph.schema.json` - URN and graph definitions
- `_enums/luhtech-enums.schema.v3.json` - PM-specific enumerations

## Usage Example

```json
{
  "$id": "urn:luhtech:project-alpha:pm-decision:DEC-2026-0001",
  "$schema": "https://schemas.luh.tech/pm/decision.schema.json",
  "schemaVersion": "3.0.0",
  "decisionId": "DEC-2026-0001",
  "title": "HVAC Duct Routing Modification",
  "type": "APPROVAL",
  "status": "APPROVED",
  "authorityLevel": {
    "required": 3,
    "current": 3
  },
  "voxelRef": "urn:luhtech:project-alpha:voxel:VOX-L2-MECH-047",
  "graphMetadata": {
    "inEdges": ["urn:luhtech:project-alpha:voxel:VOX-L2-MECH-047"],
    "outEdges": ["urn:luhtech:project-alpha:consequence:CONSQ-2026-0001"]
  }
}
```

## Validation

Validate PM schema files using:

```bash
graph-tools validate .roadmap/projects/ --schema pm
```

## Changelog

### v3.0.0 (2026-01-06)
- Initial release with V3 graph URN structure
- 7 core PM schemas
- Full graphMetadata support
- Authority cascade with auto-escalation rules
