# Clean-alloy UI frame integration — July 26, 2026

## Scope

Integrated the user-supplied `COAB_Frame_Panels_Clean_Alloy_FINAL` delivery into the faithful High Res Release.

- Imported all 20 exact 64×64 RGBA runtime tiles (`0x114`–`0x127`).
- Rebuilt all seven 2560×1600 retained UI-frame layouts.
- Kept the optional smooth 128×128 reinterpretation out of the faithful runtime because the engine uses 64×64 tiles and the smooth set intentionally changes the original 8×8 silhouette.

## Runtime occlusion correction

The supplied exact tiles made both original black pixels and magenta-key pixels transparent. In the live retained-overlay architecture, original black pixels are the opaque backing inside occupied frame cells. Leaving them transparent can expose low-resolution framebuffer text or frame pixels below the HD layer.

`scripts/import_clean_alloy_ui_frame_tiles.py` therefore:

1. preserves the supplied clean-alloy RGB artwork in every non-black source cell;
2. restores original black source cells as opaque black;
3. keeps only original magenta-key source cells transparent;
4. rebuilds all seven layouts through `scripts/build_hd_ui_frame_assets.py`.

The import is byte-idempotent.

## Verification

- Independently matched all 20 supplied PNG SHA-256 hashes against `COMPLETED_DELIVERY_VALIDATION.json`.
- Verified all 20 integrated tiles are 64×64 RGBA.
- Verified every original non-magenta source cell is fully opaque and every original magenta-key cell is transparent.
- Verified all seven assembled layouts are 2560×1600 RGBA.
- `xbuild /property:Configuration=Release coab.sln`: succeeded with 0 errors and the existing nonblocking WiX warning.
- `python3 image-uprez-pipeline/test_integration.py`: passed; 231 lookups and 121 byte-matched staged assets.
- `python3 image-uprez-pipeline/test_hd_lifecycle_contract.py`: passed for 111 approved PIC identities after aligning its stale launcher assertion with the release-local `Data/` policy.
- `COAB_PREPARE_ONLY=1 ./launch.sh`: validated 231 entries and integrated 121 approved assets.
- Live 1280×800 Xvfb smoke: game remained alive through 16 captures. The new clean-alloy frame rendered on the credits/divider screen and party-function screen without stale overlays, low-resolution bleed, missing borders, or corrupt seams.
- Live native 2560×1600 Xvfb smoke: game remained alive and the same two framed screens rendered at the layout assets' native resolution without one-pixel gaps, clipping, transparency leaks, or corruption. The frameless Play/Demo transition also remained free of a stale frame.

## Evidence

- `live-contact.jpg`: chronological contact sheet of the 16-capture 1280×800 live run.
- `steps/`: curated 1280×800 credits, frameless Play/Demo, and party-function captures.
- `native-2560x1600/`: curated native-resolution captures of those same lifecycle states.
- `SUPPLIED_SHA256SUMS.txt`: hashes of the user-supplied exact runtime tiles.
- `INTEGRATED_TILE_SHA256SUMS.txt`: hashes after runtime occlusion correction.
- `INTEGRATED_LAYOUT_SHA256SUMS.txt`: hashes of the seven rebuilt layouts.
- `game.log`, `xvfb.log`, and `result.txt`: staging and live-run evidence.
