# HEAD2/BODY2 block 003 — Tiverton innkeeper

- Original head: `../../png/HEAD2/HEAD2_block_003_frame_000.png` (88×40, 11:5)
- Original body: `../../png/BODY2/BODY2_block_003_frame_000.png` (88×48, 11:6)
- Approved HD head: `../../approved/HEAD2/HEAD2_block_003_frame_000.png` (1760×800)
- Approved HD body: `../../approved/BODY2/BODY2_block_003_frame_000.png` (1760×960)
- Combined generation/test source: `../../interchange-test/innkeeper-003/`
- Original isolated live comparison: `../../../test-evidence/woman-trace/innkeeper-original-vs-HD-live.jpg`
- Promoted Full Auto live capture: `../../../test-evidence/innkeeper-003-promoted/full-auto/full-auto-innkeeper-live.png`
- Stable/Full Auto promoted comparison: `../../../../diagnostics/innkeeper-003-promoted-live.jpg`

## Decision

**Approved and lifecycle verified by the maintainer on Telegram, 2026-07-15.**

The original head and body were reconstructed as one coherent portrait and split at the exact engine seam. The pair was installed in the isolated Full Auto runtime and traced live as `HEAD2.DAX:003:000` plus `BODY2.DAX:003:000`.

- Original seam neck width: 12 logical pixels.
- HD seam neck width: 11.95 logical pixels.
- Difference: 0.05 logical pixels / 0.42%.
- Tolerance: ±1 logical pixel — **PASS**.
- Live seam, scale, lighting, skin continuity and panel containment — **PASS**.
- Optional future polish only: increase silhouette 3–5% and soften the lower-body transition into black.
