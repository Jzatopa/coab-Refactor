#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from integration_common import build_rows

parser = argparse.ArgumentParser()
parser.add_argument("archive", nargs="?")
parser.add_argument("block", nargs="?", type=int)
parser.add_argument("frame", nargs="?", type=int, default=0)
parser.add_argument("--all", action="store_true")
args = parser.parse_args()
rows = build_rows()
if args.all:
    print(json.dumps({row["identity"]: row["runtime_name"] for row in rows}, indent=2))
else:
    if args.archive is None or args.block is None:
        parser.error("archive and block are required unless --all is used")
    archive = args.archive.upper()
    if not archive.endswith(".DAX"):
        archive += ".DAX"
    key = f"{archive}:{args.block:03d}:{args.frame:03d}"
    match = next((row for row in rows if row["identity"] == key), None)
    if match is None:
        raise SystemExit(f"no ledger entry for {key}")
    print(match["runtime_name"])
