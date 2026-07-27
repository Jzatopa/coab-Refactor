#!/usr/bin/env python3
"""Focused contract for the rebuilt HD opening-title sequence."""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "image-uprez-pipeline" / "approved" / "TITLE"
ARCHIVE = ROOT / "HD-ASSET-ARCHIVE" / "images" / "approved" / "TITLE"
RUNTIME = ROOT / "HDAssets" / "TITLE"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_for(base: Path, block: int) -> Path:
    suffix = "_HD" if base == RUNTIME else ""
    return base / f"TITLE_block_00{block}_frame_000{suffix}.png"


def main() -> None:
    expected = {
        1: ("RGB", (2560, 1600)),
        2: ("RGB", (2560, 1600)),
        3: ("RGBA", (1920, 896)),
        4: ("RGBA", (2560, 896)),
    }
    images: dict[int, Image.Image] = {}

    for block, (mode, size) in expected.items():
        paths = [path_for(base, block) for base in (APPROVED, ARCHIVE, RUNTIME)]
        assert all(path.is_file() for path in paths), paths
        assert len({digest(path) for path in paths}) == 1, paths
        image = Image.open(paths[0])
        image.load()
        assert image.mode == mode, (block, image.mode)
        assert image.size == size, (block, image.size)
        images[block] = image

    for block in (3, 4):
        alpha = images[block].getchannel("A")
        assert alpha.getextrema() == (0, 255), (block, alpha.getextrema())

    # The remastered C extends left of the original low-resolution glyph, but
    # must remain fully represented inside block 3's retained rectangle.
    block_3_bbox = images[3].getchannel("A").getbbox()
    assert block_3_bbox is not None and block_3_bbox[0] <= 225, block_3_bbox

    # Block 4 must not retain the previous Curse logo near the heroine's neck.
    block_4_alpha = images[4].getchannel("A")
    assert block_4_alpha.crop((0, 0, block_4_alpha.width, 200)).getbbox() is None
    block_4_bbox = block_4_alpha.getbbox()
    assert block_4_bbox is not None and block_4_bbox[1] >= 200, block_4_bbox

    # Transparent overlay pixels reveal the unchanged block-2 scene rather
    # than a second generated background or a rectangular donor-image patch.
    base = images[2].convert("RGBA")
    for block, (x, y) in {3: (48 * 8, 88 * 8), 4: (0, 88 * 8)}.items():
        overlay = images[block]
        composite = base.copy()
        composite.alpha_composite(overlay, (x, y))
        alpha = overlay.getchannel("A")
        base_crop = base.crop((x, y, x + overlay.width, y + overlay.height))
        composite_crop = composite.crop((x, y, x + overlay.width, y + overlay.height))
        transparent = alpha.point(lambda value: 255 if value == 0 else 0)
        difference = ImageChops.difference(composite_crop, base_crop).convert("RGB")
        transparent_rgb = Image.merge("RGB", (transparent, transparent, transparent))
        assert ImageChops.multiply(difference, transparent_rgb).getbbox() is None, block

    print("HD title sequence contract passed: supplied bases plus transparent logo overlays")


if __name__ == "__main__":
    main()
