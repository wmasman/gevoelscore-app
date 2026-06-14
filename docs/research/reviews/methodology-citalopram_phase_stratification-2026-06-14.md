# Methodology review: Citalopram-phase stratification framework (methodology/citalopram_phase_stratification.md)

**Target**: [../methodology/citalopram_phase_stratification.md](../methodology/citalopram_phase_stratification.md)
**Target commit**: untracked working-tree file as of HEAD `7c81555`. The MD was drafted in this session at 2026-06-14 and has never been committed; reviewing the on-disk v1 draft.
**Reviewer mode**: Claude (independent methodology peer reviewer per CONVENTIONS §1.2; producer-mode framework MD under §2.2 four-input bar)
**Review date**: 2026-06-14

## 1. What the MD specifies

A **framework MD** that operationalises the downstream consequences of the v3-confirmed citalopram dose-response from [`citalopram_dose_response_stress_mean_sleep.md`](../methodology/citalopram_dose_response_stress_mean_sleep.md) §5.5-§5.6. The framework locks: (i) a canonical four-phase Citalopram-traject stratification axis (unmedicated / buildup / consolidation / afbouw / post-afbouw, with date boundaries from `annotations.yaml`); (ii) per-channel inheritance rules naming which of the parent MD §3 baseline channels (3 CONFIRMED, 1 weak, 1 partial, 1 REJECTED) require treatment; (iii) three downstream-test treatment patterns (§5.A per-phase stratification, §5.B dose-adjusted-predictor covariate-correction, §5.C joint dose-and-phase model); (iv) a pre-registration template for new hypothesis MDs; (v) a worked example on Personal-register P5b. The MD is **framework-mode, not test-mode** — it does not run a hypothesis test; it specifies the methodology that future hypothesis MDs in the Wiggers + Personal registers must adopt when their predictor or outcome touches a load-bearing CONFIRMED channel.

Downstream artefacts that already reference this framework (per the v3 doc-update cascade landed earlier this session): [`personal_hypotheses.md`](../personal_hypotheses.md) P4a caveat 5, P4b caveat 6, P5b caveat 6, P6 caveat 5, P7 caveat 4; [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) C4b caveats; [`garmin_pacing_practice.md` §7.4](../methodology/garmin_pacing_practice.md#74-intervention-period-baseline-calibration--resolved-2026-06-14-across-the-autonomic-load-family) (operational sibling).

## 2. What fired and why

### Spine — §2.2 four-input bar (inherits from CONVENTIONS §2.2)

#### I1 — Best-practices standards

- **[I1.1, L2.1, L3.5 — CONVENTIONS §2.2 input 1 + Daza 2018 counterfactual framework — substantive]** — **The state-of-art for §5.B's central technique (covariate adjustment for a measured confounder) is not explicitly named.** §5.B's "dose-adjusted predictor" *is* the textbook covariate-adjustment pattern from observational-causal-inference, anchored in the counterfactual framework (Pearl 2009; Rubin 1974; for self-tracked n-of-1 designs specifically, [Daza 2018 *Methods Inf Med*](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf), which is one of the project's six anchor standards). The MD describes the technique correctly but does not anchor it to the standard literature. A reader expecting the §2.2 input-1 bar to be cleared will hit a gap: the framework's central methodological move is presented as a project-internal innovation rather than as the standard observational-causal-inference move that it is. **Fix is one paragraph in §5.B**: name the covariate-adjustment / counterfactual-framework anchor with the Daza 2018 citation, and one sentence on what Daza 2018 materially contributes (counterfactual framework specifically adapted for time-varying confounders in n-of-1 self-tracking — exactly this situation).
- **[I1.2 — minor]** — §5.C (joint dose-and-phase model) is essentially a "belt-and-braces" two-covariate regression — a standard practice that doesn't need its own state-of-art citation per se, but the MD could acknowledge it as "standard multi-variable regression with both adjustment terms" rather than a project-specific innovation.

#### I2 — Established literature

- **[I2.4 — minor, cross-references I1.1]** — Daza 2018 should be cited as the counterfactual-framework anchor in §1.3 (inheritance bar) AND in §5.B (the technique location). Local PDF at [`literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf`](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf). Closes the I1.1 audit-trail.
- **[I2.3 — partial, already noted in the MD]** — Pharmacological grounding for the per-channel β values (Licht 2010, Kemp 2010, Wichniak 2017) is correctly **queued, not retrieved**, per §1.3. The MD acknowledges this explicitly. Not a fire; just a continuity reminder.

#### I3 — Tradeoff vision

- **[I3.4 — minor]** — **Implicit tradeoff: choosing the buildup β over the afbouw β for §5.B's offset.** §5.B prescribes "use the post-CPAP buildup β since it has tighter CIs". This is reasonable but the prescription has an *implicit* tradeoff with the §8.4-noted buildup-vs-afbouw asymmetry: the buildup β was estimated on a dose-naive system, which may *overcorrect* downstream channels in the consolidation or afbouw phases where the system has adapted. The MD acknowledges the asymmetry in §8.4 (and notes the user has flagged the asymmetry investigation as out-of-scope per session memory), but the §5.B prescription doesn't explicitly weigh "tight CI vs potential dose-state-mismatch". **Fix is one sentence in §5.B**: note that using the buildup β is conservative-against-undercorrection but may overcorrect at steady-state; an alternative for steady-state-window tests is to use the afbouw β. The user-pinned scope (asymmetry investigation deferred) means this is a methodological flag for the consumer of the framework, not an action item for the framework itself.

#### I4 — Research limitations + objectives

- **No blocking fires.** §1.3 explicitly names n=1, observational design, and decision-gating objective. §3 corpus-specific phase boundaries are corpus-anchored. §4 per-channel verdicts are corpus-empirical.

### Layer 1 — Discipline gates (inherits from CONVENTIONS §2.1, §4.1-§4.3)

- **No fires.** §2.1 descriptive-before-inference: the framework is downstream of the v3-confirmed findings; descriptive layer fully cleared. §4.1 no interpretive marks: "dose-modulated" is empirically grounded; mechanism is queued not asserted. §4.2 caveats vs a-priori: the four phases are factual (calendar events from annotations.yaml), not pre-segmented based on data-peeking. §4.3 confirmatory framing: inherited from the dose-response MD.

### Layer 2 — Observational n=1 (inherits from Daza 2018)

- **[L2.1 — substantive, cross-references I1.1]** — Daza 2018 counterfactual framework is the standard anchor for n-of-1 observational covariate adjustment, and §5.B's technique is exactly that. Citation missing. Same fix as I1.1.
- **No other fires.** L2.2 stationarity: explicit core concern of the framework (non-stationarity across phases is what motivated the framework). L2.3 calendar-time framing: explicit. L2.4 data provenance: annotations.yaml + dose_response.py script cited.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

- **[L3.1 + B5 — autocorrelation reminder — minor]** — The framework provides treatment for confounder adjustment but does NOT explicitly remind the downstream-test consumer to ALSO handle autocorrelation in their final inference (HAC SE / block bootstrap / effective N — the Natesan Batley 2023 failure mode). A new hypothesis author adopting the framework could correctly apply §5.B's covariate adjustment AND then use plain OLS SE, missing the autocorrelation correction. **Fix is one sentence in §6 (pre-registration template)**: note that adopting the framework does NOT relieve the test of autocorrelation-handling per CONVENTIONS §3 / Natesan Batley 2023 — the dose-adjustment and the autocorrelation correction are independent obligations.
- **[L3.5 — cross-references I1.1]** — State-of-art naming for covariate adjustment is the I1.1 fire.
- **No other fires.** L3.2 lag/carryover: PK-smoothing handles via 35h half-life. L3.3 multiplicity: §5's three treatments are robustness arms, not separate hypotheses. L3.4 level vs trend: both handled.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3)

- **[L4.4 — minor, cross-references B5]** — CONVENTIONS §3.4 crash-drop sensitivity is a binding audit hook for any Layer 4+ regression on PEM-pacing channels. Downstream tests adopting this framework inherit the §3.4 obligation independently, but the framework could explicitly forward-reference. **Fix is one sentence in §6**: remind consumers that the framework does not absolve the test of §3.4 crash-drop sensitivity (or §3.5 spike-metric preference, where applicable) — the framework adds dose-adjustment ON TOP OF the existing audit-hook obligations, it does not replace them.
- **No other fires.** L4.1 personal baseline: §5.B IS personal-baseline correction (per-mg offset). L4.2 §3.2 lagged-lcera: explicitly addressed in §9 audit-hooks-engaged. L4.6 named counts: §3 cites days-per-phase counts with annotations.yaml as source.

### Methodology-specific Type A — A1 (Phase boundary / regime segmentation MD)

The framework is partially an A1 MD (defines four canonical Citalopram-phases) and partially an A4 MD (specifies the dose-adjusted predictor operationalisation). Walking A1:

- **[A1.2 — substantive]** — **Change-point detection (PELT [Killick et al. 2012], Bayesian online [Adams & MacKay 2007]) not named-and-rejected.** The convention for phase-boundary MDs is to name the algorithmic alternative and explicitly reject it with reason. The four Citalopram phases are pre-specified from documented clinical dose changes (annotations.yaml), which is a strong A1.1 anchor — but A1.2 specifically requires naming the algorithmic alternative even when it isn't used. **Fix is one sentence in §3**: "Change-point detection (PELT, BCP) is not used to derive these boundaries because the dates are anchored to documented clinical dose-change events from `annotations.yaml`; an algorithmic change-point sweep could corroborate the dates but not change them. The empirical confirmation of phase-effect (per the dose-response MD's §5.5/§5.6) IS the post-hoc validation that the pre-specified boundaries correspond to real distributional shifts."
- **[A1.4 — minor]** — Sensitivity to ±N days around boundary not explicitly spec'd as an option. The PK-smoothed dose function inherently softens the boundaries (5-7 day equilibration per 35h t_half), so the ±N-day question is partly built in. But for §5.A per-phase stratification specifically, the consumer could legitimately ask "should I exclude the first 14 days of each new phase to let plasma equilibrate?". **Fix is one sentence in §5.A**: note that for per-phase stratification, an optional ±N-day boundary buffer can be applied; the PK-smoothing of §5.B makes this irrelevant for §5.B.
- A1.1, A1.3, A1.5 pass: A1.1 each boundary date traceable to annotations.yaml; A1.3 boundary effect on downstream analyses explicitly traced (§4 verdict table + §10 downstream consumers list); A1.5 transition / washout windows justified by the 35h citalopram half-life from the SPC.

### Methodology-specific Type A — A4 (Operationalisation MD)

§5.B's dose-adjusted predictor is an A4-type operationalisation. Walking:

- **[A4.5 — minor]** — **NaN policy for `dose_plasma_mg` not explicitly stated for pre-2024-04-09 dates.** §3's `citalopram_phase(d)` function returns "unmedicated" for `d < 2024-04-09`, and the PK convolution returns 0 for those dates (initial dose is 0 before the buildup). But the framework should explicitly state this so consumers don't accidentally NaN-propagate or treat pre-citalopram dates as missing. **Fix is one sentence in §3 or §5.B**: `dose_plasma_mg(d) = 0` for `d < 2024-04-09`; the dose-adjusted predictor on unmedicated dates reduces to the raw channel value.
- A4.1, A4.2, A4.3, A4.4, A4.6 pass: PK window length + reference window stated (§2.3 of the dose-response MD); personal baseline (PK is participant-prescription-specific); §3.2 lagged-lcera variant family addressed; carryover handled via PK-smoothing; sensitivity via the three §5 treatments.

### Methodology-specific Type B — Cross-cutting

- **[B5 — minor, cross-references L3.1]** — Autocorrelation reminder in §6 template (same fix as L3.1).
- **No other fires.** B1 pre-spec (the framework's §5 IS the pre-spec for downstream consumers). B2 sensitivity sweep (§5 three treatments). B3 confounder enumeration (corpus-specific, citalopram-anchored). B4 stationarity (the framework's whole purpose). B6 multiplicity (robustness arms, not separate hypotheses). B7 effect size + CI (per-channel β values with CIs from the dose-response MD's §5.6.1). B8 visual + statistical (framework MD — not applicable). B9 causal vs correlational (caveat-mode framing). B10 reproducibility (script paths cited, formulas given).

### Side observations

- **Side** — **The framework's §4 table treats `stress_mean_sleep_lagged_lcera` (and similar) as load-bearing input channels, but these are NOT yet in `per_day_master.csv`** (per the pipeline-patch queue noted in the dose-response MD §7 status). Currently the lagged-lcera computation is on-the-fly in `dose_response.py`. The framework should acknowledge that adopting §5.B in a hypothesis MD today requires the consumer to ALSO compute the lagged-lcera variant in-script (or wait for the pipeline patch). One-sentence temporal-state note in §5.B or §6.
- **Side** — **§7 worked P5b example gives the formula but no numerical example.** A reader trying to internalise "what does dose-adjustment actually do to a specific day's data" would benefit from a single worked numerical example: "On 2025-08-15 (consolidation phase), raw `stress_mean_sleep` = 18.3; PK-smoothed plasma = 30mg; β = +0.43; adjusted value = 18.3 - 0.43 × 30 = 5.4". One small numerical walkthrough closes the conceptual gap.
- **Side** — **§3's `citalopram_phase(d)` Python function is hardcoded** with the four phase dates. Per the project's general approach (annotations.yaml-driven, not hardcoded), the function should derive the dates from annotations.yaml at runtime instead of hardcoding them. The hardcoded form is appropriate for a methodology MD spec (the dates ARE locked here as constants), but a worked production version should load from yaml. Minor; the MD could note this distinction.

## 3. What does not fire (selective)

Non-trivial passes worth naming:

- **The three-treatment-pattern structure (§5.A / §5.B / §5.C) is exemplary methodology-framework design**: each treatment is named with pros / cons / when-to-use criteria; the consumer has a defensible choice rather than a single take-it-or-leave-it prescription. This matches the pattern of high-quality methodology MDs in the literature (CENT 2015 § for n-of-1 design choices; STROBE 2007 § for analysis choices). The framework gives downstream hypothesis authors agency *and* discipline simultaneously.
- **§6 pre-registration template is the right discipline-tool**: it makes the §4 audit hook (downstream MDs MUST adopt one of the three treatments) machine-checkable. A reviewer of a future hypothesis MD can grep for the template's structure and instantly see whether the framework is engaged. This is the kind of operationalised methodology guidance that prevents drift.
- **§7 worked P5b example is correctly anchored**: P5b is the test case where the per-v3-reading is most consequential (both stress channels confirmed; cross-phase pooling is the default for the rest-stress trigger predictor). Using P5b as the worked example is the right choice — it tests the framework against its hardest case.
- **§4 verdict table correctly distinguishes load-bearing CONFIRMED from weak / partial / REJECTED**: the framework only requires treatment for the three load-bearing channels; the others are correctly given lighter or no obligations. This proportionality is methodology-design hygiene — the framework doesn't over-demand or over-promise.
- **§9 audit-hooks-engaged section is comprehensive** (4 hooks listed) and §10 cross-references trace forward to 5 downstream consumer files. The framework's place in the project's MD network is explicit.

## 4. What would strengthen this MD

Prioritised by impact-per-fix:

1. **Cite Daza 2018 in §1.3 + §5.B as the counterfactual / covariate-adjustment anchor.** One sentence + parenthetical citation in each location. Daza 2018 is one of the project's six anchor standards (the n-of-1-specific counterfactual framework), and §5.B's central technique IS Daza's adapted-for-self-tracking covariate adjustment. Closes the I1.1 / L2.1 / I2.4 fires in one move. Expected effect: framework is recognisable as a state-of-art adoption rather than a project-internal invention; downstream reviewers can audit-trace.

2. **Add change-point-detection rejection paragraph in §3.** One paragraph naming PELT (Killick et al. 2012) + Bayesian online change-point (Adams & MacKay 2007) and explicitly rejecting with reason ("dates anchored to documented clinical events; algorithmic CPD would corroborate but not change"). Closes A1.2. Inherits from the state-of-art pointer table in `/research-methodology-review` for "Phase / regime boundary detection in time series".

3. **Add autocorrelation + crash-drop reminder in §6 pre-registration template.** Two sentences: "Adopting this framework does not relieve downstream tests of autocorrelation handling per CONVENTIONS §3 / Natesan Batley 2023 (HAC SE, block bootstrap, or explicit acknowledgment) NOR of crash-drop sensitivity per CONVENTIONS §3.4 (and §3.5 spike-metric preference where applicable). The framework adds dose-adjustment ON TOP OF these obligations; it does not replace them." Closes L3.1, L4.4, B5 in one paragraph.

4. **Add buildup-β-vs-afbouw-β tradeoff sentence in §5.B.** One sentence acknowledging the implicit choice and pointing at §8.4: "§5.B prescribes the buildup β as the default; for steady-state-window tests the afbouw β may be more representative. The buildup-vs-afbouw asymmetry is documented in §8.4 and is explicitly out-of-scope for further investigation per the project's core mission focus." Closes I3.4.

5. **Add NaN policy + dose-plasma=0 specification in §3 or §5.B.** One sentence: "`dose_plasma_mg(d) = 0` for `d < 2024-04-09`; the dose-adjusted predictor on unmedicated dates reduces to the raw channel value." Closes A4.5.

6. **Add a numerical worked example in §7.** One concrete example like: "On 2025-08-15 (consolidation phase, 30mg plateau), raw `stress_mean_sleep` = 18.3 and PK-smoothed plasma = 30mg; the dose-adjusted value under §5.B is 18.3 - 0.43 × 30 = 5.4. This is the value the rolling-baseline machinery sees for that day." Helps reader internalise the technique. Side observation; not a fire.

7. **Add the temporal-state note about lagged-lcera column availability in §5.B.** One sentence: "Adopting §5.B today requires the consumer to also compute the lagged-lcera variant in-script for the affected channels (per `dose_response.py` pattern), since `stress_mean_sleep_lagged_lcera` and siblings are not yet in `per_day_master.csv`; the pipeline patch to add these columns is queued (per the dose-response MD §7 status)." Side observation; transparency.

None of these items are blocking. All can be folded in opportunistically; the framework is usable as-is, and the existing downstream-consumer caveats already in P4a/P4b/P5b/P6/P7 + C4b are not invalidated by the gaps above.

## 5. Verdict

**DEFENSIBLE with revision** — the framework specifies a sound and proportional set of treatment patterns (§5.A per-phase stratification, §5.B dose-adjusted predictor, §5.C joint model) that downstream hypothesis MDs can adopt with confidence, with the empirical anchor (v3 dose-response findings) tightly cited; the substantive gap is that §5.B's covariate-adjustment technique is presented as a project-internal innovation when it is actually the standard Daza-2018-style n-of-1 counterfactual adjustment (I1.1 / L2.1 fire). Folding in the Daza 2018 citation, the PELT/BCP rejection paragraph, and the autocorrelation/crash-drop reminder in §6 closes the substantive fires; the remaining items are minor / clarity-of-presentation improvements.

The framework is ready to be cited by downstream hypothesis MDs as-is for the v3 doc-update cascade already landed (P4a/P4b/P5b/P6/P7 + C4b). The Section-4 revisions can fold in opportunistically without invalidating those references.

---

## Methodology

This methodology review walks CONVENTIONS §2.2 four-input bar plus the applicable items from the 4-layer checklist defined in [README.md](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

Plus the state-of-art literature specific to this methodology question:

- **Observational confounding in n-of-1 self-tracking**: Daza 2018 counterfactual framework. §5.B's central technique is exactly the time-varying-confounder covariate-adjustment pattern from Daza 2018; citation needed (I1.1 / L2.1 fire).
- **Phase / regime boundary detection in time series**: PELT (Killick, Fearnhead, Eckley 2012 *JASA*); Bayesian online (Adams & MacKay 2007 *arXiv*); `ruptures` library. The dates here are pre-specified from annotations.yaml; algorithmic CPD should be named and rejected per A1.2 (substantive fire).
- **Drug-effect transition windows**: citalopram t_half = 35h (SPC, EMA). Inherited correctly from the dose-response MD §2.3 anchor; no new fire.

Project-specific audit hooks from [CONVENTIONS.md](../CONVENTIONS.md) §2.2 (four-input bar), §2.1 / §3 / §4 (discipline gates + audit hooks). The framework's §9 audit-hooks-engaged section already lists 4 hooks (§2.1, §2.2, §3.2, §3.7); adding the autocorrelation + crash-drop reminders per Section 4 fix #3 would extend this to cover the §3.1 / §3.4 / §3.5 / §3.6 obligations the framework inherits downstream.
