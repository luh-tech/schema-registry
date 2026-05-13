# GitHub Actions CI/CD Infrastructure

> Centralized validation pipelines for LuhTech venture roadmaps

**Version:** 1.0.0  
**Deployed:** December 9, 2025

---

## Overview

This repository provides **reusable GitHub Actions workflows** that all LuhTech ventures call to validate their `.roadmap/` files. This ensures:

- **Single source of truth** for validation logic
- **Consistent enforcement** across all 8 ventures
- **Easy updates** - change once, all ventures benefit
- **Minimal venture configuration** - ~25 lines of YAML per venture

## Architecture

```
schema-registry/
├── .github/
│   └── workflows/
│       └── roadmap-validate.yml   ← REUSABLE WORKFLOW
└── schemas/                        ← CANONICAL SCHEMAS

{venture-repo}/
└── .github/
    └── workflows/
        └── roadmap-ci.yml         ← CALLER WORKFLOW (~25 lines)
```

## Reusable Workflow

### Location

```
luh-tech/schema-registry/.github/workflows/roadmap-validate.yml
```

### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `venture-id` | string | ✅ | - | Venture identifier (e.g., `hilja`) |
| `schema-version` | string | ❌ | `v2` | Schema version to validate against |
| `fail-on-warning` | boolean | ❌ | `false` | Whether warnings fail the build |
| `generate-report` | boolean | ❌ | `true` | Generate validation report artifact |

### Outputs

| Output | Description |
|--------|-------------|
| `validation-result` | `pass` or `fail` |
| `files-validated` | Count of files validated |

### What It Validates

| File | Required | Schema |
|------|----------|--------|
| `roadmap.json` | ✅ Yes | `roadmap.schema.v2.json` |
| `venture-summary.json` | ✅ Yes | `venture-summary.schema.json` |
| `decision-log.json` | ❌ No | `decision-log.schema.json` |
| `dependencies.json` | ❌ No | `dependencies.schema.json` |
| `boundaries.json` | ❌ No | `boundaries.schema.json` |

## Caller Workflow Template

Copy this to your venture's `.github/workflows/roadmap-ci.yml`:

```yaml
name: Roadmap CI

on:
  push:
    branches: [main]
    paths:
      - '.roadmap/**'
      - 'docs/ROADMAP.md'
      - 'docs/VENTURE-SUMMARY.md'
  pull_request:
    branches: [main]
    paths:
      - '.roadmap/**'
  workflow_dispatch:

jobs:
  validate:
    name: Validate Roadmap
    uses: luh-tech/schema-registry/.github/workflows/roadmap-validate.yml@v1
    with:
      venture-id: 'YOUR_VENTURE_ID'  # ← Change this
      schema-version: 'v2'
      fail-on-warning: false
      generate-report: true
```

## Version Strategy

### Recommended: Use `@v1`

```yaml
uses: luh-tech/schema-registry/.github/workflows/roadmap-validate.yml@v1
```

This floating tag always points to the latest stable v1.x release.

### Available References

| Reference | Use Case | Stability |
|-----------|----------|-----------|
| `@v1` | Production | ✅ Stable |
| `@v1.0.0` | Pin to specific version | ✅ Immutable |
| `@main` | Development/testing | ⚠️ May break |

## Deployment Checklist

### For New Ventures

1. Ensure `.roadmap/` directory exists with required files:
   ```
   .roadmap/
   ├── roadmap.json          # Required
   ├── venture-summary.json  # Required
   ├── decision-log.json     # Optional
   ├── dependencies.json     # Optional
   └── boundaries.json       # Optional
   ```

2. Create `.github/workflows/roadmap-ci.yml` from template above

3. Replace `YOUR_VENTURE_ID` with your venture's ID (lowercase)

4. Commit and push:
   ```bash
   git add .github/workflows/roadmap-ci.yml
   git commit -m "ci: add roadmap validation workflow"
   git push origin main
   ```

5. Verify at `https://github.com/luh-tech/{venture}/actions`

### For Existing Ventures

Same steps - the workflow will trigger on next `.roadmap/` change or via manual dispatch.

## Troubleshooting

### Workflow Not Found

```
Error: Unable to find reusable workflow
```

**Solution:** Ensure the workflow path is exactly:
```
luh-tech/schema-registry/.github/workflows/roadmap-validate.yml@v1
```

### Schema Validation Failed

```
❌ roadmap.json
```

**Solution:** 
1. Check the workflow logs for specific validation errors
2. Compare your JSON against the schema at `schemas/roadmap.schema.v2.json`
3. Common issues:
   - Missing required fields (`$schema`, `schemaVersion`, `meta`, `venture`, `pitch`)
   - Incorrect date formats (use ISO 8601: `2025-12-09T00:00:00Z`)
   - Invalid enum values

### Manual Trigger

To run validation without file changes:
1. Go to your repo's Actions tab
2. Select "Roadmap CI"
3. Click "Run workflow"

## Related Documentation

- [README.md](../README.md) - Template overview
- [schemas/](../schemas/) - JSON Schema definitions
- [examples/](../examples/) - Sample JSON files

---

## Deployed Ventures

| Venture | CI Workflow | Status |
|---------|-------------|--------|
| Hilja | ✅ Deployed | Active |
| Ectropy-Business | ⏳ Pending | - |
| JobsiteControl | ⏳ Pending | - |
| Qullqa | ⏳ Pending | - |
| Viiva | ⏳ Pending | - |
| Raizal | ⏳ Pending | - |
| Replique | ⏳ Pending | - |
| LuhTech-business | ⏳ Pending | - |

---

*Part of LuhTech Enterprise Infrastructure*  
*Last Updated: December 9, 2025*
