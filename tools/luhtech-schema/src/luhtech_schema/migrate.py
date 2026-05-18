"""Schema migrations — T3.

`luhtech-schema migrate add-versions` adds a top-level ``version`` field to
every schema in the registry that lacks one.

Version-assignment policy (deterministic):
- Rule 1: $id carries v-suffix .schema.v<N>.json → <N>.0.0 (pad to semver)
- Rule 3: fallback to 1.0.0

Discipline:
- Dry-run by default, --apply mutates files.
- Idempotent — if version is already present, skip.
- Atomic per-file write — temp file + rename.
- Order-preserving — version inserted after $id or $schema.
"""
from __future__ import annotations
import json, os, re, sys, tempfile
from pathlib import Path

V_SUFFIX_RE = re.compile(r"\.schema\.v(\d+(?:\.\d+){0,2})\.json$")
# Preferred anchor order: $id first, then $schema, then front-of-doc.
ANCHOR_PRIORITY = ["$id", "$schema"]

def _propose_version(sid):
    if sid:
        m = V_SUFFIX_RE.search(sid)
        if m:
            parts = m.group(1).split(".")
            while len(parts) < 3: parts.append("0")
            return ".".join(parts[:3]), "rule-1 (v-suffix)"
    return "1.0.0", "rule-3 (default)"

def _insert_version(doc, version):
    """Insert version after the highest-priority anchor key ($id preferred over $schema)."""
    # Find the best anchor present in this document
    target_anchor = None
    for anchor in ANCHOR_PRIORITY:
        if anchor in doc:
            target_anchor = anchor
            break

    new_doc = {}
    inserted = False
    for k, v in doc.items():
        new_doc[k] = v
        if not inserted and k == target_anchor:
            new_doc["version"] = version
            inserted = True
    if not inserted:
        rebuilt = {"version": version}
        for k, v in doc.items(): rebuilt[k] = v
        return rebuilt
    return new_doc

def _atomic_write(path, content):
    fd, tmp = tempfile.mkstemp(prefix=".tmp-migrate-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f: f.write(content)
        os.replace(tmp, path)
    except Exception:
        try: os.unlink(tmp)
        except OSError: pass
        raise

def add_versions(registry_root=".", apply=False):
    root = Path(registry_root).resolve()
    map_path = root / "schemas" / "_meta" / "schema-map.json"
    if not map_path.exists():
        print(f"ERROR: schema-map missing at {map_path}", file=sys.stderr)
        return 2
    schema_map = json.loads(map_path.read_text(encoding="utf-8"))
    targets = [s for s in schema_map["schemas"] if not s.get("d6Compliant")]

    print("=== luhtech-schema migrate add-versions ===")
    print(f"mode:    {'APPLY (writes)' if apply else 'DRY-RUN'}")
    print(f"targets: {len(targets)} schemas missing top-level version")
    print()

    if not targets:
        print("nothing to migrate — all schemas D6-compliant."); return 0

    plan = []
    for entry in targets:
        version, rule = _propose_version(entry.get("$id"))
        plan.append((entry["path"], entry.get("$id"), version, rule))

    print(f"{'path':<55}  {'proposed':<10}  rule")
    print("-" * 85)
    for path, _sid, version, rule in plan:
        disp = path if len(path) <= 55 else "..." + path[-52:]
        print(f"{disp:<55}  {version:<10}  {rule}")
    print()

    if not apply:
        print("DRY-RUN — no files modified. Re-run with --apply to write."); return 0

    print("APPLYING...")
    written = []; skipped = []; failed = []

    for path_str, _sid, version, _rule in plan:
        schema_path = root / path_str
        if not schema_path.exists():
            failed.append((path_str, "file missing")); continue
        try:
            doc = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            failed.append((path_str, f"JSON: {e}")); continue
        if "version" in doc:
            skipped.append(path_str); continue
        content = json.dumps(_insert_version(doc, version), indent=2, ensure_ascii=False) + "\n"
        try:
            _atomic_write(schema_path, content)
            written.append(path_str)
        except OSError as e:
            failed.append((path_str, f"write: {e}"))

    print()
    print(f"  written:  {len(written)}")
    print(f"  skipped:  {len(skipped)}  (already had version)")
    print(f"  failed:   {len(failed)}")
    if failed:
        for p, r in failed: print(f"  FAIL {p}: {r}")
        return 1
    return 0

def migrate_cmd(subcommand, registry_root=".", apply=False):
    if subcommand == "add-versions":
        return add_versions(registry_root=registry_root, apply=apply)
    print(f"ERROR: unknown migrate subcommand: {subcommand}", file=sys.stderr)
    return 2
