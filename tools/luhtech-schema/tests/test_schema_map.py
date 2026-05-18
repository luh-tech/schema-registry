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
