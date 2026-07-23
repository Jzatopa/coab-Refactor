# PIC1 Block 029 — Approved Four-Frame Set

- Source: `PIC1.DAX`, block `29`
- Frames: `0–3`
- Candidate size: `1254×1254` each
- Mapping: the replacement `10_16_59 AM (1)–(4)` downloaded files map in order to frames `000–003`
- Replacement: this set supersedes the earlier `09_58_52/09_58_53` set
- Human decision: The maintainer explicitly requested installation in both HD game variants on 2026-07-15
- Lifecycle: normal picture retained layer, replaced per original animation frame and cleared when the panel is replaced

## Visual preflight

The replacement set is internally coherent and preserves the night campsite, tent, camper and animated campfire concept. All four frames share stable composition and framing; motion is limited to plausible fire flicker and illumination changes. Live demo replay initially exposed a stale camp overlay during combat; `ovr011.BattleSetup()` was corrected to retire every retained gameplay picture layer inside the stopped combat update batch. Post-fix 3 fps capture passed: last camp frame at 40.67s, first complete combat frame at 41.00s, with no stale overlay, fallback flash or partial combat frame. Existing capture review then found the adjacent party Name/AC/HP summary missing because each camp animation frame cleared the entire HD glyph cache. Per-layer external-image text invalidation is now rectangle-scoped, and a targeted non-demo regression test confirms the camp cells clear while Name/AC/HP and party-name cells survive both image set and clear. It is integrated because The maintainer explicitly selected and supplied the complete set.
