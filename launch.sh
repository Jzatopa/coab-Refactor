#!/bin/bash
# Launches COAB (Curse of the Azure Bonds C# reconstruction) against the
# original Curse data.
#
# COAB loads every .dax/.geo asset by bare filename (e.g. "8x8d1.dax",
# "GEO1.dax") with no path prefix -- Classes/Gbl.cs's `data_path` field is
# declared but never assigned or used anywhere, so nothing wires in a data
# directory automatically. Running Main.exe from the repo root fails with
# "Unable to load <n> from <file>" because those files only exist under
# Data/. Running with Data/ as the working directory fixes it.
set -euo pipefail

COAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$COAB_DIR/Data"
exec mono "$COAB_DIR/Main/bin/Release/Main.exe" "$@"
