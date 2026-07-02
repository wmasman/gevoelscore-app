# Recovery-phase quartiles export (R28)

**Status**: producer-mode Layer-1 descriptive export for site request **R28**
(per-phase p25/p75 for the recovery-phase box plots on
`/workings/the-recovery-in-six-phases`). Aggregated and privacy-safe:
**per-phase distribution summaries only, no dated raw values**. No
interpretive or causal marks (CONVENTIONS §4.1). Drafted 2026-07-02 by Claude
(Opus 4.8), producer-mode, for the participant-researcher (repo owner).

## 1. What this is

The box-plot data (p25 / median / p75 + min/max whiskers + n) for the
7-channel HA-P6 set across the six lived recovery phases. It is the quartile
add the register calls "a one-line research add": `recovery_arc` already emits
the bootstrap-CI-of-the-median per phase; this supplies the **distribution
spread** (IQR + whiskers) the box plots need. The recovery-phase boundaries
are lived-experience (M1), never data-tuned (inherits the R19 / R27
discipline): a quiet phase is not a refutation, and this is descriptive, not a
per-phase verdict.

## 2. The quartiles (per channel, per phase)

Named counts (CONVENTIONS §3.6): computed directly from
`per_day_master.csv` grouped on the `recovery_phase` column. Whiskers are
min/max (state this on the visual, they are the observed range, not 1.5xIQR
fences). Phase order is the lived sequence.

**stress_mean_sleep** (Garmin HRV-derived sleep-stress score; confirmed
citalopram-dose-modulated):

| phase | n | p25 | median | p75 | min | max |
|---|---:|---:|---:|---:|---:|---:|
| pre_illness_healthy | 215 | 11.31 | 15.95 | 21.93 | 4.58 | 55.05 |
| acute_infection | 14 | 14.58 | 20.31 | 27.35 | 11.25 | 63.55 |
| lc_pre_ergo | 158 | 14.98 | 19.18 | 22.90 | 7.87 | 57.10 |
| pacing_pre_citalopram_learning (4a) | 53 | 18.06 | 19.97 | 22.88 | 10.46 | 40.57 |
| pacing_habit_established (4b) | 500 | 16.66 | 19.53 | 22.90 | 8.32 | 73.00 |
| citalopram_modulated (5) [dose-mixed] | 767 | 16.34 | 18.92 | 22.01 | 9.24 | 71.99 |

**all_day_stress_avg** (confirmed citalopram-dose-modulated):

| phase | n | p25 | median | p75 | min | max |
|---|---:|---:|---:|---:|---:|---:|
| pre_illness_healthy | 216 | 26 | 30 | 35 | 15 | 54 |
| acute_infection | 14 | 32 | 33 | 41.5 | 24 | 48 |
| lc_pre_ergo | 162 | 32 | 35 | 39 | 16 | 62 |
| pacing_pre_citalopram_learning (4a) | 53 | 31 | 34 | 37 | 22 | 49 |
| pacing_habit_established (4b) | 509 | 31 | 34 | 38 | 20 | 69 |
| citalopram_modulated (5) [dose-mixed] | 778 | 27 | 31 | 34 | 19 | 57 |

**bb_lowest** (confirmed citalopram-dose-modulated):

| phase | n | p25 | median | p75 | min | max |
|---|---:|---:|---:|---:|---:|---:|
| pre_illness_healthy | 216 | 6 | 12 | 18 | 5 | 49 |
| acute_infection | 14 | 5 | 14.5 | 20 | 5 | 36 |
| lc_pre_ergo | 162 | 7 | 12 | 17 | 5 | 43 |
| pacing_pre_citalopram_learning (4a) | 53 | 14 | 19 | 23 | 5 | 37 |
| pacing_habit_established (4b) | 509 | 13 | 18 | 23 | 5 | 45 |
| citalopram_modulated (5) [dose-mixed] | 778 | 16 | 22 | 28 | 5 | 69 |

**resting_hr**:

| phase | n | p25 | median | p75 | min | max |
|---|---:|---:|---:|---:|---:|---:|
| pre_illness_healthy | 217 | 52 | 54 | 55 | 47 | 61 |
| acute_infection | 14 | 51 | 52.5 | 55 | 51 | 58 |
| lc_pre_ergo | 162 | 52 | 55 | 56 | 49 | 59 |
| pacing_pre_citalopram_learning (4a) | 53 | 52 | 53 | 54 | 50 | 55 |
| pacing_habit_established (4b) | 509 | 55 | 56 | 57 | 52 | 65 |
| citalopram_modulated (5) | 776 | 55 | 57 | 59 | 52 | 63 |

**gevoelscore** (1-10 felt-state; logging starts 2022-09, so no pre-illness /
acute data):

| phase | n | p25 | median | p75 | min | max |
|---|---:|---:|---:|---:|---:|---:|
| lc_pre_ergo | 19 | 3 | 3 | 4 | 1 | 5 |
| pacing_pre_citalopram_learning (4a) | 56 | 4 | 5 | 5 | 1 | 6 |
| pacing_habit_established (4b) | 509 | 4 | 4 | 5 | 1 | 6 |
| citalopram_modulated (5) | 788 | 4 | 5 | 5 | 2 | 6 |

**stress_low_motion_min_count_S60_Mlow** (a rest-stress pacing-behaviour
proxy):

| phase | n | p25 | median | p75 | min | max |
|---|---:|---:|---:|---:|---:|---:|
| pre_illness_healthy | 217 | 16 | 36 | 79 | 0 | 213 |
| acute_infection | 14 | 51 | 101 | 135.5 | 24 | 214 |
| lc_pre_ergo | 162 | 46 | 72.5 | 111 | 0 | 364 |
| pacing_pre_citalopram_learning (4a) | 54 | 38.25 | 64.5 | 110.75 | 0 | 269 |
| pacing_habit_established (4b) | 509 | 50 | 79 | 115 | 0 | 361 |
| citalopram_modulated (5) | 783 | 22 | 41 | 69.5 | 0 | 297 |

**bb_overnight_gain**: only the `citalopram_modulated` phase has data
(n=593; p25 41, median 49, p75 57, min 3, max 82). The earlier phases are
empty because per-minute body-battery is only available from ~2024-06 (the
measurement-regime coverage cliff, see R17). **Do not render a box plot for
bb_overnight_gain across phases** - it would read as a phase change that is a
data-availability artifact.

## 3. Site-consumable JSON shape

```json
{
  "note": "per-recovery-phase quartiles; whiskers are min/max (observed range), not IQR fences",
  "channels": {
    "<channel>": {
      "confirmed_citalopram_dose_modulated": true,
      "phases": [
        {"phase":"pre_illness_healthy","n":215,"p25":11.31,"median":15.95,"p75":21.93,"min":4.58,"max":55.05},
        {"phase":"citalopram_modulated","n":767,"p25":16.34,"median":18.92,"p75":22.01,"min":9.24,"max":71.99,
         "caveat":"dose-mixed; stratify by citalopram axis per section 5.A before use"}
      ]
    }
  }
}
```

## 4. Caveats (the site must carry these)

- **Phase-5 confirmed-citalopram channels are dose-mixed.** For
  `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`, the
  `citalopram_modulated` phase spans the whole 0-to-30-mg-and-taper range, so
  its box conflates dose states. Per
  [`../../../methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md)
  §5.A these cells must be dose-stratified before any comparison; the raw box
  is descriptive spread only. `recovery_arc` v2 does this stratification for
  the median-CI; apply the same before reading the phase-5 box as a change.
- **Small-n phases.** `acute_infection` (n=14) and
  `pacing_pre_citalopram_learning` / 4a (n=53-56) have wide, honest-limit
  distributions; the box is illustrative, not a stable estimate. Label n on
  each box.
- **Coverage gaps.** `gevoelscore` has no pre-2022-09 data (felt-state
  logging start); `bb_overnight_gain` is phase-5-only (per-minute BB cliff).
- **Descriptive only, no verdict.** These are distribution shapes per lived
  phase, not per-phase tests. The boundaries are lived-experience M1, never
  data-derived.

## 5. Reproducibility

Direct quantile computation from `per_day_master.csv` on the `recovery_phase`
column (values: `pre_illness_healthy`, `acute_infection`, `lc_pre_ergo`,
`pacing_pre_citalopram_learning`, `pacing_habit_established`,
`citalopram_modulated`); linear-interpolation quantiles; whiskers = observed
min/max. This complements the bootstrap-CI-of-the-median already in
[`../../descriptive/trajectory/recovery_arc/`](../../descriptive/trajectory/recovery_arc/)
(`median_iqr()` in `run.py` already computes p25/p75; this export surfaces
them per recovery phase for the box plots, since the on-disk `summary.json`
is gitignored and strata-grouped).

## 6. Cross-references

- Register R28 (per-phase quartile export) + R19 (per-signal recovery-phase
  read) + R27 (phase-boundary convergence).
- [`../../descriptive/trajectory/recovery_arc/`](../../descriptive/trajectory/recovery_arc/)
  (the v2 recovery-phase analysis this extends).
- [`../../../methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md)
  §5.A (phase-5 dose-stratification requirement for the confirmed channels).
