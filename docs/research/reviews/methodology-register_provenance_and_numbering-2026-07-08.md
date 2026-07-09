# Methodology review: Register provenance & numbering — the Guide/Beyond split and its id discipline (methodology/register_provenance_and_numbering.md)

**Target**: [../methodology/register_provenance_and_numbering.md](../methodology/register_provenance_and_numbering.md)
**Target commit**: working-tree state, untracked file (`??`) as of 2026-07-08; repo HEAD `5b75913`. Reviewed as the on-disk DRAFT r1.
**Reviewer mode**: Claude (independent methodology peer reviewer per CONVENTIONS §1.2; producer-mode MD under §2.2 four-input bar). *Fresh session — no exposure to the drafting context; doc-only knowledge.*
**Review date**: 2026-07-08

---

## 1. What the MD specifies

The MD locks a **structural (registry-organisation) choice, not a statistical one**. It binds four things: (a) the **Guide/Beyond split** on a single declared axis — *authorship of the tested operationalisation* (Wiggers' own → Guide `wiggers_testable_hypotheses.md`; the subject's own, including subject refinements of a Wiggers seed → Beyond `personal_hypotheses.md`), with hybrids handled by non-destructive **dual-attribution** rather than relocation, and the `founderandthecity` external-comparator register held explicitly outside the binary (§2); (b) a **`register:` provenance tag** on every `registry.md` test row, with five values (`wiggers:<claim>` / `beyond:<P#>` / `foundational` / `methodological` / `external-comparator`) and a projection rule mapping the first two onto the site's two Layer-4 ledgers (§3); (c) **numbering & id-coherence rules** — `P#` as the canonical Beyond thread id, a declared kebab-case slug as the backend↔site join key, a per-entry crosswalk block reconciling the four id vocabularies, and `ROUTED`/dual-attribution as the only cross-split mechanism (§4); and (d) a **`kind × stage` status model** for the site export, both axes derived from backend state, never hand-set (§5). Framing is producer-mode infrastructure; §7 explicitly invokes the four-input bar "in the lighter form used for the guide MDs." Status is DRAFT r1, not locked — Phase 0 of the R36 site request, with the ledger reconciliation, tagging, and export gated as later reviewer-mode-with-authorization work (§9). Downstream artefacts that inherit the choice: `personal_hypotheses.md`, `registry.md`, `STOCKTAKE §2a`, and the site's `addendum-register.json`.

---

## 2. What fired and why

### Spine — §2.2 four-input bar (inherits from CONVENTIONS §2.2)

#### I1 — Best-practices standards

- **I1.1 — no data-management state-of-art named for the id-coherence half (§4). Minor** (the lighter bar for a structural MD tempers it). §7 input 1 names SCRIBE 2016 + CENT 2015 as the standards for the *provenance-transparency* rationale, which is apt for the split's *why*. But the MD's genuinely novel machinery is in §4 — one canonical identifier (`P#`), a declared join key (the slug), a crosswalk table across four vocabularies, and a provenance tag. That is a data-architecture question with an established state-of-art the MD does not name: **W3C PROV** provenance modelling, the **FAIR** findability principle **F1** (globally unique, persistent identifiers), and classic **authority-control / linked-data** discipline (a single canonical id plus crosswalk rather than parallel id spaces). §2.2's I1.1 makes silence the fire, not non-adoption — naming and then adopting-or-rejecting these would convert §4 from "sensible-looking" to "deliberate application of known join-key discipline." Rule 3's "no new relocation vocabulary" and Rule 2's "reuse the existing slug vocabulary" are in fact *exactly* authority-control instincts; the MD just doesn't say so.

#### I2 — Established literature

- **I2.2 — the Daza 2018 citation (§7 input 2) is ornamental-leaning. Minor.** Daza's within-subject n-of-1 counterfactual framework speaks to *causal estimands in single-subject designs*, not to *author-attribution of hypotheses* or register organisation. The sentence offered — "supports treating the Beyond register as the subject's native confirmatory register, distinct from tests of an external author's claims" — does not draw on Daza's actual reasoning or evidence; the "distinct from an external author's claims" move is an authorship distinction Daza never makes. §2.2's rule is "never cite a paper because they did it that way … cite it because their reasoning, evidence, or simulation results bear on the choice." The materially-load-bearing anchor here is the MD's *own* CONVENTIONS **§4.3** (prior-driven hypotheses are confirmatory; the audit asks *which* prior drove the hypothesis) — the `register:` tag is precisely the durable record of that prior, and that mapping is exact. Leaning on §4.3 and dropping or re-grounding Daza would tighten input 2.

#### I3 — Tradeoff vision

- **I3.3 — the "Dual-axis" rejection rationale in §6 is undercut by the MD's own C4b worked example. Substantive.** §6 rejects a provenance-on-backend / scorecard-on-site dual axis as "unnecessary once the sanity check confirmed the *current* site already splits on authorship … Both sides already share one axis; a second axis and its reconciliation tag would add machinery to bridge a gap that no longer exists." But the C4b / `rest-stress-low-motion` case *is* a live gap: the backend currently files this thread in the **Guide** ledger (`wiggers_testable_hypotheses.md` `### C4b`; `personal_hypotheses.md` P5a is stamped "ROUTED to Wiggers register"), while the site surfaces `rest-stress-low-motion` on **/beyond** (`data/addendum.json`, blurb "the tweak is mine, not hers"). That is backend and site disagreeing on authorship placement for a real thread — the exact gap §6 says "no longer exists." §8 then *resolves* it by moving backend C4b → Beyond (P11), which is itself the reconciliation action §6 claims is unneeded. The tradeoff reasoning would be sound if it framed the single-axis choice as the thing that *closes* the one live discrepancy (backend moves to match the site), rather than asserting the axes already agree everywhere. §3.2's whole point is that an implicit tradeoff is the failure mode; here the tradeoff is stated but rests on a premise its own §8 contradicts.

#### I4 — Research limitations + objectives

No fires. See Section 3.

### Layer 1 — Discipline gates (inherits from CONVENTIONS §2.1, §4.1-§4.3)

No fires. L1.2 (§4.1 no interpretive marks): the MD locks a register organisation, bakes no imputed mechanism into a measurement — the `register:` tag records *provenance*, not a physiological read. L1.3 (§4.2 caveats vs a-priori): §5's two encoded disciplines ("a `stage` is not a verdict"; "descriptive `done` is a finished result, never a lesser not-yet-tested state") are explicitly anti-presuppositional and do not lift any phenomenon from caveat to analytical basis.

### Layer 2 — Observational n=1 (inherits from Daza 2018)

- **L2.4 — the P5a/C4b provenance narrative does not trace to the recorded routing rationale, and §8 reverses a user-directed routing without disclosure. Substantive — highest priority.** Two coupled problems on the same thread:

  1. **§2.2 mischaracterises why P5a was routed.** It states dual-attribution "already runs in one direction (`personal_hypotheses.md` P3 and P5a are `ROUTED to Wiggers` because, on inspection, they *were* Wiggers-native)." P3 genuinely is Wiggers-native — `personal_hypotheses.md` P3 routes to A4 because the lived component is "*retrospective felt-recognition* of the pattern Wiggers describes, not an active-monitoring prior." But P5a's own routing note (`personal_hypotheses.md` P5a) says it was routed "per user-direction for unambiguous placement: Wiggers C4 is the dominant prior; **the motion filter is the participant's operational refinement on the same shape**, not a distinct theoretical claim." That is the opposite of "Wiggers-native" — the discriminating operationalisation (the motion filter) is explicitly the subject's. Lumping P5a with P3 rewrites the recorded provenance.

  2. **§8 reverses that routing silently.** §8 assigns `rest-stress-low-motion` to Beyond **P11** as a hybrid ("extends Wiggers C4b … the subject's motion filter she did not operationalise … Lives in Beyond because the tested tweak is the subject's"). Under the §2.1 membership test that is the *correct* answer — but it directly overturns the documented 2026-06-14 user-directed P5a→C4b routing, and §8 presents it as "§2.1 resolves them cleanly," not as a reversal. It also leaves unreconciled that **HA-C4b is a LOCKED pre-reg** whose Guide-ledger entry frames it as testing "the same Wiggers claim"; the MD would retag that locked test row `beyond:P11` without saying what happens to its Guide entry or whether a reciprocal ROUTED-back pointer is owed.

  Daza-layer provenance traceability (and the project's own ROUTED discipline, `hypothesis_lock_process.md` §3.8 register-row pointer rules) exists precisely so a future session can reconstruct *why* a thread sits where it sits. A rules-MD that both restates a prior routing inaccurately and reverses it without an audit trail defeats that. This is disclosure-and-reconcile before lock, not a reason the split collapses.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

Not applicable. The MD locks no inference, null model, window, effect size, or autocorrelation-sensitive procedure. Noted rather than passed silently, per the anti-pattern against demanding time-series machinery from a non-statistical MD.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3)

- **L4.6 (§3.6 named counts) — light-touch, no fire.** The MD cites counts (`rest-stress-low-motion` n=9 below the pre-set floor; P1 "d = +0.90") but as references to already-landed worked examples, not as new descriptive output; the n=9 is consistent with the site blurb ("the clean-rest sample fell to nine crashes, one short of the floor"). §3.6's triplet discipline binds descriptive outputs the MD *produces*, which this MD does not. No other §3 hook engages (no baseline, column-pair, crash-drop, or spike-metric choice is made here).

### Side observations

- **Side — §10 cross-reference inaccurate.** §10 cites "`docs/data-architecture.md` (`addendum-register.json` marked phase-2)." `data-architecture.md` in the site repo contains no mention of `addendum-register` (nor of "register" or "phase-2") at all; the `addendum-register.json` spec and its phasing live in `beyond-rewrite-plan.md` and `research-requests.md` (R36). Repoint the cross-ref.
- **Side — §8 roster uses not-yet-minted ids.** The "reconciled Beyond roster" assigns P8–P12, but `personal_hypotheses.md` currently stops at P7 (P8–P12 do not exist). This is correct as a *prescriptive* worked example (minting is §9-gated application work), but "The reconciled Beyond roster" reads as current state; a one-line "proposed, not yet minted — see §9" marker would prevent a future session mistaking §8 for the register's actual contents.
- **Side — confirms, does not fire.** `registry.md` currently carries zero `register:` fields, consistent with §3/§9 placing tagging in later work; the MD is correctly ahead of state, not contradicting it. The §4 claim that R36's summary lists the P-register as "P1, P2, P3, P6, P7" (dropping P4a/P4b/P5b) is **verified accurate** against `research-requests.md` R36 — a fair live example of the drift the section prevents.

---

## 3. What does not fire (selective)

- **I4 passes with corpus-specific substance.** §7 input 4 does not boilerplate n=1 — it ties the constraint to the research line's stated objective ("weather report, not an alarm"; the reader must be able to tell the subject's own poking-around from a test of Wiggers' published guide) and names the numbering discipline as the thing that serves it by preventing the conflation already observed (R36's dropped P-entries). That is the objective weighing in exactly where §2.2 expects it to for a lighter-bar structural MD.
- **I3 §6 structure is otherwise strong.** Four alternatives are named with corpus-specific (not boilerplate) rejection reasons: the scorecard-status split is rejected because the site's own guide rewrite demoted the scorecard as reproducing "the crash-prediction over-focus" (verified in `guide-rewrite-extraction-plan.md`); mint-site-only-ids is rejected on id-coherence grounds that align with Rule 2. The single I3 fire above is specifically the dual-axis row's premise, not the table's method.
- **The membership test §2.1 is internally coherent and defensible.** "Whose prediction, at whose operationalisation, the test evaluates" is a clean, single-axis rule, and the seed-vs-operationalisation distinction is the right cut. The Layer 2 fire is about *application consistency* with the recorded P5a routing, not about the rule itself.
- **Rule 6 (kind × stage derived from backend, never hand-set) is a genuine anti-drift design.** Deriving the export from backend state so "the export cannot then disagree with the ledger" is the reproducibility-hook spirit (cross-cutting B10) applied correctly to a projection.

---

## 4. What would strengthen this MD

1. **Reconcile the P5a/C4b provenance narrative before lock.** (a) Correct §2.2 to state P5a was routed on the *dominant-prior + same-shape + user-direction* grounds actually recorded, not as "Wiggers-native" (reserve that phrasing for P3, where it is accurate). (b) In §8, mark the `rest-stress-low-motion` → Beyond P11 assignment as an explicit **reversal** of the 2026-06-14 P5a→C4b routing, name the authority for the reversal (the §2.1 membership test + the shipped-site framing), and state the mechanics: does LOCKED HA-C4b's test row become `beyond:P11`, and does its Guide-ledger C4b entry gain a reciprocal ROUTED-back pointer per `hypothesis_lock_process.md` §3.8? *Inherits from* Layer 2 provenance traceability (Daza 2018) + the project's own register-row-pointer discipline. *Effect*: closes the highest-priority fire and makes the one genuinely contested placement auditable instead of asserted-clean.
2. **Repair the §6 dual-axis rejection to match §8.** Replace "a gap that no longer exists" with an acknowledgement that C4b is the one live case where backend and site *disagree* on authorship, and frame the single-axis choice as what *closes* it (backend moves to match site). *Inherits from* I3 tradeoff vision. *Effect*: the tradeoff argument stops resting on a premise its own worked example contradicts.
3. **Name a data-management state-of-art in §4 / §7 input 1.** Cite W3C PROV (provenance model), FAIR principle F1 (globally-unique persistent identifiers), and authority-control single-canonical-id-plus-crosswalk discipline; adopt or explicitly reject each for the `P#`/slug/crosswalk design. *Inherits from* I1.1. *Effect*: §4 reads as deliberate join-key discipline rather than an ad-hoc scheme, at the cost of two sentences.
4. **Re-ground or drop the Daza 2018 citation (§7 input 2); lean on CONVENTIONS §4.3.** §4.3 (which-prior-drove-it → the `register:` tag operationalises it) is the materially exact anchor; Daza's counterfactual framework does not bear on author-attribution. *Inherits from* I2.2. *Effect*: removes the one ornamental-leaning cite and strengthens input 2 by resting it on the anchor that actually fits.
5. **Fix the §10 `data-architecture.md` cross-ref and add a "proposed, not yet minted" marker to §8.** Point the addendum-register cross-ref at `beyond-rewrite-plan.md` / `research-requests.md` R36 where it is actually specced; flag P8–P12 in §8 as proposed. *Side.* *Effect*: keeps the cross-reference layer honest and prevents §8 being misread as current register state.

---

## 5. Verdict

**DEFENSIBLE with revision** — the single-authorship-axis split, the `register:` provenance tag, and the numbering/crosswalk discipline are sound and the §6 alternatives table is real work, but the P5a/C4b provenance narrative (§2.2 mischaracterising P5a as "Wiggers-native" and §8 silently reversing the documented user-directed P5a→C4b routing, unreconciled against the LOCKED HA-C4b) is a substantive Layer 2 fire that must be disclosed and reconciled before lock, and it is the same case that undercuts §6's "a gap that no longer exists" tradeoff claim (I3). Fold revisions 1–2 in and lock; 3–5 strengthen.

---

## Methodology

This methodology review walks CONVENTIONS §2.2 four-input bar plus the applicable items from the 4-layer checklist defined in [README.md](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

State-of-art specific to this methodology question (registry / id-coherence / provenance — a type not in the command's state-of-art pointer table): W3C PROV provenance model, FAIR principle F1 (persistent unique identifiers), authority-control / linked-data join-key discipline. Named in the I1 cell as the standard the §4 id machinery is measured against.

Project-specific audit hooks from [../CONVENTIONS.md](../CONVENTIONS.md) §2.2 (four-input bar), §2.1 / §3 / §4 (discipline gates + audit hooks that apply to methodology choices). Cross-referenced project artefacts read for consistency: `personal_hypotheses.md` (P1–P7, P3/P5a routing notes), `wiggers_testable_hypotheses.md` (C4b entry), `analyses/hypotheses/registry.md` (no `register:` field yet), `hypothesis_lock_process.md` (register-row-pointer discipline), and the `wiggers_research_story` site repo (`research-requests.md` R36, `data/addendum.json`, `guide-rewrite-extraction-plan.md`, `data-architecture.md`).
</content>
</invoke>
