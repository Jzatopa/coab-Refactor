# All-screen high-resolution font lifecycle — July 27, 2026

## Requested change

The faithful high-resolution font is now enabled before the opening sequence and remains enabled across:

- title sequence,
- credits,
- Play/Demo prompt,
- copy protection and loading/start menus,
- demo and gameplay,
- demo return to the title sequence.

This intentionally supersedes the earlier gameplay-only font lifecycle.

## Implementation

`engine/seg001.cs` no longer disables `Display.HighResFontEnabled` before either the initial title sequence or the return-to-title sequence. All four lifecycle assignments now set it to `true`.

Runtime text on every screen therefore follows the same path:

1. retain the original 8×8 character identity, grid position, color, spacing, and wrapping;
2. suppress the low-resolution foreground pixels;
3. manually rasterize the binary faithful atlas to the exact final cell size;
4. copy the final glyph unscaled without filtered fringe pixels.

Retained title artwork remains independent and its source assets were not modified.

## Validation

- Release build: passed with 0 errors; only the expected Linux WiX warning remained.
- Staging: passed, 231 ledger entries and 121 staged assets.
- All-screen font contract: passed.
- Title-sequence contract: passed.
- Integration contract: passed for all 231 lookups.
- HD lifecycle contract: passed for 111 approved PIC identities.
- Live lossless 2560×1600 sequence: SSI title, both accumulated title-logo stages, credits, Play/Demo, start/loading menu, and active demo captured successfully.
- Live lossless 2560×1440 non-integer-scale check: Play/Demo and active demo captured successfully at 7.2× presentation scale.
- The live game remained running after both active-demo captures.
- Visual inspection confirmed consistent glyph shapes, hard binary edges, fixed-cell geometry, colors, and scale across credits, Play/Demo, menus, and demo/gameplay. The 2560×1440 check showed no exposed low-resolution under-font or spacing gaps from rounded 57/58-pixel cells.
- No stale glyphs, clipping, overlap, missing text, retained-title corruption, or frame damage observed.

## Evidence

- `01-ssi-title.jpg`
- `02-curse-title.jpg`
- `03-forgotten-realms-title.jpg`
- `07-credits.png`
- `08-play-demo.png`
- `09-start-game-menu.png`
- `10-active-demo.png`
- `11-play-demo-2560x1440.png`
- `12-active-demo-2560x1440.png`
