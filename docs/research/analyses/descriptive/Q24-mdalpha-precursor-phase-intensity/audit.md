# Descriptive audit -- Q24 MD-alpha precursor: phase-stratified + intensity-stratified data availability

*Producer-mode Stage -1 descriptive audit per [CONVENTIONS §1.1](../../../CONVENTIONS.md) + [§2.1 descriptive-before-inference](../../../CONVENTIONS.md#21-descriptive-before-inference). Drafted 2026-07-16 as r1 by Claude (Opus 4.7) in producer-mode under user authorisation. Authorising user: Willem.*

**Status**: **LOCKED r1 2026-07-16** post-review absorption per [`../../../reviews/methodology-Q24-mdalpha-precursor-phase-intensity-2026-07-16.md`](../../../reviews/methodology-Q24-mdalpha-precursor-phase-intensity-2026-07-16.md) (verdict: DEFENSIBLE with revision; all 7 fires mechanical-clarification absorbs, no architectural change). Stage -1 extension of the parent Q24 precursor audit ([`../Q24-precursor-heavy-day-structure/audit.md`](../Q24-precursor-heavy-day-structure/audit.md) LOCKED r1 2026-07-15). Audits data-availability hooks the LOCKED MD-alpha methodology ([`../../../methodology/post_heavy_day_pacing_learning.md`](../../../methodology/post_heavy_day_pacing_learning.md) LOCKED r1 2026-07-16) §7 defers to Stage -1.

**Frame**: LC-era stratum (`lc_phase == 'lc'`), n=1524 rows per parent Stage -1 audit §1. Heavy-day + episode-end (gap=0) definitions inherited verbatim from parent Q24 methodology MD ([`../../../methodology/post_heavy_day_compensatory_rest.md`](../../../methodology/post_heavy_day_compensatory_rest.md) LOCKED r1) via parent Stage -1 audit §4.

**Inheritance-only**: This audit does NOT re-derive corpus counts, episode structure, overlap density, or intensity stratification design decisions. It executes MD-alpha §7 data-availability probes and reports the results at the operand-cell resolution Stage D executors need. All machinery pointers below cite parent Q24 MD §X, MD-alpha §Y, or parent Stage -1 audit §Z; no re-derivation.

**Reproducibility**: [`scripts/audit.py`](scripts/audit.py) + [`output/`](output/); idempotent re-run against `per_day_master.csv`.

**Cross-refs**: [MD-alpha methodology MD](../../../methodology/post_heavy_day_pacing_learning.md) LOCKED r1 2026-07-16; [parent Q24 methodology MD](../../../methodology/post_heavy_day_compensatory_rest.md) LOCKED r1; [parent Q24 Stage -1 audit](../Q24-precursor-heavy-day-structure/audit.md) LOCKED r1; [CONVENTIONS §2.1 + §3.6 + §5 zero-vs-NaN](../../../CONVENTIONS.md).

---

## 1. Corpus summary

Points at parent Stage -1 audit §1 for corpus-level counts. This audit adds MD-alpha specific reads only.

| Measure | Value | Source |
|---|---|---|
| LC-era rows | 1524 days (2022-04-04 → 2026-06-05) | parent Stage -1 audit §1 |
| Combined heavy-episode-ends (gap=0) | 314 | parent Stage -1 audit §4 + verified [`output/phase_episode_counts.csv`](output/phase_episode_counts.csv) |
| Heavy days (`heavy` + `very_heavy`) | 532 | parent Stage -1 audit §1 |
| Crash days | 103 | parent Stage -1 audit §1 |
| `exertion_class_lagged_lcera` missingness | 70 days (4.6%) | parent Stage -1 audit §1 |
| Total episode-ends (gap=0) after LC-era filter | 314 | verified this audit script `[phase counts] episode-ends combined gap=0 total: 314` |

**Convergence check**: This audit's gap=0 combined episode-ends total = **314**, matches parent Stage -1 audit §4 (n=314) and MD-alpha §3.1 drafted-time probe (n=314) exactly. No divergence.

---

## 2. Phase distribution of heavy-episode-ends (MD-alpha §7.1 / §3.1)

Reproduces MD-alpha §3.1 exact drafted-time table. Source: [`output/phase_episode_counts.csv`](output/phase_episode_counts.csv).

| Phase | Heavy-episode-ends (gap=0, combined) | MD-alpha §3.1 drafted-time probe |
|---|---:|---:|
| `lc_pre_ergo` | **19** | 19 |
| `pacing_pre_citalopram_learning` | **12** | 12 |
| `pacing_habit_established` | **125** | 125 |
| `citalopram_modulated` | **158** | 158 |
| **All LC-era** | **314** | 314 |

**Reproduction verification**: MATCH across all four phase cells and total. MD-alpha §3.1 drafted-time probe is confirmed at LOCKED r1 by this Stage -1 audit against the same input file (`per_day_master.csv` 2026-07-16). No divergence, no override needed.

**Named counts** per [CONVENTIONS §3.6](../../../CONVENTIONS.md#36-named-counts): scheme = "combined heavy-episode-ends counted at the last day of a gap=0 contiguous run"; unit = episode-ends; source = [`output/phase_episode_counts.csv`](output/phase_episode_counts.csv).

**Read implication for Stage D executors**: the two early phases (`lc_pre_ergo` n=19; `pacing_pre_citalopram_learning` n=12) together contribute 31 of 314 episode-ends (9.9%); the two late phases (`pacing_habit_established` + `citalopram_modulated`) contribute 283 of 314 (90.1%). MD-alpha §3.3 sample-size warning is confirmed: early-phase per-window strict-clean sub-samples will drop further from these already-small pools; per-window per-pool floors reported at §5 below.

---

## 3. Intensity × phase cross-tab (MD-alpha §7.2 / §6.3)

Reproduces MD-alpha §6.3 exact drafted-time cross-tab. Intensity read on the episode-end day itself (last-day class) per MD-alpha §6.3. Source: [`output/phase_intensity_crosstab.csv`](output/phase_intensity_crosstab.csv).

| Intensity (last-day class) \ Phase | `lc_pre_ergo` | `pacing_pre_citalopram_learning` | `pacing_habit_established` | `citalopram_modulated` | **All** |
|---|---:|---:|---:|---:|---:|
| `heavy` | **8** | **4** | **70** | **83** | **165** |
| `very_heavy` | **11** | **8** | **55** | **75** | **149** |
| **All** | **19** | **12** | **125** | **158** | **314** |

**Reproduction verification**: MATCH across all 8 interior cells + row totals + column totals + grand total. MD-alpha §6.3 cross-tab confirmed byte-identical against this audit's fresh probe. No divergence.

**Read** (verbatim from MD-alpha §6.3 with this audit's named counts): intensity distribution across phases is roughly balanced. `heavy` fraction per phase -- `lc_pre_ergo`: 8/19 = 42.1%; `pacing_pre_citalopram_learning`: 4/12 = 33.3%; `pacing_habit_established`: 70/125 = 56.0%; `citalopram_modulated`: 83/158 = 52.5%. No phase is dominated by a single intensity class; the intensity-stratified arm (MD-alpha §4) does NOT structurally cluster into specific phases.

**Structural clustering check**: for a phase × intensity double-stratification (out of primary scope per MD-alpha §5 cross-arc consistency note but bounded for downstream reference):

| Cell | n | Below n<10 floor? |
|---|---:|---|
| `lc_pre_ergo` × `heavy` | 8 | Yes |
| `lc_pre_ergo` × `very_heavy` | 11 | No |
| `pacing_pre_citalopram_learning` × `heavy` | 4 | Yes |
| `pacing_pre_citalopram_learning` × `very_heavy` | 8 | Yes |
| `pacing_habit_established` × `heavy` | 70 | No |
| `pacing_habit_established` × `very_heavy` | 55 | No |
| `citalopram_modulated` × `heavy` | 83 | No |
| `citalopram_modulated` × `very_heavy` | 75 | No |

**Stage D disposition**: a phase × intensity double-stratification at Stage D would require narrative-only reads on 3 of 8 cells (`lc_pre_ergo` × `heavy`, both `pacing_pre_citalopram_learning` cells) before any window / overlap / pool filters bite. MD-alpha §5 already flags this as out of primary scope; this audit confirms the sample-size case for keeping the two stratification axes separate.

---

## 4. Per-outcome × per-phase × per-k coverage (MD-alpha §7.3)

MD-alpha §7.3 asks for per-outcome per-phase per-k coverage across k = 0..10. Full table at [`output/phase_per_outcome_coverage.csv`](output/phase_per_outcome_coverage.csv) (176 rows: 4 phases × 4 outcomes × 11 k-values); condensed read below.

**Coverage discipline**: cells report n_episode_ends with a non-null value on the outcome column at day+k. NaN = missing / uninstrumented; not zero-imputed per [CONVENTIONS §5 zero-vs-NaN](../../../CONVENTIONS.md#5-anchors-and-defaults). Explicit NaN column reported in the CSV alongside n_valid so the ratio can be recomputed at read time.

### 4.1 Episode-end-day coverage (k=0)

Verifies MD-alpha §7.3 drafted-time probe: 100% coverage on all 4 activity outcomes on episode-end days across all 4 phases.

| Phase | n episode-ends | `total_steps` valid | `effective_exertion_min` valid | `vigorous_min` valid | `active_min` valid |
|---|---:|---:|---:|---:|---:|
| `lc_pre_ergo` | 19 | 19 (100%) | 19 (100%) | 19 (100%) | 19 (100%) |
| `pacing_pre_citalopram_learning` | 12 | 12 (100%) | 12 (100%) | 12 (100%) | 12 (100%) |
| `pacing_habit_established` | 125 | 125 (100%) | 125 (100%) | 125 (100%) | 125 (100%) |
| `citalopram_modulated` | 158 | 158 (100%) | 158 (100%) | 158 (100%) | 158 (100%) |

Reproduction verification: MATCH. MD-alpha §7.3 100% k=0 coverage claim confirmed.

### 4.2 Extended-window coverage (k=1..10) -- attrition read

Coverage attrition across k=1..10 by phase and outcome:

**`total_steps`**:

| Phase | k=0 | k=1 | k=3 | k=5 | k=10 | Min over k=0..10 |
|---|---:|---:|---:|---:|---:|---:|
| `lc_pre_ergo` | 19 | 18 | 18 | 16 | 16 | 16 (84.2% of 19) |
| `pacing_pre_citalopram_learning` | 12 | 12 | 12 | 12 | 11 | 11 (91.7% of 12) |
| `pacing_habit_established` | 125 | 125 | 125 | 125 | 125 | 125 (100%) |
| `citalopram_modulated` | 158 | 156 | 156 | 155 | 154 | 154 (97.5% of 158) |

**`effective_exertion_min`**:

| Phase | k=0 | k=1 | k=3 | k=5 | k=10 | Min over k=0..10 |
|---|---:|---:|---:|---:|---:|---:|
| `lc_pre_ergo` | 19 | 19 | 19 | 19 | 19 | 19 (100%) |
| `pacing_pre_citalopram_learning` | 12 | 12 | 12 | 12 | 12 | 12 (100%) |
| `pacing_habit_established` | 125 | 125 | 125 | 125 | 125 | 125 (100%) |
| `citalopram_modulated` | 158 | 158 | 158 | 158 | 157 | 157 (99.4% of 158) |

**`vigorous_min`**:

| Phase | k=0 | k=1 | k=3 | k=5 | k=10 | Min over k=0..10 |
|---|---:|---:|---:|---:|---:|---:|
| `lc_pre_ergo` | 19 | 18 | 18 | 16 | 16 | 16 (84.2% of 19) |
| `pacing_pre_citalopram_learning` | 12 | 12 | 12 | 12 | 11 | 11 (91.7% of 12) |
| `pacing_habit_established` | 125 | 125 | 125 | 125 | 125 | 125 (100%) |
| `citalopram_modulated` | 158 | 157 | 156 | 155 | 155 | 154 (97.5% of 158) |

**`active_min`** (`active_sec / 60`):

| Phase | k=0 | k=1 | k=3 | k=5 | k=10 | Min over k=0..10 |
|---|---:|---:|---:|---:|---:|---:|
| `lc_pre_ergo` | 19 | 18 | 18 | 16 | 16 | 16 (84.2% of 19) |
| `pacing_pre_citalopram_learning` | 12 | 12 | 12 | 12 | 11 | 11 (91.7% of 12) |
| `pacing_habit_established` | 125 | 125 | 125 | 125 | 125 | 125 (100%) |
| `citalopram_modulated` | 158 | 157 | 156 | 155 | 155 | 154 (97.5% of 158) |

**Read**: `effective_exertion_min` has the strongest coverage across all phases; the other three activity outcomes have identical coverage to each other (source: shared Garmin daily-summary bootstrap) and drop 0-3 episode-ends per phase over the k=0..10 window. `lc_pre_ergo` shows the largest per-episode attrition on the non-effective-exertion outcomes (16/19 = 84.2%); `citalopram_modulated` next (154-155/158 = 97.5%). Attrition NEVER pushes any (phase, outcome, k) cell below the n < 5 summary-statistic drop rule (parent MD §7.10 practice); all cells remain n ≥ 11 at every k in every phase across every outcome.

**Named counts** per [CONVENTIONS §3.6](../../../CONVENTIONS.md#36-named-counts): scheme = "n episode-ends with non-null outcome value at exactly day+k after gap=0 episode-end day"; unit = episode-ends; source = [`output/phase_per_outcome_coverage.csv`](output/phase_per_outcome_coverage.csv).

---

## 5. Per-phase × per-window × per-overlap × per-pool sample floors (MD-alpha §7.5) -- key new content

MD-alpha §7.5 defers the full per-contrast cell n table to Stage -1. This section reports **all 48 cells** (4 phases × 3 windows × 2 overlaps × 2 pools) after applying strict-clean overlap filter (parent §5.2) + compensatory-success/failure pool filter (parent §3.5). Detrended-arm additional filter is reported separately at §6 below.

**Sample-size discipline reference**: parent MD §7.10 + parent Stage -1 audit §7 orchestrator disposition -- cells with n < 10 emit descriptively without bootstrap CIs. Every cell below is flagged against that floor.

Full table at [`output/phase_strict_clean_pool_floors.csv`](output/phase_strict_clean_pool_floors.csv). Panels reordered here by (window, overlap, pool) for reader-scanning.

### 5.1 Window +3d

| Phase | strict_clean × success | strict_clean × failure | inclusive × success | inclusive × failure |
|---|---:|---:|---:|---:|
| `lc_pre_ergo` | **6** (below) | **2** (below) | 16 | **3** (below) |
| `pacing_pre_citalopram_learning` | **3** (below) | **1** (below) | 11 | **1** (below) |
| `pacing_habit_established` | 41 | **8** (below) | 106 | 19 |
| `citalopram_modulated` | 59 | **5** (below) | 147 | 11 |

### 5.2 Window +5d

| Phase | strict_clean × success | strict_clean × failure | inclusive × success | inclusive × failure |
|---|---:|---:|---:|---:|
| `lc_pre_ergo` | **4** (below) | **1** (below) | 16 | **3** (below) |
| `pacing_pre_citalopram_learning` | **2** (below) | **0** (below) | 11 | **1** (below) |
| `pacing_habit_established` | 11 | **6** (below) | 100 | 25 |
| `citalopram_modulated` | 26 | **2** (below) | 141 | 17 |

### 5.3 Window +10d

| Phase | strict_clean × success | strict_clean × failure | inclusive × success | inclusive × failure |
|---|---:|---:|---:|---:|
| `lc_pre_ergo` | **1** (below) | **0** (below) | 14 | **5** (below) |
| `pacing_pre_citalopram_learning` | **0** (below) | **0** (below) | 10 | **2** (below) |
| `pacing_habit_established` | **1** (below) | **1** (below) | 88 | 37 |
| `citalopram_modulated` | **8** (below) | **0** (below) | 133 | 24 |

### 5.4 Sample-floor headline

Of 4 phases × 3 windows × 2 overlaps × 2 pools = **48 cells total**:

- **Below n < 10 descriptive floor**: **26 / 48 = 54.2%** of cells
- **At or above n ≥ 10 floor**: **22 / 48 = 45.8%** of cells

Per-phase breakdown of below-floor cells:

| Phase | Below-floor cells / 12 | Above-floor cells / 12 |
|---|---:|---:|
| `lc_pre_ergo` | 9 / 12 | 3 / 12 |
| `pacing_pre_citalopram_learning` | 9 / 12 | 3 / 12 |
| `pacing_habit_established` | 4 / 12 | 8 / 12 |
| `citalopram_modulated` | 4 / 12 | 8 / 12 |

**Per-cell design implications for Stage D readers**:

1. **Compensatory-success × strict-clean × +3d** (the primary contrast per MD-alpha §3.3 headline): 4 phases → cells at 6, 3, 41, 59. Early two phases fall below the n<10 floor; late two phases support bootstrap-CI reads comfortably. Cross-phase AUC contrast (§3.3 late-vs-early pair contrast) reads at +3d strict-clean success are **early-phase-descriptive-only, late-phase-bootstrap-CI-usable**. Per MD-alpha §6.4 sample-size confound + this audit §5.1: early-phase per-window trajectory panels at strict-clean +3d success go through as descriptive-only, not narrative-only (n=6 and n=3 are small but non-zero and support the parent MD §7.10 "descriptive without bootstrap CIs" tier).

2. **Compensatory-success × strict-clean × +5d**: 4, 2, 11, 26. Only `pacing_habit_established` and `citalopram_modulated` clear the floor; `pacing_pre_citalopram_learning` at n=2 sits at the boundary between descriptive and narrative-only per parent Stage -1 audit §5 "narrative only" threshold (n ≤ 5). `lc_pre_ergo` at n=4 also narrative-only-adjacent.

3. **Compensatory-success × strict-clean × +10d**: 1, 0, 1, 8. **All four phases below floor**; `pacing_pre_citalopram_learning` at n=0 has zero strict-clean success episodes at +10d. Late-phase 10d strict-clean reads are structurally unavailable for the phase-stratified arc; MD-alpha §6.4 flagged this at ~10 estimate for `citalopram_modulated` (actual: n=8) and viable only combined-late-phases (`pacing_habit_established` + `citalopram_modulated` = n=9 combined, still below floor).

4. **Compensatory-failure sub-arm** (parent §3.5 side-arm): 15 of 24 compensatory-failure cells are below floor. Late-phase strict-clean × failure hits floor at all windows for both `pacing_habit_established` and `citalopram_modulated` (except `pacing_habit_established` × +3d at n=8, just below). The failure sub-arm at Stage D reports descriptively per parent §3.5 + Stage D audit §10 item 1 orchestrator disposition; this audit confirms the sample-size case for the "descriptive without bootstrap CIs" tier applying to every failure cell across every phase and window and overlap policy.

5. **Inclusive-policy success cells** are the only tier that survives the floor across all four phases at all three windows (16, 11, 106, 147 at +3d; 16, 11, 100, 141 at +5d; 14, 10, 88, 133 at +10d -- all ≥ 10). MD-alpha §5 "both strict + inclusive reported side-by-side" is directly load-bearing: at +5d and +10d the inclusive policy is the only reader with all four phases at the bootstrap-CI floor. Divergence between strict-clean and inclusive readings on the two late phases is a Stage D discipline requirement per parent §5.2.

**Structurally-unavailable cells** (n = 0):

- `pacing_pre_citalopram_learning` × strict_clean × +5d × failure (n=0)
- `pacing_pre_citalopram_learning` × strict_clean × +10d × success (n=0)
- `pacing_pre_citalopram_learning` × strict_clean × +10d × failure (n=0)
- `lc_pre_ergo` × strict_clean × +10d × failure (n=0)
- `citalopram_modulated` × strict_clean × +10d × failure (n=0)

Five cells have zero episodes surviving the filters. These are not-reportable at Stage D; they will appear as `NaN` panels in Stage D output per [CONVENTIONS §5 zero-vs-NaN](../../../CONVENTIONS.md#5-anchors-and-defaults) -- never zero-imputed.

**Named counts** per [CONVENTIONS §3.6](../../../CONVENTIONS.md#36-named-counts): scheme = "n episode-ends surviving (strict-clean = no other combined-heavy in [+1, +w] OR inclusive = no filter) + (compensatory-success = no crash in [+1, +w] OR compensatory-failure = crash in [+1, +w]) filters, gated on phase membership at episode-end day"; unit = episode-ends; source = [`output/phase_strict_clean_pool_floors.csv`](output/phase_strict_clean_pool_floors.csv).

---

## 6. Per-phase detrended-arm sample floors (MD-alpha §7.5 detrend clause)

Parent MD §7.11 pre-commits detrend arm eligibility: an episode retains detrended-arm read only if its 30-day pre-window has ≥15 valid data points on the outcome column. This audit probes the eligibility rule per (phase, outcome).

Full table at [`output/phase_detrended_arm_floors.csv`](output/phase_detrended_arm_floors.csv).

| Phase | Outcome | n episode-ends | n detrend-eligible | n detrend-dropped |
|---|---|---:|---:|---:|
| `lc_pre_ergo` | `total_steps` | 19 | 19 | 0 |
| `lc_pre_ergo` | `effective_exertion_min` | 19 | 19 | 0 |
| `lc_pre_ergo` | `vigorous_min` | 19 | 19 | 0 |
| `lc_pre_ergo` | `active_min` | 19 | 19 | 0 |
| `pacing_pre_citalopram_learning` | `total_steps` | 12 | 12 | 0 |
| `pacing_pre_citalopram_learning` | `effective_exertion_min` | 12 | 12 | 0 |
| `pacing_pre_citalopram_learning` | `vigorous_min` | 12 | 12 | 0 |
| `pacing_pre_citalopram_learning` | `active_min` | 12 | 12 | 0 |
| `pacing_habit_established` | `total_steps` | 125 | 125 | 0 |
| `pacing_habit_established` | `effective_exertion_min` | 125 | 125 | 0 |
| `pacing_habit_established` | `vigorous_min` | 125 | 125 | 0 |
| `pacing_habit_established` | `active_min` | 125 | 125 | 0 |
| `citalopram_modulated` | `total_steps` | 158 | 158 | 0 |
| `citalopram_modulated` | `effective_exertion_min` | 158 | 158 | 0 |
| `citalopram_modulated` | `vigorous_min` | 158 | 158 | 0 |
| `citalopram_modulated` | `active_min` | 158 | 158 | 0 |

**Read**: **Zero episodes drop from the detrended-arm eligibility rule across every phase × outcome cell.** The 30-day pre-windows on activity outcomes are dense enough on this corpus that no episode-end fails the ≥15-valid-point threshold on any activity axis. This is a favourable finding for Stage D executors: the detrended-arm sample size equals the raw-arm sample size at every phase and every outcome. Whatever sample-size compression happens at §5 (strict-clean + pool filters) applies identically to raw and detrended arms; no additional per-outcome per-phase detrend-drop needs to be modelled.

**Caveat 1 (coverage-only claim, added at r1 lock post-review absorption per L2.1 stationarity fire)**: the 0-drop finding certifies the ≥15-valid-point **coverage** rule doesn't bite; it does NOT certify the linear-fit **stationarity assumption** underlying parent MD §7.11 `linear_detrend_on_pre` per Daza 2018 §3 n-of-1 stationarity discipline. §8 below shows a monotone `total_steps` pre-window mean decline of ~26% across the four ordered phases (6480 → 4816). A per-episode linear detrend on a pre-window sitting inside a monotone corpus-level drift may absorb some of that drift into the fit's slope, which is precisely what §7.11 wants — but the assumption that the drift is **linear** within each 30-day pre-window (adequate for extrapolation into the post-window) is a stationarity-of-slope assumption not tested by the 15-point coverage rule. Stage D reviewers should treat the detrended-arm read as inheriting §8's level-vs-change discipline: the detrend removes smooth drift but does not disambiguate nuisance-drift from pacing-learning-drift per MD-α §3.5 rescue-metric discipline.

**Caveat 2 (boundary edge case)**: this ≥15-valid-point rule is applied on the outcome column only. Per-episode 30d pre-windows near the LC-era start date (2022-04-04) have shorter available pre-window depth -- episode-ends within the first 30 days of the LC-era have pre-window truncated to `max(0, end - 30)` in the script (see `pre_window_levels` and `detrended_arm_floors` implementations). No episode-end in the four phases has a pre-window shorter than 15 days in the corpus (verified: even the earliest `lc_pre_ergo` episode-ends sit well past 30 days into the LC-era corpus).

**Named counts** per [CONVENTIONS §3.6](../../../CONVENTIONS.md#36-named-counts): scheme = "n episode-ends whose 30-day pre-window contains at least 15 non-null values on the outcome column"; unit = episode-ends; source = [`output/phase_detrended_arm_floors.csv`](output/phase_detrended_arm_floors.csv).

---

## 7. Per-intensity-stratum sample floors (MD-alpha §7.4)

MD-alpha §7.4 defers per-intensity-stratum per-outcome coverage to Stage -1. Reports per (intensity_stratum × outcome × k=0..10) valid-count. Full table at [`output/intensity_stratum_per_outcome_coverage.csv`](output/intensity_stratum_per_outcome_coverage.csv).

Condensed (k=0, k=3, k=5, k=10; min over k=0..10):

| Stratum | n stratum ends | Outcome | k=0 | k=3 | k=5 | k=10 | Min |
|---|---:|---|---:|---:|---:|---:|---:|
| `combined` | 314 | `total_steps` | 314 | 311 | 308 | 306 | 306 |
| `combined` | 314 | `effective_exertion_min` | 314 | 314 | 314 | 313 | 313 |
| `combined` | 314 | `vigorous_min` | 314 | 311 | 308 | 307 | 306 |
| `combined` | 314 | `active_min` | 314 | 311 | 308 | 307 | 306 |
| `heavy_only` | 165 | `total_steps` | 165 | 163 | 161 | 162 | 160 |
| `heavy_only` | 165 | `effective_exertion_min` | 165 | 165 | 165 | 164 | 164 |
| `heavy_only` | 165 | `vigorous_min` | 165 | 163 | 161 | 162 | 160 |
| `heavy_only` | 165 | `active_min` | 165 | 163 | 161 | 162 | 160 |
| `very_heavy_only` | 149 | `total_steps` | 149 | 148 | 147 | 144 | 144 |
| `very_heavy_only` | 149 | `effective_exertion_min` | 149 | 149 | 149 | 149 | 149 |
| `very_heavy_only` | 149 | `vigorous_min` | 149 | 148 | 147 | 145 | 145 |
| `very_heavy_only` | 149 | `active_min` | 149 | 148 | 147 | 145 | 145 |

**Read**: coverage across k=0..10 is uniformly high across all three intensity strata. No stratum × outcome × k cell drops below n=144 (which is 96.6% of the very_heavy_only stratum ends). All three intensity strata support the parent MD §9.2 read policy at +3d (combined n=306+, heavy_only n=160+, very_heavy_only n=144+) before overlap or pool filters.

**Overlap discipline**: this section reports coverage on episode-ends without overlap filter. Parent Stage -1 audit §5 already reports per-intensity strict-clean overlap density: `very_heavy` cross-scanned against `combined` at +3d gives n=52 clean; at +5d n=19; at +10d n=5. `heavy_only` cross-scanned against `combined` at +3d gives n=73 clean; at +5d n=33; at +10d n=7. This audit does NOT re-derive those cross-stratum overlap counts; refer to parent Stage -1 audit §5 cross-stratum table for the strict-clean intensity-stratified read.

**Named counts** per [CONVENTIONS §3.6](../../../CONVENTIONS.md#36-named-counts): scheme = "n episode-ends in intensity stratum (by last-day class) with non-null outcome value at exactly day+k"; unit = episode-ends; source = [`output/intensity_stratum_per_outcome_coverage.csv`](output/intensity_stratum_per_outcome_coverage.csv).

---

## 8. Per-phase pre-window mean-level table (MD-alpha §3.5 level-vs-change discipline)

MD-alpha §3.5 requires per-phase pre-window mean levels reported alongside AUC magnitudes so level-vs-change disagreements are readable at Stage D. This audit reports the pre-window (30-day) mean and median per (phase × outcome), aggregated across episode-ends in each phase.

Full table at [`output/phase_pre_window_levels.csv`](output/phase_pre_window_levels.csv).

**`total_steps`** (units: steps / day):

| Phase | n episodes | n with valid pre-window | pre-window mean | pre-window median |
|---|---:|---:|---:|---:|
| `lc_pre_ergo` | 19 | 19 | 6480 | 5885 |
| `pacing_pre_citalopram_learning` | 12 | 12 | 5500 | 5607 |
| `pacing_habit_established` | 125 | 125 | 5174 | 5143 |
| `citalopram_modulated` | 158 | 158 | 4816 | 4625 |

**`effective_exertion_min`** (units: minutes / day):

| Phase | n episodes | n with valid pre-window | pre-window mean | pre-window median |
|---|---:|---:|---:|---:|
| `lc_pre_ergo` | 19 | 19 | 9.50 | 8.92 |
| `pacing_pre_citalopram_learning` | 12 | 12 | 27.78 | 28.42 |
| `pacing_habit_established` | 125 | 125 | 19.39 | 19.29 |
| `citalopram_modulated` | 158 | 158 | 5.17 | 4.57 |

**`vigorous_min`** (units: minutes / day):

| Phase | n episodes | n with valid pre-window | pre-window mean | pre-window median |
|---|---:|---:|---:|---:|
| `lc_pre_ergo` | 19 | 19 | 2.17 | 1.63 |
| `pacing_pre_citalopram_learning` | 12 | 12 | 0.58 | 0.61 |
| `pacing_habit_established` | 125 | 125 | 1.25 | 1.07 |
| `citalopram_modulated` | 158 | 158 | 1.04 | 0.97 |

**`active_min`** (units: minutes / day, `active_sec / 60`):

| Phase | n episodes | n with valid pre-window | pre-window mean | pre-window median |
|---|---:|---:|---:|---:|
| `lc_pre_ergo` | 19 | 19 | 117.91 | 109.43 |
| `pacing_pre_citalopram_learning` | 12 | 12 | 92.98 | 94.29 |
| `pacing_habit_established` | 125 | 125 | 93.16 | 93.31 |
| `citalopram_modulated` | 158 | 158 | 91.43 | 88.56 |

**Read** (descriptive only, no inference per [CONVENTIONS §2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)):

1. **`total_steps` shows a monotone declining pre-window mean across the four ordered phases** (6480 → 5500 → 5174 → 4816). This is consistent with an absolute-load-envelope shift over the LC-era corpus. Level-vs-change discipline (MD-alpha §3.5): if a phase-stratified AUC contrast on `total_steps` shows late-phase strengthening, the reader must consider whether the per-phase absolute activity envelope shifted (measured here) as a co-driver of the AUC delta shape rather than a compensatory-behaviour improvement alone. Not a caveat rebuttal -- a discipline requirement.

2. **`effective_exertion_min` shows a non-monotone pre-window mean across phases** (9.50 → 27.78 → 19.39 → 5.17). The `pacing_pre_citalopram_learning` phase has the HIGHEST pre-window `effective_exertion_min` (27.78 min/day), well above the other three phases. `lc_pre_ergo` at 9.50 sits below `pacing_habit_established` (19.39) which sits well above `citalopram_modulated` (5.17). This is a load-bearing level-vs-change disagreement signal for the phase-stratified arc on `effective_exertion_min`: any per-phase AUC contrast on this outcome will be interpretable against very different per-phase absolute-level baselines, not against a stationary baseline. This finding is consistent with the parent Stage D audit §6.4.1 `effective_exertion_min` +3d success sign-flipper being a corpus-level level-vs-change disagreement -- that ~55% pre-window baseline gap between arms may itself vary sharply across phases.

3. **`vigorous_min` and `active_min` show relatively stable pre-window means across phases** (`vigorous_min` range 0.58-2.17; `active_min` range 91-118). `lc_pre_ergo` sits at the top for both (2.17 min vigorous, 118 min active); the three post-`lc_pre_ergo` phases cluster tightly. `pacing_pre_citalopram_learning` sits at the bottom for `vigorous_min` (0.58) while sitting at the top for `effective_exertion_min` (27.78) -- the two outcome columns are decoupled at this phase, an axis-composition artefact that the parent Stage -1 audit §3 "multi-axis heavy-day composition" caveat 2 flags as expected under the composite operand.

**Discipline for Stage D readers**: per MD-alpha §3.5 "report per-phase pre-window mean levels alongside AUC magnitudes; do not silently compress". Stage D output should include this table as a companion to any per-phase AUC contrast. Do NOT interpret a monotone `total_steps` AUC-magnitude trend across phases as pacing-learning without acknowledging the parallel monotone pre-window `total_steps` mean-level decline -- the two are dimensionally coupled through the AUC operand's dependence on absolute activity envelope.

**Named counts** per [CONVENTIONS §3.6](../../../CONVENTIONS.md#36-named-counts): scheme = "arithmetic mean of per-episode 30d pre-window mean value on the outcome column, averaged across episode-ends in the phase"; unit varies per outcome (see column headers); source = [`output/phase_pre_window_levels.csv`](output/phase_pre_window_levels.csv).

---

## 9. Findings summary and Stage D readiness assessment

### 9.1 Reproduction verification (MD-alpha §7.1 + §7.2)

- **§7.1 phase-episode-end counts**: reproduced byte-identically from MD-alpha §3.1 drafted-time probe (19 / 12 / 125 / 158 / 314). MATCH.
- **§7.2 intensity × phase cross-tab**: reproduced byte-identically from MD-alpha §6.3 drafted-time probe (heavy: 8 / 4 / 70 / 83 = 165; very_heavy: 11 / 8 / 55 / 75 = 149; totals per phase 19 / 12 / 125 / 158; grand total 314). MATCH.

No divergence between MD-alpha LOCKED r1 probes and this Stage -1 audit. MD-alpha operand definition confirmed data-well-formed on the CSV state as of 2026-07-16.

### 9.2 Stage D cell viability tiers (per MD-alpha §6.4 sample-size discipline)

Applying parent MD §7.10 orchestrator disposition + parent Stage -1 audit §5 viable-descriptive-floor terminology:

**Bootstrap-CI-viable cells** (n ≥ 10, both raw + detrended per §6): 22 / 48 phase × window × overlap × pool cells. Distribution:
- All 12 inclusive × success cells (all 4 phases × 3 windows)
- All 4 late-phase strict-clean × success cells at +3d and +5d (n=41, 59, 11, 26)
- 6 late-phase inclusive × failure cells (`pacing_habit_established` at all 3 windows: 19, 25, 37; `citalopram_modulated` at all 3 windows: 11, 17, 24)

**Descriptive-only-viable cells** (5 ≤ n < 10, per parent Stage -1 audit §5 threshold): **6 cells**.
- `lc_pre_ergo` × +3d × strict × success (6), × +3d × inclusive × success (16 → above, listed under bootstrap-CI-viable)
- `citalopram_modulated` × +3d × strict × failure (5)
- `citalopram_modulated` × +10d × strict × success (8)
- `pacing_habit_established` × +3d × strict × failure (8)
- `pacing_habit_established` × +5d × strict × failure (6) -- **added at r1 lock post-review absorption; missing from r1 draft list per fresh-session reviewer L1.2 off-by-one fire against `phase_strict_clean_pool_floors.csv`**
- `lc_pre_ergo` × +10d × inclusive × failure (5)

**Narrative-only-viable cells** (1 ≤ n ≤ 4, per parent Stage -1 audit §5 threshold): 15 cells (most of the early-phase strict-clean cells + late-phase strict-clean × failure cells except the 5 or 8 counts above).

**Structurally unavailable cells** (n = 0): 5 cells as listed in §5.4 above (all involving `pacing_pre_citalopram_learning` at extended windows or strict-clean × failure at various phases at +10d).

**Overall Stage D readiness**: MD-alpha §3.3 primary contrast at +3d strict-clean × success is bootstrap-CI-viable for both late phases and descriptive-with-CI-or-narrative for both early phases. **The MD-alpha §3.3 headline "cross-phase AUC contrast between late-pair and early-pair" is executable at Stage D at the +3d window with the discipline mix flagged in §5.1 above.** At +5d, only the two late phases support the contrast; at +10d, only the inclusive-policy panel supports all four phases. This is consistent with MD-alpha §6.4 sample-size confound pre-commit.

### 9.3 MD-alpha §3.5 rescue-metric computability

MD-alpha §3.5 rescue metric = Spearman ρ of |AUC| across the 4-phase ordinal axis + monotonicity-score companion. Computability requires:

- **Per-phase |AUC| value at the tested cell must be non-NaN across all 4 phases** (else Spearman ρ is undefined on N=4).
- **Per-phase |AUC| CIs may be wide on n ≤ 10 cells** -- MD-alpha §3.5 explicitly acknowledges that "wide CIs on early-phase per-phase |AUC| may inflate rank instability".

Given §5.1's tier distribution, the rescue metric is directly computable on any cell that has non-NaN per-phase |AUC| across all four phases. Under strict-clean × success × +3d, all four phase-cells have n ≥ 3, so |AUC| is computable in every phase (descriptive-only for the two early phases). Under strict-clean × success × +5d, `pacing_pre_citalopram_learning` sits at n=2 (below the "narrative-only" n ≤ 4 tier per parent Stage -1 audit §5 usage but non-zero -- |AUC| is technically computable with a 2-observation mean). Under strict-clean × success × +10d, `pacing_pre_citalopram_learning` sits at n=0 -- Spearman ρ is UNDEFINED for +10d strict-clean success cells (one of the four phase-cells is NaN).

**Recommended MD-alpha §3.5 rescue-metric application windows**: +3d strict-clean × success and +5d strict-clean × success (with wide-CI acknowledgement for the two early phases at +5d), and +3d inclusive × success as the sample-large sensitivity. NOT computable at +10d strict-clean × success. Inclusive-policy cells at all windows are computable across all 4 phases.

### 9.4 Level-vs-change disagreement signal (§8 finding)

`total_steps` shows a monotone decline in pre-window mean across the four phases (6480 → 5500 → 5174 → 4816); `effective_exertion_min` shows non-monotone variation with `pacing_pre_citalopram_learning` at the top (27.78 min/day). Both are load-bearing for Stage D interpretation:

- A monotone `total_steps` AUC-magnitude trend across phases cannot be attributed to compensatory-behaviour improvement alone without accounting for the parallel monotone absolute-envelope decline. This is the MD-alpha §3.5 level-vs-change discipline in action; report the pre-window mean panel alongside the AUC panel per §8 above.
- An `effective_exertion_min` phase-stratified AUC contrast will confront the non-monotone per-phase pre-window baseline; `pacing_pre_citalopram_learning`'s outlier baseline (27.78) means any AUC-magnitude computed for that phase reads against a very different absolute-level context than the other three phases.

Neither finding is a caveat rebuttal -- both are Stage D read-discipline requirements per [CONVENTIONS §2.1](../../../CONVENTIONS.md#21-descriptive-before-inference) + [§4.2 caveats-yes-a-priori-claims-no](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no).

### 9.5 Detrended-arm parity (§6 finding)

Zero episodes drop from the detrended-arm eligibility rule across every phase × outcome cell (16 cells; 0 drops). The parent MD §7.11 ≥15-valid-pre-window-point rule does not bind on this corpus for activity outcomes; detrended-arm sample sizes equal raw-arm sample sizes at every phase × outcome combination. Whatever sample-size compression happens at §5 (strict-clean + pool filters) applies identically to both arms.

### 9.6 What does NOT fire

- **Detrend-eligibility drop-rate concern** -- 0 drops across all 16 phase × outcome cells; not a bottleneck. Stage D detrended-arm reads are not further sample-compressed beyond the raw-arm compression already reported at §5.
- **Coverage attrition across k=0..10** -- worst case is 84.2% (`lc_pre_ergo` on non-effective-exertion outcomes at some k values); never drops below n=11 in any (phase, outcome, k) cell; not a bottleneck.
- **Data-quality flag on episode-end-day coverage** -- all 314 combined episode-ends have full k=0 coverage on all 4 activity outcomes; not a data-quality concern.
- **Phase × intensity structural clustering** -- intensity distribution roughly balanced across phases per §3; not a structural clustering concern for the MD-alpha §4 intensity-stratified arm.

### 9.7 Surfaced concerns for a reviewer to walk

1. **Structurally unavailable cells (n = 0)**: 5 cells across the 48-cell grid have zero episodes. Stage D output MUST emit NaN for these cells per CONVENTIONS §5 zero-vs-NaN, not zero. Verify at Stage D drafting that panels handle NaN gracefully rather than silently omitting.

2. **`pacing_pre_citalopram_learning` cell size**: at n=12 combined episode-ends, this phase sits at the boundary of every viability tier. Its strict-clean × +5d × success has n=2 (narrative-only); at +10d n=0 (unavailable); at +3d strict × success n=3 (narrative-only). Stage D readers should treat any `pacing_pre_citalopram_learning` cell result with caution independent of the MD-alpha §3.4 direction pre-commit -- the phase is small enough that any single episode is highly leveraged. MD-alpha §6.4 already flags this at ~2 estimate at +5d; this audit confirms it at n=2 actual.

3. **Level-vs-change confound on `total_steps` monotone pre-window mean decline** (§8 finding, §9.4 discipline): a monotone AUC-magnitude trend on `total_steps` across phases cannot be interpreted as pacing-learning alone without acknowledging the parallel monotone pre-window absolute-level decline. This joins MD-alpha §3.6 fifth-confound tactical-Garmin-use as a "phase-stratified label bundles multiple things" pre-commit; Stage D reading discipline requires the pre-window mean panel to accompany any AUC panel per §8 above.

4. **`effective_exertion_min` non-monotone pre-window baseline**: `pacing_pre_citalopram_learning`'s outlier at 27.78 min/day (vs. 5-19 elsewhere) means the phase-stratified `effective_exertion_min` AUC contrast reads across very different absolute-level contexts per phase. This is a per-phase level-vs-change disagreement (parallel to the parent Stage D audit §6.4.1 corpus-level level-vs-change disagreement on the same outcome), not resolvable by design at this MD level. Flag for reviewer sanity: is this an axis-composition artefact of the multi-axis heavy-day definition (parent Stage -1 audit §3 caveat 2), or a substantive activity-envelope shift specific to the ~2-month `pacing_pre_citalopram_learning` phase?

    **Favourable evidence-in-hand (added at r1 lock post-review absorption per L4.1 fire)**: §8 `effective_exertion_min` table shows pre-window mean 27.78 vs pre-window median 28.42 on `pacing_pre_citalopram_learning`. The mean-median convergence (mean sits below median by 0.64 min/day = 2.3% of median) rules out small-n mean-inflation from a small number of outlier days at the top of the distribution — if the elevation were driven by 1-2 anomalous high-exertion days on the n=12 pool, the mean would sit substantially ABOVE the median. Instead the mean sits slightly below the median, consistent with a symmetric or left-skewed pre-window distribution centred at ~28 min/day. Reading: the outlier is a **substantive activity-envelope shift** specific to this ~2-month phase, not a small-n mean-inflation artefact. Whether the shift reflects the multi-axis composite pattern (parent Stage -1 audit §3 caveat 2) or a real physiological change over the phase is still open, but the small-n-mean-inflation reading is ruled out.

5. **Detrend-arm 0-drop finding at boundary edge cases**: the ≥15-valid-point rule was applied against a `pre_start = max(0, end_idx - 30)` boundary handling that truncates pre-windows for episode-ends near the LC-era start date. No `lc_pre_ergo` episode-end sits within 30 days of the LC-era start (verified by phase-membership pattern), so no episode-end has truncated pre-window in this corpus. If future LC-era data pushes the corpus boundary or if the pre-window depth changes, the 0-drop finding should be re-verified.

6. **Overlap policy divergence at Stage D**: parent MD §5.2 requires strict-clean + inclusive reported side-by-side at all windows. §5 shows inclusive-policy success cells clear the n ≥ 10 floor across all four phases at all three windows, while strict-clean × success clears only at +3d and +5d for the two late phases. Divergence between strict-clean and inclusive readings is itself Stage D discipline evidence; systematic per-phase divergences are informative about within-phase heavy-day clustering intensity.

7. **Rescue-metric computability at +10d** (§9.3): MD-alpha §3.5 Spearman ρ + monotonicity-score are UNDEFINED at +10d strict-clean × success because `pacing_pre_citalopram_learning` has n=0 (|AUC| undefined). Stage D should not attempt the rescue metric at +10d strict-clean cells; the +3d and +5d strict-clean cells + all-window inclusive cells are the rescue-metric-computable subset.

---

## 10. Lock log

| version | date | change |
|---|---|---|
| r1 | 2026-07-16 | Initial draft as producer-mode Stage -1 descriptive audit extension of parent Q24 precursor audit ([`../Q24-precursor-heavy-day-structure/audit.md`](../Q24-precursor-heavy-day-structure/audit.md) LOCKED r1 2026-07-15) for MD-alpha methodology ([`../../../methodology/post_heavy_day_pacing_learning.md`](../../../methodology/post_heavy_day_pacing_learning.md) LOCKED r1 2026-07-16). Executes MD-alpha §7 data-availability audit hooks (§7.1 phase counts, §7.2 intensity × phase crosstab, §7.3 per-outcome per-phase coverage, §7.4 per-intensity coverage, §7.5 per-contrast cell n floors). Inheritance-only per parent MD §2 machinery; no re-derivation. **Reproduction verification**: MD-alpha §3.1 phase counts (19 / 12 / 125 / 158 / 314) reproduced byte-identically; MD-alpha §6.3 intensity × phase cross-tab reproduced byte-identically. **Key sample-floor finding**: 26 of 48 phase × window × overlap × pool cells fall below the parent MD §7.10 n < 10 bootstrap-CI floor. **Level-vs-change finding**: `total_steps` shows monotone pre-window mean decline across phases (6480 → 5500 → 5174 → 4816); `effective_exertion_min` shows `pacing_pre_citalopram_learning` outlier at 27.78 min/day. **Detrended-arm parity finding**: 0 episodes drop from parent MD §7.11 ≥15-valid-pre-point rule across all 16 phase × outcome cells. Fresh-session `/research-review` before lock is the peer-review discipline mirror to parent Q24 Stage -1 audit's r1 lock. **STATUS**: r1 DRAFTED 2026-07-16, awaiting reviewer walk of §9.7 surfaced concerns before lock consideration. |
| r1 LOCKED | 2026-07-16 | Fresh-session methodology review absorbed from [`../../../reviews/methodology-Q24-mdalpha-precursor-phase-intensity-2026-07-16.md`](../../../reviews/methodology-Q24-mdalpha-precursor-phase-intensity-2026-07-16.md) (verdict: DEFENSIBLE with revision; all 7 fires mechanical-clarification absorbs, no architectural change). Three surgical patches applied per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations) compression discipline. **Patch 1** (§9.2, review L1.2 substantive off-by-one): descriptive-only-viable tier updated from 5 to 6 cells with `pacing_habit_established × +5d × strict × failure (n=6)` added; annotated with r1-lock post-review-absorption note pointing at the CSV row that L1.2 identified as missing. **Patch 2** (§6, review L2.1 substantive): 0-drop detrended-arm parity finding split into Caveat 1 (coverage-only claim, does NOT certify Daza 2018 §3 n-of-1 linear-fit stationarity assumption given §8 monotone `total_steps` 26% pre-window drift across phases) + Caveat 2 (boundary edge case, unchanged); Stage D reviewers now told to treat detrended-arm read as inheriting §8's level-vs-change discipline. **Patch 3** (§9.7 item 4, review L4.1 substantive-minor): favourable-evidence-in-hand paragraph added -- `effective_exertion_min` `pacing_pre_citalopram_learning` outlier at 27.78 min/day pre-window mean vs 28.42 pre-window median → mean-median convergence (mean 0.64 below median = 2.3% of median) rules out small-n mean-inflation from a few outlier days; the outlier is a substantive activity-envelope shift specific to the ~2-month phase, not an artefact. Preserved byte-identically: §1-§5 (except §5.4 §9.2 patch), §7 per-intensity coverage tables, §8 pre-window mean-level tables, §9.1 reproduction verification, §9.3-§9.6 findings, §9.7 items 1-3, 5-7, §10 lock log r1 draft entry. **STATUS**: LOCKED r1 2026-07-16 post-review absorption. Stage D descriptive execution against this audit's per-cell sample-floor + level-vs-change discipline is now unblocked. |
