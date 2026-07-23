#!/usr/bin/env python3
"""Derive a reviewable frozen/static versus editable animation contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageChops

PIPELINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE))
from integration_common import build_rows  # noqa: E402

NEXTGEN = Path(__file__).resolve().parent


def changed_mask(images: list[Image.Image]) -> Image.Image:
    """White means source evidence permits motion or illumination to change."""
    base = images[0].convert("RGB")
    result = Image.new("L", base.size, 0)
    for image in images[1:]:
        diff = ImageChops.difference(base, image.convert("RGB")).convert("L")
        result = ImageChops.lighter(result, diff.point(lambda value: 255 if value else 0))
    return result


def make_contact_sheet(images: list[Image.Image], scale: int) -> Image.Image:
    width, height = images[0].size
    sheet = Image.new("RGBA", (width * scale * len(images), height * scale), (0, 0, 0, 255))
    for index, image in enumerate(images):
        sheet.alpha_composite(image.convert("RGBA").resize((width * scale, height * scale), Image.Resampling.NEAREST), (index * width * scale, 0))
    return sheet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("group", help="canonical group, e.g. PIC5.DAX:054")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--scale", type=int, default=12)
    args = parser.parse_args()
    group = args.group.upper()
    rows = sorted((row for row in build_rows() if row["animation_group"] == group), key=lambda row: row["frame"])
    if len(rows) < 2:
        raise SystemExit(f"{group} is not a multi-frame animation group")
    images = [Image.open(PIPELINE / row["source_png"]).convert("RGBA") for row in rows]
    if len({image.size for image in images}) != 1:
        raise SystemExit("source animation frames do not have identical dimensions")
    output = args.output or NEXTGEN / "work" / group.replace(":", "_")
    output.mkdir(parents=True, exist_ok=True)
    mask = changed_mask(images)
    static_pixels = sum(pixel == 0 for pixel in mask.getdata())
    total_pixels = mask.width * mask.height
    identical_source_frames: dict[str, list[int]] = defaultdict(list)
    for row, image in zip(rows, images):
        identical_source_frames[hashlib.sha256(image.tobytes()).hexdigest()].append(row["frame"])
    (output / "source-frames.png").unlink(missing_ok=True)
    make_contact_sheet(images, args.scale).save(output / "source-frames.png")
    mask.resize((mask.width * args.scale, mask.height * args.scale), Image.Resampling.NEAREST).save(output / "motion-or-illumination-mask.png")
    # A compositing mask is deliberately binary. Feathering would alter frozen
    # pixels, which defeats the contract. Human QC may expand the white region
    # only where source evidence shows a moving edge or lighting change.
    mask.save(output / "motion-or-illumination-mask-source-size.png")
    payload = {
        "schema_version": 1,
        "animation_group": group,
        "source_size": list(images[0].size),
        "frame_count": len(rows),
        "frames": [{"identity": row["identity"], "frame": row["frame"], "delay": row["delay"], "source": row["source_png"]} for row in rows],
        "identical_source_frame_sets": [
            frame_set for frame_set in identical_source_frames.values() if len(frame_set) > 1
        ],
        "mask_semantics": {
            "black": "frozen static plate: must be byte-identical to the master HD frame",
            "white": "source-derived motion or illumination region: a masked edit may change it",
            "review": "review this mask before generation; expand only with source evidence, never to hide shimmer",
        },
        "static_pixels": static_pixels,
        "editable_pixels": total_pixels - static_pixels,
        "static_percent": round(100 * static_pixels / total_pixels, 2),
    }
    (output / "animation-contract.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(f"prepared {group}: static={payload['static_percent']}% ({static_pixels}/{total_pixels}) -> {output}")


if __name__ == "__main__":
    main()
