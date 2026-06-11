# Queued work — cards (C.X) and deferred research

*Living checkpoint, written 2026-06-06 so the items below don't drop
out of context between sessions. Two layers: **Upcoming** (next to
pick up) and **Deferred** (paused with explicit gates). Each entry has
**Intention** (what the artefact is and why it exists) and **TODOs**
(what we still need to work out, concretely).*

The C.X identifiers are insight-card concepts; they overlap with but
are not identical to the a-k tier list in [STOCKTAKE §4](STOCKTAKE.md#4-candidate-indicators-for-the-app--ranked-by-evidence).
Card-concept items live here; research items (H##, dictionary work)
also live here when they have specific, scoped TODOs to track. The
hypothesis-level state of play remains in
[garmin/hypotheses/registry.md §4](garmin/hypotheses/registry.md) and
the synthesis in [garmin/hypotheses/synthesis.md](garmin/hypotheses/synthesis.md).

---

## Tier 2 — Peer-review action items (added 2026-06-07 from [reviewer-reply](RESEARCH-REPORT-ADDENDUM.md))

An independent variable-architecture peer review landed 2026-06-07
at [garmin/review/2026-06-07-variable-architecture-review.md](garmin/review/2026-06-07-variable-architecture-review.md);
the project's research lead replied at
[garmin/review/2026-06-07-reply-with-ha07d-context.md](garmin/review/2026-06-07-reply-with-ha07d-context.md).
Tier 1 framing fixes landed in the same session. Tier 2 action
items committed here:

### Cheap diagnostics on existing data (highest leverage per effort)

- **Diagnostic methodology v2 round (Option C tightened)**
  *(COMPLETED 2026-06-07)* — Per user-locked Option C following
  the HA07d diagnostic v1 CLOSE both eras (a CLOSE that revealed
  the v1 criteria themselves only capture canonical-decline
  robustness and penalise stable-plateau / rising-with-threshold
  shapes that are equally robust). All four v2 diagnostics ran
  with locked v2 criteria
  ([methodology/threshold-sweep-rescue-criteria-v2.md](garmin/methodology/threshold-sweep-rescue-criteria-v2.md)).

  **Atomic restoration map**:
  - **HA10 validate**: RESCUE via Cat 3 (rising/late-peak; peak
    at N_std=1.75 with +19.5 pp; sustained disc through strict
    tier). Restored as **corroborating secondary anchor** for
    validate-era.
  - **HA07d both eras**: RESCUE — train via Cat 3 (peak 1.75 with
    +21.4 pp, 0 sign-changes in [1.0, 3.0], positive across
    rise — the worked walkthrough confirmed against the
    researcher's earlier intuition); validate via Cat 2 (stable
    plateau, 8 contiguous tiers > +15 pp from N_std=1.0 to 2.75)
    + Cat 3. **Overall-SUPPORTED restored** — the project's first
    such finding, now confirmed under v2.
  - **HA11 train one-sided elevated**: RESCUE via Cat 1
    (canonical decline; textbook robust shape; peak at N_std=1.25
    with +45.4 pp, Spearman −0.683). Restored to load-bearing.
  - **HA06b train bidirectional**: **CLOSE** via Cat 4 (2 sign-
    changes in [1.0, 3.0]: curve crosses zero at N_std=1.0 with
    disc −4.1 and at N_std=3.0 with disc −2.1; Cat 3 also fails
    because positive_across_rise fails). **Permanently demoted**.
    Locked +18.9 pp SUPPORTED stays on record.

  Three RESCUES, one CLOSE. **The discipline binds in both
  directions**: v2 produced honest verdicts per finding; the
  RESCUES are principled via Cat 1/2/3; the CLOSE is genuine
  shape fragility per Cat 4. The reviewer's symmetric-application
  critique was vindicated — HA06b couldn't be exempt just
  because it wasn't in the original v1 round.

  **Methodology playbook**: v2 criteria are now the project's
  locked methodology for threshold-sweep diagnostics. Future
  tests with primary SUPPORTED at the loosest threshold tier
  should run a v2 diagnostic before being treated as load-bearing.
  The v3 escape hatch is strictly bounded per the methodology
  document §5.

  Atomic synthesis update applied 2026-06-07 across STOCKTAKE +
  synthesis + addendum + registry + this document + Wiggers
  progress + pem-pacing-indicators.

- **HA10 threshold-monotonicity diagnostic v1** *(CLOSED 2026-06-07,
  verdict CLOSE per locked rule v1; v2 pre-registered)* —
  Pre-registered + ran on 2026-06-07 at
  [HA10-threshold-monotonicity-diagnostic/](garmin/hypotheses/HA10-threshold-monotonicity-diagnostic/).
  Fine N_std grid [0.5 → 4.0, 13 tiers] applied to HA10
  validate-era 4d bidirectional primary. **Peak at N_std=1.75**
  (one σ-tier past the rescue window [1.0, 1.5]). Every other
  shape criterion PASSED (Spearman rho −0.456, disc held +14 at
  2.0 and +11 at 2.5, sign-changes 1). Peak-location failure is
  the sole close trigger. Per locked rule: HA10 SUPPORTED verdict
  stays on record but synthesis-level framing demotes HA10 to
  non-load-bearing. HA07d becomes sole validate-era load-bearing
  anchor for card (b2). Nuance: HA10's one-sided ELEVATED arm
  shows robust +23 pp plateau N_std=1.5 → 2.5, so the *direction*
  remains supported; only HA10's bidirectional-primary choice
  failed. Methodology lesson banked: threshold-monotonicity
  diagnostic added to project methodology playbook; future tests
  with primary SUPPORTED at loosest tier only should run it
  before entering synthesis. Doc updates landed same session in
  STOCKTAKE §4 b2 + addendum §5.20 + synthesis HA07c/HA08c/HA07d
  block + registry §4b.

- **HA01b per-axis decomposition** *(COMPLETED 2026-06-07; FIRST
  DIAGNOSTIC UNDER CONSOLIDATED PLAYBOOK)* — HA01b's withdrawal
  under Theme A left open which of the four input axes
  (effective_exertion, step_burden, max_hr_peak, vigorous_min) was
  carrying signal (if any). Per-axis re-test ran 2026-06-07 under
  the user-locked Option A testing playbook
  ([garmin/methodology/testing-playbook.md](garmin/methodology/testing-playbook.md))
  section 9 compliance bar. **Finding**: composite REFUTED was
  hiding a per-axis signal. **effective_exertion SUPPORTED both
  eras** (train +21.3 pp, validate +19.5 pp); two more axes
  SUPPORTED validate-only (step_burden +16.6 pp, vigorous_min
  +24.6 pp); max_hr_peak REFUTED both eras (validate inverted
  -7.7 pp, consistent with chronotropic incompetence). Composite
  control reproduces HA01b REFUTED (+3.4 / +1.5 pp). Per playbook
  §5.2 produces a **diagnostic finding, NOT a re-test verdict**;
  HA01b composite REFUTED stays on record. Both-eras rule reduces
  load-bearing to effective_exertion only. Critical specificity
  caveat: posterior-per-fire ~2.2% vs 1.7% base rate. Pre-committed
  follow-ups locked: HA01c + HA01c v2 threshold-monotonicity
  diagnostic. Generalisable methodology lesson on MAX-rank
  composites queued for playbook §3 addendum. Full result at
  [HA01b-per-axis-diagnostic/result.md](garmin/hypotheses/HA01b-per-axis-diagnostic/result.md).
  Doc updates landed same session: registry §4b, STOCKTAKE §2a +
  headline, addendum §5.22, synthesis "Update 2026-06-07 later
  still ×3", QUEUED-WORK (this entry + the two new pre-registered
  items below).

- **HA01c effective-exertion shock (per-axis re-formulation)**
  *(COMPLETED 2026-06-07; SUPPORTED both eras at locked threshold)*
  — pre-committed follow-up triggered by HA01b per-axis diagnostic's
  effective_exertion both-eras SUPPORTED finding. Primary:
  `effective_exertion_rank_lagged ≥ 0.75` in 4-day lead-up; same
  3-criterion bar as HA01b composite; both-eras rule. Locked
  verdict: SUPPORTED both eras (train 81.8% / +21.3 pp / median
  0.883, n=11; validate 80.0% / +19.5 pp / median 0.909, n=15;
  identical numbers to per-axis diagnostic — disciplinary re-run).
  HA01b composite REFUTED stays on record per playbook §2.2.
  Load-bearing status gated on v2 outcome (see next item). Result:
  [HA01c result.md](garmin/hypotheses/HA01c-effective-exertion-shock/result.md).

- **HA01c v2 threshold-monotonicity diagnostic** *(COMPLETED
  2026-06-07; FIRST AMBIGUOUS IN V2 SERIES — train AMBIGUOUS /
  validate RESCUE)* — 5th v2 diagnostic in v2 round. Tested rank
  thresholds {0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95} per
  rank-adapted locked five-category shape rule. **Train AMBIGUOUS**:
  shape is bumpy-but-never-negative (15.4→6.4→16.2→21.3→10.3→7.9→
  2.0→7.3); peak τ=0.75 +21.3 pp; 0 sign-changes — fails Cat 1
  (peak not in [0.50, 0.70]), Cat 2 (range too wide), Cat 3 (peak
  < 0.80, monotone rise broken by 0.50→0.60 drop), Cat 4 (no
  sign-changes), Cat 5 (peak too high). Genuine edge case the
  locked rule doesn't categorize. **Validate RESCUE via Cat 1**:
  textbook canonical decline (15.4→24.6→21.0→19.5→13.3→13.3→12.3→
  6.7); peak τ=0.60 +24.6 pp; ρ=-0.850. **Mixed verdict per playbook
  §4.4 both-eras rule**: HA01c stays SUPPORTED-with-stability-mixed
  — honest but NOT load-bearing. **No HA01c card.md drafted** (per
  playbook §2.7 + §6.2). Discipline binds: framework returns
  honest indeterminacy on train rather than forcing a fit. Result:
  [HA01c v2 result.md](garmin/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/result.md).

- **Testing playbook §3.8 composite construction addendum** *(LANDED
  2026-06-07)* — generalisable methodology lesson from HA01b
  per-axis diagnostic: MAX-rank composites can dilute per-axis
  signal in the null distribution. Rules for future composite
  pre-registration: (1) pre-register per-axis primaries IN ADDITION
  to the composite, OR (2) use AND-of-axes composites (tighter
  specificity, different trade-off). The composite's REFUTED
  verdict is a real verdict, not a stand-in for "no axis carries
  signal"; per-axis decomposition diagnostic remains pre-committed
  when MAX-rank composite refutes. Landed at
  [testing-playbook.md §3.8](garmin/methodology/testing-playbook.md).

- **H01 / H03 / H04 Generation-3 re-tests** — H01 (RHR rolling
  baseline, absolute threshold, 7d), H03 (sleep efficiency, daily,
  3-day), H04 (BB net delta, daily, 3-day) were all Generation-1
  methodology. HA06b re-tested the RHR channel through a different
  primitive (z-score) and found train SUPPORTED, partly absorbing
  H01's "channel closed" verdict. H03 and H04 have not been
  re-tested at Gen 3 standards (lagged baseline + z-score +
  bidirectional + 4d/5d). Cheap — same data, new test script
  pattern. Each could rescue, reopen, or formally close a
  foundational channel.

- **HA11 U-dip parameter sensitivity diagnostic** — The U-dip
  detector has multiple parameters (S_pre ≥ 40, drop ≥ 25, plateau
  ≥ +5, refractory 60 min) that were physiologically motivated but
  not externally anchored. HA11 train-SUPPORTED is load-bearing
  in the seven-channel synthesis; a parameter-sensitivity grid
  (vary each parameter ±20%, measure discrimination stability)
  would either strengthen the finding or surface over-fit
  concerns.

- **Fisher's exact + binomial 95% CIs on primary verdicts**
  *(COMPLETED 2026-06-08)* — retrofitted to all 11 primary
  verdicts (HA07d train+validate / HA10 validate / HA06b train /
  HA11 train / HA07c train / HA08c train / H02b train / H02d
  bridge × 5d train / HA01c train+validate). **Only H02b
  (p=0.029) and H02d (p=0.011) reach α=0.05 one-sided. Zero reach
  Bonferroni α=0.005.** HA07d validate +21.7 pp → p=0.0703;
  HA10 validate +16.2 pp → p=0.1475. The project's
  60%/+15pp/magnitude bar is more permissive than conventional
  α=0.05 with n=14-15 crashes — a conscious n-of-1 choice, now
  documented with numbers. Output:
  [garmin/cards/primary-verdict-statistics.md](garmin/cards/primary-verdict-statistics.md).
  Computation: [garmin/cards/compute_fisher_ci.py](garmin/cards/compute_fisher_ci.py).

- **Cross-channel correlation matrix** *(COMPLETED 2026-06-08)*
  — Pearson + Spearman correlations across 7 load-bearing
  primitives over the full corpus (1339-1365 days per primitive,
  inner-joined on calendar date). **Two paradigm-shifting
  findings**: (1) **H02b ≡ H02d at the per-day level (ρ = +1.000,
  identical for all 1737 shared valid days)** — H02d's bridge
  sentinel handling produces the same daily primitive as H02b;
  discrimination difference comes entirely from window/validity
  rules, NOT from a distinct underlying signal. H02d must drop
  as a separate channel in synthesis framing. (2) **HA10 ≡ −HA07c
  (ρ = −0.922)** — morning BB peak and sleep stress mean are
  nearly the same signal in opposite signs (structural in Garmin's
  BB algorithm). HA10 and HA07c are NOT independent channels.
  Effective N of independent signal clusters: 3-4 (not 7).
  Honest effective-N Bonferroni (α = 0.05/4 ≈ 0.0125): only H02d
  (p=0.011) clears it; with H02b/H02d collinearity counted as one,
  **only ONE distinct primitive survives honest effective-N
  significance correction**. The "seven SUPPORTED on six channels"
  framing must soften to "three-to-four effectively-independent
  signal clusters". Output:
  [garmin/cards/cross-channel-correlation.md](garmin/cards/cross-channel-correlation.md).
  Computation: [garmin/cards/compute_cross_channel_correlation.py](garmin/cards/compute_cross_channel_correlation.py).
  Doc updates landed same session: STOCKTAKE §2a, registry §4b,
  RESEARCH-REPORT-ADDENDUM §5.26.

- **(historical placeholder)** Original Tier 2 framing predicted:
  HA07c / HA08c / HA07d highly correlated; HA06b / HA10 / HA11 / H02b
  moderately correlated; H02d very correlated with H02b. Worth
  knowing for synthesis weighting.

### Card specificity (urgent for downstream prototyping) *(COMPLETED 2026-06-07)*

- **Specificity / precision / posterior tables for HA07d + HA10 +
  H02b + secondary anchors** *(COMPLETED 2026-06-07)* — locked
  spec at [garmin/methodology/specificity-tables-spec.md](garmin/methodology/specificity-tables-spec.md);
  derivative Bayes computation over locked result-data.json files.
  Output:
  [garmin/cards/card-b-train-specificity.md](garmin/cards/card-b-train-specificity.md)
  +
  [garmin/cards/card-b2-validate-specificity.md](garmin/cards/card-b2-validate-specificity.md).

  **DECISIVE FINDING: all 9 load-bearing anchors land in Tier C**
  (lift < 2× or precision < 5% — retrospective annotation only,
  NOT viable as forward-warning cards). Best train: H02b 3d at
  4.87% precision, 1.69× lift. Best validate: HA07d 4d at 2.24%
  precision, 1.33× lift. Zero anchors reach Tier B (5-30%
  precision + 2-5× lift) or Tier A (≥30% + ≥5×).

  **Structural insight**: lift ≈ recall/null_fire is independent
  of base rate; no anchor's recall/null_fire ratio exceeds 2×, so
  the 2× lift threshold cannot be cleared at any base rate.

  **Card framing implications**: Card (b) train + Card (b2)
  validate both restricted to retrospective-annotation-only
  surfaces per playbook §6.6. The acceptable surface is timeline
  annotation during after-the-fact review, paired with the
  gevoelscore record. Even HA07d (project's only overall-SUPPORTED
  + v2-validated finding) drops to 2.24% precision per fire vs
  1.69% base rate.

  **Methodology lesson**: hypothesis-test bar clearance and
  card-shippable precision are different gates. Future card
  pre-registrations should include specificity-table thresholds
  in the hypothesis.md, not deferred to downstream check. Candidate
  for playbook §3.9 addendum.

  Doc updates landed same session: STOCKTAKE §2a + headline,
  RESEARCH-REPORT-ADDENDUM §5.25, registry §4b, QUEUED-WORK (this
  entry).

### Outcome-side improvements

- **Crash_v3 from notes (mechanism subtyping)** — Highest-leverage
  outcome-side fix per peer-review §2. The current crash_v1
  pooled outcome probably contains 2-4 distinct mechanisms (PEM
  crash, infection-driven low, hormonal cluster, depressive
  episode). Mechanism-stratified subgroups would let the existing
  29 episodes be analysed as cleaner subgroups even at the cost
  of smaller-N per subgroup. Depends on the notes-quality work +
  Goal B (tagging-suggestion engine) work that's currently in
  the queue. Pre-condition.

- **S02 score trajectory** — Reviewer's recommendation alongside
  S01 (which plots Garmin metrics over time). S02 would plot the
  gevoelscore series over the full window, characterise its
  trajectory empirically (when did the stabilisation transition
  actually happen?), and provide the lead/lag question between
  self-experience and biometric channels. Cheap, descriptive.

### Framing arms

- **Pooled-corpus descriptive arm** — Per the earlier "stay the
  course" decision, we kept the chronological train/validate split
  as primary. The peer-review §4 critique re-surfaces the
  recommendation to add a pooled arm as exploratory secondary on
  every test. Cheap, would surface signals the both-eras rule
  masks. Add to all future result.md files; optionally retrofit
  to select prior tests where the pooled arm would change the
  reading.

- **Era-as-moderator narrative reframe** — Already applied to
  STOCKTAKE headline + synthesis + addendum + indicators in this
  session's Tier 1 fixes. Future doc updates should continue the
  reframe: era is the project's central moderator variable, not
  a generalisation gate.

### Tier 3 (methodological refinement, deferred)

- **Block-bootstrap null sample** — Replace the 200-random-window
  null with a block-bootstrap that respects the autocorrelation
  structure of the 1370-day series. Not expected to materially
  shift verdicts but would tighten claims.

- **Formal heterogeneity test** (Cochran's Q / I²) on multi-era
  effect sizes — Era-as-moderator narrative gains a formal
  statistical test rather than narrative inference.

---

## Recently completed (2026-06-07, much later same day) — HA07c + HA08c + HA07d substitutes; FIRST OVERALL-SUPPORTED TEST

After HA10 + HA11 landed and **H04b path C authorisation
completed** (garminconnect library installed, OAuth token cached
at `~/.garminconnect_tokens/`), the smoke test revealed the
**Forerunner 245 hardware does not record HRV** — the HRV Status
feature was added on the newer Forerunner 255/265/955/965 / Fenix 7
generation watches (2022-2023) with a multi-sample sensor the
FR245's 2019 hardware lacks. The `/hrv-service/hrv/{date}`
endpoint returns an empty dict for every date sampled
(2022-2026). **HA07 / HA08 / HA12 are BLOCKED-PENDING-HARDWARE
permanently for this dataset.**

Sleep stress is a defensible HRV proxy (Garmin's stress is
HRV-derived during sleep when activity ≈ 0; Workwell + Wiggers
reference it as an HRV-class indicator in pacing recommendations).
**Three substitute pre-registrations locked BEFORE any data was
inspected**:

- **HA07c** ([HA07c-sleep-stress-mean-delta/result.md](garmin/hypotheses/HA07c-sleep-stress-mean-delta/result.md))
  — night-over-night sleep stress mean delta z-scored. Primary 4d
  N_std=1.5 one-sided elevated: **train SUPPORTED at +23.2 pp
  (69.2% freq)**; validate refuted (−6.0 pp). Multi-arm robustness
  (5d elevated +18.4 pp, 4d N_std=2.0 lowered +26.0 pp,
  bidirectional +19.7 pp). **5th train-era SUPPORTED autonomic-
  channel precursor on the 5th channel.** Train directionality
  split: 33% elevated / 67% lowered-at-max-|z| — train crashes
  preceded by HIGH AUTONOMIC VOLATILITY.

- **HA08c** ([HA08c-sleep-stress-slope/result.md](garmin/hypotheses/HA08c-sleep-stress-slope/result.md))
  — trailing-5-day OLS slope of mean sleep stress, z-scored.
  Primary 4d N_std=1.5 one-sided elevated: **train SUPPORTED at
  +23.0 pp (61.5% freq)**; validate refuted (+1.5 pp). 5d
  secondary elevated +23.2 pp also SUPPORTED. Strong validate
  ANTI-PREDICTIVE at N_std=2.0 bidirectional (**−36.2 pp**).
  **6th train-era SUPPORTED finding** under clean methodology;
  both acute (HA07c delta) and sustained (HA08c slope) modes
  confirmed in train. Wiggers' "HRV daalt over meerdere dagen na
  overbelasten" creep mode is empirically present in train.

- **HA07d** ([HA07d-sleep-stress-variability/result.md](garmin/hypotheses/HA07d-sleep-stress-variability/result.md))
  — night-over-night delta of in-sleep-window stress STDEV,
  z-scored. Second-order primitive testing HRV-of-HRV-proxy.
  Bidirectional primary. **PRIMARY 4d N_std=1.5: TRAIN SUPPORTED
  (+19.6 pp, 84.6%) AND VALIDATE SUPPORTED (+21.7 pp, 86.7%) →
  OVERALL SUPPORTED per the locked rule. FIRST PROJECT
  OVERALL-SUPPORTED TEST after 19 pre-registered hypotheses.**

  Per-era directionality: **train SUPPORTS BOTH directions**
  (volatility) — elevated arm +27.4 pp AND lowered arm +16.5 pp;
  **validate SUPPORTS ONLY the LOWERED direction** (stillness) —
  +21.7 pp at N_std=1.5, **+28.5 pp at N_std=2.0** (STRONGEST
  validate-era discrimination on any arm in the project).
  Validate-era pattern is **autonomic stillness / freeze**: sleep
  stress variability DROPS before validate-era crashes; autonomic
  state becomes unusually stable; body "looks like" recovery;
  crash arrives anyway. Combined with HA10 (elevated BB peak),
  validate-era now has TWO converging empirical anchors both
  consistent with Wiggers' "freeze" / parasympathetic-swing
  pattern.

- **Net change: SEVEN train-era SUPPORTED + TWO validate-era
  SUPPORTED + ONE overall-SUPPORTED**. Card (b) train-era
  retrospective has SEVEN anchors. Card (b2) validate-era
  retrospective has TWO anchors. D7 single-mechanism-two-regimes
  reframe is now anchored on the SAME channel (sleep stress
  variability) showing different directions per era — single-test
  internal consistency, not just cross-channel inference.

- **Methodology lessons banked**:
  - Pre-register relative thresholds for autonomic-channel tests
    (HA06 → HA06b banked; followed by all subsequent tests).
  - Pre-register **bidirectional primary** when direction is
    a priori ambiguous (HA07d's primary bidirectional was
    crucial; one-sided would have missed validate).
  - **Second-order primitives can carry signal first-order
    primitives miss** (HA07c mean delta refuted validate at
    +4.3 pp; HA07d variability delta supported validate at
    +21.7 pp). The dimension that shifts before validate-era
    crashes is FLEXIBILITY, not LEVEL.
  - **Locked HRV pre-registrations remain as audit-trail records**
    even when blocked by hardware; substitutes locked *before*
    data inspection preserves methodology integrity.

- **H04b path C status**: authentication + sleep backfill running
  in background (~1372 days, recent dates only have BB / stress
  arrays populated; older dates return empty per Garmin's
  historical-backfill limitations). H03b (per-minute BB recharge
  sharpening of HA10) gated on backfill completion.

- Doc updates landed in [RESEARCH-REPORT-ADDENDUM.md §§5.17-5.21](RESEARCH-REPORT-ADDENDUM.md),
  [STOCKTAKE.md §2a + §3 + §4 + §7](STOCKTAKE.md),
  [synthesis.md](garmin/hypotheses/synthesis.md) "Update 2026-06-07
  (later still even) — HA07c + HA08c + HA07d", and [registry.md
  §4 + §4b](garmin/hypotheses/registry.md).

## Recently completed (2026-06-07, later same day)

After HA06 / HA06b, the queue ran into a data-availability blocker
on HA07 (HRV not present in any local source for this Forerunner
245 GDPR dump). User pivoted to **HA10 (BB recharge coarse proxy)
then HA11 (within-day stress U-dip)** — both operationalisable on
existing local data. Both closed on 2026-06-07 with substantial
project-level findings.

- **HA10 BB morning peak z-score** ([HA10-bb-overnight-recharge/result.md](garmin/hypotheses/HA10-bb-overnight-recharge/result.md))
  — primary 4d bidirectional: **TRAIN REFUTED (50.0% freq, −20.5 pp
  disc); VALIDATE SUPPORTED (86.7% freq, +16.2 pp disc, median
  |z|=2.121)** → overall REFUTED per the locked rule, but **the
  validate-era SUPPORTED is the project's first validate-era
  SUPPORTED test under the canonical 3-criterion bar**. 13 prior
  pre-registered tests had refuted validate-era. Striking
  directionality reversal: train 100% lowered direction (Wiggers
  canonical "didn't recharge"); validate 69% elevated direction
  (paradoxical "looked like a great night but" swing pattern).
  5d secondary each era SUPPORTED in *opposite* direction (train
  +18.3 pp lowered; validate +27.5 pp elevated) — cleanest
  era-directionality reversal in the project. Cross-channel
  coherence with HA06b: BB is inversely-related to RHR via
  vagal-tone, so opposite-direction-per-era pattern is internally
  consistent — Wiggers' "freeze" pattern empirically population-
  level visible in two independent channels. Pre-committed soft
  outcome triggered: **H04b strongly prioritised** for per-minute
  trajectory enrichment.

- **HA11 within-day stress U-dip count z-score** ([HA11-stress-udip/result.md](garmin/hypotheses/HA11-stress-udip/result.md))
  — first within-day pattern test in the project. Stage 1
  extraction re-parsed all 7888 monitoring_b FIT files (~7 min,
  1469 total U-dip events across 1722 valid days). U-dip event =
  sharp drop ≥ 25 stress points from S_pre ≥ 40 baseline followed
  by plateau ≥ 5 points HIGHER than baseline. Per-day count z-scored.
  Primary 4d one-sided elevated: **TRAIN SUPPORTED (64.3% freq,
  +22.8 pp disc, median signed z=2.168); VALIDATE REFUTED
  inverse-direction (30.8% freq, −10.7 pp disc, scaling to
  −24.1 pp at 5d N_std=2.0)** → overall REFUTED, but train
  SUPPORTED is the **fourth train-era SUPPORTED autonomic-channel
  precursor on the fourth channel** (after H02b stress spike,
  H02d bridge × 5d, HA06b RHR). Pre-cliff era's
  sympathetic-overarousal precursor signature is now four-channel-
  confirmed — strongest multi-channel convergence in the project.
  Validate-era U-dip inverse-direction is itself a characteristic
  signature of the parasympathetic-swing era (not random noise).
  Same-day Spearman ρ between u_dip_count and gevoelscore is
  essentially zero (train +0.075, validate +0.012) — U-dip is a
  4-day-lead precursor, not a same-day symptom correlate.

- **Net change to "what's SUPPORTED" under clean methodology:**
  four train-era SUPPORTED autonomic-channel precursors (H02b,
  H02d, HA06b, HA11) AND **one validate-era SUPPORTED precursor
  (HA10 morning BB peak elevated)** — the first validate-era
  SUPPORTED test in the project. D7 single-mechanism-two-regimes
  reframe now has empirical anchors in BOTH eras. Era directionality
  reversal formalised across four channels via vagal-tone physiology.

- **Card (b) train-era retrospective** has FOUR converging
  empirical anchors. Strongest empirical case for any card concept.
- **Card (b2) validate-era retrospective** promoted back from
  Tier 2 to Tier 1 *candidate*, anchored on HA10 elevated BB peak
  pattern; needs H04b per-minute trajectory enrichment before
  shipping.

- Doc updates landed in [RESEARCH-REPORT-ADDENDUM.md §§5.14-5.16](RESEARCH-REPORT-ADDENDUM.md),
  [STOCKTAKE.md §2a + §3 + §4 + §7](STOCKTAKE.md),
  [synthesis.md](garmin/hypotheses/synthesis.md) "Update 2026-06-07
  (later same day) — HA10 + HA11", [registry.md §4 + §4b](garmin/hypotheses/registry.md),
  and this document's queue (below).

## Recently completed (2026-06-07)

HA06 (morning nightly RHR delta with absolute thresholds) and HA06b
(z-score relative-threshold methodological re-test) closed on
2026-06-07.

- **HA06 — REFUTED both eras** ([HA06-morning-rhr-delta/result.md](garmin/hypotheses/HA06-morning-rhr-delta/result.md)).
  Train 21.4% freq, +13.9 pp disc (close but fails crit a); validate
  **0 of 15 crashes trigger at the 5 bpm threshold** — decisive.
  Median max-|delta| for this participant is **1.6-3.5 bpm**;
  Wiggers/Workwell-calibrated thresholds (5/10/15 bpm) exceed the
  participant's actual RHR-variability range. The bidirectional
  framing caught one extra train triggering event (+7.1 pp) but the
  Wiggers parasympathetic-swing pattern contribution is small in
  absolute terms.
- **HA06b — TRAIN SUPPORTED, validate REFUTED, overall REFUTED**
  ([HA06b-rhr-zscore/result.md](garmin/hypotheses/HA06b-rhr-zscore/result.md)).
  Same data, same lagged baseline, same windows, same bar — but
  relative threshold `|RHR − μ| / σ ≥ N_std` (N_std = 1.5 / 2.0 /
  2.5) instead of absolute bpm. **Train SUPPORTED at N_std=1.5**
  (71.4% freq, +18.9 pp disc, median |z|=2.31) AND at N_std=2.0
  (+21.3 pp), in 4 of 6 bidirectional configurations. Validate
  refuted (53.3% freq, +0.8 pp disc). Striking **directionality
  reversal between eras**: train 70% elevated / 30% lowered;
  validate **25% elevated / 75% lowered** — Wiggers'
  parasympathetic-swing pattern empirically present in validate at
  75% of triggering events but does NOT discriminate from null
  windows where the same pattern appears at similar rate. Validate
  one-sided elevated-only shows **−16.2 pp** — classical Workwell
  direction is anti-predictive in validate.
- **Net change to "what's SUPPORTED"**: investigation now has
  **three train-era SUPPORTED autonomic-deviation precursors on
  three channels** (H02b stress spike 3d, H02d bridge × 5d stress
  spike, **HA06b RHR z-score 4d**), all overall-REFUTED by validate.
  The pre-cliff autonomic-deviation precursor is now demonstrably
  multi-channel, not stress-specific. The b retrospective card
  (train-era 2022-23) has a substantially stronger empirical case
  than after H02b alone. The validate-era refutation now spans
  12 pre-registered tests (5 stress + 4 activity + 2 RHR + 1 sleep
  efficiency).
- **Methodology lesson banked**: pre-register relative thresholds
  (z-score or percentile rank) as the default for autonomic-channel
  tests. Absolute thresholds drawn from external populations need
  re-calibration to participant variability *before* the test runs.
  Applies forward to HA07, HA08, HA10 — they should pre-register
  on relative thresholds from the start.
- Doc updates landed in [RESEARCH-REPORT-ADDENDUM.md §§5.12-5.13](RESEARCH-REPORT-ADDENDUM.md),
  [STOCKTAKE.md §2a + §3 + §7](STOCKTAKE.md),
  [synthesis.md](garmin/hypotheses/synthesis.md) "Update 2026-06-07",
  and [registry.md §4 + §4b](garmin/hypotheses/registry.md).

## Recently completed (2026-06-06, later session)

The 4-review literature batch + the Theme A baseline-contamination fix
+ the bundled re-test + H02d (run independently by another agent in
the same session) all landed on 2026-06-06. Resolutions and their
effect on items below:

- **Theme A baseline fix** — implemented at
  [garmin/activity-labels/scripts/11_compute_lagged_baseline.py](garmin/activity-labels/scripts/11_compute_lagged_baseline.py)
  with spec at [severity_spec.md §Lagged baseline (v3.2)](garmin/activity-labels/spec/severity_spec.md)
  and audit trail at [registry.md §4b Theme A entry](garmin/hypotheses/registry.md).
- **Bundled re-test HA02c + HA01b-recomputed** — result at
  [activity-labels/output/ha_results_4day_lagged.md](garmin/activity-labels/output/ha_results_4day_lagged.md).
  Both REFUTED on the lagged baseline. HA01b validate-era went from
  +17.3 pp (originally SUPPORTED) to +4.0 pp (refuted). The "first
  SUPPORTED validate-era precursor" headline was substantially a
  rolling-baseline construction artifact. The pre-committed
  symmetric-re-test discipline held.
- **H02d — stress spikes with uncensored sentinels + wider window**
  ([garmin/hypotheses/H02d-stress-spikes-uncensored/result.md](garmin/hypotheses/H02d-stress-spikes-uncensored/result.md))
  — addressed two operationalisation gaps in H02b (sentinel collapse;
  3-day window). **Refuted overall** but with two clean findings:
  bridge × 5d train produced +31.8 pp discrimination (the strongest
  train-era single-channel signal of the whole project, surpassing
  H02b's +29.9 pp), and validate refuted in all 4 arms (imputed ×
  {4d, 5d}, bridge × {4d, 5d}). **5 stress-channel tests are now
  consistent on validate refutation** (H02, H02b, H02d × 4). The 4-5
  day empirical lag is now corroborated by both H02d bridge train
  (smooth monotonic 3d → 4d → 5d = +29.9 → +27.6 → +31.8 pp) AND
  HA01b's lag profile — two independent channels converging on the
  same lag.
- **Net change to "what's SUPPORTED"**: investigation now has **two
  train-era SUPPORTED stress-spike findings** (H02b 3d, H02d bridge
  × 5d), both overall-REFUTED. **Zero overall-SUPPORTED precursors
  under clean methodology.** The validate-era refutation now spans 5
  stress-channel tests + 4 activity-shock channel tests + all prior
  daily-aggregate tests.
- Synthesis updates landed in [RESEARCH-REPORT-ADDENDUM.md §§5.9-5.11](RESEARCH-REPORT-ADDENDUM.md),
  [STOCKTAKE.md §2a + §3 + §4 + §7](STOCKTAKE.md),
  [synthesis.md](garmin/hypotheses/synthesis.md) "Update 2026-06-06 (later still)" and
  "(later still even)", [pem-pacing-indicators.md §3.3](garmin/pem-pacing-indicators.md),
  and [registry.md §4 + §4b](garmin/hypotheses/registry.md).

## C.1 — clarified

An earlier draft of this document had an "Open question: what is C.1?"
section, because C.4 ("recovery-completeness over time") below was
noted as "depends on C.1" but C.1 had not been written down.

**Resolution**: the C.# naming in this document tracks the C.# in the
recent organising plan ([.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md)).
In that plan:

- **C.1** = **morning resting-HR delta** (a new pre-registered
  HA06-shaped test). See the new C.1 entry under Upcoming below.

The thing C.4 actually depends on is the **H05b sustained-recovery
primitive** ("for each crash, how many days until the score returns
to and stays at pre-crash baseline?"), not C.1. C.4's "depends on"
line has been corrected accordingly.

---

## Upcoming (next to pick up)

### H04b path C authorisation — highest-leverage next step

**Intention.** Authorise the Garmin Connect REST API path C
(`cyberjunky/python-garminconnect`) for personal-use, own-data
analysis. Three benefits stack from a single authorisation:

1. **Unlocks HRV** (`/wellness-service/wellness/dailyHrv/{date}`) for
   **HA07** (day-over-day HRV drop) **+ HA08** (multi-day HRV creep)
   **+ HA09** (parasympathetic-swing detection, reframed) **+ HA12**
   (pre-infection HRV rise). All four currently blocked because HRV
   is not present in any local data source for this participant's
   Forerunner 245 GDPR dump (verified 2026-06-07 across UDS,
   sleepData, bioMetrics, monitoring_b FIT, activity FIT).

2. **Unlocks per-minute Body Battery**
   (`/wellness-service/wellness/bodyBattery/events/{date}`) for **H03b
   proper** (overnight BB recharge as marker of unrefreshing sleep)
   AND **sharpens HA10's validate-era SUPPORTED finding** — the
   coarse 3-anchor proxy already finds 86.7% trigger / +16.2 pp
   discrimination in validate; the per-minute trajectory should
   sharpen this.

3. **HA10's §9 pre-commit triggered**: validate SUPPORTED → H04b
   strongly prioritised. The empirical signal is already there at
   coarse resolution; per-minute is plausibly cleaner.

**Status.** Protocol fully locked at
[.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md).
ToS-grey awareness: Garmin's general Terms of Use prohibit
automated scraping; internal endpoints are not covered by any
documented personal-use API agreement. **Risk accepted by user for
personal-use own-data analysis with a light footprint** (one
login, ~90-day pull, then idle).

**Two-path protocol after authorisation:**
- **Path C (API)**: pull per-minute BB + nightly HRV for the full
  corpus 2022-09-03 → 2026-06-05. Rate-limit-aware. Store outside
  app tree at `C:\Users\Gebruiker\Documents\gevoelscore-data\garmin
  data\bb_per_minute\` and parallel `hrv_per_night\`.
- **Path B (FIT decode of `unknown_233`)**: in parallel, attempt
  to decode the per-minute BB from FIT files using Path C labels
  as ground truth (small public contribution if successful).

**TODOs (when un-gated by authorisation).**
- [ ] Stand up `cyberjunky/python-garminconnect` with the
      participant's Garmin Connect credentials, stored locally only.
- [ ] Pull HRV + per-minute BB for the full corpus.
- [ ] Per-day feature extraction for HRV (RMSSD distribution
      per night, day-over-day delta, multi-day slope) and BB
      (overnight recharge rate, rise-count, drop-count,
      time-of-lowest, drain-during-waking-hours).
- [ ] Join into the daily wide table for HA07-style precursor
      testing.
- [ ] H03b spec lock (overnight BB recharge metric, z-scored).
- [ ] Path B FIT decode: extract raw `unknown_233` 4-byte payloads
      from a stratified sample; test ~12 candidate byte encodings
      against Path C ground truth on 180-day holdout.

---

### HA07 — Day-over-day HRV drop on z-score thresholds (gated on H04b path C)

**Intention.** Natural sibling test to HA06b after HA06b's
methodology lesson banked the rule: *pre-register relative thresholds
from the start for autonomic-channel tests; absolute thresholds drawn
from external populations need re-calibration to participant
variability before the test runs, not after.* HRV channel rather than
HR — less subject to the chronotropic incompetence that affects
>85% of ME/CFS (Workwell's own caveat for HA06). If HA07 train also
SUPPORTS, the autonomic-deviation pattern is five-channel-confirmed
for pre-cliff (H02b, H02d, HA06b, HA11, HA07). If validate ALSO
SUPPORTS in some direction, the validate-era picture becomes
multi-channel confirmed.

**Source**: Wiggers attributes to *de vermoeidheidskliniek* — a drop
of ≥ 10 HRV points night-over-night may indicate PEM is coming. But
per the HA06b lesson, **we pre-register on z-score thresholds, not
the absolute 10 ms**, since 10 ms is calibrated to lotgenoten /
fatigue-clinic populations whose HRV variability may not match this
participant's.

**BLOCKED on data availability (discovered 2026-06-07).** HRV is
not present in any local data source for this participant's
Forerunner 245 GDPR dump. Re-queued behind H04b path C
authorisation which unblocks HRV via the
`/wellness-service/wellness/dailyHrv/{date}` REST endpoint.

#### TODOs (locked before any test runs)

- [ ] **Verify HRV field**. Confirm the Garmin UDS HRV field used
      in the H01-H04 era is RMSSD-derived (Wiggers' explicit units
      in ms). Check identity to that field; if there is more than
      one HRV-like field, pick the one matching Wiggers' framing.
- [ ] **Lock day-over-day metric.** Two candidates, pre-register
      which is primary in hypothesis.md:
  - **(a)** signed delta `HRV(d) − HRV(d-1)` z-scored against the
    participant's own day-over-day-delta distribution computed on
    the lagged baseline window `[d-90, d-30]` (primary if it
    computes cleanly — 60 nights minus watch-off gives ~50 valid
    day-pairs typically).
  - **(b)** signed delta against personal-baseline μ ± Nσ where μ
    and σ are the HRV value's own (not the delta's) lagged
    distribution (secondary if (a) has variance pathology).
- [ ] **Lock thresholds.** Z-score thresholds N_std = 1.5 primary
      (matching HA06b's primary that lifted train to SUPPORTED) /
      2.0 secondary / 2.5 sensitivity check.
- [ ] **Lock direction.** Wiggers' rule is one-sided downward (HRV
      drops indicate PEM coming). Primary: one-sided
      `delta-z ≤ −N_std`. Sensitivity arm reports bidirectional
      `|delta-z| ≥ N_std` for symmetry with HA06b.
- [ ] **Lock lead-up window.** 4-day primary `[D-4, D-1]` (matches
      HA06b primary; the 4-5 day empirical lag is now cross-channel
      confirmed). 5-day secondary `[D-5, D-1]`.
- [ ] **Both-era test**. Same train/validate split.
- [ ] **SUPPORTED bar**: same three-criterion shape (frequency
      ≥ 60% of crash episodes; discrimination ≥ +15 pp above null;
      magnitude criterion C: median |delta-z| ≥ N_std/2). Pre-commit
      before running.
- [ ] **Caveats to flag in any result writeup.**
  - HRV is in principle less blunted than HR for chronotropic-
    incompetent patients, but Garmin's stress algorithm uses HRV
    as its input. Independent observation? Or downstream of the
    same sensor pathway as the stress channel? Note explicitly.
  - **Coverage gap**: nights with watch off do not contribute to
    the day-over-day delta sequence (consecutive valid nights are
    required for a delta). Verify night-coverage rate matches
    HA06's 99.4% train / 98.6% validate before running; report
    the actual valid-delta-pair count separately from the night
    count.
  - **Day-over-day variance can be high**. If the participant's
    natural day-over-day HRV variability already produces
    |delta-z| ≥ 1.5 on ~50% of any random window (as RHR did under
    HA06b), the test will be structurally non-discriminative.
    **The 3-episode dry-run print MUST surface this before the
    spec is finalised**, per the methodology lesson banked from
    HA06 → HA06b.
- [ ] Same null sample seed (`20260605`) and same windowing
      machinery as scripts 08/09/12 for direct comparability.
- [ ] **3-episode dry-run print** before locking the spec —
      especially important here since the day-over-day delta is a
      new measurement primitive for the project.

**Why it's now next.** HA06b banked the relative-threshold
methodology lesson AND closed the RHR channel for validate; HA07 is
the natural sibling on the HRV channel where chronotropic-
incompetence concerns are less acute. Same data, same lagged
baseline, same windows.

---

### C.2 — Cognitive / emotional load mining from notes + tags

**Intention.** A precursor hypothesis test, not a descriptive
one-pager. The notes v2 work already showed late-era lead-up days
carry +12 pp `belasting_cognitief` mention and late-era crash days
carry +22 pp `belasting_gezin` mention. The activity-labels work
*originally* showed HA01b (4-day exertion shock) as a candidate
validate-era precursor, but the Theme A bundled re-test refuted that
finding on the cleanest baseline — the +17.3 pp was substantially a
rolling-baseline construction artifact. **C.2 asks the interaction
question regardless**: does tag-load × exertion-class predict dips
(or crashes) better than exertion-class alone? The interaction
question is independent of HA01b's main-effect verdict; even a null
main effect can carry information when conditioned on a tag-load
signal. C.2 becomes *more* important now that the Garmin waking-hour
layer is closed for validate-era crashes — the journal-layer signal
may carry what the biometric layer cannot.

**Pre-register before any model fits.**

**TODOs.**
- [ ] Define "tag load" precisely. Candidates:
  - count of cognitive/emotional tags in the lead-up window
  - rolling sum of tagged-load days across N days
  - distinct categories carried (mentaal vs gebeurtenis vs project)
  - decide single metric or test 2-3 in parallel under a pre-registered grid
- [ ] Decide outcome: `crash_v1` start (29 episodes) vs `crash_v2` dip
      (79 dips) vs both. The HA01 3-day dip finding (+9.3 pp) suggests
      dips may be the more sensitive outcome.
- [ ] Lock lead-up window. Default to 4-day to match HA01b's
      validate-era precursor finding; consider also testing 3-day to
      bracket.
- [ ] Lock the model. Likely logistic regression with main effects +
      interaction term, but spec it out before running. Specify how
      "interaction beats main-effects-only" is operationalised
      (likelihood ratio test? AIC delta? discrimination delta on
      held-out?).
- [ ] Same train/validate split as H##/HA01b (train 2022-09-03 →
      2023-12-31; validate 2024-01-01 → 2026-06-05).
- [ ] Pre-register falsification: interaction term coefficient must be
      meaningfully non-zero AND held-out validate discrimination must
      improve by ≥ X pp over class-only.
- [ ] Methodology lesson banked: do the 3-episode dry-run before
      locking the spec.

**Why it's next.** Cheap (uses existing notes v2 + activity-labels
outputs, no new data extraction) and directly tests the user's lived
framing that emotional/cognitive load combines with exertion to
trigger crashes.

---

### C.3 — Personal-lag teaching one-pager (descriptive)

**Intention.** A derivative artefact, not a hypothesis test. Combines
the crash_v2 + H02b + (now-softened) activity-labels results into a
single piece teaching the participant their own PEM lag pattern:
*"your dips tend to arrive 2–3 days after a heavy day."* Descriptive
only — no prediction bar.

**Important framing change post-Theme A**: HA01b's +17.3 pp validate-era
discrimination was refuted on the lagged baseline (Theme A bundled
re-test, 2026-06-06). The 4-day lag is no longer empirically validated
by a SUPPORTED test. The teaching can still be written, but its
empirical anchors are now (a) the H02b train-era 3-day stress-spike
precursor and (b) the participant's experiential framing
("trigger day, day after still ok, crash sets in day 2-3"). The
HA01b 4-day result becomes "consistent with the experiential framing,
but the underlying activity-shock signal does not survive a
methodologically clean baseline re-test." Honest, not a hook.

**TODOs.**
- [ ] Decide era framing now that the 4-day HA01b SUPPORTED claim is
      withdrawn. Options:
  - Unified experiential framing ("typically 2-3 days") with
      H02b 3-day train-era support as the empirical anchor and the
      validate-era as currently precursor-invisible on cleanest
      baseline.
  - Era-honest framing: train-era ≈ 3-day stress-spike precursor
      (H02b SUPPORTED); validate-era no waking-hour precursor yet
      validated on a clean baseline (HA06 morning RHR is the next
      candidate).
  - Whichever the participant prefers; both are honest.
- [ ] Pull numbers:
  - H02b 3-day discrimination (+29.9 pp train, SUPPORTED)
  - HA01b 4-day rolling-baseline discrimination (originally +17.3 pp
      validate; clearly state this was refuted on the lagged
      baseline at +4.0 pp per Theme A bundled re-test)
  - lag-profile peaks (exploratory, label as such — and also subject
      to the same rolling-baseline construction caveat now)
- [ ] Draft Dutch copy. Respect tone discipline:
  - reflective, no em-dashes ([no em-dash memory](../../C:/Users/Gebruiker/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_no_emdash_in_ui.md))
  - presents conclusions not prescriptions (pacing-doc)
  - brainfog-readable in seconds (frontend-conventions)
- [ ] Identify 2–3 supporting crash examples with clear visible lag
      (e.g. a validate-era crash with a heavy day on D-4 and the
      anticipated D-1 "still OK").
- [ ] Decide delivery surface. Options:
  - paper-style one-pager (print/PDF) for the participant's own use
  - in-app card concept (later) — but not the same as the
    retrospective per-crash cards b / b2; this is a teaching piece, not
    a per-event surface
- [ ] Cross-link from [STOCKTAKE §4 Tier 1](STOCKTAKE.md#tier-1--strong-evidence-ready-to-prototype)
      once drafted — likely sits between cards (b) / (b2) and (c).

---

### C.4 — Recovery-completeness over time (descriptive)

**Intention.** Derivative one-pager. Tracks the participant's
*recovery* trend in a single monthly metric: percentage of
heavy/very_heavy days that were followed by a sustained return to
baseline. Builds on the **H05b sustained-recovery primitive**
(see Tier 3 below). Descriptive only.

**TODOs.**
- [ ] **Lock H05b sustained-recovery primitive first** (see Tier 3 below).
      Without a precise "returned to baseline" definition, C.4 cannot
      be computed. (Earlier drafts of this document used "C.1" to
      refer to this primitive; that was a naming overlap with the
      C.1 morning-RHR-delta indicator. Corrected: H05b is what C.4
      depends on; C.1 is the separate HA06-shaped pre-registered test
      above.)
- [ ] Decide the "heavy day" reference event:
  - `exertion_class ∈ {heavy, very_heavy}` (activity-labels output)?
  - any `crash_v1` episode start?
  - either, reported as two parallel series?
- [ ] Decide aggregation. Monthly %? Quarterly? Rolling 90-day?
- [ ] Compute series across full corpus 2022-09-03 → 2026-06-05.
- [ ] Plot alongside S01 stabilisation trajectories (max stress-spike
      duration, avg stress baseline, RHR, sleep efficiency) — so the
      recovery-completeness line shares an x-axis with the other
      pendulum signals.
- [ ] Honest framing of partial months and the May 2026 perturbation.
- [ ] Decide whether this lives standalone or as a panel inside the
      stabilisation-arc card (a) in [STOCKTAKE §4 Tier 1](STOCKTAKE.md#tier-1--strong-evidence-ready-to-prototype).

---

### C.5 — Volatility + dip-frequency progress metric (descriptive)

**Intention.** Derivative one-pager. A two-component progress
indicator showing whether the participant is stabilising: rolling
30-day standard deviation of `gevoelscore` (volatility) + monthly dip
count (frequency). Descriptive only.

**Status update 2026-06-07**:
[S02](garmin/hypotheses/S02-score-trajectory/notes.md) was executed
and explicitly left volatility + dip-frequency as C.5's scope (S02
covers the *level* + *distribution* framing of the score pendulum;
C.5 covers the *progress* framing). S02's hypothesis.md §2
cross-references this entry. C.5 is now downstream of S02 — it can
mirror S02's anchor grid (90d window, 7d cadence, first anchor
2022-12-02) for direct overlay with S02 panels 1-3. The May 2026
uptick that
[S02c](garmin/hypotheses/S02c-may2026-divergence/notes.md)
characterised as "RHR-only at recent baseline; other Garmin
channels and score essentially unmoved" should inform C.5's
recent-period framing.

**TODOs.**
- [ ] Compute rolling 30-day std of score across the full corpus.
      Edge-handling at the boundaries of the analysis window.
      *(Can mirror S02's anchor grid for direct overlay.)*
- [ ] Compute monthly dip count from `crash_v2` tier-2 labels
      ([labels CSV](garmin/hypotheses/crash_v2-definition/labels_crash_v2.csv)).
- [ ] Decide whether to also overlay monthly crash count (tier-1) or
      keep that for the stabilisation-arc card to avoid duplication.
- [ ] Plot together. Twin-axis (std left, count right) or two stacked
      panels. *(Could also be added as a 4th panel underneath
      S02's existing 3-panel main plot.)*
- [ ] Honest framing of the May 2026 uptick already visible in S01
      and characterised as "modest at recent-baseline σ" by
      [S02c](garmin/hypotheses/S02c-may2026-divergence/notes.md).
- [ ] Cross-reference: this is a "progress" framing of the same
      pendulum [S01](garmin/hypotheses/S01-stabilisation-trajectories/notes.md)
      visualises through biometrics, and complements
      [S02](garmin/hypotheses/S02-score-trajectory/notes.md)'s
      level/distribution framing of the score. Decide whether to ship
      this as a standalone card or as the score-side panel of the
      stabilisation-arc card (a).

---

## Autonomic-channel sibling hypotheses (HA06 family — queued 2026-06-06 from Wiggers pdf; updated 2026-06-07 after HA06 + HA06b + HA10 + HA11)

These hypotheses test the overnight-recovery / autonomic-regulation
mechanism through different channels and patterns. Source: Laure
Wiggers, *Smartwatch Pacing* (2025-07), a lotgenoten-curated
lived-experience guide that explicitly cites Workwell +
Bateman-Horne + Ruijgt/Wüst 2025 (the same Dutch HRV preprint in our
background literature), so the patterns are well-aligned with the
academic threshold-dynamics literature.

**Status update 2026-06-07**:
- **HA06** CLOSED, REFUTED both eras (absolute thresholds mis-
  calibrated to participant).
- **HA06b** CLOSED, train SUPPORTED at z-score thresholds, validate
  refuted (parasympathetic-swing pattern empirically present at 75%
  of validate triggering events but non-discriminative).
- **HA10** CLOSED, train REFUTED / **validate SUPPORTED** at z-score
  thresholds (FIRST validate-era SUPPORTED in the project under
  canonical bar). Era directionality reversal: train 100% lowered
  → validate 69% elevated.
- **HA11** CLOSED, train SUPPORTED elevated, validate REFUTED inverse-
  direction (fourth train-era SUPPORTED on fourth channel).
- **HA07 / HA08 / HA09 / HA12** all BLOCKED on data availability —
  HRV not present in any local data source. Re-queued behind H04b
  path C authorisation.

Methodology lesson banked: **pre-register relative thresholds
(z-score) from the start for all remaining autonomic-channel tests**.
H04b path C authorisation is now the highest-leverage next step
(unblocks HRV for all gated tests AND sharpens HA10 validate signal
via per-minute BB).

### Status of each test in the family

- **HA07** (day-over-day HRV drop) — top of Upcoming, GATED on H04b
  path C.
- **HA08** (multi-day HRV slope) — below, GATED on H04b path C.
- **HA10** (BB recharge coarse proxy) — CLOSED, validate SUPPORTED.
- **HA11** (within-day stress U-dip) — CLOSED, train SUPPORTED.
- **HA09** (parasympathetic-swing detection) — work-on-later;
  reframing reinforced again after HA10 + HA11 (now confirmed
  swing pattern is predictive in validate via HA10).
- **HA12** (pre-infection HRV rise) — work-on-later; gated on H04b
  path C + notes-quality.

#### HA08 — Multi-day HRV creep (sustained downward trend)

**Source**: Wiggers: *"HRV daalt over meerdere dagen na
overbelasten"* — the slow-erosion mode, complementary to HA07's
single-night-shock mode.

**Intention.** Tests whether sustained negative slope in nightly
HRV across the lead-up window predicts crashes. Matches our A.2
trend-slope concept from Theme A but on a different signal.

**Data availability.** Same as HA07. Straightforward.

**Operationalisation sketch.**
- OLS slope of nightly HRV over rolling 5-7 days (analogous to
  `effective_exertion_slope_28d` but shorter window).
- **Slope distribution z-scored against personal lagged baseline**
  per the HA06b methodology lesson — do NOT pre-register absolute
  ms/day thresholds. Threshold: slope z ≤ −N_std (N_std = 1.5
  primary / 2.0 secondary / 2.5 sensitivity check) anywhere in the
  4-5 day lead-up.

**TODOs.**
- [ ] Lock slope window (5d primary, 7d secondary).
- [ ] Lock slope z-score thresholds N_std = 1.5 / 2.0 / 2.5
      (consistent with HA06b + HA07).
- [ ] Same bar, both-era test, same null seed.
- [ ] **3-episode dry-run print** to confirm the slope-z distribution
      is not pathological (per HA06b lesson).

#### HA10 — Body Battery overnight recharge — coarse 3-anchor proxy

**Source**: Wiggers: chronic-illness BB rarely reaches 100% even
with adequate sleep. Below 70-80% is her practical "stay above"
floor for stability. Healthy people can fully recharge; this
population often cannot.

**Intention.** Coarse version of H03b that does NOT need per-minute
BB from H04b. Tests whether the overnight recharge computed from
the 3 daily BB anchor points (HIGHEST, LOWEST, MOSTRECENT — already
extracted for H04) is reduced in the crash lead-up window.

**Data availability.** We already have the 3 BB anchors per day
from the H04 extraction. **Operationalisable NOW without H04b.**

**Operationalisation sketch.**
- Nightly recharge proxy = morning HIGHEST anchor − evening LOWEST
  anchor (using anchor timestamps to identify morning vs evening).
- Alternative: `drainedValue − chargedValue` daily ratio (H04
  already produced this).
- Test whether the proxy is depressed in the 4-5 day lead-up.

**TODOs.**
- [ ] Verify anchor timestamps make morning-vs-evening
      identification reliable.
- [ ] Lock recharge metric: nightly delta vs proportional ratio.
- [ ] **Pre-register on z-score thresholds against the
      participant's own recharge distribution**, NOT Wiggers'
      absolute 70-80% floor — per the HA06b methodology lesson
      banked 2026-06-07. N_std = 1.5 primary / 2.0 secondary / 2.5
      sensitivity check (consistent with HA06b, HA07, HA08).
- [ ] Both-era test, same bar.
- [ ] **Pre-commit a soft outcome**: even if REFUTED, the coarse
      version tells us whether the per-minute version (H03b
      proper) is worth the H04b decoding effort. If the coarse
      proxy shows zero signal in train *and* validate, H03b's
      priority drops materially.
- [ ] **3-episode dry-run print** to confirm the recharge-z
      distribution is not pathological (per HA06b lesson).

#### HA11 — Stress U-dip pattern (orthostatic / electrolyte signature)

**Source**: Wiggers documents a specific within-day pattern:
per-minute stress drops sharply (U-shape) then plateaus at a
higher-than-pre-dip baseline. She resolves it with ORS /
electrolytes; hypothesised to be orthostatic / low-blood-volume
dysregulation.

**Intention.** Within-day pattern, distinct from HA06-08's
across-day patterns. Could be a precursor *or* a same-day symptom
signature — both worth testing.

**Data availability.** Per-minute stress from monitoring_b (H02b
and H02d both extracted this). Straightforward.

**Operationalisation sketch.**
- Detect within-day stress trajectories with: (a) sharp drop > X%
  over Y minutes, followed by (b) plateau at higher-than-pre-dip
  baseline for Z hours.
- Test two outcomes: (i) U-dip day precedes crash/dip within
  forward window; (ii) U-dip day correlates with same-day low
  gevoelscore.

**TODOs.**
- [ ] Lock U-dip definition: drop %, drop window, plateau threshold,
      plateau duration.
- [ ] Test against both crash and dip labels.
- [ ] Cross-reference with notes for "ORS" / electrolyte / "duizelig"
      mentions — Wiggers herself documents resolving U-dips with ORS;
      same-day notes may corroborate.
- [ ] Both-era test.

### Need more work (multi-stage definition or new labels)

#### HA09 — Parasympathetic-swing detection (work-on-later; new context after HA06b)

**Source**: Wiggers' "freeze" pattern. The most striking
lived-experience finding in the pdf, and the one that motivated
HA06's bidirectional test design.

**Intention.** Test a specific multi-stage pattern: after a heavy
day, the night sometimes shows paradoxically HIGH HRV + LOW RHR
("perfect night"). Wiggers' claim: this LOOKS like recovery but is
actually warning — body battery drains faster the next day,
symptoms continue.

**New context from HA06b (2026-06-07).** HA06b confirmed the
parasympathetic-swing pattern is **empirically present in this
participant's validate era at 75% of triggering events**, but it does
NOT discriminate validate-era crashes from random non-crash 4-day
windows — the lowered-RHR pattern appears in null windows at roughly
the same rate. The pattern is part of the participant's *current
autonomic baseline*, not a precursor signal for crashes. A swing
detection test that uses crash labels as the outcome would inherit
the same non-discrimination problem HA06b already documented.

**Reframing implication.** HA09 should NOT be pre-registered against
crash labels (that question is now answered: non-discriminative).
Instead, the more informative framing is one of two:
- **(i) Predict next-day dysregulation, not crashes**: do swing nights
  predict day-+1 BB drain rate / gevoelscore / functional capacity?
  This is the question Wiggers actually documents (next-day
  symptom continuation), and it sidesteps the crash-label non-
  discrimination already shown.
- **(ii) Anchor on known overexertion days, not crash labels**: take
  days with `exertion_class_lagged ∈ {heavy, very_heavy}` and ask
  whether the subset followed by a swing-night recover differently
  from the subset followed by a "normal" night. Tests whether the
  swing is itself functionally bad even when it doesn't precede a
  crash.

**Data availability.** All available (nightly RHR, nightly HRV,
`exertion_class_lagged`). Pattern detection + multi-stage
pre-registration is the work.

**Operationalisation sketch (revised).**
- Identify "swing nights": nights where
  (HRV z ≥ +N_std) AND (RHR z ≤ −N_std) — per the HA06b methodology
  lesson, use z-score thresholds, not absolute bpm/ms.
- Restrict to nights PRECEDED by a heavy / very_heavy exertion day.
- Test outcome (i) or (ii) above, NOT a 4-5 day crash window.

**Why still work-on-later** (not next on queue).
- Multi-stage definition is harder to pre-register cleanly without
  drifting toward outcome-shopping. The HRV-z high and RHR-z low
  thresholds + the precondition day's exertion threshold all
  interact.
- Outcome (i) needs a clean BB-decline measurement primitive,
  which is partly what H04b / HA10 are setting up.
- Outcome (ii) needs a clean "next-day recovery" primitive,
  which is what H05b is supposed to provide.
- Both gating items are queued separately; HA09 will compose with
  whichever lands first.

#### HA12 — Pre-infection HRV rise

**Source**: Wiggers and others in the lotgenoten community report
HRV paradoxically *increasing* in the day or two before catching a
cold/flu.

**Intention.** Could explain a subset of "precursor-invisible"
validate-era crashes that are actually infection-driven rather than
exertion-driven. If true, the validate-era refutation across 5
stress-channel + 4 activity-channel tests becomes more
interpretable: those crashes don't have an exertion precursor
because they're not exertion-precipitated.

**Data availability.** Nightly HRV (straightforward) +
infection-day labels (needs notes mining).

**Operationalisation sketch.**
- Mine notes for infection-suggestive keywords: "corona", "griep",
  "verkouden", "keelpijn", "koorts", "ziek".
- For each infection-suggestive day, look at the 1-3 day prior
  HRV — does it rise above the lagged baseline?
- Likely descriptive only (small N), but interesting if positive.

**TODOs.**
- [ ] Notes keyword filter for infection markers (crude first pass;
      can refine with notes-quality work / dictionary v3).
- [ ] Verify count of infection-marked days in the corpus.
- [ ] Define "HRV rise" threshold (mirror HA07's 10 ms or use
      slope direction).
- [ ] Pre-register descriptive only unless N ≥ 10; document as
      exploratory if underpowered.

### Suggested order within the family (revised 2026-06-07 after HA06/HA06b)

1. **HA06 / HA06b** — CLOSED 2026-06-07. RHR channel done (refuted
   under absolute thresholds; train SUPPORTED / validate refuted
   under z-score thresholds; methodology lesson banked).
2. **HA07** — next on queue (pulled out to its own top-level
   "Upcoming" slot above). Natural sibling; HRV channel less
   blunted by chronotropic incompetence than HR.
3. **HA10** — operationalisable NOW without H04b; pre-commits a
   soft outcome that informs H04b prioritisation.
4. **HA08** — straightforward extension of HA07.
5. **HA11** — within-day pattern, complementary axis.
6. **HA09** — work-on-later; reframed after HA06b (target next-day
   dysregulation or post-overexertion recovery, NOT crash labels —
   the crash-label version is already answered non-discriminative).
7. **HA12** — descriptive only; gated on notes-quality work for a
   cleaner version.

---

## Deferred (paused with explicit gates)

### C.6 — Dip attribution

**Intention.** Per-dip retrospective card concept. Attribute each
isolated dip to its most likely contributing factor — exertion shock,
cognitive/emotional load, calendar event, notes content match, or
"no signal." Sits in the same family as Tier 2 (g) caregiving-context
tagging.

**Gate.** *Needs the daily-entry feature design call.* Where the
attribution UX surfaces (inside daily-entry retrospect, calendar
retrospective view, or a separate "look back" surface) determines the
shape of the attribution algorithm.

**TODOs (when un-gated).**
- [ ] Wait for daily-entry design to land enough to pick a surface.
- [ ] Algorithm sketch (rank-order what to surface for each dip):
  1. HA01b-flagged exertion shock in D-4 to D-1
  2. High tag-load (per C.2 once locked) in lead-up
  3. Notes-content match against crash-day signature vocabulary
  4. Calendar event in lead-up (once calendar binding event-type tags land)
  5. "No signal" — honest fallback
- [ ] Decide whether attribution is per-dip or per-dip-cluster (15
      clusters covering 45/79 dips). Cluster-level may be more useful
      for the "rough patch" narrative.
- [ ] May depend on dip_v2 split (almost-crash vs mood-only) — gated
      on H04b. If dip_v2 lands first, attribution can be subtype-aware.
- [ ] Tone: descriptive, no prescription. "What was happening?" not
      "you should have rested."

---

### C.7 — Intervention tagging

**Intention.** Foundation work for the eventual shielder-vs-reliever
experiment (the pacing-doc's eventual payload — Tier 3 (j) in
STOCKTAKE). Tag interventions taken (rest day, supplement,
medication, pacing change, social withdrawal) so we can later ask
"did intervention X reduce crash depth or recovery time?"

**Gate.** *v2 territory.* Substantial design work; cardinal-principle
applies — research first, build second.

**TODOs (when un-gated).**
- [ ] Cardinal-principle research first: characterise existing
      intervention language in the 686 notes BEFORE designing UI.
      Likely a "Goal C" round of notes analysis (parallel to Goal A
      crash-language and Goal B tagging-suggestion).
  - frequencies of mention (rust, medicatie, supplement names,
    pacing-vocabulary)
  - co-occurrence with crash / dip / recovery days
  - whether interventions are stated as planned ("ga vandaag rusten")
    vs done ("heb gerust") vs effective ("rust hielp")
- [ ] Design the tag taxonomy. Curated list vs user-defined vs both
      (with curated as starter). Locked-tag-categories memory
      ([project_tag_clusters](../../C:/Users/Gebruiker/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_tag_clusters.md))
      already has `interventie` as one of the eight v1 categories —
      use it.
- [ ] Decide tagging mechanic:
  - inline in daily-entry tag picker?
  - separate "reflection" prompt at the end of the day?
  - retrospective tagging from the timeline view?
- [ ] Decide quantification: binary (tagged y/n) or graded (low /
      medium / high effort)?
- [ ] Hard pre-condition: H05b sustained-recovery primitive (Tier 3
      below) must be working — otherwise there is no "did the
      intervention help?" axis to measure against.

---

### H04b — Decode `unknown_233` for per-minute Body Battery

**Intention.** Unlock per-minute Body Battery data for intra-day
analyses. Specifically: count *occurrences* of BB-rise and BB-drop
events per day (the participant's framing that rises like a
middagslaap are themselves meaningful, not just totals). Unblocks
H03b (overnight BB recharge) and dip subtyping (dip_v2).

**Status (revised 2026-06-07).** **Promoted to top of Upcoming**
after HA10's validate-era SUPPORTED finding triggered the §9
pre-commit AND the HRV-not-in-local-data discovery created a
second urgent need for path C authorisation. See the new
"H04b path C authorisation" entry at the top of Upcoming.

Protocol fully locked at
[.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md).
Folder scaffolded at
[garmin/hypotheses/H04b-decode-unknown-233/](garmin/hypotheses/H04b-decode-unknown-233/)
(empty, awaiting execution).

**Gate.** ~~Notes label-quality work (participant-requested) must
complete first.~~ **Gate softened 2026-06-07** after HA10 +
HA07-blocked discovery: H04b path C authorisation is now
independently justified by the per-minute BB need (HA10 sharpening)
and the HRV need (HA07/HA08/HA09/HA12 unblocking). Notes work
remains valuable but no longer a hard pre-condition.

**TODOs (when un-gated).**
- [ ] **Path C — Garmin Connect REST API.**
  - Stand up `cyberjunky/python-garminconnect`. Auth flow with the
    participant's Garmin Connect credentials, stored locally only.
  - ToS-grey awareness: internal endpoint
    `/wellness-service/wellness/bodyBattery/events/{date}`. Accepted
    for personal-use own-data analysis only.
  - Pull per-minute BB for the full corpus 2022-09-03 → 2026-06-05.
    Rate-limit-aware; expect this to take real wall-clock time.
  - Store as tall CSV `(date, timestamp, bb_value)` outside the app
    tree at `C:\Users\Gebruiker\Documents\gevoelscore-data\garmin
    data\bb_per_minute\` (mirror the GDPR-dump location convention).
- [ ] **Path B — Decode `unknown_233` from FIT.**
  - Extract raw `unknown_233` 4-byte payloads from a stratified sample
    of `monitoring_b` files (use the 60-file sample shape from
    `02_profile_monitoring_density.py` as a baseline; expand if needed).
  - Test ~12 candidate byte encodings against the Path C ground truth
    on a 180-day holdout (pre-registered, locked in the plan):
    b3 direct, b2:b3 int16 scaled, byte-delta, off-wrist flag in b1,
    etc.
  - If no direct encoding works: three pre-locked fallback strategies
    (joint-channel regression, state-buffer reframing, raw-stream
    feature mining).
  - Write up findings — small public contribution if direct decode
    succeeds (HarryOnline community sheet, FIT-SDK forum thread).
- [ ] After either path produces per-minute BB:
  - per-day feature extraction: rise-count, drop-count, rise-rate,
    time-of-day-of-lowest, drain-during-waking-hours.
  - join into the daily wide table for hypothesis testing.

---

### H03b — Overnight Body Battery recharge *(EXECUTED 2026-06-07; INCONCLUSIVE × 12 by data availability)*

**Status update 2026-06-07.** H03b ran under its locked
hypothesis.md spec. Data-availability investigation surfaced two
Garmin API cutover dates (`bodyBatteryChange` from ~2023-12-31;
`sleepBodyBattery` from ~2024-06-03). Of 29 crash episodes, only
6 of 15 validate crashes have both per-minute data AND a usable
lagged baseline (train: 0 of 14). All 12 evaluation cells returned
INCONCLUSIVE under the locked n_clean ≥ 10 threshold. User
pre-committed to running as-locked rather than lowering the
threshold mid-run (which would have created H03c per playbook
§2.2). Result:
[H03b result.md](garmin/hypotheses/H03b-bb-overnight-recharge-permin/result.md).

**Endpoint clarification audit trail (per playbook §2.5)**:
hypothesis.md §3 specified `/wellness-service/wellness/bodyBattery/events/{date}`;
this endpoint returns event records (sleep/activities/naps), NOT
per-minute samples. The per-3-min BB during sleep window IS
available via `get_sleep_data().sleepBodyBattery` (captured by
existing path C sleep backfill; no separate BB backfill needed).
Implementation-source clarification, not a spec change.

**HA10 stays canonical for the BB overnight recharge channel** —
SUPPORTED validate at +16.2 pp, v2 RESCUE Cat 3, currently
load-bearing as corroborating secondary anchor for validate-era.

**Re-runnable only after**: path B FIT decode of `unknown_233`
unlocks per-minute BB for the old corpus (2022-09 to 2024-06).
See "H04b — Decode unknown_233 for per-minute Body Battery" entry.

**Methodology lesson banked (queued for playbook §3 addendum
consideration)**: when a pre-registered hypothesis depends on a
third-party API endpoint, verify data availability across the
analysis window BEFORE locking the inconclusive threshold. The
H03b case shows an n=10 threshold combined with a 2024-06 data
cutover automatically forces INCONCLUSIVE for any test using
2024+ data only.

**Original intention (preserved for re-run context).** Replaces
H03 (sleep efficiency, refuted decisively). Tests whether
overnight BB recharge is a physiologically targeted marker of
unrefreshing sleep — a sleep precursor whose channel is BB not
efficiency. The hypothesis.md spec is locked and stays as the
re-run target if path B succeeds.

---

### Tier 3 — H05b spec (sustained-recovery target)

**Intention.** Recovers the H05 recovery-time card concept after the
v1 spec produced trivial 0-day recoveries (recovery target
`baseline − 1` was met definitionally the day after episode end). C.4
above is the monthly aggregation that builds on this primitive.

**Gate.** None — cheap to run, deferred only by priority.

**TODOs.**
- [ ] Lock new spec. Current candidate (from
      [registry.md §4](garmin/hypotheses/registry.md)): recovery =
      first day of a ≥2-consecutive-day sustained run with
      `score ≥ pre-episode baseline rounded down`.
  - "Pre-episode baseline" — define precisely. 30-day rolling
    median ending D-4? D-7?
  - "Rounded down" — keep, since baselines are typically 4.x.
  - Edge case: what if recovery is never sustained (the participant
    moves into a new lower baseline)? Cap at N days and report as
    "no sustained recovery within window."
- [ ] Same crash_v1 episodes (29).
- [ ] **3-episode dry-run print** before finalising — banked
      methodology lesson from H03 and H05 v1.
- [ ] Descriptive only — no prediction bar. Output median, IQR,
      range of recovery time.
- [ ] Feeds into C.1 lock (see Open question) → unblocks C.4.

---

### Tier 3 — Dictionary v3 (polarity-negation handling)

**Intention.** Cheap fix to a known bug in the notes v2 dictionary.
Substring matching for `polarity_positive` does not apply the 3-word
negation window that symptom matching does — so "het is echt **niet
fijn**" fires positive because "fijn" matches.

**Gate.** None — cheap, deferred only by priority. Estimated effect:
flips 1–2 of the 16 late-era positive-dominant crash days that the
verification round surfaced (real but small).

**TODOs.**
- [ ] Extend the v2 3-word negation window to polarity markers as
      well (same logic, applied to a different marker class).
- [ ] Re-run the v2 analyses end-to-end with v3:
  - clause-categorisation per day
  - era-shift table (notes v2 finding b — mixed-day topology +39 pp)
  - polarity-dominance counts on late-era crash days
- [ ] Report which v2 conclusions changed and which were robust to
      the v3 fix. The expected outcome (per the verification round):
      finding b is mostly robust; the absolute positive-dominant
      count for late-era crashes shifts by 1–2 days but the +39 pp
      direction holds.
- [ ] Update `categories-analysis-v2.md` with a v3 amendment, not
      a fresh document, unless changes are pervasive enough to
      warrant a separate write-up.

---

*Living document. Items move from Upcoming to Deferred (or vice
versa) as gates open and priorities shift. When an item is started,
record the start date here and link to its working folder; when
closed, link to its result writeup and remove from this list.*
