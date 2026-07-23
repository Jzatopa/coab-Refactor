#!/usr/bin/env python3
"""Build source-locked jobs without touching protected or runtime art."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PIPELINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE))

from integration_common import build_rows, resolve_candidate  # noqa: E402

NEXTGEN = Path(__file__).resolve().parent
LOCK_PATH = NEXTGEN / "protected-assets.json"
DEFAULT_OUTPUT = NEXTGEN / "generation-jobs.json"


def load_protected() -> set[str]:
    if not LOCK_PATH.is_file():
        raise SystemExit("missing protected-assets.json; run lock_existing_hd_assets.py first")
    return set(json.loads(LOCK_PATH.read_text())["protected_identities"])


def prompt_for_still(row: dict) -> str:
    return (
        "Use the enlarged source image as the authoritative composition reference. "
        "Create a high-resolution grounded live-action fantasy rendering without "
        "moving or adding major source geometry. Preserve the exact aspect ratio, "
        "crop, large silhouettes, visible subject count, overlaps, and intentional "
        "empty/black regions. If a low-resolution shape is ambiguous, preserve its "
        "geometry and color role; do not invent a confident object identity. "
        "Use any finish reference for materials, lighting quality, and anatomy only, "
        "never for composition. Return one clean image with no text, border, or UI."
    )


def make_still_job(row: dict) -> dict:
    return {
        "kind": "still_source_locked_edit",
        "identity": row["identity"],
        "source": {
            "png": row["source_png"], "sha256": row["source_sha256"],
            "size": [row["width"], row["height"]], "aspect_ratio": row["aspect_ratio"],
        },
        "lifecycle": row["lifecycle"],
        "prior_candidate": row["candidate"],
        "prior_status": row["review_status"],
        "instruction": prompt_for_still(row),
        "hard_review": [
            "exact aspect ratio without stretching", "crop and negative space",
            "major silhouette/count/overlap", "no semantic invention", "no text or UI",
        ],
        "finish_review": [
            "credible materials and anatomy", "source-motivated lighting",
            "category-appropriate realism rather than a universal style reference",
        ],
    }


def make_animation_job(group: list[dict]) -> dict:
    group.sort(key=lambda row: row["frame"])
    first = group[0]
    return {
        "kind": "masked_animation_master_and_edits",
        "animation_group": first["animation_group"],
        "lifecycle": first["lifecycle"],
        "frames": [{
            "identity": row["identity"], "frame": row["frame"], "delay": row["delay"],
            "png": row["source_png"], "sha256": row["source_sha256"],
        } for row in group],
        "prior_statuses": sorted({row["review_status"] for row in group}),
        "instruction": (
            "Do not generate this sequence as independent still images. First make one "
            "approved HD master from frame 000. Then edit that master for each later "
            "source frame only inside the supplied motion/illumination mask. Composite "
            "the result with compose_animation_frame.py so every static pixel is copied "
            "from the master exactly. Preserve source frame order and delay."
        ),
        "hard_review": [
            "complete group only", "same dimensions and aspect ratio", "static pixels identical",
            "repeated source frames have identical output hashes", "only masked motion/lighting changes",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    protected = load_protected()
    queued = [row for row in build_rows() if row["identity"] not in protected]
    groups: dict[str, list[dict]] = defaultdict(list)
    jobs = []
    for row in queued:
        if row["animated"]:
            groups[row["animation_group"]].append(row)
        else:
            jobs.append(make_still_job(row))
    jobs.extend(make_animation_job(group) for _, group in sorted(groups.items()))
    jobs.sort(key=lambda job: (job.get("animation_group", ""), job.get("identity", "")))
    payload = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "policy": "Protected identities are excluded; jobs are review handoffs, not automatic installs.",
        "protected_identity_count": len(protected),
        "queued_source_frames": len(queued),
        "jobs": jobs,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    animations = sum(job["kind"].startswith("masked_animation") for job in jobs)
    print(f"queued {len(queued)} source frames as {len(jobs)} jobs ({animations} animation groups); protected={len(protected)}")


if __name__ == "__main__":
    main()
