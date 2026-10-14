#!/usr/bin/env bash
# Comparator (https://github.com/leanprover/comparator) for this package: it checks that the theorems named in the
# config are proved in the solution module with exactly the statements of the challenge module (where they are
# `sorry`), use no axioms beyond the permitted ones, and pass the Lean kernel on a lean4export dump.
# Prepare the workspace with `lake exe cache get`. Prebuilt tools can be given as COMPARATOR_BIN and
# COMPARATOR_LEAN4EXPORT; otherwise scripts/tools.sh builds them (git and network needed). Comparator runs the build
# under `landrun` (Linux Landlock); if COMPARATOR_LANDRUN is unset and no `landrun` is installed, its non-sandboxing
# shim scripts/fake-landrun.sh is used, with a warning.
# Usage: bash scripts/run_comparator.sh [config]   (default comparator.json). Log: logs/comparator.log
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
source scripts/tools.sh
[ -n "${COMPARATOR_LEAN4EXPORT:-}" ] || build_lean4export
BUILT=""
[ -n "${COMPARATOR_BIN:-}" ] || { build_comparator; BUILT=1; }
if [ -z "${COMPARATOR_LANDRUN:-}" ]; then
  if command -v landrun > /dev/null 2>&1; then
    COMPARATOR_LANDRUN="$(command -v landrun)"
  elif [ -n "$BUILT" ]; then
    COMPARATOR_LANDRUN="$TOOLS/comparator/scripts/fake-landrun.sh"
    echo "WARNING: landrun not found; using Comparator's non-sandboxing shim $COMPARATOR_LANDRUN" >&2
  else
    echo "landrun not found: set COMPARATOR_LANDRUN (landrun, or Comparator's scripts/fake-landrun.sh)" >&2; exit 1
  fi
fi
[ -x "$COMPARATOR_LANDRUN" ] || { echo "COMPARATOR_LANDRUN is not executable: $COMPARATOR_LANDRUN" >&2; exit 1; }
export COMPARATOR_LEAN4EXPORT COMPARATOR_LANDRUN LAKE_ARTIFACT_CACHE=false
mkdir -p logs
/usr/bin/time -p lake env "$COMPARATOR_BIN" "${1:-comparator.json}" 2>&1 | tee logs/comparator.log
echo "COMPARATOR EXIT: ${PIPESTATUS[0]}"
