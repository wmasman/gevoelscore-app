# Post-heavy-day pacing learning: phase-stratified trajectories and dose-response compensation, operand definition

*Producer-mode methodology MD per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). Drafted 2026-07-16 as r1; LOCKED r1 2026-07-16 post-review absorption per [`docs/research/reviews/methodology-post_heavy_day_pacing_learning-2026-07-16.md`](../reviews/methodology-post_heavy_day_pacing_learning-2026-07-16.md).*

---

## Authorship

**Drafted 2026-07-16** by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem. Subagent-drafted per user delegation; fresh-session `/research-methodology-review` before lock is the discipline mirror to the parent MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md).

**Drafting trigger**: Wave 1 Stage D descriptive audit ([`analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md`](../analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md) LOCKED r4 commit `b9ffcc5`) surfaced **36 raw-only-significant cells on the compensatory-success pool** whose signal did not survive `linear_detrend_on_pre` per parent Q24 MD §7.11. Per Stage D audit §9.1 caveat 9 (r2 user-endorsed 2026-07-15), those cells are **drift-entangled** rather than dismissible artefacts: the linear detrend on a 4-year LC-era corpus removes disease natural history, citalopram modulation, deconditioning, aging, seasonality, AND the pacing-learning drift Q24 sub-part 3 was designed to characterise. Sub-part 3 is the **design-level disambiguator** of that drift decomposition. This MD locks the sub-part 3 operand; a companion dose-response arc is co-located because both are trajectory-based outcome tests that inherit the parent Q24 MD machinery and share design constraints.

**Sister MD split rationale**: sub-part 3 (phase-stratified pacing) + dose-response (severity-scaling of compensation magnitude) both operate on trajectory-magnitude outcomes across heavy-episode-ends. The predictive-categorical outcomes — Q24 sub-part 5 (does resting prevent crashes?) and the streak-→-crash tests — use structurally different machinery (predictive-categorical, not trajectory-comparative) and are covered by the sister MD [`heavy_day_crash_risk_prediction.md`](heavy_day_crash_risk_prediction.md) (drafted in parallel; sub-part 5 + streak-→-crash arc).

**Status**: **LOCKED r1 2026-07-16 post-review absorption.** Producer-mode artefact per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations); fresh-session methodology review absorbed inline from [`docs/research/reviews/methodology-post_heavy_day_pacing_learning-2026-07-16.md`](../reviews/methodology-post_heavy_day_pacing_learning-2026-07-16.md) (DEFENSIBLE with revision). Stage D descriptive audit for sub-part 3 + dose-response now unblocked against this LOCKED r1 operand.

---

## 1. Purpose and scope

### 1.1 What this MD is

An **operand definition** for two trajectory-based sub-arcs of Q24 post-heavy-day analysis on per-day aggregates (`per_day_master.csv`, LC-era stratum):

1. **Q24 sub-part 3 — phase-stratified pacing** (§3). Reads whether post-heavy activity trajectory magnitude changes across the participant's four LC recovery phases (`lc_pre_ergo` → `pacing_pre_citalopram_learning` → `pacing_habit_established` → `citalopram_modulated`). The phase axis is the pre-committed disambiguation lever for the Stage D Wave 1 §9.1 caveat 9 drift-entanglement finding.

2. **Dose-response pacing** (§4). Reads whether trajectory magnitude scales with trigger intensity (very_heavy vs heavy), operationalising the severity-scaling prediction from Van Campen 2020 on the n=1 corpus.

Both arcs inherit their unit-of-analysis, comparator, windows, overlap-policy, pool-split, trajectory-summary-statistics, detrend method, bootstrap/multiplicity policy, and zero-vs-NaN discipline **verbatim from the parent Q24 MD** [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1 (commit `58b7723`, 555 lines). This MD extends the parent by adding stratification axes on top; it does NOT re-derive any inherited machinery.

### 1.2 What this MD is NOT

- **NOT the parent Q24 MD.** Sub-parts 1 (activity trajectory) and 4 (sleep + autonomic) plus the subjective paired channel live in the parent MD. See parent §1.3 for the full sub-part table.
- **NOT a pre-registration.** No falsifier or Stage H inferential test is locked here. Direction pre-commits (§3.4, §4.4) are the reading axis per parent MD §7.7 discipline; opposite-direction findings are sign-inversion findings in their own right per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no).
- **NOT the predictive-categorical arc.** Sub-part 5 (compensatory success as a counterfactual predictor of crash avoidance) and the consecutive-streak-→-crash tests are structurally distinct (predictive-categorical, not trajectory-comparative). Those live in the sister MD [`heavy_day_crash_risk_prediction.md`](heavy_day_crash_risk_prediction.md).
- **NOT a citalopram-vs-pacing-learning identification.** §3.6 confounds pre-commit acknowledges that `citalopram_modulated` phase temporally coincides with citalopram onset (2024-04-09) and is fully non-overlapping with the three pre-citalopram phases. Disentangling learned-pacing from citalopram-modulation on n=1 requires additional design (e.g. a citalopram-stratified companion arm on a naturalistic subset that predates 2024-04-09, or a within-`citalopram_modulated` post-hoc phase re-split). Not resolved in this MD; noted as caveat.
- **NOT a within-day shape analysis.** Q24 sub-part 2 (within-day activity shape) stays blocked on per-minute Garmin extraction, per parent MD §1.2.

### 1.3 Trigger for this MD

Wave 1 Stage D findings on parent Q24 MD detected 36 raw-significant cells that did not survive `linear_detrend_on_pre` (Stage D audit §6.1). The Wave 1 → sub-part 3 disambiguation link is the explicit exit condition from that fragility set: **if compensation trajectory magnitude strengthens across LC recovery phases, at least some of the drift that Wave 1 detrended out is the pacing-learning signal Q24 sub-part 3 was designed to characterise.** The 36-cell set is therefore not dismissible; it passes to sub-part 3 as candidate signal, and this MD locks the operand that will discriminate.

Stage D audit §10 item 8 (r4 pickup flag) additionally surfaces a corpus-general **level-vs-change disagreement** framing that applies here: when a raw AUC and detrended AUC disagree AND pre-episode slopes are statistically indistinguishable but pre-episode absolute levels differ substantially, the observation is a genuine level-vs-change ambiguity rather than a drift-artefact. Sub-part 3 phase-stratification does not resolve level-vs-change disagreements on its own, but it does provide a phase-conditional read of each channel's level+change trajectory that is downstream-interpretable at Stage S1 (internal synthesis).

---

## 2. Inherited design (pointers to parent Q24 MD)

All machinery below is inherited verbatim from parent [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md); this MD does NOT re-derive any of it.

| Design element | Parent MD section | Inherited value |
|---|---|---|
| Stratum | §2 | LC-era only (`lc_phase == 'lc'`, `date >= 2022-04-04`, n=1524 rows) |
| Heavy-day definition | §2.2 | `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` (top ~25% of participant's lagged [d-90, d-30] LC-era baseline on 4-axis composite `exertion_rank_composite_lagged_lcera`) |
| Unit of analysis | §3.1 | Episode-end (gap=0 contiguous); per-heavy-day as sensitivity per §3.3 |
| Comparator | §4 | Matched-ordinary: not heavy in [D, D+w] + no crash in [D, D+w] + valid outcome across window; recomputed per outcome (§4.2) |
| Windows | §5.1 | Primary 3d + 5d; extended 10d; 14d dropped |
| Overlap policy | §5.2 | Both strict-clean + inclusive reported side-by-side at all windows |
| Pool split | §3.5 | Compensatory-success (no crash in [+1, +w]) primary + compensatory-failure sub-arm side-by-side |
| Trajectory summary stats | §7.1-§7.9 | Nine stats per (outcome × window × overlap × stratum): per-d+k mean±CI, delta vector, AUC, slope, peak-location, RTBT, below-baseline count, variability, first-crossing |
| Trajectory detrend | §7.11 | `linear_detrend_on_pre` per-episode 30d pre-window linear extrapolation subtracted from both trigger and comparator arms; raw + detrended reported side-by-side |
| Bootstrap + multiplicity | §7.10 | B=10,000 per-episode block-length-1 for strict overlap; block length ≥ w for inclusive; Stage D descriptive-only, no multiplicity correction |
| Zero-vs-NaN | §11 | Never `.fillna(0)` on outcome trajectories; missing = uninstrumented, not zero |
| Confounds | §10 | 8 pre-committed caveats; §3.6 + §4.6 below layer sub-part 3 + dose-response specific caveats on top |

**No re-derivation rule**: Stage D reviewers finding this MD should verify inheritance-only status against parent MD hashes (parent commit `58b7723` at drafting time); any inherited-machinery change requires opening the parent MD, not this one.

---

## 3. Sub-part 3: Phase-stratified pacing

### 3.1 Phase axis

**Primary axis: `recovery_phase`** — the project-schema categorical variable with four locked buckets, per [`analyses/hypotheses/registry.md`](../analyses/hypotheses/registry.md) and consolidator [`pipeline/03_consolidate/build_unified_dataset.py`](../pipeline/03_consolidate/build_unified_dataset.py):

| Phase | Date range | LC-era days | Heavy-episode-ends (gap=0, combined) |
|---|---|---:|---:|
| `lc_pre_ergo` | 2022-04-04 → 2022-09-21 | 171 | **19** |
| `pacing_pre_citalopram_learning` | 2022-09-22 → 2022-11-16 | 56 | **12** |
| `pacing_habit_established` | 2022-11-17 → 2024-04-08 | 509 | **125** |
| `citalopram_modulated` | 2024-04-09 → 2026-06-05 | 788 | **158** |
| **All LC-era** | 2022-04-04 → 2026-06-05 | **1524** | **314** |

Source: probe against `per_day_master.csv` 2026-07-16; matches parent Stage -1 audit §2 phase-level day counts and §4 combined-episode gap=0 total (314).

**Sensitivity axis: calendar year** (5 buckets, 2022-2026). Reveals within-phase variation that the four-bucket schema collapses (e.g. `citalopram_modulated` spans 2024Q2 through 2026Q2, a ~2-year window across which the participant's compensatory behaviour may have continued to evolve independently of citalopram onset). Year distribution of heavy-episode-ends per audit + probe:

| Year | Heavy-episode-ends |
|---|---:|
| 2022 (partial Apr-Dec) | 44 |
| 2023 | 87 |
| 2024 | 81 |
| 2025 | 66 |
| 2026 (partial Jan-Jun) | 36 |

### 3.2 Outcome operand family

Verbatim from parent Q24 MD §6.1 activity axes:

| Column | Notes |
|---|---|
| `total_steps` | Garmin daily step count |
| `effective_exertion_min` | Composite exertion in minutes (primary activity axis) |
| `vigorous_min` | Minutes above vigorous-intensity threshold |
| `active_sec / 60` (`active_min`) | Total active seconds normalised to minutes |
| `exertion_class_lagged_lcera` at d+k | Categorical class distribution + prob(heavy at d+k) |

The sleep + autonomic outcome family (parent §6.2) and the subjective channel (parent §6.3) are **out of primary scope for §3**. Sub-part 3 is the pacing-learning arc, and pacing behaviour is directly measured on the activity axes. Sleep + autonomic + subjective channels may be added as descriptive companion reads at Stage D per orchestrator disposition; they do not participate in the primary sub-part 3 contrast pre-commit here.

### 3.3 Primary contrast: trajectory magnitude across phases

For each `(outcome operand, window, overlap-policy)` cell inherited from parent MD, compute:

**Per-phase trajectory summary** (from parent MD §7.1-§7.9): mean±CI per d+k, delta vector `Δ_phase(k) = mean_heavy_phase(d+k) - mean_matched_ordinary_phase(d+k)`, AUC, slope, peak-location, RTBT, below-baseline day count, trajectory variability, first-crossing day. Each phase's trajectory is read against its **own phase-stratified matched-ordinary comparator pool** — the matched-ordinary definition (parent §4.1) applies within-phase, so a heavy-episode-end in `pacing_habit_established` is contrasted against the matched-ordinary comparator pool drawn only from `pacing_habit_established` days.

**Cross-phase contrast** (the sub-part 3 headline read): for each `(outcome, window, overlap)` cell, report per-phase AUC + slope + peak-location + RTBT stacked as a four-row per-phase panel. Primary contrast is the AUC/slope difference between the **late-phase pair** (`pacing_habit_established` + `citalopram_modulated`) and the **early-phase pair** (`lc_pre_ergo` + `pacing_pre_citalopram_learning`). Each phase reads on its own phase-stratified matched-ordinary comparator; the contrast is between per-phase AUC values, not between raw heavy-arm activity levels (which would confound the absolute activity envelope with the compensatory drop).

**Sample-size warning up front**: the two early phases have small heavy-episode-end pools (n=19 + n=12 = 31 episode-ends combined; strict-clean sub-samples per parent §5.1 will be smaller at +5d and +10d). Descriptive-with-CI reads only at extended windows; the two late phases (n=125 + n=158 = 283 combined) support the parent MD's full trajectory-summary machinery at all windows. Per-phase per-window valid-episode counts must be reported at §7 audit hooks; cells with n_valid < 10 at any window drop from bootstrap-CI reads and are flagged descriptively per parent MD §7.10 practice.

### 3.4 Direction pre-commit

**Learned-pacing hypothesis**: as the participant learns to pace, the compensatory activity drop following a heavy episode should **strengthen over time**. Operationally this means later-phase AUC magnitude on activity outcomes should exceed earlier-phase AUC magnitude, with direction per parent MD §7.7:

- `total_steps`, `effective_exertion_min`, `vigorous_min`, `active_min`: pre-committed direction on the compensatory-success pool is **negative** (fewer steps/exertion/vigorous-minutes/active-time than phase-matched-ordinary comparator). **Sub-part 3 pre-commit**: `|AUC_late_phase| > |AUC_early_phase|` on activity outcomes indicates strengthening compensatory-drop magnitude (below-baseline-steps-after-heavy grows over time).
- `exertion_class_lagged_lcera` at d+k: pre-committed direction is that prob(heavy at d+k | heavy-episode-end at D) drops below phase-matched-ordinary prob(heavy at d+k). **Sub-part 3 pre-commit**: the drop widens in later phases (participant more successfully avoids clustering heavy days after a heavy episode).

**Opposite-direction findings are sign-inversion findings in their own right** (parent §7.7 discipline). A finding that early-phase compensation magnitude EXCEEDS late-phase compensation magnitude on activity would falsify the naive learned-pacing reading and would need a distinct interpretation (e.g. early-phase compensation was forced by symptom severity + hard limits; late-phase compensation is voluntary + calibrated + closer to phase-matched-ordinary baseline because the participant's absolute activity envelope shifted). Report as sign-inversion; do not silently invert the reading direction.

**Literature anchor for the direction pre-commit**: the "compensatory drop strengthens over time" reading is grounded in the ME/CFS + Long COVID pacing literature. **Goudsmit et al. 2012** on the envelope-theory / pacing framework (activity within the sustainable envelope prevents PEM). **Nijs et al. 2013** on activity self-regulation adaptation over time in CFS. **Sanal-Hayes et al. 2023** on pacing effectiveness in Long COVID. Citation status: these anchors are flagged as citation-status-deferred at [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) (not yet fetched into `docs/research/literature/`). Naming them here converts the §3.4 direction pre-commit from first-principles reasoning to confirmatory-of-established-literature framing per [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory).

### 3.5 Discipline: disambiguating the 36 drift-entangled cells

The design-level exit from Stage D §9.1 caveat 9 drift-entanglement:

**Rescue subset**: any raw-only-significant cell in Stage D §6.1 whose per-phase read shows **monotone (or near-monotone) strengthening of AUC magnitude across the four phases in the pre-committed §3.4 direction** is a candidate for reclassification from *nuisance-drift* to *compensatory-behaviour-improvement-drift*. The rescue is descriptive-only at Stage D; no formal cross-phase inferential test is pre-committed here. If a rescue-candidate cell also satisfies parent MD §7.11 detrended-arm significance within-phase (per-phase per-arm detrend read), the sub-part 3 evidence is stronger; if the within-phase detrended read collapses in every phase but the cross-phase AUC-magnitude trend is monotone, the reading is that the drift being detrended out at the corpus level IS the pacing-learning signal (which the per-phase detrend then removes twice-over).

**Non-rescue subset**: any raw-only-significant cell whose per-phase read shows **flat AUC magnitude across phases** (no cross-phase trend) or **reversed direction** (early-phase AUC magnitude exceeds late-phase AUC magnitude) is not rescued by sub-part 3. Such cells stay in the drift-entangled pile as *nuisance-drift-dominated* candidates for Stage H-level disposition, per parent MD §7.11 escalation rule.

**Rescue metric (mechanically reproducible)**: to make the rescue call reproducible across analysts, compute two per-cell diagnostics on the ordered four-phase axis (`lc_pre_ergo` < `pacing_pre_citalopram_learning` < `pacing_habit_established` < `citalopram_modulated`):

- **Spearman ρ of |AUC| on the 4-phase ordinal axis**. Thresholds: ρ ≥ +0.50 = rescue-eligible; +0.20 ≤ ρ < +0.50 = weak signal (flag but do not rescue); ρ < +0.20 = no rescue.
- **Monotonicity-score** = fraction of consecutive-phase-pair |AUC| increases (denominator = 3). Sensitivity companion. 3/3 = perfect monotone; 2/3 = one violation (still rescue-eligible if ρ ≥ +0.50); ≤1/3 = no rescue.

Report both statistics per cell. Wide CIs on early-phase per-phase |AUC| (n=19 + n=12 pools per §3.3) may inflate rank instability; interpret the ρ threshold as descriptive marker not verdict per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference).

**Corpus-general level-vs-change framing** (Stage D audit §10 item 8, r4 pickup): sub-part 3 per-phase reads are per-arm AUC contrasts (`Δ_phase(k) = mean_heavy_phase(d+k) - mean_matched_ordinary_phase(d+k)`), which read the change-from-phase-matched-comparator on absolute-level terms. The Wave 1 `effective_exertion_min` +3d success sign-flipper (Stage D §6.4.1) was a corpus-level level-vs-change disagreement where trigger arm pre-window baseline was ~55% higher than comparator pre-window baseline. Sub-part 3 does not resolve the level-vs-change disagreement per se, but a phase-stratified read of that cell reveals whether the pre-episode level offset itself changes across phases (which would be informative about whether the participant's absolute activity envelope on days-preceding-heavy shifts across phases). Report per-phase pre-window mean levels alongside AUC magnitudes; do not silently compress.

### 3.6 Confound pre-commit: the citalopram entanglement

**Locked descriptive finding** (probe against `per_day_master.csv` 2026-07-16): `recovery_phase == 'citalopram_modulated'` is **fully non-overlapping** with the three pre-citalopram phases. The `citalopram_modulated` bucket starts exactly 2024-04-09 (citalopram onset), and the `pacing_habit_established` bucket ends exactly 2024-04-08. All 158 heavy-episode-ends in the `citalopram_modulated` bucket are also post-citalopram-onset (n=158 in that phase × 158 post-onset = 158, cross-tab confirmed).

**This is a 100% temporal confound.** Any late-phase-vs-early-phase contrast on the `recovery_phase` axis conflates:

- Learned-pacing (behavioural change) across the participant's LC recovery
- Citalopram modulation (pharmacological change starting exactly at the phase-boundary)
- Envelope drift (deconditioning + baseline exertion capacity shift over ~4 years)
- Long-cycle seasonality
- Aging
- **Tactical-Garmin-use / real-time-Garmin-pacing improvement** (fifth confound). Per project memory `project_garmin_research_bias_boundary`, the participant used Garmin tactically (real-time signals + body signals + ergo principles) continuously across the entire LC-era pre-2026. If tactical-Garmin-pacing improved over the LC-era in parallel with behavioural learned-pacing, the phase-stratified arc cannot separate the two on the same corpus. **Load-bearing for the §6.1 reporting discipline**: this is what "phase-stratified" (never "learned-pacing") naming discipline is actually protecting against — the label bundles behavioural-learned-pacing with tactical-Garmin-pacing-improvement, and no design at this MD level disambiguates the two at n=1.

The `linear_detrend_on_pre` operand at the trigger arm's own per-episode 30d pre-window (parent MD §7.11) already removes the smooth component of all five factors, so **the phase-stratified read on the detrended arm is partially cleaner than the raw read** in the sense that per-episode smooth drift is subtracted. But it cannot separate learned-pacing from citalopram-modulation because the two are one-to-one temporally aligned at n=1: every day of learned-pacing evidence in the `citalopram_modulated` phase is also a day of citalopram exposure evidence.

**Disambiguation designs NOT executed at this MD**:

1. **Within-`citalopram_modulated` post-hoc phase re-split** — split the 2-year citalopram_modulated window into early (e.g. 2024-04-09 → 2025-03-31) vs late (2025-04-01 → 2026-06-05) sub-buckets and read the AUC trajectory within-citalopram. If AUC magnitude continues to strengthen within-citalopram-era, at least some of the strengthening is post-citalopram-onset behavioural, not the citalopram-onset step itself. Not pre-committed here; a downstream MD arc.
2. **Citalopram-stratified companion arm** — read the sub-part 3 contrast on a naturalistic subset drawn ONLY from pre-citalopram phases (`lc_pre_ergo` + `pacing_pre_citalopram_learning` + `pacing_habit_established`) with the three phases mapped to a within-pre-citalopram time axis. Sample sizes are small (n=19 + n=12 + n=125 = 156 heavy-episode-ends across ~2 years); descriptive-with-CI only. Not pre-committed here.
3. **Citalopram-native effect subtraction** — cross-reference the citalopram-modulation effect on activity outcomes documented in [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md) + [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md) and subtract from the `citalopram_modulated`-phase compensatory-magnitude read. Requires the citalopram-effect operand to be locked at compatible granularity (per-day activity outcomes at d+k after heavy episode-ends). Not pre-committed here.

**Priority scoping across the three designs** (tradeoff-vision per [CONVENTIONS §2.2](../CONVENTIONS.md#22-required-inputs)):

- **Priority 1 — Design 1 (within-`citalopram_modulated` post-hoc phase re-split)**. Uses the same n=158 pool, requires no additional data corpus, and directly disambiguates the citalopram-onset-step (2024-04-09) from within-citalopram-era continuation of learned-pacing. Lowest additional-corpus-degree-of-freedom cost; highest-return per unit-of-drafting-effort.
- **Priority 2 — Design 2 (pre-citalopram-only companion)**. n=156 heavy-episode-ends across 3 pre-citalopram phases (19 + 12 + 125) spanning ~2 years. Independent-of-Design-1 replication axis; workable at Stage D descriptive-with-CI given the n=125 anchor from `pacing_habit_established`. Second-priority because it operates on a smaller pool than Design 1 and does not touch the within-citalopram continuation question.
- **Priority 3 — Design 3 (citalopram-native effect subtraction)**. Highest methodological cost: requires modelling the citalopram effect on activity axes at compatible per-day-post-heavy granularity, which depends on the sister citalopram-stratification MD landing at that resolution. Do only if Priority 1 + Priority 2 are both insufficient to close the interpretive question.

**Structural note**: none of the three designs identifies learned-pacing from citalopram-modulation *from first principles* at n=1 under 100% temporal alignment — each shifts the confound to a different degree of freedom (within-citalopram continuation vs pre-citalopram cross-phase comparison vs citalopram-effect subtraction). The three together provide converging evidence if all three read consistently; no one design is a structural identification proof.

**Stage D reporting discipline**: report the sub-part 3 primary contrast with the citalopram-entanglement explicitly named as an inherited caveat (extends parent MD §10 item 5); do NOT attribute a late-phase-strengthening finding to learned-pacing alone. The pre-committed reading is that a late-phase-strengthening finding is **consistent with** learned-pacing but **also consistent with** citalopram-modulation and cannot be distinguished from it on the four-phase axis alone.

---

## 4. Dose-response pacing

### 4.1 Trigger stratification

The parent Q24 MD §9 pre-committed intensity-stratified sensitivity arm supplies the trigger strata. Three triggers per parent §9.1 + Stage -1 audit §5:

| Trigger | Definition | Strict-clean sample (episode-end, +3d) |
|---|---|---:|
| **Combined** | `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` | 125 |
| **Very-heavy only** | `exertion_class_lagged_lcera == 'very_heavy'` (last day of episode) | 52 |
| **Heavy only** | `exertion_class_lagged_lcera == 'heavy'` (last day, excluding very_heavy) | 73 |

**Cross-stratum scan discipline** (inherited from parent §9.1): the intensity-stratified triggers use **combined heavy as the scan set** for the strict-clean overlap filter. A very_heavy-episode-end followed by intervening heavy days contaminates the recovery window just as much as an intervening very_heavy day would.

Sample-size read policy per window is the parent MD §9.2 table: full at +3d for all three, combined + very_heavy_only at +5d as descriptive-with-CI (n=52 combined, n=19 very_heavy), combined-only at +10d (n=12).

### 4.2 Outcome operand family

Verbatim from parent Q24 MD §6.1 activity axes (see §3.2 above for the table). The dose-response arc's outcome family is identical to the sub-part 3 outcome family; the two arcs share activity axes and diverge on stratification axis (phase vs intensity).

Sleep + autonomic + subjective outcome families (parent §6.2, §6.3) may be added as descriptive companion reads at Stage D per orchestrator disposition. They do not participate in the primary dose-response contrast pre-commit here.

### 4.3 Primary contrast: trajectory magnitude across intensity strata

For each `(outcome operand, window, overlap-policy)` cell, compute per-trigger trajectory summary (per parent §7.1-§7.9) with each trigger's own matched-ordinary comparator pool (parent §4.1). Two headline contrasts:

**Contrast (a) — AUC comparison**: `AUC_very_heavy` vs `AUC_heavy`. Report both values with bootstrap 95% CIs; visualise as a per-window bar chart with two bars per outcome (very_heavy AUC + heavy AUC). No pre-registered inferential test between the two; the contrast is descriptive per §4.6 discipline below.

**Contrast (b) — slope comparison**: `slope_very_heavy` vs `slope_heavy` on the per-day mean-delta trajectory (parent MD §7.4 linear fit of `Δ(k)` on `k`). Reports the shape difference: does very_heavy-triggered trajectory decay faster (positive slope divergence in the compensatory direction) or persist longer than heavy-triggered?

Both contrasts are read on **raw + detrended arms side-by-side** per parent MD §7.11 discipline. Detrended reads on the intensity-stratified samples are more sensitive to sample-size floors (parent §7.11 <15-valid-pre-window-point threshold drops episodes from the detrended arm); report per-trigger per-outcome detrended-arm sample sizes explicitly at §7 audit hooks.

### 4.4 Direction pre-commit

**Dose-response hypothesis**: compensation magnitude scales with load magnitude. Operationally on activity outcomes per parent §7.7:

- `|AUC_very_heavy| > |AUC_heavy|` on the compensatory-success pool: very_heavy-triggered trajectory drops FURTHER below matched-ordinary than heavy-triggered. This is the pre-committed direction on the AUC-comparison contrast (a).
- `|slope_very_heavy_recovery| > |slope_heavy_recovery|` OR opposite-sign persistence, per the shape of the delta trajectory. On decay-shape trajectories, the pre-committed direction is that very_heavy trajectory takes longer to recover to phase-matched-ordinary (higher RTBT per parent §7.6, censored more often within the window per parent §7.6's `w+1` censoring bound).

**Opposite-direction findings** (dose-response absent or reversed):
- **Scaling absent**: `|AUC_very_heavy| ≈ |AUC_heavy|` — heavy is a uniform-response bucket; the very_heavy tier is a definitional-composite artefact rather than a physiologically-distinct load level. Reported as null on the dose-response contrast.
- **Scaling reversed**: `|AUC_heavy| > |AUC_very_heavy|` — heavy-triggered compensation exceeds very_heavy-triggered. Would indicate composite-class-label misspecification relative to the outcome operand; reported as sign-inversion finding in its own right per parent §7.7 discipline, not silently inverted.

### 4.5 Literature anchor

Van Campen 2020 (Healthcare 8(3):192, [DOI 10.3390/healthcare8030192](https://doi.org/10.3390/healthcare8030192)) 2-day CPET on severe ME/CFS documents **day-2 physiological deterioration scales with disease severity grade** — the more severe the disease, the deeper the day-2 CPET performance drop relative to day-1. Ghali 2020 (J Transl Med 18:246, [DOI 10.1186/s12967-020-02419-4](https://doi.org/10.1186/s12967-020-02419-4)) documents epidemiological severity-scaling of PEM. Moore 2023 (Medicina 59(3):571, [DOI 10.3390/medicina59030571](https://doi.org/10.3390/medicina59030571)) documents a 1-64 day recovery-time range in ME/CFS that itself implies episode/patient severity, not just the standardised trigger, drives recovery length.

Full literature synthesis at [`literature/reviews/pem_recovery_trajectory_review.md`](../literature/reviews/pem_recovery_trajectory_review.md) §5: "a minor dip should recover faster than a major crash, and recovery length is a severity signal". The dose-response arc transfers the severity-scaling of **physiological deficit** to the on-corpus severity-scaling of **behavioural compensation**: if the participant's autonomic system takes longer to recover from a very_heavy load than a heavy load, the corresponding behavioural pacing response (compensatory activity drop magnitude + duration) should scale similarly.

**Transfer caveat**: Van Campen's severity axis is disease-severity grade (between-participant); the dose-response arc's severity axis is within-participant intensity stratum (heavy vs very_heavy). The behavioural-compensation-scaling prediction is a within-participant extension of Van Campen's between-participant physiological-deficit-scaling finding. Literature-anchored direction; not literature-proven at n=1.

### 4.6 Discipline: descriptive-only at Stage D

**No formal inferential test between the two intensity strata is pre-committed at this MD level.** The dose-response contrast is a descriptive characterisation of operand behaviour, not a hypothesis test. Per parent MD §9.3, all three outcomes (scaling present / scaling absent / scaling reversed) are descriptively reportable; a Stage H pre-registration on dose-response requires the intensity-stratified arm to land first and requires a fresh methodology-review pass on this MD before Stage H drafts. Rationale for descriptive-only:

- Sample-size floor: at +5d the very_heavy_only trigger has n=19 strict-clean episodes (parent §9.2); at +10d n=5 is not viable. A formal between-strata test at +5d is underpowered; at +3d n=52 vs n=73 is workable descriptively but not the primary strength of the corpus.
- Multiplicity: adding a between-strata test on top of the parent MD's 5-channel × 3-window × 2-pool trajectory-verdict matrix (parent §8.2 = 15 branch verdicts) inflates the reporting cell count without a corresponding literature-anchored a-priori direction that would justify the multiplicity cost.
- Composite-artefact risk: if the between-strata contrast shows scaling reversed (§4.4), the primary reading is composite-class-label misspecification, which is a definition-audit finding, not a physiological-scaling test. The composite `exertion_rank_composite_lagged_lcera` reading itself would need re-examination before treating the reversal as a physiological finding.

**Stage D reporting discipline**: report the intensity-stratified panels (per parent §9.2 read policy) with per-trigger AUC + slope + peak-location + RTBT stacked. Compute both `Δ_very_heavy` and `Δ_heavy` trajectory-summary panels; do not compress into a single "dose-response verdict". Cross-strata direction (§4.4) is a descriptive read; the reading axis is `|AUC_very_heavy| vs |AUC_heavy|` magnitude ordering, not a between-strata p-value.

---

## 5. Inherited discipline (pointers)

All of the following apply verbatim to both §3 and §4 trajectories; do not re-derive.

| Discipline | Parent MD section | Applies to |
|---|---|---|
| Trajectory-detrend (`linear_detrend_on_pre` 30d pre-window) | §7.11 | §3 phase-stratified reads + §4 intensity-stratified reads; per-phase and per-trigger detrend runs must respect the <15-valid-pre-point drop rule; report per-phase per-outcome detrended-arm sample sizes at §7 |
| Bootstrap (B=10,000, block-length-1 for strict overlap, block length ≥ w for inclusive) | §7.10 | Both arcs; per-phase per-outcome bootstrap runs use each phase's own episode-end pool as the resample space |
| Multiplicity | §7.10 | Stage D descriptive-only, no multiplicity correction; Stage H (if drafted) uses parent MD single-cell headline + Holm step-down |
| Zero-vs-NaN | §11 | Both arcs; missing = uninstrumented, never `.fillna(0)`; per-phase per-outcome n_valid per k reported at §7 |
| Pool split (compensatory-success primary + compensatory-failure sub-arm) | §3.5 | Both §3 and §4 primary contrasts compute on the compensatory-success pool; failure-pool sub-arm reported for completeness at each window per phase and per trigger with sample-size discipline (n < 10 cells emit descriptively without bootstrap CIs per Stage D audit §10 item 1 orchestrator disposition) |

**Cross-arc consistency**: §3 (phase-stratified) and §4 (intensity-stratified) reads on the same outcome operand + window + overlap combination will produce distinct panel results. Do NOT collapse into a single 2D panel (phase × intensity) at Stage D — the two arcs are separate stratification axes on the parent MD's core trajectory operand. A phase × intensity double-stratification is possible in principle but is out of primary scope here; sample sizes across the 4 × 3 = 12 cells would be severely fragmented (e.g. very_heavy in `lc_pre_ergo` may drop to n < 5 strict-clean episodes).

---

## 6. Cross-arc confounds specific to §3 + §4

### 6.1 Phase confound (elaborated from §3.6)

Full temporal alignment of `citalopram_modulated` phase with post-citalopram-onset era means the sub-part 3 primary contrast cannot separate learned-pacing from citalopram-modulation on the four-phase axis alone. §3.6 pre-commits this as an inherited caveat and names three disambiguation designs not executed at this MD. **Reporting discipline**: sub-part 3 findings are always named "phase-stratified" (never "learned-pacing") in the Stage D descriptive audit output; the interpretation as learned-pacing vs citalopram-modulation is deferred to Stage S1 (internal synthesis) at the earliest.

### 6.2 Envelope drift (critical for §3 phase-stratified reads)

Parent MD §7.11 + §10 item 8 pre-commit envelope drift as the load-bearing confound for trajectory reads on the 4-year LC-era corpus. Per Stage D audit §9.1 caveat 9 drift-entanglement reframe, the `linear_detrend_on_pre` operand cannot distinguish nuisance-drift from compensatory-behaviour-improvement-drift; sub-part 3 phase-stratification is precisely the design-level lever to disambiguate. **Stage D reporting discipline for §3**: raw and detrended per-phase trajectory-summary panels reported side-by-side; per-phase pre-window mean levels reported alongside AUC magnitudes (per §3.5 level-vs-change discipline); rescue-subset flagging per §3.5 applied to any raw-only-significant cell whose per-phase read shows monotone strengthening in the pre-committed direction (§3.4).

### 6.3 Intensity × phase interaction (dose-response × phase cross-tab)

Data-availability probe against `per_day_master.csv` 2026-07-16 for heavy-episode-ends (last-day intensity class × phase):

| Intensity (last-day class) \ Phase | `lc_pre_ergo` | `pacing_pre_citalopram_learning` | `pacing_habit_established` | `citalopram_modulated` | **All** |
|---|---:|---:|---:|---:|---:|
| `heavy` | 8 | 4 | 70 | 83 | **165** |
| `very_heavy` | 11 | 8 | 55 | 75 | **149** |
| **All** | **19** | **12** | **125** | **158** | **314** |

**Read**: intensity distribution across phases is roughly balanced (`heavy` fraction: 42% lc_pre_ergo, 33% pacing_pre_citalopram_learning, 56% pacing_habit_established, 53% citalopram_modulated). No phase is dominated by a single intensity class; the intensity-stratified arm (§4) does NOT structurally cluster into specific phases. Cross-tab check: very_heavy-triggered episode-ends have adequate coverage across the two late phases (n=55 + n=75 = 130) for the parent MD §9.2 read policy to apply per-phase at +3d if a phase × intensity double-stratification is later attempted.

Envelope-drift check by year for episode-ends:

| Intensity \ Year | 2022 | 2023 | 2024 | 2025 | 2026 | **All** |
|---|---:|---:|---:|---:|---:|---:|
| `heavy` | 16 | 53 | 40 | 37 | 19 | **165** |
| `very_heavy` | 28 | 34 | 41 | 29 | 17 | **149** |
| **All** | 44 | 87 | 81 | 66 | 36 | **314** |

The 2026 elevation observed in parent Stage -1 audit §2 (47.4% heavy rate vs 34-35% baseline for 2023-2025) does NOT skew the intensity split — 2026 partial-year very_heavy fraction (17/36 = 47%) is comparable to the 2022-2025 pattern. The parent MD §10 item 1 2026-elevation caveat still applies as a sensitivity dimension.

### 6.4 Sample-size confound

Phase-stratified sample sizes at extended windows are the tightest constraint for §3:

| Phase | Combined episode-ends | Approx strict-clean sample floor at +5d (per parent §5.1 corpus rate scaling) |
|---|---:|---:|
| `lc_pre_ergo` | 19 | ~3-5 (below viable-descriptive floor per parent MD §7.10 practice) |
| `pacing_pre_citalopram_learning` | 12 | ~2 (narrative-only) |
| `pacing_habit_established` | 125 | ~20 (descriptive-with-CI) |
| `citalopram_modulated` | 158 | ~25 (descriptive-with-CI) |

Parent MD §5.1 corpus-level strict-clean rate at +5d is 52/314 ≈ 16.5% — applying that rate per-phase gives the estimated per-phase strict-clean sample floor above. Exact per-phase strict-clean sample floors must be computed at Stage D; the estimates are order-of-magnitude only. **Stage D reporting discipline for §3**: primary contrast reported only at +3d for all four phases; at +5d only for the two late phases as descriptive-with-CI; at +10d as combined-late-phases only (n_combined estimated ~10 strict-clean, at the viable descriptive floor). Early-phase (`lc_pre_ergo` + `pacing_pre_citalopram_learning`) trajectory-summary panels at extended windows are structurally unavailable and are reported as such — do not synthesise trajectory statistics on n < 5 arms.

---

## 7. Data-availability audit hooks

Stage D descriptive audit must probe and report the following before running any trajectory-summary computation. Numbers below are drafted-time probes against `per_day_master.csv` 2026-07-16 to confirm the operand definition is well-formed; Stage D re-runs against the same CSV should reproduce these.

### 7.1 Heavy-episode-end counts per phase (extends parent Stage -1 audit §2)

Reproduced from §3.1 above; corresponds to Stage -1 audit §2 heavy-day-rate-by-recovery_phase but at the episode-end unit:

| Phase | Heavy-episode-ends (gap=0, combined) |
|---|---:|
| `lc_pre_ergo` | 19 |
| `pacing_pre_citalopram_learning` | 12 |
| `pacing_habit_established` | 125 |
| `citalopram_modulated` | 158 |
| **All LC-era** | **314** |

### 7.2 Intensity × phase cross-tab (for §4 dose-response × §3 phase confound check)

Reproduced from §6.3 above.

### 7.3 Per-outcome coverage per phase

For each activity outcome (§3.2), per phase, report the fraction of heavy-episode-ends with valid outcome data at d, d+1, ..., d+w for each window w ∈ {3, 5, 10}. Stage D audit reports per-outcome per-phase per-k n_valid; cells with n_valid < 5 at any k drop from summary-statistic computation per parent §7.10 practice.

Drafted-time coverage probe on heavy-episode-end days for the four activity outcomes (per phase, at the episode-end day itself):

| Phase | n episode-ends | `total_steps` valid | `effective_exertion_min` valid | `vigorous_min` valid | `active_sec` valid |
|---|---:|---:|---:|---:|---:|
| `lc_pre_ergo` | 19 | 19 (100%) | 19 (100%) | 19 (100%) | 19 (100%) |
| `pacing_pre_citalopram_learning` | 12 | 12 (100%) | 12 (100%) | 12 (100%) | 12 (100%) |
| `pacing_habit_established` | 125 | 125 (100%) | 125 (100%) | 125 (100%) | 125 (100%) |
| `citalopram_modulated` | 158 | 158 (100%) | 158 (100%) | 158 (100%) | 158 (100%) |

Activity outcomes have full coverage on heavy-episode-end days across all phases per drafted-time probe; Stage D re-probe at per-d+k granularity (for k=1,...,10) is expected to show high coverage (parent MD §6.1 LC-era coverage: 98.5% for total_steps, 100% for effective_exertion_min, 98.6% for vigorous_min and active_sec).

### 7.4 Per-outcome coverage per intensity stratum

Same coverage probe repeated for the intensity-stratified strata (very_heavy vs heavy). Drafted-time counts of episode-ends per intensity stratum (last-day class) per phase are in §6.3 cross-tab. Full per-outcome per-intensity per-phase coverage table is a Stage D deliverable.

### 7.5 Per-contrast cell n values (§3.3 late-vs-early phase contrasts + §4.3 very_heavy-vs-heavy intensity contrasts)

Stage D deliverable: report actual n values per (outcome × window × overlap × phase-or-intensity-cell) after applying:

- Strict-clean overlap filter (parent §5.2)
- Compensatory-success pool filter (parent §3.5): no crash in [+1, +w] on the heavy-episode-end side
- Per-outcome data-validity filter across the full window
- For detrended arm: per-episode 30d pre-window ≥15-valid-point rule (parent §7.11)

Sample-size discipline per parent §7.10: cells with n < 10 emit descriptively without bootstrap CIs (per Stage D audit §10 item 1 orchestrator disposition).

---

## 8. Compression and lock discipline

Producer-mode methodology MD per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). The lock discipline follows the parent MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) §12 compression pattern:

1. **Draft (this file, r1)**: producer-mode subagent draft with all inherited machinery pointed at parent MD; only sub-part-3-specific and dose-response-specific design decisions are locked here.
2. **Fresh-session `/research-methodology-review`**: reviewer-mode session (different Claude session, cold context) audits this MD against the [CONVENTIONS §2.2](../CONVENTIONS.md#22-required-inputs) four-input bar + applicable 4-layer checklist items. Produces reviewer report at `docs/research/reviews/methodology-post_heavy_day_pacing_learning-YYYY-MM-DD.md`.
3. **r2 lock with compression absorption**: reviewer fires absorbed inline (mechanical clarifications, cross-cites, caveat additions); architectural changes escalate to r2-with-design-change and re-review.
4. **Stage D descriptive audit runs against r2-locked operand**: no Stage D sub-part-3 / dose-response output until the operand is locked.

**Compression rule** (inherited from parent MD): reviewer absorption at r2 is *mechanical* (clarifications, cross-cites, added caveats), NOT architectural (design changes). Any architectural change forces re-review before lock.

**No re-derivation gate**: any reviewer finding that this MD re-derived a piece of parent MD machinery (as opposed to pointing at parent) is a re-derivation-violation and forces pre-lock removal of the re-derivation. This MD's discipline is inheritance-only for the machinery that lives in the parent MD.

---

## 9. Lock log

| version | date | change |
|---|---|---|
| r1 | 2026-07-16 | Initial draft as producer-mode methodology MD sub-arc of parent [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1 (commit `58b7723`). Covers Q24 sub-part 3 (phase-stratified pacing) + dose-response pacing (severity-scaling of compensation magnitude); both are trajectory-based outcome tests inheriting parent MD §2 stratum + §3.1 unit + §4 comparator + §5 windows + §5.2 overlap + §3.5 pool split + §7.1-§7.9 trajectory summary stats + §7.10 bootstrap + §7.11 detrend + §11 zero-vs-NaN discipline verbatim. Sister arc (Q24 sub-part 5 + streak-→-crash predictive-categorical tests) covered by parallel-drafted [`heavy_day_crash_risk_prediction.md`](heavy_day_crash_risk_prediction.md). Drafting trigger: Stage D Wave 1 audit r4 (commit `b9ffcc5`) §9.1 caveat 9 drift-entanglement reframe — 36 raw-only-significant cells on compensatory-success pool activity that failed detrend are candidates for sub-part 3 disambiguation. §3.1 phase axis pre-committed to project-schema `recovery_phase` (4 buckets); §3.4 direction pre-commit is compensatory-drop magnitude STRENGTHENS across phases in pre-committed direction per parent §7.7. §3.5 discipline: rescue vs non-rescue subset call on the 36-cell drift-entangled pile. §3.6 confound pre-commit: `citalopram_modulated` phase 100% temporally aligned with post-citalopram-onset era per drafted-time probe (n=158 episode-ends in phase = n=158 post-onset episode-ends in phase); disambiguating learned-pacing from citalopram-modulation on n=1 requires additional design (three named designs not executed here). §4.1 intensity strata inherited from parent §9.1 (combined + very_heavy_only + heavy_only); §4.4 direction pre-commit is `|AUC_very_heavy| > |AUC_heavy|` on compensatory-success activity outcomes. §4.5 literature anchor: Van Campen 2020 physiological-deficit severity-scaling → behavioural-compensation-scaling on n=1 (transfer caveat: between-participant → within-participant). §4.6 discipline: descriptive-only at Stage D; no formal between-strata inferential test pre-committed. §6.3 intensity × phase cross-tab: intensity distribution roughly balanced across phases (no structural clustering). §7 data-availability audit hooks: phase distribution + intensity × phase cross-tab + per-outcome coverage tables drafted-time probed against `per_day_master.csv` 2026-07-16. Subagent-drafted per user delegation; fresh-session `/research-methodology-review` before lock is the peer-review discipline mirror to parent MD. **STATUS**: r1 DRAFTED 2026-07-16, awaiting fresh-session methodology review. |
| r1 LOCKED | 2026-07-16 | Fresh-session methodology review absorbed from [`docs/research/reviews/methodology-post_heavy_day_pacing_learning-2026-07-16.md`](../reviews/methodology-post_heavy_day_pacing_learning-2026-07-16.md) (verdict: DEFENSIBLE with revision). Four surgical patches applied per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations) compression discipline (mechanical clarifications only, no architectural change). **Patch 1** (§3.4, review I2.2 substantive): added literature-anchor paragraph naming Goudsmit 2012 (envelope theory) + Nijs 2013 (activity self-regulation in CFS) + Sanal-Hayes 2023 (Long COVID pacing) as citation-status-deferred anchors for the compensatory-drop-strengthens-over-time direction pre-commit; converts §3.4 from first-principles to confirmatory-of-established-literature framing per [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory). **Patch 2** (§3.6, review I3.5 substantive): added priority-scoping paragraph across the three disambiguation designs — Design 1 (within-`citalopram_modulated` post-hoc phase re-split) Priority 1 by same-pool + lowest-additional-DoF-cost; Design 2 (pre-citalopram-only companion) Priority 2 by n=156 independent-of-Design-1 replication; Design 3 (citalopram-native subtraction) Priority 3 by highest methodology cost. Structural note: none of the three identifies learned-pacing from citalopram at n=1 under 100% temporal alignment; the three together provide converging evidence. **Patch 3** (§3.6, review I4.4 substantive): added fifth confound to the four-phase-axis conflation list — tactical-Garmin-use / real-time-Garmin-pacing improvement per project memory `project_garmin_research_bias_boundary`; load-bearing for the §6.1 "phase-stratified" (never "learned-pacing") reporting-discipline naming choice — the label now protects against a five-confound bundle, not four. **Patch 4** (§3.5, discretionary user-endorsed): added mechanically-reproducible rescue metric — Spearman ρ of |AUC| on the 4-phase ordinal axis (thresholds ρ ≥ +0.50 rescue-eligible / +0.20 ≤ ρ < +0.50 weak / ρ < +0.20 no rescue) + monotonicity-score companion (fraction of consecutive-phase-pair |AUC| increases). Converts §3.5 from qualitative discipline to mechanically-verifiable across-analyst standard. Preserved byte-identically: §2 inheritance table, §3.1 phase axis + sample-size warnings, §3.2 outcome family, §3.3 primary contrast, §3.4 direction pre-commit (extended not replaced), §4 dose-response arc, §5 inherited discipline pointers, §6.2 envelope drift, §6.3 intensity × phase cross-tab, §6.4 sample-size confound, §7 data-availability audit hooks, §8 compression-and-lock discipline, §10 cross-references. **STATUS**: LOCKED r1 2026-07-16 post-review absorption. Stage D descriptive audit for sub-part 3 + dose-response is now unblocked. |

---

## 10. Cross-references

- [Parent Q24 methodology MD `post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) — LOCKED r1 2026-07-15 (commit `58b7723`). THE authoritative source for all inherited machinery in this MD (stratum + unit + comparator + windows + overlap + pool split + trajectory summary stats + detrend + bootstrap + multiplicity + zero-vs-NaN + 8 pre-committed caveats).
- [Sister methodology MD `heavy_day_crash_risk_prediction.md`](heavy_day_crash_risk_prediction.md) — drafted in parallel r1 2026-07-16. Covers Q24 sub-part 5 (compensatory-success counterfactual) + consecutive-streak-→-crash tests (predictive-categorical outcomes).
- [Stage -1 audit `analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md`](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md) LOCKED r1 2026-07-15. Corpus-level heavy-day counts + phase distribution + episode structure + intensity stratification that this MD extends.
- [Stage D descriptive audit `analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md`](../analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md) LOCKED r4 (commit `b9ffcc5`). §9.1 caveat 9 drift-entanglement reframe supplies the drafting trigger for §3; §10 item 8 level-vs-change disagreement supplies the corpus-general framing referenced in §3.5.
- [`methodology/sleep_metrics.md`](sleep_metrics.md) r1. Sleep-operand catalogue for any sleep-family outcome cross-refs at Stage D companion reads.
- [`methodology/citalopram_phase_stratification.md`](citalopram_phase_stratification.md). Cross-reference for §3.6 confound elaboration; the third disambiguation design (citalopram-native effect subtraction) depends on this MD's operand at compatible granularity.
- [`methodology/intervention_effects_descriptive.md`](intervention_effects_descriptive.md). Sister MD housing the `linear_detrend_on_pre` operand parent Q24 MD §7.11 inherits; also documents the citalopram-effect on `stress_mean_sleep` (§8) referenced by the §3.6 third disambiguation design.
- [CONVENTIONS §1.1, §1.2](../CONVENTIONS.md#1-the-role-split) producer/reviewer split; [§2.1](../CONVENTIONS.md#21-descriptive-before-inference) descriptive-before-inference; [§3.7](../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) trajectory-detrend audit hook; [§4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing.
- [`literature/reviews/pem_recovery_trajectory_review.md`](../literature/reviews/pem_recovery_trajectory_review.md). §4.5 literature anchor for dose-response; Van Campen 2020 severity-scaling of physiological deficit + Ghali 2020 epidemiological PEM severity + Moore 2023 recovery-time range as severity signal.

---

*Producer-mode methodology MD. Update when (a) the fresh-session review verdict lands and informs r2 compression, (b) Stage D descriptive audit for sub-part 3 lands and informs which drift-entangled cells rescue vs stay in the nuisance-drift pile, (c) a citalopram-disambiguation companion arc (§3.6 designs) is authorised for a downstream MD.*
