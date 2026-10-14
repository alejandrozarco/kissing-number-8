# AI disclosure

AI models produced the content of this repository: the Lean formalisation, the generators, the numerical checks, the
figures and the text. The repository owner chose the problem, approved the Lean statement, directed the work and
decided on scope and publication. The owner did not check the mathematics or the Lean code line by line.

**Models**
- Claude Opus 5.5 (Anthropic, via Claude Code) did the work. A separate instance of Claude Opus 5.5, directed by the
  first, wrote the lower-bound module `lean/Kissing8/TwoForty.lean` and its generator.
- The review was run as a separate read-only instance of gpt-6-astra (OpenAI, via the Codex CLI).
- The commits carry a `Co-Authored-By: Claude Opus 5.5` trailer.

**Review and errors found.** The review found no mathematical error. Independently of the
repository code it re-derived all 42 splitting identities and the coefficients of the polynomial in exact arithmetic,
checked the 240 points (distinct, norm 2, pairwise distance at least 2, the same set as the generator's), and checked
that the proved statements match `lean/Kissing8/Statement.lean`. It asked for three changes, all made:
- the build script only recorded the `#print axioms` output; `lean/scripts/build_test.sh` now fails unless every
  theorem of the axiom file uses only `propext`, `Classical.choice` and `Quot.sound`;
- `lean/scripts/run_comparator.sh` guessed the location of Comparator's non-sandboxing shim for prebuilt binaries; it
  now requires `landrun` or an explicit `COMPARATOR_LANDRUN` in that case;
- a doc comment in `lean/Kissing8/Solution.lean` named the wrong Comparator configuration file.

Problems found and fixed during the work: the first version of the lower-bound check stored the 240 points in a
table whose kernel lookup cost grows with the row index, and its memory use exceeded the limit set for the build
machine; the table is now a list checked block by block. Two proofs needed small corrections before they compiled.

AI review is not peer review, and no human expert has checked this work. In the terminology of the Lean community
this is a *warrant*, not a human-readable proof.

**What is checked by software**
- The Lean 4 kernel checks the formalisation in `lean/`. `#print axioms` reports `[propext, Classical.choice, Quot.sound]`.
- Comparator checks that the proved theorems have the statements of `lean/Kissing8/Statement.lean`. It ran without the
  `landrun` sandbox (`verification/`).
- The generators check every identity (sympy) and the 240 points before writing the Lean files; the Lean kernel then
  checks them again.

What remains to be trusted:
- that `lean/Kissing8/Statement.lean` expresses the intended theorem (see `lean/STATEMENT.md`);
- the Mathlib definitions used in `lean/Kissing8/Statement.lean`, which imports only Mathlib;
- the Lean kernel and toolchain;
- Comparator and lean4export (run without the `landrun` sandbox).
