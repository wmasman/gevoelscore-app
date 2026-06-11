# Reply to the variable-architecture review — with HA07d context

*Reply written 2026-06-07 in response to [the independent reviewer
write-up](2026-06-07-variable-architecture-review.md) by the
project's research lead. The review was written before the HA07c +
HA08c + HA07d substitute tests landed; HA07d became the project's
first overall-SUPPORTED test under the canonical bar. This reply
acknowledges the critique, updates the assessment where new findings
change the picture, and commits to a concrete action programme.*

---

## 1. Why this reply exists

The reviewer's critique is substantive and lands hard in several
places. Most of it remains valid after HA07d. Some pieces are
materially superseded by HA07d's overall-SUPPORTED finding and the
sleep-stress proxy results around it. The project should explicitly
record which critiques were resolved, which still apply, and which
require structural changes the project will queue rather than
adopt immediately.

The reviewer's chief move is **promoting "era" from a split-variable
to a first-class moderator variable in the framing layer**. HA07d's
both-eras-SUPPORTED-with-opposite-direction finding is, in effect,
an empirical anchor for that reframe. The project should adopt the
reframe in the narrative layer; the analytical apparatus is already
doing it in practice.

This reply is structured to mirror the review, section by section.

---

## 2. Reply to §2 — The dependent variable

### Critiques resolved or partially superseded

None. The dependent-variable critiques apply unchanged.

### Critiques still in force

- **Power is structurally bounded (14 train, 15 validate).** HA07d
  +19.6 / +21.7 pp is now the cleanest project finding but the N is
  the same. A single re-labelled episode would shift HA07d validate
  from +21.7 pp (clear) to roughly +14.4 pp (one below the bar). The
  reviewer's point about "marginal results sit within plausible
  relabel drift" is exactly correct.

- **Score is ordinal under cognitive load.** Brainfog self-report
  is bounded above by labeller-noise. The reviewer's framing
  applies sharply to *any* result with discrimination near the bar
  — including HA10 validate (+16.2 pp, 1.2 pp above bar) and the
  sub-N_std=2.0 arms of HA07d.

- **The dip/crash cleavage is a definitional, not biological, line.**
  Score 4 → 3 → 3 → 4 vs 4 → 3 → 4 → 3 → 4 still rests on the
  participant's day-by-day choice of when to register a "3". This
  has not been addressed.

- **`crash_v1` mixes mechanisms.** Still stated as a caveat in
  every result.md, still not operationalised away. The notes-driven
  mechanism categorisation is queued.

- **The score has no pre-illness baseline.** Stabilisation framing
  reframes this honestly but does not remove the asymmetry.

### Committed actions

- **Crash_v3 mechanism subtyping (from notes)** is now the highest-
  leverage outcome-side improvement, per the reviewer. Added to
  QUEUED-WORK Tier 2 with cross-link to the notes-quality work.
- **S02 score trajectory** added to QUEUED-WORK Tier 2 alongside S01.
- **Power-bounded honesty added to every future result.md** as a
  one-line caveat ("at N=14/15, +X pp discrimination is Y
  re-labellings from refutation").

---

## 3. Reply to §3 — The independent variables

### Critiques resolved or partially superseded

- **"None of the tests SUPPORT under the strict locked rule"** —
  superseded. HA07d (sleep stress variability delta, 4d primary
  bidirectional) SUPPORTS BOTH eras at +19.6 / +21.7 pp under the
  same locked rule that refuted HA01b. The "near-zero overall-
  SUPPORTED tally" the reviewer flagged is now "one overall-
  SUPPORTED" — small in count but qualitatively new.

### Critiques still in force, sharply

- **Channel independence overstated by the framing.** This is the
  reviewer's most important framing critique and HA07c/HA08c/HA07d
  make it *worse*, not better, for the synthesis: three of the
  seven train-era SUPPORTED tests are sleep-stress primitives
  (mean delta, slope, variability delta) sharing the same input
  signal. The project's "seven channels SUPPORTED" framing is
  inflated. **Correct framing: six distinct channels, one of which
  (sleep stress) has three primitives SUPPORTED in train.** The
  synthesis and STOCKTAKE must be edited to reflect this. *Action
  committed* — see §6 below.

- **HA10 is threshold-fragile and remains the project's most
  fragile headline.** HA10 validate SUPPORTED only at N_std=1.5
  bidirectional, refuted at N_std=2.0 and 2.5. The reviewer's
  diagnosis (signal sits in the loose-deviation tail, opposite of
  threshold-monotonic) stands. **HA07d does NOT inherit this
  fragility** — it SUPPORTS at N_std=1.5 AND N_std=2.0 in both
  eras, with the lowered arm extending to +28.5 pp at N_std=2.0
  validate. HA07d should now be framed as the *primary* validate-
  era anchor; HA10 as corroborating-but-fragile. *Action
  committed.*

- **Opacity asymmetry across channels.** BB algorithm opacity
  remains high. HA10 is the most opacity-exposed validate-era
  anchor; HA07d (sleep stress) inherits stress-algorithm opacity
  which is moderate (the per-minute integer is opaque in its
  derivation but stable in its meaning). The validate-era picture
  rests harder on the moderate-opacity channel than on the
  high-opacity channel — net improvement in opacity exposure.

- **Generation 1 verdicts methodologically dated.** H01 (RHR
  rolling baseline), H03 (sleep efficiency), H04 (BB net delta)
  have never been re-tested at Gen 3 standards. HA06b re-tested
  the RHR channel at Gen 3 and found train SUPPORTED, so the H01
  re-test is partly absorbed; but H03/H04 are genuinely
  unaddressed. *Action committed* — H01-Gen3, H03-Gen3, H04-Gen3
  added to QUEUED-WORK Tier 2.

- **HA11 U-dip detector has parameter degrees of freedom not
  externally anchored.** Still applies. HA11's train-SUPPORTED is
  a load-bearing finding in the seven-channel synthesis; a
  sensitivity check on the U-dip parameters is cheap and would
  either strengthen or weaken the finding. *Action committed* —
  HA11 parameter sensitivity diagnostic added to QUEUED-WORK
  Tier 2.

- **HA01b per-axis decomposition still pending.** Theme A
  withdrew HA01b's headline; the per-axis decomposition was
  reported descriptively but not formally analysed against the
  composite. *Action committed* — added to QUEUED-WORK Tier 2.

- **Sleep architecture (H03b)** — replaced by H03b proper which
  is gated on the path C backfill currently running. *Already
  in-flight*; no action change.

### Committed actions

- **Channel framing fix** in STOCKTAKE, synthesis.md,
  pem-pacing-indicators.md, RESEARCH-REPORT-ADDENDUM.md: change
  "seven channels SUPPORTED" to "six channels SUPPORTED (with the
  sleep-stress channel tested through three primitives, all of
  which SUPPORTED in train)."

- **HA10 threshold-fragility honest framing** in STOCKTAKE
  headline + §4 b2 card section + RESEARCH-REPORT-ADDENDUM §5.20.
  HA07d becomes the primary validate-era anchor; HA10 secondary
  with explicit fragility caveat.

- **HA10 threshold-monotonicity diagnostic** queued as cheap
  follow-up. Pre-register before running.

- **HA01b per-axis decomposition** queued. Cheap, would clarify
  what the composite hides.

- **Gen-3 re-tests of H01 / H03 / H04** queued. H01 partly
  absorbed by HA06b (different primitive but same channel); H03
  and H04 are unaddressed.

- **HA11 parameter sensitivity diagnostic** queued. Cheap.

- **Cross-channel correlation matrix** queued. Empirically anchors
  the channel-non-independence caveat with a number rather than
  a sentence.

---

## 4. Reply to §4 — The inferential apparatus

### Critiques resolved or partially superseded

- **"No overall-SUPPORTED finding"** — superseded by HA07d.
- **"Era is better treated as a moderator than a generalization
  gate"** — HA07d directly empirically vindicates this. The
  bidirectional primary captured the train side (volatility
  signature) AND the validate side (stillness signature) on the
  SAME channel via the SAME metric. This is era-as-moderator at
  the single-test level. The narrative layer should adopt the
  reframe.

### Critiques still in force

- **The both-eras rule is more stringent than scientific practice
  normally demands.** Conservative for the feature-design use-case;
  produces a narrative where era-specific findings get buried as
  failures. *Action committed* — adopt era-as-moderator framing
  in narrative documents (STOCKTAKE headline, synthesis, addendum),
  but keep the locked rule in result.md verdicts. Two-language
  approach: "OVERALL REFUTED per locked rule, train-era SUPPORTED
  as findings under era-moderator framing" — both true,
  reader chooses which lens is relevant.

- **N=15 per era is power-bounded; no Fisher's exact / CI on
  primary verdicts.** Still applies. *Action committed* — add
  Fisher's exact p-values and binomial 95% CIs to all primary
  verdict tables going forward. Retrospectively add to HA07d /
  HA10 / HA06b / HA11 result.md files in the next pass.

- **Multi-comparison within sensitivity arms is post-hoc.** Pre-
  registration locks the *primary* arm; the all-combinations
  table contains "interesting" arms. HA10's "5d secondary one-
  sided elevated SUPPORTED at +27.5 pp" is exactly the kind of
  post-hoc combination the reviewer flags. **HA07d does not
  inherit this** — its primary IS the bidirectional, which
  SUPPORTS. The 28.5 pp at N_std=2.0 validate is secondary and
  flagged as such. *Action committed* — explicit "PRIMARY vs
  SECONDARY arm" labelling in result.md tables.

- **Null sample autocorrelation isn't explicitly handled.**
  Block-bootstrap would be more rigorous. *Action committed* —
  add to QUEUED-WORK Tier 3 (methodological refinement; not
  expected to materially shift verdicts but would tighten claims).

- **Audit-trail when a methodological flaw is caught remains
  the gold standard** — the reviewer's praise here applies
  equally to the HA07/HA08 → HA07c/HA08c/HA07d pivot. The
  substitute pre-registrations were locked before any data
  inspection, methodology integrity preserved.

### Committed actions

- **Fisher's exact p-values and binomial 95% CIs** added to all
  primary verdict tables in current result.md files and required
  for all future result.md files.

- **Primary vs secondary arm labelling** in all combination
  tables.

- **Era-as-moderator narrative reframe** in STOCKTAKE / synthesis
  / addendum. The locked verdicts stay; the narrative around them
  changes.

- **Block-bootstrap null sample** queued at Tier 3.

---

## 5. Reply to §5 — Dependent–independent relationship across research aims

### Aim 1 — Descriptive characterisation

Reviewer says this is the project's strongest evidence base. Still
true. HA07d adds **era directionality reversal on a single
channel** as a tenth-plus axis on the "kind of crash changed"
theory. The descriptive arc gains a new dimension: it's not just
that crashes are fewer / shorter / shallower / mixed-day / less-
warned / cognitive — it's that the AUTONOMIC FLEXIBILITY axis
flips between eras (volatile → still). Single-channel internal
consistency.

### Aim 2 — Precursor / predictive correlations

Reviewer flags this aim as where the project is most conservative.
HA07d adds a finding that survives the conservatism. The reviewer's
"the framing reads era-specific findings as failures" critique is
addressed by the era-as-moderator reframe.

### Aim 3 — Post-event retrospective indicators (cards)

**Reviewer flagged this as the project's most under-instrumented
aim relative to its product-criticality.** This remains correct
and is now more urgent given that two cards (b + b2) are
empirically ready to prototype.

The reviewer's specific critique: "discrimination at +16 pp" ≠
"card is right when it fires." For HA07d validate (86.7% freq /
65% null): if the card fires, the conditional probability of a
crash within the next 4 days is dominated by the base rate. The
participant has ~15 validate-era crashes in ~890 days, base rate
1.7%. Bayes: P(crash | card fires) = (0.867 × 0.017) / (0.867 ×
0.017 + 0.65 × 0.983) ≈ **2.3%**. The card fires on 65% of days
but tells the truth ~2 in 100 times when it fires.

This is not a usable predictive card. The retrospective framing
(card explains a crash *after* the crash) is the right framing
for the product, but even the retrospective framing has a
specificity issue: of all the days that LOOK like the pattern,
only a small fraction precede crashes.

**Action committed** — explicit specificity / precision /
posterior-probability framing for every card concept BEFORE
card.md is written. Card text must be calibrated to actual
posterior probability, not to discrimination magnitude.

---

## 6. Synthesised position after HA07d

The reviewer's chief structural recommendation — **era as moderator,
not split** — is empirically vindicated by HA07d. The narrative
reframe is therefore not a choice between conservatism and
permissiveness; it's the right reading of the data we actually have.

Adopting it changes the project's story from:

> "After 19 hypotheses we finally got one to clear both eras at the
> strict bar."

to:

> "The autonomic-deviation precursor is era-moderated. Pre-cliff
> crashes are preceded by autonomic VOLATILITY (variability shifts
> in either direction, elevated stress, elevated RHR, elevated U-dip);
> post-cliff crashes are preceded by autonomic STILLNESS (variability
> collapse, elevated BB peak / paradoxical 'great recharge'
> appearance). HA07d demonstrates this directly on a single channel:
> bidirectional primary SUPPORTS both eras, with train showing
> both elevated AND lowered arms, validate showing only lowered.
> The era contrast is the project's central result."

Both readings are honest. The second is more useful for the feature
design downstream.

The reviewer's framing-layer critiques (channel-independence
overstatement, HA10 fragility, card specificity) are corrective
fixes that the project should adopt regardless of HA07d. The
empirical recommendations (Gen-3 re-tests, per-axis decompositions,
Fisher's exact, threshold monotonicity, cross-channel correlation)
are cheap and would strengthen the project's defensibility.

The single most under-instrumented aim — retrospective cards — is
the one the participant will actually meet. The reviewer's call
for specificity / precision framing before card.md is written is
correct and time-sensitive (the b + b2 cards are now empirically
ready to prototype).

---

## 7. Action programme

### Tier 1 (apply now, this session)

1. **STOCKTAKE.md headline:** rewrite to acknowledge "six channels
   SUPPORTED with sleep-stress having three primitives" (not "seven
   channels"). HA10 fragility flagged. HA07d as primary validate
   anchor; HA10 as corroborating-but-fragile.
2. **STOCKTAKE.md §4 cards:** add card specificity / precision
   caveat before any card prototyping starts.
3. **synthesis.md:** apply the channel-framing fix in the latest
   update section.
4. **RESEARCH-REPORT-ADDENDUM.md §5.20:** add HA10 fragility +
   HA07d-as-primary-anchor framing.
5. **pem-pacing-indicators.md §6:** apply channel-framing fix +
   card specificity caveat.

### Tier 2 (queue now, do later)

6. **HA10 threshold-monotonicity diagnostic** — cheap, urgent.
7. **HA01b per-axis decomposition** — cheap.
8. **H01-Gen3 / H03-Gen3 / H04-Gen3 re-tests** — cheap (re-use
   existing data, swap in lagged baseline + z-score + bidirectional).
9. **HA11 U-dip parameter sensitivity diagnostic** — cheap.
10. **Fisher's exact + binomial 95% CIs** added to HA07d / HA10 /
    HA06b / HA11 / HA07c / HA08c result.md files retroactively;
    required for all future result.md files.
11. **Cross-channel correlation matrix** for the seven SUPPORTED
    primitives.
12. **Specificity check** for HA07d + HA10 (the b2 card anchors).
13. **Crash_v3 from notes** mechanism subtyping (highest-leverage
    outcome-side improvement).
14. **S02 score trajectory** alongside S01.
15. **Pooled-corpus descriptive arm** alongside primary verdicts.

### Tier 3 (deferred, methodological refinement)

16. **Block-bootstrap null sample** for autocorrelation rigor.
17. **Era-as-moderator formal analysis** (Cochran's Q / I²-style
    heterogeneity test) on the multiple per-era effect sizes.

### Tier 4 (already in-flight or covered)

18. H03b sleep-architecture / per-minute BB — backfill running in
    background.
19. The pivot from HA07/HA08 → HA07c/HA08c/HA07d already followed
    the reviewer's "find a defensible proxy" advice.

---

## 8. What the reviewer got most right

The reviewer's chief contribution is the **framing-layer critique**.
The analyses are solid; the synthesis around them was overstating
in places where humility was warranted (channel independence,
threshold robustness, card specificity) and understating in places
where era-specific findings were findings (era-as-moderator).

Adopting the framing fixes does not weaken the project; it
*sharpens* its claims to what the data actually supports. After the
edits committed in §7, the project's story becomes more defensible
AND more interesting:

- **Pre-cliff (2022-23) era**: autonomic volatility precursor on
  six channels, with the sleep-stress channel especially robust
  (three primitives all SUPPORTED).
- **Post-cliff (2024+) era**: autonomic stillness precursor on two
  channels (HA07d sleep stress variability collapse as primary
  anchor; HA10 elevated BB peak as corroborating fragile anchor).
- **HA07d** is the single test demonstrating the era reversal at
  the channel level, providing the strongest single piece of
  evidence the era is the right moderator variable.
- **Cards** (b train-era + b2 validate-era) are empirically
  anchored but require specificity-aware framing before they ship.
- **Gen-3 re-tests + per-axis decompositions + parameter
  sensitivity diagnostics** are the project's cheap-and-cheerful
  next moves to tighten the existing claims.

---

## 9. What the reviewer might revisit

A few items where the reviewer's framing would benefit from an
update:

- The "fragile HA10 is the project's only validate-era SUPPORTED"
  framing is now obsolete; HA07d is the primary validate-era
  anchor. The reviewer's HA10-specific critiques about threshold-
  monotonicity remain valid for HA10 itself, but the validate-era
  picture as a whole is much more robust than the review suggests.
- The "no overall-SUPPORTED tally" framing is updated by one,
  qualitatively. The reviewer's broader point (the locked rule
  produces a narrative that buries era-specific findings as
  failures) still applies to most of the test family, but HA07d
  itself is a counter-example.

These are not corrections to the review; they are HA07d-arrival
updates the review's author should be aware of when re-reading.

---

*Reply locked 2026-06-07. Linked from STOCKTAKE.md and
synthesis.md as the project's response to the variable-architecture
critique. The Tier 1 edits land in the same session; Tier 2/3
queued in [QUEUED-WORK.md](../../QUEUED-WORK.md).*
