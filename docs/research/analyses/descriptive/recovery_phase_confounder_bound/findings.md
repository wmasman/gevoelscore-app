# Findings - R30 net-of-slow-confounders per-phase re-read (R19 audit)

**Layer-4 method note** for site request **R30** ("net-of-slow-confounders
per-phase re-read"), auditing the absolute per-phase LEVELS from R19
([`../recovery_phase_signal_backdrop/findings.md`](../recovery_phase_signal_backdrop/findings.md))
against the slow confounders (weight, deconditioning tail, aging). Producer-mode,
for the participant-researcher (repo owner), drafted 2026-07-06 by Claude
(Opus 4.8). Reproducible via [`run.py`](run.py).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

**Scope (RHR-focused, per the 2026-07-06 framing)**: Part A is a rigorous
per-phase decomposition of `resting_hr` - the one channel where the slow drivers
are the established drivers - reusing the EXACT locked model from
[`../../longrun_rhr_trend/decomposition.py`](../../longrun_rhr_trend/decomposition.py)
(imported, not re-derived). Part B is a brief, caveated bound for the other
exposed channels, whose cross-phase shape is citalopram-dominated (R20's territory,
not a slow drift). Felt-state (`gevoelscore`) is the clean self-report axis and
needs no correction. No causal marks per [CONVENTIONS section 4.1](../../../CONVENTIONS.md).

**Surface note**: R30 aggregates the **full recovery-phase record** (the level-strip
surface, phases 1-5, RHR observed from 2021-08), where R19's crash backdrop used
the Stratum-4 window only. So R30's phase-3 cell spans the full `lc_pre_ergo`
phase (~162 RHR-days) rather than R19's 19-day Stratum-4 tail; the two serve
different site elements (R19 = crash backdrop, R30 = the absolute-level strip).

---

## 1. Headline

**The per-phase resting-HR rise is confounder-dominated; the illness-attributable
residual LEVEL is flat across phases.** After the locked model removes weight +
aging + citalopram + season, the resting-HR level is ~52-53 bpm in **every**
phase - the observed rise from the pre-illness phase to the citalopram era
(+3.84 bpm) is almost entirely weight and aging, partly masked by citalopram. And
under the honest non-identifiability bound (2x the weight coefficient, per longrun
B9), the later-phase residual turns **negative**, which is physiologically
implausible for an illness signal - so at the per-phase LEVEL there is **no
identifiable positive illness residual**. This is the register's exact concern
("a level gap between phases is part illness-phase, part the slow drift"),
quantified: for resting-HR, the phase level-gap is essentially all slow drift.

This is consistent with the parent RHR decomposition, which found the **static
level partition non-identifiable** and only a **faint within-era residual SLOPE**
(+1.21 bpm/yr post-2023) that is itself SUGGESTIVE-not-established. R30 confirms
the level reading: the recovery-phase RHR strip should be read as the slow drift,
not an illness-phase level signal.

---

## 2. Part A - resting_hr per-phase decomposition (reused locked model)

Model reused verbatim from `longrun_rhr_trend/decomposition.py` (literature
deconditioning curve, tau = 4 months representative fit). **Reproduction gate**:
the refit coefficients match the parent exactly - b_weight = 0.322, b_dose
= -0.038 bpm/mg, decond_amp = 0.00 (non-identifiable), b_age = 0.50 (at cap).

Per-phase **mean** resting_hr (bpm), decomposed additively (contributions sum to
the mean; intercept 52.68 is the model level):

| phase | id | mean RHR | intercept | + weight | + citalopram | + aging | + season | + residual |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `pre_illness_healthy` | 1 | 53.37 | 52.68 | +0.38 | 0.00 | +0.15 | +0.11 | +0.05 |
| `acute_infection` | 2 | 53.36 | 52.68 | -0.39 | 0.00 | +0.31 | +0.86 | -0.10 |
| `lc_pre_ergo` | 3 | 54.05 | 52.68 | +0.39 | 0.00 | +0.43 | -0.41 | +0.96 |
| `pacing_pre_citalopram_learning` | 4a | 53.17 | 52.68 | +1.28 | 0.00 | +0.59 | -0.54 | -0.85 |
| `pacing_habit_established` | 4b | 56.47 | 52.68 | +2.47 | 0.00 | +0.97 | +0.21 | +0.13 |
| `citalopram_modulated` | 5 | 57.21 | 52.68 | +3.74 | -1.04 | +1.86 | +0.02 | -0.06 |

(decond contributes 0.00 in every phase - non-identifiable, collapses to the
intercept per longrun B3, so it is omitted from the columns.)

**The rise, decomposed (phase 1 -> phase 5, +3.84 bpm total):**

| driver | contribution to the rise |
|---|---:|
| **weight** (74 -> ~89 kg over the era) | **+3.36 bpm** |
| **aging** (over-capped at 0.5 bpm/yr; conservative) | **+1.71 bpm** |
| citalopram (lowers RHR; masks part of the rise) | **-1.04 bpm** |
| season | -0.09 bpm |
| **residual (illness / aging)** | **-0.11 bpm** |

Weight and aging together account for +5.07 bpm; citalopram masks -1.04; the
illness-attributable residual contributes essentially **nothing** to the
phase-to-phase rise.

**The residual LEVEL (intercept + residual) is flat across phases:**

| phase | 1 | 2 | 3 | 4a | 4b | 5 |
|---|---:|---:|---:|---:|---:|---:|
| residual RHR level (fitted b_weight) | 52.73 | 52.58 | 53.64 | 51.83 | 52.81 | **52.62** |
| residual RHR level (2x b_weight, the bound) | 52.35 | 52.97 | 53.25 | 50.55 | 50.35 | **48.88** |

Under the fitted weight coefficient the residual level is ~52-53 bpm in every
phase (no phase-level illness signal). Under the doubled coefficient (the longrun
B9 bound, which is admissible because post-2023 weight is interpolated over a
523-day gap) the later-phase residual falls **below** the early phases - an
illness term that LOWERS resting-HR, which is not credible. The honest reading is
bracketed by these two: **the phase-level RHR gap is slow-drift-dominated, and no
positive illness-phase level residual is identifiable.**

---

## 3. Part B - other exposed channels (citalopram-dominated; bound only)

For the HRV-derived stress / body-battery channels the cross-phase shape is
**dominated by citalopram** (a step at phase 5, the CONFIRMED dose-modulation
R20 characterises), which is **not a slow drift**. A slow-linear detrend is
therefore a crude aggregate-drift proxy that **partly absorbs the citalopram
step**, so the detrended medians below are a rough BOUND, not a
slow-confounder-clean level. Attribution of the phase-5 step belongs to R20.

Per-phase raw median vs residual about an LC-era linear trend:

| channel | LC-era trend | phase 3 raw / detr | phase 4a raw / detr | phase 4b raw / detr | phase 5 raw / detr |
|---|---:|---|---|---|---|
| `stress_mean_sleep` | -0.13/yr (flat) | 19.2 / -1.1 | 20.0 / -0.3 | 19.5 / -0.6 | 18.9 / -1.1 |
| `all_day_stress_avg` | -1.28/yr | 35 / -0.4 | 34 / -1.0 | 34 / +0.3 | 31 / -1.3 |
| `bb_lowest` | +1.82/yr | 12 / -4.4 | 19 / +2.1 | 18 / -0.4 | 22 / +0.5 |
| `stress_low_motion` (S60_Mlow) | -10.7/yr | 72.5 / -16.6 | 64.5 / -21.1 | 79 / +2.5 | 41 / -17.9 |

These move little once the aggregate LC-era drift is removed, except where the
citalopram step is (wrongly) partly absorbed by the linear term. R30 does **not**
build per-channel slow-confounder models for these - the slow drivers are not
their established drivers, and the honest statement is "citalopram-dominated,
see R20; slow-confounder exposure secondary and non-identifiable."

---

## 4. R28 pairing - per-phase box-strip data (resting_hr)

For the recovery-page box-strip (R28), per-phase p25/p75 of resting_hr, raw and
residual (slow-driver-removed), so the strip can show the netted level beside the
raw:

| phase | id | raw median [p25, p75] | residual-level median [p25, p75] |
|---|---|---|---|
| `pre_illness_healthy` | 1 | 54.0 [52.0, 55.0] | 52.7 [50.7, 55.2] |
| `acute_infection` | 2 | 52.5 [51.0, 55.0] | 51.7 [50.2, 54.5] |
| `lc_pre_ergo` | 3 | 55.0 [52.0, 56.0] | 54.3 [51.6, 55.5] |
| `pacing_pre_citalopram_learning` | 4a | 53.0 [52.0, 54.0] | 51.8 [50.8, 53.0] |
| `pacing_habit_established` | 4b | 56.0 [55.0, 57.0] | 52.3 [51.1, 54.0] |
| `citalopram_modulated` | 5 | 57.0 [55.0, 59.0] | 52.8 [51.3, 53.9] |

The story the box-strip carries: the **raw** boxes step up across the later phases
(4b 56, 5 57), while the **residual** boxes sit flat (~52-53 everywhere), because
the step is the slow drift. Full cells also in `summary.json`
(`part_a_rhr_decomposition.per_phase[*].rhr_p25/p75` and `resid_level_p25/p75`).

---

## 5. Caveats per CONVENTIONS section 4.1 + section 4.2

- **The static per-phase level partition is not cleanly identifiable.** The slow
  drivers (weight, deconditioning, aging) are mutually collinear (~0.96) and
  collinear with time-within-era; longrun established that only the residual
  SLOPE is identifiable, not the static level. R30's per-phase residual level is
  therefore reported as a bracket (fitted vs 2x-weight), not a point.
- **Weight is interpolated across the leverage window.** Post-2023 weight is a
  straight line across a 523-day weigh-in gap plus one participant-reported 2026
  anchor (89 kg); the +3.36 bpm weight attribution is conditional on that
  interpolated curve (longrun B9). The 2x-b_weight bound exists precisely because
  this coefficient is under-determined over the late phases.
- **Aging is over-removed (conservative).** The model caps aging at 0.5 bpm/yr,
  above the ~0.3 bpm/yr literature ceiling, so the +1.71 bpm aging attribution is
  an upper estimate; a lower aging term would push more of the rise into the
  residual, but even aging = 0 leaves the residual level near-flat, not rising.
- **Citalopram attribution is a lower bound.** The in-sample dose beta
  (-0.038 bpm/mg -> ~-1 bpm at 30 mg) is attenuated because initiation coincides
  with the steepest RHR-rise window; the true masking may be larger (longrun B2),
  which would make the confounder-domination of the rise even stronger.
- **Part B is a caveated bound, not a finding.** The stress / BB channels are
  citalopram-dominated (R20); the linear detrend partly absorbs that step and is
  not a slow-confounder-clean read.
- **Felt-state needs no correction** and is not audited here.
- **Surface difference from R19**: R30 uses the full recovery-phase record
  (level strip); R19 used the Stratum-4 crash window. Phase-3 differs most (full
  ~162-day phase vs 19-day S4 tail).
- **n=1; no causal marks.** "In this body, the phase RHR gap is accounted for by
  the modelled slow drivers", never "the slow drivers caused it".

---

## 6. Verification log

- **Reproduction gate (Part A)**: refit b_weight = 0.3218, b_dose = -0.0381,
  decond_amp = 0.00, b_age = 0.50 - matches
  [`longrun_rhr_trend/findings.md`](../../longrun_rhr_trend/findings.md) B1
  (0.322 / -0.038 / 0.00 / 0.50). Model imported from `decomposition.py`
  (SEED 20260702), literature tau = 4 months representative fit.
- **Decomposition identity**: per-phase mean RHR = intercept + weight + citalopram
  + aging + season + decond + residual (means are additive; verified to
  rounding in the table).
- **Non-identifiability bound**: residual level recomputed with b_weight x2 (the
  longrun B9 admissible range given interpolated weight).
- **Part B**: per-phase raw + LC-era-linear-detrended (OLS on LC-era days from
  2022-04-04) medians for stress_mean_sleep, all_day_stress_avg, bb_lowest,
  stress_low_motion_min_count_S60_Mlow.
- **Surface**: full RHR-observed record (n_days_fit in `summary.json`); phases per
  the `recovery_phase` column.
- **Operand-source path**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`
  + `userBioMetrics.json` (weight / VO2Max) via the reused loaders.
- **Machine-readable**: `summary.json` (gitignored per the `docs/research/**/*.json`
  rule).

---

## 7. Cross-references

- **Audited surface**: [`analyses/descriptive/recovery_phase_signal_backdrop/findings.md`](../recovery_phase_signal_backdrop/findings.md)
  (R19, the raw per-phase levels).
- **Reused model + fragilities**: [`analyses/longrun_rhr_trend/findings.md`](../../longrun_rhr_trend/findings.md)
  (B1 coefficients, B3 decond non-identifiability, B8 aging bound, B9 weight
  interpolation) + [`decomposition.py`](../../longrun_rhr_trend/decomposition.py).
- **Confounder-exposure principle**: [`methodology/confounder_exposure_triage.md`](../../../methodology/confounder_exposure_triage.md)
  (why absolute cross-phase levels are the exposed class).
- **Citalopram attribution for Part B**: [`analyses/descriptive/operationalisation_support/driver_netting_overlay/findings.md`](../operationalisation_support/driver_netting_overlay/findings.md)
  (R20) + `methodology/citalopram_phase_stratification.md`.
- **Axis**: [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md).
- **Site register R30** (this deliverable); R19 / R28 / R20. External repo
  `wiggers_research_story`, `docs/research-requests.md`.

---

*End of findings.*
