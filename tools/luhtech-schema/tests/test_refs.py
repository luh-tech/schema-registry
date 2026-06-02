"""Smoke tests for refs subcommand (T5)."""

from __future__ import annotations

import json
from pathlib import Path

from luhtech_schema.refs import (
    _build_entry,
    _build_schemas_block,
    _compute_bump_kind,
    _compute_changes,
    _derive_group_and_key,
    _first_sentence,
    _flat_entries,
    _is_refsignored,
    _iter_schema_files,
    _load_group_index,
    _load_refsignore,
    _normalize_stem,
    _parse_semver,
    _semver_bump,
    refs_rebuild_cmd,
)


# ---------------------------------------------------------------------------
# _parse_semver
# ---------------------------------------------------------------------------

def test_parse_semver_standard() -> None:
    assert _parse_semver("1.2.3") == (1, 2, 3)


def test_parse_semver_short_pads_zero() -> None:
    assert _parse_semver("1") == (1, 0, 0)
    assert _parse_semver("1.2") == (1, 2, 0)


def test_parse_semver_extra_parts_dropped() -> None:
    assert _parse_semver("1.2.3.4.5") == (1, 2, 3)


def test_parse_semver_non_numeric_zero() -> None:
    assert _parse_semver("v1.0.0") == (0, 0, 0)
    assert _parse_semver("1.x.3") == (1, 0, 3)


def test_parse_semver_non_string() -> None:
    assert _parse_semver(None) == (0, 0, 0)  # type: ignore[arg-type]
    assert _parse_semver(123) == (0, 0, 0)  # type: ignore[arg-type]


def test_parse_semver_dash_separator() -> None:
    assert _parse_semver("1-2-3") == (1, 2, 3)


# ---------------------------------------------------------------------------
# _semver_bump
# ---------------------------------------------------------------------------

def test_semver_bump_minor_resets_patch() -> None:
    assert _semver_bump("1.2.3", "minor") == "1.3.0"


def test_semver_bump_patch() -> None:
    assert _semver_bump("1.2.3", "patch") == "1.2.4"


def test_semver_bump_unknown_kind_defaults_patch() -> None:
    assert _semver_bump("1.2.3", "unknown") == "1.2.4"


def test_semver_bump_from_zero() -> None:
    assert _semver_bump("0.0.0", "minor") == "0.1.0"
    assert _semver_bump("0.0.0", "patch") == "0.0.1"


# ---------------------------------------------------------------------------
# _load_refsignore
# ---------------------------------------------------------------------------

def test_load_refsignore_absent_returns_empty(tmp_path: Path) -> None:
    assert _load_refsignore(tmp_path) == []


def test_load_refsignore_strips_comments_and_blanks(tmp_path: Path) -> None:
    (tmp_path / ".refsignore").write_text(
        "# comment\n"
        "\n"
        "crm/**  # exclude CRM\n"
        "  _instances/**  \n"
    )
    patterns = _load_refsignore(tmp_path)
    assert patterns == ["crm/**", "_instances/**"]


def test_load_refsignore_full_line_comment_excluded(tmp_path: Path) -> None:
    (tmp_path / ".refsignore").write_text("# only a comment\n")
    assert _load_refsignore(tmp_path) == []


# ---------------------------------------------------------------------------
# _is_refsignored
# ---------------------------------------------------------------------------

def test_is_refsignored_recursive_glob() -> None:
    assert _is_refsignored("crm/foo.schema.json", ["crm/**"])
    assert _is_refsignored("crm/sub/bar.schema.json", ["crm/**"])
    assert _is_refsignored("crm", ["crm/**"])


def test_is_refsignored_recursive_no_match_outside_dir() -> None:
    assert not _is_refsignored("crm-prefix/foo.schema.json", ["crm/**"])


def test_is_refsignored_fnmatch_glob() -> None:
    assert _is_refsignored("foo.schema.json", ["*.schema.json"])
    assert not _is_refsignored("foo.json", ["*.schema.json"])


def test_is_refsignored_empty_patterns() -> None:
    assert not _is_refsignored("anything.schema.json", [])


# ---------------------------------------------------------------------------
# _load_group_index
# ---------------------------------------------------------------------------

def test_load_group_index_absent_returns_empty(tmp_path: Path) -> None:
    (tmp_path / "patent").mkdir()
    assert _load_group_index(tmp_path, "patent") == {}


def test_load_group_index_strips_schema_field(tmp_path: Path) -> None:
    g = tmp_path / "patent"
    g.mkdir()
    (g / "_index.json").write_text(json.dumps({
        "$schema": "https://schemas.luh.tech/group-index.schema.json",
        "id": "https://schemas.luh.tech/patent/",
        "version": "1.2.0",
    }))
    data = _load_group_index(tmp_path, "patent")
    assert "$schema" not in data
    assert data["id"] == "https://schemas.luh.tech/patent/"
    assert data["version"] == "1.2.0"


def test_load_group_index_invalid_json_returns_empty(tmp_path: Path) -> None:
    g = tmp_path / "patent"
    g.mkdir()
    (g / "_index.json").write_text("not json {")
    assert _load_group_index(tmp_path, "patent") == {}


# ---------------------------------------------------------------------------
# _normalize_stem
# ---------------------------------------------------------------------------

def test_normalize_stem_plain() -> None:
    assert _normalize_stem("decision.schema.json") == "decision"


def test_normalize_stem_versioned() -> None:
    assert _normalize_stem("roadmap.schema.v3.4.json") == "roadmap"
    assert _normalize_stem("foo.schema.v2.json") == "foo"
    assert _normalize_stem("foo.schema.v2.1.5.json") == "foo"


def test_normalize_stem_case_insensitive() -> None:
    assert _normalize_stem("Foo.SCHEMA.JSON") == "Foo"


def test_normalize_stem_no_suffix_returned_as_is() -> None:
    assert _normalize_stem("plain.json") == "plain.json"


# ---------------------------------------------------------------------------
# _iter_schema_files
# ---------------------------------------------------------------------------

def test_iter_schema_files_empty_dir(tmp_path: Path) -> None:
    (tmp_path / "schemas").mkdir()
    assert list(_iter_schema_files(tmp_path)) == []


def test_iter_schema_files_missing_dir(tmp_path: Path) -> None:
    assert list(_iter_schema_files(tmp_path)) == []


def test_iter_schema_files_yields_canonical_only(tmp_path: Path) -> None:
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "good.schema.json").write_text("{}")
    (sd / "not-a-schema.json").write_text("{}")  # missing .schema
    (sd / "_archive").mkdir()
    (sd / "_archive" / "old.schema.json").write_text("{}")  # excluded subdir
    (sd / ".git").mkdir()
    (sd / ".git" / "garbage.schema.json").write_text("{}")  # skip part

    results = list(_iter_schema_files(tmp_path))
    names = [str(r[2]) for r in results]
    assert "good.schema.json" in names
    assert all("not-a-schema" not in n for n in names)
    assert all("_archive" not in n for n in names)
    assert all(".git" not in n for n in names)


def test_iter_schema_files_versioned_filename(tmp_path: Path) -> None:
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "roadmap.schema.v3.4.json").write_text("{}")
    results = list(_iter_schema_files(tmp_path))
    assert len(results) == 1


# ---------------------------------------------------------------------------
# _derive_group_and_key
# ---------------------------------------------------------------------------

def test_derive_group_root_level() -> None:
    assert _derive_group_and_key(Path("decision.schema.json")) == (None, "decision")


def test_derive_group_grouped_namespace() -> None:
    # 'patent' is in GROUPED_NAMESPACES
    assert _derive_group_and_key(Path("patent/claim.schema.json")) == ("patent", "claim")


def test_derive_group_flat_prefix() -> None:
    # Non-grouped subdir → flat key with prefix
    assert _derive_group_and_key(Path("cis/url-catalog.schema.json")) == (None, "cis-url-catalog")


def test_derive_group_flat_prefix_double_guard() -> None:
    # Stem already starts with subdir name → no double-prefix
    assert _derive_group_and_key(Path("cis/cis-infra-changelog.schema.json")) == (None, "cis-infra-changelog")


def test_derive_group_excluded_subdir_returns_none() -> None:
    assert _derive_group_and_key(Path("_archive/old.schema.json")) is None
    assert _derive_group_and_key(Path("_definitions/foo.schema.json")) is None


def test_derive_group_unnormalizable_returns_none() -> None:
    # _meta is in EXCLUDE_SUBDIRS
    assert _derive_group_and_key(Path("_meta/something.schema.json")) is None


# ---------------------------------------------------------------------------
# _first_sentence
# ---------------------------------------------------------------------------

def test_first_sentence_break_at_period_space() -> None:
    assert _first_sentence("Hello world. More text.") == "Hello world."


def test_first_sentence_no_break_returns_text() -> None:
    assert _first_sentence("No period here") == "No period here"


def test_first_sentence_caps_at_max_len() -> None:
    text = "a" * 300
    result = _first_sentence(text, max_len=50)
    assert len(result) == 50


def test_first_sentence_empty_or_none() -> None:
    assert _first_sentence("") == ""
    assert _first_sentence(None) == ""  # type: ignore[arg-type]
    assert _first_sentence("   ") == ""


def test_first_sentence_truncated_mid_sentence() -> None:
    """Edge: long single sentence truncates to max_len even without period."""
    text = "This is a long sentence without any sentence-ending period for a while"
    assert _first_sentence(text, max_len=20) == "This is a long sente"


# ---------------------------------------------------------------------------
# _build_entry
# ---------------------------------------------------------------------------

def test_build_entry_new_derives_description() -> None:
    doc = {
        "$id": "https://schemas.luh.tech/foo.schema.json",
        "version": "1.0.0",
        "description": "A short description. With trailing text.",
    }
    entry = _build_entry(Path("schemas/foo.schema.json"), doc, {})
    assert entry["id"] == "https://schemas.luh.tech/foo.schema.json"
    assert entry["file"] == "foo.schema.json"
    assert entry["version"] == "1.0.0"
    assert entry["description"] == "A short description."


def test_build_entry_canonical_preserves_description() -> None:
    doc = {
        "$id": "https://schemas.luh.tech/foo.schema.json",
        "version": "1.1.0",
        "description": "Auto-derived description.",
    }
    canonical = {
        "id": "https://schemas.luh.tech/foo.schema.json",
        "description": "Hand-curated wisdom.",
    }
    entry = _build_entry(Path("schemas/foo.schema.json"), doc, canonical)
    assert entry["description"] == "Hand-curated wisdom."


def test_build_entry_canonical_no_description_field_omits() -> None:
    """Canonical entry without description preserves field-set — no description added."""
    doc = {
        "$id": "https://schemas.luh.tech/foo.schema.json",
        "version": "1.0.0",
        "description": "Would be derived if new.",
    }
    canonical = {"id": "https://schemas.luh.tech/foo.schema.json", "file": "foo.schema.json"}
    entry = _build_entry(Path("schemas/foo.schema.json"), doc, canonical)
    assert "description" not in entry


def test_build_entry_preserves_urn_id() -> None:
    """URN-form canonical id wins over URL-form derived id (v1.9.0 policy)."""
    doc = {
        "$id": "https://schemas.luh.tech/voxel.schema.json",
        "version": "1.0.0",
    }
    canonical = {"id": "urn:luhtech:ectropy:schema:voxel"}
    entry = _build_entry(Path("schemas/voxel.schema.json"), doc, canonical)
    assert entry["id"] == "urn:luhtech:ectropy:schema:voxel"


def test_build_entry_strips_schemas_prefix_from_file() -> None:
    doc = {"$id": "https://schemas.luh.tech/cis/url-catalog.schema.json", "version": "1.0.0"}
    entry = _build_entry(Path("schemas/cis/url-catalog.schema.json"), doc, {})
    assert entry["file"] == "cis/url-catalog.schema.json"


def test_build_entry_new_no_description_in_doc_omits() -> None:
    doc = {"$id": "https://schemas.luh.tech/foo.schema.json", "version": "1.0.0"}
    entry = _build_entry(Path("schemas/foo.schema.json"), doc, {})
    assert "description" not in entry


# ---------------------------------------------------------------------------
# _build_schemas_block
# ---------------------------------------------------------------------------

def test_build_schemas_block_empty_root(tmp_path: Path) -> None:
    (tmp_path / "schemas").mkdir()
    assert _build_schemas_block(tmp_path, {}, []) == {}


def test_build_schemas_block_root_schema(tmp_path: Path) -> None:
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "decision.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/decision.schema.json",
        "version": "1.0.0",
        "description": "Decision record.",
    }))
    result = _build_schemas_block(tmp_path, {}, [])
    assert "decision" in result
    assert result["decision"]["version"] == "1.0.0"


def test_build_schemas_block_respects_refsignore(tmp_path: Path) -> None:
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "crm").mkdir()
    (sd / "crm" / "lead.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/crm/lead.schema.json",
        "version": "1.0.0",
    }))
    result = _build_schemas_block(tmp_path, {}, ["crm/**"])
    assert result == {}


def test_build_schemas_block_version_tiebreak(tmp_path: Path) -> None:
    """Two versioned files normalising to same key: highest version wins."""
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "roadmap.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/roadmap.schema.json", "version": "1.0.0"}))
    (sd / "roadmap.schema.v3.4.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/roadmap.schema.v3.4.json", "version": "3.4.0"}))
    result = _build_schemas_block(tmp_path, {}, [])
    assert result["roadmap"]["version"] == "3.4.0"


def test_build_schemas_block_grouped_namespace(tmp_path: Path) -> None:
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "patent").mkdir()
    (sd / "patent" / "claim.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/patent/claim.schema.json", "version": "1.0.0"}))
    result = _build_schemas_block(tmp_path, {}, [])
    assert "patent" in result
    assert "schemas" in result["patent"]
    assert "claim" in result["patent"]["schemas"]


def test_build_schemas_block_skips_invalid_json(tmp_path: Path) -> None:
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "broken.schema.json").write_text("not json {")
    (sd / "good.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/good.schema.json", "version": "1.0.0"}))
    result = _build_schemas_block(tmp_path, {}, [])
    assert "good" in result
    assert "broken" not in result


# ---------------------------------------------------------------------------
# _flat_entries
# ---------------------------------------------------------------------------

def test_flat_entries_flat_only() -> None:
    inp = {"foo": {"version": "1.0.0"}, "bar": {"version": "2.0.0"}}
    assert _flat_entries(inp) == inp


def test_flat_entries_grouped_dots_keys() -> None:
    inp = {
        "patent": {
            "id": "https://schemas.luh.tech/patent/",
            "schemas": {
                "claim": {"version": "1.0.0"},
                "spec": {"version": "1.1.0"},
            },
        },
        "decision": {"version": "2.0.0"},
    }
    result = _flat_entries(inp)
    assert result["patent.claim"] == {"version": "1.0.0"}
    assert result["patent.spec"] == {"version": "1.1.0"}
    assert result["decision"] == {"version": "2.0.0"}


def test_flat_entries_non_dict_value_normalized() -> None:
    inp = {"weird": "string-not-dict"}
    assert _flat_entries(inp) == {"weird": {}}


# ---------------------------------------------------------------------------
# _compute_changes
# ---------------------------------------------------------------------------

def test_compute_changes_added() -> None:
    old = {"foo": {"version": "1.0.0"}}
    new = {"foo": {"version": "1.0.0"}, "bar": {"version": "2.0.0"}}
    changes = _compute_changes(old, new)
    assert any("Added: bar v2.0.0" in c for c in changes)


def test_compute_changes_removed() -> None:
    old = {"foo": {"version": "1.0.0"}, "bar": {"version": "2.0.0"}}
    new = {"foo": {"version": "1.0.0"}}
    changes = _compute_changes(old, new)
    assert any("Removed: bar" in c for c in changes)


def test_compute_changes_version_updated() -> None:
    old = {"foo": {"version": "1.0.0"}}
    new = {"foo": {"version": "1.1.0"}}
    changes = _compute_changes(old, new)
    assert any("Updated: foo v1.0.0 -> v1.1.0" in c for c in changes)


def test_compute_changes_description_only() -> None:
    old = {"foo": {"version": "1.0.0", "description": "Old."}}
    new = {"foo": {"version": "1.0.0", "description": "New."}}
    changes = _compute_changes(old, new)
    assert any("Description updated: foo" in c for c in changes)


def test_compute_changes_none_returns_sentinel() -> None:
    old = {"foo": {"version": "1.0.0"}}
    new = {"foo": {"version": "1.0.0"}}
    assert _compute_changes(old, new) == ["No schema-level changes"]


# ---------------------------------------------------------------------------
# _compute_bump_kind
# ---------------------------------------------------------------------------

def test_compute_bump_kind_added_key_minor() -> None:
    old = {"foo": {"version": "1.0.0"}}
    new = {"foo": {"version": "1.0.0"}, "bar": {"version": "1.0.0"}}
    assert _compute_bump_kind(old, new) == "minor"


def test_compute_bump_kind_removed_key_minor() -> None:
    old = {"foo": {"version": "1.0.0"}, "bar": {"version": "1.0.0"}}
    new = {"foo": {"version": "1.0.0"}}
    assert _compute_bump_kind(old, new) == "minor"


def test_compute_bump_kind_version_change_minor() -> None:
    old = {"foo": {"version": "1.0.0"}}
    new = {"foo": {"version": "1.1.0"}}
    assert _compute_bump_kind(old, new) == "minor"


def test_compute_bump_kind_description_only_patch() -> None:
    old = {"foo": {"version": "1.0.0", "description": "Old."}}
    new = {"foo": {"version": "1.0.0", "description": "New."}}
    assert _compute_bump_kind(old, new) == "patch"


def test_compute_bump_kind_no_change_patch() -> None:
    old = {"foo": {"version": "1.0.0"}}
    new = {"foo": {"version": "1.0.0"}}
    assert _compute_bump_kind(old, new) == "patch"


# ---------------------------------------------------------------------------
# refs_rebuild_cmd — integration
# ---------------------------------------------------------------------------

def test_refs_rebuild_check_in_sync(tmp_path: Path, capsys) -> None:
    """No drift: --check exits 0 and reports OK."""
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "foo.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/foo.schema.json", "version": "1.0.0"}))
    # Seed schema-refs.json matching disk
    (sd / "schema-refs.json").write_text(json.dumps({
        "version": "1.0.0",
        "schemas": {
            "foo": {
                "id": "https://schemas.luh.tech/foo.schema.json",
                "file": "foo.schema.json",
                "version": "1.0.0",
            }
        },
        "meta": {"version": "1.0.0", "changelog": []},
    }))
    exit_code = refs_rebuild_cmd(check=True, registry_root=str(tmp_path))
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "in sync" in captured.out.lower()


def test_refs_rebuild_check_drift(tmp_path: Path, capsys) -> None:
    """Disk has a schema not in refs: --check exits 1 and reports drift."""
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "foo.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/foo.schema.json", "version": "1.0.0"}))
    # Empty refs
    (sd / "schema-refs.json").write_text(json.dumps({
        "version": "1.0.0", "schemas": {}, "meta": {"version": "1.0.0", "changelog": []}}))
    exit_code = refs_rebuild_cmd(check=True, registry_root=str(tmp_path))
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "DRIFT DETECTED" in captured.out


def test_refs_rebuild_writes_and_bumps(tmp_path: Path) -> None:
    """Rebuild mode writes refs.json with bumped version."""
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "foo.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/foo.schema.json", "version": "1.0.0"}))
    (sd / "schema-refs.json").write_text(json.dumps({
        "version": "1.0.0", "schemas": {}, "meta": {"version": "1.0.0", "changelog": []}}))
    exit_code = refs_rebuild_cmd(check=False, registry_root=str(tmp_path))
    assert exit_code == 0
    new_doc = json.loads((sd / "schema-refs.json").read_text())
    assert "foo" in new_doc["schemas"]
    assert new_doc["version"] == "1.1.0"  # minor bump (key added)
    assert len(new_doc["meta"]["changelog"]) == 1


def test_refs_rebuild_idempotent(tmp_path: Path) -> None:
    """Rebuild twice without disk change: second run is no-op."""
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "foo.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/foo.schema.json", "version": "1.0.0"}))
    (sd / "schema-refs.json").write_text(json.dumps({
        "version": "1.0.0", "schemas": {}, "meta": {"version": "1.0.0", "changelog": []}}))
    refs_rebuild_cmd(check=False, registry_root=str(tmp_path))
    first = (sd / "schema-refs.json").read_text()
    refs_rebuild_cmd(check=False, registry_root=str(tmp_path))
    second = (sd / "schema-refs.json").read_text()
    assert first == second


def test_refs_rebuild_missing_refs_file_treats_as_empty(tmp_path: Path) -> None:
    """No existing schema-refs.json: rebuild creates one."""
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "foo.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/foo.schema.json", "version": "1.0.0"}))
    exit_code = refs_rebuild_cmd(check=False, registry_root=str(tmp_path))
    assert exit_code == 0
    assert (sd / "schema-refs.json").exists()
    doc = json.loads((sd / "schema-refs.json").read_text())
    assert "foo" in doc["schemas"]


def test_refs_rebuild_check_no_refs_file_drift(tmp_path: Path, capsys) -> None:
    """No refs file but schemas on disk: --check reports drift."""
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "foo.schema.json").write_text(json.dumps({
        "$id": "https://schemas.luh.tech/foo.schema.json", "version": "1.0.0"}))
    exit_code = refs_rebuild_cmd(check=True, registry_root=str(tmp_path))
    assert exit_code == 1


def test_refs_rebuild_unreadable_refs_file_exits_2(tmp_path: Path, capsys) -> None:
    """Malformed schema-refs.json returns exit code 2."""
    sd = tmp_path / "schemas"
    sd.mkdir()
    (sd / "schema-refs.json").write_text("not json {")
    exit_code = refs_rebuild_cmd(check=False, registry_root=str(tmp_path))
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "ERROR" in captured.err
