# H02b — Trajectory extension: notes

**Replaces the binary train SUPPORTED / validate REFUTED verdict with
a per-anchor view of how the precursor signal fades over time.**

Plot: [trajectory.png](trajectory.png). Data: [trajectory.csv](trajectory.csv).
Script: [trajectory_per_year.py](trajectory_per_year.py).

## What it shows

Rolling 12-month windows anchored monthly. For each anchor, the
discrimination metric is computed on the crash episodes whose start
date falls inside the trailing 12 months, against a 100-window null
sample drawn from the same period.

| anchor (window right edge) | crash n | % crash ≥+10min | % null | discrim. |
|---|---:|---:|---:|---:|
| 2023-08-01 | 9  | 77.8% | 46.0% | **+31.8 pp** |
| 2023-12-01 | 10 | 70.0% | 53.0% | **+17.0 pp** |
| 2024-04-01 | 11 | 45.5% | 40.0% |  +5.5 pp     |
| 2024-08-01 | 14 | 42.9% | 41.0% |  +1.9 pp     |
| 2024-12-01 | 10 | 30.0% | 46.0% | **−16.0 pp** |
| 2025-04-01 |  7 | 28.6% | 28.0% |  +0.6 pp     |
| 2025-08-01 |  3 | 33.3% | 34.0% |  −0.7 pp     |
| 2025-12-01 |  3 | 33.3% | 35.0% |  −1.7 pp     |
| 2026-04-01 |  2 | 50.0% | 41.0% |  +9.0 pp     |

## Reading the trajectory

The signal **decayed smoothly across ~12 months** from a peak of
+31.8 pp in mid-2023 to near zero by mid-2024. Concretely:

- **Aug 2023 (peak)**: 78% of crash lead-ups had a +10min spike vs
  46% of null windows. Difference of 32 pp.
- **Dec 2023**: 70% vs 53%. Difference of 17 pp — still above the
  +15 pp criterion bar.
- **Apr 2024**: 46% vs 40%. Difference of 6 pp — below bar but
  still positive.
- **Aug 2024 onward**: signal is essentially gone.

The "cliff" we initially named the recovery transition is, in this
metric, a 12-month fade.

## What this changes about the H02b verdict

The original H02b result.md said:

> Verdict: TRAIN SUPPORTED, validate near-miss → OVERALL REFUTED per
> the locked rule.

That binary verdict was honest under the pre-registered protocol but
hid the trajectory. The richer story is:

- The precursor signal was real and discriminative through end of
  2023.
- It faded gradually through 2024.
- By late 2024 the signal was gone and briefly inverted.
- 2025–26 windows have too few crashes to say anything definitive
  but read as null.

For card-design purposes, this means a spike-anchored retrospective
card would be **reliable for crashes through ~end of 2023, then
progressively less so**, with the boundary fuzzy not sharp.

## Caveats

- **Small-N windows** (anchors after 2025-08) carry 2–3 crashes
  each. The percentages bounce around but the underlying numbers
  are 0, 1, or 2 events meeting the threshold. Don't over-read.
- **Null sample size 100** per anchor (vs 200 in the main H02b
  test) — keeps the script fast but adds a bit of noise.
- **Rolling 12-month windows overlap heavily** between successive
  anchors. Consecutive points are not statistically independent. The
  curve smoothness partly reflects this overlap.
- **The metric still uses the same lead-up + baseline + spike-
  threshold definitions** as the locked H02b protocol. We are
  computing the same metric in different time slices, not changing
  the metric.

## Combined with S01

S01 (stabilisation trajectories) shows the **typical day's
max-spike duration** fell from ~13 min (mid-2023) to ~6 min
(early-2025) and rebounded to ~11 min (May 2026). H02b-trajectory
shows the **discrimination of crash lead-ups** fell over the same
window.

These two are mechanically related: as the baseline of typical
spikes fell, the threshold for "unusually long" became harder for
crash lead-ups to clear (because there's less "unusual" room to
spike into when the typical is already low). Whether the underlying
crash mechanism truly changed or whether the metric simply lost
sensitivity is partly disentanglable — the absolute lead-up max
values also fell (per the H02b result.md "compression finding"),
not just the relative ones. Both shifted.

## Implication for the stabilisation-arc card

A retrospective card built on the H02b spike-detection metric is
**well-supported for crashes through end of 2023**. Past 2024, the
data thins both in episode count and in signal strength. The card
should:

- Fire confidently on pre-2024 crashes with a quoted note from that
  day.
- Fire with hedged framing ("we see a notable spike that day but
  the pattern is less consistent than it used to be") on 2024–25
  crashes that do have a clear spike (5 of 15 still do).
- Be honest about the fade itself in the multi-year recovery view
  ("the link between intense moments and crashes has weakened over
  time — your residual crashes are different in shape").

---

*Trajectory computed 2026-06-05. Re-runnable any time.*
