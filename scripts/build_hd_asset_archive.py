#!/usr/bin/env python3
"""Build a self-contained archive of COAB HD art and its Markdown/JSON records."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "HD-ASSET-ARCHIVE"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
DOC_EXTS = {".md", ".json"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_record(source: Path, destination: Path, category: str, records: list[dict]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    records.append({
        "category": category,
        "source": source.relative_to(ROOT).as_posix(),
        "archive_path": destination.relative_to(OUT).as_posix(),
        "bytes": destination.stat().st_size,
        "sha256": sha256(destination),
    })


def image_files(base: Path, candidates_only: bool = False):
    if not base.exists():
        return
    for path in sorted(base.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
            continue
        if candidates_only and "candidates" not in path.parts:
            continue
        yield path


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    records: list[dict] = []

    image_roots = [
        ("runtime", ROOT / "HDAssets", False),
        ("approved", ROOT / "image-uprez-pipeline" / "approved", False),
        ("review-candidates", ROOT / "image-uprez-pipeline" / "review-candidates", False),
        ("nextgen-candidates", ROOT / "image-uprez-pipeline" / "nextgen" / "production-batches", True),
        ("interchange-tests", ROOT / "image-uprez-pipeline" / "interchange-test", False),
        ("contact-sheets", ROOT / "image-uprez-pipeline" / "contact-sheets", False),
    ]
    for category, base, candidates_only in image_roots:
        for source in image_files(base, candidates_only):
            relative = source.relative_to(base)
            copy_record(source, OUT / "images" / category / relative, f"image:{category}", records)

    doc_sources: set[Path] = set()
    for base in (ROOT / "image-uprez-pipeline", ROOT / "test-evidence"):
        if base.exists():
            doc_sources.update(
                path for path in base.rglob("*")
                if path.is_file() and path.suffix.lower() in DOC_EXTS
            )
    for source in (
        ROOT / "README.md",
        ROOT / "HD_ASSET_LIFECYCLE.md",
        ROOT / "FULL_AUTO_FOUNDATION_REPORT.md",
    ):
        if source.exists():
            doc_sources.add(source)
    for source in sorted(doc_sources):
        copy_record(source, OUT / "documents" / source.relative_to(ROOT), "document", records)

    for source in (
        ROOT / "HDAssets" / "runtime-lookup.tsv",
        ROOT / "test-evidence" / "pic4-batch-2026-07-23" / "PIC4_STAGED_HASHES.tsv",
    ):
        if source.exists():
            copy_record(source, OUT / "documents" / source.relative_to(ROOT), "ledger", records)

    base_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, check=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()
    counts: dict[str, int] = {}
    for record in records:
        counts[record["category"]] = counts.get(record["category"], 0) + 1
    manifest = {
        "schema": 1,
        "description": "Self-contained COAB HD image and documentation archive",
        "base_commit": base_commit,
        "file_count": len(records),
        "total_bytes": sum(record["bytes"] for record in records),
        "counts_by_category": counts,
        "files": records,
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")

    sums = [f'{record["sha256"]}  {record["archive_path"]}' for record in records]
    sums.append(f'{sha256(OUT / "MANIFEST.json")}  MANIFEST.json')
    (OUT / "SHA256SUMS").write_text("\n".join(sums) + "\n")

    readme = f"""# HD Asset Archive

This directory is the self-contained review and runtime archive for the HD artwork produced for the Full Auto COAB branch.

It contains:

- the complete current `HDAssets` image tree, including all **87** integrated archive/block/frame identities;
- approved image sources, retained review candidates, next-generation candidates, interchange composites, and contact sheets;
- all Markdown and JSON records under `image-uprez-pipeline/` and `test-evidence/`;
- the top-level lifecycle/foundation documentation and runtime lookup ledger;
- `MANIFEST.json` and `SHA256SUMS` for reproducible file verification.

Original low-resolution extracted DAX frames under `image-uprez-pipeline/png/` are deliberately not duplicated here: this archive is for HD work products and their records. Those source frames remain in their normal repository location.

Archive inventory: **{len(records)} files**, **{manifest['total_bytes'] / 1048576:.1f} MiB** before Git object deduplication.

Rebuild from the repository root with:

```bash
python3 scripts/build_hd_asset_archive.py
```
"""
    (OUT / "README.md").write_text(readme)
    print(f"built {OUT}: {len(records)} files, {manifest['total_bytes']} bytes")


if __name__ == "__main__":
    main()
