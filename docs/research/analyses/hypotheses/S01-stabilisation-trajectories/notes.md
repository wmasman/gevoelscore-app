# S01 — Stabilisation trajectories: notes

**Status: descriptive trajectory analysis, no hypothesis test.**

Plot: [stabilisation-arc.png](stabilisation-arc.png). Data:
[trajectories.csv](trajectories.csv). Script:
[compute_trajectories.py](compute_trajectories.py).

The pendulum, visible. Four metrics, each as a 90-day rolling trimmed
mean anchored every 7 days, across the full Garmin window
(2021-08-16 → 2026-06-05). Reference lines mark the LC diagnosis
(2022-05-06), the gevoelscore tracking start (2022-09-03), and the
analytical era split (2023-12-31) — the last is *not* a real phase
boundary, just where we cut for episode-balanced analysis.

## What the trajectories show

Selected anchor dates (full table in trajectories.csv):

| anchor date | RHR | avg stress | sleep eff. | max spike (min) |
|---|---:|---:|---:|---:|
| 2021-11-14 *(pre-LC)* | 55.1 | 32.6 | 0.987 | 10.5 |
| 2022-06-12 *(just post-dx)* | 54.9 | 36.2 | 0.990 | 10.4 |
| 2023-01-08 | 55.4 | 34.7 | 0.993 | 11.2 |
| 2023-08-06 | 55.2 | 35.4 | 0.993 | **13.2** ← peak spike |
| 2024-03-03 | 56.6 | 33.0 | 0.993 | 9.6 |
| 2024-09-29 | 53.9 | 30.3 | 0.991 | 8.2 |
| 2025-04-27 | 57.8 | **29.1** | 0.995 | **5.8** ← trough |
| 2025-11-23 | 56.2 | 29.8 | 0.992 | 6.9 |
| 2026-05-31 | **60.8** | 33.7 | 0.992 | 11.4 ← recent uptick |

## Per-metric reading

**Max spike duration is the clearest pendulum signal.** Rose from
~10.5 min pre-LC to a peak of 13.2 min in mid-2023, then declined
steadily to 5.8 min by April 2025 (roughly halved from the peak),
with a recent rebound to ~11 min in May 2026. The amplitude
narrowed and then shows some recent perturbation.

**Average stress shows a clean arc too**, smaller amplitude:
- Pre-LC baseline: 32.6
- Peak 2022–23: 35–36
- Trough 2024–25: 29–30
- Recent rebound: 33.7

A ~6-point swing on a 0–100 scale, with a smooth turnaround in mid-
2024, not a cliff.

**RHR is mostly stable** (54–58 bpm range) with a notable **recent
rise to 60.8 bpm** in May 2026. This is the metric most likely to
catch a new perturbation; worth watching.

**Sleep efficiency is essentially flat** (98.7%–99.5% throughout).
Confirms H03's null finding: sleep efficiency isn't where the
stabilisation signal lives. The body's sleep continued to work
through the whole arc.

## What this confirms about the framing

The user's framing of "the pendulum stops swinging as much" is
**visible directly in the data**, on at least the two strongest
metrics (max-spike duration and avg stress). The transition is
**not a cliff** — it's a smooth turnaround over 2023–2024 followed
by a low-amplitude period and a recent perturbation in 2025–26.

The narrative-cliff framing ("recovery cliff" / "the kind of crash
changed in 2024") was an analytical convenience driven by where we
cut the train/validate split. The actual physiology shifted
gradually across ~18 months, peaking in mid-2023 and bottoming in
early-to-mid 2025. **"Stabilisation transition" or "the pendulum
settling" is more accurate.**

## The recent uptick

May 2026 anchors show stress baseline back to 33.7, max-spike back
to 11.4, RHR at 60.8 (highest in the whole window). Not a return to
peak crisis values, but a meaningful upward perturbation. Whatever
this is, it's recent.

The script doesn't speculate about why. Worth flagging to the user
for their own awareness.

## Methodology notes

- 90-day trimmed mean (drop top/bottom 10%) — robust to outlier
  days like a single 24-h work crisis or a stomach bug.
- Anchored every 7 days — gives a smooth curve without bloating
  the file.
- Window starts 90 days into the Garmin record (2021-11-14) so the
  first anchor has a full window.
- All four metrics use the same windowing for direct comparison.
- Pre-LC data is included as the healthy reference — these are the
  same person on the same watch, so the comparison is meaningful.

## What this enables

This is the empirical foundation for the **stabilisation-arc card**
deferred in registry §4. Concrete card concepts now backed by data:

- "Your stress baseline has come down from ~35 (mid-2023) to ~30
  (2025). Recent uptick to 34."
- "Your typical intense-stress moment was 13 minutes in 2023; now
  it's around 11. You've had quieter years in between."
- "Your resting heart rate is up about 5 bpm from last year —
  worth knowing."

These are descriptive, retrospective, multi-axis. Not predictive.
Aligned with the pacing-doc's "presenting conclusions, not making
decisions."

## What this does NOT do

- It does not predict crashes. Crash precursors are a different
  question (H## thread).
- It does not assign causation. We see that stress and spike
  duration came down; we do not know whether that was due to
  pacing skill, external pressures fading, naproxen, time, or some
  combination.
- It does not address whether the recent uptick will continue.
  The dataset can describe; it cannot forecast.

---

*Trajectories computed 2026-06-05. Re-runnable; will lengthen
naturally as new Garmin data is added.*
