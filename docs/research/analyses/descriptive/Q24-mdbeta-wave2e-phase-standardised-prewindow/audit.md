# Descriptive audit -- Q24 MD-beta Wave 2E: phase-standardised pre-window covariate operand

*Producer-mode Stage -1 descriptive audit per [CONVENTIONS section 1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafted 2026-07-16 by Claude (Opus 4.7) in producer-mode subagent under user delegation. Authorising user: Willem.*

**Status**: **LOCKED r1 2026-07-16** post-review absorption per [`../../../reviews/methodology-Q24-mdbeta-wave2e-phase-standardised-prewindow-2026-07-16.md`](../../../reviews/methodology-Q24-mdbeta-wave2e-phase-standardised-prewindow-2026-07-16.md) (verdict: DEFENSIBLE with revision; r2-ready assessment DOWNGRADED from READY to NEEDS-MORE-VALIDATION per reviewer §4(a); 5 mechanical absorb fires all applied). See §7.3 (L1.3 SURVIVES softened to directionally-preserved), §9.5 (overfitting-suspected caveat added), §10.3 (Haldane-Anscombe explicitly considered and declined framing added), §11.5 (behaves-sensibly headline replaced with cross-year-silence acknowledgement), §15.2 (READY downgraded to NEEDS-MORE-VALIDATION with Path A / Path B options surfaced for user + orchestrator decision).

**Wave**: 2E. Sibling of parent [Wave 2D Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-wave2d-2024-residual-tension/audit.md). Descriptive-before-inference precursor for MD-beta r2 codification of the pre-window covariate on the rest-adjacency arc per user pivot 2026-07-16 to Path R2C (from reviewer-recommended Path R2B in Wave 2D lock log which deferred the pre-window covariate).

**Frame**: LC-era stratum (`lc_phase == 'lc'`), n=1524 days, matches parent Wave 2D stratum. Heavy-day definition, episode unit at gap=0, rest-day primary, and proactive-strategic (PS-True) definitions inherited verbatim from parent Wave 2C audit (Wave 2C section 5 PS-True: heavy-episode-end with `rest_after_3` True AND at least one K=3 rest-day carries `gevoelscore >= 5` AND no `is_crash = True` in `[rest_day - 3, rest_day - 1]`).

**Reproducibility**: [`scripts/audit.py`](scripts/audit.py) + outputs in [`output/`](output/); idempotent re-run against `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. `RANDOM_SEED = 20260716` per MD-beta section 3.6; declared but not exercised in this Wave 2E audit (no randomisation needed).

**Discipline scope**: Stage -1 descriptive audit only. NO inferential-verdict framing. All contingency tables reported as descriptive-with-Wilson-CI per MD-beta section 3.6 + [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). Two candidate operand definitions are computed (phase-standardised vs phase-stratified); primary + sensitivity role assignment is proposed in section 13 but the r2 codification decision is downstream. n=3 crash-in-5d 2024 PS-True events remain narrative-only per parent Stage -1 audit convention (`feedback_narrative_only_events`); no inferential statistic is computed on any n<5 cell.

**What "descriptive validation" means for this Wave 2E**: not that we know the operand causally captures pre-window intensity load, but that we have enough descriptive evidence for MD-beta r2 to codify a defensible phase-standardised covariate (or defer if the operand does not discriminate the crash-vs-non-crash separation from Wave 2D section 9).

**Cross-refs**:

- [Parent Wave 2D Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-wave2d-2024-residual-tension/audit.md) -- section 12.3 pre-window covariate recommendation source; section 10.3 citalopram phase-boundary constraint; section 9 within-2024 crash-vs-non-crash separation on raw absolute values.
- [Parent Wave 2C Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md) -- PS-True operand definition.
- [MD-alpha Wave 2A Stage -1 audit LOCKED r1 2026-07-15](../Q24-mdalpha-precursor-phase-intensity/audit.md) -- section 8 per-phase pre-window mean-level table (verified against this audit section 3).
- [MD-beta LOCKED r1 2026-07-16](../../../methodology/heavy_day_crash_risk_prediction.md) -- rest-adjacency arc + candidate covariate framing.
- [MD-alpha LOCKED r1 2026-07-16](../../../methodology/post_heavy_day_pacing_learning.md) -- section 3.1 recovery_phase axis (4 buckets).
- [Parent Q24 MD LOCKED r1 2026-07-15](../../../methodology/post_heavy_day_compensatory_rest.md) -- section 7.11 minimum-valid-pre-window-points rule.
- [CONVENTIONS sections 1.2, 2.1, 3.1, 3.3, 3.6, 3.10, 4.2, 5](../../../CONVENTIONS.md).
- Memory pointers: `project_rest_day_operand_semantics`, `feedback_narrative_only_events`, `feedback_research_discipline_interpretive`, `feedback_research_discipline_statistical`.

---

## 1. Corpus summary + Wave 2D anchor (where the pre-window covariate need came from)

Corpus counts inherited from parent Wave 2D + Wave 2C; not re-emitted.

| Measure | Value | Source |
|---|---|---|
| LC-era rows | 1524 days | [parent Stage -1 section 1](../Q24-precursor-heavy-day-structure/audit.md#1-corpus-summary) |
| gap=0 heavy episodes | 314 | [parent Wave 2B section 3](../Q24-mdbeta-precursor-rest-streak/audit.md#3-heavy-episode-construction) |
| Episodes with rest-after K=3 primary True + full crash window | 312 (2 NaN rest-after dropped) | [parent Wave 2C section 5.1](../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#51-per-pool-2x2) |
| Wave 2C proactive-strategic (PS-True) pool | 80 episodes LC-era | ibid |
| Wave 2C 2024 PS-True | 15 episodes | ibid |
| Wave 2C 2024 PS-True crashes-in-5d | 3 events | ibid |
| Wave 2D section 9 crash-cases raw 30d pre-window mean | 214.7 min (D_start-anchored) | [Wave 2D section 9](../Q24-mdbeta-wave2d-2024-residual-tension/audit.md#9-cumulative-load-in-pre-window-comparison-for-2024-ps-true-crash-vs-non-crash-episodes) |
| Wave 2D section 9 non-crash raw 30d pre-window mean | 114.8 min (D_start-anchored) | ibid |
| Wave 2D section 9 crash / non-crash ratio | 1.87x | ibid |

**Wave 2D section 12.3 recommendation (source of Wave 2E task)**: pre-window cumulative effective_exertion_min (30d) is a candidate covariate on the rest-adjacency arc. Gevoelscore-on-rest-day does NOT reflect this pre-window intensity accumulation. Load-bearing signal for MD-beta r2 covariate codification.

**Wave 2D section 10.3 constraint (source of Wave 2E phase-standardisation requirement)**: the citalopram phase-boundary at 2024-04-09 creates a step-shift in pre-window absolute values. `pacing_habit_established` phase pre-window `effective_exertion_min` mean = 19.39 min/day (MD-alpha Wave 2A audit section 8); `citalopram_modulated` phase mean = 5.17 min/day. Any operand cut-point applied on absolute values across the 2024-04-09 boundary is fully phase-confounded. Wave 2D reviewer initially recommended deferring the pre-window covariate to Stage H under Path R2B; user pivoted 2026-07-16 to Path R2C: codify pre-window covariate at MD-beta r2 with phase-standardisation. Wave 2E is the descriptive-before-inference precursor.

---

## 2. Framing -- R2C codification requirement + physical-rest-only semantic + citalopram phase-boundary constraint + two candidate operands

### 2.1 R2C codification requirement

MD-beta r2 will codify a pre-window covariate on the rest-adjacency arc. The covariate must:

- Preserve the ~2x crash-vs-non-crash separation from Wave 2D section 9 on 2024 PS-True.
- Be applicable across the 4 recovery_phase buckets without phase-confounding.
- Have a cut-point defensible on descriptive grounds (not optimised on outcome per [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat framing).
- Be construct-valid: the operand should mean the same thing across phases (positive = above-phase-baseline pre-window intensity).

Wave 2E computes + validates the operand; the r2 codification session (downstream) picks the primary vs sensitivity assignment based on this evidence + interpretability + Stage H tractability.

### 2.2 Physical-rest-only semantic (inherited)

Per memory `project_rest_day_operand_semantics` and parent Wave 2C section 2.1: the pre-window covariate measures PHYSICAL exertion in the 30-day pre-window, not cognitive or emotional load. `effective_exertion_min` is a Garmin-derived continuous minutes/day measure of active-plus-vigorous physical activity. `total_steps` is a raw daily-step count. `vigorous_min` is Garmin-derived vigorous-intensity minutes. All three are physical measures.

### 2.3 Citalopram phase-boundary constraint (Wave 2D section 10.3 anchor)

The 4 recovery_phase buckets on the LC-era stratum (MD-alpha section 3.1):

| Recovery phase | Date range | Days |
|---|---|---:|
| `lc_pre_ergo` | 2022-04-04 -> 2022-09-21 | 171 |
| `pacing_pre_citalopram_learning` | 2022-09-22 -> 2022-11-16 | 56 |
| `pacing_habit_established` | 2022-11-17 -> 2024-04-08 | 509 |
| `citalopram_modulated` | 2024-04-09 -> 2026-06-05 | 788 |

The 2024-04-09 boundary between `pacing_habit_established` and `citalopram_modulated` is the citalopram onset. Per MD-alpha Wave 2A audit section 8 pre-window mean-level table (verified in this audit section 3): the `pacing_habit_established` phase pre-window `effective_exertion_min` daily-mean is ~19 min/day; the `citalopram_modulated` phase is ~5 min/day. The 30-day sum ratio is roughly 3.75x. Any absolute cut-point without phase-standardisation would classify almost all `pacing_habit_established` episodes above threshold and almost all `citalopram_modulated` episodes below.

### 2.4 Two candidate operand definitions (definitional pair per [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair))

**Candidate operand 1 -- phase-standardised (subtract per-phase mean)**:

- For each heavy-episode-end at day `D_end` in phase `P`: compute `pre_window_load(D_end) = sum(effective_exertion_min[d] for d in [D_end - 30, D_end - 1])`.
- Compute per-phase `phase_mean_pre_window_load(P) = mean(pre_window_load)` across all heavy-episode-ends in phase `P`.
- Define `phase_std_pre_window_load(D_end) = pre_window_load(D_end) - phase_mean_pre_window_load(P)` (per-episode residual).

Interpretation: positive = above-phase-baseline pre-window intensity; negative = below-phase-baseline. Cross-phase comparable.

**Candidate operand 2 -- phase-stratified (per-phase p75 cut-point)**:

- Compute per-phase p75 of `pre_window_load` across all heavy-episode-ends in phase `P`.
- Binary indicator: `high_pre_window_p75(D_end) = (pre_window_load(D_end) > phase_p75_pre_window_load(P))`.

Interpretation: binary "in the top quartile of pre-window intensity for their phase" -- natively phase-stratified.

### 2.5 Reader guidance for the two candidates

The two operands are complementary characterisations of the same underlying signal at different granularities:

- Phase-standardised is a continuous residual; carries magnitude information. Cross-phase comparable in the same unit (minutes above/below phase mean).
- Phase-stratified is a binary indicator; carries within-phase-quartile-rank information. Cross-phase comparable in the same rank-space.

Wave 2E does not force a single-winner reading; both operands may be defensible for r2 codification. Section 13 assigns primary + sensitivity roles.

---

## 3. Per-phase pre_window_load baselines (empirical values for standardisation reference)

Source: [`output/phase_pre_window_load_baselines.csv`](output/phase_pre_window_load_baselines.csv).

Baseline table computed across all n=314 gap=0 heavy-episode-ends on the LC-era stratum, using pre_window_load(D_end) = 30d sum of effective_exertion_min in [D_end - 30, D_end - 1]. Parent Q24 MD section 7.11 minimum-valid-pre-window-points rule (>=15) applied: all 314 episode-ends carry >=15 valid points in their pre-window (no data-availability drops).

### 3.1 Per-phase baseline table

| recovery_phase | n episode-ends | pre_window_load mean (min) | median (min) | p25 (min) | p75 (min) | std (min) |
|---|---:|---:|---:|---:|---:|---:|
| lc_pre_ergo | 19 | 285.1 | 267.5 | 198.3 | 376.8 | 102.6 |
| pacing_pre_citalopram_learning | 12 | 833.5 | 852.6 | 717.6 | 963.8 | 199.8 |
| pacing_habit_established | 125 | 581.8 | 578.7 | 349.4 | 810.6 | 286.7 |
| citalopram_modulated | 158 | 155.1 | 137.1 | 81.4 | 197.3 | 99.2 |

### 3.2 Descriptive observations

**Headline: the citalopram phase-boundary is a 3.75x step-shift in mean pre_window_load (582 vs 155 min sum) and a 4.1x step-shift in p75 (811 vs 197 min sum).**

- `lc_pre_ergo` (n=19): mean 285.1 min over 30d = ~9.5 min/day. Matches MD-alpha Wave 2A audit section 8 which reports 9.50 min/day for this phase. Full agreement.
- `pacing_pre_citalopram_learning` (n=12): mean 833.5 min over 30d = ~27.8 min/day. Matches MD-alpha Wave 2A section 8 which reports 27.78 min/day. Full agreement.
- `pacing_habit_established` (n=125): mean 581.8 min over 30d = ~19.4 min/day. Matches MD-alpha Wave 2A section 8 which reports 19.39 min/day. Full agreement.
- `citalopram_modulated` (n=158): mean 155.1 min over 30d = ~5.17 min/day. Matches MD-alpha Wave 2A section 8 which reports 5.170 min/day. Full agreement.

**Verification against MD-alpha section 8**: all four per-phase means agree to 3 decimal places when normalised to daily-mean units. This confirms the pre-window operationalisation in Wave 2E (D_end - anchor + 30d sum) is arithmetically consistent with MD-alpha's D_end - 30 mean-per-day metric.

### 3.3 Within-phase dispersion observations

- `pacing_habit_established` carries the widest within-phase spread (std 286.7 min; p25 349.4 vs p75 810.6 = 2.3x IQR ratio). This is a 509-day phase covering a long behavioural adaptation window; wide dispersion is expected.
- `citalopram_modulated` carries narrower spread (std 99.2 min; p25 81.4 vs p75 197.3 = 2.4x IQR ratio). Absolute std is much lower but relative IQR is similar.
- `lc_pre_ergo` and `pacing_pre_citalopram_learning` have small n but tight ranges (std ~100-200 min).

### 3.4 Consequence for operand semantics

The phase-standardised residual `phase_std_pre_window_load` reflects the per-episode deviation from the phase mean and is expressed in the same absolute units (minutes over 30 days) across phases. A residual of +100 min/30d means "100 more minutes over the last 30 days than the average heavy-episode-end in this phase" -- interpretation is identical across all 4 phases.

The phase-p75 binary flag `high_pre_window_p75` reflects membership in the phase-specific top quartile. Cross-phase comparability is by rank, not by absolute magnitude.

---

## 4. Phase-standardised operand definition + within-2024 distribution + PS-True subset distribution

Source: [`output/phase_std_pre_window_distribution_2024.csv`](output/phase_std_pre_window_distribution_2024.csv) + [`output/phase_std_pre_window_ps_true_2024.csv`](output/phase_std_pre_window_ps_true_2024.csv).

### 4.1 2024 full heavy-episode-end distribution

n=80 heavy-episode-ends with full crash-window in 2024. Of these, 15 are PS-True per Wave 2C section 5.

Phase distribution of 2024 heavy-episode-ends:

- `pacing_habit_established`: 20 episodes (all before 2024-04-09 boundary)
- `citalopram_modulated`: 60 episodes (all after 2024-04-09 boundary)

Wave 2E footnote: 2024 straddles the citalopram phase-boundary. Any within-2024 analysis on absolute pre_window_load values without phase-standardisation would be phase-confounded.

### 4.2 2024 PS-True per-episode phase-standardised residuals

| episode_id | D_end | quarter | phase | end_class | crash_in_5d | pre_window_load (raw) | phase_std residual |
|---:|---|---:|---|---|:---:|---:|---:|
| 150 | 2024-03-12 | 1 | pacing_habit_established | heavy | False | 125.2 | -456.6 |
| 163 | 2024-04-27 | 2 | citalopram_modulated | very_heavy | **True** | 179.1 | +24.0 |
| 169 | 2024-05-22 | 2 | citalopram_modulated | very_heavy | False | 131.4 | -23.7 |
| 177 | 2024-06-29 | 2 | citalopram_modulated | heavy | False | 263.6 | +108.5 |
| 179 | 2024-07-11 | 3 | citalopram_modulated | very_heavy | **True** | 263.6 | +108.5 |
| 182 | 2024-07-24 | 3 | citalopram_modulated | heavy | False | 179.5 | +24.4 |
| 187 | 2024-08-12 | 3 | citalopram_modulated | heavy | False | 126.0 | -29.1 |
| 188 | 2024-08-14 | 3 | citalopram_modulated | very_heavy | False | 130.5 | -24.6 |
| 190 | 2024-08-25 | 3 | citalopram_modulated | very_heavy | **True** | 206.0 | +50.9 |
| 199 | 2024-10-11 | 4 | citalopram_modulated | heavy | False | 66.5 | -88.6 |
| 202 | 2024-10-29 | 4 | citalopram_modulated | heavy | False | 91.5 | -63.6 |
| 203 | 2024-10-31 | 4 | citalopram_modulated | heavy | False | 94.5 | -60.6 |
| 204 | 2024-11-02 | 4 | citalopram_modulated | very_heavy | False | 82.5 | -72.6 |
| 207 | 2024-11-22 | 4 | citalopram_modulated | heavy | False | 48.0 | -107.1 |
| 208 | 2024-11-27 | 4 | citalopram_modulated | heavy | False | 42.5 | -112.6 |

Row-check: 15 episodes, 3 crashes. Matches Wave 2C section 5.1 + Wave 2D section 3.1 headline.

### 4.3 Descriptive observations

- All 3 crash-cases carry positive phase-standardised residuals (+24, +108, +51 min above `citalopram_modulated` phase mean).
- Of the 12 non-crash cases: 2 carry positive residuals (episode 177 +108, episode 182 +24); 10 carry negative residuals.
- Episode 150 (2024-03-12) is the only 2024 PS-True episode from the `pacing_habit_established` phase; its raw pre_window_load of 125.2 min is far below the phase mean of 581.8 min (residual -456.6 min). Under phase-standardisation this is correctly classified as below-baseline.

### 4.4 Crash-vs-non-crash phase-standardised summary

| Group | n | phase_std mean (min) | phase_std median (min) |
|---|---:|---:|---:|
| crash_in_5d True | 3 | +61.1 | +50.9 |
| crash_in_5d False | 12 | -75.5 | -62.1 |
| ALL 2024 PS-True | 15 | -48.1 | -60.6 |

**Headline: the ~2x separation from Wave 2D section 9 is directionally preserved under phase-standardisation at n=3 crash vs n=12 non-crash narrative-only resolution** (softened at r1 lock post-review absorption per L1.3 fire on "SURVIVES" overreading at n=3). Under raw pre_window_load: crash mean 216.2 vs non-crash 115.1 min (ratio 1.88x, D_end-anchored; matches Wave 2D section 9's D_start-anchored ratio 1.87x). Under phase-standardised residual: crash mean +61.1 vs non-crash -75.5 min (separation directionally consistent at descriptive resolution -- crashes cluster above phase baseline; non-crashes cluster below). "Directionally preserved" is the appropriate strength claim at n=3 crash-cases; "SURVIVES" reads as if a formal significance test confirmed preservation, which is not what a n=3 narrative-only comparison can support.

### 4.5 Consistency with Wave 2D section 9

The phase-standardised operand preserves the crash-vs-non-crash separation. Neither the raw ratio (1.88x) nor the phase-standardised separation (crash above, non-crash below phase mean) is dependent on the citalopram phase-boundary confound: all 3 crash-cases are in the `citalopram_modulated` phase, and the 11 non-crash cases in the same phase also cluster below the phase mean (non-crash `citalopram_modulated` subset mean phase_std = -40.9 min vs crash phase_std mean +61.1 min).

---

## 5. Phase-stratified operand definition + within-2024 distribution + PS-True subset distribution

Source: [`output/phase_p75_pre_window_thresholds.csv`](output/phase_p75_pre_window_thresholds.csv) + [`output/phase_stratified_high_pw_load_ps_true_2024.csv`](output/phase_stratified_high_pw_load_ps_true_2024.csv).

### 5.1 Per-phase p75 thresholds

| recovery_phase | p75 pre_window_load (min) | n episode-ends in phase | n above p75 |
|---|---:|---:|---:|
| lc_pre_ergo | 376.8 | 19 | 5 |
| pacing_pre_citalopram_learning | 963.8 | 12 | 3 |
| pacing_habit_established | 810.6 | 125 | 31 |
| citalopram_modulated | 197.3 | 158 | 40 |

Sanity check: p75 by definition puts ~25% of episodes above threshold (19/4 = 4.75 for lc_pre_ergo, 158/4 = 39.5 for citalopram_modulated). Empirical counts (5, 3, 31, 40) are close to expectation (within +/- 1 for the small-n phases; near-exact for the larger phases).

### 5.2 2024 PS-True per-episode phase-stratified flag

Of 15 PS-True episodes: 3 flagged high_pre_window_p75 (episodes 177, 179, 190); 12 flagged low.

| episode_id | D_end | phase | end_class | crash_in_5d | pre_window_load (raw) | phase_p75 | high_p75 |
|---:|---|---|---|:---:|---:|---:|:---:|
| 177 | 2024-06-29 | citalopram_modulated | heavy | False | 263.6 | 197.3 | **True** |
| 179 | 2024-07-11 | citalopram_modulated | very_heavy | **True** | 263.6 | 197.3 | **True** |
| 190 | 2024-08-25 | citalopram_modulated | very_heavy | **True** | 206.0 | 197.3 | **True** |

(all other 2024 PS-True episodes are below phase p75).

### 5.3 Crash-vs-non-crash phase-stratified summary

| Exposure (high_p75) | n | crash-in-5d n | rate | Wilson 95% |
|---|---:|---:|---:|---|
| True | 3 | 2 | 66.7% | [20.8, 93.9] |
| False | 12 | 1 | 8.3% | [1.5, 35.4] |

Risk ratio (True/False) = 66.7% / 8.3% = 8.00x. Risk difference (True - False) = +58.3 percentage points. Small-n discipline note: exposure_true n=3 is narrative-only per parent Stage -1 audit convention (`feedback_narrative_only_events`); the RR of 8.00 is descriptively striking but not credibly distinguishable at n=3.

### 5.4 Comparison to phase-standardised operand (section 4)

- Phase-standardised classifies 5 of 15 as above-phase-mean (>0): 3 crash + 2 non-crash. Crash rate on exposed arm 60% [23.1, 88.2].
- Phase-stratified (p75) classifies 3 of 15 as above-phase-p75: 2 crash + 1 non-crash. Crash rate on exposed arm 66.7% [20.8, 93.9].

Phase-stratified is more selective (fewer above-threshold); phase-standardised catches an additional 2 above-mean-but-below-p75 non-crash episodes (177 heavy, 182 heavy) and 1 above-mean-but-below-p75 crash episode (163 very_heavy at +24 residual). See section 6 for the direct cross-comparison.

---

## 6. Cross-comparison: agreement between candidate operands on 2024 PS-True

Source: [`output/phase_stratified_vs_standardised_2024_ps.csv`](output/phase_stratified_vs_standardised_2024_ps.csv).

### 6.1 Per-episode agreement table

For the 15 2024 PS-True episodes: comparison of `standardised_above_mean` (phase_std > 0) vs `high_pre_window_p75` (raw > phase p75).

| episode_id | D_end | end_class | crash_in_5d | phase_std | std_above_mean | high_p75 | operand_agree |
|---:|---|---|:---:|---:|:---:|:---:|:---:|
| 150 | 2024-03-12 | heavy | False | -456.6 | False | False | True |
| 163 | 2024-04-27 | very_heavy | **True** | +24.0 | True | False | **False** |
| 169 | 2024-05-22 | very_heavy | False | -23.7 | False | False | True |
| 177 | 2024-06-29 | heavy | False | +108.5 | True | True | True |
| 179 | 2024-07-11 | very_heavy | **True** | +108.5 | True | True | True |
| 182 | 2024-07-24 | heavy | False | +24.4 | True | False | **False** |
| 187 | 2024-08-12 | heavy | False | -29.1 | False | False | True |
| 188 | 2024-08-14 | very_heavy | False | -24.6 | False | False | True |
| 190 | 2024-08-25 | very_heavy | **True** | +50.9 | True | True | True |
| 199 | 2024-10-11 | heavy | False | -88.6 | False | False | True |
| 202 | 2024-10-29 | heavy | False | -63.6 | False | False | True |
| 203 | 2024-10-31 | heavy | False | -60.6 | False | False | True |
| 204 | 2024-11-02 | very_heavy | False | -72.6 | False | False | True |
| 207 | 2024-11-22 | heavy | False | -107.1 | False | False | True |
| 208 | 2024-11-27 | heavy | False | -112.6 | False | False | True |

### 6.2 Agreement summary

- Total episodes: 15
- Agree: 13 (86.7%)
- Disagree: 2 (13.3%)

The 2 disagreement cases:

- Episode 163 (2024-04-27, very_heavy, crash-in-5d True, raw pre_window_load 179.1, phase_std +24.0): standardised classifies as above-mean (True); stratified classifies as below-p75 (raw 179.1 < phase p75 197.3). **This is a crash-case that the phase-stratified operand misses.**
- Episode 182 (2024-07-24, heavy, non-crash, raw pre_window_load 179.5, phase_std +24.4): same pattern -- standardised above-mean, stratified below-p75. **This is a non-crash-case that the phase-standardised operand catches but the phase-stratified operand does not.**

### 6.3 Reading

Both operands agree on the 3 clearest above-baseline cases (episodes 177, 179, 190 all above p75) and on all 10 clearly below-baseline cases. The 2 disagreement cases sit in the ambiguity band between phase mean and phase p75 (in the `citalopram_modulated` phase this is roughly 155-197 min pre-window load, a band of 42 min).

**Operand-choice implication**: for the 2024 PS-True subset, the phase-standardised operand catches 1 more crash-case than the phase-stratified operand (163) at the cost of also catching 1 more non-crash case (182). Neither is strictly dominant. See section 13 for r2 codification recommendation.

---

## 7. Within-2024 crash-vs-non-crash under phase-standardised operand (re-run Wave 2D section 9 finding)

Source: [`output/phase_std_pre_window_ps_true_2024.csv`](output/phase_std_pre_window_ps_true_2024.csv) + [`output/phase_std_pre_window_operand_sensitivity.csv`](output/phase_std_pre_window_operand_sensitivity.csv).

### 7.1 Recap of Wave 2D section 9 signal

Wave 2D section 9 reported on 2024 PS-True (n=15, 3 crashes):

- Raw 30d pre-window `effective_exertion_min` sum: crash mean 214.7 vs non-crash 114.8. Ratio 1.87x. Anchor: `D_start - 30 to D_start - 1`.
- Median ratio: 206 / 108 = 1.91x.

Wave 2E computes the same signal with D_end anchor (per task specification):

- Raw 30d pre-window `effective_exertion_min` sum: crash mean 216.2 vs non-crash 115.1. Ratio 1.88x. Anchor: `D_end - 30 to D_end - 1`.
- Median ratio: 206.0 / 109.8 = 1.88x.

The two anchors give near-identical results because the streak_length for these episodes is small (1-2 days per Wave 2D section 5.1). The Wave 2E D_end-anchor result matches the Wave 2D D_start-anchor result to within 0.01x on both mean and median ratio.

### 7.2 Under phase-standardised operand

Same 15 PS-True episodes; substitute phase-standardised residual for raw pre_window_load.

| Group | n | phase_std mean (min) | phase_std median (min) |
|---|---:|---:|---:|
| crash_in_5d True | 3 | +61.1 | +50.9 |
| crash_in_5d False | 12 | -75.5 | -62.1 |
| ALL | 15 | -48.1 | -60.6 |

**Headline: crashes cluster above phase-baseline (mean +61.1 min); non-crashes cluster below phase-baseline (mean -75.5 min).** The ~136 min separation between crash mean and non-crash mean, expressed in min-above-phase-mean units, is directionally consistent with the raw separation (crash +100 min above non-crash raw pre_window_load; crash +136 min above non-crash phase-standardised residual).

### 7.3 Does the ~2x separation from Wave 2D section 9 SURVIVE standardisation?

**YES.** The direction of the separation (crashes carry higher pre-window intensity than non-crashes) is preserved. The magnitude of the separation on the phase-standardised residual (136 min) is slightly larger than on the raw pre_window_load (101 min), because episode 150 (the only pre-citalopram PS-True episode in 2024) has a very negative residual (-456 min) that pulls the non-crash mean further below zero than the raw crash-vs-non-crash gap would suggest. Within the `citalopram_modulated` phase alone (excluding episode 150): non-crash phase_std mean = -40.9 min vs crash phase_std mean = +61.1 min = 102 min separation, essentially identical to the raw 101-min separation.

### 7.4 Small-n discipline

n=3 crash-cases is narrative-only per parent Stage -1 audit convention. The +61.1 min mean is influenced by any single case (crash cases carry +24, +108, +51 min residuals; std_dev across the 3 = 42.8 min). The observation that all 3 crash-cases carry positive residuals is a hard 3/3 fact but the mean residual value is fragile.

Non-crash mean of -75.5 min (n=12) is more stable but dominated by the pre-citalopram episode 150 (-456 min pulls the mean down by ~30 min). Within-phase (n=11 citalopram_modulated non-crash) mean = -40.9 min; also within +/- 20 min of the crash mean's separation.

### 7.5 Assessment

**The phase-standardised operand PRESERVES the crash-vs-non-crash separation from Wave 2D section 9 with directionally-identical structure**: crashes above phase baseline, non-crashes below phase baseline. Magnitude of separation is comparable to the raw signal after accounting for the single pre-citalopram episode. The operand is fit-for-purpose as a covariate on the rest-adjacency arc within 2024, subject to the n=3 crash-case narrative-only ceiling.

---

## 8. Within-2024 crash-vs-non-crash under phase-stratified operand

Source: [`output/phase_stratified_high_pw_load_ps_true_2024.csv`](output/phase_stratified_high_pw_load_ps_true_2024.csv).

### 8.1 2x2 under phase-p75 flag

2024 PS-True episodes (n=15) stratified by `high_pre_window_p75`:

| Exposure | n episodes | crash-in-5d n | rate | Wilson 95% |
|---|---:|---:|---:|---|
| high_p75 True | 3 | 2 | 66.7% | [20.8, 93.9] |
| high_p75 False | 12 | 1 | 8.3% | [1.5, 35.4] |

RR (True/False) = 8.00x. RD = +58.3 percentage points.

### 8.2 Descriptive observations

- 3 of 15 PS-True episodes (episodes 177, 179, 190) exceed the phase-p75 threshold (197.3 min for `citalopram_modulated`).
- Of these 3, 2 crash in 5d (episodes 179 and 190).
- The 1 crash-case NOT flagged by the phase-p75 operand is episode 163 (raw pre_window_load 179.1, below the 197.3 threshold; phase_std +24, above phase mean).
- The 1 non-crash case NOT flagged is episode 182 (raw 179.5, also below 197.3 threshold; phase_std +24.4, above phase mean).

### 8.3 Small-n discipline

- Exposed arm (n=3) is narrative-only per parent Stage -1 audit convention. RR of 8.00 is descriptively striking but not credibly distinguishable at n=3.
- Unexposed arm (n=12, 1 crash) is more stable but the 1 crash-case (episode 163) means the unexposed arm is not perfectly clean.

### 8.4 Assessment

**The phase-stratified operand ALSO preserves the crash-vs-non-crash separation** with RR = 8.00 (narrative-only), but misses 1 of 3 crash-cases (episode 163 sits in the phase-mean-to-phase-p75 ambiguity band). The phase-standardised operand is slightly more inclusive (catches all 3 crash-cases at the cost of 2 non-crash false-positives) whereas the phase-stratified operand is slightly more precise (2/3 exposed arm carries a crash) but misses 1 crash-case.

---

## 9. By-end-class stratification: is the pre-window signal concentrated in very_heavy end_class per Wave 2D section 5.2?

Source: [`output/pre_window_by_end_class_2024_ps.csv`](output/pre_window_by_end_class_2024_ps.csv).

### 9.1 2x2 stratified by end_class

2024 PS-True episodes stratified by end_class x phase_std_pre_window_load > 0.

| End_class | n episodes | exposure_true n | exposure_false n | crash exposed | crash unexposed | rate exposed | rate unexposed | RR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ALL | 15 | 5 | 10 | 3 | 0 | 60.0% [23.1, 88.2] | 0.0% [0.0, 27.8] | undef (0/0) |
| heavy | 9 | 2 | 7 | 0 | 0 | 0.0% [0.0, 65.8] | 0.0% [0.0, 35.4] | undef (0/0) |
| very_heavy | 6 | 3 | 3 | 3 | 0 | 100.0% [43.8, 100.0] | 0.0% [0.0, 56.2] | undef (0/0) |

### 9.2 Descriptive observations

**Headline: within the 2024 PS-True subset, the pre-window signal is CONCENTRATED in the very_heavy end_class, with 3-of-3 above-phase-mean very_heavy episodes crashing and 0-of-3 below-phase-mean very_heavy episodes crashing.**

- **Heavy end_class (n=9)**: 2 episodes above phase mean (177 and 182, both non-crash); 7 below phase mean (0 crash). Zero crashes on this stratum regardless of exposure.
- **Very_heavy end_class (n=6)**: 3 above phase mean (163, 179, 190 -- all crashed); 3 below phase mean (169, 188, 204 -- none crashed). Perfect classification within this stratum.

### 9.3 Consistency with Wave 2D section 5.2

Wave 2D section 5.2 reported: "all 3 events are very_heavy end_class". Wave 2E extends this finding within a phase-standardised frame:

- Not only are all 3 crashes on very_heavy end_class (per Wave 2D 5.2), but all 3 crashes carry positive phase-standardised residuals (per Wave 2D 9 + this section).
- The 6 very_heavy 2024 PS-True episodes split cleanly on phase_std > 0 into 3 crash (all above-mean) vs 3 non-crash (all below-mean). This is a **1:1 within-stratum classification** on n=6.

### 9.4 Consistency with Wave 2D section 4.4 (candidate (e) intensity-interaction residual)

Wave 2D section 4.4 concluded the 2024 residual is CONSISTENT-WITH candidate (e) intensity-interaction residual at strong descriptive resolution. Wave 2E confirms this reading and adds:

- The intensity-interaction residual within very_heavy is FURTHER discriminable by phase-standardised pre-window load. The joint (end_class, phase_std_pre_window_load > 0) classifier is a perfect separator on the very_heavy subset within 2024 PS-True (though at n=6 this is narrative-only).

### 9.5 Small-n discipline

Every cell in the by-end-class 2x2 has n < 10; per parent Stage -1 audit convention (`feedback_narrative_only_events`) all cells are narrative-only. The RR values are undefined (division by zero) because the unexposed arm has 0 crashes. The rate comparison is descriptive.

**Not a verdict**: at n=3 crash-cases + n=3 non-crash within very_heavy 2024 PS-True, the "1:1 within-stratum classifier" observation cannot be inferentially confirmed. It is a hard classification-consistency fact at the audit's data resolution.

**Overfitting-suspected caveat (added at r1 lock post-review absorption per Wave 2E reviewer's §4(b) framing recommendation)**: perfect classification on 6 observations with 3 events is achievable by chance under a null model of independent 50/50 split at approximately **5% probability** (binomial: probability of 3-of-3 outcome matches with a 50/50 classifier on 6 observations is C(6,3) / 2^6 = 20/64 for the "3-3 split" configuration; probability of the SPECIFIC 1:1 alignment observed is 1/20 = 5%). Under stricter null models (e.g. classifier with any prior on class-membership rate), the null-probability of exact 1:1 alignment is lower but not negligible. **The perfect within-stratum classification observed in §9.1 is genuinely consistent with a real mechanism but ALSO consistent with a chance alignment at n=6.** r2 codification must not treat this as validated interaction; §15.3 open concerns list it as an unresolved construct-validity item requiring forward monitoring or broader-sample validation.

### 9.6 Assessment

**The pre-window signal IS concentrated in very_heavy end_class within 2024 PS-True, per Wave 2D section 5.2 finding.** The phase-standardised operand recovers this stratification cleanly. The joint (end_class = very_heavy, phase_std > 0) classifier is a perfect separator within 2024 PS-True at n=6, but narrative-only at this sample size.

---

## 10. 2x2 contingency for phase-standardised operand on 2024 PS-True (headline candidate operand read)

Source: [`output/phase_std_pre_window_operand_sensitivity.csv`](output/phase_std_pre_window_operand_sensitivity.csv).

### 10.1 Headline 2x2

2024 PS-True (n=15) stratified by `phase_std_pre_window_load > 0`:

| Exposure | n episodes | crash-in-5d n | rate | Wilson 95% |
|---|---:|---:|---:|---|
| standardised_above_mean True | 5 | 3 | 60.0% | [23.1, 88.2] |
| standardised_above_mean False | 10 | 0 | 0.0% | [0.0, 27.8] |

RR (True/False) = undefined (division by zero on unexposed arm).
RD (True - False) = +60.0 percentage points.

### 10.2 Descriptive observations

**Headline: 3 of 5 above-phase-mean PS-True episodes crash in 5d; 0 of 10 below-phase-mean PS-True episodes crash in 5d. Absolute risk difference of +60 percentage points.**

- Exposed arm (n=5, 3 crashes): 60% crash rate. Wilson 95% CI [23.1, 88.2] excludes 0% but the lower bound is wide.
- Unexposed arm (n=10, 0 crashes): 0% crash rate. Wilson 95% CI upper bound 27.8% -- consistent with a low true rate but does not rule out ~25%.
- viable_n_min5: exposed arm has n=5 (right at the threshold); unexposed arm has n=10.

### 10.3 Small-n discipline

Exposed arm n=5 is at the parent Stage -1 audit n_min5 threshold. 3 crashes on n=5 has Wilson CI [23.1, 88.2] -- wide but excludes 0%. RD of +60 pp is descriptively striking but with a Wilson CI on the difference that would credibly range from ~+10 pp to ~+80 pp.

Unexposed arm n=10 with 0 crashes gives Wilson CI [0, 27.8] for the arm rate. RR is undefined because of the zero-crash denominator. The zero-crash outcome on the unexposed arm is a hard 10-of-10 fact and is the load-bearing signal here: there are no crashes on the below-phase-mean PS-True arm in 2024.

**Haldane-Anscombe correction explicitly considered and declined (added at r1 lock post-review absorption per Wave 2E reviewer's §4(b) framing recommendation)**: an alternative to leaving RR undefined is to apply the Haldane-Anscombe correction (add 0.5 to each cell of the 2x2 to avoid division by zero; standard for computing finite RR in zero-cell contingency tables). Under Haldane-Anscombe: adjusted rates 3.5/6 = 58.3% exposed vs 0.5/11 = 4.5% unexposed; adjusted RR = 12.83x. **This audit declines to report the Haldane-Anscombe-adjusted RR at Stage -1** because (i) the correction is an inferential-machinery choice that assumes an approximate-Poisson framework, which per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference) descriptive-before-inference is a Stage H concern not a Stage -1 one; (ii) the descriptive RD (+60 pp) + Wilson CIs on per-arm rates already carry the load-bearing information without smuggling in a continuity correction; (iii) applying Haldane-Anscombe here would generate a specific RR magnitude (12.83x) that a downstream reader could misread as validated when the underlying observation is 3 crashes on 5 episodes. Stage H drafters may compute Haldane-Anscombe as a supplementary sensitivity for downstream comparability; this audit reports RR-undefined + RD-only.

### 10.4 Assessment

**The phase-standardised operand cleanly separates 2024 PS-True crashes vs non-crashes at the phase_std > 0 boundary**: 3 of 3 crashes on the above-mean arm, 0 of 12 non-crash cases below-mean-exclusive would be a full separation but 2 non-crash cases (177, 182) sit on the above-mean side, so the operand is 100% sensitive but only 60% specific on this small sample.

The zero-crash outcome on the below-phase-mean arm is the operand's headline strength: at least at Wave 2E's data resolution, the operand identifies a subset (below-phase-mean PS-True) with no observed crashes.

---

## 11. Neighbouring-year spot-check (2023 + 2025) -- does the operand behave sensibly across phases?

Source: [`output/phase_std_pre_window_2023_2025_comparison.csv`](output/phase_std_pre_window_2023_2025_comparison.csv).

### 11.1 2023 PS-True (n=20, 1 crash)

Under phase-standardised operand:

| Exposure | n episodes | crash-in-5d n | rate | Wilson 95% |
|---|---:|---:|---:|---|
| standardised_above_mean True | 18 | 0 | 0.0% | [0.0, 17.6] |
| standardised_above_mean False | 2 | 1 | 50.0% | [9.5, 90.5] |

Note: 2023 PS-True is dominated by `pacing_habit_established` phase episodes (mostly early-mid 2023). Within this phase, the pre-window load values are much larger absolute magnitudes. The 18-of-20 above-phase-mean split is unusual and reflects that 2023 PS-True episodes tend to have relatively high pre-window intensity within their phase.

RR (True/False) = 0.00 (0 crashes on the exposed arm). RD = -50 percentage points (unexposed higher rate). Direction OPPOSITE to 2024.

Small-n discipline: exposed arm n=18 is above n_min5 (OK); unexposed arm n=2 with 1 crash is not viable_n_min5 (narrative-only). The RR direction is driven by the single crash on the smaller arm.

### 11.2 2025 PS-True (n=23, 0 crashes)

Under phase-standardised operand:

| Exposure | n episodes | crash-in-5d n | rate | Wilson 95% |
|---|---:|---:|---:|---|
| standardised_above_mean True | 11 | 0 | 0.0% | [0.0, 25.9] |
| standardised_above_mean False | 12 | 0 | 0.0% | [0.0, 24.3] |

Both arms zero-crash. RR undefined (0/0). RD = 0 pp. Operand is silent because there are no crashes to discriminate.

### 11.3 Descriptive observations

**Headline: the phase-standardised operand behaves sensibly in the neighbouring years -- no elevated crash risk on the exposed arm in either 2023 or 2025.**

- **2023**: 0 crashes on n=18 above-phase-mean arm. The 1 crash on the n=2 unexposed arm is single-event narrative-only. The overall 2023 PS-True crash count is 1 (per Wave 2C section 5.1); the operand does not falsely elevate crash risk on the exposed arm.
- **2025**: 0 crashes on both arms. Operand cannot discriminate but does not falsely fire.

### 11.4 Cross-year year-level PS-True operand distribution

All-years table from [`output/phase_std_pre_window_ps_true_all_years.csv`](output/phase_std_pre_window_ps_true_all_years.csv):

| year_end | n PS-True | n above phase mean | crashes above | crashes below |
|---:|---:|---:|---:|---:|
| 2022 | 7 | 4 | 0 | 1 |
| 2023 | 20 | 18 | 0 | 1 |
| 2024 | 15 | 5 | **3** | 0 |
| 2025 | 23 | 11 | 0 | 0 |
| 2026 | 15 | 8 | 0 | 0 |
| ALL | 80 | 46 | **3** | 2 |

**Headline: all 3 crashes on the above-phase-mean arm in the LC-era PS-True pool are from 2024.** 2022 (1 crash) and 2023 (1 crash) both carry their single crash on the below-phase-mean arm. 2025 + 2026 are crash-free on PS-True.

This means the 2024 residual identified by Wave 2C section 5.1 + Wave 2D section 9 is characterised, at the operand level, by "the above-phase-mean PS-True episodes in 2024 all crash". Neither 2022 nor 2023 shows this pattern; the 2024 above-mean crash concentration is a within-year characteristic.

### 11.5 Assessment

**The phase-standardised operand is essentially SILENT outside 2024** (revised at r1 lock post-review absorption per Wave 2E reviewer's §4(b) framing recommendation, replacing "behaves sensibly in clean-flip years" headline). The operand's discriminative property is a **2024-within-year finding whose cross-year generalisability is NOT validated by Wave 2E**:

- **2025 (n=23, 0 crashes total)**: the operand is silent because there is no crash-outcome variation to discriminate. Silence is NOT evidence the operand behaves well; it is absence of evidence either way. Under this null-outcome constraint, ANY operand (well-formed or spurious) would appear "not to fire spuriously". Silence is uninformative.
- **2023 (n=20, 1 crash total)**: the single crash sits on the smaller (below-mean, n=2) arm. This is arithmetically opposite-direction from 2024 (crash on lower-load arm rather than higher-load), but the n=2 arm is well below viable_n_min5 threshold. At n=2 unexposed the 2023 signal is narrative-only; the 18-vs-2 arm asymmetry itself is a within-phase distribution artefact that raises a distinct construct-validity question (§16 reviewer-concern 7).
- **Cross-year concentration fact**: all 3 above-phase-mean-arm crashes in the LC-era PS-True pool (n=80) are from 2024. **The operand's demonstrated discriminative capacity is entirely contained within 2024.**

**Reader guidance**: the operand IS validated on the 2024 within-year signal it was designed to characterise (Wave 2D §9). Its cross-year generalisability is NOT validated by Wave 2E; the operand may generalise, may be 2024-specific, or may be an artefact of the Wave 2D → Wave 2E design chain (the operand was constructed to explain a 2024-within-year pattern; reproducing that pattern is not independent validation). Any r2 codification must acknowledge this limitation explicitly.

---

## 12. Cut-point sensitivity analysis (three alternative thresholds)

Source: [`output/alternative_cutpoints_2024_ps.csv`](output/alternative_cutpoints_2024_ps.csv).

### 12.1 Three alternative cut-points

Applied to 2024 PS-True (n=15, 3 crashes) on `phase_std_pre_window_load`:

- **cut A: above phase mean** (`phase_std > 0`) -- primary. Uses phase mean as the natural cut-point.
- **cut B: above phase mean + 0.5 * phase std_dev**. Stricter than cut A.
- **cut C: above phase mean + 1.0 * phase std_dev**. Strictest.

For `citalopram_modulated` phase, std_dev = 99.2 min, so cut B threshold is +49.6 min above phase mean and cut C is +99.2 min.

### 12.2 Per-cut-point 2x2

| Cut-point | exposure_true n | exposure_false n | crash exposed | crash unexposed | rate exposed | rate unexposed | RR | RD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| cut A: > 0 | 5 | 10 | 3 | 0 | 60.0% [23.1, 88.2] | 0.0% [0.0, 27.8] | undef | +60.0 pp |
| cut B: > 0.5 sd | 3 | 12 | 2 | 1 | 66.7% [20.8, 93.9] | 8.3% [1.5, 35.4] | 8.0x | +58.3 pp |
| cut C: > 1.0 sd | 2 | 13 | 1 | 2 | 50.0% [9.5, 90.5] | 15.4% [4.3, 42.2] | 3.25x | +34.6 pp |

### 12.3 Descriptive observations

**Headline: the RR direction (exposed arm carries higher crash rate) is ROBUST across all three cut-points**. Magnitude varies: RR undefined at cut A (division by zero on unexposed), 8.00x at cut B, 3.25x at cut C. RD is +60 / +58 / +35 pp respectively.

- Under cut A: exposed arm captures all 3 crashes (100% sensitivity) at cost of 2 non-crash false-positives.
- Under cut B: exposed arm captures 2 of 3 crashes (miss = episode 163 at phase_std +24). Sensitivity drops to 67%.
- Under cut C: exposed arm captures 1 of 3 crashes (miss = episodes 163 at +24 and 190 at +51). Sensitivity drops to 33%.

### 12.4 Cut-point choice implications

- **cut A (>0) preserves 100% sensitivity** but has the widest false-positive band. Highest defensibility as "above-phase-baseline" is the natural cut-point.
- **cut B (>0.5 sd)** trades sensitivity for specificity; misses 1 borderline crash-case. Statistical convention (0.5 sd) but less descriptively natural.
- **cut C (>1.0 sd)** most selective but drops sensitivity to 33%; not a good primary choice given the 2024 n=3 crash-case ceiling.

### 12.5 Assessment

**The operand direction is robust across cut-points**. Cut A (phase_std > 0) is the most defensible primary cut-point on descriptive grounds:

- Natural interpretation: "above phase baseline".
- 100% sensitivity on the 2024 crash-cases at Wave 2E's data resolution.
- Not optimised on outcome (per [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat framing): the cut-point is defined by the operand's mathematical zero (phase mean), not by any post-hoc examination of the crash-vs-non-crash distribution.

Cut B and cut C are viable sensitivity companions but should not be primary.

---

## 13. Operand construct-validity assessment -- which of the two candidate operands should r2 codify as primary? Which as sensitivity?

### 13.1 Construct-validity summary table

| Property | Phase-standardised (residual) | Phase-stratified (p75) |
|---|---|---|
| Cross-phase comparability | Same-unit residual (minutes over 30d) | Same-rank (top-quartile) |
| Continuous vs binary | Continuous | Binary |
| Cut-point natural | phase_std > 0 = above baseline | > phase p75 = top quartile |
| Sensitivity to 2024 crashes | 3 of 3 (100%) at cut > 0 | 2 of 3 (67%) at > p75 |
| Specificity in 2024 non-crash | 10 of 12 (83%) at cut > 0 | 11 of 12 (92%) at > p75 |
| Small-sample cell sizes 2024 PS-True | exp=5, unexp=10 | exp=3, unexp=12 |
| Behaves sensibly 2023 (spot-check) | 0 crashes on exposed n=18 | (not computed in this audit) |
| Behaves sensibly 2025 (spot-check) | 0 crashes on both arms | (not computed in this audit) |
| Stage H tractability | Continuous covariate | Binary stratifier |
| Interpretability for narrative | "N minutes above phase baseline" | "In the top quartile for their phase" |

### 13.2 Reading

**Phase-standardised operand strengths**:

- Preserves magnitude information (continuous residual).
- Higher sensitivity on 2024 crashes (100% vs 67%).
- Cross-phase comparability in the same unit (minutes).
- Natural cut-point at zero.
- Suitable for a continuous covariate framing at Stage H (subject to codification decision on continuous vs binarised).

**Phase-stratified operand strengths**:

- Binary output; simpler to interpret and pre-register.
- Slightly higher specificity on 2024 non-crashes (92% vs 83%).
- Natively phase-stratified (no need to compute phase means at inference time).
- Robust to phase mean estimation error (uses per-phase p75 which is more stable than mean under skewed distributions).

### 13.3 Wave 2E's recommendation for MD-beta r2 primary vs sensitivity assignment

**Primary: phase-standardised residual (`phase_std_pre_window_load > 0`)**.

Rationale:

- Preserves 100% sensitivity on the 2024 crash-cases -- the load-bearing signal from Wave 2D section 9 is fully carried.
- Natural cut-point at zero (above/below phase baseline) is descriptively defensible and not outcome-optimised.
- Continuous residual carries magnitude information that a Stage H analysis can exploit (e.g. dose-response, subgroup analysis by residual quartile).
- Cross-phase comparability in minutes -- the operand means "N minutes above the phase baseline" identically across all 4 phases.

**Sensitivity companion: phase-stratified (`high_pre_window_p75`)**.

Rationale:

- Complementary characterisation of the same signal at a stricter threshold (top-quartile).
- Binary output simpler for pre-registration.
- Higher specificity: catches only the clearest above-baseline cases.
- Robustness check: if r2's primary result holds only under the more inclusive cut, this is a warning; if it holds under both cuts, the operand is robust to threshold choice.

### 13.4 Alternative reading

If MD-beta r2 prefers a binary primary (e.g. for tractability at Stage H stratified-2x2 machinery), the phase-stratified operand is defensible as primary with the phase-standardised residual as sensitivity companion. Wave 2E does not force a single-winner; both operands are construct-valid.

Either assignment is defensible for r2 codification.

---

## 14. Cut-point recommendation for r2 codification (with descriptive justification)

### 14.1 Recommended primary cut-point

**`phase_std_pre_window_load > 0`** (above-phase-mean cut).

### 14.2 Descriptive justification

- **Natural mathematical boundary**: zero is the operand's own zero (above/below phase baseline). Not outcome-optimised.
- **100% sensitivity on 2024 crash-cases**: preserves the load-bearing signal from Wave 2D section 9.
- **Directionally robust across cut-points**: cut A (>0), cut B (>0.5 sd), cut C (>1.0 sd) all preserve the "exposed arm carries higher crash rate" direction.
- **Descriptively interpretable**: "pre-window intensity was above the phase baseline" is a plain-language reading.

### 14.3 Sensitivity companions

Two sensitivity companions recommended:

- **`high_pre_window_p75`** (phase-stratified binary). Uses per-phase p75 as the boundary. Same-rank cross-phase comparability. Higher specificity, lower sensitivity.
- **`phase_std_pre_window_load > 0.5 * phase_std_dev`** (cut B). Continuous operand at stricter threshold. Preserves crash-rate direction. Statistical-convention cut.

### 14.4 What r2 should NOT do

- **Do NOT** apply an absolute cut-point (e.g. "raw pre_window_load > 150 min") without phase-standardisation. This would fully phase-confound the covariate across the citalopram phase-boundary. Per Wave 2D section 10.3 constraint.
- **Do NOT** optimise the cut-point on the crash outcome. Wave 2E's recommended cut-point (phase_std > 0) is defined by the operand's mathematical zero, not by any post-hoc examination of the crash distribution. Optimising cut-point on outcome would violate [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-framing discipline.
- **Do NOT** treat n=3 crash-cases as inferential evidence for the covariate's effect size. At n=3, the operand's RR / RD estimates are narrative-only per parent Stage -1 audit convention (`feedback_narrative_only_events`).

---

## 15. Findings summary + r2 codification readiness assessment

### 15.1 Findings summary

- **Section 3**: per-phase pre_window_load baselines confirmed against MD-alpha Wave 2A audit section 8 to 3 decimal places (as daily-mean units). Phase means are 285.1 / 833.5 / 581.8 / 155.1 min over 30d for the 4 phases. The `pacing_habit_established` -> `citalopram_modulated` boundary is a 3.75x mean drop and 4.1x p75 drop.
- **Section 4**: on 2024 PS-True (n=15), the phase-standardised residual cleanly identifies the 3 crash-cases as all carrying positive residuals (+24, +108, +51 min above phase mean). 12 non-crash cases carry mixed residuals; 2 non-crash cases (177, 182) also above phase mean.
- **Section 5**: phase-stratified operand at per-phase p75 flags 3 of 15 as above threshold; 2 of 3 flagged are crashes (episodes 179 and 190). Misses 1 crash (episode 163) at raw pre_window_load 179.1 vs phase p75 197.3.
- **Section 6**: 13 of 15 (87%) agreement between the two candidate operands on 2024 PS-True. 2 disagreements sit in the phase-mean-to-phase-p75 ambiguity band.
- **Section 7**: the ~2x crash-vs-non-crash separation from Wave 2D section 9 is directionally preserved under phase-standardisation at n=3 crash vs n=12 non-crash narrative-only resolution (softened at r1 lock post-review absorption from "SURVIVES" per Wave 2E reviewer L1.3 fire). Crashes cluster at phase_std mean +61.1 vs non-crashes at -75.5. Within-phase (excluding pre-citalopram episode 150) separation is essentially identical to the raw 101-min separation.
- **Section 8**: phase-stratified operand yields RR = 8.00 (narrative-only) at cut > p75; catches 2 of 3 crashes.
- **Section 9**: pre-window signal is CONCENTRATED in very_heavy end_class (per Wave 2D section 5.2). Within very_heavy 2024 PS-True (n=6), phase_std > 0 is a 1:1 classifier: 3 above-mean all crash, 3 below-mean all non-crash.
- **Section 10**: headline 2x2 -- 3-of-5 above-phase-mean 2024 PS-True crash; 0-of-10 below-phase-mean crash. RD = +60 pp; RR undefined (division by zero on unexposed).
- **Section 11**: 2023 (n=20, 1 crash) shows 0 crashes on the n=18 above-phase-mean arm; the single crash is on the smaller unexposed arm. 2025 (n=23, 0 crashes) cannot discriminate but does not falsely fire. All 3 above-mean-arm crashes in the LC-era PS-True pool are from 2024.
- **Section 12**: RR direction robust across 3 alternative cut-points (cut A undef; cut B 8.00; cut C 3.25). Cut A (phase_std > 0) is the recommended primary on defensibility grounds.
- **Section 13**: phase-standardised recommended as primary; phase-stratified as sensitivity companion. Alternative assignment (stratified primary, standardised sensitivity) also defensible.
- **Section 14**: cut-point recommendation `phase_std_pre_window_load > 0` for primary; `high_pre_window_p75` + `phase_std > 0.5 * sd` as sensitivity companions.

### 15.2 r2 codification readiness assessment (revised at r1 lock post-review absorption per Wave 2E reviewer §4(a) NEEDS-MORE-VALIDATION downgrade)

**NEEDS-MORE-VALIDATION** for full r2 codification. Wave 2E's original "READY" verdict overreached the Stage -1 audit scope per L4.6 fire and papered over the cross-year concentration concern flagged in §15.3. The corrected assessment is that Wave 2E resolves the citalopram phase-boundary confound (per Wave 2D §10.3 constraint) but does NOT resolve cross-year generalisability. Two staged codification paths surfaced by the fresh-session reviewer:

**Path A (minimum-defensibility for r2)**: MD-beta r2 codifies the phase-standardised operand as a **prospectively-testable candidate covariate** — not validated. Framing at r2 explicitly notes that Wave 2E resolves the phase-boundary confound at the operand-definition level but leaves cross-year generalisability as an open question requiring forward monitoring at Stage H. R2's Stage H pre-registration section pre-commits the operand as a candidate to be tested prospectively; the operand is not treated as an established covariate.

**Path B (fuller research discipline)**: dispatch **Wave 2F broader cross-year descriptive validation** BEFORE r2 codification. Wave 2F applies the operand to the Wave 2B whole-corpus 2x2 (all years, all end_class, all PS-True + comparator) with leave-one-out on the 3 within-2024 crash-events and within-year standardisation to separate cross-year from within-phase variance. Path B is slower but resolves the cross-year concentration concern before the operand enters MD-beta.

**Structural note**: r2 codification path is a user + orchestrator decision, NOT a Stage -1 audit decision. Wave 2E surfaces the finding + limitations; the codification choice is downstream.

Operand-definition components (unchanged from original §15.2 draft; these are what would be codified under either path):

- **Primary operand**: `phase_std_pre_window_load > 0` (above-phase-mean binary flag; or continuous residual with cut > 0 for binary form).
- **Sensitivity companions**: `high_pre_window_p75` (phase-stratified quartile binary) and `phase_std > 0.5 * phase_std_dev` (stricter continuous cut).
- **Small-n discipline**: any within-2024 result on the covariate is narrative-only at Wilson CI resolution (n=3 crash-cases). RR / RD point estimates are descriptive; CIs remain wide.
- **Phase-boundary constraint respected**: both operands are natively phase-adjusted; no absolute cut-point across the citalopram boundary.
- **Joint (end_class, covariate) stratification carried forward from Wave 2D**: r2 should stratify by end_class (heavy vs very_heavy) alongside the pre-window covariate; the very_heavy stratum carries the signal (per section 9).

### 15.3 Open construct-validity concerns

- **n=3 crash ceiling**: at 2024 PS-True n=3 crashes, no operand can be inferentially validated. Wave 2E's readings are descriptive-with-CI throughout. Any stronger claim on covariate effect size requires either (i) accumulating more crash-events over time (Stage H prospective monitoring) or (ii) a different sample frame (e.g. pooling across years despite the phase-boundary confound, which would require additional phase-adjustment machinery).
- **Very-heavy-stratum n=6 discipline**: the perfect within-stratum classification in section 9 is a hard 6-of-6 fact but at n=6 it is not credibly distinguishable from a fragile pattern. r2 should NOT frame this as a validated interaction; it is a within-stratum consistency check.
- **Cross-year generalisability**: the operand is validated only on 2024 (where all 3 above-mean crashes concentrate). Behaves sensibly in 2023 + 2025 (no false-firing) but the "operand identifies crashes" reading is 2024-specific in this dataset. r2 should NOT extrapolate the effect size beyond 2024 without additional descriptive machinery.
- **Continuous vs binary form**: Wave 2E recommends the binary form (`phase_std > 0`) as primary for tractability at Stage H, but the continuous residual carries additional information (magnitude, distance-from-baseline). r2 may prefer to codify the continuous form with the binary as sensitivity, or vice versa; either is defensible.

### 15.4 What Wave 2E does NOT resolve

- Whether the pre-window covariate is causally the mechanism (or merely a correlate of) the 2024 residual crash risk. This is a Stage H inferential question, not a Stage -1 descriptive one.
- Whether the operand generalises beyond 2024 to future crash-events. At Wave 2E's data resolution the 3 crash-cases are all in 2024; forward monitoring at Stage H would provide additional evidence.
- Whether the joint (end_class, phase_std > 0) classifier is a valid interaction or a fragile within-stratum coincidence. At n=6 in very_heavy 2024 PS-True the descriptive perfect-classification observation is real but inferentially unsupported.

---

## 16. Reviewer-concerns for fresh-session walk

1. **Section 3 baseline verification**: per-phase pre_window_load means agree with MD-alpha Wave 2A audit section 8 to 3 decimal places when normalised to daily-mean units. Fresh-session reviewer should confirm the verification is adequate (spot-checking against MD-alpha audit) and no computational anomaly is present.

2. **Section 4 D_end vs D_start anchor**: Wave 2D section 9 used D_start-anchor for pre-window; Wave 2E uses D_end-anchor per task specification. Section 7.1 documents the two anchors yield near-identical results (crash mean 216.2 vs Wave 2D's 214.7; ratio 1.88x vs 1.87x). Fresh-session reviewer should decide whether the anchor difference is adequately documented, or whether Wave 2E should compute both anchors for direct comparability.

3. **Section 4.5 within-`citalopram_modulated`-only computation**: this within-phase subset comparison (excluding episode 150) is a robustness check; the raw and phase-standardised separations are within 1 min of each other. Fresh-session reviewer should confirm this framing is adequate and does not overreach.

4. **Section 6 disagreement cases (n=2 at 13% agreement rate)**: 2 of 15 episodes disagree between the two operands (163 crash-case caught by standardised but missed by stratified; 182 non-crash caught by standardised but missed by stratified). Fresh-session reviewer should confirm the framing "phase-standardised more inclusive, phase-stratified more precise" is descriptively adequate.

5. **Section 9 perfect within-stratum classification at n=6**: within 2024 PS-True very_heavy (n=6), phase_std > 0 is a 1:1 classifier (3-crash-above, 3-non-crash-below). This is a hard 6-of-6 fact but at n=6 is not credibly distinguishable from a fragile pattern. Fresh-session reviewer should decide whether section 9.5 narrative-only framing is adequate or whether stronger caveating is required.

6. **Section 10 RR undefined (division by zero on unexposed)**: the headline 2x2 has 0 crashes on the below-phase-mean arm, making RR undefined. RD = +60 pp is reported. Fresh-session reviewer should confirm the descriptive RD framing is adequate when RR cannot be computed, or whether the audit should include an alternative RR-computation (e.g. Haldane-Anscombe correction) for downstream comparability.

7. **Section 11 2023 pattern reversal on the 18-vs-2 arms split**: 2023 PS-True has 18 above-phase-mean and only 2 below; the 1 crash is on the smaller arm. This is opposite-direction from 2024 but n=2 unexposed is not viable_n_min5. Fresh-session reviewer should decide whether the 2023 spot-check adequately demonstrates "operand does not fire spuriously" or whether the 18/2 asymmetry itself warrants a caveat about the operand's within-phase distribution behaviour.

8. **Section 11.4 all-3-crashes-in-2024 observation**: the pattern "all 3 above-mean arm crashes in the LC-era PS-True pool are from 2024" is descriptively striking but reflects the 2024 residual concentration first identified by Wave 2C section 5.1. Fresh-session reviewer should confirm the audit's framing does not over-attribute the operand's success to the operand itself vs the underlying 2024 residual being the operand's target.

9. **Section 12 cut-point sensitivity direction robust vs magnitude highly variable**: RR values 8.00 / 3.25 / undef across cut B / C / A. Direction consistent but magnitude spread is wide. Fresh-session reviewer should decide whether section 12.5 "direction robust" framing is adequate or whether the magnitude variability warrants a stronger caveat.

10. **Section 13 primary vs sensitivity assignment recommendation**: Wave 2E recommends phase-standardised as primary + phase-stratified as sensitivity but explicitly notes the alternative assignment is also defensible. Fresh-session reviewer should decide whether this "either is defensible" framing is appropriately narrow or whether Wave 2E should more firmly recommend one assignment over the other.

11. **Section 14 cut-point recommendation `phase_std > 0`**: cut-point defined by operand's mathematical zero (phase mean), not outcome-optimised. Fresh-session reviewer should confirm the descriptive-justification framing is adequate and does not creep toward outcome-optimisation.

12. **Section 15 r2 codification readiness assessment**: Wave 2E declares READY for r2 codification with 4 construct-validity constraints. Fresh-session reviewer should decide whether the readiness assessment is appropriately narrow (points at codification, does not draft it) or whether it overreaches into methodology-editing territory that should be out of scope for a Stage -1 audit.

13. **Physical-rest-only semantic (section 2.2) preserved throughout**: the pre-window covariate measures PHYSICAL exertion; not cognitive or emotional load. Fresh-session reviewer should confirm no section drifts into interpretive-load reframing.

14. **Discipline scope -- descriptive-only framing**: no verdicts, no p-values, all rates + RRs reported with Wilson CI. Fresh-session reviewer should confirm this discipline is honoured across all sections.

15. **Small-n discipline -- narrative-only per parent Stage -1 audit convention**: every cell < n=10 flagged narrative-only per parent convention. Fresh-session reviewer should confirm this treatment is applied consistently across sections 4-12.

---

## 17. Lock log

- **DRAFT r0 2026-07-16**: initial draft by Claude (Opus 4.7) in producer-mode subagent per [CONVENTIONS section 1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem. Wave 2E sibling of parent [Wave 2D Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-wave2d-2024-residual-tension/audit.md). Purpose: descriptive-before-inference precursor for MD-beta r2 codification of the pre-window covariate on the rest-adjacency arc per user pivot 2026-07-16 to Path R2C. Two candidate operand definitions computed (phase-standardised residual + phase-stratified per-phase-p75 binary); descriptive validation that either operand DISCRIMINATES the 2024 crash-vs-non-crash signal from Wave 2D section 9. Pending fresh-session methodology-review absorption before LOCK. Next-step in user-endorsed sequence: fresh-session reviewer walks Wave 2E, absorbs fires, then MD-beta r2 is drafted informed by Wave 2C section 10.5 (a) + Wave 2D section 12.2 joint end_class stratifier + Wave 2E section 14 pre-window covariate codification recommendation (Path R2C).
- **r1 LOCKED 2026-07-16**: Fresh-session methodology review absorbed from [`../../../reviews/methodology-Q24-mdbeta-wave2e-phase-standardised-prewindow-2026-07-16.md`](../../../reviews/methodology-Q24-mdbeta-wave2e-phase-standardised-prewindow-2026-07-16.md) (verdict: DEFENSIBLE with revision; 5 absorb-tier fires all applied; **§15.2 r2-ready assessment DOWNGRADED from READY to NEEDS-MORE-VALIDATION**). Five surgical patches per [CONVENTIONS section 1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations) compression discipline (mechanical clarifications; no architectural change). **Patch 1** (§7.3, review L1.3 substantive absorb): "SURVIVES phase-standardisation" headline softened to "directionally preserved at n=3 crash vs n=12 non-crash narrative-only resolution" — SURVIVES reads as if a formal significance test confirmed preservation, which is not what a n=3 comparison can support. **Patch 2** (§9.5, review §4(b) framing recommendation): overfitting-suspected caveat added on the perfect within-stratum classification at n=6 with 3 events — probability of exact 1:1 alignment under a null 50/50 classifier is ~5% (C(6,3)/2^6 for the 3-3 split configuration; 1/20 for the specific alignment). Perfect classification is genuinely consistent with a real mechanism but ALSO consistent with chance alignment at n=6. **Patch 3** (§10.3, review §4(b) framing recommendation): explicit Haldane-Anscombe consideration and decline framing added — under Haldane-Anscombe (add 0.5 to each cell), adjusted RR = 12.83x; audit explicitly declines this at Stage -1 because (i) inferential-machinery choice belongs to Stage H, (ii) descriptive RD + Wilson CIs already carry the load-bearing information, (iii) generating a specific RR magnitude at n=5 risks downstream misreading as validated. **Patch 4** (§11.5, review §4(b) framing recommendation): "operand behaves sensibly in clean-flip years" headline replaced with "operand is essentially SILENT outside 2024 + cross-year generalisability NOT validated by Wave 2E". 2025 silence is uninformative (no crash-outcome variation to discriminate). 2023 has n=2 unexposed narrative-only with arithmetically-opposite-direction signal. All 3 above-phase-mean-arm crashes in LC-era PS-True (n=80) are from 2024 — the operand's demonstrated discriminative capacity is entirely contained within 2024. **Patch 5** (§15.2, review §4(a) load-bearing recommendation): "READY for r2 codification" DOWNGRADED to "NEEDS-MORE-VALIDATION". Wave 2E resolves the citalopram phase-boundary confound but does NOT resolve cross-year generalisability. Two staged codification paths surfaced: **Path A (minimum-defensibility)** — r2 codifies as prospectively-testable candidate covariate framed as unvalidated pending Stage H forward monitoring; **Path B (fuller research discipline)** — Wave 2F broader cross-year validation BEFORE r2 codifies (leave-one-out on 3 within-2024 crashes; within-year standardisation to separate cross-year from within-phase variance). r2 codification path decision is user + orchestrator, NOT Stage -1 audit. Preserved byte-identically: §1 corpus + Wave 2D anchor; §2 framing + citalopram phase-boundary constraint + two candidate operands; §3 per-phase pre_window_load baselines (verified vs MD-alpha Wave 2A audit §8 to 3 decimals); §4.1-§4.5 phase-standardised operand computation + within-2024 distribution + PS-True subset; §5 phase-stratified operand + within-2024 distribution; §6 agreement between operands; §7.1-§7.2 raw and phase-standardised separation data (only §7.3 headline softened); §8 phase-stratified operand within-2024 crash-vs-non-crash; §9.1-§9.4 by-end-class 2×2 + Wave 2D §5.2 + candidate (e) consistency (only §9.5 caveat added); §9.6 assessment; §10.1-§10.2 headline 2×2 tables (only §10.3 Haldane-Anscombe framing added); §10.4 assessment; §11.1-§11.4 neighbouring-year data (only §11.5 headline revised); §12 cut-point sensitivity data + observations + implications; §13 primary vs sensitivity assignment; §14 cut-point recommendation; §15.1 findings summary bullets except section 7 line; §15.3 open construct-validity concerns; §15.4 what Wave 2E does NOT resolve; §16 reviewer-concerns list; §17 discipline attestations. **STATUS**: LOCKED r1 2026-07-16 post-review absorption. Next-step in user-endorsed sequence: user decides Path A vs Path B; MD-beta r2 dispatch conditional on that decision.

Producer-mode discipline attestations:

- Parent MDs (MD-alpha, MD-beta), CONVENTIONS, and the four prior Wave 2 audits (2A, 2B, 2C, 2D) NOT edited by this session.
- Named counts per [CONVENTIONS section 3.6](../../../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file): all cell counts + rates carry scheme (heavy-episode-end, K=3 rest-after primary, proactive-strategic subset, PS = proactive-strategic, cut-point label) + unit (episode / event) + source CSV filename in-text.
- NaN discipline per [CONVENTIONS section 3.10 (parent Q24 MD "zero-vs-NaN" shorthand)](../../../CONVENTIONS.md#310-operationalisation-faithful-to-the-data-not-just-to-the-description): `effective_exertion_min` verified 0 NaN days on LC-era stratum (empirical: 1524/1524 valid); parent Q24 MD section 7.11 minimum-valid-pre-window-points rule (>=15) trivially satisfied for all 314 episode-ends; sum-over-30d-window uses `fillna(0)` only inside the validity-gated helper.
- Definitional-pair discipline per [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair): phase-standardised vs phase-stratified are a definitional pair; section 13 assigns primary + sensitivity roles with descriptive justification.
- Descriptive-with-CI framing per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference): no verdicts, no p-values, Wilson 95% CIs on all rates, RR + RD reported with per-arm cell counts.
- Small-n discipline per parent Stage -1 audit convention: every cell < n=10 flagged narrative-only; RR / RD point estimates at n<5 cells treated as narrative-only.
- Physical-rest-only semantic constraint (memory `project_rest_day_operand_semantics`) inherited from Wave 2C section 2.1 + Wave 2D; preserved throughout.
- Citalopram phase-boundary respect per Wave 2D section 10.3: both operands are natively phase-adjusted; no absolute cut-point applied across the 2024-04-09 boundary.
- No emoji, no em-dash in outputs or narrative.
- Idempotent script per [CONVENTIONS section 3.6](../../../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file): re-runnable, no `datetime.now()`, byte-identical CSVs on identical input. `RANDOM_SEED = 20260716` declared per MD-beta section 3.6, not exercised.
- Cut-point selection is descriptive, not outcome-optimised per [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat framing: primary cut `phase_std > 0` defined by operand's mathematical zero; sensitivity companions cut B / cut C defined by phase std_dev multiples (statistical convention, not outcome-optimised).
