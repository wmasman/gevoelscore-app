# Beyond-the-guide: the autonomic fingerprints of load (R4)

**Status**: producer-mode assembly for site request **R4** (trigger type:
physical / emotional / cognitive), Layer 3 beyond-the-guide, framed as a
**refinement of a Wiggers claim** (her mental-PEM concession) rather than pure
corroboration or a wholly new finding. Aggregated, privacy-safe (personal-baseline
effect sizes, no dated raw values). Collation of the R4 descriptive precondition +
concordance; the analysis is
[`../../descriptive/trigger_types_r4/precondition.md`](../../descriptive/trigger_types_r4/precondition.md)
(reproducible via `precondition_analysis.py`). Drafted 2026-07-04 by Claude (Opus
4.8), producer-mode, for the participant-researcher (repo owner). Flagged **newer
and less-settled** than the Wiggers-corroboration layer.

> "stress" here = Garmin's HRV-derived Stress Score (GSS), never mental /
> emotional stress. Overnight stress is used as the HRV-drop proxy (higher stress
> = lower HRV).

## 1. What the guide says

Wiggers' handleiding treats physical, cognitive, and emotional load as three
draws on **one energy envelope**, each able to trigger PEM, and warns that a
step-counter misses the non-physical ones. Her specific, testable concession (the
mental-PEM passage) is:

> *"Too much mental activity, such as working on your laptop or writing, often
> goes undetected in your Garmin, but excessive mental activity can still cause
> PEM. It will also cause your HRV to drop that night or the following night. So,
> be aware that your Garmin can't warn you about everything."*

So the guide's claim is two-part: (a) non-physical load is undetected in the
*activity* view, but (b) its *autonomic aftermath* shows up as an HRV drop that
night or the next.

## 2. The finding (three fingerprints, honestly)

Comparing each self-reported load type against the wearable channels, in
personal-baseline units, isolated of co-occurring physical load and adjusted for
felt-state (bootstrap 95% CIs; a crash-prone "good-day confound" makes the
isolated read the honest one). The load tags come from notes and calendar, not
from the wearable, so the emotional and cognitive agreements are **non-circular**
cross-modal checks.

**(a) Physical load is visible in the activity view, as the guide expects.** Peak
cardiac strain and activity volume rise modestly (both CIs exclude 0), plus the
overnight body-battery floor drops (activity depletion). This is the load the
watch is built to catch.

**(b) Cognitive load is invisible to the watch, aftermath included.** Isolated,
it moves **no channel** -- not heart rate, not daytime stress, and, tested
directly against the guide's own claim, **not overnight HRV on either the same
night or the following night, even at severe intensity**. So for cognitive load
(Wiggers' own laptop/writing example) the watch misses not just the activity but
the autonomic aftermath too. It is blinder to cognitive load than the guide
expects.

**(c) Emotional load is the keeper: invisible in heart rate, but it leaves an
autonomic trace, on the guide's exact timing.** Emotional load is **flat in heart
rate** yet **robustly raises daytime stress and lowers the overnight body-battery
floor** (both CIs exclude 0, both survive felt-state adjustment). And the
guide-predicted HRV drop appears with the timing Wiggers names: overnight stress
is suggestive *that* night and **significant the *following* night** -- her "that
night or the following night" hedge captures a real one-day lag.

**Net beyond-the-guide statement:** the guide says the watch can't see non-physical
load but its autonomic aftermath may surface overnight. This body sharpens that:
the aftermath appears for **emotional** load (in stress and body-battery, not in
heart rate, peaking the following night, exactly as the guide times it) and is
**absent for cognitive** load (Wiggers' own example), which stays invisible even
in the overnight signal. The guide lumps "mental activity"; the data splits it --
the watch sees your emotional load, just not in your heart rate, and it does not
see your cognitive load at all.

## 3. Honesty flags (carry these to the surface)

- **n=1, self-report, same-day / next-day concordance, not causation.** The load
  is self-reported (notes + calendar); the reads are associations in personal-
  baseline units, with wide, autocorrelation-unmodelled bootstrap CIs. Small
  isolated cells (emotional-isolated ~70 days).
- **The concordance is the robust part; a *trigger* claim is separate and only
  suggestive.** A companion analysis found emotional load also mildly elevated in
  the run-up to crashes, but that signal is **suggestive-not-established** (does not
  survive multiplicity, and is concentrated in one medication era). It is being
  handled as a lead for a future pre-registered test, and must **not** be presented
  here as "emotional load predicts your crashes." This card is about what the watch
  *sees*, not what *triggers* a crash.
- **Non-circular for emotional / cognitive** (loads tagged from notes, not the
  wearable); physical-load-vs-activity is partly circular and is the least novel of
  the three.
- **Descriptive, no causal marks:** "emotional load co-occurred with an overnight
  HRV drop in this body," never "emotional load caused it."

## 4. Site-consumable shape

Layer 3 (`/beyond`) refinement card, anchored to the guide's mental-PEM passage.
Suggested shape (aggregated, no dated values):

```
{
  "anchor_quote": "<Wiggers mental-PEM concession>",
  "fingerprints": [
    { "load": "physical",  "seen_in": ["cardiac strain", "activity", "battery floor"], "in_heart_rate": true },
    { "load": "cognitive", "seen_in": [], "in_heart_rate": false, "overnight_hrv": "no trace (either night)" },
    { "load": "emotional", "seen_in": ["daytime stress", "battery floor"], "in_heart_rate": false,
      "overnight_hrv": "drop, peaking the following night" }
  ],
  "headline": "The watch sees your emotional load, just not in your heart rate; it does not see your cognitive load at all.",
  "confidence": "newer / less-settled; n=1; descriptive"
}
```

## 5. Cross-references

- Analysis:
  [`../../descriptive/trigger_types_r4/precondition.md`](../../descriptive/trigger_types_r4/precondition.md)
  (section 5 concordance + section 5.4 the Wiggers timing test) and
  [`../../descriptive/trigger_types_r4/analysis.md`](../../descriptive/trigger_types_r4/analysis.md)
  (the separate, suggestive trigger read).
- Guide claims: `../../../wiggers_testable_hypotheses.md` (H2 activity-invisible /
  mental PEM; the mental-PEM concession, PDF lines 1448-1457) and the handleiding
  [`../../../literature/wiggers_pacing_handleiding.pdf`](../../../literature/wiggers_pacing_handleiding.pdf).
- Energy-envelope framing: `../../../literature/pacing-and-crash-mitigation.md`.
- Site register R4, R32 (no visible trigger-into-crash signal): the site's
  `docs/research-requests.md` (external repo `wiggers_research_story`).
