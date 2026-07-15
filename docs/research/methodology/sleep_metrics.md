# Sleep metrics — operand-catalogue for sleep-derived research constructs

*Producer-mode methodology MD per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). Drafted 2026-07-15 as r1; pending fresh-session audit per [`/research-methodology-review`](../../../.claude/commands/research-methodology-review.md) before lock.*

---

## Authorship

**Drafted 2026-07-15** by Claude (Opus 4.7) in producer-mode under user authorisation. Authorising user: Willem. Subagent-drafted as the Stage 3b documentation pass following the Stage 3a pipeline extension (2026-07-15) that landed 12 new sleep-derived columns on `per_day_master.csv` with byte-identical determinism preserved on all 205 existing columns.

**Drafting trigger**: the Q24 methodology MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) §6.2 stalled on ambiguous sleep-operand definitions (which sleep-efficiency formula? which REM operand? which BB-recovery normalisation?). This MD is the canonical operand catalogue that Q24 and future sleep-touching hypothesis MDs read; sleep-operand definitions no longer live inline in per-hypothesis MDs.

**Locked decisions at draft time** (structural, not data-driven):

1. **Catalogue scope**: five operand families (Architecture, Consistency / regularity, Composite / score, Physiological during sleep, BB overnight recovery). Every project sleep-derived operand belongs in exactly one family.
2. **PRIMARY / SENSITIVITY / DEFERRED tier system**: every operand carries a tier label. PRIMARY operands are load-bearing defaults for downstream hypothesis reads; SENSITIVITY variants are companion reads; DEFERRED are named-but-not-yet-implemented (Family B) or named-but-not-available (Family C).
3. **Definitional-pair discipline per CONVENTIONS §3.3**: pairs sharing a construct (`sleep_efficiency_tib` vs `sleep_efficiency_staged`; `stress_mean_sleep` vs `asleep_stress_avg_uds`) are documented as pairs; downstream reads pick one per analysis.
4. **Zero-vs-NaN discipline per CONVENTIONS §5**: every operand has an explicit missingness policy. No downstream `.fillna(0)` without justification at analysis time.
5. **Producer-mode discipline**: this MD does not commit to specific analyses. It names the operands that downstream hypothesis MDs consume.

**Status**: **r1 DRAFTED 2026-07-15**, awaiting fresh-session methodology review. Producer-mode artefact per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations); downstream MDs consume this catalogue only after the review verdict clears.

---

## 1. Purpose and scope

### 1.1 What this MD is

An **operand catalogue** for sleep-derived research constructs across the project. The MD locks: the family taxonomy (§4-§8), the definitional-pair reads (§4 `sleep_efficiency_*`, §7 `stress_mean_sleep` vs `asleep_stress_avg_uds`), the tier system (PRIMARY / SENSITIVITY / DEFERRED), the coverage matrix (§9), the missingness policy per operand (§10), and the downstream consumer map (§11).

### 1.2 What this MD is NOT

- **NOT a hypothesis pre-registration.** No substantive falsification criterion for any sleep-related claim is locked here; those live in per-HA pre-regs that read from this catalogue.
- **NOT a pipeline extraction spec.** The extractor scripts ([`pipeline/01_extract/garmin_sleep_extras.py`](../pipeline/01_extract/garmin_sleep_extras.py), [`pipeline/01_extract/garmin_uds_extras.py`](../pipeline/01_extract/garmin_uds_extras.py)) and the consolidator ([`pipeline/03_consolidate/build_unified_dataset.py`](../pipeline/03_consolidate/build_unified_dataset.py)) are the authoritative implementation. This MD cites them.
- **NOT a research finding.** The MD describes operand availability, not what the operands say about sleep behaviour.
- **NOT a re-derivation of DATA_DICTIONARY.md sleep rows.** DATA_DICTIONARY holds per-column row definitions; this MD holds the family taxonomy and the definitional-pair guidance a per-column row cannot carry.

### 1.3 Cross-refs into the catalogue

Downstream MDs that consume this catalogue:

- **Q24** ([`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md)): §6.2 sleep + autonomic outcome family reads a shortlist of primary + sensitivity operands defined here.
- **Future Wiggers F1** (sleep duration ↑ during PEM): candidate primary is `sleep_duration_min` (§4), sensitivity via `sleep_efficiency_tib` (§4).
- **Future Wiggers F4** (bedtime inconsistency → next-day energy): candidate primary is `bedtime_std_7d` (§5), further Family B operands DEFERRED.
- **Intervention-effects methodology** ([`intervention_effects_descriptive.md`](intervention_effects_descriptive.md)): consumes `stress_mean_sleep` (§7); other Family D operands are available additions.
- **Q24 sub-part 3** (phase-stratification, deferred): natural home for Family B (§5) once the Family B operands are implemented.

---

## 2. Data sources

### 2.1 Raw JSON schema (source of truth)

The Garmin GDPR dump provides sleep data across three JSON schemas + a FIT substrate. All coverage figures below are LC-era (2022-04-04 onward, n=1524 days) unless noted.

| Schema | Source path | Provides | Extractor |
|---|---|---|---|
| `*_sleepData.json` (quarterly shards, 18 total; 2021-06-25 → 2026-05-30; stable schema post-2021-08-17) | `$GEVOELSCORE_DATA_PATH/garmin data/DI_CONNECT/DI-Connect-Wellness/*_sleepData.json` | Sleep-stage minutes, sleep-window respiration, sleep-window SpO2, overnight HR, Garmin sleep-window confirmation label | [`pipeline/01_extract/garmin_sleep_extras.py`](../pipeline/01_extract/garmin_sleep_extras.py) → `processed/garmin/sleep_extras_daily.csv` |
| `UDSFile_*.json` (aggregator; 1734 dates) | `$GEVOELSCORE_DATA_PATH/garmin data/DI_CONNECT/DI-Connect-Aggregator/UDSFile_*.json` | Body Battery stat list, ASLEEP-stress aggregator (avg / max / highDuration), 24h respiration, 24h SpO2 | [`pipeline/01_extract/garmin_uds_extras.py`](../pipeline/01_extract/garmin_uds_extras.py) → `processed/garmin/uds_extras_daily.csv` |
| `sleep_stress_nightly.csv` (derived from `monitoring_b` FIT files via `Monitoring16Resolver`) | `processed/garmin/sleep_stress_nightly.csv` | Sleep-window bounds (`sleep_start_gmt`, `sleep_end_gmt`), FIT-derived per-minute stress aggregated over the sleep window (`stress_mean_sleep`, `stress_stdev_sleep`, `sleep_valid_flag`) | `pipeline/01_extract/extract_sleep_stress.py` |

### 2.2 UDSFile ASLEEP aggregator schema

The `allDayStress.aggregatorList` object contains three aggregator types: `TOTAL`, `AWAKE`, `ASLEEP`. The ASLEEP aggregator supplies:

- `averageStressLevel` → `asleep_stress_avg_uds`
- `maxStressLevel` → `asleep_stress_max_uds` (NEW at Stage 3a)
- `highDuration` (seconds → minutes at extraction) → `asleep_stress_high_min_uds` (NEW at Stage 3a). Garmin only emits this field on nights where high-band stress minutes actually occurred; the field is absent on nights without high-stress minutes. See §7.3.

Cross-consistency check: on 1734 corpus days, `TOTAL == AWAKE + ASLEEP` holds for every count, duration, and intensity field (verified 2026-07-15 per DATA_DICTIONARY §7B corpus verification).

### 2.3 FIT `monitoring_b` role in `stress_mean_sleep`

`stress_mean_sleep` (Family D) is recomputed from raw FIT per-minute stress samples inside the sleep window rather than reading the UDSFile aggregator. This is deliberate: FIT gives per-minute resolution and access to the exact sample distribution, and it uses the FIT-derived sleep-window boundaries. See [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) §2 for the Firstbeat-derivation chain the stress signal inherits.

### 2.4 Extractor ownership per column

| Column | Extractor / consolidator | Notes |
|---|---|---|
| `sleep_deep_min`, `sleep_light_min`, `sleep_rem_min`, `sleep_awake_min`, `sleep_unmeasurable_min` | `garmin_sleep_extras.py` | Sleep-stage minutes from `deepSleepSeconds` etc. |
| `respiration_avg_sleep`, `respiration_max_sleep`, `respiration_min_sleep` | `garmin_sleep_extras.py` | Sleep-window respiration |
| `spo2_avg_sleep`, `spo2_min_sleep` | `garmin_sleep_extras.py` | Sleep-window SpO2 |
| `sleep_hr_avg_spo2` | `garmin_sleep_extras.py` (NEW) | Overnight HR from `spo2SleepSummary.averageHR` |
| `sleep_window_confirmation_type` | `garmin_sleep_extras.py` (NEW) | Garmin sleep-window validity enum |
| `sleep_start_gmt`, `sleep_end_gmt`, `sleep_valid_flag`, `stress_mean_sleep`, `stress_stdev_sleep`, `sleep_duration_min`, `bedtime_hour_local`, `bedtime_std_7d`, `sleep_start_afternoon_flag` | `extract_sleep_stress.py` + `build_unified_dataset.py` derivations | Sleep-window bounds + FIT-derived stress + bedtime derivations |
| `asleep_stress_avg_uds`, `asleep_stress_max_uds`, `asleep_stress_high_min_uds` | `garmin_uds_extras.py` (last two NEW) | ASLEEP aggregator |
| `bb_sleep_start_value`, `bb_sleep_end_value`, `bb_during_sleep_value`, `bb_overnight_gain`, `bb_overnight_gain_proxy`, `bb_overnight_gain_best`, `bb_overnight_gain_source` | `garmin_uds_extras.py` | Body Battery stats + derived overnight-gain family |
| `sleep_efficiency_tib`, `sleep_efficiency_staged`, `sleep_rem_frac`, `sleep_deep_frac`, `sleep_waso_frac`, `bb_overnight_recovery_rate`, `bb_overnight_gain_frac` | `build_unified_dataset.py` (NEW post-pass) | Derived per-row from raw columns already present on the row; no rolling windows |

---

## 3. Device constraints — what's not available on FR245

The Forerunner 245 (Elevate V3 sensor) sets the corpus's hardware ceiling. The following operands are **REJECTED-not-available on FR245**. Downstream MDs must not propose analyses reaching for these fields.

### 3.1 Garmin Sleep Score — REJECTED-not-on-FR245

The overall Garmin Sleep Score (0-100 composite emitted daily on 745/945-family firmware) is **not produced on the FR245**. Confirmed via three independent sources plus raw JSON schema inspection:

- Garmin support forum threads confirming FR245 firmware never received the Sleep Score feature;
- dcrainmaker.com device-review post noting the feature landed on 745 / 945 only;
- the5krunner.com feature-matrix post corroborating the same firmware boundary.
- Corpus check (Stage 3a extraction verification 2026-07-15): no `overallSleepScore` / `sleepScore` field exists in any of the 1734 `*_sleepData.json` entries across the full 2021-06-25 → 2026-05-30 corpus.

**Downstream discipline**: no operand in this catalogue reads a Garmin-emitted Sleep Score; no downstream MD may propose one.

### 3.2 HRV Status (nightly summary) — REJECTED-not-on-FR245

The nightly HRV Status metric is Elevate V4-only. FR245 uses Elevate V3. Per [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) §1, the project's HRV substitute is `stress_mean_sleep` (a Firstbeat-derived proxy at the sleep-window mean, not literal HRV in RMSSD or HF units). See §7 Family D for the operand set the proxy anchors.

### 3.3 Skin temperature — REJECTED-not-on-FR245

FR245 does not carry the skin-temperature sensor required for wrist-based temperature-during-sleep signals. No temperature-during-sleep operand is available on this corpus.

### 3.4 Awakenings / restlessness event counts — REJECTED-not-on-FR245

Garmin's per-night `awakeCount` and restlessness event counts (present on some newer devices) are not emitted on FR245. `sleep_awake_min` (minutes-awake within the sleep window) is the closest available proxy; downstream discipline is to use `sleep_awake_min` (or its ratio variant `sleep_waso_frac`, §4) rather than propose an event-count operand.

### 3.5 Per-minute stage arrays — REJECTED-not-on-FR245

The `*_sleepData.json` files carry per-stage minute totals (`deepSleepSeconds`, `lightSleepSeconds`, `remSleepSeconds`, `awakeSleepSeconds`, `unmeasurableSeconds`) as scalars per night, not as per-minute arrays. FR245 firmware does not emit a per-minute stage timeline in the GDPR export. Any downstream operand needing per-minute stage information (e.g. transition counts, stage-bout durations) is not derivable from this corpus.

### 3.6 Validity anchor for the FR245 operands that ARE available

Per the [`wearables_sleep_hrv_chronic_illness_review.md`](../literature/reviews/wearables_sleep_hrv_chronic_illness_review.md) §2 anchor citing Miller 2022 (n=53 healthy adults, PSG-referenced): on the FR245 specifically, two-state sleep detection (sleep vs wake) reached 89% agreement / Cohen's κ = 0.35 ("adequate"); multi-state sleep-stage classification reached 50% agreement / κ = 0.25 ("poor"). Timing and duration operands (`sleep_duration_min`, `bedtime_hour_local`, sleep-window bounds) inherit the "adequate" validity; per-stage architecture operands (`sleep_deep_min`, `sleep_light_min`, `sleep_rem_min`) inherit the "poor" validity. Downstream MDs consuming Family A architecture operands should carry this caveat.

---

## 4. Family A — Architecture (single-night)

Per-night sleep-window characterisation: total sleep window, sleep-stage minutes, and derived ratio operands.

### 4.1 Operand table

| Column | Formula | Unit | Tier | LC-era coverage |
|---|---|---|---|---:|
| `sleep_duration_min` | raw: `sleep_end_gmt - sleep_start_gmt` (minutes) | minutes | PRIMARY | 97.0% |
| `sleep_deep_min` | raw: `deepSleepSeconds / 60` | minutes | PRIMARY | 97.3% |
| `sleep_light_min` | raw: `lightSleepSeconds / 60` | minutes | PRIMARY | 97.3% |
| `sleep_rem_min` | raw: `remSleepSeconds / 60` (NEW 2026-07-15) | minutes | PRIMARY | 95.5% |
| `sleep_awake_min` | raw: `awakeSleepSeconds / 60` | minutes | PRIMARY | 97.3% |
| `sleep_unmeasurable_min` | raw: `unmeasurableSeconds / 60` | minutes | PRIMARY (validity gate) | 97.3% |
| `sleep_window_confirmation_type` | raw: `sleepWindowConfirmationType` (enum) (NEW 2026-07-15) | enum | PRIMARY (validity gate) | 98.6% |
| `sleep_efficiency_tib` | derived: `(sleep_duration_min - sleep_awake_min) / sleep_duration_min` (NEW 2026-07-15) | fraction 0-1 | PRIMARY | 96.7% |
| `sleep_efficiency_staged` | derived: `(sleep_deep_min + sleep_light_min + sleep_rem_min) / sleep_duration_min` (NEW 2026-07-15) | fraction 0-1 | SENSITIVITY | 95.5% |
| `sleep_rem_frac` | derived: `sleep_rem_min / (sleep_deep_min + sleep_light_min + sleep_rem_min)` (NEW 2026-07-15) | fraction 0-1 | PRIMARY (architecture-share) | 95.5% |
| `sleep_deep_frac` | derived: `sleep_deep_min / (sleep_deep_min + sleep_light_min + sleep_rem_min)` (NEW 2026-07-15) | fraction 0-1 | PRIMARY (architecture-share) | 95.5% |
| `sleep_waso_frac` | derived: `sleep_awake_min / sleep_duration_min` (NEW 2026-07-15) | fraction 0-1 | SENSITIVITY | 96.7% |

### 4.2 `sleep_rem_min` — the REM extractor correction

An earlier version of [`garmin_sleep_extras.py`](../pipeline/01_extract/garmin_sleep_extras.py) asserted that the FR245 does not produce REM-stage classification and did not extract `remSleepSeconds`. That assertion was **factually wrong on this corpus**: `remSleepSeconds` is present at 95.5% LC-era coverage (1456/1524 nights), nonzero every year 2021-2026, mean 108 min, median 107 min, range 5-253. The Stage 3a extractor pass (2026-07-15) corrected the comment and added `sleep_rem_min` extraction. The ~4.5% coverage gap is nights on which Garmin fell back to the deep/light/awake-only classifier (no `remSleepSeconds` emitted).

Cross-cite: DATA_DICTIONARY §7 `sleep_light_min` note ("Superseded note (corrected 2026-07-15)") + the new `sleep_rem_min` row.

### 4.3 `sleep_window_confirmation_type` — validity gate

The Garmin sleep-window confirmation enum, with LC-era distribution (n=1524):

| Value | Count | Meaning |
|---|---:|---|
| `ENHANCED_CONFIRMED` | 990 | Enhanced-algorithm confirmation |
| `ENHANCED_CONFIRMED_FINAL` | 466 | Enhanced-algorithm confirmation, final classifier |
| `AUTO_CONFIRMED_FINAL` | 17 | Auto-confirmation, final classifier |
| `AUTO_CONFIRMED` | 1 | Auto-confirmation |
| `UNCONFIRMED` | 20 | Garmin declined to confirm the sleep-window bounds |
| `OFF_WRIST` | 9 | Device off-wrist during the candidate sleep window |
| (missing) | 21 | Field absent from JSON (nights before enum was added, or Garmin returned no sleepData entry) |

**Downstream discipline for analytical use**: filter to `ENHANCED_*` + `AUTO_*` (retain 1474 rows out of 1524 = 96.7%). Exclude `OFF_WRIST` + `UNCONFIRMED` + missing (drop 50 rows). The Stage 3a coverage numbers on Family A derived columns (`sleep_efficiency_tib` at 96.7% etc.) reflect this filter passing on the underlying architecture columns, but downstream analyses that need an explicit validity gate should apply the filter at analysis time rather than rely on upstream NaN propagation.

### 4.4 Definitional-pair discipline: `sleep_efficiency_tib` vs `sleep_efficiency_staged`

Two efficiency formulas exist in the sleep-medicine literature and both are computable on this corpus. Per CONVENTIONS §3.3, pick one per analysis; report the other as a sensitivity read only if the primary verdict is sensitive to the choice.

- **`sleep_efficiency_tib` = (dur - awake) / dur — CANONICAL, PRIMARY.** The Miller 2022 / standard sleep-medicine definition: time-asleep / time-in-bed. Uses only `sleep_duration_min` and `sleep_awake_min`; robust to per-night variation in `sleep_unmeasurable_min`.
- **`sleep_efficiency_staged` = (deep + light + rem) / dur — SENSITIVITY.** Uses classified-asleep minutes as the numerator instead of TIB-minus-awake. Differs from `sleep_efficiency_tib` when `sleep_unmeasurable_min` is non-trivial (device could not classify some minutes; those minutes exit both formulas differently). Corpus median difference is small (`tib` median 0.995, `staged` median 0.994), but per-night divergence can be larger on nights with high `sleep_unmeasurable_min`.

The two formulas answer subtly different questions: `_tib` asks "how much of my time in bed did I sleep?"; `_staged` asks "how much of my time in bed did the device classify as one of the three sleep stages?". The canonical form is `_tib` — downstream MDs default to it and report `_staged` only when a per-night unclassified-minute contrast matters.

**Coverage caveat on `_staged`**: 95.5% (inherits REM extraction coverage). `_tib` at 96.7% has ~1pp more coverage because it does not require the REM column.

### 4.5 Fraction-of-classified-asleep operands (`sleep_rem_frac`, `sleep_deep_frac`)

The three sleep stages (`deep`, `light`, `rem`) sum to a "classified-asleep" total. The fractions:

- `sleep_rem_frac = rem / (deep + light + rem)` — REM share of classified-asleep. Range 0-1; corpus median 0.174.
- `sleep_deep_frac = deep / (deep + light + rem)` — deep-sleep share of classified-asleep. Range 0-1; corpus median 0.092.

Both are architecture-share operands: absolute REM minutes vs REM fraction may diverge across nights (long night with typical REM fraction vs short night with high REM fraction), and downstream analyses should carry whichever answers the question of interest. Fraction operands are less sensitive to total-duration variation than the raw minute counts; raw minute counts are the natural read for "did the participant lose sleep on this stage?".

Light-sleep fraction is derivable as `1 - sleep_rem_frac - sleep_deep_frac` but is not stored as a separate column; downstream consumers can compute it if needed.

### 4.6 WASO fraction (`sleep_waso_frac`)

`sleep_waso_frac = sleep_awake_min / sleep_duration_min` — the wake-after-sleep-onset fraction of TIB. Range 0-1; corpus median 0.005 (most nights have very low awake-time). Definitional complement to `sleep_efficiency_tib` (`sleep_waso_frac + sleep_efficiency_tib == 1` by construction on nights where both are computable), so the two channels carry identical information; SENSITIVITY tier.

---

## 5. Family B — Consistency / regularity (multi-night rolling)

**Status: VIABLE-BUT-NOT-YET-IMPLEMENTED.** Family B operands read sleep timing + duration variability across rolling multi-night windows. The raw substrate (`sleep_start_gmt`, `sleep_end_gmt`, `bedtime_hour_local`, `sleep_duration_min`) is present at 97-98.6% coverage; the algorithms to compute Family B operands are not yet in the pipeline.

### 5.1 Currently implemented (partial)

| Column | Definition | LC-era coverage | Tier |
|---|---|---:|---|
| `bedtime_hour_local` | `sleep_start_gmt` in Europe/Amsterdam local, fractional hour | 97.0% | PRIMARY (as an input to §5.2 operands) |
| `bedtime_std_7d` | 7-day rolling std of `bedtime_hour_local` (afternoon-flagged nights excluded; wrap-around handled per DATA_DICTIONARY §7) | 100.0% | PRIMARY |

`bedtime_std_7d` is the only Family B rolling operand currently in `per_day_master.csv`. Wiggers F4 (bedtime inconsistency → next-day energy) reads it.

### 5.2 Named-but-not-implemented (DEFERRED)

The following operands are natural Family B extensions, all feasible on this corpus at the substrate coverage above. Implementation is DEFERRED until a downstream analysis needs them; estimated algorithm-implementation cost ~1-2h per operand family.

- **Sleep Regularity Index (SRI) — 7-day and 14-day rolling.** Phillips et al. 2017 (Sci Rep, DOI 10.1038/s41598-017-03171-4). Sinusoidal-model-based; two-state (asleep / awake) reconstruction from `sleep_start_gmt` / `sleep_end_gmt` at 98.6% coverage is sufficient for the algorithm. Rolling window ≥ 7 days. Range -100 (perfectly irregular) to +100 (perfectly regular). Anchors:
  - UK Biobank mortality anchor (SRI predicts all-cause + cardiovascular + cancer mortality in the general population).
  - Matcham et al. 2024 MDD relapse anchor (Fitbit-derived sleep-regularity operands predicted depression-relapse in a 393-participant recurrent MDD cohort over median 541 days per [`wearables_sleep_hrv_chronic_illness_review.md`](../literature/reviews/wearables_sleep_hrv_chronic_illness_review.md) §3).
- **`bedtime_std_14d`** — 14-day analogue of `bedtime_std_7d`. Trivial extension.
- **`waketime_std_7d`, `waketime_std_14d`** — rolling std of `sleep_end_gmt` converted to local fractional hour. Wraps handled analogously to bedtime.
- **`midpoint_std_7d`, `midpoint_std_14d`** — rolling std of the sleep-window midpoint (`(sleep_start_gmt + sleep_end_gmt) / 2`). Captures phase-shift patterns that `bedtime_std_7d` and `waketime_std_7d` miss when both drift together.
- **`sleep_duration_std_7d`, `sleep_duration_std_14d`** — rolling std of `sleep_duration_min`. Duration-regularity companion to bedtime-regularity.

### 5.3 Missing-nights inside a rolling window

For any Family B rolling operand, the policy for a rolling window containing missing nights: **require ≥ N valid nights in the window** (N depends on the operand; SRI typically requires ≥ 5 of 7). Windows below the validity bar propagate NaN. Never `.fillna(0)` a rolling-window missing night (a missing night is not a "zero-regularity" night). See `bedtime_std_7d` NaN handling in DATA_DICTIONARY §7 for the pattern to mirror.

### 5.4 Family B is the natural home for Q24 sub-part 3

Per [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) §1.2 + §1.3, Q24 sub-part 3 (phase-stratification: does the compensatory-rest response strengthen over time?) is out of scope for the Q24 parent MD and awaits implementation of a Family B operand set. **Family B operands are NOT to be read at +3d / +5d / +10d day-after trajectory windows** — the SRI + regularity family is a between-phase construct (comparing regularity across LC phases, or across pre- vs post-intervention epochs), not a day-after-trajectory construct. Reading a 7-day rolling SRI at d+3 after a heavy episode conflates the episode's response with the last three days of the pre-episode window, which is the wrong reference frame for the day-after-trajectory question.

Downstream discipline: Q24 sub-part 3, when it opens, is the natural venue for the SRI + timing-SD operands. Any pre-reg that reaches for Family B outside a phase-stratification framing must justify the choice explicitly.

---

## 6. Family C — Composite / score (single-night)

**Rejected + deferred; documented explicitly to prevent future proposals reaching for absent features.**

### 6.1 Garmin Sleep Score — REJECTED-not-on-FR245

Documented at §3.1. No downstream operand may read a Garmin-emitted Sleep Score field on this corpus.

### 6.2 Home-built composite — DEFERRED

A home-built single-night composite (e.g. a RU-SATED-inspired 4-dimension adaptation weighing duration, efficiency, regularity, timing — sometimes called "RU-TED" in the mHealth adaptation literature) is engineering-only: it is straightforward to build from the Family A + Family B operands present here, but the composite has no direct external anchor at n=1 single-subject resolution.

**If built later**, the composite lands as a DESCRIPTIVE SUMMARY read only; the per-component operands (duration, efficiency, regularity, timing) carry the analytical weight for any inferential test. This mirrors the project's discipline on other composite / index constructions (e.g. `exertion_rank_composite_lagged_lcera` is the exertion composite, but the per-axis components carry the inferential reads per [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) §6.1).

Composite construction is DEFERRED until a downstream analysis surfaces a need this MD does not currently anticipate.

---

## 7. Family D — Physiological during sleep

Autonomic, respiration, oxygenation, and HR channels aggregated over the sleep window. All are *operational* descriptors of the sleep-window physiological trace, not mechanistic autonomic measurements.

### 7.1 Operand table

| Column | Formula / source | Unit | Tier | LC-era coverage |
|---|---|---|---|---:|
| `stress_mean_sleep` | FIT: mean per-minute stress over sleep window | Garmin stress 0-100 | PRIMARY | 97.0% |
| `stress_stdev_sleep` | FIT: within-sleep-window stress std | Garmin stress 0-100 | SENSITIVITY | 97.0% |
| `asleep_stress_avg_uds` | UDSFile: `ASLEEP.averageStressLevel` | Garmin stress 0-100 | SENSITIVITY (cross-source of `stress_mean_sleep`) | 97.9% |
| `asleep_stress_max_uds` | UDSFile: `ASLEEP.maxStressLevel` (NEW 2026-07-15) | Garmin stress 0-100 | PRIMARY (arousal-peak proxy) | 97.9% |
| `asleep_stress_high_min_uds` | UDSFile: `ASLEEP.highDuration / 60` (NEW 2026-07-15) | minutes | SENSITIVITY | **10.2%** — see §7.3 |
| `respiration_avg_sleep` | JSON: `averageRespiration` | breaths/min | PRIMARY | 96.8% |
| `respiration_max_sleep` | JSON: `highestRespiration` | breaths/min | SENSITIVITY | 96.8% |
| `respiration_min_sleep` | JSON: `lowestRespiration` | breaths/min | SENSITIVITY | 96.8% |
| `spo2_avg_sleep` | JSON: `spo2SleepSummary.averageSPO2` | percent | SENSITIVITY | 84.8% |
| `spo2_min_sleep` | JSON: `spo2SleepSummary.lowestSPO2` | percent | SENSITIVITY | 84.8% |
| `sleep_hr_avg_spo2` | JSON: `spo2SleepSummary.averageHR` (NEW 2026-07-15) | bpm | PRIMARY (overnight-HR proxy) | 93.0% |

### 7.2 Definitional-pair: `stress_mean_sleep` (FIT) vs `asleep_stress_avg_uds` (UDS)

Both channels compute a sleep-window mean of the Garmin stress signal — the same construct — from different sources:

- `stress_mean_sleep` (**PRIMARY**): recomputed from raw per-minute FIT stress samples inside the sleep window bounded by `sleep_start_gmt` / `sleep_end_gmt`. Sensitive to the FIT sleep-window definition.
- `asleep_stress_avg_uds` (**SENSITIVITY / cross-source check**): the Garmin-emitted ASLEEP-aggregator mean from `UDSFile_*.json`. Sensitive to Garmin's internal sleep-window definition.

They should agree closely; documented divergence usually reflects sleep-window boundary differences between the FIT extraction and the UDS aggregator. Per DATA_DICTIONARY §7B, on 2 nights (2025-11-19, 2025-11-24) the UDS ASLEEP channel returned a sentinel while FIT-derived `stress_mean_sleep` returned a valid value — those are Garmin internal-channel discrepancies where downstream analyses should prefer `stress_mean_sleep`.

Both inherit the Firstbeat-opacity caveat per [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) §8.2 (algorithmic opacity; RMSSD/HF/LF/HR/respiration weightings proprietary; monotone but not analytically invertible). Downstream MDs treating either as an HRV proxy should carry the caveat verbatim.

### 7.3 `asleep_stress_high_min_uds` — the "missing means unknown-or-zero" semantics

Garmin only emits the `highDuration` field inside the `ASLEEP` aggregator on nights where high-band stress minutes actually occurred. On nights with zero high-band minutes, the field is **absent from the JSON entirely** (not present as zero). LC-era coverage is 10.2% (156 / 1524 days) — the low coverage IS the informative feature, not a data-quality problem.

**Zero-vs-NaN discipline decision (locked)**: missing is coded as NaN, NOT as zero. Rationale:

- On the 90% of days where the field is absent, we know Garmin's aggregator did not emit high-band minutes. Whether that means "genuinely zero high-band minutes" or "Garmin's aggregator declined to score the ASLEEP window at all on that night" (edge cases with off-wrist minutes, unmeasurable minutes, etc.) is not always distinguishable from the JSON alone.
- The right analytical default is to acknowledge the ambiguity by leaving the value NaN. Downstream consumers who want to interpret missing-as-zero (e.g. for a per-day count of nights-with-any-high-stress-minutes) must make that call explicitly at analysis time, with a stated rationale.
- Silent `.fillna(0)` at extraction time would collapse the "unknown" and "zero" cases into one, biasing any downstream contrast toward the null.

**Downstream discipline**: any analysis reading `asleep_stress_high_min_uds` must either (a) restrict to the ~10% of days where the field is present and interpret as a within-that-stratum contrast, or (b) explicitly cite this section when applying `.fillna(0)` and defend the interpretation choice.

### 7.4 `sleep_hr_avg_spo2` — overnight HR channel

Overnight-average HR reported inside the `spo2SleepSummary` JSON block (93.0% LC-era coverage; mean 61.2 bpm, median 61.0, range 50-84). This is a cleaner overnight-HR channel than any FIT re-derivation: Garmin has already computed the sleep-window HR average using their own sleep-window bounds and their own sample-quality filters.

**Downstream relevance**: directly comparable to the "nightly HR persistence in LC" finding from Radin et al. 2024 (npj Digit Med; Long COVID RHR / activity trajectories diverge from controls up to one year; per [`pem_recovery_trajectory_review.md`](../literature/reviews/pem_recovery_trajectory_review.md) §9 `/reading`). Downstream MDs testing overnight-HR dynamics against post-heavy-day trajectories or crash-precursor signatures should default to `sleep_hr_avg_spo2` rather than a FIT-derive.

**Definitional-pair note**: `sleep_hr_avg_spo2` complements the daily `resting_hr` channel (from Garmin's daily-summary) and the waking `hr_median_waking` channel (from FIT). All three answer sleep-related HR questions from different windows; downstream analyses should pick one primary per hypothesis.

### 7.5 Respiration + SpO2 caveats

`respiration_avg_sleep` (etc.) inherit the Garmin epoch-level respiration definition (breaths per minute, computed at the epoch level; the daily / sleep-window means are aggregates over epochs) per DATA_DICTIONARY §7B.

`spo2_avg_sleep` (etc.) require the Pulse Ox Sleep Mode toggle on the device. Coverage is 84.8% LC-era (lower than the 96-97% of other Family D operands) because the participant did not always have the toggle enabled. SENSITIVITY tier; Wiggers G4 deprioritised.

---

## 8. Family E — BB overnight recovery

Body Battery overnight change and derived normalisation operands. **All Family E operands are Firstbeat vendor-mechanistic; no peer-reviewed PEM anchor exists.** SENSITIVITY tier at most.

### 8.1 Operand table

| Column | Formula | Unit | Tier | LC-era coverage |
|---|---|---|---|---:|
| `bb_sleep_start_value` | UDS: `bodyBatteryStatList[SLEEPSTART].statsValue` | BB units 5-100 | SENSITIVITY | 43.8% |
| `bb_sleep_end_value` | UDS: `bodyBatteryStatList[SLEEPEND].statsValue` | BB units 5-100 | SENSITIVITY | 38.9% |
| `bb_during_sleep_value` | UDS: `bodyBatteryStatList[DURINGSLEEP].statsValue` (= SLEEPEND - SLEEPSTART; DEFINITIONAL with `bb_overnight_gain`, per DATA_DICTIONARY §7B) | BB units | SENSITIVITY | 56.5% |
| `bb_overnight_gain` | derived: `bb_sleep_end_value - bb_sleep_start_value` | BB units | SENSITIVITY (Wiggers D2 primary) | 38.9% |
| `bb_overnight_gain_proxy` | derived: `bb_highest - bb_sleep_start_value` (documented proxy, r=0.989 vs truth on n=593) | BB units | SENSITIVITY | 43.8% |
| `bb_overnight_gain_best` | derived: truth where present, else proxy | BB units | SENSITIVITY | 43.8% |
| `bb_overnight_recovery_rate` | derived: `bb_overnight_gain / (sleep_duration_min / 60)` (NEW 2026-07-15) | BB units per hour of sleep | SENSITIVITY | 38.9% |
| `bb_overnight_gain_frac` | derived: `bb_overnight_gain / (100 - bb_sleep_start_value)` (NEW 2026-07-15) | fraction 0-1 (headroom recharged) | SENSITIVITY | 38.9% |

### 8.2 `bb_overnight_recovery_rate` — duration-normalised

The raw `bb_overnight_gain` conflates two things: how much BB the participant recharged, and how many hours the participant slept. `bb_overnight_recovery_rate = bb_overnight_gain / (sleep_duration_min / 60)` normalises to "BB units per hour of sleep". Corpus range 0.586 to 8.975; mean 4.77, median 4.81.

Downstream use: when the analytical question is "how efficiently did sleep recharge autonomic reserve" (rate) rather than "how much total autonomic reserve was recharged" (level), `bb_overnight_recovery_rate` is the right operand.

### 8.3 `bb_overnight_gain_frac` — ceiling-corrected

Raw `bb_overnight_gain` conflates recharge magnitude with recharge-headroom: a night starting at BB=30 can recharge up to 70 units; a night starting at BB=80 can only recharge 20 units. `bb_overnight_gain_frac = bb_overnight_gain / (100 - bb_sleep_start_value)` normalises to "fraction of available headroom recharged". Corpus range 0.046 to 1.000; mean 0.680, median 0.690.

Downstream use: when the analytical question is "did the recharge fill the available reserve" (fraction) rather than "how many absolute BB units" (level), `bb_overnight_gain_frac` is the right operand. Degenerate case: when `bb_sleep_start_value == 100` the denominator is zero and the operand emits NaN (documented in the consolidator post-pass).

### 8.4 Coverage caveat — source-column sparsity

Both new derived operands are sourced from `bb_overnight_gain` (the "truth" column, 38.9% LC-era) rather than `bb_overnight_gain_best` (the fused truth-or-proxy column, 43.8% LC-era). Rationale: the ~5pp coverage gain from `_best` comes from the `bb_overnight_gain_proxy` fallback, which is validated but adds a provenance asymmetry across days. Downstream analyses that need the extra coverage from proxy fallback can add a separate `_best`-sourced variant if a specific downstream MD justifies it; the primary operands stay on the truth-sourced path.

### 8.5 Firstbeat-opacity caveat + no-PEM-anchor caveat

Per §7.2 and per [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) §8.2: Body Battery is a proprietary Firstbeat/Garmin composite. The exact input weighting (HRV vs HR vs activity vs stress vs sleep-stage) is not published; the mapping between raw physiological inputs and BB units is not analytically invertible; the sleep-window integration is not documented.

Additionally: **no peer-reviewed anchor** exists for BB-based operands as PEM-recovery instruments. All Family E operands are SENSITIVITY tier at most. Downstream MDs using Family E operands must cite this section as the caveat.

---

## 9. Coverage matrix

Full-corpus LC-era coverage (post-Stage-3a landing, verified 2026-07-15 via pandas probe of `per_day_master.csv`; n=1524 LC-era rows).

| Operand | Family | LC-era coverage | Tier |
|---|---|---:|---|
| `sleep_duration_min` | A | 97.0% | PRIMARY |
| `sleep_deep_min` | A | 97.3% | PRIMARY |
| `sleep_light_min` | A | 97.3% | PRIMARY |
| `sleep_rem_min` | A | 95.5% | PRIMARY |
| `sleep_awake_min` | A | 97.3% | PRIMARY |
| `sleep_unmeasurable_min` | A | 97.3% | PRIMARY (validity gate) |
| `sleep_window_confirmation_type` | A | 98.6% | PRIMARY (validity gate) |
| `sleep_efficiency_tib` | A | 96.7% | PRIMARY |
| `sleep_efficiency_staged` | A | 95.5% | SENSITIVITY |
| `sleep_rem_frac` | A | 95.5% | PRIMARY (architecture-share) |
| `sleep_deep_frac` | A | 95.5% | PRIMARY (architecture-share) |
| `sleep_waso_frac` | A | 96.7% | SENSITIVITY |
| `bedtime_hour_local` | B | 97.0% | PRIMARY (input to §5.2) |
| `bedtime_std_7d` | B | 100.0% | PRIMARY |
| SRI 7d / 14d, further Family B | B | N/A | DEFERRED (viable-not-implemented) |
| Garmin Sleep Score | C | N/A | REJECTED-not-on-FR245 |
| Home-built composite | C | N/A | DEFERRED |
| `stress_mean_sleep` | D | 97.0% | PRIMARY |
| `stress_stdev_sleep` | D | 97.0% | SENSITIVITY |
| `asleep_stress_avg_uds` | D | 97.9% | SENSITIVITY |
| `asleep_stress_max_uds` | D | 97.9% | PRIMARY (arousal-peak) |
| `asleep_stress_high_min_uds` | D | 10.2% | SENSITIVITY (see §7.3) |
| `respiration_avg_sleep` | D | 96.8% | PRIMARY |
| `respiration_max_sleep` | D | 96.8% | SENSITIVITY |
| `respiration_min_sleep` | D | 96.8% | SENSITIVITY |
| `spo2_avg_sleep` | D | 84.8% | SENSITIVITY |
| `spo2_min_sleep` | D | 84.8% | SENSITIVITY |
| `sleep_hr_avg_spo2` | D | 93.0% | PRIMARY (overnight-HR proxy) |
| `bb_sleep_start_value` | E | 43.8% | SENSITIVITY |
| `bb_sleep_end_value` | E | 38.9% | SENSITIVITY |
| `bb_during_sleep_value` | E | 56.5% | SENSITIVITY (definitional with `bb_overnight_gain`) |
| `bb_overnight_gain` | E | 38.9% | SENSITIVITY (Wiggers D2 primary) |
| `bb_overnight_gain_proxy` | E | 43.8% | SENSITIVITY |
| `bb_overnight_gain_best` | E | 43.8% | SENSITIVITY |
| `bb_overnight_recovery_rate` | E | 38.9% | SENSITIVITY |
| `bb_overnight_gain_frac` | E | 38.9% | SENSITIVITY |

**Reading the matrix**: PRIMARY operands with ≥ 90% LC-era coverage are safe defaults for downstream analyses; PRIMARY operands with 80-90% coverage (`sleep_hr_avg_spo2` at 93.0%) are safe with per-arm-n reporting; SENSITIVITY operands with < 80% coverage require explicit coverage-per-arm reporting at analysis time. Family E operands at 38.9% LC-era should NOT be used as primaries for extended-window trajectory analyses (matched-comparator pool intersections shrink materially — see [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) §6.2.1 for the pattern).

---

## 10. Missing-vs-zero discipline

Per [CONVENTIONS §5](../CONVENTIONS.md#5-project-wide-anchors-read-once-then-trust) and the parent MD [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) §3.4 no-intensity-record precedent. Under no circumstance is `.fillna(0)` applied to any sleep operand at extraction or consolidation time.

Per-operand missingness policy:

- **`sleep_duration_min`, `sleep_deep_min`, `sleep_light_min`, `sleep_rem_min`, `sleep_awake_min`, `sleep_unmeasurable_min`**: NaN when the night has no `*_sleepData.json` entry OR when the specific source field is absent from the entry. For `sleep_rem_min` specifically, the ~4.5% coverage gap is nights on which Garmin used the deep/light/awake-only classifier (no `remSleepSeconds` emitted); NaN, not zero.
- **`sleep_window_confirmation_type`**: NaN when the enum field is absent from the JSON. Downstream validity gates should filter to `ENHANCED_*` + `AUTO_*` at analysis time (see §4.3), never treat missing as a specific enum value.
- **`sleep_efficiency_tib`**: NaN when either `sleep_duration_min` or `sleep_awake_min` is NaN OR when `sleep_duration_min == 0`. The zero-denominator case is a device-side artefact (Garmin recorded no sleep on that date), not a zero-efficiency observation.
- **`sleep_efficiency_staged`**: NaN when any of `sleep_duration_min`, `sleep_deep_min`, `sleep_light_min`, `sleep_rem_min` is NaN OR when `sleep_duration_min == 0`.
- **`sleep_rem_frac`, `sleep_deep_frac`**: NaN when any of `sleep_deep_min`, `sleep_light_min`, `sleep_rem_min` is NaN OR when their sum is zero (no classified-asleep minutes; a device-side artefact).
- **`sleep_waso_frac`**: same as `sleep_efficiency_tib`.
- **`stress_mean_sleep`, `stress_stdev_sleep`**: NaN when `sleep_valid_flag == False` (per DATA_DICTIONARY §7) or when no sleep is recorded. Never treat missing as "zero stress"; a missing night carries no stress information.
- **`asleep_stress_avg_uds`, `asleep_stress_max_uds`**: NaN on days without a UDSFile entry OR when the negative-sentinel filter fires (per DATA_DICTIONARY §7B).
- **`asleep_stress_high_min_uds`**: NaN when Garmin's ASLEEP aggregator did not emit the `highDuration` field. Documented at §7.3: this covers both "genuinely zero high-band minutes" and "Garmin declined to score" cases; the two are not distinguishable in the source JSON. **Downstream consumers who choose to `.fillna(0)` must justify at analysis time.**
- **`sleep_hr_avg_spo2`**: NaN when the `spo2SleepSummary` block is absent OR when `averageHR` is missing from the block. Not correlated with SpO2 sensor toggle in the raw JSON (HR is always computed even when SpO2 is disabled), but the 93.0% coverage reflects a slightly lower rate than the sleep-stage columns for reasons Garmin does not document.
- **`respiration_avg_sleep`, `respiration_max_sleep`, `respiration_min_sleep`**: NaN when the sleep-window respiration fields are absent.
- **`spo2_avg_sleep`, `spo2_min_sleep`**: NaN when Pulse Ox Sleep Mode was disabled on that night OR when the sleep-window SpO2 fields are absent.
- **`bb_*`**: NaN per DATA_DICTIONARY §7B (structural absence before rollout dates + sentinel-filtered days). `bb_overnight_recovery_rate` and `bb_overnight_gain_frac` inherit NaN from any input NaN OR from denominator-zero cases (`sleep_duration_min == 0` for the rate; `bb_sleep_start_value == 100` for the frac).

**Downstream reporting discipline**: per-arm n_valid must be reported per operand at analysis time (analogous to the parent MD's per-bout-n reporting discipline). Silent NaN elimination without reporting the per-arm count changes the interpretability of any cross-arm contrast.

---

## 11. Downstream consumers

Which hypothesis MDs read which subset of this catalogue:

### 11.1 Q24 — `post_heavy_day_compensatory_rest.md`

Per [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) §6.2 (patched at Stage 3b to cross-ref this catalogue rather than re-define formulas inline):

**Primary sleep + autonomic outcome operands**:
- `sleep_duration_min`, `sleep_deep_min`, `sleep_light_min`, `sleep_awake_min` (Family A architecture minutes)
- `sleep_rem_min` (Family A; ADDED at Stage 3b as PRIMARY architecture outcome; 95.5% LC-era coverage)
- `sleep_efficiency_tib` (Family A; renamed from Q24 draft's `sleep_efficiency` for canonicalisation)
- `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest` (Family D + waking-stress + BB-floor)
- `hr_median_waking` (Family D + HRM4Pacing caveat carried forward)

**Sensitivity-tier sleep operands** (Q24 §6.2.3 patch):
- `sleep_efficiency_staged` (cross-check vs `_tib`)
- `bb_overnight_gain` (existing at +3d only, sparse; handled per Q24 §6.2.1)
- `bb_overnight_gain_frac` (ceiling-corrected variant)
- `sleep_hr_avg_spo2` (overnight HR per Radin 2024)
- `spo2_avg_sleep` (existing sensitivity)
- `asleep_stress_max_uds` (arousal-count proxy)

**Explicit exclude** (Q24 §6.5 patch): SRI-family + timing-SD operands (Family B) are RESERVED for Q24 sub-part 3 (phase-stratification) and are NOT read at +3d / +5d / +10d trajectory windows.

### 11.2 Future Wiggers F1 — sleep quantity → PEM

Candidate primary: `sleep_duration_min` (Family A; 97.0% coverage).
Candidate sensitivity: `sleep_efficiency_tib` (Family A) — for the "PEM day = long sleep" claim, sleep-quality via efficiency is a natural companion. Full operand shortlist locked when the F1 pre-reg opens.

### 11.3 Future Wiggers F4 — bedtime consistency → next-day energy

Candidate primary: `bedtime_std_7d` (Family B; 100.0% coverage).
Candidate extensions once Family B lands: SRI-7d, midpoint-std-7d, waketime-std-7d.

### 11.4 Intervention-effects methodology

Currently consumes `stress_mean_sleep` (Family D) per [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md). Other Family D operands (`sleep_hr_avg_spo2`, `asleep_stress_max_uds`, `respiration_avg_sleep`) are available additions if an intervention-effect analysis needs cross-channel triangulation.

### 11.5 Q24 sub-part 3 (phase-stratification) — DEFERRED

The natural home for Family B once implemented. See §5.4.

---

## 12. Compression and lock discipline

Producer-mode methodology MD per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). The lock discipline follows the parent MD [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) §3.6 compression pattern:

1. **Draft (this file, r1)**: producer-mode subagent draft. Content-locked substantive sections (§1-§11); only frontmatter Status / lock-log editable post-lock.
2. **Fresh-session `/research-methodology-review`**: reviewer-mode session (different Claude session, cold context) audits this MD against the CONVENTIONS §2.2 four-input bar + applicable 4-layer checklist items. Produces reviewer report at `docs/research/reviews/methodology-sleep_metrics-YYYY-MM-DD.md`.
3. **r2 lock with §3.6 compression**: reviewer fires absorbed inline via the parent MD's compression discipline (mechanical clarifications, cross-cites, caveat additions); architectural changes escalate to r2-with-design-change and re-review.
4. **Downstream MD consumption**: no downstream sleep-touching hypothesis MD reads from this catalogue until the r2 lock lands.

**Compression rule** (inherited from parent MD): reviewer absorption at r2 is *mechanical* (clarifications, cross-cites, added caveats) NOT architectural (design changes). Any architectural change forces re-review before lock.

---

## 13. Lock log

| version | date | change |
|---|---|---|
| r1 | 2026-07-15 | Initial draft as producer-mode methodology MD following the Stage 3a pipeline extension that landed 12 new sleep-derived columns (5 raw + 7 derived) on `per_day_master.csv` with byte-identical determinism preserved on all 205 existing columns. Five-family taxonomy locked (A Architecture / B Consistency-regularity / C Composite-score / D Physiological-during-sleep / E BB-overnight-recovery). PRIMARY / SENSITIVITY / DEFERRED tier system across all operands. Definitional-pair discipline for `sleep_efficiency_tib` vs `sleep_efficiency_staged` (§4.4) and `stress_mean_sleep` vs `asleep_stress_avg_uds` (§7.2). Zero-vs-NaN discipline per operand (§10). Downstream consumer map for Q24 + future Wiggers F1 / F4 + intervention-effects + Q24 sub-part 3 (§11). Coverage numbers verified via pandas probe of `per_day_master.csv` 2026-07-15 (§9 matrix). Subagent-drafted per user delegation; fresh-session `/research-methodology-review` before lock is the peer-review discipline. |

---

## 14. Cross-references

- [CONVENTIONS §1.2, §2.2, §3.3, §5](../CONVENTIONS.md) — producer-mode + four-input bar + definitional-pair discipline + project-wide anchors.
- Extractor scripts:
  - [`pipeline/01_extract/garmin_sleep_extras.py`](../pipeline/01_extract/garmin_sleep_extras.py) — Family A, D (respiration + SpO2 + overnight HR), sleep-window confirmation
  - [`pipeline/01_extract/garmin_uds_extras.py`](../pipeline/01_extract/garmin_uds_extras.py) — Family D (UDS-derived), Family E (BB stats)
- Consolidator: [`pipeline/03_consolidate/build_unified_dataset.py`](../pipeline/03_consolidate/build_unified_dataset.py) — derived-column post-pass (`sleep_efficiency_*`, `sleep_*_frac`, `bb_overnight_*_frac`, `bb_overnight_recovery_rate`).
- [DATA_DICTIONARY §7](../DATA_DICTIONARY.md#section-7--garmin-sleep-stress-nightly-wake-up-date-attributed) — per-column definitions for Family A sleep-stress rows.
- [DATA_DICTIONARY §7B](../DATA_DICTIONARY.md) — per-column definitions for Family D UDS-derived rows and Family E BB rows.
- Sister methodology MDs:
  - [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) — Firstbeat-opacity caveat inherited by Family D + Family E.
  - [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) — parent MD; structural precedent for tier system + zero-vs-NaN discipline + compression + lock discipline.
  - [`nightly_attribution.md`](nightly_attribution.md) — wake-up-date rule inherited by all sleep-window operands.
  - [`bb_overnight_gain_proxy.md`](bb_overnight_gain_proxy.md) — validation for the BB overnight-gain proxy chain.
  - [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) — Q24 methodology MD; primary downstream consumer, patched at Stage 3b to cross-ref this catalogue.
- Literature reviews:
  - [`literature/reviews/wearables_sleep_hrv_chronic_illness_review.md`](../literature/reviews/wearables_sleep_hrv_chronic_illness_review.md) — Miller 2022 FR245 staging κ=0.25 "poor" vs timing/duration κ=0.35 "adequate" anchor; Matcham 2024 MDD sleep-regularity relapse anchor for Family B.
  - [`literature/reviews/pem_recovery_trajectory_review.md`](../literature/reviews/pem_recovery_trajectory_review.md) — Mekhael 2022 LC sleep-architecture disturbance anchor; Radin 2021 / 2024 nightly HR persistence anchor for `sleep_hr_avg_spo2`.

---

*Producer-mode methodology MD. Update when (a) the fresh-session review verdict lands and informs r2 compression, (b) Family B operands are implemented and lift the DEFERRED tier, (c) a Family C composite is built and lifts the DEFERRED tier, (d) a new sleep-derived column lands and needs a family placement.*
