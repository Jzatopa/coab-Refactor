# Opening title sequence rebuild — July 27, 2026

## Scope

- Imported `/home/jzatopa/Downloads/Title Block 1.png` and `Title Block 2.png` as the two full-screen opening bases.
- Rebuilt TITLE blocks 3 and 4 as transparent retained overlays so the exact Title Block 2 scene remains visible beneath each logo.
- Preserved the original logical geometry:
  - block 3: `(48,88,240,112)` → 1440×672 RGBA at 6×.
  - block 4: `(0,88,320,112)` → 1920×672 RGBA at 6×.
- Used the original TITLE.DAX block-2-to-block-3/4 pixel differences as evidence-based placement gates. The HD logo pixels come from the supplied Title Block 3 and 4 artwork.

## Correction

The previous block 3 and 4 assets were opaque crops from separately generated accumulated scenes. Their backgrounds did not match the newly supplied Title Block 2, and block 4 retained visible pixels from the preceding Curse logo. The rebuilt overlays contain transparency outside their own logo geometry. The runtime now renders:

1. supplied Title Block 1;
2. supplied Title Block 2 + Curse of the Azure Bonds logo;
3. the same unchanged Title Block 2 + Forgotten Realms Collection logo.

No rectangular donor-scene patch or previous-title remnant is carried into the later stages.

## Reproduction

```bash
python3 scripts/import_title_sequence_assets.py
python3 image-uprez-pipeline/test_title_sequence_assets.py
```

The importer validates all four supplied source SHA-256 hashes before writing and was run twice with byte-identical output.

## Verification

- `python3 image-uprez-pipeline/test_title_sequence_assets.py`: passed.
- `python3 image-uprez-pipeline/test_integration.py`: passed, 231 lookups and 121 staged assets.
- `python3 image-uprez-pipeline/test_hd_lifecycle_contract.py`: passed for 111 approved PIC identities.
- `COAB_PREPARE_ONLY=1 ./launch.sh`: passed, 121 assets integrated; 108 missing and 2 gated.
- `xbuild /property:Configuration=Release coab.sln`: passed with 0 errors and the existing nonblocking WiX import warning.
- Live 2560×1600 Xvfb capture: all three title stages rendered in sequence, followed by credits. No background seam, clipping, stale Curse-logo pixels, or runtime corruption was visible.
- DeepSeek sidecar review found no demonstrated defect; it flagged color-mask heuristic fragility and insufficient transparent-region sampling as risks. The focused contract was strengthened to verify every fully transparent overlay pixel against the unchanged block-2 base.

Representative live captures are under `live/`; `live/contact.jpg` records the complete 31-second sequence at one frame per second.
