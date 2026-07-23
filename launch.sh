#!/usr/bin/env bash
# Launches COAB through the isolated full-auto runtime so the normal demo and
# game both receive the validated HD asset catalog. The tracked Data/ tree is
# used as the default original-data source but is never modified: run-full-auto
# copies it into runtime/full-auto/data, validates the identity ledger, and
# stages only approved lifecycle-verified HD replacements there.
set -euo pipefail

COAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export COAB_GAME_DIR="${COAB_GAME_DIR:-$COAB_DIR/Data}"
exec "$COAB_DIR/run-full-auto.sh" "$@"
