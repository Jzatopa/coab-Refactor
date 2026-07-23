#!/usr/bin/env python3
"""Regression checks for retained normal-PIC retirement boundaries."""
from pathlib import Path

from integration_common import build_rows

ROOT = Path(__file__).resolve().parents[1]
ovr030 = (ROOT / "engine/ovr030.cs").read_text()
ovr025 = (ROOT / "engine/ovr025.cs").read_text()
ovr003 = (ROOT / "engine/ovr003.cs").read_text()
ovr011 = (ROOT / "engine/ovr011.cs").read_text()
ovr031 = (ROOT / "engine/ovr031.cs").read_text()
seg037 = (ROOT / "engine/seg037.cs").read_text()
seg041 = (ROOT / "engine/seg041.cs").read_text()

# Every newly approved gameplay picture uses the one retained game-picture
# owner. Replacing an image updates that same layer; missing/non-PIC draws
# retire it without publishing an intermediate frame.
assert 'const string PictureLayer = "game-picture";' in ovr030
assert 'Display.SetExternalImage(\n                                layer,' in ovr030
assert 'ClearLayer(PictureLayer, false);' in ovr030

# Partial framebuffer replacement retires only intersecting retained artwork.
assert "ClearHdPictureOverlaysIntersecting" in seg041
assert "LayerIntersects" in ovr030

# The after-combat treasure panel must publish through the retained PIC path
# immediately after loading block 001. Do not rely on a later menu-input tick,
# which can expose the low-resolution framebuffer first. CMD_Combat then changes
# state and calls LoadPic again, retiring/replacing the treasure on transition.
after_combat = ovr025.split("case GameState.AfterCombat:", 1)[1].split("break;", 1)[0]
assert after_combat.index('load_pic_final(ref gbl.byte_1D556, 0, 1, "PIC");') < after_combat.index(
    "DrawMaybeOverlayed(gbl.byte_1D556.frames[0].picture, true, 3, 3);"
)
cmd_combat = ovr003.split("internal static void CMD_Combat()", 1)[1].split(
    "internal static void CMD_OnGotoGoSub()", 1
)[0]
assert "gbl.game_state = GameState.DungeonMap;" in cmd_combat
assert "gbl.game_state = GameState.WildernessMap;" in cmd_combat
assert cmd_combat.rfind("ovr025.LoadPic();") > cmd_combat.rfind(
    "gbl.game_state = GameState.WildernessMap;"
)

# Complete scene replacement boundaries retire all retained gameplay artwork
# inside stopped update batches, so no stale overlay or fallback frame can be
# published over combat, 3D/area-map, or rebuilt framed screens.
assert "Display.UpdateStop();" in ovr011 and "ovr030.ClearHdPictureOverlays(false);" in ovr011
assert "Display.UpdateStop();" in ovr031 and "ovr030.ClearHdPictureOverlays(false);" in ovr031
assert seg037.count("ovr030.ClearHdPictureOverlays(false);") >= 3

approved_pic = [
    row for row in build_rows()
    if row["archive"].startswith("PIC") and row["review_status"] == "approved"
]
assert approved_pic
assert all(row["lifecycle"] == "normal_picture_until_panel_replace" for row in approved_pic)
assert all(row["lifecycle_status"] == "verified" for row in approved_pic)

print(f"HD lifecycle contract passed for {len(approved_pic)} approved PIC identities")
