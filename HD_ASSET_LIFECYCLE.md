# HD Asset Lifecycle Rules

The game still owns a 320×200 logical framebuffer. HD artwork and HD glyphs are presentation layers, so they must follow the same replacement boundaries as the original framebuffer content.

## Core rule

For every retained HD visual asset, identify the original draw or clear operation that replaces its low-resolution counterpart. Retire the HD state at that exact boundary without publishing an intermediate frame. Let the completed replacement frame publish normally.

Do not clear retained artwork while merely loading data. Loading is not a visual transition.

## BIGPIC replacements

Current replacements cover BIGPIC1 blocks 120–123 only. The game-area check is required because other BIGPIC files may reuse the same block IDs.

Original lifecycle:

1. `ovr030.load_bigpic()` loads data.
2. `ovr030.draw_bigpic()` draws the framed BIGPIC.
3. `seg037.DrawFrame_Outer()` begins the next outer-frame scene and replaces the prior BIGPIC.

HD lifecycle:

- `draw_bigpic()` activates the matching HD panel overlay.
- `DrawFrame_Outer()` calls `ClearBigpicOverlay(false)` before drawing the replacement frame.
- The non-publishing clear is important: publishing immediately exposes a stale or partially drawn framebuffer.
- `ovr011.BattleSetup()` retains a defensive clear before combat.

Any future code path that replaces the BIGPIC panel without passing through `DrawFrame_Outer()` must retire the BIGPIC overlay at its equivalent visual boundary.

## Title replacements

Title blocks 1–4 are treated as one complete set. If any HD title file is unavailable, the entire title sequence uses original DAX artwork. This prevents an opaque retained title from hiding an original fallback block.

The final title overlay is cleared with `Display.ClearExternalImage(false)` immediately before `ClearScreen()` publishes the credits transition.

## HD font

The HD font uses the original 8×8 logical cell geometry. Original glyph pixels remain in the framebuffer as a fallback, while the HD glyph is drawn over the same cell.

Opaque picture and symbol pixels written through `Display.SetPixel3()` invalidate any retained HD glyph in the affected cell. This prevents stale HD text from remaining above replacement artwork. Transparent pixels do not invalidate cells because they do not replace framebuffer content.

## Verification requirement

Before adding or changing an HD visual asset:

1. Replay the matching scene in the original and refactor builds.
2. Capture the transition through the first subsequent scene.
3. Confirm there is no stale HD artwork, fallback flash, missing text, or partial-frame publication.
4. For combat changes, use a high-frame-rate capture to detect intermediate tile/icon states.
