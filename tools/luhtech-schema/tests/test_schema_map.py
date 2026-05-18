"""Smoke tests for map subcommand (T2)."""
from __future__ import annotations
import json
from pathlib import Path
from luhtech_schema.schema_map import build_schema_map

def test_build_schema_map_empty(tmp_path):
    doc = build_schema_map(tmp_path)
    assert doc["schemaCount"] == 0 and doc["schemas"] == []
    assert "$schema" in doc and "streamUrl" in doc

def test_build_schema_map_with_schemas(tmp_path):
    sd = tmp_path / "schemas"; sd.mkdir()
    (sd / "tech-stack.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/tech-stack.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#", "version": "1.0.0", "type": "object"}))
    sub = sd / "pm"; sub.mkdir()
    (sub / "decision.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/pm/decision.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#", "type": "object"}))
    doc = build_schema_map(tmp_path)
    assert doc["schemaCount"] == 2
    assert doc["meta"]["byLayer"].get("infrastructure", 0) == 1
    assert doc["meta"]["byLayer"].get("governance", 0) == 1
    assert doc["meta"]["d2Compliant"] == 2 and doc["meta"]["d6Compliant"] == 1


def test_build_schema_map_with_ectropy_root(tmp_path):
    """T4 — multi-root walking with ectropy-domain layer."""
    import json
    from luhtech_schema.schema_map import build_schema_map

    pf = tmp_path / "portfolio"
    (pf / "schemas").mkdir(parents=True)
    (pf / "schemas" / "tech-stack.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/tech-stack.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#", "version": "1.0.0",
    }))
    ed = tmp_path / "ectropy"
    sub = ed / "caas"; sub.mkdir(parents=True)
    (sub / "pay-app.schema.json").write_text(json.dumps({
        "$id": "urn:luhtech:ectropy:schema:caas:pay-app",
        "$schema": "http://json-schema.org/draft-07/schema#",
    }))
    doc = build_schema_map(pf, ectropy_root=ed)
    assert doc["schemaCount"] == 2
    paths = [e["path"] for e in doc["schemas"]]
    assert any(p.startswith("ectropy-domain/") for p in paths)
    assert doc["meta"]["byLayer"].get("domain", 0) == 1
    assert doc["meta"]["byRegistry"]["portfolio"] == 1
    assert doc["meta"]["byRegistry"]["ectropy-domain"] == 1


def test_build_schema_map_no_ectropy_backward_compat(tmp_path):
    """Without ectropy-domain root, behavior is portfolio-only (T2-compatible)."""
    import json
    from luhtech_schema.schema_map import build_schema_map

    pf = tmp_path / "portfolio"
    (pf / "schemas").mkdir(parents=True)
    (pf / "schemas" / "x.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/x.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#", "version": "1.0.0",
    }))
    doc = build_schema_map(pf)
    assert doc["schemaCount"] == 1
    assert doc["meta"]["byRegistry"]["ectropy-domain"] == 0
    assert doc["meta"]["byRegistry"]["portfolio"] == 1
