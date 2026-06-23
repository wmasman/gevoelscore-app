# Review: HA-C4c — Substantive Wiggers C4 retest at bout-level resolution (HA-C4c) — r2 fresh-session re-audit

**Target**: [`docs/research/analyses/hypotheses/HA-C4c/hypothesis.md`](../analyses/hypotheses/HA-C4c/hypothesis.md)
**Target commit**: `310e145` (`research(HA-C4c): r2 substantive absorb -- column-confusion fix + section 4.9 framing + Holm disclosure`, 2026-06-23; working tree clean for the target file at the time of review).
**Reviewer mode**: Claude (Opus 4.7) — independent peer reviewer per [CONVENTIONS §1.2](../CONVENTIONS.md). Fresh session — no exposure to the r1 drafting context, the r1 audit drafting context, OR the r2 substantive-absorb drafting context; doc-only knowledge.
**Review date**: 2026-06-23.
**Re-audit scope**: this is the user-selected Option γ fresh-session re-audit of the r2 substantive absorb at `310e145`, against the prior r1 audit at [`HA-C4c-2026-06-23.md`](HA-C4c-2026-06-23.md) commit `5f79bd1`. Verdict-determining for whether r2 LOCKs (PASS / PASS-with-caveats with mechanical fires only) or routes to r3 (new blocking fire emerged).

## 1. What the data shows

This is still a pre-registration, not a result. The r2 absorb does not change the empirical claim: the doc still commits to a single-cell substantive Wiggers C4 retest at bout-level resolution on `bout_n_did_not_return_day` heavy-T-vs-non-heavy-T, with the §5 SUPPORTED/PARTIAL/REJECTED/INCONCLUSIVE bars (block-perm p<0.05 AND Cliff's δ≥+0.20). What r2 changed is the stratum-specification surface (now correctly anchored on the `citalopram_phase` axis with cross-axis cross-reference to `recovery_phase` per `lc_recovery_phase_axis §1.3` layering, with 4b/5 numbering), the §4.9 inheritance-by-analogue framing (underpowered-NULL leads; descriptive-companion + coefficient-of-convenience + inheritance-fragility framing absorbed), and the §5.3 Holm shrunk-family disclosure sentence (matching the HA-C4 v2 §5.5 r2 precedent). §5 falsification bars + §9 branching pre-spec + cascade caveats at §8 are unchanged. No methodology MD edits.

## 2. What fired and why

### Layer 1 — Universal reporting (inherits from SCRIBE 2016, STROBE 2007)

**No fires.** The r1 L1.2 BLOCKING column-confusion is closed cleanly. Verified at all 5 surfaces the r1 audit named (§1 line 60, §4.2 line 118, §6 line 267, §10.2 line 403, §3.8 gate table's supporting Authorship "Locked decisions" item 2 at line 21 + "Mandatory dispatches" single-cell headline lock at line 36) plus the 3 propagation surfaces the dispatcher flagged (§4.10 unmedicated-only arm at line 205, §8 caveat 10 at line 318, §9.4 INCONCLUSIVE options at line 367) and §10.2 Stage 2a at line 403 + Stage 2c at line 413. Each surface now (a) names the correct axis for the stratum (`citalopram_phase` for the primary, with `recovery_phase` cross-reference for the 4b+5 sub-phase layering), (b) uses canonical phase numbers (sub-phase 4b + phase 5, NOT 5 + 6), and (c) where the unmedicated-only stratum appears, frames it correctly as the `citalopram_phase == unmedicated` slice with explicit `recovery_phase == pacing_habit_established` cross-reference restricted to days before 2024-04-09 + after 2022-11-17 per the 4b left-edge. The §6 exclusion-rules bullet now uses the canonical 1/2/3/4a/4b/5 numbering per `lc_recovery_phase_axis §2` verbatim and explicitly says the 4a/4b sub-boundary at 2022-11-17 is the left edge of the stratum (NOT "phase 5 begins at 2022-11-17" as r1 had). Stratum is now unambiguously implementable by a `test.py` writer; the axis-confusion that would have left the verdict-running stratum undefined is fully resolved.

### Layer 2 — Observational n=1 (inherits from Daza 2018, Personal Science)

**No fires.** The L1.2 fix collapsed the §4.2 "~70 day-clusters" anticipated-power claim back into a clean cross-axis statement (line 118: "Pooling across the `unmedicated → buildup` boundary (equivalently the 4b → 5 boundary on the recovery axis) gains ~70 day-clusters of n"). L2.4 data provenance still passes; L2.6 prior motivation still passes.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

**No fires.** The r1 L3.3 minor Holm shrunk-family disclosure is closed at §5.3 (lines 254-258). The added sentence at line 258 explicitly names the form *"Holm (3-of-4 sens arms; motion-clean INCONCLUSIVE)"* + names the recomputed cutoffs (α/3, α/2, α/1) + names the inheritance from HA-C4 v2 §5.5 r2 fewer-comparisons absorb. Reporting-discipline closure is the same pattern the HA-C4 v2 r2 absorb established; no Layer-3 verdict surface is changed.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3, §4)

**No fires.** The r1 L4.7 substantive §4.9 framing slip is closed cleanly + the r2 absorber went BEYOND the audit's request in a structurally honest direction. Three specific verifications:

1. **§4.9 reordering — underpowered-NULL leads (line 183, paragraph 1).** The opening paragraph now begins *"Underpowered-NULL framing leads"* + restates the 0/7-CONFIRMED finding at this corpus's per-window n + names the 5-surface precedent at the recalibration audit (`reviews/bout_level_dose_response_calibration-r3-2026-06-22.md` §3) verbatim + frames the bout-level β recalibration's finding as the honest claim *"we cannot demonstrate per-bout dose-modulation at this n"* (NOT a definitive claim about citalopram's bout-level pharmacology or about dose-naivety). Approach A is explicitly RELEGATED to sensitivity arm in the opening paragraph; the sign-flip mechanics now follow as derivative-of-framing rather than leading-it.

2. **Inheritance-by-analogue as descriptive companion (lines 185-190).** The "coefficient-of-convenience" framing is now explicit at the derivation surface (line 188: *"use the analogue β as a coefficient-of-convenience, sign-flipped to match HA-C4c's +1 prior direction"*) + the fiat sign-flip is explicitly acknowledged as importing a +1 directional prior the recalibration never tested for this feature + named as honest only as a descriptive-companion device, NOT a CONFIRMED-direction claim. Lines 192-198 add a 4-bullet "Why this is a descriptive companion, not a load-bearing dose-correction" subsection that surfaces the chain explicitly (source β is NULL/weakly-consistent; analogue substitution adds uncertainty; underpowered-NULL cascades; CI-crosses-zero β would inject recalibration noise). This goes structurally BEYOND the r1 audit's recommended absorb (which only asked for the lead paragraph reordering) in a direction the audit endorses — the load-bearing framing is now present at the derivation surface inline, not only at §8 caveat 3.

3. **CI-bracket sub-arm renamed to inheritance-fragility (line 199).** The previous *"sensitivity-of-verdict-to-CI-bounds"* sub-arm name is preserved as the heading per the audit's request to surface this as fragility-not-precision-check, but the body of the paragraph now adds *"Per the underpowered-NULL frame, the analogue β's CI crosses zero, so this CI bracket is structurally a NULL-bracket: re-running primary on a NULL-bracket template is a descriptive companion to illustrate inheritance fragility, NOT a substantive precision check on a CONFIRMED β"* + names the surface-as-finding as *"β-precision-fragility finding"* with the explicit framing that *"the fragility is a property of the inheritance-by-analogue construction, NOT a substantive finding about dose-modulation on `bout_n_did_not_return_day`"*. This honours the L4.7 discipline the recalibration audit preserved at 5 surfaces.

L4.4 (crash-drop sensitivity) still passes; L4.6 (named counts) still passes; L4.2 (`_lagged_lcera`) still passes; L4.8 (prior-driven confirmatory) still passes.

### Side observations

- **Side**: Authorship `Status` line at 54 reads *"r2 drafted, not locked. Awaiting fresh-session re-audit per user-selected Option γ"* — matches the dispatcher's verdict-routing expectation. The LOCK signal is this re-audit's verdict.
- **Side**: Revision log at row 52 documents all three r1 fires + the absorb scope precisely + explicitly notes the §4.9 absorb went *"the inheritance-by-analogue is now explicitly framed as a **descriptive companion** using the analogue β as a coefficient-of-convenience, NOT a CONFIRMED dose-correction; the CI-bracket sub-arm is named as inheritance-fragility, NOT a substantive precision check"* — the absorb-beyond-handoff is transparently documented and traceable, not silent scope-creep.
- **Side**: The r2 absorb correctly retains the `recovery_phase` cross-reference everywhere the cross-axis layering matters (e.g. §4.2 line 118 *"equivalently `sub-phase 4b (pacing_habit_established) → phase 5 (citalopram_modulated)` on the `recovery_phase` axis"*), so the original drafter intent (primary stratum implicates both axes) is preserved without re-introducing the column-confusion fire.

## 3. What does not fire (selective)

- **L1.2 (column-confusion 5-surface propagation)** — passes cleanly. The 5 r1-named surfaces + 3 dispatcher-flagged propagation surfaces (§4.10, §8 caveat 10, §9.4) all use the correct axis + canonical phase numbers + cross-axis cross-reference where appropriate. No regression at any propagation site.
- **L4.7 framing (5-surface discipline preservation)** — passes with strong evidence. The §4.9 reorder + descriptive-companion framing + inheritance-fragility renaming all match the 5-surface precedent the recalibration audit (`reviews/bout_level_dose_response_calibration-r3-2026-06-22.md` §3) preserved on the underpowered-NULL frame. The r2 absorber surfaces the framing at BOTH §4.9 derivation AND §8 caveat 3 (the load-bearing surface); the previous structural vulnerability — where the headline-surface caveat 3 was clean but the derivation-surface §4.9 leaked — is closed.
- **L3.3 Holm shrunk-family disclosure** — passes. The added sentence at line 258 names the form, the cutoffs, and the inheritance precedent. Reporting-discipline only; does not change the §5.2 hard rule for primary verdict.
- **Authorship `Status` discipline + revision log** — passes with strong evidence. The r2 status reads correctly for the dispatcher routing; the revision log row at line 52 documents each absorb item against its r1 fire + the audit commit `5f79bd1` + the scope of the absorb-beyond-handoff transparently.
- **§5 falsification bars + §9 branching pre-spec preserved verbatim** — passes. Verified by reading §5 (lines 224-262) + §9 (lines 320-382): the (a)/(b) bars, verdict-precedence (INCONCLUSIVE → REJECTED → SUPPORTED → PARTIAL), single-cell headline lock, INCONCLUSIVE-aware pattern, and 5 branching sub-sections (9.1-9.5 + 9.6) all match the r1 spec. No drift past the absorb scope.
- **§3.8 lock-blocking gate table** — passes; Gate 4 status row correctly reads *"[pending audit + r2 + decision]"* awaiting this re-audit's verdict.

## 4. What would strengthen this finding

Per [CONVENTIONS §1.2](../CONVENTIONS.md): all suggestions are surfaced in this section, not silently absorbed.

1. **(Optional precision)** §4.7 walk-forward gate's *"Expected n per arm"* (line 166) still cites STOCKTAKE §6's "~70 day-clusters" gain figure rather than computing it inline from citalopram_modulated days × heavy-T fraction. This was the r1 audit's mechanical absorb item #4; not absorbed at r2 (correctly — the r1 audit explicitly named it as "mechanical r2 absorb opportunity if substantive" rather than a fire). At lock, either replicate the estimate inline OR cite the precise STOCKTAKE §6 row; the chain-of-inheritances at dry-run is one indirection deeper than it could be. **Expected effect**: reader can verify the §4.7 walk-forward gate evaluation at dry-run without re-deriving via STOCKTAKE chain.

2. **(Optional clarification)** §6 last bullet (line 272) is intact verbatim. The r1 audit's item #5 was an optional addition (closing the cross-phase-pooling-permission chain explicitly at §6). Not absorbed at r2. Acceptable; not a fire. **Expected effect**: marginal reader benefit; lock-blocking gate not affected.

Both items above are precision improvements, not gating items. The r2 absorb's structural soundness is sufficient for LOCK per the dispatcher's "PASS-with-caveats with mechanical fires only → LOCK per §3.6 pattern" routing rule.

## 5. Verdict

**PASS with caveats** — all three r1 fires (L1.2 BLOCKING column-confusion at 5 surfaces, L4.7 substantive §4.9 framing slip, L3.3 minor Holm shrunk-family disclosure) are closed cleanly with no new fires introduced from propagation. The r2 absorber went structurally BEYOND the audit's request on §4.9 in the audit-endorsed direction (descriptive-companion + coefficient-of-convenience + inheritance-fragility framing at the derivation surface, not only at the headline §8 caveat surface), preserving the L4.7 5-surface discipline the recalibration audit established. Strongest evidence for PASS: the propagation safety-check at 3 additional surfaces (§4.10 + §8 caveat 10 + §9.4) the dispatcher flagged all show clean axis-naming + canonical 4b/5 phase numbering. Caveats are the 2 mechanical opportunities at §4 above (precision improvements not gating LOCK).

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
