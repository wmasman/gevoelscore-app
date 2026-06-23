# HA-C3 v2 r2 RESULT: REJECTED (wrong-direction override)

## Authorship

Drafted 2026-06-23 by Claude (Opus 4.7, 1M context) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default). Authorising user: Willem. Pre-reg v2 r2 LOCKED 2026-06-23 at commit `2a0b0df`. Test execution session per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).

**v1 lineage**: HA-C3 v1 r2 LOCKED 2026-06-23 at `de22b68` (archived as `hypothesis-v1-archived.md`); test-executed 2026-06-23 at `a9423af` and **HALTed on §7.5 Gate 1** because B1 [0,20) had n=0 on this corpus (`all_day_stress_avg` never falls below 20 in Stratum 4 unmedicated pool). Per [`hypothesis_lock_process §10.4 step 3`](../../../methodology/hypothesis_lock_process.md#104-five-stage-arc-iteration-policy) no-iteration-post-dry-run discipline, the v2 redraft created the new bin spec `[0,30), [30,40), [40,60), [60,100]` with the Wiggers verbatim 30→40 anchor preserved at the new B2-B3 boundary, plus §7.3 halt-option-A PRE-COMMITTED for B4. This is a CLEAN RETEST at the revised bin spec; the v1 partial-pool trajectory (B2-B3-B4 = 3.958 → 4.265 → 3.860 across v1 bins) enters as §8 caveat 9 caveat-class prior per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), NOT promoted to a substantive v2 output.

**§7.3 halt-option-A APPLIED (PRE-COMMITTED absorb)**: B4 [60,100] had n < 30 at dry-run; per the LOCKED v2 r2 spec §7.3, B3 [40,60) was automatically widened to absorb B4, producing the 3-bin reduction `{B1 [0,30), B2 [30,40), B3' [40,100]}`. The test runs on the 3-bin reduction with the contrast reduced to a single second-difference `S = m_3 − 2·m_2 + m_1` and the spline reduced to 2 internal knots at (30, 40); visual-gating count reduces to ≥ 1 of 2 segment midpoints from {35, 70}. **This is NOT a halt** — the LOCKED spec PRE-COMMITS to this absorption.

## §1 What was tested

**Headline cell** (per pre-reg §1 + §5.0): unmedicated (full LC era through 2024-04-08) × full Stratum 4 single pool × `all_day_stress_avg` binned at {B1[0,30), B2[30,40), B3'[40,100]} × `gevoelscore` bin-mean × {Jonckheere-Terpstra monotone-decreasing + second-difference convexity contrast S + spline non-linearity F-test with sign-gated second-derivative check} × block-permutation null at E[L]=7 × 3-condition gated verdict per §5.1.

**Wiggers C3 verbatim claim** (PDF lines 1357-1368, Annual Stress Scores section): the stress → fatigue relationship is non-linear / convex — a 30 → 40 stress step costs more gevoelscore than the steps preceding it. **v2 preserves the verbatim 30→40 anchor at the new B2-B3 boundary**. Tested as the bin-mean trajectory should be **monotone-decreasing** AND **convex** (accelerating decrement at higher stress bins).

**3-condition gated verdict per §5.1**:

| outcome | condition status | verdict |
|---|---|---|
| (a) MET AND (b) MET AND (c) MET | 3-of-3 | **SUPPORTED** |
| Exactly 2-of-3 MET | 2-of-3 | **PARTIAL** |
| ≤ 1-of-3 MET | 0/1-of-3 | **REJECTED** |
| Any wrong-direction firing | override | **REJECTED** |

**STROBE-Item-12 forward-reference** (per pre-reg §1 + §8 caveat 7): operationalised measures sourced per [DATA_DICTIONARY](../../../DATA_DICTIONARY.md) §C (`all_day_stress_avg`) + §S (`gevoelscore`); computation paths traceable to [pipeline](../../../pipeline/).

## §2 Data + descriptives

Primary unmedicated pool (post-§4.3 day-validity gate): n = **581**. Stress median: **34.00**. Gevoelscore median: **4.00**.

### 4-bin descriptive sanity (pre-§7.3 absorption check)

| bin | label | n | bin-mean gevoelscore | bin-median |
|---|---|---:|---:|---:|
| B1 | B1[0,30) | 95 | 3.958 | 4.00 |
| B2 | B2[30,40) | 385 | 4.265 | 4.00 |
| B3 | B3[40,60) | 100 | 3.860 | 4.00 |
| B4 | B4[60,100] | 1 | 1.000 | 1.00 |

**Note**: B4 underpower triggered §7.3 halt-option-A PRE-COMMITTED absorb at dry-run; subsequent test runs on the 3-bin reduction below.

### 3-bin reduction descriptives (post-§7.3 absorption)

| bin | label | n | bin-mean gevoelscore |
|---|---|---:|---:|
| B1 | B1[0,30) | 95 | 3.958 |
| B2 | B2[30,40) | 385 | 4.265 |
| B3 | B3'[40,100] | 101 | 3.832 |

## §3 Primary test result

Per pre-reg §4.5.1 + §4.7 block-permutation at E[L]=7 (B = 10000 draws, seed = 20260623).

| condition | statistic | observed | one-sided p | direction OK | bar (p<0.05) | MET |
|---|---|---:|---:|:---:|:---:|:---:|
| (a) Jonckheere-Terpstra (monotone-decreasing) | J* (standardised) | +0.4806 | 0.6742 | NO | fail | fail |
| (b) Second-difference convexity | S = D²_2 = m_3 − 2·m_2 + m_1 | -0.7403 | 0.0002 | YES (S<0) | PASS | **PASS** |
| (c) Spline non-linearity (2 segment midpoints: x=35/70) | F (continuous predictor) | +28.2689 | 0.0003 | YES (1 of 2 midpoints negative; bar ≥ 1) | PASS | **PASS** |
| (d) Companion orthogonal quadratic (descriptive) | c·m, c=(+1,−2,+1) | -0.7403 | 0.0002 | n/a | n/a | n/a |

**Aggregate 3-condition verdict: REJECTED (wrong-direction override)**

**Wrong-direction overrides** fired:
- (c) spline second-derivative POSITIVE at >= 1 midpoints (positive sign at majority of contributing midpoints)

**Spline second-derivative at segment midpoints**:

| midpoint x | spline second-derivative | sign |
|---:|---:|:---:|
| 35 | -0.00151 | NEG |
| 70 | +0.00000 | POS |

*Spline parametric F (descriptive only per pre-reg §4.5.1(c)): F = 28.268865170890678, parametric p = 1.5107630908819702e-07.*

**Bin-means (primary)**:

| bin | n | mean | 95% CI (stationary bootstrap E[L]=7, B=1000) |
|---|---:|---:|---|
| B1 (B1[0,30)) | 95 | 3.958 | [3.671, 4.222] |
| B2 (B2[30,40)) | 385 | 4.265 | [4.145, 4.381] |
| B3 (B3'[40,100]) | 101 | 3.832 | [3.516, 4.169] |

**Pairwise adjacent-bin Mann-Whitney + Holm step-down (2 pairs; descriptive, secondary)**:

| pair | n_i | n_j | U | raw p | Holm threshold | Holm-adj p | Holm-rejected |
|---|---:|---:|---:|---:|---:|---:|:---:|
| B1-B2 | 95 | 385 | 15328 | 0.0089 | 0.0500 | 0.0089 | YES |
| B2-B3' | 385 | 101 | 23168 | 0.0015 | 0.0250 | 0.0030 | YES |

**Sanity-check companion Spearman ρ** (the *opposing-model* linear test per §4.5.2): ρ = -0.0298 (p = 0.4738, n = 581). Reading: a positive Spearman alongside a failing convexity test would indicate roughly linear-or-concave monotone-decreasing — i.e. against C3.

## §4 §4.4 citalopram approach results

### §5.A unmedicated headline (PRIMARY)

Per §4.4 LOCKED + Locked decision 8: the §5.A unmedicated phase headline IS the primary cell reported in §3 above. CONFIRMED-channel inheritance per [`citalopram_phase_stratification §4`](../../../methodology/citalopram_phase_stratification.md#4-per-channel-inheritance-rules): `all_day_stress_avg` is dose-modulated at +0.57/mg per [`citalopram_dose_response §5.6.1`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read); §5.A per-phase stratification with the unmedicated phase as the headline pool is the load-bearing choice. **No separate §5.A result is reported; §3 above IS the §5.A result**.

### §5.B dose-adjusted cross-phase sensitivity arm

Per §4.4 + Locked decision 8: §5.B cross-phase test with predictor adjusted as `all_day_stress_avg − 0.57/mg × dose_plasma_mg(d)` per [`citalopram_phase_stratification §5.B`](../../../methodology/citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests).

- Pool n = 1351; n_bins = 3; optA_applied = True; bin-n = [844, 403, 104]; bin-mean = [4.513, 4.27, 3.875].
- **Verdict (descriptive, NOT promoted to primary)**: **REJECTED (0-of-3 conditions MET)**.

### Within-consolidation §5.A replication (§4.4 secondary)

- Pool n = 635; bin-n (initial 4-bin) = [273, 315, 47, 0].
- §7.3 halt-option-A APPLIED recursively on the consolidation arm (B3 absorbed B4); bin-n after = [273, 315, 47]; n_bins_used = 3.
- **Verdict (descriptive, NOT promoted)**: **REJECTED (wrong-direction override)**.

## §5 Sensitivity arms (per §4.8; descriptive, no verdict weight)

### §4.6 Crash-drop sensitivity (CONVENTIONS §3.4)

- S (full) = -0.7403 (n = 581); S (no-crash) = -0.1473 (n = 503).
- |Δ S| standardised = 0.6427; sign-change = False; flag = **FLAG**.
- Per pre-reg §4.6 + CONVENTIONS §3.4: flag is informative for interpretation; does NOT modify the §5.1 verdict.

### §4.8 Train/validate M3 descriptive overlay

- Train (≤ 2023-12-31): n = 482; bin-n = [77, 312, 93]; bin-mean = [3.974, 4.333, 3.817]; S = -0.8754.
- Validate (2024-01-01 → 2024-04-08): n = 99; bin-n = [18, 73, 8]; bin-mean = [3.889, 3.973, 4.0]; S = -0.0563.
- Per `train_validate_split_fate.md`: divergence is a number, not a narrative; no per-era verdicts.

### §4.8 t+1 lagged variant (gevoelscore[T+1] on stress[T])

- n = 581; bin-n = [95, 385, 101]; bin-mean = [4.232, 4.249, 3.644]; S = -0.6236.

## §6 Sister-test cross-reference (descriptive context per §8 caveat 12)

| sister test | verdict | one-line context | commit |
|---|---|---|---|
| **HA-C3p** (personal-baseline-anchored sister; equal-N quintile bins) | **verdict pending; consolidation in HA-C3p result.md §6 4-cell agreement matrix** | personal-baseline equal-N quintile bins on full Stratum 4 pool; running in parallel session; 4-cell agreement matrix lives in HA-C3p result.md §6 per LOCKED HA-C3p decision | `c0148ca` (LOCKED) |
| HA-C4 v2 | **REJECTED** | daily-aggregate triad sum 0.0/3.0; Ch1+Ch2 validate SUPPORTED but train REFUTED -> mixed-era cancellation | `52bddb5` |
| HA-C4c | **PARTIAL** | bout-level recovery dynamics; bar (a) PASS p=0.0001 / bar (b) FAIL δ=+0.120 at cross-phase-pooled n=465/n=809; weak-effect-but-real positive pattern | `a69a8ed` |
| HA-P6 | (informational) | per cross-test register; substantively distinct from C3 daily-aggregate shape | -- |
| HA11 v1 | SUPPORTED-on-train | within-day U-dip count +22.8 pp (calm-day sister channel); structurally distinct from cross-day-aggregate shape | (per register) |

**Reading**: HA-C3 v2 tests Wiggers' verbatim 30→40 numerical anchor on the v2 4-bin scheme (or 3-bin reduction post-§7.3 absorption). The sister pre-reg HA-C3p tests the underlying convex-shape mechanism on personal-baseline-anchored quintile bins per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds). The 4-cell agreement matrix between HA-C3 v2 and HA-C3p verdicts is consolidated in HA-C3p result.md §6 by the dispatcher post-parallel-session completion; this result.md does NOT populate that matrix.

## §7 §4.7 E[L]* report (factor-of-2 flag)

Per pre-reg §4.7 r2 amendment: two data-driven E[L]* checks (linear-residual + bin-label) per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md).

| derivation | E[L]* | cutoff lag | factor-of-2 flag | note |
|---|---:|---:|:---:|---|
| linear residual (continuous-predictor) | 5.35 | 3 | ok |  |
| bin-label sequence | 7.00 | 1 | ok | Closed-form formula degenerate; returning default |

No flags.

## §8 Caveats (per pre-reg §8; surfaced prominently)

1. **Power-calc dispatch**: inapplicable per Daza 2018 within-subject n-of-1 design ([within-subject Methods Inf Med citation](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)). Block-permutation null at E[L]=7 is the within-subject inferential machinery; the 3-condition gated verdict is the decision rule. INCONCLUSIVE per §5.2 is the operational definition of 'underpowered for this cell'.
2. **n=1 single-subject caveats** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-population-norm): thresholds (p<0.05; S<0; spline 2nd-deriv negative at ≥ 1 of 2 segment midpoints) calibrated to the participant's distribution. No cross-subject generalisation.
3. **Citalopram-channel inheritance**: `all_day_stress_avg` is CONFIRMED dose-modulated at +0.57/mg ([dose-response §5.6.1](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read)). Primary uses §5.A per-phase stratification (unmedicated headline); §5.B dose-adjusted is cross-phase sensitivity. §4 above.
4. **Crash-day inclusion structural fragility** per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions): crashes KEPT in primary; §4.6 crash-drop arm flagged if |Δ S| > 0.10 standardised OR sign-change. §5 above. Flag is informative; does NOT modify §5.1 verdict.
5. **Within-subject shape, NOT between-subject prediction**: the convex stress→fatigue claim is about THIS participant's mapping; no cross-person generalisation claimed.
6. **No causal-direction inference**: the test answers "does the mapping have a convex shape?" — it does NOT answer "does stress CAUSE fatigue?". Per [CONVENTIONS §4.1-§4.3](../../../CONVENTIONS.md#4-statistical-discipline): descriptive characterisation of mapping shape, not causal claim.
7. **v2 scope is corpus-stress-range AS-REPRESENTED, NOT Wiggers' abstract register range** (NEW in v2 per the v1 HALT lineage). v1 r2 was test-executed and HALTed at §7.5 Gate 1 because B1 [0,20) had n = 0 on the unmedicated pool. v2 responds by collapsing v1's B1 [0,20) into v1's B2 [20,30) to form v2's new B1 [0,30). The v2 verdict scope is therefore the corpus-represented stress range (effectively [20, 100]), NOT the abstract Wiggers register range. A SUPPORTED v2 verdict would mean: the convex shape is empirically confirmed on this participant's `all_day_stress_avg` distribution AS REPRESENTED, with the explicit caveat that the low-stress register (< 20) is structurally absent and therefore not tested. **STROBE-Item-12 source-file traceability inventory**: operationalised measures sourced per [DATA_DICTIONARY](../../../DATA_DICTIONARY.md) §C + §S; computation paths traceable to [pipeline](../../../pipeline/) per CONVENTIONS STROBE-Item-12 inheritance.
8. **Wiggers' phrasing is qualitative**: the (0-30, 30-40, 40-60, 60+) binning is OUR operationalisation; a REJECTED verdict at these specific bins does NOT universally falsify the qualitative stair-step framing per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no).
9. **v1 partial-pool non-monotone trajectory as caveat-class prior informing v2 interpretation** (NEW in v2). v1's HALT-time partial-pool descriptive trajectory across the 3 populated bins was **B2-B3-B4 = 3.958 → 4.265 → 3.860**, peak at v1 B3 = stress 30-40, **non-monotone** at the descriptive level. This is a **caveat-class prior informing v2 interpretation, NOT a quasi-result and NOT a substantive v2 output**. v2 does NOT pre-commit to an inverted-U / threshold-pattern alternative claim; promoting that observation to a SUPPORTED-of-inverted-U claim would require a separate §3.2 fresh-session redraft to HA-C3-v3 with the alternative-shape claim as the primary.
10. **Independent-obligations block** per [`citalopram_phase_stratification §6`](../../../methodology/citalopram_phase_stratification.md#6-pre-registration-template-for-new-hypothesis-mds) — autocorrelation (§4.7) + crash-drop (§4.6) + spike-companion (N/A; HA-C3 is the cross-day-aggregate test, not within-day) + trajectory-detrend (N/A; not a pre-vs-post comparison) all handled per §4.
11. **Drafting-context disclosure** (NEW in v2 + operational consequence in v2 r2): v2 r1 was drafted in a fresh worktree-isolated session 2026-06-23. The drafter had seen v1 partial-pool descriptives (pool n=581, stress median 34, gevoelscore median 4, populated-bins trajectory 3.958 → 4.265 → 3.860); the §4.1 v2 bin spec was chosen with knowledge of this distribution. **Operational consequence per [CONVENTIONS §4.3](../../../CONVENTIONS.md#43-confirmatory-vs-exploratory-distinction)**: the substantive Wiggers C3 convex-shape question stays **confirmatory** per the source-verified prior (Wiggers PDF 1357-1368); the v2 **operationalisation choice** (4-bin scheme collapsing v1's empty B1 into the new low-stress bin) is **exploratory-with-caveat** per the corpus-conditional redraft trigger. The distinction matters for §5.1 verdict interpretation: SUPPORTED supports the confirmatory question; PARTIAL or REJECTED carries the additional operationalisation-choice uncertainty.
12. **Sister-test cross-references** (extended in v2 r2): HA-C4 v2 REJECTED + HA-C4c PARTIAL + HA11 SUPPORTED-on-train are sister Wiggers-cluster results at structurally-distinct operationalisations; no direct cross-test prior import on the convex-shape claim. **Sister pre-reg [HA-C3p](../HA-C3p/hypothesis.md)** is the personal-baseline operationalisation per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-population-norm) (equal-N quintile bins on the participant's `all_day_stress_avg` distribution); HA-C3p tests the underlying convex-shape claim on the participant's actual stress range, while HA-C3 v2 tests Wiggers' verbatim 30→40 numerical anchor. The 4-cell agreement matrix lives in HA-C3p result.md §6.

## §9 Downstream actions (per pre-reg §9 verdict branch)

**§9.3 REJECTED branch**: the C3 verbatim claim is NOT empirically confirmed at the chosen v2 operationalisation within the §8 caveat 7 scope. See pre-reg §9.3 for the three distinguishable REJECTED configurations (wrong-direction firings; 0/1 conditions met). Under the 0-or-1-conditions branch with no wrong-direction firing, the mapping is roughly linear-or-flat OR non-monotone in the v1-partial-pool-trajectory direction. **Cross-reference downstream**: HA-C3 v2 REJECTED + HA-C4 v2 REJECTED would mean the Wiggers C-family at daily-aggregate is exhaustively-tested-and-not-supported on this corpus.

## §10 §7.5 dry-run gate results

| gate | description | result |
|---|---|---|
| 1 | per-bin n >= 30 (4 bins) | PASS |
| 2 | stress median in [20.0, 60.0] | PASS |
| 3 | gevoelscore median in [3.0, 6.0] | PASS |
| 4 | >= 2 bins n>=30 AND total n>=100 | PASS |

**§7.3 halt-option-A status**: **TRIGGERED at dry-run as PRE-COMMITTED** — B4 [60,100] underpower (n < 30) auto-absorbed into B3 [40,60), producing 3-bin reduction `{B1 [0,30), B2 [30,40), B3' [40,100]}`. Per the LOCKED v2 r2 spec §7.3 this is NOT a halt.

## §11 Reproducibility

- **Script**: `docs/research/analyses/hypotheses/HA-C3/test.py`
- **Environment variable**: `GEVOELSCORE_DATA_PATH` (default: `C:\Users\Gebruiker\Documents\gevoelscore-data`)
- **Seed**: `RANDOM_SEED = 20260623`
- **Bootstrap**: B = 10000 stationary-bootstrap draws per condition; E[L] = 7 (geometric block length).
- **Regenerate command**: `python docs/research/analyses/hypotheses/HA-C3/test.py`
- **Dependencies**: numpy, scipy (`CubicSpline`, `mannwhitneyu`, `spearmanr`, `f.sf`); project utility `docs/research/analyses/_utils/inference.py` for `compute_data_driven_block_length` + `holm_step_down`.
- **Spec commit**: `2a0b0df` (LOCKED 2026-06-23)
- **Machine-readable companion**: `result-data.json` (gitignored per `docs/research/**/*.json`).
- **Pipeline-trust**: `per_day_master.csv` snapshot read at run-time from `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`.

---

*test.py run with `RANDOM_SEED = 20260623`, `BOOTSTRAP_E_L = 7`, B = 10000 draws per condition. Source: `per_day_master.csv` from `$GEVOELSCORE_DATA_PATH`. Spec commit: `2a0b0df`.*
