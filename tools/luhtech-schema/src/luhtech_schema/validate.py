"""Read-only validation for T0âT1. D2, D6, D9-aware."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from typing import Iterable
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen

CANONICAL_HOST = "https://schemas.luh.tech/"
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][\w.-]+)?$")
_SKIP_PARTS = {".git", "node_modules", ".venv", "venv", "__pycache__"}

def _is_url(t): return urlparse(t).scheme in {"http", "https"}

def _load_json_from_url(url):
    try:
        with urlopen(url, timeout=10) as r: return json.loads(r.read().decode()), None
    except (URLError, json.JSONDecodeError) as e: return None, str(e)

def _load_json_from_path(path):
    try: return json.loads(path.read_text(encoding="utf-8")), None
    except (json.JSONDecodeError, OSError) as e: return None, str(e)

def _check_schema_doc(doc):
    issues = []
    sid = doc.get("$id")
    if not sid: issues.append("missing $id (D2)")
    elif not isinstance(sid, str) or not sid.startswith(CANONICAL_HOST):
        issues.append(f"$id not URL form at {CANONICAL_HOST} (D2): {sid!r}")
    version = doc.get("version")
    if not version: issues.append("missing top-level version field (D6)")
    elif not isinstance(version, str) or not SEMVER_RE.match(version):
        issues.append(f"version not semver (D6): {version!r}")
    if not doc.get("$schema"): issues.append("missing $schema (no draft reference)")
    return issues

def _check_instance_doc(doc):
    issues = []
    sr = doc.get("$schema")
    if not sr: issues.append("instance has no $schema reference")
    elif not isinstance(sr, str) or not sr.startswith("http"):
        issues.append(f"$schema is not a URL: {sr!r}")
    return issues

def validate_path(target):
    if _is_url(target):
        doc, err = _load_json_from_url(target); display = target
    else:
        p = Path(target)
        if not p.exists(): print(f"ERROR: path not found: {p}", file=sys.stderr); return 2
        doc, err = _load_json_from_path(p); display = str(p)
    if err: print(f"FAIL {display}: {err}"); return 1
    if not isinstance(doc, dict): print(f"FAIL {display}: top-level is not an object"); return 1
    issues = _check_schema_doc(doc) if "$id" in doc else _check_instance_doc(doc)
    if not issues: print(f"OK   {display}"); return 0
    print(f"FAIL {display}")
    for issue in issues: print(f"     - {issue}")
    return 1

def _iter_schema_files(root):
    for p in sorted(root.rglob("*.schema.json")):
        if any(part in _SKIP_PARTS for part in p.parts): continue
        yield p

def validate_registry(root_str):
    root = Path(root_str).resolve()
    if not root.exists(): print(f"ERROR: registry root not found: {root}", file=sys.stderr); return 2
    total = failed = 0
    fail_details = []
    for sp in _iter_schema_files(root):
        total += 1
        doc, err = _load_json_from_path(sp)
        if err: failed += 1; fail_details.append((sp, [err])); continue
        if not isinstance(doc, dict): failed += 1; fail_details.append((sp, ["top-level is not an object"])); continue
        issues = _check_schema_doc(doc)
        if issues: failed += 1; fail_details.append((sp, issues))
    print("===== luhtech-schema validate registry =====")
    print(f"root:    {root}")
    print(f"schemas: {total}")
    print(f"passed:  {total - failed}")
    print(f"failed:  {failed}")
    if fail_details:
        print()
        print("Violations:")
        for path, issues in fail_details:
            try: rel = path.relative_to(root)
            except ValueError: rel = path
            print(f"  {rel}")
            for issue in issues: print(f"    - {issue}")
    return 0 if failed == 0 else 1
