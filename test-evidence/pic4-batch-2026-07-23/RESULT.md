# PIC4 HD integration result — 2026-07-23

## Integrated groups

- `PIC4.DAX:039`: 4 frames
- `PIC4.DAX:040`: 4 frames
- `PIC4.DAX:041`: 2 frames
- `PIC4.DAX:049`: 8 frames
- `PIC4.DAX:067`: 3 frames

All 21 files use canonical names `PIC4_block_NNN_frame_NNN.png` and are staged under their exact archive/block/frame identities. Static or incomplete PIC4 groups remain unapproved and unstaged.

## Frame and file validation

- Visual comparison confirmed each candidate sequence follows the numbered original DAX frame order.
- All candidates are valid square PNG files at or above the 1024-pixel minimum.
- Complete animation groups are enforced all-or-nothing.
- Duplicate-frame contracts pass byte-for-byte:
  - block 039 frame 003 = frame 000
  - block 049 frame 005 = frame 002
  - block 049 frame 006 = frame 001
- Integration regression verifies every staged file hash equals its approved candidate hash. Exact staged hashes are recorded in `PIC4_STAGED_HASHES.tsv`.

## Placement and lifecycle

PIC frames are registered with game area, block, and frame identity and resolve through `runtime-lookup.tsv`. Every PIC4 frame occupies the original logical 88×88 picture rectangle. Successive animation frames replace the same `game-picture` retained layer rather than accumulating additional layers.

Regression coverage verifies that the retained picture layer is retired with `publishImmediately=false` before the stopped-update replacement paths for the 3D viewport and combat screen. The shared renderer also clears or replaces this layer at picture, portrait, outer-frame, and intersecting framebuffer replacement boundaries, preventing the prior PIC4 image from surviving onto the next screen.

## Validation results

- Ledger: 231 deterministic identities
- Candidate entries after merging with the authoritative branch: 89
- Stageable/integrated entries: 87
- Missing entries: 142
- Review/lifecycle gated entries: 2
- PIC4 staged entries: 21
- Release build: 0 errors (23 pre-existing warnings)
- Protected lock: 123 files / 87 integrated identities unchanged

A direct scripted encounter replay for each PIC4 scene was not available in this pass; lifecycle confidence comes from exact runtime identity staging, byte-matched files, source-level replacement-boundary regression, the shared retained-layer implementation, and prior live lifecycle captures of the same normal-PIC path.
