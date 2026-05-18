"""Smoke tests for the T0 validate subcommand."""

from __future__ import annotations

import json
from pathlib import Path

from luhtech_schema.validate import (
    _check_instance_doc,
    _check_schema_doc,
    validate_path,
    validate_registry,
)


def test_valid_schema_passes() -> None:
    doc = {"$id": "https://schemas.luh.tech/example.schema.json", "$schema": "https://json-schema.org/draft-07/schema", "version": "1.0.0", "type": "object"}
    assert _check_schema_doc(doc) == []


def test_missing_id_fails() -> None:
    doc = {"$schema": "https://json-schema.org/draft-07/schema", "version": "1.0.0"}
    assert any("$id" in i for i in _check_schema_doc(doc))


def test_urn_id_fails() -> None:
    doc = {"$id": "urn:luhtech:ectropy:schema:voxel", "$schema": "https://json-schema.org/draft-07/schema", "version": "1.0.0"}
    assert any("D2" in i for i in _check_schema_doc(doc))


def test_missing_version_fails() -> None:
    doc = {"$id": "https://schemas.luh.tech/example.schema.json", "$schema": "https://json-schema.org/draft-07/schema"}
    assert any("version" in i for i in _check_schema_doc(doc))


def test_bad_semver_fails() -> None:
    doc = {"$id": "https://schemas.luh.tech/example.schema.json", "$schema": "https://json-schema.org/draft-07/schema", "version": "v1.0"}
    assert any("semver" in i for i in _check_schema_doc(doc))


def test_instance_with_schema_passes() -> None:
    doc = {"$schema": "https://schemas.luh.tech/foo.schema.json", "title": "hi"}
    assert _check_instance_doc(doc) == []


def test_instance_without_schema_fails() -> None:
    assert any("$schema" in i for i in _check_instance_doc({"title": "hi"}))


def test_validate_path_round_trip(tmp_path: Path) -> None:
    f = tmp_path / "example.schema.json"
    f.write_text(json.dumps({"$id": "https://schemas.luh.tech/example.schema.json", "$schema": "https://json-schema.org/draft-07/schema", "version": "1.0.0"}))
    assert validate_path(str(f)) == 0


def test_validate_registry_empty(tmp_path: Path) -> None:
    assert validate_registry(str(tmp_path)) == 0


def test_validate_registry_mixed(tmp_path: Path) -> None:
    good = tmp_path / "good.schema.json"
    good.write_text(json.dumps({"$id": "https://schemas.luh.tech/good.schema.json", "$schema": "https://json-schema.org/draft-07/schema", "version": "1.0.0"}))
    bad = tmp_path / "bad.schema.json"
    bad.write_text(json.dumps({"version": "1.0.0"}))
    assert validate_registry(str(tmp_path)) == 1
