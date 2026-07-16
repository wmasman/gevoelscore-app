# Descriptive audit -- Q24 MD-beta precursor: rest-adjacency + streak-length structure with binary crash-in-5d outcome

*Producer-mode Stage -1 descriptive audit per [CONVENTIONS section 1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafted 2026-07-16 by Claude (Opus 4.7) in producer-mode subagent under user delegation. Authorising user: Willem.*

**Status**: **LOCKED r1 2026-07-16** post-review absorption per [`../../../reviews/methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md`](../../../reviews/methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md) (verdict: DEFENSIBLE with revision; 2 absorb-tier fires on this audit + 2 escalate-tier fires on MD-beta that this audit surfaces but does not itself resolve -- see §13.10). Extension of the parent [Q24 Stage -1 audit](../Q24-precursor-heavy-day-structure/audit.md) LOCKED r1; adds MD-beta-specific descriptive layer for the rest-adjacency + streak-length predictive-categorical operands. This audit reproduces + verifies [MD-beta section 6](../../../methodology/heavy_day_crash_risk_prediction.md#6-data-availability-audit-hooks) drafted-time probes and extends section 6.6 (K=3 primary rest-after only) to a full 12-cell grid across K x direction x operand, with era-stratified and intensity-stratified 3-way companions.

**Frame**: LC-era stratum (`lc_phase == 'lc'`), n=1524 days (2022-04-04 -> 2026-06-05), matches parent Q24 Stage -1 audit stratum. `is_crash` day-count = 103 (crash_v2 day-level, `labels_crash_v2.csv` via `build_unified_dataset.py`; propagated to `per_day_master.csv` as boolean `is_crash` per [CONVENTIONS section 3.6](../../../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file) named-count discipline).

**Heavy-day definition**: `exertion_class_lagged_lcera in {heavy, very_heavy}` (inherited verbatim from parent Q24 Stage -1 audit + MD-beta section 2).

**Unit of analysis**: episode-end (gap=0 contiguous heavy-day run; last day of the run). n=314 episodes on LC-era (matches parent Stage -1 section 4 exactly).

**Reproducibility**: [`scripts/audit.py`](scripts/audit.py) + outputs in [`output/`](output/); idempotent re-run against `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. `RANDOM_SEED = 20260716` per MD-beta section 3.6; not exercised in this Stage -1 audit (no randomisation needed; bootstrap null + Fisher exact + Cochran-Armitage trend test are Stage D concerns).

**Discipline scope**: Stage -1 descriptive audit only. NO inferential-verdict framing. All contingency tables reported as descriptive-with-Wilson-CI per MD-beta section 3.6 + [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

**Sign-inversion framing**: MD-beta section 6.6 exploratory probe surfaced RR = 1.57 (rest-after K=3 primary) + RR = 1.86 (rest-before K=3 primary) -- both directions **sign-inverted** relative to the section 3.7 pre-committed direction (rest-adjacent -> LOWER crash rate). MD-beta section 6.8 anticipates the sign-inversion as consistent with the confounding-by-indication mechanism in MD-beta section 3.9 confound 1 (rest-because-felt-bad enriches the rest-adjacent arm with crash-prone episodes; Salas 2001; Kyriacou & Lewis 2016 *JAMA*). This audit reports the extended 12-cell grid + era-stratified + intensity-stratified 3-way as **descriptive-with-CI framing under anticipated sign-inversion, not as a verdict on either direction**. Interpretation stays predictive-associational per MD-beta section 1.3.

**Cross-refs**:

- [MD-beta LOCKED r1 2026-07-16](../../../methodology/heavy_day_crash_risk_prediction.md) -- operand + machinery lock.
- [Parent Q24 MD LOCKED r1 2026-07-15](../../../methodology/post_heavy_day_compensatory_rest.md) -- stratum + heavy-day definition + unit-of-analysis inheritance.
- [Parent Q24 Stage -1 audit LOCKED r1 2026-07-15](../Q24-precursor-heavy-day-structure/audit.md) -- episode structure + overlap density.
- [Parent Q24 Stage D audit LOCKED r4](../Q24-post-heavy-trajectory/descriptive_audit.md) -- compensatory-failure sub-arm sample sizes; crash-in-window base rate anchor.
- [CONVENTIONS sections 1.2, 2.1, 3.1, 3.3, 3.6, 3.7, 4.2, 5](../../../CONVENTIONS.md).

---

## 1. Corpus summary (points to parent Stage -1; MD-beta-specific numbers)

Corpus counts inherited from parent Q24 Stage -1 audit [`corpus_summary.csv`](../Q24-precursor-heavy-day-structure/output/corpus_summary.csv) and MD-beta section 2 inheritance table:

| Measure | Value | Source |
|---|---|---|
| LC-era rows | 1524 days (2022-04-04 -> 2026-06-05, ~4.2 years) | [parent Stage -1 section 1](../Q24-precursor-heavy-day-structure/audit.md#1-corpus-summary) |
| Heavy days (heavy + very_heavy) | 532 (34.9% of LC-era) | ibid |
| Very-heavy days | 256 (16.8%) | ibid |
| Heavy-only days | 276 (18.1%) | ibid |
| Crash days | 103 (crash_v2, day-level, `labels_crash_v2.csv`) | ibid |
| `exertion_class_lagged_lcera` missingness | 70 days (4.6%) | ibid |
| gap=0 heavy episodes | 314 (matches parent Stage -1 section 4) | ibid |
| MD-beta primary outcome | `crash_in_5d(D_end) = any(is_crash[d] for d in [D_end+1, D_end+5])` where D_end is episode-end | MD-beta section 3.4 |
| Base rate on 314-episode pool | 46 / 314 = 14.6% (crash_v2 episode-end crash-in-5d) | this audit section 8 + MD-beta section 6.7 |
| Base rate on strict-clean +5d subset | 9 / 52 = 17.3% (crash_v2 episode-end crash-in-5d) | parent Stage D r4 section 3 + MD-beta section 3.4 |
| Corpus baseline LC-era crash rate | 103 / 1524 = 6.8% (crash_v2, day-level) | parent Stage -1 section 1 |

MD-beta-specific numbers this audit newly emits (not in parent Stage -1):

- Rest-day operand distributions on LC-era corpus (section 2 below).
- Streak-length x intensity + streak-length x era cross-tabs at episode-end level (sections 4 + 5 below).
- Rest-adjacency prevalence at K in {1, 2, 3} x direction in {before, after} x operand in {primary, sensitivity} = 12-cell grid (section 6 below).
- Full 12-cell rest-adjacency x crash-in-5d 2x2 grid with Wilson CIs and RR/RD (section 7 below; MD-beta section 6.6 only reports K=3 primary rest-after + rest-before).
- Streak-length x crash-in-5d table on both all-episodes and strict-clean pools (section 8).
- Era-stratified 3-way rest-adjacency x crash cross-tab (section 9).
- Intensity-stratified 3-way rest-adjacency x crash cross-tab (section 10).
- Overlap-policy sensitivity 2x2 (strict-clean subset only, K=3 primary rest-after, section 11).
- Era-stratified streak-length x crash-in-5d cross-tab (section 12).

---

## 2. Rest-day operand distributions (reproduces + verifies MD-beta section 6.1)

Source: [`output/rest_day_distribution.csv`](output/rest_day_distribution.csv).

| Rest-day operand | Definition | LC-era `n_true` | LC-era `n_nan` | Rate over total (n=1524) | Rate over non-NaN |
|---|---|---:|---:|---:|---:|
| Primary (`rest_day_p25`) | `total_steps < 30d rolling p25` (min_periods=15) | **404** | 37 | **26.5%** | 27.2% |
| Sensitivity (`rest_day_class`) | `exertion_class_lagged_lcera in {none, light}` | **724** | 70 | **47.5%** | 49.8% |

**Verification vs MD-beta section 6.1**: 404 / 26.5% + 724 / 47.5% MATCH byte-for-byte.

Full `exertion_class_lagged_lcera` breakdown (LC-era n=1524):

| Class | n | rate |
|---|---:|---:|
| none | 372 | 24.4% |
| light | 352 | 23.1% |
| moderate | 198 | 13.0% |
| heavy | 276 | 18.1% |
| very_heavy | 256 | 16.8% |
| NaN | 70 | 4.6% |

**Verification vs MD-beta section 6.1**: all six class counts + rates MATCH byte-for-byte.

**NaN discipline note per [CONVENTIONS section 3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from `bout_level_recovery_dynamics.md`)](../../../CONVENTIONS.md#310-operationalisation-faithful-to-the-data-not-just-to-the-description)**: `rest_day_p25` returns NaN when `total_steps` is missing (Garmin non-collection days) OR when the 30-day rolling window has fewer than 15 valid readings; 37 NaN cases on LC-era. `rest_day_class` returns NaN when `exertion_class_lagged_lcera` is NaN; 70 NaN cases on LC-era (matches the 70 class-NaN count above; structural). This audit's rest-day operand is emitted as `{True, False, NaN}` NOT coerced to boolean.

**Definitional-pair discipline per [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair)**: the primary + sensitivity operands are a definitional pair per MD-beta section 3.1 (both operationalise "low-activity day" from different axes). Rate divergence 26.5% vs 47.5% identifies the sensitivity operand as coarser -- the sensitivity operand fires when steps are low OR when the composite heavy-day classifier fires below-moderate; the primary operand fires only when steps are in the personal bottom quartile. Both are reported below in the 12-cell grid; per definitional-pair discipline they must NOT be reported as independent evidence when they agree.

---

## 3. Streak-length distribution (reproduces + verifies MD-beta section 6.2)

Source: [`output/streak_length_distribution.csv`](output/streak_length_distribution.csv).

`gap=0` contiguous heavy-episode counts on LC-era, n=314 episodes total:

| L_bin | n | rate |
|---|---:|---:|
| 1 | 188 | 59.9% |
| 2 | 77 | 24.5% |
| 3 | 27 | 8.6% |
| 4+ | 22 | 7.0% |

**Verification vs MD-beta section 6.2**: 188 / 77 / 27 / 22 MATCH byte-for-byte + rates match.

Sub-bins within 4+ (context, not for primary bins):

| L | n |
|---:|---:|
| 4 | 12 |
| 5 | 6 |
| 6 | 1 |
| 7 | 1 |
| 8 | 1 |
| 10 | 1 |

**Verification vs MD-beta section 6.2 + parent Stage -1 section 4**: MATCH byte-for-byte.

**Interpretive discipline**: as MD-beta section 4.6 acknowledges, per-sub-bin analysis at L in {6, 7, 8, 10} has n=1 each and is narrative-only. The merged 4+ bin (n=22) preserves ordinal ranking without over-claiming resolution. The 4-bin ordinal ladder {1, 2, 3, 4+} is the primary bin scheme for MD-beta section 4.3.

---

## 4. Streak-length x intensity cross-tab (reproduces + verifies MD-beta section 6.3)

Source: [`output/streak_intensity_crosstab.csv`](output/streak_intensity_crosstab.csv).

Per-episode intensity fingerprint (`vh_frac` = fraction of episode's days that are `very_heavy`; `vh_count` = count of very_heavy days in the episode):

| L_bin | n episodes | mean vh_frac | median vh_frac | mean vh_count | median vh_count |
|---|---:|---:|---:|---:|---:|
| 1 | 188 | 0.436 | 0.000 | 0.436 | 0.0 |
| 2 | 77 | 0.481 | 0.500 | 0.961 | 1.0 |
| 3 | 27 | 0.519 | 0.667 | 1.556 | 2.0 |
| 4+ | 22 | 0.538 | 0.550 | 2.636 | 3.0 |

**Verification vs MD-beta section 6.3**: mean vh_frac, median vh_frac, mean vh_count MATCH byte-for-byte across all four bins (median vh_count is newly emitted; not in MD-beta table).

**Interpretive discipline** (reproduces MD-beta section 6.3 read verbatim): mean vh_frac is only mildly monotonically increasing with L_bin (0.44 -> 0.48 -> 0.52 -> 0.54), so the streak-length x intensity confound is real but not extreme. Median vh_frac shows more variation (0 at L=1, 0.5 at L=2, 0.67 at L=3) driven by the L=1 bin's high count of heavy-only single-day episodes. Mean vh_count grows roughly linearly with L_bin (as expected mechanically -- more days -> more opportunities for very_heavy).

**Load-bearing for MD-beta section 5 confound 2**: Stage D intensity-adjusted companion (streak-length crash-rate restricted to streaks where vh_frac below some cutoff, or intensity as a stratifier per parent MD section 9) uses this cross-tab as the empirical anchor. The mild-monotonic pattern means intensity is an unavoidable confound for the streak-length arc but not one that would trivially explain a monotone streak-length -> crash-rate dose-response.

---

## 5. Streak-length x era cross-tab (reproduces + verifies MD-beta section 6.4)

Source: [`output/streak_era_crosstab.csv`](output/streak_era_crosstab.csv).

`gap=0` heavy episodes by year_end (year of episode-end date) x L_bin:

| Year | n episodes | L=1 | L=2 | L=3 | L=4+ | (L=3 + L=4+) / n |
|---|---:|---:|---:|---:|---:|---:|
| 2022 | 44 | 26 | 11 | 2 | 5 | 15.9% |
| 2023 | 87 | 59 | 20 | 5 | 3 | 9.2% |
| 2024 | 81 | 50 | 23 | 4 | 4 | 9.9% |
| 2025 | 66 | 37 | 14 | 9 | 6 | 22.7% |
| 2026 (partial Jan-Jun) | 36 | 16 | 9 | 7 | 4 | 30.6% |

**Verification vs MD-beta section 6.4**: all 25 cells MATCH byte-for-byte.

**Interpretive discipline** (reproduces + extends MD-beta section 6.4 read): the 2026 partial year has a notably higher rate of L=3 and L=4+ episodes relative to total (11 / 36 = 30.6%, vs 8 / 87 = 9.2% in 2023 and 8 / 81 = 9.9% in 2024). The **2025 elevation** (15 / 66 = 22.7% at L=3 or L=4+) is newly surfaced by this audit's derived (L=3 + L=4+) rate column and is comparable in direction to the 2026 partial elevation. Both align with parent Q24 MD section 10 caveat 1 (2026 heavy-rate elevation) and confirm the era-confound for MD-beta section 4 streak-length tests. **Stage D handling**: era-stratified sensitivity arm (section 12 below is the descriptive companion).

**Cross-reference to MD-beta section 5 confound 3**: era-stratified sensitivity arm on the streak-length contrast is a required Stage D companion; section 12 below is the descriptive precursor.

---

## 6. Rest-adjacent prevalence full grid (reproduces + verifies MD-beta section 6.5)

Source: [`output/rest_adjacent_prevalence.csv`](output/rest_adjacent_prevalence.csv).

For all 314 heavy-episode-ends on LC-era, rest-adjacency prevalence by K x direction x operand:

| K | Direction | Operand | n_rest_true | n_rest_false | n_rest_nan | Rate (n_true / 314) |
|---:|---|---|---:|---:|---:|---:|
| 1 | after | primary | 127 | 184 | 3 | 40.4% |
| 1 | after | sensitivity | 233 | 81 | 0 | 74.2% |
| 1 | before | primary | 108 | 206 | 0 | 34.4% |
| 1 | before | sensitivity | 234 | 80 | 0 | 74.5% |
| 2 | after | primary | 171 | 140 | 3 | 54.5% |
| 2 | after | sensitivity | 268 | 46 | 0 | 85.4% |
| 2 | before | primary | 152 | 160 | 2 | 48.4% |
| 2 | before | sensitivity | 265 | 49 | 0 | 84.4% |
| 3 | after | primary | 202 | 110 | 2 | 64.3% |
| 3 | after | sensitivity | 283 | 31 | 0 | 90.1% |
| 3 | before | primary | 198 | 114 | 2 | 63.1% |
| 3 | before | sensitivity | 286 | 28 | 0 | 91.1% |

**Verification vs MD-beta section 6.5**: `n_rest_true` and `rate_over_total` MATCH byte-for-byte across all 12 cells for `after primary`, `after sensitivity`, `before primary`, `before sensitivity` at K in {1, 2, 3}. MD-beta section 6.5 table specifically:

- K=3 rest-AFTER sensitivity = 283 / 314 (90.1%): MATCH.
- K=3 rest-BEFORE sensitivity = 286 / 314 (91.1%): MATCH.
- All other cells: MATCH.

MD-beta section 6.5 does not report `n_rest_nan`; this audit surfaces it explicitly per [CONVENTIONS section 3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from `bout_level_recovery_dynamics.md`)](../../../CONVENTIONS.md#310-operationalisation-faithful-to-the-data-not-just-to-the-description). The 2-3 NaN cases at K in {1, 2, 3} rest-after primary correspond to Garmin non-collection days in the K-day post-episode-end window (2 episodes at K=3, matching the 2 NaN cases surfaced in section 7).

**Interpretive discipline** (reproduces MD-beta section 6.5 read): rest-adjacent prevalence is high under both operands, especially the sensitivity (class-based) operand (90%+ at K=3). This means the rest-absent comparator arm at K=3 primary has n = 314 - 202 = 112 episodes (NaN-as-False; 110 under strict NaN drop per this audit's discipline; see section 7); the primary contrast has plenty of statistical resolution. The sensitivity operand at K=3 leaves only ~31 rest-absent episodes; per-cell counts in the 2x2 contingency will be tight at K=3 under the sensitivity operand.

---

## 7. Rest-adjacency x crash-in-5d full 2x2 grid -- 12 cells (BIGGEST NEW CONTENT)

Source: [`output/rest_adjacency_crash_2x2_full_grid.csv`](output/rest_adjacency_crash_2x2_full_grid.csv) (primary NaN-drop discipline) + [`output/rest_adjacency_crash_2x2_full_grid_naneqfalse.csv`](output/rest_adjacency_crash_2x2_full_grid_naneqfalse.csv) (companion NaN=False; reproduces MD-beta section 6.6 byte-for-byte at K=3 primary).

**NaN-handling deviation from MD-beta section 6.6**: MD-beta section 6.6 draft implicitly treats the 2 NaN rest_after_3_primary cases + the 2 NaN rest_before_3_primary cases as `False` (giving row totals of 112 rest-after-False + 116 rest-before-False). This audit's primary CSV honours [CONVENTIONS section 3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from `bout_level_recovery_dynamics.md`)](../../../CONVENTIONS.md#310-operationalisation-faithful-to-the-data-not-just-to-the-description) zero-vs-NaN discipline and drops NaN rows (giving 110 rest-after-False + 114 rest-before-False). The companion NaN=False CSV [`output/rest_adjacency_crash_2x2_full_grid_naneqfalse.csv`](output/rest_adjacency_crash_2x2_full_grid_naneqfalse.csv) reproduces MD-beta section 6.6 exactly: **K=3 rest-after primary RR = 1.571, K=3 rest-before primary RR = 1.864** -- matches MD-beta section 6.6 "RR = 1.57" + "RR = 1.86" byte-for-byte to 3 significant figures. Deviation between primary + companion grids is 2 to 4 episodes per cell (out of 314); RR and RD differ in the second decimal but never change sign.

### 7.1 Full 12-cell 2x2 grid under primary NaN-drop discipline

| K | Direction | Operand | n_used | Rest-adj crash+/n | Rest-abs crash+/n | Rate rest-adj | Rate rest-abs | RR | RD | Sign |
|---:|---|---|---:|---|---|---:|---:|---:|---:|---|
| 1 | after | primary | 311 | 21/127 | 25/184 | 16.5% [11.1, 24.0] | 13.6% [9.4, 19.3] | 1.22 | +0.03 | inverted |
| 1 | after | sensitivity | 314 | 35/233 | 11/81 | 15.0% [11.0, 20.2] | 13.6% [7.8, 22.7] | 1.11 | +0.01 | inverted |
| 1 | before | primary | 314 | 19/108 | 27/206 | 17.6% [11.6, 25.8] | 13.1% [9.2, 18.4] | 1.34 | +0.04 | inverted |
| 1 | before | sensitivity | 314 | 33/234 | 13/80 | 14.1% [10.2, 19.1] | 16.3% [9.7, 25.8] | 0.87 | -0.02 | **match_pre_commit** |
| 2 | after | primary | 311 | 27/171 | 19/140 | 15.8% [11.1, 22.0] | 13.6% [8.9, 20.2] | 1.16 | +0.02 | inverted |
| 2 | after | sensitivity | 314 | 41/268 | 5/46 | 15.3% [11.5, 20.1] | 10.9% [4.7, 23.0] | 1.41 | +0.04 | inverted |
| 2 | before | primary | 312 | 27/152 | 19/160 | 17.8% [12.5, 24.6] | 11.9% [7.7, 17.8] | 1.50 | +0.06 | inverted |
| 2 | before | sensitivity | 314 | 41/265 | 5/49 | 15.5% [11.6, 20.3] | 10.2% [4.4, 21.8] | 1.52 | +0.05 | inverted |
| 3 | after | primary | 312 | 34/202 | 12/110 | 16.8% [12.3, 22.6] | 10.9% [6.4, 18.1] | 1.54 | +0.06 | inverted |
| 3 | after | sensitivity | 314 | 42/283 | 4/31 | 14.8% [11.2, 19.5] | 12.9% [5.1, 28.9] | 1.15 | +0.02 | inverted |
| 3 | before | primary | 312 | 35/198 | 11/114 | 17.7% [13.0, 23.6] | 9.6% [5.5, 16.5] | 1.83 | +0.08 | inverted |
| 3 | before | sensitivity | 314 | 43/286 | 3/28 | 15.0% [11.4, 19.6] | 10.7% [3.7, 27.2] | 1.40 | +0.04 | inverted |

Brackets are Wilson 95% score CI on the per-arm rate. RR = rate_rest_adjacent / rate_rest_absent. `sign` = "inverted" when RR > 1.0 (rest-adjacent HIGHER crash rate; opposite of MD-beta section 3.7 pre-commit direction of "rest-adjacent -> LOWER crash rate"); "match_pre_commit" when RR < 1.0.

**Grid headline** (refined at r1 lock post-review absorption per L3 minor fire on definitional-pair structure): **11 of 12 cells show sign-inversion** (RR > 1.0; rest-adjacent HIGHER crash rate than rest-absent, opposite of MD-beta section 3.7 pre-commit direction). **1 of 12 cells matches pre-commit** (K=1 rest-before sensitivity operand: RR = 0.87). **Note on cell independence**: the 12-cell grid is structured as 6 independent (K × direction) contrasts × 2 definitional-pair operand variants (primary p25 + sensitivity class) per MD-beta section 3.1. **5 of 6 (K × direction) contrasts show sign-inversion under BOTH primary and sensitivity operands** (K in {2, 3} × both directions + K=1 rest-after both operands); **1 of 6 contrasts shows a definitional-pair split** (K=1 rest-before: primary RR = 1.34 inverted, sensitivity RR = 0.87 matches-pre-commit). Per [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair) definitional-pair discipline, the split does not constitute independent evidence against the aggregate inversion pattern -- it is one contrast on which the two operands diverge. Aggregate reading: 5 of 6 K × direction contrasts inverted under both operands; 1 of 6 shows operand-split. No cell has a Wilson-CI overlap that would credibly rule out RR = 1.0 within Stage -1 descriptive-with-CI framing (all per-arm CIs overlap the counter-arm; RR CIs would require bootstrap at Stage D). The inverted pattern is consistent with the MD-beta section 6.8 anticipatory-drafting-note: the confounding-by-indication mechanism (MD-beta section 3.9 confound 1; Salas 2001; Kyriacou & Lewis 2016 *JAMA*) is compatible with the observed pattern.

### 7.2 Endogeneity confound framing per MD-beta section 3.9 item 1

**Per [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing**: the sign-inversion is REPORTED as a descriptive-with-CI observation UNDER the confounding-by-indication caveat, NOT as a verdict. MD-beta section 3.9 confound 1 explicitly names this pattern:

> Rest-day-adjacency is observational, not experimentally-manipulated. The participant may have chosen to rest **because they felt bad** -- pre-heavy fatigue -> rest-before-heavy chosen -> participant enters heavy day already vulnerable -> higher crash risk in +5d.

The 11 inverted cells + 1 match-pre-commit cell are compatible with (a) genuine sign-inversion under the endogeneity mechanism, (b) chance sampling variation in a corpus of n=314 episodes with a 14.6% crash-in-5d base rate (Wilson CIs are wide), or (c) unobserved confounder (envelope-shift, era-specific rest-taking behaviour; see section 9). This audit does NOT distinguish between these -- Stage D formal testing with block-appropriate null (MD-beta section 3.10 sensitivity 2) is the appropriate machinery for that.

### 7.3 Asymmetry between rest-before and rest-after directions

Per MD-beta section 3.9 item 2, the endogeneity mechanism is **stronger for rest-BEFORE than rest-AFTER**: pre-heavy rest may reflect either strategic pacing or felt-bad-so-rested, while post-heavy rest is more forward-looking recovery. Under the endogeneity reading, rest-before would be more sign-inverted than rest-after.

Data pattern (primary operand only, dropping sensitivity for comparability with MD-beta section 3.9 item 2 reasoning):

| K | rest-after primary RR | rest-before primary RR | before - after |
|---:|---:|---:|---:|
| 1 | 1.22 | 1.34 | +0.12 |
| 2 | 1.16 | 1.50 | +0.34 |
| 3 | 1.54 | 1.83 | +0.29 |

**Descriptive-with-CI read**: rest-before RR exceeds rest-after RR at every K under the primary operand (all three deltas positive, mean +0.25). Direction is compatible with the MD-beta section 3.9 item 2 endogeneity-asymmetry prediction (rest-before more sign-inverted than rest-after). Not a verdict; Wilson CIs on all four rates overlap substantially; formal test of RR difference is a Stage D concern.

### 7.4 Which cells maintain vs flip the sign-inversion

**All 6 primary-operand cells (K x direction)** show RR >= 1.16, all inverted.

**5 of 6 sensitivity-operand cells** show RR >= 1.11, inverted. The exception is K=1 rest-before sensitivity (RR = 0.87), the only cell that matches the pre-commit direction. Per [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair) definitional-pair discipline, this single match-pre-commit cell must NOT be reported as independent evidence against the sign-inversion pattern -- it is one member of a definitional pair with K=1 rest-before primary (which shows RR = 1.34, inverted).

**Descriptive summary**: the sign-inversion is broadly consistent across the 12-cell grid (11 / 12 inverted); the single match-pre-commit cell has a wide Wilson CI on the rest-absent arm (16.3% [9.7, 25.8]) and does not credibly contradict the aggregate pattern.

---

## 8. Streak-length x crash-in-5d table -- descriptive precursor to MD-beta section 4.3

Source: [`output/streak_length_crash_table.csv`](output/streak_length_crash_table.csv).

### 8.1 All-episodes pool (n=314)

| L_bin | n episodes | n crash+ | Crash rate | Wilson 95% CI |
|---|---:|---:|---:|---|
| 1 | 188 | 28 | 14.9% | [10.5, 20.7] |
| 2 | 77 | 10 | 13.0% | [7.2, 22.3] |
| 3 | 27 | 5 | 18.5% | [8.2, 36.7] |
| 4+ | 22 | 3 | 13.6% | [4.7, 33.4] |

**Row-total check**: 188 + 77 + 27 + 22 = 314 (matches parent Stage -1 section 4). Crash-count total: 28 + 10 + 5 + 3 = 46, matches MD-beta section 6.7 "46 / 314 = 14.6%" base rate byte-for-byte.

### 8.2 Strict-clean subset (parent MD section 5.2 filter: no other heavy day in [D+1, D+5])

| L_bin | n episodes | n crash+ | Crash rate | Wilson 95% CI |
|---|---:|---:|---:|---|
| 1 | 40 | 6 | 15.0% | [7.1, 29.1] |
| 2 | 6 | 1 | 16.7% | [3.0, 56.4] |
| 3 | 4 | 2 | 50.0% | [15.0, 85.0] |
| 4+ | 2 | 0 | 0.0% | [0.0, 65.8] |

**Row-total check**: 40 + 6 + 4 + 2 = 52 (matches parent Stage D r4 section 3 strict-clean +5d n=52 exactly). Crash-count total: 6 + 1 + 2 + 0 = 9, matches parent Stage D r4 section 3 "9 / 52 = 17.3%" byte-for-byte.

### 8.3 Descriptive-with-CI framing per MD-beta section 4.3

**All-episodes pool**: crash rate is essentially flat across L_bin (14.9% -> 13.0% -> 18.5% -> 13.6%); no monotone increasing pattern visible. Wilson CIs at L=3 and L=4+ are wide (10-37% and 5-33%) reflecting small per-bin sample sizes (n=27 and n=22). **MD-beta section 4.4 pre-committed direction** (longer streaks -> HIGHER crash rate, dose-response of cumulative load) is NOT visible in the descriptive-with-CI read; the observed pattern is closer to flat than dose-response, and neither monotone-increasing nor monotone-decreasing.

**Strict-clean subset**: n=52 total with n <= 6 at L in {2, 3, 4+}; crash rate at L=3 (50%, n=4) is noisy artefact of the tiny cell (Wilson CI [15, 85]) and does NOT constitute descriptive evidence for the dose-response direction. **Non-interpretable at the tight-cell resolution**; noted per Stage -1 audit discipline that per-sub-bin analysis at n < 10 is narrative-only.

**Cochran-Armitage trend test discipline (Stage D, NOT this audit)**: the ordinal 4-bin x binary-outcome contingency at all-episodes pool has enough total events (46) for the Cochran-Armitage trend test to run per MD-beta section 4.5; this Stage -1 descriptive audit does NOT run the test. Descriptive-with-CI direction (flat, not monotone-increasing) is a Stage D concern to reason about post-test.

### 8.4 Confound-2 (streak-length x intensity) descriptive check

Cross-referencing section 4 above: mean vh_frac increases mildly across L_bin (0.44 -> 0.48 -> 0.52 -> 0.54). Under MD-beta section 5 confound 2, a monotone streak-length -> crash-rate relationship could be confounded by intensity accumulation. This audit's descriptive read shows **no monotone crash-rate pattern to confound in the first place** -- the confound is a foreseen Stage D concern per MD-beta but does not have an observed effect to modulate at Stage -1.

---

## 9. Era-stratified rest-adjacency 3-way cross-tab

Source: [`output/rest_adjacency_by_era.csv`](output/rest_adjacency_by_era.csv). Uses K=3 primary rest-after operand (the MD-beta section 3.2 primary K value on the section 3.1 primary operand).

| Year | rest-adj n_ep | rest-adj crash+ | rest-adj rate | rest-abs n_ep | rest-abs crash+ | rest-abs rate | RR (adj/abs) | RD (adj-abs) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | 30 | 5 | 16.7% [7.3, 33.6] | 13 | 2 | 15.4% [4.3, 42.2] | **1.08** | +0.01 |
| 2023 | 52 | 12 | 23.1% [13.7, 36.1] | 35 | 4 | 11.4% [4.5, 26.0] | **2.02** | +0.12 |
| 2024 | 60 | 14 | 23.3% [14.4, 35.4] | 20 | 3 | 15.0% [5.2, 36.0] | **1.56** | +0.08 |
| 2025 | 37 | 1 | 2.7% [0.5, 13.8] | 29 | 1 | 3.4% [0.6, 17.2] | **0.78** | -0.01 |
| 2026 (partial) | 23 | 2 | 8.7% [2.4, 26.8] | 13 | 2 | 15.4% [4.3, 42.2] | **0.57** | -0.07 |

Wilson 95% CI in brackets. RR = crash rate rest-adjacent / crash rate rest-absent.

### 9.1 Era-stratified sign-inversion pattern

**Sign-inversion is NOT stable across the LC era**:

- 2022 (partial): RR = 1.08, essentially null (very small n).
- **2023 + 2024: strongly inverted** (RR = 2.02 and 1.56; rest-adjacent has ~2x the crash rate of rest-absent).
- **2025 + 2026: matches pre-commit direction** (RR = 0.78 and 0.57; rest-adjacent has LOWER crash rate).

This is a **substantive era-stratified finding**. The whole-corpus sign-inversion at RR = 1.57 (K=3 rest-after primary; section 7 or MD-beta section 6.6) is driven **primarily by 2023 + 2024**, the years with the highest absolute crash-rate on the rest-adjacent arm (23% and 23%). In 2025 and 2026, the absolute crash rate on the rest-adjacent arm drops dramatically (2.7% and 8.7% respectively), and the direction reverses.

**Alignment with parent Q24 MD section 10 caveat 1 + registry.md recovery trajectory**: crash frequency dropped from ~10/year in 2023-2024 to ~2/year in 2025-2026 per the registry trajectory. The era-stratified sign-inversion pattern here is consistent with (a) both arms having much smaller absolute crash counts in 2025-2026 (Wilson CIs get very wide; e.g. 2025 rest-adj CI is [0.5, 13.8] on 1/37), and (b) the participant's rest-behaviour envelope potentially shifting with the recovery trajectory.

### 9.2 Confound 7 escalation-to-caveat per parent Q24 MD

Per MD-beta section 5 confound 7 + parent Q24 MD section 10 caveat 8 (envelope-drift asymmetry), the era-stratified sensitivity arm IS the analogue drift-correction mechanism per MD-beta section 5 confound 7 does-not-apply-redirected-to-analogue paragraph (CONVENTIONS section 3.7 detrend does not apply to binary-outcome contingency tests). This audit surfaces era-instability of the sign-inversion; that instability is a **caveat-class finding per [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)** to be pre-committed in any downstream Stage H pre-registration.

**Descriptive-with-CI framing**: the 2023 + 2024 sign-inversion + 2025 + 2026 direction-flip is presented as descriptive-with-CI observation UNDER the confounding-by-indication caveat (section 7.2 + MD-beta section 3.9 confound 1). It is not a Stage D verdict; it is a Stage -1 signal that any downstream Stage D contrast must stratify by era, not pool across the full 4-year LC-era corpus, or explicitly acknowledge the era-drift as an uncorrected confounder.

### 9.3 Endogeneity confound framing per MD-beta section 3.9

The era-instability does NOT rule out the confounding-by-indication mechanism (MD-beta section 3.9 confound 1). Under the endogeneity reading, the participant's rest-taking behaviour + crash-vulnerability envelope may both have shifted with the recovery trajectory, producing era-specific joint-distribution changes. Alternative interpretations (rest genuinely became protective in 2025-2026 as the participant's baseline improved; sign-inversion in 2023-2024 driven by acute confounding-by-indication) are structurally indistinguishable at Stage -1 descriptive resolution and remain plausible without further data.

---

## 10. Intensity-stratified rest-adjacency 3-way cross-tab

Source: [`output/rest_adjacency_by_intensity.csv`](output/rest_adjacency_by_intensity.csv). Uses K=3 primary rest-after operand; stratified by episode-end intensity class (D_end is heavy vs very_heavy).

| End class | rest-adj n_ep | rest-adj crash+ | rest-adj rate | rest-abs n_ep | rest-abs crash+ | rest-abs rate | RR (adj/abs) | RD (adj-abs) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| heavy (D_end class = heavy) | 108 | 24 | 22.2% [15.4, 30.9] | 56 | 6 | 10.7% [5.0, 21.5] | **2.07** | +0.12 |
| very_heavy (D_end class = very_heavy) | 94 | 10 | 10.6% [5.9, 18.5] | 54 | 6 | 11.1% [5.2, 22.2] | **0.96** | -0.005 |

### 10.1 Intensity-stratified sign-inversion pattern

**Sign-inversion is intensity-dependent**:

- **Heavy episode-end: strongly inverted** (RR = 2.07; rest-adjacent has 2x the crash rate).
- **Very_heavy episode-end: essentially null** (RR = 0.96; rest-adjacent and rest-absent arms have similar crash rates).

This is another **substantive stratified finding** parallel to section 9. The whole-corpus sign-inversion is driven **primarily by heavy-episode-end episodes**; very_heavy episode-ends show no sign-inversion at all.

**Confound-2 cross-reference** (streak-length x intensity, MD-beta section 5 confound 2): the "heavy" episode-end stratum includes episodes where D_end is `heavy` (not `very_heavy`); this stratum captures lower-intensity heavy days at the episode terminus. If the confounding-by-indication mechanism is stronger for felt-bad episodes that end at a heavy (not very_heavy) day, that would be consistent with the pattern here -- but this is speculation at Stage -1 descriptive resolution.

**Alternative reading**: very_heavy episode-ends may reflect episodes where the participant was genuinely pushing rather than reactively-resting-because-felt-bad. The felt-bad-so-rested endogeneity would then be less operative for very_heavy-terminal episodes than for heavy-terminal episodes.

### 10.2 Descriptive-with-CI framing

Neither stratum's per-arm CIs credibly rule out RR = 1.0 for that stratum. Cross-stratum comparison (heavy RR = 2.07 vs very_heavy RR = 0.96) is descriptive; the intensity-stratified interaction test is a Stage D concern.

**Per [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing**: the intensity-instability of the sign-inversion is a **caveat-class finding** for any downstream Stage H pre-registration. It suggests any Stage D contrast should either stratify by intensity or acknowledge the intensity-dependence as an uncorrected confounder.

### 10.3 Cross-reference to MD-beta section 5 confound 2 machinery

MD-beta section 5 confound 2 pre-commits Stage D handling as "report streak-length x crash-rate contrast alongside an intensity-adjusted companion". This audit's section 10 shows the intensity-adjusted companion is load-bearing for the rest-adjacency arc too (not just the streak-length arc). Stage D machinery for the rest-adjacency arc should apply an analogous intensity-adjustment (stratify by end_class heavy vs very_heavy at minimum; log-binomial regression with intensity as covariate per MD-beta section 3.6 state-of-art naming as the natural extension).

---

## 11. Overlap-policy sensitivity 2x2 (strict-clean subset)

Source: [`output/overlap_policy_sensitivity_2x2.csv`](output/overlap_policy_sensitivity_2x2.csv). K=3 primary rest-after operand on the **strict-clean subset** (parent MD section 5.2 filter: no other heavy day in [D_end+1, D_end+5]; n=52 at +5d matches parent Stage D r4 section 3).

| Pool | K | Direction | Operand | n_used | Rest-adj crash+/n | Rest-abs crash+/n | Rate rest-adj | Rate rest-abs | RR | RD |
|---|---:|---|---|---:|---|---|---:|---:|---:|---:|
| strict_clean | 3 | after | primary | 51 | 6/43 | 3/8 | 14.0% [6.6, 27.3] | 37.5% [13.7, 69.4] | **0.37** | -0.24 |

Row-total check: 43 + 8 = 51 (one NaN dropped from the strict-clean n=52 per section 7 NaN discipline).

### 11.1 Overlap-policy sensitivity finding

**On the strict-clean subset the sign-inversion FLIPS**: RR = 0.37 (rest-adjacent has LOWER crash rate than rest-absent), matching the MD-beta section 3.7 pre-committed direction. The all-episodes pool at the same K x direction x operand (section 7 row 9) shows RR = 1.54 (rest-adjacent HIGHER crash rate).

**Sample-size caveat**: strict-clean n=51 is small; the rest-absent arm has n=8 with 3 crash-in-5d events (Wilson CI [13.7, 69.4] -- very wide). The 3/8 = 37.5% rate on the rest-absent arm is an outlier driven by tiny cell size (the corpus-baseline rest-absent rate on all-episodes is 10.9%); the strict-clean flip may be an artefact of the small comparator arm rather than a genuine overlap-policy effect.

### 11.2 Interpretive discipline per MD-beta section 3.10

Per MD-beta section 3.10 overlap-policy sensitivity: "Divergence between primary and sensitivity 1 identifies whether overlap contamination is confounding the rest-adjacency signal." The observed divergence (RR = 1.54 vs 0.37) is **substantial** at the RR level but rests on a very small strict-clean sample. **Descriptive-with-CI framing**: the divergence is a caveat-class observation; it does not falsify either direction, and the strict-clean rest-absent arm's 3/8 = 37.5% rate is too noisy for a Stage -1 verdict.

**Confound 4 in MD-beta section 3.9** (all-episodes pool vs strict-clean pool) pre-commits this exact sensitivity report; the divergence surfaced here fires the "substantive finding" flag in that pre-commit. Stage D machinery per MD-beta section 3.10 (block-length-appropriate null for the inclusive sensitivity 2) may resolve whether the divergence is real or noise, but not at Stage -1 descriptive resolution.

---

## 12. Era-stratified streak-length x crash-in-5d

Source: [`output/streak_length_by_era_crash.csv`](output/streak_length_by_era_crash.csv). All-episodes pool per section 8.1 + parent MD section 4.3.

| Year | L=1 crash+/n | L=2 crash+/n | L=3 crash+/n | L=4+ crash+/n |
|---|---|---|---|---|
| 2022 | 5/26 (19.2%) | 2/11 (18.2%) | 0/2 (0.0%) | 0/5 (0.0%) |
| 2023 | 10/59 (16.9%) | 3/20 (15.0%) | 2/5 (40.0%) | 1/3 (33.3%) |
| 2024 | 11/50 (22.0%) | 3/23 (13.0%) | 2/4 (50.0%) | 1/4 (25.0%) |
| 2025 | 1/37 (2.7%) | 0/14 (0.0%) | 1/9 (11.1%) | 0/6 (0.0%) |
| 2026 (partial) | 1/16 (6.3%) | 2/9 (22.2%) | 0/7 (0.0%) | 1/4 (25.0%) |

### 12.1 Era-stratified dose-response pattern

**Dose-response direction is NOT stable across the LC era**:

- **2022**: L=3 and L=4+ have 0/2 and 0/5 crash rates (very small samples); L=1 and L=2 are ~18-19%. Descriptively contradicts dose-response.
- **2023**: L=3 (40%) and L=4+ (33%) rates exceed L=1 (17%) and L=2 (15%) rates. Descriptively matches MD-beta section 4.4 pre-committed direction (longer streaks -> higher crash rate) BUT L=3 and L=4+ have n <= 5 each; Wilson CIs are wide (~10-70%).
- **2024**: L=3 (50%) and L=4+ (25%) rates exceed L=1 (22%) and L=2 (13%) rates. Same descriptive pattern as 2023 with same small-n caveat.
- **2025**: essentially all bins near zero crash rate (0-11%). Dose-response direction not visible; total 2/66 = 3% base rate.
- **2026 (partial)**: L=2 (22%) exceeds L=1 (6%); L=3 = 0%; L=4+ = 25%. Non-monotone.

**Row-total check**: 2022 n = 26+11+2+5 = 44 (matches section 5); 2023 n = 87; 2024 n = 81; 2025 n = 66; 2026 partial n = 36. Grand total = 314. Grand crash-count = (5+2+0+0)+(10+3+2+1)+(11+3+2+1)+(1+0+1+0)+(1+2+0+1) = 7+16+17+2+4 = 46. Matches section 8.1 all-episodes pool crash-count.

### 12.2 Descriptive-with-CI framing

**Overall pattern**: the pooled all-episodes crash-rate-by-L_bin (section 8.1) shows a flat pattern (14.9% / 13.0% / 18.5% / 13.6%). The era-stratified breakdown shows that **2023 and 2024 exhibit the descriptive dose-response direction MD-beta section 4.4 pre-commits (albeit at small sub-cell n)**, while **2025 and 2026 do not**. The pooled flat pattern is a mix of era-specific patterns that partially cancel.

**Alignment with section 9**: exactly the same era-split -- 2023-2024 exhibit the "expected" direction (per MD-beta section 4.4 pre-commit); 2025-2026 do not. Both stratifications point at the same era-boundary; the recovery trajectory from 2023-2024 (high crash frequency) to 2025-2026 (low crash frequency) is the natural mechanistic anchor.

### 12.3 Confound 3 escalation-to-caveat per MD-beta section 5 + parent Q24 MD

Per MD-beta section 5 confound 3 (streak-length x era confound), Stage D handling pre-commits an era-stratified sensitivity arm for the streak-length contrast. This audit surfaces exactly why: the dose-response direction visible in 2023-2024 (small n but consistent sign) is diluted by the flat 2025-2026 pattern in the pooled read.

**Caveat-class finding per [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)**: Stage D contrasts for the streak-length arc should either stratify by era or acknowledge era-drift as an uncorrected confounder.

---

## 13. Findings summary + Stage D readiness assessment

### 13.1 Section 2-6 reproducibility of MD-beta section 6.1-6.5 numbers

**All MD-beta section 6.1-6.5 numbers MATCH byte-for-byte** with this audit's re-computation on the same `per_day_master.csv`:

- Section 6.1 rest-day distribution: 404 primary + 724 sensitivity + 6-class breakdown -- MATCH.
- Section 6.2 streak-length distribution: 188 / 77 / 27 / 22 + sub-bin structure -- MATCH.
- Section 6.3 streak-length x intensity: mean vh_frac + median vh_frac + mean vh_count across 4 bins -- MATCH.
- Section 6.4 streak-length x era: 25-cell year x L_bin cross-tab -- MATCH.
- Section 6.5 rest-adjacent prevalence: 12-cell K x direction x operand grid -- MATCH.

### 13.2 Section 6.6 reproducibility (K=3 primary rest-after + rest-before) -- deviation documented

**MD-beta section 6.6 numbers match under NaN=False convention (companion CSV [`rest_adjacency_crash_2x2_full_grid_naneqfalse.csv`](output/rest_adjacency_crash_2x2_full_grid_naneqfalse.csv))**:

- K=3 rest-after primary: 34/202 rest-adj + 12/112 rest-abs = 202 + 112 = 314. Rate rest-adj 16.8%, rate rest-abs 10.7%, RR = 1.571. Matches MD-beta section 6.6 "RR = 1.57" byte-for-byte.
- K=3 rest-before primary: 35/198 rest-adj + 11/116 rest-abs = 198 + 116 = 314. Rate rest-adj 17.7%, rate rest-abs 9.5%, RR = 1.864. Matches MD-beta section 6.6 "RR = 1.86" byte-for-byte.

**Under this audit's primary NaN-drop discipline per [CONVENTIONS section 3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from `bout_level_recovery_dynamics.md`)](../../../CONVENTIONS.md#310-operationalisation-faithful-to-the-data-not-just-to-the-description)**: 2 rest-after NaN cases + 2 rest-before NaN cases are dropped, giving n=110 rest-after-abs and n=114 rest-before-abs. RR moves modestly (1.54 rest-after; 1.83 rest-before) but never changes sign. Deviation documented explicitly in section 7 above.

### 13.3 12-cell 2x2 grid headline (section 7)

**11 of 12 cells show sign-inversion** (RR > 1.0; rest-adjacent HIGHER crash rate than rest-absent, opposite of MD-beta section 3.7 pre-commit).

**1 of 12 cells matches pre-commit** (K=1 rest-before sensitivity, RR = 0.87). Per definitional-pair discipline, this single cell is not independent evidence -- it is one member of a definitional pair with the K=1 rest-before primary cell (RR = 1.34, inverted).

**Sign-inversion asymmetry between rest-before and rest-after (primary operand only)**: rest-before RR > rest-after RR at every K (+0.12, +0.34, +0.29). Direction is compatible with MD-beta section 3.9 item 2 endogeneity-asymmetry prediction.

### 13.4 Era-stratified pattern (section 9)

**Sign-inversion is NOT stable across the LC era**. RR at K=3 rest-after primary by year:

- 2022: 1.08 (essentially null)
- 2023: **2.02** (strong inversion)
- 2024: 1.56 (moderate inversion)
- 2025: **0.78** (matches pre-commit)
- 2026: **0.57** (matches pre-commit)

The whole-corpus RR = 1.57 is driven primarily by 2023 + 2024; 2025 + 2026 show the pre-committed direction. Era-stratified sensitivity arm at Stage D is a required companion; era-drift is a caveat-class confound to pre-commit in any downstream Stage H pre-registration.

### 13.5 Intensity-stratified pattern (section 10)

**Sign-inversion is intensity-dependent**. RR at K=3 rest-after primary by episode-end class:

- heavy end_class: **2.07** (strong inversion; parallel to 2023 + 2024 era pattern)
- very_heavy end_class: **0.96** (essentially null; no inversion)

The whole-corpus sign-inversion is driven primarily by heavy-terminal episodes; very_heavy-terminal episodes show no inversion. Intensity-stratified sensitivity arm at Stage D is a required companion; intensity-dependence is a caveat-class confound.

### 13.6 Overlap-policy sensitivity flip (section 11)

**On the strict-clean subset (n=51 with valid rest indicator; n=52 in parent Stage D r4)**: K=3 rest-after primary shows RR = 0.37 (rest-adjacent LOWER crash rate; matches pre-commit direction). The flip vs all-episodes pool (RR = 1.54) is substantial at the RR level but rests on a tiny rest-absent arm (n=8 with 3 crash-in-5d). Divergence flagged per MD-beta section 3.10 sensitivity 1 discipline; too small for a Stage -1 verdict.

### 13.7 Streak-length dose-response (section 8 + section 12)

**No monotone streak-length -> crash-rate dose-response visible on the all-episodes pool** (14.9% / 13.0% / 18.5% / 13.6% across L_bin {1, 2, 3, 4+}). Era-stratified breakdown shows 2023 + 2024 exhibit the pre-committed direction at small sub-cell n; 2025 + 2026 do not. Pooled flat pattern is a mix of era-specific patterns that partially cancel. Stage D Cochran-Armitage trend test per MD-beta section 4.5 will formally test on 46 events; the descriptive pattern suggests the trend test is unlikely to fire on the pooled all-episodes read but may fire in era-stratified sub-reads. Confound 3 (streak-length x era) is load-bearing.

### 13.8 Stage D readiness assessment per MD-beta section 6.8

**Which cells are viable for Stage D contrast**:

- **K=3 primary rest-after all-episodes pool** (n=312 usable per this audit's NaN-drop; 314 under NaN=False): viable for Fisher's exact + Wilson CI + bootstrap null. Base rate 14.6%. Sign-inversion anticipated per MD-beta section 6.8 (RR = 1.54 under NaN drop; RR = 1.57 under NaN=False).
- **K=3 primary rest-before all-episodes pool** (n=312 usable per NaN-drop; 314 NaN=False): viable. Sign-inversion anticipated (RR = 1.83 / 1.86).
- **K=1 and K=2 primary rest-after and rest-before all-episodes pool**: viable. All 4 cells inverted with RR in [1.16, 1.50].
- **All 6 sensitivity-operand cells**: 5 inverted (RR in [1.11, 1.52]), 1 match-pre-commit (K=1 rest-before, RR = 0.87). Per definitional-pair discipline the sensitivity operand is a robustness check, not independent evidence.
- **Strict-clean subset (K=3 rest-after primary, n=51)**: rest-absent arm has n=8, TOO SMALL for Fisher's exact at usable resolution. Descriptive-only-with-CI.
- **Streak-length dose-response on all-episodes pool (n=314)**: Cochran-Armitage trend test viable; descriptive-with-CI shows flat pattern. Per-bin Wilson CIs at L=3 (n=27) and L=4+ (n=22) are wide.
- **Era-stratified rest-adjacency**: per-year n is 36-87; per-year x rest-arm cell size is 13-60; Fisher's exact viable for 2023 and 2024 individually; underpowered for 2022, 2025, 2026.
- **Intensity-stratified rest-adjacency**: n=164 heavy end + n=148 very_heavy end; Fisher's exact viable for each stratum individually.

**Which cells are underpowered**:

- Any per-year x per-L_bin cell (L=3 or L=4+ within a single year; n <= 9). Narrative-only.
- Strict-clean subset x L_bin (L=2 / L=3 / L=4+ each has n <= 6). Narrative-only.

**Sign-inversion pre-commit path per MD-beta section 6.8** (anticipatory closure): Stage D confirms the pooled sign-inversion at the primary K=3 rest-after cell (RR = 1.54 / 1.57). Two acceptable Stage H pre-reg closure paths:

- **(a)** Stage H pre-reg drafts with sign-inversion as the pre-committed direction, cites MD-beta section 3.9 confound 1 (confounding-by-indication; Salas 2001; Kyriacou & Lewis 2016) as the interpretive-caveat, and treats the mechanism-not-effect reading as the Stage H falsifier.
- **(b)** Stage D triggers a pre-Stage-H MD r2 revision that formally flips the section 3.7 direction pre-commit; the r2 revision goes through fresh-session review before any Stage H pre-reg drafts.

**Additional caveat-class findings for any Stage H pre-reg**: (i) era-stratified instability (section 9); (ii) intensity-stratified instability (section 10); (iii) overlap-policy sensitivity flip on strict-clean subset (section 11); (iv) flat streak-length dose-response on pooled all-episodes (section 8). None of these are individually Stage-D verdicts; all are caveats a downstream Stage H pre-reg must acknowledge.

### 13.9 Reviewer-concerns to walk

Points a reviewer should verify or push back on:

1. **NaN discipline choice**: this audit's NaN-drop primary vs MD-beta section 6.6 draft's implicit NaN-as-False. Which is the correct discipline for a downstream Stage H pre-reg? Recommendation: NaN-drop (per CONVENTIONS section 3.10 (parent MD "zero-vs-NaN" shorthand)); NaN-as-False companion CSV preserved for byte-for-byte reproduction of MD-beta section 6.6.
2. **Era-stratified vs pooled reporting** in any Stage H pre-reg: given the strong era-instability (section 9), is pooling still defensible? MD-beta section 3.5 stationarity assumption paragraph acknowledges pooling as a substantive assumption; section 9 empirical evidence tests that assumption and finds it does not hold. Reviewer should decide whether pooled contrast is still primary or whether era-stratified becomes primary.
3. **Intensity-stratified vs pooled reporting**: same question, mirrored. Section 10 shows strong intensity-instability (heavy RR = 2.07 vs very_heavy RR = 0.96). Should Stage H pre-reg stratify by end_class or covariate-adjust via log-binomial per MD-beta section 3.6 state-of-art naming?
4. **Overlap-policy sensitivity flip on strict-clean (section 11)**: is this a genuine overlap-contamination effect or a small-cell artefact? Divergence between all-episodes RR = 1.54 and strict-clean RR = 0.37 is large but rests on n=8 rest-absent cell in strict-clean. Reviewer should decide whether strict-clean is a load-bearing sensitivity or a noise floor.
5. **Streak-length flat dose-response (section 8.1)**: the whole-corpus pattern is essentially flat (14.9% / 13.0% / 18.5% / 13.6%). MD-beta section 4.4 pre-commits direction "longer streaks -> HIGHER crash rate". Stage D Cochran-Armitage will formally test; descriptive Stage -1 pattern suggests the trend test is unlikely to fire on the pooled read. Reviewer should decide whether Stage H pre-reg should draft with sign-inversion or null-direction pre-commit for the streak-length arc.
6. **Compound confound stack**: sections 9 + 10 + 11 each surface a caveat-class instability. Stacked together, they materially constrain the interpretability of any Stage H pre-reg on the rest-adjacency arc. Reviewer should assess whether the operand family is Stage-H-viable at all, or whether MD-beta needs r2 revision that pre-commits era + intensity stratification as primary rather than sensitivity.

### 13.10 MD-beta r2-forcing findings (added at r1 lock post-review absorption)

Fresh-session methodology reviewer ([`../../../reviews/methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md`](../../../reviews/methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md)) classified two of this audit's findings as **escalate-tier fires against MD-beta** (not against this audit; the audit itself is DEFENSIBLE with revision at absorb-tier only):

1. **L2 substantive-escalate (Layer 2 stationarity)**: section 9 era-stratified RR pattern (2022=1.08, 2023=2.02, 2024=1.56, 2025=0.78, 2026=0.57) **empirically rejects MD-beta section 3.5 stationarity assumption** at descriptive-with-CI resolution. Reviewer recommends MD-beta r2 revision upgrading section 5 confound 7 (era-drift) from Stage D sensitivity companion to **Stage D primary pre-commit stratifier** for the rest-adjacency arc.

2. **L4 substantive-escalate (Layer 4 project-specific)**: section 10 intensity-stratified RR pattern (heavy=2.07 vs very_heavy=0.96) **breaks MD-beta section 5 confound 2 sensitivity framing** for the rest-adjacency arc (confound 2 currently pre-commits intensity as sensitivity for the streak-length arc only). Reviewer recommends MD-beta r2 revision upgrading confound 2 to **Stage D primary pre-commit stratifier** for the rest-adjacency arc as well; pooled contrast demoted to caveat-class.

**Reviewer-recommended r2 path (Path A per user endorsement 2026-07-16)**: mechanical patches to MD-beta section 5 confound 2 + confound 7 language upgrading from "sensitivity companions" to "primary pre-commit stratifiers" for the rest-adjacency arc; absorbs inline per MD-beta section 7 compression discipline. Path B (rewriting MD-beta section 3.5 primary contrast) rejected as architectural + forces re-review.

**Structural note**: this audit r1 lock is INDEPENDENT of the MD-beta r2 revision. The audit's job at Stage -1 is to surface the empirical stress on MD-beta's assumptions; that job is complete. The r2 revision is a separate producer-mode artefact drafted in a downstream session under user authorisation, with its own fresh-session methodology review before r2 lock. Stage D descriptive execution against MD-beta operands is blocked until MD-beta r2 lands (per user endorsement of sequence: audit lock → Wave 2C descriptive extension for gevoelscore-conditioned reactive-vs-proactive rest test → MD-beta r2 informed by Wave 2C findings).

---

## 14. Lock log

| version | date | change |
|---|---|---|
| r1 (DRAFTED) | 2026-07-16 | Initial DRAFTED status. Stage -1 descriptive audit extension for MD-beta LOCKED r1 2026-07-16. Reproduces MD-beta section 6.1-6.5 byte-for-byte on `per_day_master.csv` (verified in section 13.1). Extends MD-beta section 6.6 (K=3 primary rest-after only) to full 12-cell K x direction x operand grid on the all-episodes pool (section 7); 11 of 12 cells show sign-inversion (RR > 1.0), 1 cell matches pre-commit direction (K=1 rest-before sensitivity, RR = 0.87). Sign-inversion is era-stratified: 2023 + 2024 strongly inverted (RR = 2.02 + 1.56), 2025 + 2026 match pre-commit (RR = 0.78 + 0.57), 2022 essentially null (RR = 1.08) -- section 9. Sign-inversion is intensity-stratified: heavy end_class strongly inverted (RR = 2.07), very_heavy end_class essentially null (RR = 0.96) -- section 10. Strict-clean overlap policy flips the sign to RR = 0.37 but on very small n=8 rest-absent arm -- section 11. Streak-length crash-rate on all-episodes pool is flat across L_bin (14.9% / 13.0% / 18.5% / 13.6%) not monotonically increasing per MD-beta section 4.4 pre-commit direction; era-stratified breakdown shows 2023 + 2024 exhibit the expected direction at small sub-cell n, 2025 + 2026 do not -- sections 8 + 12. NaN discipline deviation from MD-beta section 6.6 documented: this audit's primary NaN-drop discipline (per CONVENTIONS section 3.10 (parent MD "zero-vs-NaN" shorthand)) gives 2 fewer usable episodes than MD-beta's implicit NaN-as-False convention; RR moves modestly (1.54 vs 1.57 rest-after; 1.83 vs 1.86 rest-before) but never changes sign -- section 7 + section 13.2. Companion CSV `rest_adjacency_crash_2x2_full_grid_naneqfalse.csv` reproduces MD-beta section 6.6 byte-for-byte at K=3 primary. Six reviewer-concerns surfaced for downstream discipline -- section 13.9. No inferential tests run; Fisher's exact + Cochran-Armitage + bootstrap null are Stage D concerns. RANDOM_SEED = 20260716 declared but not exercised. |
| r1 LOCKED | 2026-07-16 | Fresh-session methodology review absorbed from [`../../../reviews/methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md`](../../../reviews/methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md) (verdict: DEFENSIBLE with revision; 4 fires total: 2 absorb-tier on this audit + 2 escalate-tier on MD-beta). Four surgical patches applied per [CONVENTIONS section 1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations) compression discipline. **Patch 1** (bulk anchor fix, review L1 minor): all `[CONVENTIONS section 5](#5-zero-vs-nan)` markdown-link anchors changed to `[CONVENTIONS section 3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from bout_level_recovery_dynamics.md)](#310-operationalisation-faithful-to-the-data-not-just-to-the-description)` -- fixes reviewer's L1 fire that CONVENTIONS section 5 is Project-wide anchors (not zero-vs-NaN) + acknowledges the shorthand terminology's actual codification in parent MD lineage. **Patch 2** (section 7.1 grid headline, review L3 minor): softened "11 of 12 cells inverted" phrasing with cell-independence note -- 12 cells = 6 independent (K × direction) contrasts × 2 definitional-pair operand variants; 5 of 6 K × direction contrasts inverted under BOTH operands; 1 of 6 shows operand-split (K=1 rest-before); per CONVENTIONS section 3.3 definitional-pair discipline the split does not constitute independent evidence against the aggregate pattern. **Patch 3** (new section 13.10, review L2 substantive-escalate + L4 substantive-escalate): reviewer's escalate-tier fires against MD-beta (not against this audit) documented as r2-forcing findings for MD-beta downstream revision. L2 escalate: section 9 era-stratified pattern empirically rejects MD-beta section 3.5 stationarity assumption at descriptive-with-CI resolution. L4 escalate: section 10 intensity-stratified pattern breaks MD-beta section 5 confound 2 sensitivity framing for rest-adjacency arc. User endorsement 2026-07-16 of reviewer-recommended Path A (mechanical patches to MD-beta section 5 confound 2 + confound 7 upgrading from Stage D sensitivity to Stage D primary pre-commit stratifiers for rest-adjacency arc) noted as downstream sequence step. Structural note: audit r1 lock INDEPENDENT of MD-beta r2 revision; audit's job at Stage -1 is to surface empirical stress on MD-beta assumptions, done. **Patch 4** (status header): updated from DRAFTED to LOCKED with pointer to review report + section 13.10 for the 2 absorb + 2 escalate structure. Preserved byte-identically: sections 1-6 (reproduction verification chain intact), section 7.2-7.4 (endogeneity + asymmetry + operand-split reads), section 8 (streak-length crash tables), section 9 (era-stratified 3-way + section 9.1-9.3 interpretation), section 10 (intensity-stratified 3-way + section 10.1-10.3 interpretation), section 11 (overlap-policy sensitivity 2x2), section 12 (era-stratified streak-length), section 13.1-13.9 reviewer-concerns (unchanged; new section 13.10 added after). **STATUS**: LOCKED r1 2026-07-16 post-review absorption. Next-step in user-endorsed sequence: (a) Wave 2C descriptive audit for gevoelscore-conditioned reactive-vs-proactive rest quadrants + very-heavy trend + envelope-variance per [[project_rest_day_operand_semantics]]; (b) MD-beta r2 Path A revision informed by Wave 2C findings; (c) Stage D descriptive execution unblocked after MD-beta r2 lands. |

---

*Producer-mode Stage -1 descriptive audit. Update when (a) any deviation from MD-beta section 6.1-6.5 numbers is surfaced by a downstream re-run, (b) MD-beta advances to r2 with formally revised direction pre-commit, (c) Stage D descriptive audit lands and its numbers should propagate here as the next-stage anchor.*
