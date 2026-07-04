# Review: HA01c single-pool cross-check pre-registration (HA01c-single-pool-crosscheck)

**Target**: [../analyses/hypotheses/HA01c-single-pool-crosscheck/pre-registration.md](../analyses/hypotheses/HA01c-single-pool-crosscheck/pre-registration.md)
**Target commit**: untracked working-tree file (`git status` = `??`; never committed as of review). Reviewed at working-tree state 2026-07-03, repo HEAD `8820e65`.
**Reviewer mode**: Claude (independent peer reviewer per CONVENTIONS §1.2). Fresh session — no exposure to the drafting context; doc-only knowledge.
**Review date**: 2026-07-03

---

## 1. What the data shows

The target is a **pre-registration**, not a result — it commits a plan to
re-run the already-locked HA01c effective-exertion precursor test under the
single-pool framework (full Stratum 4, n=29 crash episodes; block-permutation
null E[L]=7; stationary-bootstrap CI; the 2023-12-31 split demoted to an M3
descriptive overlay). The locked spec (metric `effective_exertion_rank_lagged`,
threshold ≥0.75, 4-day lead-up, one-sided elevated) is inherited verbatim; only
the **validation framework** is swapped (§2 table). The pre-reg's stated premise
(§1, §preamble) is that "the seven scorecard signals were re-run single-pool
… HA01c was not," so this cross-check is needed to give the effective-exertion
channel "an honest single-pool number." It commits a verdict rule (SUPPORTED iff
permutation p < 0.05), four decisions flagged for confirm-at-review (§6), and an
honest-expected-outcome section (§9) that pre-declares usability as "robustly
poor" while insisting the significance verdict is "genuinely uncertain and must
not be pre-judged."

The empirical framing (single-pool discrimination, permutation null, E[L]=7,
M3-as-number) is faithful to the two cited methodology MDs. The problem is not
the method — it is that **the central premise is factually wrong against the
committed source data**: HA01c has already been re-run single-pool under a
near-identical protocol, and the result is on record.

---

## 2. What fired and why

### Layer 1 — Universal reporting (inherits from SCRIBE 2016, STROBE 2007)

- **[L1.1 — CONVENTIONS §2.1 descriptive-before-inference; pre-registration integrity]** — **BLOCKING.**
  The pre-reg's load-bearing premise is that HA01c "was not" re-run single-pool
  (§preamble line 40-42: *"The seven scorecard signals were re-run single-pool …
  HA01c was not"*; §1). This is contradicted by a **committed** artefact the
  pre-reg never cites:
  [`analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md)
  (R14 single-pool re-anchor, committed `958bfe2`, 2026-06-30). That file's
  §2 table row **HA01c** (line 21) and §3 narrative (lines 73-78) already report
  the single-pool re-run of the *same* operand — "frac windows with ≥1 day in
  4-day leadup at eff_exertion_rank_lagged ≥ 0.75; median rank on triggering
  episodes ≥ 0.875" — with **disc_pp = +19.6, perm p (E[L]=7) = 0.0290,
  frac_crash = 0.821, frac_null = 0.625, n = 28/200, verdict SUPPORTED**, and
  explicitly lists HA01c (line 124) as one of two HAs whose locked
  OVERALL-SUPPORTED verdict reproduces under single-pool. The proposed test is
  therefore not "the honest single-pool number that does not yet exist" — it is
  a near-duplicate of a run whose answer (SUPPORTED, p ≈ 0.029) is already on
  record. *Why it matters*: pre-registration's entire epistemic value is that
  the analyst commits before the answer is known (STROBE item 6 / SCRIBE
  design-specification; CONVENTIONS §2.1). Pre-registering a test whose result
  already exists — while §9 frames the verdict as "genuinely uncertain … not a
  foregone conclusion" — is not a genuine pre-commitment; the drafting session
  either did not know about findings.md or did not reconcile with it, and either
  way the reader is told this number is unknown when it is known and points
  clearly to SUPPORTED. This must be reconciled before any run.

- **[L1.1 / L1.4 — CONVENTIONS §2.1; Q10 row-list scope]** — **SUBSTANTIVE.**
  The §preamble claim that "HA01c is not currently in Q10's row-list (HA01b,
  HA02c, HA08, HA11, H05); this file adds it" is **literally true** against the
  canonical Q10 recipe
  ([`queued_work.md` §Q10, line 646](../methodology/queued_work.md): rows =
  HA01b, HA02c, HA08, HA11, H05). But it is misleading in context: the R14
  findings.md already went **beyond** the Q10 row-list (it evaluated 12 HAs
  including HA01c and HA07d) and did the HA01c single-pool re-run there. So the
  honest statement is not "HA01c has not been done and this file adds it," but
  "HA01c was done in R14 outside the canonical Q10 list, and this file promotes
  that descriptive overlay into a dedicated pre-reg with a hardened verdict
  rule." The pre-reg's own framing hides the prior run behind the narrower Q10
  list. *Why it matters*: §2.1/§1.4 require confounders and prior work to be
  named, not silently controlled for; the existence of a prior single-pool
  number is the single most important piece of context for this pre-reg and it
  is absent.

- **[L1.3 — CONVENTIONS §2.2; permutation scheme fully specified]** — **MINOR.**
  §4.4 specifies the permutation null as a *stationary-block bootstrap of the
  anchor labels drawn from the background pool*. The R14 findings.md achieved
  its p = 0.0290 under "block-permutation null at E[L]=7, B=10,000, seed
  20260624" (findings.md line 4). The two schemes are described differently
  (this pre-reg resamples anchor labels from the ordinary-window background pool;
  R14's header describes a block-permutation of crash/null labels). They may or
  may not be identical implementations. Because the pre-reg is proposing a fresh
  run that should reproduce (or consciously differ from) the R14 number, the
  relationship between the two null constructions must be stated: is this the
  same null as R14 (in which case p ≈ 0.029 is essentially known) or a
  deliberately different one (in which case say why, and why the difference is
  expected to matter)?

### Layer 2 — Observational n=1 (inherits from Daza 2018, Personal Science)

- **[L2.5 — memory `project_garmin_research_bias_boundary`; held-out framing]** — no fire.
  The pre-reg does not over-claim held-out structure; it explicitly retires the
  split as primary and demotes it to a descriptive overlay (§7), consistent with
  `train_validate_split_fate.md` §4.4's tactical-vs-analytical framing. It does
  not regress to "user has been continuously analysing the data." Passes.

- **[L2.6 — CONVENTIONS §4.3; prior-driven vs post-hoc]** — no fire (framing correct),
  but see L4.8 for the interaction with §9. HA01c's parent hypothesis is
  prior-driven (lived exertion→crash experience + the HA01b per-axis diagnostic);
  confirmatory framing is appropriate.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

- **[L3.1 / L3.4 — `permutation_null_block_length.md`; autocorrelation + block length]** — no fire.
  Autocorrelation is handled head-on: block-permutation null + stationary
  bootstrap CI at E[L]=7 (§4.4, §4.5), plus a data-driven E[L]* companion with
  the factor-of-2 flag (§4.6) exactly per the MD's result template (MD3
  Operational-consequences item 2). This is the strongest part of the pre-reg
  and is well above the Natesan-Batley 2023 bar (83.8% of n-of-1 studies ignore
  autocorrelation). See §3 below.

- **[L3.3 — multiplicity]** — see L4 / decision-2 discussion; the "re-expression
  of HA01b's channel" argument is defensible but has a wrinkle (§ decision calls
  below). Not an independent fire beyond that.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3, §4)

- **[L4.8 — CONVENTIONS §4.2/§4.3; caveats-vs-apriori, verdict not pre-judged]** — **SUBSTANTIVE.**
  §9 was clearly rewritten to separate "usability is robustly poor" (base-rate
  fact, does not depend on p) from "the verdict is genuinely uncertain." The
  *structure* of that split now complies with §4.2 — it keeps the specificity
  caveat (KEEP-class) and refuses to pre-commit the verdict. **But** the
  uncertainty claim is undercut by the very data the pre-reg cites elsewhere:
  §9's own reasoning ("dry synthetic checks put the iid-background pooled p near
  ~0.02 … block-bootstrap then inflates that back up … can land on either side
  of 0.05") is speculating about a number that **already exists** at 0.0290
  (findings.md line 76) — under a *real* block-bootstrap null, not a synthetic
  one. So §9 presents as "genuinely uncertain, could go either way" a quantity
  the committed corpus already resolves to SUPPORTED at p = 0.029. That is the
  §4.3 failure mode inverted: not a-priori-claiming an unestablished effect, but
  a-priori-framing-as-uncertain an effect the source data has already
  established. The honest §9 would read: "R14 already produced p = 0.0290
  (SUPPORTED) under a real E[L]=7 block null; this run is a confirmation /
  reproducibility check of that number under the anchor-label null variant, not
  a first look." *Magnitude*: substantive — the verdict is not biased toward
  NOT-SUPPORTED (the stress-test worry), but the "must not be pre-judged"
  framing is itself slightly misleading given the prior run points to SUPPORTED.

- **[L4.6 — CONVENTIONS §3.6; name every count]** — no fire.
  Counts are well-named: "29 episodes … crash_v1 tier-1 from labels_crash_v2.csv"
  (§3), base rate "2.11% (29/1372)" (§4.7), n_clean floor (§4.1). Compliant.

- **[L4.1 / L4.2 — §3.1/§3.2; lagged baseline]** — no fire. Uses
  `effective_exertion_rank_lagged` (the lagged rank, §2). Correct family.

- **[L4.3 — §3.3; definitional pairs]** — no fire. Single axis; no pair
  double-count.

### Side observations

- **Side** — §9 usability arithmetic is internally consistent: p_bg ≈ 0.605 →
  specificity ≈ 39.5%, matching frac_null = 0.625 in R14 (spec ≈ 37.5%); PPV
  ~2-3% at 2.11% base rate is consistent with the trust-panel Tier-C band. Base
  rate 29/1372 = 2.114% checks out. No numeric error here.
- **Side** — the pre-reg conflates two different source sets under one "seven
  scorecard signals" label. The trust-panel export's seven
  ([`cards/trust-panel-export.md`](../analyses/garmin_exploration/cards/trust-panel-export.md) §2:
  HA07d, HA11, HA06b, HA07c, **HA01b**, HA10, H02b) does **not** contain HA01c —
  it contains HA01b (the composite). The R14 findings.md set (12 HAs) **does**
  contain HA01c. §1's sentence "the seven scorecard signals were re-run
  single-pool; HA01c was not" reads the trust-panel's seven, then infers HA01c
  was never run — but HA01c *was* run, in the R14 twelve. The two sources must be
  cited distinctly.
- **Side** — §5 asserts the operative single-pool bar is "only HA07d cleared."
  Verified: trust-panel §"Verdict honesty" confirms "only HA07d is single-pool
  SUPPORTED" among its seven. But R14 findings.md line 124 lists **two**
  OVERALL-SUPPORTED-reproducing HAs: HA07d **and HA01c**. So on the R14 set,
  HA01c already *is* the second single-pool SUPPORTED — which is exactly the
  number this pre-reg claims not to have.
- **Side** — §9's per-era Fisher p-values (0.14 train, 0.11 validate) check out
  against
  [`primary-verdict-statistics.md`](../analyses/garmin_exploration/cards/primary-verdict-statistics.md)
  lines 28-29 (0.1355 train, 0.1085 validate). Correctly cited.

---

## 3. What does not fire (selective)

- **L3.1 / L3.4 (autocorrelation + block length)** — passes with strong evidence.
  §4.4-§4.6 implement the block-permutation null, stationary-bootstrap CI, and
  data-driven E[L]* companion + factor-of-2 flag exactly as
  [`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md)
  Operational-consequences item 2 specifies. Seed and B are locked (20260703,
  10,000). This is textbook compliance with the cited MD.
- **L4.6 (named counts)** — passes; every episode/day count carries scheme +
  unit + source file per §3.6.
- **L2.5 (held-out framing)** — passes; the split is correctly demoted to an M3
  descriptive overlay "number, not a narrative" (§7) per
  [`train_validate_split_fate.md`](../methodology/train_validate_split_fate.md)
  §5.8, with the explicit disclaimer that the overlay answers robustness-to-partition,
  not effect-change-over-time.
- **HA01d lock-clause reasoning** — passes on its own terms. HA01c's
  hypothesis.md preamble locks "claim, measurement, threshold, window, or
  direction"; changing the *validation framework* (pooling + null + CI) touches
  none of those five, so no HA01d is created. Retiring the both-eras rule is a
  change to the *verdict-combination rule across eras*, not to threshold or
  direction — it is genuinely a framework change, so the pre-reg's reasoning
  here holds (see stress-test note below).

---

## 4. What would strengthen this finding

1. **Cite and reconcile with R14 findings.md before locking.** Add a §
   "Relationship to the R14 single-pool re-anchor" naming
   [`single_pool_reanchor/findings.md`](../analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md)
   (committed `958bfe2`), quoting its HA01c row (disc +19.6 pp, p = 0.0290,
   SUPPORTED). Re-frame this pre-reg's purpose from "produce the missing number"
   to one of: (a) a **reproducibility/confirmation** run of the R14 number under
   the anchor-label null variant, or (b) a **promotion** of the R14 descriptive
   overlay into a dedicated hardened-verdict-rule artefact. Either is legitimate;
   the current "does not yet exist" framing is not. Effect: restores
   pre-registration integrity and removes the L1.1 blocking fire.

2. **State the null-construction relationship to R14 explicitly (§4.4).** Say
   whether this pre-reg's anchor-label stationary-block null is the same
   implementation as R14's "block-permutation null at E[L]=7" or a deliberate
   variant, and if a variant, why the difference is expected to move the p-value.
   Per [`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md).
   Effect: makes the §9 "uncertain verdict" claim honest — either the number is
   ~known (same null) or the divergence source is named.

3. **Rewrite §9's uncertainty paragraph to reflect the prior run.** Replace the
   synthetic-check speculation ("dry synthetic checks put the pooled p near
   ~0.02") with the actual R14 result (p = 0.0290 under a real block null). Keep
   the E[L]* caveat as the one genuine open variable. Per CONVENTIONS §4.2/§4.3.
   Effect: the section stops presenting a resolved quantity as unresolved, which
   is the mirror-image of the a-priori failure mode §4.3 guards against.

4. **Disambiguate the two "seven"/"twelve" source sets (§1, §5).** Cite the
   trust-panel seven (which contains HA01b, not HA01c) and the R14 twelve (which
   contains HA01c) as distinct provenances. Effect: removes the inference error
   that "HA01c was not run" and clarifies that HA01c is already the second
   single-pool SUPPORTED on the R14 set.

---

## 5. Verdict

**REVISION RECOMMENDED** — Layer 1 blocking fire: the pre-reg's central premise
that HA01c "was not re-run single-pool" is contradicted by the committed R14
re-anchor findings.md, which already reports the same-operand single-pool run as
SUPPORTED at permutation p = 0.0290; pre-registering an "uncertain" test whose
answer is already on record breaks the pre-registration integrity the artefact
depends on, and the fix is to cite/reconcile with R14 and re-frame as a
confirmation run rather than a first look (not to change the method, which is
sound).

---

### Stress-test calls on the four §6 decisions and the HA01d clause (requested)

- **HA01d lock clause (does retiring the both-eras rule sneak in a
  direction/threshold change?)** — **The reasoning holds.** HA01c's hypothesis.md
  preamble locks claim/measurement/threshold/window/direction; the both-eras rule
  lives in §4.7 as a *verdict-combination rule across eras*, not in the locked
  five. Swapping "both-eras 3-criterion bar" for "single-pool permutation p" does
  not alter the ≥0.75 threshold, the 4-day window, or the one-sided-elevated
  direction — the per-episode trigger is inherited verbatim (§4.1). So no HA01d
  is created. The *legitimate* concern is not HA01d; it is that the new
  single-pool verdict is **more lenient** than the retired both-eras + v2 gate
  (which returned "SUPPORTED-with-stability-mixed, NOT load-bearing"), so the
  pre-reg must not let a bare single-pool SUPPORTED silently re-open the
  load-bearing status the v2 diagnostic withheld. §8's off-scorecard placement
  partly guards this, but it should say so explicitly.

- **Decision 1 (verdict rule = permutation-p primary):** **CONFIRM.** The
  single-pool framework mandates permutation null + CI
  ([`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md));
  the legacy 3-criterion bar has no significance/CI component, and R14 already
  used exactly this permutation-p rule (p = 0.0290 → SUPPORTED). Consistent.

- **Decision 2 (multiplicity = re-expression of HA01b's channel):** **CONTEST
  (mild).** HA01c and HA01b are *not the same primitive* — HA01b is the
  MAX-of-4-axes composite (single-pool NOT-SUPPORTED, p = 0.3689 in R14 line 15);
  HA01c is the single-axis `effective_exertion_rank_lagged` (SUPPORTED, p = 0.0290).
  Calling HA01c a "re-expression of HA01b's channel" so it "does not add to the
  effective-N budget" is convenient given HA01c is the one that clears. It is
  defensible (same underlying exertion axis, already represented on the
  scorecard) but it is also the self-serving direction. Safer: report HA01c
  against *both* alpha = 0.05 and the effective-N Bonferroni alpha ≈ 0.0125 (the
  pre-reg already commits to this in §5) and let the reader see that p = 0.0290
  clears 0.05 but **not** 0.0125 — which materially changes the headline.

- **Decision 3 (permutation scheme = anchor-label block-bootstrap from the
  background pool, E[L]=7):** **CONFIRM, with the reconciliation caveat.** It is
  the closest match to the MD's "permute labels in blocks drawn from the
  geometric distribution." But because R14 already produced a p under a
  block-permutation null, decision 3 must state whether it reproduces R14's null
  or deliberately differs (see strengthening item 2). Confirm the scheme; require
  the R14 relationship stated.

- **Decision 4 (off-scorecard placement):** **CONFIRM.** Keeping the scorecard at
  seven and reporting HA01c as an adjacent per-axis companion to HA01b is the
  honest placement — HA01c is the single-axis sibling, not an independent eighth
  signal, and the "1 of 7 supported" headline should not silently become "2 of 8."
  This decision also happens to be the guardrail against the load-bearing-status
  concern above; make that dual purpose explicit.

---

## Methodology

This review walks the 4-layer checklist defined in
[reviews/README.md](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

Project-specific audit hooks from
[../CONVENTIONS.md](../CONVENTIONS.md) §3 and §4.
