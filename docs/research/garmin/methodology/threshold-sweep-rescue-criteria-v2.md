# Threshold-sweep rescue/close/ambiguous criteria — v2 methodology

**Locked 2026-06-07** in response to the HA07d threshold-monotonicity
diagnostic v1 CLOSE verdict in both eras (2026-06-07), which
revealed that the v1 locked criteria captured only *one* form of
robust signal shape (canonical decline from peak at loose threshold,
Spearman rho ≤ −0.3) and penalised other forms of robust shapes
that the participant's data demonstrably contains.

This document **locks v2 criteria** as a separate methodology
document — separate from any specific test's hypothesis.md or
diagnostic.md — so that the criteria revision applies to the
**whole family of tests** that use a threshold-tier sweep as a
robustness diagnostic. Per the user-locked Option C, v2 criteria
must be applied **symmetrically** to all relevant tests: any
finding that RESCUES under v2 gets load-bearing status restored
with the revised-criteria reasoning cited; any that doesn't keeps
the permanent demotion.

## 1. Scope of this document

The v2 criteria apply to:

- Tests that produced a `SUPPORTED` verdict on a primary
  arm at the project's pre-registered threshold tier (typically
  N_std = 1.5), AND
- For which a fine-grid threshold sweep is computable from the
  test's data + machinery without re-running the test.

Specifically, the v2 criteria are locked for application to:

- **HA10 threshold-monotonicity diagnostic v2** (re-evaluates the
  HA10 v1 CLOSE).
- **HA07d threshold-monotonicity diagnostic v2** (re-evaluates the
  HA07d v1 CLOSE both eras).
- **HA06b threshold-monotonicity diagnostic v2** (new diagnostic,
  no v1 existed; HA06b train SUPPORTED at primary 4d N_std=1.5
  bidirectional +18.9 pp).
- **HA11 threshold-monotonicity diagnostic v2** (new diagnostic,
  no v1 existed; HA11 train SUPPORTED at primary 4d N_std=1.5
  one-sided elevated +22.8 pp).

The v2 criteria are explicitly **not** applied to:

- Tests that use a different metric primitive (e.g. H02b's
  "minutes ≥ +10" rather than z-score against a personal baseline)
  — those would need a separate diagnostic framework.
- Tests that have not been pre-registered with a threshold-tier
  primary arm.

Future pre-registered tests may either explicitly reference v2
criteria in their hypothesis.md or pre-register their own
diagnostic framework if v2 doesn't apply. If a future test does
both (passes its locked verdict at N_std=1.5 AND wants a
robustness diagnostic), v2 is the default.

## 2. Honesty caveat on locking now

The v2 criteria are locked **after** the v1 CLOSE verdicts have
been observed on HA10 and HA07d. This is the precise situation in
which motivated reasoning is most concerning — the locked criteria
are being revised after they produced an inconvenient verdict on
findings the project would prefer to retain.

The discipline binds because:

1. The v1 verdicts on HA10 and HA07d **remain in force** — they
   have already been propagated to synthesis-level docs, locked
   verdicts demoted to non-load-bearing, card (b2) stripped of
   anchors. The pre-registration discipline cost of v1 has
   already been paid before v2 is locked.

2. The v2 criteria are **locked symmetrically** — applied to ALL
   four findings (HA10, HA07d, HA06b, HA11), not just to HA07d.
   To prevent the interim-asymmetry escape hatch flagged by
   the peer reviewer, **HA06b and HA11 are also demoted to
   "load-bearing pending v2"** in synthesis-level framing until
   their v2 diagnostics complete. Atomic restoration follows
   atomic demotion.

3. The v2 criteria are **locked as a methodology document** —
   referenced by all four v2 diagnostic.md files, not embedded
   inside one of them. This prevents incremental criteria
   adjustments inside any individual diagnostic.md.

4. The v2 criteria are pre-registered **as a five-category shape
   rule** based on signal-detection-theory principles. The
   shape-category logic (decline / plateau / rising / bumpy /
   loose-tail) is theoretically grounded. **The quantitative
   thresholds** (e.g. ≥ +15 pp plateau floor, ≥ +7 pp at N_std=2.5
   for Cat 1, restricted range [1.0, 3.0]) are partly empirically
   calibrated against the curves the v1 diagnostics produced.
   This is named explicitly here so the calibration cannot be
   re-argued post-hoc.

5. **Honest worked example before locking**: hand-walking HA07d
   train bidirectional through the v2 criteria below produces
   **RESCUE** (Cat 3: rising/late-peak, peak at N_std=1.75 with
   disc ≥ +15, sustained positive across the meaningful range,
   zero sign-changes in [1.0, 3.0]). This contradicts the
   researcher's earlier intuitive prediction (which had said HA07d
   train would CLOSE because of curve "bumpiness"). The discipline
   binds against the researcher's intuition: the curve's
   bumpiness in raw direction-reversals is real but does NOT
   include sign-changes in the meaningful range, and Cat 4 fires
   on sign-changes (zero-crossings), not direction-reversals.
   This consequence is named here so the synthesis update after
   v2 runs is not "surprised" by it.

   Same hand-walk: **HA10 validate bidirectional** also produces
   RESCUE (Cat 3); **HA07d validate bidirectional** produces
   RESCUE (Cat 2: stable plateau). All three findings whose v1
   verdicts were CLOSE likely rescue under v2 strict reading.
   Card (b2) anchors may be restored after the diagnostics run
   and confirm these expectations. HA06b and HA11 verdicts are
   genuinely unknown (their fine grids have not been computed)
   and remain pending.

## 3. The five-category shape rule

For each (era, direction) pair tested on the fine N_std grid
[0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5,
4.0], compute the discrimination-vs-threshold curve and classify
its shape per the five categories below.

### 3.0 Definitions locked

The following terms are used in the categories below. Lock them
explicitly to prevent ambiguity:

- **Meaningful range**: N_std ∈ [1.0, 3.0] inclusive (9 tiers).
  All shape statistics are computed on this restricted range,
  not the full grid. The grid extremes (0.5, 0.75 at the loose
  end; 3.5, 4.0 at the strict end) are reported for completeness
  but do not enter the verdict computation. Rationale: at
  N_std < 1.0 the null rate is near saturation (most random
  windows trigger), making discrimination noise-dominated; at
  N_std > 3.0 the null rate is near zero (few random windows
  trigger), making discrimination dominated by tiny null
  fluctuations.

- **Sign-changes count**: count of i ∈ [first_meaningful,
  last_meaningful − 1] such that
  sign(disc[i]) ≠ sign(disc[i+1])
  where sign is +1 for disc > 0, −1 for disc < 0, undefined for
  disc = 0 (in which case the comparison skips that point and
  joins the next). This counts **zero-crossings** of the
  discrimination curve, NOT direction reversals (where slope
  changes sign). A curve that rises then declines without
  crossing zero has 0 sign-changes regardless of how bumpy the
  rise or decline. A curve that crosses from positive to
  negative has 1 sign-change.

- **Direction reversals** (NOT used in verdict logic; reported
  for descriptive context only): count of i where
  sign(disc[i+1] − disc[i]) ≠ sign(disc[i+2] − disc[i+1]).
  Counts changes in slope direction. A bumpy-but-positive curve
  has many direction reversals but possibly 0 sign-changes.
  This statistic is reported in result.md for descriptive
  purposes but does NOT trigger Cat 4.

- **Peak N_std**: the N_std at which discrimination is maximised
  across the meaningful range [1.0, 3.0]. If multiple tiers have
  the same maximum, the lowest N_std is used.

- **Peak disc**: maximum discrimination across the meaningful
  range [1.0, 3.0].

- **Spearman rho**: rank correlation between N_std and
  discrimination across the meaningful range [1.0, 3.0]. Negative
  rho indicates discrimination declines as N_std rises (canonical
  shape).

- **Max negative disc**: minimum discrimination value across the
  meaningful range [1.0, 3.0]. Negative if any tier in the range
  shows inverse signal.

These definitions apply to all five categories unless explicitly
overridden.

### Category 1 — Canonical decline (PASS)

**Definition**: Discrimination peaks within the meaningful range's
loose half (peak N_std in [1.0, 1.5]) and decreases as threshold
tightens. The classical "real signal embedded in noise" shape.

**Locked criteria** (all required, using definitions in §3.0):
- Peak N_std ∈ [1.0, 1.5].
- Spearman rho (N_std, disc) ≤ −0.3 (monotonic decline at
  rank-correlation level within meaningful range).
- Sign-changes count ≤ 1.
- Discrimination at N_std = 2.0 ≥ +10 pp.
- Discrimination at N_std = 2.5 ≥ **+7 pp** (raised from v2 draft
  +5 pp per peer-review concern #3: a +5 pp floor at strict tier
  was a generous interpretation of "robust signal survives";
  +7 pp is the locked floor).

**Interpretation**: signal is strongest at the locked test's
primary threshold and weakens at strict tiers as expected.

### Category 2 — Stable plateau (PASS)

**Definition**: Discrimination is sustained across a wide
threshold range without strong decline. The "signal-to-noise
ratio is favourable across many threshold choices" shape.

**Locked criteria** (all required, definitions per §3.0):
- Discrimination > +15 pp at ≥ 4 contiguous grid tiers within the
  meaningful range [1.0, 3.0], including at least one tier in
  [1.0, 1.5] AND at least one tier in [2.0, 2.5].
- (Max discrimination − min discrimination across the plateau
  region) ≤ 50% of the maximum discrimination. The "plateau
  region" is the longest contiguous run of tiers > +15 pp within
  the meaningful range.
- Sign-changes count ≤ 1 (in meaningful range per §3.0).

**Interpretation**: signal holds across multiple threshold
choices. This is a MORE robust shape than canonical decline
because the signal doesn't drop off at stricter thresholds.

### Category 3 — Rising / late-peak (PASS)

**Definition**: Discrimination is positive across the meaningful
range and peaks at a strict threshold tier (peak N_std > 1.5).
The "signal-to-noise ratio improves at strict thresholds because
noise drops faster than signal" shape.

**Locked criteria** (all required, definitions per §3.0):
- Peak N_std > 1.5 (within meaningful range [1.0, 3.0]).
- Discrimination ≥ +15 pp at peak.
- Discrimination ≥ +10 pp at N_std = 2.0.
- Sign-changes count ≤ 1 (in meaningful range).
- Discrimination > 0 at ALL tiers in [1.0, peak] inclusive (signal
  positive across the rise to peak).

**Interpretation**: this is a robust signal that the v1 criteria
were specifically broken on. The signal's strength rises as the
threshold tightens, because at strict thresholds, the few null
windows that still trigger are increasingly outnumbered by crash
windows that still trigger. This is *more* discriminating, not
less.

**Note**: Cat 3 does NOT require Spearman rho ≤ −0.3 because
rising/late-peak shapes have rho ≥ 0 by construction in the
ascending portion. This is the specific defect in v1 criteria
that v2 corrects.

### Category 4 — Bumpy with sign changes (FAIL)

**Definition**: Discrimination crosses zero or shows a large
negative deviation within the meaningful range. Catches curves
where the test's verdict could flip direction depending on which
threshold tier is chosen.

**Locked criteria** (any triggers FAIL, all in meaningful range):
- Sign-changes count ≥ 2 (per §3.0 — zero-crossings, NOT direction
  reversals).
- Spearman rho (N_std, disc) in [−0.1, +0.1] AND any tier shows
  discrimination ≤ −5 pp.
- Maximum negative discrimination across the **meaningful range**
  [1.0, 3.0] ≤ −10 pp.

**Interpretation**: the curve genuinely flips direction or has
substantial inverse signal at some threshold within the meaningful
range. This indicates threshold-instability of verdict.

**Note on bumpy-but-positive curves**: a curve like HA07d train
bidirectional rises with multiple direction-reversals but never
crosses zero in the meaningful range. The v2 locked rule treats
this as NOT Cat 4 (no zero-crossings, no large negative). Direction
reversals are reported descriptively but do not trigger Cat 4. This
is the discipline applying as written: the bumpiness is real but
the curve does not flip direction, so it is not threshold-unstable
in the verdict-direction sense.

The researcher's earlier intuition that "4 direction-reversals
means non-robust" is overridden by the explicit locked definition
of sign-changes as zero-crossings. Per the discipline, the explicit
definition wins.

### Category 5 — Loose-tail noise (FAIL)

**Definition**: Discrimination peaks at the loosest end of the
meaningful range and drops sharply at slightly stricter thresholds.
The "signal is artefact of a specific permissive cutoff" shape.

**Locked criteria** (all required to trigger FAIL, definitions
per §3.0):
- Peak N_std ≤ 1.0 (peak at the loose edge of meaningful range).
- Discrimination at N_std = peak + 1.0 (the tier 1.0 N_std-unit
  above the peak) drops to ≤ 25% of peak value.
- Discrimination at N_std = 2.0 ≤ +5 pp.

**Interpretation**: the v1 criteria were correctly targeting this
shape category. v2 retains the detection logic with sharper
quantitative thresholds.

**Note**: Cat 5 is the most restrictive FAIL category. A curve
that peaks at N_std=1.25 with a smooth decline would NOT trigger
Cat 5 (peak > 1.0); it would be Cat 1 if it meets the canonical
decline criteria. The peer-review boundary concern between Cat 1
and Cat 5 is resolved by the strict "peak ≤ 1.0" trigger for
Cat 5.

## 4. Verdict logic

All five categories are evaluated against each test's primary
discrimination curve per era. The categories are independent
checks; their ordering in §3 is for presentation only and does NOT
affect the verdict computation.

Compute for each curve:

1. Cat 1 PASS or fail.
2. Cat 2 PASS or fail.
3. Cat 3 PASS or fail.
4. Cat 4 FAIL or no-trigger.
5. Cat 5 FAIL or no-trigger.

Then apply the verdict rules in this strict order (these ARE
ordered; the first matching rule produces the verdict):

- **Rule (i)**: If ANY of Cat 4 or Cat 5 triggers AND ANY of Cat
  1, Cat 2, Cat 3 passes → **CLOSE wins** (PASS + FAIL = CLOSE).
- **Rule (ii)**: If ANY of Cat 1, Cat 2, Cat 3 passes AND neither
  Cat 4 nor Cat 5 triggers → **RESCUE**.
- **Rule (iii)**: If ANY of Cat 4 or Cat 5 triggers AND none of
  Cat 1, Cat 2, Cat 3 passes → **CLOSE**.
- **Rule (iv)**: If no category matches → **AMBIGUOUS**. Defaults
  to CLOSE for synthesis-framing purposes; flagged in result.md
  for case-by-case methodological review.

The asymmetry is the right asymmetry: a curve that *both* passes
a robust-shape category *and* triggers a fragile-shape category is
classified as CLOSE, because the fragility signal is dispositive.

For reporting, the result.md must list ALL category matches and
no-triggers (not just the verdict-determining one). This makes the
verdict's basis transparent and reviewable.

## 5. Application rules

### Symmetric application

The v2 criteria are applied to ALL of HA10, HA07d, HA06b, HA11 at
their pre-registered bidirectional primary arms. The criteria do
NOT consider one-sided arms in v2; one-sided arms are recorded as
descriptive context in result.md files.

### Locked verdicts unchanged

The original locked SUPPORTED verdicts in each test's result.md
stay on record per pre-registration discipline. The v2 diagnostic
only informs synthesis-level load-bearing status.

### Single attempt per test

Each test gets exactly one v2 diagnostic application. No
re-diagnostics with re-tuned criteria.

**v3 escape hatch — strictly bounded**: a v3 methodology document
may only be locked if **all three** conditions are met:

1. **External authority**: v3 must respond to a methodological
   principle independently articulated by an external authority
   — a published peer-reviewed signal-detection-theory paper, a
   peer-reviewed PEM/HRV methodology source, or an equivalent
   academic source. v3 may NOT be locked because v2 verdicts are
   intuitively unsatisfying to the project's researchers.

2. **Pre-locked statement of inadequacy**: before v3 is drafted,
   a written statement must be locked describing which v2
   category (1-5) fails to capture which kind of robust signal,
   citing the external source. This statement is itself
   pre-registered and dated; v3 design follows from the
   pre-locked inadequacy statement, not vice versa.

3. **Symmetric re-application**: v3 criteria, if locked, apply
   symmetrically to ALL tests in the same family that v2 covered
   — including v2 RESCUE findings. A test that RESCUES under v2
   could CLOSE under v3 if the v3 criteria are stricter. The
   discipline must bind in both directions.

This is strict by design. The current discipline binds because
no v3 has been invoked; once invoked, the boundary is defined by
precedent. The three conditions above are the precedent.

### Result.md outputs

Each v2 diagnostic.md will produce a result.md with:
- The shape category match for bidirectional primary per era.
- RESCUE / CLOSE / AMBIGUOUS verdict per era.
- Locked verdict status statement (unchanged from original test).
- Synthesis-level framing implication per era.
- Direct comparison with v1 diagnostic outcome (where v1 was run).

### Synthesis update protocol

Synthesis-level docs are updated **only after all four v2
diagnostics are complete**, in one consolidated update. This
prevents partial updates that read selectively (e.g. updating
synthesis with HA07d RESCUE while HA06b v2 is still pending).

## 6. What this methodology does NOT do

- **Does not unlock any test's pre-registered SUPPORTED verdict.**
  Audit trail intact.
- **Does not pretend the v1 verdicts were wrong.** v1 verdicts
  stand on record; the discipline cost has been paid; v2 is a
  separate methodology epoch.
- **Does not promise restoration** of any specific finding. v2
  outcomes determine outcomes; we do not pre-commit to a
  particular set of restorations.
- **Does not replace specificity / posterior-probability analysis
  for cards.** A v2 RESCUE on a test is necessary but not
  sufficient to ship a card built on that test; specificity
  tables (per Tier 2 peer-review action items) remain a separate
  gate.

## 7. Acknowledgement of the timing concern

It is not lost on the methodology architects that v2 is being
locked **in the same session** as the v1 verdict that motivated
its locking. The user-locked Option C explicitly accepts this
risk because the alternative (deferring criteria revision to
"this week" or "next week") creates the worse risk of the
criteria being revised quietly later, when motivated-reasoning
pressure has had time to compound.

The discipline binding here is: **the v1 demotions remain in
effect from the moment they were applied until the v2 diagnostics
complete and synthesis is updated atomically**. The interim doc
state honestly shows the demotion. The v2 criteria are locked
publicly with their five-category logic exposed. Any selective
application by future agents or researchers will be visible as
a deviation from this document.

## 8. Companion documents

- v1 diagnostics (run, CLOSE):
  - [HA10 v1 result.md](../hypotheses/HA10-threshold-monotonicity-diagnostic/result.md)
  - [HA07d v1 result.md](../hypotheses/HA07d-threshold-monotonicity-diagnostic/result.md)
- v2 diagnostics (pre-registered, pending run):
  - [HA10 v2 diagnostic.md](../hypotheses/HA10-threshold-monotonicity-diagnostic-v2/diagnostic.md)
  - [HA07d v2 diagnostic.md](../hypotheses/HA07d-threshold-monotonicity-diagnostic-v2/diagnostic.md)
  - [HA06b v2 diagnostic.md](../hypotheses/HA06b-threshold-monotonicity-diagnostic-v2/diagnostic.md)
  - [HA11 v2 diagnostic.md](../hypotheses/HA11-threshold-monotonicity-diagnostic-v2/diagnostic.md)

---

*Locked 2026-06-07 as a separate methodology document. The v2
criteria are explicitly locked with their five-category shape
rule and verdict logic; pre-registered diagnostic.md files in each
test's folder reference this document as their criteria source.
The discipline binds.*
