# Findings -- `exertion_class` operationalisation-support descriptive (Q3.7.a-i)

**Channel**: `exertion_class` (HA01b-recomputed + HA01b-per-axis-diagnostic + HA01c primary operand; HA-C4c heavy-T classifier substrate via the lagged variant; per-day categorical 5-level ordinal {none, light, moderate, heavy, very_heavy} derived from steps + moderate-VPA + Garmin activity-labels per [`analyses/garmin_exploration/activity-labels/definition.md`](../../../analyses/garmin_exploration/activity-labels/definition.md)). Column semantics: [DATA_DICTIONARY.md activity-axis section](../../../DATA_DICTIONARY.md).

**Substantive context**: HA01b-recomputed (v3.2 lagged baseline) is LOCKED REFUTED both eras (train +5.8 pp / validate +4.0 pp); R14 single-pool **+5.1 pp [-14.7, +13.3] perm p (E[L]=7) = 0.3689 NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED)** per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) row HA01b-recomputed. HA01b-per-axis-diagnostic SUPPORTED both eras at locked tau=0.75 per cell; load-bearing WITHHELD due to v2 threshold-monotonicity-diagnostic AMBIGUOUS. HA01c-effective-exertion-shock SUPPORTED both eras (train +21.3 / validate +19.5) at locked tau=0.75; also load-bearing WITHHELD per the same v2 diagnostic ambiguity per [REJECTED.md HA01c row](../../../REJECTED.md). HA-C4c (LANDED PARTIAL `a69a8ed`) uses `exertion_class_lagged_lcera in {heavy, very_heavy}` as the heavy-T classifier per [HA-C4c hypothesis.md section 4.1](../../../analyses/hypotheses/HA-C4c/hypothesis.md); the un-lagged primary `exertion_class` (this Q3.7 scope) is the underlying raw 5-level signal.

**v3.1 -> v3.2 lagged-baseline correction context**: per [REJECTED.md HA01b-recomputed](../../../REJECTED.md) + [CONVENTIONS section 3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses): the original HA01b validate +17.3 pp 'first SUPPORTED' headline was a v3.1 rolling-baseline artefact that did NOT survive v3.2 lagged-baseline recomputation (softened by -13.3 pp to +4.0 pp). This is the **canonical project example of why lagged-baseline matters** per CONVENTIONS section 3.2. Q3.7.b autocorrelation discussion below cites descriptively; this Q3.7 is on the **un-lagged primary** `exertion_class` and does NOT re-litigate the v3.1 -> v3.2 correction per handoff section 3 hard constraint.

**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to 2026-06-05). n=1372 days with channel out of 1372 Stratum 4 days (0 NaN days).

**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- HA-touched non-confirmed channel candidate list bullet `exertion_class + push_burden_7d (HA01b/HA01c primaries) -- partially covered by activity-labels/`. **3rd of the 5 Tier 2 channels** in the user-prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; Tier 2 2nd = Q3.6 resting_hr `5d28219`; this Q3.7 closes Tier 2 3rd; next: Q3.8 push_burden_7d, Q3.9 gevoelscore). **Q3.7.a-i template applied with explicit CATEGORICAL ADAPTATIONS** documented per question (per handoff section 1 + the stress_low_motion_min_count_S60_Mlow count-primitive adaptation precedent).

**Sources**: `per_day_master.csv` (exertion_class column derived from activity-axis upstream extractor) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per CONVENTIONS section 3.6).

**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). HA01b-recomputed + HA01b-per-axis-diagnostic + HA01c + HA-C4c (LOCKED) + R14 single-pool re-anchor (LOCKED `badd04a`) cross-references in this analysis are **descriptive corroboration only**; the substantive verdicts live in those result.md files and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). The v3.1 -> v3.2 lagged-baseline correction is descriptively cited in Q3.7.b per handoff section 2.4; NOT re-litigated. Statistical hygiene anchors: section 3.1 (personal baseline), section 3.2 (lagged-baseline discipline; this analysis is on the un-lagged primary by handoff scope), section 3.3 (column-duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity |delta|>0.10), section 3.5 (spike metrics -- heavy/very_heavy class fraction IS the spike-form on this categorical channel), section 3.6 (named counts).

---

## Headline

`exertion_class` on Stratum 4 is a **5-level categorical activity-axis channel** (distribution: none 25.3%, light 23.7%, moderate 16.0%, heavy 17.8%, very_heavy 17.2%; Shannon entropy = 1.592 nats = 98.9% of max log(5)=1.609; heavy+very_heavy spike-class fraction = 35.0%; at-rest none-class fraction = 25.3%). **Data-driven E[L]\*=7.0 on ordinal-encoded series** (Politis-White; cutoff lag M=1; factor-of-2 flag=False; day-to-day transition rate = 77.0%; same-class persistence rate = 23.0%). **Per-phase frequency shifts** (citalopram axis): chi-square(df=12) = 11.99, p=0.4466; per-phase heavy+very_heavy fraction unmedicated 36.1% -> consolidation 33.5% -> afbouw 34.6%. **Crash-vs-normal**: chi-square 2x5 = 5.03 p=0.2836; Mann-Whitney U on ordinal encoding z=-1.94 p=0.0527 P(crash > normal) = 0.444; heavy+very_heavy fraction crash 25.2% vs normal 35.8% (diff -10.5%); none fraction crash 29.1% vs normal 25.0% (diff +4.1%); ordinal median diff = -1.0 -- descriptively re-anchors HA01b-recomputed locked-REFUTED + R14 +5.1 pp NOT-SUPPORTED and HA01c locked-SUPPORTED-load-bearing-WITHHELD signals at the un-lagged-primary day-level read (HA01b/HA01c tested operand is on the v3.2 lagged variant; this Q3.7.f is the first-order day-level descriptive complement). Near-identity check: **Zero** pair(s) fire at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. **Spike-form**: heavy+very_heavy burst-rate (>=2 spike days in trailing 7d) = 73.9% of days; max consecutive heavy/very_heavy run = 5 days; HA-C4c uses the lagged variant for its heavy-T classifier.

---

## Q3.7.a -- Distribution shape (Stratum 4) -- CATEGORICAL ADAPTATION

**CATEGORICAL ADAPTATION**: The distribution-shape primitive IS the per-category frequency vector + marginal Shannon entropy (instead of mean/median/skewness applicable to continuous channels). Ordinal-encoded mean/median reported as auxiliary summaries (the channel has natural ordering none < light < moderate < heavy < very_heavy). No heavy-tail flag (not meaningful on a 5-level ordinal); rare-class flag (any class < 5%) used instead.

### Per-category frequencies

| category | n | frequency |
|---|---:|---:|
| none | 347 | 25.3% |
| light | 325 | 23.7% |
| moderate | 220 | 16.0% |
| heavy | 244 | 17.8% |
| very_heavy | 236 | 17.2% |
| **total** | **1372** | **100%** |

### Entropy + auxiliary ordinal summaries

| stat | value | source |
|---|---:|---|
| n (Stratum 4) | 1372 | `per_day_master.csv` `exertion_class` non-NaN within S4 |
| Shannon entropy (nats) | **1.592** | -sum p log p over 5 categories |
| Max entropy log(5) | 1.609 | uniform 5-class baseline |
| Normalised entropy | **98.9%** | observed / log(5); near 100% = near-uniform |
| Ordinal mean (none=0, ..., very_heavy=4) | 1.779 | auxiliary summary on ordinal encoding |
| Ordinal median | 2.0 | auxiliary summary on ordinal encoding |
| Ordinal mode | **none** | most-frequent category |
| heavy + very_heavy fraction (spike-class) | **35.0%** | binary collapse for Q3.7.g spike-form |
| none fraction (at-rest class) | **25.3%** | |
| min category frequency | 16.0% | rare-class flag if < 5% |
| max category frequency | 25.3% | |
| rare-class flag (any class < 5%) | **False** | CATEGORICAL ADAPTATION equivalent of heavy-tail flag |

**Interpretation**: the 5-level distribution is **near-uniform across 5 classes** (normalised entropy 98.9%); the **spike-class (heavy + very_heavy) covers 35.0% of days** on Stratum 4 -- this fraction is the rate that drives HA01b-recomputed's operand (frac windows with >=1 day in 4-day leadup at lagged-class in {heavy, very_heavy}) on the lagged variant. The **at-rest class (none) covers 25.3%** -- the complement-rate informative for any future HA pre-reg operationalising 'low-activity day' on this channel.

See [`plots/fig1_per_category_frequency_s4.png`](plots/fig1_per_category_frequency_s4.png).

---

## Q3.7.b -- Autocorrelation structure -- CATEGORICAL ADAPTATION + v3.1 -> v3.2 lagged-baseline correction citation

**CATEGORICAL ADAPTATION**: Politis-White E[L]\* computed on the **ordinal-encoded series** (none=0, light=1, moderate=2, heavy=3, very_heavy=4); transition-rate analysis (P(state_t != state_{t-1})) reported alongside as the additional categorical autocorrelation primitive distinct from the ordinal-encoded ACF (which leverages the ordering).

### Ordinal-encoded ACF + Politis-White E[L]\*

The **data-driven block length is E[L]\*=7.0** (Politis-White 2004 with Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The **factor-of-2 deviation flag = False** (deviation ratio = 0.00). Cutoff lag M=1.

| lag (days) | autocorrelation (ordinal) |
|---:|---:|
| 1 | +0.050 |
| 2 | +0.087 |
| 3 | +0.009 |
| 7 | +0.029 |
| 14 | +0.015 |

Politis-White 2-sigma significance threshold (n=1372): |rho| = 0.145.

### Transition-rate analysis (categorical autocorrelation primitive)

Over **1371** consecutive-day pairs in Stratum 4: **1055 transitions** (day-over-day class change). **Transition rate P(state_t != state_{t-1}) = 77.0%** (equivalently, same-class persistence rate = 23.0%). Per-class previous-day persistence (P(state_t = c | state_{t-1} = c)):

| previous-day class | n prev in class | next-day same-class count | next-day same-class rate |
|---|---:|---:|---:|
| `none` | 346 | 118 | 34.1% |
| `light` | 325 | 73 | 22.5% |
| `moderate` | 220 | 34 | 15.5% |
| `heavy` | 244 | 52 | 21.3% |
| `very_heavy` | 236 | 39 | 16.5% |

### v3.1 -> v3.2 lagged-baseline correction descriptive citation (per handoff section 2.4)

Per [CONVENTIONS section 3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) + [REJECTED.md HA01b-recomputed](../../../REJECTED.md): the v3.1 `exertion_class` uses a 30-day **trailing rolling baseline that includes the candidate day itself**. In sustained-push periods the baseline creeps up with the pushes and a slow grind rebases into its own reference frame and stops looking heavy. v3.2 fixes this with a `[d-90, d-30]` window. The `_lagged_lcera` variant additionally restricts the baseline to LC-era days only.

The original HA01b validate +17.3 pp 'first SUPPORTED' headline was substantially a v3.1 rolling-baseline artefact; HA01b-recomputed (v3.2 lagged) showed **REFUTED both eras** (train +5.8 pp / validate +4.0 pp); the delta vs original validate was **-13.3 pp**. This is the **canonical project example of why lagged-baseline matters** per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed.

**This Q3.7.b autocorrelation analysis is on the un-lagged primary `exertion_class`** (NOT on the rolling-baseline-derived pre-classifier signal -- the categorical class IS the downstream operand of the v3.1 classifier). The autocorrelation observed here characterises the raw categorical day-to-day class signal AS-IS; per handoff section 3 hard constraint, this analysis does **NOT re-litigate the v3.1 -> v3.2 correction**. The lagged variants `exertion_class_lagged` + `exertion_class_lagged_lcera` are out of Strand-A scope per handoff section 1; any future HA pre-reg on this channel should default to the v3.2 lagged variant per CONVENTIONS section 3.2 audit hook.

See [`plots/fig5_acf_ordinal.png`](plots/fig5_acf_ordinal.png).

---

## Q3.7.c -- Base rates per citalopram phase -- CATEGORICAL ADAPTATION

**CATEGORICAL ADAPTATION**: Per-phase per-category frequency distribution + per-phase Shannon entropy (instead of per-phase median + dispersion as in continuous templates). Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3:

| phase (window) | n | none | light | moderate | heavy | very_heavy |
|---|---:|---|---|---|---|---|
| unmedicated (2022-09-03 to 2024-04-08) | 584 | 134 (22.9%) | 141 (24.1%) | 98 (16.8%) | 98 (16.8%) | 113 (19.3%) |
| buildup (2024-04-09 to 2024-06-19) | 72 | 16 (22.2%) | 21 (29.2%) | 7 (9.7%) | 13 (18.1%) | 15 (20.8%) |
| consolidation (2024-06-20 to 2026-03-19) | 638 | 175 (27.4%) | 148 (23.2%) | 101 (15.8%) | 120 (18.8%) | 94 (14.7%) |
| afbouw (2026-03-20 to 2026-06-05) | 78 | 22 (28.2%) | 15 (19.2%) | 14 (17.9%) | 13 (16.7%) | 14 (17.9%) |

### Per-phase summary statistics

| phase | n | heavy+very_heavy fraction | none fraction | ordinal median | Shannon entropy (nats) |
|---|---:|---:|---:|---:|---:|
| unmedicated | 584 | **36.1%** | 22.9% | 2.0 | 1.598 |
| buildup | 72 | **38.9%** | 22.2% | 1.0 | 1.556 |
| consolidation | 638 | **33.5%** | 27.4% | 1.0 | 1.582 |
| afbouw | 78 | **34.6%** | 28.2% | 2.0 | 1.589 |

The two **transition phases** (buildup n=72; afbouw n=78) have **n<75 each**; the two **steady-state phases** (unmedicated n=584; consolidation n=638) are an order of magnitude larger. Any HA test that wants per-phase verdicts on this channel faces a ~10x n disadvantage vs the steady-state phases (same pattern as sister channels Q3.1.c / ... / Q3.6.c).

Named counts (CONVENTIONS section 3.6): the per-phase per-category n's above are `exertion_class`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per `citalopram_phase_stratification.md section 3` boundary dates.

See [`plots/fig2_phase_stratified_stacked_bar.png`](plots/fig2_phase_stratified_stacked_bar.png) (citalopram-phase stacked-frequency bars).

---

## Q3.7.d -- Phase-stratified distribution + chi-square test -- CATEGORICAL ADAPTATION

**CATEGORICAL ADAPTATION**: Per handoff section 1 + CONVENTIONS section 4.2: phase shift primitive IS per-phase per-category frequency vector + entropy (instead of mean/median delta as in continuous-channel templates Q3.1.d ... Q3.6.d). Chi-square test of independence (4 phases x 5 categories) is the global-null descriptive indicator; pairwise per-category frequency deltas are the per-pair descriptive details.

### Global chi-square test of independence

| stat | value |
|---|---:|
| Chi-square statistic | **11.99** |
| Degrees of freedom | 12 |
| p-value (Wilson-Hilferty approx) | **0.4466** |

**Descriptive reading**: the chi-square p-value is a nominal-null indicator only (CONVENTIONS section 4.2). Per handoff section 1 + 3 hard constraint: this Q3.7.d does NOT promote a substantive HA verdict; observed phase shifts may reflect (i) genuine activity-pattern change, (ii) categorical-boundary calibration drift on the v3.1 rolling-baseline definition of the upstream classifier per CONVENTIONS section 3.2, or (iii) co-temporal trajectory effects. The lagged variants `exertion_class_lagged` + `exertion_class_lagged_lcera` are out of Strand-A scope per handoff section 1; this Q3.7.d characterises the un-lagged primary as-is.

### Pairwise frequency shifts (per category, between selected phase pairs)

**consolidation minus unmedicated** (frequency-points):

| category | delta frequency (pp) |
|---|---:|
| `none` | **+4.5%** |
| `light` | **-0.9%** |
| `moderate` | **-1.0%** |
| `heavy` | **+2.0%** |
| `very_heavy` | **-4.6%** |

**afbouw minus consolidation** (frequency-points):

| category | delta frequency (pp) |
|---|---:|
| `none` | **+0.8%** |
| `light` | **-4.0%** |
| `moderate` | **+2.1%** |
| `heavy` | **-2.1%** |
| `very_heavy` | **+3.2%** |

**afbouw minus unmedicated** (frequency-points):

| category | delta frequency (pp) |
|---|---:|
| `none` | **+5.3%** |
| `light` | **-4.9%** |
| `moderate` | **+1.2%** |
| `heavy` | **-0.1%** |
| `very_heavy` | **-1.4%** |

### HA01b-recomputed + HA01c + HA-C4c locked-verdict cross-reference

Per handoff section 1 + section 2.4 + section 3 hard constraint: HA01b-recomputed (v3.2 lagged baseline) LOCKED REFUTED both eras (train +5.8 / validate +4.0 pp); R14 single-pool +5.1 pp [-14.7, +13.3] perm p=0.3689 NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED). HA01b-per-axis-diagnostic SUPPORTED both eras at locked tau=0.75 per cell; load-bearing WITHHELD due to v2 threshold-monotonicity-diagnostic AMBIGUOUS. HA01c SUPPORTED both eras at locked tau=0.75 (train +21.3 / validate +19.5); also load-bearing WITHHELD per the same v2 diagnostic ambiguity. HA-C4c (LANDED PARTIAL `a69a8ed`) uses the lagged variant `exertion_class_lagged_lcera in {heavy, very_heavy}` as the heavy-T classifier on T; the cross-phase pooled with bar (b) failing per HA-C4c result.md. These are LOCKED and the observed phase shifts in Q3.7.d above are NOT a re-interpretation per CONVENTIONS section 4.2.

See [`plots/fig2_phase_stratified_stacked_bar.png`](plots/fig2_phase_stratified_stacked_bar.png) (stacked bars) and [`plots/fig3_monthly_rate_trajectory.png`](plots/fig3_monthly_rate_trajectory.png) (monthly heavy+very_heavy and none rate trajectory across the multi-year window).

---

## Q3.7.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3) -- CATEGORICAL ADAPTATION

**CATEGORICAL ADAPTATION**: Spearman on ordinal-encoded primary vs continuous-form activity-axis sibling primitives. The two lagged categorical variants (`exertion_class_lagged` + `exertion_class_lagged_lcera`) are ordinal-encoded with the same 5-level mapping; expected high rho with the un-lagged primary by construction since they share the underlying classifier with shifted baseline windows. Per CONVENTIONS section 3.3: threshold is |rho|>=0.92. Per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed: downstream PEM-pacing consumers prefer the v3.2 lagged variant; any near-identity between un-lagged primary and a lagged variant reflects categorical-classifier overlap, NOT operand equivalence (the baseline window differs).

| target channel | n | Pearson r | Spearman rho | near-identity flag? |
|---|---:|---:|---:|---|
| `exertion_class_lagged` (categorical sibling) | 1372 | +0.859 | +0.860 | no |
| `exertion_class_lagged_lcera` (categorical sibling) | 1372 | +0.859 | +0.860 | no |
| `effective_exertion_min` | 1372 | +0.505 | +0.696 | no |
| `eff_exertion_rank_lagged` | 1372 | +0.718 | +0.706 | no |
| `eff_exertion_rank_lagged_lcera` | 1372 | +0.718 | +0.706 | no |
| `exertion_rank_composite_lagged` | 1372 | +0.852 | +0.875 | no |
| `exertion_rank_composite_lagged_lcera` | 1372 | +0.852 | +0.875 | no |
| `effective_exertion_slope_28d` | 1372 | +0.059 | +0.058 | no |
| `push_burden_7d` | -- | -- | -- | column absent |
| `step_z_30d` | 1358 | +0.652 | +0.661 | no |
| `steps_total` | -- | -- | -- | column absent |
| `steps` | -- | -- | -- | column absent |
| `mvpa_minutes` | -- | -- | -- | column absent |
| `moderate_intensity_minutes` | -- | -- | -- | column absent |
| `vigorous_intensity_minutes` | -- | -- | -- | column absent |

**Zero** near-identity pair(s) fire at the |rho|>=0.92 CONVENTIONS section 3.3 threshold.

**Note**: any near-identity flag on the lagged variants is *expected* by construction (same classifier with shifted baseline window) and is **not a duplication finding** -- the operand differs even when the categorical encoding correlates highly. Per CONVENTIONS section 3.2 audit hook: any draft analysis touching `exertion_class` (un-lagged) must stop and ask whether the v3.2 lagged variant is what's meant; this Q3.7.e quantifies the operand-overlap rho descriptively.

---

## Q3.7.f -- Crash-day vs normal-day (Stratum 4) -- CATEGORICAL ADAPTATION + R14 HA01b-recomputed cross-reference

**CATEGORICAL ADAPTATION**: Per handoff section 1 + section 2.4: chi-square 2x5 (crash x normal x 5 categories) AND Mann-Whitney U on ordinal encoding both reported (per handoff section 1 'chi-square or Mann-Whitney U on ordinal encoding for crash-vs-normal'); Cohen's d computed on ordinal encoding for parity with sister continuous Strand-A analyses (the rank-biserial r is also defensible on ordinal data; Cohen's d reported for cross-analysis consistency). Heavy+very_heavy spike-class fraction shift IS the spike-form crash-vs-normal primitive on this categorical channel.

Per CONVENTIONS section 3.6 named counts: **29** crash-episodes (crash_v2 episode-level via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); **103** crash-days (day-level, `label=='crash'`); **1269** non-crash days (the complement within Stratum 4 channel-valid days).

### Day-level per-category frequencies (crash vs normal)

| category | crash freq | normal freq | crash minus normal (pp) |
|---|---:|---:|---:|
| `none` | 29.1% | 25.0% | **+4.1%** |
| `light` | 27.2% | 23.4% | **+3.8%** |
| `moderate` | 18.4% | 15.8% | **+2.6%** |
| `heavy` | 14.6% | 18.0% | **-3.5%** |
| `very_heavy` | 10.7% | 17.7% | **-7.1%** |

### Day-level shifts on collapsed bins + ordinal-encoded summaries

| stat | value |
|---|---:|
| heavy + very_heavy fraction crash | **25.2%** |
| heavy + very_heavy fraction normal | **35.8%** |
| diff (crash minus normal) | **-10.5%** |
| none fraction crash | **29.1%** |
| none fraction normal | **25.0%** |
| diff (crash minus normal) | **+4.1%** |
| ordinal mean diff (crash - normal) | **-0.297** |
| ordinal median diff (crash - normal) | **-1.0** |

### Chi-square 2x5 (crash x normal x 5 categories)

| stat | value |
|---|---:|
| Chi-square statistic | **5.03** |
| Degrees of freedom | 4 |
| p-value (Wilson-Hilferty approx) | **0.2836** |

### Mann-Whitney U on ordinal encoding

| stat | value |
|---|---:|
| U (crash as first sample) | 58028.5 |
| z (normal approx, tie-corrected) | **-1.94** |
| p (two-sided) | **0.0527** |
| P(crash > normal) | **0.444** |

### Episode-level (per CONVENTIONS section 3.6)

| stat | value |
|---|---:|
| n crash-episodes | 29 |
| n normal-day base rate | 1269 |
| mean per-episode ordinal value | 1.472 |
| mean normal-day ordinal value | 1.801 |
| mean diff (episode minus normal-day) | **-0.329** |
| Cohen's d (episode-level vs normal-day pooled, ordinal-encoded) | **-0.23** |
| Bootstrap 95% CI on mean diff (ordinal) | **[-0.676, +0.029]** (5000 iters, seed=20260624) |

### LOAD-BEARING HA01b-recomputed R14 single-pool + HA01c locked descriptive cross-reference (per handoff section 2.4)

Per [single_pool_reanchor/findings.md](../single_pool_reanchor/findings.md) row HA01b-recomputed: R14 single-pool **+5.1 pp [CI -14.7, +13.3] perm p=0.3689 NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED)** (`badd04a`). Per [REJECTED.md HA01c](../../../REJECTED.md): HA01c SUPPORTED both eras at locked tau=0.75 (train +21.3 / validate +19.5); load-bearing WITHHELD due to v2 threshold-monotonicity-diagnostic AMBIGUOUS. This Q3.7.f's day-level chi-square + Mann-Whitney U + episode-level Cohen's d on the un-lagged primary **descriptively re-anchor** the HA01b-recomputed locked-REFUTED + R14 NOT-SUPPORTED signal and the HA01c locked-SUPPORTED-load-bearing-WITHHELD signal at the first-order day-level read on the categorical primary -- the HA tests use the v3.2 lagged variant operand (exertion_class_lagged in {heavy, very_heavy} OR eff_exertion_rank_lagged at tau=0.75); this Q3.7.f reports the day-level descriptive complement on the un-lagged categorical primary. **The HA01b-recomputed + HA01b-per-axis-diagnostic + HA01c + R14 single-pool substantive verdicts are LOCKED**; this Q3.7.f observation is descriptive corroboration only, NOT a re-interpretation of either, and NOT a re-litigation of the v3.1 -> v3.2 correction (Q3.7.b citation is the descriptive cite per handoff section 2.4).

### Crash-drop sensitivity (CONVENTIONS section 3.4) on Spearman vs gevoelscore (ordinal-encoded)

| frame | Spearman rho (ordinal vs gevoelscore) | n |
|---|---:|---:|
| full Stratum 4 | +0.086 | 1372 |
| crash-days dropped | +0.070 | 1269 |
| \|delta\| | **0.017** | -- |
| section 3.4 threshold (0.10) crossed? | **no** | -- |

See [`plots/fig4_crash_vs_normal_per_category.png`](plots/fig4_crash_vs_normal_per_category.png).

---

## Q3.7.g -- Spike-detecting primitive availability -- CATEGORICAL ADAPTATION + HA-C4c heavy-T classifier framing

**CATEGORICAL ADAPTATION**: Per handoff section 1 + CONVENTIONS section 3.5 spike metrics: the spike-form on a 5-level ordinal channel is the **heavy/very_heavy class fraction** (rare-class point primitive) + the **within-7d burst-rate** (sustained-exertion primitive). These mirror the spike-form for count primitives (stress_low_motion_min_count_S60_Mlow Q3.4.g) and the per-4-day MAX |z| spike-form for daily-aggregate continuous channels (resting_hr Q3.6.g). Per CONVENTIONS section 3.5: this categorical spike-form IS the operationalisation substrate for HA-C4c's heavy-T classifier construct on the lagged variant.

### Spike-class point primitive

| stat | value |
|---|---:|
| n heavy/very_heavy spike days | 480 |
| heavy + very_heavy day rate | **35.0%** |
| n very_heavy days (extreme tail) | 236 |
| very_heavy day rate | 17.2% |

### Within-7d burst-rate primitive

| stat | value |
|---|---:|
| burst-rate (>=2 spike days in trailing 7d) | **73.9%** |
| burst-rate (>=3 spike days in trailing 7d) | 47.4% |

### Consecutive heavy/very_heavy run distribution

| stat | value |
|---|---:|
| n runs | 303 |
| max run length (days) | **5** |
| median run length (days) | 1.0 |
| mean run length (days) | 1.58 |

### HA-C4c heavy-T classifier framing (per handoff section 2.4)

Per [HA-C4c hypothesis.md section 4.1](../../../analyses/hypotheses/HA-C4c/hypothesis.md) (LANDED PARTIAL `a69a8ed`): HA-C4c uses **`exertion_class_lagged_lcera in {heavy, very_heavy}` on T as the heavy-T classifier**. The un-lagged primary `exertion_class` (this Q3.7 scope) is the underlying raw 5-level signal; the lagged variant applies the lagged-baseline correction per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed canonical example (the v3.2 _lagged_lcera form uses a [d-90, d-30] window restricted to LC-era days). Coverage within LC era ~83% per HA-C4c hypothesis.md section 4.4. **Per handoff section 3 hard constraint**: HA-C4c result is LOCKED PARTIAL (cross-phase pooled with bar (b) failing); this Q3.7.g does **NOT extend or re-anchor HA-C4c** -- the substrate characterisation here is descriptive only.

Lagged variant coverage in master:

- `exertion_class_lagged`: n non-NaN = 1372 / total 1372 (100.0%)
- `exertion_class_lagged_lcera`: n non-NaN = 1372 / total 1372 (100.0%)

---

## Q3.7.h -- Outlier detection + calibration-drift check -- CATEGORICAL ADAPTATION + activity-labels partial-coverage xref

**CATEGORICAL ADAPTATION**: Per handoff section 1: outlier semantics differ for categorical channels -- no MAD-z applicable (the channel is a 5-level ordinal, not a continuous magnitude). The categorical-equivalent diagnostics are (i) rare-class flag (any class < 5%) reported in Q3.7.a, (ii) per-month rate-drift snapshots for the rare-class (very_heavy) and the spike-class (heavy/very_heavy combined) reported below, and (iii) boundary-step reads at the citalopram phase boundaries (where a categorical-classifier calibration drift would surface as a step change in class frequencies).

### activity-labels partial-coverage descriptive cross-reference (per handoff section 2.4)

Per [`garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/): existing primitive-validation + visualisation runs on this channel family (definition.md severity cutoffs + scripts/ produced ha_results_4day_lagged.md). **Coverage is PARTIAL** per descriptive README section 3.4: the existing artefact does primitive-spec + HA-test validation but does NOT cover the Q3.x.a-i operationalisation-support per-channel template. This Q3.7 provides the per-channel substrate the activity-labels artefact does NOT have. Per activity-labels/definition.md (cited descriptively): 'severity cutoffs for exertion_class are NOT locked' -- this is the upstream-classifier discipline note. Q3.7.h's per-month rate-drift snapshots below characterise the categorical-distribution stability AS-IS for the v3.1 un-lagged primary; any calibration-drift signature in the snapshot table is a Layer 1 descriptive observation, NOT a re-promotion of the v3.1 cutoff lock per handoff section 3 hard constraint.

### Per-month rate snapshots (selected; full table available in summary.json)

| year_month | n | very_heavy rate | heavy+very_heavy rate | none rate |
|---|---:|---:|---:|---:|
| 2022-09 | 28 | 14.3% | 32.1% | 17.9% |
| 2022-12 | 31 | 12.9% | 32.3% | 32.3% |
| 2023-03 | 31 | 12.9% | 48.4% | 22.6% |
| 2023-06 | 30 | 20.0% | 36.7% | 16.7% |
| 2023-09 | 30 | 30.0% | 46.7% | 26.7% |
| 2023-12 | 31 | 16.1% | 35.5% | 29.0% |
| 2024-03 | 31 | 16.1% | 29.0% | 16.1% |
| 2024-06 | 30 | 13.3% | 30.0% | 13.3% |
| 2024-09 | 30 | 10.0% | 30.0% | 13.3% |
| 2024-12 | 31 | 19.4% | 35.5% | 3.2% |
| 2025-03 | 31 | 9.7% | 29.0% | 38.7% |
| 2025-06 | 30 | 10.0% | 46.7% | 26.7% |
| 2025-09 | 30 | 6.7% | 16.7% | 53.3% |
| 2025-12 | 31 | 9.7% | 35.5% | 25.8% |
| 2026-03 | 31 | 19.4% | 48.4% | 22.6% |
| 2026-06 | 5 | 0.0% | 0.0% | 100.0% |
| 2026-06 | 5 | 0.0% | 0.0% | 100.0% |

### Boundary-step reads (pre/post 30d at citalopram phase boundaries)

| boundary | n_pre | n_post | heavy+very_heavy rate pre | rate post | diff | none rate pre | rate post | diff |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| citalopram_boundary_2024_04_09 | 30 | 30 | 33.3% | 46.7% | **+13.3%** | 16.7% | 23.3% | **+6.7%** |
| consolidation_boundary_2024_06_20 | 30 | 30 | 33.3% | 36.7% | **+3.3%** | 20.0% | 26.7% | **+6.7%** |
| afbouw_boundary_2026_03_20 | 30 | 30 | 33.3% | 46.7% | **+13.3%** | 33.3% | 10.0% | **-23.3%** |

See [`plots/fig3_monthly_rate_trajectory.png`](plots/fig3_monthly_rate_trajectory.png) (monthly trajectory with citalopram-phase shading).

---

## Q3.7.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel

Discipline anchor: [HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) (secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and candidate alternative readings). Names **four** candidate covariates a future HA on `exertion_class` as predictor should pre-spec.

### 1. `exertion_class_lagged_lcera (v3.2 lagged variant; LC-era-restricted baseline window)`

Per CONVENTIONS section 3.2 lagged-baseline discipline + REJECTED.md HA01b-recomputed canonical example: any future HA on the un-lagged primary `exertion_class` should pre-spec the v3.2 lagged variant as a parallel-arm sensitivity check (the v3.1 -> v3.2 correction was load-bearing on HA01b's original validate +17.3 pp 'first SUPPORTED' headline that softened to +4.0 pp). If both arms produce concordant verdicts, the baseline-construction choice is not load-bearing; divergence is the load-bearing flag.

*Source*: CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed + analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md

### 2. `effective_exertion_min (continuous-form sibling)`

Per descriptive README section 3.4 + handoff section 1: the continuous-form sibling effective_exertion_min carries the pre-discretisation magnitude information that the 5-level categorical encoding compresses. The covariate disambiguates: beta_channel attenuates if the categorical encoding is just a coarsening of the continuous magnitude (the continuous form carries the signal); beta_channel survives if the categorical encoding carries discrete-class-boundary information beyond the continuous form (e.g. the heavy/very_heavy cutoff IS the operationally relevant boundary).

*Source*: DATA_DICTIONARY.md effective_exertion_min + descriptive README section 3.4 HA-touched candidates

*Observed Spearman rho on S4 (ordinal-encoded primary vs covariate)*: rho=+0.696 (n=1372).

### 3. `push_burden_7d (rolling 7d sustained-exertion sibling; HA02 family primary)`

Per descriptive README section 3.4 + Q3.7.g spike-form note: push_burden_7d captures the trailing 7d cumulative exertion while exertion_class is the per-day point measurement. The covariate disambiguates: beta_channel attenuates if same-day exertion is just a marker for ongoing accumulated burden (push_burden_7d carries the signal); beta_channel survives if the day-level class encodes acute-day information beyond the rolling burden.

*Source*: DATA_DICTIONARY.md push_burden_7d + descriptive README section 3.4

### 4. `resting_hr (cross-family cardiovascular anchor)`

Per Q3.6 sister analysis (resting_hr LANDED `5d28219`): cardiovascular state vs activity-axis state are conceptually distinct mechanisms. The covariate disambiguates: beta_channel attenuates if exertion-class signal is shared cardiovascular-tone (high RHR co-occurs with heavy exertion); beta_channel survives if exertion-class encodes activity-axis information beyond cardiovascular state.

*Source*: Q3.6 resting_hr Strand-A sister analysis

*Observed Spearman rho on S4 (ordinal-encoded primary vs covariate)*: rho=-0.026 (n=1357).

### Recommendation

Pre-spec all four covariates as secondary sensitivity arms. Covariate 1 (v3.2 lagged variant) is the CONVENTIONS section 3.2 audit-hook compliance covariate; covariates 2 + 3 are the within-family operationalisation disambiguators; covariate 4 is the cross-family cardiovascular disambiguator. Per CONVENTIONS section 3.2: any draft analysis touching un-lagged exertion_class MUST stop and ask whether the v3.2 lagged variant is what's meant -- this Q3.7.i covariate 1 operationalises that audit hook for downstream HA pre-regs.

---

## Cross-references

### HA-* tests that touch this channel (cite this analysis)

- **HA01b-recomputed** (v3.2 lagged composite at exertion_class_lagged in {heavy, very_heavy}; LOCKED REFUTED both eras +5.8 / +4.0 pp; R14 single-pool NOT-SUPPORTED CONVERGE `badd04a`): primary operand IS this channel on the **lagged** variant. **The descriptive substrate this analysis produces -- the per-category frequencies (Q3.7.a) + ordinal autocorrelation E[L]\*=7.0 + transition-rate 77.0% (Q3.7.b) + per-citalopram-phase frequency distribution + chi-square (Q3.7.c+d) + first-order day-level crash-vs-normal chi-square + Mann-Whitney U + per-class shifts (Q3.7.f) -- complements HA01b-recomputed's tested operand with the un-lagged categorical-channel distribution view.** The substantive HA01b-recomputed verdict + the R14 single-pool verdict are LOCKED; this analysis's descriptive corroboration in Q3.7.f is NOT a re-interpretation and NOT a re-litigation of the v3.1 -> v3.2 correction (descriptive citation only per Q3.7.b + handoff section 2.4).
- **HA01b-per-axis-diagnostic** (locked SUPPORTED both eras at tau=0.75 per cell; load-bearing WITHHELD due to v2 threshold-monotonicity-diagnostic AMBIGUOUS): the per-axis diagnostic operand reduces to this channel's per-category structure on the lagged variant; Q3.7.c+d descriptively characterise the un-lagged-primary per-phase structure.
- **HA01c-effective-exertion-shock** (locked SUPPORTED both eras at tau=0.75; load-bearing WITHHELD; uses eff_exertion_rank_lagged at tau=0.75): Q3.7.f day-level descriptively re-anchors at the un-lagged categorical-primary read.
- **HA-C4c** (LANDED PARTIAL `a69a8ed`; cross-phase pooled with bar (b) failing): uses `exertion_class_lagged_lcera in {heavy, very_heavy}` as the heavy-T classifier on T per hypothesis.md section 4.1; this Q3.7 characterises the un-lagged primary `exertion_class` as the underlying raw 5-level signal substrate.

### Methodology MDs cited

- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 -- Q3.7.c phase axis; Q3.7.d phase-stratified treatment.
- [`CONVENTIONS.md` section 3.2 lagged-baseline](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) + [`REJECTED.md` HA01b-recomputed row](../../../REJECTED.md) -- canonical project example of why lagged-baseline matters; cited descriptively in Q3.7.b (NOT re-litigated per handoff section 3 hard constraint).
- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule; Q3.7.b reports E[L]\*=7.0.
- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition.
- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- Q3.7.h cross-reference framing (the activity-axis classifier itself is upstream of UDS passthrough; Q3.7.h's per-month rate-drift snapshots are the categorical-equivalent calibration-drift diagnostic).

### Existing artefacts referenced

- [`analyses/garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/) **partial-coverage** descriptive cross-reference in Q3.7.h: existing primitive-spec + HA-test validation; does NOT cover Q3.x.a-i operationalisation-support per-channel template (this Q3.7 closes the gap).
- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) -- R14 HA01b-recomputed row (LANDED `badd04a`); descriptively corroborated in Q3.7.f.
- [`descriptive/operationalisation_support/resting_hr/findings.md`](../resting_hr/findings.md) -- Q3.6 most-recent Tier 2 precedent; programmatic-emit pattern + clean f-string discipline.
- [`descriptive/operationalisation_support/bb_overnight_gain/findings.md`](../bb_overnight_gain/findings.md) -- Q3.5 Tier 2 first precedent; coverage-discipline.
- [`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/findings.md`](../stress_low_motion_min_count_S60_Mlow/findings.md) -- Phase 1 third precedent; non-continuous primitive (count) adaptation precedent for this Q3.7's CATEGORICAL ADAPTATION discipline.
- [`analyses/hypotheses/HA-C4c/hypothesis.md`](../../../analyses/hypotheses/HA-C4c/hypothesis.md) -- heavy-T classifier framing cited in Q3.7.g (LANDED PARTIAL `a69a8ed`).
- [`REJECTED.md`](../../../REJECTED.md) HA01b-recomputed row -- canonical v3.1 -> v3.2 lagged-baseline correction example cited descriptively in Q3.7.b.

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- activity-axis upstream classifier producing exertion_class per `analyses/garmin_exploration/activity-labels/definition.md` severity cutoffs.
- `labels_crash_v2.csv` <- `analyses/hypotheses/crash_v2-definition/definition.md` (locked).

---

## Limitations

For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding constraints are:

1. **No HA verdict promotion**: HA01b-recomputed + HA01b-per-axis-diagnostic + HA01c + HA-C4c + R14 single-pool verdicts are LOCKED; this analysis's descriptive observations are NOT re-interpretations or re-promotions per CONVENTIONS section 4.2 + handoff section 3.
2. **No re-litigation of v3.1 -> v3.2 lagged-baseline correction** per handoff section 3 hard constraint. The Q3.7.b descriptive citation acknowledges the correction as the canonical project example per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed; the load-bearing correction story lives in those artefacts and is the canonical reference, NOT extended or restated here.
3. **Un-lagged primary scope per handoff section 1**: this Q3.7 covers the un-lagged primary `exertion_class` only; the lagged variants `exertion_class_lagged` + `exertion_class_lagged_lcera` are derivatives used in HA pre-reg contexts and are out of Strand-A scope. Any future HA pre-reg should default to the v3.2 lagged variant per CONVENTIONS section 3.2 audit hook (Q3.7.i covariate 1 operationalises that).
4. **Categorical adaptations explicitly documented per question** per handoff section 1 + 3 hard constraint: each Q3.7.x section flags its categorical adaptation deviation from the continuous-template precedents (mean/median/skewness -> per-category frequencies + entropy; ACF -> ordinal-encoded ACF + transition rate; near-identity -> Spearman on ordinal encoding + explicit categorical-sibling marking; crash-vs-normal -> chi-square 2x5 + MWU on ordinal + heavy/very_heavy spike-class fraction; spike-form -> heavy/very_heavy burst frequency; outlier -> rare-class flag + per-month rate-drift). Per handoff section 1: 'document adaptations explicitly in narrative + flag any deviations from continuous-template precedents.'
5. **First-order day-level read distinct from HA01b/HA01c tested operands**: HA01b-recomputed's operand is the 4-day-window composite on the lagged variant; HA01c's is the effective-exertion-rank shock at tau=0.75 on the lagged rank; HA-C4c's is the heavy-T classifier on the lagged-lcera variant. This Q3.7.f's first-order day-level chi-square + Mann-Whitney U on the un-lagged categorical primary is the descriptive complement at a coarser resolution -- NOT a re-anchoring of the locked HA verdicts.

---

*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: ``python run.py``.*
