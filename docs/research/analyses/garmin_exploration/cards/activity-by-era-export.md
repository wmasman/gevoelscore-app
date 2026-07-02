# Activity-by-era export (R11)

**Status**: producer-mode Layer-1 descriptive export for site request **R11**
(activity before/after, the "fit-then-collapsed" story snapshots). Aggregated
and privacy-safe: **era-level counts only, no dated tracks, no GPS, no raw
per-activity rows**. No interpretive or causal marks (CONVENTIONS §4.1).
Drafted 2026-07-02 by Claude (Opus 4.8), producer-mode, for the
participant-researcher (repo owner).

## 1. What this is

Recorded Garmin activity aggregated by era, for the site's personal-story
"activity before/after" beat (prototype `story-data-snapshots.html`). It shows
the collapse of structured endurance training after Long COVID onset, as
counts / rates / volume only.

## 2. The export (aggregated, per era)

Named counts (CONVENTIONS §3.6): logged Garmin activities from
`processed/garmin/activities.csv`, era spans from the LC timeline
(`lc_era_temporal_segmentation.md`). Distance is stored in centimetres in the
source (verified by pace: raw/100000 = km gives ~6 min/km for runs); km below
are corrected.

| era | span | sessions | sessions/wk | runs | cycles | walks | other | km | km/wk | active hrs | % days active |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **pre-illness** | 2021-08-16 to 2022-03-20 | 103 | 3.32 | **82** | 17 | 3 | 1 | 1707 | **55.0** | 120 | **45.6%** |
| covid-acute | 2022-03-21 to 2022-04-03 | 1 | 0.50 | 0 | 1 | 0 | 0 | 55 | 27.4 | 3 | 7.1% |
| **LC early** | 2022-04-04 to 2023-12-31 | 256 | 2.81 | **4** | 20 | **231** | 1 | 685 | 7.5 | 160 | 33.4% |
| **LC later** | 2024-01-01 to 2026-03-19 | 42 | 0.36 | **0** | 4 | 34 | 4 | 85 | 0.7 | 18 | 4.4% |
| LC taper | 2026-03-20 to 2026-06-05 | 2 | 0.18 | 0 | 0 | 0 | 2 | 0 | 0.0 | 1 | 2.6% |

**The honest reading of the collapse (present via the running-specific rows,
not raw session count):** structured endurance training (runs, km/week) drops
to near zero after LC onset; the LC-early session count stays moderate only
because **231 walks** replace running (a different, lower-intensity activity,
consistent with the pacing shift). The cleanest collapse markers are
**runs (82 to 4 to 0)**, **km/week (55 to 7.5 to 0.7)**, and **% days active
(46% to 33% to 4%)**.

## 3. Site-consumable JSON shape

```json
{
  "unit_note": "distance corrected from source centimetres; km per week",
  "eras": [
    {"id":"pre_illness","label":"before","sessions":103,"sessions_per_wk":3.32,"runs":82,"cycles":17,"walks":3,"other":1,"km":1707,"km_per_wk":55.0,"active_hrs":120,"pct_days_active":45.6},
    {"id":"lc_early","label":"after (2022-2023)","sessions":256,"sessions_per_wk":2.81,"runs":4,"cycles":20,"walks":231,"other":1,"km":685,"km_per_wk":7.5,"active_hrs":160,"pct_days_active":33.4},
    {"id":"lc_later","label":"after (2024+)","sessions":42,"sessions_per_wk":0.36,"runs":0,"cycles":4,"walks":34,"other":4,"km":85,"km_per_wk":0.7,"active_hrs":18,"pct_days_active":4.4}
  ]
}
```

(The `covid_acute` and `lc_taper` rows are tiny transition slivers; fold into
the neighbouring eras or omit on the site.)

## 4. Caveats (the site must carry these)

- **Left-censored:** activity records begin at the 2021-08-16 GDPR-dump edge,
  so "pre-illness" is the last ~7 months of a longer training history, not
  its whole. The pre-illness volume is a floor, not a peak.
- **Logging completeness varies by era.** Structured workouts (runs, rides)
  are reliably logged; casual walking is logged inconsistently, so the LC-era
  **walk** counts are a lower bound and the walk-vs-run mix should be read as
  directional, not exact.
- **Descriptive only.** This is the recorded-activity shape by era, not a
  claim about capacity or cause. Pair it on the site with the deconditioning
  driver-ledger finding (R12 leg) for the "what it did to the body" half.
- No dated tracks, no GPS, no per-activity rows leave this export.

## 5. Reproducibility

- Source: `processed/garmin/activities.csv` (session-level; 404 rows total).
- Era spans: `lc_era_temporal_segmentation.md`.
- **Unit gotcha:** the source distance field is in centimetres despite a
  `distance_m` name (verified by running pace); use raw/100000 for km.

## 6. Cross-references

- Register R11 (activity before/after, Layer 1 story snapshot).
- [`../../longrun_rhr_trend/driver_ledger.md`](../../longrun_rhr_trend/driver_ledger.md)
  and [`../../descriptive/training_load_coverage/precondition.md`](../../descriptive/training_load_coverage/precondition.md)
  (the same activity data underpins the deconditioning / fitness driver).
