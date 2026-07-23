#!/usr/bin/env python3
"""Create or verify an immutable lock for HD assets already accepted in-game."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

from integration_common import resolve_candidate

PIPELINE = Path(__file__).resolve().parent.parent
WORKSPACE = PIPELINE.parents[1]
MANIFEST = PIPELINE / "integration-manifest.json"
OUTPUT = Path(__file__).resolve().parent / "protected-assets.json"
ROOTS = {
    "stable-runtime": Path.home() / "Downloads/curseoftheazurebonds/HDAssets",
    "full-auto-runtime": WORKSPACE / "coab-uprez-full-auto/runtime/full-auto/data/HDAssets",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect() -> dict:
    files = []
    for root_name, root in ROOTS.items():
        if not root.is_dir():
            raise SystemExit(f"missing HD asset root: {root}")
        for path in sorted(root.rglob("*.png")):
            with Image.open(path) as image:
                width, height = image.size
            files.append({
                "root": root_name,
                "relative_path": path.relative_to(root).as_posix(),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
                "width": width,
                "height": height,
            })

    rows = json.loads(MANIFEST.read_text())
    protected_entries = []
    for row in rows:
        if row["review_status"] != "approved" or row["lifecycle_status"] != "verified":
            continue
        candidate = resolve_candidate(row["candidate"])
        if candidate is None or not candidate.is_file():
            raise SystemExit(f"approved candidate is missing: {row['candidate']}")
        protected_entries.append({
            "identity": row["identity"],
            "runtime_name": row["runtime_name"],
            "candidate_sha256": sha256(candidate),
        })
    protected_entries.sort(key=lambda item: item["identity"])
    return {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "policy": "Never overwrite, regenerate, restage, or silently replace these files or identities without explicit maintainer approval.",
        "roots": {
            "stable-runtime": "$COAB_GAME_DIR/HDAssets",
            "full-auto-runtime": "runtime/full-auto/data/HDAssets",
        },
        "protected_identities": [item["identity"] for item in protected_entries],
        "protected_entries": protected_entries,
        "files": files,
    }


def verify(lock: dict) -> list[str]:
    errors = []
    for record in lock["files"]:
        path = ROOTS[record["root"]] / record["relative_path"]
        if not path.is_file():
            errors.append(f"missing: {path}")
            continue
        actual = sha256(path)
        if actual != record["sha256"]:
            errors.append(f"changed: {path} expected={record['sha256']} actual={actual}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        lock = json.loads(OUTPUT.read_text())
        errors = verify(lock)
        if errors:
            raise SystemExit("\n".join(errors))
        print(f"PASS: {len(lock['files'])} protected HD files and {len(lock['protected_identities'])} integrated identities are unchanged")
        return

    lock = collect()
    OUTPUT.write_text(json.dumps(lock, indent=2) + "\n")
    print(f"locked {len(lock['files'])} HD files and {len(lock['protected_identities'])} integrated identities in {OUTPUT}")


if __name__ == "__main__":
    main()
