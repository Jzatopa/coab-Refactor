#!/usr/bin/env python3
"""Focused contract for the faithful high-resolution in-game font layer."""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "HD-ASSET-ARCHIVE" / "images" / "runtime"
RUNTIME = ROOT / "runtime" / "full-auto" / "data" / "HDAssets"

EXPECTED = {
    "coab-font-atlas.png": "f71d6d5cbfe6041bd83041843ae8b42aec55e65454474eab40c64b749fdfb65d",
    "coab-font-atlas-original-uprez.png": "f71d6d5cbfe6041bd83041843ae8b42aec55e65454474eab40c64b749fdfb65d",
    "coab-font-atlas-quill-brush.png": "9b23c13ee003467fca0c9cee974a50a2fb1f2eb449ece4834abf5b50960ebec3",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for filename, expected_hash in EXPECTED.items():
        archived = ARCHIVE / filename
        staged = RUNTIME / filename
        assert archived.is_file(), archived
        assert staged.is_file(), staged
        assert sha256(archived) == expected_hash, archived
        assert sha256(staged) == expected_hash, staged
        with Image.open(staged) as image:
            assert image.mode == "RGBA", (staged, image.mode)
            assert image.size == (1024, 1024), (staged, image.size)

    # The default atlas must remain the faithful original-topology atlas; the
    # quill/brush alternative is shipped but is not silently made the default.
    assert sha256(RUNTIME / "coab-font-atlas.png") == sha256(
        RUNTIME / "coab-font-atlas-original-uprez.png"
    )
    with Image.open(RUNTIME / "coab-font-atlas.png") as faithful_atlas:
        assert set(faithful_atlas.getchannel("A").getdata()) == {0, 255}

    renderer = (ROOT / "Main" / "PixelDisplay.cs").read_text(encoding="utf-8")
    display = (ROOT / "Classes" / "Display.cs").read_text(encoding="utf-8")
    startup = (ROOT / "engine" / "seg001.cs").read_text(encoding="utf-8")
    text_renderer = renderer.split("static void DrawHighResolutionText", 1)[1].split(
        "protected override void OnPaint", 1
    )[0]
    assert "GetRasterizedGlyph" in renderer
    assert "((gx * 128) / width)" in renderer
    assert "((gy * 128) / height)" in renderer
    assert "DrawImageUnscaled" in text_renderer
    assert "InterpolationMode.HighQualityBicubic" not in text_renderer
    assert "title artwork remains an" in renderer
    assert "public static bool HighResFontActive" in display
    assert "bool highResFont = HighResFontActive;" in display
    assert "Display.HighResFontEnabled = false;" in startup
    assert startup.count("Display.HighResFontEnabled = true;") == 2

    print(
        "HD in-game font contract passed: binary faithful atlas staged with "
        "manual final-size razor-sharp glyph rasterization"
    )


if __name__ == "__main__":
    main()
