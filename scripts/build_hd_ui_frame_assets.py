#!/usr/bin/env python3
"""Compose transparent HD UI-frame overlays from the original tile layouts."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TILES = ROOT / "HDAssets" / "UI_FRAME" / "tiles"
OUTPUT = ROOT / "HDAssets" / "UI_FRAME" / "layouts"
SCALE = 64

OUTER_BOTTOM = [1,8,6,1,1,1,1,1,1,1,1,4,1,1,1,1,1,6,8,1,1,1,4,1,1,1,1,1,1,6,1,1,1,1,1,1,1,1,4,3]
TOP = [0,6,1,1,1,1,1,1,6,1,1,1,1,4,1,1,1,6,1,1,1,1,1,1,1,8,1,1,1,1,1,1,1,4,1,1,1,6,1,2]
DIVIDER = [0,8,1,1,1,1,1,1,1,1,1,6,1,1,1,8,4,1,1,1,6,1,1,1,1,1,1,1,1,1,4,1,6,1,1,1,1,1,8,2]
LEFT = [0,2,9,5,2,2,2,2,2,2,5,7,2,2,2,2,2,9,7,2,2,2,7,1]
RIGHT = [2,2,9,7,2,2,2,5,2,2,2,2,2,2,2,2,2,7,2,2,2,2,5,2]
INNER_TOP = [4,3,0,6,1,1,1,1,8,1,1,4,1,1,2,1,4]
INNER_RIGHT = [0,7,5,2,2,2,2,2,2,2,2,2,2,5,2,9,4]
INNER_BOTTOM = [1,2,1,4,1,1,1,1,1,1,8,4,1,1,3]
INNER_LEFT = [5,2,0,2,7,2,2,2,2,5,2,2,2,2,1]
INNER_RIGHT2 = [2,1,2,5,9,2,2,2,7,5,2,2,2,2,3]
COMBAT_LEFT = [0,2,9,5,2,2,2,2,2,2,5,7,2,2,2,2,2,9,7,2,2,2,1]
COMBAT_MIDDLE = [0,7,5,2,2,2,2,2,2,2,2,2,7,5,2,2,2,2,2,2,5,2,4]
COMBAT_RIGHT = [2,2,9,7,2,2,2,5,2,2,2,2,2,2,2,2,2,7,2,2,2,2,2]

def load_tiles():
    tiles = {}
    for source_index in range(20, 40):
        symbol = 0x100 + source_index
        path = TILES / ("UI_FRAME_symbol_{0:03X}_tile_{1:03d}.png".format(symbol, source_index))
        if not path.is_file():
            raise SystemExit("missing UI-frame tile: {0}".format(path))
        image = Image.open(path).convert("RGBA")
        if image.size != (SCALE, SCALE):
            raise SystemExit("expected 64x64 tile: {0}".format(path))
        tiles[symbol] = image
    return tiles

def outer(grid):
    for x, value in enumerate(TOP): grid[x, 0] = 0x11e + value
    for y in range(0x17):
        grid[0, y] = 0x11e + LEFT[y]
        grid[0x27, y] = 0x11e + RIGHT[y]
    for x, value in enumerate(OUTER_BOTTOM): grid[x, 0x17] = 0x11e + value

def compose(name, draw, tiles):
    grid = {}
    draw(grid)
    canvas = Image.new("RGBA", (40 * SCALE, 25 * SCALE), (0, 0, 0, 0))
    for (x, y), symbol in grid.items():
        canvas.alpha_composite(tiles[symbol], (x * SCALE, y * SCALE))
    canvas.save(OUTPUT / name)

def layout_outer(grid): outer(grid)
def layout_menu(grid):
    outer(grid)
    for x, value in enumerate(DIVIDER): grid[x, 3] = grid[x, 8] = 0x11e + value
def layout_inset(grid):
    outer(grid)
    for x, value in enumerate(DIVIDER): grid[x, 0x10] = 0x11e + value
    for y, value in enumerate(INNER_RIGHT): grid[0x10, y] = 0x11e + value
    for x in range(2, 15):
        grid[x, 2] = 0x114 + INNER_TOP[x]
        grid[x, 14] = 0x114 + INNER_BOTTOM[x]
    for y in range(2, 15):
        grid[2, y] = 0x114 + INNER_LEFT[y]
        grid[14, y] = 0x114 + INNER_RIGHT2[y]
def layout_wilderness(grid):
    outer(grid)
    for x, value in enumerate(DIVIDER): grid[x, 0x10] = 0x11e + value
def layout_short(grid):
    for x, value in enumerate(TOP): grid[x, 0] = 0x11e + value
    for y in range(0x18):
        grid[0, y] = 0x11e + LEFT[y]
        grid[0x27, y] = 0x11e + RIGHT[y]
    for x, value in enumerate(OUTER_BOTTOM): grid[x, 0x17] = 0x11e + value
    for x, value in enumerate(DIVIDER): grid[x, 0x10] = 0x11e + value
def layout_combat(grid):
    for x, value in enumerate(TOP): grid[x, 0] = 0x11e + value
    for y in range(0x17):
        grid[0, y] = 0x11e + COMBAT_LEFT[y]
        grid[0x16, y] = 0x11e + COMBAT_MIDDLE[y]
        grid[0x27, y] = 0x11e + COMBAT_RIGHT[y]
    for x, value in enumerate(OUTER_BOTTOM): grid[x, 0x16] = 0x11e + value
def layout_status(grid):
    outer(grid)
    for x, value in enumerate(DIVIDER): grid[x, 2] = 0x11e + value

def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    tiles = load_tiles()
    layouts = [
        ("UI_FRAME_layout_01_outer_overlay.png", layout_outer),
        ("UI_FRAME_layout_02_menu_dividers_overlay.png", layout_menu),
        ("UI_FRAME_layout_03_inset_panel_overlay.png", layout_inset),
        ("UI_FRAME_layout_04_wilderness_overlay.png", layout_wilderness),
        ("UI_FRAME_layout_05_short_overlay.png", layout_short),
        ("UI_FRAME_layout_06_combat_overlay.png", layout_combat),
        ("UI_FRAME_layout_07_status_overlay.png", layout_status),
    ]
    for name, draw in layouts: compose(name, draw, tiles)
    print("built {0} transparent UI-frame layouts from {1} tiles".format(len(layouts), len(tiles)))

if __name__ == "__main__": main()
