#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from PIL import Image

from integration_common import INTEGRATION_PATH, VALIDATION_PATH, build_rows, resolve_candidate, sha256, write_json


def validate(rows: list[dict]) -> dict:
    by_group: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_group[row["animation_group"]].append(row)
    results = []
    for row in rows:
        path = resolve_candidate(row["candidate"])
        errors: list[str] = []
        warnings: list[str] = []
        candidate_width = candidate_height = None
        candidate_sha = None
        if path is not None:
            if not path.is_file():
                errors.append("candidate file is missing")
            else:
                try:
                    with Image.open(path) as image:
                        image.verify()
                    with Image.open(path) as image:
                        candidate_width, candidate_height = image.size
                        if image.format != "PNG":
                            errors.append("candidate must be PNG")
                except Exception as exc:
                    errors.append(f"invalid image: {exc}")
                if candidate_width and candidate_height:
                    # TITLE blocks 3 and 4 are partial DAX updates, but every
                    # retained HD title is an accumulated full-screen plate.
                    # The title lifecycle therefore validates the 320x200
                    # presentation canvas rather than the partial block crop.
                    source_ratio = 8 / 5 if row["lifecycle"] == "title_sequence" else row["width"] / row["height"]
                    candidate_ratio = candidate_width / candidate_height
                    ratio_error = abs(candidate_ratio - source_ratio) / source_ratio
                    tolerance = max(0.001, 1.0 / max(candidate_width, candidate_height))
                    if ratio_error > tolerance:
                        errors.append(
                            f"aspect ratio mismatch: source {'8:5 full-screen title' if row['lifecycle'] == 'title_sequence' else row['aspect_ratio']}, "
                            f"candidate {candidate_width}x{candidate_height}"
                        )
                    if max(candidate_width, candidate_height) < 1024:
                        errors.append("candidate resolution is below the 1024-pixel minimum")
                    if min(candidate_width, candidate_height) < min(row["width"], row["height"]):
                        errors.append("candidate is smaller than the source frame")
                    candidate_sha = sha256(path)
        if row["animated"] and row["review_status"] == "approved":
            incomplete = [r["identity"] for r in by_group[row["animation_group"]] if r["review_status"] != "approved"]
            if incomplete:
                errors.append("animated block is only partially approved")
        if row["review_status"] == "approved" and not row["candidate"]:
            errors.append("approved entry has no candidate")
        if row["review_status"] == "rejected" and row["candidate"]:
            warnings.append("candidate retained for review history but is not stageable")
        if row["lifecycle_status"] != "verified" and row["review_status"] == "approved":
            errors.append("approved art lacks verified lifecycle status")
        stageable = (
            row["review_status"] == "approved" and
            row["lifecycle_status"] == "verified" and
            path is not None and not errors
        )
        results.append({
            "identity": row["identity"],
            "candidate": row["candidate"],
            "candidate_width": candidate_width,
            "candidate_height": candidate_height,
            "candidate_sha256": candidate_sha,
            "errors": errors,
            "warnings": warnings,
            "stageable": stageable,
        })

    # TITLE blocks are one retained full-sequence lifecycle. Never permit a
    # partially approved set to hide an original DAX fallback block.
    title_rows = [row for row in rows if row["archive"] == "TITLE.DAX"]
    title_results = {item["identity"]: item for item in results if item["identity"].startswith("TITLE.DAX:")}
    if any(row["review_status"] == "approved" for row in title_rows):
        complete = len(title_rows) == 4 and all(title_results[row["identity"]]["stageable"] for row in title_rows)
        if not complete:
            for row in title_rows:
                if row["review_status"] == "approved":
                    item = title_results[row["identity"]]
                    item["errors"].append("title sequence is not approved as a complete four-block set")
                    item["stageable"] = False
    return {
        "ledger_entries": len(rows),
        "candidate_entries": sum(bool(row["candidate"]) for row in rows),
        "stageable_entries": sum(item["stageable"] for item in results),
        "invalid_candidate_entries": sum(bool(item["errors"]) for item in results if item["candidate"]),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    rows = build_rows()
    write_json(INTEGRATION_PATH, rows)
    report = validate(rows)
    write_json(VALIDATION_PATH, report)
    approved = {row["identity"] for row in rows if row["review_status"] == "approved"}
    failures = [item for item in report["results"] if item["identity"] in approved and not item["stageable"]]
    print(f"validated {report['ledger_entries']} entries; candidate entries={report['candidate_entries']}; stageable={report['stageable_entries']}")
    if args.strict and failures:
        raise SystemExit(f"{len(failures)} approved candidates failed validation")


if __name__ == "__main__":
    main()
