# Methodology review: Intervention-effect descriptive characterisation (methodology/intervention_effects_descriptive.md) — v2

**Target**: [../methodology/intervention_effects_descriptive.md](../methodology/intervention_effects_descriptive.md)
**Target commit**: untracked working-tree file as of HEAD `7c81555`. The MD has never been committed; reviewing the on-disk draft as revised 2026-06-14 in response to the v1 review at [`methodology-intervention_effects_descriptive-2026-06-14.md`](methodology-intervention_effects_descriptive-2026-06-14.md). The §7 revision log in the target MD documents the v1 → v2 fix-by-fix landing map.
**Reviewer mode**: Claude (independent methodology peer reviewer per CONVENTIONS §1.2; producer-mode MD under §2.2 four-input bar)
**Review date**: 2026-06-14 (v2; same-day re-review per skill Phase 4 convention)

## 1. What the MD specifies

A Layer 1 descriptive methodology MD characterising whether documented interventions (citalopram-traject collapsed into 3 phases via containment filter + 2 phase-transition markers, CPAP-interventie, Ergotherapie Rouschop) coincide with visible step-changes in 8 per-day channels (7 baseline channels in §3 + `gevoelscore` as the methodologically-distinct outcome-contamination channel in §3b).

**Substantive revision vs v1**: the recovery-trajectory confound (highest-priority v1 fire) is now named in §1 as a substantive unresolvable caveat; ITS is named as state-of-art with Mann-Whitney U framed as deliberate Layer 1 simplification; a 4-buffer sensitivity sweep on the transition window `B ∈ {7, 14, 28, 42}` produces one CSV row per (intervention, channel, buffer); block-bootstrap p complements asymptotic Mann-Whitney p; rank-biserial r + bootstrap CI on median-diff add effect-size + uncertainty; `no_visible_change` is a four-condition pre-spec (median_diff, r_rb, mw_p, mw_p_block_bootstrap) operationalising the null finding; definitional-pair structure noted in §3; PELT/BCP mentioned as corroborating-not-primary. Per the §7 revision log: 8 of 10 v1 fixes applied, 1 queued to QUEUED-WORK Tier 3 (per-channel literature citations: Marin/Tantucci/Licht/Kemp/Wichniak), 1 deferred as a process change with partial mitigation via the `no_visible_change` pre-spec (blinded coding).

Downstream artefacts unchanged from v1: every PEM-pacing pre-reg with a `_lagged_lcera` baseline window overlapping an intervention boundary inherits the methodology choice (B1, B4, C4, D5, H4, H5 in the Wiggers register; P4a / P4b / P5b in the Personal register; C4b in the Wiggers register's personal-extension entry).

## 2. What fired and why

### Spine — §2.2 four-input bar (inherits from CONVENTIONS §2.2)

#### I1 — Best-practices standards

- **No fires.** All three v1 fires (I1.1 ITS not named; I1.2 not rejected with reason; A7.1 same as I1.1) are CLOSED via the §1 method-choice paragraph: *"The state-of-art for observational intervention-effect estimation is interrupted time series (ITS) with segmented regression (Bernal, Cummins, Gasparrini 2017 BMJ), decomposing the response into pre-intervention level + trend + level-change β2 + post-intervention trend-change β3. We deliberately use level-only Mann-Whitney U for this Layer 1 descriptive pass — ITS is reserved for the follow-up segmentation MD if findings warrant."* The rejection-with-reason is tied to the Layer 1 descriptive framing, not corpus n=1 specifically — that's defensible because the descriptive-before-inference discipline is itself a corpus-imposed sequencing constraint.

#### I2 — Established literature

- **[I2.1, I2.4 — CONVENTIONS §2.2 input 2 — substantive, queued]** — Per-channel intervention-effect literature (Marin 2010 + Tantucci 2003 for CPAP; Licht 2010 + Kemp 2010 for SSRI HRV; Wichniak 2017 for SSRI sleep) is **NOT cited** in §3, but the gap is **named and queued** in the §3 paragraph: *"the 'plausibly affected by CPAP / citalopram' framing above is project-intuition. Per-channel intervention-effect literature exists ... Queued in QUEUED-WORK.md Tier 3."* The QUEUED-WORK Tier 3 entry exists and is concrete (specific papers named with a description of what each materially contributes). Fire status: **open but tracked-deferred**. Not blocking — descriptive findings can run without lit grounding; the lit pass tightens the channel-selection justification post-hoc.
- **[I2.3, A7.2 — CONVENTIONS §2.2 input 2 — partial]** — Pharmacokinetic literature anchoring the transition-buffer choice is **implicitly referenced** (the §4 "Why the buffer sweep matters" paragraph mentions "Citalopram clinical onset is 2-4 weeks (longer than the original 14-day buffer)" and §1 mentions CPAP autonomic effects emerging within 2-4 weeks) but **no specific pharmacokinetic citation is named**. The sensitivity sweep `B ∈ {7, 14, 28, 42}` partly closes the methodological gap by surfacing buffer-choice sensitivity directly; a fragility-only finding at one buffer-width is now visible. **Mitigated from v1 substantive to v2 minor**: the sweep is the descriptive response to the absent citation; a single citation (Hyttel 1982 for citalopram steady-state pharmacokinetics; Marin 2010 for CPAP onset window) would close it cleanly without changing the script.

#### I3 — Tradeoff vision

- **[I3.3 — CONVENTIONS §2.2 input 3 — minor, unaddressed]** — The 30-day pre vs 60-day post asymmetric window choice (max_window minus buffer) is still unstated. Carried unchanged from v1. The buffer sweep doesn't address this: the pre cap stays at 30 days and the post cap stays at 60 across all buffer values. One sentence covers it.

#### I4 — Research limitations + objectives

- **No fires.** I4.4 (the v1 highest-priority fire on the unacknowledged recovery trajectory) is CLOSED via the §1 substantive-confound paragraph, which explicitly names the trajectory (~10/year → ~2/year per registry.md), names the overlap with early-2024 interventions (CPAP-interventie 2024-01-10 → 2024-04-17 and citalopram-buildup 2024-04-09 → 2024-06-20), states that pre-vs-post will detect trajectory as step-change "even when no intervention effect exists", and reframes findings as "consistent with intervention effect OR with secular recovery, not as causal attribution". This is the model paragraph for §4.2 caveat framing on a substantive confound.

### Layer 1 — Discipline gates (inherits from CONVENTIONS §2.1, §4.1-§4.3)

- **No fires.** L1.4 (recovery-trajectory caveat) CLOSED — same root as I4.4. All other Layer 1 items pass cleanly (descriptive-before-inference framing throughout; caveat-mode framing of all confounds; no interpretive marks on the measurement procedure).

### Layer 2 — Observational n=1 (inherits from Daza 2018)

- **[L2.1 — CONVENTIONS §5 / Daza 2018 — minor, unaddressed]** — Within-subject counterfactual framing is still implicit. Carried unchanged from v1. One sentence under §1 or §4: *"All comparisons are within-subject counterfactual: post-intervention windows are compared to subject-baseline-at-this-time, not to a population or to subject-pre-LC baseline. Per Daza 2018, the comparison assumes the channel's distribution is exchangeable across the boundary modulo the intervention — see §1 confounder paragraph and §4 buffer-sweep block."*
- **[L2.2 / B4 — Daza 2018 — partly closed]** — Stationarity assumption is now **partly named** via the §1 recovery-trajectory caveat (an explicit non-stationarity statement on the most material confound). The block-bootstrap p further relaxes the iid assumption within windows. What's **still implicit**: a general stationarity statement covering seasonality, episodic life events, and tracking-compliance drops during crashes. Lifting the recovery-trajectory caveat into a general "intra-window stationarity may be violated by: (a) recovery trajectory, (b) seasonality, (c) life events outside annotations.yaml, (d) tracking-compliance dropping during crashes" closes both this and the A7.3.c seasonality fire below.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

- **[L3.3 / B6 — multiplicity, NEW fire in v2]** — The v2 revision substantially increased the row count (now ~256 rows from ~64) via the 4-buffer sweep. **No multiplicity correction policy is named**, even at the descriptive layer. The descriptive-only framing partly absolves (B9 causal-language discipline is intact), but with 256 (channel × intervention × buffer) cells, ~13 of them are expected to fire at p<0.05 under the null. One paragraph in §4 or §5: *"With ~256 (intervention, channel, buffer) cells, descriptive-only p-values are not corrected for multiplicity; expect ~13 cells at p<0.05 under the null. The reader should weight `mw_p < 0.01` and `r_rb > 0.3` more heavily than borderline p-values; the buffer-sweep coherence (a finding that fires at multiple buffer widths) is itself an informal multiplicity check."* Minor in v2 (descriptive framing reasonable) but should be named — this is the Natesan 2023 §3 multiple-comparison failure mode.
- **[A7.4 — substantive, named-but-not-addressed]** — The recovery-trajectory caveat in §1 names the underlying-trend confound; the script does **not detrend** before window comparison. The §1 paragraph says "A follow-up segmentation MD would need ... trend-detrending to disentangle. Out of scope here." This is honest deferral but the gap remains substantive: a reader expecting the v2 revision to *analytically* address the highest-priority v1 fire (rather than just caveat it) will be disappointed. **Verdict**: the caveat framing is defensible at Layer 1 descriptive level, but a one-column detrend sensitivity (the `mw_p_after_linear_detrend` column the v1 audit recommended) would have moved this from "named confound" to "tested confound" cheaply. Worth recommending again as the single highest-leverage post-v2 addition.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3)

- **No fires.** L4.3 (definitional-pair structure) CLOSED via the §3 paragraph: *"three pairs in the list are correlated by construction or by Layer 3 finding — `bb_overnight_gain` ↔ `bb_lowest`, `stress_mean_sleep` ↔ `all_day_stress_avg`, and `sleep_efficiency` ↔ `sleep_duration_min`/`sleep_awake_min`. Downstream §5 interpretation should treat co-firing pair-members as one signal, not two."* Per CONVENTIONS §3.3 letter and spirit.

### Methodology-specific elements

#### Type A7 — Intervention-effect MD

- **A7.1, A7.6, A7.7** — All CLOSED. A7.1 (ITS named) closed via §1 method-choice paragraph. A7.6 (`no_visible_change` pre-spec) closed via §4 four-condition rule. A7.7 (outcome-contamination check) was already the strongest part of v1 and remains so.
- **[A7.2 — partially closed]** — Pharmacokinetic literature is **implicitly referenced** as the motivation for the buffer sweep but specific citations not named. See I2.3 above.
- **[A7.3 — partially closed]** — Confounder enumeration covers (a) other concurrent interventions (neighbour truncation) and (b) LC recovery trajectory (newly closed). **Still missing**: (c) seasonality (winter blues / daylight / hayfever; in NL the citalopram buildup overlaps spring transition and the consolidation plateau spans two winters), (e) life events not in `annotations.yaml`. Resolution: one line in the §1 confounder paragraph extending the trajectory list with `+ seasonality (NL latitude; citalopram buildup overlaps spring; consolidation spans 2 winters) + life events not curated in annotations.yaml + tracking-compliance dropping during crashes (skipped 5-day-floor pairs disproportionately during crash periods)`. Cheapest single-line closure of three residual items.
- **[A7.4 — named but not analytically addressed]** — See Layer 3 entry above. The §1 caveat names the underlying-trend confound; the script does not detrend.
- **[A7.5 — deferred per revision log]** — Blinded transition_shape coding is explicitly deferred as a process change. The four-condition `no_visible_change` pre-spec (A7.6) partly mitigates by removing rater discretion on the null finding. **Acceptable resolution** given the descriptive framing; not a fire in v2 because the revision log makes the deferral visible and the mitigation strategy explicit.

#### Type B — Cross-cutting

- **B1, B2, B5, B7, B8, B9, B10 — all CLOSED or PASS.** Pre-spec of null (B1), sensitivity sweep (B2), autocorrelation handling (B5), effect-size+CI (B7), visual+statistical paired (B8), causal-language honesty (B9), reproducibility hook (B10) — all clean.
- **B3 (corpus-specific confounder enumeration)** — partially closed; see A7.3 above.
- **B4 (stationarity assumption)** — partially closed via recovery-trajectory caveat; see L2.2 above.
- **B6 (multiplicity policy)** — new fire in v2 from row-count expansion; see L3.3 above.

### Side observations

- **Side**: Block length for the permutation null is hard-coded as `BLOCK_LEN = 7` with the comment "matches project default". The MD says "(per `methodology/permutation_null_block_length.md`'s default)" in §4 prose but the script comment is loose. Citing the specific section / value in the permutation_null MD (or noting it's "7 days per `methodology/permutation_null_block_length.md` §X") closes the audit-trail loop cleanly.
- **Side**: The block-bootstrap is `O(N_BOOTSTRAP × N_BUFFERS × N_CHANNELS × N_INTERVENTIONS)` ≈ 1000 × 256 ≈ 256k Mann-Whitney recomputes; plus the same magnitude on the median-diff CI. At Python+scipy speeds this is plausibly 5-15 minutes of compute. The §7 status line "Script not yet run" doesn't flag this expected runtime — a one-line note prevents the user from killing a perceived-stuck run.
- **Side**: The script uses scipy's `mannwhitneyu(... alternative="two-sided")`. For small-N windows (e.g. post-window of 25 days minus NaNs ≈ 20 valid samples), scipy uses the asymptotic approximation by default. `method="exact"` would avoid continuity-correction artefacts at small n. Carried from v1 side observation, unchanged. Implementation note only — not material to the methodology choice.
- **Side**: §1 references "the 'resting pulse of 60 as a global reference' framing" without inline citation source. Carried from v1 side observation, unchanged. Likely a memory-anchor or a quote from `garmin_pacing_practice.md`; one inline parenthetical fixes it.

## 3. What does not fire (selective)

- **Recovery-trajectory caveat (I4.4 / L1.4 / B3.b)** — the highest-priority v1 substantive fire is **clearly CLOSED** at the caveat level. The §1 paragraph is concrete (names the trajectory magnitude with source, names the overlap with early-2024 interventions with dates, names what the analysis "CANNOT resolve", reframes findings) and structurally model — future intervention-effect MDs across the project can copy this paragraph as the template for substantive-confound disclosure.
- **ITS-as-state-of-art framing (I1.1 / I1.2 / A7.1)** — closed cleanly. The Mann-Whitney is now explicitly framed as a deliberate Layer 1 descriptive simplification, with the level-only blind spot acknowledged and the slope-inflection failure mode named.
- **Autocorrelation handling via block-bootstrap p (L3.1 / B5)** — the 7-day-block permutation null + 1000 resamples is the standard project-conforming response to the Natesan 2023 83.8% failure mode. The script's helper `block_bootstrap_p` correctly preserves within-block autocorrelation and computes a two-tailed p against the observed deviation from the null centre. This is well-engineered.
- **Effect-size + CI together (B7)** — rank-biserial r matched to Mann-Whitney + bootstrap CI on median-diff lifts the statistical output from "p-value alone" to "p-value + effect-size + uncertainty". Standard SCED practice per WWC 2022 §V.
- **`no_visible_change` four-condition pre-spec (A7.6 / B1)** — concrete operational rule: `|median_diff| ≤ 0.5 × IQR_pre AND |r_rb| < 0.1 AND mw_p > 0.10 AND mw_p_block_bootstrap > 0.10`. All four conditions must hold; the null finding outcome is no longer rater-dependent.
- **Buffer sensitivity sweep (B2 / I3.4 / A7.4 partial)** — the {7, 14, 28, 42} sweep with primary B=14 surfaces buffer-fragility directly. A finding that fires only at B=7 but not at B=28 is now visibly weaker than a finding that survives all four. This is the v2's biggest single methodological improvement after the recovery-trajectory caveat.
- **Definitional-pair structure (L4.3)** — §3 paragraph correctly identifies the three correlated pairs and instructs §5 interpretation to treat co-firing pair-members as one signal. CONVENTIONS §3.3 letter and spirit.
- **3-phase citalopram decision (I3.1)** — still exemplary. Alternatives named (6 dose-step sub-phases, 1 umbrella boundary), each rejected with reason tied to the corpus's specific data resolution. Carried from v1.
- **§3 vs §3b distinction (A7.7)** — still the strongest single methodological observation in the MD. Carried from v1.
- **Neighbour-truncation mechanism** — well-engineered; carried from v1.
- **§7 revision log table** — meta-level practice that other producer-mode MDs in this project should adopt. Audit-fix-to-landing-location map is auditable and creates a verifiable trail from review-report → MD-revision.

## 4. What would strengthen this MD

In rough priority order (residual after the v1 revision pass):

1. **Add a `mw_p_after_linear_detrend` sensitivity column** (closes A7.4 properly). The §1 recovery-trajectory caveat names the underlying-trend confound but the script does not address it. Cheapest analytical closure: fit a linear trend on the pre-window of each `(intervention, channel)`, subtract it from both pre and post values before computing Mann-Whitney U, report the detrended p as a sensitivity column. If the detrended p is meaningfully higher than the un-detrended p, the trajectory is doing work on the finding. ~30 lines of script. Moves A7.4 from "named confound" to "tested confound".

2. **Extend the §1 confounder paragraph to cover seasonality + life-events-outside-corpus + tracking-compliance** (closes A7.3.c, A7.3.e, partly L2.2 / B4). One sentence at the end of the §1 substantive-confound paragraph: *"Other confounders this descriptive pass also does not control for: seasonality (NL latitude; the citalopram buildup overlaps spring transition; the 30mg consolidation plateau spans 2 winters), life events not curated in `annotations.yaml` (the catalog is data-driven but `annotations.yaml` is incomplete on non-clinical life events), and tracking-compliance dropping during PEM episodes (the `len < 5` skip disproportionately drops crash-adjacent windows). All three are caveat-class; none warrant additional analytical machinery at Layer 1."* Cheapest single-line closure of three audit items.

3. **Add a multiplicity-policy sentence in §4 or §5** (closes L3.3 / B6 new fire). One paragraph: *"With ~256 (intervention, channel, buffer) cells and descriptive-only framing, p-values are not corrected for multiplicity; under the null ~13 cells are expected to fire at p<0.05 by chance. Read `mw_p < 0.01` and `|r_rb| > 0.3` more heavily than borderline p-values; the buffer-sweep coherence (a finding that fires at multiple buffer widths) is itself an informal multiplicity check. Formal correction (Benjamini-Hochberg FDR) is reserved for the follow-up segmentation MD if findings warrant."* Names the issue, sets reader-side weighting, and defers formal correction appropriately for descriptive layer.

4. **Cite specific pharmacokinetic / pharmacodynamic references for the buffer sweep** (closes I2.3 / A7.2 fully). Currently the §4 "Why the buffer sweep matters" paragraph references "Citalopram clinical onset is 2-4 weeks" without citation. Hyttel 1982 (citalopram pharmacokinetics, *Prog Neuropsychopharmacol Biol Psychiatry*) and Marin 2010 (CPAP autonomic effect onset, *Lancet*) close it cleanly. Composes with the queued QUEUED-WORK Tier 3 entry for per-channel literature; consider whether the buffer-justification citations should be in the same lit pass.

5. **Justify the 30/60 asymmetric window** (closes I3.3 carried minor). One sentence in §4 item 2: *"The 30-day pre / 60-day post asymmetry reflects pharmacological reality — citalopram acute effects peak 4-6 weeks post-dose-change so a 60-day post-window covers the clinical-effect window; baseline characterisation needs less time so 30-day pre is sufficient."*

6. **Add the within-subject counterfactual framing explicitly** (closes L2.1 carried minor). One sentence per Daza 2018.

7. **Add the block-bootstrap runtime estimate to §7 status** (closes "Side" computational note). One line: *"Expected runtime: ~10 minutes for the bootstrap × 256 rows × 1000 resamples on standard hardware."*

8. **Cite the specific permutation_null_block_length §X for the 7-day block** (closes "Side" block-length-citation). One inline parenthetical in §4 + one comment line in §6 script.

Items #1-#3 are the high-priority post-v2 residual. Items #4-#8 are tidying and could be batched with the queued lit pass.

## 5. Verdict

**DEFENSIBLE with revision** — substantively up from v1's REVISION RECOMMENDED. The v1's three highest-priority fires (I4.4 recovery-trajectory, I1.x ITS framing, L3.1 autocorrelation) are CLOSED at the caveat or analytical level; the remaining fires are minor (stationarity statement extension, multiplicity-policy sentence) or honestly-deferred (per-channel literature → QUEUED-WORK Tier 3; blinded coding → process change with `no_visible_change` mitigation). The single highest-leverage post-v2 addition is the `mw_p_after_linear_detrend` sensitivity column, which would move A7.4 from "named confound" to "tested confound" with ~30 lines of script. Without it, the MD is honest but the headline confound is caveated rather than tested; with it, the MD's findings are substantively more credible. Recommend adding #1 in §4 above before the script runs in Session C; the rest of §4 (#2–#8) can land post-Session-C as tightening.

---

## Methodology

This methodology review walks CONVENTIONS §2.2 four-input bar plus the applicable items from the 4-layer checklist defined in [README.md](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

Plus the state-of-art literature specific to this methodology question (named in v1's I1 / I2 cells, retained in v2 for traceability):

- **Bernal, Cummins, Gasparrini 2017** *Int J Epidemiol* — ITS state-of-art (now cited in target §1). Material contribution: defines the segmented-regression decomposition the MD's Mann-Whitney U is now explicitly framed as a Layer 1 simplification of.
- **Marin et al. 2010** *Lancet*, **Tantucci et al. 2003** *Chest* — CPAP autonomic effects (queued in target §3).
- **Licht et al. 2010** *Biol Psychiatry*, **Kemp et al. 2010** — SSRI autonomic effects (queued).
- **Wichniak et al. 2017** *Curr Psychiatry Rep* — SSRI sleep architecture (queued).
- **Killick, Fearnhead, Eckley 2012** *JASA* — PELT (now cited in target §1 as corroborating-not-primary).
- **Hyttel 1982** *Prog Neuropsychopharmacol Biol Psychiatry* (or similar) — citalopram pharmacokinetics + steady-state. Surfaced in §4 #4 above as the pharmacokinetic anchor for the buffer choice.

Project-specific audit hooks from [../CONVENTIONS.md](../CONVENTIONS.md) §2.2 (four-input bar), §2.1 / §3 / §4 (discipline gates + audit hooks that apply to methodology choices). Recovery-trajectory confound now anchored in the target's §1 paragraph (closes the v1 substantive fire from [`registry.md`](../analyses/hypotheses/registry.md)).
