# H03 — Sleep efficiency drop before crashes

**Pre-registration written 2026-06-05, before any data was inspected
for this test.** Locked. Any subsequent change creates an H03b.

## 1. Claim

In the 7 nights before a `crash_v1` episode (per [registry §2](../registry.md)),
this user's mean nightly **sleep efficiency** drops below their own
rolling 90-day baseline. The drop is *discriminative* — appears more
often before crash episodes than in randomly-sampled non-crash 7-night
windows.

Sleep efficiency = `(deepSleepSeconds + lightSleepSeconds + remSleepSeconds)`
divided by
`(deepSleepSeconds + lightSleepSeconds + remSleepSeconds + awakeSleepSeconds + unmeasurableSeconds)`,
expressed as a fraction 0.0–1.0.

## 2. Why we think this

- Sleep dysregulation is one of the most consistently cited PEM
  precursors in the ME/CFS / Long COVID literature
  ([pais-pem-literature-review](../../../pais-pem-literature-review.md);
  [pacing-and-crash-mitigation](../../../pacing-and-crash-mitigation.md) §4).
- H01 (RHR) was refuted across both windows. H02 (daily avg stress)
  was refuted overall but showed a clear train-window signal that
  disappeared in validate — consistent with the recovery cliff
  changing the *kind* of crash. If H03 is *also* train-yes / validate-no,
  the mechanism-shift story gets strongly supported. If H03 is
  **supported in both windows**, we've found the residual precursor and
  it earns a `card.md`.
- Sleep is mechanistically distinct from sympathetic-arousal load
  (stress) and from chronic autonomic state (RHR), so a positive H03
  alongside null H01/H02 would be biologically coherent: pacing has
  kept exertion-load and sympathetic-arousal in check, but sleep
  disruption from any source (cognitive load, hormonal, anxiety,
  illness onset) still slips through and triggers crashes.
- We have ~1.700 nights of sleep data with full coverage across the
  analysis window.

## 3. Data sources

- **Crash labels**: identical to H01/H02 — `crash_v1` per registry §2.
- **Nightly sleep**: `DI_CONNECT/DI-Connect-Wellness/*_sleepData.json`,
  fields per night: `calendarDate`, `deepSleepSeconds`,
  `lightSleepSeconds`, `remSleepSeconds`, `awakeSleepSeconds`,
  `unmeasurableSeconds`, `sleepWindowConfirmationType`.
- **Analysis window**: 2022-09-03 → 2026-06-05.
- **Train / validate split**: train 2022-09-03 → 2023-12-31 (14
  episodes); validate 2024-01-01 → 2026-06-05 (15 episodes). Same as
  H01/H02.

## 4. Measurement protocol

For each crash episode dated `D`:

1. **Lead-up window** = `[D − 7, D − 1]` (7 nights before, exclusive of
   D). Same as H01 for cross-hypothesis comparability. The
   sleep-efficiency-of-night-N is indexed by N's `calendarDate`, which
   per Garmin convention is the morning the user woke up.
2. **Baseline window** = `[D − 97, D − 8]` (90 nights ending 7 days
   before, so baseline doesn't include lead-up).
3. **Baseline efficiency** = trimmed mean (drop top + bottom 10%) of
   nightly efficiency within the baseline window.
4. **Lead-up efficiency** = simple mean of nightly efficiency within
   the lead-up window.
5. **`delta_eff` for this episode** = lead-up minus baseline (units:
   fraction, e.g. −0.04 = "4 percentage points lower than baseline").

For discrimination:

6. **Null sample** = 200 randomly-selected 7-night windows from the
   same analysis window, disjoint from any crash episode's lead-up.
   Seed `20260605`.

## 5. Pre-registered falsification criterion

The hypothesis is **supported** if and only if **all three** hold in
**both** train and validate independently:

a. **Frequency**: at least **60%** of crash episodes have
   `delta_eff ≤ −0.05` (lead-up efficiency at least 5 percentage points
   below baseline).

b. **Discrimination**: the crash-episode frequency from (a) is at
   least **15 percentage points higher** than the null-sample frequency
   of windows with `delta_eff ≤ −0.05`.

c. **Magnitude**: the median `delta_eff` across crash episodes is at
   most **−0.03** (3 pp drop), and the upper quartile is at most
   **0.00** (most lead-ups showed some drop, not just a few extreme).

Any one of (a), (b), (c) failing in either window → **refuted**.

If we have fewer than 10 clean crash episodes per window after
exclusions, the result is **inconclusive**.

## 6. Exclusion rules

- **Episode requires ≥ 5 valid sleep nights out of 7** in lead-up
  (slightly more permissive than H02's all-or-nothing because sleep
  data has occasional unconfirmed nights even when the watch is on).
- **Episode requires ≥ 30 valid nights out of 90** in baseline.
- **Nights with `sleepWindowConfirmationType` of `OFF_WRIST`,
  `UNCONFIRMED`, or `NOT_CONFIRMED` are excluded** from both lead-up
  and baseline counts. Only `ENHANCED_CONFIRMED_FINAL` and similar
  positively-confirmed types are used.
- **Nights where TST + awake + unmeasurable < 4 hours** are excluded as
  unreliable (likely a nap or off-wrist period misclassified as sleep).
- **Episodes whose lead-up overlaps another crash episode's days** are
  excluded from primary analysis, reported separately.
- Baseline may use pre-2022-09 sleep data (Garmin coverage starts
  2021-08).

## 7. Expected effect size if the hypothesis is true

Rough sanity checks for result.md:

- 70–80% of crash episodes show `delta_eff ≤ −0.05`
- Null sample rate: 10–20%
- Median `delta_eff` across crashes: roughly −0.05 to −0.10
- Healthy baseline efficiency is typically 0.85–0.95; a 5 pp drop is
  meaningful sleep degradation (~25 extra waking minutes per 8-h night)

## 8. Caveats `result.md` must explicitly acknowledge

- **Sleep efficiency is a single number** that smooths over many
  pathophysiologies (fragmentation, latency, deep-sleep loss, REM
  loss). If the precursor signal lives in deep-sleep loss specifically
  but total efficiency is preserved, we'd miss it. A follow-up H03b
  could look at deep-sleep fraction or fragmentation count.
- **Garmin's sleep staging accuracy** is wrist-based and imperfect.
  Validation against PSG suggests it's accurate to within ~10–15% on
  total sleep time but less reliable on deep/REM splits.
- **The 7-night lead-up window** may be too long. Some literature
  suggests the relevant signal is 1–3 nights before. If H03 is
  refuted but the train sub-pattern is interesting, H03b with 3-night
  lead-up is a candidate.
- **Shared cause**: a developing infection / hormonal cycle / acute
  stress event can disrupt sleep AND precipitate a crash via shared
  mechanism. The test cannot distinguish "sleep predicts crash" from
  "shared upstream cause."
- **`crash_v1` mixes mechanisms** — same caveat as before. Sleep may
  predict the sleep-precipitated subset cleanly while being null on
  others.
- **Multi-comparison**: 3rd of 5 hypotheses.

## 9. What we do with each outcome

- **Supported in both windows** → first supported hypothesis in the
  batch. Write `card.md` with 2–3 candidate card-text variants using
  real numbers from this user's data and real quoted notes from the
  supported crash days. The card would say something like "the nights
  before this crash had more wake time than your usual." Proceed to H04.
- **Refuted** → write `result.md` exhaustively. Do not re-run.
  If train shows a signal that validate doesn't, treat as confirmation
  of the recovery-cliff mechanism-shift story (which would now have
  three independent precursor signals all behaving the same way).
  Proceed to H04 unchanged.
- **Inconclusive** → bring `crash_v2` forward as priority.
- **Partial** (train-yes / validate-no, or vice versa) → record
  explicitly. With H02 already partial in this shape, a *third*
  same-shape partial would be very strong evidence for the
  mechanism-shift theory.

---

*Pre-registration locked 2026-06-05. Next: `test.py`.*
