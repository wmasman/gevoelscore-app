# H03 — Result: sleep efficiency drop before crashes

**Verdict: REFUTED, decisively, in both windows.**

Unlike H02's train-supported partial pattern, H03 is null on both sides
of the recovery cliff. Sleep efficiency simply does not budge before
crashes for this user — neither in 2022–23 (when stress did) nor in
2024–26 (when stress also didn't).

No `card.md`. Data: [result-data.json](result-data.json). Plots:
[result-train.png](result-train.png),
[result-validate.png](result-validate.png).

## Implementation note

The first run mistakenly used a whitelist of "confirmed" sleep-window
types and excluded 1.268 valid nights (most of the user's data has
type `ENHANCED_CONFIRMED`, which the whitelist didn't list). Fixed to
match hypothesis.md §6's actual blacklist spec
(`UNCONFIRMED` / `OFF_WRIST` / `NOT_CONFIRMED` excluded; everything
else accepted). The fix increased usable nights from 466 → 1.704 and
brought the test to the proper sample size. The pre-registration was
not changed; only the implementation was corrected to match it.

## Numbers

|                                              | train  | validate |
|----------------------------------------------|-------:|---------:|
| crash episodes in window                     | 14     | 15       |
| excluded for missing sleep nights            | 0      | 0        |
| excluded for lead-up overlap                 | 2      | 2        |
| **clean crash episodes**                     | **12** | **13**   |
| null sample size                             | 200    | 200      |
| % of crash lead-ups with delta_eff ≤ −0.05   | **0.0%** | **0.0%** |
| % of null windows with delta_eff ≤ −0.05     | 0.0%   | 0.0%     |
| discrimination (crash − null, pp)            | 0.0    | 0.0      |
| median delta_eff                             | −0.002 | −0.004   |
| upper quartile delta_eff                     | +0.001 | +0.000   |
| criterion a (≥60% at ≤ −0.05)                | FAIL   | FAIL     |
| criterion b (discrimination ≥ +15 pp)        | FAIL   | FAIL     |
| criterion c (median ≤ −0.03, upper-q ≤ 0)    | FAIL   | FAIL     |

Not just refuted — the threshold (5 pp drop) wasn't crossed by a single
episode in either window, nor by any of the 200 null windows. The
median pre-crash drop is ~0.2–0.4 pp, well inside daily noise.

## Reading the result

Sleep efficiency, as defined
(`TST / (TST + awake + unmeasurable)`), is remarkably stable for this
user across the full window. Neither crash lead-ups nor random non-crash
windows produce 5-percentage-point efficiency drops. The user's sleep
efficiency is **flat as a board**.

Two compatible interpretations:

1. **The metric is too smooth.** Sleep efficiency averages over many
   pathophysiologies. The user's sleep could be disrupted in ways
   invisible to efficiency: shorter total sleep time, more
   fragmentation (many short awakenings without one long awakening),
   reduced deep-sleep fraction specifically, reduced REM specifically,
   longer sleep latency. Hypothesis.md §8 flagged this risk
   explicitly.
2. **Sleep efficiency genuinely is not a precursor.** Even in the
   train window where H02 showed a real stress precursor signal, sleep
   efficiency was null. This is consistent with the user's pre-recovery
   crashes being sympathetic-arousal precipitated (which H02 picked up)
   rather than sleep-debt precipitated. Sleep stayed within normal
   range; the autonomic system was the load-bearing channel.

The second reading aligns with the pacing literature's framing:
sympathetic overload → crash, not chronic sleep dysregulation → crash.
Sleep dysregulation matters in *post-crash* recovery (an H05 question),
not as the primary trigger.

The first reading argues for an **H03b** with sharper sleep metrics:
deep-sleep fraction, REM fraction, total sleep time, fragmentation
count. We can't distinguish (1) from (2) without that.

## What this rules out

- **Sleep efficiency as a precursor signal is dead** for this user, in
  both pre- and post-recovery windows.

## What this does *not* rule out

- That **specific sleep stage proportions** (deep, REM) drop before
  crashes while overall efficiency is preserved.
- That **fragmentation** (many short awakenings) rises before crashes
  even when total awake time is unchanged.
- That **total sleep time** is the precursor — short nights rather than
  inefficient nights.
- That sleep matters most for **recovery** (H05) rather than precursor.

## The cross-hypothesis picture so far

| hypothesis | train         | validate     | net pattern |
|---|---|---|---|
| H01 RHR    | refuted (~null) | refuted (~null, slight inversion) | flat |
| H02 avg stress | refuted but real direction (median +2.7, disc +25.9pp, 79% positive) | refuted (~null) | recovery cliff |
| H03 sleep eff | refuted (null) | refuted (null) | flat |

H02 is the only hypothesis to show a real biometric precursor signal,
and only in train. H01 (RHR) and H03 (sleep efficiency) are flat in
both windows. This is a coherent picture: **pre-recovery crashes had a
sympathetic-arousal precursor (H02 train) but no RHR or
sleep-efficiency precursor**. Post-recovery, even the sympathetic
precursor disappears. This matches the recovery-cliff "kind of crash
changed" theory and adds new information: the kind that *did* trigger
crashes pre-recovery was specifically the sympathetic-arousal kind,
not the chronic-sleep-debt kind.

## Caveats acknowledged

- The whitelist bug (1.268 valid nights initially excluded) was caught
  before result interpretation. Fix matches hypothesis.md §6 verbatim.
- Garmin's wrist-based sleep staging is imperfect; deep/REM splits
  especially are less reliable than total sleep time.
- Sleep efficiency is one of many possible sleep metrics — see "What
  this does not rule out."
- Shared cause confounds remain in principle but the null result
  largely mooted them.

## Implications for H04 / H05 / follow-ups

- **H04 (body battery)**: H04 composites RHR + HRV + stress. RHR is
  null (H01). Stress shows train-only pattern (H02). If HRV adds
  anything, H04 might inherit the train-only pattern. If HRV is also
  null, H04 will be flat in both windows.
- **H05 (recovery time)**: unchanged — descriptive, not predictive.
- **H02b (per-minute stress spike count)** is now the highest-priority
  follow-up. User has independently confirmed (2026-06-05) the
  experiential pattern that *an intense moment during an otherwise
  calm day can trigger a crash* — exactly the signal a daily average
  smooths away. H02b's per-minute resolution is built for this.
- **H03b candidates**: deep-sleep fraction, REM fraction, total sleep
  time, fragmentation count. Defer to second batch unless H05
  surfaces a sleep-recovery angle.

## What we do next

- Per hypothesis.md §9: write this result.md (done), proceed to H04.
- Promote H02b to next-in-line after H04, ahead of any H03b.

---

*Test run 2026-06-05. Re-runnable with the same inputs + seed.*
