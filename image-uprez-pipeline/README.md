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

- `PIC1-PIC6 block 001`: The maintainer supplied and approved one 1254×1254 treasure still on 2026-07-21 for every treasure scene. The six original frames are byte-identical, so the pipeline deliberately maps the same candidate bytes to all six archive identities.
- `PIC1-PIC6 block 029`: The maintainer supplied and approved the replacement four-frame 1254×1254 night-camp animation set (`10_16_59 AM (1)–(4)`) and requested it everywhere. All six original camp sequences are byte-identical frame-for-frame. Live demo replay verified an atomic camp-to-combat clear with no stale overlay or fallback flash.
- `PIC2 blocks 007, 009-014`: the 2026-07-21 Documents asset pack is reviewed and integrated. Filename order maps complete animation groups for blocks 007, 009 and 010; the four `11_52_31 AM` images map to blocks 011-014. PIC4 block 009 is byte-identical to PIC2 block 009 and deliberately reuses the same five HD frames. Block 009's sixth generated still is retained as an unused alternate because the source block has only five frames. The independently generated animation frames have mild texture/detail shimmer, documented in their review notes.
- `PIC3 blocks 016-019, 025, 027 and 030`: ten recovered HD frames were approved and integrated on 2026-07-23. Block 027 is a complete four-frame animation in source-ledger order.
- `PIC4 blocks 033, 035, 037 and 038`: six recovered HD frames were approved and integrated on 2026-07-23. Block 035 is a complete three-frame animation; block 037 uses the maintainer-selected Option B bytes.
- `PIC4 blocks 039, 040, 041, 049 and 067`: 21 frames were approved and integrated on 2026-07-23 as complete animation groups. Canonical archive/block/frame filenames preserve exact frame order and original delay metadata. Duplicate-state hash contracts require block 039 frame 003 to equal frame 000, block 049 frame 005 to equal frame 002, and block 049 frame 006 to equal frame 001.
- `PIC5 blocks 051-053, 055, 057 and 060`: eleven recovered HD frames were approved and integrated on 2026-07-23. Blocks 052 and 057 are complete animation groups; block 057 frame 003 intentionally returns to byte-identical frame 000 art.
- `PIC6 blocks 068, 072, 073 and 077`: four completed static HD replacements were approved and integrated on 2026-07-23. Remaining original-resolution PIC6 files are not treated as HD candidates.
- `BIGPIC2_block_120`: candidate A rejected; candidate B accepted after correcting the prompt's scale hierarchy and cropped without stretching to exact 38:15.
- `HEAD2/BODY2 block 003`: The maintainer approved the Tiverton innkeeper pair after exact-seam reconstruction and live Full Auto testing. Neck width differs by only 0.42% from the original and both retained portrait layers load together correctly.
- Eight strong prior eligible replacements are reused: four TITLE screens, BIGPIC1 blocks 121/123, BIGPIC6 block 122 (from a legacy misnamed file), and PIC1 block 80.

No generated candidate is automatically installed in the game. Every image requires ratio, composition, object-count, quality and lifecycle approval first. Current deterministic staging: **118 approved/integrated, 2 rejected entries, 111 missing entries**. A production-folder reconciliation found 71 HD-sized PNG files representing 67 unique hashes; 70 files are covered by approved repository assets. The sole excluded file is the documented unused sixth PIC2 block 009 alternate, because that source animation has only five frames.

## Deterministic integration

The full-auto runtime is ledger-driven and never infers identity from a loose filename:

- `asset-decisions.json` records explicit review and lifecycle decisions.
- `build_integration_manifest.py` maps all 231 archive/block/frame identities to unique canonical runtime names.
- `validate_candidates.py --strict` checks file presence, PNG validity, minimum dimensions, aspect ratio, complete animation groups, and lifecycle approval.
- `stage_approved_assets.py <HDAssets>` atomically stages only approved, lifecycle-verified assets and writes `runtime-lookup.tsv` for the game.
- `report_status.py` reports generated, missing, approved, rejected, stageable, and integrated counts.
- `runtime_lookup.py` resolves canonical names without collapsing archive, block, or frame identity.

Animated blocks are all-or-nothing: no approved frame is staged unless every frame in that archive/block group is approved. Runtime files are canonicalized as `ARCHIVE_block_NNN_frame_NNN.png`; legacy source filenames may remain unchanged.

## Next-generation production workflow

`nextgen/` is now the authoritative pre-generation workflow. It locks all
currently accepted HD files and their canonical identities, excludes them from
the generation queue, and blocks staging if an accepted identity's bytes would
change. This preserves existing high-resolution assets exactly.

For stills, it separates hard source facts (ratio, crop, silhouette, count,
overlap, negative space) from reviewable material interpretation. Ambiguous
low-resolution marks are described geometrically rather than forced into an
invented object name. For animations it derives a motion/illumination mask from
the entire source sequence: one HD master is generated, later frames are masked
edits, and all static regions are copied pixel-for-pixel from that master.
Temporal verification also requires duplicate source frames to produce
identical HD output hashes. See `nextgen/README.md`.
