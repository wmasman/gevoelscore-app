# Fresh-session peer review -- post-crash-exertion-relapse pre-registration

**Target**: [`../analyses/hypotheses/post-crash-exertion-relapse/hypothesis.md`](../analyses/hypotheses/post-crash-exertion-relapse/hypothesis.md)
(pre-registration, LOCKED 2026-07-04, reviewer-mode-with-authorization draft),
with its authoritative sources read cold: the locked methodology MD
[`../methodology/post_crash_exertion_relapse.md`](../methodology/post_crash_exertion_relapse.md)
(DESIGN PROPOSED r3), the descriptive precondition
[`../analyses/descriptive/post_crash_exertion_relapse/precondition.md`](../analyses/descriptive/post_crash_exertion_relapse/precondition.md),
the prior methodology review
[`methodology-post_crash_exertion_relapse-2026-07-03.md`](methodology-post_crash_exertion_relapse-2026-07-03.md),
the inherited operand
[`../analyses/hypotheses/HA01c-effective-exertion-shock/hypothesis.md`](../analyses/hypotheses/HA01c-effective-exertion-shock/hypothesis.md),
the cited literature (`push crash research.md`, `pacing-and-crash-mitigation.md`),
the null policy [`../methodology/permutation_null_block_length.md`](../methodology/permutation_null_block_length.md),
and CONVENTIONS Sections 1.2 / 3.2 / 3.5 / 3.6 / 4.3.

**Review type**: fresh-session `/research-review`, pre-registration gating (binding
lock before any outcome is inspected).

**Reviewer mode**: fresh session -- no exposure to the drafting context; doc-only
knowledge. Per the prompt's discipline instruction, the drafting handoff MD
(`_push_crash_pipeline_handoff.md`) was NOT read, to preserve cold independence.

---

## Overall verdict: ACCEPT-WITH-MINOR-REVISIONS

The pre-reg is a faithful, disciplined implementation of the locked r3 methodology.
The spine is sound: the no-outcome-peek boundary holds cleanly; the r3 cardiac-strain
swap is physiologically correct and confirmatory; the constructed matched-baseline
reference (the load-bearing fix) is built as a construction rather than an adjective;
the event-level 28-unit null is honestly specified; the crash-vs-dip contrast is a
formal slope interaction with base-rate conditioning and the stated 2.7x power
asymmetry; the two-case null-reading and physical-only scope are stated so scope is
not immunity; single-primary-test multiplicity control and peak-primacy irrevocability
are locked; and there is no PII, no em-dash, and the GSS guardrail is present.

It is *not* an outright ACCEPT because four small but real degrees-of-freedom remain
open at lock, three of them the drafting agent flagged itself. None touches the design
spine or breaches no-peek. But a binding pre-registration should carry zero
post-lock analyst discretion on mechanics that could be tuned to the unseen outcome,
and two of the self-flags (c: the `_lcera` masking branch; d: the per-replicate
null mechanic) are exactly such discretion left un-resolved. These are MINOR because
each has an obvious no-peek-safe resolution that does not change the claim, the
exposure, the window, or the test; they should be closed before the test script is
written. Because a pre-reg lock is binding, I recommend the revisions be folded in
and the lock re-dated, rather than treated as analysis-time latitude.

## NO-OUTCOME-PEEK: HELD

## r3 EXPOSURE RE-CONFIRMED: YES

## Counts

- **BLOCKING**: 0
- **MAJOR**: 0
- **MINOR**: 6 (findings 1-seam, 6b, 6c, 6d, and the two link/masking mechanics)
- **NIT**: 2

---

## Findings (keyed to the review checklist)

### 1. NO-OUTCOME-PEEK held -- PASS (one residual seam, NIT)

**Held.** This is the single most important check and it passes. Every number the
pre-reg fixes is a predictor-only coverage count or an exposure (predictor)
distribution, and the pre-reg's binding box enumerates the permitted class correctly
and the forbidden class explicitly. I independently traced each cited number to a
non-outcome quantity:

- `29 crash episodes / 79 dip days` -- event location (labeling counts), named per
  Section 3.6 with scheme + unit + file. Not an outcome.
- `28 / 29` and `79 / 79` felt-recovery -- row-presence coverage of a
  `gevoelscore >= 4` day in the window. A coverage count, not a relapse count.
- `235 / 236` and `236 / 236` / `790 / 790` -- exposure-column non-null coverage in
  the danger windows. Coverage, not outcome.
- peak `max_hr_rank_lagged_lcera` median 0.95 (p25/p75/min/max) and peak
  `eff_exertion_rank_lagged_lcera` median 0.93 (crash) / 0.92 (dip) -- these are
  **exposure** (predictor) distributions, no relapse involved.
- `rho(max_hr_rank, eff_exertion) = +0.42` (n=235 days) -- a
  predictor-versus-predictor rank correlation. Crucially this is NOT an
  exposure-versus-relapse relationship; it is the confound-test premise (do the two
  exposure axes diverge), which is legitimately pre-outcome.

Nowhere does the pre-reg or the precondition it cites compute or imply a relapse count
(marginal or conditional), a relapse rate, a dose-response slope, or any
exposure-versus-relapse contrast. The precondition's binding box makes the same
promise and the earlier methodology review independently certified it HELD; I concur
on a cold re-read. The one degenerate-binary finding (86% of windows flag on a
`>= 0.75` binary) is a property of the *exposure* distribution (share of windows with
>= 1 high-rank day), not of any relapse relationship, so it does not breach the
boundary. The outcome-window sensitivity is disclosed at the *coverage* (row-presence)
level only, with the outcome values explicitly withheld -- correct.

**NIT (residual seam, inherited from methodology review finding 1).** Both exposure
constructions (peak and cumulative) are now fully mapped pre-outcome. That is a
garden-of-forking-paths temptation at analysis time ("report whichever of
peak/cumulative separates better"). The pre-reg already closes this: Section 8 makes
peak-primacy irrevocable and states cumulative is reported "regardless of which of
peak/cumulative separates better ... does not become the primary verdict." No change
required; noting it discharges the inherited seam.

### 2. r3 exposure re-confirmation (mandated cold re-confirm) -- CONFIRMED (NIT)

The MD Section 7 and the pre-reg authorship block both require this fresh-session
review to independently re-confirm the r3 primary-exposure swap
(activity-volume -> peak cardiac strain `max_hr_rank`). I re-confirm YES on all three
sub-questions, from the literature cold:

**(a) Physiologically faithful threshold-crossing exposure.** `push crash research.md`
is unambiguous that the *evidenced* PEM mechanism is single-bout cardiac threshold
suppression: the 2-day-CPET paradigm (Workwell/Keller/Lien/Thomas), VT1 as "the PEM
threshold," ~24h HRV suppression after a single crossing (the Dutch Ruijgt 2025
wearable finding, "VT1 can be practically interpreted as a PEM threshold").
`pacing-and-crash-mitigation.md` Section 2 independently anchors the HR/VT1 ceiling as
"the most established tool." So the faithful threshold-crossing exposure is peak
cardiac output relative to current capacity, which is exactly what
`max_hr_rank_lagged_lcera` (peak single-day HR rank against the lagged era-local
window) operationalises. Confirmed.

**(b) Correct answer to the step-count / activity-volume confound.** The Founder&City
700k-day finding cited in both the MD (decision d [L]) and the literature framing
("PEM cases needed ~50% more cardiac work for identical walks; measure the cardiac
cost of movement, not volume") is the documented confound. The pre-reg's argument that
it applies within-person -- cardiac cost per unit activity rises as capacity falls, so
an activity-volume exposure under-detects the low-volume cardiac threshold-crossings
that matter most in the low-capacity danger window -- is sound and is exactly the
right direction. Confirmed.

**(c) Prior-given / confirmatory, not fished.** All three CONVENTIONS Section 4.3
questions are yes: lived pacing experience pre-dating the analysis; published
single-bout cardiac support; a mechanistic argument (felt-fast / autonomic-slow
mismatch) independent of any data look. Critically, and as the prior methodology
review (finding 2) already established, peak was the evidenced mechanism *before* the
binary degenerated, so the swap is not motivated by the degeneracy -- it is not a
post-hoc salvage. The pre-reg keeps `eff_exertion` as the *comparison arm* rather than
discarding it, which is the honest move: the strain-vs-volume divergence (rho +0.42)
becomes an in-sample confound test rather than a silent substitution. Confirmed.

**Adjudication: `max_hr_rank` (peak) vs `hr_area` (integral) confound-robustness.**
The pre-reg's claim -- that the peak spike is confound-robust where the integral is
not, because `hr_area_above_daytime_baseline_waking_lcera` sweeps up all-day HR
elevation including the resting autonomic arousal that IS the danger-window state,
conflating exposure with the outcome-adjacent state, whereas a peak-HR spike is
activity-driven -- is correct and important. This is a genuine estimand-contamination
argument, not hand-waving: in the danger window the autonomic channel is elevated *by
the danger-window state itself* (that is the whole premise, R9 / HA-P6), so an
integral of above-baseline HR partly measures the very condition whose effect is being
estimated. The peak (a single-day activity-driven maximum) is the cleaner
threshold-crossing sensor. Keeping `hr_area` as a disclosed *secondary* (Section 4b,
Section 9c) rather than promoting it is the right call. I note the pre-reg is candid
that the integral is not thereby worthless -- it is the dose-accumulation competitor
on a question the literature explicitly leaves open (`push crash research.md`,
threshold-crossing vs dose-accumulation "no study formally operationalizes or tests
these"), so a cumulative-wins result is flagged as a genuinely novel (n=1,
un-generalisable) data point without becoming the primary verdict. This is exactly
right. **NIT only**: Section 3.3 of CONVENTIONS names
`hr_area_above_daytime_baseline_waking_lcera` as the *preferred* magnitude x duration
integral for cumulative-burden hypotheses (the A4 example). The pre-reg's demotion of
it to secondary here is well-justified by the conflation argument and does not conflict
with Section 3.3 (which governs which integral to pick *if* you use an integral, not
whether the integral or the peak is primary), but a one-line note that the demotion is
scope-specific to the danger-window estimand (where the integral conflates) and does
not override Section 3.3's general preference would pre-empt a cross-doc confusion.
Optional.

### 3. The constructed matched-baseline (the load-bearing fix) -- SOUND (MINOR)

This was the methodology review's single most consequential fix (its finding 4a), and
the pre-reg closes it as a construction, not an intention. Section 4d specifies the
reference set as equal-magnitude peak-strain days OUTSIDE any post-crash danger window,
matched on (1) peak-strain-rank band, (2) LC-era / deconditioning epoch, (3) a
comparable felt-state trajectory (RTM control). The primary test is explicitly the
relapse rate of danger-window peaks vs matched-baseline peaks at equal peak-strain
magnitude (Section 4d, Section 6, Section 8). This delivers the actual "same spike at
baseline" counterfactual the hypothesis sentence demands, and it correctly rejects the
weaker within-window-dose-response-alone reading (which would silently change the
claim). The three matching axes are the right ones: rank-band makes it
same-spike-vs-same-spike, LC-era epoch handles the demonstrable envelope shrinkage
(~15 kg / VO2Max 52->37 across the era), and felt-state-trajectory matching handles the
"relapse is common after any low day" RTM problem. Good.

**MINOR (implementability seam).** The matched-baseline is sound in specification but
two mechanics are left for the analyst to settle at test time, and each is a small
forking path:

- **"Comparable felt-state trajectory" is not operationalised.** What makes a
  baseline day's felt-state path "comparable" -- the same nadir depth, the same
  pre-day slope, a caliper on `gevoelscore` over some lookback? This is the RTM
  control, so its definition is load-bearing: a loose match under-controls RTM, a tight
  match starves the reference set. This can and should be pinned pre-outcome (it is a
  predictor-side construction, no-peek-safe) rather than chosen when the reference set
  is being built.
- **Matched-set size / matching ratio is unstated.** With 28 danger-window peaks and
  a self-selected exposure that is near-ubiquitous (Section 3.1), the pool of
  equal-magnitude out-of-window peak days at the top of the rank distribution
  (median 0.95, p75 0.98) may be thin. The pre-reg should state how many matched
  baseline days per danger-window peak are drawn (1:1, k:1, or all-eligible-in-caliper)
  and the caliper width on rank-band, because that choice governs the reference's
  variance and is tunable post-hoc if left open. Reporting the *available pool size*
  per rank band is a predictor-only coverage number and would be a welcome no-peek-safe
  addition to confirm the reference set is even constructible at the high-rank end.

Neither is a rigor breach; both are the kind of "construction not adjective" tightening
the methodology review demanded, applied one level deeper. Residual RTM after matching
is honestly carried as a caveat (Section 9), which is the correct posture given n=1.

### 4. The event-level null -- SOUND (MINOR)

The 28-unit block-permutation is correctly specified. Section 6 states the null is
EVENT-LEVEL (n = 28 events, not ~1700 days), block-permutes the event-level
danger-window-vs-matched-baseline labels (not day-level rows), and explicitly declines
to inflate the effective n to the day count. This is faithful to methodology review
finding 4c and to `permutation_null_block_length.md` Section 4's own warning that
crash-event-level tests are "tight ... where the relevant n is 29." The ACF readout +
E[L]=7 default + data-driven E[L]* companion + factor-of-2 override are all carried
(Section 6), matching the null-policy MD's decision (c) and override clause. The
transparency note that the null MD's literature anchor is itself deferred (E[L]=7 rests
on first-principles + the data-driven companion, not a verified citation) is present
and correct -- this is the honest disclosure the methodology review finding 9 asked
for. Effective-n is honestly 28.

**MINOR (this is self-flag (d); see the dedicated adjudication below).** The one gap
is that the *per-replicate mechanic* of the block-permutation is left at the family
level ("the same block-permutation machinery, so one null model serves both the
p-analogue and the CI"), where the sibling peri-event-covid pre-reg spelled its
resampling step out concretely. Adjudicated under the four-self-flags section.

One clarifying observation, no change required: the ACF readout in Section 6 is
computed on `max_hr_rank_lagged_lcera` (the primary), which is the right series --
the earlier methodology review referred to `eff_exertion` because that was the r1/r2
primary; the r3 pre-reg correctly moved the ACF readout to the new primary. Consistent.

### 5. Crash-vs-dip interaction -- SOUND (PASS)

Section 7 implements decision f-iv exactly: a formal slope interaction (does the
peak-strain-relapse slope differ between crashes and dips), not two eyeballed verdicts.
All three fairness components the methodology review (finding 6) demanded are present:
(a) base-rate conditioning so "weaker after dips" must be a slope difference not a
level difference; (b) the 2.7x power asymmetry stated explicitly, with the correct
warning that a better-powered dip-null while the underpowered crash arm shows an effect
is what noise plus a small true effect produces (i.e. specificity must not be inferred
from a power difference); (c) comparable exposure support confirmed from the
predictor-only dip-window peak distribution (median 0.92 vs crash 0.93), which the
precondition Section 3.2 supplied without breaching no-peek. The dip arm is correctly
kept secondary and not promoted to primary. This is a clean pass.

### 6. The four drafting-agent self-flags -- adjudicated by name

**(a) r3 exposure re-confirmation.** Adjudicated in finding 2: **CONFIRMED YES**.
Peak cardiac strain is the physiologically faithful threshold-crossing exposure, the
correct answer to the step-count/activity-volume confound, and prior-given/confirmatory
not fished. No change.

**(b) Autonomic-trend sensitivity conditional on "if the column is available" --
should it be a hard commitment? -- PARTLY. MINOR.** The self-flag asserts the columns
`stress_mean_sleep` / `resting_hr` are ~99% covered, so the Section 4f
autonomic-trend reverse-causation sensitivity should be a hard commitment rather than
conditional. I agree with the *direction* but the ~99% premise does not hold for the
column the sensitivity actually needs, so the fix must be more precise than "just make
it unconditional." The sensitivity needs to detect a danger-window day whose autonomic
channel is *already trending adverse* -- that is a lagged / z-scored trend read, not a
raw daily value. Per DATA_DICTIONARY.md the relevant trend variants are
`stress_mean_sleep_lagged_lcera_z` at ~82.4% fill (within `has_garmin_sleep=True`),
`resting_hr_lagged_lcera_z` at ~78.0% fill, and `respiration_avg_sleep` at ~23%. The
raw source channels may be higher, but the trend variant needed for "trending adverse"
is materially below 99%, and coverage *conditional on danger-window days* is not yet
reported. **Fix (MINOR)**: convert the conditional to a definite commitment, but do so
by (i) naming the exact column the sensitivity uses (recommend
`stress_mean_sleep_lagged_lcera_z` and/or `resting_hr_lagged_lcera_z`, the R9-signature
channels), (ii) reporting its danger-window-conditional non-null coverage (a
predictor-only, no-peek-safe number), and (iii) committing to run the sensitivity on
the covered subset with the uncovered subset disclosed. A blanket "hard commitment on
~99% coverage" would misstate the coverage; a named-column commitment with its real
coverage is both honest and unconditional. The residual felt-lag directional bias on
the CI (Section 4f, Section 9d) is correctly retained regardless -- the autonomic
sensitivity mitigates but does not remove it.

**(c) `_lcera` baseline crash-masking left as "mask, or say-so-if-already-excluded" --
should it resolve to a single definite branch? -- YES. MINOR.** This is a genuine
open degree of freedom in a binding pre-reg and should be closed before lock.
Section 4e currently reads: crash/dip days are masked out of the baseline; if the
`_lcera` column already excludes them, the test states so and cites where, otherwise
masking is applied. That is two branches whose selection depends on a fact about the
column that is knowable *now*, pre-outcome, from
`pipeline/03_consolidate/build_unified_dataset.py` and the lagged-baseline extractor
(`11_compute_lagged_baseline.py`). Leaving it as a runtime "whichever turns out to be
the case" is exactly the analyst discretion a lock should eliminate. **Fix (MINOR)**:
resolve the branch now by reading the extractor -- confirm whether `_lagged_lcera`
already drops `is_crash`/`is_dip` days from its `[d-90, d-30]` reference. If it does,
state "already excluded, see <file:line>, no additional masking; un-masked sensitivity
is the as-built column." If it does not, state "masking applied in test.py; un-masked
sensitivity reported." Either way the pre-reg lands on one definite primary branch plus
one named sensitivity, with zero post-lock discretion. This is a fact-check, not a
design choice, so closing it does not create a v2. (Note: this is a pre-outcome
structural fact, fully no-peek-safe to resolve.)

**(d) Dose-response link-function per-replicate resampling left at the family level --
should it be tightened to zero post-lock degrees of freedom? -- YES. MINOR.** The
sibling reviewer-mode pre-reg (`peri-event-covid/hypothesis.md` Section 5, closing its
own review's MINOR-1) spelled its null out per-replicate: "each bootstrap replicate
resamples the daily factor-z series under E[L]=7 stationary blocks to a synthetic
217-day series, then computes ONE 14-day-window-mean factor-z from that synthetic
series; repeating (>= 10,000 replicates) builds the reference distribution," and its
`test.py` implemented exactly that. The post-crash pre-reg leaves the analogue at the
family level (Section 6: "the same block-permutation machinery, so one null model
serves both the p-analogue and the CI") without stating, per replicate: how the
event-level danger-window-vs-matched-baseline labels are block-permuted (block over
what ordering, at what E[L]), what single statistic is recomputed per permutation (the
standardised danger-window-vs-baseline difference and/or the rank-slope), and the
replicate count. The link function *form* is well locked in Section 4c (relapse-rate
monotone in peak rank, reported as a rank-slope / rank-correlation with CI, no
post-hoc functional-form substitution) -- that half is airtight and closes the
methodology review's finding 3 cleanly. What is missing is the *resampling mechanic*
that produces the CI and p-analogue for that locked statistic. **Fix (MINOR)**: add a
per-replicate paragraph mirroring the peri-event-covid precedent -- state that each
permutation block-permutes the 28 event-level labels (danger-window vs matched-baseline)
at E[L]=7 (or the E[L]* the ACF readout justifies), recomputes the one primary
statistic, and that >= N replicates (name N) build the reference distribution from which
both the p-analogue and the CI are read. This drives post-lock degrees of freedom to
zero on the null mechanic, matching the project's own established precedent one pre-reg
earlier.

**(bonus, self-flag family) the matched-baseline operationalisation (finding 3
MINOR)** overlaps self-flag territory: "comparable felt-state trajectory" and the
matching ratio are the same class of pre-outcome mechanic that (c) and (d) are.
Recommend closing all three in the same revision pass.

### 7. Two-case null-reading + physical-only scope -- SOUND (PASS)

Section 9a states the two-case rule so scope is NOT immunity, faithfully to methodology
review finding 7 and MD decision g: case (1) a relapse with no physical/cardiac
exposure at all is out-of-support / neutral (a possible mental-PEM trigger, parked R4),
NOT counter-evidence; case (2) an in-danger-window strain spike that does NOT relapse
above the matched baseline IS disconfirming. The pre-reg is explicit that the mental-PEM
escape applies ONLY to case (1) and "must never absorb a physical spike that failed to
relapse," and Section 10's "not supported" branch correctly routes case (2) to "the
physically-visible danger-window effect is not established." This closes the
unfalsifiable-on-the-downside risk the methodology review flagged. The physical/cardiac
scope limitation (blind to cognitive/emotional/orthostatic load, which
`pacing-and-crash-mitigation.md` Section 1 confirms draws on the same envelope) is
disclosed as a scope bound, not a rescue. Clean pass.

### 8. Power posture + single primary test + peak-primacy irrevocable -- SOUND (PASS)

Section 8 locks all three. "Cannot resolve = the pre-committed default reading of a CI
that spans the null" is stated and Section 10 refuses to upgrade a wide CI to
"suggestive" or "consistent with" -- the exact posture the methodology review finding 8
required be carried into the design body, not left in the falsification section. The
single primary test is named unambiguously (peak `max_hr_rank_lagged_lcera` x crash arm
x 10-day danger window x 4-day relapse window x matched-baseline contrast) and
everything else (activity-volume comparison, `hr_area` cumulative, dip arm, all
sensitivity bands) is explicitly secondary and NOT promoted if it wins (peak-primacy
irrevocable). The multiplicity context (effective independent looks ~3-4 per the null
MD Section 4, "must not be silently spent") is acknowledged. The design is honestly
declared underpowered for anything but a large effect at 28 event-level units, and the
primary deliverable is correctly framed as an estimate-with-CI, not a reject/accept
verdict. Single-pool primacy is preserved verbatim from the MD (decision f [P]). Clean
pass.

### 9. Discipline -- PASS

- **No PII.** Grep for name/email/`—` over the pre-reg returns nothing. Authorship
  block reads "Claude (Opus 4.8) under reviewer-mode-with-authorization, for the
  participant-researcher (repo owner)" -- no name, no email. Compliant.
- **No em-dashes.** None present (double-hyphen used throughout). Compliant.
- **GSS guardrail on first use.** Section 1 carries the explicit guardrail: "'stress'
  means Garmin's stress score (GSS), an HRV-derived measure, NOT mental or emotional
  stress," and "exertion/strain means physical activity/cardiac load." Compliant with
  the project's load-bearing stress-is-a-Garmin-measure rule.
- **Prior-given / confirmatory framing.** Section 2 answers all three CONVENTIONS
  Section 4.3 questions yes and correctly states the pre-reg protects the *outcome*
  (unseen until lock), not the *direction* (prior-given). Compliant.
- **Named counts (Section 3.6).** Event counts are named with scheme + unit + file
  ("29 crash episodes and 79 dip days on Stratum 4, `per_day_master.csv`, `is_crash` /
  `is_dip` / `crash_episode_id`, 2022-09-03 to 2026-06-05"). Compliant.
- **Lagged-lcera (Section 3.2).** All three exposures use the `[d-90, d-30]` LC-era
  baseline; the pre-reg defaults to `_lagged_lcera` as the section mandates. Compliant.
  (The one open item is the crash-masking branch of Section 3.3's contamination
  caveat -- self-flag (c) above.)

---

## Summary of required revisions before the lock is final

None is BLOCKING or MAJOR; all are pre-outcome, no-peek-safe tightenings that a binding
lock should carry, and all can be closed in one revision pass without changing the
claim, exposure, window, or primary test (so no v2):

1. **(self-flag c, MINOR)** Resolve the `_lcera` baseline crash-masking to a single
   definite primary branch by fact-checking the extractor now; state the branch + its
   file:line, keep one named sensitivity.
2. **(self-flag d, MINOR)** Add a per-replicate null mechanic paragraph mirroring the
   peri-event-covid precedent (block-permute the 28 event-level labels at E[L], recompute
   the one primary statistic, name the replicate count) so post-lock null discretion is
   zero.
3. **(self-flag b, MINOR)** Convert the autonomic-trend sensitivity from conditional to
   a definite commitment, but name the exact trend column (recommend
   `stress_mean_sleep_lagged_lcera_z` / `resting_hr_lagged_lcera_z`) and report its
   danger-window-conditional coverage rather than blank-committing on a "~99%" that does
   not hold for the lagged trend variant.
4. **(finding 3, MINOR)** Operationalise "comparable felt-state trajectory" (the RTM
   matching caliper) and state the matched-set ratio / caliper width; optionally report
   the available baseline-pool size per rank band (predictor-only, no-peek-safe).
5. **(finding 2 / 8 NITs, optional)** One line noting the `hr_area` demotion is
   scope-specific and does not override CONVENTIONS Section 3.3's general integral
   preference.

The design spine -- no-peek boundary, r3 cardiac-strain primacy, constructed
matched-baseline, event-level 28-unit null, crash-vs-dip slope interaction, two-case
scope, single-primary multiplicity control -- is sound and needs no change. The
revisions are mechanics-level; close them, re-date the lock, and proceed to the test
script.

---

## Authorship

Claude (Opus 4.8) fresh-session reviewer, for the participant-researcher (repo owner).
