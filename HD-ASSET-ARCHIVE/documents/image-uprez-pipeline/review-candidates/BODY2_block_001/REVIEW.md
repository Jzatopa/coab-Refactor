# BODY2 block 001 — Full-auto review

Original: `../../png/BODY2/BODY2_block_001_frame_000.png`  
Matched portrait: `../../png/HEAD2/HEAD2_block_001_frame_000.png`  
Exact source ratio: **11:6**.

## Superseded candidate A — rejected

`superseded-village-reference-A.png` was already in flight when the human-reference hierarchy changed. It used the village image instead of the required logo-free `HDAssets/Title Block 2.png` person reference and also changed the arm/hand, weapon, chest-plate and black-negative-space geometry. It is retained only as superseded evidence.

## Candidate B with correct person reference — rejected

Candidate B used the enlarged original as composition authority, `Title Block 2.png` for human realism, and the matching HEAD2 extraction for identity/lighting context. It has strong materials, but materially changes the source: both hands become larger and more explicit, the far-right hand/fingers alter the crop, the sword/strap and central plate change thickness and termination, the purple cloth distribution moves, and hard black internal cutouts become continuous red cloth.

## Attempt 2 localized edit — rejected; identity explicitly handled as rejected

The localized correction pass reduced the added far-right hand but omitted/abstracted the source hand/bracer detail, distorted the screen-left hand, kept the central plate and diagonal object at the wrong bounding boxes, enlarged hard black voids, and reduced the cloth/metal anatomy into coarse shapes. The exact-ratio file is 1694×924 (11:6). The two-attempt source-lock gate is exhausted; do not stage.

Rejected comparison: `../../review-evidence/BODY2_block_001_attempt2_rejected_compare.jpg`.

A future human-QC retry must first add one shared asset-specific lighting contract to both BODY2 block 001 and HEAD2 block 001 prompts, then use the enlarged original as input 1 and `Title Block 2.png` only for finish/anatomy quality.
