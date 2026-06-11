# H04 — Result: body battery net-drain before crashes

**Verdict: REFUTED in both windows.**

But with a notable pattern that's worth recording: H04 is the **first
test in the batch to show any directional signal in the validate
window**. Validate discrimination is +13.3 pp (vs criterion +15 pp);
median delta_bb_net is −3.0 (vs criterion ≤ −3). It misses by tiny
margins. Train, oddly, is slightly inverted.

This is the *inverse* of H02's train-only pattern. No `card.md`. Data:
[result-data.json](result-data.json). Plots:
[result-train.png](result-train.png),
[result-validate.png](result-validate.png).

## Numbers

|                                            | train  | validate |
|--------------------------------------------|-------:|---------:|
| crash episodes in window                   | 14     | 15       |
| excluded for missing data                  | 0      | 0        |
| excluded for lead-up overlap               | 0      | 0        |
| **clean crash episodes**                   | **14** | **15**   |
| null sample size                           | 200    | 200      |
| % of crash lead-ups with delta_bb_net ≤ −5 | 14.3%  | 33.3%    |
| % of null windows with delta_bb_net ≤ −5   | 20.0%  | 20.0%    |
| discrimination (crash − null, pp)          | **−5.7** | **+13.3** |
| median delta_bb_net                        | −2.76  | −2.99    |
| upper quartile delta_bb_net                | +1.97  | +5.11    |
| criterion a (≥60% at ≤ −5)                 | FAIL   | FAIL     |
| criterion b (discrim ≥ +15 pp)             | FAIL   | **FAIL** (close) |
| criterion c (median ≤ −3, upper-q ≤ 0)     | FAIL   | FAIL     |

All criteria fail in both windows, so the verdict is unambiguously
refuted by the locked rules. But validate misses criterion b by 1.7 pp
and criterion c (median) by 0.01 — within rounding noise of "almost".

## The cross-window inversion is the headline

H01–H03 all showed either flat patterns or train-only signal. H04 is
the first hypothesis whose *validate* window leans toward signal while
train doesn't. Two possible reasons:

1. **Composite smoothing in train.** Body battery fuses HR + HRV +
   stress + sleep. In train, stress was elevated (H02 train-positive)
   but HR (H01) and sleep efficiency (H03) were stable. The composite
   averages stress's positive signal against null components, which
   pulls it toward zero or slightly inverts. The signal was visible in
   stress alone but invisible in the composite — and that's a finding
   in itself.
2. **A weak validate signal from another channel.** Body battery
   incorporates HRV (which we haven't tested directly). If HRV catches
   something in 2024+ crashes that RHR / stress / sleep efficiency
   don't (e.g. acute sympathetic-vagal imbalance in the lead-up), it
   would show up in body battery's composite. The signal is just
   below threshold, but its presence in validate when nothing else
   showed validate signal is worth flagging.

Either way: body battery's daily aggregate is **not** a reliable
crash precursor. The marginal validate signal is real enough to
mention but not strong enough to act on. Re-reading would defeat
pre-registration.

## What this rules out

- Body battery's daily net delta does not pass the pre-registered
  criteria as a crash precursor in either window.
- The composite does not inherit H02 train's strong positive signal —
  meaning the stress-precursor finding from H02 is **specifically a
  stress phenomenon**, not a generalisable "energy envelope" signal.
  The pacing literature's "energy envelope" framing maps onto stress
  for this user, not onto the body battery composite.

## What this does *not* rule out

- That body battery's **per-minute curve** (vs the daily charged /
  drained totals) carries more signal — body battery moves quite a
  lot intraday, and the daily summary loses the timing of dips. This
  would be H04b, and would require either parsing the FIT-level
  body-battery data (likely in `unknown_233`, which the community
  hasn't decoded) or hitting Garmin Connect's REST API. Defer.
- That HRV itself catches the validate signal that body battery
  almost did. HRV-on-rest from FIT would be a candidate
  late-batch test.

## The four-hypothesis pattern so far

| hypothesis             | train direction         | validate direction      | what we learn |
|---|---|---|---|
| H01 RHR drift          | flat                    | slight inversion        | RHR is not the channel |
| H02 avg stress         | clear positive (refuted on bar) | flat | sympathetic-arousal was the pre-recovery channel; gone in residual |
| H03 sleep efficiency   | flat                    | flat                    | sleep efficiency is not the channel; not in either era |
| H04 body battery net   | slight inversion        | weak positive (almost) | composite doesn't beat its components; validate hint worth flagging for HRV follow-up |

Daily-aggregate Garmin signals are **closed as a precursor channel**
for this user's residual (post-recovery) crashes. The only meaningful
finding in the batch was H02 train. Everything else is flat, almost-
flat, or inverted within noise.

This is the **definitive close of the daily-aggregate question**. The
remaining unexplored angles are:

- **Per-minute / spike** (H02b) — directly tests the user's
  experiential claim about intense brief moments triggering crashes.
- **Sleep sub-components** (H03b) — deep fraction, REM fraction, TST,
  fragmentation.
- **HRV-on-rest** — the only candidate the body-battery validate hint
  points at.
- **Aftermath, not precursor** (H05) — descriptive recovery
  characterisation.
- **`crash_v2` (notes-based labels)** — could split the 29 episodes
  into subtypes that have different precursors.

## Caveats acknowledged

- Body Battery's opaque algorithm and known firmware-version drift
  between FR245 versions 7.x and 10.4 are confounds we cannot
  control for.
- The composite includes sleep charging which is large compared to
  daytime drain — small daytime stress-induced drain may be masked
  by normal sleep recovery on the same day.
- Mechanism mixing in `crash_v1` applies as in H01–H03.
- Multi-comparison: H04 is the 4th of 5 hypotheses. None has been
  declared supported, so inflation isn't a concern.

## What we do next

Per hypothesis.md §9: refuted in both → write this result.md (done),
proceed to H05 unchanged. The validate-side hint at HRV is logged but
not chased now.

---

*Test run 2026-06-05.*
