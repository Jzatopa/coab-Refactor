#!/usr/bin/env python3
"""Prove static regions stayed unchanged across a prepared HD animation."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frames", type=Path, help="directory containing frame_000.png, frame_001.png, ...")
    parser.add_argument("--mask", type=Path, required=True, help="source-sized motion/illumination mask")
    parser.add_argument("--contract", type=Path, help="also require duplicate source frames to have identical output hashes")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    paths = sorted(args.frames.glob("frame_*.png"))
    if len(paths) < 2:
        raise SystemExit("need at least two frame_XXX.png files")
    frames = [Image.open(path).convert("RGBA") for path in paths]
    if len({frame.size for frame in frames}) != 1:
        raise SystemExit("HD animation frame dimensions differ")
    mask = Image.open(args.mask).convert("L").resize(frames[0].size, Image.Resampling.NEAREST)
    frozen = mask.point(lambda value: 255 if value == 0 else 0)
    master = frames[0]
    violations = []
    for path, frame in zip(paths[1:], frames[1:]):
        difference = ImageChops.difference(master.convert("RGB"), frame.convert("RGB"))
        outside = Image.composite(difference, Image.new("RGB", master.size), frozen)
        if outside.getbbox() is not None:
            violations.append(path.name)
    hashes = {path.name: digest(path) for path in paths}
    duplicate_violations = []
    frame_set_violations = []
    if args.contract:
        contract = json.loads(args.contract.read_text())
        expected = {f"frame_{int(item['frame']):03d}.png" for item in contract["frames"]}
        actual = set(hashes)
        if expected != actual:
            missing = sorted(expected - actual)
            unexpected = sorted(actual - expected)
            if missing:
                frame_set_violations.append("missing " + ", ".join(missing))
            if unexpected:
                frame_set_violations.append("unexpected " + ", ".join(unexpected))
        for source_frames in contract.get("identical_source_frame_sets", []):
            output_names = [f"frame_{int(frame):03d}.png" for frame in source_frames]
            values = {hashes.get(name) for name in output_names}
            if None in values:
                duplicate_violations.append("missing " + ", ".join(output_names))
            elif len(values) != 1:
                duplicate_violations.append(", ".join(output_names))
    payload = {
        "frame_count": len(paths),
        "dimensions": list(master.size),
        "static_region_exact": not violations,
        "violating_frames": violations,
        "duplicate_source_frames_exact": not duplicate_violations,
        "duplicate_source_violations": duplicate_violations,
        "frame_set_complete": not frame_set_violations,
        "frame_set_violations": frame_set_violations,
        "sha256": hashes,
    }
    output = args.output or args.frames / "temporal-verification.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    failures = []
    if violations:
        failures.append(f"static-region violations: {', '.join(violations)}")
    if duplicate_violations:
        failures.append(f"duplicate-source violations: {'; '.join(duplicate_violations)}")
    if frame_set_violations:
        failures.append(f"frame-set violations: {'; '.join(frame_set_violations)}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: {len(paths)} frames retain every frozen pixel exactly; report={output}")


if __name__ == "__main__":
    main()
