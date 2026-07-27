# Native-8x title typography sharpening — July 27, 2026

## Change

The opening title assets were rebuilt directly at the engine's 8x logical resolution instead of being stored at 6x and enlarged again at runtime:

- TITLE block 1: 2560×1600 RGB.
- TITLE block 2: 2560×1600 RGB, unchanged photographic scene treatment.
- TITLE block 3: 1920×896 RGBA for logical rectangle `(48,88,240,112)`.
- TITLE block 4: 2560×896 RGBA for logical rectangle `(0,88,320,112)`.

The typography/logo pixels receive a restrained unsharp mask. Logo alpha construction now uses an 8x-scaled evidence gate, a 9-pixel edge expansion, and a reduced 0.45-pixel Gaussian edge treatment instead of the previous 1.0-pixel blur. The photographic Title Block 2 scene is not sharpened.

## Visual result

- SSI/AD&D lettering has clearer highlight and shadow boundaries.
- Curse of the Azure Bonds strokes and fine horizontal rules are crisper.
- Forgotten Realms plaque lettering and subtitle have stronger edge definition.
- No rectangular overlay seam, clipped stroke, stale Curse-logo remnant, ringing halo, or visible damage to the photographic scene was found in the live sequence.

`before-after-contact.jpg` shows the previous 6x runtime captures beside the native-8x live captures.

## Verification

- Importer rerun produced byte-identical outputs.
- `python3 image-uprez-pipeline/test_title_sequence_assets.py`: passed.
- `python3 image-uprez-pipeline/test_integration.py`: passed, 231 lookups and 121 staged assets.
- `python3 image-uprez-pipeline/test_hd_lifecycle_contract.py`: passed for 111 approved PIC identities.
- `COAB_PREPARE_ONLY=1 ./launch.sh`: passed, 121 assets integrated; 108 missing and 2 gated.
- `xbuild /property:Configuration=Release coab.sln`: passed with zero errors and the existing nonblocking WiX import warning.
- Live 2560×1600 Xvfb capture completed through all title stages and credits.
- DeepSeek sidecar review found no concrete risk or blocker in the supplied implementation and validation evidence.
