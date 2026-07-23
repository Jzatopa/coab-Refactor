# Next-generation HD asset production

This directory is the production workflow for assets that are **not already
approved HD assets**. It never writes to `HDAssets/`, the game runtime, or the
approval ledger. Those actions remain deliberately human-approved staging
steps.

## What changed

The old workflow treated a plausible semantic reading of every low-resolution
pixel as a hard requirement and asked a model to regenerate each animation
frame as a separate illustration. That caused invented details, unnecessary
rejections, and temporal shimmer.

This workflow treats the source image as a contract with two kinds of rules:

- **hard:** archive/block/frame identity, source ratio, crop, major silhouette,
  count, overlap, negative space, source-defined animation timing, and frozen
  animation pixels;
- **reviewable:** material interpretation, tiny ambiguous details, and whether
  the result reaches the right category-specific finish.

An ambiguous mark is described by geometry and color role, never promoted to a
confident object name without supporting evidence.

## Production path

1. Run `lock_existing_hd_assets.py` once, then use `--verify` before any batch.
   The resulting registry excludes all already-approved HD identities and
   records exact file hashes. `stage_approved_assets.py` refuses to replace a
   protected identity with different bytes.
2. Run `build_generation_jobs.py`. It emits a reviewable job queue for only
   missing or strategically re-opened entries. It retains prior failed
   candidates as evidence; `rejected` is not a permanent artistic verdict.
3. For a still, create one source-locked image edit: enlarged source first,
   optional geometry annotation second, finish reference last. Keep source
   geometry and crop; improve material and photographic detail only.
4. For a portrait pair, generate one 88×88-equivalent master portrait and
   split it once at the engine's 40/88 seam. Validate cross-pair connector
   bands separately before treating pieces as interchangeable.
5. For an animation, run `prepare_animation_contract.py GROUP`. Generate and
   approve a single master frame, then use a masked edit for every later frame.
   `compose_animation_frame.py` copies the master into every source-static
   region byte-for-byte. Only the source-derived motion/illumination region can
   vary. `verify_animation_consistency.py` proves this before review.
6. Review a contact sheet or preview video, then perform the existing ratio,
   lifecycle, complete-group, and in-game tests before an explicit approval
   changes the integration ledger.

## Animation rule

Never ask a generator to make an independent still for each animation frame.
It cannot preserve a set, face, tent, wall, or background exactly. The master
HD image is the static plate. Source-frame differences define the edit region;
an explicitly reviewed illumination region may be included when the original
lighting changes. Everything outside that region is composited from the master
without modification. Repeated original frames must produce identical output
hashes.

## Commands

```bash
cd coab-uprez-full-auto/image-uprez-pipeline
python3 nextgen/lock_existing_hd_assets.py
python3 nextgen/lock_existing_hd_assets.py --verify
python3 nextgen/build_generation_jobs.py
python3 nextgen/prepare_animation_contract.py PIC5.DAX:054
python3 nextgen/verify_animation_consistency.py work/PIC5.DAX_054/frames \\
  --mask work/PIC5.DAX_054/motion-or-illumination-mask-source-size.png \\
  --contract work/PIC5.DAX_054/animation-contract.json
```

The job queue is a handoff to an image-edit provider; it is not authorization
to generate or install artwork automatically.
