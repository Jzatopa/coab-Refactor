# PIC1–3 photoreal generation prompts

Source dimensions and ratio for every file: **88×88 px, 1:1**. Generate at **1024×1024 px** with no stretching or crop change. Apply `global_prompt` and `global_constraints` from `PIC1-3-prompts.json` to every entry below; its JSON group supplies the detailed scene, image-specific prompt, constraints and (for animation) the shared identity lock plus exact frame delta.

## PIC1

| File | Group | Frame-specific state |
|---|---|---|
| PIC1_block_001_frame_000.png | PIC1-001 | static diagonal ritual weapon |
| PIC1_block_029_frame_000–003.png | PIC1-029 | ember → right lean → tall upright → ember |
| PIC1_block_080_frame_000.png | PIC1-080 | static village yard |

## PIC2

| File | Group | Frame-specific state |
|---|---|---|
| PIC2_block_001_frame_000.png | PIC2-001 | static diagonal ritual weapon |
| PIC2_block_007_frame_000–007.png | PIC2-007 | left claw: low, out, retract, side reach, long reach, mid, near torso, out |
| PIC2_block_009_frame_000–004.png | PIC2-009 | upper-right appendage: minimal, in, out, small, full |
| PIC2_block_010_frame_000–002.png | PIC2-010 | forearm magic: bright, faded, bright |
| PIC2_block_011_frame_000.png | PIC2-011 | static wagon |
| PIC2_block_012_frame_000.png | PIC2-012 | static interior trio |
| PIC2_block_013_frame_000.png | PIC2-013 | static confrontation trio |
| PIC2_block_014_frame_000.png | PIC2-014 | static sword/obelisk |
| PIC2_block_029_frame_000–003.png | PIC2-029 | ember → right lean → tall upright → ember |

## PIC3

| File | Group | Frame-specific state |
|---|---|---|
| PIC3_block_001_frame_000.png | PIC3-001 | static diagonal ritual weapon |
| PIC3_block_016_frame_000.png | PIC3-016 | static wasteland sinkhole |
| PIC3_block_017_frame_000.png | PIC3-017 | static four-face palisade tableau |
| PIC3_block_018_frame_000.png | PIC3-018 | static captive woman and claw |
| PIC3_block_019_frame_000.png | PIC3-019 | static palm eye |
| PIC3_block_025_frame_000.png | PIC3-025 | static hooded wraith |
| PIC3_block_027_frame_000–003.png | PIC3-027 | gaze right → blink → gaze forward → blink |
| PIC3_block_029_frame_000–003.png | PIC3-029 | ember → right lean → tall upright → ember |
| PIC3_block_030_frame_000.png | PIC3-030 | static swan with fan-wing |

Every filename is enumerated in the `frames` arrays of the JSON, where each has an exact scene-specific generation instruction. Animation renderers must use the group’s `shared_scene_identity` as a fixed reference and apply only that filename’s frame delta.
