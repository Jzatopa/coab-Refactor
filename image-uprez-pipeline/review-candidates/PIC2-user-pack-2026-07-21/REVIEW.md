# PIC2 user asset pack review — 2026-07-21

## Accepted mappings

- `12_00_31 PM`: shared treasure replacement for `PIC1.DAX` through `PIC6.DAX`, block 001. The six source frames are byte-identical.
- `09_25_22/23/24 AM (1)-(8)`: `PIC2.DAX:007`, frames 000-007 in filename order.
- `11_15_55/56/57 AM (1)-(5)`: `PIC2.DAX:009`, frames 000-004 in filename order.
- `11_30_36/37 AM (1)-(3)`: `PIC2.DAX:010`, frames 000-002 in filename order.
- `11_52_31 AM (1)-(4)`: `PIC2.DAX` blocks 011-014, respectively.
- Existing approved `HDAssets/PIC1/PIC1_block_029_frame_000-003.png`: reused for `PIC2.DAX` through `PIC6.DAX`, block 029. All six source camp sequences are byte-identical frame-for-frame.

## Not staged

`11_15_57 AM (6)` is retained as `block-009/unused-extra-candidate-6.png`. Block 009 has five source frames, so this sixth generated still has no deterministic archive/block/frame identity.

## Quality notes

All accepted files are square 1254×1254 PNGs and preserve the major source composition. The three supplied animation sets were generated as independent full frames rather than from one frozen static plate, so minor texture/detail shimmer remains between frames. This does not break identity or ordering, but it is below the pipeline's preferred next-generation animation method. The shared camping set remains the stronger temporal reference because its transition lifecycle has already been live-tested through combat.
