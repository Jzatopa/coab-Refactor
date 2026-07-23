# Retained-image lifecycle fix — Full Auto

## Reproduction

The separate HD Tiverton innkeeper head/body layers correctly remained through two dialogue pages, but stayed stale when the original panel changed to the 3D viewport and area map.

## Fix

- `ovr031.Draw3dWorld()` retires all retained gameplay layers inside its stopped update batch before drawing the 3D viewport or area map.
- Complete alternate/combat frame renderers use the same shared clear.
- `seg041.DrawRectangle()` retires only gameplay layers intersecting an ad-hoc framebuffer clear, preserving unrelated layers.
- Split head/body layers retire together at complete scene boundaries and publish at most once.

## Verification

- Release build: PASS, 0 errors.
- Retained-image intersection harness: PASS; non-overlapping redraw retained both layers, head overlap cleared only head, body overlap cleared body.
- Existing scoped HD-text regression: PASS.
- Candidate validation: 231 entries, 15 stageable.
- Integration test: PASS, 15 staged.
- Live trace: `COAB_HD_HEAD_BODY area=2 head=3 body=3`.
- Live sequence: step 0/1 portrait active; step 2 portrait cleared and 3D viewport visible; step 3 area map visible.
- Name/AC/HP and dialogue remain intact; no stale or partial overlays.

**Result: PASS.**
