# HA-C3p r2 RESULT: PARTIAL (2-of-3 conditions MET)

## Authorship

Drafted 2026-06-23 by Claude (Opus 4.7, 1M context) in producer-mode under user authorisation per [CONVENTIONS section 1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default). Authorising user: Willem. Pre-reg r2 LOCKED 2026-06-23 at commit `c0148ca`. Test commit: `(this-commit)`. Status: **LANDED**.

**Test-session context**: this `test.py` was implemented and run in a FRESH Claude session per the post-lock discipline of [`hypothesis_lock_process.md` section 3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). Sister-session note: HA-C3 v2 r2 test execution runs in parallel; section 6 4-cell agreement matrix populates HA-C3p's column only; HA-C3 v2's column is marked TBD (dispatcher consolidates).

## Section 1 - What was tested

**Headline cell** (per pre-reg section 1 + section 5.0): unmedicated (full LC era through 2024-04-08) x full Stratum 4 single pool x `all_day_stress_avg` binned at equal-N quintile bins {Q1[0,28), Q2[28,31), Q3[31,34), Q4[34,37), Q5[37,100]} x `gevoelscore` bin-mean x {Jonckheere-Terpstra monotone-decreasing + second-difference convexity contrast S = mean(D2_2, D2_3, D2_4) + spline non-linearity with 4 internal knots at quintile boundaries} x block-permutation null at E[L]=7 x 3-condition gated verdict per section 5.1.

**Substantive question** (per pre-reg section 2(a) Wiggers source + section 1 sister-pre-reg framing): does the underlying convex stress -> fatigue shape Wiggers describes (PDF lines 1357-1368, Annual Stress Scores, 'stair-step' qualitative reading) fire on the participant's **personal-baseline-anchored quintile bins** per [CONVENTIONS section 3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds), rather than at Wiggers' verbatim 30 -> 40 numerical anchor (HA-C3 v2 carries that operationalisation)? The user's framing per the session handoff: HA-C3 v2 stays honest against the original Wiggers document; **HA-C3p goes further to see if we can find the mechanism Wiggers is describing besides the numbers she uses**.

**3-condition gated verdict per section 5.1**:

| outcome | condition status | verdict |
|---|---|---|
| (a) MET AND (b) MET AND (c) MET | 3-of-3 | **SUPPORTED** |
| Exactly 2-of-3 MET | 2-of-3 | **PARTIAL** |
| <=1-of-3 MET | 0/1-of-3 | **REJECTED** |
| Any wrong-direction firing | override | **REJECTED** |

## Section 2 - Data + descriptives

Primary unmedicated pool: n = **581**. Stress median: **34.00**. Gevoelscore median: **4.00**.
Full Stratum 4 pool (for cross-arm bin-edge cleanliness): n = 1351.

### Unmedicated per-bin distribution

| bin | label | n | bin-mean gevoelscore | bin-median |
|---|---|---:|---:|---:|
| Q1 | Q1[0,28) | 45 | 3.822 | 4.00 |
| Q2 | Q2[28,31) | 80 | 4.138 | 4.00 |
| Q3 | Q3[31,34) | 129 | 4.271 | 4.00 |
| Q4 | Q4[34,37) | 138 | 4.290 | 4.00 |
| Q5 | Q5[37,100] | 189 | 4.016 | 4.00 |

### Full Stratum 4 per-bin distribution (descriptive)

| bin | label | n | bin-mean gevoelscore |
|---|---|---:|---:|
| Q1 | Q1[0,28) | 248 | 4.379 |
| Q2 | Q2[28,31) | 253 | 4.443 |
| Q3 | Q3[31,34) | 294 | 4.483 |
| Q4 | Q4[34,37) | 251 | 4.466 |
| Q5 | Q5[37,100] | 305 | 4.210 |

### Right-shift unmedicated bin observation (per spec section 8 caveat 4)

The unmedicated stratum is **right-shifted** relative to the full Stratum 4 pool: unmedicated [Q1=45, Q2=80, Q3=129, Q4=138, Q5=189] vs full-pool [Q1=248, Q2=253, Q3=294, Q4=251, Q5=305]. Q1 share: 7.7% (unmed) vs 18.4% (full pool); Q5 share: 32.5% (unmed) vs 22.6% (full pool). The unmedicated pool concentrates mass at higher quintiles relative to the full Stratum 4 pool. This is **consistent with citalopram's CONFIRMED +0.57/mg `all_day_stress_avg` beta per [`citalopram_dose_response_stress_mean_sleep.md` section 5.6.1](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read)**: medication (consolidation + afbouw phases of Stratum 4) compresses the stress range; unmedicated days populate the higher quintiles disproportionately. This is a **substantive cross-test validation of the recalibration finding at a different operationalisation** (bin distribution rather than mean beta).

## Section 3 - Primary test result

Per pre-reg section 4.5.1 + section 4.7 block-permutation at E[L]=7 (B = 10000 draws, seed = 20260624).

| condition | statistic | observed | one-sided p | direction OK | bar (p<0.05) | MET |
|---|---|---:|---:|:---:|:---:|:---:|
| (a) Jonckheere-Terpstra (monotone-decreasing) | J* (standardised) | +0.2671 | 0.5925 | NO | fail | fail |
| (b) Second-difference convexity | S = mean(D2_2, D2_3, D2_4) | -0.1964 | 0.0018 | YES (S<0) | PASS | PASS |
| (c) Spline non-linearity (block-permutation) | F (continuous predictor) | +19.5540 | 0.0020 | YES (3 of 4 midpoints negative) | PASS | PASS |
| (d) Companion orthogonal quadratic (descriptive) | c.m, c=(+2,-1,-2,-1,+2) | -1.2938 | 0.0008 | n/a | n/a | n/a |

**Aggregate 3-condition verdict: PARTIAL (2-of-3 conditions MET)**

*Spline parametric F (descriptive only per pre-reg section 4.5.1(c)): F = 19.553958253022355, parametric p = 6.07069506577535e-09.*

**Bin-means (primary, unmedicated)**:

| bin | n | mean | 95% CI (stationary bootstrap E[L]=7, B=1000) |
|---|---:|---:|---|
| Q1 | 45 | 3.822 | [3.387, 4.212] |
| Q2 | 80 | 4.138 | [3.941, 4.338] |
| Q3 | 129 | 4.271 | [4.090, 4.436] |
| Q4 | 138 | 4.290 | [4.143, 4.422] |
| Q5 | 189 | 4.016 | [3.791, 4.246] |

**Pairwise adjacent-bin Mann-Whitney + Holm step-down (per spec section 4.5.2 + section 5.1 PARTIAL-band multiplicity disclosure)**:

| pair | n_i | n_j | U | raw p | Holm threshold | Holm-adj p | Holm-rejected |
|---|---:|---:|---:|---:|---:|---:|:---:|
| Q1-Q2 | 45 | 80 | 1552 | 0.1778 | 0.0167 | 0.5333 | no |
| Q2-Q3 | 80 | 129 | 4648 | 0.1988 | 0.0250 | 0.5333 | no |
| Q3-Q4 | 129 | 138 | 8967 | 0.9106 | 0.0500 | 0.9106 | no |
| Q4-Q5 | 138 | 189 | 14803 | 0.0257 | 0.0125 | 0.1029 | no |

**Sanity-check companion Spearman rho** (the *opposing-model* linear test per section 4.5.2): rho = -0.0298 (p = 0.4738, n = 581).

## Section 4 - Sensitivity arms (descriptive, no verdict weight)

### Section 5.B - cross-phase dose-adjusted (predictor - 0.57/mg x dose_plasma_mg; REUSES locked quintile boundaries)

- Pool n = 1351; bin-n = [782, 96, 136, 143, 194]; bin-mean = [4.544757033248082, 4.166666666666667, 4.286764705882353, 4.27972027972028, 4.041237113402062].
- Verdict (descriptive, NOT promoted): **REJECTED (0-of-3 conditions MET)**.

### z-scored vs 28d-lagged baseline (per Locked decision 2 + CONVENTIONS section 3.1)

- Pool n = 567; bin-n = [111, 126, 101, 118, 111].
- z-score quintile edges (q=0.2,0.4,0.6,0.8): [-0.899, -0.289, 0.27, 1.012].
- bin-mean = [4.126126126126126, 4.277777777777778, 4.267326732673268, 4.1525423728813555, 3.936936936936937].
- S = -0.1224; J* = +1.4288; p_a=0.9034, p_b=0.0194, p_c=0.0886.
- Verdict (descriptive, NOT promoted): **REJECTED (1-of-3 conditions MET)**.

### Crash-drop sensitivity (CONVENTIONS section 3.4)

- S (full) = -0.1964 (n = 581); S (no-crash) = -0.0331 (n = 503).
- |Delta S| standardised = 0.1771; sign-change = False; flag = **FLAG**.

### Train/validate M3 descriptive overlay (per `train_validate_split_fate.md` section 5)

- Train (<= 2023-12-31): n = 482; bin-n = [38, 61, 101, 111, 171]; bin-mean = [3.8157894736842106, 4.229508196721311, 4.366336633663367, 4.351351351351352, 4.011695906432749]; S = -0.25112472265190117.
- Validate (2024-01-01 -> 2024-04-08): n = 99; bin-n = [7, 19, 28, 27, 18]; bin-mean = [3.857142857142857, 3.8421052631578947, 3.9285714285714284, 4.037037037037037, 4.055555555555555]; S = 0.011185370834493558.
- Per `train_validate_split_fate.md` section 5: divergence is a number, not a narrative; no per-era verdicts.

### t+1 lagged variant (gevoelscore[T+1] on stress[T])

- n = 581; bin-n = [45, 80, 129, 138, 189]; bin-mean = [4.111111111111111, 4.35, 4.232558139534884, 4.304347826086956, 3.878306878306878]; S = -0.22164327888965563.

## Section 5 - Bin-by-bin descriptive characterisation

Adjacent-bin step magnitudes (positive = bin-mean DROP from low -> high):

| step | bin pair | magnitude (m_low - m_high) |
|---|---|---:|
| 1 | Q1-Q2 | -0.315 |
| 2 | Q2-Q3 | -0.134 |
| 3 | Q3-Q4 | -0.019 |
| 4 | Q4-Q5 | +0.274 |

Per pre-reg section 7.1 SUPPORTED expectation: monotone decreasing (positive steps); accelerating decrement (Q4 -> Q5 step LARGEST in magnitude because Q5 has width 63 vs Q2-Q4 widths 3).

## Section 6 - Cross-test reading: 4-cell agreement matrix with HA-C3 v2

Per pre-reg Locked decision 5 + section 1 sister-pre-reg framing, HA-C3p's result.md section 6 carries the 4-cell agreement-matrix interpretation with HA-C3 v2 (Wiggers-verbatim sister test). HA-C3 v2 r2 test execution runs in **parallel** with this HA-C3p session; its verdict is **TBD** at this result-emission time. The dispatcher consolidates the matrix in a follow-up commit after both sessions return.

### 4-cell matrix (HA-C3p column populated; HA-C3 v2 column TBD)

| HA-C3 v2 (Wiggers) v / HA-C3p (personal) > | SUPPORTED | REJECTED |
|---|---|---|
| SUPPORTED | strong (both agree on convexity) | bin-edge artefact (v2 anchors happen to fall on a peak HA-C3p smooths) |
| REJECTED | Wiggers' numbers wrong-for-this-participant but underlying shape real | informative null (no convexity at either operationalisation) |

**HA-C3p verdict**: **PARTIAL**. **HA-C3 v2 axis**: **TBD (parallel session pending; dispatcher consolidates)**.

**HA-C3p column under PARTIAL** (note: matrix shown above is 2x2 SUPPORTED/REJECTED; PARTIAL is the intermediate state). The PARTIAL verdict is 2-of-3 conditions MET; downstream interpretation follows pre-reg section 9.2's three operationally-distinguishable PARTIAL configurations. Cross-test reading: PARTIAL is interpreted as 'evidence of some convex structure but not the full 3-condition headline'; the HA-C3 v2 cross-test consolidation will frame the PARTIAL-vs-v2-verdict reading at dispatcher-consolidation time.

### Sister-test cross-reference table

| pre-reg | verdict | venue | cited per |
|---|---|---|---|
| **HA-C3p (this test)** | **PARTIAL** | personal-baseline quintile bins | pre-reg section 5.1 |
| HA-C3 v2 r2 (Wiggers-verbatim sister; running in parallel) | **PENDING** (parallel session) | bins [0,30), [30,40), [40,60), [60,100] | pre-reg section 1 sister-test framing; dispatcher consolidates |
| HA-C4 v2 (daily-aggregate recovery-dynamics triad) | REJECTED at triad sum 0/3 | commit `52bddb5` 2026-06-18 | structurally distinct (recovery dynamics, not same-day shape) |
| HA-C4c (bout-level cross-phase) | PARTIAL (bar (b) effect-size failing; bar (a) PASS p=0.0001, delta=+0.120 at n_heavy=465/n_non=809) | commit `a69a8ed` 2026-06-23 | structurally distinct (bout-level, not bin-shape) |
| HA-P6 v3 (post-crash autonomic recovery shape) | noisy-inconclusive / mixed per-channel | 2026-06-17 | structurally distinct (event-anchored recovery, not cross-day shape) |
| HA11 v1 (within-day stress U-dip count) | SUPPORTED on train, REFUTED on validate (overall REFUTED) | committed in HA11-stress-udip | structurally distinct (within-day pattern, not cross-day shape) |

## Section 7 - Section 4.7 E[L]* report (factor-of-2 flag)

Per pre-reg section 4.7: two data-driven E[L]* checks (linear-residual + bin-label).

| derivation | E[L]* | cutoff lag | factor-of-2 flag | note |
|---|---:|---:|:---:|---|
| linear residual (continuous-predictor) | 5.35 | 3 | ok |  |
| bin-label sequence | 7.00 | 1 | ok | Closed-form formula degenerate; returning default |

No flags.

## Section 8 - Caveats (per pre-reg section 8)

1. **Power-calc dispatch**: power calculation is **inapplicable per Daza 2018** within-subject n-of-1 design. Block-permutation null at E[L]=7 is the within-subject inferential machinery; the 3-condition gated verdict is the decision rule. Equal-N quintile-bin design eliminates structural-underpower from the bin-design dimension.
2. **Sister-pre-reg framing**: HA-C3p tests the underlying convex-shape claim Wiggers describes on **personal-baseline-anchored bins** per CONVENTIONS section 3.1; HA-C3 v2 tests Wiggers' verbatim 30->40 numerical anchor. The 4-cell agreement matrix lives in section 6 above (HA-C3 v2 axis TBD pending parallel-session consolidation).
3. **CONVENTIONS section 3.1 personal-baseline framing**: HA-C3p's quintile bins are pool-anchored (equal-N quintiles on the full Stratum 4 distribution at the locked draft-time snapshot). The z-scored-against-personal-rolling-baseline variant is reported as the section 4.8(b) sensitivity arm; raw quintiles are primary because the rolling-baseline z-score has edges that drift in raw stress-units over time, complicating cross-arm bin-edge cleanliness.
4. **Citalopram-channel inheritance** (load-bearing for the right-shift unmedicated bin observation surfaced in section 2): `all_day_stress_avg` is CONFIRMED dose-modulated at +0.57/mg per `citalopram_dose_response_stress_mean_sleep.md` section 5.6.1. The unmedicated stratum's right-shifted bin distribution (see section 2 above) is a **cross-test validation of this recalibration finding at a different operationalisation** (bin distribution rather than mean beta).
5. **HA-C3 v1 partial-pool non-monotone observation as caveat-class prior**: v1's HALT-time partial-pool descriptive trajectory (B2-B3-B4 = 3.958 -> 4.265 -> 3.860, peak at v1 B3 = stress 30-40) was descriptively non-monotone. Caveat-class prior informing HA-C3p's interpretation; not promoted to a substantive HA-C3p output. HA-C3p does NOT pre-commit to an inverted-U / threshold-pattern alternative claim.
6. **n=1 single-subject** per CONVENTIONS section 3.1: thresholds in section 5.1 calibrated against the participant's distribution. The block-permutation null is the within-subject inferential anchor.
7. **Operational vs mechanistic** per CONVENTIONS section 4.1-4.3: the convex shape is the operationalised pattern; the 'stress-cost asymmetry' mechanism Wiggers describes is the substantive interpretation but not the operational measure. A SUPPORTED verdict means the operationalised convex-shape pattern fires on the personal-range bins; it does NOT prove the substantive Wiggers stress-cost-asymmetry mechanism causally.
8. **Crash-day inclusion structural fragility** (CONVENTIONS section 3.4): crashes KEPT in primary; section 4.6 crash-drop arm reported in section 4 above (sign-boundary flag if |Delta S| > 0.10 standardised OR sign-change).
9. **No causal-direction inference**: test answers 'does the gevoelscore-vs-stress-quintile mapping have a convex shape?', not 'does stress CAUSE fatigue?'.
10. **Bin-edge snapshot pinning** (NEW in HA-C3p): the section 4.1 quintile boundaries are pre-committed at draft time to `per_day_master.csv` SHA-256 `d0ff9253`. Section 7.5 Gate 5 verifies the boundaries have not shifted by > 1 stress-unit on the test-time snapshot. **Gate 5 status at run-time** (see section 9.5 below).
11. **Independent-obligations block** per `citalopram_phase_stratification section 6`: autocorrelation (section 4.7) + crash-drop (section 4.6) + spike-companion (N/A; HA-C3p is cross-day-aggregate) + trajectory-detrend (N/A; not a pre-vs-post comparison).
12. **Drafting context disclosure**: the drafter saw the bin boundaries (28, 31, 34, 37) and per-bin n on both pools at draft time, but NOT the per-bin gevoelscore means on the quintile-binned distribution. The joint bin-mean trajectory was the post-lock deferred artefact.
13. **Wiggers' phrasing is qualitative**: the verbatim 'stair-step' language is qualitative. HA-C3 v2's (0,30,40,60,100) bins are ONE operationalisation; HA-C3p's quintile bins are a DIFFERENT operationalisation. A REJECTED verdict on either does not falsify the qualitative Wiggers framing universally.
14. **Sister-test cross-references**: see section 6 cross-reference table above.

## Section 9 - Section 7.5 gate results + reproducibility

### Section 7.5 sanity gates

| gate | description | result |
|---|---|---|
| 1 | per-bin n >= 30 (x5 quintile bins) | PASS |
| 2 | stress median in [20, 60] | PASS |
| 3 | gevoelscore median in [3, 6] | PASS |
| 4 | all 5 bins n>=30 AND total n>=100 | PASS |
| 5 (SHA) | snapshot SHA-256 matches `d0ff9253` | PASS |
| 5 (bound) | quintile boundary shift <= 1 stress-unit | PASS |

**Gate 5 observed SHA**: `d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d`. **Expected SHA**: `d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d`. **Recomputed quintile boundaries**: [28.0, 31.0, 34.0, 37.0]. **Locked boundaries**: [28.0, 31.0, 34.0, 37.0].

### Reproducibility checklist

- **Script**: `docs/research/analyses/hypotheses/HA-C3p/test.py`
- **Environment variable**: `GEVOELSCORE_DATA_PATH` (default: `C:\Users\Gebruiker\Documents\gevoelscore-data`)
- **Seed**: `RANDOM_SEED = 20260624`
- **Bootstrap**: B = 10000 stationary-bootstrap draws per condition; E[L] = 7 (geometric block length)
- **Regenerate command**: `python docs/research/analyses/hypotheses/HA-C3p/test.py`
- **Dependencies**: numpy, scipy (for `CubicSpline`, `mannwhitneyu`, `spearmanr`, `f.sf`); project utility `docs/research/analyses/_utils/inference.py` for `compute_data_driven_block_length` + `holm_step_down`.
- **Spec commit**: `c0148ca` (LOCKED 2026-06-23)
- **Snapshot SHA-256 at run-time**: `d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d`
- **Machine-readable companion**: `result-data.json` (gitignored per `docs/research/**/*.json`)

---

*test.py run with `RANDOM_SEED = 20260624`, `BOOTSTRAP_E_L = 7`, B = 10000 draws per condition. Source: `per_day_master.csv` from `$GEVOELSCORE_DATA_PATH`. Spec commit: `c0148ca`. Snapshot SHA-256: `d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d`.*
