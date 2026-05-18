"""Read-only validation T0-T2. D2, D6, D9-aware. User-Agent fix for Cloudflare."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError
from luhtech_schema import __version__

CANONICAL_HOST = "https://schemas.luh.tech/"
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][\w.-]+)?$")
_SKIP_PARTS = {".git", "node_modules", ".venv", "venv", "__pycache__"}
_UA = f"luhtech-schema/{__version__}"

def _is_url(t): return urlparse(t).scheme in {"http", "https"}

def _load_json_from_url(url):
    try:
        req = Request(url, headers={"User-Agent": _UA, "Accept": "application/json, */*;q=0.5"})
        with urlopen(req, timeout=10) as r: return json.loads(r.read().decode()), None
    except URLError as e: return None, f"URL fetch error: {e}"
    except json.JSONDecodeError as e: return None, f"JSON parse error: {e}"

def _load_json_from_path(path):
    try: return json.loads(path.read_text(encoding="utf-8")), None
    except (json.JSONDecodeError, OSError) as e: return None, str(e)

def _check_schema_doc(doc):
    issues = []
    sid = doc.get("$id")
    if not sid: issues.append("missing $id (D2)")
    elif not isinstance(sid, str) or not sid.startswith(CANONICAL_HOST):
        issues.append(f"$id not URL form at {CANONICAL_HOST} (D2): {sid!r}")
    ver = doc.get("version")
    if not ver: issues.append("missing top-level version field (D6)")
    elif not isinstance(ver, str) or not SEMVER_RE.match(ver):
        issues.append(f"version not semver (D6): {ver!r}")
    if not doc.get("$schema"): issues.append("missing $schema")
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
    for i in issues: print(f"     - {i}")
    return 1

def _iter_schema_files(root):
    for p in sorted(root.rglob("*.schema.json")):
        if any(part in _SKIP_PARTS for part in p.parts): continue
        yield p

def validate_registry(root_str):
    root = Path(root_str).resolve()
    if not root.exists(): print(f"ERROR: not found: {root}", file=sys.stderr); return 2
    total = failed = 0; fail_details = []
    for sp in _iter_schema_files(root):
        total += 1
        doc, err = _load_json_from_path(sp)
        if err: failed += 1; fail_details.append((sp, [err])); continue
        if not isinstance(doc, dict): failed += 1; fail_details.append((sp, ["top-level not object"])); continue
        issues = _check_schema_doc(doc)
        if issues: failed += 1; fail_details.append((sp, issues))
    print("===== luhtech-schema validate registry =====")
    print(f"root:    {root}\nschemas: {total}\npassed:  {total-failed}\nfailed:  {failed}")
    if fail_details:
        print("\nViolations:")
        for path, issues in fail_details:
            try: rel = path.relative_to(root)
            except ValueError: rel = path
            print(f"  {rel}")
            for i in issues: print(f"    - {i}")
    return 0 if failed == 0 else 1

def build_local_registry(registry_root="."):
    """Build referencing.Registry from schemas/_meta/schema-map.json."""
    try:
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT7
    except ImportError: return None
    root = Path(registry_root).resolve()
    map_path = root / "schemas" / "_meta" / "schema-map.json"
    if not map_path.exists(): return None
    try: schema_map = json.loads(map_path.read_text())
    except (OSError, json.JSONDecodeError): return None
    registry = Registry()
    for entry in schema_map.get("schemas", []):
        if not entry.get("loadable", True): continue
        sp = root / entry["path"]
        if not sp.exists(): continue
        try: schema_doc = json.loads(sp.read_text())
        except (OSError, json.JSONDecodeError): continue
        sid = entry.get("$id") or schema_doc.get("$id")
        if not sid: continue
        resource = Resource.from_contents(schema_doc, default_specification=DRAFT7)
        registry = registry.with_resource(sid, resource)
    return registry
