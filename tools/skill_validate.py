#!/usr/bin/env python3
"""
skill_validate.py — Validates skill-instance.json files against skill.schema.json.

Usage: python3 tools/skill_validate.py <path-to-skill-instance.json>
Exit 0 on pass, non-zero on fail with structured error output.
"""
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("ERROR: jsonschema package required. pip install jsonschema", file=sys.stderr)
    sys.exit(2)

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "skill.schema.json"


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-skill-instance.json>", file=sys.stderr)
        sys.exit(2)

    instance_path = Path(sys.argv[1])
    if not instance_path.exists():
        print(f"ERROR: {instance_path} not found", file=sys.stderr)
        sys.exit(2)

    if not SCHEMA_PATH.exists():
        print(f"ERROR: schema not found at {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)

    schema = json.loads(SCHEMA_PATH.read_text())
    instance = json.loads(instance_path.read_text())

    Draft7Validator.check_schema(schema)
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))

    if errors:
        print(f"FAIL: {instance_path}")
        for err in errors:
            path = ".".join(str(p) for p in err.path) or "(root)"
            print(f"  {path}: {err.message}")
        sys.exit(1)

    print(f"PASS: {instance_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
