"""Smoke tests for the T1 acronyms subcommands."""
from __future__ import annotations
import json
from pathlib import Path
from luhtech_schema.acronyms import _build_index, check, extract_candidate_terms, register

SAMPLE_CATALOG = {
    "$schema": "https://schemas.luh.tech/acronyms-catalog.schema.json",
    "streamUrl": "https://schemas.luh.tech/acronyms-catalog.json",
    "version": "1.2.0", "lastUpdated": "2026-05-17T00:00:00Z", "author": "Erik Luhtala",
    "terms": [
        {"id": "SBPA", "term": "SBPA", "expansion": "Spatially-Bound Provenance Architecture",
         "definition": "Umbrella.", "sourceStatus": "LOCKED", "status": "LOCKED", "section": "A"},
        {"id": "CTA", "term": "CTA", "expansion": None, "definition": "Former name.",
         "sourceStatus": "DEPRECATED", "status": "DEPRECATED", "supersededBy": "SBPA", "section": "A"},
        {"id": "RVGT", "term": "RVGT", "expansion": "Rolling Validated Ground Truth",
         "definition": "Hash-chained.", "sourceStatus": "PATENT-OWNED", "status": "PATENT-OWNED", "section": "B"},
    ],
}

def test_extract_candidate_terms_finds_acronyms():
    tokens = extract_candidate_terms("The SBPA and RVGT primitives compose.")
    assert "SBPA" in tokens and "RVGT" in tokens

def test_extract_skips_dedup():
    assert extract_candidate_terms("SBPA SBPA SBPA").count("SBPA") == 1

def test_build_index_keys():
    idx = _build_index(SAMPLE_CATALOG)
    assert "SBPA" in idx and idx["SBPA"]["id"] == "SBPA"

def test_check_known_terms_pass(tmp_path):
    p = tmp_path / "catalog.json"; p.write_text(json.dumps(SAMPLE_CATALOG))
    assert check("The SBPA architecture uses RVGT chains.", local=str(p)) == 0

def test_check_unknown_term_fails(tmp_path):
    p = tmp_path / "catalog.json"; p.write_text(json.dumps(SAMPLE_CATALOG))
    # MYSTERYTHING: natural-language acronym (no underscores); _TERM_RE matches [A-Z][A-Z0-9§]{1,}
    assert check("MYSTERYTHING appears in the text.", local=str(p)) == 1

def test_check_deprecated_term_fails(tmp_path):
    p = tmp_path / "catalog.json"; p.write_text(json.dumps(SAMPLE_CATALOG))
    assert check("Legacy CTA reference.", local=str(p)) == 1

def test_register_emits_valid_json(capsys):
    exit_code = register("FOO_BAR", expansion="Foo Bar", definition="Demo.", section="K")
    captured = capsys.readouterr()
    assert exit_code == 0
    parsed = json.loads(captured.out.split("\n\n")[0])
    assert parsed["id"] == "FOO_BAR" and parsed["status"] == "LOCKED"
