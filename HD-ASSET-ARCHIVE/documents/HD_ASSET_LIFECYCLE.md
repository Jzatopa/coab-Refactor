# HD Asset Lifecycle Rules

The game still owns a 320×200 logical framebuffer. HD artwork and HD glyphs are presentation layers, so they must follow the same replacement boundaries as the original framebuffer content.

## Core rule

For every retained HD visual asset, identify the original draw or clear operation that replaces its low-resolution counterpart. Retire the HD state at that exact boundary without publishing an intermediate frame. Let the completed replacement frame publish normally.

Do not clear retained artwork while merely loading data. Loading is not a visual transition.

### Enforced retirement rule

Every retained gameplay image is owned by `ovr030`. Before the original renderer replaces any part of that image's logical framebuffer rectangle, the owning HD layer must retire with `publishImmediately=false`; the completed replacement draw publishes normally. A retained image cannot survive a partial rectangle replacement because it would hide the new framebuffer content.

This is enforced at all complete scene boundaries: outer/menu frames, the 3D viewport and area map, combat frames, and the alternate `draw8x8_05` frame. Ad-hoc framebuffer rectangle clears retire only intersecting gameplay layers. Image-to-image and portrait-to-picture changes remain enforced in `ovr030`. New HD assets must use these shared paths rather than adding one-off clear logic.

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

In the full-auto fork, blocks 1–2 are exact 8:5 full-screen base layers. Blocks 3–4 preserve their exact partial-DAX ratios and logical rectangles: block 3 is 15:7 at `(48,88,240,112)` and block 4 is 20:7 at `(0,88,320,112)`. These overlays are cropped from the approved accumulated HD compositions without stretching, ordered above the title base, and still activate only when the complete four-file set is available.

## Normal PIC replacements

PIC1 block 80 replaces the demo village panel at logical rectangle `(24,24,88,88)`.

PIC1-PIC6 block 001 use one shared treasure replacement because all six original source frames are byte-identical. The catalog still contains six exact archive identities, so each area resolves deterministically without a block-only fallback.

The after-combat treasure state draws frame 0 through `ovr030.DrawMaybeOverlayed()` immediately after loading block 001. This makes the retained HD image part of the first published treasure frame instead of waiting for a later menu-input animation tick. When combat handling advances to the dungeon or wilderness state, its final `ovr025.LoadPic()` rebuilds the destination view through the normal shared retirement paths, so the treasure cannot remain over the following scene.

PIC1-PIC6 block 029 use the same complete four-frame retained HD camping animation because the six original source sequences are byte-identical frame-for-frame. Downloaded files `(1)–(4)` map to original DAX frames `0–3`. Each decoded DAX frame is registered with its archive/block/frame identity, resolved through `runtime-lookup.tsv`, displayed at the original frame index and delay, and cleared at normal panel replacement. `ovr011.BattleSetup()` retires every retained gameplay picture layer inside the stopped update batch immediately before the completed combat screen is assembled and published. Every archive's full set is staged atomically; no partial animation is permitted.

PIC2 blocks 007, 009 and 010 are complete retained HD animation groups; blocks 011-014 are retained HD stills. PIC4 block 009 is byte-identical to PIC2 block 009 frame-for-frame and reuses the same five HD files through distinct PIC4 catalog identities. They use the same `game-picture` owner and therefore retire on image-to-image replacement, any intersecting framebuffer clear, outer/menu frame construction, 3D/area-map drawing, BIGPIC replacement, or combat setup. Frame changes replace the existing `game-picture` layer in place rather than accumulating retained images.

PIC4 blocks 039, 040, 041, 049, and 067 are complete retained HD animations containing 4, 4, 2, 8, and 3 frames respectively. Each file is keyed by `PIC4.DAX:block:frame` and uses `PIC4_block_NNN_frame_NNN.png`; no loose filename or same-numbered block from another archive is accepted. Visual review on 2026-07-23 confirmed the numbered blink, eyestalk, jaw, snake-hair, and smoke states against the original frame order. Duplicate-state contracts are enforced by hash: block 039 frame 003 equals frame 000, block 049 frame 005 equals frame 002, and block 049 frame 006 equals frame 001. All five groups stage atomically and use the same verified `game-picture` owner, so each frame replaces its predecessor and the retained layer retires non-publishing before panel, 3D-view, portrait, outer-frame, or combat replacement.

Normal-PIC mappings must include archive, game area, block ID and frame because DAX block numbers are reused.

## Portrait replacements

The approved Tiverton innkeeper uses `HEAD2.DAX:003:000` and `BODY2.DAX:003:000`. The head and body remain separate retained layers, placed at their original 88×40 and 88×48 logical rectangles with the body beginning exactly five text rows below the head. Both identities must be approved and lifecycle verified before staging. A different portrait or normal picture clears both layers inside the same update transition; outer-frame and combat boundaries clear all gameplay layers atomically. Live testing confirmed a 12-pixel original neck versus 11.95 logical pixels in HD, within the ±1-pixel seam tolerance.

## HD font

The HD font uses the original 8×8 logical cell geometry. While the HD atlas is active, its low-resolution foreground pixels are suppressed in the framebuffer so non-integer presentation scaling cannot reveal a second pixel font underneath the HD glyph.

Opaque picture and symbol pixels written through `Display.SetPixel3()` invalidate any retained HD glyph in the affected cell. Every retained external-art layer likewise invalidates only the 8×8 text cells intersecting its own logical rectangle; it must not clear unrelated text such as the party Name/AC/HP summary beside an animated PIC panel. A full-screen retained layer still invalidates the complete glyph cache. This prevents stale HD text above replacement artwork without erasing adjacent interface text. Transparent pixels do not invalidate cells because they do not replace framebuffer content.

## Visual quality standard

`HDAssets/PIC1_block_080_village.png` is the baseline reference for replacement-art realism. New manually created or automated image generations should match or exceed its grounded detail, material realism, natural lighting, coherent perspective, and scene fidelity. Do not accept visibly painterly, plastic, generic, low-detail, or loosely interpreted generations when the reference supports a more realistic result.

Generated replacements must still preserve the original composition, important objects, gameplay readability, panel aspect ratio, and transition lifecycle.

## Manifest-driven full-auto branch

The isolated `full-auto-upgrade` branch uses `image-uprez-pipeline/integration-manifest.json` as the authoritative archive/block/frame ledger. Every one of the 231 entries has a unique runtime lookup name, animation-group membership, exact source dimensions/aspect ratio, and lifecycle class.

Only `review_status=approved` plus `lifecycle_status=verified` assets may be staged. Animated archive/block groups are staged all-or-nothing. The runtime reads `HDAssets/runtime-lookup.tsv`; it does not infer identity from a legacy filename or reuse a block number across archives. Staging is atomic and occurs only in the isolated full-auto runtime.

## Verification requirement

Before adding or changing an HD visual asset:

1. Replay the matching scene in the original and refactor builds.
2. Capture the transition through the first subsequent scene.
3. Continue past the asset until the original framebuffer replaces it; confirm the HD layer retires on that exact frame.
4. Confirm there is no stale HD artwork, fallback flash, missing text, or partial-frame publication.
5. For combat changes, use a high-frame-rate capture to detect intermediate tile/icon states.
