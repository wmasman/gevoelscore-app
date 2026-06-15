# analyses/_utils/

Shared utilities for analysis code under [`../`](../). Producer-mode per [`../../CONVENTIONS.md`](../../CONVENTIONS.md) §1.1 — Claude can write / edit freely. Sits at top level of `analyses/` so all subpackages can import without traversing producer-mode / reviewer-mode boundaries.

## What's here

| file | purpose | governed by |
|---|---|---|
| [`__init__.py`](__init__.py) | Python package marker | — |
| [`inference.py`](inference.py) | shared statistical-inference utilities used by HA-numbered hypothesis tests (stationary bootstrap, block-permutation null, Holm step-down). Empty pending Wiggers Tier 1 execution plan C.2-C.4. | [`../../methodology/permutation_null_block_length.md`](../../methodology/permutation_null_block_length.md) + [`../../methodology/wiggers_test_design_on_chained_regime.md`](../../methodology/wiggers_test_design_on_chained_regime.md) § Cross-cutting §3-§4 |

Each function in `inference.py` will have a companion test in `test_inference.py` (synthetic-data correctness check; gates code correctness before any HA-test imports it).

## When to add a new utility here vs inline

**Add here**:

- Code used by ≥ 2 HA-tests (avoids divergence between near-identical implementations).
- Code whose correctness affects verdict comparability across tests (e.g. multiplicity correction).
- Code that implements a binding methodology MD (must stay in sync with the MD).

**Inline (in the test.py itself)**:

- Code specific to one hypothesis's operationalisation (e.g. HA-C3's spline fit; HA-C4's triad pass-2-of-3 rule).
- Code that wraps a shared utility for a specific hypothesis (the wrapper is per-test; the wrapped function lives here).

## What's NOT here

- **Pipeline / extraction code** lives under [`../../pipeline/`](../../pipeline/).
- **FIT timestamp_16 resolver** lives at [`../garmin_exploration/scripts/fit_utils.py`](../garmin_exploration/scripts/fit_utils.py) per CONVENTIONS §5 — that's the existing precedent for a shared utility in a producer-mode subfolder; `_utils/` is the equivalent for cross-hypothesis-test infrastructure.
- **Hypothesis-test artefacts** (`hypothesis.md`, `test.py`, `result.md`) are reviewer-mode per CONVENTIONS §1.2 and live under [`../hypotheses/`](../hypotheses/).
- **Descriptive analyses** that use shared utilities live under [`../descriptive/`](../descriptive/) or [`../garmin_exploration/`](../garmin_exploration/); they may import from `_utils/`.

## Discipline on changes

Because shared inference utilities affect verdict comparability across tests:

1. **A change to any function in `inference.py` after first use** is a methodological change and must be reflected in the relevant methodology MD (cite the MD § in the commit message + update the MD's revision date if the change is binding).
2. **The companion `test_inference.py` must stay green** on every change — synthetic-data correctness tests are the project's first defence against a silent inference bug propagating into multiple HA-test verdicts.
3. **HA-test re-runs after an `inference.py` change** are not automatic. The change-log in this README's "Revision log" section (added on first revision) tracks which HA-tests still need a re-run; cross-check before pushing.

## Cross-references

- [`../../CONVENTIONS.md`](../../CONVENTIONS.md) §1.1 (producer-mode role split)
- [`../../methodology/permutation_null_block_length.md`](../../methodology/permutation_null_block_length.md) (governs `stationary_bootstrap_ci` + `block_permutation_pvalue`)
- [`../../methodology/wiggers_test_design_on_chained_regime.md`](../../methodology/wiggers_test_design_on_chained_regime.md) § Cross-cutting §3 (governs `holm_step_down`) and § Cross-cutting §4 (two-resampling-layers distinction)
- [`../garmin_exploration/cards/cross-channel-correlation.md`](../garmin_exploration/cards/cross-channel-correlation.md) (source of the N_eff ≈ 4 estimate used by `holm_step_down`)
- Wiggers Tier 1 execution plan at `C:/Users/Gebruiker/.claude/plans/wiggers-tier1-execution-plan-2026-06-14.md` (the work plan that drives the initial contents)
