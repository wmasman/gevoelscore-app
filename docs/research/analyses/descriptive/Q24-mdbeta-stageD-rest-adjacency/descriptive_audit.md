# Stage D descriptive audit: rest-adjacency arc under MD-beta r2 LOCKED

*Producer-mode Stage D descriptive audit per [CONVENTIONS section 1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). Drafted 2026-07-19 by Claude (Opus 4.7) in producer-mode subagent under user delegation. Authorising user: Willem.*

**Status**: **LOCKED r1 2026-07-19** post fresh-session review absorption. See section 14 lock log for r1 LOCKED entry and the six absorb-tier patches applied.
**Anchor MD**: [`heavy_day_crash_risk_prediction.md`](../../../methodology/heavy_day_crash_risk_prediction.md) LOCKED r2 2026-07-17.
**Data source**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` (LC-era stratum, `lc_phase == 'lc'`, n=1524 rows).
**Random seed**: 20260716 per MD-beta section 3.6.
**Reproducibility**: [`scripts/stage_d_rest_adjacency.py`](scripts/stage_d_rest_adjacency.py); outputs in [`output/`](output/); idempotent re-run.

**Discipline scope**: Stage D descriptive audit only per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). All contingency tables reported as descriptive-with-Wilson-CI + descriptive-with-bootstrap-CI. Fisher's exact p-values reported for completeness only, NOT as verdicts. No inferential closure at Stage D.

**Cross-refs**:

- [MD-beta LOCKED r2 2026-07-17](../../../methodology/heavy_day_crash_risk_prediction.md) sections 3.1.1 (operand family), 3.2 + 3.3 (K-ladder), 3.5.1 (joint stratifier), 3.6 (statistical machinery), 3.7 (asymmetric direction pre-commit), 5 confounds 2 + 7 + 8, 6.5 + 6.6 + 6.9 baseline anchors + headline cell.
- [Wave 2C audit LOCKED r1 2026-07-16](../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md) sections 5 + 6 (proactive-strategic + crisis-reactive pooled 2x2s).
- [Wave 2D audit LOCKED r1 2026-07-16](../Q24-mdbeta-wave2d-2024-residual-tension/audit.md) sections 4 + 7 (within-2024 by-intensity + absolute-step operand).
- [Parent Q24 MD LOCKED r1 2026-07-15](../../../methodology/post_heavy_day_compensatory_rest.md).
- Memory pointer: `project_rest_day_operand_semantics` (physical-rest-only constraint).

---

## 1. Corpus and preflight sample-floor probe

### 1.1 Corpus counts (points to parent Wave 2B / 2C; Stage D-specific numbers)

| Measure | Value | Source |
|---|---|---|
| LC-era rows | 1524 days (2022-04-04 to 2026-06-05) | script header printout |
| Heavy days (heavy + very_heavy) | 532 (34.9%) | parent Stage -1 section 1 |
| Very-heavy days | 256 (16.8%) | parent Stage -1 section 1 |
| Crash days | 103 (crash_v2, day-level) | parent Stage -1 section 1 |
| gap=0 heavy episodes | 314 | script + parent Wave 2B section 3 |
| Episodes with heavy end_class | 165 | script |
| Episodes with very_heavy end_class | 149 | script |
| Episodes in pre-cital era (D_end < 2024-04-09) | 156 | script |
| Episodes in post-cital era (D_end >= 2024-04-09) | 158 | script |
| Episodes with crash_in_5d True | 46 (14.6%) | script + MD-beta section 6.7 |
| Rest-day primary (`rest_day_p25` True on LC-era) | 404 (26.5%) | parent Wave 2B section 2 |
| Rest-day primary NaN | 37 (2.4%) | parent Wave 2B section 2 |
| Gevoelscore non-NaN (LC-era) | 1372 / 1524 = 90.0% | Wave 2C section 1 |
| Gevoelscore NaN (LC-era) | 152 (10.0%; near-fully 2022 pre-tracker onset) | Wave 2C section 1 |
| Episodes with rest-after K=3 primary True (omnibus NaN=False) | 202 / 314 (64.3%) | parent MD-beta section 6.5 |

### 1.2 Baseline reproduction anchor (MD-beta section 6.6 byte-for-byte)

Under the MD-beta section 3.10 NaN=False convention on the omnibus `rest_day_p25` operand, at K=3 rest-after on the full 314-episode all-end_class pool:

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| rest_after_3 False | 100 | 12 | 112 |
| rest_after_3 True | 168 | 34 | 202 |
| Total | 268 | 46 | 314 |

- Crash rate rest-after-adjacent: 34/202 = 16.83% (Wilson 95% CI 12.30, 22.60)
- Crash rate rest-after-absent: 12/112 = 10.71% (Wilson 95% CI 6.24, 17.80)
- RR = 1.571 (bootstrap 95% CI 0.885, 3.297)
- RD = 0.061 (bootstrap 95% CI -0.018, 0.138)

Reproduces MD-beta section 6.6 100/12/168/34 with RR = 1.57 byte-for-byte. Source: [`output/omnibus_by_end_class_K3_after.csv`](output/omnibus_by_end_class_K3_after.csv) row `omnibus_ALL_K3_after_era_ALL`.

### 1.3 Wave 2C reproduction spot-check

Two variants of the strategic-primary contrast restricted to ALL end_class (not just heavy), K=3 rest-after, era-pooled:

| Variant | operand | strategic_true_n | strategic_false_n | crash_true | crash_false | RR |
|---|---|---:|---:|---:|---:|---:|
| MD-beta 3.1.1 pure-strategic | `rest_day_p25 == True AND gs >= 5` | 84 | 226 | 8 | 38 | 0.566 |
| Wave 2C proactive-strategic | `strategic AND no is_crash in [d-3, d-1]` | 80 | 230 | 5 | 41 | 0.351 |

The Wave 2C reference is 80/232/5/41 with RR = 0.354 (source [`../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/output/proactive_strategic_rest_crash_2x2.csv`](../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/output/proactive_strategic_rest_crash_2x2.csv) row ALL_ERA_POOLED). My reproduction differs by 2 episodes in the false arm (my `undef` drop removes 2 episodes that Wave 2C keeps under a different NaN-handling convention); the RR agrees to within 0.9% (0.351 vs 0.354). See section 12 for a note on the operand-scope tension.

Source: [`output/wave2c_reproduction_spotcheck.csv`](output/wave2c_reproduction_spotcheck.csv).

### 1.4 Preflight sample-floor probe (informal Wilson-viable floor ~10 exposed per arm)

Per user Option B endorsement, cells with either arm below the informal Wilson-viable floor of 10 exposed episodes are flagged NEEDS-MORE-DATA and reported as narrative-only downstream. The full preflight table lives at [`output/preflight_sample_floor.csv`](output/preflight_sample_floor.csv); the two failing cells are:

| Family | Cell | exposed_true_n | exposed_false_n | Floor pass |
|---|---|---:|---:|---|
| strategic_abs3k | K=3 rest-after, era=pre_cital, end_class=heavy | 4 | 78 | FAIL |
| crisis_p25 | K=3 rest-after, era=pre_cital, end_class=very_heavy | 8 | 66 | FAIL |

The 34 remaining cells pass the floor. The 2 failing cells are surfaced verbatim in their respective section reads with NEEDS-MORE-DATA framing.

### 1.5 Cell inventory across headline + companions

| Section | Family | Cells | All pass floor? |
|---|---|---:|---|
| 3 headline | strategic x heavy x K=3 rest-after (era ALL + pre_cital + post_cital) | 3 | pass |
| 4 era-strat | strategic x heavy x K=3 rest-after (pre_cital + post_cital) | 2 | pass |
| 5 very_heavy | strategic x very_heavy x K=3 rest-after (3 eras) | 3 | pass |
| 6 crisis | crisis x {heavy, very_heavy} x K=3 rest-after (3 eras) | 6 | 5 pass / 1 fail |
| 7 borderline | borderline x {heavy, very_heavy} x K=3 rest-after (era ALL) | 2 | pass |
| 8 omnibus | omnibus x {heavy, very_heavy, ALL} x K=3 rest-after (3 eras) | 9 | pass |
| 9 abs-step | abs3k-strategic x heavy x K=3 rest-after (era ALL) | 1 | pass |
| 10 K-ladder | strategic x heavy x K in {1, 2, 3} rest-after (era ALL) | 3 | pass |
| 11 rest-before | strategic x heavy x K=3 rest-BEFORE (3 eras) | 3 | pass |

Section 4 is the immediate era-stratified companion to section 3; the two cells overlap.

---

## 2. Reproducibility

- **Script**: [`scripts/stage_d_rest_adjacency.py`](scripts/stage_d_rest_adjacency.py). Idempotent, re-runnable, single entry point.
- **Data**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`; expected LC-era stratum n=1524 rows.
- **Dump version**: v3.2 or current locked dump per user working state 2026-07-19.
- **Random seed**: 20260716 per MD-beta section 3.6.
- **Statistical machinery** per MD-beta section 3.6:
  - Wilson 95% CI on per-arm rates via `statsmodels.stats.proportion.proportion_confint(method='wilson')` at alpha=0.05.
  - Fisher's exact two-sided p-value via `scipy.stats.fisher_exact`, descriptive-only per CONVENTIONS section 2.1.
  - Bootstrap 95% CI on RR + RD: B = 10,000 episode-level resamples, block length = 1 per MD-beta section 3.6, percentile 2.5 / 97.5.
  - Haldane-Anscombe correction (+0.5 to all cells) applied to RR only when any raw cell = 0; the correction is labelled explicitly in the output CSV `haldane_applied` column.
- **NaN handling per operand**:
  - Omnibus `rest_day_p25`: NaN=False convention per MD-beta section 3.10 (matches section 6.6 baseline anchor).
  - All other operands (strategic, crisis, borderline, absolute-step-strategic, proactive-strategic): drop episodes where the operand is undef AND observed False (the arm-True observation resolves the ambiguity so True cases are retained).
- **Era stratifier**: pre_cital = D_end < 2024-04-09; post_cital = D_end >= 2024-04-09.
- **Unit of analysis**: episode-end at gap=0 contiguous heavy runs, inherited from MD-beta section 2 + parent Q24 MD section 3.1.
- **Filter chain**: LC-era only + `crash_window_full == True` + operand-specific undef drop where applicable.

---

## 3. Headline cell: strategic x heavy x K=3 rest-after x crash-in-5d, era-pooled

**Primary operand**: `rest_day_p25_physical_strategic` (physical rest AND gevoelscore >= 5 on the rest-day) per MD-beta section 3.1.1.
**Sample restriction**: heavy end_class at the episode-end day.
**Contrast**: at least one strategic-rest-day in [D_end+1, D_end+3] (arm True) versus no such day (arm False).
**Outcome**: `crash_in_5d = any(is_crash[d] for d in [D_end+1, D_end+5])`.
**Direction pre-commit** per MD-beta section 3.7: strategic-rest-adjacent -> LOWER crash rate.

Source: [`output/headline_strategic_heavy_K3_after.csv`](output/headline_strategic_heavy_K3_after.csv).

### 3.1 2x2 contingency, era-pooled

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| strategic_rest_after_3 False | 94 | 28 | 122 |
| strategic_rest_after_3 True | 38 | 2 | 40 |
| Total | 132 | 30 | 162 |

3 episodes dropped from the 165 heavy-end pool where the strategic operand is undef AND False in the K=3 window. Per the operand-specific undef-drop convention documented at section 2 NaN-handling, gevoelscore-NaN on a physical rest-day drops the episode from the strategic operand where the arm-True observation is not resolved by a valid True case; this differs from the omnibus operand's NaN=False convention (section 8) which is retained to preserve the MD-beta section 6.6 byte-for-byte anchor at section 1.2. The 162-episode strategic pool versus the 165-episode heavy pool delta is an NaN-handling difference under an internally consistent policy, not an operand-selection artefact.

- Crash rate strategic-rest-adjacent: 2/40 = 5.00% (Wilson 95% CI 1.38, 16.50)
- Crash rate strategic-rest-absent: 28/122 = 22.95% (Wilson 95% CI 16.38, 31.17)
- RR = 0.218 (bootstrap 95% CI 0.000, 0.610; 10000 / 10000 valid rounds)
- RD = -0.180 (bootstrap 95% CI -0.276, -0.074)
- Fisher's exact p-value (two-sided): 0.0097 (descriptive-only per CONVENTIONS section 2.1)
- Wilson-viable floor: PASS (40 exposed vs 122 unexposed)

### 3.2 Descriptive observation

The rate on the strategic-adjacent arm (5.00%) is lower than the rate on the strategic-absent arm (22.95%), with a bootstrap 95% CI on RR that does not include 1.0 (0.000, 0.610). The pattern is descriptively consistent with the MD-beta section 3.7 pre-commit direction (strategic-rest-adjacent -> LOWER crash rate) at the era-pooled read on heavy end_class. Per CONVENTIONS section 2.1, this is a descriptive observation, not a verdict; the read is qualified by (i) the immediate era-stratified companion read in section 4 which shows era-instability of the effect size and CI width; (ii) the confounding-by-indication caveat per MD-beta section 3.9 confound 1; (iii) the reciprocal definitional-pair discipline attestation in section 6 which frames strategic + crisis as one split, not two independent tests.

Sample-viability note: 40 exposed episodes on the strategic arm is above the informal Wilson-viable floor of 10 but tight for a 2 vs 28 crash-count comparison. Bootstrap 95% CI lower bound on RR is 0.000 (the bootstrap draws at least one round where the exposed arm has zero crashes; that is a small-sample feature of a rate-2/40 arm, not a data-quality artefact).

---

## 4. Era-stratified sensitivity (pre-cital + post-cital, side-by-side)

Same operand and same restriction as section 3, split at the citalopram-onset era boundary 2024-04-09 per MD-beta section 5 confound 7 revision. Side-by-side reporting per MD-beta section 6.9 era-pooled headline rationale + falsifiability-via-immediate-companions discipline.

### 4.1 Pre-cital era (2022-04-04 to 2024-04-08)

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| strategic_rest_after_3 False | 51 | 21 | 72 |
| strategic_rest_after_3 True | 9 | 1 | 10 |
| Total | 60 | 22 | 82 |

- Crash rate strategic-rest-adjacent: 1/10 = 10.00% (Wilson 95% CI 1.79, 40.42)
- Crash rate strategic-rest-absent: 21/72 = 29.17% (Wilson 95% CI 19.94, 40.51)
- RR = 0.343 (bootstrap 95% CI 0.000, 1.267)
- RD = -0.192 (bootstrap 95% CI -0.371, 0.062)
- Fisher's exact p-value: 0.2745
- Wilson-viable floor: PASS at threshold (10 exposed vs 72 unexposed; 10 is exactly at the floor).

### 4.2 Post-cital era (2024-04-09 to 2026-06-05)

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| strategic_rest_after_3 False | 43 | 7 | 50 |
| strategic_rest_after_3 True | 29 | 1 | 30 |
| Total | 72 | 8 | 80 |

- Crash rate strategic-rest-adjacent: 1/30 = 3.33% (Wilson 95% CI 0.59, 16.67)
- Crash rate strategic-rest-absent: 7/50 = 14.00% (Wilson 95% CI 6.95, 26.19)
- RR = 0.238 (bootstrap 95% CI 0.000, 1.179)
- RD = -0.107 (bootstrap 95% CI -0.225, 0.014)
- Fisher's exact p-value: 0.2471
- Wilson-viable floor: PASS (30 exposed vs 50 unexposed).

### 4.3 Descriptive comparison relative to pooled headline

Both era arms show a lower crash rate on the strategic-adjacent side than on the strategic-absent side (pre-cital 10.0% vs 29.2%; post-cital 3.3% vs 14.0%). Per-era point-estimate RRs (0.343 pre-cital, 0.238 post-cital) sit close to the pooled RR (0.218). Per-era bootstrap 95% CIs on RR both include 1.0 while the era-pooled CI does not; the pooled read is the sample-viability-tighter primary while the era-stratified companions carry the falsifiability discipline per MD-beta section 6.9 era-pooled headline rationale attestation.

Descriptively the direction is consistent with the MD-beta section 3.7 pre-commit on both eras, though wider per-era CIs (both include 1.0) mean the descriptive read is CONSISTENT-WITH the pre-commit direction on each era without individually excluding the null. The era-pooled cell is the CI-tighter primary; the two era arms are the falsifiability check.

### 4.4 6-mechanism era caveat (verbatim per MD-beta section 5 confound 7)

The pre-cital vs post-cital era stratifier is a temporal anchor at 2024-04-09 (citalopram onset). Any RR difference between the two strata conflates at least six co-occurring factors:

1. Citalopram pharmacological effect.
2. Learned-pacing behavioural evolution (per MD-alpha section 3.6 five-confound bundle).
3. Tactical-Garmin-use improvement (per memory `project_garmin_research_bias_boundary`).
4. Natural LC disease-course trajectory.
5. Envelope drift (documented in MD-alpha Wave 2A audit section 8 pre-window mean-level shift; per Wave 2D section 10.3 the pre-window `effective_exertion_min` per day mean is 19.39 min/day on `pacing_habit_established` vs 5.17 min/day on `citalopram_modulated`, a ~4x shift at the phase boundary).
6. Aging + seasonality across the ~2-year window.

The stratifier does NOT identify medication effect at n=1. It is a temporal anchor for descriptive era-stratified reads. No causal claim about medication is made or supported by this stratifier. Any interpretation attributing an era-stratum RR difference to citalopram specifically is out of scope for this Stage D audit and would require a between-participant or within-participant crossover design not available at n=1.

---

## 5. Very-heavy end_class sensitivity

Same operand, same K=3 rest-after direction, sample-restricted to very_heavy end_class (149 episodes) instead of heavy. Framed as a sensitivity companion per MD-beta section 3.5.1 sensitivity cell 1: this is the cell where gevoelscore-conditioning alone is insufficient per Wave 2D section 4 empirical anchor (within-2024 heavy-end RR = 0.00 clean flip vs very_heavy-end RR = 3.50 residual). NOT an alternative headline.

Source: [`output/sens_strategic_very_heavy_K3_after.csv`](output/sens_strategic_very_heavy_K3_after.csv).

### 5.1 Era-pooled

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| strategic_rest_after_3 False | 94 | 10 | 104 |
| strategic_rest_after_3 True | 38 | 6 | 44 |
| Total | 132 | 16 | 148 |

- Crash rate strategic-rest-adjacent: 6/44 = 13.64% (Wilson 95% CI 6.40, 26.71)
- Crash rate strategic-rest-absent: 10/104 = 9.62% (Wilson 95% CI 5.31, 16.80)
- RR = 1.418 (bootstrap 95% CI 0.417, 3.772)
- RD = 0.040 (bootstrap 95% CI -0.070, 0.160)
- Fisher's exact p-value: 0.5635
- Wilson-viable floor: PASS.

### 5.2 Pre-cital era

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| strategic_rest_after_3 False | 49 | 5 | 54 |
| strategic_rest_after_3 True | 17 | 2 | 19 |

- Crash rate strategic-rest-adjacent: 2/19 = 10.53% (Wilson 95% CI 2.94, 31.39)
- Crash rate strategic-rest-absent: 5/54 = 9.26% (Wilson 95% CI 4.02, 19.91)
- RR = 1.137 (bootstrap 95% CI 0.000, 5.156)
- RD = 0.013 (bootstrap 95% CI -0.132, 0.187)

### 5.3 Post-cital era

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| strategic_rest_after_3 False | 45 | 5 | 50 |
| strategic_rest_after_3 True | 21 | 4 | 25 |

- Crash rate strategic-rest-adjacent: 4/25 = 16.00% (Wilson 95% CI 6.40, 34.65)
- Crash rate strategic-rest-absent: 5/50 = 10.00% (Wilson 95% CI 4.35, 21.36)
- RR = 1.600 (bootstrap 95% CI 0.283, 6.783)
- RD = 0.060 (bootstrap 95% CI -0.098, 0.233)

### 5.4 Descriptive observation

On very_heavy end_class, the strategic-adjacent arm shows a HIGHER crash rate than the strategic-absent arm at every era read (era-pooled 13.6% vs 9.6%; pre-cital 10.5% vs 9.3%; post-cital 16.0% vs 10.0%). All three bootstrap 95% CIs on RR include 1.0. This is a **sign-inversion relative to the MD-beta section 3.7 pre-commit direction** on this sensitivity cell.

The sign-inversion is consistent with Wave 2D section 4 within-2024 finding (very_heavy-end RR = 3.50 residual on n=6 exposed / n=35 unexposed at n=3 crashes on the exposed arm) and with parent Wave 2B section 10 whole-corpus intensity finding (very_heavy end_class RR = 0.96 pooled). Per MD-beta section 6.9 generalisation-scope attestation, the strategic-primary sign-flip is descriptively supported on heavy end_class only and is NOT claimed to generalise to very_heavy end_class. This section 5 read is the codified sensitivity companion documenting that non-generalisation, per MD-beta section 3.5.1 sensitivity cell 1.

The very_heavy sign-inversion is one of the two candidate mechanisms (mechanism (e) intensity-interaction residual) named at MD-beta section 5 confound 8 as the 2024-residual-tension diagnosis. Mechanism (b) pre-window-load partial-mitigation is the deferred descriptive observation per MD-beta post-confound-8 paragraph and is NOT read at this Stage D.

---

## 6. Crisis-rest x end_class stratified (endogeneity diagnostic)

**Reciprocal definitional-pair attestation upfront** per MD-beta section 3.7 reciprocal-attestation recommendation 4: strategic + crisis are ONE definitional-pair split of the omnibus `rest_day_p25` operand, NOT two independent tests. Any Stage S1 synthesis that reports the strategic-primary section 3 RR and the crisis-sensitivity section 6 RR as independent evidence violates the definitional-pair discipline codified at MD-beta section 3.7 + Wave 2C section 6.5. The strategic + crisis reads are two views on the same underlying joint distribution split by gevoelscore-bucket.

Primary operand: `rest_day_p25_physical_crisis` (physical rest AND gevoelscore <= 3). Direction pre-commit: crisis-rest-adjacent -> HIGHER crash rate per MD-beta section 3.7. Reversed direction is the direct signature of the section 3.9 confound 1 confounding-by-indication mechanism (Salas 2001; Kyriacou & Lewis 2016 *JAMA*).

Source: [`output/crisis_by_end_class_K3_after.csv`](output/crisis_by_end_class_K3_after.csv).

### 6.1 Heavy end_class, era-pooled

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| crisis_rest_after_3 False | 117 | 15 | 132 |
| crisis_rest_after_3 True | 13 | 15 | 28 |
| Total | 130 | 30 | 160 |

- Crash rate crisis-rest-adjacent: 15/28 = 53.57% (Wilson 95% CI 35.81, 70.47)
- Crash rate crisis-rest-absent: 15/132 = 11.36% (Wilson 95% CI 7.01, 17.90)
- RR = 4.714 (bootstrap 95% CI 2.600, 9.000)
- RD = 0.422 (bootstrap 95% CI 0.226, 0.611)
- Fisher's exact p-value: 3.26e-06
- Wilson-viable floor: PASS.

### 6.2 Heavy end_class, pre-cital era

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| crisis_rest_after_3 False | 54 | 10 | 64 |
| crisis_rest_after_3 True | 6 | 12 | 18 |

- Crash rate crisis-rest-adjacent: 12/18 = 66.67% (Wilson 95% CI 43.75, 83.72)
- Crash rate crisis-rest-absent: 10/64 = 15.63% (Wilson 95% CI 8.71, 26.43)
- RR = 4.267 (bootstrap 95% CI 2.234, 9.620)
- RD = 0.510 (bootstrap 95% CI 0.255, 0.740)

### 6.3 Heavy end_class, post-cital era

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| crisis_rest_after_3 False | 63 | 5 | 68 |
| crisis_rest_after_3 True | 7 | 3 | 10 |

- Crash rate crisis-rest-adjacent: 3/10 = 30.00% (Wilson 95% CI 10.78, 60.32)
- Crash rate crisis-rest-absent: 5/68 = 7.35% (Wilson 95% CI 3.18, 16.09)
- RR = 4.080 (bootstrap 95% CI 0.000, 18.19)
- RD = 0.226 (bootstrap 95% CI -0.069, 0.547)

### 6.4 Very_heavy end_class, era-pooled

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| crisis_rest_after_3 False | 117 | 12 | 129 |
| crisis_rest_after_3 True | 15 | 4 | 19 |

- Crash rate crisis-rest-adjacent: 4/19 = 21.05% (Wilson 95% CI 8.51, 43.33)
- Crash rate crisis-rest-absent: 12/129 = 9.30% (Wilson 95% CI 5.40, 15.56)
- RR = 2.263 (bootstrap 95% CI 0.429, 5.941)
- RD = 0.118 (bootstrap 95% CI -0.066, 0.320)

### 6.5 Very_heavy end_class, pre-cital era: NEEDS-MORE-DATA

exposed_true_n = 8, exposed_false_n = 65. Fails the informal Wilson-viable floor (8 < 10). Reported narrative-only: 2/8 crashes on the crisis-adjacent arm (25.0%) vs 5/65 on the crisis-absent arm (7.7%); raw RR 3.25 with no bootstrap CI computed at this sample floor. Descriptive-only.

**Note on Wilson-viable-floor restraint**: Wilson per-arm CIs ARE mathematically computable at n=8 exposed; the audit body deliberately does NOT report them, per the Wilson-viable floor policy that treats sub-floor cells as narrative-only rather than emitting CIs whose small-sample width would be a floor-fail artefact rather than an evidential surface. The script still writes the computed Wilson bounds to `output/crisis_by_end_class_K3_after.csv` for reproducibility trace; the audit body's silence on those bounds is deliberate discipline, not a computation gap.

### 6.6 Very_heavy end_class, post-cital era

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| crisis_rest_after_3 False | 57 | 7 | 64 |
| crisis_rest_after_3 True | 9 | 2 | 11 |

- Crash rate crisis-rest-adjacent: 2/11 = 18.18% (Wilson 95% CI 5.14, 47.70)
- Crash rate crisis-rest-absent: 7/64 = 10.94% (Wilson 95% CI 5.40, 20.90)
- RR = 1.662 (bootstrap 95% CI 0.000, 6.359)
- RD = 0.072 (bootstrap 95% CI -0.143, 0.353)

### 6.7 Descriptive observation

On heavy end_class the crisis-adjacent arm shows a substantially HIGHER crash rate than the crisis-absent arm at every era read where the floor passes (era-pooled 53.6% vs 11.4%; pre-cital 66.7% vs 15.6%; post-cital 30.0% vs 7.4%). The era-pooled and pre-cital era bootstrap 95% CIs on RR both exclude 1.0 (bootstrap CI 2.6 to 9.0 pooled; 2.23 to 9.62 pre-cital). The post-cital era CI includes 0.0 in the bootstrap (from resamples where the arm-True side has 0 exposed episodes) but the point estimate remains 4.08.

The pattern is descriptively consistent with the MD-beta section 3.7 reversed direction pre-commit on the crisis-primary operand (crisis-rest-adjacent -> HIGHER) and with the confounding-by-indication mechanism (Salas 2001; Kyriacou & Lewis 2016 *JAMA*): a rest-day chosen while feeling badly is enriched for crash-vulnerable episodes; the crisis-adjacent arm is a proxy for the endogenous felt-bad signal that the strategic-primary arm attempts to partial out.

On very_heavy end_class the same directional pattern holds but at smaller magnitudes and wider CIs; the era-pooled bootstrap CI (0.43, 5.94) includes 1.0.

**Discipline reminder**: this section 6 finding is one leg of a definitional-pair split per MD-beta section 3.7 reciprocal-attestation. The section 3 headline RR (0.218) and the section 6.1 crisis RR (4.714) are read from opposite sides of the same joint (rest_day_p25 True) x (gs_bucket) distribution partition. They MUST NOT be reported as independent tests at Stage S1.

---

## 7. Borderline-rest x end_class stratified (descriptive-only)

Primary operand: `rest_day_p25_physical_borderline` (physical rest AND gevoelscore == 4). No direction pre-commit per MD-beta section 3.7 (semantic ambiguity of gevoelscore = 4). Reported descriptively as its own stratum per MD-beta section 3.1.1 borderline definition.

Source: [`output/borderline_by_end_class_K3_after.csv`](output/borderline_by_end_class_K3_after.csv).

### 7.1 Heavy end_class, era-pooled

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| borderline_rest_after_3 False | 87 | 21 | 108 |
| borderline_rest_after_3 True | 45 | 9 | 54 |

- Crash rate borderline-rest-adjacent: 9/54 = 16.67% (Wilson 95% CI 9.02, 28.74)
- Crash rate borderline-rest-absent: 21/108 = 19.44% (Wilson 95% CI 13.08, 27.90)
- RR = 0.857 (bootstrap 95% CI 0.346, 1.674)
- RD = -0.028 (bootstrap 95% CI -0.148, 0.100)

### 7.2 Very_heavy end_class, era-pooled

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| borderline_rest_after_3 False | 91 | 12 | 103 |
| borderline_rest_after_3 True | 41 | 4 | 45 |

- Crash rate borderline-rest-adjacent: 4/45 = 8.89% (Wilson 95% CI 3.51, 20.73)
- Crash rate borderline-rest-absent: 12/103 = 11.65% (Wilson 95% CI 6.79, 19.27)
- RR = 0.763 (bootstrap 95% CI 0.144, 2.035)
- RD = -0.028 (bootstrap 95% CI -0.127, 0.078)

### 7.3 Descriptive observation

On both end_class intensities the borderline-adjacent crash rate is slightly below the borderline-absent crash rate (16.7% vs 19.4% on heavy; 8.9% vs 11.6% on very_heavy). Both bootstrap 95% CIs on RR include 1.0. The borderline stratum sits closer to the omnibus pooled rate than to either the strategic or crisis extreme; the read is consistent with the borderline bucket capturing a mixed felt-state population (gs=4 as both "bad day that is not that bad" and "good day with existing fatigue") per MD-beta section 3.1.1 semantic ambiguity note.

No direction pre-commit was made for this stratum; the descriptive read stands on its own.

---

## 8. Omnibus rest x end_class stratified (anchor read)

Primary operand: `rest_day_p25` (physical rest, gevoelscore-unconditioned). No direction pre-commit at r2 per MD-beta section 3.7 composition-shift caveat. Anchored against MD-beta section 6.6 whole-pool baseline; the ALL end_class ALL era row reproduces byte-for-byte per section 1.2.

Source: [`output/omnibus_by_end_class_K3_after.csv`](output/omnibus_by_end_class_K3_after.csv).

**NaN-policy note**: this section uses the NaN=False convention on `rest_day_p25` per section 2 NaN-handling, intentionally distinct from the undef-drop convention used for strategic + crisis + borderline + abs3k operands elsewhere in this audit. NaN=False is retained here to preserve the byte-for-byte MD-beta section 6.6 baseline reproduction anchor at section 1.2. Cross-reference to section 3.1 NaN-policy cross-ref where the strategic pool uses the undef-drop convention.

### 8.1 Heavy end_class, era-pooled

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| omnibus_rest_after_3 False | 51 | 6 | 57 |
| omnibus_rest_after_3 True | 84 | 24 | 108 |

- Crash rate omnibus-rest-adjacent: 24/108 = 22.22% (Wilson 95% CI 15.41, 30.94)
- Crash rate omnibus-rest-absent: 6/57 = 10.53% (Wilson 95% CI 4.91, 21.12)
- RR = 2.111 (bootstrap 95% CI 1.017, 6.711)
- RD = 0.117 (bootstrap 95% CI 0.003, 0.229)

### 8.2 Heavy end_class, pre-cital era

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| omnibus_rest_after_3 False | 21 | 4 | 25 |
| omnibus_rest_after_3 True | 39 | 18 | 57 |

- Crash rate omnibus-rest-adjacent: 18/57 = 31.58% (Wilson 95% CI 21.00, 44.48)
- Crash rate omnibus-rest-absent: 4/25 = 16.00% (Wilson 95% CI 6.40, 34.65)
- RR = 1.974 (bootstrap 95% CI 0.844, 7.742)
- RD = 0.156 (bootstrap 95% CI -0.042, 0.337)

### 8.3 Heavy end_class, post-cital era

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| omnibus_rest_after_3 False | 30 | 2 | 32 |
| omnibus_rest_after_3 True | 45 | 6 | 51 |

- Crash rate omnibus-rest-adjacent: 6/51 = 11.76% (Wilson 95% CI 5.51, 23.38)
- Crash rate omnibus-rest-absent: 2/32 = 6.25% (Wilson 95% CI 1.73, 20.15)
- RR = 1.882 (bootstrap 95% CI 0.403, 5.940)
- RD = 0.055 (bootstrap 95% CI -0.074, 0.175)

### 8.4 Very_heavy end_class

Era-pooled: exposed_true 10/94 (10.6%) vs exposed_false 6/55 (10.9%), RR = 0.975 (bootstrap 95% CI 0.367, 3.409). Pre-cital: 4/44 (9.1%) vs 3/30 (10.0%), RR = 0.909. Post-cital: 6/50 (12.0%) vs 3/25 (12.0%), RR = 1.000. Descriptive-only.

### 8.5 ALL end_class, all-era anchor (MD-beta section 6.6 reproduction)

Per section 1.2: 100/12/168/34 with RR = 1.571. Reproduces MD-beta section 6.6 whole-pool K=3 rest-after RR = 1.57 byte-for-byte.

Additional era splits:
- Pre-cital ALL end_class: 55/7/101/22, exposed_true rate 21.8% (Wilson 14.85, 30.78) vs exposed_false 12.7% (Wilson 6.30, 24.02), RR = 1.711, bootstrap 95% CI 0.839, 4.992.
- Post-cital ALL end_class: 57/5/101/12, exposed_true 11.9% (Wilson 6.93, 19.63) vs exposed_false 8.8% (Wilson 3.81, 18.94), RR = 1.354, bootstrap 95% CI 0.534, 5.495.

### 8.6 Descriptive observation

The omnibus pooled RR on heavy end_class (2.11 era-pooled) is elevated relative to the ALL end_class whole-pool baseline (1.57 era-pooled); the very_heavy pooled RR is close to 1.00 at every era read. The omnibus-heavy pattern is descriptively consistent with parent Wave 2B section 10 whole-corpus intensity-stratified RR (heavy = 2.07, very_heavy = 0.96) and confirms the intensity primary-stratifier upgrade codified at MD-beta section 5 confound 2. Per MD-beta section 3.7 composition-shift caveat, this omnibus read is caveat-class descriptive at r2; no direction pre-commit was made because the omnibus mixes strategic + crisis at a shifting composition ratio across eras (Wave 2C section 3.2 rest-day composition drift).

---

## 9. Absolute-step operand sensitivity (moves-with-envelope artefact test)

Primary sensitivity operand: `rest_day_abs_3k = total_steps < 3000` AND gevoelscore >= 5 (absolute-step strategic; no rolling-baseline). Per MD-beta section 3.1 recommendation 3 absolute-step sensitivity companion + Wave 2C section 5.5 rolling-baseline moves-with-envelope concern. Wave 2D section 7 empirical anchor: pooled RR shifts 0.354 to 0.111 in the sign-flip direction; 2024 RR shifts 0.929 to 0.652 modestly.

Source: [`output/abs3k_strategic_heavy_K3_after.csv`](output/abs3k_strategic_heavy_K3_after.csv).

### 9.1 Heavy end_class, era-pooled

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| abs3k_strategic_rest_after_3 False | 107 | 30 | 137 |
| abs3k_strategic_rest_after_3 True | 26 | 0 | 26 |

- Crash rate abs3k-strategic-rest-adjacent: 0/26 = 0.00% (Wilson 95% CI 0.00, 12.87)
- Crash rate abs3k-strategic-rest-absent: 30/137 = 21.90% (Wilson 95% CI 15.79, 29.54)
- RR (Haldane-corrected: +0.5 to all cells): 0.084
- RD: -0.219 (bootstrap 95% CI -0.290, -0.151)
- Fisher's exact p-value: 0.0047
- Wilson-viable floor: PASS (26 exposed).
- Haldane-Anscombe correction applied because the exposed-True crash count is zero.

### 9.2 Descriptive observation

Restricting the rest-day operand to an absolute-step threshold (total_steps < 3000) plus strategic gs shows the same directional pattern as the rolling-baseline strategic-primary read in section 3: strategic-rest-adjacent shows a LOWER crash rate than strategic-rest-absent (0.0% vs 21.9%). The zero-crash exposed arm (0/26) means the raw RR is undefined; the Haldane-corrected RR (0.084) sits in the sign-flip direction. RD (-0.219) has a bootstrap 95% CI excluding zero.

Per MD-beta section 3.1 absolute-step sensitivity companion codification: this read tests whether the section 3 headline pattern is an artefact of the rolling-baseline moves-with-envelope. The observed direction (rest-adjacent lower) survives the operand swap; the descriptive read on the section 3 headline pattern is NOT explained solely by the rolling-baseline artefact concern.

**Cross-reference note vs MD-beta section 3.1 anchor**: MD-beta section 3.1 sensitivity companion paragraph cites Wave 2D section 7 pooled RR shift from 0.354 to 0.111. That Wave 2D anchor is on an ALL-end_class + proactive-filter operand. This audit's abs3k read reports Haldane-corrected RR = 0.084 on heavy-end_class only + no proactive filter. Both sit in the sign-flip direction; the 0.111 vs 0.084 magnitude delta is operand-scope (intensity restriction + proactive-filter presence + Haldane on zero-crash arm). The audit magnitude 0.084 is NOT a byte-match against the MD-beta cited 0.111; the two RRs are operand-analogous rather than operand-identical.

---

## 10. K-ladder sensitivity (K=1, K=2, K=3)

Same operand and end_class restriction as section 3 (strategic x heavy), varying the tightness-of-adjacency window K across {1, 2, 3} per MD-beta section 3.2 K-ladder.

Source: [`output/kladder_strategic_heavy_after.csv`](output/kladder_strategic_heavy_after.csv).

### 10.1 K=1 rest-after

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| strategic_rest_after_1 False | 112 | 30 | 142 |
| strategic_rest_after_1 True | 21 | 0 | 21 |

- Crash rate: 0/21 = 0.00% (Wilson 0.00, 15.46) vs 30/142 = 21.13% (Wilson 15.22, 28.56)
- RR (Haldane-corrected): 0.107; RD -0.211 (bootstrap 95% CI -0.281, -0.144)

### 10.2 K=2 rest-after

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| strategic_rest_after_2 False | 105 | 30 | 135 |
| strategic_rest_after_2 True | 28 | 0 | 28 |

- Crash rate: 0/28 = 0.00% (Wilson 0.00, 12.06) vs 30/135 = 22.22% (Wilson 16.03, 29.95)
- RR (Haldane-corrected): 0.077; RD -0.222 (bootstrap 95% CI -0.295, -0.153)

### 10.3 K=3 rest-after (headline)

Reproduces section 3.1: 40/2 vs 122/28, RR = 0.218 (bootstrap 95% CI 0.000, 0.610).

### 10.4 Descriptive observation

At K=1 and K=2 the exposed strategic-adjacent arm has zero crashes (0/21 and 0/28 respectively), forcing Haldane correction on RR. The RD reads are consistently in the pre-commit direction across the K-ladder (-0.211 at K=1, -0.222 at K=2, -0.180 at K=3). At K=3 the exposed arm gains 2 crashes because the wider adjacency window admits more episodes that happen to be strategic-adjacent-and-crashing. The tightness-of-adjacency read is descriptively consistent with the pre-commit direction across the K-ladder; wider K does not sign-invert the finding. Per MD-beta section 3.2 rationale, K=3 remains the primary because it matches the parent Q24 MD outcome window +5d and the Chu 2018 24-72h PEM-peak anchor.

---

## 11. Rest-BEFORE-heavy companion (K=3 rest-before)

Same operand and end_class restriction as section 3, direction = rest-BEFORE (window [D_start-3, D_start-1] where D_start is the first day of the heavy episode) per MD-beta section 3.3.

Source: [`output/restbefore_strategic_heavy_K3.csv`](output/restbefore_strategic_heavy_K3.csv).

### 11.1 Era-pooled

| | crash_in_5d False | crash_in_5d True | Total |
|---|---:|---:|---:|
| strategic_rest_before_3 False | 100 | 24 | 124 |
| strategic_rest_before_3 True | 34 | 6 | 40 |

- Crash rate strategic-rest-before-adjacent: 6/40 = 15.00% (Wilson 95% CI 7.06, 29.07)
- Crash rate strategic-rest-before-absent: 24/124 = 19.35% (Wilson 95% CI 13.37, 27.19)
- RR = 0.775 (bootstrap 95% CI 0.242, 1.584)
- RD = -0.044 (bootstrap 95% CI -0.169, 0.091)

### 11.2 Pre-cital era

12 exposed / 69 unexposed with 2/12 vs 20/69 crashes. Crash rate 16.67% vs 28.99%; RR = 0.575 (bootstrap 95% CI 0.000, 1.597). Wilson-viable floor: PASS.

### 11.3 Post-cital era

28 exposed / 55 unexposed with 4/28 vs 4/55 crashes. Crash rate 14.29% vs 7.27%; RR = 1.964 (bootstrap 95% CI 0.346, 8.848). Bootstrap CI includes 1.0.

### 11.4 Descriptive observation

The rest-BEFORE-3 strategic contrast on heavy end_class shows a much smaller directional effect than the rest-AFTER-3 contrast. Era-pooled RR = 0.775 with bootstrap 95% CI (0.242, 1.584) including 1.0. Per-era reads sign-flip: pre-cital rest-before shows RR = 0.575 (direction consistent with pre-commit, wide CI including 1.0); post-cital rest-before shows RR = 1.964 (sign-inverted, wide CI including 1.0).

Endogeneity-asymmetry caveat per MD-beta section 3.9 confound 1 item 2: rest-BEFORE is more endogenous than rest-AFTER (the participant may have rested before the heavy episode because they felt bad, biasing the rest-before-adjacent arm toward crash-vulnerable episodes); a smaller or sign-inverted pre-commit direction on rest-before is consistent with the endogeneity being stronger on that direction. The rest-after / rest-before asymmetry is itself a substantive descriptive finding per MD-beta section 3.3 K-symmetry rationale.

**Two-framing cross-reference for the post-cital sign-inversion**: the post-cital rest-BEFORE-3 sign-inversion (RR = 1.964) has TWO possible descriptive framings both consistent with the pre-commit: (i) endogeneity-asymmetry per MD-beta section 3.9 confound 1 item 2 as stated above, and (ii) pre-cital vs post-cital era instability documented at section 12.4 which affects the rest-after direction as well (per-era rest-after CIs both include 1.0 while the pooled excludes 1.0). Both framings sit side-by-side without either being load-bearing; a Stage S1 or downstream synthesis must NOT over-attribute the post-cital rest-before sign-inversion to a single mechanism at this stage of the descriptive audit.

---

## 12. Descriptive observations

### 12.1 Sign of the headline read relative to the pre-commit

The section 3 headline cell (strategic x heavy x K=3 rest-after x crash-in-5d, era-pooled) shows a lower crash rate on the strategic-adjacent arm than on the strategic-absent arm (5.00% vs 22.95%; RR = 0.218 with bootstrap 95% CI 0.000, 0.610). This is **descriptively consistent with the MD-beta section 3.7 pre-commit direction at era-pooled read on heavy end_class only**. Per CONVENTIONS section 2.1 descriptive-before-inference, this is a descriptive observation and NOT a validation; the Stage D descriptive audit reports the pattern; any inferential-verdict framing is a downstream Stage H pre-registration + Stage H test concern.

Per MD-beta section 6.9 generalisation-scope attestation, this consistent-with-pre-commit descriptive observation is scoped to heavy end_class ONLY. Section 5 very_heavy sensitivity documents that the descriptive pattern sign-inverts on very_heavy end_class (era-pooled RR = 1.418).

### 12.2 Sign-inversions surfaced

- **Very_heavy end_class strategic contrast (section 5)**: RR = 1.418 era-pooled, 1.137 pre-cital, 1.600 post-cital. Sign-inverted relative to MD-beta section 3.7 strategic pre-commit direction. Per MD-beta section 6.9 generalisation-scope attestation this is expected non-generalisation; per MD-beta section 5 confound 8 the very_heavy sign-inversion is the (e) intensity-interaction leg of the 2024 residual tension.
- **Post-cital rest-BEFORE-3 (section 11.3)**: RR = 1.964 with bootstrap 95% CI including 1.0. Sign-inverted relative to section 3.7 pre-commit; expected under section 3.9 confound 1 item 2 endogeneity asymmetry.
- **Omnibus-heavy era-pooled (section 8.1)**: RR = 2.111 with bootstrap 95% CI (1.017, 6.711). No direction pre-commit was made on the omnibus at r2 per MD-beta section 3.7 composition-shift caveat, so this is a descriptive read against no pre-commit; the pattern nonetheless matches parent Wave 2B section 10 intensity finding.
- **Crisis-primary reads (section 6)**: RR > 1.0 across every floor-passing cell; era-pooled heavy RR = 4.714, pre-cital heavy RR = 4.267. This is the pre-committed reversed direction per MD-beta section 3.7 crisis-operand direction pre-commit; NOT an anti-commit sign-inversion. Reciprocal-pair discipline attestation per section 6 headnote.

### 12.3 Sample-floor failures logged

- crisis_p25 x very_heavy x pre-cital: 8 exposed vs 65 unexposed. Narrative read only per section 6.5.
- strategic_abs3k x heavy x pre-cital: 4 exposed vs 78 unexposed. Not reported as its own section; the era-pooled abs3k read in section 9 stands as the primary abs-step read.

### 12.4 Pre-cital vs post-cital era instability of the strategic-primary headline

Per-era point estimates on the section 3 + 4 strategic-primary headline: RR = 0.343 pre-cital vs RR = 0.238 post-cital; both bootstrap CIs include 1.0. The era-pooled cell is CI-tighter but pools across the primary stratifier per MD-beta section 5 confound 7. The era-stratified companions per MD-beta section 6.9 era-pooled headline rationale attestation are the falsifiability-carrying arm of the pooled read; they descriptively support the pre-commit direction on both eras without individually excluding the null.

### 12.5 K-ladder tightness

K=1 and K=2 rest-after strategic reads show zero crashes on the exposed arm (0/21 and 0/28), forcing Haldane-corrected RRs. The RD reads (-0.211 and -0.222) are close to the K=3 RD (-0.180). Tightness of the adjacency window does not sign-invert the pattern; wider K admits more episodes into the strategic-adjacent arm, some of which do crash.

### 12.6 Absolute-step operand survives the moves-with-envelope test

The section 9 absolute-step-strategic read (0/26 vs 30/137, RD -0.219) preserves the direction of the section 3 headline. Per MD-beta section 3.1 absolute-step sensitivity companion rationale, this descriptive read reduces (does not eliminate) the moves-with-envelope artefact concern for the section 3 headline.

### 12.7 Discipline reminder: reciprocal definitional-pair

The strategic-primary headline (section 3, RR = 0.218) and the crisis-sensitivity contrast (section 6, RR = 4.714 on the heavy era-pooled cell) are two views of the same joint (rest_day_p25 True) x (gs_bucket) partition. Per MD-beta section 3.7 reciprocal-attestation, ANY Stage S1 synthesis that treats these as independent evidence violates the definitional-pair discipline. Both reads collapse into ONE definitional-pair split at Stage S1.

### 12.8 Operand-scope tension vs the MD-beta section 3.7 empirical anchor

MD-beta section 3.7 cites the Wave 2C proactive-strategic pooled RR = 0.354 as the empirical anchor for the strategic direction pre-commit. That empirical anchor was measured on the Wave 2C **proactive-strategic** operand, which adds a `no is_crash in [d-3, d-1]` filter to the strategic definition. The MD-beta section 3.1.1 primary operand is **pure-strategic** (`rest_day_p25 == True AND gs >= 5`), without the prior-3-day-crash filter.

Section 1.3 reproduces both variants on the same ALL end_class + K=3 rest-after + era-pooled cell:

- Pure-strategic (MD-beta section 3.1.1 primary): 84 True / 226 False with 8/38 crashes, RR = 0.566.
- Proactive-strategic (Wave 2C empirical anchor): 80 / 230 with 5/41 crashes, RR = 0.351 (reproduces Wave 2C 0.354 within 0.9%).

Both variants match the MD-beta section 3.7 pre-commit direction (strategic-adjacent -> LOWER); the magnitude difference is operand-scope (proactive filter shrinks the arm-True side by 4 episodes and drops 3 crashes from that arm, tightening the RR toward the sign-flip direction).

A Stage S1 synthesis reader must NOT read the section 3 headline RR = 0.218 (pure-strategic on heavy end_class only) as a byte-match against the MD-beta section 3.7 cited RR = 0.354 (proactive-strategic on ALL end_class). The two empirical points support the same pre-commit direction but come from operand-analogous rather than operand-identical reads with a further intensity restriction on the section 3 headline (heavy end_class only). This is a framing tightening for Stage S1 and downstream Stage H, not a numerical revision at Stage D. Cross-reference to section 1.3 reproduction spot-check.

---

## 13. Discipline compliance attestations

- **CONVENTIONS section 2.1 descriptive-before-inference**: no inferential verdicts emitted at Stage D; Fisher's exact p-values reported for completeness only per MD-beta section 3.6 statistical-framing note.
- **CONVENTIONS section 3.3 definitional-pair discipline**: strategic + crisis reported as ONE definitional-pair split at section 6; borderline reported as its own descriptive stratum at section 7; omnibus reported as caveat-class descriptive at section 8. Reciprocal-attestation upfront at section 6 head + section 12.7 reminder.
- **CONVENTIONS section 3.6 named-count discipline**: all counts named with scheme (episode-end, day-level, is_crash column) + unit (episodes, days) + source (parent Wave 2B section, MD-beta section, or script output CSV path).
- **CONVENTIONS section 3.10 NaN-boundary rule**: gevoelscore-NaN drops from the strategic + crisis + borderline operands (undef flag). Omnibus `rest_day_p25` uses NaN=False convention per MD-beta section 3.10 to reproduce the section 6.6 baseline anchor byte-for-byte. Both conventions documented at section 2.
- **CONVENTIONS section 4.2 caveat-class framing**: all six MD-beta section 3.9 confounds + section 5 confounds 1 through 8 acknowledged as caveats, not corrections. No post-hoc adjustment attempted at Stage D.
- **Descriptive-before-theory discipline** (user 2026-07-17 directive): NO citation of `resilience_latent_state.md`; NO latent-state / R(t) / reserve / buffer / envelope-capacity constructs anywhere in this audit.
- **Physical-rest-only semantic constraint** per memory `project_rest_day_operand_semantics`: all `_physical_` operands measure low-step days modulated by gevoelscore-on-that-day; they do NOT measure cognitive rest, emotional rest, or planning quality. Constraint respected throughout.
- **6-mechanism era caveat** per MD-beta section 5 confound 7: verbatim at section 4.4; no causal attribution at n=1.
- **Reciprocal-attestation upfront** per MD-beta section 3.7 recommendation 4: at section 6 head + section 12.7 reminder.
- **Generalisation-scope attestation** per MD-beta section 6.9 recommendation 5: headline claim scoped to heavy end_class only per section 3.2 descriptive observation + section 5 non-generalisation cell.
- **Era-pooled headline rationale attestation** per MD-beta section 6.9 recommendation 6: era-pooled cell + immediate era-stratified companions in section 3 and section 4 side-by-side; falsifiability carried by the immediate era-stratified arm.
- **Autocorrelation attestation** per MD-beta section 3.5.1 recommendation 2: bootstrap block length = 1 inherits parent Q24 MD section 7.10; the joint (rest-gs-bucket) x (end_class) stratifier does not introduce autocorrelation the unit-of-analysis choice does not already address.
- **Wilson-viable floor** per user Option B: informal ~10-per-arm threshold; failures marked NEEDS-MORE-DATA at section 6.5.
- **Haldane-Anscombe correction**: applied to RR only on cells with any raw cell = 0; correction labelled in the `haldane_applied` column of every output CSV.
- **Multiple-testing surface disclosure**: this audit reports 30+ cells across headline (1 pooled + 2 era-stratified companions), very_heavy sensitivity (3), crisis (5 floor-passing + 1 NEEDS-MORE-DATA), borderline (2), omnibus (9), abs-step (1), K-ladder (3), rest-BEFORE (3). Fisher's exact p-values reported at individual cells (0.0097 headline; 0.0047 abs-step; 3.26e-06 crisis heavy pooled; 6.02e-05 crisis heavy pre-cital; smaller values on the crisis stratum reflect the wide arm-rate gap, not a Stage-D inferential claim) are descriptive-only per CONVENTIONS section 2.1 and are NOT interpreted at Stage D. No single p-value crosses to a verdict; the audit does not commit to any inferential threshold at any cell. Any Stage S1 or downstream Stage H reader who treats a single Fisher p as inferentially load-bearing must first account for the 30-cell multiple-testing surface. The descriptive-with-CI framing (bootstrap 95% CI on RR; Wilson 95% CI per arm) is the primary evidential surface at Stage D; Fisher p-values are a completeness column, not the verdict axis.
- **No em-dash in any output text** per memory `feedback_no_emdash_in_ui`.
- **No emoji anywhere** in the audit MD or the script.

---

## 14. Lock log

| version | date | change |
|---|---|---|
| r1 DRAFT | 2026-07-19 | Initial DRAFT for fresh-session review. Producer-mode subagent draft per CONVENTIONS section 1.2 under user delegation (authorising user: Willem). Walks headline cell per MD-beta section 6.9 (strategic x heavy x K=3 rest-after x crash-in-5d, era-pooled) plus 8 companion families: era-stratified sensitivity (pre-cital + post-cital), very_heavy end_class sensitivity, crisis-rest x end_class stratified with reciprocal-pair attestation, borderline-rest x end_class stratified, omnibus rest x end_class stratified with MD-beta section 6.6 byte-for-byte anchor reproduction, absolute-step operand sensitivity, K-ladder K=1 / K=2 / K=3, rest-BEFORE-heavy K=3 companion. Preflight sample-floor probe (36 cells, 34 pass, 2 fail) enumerated per user Option B; two failing cells (crisis vh pre-cital n=8 exposed; abs3k pre-cital n=4 exposed) reported narrative-only. Discipline attestations at section 13. Statistical machinery per MD-beta section 3.6 (Wilson CI + Fisher exact + bootstrap B=10000 seed=20260716 + Haldane correction). Descriptive-only per CONVENTIONS section 2.1; no verdicts. No latent-state / R(t) / reserve / buffer / envelope-capacity constructs; no citation of `resilience_latent_state.md` per user 2026-07-17 descriptive-before-theory directive. Awaiting fresh-session review before r1 LOCK. |
| r1 LOCKED | 2026-07-19 | Fresh-session methodology review absorbed from [`../../../reviews/methodology-Q24-mdbeta-stageD-rest-adjacency-2026-07-19.md`](../../../reviews/methodology-Q24-mdbeta-stageD-rest-adjacency-2026-07-19.md) (verdict: DEFENSIBLE with revision; 6 absorb-tier recommendations all applied inline; 0 substantive; 0 escalate; no architectural revision required). Six surgical patches per CONVENTIONS section 1.2 compression discipline (mechanical clarifications + framing tightenings + one new subsection; no numerical revision). **Patch 4.1 absorbed** (§3.1 + §8 NaN-policy cross-reference per L4.12 absorb): added NaN-policy cross-reference sentences at §3.1 (strategic pool undef-drop convention explaining 162-vs-165 pool delta) and at §8 preamble (omnibus NaN=False convention retained for §6.6 anchor). Consistent split policy documented; prevents Stage S1 readers from misreading the pool-size delta as an operand-selection artefact. **Patch 4.2 absorbed** (new §12.8 operand-scope tension subsection per L4.13 absorb): new §12.8 explicitly discusses the operand-scope tension between MD-beta section 3.7 empirical anchor RR = 0.354 (Wave 2C proactive-strategic, adds no-crash-in-prior-3d filter) and MD-beta section 3.1.1 primary operand (pure-strategic, no prior-3d filter); reproduces both variants on ALL end_class K=3 rest-after era-pooled (pure-strategic RR = 0.566; proactive-strategic RR = 0.351 reproducing Wave 2C 0.354 within 0.9%); states clearly that both match the pre-commit direction but from operand-analogous rather than operand-identical reads; forbids Stage S1 byte-match reading of the section 3 headline RR = 0.218 against MD-beta cited RR = 0.354. Section 1.3 spot-check cross-referenced. **Patch 4.3 absorbed** (§9.2 abs-step reconciliation vs Wave 2D 0.111 per L4.15 absorb): added cross-reference note in §9.2 explaining MD-beta section 3.1 sensitivity companion cites Wave 2D pooled RR shift 0.354 -> 0.111 on ALL-end-class + proactive-filter operand; the audit's own RR = 0.084 is on heavy-end-class only + no proactive filter + Haldane; magnitude delta is operand-scope, direction preserved across both. **Patch 4.4 absorbed** (§13 multiple-testing surface disclosure bullet per L3.3 absorb): new bullet enumerates the 30+ cell surface (headline 3 + very_heavy sensitivity 3 + crisis 6 + borderline 2 + omnibus 9 + abs-step 1 + K-ladder 3 + rest-BEFORE 3) and states that all Fisher p-values including the crisis stratum's small p = 3.26e-06 are descriptive-only per CONVENTIONS section 2.1; no single p crosses to a verdict at Stage D; Stage S1 or downstream Stage H readers must account for the multiple-testing surface before treating any single Fisher p as inferentially load-bearing. Descriptive-with-CI is the primary evidential surface; Fisher p a completeness column. **Patch 4.5 absorbed** (§6.5 Wilson-computable-but-withheld attestation per L4.16 discretionary absorb): added note at §6.5 that Wilson per-arm CIs are mathematically computable at n=8 exposed but deliberately withheld from the audit body per the Wilson-viable floor policy; the script writes the computed bounds to the output CSV for reproducibility trace but the body silence is deliberate discipline, not a computation gap. **Patch 4.6 absorbed** (§11.4 two-framing cross-reference for post-cital rest-before sign-inversion per L4.6-analogue discretionary absorb): added "Two-framing cross-reference" paragraph at end of §11.4 stating the post-cital rest-before sign-inversion (RR = 1.964) has two descriptive framings both consistent with the pre-commit: (i) endogeneity asymmetry per MD-beta section 3.9 confound 1 item 2, (ii) pre-cital vs post-cital era instability per §12.4; forbids over-attribution to a single mechanism at Stage D. **Preserved byte-identically vs r1 DRAFT**: every 2x2 table (100/12/168/34 baseline reproduction; 40/2 vs 122/28 headline; every companion contingency), every RR + bootstrap CI + Wilson CI + Fisher p + RD; §1.1 corpus counts + §1.4 preflight table + §1.5 cell inventory; §2 reproducibility (script path, seed, statistical machinery, NaN handling per operand, era stratifier, unit of analysis); §4.4 6-mechanism era caveat verbatim from MD-beta section 5 confound 7; §5 very_heavy sensitivity framing as expected non-generalisation per §6.9 generalisation-scope attestation; §6 reciprocal-attestation upfront body; §7 borderline descriptive-only body; §10 K-ladder body; §11 rest-BEFORE body except §11.4 addition; §12.1-§12.7 preserved verbatim; §13 attestation bullets preserved except new multiple-testing bullet inserted between Haldane and no-em-dash items. **No numerical revisions**: every count, RR, Wilson CI, bootstrap CI, RD, Fisher p in the r1 DRAFT is preserved byte-identically in r1 LOCKED. **STATUS**: LOCKED r1 2026-07-19 post-review absorption. Stage D descriptive audit for MD-beta section 6.9 headline cell + companion sensitivity family fully landed. Any downstream Stage H pre-registration for the rest-adjacency arc drafts in a separate reviewer-mode-authorized session per MD-beta section 6.9 + section 7 compression discipline; this Stage D r1 LOCKED provides the operand-locked descriptive baseline. |
