"""Schema classification — T2, extended T4 for multi-root support."""
from __future__ import annotations
import json, re
from pathlib import Path

LAYERS = ["vocabulary","governance","infrastructure","portfolio-ops","venture-ops","ip","meta","domain","unclassified"]
_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][\w.-]+)?$")

_DIR_TO_LAYER = {
    "_definitions": "vocabulary", "_enums": "vocabulary", "_meta": "meta",
    "pm": "governance", "patent": "ip", "portfolio": "portfolio-ops", "cis": "infrastructure",
}

_ROOT_NAME_TO_LAYER = [
    ("acronyms-catalog","vocabulary"), ("decision-log","governance"),
    ("follow-up-register","governance"), ("boundaries","governance"),
    ("dependencies","governance"), ("evidence-session","governance"),
    ("infrastructure-catalog","infrastructure"), ("tech-stack","infrastructure"),
    ("interfaces","infrastructure"), ("workflow-registry","infrastructure"),
    ("agent-prompt","infrastructure"), ("metrics-pipeline","portfolio-ops"),
    ("roadmap","venture-ops"), ("roadmap-business","venture-ops"),
    ("feature","venture-ops"), ("venture-summary","venture-ops"),
]

def _is_semver(v): return isinstance(v, str) and bool(_SEMVER_RE.match(v))

def _collect_refs(node):
    refs = set()
    def walk(n):
        if isinstance(n, dict):
            if isinstance(n.get("$ref"), str): refs.add(n["$ref"])
            for v in n.values(): walk(v)
        elif isinstance(n, list):
            for v in n: walk(v)
    walk(node)
    return sorted(refs)

def _derive_layer(rel_parts):
    if len(rel_parts) >= 2 and rel_parts[0] == "schemas":
        if len(rel_parts) == 2:
            subdir = "(root)"
            stem = re.sub(r"\.v\d+$", "", rel_parts[1].replace(".schema.json",""))
            for prefix, layer in _ROOT_NAME_TO_LAYER:
                if stem == prefix or stem.startswith(prefix + "."):
                    return layer, subdir
            return "unclassified", subdir
        subdir = rel_parts[1]
        return _DIR_TO_LAYER.get(subdir, "unclassified"), subdir
    return "unclassified", "—"

def classify(path: Path, registry_root: Path, registry_label: str = "portfolio") -> dict:
    """Classify a single schema file.

    registry_label="portfolio" uses layered taxonomy from schemas/<subdir>/.
    registry_label="ectropy-domain" classifies every entry as layer="domain"
    with subdir = first path component (L11 domain directories).
    """
    try: rel = path.relative_to(registry_root)
    except ValueError: rel = path

    if registry_label == "ectropy-domain":
        rel_parts = tuple(rel.parts)
        subdir = rel_parts[0] if len(rel_parts) > 1 else "(root)"
        layer = "domain"
    else:
        rel_parts = tuple(rel.parts)
        layer, subdir = _derive_layer(rel_parts)

    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return {"path": str(rel), "subdir": subdir, "layer": layer, "loadable": False, "loadError": str(e)}

    sid = doc.get("$id")
    refs = _collect_refs(doc)
    return {
        "$id": sid if isinstance(sid, str) else None,
        "path": str(rel), "version": doc.get("version"), "title": doc.get("title"),
        "subdir": subdir, "layer": layer,
        "d2Compliant": isinstance(sid, str) and sid.startswith("https://schemas.luh.tech/"),
        "d6Compliant": _is_semver(doc.get("version")),
        "refCount": len(refs), "refs": refs, "loadable": True,
    }

def classify_cmd(target, registry_root="."):
    root = Path(registry_root).resolve()
    p = Path(target)
    if not p.exists(): print(f"ERROR: path not found: {p}"); return 2
    print(json.dumps(classify(p, root), indent=2, ensure_ascii=False))
    return 0
