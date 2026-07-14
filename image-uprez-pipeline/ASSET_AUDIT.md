# Eligible Asset Audit

- Eligible extracted frames: **231**
- Manifest rows matched: **231/231**
- Unique source images by SHA-256: **175**
- Duplicate frame rows reusable after one approved generation: **56**
- Prompt content checks passed: **231/231**
- Eligible frames already integrated from strong prior assets: **8**
- Eligible frames integrated under canonical archive paths: **1**
- Frames with reviewed/rejected candidates: **1**
- Frames still requiring an approved generation: **221**

## Prompt-ledger audit

All 231 entries have a substantial generation prompt and resolve to an extracted source PNG. The combined ledger has incomplete convenience metadata in some imported rows; runtime identity is therefore derived from the authoritative source filename and cross-checked against `manifest.json`.

Metadata gaps: `{}`.

## Candidate review

Review directories currently contain **13** candidate PNG files. Per-entry approval and rejection decisions are recorded in `REVIEW.md` files and `asset-decisions.json`; the audit does not infer approval from file presence.

## Status by frame

| Source | Status | Integrated path | Duplicate group |
|---|---|---|---:|
| `png/BIGPIC1/BIGPIC1_block_121_frame_000.png` | integrated-existing | `HDAssets/BIGPIC1_block_121.png` | 1 |
| `png/BIGPIC1/BIGPIC1_block_123_frame_000.png` | integrated-existing | `HDAssets/BIGPIC1_block_123.png` | 1 |
| `png/BIGPIC2/BIGPIC2_block_120_frame_000.png` | integrated-generated | `HDAssets/BIGPIC2/BIGPIC2_block_120_frame_000.png` | 1 |
| `png/BIGPIC6/BIGPIC6_block_122_frame_000.png` | integrated-existing | `HDAssets/BIGPIC1_block_122.png` | 1 |
| `png/BODY2/BODY2_block_000_frame_000.png` | missing-generation | — | 1 |
| `png/BODY2/BODY2_block_001_frame_000.png` | missing-generation | — | 1 |
| `png/BODY2/BODY2_block_002_frame_000.png` | missing-generation | — | 1 |
| `png/BODY2/BODY2_block_003_frame_000.png` | missing-generation | — | 3 |
| `png/BODY2/BODY2_block_004_frame_000.png` | missing-generation | — | 1 |
| `png/BODY2/BODY2_block_005_frame_000.png` | missing-generation | — | 1 |
| `png/BODY2/BODY2_block_006_frame_000.png` | missing-generation | — | 1 |
| `png/BODY2/BODY2_block_065_frame_000.png` | missing-generation | — | 2 |
| `png/BODY3/BODY3_block_003_frame_000.png` | missing-generation | — | 3 |
| `png/BODY3/BODY3_block_016_frame_000.png` | missing-generation | — | 2 |
| `png/BODY3/BODY3_block_017_frame_000.png` | missing-generation | — | 1 |
| `png/BODY3/BODY3_block_018_frame_000.png` | missing-generation | — | 1 |
| `png/BODY3/BODY3_block_019_frame_000.png` | missing-generation | — | 1 |
| `png/BODY3/BODY3_block_022_frame_000.png` | missing-generation | — | 1 |
| `png/BODY4/BODY4_block_032_frame_000.png` | missing-generation | — | 1 |
| `png/BODY4/BODY4_block_033_frame_000.png` | missing-generation | — | 1 |
| `png/BODY4/BODY4_block_034_frame_000.png` | missing-generation | — | 1 |
| `png/BODY4/BODY4_block_035_frame_000.png` | missing-generation | — | 1 |
| `png/BODY4/BODY4_block_042_frame_000.png` | missing-generation | — | 1 |
| `png/BODY4/BODY4_block_049_frame_000.png` | missing-generation | — | 1 |
| `png/BODY4/BODY4_block_070_frame_000.png` | missing-generation | — | 2 |
| `png/BODY5/BODY5_block_003_frame_000.png` | missing-generation | — | 3 |
| `png/BODY5/BODY5_block_049_frame_000.png` | missing-generation | — | 1 |
| `png/BODY5/BODY5_block_050_frame_000.png` | missing-generation | — | 1 |
| `png/BODY5/BODY5_block_051_frame_000.png` | missing-generation | — | 1 |
| `png/BODY5/BODY5_block_058_frame_000.png` | missing-generation | — | 1 |
| `png/BODY5/BODY5_block_059_frame_000.png` | missing-generation | — | 1 |
| `png/BODY6/BODY6_block_016_frame_000.png` | missing-generation | — | 2 |
| `png/BODY6/BODY6_block_064_frame_000.png` | missing-generation | — | 1 |
| `png/BODY6/BODY6_block_065_frame_000.png` | missing-generation | — | 2 |
| `png/BODY6/BODY6_block_070_frame_000.png` | missing-generation | — | 2 |
| `png/HEAD2/HEAD2_block_000_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD2/HEAD2_block_001_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD2/HEAD2_block_002_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD2/HEAD2_block_003_frame_000.png` | missing-generation | — | 3 |
| `png/HEAD2/HEAD2_block_004_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD2/HEAD2_block_005_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD2/HEAD2_block_006_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD2/HEAD2_block_008_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD2/HEAD2_block_009_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD2/HEAD2_block_065_frame_000.png` | missing-generation | — | 2 |
| `png/HEAD3/HEAD3_block_003_frame_000.png` | missing-generation | — | 3 |
| `png/HEAD3/HEAD3_block_016_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD3/HEAD3_block_017_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD3/HEAD3_block_018_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD3/HEAD3_block_019_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD3/HEAD3_block_020_frame_000.png` | missing-generation | — | 2 |
| `png/HEAD3/HEAD3_block_021_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD3/HEAD3_block_022_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD3/HEAD3_block_024_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD4/HEAD4_block_032_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD4/HEAD4_block_033_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD4/HEAD4_block_034_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD4/HEAD4_block_035_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD4/HEAD4_block_036_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD4/HEAD4_block_037_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD4/HEAD4_block_038_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD4/HEAD4_block_042_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD4/HEAD4_block_049_frame_000.png` | missing-generation | — | 2 |
| `png/HEAD4/HEAD4_block_070_frame_000.png` | missing-generation | — | 2 |
| `png/HEAD5/HEAD5_block_003_frame_000.png` | missing-generation | — | 3 |
| `png/HEAD5/HEAD5_block_049_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD5/HEAD5_block_050_frame_000.png` | missing-generation | — | 2 |
| `png/HEAD5/HEAD5_block_051_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD5/HEAD5_block_058_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD5/HEAD5_block_059_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD6/HEAD6_block_020_frame_000.png` | missing-generation | — | 2 |
| `png/HEAD6/HEAD6_block_064_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD6/HEAD6_block_065_frame_000.png` | missing-generation | — | 2 |
| `png/HEAD6/HEAD6_block_067_frame_000.png` | missing-generation | — | 1 |
| `png/HEAD6/HEAD6_block_070_frame_000.png` | missing-generation | — | 2 |
| `png/PIC1/PIC1_block_001_frame_000.png` | candidates-rejected | — | 6 |
| `png/PIC1/PIC1_block_029_frame_000.png` | missing-generation | — | 6 |
| `png/PIC1/PIC1_block_029_frame_001.png` | missing-generation | — | 6 |
| `png/PIC1/PIC1_block_029_frame_002.png` | missing-generation | — | 6 |
| `png/PIC1/PIC1_block_029_frame_003.png` | missing-generation | — | 6 |
| `png/PIC1/PIC1_block_080_frame_000.png` | integrated-existing | `HDAssets/PIC1_block_080_village.png` | 1 |
| `png/PIC2/PIC2_block_001_frame_000.png` | missing-generation | — | 6 |
| `png/PIC2/PIC2_block_007_frame_000.png` | missing-generation | — | 1 |
| `png/PIC2/PIC2_block_007_frame_001.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_007_frame_002.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_007_frame_003.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_007_frame_004.png` | missing-generation | — | 1 |
| `png/PIC2/PIC2_block_007_frame_005.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_007_frame_006.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_007_frame_007.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_009_frame_000.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_009_frame_001.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_009_frame_002.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_009_frame_003.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_009_frame_004.png` | missing-generation | — | 2 |
| `png/PIC2/PIC2_block_010_frame_000.png` | missing-generation | — | 1 |
| `png/PIC2/PIC2_block_010_frame_001.png` | missing-generation | — | 1 |
| `png/PIC2/PIC2_block_010_frame_002.png` | missing-generation | — | 1 |
| `png/PIC2/PIC2_block_011_frame_000.png` | missing-generation | — | 1 |
| `png/PIC2/PIC2_block_012_frame_000.png` | missing-generation | — | 1 |
| `png/PIC2/PIC2_block_013_frame_000.png` | missing-generation | — | 1 |
| `png/PIC2/PIC2_block_014_frame_000.png` | missing-generation | — | 1 |
| `png/PIC2/PIC2_block_029_frame_000.png` | missing-generation | — | 6 |
| `png/PIC2/PIC2_block_029_frame_001.png` | missing-generation | — | 6 |
| `png/PIC2/PIC2_block_029_frame_002.png` | missing-generation | — | 6 |
| `png/PIC2/PIC2_block_029_frame_003.png` | missing-generation | — | 6 |
| `png/PIC3/PIC3_block_001_frame_000.png` | missing-generation | — | 6 |
| `png/PIC3/PIC3_block_016_frame_000.png` | missing-generation | — | 1 |
| `png/PIC3/PIC3_block_017_frame_000.png` | missing-generation | — | 1 |
| `png/PIC3/PIC3_block_018_frame_000.png` | missing-generation | — | 1 |
| `png/PIC3/PIC3_block_019_frame_000.png` | missing-generation | — | 1 |
| `png/PIC3/PIC3_block_025_frame_000.png` | missing-generation | — | 1 |
| `png/PIC3/PIC3_block_027_frame_000.png` | missing-generation | — | 1 |
| `png/PIC3/PIC3_block_027_frame_001.png` | missing-generation | — | 1 |
| `png/PIC3/PIC3_block_027_frame_002.png` | missing-generation | — | 1 |
| `png/PIC3/PIC3_block_027_frame_003.png` | missing-generation | — | 1 |
| `png/PIC3/PIC3_block_029_frame_000.png` | missing-generation | — | 6 |
| `png/PIC3/PIC3_block_029_frame_001.png` | missing-generation | — | 6 |
| `png/PIC3/PIC3_block_029_frame_002.png` | missing-generation | — | 6 |
| `png/PIC3/PIC3_block_029_frame_003.png` | missing-generation | — | 6 |
| `png/PIC3/PIC3_block_030_frame_000.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_001_frame_000.png` | missing-generation | — | 6 |
| `png/PIC4/PIC4_block_009_frame_000.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_009_frame_001.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_009_frame_002.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_009_frame_003.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_009_frame_004.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_029_frame_000.png` | missing-generation | — | 6 |
| `png/PIC4/PIC4_block_029_frame_001.png` | missing-generation | — | 6 |
| `png/PIC4/PIC4_block_029_frame_002.png` | missing-generation | — | 6 |
| `png/PIC4/PIC4_block_029_frame_003.png` | missing-generation | — | 6 |
| `png/PIC4/PIC4_block_033_frame_000.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_035_frame_000.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_035_frame_001.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_035_frame_002.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_037_frame_000.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_038_frame_000.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_039_frame_000.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_039_frame_001.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_039_frame_002.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_039_frame_003.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_040_frame_000.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_040_frame_001.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_040_frame_002.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_040_frame_003.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_041_frame_000.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_041_frame_001.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_049_frame_000.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_049_frame_001.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_049_frame_002.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_049_frame_003.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_049_frame_004.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_049_frame_005.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_049_frame_006.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_049_frame_007.png` | missing-generation | — | 1 |
| `png/PIC4/PIC4_block_067_frame_000.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_067_frame_001.png` | missing-generation | — | 2 |
| `png/PIC4/PIC4_block_067_frame_002.png` | missing-generation | — | 2 |
| `png/PIC5/PIC5_block_001_frame_000.png` | missing-generation | — | 6 |
| `png/PIC5/PIC5_block_029_frame_000.png` | missing-generation | — | 6 |
| `png/PIC5/PIC5_block_029_frame_001.png` | missing-generation | — | 6 |
| `png/PIC5/PIC5_block_029_frame_002.png` | missing-generation | — | 6 |
| `png/PIC5/PIC5_block_029_frame_003.png` | missing-generation | — | 6 |
| `png/PIC5/PIC5_block_051_frame_000.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_052_frame_000.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_052_frame_001.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_052_frame_002.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_053_frame_000.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_054_frame_000.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_054_frame_001.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_054_frame_002.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_054_frame_003.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_054_frame_004.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_055_frame_000.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_057_frame_000.png` | missing-generation | — | 2 |
| `png/PIC5/PIC5_block_057_frame_001.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_057_frame_002.png` | missing-generation | — | 1 |
| `png/PIC5/PIC5_block_057_frame_003.png` | missing-generation | — | 2 |
| `png/PIC5/PIC5_block_060_frame_000.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_001_frame_000.png` | missing-generation | — | 6 |
| `png/PIC6/PIC6_block_029_frame_000.png` | missing-generation | — | 6 |
| `png/PIC6/PIC6_block_029_frame_001.png` | missing-generation | — | 6 |
| `png/PIC6/PIC6_block_029_frame_002.png` | missing-generation | — | 6 |
| `png/PIC6/PIC6_block_029_frame_003.png` | missing-generation | — | 6 |
| `png/PIC6/PIC6_block_064_frame_000.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_064_frame_001.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_064_frame_002.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_064_frame_003.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_064_frame_004.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_064_frame_005.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_064_frame_006.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_064_frame_007.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_065_frame_000.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_065_frame_001.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_065_frame_002.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_065_frame_003.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_065_frame_004.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_067_frame_000.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_067_frame_001.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_067_frame_002.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_068_frame_000.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_069_frame_000.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_069_frame_001.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_069_frame_002.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_069_frame_003.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_071_frame_000.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_071_frame_001.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_071_frame_002.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_071_frame_003.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_072_frame_000.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_073_frame_000.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_074_frame_000.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_074_frame_001.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_074_frame_002.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_074_frame_003.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_074_frame_004.png` | missing-generation | — | 2 |
| `png/PIC6/PIC6_block_074_frame_005.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_074_frame_006.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_075_frame_000.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_075_frame_001.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_075_frame_002.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_075_frame_003.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_075_frame_004.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_076_frame_000.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_076_frame_001.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_076_frame_002.png` | missing-generation | — | 1 |
| `png/PIC6/PIC6_block_077_frame_000.png` | missing-generation | — | 1 |
| `png/TITLE/TITLE_block_001_frame_000.png` | integrated-existing | `HDAssets/Title Block 1.png` | 1 |
| `png/TITLE/TITLE_block_002_frame_000.png` | integrated-existing | `HDAssets/Title Block 2.png` | 1 |
| `png/TITLE/TITLE_block_003_frame_000.png` | integrated-existing | `HDAssets/Title Block 3.png` | 1 |
| `png/TITLE/TITLE_block_004_frame_000.png` | integrated-existing | `HDAssets/Title Block 4.png` | 1 |
