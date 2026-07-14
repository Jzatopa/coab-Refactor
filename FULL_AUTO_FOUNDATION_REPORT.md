# COAB Full-Auto Upgrade Report

## Completed foundation and integration

- Isolated branch/runtime: `full-auto-upgrade` in `/home/jzatopa/.openclaw/workspace/coab-uprez-full-auto`, with mutable game data under ignored `runtime/` paths.
- Isolated launchers: repository `run-full-auto.sh` and workspace `/home/jzatopa/.openclaw/workspace/run-coab-uprez-full-auto.sh`.
- Audited all **231** eligible extracted frames against the manifest and prompt ledger; all source paths resolve, all prompts are populated, and all archive/block/frame metadata is normalized.
- Identified **175** unique source images and **56** duplicate frame rows that may reuse one approved generation.
- Added manifest-driven identity, candidate validation, atomic approved-asset staging, runtime lookup, status reporting, and integration tests.
- Runtime retained-HD layers support normal pictures, animation frames, simultaneous head/body portraits, BIGPICs, and the complete four-screen TITLE sequence while preserving the original replacement boundaries.
- Combat maps/tiles/sprites/icons, dungeon walls, and world terrain remain outside the eligible manifest and were not modified.

## Asset counts

- Eligible ledger entries: **231**
- Strong prior eligible replacements reused: **8**
- New generations during this run: **3**
- New generations accepted/integrated: **1**
- New generations rejected after review: **2**
- Total approved and deterministically staged eligible entries: **9**
- Rejected eligible entry retained for review history: **1**
- Eligible entries still missing an approved generation: **221**
- Total eligible entries not integrated: **222**

Integrated identities:

- TITLE blocks 1–4, fitted without stretching to exact 8:5 full-screen canvases;
- BIGPIC1 blocks 121 and 123;
- BIGPIC2 block 120, accepted candidate B at exact 38:15;
- BIGPIC6 block 122, reused from a strong legacy asset whose old filename incorrectly said BIGPIC1;
- PIC1 block 80.

Rejected generation evidence:

- PIC1 block 1 candidate E: separate curved horn still merged into sword guard; open scroll became rolled parchment.
- BIGPIC2 block 120 candidate A: center face too dominant and black separation gaps reduced. Candidate B corrected those issues and was accepted.

## Verification

- Inventory verification: pass, 20 archives / 135 blocks / 231 frames / 231 PNGs.
- Prompt audit: pass, 231/231 populated and composition-constrained; BIGPIC2 block 120 prompt corrected after equal-scale source review.
- Python integration test: pass, 231 unique runtime lookups, complete-animation enforcement, 9 staged, rejected candidate excluded.
- Release build: pass, 0 errors (existing compiler/WiX warnings only).
- Isolated Xvfb smoke launch: pass; title rendered full-frame without stale overlays or corruption.
- Full demo playback evidence is stored under `test-evidence/full-demo/` when complete.
- Stable `/home/jzatopa/.openclaw/workspace/coab-refactor` source checkout was not modified by this work.

## Remaining blocker

Image-generation credentials are available and the configured OpenAI provider succeeded. The blocker is throughput, not authentication: the available generator is one asynchronous image request per tool task, with no bulk queue, and every result requires composition/object-count review plus exact-ratio post-processing. It also returned lower dimensions than requested (for example 1254×1254 for a 2048×2048 request and 1997×788 for a 3840×2160 request). Completing and reviewing the remaining 221 ledger entries requires a sustained multi-run generation campaign; they are deliberately left unstaged rather than filled with unreviewed or upscaled placeholders.
