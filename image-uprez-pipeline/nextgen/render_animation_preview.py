#!/usr/bin/env python3
"""Render a review MP4 from composited HD frames and source frame delays."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def duration(delay: int | None, fallback_fps: float) -> float:
    # DAX values are retained verbatim in the contract. A zero/unknown delay
    # uses a conservative preview cadence; callers may override it.
    return (delay / 18.2) if delay and delay > 0 else (1.0 / fallback_fps)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    parser.add_argument("frames", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--fallback-fps", type=float, default=6.0)
    args = parser.parse_args()
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required to render the preview")
    contract = json.loads(args.contract.read_text())
    source_frames = contract["frames"]
    paths = [args.frames / f"frame_{item['frame']:03d}.png" for item in source_frames]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise SystemExit("missing output frames: " + ", ".join(missing))
    with tempfile.TemporaryDirectory(prefix="coab-animation-") as temporary:
        concat = Path(temporary) / "frames.txt"
        lines = []
        for path, source in zip(paths, source_frames):
            lines.append(f"file '{path.resolve()}'")
            lines.append(f"duration {duration(source.get('delay'), args.fallback_fps):.6f}")
        lines.append(f"file '{paths[-1].resolve()}'")
        concat.write_text("\n".join(lines) + "\n")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
            "-vf", "format=yuv420p", "-movflags", "+faststart", str(args.output),
        ], check=True)
    print(f"wrote preview video {args.output}")


if __name__ == "__main__":
    main()
