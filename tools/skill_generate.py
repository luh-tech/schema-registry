#!/usr/bin/env python3
"""
skill_generate.py — Deterministic JSON-to-SKILL.md transform.

Reads a skill-instance.json file, validates it against skill.schema.json,
and writes a SKILL.md sibling file. Output is byte-stable across re-runs.

Per LuhTech canonical pattern: JSON is the truth, SKILL.md is generated.
Memory rule 19 (no-md-terminus) — markdown is never the home of truth.

Usage: python3 tools/skill_generate.py <path-to-skill-instance.json>
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("ERROR: jsonschema package required. pip install jsonschema", file=sys.stderr)
    sys.exit(2)

GENERATOR_VERSION = "1.0.0"
SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "skill.schema.json"


def load_schema():
    if not SCHEMA_PATH.exists():
        print(f"ERROR: schema not found at {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)
    return json.loads(SCHEMA_PATH.read_text())


def validate_instance(instance, schema):
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    if errors:
        print("ERROR: skill instance fails schema validation:", file=sys.stderr)
        for err in errors:
            path = ".".join(str(p) for p in err.path) or "(root)"
            print(f"  {path}: {err.message}", file=sys.stderr)
        sys.exit(1)


def yaml_frontmatter(instance):
    lines = ["---"]
    lines.append(f"name: {instance['name']}")
    desc = instance["description"].replace('"', '\\"')
    lines.append(f'description: "{desc}"')
    lines.append(f"version: {instance['version']}")
    lines.append(f"category: {instance['category']}")
    lines.append(f"lifecycleStatus: {instance['lifecycleStatus']}")
    lines.append(f"triggerMode: {instance['triggerMode']}")
    compat = instance.get("compatibility")
    if compat:
        lines.append("compatibility:")
        if compat.get("environments"):
            lines.append("  environments:")
            for env in compat["environments"]:
                lines.append(f"    - {env}")
        if compat.get("requiredTools"):
            lines.append("  requiredTools:")
            for t in compat["requiredTools"]:
                lines.append(f"    - {t}")
        if compat.get("dependencies"):
            lines.append("  dependencies:")
            for d in compat["dependencies"]:
                lines.append(f"    - {d}")
    lines.append("---")
    return "\n".join(lines)


def render_body(instance):
    out = []
    out.append(f"# {instance['name']}")
    out.append("")
    out.append(instance["behavior"]["summary"])
    out.append("")

    out.append("## When this skill fires")
    out.append("")
    for ctx in instance["triggerContext"]:
        out.append(f"**{ctx['precondition']}**")
        out.append("")
        out.append("Example cues:")
        for cue in ctx["exampleCues"]:
            out.append(f"- {cue}")
        out.append("")

    out.append("## Behavior")
    out.append("")
    for i, d in enumerate(instance["behavior"]["directives"], 1):
        out.append(f"{i}. **{d['action']}**")
        out.append(f"   {d['rationale']}")
        out.append("")

    anti = instance["behavior"].get("antiPatterns") or []
    if anti:
        out.append("## Anti-patterns")
        out.append("")
        for ap in anti:
            out.append(f"- DO NOT: {ap['pattern']}")
            out.append(f"  INSTEAD: {ap['instead']}")
        out.append("")

    examples = instance.get("examples") or []
    if examples:
        out.append("## Examples")
        out.append("")
        for ex in examples:
            out.append(f"**Scenario:** {ex['scenario']}")
            out.append("")
            out.append(f"**Expected:** {ex['expectedBehavior']}")
            if ex.get("antiExample"):
                out.append("")
                out.append(f"**Anti-example:** {ex['antiExample']}")
            out.append("")

    boundaries = instance.get("boundaryConditions") or []
    if boundaries:
        out.append("## Boundary conditions (when this skill does NOT fire)")
        out.append("")
        for b in boundaries:
            out.append(f"- {b}")
        out.append("")

    paired = instance.get("pairedRule")
    if paired:
        out.append("## Paired rule")
        out.append("")
        out.append(f"This skill pairs with rule instance: `{paired}`")
        out.append("")

    refs = instance.get("references") or []
    if refs:
        out.append("## References")
        out.append("")
        for r in refs:
            line = f"- [{r['type']}] {r['location']}"
            if r.get("purpose"):
                line += f" — {r['purpose']}"
            out.append(line)
        out.append("")

    out.append("## Governance")
    out.append("")
    out.append(f"- Author: {instance['authority']['author']}")
    out.append(f"- Approver: {instance['authority']['approver']}")
    out.append(f"- Revert authority: {instance['authority']['revertAuthority']}")
    out.append("")

    return "\n".join(out)


def generate(instance_path: Path, deterministic_timestamp: str = None):
    schema = load_schema()
    instance_text = instance_path.read_text()
    instance = json.loads(instance_text)
    validate_instance(instance, schema)

    source_sha = hashlib.sha256(instance_text.encode()).hexdigest()
    # For SHA-stable output across runs, derive timestamp from source SHA
    # rather than wall clock. CI compares regenerated MD to committed MD;
    # wall-clock timestamps would cause false drift failures.
    if deterministic_timestamp is None:
        # Use the source JSON's first transition timestamp if present,
        # else a constant epoch marker. NEVER wall clock.
        transitions = instance.get("transitions", [])
        ts = None
        if transitions:
            ts = transitions[-1].get("transitionedAt")
        deterministic_timestamp = ts or "0000-00-00T00:00:00Z"

    frontmatter = yaml_frontmatter(instance)
    body = render_body(instance)
    footer = (
        f"\n<!-- generated by luhtech-skill-generate v{GENERATOR_VERSION} "
        f"from sha256:{source_sha} at {deterministic_timestamp} -->\n"
    )

    md = frontmatter + "\n\n" + body + footer
    md_path = instance_path.parent / "SKILL.md"
    md_path.write_text(md)
    print(f"Generated: {md_path}")
    print(f"  Source SHA: {source_sha[:16]}...")
    return md_path


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-skill-instance.json>", file=sys.stderr)
        sys.exit(2)
    instance_path = Path(sys.argv[1])
    if not instance_path.exists():
        print(f"ERROR: {instance_path} not found", file=sys.stderr)
        sys.exit(2)
    generate(instance_path)


if __name__ == "__main__":
    main()
