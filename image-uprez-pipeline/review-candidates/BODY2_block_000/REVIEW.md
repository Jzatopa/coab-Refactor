# BODY2 block 000 — Full-auto review

Original: `../../png/BODY2/BODY2_block_000_frame_000.png`  
Matched future portrait: `../../png/HEAD2/HEAD2_block_000_frame_000.png`  
Exact source ratio: **11:6**.

## Candidate A — rejected

Candidate A is retained as `candidate-A.png` and `candidate-A-exact-ratio.png`. It has strong photoreal materials, but it changes the source composition and costume geometry: it exposes a dark neck/throat area, broadens and lowers the torso crop, enlarges the riveted pauldrons, replaces the source diagonal-baldric-plus-lower-belt arrangement with one dominant strap, turns the two small gold fixtures into one oversized central buckle, enlarges and relocates the purple heraldic animal, and invents extra leather/arm-armor detail. The purported exact-ratio derivative also remained 1698×926 rather than an exact integer 11:6 frame.

Rejected comparison: `../../review-evidence/BODY2_block_000_candidate-A_rejected_compare.jpg`.

## Prompt correction after candidate A

The authored portrait ledger and all normalized master-ledger formats now explicitly lock:

- zero visible skin, throat, neck or head;
- the neckline touching the top edge;
- simple rounded pauldrons, brown upper arms and lower torso clipped by the source edges;
- one slim diagonal baldric from upper screen-left to lower screen-right plus a crossing lower waist belt;
- two small gold buckle/fixture shapes, not one large central buckle;
- a tiny turquoise top-edge clasp and narrow magenta accents;
- one compact purple rearing animal on the upper screen-right chest;
- no extra rivets, rims, trim, armor segments or near-black background falloff;
- youthful athletic build and neutral frontal lighting compatible with the young dark-skinned man in HEAD2 block 000.

Candidate B generation had already started from the previously normalized exact ledger prompt when this stricter standing rejection workflow arrived.

## Candidates B–E — rejected

All four generated candidates are preserved as `candidate-B.png` through `candidate-E.png`. They have credible photoreal materials but repeat the same critical source-fidelity failures: each treats the top-center black cutout as a physical dark throat/neck opening, omits the separate lower waist belt, enlarges a central gold buckle, enlarges or relocates the purple heraldic animal, and adds ornate rivets, leather rims or sculpted armor geometry. Candidate E is the closest of the batch, but it still fails the torso cutout, belt map, buckle scale and emblem scale locks.

Rejected comparisons:

- `../../review-evidence/BODY2_block_000_candidate-B_rejected_compare.jpg`
- `../../review-evidence/BODY2_block_000_candidate-C_rejected_compare.jpg`
- `../../review-evidence/BODY2_block_000_candidate-D_rejected_compare.jpg`
- `../../review-evidence/BODY2_block_000_candidate-E_rejected_compare.jpg`

## Prompt correction after candidates B–E

The ledger was revised again before further generation. It now defines the top-center black shape as a small pure-black background cutout for the separate HEAD panel rather than anatomy, forbids all skin, locks exactly one narrow upper-screen-left to lower-screen-right baldric plus one separate almost-horizontal lower waist belt, locks exactly two small square gold fixtures, and explicitly forbids a large central buckle, parallel straps, X harness, ornate yoke, rivets, leather rims, decorative edging and sculpted abdominal plates. The corrected normalized master prompt must be used verbatim with both original BODY2 and HEAD2 conditioning images for the next attempt.

## Candidate B — rejected

Candidate B improves the all-black background and removes visible neck skin, but still fails the corrected normalized prompt. It uses oversized layered pauldrons and segmented armor with ornate rims and rivets, one large central gold buckle, a large detailed unicorn-head emblem, extra leather/armor structures, and a broad lower-torso crop. It does not preserve the compact pixel silhouette, the slim baldric plus low crossing belt, the two small gold fixtures, or the small rearing-animal mark. Retained only as rejection evidence; do not stage.

## Candidate C — rejected

Candidate C was generated from the corrected normalized prompt with both BODY2 and matching HEAD2 conditioning. It is substantially closer, with the right compact crop, black wedges, one diagonal baldric, low belt, top-edge clasp and rearing emblem. It remains rejected because the diagonal fixture is still oversized and dominant, the pauldrons retain extra rims/segmentation, the straps retain small rivet details, and the top magenta treatment is broader than the source lock. Do not stage.

## Candidate D — rejected; identity explicitly handled as rejected

Candidate D used the corrected exact prompt with BODY2, matched HEAD2 and candidate-C refinement conditioning. It still preserves too-wide/rimmed pauldrons, a dominant diagonal buckle, a third prominent gold clasp/buckle, strap holes, a wide baldric and extra leather detail. The provider repeatedly converged on the same costume redesign across four attempts. This identity remains explicitly rejected rather than approving a weak match. A future retry must begin from the current corrected normalized prompt and the original BODY2/HEAD2 references.
