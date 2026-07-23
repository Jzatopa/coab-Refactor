# Source-Locked Generation Workflow

This workflow is designed to produce an approvable asset in one or two attempts.

## Attempt 1 — faithful style conversion

Inputs, in order:

1. nearest-neighbor enlarged original extraction — authoritative composition;
2. optional annotated/masked original — authoritative object boundaries;
3. subject-appropriate finish reference only:
   - `HDAssets/Title Block 2.png` for people, heads, bodies, portraits and humanoid creatures;
   - `HDAssets/PIC1_block_080_village.png` for environments, architecture, objects and non-character scenes.

`Title Block 2.png` is the opening image with a clearly rendered person and no visible title logo/text. When used, it controls only human realism, anatomy quality, skin, practical costume materials and lighting. It must not transfer the woman's identity, pose, armor design or composition into the target asset.

Prompt structure:

1. one-sentence edit instruction;
2. exact object/figure count and checklist;
3. exact spatial relationships and crop;
4. forbidden omissions, merges, additions, or redesigns;
5. desired realistic materials and finish.
6. one explicit asset-specific lighting sentence derived from the source.

Lead instruction:

> Transform input image 1 into grounded photoreal live-action Forgotten Realms fantasy. Preserve every object, silhouette, overlap, crop, position, orientation, color role, empty area, and exact aspect ratio. Input image 2, if supplied, defines finish only. Change only rendering style and material detail.

## Attempt 2 — localized edit

Use candidate A as the editable input, with the enlarged original supplied again as the composition reference. Name only the failed details. Example:

> Keep the current image unchanged except for these corrections: restore the separate curved horn at upper left; change the lower-left parchment into one fully open scroll; reduce the helmet to the original bounding box. Match input image 2 for those positions and silhouettes. Do not alter lighting, coins, sword, bottle, gemstones, camera, or crop.

Do not repeat a full scene-generation prompt for attempt 2.

## Lighting

Do not reuse one generic lighting description across all assets. Record the target's key direction, softness, temperature, fill, contrast, rim/magical light and background spill before generating. For matched HEAD/BODY components, use the same lighting sentence in both prompts and review the combined 88×88 game-layout composite before either component is approved.

## HEAD/BODY combined-first workflow

The engine stacks HEAD at y=0 and BODY at y=40 logical pixels with no overlap. Create the first high-resolution version as one coherent 88×88-equivalent portrait, then split it at 45.4545% height. This establishes a seamless matched pair and the neck/collar connector template used by later interchangeable parts.

Acceptance requires:

- no black gap or floating head;
- continuous neck anatomy into the collar;
- identical key, fill and rim lighting across both panels;
- consistent scale, skin tone and texture density;
- exact 11:5 HEAD and 11:6 BODY ratios after splitting;
- clean recombination at the engine's no-overlap seam;
- a cross-pair test using another generated head on the same body.

Iterate the combined portrait rather than independently regenerating the cropped pieces. Keep a numbered iteration log. If six combined-layout iterations fail to produce both a seamless matched pair and a credible reusable connector, stop and review the evidence with the maintainer before proceeding.

### Fast in-game test loop

Use the woman figure shown shortly after character creation in a new game as the primary live HEAD/BODY validation scene. It is quick to reach and exercises the engine's real two-asset rendering path. For every interchangeability iteration:

1. stage the separate HEAD and BODY files in the isolated Full Auto runtime;
2. start a new game and complete/advance past character creation;
3. capture the first woman HEAD/BODY figure at full presentation resolution;
4. inspect the live render for floating, seams, scale, connector position, lighting, skin-tone continuity and stale overlays;
5. compare the live capture with the offline exact-stack composite;
6. reject any pair whose offline composite looks correct but whose actual game render does not.

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
