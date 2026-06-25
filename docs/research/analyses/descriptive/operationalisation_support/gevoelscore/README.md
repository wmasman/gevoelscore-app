# `gevoelscore` -- operationalisation-support descriptive analysis

**Strand**: A (operationalisation support; template-driven; no operationalisation interview required per [`descriptive/README.md`](../../README.md) section 7b).

## Research question

Operationalisation-support descriptive characterisation of `gevoelscore` (per-day self-reported felt-state on a 1-6 integer scale; the OUTCOME side of nearly every HA in the project) on Stratum 4, answering Q3.9.a-i per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`; this channel listed under HA-touched non-confirmed candidate list as `gevoelscore (almost every test's outcome side)`). **5th (FINAL) of the 5 Tier 2 channels** in the user-prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; 2nd = Q3.6 resting_hr `5d28219`; 3rd = Q3.7 exertion_class `9b03bed`; 4th = Q3.8 push_burden_7d `92d7193`; this Q3.9 closes Tier 2).

Substantive status: **HA-C3 v2 + HA-C3p direct outcome** (both LOCKED; joint inverted-U finding -- the stress -> felt-state mapping is concave with peak around stress 30-40, NOT convex per Wiggers' verbatim prediction). **HA10 + HA07d + many other HAs** use gevoelscore in their crash labels indirectly via [`crash_v2-definition`](../../../analyses/hypotheses/crash_v2-definition/) (LOCKED). **gevoelscore was NOT in v3 multi-channel dose-response sweep scope** per descriptive README section 3.4 + handoff section 1 ('it's the outcome, not a Garmin channel'); no v3 verdict exists to cite or re-promote.

## Method

- **Surface**: Stratum 4 primary (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; n=1372 channel-valid days out of 1372 S4 days). Stratum 4 IS the gevoelscore-having days by definition per [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md).
- **Channel-as-it-appears**: `gevoelscore` (bounded 1-6 INTEGER scale per crash_v2-definition substrate; app-brief framing is 1-10 but empirical range is 1-6).
- **Phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister Strand-A analyses Q3.1-Q3.8. Also 6-phase recovery axis per [`lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) for Q3.9.c overlap notation against recovery_arc v2.
- **Scope per handoff section 2.2**: standard Q-template Q3.9.a-i with **OUTCOME-CHANNEL ADAPTATIONS** documented at each cell. The bounded 1-6 integer scale requires: per-value frequency vector + Shannon entropy as load-bearing distribution primitives in Q3.9.a; no classical outliers in Q3.9.h (MAD-z > 5 is structurally impossible); DROP primitive (NOT spike-count) in Q3.9.g; honest tautology framing in Q3.9.f (crash IS defined by gevoelscore).
- **Cross-references** per handoff section 2.4: HA-C3 v2 + HA-C3p outcome-side inverted-U descriptively corroborated in Q3.9.a + Q3.9.d + Q3.9.e; recovery_arc v2 overlap notation in Q3.9.c (not re-characterisation); crash_v2-definition tautology honestly framed in Q3.9.f; **Q3.9.e SUBSTANTIVE Strand-A first-pass at Q4.9 subjective<->objective coupling** -- Spearman rho vs key Garmin sister channels.
- **Computed directly from `per_day_master.csv`**: Q3.9.a (distribution shape + per-value frequency + Shannon entropy for bounded integer scale), Q3.9.b (Politis-White E[L]\* on Stratum-4 pool), Q3.9.c (per-phase base rates + recovery_arc v2 overlap), Q3.9.d (phase-stratified medians + HA-C3 v2 + HA-C3p cross-reference), Q3.9.e (SUBSTANTIVE: Spearman rho vs 5 primary + 10 extended Garmin sister channels), Q3.9.f (tautological day-level read + non-tautological episode-level min + dip + score-floor verification), Q3.9.g (drop primitive distribution + HA11 family clarification), Q3.9.h (coverage / missingness on bounded scale), Q3.9.i (covariate-sensitivity readiness for future HA using gevoelscore as outcome).
- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) (`compute_data_driven_block_length`).
- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

## Result

Headline (see [`findings.md`](findings.md) for the full answers Q3.9.a-i):

`gevoelscore` on Stratum 4 is a **bounded 1-6 INTEGER felt-state outcome channel** (skew -0.71; heavy_tail_flag=False; Shannon entropy 69.6% of log-6 ceiling). **Data-driven E[L]\*=15.1** (Politis-White; vs project default E[L]=7). **Phase-stratified medians** (citalopram axis): unmedicated 4.0 -> buildup 4.0 -> consolidation 5.0 -> afbouw 5.0. **Q3.9.e SUBSTANTIVE (subjective<->objective coupling)**: top-tracking Garmin sister channel is `stress_mean_sleep` (Spearman rho = -0.194); weakest is `bb_lowest` (rho = +0.010) -- Strand-A first-pass at Q4.9 territory; descriptive only, no causal interpretation per CONVENTIONS section 4.1. **Q3.9.f crash-vs-normal is TAUTOLOGICAL** by crash_v2-definition section 2.1 (crashes are by-definition score <= 3 days; max crash score = 4; n score-4 days inside merged crash episodes per merge rule sec 2.1.b = 5). HA-C3 v2 + HA-C3p outcome-side inverted-U descriptively corroborated from the gevoelscore distribution side.

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering Q3.9.a-i + tables (programmatically emitted by run.py from summary.json per the Q3.5/Q3.6/Q3.7/Q3.8 architectural note about the Write-tool harness heuristic on the literal filename "findings")
- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 6 PNGs: per-value frequency, phase-stratified stacked bar, trajectory-with-phases, Q3.9.e Spearman scatter, ACF, drop primitive distribution (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-05 corpus + 2026-06-25 analysis** (commit context: post-`92d7193` Q3.8 push_burden_7d LANDED; Phase 2 'finish the descriptive analysis' Tier 2 batch 5th of 5 channels; **CLOSES TIER 2** of user-prioritised Phase 2 batch). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg using gevoelscore as outcome is about to spin up beyond the HA-C3 v2 / HA-C3p locked operands.
2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).
3. Politis-White E[L]\* shifts by another factor of 2 from current 15.1.
4. crash_v2-definition is revised (current state: LOCKED; revision would warrant a Q3.9 refresh + careful re-derivation across all downstream HA tests).
5. Strand-B Q4.9 subjective<->objective coupling analysis is spun up (this Q3.9.e is a partial first-pass; Q4.9 would extend with per-phase + lagged + episode-level coupling + pre-crash divergence patterns).

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`); section 3.4 lists `gevoelscore (almost every test's outcome side)` under HA-touched non-confirmed candidate channels; section 4.9 deferred Q4.9 subjective<->objective coupling -- this Q3.9.e is a partial Strand-A first-pass.
- **LOAD-BEARING outcome-side substantive references**: [`HA-C3/result.md`](../../../analyses/hypotheses/HA-C3/result.md) (LOCKED REJECTED wrong-direction override) + [`HA-C3p/result.md`](../../../analyses/hypotheses/HA-C3p/result.md) (LOCKED PARTIAL 2-of-3); joint inverted-U finding descriptively corroborated from the outcome side in Q3.9.a + Q3.9.d + Q3.9.e.
- **LOCKED gevoelscore-to-crash mapping**: [`crash_v2-definition/`](../../../analyses/hypotheses/crash_v2-definition/) -- the canonical definitional substrate this Q3.9 characterises; NOT modified per handoff section 3 hard constraint. Q3.9.f surfaces the day-level tautology honestly.
- **Recovery_arc v2 6-phase characterisation**: [`trajectory/recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) (LOCKED) -- Q3.9.c provides overlap notation per handoff section 2.4 'check overlap; do NOT re-characterise'.
- **Q3.8 most-recent Tier 2 precedent (count-primitive sister)**: [`descriptive/operationalisation_support/push_burden_7d/`](../push_burden_7d/) -- Tier 2 4th of 5; LANDED `92d7193`; clean programmatic-emit + bounded-integer-support precedent.
- **Q3.7 categorical adaptation precedent**: [`descriptive/operationalisation_support/exertion_class/`](../exertion_class/) -- Tier 2 3rd of 5; non-continuous channel adaptation pattern.
- **Q3.6 continuous-channel precedent**: [`descriptive/operationalisation_support/resting_hr/`](../resting_hr/) -- Tier 2 2nd of 5; clean programmatic-emit + f-string discipline.
- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) -- HA11 row referenced in Q3.9.g for the within-day stress U-dip clarification.
- **HA-* tests that this analysis anchors (outcome-side)**:
  - **HA-C3 v2** + **HA-C3p**: direct outcome operands (joint inverted-U finding).
  - **HA10 + HA07d + many other HAs**: indirect outcome via crash_v2-definition.
- **Methodology MDs**: `citalopram_phase_stratification.md`, `permutation_null_block_length.md`, `lc_era_temporal_segmentation.md` (Stratum 4 IS the gevoelscore-having days), `lc_recovery_phase_axis.md` (Q3.9.c 6-phase overlap notation), `_descriptive_stocktake_2026-06-23.md` (gap-list framing).
- **Upstream pipeline**: `per_day_master.csv` `gevoelscore` column <- `pipeline/03_consolidate/build_unified_dataset.py` <- app-side self-report on 1-10 scale (empirical range 1-6). `labels_crash_v2.csv` per locked `crash_v2-definition`.
