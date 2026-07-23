#!/usr/bin/env python3
"""Mirror the original-asset category tree and place verified HD counterparts in it.

The target name is always the original PNG stem suffixed with ``_HD``.  Only
asset-decision entries marked both approved and lifecycle-verified are used;
that avoids selecting an arbitrary rejected or competing review candidate.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "original assets"
HD_ROOT = ROOT / "HDAssets"
DECISIONS = ROOT / "image-uprez-pipeline" / "asset-decisions.json"
MANIFEST = ROOT / "HD_ASSET_TREE_MANIFEST.json"
HD_ARCHIVE_RUNTIME = ROOT / "HD-ASSET-ARCHIVE" / "images" / "runtime"
KEY = re.compile(r"^(?P<archive>[A-Z0-9]+)\.DAX:(?P<block>\d{3}):(?P<frame>\d{3})$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def original_path(archive: str, block: str, frame: str) -> Path:
    return ORIGINAL / archive / f"{archive}_block_{block}_frame_{frame}.png"


def hd_name(original: Path) -> str:
    return f"{original.stem}_HD{original.suffix}"


def resolve_hd_source(candidate: str) -> Path:
    """Resolve a decision candidate, including removed legacy HDAssets paths."""
    source = (DECISIONS.parent / candidate).resolve()
    if source.is_file():
        return source
    try:
        legacy_relative = source.relative_to(HD_ROOT)
    except ValueError:
        return source
    archived = HD_ARCHIVE_RUNTIME / legacy_relative
    return archived if archived.is_file() else source


def main() -> None:
    decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))

    matched: dict[Path, tuple[Path, str]] = {}
    skipped: list[dict[str, str]] = []
    for identity, decision in sorted(decisions.items()):
        if (
            decision.get("review_status") != "approved"
            or decision.get("lifecycle_status") != "verified"
        ):
            continue
        match = KEY.fullmatch(identity)
        if not match:
            skipped.append({"identity": identity, "reason": "unrecognized identity"})
            continue
        original = original_path(**match.groupdict())
        source = resolve_hd_source(decision["candidate"])
        if not original.is_file():
            skipped.append({"identity": identity, "reason": f"original absent: {original.relative_to(ROOT)}"})
            continue
        if not source.is_file():
            skipped.append({"identity": identity, "reason": f"HD source absent: {source}"})
            continue
        matched[original] = (source, identity)

    # The extracted village PNG is a duplicate source asset with a distinct
    # user-facing filename, so retain its direct HD counterpart as well.
    village_original = ORIGINAL / "extracted-assets" / "PIC1_block_080_village.png"
    village_hd = ROOT / "image-uprez-pipeline" / "approved" / "PIC1_block_080_village.png"
    if village_original.is_file() and village_hd.is_file():
        matched[village_original] = (village_hd, "PIC1.DAX:080:000 (extracted alias)")

    # Reuse an HD rendering only when the corresponding original PNG bytes are
    # exactly identical. This safely handles artwork repeated across DAX
    # archives (for example PIC4 block 067 repeated in PIC6) without relying on
    # filenames or subjective visual similarity.
    duplicate_groups: dict[str, list[Path]] = defaultdict(list)
    for original in ORIGINAL.rglob("*.png"):
        duplicate_groups[sha256(original)].append(original)
    for originals in duplicate_groups.values():
        donors = [(original, matched[original]) for original in originals if original in matched]
        if not donors:
            continue
        donor_hashes = {sha256(source) for _, (source, _) in donors}
        if len(donor_hashes) != 1:
            skipped.append(
                {
                    "identity": ", ".join(p.relative_to(ORIGINAL).as_posix() for p in originals),
                    "reason": "identical originals have conflicting HD donor images",
                }
            )
            continue
        donor_original, (source, donor_identity) = donors[0]
        for original in originals:
            if original not in matched:
                matched[original] = (
                    source,
                    "exact-original duplicate of "
                    f"{donor_original.relative_to(ORIGINAL).as_posix()} [{donor_identity}]",
                )

    staging = Path(tempfile.mkdtemp(prefix="HDAssets.", dir=ROOT))
    for directory in sorted(path for path in ORIGINAL.rglob("*") if path.is_dir()):
        (staging / directory.relative_to(ORIGINAL)).mkdir(parents=True, exist_ok=True)

    entries = []
    for original, (source, identity) in sorted(matched.items()):
        relative_target = original.relative_to(ORIGINAL).parent / hd_name(original)
        target = staging / relative_target
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        entries.append(
            {
                "original": original.relative_to(ORIGINAL).as_posix(),
                "hd": relative_target.as_posix(),
                "identity": identity,
                "source": source.relative_to(ROOT).as_posix(),
                "sha256": sha256(target),
            }
        )

    payload = {
        "purpose": "Verified HD counterparts arranged in the original asset folder tree.",
        "naming": "Each target uses the original filename with _HD before .png.",
        "original_png_count": sum(1 for _ in ORIGINAL.rglob("*.png")),
        "matched_hd_count": len(entries),
        "unmatched_original_count": sum(1 for _ in ORIGINAL.rglob("*.png")) - len(entries),
        "selection_rule": "approved and lifecycle-verified entries, plus reuse where original PNG SHA-256 hashes are exactly identical",
        "entries": entries,
        "skipped": skipped,
    }
    if HD_ROOT.exists():
        shutil.rmtree(HD_ROOT)
    staging.rename(HD_ROOT)
    MANIFEST.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"created a clean tree with {len(entries)} matched HD files")
    print(f"mirrored {sum(1 for _ in ORIGINAL.rglob('*') if _.is_dir())} original asset directories")
    print(f"wrote {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
