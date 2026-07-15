# Curse of the Azure Bonds — HD Image Art Direction

## Quality reference

`HDAssets/PIC1_block_080_village.png` is the minimum realism and finish standard.

Every generated image must equal or exceed its:

- grounded photographic realism;
- natural, physically coherent lighting;
- convincing stone, timber, cloth, leather, metal, earth, vegetation and skin;
- coherent camera perspective and depth;
- environmental detail without visual clutter;
- serious Forgotten Realms high-fantasy atmosphere;
- fidelity to the original scene composition.

## Cohesive presentation

All replacements should feel photographed from the same prestige live-action fantasy production:

- realistic late-medieval materials and construction;
- practical costumes and armor rather than glossy cosplay;
- restrained cinematic color grading;
- subtle filmic contrast and atmospheric depth;
- natural skin texture and believable anatomy;
- magic represented as physically present light, energy, smoke or material transformation;
- no modern objects, typography, logos or interface elements;
- no cartoon, anime, painterly concept-art, plastic 3D-render or generic AI-fantasy appearance.

## Composition lock

The original extraction is the authoritative composition reference. Preserve:

1. original aspect ratio;
2. camera angle and horizon placement;
3. relative scale and position of major subjects;
4. silhouettes and facing directions;
5. architecture and environmental divisions;
6. negative space needed for readability;
7. number and broad identity of important people, creatures and objects;
8. foreground, middle-ground and background proportions.

Small details may be clarified, but the image must remain immediately recognizable as the same scene.

## Generation method — source-locked edit workflow

Use an **image edit/reference workflow**, not text-to-image reconstruction from prose alone.

1. Enlarge the original extraction with nearest-neighbor scaling so its shapes and object boundaries are plainly visible. Use this as the first and primary input image.
2. Choose the second input by subject type, and never let it replace the first image's composition:
   - **people, heads, bodies, portraits and humanoid creatures:** use `HDAssets/Title Block 2.png` as the human realism, anatomy, skin, costume and lighting reference. It contains the opening-scene woman without title logos or text;
   - **environments, architecture, objects and non-character scenes:** use `HDAssets/PIC1_block_080_village.png` as the material, lighting and environmental-finish reference.
3. Prefer a short, direct first-pass instruction: **“Transform input image 1 into grounded photoreal live-action fantasy. Preserve every object, silhouette, overlap, crop, position, orientation, color role, empty area, and exact aspect ratio. Input image 2 defines finish only. Change only rendering style and material detail.”** For portraits, explicitly state that input image 2 controls realistic human anatomy, skin, costume materials and lighting—not identity, pose, clothing design or composition. Append only the asset-specific object checklist and prohibited changes.
4. Do not bury the composition instruction inside a long cinematic prompt. Put the invariant instruction first and repeat the highest-risk details at the end.
5. If the first result is close, make the second attempt as an **edit of the first result**, supplying the original reference again and requesting only the named corrections. Do not regenerate the entire scene from scratch.
6. Use high input fidelity when the provider/model exposes that control. For multi-image input, explicitly identify which image controls composition and which controls finish.
7. For tiny or ambiguous originals, create a temporary annotated composition reference with numbered objects, boundary boxes, arrows, or flat-color masks. Use it as an additional reference; annotations must not appear in the final output.
8. Stop after two failed attempts and escalate for human QC rather than repeatedly spending generations on an unchanged strategy.

## Asset-specific lighting contract

Every uprez prompt must define lighting for that exact asset rather than relying on a generic cinematic-style phrase. Before generation, inspect the original and record:

- key-light direction and height;
- key softness or hardness;
- brightness/contrast level;
- warm, neutral or cool color temperature;
- fill-light strength and shadow depth;
- rim, magical or environmental light if visibly present;
- background illumination and whether empty black areas must remain unlit.

Write one concise lighting sentence into the asset prompt. Example: **“Soft neutral key light from upper screen-left, weak frontal fill, restrained cool rim on screen-right, medium contrast, and no spill into the pure-black background.”**

Connected HEAD/BODY components must share one lighting contract so skin, armor, cloth, shadow direction and seam brightness match when the game stacks them. The realism reference defines quality only; it does not override the target asset's authored lighting.

The first attempt should establish fidelity. The second attempt should be a narrow correction pass, not another broad reinterpretation.

## Resolution

Generate square panels at 1024×1024 minimum. Generate non-square images at the closest supported resolution that preserves the source ratio, then crop only if required to restore the exact source ratio. Never stretch.

The final review file must have the same aspect ratio as its original extraction.

## Rejection criteria

Reject or regenerate images with:

- changed composition or subject proportions;
- missing or invented major subjects;
- incorrect number of people or creatures;
- distorted faces, hands, anatomy or architecture;
- modern, steampunk or science-fiction contamination;
- illegible clutter;
- oversaturated fantasy colors;
- excessive shallow depth of field hiding important content;
- painterly, illustrative or obviously synthetic surfaces;
- text, signatures, watermarks or borders;
- quality below PIC1 block 80.
