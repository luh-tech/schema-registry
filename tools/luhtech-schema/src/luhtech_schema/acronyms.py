"""acronyms subcommand surface — T1.

Implements `acronyms check <text>` and `acronyms register <term>`.

Catalog is loaded from its canonical stream URL by default (D9):
    https://schemas.luh.tech/acronyms-catalog.json

Pass --local <path> to read from disk for offline dev / pre-commit hooks.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

CATALOG_STREAM_URL = "https://schemas.luh.tech/acronyms-catalog.json"

# Tokens that look like acronyms or canonical identifiers
_TERM_RE = re.compile(r"\b([A-Z][A-Z0-9§]{1,}|[A-Z][a-z]+[A-Z][A-Za-z0-9]*)\b")


def _load_catalog(stream_url: str | None, local: str | None) -> dict:
    if local:
        return json.loads(Path(local).read_text(encoding="utf-8"))
    url = stream_url or CATALOG_STREAM_URL
    try:
        with urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except URLError as e:
        raise RuntimeError(f"failed to fetch catalog from {url}: {e}") from e


def _build_index(catalog: dict) -> dict[str, dict]:
    """Build uppercase lookup: id / term / alias → entry."""
    index: dict[str, dict] = {}
    for entry in catalog.get("terms", []):
        index[entry["id"].upper()] = entry
        index[entry["term"].upper()] = entry
        for alias in entry.get("aliases", []) or []:
            index[alias.upper()] = entry
    return index


def extract_candidate_terms(text: str) -> list[str]:
    """Return ordered unique candidate-term tokens from input text."""
    seen: set[str] = set()
    out: list[str] = []
    for m in _TERM_RE.finditer(text):
        tok = m.group(1)
        key = tok.upper()
        if key in seen:
            continue
        seen.add(key)
        out.append(tok)
    return out


def check(
    text: str,
    *,
    stream_url: str | None = None,
    local: str | None = None,
) -> int:
    """Scan input text for acronyms and report against catalog. Returns exit code."""
    catalog = _load_catalog(stream_url, local)
    index = _build_index(catalog)

    candidates = extract_candidate_terms(text)
    known: list[tuple[str, str]] = []
    unknown: list[str] = []
    deprecated: list[tuple[str, str]] = []

    for tok in candidates:
        entry = index.get(tok.upper())
        if entry is None:
            unknown.append(tok)
        elif entry.get("status") == "DEPRECATED":
            deprecated.append((tok, entry.get("supersededBy") or ""))
        else:
            known.append((tok, entry["id"]))

    src = f"local: {local}" if local else f"stream: {stream_url or CATALOG_STREAM_URL}"
    print("=== luhtech-schema acronyms check ===")
    print(f"source:     {src}")
    print(f"candidates: {len(candidates)}")
    print(f"known:      {len(known)}")
    print(f"deprecated: {len(deprecated)}")
    print(f"unknown:    {len(unknown)}")

    if deprecated:
        print()
        print("Deprecated terms (status=DEPRECATED in catalog):")
        for tok, replacement in deprecated:
            print(f"  {tok}" + (f" → {replacement}" if replacement else ""))

    if unknown:
        print()
        print("Unknown terms (not in catalog):")
        for tok in unknown:
            print(f"  {tok}")

    return 0 if (not unknown and not deprecated) else 1


def register(
    term: str,
    expansion: str | None = None,
    definition: str | None = None,
    section: str = "K",
) -> int:
    """Emit a starter catalog entry JSON for a new term. T1: stdout only."""
    s = unicodedata.normalize("NFKD", term)
    s = "".join(c for c in s if not unicodedata.combining(c))
    slug_chars = []
    for c in s:
        if c.isalnum() or c == "_":
            slug_chars.append(c.upper())
        elif c in " -/.()":
            slug_chars.append("_")
    tid = re.sub(r"_+", "_", "".join(slug_chars)).strip("_")

    entry = {
        "id": tid,
        "term": term,
        "expansion": expansion,
        "definition": definition or "TODO — define this term before registering.",
        "sourceStatus": "PENDING · TODO",
        "status": "LOCKED",
        "section": section,
        "sectionTitle": "(set by reviewer)",
    }
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    print()
    print(
        "Next step: add this entry to acronyms-catalog.json under .terms[], "
        "verify section, and open a PR. T7+ will make this interactive via MCP."
    )
    return 0
