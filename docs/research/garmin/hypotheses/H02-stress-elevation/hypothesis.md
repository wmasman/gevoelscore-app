# H02 — Sustained stress elevation before crashes

**Pre-registration written 2026-06-05, before any data was inspected
for this test.** Locked. Any subsequent change creates an H02b.

## 1. Claim

In the 3 days before a `crash_v1` episode (per [registry §2](../registry.md)),
this user's daily mean `averageStressLevel` (Garmin's 0–100 algorithm,
from the UDS daily aggregates) is consistently elevated above their own
rolling 90-day baseline. The elevation is *discriminative* — it appears
more often before crash episodes than in randomly-sampled non-crash
3-day windows from the same period.

## 2. Why we think this

- Garmin's stress score is derived from HRV-via-HR (the same machinery
  underlying the pacing literature's autonomic-overload model). It
  captures **sympathetic activation that is not purely physical
  exertion** — cognitive load, emotional stress, sleep deprivation,
  illness onset.
- H01 refuted the pure-HR-elevation precursor. The plausibility-1
  interpretation in [H01/result.md](../H01-rhr-drift/result.md) is that
  the user's residual crashes aren't physical-exertion-triggered;
  whatever's left is cognitive / emotional / sleep / mast-cell / viral.
  H02 directly tests whether Garmin's stress signal captures that
  residual.
- We've already verified per-minute stress samples exist at
  ~1.400/day resolution across the full 1.733-day window
  (see [README §what's inside one full-day monitoring_b](../../README.md)),
  but for v1 we use the **per-day aggregate** in
  `UDSFile_*.json → allDayStress.aggregatorList[type=TOTAL]
  .averageStressLevel`, not the raw FIT samples. This keeps the test
  comparable to H01 in shape, runs in seconds instead of hours, and
  defers FIT-level stress parsing to H02b if H02 is borderline.

## 3. Data sources

- **Crash labels**: identical to H01 — `crash_v1` per registry §2.
- **Daily stress**: `averageStressLevel` from
  `DI_CONNECT/DI-Connect-Aggregator/UDSFile_*.json`, field
  `allDayStress.aggregatorList[type=TOTAL].averageStressLevel`. Range
  0–100.
- **Secondary metric (reported but not used for verdict)**:
  `highDuration` from the same aggregator — seconds per day in Garmin's
  HIGH stress band (>75). Reported in result.md as a robustness check
  but not part of the pre-registered criteria.
- **Analysis window**: 2022-09-03 → 2026-06-05.
- **Train / validate split**: train 2022-09-03 → 2023-12-31 (14
  episodes); validate 2024-01-01 → 2026-06-05 (15 episodes). Same as
  H01.

## 4. Measurement protocol

For each crash episode dated `D`:

1. **Lead-up window** = `[D − 3, D − 1]` (3 days, exclusive of D).
   *Tighter than H01's 7-day window because stress is more reactive
   than RHR — sympathetic state changes day-by-day, not week-by-week.*
2. **Baseline window** = `[D − 93, D − 4]` (90 days ending 3 days
   before the episode, so the baseline doesn't include the lead-up).
3. **Baseline stress** = trimmed mean (drop top and bottom 10%) of
   `averageStressLevel` within the baseline window.
4. **Lead-up stress** = simple mean of `averageStressLevel` within the
   lead-up window.
5. **`delta_stress` for this episode** = lead-up minus baseline
   (units: stress points, 0–100 scale).

For discrimination:

6. **Null sample** = 200 randomly-selected 3-day windows from the same
   analysis window, each with the same baseline construction, each
   disjoint from any crash episode's lead-up window. Seed `20260605`.

## 5. Pre-registered falsification criterion

The hypothesis is **supported** if and only if **all three** hold in
**both** the train window and the validate window independently:

a. **Frequency**: at least **60%** of crash episodes have
   `delta_stress ≥ 3` stress points.

b. **Discrimination**: the crash-episode frequency from (a) is at least
   **15 percentage points higher** than the null-sample frequency of
   windows with `delta_stress ≥ 3`.

c. **Magnitude**: the median `delta_stress` across crash episodes is at
   least **+2 stress points**, and the lower quartile is at least
   **0 points** (most lead-ups elevated, not just a few extreme).

Any one of (a), (b), (c) failing in either window → **refuted**.

If we have fewer than 10 clean crash episodes per window after
exclusions, the result is **inconclusive**.

The +3 / +2 thresholds reflect that on Garmin's 0–100 scale, a 3-point
shift on a baseline near ~30 is a ~10% relative elevation — large
enough to be perceptible but not so large that only severe events
would register.

## 6. Exclusion rules

- **Episode requires all 3 valid stress days in lead-up** (3 of 3, not
  2 of 3 — the window is smaller so missing days hurt more).
- **Episode requires ≥30 valid days out of 90** in baseline.
- **Episodes whose lead-up overlaps another crash episode's days** are
  excluded from the primary analysis, reported separately.
- Baseline may use pre-2022-09 UDS data (Garmin coverage starts
  2021-08, gevoelscore-window restriction is only on the labelled
  side).

## 7. Expected effect size if the hypothesis is true

Rough sanity checks for result.md:

- 70–80% of crash episodes show `delta_stress ≥ 3`
- Null sample rate: ~30–40% (random 3-day windows naturally fluctuate)
- Median `delta_stress` across crashes: roughly +5 to +10 points
- If we see crash rate of 95% and null rate of 90%, the baseline is
  probably broken (probably contaminated by lead-up days) — flag it.

## 8. Caveats `result.md` must explicitly acknowledge

- **Garmin's stress algorithm is opaque** and changes between firmware
  versions. The user's FR245 firmware spans 7.x → 10.4 across the
  analysis window; algorithm updates may have shifted the baseline. We
  do not control for this.
- **Stress samples require the watch be worn** with reasonable contact.
  Off-wrist periods (yard work, charging, sweaty workouts) are reported
  by Garmin as `stressOffWristCount` — we don't filter on this in v1,
  but result.md should report mean off-wrist count for crash vs null
  windows as a sanity check.
- **Shared-cause confound**: if a developing infection elevates both
  stress (via inflammation) and crash risk (sickness behaviour), the
  signal looks like "stress predicts crash" but actually reflects a
  common upstream cause. The analysis cannot distinguish these.
- **`crash_v1` mixes mechanisms** — same caveat as H01. Stress may
  predict the cognitive/emotional subset cleanly while being null on
  others, and the overall verdict could be diluted to "weakly
  supported" or "refuted" by averaging.
- **Multiple-comparisons**: H02 is the second of five hypotheses. The
  held-out validation is the primary protection.

## 9. What we do with each outcome

- **Supported in both windows** → write `card.md` with 2–3 candidate
  card-text variants using real numbers from this user's data and
  (where present) real quoted phrases from the user's notes on those
  crash days. The card here would say something like "the three days
  before this had higher stress than normal." (Real copy in `card.md`,
  not here.) Proceed to H03.
- **Refuted** → write `result.md` documenting exactly why. Do not
  re-run. If the failure shape is interesting (e.g. the secondary
  `highDuration` metric showed signal where average didn't), record
  that as a candidate for H02b. Proceed to H03 unchanged.
- **Inconclusive (too few episodes)** → write `result.md` and consider
  bringing `crash_v2` (notes-based labels) forward.
- **Partial** (e.g. train supported, validate refuted, or vice versa)
  → write `result.md` describing the time-asymmetry. This is the most
  interesting failure mode and would inform whether the cliff in the
  recovery-trajectory pattern matters. Do not call it supported.

---

*Pre-registration locked 2026-06-05. Next: `fetch_day_entries.mjs`
(near-duplicate of H01's) then `test.py`.*
