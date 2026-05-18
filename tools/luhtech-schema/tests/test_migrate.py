"""Smoke tests for migrate subcommand (T3)."""
from __future__ import annotations
import json
from pathlib import Path
from luhtech_schema.migrate import _insert_version, _propose_version, add_versions

def test_propose_version_default():
    v, rule = _propose_version("https://schemas.luh.tech/decision-log.schema.json")
    assert v == "1.0.0" and "rule-3" in rule

def test_propose_version_v_suffix_major():
    v, rule = _propose_version("https://schemas.luh.tech/foo.schema.v2.json")
    assert v == "2.0.0" and "rule-1" in rule

def test_propose_version_v_suffix_minor():
    v, rule = _propose_version("https://schemas.luh.tech/roadmap.schema.v3.4.json")
    assert v == "3.4.0"

def test_propose_version_v_suffix_full():
    v, _ = _propose_version("https://schemas.luh.tech/foo.schema.v2.1.5.json")
    assert v == "2.1.5"

def test_propose_version_none_id():
    v, _ = _propose_version(None)
    assert v == "1.0.0"

def test_insert_version_after_id():
    doc = {"$schema": "draft", "$id": "https://x", "title": "T", "type": "object"}
    new = _insert_version(doc, "1.0.0")
    keys = list(new.keys())
    assert keys.index("$id") < keys.index("version") < keys.index("title")
    assert new["version"] == "1.0.0"

def test_insert_version_after_schema_no_id():
    doc = {"$schema": "draft", "title": "T"}
    new = _insert_version(doc, "1.0.0")
    keys = list(new.keys())
    assert keys.index("$schema") < keys.index("version") < keys.index("title")

def test_insert_version_no_anchor_inserts_first():
    doc = {"title": "T", "type": "object"}
    new = _insert_version(doc, "1.0.0")
    assert list(new.keys())[0] == "version"
    assert new["title"] == "T"

def test_add_versions_dry_run(tmp_path):
    sd = tmp_path / "schemas"; sd.mkdir()
    f = sd / "x.schema.json"
    f.write_text(json.dumps({"$id": "https://schemas.luh.tech/x.schema.json", "$schema": "draft"}))
    (sd / "_meta").mkdir()
    (sd / "_meta" / "schema-map.json").write_text(json.dumps({
        "schemas": [{"path": "schemas/x.schema.json", "$id": "https://schemas.luh.tech/x.schema.json", "d6Compliant": False}]
    }))
    assert add_versions(registry_root=str(tmp_path), apply=False) == 0
    assert "version" not in json.loads(f.read_text())

def test_add_versions_apply_writes(tmp_path):
    sd = tmp_path / "schemas"; sd.mkdir()
    f = sd / "x.schema.json"
    f.write_text(json.dumps({"$id": "https://schemas.luh.tech/x.schema.json", "$schema": "draft"}))
    (sd / "_meta").mkdir()
    (sd / "_meta" / "schema-map.json").write_text(json.dumps({
        "schemas": [{"path": "schemas/x.schema.json", "$id": "https://schemas.luh.tech/x.schema.json", "d6Compliant": False}]
    }))
    assert add_versions(registry_root=str(tmp_path), apply=True) == 0
    doc = json.loads(f.read_text())
    assert doc["version"] == "1.0.0"
    keys = list(doc.keys())
    assert keys.index("$id") < keys.index("version")

def test_add_versions_idempotent(tmp_path):
    sd = tmp_path / "schemas"; sd.mkdir()
    f = sd / "x.schema.json"
    f.write_text(json.dumps({"$id": "https://x", "version": "2.5.1"}))
    (sd / "_meta").mkdir()
    (sd / "_meta" / "schema-map.json").write_text(json.dumps({
        "schemas": [{"path": "schemas/x.schema.json", "d6Compliant": False}]
    }))
    assert add_versions(registry_root=str(tmp_path), apply=True) == 0
    assert json.loads(f.read_text())["version"] == "2.5.1"
