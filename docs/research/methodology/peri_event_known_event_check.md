# Peri-event known-event check — proposed methodology (R23)

**Status**: **DESIGN READY FOR FINAL LOCK — user-accepted + methodology
review absorbed (2026-06-30).** Both gates cleared: user locked the
design forks (§5 "Locked decisions"); the fresh-session
[`/research-methodology-review`](../reviews/methodology-peri_event_known_event_check-2026-06-30.md)
returned ACCEPT-WITH-MINOR-REVISIONS (no-outcome-peek HELD;
predicted-direction anchor SURVIVES) and its M1/M2/M5 fixes are absorbed
(see §10 lock log). Drafted producer-mode, STAGE 1 scoping for site
request **R23**: *does the watch's autonomic factor visibly move during the
~14-day COVID infection?* It still does **not** run the test — the
infection-vs-baseline contrast runs only after the **pre-registration**
(a separate reviewer-mode artefact, drafted citing this MD, reviewed fresh
in another session) locks per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.5 hard rule + [CONVENTIONS §1.2](../CONVENTIONS.md). **Next: draft the
pre-registration.**

> **NO-OUTCOME-PEEK CONTRACT (binding).** R23 is a pre-registered
> single-event test. Pre-registration is only credible if the outcome
> is unseen when the design locks. This MD characterises *event dates,
> window length, data coverage/missingness, factor computability, the
> factor definition, and the candidate comparison-window set + count*.
> It does **not** compute, estimate, plot, or infer whether the
> autonomic factor actually moved during the infection vs baseline.
> The infection-vs-baseline contrast IS the test; it runs only after
> the pre-reg locks. The descriptive precondition backing this MD is
> [`../analyses/descriptive/peri_event_covid/precondition.md`](../analyses/descriptive/peri_event_covid/precondition.md),
> which carries the same contract.

## Authorship

| Field | Value |
|---|---|
| Drafted by | Claude (Opus 4.8, 1M context), producer-mode STAGE-1 scoping session |
| Authorising user | the participant-researcher (repo owner) |
| Date | 2026-06-30 |
| Mode | Producer-mode methodology MD (per CONVENTIONS §1.1; this is upstream-of-verdict infrastructure). The pre-registration this MD specifies is a separate reviewer-mode artefact drafted + reviewed in a different session per CONVENTIONS §1.2 / §4 producer-reviewer split. |
| Review status | PROPOSED; pending fresh-session `/research-methodology-review` before any decision below locks. |

---

## 1. Aim and one-paragraph framing

The corpus contains exactly one **independently-dated autonomic event**
that the subject did not derive from the biometrics: the acute COVID
infection of **2022-03-21 → 2022-04-03** (CONVENTIONS §5 anchor; 14
days). An acute viral infection is the textbook external perturbation
that an autonomic-state signal *should* register — fever, tachycardia,
sympathetic dominance, suppressed recovery (see §6 literature). The
question R23 asks is narrow and falsifiable: **during this known
infection window, does the project's "autonomic factor" (the
cross-channel autonomic-state cluster) visibly depart from the
subject's pre-infection healthy-era baseline, in the direction
physiology predicts?** This is a single-event peri-event check, not a
mechanism test. A clean positive corroborates that the factor tracks a
real autonomic perturbation; **a null is publishable** (the factor may
be too coarse, the channels may not have recorded the acute phase, or
the perturbation may not have moved the daily-aggregate primitives).

**Why this is confirmatory, not data-peeking** (per
[CONVENTIONS §4.3](../CONVENTIONS.md)). The hypothesis "an acute
infection moves the autonomic signal" has independent prior support on
all three §4.3 tests: (1) the subject lived through the infection and
its dates are annotated from contemporaneous notes, not from the
biometrics; (2) the published literature establishes an autonomic
infection signature without reference to this corpus (§6); (3) a
mechanistic argument (acute sympathetic activation + suppressed vagal
recovery during febrile viral illness) motivates the direction. The
in-corpus check is therefore *corroboration of a pre-specified prior*,
not origination of a post-hoc claim. The pre-registration discipline
here protects the **outcome** (unseen until lock), not the direction
of the hypothesis (which is prior-given).

## 2. The autonomic factor — what it precisely is (and a definition discrepancy)

**Resolved.** The factor is the **cross-channel "autonomic-state"
cluster (Cluster 2)** defined in
[`../analyses/garmin_exploration/cards/cross-channel-correlation.md`](../analyses/garmin_exploration/cards/cross-channel-correlation.md)
(computed 2026-06-08), **not** a PCA first principal component and
**not** a named weighted composite. It is a **structural / correlational
collapse** — several channels that move together because they share an
autonomic cause, with effective-N ≈ 1 for the cluster:

| Role | Channel | Column / primitive | Relation to anchor |
|---|---|---|---|
| Primary anchor | HA07c | `sleep_stress_mean` (overnight Garmin GSS mean) | — |
| Redundant (inverse) | HA10 | `morning_bb_peak` (morning body-battery peak) | Spearman ρ = −0.922 to HA07c (structural in Garmin's BB algorithm) |
| Peripheral | HA06b | `resting_hr` (resting heart rate) | ρ = +0.377 to HA07c; ρ = −0.393 to HA10 (vagal-tone pathway) |

The site's foundation Link 1/2 phrase the same object as *"these
channels are not independent witnesses — they share an autonomic
cause, and collapse to a single factor measured several ways"*
(`chain.json` / `clusters.json`, site label **"overnight autonomic
state"**). HA07d (`sleep_stress_stdev`, ρ=+0.50 to HA07c) and HA08c
(a slope of the same primitive) are adjacent members of the same
cluster; the **core triad is HA07c + HA10 + HA06b**.

> **Definition discrepancy — flagged for the user.** The R23 register
> states the factor is from `cohort_topology/findings.md`. That is
> **incorrect**:
> [`../analyses/descriptive/trajectory/cohort_topology/findings.md`](../analyses/descriptive/trajectory/cohort_topology/findings.md)
> is **event-topology + recovery-window work** (crash/dip geometry, per-
> channel recovery trajectories), **not** the inter-signal factor
> definition. The factor's only source is the cross-channel card above;
> [`../analyses/garmin_exploration/cards/clusters-export.md`](../analyses/garmin_exploration/cards/clusters-export.md)
> already records this correction verbatim (*"cohort_topology ... is
> event-topology + recovery-window work ... NOT the inter-signal factor
> definition. There is no separate cohort_topology factor doc to fold
> in; the cross-channel card is the whole factor substrate for R25"*).
> **Open question for the user**: the pre-reg must cite the
> cross-channel card as the factor source and either (a) define the
> factor operationally as the **HA07c sleep-stress primary anchor**
> (single primitive, cleanest), or (b) define it as a **multi-channel
> agreement readout** across the triad (closer to the site's "moves
> coherently across channels" framing). Decision (g) in §5 surfaces
> this.

**Guardrail.** Throughout, **"stress" = Garmin HRV-derived GSS**
(Firstbeat), not mental stress. The factor is HRV-derived (per
[`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md)); the FR245 has no
direct HRV channel, so the autonomic signal is recovered through the
overnight stress / body-battery / RHR triad.

## 3. Descriptive precondition (summary; full version in the analyses folder)

Established in
[`../analyses/descriptive/peri_event_covid/precondition.md`](../analyses/descriptive/peri_event_covid/precondition.md)
(coverage counts only, no outcome peek):

- **Event located**: 2022-03-21 → 2022-04-03, 14 days, single event, no
  reinfection annotated. Era = `corona_infection` (Stratum 2,
  corona-transition; Garmin-only).
- **Factor computable in window**: the three component channels
  (`resting_hr`, overnight stress, body-battery) have **row presence
  14/14 days** across the infection window; March + April 2022 are
  ~100% covered. Caveat: presence was confirmed at the raw-channel
  level; the **exact sleep-window primitives** (`sleep_stress_mean`,
  `morning_bb_peak`) need a one-line confirmation that the overnight
  derivation is non-null in March 2022 (logged as an open input).
- **Comparison design space**: the pre-LC healthy era 2021-08-16 →
  2022-03-20 (217 days) holds **15 non-overlapping** or **204 sliding**
  14-day windows, at ~99.5–100% per-channel coverage — so essentially
  all candidate windows are computable.

## 4. §2.2 four-input reasoning for the design

Per [CONVENTIONS §2.2](../CONVENTIONS.md), each major choice below is
reasoned from four inputs. This section gives the cross-cutting
reasoning; §5 carries the per-decision option tables.

### 4.1 Best-practices standards

- A **single-event peri-event design** is a degenerate interrupted-time-
  series (ITS): one known intervention/perturbation date, a pre-window
  baseline, a peri/post-window, and a contrast. The N-of-1 standards
  the corpus already inherits (CENT 2015, SCRIBE 2016, Daza 2018, WWC
  SCED 2022) treat the single-case design as legitimate **for
  within-subject change**, not for group inference. The reach is bounded
  to "did *this* signal move in *this* subject around *this* event."
- For inference on autocorrelated daily physiology, the project default
  is the **stationary bootstrap E[L]=7** null + bootstrap CI per
  [`permutation_null_block_length.md`](permutation_null_block_length.md).
  A single-event design adapts this: the relevant resampling unit is the
  *placement of a 14-day window* in the pre-LC baseline (a
  **window-shuffle / placebo-window null**), which preserves
  within-window autocorrelation by construction.
- Pre-vs-post raw-channel comparisons across a recovery trajectory must
  carry a **detrend sensitivity** ([CONVENTIONS §3.7](../CONVENTIONS.md)).
  Here the pre-LC era is a flat healthy baseline (no LC recovery
  trajectory yet), so trajectory-leak risk is low — but the §3.7 column
  is cheap and should be reported.

### 4.2 Established literature (cited where it materially bears)

The expected a-priori shape of an autonomic infection signature is
**not neutral** — see §6. The literature predicts an acute sympathetic-
dominant, vagal-suppressed signature during febrile viral illness, with
the strongest, cleanest move expected at the acute phase and possible
**non-monotonicity** (a blunted/collapsed signal at the most depleted
point). This shapes decision (e): the "moved" criterion should test for
**departure in the predicted direction**, but should not be so narrow
that it misses a non-monotone or blunted departure.

### 4.3 Our own tradeoff vision

The dominant tradeoff is **honesty about n=1 single-event reach vs the
temptation to over-claim from a clean picture**. One event cannot
separate "the factor tracks infection" from "the factor happened to
move that fortnight." We weight **defensibility + a publishable null**
over power. The design therefore (i) pre-specifies the criterion before
the look, (ii) uses a placebo-window null so "how unusual is a move
this size in an ordinary 14-day window" is quantified, and (iii) frames
even a strong positive as **corroboration, not proof** (single
corroborating event).

### 4.4 Our research limitations + objectives

Binding limitations from
[`research_line_limitations.md`](research_line_limitations.md): **L1**
single-subject reach (one event; n=1); **L2** era confounds — the
infection sits at the Stratum-1→Stratum-2 hard boundary, and the
comparison baseline is **Stratum 1 (pre-corona healthy)**, which is the
only legitimate "ordinary" comparator (post-infection days are LC-era
and not interchangeable per the HARD-BOUNDARY rule). **Acute-vs-LC-onset
inseparability (per methodology review M5).** The infection window
(2022-03-21→04-03) abuts LC onset (`LC_ERA_START = 2022-04-04`, the day
after the window's edge) — the acute infection and the *beginning of the
persistent LC autonomic shift* are temporally adjacent and cannot be
separated by this single-event design. A MOVED result must be reported
as *"the factor departed baseline around the infection / LC-onset
hinge,"* never as *"the acute infection caused the factor to move"*; the
window-tail signal especially cannot be attributed to the acute phase
alone. This caveat travels with every decision-(e)/(f) verdict. **L3** device
generation (FR245 Elevate V3, no direct HRV — factor is the GSS proxy);
**L7** survivorship/missingness (here near-zero — coverage is ~100% in
the window and baseline). The objective is **descriptive
characterisation** (Layer-1, no causal/interpretive marks per
[CONVENTIONS §4.1](../CONVENTIONS.md)): "the factor did / did not depart
from baseline around the event," never "the infection caused the
factor to move."

## 5. Design space — options + recommended default per decision (FOR USER LOCK)

Each decision is **PROPOSED**; the recommended default is the
drafter's pick under §4 reasoning. The user locks each in the pre-reg.

### Locked decisions (user sign-off, 2026-06-30)

Three load-bearing forks chosen explicitly; the rest accepted as
recommended defaults (flagged for the fresh-session methodology review).

| Decision | Locked option | How |
|---|---|---|
| (a) window | **a1** 14-day primary (2022-03-21→04-03) + a2 acute-core overlay + ±7d descriptive buffer | default |
| (b) comparison | **b2** matched sliding 14-day windows (n≈204) primary null + **b1** full-band personal baseline frame; report n=15 non-overlapping per §3.6 | **user-chosen** |
| (c) date-free | **c1** window-level aggregate + percentile only | default |
| (d) statistic/null | **d3** matched-window percentile + stationary-bootstrap E[L]=7 CI on standardised diff + §3.7 detrend column | default |
| (e) criterion | **e3 tiered** moved / ambiguous / moved-unexpected; predicted direction = high-autonomic-load pole | **user-chosen** |
| (f) null handling | **f1** publishable "AMBIGUOUS" + reasons + higher-resolution follow-ups | default |
| (g) factor readout | **g1** HA07c anchor primary + **g2** triad-coherence companion | **user-chosen** |

**Pending before final lock**: (i) ~~acute-viral-infection literature
anchor~~ — **DONE 2026-06-30** (`acute_viral_infection_autonomic_signature_review.md`;
folded into §6, predicted direction = high-load pole, daily-aggregate
detectability confirmed, blunting caveat moderate/severity-gated); (ii)
fresh-session `/research-methodology-review`; (iii) open-input #1 (the
overnight-primitive non-null confirmation in §8).

### (a) Infection-window definition + buffer days

| Option | Definition | Note |
|---|---|---|
| a1 | CONVENTIONS §5 anchor **2022-03-21 → 2022-04-03** (14 d) | Matches the locked `lc_phase == corona_infection` stratum; pre-registered era boundary. |
| a2 | Annotation core **2022-03-23 → 2022-03-30** (symptom/fever days) | Tighter "acute" window from the contemporaneous note ("a few days in bed with fever"). |
| a3 | a1 **+ buffer** (e.g. 7 pre-buffer + 7 post-buffer) to capture pre-rise + recovery tail | Buffer days are **descriptive context only**, not part of the contrast window. |

**Recommended default: a1 as the primary window** (it is the
pre-registered, lc_phase-locked 14-day stratum and matches the
comparison-window length exactly), **with a2 reported as an
"acute-core" sensitivity overlay** and a **±7-day descriptive buffer**
plotted for context (not entered into the contrast statistic). Buffer
is presentation, not test.

### (b) Comparison design — matched windows vs full pre-LC baseline band

| Option | Comparator | Strength | Weakness |
|---|---|---|---|
| b1 | **Full pre-LC baseline band** (2021-08-16 → 2022-03-20, 217 d): compute the factor's baseline distribution, place the infection window as a single point/window against it | Simple, uses all 217 healthy days, defines the personal baseline cleanly | Ignores within-baseline window-to-window structure unless paired with the window null |
| b2 | **Matched ordinary 14-day windows**: the 15 non-overlapping (or 204 sliding) pre-LC windows form the null distribution of "an ordinary 14-day window's factor value/move" | Like-for-like (14-day vs 14-day); directly answers "how unusual is this fortnight"; IS the placebo-window null | Sliding windows are autocorrelated (handled by block/window resampling) |

**Recommended default: b2 (matched sliding 14-day windows) as the
primary comparison, with b1 (full-band personal baseline) as the
descriptive frame.** The matched-window design is the honest
single-event analogue: it asks "is the infection fortnight extreme
relative to the distribution of *ordinary* fortnights this body
produced when healthy?" Use **sliding windows (n≈204)** for the null
distribution (richer), and **report the non-overlapping count (n=15)**
as the count of genuinely independent placements per
[CONVENTIONS §3.6](../CONVENTIONS.md) named-count discipline. Personal
baseline (b1) supplies the z-reference per
[CONVENTIONS §3.1](../CONVENTIONS.md).

### (c) Date-free aggregation + privacy floor

| Option | Aggregation | Privacy posture |
|---|---|---|
| c1 | Report only the **window-level summary statistic** (e.g. mean factor-z over the 14 days) + its rank/percentile against the null, no per-day values | Date-free, no daily trace exposed; passes `audit_for_publication.py` cleanly |
| c2 | Report per-day factor-z within the window | Exposes a dated 14-day biometric trace; heavier privacy review |

**Recommended default: c1.** Report the **window-level aggregate**
(window mean factor-z, and optionally window max single-day z for the
spike view per [CONVENTIONS §3.5](../CONVENTIONS.md)) plus its
**percentile against the matched-window null** — a single number with a
plain-language frame, no dated daily trace. This is date-free,
publication-safe, and keeps the artefact aligned with the existing
audit gate (CONVENTIONS §2.3). Per-day values stay internal.

### (d) Effect-size statistic + null model

| Option | Statistic | Null |
|---|---|---|
| d1 | **Window mean factor-z** (z against personal pre-LC baseline median+MAD per §3.1) | **Matched-window placebo null**: recompute the same window statistic over all sliding 14-day pre-LC windows; the infection window's percentile is the p-value analogue |
| d2 | Standardised mean difference (infection-window vs pooled pre-LC baseline) with **stationary bootstrap E[L]=7 CI** per [`permutation_null_block_length.md`](permutation_null_block_length.md) | Block-bootstrap CI on the difference |
| d3 | Both d1 + d2 reported side by side | — |

**Recommended default (REVISED per methodology review M1, 2026-06-30):
d3, but with the p-analogue null specified correctly.** The naive
percentile of the infection window against the **204 sliding** windows
is NOT a valid p-value — sliding windows share 13/14 days, so they are
not independent placements, and the stationary-bootstrap E[L]=7 the MD
cites disciplines the *d2 standardised-difference CI*, a different null.
The locked null model is therefore:

- **Primary p-analogue**: a **stationary-bootstrap E[L]=7 on the daily
  factor series** that regenerates the null distribution of the
  *14-day-window-mean factor-z* statistic under ordinary healthy
  variation; the infection window's percentile **in that bootstrap
  distribution** is the p-analogue. This uses all 217 healthy days and
  respects within-window autocorrelation by construction.
- **Transparent sanity-check**: the rank of the infection window among
  the **n=15 non-overlapping** (genuinely independent) 14-day windows,
  reported alongside per [CONVENTIONS §3.6](../CONVENTIONS.md).
- **The 204 sliding windows are a descriptive density backdrop only**,
  never a p-value denominator.
- **d2 effect size**: the stationary-bootstrap E[L]=7 CI on the
  standardised difference (infection window vs pooled pre-LC baseline),
  same bootstrap machinery — so one null model serves both the
  p-analogue and the CI.

Report **direction + magnitude alongside any p-analogue, never the p
alone** ([CONVENTIONS §3.7 / A7](../CONVENTIONS.md)); carry the **§3.7
detrend sensitivity** column (expected negligible pre-LC); confirm the
data-driven **E[L]\*** does not deviate by >2× from 7 before locking.

### (e) Pre-specified "moved vs null" criterion

| Option | Criterion |
|---|---|
| e1 | Infection-window factor-z lies in the **predicted-direction tail** beyond the 95th percentile of the matched-window null (one-sided, direction pre-given by §6) |
| e2 | Two-sided: window lies beyond the 2.5/97.5 percentile (catches a blunted/collapsed move in either direction per the non-monotone caveat in §6) |
| e3 | Tiered: **MOVED** (beyond predicted-direction 95th pct) / **AMBIGUOUS** (inside the band) / **MOVED-UNEXPECTED-DIRECTION** (beyond the opposite tail) |

**Recommended default: e3 (tiered), with the predicted direction = the
literature-anchored autonomic-infection signature (§6: elevated
overnight stress + RHR, suppressed body-battery → factor moves toward
the "high autonomic load" pole).** The tiered criterion is the honest
choice because §6 warns the *worst/most-depleted* states can **blunt**
the very signal the watch measures — so an unexpected-direction or
in-band result is informative, not a non-result. Lock the direction and
the 95th-percentile threshold in the pre-reg **before** the look.

### (f) How a NULL is reported (publishable)

| Option | Reporting |
|---|---|
| f1 | "AMBIGUOUS — the infection fortnight's factor value was within the ordinary-fortnight band (percentile X); the factor did not visibly depart from baseline at the 14-day aggregate resolution." + candidate reasons (acute phase too short for a daily-aggregate; channel-resolution dilution per §3.5; single-event power) | Frames the null as a finding, names what would change it |

**Recommended default: f1.** A null is a publishable Layer-1
descriptive result: it constrains the factor's sensitivity. The report
must (i) state the percentile/CI plainly, (ii) avoid any "absence of
evidence = evidence of absence" overclaim, (iii) log in the open-inputs
the higher-resolution follow-ups (per-minute intraday extraction; the
acute-core a2 window; the spike-count §3.5 metric) that could detect a
move the daily aggregate misses, and (iv) keep the §4.1 reach bound
("this signal, this subject, this one event").

### (g) [Surfaced by the discrepancy] Factor operationalisation for the pre-reg

| Option | Operationalisation |
|---|---|
| g1 | **Single primitive**: the factor = HA07c `sleep_stress_mean` (the cluster's primary anchor) z-scored against personal baseline | Cleanest, single number; matches "primary anchor" |
| g2 | **Triad agreement readout**: report the move on each of HA07c / HA10 / HA06b separately + a coherence flag (do they move together in the predicted signs?) | Matches the site's "moves coherently across channels" framing; richer but multi-comparison |

**Recommended default: g1 as the primary factor statistic (single
anchor, clean null), with g2's per-channel triad readout as a
descriptive companion** showing whether the three channels moved
coherently (the site's foundation claim). The pre-reg cites
[`cross-channel-correlation.md`](../analyses/garmin_exploration/cards/cross-channel-correlation.md)
as the factor source (NOT cohort_topology) and applies the
**one-column-per-definitional-pair** rule
([CONVENTIONS §3.3](../CONVENTIONS.md)): HA07c and HA10 are ρ=−0.92
near-identical, so they are not both entered as independent evidence —
the coherence readout treats them as one signal viewed twice.

**Pre-specified anchor contingency (REVISED per methodology review M2,
2026-06-30).** The g1 anchor depends on open-input #1 — whether the
overnight primitive `sleep_stress_mean` is non-null across the 2022-03
window. This must be **locked as a contingency keyed to a COVERAGE fact,
not chosen after the look**: *if the §8 #1 coverage query confirms
`sleep_stress_mean` is adequately present across the window → the
primary anchor is **HA07c `sleep_stress_mean`** (g1); if it is null or
too sparse → the primary anchor falls back to **HA06b `resting_hr`**
(confirmed present, RHR-up is the strongest/most-direct leg per §6).*
Resolving #1 is a **coverage check** (row-presence of the primitive),
NOT an outcome peek — it touches no infection-vs-baseline contrast. The
rule is locked in the pre-reg before any factor value is computed.

## 6. Expected a-priori autonomic infection signature (literature anchor)

What *should* an acute viral infection do to the factor, independent of
this corpus? Anchored by the dedicated acute-infection review
[`../literature/reviews/acute_viral_infection_autonomic_signature_review.md`](../literature/reviews/acute_viral_infection_autonomic_signature_review.md)
(landed 2026-06-30 — the directly-relevant **wearable infection-detection**
body; distinct from the chronic-LC HRV papers, which describe the
*persistent* state, not the acute phase). Cited per
[CONVENTIONS §2.2](../CONVENTIONS.md) item 2:

- **Direction — fixes decision (e), per-channel.** An acute febrile viral
  infection pushes the factor toward the **high-autonomic-load pole**:
  resting HR (HA06b) **UP**, HRV **DOWN** → the HRV-derived overnight
  Garmin GSS (HA07c) **UP**, overnight recovery / body-battery (HA10)
  **DOWN**. The RHR-up leg is strong and direct in the wearable cohorts
  (Mishra/Snyder 2020 Nat Biomed Eng; Natarajan 2020 npj Digit Med —
  *"respiration rate and heart rate are elevated by illness, while HRV is
  decreased"*; Radin 2020 Lancet Digit Health). The GSS-up and
  body-battery-down legs are **one inferential step** from the validated
  HRV↓/RHR↑ inputs Garmin's proprietary indices are built on. The chronic
  post-COVID HRV literature (Marques 2023 / Mooren 2023 / Suh 2023)
  corroborates the autonomic-impairment *direction* but is secondary
  context (persistent, not acute).
- **Detectability at this resolution — validates the design.** The
  signature is recoverable at **daily / overnight-aggregate resolution**:
  every directly-relevant cohort (Mishra, Natarajan, Radin) detects it
  from daily RHR + nightly aggregates, so R23 needs **no intraday data**.
  Qualification: the HRV component can present as a *circadian-pattern*
  change (Hirten 2021), and a short acute spike can be diluted by a
  14-day mean — which is exactly why decision (d) carries the
  **window-max companion** ([CONVENTIONS §3.5](../CONVENTIONS.md))
  alongside the window mean.
- **Blunting caveat — REAL but severity-gated (MODERATE).** Mechanistic
  autonomic uncoupling at extreme inflammation (Gholami 2012 endotoxemia;
  de Castilho 2017 ICU sepsis) licenses the *possibility* that a derived
  index flattens or decouples at the deepest point — but both are
  sepsis/ICU-tier, too severe to **predict** an inversion in a
  home-recovered infection. **Consequence for decision (e):** the tiered
  criterion's `MOVED-UNEXPECTED-DIRECTION` tier is a *guard* against a
  blunted/decoupled reading, **not a predicted outcome**; the predicted
  direction stays the high-load pole, and an in-band (`AMBIGUOUS`) result
  is the live alternative to a clean `MOVED`.

## 7. Existing peri-event / window-matching tooling (for reuse)

- **Closest existing tooling**: [`queued_work.md`](queued_work.md) **Q9**
  specifies "matching machinery for same-DOW within-baseline-window
  crash/non-crash pairs" and an aggregate-panel design with 95% CI
  bands — the same matched-window machinery this check needs, queued but
  not yet built. The R23 pre-reg should reuse / co-build it rather than
  re-implement.
- No dedicated `peri_event_*` script exists yet (glob clean); the
  matched-window null is new tooling to write under the pre-reg, sharing
  the [`permutation_null_block_length.md`](permutation_null_block_length.md)
  stationary-bootstrap helper and the personal-baseline z machinery
  ([CONVENTIONS §3.1](../CONVENTIONS.md)).
- The recovery-window infrastructure in
  [`../analyses/descriptive/trajectory/cohort_topology/`](../analyses/descriptive/trajectory/cohort_topology/)
  is **adjacent** (per-channel event recovery), reusable for the
  descriptive buffer plot in decision (a), but is **not** the factor
  source (see §2 discrepancy).

## 8. Open inputs (per `_plan_results_analysis_layer.md` §3.5)

| # | What is missing | Blocks | Cheapest path | Fallback |
|---|---|---|---|---|
| 1 | Confirm the **exact sleep-window primitives** (`sleep_stress_mean`, `morning_bb_peak`) are non-null in 2022-03 (raw-channel presence is confirmed; the overnight-derivation presence is not) | Locking decision (g1) on HA07c as primary | One-line coverage query on the two columns for March 2022 (S, < 30 min) | Use `resting_hr` (HA06b, confirmed present) as the primary anchor instead |
| 2 | User lock on decisions (a)–(g) | The pre-registration | This MD's §5 tables + a fresh-session methodology review | — |
| 3 | The matched-window null helper (Q9 machinery) | The test run (post-lock) | Co-build with Q9 per §7 (M) | — |
| 4 | Per-minute intraday FIT extraction for the acute-core (a2) window | A higher-resolution NULL follow-up only | Wave-4 intraday extractor if it exists; else new (M) | Daily-aggregate result stands as primary |

## 9. Cross-references

- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  §3.5 (open-inputs first-class), §3.6 / §4 (producer-vs-reviewer
  split for the pre-reg this MD specifies).
- [CONVENTIONS.md](../CONVENTIONS.md) §1.2 (no-outcome-peek / fresh-
  session pre-reg discipline), §2.2 (four-input methodology bar), §3.1
  (personal baseline), §3.3 (definitional-pair), §3.5 (spike metrics),
  §3.6 (named counts), §3.7 (detrend sensitivity), §4.1 (no interpretive
  marks on descriptive layers), §4.3 (prior-driven = confirmatory),
  §5 (LC timeline anchor).
- [`permutation_null_block_length.md`](permutation_null_block_length.md)
  — stationary bootstrap E[L]=7 null + CI (decision d).
- [`research_line_limitations.md`](research_line_limitations.md) — L1
  (single-subject), L2 (era hard boundaries; the infection sits at the
  Stratum-1→2 boundary), L3 (FR245 no-HRV), L7 (survivorship).
- [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) — the GSS-as-HRV-
  proxy justification underpinning the factor's stress component.
- [`../analyses/garmin_exploration/cards/cross-channel-correlation.md`](../analyses/garmin_exploration/cards/cross-channel-correlation.md)
  — **the factor source** (NOT cohort_topology).
- [`../analyses/descriptive/peri_event_covid/precondition.md`](../analyses/descriptive/peri_event_covid/precondition.md)
  — the descriptive precondition backing this MD.
- [`../literature/reviews/acute_viral_infection_autonomic_signature_review.md`](../literature/reviews/acute_viral_infection_autonomic_signature_review.md)
  — **the predicted-direction anchor** for decision (e) (acute wearable
  infection-detection body; Natarajan/Mishra/Radin/Hirten + the
  sepsis-tier blunting caveat). Plus the chronic-LC secondary context:
  [`../literature/reviews/expected_shapes_autonomic_signals_review.md`](../literature/reviews/expected_shapes_autonomic_signals_review.md)
  + Suh 2023 / Mooren 2023 / Marques 2023.
- [`queued_work.md`](queued_work.md) Q9 — reusable matched-window
  tooling.

## 10. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-30 | Drafted PROPOSED | Producer-mode STAGE-1 scoping for site request R23 by a fresh agent. Lays out design space (a)–(g) with recommended defaults; no decision locked. Factor source discrepancy (register said cohort_topology; actually cross-channel-correlation.md) resolved and surfaced as decision (g). No outcome peeked. Pending fresh-session `/research-methodology-review` and user lock before the pre-registration is drafted. |
| 2026-06-30 | Design decisions accepted by user | Three load-bearing forks chosen explicitly (e=tiered; g=anchor+companion; b=sliding+full-band); a/c/d/f accepted as recommended defaults. Producer-mode in-the-loop acceptance (distinct from the methodology peer-review gate). Pending before final lock: an acute-viral-infection literature anchor for decision (e) (user-requested 2026-06-30), then fresh-session `/research-methodology-review`, then the pre-reg is drafted. |
| 2026-06-30 | Acute-infection literature anchor folded in | `acute_viral_infection_autonomic_signature_review.md` landed; §6 now anchors the predicted direction (high-load pole) on the wearable infection-detection body, confirms daily-aggregate detectability, and reframes the blunting caveat as severity-gated (guard, not prediction). |
| 2026-06-30 | Fresh-session methodology review absorbed | [`reviews/methodology-peri_event_known_event_check-2026-06-30.md`](../reviews/methodology-peri_event_known_event_check-2026-06-30.md): verdict ACCEPT-WITH-MINOR-REVISIONS. No-outcome-peek contract HELD (airtight across MD + precondition); predicted-direction anchor SURVIVES. Absorbed: **M1** (percentile null re-specified — daily-series stationary-bootstrap E[L]=7 regenerates the window-statistic null; 204 sliding windows are descriptive density only; n=15 non-overlapping = transparent rank check); **M2** (g1-vs-HA06b anchor locked as a contingency keyed to the open-input #1 COVERAGE check, not an outcome peek); **M5** (acute-vs-LC-onset inseparability caveat added to §4.4). Factor definition (g) + §3.3 definitional-pair handling confirmed correct. **Design is now ready for final lock; pre-reg drafting may proceed.** |
