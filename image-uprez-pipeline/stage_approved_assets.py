#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import shutil
import tempfile
import json
from pathlib import Path

from integration_common import build_rows, resolve_candidate, sha256
from validate_candidates import validate

FIELDS = [
    "identity", "archive", "area", "block", "frame", "width", "height", "x", "y",
    "aspect_ratio", "animated", "delay", "animation_group", "animation_frame_count",
    "lifecycle", "runtime_name", "review_status", "lifecycle_status", "stage_status",
    "runtime_path", "candidate_sha256"
]

PIPELINE = Path(__file__).resolve().parent
PROTECTED_LOCK = PIPELINE / "nextgen" / "protected-assets.json"


def assert_protected_assets_unchanged(rows: list[dict], checks: dict[str, dict]) -> None:
    """Do not let a future staging run replace an accepted HD asset.

    The lock is intentionally opt-in for legacy checkouts.  Once created, a
    protected identity must remain stageable from byte-identical candidate art.
    New identities are unaffected.
    """
    if not PROTECTED_LOCK.is_file():
        return
    lock = json.loads(PROTECTED_LOCK.read_text())
    entries = {item["identity"]: item for item in lock.get("protected_entries", [])}
    for row in rows:
        protected = entries.get(row["identity"])
        if protected is None:
            continue
        check = checks[row["identity"]]
        source = resolve_candidate(row["candidate"])
        if not check["stageable"] or source is None:
            raise RuntimeError(
                f"protected asset {row['identity']} would be removed or unstaged; "
                "create a new identity instead"
            )
        actual = sha256(source)
        if actual != protected["candidate_sha256"]:
            raise RuntimeError(
                f"protected asset {row['identity']} would change; explicit approval and a new lock are required"
            )


def stage(destination: Path) -> dict:
    rows = build_rows()
    checks = {item["identity"]: item for item in validate(rows)["results"]}
    assert_protected_assets_unchanged(rows, checks)
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    managed = destination / "integrated"
    temp = Path(tempfile.mkdtemp(prefix=".integrated-", dir=destination))
    integrated = 0
    try:
        runtime_rows = []
        for row in rows:
            check = checks[row["identity"]]
            runtime_path = ""
            stage_status = "missing"
            if row["candidate"]:
                stage_status = "review_pending"
            if row["review_status"] == "rejected":
                stage_status = "rejected"
            if check["stageable"]:
                source = resolve_candidate(row["candidate"])
                shutil.copy2(source, temp / row["runtime_name"])
                runtime_path = f"integrated/{row['runtime_name']}"
                stage_status = "integrated"
                integrated += 1
            runtime_rows.append({
                **{field: row.get(field, "") for field in FIELDS},
                "stage_status": stage_status,
                "runtime_path": runtime_path,
                "candidate_sha256": check["candidate_sha256"] or "",
            })
        backup = destination / ".integrated-old"
        if backup.exists():
            shutil.rmtree(backup)
        if managed.exists():
            os.replace(managed, backup)
        os.replace(temp, managed)
        if backup.exists():
            shutil.rmtree(backup)
        manifest_tmp = destination / ".runtime-lookup.tsv.tmp"
        with manifest_tmp.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, dialect="excel-tab", extrasaction="ignore")
            writer.writeheader()
            writer.writerows(runtime_rows)
        os.replace(manifest_tmp, destination / "runtime-lookup.tsv")
    except Exception:
        if temp.exists():
            shutil.rmtree(temp)
        raise
    return {
        "ledger_entries": len(rows),
        "generated_entries": sum(bool(row["candidate"]) for row in rows),
        "integrated_entries": integrated,
        "missing_entries": sum(not row["candidate"] for row in rows),
        "review_or_lifecycle_gated_entries": sum(bool(row["candidate"]) and not checks[row["identity"]]["stageable"] for row in rows),
        "destination": str(destination),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    report = stage(args.destination)
    print(f"ledger={report['ledger_entries']} generated={report['generated_entries']} missing={report['missing_entries']} integrated={report['integrated_entries']} review_or_lifecycle_gated={report['review_or_lifecycle_gated_entries']}")


if __name__ == "__main__":
    main()
