# Findings - R1 fresh crash lead-up curves (single-pool, descriptive)

**Descriptive Layer-1 extraction** for site request **R1** (beat-2 chart data),
producing the REAL lead-up shape the charts wanted, honestly. Producer-mode, for
the participant-researcher (repo owner), drafted 2026-07-06 by Claude (Opus 4.8).
Reproducible via [`run.py`](run.py).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

**Why this exists**: the [`chart-exports.md`](../../garmin_exploration/cards/chart-exports.md)
assembly flagged two beat-2 charts (F1 parasympathetic-swing, F2 walls-of-orange)
whose requested shape - a per-era `{early[], late[]}` dual swing / a per-year decay
array - is the retired era-split framing and could not be honored without
fabrication. The chosen resolution (2026-07-06) was to replace both the fabricated
curves AND the bare null-chip fallback with a **real, single-pool, per-timestep
lead-up curve**: what the signal actually does in the week before a crash, pooled
across all crashes, against an ordinary-day null band.

**Method**: for each channel, the z-vs-personal-baseline at each day-offset t-6..t0
(0 = crash onset day), using the SAME [d-90, d-30] trimmed-mean/std lagged personal
baseline the locked crash operands use (imported verbatim from the R14 machinery,
[`../operationalisation_support/single_pool_reanchor/run.py`](../operationalisation_support/single_pool_reanchor/run.py)).
Per offset: the mean z across the 29 crash episodes (crash band) and across 200
random ordinary-day windows (null band), each with a bootstrap 95% CI
(seed 20260706, B=10,000). No new hypothesis test, no falsification bar, no
re-lock: this is a descriptive shape per [CONVENTIONS section 2.1 / 4.1](../../../CONVENTIONS.md).
Single-pool (no era split); baseline-relative (no dated raw values); aggregated
per-offset means + CIs only.

---

## 1. Headline

**The departure is at onset, not before it.** Across all three curves the crash
band only separates from the ordinary-day band **at t0 (the crash day itself)**;
through the predictive lead-up (t-6 .. t-1) the crash band sits **inside** the
ordinary-day band. Of the six lead-up offsets, the number whose bootstrap CI
excludes zero is **0 / 6** (parasympathetic-swing), **1 / 6** (walls-of-orange,
a lone t-1 blip in an otherwise-flat null), and **0 / 6** (hrv-decline). Even the
one single-pool SUPPORTED signal (HA07d) has its departure concentrated at onset,
not as a multi-day precursor.

This is the visual confirmation of the R32(a) finding
([`no-visible-trigger-into-crash-signal-export.md`](../../garmin_exploration/cards/no-visible-trigger-into-crash-signal-export.md)):
**the watch reads the crash, not its approach.** A signal that departs at t0 but is
within-band at t-1 .. t-6 characterises the crash, it does not forecast it - which
is exactly why the single-pool windowed discriminations are null or Tier-C.

---

## 2. The three curves

Mean z vs personal baseline per day-offset (0 = crash onset). "crash" = pooled over
the 29 episodes; "null" = ordinary-day band. Bracketed values are the bootstrap 95%
CI at the endpoints; full per-offset CIs are in `summary.json`.

### parasympathetic-swing - HA10 morning body-battery peak (single-pool NOT-SUPPORTED)

| offset | t-6 | t-5 | t-4 | t-3 | t-2 | t-1 | t0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| crash mean z | +0.21 | -0.03 | -0.12 | -0.07 | -0.09 | -0.32 | **-0.92** |
| null mean z | -0.15 | -0.33 | -0.17 | -0.15 | -0.19 | -0.12 | -0.18 |

The morning body-battery peak **collapses at onset** (t0 = -0.92, CI [-1.78, -0.13],
excludes 0) after a lead-up that hugs the null band (0 / 6 lead-up offsets exclude
zero). The "parasympathetic swing" is an at-crash phenomenon, not a lead-up.

### walls-of-orange - H02b per-minute stress-spike minutes (single-pool NOT-SUPPORTED)

| offset | t-6 | t-5 | t-4 | t-3 | t-2 | t-1 | t0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| crash mean z | +0.59 | +0.58 | +0.38 | -0.14 | -0.06 | +0.62 | -0.04 |
| null mean z | +0.54 | +0.39 | +0.41 | +0.48 | +0.40 | +0.52 | +0.19 |

The crash and ordinary-day bands **overlap across the whole week** - a genuine
visual null. The single lead-up offset whose CI excludes zero (t-1, +0.62 CI
[+0.06, +1.22]) is an isolated blip inside an otherwise-flat, NOT-SUPPORTED signal,
not a trajectory. There is no "walls of orange held early then faded" shape to draw.

### hrv-decline - HA07d overnight stress variability (single-pool SUPPORTED, Tier C)

| offset | t-6 | t-5 | t-4 | t-3 | t-2 | t-1 | t0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| crash mean z | -0.22 | +0.69 | -0.22 | +0.44 | +0.07 | +0.61 | **+1.25** |
| null mean z | +0.34 | +0.48 | +0.45 | +0.69 | +0.42 | +0.25 | +0.44 |

Overnight stress variability **spikes at onset** (t0 = +1.25, CI [+0.33, +2.27],
excludes 0) after a noisy lead-up that stays within the null band (0 / 6 lead-up
offsets exclude zero). This is the project's strongest signal, and even here the
real curve shows the departure is concurrent with the crash, not a clean days-ahead
decline. The "hrv-decline over time" framing is dropped; this is the honest
at-onset shape.

---

## 3. What was emitted to the site

Five beat-2 chart JSONs written on disk to
`wiggers_research_story/site/data/charts/` (for the participant-researcher to commit
from the site checkout):

| file | content |
|---|---|
| `parasympathetic-swing.json` | fresh single-pool lead-up curve (HA10 body-battery), crash + null bands |
| `walls-of-orange.json` | fresh single-pool lead-up curve (H02b spikes) - REPLACES the retired-empty placeholder |
| `hrv-decline.json` | fresh single-pool lead-up curve (HA07d variability) |
| `crash-frequency.json` | clean descriptive count per year (5/9/11/2/2; duration buckets), from chart-exports.md |
| `exertion-lead-up.json` | reframed single-pool share pair (HA01b null + HA01c sibling), from chart-exports.md |

Each curve JSON carries `offsets_days_from_onset`, `crash` and
`ordinary_day_null_band` (mean / lo / hi / n_per_offset), the `single_pool_summary`
(disc_pp + CI + verdict), and an honest `note`. The felt-state establishing shot
(`felt-state-timeline.json`, R13) already shipped real data 2026-07-02 and is
untouched.

---

## 4. Caveats per CONVENTIONS section 4.1 + section 4.2

- **t0 is the onset day, not a forecast horizon.** The departures concentrate at
  t0, which is concurrent with the crash (the crash is defined on the felt-state at
  onset). A t0 physiological move is characterisation, not prediction; the
  predictive question is t-6 .. t-1, which sits within the ordinary-day band. The
  charts show the full trajectory including onset - label t0 as onset, not lead-up.
- **Descriptive shape, no verdict.** The single-pool windowed verdicts
  (NOT-SUPPORTED / SUPPORTED-Tier-C) come from R14; these curves are the shape
  behind those numbers, not a new test. No falsification bar.
- **Wide CIs at n=29.** The crash band is pooled over ~26 episodes per offset (3-4
  lack a computable 40-day baseline); the bootstrap CIs are wide. Bands are
  episode-to-episode spread, not error of a fitted line.
- **Single-pool, baseline-relative.** No era split; z vs the personal lagged
  baseline; no dated raw values; aggregated per-offset means only.
- **The null band is not exactly zero.** z-vs-lagged-baseline for ordinary days
  centres slightly off zero on some channels (trimmed-baseline + skew); the honest
  read is the crash band relative to the null band, not to an absolute zero line.
- **n=1; no causal marks.** "In this body, body-battery collapsed at crash onset",
  never "the crash was caused / predicted by it".

---

## 5. Verification log

- **Machinery**: reused the R14 lagged baseline verbatim
  (`compute_lagged_baseline`, `build_null_dates`, `_index_master` imported from
  `single_pool_reanchor/run.py`); [d-90, d-30] trimmed mean/std, min 40 valid days.
- **Channels + sigma floors**: bb_highest (2.0), max_spike_minutes (1.0),
  stress_stdev_sleep (0.5).
- **Offsets**: t-6 .. t0 relative to `episode_start`. Pooling: mean z per offset;
  bootstrap 95% CI, seed 20260706, B=10,000. Null: 200 windows, legacy seed 20260605.
- **n_crash per offset**: ~26 (of 29); n_null 200.
- **t0 CI excludes zero**: HA10 [-1.78, -0.13], HA07d [+0.33, +2.27]; H02b spans
  zero. Lead-up (t-6..t-1) offsets excluding zero: 0/6, 1/6, 0/6.
- **Operand-source path**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`
  + `labels_crash_v2.csv`.
- **Machine-readable**: `summary.json` (gitignored per the `docs/research/**/*.json`
  rule). Site JSON target overridable via `GEVOELSCORE_SITE_PATH`.

---

## 6. Cross-references

- **Assembly + reframe this implements**: [`analyses/garmin_exploration/cards/chart-exports.md`](../../garmin_exploration/cards/chart-exports.md)
  (R1; flags F1/F2/F3, the retired-decay reframe).
- **Verdicts behind the curves**: [`analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../operationalisation_support/single_pool_reanchor/findings.md)
  (R14) + `cards/trust-panel-export.md`.
- **The finding these curves confirm**: [`analyses/garmin_exploration/cards/no-visible-trigger-into-crash-signal-export.md`](../../garmin_exploration/cards/no-visible-trigger-into-crash-signal-export.md)
  (R32a; the watch reads the crash, not its approach).
- **Home establishing shot (already shipped)**: `felt_state_timeline/` (R13).
- **Site register R1** (this deliverable). External repo `wiggers_research_story`,
  `docs/research-requests.md` + `site/data/charts/`.

---

*End of findings.*
