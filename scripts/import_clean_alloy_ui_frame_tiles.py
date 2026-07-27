#!/usr/bin/env python3
"""Import the faithful clean-alloy UI-frame delivery and rebuild layouts.

The supplied art uses transparency for every black source pixel. In the live
game those black pixels are the opaque backing inside an occupied 8x8 frame
cell; leaving them transparent can expose the low-resolution framebuffer and
text below the HD overlay. This importer preserves the supplied alloy pixels,
restores opaque black backing, and keeps only original magenta-key pixels
transparent.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHEET = (
    ROOT
    / "original assets"
    / "extracted-assets"
    / "8X8D1_block_202_interface_tiles.png"
)
TILE_OUTPUT = ROOT / "HDAssets" / "UI_FRAME" / "tiles"
LAYOUT_BUILDER = ROOT / "scripts" / "build_hd_ui_frame_assets.py"
MAGENTA_KEY = (255, 82, 255)


def expected_name(source_index: int) -> str:
    return "UI_FRAME_symbol_{0:03X}_tile_{1:03d}.png".format(
        0x100 + source_index, source_index
    )


def source_tile(sheet: Image.Image, source_index: int) -> Image.Image:
    x = (source_index % 8) * 8
    y = (source_index // 8) * 8
    return sheet.crop((x, y, x + 8, y + 8)).convert("RGB")


def import_tile(delivery: Image.Image, original: Image.Image) -> Image.Image:
    rgba = delivery.convert("RGBA")
    if rgba.size != (64, 64):
        raise ValueError("delivery tile is not 64x64")

    output = rgba.copy()
    pixels = output.load()
    original_pixels = original.load()
    for source_y in range(8):
        for source_x in range(8):
            source_color = original_pixels[source_x, source_y]
            for y in range(source_y * 8, (source_y + 1) * 8):
                for x in range(source_x * 8, (source_x + 1) * 8):
                    if source_color == MAGENTA_KEY:
                        pixels[x, y] = (0, 0, 0, 0)
                    elif source_color == (0, 0, 0):
                        pixels[x, y] = (0, 0, 0, 255)
                    else:
                        red, green, blue, _alpha = pixels[x, y]
                        pixels[x, y] = (red, green, blue, 255)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "delivery",
        type=Path,
        help="directory containing the 20 FINAL_64x64_RGBA PNG files",
    )
    args = parser.parse_args()

    delivery = args.delivery.resolve()
    if not delivery.is_dir():
        raise SystemExit("delivery directory not found: {0}".format(delivery))

    sheet = Image.open(SOURCE_SHEET).convert("RGB")
    if sheet.size != (64, 40):
        raise SystemExit("unexpected authoritative source-sheet dimensions")

    expected = {expected_name(index) for index in range(20, 40)}
    actual = {path.name for path in delivery.glob("*.png")}
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected:
        raise SystemExit(
            "delivery filename mismatch; missing={0}, unexpected={1}".format(
                missing, unexpected
            )
        )

    TILE_OUTPUT.mkdir(parents=True, exist_ok=True)
    for source_index in range(20, 40):
        name = expected_name(source_index)
        supplied = Image.open(delivery / name).convert("RGBA")
        imported = import_tile(supplied, source_tile(sheet, source_index))
        imported.save(TILE_OUTPUT / name, optimize=True)

    subprocess.run([sys.executable, str(LAYOUT_BUILDER)], check=True)
    print("imported 20 clean-alloy UI-frame tiles and rebuilt 7 layouts")


if __name__ == "__main__":
    main()
