# COAB Photoreal Image Uprez Review Pipeline

This folder contains the extracted eligible artwork, composition-aware generation prompts, and generated review candidates for Curse of the Azure Bonds.

## Scope

Included:

- TITLE
- PIC1–PIC6
- BIGPIC1, BIGPIC2 and BIGPIC6
- HEAD2–HEAD6
- BODY2–BODY6

Deliberately excluded:

- combat maps and tiles;
- combat sprites and icons;
- dungeon walls and first-person world graphics;
- wilderness/game-world terrain systems.

## Inventory

- 20 eligible archives
- 135 blocks
- 231 extracted frames
- 231 master prompt-ledger entries

## Review locations

- Original extractions: `png/`
- Human-readable prompt ledger: `prompts/MASTER_PROMPT_LEDGER.md`
- Machine-readable prompt ledger: `prompts/MASTER_PROMPT_LEDGER.json`
- Spreadsheet-friendly ledger: `prompts/MASTER_PROMPT_LEDGER.csv`
- Generated candidates: `review-candidates/`
- Candidate contact sheets: `contact-sheets/`
- Art-quality rules: `ART_DIRECTION.md`

## Current candidate status

- `PIC1_block_001`: five candidates reviewed and rejected. Candidate E used the corrected prompt but still merged the separate horn into the sword and changed the open scroll into a rolled parchment.
- `BIGPIC2_block_120`: candidate A rejected; candidate B accepted after correcting the prompt's scale hierarchy and cropped without stretching to exact 38:15.
- Eight strong prior eligible replacements are reused: four TITLE screens, BIGPIC1 blocks 121/123, BIGPIC6 block 122 (from a legacy misnamed file), and PIC1 block 80.

No generated candidate is automatically installed in the game. Every image requires ratio, composition, object-count, quality and lifecycle approval first. Current deterministic staging: **9 approved/integrated, 1 rejected entry, 221 missing entries**.

## Deterministic integration

The full-auto runtime is ledger-driven and never infers identity from a loose filename:

- `asset-decisions.json` records explicit review and lifecycle decisions.
- `build_integration_manifest.py` maps all 231 archive/block/frame identities to unique canonical runtime names.
- `validate_candidates.py --strict` checks file presence, PNG validity, minimum dimensions, aspect ratio, complete animation groups, and lifecycle approval.
- `stage_approved_assets.py <HDAssets>` atomically stages only approved, lifecycle-verified assets and writes `runtime-lookup.tsv` for the game.
- `report_status.py` reports generated, missing, approved, rejected, stageable, and integrated counts.
- `runtime_lookup.py` resolves canonical names without collapsing archive, block, or frame identity.

Animated blocks are all-or-nothing: no approved frame is staged unless every frame in that archive/block group is approved. Runtime files are canonicalized as `ARCHIVE_block_NNN_frame_NNN.png`; legacy source filenames may remain unchanged.
