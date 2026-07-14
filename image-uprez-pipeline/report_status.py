#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from integration_common import build_rows
from validate_candidates import validate

parser = argparse.ArgumentParser()
parser.add_argument("--runtime", type=Path)
parser.add_argument("--json", action="store_true")
args = parser.parse_args()
rows = build_rows()
checks = validate(rows)
integrated = 0
if args.runtime and (args.runtime / "runtime-lookup.tsv").is_file():
    with (args.runtime / "runtime-lookup.tsv").open(newline="") as handle:
        integrated = sum(row["stage_status"] == "integrated" for row in csv.DictReader(handle, dialect="excel-tab"))
report = {
    "ledger_entries": len(rows),
    "generated_entries": sum(bool(row["candidate"]) for row in rows),
    "review_candidate_files": len(list((Path(__file__).resolve().parent / "review-candidates").rglob("*.png"))),
    "missing_entries": sum(not row["candidate"] for row in rows),
    "approved_entries": sum(row["review_status"] == "approved" for row in rows),
    "rejected_entries": sum(row["review_status"] == "rejected" for row in rows),
    "stageable_entries": checks["stageable_entries"],
    "integrated_entries": integrated,
}
print(json.dumps(report, indent=2) if args.json else " ".join(f"{key}={value}" for key, value in report.items()))
