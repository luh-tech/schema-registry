"""Smoke tests for classify subcommand (T2)."""
from __future__ import annotations
import json
from pathlib import Path
from luhtech_schema.classify import LAYERS, _collect_refs, _derive_layer, _is_semver, classify

def test_derive_layer_root_acronyms():
    layer, subdir = _derive_layer(("schemas", "acronyms-catalog.schema.json"))
    assert layer == "vocabulary" and subdir == "(root)"

def test_derive_layer_root_decision_log():
    layer, subdir = _derive_layer(("schemas", "decision-log.schema.v2.json"))
    assert layer == "governance" and subdir == "(root)"

def test_derive_layer_subdir_pm():
    layer, subdir = _derive_layer(("schemas", "pm", "decision.schema.json"))
    assert layer == "governance" and subdir == "pm"

def test_derive_layer_subdir_enums():
    layer, subdir = _derive_layer(("schemas", "_enums", "luhtech-enums.schema.v2.json"))
    assert layer == "vocabulary" and subdir == "_enums"

def test_derive_layer_unclassified():
    layer, subdir = _derive_layer(("schemas", "unknown-dir", "foo.schema.json"))
    assert layer == "unclassified" and subdir == "unknown-dir"

def test_collect_refs_finds_nested():
    doc = {"properties": {"a": {"$ref": "#/definitions/A"}, "b": {"items": {"$ref": "../_enums/e.json#/definitions/Foo"}}}}
    refs = _collect_refs(doc)
    assert "#/definitions/A" in refs
    assert "../_enums/e.json#/definitions/Foo" in refs

def test_is_semver():
    assert _is_semver("1.0.0") and _is_semver("1.2.3-alpha")
    assert not _is_semver("v1.0") and not _is_semver("1.0") and not _is_semver(None)

def test_classify_round_trip(tmp_path):
    (tmp_path / "schemas").mkdir()
    f = tmp_path / "schemas" / "tech-stack.schema.json"
    f.write_text(json.dumps({"$id": "https://schemas.luh.tech/tech-stack.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#", "version": "1.0.0", "type": "object"}))
    entry = classify(f, tmp_path)
    assert entry["layer"] == "infrastructure" and entry["d2Compliant"] and entry["d6Compliant"]
