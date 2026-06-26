# `trajectory/seasonality_dow/` -- Q4.8 confound check

## What this analysis answers

**Q4.8 per [`descriptive/README.md`](../../README.md) section 4.8** (r2 closure D4.9): Are there time-of-year (seasonality) or weekday-vs-weekend (DOW) patterns per channel? These act as confounders for recovery_arc + Q4.2 + Q4.3 attribution.

**Tier 3 deferred topic 1 of 2** (Q4.7 notes-categorisation patterns is the other; user wants both done before research-interpret skill pivot).

---

## User-LOCKED operationalisation (per Strand B section 7c interview 2026-06-25; do NOT iterate)

1. **Channel scope = 6 channels** (matches Q4.9 + Q4.5.b + Q4.2): `stress_mean_sleep` + `all_day_stress_avg` + `bb_lowest` + `stress_stdev_sleep` + `stress_low_motion_min_count_S60_Mlow` + `resting_hr`.
2. **Seasonality method = (c) both harmonic + per-month**: sin/cos annual harmonic regression (1-year periodicity) + per-month median table (12 strata).
3. **DOW method = (c) both per-DOW + weekday-vs-weekend**: per-DOW median (7 strata) + weekday-vs-weekend Mann-Whitney U.
4. **Confound disambiguation = (c) both v3 spring-control extension + per-recovery-phase seasonality**:
   - extend v3 spring-2025 control logic to all 6 channels (per [citalopram_dose_response_stress_mean_sleep.md section 5.5.1 + section 5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) LOAD-BEARING)
   - per-recovery-phase seasonality (per [lc_recovery_phase_axis.md section 2](../../../../methodology/lc_recovery_phase_axis.md) 6-phase axis)

---

## Method (9-stage architecture)

- **Stage 1** (data prep): load `per_day_master.csv`; identify recovery_phase + citalopram_phase + month + DOW per row.
- **Stage 2** (seasonality harmonic): per channel, fit `y = alpha + b1*sin(2*pi*doy/365) + b2*cos(2*pi*doy/365)`; report amplitude + phase + R2; suspect-flag = `R2 >= 0.10`.
- **Stage 3** (seasonality per-month): per channel, 12-month median table + IQR; Kruskal-Wallis across 12 months.
- **Stage 4** (DOW per-day): per channel, 7-DOW median table + IQR; Kruskal-Wallis across 7 days.
- **Stage 5** (DOW weekday-vs-weekend): per channel, Mann-Whitney U + Cliff's delta.
- **Stage 6** (v3 spring-control extension): per channel, fit `channel ~ const + beta_time*days` on March 20 -> June 5 of 2025 (control: 30mg consolidation) vs 2026 (test: afbouw); HAC SE; descriptive 'step-survives-same-season' flag for CONFIRMED-citalopram channels.
- **Stage 7** (per-recovery-phase seasonality): per channel x per-recovery-phase, refit the annual harmonic on within-phase data (n >= 30 + span >= 180d gate).
- **Stage 8** (plots): 5 PNG artefacts in [`plots/`](plots/) (gitignored).
- **Stage 9** (programmatic emit): [`findings.md`](findings.md) + this README + [`summary.json`](summary.json) (gitignored).

---

## Discipline guards

- **Layer 1 descriptive per CONVENTIONS section 2.1**: NO causal claims; NO claim citalopram is/is-not seasonally confounded (that is v3-extension territory; this is a descriptive check only).
- **Per CONVENTIONS section 4.2 caveat-class**: a seasonality-detected channel is reported as `harmonic R2=X; amplitude Y; suspect for seasonality confound` -- NOT promoted to `the multi-year arc is partly seasonal`.
- **DOW patterns on stress/RHR channels may be expected** (work-week stress is well-documented in general literature). The Stage 4 + Stage 5 suspect flags are descriptive substrate; mechanism claims are out of scope.
- **v3 spring-control extension is descriptive observation only**; it neither confirms nor refutes the v3 verdict (3 CONFIRMED channels: stress_mean_sleep, all_day_stress_avg, bb_lowest).
- **ASCII-only stdout; no em-dashes; no emojis** per project convention.
- **f-string discipline**: no nested double-quotes inside f-string expressions (pre-3.12 compatibility).

---

## How to run

```
# Requires GEVOELSCORE_DATA_PATH env var pointing to gevoelscore-data root
python docs/research/analyses/descriptive/trajectory/seasonality_dow/run.py
```

Outputs (all but [`run.py`](run.py) + [`README.md`](README.md) + [`findings.md`](findings.md) gitignored):

- `summary.json` -- machine-readable per-channel per-stage statistics
- `plots/harmonic_fits.png` -- per-channel annual harmonic fit visualisation
- `plots/seasonality_per_month.png` -- per-channel x month median grid (with IQR error bars)
- `plots/dow_per_day.png` -- per-channel x DOW median grid (weekday blue / weekend orange)
- `plots/v3_spring_control_extension.png` -- per-channel beta_time bar (2025 control vs 2026 test)
- `plots/per_phase_seasonality_heatmap.png` -- channel x phase amplitude + R2 heatmap

---

## Status

**LANDED 2026-06-26**. Tier 3 deferred-topic 1 of 2 closed. Remaining: Q4.7 notes-categorisation patterns.

