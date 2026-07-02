# R23 peri-event COVID known-event check: RESULT

## Tier verdict

**MOVED.** The overnight autonomic factor, read through its anchor
`stress_mean_sleep`, departed the pre-LC healthy baseline toward the
high-autonomic-load pole during the 2022-03 COVID infection window. The
infection window-mean factor-z sits at the **99.23rd percentile** of the
E[L]=7 stationary-bootstrap null, beyond the locked 95th-percentile
threshold in the predicted (high-load) direction, one-sided.

This is a percentile classification against the locked tiers of the
pre-registration ([hypothesis.md §6](hypothesis.md)), nothing more. See
caveat (a): a MOVED result here means the factor **departed baseline
around the infection / LC-onset hinge**, never that the infection caused
the factor to move.

## Authorship

| Field | Value |
|---|---|
| Executed by | Claude (Opus 4.8) producer-mode test execution, for the participant-researcher (repo owner) |
| Date | 2026-07-02 |
| Mode | Producer-mode faithful execution of the LOCKED pre-registration. No design parameter changed. |
| Pre-registration | [hypothesis.md](hypothesis.md), LOCKED 2026-07-02 (before any factor value was inspected). |
| Precondition | [../../descriptive/peri_event_covid/precondition.md](../../descriptive/peri_event_covid/precondition.md) |
| RNG seed (recorded) | `20220321` |

This artefact stays at Layer-1 DESCRIPTIVE. It reports a percentile
classification and the associated numbers. It does NOT interpret what
the classification means for the factor's overall validity: that is a
later Stage-I interpretation step, not this document
([CONVENTIONS §4.1](../../../CONVENTIONS.md)).

---

## 1. What was tested

Faithful execution of the locked pre-registration
([hypothesis.md](hypothesis.md), §4 to §6), backed by the descriptive
precondition
([precondition.md](../../descriptive/peri_event_covid/precondition.md)).

- **Anchor factor-z (primary, g1):** daily `stress_mean_sleep` (HA07c),
  z-scored against the personal pre-LC baseline using robust median +
  MAD over the 217-day pre-LC band, `robust z = (x - median) / (1.4826 *
  MAD)` ([CONVENTIONS §3.1](../../../CONVENTIONS.md)). Sign convention:
  upward = high-load pole. Personal pre-LC baseline: `median = 15.9492`,
  `1.4826 * MAD = 7.8728`.
- **Window statistic:** 14-day-window-mean of the daily factor-z, with a
  window-max companion (max single daily factor-z within the window).
- **Comparator band:** pre-LC healthy era, 2021-08-16 to 2022-03-20, 217
  days, `lc_phase == pre_corona`.
- **Infection window:** 2022-03-21 to 2022-04-03, 14 days,
  `lc_phase == corona_infection`.

Named counts ([CONVENTIONS §3.6](../../../CONVENTIONS.md)): 217
pre-LC baseline days and 14 infection-window days
(`per_day_master.csv`, `lc_phase == pre_corona` / `corona_infection`);
15 independent non-overlapping 14-day pre-LC windows and 204 sliding
14-day pre-LC windows over the same band.

## 2. Primary result

| Quantity | Value |
|---|---:|
| Infection window-mean factor-z | **+1.1115** |
| Infection window-max factor-z (companion) | +6.0461 |
| Null 95th percentile (predicted-direction threshold) | +0.8460 |
| Null 5th percentile (opposite-direction threshold) | -0.4873 |
| Percentile of infection window within null | **99.23** |
| p-analogue (one-sided, high-load direction) | **0.0077** |

Primary p-analogue mechanic (locked, [hypothesis.md §5](hypothesis.md)):
a stationary bootstrap on the daily factor-z series over the 217-day
pre-LC band, expected block length **E[L] = 7 days**
([permutation_null_block_length.md](../../../methodology/permutation_null_block_length.md)),
**10,000 replicates**. Each replicate resamples the daily factor-z
series under E[L]=7 stationary blocks to a synthetic 217-day series,
then computes one 14-day-window-mean factor-z from that synthetic
series; the 10,000 window-means form the reference distribution. The
infection window's percentile within that distribution is the
p-analogue. The infection window lies beyond the 95th-percentile
threshold in the predicted high-load direction: **MOVED**.

## 3. Effect size d2

| Quantity | Value |
|---|---:|
| d2 standardised difference (point) | **+0.8576** |
| d2 95% CI (same E[L]=7 machinery) | **[+0.1582, +1.5656]** |

d2 is the standardised difference of the infection-window mean vs the
pooled pre-LC baseline, in pre-LC-SD units, with the 95% CI drawn from
the **same E[L]=7 stationary-bootstrap machinery** so one null model
serves both the p-analogue and the CI
([hypothesis.md §5](hypothesis.md)). **Direction: positive (high-load).
Magnitude: approximately 0.86 SD.** The CI excludes zero in the
predicted direction.

## 4. n=15 non-overlapping sanity rank

**Rank 1 of 16** (1 = most extreme in the high-load direction; among the
15 non-overlapping pre-LC windows plus the infection window). The
infection window-mean factor-z (+1.11) exceeds every one of the 15
non-overlapping pre-LC fortnights (min -0.633, median +0.315, max
+1.016).

This is a transparent sanity check
([CONVENTIONS §3.6](../../../CONVENTIONS.md)), NOT the primary
inference. It is consistent with the primary p-analogue.

## 5. E[L]* data-driven block-length check

| Quantity | Value |
|---|---:|
| Data-driven E[L]* (Politis-White / Patton-Politis-White) | **7.000** |
| Project default E[L] | 7 |
| Flagged (deviation > factor of 2)? | **No** |
| ACF cutoff lag | 1 |

E[L]* is within 2x of the locked E[L] = 7 (in fact identical to the
default at this resolution). No block-length flag; the E[L]=7 null is
used as locked.

## 6. Triad coherence (g2)

Each channel z-scored against its own personal pre-LC baseline; the
coherence flag checks each channel against **its own predicted sign**
(never a uniform "all z positive" test).

| Channel | Column | Window-mean z | Predicted sign | Moved in own sign? |
|---|---|---:|:---:|:---:|
| HA07c anchor | `stress_mean_sleep` | **+1.1115** | UP (+) | **Yes** |
| HA06b peripheral | `resting_hr` | **-0.2168** | UP (+) | **No** |
| HA10 inverse | `bb_highest` | **-0.7783** | DOWN (-) | **Yes** |

**Coherence flag (all three in own predicted sign on the raw window
mean): FALSE.** Two of the three channels moved in their predicted sign
(`stress_mean_sleep` up, `bb_highest` down); `resting_hr` did not, on the
raw 14-day window mean (its window-mean z is slightly negative, -0.22).

**One signal viewed twice, not independent confirmation.** HA07c
(`stress_mean_sleep`) and HA10 (`bb_highest`) are Spearman rho = -0.92
near-identical ([CONVENTIONS §3.3](../../../CONVENTIONS.md)); the
coherence readout treats them as one signal viewed twice, NOT two
independent witnesses. The two coherent channels are therefore
effectively one coherent signal; the one directly-validated wearable
channel, `resting_hr` (see caveat c), did not move in its predicted sign
on the raw daily-mean window. The coherence flag is a companion check,
not a set of independent confirmations.

## 7. Detrend §3.7 sensitivity (raw g2 triad channels)

The [§3.7](../../../CONVENTIONS.md) detrend audit hook fires on the
**raw** g2 triad channels (not the z-scored primary, whose scope §3.7
excludes), per the locked text: fit a linear trend on the pre-LC raw
channel, extrapolate through the infection window, subtract, then
re-z-score.

| Channel | Detrended window-mean z | Pre-LC slope / day (raw) |
|---|---:|---:|
| `stress_mean_sleep` | **+1.7570** | -0.03197 |
| `resting_hr` | **+1.7656** | -0.03032 |
| `bb_highest` | **-1.3315** | +0.06710 |

**Verdict stability under detrend.** The primary anchor
(`stress_mean_sleep`) is stable: it moves up strongly both raw
(+1.11 window-mean z) and detrended (+1.76). The MOVED tier for the
primary anchor does not depend on the trend. Under detrending, **all
three channels move in their predicted signs** (detrend coherence
preserved = True): the raw `resting_hr` carried a mild downward pre-LC
slope (-0.030 per day), so its infection-window level sits well above the
extrapolated trend once detrended (+1.77), which is the predicted UP
direction. In short: the primary anchor verdict is stable under detrend,
and detrending strengthens rather than weakens the triad coherence. This
is reported as a sensitivity column; it does not change the locked
primary classification, which is the raw-anchor percentile.

## 8. Acute-core overlay (descriptive only, no p-analogue)

Descriptive/visual overlay for the tighter symptom/fever core
2022-03-23 to 2022-03-30 (decision a1 / MINOR-5): it carries **no
separate p-analogue** and is not ranked against the E[L]=7 null.

| Quantity | Value |
|---|---:|
| Acute-core mean factor-z | +1.3200 |
| Acute-core max factor-z | +6.0461 |

## 9. Caveats (carried verbatim in substance from the pre-reg §8)

- **(a) Acute-infection vs LC-onset inseparability (M5).** The infection
  window (2022-03-21 to 2022-04-03) sits on the Stratum-1 to Stratum-2
  boundary and abuts LC onset (`LC_ERA_START = 2022-04-04`, the day after
  the window's close). The acute infection and the beginning of the
  persistent LC autonomic shift are temporally adjacent and cannot be
  separated by this single-event design. This MOVED result is reported as
  "the factor departed baseline around the infection / LC-onset hinge,"
  NEVER as "the acute infection caused the factor to move." The
  window-tail signal especially cannot be attributed to the acute phase
  alone.
- **(b) Stress = Garmin's stress score (an HRV-derived measure), not
  mental stress.** All "stress" language refers to the Firstbeat
  HRV-derived Garmin GSS, not mental or emotional stress.
- **(c) The Forerunner 245 records no direct HRV.** The factor is an HRV
  proxy recovered via the overnight stress / body-battery / resting-HR
  triad. The Garmin-stress-up and body-battery-down legs are one
  inferential step beyond the directly-validated RHR/HRV inputs; the
  strongest direct channel is `resting_hr`. The cited wearable cohorts
  used other device generations (Fitbit / Apple Watch / Oura): the
  direction generalises, the exact magnitude / calibration does not.
- **(d) n=1, single event.** This validates that the factor tracks
  autonomic load on the one available known event; it does NOT establish
  crash-precursor value, and one event cannot separate "the factor tracks
  infection" from "the factor happened to move that fortnight." The reach
  is bounded to this signal, this subject, this one event.
- **(e) The factor is correlational (effective-N approximately 1), not a
  variance-decomposition construct.** No variance-explained percentage is
  defined; the factor is the correlational near-identity of the channels.
  HA07c and HA10 (rho = -0.92) are one signal viewed twice, not two
  independent witnesses ([CONVENTIONS §3.3](../../../CONVENTIONS.md)).
- **(f) Severity characterisation (M4).** The event is home-recovered and
  febrile (days in bed with fever, zero training activities in week 12),
  not hospitalised. This severity anchor justifies down-weighting the
  blunting caveat to moderate: the blunting evidence (Gholami 2012 rat
  endotoxemia; de Castilho 2017 ICU sepsis) is severity-gated, so the
  `MOVED-UNEXPECTED-DIRECTION` tier was a guard, not a prediction.
- **(g) No causal / interpretive marks on the descriptive layer
  ([§4.1](../../../CONVENTIONS.md)).** The claim is "the factor departed
  from baseline around the event," never "the infection caused the factor
  to move."

## 10. Reproducibility

- Test script: [test.py](test.py). Fixed RNG seed `20220321` recorded
  in-file; 10,000 replicates; E[L] = 7; 14-day window.
- Data source: `per_day_master.csv` (unified corpus).
- House utilities reused: `stationary_bootstrap_ci` and
  `compute_data_driven_block_length` from
  [`../../_utils/inference.py`](../../_utils/inference.py) (Politis-Romano
  1994 stationary bootstrap; Politis-White 2004 / Patton-Politis-White
  2009 block-length estimator).

## 11. Cross-references

- [hypothesis.md](hypothesis.md) - the LOCKED pre-registration this test
  implements.
- [../../descriptive/peri_event_covid/precondition.md](../../descriptive/peri_event_covid/precondition.md)
  - the descriptive precondition (event location, coverage, comparator
  band).
- [../../../methodology/permutation_null_block_length.md](../../../methodology/permutation_null_block_length.md)
  - the E[L] = 7 stationary-bootstrap block-length rationale.
- [CONVENTIONS.md](../../../CONVENTIONS.md) - §3.1 (personal baseline),
  §3.6 (named counts), §3.7 (detrend audit hook), §4.1 (no interpretive
  marks on the descriptive layer).
