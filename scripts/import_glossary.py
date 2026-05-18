"""One-shot import: canonical_glossary_v1.2.md → acronyms-catalog.json.

Run from repo root:
    python3 scripts/import_glossary.py

Deterministic regex parse. Halts on id collisions or malformed rows.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

SRC = Path("sources/canonical_glossary_v1.2.md")
OUT = Path("schemas/acronyms-catalog.json")
STREAM_URL = "https://schemas.luh.tech/acronyms-catalog.json"
SCHEMA_URL = "https://schemas.luh.tech/acronyms-catalog.schema.json"

text = SRC.read_text(encoding="utf-8")

# Matches: **A. Section Title** or **E2. Section Title  \[PATENT-OWNED\]**
SECTION_RE = re.compile(
    r"^\*\*([A-Z][0-9]?)\.\s+([^*\[\n]+?)(?:\s+\\\[([A-Z-]+)\\\])?\s*\*\*\s*$",
    re.MULTILINE,
)

STATUS_LEGEND = {
    "LOCKED": "definition fixed, used in filings as-is.",
    "PATENT-OWNED": "defined here; catalog defers to this Glossary.",
    "DEPRECATED": "historical term, retained for cross-reference only.",
}


def slugify_id(term: str) -> str:
    s = term.strip().strip("*").strip().strip("\"'")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    keep = []
    for c in s:
        if c.isalnum() or c in ("_", "§"):
            keep.append(c.upper())
        elif c in " -/.()":
            keep.append("_")
    return re.sub(r"_+", "_", "".join(keep)).strip("_")


def derive_status(source_status: str) -> str:
    s = source_status.upper()
    if "DEPRECATED" in s or "PROHIBITED" in s:
        return "DEPRECATED"
    if "PATENT-OWNED" in s:
        return "PATENT-OWNED"
    return "LOCKED"


def parse_row(line: str) -> list[str] | None:
    if re.match(r"^\|[\s:-]+\|", line):
        return None
    if not line.strip().startswith("|"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells if len(cells) == 4 else None


def clean_cell(s: str) -> str:
    replacements = [
        (r"\.", "."), (r"\[", "["), (r"\]", "]"), (r"\+", "+"),
        (r"\$", "$"), (r"\(", "("), (r"\)", ")"), (r"\~", "~"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    s = re.sub(r"^\*+", "", s)
    s = re.sub(r"\*+$", "", s)
    return s.strip()


sections = []
matches = list(SECTION_RE.finditer(text))
for i, m in enumerate(matches):
    sec_id = m.group(1)
    sec_title = m.group(2).strip()
    sec_tag = m.group(3) or ""
    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
    sections.append({
        "id": sec_id,
        "title": sec_title,
        "body": text[start:end],
        "ownership": "patent-owned" if sec_tag == "PATENT-OWNED" else "catalog-derived",
    })

if not sections:
    print("FATAL: no sections matched. Check SECTION_RE against glossary format.", file=sys.stderr)
    sys.exit(1)

print(f"Parsed {len(sections)} sections")

terms_by_id: dict[str, dict] = {}
collisions: list[tuple[str, str, str]] = []
section_records = []

for sec in sections:
    section_records.append({"id": sec["id"], "title": sec["title"], "ownership": sec["ownership"]})
    n = 0
    for line in sec["body"].splitlines():
        cells = parse_row(line)
        if not cells:
            continue
        if cells[0].lower().strip("*") == "term":
            continue
        term_raw, expansion_raw, definition_raw, source_status_raw = cells
        term = clean_cell(term_raw)
        if not term:
            continue
        expansion = clean_cell(expansion_raw)
        if expansion in {"—", "-", ""}:
            expansion = None
        definition = clean_cell(definition_raw)
        source_status = clean_cell(source_status_raw)
        status = derive_status(source_status)
        tid = slugify_id(term)
        if not tid:
            print(f"  WARN: empty id from {term!r} in {sec['id']}", file=sys.stderr)
            continue
        if tid in terms_by_id:
            tid2 = f"{tid}_{sec['id']}"
            if tid2 in terms_by_id:
                collisions.append((tid, terms_by_id[tid]["section"], sec["id"]))
                continue
            tid = tid2
        terms_by_id[tid] = {
            "id": tid, "term": term, "expansion": expansion,
            "definition": definition, "sourceStatus": source_status,
            "status": status, "section": sec["id"], "sectionTitle": sec["title"],
        }
        n += 1
    print(f"  Section {sec['id']:2} ({sec['title'][:50]:50}) — {n} terms")

if collisions:
    print(f"\nHALT: {len(collisions)} id collisions:", file=sys.stderr)
    for tid, a, b in collisions:
        print(f"  {tid}: section {a} vs {b}", file=sys.stderr)
    sys.exit(2)

terms = list(terms_by_id.values())
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

doc = {
    "$schema": SCHEMA_URL,
    "streamUrl": STREAM_URL,
    "version": "1.2.0",
    "documentId": "ACRONYMS-CATALOG",
    "title": "LuhTech Canonical Glossary / Acronyms Catalog",
    "description": (
        f"Canonical LuhTech vocabulary at {STREAM_URL}. "
        "Ingested from canonical_glossary_v1.2 (2026-05-05). "
        "Patent-owned sections (B, D, E, E2) are primary; other sections are catalog-derived."
    ),
    "lastUpdated": now,
    "author": "Erik Luhtala",
    "sourceMaterial": "sources/canonical_glossary_v1.2.md",
    "scope": {
        "inScope": [
            "LuhTech-coined terms across ten ventures",
            "Industry-standard construction acronyms in active use",
            "Third-party standards, specifications, and regulations",
            "Construction roles, document types, contract forms",
            "Carbon and MRV terminology",
            "Patent-owned cryptographic and positioning vocabulary",
            "Patent law shorthand and Procopio drafting conventions",
            "Prohibited and deprecated terms (with supersession)",
        ],
        "outOfScope": [
            "Quantitative claims and stats — separate provenance system",
            "Per-venture domain assignments — covered by url-catalog.json",
            "Speculative names not yet realized",
        ],
    },
    "statusLegend": STATUS_LEGEND,
    "sections": section_records,
    "terms": terms,
    "_meta": {
        "termCount": len(terms),
        "sectionCount": len(section_records),
        "deprecatedCount": sum(1 for t in terms if t["status"] == "DEPRECATED"),
        "patentOwnedCount": sum(1 for t in terms if t["status"] == "PATENT-OWNED"),
        "lockedCount": sum(1 for t in terms if t["status"] == "LOCKED"),
        "generatedBy": "scripts/import_glossary.py (T1 one-shot)",
        "generatedAt": now,
    },
}

OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print()
print(f"wrote {OUT}")
print(f"  total terms:  {len(terms)}")
print(f"  sections:     {len(section_records)}")
print(f"  LOCKED:       {doc['_meta']['lockedCount']}")
print(f"  PATENT-OWNED: {doc['_meta']['patentOwnedCount']}")
print(f"  DEPRECATED:   {doc['_meta']['deprecatedCount']}")
