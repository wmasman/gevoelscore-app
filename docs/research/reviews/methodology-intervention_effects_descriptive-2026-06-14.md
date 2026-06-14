# Methodology review: Intervention-effect descriptive characterisation (methodology/intervention_effects_descriptive.md)

**Target**: [../methodology/intervention_effects_descriptive.md](../methodology/intervention_effects_descriptive.md)
**Target commit**: untracked working-tree file as of HEAD `7c81555` (the MD has never been committed; reviewing the on-disk draft dated 2026-06-14 per its §1 status line)
**Reviewer mode**: Claude (independent methodology peer reviewer per CONVENTIONS §1.2; producer-mode MD under §2.2 four-input bar)
**Review date**: 2026-06-14

## 1. What the MD specifies

A **Layer 1 descriptive methodology MD** characterising whether documented interventions (citalopram-traject in 3 phases, CPAP-interventie, Ergotherapie Rouschop, plus any other `interventie`-category annotation) coincide with visible step-changes in eight per-day channels (seven baseline channels + `gevoelscore` as outcome). Specifies a pre-vs-post window comparison with a 14-day transition buffer, neighbour-truncated pre/post windows to handle the citalopram afbouw cluster, Mann-Whitney U as a descriptive statistic (explicitly not a verdict), median + IQR + signed median-diff per pair, plus human-coded `transition_shape` after plot review.

**Framing is descriptive-only**: no segmentation choice is locked. The MD's findings feed a conditional follow-up `intervention_baseline_segmentation.md` (currently nonexistent) only if findings warrant. Downstream artefacts that *would* be affected if a segmentation decision lands: every PEM-pacing pre-reg using `_lagged_lcera` columns whose baseline window overlaps an intervention boundary (B1, B4, C4, D5, H4, H5 in the Wiggers register; P4a / P4b / P5b in the personal register; C4b in Wiggers' personal register). The MD names this cascade explicitly in §7.

## 2. What fired and why

### Spine — §2.2 four-input bar (inherits from CONVENTIONS §2.2)

#### I1 — Best-practices standards

- **[I1.1 — CONVENTIONS §2.2 input 1 — substantive]** — **Interrupted Time Series (ITS) with segmented regression is the state-of-art for observational intervention-effect estimation** (Bernal, Cummins, Gasparrini 2017 *Int J Epidemiol*; Wagner et al. 2002; Cochrane EPOC). ITS decomposes the response into pre-intervention level + pre-intervention trend + level change at intervention (β2) + trend change post-intervention (β3). The MD does not name ITS in §1 or §4. A reader (or a future producer agent) cannot tell whether the MD's authors are unaware of ITS or whether ITS was deliberately rejected for Layer 1 descriptive purposes. §2.2 wants the standard named-and-rejected-with-reason, not unnamed.
- **[I1.2 — CONVENTIONS §2.2 input 1 — substantive]** — Mann-Whitney U is asserted as the analysis method without justifying it as a *deliberate descriptive simplification of ITS*. The honest framing would be: "we run Mann-Whitney U on pre vs post as a level-only descriptive characterisation; ITS with segmented regression is the state-of-art alternative and is deferred to the follow-up segmentation MD if findings warrant". One paragraph closes both I1.1 and I1.2.

#### I2 — Established literature

- **[I2.1, I2.4 — CONVENTIONS §2.2 input 2 — substantive]** — **Channel-specific literature exists and is not consulted.**
  - **CPAP autonomic effects**: Marin et al. 2010 *Lancet* (long-term cardiovascular effects of CPAP), Tantucci et al. 2003 *Chest* (CPAP effect on autonomic indices). CPAP demonstrably affects RHR, HRV, sleep architecture within 2-4 weeks.
  - **SSRI autonomic effects**: Licht et al. 2010 *Biol Psychiatry* (SSRI lowers HRV in depression); Kemp et al. 2010 (meta-analysis of SSRI effect on HRV).
  - **SSRI sleep architecture**: Wichniak et al. 2017 *Curr Psychiatry Rep* (SSRI effects on sleep stages, REM suppression).
  - The MD's §3 says channels are "plausibly affected by CPAP" / "plausibly affected by CPAP + citalopram". Lifting this to "documented to affect RHR / HRV / REM per [Marin 2010 / Licht 2010 / Wichniak 2017]" makes the channel selection literature-grounded rather than project-intuition.
- **[I2.3 — CONVENTIONS §2.2 input 2 — substantive]** — **Pharmacokinetic / clinical-onset literature is not cited for the 14-day transition window**. Citalopram steady-state plasma occurs at ~7-10 days post-dose-change but clinical effect onset is conventionally 2-4 weeks (clinical pharmacology). CPAP autonomic effects emerge within 2-4 weeks per Marin 2010. **The 14-day buffer is shorter than the citalopram clinical-onset window** — pre-vs-post comparison around a citalopram start with only a 14-day buffer will straddle the drug's onset rather than separating pre-drug from steady-state. Either widen the buffer (28 days?) with literature anchor, or run sensitivity sweep across {7, 14, 28, 42} days.

#### I3 — Tradeoff vision

- **[I3.2 — CONVENTIONS §2.2 input 3 — substantive]** — **Mann-Whitney U vs segmented regression / ITS is the load-bearing methodological choice in this MD and the tradeoff is implicit**. The MD doesn't name the alternative or state which dimension was weighted (simplicity vs power, level-only vs level+trend, descriptive vs inferential). Cf. I1.2.
- **[I3.4 — CONVENTIONS §2.2 input 3 — substantive]** — **14-day transition buffer choice is unstated**. The §4.2 spec line says "Transition window: `[d, d+14]` — buffered out of the post analysis (transient effects); not separately reported" without saying why 14 (not 7, not 28). Cf. I2.3.
- **[I3.3 — CONVENTIONS §2.2 input 3 — minor]** — **30-day pre / 60-day post asymmetric window is unstated**. Why asymmetric? The asymmetry isn't pharmacologically obvious (citalopram acute effects peak 4-6 weeks, so post-window of 60-14=46 days is reasonable; pre-window of 30 days is enough to characterise baseline but the choice should be stated). One sentence covers it.

#### I4 — Research limitations + objectives

- **[I4.4 — CONVENTIONS §2.2 input 4 — substantive]** — **The LC recovery trajectory documented in `registry.md` is the corpus-specific confound the MD does not acknowledge**. The trajectory: crash frequency ~10/year in 2023-24 → ~2/year in 2025-26. The CPAP-interventie (2024-01-10 → 2024-04-17) and citalopram-buildup (2024-04-09 → 2024-06-20) **overlap directly with the steepest part of the recovery cliff**. Mann-Whitney U on pre-vs-post around early-2024 interventions will detect the recovery trajectory as a "step change" *even when no intervention effect exists*. This is the highest-priority methodological gap for this specific corpus. One paragraph in §1 or §4 acknowledging the confound (and stating the analysis cannot distinguish intervention-induced step from trajectory-coincidence) is mandatory for the I4 input to clear.

### Layer 1 — Discipline gates (inherits from CONVENTIONS §2.1, §4.1-§4.3)

- **[L1.4 — CONVENTIONS §4.2 — substantive]** — Same root as I4.4 above. The MD frames itself in caveat mode (good) but the underlying-trend confound is a *substantive caveat that's missing*, not an a-priori claim that needs removing. §4.2's "keep caveats" rule applies: the recovery-trajectory acknowledgment is a missing caveat the MD owes.

### Layer 2 — Observational n=1 (inherits from Daza 2018)

- **[L2.1 — CONVENTIONS §5 / Daza 2018 — minor]** — Within-subject counterfactual framing is implicit (the `_lagged_lcera` rolling baseline is named) but not stated explicitly per Daza's terms. One sentence under "How to read this" lifts this from implicit to explicit: *"All comparisons are within-subject counterfactual: post-intervention windows are compared to subject-baseline-at-this-time (the `_lagged_lcera` rolling baseline), not to a population or to the subject-pre-LC-baseline. Comparisons assume the channel's distribution is exchangeable across the boundary modulo the intervention — see §X for confounders."*
- **[L2.2 — Daza 2018 — substantive]** — **Stationarity assumption is unacknowledged**. Mann-Whitney U on a 30-day pre window vs ≤45-day post window assumes the underlying distribution within each window is stationary. On this corpus the documented recovery trajectory + seasonality + per-year variation in life-events make this assumption obviously violated. The MD must either acknowledge the violation explicitly or use an analysis shape that doesn't assume stationarity (ITS with trend term).

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

- **[L3.1 — Natesan Batley 2023 — substantive]** — **Autocorrelation gap = the 83.8% failure mode**. Mann-Whitney U assumes independent observations. Days within a 30-day or 45-day window are autocorrelated (RHR autocorrelation typically ρ > 0.5 at lag 1 in healthy populations, higher in chronic illness). The reported Mann-Whitney p-values are inflated. At minimum the MD should:
  - Note p-values are inflated under positive autocorrelation;
  - Or replace Mann-Whitney U with a block-bootstrap permutation null using a block length per `methodology/permutation_null_block_length.md`;
  - Or report a HAC (Newey-West) corrected effect-size CI on a segmented regression.
- **[L3.4 — Bernal et al. 2017 — substantive]** — **Method is level-only; cannot distinguish level shift from slope inflection.** Citalopram could plausibly produce a *slope* change (e.g. accelerated recovery on SSRI) without a clean *level* step at the boundary. The MD's Mann-Whitney U would miss this entirely. The human-coded `transition_shape` partly mitigates ("gradual drift" is a category) but the quantitative output is level-only. This is exactly what ITS's β3 (trend change) term captures.
- **[L3.5 — same as I1.1 — substantive]** — State-of-art name (ITS) not in the MD. Already named in I1.1.
- **[L3.2 — minor]** — Window sizing (14-day transition + 30/60 pre/post) is specified but not justified by carryover literature. Already covered in I2.3 / I3.3 / I3.4.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3)

- **[L4.3 — CONVENTIONS §3.3 — minor]** — The 7-channel list (§3) includes plausibly correlated pairs: `bb_overnight_gain` ↔ `bb_lowest`, `stress_mean_sleep` ↔ `all_day_stress_avg`, `sleep_efficiency` is partly derivable from `sleep_duration_min` + `sleep_awake_min`. For a descriptive sweep this is fine — the MD says "additional baseline channels can be added without pre-registration concern". But a future reader interpreting Section 5's "one specific channel is affected by most interventions" rule could double-count a pair as two channels. One sentence in §3 noting the correlation structure (or in §5 noting that pair-members count as one signal for the row in Section 5's findings table) closes it.

### Methodology-specific elements

#### Type A7 — Intervention-effect MD (relevant sub-type)

- **[A7.1 — Bernal et al. 2017 BMJ — substantive]** — ITS not named. Same as I1.1.
- **[A7.2 — clinical pharmacology — substantive]** — Pharmacokinetic literature for transition window not cited. Same as I2.3.
- **[A7.3 — corpus-specific — substantive]** — **Confounder enumeration is incomplete**. The MD names other interventions (handled via neighbour truncation, good) and LC era (handled via `_lagged_lcera`, good). Missing: (a) the documented recovery trajectory (see I4.4 / L1.4), (b) seasonality (winter blues, hayfever, daylight; in NL the citalopram buildup overlaps spring transition + the consolidation plateau spans 2 winters), (c) life events not in `annotations.yaml` (the MD says "the catalog is data-driven" but `annotations.yaml` is itself curated and likely incomplete on non-clinical life events), (d) tracking-compliance during PEM episodes (the user has fewer compliant tracking days during crashes, which biases the 5-day-floor `len < 5` skip toward crash-windows being dropped). Each of these is a one-line addition to a confounders section.
- **[A7.4 — substantive]** — **Sensitivity to underlying trend is not addressed**. The fix is small: either detrend each channel before the window comparison (subtract a linear fit on the full pre-intervention `_lagged_lcera` series), or add a one-column-sensitivity output showing the Mann-Whitney p-value AFTER detrending. The latter is cheaper.
- **[A7.5 — minor]** — **Blinded transition_shape coding is not specified.** Visual coding of shape labels {no visible change, gradual drift, step, U-shaped / overshoot, noisy / inconclusive} is susceptible to motivated coding (the rater expects citalopram start to produce a step, so reads ambiguous plots as steps). Blinding the rater to which (intervention, channel) they're coding — by serving plots with anonymised titles — reduces this. One sentence in §4 §4 names this.
- **[A7.6 — minor]** — **Pre-spec of "no visible change" criterion is missing.** The five shape categories are listed but not operationalised. Concrete pre-spec: *"no visible change = median_diff within ±0.5×IQR_pre AND no monotonic post-trend AND no overshoot in transition window AND mw_p > 0.10"*. Without this, rater intuition fills the gap and the "no findings" outcome category becomes hard to verify.
- **[A7.7 — N/A — passes]** — **Outcome-contamination check (§3 vs §3b) is the strongest methodological observation in the MD.** The distinction between *baseline-channel step-change* (distorts the predictor's lagged baseline; affects *predictors*) and *outcome-channel step-change* (distorts the crash-label-generating distribution; affects *both predictors AND labels*) is exactly right. The implication table at the end of §3b is well-articulated. This passes A7.7 cleanly with non-trivial evidence — surfaced in Section 3 below.

#### Type B — Cross-cutting

- **[B1 — minor]** — Pre-spec of "no finding" criterion is partial. Section 5's "no `(intervention, channel)` pair shows visible step-change" outcome is a *rater judgement*, not a pre-spec rule. Same root as A7.6.
- **[B2 — substantive]** — **Sensitivity sweep on key parameters is not pre-spec'd**. Window width (`pre_days`, `post_days`), transition buffer width, and the `len < 5` skip threshold are all parameters the result is sensitive to. A pre-spec'd sweep — e.g. transition buffer ∈ {7, 14, 28} days — would surface fragility cheaply.
- **[B3 — substantive]** — Corpus-specific confounder enumeration incomplete. Same root as A7.3.
- **[B4 — substantive]** — Stationarity not acknowledged. Same as L2.2.
- **[B5 — substantive]** — Autocorrelation handling absent. Same as L3.1.
- **[B7 — minor]** — **Effect size + CI together: partial.** Median + IQR + signed median-diff are reported, but no formal standardized effect-size (Cohen's d / Hedges' g for small N, or rank-biserial r for Mann-Whitney) and no CI on the median-diff. Adding `r_rb` (rank-biserial = U / (n1 × n2) - 0.5, then linear-transformed) plus a bootstrap CI on the median-diff is cheap and lifts the statistical output from descriptive-only to descriptive-with-effect-size.
- **[B8 — passes]** — Visual + statistical paired (PNGs + summary CSV). Good.
- **[B9 — passes]** — Causal language is honestly distinguished. "Reported as descriptive statistic, NOT as a verdict" and "p < 0.05 is *consistent with a step-change* on this channel × intervention; not 'significant' in any confirmatory sense". This is the discipline.
- **[B10 — passes]** — Reproducibility hook: script in §6 is concrete with paths, column references, and explicit logic. Runnable from spec. Good.

### Side observations

- **Side**: The MD says "the n-of-1 corpus does not justify automated change-point detection over visual inspection." Defensible as a primary-method choice, but the framing could be tightened: PELT (Killick et al. 2012) or BCP (Adams & MacKay 2007) could be run as a *corroborating* layer alongside visual coding (auto-detected change-points × human-coded transition_shape; agreement strengthens the finding, disagreement flags rater-coder uncertainty). Naming the algorithm and rejecting it explicitly closes A1.2 / I1 cleanly even at n=1.
- **Side**: §1 references "the 'resting pulse of 60 as a global reference' framing" without citation — this appears to be a user-quote anchor from another doc (likely `garmin_pacing_practice.md` or memory). Worth either inlining the quote source or removing the reference if it's not material to this MD's argument.
- **Side**: §6 script uses `mannwhitneyu(pre, post, alternative="two-sided")` from scipy. At small n (e.g. post-window of 25 days = ~20 valid samples after NaN drop), the scipy default uses the asymptotic approximation; the exact test should be requested via `method="exact"` for small n to avoid continuity-correction artefacts. Minor implementation note.

## 3. What does not fire (selective)

- **I4.1-I4.3 pass with non-trivial evidence** — n=1 explicitly acknowledged ("the n-of-1 corpus does not justify automated change-point detection"); observational design implicit in the descriptive-only framing; corpus-specific objective stated ("findings inform whether segmented-baseline machinery is warranted"). The descriptive-only framing is itself an objective alignment.
- **I3.1 passes — the 3-phase citalopram decision is exemplary tradeoff articulation.** Alternatives named (6 dose-step sub-phases, 1 umbrella boundary). Each rejected with reason: sub-truncation at fine phases (the early buildup 10→20mg phase is only 21 days, producing post-windows < 5 days that get skipped), 1-umbrella too coarse (misses the 30mg plateau distinction). 3 phases chosen because each has a long stable consolidation plateau that maximises signal. This is what every methodological choice in the MD should look like.
- **A7.7 (outcome-contamination check, §3 vs §3b) passes with the strongest methodological observation in the MD.** The distinction between baseline-channel step-change (distorts predictor's reference frame) and outcome-channel step-change (distorts crash-label-generating distribution) is structurally important and well-articulated. The implication table at the end of §3b — "a §3 baseline channel step-change affects predictors; §3b gevoelscore step-change affects both predictors AND labels themselves" — is the kind of methodological subtlety that should propagate to all future intervention-related MDs.
- **L1.1 / L1.3 (discipline gates) pass.** The MD explicitly cites §2.1 (descriptive-before-inference) and §4.2 (caveats vs a-priori) and stays in their discipline throughout. "What this MD does NOT do" in §1 is the model paragraph for §4.2 caveat-vs-a-priori framing.
- **L4.1 / L4.2 (project audit hooks on baselines) pass.** `_lagged_lcera` referenced as the reference frame; the v3.2 column family correctly named.
- **B9 (causal language honesty) passes.** "Consistent with a step-change on this channel × intervention; not 'significant' in any confirmatory sense" is the discipline.
- **The neighbour-truncation mechanism (§4 + §6) passes as a non-trivial methodological achievement.** The citalopram afbouw cluster has boundaries ~28-40 days apart. Without truncation, the post-window of one boundary contains the next boundary's onset + post-transient, contaminating the step-change estimate. The MD's `_window_days` columns surface truncation at read-time, making contamination-by-neighbour visible. This is well-engineered.

## 4. What would strengthen this MD

In rough priority order (each item is one paragraph or one column):

1. **Acknowledge the LC recovery-trajectory confound** (addresses I4.4 / L1.4 / A7.3 / B3). One paragraph in §1 or §4: *"This analysis cannot distinguish an intervention-induced step-change from coincidence with the documented LC recovery trajectory (crash frequency ~10/year in 2023-24 → ~2/year in 2025-26 per `analyses/hypotheses/registry.md`). CPAP-interventie (2024-01-10 → 2024-04-17) and citalopram-buildup (2024-04-09 → 2024-06-20) overlap directly with the steepest part of the recovery cliff. Findings should be read as 'consistent with intervention effect OR with secular recovery', not as causal attribution. The follow-up segmentation MD will need a control comparison — e.g. matched pre-intervention pseudo-boundaries — to disentangle."* Highest-impact fix; closes the largest single fire on this corpus.

2. **Name ITS as the state-of-art and frame the Mann-Whitney U as a deliberate Layer 1 descriptive simplification** (addresses I1.1 / I1.2 / I3.2 / L3.4 / A7.1). One paragraph in §4: *"The state-of-art for observational intervention-effect estimation is interrupted time series (ITS) with segmented regression (Bernal, Cummins, Gasparrini 2017 BMJ), decomposing the response into pre-intervention level + trend + level-change β2 + trend-change β3. We deliberately use level-only Mann-Whitney U for this Layer 1 descriptive pass — ITS is reserved for the follow-up segmentation MD if findings warrant. Step-changes that are actually slope inflections will read as 'gradual drift' or 'no visible change' in the human-coded transition_shape and we accept that blind spot at this layer."*

3. **Add a HAC (Newey-West) or block-bootstrap p-value column** (addresses L3.1 / B5). Cheapest closure of the autocorrelation gap: add one column to the summary CSV — `mw_p_block_bootstrap_7d` — running a 7-day block-permutation null per the project's block-length policy (`methodology/permutation_null_block_length.md`). If the corrected p is meaningfully higher than the scipy default, surface the gap.

4. **Add a literature paragraph naming per-channel intervention effects** (addresses I2.1 / I2.4 / A7.2). One paragraph in §3 or §1: *"CPAP autonomic effects on RHR and HRV are documented within 2-4 weeks of treatment onset (Marin et al. 2010 *Lancet*; Tantucci et al. 2003 *Chest*). SSRI / citalopram autonomic effects on HRV are documented (Licht et al. 2010 *Biol Psychiatry*; Kemp et al. 2010). SSRI effects on sleep architecture (REM suppression in particular) are documented (Wichniak et al. 2017 *Curr Psychiatry Rep*). Channel selection in §3 is grounded in these channels' literature-documented sensitivity to the interventions in scope."* Lifts the channel list from project intuition to literature-grounded and closes I2 cleanly.

5. **Justify the 14-day transition buffer and the 30/60 asymmetric window from clinical pharmacology** (addresses I2.3 / I3.3 / I3.4). One paragraph: *"Citalopram steady-state plasma is reached at ~7-10 days post-dose-change; clinical effect onset is conventionally 2-4 weeks. CPAP autonomic effects emerge within 2-4 weeks. The 14-day transition buffer therefore captures steady-state plasma but only the lower end of clinical-onset. A sensitivity sweep across {7, 14, 28} days surfaces fragility — `transition_buffer_sensitivity` columns in the summary CSV."* If the 14-day choice is genuinely deliberate, this paragraph makes the deliberation visible.

6. **Add an effect-size + CI alongside the Mann-Whitney p-value** (addresses B7). Cheapest fix: add `r_rb` (rank-biserial correlation = 2U/(n1*n2) - 1) and a bootstrap CI on the median-diff (1000 resamples within each window, percentile CI). Two columns to the summary CSV. Lifts the statistical output from "p-value alone" to "effect-size + CI" per the Natesan 2023 65.8% distributional-failure-mode mitigation.

7. **Blind the transition_shape coding** (addresses A7.5). One sentence in §4.4: *"Plots are served to the rater with anonymised titles (channel and date only, no intervention label) and shape-coded before the rater reveals the (intervention, channel) mapping. This reduces motivated coding bias toward expected step-changes at expected boundaries."* Cheap, well-established SCED practice.

8. **Pre-spec the "no visible change" criterion** (addresses A7.6 / B1). One sentence in §4.4 attaching to the five shape categories: *"no visible change = median_diff within ±0.5×IQR_pre AND no monotonic post-trend (Mann-Kendall τ on post-window not significant at α=0.10 uncorrected) AND no overshoot in transition window AND `mw_p > 0.10`. All four conditions required."* Operationalises the null finding.

9. **Mention PELT / BCP as corroborating-not-primary** (addresses Side / A1.2). One sentence in §4: *"Automated change-point detection (PELT, Killick et al. 2012; BCP, Adams & MacKay 2007) is not used as primary at n=1 per WWC visual-inspection tradition, but could corroborate the human-coded transition_shape as a secondary layer. Deferred to the follow-up segmentation MD."*

10. **Note the definitional-pair structure in §3** (addresses L4.3). One sentence: *"Among the seven baseline channels, three pairs are correlated by construction or by Layer 3 finding: `bb_overnight_gain` ↔ `bb_lowest`, `stress_mean_sleep` ↔ `all_day_stress_avg`, `sleep_efficiency` is partly derivable from `sleep_duration_min` + `sleep_awake_min`. Per CONVENTIONS §3.3, downstream Section 5 interpretation treats co-firing pair-members as one signal, not two."*

## 5. Verdict

**REVISION RECOMMENDED** — §2.2 inputs I1 (best-practices standards not named) and I2 (per-channel intervention-effect literature not cited) are absent; I4 substantively fires on the unacknowledged LC recovery-trajectory confound which is the highest-priority methodological gap on this specific corpus; Layer 3 fires on autocorrelation (Natesan Batley 2023 failure mode) and level-only blind spot. The descriptive-only framing partly absolves I1 / I2 but doesn't make them disappear, and the recovery-trajectory gap is corpus-specific not framework-shaped. A focused tightening pass (#1-#5 in Section 4) lifts this from "honest descriptive" to "honest descriptive on the state-of-art map" without changing the script or the §3 / §3b distinction — both of which are strong.

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

- **Bernal, Cummins, Gasparrini 2017** *Int J Epidemiol* (BMJ guidance) — Interrupted Time Series with segmented regression as state-of-art for observational intervention effects. Not currently downloaded; cited externally.
- **Marin et al. 2010** *Lancet*, **Tantucci et al. 2003** *Chest* — CPAP autonomic effects. Not downloaded.
- **Licht et al. 2010** *Biol Psychiatry*, **Kemp et al. 2010** — SSRI autonomic effects on HRV. Not downloaded.
- **Wichniak et al. 2017** *Curr Psychiatry Rep* — SSRI sleep-architecture effects. Not downloaded.
- **Killick, Fearnhead, Eckley 2012** *JASA* — PELT change-point detection. Not downloaded.

Project-specific audit hooks from [../CONVENTIONS.md](../CONVENTIONS.md) §2.2 (four-input bar), §2.1 / §3 / §4 (discipline gates + audit hooks). Corpus-specific recovery-trajectory confound surfaced from [`../analyses/hypotheses/registry.md`](../analyses/hypotheses/registry.md). LC era + lagged-baseline references from [`./lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md).
