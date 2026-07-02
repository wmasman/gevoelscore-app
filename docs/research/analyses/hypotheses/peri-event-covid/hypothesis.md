# R23: Peri-event COVID known-event external check, does the overnight autonomic factor visibly move during the 2022-03 infection?

**Pre-registration written 2026-07-02, before any factor value in the
infection window or any comparator window has been inspected. Locked.
Any subsequent change creates an R23v2.**

R23 is the **external-validation check** of the project's overnight
autonomic factor. The corpus contains exactly one independently-dated,
physiologically-unambiguous autonomic event that the participant did not
derive from the biometrics: an acute COVID infection (bed with fever),
dated **2022-03-21 to 2022-04-03** from contemporaneous notes. This
pre-registration tests whether the factor visibly departs from the
pre-COVID healthy baseline during that infection window, in the
literature-predicted direction. It is the strongest available
"ground-truth" test that the factor tracks real autonomic load.

This pre-reg faithfully implements the locked methodology design
[`../../../methodology/peri_event_known_event_check.md`](../../../methodology/peri_event_known_event_check.md)
(decisions a to g, ACCEPT-WITH-MINOR-REVISIONS from the fresh-session
[methodology review](../../../reviews/methodology-peri_event_known_event_check-2026-06-30.md),
M1 / M2 / M5 absorbed) and is backed by the descriptive precondition
[`../../descriptive/peri_event_covid/precondition.md`](../../descriptive/peri_event_covid/precondition.md).

> ## NO-OUTCOME-PEEK LOCK (binding)
>
> R23 is a **pre-registered single-event test**. The pre-registration is
> credible only if the outcome, whether the autonomic factor actually
> MOVED during the infection window relative to baseline, is **unseen**
> when this document locks.
>
> **What HAS been seen, and is fixed here:**
> - The event dates: **2022-03-21 to 2022-04-03**, 14 days inclusive,
>   single event, no reinfection annotated.
> - The window length: **14 days**.
> - Data coverage / non-null counts (row presence only): the anchor
>   `stress_mean_sleep` is present **14 / 14** infection-window days,
>   **31 / 31** March 2022 days, **215 / 217** pre-LC comparator days
>   (99.1%); `bb_highest` **14 / 14**, **216 / 217** (99.5%);
>   `resting_hr` **14 / 14**, **217 / 217** (100%).
> - The factor definition: the Cluster-2 overnight autonomic-state
>   correlational near-identity (effective-N approximately 1).
> - The comparator-window counts: **15** non-overlapping and **204**
>   sliding 14-day windows in the pre-LC band.
> - The resolved anchor: **HA07c `stress_mean_sleep`** (contingency g1
>   satisfied by the coverage check; the HA06b fallback is NOT
>   triggered).
>
> **What has NOT been seen, and MUST stay unseen until this locks:**
> any factor VALUE, mean, median, z-score, percentile, trend, or
> infection-vs-baseline contrast, in the infection window OR in any
> comparator window. No test has been run; no `test.py` has been written
> or executed; the biometric value columns have not been opened for the
> infection window. **Every number above is a row-presence / non-null
> day count, never a channel value.** The infection-vs-baseline contrast
> IS the test; it runs only after this pre-reg locks and is reviewed
> fresh in another session (per
> [CONVENTIONS §1.2 / §3.5](../../../CONVENTIONS.md)).

## Authorship

| Field | Value |
|---|---|
| Drafted by | Claude (Opus 4.8) under reviewer-mode-with-authorization, for the participant-researcher (repo owner) |
| Date | 2026-07-02 |
| Mode | Reviewer-mode pre-registration (per CONVENTIONS §1.2). Drafted from the locked producer-mode methodology MD; to be peer-reviewed by `/research-review` in a fresh session before the test runs. |
| Discipline | No-outcome-peek LOCK (above), no interpretive marks on the descriptive layer (§4.1), stress = Garmin GSS not mental stress (below). |

---

## 1. Claim

During the COVID infection window (**2022-03-21 to 2022-04-03**), the
project's overnight autonomic factor sits at the **high-autonomic-load
pole** relative to the pre-COVID healthy baseline (pre-LC Stratum 1,
2021-08-16 to 2022-03-20), measured at daily-aggregate resolution.

The factor is read primarily through its anchor **HA07c
`stress_mean_sleep`** (the sleep-window mean of Garmin's stress score,
an HRV-derived autonomic-load measure), with a companion triad
readout. The pre-specified directional prediction, per channel, is:

| Channel | Column | Predicted sign during infection |
|---|---|---|
| HA07c anchor | `stress_mean_sleep` | **UP** (overnight stress elevated) |
| HA10 redundant inverse | `bb_highest` | **DOWN** (body-battery suppressed) |
| HA06b peripheral | `resting_hr` | **UP** (resting HR elevated) |

The composite prediction is a coherent move toward the high-load pole:
`stress_mean_sleep` up, `bb_highest` down, `resting_hr` up. The
predicted "MOVED" outcome is that the infection window's factor
statistic lies in this predicted-direction tail of the pre-LC
ordinary-fortnight null (§5, §6).

**Guardrail.** Throughout this document, "stress" means **Garmin's
stress score (an HRV-derived measure)**, computed by Firstbeat from HRV
and heart rate, NOT mental or emotional stress. The Forerunner 245
records no direct HRV channel, so the factor is an HRV *proxy* recovered
through the overnight stress / body-battery / resting-HR triad (per
[`hrv_proxy_via_stress.md`](../../../methodology/hrv_proxy_via_stress.md)).

## 2. Why we think this

Two independent legs justify a pre-specified direction, so this is
**confirmatory, not data-fishing** (CONVENTIONS §4.3):

- **The literature anchor.** An acute febrile viral infection drives a
  sympathetic-dominant, vagally-withdrawn autonomic state that maps
  cleanly onto the three factor channels. The directly-relevant wearable
  infection-detection cohorts report the direction at exactly the
  daily / overnight-aggregate resolution R23 uses: resting HR up,
  HRV down (hence the HRV-derived Garmin stress score up), overnight
  recovery / body-battery down. This is anchored by
  [`../../literature/reviews/acute_viral_infection_autonomic_signature_review.md`](../../literature/reviews/acute_viral_infection_autonomic_signature_review.md)
  (Natarajan 2020 npj Digit Med, the cleanest single statement:
  "respiration rate and heart rate are typically elevated by illness,
  while HRV is decreased"; Mishra/Snyder 2020 Nat Biomed Eng, RHR up vs
  personal baseline at symptom onset; Radin 2020 Lancet Digit Health,
  RHR up from nightly aggregates; Hirten 2021 JMIR, HRV disturbed;
  Mason 2022 TemPredict, RHR up / HRV down / recovery down under a
  controlled vaccination challenge). The RHR-up leg is strong and direct
  in the wearable cohorts; the Garmin-stress-up and body-battery-down
  legs are one inferential step from the validated HRV-down / RHR-up
  inputs those proprietary indices are built on. The literature review
  reads no project data, so the prior is genuinely external.

- **The external-validation logic.** This COVID infection is the single
  **independently-dated** autonomic event in the corpus: dated from
  contemporaneous notes (days in bed with fever, zero training
  activities in week 12), not derived from the biometrics. A signal that
  claims to track autonomic load *should* register the textbook external
  autonomic perturbation. This is therefore the strongest available
  ground-truth check of whether the factor tracks real autonomic load. A
  clean positive banks a ground-truth anchor for the factor; a null
  honestly constrains the factor's sensitivity. Per CONVENTIONS §4.3,
  the pre-registration protects the **outcome** (unseen until lock), not
  the **direction** (which is prior-given by the literature).

## 3. Data sources

- **Per-day series**: `per_day_master.csv` at
  `C:\Users\Gebruiker\Documents\gevoelscore-data\unified\per_day_master.csv`,
  with the `lc_phase` column present across the corona transition.
- **Resolved factor columns** (real `per_day_master.csv` names, per the
  precondition §5.1 coverage resolution):
  - `stress_mean_sleep` (HA07c anchor, the sleep-window Garmin stress
    mean).
  - `bb_highest` (HA10, the daily body-battery peak; the HA10 operand
    per the R18 correction, not "morning_bb_peak" which was a
    descriptive label).
  - `resting_hr` (HA06b).
- **Event dates**: 2022-03-21 to 2022-04-03 (14 days,
  `lc_phase == corona_infection`), CONVENTIONS §5 anchor, confirmed
  against `annotations.yaml` (`label: Corona-infectie`, core symptom
  window 2022-03-23 to 2022-03-30).
- **Comparator band**: the pre-LC healthy era, **2021-08-16 to
  2022-03-20**, 217 days, `lc_phase == pre_corona` (Stratum 1). This is
  the only legitimate "ordinary" comparator: post-infection days are
  LC-era and non-interchangeable with healthy baseline under the L2
  hard-boundary rule.
- **Coverage** (row presence only, no values): confirmed in the
  precondition §3 and §5.1. The anchor and triad are non-null on every
  infection-window day; the comparator band is 99.1 to 100% covered per
  channel, so all 15 non-overlapping and all 204 sliding windows are
  well-populated. See
  [`../../descriptive/peri_event_covid/precondition.md`](../../descriptive/peri_event_covid/precondition.md).

**Factor provenance disclosure (per methodology review M3).** The
factor's defining correlation structure (HA07c to HA10 Spearman
rho = −0.922, HA06b to HA07c rho = +0.377, from
[`../../garmin_exploration/cards/cross-channel-correlation.md`](../../garmin_exploration/cards/cross-channel-correlation.md),
computed on the 2022-09-03 to 2026-06-05 window) is a **fixed instrument
definition**. It is NOT re-fit on the infection window and is not an
infection-vs-baseline contrast; it is a factor-structure property fixed
before this test. The factor is read here using the pre-fixed definition
only.

## 4. Measurement protocol

### 4.1 The factor statistic per window

The factor is a correlational near-identity (effective-N approximately
1), NOT a PCA component or a weighted composite. Per methodology
decision (g), it is read two ways:

- **Primary (g1, single anchor).** The factor value on day `d` is the
  anchor `stress_mean_sleep[d]`, z-scored against the **personal pre-LC
  baseline** using robust location and scale (median + MAD over the
  217-day pre-LC band, per CONVENTIONS §3.1). Call this the daily
  factor-z.
- **Companion (g2, triad coherence).** The per-channel move on each of
  `stress_mean_sleep`, `bb_highest`, `resting_hr` (each z-scored against
  its own personal pre-LC baseline), plus a **coherence flag**: did all
  three move in the predicted signs together (anchor up, `bb_highest`
  down, `resting_hr` up)? **Implementation note** (per review MINOR-2):
  the coherence flag tests each channel against **its own predicted
  sign**, a positive baseline deviation for `stress_mean_sleep` and
  `resting_hr` and a **negative** deviation for the inverse channel
  `bb_highest`, never a uniform "all z positive" test, so `test.py`
  cannot accidentally sign-align the inverse channel. Per CONVENTIONS
  §3.3, HA07c and HA10 are
  rho = −0.92 near-identical, so they are NOT entered as two independent
  witnesses: the coherence readout treats them as one signal viewed
  twice, and the companion is a coherence check, not three independent
  confirmations.

### 4.2 Window aggregation (14-day window statistic)

For any 14-day window, the primary window statistic is the **window mean
of the daily factor-z** over the 14 days (decision g1 + c1). A
**window-max companion** (the max single-day factor-z within the window)
is reported alongside, because a short acute febrile spike inside a
14-day window can be diluted by the 14-day mean (per CONVENTIONS §3.5
and the literature review's daily-aggregate qualification). Note:
"window-max" here means the max over **daily** factor-z, not an intraday
spike count (per methodology review M6); the per-minute intraday version
is deferred to a higher-resolution follow-up (open input, §8).

### 4.3 Aggregation and privacy floor

Per decision (c1), only the **window-level aggregate** (window mean
factor-z, window-max factor-z) and its rank/percentile against the null
are reported. No dated per-day biometric trace is exposed; per-day
values stay internal. This keeps the artefact date-free and aligned with
the publication audit gate.

### 4.4 Acute-core overlay and buffer (descriptive only)

The tighter annotation core **2022-03-23 to 2022-03-30** (symptom/fever
days) is reported as an "acute-core" sensitivity overlay, and a
±7-day descriptive buffer is plotted for context. **Neither the
acute-core overlay nor the buffer enters the primary contrast
statistic** (decision a1); they are presentation, not test. The overlay
carries **no separate p-analogue** (it is not ranked against the E[L]=7
null; purely visual), so no second implicit test is created (per review
MINOR-5).

## 5. The null / comparison

Faithfully implementing the locked design (decisions b2 + d3) as
revised by methodology review **M1** (the naive percentile against the
204 overlapping sliding windows is NOT a valid primary p-value, because
adjacent sliding windows share 13 of 14 days and the empirical
distribution is narrower than 204 independent draws):

- **Primary p-analogue (daily-series stationary bootstrap).** A
  **stationary bootstrap on the daily factor-z series over the 217-day
  pre-LC band**, with expected block length **E[L] = 7 days** (per
  [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)),
  regenerates the null distribution of the **14-day-window-mean
  factor-z** statistic under ordinary healthy variation. **Per-replicate
  mechanic** (locked here to remove a post-lock degree of freedom, per
  review MINOR-1): each bootstrap replicate resamples the daily factor-z
  series under E[L]=7 stationary blocks to a synthetic 217-day series,
  then computes one 14-day-window-mean factor-z from that synthetic
  series; repeating (>= 10,000 replicates) builds the reference
  distribution. The infection window's **percentile within that bootstrap
  distribution** is the p-analogue. This uses all 217 healthy days and
  respects within-window autocorrelation by construction. Before locking
  the inference, confirm the data-driven E[L]* does not deviate by more
  than 2x from 7.

- **Transparent sanity check (n=15 non-overlapping windows).** The rank
  of the infection window among the **15 genuinely independent
  non-overlapping** 14-day pre-LC windows is reported alongside (per
  CONVENTIONS §3.6 named-count discipline): *15 independent
  non-overlapping 14-day pre-LC windows (per_day_master.csv,
  `lc_phase == pre_corona`, 2021-08-16 to 2022-03-20)*.

- **Descriptive density backdrop (204 sliding windows).** The 204
  sliding 14-day pre-LC windows (step 1 day) are used **only** as a
  descriptive "shape of ordinary fortnights" visual. They are **never**
  a p-value denominator (this is the M1 fix: no naive percentile against
  the 204 overlapping windows is used as the primary inference).

- **Effect size (d2).** The stationary-bootstrap E[L]=7 CI on the
  standardised difference (infection-window mean vs pooled pre-LC
  baseline), from the same bootstrap machinery, so one null model serves
  both the p-analogue and the CI. Direction + magnitude are always
  reported alongside any p-analogue, never the p alone (CONVENTIONS
  §3.7 / A7).

- **Detrend sensitivity column (§3.7).** Carried as a belt-and-braces
  sensitivity even though pre-LC baseline-trajectory leak is expected
  negligible (the pre-LC band is flat healthy, not an LC recovery
  trajectory). Note the §3.7 audit-hook fires on the **raw** channels in
  the g2 triad companion, not on the z-scored primary (whose scope §3.7
  excludes); it is applied there (per methodology review M6).

**Baseline reference.** All z-scores use the personal pre-LC baseline
(median + MAD, robust, CONVENTIONS §3.1). No absolute cutoff is used as
the classification gate; the classification is a percentile against the
null.

## 6. Pre-registered falsification criterion (TIERED)

Implementing decision (e3) exactly. The predicted direction is the
**high-autonomic-load pole** (§1, §2). Let the infection window's
primary statistic be its window-mean factor-z, and let its percentile be
read against the primary p-analogue (the daily-series stationary-
bootstrap null of §5). The direction is oriented so that the high-load
pole is the **predicted-direction tail** (anchor `stress_mean_sleep`
elevated).

| Tier | Condition | Meaning |
|---|---|---|
| **MOVED** | Infection window lies **beyond the 95th percentile** of the null distribution **in the predicted direction** (high-load pole: `stress_mean_sleep` elevated), one-sided | The factor **visibly moved** as physiology predicts. This is the supported outcome. |
| **AMBIGUOUS** | Infection window lies **inside the band** (below the predicted-direction 95th percentile and above the opposite-direction 5th percentile) | The factor did **not** visibly depart from the ordinary-fortnight distribution at the 14-day aggregate resolution. This is the null tier, and it is publishable. |
| **MOVED-UNEXPECTED-DIRECTION** | Infection window lies **beyond the 5th percentile in the opposite direction** (low-load pole) | A blunted / decoupled reading in the direction opposite the prediction. This tier is a **guard** against a severity-gated blunting (see §8), NOT a predicted outcome. |

The predicted-direction tail and the 95th-percentile threshold are
**locked here, before the look**. The high-load pole is the predicted
outcome; the `MOVED-UNEXPECTED-DIRECTION` tier exists only because the
literature warns (severity-gated, moderate) that a derived index can
flatten or decouple at the deepest point of extreme inflammation, so an
opposite-direction result is informative rather than a non-result.

"Visibly moving" = the **MOVED** tier. The factor "does not visibly
move" = the **AMBIGUOUS** tier.

## 7. Predicted direction + effect size

- **Direction (per channel, high-load pole):** `stress_mean_sleep`
  **UP**, `bb_highest` **DOWN**, `resting_hr` **UP** (§1 table). The
  coherence flag is expected to fire (all three in the predicted signs).
- **Magnitude if true.** If the factor tracks the infection, the
  infection window's window-mean factor-z is expected to sit clearly in
  the predicted-direction tail (beyond the 95th percentile of ordinary
  pre-LC fortnights), and the window-max factor-z may exceed the window
  mean, because the acute febrile phase is a short spike inside the
  14-day window. The RHR leg is expected to be the strongest and most
  direct (it is the directly-validated wearable channel); the
  Garmin-stress-up and body-battery-down legs are one inferential step
  from the RHR/HRV inputs and are expected to move coherently with it.
- The stationary-bootstrap E[L]=7 CI on the standardised difference is
  expected to exclude zero in the predicted direction if the factor
  moves.

## 8. Caveats result.md must carry

`result.md` must explicitly acknowledge all of the following:

- **(a) Acute-infection vs LC-onset inseparability (methodology review
  M5).** The infection window (2022-03-21 to 2022-04-03) sits on the
  Stratum-1 to Stratum-2 boundary and abuts LC onset
  (`LC_ERA_START = 2022-04-04`, the day after the window's close). The
  acute infection and the *beginning of the persistent LC autonomic
  shift* are temporally adjacent and **cannot be separated by this
  single-event design**. A MOVED result must be reported as "the factor
  departed baseline around the infection / LC-onset hinge," never as
  "the acute infection caused the factor to move." The window-tail
  signal especially cannot be attributed to the acute phase alone.
- **(b) Stress = Garmin's stress score (an HRV-derived measure), not
  mental stress.** All "stress" language refers to the Firstbeat
  HRV-derived Garmin GSS, not mental or emotional stress.
- **(c) The Forerunner 245 records no direct HRV.** The factor is an
  HRV *proxy* recovered via the overnight stress / body-battery / RHR
  triad. The Garmin-stress-up and body-battery-down legs are one
  inferential step beyond the directly-validated RHR/HRV inputs; the
  strongest *direct* channel is `resting_hr`. Cited device generation
  differs from the wearable cohorts (Fitbit / Apple Watch / Oura): the
  direction generalises, the exact magnitude/calibration does not.
- **(d) n=1, single event.** This validates that the factor **tracks
  autonomic load** on the one available known event; it does **NOT**
  establish crash-precursor value, and one event cannot separate "the
  factor tracks infection" from "the factor happened to move that
  fortnight." The reach is bounded to "this signal, this subject, this
  one event."
- **(e) The factor is correlational (effective-N approximately 1), not a
  variance-decomposition construct.** No variance-explained percentage
  is defined; the factor is the correlational near-identity of the
  channels. HA07c and HA10 (rho = −0.92) are one signal viewed twice,
  not two independent witnesses (CONVENTIONS §3.3).
- **(f) Severity characterisation (methodology review M4).** The event
  is home-recovered and febrile (days in bed with fever, zero training
  activities in week 12), not hospitalised. This is the severity anchor
  that justifies down-weighting the blunting caveat to moderate: the
  blunting evidence (Gholami 2012 rat endotoxemia; de Castilho 2017 ICU
  sepsis) is severity-gated, so the `MOVED-UNEXPECTED-DIRECTION` tier is
  a guard, not a prediction.
- **(g) No causal / interpretive marks on the descriptive layer
  (§4.1).** The claim is "the factor did / did not depart from baseline
  around the event," never "the infection caused the factor to move."

## 9. What we do with each outcome

- **MOVED (supported)** → the factor departed baseline toward the
  high-load pole in the one available known autonomic event. This is
  **external validation that the factor tracks real autonomic load**,
  and it **banks a ground-truth anchor** for the factor. Report the
  percentile / CI plainly, report the triad-coherence flag, and carry
  caveat (a): the departure is around the infection / LC-onset hinge and
  cannot be attributed to the acute phase alone. It does NOT establish
  crash-precursor value (caveat d).
- **AMBIGUOUS (null)** → the infection fortnight's factor value was
  within the ordinary-fortnight band; the factor did **not** visibly
  depart from baseline at the 14-day aggregate resolution. This is a
  **publishable Layer-1 finding**: it constrains the factor's
  sensitivity. The factor's autonomic-tracking claim is **not
  corroborated** by the one available known event, reported honestly. It
  must (i) state the percentile / CI plainly, (ii) avoid any
  "absence of evidence = evidence of absence" overclaim, (iii) log the
  higher-resolution follow-ups that could detect a move the daily
  aggregate misses (per-minute intraday extraction for the acute-core
  window; the window-max spike view), and (iv) keep the reach bound.
- **MOVED-UNEXPECTED-DIRECTION (blunted / ambiguous middle)** → the
  factor departed baseline in the direction **opposite** the prediction.
  Report as a possible severity-gated blunting / decoupling of the
  derived index (caveat f), not as a true autonomic reversal, and treat
  it as the documented minority tail the tiered criterion exists to
  catch, not as a clean corroboration of the tracking claim.

---

*Pre-registration locked 2026-07-02 before any factor value in the
infection window or any comparator window was inspected. Faithfully
implements the locked methodology
[`../../../methodology/peri_event_known_event_check.md`](../../../methodology/peri_event_known_event_check.md)
(decisions a to g; M1 percentile-null re-spec, M2 anchor-contingency
resolved to HA07c, M5 acute-vs-LC-onset inseparability). Anchor:
HA07c `stress_mean_sleep` (contingency g1 satisfied; HA06b fallback not
triggered).*

*Lock log: fresh-session peer review
[`../../../reviews/hypothesis-peri-event-covid-2026-07-02.md`](../../../reviews/hypothesis-peri-event-covid-2026-07-02.md)
returned ACCEPT-WITH-MINOR-REVISIONS, NO-OUTCOME-PEEK HELD, 0 BLOCKING /
0 MAJOR. Revisions MINOR-1 (bootstrap per-replicate mechanic, §5),
MINOR-2 (g2 inverse-channel sign convention, §4.1), and MINOR-5 (§4.4
overlay carries no separate p-analogue) absorbed 2026-07-02. MINOR-3 /
MINOR-4 confirmed already-present; NIT-1 (data path) waived (matches
corpus convention, does not trip the publication audit). **LOCKED
2026-07-02.** Any change creates an R23v2. `test.py` may now be written
and run.*
