# Research-thinking note — the autonomic-shape literature anchor: the curve is corroboration, the scale + convergence findings are the result

*Conversation date: 2026-06-29. Captured as essence, not transcript. Companion artefact: [`literature/reviews/expected_shapes_autonomic_signals_review.md`](literature/reviews/expected_shapes_autonomic_signals_review.md) (the full PubMed-sourced brief with DOIs).*

## Why this note exists

The descriptive programme's **shape-not-linear** observation (STOCKTAKE §6; near-zero linear ρ on the stress channels, but a real spline non-linearity F=28.27 p=0.0002 in HA-C3 v2) has been defended *internally* (a curve cancels under a linear ρ; the signal lives finer than daily). That defence is correct but incomplete — and, as the next section argues, the curve has been **mis-billed as the headline finding** when it is in fact theory-expected *corroboration*. This note does two things: (a) records that the **external-literature positioning HA-C3 §4.7/§4.8 flagged as still-needed is now done**, supplying the "why a curve is expected" backing; and (b) draws the line between that corroboration and the project's genuinely informative results — the *scale* finding (Pattern A) and the *lived-phase-convergence* finding (Q4.3), neither of which the shape literature predicts. Logged so a future `/research-interpret` Stage S₂ session, or whoever drafts HA-C3-v3, can pick up the thread without re-deriving it.

---

## The distinction this note exists to protect: corroboration vs result

It is tempting to bill "the felt-state↔Garmin relationship is non-linear" (shape-not-linear) as the descriptive programme's headline finding. After this literature work, that billing is **wrong, and saying so is half the point of the note.** Sort the claim into three parts:

1. **"A curve exists / the relationship is non-linear" — corroboration, not a finding.** The four-strand literature *predicts* a curve before anyone looks. Finding one confirms the instrument + data are good enough to surface the theoretically-expected structure — a non-trivial *measurement* success, and a debunking of the natural-but-wrong "ρ≈0 → the watch says nothing" inference — but it is **not a discovery about the world**, and must not be presented as one.

2. **"The signal cancels at daily resolution but returns episode-matched" (Pattern A / Q4.9) — genuinely informative, NOT predicted by the shape literature.** The four strands speak to the *shape* of a dose-response curve; they say nothing about *temporal scale*. That a daily average washes the signal to ρ≈0 while a 4-day pre-crash window recovers it (resting_hr +0.42z, etc.) is a fact about where in time the signal lives and how aggregation destroys it — the project's own result.

3. **"Lived-experience phase boundaries show up independently in the watch" (Q4.3 era_boundaries) — also genuinely informative, also outside the shape literature.** Boundaries placed from memory (never tuned to the data) each shift ≥4 of 7 channels; blind change-point detection lands 18 of 108 candidates on a lived seam. Convergent construct-validation between two independently-drawn maps — again not something the dose-response shape literature gives you.

**The synthesis:** parts 2 and 3 are the same species — *the watch independently registers structure defined from lived experience (episodes, phases), at scales and against frames a daily correlation cannot see.* That is the defensible interpretive headline. The curve (part 1) is merely the reason the **naive** look fails; the convergence is the reason the **careful** look succeeds. The literature's job in this note is to explain part 1 — so a flat ρ isn't mistaken for "nothing" — **not** to inflate it into the result.

---

## Trigger

A request to anchor the "not a straight line" finding in nervous-system science rather than curve-fitting — i.e., *before* trusting any shape we find, ask what shape autonomic physiology predicts we **should** see. ~15 PubMed searches → a new review brief. The motivating worry is the same one HA-C3 v2 §4.5 (L6) raised in passing: "the wrong-direction override on condition (c) at the x=70 midpoint sits inside [the self-report] noise envelope, **which the §4.7 external-literature positioning should engage with.**" This note + the brief are that engagement.

---

## What the literature brief establishes (the short version)

According to PubMed, a straight line is the **wrong default**, and the prediction of a *curve* comes from four independent directions — so a curve is over-determined by theory, not an artefact of one analyst's bin scheme (which is exactly why finding one is corroboration, per the section above, not a discovery):

1. **HRV is itself a non-linear transform of autonomic activity — a measurement fact, before any psychology.** The neural→sinus-cycle map is non-linear, imposing intrinsic rate-dependency on HRV indices ([Zaza & Lombardi 2001, *Cardiovasc Res*](https://doi.org/10.1016/s0008-6363(01)00240-1)); HRV and mean HR are bound by a non-linear inverse relation, and explicitly correcting for it *improves* prediction ([Pradhapan 2014, *Front Physiol*](https://doi.org/10.3389/fphys.2014.00208)). **A near-zero linear ρ on an HRV-derived channel is the predicted artefact, not a null.** Garmin/Firstbeat "stress" is HRV-derived → inherits this curvature directly.
2. **Yerkes–Dodson inverted-U** of arousal→outcome, whose shape *steepens with load/difficulty* ([Mair 2010, *Dose-Response*](https://doi.org/10.2203/dose-response.10-017.Mair); [Sörensen 2022, *PLoS Comput Biol*](https://doi.org/10.1371/journal.pcbi.1009976); [Fan 2022, *IJERPH*](https://doi.org/10.3390/ijerph191912434)) → predicts the channel-specificity STOCKTAKE §6 reports.
3. **Allostatic-load / exhaustion: both extremes are pathological, and activation collapses at the worst stage.** Whitehall II found a *non-linear, both-tails* association between negative-emotional-response and physiological dysregulation ([Dich 2014, *Psychoneuroendocrinology*](https://doi.org/10.1016/j.psyneuen.2014.07.001)); overtraining progresses from sympathetic dominance to "total autonomic dystonia" where *both* branches depress ([Kajaia 2017, *Georgian Med News*, PMID 28480859](https://pubmed.ncbi.nlm.nih.gov/28480859/)). **This is the physiological reading of HA-C3's non-monotone curvature (felt-state peaks at mid-range stress, not at the extremes): the worst felt days need not sit at the highest measured activation, because the most depleted state can blunt the very response the watch measures.**
4. **Neurovisceral integration** — a prefrontal–autonomic inhibitory feedback loop that, when compromised, flips to positive-feedback runaway: dynamically non-linear by construction ([Thayer & Lane 2000, *J Affect Disord*](https://doi.org/10.1016/s0165-0327(00)00338-4)).

The ME/CFS autonomic phenotype is consistent with strand 3 — markedly reduced HRV, vagal withdrawal, blunted response to challenge ([Stewart 1998](https://doi.org/10.1007/BF02267785); [Stewart 2000](https://doi.org/10.1203/00006450-200008000-00016); [Wyller 2008](https://doi.org/10.1111/j.1542-474X.2007.00202.x)), corroborating Pattern A (autonomic-load family elevates in the pre-crash lead-up).

---

## What this licenses (and what it does NOT)

**Licenses** — at Stage S₂ (external-literature positioning), the reframe:
> The felt-state↔autonomic relationship in this corpus is non-linear *as physiology predicts*. A flat linear correlation is the expected signature of measuring a curved, HRV-derived signal with a straight ruler — not evidence of "no relationship." HA-C3 v2's significant spline curvature, and the inverse direction of its failure of Wiggers' convex numbers, are concordant with mainstream arousal / allostatic-load / neurovisceral theory.

**Does NOT license** (carry the HA-C3 §4 discipline forward):
- It does **not** upgrade HA-C3 v2's REJECTED verdict. The verdict stands; the literature changes how we *frame* the curve, not the operationalisation-bound result.
- It does **not** transplant a specific curve. The cited cohorts (overtraining, allostatic-load, arousal-performance) are adjacent, not ME/CFS-identical; they license the *expectation* of a non-linear shape, not this body's particular one. L1 (single-subject reach) is unchanged.
- It does **not** make the inverted-U a SUPPORTED claim. Promoting it to a primary positive finding still requires the fresh pre-reg already named in HA-C3 §4.8 (HA-C3-v3 with the inverted-U / threshold shape as PRIMARY). The literature *motivates* that pre-reg; it does not substitute for it.
- The subject's prior was **null** (HA-C3 §4.6, verbatim "I did not know what to expect"). Theory-concordance is not prior-confirmation; this remains discovery-via-test.
- It does **not** make "the relationship is non-linear" a headline result. That is theory-expected corroboration (see "corroboration vs result" above); the project's informative results are the scale (Pattern A) and lived-phase-convergence (Q4.3) findings, which the shape literature does not predict.

### On the word "inverted-U" (a deliberate under-claim)

Do not let the literature's vocabulary over-describe our data. What HA-C3 v2 robustly licenses is **a significant non-monotone curvature** — three bin-means (3.96 → 4.27 → 3.83), felt-state peaking in the mid-stress band, with spline F=28.27 (p=0.0002) and convexity S=−0.74, against a flat linear ρ=−0.03. Calling that an "inverted-U" imports four things the data does not carry:

1. **A single smooth hump.** Three bins cannot distinguish a ∩ from a step, plateau-with-dip, or threshold. The registered spline's second derivative actually **flips sign** (NEG at x=35, POS at x=70) — concave low-mid, convex high — i.e. *not* a clean inverted-U; that sign-flip is precisely what fired the wrong-direction REJECTED override.
2. **A populated high end.** The true high-stress region is near-empty (original [60,100] bin n=1, absorbed). "The downturn at high stress" is really the [40,60] bin; genuinely high stress is unsampled, so "worst days aren't at highest stress" is partly *"we have almost no highest-stress days."*
3. **A meaningful hump.** Peak sits ~0.3–0.4 gevoelscore points above the tails — inside the §4.5 (L6) self-report noise envelope; the two tails are within noise of each other.
4. **Circularity with this very brief.** The brief invokes the Yerkes–Dodson *inverted-U* as the expected shape. Naming our data the same lets theory and finding validate each other by vocabulary — but Yerkes–Dodson is arousal→performance, ours is watch-stress→felt-state, and ours is an *informative falsification* of Wiggers' convex numbers, not a positive fit to any named curve.

**Use, in artefacts and on the site:** "a significant curvature — non-monotone, peaking at mid-stress, not the predicted accelerating decline." Reserve "inverted-U" for an explicitly-flagged loose visual gloss, never as the claim.

---

## Research-side action items this opens

### Own-research track
1. **HR-correction sensitivity check on the HRV-derived stress channels (NEW, highest leverage).** Because HRV carries a built-in non-linear mean-HR term ([Pradhapan 2014](https://doi.org/10.3389/fphys.2014.00208); [Zaza 2001](https://doi.org/10.1016/s0008-6363(01)00240-1)), part of any felt-state↔stress structure could be mean-HR leakage rather than autonomic-balance signal. Cheap descriptive run: re-express `all_day_stress_avg` / `stress_mean_sleep` net of `resting_hr` (regress out, or HR-correct per Pradhapan's divide-by-mean-RR-power approach) and re-check the HA-C3 curvature + the Pattern-A pre-crash elevation. Outcome either way is publishable: structure that survives correction is cleaner; structure that doesn't is an honest narrowing. Routing: `/research-interpret` D-stage descriptive, or `methodology/queued_work.md`.
2. **Feed HA-C3-v3 motivation.** When the inverted-U-as-PRIMARY pre-reg (HA-C3 §4.8 own-research track) is drafted, cite the four-strand prior as the *named expectation* — converting "exploratory curve-fit" into "pre-registered test of a theory-motivated shape," which is exactly the epistemic upgrade §4.3 confirmatory-framing rewards.

### External-literature positioning (Stage S₂)
3. **The brief IS the S₂ artefact seed for the C-stress-fatigue-shape cluster.** HA-C3 §4.8 external-research track named two studies we *can't* run (group-level inverted-U cohort; cross-instrumentation Garmin-stress-vs-subjective comparability). The brief supplies the literature scaffold both would sit in; when `synthesis/cluster-stress-fatigue-shape.md` reaches S₂, pull the brief in rather than re-searching.

### Methodology / Step-1 backbone
4. **Folds into the Step-1 literature backbone to-do** ([note 2026-06-26 §A](note_2026-06-26_scope_clarification_and_step1_steelman.md)). That to-do collects wearable-*validity* papers (Quer, Nelson, Shaffer…); this brief adds the *shape-validity* layer — why the signal's relationship to outcomes is expected to be curved. Same `methodology/watch_signal_validity_evidence_base.md` destination, distinct subsection ("expected shape", not "signal exists").

---

## What this does NOT change

- **Scope.** Still Steps 1+2+3 (note 2026-06-26). The brief strengthens Step 2's interpretation (signal↔felt-experience is curved-but-real), nothing past Step 3.
- **Descriptive discipline.** No causal claim added. "Expected shape" = physiological *prior*, not proof for this body.
- **The verdict ledger.** HA-C3 v2 stays REJECTED; the site's `/workings/not-a-straight-line` page keeps its finding — the change is *framing confidence*, not the result.

---

## Cross-references

- [`literature/reviews/expected_shapes_autonomic_signals_review.md`](literature/reviews/expected_shapes_autonomic_signals_review.md) — the full brief (PubMed, DOIs, method guidance §7).
- [`analyses/interpretation/HA-C3.md`](analyses/interpretation/HA-C3.md) §4.5 (L6 — flagged the §4.7 positioning need), §4.6 (null prior), §4.8 (own + external follow-up tracks this note feeds).
- [`analyses/interpretation/HA-C3p.md`](analyses/interpretation/HA-C3p.md) — sister HA (PARTIAL; detected curvature) in the C-stress-fatigue-shape cluster.
- `STOCKTAKE.md §6` — Patterns 3 (flat linear ρ) and A (pre-crash autonomic-load elevation); the descriptive substrate this anchors.
- [`analyses/descriptive/trajectory/era_boundaries/findings.md`](analyses/descriptive/trajectory/era_boundaries/findings.md) — Q4.3, the lived-phase-convergence result (part 3 above): lived boundaries each shift ≥4/7 channels; 18/108 blind change-points land on a lived seam.
- [`note_2026-06-26_scope_clarification_and_step1_steelman.md`](note_2026-06-26_scope_clarification_and_step1_steelman.md) §A — the Step-1 literature-backbone to-do this folds into.
- Site-side hook: `wiggers_research_story/site/docs/research-requests.md §G` R18 flag (c) "shape-assuming" — the editorial pipeline already expects this engagement.
- Companion review: [`literature/reviews/PEM_HRV_heart_rate_literature_review.md`](literature/reviews/PEM_HRV_heart_rate_literature_review.md), [`literature/reviews/SYNTHESIS_wearables_autonomic_PEM_research_programme.md`](literature/reviews/SYNTHESIS_wearables_autonomic_PEM_research_programme.md).

*Source database for the brief: PubMed; findings paraphrased, DOIs above. Research synthesis, not medical advice. n=1 instrument-test discipline holds throughout.*
