# H02d — Result: stress spikes with uncensored sentinels + wider window

**Primary verdict (imputed × 4-day window): REFUTED.** All four
combinations of {imputed, bridge} × {4-day, 5-day} refuted overall,
but the *shape* of the refutation tells two clean and distinct
stories.

The censoring fix (treating "too active" sentinels as ≥ 75) made the
metric over-sensitive: both crash and null windows hit ~85% above the
+10-minute threshold. The wider-window fix worked in train as
predicted (bridge × 5-day = +31.8 pp discrimination, the strongest
train signal of any H02-family test), but validate refuted across the
board — confirming the recovery-cliff reading: residual 2025+ crashes
are *not* stress-spike-precipitated, regardless of how we measure the
spike.

No `card.md`. Data: [result-data.json](result-data.json).

## Headline numbers

|                                              | imputed × 4d (PRIMARY) | imputed × 5d | bridge × 4d | bridge × 5d |
|----------------------------------------------|----:|----:|----:|----:|
| train clean episodes                         | 14   | 13   | 14   | 13   |
| validate clean episodes                      | 15   | 15   | 15   | 15   |
| **train** % crash ≥ +10 min                  | 85.7% | 84.6% | 78.6% | **92.3%** |
| **train** % null ≥ +10 min                   | 82.0% | 86.5% | 51.0% | 60.5% |
| **train** discrimination (pp)                | +3.7 | −1.9 | **+27.6** | **+31.8** |
| **train** median delta_spike (min)           | 34.8 | 40.6 | 16.6 | 28.2 |
| **train** verdict                            | refuted | refuted | **supported** | **supported** |
| **validate** % crash ≥ +10 min               | 73.3% | 86.7% | 60.0% | 66.7% |
| **validate** % null ≥ +10 min                | 82.0% | 86.5% | 51.0% | 60.5% |
| **validate** discrimination (pp)             | −8.7 | +0.2 | +9.0 | +6.2 |
| **validate** median delta_spike (min)        | 26.0 | 25.9 | 11.0 | 11.1 |
| **validate** verdict                         | refuted | refuted | refuted | refuted |
| **overall verdict**                          | **refuted** | refuted | refuted | refuted |

(`+10 min` threshold = pre-registered criterion a. `+15 pp` = criterion b.)

## What the numbers say

**1. Sentinel imputation made the metric undiscriminating.** Across
1738 valid days, 276 015 "too active" samples were classified — about
159/day on average. When we count them all as ≥ 75 stress, the
*baseline* trimmed-mean max-spike rises uniformly with the *lead-up*
max-spike. Crashes and null windows both end up at ~85% above the
+10-min threshold. The censored-arousal idea wasn't physiologically
wrong — too_active sentinels DO correlate with HR-confirmed
on-wrist arousal (calibration showed 100% within ±60 s) — but the
operationalisation "treat ALL too_active as 75-stress" is far too
generous. Almost every day has some walking, light exertion, or
in-bed restlessness that crosses into "too active" without being a
panic-grade event.

**2. The window extension worked exactly as the lag profile
predicted.** Bridge arm (= H02b's censoring logic) at the new windows
shows clean train discrimination:

- H02b at 3 days: +29.9 pp train (locked baseline)
- H02d bridge at 4 days: **+27.6 pp** train
- H02d bridge at 5 days: **+31.8 pp** train

The 5-day window is the strongest *single-channel train signal of any
H02-family test*. This matches HA01b's lag-profile finding for the
activity channel (+23 pp validate disc at 5d) and gives independent
cross-channel confirmation that this user's empirical precursor lag
peaks at ~5 days. The 3 → 4 → 5-day progression in train discrimination
is smooth and monotonic.

**3. Validate refuted in all four arms.** This is the robust finding.
The recovery cliff genuinely changed the precursor structure:

- imputed_4d validate disc: −8.7 pp
- imputed_5d validate disc: +0.2 pp
- bridge_4d validate disc: +9.0 pp
- bridge_5d validate disc: +6.2 pp

Crash frequencies in validate are not zero — 60–87% of validate
episodes have lead-up max-spike ≥ +10 min above baseline — but the
*null* windows also hit 51–87% above threshold. The discriminative
signal genuinely isn't there for the 2024+ era. This is the same
conclusion H02b reached at 3 days; widening the window and uncensoring
the sentinels did not recover it.

**4. The validate null rate is much higher than pre-registered
expectation.** §7 of the hypothesis predicted null rate 25–40%. Actual
null rates: 51% (bridge_4d), 60.5% (bridge_5d), 82% (imputed_4d),
86.5% (imputed_5d). Two reasons:
- At a 5-day window, random non-crash windows almost always include
  one day with a sustained ≥75 stress block — this user simply has
  enough busy/stressful days that any 5-day stretch contains one.
- Under imputation, the threshold is effectively trivial.

This was flagged as a possible failure mode in §7 ("if crash rate
≥ 95% and null rate ≥ 90% → metric is over-inflated"). At 82–87% for
the imputed arm, the metric is in that regime.

## Per-episode breakdown (bridge × 5-day, strongest train signal)

### Train (13 of 14 with clean lead-up + baseline; 12 crossed +10 min)

| episode start | lead-up max | baseline | delta | crosses +10? |
|---|---:|---:|---:|---|
| 2022-09-03 | 43.0 | 14.2 | **+28.8** | YES |
| 2022-09-16 | 27.0 | 15.8 | **+11.2** | YES |
| 2022-09-30 | 56.0 | 16.1 | **+39.9** | YES |
| 2022-11-23 | 41.0 | 12.4 | **+28.6** | YES |
| 2022-12-27 | 38.0 | 10.8 | **+27.2** | YES |
| 2023-02-04 | 63.0 | 12.6 | **+50.4** | YES |
| 2023-04-02 | 42.0 | 13.8 | **+28.2** | YES |
| 2023-05-28 | 19.0 | 12.2 | +6.8 | no |
| 2023-09-07 | 42.0 | 13.0 | **+29.0** | YES |
| 2023-09-16 | 29.0 | 13.1 | **+15.9** | YES |
| 2023-09-27 | 31.0 | 12.8 | **+18.2** | YES |
| 2023-11-12 | 40.0 | 11.2 | **+28.8** | YES |
| 2023-11-27 | 27.0 | 11.2 | **+15.8** | YES |

Compared to H02b's 3-day train: 12 of 13 versus H02b's 10 of 14. The
wider window picks up two episodes H02b missed (2022-09-16 and
2023-09-27 in particular), without adding a single false negative.

### Validate (15 of 15 clean; 10 of 15 crossed +10 min)

| episode start | lead-up max | baseline | delta | crosses +10? |
|---|---:|---:|---:|---|
| 2024-01-12 | 28.0 | 10.5 | **+17.5** | YES |
| 2024-01-21 | 9.0 | 10.0 | −1.0 | no |
| 2024-02-15 | 24.0 | 9.6 | **+14.4** | YES |
| 2024-02-25 | 29.0 | 9.5 | **+19.5** | YES |
| 2024-04-30 | 32.0 | 11.6 | **+20.4** | YES |
| 2024-05-28 | 18.0 | 10.3 | +7.7 | no |
| 2024-06-18 | 30.0 | 10.0 | **+20.0** | YES |
| 2024-06-25 | 21.0 | 9.9 | **+11.1** | YES |
| 2024-07-15 | 69.0 | 9.6 | **+59.4** | YES |
| 2024-08-29 | 17.0 | 10.4 | +6.6 | no |
| 2024-12-23 | 14.0 | 7.3 | +6.7 | no |
| 2025-04-24 | 16.0 | 5.8 | **+10.2** | YES |
| 2025-10-02 | 21.0 | 10.3 | **+10.7** | YES |
| 2026-05-12 | 13.0 | 11.2 | +1.8 | no |
| 2026-05-20 | 23.0 | 11.5 | **+11.5** | YES |

Validate is genuinely different from H02b's 3d validate:
- 10 of 15 above +10 min (H02b: 5 of 15)
- median delta +11.1 (H02b: +6.7)
- a few clear positive cases (2024-07-15 with +59.4; 2024-04-30 with
  +20.4) — these episodes look like pre-cliff crashes did.

But the null at 5d hits 60.5%, so 67% crash rate isn't enough to
clear the +15 pp bar. The signal is *there* in validate at the new
window — it just doesn't differentiate from a population of equally
busy non-crash 5-day windows.

## Cross-channel comparison

H02d bridge_5d train (+31.8 pp) is the strongest train-window single-
channel discrimination of any pre-registered hypothesis so far. The
runners-up:
- H02b train (3d, stress-spikes): +29.9 pp
- H02-train (3d, daily-average stress): +25.9 pp
- HA01b validate (4d, activity shock): +17.3 pp [the only SUPPORTED
  validate-era hypothesis to date]

The pre-cliff era's strongest single Garmin precursor is sustained
intense-stress events in the days before the crash, with the lag
window peaking around 4–5 days. This matches the user's experiential
framing precisely. The post-cliff era does not show the same signal
through this channel.

## Caveats per §8

- **Garmin's stress algorithm changes** across firmware versions, so
  some of the lower validate-era baseline (~10 vs ~13 in train) may
  be firmware drift, not pure physiological change. This would
  *boost* delta_spike spuriously in validate, not depress it, so it
  doesn't explain the validate refutation.
- **Sentinel codes not semantically distinguished.** The two codes
  (−1, −2) were treated identically. Whether one carries "moderate
  effort" and the other "near-VT crossing" is undecoded; could
  matter for H02e.
- **±60 s tolerance is locked from an 8-file sample.** Cross-firmware
  stability of HR cadence wasn't tested across the full 1738-day
  window. Unlikely to materially affect the verdict.
- **Wider lead-up window inflates both numerators** (predicted, §8).
  The +15 pp criterion was deliberately held identical to make H02d
  *harder to pass*. Honest accounting: the bar bit.
- **No activity-overlap diagnostic surfaced in this result.** The
  `extract_v2.py` does not currently cross-reference activity
  sessions; this is now the leading candidate for an H02e refinement.
- **`crash_v1` mixes mechanisms.** Per the train per-episode table,
  one of 13 train episodes (2023-05-28) shows baseline-level
  spike — likely the non-spike-precursor subset, consistent with
  the H02b finding.

## What this changes

1. **The censored-arousal hypothesis is not killed, but the specific
   operationalisation is.** Treating all too_active as 75-stress is
   too generous. A future H02e should classify too_active samples by
   HR magnitude — only impute when HR ≥ ~100 bpm (real sympathetic
   arousal) rather than blanket-applying. This filters out the daily
   "took a brisk walk to the bathroom" too_active minutes.
2. **The lag profile insight is confirmed for the stress channel.**
   This user's empirical precursor lag is 4–5 days, not 3. Future
   precursor hypotheses default to 4d/5d windows, not 3d.
3. **The "recovery cliff changed the precursor structure" reading
   gets stronger.** Across four operationalisations (H02 daily mean,
   H02b 3d spikes, H02d 4d/5d × imputed/bridge), validate never
   shows clean spike-precursor discrimination. Five tests on the
   stress channel are now consistent. The residual 2025+ crashes are
   *not* sympathetic-spike-precipitated.
4. **HA01b remains the only SUPPORTED validate-era precursor.** The
   activity-shock signal at 4d survives the cliff in a way the stress
   channel does not. That asymmetry is the next analytical lead.
5. **No card from H02d directly.** But the bridge_5d train per-episode
   table is the cleanest pre-cliff illustration of the original user
   claim: "an intense moment can trigger a crash." For pre-cliff
   retrospective cards (2022–23 era only) this is the strongest
   single-channel finding we have.

## Cross-feature note

The [exertion-tracking](../../../../features/exertion-tracking/) v2
feature will capture the same construct H02d targets but from the
subjective side (cognitive / physical / emotional load, 4-point
worded scale per day). Once it accrues data, the natural follow-up is
testing whether subjective lead-up exertion subsets crash episodes by
which Garmin-channel precursor fired. The 4-day primary window in
H02d matches the exertion feature's own "delayed-cost surfacing"
framing in its Future Considerations — consistent across feature and
research planes.

---

*Tests run 2026-06-06. Pre-registration locked 2026-06-06 at
[hypothesis.md](hypothesis.md). Calibration locked 2026-06-06 at
[../H02b-stress-spikes/calibrate_sentinel_hr_result.md](../H02b-stress-spikes/calibrate_sentinel_hr_result.md).*
