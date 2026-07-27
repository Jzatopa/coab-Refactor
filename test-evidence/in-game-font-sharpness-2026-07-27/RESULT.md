# Gameplay-only HD font correction — July 27, 2026

## Scope correction

The native-8x title-art sharpening commit was reverted in both releases. The approved opening title images and their supplied typography are restored byte-for-byte. The HD in-game font layer is now explicitly disabled throughout the title sequence, credits, Play/Demo prompt, and copy-protection screen.

## In-game font improvement

The faithful original-topology font atlas already preserved in `HD-ASSET-ARCHIVE/images/runtime/` was not being copied into the isolated full-auto runtime after the HD asset-tree reconciliation. The launcher now restores the active faithful atlas and its documented optional variants into the runtime without modifying original game data.

During gameplay only, the 128x128 atlas cells are downsampled into the original 8x8 logical text cells with high-quality bicubic interpolation and high-quality pixel alignment. This retains the original glyph identities, fixed 40x25 text grid, colors, wording, wrapping, and gameplay geometry while giving diagonals and curves a clean one-pixel antialiased edge instead of enlarged framebuffer stair-steps.

## Verification

- Opening title asset contract passed with the previously approved hashes and dimensions.
- Focused font contract passed: all three archived atlases were staged byte-exactly; the faithful original-topology atlas remains the default.
- Runtime lifecycle contract verifies the font layer is off for opening screens and enabled only after opening/copy-protection flow.
- Release build succeeded with 0 errors; existing warnings remain nonblocking.
- Pipeline integration passed: 231 lookups and 121 staged assets.
- HD lifecycle contract passed for 111 approved PIC identities.
- Live 2560x1600 demo gameplay reached Tilverton dialogue with clean text, intact fixed cells, no overlap, clipping, stale glyphs, or frame/art corruption.
- Game remained alive through the capture sequence.
- DeepSeek sidecar review found no blocker. Its only general caution was to preserve the explicit font lifecycle if future non-gameplay screens are added; the optional quill atlas hash and dimensions are already covered by the focused contract.

## Evidence

- `before-after-in-game-font.jpg`: previous framebuffer-only menu text versus the corrected gameplay-only HD text.
- `live-gameplay-contact.jpg`: three consecutive live gameplay dialogue captures.
- `opening-credits-unchanged.jpg` and `play-demo-unchanged.jpg`: live proof that the opening text remains on the original rendering path.
- `prototypes/font-variants.png`: original-nearest, faithful-antialiased, and optional quill/brush comparison used to select the faithful approach.
