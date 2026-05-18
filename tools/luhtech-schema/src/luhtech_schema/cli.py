"""luhtech-schema CLI dispatch. T4: validate, acronyms, classify, map, migrate."""
from __future__ import annotations
import argparse, sys
from luhtech_schema import __version__
from luhtech_schema.validate import validate_path, validate_registry
from luhtech_schema.acronyms import check as acronyms_check, register as acronyms_register
from luhtech_schema.classify import classify_cmd
from luhtech_schema.schema_map import map_cmd
from luhtech_schema.migrate import migrate_cmd

def build_parser():
    p = argparse.ArgumentParser(prog="luhtech-schema", description="Schema-first validation substrate for LuhTech Holdings.")
    p.add_argument("--version", action="version", version=f"luhtech-schema {__version__}")
    sp = p.add_subparsers(dest="command", required=True)

    vp = sp.add_parser("validate"); vp.add_argument("target"); vp.add_argument("--registry-root", default=".")
    ap = sp.add_parser("acronyms"); asp = ap.add_subparsers(dest="acro_command", required=True)
    cp = asp.add_parser("check"); cp.add_argument("text"); cp.add_argument("--local", default=None); cp.add_argument("--stream-url", default=None)
    rp = asp.add_parser("register"); rp.add_argument("term"); rp.add_argument("--expansion", default=None); rp.add_argument("--definition", default=None); rp.add_argument("--section", default="K")
    clp = sp.add_parser("classify"); clp.add_argument("target"); clp.add_argument("--registry-root", default=".")
    mp = sp.add_parser("map"); mp.add_argument("--registry-root", default=".")
    mp.add_argument("--include-ectropy-domain", default=None,
                    help="Path to ectropy-ai/schemas root for L11 inclusion.")
    mig = sp.add_parser("migrate"); mig_sp = mig.add_subparsers(dest="mig_command", required=True)
    av = mig_sp.add_parser("add-versions"); av.add_argument("--registry-root", default="."); av.add_argument("--apply", action="store_true")
    return p

def main(argv=None):
    parser = build_parser(); args = parser.parse_args(argv)
    if args.command == "validate":
        return validate_registry(args.registry_root) if args.target == "registry" else validate_path(args.target)
    if args.command == "acronyms":
        if args.acro_command == "check": return acronyms_check(args.text, stream_url=args.stream_url, local=args.local)
        if args.acro_command == "register": return acronyms_register(args.term, expansion=args.expansion, definition=args.definition, section=args.section)
    if args.command == "classify": return classify_cmd(args.target, registry_root=args.registry_root)
    if args.command == "map": return map_cmd(registry_root=args.registry_root, include_ectropy_domain=args.include_ectropy_domain)
    if args.command == "migrate": return migrate_cmd(args.mig_command, registry_root=args.registry_root, apply=args.apply)
    parser.print_help(); return 2

if __name__ == "__main__": sys.exit(main())
