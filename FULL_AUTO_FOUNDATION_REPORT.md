# COAB Full-Auto Foundation Report

## Completed

- Isolated branch/runtime: `full-auto-upgrade` in `/home/jzatopa/.openclaw/workspace/coab-uprez-full-auto`, with mutable game data under ignored `runtime/full-auto/`.
- Launchers: repository `run-full-auto.sh` and `/home/jzatopa/.openclaw/workspace/run-coab-uprez-full-auto.sh`.
- All **231** ledger frames have deterministic archive/block/frame identity, exact source dimensions and aspect ratio, animation group/frame count/delay, canonical runtime name, and lifecycle class.
- Added candidate validation, atomic approved-asset staging, generated/missing/integrated reporting, runtime-name lookup, and integration tests.
- Runtime lookup uses `HDAssets/runtime-lookup.tsv`; retained layers support normal pictures, animation frames, simultaneous head/body portraits, BIGPICs, and the complete TITLE sequence with deterministic ordering and lifecycle clears.

## Current strict-stage counts

- Ledger entries: **231**
- Replacement-bearing entries: **10**
- Missing entries: **221**
- Approved and integrated in the isolated runtime: **9**
- Rejected and retained for review history: **1**

Integrated identities: TITLE blocks 1–4 as one exact-ratio lifecycle set; BIGPIC1 blocks 121/123; BIGPIC2 block 120 at exact 38:15; BIGPIC6 block 122; and PIC1 block 80.

PIC1 block 001 candidate D remains the strongest first batch candidate, but it is not integrated because the curved golden horn and open parchment scroll are omitted or weakened. Its rejected review status is preserved.

## Verification

- Inventory and prompt audit: pass for 231/231 entries.
- Python integration test: pass; 231 unique lookups, complete-animation/title-set enforcement, 9 staged, rejected candidate excluded.
- Release build: pass with no errors.
- Isolated prepare/stage: pass.
- Xvfb smoke launch: remained alive until the 10-second timeout; only the known XIM warning appeared.
- Stable `coab-refactor` and Downloads runtime were not written by the full-auto launcher.
