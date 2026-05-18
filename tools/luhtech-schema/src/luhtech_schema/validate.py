"""Read-only validation for T0.

Canonical rules:
- D2: $id is URL form at https://schemas.luh.tech/
- D6: top-level semver version field is present
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

CANONICAL_HOST = "https://schemas.luh.tech/"
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][\w.-]+)?$")
_SKIP_PARTS = {".git", "node_modules", ".venv", "venv", "__pycache__"}


def _load_json(path: Path) -> tuple[dict | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"
    except OSError as e:
        return None, f"file read error: {e}"


def _check_schema_doc(doc: dict) -> list[str]:
    issues: list[str] = []
    sid = doc.get("$id")
    if not sid:
        issues.append("missing $id (D2)")
    elif not isinstance(sid, str) or not sid.startswith(CANONICAL_HOST):
        issues.append(f"$id not URL form at {CANONICAL_HOST} (D2): {sid!r}")
    version = doc.get("version")
    if not version:
        issues.append("missing top-level version field (D6)")
    elif not isinstance(version, str) or not SEMVER_RE.match(version):
        issues.append(f"version not semver (D6): {version!r}")
    if not doc.get("$schema"):
        issues.append("missing $schema (no draft reference)")
    return issues


def _check_instance_doc(doc: dict) -> list[str]:
    issues: list[str] = []
    schema_ref = doc.get("$schema")
    if not schema_ref:
        issues.append("instance has no $schema reference")
    elif not isinstance(schema_ref, str) or not schema_ref.startswith("http"):
        issues.append(f"$schema is not a URL: {schema_ref!r}")
    return issues


def validate_path(path_str: str) -> int:
    path = Path(path_str)
    if not path.exists():
        print(f"ERROR: path not found: {path}", file=sys.stderr)
        return 2
    doc, err = _load_json(path)
    if err:
        print(f"FAIL {path}: {err}")
        return 1
    if not isinstance(doc, dict):
        print(f"FAIL {path}: top-level is not an object")
        return 1
    issues = _check_schema_doc(doc) if "$id" in doc else _check_instance_doc(doc)
    if not issues:
        print(f"OK   {path}")
        return 0
    print(f"FAIL {path}")
    for issue in issues:
        print(f"     - {issue}")
    return 1


def _iter_schema_files(root: Path) -> Iterable[Path]:
    for p in sorted(root.rglob("*.schema.json")):
        if any(part in _SKIP_PARTS for part in p.parts):
            continue
        yield p


def validate_registry(root_str: str) -> int:
    root = Path(root_str).resolve()
    if not root.exists():
        print(f"ERROR: registry root not found: {root}", file=sys.stderr)
        return 2
    total = 0
    failed = 0
    fail_details: list[tuple[Path, list[str]]] = []
    for schema_path in _iter_schema_files(root):
        total += 1
        doc, err = _load_json(schema_path)
        if err:
            failed += 1
            fail_details.append((schema_path, [err]))
            continue
        if not isinstance(doc, dict):
            failed += 1
            fail_details.append((schema_path, ["top-level is not an object"]))
            continue
        issues = _check_schema_doc(doc)
        if issues:
            failed += 1
            fail_details.append((schema_path, issues))
    print("===== luhtech-schema validate registry =====")
    print(f"root:    {root}")
    print(f"schemas: {total}")
    print(f"passed:  {total - failed}")
    print(f"failed:  {failed}")
    if fail_details:
        print()
        print("Violations:")
        for path, issues in fail_details:
            try:
                rel = path.relative_to(root)
            except ValueError:
                rel = path
            print(f"  {rel}")
            for issue in issues:
                print(f"    - {issue}")
    return 0 if failed == 0 else 1
