# Source-Locked Generation Workflow

This workflow is designed to produce an approvable asset in one or two attempts.

## Attempt 1 — faithful style conversion

Inputs, in order:

1. nearest-neighbor enlarged original extraction — authoritative composition;
2. optional annotated/masked original — authoritative object boundaries;
3. `HDAssets/PIC1_block_080_village.png` — finish and realism reference only.

Prompt structure:

1. one-sentence edit instruction;
2. exact object/figure count and checklist;
3. exact spatial relationships and crop;
4. forbidden omissions, merges, additions, or redesigns;
5. desired realistic materials and finish.

Lead instruction:

> Transform input image 1 into grounded photoreal live-action Forgotten Realms fantasy. Preserve every object, silhouette, overlap, crop, position, orientation, color role, empty area, and exact aspect ratio. Input image 2, if supplied, defines finish only. Change only rendering style and material detail.

## Attempt 2 — localized edit

Use candidate A as the editable input, with the enlarged original supplied again as the composition reference. Name only the failed details. Example:

> Keep the current image unchanged except for these corrections: restore the separate curved horn at upper left; change the lower-left parchment into one fully open scroll; reduce the helmet to the original bounding box. Match input image 2 for those positions and silhouettes. Do not alter lighting, coins, sword, bottle, gemstones, camera, or crop.

Do not repeat a full scene-generation prompt for attempt 2.

## Review gate

Compare original and candidate side by side. Review in this order:

1. object/figure count;
2. crop and aspect ratio;
3. bounding boxes and overlaps;
4. silhouette and facing direction;
5. omitted, merged, or invented details;
6. anatomy and material realism;
7. lifecycle suitability.

If attempt 2 fails, preserve and send the comparison for human QC, revise the asset-specific prompt/annotation, and do not install the candidate.
