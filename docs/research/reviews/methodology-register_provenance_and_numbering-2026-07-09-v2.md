# Methodology review (second-pass): Register provenance & numbering — the Guide/Beyond split and its id discipline (methodology/register_provenance_and_numbering.md)

**Target**: [../methodology/register_provenance_and_numbering.md](../methodology/register_provenance_and_numbering.md)
**Target commit**: working-tree state, untracked file (`??`) as of 2026-07-09; repo HEAD `13f8ee3`. Reviewed as the on-disk **DRAFT r2** (revised 2026-07-09 per §11).
**Reviewer mode**: Claude (independent methodology peer reviewer per CONVENTIONS §1.2; producer-mode MD under §2.2 four-input bar). *Fresh session, second-pass on r2; doc-only knowledge.*
**Review date**: 2026-07-09
**First-pass**: [methodology-register_provenance_and_numbering-2026-07-08.md](methodology-register_provenance_and_numbering-2026-07-08.md) (DRAFT r1, verdict DEFENSIBLE-with-revision). This pass verifies closure of that report's two lock-blockers (R1, R2) and two strengthening items (I1, I2), then re-walks the §2.2 four-input bar cold against r2 to catch anything the revisions introduced.

---

## 1. What the MD specifies

Unchanged in scope from r1: the MD locks a **structural (registry-organisation) choice, not a statistical one** — the Guide/Beyond split, a `register:` provenance tag on every `registry.md` test row, the `P#`/slug/crosswalk numbering discipline, and a backend-derived `kind × stage` status model for the R36 site export. What r2 changed is the *axis definition and one worked example*: the split axis is now stated as **authorship of the tested claim**, operationalised by the §2.1 membership test (*distinct theoretical claim* → Beyond vs *operational refinement of a Wiggers claim* → Guide), rather than the "authorship of the tested operationalisation" reading the r1 review had inferred. That re-specification is the spine of the R1 closure and it cascades into §2.2 (cross-attribution), §6 (the dual-axis tradeoff row), and §8 (the C4b worked example, which now stays in Guide instead of moving to Beyond P11). Framing remains producer-mode infrastructure under the lighter four-input bar (§7). Status is DRAFT r2, not locked; downstream artefacts that inherit the choice are unchanged (`personal_hypotheses.md`, `registry.md`, `STOCKTAKE §2a`, the site's `addendum-register.json`).

---

## 2. What fired and why

This is a second-pass, so Section 2 opens with the **closure verification** of the four items the r1 review raised, then reports the one fresh fire the re-specification introduced.

### Closure verification (r1 → r2)

**R1 — Layer 2 provenance (r1: substantive, highest-priority) — CLOSED, and closed better than recommended.** The r1 fire had two coupled parts: (a) §2.2 mischaracterised P5a as "Wiggers-native", and (b) §8 silently reversed the documented 2026-06-14 user-directed P5a→C4b routing by minting C4b as Beyond P11 against a LOCKED `HA-C4b`. r2 resolves both by re-specifying the axis rather than by disclosing a reversal:

- §2.1 (line 33) now anchors the membership test to the *distinct-claim-vs-operational-refinement* cut the subject actually applied on 2026-06-14, and correctly records P5a as the operational-refinement case that stays in Guide. This matches the source-of-truth routing note verbatim: `wiggers_testable_hypotheses.md` C4b entry (line 622) records "the motion filter is an operational refinement on the same shape, not a distinct theoretical claim", and `personal_hypotheses.md` P5a (line 333) records the same. The false "Wiggers-native" characterisation is gone.
- §2.1 (line 35) adds a **standing-routing-is-authoritative** clause: the rule governs new mintings and unrouted threads; a change to a standing routing is an explicit, disclosed user decision, never a side effect. This structurally forecloses the class of silent reversal that (b) was.
- §8 (lines 164, 167) keeps `rest-stress-low-motion` as `wiggers:C4b`, editorially surfaced on `/beyond` via the `provenance: guide-extension` tag, and states in as many words that this "corrects an r1 draft that reversed the 2026-06-14 routing" and that "`HA-C4b` is untouched". Because C4b is no longer re-routed, the r1 sub-concern — what happens to the LOCKED `HA-C4b` test row and whether a reciprocal ROUTED-back pointer is owed — dissolves rather than needing a separate reconciliation. This is the cleaner resolution: r1's own recommended fix (disclose the reversal) would have overturned a recorded user-directed routing, whereas r2's re-specification honours it.

**R2 — §6 tradeoff premise (r1: substantive, I3.3) — CLOSED.** r1 fired because §6's dual-axis rejection rested on "a gap that no longer exists", a premise the MD's own C4b worked example contradicted. r2 §6 (line 135) rewrites the row: it now names C4b as "the live counter-example" where "authorship (backend provenance) and editorial surfacing … do **not** coincide", keeps the single provenance axis, and routes the residual to the per-item `provenance: guide-extension` tag (§3). It explicitly retracts the earlier claim — "An earlier draft of this MD over-claimed that no gap exists; C4b is the live counter-example, and it is handled explicitly rather than denied." §6, §3 (lines 60, 66), and §8 (line 164) now agree on the C4b handling: Guide-by-provenance, surfaced on `/beyond`, kept honest by the per-item tag. The tradeoff no longer rests on a premise its own worked example refutes.

**I1 — data-management state-of-art (r1: minor, I1.1) — CLOSED.** r2 §7 input 1 (line 149) adds the named standards the §4 id machinery is measured against: FAIR principle **F1** (globally unique, persistent identifiers), **authority-control** (one authoritative id per entity, aliases cross-referenced), and **W3C PROV**-style explicit lineage, each mapped to a concrete §4 element (P# as the canonical id, the declared slug as join key, the crosswalk block as the alias record, the §2.2 cross-references as the lineage record). §4 now reads as deliberate join-key discipline rather than an ad-hoc scheme. Minor residual only: the anchors live in §7 rather than at §4 itself (Section 4, item 1).

**I2 — Daza demotion / §4.3 centring (r1: minor, I2.2) — CLOSED, exemplarily.** r2 §7 input 2 (line 150) drops the Daza citation entirely and states *why* keeping it would fail the bar: "No inference-methodology citation (Daza, Natesan) is invoked — this MD locks no inference choice, and citing them for a numbering convention would be ornamental." It centres CONVENTIONS §4.3 as the materially exact anchor (the `register:` tag *is* the durable record of which prior drove each thread). This is a model application of §2.2's "never cite a paper because they did it that way".

**Side items — CLOSED.** The §10 cross-reference now points at `beyond-rewrite-plan.md` / `research-requests.md` R36 (line 197) instead of the inaccurate `data-architecture.md`. The §8 illustrative-ids marker is added (line 169: "The `P8`–`P10` ids above are illustrative pending Phase-1 minting"), and the roster range correctly shrank from r1's P8–P12 to P8–P10 now that C4b is no longer minted as a P#.

### Spine — §2.2 four-input bar (fresh pass on r2)

#### I1 — Best-practices standards

No new fires; see closure above. The lighter structural bar is met on both halves now — SCRIBE 2016 / CENT 2015 for the provenance-transparency *why*, and FAIR-F1 / authority-control / PROV for the id-coherence *machinery*.

#### I2 — Established literature

No new fires; see closure above.

#### I3 — Tradeoff vision

No new fires; see R2 closure. §6's four-row alternatives table is intact and the dual-axis row's premise is now sound.

#### I4 — Research limitations + objectives

No fires. §7 input 4 (line 152) is unchanged from r1, where it already passed with corpus-specific substance (the honesty objective — "weather report, not an alarm" — depends on the reader telling the subject's own poking-around from a test of Wiggers' published guide, and the numbering discipline serves exactly that).

### Layer 1 — Discipline gates (inherits from CONVENTIONS §2.1, §4.1-§4.3)

No fires. The MD still locks a register organisation, bakes no imputed mechanism into a measurement (L1.2), and §5's two encoded disciplines remain explicitly anti-presuppositional (L1.3). The r2 axis re-specification is a definitional tightening, not a lift of any phenomenon from caveat to analytical basis.

### Layer 2 — Observational n=1 (inherits from Daza 2018)

- **L2.4 — the r2 re-specification introduces a mirror-image mischaracterisation on P3. Minor (residual, not blocking).** In closing R1, r2 §2.2 (line 41) states: "P3 and P5a are the two current `ROUTED to Wiggers` entries; the routing rationale in each is **the operational-refinement call**, **not** that the thread was 'Wiggers-native.'" That is accurate for P5a but **not for P3**. P3's own recorded routing note (`personal_hypotheses.md` line 215) gives a *different* rationale: "The lived-experience component is *retrospective felt-recognition* of the pattern Wiggers describes, not an active-monitoring prior. That's a Wiggers-test shape (literature prior + on-corpus test)." P3 contributes no operational refinement — no motion filter, no sensor tweak that sharpens her claim; it is routed to Guide because *the prior itself is Wiggers'* and the lived component is mere recognition. So r2 has flipped the r1 error rather than resolving its root: r1 lumped both threads as "Wiggers-native" (wrong for P5a); r2 lumps both as "operational-refinement" (wrong for P3). The accurate statement un-lumps them — P5a lands in Guide via operational-refinement, P3 lands in Guide via prior-is-Wiggers'/retrospective-recognition. This is the same provenance-traceability failure class as the original R1 fire (a rules-MD restating a recorded routing rationale inaccurately), which is why a second-pass exists to catch it; it is minor because P3 still lands in the correct ledger, the discrepancy is confined to one parenthetical, and nothing downstream cascades. Daza-layer traceability (L2.4) is the standard: a future session reading line 41 would reconstruct P3's provenance wrongly.

  **Coupled completeness gap (surfaced, not separately fired):** the mischaracterisation exists because §2.1's membership test, as written, only articulates the *refinement-vs-distinct-claim* branch. It has no branch for the pure "the prior/claim is Wiggers', the subject's lived experience is retrospective recognition, no refinement contributed" case that P3 represents — even though that case routes to Guide under the top-level §2 authorship axis. The test would be complete if it first asked "is the tested claim the subject's own or Wiggers'?" and only then, where the subject contributed, asked "refinement vs distinct claim." See Section 4, item 2.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

Not applicable. The MD locks no inference, null model, window, effect size, or autocorrelation-sensitive procedure. Noted rather than passed silently, per the anti-pattern against demanding time-series machinery from a non-statistical MD. Unchanged from r1.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3)

No fires. As in r1, no §3 hook engages — the MD makes no baseline, column-pair, crash-drop, or spike-metric choice, and produces no new descriptive output subject to §3.6's named-count triplet (its counts are references to already-landed worked examples).

### Side observations

- **Side — §8 C4b stage/count is stale against the current backend verdict.** §8 (line 164) records C4b as "`tested / inconclusive` (n=9, below the pre-set floor)". The Guide register now records `HA-C4b` **v3 LOCKED 2026-06-17, test-executed → NOT-SUPPORTED**, pooled **n=10** (8 train + 2 validate), 0 load-bearing (`wiggers_testable_hypotheses.md` line 383). Under §5's own stage model, a landed `result.md` with a NOT-SUPPORTED verdict is arguably `tested / done`, not `tested / inconclusive`; and the illustrative n differs (9 vs 10). This is illustrative worked-example content, not a load-bearing part of the methodology choice, so it does not fire — but a one-line refresh (or an explicit "as-of" date on the §8 roster) would keep the worked example from drifting against the register it is supposed to demonstrate.

---

## 3. What does not fire (selective)

- **The r2 axis re-specification is a genuine improvement, not merely a patch.** Re-framing the split as authorship *of the tested claim* (with operational refinement not transferring authorship) is a cleaner and more defensible cut than the "authorship of the operationalisation" reading, because it is the rule the subject already applied by hand and it keeps the standing C4b routing intact. The membership test §2.1 is internally coherent on the two-thread worked example (P5a → Guide, P5b → Beyond) and matches both source registers verbatim.
- **The standing-routing-is-authoritative clause (§2.1, line 35) is a structural upgrade.** It generalises the R1 fix beyond C4b: it prevents *any* future application of these conventions from silently overturning a recorded user-directed routing, which is exactly the provenance-audit-trail discipline `hypothesis_lock_process.md` §3.8 exists to protect. This is a stronger closure than fixing the one instance would have been.
- **R2's §6 retraction is done honestly.** §6 does not quietly delete the over-claim; it names it ("An earlier draft … over-claimed that no gap exists") and shows the handling. That preserves the audit trail of what the earlier draft asserted, consistent with the project's REJECTED-style visible-correction principle.
- **I2's closure is exemplary.** Dropping Daza *and stating why keeping it would be ornamental* is the §2.2 literature discipline applied to itself.

---

## 4. What would strengthen this MD

1. **Un-lump the P3 and P5a routing rationales in §2.2 (line 41).** Replace "the routing rationale in each is the operational-refinement call" with a two-clause statement: P5a is routed to Guide as an *operational refinement of C4* (the motion filter sharpens her claim), while P3 is routed to Guide because *the prior itself is Wiggers'* and the lived component is retrospective felt-recognition, not an active-monitoring protocol prior (per `personal_hypotheses.md` line 215). *Inherits from* Layer 2 provenance traceability (Daza 2018) + the project's ROUTED-record discipline. *Effect*: closes the one residual fire, and stops the second-pass from having merely flipped the r1 error onto a different thread. One-line fix; no structural change.

2. **Add the prior-authorship branch to the §2.1 membership test.** Front the test with the question the P3 case needs — "is the tested claim the subject's own, or Wiggers' (with the subject's lived experience being recognition of her pattern)?" — and only ask the refinement-vs-distinct-claim question where the subject contributed operational or theoretical content. *Inherits from* the §2 authorship axis (which already covers P3) and Layer 2. *Effect*: makes §2.1 complete against all three current ROUTED/Guide rationales (prior-is-Wiggers', operational-refinement, distinct-extension), so a future session routing a P3-shaped thread has an explicit branch to follow rather than forcing it through the refinement lens.

3. **Refresh or date-stamp the §8 C4b worked example.** Update the stage to match the current `HA-C4b` v3 NOT-SUPPORTED verdict (or add an "as-of 2026-07-09" note to the §8 roster). *Side.* *Effect*: keeps the worked example from contradicting the register it demonstrates; prevents a future reader taking `tested / inconclusive (n=9)` as current backend state.

4. **(Carry-over from r1, optional) Echo the FAIR-F1 / authority-control anchor at §4 itself.** §7 input 1 now names the standards, but §4 — where the machinery lives — still reads without them. A half-sentence in Rule 1 or Rule 2 ("P# as the single authoritative thread id, aliases cross-referenced in the crosswalk block, per authority-control discipline") would let a reader of §4 see the discipline in place. *Inherits from* I1.1. *Effect*: marginal; the closure is already real via §7.

---

## 5. Verdict

**DEFENSIBLE with revision** — all four r1 items (R1 Layer-2 provenance, R2 §6 tradeoff premise, I1 data-management state-of-art, I2 Daza demotion) are substantively and faithfully closed, the R1 closure via axis re-specification is cleaner than the r1 report's own recommended fix, and no new spine or Layer-1/3/4 fire appears; the single residual is a **minor Layer-2 traceability slip** where the R1 closure flipped the original "Wiggers-native" mischaracterisation onto P3 (§2.2 line 41 wrongly attributes P3's routing to "operational refinement" when its recorded rationale is retrospective felt-recognition of a Wiggers prior), which a one-line un-lumping (Section 4, items 1–2) fixes. Fold revision 1 in — and ideally 2 — then lock; 3–4 are polish.

---

## Methodology

This second-pass methodology review walks CONVENTIONS §2.2 four-input bar plus the applicable items from the 4-layer checklist defined in [README.md](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

State-of-art specific to this methodology question (registry / id-coherence / provenance — a type not in the command's state-of-art pointer table): W3C PROV provenance model, FAIR principle F1 (persistent unique identifiers), authority-control / linked-data join-key discipline. r2 now names these in §7 input 1 (an I1.1 closure verified this pass).

This being a second-pass, the review also cross-checked r2's closures against the source-of-truth records they cite: `personal_hypotheses.md` (P3 routing note line 215, P5a routing note line 333) and `wiggers_testable_hypotheses.md` (C4b entry lines 622, 383) confirmed the P5a operational-refinement characterisation and the standing routing, and surfaced the residual P3 discrepancy. First-pass report [methodology-register_provenance_and_numbering-2026-07-08.md](methodology-register_provenance_and_numbering-2026-07-08.md) supplied the R1/R2/I1/I2 items verified here.

Project-specific audit hooks from [../CONVENTIONS.md](../CONVENTIONS.md) §2.2 (four-input bar), §2.1 / §3 / §4 (discipline gates + audit hooks that apply to methodology choices).

---

## Note to the user (process observation)

The R1 closure is a case where the producer agent correctly *declined* the first reviewer's recommended fix (disclose the C4b → Beyond P11 reversal) in favour of a re-specification (keep C4b in Guide, correct the axis) that honours the recorded 2026-06-14 routing. That is the right call, and it is exactly the kind of substantive re-specification the project's "second fresh-session review before lock" discipline is designed to re-examine. The residual P3 slip found this pass is a reminder that the *root* of the R1 fire was a two-into-one lumping of distinct Guide-routing rationales; fixing the axis fixed P5a but left the lumping alive on P3. Worth a glance at whether any *other* register doc inherited the same "these threads are all Wiggers-native / all refinements" shorthand.
