# `push_burden_7d` -- operationalisation-support descriptive analysis

**Strand**: A (operationalisation support; template-driven; no operationalisation interview required per [`descriptive/README.md`](../../README.md) section 7b).

## Research question

Operationalisation-support descriptive characterisation of `push_burden_7d_lagged` (the v3.2 lagged-baseline-corrected variant of `push_burden_7d`; the v3.1 un-lagged form is absent from master per audit MD 2026-06-11 item 2) on Stratum 4, answering Q3.8.a-i per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`; this channel listed under HA-touched non-confirmed candidate list as HA01b/HA01c primary, partially covered by activity-labels/; descriptive README section 3.4 also explicitly acknowledges 'push_burden's rolling-baseline contamination'). **4th of the 5 Tier 2 channels** in the user-prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; Tier 2 2nd = Q3.6 resting_hr `5d28219`; Tier 2 3rd = Q3.7 exertion_class `9b03bed`; this Q3.8 closes Tier 2 4th; next: Q3.9 gevoelscore -- dispatched in parallel).

Substantive status: **HA02c primary operand** on the v3.2 lagged baseline; LOCKED REFUTED both eras (train -18.7 pp / validate +0.7 pp per [`REJECTED.md`](../../../REJECTED.md) HA02c row + [`activity-labels/output/ha_results_4day_lagged.md`](../../../analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md); the lagged-baseline correction improved measurement standing but did NOT resurrect push_burden as a predictor). HA02c was NOT in the R14 single-pool re-anchor stretch list per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md); the closest single-pool diagnostic neighbour is the sister activity-axis **HA01b-recomputed** (LOCKED REFUTED both eras train +5.8 / validate +4.0; R14 single-pool **+5.1 pp [CI -14.7, +13.3] perm p (E[L]=7) = 0.3689** NOT-SUPPORTED CONVERGE; `badd04a`). Sister channel to Q3.7 exertion_class (just LANDED `9b03bed`); both activity-labels-family v3.1 -> v3.2 lagged-baseline corrected. **v3.1 -> v3.2 lagged-baseline correction is the canonical project example** per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed + descriptive README section 3.4 explicit acknowledgment + audit MD 2026-06-11 item 2 drop. Q3.8.b cites the correction descriptively per handoff section 2.4; this Q3.8 does NOT re-litigate per handoff section 3 hard constraint.

## Method

- **Surface**: Stratum 4 primary (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; n=1372 channel-valid days out of 1372 S4 days).
- **Channel-as-it-appears**: `push_burden_7d_lagged` (the v3.2 fix; integer-valued bounded support [0, 6]; count of push-days in trailing 7d window above the `[d-90, d-30]` lagged baseline per CONVENTIONS section 3.2). The v3.1 un-lagged `push_burden_7d` was DROPPED from master per audit MD 2026-06-11 item 2 (known rolling-baseline contamination per descriptive README section 3.4).
- **Phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister Strand-A analyses Q3.1 / Q3.2 / Q3.3 / Q3.4 / Q3.5 / Q3.6 / Q3.7.
- **Scope per handoff section 2.2**: standard continuous-channel template (no categorical adaptations; the integer-valued bounded-support means mean / median / MAD / quantiles apply identically to the continuous-channel precedent Q3.5 / Q3.6).
- **Cross-references** per handoff section 2.4: v3.1 -> v3.2 lagged-baseline correction descriptively cited in Q3.8.b (per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed + descriptive README section 3.4 explicit acknowledgment); REJECTED.md HA02c NULL + R14 HA01b-recomputed result (closest single-pool neighbour) in Q3.8.f; Q3.7 exertion_class sister-channel Spearman on ordinal-vs-numeric in Q3.8.e; sister-channel E[L]\* spread in Q3.8.b.
- **Computed directly from `per_day_master.csv`**: Q3.8.a (distribution shape + per-value frequency for integer count), Q3.8.b (Politis-White E[L]\* on Stratum-4 pool + v3.1 -> v3.2 correction descriptive citation), Q3.8.c (per-phase base rates citalopram axis), Q3.8.d (phase-stratified medians + v3 scope status), Q3.8.e (near-identity check |rho|>=0.92 on 17-channel panel incl. ordinal-encoded sister Q3.7 exertion_class), Q3.8.f (crash-vs-normal Cohen's d + Mann-Whitney U + stationary-bootstrap CI at E[L]=7 and data-driven E[L]\* + crash-drop sensitivity + LOAD-BEARING REJECTED.md HA02c + R14 HA01b-recomputed descriptive cross-reference), Q3.8.g (count-primitive spike-form discussion + cross-channel pairwise correlations), Q3.8.h (outlier detection + calibration-drift + activity-labels partial-coverage), Q3.8.i (covariate-sensitivity readiness for future HA pre-regs).
- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) (`compute_data_driven_block_length`, `stationary_bootstrap_ci`).
- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

## Result

Headline (see [`findings.md`](findings.md) for the full answers Q3.8.a-i):

`push_burden_7d_lagged` on Stratum 4 is an **integer-valued bounded-support [0, 6] count primitive on the activity axis** (median 2.00; MAD 1.00; skew +0.58; heavy_tail_flag=False; fraction at 0 = 19.2%; fraction at >=4 = 14.1%). **Data-driven E[L]\*=7.0** (Politis-White; vs project default E[L]=7). **Phase-stratified medians** (citalopram axis): unmedicated 2.00 -> consolidation 2.00. Episode-level Cohen's d=+0.13 (bootstrap CI95 [-0.36, +0.69]) -- descriptively corroborates HA02c's locked REJECTED-both-eras outcome (REJECTED.md HA02c row) at the first-order day-level read (HA02c's tested operand IS this Q3.8 channel at the spike-form Wiggers level). Near-identity check: **1** pair(s) at the |rho|>=0.92 CONVENTIONS section 3.3 threshold (the v3.2 _lcera sibling channel is the expected high-rho neighbour by construction).

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering Q3.8.a-i + tables (programmatically emitted by run.py from summary.json per the Q3.2/Q3.3/Q3.4/Q3.5/Q3.6/Q3.7 architectural note about the Write-tool harness heuristic on the literal filename "findings")
- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 5 PNGs: per-value frequency, phase-stratified violins, trajectory-with-phases, crash-vs-normal, ACF (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-05 corpus + 2026-06-24 analysis** (commit context: post-`9b03bed` Q3.7 exertion_class LANDED; Phase 2 'finish the descriptive analysis' Tier 2 batch 4th of 5 channels; Q3.9 gevoelscore dispatched in parallel). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up beyond the HA02c-locked operand.
2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).
3. Politis-White E[L]\* shifts by another factor of 2 from current 7.0.
4. activity-labels classifier definition.md severity cutoffs change (current state: cutoffs NOT locked per definition.md; Q3.8.h per-month rate-drift snapshots characterise stability AS-IS).
5. A v3.3 baseline-correction or any further upstream-classifier revision lands (current state: v3.2 lagged is canonical per CONVENTIONS section 3.2 + audit MD 2026-06-11 item 2 v3.1 drop).

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`); section 3.4 also explicitly names 'push_burden's rolling-baseline contamination'.
- **LOAD-BEARING canonical correction example**: [`REJECTED.md`](../../../REJECTED.md) HA02c row + HA01b-recomputed row + [CONVENTIONS section 3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses); Q3.8.b cites descriptively (NOT re-litigated per handoff section 3 hard constraint).
- **Q3.7 most-recent Tier 2 precedent (sister activity-axis channel)**: [`descriptive/operationalisation_support/exertion_class/`](../exertion_class/) -- Tier 2 3rd of 5; CATEGORICAL ADAPTATION + activity-labels family Q-template discipline; ordinal-encoded sibling near-identity check in Q3.8.e references the Q3.7 CATEGORY_ORDER encoding.
- **Q3.6 continuous-channel precedent**: [`descriptive/operationalisation_support/resting_hr/`](../resting_hr/) -- Tier 2 2nd of 5; clean programmatic-emit + f-string discipline.
- **Q3.5 Tier 2 first precedent**: [`descriptive/operationalisation_support/bb_overnight_gain/`](../bb_overnight_gain/) -- Tier 2 1st of 5; load-bearing cross-reference template.
- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) -- HA02c NOT in stretch list (row absent); HA01b-recomputed row descriptively corroborated in Q3.8.f as the closest sister-channel neighbour.
- **Partial-coverage activity-labels artefact**: [`analyses/garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/) -- existing primitive validation + visualisation; descriptively referenced in Q3.8.h.
- **HA-* tests that this analysis anchors**:
  - **HA02c** (LOCKED REFUTED both eras train -18.7 / validate +0.7; NOT in R14 stretch list); primary operand on this channel.
  - **HA01b-recomputed** (LOCKED REFUTED both eras train +5.8 / validate +4.0; R14 single-pool +5.1 pp NOT-SUPPORTED CONVERGE); sister activity-axis channel.
- **Methodology MDs**: `citalopram_phase_stratification.md`, `permutation_null_block_length.md`, `lc_era_temporal_segmentation.md`, `garmin_indicators_audit.md` (v3.1 drop + v3.2 lagged landing), `_descriptive_stocktake_2026-06-23.md` (gap-list framing).
- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- activity-axis upstream classifier per `activity-labels/definition.md` severity cutoffs + v3.2 lagged-baseline construction per CONVENTIONS section 3.2 `[d-90, d-30]` window. `labels_crash_v2.csv` per locked `crash_v2-definition`.
