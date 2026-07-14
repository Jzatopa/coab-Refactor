#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "manifest.json"
DECISIONS_PATH = ROOT / "asset-decisions.json"
INTEGRATION_PATH = ROOT / "integration-manifest.json"
VALIDATION_PATH = ROOT / "candidate-validation.json"


def identity(entry: dict[str, Any]) -> str:
    return f"{entry['archive'].upper()}:{int(entry['block']):03d}:{int(entry['frame']):03d}"


def archive_stem(entry: dict[str, Any]) -> str:
    return Path(entry["archive"]).stem.upper()


def runtime_name(entry: dict[str, Any]) -> str:
    return f"{archive_stem(entry)}_block_{int(entry['block']):03d}_frame_{int(entry['frame']):03d}.png"


def aspect_ratio(width: int, height: int) -> str:
    divisor = math.gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


def lifecycle(entry: dict[str, Any]) -> str:
    stem = archive_stem(entry)
    if stem == "TITLE":
        return "title_sequence"
    if stem.startswith("BIGPIC"):
        return "bigpic_until_outer_frame"
    if stem.startswith("PIC") or stem.startswith("FINAL"):
        return "normal_picture_until_panel_replace"
    if stem.startswith("HEAD"):
        return "portrait_head_until_portrait_or_panel_replace"
    if stem.startswith("BODY"):
        return "portrait_body_until_portrait_or_panel_replace"
    raise ValueError(f"unsupported lifecycle for {stem}")


def load_source_manifest() -> list[dict[str, Any]]:
    rows = json.loads(MANIFEST_PATH.read_text())
    if len(rows) != 231:
        raise ValueError(f"expected 231 ledger rows, found {len(rows)}")
    keys = [identity(row) for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate archive/block/frame identity in source manifest")
    return rows


def load_decisions() -> dict[str, dict[str, Any]]:
    return json.loads(DECISIONS_PATH.read_text()) if DECISIONS_PATH.exists() else {}


def resolve_candidate(candidate: str | None) -> Path | None:
    return (ROOT / candidate).resolve() if candidate else None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_rows() -> list[dict[str, Any]]:
    source_rows = load_source_manifest()
    decisions = load_decisions()
    source_keys = {identity(row) for row in source_rows}
    unknown = sorted(set(decisions) - source_keys)
    if unknown:
        raise ValueError(f"decisions reference unknown ledger identities: {unknown}")
    group_counts: dict[str, int] = {}
    for row in source_rows:
        group = f"{row['archive'].upper()}:{int(row['block']):03d}"
        group_counts[group] = group_counts.get(group, 0) + 1
    result = []
    for source in source_rows:
        key = identity(source)
        group = f"{source['archive'].upper()}:{int(source['block']):03d}"
        decision = decisions.get(key, {})
        result.append({
            "identity": key,
            "archive": source["archive"].upper(),
            "area": source.get("area"),
            "block": int(source["block"]),
            "frame": int(source["frame"]),
            "width": int(source["width"]),
            "height": int(source["height"]),
            "x": int(source["x"]),
            "y": int(source["y"]),
            "aspect_ratio": aspect_ratio(int(source["width"]), int(source["height"])),
            "animated": bool(source["animated"]),
            "delay": source.get("delay"),
            "animation_group": group,
            "animation_frame_count": group_counts[group],
            "source_png": source["png"],
            "source_sha256": source["sha256"],
            "runtime_name": runtime_name(source),
            "runtime_lookup": key,
            "lifecycle": lifecycle(source),
            "candidate": decision.get("candidate"),
            "review_status": decision.get("review_status", "missing"),
            "lifecycle_status": decision.get("lifecycle_status", "pending"),
            "notes": decision.get("notes", "")
        })
    return result


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=False) + "\n")
