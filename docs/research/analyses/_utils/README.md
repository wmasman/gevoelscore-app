# analyses/_utils/

Shared utilities for analysis code under [`../`](../). Producer-mode per [`../../CONVENTIONS.md`](../../CONVENTIONS.md) §1.1 — Claude can write / edit freely. Sits at top level of `analyses/` so all subpackages can import without traversing producer-mode / reviewer-mode boundaries.

## What's here

| file | purpose | governed by |
|---|---|---|
| [`__init__.py`](__init__.py) | Python package marker | — |
| [`inference.py`](inference.py) | shared statistical-inference utilities used by HA-numbered hypothesis tests. Landed (Wiggers Tier 1 execution plan Bucket C, 2026-06-15): `stationary_bootstrap_ci` + `compute_data_driven_block_length` (C.2); `permutation_pvalue` (C.3 — event-level; renamed from "block-permutation null" since at the event level the resolution is combinatorics-dominated, not block-dominated); `holm_step_down` (C.4 — Holm step-down on N_eff ≈ 4 effective channels per cross-channel-correlation card). All four with companion synthetic-data tests in `test_inference.py`. | [`../../methodology/permutation_null_block_length.md`](../../methodology/permutation_null_block_length.md) + [`../../methodology/wiggers_test_design_on_chained_regime.md`](../../methodology/wiggers_test_design_on_chained_regime.md) § Cross-cutting §3-§4 |
| [`frame.py`](frame.py) | shared frame / data-prep utilities. Landed (Wiggers Tier 1 execution plan Bucket C, 2026-06-15): `z_score_vs_rolling_baseline` (CONVENTIONS §3.1; default robust median+MAD with configurable lag); `crash_drop_sensitivity` (CONVENTIONS §3.4 + pre-reg constraint 7; flags `|delta| > 0.10`); `stratum_4_mask` + `filter_to_stratum_4` (MD 1, single source of truth for Stratum 4 boundary, exposes `STRATUM_4_START` constant); `load_master` + `load_crash_labels` (resolve `$GEVOELSCORE_DATA_PATH`, enforce as-of-date convention per MD 1 §7). All with companion synthetic-data tests in `test_frame.py` (loaders tested for error-handling contract only — happy-path requires external CSVs per the privacy boundary). Tier 2 expansions land here lazily (peri-event window stacker, match-pair-finder, standardised effect-size functions, sensitivity-ladder runner) when the first HA-test imports them. | CONVENTIONS §3.1 + §3.4 + [`../../methodology/lc_era_temporal_segmentation.md`](../../methodology/lc_era_temporal_segmentation.md) |

Each function in `inference.py` / `frame.py` will have a companion test in `test_inference.py` / `test_frame.py` (synthetic-data correctness check; gates code correctness before any HA-test imports it; not skipped).

**Module organisation** (locked 2026-06-15): two thematic modules — `inference.py` (resampling + multiplicity correction) vs `frame.py` (data prep + sensitivity wrappers). The "do I import from inference or frame?" question is answered by "am I computing a CI / p-value / corrected threshold (inference) or am I prepping data / defining the stratum / running a sensitivity row (frame)?". If `frame.py` outgrows itself, can split into `baseline.py` / `events.py` / `sensitivity.py` later without breaking imports (re-exports work fine).

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
