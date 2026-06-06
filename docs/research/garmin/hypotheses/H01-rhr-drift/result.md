# H01 — Result: RHR drift before crashes

**Verdict: REFUTED.** In both train and validate windows, on all three
pre-registered criteria. No card.md is written (per the per-hypothesis
flow rule: `card.md` only if supported).

Data: [result-data.json](result-data.json). Plots: [result-train.png](result-train.png),
[result-validate.png](result-validate.png). Test: [test.py](test.py).
Pre-registration: [hypothesis.md](hypothesis.md).

## Numbers

|                                                 | train      | validate    |
|-------------------------------------------------|-----------:|------------:|
| crash episodes in window                        | 14         | 15          |
| excluded for missing RHR data                   | 0          | 0           |
| excluded for lead-up overlap with another crash | 2          | 2           |
| **clean crash episodes**                        | **12**     | **13**      |
| null sample size                                | 200        | 200         |
| % of crash lead-ups with delta_rhr ≥ +3 bpm     | 8.3%       | **0.0%**    |
| % of null windows with delta_rhr ≥ +3 bpm       | 9.5%       | 9.5%        |
| discrimination (crash − null, pp)               | −1.2       | **−9.5**    |
| median delta_rhr across crashes (bpm)           | +0.5       | **−1.0**    |
| lower quartile delta_rhr across crashes (bpm)   | −0.2       | −1.4        |
| criterion a (≥60% at +3 bpm)                    | FAIL       | FAIL        |
| criterion b (crash rate ≥ null + 15 pp)         | FAIL       | FAIL        |
| criterion c (median ≥ +2 bpm, lower-q ≥ 0)      | FAIL       | FAIL        |

All three criteria fail in both windows. The test is decisive — this is
not an underpowered or borderline result. With 25 clean episodes and
200 null windows, we'd see a real signal if it existed.

## The directionality finding

The validate window's mean RHR was **lower in the 7 days before crashes
than baseline**, by about 1 bpm. The exact opposite of Workwell's
"RHR + 15" prediction. This is not random — the lower-quartile is
−1.4 bpm, meaning at least 75% of validate crashes had below-baseline
or near-baseline lead-up RHR, not elevated.

This is more interesting than "no signal." It suggests something
specific about how this user's residual crashes happen. See
"Interpretations" below.

## What this rules out

- The Workwell pacing rule ("RHR + 15 bpm above baseline") **does not
  predict crashes for this user** in this dataset, on the 7-day lead-up
  window.
- A wider lead-up window (e.g. 3-day or 14-day) would constitute a
  *different* hypothesis, not a re-test of H01. If we want to ask that,
  it becomes H01b with its own pre-registration.

## What this does *not* rule out

- That RHR rises during or after a crash (rather than before).
- That a sub-population of crashes — e.g. acute infection-triggered
  flares — does show RHR elevation, but is washed out by the broader
  crash_v1 mix (the pacing-doc's "endogenous immune flare" hypothesis
  predicts exactly this kind of subset).
- That HRV (which the GDPR dump doesn't expose at the per-day level
  without decoding the FIT files) would have caught what RHR missed.

## Interpretations to weigh

Listed in rough order of plausibility given what we know:

1. **The user is genuinely well-paced.** If physical exertion is being
   managed inside the envelope (the gevoelsscore-dashboard-findings
   already suggested this — "the cost lands as a ~1-point sag 48–72h
   later, not a crash"), then crashes that *do* happen aren't
   precipitated by HR-visible load. The residual triggers would be
   cognitive, emotional, sleep-related, hormonal, viral, or mast-cell
   — none of which move RHR much in lead-up. This fits the validate
   window finding cleanly: when pacing improves enough that physical
   exertion stops triggering crashes, the crashes that survive are
   *categorically different* from the ones a Workwell-style rule was
   developed against.

2. **Chronotropic incompetence**, which Workwell themselves flag as
   present in >85% of ME/CFS patients. The user's HR response may be
   blunted enough that even real exertion doesn't elevate RHR
   meaningfully. This is a "no signal because the signal is broken at
   the transducer," not "no signal because the relationship isn't
   there."

3. **`crash_v1` mixes mechanisms.** A score ≤ 3 day could be PEM, could
   be acute illness, could be a migraine, could be a bad mental-health
   day. If only ~30% of these are exertion-PEM, the precursor signal
   from that subset is diluted by 70% noise. `crash_v2` (notes-based
   labels) might separate these.

4. **The lead-up window is wrong.** Some literature describes RHR
   elevation in a tighter 24–48h window or on the day of the crash
   itself, not a 7-day mean. This would be a follow-up H01b.

5. **Regression toward the mean.** The lower-than-baseline finding in
   validate could partly reflect that pre-crash days happen to be
   below-average activity days (the user was already conserving
   energy), pulling RHR slightly lower in the lead-up. Hard to
   distinguish from interpretation 1.

The validate-only direction reversal (positive in train, negative in
validate) also lines up with the recovery cliff: as pacing skill grew,
fewer crashes were precipitated by HR-visible load, so the residual
crashes started having a *different* signature.

## Multi-comparison honesty

H01 is the first of 5 hypotheses we're testing. A refuted first
hypothesis does *not* count against the others — and a positive third
hypothesis (e.g. H03 sleep) does not have its credibility eroded by
H01's failure. Each is independently pre-registered with its own
criterion.

## Implications for H02–H05

- **H02 (sustained stress elevation)** becomes the most interesting
  next test. Stress (Garmin's 0–100 algorithm) captures sympathetic
  load that's *not* pure physical exertion — cognitive, emotional,
  sleep-deprivation effects. If the residual crashes are
  non-physical-exertion in origin (interpretation 1 or 3), stress is a
  plausible lead-indicator where RHR fails.
- **H03 (sleep)** is also strengthened in priority. Sleep dysregulation
  is the other classic ME/CFS precursor and is mechanistically distinct
  from RHR drift.
- **H04 (body battery net-drain)** is now harder to predict. Body
  battery composites RHR (null here) + HRV (unknown) + stress (to be
  tested). It might still fire if HRV or stress carries the signal,
  but RHR's null contribution makes a strong support less likely.
- **H05 (recovery time, descriptive)** is unchanged. It doesn't depend
  on precursor signals.

## Caveats that hypothesis.md §8 told us to acknowledge

- **Chronotropic incompetence**: see interpretation 2. Cannot rule out.
- **Seasonality / training load / acute illness as confounders**: not
  controlled for. None of the analysis decomposed RHR by season.
- **Score scale drift**: the user has confirmed their score is not
  drifting (recovery is real). This concern is largely mooted.
- **Multiple-comparisons**: H01 is refuted, so this doesn't bite. But
  it would have if we'd seen a borderline positive.
- **Reverse causation / shared cause**: moot for a refuted hypothesis,
  but would have been the main caveat had H01 supported.

## What we do next

Per [hypothesis.md §9](hypothesis.md):
- **Refuted** → write this `result.md` (done). Do not re-run with
  tweaked criteria. Proceed to H02 unchanged.
- If interpretation 1 or 3 is correct, H02 (stress) is the natural next
  test — proceed there.

---

*Test run 2026-06-05 against day_entries.csv (1.372 entries) and Garmin
UDS files (1.731 days with RHR). Re-runnable any time with the same
inputs and the same seed (`20260605`).*
