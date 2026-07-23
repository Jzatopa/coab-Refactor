# HD Asset Archive

This directory is the self-contained review and runtime archive for the HD artwork produced for the Full Auto COAB branch.

It contains:

- the complete current `HDAssets` image tree, including all **87** integrated archive/block/frame identities;
- approved image sources, retained review candidates, next-generation candidates, interchange composites, and contact sheets;
- all Markdown and JSON records under `image-uprez-pipeline/` and `test-evidence/`;
- the top-level lifecycle/foundation documentation and runtime lookup ledger;
- `MANIFEST.json` and `SHA256SUMS` for reproducible file verification.

Original low-resolution extracted DAX frames under `image-uprez-pipeline/png/` are deliberately not duplicated here: this archive is for HD work products and their records. Those source frames remain in their normal repository location.

Archive inventory: **268 files**, **473.1 MiB** before Git object deduplication.

Rebuild from the repository root with:

```bash
python3 scripts/build_hd_asset_archive.py
```
