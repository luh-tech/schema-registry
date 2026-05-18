"""luhtech-schema CLI dispatch. T1: validate + acronyms."""
from __future__ import annotations
import argparse, sys
from luhtech_schema import __version__
from luhtech_schema.validate import validate_path, validate_registry
from luhtech_schema.acronyms import check as acronyms_check, register as acronyms_register

def build_parser():
    p = argparse.ArgumentParser(prog="luhtech-schema", description="Schema-first validation substrate for LuhTech Holdings.")
    p.add_argument("--version", action="version", version=f"luhtech-schema {__version__}")
    sp = p.add_subparsers(dest="command", required=True)

    vp = sp.add_parser("validate", help="Validate a path/URL or the full registry.")
    vp.add_argument("target", help="Local path, http(s) URL, or \'registry\' for registry-wide validation.")
    vp.add_argument("--registry-root", default=".", help="Repository root for registry validation.")

    ap = sp.add_parser("acronyms", help="Acronyms catalog operations.")
    asp = ap.add_subparsers(dest="acro_command", required=True)

    cp = asp.add_parser("check", help="Check input text against the canonical catalog.")
    cp.add_argument("text"); cp.add_argument("--local", default=None); cp.add_argument("--stream-url", default=None)

    rp = asp.add_parser("register", help="Emit a starter catalog entry for a new term.")
    rp.add_argument("term"); rp.add_argument("--expansion", default=None)
    rp.add_argument("--definition", default=None); rp.add_argument("--section", default="K")

    return p

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "validate":
        return validate_registry(args.registry_root) if args.target == "registry" else validate_path(args.target)
    if args.command == "acronyms":
        if args.acro_command == "check":
            return acronyms_check(args.text, stream_url=args.stream_url, local=args.local)
        if args.acro_command == "register":
            return acronyms_register(args.term, expansion=args.expansion, definition=args.definition, section=args.section)
    parser.print_help(); return 2

if __name__ == "__main__":
    sys.exit(main())
