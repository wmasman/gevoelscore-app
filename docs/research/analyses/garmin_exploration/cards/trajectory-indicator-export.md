# Trajectory indicator export (R10)

**Status**: producer-mode Layer-1 descriptive export for site request **R10**
(one proven Garmin indicator across the whole timeline, for the trajectory
scrollytelling). Aggregated and privacy-safe: **monthly summaries only, no
dated raw daily values**. No interpretive or causal marks (CONVENTIONS §4.1).
Drafted 2026-07-02 by Claude (Opus 4.8), producer-mode, for the
participant-researcher (repo owner).

## 1. The indicator, and why

**`stress_mean_sleep`** (the overnight mean of Garmin's HRV-derived stress
score), monthly **median + p25/p75 band**, 2021-08 to 2026-05 (58 months).
Chosen as the single Garmin trajectory indicator because it is the anchor
autonomic-load channel: a v3-CONFIRMED crash discriminator (HA07c), the
least activity-confounded stress read (sleep window, activity approximately
0), and the channel the site's other beats already use.

**It is the sibling of R13, not a replacement.** R13's felt-state timeline is
the lived ground truth (the home opener); this is the *watch's* overnight
autonomic view of the same span, shown honestly as a proxy.

## 2. Honest framing the site MUST carry

- **It is a proxy, not wellbeing.** Label it "overnight autonomic-load
  (Garmin stress score, HRV-derived)," never "wellbeing" or "how I felt."
- **It is noisy and does NOT trace a clean illness arc.** The monthly median
  wobbles between roughly 10 and 24 across the whole record with strong
  month-to-month and seasonal variation and no single monotonic
  healthy-to-LC ramp. Present it as a textured autonomic time-series to
  scroll through, not as a smooth decline-and-recovery story. This honesty is
  the point: the felt-state (R13) carries the arc; the watch carries texture.
- **Citalopram confound from 2024-04 (load-bearing).** `stress_mean_sleep` is
  confirmed citalopram-dose-modulated (+0.43 per mg plasma). So from the
  2024-04 initiation, the *level* partly reflects the drug, not the
  underlying autonomic state. **We deliberately do NOT ship a
  dose-corrected line:** the naive correction (`raw - 0.43*dose`) subtracts
  approximately 12.9 at 30 mg, which drives the corrected level to about 3-8,
  *below* the healthy baseline (about 16) and physiologically implausible.
  The reason is that the +0.43/mg beta is a short-window buildup slope, and
  the raw levels before (2022-2023, about 20) and during (2024-2026, about
  17-23) citalopram are in fact *similar*, not 12.9 apart. So the era level
  cannot be cleanly de-confounded on n=1. The honest move: show the raw line,
  shade the citalopram era, and link the driver ledger (R6 / R15 / R16). See
  [`../../../methodology/citalopram_dose_response_confounder_reaudit_2026-07-02.md`](../../../methodology/citalopram_dose_response_confounder_reaudit_2026-07-02.md).
- **Left-censored:** the series starts at the 2021-08-16 Garmin-dump edge, so
  the pre-illness segment is about 7 months, not the whole healthy history.
- Event dates for the overlay are already in `corpus.json`; not duplicated
  here.

## 3. The series (site-consumable JSON)

Named counts (CONVENTIONS §3.6): monthly median + p25/p75 of daily
`stress_mean_sleep` from `per_day_master.csv`; n is non-null days per month
(typically 25-31). Linear-interpolation quantiles.

```json
{"indicator":"stress_mean_sleep","label":"overnight autonomic-load proxy (Garmin HRV-derived stress score, not wellbeing)","aggregation":"monthly median + p25/p75 band","span":["2021-08","2026-05"],"citalopram_from":"2024-04","series":[{"t":"2021-08","n":14,"median":19.13,"p25":11.47,"p75":22.41},{"t":"2021-09","n":30,"median":20.58,"p25":16.26,"p75":26.01},{"t":"2021-10","n":31,"median":15.43,"p25":12.55,"p75":19.58},{"t":"2021-11","n":30,"median":16.57,"p25":12.63,"p75":22.44},{"t":"2021-12","n":31,"median":17.44,"p25":14.19,"p75":22.74},{"t":"2022-01","n":31,"median":9.91,"p25":8.0,"p75":13.47},{"t":"2022-02","n":28,"median":12.66,"p25":10.5,"p75":16.94},{"t":"2022-03","n":31,"median":16.61,"p25":13.79,"p75":25.72},{"t":"2022-04","n":30,"median":21.72,"p25":18.59,"p75":25.08},{"t":"2022-05","n":29,"median":21.42,"p25":19.83,"p75":26.68},{"t":"2022-06","n":30,"median":21.31,"p25":18.6,"p75":24.29},{"t":"2022-07","n":26,"median":13.92,"p25":12.78,"p75":22.28},{"t":"2022-08","n":25,"median":15.02,"p25":12.05,"p75":17.03},{"t":"2022-09","n":30,"median":18.47,"p25":16.65,"p75":19.68},{"t":"2022-10","n":28,"median":20.8,"p25":18.71,"p75":23.3},{"t":"2022-11","n":30,"median":19.58,"p25":17.83,"p75":23.34},{"t":"2022-12","n":30,"median":21.8,"p25":19.67,"p75":25.26},{"t":"2023-01","n":31,"median":20.07,"p25":18.34,"p75":21.6},{"t":"2023-02","n":28,"median":23.8,"p25":20.43,"p75":26.38},{"t":"2023-03","n":31,"median":18.82,"p25":16.57,"p75":22.76},{"t":"2023-04","n":30,"median":17.76,"p25":14.78,"p75":23.77},{"t":"2023-05","n":31,"median":17.32,"p25":13.3,"p75":20.02},{"t":"2023-06","n":30,"median":22.61,"p25":17.52,"p75":27.87},{"t":"2023-07","n":31,"median":15.55,"p25":12.78,"p75":19.48},{"t":"2023-08","n":30,"median":15.88,"p25":14.39,"p75":19.46},{"t":"2023-09","n":29,"median":19.71,"p25":17.59,"p75":20.58},{"t":"2023-10","n":31,"median":19.69,"p25":17.91,"p75":21.02},{"t":"2023-11","n":27,"median":21.32,"p25":17.88,"p75":22.19},{"t":"2023-12","n":30,"median":21.58,"p25":16.89,"p75":26.17},{"t":"2024-01","n":30,"median":18.72,"p25":15.57,"p75":20.73},{"t":"2024-02","n":29,"median":20.73,"p25":18.16,"p75":23.22},{"t":"2024-03","n":30,"median":18.7,"p25":16.59,"p75":19.92},{"t":"2024-04","n":29,"median":16.89,"p25":12.92,"p75":18.39},{"t":"2024-05","n":31,"median":17.14,"p25":15.18,"p75":18.91},{"t":"2024-06","n":30,"median":17.53,"p25":15.64,"p75":20.17},{"t":"2024-07","n":31,"median":17.77,"p25":15.95,"p75":19.77},{"t":"2024-08","n":31,"median":15.95,"p25":14.92,"p75":17.89},{"t":"2024-09","n":29,"median":17.63,"p25":15.6,"p75":19.55},{"t":"2024-10","n":29,"median":19.27,"p25":16.23,"p75":20.49},{"t":"2024-11","n":30,"median":18.66,"p25":16.84,"p75":20.26},{"t":"2024-12","n":31,"median":20.52,"p25":17.5,"p75":22.37},{"t":"2025-01","n":31,"median":22.13,"p25":18.57,"p75":27.9},{"t":"2025-02","n":28,"median":20.32,"p25":18.07,"p75":22.28},{"t":"2025-03","n":31,"median":19.43,"p25":17.67,"p75":21.02},{"t":"2025-04","n":30,"median":19.88,"p25":17.43,"p75":22.19},{"t":"2025-05","n":31,"median":17.34,"p25":15.98,"p75":19.62},{"t":"2025-06","n":30,"median":17.43,"p25":14.43,"p75":19.07},{"t":"2025-07","n":29,"median":18.53,"p25":14.93,"p75":22.23},{"t":"2025-08","n":28,"median":16.44,"p25":14.21,"p75":18.57},{"t":"2025-09","n":30,"median":18.53,"p25":15.79,"p75":20.73},{"t":"2025-10","n":31,"median":19.77,"p25":17.38,"p75":22.42},{"t":"2025-11","n":30,"median":23.16,"p25":16.84,"p75":25.54},{"t":"2025-12","n":31,"median":22.63,"p25":20.43,"p75":26.04},{"t":"2026-01","n":29,"median":21.08,"p25":17.16,"p75":25.04},{"t":"2026-02","n":27,"median":20.21,"p25":17.91,"p75":21.43},{"t":"2026-03","n":31,"median":22.51,"p25":20.43,"p75":25.47},{"t":"2026-04","n":30,"median":18.7,"p25":15.39,"p75":22.04},{"t":"2026-05","n":27,"median":20.2,"p25":18.2,"p75":22.24}]}
```

## 4. Reproducibility

Monthly median + p25/p75 of daily `stress_mean_sleep` from
`per_day_master.csv`, grouped by calendar month, NaN days dropped. The
dose-correction that is deliberately NOT shipped would be
`raw - 0.43*dose_plasma_mg` (see §2 for why it over-corrects at the level).

## 5. Cross-references

- Register R10 (trajectory scrollytelling) + R13 (felt-state timeline, the
  ground-truth sibling).
- [`../../longrun_rhr_trend/findings.md`](../../longrun_rhr_trend/findings.md)
  (the multi-year confounder work; same honesty about proxies drifting for
  non-illness reasons).
- Driver ledger (R6 / R15 / R16) for the citalopram-era caveat.
