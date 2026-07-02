# Confounder-exposure triage: which analyses need the RHR-style confounder audit

**Status**: methodology decision artefact (2026-07-02). The long-run RHR
trend work built a literature-gated confounder set (deconditioning, weight,
citalopram, seasonality, aging, measurement drift; see
[`../analyses/longrun_rhr_trend/driver_ledger.md`](../analyses/longrun_rhr_trend/driver_ledger.md)).
Question: do the project's OTHER findings need re-testing against those
confounders? This doc gives the principle, an empirical demonstration, and a
per-analysis triage. Drafted by Claude (Opus 4.8), producer-mode, for the
participant-researcher (repo owner).

## 1. The principle

Slow confounders (deconditioning-tail, weight, aging, firmware drift) move on
**year scales** (~1 bpm/yr). Whether an analysis is exposed to them depends
entirely on its **temporal structure**:

- **Short-horizon, lagged-personal-baseline tests are immune.** The
  crash-precursor hypotheses z-score a deviation in the 4-5 days before a
  crash against a **rolling personal baseline** (e.g. deltas or levels over
  [d-90, d-30]). A confounder that moves ~1 bpm/yr is essentially constant
  over that window, and a lagged baseline already contains whatever slow
  level shift happened, so it is differenced / baselined out.
- **Long-horizon, cross-era, or absolute-level claims are exposed.** Anything
  that attributes a multi-year drift or a between-era difference to LC can be
  confounded by the slow drivers, because there is no recent baseline
  removing them. This is the class the RHR long-run work itself belongs to.

## 2. Empirical demonstration (not just assertion)

Tested on `resting_hr` (the most confounder-exposed channel, since the
confounders are RHR drivers), comparing the precursor metric computed on the
raw series vs the series with the slow trend removed. If removing the slow
confounder barely changes the metric, the test is immune.

| Precursor metric | Detrend applied | Correlation (raw vs detrended z) | Trigger-flag agreement (\|z\|>=1.5) |
|---|---|---|---|
| **Level** (HA06b-style, lagged [d-90,d-30] median+MAD) | **pure linear** (the 1.11 bpm/yr slow confounder) | **0.998** | **97.9%** |
| Level | 365-day median (slow + fast-2022 transient) | 0.968 | 92.7% |
| **Delta** (HA07c-style, day-over-day) | pure linear | ~1.00 (differencing kills a linear trend) | 96% (n=202) |

**Read:** against a pure slow confounder of the size we actually have
(1.11 bpm/yr), the precursor level-test is **99.8% correlated and 98%
flag-identical** with and without it; delta tests are even more immune.
**The one exposure**: the *fast 2022 deconditioning transition* is a
medium-frequency event (not slow), so a precursor whose baseline straddles
early-2022 sees a small shift (mean ~0.2 z, still ~93% flag agreement). The
2% of non-immunity lives entirely in the acute 2022 deconditioning window.

## 3. Triage

### SAFE (no confounder re-test needed): short-horizon, lagged-baseline

All crash-precursor and crash-geometry hypotheses use lagged personal
baselines and 4-5 day horizons:

- H01, H02, H02b, H02d, H03, H03b, H04, H05 (channel precursors)
- HA01b, HA01c, HA06, HA06b, HA07, HA07c, HA07d, HA08, HA08c, HA10, HA11
  (per-axis and threshold diagnostics)
- K01 (crash depth), K02 (crash duration), crash_v2-definition
  (within-event / definitional)
- HA-C3, HA-C4, HA-P6, HA-P7, S02b (cluster / lead diagnostics, same
  lagged-baseline structure)

These are immune per section 2. **Footnote:** any precursor result that leans
specifically on **crashes during the acute 2022 deconditioning window** gets
a one-off spot-check (the only place the 2% non-immunity lives), not a
library-wide re-run.

### NEEDS AUDIT (long-horizon / cross-era / absolute-level)

- **Citalopram dose-response (§5.B correction) -- PRIORITY.** It has the
  EXACT collinearity structure the RHR work uncovered: over 2024+, dose,
  continued weight gain, and the deconditioning tail all co-trend. The
  confirmed betas (stress_mean_sleep +0.43/mg, all_day_stress_avg +0.57/mg,
  bb_lowest -1.13/mg) may partly absorb weight/fitness co-trends, just as
  the RHR aging term over-absorbed. Load-bearing for the site's citalopram
  mechanism, so audit first.
- **Any "the factor drifted over the LC era" / cross-era baseline
  comparison** (e.g. era-directionality-reversal claims).
- **The stress-to-felt curve (R22)** IF it uses absolute cross-era stress
  levels (stress is HRV-derived, so fitness/deconditioning can confound it);
  verify its baseline construction.
- **Cross-era descriptive levels** in felt_state_timeline (R13), phase_axis
  (R19): verify whether they compare absolute cross-era levels (exposed) or
  within-window relatives (safe).

## 4. Recommended action

1. Do NOT re-test the precursor library (section 2 demonstrates immunity).
2. Audit the **citalopram dose-response** against the confounder set first
   (same collinearity as RHR; highest value).
3. For each other NEEDS-AUDIT item, first verify its baseline construction:
   if it uses a rolling lagged baseline it is safe; only fixed-era-baseline /
   absolute-level analyses need the full audit.
4. Spot-check precursor results that depend on acute-2022 crashes.

## 5. Cross-references

- [`../analyses/longrun_rhr_trend/driver_ledger.md`](../analyses/longrun_rhr_trend/driver_ledger.md)
  (the confounder set), [`../analyses/longrun_rhr_trend/findings.md`](../analyses/longrun_rhr_trend/findings.md)
  (the decomposition + its fragilities).
- [CONVENTIONS.md](../CONVENTIONS.md) §3.1 (lagged personal baseline), §3.5.
