#!/usr/bin/env python3
from integration_common import INTEGRATION_PATH, build_rows, write_json

rows = build_rows()
write_json(INTEGRATION_PATH, rows)
print(f"wrote {INTEGRATION_PATH.name}: {len(rows)} deterministic runtime lookups")
