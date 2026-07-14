#!/usr/bin/env bash
set -euo pipefail

COAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAME_DIR="${COAB_GAME_DIR:-$HOME/Downloads/curseoftheazurebonds}"
RUNTIME_DIR="${COAB_FULL_AUTO_RUNTIME_DIR:-$COAB_DIR/runtime/full-auto}"
DATA_DIR="$RUNTIME_DIR/data"
USER_DATA_DIR="$RUNTIME_DIR/user-data"
EXE="$COAB_DIR/Main/bin/Release/Main.exe"
PIPELINE="$COAB_DIR/image-uprez-pipeline"

if [[ ! -f "$EXE" ]]; then
  echo "Full-auto COAB executable not found: $EXE" >&2
  echo "Build it with: xbuild /property:Configuration=Release $COAB_DIR/coab.sln" >&2
  exit 1
fi
if [[ ! -d "$GAME_DIR" ]]; then
  echo "Original Curse data directory not found: $GAME_DIR" >&2
  exit 1
fi
if [[ ! -d "$COAB_DIR/HDAssets" ]]; then
  echo "Full-auto HD asset directory not found: $COAB_DIR/HDAssets" >&2
  exit 1
fi

mkdir -p "$DATA_DIR" "$USER_DATA_DIR"

# The full-auto fork receives its own mutable runtime tree. Never install or
# synchronize HD assets into the stable game directory.
rsync -a --delete \
  --exclude='/HDAssets/' \
  --exclude='/HDAssets-disabled/' \
  --exclude='/mono_crash.*' \
  "$GAME_DIR/" "$DATA_DIR/"
rm -rf "$DATA_DIR/HDAssets"
cp -a "$COAB_DIR/HDAssets" "$DATA_DIR/HDAssets"

# Validate all 231 ledger identities and atomically stage only assets whose
# art review and retained-HD lifecycle are both approved.
python3 "$PIPELINE/validate_candidates.py" --strict
python3 "$PIPELINE/stage_approved_assets.py" "$DATA_DIR/HDAssets"

if [[ "${COAB_PREPARE_ONLY:-0}" == "1" ]]; then
  python3 "$PIPELINE/report_status.py" --runtime "$DATA_DIR/HDAssets"
  exit 0
fi

export COAB_USER_DATA_DIR="$USER_DATA_DIR"
export DISPLAY="${DISPLAY:-:0}"
export GTK_MODULES="${GTK_MODULES:-}"
export GTK3_MODULES="${GTK3_MODULES:-}"
export MONO_IOMAP="${MONO_IOMAP:-case}"
export MONO_MWF_USE_XIM="${MONO_MWF_USE_XIM:-disabled}"

if [[ -z "${XAUTHORITY:-}" ]]; then
  shopt -s nullglob
  auth_files=(/run/user/"$(id -u)"/.mutter-Xwaylandauth.* "$HOME/.Xauthority")
  shopt -u nullglob
  if (( ${#auth_files[@]} > 0 )); then
    export XAUTHORITY="${auth_files[0]}"
  fi
fi

cd "$DATA_DIR"
exec mono "$EXE" "$@"
