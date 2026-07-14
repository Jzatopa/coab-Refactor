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

## Normal PIC replacements

PIC1 block 80 replaces the demo village panel at logical rectangle `(24,24,88,88)`. `DrawMaybeOverlayed()` activates it only when drawing the exact first frame loaded from `PIC1.DAX` block 80. It is retired without an intermediate publish before a different normal picture, portrait, animation, BIGPIC, or outer frame replaces that panel.

Normal-PIC mappings must include both game area and block ID because DAX block numbers are reused.

## HD font

The HD font uses the original 8×8 logical cell geometry. While the HD atlas is active, its low-resolution foreground pixels are suppressed in the framebuffer so non-integer presentation scaling cannot reveal a second pixel font underneath the HD glyph.

Opaque picture and symbol pixels written through `Display.SetPixel3()` invalidate any retained HD glyph in the affected cell. This prevents stale HD text from remaining above replacement artwork. Transparent pixels do not invalidate cells because they do not replace framebuffer content.

## Visual quality standard

`HDAssets/PIC1_block_080_village.png` is the baseline reference for replacement-art realism. New manually created or automated image generations should match or exceed its grounded detail, material realism, natural lighting, coherent perspective, and scene fidelity. Do not accept visibly painterly, plastic, generic, low-detail, or loosely interpreted generations when the reference supports a more realistic result.

Generated replacements must still preserve the original composition, important objects, gameplay readability, panel aspect ratio, and transition lifecycle.

## Verification requirement

Before adding or changing an HD visual asset:

1. Replay the matching scene in the original and refactor builds.
2. Capture the transition through the first subsequent scene.
3. Confirm there is no stale HD artwork, fallback flash, missing text, or partial-frame publication.
4. For combat changes, use a high-frame-rate capture to detect intermediate tile/icon states.
