"""Schema map generation — T2, extended T4 for multi-root (L11) walking."""
from __future__ import annotations
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from luhtech_schema import __version__
from luhtech_schema.classify import classify

STREAM_URL = "https://schemas.luh.tech/_meta/schema-map.json"
SCHEMA_URL = "https://schemas.luh.tech/_meta/schema-map.schema.json"
SKIP_PARTS = {".git","node_modules",".venv","venv","__pycache__"}

def _iter_schema_files(root):
    for p in sorted(root.rglob("*.schema.json")):
        if any(part in SKIP_PARTS for part in p.parts): continue
        if "_meta" in p.parts and "schema-map" in p.name: continue
        yield p

def build_schema_map(registry_root: Path, ectropy_root: Path | None = None) -> dict:
    schemas: list[dict] = []

    # Portfolio walk
    for p in _iter_schema_files(registry_root):
        schemas.append(classify(p, registry_root))

    # Ectropy-domain walk (L11) — prefix paths with ectropy-domain/
    if ectropy_root is not None and ectropy_root.exists():
        for p in _iter_schema_files(ectropy_root):
            entry = classify(p, ectropy_root, registry_label="ectropy-domain")
            entry["path"] = f"ectropy-domain/{entry['path']}"
            schemas.append(entry)

    by_layer = Counter(e.get("layer","—") for e in schemas)
    by_subdir = Counter(e.get("subdir","—") for e in schemas)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    portfolio_count = sum(1 for e in schemas if not e["path"].startswith("ectropy-domain/"))
    ectropy_count = sum(1 for e in schemas if e["path"].startswith("ectropy-domain/"))

    return {
        "$schema": SCHEMA_URL, "streamUrl": STREAM_URL, "version": "1.0.0",
        "generatedAt": now, "generatedBy": f"luhtech-schema map (v{__version__})",
        "registry": "luh-tech/schema-registry + ectropy-ai/schemas (L11, post-T5)" if ectropy_root else "luh-tech/schema-registry",
        "schemaCount": len(schemas),
        "meta": {
            "d2Compliant": sum(1 for e in schemas if e.get("d2Compliant")),
            "d6Compliant": sum(1 for e in schemas if e.get("d6Compliant")),
            "byLayer": dict(by_layer), "bySubdir": dict(by_subdir),
            "byRegistry": {"portfolio": portfolio_count, "ectropy-domain": ectropy_count},
        },
        "schemas": schemas,
    }

def map_cmd(registry_root=".", include_ectropy_domain=None):
    root = Path(registry_root).resolve()
    if not root.exists(): print(f"ERROR: not found: {root}"); return 2
    ectropy = None
    if include_ectropy_domain:
        ectropy = Path(include_ectropy_domain).resolve()
        if not ectropy.exists(): print(f"ERROR: ectropy-domain not found: {ectropy}"); return 2
    doc = build_schema_map(root, ectropy_root=ectropy)
    out = root / "schemas" / "_meta" / "schema-map.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(root)}")
    print(f"  schemas:      {doc['schemaCount']}")
    print(f"  D2 compliant: {doc['meta']['d2Compliant']}")
    print(f"  D6 compliant: {doc['meta']['d6Compliant']}")
    print(f"  by registry:  {doc['meta']['byRegistry']}")
    print(f"  by layer:     {doc['meta']['byLayer']}")
    return 0
