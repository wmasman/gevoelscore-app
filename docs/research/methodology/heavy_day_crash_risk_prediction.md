# Heavy-day crash-risk prediction: rest-adjacency + streak-length as predictors of crash-in-window

*Producer-mode methodology MD per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafted 2026-07-16 as r1; LOCKED r1 2026-07-16 post-review absorption per [`docs/research/reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md`](../reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md). ****LOCKED r2 2026-07-17** post-review absorption**: codifies Wave 2B/2C/2D findings via Path R2B (gevoelscore-conditioning definitional-pair extension at §3.1; joint end_class × gevoelscore stratifier at §3.5.x; era + intensity primary-stratifier upgrade at §5; new confound 8 for 2024 residual tension; §6.9 supersession of r1 §6.8 anticipatory closure). Pre-window covariate deferred per Option 1 (see §5 deferred-observation paragraph + Wave 2E cross-reference).*

---

## Authorship

**Drafted 2026-07-16** by Claude (Opus 4.7) in producer-mode subagent under user delegation per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem. Fresh-session `/research-methodology-review` before lock is the discipline mirror to the parent MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) (LOCKED r1 2026-07-15).

**Drafting trigger**: Q24 sub-part 5 ("does resting prevent crashes?") was framed by [Q24 MD §1.3](post_heavy_day_compensatory_rest.md#13-q24-sub-parts-covered) as an unfalsifiable counterfactual and left out of scope. User surfaced 2026-07-16 a **specific operationalisation** — *rest-day-adjacency around heavy episodes predicts crash rate in a fixed +K window* — that is testably predictive on the corpus (rest-day presence is observable, crash occurrence is observable, the association is measurable). Together with the consecutive-heavy-days-streak → crash-risk direction (cumulative-load-dose predictor) this MD frames both predictive-categorical outcome tests. Sister MD [`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md) (drafted in parallel) covers the trajectory-based outcomes (Q24 sub-part 3 + dose-response pacing) in a separate arc.

**Status**: ****LOCKED r2 2026-07-17** post-review absorption.** Producer-mode artefact per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). r1 LOCKED 2026-07-16 post-review absorption from [`docs/research/reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md`](../reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md) (DEFENSIBLE with revision). r2 DRAFT informed by Wave 2B / 2C / 2D Stage -1 audit findings (audits LOCKED r1 2026-07-16) codifying Path R2B: (i) gevoelscore-conditioning definitional-pair extension at §3.1 introducing `rest_day_p25_physical_strategic` + `rest_day_p25_physical_crisis` + `rest_day_p25_physical_borderline`; (ii) joint end_class × gevoelscore stratifier for the rest-adjacency arc per Wave 2D §12.2; (iii) upgrade of §5 confounds 2 + 7 from Stage D sensitivity companions to Stage D primary pre-commit stratifiers for the rest-adjacency arc per Wave 2B §13.10; (iv) new §5 confound 8 for the 2024 residual tension per Wave 2D §11.2; (v) supersession of r1 §6.8 anticipatory closure by operand refinement rather than direction flip. Pre-window cumulative-load covariate NOT codified at r2 per Option 1 (Wave 2E cross-reference; deferred descriptive observation paragraph after §5 confounds).

---

## 1. Purpose and scope

### 1.1 What this MD covers

Two predictive-categorical tests on the LC-era corpus, both taking crash occurrence in a fixed post-episode window as the outcome (binary; `is_crash` column):

1. **Q24 sub-part 5 reframed — rest-adjacency around heavy episodes as a crash-rate predictor** (bidirectional: rest-before and rest-after the heavy episode).
2. **Consecutive-heavy-days-streak length as a crash-rate predictor** (cumulative-load-dose reading; single ordinal exposure).

Both tests share stratum, heavy-day definition, unit-of-analysis, and comparator machinery with the parent Q24 MD; this MD extends the inherited machinery to categorical crash-occurrence outcomes rather than continuous trajectory outcomes.

### 1.2 What this MD does not cover

- **Q24 sub-parts 1 + 4**: activity + sleep + autonomic trajectory outcomes on the compensatory-success pool. Covered in the parent MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1 (commit `58b7723`).
- **Q24 sub-part 3 + dose-response pacing trajectory**: phase-stratified reads + intensity dose-response on continuous outcomes. Covered in the sister MD [`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md), drafted in parallel on 2026-07-16.
- **Q24 sub-part 2**: within-day shape. Blocked on per-minute Garmin extraction; out of scope structurally.
- **Any Stage H pre-registration**: this MD locks operand + machinery; per-HA pre-regs draft after Stage D descriptive audit results land, in a downstream session under reviewer-mode-with-authorization.

### 1.3 Reframing note: Q24 sub-part 5 from unfalsifiable to testably predictive

[Q24 MD §1.3](post_heavy_day_compensatory_rest.md#13-q24-sub-parts-covered) marked sub-part 5 ("does resting prevent crashes?") as an **unfalsifiable counterfactual** and out of scope. That framing is correct for the causal reading of the question — no counterfactual "same episode without rest" exists at n=1. The reframing this MD adopts is not a re-opening of the causal claim; it is a distinct question about the same episodes:

- **Causal claim (unfalsifiable)**: rest-day-adjacency *caused* the absence of crash. Requires a counterfactual and is out of reach at n=1.
- **Predictive-associational claim (testably predictive on this corpus)**: rest-day-adjacency around a heavy episode is *associated with* crash rate in a fixed post-episode window. The association is measurable — two arms (rest-adjacent vs rest-absent) yield two crash rates; the risk ratio has a confidence interval; a null hypothesis can be defined.

The two readings are structurally distinct. This MD tests only the predictive-associational reading. Interpretation of any Stage D finding under this MD stays predictive-descriptive, not causal — a positive association is compatible with (a) rest lowering crash risk, (b) participant felt bad pre-heavy and both rested *and* was crash-vulnerable (endogenous choice; see §3.9), or (c) unobserved confounder. The distinction is preserved in all §7 caveat framing.

**Same discipline for the streak-length test in §4**: dose-response of streak length on crash rate is predictive-associational, not a causal claim about cumulative load causing crashes. The observational structure of the corpus does not support the causal reading; interpretation stays predictive.

### 1.4 Relation to sibling infrastructure

- **Parent Q24 MD** [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1: stratum, unit-of-analysis (episode-end gap=0), heavy-day definition, comparator machinery, pool-split framework. This MD inherits verbatim; §2 below is pointer-only.
- **Sister MD** [`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md) (drafted in parallel): trajectory-based outcomes for sub-part 3 + dose-response. Complementary arc; both MDs load-share on the parent MD's machinery.
- **Stage -1 audit** [`analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md`](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md) LOCKED r1: episode-length distribution (§4 — max 10d, 60% single-day, 22 episodes at 4+d) + heavy-rate-by-year cross-tab.
- **Stage D descriptive audit r4** [`analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md`](../analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md) LOCKED r4: parent-MD Wave 1 results. §3 pool sample sizes give the crash-in-window base-rate anchor (16/125 = 12.8% at +3d) that this MD's predictive tests read against.
- **HA-P7** [`analyses/hypotheses/HA-P7/`](../analyses/hypotheses/HA-P7/) — predictive-classifier precedent (rolling-crash-count → crash; NOT-SUPPORTED at r1). Structural-autocorrelation flag from HA-P7's E[L]* factor-of-2 review ([`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md)) transfers to §4 streak-length as a rolling-window predictor.
- **HA01c** [`analyses/hypotheses/HA01c-effective-exertion-shock/`](../analyses/hypotheses/HA01c-effective-exertion-shock/) — predictive-classifier precedent for effective-exertion-shock → crash.
- **CONVENTIONS**: §1.2 producer-mode, §2.1 descriptive-before-inference, §3.3 definitional-pair, §3.6 named-counts, §3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from `bout_level_recovery_dynamics.md`), §4.2 caveat-class framing.

---

## 2. Inherited design (pointers to parent Q24 MD)

Every design element in this section is inherited from parent Q24 MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1 verbatim. No re-derivation. This section exists as a pointer table so the operand hooks below are readable without opening the parent MD.

| Element | Value | Source in parent Q24 MD |
|---|---|---|
| Stratum | LC-era only (`lc_phase == 'lc'`, `date >= 2022-04-04`), n=1524 | [Q24 MD §2.1](post_heavy_day_compensatory_rest.md#21-stratum) |
| Heavy-day definition | `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` | [Q24 MD §2.2](post_heavy_day_compensatory_rest.md#22-heavy-day-definition-locked-inherited) |
| Unit of analysis | Episode-end (gap=0 contiguous) | [Q24 MD §3.1](post_heavy_day_compensatory_rest.md#31-primary-episode-end-gap0-contiguous) |
| Episode-count | 314 gap=0 episode-ends on LC-era | [Stage -1 §4](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md#4-episode-structure--three-gap-tolerances) |
| Crash-outcome column | `is_crash` (boolean, LC-era total = 103; source `labels_crash_v2.csv` via `build_unified_dataset.py`) | [Q24 MD §3.5](post_heavy_day_compensatory_rest.md#35-crash-adjacency-handling-compensatory-success-vs-compensatory-failure-split) |
| Outcome window | Primary +5d (crash occurrence in `[D+1, D+5]` where D is episode-end) | [Q24 MD §5.1](post_heavy_day_compensatory_rest.md#51-window-ladder-locked-from-audit-63); sample n=52 strict-clean at +5d |
| Overlap policy | Strict-clean primary; inclusive as sensitivity | [Q24 MD §5.2](post_heavy_day_compensatory_rest.md#52-overlap-policies-both-reported-side-by-side-from-audit-64) |
| Multiplicity | Descriptive-only at Stage D; per-cell reads | [Q24 MD §7.10](post_heavy_day_compensatory_rest.md#710-null-hypothesis-inference-machinery-bootstrap--permutation--multiplicity) |

**Named-count discipline per [CONVENTIONS §3.6](../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file)**: all crash counts in this MD refer to `crash_v2` day-level rows (`is_crash == True` in `per_day_master.csv`, propagated from `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv`) unless otherwise stated. Episode counts refer to `gap=0` contiguous heavy-day runs where the heavy definition is per §2 above.

---

## 3. Sub-part 5: Rest-adjacency → crash risk (bidirectional)

### 3.1 Rest-day operand — primary + sensitivity (definitional-pair per [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair))

**Primary**: `rest_day_p25(d) = total_steps[d] < rolling_percentile_25(total_steps, window=30d, min_periods=15)`

- Anchored to a **personal 30-day rolling baseline** rather than an absolute cutoff, in the spirit of [CONVENTIONS §3.1](../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) (personal-baseline discipline).
- Adapts to participant's own recent activity envelope; addresses the LC-era baseline-drift concern inherited from parent Q24 MD §10 caveat 3 (2026 heavy-rate elevation, baseline drift).
- The 30d rolling window matches the pre-window used by the parent MD's trajectory-detrend companion ([Q24 MD §7.11](post_heavy_day_compensatory_rest.md#711-trajectory-detrend-sensitivity-per-conventions-37-envelope-drift-confound)); consistent-envelope discipline.
- `total_steps` LC-era coverage: 100.0% at daily row-level (structural for Garmin-instrumented days).

**Sensitivity**: `rest_day_class(d) = exertion_class_lagged_lcera[d] ∈ {none, light}`

- Categorical class already in `per_day_master.csv`; the coarser project-canonical definition of a low-load day.
- Definitional-pair-adjacent to the primary; both operationalise "low activity day" but from different axes (steps only vs the 4-axis composite class).
- Definitional-pair per [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair): pick primary + sensitivity; do not report both as independent evidence.

**Sensitivity companion added at r2 lock post-review absorption (recommendation 3 per fresh-session review — rolling-baseline moves-with-envelope artefact test)**: an **absolute-step operand** (`rest_day_abs_3k(d) = total_steps[d] < 3000`) is available as a Stage D sensitivity companion for testing the [Wave 2C §5.5](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#55-rolling-baseline-moves-with-envelope-artefact-concern) rolling-baseline moves-with-envelope concern. [Wave 2D §7](../analyses/descriptive/Q24-mdbeta-wave2d-2024-residual-tension/audit.md#7-absolute-step-threshold-companion) confirmed that the pooled sign-flip is preserved under the absolute-step operand (2024 RR shifts 0.929 → 0.652 modestly; pooled RR shifts 0.354 → 0.111 in the sign-flip direction). Not codified as r2 primary; available for Stage D sensitivity walk at the operand-availability level.

### 3.1.1 Gevoelscore-conditioning definitional-pair extension (added at r2 per Wave 2C findings)

**Rationale added at r2**: Wave 2C Stage -1 audit ([`../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md) LOCKED r1 2026-07-16) surfaced a rest-day composition shift across the LC era on the heavy-adjacent rest-day pool (proactive-strategic fraction 18% → 27% → 25% → 53% → 56% across 2022 → 2026 partial; crisis-reactive fraction 8% → 15% → 10% → 1% → 0% across the same window; Wave 2C §3.2). The omnibus `rest_day_p25` operand pools strategic-choice rest with crisis-forced rest at a mixing ratio that shifts across the era. The Wave 2C load-bearing 2×2 further shows that restricting the K=3 primary rest-after contrast to a proactive-strategic subset produces pooled RR = 0.354 (5/80 crash rate on strategic vs 41/232 crash rate on complement; source [`../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/output/pssubset_2x2_pooled.csv`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#5-proactive-strategic-2x2-pooled) via Wave 2C §5.1); restricting to a crisis-reactive subset produces pooled RR = 4.29. The pooled sign flips on both subsets in opposite directions relative to the omnibus Wave 2B pooled RR = 1.54, isolating gevoelscore-on-rest-day as the discriminator that partitions the endogeneity signature from the calibrated-pacing signature.

**Physical-rest-only semantic constraint** (per memory `project_rest_day_operand_semantics`): the `_physical_` infix in the three operand names below flags that these operands measure **physical rest only** (low steps, per the primary `rest_day_p25` definition) modulated by gevoelscore-on-that-day as a felt-state discriminator. They do NOT measure cognitive rest, emotional rest, or planning quality. A day with low steps but heavy cognitive load reads as physical rest under these operands but functionally is not full rest; no systematic instrumentation of cognitive/emotional load exists in the corpus. This constraint is load-bearing for all downstream interpretation: any finding on `_physical_strategic` reads as "physical rest chosen while feeling well enough (gevoelscore ≥ 5) that day", NOT as "genuine full-spectrum rest".

**Definitional-pair extension operands** (added to §3.1 primary + sensitivity omnibus operands, not replacing them):

- **`rest_day_p25_physical_strategic(d)`** = `rest_day_p25(d) == True AND gevoelscore(d) >= 5`: physical rest with adequate felt-state; the primary member of the strategic-vs-crisis definitional pair for the rest-adjacency arc at r2. Wave 2C empirical anchor: on the 341 heavy-adjacent rest-day pool the strategic fraction is 116/341 = 34.0% (Wave 2C §3.1).
- **`rest_day_p25_physical_crisis(d)`** = `rest_day_p25(d) == True AND gevoelscore(d) <= 3`: physical rest with low felt-state; the sensitivity member of the definitional pair. This operand also serves as the direct diagnostic for §3.9 confound 1 (rest-day-choice endogeneity / confounding-by-indication; Salas 2001; Kyriacou & Lewis 2016). By construction, a rest-day chosen while feeling badly is enriched for crash-vulnerable episodes. Wave 2C empirical anchor: on the 341 heavy-adjacent rest-day pool the crisis fraction is 41/341 = 12.0%.
- **`rest_day_p25_physical_borderline(d)`** = `rest_day_p25(d) == True AND gevoelscore(d) == 4`: physical rest with borderline felt-state; a third named bucket, descriptive-not-primary. Reflects the semantic ambiguity of gevoelscore = 4 (both "bad day that's not that bad" and "good day with existing fatigue"). Reported descriptively at Stage D as its own stratum alongside the primary strategic-vs-crisis pair; does NOT contaminate the primary read and is NOT part of the primary definitional pair. Wave 2C empirical anchor: on the 341 heavy-adjacent rest-day pool the borderline fraction is 111/341 = 32.6%.

**Primary vs sensitivity assignment per [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair)**: pick ONE of {strategic, crisis} as primary + the other as sensitivity companion; do NOT report both as independent evidence at Stage S1. **Strategic is the primary** at r2 per direction pre-commit alignment with §3.7 (Wave 2C pooled RR = 0.354 on the strategic subset empirically matches the §3.7 pre-commit direction of rest-adjacent → LOWER crash rate). Crisis is the sensitivity companion + the endogeneity diagnostic. Borderline is a third named bucket outside the pair, reported at Stage D as descriptive-only.

**Omnibus operand preservation**: the original `rest_day_p25` (physical rest, gevoelscore-unconditioned) is preserved as the omnibus physical-rest operand (definitional-pair anchor at §3.1). Any Stage D report on the rest-adjacency arc under r2 reports (a) the omnibus contrast + (b) the strategic-primary contrast + (c) the crisis-sensitivity contrast + (d) the borderline stratum as its own descriptive read, side-by-side.

**NaN handling per [CONVENTIONS §3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from `bout_level_recovery_dynamics.md`)](../CONVENTIONS.md#310-operationalisation-faithful-to-the-data-not-just-to-the-description)** for the gevoelscore-conditioning operands: gevoelscore NaN on a physical rest-day drops the rest-day from analysis rather than coercing to a bucket. Wave 2C measured 152/1524 = 10.0% gevoelscore-NaN on LC-era, near-fully concentrated in 2022 pre-tracker onset ([`../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#1-corpus-summary`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#1-corpus-summary)); post-tracker-onset gevoelscore coverage is near-full. Operand-availability caveat: the 2022 rest-day count on the strategic subset is small (Wave 2C §3.1 has 2022 strategic n = 9 / borderline n = 10 / crisis n = 5 / nan n = 20 on the 49-episode 2022 heavy-adjacent pool); Stage D reads on the strategic-primary subset restricted to 2022 are narrative-only.

### 3.2 Rest-AFTER-heavy window

For each heavy-episode-end at day D (per §2 unit-of-analysis), the rest-AFTER indicator is:

`rest_after_K(D) = any(rest_day(d) for d in [D+1, D+K])`

K values tested at Stage D: **K = 1, 2, 3**. `K = 3` is the primary rest-after-K value; K=1 + K=2 are reported as sensitivity ladder (does the association vary with tightness of the adjacency window?).

**Rationale for K=3 as primary**: matches the [Q24 MD §5.1](post_heavy_day_compensatory_rest.md#51-window-ladder-locked-from-audit-63) primary trajectory window (+3d) and the Chu 2018 24-72h PEM-peak window that anchors the parent MD's window ladder. Rest within 72h of the heavy episode is the most physiologically-relevant adjacency; K=1 and K=2 are tightness sensitivity companions.

### 3.3 Rest-BEFORE-heavy window

For each heavy episode, let `D_start` = first day of the episode (episode's start, not end). The rest-BEFORE indicator is:

`rest_before_K(D_start) = any(rest_day(d) for d in [D_start - K, D_start - 1])`

K values tested at Stage D: **K = 1, 2, 3**. Same K-ladder as §3.2 for symmetry.

**Rationale for K-symmetry**: pre-committed to keep rest-before + rest-after tests structurally comparable. A finding that only fires in one direction (only rest-before matters, or only rest-after matters) is itself a substantive descriptive finding; asymmetric K definitions would confound directionality with window-tightness.

### 3.4 Outcome — crash occurrence in +5d window post-episode-end

`crash_in_5d(D) = any(is_crash[d] for d in [D+1, D+5])` where D is the heavy-episode-end (per §2).

**Anchored to parent Q24 MD §3.5 pool-split**: the compensatory-failure sub-arm in the parent's Stage D r4 audit ([`descriptive_audit.md` §3](../analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md)) is exactly `crash_in_5d == True`. This MD's outcome IS the parent MD's pool-split axis, read from a different angle:

- **Parent MD**: split episodes into compensatory-success (`crash_in_5d == False`) vs compensatory-failure (`crash_in_5d == True`); read trajectory shape within each pool.
- **This MD**: predict which pool an episode falls into from rest-adjacency (§3.5) or streak length (§4.3).

The two questions are complementary, not competing (see §3.9).

**Sample-size anchor from parent Stage D r4 §3** (crash-in-window rate on strict-clean episode-ends):

| Window | Compensatory-success | Compensatory-failure | Total strict-clean | Crash-rate on strict-clean |
|---:|---:|---:|---:|---:|
| +3d | 109 | 16 | 125 | 12.8% |
| +5d | 43 | 9 | 52 | 17.3% |
| +10d | 11 | 1 | 12 | 8.3% |

Corpus baseline crash rate (LC-era) is 103/1524 = **6.8%** ([Stage -1 audit §1](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md#1-corpus-summary)); the trigger-day-following crash rate is roughly **2×** the corpus baseline at primary windows. Descriptive anchor; interpretation is inherited from parent Stage D r4 §7.

**+5d as primary window for this MD** (not +3d): the +5d window is where the crash-rate signal is strongest (17.3% at +5d vs 12.8% at +3d in the strict-clean sample) and where the compensatory-failure sub-arm sample size is still workable (n=9 at strict-clean; the full-episode sample used in this MD is n=314, so cell counts are usable). Sub-arm sample sizes for this MD's tests are derived in §6 data-availability numbers.

### 3.5 Primary contrast — 2×2 contingency and risk ratio

For each `K ∈ {1, 2, 3}` × direction ∈ {before, after}:

**2×2 contingency**: (`rest_K` presence: True/False) × (`crash_in_5d`: True/False), computed over the full 314 heavy-episode-end pool (all-episodes pool, not restricted to strict-clean overlap — see §3.10 for the overlap-policy sensitivity).

**Primary reported statistics** per (K, direction) cell:

- Crash rate on rest-adjacent heavy-episodes: `P(crash_in_5d = True | rest_K = True)`
- Crash rate on rest-absent heavy-episodes: `P(crash_in_5d = True | rest_K = False)`
- Risk ratio (RR): rate_rest_adjacent / rate_rest_absent
- Risk difference (RD): rate_rest_adjacent − rate_rest_absent
- Wilson 95% CI on each per-arm rate
- Bootstrap 95% CI on RR (per §3.6 machinery)

**Stationarity assumption at the primary-contrast level**: the primary contrast pools across the full LC-era stratum (n=314 heavy-episode-ends spanning 2022-04-04 → 2026-06-05). Stationarity of the rest-adjacency × crash contingency across the 4-year era is a substantive assumption partially addressed by §5 confound 7 (era-stratified sensitivity arm) and §5 confound 3 (streak-length × era cross-tab); the §6 data-availability audit hook is the empirical check. Non-stationarity of rest-day prevalence, crash-rate baseline, or the joint distribution is a caveat-class concern per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), not a correction pre-committed at this MD level. **r2 empirical update**: Wave 2B §9 era-stratified K=3 primary rest-after RR by year (2022: 1.08, 2023: 2.02, 2024: 1.56, 2025: 0.78, 2026 partial: 0.57) empirically rejects the stationarity assumption at descriptive-with-CI resolution. Consequence at r2: era is upgraded from Stage D sensitivity companion to Stage D primary pre-commit stratifier for the rest-adjacency arc per §5 confound 7 revision.

### 3.5.1 Joint end_class × gevoelscore-bucket stratification (added at r2 per Wave 2D §12.2)

**Rationale added at r2**: Wave 2D Stage -1 audit ([`../analyses/descriptive/Q24-mdbeta-wave2d-2024-residual-tension/audit.md`](../analyses/descriptive/Q24-mdbeta-wave2d-2024-residual-tension/audit.md) LOCKED r1 2026-07-16) surfaced an intensity-interaction residual within the 2024 proactive-strategic subset: heavy end_class shows RR = 0.00 (0/9 crashes; clean sign-flip toward the §3.7 pre-committed direction); very_heavy end_class shows RR = 3.50 (3/6 crashes; sign-inverted residual). All three 2024 crash-in-5d events on the strategic subset sit on very_heavy end_class episodes (Wave 2D §4.1 + §5.2). Gevoelscore-conditioning is sufficient to reveal the pre-committed direction on the heavy-end 2024 subset (clean flip) but is INSUFFICIENT on the very_heavy-end 2024 subset. This pattern is consistent with parent Wave 2B §10 whole-corpus intensity stratification (heavy end_class RR = 2.07, very_heavy end_class RR = 0.96) and internally-replicated within Wave 2D itself (§4 stratified 2×2 + §5.2 all-3-crashes-on-vh confirmation).

**Joint stratifier codification at r2**: end_class at the episode-end day (heavy vs very_heavy) is promoted from §5 confound 2 Stage D sensitivity companion to **joint primary pre-commit stratifier alongside gevoelscore-conditioning** for the rest-adjacency arc at Stage D + at any downstream Stage H pre-registration. Any Stage D 2×2 on the rest-adjacency arc under r2 reports the contrast **simultaneously stratified by (rest-day gevoelscore bucket per §3.1.1) × (end_class ∈ {heavy, very_heavy})** rather than by gevoelscore bucket alone.

**Reporting shape at Stage D under r2** for the rest-adjacency arc:

- Primary cell = strategic-rest × heavy end_class × K=3 rest-after × crash-in-5d, era-pooled. Wave 2D within-2024 empirical anchor: strategic × heavy × 2024 RR = 0.00 (0/9 crashes on strategic-rest arm vs 9/30 on complement; Wave 2D §4.1). Pooled RR from Wave 2C strategic-primary subset: RR = 0.354. Sample viability: on the pooled LC-era strategic-primary subset restricted to heavy end_class only, per §6 data-availability audit hooks the cell holds approximately n ≈ 80 episodes.
- Sensitivity cell 1 = strategic-rest × very_heavy end_class (Wave 2D residual). This is the cell where gevoelscore-conditioning alone is insufficient; reports the sign-inverted RR with the §5 confound 8 caveat (see below).
- Sensitivity cell 2 = crisis-rest × end_class stratified. Read for endogeneity diagnostic per §3.9 confound 1.
- Sensitivity cell 3 = borderline-rest × end_class stratified. Reported descriptively-only.
- **Immediate era-stratified companions**: same headline cell restricted to pre-cital era (2022-04-04 → 2024-04-08) + same headline cell restricted to post-cital era (2024-04-09 → 2026-06-05), reported side-by-side with the era-pooled headline. Documents the Wave 2B §9 + Wave 2C §5 era-instability of the sign direction. See §5 confound 7 revision for the citalopram temporal-anchor caveat framing.

**Sample-viability note**: the joint stratification splits the 314-episode LC-era pool into ~4 cells (strategic vs crisis vs borderline vs omnibus-rest-absent, × heavy vs very_heavy end_class). Per-cell counts are tight at the crisis and borderline strata within each intensity; the strategic × heavy cell is the load-bearing primary and holds the largest cell-count under the r2 codification. [Reproduces via filter on `../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/output/phase_std_pre_window_ps_true_all_years.csv` (Wave 2C companion + Wave 2E extension) restricted to `end_class == 'heavy'` at episode-end; the ~80 pooled + ~40 per-era counts are direct reproducible figures, not extrapolations.] Stage D descriptive-with-CI framing per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) is preserved; Wilson CIs will be wide on smaller cells.

**Autocorrelation attestation at r2 lock post-review absorption (recommendation 2 per fresh-session review)**: bootstrap resampling on the joint (rest-day gevoelscore bucket) × (end_class) stratifier inherits the episode-end unit-of-analysis + block length = 1 per §3.6 + parent Q24 MD §7.10; the joint stratification does not introduce autocorrelation the unit-of-analysis choice does not already address. HA-P7 precedent E[L]* factor-of-2 flag is a rolling-window-predictor concern (§4.7) not a joint-stratifier concern.

### 3.6 Statistical framing

**Small-sample-appropriate inference**: the compensatory-failure sub-arm has ~46 crash-in-5d episodes across the full 314-episode pool (see §6 data-availability numbers); per-cell counts in the 2×2 contingency can drop to n < 10 in a corner cell. Standard machinery:

- **Fisher's exact test** for the 2×2 contingency (small-sample-appropriate; no asymptotic assumption).
- **Bootstrap null** (B = 10,000; episode-level resampling; block length = 1 per parent MD §7.10 argument that episode-ends are approximately independent under the strict-clean policy; see §3.10 for the inclusive-policy sensitivity where a different block length is required).
- **RANDOM_SEED = 20260716** for reproducibility.
- **Wilson score CI** on each per-arm rate (small-sample-appropriate for proportions).

**Effect-size bar for descriptive-with-CI reads at this MD level**: risk-ratio CI excluding 1.0. This is a descriptive marker, NOT a p-value verdict — per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) descriptive-before-inference discipline, Stage D descriptive audits report CIs without inferential-verdict framing. Any downstream Stage H pre-registration draws its own falsification bar per [`hypothesis_lock_process.md`](hypothesis_lock_process.md) discipline.

**State-of-art for RR estimation with covariate adjustment**: Fisher's exact + Wilson score CI is the small-sample-appropriate primary read at this MD level; the state-of-art extension for covariate-adjusted RR estimation is **log-binomial regression** or **modified-Poisson regression with robust SE** (Zou 2004 *Am J Epidemiol*, "A modified Poisson regression approach to prospective studies with binary data"). Named + deferred: the natural Stage H extension when a specific confound (e.g. streak-length × era per §5 confound 3, or streak-length × intensity per §5 confound 2) needs direct adjustment is a log-binomial fit; not pre-committed at this MD level per the descriptive-only framing (§3.8, §4.5). Silence on this state-of-art would leave the reader without an audit-trail for why the simpler Fisher's + Wilson pair is the deliberate primary at Stage D.

### 3.7 Direction pre-commit

**r2 update, asymmetric direction pre-commit across the §3.1.1 gevoelscore-conditioning definitional-pair**. The original §3.7 pre-commit direction (rest-adjacent → LOWER crash rate) stands; r2 refines its scope by binding it to the strategic member of the definitional pair introduced at §3.1.1. The asymmetry is:

- **`rest_day_p25_physical_strategic` (primary)**: rest-adjacency → **LOWER** crash rate. Original §3.7 pre-commit direction preserved on this operand. **Empirical support**: Wave 2C pooled proactive-strategic subset RR = 0.354 (5/80 crash rate on strategic vs 41/232 on complement; [`../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#5-proactive-strategic-2x2-pooled`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#5-proactive-strategic-2x2-pooled)). Wave 2D within-2024 heavy-end stratum RR = 0.00 (0/9 crashes strategic-rest arm; [`../analyses/descriptive/Q24-mdbeta-wave2d-2024-residual-tension/audit.md#41-per-end-class-2024-2x2`](../analyses/descriptive/Q24-mdbeta-wave2d-2024-residual-tension/audit.md#41-per-end-class-2024-2x2)) is the strongest within-era corroboration.
- **`rest_day_p25_physical_crisis` (sensitivity + endogeneity diagnostic)**: rest-adjacency → **HIGHER** crash rate. Pre-committed reversed direction: by construction of the operand (physical rest chosen while feeling badly), the crisis subset is enriched for crash-vulnerable episodes; the reversed direction is the direct signature of the §3.9 confound 1 confounding-by-indication mechanism (Salas 2001; Kyriacou & Lewis 2016). **Empirical support**: Wave 2C pooled crisis-reactive subset RR = 4.29 ([`../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#6-crisis-reactive-2x2-pooled`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#6-crisis-reactive-2x2-pooled)).
- **`rest_day_p25_physical_borderline` (descriptive-not-primary)**: **no direction pre-commit**. Reported descriptively at Stage D as its own stratum; the semantic ambiguity of gevoelscore = 4 precludes a testable direction pre-commit.
- **Omnibus `rest_day_p25`** (physical rest, gevoelscore-unconditioned): no direction pre-commit at r2, because the omnibus operand mixes the two asymmetric direction pre-commits above at an era-shifting composition ratio (Wave 2C §3.2). Wave 2B pooled RR = 1.54 on the omnibus operand at K=3 primary rest-after is documented as a caveat-class descriptive finding under the composition-shift caveat, not as evidence for or against either sub-operand direction pre-commit.

**Rest-BEFORE vs rest-AFTER discipline preserved**: both directions retain the K-symmetry rationale from r1 (rest-before and rest-after tested with the same K-ladder for structural comparability); the asymmetry above applies to each rest-direction independently. Under §3.9 confound 1 + §3.9 item 2 (endogeneity is stronger for rest-before than rest-after), the crisis-subset reversed direction pre-commit is expected to be stronger for rest-before than rest-after; the strategic-subset original direction pre-commit is expected to be more robust for rest-after than rest-before.

**Interpretation guidance at Stage D**: opposite-direction findings on the strategic-subset primary (rest-adjacent-and-strategic → HIGHER crash rate) are reported as sign-inversions per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), a substantive finding in its own right. Opposite-direction findings on the crisis-subset (rest-adjacent-and-crisis → LOWER crash rate) are also reported as sign-inversions, and would substantively challenge the confounding-by-indication reading of the endogeneity confound.

**Reciprocal definitional-pair discipline attestation added at r2 lock post-review absorption (recommendation 4 per fresh-session review)**: strategic pooled RR = 0.354 + crisis pooled RR = 4.29 are read from the same underlying joint distribution split (Wave 2C §6.5 definitional-pair discipline) and must NOT be reported as independent evidence at Stage S1. The asymmetric direction pre-commit codified here is a within-operand-pair reading structure; at Stage S1 synthesis the two findings are one definitional-pair split, not two independent tests. Cross-referenced to [`../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#65-definitional-pair-discipline`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#65-definitional-pair-discipline).

**Supersession of r1 §6.8 anticipatory closure by r2 operand refinement (see §6.9)**: r1 §6.8 anticipated that a Stage D confirmation of the omnibus-operand pooled sign-inversion (RR = 1.54 at K=3 primary rest-after) would trigger either (a) Stage H drafting with sign-inversion as the pre-committed direction, or (b) an MD-β r2 revision formally flipping the §3.7 direction pre-commit. r2 executes path (b) but NOT by flipping the direction pre-commit. Instead, r2 refines the primary operand from the omnibus `rest_day_p25` (which mixes strategic + crisis rest at a shifting mixing ratio per Wave 2C §3.2) to `rest_day_p25_physical_strategic` (which shows Wave 2C pooled RR = 0.354 matching the original §3.7 pre-commit direction). The original §3.7 pre-commit direction stands on the refined primary; the omnibus-operand sign-inversion is descriptively true but no longer the primary contrast at r2. See §6.9 for the r1 §6.8 supersession closure paragraph.

### 3.8 Discipline — descriptive predictive-only

This MD tests a **predictive-associational** claim (§1.3), NOT a causal one. Interpretation of any Stage D finding stays predictive:

- A positive finding (rest-adjacent → lower crash rate, RR CI < 1.0) is compatible with: (a) rest genuinely lowers crash risk in the window; (b) unobserved third factor (e.g. participant felt fine pre-heavy → both rested less and was less crash-vulnerable, biasing the rest-adjacent arm toward crash-prone episodes — a sign-inversion mechanism); (c) chance in a small-sample corpus.
- A null or sign-inversion finding does NOT falsify the causal reading of "rest prevents crashes"; it falsifies the specific predictive-associational operationalisation on this corpus.

No causal claim is made regardless of Stage D outcome.

### 3.9 Confound pre-commit

Per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing. Each is acknowledged as an uncorrected confounder; none is claimed to drive the outcome a-priori.

1. **Rest-day-choice endogeneity** (primary confound): rest-day-adjacency is observational, not experimentally-manipulated. The participant may have chosen to rest **because they felt bad** — pre-heavy fatigue → rest-before-heavy chosen → participant enters heavy day already vulnerable → higher crash risk in +5d. The comparator group (rest-absent) is then enriched for episodes where the participant felt fine, biasing the "rest prevented crash" reading toward **NO effect**, or toward sign-inversion where rest-adjacent shows HIGHER crash rate. Directionality of the endogeneity is asymmetric between rest-before and rest-after (see item 2). **Epidemiological literature construct**: this mechanism is the pattern known in observational pharmacoepidemiology as **confounding-by-indication** (Salas et al. 2001; Kyriacou & Lewis 2016 *JAMA*) — treatment choice (rest vs no-rest) is driven by the underlying condition being treated (felt-bad pre-heavy). Naming the pattern per [CONVENTIONS §2.2](../CONVENTIONS.md#22-required-inputs) I2 discipline; ties the §6.6 exploratory sign-inversion to a decades-old epidemiological framing.

2. **Directionality of endogeneity — rest-before vs rest-after**: hardest for rest-BEFORE-heavy (the participant may have rested strategically before the heavy episode because they anticipated the load, but may also have rested because they felt bad). Rest-AFTER-heavy is **less endogenous** in direction — the heavy day is complete before the rest-day decision is made; subsequent rest is more forward-looking recovery than pre-episode illness signalling. If rest-before shows sign-inversion and rest-after shows the predicted direction, that pattern is consistent with the endogeneity asymmetry rather than a rest-prevents-crash mechanism.

3. **Circularity with parent Q24 MD §3.5 pool-split**: parent MD splits strict-clean episode-ends into compensatory-success vs compensatory-failure by `crash_in_5d`. This MD's outcome IS `crash_in_5d`. There is **no circularity of test-statistic** — this MD asks what predicts pool-membership; the parent asks what the trajectory looks like within each pool. But the shared sample means findings from the two MDs must not be doubly-invoked as independent evidence. **Reporting discipline**: any Stage D finding from this MD that fires on the same episode set as a parent MD Stage D finding cites the parent explicitly + notes the shared sample.

4. **All-episodes pool vs strict-clean pool** (see §3.10): this MD's primary contrast uses the full 314-episode pool (all gap=0 episode-ends) rather than the parent MD's strict-clean subset (n=125 at +3d, n=52 at +5d). Rationale: (a) rest-adjacency is a per-episode property that does not require the strict-clean overlap filter to be well-defined; (b) using the full pool preserves sample size for the crash-in-window contingency, which is the load-bearing measurement. Sensitivity: report the strict-clean subset as a companion arm at Stage D — divergence between all-episodes and strict-clean reads is a substantive finding (it identifies whether overlap-density confounds the rest-adjacency signal).

5. **Baseline-drift on the rest-day operand**: primary rest-day operand uses `personal 30d rolling-baseline percentile 25`. Inherits the baseline-drift caveat from parent Q24 MD §10 caveat 3 — the personal baseline is itself drifting across the LC era. Interpretation of the rest-day operand is relative-to-recent-past, not absolute. Sensitivity operand (`exertion_class_lagged_lcera ∈ {none, light}`, §3.1) uses a slower-drifting reference (lagged [d-90, d-30] baseline per parent MD §2.2) and is a robustness check on drift sensitivity.

6. **Envelope-drift asymmetry across the corpus** (parent Q24 MD §10 caveat 8): the LC-era corpus has drifting crash rate (~10/year 2023-2024 → ~2/year 2025-2026). Rest-adjacency prevalence may also drift (participant's rest-day frequency may have changed over the era; see §6 data-availability numbers). Reporting: an era-stratified sensitivity arm (rest-adjacency × crash-in-5d cross-tab restricted to same-year episodes) is a Stage D companion for the primary contrast. Escalation-to-caveat rule per parent MD §10 caveat 8 applies.

### 3.10 Overlap-policy sensitivity

Parent Q24 MD §5.2 locks strict-clean + inclusive as side-by-side arms for trajectory reads. For this MD's predictive tests:

- **Primary contrast**: all-episodes pool (n=314). No overlap-clean filter applied at the trigger side. Rationale: the rest-adjacency indicator + crash-in-5d outcome are well-defined regardless of other heavy days in the +K rest-window or the +5d crash-window.
- **Sensitivity 1 (strict-clean)**: restrict to episode-ends with no other heavy day in `[D+1, D+5]` (the parent MD's strict-clean at +5d, n=52). Removes overlap contamination in the crash-outcome window.
- **Sensitivity 2 (inclusive with block-appropriate null)**: full 314-episode pool with block-permutation null block length ≥ 5 (matching the +5d outcome window per parent MD §7.10 inclusive-policy machinery).

Divergence between primary and sensitivity 1 identifies whether overlap contamination is confounding the rest-adjacency signal. Divergence between primary and sensitivity 2 identifies whether autocorrelation in the null construction changes the effect-size CI materially.

---

## 4. Consecutive-heavy-days-streak length → crash risk

### 4.1 Streak-length operand

`streak_length(D_end) = |{contiguous heavy days ending at D_end}|` where D_end is the heavy-episode-end (per §2 unit-of-analysis; gap=0 contiguous definition inherited from parent MD).

**Streak-length bins**: `L_bin ∈ {1, 2, 3, 4+}` (four-level ordinal exposure).

- **`1`**: single-day heavy episodes (n=188 per [Stage -1 §4](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md#4-episode-structure--three-gap-tolerances)).
- **`2`**: two-day heavy episodes (n=77).
- **`3`**: three-day heavy episodes (n=27).
- **`4+`**: four-or-more-day heavy episodes (n=22, merged; the 4d/5d/6d/7d/8d/10d sub-bins have 12/6/1/1/1/1 respectively, so per-sub-bin analysis is not viable).

Merging at 4+ is the disciplined choice for statistical viability: no formal test can distinguish 6d vs 8d vs 10d with 1 episode each; the merged bin preserves ordinal ranking without over-claiming resolution.

### 4.2 Outcome — crash occurrence in +5d window after streak ends

Same as §3.4: `crash_in_5d(D_end) = any(is_crash[d] for d in [D_end+1, D_end+5])`.

Same rationale as §3.4 (parent MD Stage D r4 §3 pool-split anchor); +5d is the primary window because the crash-rate signal is strongest and the sample viability holds.

### 4.3 Primary contrast — crash rate by streak-length bin

For each `L_bin ∈ {1, 2, 3, 4+}`:

- Crash rate: `P(crash_in_5d = True | L_bin)` on the 314-episode pool.
- Wilson 95% CI per bin.

### 4.4 Direction pre-commit

**Longer streaks → higher crash rate** (dose-response of cumulative load on crash risk).

Mechanistic anchor: cumulative-load model + Wiggers push-crash framing; a 4-day heavy streak represents more cumulative load than a 1-day heavy episode and (under the dose-response reading) should carry higher post-episode crash risk. This is the pre-committed reading axis; a monotonic-decreasing pattern (shorter streaks → higher crash rate) would be a sign-inversion, reported as a substantive finding per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no).

### 4.5 Statistical framing

- **Wilson score CI** on each per-bin rate (small-sample-appropriate).
- **Cochran-Armitage trend test** on the ordinal 4-bin × binary-outcome contingency. Cochran-Armitage is the appropriate small-sample trend test for ordinal exposure on a binary outcome (references: Armitage 1955; standard biostatistical practice for dose-response on binary outcomes).
- **Bootstrap null** (B = 10,000; episode-level resampling; RANDOM_SEED = 20260716). Under the all-episodes primary pool the resampling unit is the episode; block length = 1 for strict-clean sensitivity companion, block length ≥ 5 for inclusive sensitivity companion (matches §3.10 machinery).
- **Effect-size bar for descriptive-with-CI reads at this MD level**: monotone increasing across bins with all-bin Wilson CIs distinct at extremes (1 vs 4+). Descriptive marker, not p-value verdict per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference).

### 4.6 Sample constraint

From [Stage -1 §4](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md#4-episode-structure--three-gap-tolerances): 188 single-day episodes (60%), 77 two-day (25%), 27 three-day (9%), 22 four-plus (7%). The 4+ bin merges all longer streaks; per-sub-bin at 6+d has only 4 episodes.

**Formal-test resolution**: the Cochran-Armitage trend test on the 4-bin ladder is defensible; per-bin descriptive reads at bins {1, 2, 3, 4+} are viable; per-sub-bin reads at 6+d are narrative-only. Crash-rate CIs at bin 4+ will be wide given n=22; interpretive discipline respects the wide-CI caveat.

### 4.7 Rolling-window-predictor structural-autocorrelation flag

Per [`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md) and the HA-P7 precedent ([HA-P7 verdict-review](../analyses/hypotheses/HA-P7/verdict-review.md)), any rolling-window predictor at window W ≥ 10 typically trips the E[L]* factor-of-2 flag under [`permutation_null_block_length.md`](permutation_null_block_length.md) machinery — the lag-1 autocorrelation of a rolling sum at window W approaches (W−1)/W by construction.

**Streak-length as a rolling-window predictor**: streak_length is technically a "rolling identifier" of contiguous heavy-day runs, not a true rolling sum. However, the day-level construction of streak_length has structural autocorrelation across consecutive days (day D and day D+1 within the same streak share streak_length identity by definition). At the episode-end unit-of-analysis this MD adopts, the per-episode streak_length is a **single value per episode-end**, not a rolling-window emission — the autocorrelation concern is mostly deflected by the unit-of-analysis choice.

**Pre-commitment for Stage D**: block length = 1 for episode-level resampling is defensible under the episode-end unit (per parent MD §7.10 argument). If the Stage D descriptive audit surfaces evidence that longer streaks cluster in time (e.g. multiple 4+d streaks within a 30d window), the data-driven E[L]* diagnostic per [`permutation_null_block_length.md §2`](permutation_null_block_length.md) is computed as a companion. If E[L]* ≥ 2× the locked block length of 1, the finding is flagged per HA-P7 §4.6 closure template: (a) cite structural clustering; (b) re-run at E[L]* block; (c) verify verdict robustness across block-length arms.

This is a foreseen review trigger, named per [`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md) anticipatory-drafting-note discipline.

---

## 5. Cross-arc confounds specific to §3 + §4

Per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing. Extends parent Q24 MD §10 caveats to the §3 + §4 predictive tests.

1. **Rest-day-choice endogeneity** (§3.9 item 1 + item 2): rest-day-adjacency is observational; the endogeneity biases the direction reported per §3.9. **Not corrected** in the primary read; caveat-class.

2. **Streak-length ↔ intensity confound + rest-adjacency intensity primary-stratifier upgrade at r2**: for the streak-length arc (§4), the r1 framing stands. Do longer streaks contain a higher fraction of very_heavy days on average? A monotonic streak-length-crash relationship may be confounded by intensity (longer streaks → more very_heavy → higher crash rate not because of length per se but because of intensity accumulation). §6 data-availability numbers include the streak-length × intensity cross-tab. **Stage D handling for the streak-length arc**: report streak-length × crash-rate contrast alongside an intensity-adjusted companion (streak-length crash-rate restricted to streaks where fraction-very-heavy ≤ some cutoff, or intensity as a stratifier per parent MD §9). **r2 upgrade for the rest-adjacency arc**: intensity (end_class at episode-end day, heavy vs very_heavy) is upgraded from Stage D sensitivity companion to **Stage D primary pre-commit stratifier** for the rest-adjacency arc per Wave 2B §13.10 escalate-tier finding (whole-corpus intensity-stratified K=3 primary rest-after RR: heavy = 2.07, very_heavy = 0.96; [`../analyses/descriptive/Q24-mdbeta-precursor-rest-streak/audit.md#10-intensity-stratified-rest-adjacency-3-way-cross-tab`](../analyses/descriptive/Q24-mdbeta-precursor-rest-streak/audit.md#10-intensity-stratified-rest-adjacency-3-way-cross-tab)) + Wave 2D §12.2 joint-stratifier recommendation. Pooled-across-intensity contrast on the rest-adjacency arc is demoted to caveat-class descriptive read at r2. Codification detail lives in §3.5.1 above; the r2 primary Stage D read for the rest-adjacency arc reports the joint (rest-day gevoelscore bucket) × (end_class) stratification.

3. **Streak-length ↔ era confound**: are longer streaks more common in specific years? Parent Q24 MD §10 caveat 1 flags 2026 heavy-rate elevation (47.4% partial-year vs ~34-35% baseline). §6 data-availability numbers include the streak-length × era cross-tab. **Stage D handling**: era-stratified sensitivity arm on the streak-length contrast (report crash-rate-by-bin excluding 2026, in parallel with primary all-era report). Same escalation-to-caveat rule as parent MD §10 caveat 1.

4. **Baseline-drift on the rest-day operand**: §3.9 item 5. Personal 30d rolling p25 drifts across the LC era; sensitivity operand (`exertion_class ∈ {none, light}`) is a robustness check.

5. **Rolling-sum-predictor autocorrelation flag** for streak-length as a rolling-window construct (§4.7): the E[L]* factor-of-2 flag from HA-P7 precedent applies. Foreseen review trigger; not corrected at MD level; Stage D descriptive-time diagnostic per [`permutation_null_block_length.md §2`](permutation_null_block_length.md).

6. **Circularity with parent Q24 MD §3.5 pool-split** (§3.9 item 3): shared sample with parent MD; findings must not be doubly-invoked. Reporting discipline: any Stage D finding cites the parent MD explicitly + notes the shared sample. **Any Stage S1 synthesis must pick one of {this MD, parent Q24 MD} as headline per Q24 sub-part and cite the other as complementary — the two are NOT independent evidence at Stage S1 level given the shared crash-in-5d outcome sample.**

7. **Envelope-drift asymmetry across the corpus + rest-adjacency era primary-stratifier upgrade at r2** (parent Q24 MD §10 caveat 8, inherited). Reporting: era-stratified sensitivity for both the §3 rest-adjacency and §4 streak-length contrasts (see also confound 3 above for the streak-length × era angle). **r2 upgrade for the rest-adjacency arc**: era is upgraded from Stage D sensitivity companion to **Stage D primary pre-commit stratifier** for the rest-adjacency arc per Wave 2B §13.10 escalate-tier finding. Empirical anchor: Wave 2B §9 era-stratified K=3 primary rest-after RR by year is 2022 = 1.08, 2023 = 2.02, 2024 = 1.56, 2025 = 0.78, 2026 partial = 0.57 ([`../analyses/descriptive/Q24-mdbeta-precursor-rest-streak/audit.md#9-era-stratified-rest-adjacency-3-way-cross-tab`](../analyses/descriptive/Q24-mdbeta-precursor-rest-streak/audit.md#9-era-stratified-rest-adjacency-3-way-cross-tab)). The pooled RR = 1.54 is 2023 + 2024 driven; 2025 + 2026 partial flip to the pre-commit direction. This empirically rejects the §3.5 stationarity assumption at descriptive-with-CI resolution. Pooled-across-era contrast on the rest-adjacency arc is demoted to caveat-class descriptive read at r2.

   **r2 era-stratifier codification, pre-cital vs post-cital 2-bucket at boundary 2024-04-09**. The r2 era stratifier for the rest-adjacency arc is a **2-bucket split at the 2024-04-09 citalopram-onset boundary**: pre-cital era spans 2022-04-04 → 2024-04-08 (roughly balanced with the post-cital span; approximately 156 pre-cital episode-ends vs approximately 158 post-cital episode-ends out of the 314 LC-era total). This boundary aligns with the MD-α `recovery_phase` axis boundary between `pacing_habit_established` and `citalopram_modulated` ([`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md) §3.1). The 2-bucket split is an upgrade from Wave 2B r1's implicit per-year-cell framing (2022-2026 as five yearly cells) to a coarser but more sample-viable split; per-year cells remain available as descriptive-only sub-reads.

   **Era caveat, 6-mechanism conflation with no causal attribution at n=1**. The pre-cital vs post-cital era stratifier is a **temporal anchor at 2024-04-09 (citalopram onset)**. Any RR difference between the two strata **conflates at least six co-occurring factors**:

   1. Citalopram pharmacological effect.
   2. Learned-pacing behavioural evolution (per MD-α §3.6 five-confound bundle).
   3. Tactical-Garmin-use improvement (per memory `project_garmin_research_bias_boundary`).
   4. Natural LC disease-course trajectory.
   5. Envelope drift (documented in MD-α Wave 2A audit §8 pre-window mean-level shift; per Wave 2D §10.3 the pre-window `effective_exertion_min` per day mean is 19.39 min/day on `pacing_habit_established` vs 5.17 min/day on `citalopram_modulated`, a ~4× shift at the phase boundary).
   6. Aging + seasonality across the ~2-year window.

   **The stratifier does NOT identify medication effect at n=1.** It is a temporal anchor for descriptive era-stratified reads. **No causal claim about medication is made or supported by this stratifier.** Any interpretation attributing an era-stratum RR difference to citalopram specifically is out of scope for this MD and would require a between-participant or within-participant crossover design not available at n=1. This caveat is load-bearing for every era-stratified reading of the r2 primary rest-adjacency contrast and must be surfaced explicitly in any Stage D descriptive audit + any downstream Stage H pre-registration synthesis.

   **CONVENTIONS §3.7 detrend hook — does-not-apply-redirected-to-analogue documentation**: parent Q24 MD §7.11 imports the [CONVENTIONS §3.7](../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) trajectory-detrend audit hook because its outcome family is raw-mean pre-vs-post windowed trajectories on continuous channels (parent §7.1-§7.9 nine trajectory-summary stats). This MD's outcome family is **binary crash occurrence** (`crash_in_5d`, a binary outcome per §3.4 / §4.2) with **binary-or-ordinal exposure** (rest-adjacent yes/no per §3.5; streak-length bin per §4.3). The CONVENTIONS §3.7 detrend machinery — subtract a linear pre-window fit from both trigger and comparator arms to remove smooth envelope drift — is **not directly applicable to a binary-outcome contingency test**: there is no "windowed mean" on a binary outcome whose pre-episode slope can be linearly extrapolated and subtracted at the per-episode level. **The era-stratified pre-commit stratifier (this confound 7 + confound 3 for the streak-length × era angle) is the analogue mechanism for the same underlying envelope-drift concern** — same concern (baseline-shift across the 4-year LC era), different statistical machinery (stratification of the contingency table by era rather than detrending of a continuous outcome). Per CONVENTIONS §3.7 concern, era-stratification is the equivalent drift-correction test for the categorical-outcome test family. Documented explicitly here so a Stage D reviewer does not need to re-derive why the parent MD's pre-lock §7.11 absorption is not mirrored in this MD.

8. **2024 residual tension on the strategic-primary rest-adjacency arc** (added at r2 per Wave 2D §11.2). On the r2 primary operand `rest_day_p25_physical_strategic`, Wave 2C §5 per-year RR at K=3 primary rest-after is: 2023 = 0.223, **2024 = 0.929**, 2025 = 0.000, 2026 partial = 0.000. 2024 does not sign-flip cleanly on the strategic-primary subset while 2023 and 2025 + 2026 do. Wave 2D diagnosed the residual as most consistent with a joint reading of two candidate mechanisms at strong descriptive resolution (Wave 2D §11.2): (b) partial-mitigation-via-pre-window-load, where 2024 strategic-primary crash cases carry ~2× higher pre-window 30d effective_exertion_min sum (mean 214.7 min vs non-crash mean 114.8 min at n=3 vs n=12 narrative-only resolution; Wave 2D §5.4 + §9); and (e) intensity-interaction residual, where all 3 strategic-primary 2024 crash events sit on very_heavy end_class episodes (Wave 2D §4). The (e) intensity-interaction leg is addressed at r2 by the joint end_class × gevoelscore stratifier codification at §3.5.1 + confound 2 upgrade above. The (b) pre-window-load leg is NOT codified at r2 per Option 1 (see the deferred descriptive observation paragraph immediately below this list). Caveat-class per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no); descriptive-only at r2.

**Deferred descriptive observation, pre-window cumulative load** (added at r2 per Wave 2E finding + Wave 2D §12.3 codification-path recommendation). **Coherence bridge added at r2 lock post-review absorption (recommendation 7 per fresh-session review)**: the (b) pre-window-load leg named in confound 8 above is the specific mechanism deferred here; the (e) intensity-interaction leg named in confound 8 is codified at §3.5.1 joint stratifier + §5 confound 2. Confound 8 documents the 2024 residual tension as caveat-class; this paragraph documents the (b) mechanism as pending work not codified at r2. Wave 2D §12.3 + Wave 2E surfaced a within-2024 descriptive pattern where phase-standardised pre-window 30d `effective_exertion_min` discriminates crash-in-5d on the very-heavy end_class strategic-rest subset (n=3 crashes at positive phase-standardised residuals vs n=12 non-crashes centred below the phase mean). The same operand reads backwards outside 2024 per the LC-era phase-standardised strategic-primary pool probe (2 pre-cital crashes sit at large negative residuals; pooled cross-year RR ≈ 1.0 on the standardised covariate). **This descriptive observation is not codified as MD-β r2 machinery.** It sits as pending work awaiting either (a) more crash-event accumulation across eras before codification, or (b) a conceptual framework that motivates the within-era operationalisation while acknowledging the cross-era divergence. Cross-reference: [Wave 2D §12.3](../analyses/descriptive/Q24-mdbeta-wave2d-2024-residual-tension/audit.md#123-wave-2d-adds-a-pre-window-covariate-recommendation) + [Wave 2E §5-§11 + Wave 2E §15.2 NEEDS-MORE-VALIDATION assessment](../analyses/descriptive/Q24-mdbeta-wave2e-phase-standardised-prewindow/audit.md).

---

## 6. Data availability audit hooks

Per [CONVENTIONS §3.6](../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file) named-count discipline. All numbers below reproduced by running an idempotent data-availability probe against `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` on 2026-07-16 with the LC-era stratum filter (`date >= 2022-04-04`, n=1524 rows).

### 6.1 Rest-day distribution across corpus

| Rest-day operand | Definition | LC-era rest-day count | Rest-day rate |
|---|---|---:|---:|
| Primary (`rest_day_p25`) | `total_steps < 30d rolling p25` (min_periods=15) | **404** | **26.5%** |
| Sensitivity (`rest_day_class`) | `exertion_class_lagged_lcera ∈ {none, light}` | **724** | **47.5%** |

The two operands diverge substantially in rate (~27% vs ~48%); the divergence identifies genuine operational-definition difference, not a data-quality flag. Primary is stricter (personal-baseline-relative); sensitivity is coarser (project-canonical class boundary). Both are load-bearing in different ways; the divergence is a foreseen sensitivity axis, not a bug.

**Note on `exertion_class` distribution** (LC-era n=1524):

| Class | n | rate |
|---|---:|---:|
| none | 372 | 24.4% |
| light | 352 | 23.1% |
| moderate | 198 | 13.0% |
| heavy | 276 | 18.1% |
| very_heavy | 256 | 16.8% |
| NaN | 70 | 4.6% |

Reproduces [Stage -1 audit §1](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md#1-corpus-summary) heavy + very_heavy + NaN counts; light + none + moderate breakdown is new to this MD.

### 6.2 Streak-length distribution (extends Stage -1 §4)

`gap=0` contiguous heavy-episode counts on LC-era, n=314 episodes total:

| L_bin | n | rate |
|---|---:|---:|
| 1 | 188 | 59.9% |
| 2 | 77 | 24.5% |
| 3 | 27 | 8.6% |
| 4+ | 22 | 7.0% |

Sub-bins within 4+ (for context, not for §4 primary bins):

| L | n |
|---:|---:|
| 4 | 12 |
| 5 | 6 |
| 6 | 1 |
| 7 | 1 |
| 8 | 1 |
| 10 | 1 |

Reproduces Stage -1 §4 exactly.

### 6.3 Streak-length × intensity cross-tab

Per-episode intensity fingerprint (fraction of episode's days that are `very_heavy`):

| L_bin | n episodes | mean vh_frac | median vh_frac | mean vh_count |
|---|---:|---:|---:|---:|
| 1 | 188 | 0.436 | 0.000 | 0.436 |
| 2 | 77 | 0.481 | 0.500 | 0.961 |
| 3 | 27 | 0.519 | 0.667 | 1.556 |
| 4+ | 22 | 0.538 | 0.550 | 2.636 |

**Interpretive discipline**: mean vh_frac is only mildly monotonically increasing with L_bin (0.44 → 0.48 → 0.52 → 0.54), so the streak-length × intensity confound is real but not extreme. Median vh_frac shows more variation (0 at L=1, 0.5 at L=2, 0.67 at L=3) driven by the L=1 bin's high count of heavy-only single-day episodes. Mean vh_count grows roughly linearly with L_bin (as expected mechanically). Stage D intensity-adjusted companion (§5 confound 2) uses this cross-tab as the anchor.

### 6.4 Streak-length × era cross-tab

`gap=0` heavy episodes by year × L_bin:

| Year | n episodes | L=1 | L=2 | L=3 | L=4+ |
|---|---:|---:|---:|---:|---:|
| 2022 | 44 | 26 | 11 | 2 | 5 |
| 2023 | 87 | 59 | 20 | 5 | 3 |
| 2024 | 81 | 50 | 23 | 4 | 4 |
| 2025 | 66 | 37 | 14 | 9 | 6 |
| 2026 (partial Jan-Jun) | 36 | 16 | 9 | 7 | 4 |

**Interpretive discipline**: the 2026 partial year has a notably higher rate of L=3 and L=4+ episodes relative to total (7+4 out of 36 = 30.6%, vs 8-11% in 2023 and 2024). This aligns with parent Q24 MD §10 caveat 1 (2026 heavy-rate elevation) and confirms the era-confound for §4 streak-length tests. Stage D era-stratified sensitivity arm (§5 confound 3) is the required companion.

### 6.5 Rest-adjacent heavy-episode counts (before + after)

For all 314 heavy-episode-ends on LC-era, rest-adjacency prevalence by K and direction:

| K | Rest-AFTER (primary p25) | Rest-BEFORE (primary p25) | Rest-AFTER (sensitivity class) | Rest-BEFORE (sensitivity class) |
|---:|---:|---:|---:|---:|
| 1 | 127 / 314 (40.4%) | 108 / 314 (34.4%) | 233 / 314 (74.2%) | 234 / 314 (74.5%) |
| 2 | 171 / 314 (54.5%) | 152 / 314 (48.4%) | 268 / 314 (85.4%) | 265 / 314 (84.4%) |
| 3 | 202 / 314 (64.3%) | 198 / 314 (63.1%) | 283 / 314 (90.1%) | 286 / 314 (91.1%) |

**Interpretive discipline**: rest-adjacent prevalence is high under both operands, especially the sensitivity (class-based) operand (90%+ at K=3). This means the rest-absent comparator arm at K=3 primary has n = 314 − 202 = **112 episodes**; the primary contrast has plenty of statistical resolution. The sensitivity operand at K=3 leaves only 314 − 283 = 31 rest-absent episodes; per-cell counts in the 2×2 contingency will be tight at K=3 under the sensitivity operand.

### 6.6 Rest-adjacency × crash-in-5d 2×2 (primary operand, K=3)

For all 314 heavy-episode-ends, using primary rest-day operand (p25) and K=3:

**Rest-AFTER-3 × crash-in-5d**:

| | crash-5d False | crash-5d True | Total |
|---|---:|---:|---:|
| rest_after_3 False | 100 | 12 | 112 |
| rest_after_3 True | 168 | 34 | 202 |
| Total | 268 | 46 | 314 |

- Crash rate on rest-after-adjacent: 34/202 = **16.8%**
- Crash rate on rest-after-absent: 12/112 = **10.7%**
- RR (rest-after-adjacent / rest-after-absent) = 16.8 / 10.7 = **1.57**

**Rest-BEFORE-3 × crash-in-5d**:

| | crash-5d False | crash-5d True | Total |
|---|---:|---:|---:|
| rest_before_3 False | 105 | 11 | 116 |
| rest_before_3 True | 163 | 35 | 198 |
| Total | 268 | 46 | 314 |

- Crash rate on rest-before-adjacent: 35/198 = **17.7%**
- Crash rate on rest-before-absent: 11/116 = **9.5%**
- RR (rest-before-adjacent / rest-before-absent) = 17.7 / 9.5 = **1.86**

**Interpretive discipline** (data-availability numbers only; no verdict): both directions show **sign-inversion relative to the §3.7 pre-committed direction** (rest-adjacent shows HIGHER crash rate in both directions). This is exactly the endogeneity pattern the §3.9 confound anticipates — rest-because-felt-bad enriches the rest-adjacent arm with crash-prone episodes. The Stage D descriptive audit will confirm sample-size stability + Wilson CIs + Fisher's exact test statistics; this MD-level data-availability sketch is not a verdict.

**Note on why to report the pre-committed direction anyway**: per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) and [`hypothesis_lock_process.md`](hypothesis_lock_process.md) discipline, pre-committed directions are locked *before* looking at the data. The §3.7 pre-commit stands as the reading axis even though the exploratory data-availability probe surfaces a probable sign-inversion. Stage D will confirm rigorously and report the finding as a sign-inversion, not silently flip the direction.

### 6.7 Crash-rate baseline anchor

From parent Stage D r4 §3 (inherited): crash-in-5d rate on strict-clean episode-ends = 9/52 = **17.3%** at +5d. Corpus baseline (LC-era) crash rate = 103/1524 = **6.8%**.

On the all-episodes pool this MD uses (n=314), crash-in-5d rate = 46/314 = **14.6%** — approximately 2× the corpus baseline, consistent with parent MD's compensatory-failure rate.

### 6.8 Anticipatory Stage H drafting-discipline note re sign-inversion pre-commit

Per [`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md) anticipatory-drafting-note discipline (same pattern §4.7 uses for the HA-P7 rolling-sum-predictor structural-autocorrelation flag). §6.6 exploratory data-availability probe surfaces a probable sign-inversion on both rest-adjacency directions (RR = 1.57 rest-after, RR = 1.86 rest-before) relative to the §3.7 pre-committed direction (rest-adjacent → LOWER crash rate). §3.9 confound 1 explicitly anticipates this pattern as the confounding-by-indication mechanism (rest-because-felt-bad enriches the rest-adjacent arm with crash-prone episodes).

**Anticipatory closure pathway**: if Stage D descriptive audit confirms the §6.6 exploratory sign-inversion — the rest-adjacent → HIGHER crash rate pattern, rather than the §3.7 pre-committed direction — any subsequent Stage H pre-registration on this test **must draft with sign-inversion as the pre-committed direction**. Reversing the direction pre-commit post-Stage-D without formal r-revision at this MD level would violate [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) descriptive-before-inference. Two acceptable closure paths:

- **(a)** Stage H drafts with the anti-committed direction (rest-adjacent → HIGHER crash rate) as primary, cites §3.9 endogeneity as the interpretive-caveat, and treats the mechanism-not-effect reading as the Stage H falsifier.
- **(b)** Stage D triggers a pre-Stage-H MD r2 revision that formally flips the §3.7 direction pre-commit; the r2 revision goes through fresh-session review before any Stage H pre-reg drafts.

Either closure preserves the descriptive-before-inference gate. The pattern to avoid: silently absorbing the Stage D sign-inversion into a Stage H pre-reg whose direction pre-commit reads as if it had always been the sign-inverted direction — that is data-driven-pre-commit, not descriptive-before-inference.

### 6.9 Path R2B revision closure: r2 supersedes r1 §6.8 anticipatory closure

Added at r2 2026-07-17 as the resolution of the r1 §6.8 anticipatory pathway. r1 §6.8 named two acceptable closure paths conditional on a Stage D confirmation of the §6.6 exploratory sign-inversion (pooled RR = 1.54 / 1.57 at K=3 primary rest-after on the omnibus operand):

- **Path (a)**: Stage H pre-reg drafts with sign-inversion as pre-committed direction on the omnibus operand.
- **Path (b)**: pre-Stage-H MD r2 revision that formally flips the §3.7 direction pre-commit on the omnibus operand.

**r2 executes neither path as originally framed.** Wave 2C's definitional-pair extension made a third path available: refine the primary operand from the omnibus `rest_day_p25` to `rest_day_p25_physical_strategic` (per §3.1.1) rather than flipping the direction on the omnibus. Path (a) is no longer applicable because r2 no longer treats the omnibus-operand pooled contrast as the primary; the primary at r2 is the strategic-subset contrast, on which Wave 2C pooled RR = 0.354 matches the §3.7 pre-commit direction preserved at r2. Path (b) is executed by this r2, but the direction pre-commit is not flipped; it is refined to bind explicitly to the strategic member of the §3.1.1 definitional pair (see §3.7 asymmetric direction pre-commit codification), with a mirror reversed direction pre-commit codified on the crisis member.

**Headline cell for Stage D under r2** (announced here for downstream Stage D pre-registration): `rest_day_p25_physical_strategic × heavy end_class × K=3 rest-after × crash-in-5d, era-pooled`, with **immediate era-stratified sensitivity companions** (same cell restricted to pre-cital era 2022-04-04 → 2024-04-08 + same cell restricted to post-cital era 2024-04-09 → 2026-06-05, reported side-by-side). Rationale:

- Uses the r2 primary operand from the Wave 2C definitional-pair extension (§3.1.1).
- Excludes very_heavy end_class from the headline: Wave 2D §4 showed very_heavy is the residual population where gevoelscore-conditioning alone does not work; very_heavy is reported as a sensitivity companion at Stage D per §3.5.1 sensitivity cell 1 (not as an alternative headline). **Generalisation-scope attestation added at r2 lock post-review absorption (recommendation 5 per fresh-session review)**: the r2 headline claim is scoped to heavy end_class only; the strategic-primary sign-flip is descriptively supported on heavy end_class at Wave 2D §4.1 (RR = 0.00) but NOT claimed to generalise to very_heavy end_class (RR = 3.50 residual per §3.5.1 sensitivity cell 1 + §5 confound 8). Any Stage S1 synthesis inference that the sign-flip generalises across intensity classes is out of scope for r2.
- Era-pooled headline with immediate era-stratified sensitivity companions documents the Wave 2B §9 + Wave 2C §5 era-instability while keeping the primary contrast at a sample-viable resolution (~80 strategic-True heavy-end episodes on the pooled read; per-era ~40 each). **Era-pooled headline rationale attestation added at r2 lock post-review absorption (recommendation 6 per fresh-session review)**: the era-pooled cell is the sample-viability-preferring primary at ~80 episodes; the immediate era-stratified companions (pre-cital ~40 + post-cital ~40) carry the falsifiability discipline for the era-primary-stratifier codification at §5 confound 7. Under §5 confound 7's era-as-primary-stratifier upgrade, the era-pooled headline is a pooled-across-a-primary-stratifier cell whose falsifiability rests on the immediate era-stratified companions being reported side-by-side without exception. Wilson CIs on per-era arms (~6 crashes / 40 episodes on strategic side) will be wider than the pooled read (~12 / 80); the pooled read is the tighter primary; the era-stratified companions are the era-instability-documenting sensitivity per Wave 2B §9 + Wave 2C §5.
- Descriptive-with-CI framing per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference); Wilson 95% CI + RR + RD per cell + bootstrap null per §3.6 machinery; no verdict at Stage D.

**Discipline preserved**: this headline cell is announced at MD-β r2 as the operand-locked Stage D primary read, NOT as a Stage H pre-registration. Any Stage H pre-registration downstream drafts in a separate session under reviewer-mode-with-authorization per §7 compression + lock discipline. r2 codifies the operand + machinery; Stage H drafts the inferential-test hypothesis + falsification bar as its own reviewer-mode-authorized artefact.

---

## 7. Compression and lock discipline

Producer-mode methodology MD per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). Lock discipline follows parent MD [`post_heavy_day_compensatory_rest.md` §12](post_heavy_day_compensatory_rest.md#12-compression-and-lock-discipline):

1. **Draft (this file, r1)**: producer-mode subagent draft with all inherited machinery propagated from parent Q24 MD LOCKED r1 (commit `58b7723`) + Stage -1 audit LOCKED r1 + Stage D descriptive audit LOCKED r4. Two new operand families defined (rest-adjacency + streak-length as crash-rate predictors); reframing of Q24.5 from unfalsifiable to testably predictive.
2. **Fresh-session `/research-methodology-review`**: reviewer-mode session (different Claude session, cold context) audits this MD against the CONVENTIONS §2.2 four-input bar + applicable 4-layer checklist items. Produces reviewer report at `docs/research/reviews/methodology-heavy_day_crash_risk_prediction-YYYY-MM-DD.md`.
3. **r2 lock with §3.6 compression**: reviewer fires absorbed inline per parent MD's compression discipline (mechanical clarifications, cross-cites, caveat additions); architectural changes escalate to r2-with-design-change and re-review.
4. **Stage D descriptive audit runs against r2-locked operand**: no Stage D output until the operand is locked.

**Compression rule** (inherited from parent MD): reviewer absorption at r2 is *mechanical* (clarifications, cross-cites, added caveats) NOT architectural (design changes). Any architectural change forces re-review before lock.

---

## 8. Lock log

| version | date | change |
|---|---|---|
| r1 | 2026-07-16 | Initial DRAFTED status. Producer-mode methodology MD for Q24 sub-part 5 (reframed from unfalsifiable to testably predictive rest-adjacency → crash-rate association) + consecutive-heavy-days-streak → crash-rate association. Inherits stratum + heavy-day definition + unit-of-analysis + comparator + pool-split machinery from parent Q24 MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1 (commit `58b7723`). New operand definitions: (a) `rest_day_p25` primary + `rest_day_class` sensitivity per [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair) definitional-pair discipline; (b) `streak_length` binned to `{1, 2, 3, 4+}` at episode-end unit. Primary outcome: `crash_in_5d` (episode-end + 5d window on `is_crash` column). Primary window: +5d (matches parent MD strict-clean +5d crash-rate signal of 17.3%). Statistical machinery: Fisher's exact + Wilson CIs + bootstrap B=10,000 + Cochran-Armitage trend test (streak-length) + RANDOM_SEED=20260716. Foreseen review trigger: rolling-window-predictor structural-autocorrelation flag per HA-P7 precedent + [`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md). Six confound classes pre-committed as caveat-class per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) (rest-day-choice endogeneity dominant; streak-length × intensity + × era confounds; baseline-drift on rest-day operand; rolling-sum-predictor autocorrelation; circularity with parent MD §3.5). Data-availability audit hooks §6 confirm sample viability: 314 episode-ends × 46 crash-in-5d gives a 14.6% base rate on the all-episodes pool; rest-adjacency prevalence 40-64% under primary p25 operand at K=1-3; streak-length bins 188/77/27/22 across L={1, 2, 3, 4+}. Sub-part 5 REFRAMED from Q24 MD §1.3 unfalsifiable framing to testably-predictive framing per §1.3 above; framing distinction load-bearing throughout §3.8. Awaiting fresh-session `/research-methodology-review` before lock. |
| r1 LOCKED | 2026-07-16 | Fresh-session methodology review absorbed from [`docs/research/reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md`](../reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md) (verdict: DEFENSIBLE with revision). Five surgical patches applied per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations) compression discipline (mechanical clarifications only, no architectural change; causal-vs-predictive-associational framing per §1.3 preserved throughout). **Patch 1** (§3.5, review L2.2 substantive-partial): added stationarity-assumption paragraph at the primary-contrast level naming the 4-year LC-era pooling as a substantive assumption partially addressed by §5 confound 7 (era-stratified sensitivity) + §5 confound 3 (streak-length × era cross-tab); caveat-class per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) not correction pre-committed. **Patch 2** (§3.9 confound 1 + §3.6, review I2.1 + I1.1 + L3.5 substantive-partial): added confounding-by-indication epidemiological citation (Salas 2001; Kyriacou & Lewis 2016 *JAMA*) as the literature construct for the rest-day-choice endogeneity mechanism at §3.9 confound 1; added log-binomial / modified-Poisson regression state-of-art (Zou 2004 *Am J Epidemiol*) at §3.6 as the natural Stage H extension for covariate-adjusted RR estimation. **Patch 3** (§5 confound 7, review I4.2 + L3.2 substantive-partial): added does-not-apply-redirected-to-analogue documentation for CONVENTIONS §3.7 trajectory-detrend audit hook — binary-outcome contingency tests have no windowed-mean to detrend, so era-stratified sensitivity (§5 confound 7 + confound 3) is the analogue drift-correction mechanism; documents explicitly why parent MD's §7.11 pre-lock absorption is not mirrored here. **Patch 4** (§5 confound 6, review I3.6 minor): added Stage-S1-synthesis reporting-discipline closure — Stage S1 synthesis must pick one of {this MD, parent Q24 MD} as headline per Q24 sub-part and cite the other as complementary (shared crash-in-5d outcome sample means the two are NOT independent evidence at Stage S1 level). **Patch 5** (new §6.8, discretionary user-endorsed): added anticipatory Stage H drafting-discipline note re sign-inversion pre-commit — if Stage D confirms §6.6 exploratory sign-inversion, subsequent Stage H pre-reg must (a) draft with sign-inversion as pre-committed direction citing §3.9 endogeneity as interpretive-caveat, OR (b) trigger a pre-Stage-H MD r2 revision formally flipping §3.7 direction pre-commit; either closure preserves the descriptive-before-inference gate. Pattern to avoid: silently absorbing Stage D sign-inversion into a Stage H pre-reg whose direction pre-commit reads as if always sign-inverted. Preserved byte-identically: §1 purpose + scope + reframing note, §2 inheritance table, §3.1-§3.4 operand definitions + K-ladder + outcome, §3.7 direction pre-commit, §3.8 predictive-only discipline, §4 streak-length arc, §5 confounds 1-5, §6.1-§6.7 data-availability audit hooks (all counts, all 2×2 tables), §7 compression-and-lock discipline, §9 cross-references. **STATUS**: LOCKED r1 2026-07-16 post-review absorption. Stage D descriptive audit for §3 rest-adjacency + §4 streak-length is now unblocked. |
| r2 DRAFT | 2026-07-17 | **r2 DRAFT status pending fresh-session methodology-review.** Producer-mode subagent revision under user delegation per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem. r2 codifies Path R2B per user-endorsed sequence 2026-07-16 → 2026-07-17, informed by five Wave 2 Stage -1 audits (Wave 2B rest-streak-precursor + Wave 2C reactive-vs-proactive-rest + Wave 2D 2024-residual-tension + Wave 2E phase-standardised-prewindow, plus Wave 2A on the MD-α axis referenced only for the citalopram phase-boundary), each LOCKED r1 2026-07-16, and their fresh-session methodology reviews (all DEFENSIBLE with revision). **DESCRIPTIVE-BEFORE-THEORY discipline binds r2**: no citation of `resilience_latent_state.md`, no latent-state variables (reserve, buffer, envelope-capacity, R(t)), no theoretical mechanism-framing that requires an unobserved variable. All findings framed as descriptive-with-CI patterns per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) + consistent-with, confounder-bounded caveat framing per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no). Five surgical patches applied per §7 compression discipline (mechanical clarifications + new subsections; no architectural change). **Patch 1** (§3.1 + new §3.1.1, per Wave 2C definitional-pair extension): added gevoelscore-conditioning definitional-pair extension introducing `rest_day_p25_physical_strategic` (primary; physical rest AND gevoelscore ≥ 5) + `rest_day_p25_physical_crisis` (sensitivity + endogeneity diagnostic; physical rest AND gevoelscore ≤ 3) + `rest_day_p25_physical_borderline` (descriptive-not-primary; physical rest AND gevoelscore = 4). Physical-rest-only semantic constraint codified per memory `project_rest_day_operand_semantics`: the `_physical_` infix flags that these operands do NOT measure cognitive rest, emotional rest, or planning quality. Wave 2C empirical anchors cited: pooled strategic-subset RR = 0.354; crisis-subset RR = 4.29; rest-day composition shift 18% → 27% → 25% → 53% → 56% across 2022 → 2026 partial. NaN handling per [CONVENTIONS §3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from `bout_level_recovery_dynamics.md`)](../CONVENTIONS.md#310-operationalisation-faithful-to-the-data-not-just-to-the-description): gevoelscore-NaN drops from analysis; 2022 pre-tracker-onset caveat flagged. **Patch 2** (new §3.5.1 + §5 confound 2 rewrite, per Wave 2D §12.2 joint-stratifier recommendation): added Joint end_class × gevoelscore-bucket stratification subsection codifying end_class (heavy vs very_heavy at episode-end) as **joint primary pre-commit stratifier alongside gevoelscore-conditioning** for the rest-adjacency arc. Wave 2D empirical anchor cited: within-2024 strategic-primary heavy-end RR = 0.00 (clean flip) vs very_heavy-end RR = 3.50 (all 3 strategic-primary 2024 crashes on very_heavy). §5 confound 2 upgraded from Stage D sensitivity companion to Stage D primary pre-commit stratifier for the rest-adjacency arc; streak-length arc confound 2 framing preserved verbatim. **Patch 3** (§5 confound 7 rewrite, per Wave 2B §13.10 escalate-tier + user decision 4): upgraded confound 7 from Stage D sensitivity companion to Stage D primary pre-commit stratifier for the rest-adjacency arc. Wave 2B §9 era-stratified RR by year cited (2022: 1.08, 2023: 2.02, 2024: 1.56, 2025: 0.78, 2026 partial: 0.57) as empirical rejection of the §3.5 stationarity assumption at descriptive-with-CI resolution. r2 era stratifier codified as **pre-cital vs post-cital 2-bucket at boundary 2024-04-09**, aligned with MD-α `recovery_phase` boundary between `pacing_habit_established` and `citalopram_modulated`. **Era caveat, 6-mechanism conflation with no causal attribution at n=1** codified verbatim per user decision 4: pre-cital vs post-cital stratifier is a temporal anchor at 2024-04-09 conflating (1) citalopram pharmacological effect + (2) learned-pacing behavioural evolution per MD-α §3.6 five-confound bundle + (3) tactical-Garmin-use improvement per memory `project_garmin_research_bias_boundary` + (4) natural LC disease-course trajectory + (5) envelope drift per MD-α Wave 2A §8 (pre-window `effective_exertion_min` per day 19.39 min on `pacing_habit_established` vs 5.17 min on `citalopram_modulated`) + (6) aging + seasonality. Stratifier does NOT identify medication effect at n=1; no causal claim about medication is made or supported. **Patch 4** (new §5 confound 8, per Wave 2D §11.2): added confound 8 for 2024 residual tension on the strategic-primary rest-adjacency arc. Wave 2C per-year strategic-primary RR cited (2023: 0.223, 2024: 0.929, 2025: 0.000, 2026 partial: 0.000); Wave 2D diagnosis as joint reading of candidate (b) pre-window-load partial-mitigation + candidate (e) intensity-interaction residual cited. (e) leg addressed via §3.5.1 joint-stratifier codification; (b) leg NOT codified at r2 per Option 1 (user decision 5). **Patch 5** (new "Deferred descriptive observation, pre-window cumulative load" paragraph after §5 confound 8): added the Wave 2D §12.3 + Wave 2E findings as pending work per user decision 5. Descriptive-only statement: phase-standardised pre-window 30d `effective_exertion_min` discriminates crash-in-5d on very-heavy end_class strategic-rest subset within 2024 (n=3 crashes at positive residuals vs n=12 non-crashes centred below phase mean); reads backwards outside 2024 (pooled cross-year RR ≈ 1.0). NOT codified as r2 machinery; awaiting either more crash-event accumulation across eras OR a conceptual framework motivating the within-era operationalisation. Cross-reference to Wave 2D §12.3 + Wave 2E §5-§11 + §15.2. **Patch 6** (§3.7 asymmetric direction pre-commit codification): extended §3.7 to codify direction pre-commit asymmetry across the §3.1.1 definitional-pair: strategic → LOWER (original §3.7 direction preserved on refined operand; Wave 2C RR = 0.354 empirical support); crisis → HIGHER (reversed direction; endogeneity diagnostic; Wave 2C RR = 4.29 empirical support); borderline → no direction pre-commit; omnibus operand → no direction pre-commit at r2 (composition-shift caveat). Added explicit supersession note that r2 refines primary operand rather than flipping direction on the omnibus. **Patch 7** (new §6.9, per user decision 9 headline cell + Path R2B closure): added Path R2B revision closure supersession subsection documenting how r2 supersedes r1 §6.8 anticipatory pathway. Neither r1 §6.8 path (a) nor (b) is executed as originally framed; r2 executes a third path made available by Wave 2C's definitional-pair extension: refine the primary operand rather than flip the direction pre-commit on the omnibus. Headline cell announced for Stage D: `rest_day_p25_physical_strategic × heavy end_class × K=3 rest-after × crash-in-5d, era-pooled` with immediate era-stratified sensitivity companions (pre-cital + post-cital side-by-side). Rationale for excluding very_heavy from headline cited per Wave 2D §4 finding. Sample viability ~80 strategic-True heavy-end pooled; per-era ~40 each. **Patch 8** (bulk anchor fix): §1.4 cross-reference line `§5 zero-vs-NaN` broken CONVENTIONS anchor changed to `§3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from bout_level_recovery_dynamics.md)`; §9 cross-reference bullet updated to add §3.3 + drop the broken §5-anchored zero-vs-NaN listing (§3.10 replaces it). Same anchor pattern applied within §3.1.1 for the gevoelscore-NaN handling paragraph. Fires the shorthand-terminology broken-anchor fix that Wave 2B/C/D/E audit locks already applied. **Patch 9** (§9 cross-reference additions): added Wave 2B + Wave 2C + Wave 2D + Wave 2E audits + their four review reports to §9. Did NOT add `resilience_latent_state.md`; descriptive-before-theory discipline forbids the citation. **Path R2A / R2C rejected alternatives**: Path R2A (minimal, caveat-only for Wave 2D findings) rejected because Wave 2D §4 intensity-interaction signal has internal replication via §5.2 + inherits from Wave 2B §10 whole-corpus intensity finding (per Wave 2D review report). Path R2C (full extension including pre-window covariate at r2) initially endorsed but reverted after (i) Wave 2E revealed the pre-window operand reads backwards pre-cital, and (ii) user's descriptive-before-theory guidance made codifying a theory-loaded covariate at r2 inappropriate. Path R2B (joint end_class stratifier now, pre-window covariate deferred) endorsed and implemented. **Preserved byte-identically**: §1 purpose + scope + reframing note; §2 inheritance table; §3.2-§3.3 K-ladder + rest-BEFORE definition; §3.4 outcome + parent-Q24 pool-split anchor + +5d sample-size table; §3.6 statistical framing (Fisher's exact + Wilson CI + bootstrap machinery + Zou 2004 state-of-art citation); §3.8 predictive-only discipline; §3.9 confounds 1-6 (r1 numbering preserved); §3.10 overlap-policy sensitivity; §4 streak-length arc (all sections; §4.7 rolling-window-predictor autocorrelation flag preserved); §6.1-§6.8 data-availability audit hooks (all counts, all 2×2 tables byte-identical; §6.8 anticipatory closure preserved and superseded via new §6.9); §7 compression + lock discipline; §8 lock log (r1 + r1 LOCKED entries preserved byte-identically; r2 DRAFT entry appended). **No r1 empirical numbers revised**: all §6.1-§6.7 counts + rates unchanged; Wave 2 audits all verified MD-β §6.1-§6.5 numbers byte-for-byte and MD-β §6.6 numbers byte-for-byte under NaN=False convention. **STATUS**: r2 DRAFT 2026-07-17 pending fresh-session `/research-methodology-review`. Stage D descriptive audit for §3 rest-adjacency arc will re-anchor against r2-locked operand family (`rest_day_p25_physical_strategic` primary + joint end_class × gevoelscore-bucket stratification + era-stratified sensitivity companions per §6.9 headline cell); §4 streak-length arc unblocking already surfaced at r1 LOCK, machinery unchanged at r2. |
| r2 LOCKED | 2026-07-17 | Fresh-session methodology review absorbed from [`docs/research/reviews/methodology-heavy_day_crash_risk_prediction-r2-2026-07-17.md`](../reviews/methodology-heavy_day_crash_risk_prediction-r2-2026-07-17.md) (verdict: DEFENSIBLE with revision; **descriptive-before-theory compliance PASSES load-bearing check**; 7 mechanical clarification absorbs all applied inline; no architectural revision; all four subagent-flagged tensions resolved as absorb-tier). Seven surgical patches per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations) compression discipline. **Recommendation 1 absorbed** (§3.5.1 sample-viability anchor per L1.2 absorb): bracketed one-liner added anchoring the ~80 pooled + ~40 per-era counts to `../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/output/phase_std_pre_window_ps_true_all_years.csv` filtered on `end_class == 'heavy'`; converts sample-viability claim from extrapolation to direct reproducible figure. **Recommendation 2 absorbed** (§3.5.1 autocorrelation attestation per L3.1 absorb): bracketed one-liner added attesting the joint-stratifier resampling inherits parent Q24 MD §7.10 block length = 1 discipline; forestalls the Stage D audit-hook question about whether the joint stratification changes the HA-P7 E[L]* factor-of-2 flag. **Recommendation 3 absorbed** (§3.1 absolute-step sensitivity companion per L4.1 absorb): added Wave 2D §7 absolute-step operand (`total_steps < 3000`) as Stage D sensitivity companion for the Wave 2C §5.5 rolling-baseline moves-with-envelope artefact test; Wave 2D empirical anchor cited (2024 RR shifts 0.929 → 0.652; pooled RR shifts 0.354 → 0.111 in sign-flip direction). Not codified as primary. **Recommendation 4 absorbed** (§3.7 reciprocal definitional-pair discipline per L4.2 absorb): reciprocal independence-doubling attestation added at end of §3.7 Interpretation-guidance paragraph — strategic pooled RR = 0.354 + crisis pooled RR = 4.29 are read from the same underlying joint distribution split (Wave 2C §6.5) and MUST NOT be reported as independent evidence at Stage S1; the asymmetric direction pre-commit is a within-operand-pair reading structure, not two independent tests. **Recommendation 5 absorbed** (§6.9 generalisation-scope attestation per L4.5 absorb): explicit generalisation-scope attestation added — r2 headline claim scoped to heavy end_class only; strategic-primary sign-flip descriptively supported on heavy end_class at Wave 2D §4.1 (RR = 0.00) but NOT claimed to generalise to very_heavy end_class (RR = 3.50 residual per §3.5.1 sensitivity cell 1 + §5 confound 8); Stage S1 inference of generalisation across intensity classes is out of scope for r2. **Recommendation 6 absorbed** (§6.9 era-pooled headline rationale attestation per L4.6 absorb): explicit reconciliation added between the "era-pooled headline" and the "era = Stage D primary pre-commit stratifier" codification at §5 confound 7 — era-pooled cell is the sample-viability-preferring primary at ~80 episodes; immediate era-stratified companions carry the falsifiability discipline for the era-primary-stratifier codification; the era-pooled + immediate era-stratified companion framing preserves definitional-pair discipline via side-by-side reporting without exception; Wilson CIs on per-era arms will be wider than the pooled read (~6/40 per era vs ~12/80 pooled). **Recommendation 7 absorbed** (Confound 8 vs deferred paragraph coherence per L1.3 absorb): bridging sentence added at top of Deferred descriptive observation paragraph — the (b) pre-window-load leg named in confound 8 is the specific mechanism deferred in this paragraph; the (e) intensity-interaction leg is codified at §3.5.1 + §5 confound 2. Makes the split coherent for a fresh reader without collapsing the confound-class vs pending-work-flag distinction. **Preserved byte-identically vs r2 DRAFT**: §1 purpose + scope + reframing note (except §1.4 anchor fix from r2 DRAFT); §2 inheritance table; §3.1 primary + sensitivity operand block (only new sensitivity-companion paragraph added at end); §3.1.1 gevoelscore-conditioning definitional-pair extension body (only sample-viability + autocorrelation attestations added at end); §3.2-§3.3 K-ladder + rest-BEFORE definition; §3.4 outcome + parent-Q24 pool-split anchor + +5d sample-size table; §3.5 primary contrast body + stationarity paragraph; §3.5.1 joint end_class × gevoelscore-bucket stratification (body preserved; two attestations appended at end); §3.6 statistical framing; §3.7 direction pre-commit asymmetry body (only reciprocal-attestation added at end); §3.8 predictive-only discipline; §3.9 confounds 1-6; §3.10 overlap-policy sensitivity; §4 streak-length arc all sections including §4.7 rolling-window-predictor autocorrelation flag; §5 confounds 1 + 3 + 4 + 5 + 6 + 7 body + 8 body + Deferred paragraph body (only bridging sentence prepended); §6.1-§6.8 data-availability tables (all counts + 2×2 byte-identical, verified against r1 LOCKED at commit `05fd4bf`); §6.9 Path R2B revision closure body (only two attestations added within existing rationale bullets); §7 compression + lock discipline; §8 lock log r1 + r1 LOCKED + r2 DRAFT rows preserved byte-identically. **No new r1 empirical numbers revised at r2 LOCKED** (attestation continues from r2 DRAFT). **STATUS**: LOCKED r2 2026-07-17 post-review absorption. Wave 2 arc fully landed. Stage D descriptive audit for §3 rest-adjacency arc unblocked against r2-locked operand family + joint stratifier + era-stratified sensitivity companions. §4 streak-length arc unchanged since r1 LOCK. |

---

## 9. Cross-references

- Parent Q24 MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1 (commit `58b7723`) — inherited stratum, heavy-day definition, unit-of-analysis (episode-end gap=0), comparator (matched-ordinary), pool-split machinery (§3.5 compensatory-success vs compensatory-failure), overlap policies (§5.2), null-machinery discipline (§7.10), envelope-drift caveat (§10 caveat 8).
- Sister MD [`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md) (drafted in parallel 2026-07-16) — Q24 sub-part 3 phase-stratification + dose-response trajectory outcomes; complementary arc to this MD's categorical-outcome arc.
- [Stage -1 audit `analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md`](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md) LOCKED r1 — episode-length distribution (§4), heavy-rate-by-year (§2), corpus summary (§1). Data-availability numbers in §6 reproduce §4 exactly.
- [Stage D descriptive audit r4 `analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md`](../analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md) LOCKED r4 — compensatory-failure sub-arm sample sizes (§3), crash-in-window base-rate anchor (16/125 at +3d; 9/52 at +5d).
- [`analyses/hypotheses/HA-P7/`](../analyses/hypotheses/HA-P7/) — predictive-classifier precedent (rolling-crash-count → crash; NOT-SUPPORTED). Rolling-sum-predictor structural-autocorrelation flag surfaced at result-review time per [`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md) — transferred anticipatorily to §4.7 streak-length machinery.
- [`analyses/hypotheses/HA01c-effective-exertion-shock/`](../analyses/hypotheses/HA01c-effective-exertion-shock/) — predictive-classifier precedent for exertion-shock → crash.
- [`methodology/hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md) — rolling-sum-predictor structural-autocorrelation factor-of-2 flag anticipatory-drafting-note discipline.
- [`methodology/permutation_null_block_length.md`](permutation_null_block_length.md) — E[L] block-length machinery + data-driven E[L]* diagnostic; §4.7 streak-length inherits.
- **Wave 2 Stage -1 audits informing r2 codification** (all LOCKED r1 2026-07-16):
  - [Wave 2B `analyses/descriptive/Q24-mdbeta-precursor-rest-streak/audit.md`](../analyses/descriptive/Q24-mdbeta-precursor-rest-streak/audit.md): 12-cell rest-adjacency × crash 2×2 grid; era-stratified + intensity-stratified 3-way cross-tabs; §13.10 escalate-tier findings driving r2 confound 2 + confound 7 primary-stratifier upgrades for the rest-adjacency arc.
  - [Wave 2C `analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md): gevoelscore-conditioned rest-day quadrants + reactive-vs-proactive rest 2×2s; §5 pooled proactive-strategic RR = 0.354 + crisis-reactive RR = 4.29 empirical anchors for §3.1.1 + §3.7 asymmetric direction pre-commit.
  - [Wave 2D `analyses/descriptive/Q24-mdbeta-wave2d-2024-residual-tension/audit.md`](../analyses/descriptive/Q24-mdbeta-wave2d-2024-residual-tension/audit.md): within-2024 by-intensity + per-episode diagnostic + pre-window load characterisation; §4 heavy RR = 0.00 vs very_heavy RR = 3.50 empirical anchor for §3.5.1 joint end_class × gevoelscore-bucket stratifier; §11.2 joint (b) + (e) reading for §5 confound 8.
  - [Wave 2E `analyses/descriptive/Q24-mdbeta-wave2e-phase-standardised-prewindow/audit.md`](../analyses/descriptive/Q24-mdbeta-wave2e-phase-standardised-prewindow/audit.md): phase-standardised pre-window covariate probe; §15.2 NEEDS-MORE-VALIDATION assessment underpinning the deferred descriptive observation paragraph after §5 confound 8.
  - Corresponding fresh-session methodology-review reports at [`../reviews/methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md`](../reviews/methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md) + [`../reviews/methodology-Q24-mdbeta-wave2c-reactive-vs-proactive-rest-2026-07-16.md`](../reviews/methodology-Q24-mdbeta-wave2c-reactive-vs-proactive-rest-2026-07-16.md) + [`../reviews/methodology-Q24-mdbeta-wave2d-2024-residual-tension-2026-07-16.md`](../reviews/methodology-Q24-mdbeta-wave2d-2024-residual-tension-2026-07-16.md) + [`../reviews/methodology-Q24-mdbeta-wave2e-phase-standardised-prewindow-2026-07-16.md`](../reviews/methodology-Q24-mdbeta-wave2e-phase-standardised-prewindow-2026-07-16.md).
- **MD-α methodology MD** [`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md) LOCKED r1: cited only for the 2024-04-09 citalopram-onset boundary that anchors r2's pre-cital vs post-cital 2-bucket era stratifier (§5 confound 7 revision). No integration of MD-α trajectory-arc framing beyond that boundary reference.
- [CONVENTIONS §1.2, §2.1, §3.1, §3.3, §3.6, §3.10, §4.2](../CONVENTIONS.md): producer-mode + descriptive-before-inference + personal-baseline + definitional-pair + named-counts + NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from `bout_level_recovery_dynamics.md`) + caveat-class framing.
- Memory pointer: `project_rest_day_operand_semantics`, the physical-rest-only semantic constraint codified in §3.1.1 for the r2 gevoelscore-conditioning definitional-pair operands.

---

*Producer-mode methodology MD. Update when (a) the fresh-session review verdict on r2 DRAFT lands and informs r2 LOCK compression, (b) Stage D descriptive audit results land against the r2 primary operand family (per-cell contingency + risk ratio + Wilson CI + bootstrap null outputs on the §6.9 headline cell), (c) a downstream per-HA pre-registration draws the operand into an inferential test, (d) additional crash-event accumulation across eras enables codification of the deferred pre-window cumulative-load observation (see §5 deferred-observation paragraph + Wave 2E cross-reference).*
