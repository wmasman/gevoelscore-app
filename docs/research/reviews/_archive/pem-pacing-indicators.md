> **ARCHIVED 2026-06-07.** This document has been **superseded by
> [app-plan.md](../app-plan.md)** (the merged active product plan
> combining this piece with the trajectory-and-events plan). Content
> preserved verbatim below for audit-trail continuity. Do not edit;
> update the merged plan instead. Historical research references to
> "pem-pacing-indicators" should be read as pointing here.

---

# PEM-pacing indicators from Garmin biometrics

*Status: descriptive — derived from the activity-labels phase and the H02b stress-spike finding. Reading version of the research; precedes any feature plan.*

*Audience: someone living with chronic post-acute infection syndrome (PAIS), trying to characterise their personal energy envelope and notice events that affect exertion or raise risk of a PEM episode.*

## 1. What this document is

This is a curated list of biometric indicators, derived from Garmin wearable data, that have **at least some defensible statistical credibility** as awareness signals for PEM-pacing in a person with PAIS. Tier 1 indicators have direct support from a pre-registered hypothesis test. Tier 2 indicators are descriptive companions — useful for understanding context, not for prediction in isolation.

All indicators are constructed to be **baseline-relative**: defined against the individual's own rolling history, not against population norms or athletic-training targets. The framing is *PEM envelope*, not *training load*. The aim is to help someone avoid pushing the wall, not to optimise an athletic adaptation.

**Relative thresholds, not absolute**: thresholds are pre-registered in z-score or percentile-rank units, not in absolute bpm / ms / minutes. The HA06 → HA06b methodological lesson made this explicit — absolute thresholds drawn from external populations (Workwell's RHR +5/10/15 bpm, the *vermoeidheidskliniek*'s HRV −10 ms day-over-day rule) need re-calibration to participant variability *before* the test, since the participant's signal-to-noise characteristic can materially differ from the calibration population. The principle is locked in the project's feedback memory.

The evidence base is n=1 (the participant). Any cross-person generalisation is a hypothesis, not a claim.

## 2. Framing: energy envelope, PAIS, PEM

In PAIS conditions — Long COVID, ME/CFS, post-Lyme, post-EBV — patients often describe an *energy envelope*: a range of exertion they can sustain without triggering Post-Exertional Malaise (PEM). The envelope is small and unstable. Push above it once (a *shock*) or repeatedly (a *push-crash pattern*) and a crash follows, often delayed by hours to days.

Two mechanistic threads recur in the literature:

- **Sympathetic over-activation**: autonomic dysregulation, with the sympathetic nervous system firing harder than it should during ordinary moments. Measurable as transient spikes in HR-derived stress.
- **Parasympathetic recharge failure**: insufficient overnight recovery, often reported subjectively as "unrefreshing sleep". Measurable, in principle, as the overnight recharge of physiological reserves.

The indicators below partially cover the first thread. The second thread is gated on future work decoding per-minute Body Battery (see registry §4 H04b).

Two further patterns are useful for understanding why a metric matters:

- **Shock-induced PEM**: a single acute event in an otherwise calm period can trigger a crash.
- **Push-crash**: sustained moderate elevation over a 5-10 day window erodes the envelope until a crash arrives.

A complete picture needs indicators that catch both modes.

---

## 3. Tier 1 — directly supported indicators

These indicators have at least one pre-registered hypothesis test SUPPORTED, or are sensitivity-tested as robust.

### 3.1 Daily exertion class

**What it is.** A five-level classification of today's overall exertion: `none / light / moderate / heavy / very_heavy`. Computed from a composite percentile rank over four axes (effective intensity-minutes, total steps, daily-max HR, vigorous minutes), each ranked within a 30-day rolling baseline of the *same* person.

**What it measures.** Not "how active you were" in absolute terms. Rather: where today sat relative to your own recent typical days. A 4 000-step day might be `very_heavy` for someone whose 30-day median is 1 800 steps, and `light` for someone whose median is 6 000.

**Why it matters for PEM-pacing.** PEM is induced by exertion that exceeds the personal envelope. The envelope shifts with stabilisation trajectory and recent load. An absolute step or HR threshold cannot track this. A percentile-rank class can.

The validate-era pre-registered test (HA01b) showed that the presence of a `heavy` or `very_heavy` day in the 4-day window before a crash discriminates crash days from baseline days by +17.3 percentage points. This is the first SUPPORTED validate-era precursor in the investigation.

**Sensitivity status**: ROBUST. The classification agrees with itself across 13 parameter variations (Jaccard ≥ 0.7), so small changes in the rank cutoffs do not materially change which days get flagged as heavy+.

**App implementation idea.**

A single-line reading card on the day's overview:

```
vandaag
[ . . . . . ] matig zwaar
```

Five dots, three filled to indicate `moderate-heavy`. No number. No score. Compact enough for the timeline; can sit next to the gevoelscore for the same day so the user sees both the *felt* score and the *measured* exertion class side by side.

For the timeline view: render the class as a small coloured bar under each day, using the warm-earth palette graded from sand to a darker terracotta for `none → very_heavy`.

### 3.2 Seven-day push burden

**What it is.** A simple count: how many `heavy` or `very_heavy` days fell in the last 7 days. A single number from 0 to 7.

**What it measures.** Sustained-push pattern accumulation. A week of 1-2 heavy days is typical; a week of 4-5 is a sustained push that often precedes a crash even when no single day was extreme.

**Why it matters for PEM-pacing.** The push-crash pattern is a defining feature of PAIS-PEM. It is one of the hardest patterns for the patient to self-detect, because no individual day feels extreme. A running count makes it visible.

**Statistical credibility.** The *predictive* test (HA02, push burden → crash) was REFUTED. But the *raw count* is sensitivity-ROBUST as a descriptive measure of sustained load. It does not predict tomorrow's crash by itself — but it does honestly describe whether you are inside a sustained-push pattern.

This is the most important caveat in the document: a descriptive metric can be useful and honest *without* being predictive. Push burden is one such case.

**App implementation idea.**

A second line on the same overview card:

```
deze week
3 zware dagen, jouw mediaan is 1
```

Two facts. Today's count, your typical count. The user is left to draw the inference. No alert, no traffic light.

For the timeline: a faint horizontal band across the last 7 days, slightly more saturated when push burden is above the personal median. Glanceable, not demanding.

### 3.3 Daily stress spike

**What it is.** The single highest minute of HR-derived stress in the day. Garmin's continuous stress estimate (0-100 per minute, computed from HRV) gives one value per minute; this indicator takes the maximum across the day.

**What it measures.** Acute sympathetic over-activation. Not how stressed you felt all day on average — that is a different and less useful signal. Rather: did the autonomic system fire hard at any point today?

**Why it matters for PEM-pacing.** The participant's experiential observation is that intense moments inside otherwise calm days can trigger crashes. This matches the sympathetic-over-activation mechanism. A spike measure catches this; a daily average does not.

**Statistical credibility.** **Seven pre-registered tests have locked SUPPORTED verdicts in train-era on record** and **two pre-registered tests have locked SUPPORTED verdicts in validate-era on record**, with **one (HA07d) SUPPORTED in BOTH** under the strict locked rule. The threshold-monotonicity diagnostic round (v1 → v2, atomic update 2026-06-07) applied locked rescue/close criteria across HA10, HA07d, HA06b, HA11. v2 outcomes: HA10 validate RESCUE via Cat 3 (rising/late-peak); HA07d both eras RESCUE via Cat 2 (stable plateau) and Cat 3; HA11 train RESCUE via Cat 1 (canonical decline); HA06b train CLOSE via Cat 4 (2 sign-changes in meaningful range) — permanently demoted from load-bearing. HA07d's overall-SUPPORTED status restored under v2. Card (b2) validate-era anchored on HA07d primary + HA10 corroborating; specificity tables required before any card.md ships. Train-era SUPPORTED: H02b at 3-day stress spike (+29.9 pp, 71% freq); H02d bridge × 5d sentinel-corrected (+31.8 pp, 92% freq — strongest train signal); HA06b nightly RHR z-score 4d (+18.9 pp); HA11 within-day U-dip count z-score 4d (+22.8 pp); HA07c sleep stress mean delta z-score 4d (+23.2 pp — HRV proxy); HA08c sleep stress slope z-score 4d (+23.0 pp); **HA07d sleep stress VARIABILITY delta z-score 4d bidirectional (+19.6 pp — also validate-era SUPPORTED)**. Validate-era SUPPORTED: HA10 morning BB peak z-score 4d bidirectional (+16.2 pp, 86.7% freq, elevated direction); **HA07d sleep stress variability delta z-score 4d bidirectional (+21.7 pp at primary, +28.5 pp at N_std=2.0 lowered direction — strongest validate-era discrimination in the project)**. H02d's bridge train discrimination scales monotonically with window (3d → 4d → 5d = +29.9 → +27.6 → +31.8 pp), corroborating the user's 4-5 day empirical PEM lag, now confirmed across seven channels. **Era-shift framing**: the pre-cliff era (2022-23) shows sympathetic-arousal-spectrum + autonomic-volatility precursors firing across seven channels/primitives. The post-cliff era (2024+) shows parasympathetic-swing + autonomic-stillness precursors firing across two channels. HA07d's overall-SUPPORTED finding formalises the era directionality reversal on a single channel: train SUPPORTS both elevated AND lowered direction (volatility); validate SUPPORTS only the lowered direction (stillness). **Wiggers' "freeze" pattern is now empirically population-level visible** in two independent validate-era channels (HA10 elevated BB + HA07d lowered variability) at substantial discrimination magnitudes (+16.2 to +28.5 pp). For 2022-23 retrospective surfacing, the daily stress spike indicator is well-grounded across multiple time-scales and channels. For 2024+ live use, the validate-era anchors live in HA10 BB peak elevated direction AND HA07d sleep stress variability lowered direction — both consistent with the freeze pattern.

**App implementation idea.**

A small marker, only shown when the day's max-stress exceeds the personal H02b threshold. Treated as an event, not a continuous gauge:

```
vandaag was er een acute stresspiek
```

One sentence. Optional: a small icon on the timeline day-marker. Avoid any "stress level" gauge — the daily-max-spike is binary in its information content.

---

## 4. Tier 2 — descriptive companion indicators

These do not have a pre-registered SUPPORTED test of their own, but they are robust, baseline-relative, and useful for explaining or contextualising the Tier 1 signals.

### 4.1 Effective exertion percentile rank

**What it is.** The single-axis percentile rank of today's `effective_exertion_min` (UDS-derived intensity-minutes plus duration of recorded activities) within the personal 30-day baseline. A number from 0 to 100.

**What it measures.** The dominant single physical-load axis. Exploratory per-axis decomposition of the HA01b composite showed that `effective_exertion_min` is the largest contributor (+32.4 pp train, +17.4 pp validate). Of all the individual axes, this one carries most of the signal.

**Why it matters for PEM-pacing.** If you can only display one number for "how much physical load did today carry", this is the most defensible single number. It captures both passive intensity (walking can count for a deconditioned person) and recorded activity duration in one metric.

**App implementation idea.** Rarely shown as a number on its own. Instead used as a *tooltip* or detail-view on the exertion-class card: when the user taps to expand, show "today: 78th percentile in your 30-day window for effective intensity-minutes". A way to drill in without cluttering the daily overview.

### 4.2 Dip-cluster proximity

**What it is.** A flag: are you currently inside a 7-day window after a recent crash or dip?

**What it measures.** Vulnerability windows. Empirical observation (crash_v2 cluster analysis): dips and crashes arrive in clusters more often than in isolation. Within ~7 days of a recent dip, the next dip is more likely.

**Why it matters for PEM-pacing.** When today feels harder than the activity level would predict, "we are still inside a cluster from 4 days ago" is often the explanation. Naming it helps the user not over-explain bad days with confounding theories.

**Statistical credibility.** Descriptive only. We have not tested whether cluster-proximity predicts the next crash — only observed that crashes/dips do cluster. Useful as context, not as a prediction.

**App implementation idea.** A subtle background tint on the daily card if today is within 7 days of a recent dip, with hover/expand text "5 dagen na een dip". Easy to ignore when not relevant; visible when needed.

### 4.3 Personal-baseline z-score

**What it is.** Today's effective-exertion deviation from the 30-day rolling baseline, expressed as a z-score. Complement to the percentile rank: rank is robust but flattens magnitude; z-score preserves how *much* above baseline today is.

**What it measures.** The size of the shock, not just whether one occurred. A z of +2 and a z of +4 both sit at the 95th-plus percentile, but they are very different physiological events.

**Why it matters for PEM-pacing.** Two consecutive `very_heavy` days are not equivalent: one might be 2× the rolling median, the other 5×. The z-score lets the user see this distinction when looking back over a week.

**App implementation idea.** Not surfaced on daily card. Surfaced on weekly/monthly review screens as a small chart: 30 days of z-scores with a band at ±2 marked. A reflection tool, not a daily-pacing one.

---

## 5. Implementation patterns

### 5.1 Composition principles

The indicators above are not meant to be displayed in parallel as six separate widgets. They compose into roughly three reading surfaces:

| Surface | Purpose | Indicators it carries |
|---|---|---|
| Today's overview | Glance: where am I now | 3.1 exertion class, 3.2 push burden, 3.3 stress-spike flag (if triggered) |
| Looking-back review | Reflection: what was the last week shaped like | 4.3 z-score chart, 3.1 class strip, 3.3 spike markers, 4.2 cluster windows |
| Forward-window awareness | Caution: what should the next 4-5 days look like | derived from 3.1 (if today is heavy+, the next 4-5 days warrant lighter targets) |

Both surfaces are *reading* surfaces. They can live anywhere on the screen and do not need to obey the thumb-first input-zone rule (which governs the score / note / tag entry surfaces).

### 5.2 Suggested build priority

If implementing incrementally, the suggested order is:

1. **Daily exertion class** (3.1). The single most evidence-supported indicator and the easiest to interpret. Anchor for everything else.
2. **Seven-day push burden** (3.2). Builds directly on (1), trivial to compute once class is in place, fills a different visibility gap.
3. **Dip-cluster proximity** (4.2). Pure derivation from existing crash_v2 labels. No new Garmin parsing needed.
4. **Daily stress spike flag** (3.3). Requires daily-max stress extraction (already done for H02b). Surface as an event marker.
5. **Effective exertion percentile rank** (4.1) and **personal z-score** (4.3). Detail-view content, lower priority than the daily-overview indicators.

### 5.3 UI tone

Following the project design brief: reflective Dutch, restrained, warm-earth palette, no alarming patterns. Indicators should describe state, not issue instructions. Examples of the right register:

```
vandaag was matig zwaar
3 zware dagen deze week, jouw mediaan is 1
vandaag was er een acute stresspiek
5 dagen na een dip
```

Examples of the wrong register:

```
CRASH RISK 67%
WAARSCHUWING: rust nemen
je moet vandaag rustig aan doen
```

The first set names. The second set commands and ranks. PAIS patients are exhausted enough; surfaces should *inform* and let the patient interpret.

### 5.4 What NOT to build

Several tempting implementations would actively harm credibility or user experience:

- **A composite "crash risk" percentage**. We do not have a calibrated multi-day predictor. Any single percentage would be either dishonestly precise or trivially the base rate. Even HA07d (the project's first overall-SUPPORTED test at +19.6/+21.7 pp discrimination) has a posterior probability of ~2.3% when its primary arm fires, against a ~1.7% base rate. Discrimination magnitudes ≠ predictive value. Refuse to build until a pre-registered test produces both SUPPORTED-on-held-out AND a posterior-probability ≥ ~20% per fire (which would require much higher discrimination than +22 pp).
- **A red/yellow/green traffic light implying certainty**. Same problem in a different shape. Implies a decision when the underlying evidence is awareness-grade.
- **Push notifications or alerts**. Even well-meaning ones induce anxiety in PAIS patients and crowd the autonomic recovery these indicators are trying to protect. Passive surfaces only.
- **A "recovery score"** in Garmin's house style. Recovery in athletic-training framing means muscular and cardiovascular adaptation. In PAIS framing it means autonomic recharge of an unstable envelope. Conflating them does damage. If a recovery metric is built, it must be PEM-specific and clearly named.
- **An automated daily targets feature**. "Today aim for ≤ 3 000 steps" is a step away from a control-and-shame loop that has hurt many patients in the published literature on activity prescription in ME/CFS. Targets, if any, come from the patient.

---

## 6. Honest caveats

- **n=1 evidence**. Every indicator above was developed against a single participant's data. Transfer to other PAIS individuals is plausible but not demonstrated. The *framework* (baseline-relative, multi-axis, percentile-rank) should transfer; the specific cutoffs almost certainly should not.
- **Era split**. Seven train-era SUPPORTED tests across **six distinct channels** (the sleep-stress channel was tested through three primitives — mean delta, slope, variability — all of which SUPPORTED in train): H02b 3d stress spike, H02d bridge × 5d stress spike, HA06b 4d RHR z-score, HA11 4d U-dip count, HA07c 4d sleep stress mean delta, HA08c 4d sleep stress slope, HA07d 4d sleep stress VARIABILITY delta (also validate-era SUPPORTED). **Honest framing caveat per peer-review §3**: these channels are NOT statistically independent. Body Battery is a fused composite of HR/HRV/stress/sleep; sleep stress is per-minute stress restricted to the sleep window; HA07c/HA08c/HA07d are three primitives of the same channel. The "convergence" should be read as multiple operationalisations of an underlying autonomic-state construct, not as independent samples of nature. **TWO validate-era SUPPORTED tests**: HA07d sleep stress variability lowered direction (PRIMARY anchor, +21.7 pp at primary, +28.5 pp at N_std=2.0, threshold-robust) and HA10 morning BB peak elevated direction (CORROBORATING-BUT-FRAGILE secondary, +16.2 pp at N_std=1.5 only — refuted at N_std=2.0 and 2.5, sits in loose-deviation tail per peer-review §3 fragility diagnosis). Both validate-era anchors are consistent with Wiggers' "freeze" / parasympathetic-swing pattern. **HA07d is the project's first overall-SUPPORTED test under the strict locked rule** and demonstrates the era-as-moderator framing empirically: it SUPPORTS both eras at primary bidirectional, with directional preferences flipping (train: VOLATILITY in either direction; validate: STILLNESS only). Pre-cliff indicators reflect sympathetic-arousal-spectrum + autonomic-volatility patterns; post-cliff indicators reflect parasympathetic-swing + autonomic-stillness patterns.
- **No medical advice**. These indicators are awareness signals. They do not replace clinical assessment, do not prescribe behaviour, and are not validated for clinical use.
- **Pending work**. Sleep-recharge indicators (overnight Body Battery, parasympathetic recovery) are gated on H04b decoding the Garmin `unknown_233` message. Until then, the parasympathetic side of the PAIS picture is not covered by any Tier 1 or Tier 2 indicator.
- **The dataset window ends 2026-06-05**. Anyone re-running the analyses against a later window will find different cutoffs as the rolling baseline shifts.

---

## 7. References

- [docs/research/garmin/hypotheses/registry.md](hypotheses/registry.md) — full registry of pre-registered hypotheses and outcomes
- [docs/research/garmin/hypotheses/crash_v2-definition/](hypotheses/crash_v2-definition/) — the crash and dip definitions used as the dependent variable
- [docs/research/garmin/activity-labels/](activity-labels/) — full spec, sensitivity test, and HA01 / HA01b / HA02 / HA05 test scripts and outputs
- [docs/research/garmin/hypotheses/H02b-stress-spikes/](hypotheses/H02b-stress-spikes/) — the train-era SUPPORTED stress-spike precursor
- [docs/research/RESEARCH-REPORT-ADDENDUM.md](../RESEARCH-REPORT-ADDENDUM.md) §5 — the activity-labels phase narrative
- [docs/research/STOCKTAKE.md](../STOCKTAKE.md) — the running stocktake of what has been tested, supported, refuted, and queued

When ready to convert this into a build, run `/plan-feature` against §3 + §4 + §5 to produce a feature folder under `docs/features/`.
