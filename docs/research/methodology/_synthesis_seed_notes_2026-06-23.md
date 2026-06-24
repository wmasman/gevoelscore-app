# Synthesis seed notes — 2026-06-23

**Status**: non-binding advisory artefact, producer-mode. Authored
2026-06-23. **NOT part of the structural pre-registration** of
[`synthesis_structure_map.md`](synthesis_structure_map.md). Relocated
here from the r1 draft of that map per the r2 fresh-session
methodology-review's R2 finding — keeping the candidate joint-reading
sketches inside the map's structural-pre-registration MD crossed the
§3.6 structure-vs-synthesis line that the map is supposed to honour.

**Status as input to S₁ sessions**: **advisory only**. A future Stage
S₁ (internal synthesis) session may:
- read these notes and use them as caveat-class context, or
- ignore them entirely and start the coherence call cold.

Either choice is methodologically correct. The notes record what the
r1 drafter *expected* the joint readings might look like, based on
the four ready HAs' result.md files at the time of map drafting; they
do **not** constrain what S₁ should find.

The underscore prefix follows the project convention for non-binding
planning artefacts (`_pending_literature_fetch.md`,
`_descriptive_stocktake_2026-06-23.md`,
`_plan_results_analysis_layer.md`).

---

## 1. Why these notes exist

When r1 of the synthesis-structure map was drafted, the drafter had
just read the four ready HAs' result.md files via the construct-
gathering Explore agent. Two coherence-read sketches emerged
naturally from that reading. The r1 draft included them in §3 of the
map under a "Coherence read for active clusters" subsection with the
disclaimer "S₁ session will make the actual call; this is not
pre-decided here."

The fresh-session methodology-review's R2 finding pointed out that
this disclaimer was structurally insufficient: downstream S₁ session
drafters reading the map cold would read the sketches as authoritative
even with the hedging, because the sketches' presence in the
structural-pre-registration MD lent them weight the disclaimer
couldn't fully discount. The §3.6 layer rule says the map records
structure, not synthesis; the sketches crossed that line even when
hedged.

The fix was to relocate the sketches to this separate file, marked
clearly as advisory-only and outside the map's structural scope.
This preserves the work (the sketches reflect real reading of the
four HAs' results) while honouring the §3.6 discipline.

## 2. Candidate joint reading — C-stress-fatigue-shape

**Cluster members**: HA-C3 v2, HA-C3p (per
[`synthesis_structure_map.md`](synthesis_structure_map.md) §3).

**Verdicts at the time of map drafting**:
- HA-C3 v2: **REJECTED** (wrong-direction monotonicity override).
- HA-C3p: **PARTIAL** (conditions (b) + (c) PASSED — curvature
  machinery detected non-linearity; condition (a) Jonckheere-Terpstra
  FAILED — non-monotone inverted-U pattern, trajectory peaks at Q4).

**Candidate joint reading the r1 drafter sketched**:

> "The participant's stress-fatigue mapping has detectable curvature
> (HA-C3p's PARTIAL on (b)+(c) machinery surfaces this), but the
> shape is **inverted-U / threshold-like rather than monotone-
> convex** (both HAs fail monotonicity; the bin-mean trajectories
> peak at mid-range stress and drop at high range). Wiggers'
> *direction* (monotone-decreasing gevoelscore with rising stress)
> does not match this participant; Wiggers' *mechanism* (curvature/
> non-linearity in the stress-fatigue mapping) does."

**Caveats S₁ should weigh**:
- The two HAs' bin schemes differ (Wiggers-verbatim 4-bin absolute
  vs personal-quintile 5-bin); the bin schemes produce different
  peak locations (HA-C3 v2 peaks at the 30-40 junction; HA-C3p
  peaks at Q4 = upper-mid stress range). Whether these are the same
  underlying shape or two different shapes is the substantive
  question; the sketch above assumes they're the same shape on
  different x-axis scalings.
- The HA-C3p result.md §6 4-cell agreement matrix names a "Wiggers'
  numbers wrong for this participant but underlying shape IS REAL
  in the INVERSE direction" reading explicitly **as caveat-class
  post-hoc, NOT as substantive output**. The S₁ coherence call must
  decide whether to inherit / cite / discard that reading.
- The L4 (analyst-is-subject) prior of "Wiggers' direction" was
  prior-driven (the HAs were drafted with Wiggers' canonical claim
  as the testable direction); per CONVENTIONS §4.3 the
  prior-driven-hypothesis-is-confirmatory discipline applies, which
  bounds the inversion-claim inferential reach.

**S₁ alternatives the sketch does not consider**:
- Both HAs' results could be artefacts of cell-size constraints
  (HA-C3 v2's B4 collapse-to-B3 at dry-run; HA-C3p's right-shifted
  Q5 representation in the unmedicated sub-arm). The L7 survivorship
  caveat may dominate.
- The curvature signal could be real but driven by a confounder not
  yet identified (e.g., circadian timing of high-stress days
  clustering with sleep-deprived following days).
- S₁ may legitimately call this cluster CONFLICT rather than
  PARTIALLY CONCORDANT, given the binary-verdict reading (REJECTED
  vs PARTIAL).

## 3. Candidate joint reading — C-bout-substance (with C-bout-framework cascade)

**Cluster members**: C-bout-substance = HA-C4c (per the r2 split);
C-bout-framework = HA11-bout-redo (upstream calibration precondition).

**Verdicts at the time of map drafting**:
- HA11-bout-redo: **PARTIAL** (bars 1 + 2 PASSED — direction +
  effect-size reproduction at +20.26 pp; bar 3 FAILED — block-
  permutation p = 0.2609, not significant at α = 0.05 due to small
  n_calm=70 / n_crash=11).
- HA-C4c: **PARTIAL** (bar (a) PASSED — p = 0.0001, statistically
  distinguishable from null at high confidence; bar (b) FAILED —
  Cliff's δ = +0.120 below the +0.20 threshold for small-to-medium
  effect-size).

**Candidate joint reading the r1 drafter sketched** (now reframed
per the r2 cluster split):

> "The bout-level operand family is **fit-for-purpose** (C-bout-
> framework's bars 1+2 PASS confirm the operand reproduces HA11 v1's
> effect-size magnitude at bout resolution); the **substantive
> heavy-T vs non-heavy-T differentiation exists but is modest**
> (C-bout-substance's high-p / low-δ configuration shows
> statistically real but small effect). Both clusters' bar-failures
> (HA11-bout-redo on p-value, HA-C4c on effect-size) suggest the
> operand is approaching the **corpus's effect-size detection limits**
> — not a methodology failure, but a corpus-property constraint."

**Caveats S₁ should weigh**:
- The era-scope mismatch is structural: C-bout-framework runs
  unmedicated × train; C-bout-substance runs cross-phase pooled.
  This is by design (each cluster's question requires its own
  scope), but the joint reading must respect that the framework's
  validity claim is for unmedicated × train data and may not
  generalise cleanly to the cross-phase pool.
- C-bout-substance's small effect size could reflect (a) genuine
  smallness of the heavy-T discrimination, (b) cross-phase pooling
  diluting an unmedicated-only signal (the §4.10 sensitivity arm
  shows δ = +0.059 unmedicated-only, REJECTED — pooling does the
  work of reaching p < 0.05 by increasing n, but at the cost of
  effect-size compression), or (c) both. S₁ cannot disambiguate
  without further descriptive work.
- The PPV-with-base-rate computation (per locked-plan §3.10 hard
  predictive gate) is the binding next step for any tier-2+
  actionability claim; that computation happens at Stage A on
  K-bout-recovery-signal, not at S₁.

**S₁ alternatives the sketch does not consider**:
- The "corpus detection limits" framing may be too charitable to
  the operand. An alternative reading: the operand IS detecting a
  signal but the signal is too small to be useful, regardless of n.
  These differ in what they imply for actionability tier.
- The bimodal-arousal-pattern speculation that the r1 sketch hinted
  at (linking C-bout-substance's modest effect to C-stress-fatigue-
  shape's inverted-U pattern) is **not in scope for S₁ on
  C-bout-substance** — that would be a Stage S₂ (cross-construct)
  reading or a downstream Stage A claim. S₁ should refuse the
  cross-cluster reading.

## 4. Cross-cluster cross-reference (Stage S₂ territory)

The r1 drafter also sketched a cross-cluster reading linking
C-stress-fatigue-shape's inverted-U pattern to C-bout-substance's
modest effect size. That reading is **out of scope for S₁** (which
operates one cluster at a time); it would belong to either Stage S₂
(contextualisation against external literature on bimodal-arousal
patterns in PEM populations) or a separate cross-topic synthesis at
Stage A or later.

The reading is recorded here for completeness, marked clearly as
cross-cluster speculation:

> "If C-stress-fatigue-shape's inverted-U holds (mid-stress peak,
> drop at high stress), and C-bout-substance's modest heavy-T
> effect size reflects the high-stress tail being where the daily-
> aggregate signal compresses, then both readings could share a
> bimodal-arousal mechanism — low stress days have sharp recovery
> (HA11 v1's U-dip pattern); high stress days have stuck stress
> (HA-C4c's failure-to-return pattern); the inverted-U at daily
> aggregate may be the visible joint signature of two different
> within-day dynamics."

S₁ sessions on either cluster MUST NOT use this speculation as
input. Any future S₂ or cross-topic session that wants to evaluate
the speculation should treat it as a candidate hypothesis to test,
not a finding to inherit.

## 5. How to use these notes (if at all)

S₁ session drafters reading these notes should treat them as a
**colleague's notes-on-the-data** — useful as descriptive context for
what the r1 drafter saw in the four HAs' results, but not as
constraints on the S₁ coherence call. The S₁ guide (forthcoming as
[`internal_synthesis.md`](internal_synthesis.md) per the locked plan
§6.3) will be the authoritative procedure for producing the coherence
call.

If an S₁ session lands a coherence call that contradicts the sketch
above, the contradiction is itself useful: it surfaces a place where
the r1 drafter's quick read of the result.md files diverges from the
disciplined synthesis the S₁ guide produces. The divergence should be
logged in the S₁ artefact's `open_inputs` block as descriptive
context.

## 6. Cross-references

- [`synthesis_structure_map.md`](synthesis_structure_map.md) — the
  map this file was relocated out of; §3 references this file as
  advisory only.
- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  §3.6 (structure-vs-synthesis line that this relocation honours);
  §6.3 (internal synthesis guide, where the S₁ coherence-call
  procedure will land).
- [`research_line_limitations.md`](research_line_limitations.md)
  (L4 prior-driven discipline; L7 survivorship; both relevant to the
  C-stress-fatigue-shape caveats above).
- [`reviews/methodology-synthesis_structure_map-2026-06-23.md`](../reviews/methodology-synthesis_structure_map-2026-06-23.md)
  R2 finding (the fresh-session review note that produced this
  relocation).
- HA result.md files:
  [HA-C3 v2 result](../analyses/hypotheses/HA-C3/result.md);
  [HA-C3p result](../analyses/hypotheses/HA-C3p/result.md);
  [HA-C4c result](../analyses/hypotheses/HA-C4c/result.md);
  [HA11-bout-redo result](../analyses/hypotheses/HA11-bout-redo/result.md).
