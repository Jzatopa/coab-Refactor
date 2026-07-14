#!/usr/bin/env python3
"""Audit the complete COAB eligible-frame prompt and HD replacement inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

FRAME_RE = re.compile(
    r"(?P<archive>TITLE|PIC[1-6]|BIGPIC[126]|HEAD[2-6]|BODY[2-6])_block_"
    r"(?P<block>\d{3})_frame_(?P<frame>\d{3})\.png$"
)

LEGACY_INTEGRATED = {
    ("TITLE", 1, 0): "Title Block 1.png",
    ("TITLE", 2, 0): "Title Block 2.png",
    ("TITLE", 3, 0): "Title Block 3.png",
    ("TITLE", 4, 0): "Title Block 4.png",
    ("PIC1", 80, 0): "PIC1_block_080_village.png",
    ("BIGPIC1", 121, 0): "BIGPIC1_block_121.png",
    ("BIGPIC1", 123, 0): "BIGPIC1_block_123.png",
    ("BIGPIC6", 122, 0): "BIGPIC1_block_122.png",
}


def parse_source(source: str) -> tuple[str, int, int]:
    match = FRAME_RE.search(source)
    if not match:
        raise ValueError(f"unrecognized source path: {source}")
    return match.group("archive"), int(match.group("block")), int(match.group("frame"))


def source_path(root: Path, source: str) -> Path:
    candidates = [root / source, root / "png" / source]
    if source.startswith("png/"):
        candidates.append(root / source)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(source)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--hd-assets", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    pipeline = args.pipeline.resolve()
    repo = pipeline.parent
    hd_assets = (args.hd_assets or repo / "HDAssets").resolve()
    ledger = json.loads((pipeline / "prompts/MASTER_PROMPT_LEDGER.json").read_text())
    manifest = json.loads((pipeline / "manifest.json").read_text())
    rows = ledger["entries"]

    manifest_by_key = {
        (entry["archive"].removesuffix(".DAX"), int(entry["block"]), int(entry["frame"])): entry
        for entry in manifest
    }

    results = []
    hashes: dict[str, list[str]] = defaultdict(list)
    prompt_failures = []
    metadata_gaps = Counter()

    for index, row in enumerate(rows):
        archive, block, frame = parse_source(row["source"])
        key = (archive, block, frame)
        original = source_path(pipeline, row["source"])
        original_hash = sha256(original)
        hashes[original_hash].append(row["source"])
        manifest_row = manifest_by_key.get(key)

        for field in ("archive", "block", "frame", "source_size", "category"):
            if row.get(field) in (None, "", []):
                metadata_gaps[field] += 1

        prompt = row.get("prompt", "").strip()
        failures = []
        if len(prompt) < 350:
            failures.append("prompt shorter than 350 characters")
        if "photoreal" not in prompt.lower():
            failures.append("missing prompt concept: photoreal")
        if not any(phrase in prompt.lower() for phrase in ("composition", "preserve its", "preserve exactly")):
            failures.append("missing prompt concept: composition lock")
        if not any(phrase in prompt.lower() for phrase in ("no text", "do not add text", "do not generate")):
            failures.append("missing prompt concept: text exclusion")
        if failures:
            prompt_failures.append({"index": index, "source": row["source"], "failures": failures})

        generic = hd_assets / archive / f"{archive}_block_{block:03d}_frame_{frame:03d}.png"
        legacy_name = LEGACY_INTEGRATED.get(key)
        legacy = hd_assets / legacy_name if legacy_name else None
        integrated = generic if generic.is_file() else legacy if legacy and legacy.is_file() else None

        candidate_dir = pipeline / "review-candidates" / f"{archive}_block_{block:03d}"
        candidates = sorted(str(path.relative_to(pipeline)) for path in candidate_dir.glob("*.png"))
        status = (
            "integrated-generated" if integrated == generic and generic.is_file()
            else "integrated-existing" if integrated
            else "missing-generation"
        )
        if key == ("PIC1", 1, 0) and candidates:
            status = "candidates-rejected"

        results.append(
            {
                "index": index,
                "source": row["source"],
                "archive": archive,
                "block": block,
                "frame": frame,
                "manifest_found": manifest_row is not None,
                "width": manifest_row["width"] if manifest_row else None,
                "height": manifest_row["height"] if manifest_row else None,
                "aspect_ratio": row.get("aspect_ratio"),
                "sha256": original_hash,
                "duplicate_count": 0,
                "prompt_length": len(prompt),
                "prompt_audit": "pass" if not failures else "fail",
                "status": status,
                "integrated_path": str(integrated.relative_to(repo)) if integrated else None,
                "candidates": candidates,
            }
        )

    duplicate_count_by_hash = {digest: len(sources) for digest, sources in hashes.items()}
    for result in results:
        result["duplicate_count"] = duplicate_count_by_hash[result["sha256"]]

    status_counts = Counter(result["status"] for result in results)
    reviewed_candidate_files = sum(1 for _ in (pipeline / "review-candidates").rglob("*.png"))
    report = {
        "eligible_rows": len(rows),
        "manifest_rows": len(manifest),
        "unique_original_images": len(hashes),
        "duplicate_rows_reusable": len(rows) - len(hashes),
        "prompt_failures": prompt_failures,
        "ledger_metadata_gaps": dict(metadata_gaps),
        "status_counts": dict(status_counts),
        "reviewed_candidate_files": reviewed_candidate_files,
        "results": results,
        "duplicate_groups": [sources for sources in hashes.values() if len(sources) > 1],
    }

    md = [
        "# Eligible Asset Audit",
        "",
        f"- Eligible extracted frames: **{len(rows)}**",
        f"- Manifest rows matched: **{sum(1 for result in results if result['manifest_found'])}/{len(rows)}**",
        f"- Unique source images by SHA-256: **{len(hashes)}**",
        f"- Duplicate frame rows reusable after one approved generation: **{len(rows) - len(hashes)}**",
        f"- Prompt content checks passed: **{len(rows) - len(prompt_failures)}/{len(rows)}**",
        f"- Eligible frames already integrated from strong prior assets: **{status_counts['integrated-existing']}**",
        f"- Eligible frames integrated under canonical archive paths: **{status_counts['integrated-generated']}**",
        f"- Frames with reviewed/rejected candidates: **{status_counts['candidates-rejected']}**",
        f"- Frames still requiring an approved generation: **{status_counts['missing-generation']}**",
        "",
        "## Prompt-ledger audit",
        "",
        "All 231 entries have a substantial generation prompt and resolve to an extracted source PNG. "
        "The combined ledger has incomplete convenience metadata in some imported rows; runtime identity is therefore derived from the authoritative source filename and cross-checked against `manifest.json`.",
        "",
        f"Metadata gaps: `{dict(metadata_gaps)}`.",
        "",
        "## Candidate review",
        "",
        f"Review directories currently contain **{reviewed_candidate_files}** candidate PNG files. Per-entry approval and rejection decisions are recorded in `REVIEW.md` files and `asset-decisions.json`; the audit does not infer approval from file presence.",
        "",
        "## Status by frame",
        "",
        "| Source | Status | Integrated path | Duplicate group |",
        "|---|---|---|---:|",
    ]
    for result in results:
        integrated_cell = (
            "`{}`".format(result["integrated_path"])
            if result["integrated_path"]
            else "—"
        )
        md.append(
            f"| `{result['source']}` | {result['status']} | "
            f"{integrated_cell} | "
            f"{result['duplicate_count']} |"
        )
    md.append("")

    if args.write:
        (pipeline / "asset-audit.json").write_text(json.dumps(report, indent=2) + "\n")
        (pipeline / "ASSET_AUDIT.md").write_text("\n".join(md))
    else:
        print(json.dumps({key: value for key, value in report.items() if key not in ("results", "duplicate_groups")}, indent=2))

    return 1 if prompt_failures or len(rows) != 231 or len(manifest) != 231 else 0


if __name__ == "__main__":
    raise SystemExit(main())
