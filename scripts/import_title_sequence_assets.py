#!/usr/bin/env python3
"""Import the supplied COAB opening artwork and rebuild title logo overlays.

TITLE blocks 1 and 2 are full-screen 320x200 replacements rendered at 8x.
The original engine keeps block 2 visible while blocks 3 and 4 replace lower
logical rectangles.  Blocks 3 and 4 are therefore emitted as transparent
logo-only RGBA overlays.  Their placement/topology comes from the original
TITLE.DAX pixels; their high-resolution logo pixels come from the supplied
Title Block 3/4 artwork.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageOps

SCALE = 8
FULL_SIZE = (320 * SCALE, 200 * SCALE)
EXPECTED_SOURCES = {
    1: "4a7410c1e7c5eb32cce0884ceb020488a2f9e70e651ab15abdf84f61be68b8db",
    2: "115cdbd986d32c4c5beb81c3fd27787ea858c4af3d9741c1721d72297dc8deef",
    3: "f9be42f35468a1c9d4dfb9989afa98e46ec73354e561d3fd53bbeb7371f9d8bf",
    4: "f3a449bce5e293e069c8de81aabbdbe247d03332627ccb61e497af6763574f18",
}
OVERLAYS = {
    3: (48, 88, 240, 112),
    4: (0, 88, 320, 112),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_source(path: Path, block: int) -> None:
    if not path.is_file():
        raise SystemExit(f"Missing supplied Title Block {block}: {path}")
    actual = sha256(path)
    expected = EXPECTED_SOURCES[block]
    if actual != expected:
        raise SystemExit(
            f"Title Block {block} SHA-256 mismatch: expected {expected}, got {actual}: {path}"
        )


def fit_full_screen(source: Path, background: tuple[int, int, int]) -> Image.Image:
    image = Image.open(source).convert("RGB")
    return ImageOps.pad(
        image,
        FULL_SIZE,
        method=Image.Resampling.LANCZOS,
        color=background,
        centering=(0.5, 0.5),
    )


def sharpen_lettering(image: Image.Image, *, percent: int) -> Image.Image:
    """Restore edge contrast lost when supplied raster lettering is enlarged."""
    return image.filter(
        ImageFilter.UnsharpMask(radius=1.0, percent=percent, threshold=2)
    )


def original_change_mask(repo: Path, block: int) -> Image.Image:
    x, y, width, height = OVERLAYS[block]
    original_dir = repo / "original assets" / "TITLE"
    base = Image.open(original_dir / "TITLE_block_002_frame_000.png").convert("RGB")
    base = base.crop((x, y, x + width, y + height))
    overlay = Image.open(original_dir / f"TITLE_block_00{block}_frame_000.png").convert("RGB")
    return ImageChops.difference(overlay, base).convert("L").point(
        lambda value: 255 if value else 0
    )


def logo_overlay(repo: Path, block: int, donor_source: Path) -> Image.Image:
    x, y, width, height = OVERLAYS[block]
    donor_full = fit_full_screen(donor_source, (0, 0, 0))
    donor = donor_full.crop(
        (x * SCALE, y * SCALE, (x + width) * SCALE, (y + height) * SCALE)
    ).convert("RGBA")

    # The original per-pixel difference supplies an evidence-based placement
    # gate. Block 3 needs a wider allowance because the remastered C extends
    # beyond the low-resolution glyph silhouette.
    gate_size = 135 if block == 3 else 55
    gate = original_change_mask(repo, block).resize(
        donor.size, Image.Resampling.NEAREST
    ).filter(ImageFilter.MaxFilter(gate_size))

    rgb = donor.convert("RGB")
    pixels = rgb.load()
    gate_pixels = gate.load()
    seed = Image.new("L", donor.size, 0)
    seed_pixels = seed.load()

    for py in range(donor.height):
        for px in range(donor.width):
            if gate_pixels[px, py] == 0:
                continue
            red, green, blue = pixels[px, py]
            warm_logo = (
                (red > blue + 10 and red + green > 100)
                or (red > 145 and green > 125 and blue > 105 and red >= blue)
            )
            stone_plaque = (
                block == 4
                and 53 <= py <= 547
                and 227 <= px <= 2093
                and red > 45
                and green > 38
                and red >= blue - 2
                and green >= blue - 12
            )
            if warm_logo or stone_plaque:
                seed_pixels[px, py] = 255

    alpha = seed.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(0.45))
    alpha = ImageChops.multiply(alpha, gate)
    donor = sharpen_lettering(donor, percent=155)
    donor.putalpha(alpha)
    return donor


def destinations(repo: Path, block: int) -> list[Path]:
    filename = f"TITLE_block_00{block}_frame_000.png"
    return [
        repo / "image-uprez-pipeline" / "approved" / "TITLE" / filename,
        repo / "HD-ASSET-ARCHIVE" / "images" / "approved" / "TITLE" / filename,
        repo / "HDAssets" / "TITLE" / filename.replace(".png", "_HD.png"),
    ]


def save_all(image: Image.Image, paths: list[Path]) -> None:
    primary = paths[0]
    primary.parent.mkdir(parents=True, exist_ok=True)
    image.save(primary, format="PNG", optimize=True)
    for path in paths[1:]:
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(primary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--block-1", type=Path, default=Path.home() / "Downloads" / "Title Block 1.png")
    parser.add_argument("--block-2", type=Path, default=Path.home() / "Downloads" / "Title Block 2.png")
    parser.add_argument("--block-3", type=Path, default=Path.home() / "Downloads" / "Title Block 3.png")
    parser.add_argument(
        "--block-4",
        type=Path,
        default=Path.home() / "Downloads" / "curseoftheazurebonds" / "HDAssets" / "Title Block 4.png",
    )
    args = parser.parse_args()
    repo = args.repo.resolve()
    sources = {1: args.block_1, 2: args.block_2, 3: args.block_3, 4: args.block_4}
    for block, path in sources.items():
        require_source(path, block)

    block_1 = sharpen_lettering(
        fit_full_screen(sources[1], (1, 9, 114)), percent=125
    )
    block_2 = fit_full_screen(sources[2], (0, 0, 0))
    block_3 = logo_overlay(repo, 3, sources[3])
    block_4 = logo_overlay(repo, 4, sources[4])

    for block, image in {1: block_1, 2: block_2, 3: block_3, 4: block_4}.items():
        save_all(image, destinations(repo, block))
        alpha = image.getchannel("A").getextrema() if image.mode == "RGBA" else None
        print(f"TITLE block {block}: {image.mode} {image.size} alpha={alpha} sha256={sha256(destinations(repo, block)[0])}")


if __name__ == "__main__":
    main()
