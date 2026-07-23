# PIC1 Block 029 10:16:59 Replacement Lifecycle Result — Full Auto HD

- Asset set: `ChatGPT Image Jul 15, 2026, 10_16_59 AM (1)–(4).png`
- Mapping: filename order to PIC1 block 29 frames `000–003`
- Strict 231-entry validation and deterministic staging: **PASS**
- Pre-fix replay: **FAIL** — retained HD camp remained visible beneath combat.
- Root cause: `BattleSetup()` cleared only BIGPIC overlays; the layered gameplay picture remained active.
- Fix: call `ClearHdPictureOverlays(false)` inside the stopped combat update batch before combat assembly.
- Release build: **PASS**
- Post-fix replay at 3 fps: **PASS**
- Last camp frame: `40.67s`
- First complete combat frame: `41.00s`
- No stale camp, low-resolution fallback flash, blank panel, mixed overlay, or partial combat frame observed.
- Follow-up existing-capture review found the adjacent party Name/AC/HP summary missing during the camp animation.
- Cause: every external-image layer update cleared the entire HD glyph cache.
- Text fix: each external-image layer now invalidates only cells intersecting its logical rectangle; full-screen layers still clear all glyphs.
- Non-demo regression harness: **PASS** — camp cell invalidated while Name, AC/HP, and party-name cells survive image set and clear.
- Per the maintainer's request, the demo was not rerun for this text fix.
