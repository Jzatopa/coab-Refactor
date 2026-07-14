#!/usr/bin/env python3
from __future__ import annotations

import csv
import tempfile
from pathlib import Path

from integration_common import build_rows
from stage_approved_assets import stage
from validate_candidates import validate

rows = build_rows()
assert len(rows) == 231
assert len({row["identity"] for row in rows}) == 231
assert len({row["runtime_name"] for row in rows}) == 231
assert all(row["animation_frame_count"] >= 1 for row in rows)
validation = validate(rows)
assert validation["stageable_entries"] == 5
rejected = next(row for row in rows if row["identity"] == "PIC1.DAX:001:000")
assert rejected["review_status"] == "rejected"
with tempfile.TemporaryDirectory() as temp:
    destination = Path(temp) / "HDAssets"
    report = stage(destination)
    assert report["integrated_entries"] == 5
    with (destination / "runtime-lookup.tsv").open(newline="") as handle:
        staged = list(csv.DictReader(handle, dialect="excel-tab"))
    assert len(staged) == 231
    assert sum(row["stage_status"] == "integrated" for row in staged) == 5
    pic1 = next(row for row in staged if row["identity"] == "PIC1.DAX:001:000")
    assert pic1["stage_status"] == "rejected" and not pic1["runtime_path"]
    for row in staged:
        if row["stage_status"] == "integrated":
            assert (destination / row["runtime_path"]).is_file()
print("integration foundation tests passed: 231 lookups, 5 staged, gated title set and rejected candidate preserved")
