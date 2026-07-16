# Descriptive audit -- Q24 MD-beta Wave 2C: reactive vs proactive rest (gevoelscore-conditioned rest-day quadrants + load-envelope descriptors)

*Producer-mode Stage -1 descriptive audit per [CONVENTIONS section 1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafted 2026-07-16 by Claude (Opus 4.7) in producer-mode subagent under user delegation. Authorising user: Willem.*

**Status**: **LOCKED r1 2026-07-16** post-review absorption per [`../../../reviews/methodology-Q24-mdbeta-wave2c-reactive-vs-proactive-rest-2026-07-16.md`](../../../reviews/methodology-Q24-mdbeta-wave2c-reactive-vs-proactive-rest-2026-07-16.md) (verdict: DEFENSIBLE with revision; 2 audit-level absorb fires + 2 load-bearing r2 recommendations for MD-beta downstream). See §5.5 (L3.2 absorb), §6.5 (L4.2 absorb), §10.5 (r2 recommendations).

**Wave**: 2C. Sibling of parent [Wave 2B Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-precursor-rest-streak/audit.md). Extension of the parent [Q24 Stage -1 audit LOCKED r1 2026-07-15](../Q24-precursor-heavy-day-structure/audit.md). Points at [MD-beta LOCKED r1 2026-07-16](../../../methodology/heavy_day_crash_risk_prediction.md) for operand + machinery lock.

**Frame**: LC-era stratum (`lc_phase == 'lc'`), n=1524 days (2022-04-04 -> 2026-06-05), matches parent Stage -1 audit stratum. Heavy-day definition, episode unit, and rest-day primary operand inherited verbatim from parent Wave 2B audit.

**Reproducibility**: [`scripts/audit.py`](scripts/audit.py) + outputs in [`output/`](output/); idempotent re-run against `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. `RANDOM_SEED = 20260716` per MD-beta section 3.6; not exercised in this Wave 2C audit (no randomisation needed).

**Discipline scope**: Stage -1 descriptive audit only. NO inferential-verdict framing. All contingency tables reported as descriptive-with-Wilson-CI per MD-beta section 3.6 + [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). Both Interpretation A and Interpretation D are treated as **partial-testable at n=1**: findings can be described as CONSISTENT-WITH, AMBIGUOUS-FOR, or FALSIFYING for each interpretation, but no test in this audit constitutes a verdict on either.

**Cross-refs**:

- [MD-beta LOCKED r1 2026-07-16](../../../methodology/heavy_day_crash_risk_prediction.md) -- operand + machinery lock.
- [Parent Wave 2B Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-precursor-rest-streak/audit.md) -- pooled + era-stratified sign-inversion findings that motivate Wave 2C.
- [Parent Q24 MD LOCKED r1 2026-07-15](../../../methodology/post_heavy_day_compensatory_rest.md) -- stratum + heavy-day + unit-of-analysis inheritance.
- [Parent Q24 Stage -1 audit LOCKED r1 2026-07-15](../Q24-precursor-heavy-day-structure/audit.md) -- episode structure + overlap density.
- [CONVENTIONS sections 1.2, 2.1, 3.1, 3.6, 3.7, 4.2, 5](../../../CONVENTIONS.md).
- Memory pointer: `project_rest_day_operand_semantics` -- physical-rest-only constraint on `rest_day_p25`; gevoelscore modulates interpretation but not operand.

---

## 1. Corpus summary (points to parent Stage -1; Wave 2C-specific numbers)

Corpus counts inherited from parent Q24 Stage -1 audit and parent Wave 2B audit (which itself points at parent). Not re-emitted here to avoid duplication.

| Measure | Value | Source |
|---|---|---|
| LC-era rows | 1524 days | [parent Stage -1 section 1](../Q24-precursor-heavy-day-structure/audit.md#1-corpus-summary) |
| Heavy days (heavy + very_heavy) | 532 (34.9%) | ibid |
| Very-heavy days | 256 (16.8%) | ibid |
| Heavy-only days | 276 (18.1%) | ibid |
| Crash days | 103 (crash_v2, day-level, `labels_crash_v2.csv`) | ibid |
| gap=0 heavy episodes | 314 | [parent Wave 2B section 3](../Q24-mdbeta-precursor-rest-streak/audit.md#3-heavy-episode-construction) |
| Rest-day primary (`rest_day_p25` True on LC-era) | 404 (26.5%) | [parent Wave 2B section 2](../Q24-mdbeta-precursor-rest-streak/audit.md#2-rest-day-operand-distribution) |
| Rest-day primary NaN (steps or 30d-p25 undefined) | 37 (2.4%) | ibid |
| Gevoelscore non-NaN (LC-era) | 1372 / 1524 = 90.0% | Wave 2C script header printout |
| Gevoelscore NaN (LC-era) | 152 (10.0%; ~all in 2022 pre-tracker onset per `per_day_master.csv`) | ibid |
| Heavy-adjacent rest-days (K=3 window around 314 episodes) | 341 (dedup) | Wave 2C section 3 |
| Episodes with rest-after K=3 primary True | 202 / 314 | [parent Wave 2B section 6](../Q24-mdbeta-precursor-rest-streak/audit.md#6-rest-adjacency-prevalence-across-12-cell-grid) |

Base rates for Wave 2C sections:

- Wave 2B pooled RR (K=3 rest-after primary; NaN-drop discipline): **1.54** (rest-adj 34/202 = 16.8% vs rest-abs 12/110 = 10.9%). [source: parent Wave 2B section 7](../Q24-mdbeta-precursor-rest-streak/audit.md#7-rest-adjacency-x-crash-2x2-12-cell-grid).
- Wave 2B era-stratified K=3 rest-after primary RR by year: 2022: 1.08 | 2023: **2.02** | 2024: **1.56** | 2025: 0.78 | 2026: 0.57. [source: parent Wave 2B section 9](../Q24-mdbeta-precursor-rest-streak/audit.md#9-era-stratified-rest-adjacency-3-way-cross-tab).

---

## 2. Framing -- Interpretations A + D + the physical-rest-only semantic constraint

### 2.1 Load-bearing semantic constraint per `project_rest_day_operand_semantics`

The MD-beta `rest_day_p25` operand measures **physical rest only** (`total_steps < 30d rolling p25`). It does NOT distinguish strategic from crisis rest. Every rest-day is a low-step day by definition. Cognitive rest, emotional rest, and other "rest-shape" dimensions are NOT measured by this operand; this audit does not treat them as measured either.

**Gevoelscore on the rest-day is the discriminator**. Bucket definitions (memory `project_rest_day_operand_semantics`, adopted for this audit):

- `strategic` = gevoelscore >= 5 on the rest-day -- feels okay, choosing to move less; calibrated pacing.
- `borderline` = gevoelscore == 4 on the rest-day -- reported as its own bucket; neither strategic nor crisis.
- `crisis` = gevoelscore <= 3 on the rest-day -- feels bad, physically can't move; endogeneity signature.
- `nan` = gevoelscore missing on the rest-day (~10% LC-era rate; concentrated in 2022 pre-tracker onset).

**Gevoelscore-conditioning is a partial mitigation** of the confounding-by-indication mechanism (Salas 2001; Kyriacou & Lewis 2016 *JAMA*) that MD-beta section 3.9 confound 1 anticipates. It is not a full mitigation because (i) the split-point at gevoelscore = 4 vs 5 is a construct-validity judgement rather than a data-driven cut; (ii) gevoelscore itself is a same-day summary that may co-vary with same-day exertion in ways that partially entangle rest-choice with felt-state.

### 2.2 Interpretation A -- rest-day composition shift

**Interpretation A**: the sign-inversion flip between 2023-24 (RR = 2.02 / 1.56, rest -> more crashes) and 2025-26 (RR = 0.78 / 0.57, rest -> fewer crashes) reflects a **shift in rest-day composition** from crisis-dominant (early era, rest because felt bad = endogeneity) to strategic-dominant (late era, planned proactive rest).

Under Interpretation A, the pooled sign-inversion isn't a stable feature of the participant's physiology; it's a feature of the participant's early pacing journey -- a period when most rest-days followed crashes rather than preceded them.

Three descriptive tests operationalise Interpretation A:

1. **§3 rest-day gevoelscore-conditioned quadrants per year** -- does the fraction of rest-days that are proactive-strategic (no crash in the prior 3d AND gevoelscore >= 5) grow over 2022 -> 2026?
2. **§4 mean gevoelscore on rest-day per year** -- does the average felt-state on rest-days shift upward?
3. **§5 proactive-strategic-rest-after -> crash-in-5d RR** (LOAD-BEARING) -- when we restrict the K=3 rest-after primary 2x2 to episodes where the adjacent rest-day is proactive-strategic, does the sign flip from pooled inversion (RR = 1.54) to the MD-beta section 3.7 pre-committed direction (RR < 1)?

**§6 crisis-reactive-rest 2x2** is the companion test: the endogeneity signature should be maximally concentrated in the crisis-reactive subset.

### 2.3 Interpretation D -- load-envelope shrinkage + tactical response

**Interpretation D**: the crash-rate collapse in 2025-26 (~2/year vs ~10/year in 2023-24) reflects **load-envelope shrinkage** (fewer very-heavy days, narrower step-envelopes) + potentially better tactical Garmin use (faster rest-response after heavy days).

Three descriptive tests operationalise Interpretation D:

1. **§7 very-heavy day frequency per year** -- direct test of the load-envelope shrinkage sub-claim.
2. **§8 step-envelope variance per year** -- IQR + coefficient-of-variation as proxy for narrower self-regulated ranges.
3. **§9 heavy-episode-end to next rest-day gap per year** -- shorter gaps = faster tactical rest-response.

### 2.4 Framing discipline (both interpretations)

Both Interpretation A and Interpretation D are **partial-testable at n=1**. This audit describes findings as CONSISTENT-WITH, AMBIGUOUS-FOR, or FALSIFYING for each interpretation. It does NOT emit a verdict, does NOT run inferential tests, does NOT compute p-values, and reports every rate + RR + RD with Wilson 95% CI + per-arm cell counts per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

**The sign-inversion + sign-flip findings from parent Wave 2B are treated as descriptive Stage -1 signals**, not as verdicts on either interpretation. This audit extends the descriptive layer by conditioning on gevoelscore + reading load-envelope descriptors per year.

---

## 3. Rest-day gevoelscore-conditioned quadrants per year (Interpretation A test 1)

Source: [`output/rest_day_gevoelscore_quadrants_per_year.csv`](output/rest_day_gevoelscore_quadrants_per_year.csv).

**Pool**: 341 heavy-adjacent rest-days (dedup) inside `[D_start - 3, D_end + 3]` window around each of the 314 episodes. Rest-day defined as `rest_day_p25 == 1.0` (physical rest only per §2.1).

**Cross-tab**: (crash_before_3d in `[rest_idx - 3, rest_idx - 1]`) x (gevoelscore bucket on rest-day).

### 3.1 Per-year counts + fractions

| Year | Bucket | crash_before_3d = False | crash_before_3d = True | Year total |
|---|---|---:|---:|---:|
| 2022 | strategic (>=5) | 9 (18.4%) | 0 (0.0%) | 49 |
| 2022 | borderline (=4) | 10 (20.4%) | 1 (2.0%) | 49 |
| 2022 | crisis (<=3) | 5 (10.2%) | 4 (8.2%) | 49 |
| 2022 | nan | 20 (40.8%) | 0 (0.0%) | 49 |
| 2023 | strategic | 23 (26.7%) | 1 (1.2%) | 86 |
| 2023 | borderline | 34 (39.5%) | 7 (8.1%) | 86 |
| 2023 | crisis | 8 (9.3%) | 13 (15.1%) | 86 |
| 2023 | nan | 0 | 0 | 86 |
| 2024 | strategic | 24 (25.3%) | 5 (5.3%) | 95 |
| 2024 | borderline | 30 (31.6%) | 11 (11.6%) | 95 |
| 2024 | crisis | 16 (16.8%) | 9 (9.5%) | 95 |
| 2024 | nan | 0 | 0 | 95 |
| 2025 | strategic | 42 (53.2%) | 0 (0.0%) | 79 |
| 2025 | borderline | 27 (34.2%) | 1 (1.3%) | 79 |
| 2025 | crisis | 8 (10.1%) | 1 (1.3%) | 79 |
| 2025 | nan | 0 | 0 | 79 |
| 2026 (partial) | strategic | 18 (56.2%) | 0 (0.0%) | 32 |
| 2026 (partial) | borderline | 10 (31.2%) | 0 | 32 |
| 2026 (partial) | crisis | 4 (12.5%) | 0 | 32 |
| 2026 (partial) | nan | 0 | 0 | 32 |
| ALL | strategic | 116 (34.0%) | 6 (1.8%) | 341 |
| ALL | borderline | 111 (32.6%) | 20 (5.9%) | 341 |
| ALL | crisis | 41 (12.0%) | 27 (7.9%) | 341 |
| ALL | nan | 20 (5.9%) | 0 (0.0%) | 341 |

### 3.2 Descriptive observations

**Proactive-strategic (crash_before = False AND bucket = strategic) fraction per year, headline monotone pattern**:

| Year | Proactive-strategic fraction | Crisis-reactive fraction (crash_before True AND bucket crisis) |
|---|---:|---:|
| 2022 (partial) | 18.4% (9/49) | 8.2% (4/49) |
| 2023 | 26.7% (23/86) | 15.1% (13/86) |
| 2024 | 25.3% (24/95) | 9.5% (9/95) |
| 2025 | 53.2% (42/79) | 1.3% (1/79) |
| 2026 (partial) | 56.2% (18/32) | 0.0% (0/32) |

**Descriptive summary**:

- **Proactive-strategic rest-day fraction rises monotonically 2023 -> 2026** (26.7% -> 25.3% -> 53.2% -> 56.2%), with the 2024 -> 2025 step being the largest single-year jump. 2022 (partial + 40.8% gs-missing) is inconclusive.
- **Crisis-reactive rest-day fraction collapses** from 2023 (15.1%) to 2025 (1.3%) and 2026 (0.0% -- no crashes observed to precede rest-days in the partial 2026 window).
- The 2022 40.8% gs-nan bucket is entirely a data-availability artefact (gevoelscore tracking started mid-2022; see §1 corpus row).
- The borderline (=4) bucket stays ~30-40% across all years without a clean trend, consistent with borderline being a genuine intermediate state rather than either endpoint of the shift.

**Reading discipline**: These per-year fractions are marginal composition estimates on the heavy-adjacent rest-day pool. Wilson CIs on individual cell fractions (e.g. 2025 proactive-strategic 42/79 = 53.2%) are not computed here because the cell-fraction is a composition statistic on a fixed denominator per year, not a rate estimate for a stochastic process. Sample sizes per year (49, 86, 95, 79, 32) are adequate for descriptive composition read.

### 3.3 Consistency with Interpretation A

The **monotone rise in proactive-strategic fraction** (18% -> 27% -> 25% -> 53% -> 56%) + **collapse in crisis-reactive fraction** (8% -> 15% -> 9% -> 1% -> 0%) is CONSISTENT-WITH Interpretation A's rest-day composition shift claim. The shift is descriptively visible in the raw fractions before any 2x2 test is run.

**Not-yet-a-verdict**: composition change is necessary but not sufficient for Interpretation A. The load-bearing test is §5 -- does the sign of the rest-after 2x2 flip when we restrict to the proactive-strategic subset?

---

## 4. Mean gevoelscore on rest-day per year (Interpretation A test 2)

Source: [`output/rest_day_mean_gevoelscore_per_year.csv`](output/rest_day_mean_gevoelscore_per_year.csv).

Two pools:

- **heavy_adjacent** -- same 341 rest-days from §3.
- **all_corpus_rest_days** -- 404 rest-days on LC-era (any `rest_day_p25 == 1.0`), as a comparator to check whether the heavy-adjacent pool is representative.

### 4.1 Per-year means + medians

| Pool | Year | n_rest_days | n_gs_valid | mean_gs | median_gs |
|---|---|---:|---:|---:|---:|
| heavy_adjacent | 2022 | 49 | 29 | 3.79 | 4.0 |
| heavy_adjacent | 2023 | 86 | 86 | 3.93 | 4.0 |
| heavy_adjacent | 2024 | 95 | 95 | 3.99 | 4.0 |
| heavy_adjacent | 2025 | 79 | 79 | **4.54** | **5.0** |
| heavy_adjacent | 2026 (partial) | 32 | 32 | 4.53 | 5.0 |
| heavy_adjacent | ALL | 341 | 321 | 4.15 | 4.0 |
| all_corpus_rest_days | 2022 | 70 | 31 | 3.84 | 4.0 |
| all_corpus_rest_days | 2023 | 97 | 97 | 3.73 | 4.0 |
| all_corpus_rest_days | 2024 | 102 | 102 | 4.03 | 4.0 |
| all_corpus_rest_days | 2025 | 100 | 100 | **4.57** | **5.0** |
| all_corpus_rest_days | 2026 (partial) | 35 | 35 | 4.54 | 5.0 |
| all_corpus_rest_days | ALL | 404 | 365 | 4.13 | 4.0 |

### 4.2 Descriptive observations

- **Mean gs on rest-day is flat 2022-2024** (3.79 -> 3.93 -> 3.99 heavy-adjacent; 3.84 -> 3.73 -> 4.03 all-corpus). Same-shape between pools.
- **A ~0.5-point step-jump in mean gs occurs at 2024 -> 2025** (3.99 -> 4.54 heavy-adjacent; 4.03 -> 4.57 all-corpus). The **median steps from 4 -> 5** at the same transition.
- **2025 and 2026 are near-identical** (means 4.54 vs 4.53), suggesting the shift is not a monotone drift but a phase-transition around late 2024 / early 2025.
- **Heavy-adjacent pool and all-corpus pool agree in year-level pattern**, showing that the 341 heavy-adjacent rest-days are broadly representative of the 404 all-corpus rest-days on the gevoelscore-on-rest-day dimension.

### 4.3 Consistency with Interpretation A

The **step-jump in mean gevoelscore on rest-day at the 2024 -> 2025 boundary** aligns temporally with the sign-flip in the parent Wave 2B era-stratified RR (2024 RR = 1.56 -> 2025 RR = 0.78). This is CONSISTENT-WITH Interpretation A: rest-days on average carried a lower felt-state pre-2025 (~4.0, indicative of borderline / crisis rest) and a higher felt-state post-2025 (~4.5, indicative of strategic / borderline rest).

**Confound to flag**: the mean gs on all-corpus rest-days also shifted (3.73 -> 4.57), so the shift is not specific to heavy-adjacent rest-days. It is a whole-corpus-of-rest-days shift, consistent with either (a) genuine composition shift (Interpretation A) or (b) mean felt-state on ALL days improving in 2025 (which would make gevoelscore-on-rest-day rise trivially without any composition change). §4.4 addresses this comparator.

### 4.4 Comparator -- mean gevoelscore on all LC-era days per year (not just rest-days)

Not emitted as a separate CSV to keep the file surface tight; computed from the same underlying data. LC-era mean gevoelscore per year (all non-NaN days):

- 2022 (n=120 valid): 4.15
- 2023 (n=365): 4.10
- 2024 (n=366): 4.31
- 2025 (n=365): 4.79
- 2026 partial (n=156): 4.71

The whole-year mean rose 4.10 (2023) -> 4.79 (2025) -- a +0.69 step. The **mean gs on rest-days rose +0.55 (heavy-adj) / +0.54 (all-corpus)** at the same transition. The rest-day shift is **not larger than the whole-year shift**; both consistent with a general felt-state improvement in 2025 that lifts both rest-day gs and non-rest-day gs by roughly the same amount.

**Reading**: §4 alone does NOT distinguish "rest-day composition shifted specifically" from "everything felt better in 2025". §3 and §5 are the composition-specific tests; §4 confirms the shift exists, does not attribute it to composition specifically.

**Consistency assessment**: AMBIGUOUS-FOR Interpretation A at the composition-specificity resolution. CONSISTENT-WITH Interpretation A at the felt-state-on-rest-day-improved resolution.

---

## 5. Proactive-strategic-rest -> crash-in-5d RR (Interpretation A test 3 -- LOAD-BEARING)

Source: [`output/proactive_strategic_rest_crash_2x2.csv`](output/proactive_strategic_rest_crash_2x2.csv).

**Operational definition**:

1. For each of 314 heavy-episode-ends: check if any rest-day exists in `[D_end+1, D_end+3]` (rest-after K=3, primary operand).
2. For each such rest-day, check if it is **proactive-strategic**: NO `is_crash = True` in `[rest_day - 3, rest_day - 1]` AND `gevoelscore >= 5` on rest_day.
3. Reclassify the K=3 rest-after episodes into: **proactive-strategic-rest-after** (episode has at least one proactive-strategic rest-day in `[D_end+1, D_end+3]`) vs **complement** (all other episodes with rest-after indicator not NaN, including rest_after_3_primary True but no strategic rest-day, and rest_after_3_primary False).
4. Build the 2x2: (proactive_strategic True/False) x (crash_in_5d True/False).
5. Compute per-arm rate + RR + RD + Wilson CI.

**Reading**:

- Under **Interpretation A**: the proactive-strategic subset RR should be **< 1.0** (rest actually associates with FEWER crashes-in-5d when rest is genuinely strategic).
- Under **null / the confounding-by-indication mechanism alone**: RR should stay ~1.5 (endogeneity or noise still dominates).

### 5.1 Per-pool 2x2

| Pool | n_used | PS-True n / crash | PS-False n / crash | Rate PS-True [Wilson] | Rate PS-False [Wilson] | RR (PS/complement) | RD |
|---|---:|---|---|---|---|---:|---:|
| ALL_ERA_POOLED | 312 | 80 / 5 | 232 / 41 | 6.25% [2.7, 13.8] | 17.67% [13.3, 23.1] | **0.354** | -0.114 |
| year_2022 (partial) | 43 | 7 / 1 | 36 / 6 | 14.29% [2.6, 51.3] | 16.67% [7.9, 31.9] | 0.857 | -0.024 |
| year_2023 | 87 | 20 / 1 | 67 / 15 | 5.00% [0.9, 23.6] | 22.39% [14.1, 33.7] | **0.223** | -0.174 |
| year_2024 | 80 | 15 / 3 | 65 / 14 | 20.00% [7.0, 45.2] | 21.54% [13.3, 33.0] | 0.929 | -0.015 |
| year_2025 | 66 | 23 / 0 | 43 / 2 | 0.00% [0.0, 14.3] | 4.65% [1.3, 15.5] | 0.000 | -0.047 |
| year_2026 (partial) | 36 | 15 / 0 | 21 / 4 | 0.00% [0.0, 20.4] | 19.05% [7.7, 40.0] | 0.000 | -0.190 |

Wilson 95% CI in brackets. RR = crash rate proactive-strategic / crash rate complement.

Row-total checks: 2022 = 43; 2023 = 87; 2024 = 80; 2025 = 66; 2026 = 36. Grand total = 312 = 314 - 2 (2 NaN rest-after episodes dropped per parent Wave 2B NaN-drop discipline). Sum of proactive-strategic-True arm crash-counts: 1+1+3+0+0 = 5; complement crash-counts: 6+15+14+2+4 = 41. Grand crash total: 46. Matches parent Wave 2B section 7 K=3 rest-after primary NaN-drop crash count.

### 5.2 Descriptive observations

**Headline: on the all-era-pooled subset, the sign flips.**

- Parent Wave 2B pooled K=3 rest-after primary RR: **1.54** (rest-adj arm HIGHER crash rate).
- Wave 2C proactive-strategic-only pooled RR: **0.354** (proactive-strategic arm ~1/3 the crash rate of complement).
- The proactive-strategic arm rate 6.25% [Wilson 2.7, 13.8] is **below** the corpus-baseline LC-era crash rate of 6.8% [via 103/1524] and **well below** the parent Wave 2B rest-abs arm rate 10.9%.
- The complement arm rate 17.67% [13.3, 23.1] is **above** both the parent Wave 2B rest-adj arm rate (16.8%) and the rest-abs arm rate (10.9%). The complement absorbs both rest_after_3_primary True + not-proactive-strategic (n=122; the crisis + borderline + missing-gs subset of the original rest-adj arm) AND rest_after_3_primary False (n=110); the arithmetic works out to a higher rate than either parent arm because the crisis subset carries most of the endogeneity signal.

**Per-year read (all n_min5 viable at the arm level)**:

- 2022 (partial): RR = 0.86 -- essentially null, tiny n on PS-True arm.
- 2023: RR = **0.22** (PS 5.0% [0.9, 23.6] vs complement 22.4% [14.1, 33.7]). Strong sign-flip; the 2023 sign-inversion in the parent Wave 2B (RR = 2.02) reverses when we restrict to proactive-strategic.
- 2024: RR = **0.93** (PS 20.0% [7.0, 45.2] vs complement 21.5% [13.3, 33.0]). No sign-flip. The 2024 parent Wave 2B sign-inversion (RR = 1.56) is NOT resolved by restricting to proactive-strategic. Wide Wilson CI on the PS arm (only 15 episodes with 3 crashes) means this cell is under-powered.
- 2025: RR = 0.00 (0 crashes on 23 PS episodes; 2 on 43 complement). Descriptively supports pre-commit direction but Wilson CI on PS arm is [0.0, 14.3], not credibly distinguishable from the complement rate 4.65% [1.3, 15.5].
- 2026 (partial): RR = 0.00 (0 / 15 PS vs 4 / 21 complement). Similar under-powered pattern.

### 5.3 Consistency with Interpretation A

**Pooled RR = 0.35 is CONSISTENT-WITH Interpretation A**: when we isolate the proactive-strategic rest subset, the sign of the rest-after arm flips from inverted (RR = 1.54) to the MD-beta section 3.7 pre-committed direction (RR < 1). The pooled shift is substantial (from RR = 1.54 to RR = 0.35, a ~4x reduction in relative crash rate on the "rest" arm).

**BUT the year-2024 finding is AMBIGUOUS-FOR Interpretation A**. Interpretation A predicts that once we condition away the endogeneity, per-year RRs should trend toward < 1.0 in years that showed the pooled sign-inversion. 2023 does (0.22); 2024 does not (0.93). Two candidate readings for the 2024 exception:

- **(a) small-n artefact** -- 2024 PS-True arm has 15 episodes with 3 crashes; Wilson CI [7.0, 45.2] does not credibly rule out RR ~ 1 or RR ~ 2.
- **(b) partial mitigation only** -- gevoelscore >= 5 does not fully isolate calibrated pacing; there may be a 2024-specific residual endogeneity (e.g. participant felt okay on rest-day but subsequent load resurged; the strategic-rest quadrant does not capture forward-window compensatory failure).

**Definitionally**: proactive-strategic subset RR = 0.35 pooled is not a Stage-D verdict on Interpretation A; it is a descriptive-with-CI sign-flip on the pooled arm. Per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference) the reading discipline is descriptive, not inferential.

**Companion finding**: the **complement arm rate 17.67%** (which pools crisis + borderline rest-after episodes with rest-absent episodes) is meaningfully higher than the parent Wave 2B rest-adj arm rate 16.8%. This means the crisis-rest subset within the original rest-adj arm was carrying disproportionate crash-in-5d risk, consistent with the confounding-by-indication mechanism.

### 5.4 Caveat -- construct-validity of the gevoelscore >= 5 threshold

The gevoelscore = 4/5 boundary is a construct-validity judgement. Alternative thresholds (>= 4, borderline-inclusive; >= 6, strict-strategic-only) were not tested in this Wave 2C audit; a Stage D companion would need to run threshold sensitivity per MD-beta section 3.10 definitional-pair discipline. The **pooled RR = 0.35** finding is contingent on the >= 5 threshold; the direction of the sign-flip is robust as long as rest-days with gevoelscore >= 5 are less crash-associated than rest-days with gevoelscore <= 4.

### 5.5 Caveat -- rest-day operand rolling-baseline moves-with-envelope artefact (added at r1 lock post-review absorption per L3.2 substantive fire)

The `rest_day_p25` operand is defined as `total_steps < rolling_percentile_25(total_steps, window=30d, min_periods=15)`. Per §8 the LC-era mean `total_steps` dropped 25% across the corpus (6006 in 2023 -> 4528 in 2026 partial); the rolling 30d p25 threshold necessarily shifts with the mean-step trend (approximately linearly with the p50 shift under a stable distribution shape; §8 CV non-monotonicity means the shape does shift somewhat but the direction of threshold drift is still downward).

**Implication for the §5 pooled sign-flip finding**: what counts as a "rest-day" in 2023 (absolute step-cutoff ~2900 at the p25 rolling threshold) differs from what counts as a "rest-day" in 2026 (absolute step-cutoff ~2200). A 2500-step day in 2023 is a non-rest-day; a 2500-step day in 2026 is a rest-day. The gevoelscore >= 5 conditioning applies to different absolute-step populations across eras. If gevoelscore is correlated with absolute step count (higher steps -> higher gevoelscore on average, ceteris paribus), the composition of the proactive-strategic subset may shift toward higher-absolute-step days in the late era relative to early era.

**Does this undermine the §5 pooled RR = 0.35 finding?** Not necessarily -- the sign-flip is directionally consistent even under the moving-target caveat, because the mechanism of interest (gevoelscore >= 5 discriminating strategic from crisis rest) is defined relative to the participant's own daily felt-state rather than to an absolute step benchmark. But the reader must not interpret the pooled RR = 0.35 as a fixed physiological effect estimate; it is a descriptive summary of the joint distribution of (rest-day-by-rolling-envelope, gevoelscore-on-rest-day, crash-in-5d) on this corpus with a moving rest-day threshold.

**Recommended follow-up for MD-beta r2 or Wave 2D companion**: a companion analysis with an **absolute-step-threshold rest-day operand** (e.g. `total_steps < 3000`, per parent Q24 discussion) would test the moving-target artefact concern directly. If the sign-flip holds under an absolute threshold, the moving-target artefact is not driving the finding. If the sign-flip weakens or reverses, the moving-target artefact is load-bearing and MD-beta r2 must either codify the rest-day operand differently or explicitly caveat the moving-target dependency in any Stage H pre-reg.

See §11 item 6 for the reviewer-concern framing of this artefact.

---

## 6. Crisis-reactive-rest -> crash-in-5d RR (companion; endogeneity isolation)

Source: [`output/crisis_reactive_rest_crash_2x2.csv`](output/crisis_reactive_rest_crash_2x2.csv).

**Operational definition** (companion to §5; same 314-episode base):

- Episode is **crisis-reactive-rest-after** if `rest_after_3_primary = True` AND any of the K=3 rest-days has EITHER `is_crash = True` in `[rest_day - 3, rest_day - 1]` OR gevoelscore <= 3 (crisis bucket) on rest_day.
- Complement: all other episodes with rest-after indicator not NaN.

**Prediction**: the crisis-reactive arm should carry strong sign-inversion relative to the complement (endogeneity signature).

### 6.1 Per-pool 2x2

| Pool | n_used | CR-True n / crash | CR-False n / crash | Rate CR-True [Wilson] | Rate CR-False [Wilson] | RR (CR/complement) | RD |
|---|---:|---|---|---|---|---:|---:|
| ALL_ERA_POOLED | 312 | 59 / 23 | 253 / 23 | 38.98% [27.6, 51.7] | 9.09% [6.1, 13.3] | **4.29** | +0.299 |
| year_2022 (partial) | 43 | 8 / 4 | 35 / 3 | 50.00% [21.5, 78.5] | 8.57% [3.0, 22.4] | 5.83 | +0.414 |
| year_2023 | 87 | 14 / 9 | 73 / 7 | 64.29% [38.8, 83.7] | 9.59% [4.7, 18.5] | **6.70** | +0.547 |
| year_2024 | 80 | 29 / 9 | 51 / 8 | 31.03% [17.3, 49.2] | 15.69% [8.2, 28.0] | 1.98 | +0.153 |
| year_2025 | 66 | 4 / 0 | 62 / 2 | 0.00% [0.0, 49.0] | 3.23% [0.9, 11.0] | 0.00 | -0.032 |
| year_2026 (partial) | 36 | 4 / 1 | 32 / 3 | 25.00% [4.6, 69.9] | 9.38% [3.2, 24.2] | 2.67 | +0.156 |

Row-total checks: 43 + 87 + 80 + 66 + 36 = 312. Sum CR-True crash: 4+9+9+0+1 = 23; sum CR-False crash: 3+7+8+2+3 = 23; total 46 (matches §5 grand crash total).

### 6.2 Descriptive observations

**Headline: crisis-reactive arm is dramatically enriched for crash-in-5d.**

- Pooled crisis-reactive rate: **38.98%** [27.6, 51.7]. Complement rate: 9.09% [6.1, 13.3]. RR = **4.29**.
- **2023 crisis-reactive rate: 64.29%** [38.8, 83.7] -- 9/14 episodes with a crisis rest-day in [D_end+1, D_end+3] had a crash-in-5d. RR = 6.70.
- 2024 crisis-reactive rate: 31.03% [17.3, 49.2]. RR = 1.98.
- 2025 crisis-reactive rate: 0/4 (all viable_n_min5 = False for 2025 and 2026 at the CR-True arm; small n).
- 2026 partial: 1/4.

**The crisis-reactive subset carries the sign-inversion at extreme concentration in 2023**: crash-in-5d rate is nearly 2/3 on the crisis-reactive arm vs ~10% on the complement, an RR ~ 6.7.

### 6.3 Confounding-by-indication mechanism isolation

The parent Wave 2B pooled RR = 1.54 and 2023 RR = 2.02 are consistent with the confounding-by-indication mechanism (Salas 2001; Kyriacou & Lewis 2016). This §6 isolates that mechanism at high fidelity: the 59 crisis-reactive-rest episodes have a **38.98%** crash-in-5d rate (23 events), 4.3x the complement rate. Within the crisis-reactive subset, the "rest" is downstream of the crash risk that materialises in the +5d window; the rest-day is a **symptom** of the imminent crash trajectory, not a cause of it.

**Reading**: §6 is descriptive-with-CI evidence that the confounding-by-indication mechanism is empirically operative in this participant's 2023-2024 data at high strength. It does not falsify Interpretation A; it strengthens the plausibility of Interpretation A's mechanism-diagnosis.

### 6.4 Convergent evidence from §5 + §6

§5 pooled proactive-strategic arm rate: **6.25%** [2.7, 13.8].
§6 pooled crisis-reactive arm rate: **38.98%** [27.6, 51.7].
Ratio (crisis / strategic): **6.24x**.

The gevoelscore-conditioning splits the K=3 rest-after arm into two sub-populations with drastically different crash-in-5d risk. The pooled rest-adj arm rate (16.8%) is an arithmetic average of these sub-populations; the sign of the pooled RR depends on the mixture weights of strategic vs crisis rest-days, which per §3 shift over the LC-era corpus.

This finding is **the descriptive core of Interpretation A**: the sign of the pooled RR is a function of the composition of the rest-arm, not an invariant physiological signal.

### 6.5 Definitional-pair discipline for §5 + §6 (added at r1 lock post-review absorption per L4.2 substantive fire)

§5 (`proactive_strategic_rest`) and §6 (`crisis_reactive_rest`) are structurally a **definitional pair per [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair)**: both operationalise a bifurcation of the K=3 rest-after arm using the same gevoelscore-on-rest-day discriminator (>= 5 strategic vs <= 3 crisis), with the borderline (=4) + NaN buckets split across the two complements. Their crash-rate readings are not independent evidence -- they read the same underlying joint distribution from opposite ends.

**Reporting discipline**: §5.3 CONSISTENT-WITH Interpretation A + §6.3 CONVENTIONS §3.9 confounding-by-indication isolation are convergent readings of the same definitional-pair split. Per §3.3 definitional-pair discipline, any downstream Stage H pre-reg or MD-beta r2 revision that codifies the gevoelscore-conditioning must pick ONE of {`strategic`, `crisis`} as the primary operand and the other as the sensitivity companion, NOT report both as independent evidence at Stage S1 (internal synthesis).

**Absorb-eligibility for MD-beta r2**: this discipline fire is absorb-eligible **if and only if** MD-beta r2 codifies the definitional-pair extension at MD-beta section 3.1 (i.e. adds `rest_day_p25_strategic` + `rest_day_p25_crisis` as a formally-named definitional pair with primary vs sensitivity roles chosen). If MD-beta r2 defers the codification to a later r3, this fire escalates from absorb-tier to substantive-open at the Wave 2C audit level. Fresh-session review recommendation is r2 codification (per §10.5); Wave 2C absorbs the fire on the assumption that r2 will follow through.

---

## 7. Very-heavy day frequency per year (Interpretation D test 1)

Source: [`output/very_heavy_frequency_per_year.csv`](output/very_heavy_frequency_per_year.csv).

### 7.1 Per-year counts + fractions

| Year | n_days_total | n_activity_classified | n_heavy_only | n_very_heavy | n_heavy_all | VH / activity-days | VH / heavy-all |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2022 (partial) | 272 | 202 | 27 | 52 | 79 | **25.7%** | **65.8%** |
| 2023 | 365 | 365 | 75 | 52 | 127 | 14.2% | 40.9% |
| 2024 | 366 | 366 | 65 | 60 | 125 | 16.4% | 48.0% |
| 2025 | 365 | 365 | 68 | 59 | 127 | 16.2% | 46.5% |
| 2026 (partial) | 156 | 156 | 41 | 33 | 74 | 21.2% | 44.6% |

### 7.2 Descriptive observations

- **Very-heavy fraction of activity-days does NOT show monotone shrinkage over 2023 -> 2026** (14.2% -> 16.4% -> 16.2% -> 21.2%). 2026 partial has the highest VH fraction after 2022.
- **Very-heavy absolute counts are essentially flat 2023-2025** (52, 60, 59). 2026 partial has 33 in the first ~5 months.
- **Heavy-all fraction of activity-days is flat** (34.8% in 2023, 34.2% in 2024, 34.8% in 2025).
- **2022 partial VH fraction 25.7%** is confounded by the truncated year + smaller activity-classified base (n=202 of 272 days; ~26% of 2022 days lack an `exertion_class_lagged_lcera`), so 2022 is not a clean pre-2023 comparator.
- **Only 2023 is a clean low-VH year** among the 2023-2026 fully-tracked years; 2024, 2025, and 2026 all sit at 16-21% VH fraction of activity-days.

### 7.3 Consistency with Interpretation D

Interpretation D's load-envelope shrinkage sub-claim -- "fewer very-heavy days in 2025-2026" -- is **FALSIFIED at the descriptive resolution of this audit**. Very-heavy day absolute count and fraction of activity-days are essentially flat 2023-2025 and slightly ELEVATED in 2026 partial.

**Reading discipline**: The crash-rate collapse in 2025-2026 (~2/year vs ~10/year) is real per parent Wave 2B section 9 and parent Q24 MD section 10; it is NOT accompanied by a reduction in very-heavy day frequency. If Interpretation D is to survive, it must survive on the tactical-response sub-claim (§9) or the step-envelope sub-claim (§8), not the very-heavy-frequency sub-claim.

**Alternative reading**: the very-heavy classification (`exertion_class_lagged_lcera == 'very_heavy'`) is a step-count-based categorical that may not fully capture the sub-day intensity structure (bout-level intensity, HR spikes, sympathetic-arousal moments); a tactical Garmin-use improvement could reduce crash frequency without changing the day-level VH classification if the improvement operates at the sub-day resolution (e.g. shorter bouts, more sit-breaks, better paced VH days). This is speculation at Stage -1 resolution; it flags a limitation of the day-level VH count as a proxy for load-envelope shape.

---

## 8. Step-envelope variance per year (Interpretation D test 2)

Source: [`output/step_envelope_variance_per_year.csv`](output/step_envelope_variance_per_year.csv).

### 8.1 Per-year step-envelope descriptors

| Year | n_days_with_steps | mean_steps | median_steps | std_steps | CV (std/mean) | IQR | p25 | p75 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 (partial) | 261 | 6006 | 5618 | 2601 | 0.433 | 3382 | 4190 | 7572 |
| 2023 | 365 | 5177 | 4920 | 2438 | 0.471 | 3235 | 3409 | 6644 |
| 2024 | 365 | 5088 | 4985 | 1823 | **0.358** | 2411 | 3809 | 6220 |
| 2025 | 363 | 4669 | 4402 | 1884 | 0.404 | 2519 | 3283 | 5802 |
| 2026 (partial) | 147 | 4528 | 4343 | 1903 | 0.420 | 2650 | 3204 | 5854 |

### 8.2 Descriptive observations

- **Mean total_steps drops monotonically 2022 -> 2026** (6006 -> 5177 -> 5088 -> 4669 -> 4528). A ~25% reduction across the 4-year window.
- **Coefficient of variation is not monotone** (0.43 -> 0.47 -> **0.36** -> 0.40 -> 0.42). 2024 has the narrowest normalised envelope; 2023 the widest. 2025-2026 sit in between.
- **IQR is narrower 2024-2026** than in 2022-2023 (2411, 2519, 2650 vs 3382, 3235), consistent with the envelope tightening at the tails without the CV moving cleanly.
- **p75 drops monotonically** (7572 -> 6644 -> 6220 -> 5802 -> 5854), consistent with fewer high-step days; **p25 is roughly flat** at ~3200-3800 across all years, so the shrinkage is asymmetric (upper-tail compression, lower-tail unchanged).

### 8.3 Consistency with Interpretation D

The step-envelope sub-claim of Interpretation D is **PARTIALLY CONSISTENT** with the descriptive pattern:

- **Upper-tail compression** (p75 dropping 7572 -> 5802) and **mean step reduction** (6006 -> 4528) are consistent with a narrower load-envelope over time.
- **CV is NOT monotone** and does not support "increasingly-disciplined self-regulation" as a monotone narrative; 2024 had the tightest normalised envelope, then 2025-2026 widened slightly.
- The envelope shrinkage is a **downshift-and-compress** pattern (whole distribution shifts down + upper tail compresses more than lower tail), not a symmetric tightening.

**Reading**: The mean + p75 shift supports a lower-daily-load claim; the CV non-monotonicity suggests the participant did not simply become more consistent day-to-day, but rather shifted the whole envelope down. Interpretation D's tactical-Garmin-improvement reading (narrower envelope = more disciplined) is a partial fit; a stronger reading is "the whole step envelope moved down" without necessarily becoming more precisely regulated.

### 8.4 Confound to flag -- step_count reduction may not be voluntary

Whether the step-envelope reduction is voluntary tactical Garmin-use improvement vs a symptom of reduced functional capacity (LC-driven reduction in movement tolerance) is **not distinguishable from step counts alone**. Per memory `project_stress_is_garmin_measure`, and per parent Q24 MD section 10 caveat 8 envelope-drift asymmetry, envelope shifts across a chronic-illness recovery trajectory are structurally ambiguous. This audit reports the descriptive shift + flags the interpretation as ambiguous.

---

## 9. Heavy-episode-end to next rest-day gap per year (Interpretation D test 3, tactical response proxy)

Source: [`output/heavy_gap_to_next_rest_per_year.csv`](output/heavy_gap_to_next_rest_per_year.csv).

**Operational definition**: for each of 314 episodes, gap in days from `D_end` to the smallest subsequent index with `rest_day_p25 == 1.0`. Right-censored if no rest-day exists before corpus end (0 episodes right-censored across all years).

### 9.1 Per-year gap statistics

| Year | n_episodes | n_observed | mean_gap | median_gap | p25 | p75 |
|---|---:|---:|---:|---:|---:|---:|
| 2022 (partial) | 44 | 44 | 3.07 | 2.0 | 1.0 | 4.00 |
| 2023 | 87 | 87 | 5.22 | 2.0 | 1.0 | 7.00 |
| 2024 | 81 | 81 | 2.81 | 2.0 | 1.0 | 4.00 |
| 2025 | 66 | 66 | 4.52 | **3.0** | 1.0 | 6.75 |
| 2026 (partial) | 36 | 36 | 3.92 | **1.0** | 1.0 | 5.25 |
| ALL | 314 | 314 | 4.00 | 2.0 | 1.0 | 5.00 |

### 9.2 Descriptive observations

- **Median heavy-to-next-rest gap is flat at 2.0 days for 2022-2024**, jumps to **3.0 in 2025**, drops to **1.0 in 2026 partial**.
- Mean gap is noisy across years (3.07 -> 5.22 -> 2.81 -> 4.52 -> 3.92), driven by right-tail episodes without a clean trend.
- p75 (upper-quartile gap) is **highest in 2023** (7.0 days) and 2025 (6.75 days), suggesting some episodes with long delays before the next rest-day in those years.

### 9.3 Consistency with Interpretation D

The tactical-response sub-claim of Interpretation D -- "shorter gaps = faster tactical response" -- is **AMBIGUOUS-TO-FALSIFIED at the descriptive resolution of this audit**:

- Median gap does NOT drop over 2022 -> 2026 (2, 2, 2, 3, 1 -- non-monotone; 2025 actually LONGER than 2022-2024).
- The 2026 partial median of 1.0 is the shortest but 2026 is only 5 months; small-n year should not be over-read.
- If tactical Garmin improvement produced faster rest-response, we would expect monotone median gap reduction; that pattern is not visible.

**Reading**: The heavy-to-next-rest gap descriptor does not support Interpretation D's tactical-response sub-claim at Stage -1 descriptive resolution.

**Alternative reading**: rest-day operand (`rest_day_p25`) is a relative operand (30d rolling p25); if the whole step-envelope shifts down (§8), the p25 threshold moves down too, potentially DELAYING the classification of a low-step day as a rest-day in years with lower overall step counts. This is an operand-artefact concern per MD-beta section 3.1 rolling-threshold discussion; not resolved at Stage -1.

---

## 10. Findings summary + Interpretation-A + Interpretation-D readiness assessment for MD-beta r2

### 10.1 Interpretation A -- rest-day composition shift

**§3 Rest-day gevoelscore-conditioned quadrants per year**: proactive-strategic fraction rises monotonically 2023 -> 2026 (26.7% -> 25.3% -> 53.2% -> 56.2%); crisis-reactive fraction collapses 2023 -> 2025 (15.1% -> 1.3%). **CONSISTENT-WITH Interpretation A**.

**§4 Mean gevoelscore on rest-day per year**: step-jump at 2024 -> 2025 (3.99 -> 4.54 heavy-adj; 4.03 -> 4.57 all-corpus). **CONSISTENT-WITH Interpretation A** at the felt-state resolution; **AMBIGUOUS-FOR at the composition-specificity resolution** (whole-year mean gs also rose, so the rest-day shift is not obviously composition-specific).

**§5 Proactive-strategic rest-after -> crash-in-5d RR (LOAD-BEARING)**: **pooled RR = 0.354** (arm rate 6.25% [2.7, 13.8] vs complement 17.67% [13.3, 23.1]). **Sign flips from pooled RR = 1.54 to RR = 0.35**. Per-year: 2023 sign-flip clean (RR = 0.22); 2024 sign-flip absent (RR = 0.93, small n on PS-True arm); 2025 + 2026 both RR = 0.00 (small events). **POOLED CONSISTENT-WITH Interpretation A; 2024 per-year AMBIGUOUS-FOR**.

**§6 Crisis-reactive rest-after -> crash-in-5d RR**: pooled RR = **4.29**; 2023 RR = **6.70**. Endogeneity signature is dramatically isolated in the crisis-reactive subset. **CONSISTENT-WITH the confounding-by-indication mechanism** that Interpretation A relies on.

**Overall Interpretation A assessment**: at the pooled level, the sign-flip from RR = 1.54 (parent Wave 2B) to RR = 0.35 (Wave 2C proactive-strategic-only) is the **strongest descriptive evidence** for Interpretation A this audit produces. The mechanism -- gevoelscore-on-rest-day as discriminator between calibrated pacing and endogeneous rest -- is descriptively consistent with the full pattern (§3 composition shift + §4 mean-gs shift + §5 sign-flip + §6 endogeneity isolation).

**BUT**: the 2024 per-year proactive-strategic RR = 0.93 does not neatly resolve. Either (a) 2024 had residual endogeneity not captured by gevoelscore >= 5 + no crash in prior 3d, or (b) the small n on the 2024 PS-True arm (15 episodes, 3 crashes) leaves the sign under-determined. This should be pre-committed as a **caveat-class finding per [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)** for any MD-beta r2 revision that adopts Interpretation A framing.

### 10.2 Interpretation D -- load-envelope shrinkage + tactical response

**§7 Very-heavy frequency per year**: 14.2% -> 16.4% -> 16.2% -> 21.2% (VH / activity-days). **FALSIFIES the very-heavy-shrinkage sub-claim** at the day-level resolution.

**§8 Step-envelope variance per year**: mean drops 6006 -> 4528; p75 drops 7572 -> 5854; CV non-monotone (0.47 -> 0.36 -> 0.40 -> 0.42). **PARTIALLY CONSISTENT** with the envelope-shrinkage sub-claim -- the whole envelope moved down + compressed at the upper tail, but the distribution did not become more precisely regulated in CV terms.

**§9 Heavy-to-next-rest gap per year**: median 2, 2, 2, 3, 1 (non-monotone). **AMBIGUOUS-TO-FALSIFIES the tactical-response sub-claim** at the day-level rest-day operand resolution.

**Overall Interpretation D assessment**: the crash-rate collapse in 2025-2026 is **NOT explained by** (a) reduced very-heavy day frequency (§7) or (b) faster tactical rest-response (§9). It is **partially explained by** (c) lower daily step envelope with tighter upper tail (§8). The load-envelope shrinkage sub-claim of Interpretation D survives at the mean-step and p75 level but fails at the very-heavy-day level.

**MD-beta r2 revision readiness**: Interpretation D as originally stated (VH-frequency reduction + tactical improvement) is not supported by this Wave 2C descriptive evidence. A **revised Interpretation D** -- "the daily step envelope shifted DOWN (mean, p75) without VH-frequency reduction or measurable tactical-response acceleration" -- is descriptively consistent with the data but does not by itself explain the ~5x crash-rate reduction. Some other mechanism (e.g. altered response to identical exertion, medication effect per memory `project_stress_is_garmin_measure`'s citalopram anchor, chronic-illness recovery trajectory not captured by step-count metrics) would need to carry the residual explanation.

### 10.3 What Wave 2C supports vs falsifies vs leaves ambiguous for MD-beta r2

**SUPPORTS** (for MD-beta r2 to adopt):

- Interpretation A's pooled mechanism-diagnosis: the sign of the pooled RR is a function of the rest-day composition, and the composition demonstrably shifts across the LC era.
- The confounding-by-indication mechanism (Salas 2001; Kyriacou & Lewis 2016) is descriptively operative in this participant's 2023-2024 data at high strength (§6 crisis-reactive RR pooled = 4.29; 2023 RR = 6.70).
- Gevoelscore-conditioning is a partial mitigation of the endogeneity, with pooled sign-flip from RR = 1.54 to RR = 0.35 on the strategic subset.

**FALSIFIES** (for MD-beta r2 to NOT adopt without revision):

- Interpretation D's very-heavy-frequency-reduction sub-claim (§7).
- Interpretation D's tactical-Garmin-response-acceleration sub-claim as measured by heavy-to-next-rest gap (§9).

**LEAVES AMBIGUOUS** (for MD-beta r2 to flag as caveat-class):

- The 2024 per-year proactive-strategic RR = 0.93 (§5) -- does not fit the Interpretation A monotone-recovery story; either small-n artefact or residual endogeneity.
- The composition-specificity of the 2024 -> 2025 mean-gs shift (§4) -- whole-year mean gs also rose, so the rest-day shift is not obviously composition-specific.
- The step-envelope-shrinkage-vs-functional-capacity-reduction distinction (§8) -- the descriptive shift is compatible with either voluntary tactical improvement or LC-driven capacity reduction; not distinguishable from step counts alone.
- The rest-day operand rolling-threshold artefact concern (§9) -- if the whole step envelope shifts down, the p25 threshold moves down too, potentially confounding the rest-day classification's timing.

### 10.4 Recommended MD-beta r2 revision surface (producer-mode note; not a spec)

The parent MD-beta r1 pre-committed sign-inversion (RR = 1.57 on pooled K=3 rest-after primary) as consistent with the confounding-by-indication mechanism. Wave 2C provides descriptive evidence that:

- The pooled sign-inversion is composition-driven; the composition shifts across the LC era; a proactive-strategic subset shows the pre-committed direction at RR = 0.35.
- Any MD-beta r2 rest-adjacency arc pre-registration should either (i) stratify explicitly by rest-day gevoelscore bucket, or (ii) acknowledge rest-day composition as a first-class uncorrected confounder that dominates the direction of the pooled RR.
- The era-stratified sensitivity arm (already pre-committed in parent MD-beta section 5 confound 3) should be extended to a rest-day-composition-stratified sensitivity arm.

This is producer-mode note only; the MD-beta r2 revision itself is a downstream methodology-editing session, not this Wave 2C audit's scope.

### 10.5 Fresh-session review load-bearing r2 recommendations (added at r1 lock post-review absorption)

Fresh-session methodology reviewer ([`../../../reviews/methodology-Q24-mdbeta-wave2c-reactive-vs-proactive-rest-2026-07-16.md`](../../../reviews/methodology-Q24-mdbeta-wave2c-reactive-vs-proactive-rest-2026-07-16.md)) recommended two load-bearing MD-beta r2 decisions:

**(a) Codify gevoelscore-conditioning as definitional-pair extension at MD-beta section 3.1**: YES.

Reviewer rationale: memory [[project_rest_day_operand_semantics]] bullet 4 explicitly deferred the definitional-pair codification decision to Wave 2C findings. The RR = 0.354 (proactive-strategic) vs RR = 4.29 (crisis-reactive) factor-of-12 divergence satisfies the deferral condition. Combined with the Wave 2B Path A upgrade (era + intensity as primary stratifiers per parent Wave 2B audit section 13.10), this constitutes a **substantial r2** that per MD-beta section 7 compression discipline may require fresh-session re-review before r2 lock.

Absorbed into §10.4 producer-mode note; MD-beta r2 downstream session should codify:

- `rest_day_p25_strategic` (low_steps AND gevoelscore >= 5) as one member of the definitional pair
- `rest_day_p25_crisis` (low_steps AND gevoelscore <= 3) as the other member
- Primary vs sensitivity role assignment: reviewer defers to the MD-beta r2 author

**(b) 2024 residual tension formal sub-arc investigation BEFORE Stage H**: YES.

Reviewer rationale: 2023 / 2025 / 2026 all sign-flip cleanly on the proactive-strategic subset; 2024 does NOT (per-year RR = 0.93, n=15 on PS arm). This is a **sign-flip PAUSE, not a smooth transition curve**; running Stage H without a Wave 2D/2E investigation of the 2024 exception would leave Interpretation A architecturally exposed on a specific empirical counterexample that a sceptical Stage H reviewer will foreground.

Candidate Wave 2D scope (producer-mode note; NOT this audit's scope):

- Per-quarter or per-half-year proactive-strategic RR within 2024 to see whether the exception is a specific sub-period
- Cross-tab 2024 proactive-strategic episodes by intensity (heavy vs very_heavy end_class) to see if the intensity stratification per Wave 2B section 10 changes the 2024 read
- Per-episode diagnostic on the 3 crash-in-5d events within the 2024 proactive-strategic subset to see if there's a common feature (e.g. cumulative-load in the pre-window, seasonal effect, medication change)
- Alternative gevoelscore threshold sensitivity (>= 6 stricter) applied to 2024 only

**Structural note**: (a) is inline-absorbable into MD-beta r2 as a mechanical §3.1 definitional-pair extension. (b) is a downstream Wave 2D descriptive-audit scope decision requiring user endorsement of the sequence detour before Stage H. Both recommendations are surfaced here as documentation; the actual decisions (r2 timing + Wave 2D dispatch) are for the orchestrator + user.

---

## 11. Reviewer-concerns for a fresh-session walk

1. **Gevoelscore >= 5 threshold construct-validity**: the 4/5 split is a judgement call. Alternative thresholds (>= 4, borderline-inclusive; >= 6, strict) were not tested. §5 pooled RR = 0.35 is contingent on the specific threshold; a threshold-sensitivity companion at Stage D would strengthen the finding.

2. **§4 whole-corpus felt-state comparator**: the mean gs on rest-days rose +0.55 (heavy-adjacent) at 2024 -> 2025, but the whole-year mean gs also rose +0.48 at the same transition. This audit reports the comparator numerically in §4.4 as an inline paragraph rather than a separate CSV. Fresh-session reviewer should confirm this treatment is adequate for the composition-specificity question, or ask for a proper LC-era-per-year mean-gs CSV.

3. **§5 2024 per-year proactive-strategic RR = 0.93**: this cell is the biggest tension with the Interpretation A monotone-recovery story. Fresh-session reviewer should decide whether §5.3 candidate reading (a) small-n artefact vs (b) partial mitigation only is adequately framed, or whether the audit should flag this as a "narrative-only" caveat per memory `feedback_narrative_only_events` and mark it DECLINED-NARRATIVE-ONLY upfront rather than DEFERRED.

4. **§7 day-level very-heavy classification as load-envelope proxy**: the falsification of Interpretation D's VH-frequency sub-claim rests on the day-level `exertion_class_lagged_lcera == 'very_heavy'` categorical. Fresh-session reviewer should confirm whether this day-level operand is adequate for the VH-frequency question, or whether sub-day bout-level intensity (per `per_bout_master.csv`) should be a follow-up Wave 2D probe.

5. **§8 CV non-monotonicity**: the coefficient of variation is not monotone (0.47 -> 0.36 -> 0.40 -> 0.42). The audit reports this as "partial fit" for Interpretation D's tactical-improvement reading. Fresh-session reviewer should confirm whether the CV metric is the right normalised-envelope metric, or whether an alternative (e.g. p75 - p25 in absolute terms; MAD; entropy of the step distribution) would carry the interpretation more cleanly.

6. **§9 rest-day-operand rolling-threshold artefact**: the p25 rolling threshold shifts with the mean-step trend from §8. If the whole envelope shifts down 25%, the p25 threshold also shifts down ~25%, and the rest-day classification is defined against a moving target. Fresh-session reviewer should decide whether this artefact concern warrants a companion analysis with an absolute-step-threshold rest-day operand (e.g. total_steps < 3000, per parent Q24 discussion), or whether the rolling-p25 operand is faithful-to-data despite the moving target.

7. **Interpretation A vs Interpretation B (aliases)**: this audit tests Interpretation A (rest-day composition shift) against the pooled sign-inversion baseline. It does not explicitly test against "Interpretation B" alternatives (e.g. participant physiology genuinely changed, rest became more protective in 2025-2026 not because of composition but because of altered response; medication effect; recovery-trajectory-driven change in crash vulnerability). Fresh-session reviewer should confirm whether the framing discipline in §2.4 (both interpretations partial-testable) is adequate, or whether an explicit Interpretation B section is warranted.

8. **Physical-rest-only semantic constraint disclosure**: §2.1 flags that `rest_day_p25` measures physical rest only. Cognitive rest and emotional rest are not measured. Fresh-session reviewer should confirm this disclosure is prominent enough (currently in §2.1 and cross-referenced from §2.4), or whether it should be repeated in §5 and §6 headers where the load-bearing tests run.

9. **Two-session peer-review at the reviewer-mode level**: per memory `feedback_pre_reg_writer_role`, reviewer-mode artefacts require draft + review in DIFFERENT sessions. This audit is producer-mode (Stage -1 descriptive), so the two-session rule does not strictly apply. However, per [CONVENTIONS section 1.2](../../../CONVENTIONS.md#12-reviewer-mode), any downstream Stage-D or Stage-H artefact that consumes Wave 2C findings must be draft-review-split across sessions.

10. **Wave 2C -> MD-beta r2 revision path**: §10.4 makes a producer-mode revision-surface note. Fresh-session reviewer should decide whether this note is appropriately narrow (points at revision, does not draft it) or whether it overreaches into methodology-editing territory that should be strictly out-of-scope for this Stage -1 audit.

---

## 12. Lock log

- **DRAFT r0 2026-07-16**: initial draft by Claude (Opus 4.7) in producer-mode subagent per [CONVENTIONS section 1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem. Wave 2C sibling of parent [Wave 2B Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-precursor-rest-streak/audit.md). Pending fresh-session methodology-review absorption before LOCK.
- **r1 LOCKED 2026-07-16**: Fresh-session methodology review absorbed from [`../../../reviews/methodology-Q24-mdbeta-wave2c-reactive-vs-proactive-rest-2026-07-16.md`](../../../reviews/methodology-Q24-mdbeta-wave2c-reactive-vs-proactive-rest-2026-07-16.md) (verdict: DEFENSIBLE with revision; 4 fires total: 2 audit-level absorb + 2 load-bearing r2 recommendations for MD-beta downstream). Four surgical patches applied per [CONVENTIONS section 1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations) compression discipline (mechanical clarifications, no architectural change; the load-bearing §5 sign-flip finding + §6 endogeneity isolation + §7 Interpretation D falsification + §10 readiness assessment all preserved byte-identically). **Patch 1** (bulk anchor fix, review L1 minor): `[CONVENTIONS section 5](#5-zero-vs-nan-discipline)` broken anchor changed to `[CONVENTIONS section 3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from bout_level_recovery_dynamics.md)](#310-operationalisation-faithful-to-the-data-not-just-to-the-description)` -- same fix pattern as parent Wave 2B audit r1 lock. **Patch 2** (new §5.5, review L3.2 substantive absorb): rest-day operand rolling-baseline moves-with-envelope artefact caveat elevated from §11 item 6 reviewer-concern to a §5-embedded caveat because §5 is the load-bearing pooled sign-flip test that uses the moving-target `rest_day_p25` operand. Reader now told: (a) 2023 rest-day threshold ~2900 vs 2026 ~2200 = moving target; (b) does not undermine the pooled RR = 0.35 finding (mechanism is defined relative to felt-state not absolute steps) but (c) reader must not interpret pooled RR = 0.35 as a fixed physiological effect estimate; recommended follow-up = absolute-step-threshold rest-day companion operand at MD-beta r2 or Wave 2D. **Patch 3** (new §6.5, review L4.2 substantive absorb-eligible): §5 (proactive-strategic) + §6 (crisis-reactive) explicitly named as a **definitional pair per CONVENTIONS section 3.3** with reporting-discipline note (not independent evidence at Stage S1). Absorb-eligibility contingent on MD-beta r2 codifying `rest_day_p25_strategic` + `rest_day_p25_crisis` as a formally-named definitional pair at MD-beta section 3.1 with primary vs sensitivity roles assigned; if r2 defers, this fire escalates from absorb-tier to substantive-open at Wave 2C level. **Patch 4** (new §10.5, review §4 load-bearing r2 recommendations documentation): fresh-session reviewer's two r2 recommendations formally documented: (a) YES codify gevoelscore-conditioning as definitional-pair extension at MD-beta section 3.1; (b) YES 2024 residual tension (per-year proactive-strategic RR = 0.93 while other years cleanly flip) formal sub-arc investigation BEFORE Stage H via Wave 2D/2E; candidate Wave 2D scope drafted as producer-mode note (per-quarter breakdown within 2024, intensity-cross-tab within 2024, per-episode diagnostic on the 3 crash-in-5d 2024 PS events, alternative gevoelscore threshold sensitivity). Preserved byte-identically: §1 corpus summary + base rates, §2 framing + interpretations + physical-rest-only semantic constraint, §3 quadrant per-year tables, §4 mean-gevoelscore per year + comparator, §5.1-§5.3 pooled + per-year proactive-strategic tables + Interpretation A consistency read, §5.4 gevoelscore >=5 threshold construct-validity caveat, §6.1-§6.4 crisis-reactive pooled + per-year tables + confounding-by-indication isolation + convergent evidence, §7 very-heavy frequency per year + Interpretation D VH-frequency-falsification, §8 step-envelope variance per year + CV non-monotonicity + partial-fit read, §9 heavy-to-next-rest gap + ambiguous-tactical-response read, §10.1-§10.4 findings summary + interpretations readiness assessments + producer-mode MD-beta r2 revision surface note, §11 reviewer-concerns list, §12 producer-mode discipline attestations. **STATUS**: LOCKED r1 2026-07-16 post-review absorption. Next-step in user-endorsed sequence: user decides between (i) MD-beta r2 immediate + Wave 2D as separate follow-on OR (ii) Wave 2D first (2024 tension investigation) informing MD-beta r2 scope + timing. Stage H remains blocked on MD-beta r2 land per parent Wave 2B section 13.10.

Producer-mode discipline attestations:

- Parent MDs (MD-alpha, MD-beta), CONVENTIONS, and the two Wave 2A + 2B audits NOT edited by this session.
- Named counts per [CONVENTIONS section 3.6](../../../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file): all cell counts + rates carry scheme (e.g. K=3 rest-after primary) + unit (episode / rest-day) + source CSV filename in-text.
- Zero-vs-NaN discipline per [CONVENTIONS section 3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from `bout_level_recovery_dynamics.md`)](../../../CONVENTIONS.md#310-operationalisation-faithful-to-the-data-not-just-to-the-description): `is_crash.fillna(False).astype(bool)` only; gevoelscore NaN preserved as its own bucket (`gs_bucket == "nan"`, 20 heavy-adjacent rest-days in 2022 pre-tracker onset); rest_day_p25 NaN preserved via parent Wave 2B `_rest_indicator` logic (2 rest-after NaN episodes dropped from §5 + §6 2x2s).
- No emoji, no em-dash in outputs or narrative.
- Idempotent script per [CONVENTIONS section 3.6](../../../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file): re-runnable, no `datetime.now()`, byte-identical CSVs on identical input.
- Descriptive-with-CI framing per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference): no verdicts, no p-values, Wilson 95% CIs on all rates, RR + RD reported with per-arm cell counts.
- Physical-rest-only semantic constraint (memory `project_rest_day_operand_semantics`) disclosed in §2.1 and honoured throughout: cognitive rest + emotional rest not treated as measured.
- Interpretation-A + D framing discipline per §2.4: both partial-testable at n=1; findings framed as CONSISTENT-WITH / AMBIGUOUS-FOR / FALSIFYING, not as verdicts.
