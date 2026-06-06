# H02 — Result: sustained stress elevation before crashes

**Verdict: REFUTED, but with a meaningful train/validate asymmetry.**

The overall verdict is refuted because criterion (a) fails in both
windows and criteria (b)+(c) fail in validate. But the train window
shows a real directional signal that *almost* passes — 11 of 14 train
episodes had elevated lead-up stress, median +2.7 points, discrimination
+25.9 pp above null. Validate has no such pattern (median −0.2, slightly
inverted).

This is the **partial / time-asymmetric** failure mode that
[hypothesis.md §9](hypothesis.md) flagged as the most interesting. It
matches the recovery-cliff structure precisely: pre-2024 crashes show
the precursor; post-2024 crashes don't.

No `card.md` is written (per the rule: only on supported). But the
train pattern earns a place in deferred follow-up.

Data: [result-data.json](result-data.json). Plots:
[result-train.png](result-train.png), [result-validate.png](result-validate.png).

## Primary numbers — avg daily stress (0–100 scale)

|                                            | train  | validate |
|--------------------------------------------|-------:|---------:|
| crash episodes in window                   | 14     | 15       |
| excluded for missing data                  | 0      | 0        |
| excluded for lead-up overlap               | 0      | 0        |
| **clean crash episodes**                   | **14** | **15**   |
| null sample size                           | 200    | 200      |
| % of crash lead-ups with delta ≥ +3 stress | 42.9%  | 13.3%    |
| % of null windows with delta ≥ +3 stress   | 17.0%  | 17.0%    |
| **discrimination (crash − null, pp)**      | **+25.9** | **−3.7** |
| median delta_stress                        | +2.66  | −0.18    |
| lower quartile delta_stress                | +0.71  | −3.00    |
| criterion a (≥60% at +3)                   | FAIL   | FAIL     |
| criterion b (crash ≥ null + 15 pp)         | **PASS** | FAIL   |
| criterion c (median ≥ +2, lower-q ≥ 0)     | **PASS** | FAIL   |

Train passes 2 of 3 criteria; validate passes 0 of 3. Pre-registration
requires all 3 in both windows → refuted.

But the train pattern is real, not noise: discrimination of +25.9 pp
against a 200-window null is well outside chance.

## Direction-of-signal breakdown (per-episode)

Out of clean episodes, how many had positive delta_stress (any
elevation):

| window | episodes with delta > 0 | % |
|---|---:|---:|
| train | 11 of 14 | **79%** |
| validate | 6 of 15 | **40%** |

A coin-flip baseline would be ~50%. Train is well above; validate is
well below. The directionality finding holds independent of the strict
+3 threshold.

## Secondary metric — high_duration (seconds/day in HIGH stress band)

Reported descriptively only (not part of verdict):

|                        | train | validate | null   |
|------------------------|------:|---------:|-------:|
| n                      | 14    | 15       | 200    |
| median delta (sec/day) | **+763** | −180   | +346   |
| mean delta (sec/day)   | **+1.196** | +102 | +563   |
| p25 delta (sec/day)    | −169  | −1.399   | −837   |
| p75 delta (sec/day)    | **+2.928** | +649 | +1.768 |

In train, the median lead-up day had **~13 minutes more high-band stress
than baseline**; the 75th-percentile episode had ~49 minutes more.
That's a substantial sustained sympathetic elevation. In validate it's
roughly zero / slightly below baseline.

The secondary metric tells the same story as the primary but more
loudly — the early-recovery crashes had **sustained spikes** of high
stress in the 3 days before, not just slightly elevated averages.

## What this rules out

- Stress (as the daily avg) **does not predict** the residual 2024+
  crashes for this user. Criterion-(b) fails by −3.7 pp in validate;
  median direction is slightly inverted.

## What this confirms

- Pre-2024 crashes **did show** a stress precursor pattern that's
  statistically distinguishable from random non-crash windows. It
  doesn't pass our strict pre-registered bar — but the bar was set
  before we knew the recovery cliff existed.

## Interpretation — the recovery cliff is showing through

The asymmetry is the finding. Two compatible reads:

1. **Mechanism shift.** Pre-recovery crashes were partly precipitated
   by sympathetic-overload accumulation that Garmin's stress score
   could see. As pacing got better, those crashes stopped happening.
   The 2024+ residual crashes are triggered by something Garmin's
   stress score can't see — sleep dysregulation, mast-cell, viral
   reactivation, hormonal, purely cognitive. The signal didn't fade;
   the kind of crash changed.
2. **Threshold compression.** As recovery improved, the user's
   physiological response to stressors got smaller in absolute terms.
   Pre-recovery, a stressful 3-day stretch might push avg_stress from
   30 → 38 (visible). Post-recovery, the same psychological stretch
   might only push it from 25 → 28 (invisible at our threshold). If
   we'd set crit_a at +1 instead of +3, validate might look different
   — but that would be moving the goalposts post-hoc and we don't.

Both readings have implications for H03 (sleep) and H04 (body battery).

## What this does *not* rule out

- That stress lights up before a specific *sub-type* of crash (e.g. the
  ones with a tagged emotional / cognitive precipitant in the notes).
  `crash_v2` (notes-based labels) could separate these.
- That a different lead-up window — e.g. day-of-crash rather than
  3-day mean — would show signal. That would be H02b.
- That **raw FIT stress samples** (per-minute, ~1.400/day) carry more
  signal than the daily aggregate. The peak-spike count is what
  hypothesis.md originally sketched (samples > 60). The aggregate
  averages spikes with quiet periods. If the underlying pattern is
  "20 minutes of intense stress per day" — invisible to the average,
  visible to the spike count — we'd miss it here. That's H02c if we
  want to dig.

## Honest acknowledgements (from hypothesis.md §8)

- **Off-wrist contamination**: train episode 2023-11-27 had a
  lead-up_mean_off_wrist of 229. That's high enough that the stress
  averages for that episode may be unreliable. Without filtering, this
  reduces precision but doesn't change the direction of the train
  finding (which doesn't depend on any one episode). validate has its
  own high-off-wrist episodes (2024-06-25 at 81), with similar caveat.
- **Garmin firmware drift** from 7.x → 10.4 across the window is
  unaccounted for. Stress algorithm changes plausibly contribute to the
  cliff but cannot be isolated from the recovery signal.
- **Shared-cause**: a developing infection elevates both stress and
  crash risk. The train signal could be partly "infection precursor"
  rather than "stress precursor" — and the validate null could mean
  the user is having fewer infection-triggered crashes now. We can't
  distinguish these.
- **`crash_v1` mixes mechanisms**: confirmed again. The train pattern
  is consistent with stress-precipitated crashes being a *subset* of
  the train episodes; the validate null is consistent with that subset
  no longer existing.

## Multi-comparison honesty

H02 is the 2nd of 5. Refuted on the pre-registered criterion → no
inflation concern for downstream tests. The train partial result is
*not* called "supported" — moving the bar to fit would corrode the
whole exercise.

## Implications for H03–H05

- **H03 (sleep efficiency)** is now the highest-priority remaining
  test. If interpretation 1 is correct (mechanism shift), sleep is the
  most likely candidate residual precursor. If sleep is also
  train-yes / validate-no, the mechanism-shift story is strongly
  supported. If sleep is supported in *both* windows, we've found the
  residual precursor — and that's a real card.
- **H04 (body battery)**: now harder to predict. Body battery composites
  RHR (null in H01) + HRV (untested) + stress (H02-pattern). H04 may
  inherit the train/validate asymmetry from H02 or get washed out
  entirely.
- **H05 (recovery time)**: unchanged. May want to add a secondary
  output: "did recovery time correlate with lead-up stress in train
  but not validate?" — another lens on the mechanism shift.
- **`crash_v2`**: getting more interesting. If we could split the
  29 episodes by mechanism (notes-derived: physical-load / cognitive /
  sleep / illness / unclassified), each sub-type might have its own
  supported precursor pattern, even if the union doesn't.

## What we do next

- Per [hypothesis.md §9](hypothesis.md): write this `result.md` (done),
  proceed to H03 unchanged, do not re-run with tweaked criteria.
- Add an explicit follow-up note in registry §4 for **H02b /
  per-minute FIT stress samples** (peak-spike count) as a future test.

---

*Test run 2026-06-05. Re-runnable with the same inputs + seed
(`20260605`).*
