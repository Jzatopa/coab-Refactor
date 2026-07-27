# Razor-sharp in-game font pixel diagnosis — July 27, 2026

## What was actually causing the blur

The faithful active atlas is not blurry: it is a binary-alpha 1024×1024 bitmap containing only fully transparent and fully opaque glyph pixels. The softness was introduced during runtime presentation.

The first implementation drew each 128×128 atlas cell into a smaller destination rectangle through Mono/libgdiplus `Graphics.DrawImage`. A lossless 2560×1600 screenshot showed 186 green shades in the dialogue region. Of 158,786 green-tinted glyph pixels, 23,828 (15.006%) were partial-color edge pixels rather than full EGA green. At a typical vertical stroke, the captured output transitioned from black through a dim green fringe before reaching `(82,255,82)`.

Changing `Graphics.InterpolationMode` from high-quality bicubic to nearest-neighbor did not solve it: before/after lossless screenshots were byte-identical. On this Mono/libgdiplus path, the scaled alpha bitmap was still filtered despite the requested interpolation mode.

## Correct fix

`Main/PixelDisplay.cs` now avoids scaled `DrawImage` for text entirely:

1. Determine the exact integer destination width and height for each original 8×8 logical cell.
2. Manually sample the binary atlas into a final-size RGBA bitmap with integer nearest-neighbor coordinates.
3. Cache by glyph, EGA color, width, and height.
4. Copy the completed bitmap with `DrawImageUnscaled`, so libgdiplus cannot synthesize fringe pixels.

The lifecycle remains unchanged: this renderer is enabled only after gameplay begins. Opening title artwork, credits, Play/Demo, and copy-protection typography remain untouched.

## Measured result

- Before: 186 green shades; 23,828 partial edge pixels; 15.006% partial.
- After: 3 green-like values in the whole sampled panel; 2 incidental partial pixels; 0.001% partial.
- Full EGA-green pixels increased from 134,958 to 148,988.
- The live game remained running through the 2560×1600 capture.
- Visual review found hard binary glyph edges with no clipping, overlap, missing strokes, stale text, or UI corruption.
- DeepSeek sidecar review confirmed the measured correction and found no concrete risk or blocker.

## Evidence

- `gameplay-lossless.png`: lossless filtered baseline.
- `gameplay-software-raster.png`: lossless corrected runtime.
- `before-after-pixel-zoom.png`: nearest-enlarged comparison of the same screen region.
- `glyph-edge-6x-pixel-grid.png`: six-times enlarged baseline with original-pixel grid.
- `PIXEL_ANALYSIS.txt`: measured color counts.
