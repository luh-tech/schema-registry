"""luhtech-schema CLI dispatch. T0 scope: validate only."""

from __future__ import annotations

import argparse
import sys

from luhtech_schema import __version__
from luhtech_schema.validate import validate_path, validate_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="luhtech-schema",
        description="Schema-first validation substrate for LuhTech Holdings.",
    )
    parser.add_argument("--version", action="version", version=f"luhtech-schema {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_p = subparsers.add_parser("validate", help="Validate a path or the full registry.")
    validate_p.add_argument("target", help="File path to validate, or 'registry' for registry-wide validation.")
    validate_p.add_argument("--registry-root", default=".", help="Repository root for registry validation.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "validate":
        if args.target == "registry":
            return validate_registry(args.registry_root)
        return validate_path(args.target)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
