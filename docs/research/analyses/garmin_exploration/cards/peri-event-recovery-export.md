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
