#!/usr/bin/env python3
"""Normalize the 231-entry master ledger without rewriting authored prompts."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"
FRAME_RE = re.compile(
    r"(?P<archive>TITLE|PIC[1-6]|BIGPIC[126]|HEAD[2-6]|BODY[2-6])_block_"
    r"(?P<block>\d{3})_frame_(?P<frame>\d{3})\.png$"
)


def key_from_source(source: str) -> tuple[str, int, int]:
    match = FRAME_RE.search(source)
    if not match:
        raise ValueError(source)
    return match.group("archive"), int(match.group("block")), int(match.group("frame"))


def ratio(width: int, height: int) -> str:
    import math

    common = math.gcd(width, height)
    return f"{width // common}:{height // common}"


def main() -> None:
    master_path = PROMPTS / "MASTER_PROMPT_LEDGER.json"
    master = json.loads(master_path.read_text())
    current = {key_from_source(row["source"]): row for row in master["entries"]}

    title_bigpic = json.loads((PROMPTS / "TITLE-BIGPIC-prompts.json").read_text())
    title_rows = {key_from_source(row["source"]): row for row in title_bigpic["images"]}
    manifest = json.loads((ROOT / "manifest.json").read_text())

    normalized = []
    for item in manifest:
        key = (item["archive"].removesuffix(".DAX"), int(item["block"]), int(item["frame"]))
        authored = dict(current[key])
        if key in title_rows:
            source = title_rows[key]
            authored["scene_description"] = source["scene"]
            authored["constraints"] = source["constraints"]
            authored["prompt"] = source["full_prompt"]
            authored["ledger"] = "TITLE-BIGPIC-prompts.json"

        authored.update(
            {
                "source": item["png"],
                "archive": item["archive"],
                "block": int(item["block"]),
                "frame": int(item["frame"]),
                "source_size": [int(item["width"]), int(item["height"])],
                "aspect_ratio": ratio(int(item["width"]), int(item["height"])),
                "category": item["category_guess"],
                "animated": bool(item["animated"]),
                "delay": item["delay"],
                "source_sha256": item["sha256"],
            }
        )
        normalized.append(authored)

    if len(normalized) != 231:
        raise RuntimeError(f"expected 231 rows, got {len(normalized)}")
    if any(not row.get("prompt", "").strip() for row in normalized):
        missing = [row["source"] for row in normalized if not row.get("prompt", "").strip()]
        raise RuntimeError(f"empty prompts after normalization: {missing}")

    output = {
        "count": len(normalized),
        "art_direction": "../ART_DIRECTION.md",
        "quality_reference": "../../HDAssets/PIC1_block_080_village.png",
        "normalization_note": (
            "Metadata is normalized from manifest.json. Authored prompt text is retained from the "
            "component ledgers; TITLE/BIGPIC uses its full_prompt field."
        ),
        "entries": normalized,
    }
    master_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")

    fields = [
        "source",
        "archive",
        "block",
        "frame",
        "source_size",
        "aspect_ratio",
        "category",
        "animated",
        "delay",
        "scene_description",
        "constraints",
        "prompt",
        "ledger",
        "source_sha256",
    ]
    with (PROMPTS / "MASTER_PROMPT_LEDGER.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in normalized:
            csv_row = dict(row)
            csv_row["source_size"] = "x".join(str(value) for value in row["source_size"])
            writer.writerow(csv_row)

    lines = [
        "# Master Prompt Ledger",
        "",
        "**Entries:** 231  ",
        "**Composition authority:** the extracted source PNG listed for each entry  ",
        "**Quality floor:** `HDAssets/PIC1_block_080_village.png`",
        "",
        "Metadata below is normalized from `manifest.json`; prompt prose is preserved from the authored component ledgers.",
        "",
    ]
    for index, row in enumerate(normalized, 1):
        lines.extend(
            [
                f"## {index}. `{row['source']}`",
                "",
                f"- Archive/block/frame: `{row['archive']}` / `{row['block']}` / `{row['frame']}`",
                f"- Source size/ratio: `{row['source_size'][0]}×{row['source_size'][1]}` / `{row['aspect_ratio']}`",
                f"- Category: `{row['category']}`",
                f"- Animated: `{str(row['animated']).lower()}`",
                f"- Authored in: `{row.get('ledger', '')}`",
                "",
                "### Prompt",
                "",
                row["prompt"].strip(),
                "",
            ]
        )
    (PROMPTS / "MASTER_PROMPT_LEDGER.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
