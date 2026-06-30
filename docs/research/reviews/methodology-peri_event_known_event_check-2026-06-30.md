# Methodology review — `peri_event_known_event_check.md` (R23)

**Target**: [`../methodology/peri_event_known_event_check.md`](../methodology/peri_event_known_event_check.md)
(R23 — peri-event known-event check: does the watch's autonomic factor
move during the ~14-day 2022-03 COVID infection?)
**Review date**: 2026-06-30
**Reviewer**: Claude (Opus 4.8, 1M context). **Fresh session — no
exposure to the drafting context; doc-only knowledge.** Independent
methodology peer-review gate per
[CONVENTIONS §2.2](../CONVENTIONS.md) +
[reviews/README.md](README.md) (methodology-MD branch, four-input bar +
applicable 4-layer items).
**Mode**: producer-mode methodology-MD review (the MD is upstream-of-
verdict infrastructure per CONVENTIONS §1.1; the pre-registration it
specifies is the separate reviewer-mode artefact).
**Verdict tiers used**: DEFENSIBLE / DEFENSIBLE-WITH-REVISION / REVISIT
(per the methodology-review spine), mapped to the prompt's
ACCEPT / ACCEPT-WITH-MINOR-REVISIONS / REVISION-RECOMMENDED / REJECT.

---

## Verdict

**ACCEPT-WITH-MINOR-REVISIONS** (= DEFENSIBLE-WITH-REVISION).

The design is unusually disciplined for a single-event pre-registration.
The no-outcome-peek contract holds across both documents; the
predicted-direction anchor survives scrutiny and is honestly tiered; the
factor definition and definitional-pair handling are correct. Three
items must be tightened **before the pre-reg is drafted** — none are
fatal, but two of them (M1 the between-window-autocorrelation gap in the
percentile null, and M2 the open-input #1 primitive-presence
confirmation that gates the whole factor choice) are load-bearing for
the test that follows. The rest are clarity/wording revisions.

---

## 1. What the document proposes (plain restatement)

R23 will, *after* a separate pre-reg locks, ask whether the project's
"autonomic factor" (an overnight Garmin GSS / body-battery / resting-HR
correlational cluster) departed from the subject's pre-LC healthy
baseline during the known 2022-03-21→04-03 COVID infection, in the
literature-predicted direction (high-autonomic-load pole). The MD does
not run that test; it locks the design space: window (a1 14-day primary
+ a2 acute-core overlay + buffer), comparator (b2 matched sliding 14-day
pre-LC windows as the placebo null + b1 full-band baseline as the
frame), aggregation (c1 window-level, date-free), statistic/null (d3 =
matched-window percentile + stationary-bootstrap E[L]=7 CI on the
standardised diff + §3.7 detrend column), criterion (e3 tiered MOVED /
AMBIGUOUS / MOVED-UNEXPECTED with predicted direction pre-given),
null-reporting (f1 publishable AMBIGUOUS), and factor operationalisation
(g1 HA07c anchor primary + g2 triad-coherence companion). The empirical
claim under test is descriptive Layer-1 ("the factor did / did not
depart"), explicitly not causal.

---

## 2. The five PUSH-HARDEST items (verdict per item)

### 2.1 No-outcome-peek contract — HELD (airtight across both docs)

This is the single most important check and it passes.

- The MD carries the binding contract at lines 18-28 and enumerates
  exactly what it characterises (event dates, window length,
  coverage/missingness, computability, factor definition, candidate
  comparison set + count) and what it does **not** (compute, estimate,
  plot, or infer the infection-vs-baseline contrast). The contrast is
  correctly named as *the test itself*, deferred to post-lock
  (MD:9-12, 24-27).
- The precondition carries the *same* contract verbatim-in-spirit
  ([precondition.md:14-31](../analyses/descriptive/peri_event_covid/precondition.md)),
  and — critically — adds the stronger sentence *"No biometric values,
  means, trends, z-scores, or infection-vs-baseline contrasts were
  inspected or computed in producing this document"* (precondition:24-26)
  and the rule *"Every coverage number below is a row-presence /
  non-null day count — never a channel value"* (precondition:30-31).
- I audited every quantitative statement in the precondition for a
  value leak. **§3 coverage tables (precondition:121-140)** report only
  `14/14`, `31/31`, `30/30` day-presence counts — no channel value, no
  mean, no z. **§4 (precondition:142-171)** reports only window *counts*
  (15 non-overlapping, 204 sliding) and per-channel *presence density*
  (217/217, 216/217) — again no value. The pre-LC density numbers are
  coverage, not contrast.
- The MD's §3 summary (MD:124-144) re-states only these presence/count
  facts. No infection-vs-baseline quantity appears anywhere in either
  doc.
- The literature anchor explicitly reads no project data
  ([acute review:80, 99](../literature/reviews/acute_viral_infection_autonomic_signature_review.md))
  and fixes direction from population literature only — so the prior is
  genuinely external (CONVENTIONS §4.3 test 2 satisfied independently of
  the corpus).

**One residual peek-surface to close (minor, → M3).** The §2 factor
definition cites the cross-channel card, whose ρ values
(HA07c↔HA10 = −0.922, HA06b↔HA07c = +0.377) are
[computed on the 2022-09-03 → 2026-06-05 window](../analyses/garmin_exploration/cards/cross-channel-correlation.md)
(card:28, 34-42) — i.e. **LC-era data, which post-dates the infection
and overlaps the test era**. This is not an outcome peek (the ρ values
are a *factor-structure* property, not the infection-vs-baseline
contrast, and they were established 2026-06-08 for an unrelated
peer-review action), and using a structurally-defined factor whose
internal correlations were measured on later data does not leak the R23
*outcome*. But the pre-reg should state explicitly that the factor's
definitional ρ structure is fixed from the cross-channel card's LC-era
window and is treated as a *fixed instrument definition*, not re-fit on
the infection window — so a future reader cannot mistake the
factor-structure provenance for a baseline contrast. This is a
one-sentence disclosure, not a design change.

**Contract verdict: HELD.** No place was found where an
infection-vs-baseline result could have leaked into either document.

### 2.2 Predicted-direction anchor (decision e + §6) — SURVIVES

The anchor is correctly grounded and, importantly, honestly hedged.

- **Direction is correctly sourced.** §6 (MD:358-399) maps each channel
  to the literature: RHR↑ (HA06b), HRV↓ → GSS↑ (HA07c), body-battery↓
  (HA10). This matches the acute review's RQ1 table
  ([acute review:15-21](../literature/reviews/acute_viral_infection_autonomic_signature_review.md))
  channel-for-channel, including the strength gradations (RHR strong /
  direct; GSS moderate-strong / one inferential step; BB moderate /
  inferred).
- **The "one inferential step" is flagged, not asserted as direct
  evidence.** MD:376-378 states the GSS-up and body-battery-down legs
  are *"one inferential step from the validated HRV↓/RHR↑ inputs"* — and
  §6's honest-limits equivalent in the review (acute review:77) says the
  same. This is the correct epistemic posture: the *directly* validated
  channel is RHR; the derived Garmin indices inherit the direction by
  construction, and the MD says so rather than laundering the inference.
  This is exactly the §4.2 caveat-vs-a-priori discipline applied
  correctly — the inferential gap is disclosed as a caveat, not hidden.
- **Blunting is treated as a guard, not a prediction.** MD:390-399
  states the `MOVED-UNEXPECTED-DIRECTION` tier is *"a guard against a
  blunted/decoupled reading, not a predicted outcome; the predicted
  direction stays the high-load pole."* This is faithful to the review,
  which is explicit that the blunting evidence is sepsis/ICU-tier
  (Gholami endotoxemia rat model; de Castilho ICU sepsis) and therefore
  a **moderate** caveat that licenses the *possibility* of inversion,
  not a prediction of it
  ([acute review:53, 60-64, 79](../literature/reviews/acute_viral_infection_autonomic_signature_review.md)).
  The MD does not over-weight it. Good.
- **CONVENTIONS §4.3 (prior-driven = confirmatory) is correctly
  invoked** (MD:60-72): the three §4.3 tests are each independently
  satisfied (lived-through dates from contemporaneous notes; external
  literature; mechanistic argument), so confirmatory framing of a
  pre-specified direction is justified, and the MD correctly says the
  pre-reg discipline protects the *outcome*, not the *direction*.

**One precision fix (minor, → M4).** §6 and the review repeatedly frame
the infection as "mild-to-moderate / home-recovered"
(acute review:53, 61, 79) to justify down-weighting blunting. The MD
inherits this framing implicitly but never states the *severity
evidence* for this specific case. The precondition's annotation —
*"een aantal dagen op bed met koorts ... 0 training-activities in week
12"* (precondition:41-43) — is the only severity anchor, and it is
consistent with "home-recovered, febrile but not hospitalised." The
pre-reg should carry that one-line severity characterisation explicitly
where it leans on the "blunting is only a moderate caveat" argument, so
the down-weighting is auditable rather than assumed. (This is a
descriptive note about the event, not an outcome peek.)

**Anchor verdict: SURVIVES.** The high-load-pole direction is correctly
grounded, the one-inferential-step gap is honestly flagged, and the
tiered criterion's treatment of blunting as guard-not-prediction is
sound given the severity-gated evidence.

### 2.3 Factor definition (decision g) — COHERENT, §3.3 correctly applied

- The factor is correctly identified as **Cluster 2** from the
  cross-channel card, *not* a PCA PC1 and *not* a weighted composite
  (MD:74-96; card:19). The triad HA07c + HA10 + HA06b is faithfully
  transcribed, including the ρ values
  (HA07c↔HA10 = −0.922, HA06b↔HA07c = +0.377, HA06b↔HA10 = −0.393),
  which match the card's Spearman matrix exactly (card:48-54).
- **The cohort_topology mis-citation in the R23 register is caught and
  corrected** (MD:98-116; precondition:86-104), with the correction
  cross-checked against `clusters-export.md`'s prior record of the same
  fix. This is exactly the kind of provenance error a fresh review
  exists to catch, and it was caught by the producer before this gate —
  good hygiene.
- **§3.3 (one column per definitional pair) is correctly applied.**
  MD:351-356 states HA07c and HA10 are ρ=−0.92 near-identical and *"are
  not both entered as independent evidence — the coherence readout
  treats them as one signal viewed twice."* This is the correct reading
  of §3.3: HA07c and HA10 are not independent witnesses. The g2
  triad-coherence companion is therefore framed as a *coherence check*
  (do the three move in the predicted signs together?), not as three
  independent confirmations — which is the only §3.3-safe way to report
  a triad where two members are ρ=−0.92.
- **g1 (HA07c single anchor) as primary + g2 (triad coherence) as
  companion** is internally coherent: the primary statistic is one
  signal (clean null), and the companion is explicitly a
  not-independent coherence readout. No double-counting.

**One caveat the pre-reg must carry (minor, → M2 dependency).** g1
*requires* `sleep_stress_mean` (HA07c) to be non-null at the overnight-
primitive level in 2022-03, which is **open input #1** and currently
**unconfirmed** (see 2.6 below). If #1 fails, the fallback is HA06b
`resting_hr` as primary anchor (MD:424; precondition:177) — which is
*better* on direct-evidence grounds (RHR is the strongest, most directly
validated channel per the acute review) but *changes the factor's
center of gravity* from the HRV-derived overnight index to the RHR
channel. The pre-reg must lock g1-vs-fallback as a pre-specified
contingency keyed to the #1 result, **not** choose it after seeing
which primitive is present — otherwise the anchor choice becomes a
researcher-degree-of-freedom. Flag this as a pre-registered conditional.

**Factor verdict: COHERENT.** §3.3 correctly applied; the only open
thread is the #1-gated anchor contingency.

### 2.4 Comparison / null design (b + d) — MOSTLY SOUND, one real gap (M1)

This is where the design needs the most work before lock.

- **The matched sliding-window placebo null (b2) is the right
  single-event analogue.** Asking "is the infection fortnight extreme
  relative to the distribution of ordinary healthy fortnights this body
  produced" is the honest framing, and using the pre-LC Stratum-1 band
  as the *only* legitimate comparator is correct under the L2
  hard-boundary rule (post-infection days are LC-era and
  non-interchangeable). b1 (full-band baseline) as the z-reference per
  §3.1 is correctly subordinated to the descriptive frame.
- **§3.6 named-count discipline is correctly applied.** Reporting the
  null distribution as n≈204 sliding but reporting **n=15
  non-overlapping** as the count of genuinely independent placements
  (MD:226, 262-272; precondition:153, 168-171) is the right call:
  consecutive sliding windows are autocorrelated, and 15 is the honest
  independent-placement count. The phrasing names scheme + unit + source
  (precondition:168-171). Good.

- **M1 — THE REAL GAP: the between-window autocorrelation of the 204
  sliding windows is not actually handled by the stated machinery, and
  the MD asserts it is.** MD:166 and MD:260 say sliding-window
  autocorrelation is "handled by block/window resampling" and the
  stationary-bootstrap E[L]=7. **These are two different null objects
  and the E[L]=7 bootstrap does not discipline the percentile null.**
  - The **percentile null (d1)** is: compute the window statistic over
    each of the 204 sliding placements, then read the infection window's
    rank/percentile against that empirical distribution. The 204 values
    are **not independent** — adjacent windows share 13 of 14 days — so
    the empirical distribution is *narrower and lumpier* than 204
    independent draws would be, and a naive percentile against it
    **understates the tail** (over-states extremity). The MD's §4.1
    claim that window-shuffle "preserves within-window autocorrelation
    by construction" (MD:163-166) is true but addresses the *wrong*
    autocorrelation: within-window structure is preserved, but
    *between-window* dependence among the 204 placements is what biases
    the percentile.
  - The **stationary-bootstrap E[L]=7 (d2)** is a CI on the
    *standardised difference* (infection mean vs pooled baseline) — a
    different statistic with a different null. It does not fix the
    percentile-null's between-window dependence.
  - **What must change before lock:** the pre-reg must state how the
    percentile p-analogue accounts for between-window dependence. Two
    defensible routes: (i) **report the percentile against the n=15
    non-overlapping windows as the primary p-analogue** (independent by
    construction; the 204-sliding distribution becomes a descriptive
    "shape of ordinary fortnights" visual only), or (ii) keep the
    204-sliding percentile but compute its calibration via a
    **block/stationary-bootstrap over the daily series** that
    regenerates synthetic 217-day baselines and recomputes the full
    sliding-window distribution per resample, so the null accounts for
    the dependence. Route (i) is simpler and is what §3.6 already
    gestures at; route (ii) is the E[L]=7-consistent version but is more
    work. The MD currently implies the machinery is settled when it
    conflates the two nulls — that conflation must be resolved in the
    pre-reg, with the chosen route named. **This is the one substantive
    statistical revision.**
  - Note this does not require new homework in the §2.2 sense (no new
    methodology MD): it is a clarification/selection between two
    routes the project already owns (n=15 independent count per §3.6,
    and the stationary bootstrap per `permutation_null_block_length.md`).
    But it must be *decided and named* in the pre-reg, not left as the
    current "handled by block/window resampling" hand-wave.

- **E[L]\* confirmation is correctly required.** MD:306 carries the
  `permutation_null_block_length.md` rule that the data-driven E[L]*
  must not deviate >2× from 7 before locking (matching that MD's:23-24
  policy). Good — but note this E[L]* check belongs to the *daily-series*
  bootstrap, which only becomes the percentile-null engine under route
  (ii); under route (i) the E[L]=7 bootstrap applies only to the d2
  standardised-difference CI. The pre-reg should be clear which
  statistic E[L]=7 governs.

**Comparison/null verdict: MOSTLY SOUND** with one required revision
(M1) — the percentile-null's between-window dependence is asserted
handled but is not, and the route must be named before lock.

### 2.5 §3.7 detrend / §3.5 spike-window-max / §3.1 personal-baseline — correctly applied

- **§3.1 personal baseline.** The factor is z-scored against the
  personal pre-LC median+MAD baseline (MD:272, 293; d1). This is the
  §3.1 prescription (median+MAD, robust). Correct. The "lock z-thresholds
  across the same values, let the baseline personalise" rule is
  respected (no absolute cutoff is used as the classification gate; the
  cut is a percentile against the matched-window null).
- **§3.5 spike / window-max companion.** MD:283-287 and MD:386-389 carry
  the window-max single-day-z companion alongside the window-mean,
  explicitly because a short acute spike inside a 14-day window can be
  mean-diluted — which is exactly the §3.5 rationale and exactly what the
  acute review's RQ2 qualification warns about
  (acute review:42-47). Correctly applied and well-motivated. (Caveat:
  the §3.5 prototypes are *minutes-with-stress≥75* / *max-HR-sample* type
  intraday metrics; here the "window-max" is a max over *daily*
  factor-z, which is the coarser daily-aggregate analogue. That is the
  right thing at daily resolution and the per-minute version is correctly
  deferred to open-input #4 as a higher-resolution follow-up — MD:427.
  The pre-reg should just be explicit that "window-max" = max daily-z,
  not an intraday spike count, to avoid conflation with the §3.5
  prototypes.)
- **§3.7 detrend sensitivity.** MD:168-171, 304-306 carry the detrend
  column even though pre-LC baseline-trajectory leak is expected
  negligible (the recovery trajectory that §3.7 worries about is an
  LC-era phenomenon; the pre-LC band is flat healthy). The MD's
  reasoning is correct — §3.7's worked example shows the column catching
  real trajectory artefacts, and carrying it cheaply here is the
  disciplined default even when leak-risk is low. Note: §3.7 *as written*
  applies to **raw** pre-vs-post comparisons, and explicitly does NOT
  apply to lagged-baseline z-scores (CONVENTIONS §3.7 scope). R23's
  primary statistic is a **z-score against the personal baseline**, which
  is closer to the "does NOT apply" branch. The MD is not wrong to carry
  the column as a belt-and-braces sensitivity, but the pre-reg should
  note that §3.7's audit-hook *fire* is really aimed at the raw-channel
  triad-coherence companion (g2 reports per-channel moves, some of which
  may be raw), and apply the detrend there rather than implying it is
  mandatory on the z-scored primary. Minor clarity, not a defect.

**Verdict: correctly applied**, with one wording clarification on §3.7
scope and one on §3.5 "window-max" semantics.

### 2.6 Era / L2 limitation — adequately carried, with one tightening

- The infection-at-the-Stratum-1→2-boundary fact and the pre-LC-only
  comparator are correctly and repeatedly carried (MD:198-211, 244;
  precondition:50-54, 144-149). The L2 hard-boundary rule (post-infection
  = LC-era, non-interchangeable) is the reason the comparator is
  Stratum-1-only, and both docs state this.
- **The "infection window is also LC-onset" interpretive caveat** is the
  subtle one. The corpus anchors LC onset at 2022-04-04, *immediately
  after* the infection window's close (2022-04-03). So the infection
  window is not merely *adjacent to* the era boundary — it is the
  putative **causal origin** of the LC era. The MD acknowledges the
  boundary position (MD:200-204) but does **not** explicitly carry the
  interpretive caveat that **a "MOVED" result cannot distinguish "the
  factor tracks the acute infection" from "the factor is registering the
  beginning of the persistent LC autonomic shift that starts in this
  same window."** The acute review even flags that the *chronic*
  post-COVID HRV literature describes a persistent shift (acute
  review:19-20, Marques/Mooren/Suh as secondary context) — so the acute
  and chronic-onset signals are temporally inseparable in this single
  window. **This belongs in the pre-reg's limitations as a named
  interpretive caveat (→ M5):** R23 can say "the factor departed from
  healthy baseline in this window," but cannot attribute the departure
  to the acute infection *as distinct from* LC onset, because the two
  begin in the same fortnight. This does not weaken the design (the
  Layer-1 descriptive claim is unaffected), but the interpretation
  section must not let a reader slide from "moved during the infection"
  to "the acute infection moved it."

**Era/L2 verdict: adequately carried at the boundary-position level;
the acute-vs-LC-onset inseparability caveat must be added explicitly.**

---

## 3. Four-input bar (CONVENTIONS §2.2) — all four present

- **Best-practices standards (§4.1):** single-event ITS framing, N-of-1
  standards (CENT/SCRIBE/Daza/WWC) correctly bounded to within-subject
  reach, stationary-bootstrap default inherited. Present and sound.
- **Established literature (§4.2 + §6):** the acute-infection anchor is
  cited where it *materially* fixes the direction (not "they did it that
  way"), each citation earns its place, and the inferential gap on the
  derived indices is disclosed. This is the strongest section. Present.
- **Tradeoff vision (§4.3):** "defensibility + publishable null over
  power," explicitly weighted, with the single-event over-claim risk
  named. Present.
- **Limitations + objectives (§4.4):** L1/L2/L3/L7 each mapped, objective
  bounded to Layer-1 descriptive with no causal mark. Present — and the
  M5 acute-vs-LC-onset caveat is the one addition this section needs.

All four inputs are genuinely reasoned, not box-ticked. The §2.2 bar is
met.

---

## 4. What does not fire (selective)

- **Data-peeking (§4.3):** does not fire. Prior is independently
  established on all three tests; the outcome is unseen. Confirmatory
  framing is justified.
- **§3.2 lagged-baseline:** not applicable — this is a peri-event
  departure check against a fixed pre-LC baseline, not a sustained-push
  exertion test. Correctly not invoked.
- **§3.4 crash-drop sensitivity:** not applicable — no crash-day frame
  enters a single-event infection-window contrast. Correctly absent.
- **§3.8 boundary-spacing / §3.9 curated-catalog:** not applicable —
  single event, single annotated span, no multi-boundary sweep and no
  heterogeneous-category pull. Correctly absent.

---

## 5. Required changes before the pre-reg locks

| # | Severity | Item | Where |
|---|---|---|---|
| **M1** | **Substantive (must fix)** | The percentile-null's **between-window** autocorrelation (204 sliding windows share 13/14 days) is asserted "handled" but the E[L]=7 bootstrap addresses a different null (the d2 standardised-difference CI). Name the route: (i) percentile against the **n=15 non-overlapping** windows as the primary p-analogue (204-sliding = descriptive visual only), or (ii) a daily-series stationary bootstrap that regenerates the full sliding distribution per resample. Resolve the d1/d2 conflation. | MD:163-166, 226, 260, 293 |
| **M2** | **Substantive (must fix)** | Open-input #1 (overnight-primitive non-null in 2022-03) is **unconfirmed** and gates g1. Lock g1-vs-HA06b-fallback as a **pre-specified contingency keyed to the #1 result**, decided before the look — not chosen after seeing which primitive is present. | MD:344, 424; precondition:177 |
| **M3** | Minor (disclosure) | State explicitly that the factor's defining ρ structure is fixed from the cross-channel card's LC-era window (2022-09→2026-06) and treated as a **fixed instrument definition**, not re-fit on the infection window. Closes a provenance-vs-peek ambiguity. | MD:74-96; card:28 |
| **M4** | Minor (disclosure) | Carry a one-line **severity characterisation** of the event ("home-recovered, febrile, days-in-bed, 0 training week 12") where the design leans on "blunting is only a moderate caveat," so the down-weighting is auditable. | MD:390-399; precondition:41-43 |
| **M5** | Minor (limitations) | Add the **acute-vs-LC-onset inseparability** interpretive caveat: a MOVED result cannot distinguish "tracks the acute infection" from "registers LC onset," because LC begins (2022-04-04) in the same window. Belongs in the pre-reg limitations + interpretation sections. | MD:198-211 |
| **M6** | Trivial (wording) | Clarify (a) "window-max" = max **daily** factor-z, not an intraday §3.5 spike count; and (b) §3.7's audit-hook fires on the **raw** channels in the g2 companion, not on the z-scored primary (§3.7 scope excludes lagged-z). | MD:283-287, 304-306 |

None of M1-M6 require a new §2.2 methodology MD; all are decidable
within the existing methodology corpus. M1 and M2 must be resolved in
the pre-reg text itself; M3-M6 are disclosure/wording additions.

---

## 6. Verdict + one-sentence reasoning

**ACCEPT-WITH-MINOR-REVISIONS (DEFENSIBLE-WITH-REVISION).** The
no-outcome-peek contract holds airtight across both the MD and the
precondition, the predicted-direction anchor is correctly grounded and
honestly hedged (one-inferential-step flagged, blunting treated as guard
not prediction), and §3.3/§3.5/§3.7/§3.1 are correctly applied; the one
substantive fix is M1 (the percentile null asserts it handles
between-window autocorrelation but the stated E[L]=7 machinery addresses
a different null — the route must be named before lock), with M2 (the
#1-gated anchor contingency must be pre-specified) close behind, and
M3-M6 as disclosure/wording tightening. The highest-priority concern is
Layer-3 (time-series autocorrelation handling, M1).
