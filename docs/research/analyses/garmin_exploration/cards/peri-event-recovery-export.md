# Peri-event recovery curve export (R9)

**Status**: producer-mode Layer-1/3 descriptive export for site request **R9**
(the shape of getting back up: every crash aligned at its felt-state nadir,
individual episodes + an average line). Aggregated and privacy-safe:
**relative-to-nadir days only, no calendar dates**. No interpretive or causal
marks (CONVENTIONS §4.1). Drafted 2026-07-02 by Claude (Opus 4.8),
producer-mode, for the participant-researcher (repo owner).

## 1. What this is

Each of the **29 crash episodes** aligned at its felt-state nadir (t0 = the
lowest-gevoelscore day of the episode), with two metrics tracked across
t-3..t+14: the felt-state (`gevoelscore`, the lived recovery) and the
overnight autonomic-load proxy (`stress_mean_sleep`). The average line + the
per-episode spread show "the shape of getting back up."

## 2. The finding (descriptive)

- **Felt-state recovers fast, in a sharp V.** Median gevoelscore falls to the
  nadir (t0 median **2**), bounces to **3** at t+1, **4** by t+2-3, and then
  **plateaus at 4-5** for the rest of the fortnight. The return to the usual
  band takes about **2-3 days**.
- **The plateau is the lived ceiling.** Recovery returns to ~4-5, not higher;
  the felt-state ceiling (the body rarely passing 6, per R13) reasserts. This
  is not "full recovery to a high", it is "back to the constrained normal."
- **Overnight stress settles more slowly.** `stress_mean_sleep` is elevated
  around the nadir (t-1/t0 median ~21) and drifts down only gradually to
  ~18-19 by t+8-14, a gentler, slower curve than the felt-state snap-back.

## 2b. Dip recovery signature, and the crash-vs-dip autonomic contrast

The same alignment was run on the **79 dips** (transient single-bad-days, all
1-day episodes; aligned at the dip day t0). The contrast with crashes is the
informative result:

| | crashes (n=29) | dips (n=79) |
|---|---|---|
| felt-state at nadir (t0 median) | **2** (deeper) | **3** (shallower) |
| felt-state recovery | V over ~2-3 days | single-day notch (back to 4 at t+1) |
| overnight stress (`stress_mean_sleep`) around nadir | **ELEVATED (~21)**, settles slowly over ~2 weeks | **FLAT (~18-19)**, no elevation at all |

**The autonomic signature separates crashes from dips.** A crash carries an
overnight-stress perturbation (elevated at the nadir, slow settle); a dip does
NOT (the overnight stress is flat straight through it). So the watch's stress
channel physiologically distinguishes a real crash from a transient
felt-state notch. This is consistent with the site's crash-vs-dip framing (R13:
sustained crashes vs growing transient dips) and with "the watch sees the
crash": it sees crashes, not dips. (Descriptive; the felt-state depth at t0 is
definitional for both, so the load-bearing contrast is the *autonomic* one.)

Dip recovery curves (aggregated, relative days, no dates):

```json
{"note":"DIP recovery curves aligned at each dip day (t0); relative days only, no dates","t_axis":[-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],"n_dips":79,"gevoelscore":{"aggregate":[{"t":-3,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":-2,"n":79,"median":5.0,"p25":4.0,"p75":5.0},{"t":-1,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":0,"n":79,"median":3.0,"p25":3.0,"p75":3.0},{"t":1,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":2,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":3,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":4,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":5,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":6,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":7,"n":79,"median":5.0,"p25":4.0,"p75":5.0},{"t":8,"n":79,"median":5.0,"p25":4.0,"p75":5.0},{"t":9,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":10,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":11,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":12,"n":79,"median":4.0,"p25":4.0,"p75":5.0},{"t":13,"n":79,"median":5.0,"p25":4.0,"p75":5.0},{"t":14,"n":79,"median":4.0,"p25":4.0,"p75":5.0}]},"stress_mean_sleep":{"aggregate":[{"t":-3,"n":79,"median":18.81,"p25":15.79,"p75":21.47},{"t":-2,"n":79,"median":18.68,"p25":15.95,"p75":20.45},{"t":-1,"n":78,"median":18.9,"p25":16.7,"p75":23.26},{"t":0,"n":76,"median":18.55,"p25":16.57,"p75":21.78},{"t":1,"n":76,"median":18.97,"p25":16.92,"p75":21.58},{"t":2,"n":77,"median":18.94,"p25":16.88,"p75":22.9},{"t":3,"n":79,"median":18.78,"p25":16.38,"p75":21.92},{"t":4,"n":76,"median":18.84,"p25":16.64,"p75":21.6},{"t":5,"n":78,"median":19.56,"p25":16.12,"p75":22.59},{"t":6,"n":77,"median":19.93,"p25":17.05,"p75":22.96},{"t":7,"n":76,"median":19.02,"p25":16.49,"p75":21.77},{"t":8,"n":79,"median":18.98,"p25":15.77,"p75":21.39},{"t":9,"n":78,"median":19.9,"p25":16.85,"p75":23.2},{"t":10,"n":77,"median":19.21,"p25":15.84,"p75":21.84},{"t":11,"n":76,"median":18.6,"p25":16.1,"p75":22.97},{"t":12,"n":77,"median":19.38,"p25":16.45,"p75":23.41},{"t":13,"n":77,"median":19.59,"p25":16.89,"p75":21.46},{"t":14,"n":78,"median":19.84,"p25":17.32,"p75":22.37}]}}
```

Note: `stress_mean_sleep` from ~2024-04 is citalopram-dose-modulated, so the
dip/crash stress-level comparison is cleanest within a single medication era;
the crash-vs-dip *shape* contrast (elevation vs flat around t0) is a
within-window effect and robust to the slow dose drift.

## 2c. Literature anchor (external validation of the shape)

The symptom-fast / autonomic-slow shape is corroborated by published PEM
recovery literature (reads no project data):
[`../../../literature/reviews/pem_recovery_trajectory_review.md`](../../../literature/reviews/pem_recovery_trajectory_review.md).
Key points:

- **PEM recovery is prolonged, days-to-weeks** (Moore 2023: mean ~12.7 days in
  ME/CFS, range 1-64, vs ~2.1 days in controls). Our ~2-week overnight-stress
  settle sits well inside this.
- **The autonomic channel is the slowest to recover.** Radin 2021 (JAMA Netw
  Open): resting HR took ~79 days to normalise (biphasic) while step count
  (~32d) and sleep (~24d) settled far sooner. So a felt-state that rebounds in
  2-3 days while an autonomic index settles over weeks is the *expected*
  ordering, not an anomaly.
- **Our felt-state rebound (2-3 d) is fast relative to ME/CFS norms** (the
  mild / control-adjacent tail), consistent with the felt-state *understating*
  the true, slower physiological recovery, which is precisely the dissociation.
- **Honest caveat (from the review):** no published study paired a daily
  felt-state and an overnight HRV-derived index through the *same* spontaneous
  crash, so the exact pairing is an inference from adjacent literatures, and
  PEM recovery-trajectory quantification is genuinely thin.

## 3. Two honesty flags the site MUST carry

- **The felt-state DEPTH at t0 is definitional, not a finding.** Crashes are
  defined as low-felt-state episodes, so the gevoelscore nadir being low is
  true by construction. What is informative is the **recovery SHAPE** (how
  fast it returns), not the depth.
- **The `stress_mean_sleep` curve is the independent one.** It is a separate
  channel aligned at the felt-state nadir, so its elevation-around-nadir and
  slow settle are NOT circular; that curve is the more informative of the two.
- **n=29, show the spread.** Per-day n is 26-29 (some nadir+k days miss data);
  the per-episode arrays are provided so the visual shows individual lines and
  the band, not just the mean.

## 4. The export (aggregated + per-episode, relative days only)

`t_axis` is days relative to the felt-state nadir (t0). `aggregate` gives
per-day median + p25/p75 + n across episodes. `gevoelscore.episodes` is the 29
per-episode arrays (de-identified, relative days, no dates) for the individual
faint lines; `null` = missing day.

```json
{"note":"peri-event recovery curves aligned at each crash felt-state nadir (t0); relative days only, no dates","t_axis":[-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],"n_episodes":29,"gevoelscore":{"aggregate":[{"t":-3,"n":28,"median":4.5,"p25":4.0,"p75":5.0},{"t":-2,"n":28,"median":4.0,"p25":4.0,"p75":5.0},{"t":-1,"n":28,"median":4.0,"p25":3.75,"p75":4.25},{"t":0,"n":29,"median":2.0,"p25":2.0,"p75":3.0},{"t":1,"n":29,"median":3.0,"p25":3.0,"p75":3.0},{"t":2,"n":29,"median":4.0,"p25":3.0,"p75":4.0},{"t":3,"n":29,"median":4.0,"p25":4.0,"p75":5.0},{"t":4,"n":29,"median":4.0,"p25":4.0,"p75":5.0},{"t":5,"n":29,"median":4.0,"p25":4.0,"p75":5.0},{"t":6,"n":29,"median":4.0,"p25":4.0,"p75":5.0},{"t":7,"n":29,"median":4.0,"p25":4.0,"p75":5.0},{"t":8,"n":29,"median":4.0,"p25":4.0,"p75":5.0},{"t":9,"n":29,"median":4.0,"p25":4.0,"p75":5.0},{"t":10,"n":29,"median":4.0,"p25":4.0,"p75":5.0},{"t":11,"n":29,"median":5.0,"p25":4.0,"p75":5.0},{"t":12,"n":29,"median":5.0,"p25":4.0,"p75":5.0},{"t":13,"n":29,"median":4.0,"p25":4.0,"p75":5.0},{"t":14,"n":29,"median":4.0,"p25":4.0,"p75":5.0}],"episodes":[[null,null,null,2,3,4,4,4,3,4,2,5,5,4,3,4,3,1],[3,4,3,1,2,3,3,4,3,1,3,4,4,4,5,5,2,3],[4,5,5,2,3,4,5,5,5,2,5,4,5,5,5,5,5,4],[4,4,3,2,3,4,5,3,4,5,5,3,4,4,5,5,5,4],[5,5,5,2,3,3,3,4,5,5,5,5,5,5,5,5,4,3],[4,4,2,1,2,2,3,4,4,4,4,5,5,4,5,5,4,4],[4,2,4,2,3,4,4,3,4,5,5,5,5,4,4,4,4,4],[4,4,3,2,3,2,3,3,3,4,4,3,4,3,3,4,5,5],[4,3,4,3,3,4,5,5,5,4,5,5,5,5,3,5,5,5],[5,4,4,3,3,5,4,4,5,5,5,4,3,3,4,5,5,4],[5,5,4,3,3,4,5,5,4,5,4,4,4,4,2,3,4,4],[4,4,4,2,3,4,4,4,4,3,4,4,4,3,4,5,4,5],[4,3,4,2,2,3,2,3,4,5,5,5,5,4,5,4,5,5],[5,3,3,1,1,1,2,3,3,2,3,3,3,3,3,4,3,4],[3,4,4,3,3,4,4,4,4,4,2,4,3,3,4,4,4,4],[4,2,4,3,3,4,4,4,4,4,4,4,4,4,5,4,4,5],[5,5,4,3,3,5,4,3,5,4,4,4,4,3,3,3,4,4],[4,4,4,3,3,3,4,4,3,3,4,4,4,4,4,3,4,5],[5,5,5,3,3,4,5,5,4,4,4,5,5,5,5,4,4,4],[5,5,5,2,3,5,4,5,5,4,4,4,5,5,5,5,5,4],[5,4,5,3,3,5,4,5,5,4,2,3,4,5,5,5,4,4],[5,5,4,2,3,4,5,5,5,4,4,5,4,4,4,5,5,4],[5,5,3,2,3,4,4,4,4,5,5,5,5,5,5,5,4,3],[5,5,4,3,3,5,4,4,4,5,5,5,5,5,5,4,3,4],[4,4,3,2,2,3,4,5,4,5,5,2,4,3,4,4,4,4],[4,4,4,3,3,4,4,4,4,5,5,5,5,5,4,5,3,5],[5,5,5,3,3,4,5,4,5,6,5,5,5,5,6,5,5,4],[5,6,5,2,3,5,5,5,5,4,4,3,3,4,5,6,5,5],[5,4,4,3,3,4,5,6,5,5,5,6,5,5,5,5,4,4]]},"stress_mean_sleep":{"aggregate":[{"t":-3,"n":29,"median":19.08,"p25":17.15,"p75":23.48},{"t":-2,"n":29,"median":19.36,"p25":16.11,"p75":20.58},{"t":-1,"n":28,"median":21.23,"p25":18.37,"p75":25.16},{"t":0,"n":29,"median":21.29,"p25":18.4,"p75":27.48},{"t":1,"n":29,"median":19.62,"p25":16.12,"p75":22.96},{"t":2,"n":27,"median":23.09,"p25":17.1,"p75":28.0},{"t":3,"n":29,"median":20.4,"p25":17.2,"p75":24.67},{"t":4,"n":29,"median":19.97,"p25":17.32,"p75":23.47},{"t":5,"n":29,"median":20.45,"p25":16.96,"p75":23.86},{"t":6,"n":28,"median":19.75,"p25":17.47,"p75":21.65},{"t":7,"n":29,"median":19.21,"p25":16.44,"p75":22.47},{"t":8,"n":27,"median":18.68,"p25":16.61,"p75":20.35},{"t":9,"n":29,"median":19.43,"p25":17.89,"p75":20.96},{"t":10,"n":27,"median":19.55,"p25":16.88,"p75":21.78},{"t":11,"n":28,"median":17.71,"p25":15.7,"p75":21.3},{"t":12,"n":28,"median":19.31,"p25":15.02,"p75":23.47},{"t":13,"n":26,"median":18.69,"p25":14.9,"p75":22.77},{"t":14,"n":26,"median":18.21,"p25":16.95,"p75":19.65}]}}
```

## 5. Reproducibility

Crash episodes from the `crash_episode_id` + `is_crash` columns of
`per_day_master.csv` (29 episodes); nadir = the min-`gevoelscore` day per
episode; the two metrics read from the daily series at nadir+k for
k in [-3, 14]. Median + p25/p75 across episodes per relative day; per-episode
arrays de-identified to relative days.

## 6. Cross-references

- Register R9 (peri-event recovery curve, prototype `peri-event-recovery.html`)
  + R7 (post-crash recovery signatures, the Beyond-the-guide sibling).
- [`recovery-phase-quartiles-export.md`](recovery-phase-quartiles-export.md)
  (R28, the per-phase distributions) and R13 (the felt-state ceiling context).
