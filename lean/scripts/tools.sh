# Sourced by run_comparator.sh: clones the two external checkers at fixed revisions into $TOOLS (default .tools/)
# and builds them. The records in verification/ were made with binaries built from these revisions:
#   comparator   9c52a28d59016a453d9d5da3c1fe09240f6fc4946863bc60849c9b361310c499 (sha256; its own toolchain)
#   lean4export  8c5d64ba68f4d3a68b3bcb7e1c5f188e35ae573b29470b8d4530a62324c9ddd1 (sha256; this package's toolchain)
COMPARATOR_REV=fd5d5bcf14177b187f66d4502071268d877887c3   # https://github.com/leanprover/comparator
EXPORT_REV=076e8e57707e813375e8f9da8bf989799ace9680       # https://github.com/leanprover/lean4export (format 3.1.0)
TOOLS="${TOOLS:-$ROOT/.tools}"; mkdir -p "$TOOLS"; TOOLS="$(cd "$TOOLS" && pwd)"

checkout_at() {  # checkout_at <name> <repository url> <revision>
  local dir="$TOOLS/$1"
  [ -d "$dir/.git" ] || git clone --quiet "$2" "$dir"
  git -C "$dir" checkout --quiet "$3"
  if [ "$(git -C "$dir" rev-parse HEAD)" != "$3" ]; then echo "$1: expected revision $3" >&2; exit 1; fi
}

build_lean4export() {
  checkout_at lean4export https://github.com/leanprover/lean4export "$EXPORT_REV"
  # The exporter reads .olean files, so it has to be built with the Lean version that wrote them.
  if ! cmp -s "$ROOT/lean-toolchain" "$TOOLS/lean4export/lean-toolchain"; then
    cp "$ROOT/lean-toolchain" "$TOOLS/lean4export/lean-toolchain"
    rm -rf "$TOOLS/lean4export/.lake/build"
  fi
  (cd "$TOOLS/lean4export" && lake build)
  COMPARATOR_LEAN4EXPORT="$TOOLS/lean4export/.lake/build/bin/lean4export"
}

build_comparator() {
  checkout_at comparator https://github.com/leanprover/comparator "$COMPARATOR_REV"
  (cd "$TOOLS/comparator" && lake build)
  COMPARATOR_BIN="$TOOLS/comparator/.lake/build/bin/comparator"
}
