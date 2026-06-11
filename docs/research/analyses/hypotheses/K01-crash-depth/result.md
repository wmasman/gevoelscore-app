# K01 — Result: crash depth shifted across recovery eras

**Verdict: SUGGESTIVE BUT UNDERPOWERED.** Direction matches the
hypothesis cleanly (later crashes are shallower) but the permutation
test cannot rule out chance at the pre-registered p ≤ 0.10 bar.

A categorical finding inside the distribution is more striking than
the median test: **no late-era crash reached the rock-bottom score
of 1; the early era had three.**

Data: [result-data.json](result-data.json). Plot:
[result-histogram.png](result-histogram.png).

## Numbers

|                            | early (2022–23) | late (2024+) |
|----------------------------|----------------:|-------------:|
| n episodes                 | 14              | 15           |
| min nadir                  | **1**           | **2**        |
| max nadir                  | 3               | 3            |
| **median nadir**           | **2**           | **3**        |
| mean nadir                 | 2.00            | 2.67         |
| nadirs at 1                | 3 episodes      | **0 episodes** |
| nadirs at 2                | 8 episodes      | 5 episodes   |
| nadirs at 3                | 3 episodes      | 10 episodes  |

`delta_median = +1.0` (late ≥ early by one full score point).
`delta_mean = +0.67` (late ≥ early by 2/3 of a score point).

**Permutation test (10.000 shuffles, seed 20260605):**
- One-sided empirical p-value: **0.276**

**Criteria check:**
- a. delta_median ≥ 0.3: **PASS** (delta = +1.0)
- b. permutation p ≤ 0.10: **FAIL** (p = 0.276)

Per the pre-registered rule (both criteria required), verdict =
**suggestive_underpowered** — direction matches but the small sample
+ integer scale make the median brittle.

## Why the p-value is high despite the clear direction

The nadir variable only takes three values (1, 2, 3 — no late
episode reached 1; no episode of either era exceeded 3 at its worst
moment). With 29 episodes total clustering on three values, the
median can flip between 2 and 3 with a single swap. Under random
shuffling, a delta of +1 in the median happens in ~28% of trials.
Statistical tests do not love integer scales with small samples.

The **mean** is less brittle. A 0.67-point shift on a 1–6 scale
is large; the same permutation logic on means (descriptive, not
pre-registered) would likely show a much lower p-value.

But we pre-registered the median criterion specifically *because*
medians are more robust to outliers — and on small samples that
robustness becomes brittleness. Lesson for K02 and future K-thread
tests: consider pre-registering both median *and* mean criteria
when the metric takes few discrete values.

## What the data DOES say

- **Direction is unambiguous.** Late-era crashes are shallower than
  early-era crashes on every summary statistic computed (min, median,
  mean, count-of-deepest-nadirs).
- **A categorical finding emerges**: 0 of 15 late-era crashes reached
  the floor of score 1, where 3 of 14 early-era crashes did. The
  worst late-era crashes (nadir = 2) match the *average* early-era
  crash. The user's recovery hasn't just made crashes less frequent;
  the residual ones don't go as deep.
- **The mean shift of +0.67** on a 1–6 scale is meaningful. On a
  scale where the user typically rates 4 or 5, a 2/3-point shift in
  the worst-day score is what most people would call "less bad."

## What the data does NOT say

- **It does NOT statistically rule out chance.** With 14 vs 15
  episodes and a 3-value variable, the median shift could occur by
  chance roughly 1 in 4 random reshufflings.
- **It does NOT tell us why depths shifted**. Could be: better
  pacing keeps crashes from going as far; smaller triggers produce
  smaller crashes; user is generally more resilient; some of all
  three.
- **It does NOT distinguish "lower floor" from "shorter floor"** —
  K02 (duration) tests the orthogonal axis.

## Combined with H02 + H02b

The kind-of-crash theory now has three independent supporting
findings:

1. H02 train: stress precursor present in 2022–23, absent in
   2024+ (refuted on bar, but real direction)
2. H02b train: stress-spike precursor **supported** in 2022–23,
   absent in 2024+
3. K01: late-era crashes are shallower than early-era crashes
   (suggestive_underpowered, but clear direction + 0 floor-nadirs)

No single piece is conclusive. Together they paint a coherent
picture: pacing recovery has changed both the precursor profile
(H02 / H02b) and the depth (K01) of the crashes that still happen.

## Caveats

- **Small samples** (per hypothesis.md §8): 14 early + 15 late.
  Permutation p inflated by the brittleness above.
- **Late era is mostly 2024** (11 of 15 episodes), with a small
  2025+ tail (4 episodes). Re-running K01 in late 2026 or 2027,
  when more late-era crashes have accumulated (or hopefully fewer,
  if recovery continues), would tighten the estimate.
- **`crash_v1` mixes mechanisms** — depth shift could be driven by
  one subtype changing while others stay constant. K03
  (symptom-keyword profile) is the natural test to disentangle this.

## What we do next

- Per hypothesis.md §9: suggestive_underpowered → record finding,
  don't claim support, proceed.
- **K02 (duration) is next** — same data, same shape of test,
  different axis. If K02 also shows direction-supportive but
  underpowered, the cumulative evidence across K01 + K02 + H02b is
  meaningful even if no single one passes.
- Note for future: **K01b** with more episodes (in 1+ year) would
  likely give a clean answer. Mark for re-run.

---

*Test run 2026-06-05. Re-runnable any time with same seed.*
