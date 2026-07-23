# COAB Full-Auto Foundation Report

## Completed

- Isolated branch/runtime: `full-auto-upgrade` in this repository, with mutable game data under ignored `runtime/full-auto/`.
- Launchers: repository launcher `run-full-auto.sh`.
- All **231** ledger frames have deterministic archive/block/frame identity, exact source dimensions and aspect ratio, animation group/frame count/delay, canonical runtime name, and lifecycle class.
- Added candidate validation, atomic approved-asset staging, generated/missing/integrated reporting, runtime-name lookup, and integration tests.
- Runtime lookup uses `HDAssets/runtime-lookup.tsv`; retained layers support normal pictures, animation frames, simultaneous head/body portraits, BIGPICs, and the complete TITLE sequence with deterministic ordering and lifecycle clears.

## Current strict-stage counts

- Ledger entries: **231**
- Replacement-bearing entries: **89**
- Missing ledger entries: **142**
- Unique original images: **175**
- Unique originals handled: **54** (**52 approved**, **2 explicitly rejected**)
- Unique originals still missing: **126**
- Approved and integrated in the isolated runtime: **87 entries**
- Rejected and retained for review history: **2 entries**

Integrated identities include the TITLE 1-4 set; BIGPIC1 121/123; BIGPIC2 120; BIGPIC6 122; PIC1 80; the six-area treasure and four-frame camp mappings; the PIC2 user pack; the PIC2/PIC4 block 009 duplicate reuse; the HEAD2/BODY2 block 003 innkeeper pair; and complete PIC4 groups 039, 040, 041, 049, and 067.

Explicitly rejected identities are BODY2 blocks 000 and 001. Their review candidates and notes remain excluded from staging.

## Resume point

- The 2026-07-23 PIC4 pass integrated complete groups 039, 040, 041, 049, and 067. Incomplete or unapproved PIC4 material remains gated.
- Next missing unique ledger identity in the broader production order: **`BODY2.DAX:002:000`** (`png/BODY2/BODY2_block_002_frame_000.png`).
- Nearest-neighbor source prep is retained as `review-evidence/BODY2_block_002_source_22x.png` and matching `HEAD2_block_002_source_22x.png`.
- Before generating, add one shared asset-specific lighting sentence to both BODY2 block 002 and HEAD2 block 002 prompt records, normalize the master ledger, then use the enlarged BODY source as composition input and `HDAssets/Title Block 2.png` only as the human realism/lighting-quality reference.
- The requested **231/231 final acceptance and final all-assets demo replay have not passed**; the replay evidence below is the verified deterministic-foundation baseline; current deterministic staging contains 87 approved entries.

## Verification

- Inventory and prompt audit: pass for 231/231 entries.
- Python integration test: pass; 231 unique lookups, 87 staged with byte-matched runtime files, complete PIC2/PIC4 animation enforcement, duplicate-frame hash contracts, retained-layer boundary checks, and rejected candidates excluded.
- Release build: pass with no errors.
- Isolated prepare/stage: pass.
- Xvfb smoke launch: remained alive with all 9 approved assets staged; only the known XIM warning appeared.
- Automated 240-second demo capture: pass. Two complete cycles returned to TITLE block 1, approximately **83 seconds** and **104 seconds** after gameplay became visible.
- Reached: TITLE 1, accumulated TITLE 2+3, TITLE 4, credits, demo menu, village/story panel, overland maps, night camp, tactical combat, fireball/spell state, black dragon combat, demon/skull BIGPIC narration, and title return.
- Lifecycle review found no stale picture/BIGPIC/title layer, transparent gap, partial-frame flash, missing title layer, or final TITLE block 4 seam.
- Representative evidence: `test-evidence/full-demo-final/steps/05-demo-start.png`, `test-evidence/full-demo-final/contact-sheets/demo-scenes-01.jpg`, `demo-scenes-02.jpg`, `demo-scenes-03.jpg`, and `SCENE_REVIEW.md`.
- Stable `coab-refactor` and Downloads runtime were not written by the full-auto launcher.
