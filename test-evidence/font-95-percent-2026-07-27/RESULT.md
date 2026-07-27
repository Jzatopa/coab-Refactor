# Centered 95% HD font presentation — July 27, 2026

## Change

The high-resolution glyph bitmap is now rendered at 95% of each existing destination cell in both dimensions and centered within that cell.

The original 40×25 grid, logical 8×8 cells, character identities, colors, spacing, wrapping, and text content remain unchanged. Only the visible glyph body becomes approximately 5% smaller.

At native 2560×1600 presentation, a 64×64 output cell receives a centered 61×61 glyph. At 2560×1440, the 7.2× presentation produces 57/58-pixel cells and centered 54/55-pixel glyphs. Integer output pixels necessarily round the exact 5% target to the closest representable size.

The glyph is still manually sampled from the binary faithful atlas and copied with `DrawImageUnscaled`; no antialiasing or dim fringe pixels are introduced. The low-resolution foreground remains suppressed across the full cell, so the new inset margin cannot expose an underlying second font.

## Validation

- Release build: passed with 0 errors; expected Linux WiX warning only.
- Staging: passed with 231 ledger entries and 121 staged assets.
- All-screen font contract: passed with explicit 0.95 scale and centered placement checks.
- Title-sequence contract: passed.
- Integration contract: passed for all 231 lookups.
- HD lifecycle contract: passed for 111 approved PIC identities.
- Lossless 2560×1600 Play/Demo and active-demo captures: passed; game remained running.
- Lossless 2560×1440 Play/Demo and active-demo captures: passed; game remained running.
- Visual comparison confirmed the intended smaller glyph bodies with unchanged cell positions, line wrapping, colors, and content.
- No clipping, baseline drift, uneven positioning, exposed low-resolution under-font, stale glyphs, overlap, gaps, or UI/frame corruption observed.
- Sidecar review raised a theoretical fractional-centering concern, but it does not apply here: `destinationLeft`, `destinationRight`, and `destinationWidth` are integer-rounded before glyph sizing and centering, so `DrawImageUnscaled` receives intentional integer coordinates.

## Evidence

- `play-demo-before-after-2560x1600.png`
- `play-demo-before-after-2560x1440.png`
- `play-demo-2560x1600.png`
- `active-demo-2560x1600.png`
- `play-demo-2560x1440.png`
- `active-demo-2560x1440.png`
- `MEASUREMENTS.txt`
