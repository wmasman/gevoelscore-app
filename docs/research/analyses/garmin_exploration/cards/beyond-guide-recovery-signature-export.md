# Beyond-the-guide: post-crash recovery signature (R7)

**Status**: producer-mode assembly for site request **R7** (beyond-the-guide
findings, Layer 3) -- the first candidate: post-crash recovery signatures /
recovery-debt. A pattern the *research* found that Wiggers does not name,
flagged as **newer and less-settled** than the Wiggers-corroboration layer.
Aggregated, privacy-safe. Collation of locked results (HA-P6, HA-P7) + R9; no
new analysis. Drafted 2026-07-03 by Claude (Opus 4.8), producer-mode, for the
participant-researcher (repo owner).

## 1. The finding (three parts, honestly)

**(a) The body IS measurably different after a crash, on the autonomic
channels.** HA-P6 (a locked Layer-1 descriptive characterisation) compared the
post-crash recovery window against **matched deep-trough non-crash days** (the
strict regression-to-the-mean control). **4 of 7 channels are statistically
distinguishable from that control** for 2 or more of the first 5 days: the
overnight/all-day stress and body-battery channels (`stress_mean_sleep`,
`all_day_stress_avg`, `bb_lowest`, `stress_low_motion`). So a crash leaves a
distinctive **autonomic** recovery shape, not just a return from a low day.

**(b) But the felt-state and resting HR just bounce back (regression to the
mean).** In the same matched-control test, **`resting_hr` and `gevoelscore`
are NOT distinguishable** from the deep-trough controls (0 of 5 days). Their
post-crash "recovery" looks like any recovery from a low day. This mirrors the
R9 recovery curves: felt-state snaps back in 2-3 days (the definitional
notch), while the autonomic stress settles slowly over ~2 weeks.

**(c) The recovery-debt does NOT compound into crash-proneness.** HA-P7 (a
locked inferential test) asked whether recent crash density predicts crash
risk. **Verdict: NOT-SUPPORTED** (odds ratio 1.13 per extra crash-day in the
prior 14 days, 95% CI [0.88, 1.27] includes 1; permutation p = 0.17). So there
is a lingering *autonomic* signature after a crash, but no measurable
*cumulative* recovery-debt that makes the next crash more likely.

**Net beyond-the-guide statement:** after a crash the watch's autonomic
channels carry a distinctive, days-long recovery signature that the felt-state
does not show, yet that signature does not accumulate into a higher crash risk
from recent crashes. The body is different after a crash; that difference does
not obviously snowball.

## 2. Literature anchor

Consistent with the PEM-recovery literature
([`../../../literature/reviews/pem_recovery_trajectory_review.md`](../../../literature/reviews/pem_recovery_trajectory_review.md)):
PEM recovery is prolonged (Moore 2023 ~12.7 d mean in ME/CFS), and the
autonomic channel is the slowest to settle (Radin 2021: resting HR ~79 d vs
steps ~32 d), so a felt-state that recovers while the autonomic index lags is
the expected ordering. Caveat: no published study paired daily felt-state +
overnight HRV through the same crash; the pairing is inferred.

## 3. Site-consumable addendum shape

Mirrors the guide-family structure; the site maps it to `addendum.json`.

```json
{
  "family": "recovery",
  "layer": 3,
  "settledness": "newer-less-settled",
  "findings": [
    {"id":"post-crash-autonomic-signature","title":"After a crash, the watch sees a recovery signature the feeling doesn't",
     "claim":"Overnight stress and body-battery stay distinctively perturbed for days after a crash, distinguishable from ordinary deep-trough days; resting HR and felt-state just bounce back.",
     "evidence":"HA-P6 (descriptive): 4 of 7 channels distinguishable from matched deep-trough controls; resting_hr + gevoelscore not.","status":"descriptive"},
    {"id":"no-recovery-debt-compounding","title":"Recent crashes don't stack the odds of the next one",
     "claim":"A lingering autonomic signature after a crash does not translate into higher crash risk from recent crash density.",
     "evidence":"HA-P7 (inferential): OR 1.13 [0.88, 1.27], p=0.17, NOT-SUPPORTED.","status":"not-supported"}
  ]
}
```

## 4. Caveats (the site must carry these)

- **Newer / less-settled layer.** Flag distinctly from the Wiggers-corroborated
  scorecard. HA-P6 is a Layer-1 *descriptive characterisation* (no
  SUPPORTED/NOT-SUPPORTED bar, by design); HA-P7 is a genuine NOT-SUPPORTED.
- **n=1, small n.** 29 crashes; CIs are wide; the matched-control RTM design is
  the honest guard but cannot make n large.
- **The felt-state depth is definitional** (crashes are low-felt-state days),
  so the informative half is the autonomic channels' distinguishability, not
  the felt-state.
- **Citalopram caveat** on the stress/BB channels post-2024 (dose-modulated);
  HA-P6's matched-control design and the within-window shape read reduce, but
  do not erase, that confound.
- **Descriptive, no causal claim.** "The body is measurably different after a
  crash," never "the crash caused a lasting change."

## 5. Cross-references

- Register R7 (beyond-the-guide, Layer 3 addendum).
- [`../../hypotheses/HA-P6/result.md`](../../hypotheses/HA-P6/result.md)
  (recovery-shape, the 4/7 matched-control read) +
  [`../../hypotheses/HA-P7/result.md`](../../hypotheses/HA-P7/result.md)
  (recovery-debt NOT-SUPPORTED).
- [`peri-event-recovery-export.md`](peri-event-recovery-export.md) (R9, the
  recovery curves + crash-vs-dip contrast) and the PEM-recovery review.
- Deferred sibling: the crash-character-flip early-vs-late deep pass
  (`../../../methodology/queued_work.md` Q22).
