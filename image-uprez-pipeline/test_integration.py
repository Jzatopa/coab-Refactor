#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import tempfile
from pathlib import Path

from integration_common import build_rows, resolve_candidate
from stage_approved_assets import stage
from validate_candidates import validate

rows = build_rows()
project_root = Path(__file__).resolve().parent.parent
assert len(rows) == 231
assert len({row["identity"] for row in rows}) == 231
assert len({row["runtime_name"] for row in rows}) == 231
assert all(row["animation_frame_count"] >= 1 for row in rows)
validation = validate(rows)
assert validation["stageable_entries"] == 118
treasure = [row for row in rows if row["block"] == 1 and row["archive"].startswith("PIC")]
assert len(treasure) == 6
assert all(row["review_status"] == "approved" for row in treasure)
assert len({row["candidate"] for row in treasure}) == 1
assert len({row["source_sha256"] for row in treasure}) == 1
pic2_supplied = [row for row in rows if row["archive"] == "PIC2.DAX" and row["block"] in {1, 7, 9, 10, 11, 12, 13, 14}]
assert len(pic2_supplied) == 21
assert all(row["review_status"] == "approved" for row in pic2_supplied)
shared_block_9 = [row for row in rows if row["archive"] in {"PIC2.DAX", "PIC4.DAX"} and row["block"] == 9]
assert len(shared_block_9) == 10
for frame in range(5):
    matching = [row for row in shared_block_9 if row["frame"] == frame]
    assert len(matching) == 2
    assert len({row["source_sha256"] for row in matching}) == 1
    assert len({row["candidate"] for row in matching}) == 1
    assert all(row["review_status"] == "approved" for row in matching)
pic1_block_29 = [row for row in rows if row["animation_group"] == "PIC1.DAX:029"]
assert len(pic1_block_29) == 4
assert all(row["review_status"] == "approved" for row in pic1_block_29)
assert all(row["lifecycle_status"] == "verified" for row in pic1_block_29)
pic4_groups = {
    "PIC4.DAX:039": 4,
    "PIC4.DAX:040": 4,
    "PIC4.DAX:041": 2,
    "PIC4.DAX:049": 8,
    "PIC4.DAX:067": 3,
}
for group, expected_count in pic4_groups.items():
    frames = [row for row in rows if row["animation_group"] == group]
    assert len(frames) == expected_count
    assert [row["frame"] for row in frames] == list(range(expected_count))
    assert all(row["review_status"] == "approved" for row in frames)
    assert all(row["lifecycle_status"] == "verified" for row in frames)
    assert all(row["lifecycle"] == "normal_picture_until_panel_replace" for row in frames)
    block = int(group.rsplit(":", 1)[1])
    assert [row["runtime_name"] for row in frames] == [
        f"PIC4_block_{block:03d}_frame_{frame:03d}.png"
        for frame in range(expected_count)
    ]
pic4_by_identity = {row["identity"]: row for row in rows if row["archive"] == "PIC4.DAX"}
for left, right in [
    ("PIC4.DAX:039:003", "PIC4.DAX:039:000"),
    ("PIC4.DAX:049:005", "PIC4.DAX:049:002"),
    ("PIC4.DAX:049:006", "PIC4.DAX:049:001"),
]:
    left_path = resolve_candidate(pic4_by_identity[left]["candidate"])
    right_path = resolve_candidate(pic4_by_identity[right]["candidate"])
    assert left_path is not None and right_path is not None
    assert hashlib.sha256(left_path.read_bytes()).hexdigest() == hashlib.sha256(right_path.read_bytes()).hexdigest()

recovered_groups = {
    "PIC3.DAX:027": 4,
    "PIC4.DAX:035": 3,
    "PIC5.DAX:052": 3,
    "PIC5.DAX:057": 4,
}
for group, expected_count in recovered_groups.items():
    frames = [row for row in rows if row["animation_group"] == group]
    assert len(frames) == expected_count
    assert [row["frame"] for row in frames] == list(range(expected_count))
    assert all(row["review_status"] == "approved" for row in frames)
    assert all(row["lifecycle_status"] == "verified" for row in frames)
    assert all(row["lifecycle"] == "normal_picture_until_panel_replace" for row in frames)
with tempfile.TemporaryDirectory() as temp:
    destination = Path(temp) / "HDAssets"
    report = stage(destination)
    assert report["integrated_entries"] == 118
    with (destination / "runtime-lookup.tsv").open(newline="") as handle:
        staged = list(csv.DictReader(handle, dialect="excel-tab"))
    assert len(staged) == 231
    assert sum(row["stage_status"] == "integrated" for row in staged) == 118
    staged_treasure = [row for row in staged if row["block"] == "1" and row["archive"].startswith("PIC")]
    assert len(staged_treasure) == 6
    assert all(row["stage_status"] == "integrated" for row in staged_treasure)
    assert len({row["candidate_sha256"] for row in staged_treasure}) == 1
    staged_camps = [row for row in staged if row["block"] == "29" and row["archive"].startswith("PIC")]
    assert len(staged_camps) == 24
    assert all(row["stage_status"] == "integrated" for row in staged_camps)
    for frame in range(4):
        matching = [row for row in staged_camps if row["frame"] == str(frame)]
        assert len(matching) == 6
        assert len({row["candidate_sha256"] for row in matching}) == 1
    staged_pic2_pack = [row for row in staged if row["archive"] == "PIC2.DAX" and row["block"] in {"1", "7", "9", "10", "11", "12", "13", "14"}]
    assert len(staged_pic2_pack) == 21
    assert all(row["stage_status"] == "integrated" for row in staged_pic2_pack)
    staged_shared_block_9 = [row for row in staged if row["archive"] in {"PIC2.DAX", "PIC4.DAX"} and row["block"] == "9"]
    assert len(staged_shared_block_9) == 10
    for frame in range(5):
        matching = [row for row in staged_shared_block_9 if row["frame"] == str(frame)]
        assert len(matching) == 2
        assert len({row["candidate_sha256"] for row in matching}) == 1
        assert all(row["stage_status"] == "integrated" for row in matching)
    innkeeper = [row for row in staged if row["identity"] in {
        "HEAD2.DAX:003:000", "BODY2.DAX:003:000"
    }]
    assert len(innkeeper) == 2
    assert all(row["stage_status"] == "integrated" for row in innkeeper)
    assert {row["aspect_ratio"] for row in innkeeper} == {"11:5", "11:6"}
    staged_pic4_new = [row for row in staged if row["animation_group"] in pic4_groups]
    assert len(staged_pic4_new) == 21
    assert all(row["stage_status"] == "integrated" for row in staged_pic4_new)
    staged_recovered = [row for row in staged if row["animation_group"] in recovered_groups]
    assert len(staged_recovered) == sum(recovered_groups.values())
    assert all(row["stage_status"] == "integrated" for row in staged_recovered)
    for row in staged:
        if row["stage_status"] == "integrated":
            runtime_file = destination / row["runtime_path"]
            assert runtime_file.is_file()
            assert hashlib.sha256(runtime_file.read_bytes()).hexdigest() == row["candidate_sha256"]

ovr030 = (project_root / "engine" / "ovr030.cs").read_text()
ovr031 = (project_root / "engine" / "ovr031.cs").read_text()
ovr011 = (project_root / "engine" / "ovr011.cs").read_text()
display = (project_root / "Classes" / "Display.cs").read_text()
assert 'const string PictureLayer = "game-picture";' in ovr030
assert 'layer = PictureLayer;' in ovr030
assert 'ClearLayer(PictureLayer, false);' in ovr030
assert ovr031.index("Display.UpdateStop();") < ovr031.index("ovr030.ClearHdPictureOverlays(false);") < ovr031.index("Draw3dWorldBackground();")
battle = ovr011.index("internal static void BattleSetup")
battle_clear = ovr011.index("ovr030.ClearHdPictureOverlays(false);", battle)
battle_draw = ovr011.index("SetupGroundTiles();", battle)
assert battle < battle_clear < battle_draw
assert "externalImages[key] = new ExternalImageLayer" in display
assert "externalImages.Remove(key);" in display
print("integration tests passed: 231 lookups, 118 staged with byte-matched runtime files, shared six-area treasure/camp mappings, complete approved PIC2-PIC5 animations with duplicate-frame contracts, verified retained-layer replacement boundaries, and exact-ratio innkeeper/title assets")
