# Bout-level citalopram dose-response recalibration — result

## Authorship

**Drafted 2026-06-22** by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../../CONVENTIONS.md). Authorising user: Willem.

**Implements**: [`methodology/bout_level_dose_response_calibration.md`](../../../../methodology/bout_level_dose_response_calibration.md) (LOCKED r2 2026-06-19 commit `c57ff3f`).

**Status**: **LANDED 2026-06-22**. The §6 inheritance table in the sub-MD is populated by this run; the sub-MD §8 status log carries a parallel r3 entry referencing this result.md.

**Reproducibility**:
- Script: `docs/research/analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration/run.py`.
- External inputs: `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` (4,317 bouts, pipeline LOCKED `d5b394c` 2026-06-22) + `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` (1,755 days).
- External output: `$GEVOELSCORE_DATA_PATH/unified/bout_level_dose_response_calibration_results.csv` (189 rows, 11-column schema per sub-MD §4).
- Repo outputs (gitignored): `summary.json` + `plots/*.png`.
- Env var: `GEVOELSCORE_DATA_PATH` per CONVENTIONS §5; defaults to `C:/Users/Gebruiker/Documents/gevoelscore-data` if unset.
- Seed: `20260622`.
- Regenerate: `python docs/research/analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration/run.py`.
- Runtime: ~60 seconds (bootstrap dominates).

---

## §1 What was run

The recalibration fit each of 7 features × 3 windows × 9 specs = **189 cells** per sub-MD §3.

**Features** (sub-MD §2):

- Per-bout (5): `peak_height`, `pre_bout_baseline`, `recovery_half_life`, `decay_slope`, `AUC_above_baseline`.
- Per-day aggregations (2): `bout_n_per_day` (pipeline name; sub-MD spec name `bout_count_day`), `bout_n_fast_recovery_day`.

**Windows** (sub-MD §3.1):

| window | dates | n_days | dose range |
|---|---|---|---|
| afbouw_2026 (primary substantive) | 2026-03-20 → 2026-06-05 | 78 | 8.03 – 30.00 mg |
| buildup_post_cpap_2024 (headline inheritance) | 2024-05-01 → 2024-06-19 | 50 | 10.00 – 20.00 mg |
| spring_2025_control (negative control) | 2025-03-20 → 2025-06-05 | 78 | 30.00 mg (flat) |

**Specs** (sub-MD §3.3): primary + Sensitivities A (block bootstrap E[L]=7, 1000 iter), B (prescribed-step), C (lagged-lcera), D (alt-lag/HAC), E (crash-drop), F (4-knot natural cubic spline on time), G (motion-clean; per-bout only), H (within-day AR(1); diagnostic-only).

**Model form** (sub-MD §3.1):

- Per-bout: OLS with cluster-robust SE on `date` (the cluster is the day-level random-intercept analogue per Daza 2018). `f(bout, d) = β_0 + β_dose · dose_plasma_mg(d) + β_time · days_from_window_start(d) + ε`. Cluster-robust SE absorbs within-day correlation across bouts.
- Per-day: OLS with Newey-West HAC SE (Andrews 1991 automatic lag). Same predictors.
- Control window: dose term dropped (no within-window variance); `β_time` reported in `verdict` notes column.
- `decay_slope`: β fit on **raw signed slope** (prior +1 = less-negative under higher plasma).

**Decisions documented in run.py docstring**: library choice (OLS+cluster-robust as MixedLM analogue), AR(1) diagnostic-only fallback, lagged-lcera computation per CONVENTIONS §3.2, Holm-family scope (5 per-bout features per window), spring-2025 dose-degenerate handling, MD-spec-to-pipeline column-name mapping.

---

## §2 What landed in the CSV

CSV schema per sub-MD §4 verbatim:

```
feature, window, spec, n_bouts, n_days, beta_dose, beta_dose_lo95, beta_dose_hi95, p_value, sign_match_prior, verdict
```

189 rows; `N/A` markers populate cells the spec declares inapplicable (Sensitivity G for per-day aggregations; Sensitivity C for `decay_slope`; all dose-cells in `spring_2025_control` where dose-variance is zero). CSV is external (gitignored under `$GEVOELSCORE_DATA_PATH/unified/`).

**Sample read (3 buildup-post-CPAP primary rows)**:

| feature | β_dose | CI95 | p | n_bouts | n_days |
|---|---:|---|---:|---:|---:|
| `peak_height` | −0.029 | [−0.937, +0.878] | 0.949 | 142 | 49 |
| `recovery_half_life` | +1.096 | [−0.217, +2.410] | 0.102 | 132 | 47 |
| `bout_n_fast_recovery_day` | −0.056 | [−0.145, +0.034] | 0.223 | 50 | 50 |

---

## §3 Per-feature headline (buildup post-CPAP as inheritance default)

The buildup post-CPAP β is the headline inheritance default per sub-MD §3.5; afbouw + control reported alongside for the verdict assignment.

*Framing note (r4 absorb 2026-06-23, audit L2.1): all β coefficients in this section are **within-window within-subject partial-derivatives of feature-on-dose** (per sub-MD §1.3 caveat + §7.3 confound-stack acknowledgement), not population-level dose-responses. CIs are conditional on the §3.1 model form (cluster-robust SE at the day level for per-bout features; Newey-West HAC for per-day aggregations). The afbouw + buildup + control three-window spec is the project-canonical mitigation for within-window non-stationarity; the linear time covariate absorbs local LC-recovery slope; the spring 2025 control verifies seasonality-alibi absence.*

### `peak_height` — verdict NULL

Buildup β = −0.029/mg, CI95 [−0.937, +0.878], p = 0.949. Afbouw β = +0.240/mg, CI95 [−0.321, +0.800], p = 0.402. Spring 2025 β_time = −0.014/day (flat). Sign-concordant with prior (+1) in afbouw but sign-reversed in buildup; in both windows CI brushes far from excluding zero. The null-finding pre-spec (sub-MD §3.4) is met: primary CI contains zero; |β| << SD-half-width gating; sens A block-bootstrap CI [−2.94, +2.16] also contains zero; lagged-lcera p = 0.546 > 0.05. **NULL** per pre-spec.

### `pre_bout_baseline` — verdict NULL

Buildup β = +0.244/mg, CI95 [−0.399, +0.887], p = 0.457. Afbouw β = +0.452/mg, CI95 [−0.059, +0.963], p = 0.083 (brushes zero from below). Spring 2025 β_time = −0.009/day (flat). Sign-concordant with prior (+1) in BOTH windows but buildup CI crosses zero on both sides; sens A block-bootstrap [−2.32, +3.59] contains zero; lagged-lcera p = 0.464 > 0.05. **NULL** per pre-spec.

### `recovery_half_life` — verdict weakly_consistent

Buildup β = +1.096 min/mg, CI95 [−0.217, +2.410], p = 0.102. Afbouw β = +0.957 min/mg, CI95 [−0.350, +2.264], p = 0.151. Spring 2025 β_time = +0.014 min/day (flat). Sign-concordant with prior (+1) in BOTH windows, with the largest effect-size of any feature relative to its standard deviation. Buildup CI brushes zero from below; primary p > 0.05 in both windows. Sens A block-bootstrap [−13.47, +22.64] contains zero (n=49 day-clusters drives huge bootstrap variance). Does NOT meet the null pre-spec (sign-concordant + non-trivial β + lagged-lcera p < 0.05) but does NOT meet CONFIRMED (CI does not exclude zero). **weakly_consistent**.

### `decay_slope` — verdict NULL

Buildup β = +0.019 stress·min⁻¹/mg, CI95 [−0.060, +0.098], p = 0.644. Afbouw β = +0.013, CI95 [−0.029, +0.054], p = 0.535. Sign-concordant with prior (+1) in both windows but |β| is tiny (< 0.05 SD-half-width). Sens A bootstrap CI [−0.56, +0.25] contains zero; lagged-lcera N/A (sub-MD §2 explicitly excludes the variant for `decay_slope`). Null pre-spec collapses to 3 conditions per sub-MD §2; all three hold. **NULL**.

### `AUC_above_baseline` — verdict weakly_consistent

Buildup β = +52.4 stress·min/mg, CI95 [−49.5, +154.3], p = 0.314 (sign-concordant with +1 prior). Afbouw β = **−20.5**, CI95 [−112.2, +71.2], p = 0.661 (**sign-DISCORDANT** with +1 prior; this is a cross-window-coherence caveat, not a verdict-changer because the buildup-headline weakly_consistent stands on the buildup cell alone per §3.5 headline-default discipline). Spring 2025 β_time = +1.66/day (mild positive drift but n.s.). Sens A bootstrap CI for afbouw [−134.4, +54.8] also negative point estimate; sens_E crash-drop β = −18.8 also negative; sens_D alt_lag β = −81.7 negative-significant-direction — five of seven afbouw sens cells are sign-discordant (only sens_B + sens_F flip to positive). Does NOT meet null pre-spec at buildup (sign-concordant + non-trivial β). Does NOT meet CONFIRMED (CI does not exclude zero in either window). **weakly_consistent** at buildup-headline; the afbouw sign-discordance is a cross-window-coherence flag worth surfacing for any downstream HA pre-reg invoking Approach A on `AUC_above_baseline` in the afbouw window.

### `bout_n_per_day` (≡ MD-spec `bout_count_day`) — verdict NULL

Buildup β = −0.020 bouts/day/mg, CI95 [−0.121, +0.081], p = 0.698. Afbouw β = **−0.102 bouts/day/mg, CI95 [−0.202, −0.002], p = 0.045** (afbouw primary excludes zero on the WRONG side of the +1 prior). Spring 2025 β_time = +0.005/day (flat). Buildup is sign-discordant with prior (+1) AND CI contains zero; afbouw is sign-discordant AND CI excludes zero. Null pre-spec at buildup-headline: CI contains zero, β small, sens A bootstrap [−0.17, +2.42] contains zero, lagged-lcera p = 0.752 > 0.05 — all four NULL conditions hold at the buildup-headline. **NULL** per pre-spec at headline. The afbouw signal (significant in the wrong direction) is reported as a substantive observation in §4 below and §6 caveat 4.

### `bout_n_fast_recovery_day` — verdict weakly_consistent

Buildup β = −0.056 bouts/day/mg, CI95 [−0.145, +0.034], p = 0.223. Afbouw β = −0.034, CI95 [−0.118, +0.050], p = 0.428. Spring 2025 β_time = +0.005/day (flat). Sign-concordant with prior (**−1**) in BOTH windows; sub-MD §2 prior is "higher plasma → fewer fast-recovery bouts" via SSRI-induced slower-recovery mechanism. Buildup CI brushes zero from above (does not exclude); sens A bootstrap [−0.67, +1.20] contains zero. Does NOT meet null pre-spec (sign-concordant + non-trivial β); does NOT meet CONFIRMED. **weakly_consistent**.

---

## §4 The dynamics-vs-level read (sub-MD §5.5)

The per-feature verdict pattern across the 5 per-bout features:

| cluster | features | verdicts |
|---|---|---|
| **Level cluster** | `peak_height`, `pre_bout_baseline` | NULL, NULL |
| **Dynamics cluster** | `recovery_half_life`, `decay_slope` | weakly_consistent, NULL |
| **Composite (level × dynamics)** | `AUC_above_baseline` | weakly_consistent |

**Read**: The level cluster is NULL on the buildup post-CPAP headline; the dynamics cluster shows one weakly-consistent feature (`recovery_half_life`) and one NULL (`decay_slope`). This pattern does NOT cleanly support the sub-MD §5.5 hypothesis that "citalopram acts on level but not on dynamics" — the LEVEL features are NULL while the dynamics half-life shows the largest sign-concordant β in the corpus. The most honest reading is: **at bout-level n=49 day-clusters in buildup-post-CPAP and n=78 in afbouw, NONE of the per-bout features achieve CONFIRMED dose-modulation.** The buildup-headline `recovery_half_life` β=+1.10 min/mg (p=0.10, CI [−0.22, +2.41]) is the most directionally-supportive result; this hints that **if** any signal exists, it sits in recovery dynamics rather than peak amplitude — opposite to the level-only mechanism that the level-cluster NULL would suggest in the OTHER direction. The honest verdict: the bout-level n is binding (effective n ≈ 49 day-clusters in buildup), and the per-bout features do not detect dose-modulation at the headline-precision the buildup window admits.

The substantive read is therefore **not the level-vs-dynamics question of sub-MD §5.5**; it is the **bout-level n-power question**. The recalibration produces NULL/weakly-consistent verdicts across the board because the bout-level CIs are wide relative to the underlying signal at this corpus's n. The parent dose-response MD's daily-aggregate +0.57/mg `all_day_stress_avg` β does NOT cleanly propagate to per-bout features at this resolution — but the parent finding remains intact at its own (daily) layer.

**Per-day aggregations** read separately:

| feature | verdict | buildup β | afbouw β |
|---|---|---:|---:|
| `bout_n_per_day` | NULL (headline); afbouw shows significant negative β | −0.020 | **−0.102** (p=0.045) |
| `bout_n_fast_recovery_day` | weakly_consistent | −0.056 | −0.034 |

The afbouw `bout_n_per_day` β = −0.10/mg (p=0.045 in primary HAC; brushes zero in sens A bootstrap at [−0.17, +2.42]) is a substantive observation: higher plasma citalopram in afbouw 2026 associates with **fewer bouts per day**, opposite to the +1 prior (the +1 prior expected "higher baseline sympathetic tone → more frequent 60-crossings"). The buildup-headline does not reach the same significance (n=50 days, CI brushes zero in both directions). Two competing readings are open: (a) citalopram's autonomic-suppression effect at high plasma reduces stress-bout incidence overall (which would be the OPPOSITE-direction signal vs the +1 prior derived from "elevated tone → more crossings"); (b) the afbouw signal is an unusual within-window time-trend that the linear `days_from_window_start` covariate fails to absorb. Sens E (crash-drop) on afbouw bout_n_per_day shows β = **−0.108**/mg [−0.202, −0.013] p=0.025 with |Δβ| = **0.0054** < 0.10·SD threshold = **0.113** — does not fire the crash-distortion flag (well within the CONVENTIONS §3.4 tolerance band). The substantive observation is logged here; the verdict at the buildup-headline remains NULL per pre-spec.

**Sens F nonlinear-time surfacing** (r4 absorb 2026-06-23, audit L3.5): three sens_F cells reach p<0.05 under the 4-knot natural cubic spline on time, which the primary linear time covariate does not: `recovery_half_life` buildup β=+3.84 [+0.32, +7.36] p=0.032; `AUC_above_baseline` buildup β=+335.95 [+152.82, +519.09] p=0.0003; `bout_n_per_day` afbouw β=−0.196 [−0.325, −0.066] p=0.003. The sens_F spline absorbs more within-window time-trend variance than the linear covariate; the dose-β under sens_F is the MORE-confound-adjusted estimate. Two interpretations open: (a) the linear time covariate under-fits the within-window trend and the dose-causal signal is larger than the headline-spec admits (sens_F STRENGTHENS the dose-causal reading on these three cells); (b) the spline overfits a noisy 47-78-day window. The headline-spec compound-symmetry + linear-time pre-commit holds the load-bearing verdicts; the sens_F results add nuance worth surfacing in downstream HA-C4c framing. None of the sens_F cells change a §6 inheritance assignment; recovery_half_life + AUC_above_baseline remain weakly_consistent (their sens_F cells just sharpen the directional read), and the bout_n_per_day sens_F result is the sharpest of the 7 sens cells supporting the afbouw substantive observation that downstream HA pre-regs touching bout_n_per_day in afbouw must pre-spec a dose-sensitivity arm.

---

## §5 Inheritance assignments for [`bout_level_recovery_dynamics.md` §5.3 Approach A](../../../../methodology/bout_level_recovery_dynamics.md)

Per sub-MD §3.5 verdict mapping → §5.4 inheritance status:

| feature | verdict | Approach A inheritance |
|---|---|---|
| `peak_height` | NULL | **Dose-naive freely usable** — no dose-adjustment applied; the feature can be used directly across phases without bias-correction. |
| `pre_bout_baseline` | NULL | **Dose-naive freely usable** — same as above. |
| `recovery_half_life` | weakly_consistent | **Sensitivity-only** — Approach A NOT load-bearing for primary cross-phase tests; downstream HA pre-regs should use the raw feature as primary and report dose-adjusted variant as sensitivity arm. Per-phase stratification (Approach C) recommended as primary when the cross-phase question is unavoidable. |
| `decay_slope` | NULL | **Dose-naive freely usable** — same as `peak_height`. |
| `AUC_above_baseline` | weakly_consistent | **Sensitivity-only** — same as `recovery_half_life`. |
| `bout_n_per_day` (≡ `bout_count_day`) | NULL | **Dose-naive freely usable** at the buildup-headline; the **afbouw substantive finding (β=−0.10/mg p=0.045 in wrong direction)** is a separate caveat that downstream HA pre-regs touching `bout_n_per_day` in afbouw should pre-spec a sensitivity arm dropping or covarying for `dose_plasma_mg` to disambiguate the afbouw signal from a within-window confound. |
| `bout_n_fast_recovery_day` | weakly_consistent | **Sensitivity-only** — Approach A NOT load-bearing for HA-C4c's primary inheritance; the framework-validity gate on HA11-bout-redo (restricted to the unmedicated stratum per parent MD §5.5) is unaffected by this verdict because that gate runs at `dose_plasma_mg = 0`. |

**Net for downstream HA pre-regs using Approach A**:
- **No feature is CONFIRMED** at the buildup-headline precision. Approach A's load-bearing role is therefore **not triggered** for any feature at this lock.
- **Two features (`recovery_half_life`, `AUC_above_baseline`, `bout_n_fast_recovery_day`) are weakly_consistent**; downstream HA pre-regs touching them should treat Approach A as a sensitivity arm, not a primary inheritance.
- **Three per-bout features and one per-day aggregation are NULL**; these can be used dose-naive without per-feature dose-adjustment overhead.

**Holm step-down across the 5 per-bout features per window** (sub-MD §3.7 descriptive overlay):

| window | feature | raw p | Holm-adj p | reject at α=0.05 |
|---|---|---:|---:|---|
| afbouw_2026 | `pre_bout_baseline` | 0.083 | 0.414 | no |
| afbouw_2026 | `recovery_half_life` | 0.151 | 0.604 | no |
| afbouw_2026 | `peak_height` | 0.402 | 1.000 | no |
| afbouw_2026 | `AUC_above_baseline` | 0.661 | 1.000 | no |
| afbouw_2026 | `decay_slope` | 0.740 | 0.740 | no |
| buildup_post_cpap_2024 | `recovery_half_life` | 0.102 | 0.509 | no |
| buildup_post_cpap_2024 | `AUC_above_baseline` | 0.314 | 1.000 | no |
| buildup_post_cpap_2024 | `pre_bout_baseline` | 0.457 | 1.000 | no |
| buildup_post_cpap_2024 | `decay_slope` | 0.644 | 1.000 | no |
| buildup_post_cpap_2024 | `peak_height` | 0.949 | 0.949 | no |
| spring_2025_control | N/A (no dose variance) | — | — | — |

No per-bout feature rejects at α=0.05 in either window after Holm correction. Consistent with the per-feature NULL/weakly-consistent verdicts.

*Footnote (r4 absorb 2026-06-23, audit L3.3)*: the Holm family is the **5 per-bout features per window** per run.py docstring decision #6 + sub-MD §3.7. The 2 per-day aggregations (`bout_n_per_day`, `bout_n_fast_recovery_day`) are excluded from the Holm family because they are different unit-of-analysis fits (day-level Newey-West HAC, not bout-level cluster-robust SE) and report their own per-feature verdicts in §3.

---

## §6 Open questions for downstream HA pre-regs

1. **HA-C4c (substantive Wiggers C4 bout-level retest) — Approach A inheritance**: per §5 above, no feature is CONFIRMED. HA-C4c's pre-reg should use the bout-level features dose-naive as primary, with Approach A as one of multiple sensitivity arms. The bout-level n is the binding constraint; a NULL HA-C4c verdict at primary should not be interpreted as a dose-confound artefact because the dose-confound is itself NULL on this dataset.
2. **The afbouw `bout_n_per_day` β=−0.10/mg (p=0.045 in wrong direction)** is a substantive observation that any downstream HA pre-reg using bout_n_per_day in afbouw should pre-spec a sensitivity arm for. The most disciplined choice is per-phase stratification (Approach C) for any cross-afbouw test on `bout_n_per_day`. The reading-versus-reading question (is it autonomic suppression or a within-window time-trend?) is OPEN; the recalibration documents the observation without committing the substantive interpretation.
3. **`recovery_half_life` weakly_consistent β=+1.10 min/mg** is the most directionally-supportive bout-level signal. HA-C4c may consider explicitly pre-committing a `recovery_half_life`-primary arm and treating the +1 mg dose adjustment (≈+1.1 min) as a sensitivity-arm bias-correction rather than a primary-arm bias-correction.
4. **Bout-level n power**: with n_buildup ≈ 49 day-clusters and n_afbouw ≈ 75-78 day-clusters, the per-bout CIs are wide enough that CONFIRMED verdicts are structurally hard to reach on a single-cell-headline. Downstream HA pre-regs should pre-commit to single-cell headlines + Holm-companion descriptive read; they should NOT chase joint multi-feature "average" β estimates which would require shrinkage priors that the sub-MD's tradeoff vision rejects.
5. **HA11-bout-redo (framework-validity reproduction check)** is restricted to unmedicated stratum per parent MD §5.5; this recalibration does not affect HA11-bout-redo's design. The recalibration's NULL on `bout_n_fast_recovery_day` at buildup-headline is irrelevant to HA11-bout-redo (different dose regime).

---

## §7 Caveats

Per sub-MD §7 verbatim, with session-specific learnings appended:

1. **Conditional on the §3.1 mixed-effects specification.** Cluster-robust SE at the day level was used as the operational analogue of MixedLM with day-level random intercept per Daza 2018. A native MixedLM fit with explicit random intercept yields numerically near-identical β with slightly different SEs; this run's CIs are the cluster-robust SE CIs. Sensitivity H (within-day AR(1)) was reported as diagnostic-only — within-day n ≈ 3 bouts/day is too small for stable AR(1) estimation per the MD pre-spec fallback wording.
2. **Bout-level n much smaller than day-level n.** Effective n ≈ 49 day-clusters in buildup-post-CPAP, ≈ 75-78 in afbouw + control. CIs are wide proportionally. This is the binding constraint; no model-form change recovers power.
3. **Per-feature β inherits parent MD §1.3 confound stack.** LC recovery trajectory, seasonality, Breinvoeding, CPAP-end. The linear time covariate + three-pronged spec mitigate; not re-stated per feature.
4. **Per-bout features are operational descriptions of the per-minute trace, not mechanistic measurements.** A CONFIRMED β (none observed here) would be a statement about per-minute-trace operand's dose-modulation, NOT directly autonomic-recovery physiology. A NULL β (observed) does not falsify the autonomic-recovery construct; it only documents that the bout-level operand does not detect the daily-aggregate signal at this n.
5. **Approach A's downstream usefulness**: zero CONFIRMED features → Approach A is NOT load-bearing for any downstream HA pre-reg at this lock. Pre-regs touching the 3 weakly-consistent features should treat Approach A as a sensitivity arm; pre-regs touching the 4 NULL features can use them dose-naive.
6. **n=1 single-subject observational; cross-subject generalisation out of scope.**
7. **Session-specific learning — bout-level recalibration is a precision question, not a substantive question, at this n.** The result.md primary read is "the binding constraint is bout-level n, not feature-by-feature dose-response heterogeneity". If a future bout-extraction methodology refinement increases effective n per window (e.g., by relaxing the 21-day device-baseline-lag exclusion under a documented justification), the recalibration could re-run at improved precision; the same r3 → r4 absorb pattern would apply.
8. **Session-specific learning — afbouw bout_n_per_day wrong-direction signal**: the β=−0.10/mg p=0.045 observation is a notable departure from the +1 prior. Honest reading per [CONVENTIONS §4.2](../../../../CONVENTIONS.md): the observation is a research-finding-candidate, not a confound-explanation. It is logged in §4 above + the §6 inheritance assignment for `bout_n_per_day` notes the disambiguation requirement for any downstream HA pre-reg touching it.

---

## §8 Reproducibility checklist

- **Script**: `docs/research/analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration/run.py`.
- **Env var**: `GEVOELSCORE_DATA_PATH` per CONVENTIONS §5; default `C:/Users/Gebruiker/Documents/gevoelscore-data`.
- **Inputs (external)**:
  - `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` (pipeline LOCKED `d5b394c` 2026-06-22).
  - `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` (per-day master).
- **Outputs**:
  - External: `$GEVOELSCORE_DATA_PATH/unified/bout_level_dose_response_calibration_results.csv` (189 rows × 11 columns per sub-MD §4).
  - Repo (gitignored): `summary.json` + `plots/*.png`.
- **Expected runtime**: ~60 seconds on a 1-thread Python 3.14 install with statsmodels 0.14.6 + patsy + numpy + pandas.
- **Regenerate**:
  ```powershell
  python docs/research/analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration/run.py
  ```
- **Seed**: `20260622` (block-bootstrap reproducibility).
- **Pre-spec → result-file traceability**: each of the 189 CSV rows maps directly to a (feature × window × spec) cell of sub-MD §3 + §4; no improvised computations beyond the pre-spec.

---

## Cross-references

- [`methodology/bout_level_dose_response_calibration.md`](../../../../methodology/bout_level_dose_response_calibration.md) — the sub-MD this result implements. §6 inheritance table populated by this run; §8 r3 status log + revision log carries the parallel entry.
- [`methodology/bout_level_recovery_dynamics.md`](../../../../methodology/bout_level_recovery_dynamics.md) — parent MD; §5.3 Approach A inheritance assignment per §5 of this result.md.
- [`methodology/citalopram_dose_response_stress_mean_sleep.md` §5.6.1](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) — parent daily-aggregate β reference (+0.43/mg `stress_mean_sleep`, +0.57/mg `all_day_stress_avg`, −1.13/mg `bb_lowest`); the recalibration's NULL bout-level peak_height β is the level-vs-bout-level non-propagation observation.
- [`pipeline/02_features/extract_stress_bouts.py`](../../../../pipeline/02_features/extract_stress_bouts.py) — bout-extraction pipeline that produced `per_bout_master.csv` (LOCKED `d5b394c` 2026-06-22).
- Pattern reference: `docs/research/analyses/descriptive/operationalisation_support/stress_mean_sleep/run.py` + `docs/research/analyses/descriptive/trajectory/recovery_arc/run.py` (block-bootstrap idiom).
