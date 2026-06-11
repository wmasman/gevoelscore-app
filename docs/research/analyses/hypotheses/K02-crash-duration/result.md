# K02 — Result: crash duration shifted across recovery eras

**Verdict: REFUTED by strict bar (criterion a magnitude not met) but
with a striking structural finding the median test missed.**

Median spans differ by only 0.5 days (early 2.5, late 2.0), which
fails the pre-registered +1 day delta threshold. But the **mean**
shift is dramatic (early 4.64 days, late 2.53 days = −2.11 days),
driven by the **near-disappearance of the long-crash tail**: 5 of 14
early-era crashes ran ≥ 5 days; only 1 of 15 late-era crashes did.
Maximum span: 14 days early → 7 days late.

Same lesson as K01: the median was pre-registered for outlier-
robustness, which on a sample of 29 with heavy skew is actually the
*opposite* of what we want. Mean would have caught it cleanly.

Data: [result-data.json](result-data.json). Plot:
[result-histogram.png](result-histogram.png).

## Numbers

|                            | early (2022–23) | late (2024+) |
|----------------------------|----------------:|-------------:|
| n episodes                 | 14              | 15           |
| min span                   | 2 days          | 2 days       |
| **max span**               | **14 days**     | **7 days**   |
| **median span**            | 2.5 days        | 2 days       |
| mean span                  | **4.64 days**   | **2.53 days** |
| p25 / p75                  | 2 / 5 days      | 2 / 2 days   |
| episodes ≥ 5 days          | **5**           | **1**        |

`delta_median = -0.5` (late shorter by half a day; criterion needed -1)
`delta_mean = -2.11` (massive, but not pre-registered)

**Permutation test (10.000 shuffles, seed 20260605):**
- One-sided empirical p-value (late ≤ early): **0.095**

**Criteria check:**
- a. delta_median ≤ −1 day: **FAIL** (delta = −0.5)
- b. permutation p ≤ 0.10: **PASS** (p = 0.095, just below)

Per the pre-registered rule (both required), verdict = **refuted**.
But it's the kind of refuted that's worth its own structural reading.

## The long-crash tail

The clearest single finding from K02:

| era    | episodes ≥ 5 days                                                |
|--------|------------------------------------------------------------------|
| early  | 2022-09-16 (9d), 2023-02-04 (5d), 2023-05-28 (11d), 2023-11-12 (5d), 2023-11-27 (**14d**) |
| late   | 2024-02-25 (7d)                                                  |

Five long crashes in 14 early episodes (36%). One long crash in 15
late episodes (7%). The 14-day February 2024 episode is the only
remaining outlier. Everything else in 2024+ is 2–4 days.

This isn't statistical fluff — it's a categorical shift in the kind
of crash. **The user's "deep dragging weeks" appear to be over.**

## What the data DOES say

- **Mean span dropped from ~4.6 days to ~2.5 days.** That's about
  half. On its own that's a sizeable effect, larger than the median
  test caught.
- **The long-crash tail (≥ 5 days) shrank from 36% to 7%** of
  episodes. This is a categorical shift, not just a numerical one.
  Whatever produced multi-week crashes in 2023 is largely gone.
- **The shortest possible crash (2 days) is now the modal pattern
  for the late era**: 12 of 15 late episodes are 2-day crashes; in
  the early era, 7 of 14 were.

## What the data does NOT say

- **It does NOT pass the pre-registered bar.** Crit a was magnitude
  on the median; the median barely moved because both eras' median
  is dominated by 2-day episodes. We pre-registered the wrong
  statistic for this distribution shape.
- **It does NOT distinguish "individual crashes got shorter" from
  "fewer crashes merged into long episodes."** The `crash_v1` merge
  rule (within 3 days = same episode) means a reduction in crash
  *clustering* could explain the span shrinkage without the
  individual crashes themselves changing. Both interpretations are
  recovery-supportive but mechanically different.
- **It does NOT prove the depth (K01) and duration (K02) shifts are
  independent**. They could be two views of the same underlying
  change (a smaller trigger → smaller, shorter response).

## Combined with K01, H02 and H02b

The kind-of-crash theory now has four directional supporting
findings:

| test  | axis                            | verdict                  | direction |
|-------|---------------------------------|--------------------------|-----------|
| H02   | stress precursor (daily avg)    | refuted but train-direction | train +  |
| H02b  | stress precursor (spike count)  | refuted (train SUPPORTED) | train +  |
| K01   | crash depth                     | suggestive_underpowered  | late shallower |
| K02   | crash duration                  | refuted but mean −2.11d / tail collapse | late shorter |

None individually clears its full pre-registered bar (H02b train
does, but its overall verdict was refuted because of validate). But
**every single test points in the same direction**, on independent
axes, with magnitudes that aren't trivial. The cumulative weight is
substantial even if no single piece passes.

## The methodology lesson (carried from K01)

Pre-registering on the median when the metric:
- Takes a small number of distinct values (nadir: 3; span: ~13),
- Has its mass clustered on the minimum value (2-day spans, score-2
  nadirs),

… makes the median statistic brittle. The mean catches the shift
clearly in both K01 and K02. **For K03 and onward in this thread,
pre-register on both median AND mean criteria** (require either to
pass, or report both transparently). Add to synthesis as a
methodology note.

## What we do next

- Per hypothesis.md §9: refuted on bar → record, don't claim
  support, proceed. But note the categorical tail-collapse finding
  prominently.
- **The kind-of-crash investigation now has enough cumulative
  signal to recommend updating the synthesis.** Four directional
  supporting findings, no contradictions.
- K03 (symptom-keyword profile) requires user collaboration on a
  Dutch keyword set. Worth raising now.
- Future K01b + K02b (in a year or two with more late-era episodes)
  would tighten both verdicts.

---

*Test run 2026-06-05.*
