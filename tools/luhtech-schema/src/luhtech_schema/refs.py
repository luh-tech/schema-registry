"""Schema reference registry generator.

`luhtech-schema refs rebuild`         Regenerate schema-refs.json from disk.
`luhtech-schema refs rebuild --check`  Drift detection only; exit 1 if out of sync.

Pure disk-truth regeneration. Does not read existing schema-refs.json schema
entries to preserve curated content — disk is authoritative. Existing top-level
document fields ($schema, $id, title, description) are preserved; only the
`schemas` block and `meta` block are regenerated.

Namespace handling:
  - schemas in GROUPED_NAMESPACES (patent) → nested under parent.schemas dict
  - schemas in other subdirs              → flat key with subdir prefix (cis-*)
  - schemas at schemas/ root              → flat key, no prefix
  - schemas in EXCLUDE_SUBDIRS           → skipped entirely
"""
from __future__ import annotations
import json, re, sys
from datetime import datetime, timezone
from pathlib import Path

GROUPED_NAMESPACES: frozenset[str] = frozenset({"patent"})
EXCLUDE_SUBDIRS: frozenset[str] = frozenset({"_archive", "_definitions", "_enums", "_meta"})
SKIP_PARTS: frozenset[str] = frozenset({".git", "node_modules", ".venv", "venv", "__pycache__"})

REFS_FILENAME = "schemas/schema-refs.json"

# Matches .schema[.vX[.Y[.Z]]].json at end of filename (case-insensitive)
_STEM_RE = re.compile(r"\.schema(?:\.v\d+(?:\.\d+)*)?\.json$", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Version utilities
# ---------------------------------------------------------------------------

def _parse_semver(v: str) -> tuple[int, ...]:
    if not isinstance(v, str):
        return (0, 0, 0)
    parts = re.split(r"[.\-]", v)
    result = []
    for p in parts[:3]:
        try:
            result.append(int(p))
        except ValueError:
            result.append(0)
    while len(result) < 3:
        result.append(0)
    return tuple(result)


def _semver_bump(version: str, kind: str) -> str:
    """Bump a semver string. kind: 'minor' | 'patch'."""
    major, minor, patch = _parse_semver(version)
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


# ---------------------------------------------------------------------------
# Schema file discovery
# ---------------------------------------------------------------------------

def _normalize_stem(filename: str) -> str:
    """Strip .schema[.vX.Y.Z].json suffix to get the base registry key stem."""
    return _STEM_RE.sub("", filename)


def _iter_schema_files(root: Path):
    """Yield (abs_path, rel_from_root, rel_from_schemas) for canonical schemas.

    Scans schemas/**/*.json, filtering to files whose name contains '.schema'
    (catches both foo.schema.json and foo.schema.v2.3.json). Excluded: any
    path part in SKIP_PARTS, any top-level subdir in EXCLUDE_SUBDIRS.
    """
    schemas_dir = root / "schemas"
    if not schemas_dir.exists():
        return
    for p in sorted(schemas_dir.rglob("*.json")):
        if any(part in SKIP_PARTS for part in p.parts):
            continue
        if ".schema" not in p.name:
            continue
        rel_from_schemas = p.relative_to(schemas_dir)
        parts = rel_from_schemas.parts
        if len(parts) > 1 and parts[0] in EXCLUDE_SUBDIRS:
            continue
        yield p, p.relative_to(root), rel_from_schemas


def _derive_group_and_key(rel_from_schemas: Path) -> tuple[str | None, str] | None:
    """Derive (group, local_key) for a schema file.

    Returns None for excluded files or files with no derivable key.
    group=None  → top-level entry in schemas dict
    group=name  → nested under schemas[group]['schemas'][key]
    """
    parts = rel_from_schemas.parts
    filename = parts[-1]
    stem = _normalize_stem(filename)
    if not stem:
        return None

    if len(parts) == 1:
        return (None, stem)

    subdir = parts[0]
    if subdir in EXCLUDE_SUBDIRS:
        return None
    if subdir in GROUPED_NAMESPACES:
        return (subdir, stem)
    # Flat prefix: cis/url-catalog → cis-url-catalog
    # Guard: if stem already carries the subdir prefix (e.g. cis/cis-infra-changelog),
    # use stem directly to avoid double-prefix (cis-cis-infra-changelog).
    if stem.startswith(f"{subdir}-"):
        return (None, stem)
    return (None, f"{subdir}-{stem}")


# ---------------------------------------------------------------------------
# Entry builder
# ---------------------------------------------------------------------------

def _first_sentence(text: str, max_len: int = 200) -> str:
    """Take up to the first sentence (ends at '. ') or first max_len chars."""
    text = (text or "").strip()
    if not text:
        return ""
    # Split at '. ' boundary
    m = re.search(r"\.\s", text)
    if m:
        first = text[:m.start() + 1]
    else:
        first = text
    return first[:max_len]


def _build_entry(file_rel_root: Path, doc: dict) -> dict:
    return {
        "id": doc.get("$id", ""),
        "file": str(file_rel_root).replace("\\", "/"),
        "version": doc.get("version", ""),
        "description": _first_sentence(doc.get("description", "")),
    }


# ---------------------------------------------------------------------------
# Schemas block generation
# ---------------------------------------------------------------------------

def _build_schemas_block(root: Path) -> dict:
    """Scan disk and build a fresh .schemas dict.

    For keys with multiple versioned files (e.g. roadmap.schema.v3.4.json and
    roadmap.schema.json both normalise to 'roadmap'), the file with the highest
    `version` field wins. Ties are broken by filename lexicographic order (last
    alphabetically wins — higher version suffix sorts later).
    """
    candidates: dict[tuple[str | None, str], list[tuple[tuple[int, ...], Path, dict]]] = {}

    for abs_path, rel_root, rel_schemas in _iter_schema_files(root):
        try:
            doc = json.loads(abs_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        result = _derive_group_and_key(rel_schemas)
        if result is None:
            continue
        group, key = result
        ver_tuple = _parse_semver(doc.get("version", ""))
        bucket = (group, key)
        candidates.setdefault(bucket, []).append((ver_tuple, rel_root, doc))

    schemas: dict = {}
    for (group, key), variants in sorted(candidates.items(), key=lambda x: (x[0][0] or "", x[0][1])):
        # Highest version first; use rel_root as tiebreaker (sorted desc → last filename)
        variants.sort(key=lambda x: (x[0], str(x[1])), reverse=True)
        _, rel_root, doc = variants[0]
        entry = _build_entry(rel_root, doc)

        if group is not None:
            if group not in schemas:
                schemas[group] = {
                    "id": f"https://schemas.luh.tech/{group}/",
                    "baseUrl": f"https://schemas.luh.tech/{group}/",
                    "description": f"{group.capitalize()} schema family.",
                    "version": "1.0.0",
                    "schemas": {},
                }
            schemas[group]["schemas"][key] = entry
        else:
            schemas[key] = entry

    return schemas


# ---------------------------------------------------------------------------
# Changelog and diff helpers
# ---------------------------------------------------------------------------

def _flat_entries(schemas: dict) -> dict[str, dict]:
    """Flatten grouped schemas to a single dotted-key → entry map for diffing."""
    flat: dict[str, dict] = {}
    for k, v in schemas.items():
        if isinstance(v, dict) and "schemas" in v:
            for sk, sv in v["schemas"].items():
                flat[f"{k}.{sk}"] = sv if isinstance(sv, dict) else {}
        else:
            flat[k] = v if isinstance(v, dict) else {}
    return flat


def _compute_changes(old: dict, new: dict) -> list[str]:
    old_flat = _flat_entries(old)
    new_flat = _flat_entries(new)
    old_keys, new_keys = set(old_flat), set(new_flat)
    changes: list[str] = []
    for k in sorted(new_keys - old_keys):
        v = new_flat[k].get("version", "?")
        changes.append(f"Added: {k} v{v}")
    for k in sorted(old_keys - new_keys):
        changes.append(f"Removed: {k}")
    for k in sorted(old_keys & new_keys):
        oe, ne = old_flat[k], new_flat[k]
        ov, nv = oe.get("version", ""), ne.get("version", "")
        if ov != nv:
            changes.append(f"Updated: {k} v{ov} -> v{nv}")
        elif oe.get("description", "") != ne.get("description", ""):
            changes.append(f"Description updated: {k}")
    return changes or ["No schema-level changes"]


def _compute_bump_kind(old: dict, new: dict) -> str:
    old_flat = _flat_entries(old)
    new_flat = _flat_entries(new)
    if set(old_flat) != set(new_flat):
        return "minor"
    for k in old_flat:
        ov = old_flat[k].get("version", "") if isinstance(old_flat[k], dict) else ""
        nv = new_flat[k].get("version", "") if isinstance(new_flat[k], dict) else ""
        if ov != nv:
            return "minor"
    return "patch"


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def refs_rebuild_cmd(check: bool = False, registry_root: str = ".") -> int:
    root = Path(registry_root).resolve()
    refs_path = root / REFS_FILENAME

    if refs_path.exists():
        try:
            current = json.loads(refs_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"ERROR: cannot read {refs_path}: {e}", file=sys.stderr)
            return 2
    else:
        current = {}

    old_schemas = current.get("schemas", {})
    old_meta = current.get("meta", {})
    old_version = old_meta.get("version", current.get("version", "1.0.0"))
    old_changelog = old_meta.get("changelog", [])

    new_schemas = _build_schemas_block(root)

    # Normalise both for deterministic comparison
    new_norm = json.dumps(new_schemas, sort_keys=True, ensure_ascii=False)
    old_norm = json.dumps(old_schemas, sort_keys=True, ensure_ascii=False)
    has_drift = new_norm != old_norm

    if check:
        if has_drift:
            print("DRIFT DETECTED: schema-refs.json is out of sync with disk.")
            for c in _compute_changes(old_schemas, new_schemas):
                print(f"  {c}")
            return 1
        print("OK: schema-refs.json is in sync with disk.")
        return 0

    if not has_drift:
        print("schema-refs.json is already in sync with disk. Nothing to write.")
        return 0

    bump_kind = _compute_bump_kind(old_schemas, new_schemas)
    new_version = _semver_bump(old_version, bump_kind)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    changes = _compute_changes(old_schemas, new_schemas)

    changelog_entry = {
        "version": new_version,
        "date": now[:10],
        "changes": changes,
    }

    # Preserve all existing top-level document fields; update schemas + meta only
    out_doc = {k: v for k, v in current.items()}
    out_doc["version"] = new_version
    out_doc["meta"] = {
        **{k: v for k, v in old_meta.items()
           if k not in ("version", "lastUpdated", "changelog")},
        "version": new_version,
        "lastUpdated": now,
        "changelog": [changelog_entry] + old_changelog,
    }
    out_doc["schemas"] = new_schemas

    refs_path.write_text(
        json.dumps(out_doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Rebuilt schema-refs.json: {old_version} -> {new_version}  ({bump_kind} bump)")
    for c in changes:
        print(f"  {c}")
    return 0
