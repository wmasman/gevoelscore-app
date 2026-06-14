# crash_v2 episode geometry — descriptive overlay

*Per-event geometry on labels_crash_v2.csv x per_day_master.csv. Generated*
*2026-06-12 from `c:/tmp/layer3_crash_geometry.py`. Pure-observation per the*
*no-interpretive-marks rule: describes distributions and raw counts, does*
*not interpret. Re-run when the master or labels change.*

**Scope.** This document characterises (a) inter-event geometry of the
crash_v2 events, (b) an empirically-derived recovery window, (c) a candidate
prolonged-episode merge rule for peri-event analyses, and (d) co-occurrence
of illness markers within the proposed prolonged events. It is an overlay
proposal; **crash_v2 is locked** at
`docs/research/analyses/hypotheses/crash_v2-definition/definition.md` and is
not modified by this work.

**Inputs.**

- `unified/per_day_master.csv` (1755 x 172) — `date`, `gevoelscore`,
  `is_crash`, `is_dip`, `dip_type`, `crash_episode_id`, `pwc_illness_flag`,
  `cat_sub_keel_resp`, `cat_sub_systemisch_vermoeid`, `lc_phase`.
- `processed/crash_labels/labels_crash_v2.csv` (1372 x 12) — `label`,
  `episode_id`, `tail_median`, `tail_n_days`, `in_crash_tail`,
  `dip_cluster_id`.

**Read-out caveats** (pure observation; interpretation deferred):

- All crash and dip events fall in `lc_phase == 'lc'` by construction
  (`gevoelscore` corpus starts 2022-09-03). No events lie in `pre_corona`
  or `corona_infection`. `lc_phase` is the only data-driven temporal
  phase column on the master; no within-`lc` sub-phase column exists, so
  no further temporal stratification is performed in this pass (see §5).
- `dip_type` is a notes-categorisation tag and is populated for only
  35 days in the master (1 of 79 dip events). The brainfog-only-dip
  count in task 7 is therefore a lower bound on what is actually a
  brainfog-only event.
- Distributions are NOT corrected for seasonality, day-of-week, or
  umbrella event labels.

---

## 1. crash-episode length distribution

Total crash episodes: **29** (matches locked v2 spec).
Length is `end - start + 1` in calendar days (gevoelscore corpus is
complete-coverage; no missing-day gap effects observed).

| population | n | min | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|
| all crash episodes | 29 | 2 | 2 | 2 | 4 | 7.4 | 14 | 3.55 |

---

## 2. inter-event gap distribution

Gap = `next_event.start - prev_event.end - 1` (full clean days between
the end of event A and the start of event B). Three populations.

By definition of the v2 3-day intra-crash merge rule, crash->crash gaps
here are all >= 3.

| pair | n | min | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|
| crash -> crash | 10 | 4 | 5.2 | 7 | 8.8 | 10.9 | 19 | 8.00 |
| crash -> dip | 18 | 7 | 9.2 | 11.5 | 13.8 | 19.9 | 28 | 13.06 |
| dip -> crash | 18 | 1 | 2.2 | 5.5 | 13.2 | 17.9 | 21 | 8.06 |
| dip -> dip (informational) | 61 | 1 | 4 | 8 | 15 | 23 | 57 | 11.72 |

### gap bucket counts (informational shape readout)

| bucket (days) | crash->crash | crash->dip | dip->crash |
|---|---|---|---|
| 0-3 | 0 | 0 | 6 |
| 4-7 | 6 | 1 | 5 |
| 8-14 | 3 | 13 | 3 |
| 15-30 | 1 | 4 | 4 |
| 31-60 | 0 | 0 | 0 |
| 61-120 | 0 | 0 | 0 |
| 121+ | 0 | 0 | 0 |

---

## 3. empirical recovery window (isolated crash episodes)

Isolated = no other crash or dip starts within 30 days after the
episode_end. Identified: **1** isolated crash episodes
out of 29 total.

Two operationalisations of "recovered":

- **(A) rolling-30d baseline**: time-to-first-day where
  `gevoelscore >= rolling_30d_median` (lagged by 1 day, over scored
  days only; min 10 observations required).
- **(B) v2 tail_median**: time-to-first-day where
  `gevoelscore >= tail_median` (per-episode value already stored in
  `labels_crash_v2.csv`).

Day counts are days after `episode_end` (so 1 = the day immediately
after the episode ends). Cap = 60 days.

| op | n | min | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|
| (A) vs rolling 30d median | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2.00 |
| (B) vs v2 tail_median | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2.00 |

Both operationalisations are reported. Op (A) p75 = **2** days.
Op (B) p75 = **2** days.

### supplementary — relaxed isolation windows

With the strict 30-day isolation filter, only one crash episode in the
corpus qualifies as "isolated", so the primary table's p-statistics
collapse onto a single observation. The table below reports the same
distribution for progressively looser isolation thresholds. **This is
informational only**; the brief asks for the strict-30-day p75 as the
operational threshold, and that is what task 4 uses.

| isolation window | n isolated | op A p50 | op A p75 | op A p90 | op B p50 | op B p75 | op B p90 |
|---|---|---|---|---|---|---|---|
| >7d no event | 24 | 1 | 1 | 2 | 1 | 2 | 2 |
| >14d no event | 7 | 1 | 1.5 | 2 | 2 | 2 | 2 |
| >21d no event | 3 | 2 | 2 | 2 | 2 | 2 | 2 |
| >30d no event | 1 | 2 | 2 | 2 | 2 | 2 | 2 |

---

## 4. proposed prolonged-episode merge rule

**Sketch:**

```
for each pair of consecutive events (crash or dip), sorted by start date:
    gap = (next.start - prev.end).days - 1
    if gap < recovery_window_p75:
        merge into prolonged_event
# Applied transitively across chains via union-find.
```

Applied with threshold = **2 days** (op-A p75, rounded).

### counts

| class | count |
|---|---|
| isolated_crash | 26 |
| isolated_dip | 69 |
| prolonged_crash_dip | 3 |
| prolonged_dip_only | 3 |
| **prolonged (any non-singleton)** | **6** |

### composition of prolonged (non-singleton) events

| class | n | median crashes | median dips | median span (d) | min span | max span |
|---|---|---|---|---|---|---|
| prolonged_crash_dip | 3 | 1 | 1 | 7 | 6 | 11 |
| prolonged_dip_only | 3 | 0 | 2 | 3 | 3 | 3 |

### supplementary — sensitivity sweep over alternative thresholds

How merge counts change with the merge-gap threshold (informational
only; the user picks the operational threshold).

| threshold (d) | n prolonged | isolated crash | isolated dip | c->c | c->d | d->d | median span | max span |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 29 | 79 | 0 | 0 | 0 | 0 | 0 |
| 2 | 6 | 26 | 69 | 0 | 3 | 3 | 4 | 11 |
| 3 | 10 | 24 | 59 | 0 | 5 | 5 | 6 | 11 |
| 5 | 17 | 19 | 45 | 1 | 8 | 8 | 7 | 17 |
| 7 | 22 | 12 | 29 | 2 | 11 | 9 | 9 | 34 |
| 14 | 21 | 1 | 9 | 1 | 13 | 7 | 21 | 138 |

Per-day proposed labels saved as sidecar to
`processed/crash_labels/prolonged_episodes_proposed.csv`
(189 rows across 101 prolonged ids).

Columns: `prolonged_episode_id`, `date`, `crash_episode_id` (nullable),
`dip_event_id` (nullable), `dip_cluster_id` (nullable), `prolonged_class`
(`isolated_crash` / `isolated_dip` / `prolonged_crash_dip` /
`prolonged_crash_crash` / `prolonged_dip_only`).

---

## 5. LC-phase stability check

All 29 crash episodes and all 79 dip events fall in `lc_phase == 'lc'`.
`pre_corona` and `corona_infection` cells are empty (n = 0) by
construction: the `gevoelscore` corpus starts 2022-09-03, after
`LC_ERA_START` (2022-04-04). The recovery-window measurement from §3
(n = 1, the single isolated-crash on 2025-10-03) also lies in
`lc_phase == 'lc'`.

| lc_phase | n_crash_episodes | n_dip_events | recovery-window measurements |
|---|---|---|---|
| pre_corona | 0 | 0 | 0 |
| corona_infection | 0 | 0 | 0 |
| lc | 29 | 79 | 1 |

No within-`lc` sub-phase stratification is performed. `lc_phase` is the
only data-driven temporal phase column on the master; no within-`lc`
sub-phase indicator exists. Any sub-phase split would have to come
from a future derived signal (e.g. a data-driven threshold on
`gevoelscore_rolling_std_90d` or equivalent); when such a column lands
in the master and the dictionary, this section can be rerun.

---

## 6. illness-marker co-occurrence within prolonged events

Span = `[span_start - 3 days, span_end]`. For each non-singleton
prolonged event we record whether any of the three markers is
positive on any day within that span. No interpretation.

Marker semantics:
- `pwc_illness_flag`: True / False / NaN; counted positive if any True.
- `cat_sub_keel_resp`: integer 0..2 (note-derived); counted positive if > 0.
- `cat_sub_systemisch_vermoeid`: integer 0..3; counted positive if > 0.

### overall (across all prolonged events)

| metric | count |
|---|---|
| n prolonged events (non-singleton) | 6 |
| with pwc_illness_flag = True in span or pre-3 | 2 |
| with cat_sub_keel_resp > 0 in span or pre-3 | 2 |
| with cat_sub_systemisch_vermoeid > 0 in span or pre-3 | 4 |

### by class

| class | n | pwc_illness | keel_resp | systemisch_vermoeid |
|---|---|---|---|---|
| prolonged_crash_dip | 3 | 2 | 2 | 1 |
| prolonged_dip_only | 3 | 0 | 0 | 3 |

---

## 7. edge cases

| edge case | count |
|---|---|
| prolonged events containing brainfog-only dips (no general, no crashes) | 0 |
| prolonged events spanning an lc_phase boundary | 0 |
| prolonged events at corpus boundary (span_end within 7 days of master max) | 0 |

Note on dip_type sparsity: only 35 days carry a `dip_type` tag in the
master and only 1 of the 79 dip events has a tagged day, so the
brainfog-only-dip count is a lower bound by data sparsity, not by rule.

---

*End of crash_v2 geometry descriptive overlay. The user reviews and
decides whether to fold the proposed prolonged-episode rule into
`per_day_master.csv` (adding a `prolonged_episode_id` column +*
*DATA_DICTIONARY.md entry).*