# Review: Q24 post-heavy-day trajectory descriptive audit — Stage D Wave 1 (Q24-post-heavy-trajectory)

**Target**: [../analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md](../analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md)
**Target commit**: `0dd38c1` ("research/Q24: Stage D descriptive audit Wave 1 LOCKED r1"); working tree clean at review time.
**Reviewer mode**: Claude (independent peer reviewer per CONVENTIONS §1.2 — fresh session, doc-only knowledge; producer-mode Stage D descriptive audit under §2.1 descriptive-before-inference).
**Review date**: 2026-07-15

---

## 1. What the data shows

The audit executes the Q24 methodology MD (LOCKED r1 2026-07-15, `58b7723`) at Wave 1 scope: combined intensity trigger × strict-clean overlap × both compensatory-success and compensatory-failure pools at +3d/+5d/+10d, ~20 outcomes, raw + trajectory-detrended arms side-by-side, B=10,000 bootstrap, and the §8 four-branch decision-tree per (5 autonomic channels × 3 windows × 2 pools). Empirically:

- **Pool sizes** reproduce the Stage -1 audit byte-identically: 125 / 52 / 12 strict-clean episode-ends at +3d/+5d/+10d, split into compensatory-success 109/43/11 and compensatory-failure 16/9/1. Crash-in-window rate on strict-clean episode-ends is ~2× the corpus baseline at primary windows.
- **Activity-side compensation** is unambiguous (negative-direction AUCs with tight CIs across `total_steps`, `vigorous_min`, `active_min`) but is heavily trajectory-confound-suspect under §7.11 detrending on the success pool.
- **Sleep quantity** shows a compensatory rebound (`sleep_duration_min` +74/+180/+279 min AUC) that largely does NOT survive detrending on the success pool.
- **Autonomic panel** on the success pool is channel-heterogeneous: `stress_mean_sleep` decays at all three windows (BOTH-decay), `hr_median_waking` and `sleep_hr_avg_spo2` show delayed-decay (ONLY-subjective at +3d → BOTH-decay at +5d/+10d), `bb_lowest` and `all_day_stress_avg` show sustained autonomic sign-inversion in raw AUC that mostly evaporates under detrending.
- **Compensatory-failure sub-arm** subjective channel is sustained at every window (does NOT decay) while success pool subjective decays everywhere; failure-pool subjective AUC is ~8× the success-pool magnitude at +3d.
- **Load-bearing quantitative headline**: 44 of 118 (outcome × window × pool) cells are XOR-detrend-fragile; the audit reports "7 cells" where raw AND detrended AUC CIs both exclude zero, and frames these as the trajectory-confound-*surviving* set worth Stage H prioritisation.

The interpretive frame is disciplined caveat-class throughout; the author consistently distinguishes descriptive verdicts from mechanistic imputations and flags the compensatory-failure vs compensatory-success subjective contrast as inheriting some crash-definition circularity by construction.

---

## 2. What fired and why

### Layer 1 — Universal reporting (inherits from SCRIBE 2016, STROBE 2007)

- **[L1.4 — enumerated confounders — SCRIBE Item 22 / STROBE Item 12] — passes (see §3).** No fire.

- **[L1.5 — limitations stated separately from results — SCRIBE Item 22 / STROBE Item 19] — minor.** §10 "open inputs surfaced for orchestrator review" mixes producer-mode operational ambiguities (item 1: n=1 bootstrap cosmetic; item 5: detrend n-loss confirmation) with substantive interpretive concerns (item 2: sign-inversion two-candidate-readings; item 3: circularity caveat on failure-pool subjective). A cleaner separation between "operational refinement candidates" and "interpretive concerns needing orchestrator disposition" would strengthen the report — the current §10 mixes both classes and risks the substantive items being read as merely cosmetic. *Magnitude*: minor (framing, not substance).

### Layer 2 — Observational n=1 (inherits from Daza 2018, Personal Science)

- **[L2.2 — stationarity assumption — Daza 2018 §3.2] — substantive.** The audit inherits from Q24 MD §10 caveat 8 the envelope-drift-asymmetry concern, and correctly flags 8 detrend-surfacing failure-pool cells as an era-imbalance signal (§6.2 read). However, the era-stratified comparator sensitivity arm that Q24 MD §10 item 8 explicitly names ("restrict matched-ordinary comparator to same-era days as the heavy-episode") is not run in Wave 1 — it is only mentioned as a Wave 2 candidate (§9 caveat 8 row). Given that §6 shows 44 of 118 cells are XOR-detrend-fragile — i.e., envelope-drift is empirically load-bearing on this Wave 1 corpus — the era-stratified sensitivity arm is doing more work than the §9 caveat table suggests. Naming it as a *finding-specific* companion for the 7 trajectory-confound-surviving cells (rather than a generic Wave 2 candidate) would sharpen the discipline. *Magnitude*: substantive (the caveat's escalation-to-finding threshold per Q24 MD §10 item 8 arguably fires, but the audit reports it at caveat-class only).

- **[L2.5 — held-out structure framing — memory `project_garmin_research_bias_boundary`] — no fire.** The audit does not invoke a held-out era or a train/validate split; it is a producer-mode descriptive execution of a locked operand. Not applicable.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

- **[L3.1 — autocorrelation — Natesan Batley 2023 headline (83.8% ignore)] — passes with caveat (see §3).** The Q24 MD §7.10 bootstrap block-length choice is documented and inherited; block length = 1 per-episode resampling is defensible under strict-clean episode independence. No fire on Wave 1 scope.

- **[L3.3 — multiplicity across cells — Natesan Batley 2023 + Q24 MD §7.10] — substantive.** The audit reports 236 rows in `trajectory_summary.csv` (raw + detrended arms across ~20 outcomes × 3 windows × 2 pools) with no multiplicity correction, per Q24 MD §7.10 explicit "descriptive-only at Stage D; no correction". This is defensible pre-lock, but the audit's *reading* of the results uses the shorthand "bold AUC = bootstrap 95% CI excludes zero" (§4 reading convention) as a descriptive marker for every headline cell in the tables. At 43 raw-sig cells out of 118, the expected null-hypothesis false-positive rate under independent tests at α=0.05 would be ~6 cells — the audit's ~36% raw-sig rate is well above that, but the "bold marker" framing across each of §4.1-§4.6 subtly invites treating the boldface as evidence per cell. One sentence per subsection reiterating "descriptive-only marker; not corrected across the 236-row grid" would prevent the boldface from doing inferential work. *Magnitude*: substantive (framing risk given the 236-cell grid).

- **[L3.5 — trend/trajectory claim separated from level/cross-sectional claim — CONVENTIONS §4.2 / WWC 2022] — substantive.** The §5 decision-tree branch verdicts are computed on the RAW arm per §8.1 (as the audit correctly documents in §10 item 6). But the §5 subsection §5.1 reads the branches as substantive descriptive findings ("`stress_mean_sleep` decays at all three windows — most literature-concordant panel per Radin/Germain two-clock reading") *without* noting that 4 of the 5 autonomic channels on the success pool have raw-only-significant AUCs (§6.1 detrend-erasing set). The `stress_mean_sleep` +3d/+5d/+10d BOTH-decay verdict, for example, is computed on a raw trajectory where the +5d AUC CI excludes zero on the negative-inversion side but the detrended CI does not — meaning the BOTH-decay verdict may partly reflect envelope drift, not event-triggered decay. The audit reads the branch verdicts as if they were independent of the §6 detrend fragility, but they use the same raw-arm delta trajectory that §6 flags as fragile. Recommendation: annotate each branch verdict cell in §5.1 tables with the corresponding §6 detrend-fragility flag. *Magnitude*: substantive (branch verdicts inherit detrend fragility).

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3, §4)

- **[L4.7 — caveat-class framing kept, a-priori-class framing cut — CONVENTIONS §4.2] — passes (see §3).** No fire.

- **[L4.8 — prior-driven hypothesis framed as confirmatory — CONVENTIONS §4.3] — no fire.** The audit is producer-mode descriptive; hypothesis framing is deferred to Stage H per Q24 MD §1.2.

- **[L4.9 — operationalisation faithful to data — CONVENTIONS §3.10] — substantive.** The **"7 trajectory-confound-surviving cells" claim in §6.3** is arithmetically 15 (detrend-sig) − 8 (det-only-sig) = 7, but this arithmetic silently assumes that every "both raw+detrend sig" cell is a survivor. Empirical verification of the output CSV shows that **only 5 of the 7 have same-sign raw and detrend AUC**; the remaining **2 cells are sign-flippers**: `effective_exertion_min` at +3d success (raw AUC +3.55 [+0.25, +7.17]; detrend AUC **−6.49** [−12.88, −0.47]) and `spo2_avg_sleep` at +3d failure (raw AUC +1.01; detrend AUC −1.36). A sign-flip under detrending is a *stronger* caveat than a null detrend — the sign of the effect inverts when envelope drift is removed. The audit §4.1 does obliquely acknowledge the `effective_exertion_min` "nuanced story" as a "definitional-pair signal (§6.1 discipline)" but does not connect it to the §6.3 headline "7 cells worth prioritising for Stage H pre-reg drafting". The 7-cell figure is load-bearing for downstream Stage H triage — if the parent orchestrator or a downstream pre-reg author reads "7 survivors" as the trajectory-confound-surviving prioritisation set, two of those seven will lead to Stage H pre-regs on cells whose sign inverts under the more defensible reading. *Magnitude*: **substantive-to-blocking** for downstream Stage H seed selection; recommend §6.3 revise the count to "**5 sign-consistent survivors + 2 sign-flip cells** (the latter constitute stronger caveats, not survivors)".

- **[L4.9 — operationalisation faithful to data — CONVENTIONS §3.10] — substantive.** The audit tables in §4.1-§4.6 report an **n_c column that materially undercounts the actual comparator pool sizes emitted by the script**. Sampled discrepancies (audit.md value vs `trajectory_summary.csv` `n_comparator_days` at +3d compensatory-success):
  - `total_steps`: audit.md n_c=145; CSV=308.
  - `effective_exertion_min`: audit.md n_c=148; CSV=327.
  - `hr_median_waking`: audit.md n_c=148; CSV=308.
  - `sleep_duration_min`: audit.md n_c=133; CSV=296.
  - `gevoelscore`: audit.md n_c=118; CSV=242.

  The audit.md n_c figures are systematically ~2× smaller than the actual comparator-pool sizes. §8's coverage table ("comparator pool sizes range from ~120 to ~148 at +3d") reproduces the same undercount, so this is not a table-typo but an internal-consistency error carried across §4-§8. The pool-size-CSV `compensatory_pool_sizes.csv` and the trigger-arm n_t values match audit.md exactly, so the discrepancy is comparator-side only. The bootstrap-CI values in §4 tables DO reproduce the CSV — so the *analysis* used the correct 308-day comparator pool and the numeric AUC/CI findings are unaffected, but the *reported* comparator sample size is wrong. If a downstream reader uses the audit.md n_c figures to reason about statistical power (e.g., "at +3d success, effective sample is 109 trigger + 148 comparator = 257 unit-days"), the reasoning will be off by a factor of ~2. *Magnitude*: substantive (numerical reporting inaccuracy; corrigible by re-generating the tables from the CSV).

### Side observations

- **Side** — §10 item 6 correctly flags that Q24 MD §8.1 does not explicitly say "raw or detrended" for the decay screen input, and the audit reads it as raw with an explicit interpretive-extension flag for orchestrator review. This is exemplary transparency about a real methodology-MD ambiguity — a good instance of the §1.2 role-split working as intended. No fire.

- **Side** — §7.1 states "the failure-pool AUC being ~8× larger than success-pool AUC is partly definitional" — the circularity caveat is correctly surfaced. This is a load-bearing acknowledgement (see Section 4 recommendations).

- **Side** — §5.2 compensatory-failure branch verdicts at +10d are computed on n=1 and correctly flagged NOT DEFENSIBLE, but the audit still emits the branch rows into `branch_verdicts.csv` (n=1 rows produce degenerate zero-width CIs). §10 item 1 acknowledges this as a "minor cosmetic issue" — fine.

- **Side** — §9 confound-status table describes caveats 4 (deconditioning) and 8 (envelope-drift) as "RELEVANT" but only caveat 8 gets a concrete Wave 2 companion suggestion. Caveat 4's status ("PARTIALLY RELEVANT — the compensatory-success pool's autonomic sign-inversion may partly reflect a floor effect") does not point at a specific sensitivity arm. If the sign-inversion pattern is load-bearing, caveat 4 deserves a concrete Wave 2 escalation candidate too.

- **Side** — §11 cross-refs correctly cite `bout_level_recovery_dynamics.md` as sister structural precedent but do not cite HA-C4c/HA-C4cp precedent, though Q24 MD §1.4 explicitly names those hypotheses as siblings using the same heavy-day trigger. A one-line cross-ref would connect the Stage D read to the parallel bout-level Garmin-stress recovery evidence.

---

## 3. What does not fire (selective)

Non-trivial passes worth naming:

- **L1.4 (enumerated confounders) passes with §9's 8-row confound table** — each caveat is walked with a RELEVANT / STRUCTURAL / PARTIALLY RELEVANT status; the framing separates caveats that Wave 1 evidence bears on from caveats that are structural to the Wave 1 scope. This is textbook Layer 1 discipline.

- **L3.1 (autocorrelation) passes with documented block-length choice** — Q24 MD §7.10's block-length=1 rationale (strict-clean episode-ends approximately independent given multi-week separation) is inherited and executed faithfully. The audit does not silently i.i.d.-assume; the bootstrap resampling scheme is specified.

- **L4.1 (personal baseline) passes non-trivially** — the heavy-day trigger uses `_lagged_lcera` (personal-baseline anchored) and the audit correctly notes in §9 caveat 3 that "envelope drift is precisely what §7.11 detrending addresses". The audit does not silently mix `_lagged_lcera` and non-lagged variants.

- **L4.2 (`_lagged_lcera` for PEM hypotheses on LC frame) passes** — the trigger operand is v3.2 `_lagged_lcera` throughout; no v3.1 columns silently appear.

- **L4.3 (one column per definitional pair) passes with the sleep-architecture handling** — §4.2 reports `sleep_duration_min` + the four architecture stages side-by-side without inflating them into independent tests; `sleep_efficiency_tib` (canonical) sits alongside `sleep_efficiency_staged` (sensitivity) exactly per Q24 MD §6.2.

- **L4.7 (caveat-class framing) passes non-trivially with §7.1's circularity acknowledgement** — the audit explicitly names the crash-definition circularity in the failure-pool subjective magnitude comparison BEFORE surfacing the pool-contrast finding, not after. This is caveat-first framing, not caveat-hedging-after-a-finding.

- **§10 open-inputs discipline passes as a producer-mode-transparency pattern** — surfacing four "interpretive extensions" for orchestrator review (§8 branches on raw only; §7.9 first-crossing operationalisation; sub-arm bootstrap at n<10; sparse×sparse handling) is exactly the §1.2 role-split surface-boundary work. The reader can see where the subagent made a defensible reading vs where the methodology MD is silent.

---

## 4. What would strengthen this finding

Concrete, named, with expected effect:

1. **§6.3 revision: split "7 cells" into "5 sign-consistent survivors + 2 sign-flip cells".** The current arithmetic (15 − 8 = 7) conflates two categorically different outcomes. Sign-flip cells under detrending are stronger caveats than null-detrend cells, not survivors. Add the explicit list: `effective_exertion_min` +3d success and `spo2_avg_sleep` +3d failure are sign-flippers; the 5 sign-consistent survivors are `total_steps` +3d failure, `sleep_awake_min` +3d failure, `sleep_efficiency_tib` +3d failure, `gevoelscore` +3d failure, `gevoelscore` +5d failure. **Inherits**: CONVENTIONS §3.10 operationalisation-faithful-to-data + §4.2 caveat-class discipline. **Expected effect**: closes L4.9 substantive fire; if Stage H pre-registration authors use the survivor list as a triage seed, they will not draft pre-regs on cells whose sign inverts under the more defensible reading. Notice also that 4 of the 5 sign-consistent survivors are on the compensatory-failure sub-arm at +3d — this concentration is itself descriptively substantive.

2. **§4-§8 revision: correct the n_c comparator-pool figures throughout.** The audit's n_c column undercounts the actual comparator pool by ~2× consistently. Regenerate the tables from `trajectory_summary.csv` `n_comparator_days` directly, and update §8 coverage-table's "comparator pool sizes range from ~120 to ~148" text to the actual ranges from the CSV. **Inherits**: CONVENTIONS §3.6 named counts + §3.10 operationalisation-faithful-to-data. **Expected effect**: closes the second L4.9 substantive fire; ensures downstream statistical-power reasoning is anchored to the correct pool sizes.

3. **§5.1 revision: annotate branch verdicts with the corresponding §6 detrend-fragility flag.** For each row of the §5.1 branch matrix, add a column or footnote indicating whether the underlying delta trajectory is XOR-detrend-fragile on the (channel × window × success-pool) cell. The BOTH-decay verdicts on `stress_mean_sleep`, `hr_median_waking`, and `sleep_hr_avg_spo2` should carry the fragility annotation where §6.1 flags them, so the branch-verdict reader can immediately see which decay verdicts are running on trajectories that don't survive detrending. **Inherits**: L3.5 level-vs-trend + Q24 MD §7.11 escalation rule. **Expected effect**: closes L3.5 substantive fire; prevents §5 branch verdicts from being read as independent of §6 fragility.

4. **§4 revision: add a one-sentence reminder in each table subsection that "bold AUC" is a descriptive-only marker with no multiplicity correction across the 236-row grid.** The current §4 reading convention notes it once at the top but the boldface is doing implicit inferential work by every subsequent table. **Inherits**: Q24 MD §7.10 no-inferential-tests-at-Stage-D + Natesan Batley 2023 multiplicity discipline. **Expected effect**: closes L3.3 substantive fire; prevents boldface from doing multiplicity-uncorrected inferential work.

5. **§9 caveat 8 revision: escalate the era-stratified comparator sensitivity arm from "Wave 2 candidate" to a Wave 2 pre-requisite for any of the 5 sign-consistent survivors' Stage H pre-reg draft.** Given that 44 of 118 cells are XOR-detrend-fragile (§6 headline) and Q24 MD §10 item 8 explicitly names era-stratification as the concrete companion when envelope-drift is empirically load-bearing, the current "Wave 2 candidate" framing understates the discipline the finding-set warrants. **Inherits**: L2.2 stationarity + Q24 MD §10 item 8. **Expected effect**: closes L2.2 substantive fire; ties the era-stratified companion arm to the specific survivor cells rather than to generic Wave 2 scope.

6. **§10 revision: separate "operational refinements" (items 1, 4, 5) from "interpretive concerns needing user disposition" (items 2, 3, 6, 7).** The current mix risks the substantive items being read as cosmetic. Two subsections with different headers would clarify. **Inherits**: L1.5 SCRIBE limitations-separated-from-results. **Expected effect**: closes L1.5 minor fire; makes orchestrator triage easier.

7. **§7.1 revision (optional): pre-commit the matched-subjective-baseline sensitivity arm for the pool-contrast comparison, either as Wave 2 scope or with a rationale for why it is out-of-scope.** The current audit surfaces the circularity caveat cleanly but leaves the disposition question open ("worth surfacing for Wave 2 orchestrator review: whether a matched-subjective-decay-magnitude comparator would meaningfully change the failure-vs-success magnitude ratio"). Given the failure-pool subjective contrast is described as "the load-bearing empirical anchor for the Q24.5 sub-part interpretation" (§5.2), the sensitivity-arm decision is load-bearing for how much interpretive weight the pool-contrast finding can carry. **Inherits**: CONVENTIONS §4.2 caveat-class discipline; Q24 MD §3.5 no-pre-registered-inferential-test. **Expected effect**: closes an open reader-facing ambiguity about interpretive weight of the pool-contrast headline.

---

## 5. Verdict

**PASS with caveats** — the audit executes the Q24 MD LOCKED r1 operand faithfully and the substantive descriptive findings (44 XOR-fragile cells, channel-heterogeneous decay pattern, pool-contrast on subjective with circularity acknowledged) are load-bearing and defensible, but two Layer 4 substantive fires (§6.3's "7 cells" arithmetic conflates 5 sign-consistent survivors with 2 sign-flip cells, and §4-§8's n_c column undercounts comparator pools by ~2×) require correction before the survivor cell list is used as Stage H pre-reg seed, and one Layer 3 substantive fire (§5 branch verdicts inherit §6 detrend fragility unannotated) warrants annotation before the branch matrix is read as independent evidence.

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

Empirical verification of load-bearing claims in the target: pool sizes cross-checked against `output/compensatory_pool_sizes.csv` (byte-identical to Stage -1 audit §5 clean totals); §5 branch verdicts cross-checked against `output/branch_verdicts.csv` (matches); §4.1-§4.6 AUC/CI values sampled across activity, sleep, autonomic, subjective outcomes against `output/trajectory_summary.csv` (all sampled values match); §6 detrend-fragility cell counts (44 XOR = 36 raw-only + 8 detrend-only) reproduced from CSV; §6.3 "7 survivors" arithmetic reproduced but recomposed into 5 sign-consistent + 2 sign-flip via CSV walkthrough. Audit script (`scripts/audit.py`) + detrend helper (`scripts/detrend.py`) inspected for methodology-MD conformance across pool construction (§3.5), comparator conditions (§4.1), bootstrap parameters (§7.10), decay-screen operationalisation (§8.1), and detrend rules (§7.11).
