#!/usr/bin/env python3
"""Hard-composite a masked animation edit over an immutable HD master."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("master", type=Path, help="approved HD anchor frame")
    parser.add_argument("edit", type=Path, help="model edit for one later source frame")
    parser.add_argument("mask", type=Path, help="binary source motion/illumination mask")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    master = Image.open(args.master).convert("RGBA")
    edit = Image.open(args.edit).convert("RGBA")
    source_mask = Image.open(args.mask).convert("L")
    if edit.size != master.size:
        raise SystemExit(f"edit size {edit.size} does not match master {master.size}")
    mask = source_mask.resize(master.size, Image.Resampling.NEAREST)
    # Image.composite copies master exactly anywhere mask == 0.
    frame = Image.composite(edit, master, mask)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame.save(args.output)
    print(f"wrote {args.output}; frozen regions are copied exactly from {args.master}")


if __name__ == "__main__":
    main()
