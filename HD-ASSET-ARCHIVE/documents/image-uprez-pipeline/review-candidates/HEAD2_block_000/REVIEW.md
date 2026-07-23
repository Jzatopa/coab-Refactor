# HEAD2 block 000 — Full-auto review

Original: `../../png/HEAD2/HEAD2_block_000_frame_000.png`  
Matching body: `../../png/BODY2/BODY2_block_000_frame_000.png`  
Required ratio: **11:5**; game placement draws HEAD2 at y=0 and BODY2 at y=40, producing an 88×88 combined portrait.

## Candidate A — rejected

Broad style and color family are plausible, but strict identity/crop fidelity fails: the face became older and wider, facial hair became fuller and gray, the dark-blue hair/head-covering silhouette became oversized and rounded, and the realistic neck is too long for the exact BODY2 seam. It is retained for the maintainer's QC and is not staged.

## Corrected second-pass edit

Candidate B must edit candidate A rather than regenerate the scene. Keep its realism and lighting, but restore the original's younger narrow face, dark non-gray moustache plus small pointed goatee, smaller angular dark hair/head-covering with restrained blue highlights, tighter head scale, and a short centered lower neck ending at the 11:5 panel boundary. Preserve frontal pose, medium-brown skin, pure black background and zero shoulders/armor.

## Candidate B — game-layout test

Candidate B was generated as a localized second-pass edit using the enlarged original HEAD2, original BODY2 and logo-free Title Block 2 human reference. It is substantially closer in age, face width, dark facial hair and head-covering silhouette. The exact game code draws HEAD2 at `(rowY,colX)` and BODY2 at `(rowY+5,colX)`, so the 88×40 head panel stacks directly above the 88×48 body panel at logical y=40 with no overlap. The resulting HD test composite exposes a remaining neck/collar gap, a slightly small/high head, and cooler/darker head lighting than the current unapproved BODY2 candidate. It is retained for the maintainer's QC; neither component is approved from this composite alone.
