# Methodology review -- post_crash_exertion_relapse (danger-window test)

**Target**: [`../methodology/post_crash_exertion_relapse.md`](../methodology/post_crash_exertion_relapse.md)
(status DESIGN, PROPOSED, 2026-07-03) and its descriptive precondition
[`../analyses/descriptive/post_crash_exertion_relapse/precondition.md`](../analyses/descriptive/post_crash_exertion_relapse/precondition.md).

**Review type**: fresh-session `/research-methodology-review`, pre-registration
gating. Audited against [CONVENTIONS §2.2](../CONVENTIONS.md) four-input bar,
§3.2 (lagged-lcera), §3.5 (no-outcome-peek), §3.6 (named counts), §4.1/§4.3
(descriptive-before-inference, prior-driven = confirmatory), the cited PEM
literature (`push crash research.md`, `pacing-and-crash-mitigation.md`), the
inherited HA01c operand, and `permutation_null_block_length.md`.

**Reviewer mode**: fresh session, no exposure to the drafting context;
doc-only knowledge.

---

## Overall verdict: ACCEPT-WITH-MINOR-REVISIONS

The design is sound in its spine: the mechanism is prior-given, the peak-primary
framing is correctly literature-anchored, the degenerate-binary reasoning is
honest and load-bearing, and the no-outcome-peek boundary holds. It is *not*
ready to lock as written, because three guards that the design itself names as
the decisive ones (the RTM/base-rate reference, the reverse-causation ordering
rule, and the crash-vs-dip comparison's fairness) are still specified at the
level of intention rather than construction. None is a rigor breach; each is an
under-specification the pre-registration must close before it locks, and the MD
already flags all three as open inputs. Hence minor revisions, not
revise-and-resubmit. One honesty item (power) is a required addition to the MD
body, not merely the falsification section.

## NO-OUTCOME-PEEK: HELD

The precondition characterises only event location (29 crashes / 79 dips),
the exposure (predictor) distribution, coverage/missingness, and the comparison
design space. It computes no relapse count, marginal or conditional, and no
exposure-versus-relapse relationship. The binding statement is explicit and
accurate, and every number in §3 is traceable to a coverage count or a
predictor distribution. See finding 1 for the one residual seam.

## Counts

- **BLOCKING**: 0
- **MAJOR**: 3 (findings 4, 6, 8)
- **MINOR**: 5 (findings 1, 3, 5, 7, 9)
- **NIT**: 1 (finding 2)

---

## Findings (keyed to the 9 stress-tests)

### 1. No-outcome-peek held in the precondition -- MINOR

**Held.** The precondition's binding box is correct: it inspects events,
exposure distribution, coverage, and the comparison-window set, never the
outcome. The load-bearing §3.1 finding ("binary flags 86%") is a property of
the *exposure* distribution (share of windows with >=1 day >=0.75), not of any
relapse relationship, so it does not breach the boundary. This is the right
call and worth stating: a degeneracy-of-exposure finding is a legitimate
pre-outcome result; a degeneracy-of-*discrimination* finding would not be.

One residual seam, MINOR. The precondition reports "count of days >= 0.75 spread
0-6 (median ~3)" and the peak-distribution quantiles. These are exposure-only,
but the *cumulative* secondary exposure (count of shock-days) is now
characterised in full while the primary (peak) is also characterised in full.
That is fine for locking, but note for the pre-reg: once both exposure
constructions are this well-mapped pre-outcome, the temptation at analysis time
to report "whichever of peak/cumulative separates better" is a garden-of-forking
-paths risk. The MD already names peak primary and cumulative secondary
(decision d), so the fix is cheap: **the pre-reg must state that the primary
verdict is read off peak, and cumulative is reported as a mechanism-adjudication
contrast regardless of which is larger** -- not promoted to primary if it wins.
Make the primacy irrevocable in the pre-reg, not just asserted in the MD.

### 2. Threshold-crossing (peak) primary vs dose-accumulation prior-given -- NIT

**Correct and confirmatory, not fished.** The literature check passes cleanly.
`push crash research.md` is unambiguous: the single-bout 2-day-CPET
threshold-suppression paradigm is the *evidenced* mechanism (Workwell/Keller/
Lien/Thomas), and the dose-accumulation "total load" model "appears only in
clinical-consensus and patient-guidance language" plus the untested
Wirth/Scheibenbogen sodium hypothesis -- "no study formally operationalizes or
tests these as competing mechanisms." So peak-primary (evidenced) and
cumulative-secondary (novel, competing) is exactly the correct reading of the
cited source, and the direction is prior-given (§4.3 questions 1-3 all yes:
lived pacing experience, published single-bout support, mechanistic
symptom-fast/autonomic-slow argument). This is confirmatory framing, properly
earned. It is not a post-hoc salvage: peak was the evidenced mechanism *before*
the binary degenerated, so choosing it is not motivated by the degeneracy.

The only reason this is a NIT and not a clean pass: decision (d) is doing a lot
of work in one paragraph. The claim "no study has pitted the two against each
other, so cumulative is a genuinely novel competing arm" is a strength worth
foregrounding as such -- this test's *cumulative arm is the more original
contribution* even though peak is primary. Consider a one-line note that a
cumulative-wins result would be a genuinely new (though n=1, un-generalisable)
data point on a question the literature explicitly flags as open. No change
required.

### 3. The degenerate-binary finding motivating the continuous peak -- MINOR

**Reasoning sound; the move restores contrast honestly; watch the new degrees
of freedom.** The §3.1 logic is correct and, importantly, correct in the
*right direction*: ">=1 day above your own 75th percentile in a ~week window"
is near-guaranteed by construction (86% exposed, 4 unexposed = no contrast
group), so a binary split is structurally dead. Moving to the continuous
0.60-1.00 peak gradient (median 0.93) genuinely restores contrast, and it does
so without an arbitrary cutoff, which also sidesteps HA01c's
threshold-monotonicity trap. Good. The inversion of the pacing confound
(exposure is near-ubiquitous, so the problem is contrast not rarity) is an
honest and useful reframing.

The MINOR concern is the new degrees of freedom that a continuous dose-response
introduces, which the MD does not fully enumerate. A continuous peak still
carries choices that could be tuned to the unseen outcome: (i) the functional
form of the dose-response (linear in rank? logistic? a spline?), (ii) whether
peak is on the rank scale or a transform, (iii) whether "peak" is the max single
day or a top-k average. The degenerate-binary problem was *cutoff* freedom;
the continuous move trades it for *functional-form* freedom, which is not
obviously smaller. **Fix**: the pre-reg must lock the dose-response link
function and the exact peak definition (max single-day rank, per the
precondition's "peak single-day" wording) before outcome inspection, and state
that no alternative link will be substituted post-hoc. As written the MD says
"continuous dose-response" without pinning the form.

### 4. The null and the two hardest confounds -- MAJOR

This is the finding that most holds the design back from ACCEPT. All three
sub-parts are named correctly by the MD but under-constructed.

**(a) RTM / base-rate reference -- still hand-wavy.** The MD (decision f,
confound 2) mandates "the null must be the RTM/base-rate reference, not a naive
comparison" and the precondition open-input #2 asks whether it is "matched
non-event windows vs within-window" -- which concedes the construction is not
yet chosen. This is the single most consequential un-locked knob in the design,
because the entire hypothesis is "*more* likely than at baseline," and
"baseline" is precisely this reference. Two constructions give materially
different tests: (i) a within-danger-window dose-response (does higher peak ->
higher relapse *within* the exposed windows), which does not by itself answer
"more than baseline," versus (ii) a matched-comparison against
peak-exertion-of-equal-magnitude days *outside* any danger window (the actual
"same spike at baseline" counterfactual the hypothesis states). The hypothesis
sentence in §1 -- "than the same spike at baseline" -- demands construction
(ii) or a hybrid; construction (i) alone silently changes the claim. **Fix**:
the pre-reg must specify the base-rate reference as an explicit
matched-non-danger-window comparison set (equal-magnitude peak days outside any
post-crash danger window), state the matching variables (at minimum: peak-rank
band, and ideally LC-era/deconditioning epoch given the shrinking envelope), and
define RTM handling (relapse is common after any low day, so the reference must
condition on a comparable felt-state trajectory, not just a comparable peak).
Until this is a construction and not an adjective, the test is not locked.

**(b) Reverse causation -- the guard is necessary but not yet sufficient.** The
"peak strictly precedes relapse + exclude days already inside a descending
felt-state" guard is the right instinct and covers the crude case (a relapse
day counted as its own exposure). It does not fully close the subtler channel:
a *prodromal* relapse can suppress exertion *before* the felt-state visibly
descends, so a day that is still felt-flat but autonomically pre-crashing would
be (correctly) low-exertion and (incorrectly) counted as an un-exposed
danger-window day, deflating the exposed group's apparent innocence and inflating
the contrast. The guard keys on *felt-state* descent; the hypothesis's own
premise is that felt-state lags the autonomic state -- so a felt-based
exclusion is, by the design's own logic, the wrong sensor for detecting a
brewing relapse. **Fix**: state this residual explicitly as a limitation the
design cannot fully remove (the felt-recovered gate is the only available
ordering sensor, and it is known to lag), and add a sensitivity that also
excludes days whose *autonomic* channel (overnight stress / RHR, the R9
signature) is already trending adverse, if that column is available for the
danger-window days. If it is not available, say so and treat the residual as a
named directional bias on the CI.

**(c) Block-permutation E[L]~7 -- right family, wrong default without a check.**
The stationary bootstrap at E[L]=7 is the correct autocorrelation-respecting
choice per `permutation_null_block_length.md`, and citing it is right. But that
MD's own override rule (its "Per-hypothesis override allowed only when" clause)
requires an ACF readout of *this* metric before adopting the E[L]=7 default, and
mandates a data-driven E[L]* companion with a factor-of-2 flag. The peak
exertion in a ~10-day danger window is not a generic daily physiological signal;
it is an event-conditional extremum, and its effective block structure at the
*event* level (28 crash windows) is what governs the null, not the day-level
ACF of the raw exertion series. **Fix**: the pre-reg must (i) report the
day-level ACF readout for `eff_exertion_rank_lagged_lcera` to justify E[L]=7 or
trigger the override, and (ii) clarify that the permutation is over
*event-level* units (block-permute the crash/non-crash window labels), given
that with 28 events the relevant n is 28, not ~1700 days -- exactly the tension
`permutation_null_block_length.md` §4 flags ("tight for permutation null tests
at the crash-event level, where the relevant n is 29"). This is a MAJOR because
an event-level test with 28 units and heavy autocorrelation is where the null
construction most easily goes wrong.

### 5. The lagged-lcera baseline -- MINOR

**Right frame; the self-cleaning claim is arithmetically correct for the index
crash but overstated for neighbouring crashes.** The lagged-lcera choice is
correct and well-justified: the exertion envelope demonstrably shrank across the
LC era (the ~15 kg / VO2Max 52->37 deconditioning finding), so "a spike relative
to *current* capacity" is the only frame that does not mis-scale, and a naive
trailing baseline would rebase into the ramp (CONVENTIONS §3.2). Agreed.

The self-cleaning claim checks out for the *index* crash. Window arithmetic:
a danger-window day sits at nadir+k for k in roughly 1..10 (felt-recovery day
through nadir+10). Its baseline is [d-90, d-30] = [nadir+k-90, nadir+k-30]. The
upper edge nadir+k-30 is at most nadir-20 for k<=10 -- i.e. the baseline window
closes at least 20 days *before* the index nadir. So the index crash cannot
contaminate the baseline. Correct.

But "self-cleaning against crash contamination" is stated without the
neighbouring-crash caveat, and the corpus makes that caveat load-bearing in one
era. Crash frequency was ~10/year in 2023-24 (CONVENTIONS §3.7; RESEARCH-REPORT
et al.), i.e. crashes as little as ~30-40 days apart. A 60-day-wide baseline
window ending 20+ days before the index nadir can therefore straddle the
*previous* crash episode in the dense era, pulling the baseline down toward
crash-suppressed exertion and mechanically *inflating* the index day's rank
(a spike looks bigger against a crash-deflated reference). **Fix**: state that
the [d-90,d-30] window self-cleans against the *index* crash but may include
neighbouring crash/dip days in the dense (2023-24) era, and either (i) mask
crash/dip days out of the baseline computation, or (ii) report a sensitivity
that does so, or (iii) if the `_lcera` column already excludes crash days from
its baseline, say so explicitly and cite where. The MD currently asserts a
stronger cleanliness than the arithmetic supports.

### 6. The crash-vs-dip mechanism control -- MAJOR

**A valid falsification lever in principle, but the comparison as specified is
not fair, and the unfairness runs in the direction that could manufacture the
"autonomic-specific" result.** The logic is genuinely good: crashes carry the
R9/HA-P6 autonomic signature (4/7 channels distinguishable), dips do not (flat
overnight stress), so "premature exertion raises relapse after crashes but not
after dips" would be strong evidence the effect is autonomic-window-specific
rather than "any low day" (decision a, precondition §1). This is the design's
best idea.

The fairness problem is threefold and the MD does not address it. (i) **Base
rate**: crashes (29) and dips (79) have different relapse base rates by
construction -- a dip is a milder event, so the post-dip relapse rate is a
different baseline, and "weaker effect after dips" could simply be a
floor/ceiling artefact of the different base rate, not autonomic specificity.
(ii) **Power asymmetry**: 79 dip windows have ~2.7x the power of 28 crash
windows, so "effect present for crashes, absent for dips" could be the *opposite*
of what a power-blind reader assumes -- the better-powered dip arm failing to
show an effect while the underpowered crash arm shows one is exactly what noise
plus a small true effect can produce, and it would be over-read as specificity.
(iii) **Exposure distribution**: the precondition characterises the crash-window
peak distribution (median 0.93) but not the dip-window peak distribution, so it
is unknown whether the two arms even span comparable exposure ranges; if dips
have systematically lower peaks (milder events, less subsequent activity), the
dose-response is being compared over different supports. **Fix**: the pre-reg
must (a) define the crash-vs-dip contrast as a formal interaction (does the
peak-relapse slope *differ* between crashes and dips), not two separate
verdicts eyeballed side by side; (b) match or condition on the base-rate
difference so "weaker after dips" is a slope difference, not a level
difference; (c) add the dip-window peak-exposure distribution to the
precondition (it is a predictor, so this does not breach no-peek) to confirm
comparable support; and (d) state the power asymmetry explicitly so a null-on-
crashes / effect-on-dips or effect-on-crashes / null-on-dips is not
mis-read as specificity when it is a power difference.

### 7. Physical-only scope + the null-asymmetry -- MINOR

**A legitimate scope statement, but currently written in a way that makes the
hypothesis harder to falsify than it should be, and the null-reading needs a
sharper rule.** The scope is defensible and literature-grounded: "all exertion
counts -- cognitive overexertion can crash someone as hard as a walk, and a
step-counter misses it entirely" (`pacing-and-crash-mitigation.md` §1), and the
mental/emotional/orthostatic channels are genuinely sparse (parked R4). So
scoping to the physically-visible subset is honest, and stating that a relapse
with no physical spike is "expected noise (a possible mental-PEM trigger), not
counter-evidence" is a correct *asymmetry* -- a physical-only exposure cannot be
blamed for a relapse it never saw.

The risk, MINOR: as phrased, "a relapse with no physical spike is expected
noise, not evidence against the hypothesis" can absorb *any* null. If every
non-confirming relapse is reclassified as an unobserved-mental-PEM case, the
hypothesis becomes unfalsifiable on the downside. The get-out-of-jail reading is
avoided only if the null is read on the *right* estimand. **Fix**: state
precisely what a null does and does not license. The hypothesis is falsifiable
on its actual claim -- *among physical spikes, danger-window peaks relapse more
than matched baseline peaks*. A null on **that** contrast (physical spikes in
the danger window are *not* more relapse-prone than matched physical spikes at
baseline) IS counter-evidence and must be reported as "the physically-visible
danger-window effect is not established," which §5 already says. The mental-PEM
escape applies only to relapses with *no physical exposure at all* (they are
outside the test's support), not to physical spikes that failed to relapse.
Make that two-case split explicit: no-exposure relapses are out of support
(neutral); in-danger-window physical spikes that do not relapse above baseline
ARE disconfirming. Without that sentence, decision (g)'s asymmetry reads as
immunity.

### 8. Power / n -- MAJOR

**"Cannot resolve" is the honest modal outcome, and the MD says so in the
falsification section but does not carry it into the design body where it
belongs.** With 28 usable crash windows, a continuous dose-response, n=1, heavy
autocorrelation, and an event-level null where the relevant n is 28, the design
is underpowered to detect anything but a large effect. The MD is commendably
honest in §5 ("an honest 'cannot resolve' is a valid, publishable outcome") and
confound 5 ("CIs are wide (29 crashes)"). But this is currently framed as a
*post-hoc consolation* rather than a *pre-registered expectation*. A
pre-registration that does not state its own detectable-effect floor invites the
post-hoc reading of a wide CI as "suggestive." **Fix (required, MAJOR)**: add to
the MD body (not just §5) a power/precision statement: at 28 event-level units
with E[L]~7 autocorrelation, name the smallest dose-response slope the design
could distinguish from the RTM null at the chosen bootstrap CI, or -- if that
is not computable pre-outcome without peeking -- state that the primary
deliverable is an *estimate with an honest CI*, not a reject/accept verdict, and
that "cannot resolve" is the pre-committed default reading of a CI that spans the
null. Also flag the multiplicity context: peak-primary + cumulative-secondary +
crash-arm + dip-arm + a 3/4/5-day sensitivity band + a 3-window danger-length
sensitivity is a non-trivial number of looks; the pre-reg must name the primary
single test whose CI is the verdict, with the rest explicitly
labelled secondary/sensitivity, so the effective-N multiplicity
(`permutation_null_block_length.md` §4, effective independent channels ~3-4)
is not silently spent. This is MAJOR because unstated multiplicity plus wide
CIs is the exact configuration where an n=1 "cannot resolve" gets quietly
upgraded to "consistent with."

### 9. Four-input completeness -- MINOR

**Each decision (a)-(g) carries an L/D/M/P tag, and most are genuine. Three are
thinner than the four-input bar wants.** The template is applied conscientiously
and decision (d) in particular is a model four-input paragraph (literature does
real work, dataset degeneracy is cited, the methodology tradeoff is explicit,
project inheritance from HA01c is named). Findings:

- **Decision (c) danger-window length ([D] is absent).** (c) carries [L], [M],
  [P] but no [D] -- there is no dataset/coverage input for why 10 days and not
  7 or 14, even though the precondition *has* the coverage numbers (236 crash
  danger-window days over 28 windows) that would support a [D] line. The
  four-input bar wants all four where they exist; the [D] here is available and
  omitted. MINOR fix: add the coverage/dilution [D] tradeoff.
- **Decision (e) relapse window ([D] and [M] thin).** (e) leans on [L]
  (delayed-onset 12-72h) and asserts a "3/4/5-day sensitivity band" but the [M]
  is one sentence and there is no [D] on how many events even *have* a
  computable outcome at 3 vs 4 vs 5 days -- which is a coverage question the
  precondition could answer without peeking the outcome *values* (coverage !=
  outcome). MINOR fix: add the outcome-*coverage* (not outcome-value) count per
  window length.
- **Decision (f) null ([L] deferred, correctly, but flagged here for
  visibility).** (f)'s literature input honestly inherits
  `permutation_null_block_length.md`, whose own [L] row is "deferred" (the
  stationary-bootstrap canon is unread in the literature folder). This is not a
  fault of *this* MD -- it correctly cites the null MD -- but the pre-reg should
  note that the null's literature anchor is itself pending, so the E[L]=7 choice
  rests on first-principles reasoning plus the data-driven companion, not on a
  verified citation. Transparency item, MINOR.

The [P] "single-pool primacy" line in (f) ("any over-time difference is a
number with wide error, never an era verdict") is exactly the right posture and
should be preserved verbatim into the pre-reg.

---

## Summary of required changes before the pre-registration locks

The verdict is ACCEPT-WITH-MINOR-REVISIONS; the "minor" reflects that none of
these touches the design's spine, but findings 4, 6, and 8 must be closed as
*constructions* (not intentions) in the pre-registration:

1. **(finding 4a, MAJOR)** Build the RTM/base-rate reference as an explicit
   matched-non-danger-window comparison set with named matching variables; the
   hypothesis's "than the same spike at baseline" demands the counterfactual be
   constructed, not adjectival.
2. **(finding 4c + 8, MAJOR)** Specify the null as an event-level (28-unit)
   block-permutation with a reported ACF readout justifying E[L]=7 and a
   data-driven E[L]* companion; carry a power/precision + multiplicity statement
   into the MD body naming the single primary test.
3. **(finding 6, MAJOR)** Reframe crash-vs-dip as a formal slope *interaction*
   with base-rate conditioning, add the dip-window peak-exposure distribution to
   the precondition, and state the power asymmetry so specificity is not
   confounded with power.
4. **(findings 3, 5, 7, minor but do before lock)** Lock the dose-response link
   function and peak definition; qualify the "self-cleaning" claim for
   neighbouring crashes in the dense era (and mask/sensitivity); add the
   two-case null-reading rule so physical-only scope is not immunity.
5. **(finding 9, minor)** Fill the missing [D] on decisions (c) and (e); note
   the null MD's deferred literature anchor.

The single most important fix: **construct the RTM/base-rate reference as an
explicit matched non-danger-window comparison (equal-magnitude peak days outside
any post-crash window, matched on exposure band and deconditioning epoch)** --
without it, "more likely than at baseline" has no baseline, and the primary
verdict is undefined regardless of how clean everything else is.

---

## Authorship

Claude (Opus 4.8) fresh-session methodology reviewer, for the
participant-researcher (repo owner).
