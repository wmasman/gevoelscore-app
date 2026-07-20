# Stage D descriptive audit: streak-length arc under MD-beta r2 LOCKED

*Producer-mode Stage D descriptive audit per [CONVENTIONS section 1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). Drafted 2026-07-19 by Claude (Opus 4.7) in producer-mode subagent under user delegation. Authorising user: Willem.*

**Status**: **LOCKED r1 2026-07-20** post fresh-session review absorption. See section 9 lock log for r1 LOCKED entry and the four absorb-tier patches applied.
**Anchor MD**: [`heavy_day_crash_risk_prediction.md`](../../../methodology/heavy_day_crash_risk_prediction.md) LOCKED r2 2026-07-17, section 4 (streak-length arc) + section 5 confounds 2, 3, 5, 6, 7 + section 6.2 / 6.3 / 6.4 / 6.7 (byte-for-byte anchors).
**Data source**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` (LC-era stratum, `lc_phase == 'lc'`, n=1524 rows).
**Random seed**: 20260716 per MD-beta section 4.5.
**Reproducibility**: [`scripts/stage_d_streak_length.py`](scripts/stage_d_streak_length.py); outputs in [`output/`](output/); idempotent re-run.

**Discipline scope**: Stage D descriptive audit only per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). All per-bin crash rates reported as descriptive-with-Wilson-CI + descriptive-with-bootstrap-CI. Cochran-Armitage Z statistic + two-sided asymptotic p + permutation-null p reported for completeness only, NOT as verdicts. No inferential closure at Stage D.

**Cross-refs**:

- [MD-beta LOCKED r2 2026-07-17](../../../methodology/heavy_day_crash_risk_prediction.md) sections 4.1 (operand), 4.2 (outcome), 4.3 (primary contrast), 4.4 (direction pre-commit), 4.5 (statistical machinery), 4.6 (sample constraint), 4.7 (rolling-window-predictor autocorrelation flag), 5 confounds 2 + 3 + 5 + 6 + 7, 6.2 + 6.3 + 6.4 + 6.7 baseline anchors.
- [Sibling Stage D audit rest-adjacency arc LOCKED r1 2026-07-19](../Q24-mdbeta-stageD-rest-adjacency/descriptive_audit.md) for the pattern of the era-stratified 6-mechanism caveat, the sample-floor discipline, the discipline attestation block, and the lock-log entry style.
- [Parent Q24 MD LOCKED r1 2026-07-15](../../../methodology/post_heavy_day_compensatory_rest.md) sections 3.1 (unit-of-analysis gap=0), 3.5 (pool-split), 7.10 (block-length machinery).
- [Stage -1 audit LOCKED r1](../Q24-precursor-heavy-day-structure/audit.md) section 4 (streak-length distribution).
- [HA-P7 verdict-review + sensitivity_block_length.py](../../hypotheses/HA-P7/) for the E[L]* factor-of-2 precedent and the estimator implementation.
- [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) section 2 for the data-driven E[L]* estimator + factor-of-2 flag rule.

---

## 1. Corpus and preflight per-bin sample-floor probe

### 1.1 Corpus counts (points to parent Wave 2B / Stage -1 audit; Stage D-specific numbers)

| Measure | Value | Source |
|---|---|---|
| LC-era rows | 1524 days (2022-04-04 to 2026-06-05) | script header printout |
| Heavy days (heavy + very_heavy) | 532 (34.9%) | parent Stage -1 section 1 |
| Very-heavy days | 256 (16.8%) | parent Stage -1 section 1 |
| Crash days | 103 (crash_v2, day-level) | parent Stage -1 section 1 |
| gap=0 heavy episodes | 314 | script + parent Stage -1 section 4 |
| Episodes with heavy end_class | 165 | script |
| Episodes with very_heavy end_class | 149 | script |
| Episodes in pre-cital era (D_end < 2024-04-09) | 156 | script |
| Episodes in post-cital era (D_end >= 2024-04-09) | 158 | script |
| Episodes with crash_in_5d True | 46 (14.65%) | script + MD-beta section 6.7 |
| Corpus baseline crash rate (LC-era) | 103 / 1524 = 6.8% | MD-beta section 6.7 |

The 14.65% crash-in-5d rate on the 314-episode heavy-episode-end pool is approximately 2x the 6.8% corpus baseline, consistent with the parent MD's compensatory-failure interpretation cited at MD-beta section 6.7.

### 1.2 Baseline reproduction: MD-beta section 6.2 byte-for-byte

Source: [`output/md_beta_6_2_streak_distribution.csv`](output/md_beta_6_2_streak_distribution.csv).

| L_bin | n | rate |
|---|---:|---:|
| 1 | 188 | 59.87% |
| 2 | 77 | 24.52% |
| 3 | 27 | 8.60% |
| 4+ | 22 | 7.01% |
| total | 314 | 100.00% |

Sub-bins within 4+ for context, not for primary bins:

| L | n |
|---:|---:|
| 4 | 12 |
| 5 | 6 |
| 6 | 1 |
| 7 | 1 |
| 8 | 1 |
| 10 | 1 |

Reproduces MD-beta section 6.2 counts 188 / 77 / 27 / 22 (total 314) plus the sub-bin 12 / 6 / 1 / 1 / 1 / 1 breakdown byte-for-byte.

### 1.3 Baseline reproduction: MD-beta section 6.3 byte-for-byte

Source: [`output/md_beta_6_3_streak_intensity.csv`](output/md_beta_6_3_streak_intensity.csv).

| L_bin | n_episodes | mean_vh_frac | median_vh_frac | mean_vh_count |
|---|---:|---:|---:|---:|
| 1 | 188 | 0.436 | 0.000 | 0.436 |
| 2 | 77 | 0.481 | 0.500 | 0.961 |
| 3 | 27 | 0.519 | 0.667 | 1.556 |
| 4+ | 22 | 0.538 | 0.550 | 2.636 |

Reproduces MD-beta section 6.3 mean vh_frac 0.436 / 0.481 / 0.519 / 0.538 and mean vh_count 0.436 / 0.961 / 1.556 / 2.636 byte-for-byte to three decimals.

### 1.4 Baseline reproduction: MD-beta section 6.4 byte-for-byte

Source: [`output/md_beta_6_4_streak_era.csv`](output/md_beta_6_4_streak_era.csv).

| Year | n episodes | L=1 | L=2 | L=3 | L=4+ |
|---|---:|---:|---:|---:|---:|
| 2022 | 44 | 26 | 11 | 2 | 5 |
| 2023 | 87 | 59 | 20 | 5 | 3 |
| 2024 | 81 | 50 | 23 | 4 | 4 |
| 2025 | 66 | 37 | 14 | 9 | 6 |
| 2026 (partial Jan-Jun) | 36 | 16 | 9 | 7 | 4 |
| total | 314 | 188 | 77 | 27 | 22 |

Reproduces MD-beta section 6.4 exactly.

### 1.5 Per-bin sample-viability preflight

Source: [`output/preflight_sample_floor.csv`](output/preflight_sample_floor.csv). Informal Wilson-viable floor is n >= 10 exposed per user Option B endorsement (sibling audit section 1.4).

Era-pooled headline cells (all four bins pass):

| L_bin | n_episodes | n_crashes | Wilson-viable pass |
|---|---:|---:|---|
| 1 | 188 | 28 | pass |
| 2 | 77 | 10 | pass |
| 3 | 27 | 5 | pass |
| 4+ | 22 | 3 | pass |

Era-stratified companion cells (2 of 8 fail the informal floor):

| L_bin | era | n_episodes | n_crashes | Wilson-viable pass |
|---|---|---:|---:|---|
| 1 | pre_cital | 100 | 19 | pass |
| 2 | pre_cital | 39 | 6 | pass |
| 3 | pre_cital | 8 | 3 | FAIL |
| 4+ | pre_cital | 9 | 1 | FAIL |
| 1 | post_cital | 88 | 9 | pass |
| 2 | post_cital | 38 | 4 | pass |
| 3 | post_cital | 19 | 2 | pass |
| 4+ | post_cital | 13 | 2 | pass |

Intensity-stratified companion cells (all 8 pass at informal-floor n >= 10, though the tightest cells n=11 will have wide Wilson CIs):

| L_bin | stratum | n_episodes | Wilson-viable pass |
|---|---|---:|---|
| 1 | low_vh_frac_le_05 | 106 | pass |
| 2 | low_vh_frac_le_05 | 56 | pass |
| 3 | low_vh_frac_le_05 | 13 | pass |
| 4+ | low_vh_frac_le_05 | 11 | pass |
| 1 | high_vh_frac_gt_05 | 82 | pass |
| 2 | high_vh_frac_gt_05 | 21 | pass |
| 3 | high_vh_frac_gt_05 | 14 | pass |
| 4+ | high_vh_frac_gt_05 | 11 | pass |

Two failing cells (L=3 pre-cital n=8; L=4+ pre-cital n=9) fall in the section 4 era-stratified companion; they are reported narrative-only at section 4.1.

---

## 2. Reproducibility

- **Script**: [`scripts/stage_d_streak_length.py`](scripts/stage_d_streak_length.py). Idempotent, re-runnable, single entry point.
- **Data**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`; expected LC-era stratum n=1524 rows.
- **Dump version**: v3.2 or current locked dump per user working state 2026-07-19.
- **Random seed**: 20260716 per MD-beta section 4.5.
- **Statistical machinery** per MD-beta section 4.5:
  - Wilson 95% CI on per-bin crash rate via `statsmodels.stats.proportion.proportion_confint(method='wilson')` at alpha=0.05.
  - Cochran-Armitage trend test manual implementation using the Armitage 1955 linear-score statistic with row_scores = [1, 2, 3, 4] for L_bin in {1, 2, 3, 4+} and col_scores = [0, 1] for crash_in_5d; Z + asymptotic two-sided p via `scipy.stats.norm`. Descriptive-only per CONVENTIONS section 2.1.
  - Permutation-null companion on Cochran-Armitage Z: B = 10000 permutations of L_bin labels within the episode-end pool, block length = 1 per MD-beta section 4.5 primary, seed = 20260716.
  - Bootstrap 95% CI on per-bin crash rate: B = 10000 episode-level resamples, block length = 1 primary, percentile 2.5 / 97.5.
  - Sensitivity companion at E[L]*-block-length stationary bootstrap: fires when the E[L]* factor-of-2 flag trips per section 6.
- **NaN handling**: `is_crash` propagates as False under `.fillna(False)`; no other operand-side NaN handling required (streak_length is a structural count, not an operand with NaN semantics). Episodes with truncated crash-window are excluded from crash-in-5d cells (`crash_window_full == True` filter).
- **Era stratifier**: pre_cital = D_end < 2024-04-09; post_cital = D_end >= 2024-04-09.
- **Unit of analysis**: episode-end at gap=0 contiguous heavy runs, inherited from MD-beta section 2 + parent Q24 MD section 3.1.
- **L_bin ordinal encoding**: {1: 1, 2: 2, 3: 3, 4+: 4} for Cochran-Armitage row_scores per MD-beta section 4.5.

---

## 3. Headline: crash rate by L_bin, era-pooled

**Primary operand**: `streak_length(D_end) = |{contiguous heavy days ending at D_end}|` per MD-beta section 4.1.
**L_bin mapping**: {1, 2, 3, 4+} per MD-beta section 4.1 with 4+ merging 4 / 5 / 6 / 7 / 8 / 10 sub-bins.
**Outcome**: `crash_in_5d(D_end) = any(is_crash[d] for d in [D_end+1, D_end+5])` per MD-beta section 4.2.
**Direction pre-commit** per MD-beta section 4.4: longer streaks -> HIGHER crash rate (dose-response, cumulative-load reading).

Source: [`output/per_bin_crash_rate.csv`](output/per_bin_crash_rate.csv) rows era=ALL.

### 3.1 Per-bin crash rates + Wilson 95% CIs

| L_bin | n_episodes | n_crashes | crash_rate | Wilson 95% lo | Wilson 95% hi | Bootstrap 95% lo | Bootstrap 95% hi | Floor pass |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 188 | 28 | 14.89% | 10.51% | 20.68% | 10.11% | 20.21% | pass |
| 2 | 77 | 10 | 12.99% | 7.21% | 22.28% | 6.49% | 20.78% | pass |
| 3 | 27 | 5 | 18.52% | 8.18% | 36.70% | 3.70% | 33.33% | pass |
| 4+ | 22 | 3 | 13.64% | 4.75% | 33.33% | 0.00% | 27.27% | pass |

Companion: per-bin RR versus L=1 as reference (source [`output/per_bin_rr_vs_L1.csv`](output/per_bin_rr_vs_L1.csv)):

| L_bin | RR vs L=1 | Bootstrap 95% lo | Bootstrap 95% hi |
|---|---:|---:|---:|
| 1 | 1.000 | 0.605 | 1.650 |
| 2 | 0.872 | 0.376 | 1.628 |
| 3 | 1.243 | 0.303 | 2.611 |
| 4+ | 0.916 | 0.000 | 2.229 |

All three non-reference bins have bootstrap 95% CIs on RR that include 1.0. The point estimates are non-monotonic: crash rate is 14.89% at L=1, drops to 12.99% at L=2, rises to 18.52% at L=3, drops again to 13.64% at L=4+.

### 3.2 Cochran-Armitage trend test

Source: [`output/cochran_armitage_trend.csv`](output/cochran_armitage_trend.csv) row era=ALL.

- Row_scores = [1, 2, 3, 4] for L_bin in {1, 2, 3, 4+}
- Col_scores = [0, 1] for crash_in_5d in {False, True}
- n_episodes = 314; n_crashes = 46
- **Z_asymptotic = 0.025**
- **p_asymptotic two-sided = 0.9804**
- **p_permutation two-sided (B = 10000, block length = 1, seed = 20260716) = 0.9675**
- null Z quantiles (permutation): 2.5% = -1.907, median = 0.025, 97.5% = 1.956

Descriptive-only per CONVENTIONS section 2.1. Z_observed = 0.025 is exactly at the null-median (rounded to three decimals) with p_asymptotic 0.9804 and p_permutation 0.9675; both p-values are far above conventional thresholds. The permutation and asymptotic p-values are close, indicating the asymptotic reference distribution is well-calibrated at this sample size.

### 3.3 Descriptive observation

The section 3.1 per-bin rates are **non-monotonic** and the section 3.2 Cochran-Armitage Z sits essentially at the null-median. The MD-beta section 4.4 direction pre-commit was longer streaks -> HIGHER crash rate; the observed pattern does not support that pre-commit direction at descriptive-with-CI resolution. Per [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), this is a substantive descriptive finding: the era-pooled per-bin crash rate does not show the predicted dose-response.

Specifically:
- L=1 (n=188, 14.9%) and L=2 (n=77, 13.0%) sit close to each other and close to the pool baseline of 14.6%.
- L=3 (n=27, 18.5%) sits slightly above; the L=3 vs L=1 RR = 1.24 with bootstrap 95% CI (0.30, 2.61) is compatible with the pre-commit direction but the CI is wide and includes 1.0.
- L=4+ (n=22, 13.6%) is below L=3 and near L=1; the L=4+ vs L=1 RR = 0.92 with bootstrap 95% CI (0.00, 2.23) is compatible with either direction and includes 1.0.

The read at Stage D is: **the era-pooled per-bin crash rate does not show the MD-beta section 4.4 pre-commit monotonic dose-response direction**. Whether this reflects (i) a genuine flat dose-response of streak-length on crash-in-5d, (ii) sample-floor sparsity at the L=3 and L=4+ bins (wide Wilson CIs 8.2% to 36.7% at L=3 and 4.7% to 33.3% at L=4+ both include L=1's point estimate and each other), (iii) intensity confounding per MD-beta section 5 confound 2 diluting the streak-length signal (see section 5), (iv) era instability of the sign (see section 4), or (v) rolling-window autocorrelation inflating the effective sample size beyond the 314 episode count (see section 6) is descriptive-open at Stage D; no verdict is emitted here per CONVENTIONS section 2.1.

Circularity with parent Q24 MD section 3.5 pool-split per MD-beta section 5 confound 6: the crash_in_5d outcome sample is shared with the parent Q24 MD Stage D r4 audit. This section 3 finding is NOT independent evidence relative to the parent MD's pool-split-based reads; any Stage S1 synthesis must pick one of {this MD, parent Q24 MD} as headline per Q24 sub-part and cite the other as complementary. See section 8 for the shared-sample framing.

---

## 4. Era-stratified sensitivity

Same operand and outcome as section 3, split at the citalopram-onset era boundary 2024-04-09 per MD-beta section 5 confound 3 (streak-length x era) + section 5 confound 7 (envelope-drift asymmetry). Side-by-side reporting per the sibling audit section 4 discipline.

### 4.1 Pre-cital era (2022-04-04 to 2024-04-08)

Source: [`output/per_bin_crash_rate.csv`](output/per_bin_crash_rate.csv) rows era=pre_cital.

| L_bin | n_episodes | n_crashes | crash_rate | Wilson 95% lo | Wilson 95% hi | Floor pass |
|---|---:|---:|---:|---:|---:|---|
| 1 | 100 | 19 | 19.00% | 12.51% | 27.78% | pass |
| 2 | 39 | 6 | 15.38% | 7.25% | 29.73% | pass |
| 3 | 8 | 3 | 37.50% | 13.68% | 69.43% | FAIL (narrative-only) |
| 4+ | 9 | 1 | 11.11% | 1.99% | 43.50% | FAIL (narrative-only) |

**NEEDS-MORE-DATA notes** for the two failing cells:

- L=3 pre-cital: 3 / 8 = 37.5% raw. The Wilson CI (13.7%, 69.4%) is mathematically computable but is deliberately not treated as an evidential surface at this floor per the sibling audit section 6.5 Wilson-computable-but-withheld policy. The script writes the Wilson bounds to the output CSV for reproducibility trace; the audit body treats the cell as narrative-only per user Option B endorsement.
- L=4+ pre-cital: 1 / 9 = 11.1% raw. Same policy.

Pool rate on pre-cital era: 29 / 156 = 18.59% (higher than the pool-baseline of 14.65% by roughly 4 percentage points; the pre-cital pool has a substantially higher crash-in-5d rate than the post-cital pool per section 4.2).

### 4.2 Post-cital era (2024-04-09 to 2026-06-05)

Source: [`output/per_bin_crash_rate.csv`](output/per_bin_crash_rate.csv) rows era=post_cital.

| L_bin | n_episodes | n_crashes | crash_rate | Wilson 95% lo | Wilson 95% hi | Floor pass |
|---|---:|---:|---:|---:|---:|---|
| 1 | 88 | 9 | 10.23% | 5.47% | 18.31% | pass |
| 2 | 38 | 4 | 10.53% | 4.17% | 24.13% | pass |
| 3 | 19 | 2 | 10.53% | 2.94% | 31.39% | pass |
| 4+ | 13 | 2 | 15.38% | 4.33% | 42.23% | pass |

Pool rate on post-cital era: 17 / 158 = 10.76%.

### 4.3 Cochran-Armitage trend per era

Source: [`output/cochran_armitage_trend.csv`](output/cochran_armitage_trend.csv).

| era | n_episodes | n_crashes | Z_asymptotic | p_asymptotic | p_permutation (B=10000) |
|---|---:|---:|---:|---:|---:|
| ALL | 314 | 46 | 0.025 | 0.9804 | 0.9675 |
| pre_cital | 156 | 29 | -0.060 | 0.9522 | 1.0000 |
| post_cital | 158 | 17 | 0.433 | 0.6654 | 0.6934 |

The pre-cital Z is slightly negative (opposite sign to the pre-commit direction); post-cital Z is slightly positive (matches the pre-commit direction sign). Both era-stratified Z statistics have two-sided p-values above 0.65; neither individually excludes the null under the descriptive-only framing.

### 4.4 Descriptive comparison

The per-bin crash rate on the pre-cital era shows a rough non-monotonic pattern with L=3 elevated (37.5% raw, narrative-only) and L=4+ suppressed (11.1%, narrative-only) relative to L=1 (19.0%) and L=2 (15.4%); the two elevated / suppressed cells fail the informal floor and are not the load-bearing surface. On the L=1 and L=2 bins alone the pre-cital era is roughly flat (19.0% vs 15.4%).

The post-cital era shows a roughly flat rate at L=1, L=2, L=3 (all near 10.5%) with a modest rise at L=4+ (15.4%, Wilson 4.3% to 42.2%). The post-cital Cochran-Armitage Z = 0.433 is directionally consistent with the pre-commit but well within the null.

Per-era Wilson CIs on every bin include the pool-baseline of the corresponding era; no bin's Wilson CI excludes the baseline. The era-stratified per-bin reads are compatible with a flat dose-response within each era.

Cross-era observation: the era-pool-baseline shift is substantial (pre-cital 18.6% vs post-cital 10.8%), consistent with the parent MD's envelope-drift caveat and with the sibling audit section 4 rest-adjacency era instability. The 6-mechanism era caveat below applies to this era shift verbatim.

### 4.5 6-mechanism era caveat (verbatim per MD-beta section 5 confound 7)

The pre-cital vs post-cital era stratifier is a temporal anchor at 2024-04-09 (citalopram onset). Any RR difference between the two strata conflates at least six co-occurring factors:

1. Citalopram pharmacological effect.
2. Learned-pacing behavioural evolution (per MD-alpha section 3.6 five-confound bundle).
3. Tactical-Garmin-use improvement (per memory `project_garmin_research_bias_boundary`).
4. Natural LC disease-course trajectory.
5. Envelope drift (documented in MD-alpha Wave 2A audit section 8 pre-window mean-level shift; per Wave 2D section 10.3 the pre-window `effective_exertion_min` per day mean is 19.39 min/day on `pacing_habit_established` vs 5.17 min/day on `citalopram_modulated`, a ~4x shift at the phase boundary).
6. Aging + seasonality across the ~2-year window.

The stratifier does NOT identify medication effect at n=1. It is a temporal anchor for descriptive era-stratified reads. No causal claim about medication is made or supported by this stratifier. Any interpretation attributing an era-stratum crash-rate difference to citalopram specifically is out of scope for this Stage D audit and would require a between-participant or within-participant crossover design not available at n=1.

---

## 5. Intensity-adjusted companion (streak x vh_frac stratifier)

Same operand and outcome as section 3, cross-stratified by per-episode intensity fingerprint. Per MD-beta section 5 confound 2 the streak-length arc requires an intensity-adjusted companion because longer streaks accumulate more very_heavy days by construction (MD-beta section 6.3 empirical anchor: mean vh_frac rises from 0.436 at L=1 to 0.538 at L=4+). Framed as a Stage D descriptive companion per MD-beta section 5 confound 2 Stage D handling paragraph.

Source: [`output/intensity_stratified.csv`](output/intensity_stratified.csv).

### 5.1 Reproduce MD-beta section 6.3 streak x intensity fingerprint

Reproduced at section 1.3 above (mean vh_frac 0.436 / 0.481 / 0.519 / 0.538; mean vh_count 0.436 / 0.961 / 1.556 / 2.636 across L in {1, 2, 3, 4+}). The mean vh_frac is only mildly monotonically increasing with L_bin per MD-beta section 6.3 interpretive discipline (0.44 to 0.54 over the four bins); the intensity-adjusted companion below tests whether the flat era-pooled dose-response persists on subsets restricted to a common intensity band.

### 5.2 Intensity-restricted crash-rate: streak x crash-rate on low-vh-frac subset (vh_frac <= 0.5)

| L_bin | n_episodes | n_crashes | crash_rate | Wilson 95% lo | Wilson 95% hi | Floor pass |
|---|---:|---:|---:|---:|---:|---|
| 1 | 106 | 21 | 19.81% | 13.34% | 28.40% | pass |
| 2 | 56 | 7 | 12.50% | 6.19% | 23.63% | pass |
| 3 | 13 | 2 | 15.38% | 4.33% | 42.23% | pass |
| 4+ | 11 | 1 | 9.09% | 1.62% | 37.74% | pass |

Cochran-Armitage on low_vh_frac subset: Z = **-1.189** (asymptotic two-sided p = 0.234). Sign is negative (opposite to pre-commit direction); descriptive-only.

### 5.3 Intensity-restricted crash-rate: streak x crash-rate on high-vh-frac subset (vh_frac > 0.5)

| L_bin | n_episodes | n_crashes | crash_rate | Wilson 95% lo | Wilson 95% hi | Floor pass |
|---|---:|---:|---:|---:|---:|---|
| 1 | 82 | 7 | 8.54% | 4.20% | 16.59% | pass |
| 2 | 21 | 3 | 14.29% | 4.98% | 34.64% | pass |
| 3 | 14 | 3 | 21.43% | 7.57% | 47.59% | pass |
| 4+ | 11 | 2 | 18.18% | 5.14% | 47.70% | pass |

Cochran-Armitage on high_vh_frac subset: Z = **1.508** (asymptotic two-sided p = 0.131). Sign is positive (matches pre-commit direction); descriptive-only.

### 5.4 Descriptive observation

The intensity-stratified companion reveals a **directionally-opposite pattern by intensity stratum**:

- **Low vh_frac subset (episodes where <= 50% of days are very_heavy)**: crash rate is highest at L=1 (19.8%) and drops slightly at L=2 through L=4+ (12.5% / 15.4% / 9.1%). Cochran-Armitage Z = -1.19, sign opposite the pre-commit direction; Wilson CIs on all four bins overlap.
- **High vh_frac subset (> 50% of days very_heavy)**: crash rate rises with L_bin (L=1 8.5%, L=2 14.3%, L=3 21.4%, L=4+ 18.2%). Cochran-Armitage Z = +1.51, sign matches the pre-commit direction; Wilson CIs on all four bins overlap.

The pattern is descriptively consistent with **intensity being the load-bearing signal, not streak length** in the era-pooled contrast at section 3. On the low-intensity subset the streak-length signal is absent or inverted; on the high-intensity subset it is directionally present but with wide CIs. Per MD-beta section 5 confound 2 the streak-length arc primary contrast at section 3 has been diluted by pooling across intensity strata that carry opposing signals; the flat era-pooled Cochran-Armitage Z = 0.025 is at least partially explained by the intensity-stratum sign cancellation.

The low-vh-frac L=1 crash rate (19.8%) is materially higher than the high-vh-frac L=1 crash rate (8.5%). At L=4+ the ordering reverses: high-vh-frac 4+ is at 18.2%, low-vh-frac 4+ is at 9.1%. The intensity signal on crash rate is bin-dependent; this is a substantive descriptive finding on the intensity confound but does NOT resolve into a clean streak-length dose-response either.

Sample-viability note: the tightest cells at n=11 (L=4+ on both strata) and n=13 (L=3 low-vh-frac) have Wilson CIs that span 30+ percentage points; the intensity-stratified reads are exploratory descriptive companions per MD-beta section 5 confound 2 Stage D handling, not the primary read.

**Descriptive-only framing restatement** (mirroring the section 3.2 discipline at the era-pooled cell): the low-vh-frac Cochran-Armitage p_asymptotic = 0.234 and high-vh-frac p_asymptotic = 0.131 are both well above conventional thresholds and are reported here descriptively per CONVENTIONS section 2.1. Neither Z is treated as an inferential verdict at Stage D; both are companion diagnostics on the confounding-with-intensity concern named at MD-beta section 5 confound 2. The section 8 multiple-testing surface attestation covers this globally; the restatement here is at the specific cell where the temptation to over-read a moderate-magnitude Z is real (Z = 1.51 is the largest |Z| in the audit at approximately 1.5 standard deviations from null).

Descriptive-only per CONVENTIONS section 2.1; no verdicts.

---

## 6. Rolling-window-predictor autocorrelation diagnostic (per §4.7 + HA-P7 §4.6 template)

Per MD-beta section 4.7 + [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) section 2 + HA-P7 verdict-review section 4.6 closure template.

Source: [`output/el_star_diagnostic.csv`](output/el_star_diagnostic.csv) + [`output/el_star_4plus_dates.csv`](output/el_star_4plus_dates.csv) + [`output/el_star_4plus_pair_details.csv`](output/el_star_4plus_pair_details.csv).

### 6.1 Streak-length day-level lag-1 autocorrelation

Day-level streak_length sequence on LC-era stratum: for each of 1524 LC-era days, the length of the contiguous heavy run that day belongs to (0 if the day is not heavy). Summary:

| Measure | Value |
|---|---:|
| n_days_lc_stratum | 1524 |
| day-level streak_length mean | 0.873 |
| day-level streak_length max | 10 |
| day-level streak_length zero fraction | 65.1% |
| lag-1 autocorrelation (rho_1) | 0.664 |

The lag-1 autocorrelation of 0.664 is high by construction: within a single heavy episode, day D and day D+1 share the streak_length identity because both belong to the same contiguous run. This structural autocorrelation is the rolling-window-predictor concern named at MD-beta section 4.7.

### 6.2 E[L]* computation

Using the pragmatic Politis-White-style ACF-summation estimator (same estimator as HA-P7 [`sensitivity_block_length.py`](../../hypotheses/HA-P7/sensitivity_block_length.py) implementation cited in MD-beta section 4.7):

`E[L]* = 1 + 2 * sum_{h=1..H} rho_h` where H is the first h at which `|rho_h| < 2 / sqrt(n)` (Bartlett band).

Result: **E[L]* = 7.80 days** on the day-level streak_length sequence.

The locked block length under MD-beta section 4.5 primary is 1 (episode-end unit-of-analysis argument per parent MD section 7.10). E[L]* / locked = 7.80x, which is above the factor-of-2 flag threshold per MD-beta section 4.7 + `permutation_null_block_length.md` section 2. **FLAGGED per HA-P7 section 4.6 closure template.**

### 6.3 Streak-clustering probe: multiple 4+ streaks within 30d window

Source: [`output/el_star_4plus_pair_details.csv`](output/el_star_4plus_pair_details.csv).

22 L=4+ episodes total; 8 pairs of L=4+ episodes fall within a 30-day rolling window of each other. The clusters:

| Pair a | Pair b | Days apart |
|---|---|---:|
| 2022-07-20 | 2022-07-28 | 8 |
| 2022-07-20 | 2022-08-03 | 14 |
| 2022-07-28 | 2022-08-03 | 6 |
| 2025-06-07 | 2025-06-12 | 5 |
| 2025-06-07 | 2025-06-21 | 14 |
| 2025-06-12 | 2025-06-21 | 9 |
| 2025-08-08 | 2025-08-29 | 21 |
| 2026-03-12 | 2026-04-10 | 29 |

The 22 L=4+ episodes are not uniformly distributed across the LC era; they cluster in three tight windows (July-August 2022 with 3 episodes in 14 days; June 2025 with 3 episodes in 14 days; August 2025 with 2 episodes 21 days apart; March-April 2026 with 2 episodes 29 days apart). This is the specific clustering behaviour the MD-beta section 4.7 anticipatory-drafting note flagged as a review trigger.

### 6.4 Diagnostic verdict: block length = 1 appropriate, or flag per HA-P7 template

**FLAGGED per HA-P7 section 4.6 closure template + `permutation_null_block_length.md` section 2 factor-of-2 rule.**

E[L]* = 7.80 exceeds 2 * locked_block_length = 2 substantially (factor of 7.80). The flag is triggered at both (i) the ACF-derived Politis-White estimator level and (ii) the empirical clustering probe level (8 pairs of L=4+ within 30d; 22 episodes cluster in 3-4 tight windows).

**Note on unit-of-analysis compression**: per MD-beta section 4.7, the episode-end unit-of-analysis already deflects most of the autocorrelation concern by emitting a single value per episode-end. The day-level lag-1 autocorrelation (0.664) is computed on the day-level rolling-identifier form, not on the episode-level unit-of-analysis. The section 4.7 rationale for locked block length = 1 at the episode-level unit stands independently of the day-level E[L]* diagnostic; the diagnostic is a foreseen review trigger, not a hard override. Per HA-P7 section 4.6 closure template, the appropriate response is (a) cite the structural clustering explicitly (done at section 6.3), (b) recompute per-bin bootstrap CI at E[L]*-block-length as a sensitivity companion (section 6.5 below), (c) verify verdict robustness across block-length arms.

### 6.5 Sensitivity companion at E[L]*-block-length permutation null

Per section 6.4 flag response, per-bin bootstrap CI on crash rate at E[L]*-block-length stationary bootstrap (mean geometric block length rounded to E[L]* = 8; Politis-Romano stationary bootstrap; block length drawn from geometric distribution with mean 8; wrap-around continuation; B = 10000; seed = 20260716; ordered by D_end within each bin). Source: [`output/per_bin_boot_at_el_star.csv`](output/per_bin_boot_at_el_star.csv).

| L_bin | n_episodes | n_crashes | crash_rate | Bootstrap 95% lo (E[L]*=8) | Bootstrap 95% hi (E[L]*=8) |
|---|---:|---:|---:|---:|---:|
| 1 | 188 | 28 | 14.89% | 9.04% | 20.74% |
| 2 | 77 | 10 | 12.99% | 6.49% | 20.78% |
| 3 | 27 | 5 | 18.52% | 3.70% | 33.33% |
| 4+ | 22 | 3 | 13.64% | 4.55% | 22.73% |

Comparison with the locked-block-length=1 primary bootstrap CIs at section 3.1:

| L_bin | primary boot 95% (block=1) | sensitivity boot 95% (block=8, E[L]*) |
|---|---|---|
| 1 | (10.11%, 20.21%) | (9.04%, 20.74%) |
| 2 | (6.49%, 20.78%) | (6.49%, 20.78%) |
| 3 | (3.70%, 33.33%) | (3.70%, 33.33%) |
| 4+ | (0.00%, 27.27%) | (4.55%, 22.73%) |

The E[L]* = 8 stationary-bootstrap CIs sit close to the primary block-length-1 CIs on L=1, L=2, and L=3 (differences in the low single-percentage-point range). At L=4+ the E[L]* CI is slightly narrower (4.55% to 22.73% vs 0.00% to 27.27% primary); this is a small-sample artefact where the stationary-bootstrap block length (8) is comparable to the arm-size 22 (ratio 2.75x, marginal for stationary bootstrap). The same class of small-sample artefact applies to the **L=3 arm (n=27, arm-to-block ratio 3.4x)**, which is also marginal for stationary bootstrap; at both L=3 and L=4+ the E[L]* = 8 stationary-bootstrap CI is a companion diagnostic rather than a strict correction, and the audit does not treat either CI as a verdict-changing surface at Stage D.

**Verdict robustness across block-length arms**: the non-monotonic per-bin pattern surfaced at section 3.1 (L=1 14.9%, L=2 13.0%, L=3 18.5%, L=4+ 13.6%) is preserved under the E[L]*-block-length sensitivity companion; the block-length flag does NOT change the descriptive pattern or the section 3.3 read that the era-pooled per-bin crash rate does not show the MD-beta section 4.4 pre-commit monotonic dose-response direction. Per HA-P7 section 4.6 closure template step (c), verdict robustness across block-length arms is confirmed at the descriptive-with-CI level.

**Framing note**: E[L]* * n_episodes / n_days_lc_stratum = 7.80 * 314 / 1524 = 1.61 effective independent-episode ratio; the effective sample size at the episode level is roughly 1.61x smaller than the raw 314 count would suggest under the day-level autocorrelation reading. This does NOT materially widen the CIs above at the episode-level bootstrap, because the episode-end unit-of-analysis is already downsampled per MD-beta section 4.7 (heavy-episode boundaries are event-triggered, not fixed windows). The effective-independent-episode framing is a companion diagnostic, not a correction pre-committed at Stage D.

---

## 7. Descriptive observations

### 7.1 Dose-response relative to section 4.4 pre-commit direction

Section 3.1 per-bin era-pooled crash rates: 14.9% / 13.0% / 18.5% / 13.6% across L in {1, 2, 3, 4+}. Section 3.2 Cochran-Armitage Z = 0.025 with p_asymptotic = 0.9804 and p_permutation = 0.9675. The pattern is **non-monotonic** and the Cochran-Armitage Z sits essentially at the null-median.

The MD-beta section 4.4 pre-commit direction was longer streaks -> HIGHER crash rate; **the observed era-pooled pattern does not support that pre-commit direction at descriptive-with-CI resolution**. Per CONVENTIONS section 4.2 caveat-class framing, the pre-commit direction is not confirmed by this Stage D descriptive audit; whether the flat pattern is genuine or reflects sample-floor sparsity, intensity confounding, era instability, or rolling-window autocorrelation inflating effective sample size is descriptive-open per section 3.3.

### 7.2 Sign-inversions or non-monotonicity, if any

- **Section 3.1 non-monotonicity**: era-pooled L=3 (18.5%) sits above L=1 (14.9%), but L=4+ (13.6%) drops back below L=3. RR vs L=1 point estimates at 1.24 (L=3) and 0.92 (L=4+) are on opposite sides of 1.0 with overlapping bootstrap CIs.
- **Section 4 pre-cital era**: L=3 raw rate 37.5% (narrative-only, n=8) is the highest observed per-bin rate anywhere in the audit; L=4+ raw rate 11.1% (narrative-only, n=9) is among the lowest. Both cells fail the informal floor and are not load-bearing.
- **Section 5.2 low-vh-frac sub-stratum**: sign-inverted Cochran-Armitage Z = -1.19; crash rate at L=1 (19.8%) is the highest in the sub-stratum.
- **Section 5.3 high-vh-frac sub-stratum**: Cochran-Armitage Z = +1.51, sign matches pre-commit direction.

The sign-inversion-by-intensity-stratum surfaced at section 5.4 is the substantive descriptive finding of this audit alongside the era-pooled flat pattern of section 3.

### 7.3 Era instability

Per section 4.3 Cochran-Armitage Z: pre-cital Z = -0.06 (slight sign inversion); post-cital Z = +0.43 (matches pre-commit direction sign but well within null). Per-era pool-baseline crash rates differ substantially (pre-cital 18.6% vs post-cital 10.8%); the era-pool-baseline shift is documented under the section 4.5 6-mechanism caveat and inherits the parent MD's envelope-drift caveat verbatim. No causal attribution to any single mechanism (medication, learned pacing, envelope drift, natural LC course, seasonality, aging) at n=1.

### 7.4 Intensity confound reading

Per section 5.4 the streak-length signal on crash rate reads differently across low-vh-frac vs high-vh-frac subsets: low-vh-frac shows an inverted (or absent) dose-response; high-vh-frac shows a directional dose-response consistent with the pre-commit but with wide CIs. Per MD-beta section 5 confound 2 (streak x intensity), the streak-length arc is confounded with intensity by construction (mean vh_frac rises monotonically across L_bins per MD-beta section 6.3); the intensity-stratified companion partial-decouples the two axes and reveals that intensity carries at least part of the section 3 signal that would otherwise be attributed to streak length alone. Descriptive-only per CONVENTIONS section 2.1.

### 7.5 Discipline reminder: circularity with parent Q24 MD

Per MD-beta section 5 confound 6, the crash_in_5d outcome sample is shared with the parent Q24 MD Stage D r4 audit at [`../Q24-post-heavy-trajectory/descriptive_audit.md`](../Q24-post-heavy-trajectory/descriptive_audit.md) LOCKED r4 (the sibling artefact on the shared 314-episode pool). This audit's section 3 headline and every companion in sections 4 through 6 read on the SAME 314-episode-end pool as the parent MD's compensatory-success vs compensatory-failure pool-split analysis. Any Stage S1 synthesis must pick ONE of {this MD, parent Q24 MD} as headline per Q24 sub-part and cite the other as complementary; the two Stage D findings are NOT independent evidence at the Stage S1 level. This section 3 finding descriptively coexists with the parent MD's Stage D r4 §3 pool-split anchor (crash-rate on strict-clean +5d = 9/52 = 17.3%; this audit's all-episodes pool rate = 46/314 = 14.65%) without duplicating the descriptive surface. The parent MD Stage D r4 audit is the sibling read on the same sample; a Stage S1 reader navigating from this audit should read both in tandem before picking the headline framing.

### 7.6 Rolling-window autocorrelation caveat

Per section 6, the E[L]* = 7.80 factor-of-2 flag is triggered at the day-level ACF diagnostic. The section 6.5 sensitivity companion at E[L]*-block-length stationary bootstrap preserves the section 3.1 non-monotonic descriptive pattern; the block-length flag does not sign-invert the finding. The clustering probe (section 6.3) documents that 8 pairs of L=4+ episodes fall within 30 days of each other, concentrated in 3-4 tight windows (July-August 2022; June 2025; August 2025; March-April 2026). The effective independent-episode count is roughly 314 / 7.80 * (day-level heavy fraction 532 / 1524) = ~14 in the strictest reading, though the episode-end unit-of-analysis already deflects most of this concern per MD-beta section 4.7. Caveat-class per CONVENTIONS section 4.2; not a correction.

---

## 8. Discipline compliance attestations

- **CONVENTIONS section 2.1 descriptive-before-inference**: no inferential verdicts emitted at Stage D; Cochran-Armitage Z + asymptotic p + permutation p reported for completeness only per MD-beta section 4.5 statistical-framing note; per-bin RR vs L=1 reported as descriptive companion.
- **CONVENTIONS section 3.1 personal-baseline discipline**: streak_length is a structural count on the LC-era stratum, not a threshold-based operand; no personal-baseline concern. Wilson CIs use the standard normal-approximation-corrected form; Bootstrap CIs use block length = 1 primary + E[L]*-block-length sensitivity companion.
- **CONVENTIONS section 3.6 named-count discipline**: all counts named with scheme (episode-end at gap=0 heavy runs, `is_crash` day-level column, `crash_in_5d` derived indicator) + unit (episodes, days, LC-era stratum) + source (MD-beta section, script output CSV path, parent Stage -1 audit reference).
- **CONVENTIONS section 3.10 NaN-boundary rule**: `is_crash` NaN propagates as False per parent MD convention; no other operand-side NaN semantics are load-bearing for streak_length. Episodes with truncated crash-window (`crash_window_full == False`) are excluded from every per-bin cell.
- **CONVENTIONS section 4.2 caveat-class framing**: all MD-beta section 5 confounds 2 (streak x intensity), 3 (streak x era), 5 (rolling-sum autocorrelation), 6 (circularity with parent Q24), 7 (envelope-drift) acknowledged as caveats, not corrections. No post-hoc adjustment attempted at Stage D.
- **Descriptive-before-theory discipline** (user 2026-07-17 directive): NO citation of `resilience_latent_state.md`; NO latent-state / R(t) / reserve / buffer / envelope-capacity constructs anywhere in this audit; the cumulative-load framing at MD-beta section 4.4 is cited as descriptive dose-response reading only, without appeal to any latent-capacity mechanism.
- **6-mechanism era caveat** per MD-beta section 5 confound 7: verbatim at section 4.5; no causal attribution to any single mechanism (medication, pacing, Garmin use, LC course, envelope drift, aging + seasonality) at n=1.
- **Circularity with parent Q24 MD** per MD-beta section 5 confound 6: shared 314-episode crash-in-5d outcome sample explicitly documented at section 3.3 and section 7.5; Stage S1 must pick one of {this MD, parent Q24 MD} as headline per Q24 sub-part.
- **Rolling-window-predictor autocorrelation flag** per MD-beta section 4.7: E[L]* diagnostic computed at section 6.2; factor-of-2 flag triggered; sensitivity companion at E[L]*-block-length reported at section 6.5 per HA-P7 section 4.6 closure template; verdict robustness across block-length arms confirmed at the descriptive-with-CI level.
- **Wilson-viable floor** per user Option B endorsement: informal ~10-per-arm threshold; two failures at section 4.1 (L=3 pre-cital n=8; L=4+ pre-cital n=9) reported narrative-only per sibling audit section 6.5 Wilson-computable-but-withheld policy.
- **Multiple-testing surface disclosure**: this audit reports 20 per-bin cells (12 headline + era-stratified = 4 bins x 3 eras) + 8 intensity-stratified cells (4 bins x 2 strata) + 4 E[L]*-block-length sensitivity cells + 3 Cochran-Armitage Z statistics (era-pooled, pre-cital, post-cital) + 2 Cochran-Armitage Z statistics on intensity strata. All p-values (asymptotic + permutation) are descriptive-only per CONVENTIONS section 2.1; the largest p-value in the audit is the era-pooled Cochran-Armitage p_asymptotic = 0.9804 (essentially the null); the smallest asymptotic p in the audit is on the intensity-stratified high-vh-frac stratum at Z = 1.51 p = 0.131 (well above conventional thresholds). No single p crosses to a verdict at Stage D. Descriptive-with-CI is the primary evidential surface; Cochran-Armitage p a completeness column.
- **No em-dash in any output text** per memory `feedback_no_emdash_in_ui`.
- **No emoji anywhere** in the audit MD or the script.

---

## 9. Lock log

| version | date | change |
|---|---|---|
| r1 DRAFT | 2026-07-19 | Initial DRAFT for fresh-session review. Producer-mode subagent draft per CONVENTIONS section 1.2 under user delegation (authorising user: Willem). Walks MD-beta section 4 streak-length arc: per-bin crash rate on L_bin in {1, 2, 3, 4+} era-pooled headline + immediate era-stratified companions (pre-cital + post-cital); Cochran-Armitage trend test per era; per-bin RR vs L=1 as descriptive companion; intensity-stratified sensitivity companion on vh_frac <= 0.5 vs vh_frac > 0.5 sub-strata; E[L]* rolling-window autocorrelation diagnostic per MD-beta section 4.7 + HA-P7 section 4.6 template; E[L]*-block-length stationary-bootstrap sensitivity companion when the factor-of-2 flag trips. Preflight sample-floor probe enumerates 20 headline + era-stratified cells (18 pass, 2 fail at pre-cital L=3 n=8 and L=4+ n=9) + 8 intensity-stratified cells (all pass). MD-beta sections 6.2 (streak distribution 188/77/27/22), 6.3 (mean vh_frac 0.436/0.481/0.519/0.538; mean vh_count 0.436/0.961/1.556/2.636), 6.4 (streak x era cross-tab), 6.7 (crash-in-5d rate 46/314 = 14.65%) reproduced byte-for-byte per sections 1.2 through 1.4. Statistical machinery per MD-beta section 4.5 (Wilson score CI + Cochran-Armitage trend + Bootstrap CI B=10000 seed=20260716 + permutation-null companion on Cochran-Armitage). Descriptive-only per CONVENTIONS section 2.1; no verdicts. No latent-state / R(t) / reserve / buffer / envelope-capacity constructs; no citation of `resilience_latent_state.md` per user 2026-07-17 descriptive-before-theory directive. 6-mechanism era caveat verbatim at section 4.5 per MD-beta section 5 confound 7. E[L]* factor-of-2 flag TRIPPED at E[L]* = 7.80 (day-level lag-1 rho = 0.664) with 8 pairs of L=4+ within 30d clustering probe; HA-P7 section 4.6 closure template applied (cite clustering + recompute at E[L]*-block-length + verify robustness); verdict robustness across block-length arms confirmed at the descriptive-with-CI level. Headline observation: era-pooled Cochran-Armitage Z = 0.025 with p_asymptotic = 0.9804 + p_permutation = 0.9675; per-bin crash rates 14.9% / 13.0% / 18.5% / 13.6% across L_bin {1, 2, 3, 4+} are NON-MONOTONIC and DO NOT support the MD-beta section 4.4 pre-commit direction (longer streaks -> HIGHER crash rate) at descriptive-with-CI resolution. Intensity-stratified companion at section 5 reveals sign-inversion-by-intensity-stratum (low vh_frac Z = -1.19; high vh_frac Z = +1.51) consistent with intensity as the load-bearing signal per MD-beta section 5 confound 2 dilution reading. Awaiting fresh-session review before r1 LOCK. |
| r1 LOCKED | 2026-07-20 | Fresh-session methodology review absorbed from [`../../../reviews/methodology-Q24-mdbeta-stageD-streak-length-2026-07-20.md`](../../../reviews/methodology-Q24-mdbeta-stageD-streak-length-2026-07-20.md) (verdict: DEFENSIBLE with revision; 4 absorb-tier recommendations all applied inline; 0 substantive-tier; 0 escalate-tier; no architectural revision required; HA-P7 section 4.6 closure template treatment praised as substantive-load-bearing PASS at L3.1 + L4.15; non-monotonic pattern framing praised as substantive-load-bearing PASS at L4.7). Four surgical patches per CONVENTIONS section 1.2 compression discipline (mechanical clarifications + framing tightenings + one transcription cleanup; no numerical revision). **Patch 4.1 absorbed** (section 3.2 null Z quantile transcription cleanup per L1.6 + L4.17 absorb): corrected null Z quantile values from "-1.919 / 0.001 / 1.986" to CSV-emitted "-1.907 / 0.025 / 1.956" per `cochran_armitage_trend.csv` row `cochran_armitage_era_ALL`; replaced "Z = 0.025 sits essentially at the null-median (0.001)" with "Z_observed = 0.025 is exactly at the null-median (rounded to three decimals)". Restores byte-for-byte body-CSV match at the specific cell where the audit had diverged; no downstream finding depends on the null-median value. **Patch 4.2 absorbed** (section 5.4 descriptive-only framing restatement at intensity-stratified cells per absorb-tier discretionary): added a new paragraph after the sample-viability note explicitly stating that low-vh-frac p_asymptotic = 0.234 and high-vh-frac p_asymptotic = 0.131 are both well above conventional thresholds and reported descriptively per CONVENTIONS section 2.1, mirroring the section 3.2 discipline; explicitly names the section 8 multiple-testing surface attestation and clarifies that the restatement is at the specific cell where the temptation to over-read a moderate-magnitude Z (Z = 1.51 largest |Z| in the audit) is real. Hardens the descriptive-before-inference gate at the substantive intensity-stratified cell. **Patch 4.3 absorbed** (section 6.5 small-sample-artefact caveat extended to L=3 arm per absorb-tier discretionary): extended the existing "small-sample artefact where the stationary-bootstrap block length is comparable to the arm-size 22" note to also flag the L=3 arm (n=27, arm-to-block ratio 3.4x, marginal for stationary bootstrap); explicitly states at both L=3 and L=4+ the E[L]*=8 stationary-bootstrap CI is a companion diagnostic rather than a strict correction. Hardens the sensitivity-companion caveat at the exact cells where the block-length choice is marginal. **Patch 4.4 absorbed** (section 7.5 explicit file link to parent MD Stage D r4 sibling audit per absorb-tier discretionary): added explicit markdown link to `../Q24-post-heavy-trajectory/descriptive_audit.md` at section 7.5 opening sentence naming it as the sibling artefact on the shared 314-episode pool; added closing sentence stating a Stage S1 reader navigating from this audit should read both in tandem before picking the headline framing. Makes the circularity-with-parent-MD flag actionable at the findings-summary level without a MD-beta lookup. **Preserved byte-identically vs r1 DRAFT**: every per-bin crash rate + Wilson CI + bootstrap CI + Cochran-Armitage Z + permutation p (except the section 3.2 transcription cleanup); MD-beta sections 6.2 / 6.3 / 6.4 / 6.7 baseline reproduction anchors; section 1.5 preflight sample-floor probe (20 + 8 cells; 2 failures); section 2 reproducibility (script path, seed, statistical machinery, NaN handling); section 4.5 6-mechanism era caveat verbatim from MD-beta section 5 confound 7 with MD-alpha Wave 2A envelope-drift anchor (19.39 vs 5.17 min/day); section 5 intensity-stratified companion body (only new descriptive-only-framing paragraph appended in §5.4); section 6 rolling-window autocorrelation diagnostic body (only L=3 caveat extension added at §6.5); section 7 descriptive observations bodies (only sibling-audit link added at §7.5); section 8 discipline compliance attestations preserved verbatim including multiple-testing surface disclosure enumeration; section 3.3 five-candidate-explanation enumeration + circularity-with-parent-MD flag; section 4 era-stratified sensitivity bodies including pre-cital narrative-only for L=3 + L=4+ cells; section 6.5 E[L]*-block-length sensitivity CI table + comparison to primary block-1 CIs; section 6.5 verdict robustness closure statement. **No numerical revisions**: every count, crash rate, Wilson CI, bootstrap CI, Cochran-Armitage Z, permutation p in the r1 DRAFT is preserved byte-identically in r1 LOCKED except the section 3.2 null Z quantile values corrected from the transcription residue to match the CSV-emitted values. **STATUS**: LOCKED r1 2026-07-20 post-review absorption. Q24 sub-part 5 (rest-adjacency arc + streak-length arc) descriptively landed. Any downstream Stage S1 synthesis or Stage H pre-registration for either arc drafts in a separate reviewer-mode-authorized session per MD-beta section 6.9 + section 7 compression discipline; this Stage D r1 LOCKED provides the operand-locked descriptive baseline for the streak-length arc. |
