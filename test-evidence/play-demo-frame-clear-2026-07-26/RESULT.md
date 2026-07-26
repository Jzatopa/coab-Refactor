# Play Demo frame-lifecycle verification — July 26, 2026

## Defect

The original Play Demo selection screen is intentionally frameless: a black field with the version, `PLAY`, and `DEMO` prompt on the bottom row. The High Res build retained `UI_FRAME_layout_02_menu_dividers_overlay.png` from the preceding credits screen after the framebuffer was cleared, producing an outer frame and two incorrect horizontal dividers.

## Fix

`seg041.ClearScreen()` now retires the retained `ui-frame` presentation layer before clearing the original framebuffer. This mirrors the lifecycle of the original frame pixels and prevents frame overlays from leaking into frameless screens.

## Verification

- `xbuild /property:Configuration=Release coab.sln`: succeeded with zero errors.
- `COAB_PREPARE_ONLY=1 ./launch.sh`: validated 231 identities and staged 121 approved assets.
- Live 1280x800 Xvfb capture: `play-demo-fixed.png`.
- Original reference: `../full-demo-final/steps/04-main-menu.png`.
- Both reference and fixed captures contain exactly 72 non-black pixels above the prompt region; these are the mouse pointer. No stale frame pixels remain.
