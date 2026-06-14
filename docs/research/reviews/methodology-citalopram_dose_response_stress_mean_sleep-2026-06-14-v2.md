# Methodology review: Citalopram dose-response on stress_mean_sleep (methodology/citalopram_dose_response_stress_mean_sleep.md) — v2

**Target**: [../methodology/citalopram_dose_response_stress_mean_sleep.md](../methodology/citalopram_dose_response_stress_mean_sleep.md)
**Target commit**: untracked working-tree file as of HEAD `7c81555`. The MD has never been committed; reviewing the v2 on-disk draft as revised 2026-06-14 in response to the v1 review at [`methodology-citalopram_dose_response_stress_mean_sleep-2026-06-14.md`](methodology-citalopram_dose_response_stress_mean_sleep-2026-06-14.md). The §7 revision log in the target MD documents the v1 → v2 fix-by-fix landing map for all 13 v1-review recommendations.
**Reviewer mode**: Claude (independent methodology peer reviewer per CONVENTIONS §1.2; producer-mode MD under §2.2 four-input bar)
**Review date**: 2026-06-14 (v2; same-day re-review per skill Phase 4 convention)

## 1. What the MD specifies

Unchanged from v1 in substance: a confirmatory methodology MD locking the analytical specification for a single narrow follow-up question (does `stress_mean_sleep` respond to the citalopram afbouw in a graded, dose-dependent way) descended from [`intervention_effects_descriptive.md`](../methodology/intervention_effects_descriptive.md) §8. Linear regression of `stress_mean_sleep` on PK-smoothed plasma dose proxy + linear `days_from_afbouw_start` covariate; Newey-West HAC primary SE with Andrews 1991 lag selection; sensitivity columns A-F now (block bootstrap, prescribed-step, lagged-lcera, alternative HAC lag, crash-drop, nonlinear time); 4-condition all-must-hold null pre-spec; confirmatory framing per §4.3 with three independent priors.

**Substantive revision vs v1**: all 13 v1-review recommendations folded in per §7 revision log. The locked choices (linear-in-dose, PK-smoothed primary exposure, Newey-West HAC, raw outcome primary, 4-condition null pre-spec) are unchanged; the v2 changes are uniformly **additive**: state-of-art naming for the PK/PD framework (§2.3); journal-cited literature for ITS rejection (§4.6), block bootstrap (§4.3-A), HAC SE (§4.2); seasonality + Breinvoeding + device-stability + life-events enumeration in §1.3; two new sensitivity columns E (crash-drop per §3.4 binding audit hook) and F (nonlinear time, seasonality robustness); CONVENTIONS §3.5 spike-vs-mean acknowledgment in §3.1; queued-literature-prior status acknowledged in §1.4; one-sided test explicitly defended as tradeoff in §4.1; lag-1 ρ + effective-N pre-spec'd in §6.3 outputs; bootstrap seed pinned; analytical-window endpoint precisified; monotonicity-scatter dose-binning made explicit; `initial_dose_decay_term` defined. Audit-hooks-engaged section in §7 expanded from 6 hooks (v1) to 8 hooks (v2).

Downstream artefacts unchanged from v1: every PEM-pacing hypothesis using `stress_mean_sleep_lagged_lcera` across the 2026-03-20 → 2026-06-05 frame (P4a, P4b, P5b); the open question in [`garmin_pacing_practice.md`](../methodology/garmin_pacing_practice.md) §7.4; the parent MD §8.4 follow-up bullet.

## 2. What fired and why

### Spine — §2.2 four-input bar (inherits from CONVENTIONS §2.2)

#### I1 — Best-practices standards

- **No fires.** v1 fires CLOSED:
  - **I1.1 (PK/PD as state-of-art framework not named) — CLOSED.** §2.3 now opens with an explicit "State-of-art framework" paragraph naming "one-compartment first-order absorption-elimination pharmacokinetic / pharmacodynamic (PK/PD) model" with anchor citations (Rowland & Tozer 2011 *Clinical Pharmacokinetics and Pharmacodynamics* 4th ed. chapter 4; Gabrielsson & Weiner 2016 *Pharmacokinetic and Pharmacodynamic Data Analysis*). The state-of-art-named-then-adopted pattern matches the worked-example bar.
  - **I1.4 (ITS rejection reason was question-type-based, not corpus-constraint-based) — CLOSED.** §4.6 now sharpens to a mechanism-based rejection: *"A multi-boundary ITS would estimate 6 step-level parameters (β2/β3 at each of the 3 step-dates) where the mechanism predicts a single per-mg slope; collapsing those 6 parameters into 1 by the dose-regression parameterisation is the methodological choice here, with the dose-response framing as the rationale."* This is corpus-and-mechanism-aware reasoning, not pure question-type taxonomy.

#### I2 — Established literature

- **No blocking fires.** v1 fires CLOSED with concrete journal references:
  - **I2.2 (Bernal 2017, Künsch 1989, Politis & Romano 1994, Newey & West 1987, Andrews 1991 uncited) — CLOSED.** All five citations added with full journal references:
    - Bernal Cummins Gasparrini 2017, *International Journal of Epidemiology* 46(1):348-355 in §4.6 with material contribution stated (level-change β2 + post-intervention trend-change β3 decomposition, which the dose-regression subsumes).
    - Künsch 1989, *Annals of Statistics* 17(3):1217-1241 in §4.3-A with local PDF link to [`literature/methodology/kunsch_1989_jackknife_bootstrap_stationary.pdf`](../literature/methodology/kunsch_1989_jackknife_bootstrap_stationary.pdf).
    - Politis & Romano 1994, *JASA* 89(428):1303-1313 as the stationary-bootstrap variant fallback.
    - Newey & West 1987, *Econometrica* 55(3):703-708 in §4.2 as the canonical HAC estimator.
    - Andrews 1991, *Econometrica* 59(3):817-858 in §4.2 as the data-dependent lag-selection rule.
    Each citation includes a sentence on its material contribution rather than ornamental name-drop.
  - **I2.3 (literature prior queued, fragile for confirmatory framing) — CLOSED with explicit acknowledgment.** §1.4 now has a dedicated "Audit-trail note on the queued-literature-prior status" paragraph that names which two priors (lived-experience, mechanism) are independently sufficient under §4.3's "any one is yes" rule and explicitly states the queued literature prior would tighten but not change the framing.
- **[I2.4 — minor, partly residual from v1]** — The "0.05 × SD per mg" effect-size threshold in §4.4 is dimensionally a standardised regression coefficient (SD-normalised slope), and the v1 review flagged this against the WWC 2022 SCED Handbook §V menu (Cohen's d, Hedges' g, Tau-U, NAP, IRD). On v2 re-read, the SCED menu is designed for *group / phase comparison*, not for *regression coefficients on continuous exposure*, so direct anchoring would be category-mismatched. The SD-normalised β IS effect-size + CI per Natesan Batley 2023's distributional-assumption requirement (the v1 fire's underlying concern). **Re-classified as a minor v1-residual that is actually defensible on v2 re-read**; no v2 fire. One sentence in §4.4 acknowledging the SCED menu doesn't apply directly to regression coefficients would close the audit trail (see Section 4 recommendation 1).

#### I3 — Tradeoff vision

- **No fires.** v1 fires CLOSED:
  - **I3.4 (one-sided test choice not defended as tradeoff) — CLOSED.** §4.1 now has a dedicated "Tradeoff on one-sided vs two-sided test" paragraph naming both alternatives, the power-vs-conservatism asymmetry, the §1.4 priors-commit-direction as methodological premise, and the explicit recourse path: *"if a reviewer rejects the §1.4 direction-commitment, the analysis should be re-spec'd to two-sided rather than mid-stream."* This is exactly the "methodological premise vs free analytical choice" framing the I3.4 fire was asking for.
  - **I3.3 (linear-in-dose vs log-dose distinguishability) — minor v1 residual, unchanged in v2.** §4.1 still says "the regression cannot reliably distinguish linear-in-dose from log-dose anyway (the two are co-linear over the relevant range)". This is correct but slightly understated; one sentence to clarify "they are co-linear for the smooth-monotonic-decline range of dose values in this corpus" would tighten it. **Minor; not blocking.**

#### I4 — Research limitations + objectives

- **No fires.** v1 was already clean here; v2 added the §3.2 "Analytical n" specification ("expected count is ~71 minus any incidental missing days") which makes the n=1-on-~70-day-window precision explicit, and §3.2 + §6.2 codify `analytical_end = 2026-05-29` vs nominal `afbouw_end = 2026-06-05` (the v1-review §13a fire).

### Layer 1 — Discipline gates (inherits from CONVENTIONS §2.1, §4.1-§4.3)

- **No fires.** v1 fires CLOSED:
  - **L1.4 (confirmatory framing's queued-literature-prior status) — CLOSED.** §1.4 audit-trail note covers it.
- **Caveat-vs-a-priori discipline holds in the v2 additions**: the §1.3 seasonality bullet is correctly caveat-class ("All co-vary with calendar time and therefore partially with the dose function" — acknowledges confound, doesn't pre-segment); the §4.3 Sensitivity F is the test against the caveat, not pre-spec of a phase. The Sensitivity E "Expected impact" paragraph ("~0.4 expected crashes ... likely to be near-identical to the primary") is a calibration expectation, not a hypothesis presupposition.

### Layer 2 — Observational n=1 (inherits from Daza 2018)

- **[L2.1 — minor v1 residual]** — Daza 2018 counterfactual framework still not explicitly cited. The §1.3 substantive confound paragraph IS counterfactual reasoning (what would have happened absent the dose change; the linear time covariate is the model's answer), but the Daza 2018 anchor citation isn't named. **Minor audit-trail; not blocking.** One sentence in §1.3 or §1.4 would close it.
- L2.2-L2.4 pass cleanly (stationarity acknowledged; calendar-time framing clear; data provenance traceable per §6.2).

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

- **No fires.** v1 fires CLOSED:
  - **L3.1 + B5 (effective N + lag-1 ρ not pre-spec'd) — CLOSED.** §6.3 outputs now include `lag1_residual_rho` and `effective_n_under_hac` (Bartlett-window-derived) with explicit purpose statement: "lets the reader judge whether `HAC_maxlags = 4` is doing meaningful work given the observed residual autocorrelation."
  - **L3.5 (PK/PD as state-of-art for exposure model not explicitly named) — CLOSED** via I1.1 closure.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3)

- **No fires.** v1 fires CLOSED:
  - **L4.4 (CONVENTIONS §3.4 crash-drop sensitivity not pre-spec'd) — CLOSED**, the highest-priority v1 fire. Sensitivity Column E now in §4.3, with:
    - The full §3.4 rule quoted in-line for audit transparency.
    - An "Expected impact" paragraph quantifying the prior (~0.4 expected crash-days in the 77-day late-LC window) so the reader knows what null-effect-here means.
    - A §3.6-formatted named count in §6.3 outputs (`"0 crash-days (crash_v2 day-level, per_day_master.csv, is_crash == True, 2026-03-20 <= date <= 2026-06-05)"`).
    The binding audit hook is now fully engaged.
  - **L4.5 (§3.5 spike-vs-mean preference) — CLOSED.** §3.1 acknowledges with inherited-from-parent justification and queues spike-metric corroboration as future work without changing the script.

### Methodology-specific elements — Type A.7 (Intervention-effect MD)

- **A7.1 PASSES**: cross-references I1.4 closure (ITS named + sharp-rejection-reason in §4.6 with Bernal 2017 citation).
- **A7.2 CLOSED**: PK literature now cited (Rowland & Tozer 2011, Gabrielsson & Weiner 2016 for framework; citalopram SPC EMA + Hyttel 1994 for SSRI-class pharmacology).
- **A7.3a (other concurrent interventions) — CLOSED.** §1.3 acknowledges Breinvoeding-interventie 2026-03-10 → 2026-08-31 as the unmodeled concurrent intervention spanning the entire afbouw window; effect plausibly small but acknowledged.
- **A7.3c (seasonality) — CLOSED.** §1.3 has a dedicated seasonality bullet (daylight, pollen, mood-cycle, ambient temperature) with explicit collinearity-with-dose acknowledgment AND a routed sensitivity test (Sensitivity F nonlinear time). The fire-and-fix-and-test pattern is the right shape per the v1-review §2 / §4.
- **A7.3d (device-stability) — CLOSED.** FR245-throughout one-liner in §1.3.

### Methodology-specific elements — Type B (cross-cutting)

- **B3 (confounder enumeration) — CLOSED.** §1.3 ordered by likely impact (seasonality > Breinvoeding > device > life-events).
- **B5 (autocorrelation effective N) — CLOSED** via §6.3 lag-1 ρ + effective N output.
- **B10 (reproducibility seed) — CLOSED.** `bootstrap_seed = 42` in §6.2.
- **B7 (effect size + CI) — re-classified PASS in v2.** See I2.4 discussion above.

### Side observations

- **Side** — **§4.4 null pre-spec scope vs the new sensitivity columns (judgment-call, not a fire).** The 4-condition null pre-spec was locked in v1 (HAC CI, effect-size floor, bootstrap CI, lagged-lcera p). v2 adds Sensitivity Column E (crash-drop) and Sensitivity Column F (nonlinear time) but does NOT extend the null pre-spec to include them. This is internally consistent — the v2 fixes were specified as additive — but a reader could legitimately ask: "if these new sensitivities are robustness checks, why aren't they in the null pre-spec?" The defensible answer is that the lagged-lcera sensitivity is the most relevant to downstream Personal-register hypotheses (it gates baseline machinery), while crash-drop is expected-near-null per §4.3-E and nonlinear-time is a one-shape robustness check rather than a discriminating test. Including all six in null pre-spec would tighten "evidence of absence" but make null-declaration harder. The judgment call is defensible either way; the current spec stands. Surfacing for the v3 conversation if it happens.
- **Side** — **§4.1 nominal range vs §3.2 analytical range internal cross-reference.** §4.1 says `d ∈ [2026-03-20, 2026-06-05]` (the nominal window) "restricted to days where stress_mean_sleep(d) is observed". §3.2 says the analytical window after NaN-tail filter is 2026-03-20 → 2026-05-29. The two are consistent (auto-NaN-filter handles it) but a reader could read §4.1's nominal-end-date as the analytical-end. Minor inconsistency-of-presentation; one bracketed clarification in §4.1 ("nominal range; effective analytical end per §3.2 = 2026-05-29") would close it.
- **Side** — **The Sensitivity F df concern is pre-addressed**. The §6.2 spec says "month-indicator dummies as fallback if the spline basis becomes singular at this n", which gracefully handles the n≈70 ÷ 5-parameter df concern. Good preemptive engineering.
- **Side** — **Citation form is uniformly tighter in v2**. Each citation includes journal + volume + issue + page range (where applicable) + a material-contribution sentence; this matches the §2.2 input-2 standard ("each citation gets a sentence on what it actually contributes"). The v1-review's I2.2 form-fires are uniformly closed.
- **Side** — **The §7 audit-hooks-engaged section is well-maintained**: expanded from 6 hooks (v1) to 8 hooks (v2: added §3.4, §3.5, §3.6 entries) with concrete cross-references to where each hook is engaged in the MD body.

## 3. What does not fire (selective)

Non-trivial passes worth naming for the v2 lock:

- **The state-of-art naming pattern is now uniform across the MD's three methodological choices.** §2.3 names PK/PD as state-of-art for the exposure model with citation; §4.2 names HAC SE as state-of-art for autocorrelation with citation; §4.6 names ITS as state-of-art for intervention effects with citation (and rejects with sharpened reason). This is the worked-example state-of-art-named-then-adopted-or-rejected discipline applied consistently. v1 had two of three; v2 has three of three.
- **The seasonality fire-and-fix pattern is the model treatment for a Layer 4 confound.** The v1 review identified seasonality as a substantive fire (calendar-time / dose-time collinearity over the spring window). The v2 response: (1) name the confound in §1.3 with the specific mechanisms (daylight, pollen, mood-cycle, temperature); (2) acknowledge the linear-time covariate's partial coverage; (3) add Sensitivity Column F as the test against the caveat; (4) pre-spec the read for either direction (survives → bounded leakage; disappears → ambiguous). This is the same fire-and-fix shape the parent MD §1 used for the LC recovery trajectory confound; consistent project discipline.
- **The Sensitivity E "Expected impact" paragraph is a model of caveat-class quantitative pre-spec.** v2 doesn't just add the column — it tells the reader what null-effect-on-this-column means (~0.4 expected crash-days; near-identical to primary; informative because §3.6 named count confirms the late-LC crash-rarity prior). This is the right asymmetry: pre-spec the expected outcome, not the test result.
- **The one-sided test tradeoff defence in §4.1 is exemplary.** Most one-sided-test choices in methodology MDs are silent or hand-waved. v2's "if a reviewer rejects the §1.4 direction-commitment, the analysis should be re-spec'd to two-sided rather than mid-stream" is a methodological-premise framing that maintains audit trail across the prior-commitment / direction-commitment / test-direction chain. Other intervention MDs in the project could borrow this pattern.
- **The §4.3-C lagged-lcera attenuation caveat carries over from v1 unchanged and remains the model treatment for a §3.2 audit hook engagement.** v1 review section 3 already named this; the v2 review confirms it survives the v2 expansion.
- **The §7 v2 revision-log entry is a thorough fix-by-fix landing map.** All 13 v1-review recommendations enumerated, each with the section where the fix landed and a short description. This is the right v1 → v2 audit-trail practice and matches the parent MD's v2 pattern.

## 4. What would strengthen this MD (minor, judgment-call items only)

The v2 closes all blocking and substantive v1 fires. The remaining items are minor audit-trail / clarity additions that do not affect defensibility:

1. **Acknowledge in §4.4 that the WWC 2022 SCED effect-size menu (Cohen's d, Hedges' g, Tau-U, NAP, IRD) does not apply directly to regression coefficients**. One sentence: "Effect-size measurement here is the SD-normalised regression coefficient (`β_dose` / SD(stress_mean_sleep)), not a SCED group-phase comparison metric; the WWC 2022 §V menu of effect sizes (Cohen's d, Tau-U etc.) is designed for phase-comparison designs and does not directly apply to continuous-exposure regression." Closes the I2.4 audit-trail item.
2. **Cite Daza 2018 in §1.3 substantive-confound paragraph or §1.4 framing paragraph**. One sentence anchoring the within-subject counterfactual framework. Local PDF at [`literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf`](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf). Closes L2.1.
3. **Add bracketed clarification in §4.1 model definition**: "with `d ∈ [2026-03-20, 2026-06-05]` (nominal window; effective analytical end per §3.2 = 2026-05-29 after NaN-tail filter)". Closes the §3.2-vs-§4.1 presentation inconsistency.
4. **Tighten the I3.3 linear-vs-log-dose distinguishability sentence in §4.1 four-input reasoning**: "the two are co-linear over the relevant range" → "the two are co-linear for the smooth-monotonic-decline range of dose values in this corpus; with substantial dose-range variation outside the clinical 8-30mg window, linear-vs-log would be distinguishable, but at this corpus's coverage they are not".
5. **(Optional, defer to a v3 conversation)** Consider whether Sensitivity Columns E (crash-drop) and F (nonlinear time) should enter the §4.4 null pre-spec. The current 4-condition rule is defensible; expanding to 6 conditions would tighten "evidence of absence" but make null-declaration harder. This is a substantive methodological judgment call that the v1 review did not surface; raised here for completeness, not as a fire.

None of these items block the v2 lock.

## 5. Verdict

**DEFENSIBLE** — all 13 v1-review recommendations folded in with concrete, well-cited, mechanism-aware additions; the highest-priority v1 fires (L4.4 crash-drop binding audit hook, A7.3c seasonality confound, I2.2 missing canonical citations, I1.1 PK/PD state-of-art naming) are uniformly closed; the locked choices (linear-in-dose, PK-smoothed primary exposure, Newey-West HAC, 4-condition null pre-spec) survive the v2 expansion unchanged; remaining minor items (Cohen's d anchoring, Daza 2018 explicit citation, presentation polish, optional null-pre-spec expansion) are audit-trail clarifications rather than methodological gaps and can be folded in opportunistically without re-review.

The MD is ready to lock for the script-implementation session.

---

## Methodology

This methodology review walks CONVENTIONS §2.2 four-input bar plus the applicable items from the 4-layer checklist defined in [README.md](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

Plus the state-of-art literature specific to this methodology question (now properly cited in the v2 target):

- **Observational intervention effect on a single subject**: Interrupted Time Series — Bernal Cummins Gasparrini 2017 *IJE* 46(1):348-355. Named in §4.6, rejected with mechanism-based reason. CLOSED in v2.
- **Dose-response in single subjects (PK/PD modelling)**: Rowland & Tozer 2011 textbook; Gabrielsson & Weiner 2016 textbook; citalopram SPC EMA; Hyttel 1994 SSRI-class pharmacology. Named in §2.3 as state-of-art and adopted. CLOSED in v2.
- **Block bootstrap**: Künsch 1989 *Annals of Statistics* 17(3):1217-1241 (moving-block); Politis & Romano 1994 *JASA* 89(428):1303-1313 (stationary). Named in §4.3-A. CLOSED in v2.
- **HAC standard errors**: Newey & West 1987 *Econometrica* 55(3):703-708 (canonical estimator); Andrews 1991 *Econometrica* 59(3):817-858 (lag selection). Named in §4.2. CLOSED in v2.
- **SSRI/citalopram autonomic + sleep literature**: Marin 2010, Tantucci 2003, Licht 2010, Kemp 2010, Wichniak 2017. Queued at QUEUED-WORK Tier 3; status acknowledged in §1.4 audit-trail note. CLOSED in v2 (status acknowledged, retrieval not gating).

Project-specific audit hooks from [CONVENTIONS.md](../CONVENTIONS.md) §2.2 (four-input bar), §2.1 / §3 / §4 (discipline gates + audit hooks). The v2 MD engages 8 hooks (vs 6 in v1): §2.1, §2.2, §3.2, §3.3, §3.4, §3.5, §3.6, §3.7, §4.3. The binding §3.4 crash-drop sensitivity hook (highest-priority v1 fire L4.4) is fully closed via Sensitivity Column E in §4.3 with §3.6-formatted named count output in §6.3.
