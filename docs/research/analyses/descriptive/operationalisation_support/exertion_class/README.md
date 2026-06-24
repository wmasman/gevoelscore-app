# `exertion_class` -- operationalisation-support descriptive analysis

**Strand**: A (operationalisation support; template-driven with CATEGORICAL ADAPTATIONS documented per Q3.7.a-i; no operationalisation interview required per [`descriptive/README.md`](../../README.md) section 7b).

## Research question

Operationalisation-support descriptive characterisation of `exertion_class` on Stratum 4, answering Q3.7.a-i per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`; this channel listed as HA01b/HA01c primary, partially covered by activity-labels/). **3rd of the 5 Tier 2 channels** in the user-prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; Tier 2 2nd = Q3.6 resting_hr `5d28219`; this Q3.7 closes Tier 2 3rd; next: Q3.8 push_burden_7d, Q3.9 gevoelscore).

Substantive status: **HA01b-recomputed primary operand** on the lagged variant (v3.2 lagged composite at exertion_class_lagged in {heavy, very_heavy}; LOCKED REFUTED both eras +5.8 / +4.0 pp per [activity-labels/output/ha_results_4day_lagged.md](../../../analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md); R14 single-pool **+5.1 pp [-14.7, +13.3] perm p=0.3689 NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED)** `badd04a`). Also **HA01b-per-axis-diagnostic primary** (SUPPORTED both eras at locked tau=0.75; load-bearing WITHHELD due to v2 threshold-monotonicity-diagnostic AMBIGUOUS) and **HA01c-effective-exertion-shock primary** on eff_exertion_rank_lagged (SUPPORTED both eras train +21.3 / validate +19.5; load-bearing WITHHELD per the same v2 diagnostic ambiguity per [REJECTED.md HA01c](../../../REJECTED.md)). HA-C4c (LANDED PARTIAL `a69a8ed`) uses `exertion_class_lagged_lcera in {heavy, very_heavy}` as the heavy-T classifier on T per [HA-C4c hypothesis.md section 4.1](../../../analyses/hypotheses/HA-C4c/hypothesis.md). **v3.1 -> v3.2 lagged-baseline correction is the canonical project example** per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed; the original HA01b validate +17.3 pp 'first SUPPORTED' headline was a v3.1 rolling-baseline artefact (softened by -13.3 pp on v3.2 recomputation). Q3.7.b cites the correction descriptively per handoff section 2.4; this Q3.7 does NOT re-litigate per handoff section 3 hard constraint.

## Method

- **Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; n=1372 channel-valid days out of 1372 S4 days).
- **Primary phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister Strand-A analyses Q3.1 / Q3.2 / Q3.3 / Q3.4 / Q3.5 / Q3.6.
- **Scope per handoff section 1**: focus on **un-lagged primary `exertion_class`**; lagged variants (`exertion_class_lagged` + `exertion_class_lagged_lcera`) are derivatives used in HA pre-reg contexts (HA01b-recomputed, HA-C4c heavy-T classifier) and are out of Strand-A scope.
- **CATEGORICAL ADAPTATIONS** of the Q-template (per handoff section 1, modelled on the stress_low_motion count-primitive adaptation precedent) documented explicitly per Q3.7.x section: Q3.7.a per-category frequencies + Shannon entropy (no mean/median/skewness); Q3.7.b autocorrelation on **ordinal encoding** + transition-rate analysis; Q3.7.c per-phase per-category frequency distribution + per-phase entropy; Q3.7.d chi-square test of independence (4 phases x 5 categories) + pairwise frequency shifts; Q3.7.e Spearman on ordinal encoding vs continuous-form sibling activity-axis primitives + categorical-sibling marking on lagged variants; Q3.7.f **chi-square 2x5 AND Mann-Whitney U on ordinal** + Cohen's d on ordinal; Q3.7.g heavy/very_heavy class fraction + within-7d burst-rate + consecutive-run distribution; Q3.7.h rare-class flag + per-month rate-drift snapshots + boundary-step reads (no MAD-z; outlier semantics differ for categorical); Q3.7.i covariate-sensitivity readiness.
- **Computed directly from `per_day_master.csv`**: Q3.7.a (per-category frequencies + entropy + auxiliary ordinal summaries), Q3.7.b (Politis-White E[L]\* on ordinal + transition rate + per-class persistence + v3.1 -> v3.2 lagged-baseline correction descriptive citation), Q3.7.c (per-phase per-category frequencies + entropy), Q3.7.d (global chi-square + pairwise frequency shifts + HA01b-recomputed/HA01c/HA-C4c locked-verdict cross-reference), Q3.7.e (Spearman on ordinal vs activity-axis sibling panel), Q3.7.f (chi-square 2x5 + Mann-Whitney U + ordinal Cohen's d + LOAD-BEARING R14 HA01b-recomputed single-pool descriptive cross-reference), Q3.7.g (heavy/very_heavy spike-form + burst-rate + run distribution + HA-C4c heavy-T classifier framing), Q3.7.h (rare-class + per-month rate-drift + boundary-step reads + activity-labels partial-coverage xref), Q3.7.i (covariate readiness with v3.2 lagged variant as the CONVENTIONS section 3.2 audit-hook compliance covariate).
- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) (`compute_data_driven_block_length`, `stationary_bootstrap_ci`).
- **Load-bearing cross-references** per handoff section 2.4: v3.1 -> v3.2 lagged-baseline correction descriptively cited in Q3.7.b per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed; R14 HA01b-recomputed NOT-SUPPORTED single-pool descriptively corroborated in Q3.7.f; HA-C4c heavy-T classifier framing in Q3.7.g; activity-labels partial-coverage descriptively referenced in Q3.7.h. NO substantive HA verdict promotion per CONVENTIONS section 2.1; NO re-litigation of v3.1 -> v3.2 correction per handoff section 3 hard constraint.
- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

## Result

Headline (see [`findings.md`](findings.md) for the full answers Q3.7.a-i):

`exertion_class` on Stratum 4 is a **5-level categorical activity-axis channel** (distribution: none 25.3%, light 23.7%, moderate 16.0%, heavy 17.8%, very_heavy 17.2%; Shannon entropy = 1.592 nats = 98.9% of max log(5); heavy+very_heavy spike-class fraction = 35.0%; at-rest none-class fraction = 25.3%). **Politis-White E[L]\*=7.0 (vs project default 7); factor-of-2 deviation flag = False** on ordinal-encoded series (transition rate = 77.0%). **Per-citalopram-phase**: chi-square(df=12) = 11.99, p=0.4466; heavy+very_heavy fraction unmedicated 36.1% -> consolidation 33.5% -> afbouw 34.6%. **Crash-vs-normal**: chi-square 2x5 = 5.03 p=0.2836; MWU on ordinal z=-1.94 p=0.0527; heavy+very_heavy fraction diff = -10.5%; ordinal median diff = -1.0; episode-level Cohen's d on ordinal = -0.23 -- descriptively re-anchors HA01b-recomputed locked-REFUTED + R14 +5.1 pp NOT-SUPPORTED and HA01c locked-SUPPORTED-load-bearing-WITHHELD signals at the un-lagged-primary day-level read. **Spike-form**: heavy+very_heavy burst-rate (>=2 spike days in trailing 7d) = 73.9%; max consecutive heavy+very_heavy run = 5 days; HA-C4c uses the lagged variant for its heavy-T classifier per hypothesis.md section 4.1. Near-identity check: **0** pair(s) fire at the |rho|>=0.92 CONVENTIONS section 3.3 threshold.

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering Q3.7.a-i + tables (programmatically emitted by run.py from summary.json per the Q3.2/Q3.3/Q3.4/Q3.5/Q3.6 architectural note about the Write-tool harness heuristic on the literal filename "findings")
- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 5 PNGs: per-category frequency, phase-stratified stacked bars, monthly rate trajectory with phase shading, crash-vs-normal per-category bars, ACF on ordinal encoding (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-05 corpus + 2026-06-24 analysis** (commit context: post-`5d28219` Q3.6 resting_hr LANDED; Phase 2 'finish the descriptive analysis' Tier 2 batch 3rd of 5 channels). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up beyond the HA01b-recomputed-locked + HA-C4c-locked operands.
2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).
3. Politis-White E[L]\* on ordinal encoding shifts by another factor of 2 from current 7.0.
4. activity-labels classifier definition.md severity cutoffs change (current state: cutoffs NOT locked per definition.md; Q3.7.h per-month rate-drift snapshots characterise stability AS-IS).
5. A v3.3 baseline-correction or any further upstream-classifier revision lands (current state: v3.2 lagged is canonical for downstream PEM-pacing consumers per CONVENTIONS section 3.2).

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`)
- **LOAD-BEARING canonical correction example**: [`REJECTED.md`](../../../REJECTED.md) HA01b-recomputed row + [CONVENTIONS section 3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses); Q3.7.b cites descriptively (NOT re-litigated per handoff section 3 hard constraint).
- **Q3.6 most-recent Tier 2 precedent**: [`descriptive/operationalisation_support/resting_hr/`](../resting_hr/) -- Tier 2 2nd of 5; programmatic-emit pattern + clean f-string discipline.
- **Q3.5 Tier 2 first precedent**: [`descriptive/operationalisation_support/bb_overnight_gain/`](../bb_overnight_gain/) -- Tier 2 1st of 5; load-bearing cross-reference template.
- **Non-continuous-primitive adaptation precedent**: [`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/`](../stress_low_motion_min_count_S60_Mlow/) -- count-primitive adaptation precedent; model for CATEGORICAL ADAPTATION discipline in this Q3.7.
- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) -- HA01b-recomputed row descriptively corroborated in Q3.7.f.
- **Partial-coverage activity-labels artefact**: [`analyses/garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/) -- existing primitive validation + visualisation; descriptively referenced in Q3.7.h.
- **HA-* tests that this analysis anchors**:
  - **HA01b-recomputed** (LOCKED REFUTED both eras +5.8 / +4.0; R14 single-pool NOT-SUPPORTED CONVERGE); primary operand on lagged variant of this channel.
  - **HA01b-per-axis-diagnostic** (LOCKED SUPPORTED both eras at tau=0.75; load-bearing WITHHELD); per-axis read on lagged variant of this channel.
  - **HA01c-effective-exertion-shock** (LOCKED SUPPORTED both eras at tau=0.75; load-bearing WITHHELD); uses eff_exertion_rank_lagged.
  - **HA-C4c** (LANDED PARTIAL `a69a8ed`): uses exertion_class_lagged_lcera in {heavy, very_heavy} as heavy-T classifier on T.
- **Methodology MDs**: `citalopram_phase_stratification.md`, `permutation_null_block_length.md`, `lc_era_temporal_segmentation.md`, `garmin_indicators_audit.md`, `_descriptive_stocktake_2026-06-23.md` (gap-list framing).
- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- activity-axis upstream classifier producing exertion_class per `analyses/garmin_exploration/activity-labels/definition.md` severity cutoffs. `labels_crash_v2.csv` per locked `crash_v2-definition`.
