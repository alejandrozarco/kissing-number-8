# Verification records

Release check of `lean/` exactly as published (every `.lean` file and the Lake configuration byte-identical; sha256 in
`files.sha256`), 2026-10-14, Linux x86_64, Lean v4.34.1, in two fresh copies of the package, each prepared with
`lake exe cache get` (Mathlib from the cache).

| file | content |
|---|---|
| `build_test.tsv` | first copy: `scripts/build_test.sh`, the 13 modules of `lean/Kissing8/`, each compiled one at a time in dependency order (`lean -j1`), wall time and peak resident memory (KiB) per module, all exit 0; then the axiom check of the script ("6 of 6 theorems reported, 0 outside" the three standard axioms) |
| `comparator.out` | second copy: `scripts/run_comparator.sh comparator.json`, a `lake build` of `Kissing8.Statement` and `Kissing8.Solution` from scratch, lean4export, "Lean default kernel accepts the solution", "Your solution is okay!", exit 0, for the six theorems of `lean/comparator.json`; Comparator step 17.9 min wall |
| `axioms.out` | `#print axioms`: `[propext, Classical.choice, Quot.sound]` for all six (the same output in both copies) |
| `files.sha256` | sha256 of the Lean files and the Lake configuration of the checked copies; identical in both copies |
| `time.txt` | GNU time of the whole check (both copies, including waiting for the shared lock): peak resident memory of any single process 7575052 KiB (7.22 GiB) |

Comparator ran with its non-sandboxing shim `fake-landrun.sh`, because `landrun` was not available on the machine.
Tool revisions and binary sha256: `lean/scripts/tools.sh`.
