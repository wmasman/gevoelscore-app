# Data dictionary — `per_day_master.csv`

**Status**: locked spec, 2026-06-11. Until Phase B builds the dataset,
this file describes the *target* schema. After Phase B it becomes
authoritative on what's actually in the file.

The unified per-day master dataset is **one row per calendar date**
from `2021-08-16` (earliest Garmin coverage) to today. It lives at
`$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` — **outside the
repo** because it inherits raw text fields. See
[methodology/symptom_mention_asymmetry.md](methodology/symptom_mention_asymmetry.md)
and [methodology/nightly_attribution.md](methodology/nightly_attribution.md)
for the binding interpretive rules.

---

## Reading this dictionary

Each row of the table below is one column in `per_day_master.csv`.
Columns are documented with:

- **Name** — the exact column header in the CSV.
- **Class** — one of:
  - `daily_computed` — exists every day in coverage; safe for
    trajectory analyses; missing-of-value means out-of-coverage.
  - `presence_conditioned_positive_evidence` ⚠️ — exists only when the
    column's **section-specific gating flag** is True. The gating flag
    is NOT universally `has_note`: e.g. §9/§10 (v24 categorisation rollup)
    gates on `has_note=True`; §2 (cog/phy/emo load triage) gates on
    `has_intensity_triage=True` (= `intensity_source != ""`). Always
    check the section's preamble for its specific rule; do not assume
    `has_note` applies. Once gated: value > 0 is positive evidence,
    value = 0 (or `_no_info` for §2) on a gated day is *low-specificity*
    about absence, `NaN` on a non-gated day. See
    [methodology/symptom_mention_asymmetry.md](methodology/symptom_mention_asymmetry.md).
  - `derived` — computed from other columns of the master (coverage
    flags, identity, etc.).
- **Source dataset** — which file the column is sourced from (paths
  relative to `$GEVOELSCORE_DATA_PATH/`).
- **Source column** — the name in the source file (may differ from
  the master column name).
- **dtype** — pandas dtype: `int64`, `float64`, `bool`, `category`,
  `object` (string), `datetime64[ns]`.
- **Units / categories** — units of measure or enumerated category
  values.
- **Coverage** — the date range during which the column has data.
- **Missingness rule** — what an absent value means.
- **Notes** — cross-references, derivation rules, gotchas.

---

## Section 0 — identity

| name | class | source | source column | dtype | units / categories | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `date` | daily_computed | computed (calendar index) | — | datetime64[ns] | ISO `YYYY-MM-DD` | full range 2021-08-16 → today | never null | primary key; one row per value |
| `day_of_week` | derived | computed from `date` | — | category | `Mon`, `Tue`, … `Sun` | full | never null | useful for weekday/weekend stratification |
| `era` | derived | computed from `date` | — | category | `pre_score` (< 2022-09-03), `train` (2022-09-03 → 2023-12-31), `validate` (2024-01-01 → today) | full | never null | matches existing crash_v2 era split — pre-registered before the validate-era data came in, so the boundary is methodologically defensible. **Backward-compat label.** For research timeline questions ("is this day pre-LC or LC?") use `lc_phase` below — `era` boundaries are gevoelscore-corpus-driven, not LC-onset-driven. |
| `lc_phase` | derived | computed from `date` | — | category | `pre_corona` (< 2022-03-21), `corona_infection` (2022-03-21 → 2022-04-03), `lc` (>= 2022-04-04) | full | never null | **The research-wide LC timeline indicator (added 2026-06-12, locked by user).** `pre_corona` = healthy training-period baseline window. `corona_infection` = corona-ziek-week (2022-03-21 → 2022-03-27 per the Training-periode span note in `annotations.yaml`) extended through the Fietsweekend Ardennen (2022-04-01 → 2022-04-03, the user-identified trigger / end-of-acute-corona event). `lc` = LC-symptom-onset and onwards, starting the Monday after Ardennen (2022-04-04). See the 2022-04-04 marker in `annotations.yaml` and the `LC_ERA_START` / `CORONA_START` constants in `pipeline/03_consolidate/build_unified_dataset.py`. **For PEM-pacing analyses, gate on `lc_phase == "lc"`.** For healthy-baseline characterisation, gate on `lc_phase == "pre_corona"`. Avoid using `corona_infection` days as either a baseline or analysis target. |

---

## Section 1 — subjective state (gevoelscore + note)

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `gevoelscore` | daily_computed | `raw/directus_exports/day_entries.json` | `score` | float64 (nullable int) | 1-10 (in practice 1-6 dense, 7-10 sparse) | 2022-09-03 → today | NaN when no entry that day | the primary subjective signal |
| `has_note` | derived | computed | — | bool | True when `note_text` is non-empty | full | never null | **mandatory companion** to every §9 + §10 presence-conditioned column (the v24 categorisation rollup). NOT the universal gating flag — §2 presence-conditioned load columns gate on `has_intensity_triage` instead. |
| `note_text` | daily_computed | `raw/directus_exports/day_entries.json` | `note` | object (string) | free text | 2022-09-03 → today | empty string when no note (then `has_note=False`) | **personal data — external only** |

---

## Section 2 — manual load triage (per-day intensity)

⚠️ **`cog_load` / `phy_load` / `emo_load` / `intensity_notes` are
`presence_conditioned_positive_evidence`** — the load assignment is
derived from upstream calendar events + day-notes. A blank cog_load
does NOT mean cog intensity was zero; it means no signal was found.
Gate on `intensity_source != ""` (the companion flag, analogous to
`has_note` for §9/§10) before interpreting blanks. See
[methodology/symptom_mention_asymmetry.md](methodology/symptom_mention_asymmetry.md)
for the three-state semantics.

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `cog_load` | presence_conditioned ⚠️ | `processed/manual_triage/per_day_intensity.csv` | `cog` | float64 (nullable int) | 1, 2, 3 (mild / moderate / severe event intensity) | rows with non-empty `intensity_source` only | NaN when `intensity_source` empty (not triaged); NaN when `intensity_source = bulk_triage_*_no_info` (reviewed, no signal found) — the source flag distinguishes the two | see [methodology/methodology.md](methodology/methodology.md) §2; gating rule: `intensity_source != ""` |
| `phy_load` | presence_conditioned ⚠️ | `processed/manual_triage/per_day_intensity.csv` | `phy` | float64 (nullable int) | 1, 2, 3 | same | same | |
| `emo_load` | presence_conditioned ⚠️ | `processed/manual_triage/per_day_intensity.csv` | `emo` | float64 (nullable int) | 1, 2, 3 | same | same | |
| `intensity_source` | daily_computed | `processed/manual_triage/per_day_intensity.csv` | `source` | category | `consolidation_YYYY-MM-DD`, `bulk_triage_YYYY_YYYY-MM-DD`, `bulk_triage_YYYY_no_info`, `manual_*`, `triage_notes_classified`, `pwc_cross_validation_2026-06-11` | matches `per_day_intensity.csv` | empty string when not in source (= not yet triaged); a non-empty value is the **mandatory companion** to interpret cog/phy/emo loads | `*_no_info` is presence-conditioned **explicit absence** (user reviewed, found no load-bearing material). Distinct from empty source (= unreviewed). **Rate-computation caveat (Layer 2 audit 2026-06-12)**: per-quarter rates of the form `% cog/phy/emo_load notna among has_intensity_triage=True days` are not directly comparable across quarters when the `_no_info` share differs. Quarters with high `_no_info` counts shrink the load-assignable denominator and inflate the rate. For honest cross-quarter comparison, split `has_intensity_triage=True` into `_no_info` and context-sufficient subsets and compute rates within the context-sufficient subset only. Observed example: 2025Q3 = 92 triaged / 61 `_no_info` / 31 context-sufficient → 74.2% cog-rate; 2024Q1 = 91 triaged / 1 `_no_info` / 90 context-sufficient → 26.7% cog-rate; absolute cog-assigned counts are 23 vs 24 across the two quarters. |
| `intensity_notes` | presence_conditioned ⚠️ | `processed/manual_triage/per_day_intensity.csv` | `notes` | object (string) | free text | matches | empty string when no notes | **personal data — external only**; same gating rule as cog/phy/emo |

---

## Section 3 — research-derived crash labels

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `is_crash` | daily_computed | `processed/crash_labels/labels_crash_v2.csv` | `is_crash` (or derived from `label`) | bool | True if day inside a v2 crash episode | 2022-09-03 → today | False outside any episode | see [methodology/crash_v2_definition.md](methodology/crash_v2_definition.md) |
| `is_dip` | daily_computed | `processed/crash_labels/labels_crash_v2.csv` | `is_dip` (or derived) | bool | True if day is a v2 isolated single-day dip | 2022-09-03 → today | False otherwise | |
| `crash_episode_id` | daily_computed | `processed/crash_labels/labels_crash_v2.csv` | `episode_id` | object (string) | episode identifier (e.g. `EP_2023_06_05`) | matches | empty when not in an episode | tags every day inside a crash episode AND every single-day `is_dip` day; 108 distinct IDs across 182 in-episode days (= 29 crash streaks + 79 isolated dips, per Layer 1 audit 2026-06-12) |
| `is_sub_threshold_dip` | daily_computed | `processed/crash_labels/sub_threshold_dips.csv` | derived | bool | True if day is user-confirmed sub-threshold dip | 2022-09-03 → today | False otherwise | distinct from `is_dip` (research-derived); user-triaged |
| `dip_type` | daily_computed | `processed/crash_labels/sub_threshold_dips.csv` | `dip_type` | category | `general`, `brainfog` | only where `is_sub_threshold_dip=True` | NaN otherwise | brainfog dips added 2026-06-11 from Q2 review |

---

## Section 4 — Garmin daily activity

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `total_steps` | daily_computed | `processed/garmin/daily_uds.csv` | `total_steps` | float64 (nullable int) | step count | 2021-08-16 → today (1.754 days, 98.8% coverage) | NaN on FIT gap days | from Garmin UDS export |
| `moderate_min` | daily_computed | `processed/garmin/daily_uds.csv` | `moderate_min` | float64 (nullable int) | minutes | same | NaN on gap | UDS-computed intensity minutes |
| `vigorous_min` | daily_computed | `processed/garmin/daily_uds.csv` | `vigorous_min` | float64 (nullable int) | minutes | same | NaN on gap | |
| `total_calories` | daily_computed | `processed/garmin/daily_uds.csv` | `total_calories` | float64 | kcal | same | NaN on gap | Garmin active+resting calories combined |
| `highly_active_sec` | daily_computed | `processed/garmin/daily_uds.csv` | `highly_active_sec` | float64 (nullable int) | seconds | same (1734 / 1755) | NaN on gap | Wave 2 add 2026-06-12. Finer-grained intensity bucket from UDS; complements `vigorous_min`. |
| `active_sec` | daily_computed | `processed/garmin/daily_uds.csv` | `active_sec` | float64 (nullable int) | seconds | same (1734 / 1755) | NaN on gap | Wave 2 add 2026-06-12. Finer-grained intensity bucket from UDS; complements `moderate_min`. |
| `is_vigorous_day` | daily_computed | `processed/garmin/daily_uds.csv` | `is_vigorous_day` | bool | True if Garmin classified the day as containing a vigorous burst | 2021-08-16 → today (896 / 1755 ≈ 51% populated; Garmin only emits the flag when a vigorous burst was actually detected, so empty ≠ NaN strictly) | empty when no vigorous burst (treat as False for analysis) | Wave 2 add 2026-06-12. Binary daily flag, useful as Wiggers C2 covariate and as an E3 supporting axis. |
| `daily_step_goal` | daily_computed | `processed/garmin/daily_uds.csv` | `daily_step_goal` | float64 (nullable int) | step target | 2021-08-16 → today (1734 / 1755) | NaN on gap | Wave 2 add 2026-06-12. Garmin's adaptive step target. Use as personal-anchored reference for Wiggers E1 (personal step threshold) — values drift over the timeline, so absolute step counts should be read against this rather than a fixed cutoff. |
| `steps_above_goal_flag` | derived | computed from `total_steps` + `daily_step_goal` | — | bool | True iff `total_steps >= daily_step_goal` | matches inputs (1732 / 1755) | empty when either input missing | Wave 2 add 2026-06-12. Convenience boolean for Wiggers E1 dose-response binning. Personal-anchored "did I exceed my target" flag, not a fixed-threshold above-X-steps. |

---

## Section 5 — Garmin heart rate

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `resting_hr` | daily_computed | `processed/garmin/daily_uds.csv` | `resting_hr` | float64 | bpm | 2021-08-16 → today (1731 of 1755 days) | NaN on FIT-gap day; Garmin's algorithmic RHR is passed through directly (no sanity filter — observed range is 47-65 bpm with 0 outliers, see [methodology/garmin_indicators_audit.md](methodology/garmin_indicators_audit.md)) | **nightly attribution applies** — Garmin computes RHR during sleep; the value is attributed to the wake-up date. See [methodology/nightly_attribution.md](methodology/nightly_attribution.md) |
| `min_hr` | daily_computed | `processed/garmin/daily_uds.csv` | `min_hr` | float64 | bpm | same | NaN on gap | |
| `max_hr` | daily_computed | `processed/garmin/daily_uds.csv` | `max_hr` | float64 | bpm | same | NaN on gap | |
| `max_avg_hr_uds` | daily_computed | `processed/garmin/daily_uds.csv` | `max_avg_hr` | float64 | bpm | same | NaN on gap | Garmin UDS "max-of-averages" metric (max value across averaging windows) — NOT a daily mean. Use cautiously; the daily true mean is not in UDS. **Layer 3**: Spearman with `max_hr` = +0.97 on LC frame (n=1502); treat as one signal in regression / VAR / CCF (pick `max_hr`). See memory `feedback_definitional_pair_guardrail`. |

---

## Section 6 — Garmin exertion features (engineered)

**Two versions live side by side in the master.** v3.1 columns are
retained for backward compatibility with HA01b / HA02c results;
v3.2 lagged columns are the default for new analyses (see
[`methodology/garmin_indicators_audit.md`](methodology/garmin_indicators_audit.md)
§ Rule for new analyses and the column-choice matrix in
[`wiggers_testable_hypotheses.md`](wiggers_testable_hypotheses.md)).

### v3.1 (legacy, backward compat)

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `exertion_class` | daily_computed | `processed/garmin/activity_features_daily.csv` | `exertion_class` | category | `none`, `very_light`, `light`, `moderate`, `heavy`, `very_heavy` | 2021-08-16 → today (1.754 days) | NaN on gap | v3.1 spec, 4-axis percentile rank against 30-day **trailing** rolling baseline that includes the candidate day. **Known issue**: sustained pushes rebase into their own reference frame; use `exertion_class_lagged` for new work. See `analyses/garmin_exploration/exertion-class-definition.md`. **Note**: `none` (sedentary day inside coverage; ≈26.5% of `has_garmin_uds=True` days per Layer 1 audit 2026-06-12) is distinct from `NaN` (out-of-coverage). `very_light` does not appear in the current dataset — the 4-axis rank may always route low-activity days to `none`; worth re-confirming against the v3.1 spec. |
| `effective_exertion_min` | daily_computed | `processed/garmin/activity_features_daily.csv` | `effective_exertion_min` | float64 | minutes | same | NaN only on Garmin UDS gap days (1734/1734 = 100% fill within `has_garmin_uds=True` after the 2026-06-12 re-extract that extended `ANALYSIS_START` to 2021-08-16) | raw minutes; not affected by the v3.1/v3.2 baseline split |
| `step_z_30d` | daily_computed | `processed/garmin/activity_features_daily.csv` | `step_z_30d` | float64 | z-score of daily steps vs 30d rolling baseline | same | NaN on first 20 days of coverage (2021-08-16 → 2021-09-04, the rolling-baseline warmup) and after multi-day Garmin gaps — empirically 1712/1734 = 98.7% fill within `has_garmin_uds=True` after the 2026-06-12 re-extract | step-based; do not interpret as a generic "intensity z-score" — earlier draft renamed it from the misleading `intensity_z_score` proxy. **For new work use `step_rank_lagged`** (same rolling-baseline-contamination issue as `exertion_class`). |

### v3.2 lagged baseline (default for new analyses, added 2026-06-12)

Baseline window `[d-90, d-30]` — 60 days ending 30 days BEFORE the
candidate day; excludes the recent push period from its own reference.
Computed by
[`analyses/garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py`](analyses/garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py);
specced in
[`analyses/garmin_exploration/activity-labels/spec/severity_spec.md`](analyses/garmin_exploration/activity-labels/spec/severity_spec.md)
§ Lagged baseline + trend slope.

| name | class | source | source column | dtype | units / values | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `exertion_class_lagged` | daily_computed | `processed/garmin/activity_features_daily.csv` | `exertion_class_lagged` | category | `none`, `light`, `moderate`, `heavy`, `very_heavy` | 2021-08-16 → today | NaN before the 90-day baseline window is full and after multi-day Garmin gaps. **Fill 1664/1734 = 96.0% within `has_garmin_uds=True`** after the 2026-06-12 re-extract from 2021-08-16 (the missing ~70 days are the start-of-coverage warmup 2021-08-16 → ~2021-11-13 plus a handful of Garmin gap days) | composite of 4 lagged per-axis classes; use for overexertion thresholding (Wiggers B4, D5, H2, H4) |
| `exertion_rank_composite_lagged` | daily_computed | derived in `pipeline/03_consolidate/build_unified_dataset.py` | `max(eff_exertion_rank_lagged, step_rank_lagged, max_hr_rank_lagged, vigorous_min_rank_lagged)` | float64 | 0.0 – 1.0 | same | same (96.0% fill within `has_garmin_uds=True`) | continuous companion to `exertion_class_lagged`; use for scaling, correlation, cross-correlation lag-profile (Wiggers A1, H1, H3, H5) |
| `eff_exertion_rank_lagged` | daily_computed | `processed/garmin/activity_features_daily.csv` | `effective_exertion_rank_lagged` | float64 | 0.0 – 1.0 | same | same | per-axis input to the composite; for per-axis comparison (Wiggers E3) |
| `step_rank_lagged` | daily_computed | `processed/garmin/activity_features_daily.csv` | `step_rank_lagged` | float64 | 0.0 – 1.0 | same | same | steps axis; supports E1 (personal step threshold) and E3 |
| `max_hr_rank_lagged` | daily_computed | `processed/garmin/activity_features_daily.csv` | `max_hr_rank_lagged` | float64 | 0.0 – 1.0 | same | same | HR-peak axis; supports H2 (activity-invisible crashes use low-HR-rank as a defining criterion) |
| `vigorous_min_rank_lagged` | daily_computed | `processed/garmin/activity_features_daily.csv` | `vigorous_min_rank_lagged` | float64 | 0.0 – 1.0 | same | same | intensive-minutes axis; supports A4 (sustained vs spike) and E3 |
| `push_burden_7d_lagged` | daily_computed | `processed/garmin/activity_features_daily.csv` | `push_burden_7d_lagged` | int | 0 – 7 | full | 0 on days where the rolling 7-day window has no day with rank ≥ 0.75. **Fill 1734/1734 = 100% within `has_garmin_uds=True`** after the 2026-06-12 re-extract (0 emitted for pre-warmup days where no lagged-rank threshold is met). | count of days in last 7 where any lagged axis rank ≥ 0.75; v3.2 fix for the contamination that dropped v3.1 `push_burden_7d` |
| `effective_exertion_slope_28d` | daily_computed | `processed/garmin/activity_features_daily.csv` | `effective_exertion_slope_28d` | float64 | log-units per day | same | NaN before 28d of history available. **Fill 1713/1734 = 98.8% within `has_garmin_uds=True`** after the 2026-06-12 re-extract | OLS slope of log(1 + effective_exertion_min) over trailing 28 days; first-class signal for creeping-floor / sustained-creep patterns (Wiggers E2) |
| `class_axis_A_eff` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_A_eff` | category | `none`, `light`, `moderate`, `heavy`, `very_heavy` | 2021-08-16 → today (1734 / 1734 within `has_garmin_uds=True` after the 2026-06-12 re-extract) | NaN only on Garmin gap days | Wave 2 add 2026-06-12. Per-axis v3.1 class for effective-exertion axis. Supports Wiggers E3 (per-axis comparison) and class attribution ("which axis drove `exertion_class`"). |
| `class_axis_B_step` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_B_step` | category | same | same | same | Wave 2 add 2026-06-12. Per-axis v3.1 class for step axis. |
| `class_axis_C_maxhr` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_C_maxhr` | category | same | same | same | Wave 2 add 2026-06-12. Per-axis v3.1 class for max-HR axis. |
| `class_axis_D_vig` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_D_vig` | category | same | same | same | Wave 2 add 2026-06-12. Per-axis v3.1 class for vigorous-minutes axis. |
| `class_axis_A_eff_lagged` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_A_eff_lagged` | category | same | 2021-08-16 → today (1664 / 1734 = 96.0% within `has_garmin_uds=True` after the 2026-06-12 re-extract) | NaN before 90d warmup (~2021-11-13) + after Garmin gaps | Wave 2 add 2026-06-12. Per-axis v3.2 lagged class for effective-exertion axis. **Default for new analyses** (no rolling-baseline contamination). |
| `class_axis_B_step_lagged` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_B_step_lagged` | category | same | same | same | Wave 2 add 2026-06-12. Per-axis v3.2 lagged class for step axis. |
| `class_axis_C_maxhr_lagged` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_C_maxhr_lagged` | category | same | same | same | Wave 2 add 2026-06-12. Per-axis v3.2 lagged class for max-HR axis. |
| `class_axis_D_vig_lagged` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_D_vig_lagged` | category | same | same | same | Wave 2 add 2026-06-12. Per-axis v3.2 lagged class for vigorous-minutes axis. |
| `above_baseline_streak` | daily_computed | `processed/garmin/activity_features_daily.csv` | `above_baseline_streak` | int | consecutive days where the day-of-interest's composite rank ≥ baseline threshold | 2021-08-16 → today (1734 / 1734 = 100% within `has_garmin_uds=True` after the 2026-06-12 re-extract) | 0 on days where no qualifying streak exists | Wave 2 add 2026-06-12. Direct count of how many days in a row the user has been above their baseline. Complements `effective_exertion_slope_28d` for Wiggers E2 (creeping-floor detection) — slope tracks gradual rise, streak tracks consecutive elevation. NB: uses the v3.1 baseline (trailing 30d) — when a v3.2 lagged streak becomes available upstream, propagate it alongside. |

### v3.2 LC-era-only lagged variants (added 2026-06-12)

Same lagged-baseline window `[d-90, d-30]` as the all-era v3.2 set above,
but the baseline values are **restricted to dates >= 2022-04-04**
(`LC_ERA_START`, the locked LC analysis boundary; see §0 `lc_phase`).
This makes the rank "today's load relative to the user's LC-era normal"
rather than relative to a baseline that mixes pre-LC healthy-capacity
days with LC-era days.

**Use which when**:
- **All-era variants** (the `*_lagged` set above): trajectory characterisation, "how have I changed from pre-LC capacity" questions, cross-era comparison.
- **LC-era variants** (the `*_lagged_lcera` set below): PEM-pacing analyses, Wiggers hypotheses on LC-era pacing, "is today heavy relative to my current normal" questions. Avoids the early-LC under-ranking that the all-era variant produces for ~120 days of train-era when the lagged window still reaches into pre-LC days.

| name | class | source | source column | dtype | units / values | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `exertion_class_lagged_lcera` | daily_computed | `processed/garmin/activity_features_daily.csv` | `exertion_class_lagged_lcera` | category | `none`, `light`, `moderate`, `heavy`, `very_heavy` | 2021-08-16 → today | NaN before the LC-era window has ≥ 40 valid days inside it (effective start ≈ 2022-07-03 = LC_ERA_START + 90d warmup) | composite of 4 LC-era-only per-axis classes. **For PEM-pacing / Wiggers analyses.** ~82.6% fill within `has_garmin_uds=True`. |
| `exertion_rank_composite_lagged_lcera` | daily_computed | derived in `pipeline/03_consolidate/build_unified_dataset.py` | `max(eff_exertion_rank_lagged_lcera, step_rank_lagged_lcera, max_hr_rank_lagged_lcera, vigorous_min_rank_lagged_lcera)` | float64 | 0.0 – 1.0 | same | same | continuous companion to `exertion_class_lagged_lcera`. **For PEM-pacing correlation / lag-profile analyses.** |
| `eff_exertion_rank_lagged_lcera` | daily_computed | `processed/garmin/activity_features_daily.csv` | `effective_exertion_rank_lagged_lcera` | float64 | 0.0 – 1.0 | same | same | per-axis input to the LC-era composite. |
| `step_rank_lagged_lcera` | daily_computed | `processed/garmin/activity_features_daily.csv` | `step_rank_lagged_lcera` | float64 | 0.0 – 1.0 | same | same | LC-era steps axis. |
| `max_hr_rank_lagged_lcera` | daily_computed | `processed/garmin/activity_features_daily.csv` | `max_hr_rank_lagged_lcera` | float64 | 0.0 – 1.0 | same | same | LC-era HR-peak axis. |
| `vigorous_min_rank_lagged_lcera` | daily_computed | `processed/garmin/activity_features_daily.csv` | `vigorous_min_rank_lagged_lcera` | float64 | 0.0 – 1.0 | same | same | LC-era intensive-minutes axis. |
| `push_burden_7d_lagged_lcera` | daily_computed | `processed/garmin/activity_features_daily.csv` | `push_burden_7d_lagged_lcera` | int | 0 – 7 | full | always populated (0 when no LC-era rank meets threshold in last 7 days) | count of days in last 7 where any LC-era axis rank ≥ 0.75. v3.2 LC-era variant of `push_burden_7d_lagged`. |
| `class_axis_A_eff_lagged_lcera` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_A_eff_lagged_lcera` | category | `none`, `light`, `moderate`, `heavy`, `very_heavy` | same | same | LC-era per-axis class for effective-exertion. |
| `class_axis_B_step_lagged_lcera` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_B_step_lagged_lcera` | category | same | same | same | LC-era per-axis class for step axis. |
| `class_axis_C_maxhr_lagged_lcera` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_C_maxhr_lagged_lcera` | category | same | same | same | LC-era per-axis class for max-HR axis. |
| `class_axis_D_vig_lagged_lcera` | daily_computed | `processed/garmin/activity_features_daily.csv` | `class_axis_D_vig_lagged_lcera` | category | same | same | same | LC-era per-axis class for vigorous-minutes axis. |

Note: `effective_exertion_slope_28d` is **not duplicated** as an `_lcera` variant — its 28-day window slides fully into LC era within ~4 weeks of `LC_ERA_START`, so a separate variant would not differ except at the boundary.

### v3.2 LC-era z-score lagged variants (`*_lagged_lcera_z`, added 2026-06-14)

Same `[d-90, d-30]` LC-era-only rolling window as the percentile-rank variants above, but for **raw-continuous baseline channels** (stress / RHR / BB / respiration). The z-score formulation uses **median + 1.4826 × MAD** (normal-equivalent SD) over the lookback window, gating on ≥ 5 valid LC-era days. Returns NaN ("") when the window is too sparse, the candidate day's value is missing, or MAD is zero.

**Naming convention**: the `_z` suffix distinguishes these from the percentile-rank `*_lagged_lcera` family above. The percentile-rank pattern is the natural lagged variant for rank-source columns (the exertion family); the z-score pattern is the natural lagged variant for raw-continuous-source columns (stress / HR / BB / respiration).

**Use which when**:
- **Percentile-rank `*_lagged_lcera`** (above): rank-source channels; comparison "where today sits in the 60-day LC-era baseline window".
- **Z-score `*_lagged_lcera_z`** (below): raw-continuous channels; comparison "how many SD-equivalents above/below the 60-day LC-era median is today". Used by [`citalopram_dose_response_stress_mean_sleep.md`](methodology/citalopram_dose_response_stress_mean_sleep.md) §4.3-C Sensitivity Column and the [`citalopram_phase_stratification.md`](methodology/citalopram_phase_stratification.md) framework.

Built inline in `pipeline/03_consolidate/build_unified_dataset.py` post-pass (no external script-11 dependency); validated 2026-06-14 against the on-the-fly implementation in `analyses/garmin_exploration/intervention_effects/dose_response.py` to ≤ 5e-5 rounding tolerance across all 6 channels.

| name | class | source | source column | dtype | units / values | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `stress_mean_sleep_lagged_lcera_z` | daily_computed | derived in `pipeline/03_consolidate/build_unified_dataset.py` | computed from `stress_mean_sleep` | float64 | SD-units against rolling LC-era median + 1.4826*MAD; typical range ~−3 to +3 | 2022-05-08 → today | ~82.4% fill within `has_garmin_sleep=True`. NaN before LC-era window has ≥ 5 valid days. | v3.2 z-score lagged variant of `stress_mean_sleep`. **Used by dose_response Sensitivity C + downstream §5b stress-trigger tests.** Citalopram-dose-modulated channel (CONFIRMED per [`citalopram_dose_response`](methodology/citalopram_dose_response_stress_mean_sleep.md) §5.6.1). |
| `all_day_stress_avg_lagged_lcera_z` | daily_computed | same | computed from `all_day_stress_avg` | float64 | same | 2022-05-08 → today | ~83.6% fill | v3.2 z-score lagged variant of `all_day_stress_avg`. Citalopram-dose-modulated channel (CONFIRMED, strongest signal of the v3 multi-channel sweep). **Used by C4b + Wiggers C2/C3/C4 + Personal P5b.** |
| `resting_hr_lagged_lcera_z` | daily_computed | same | computed from `resting_hr` | float64 | same | 2022-05-08 → today | ~78.0% fill | v3.2 z-score lagged variant of `resting_hr`. Citalopram dose-response **weakly consistent** (sign matches, buildup CI brushes zero). **Used by Wiggers A1/A2/A3 RHR-shape tests.** |
| `respiration_avg_sleep_lagged_lcera_z` | daily_computed | same | computed from `respiration_avg_sleep` | float64 | same | 2022-05-08 → today | ~23.0% fill (sparse source channel) | v3.2 z-score lagged variant of `respiration_avg_sleep`. Citalopram dose-response **REJECTED** (informative-by-rejection per [REJECTED.md](REJECTED.md) `RESP-SSRI`). **Used by Wiggers G1.** |
| `bb_lowest_lagged_lcera_z` | daily_computed | same | computed from `bb_lowest` | float64 | same | 2022-05-08 → today | ~82.6% fill | v3.2 z-score lagged variant of `bb_lowest`. Citalopram-dose-modulated channel (CONFIRMED). **Used by Personal P4a BB-floor-crossing tests.** |
| `bb_overnight_gain_lagged_lcera_z` | daily_computed | same | computed from `bb_overnight_gain` | float64 | same | 2024-12-17 → today (effectively) | ~32.1% fill (source coverage starts 2024-09-18 per [§2b](methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain)) | v3.2 z-score lagged variant of `bb_overnight_gain`. Citalopram dose-response **partial** (no 2024 buildup data). **Used by Personal P4b BB-trajectory tests.** |

### Citalopram plasma proxy (`dose_plasma_mg`, added 2026-06-14)

| name | class | source | source column | dtype | units / values | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `dose_plasma_mg` | daily_computed | derived in `pipeline/03_consolidate/build_unified_dataset.py` | computed from documented citalopram dose-step dates | float64 | mg of citalopram plasma steady-state | full (0 mg pre-2024-04-09) | always populated | PK-smoothed one-compartment first-order model with t_half = 35h (citalopram SPC, EMA). Step inputs at the 6 documented dose-change dates (verified against `annotations.yaml` Citalopram-fase-1...6 spans). Used by [`citalopram_phase_stratification`](methodology/citalopram_phase_stratification.md) §5.B dose-adjusted-predictor pattern. Canonical formula at [`citalopram_dose_response`](methodology/citalopram_dose_response_stress_mean_sleep.md) §2.3. |

---

## Section 7 — Garmin sleep-stress (nightly, wake-up-date attributed)

All columns in this section follow the wake-up-date rule. See
[methodology/nightly_attribution.md](methodology/nightly_attribution.md).

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `sleep_start_gmt` | daily_computed | `processed/garmin/sleep_stress_nightly.csv` | `sleep_start_gmt` | datetime64[ns, UTC] | timestamp | 2021-08-16 → today (1.740 nights) | NaN if no sleep recorded | the row's `date` is the wake-up date; this is the start of the night that ended on `date` |
| `sleep_end_gmt` | daily_computed | `processed/garmin/sleep_stress_nightly.csv` | `sleep_end_gmt` | datetime64[ns, UTC] | timestamp | same | NaN if no sleep | wake-up moment |
| `stress_mean_sleep` | daily_computed | `processed/garmin/sleep_stress_nightly.csv` | `stress_mean` | float64 | Garmin stress 0-100 | same | NaN if no sleep or sleep_valid_flag=False | mean across the sleep window |
| `stress_stdev_sleep` | daily_computed | `processed/garmin/sleep_stress_nightly.csv` | `stress_stdev` | float64 | same scale | same | NaN if invalid | within-window variability |
| `sleep_valid_flag` | daily_computed | `processed/garmin/sleep_stress_nightly.csv` | `valid` | bool | True if enough samples to trust | same | False if too few samples | gate stress_mean_sleep on this |
| `sleep_start_afternoon_flag` | derived | computed from `sleep_start_gmt` | — | bool | True iff `sleep_valid_flag=True` AND `sleep_start_gmt` converted to Europe/Amsterdam (DST-correct) has `hour < 17` | same as `sleep_valid_flag` | NaN/blank when `sleep_valid_flag=False` | Layer 2 audit 2026-06-12 — "Definition A" flag for afternoon `sleep_start_gmt` values; 144 / 1707 valid-sleep nights = 8.44% at landing. See [methodology/nightly_attribution.md](methodology/nightly_attribution.md) §"Afternoon `sleep_start_gmt` values" for context, co-occurrence with crash labels and umbrella event_labels, and the rejected Definition B (additional `sleep_duration_min > p95` constraint — degenerate at n=1 on this dataset). |
| `bedtime_hour_local` | derived | computed from `sleep_start_gmt` | — | float64 | fractional local hour (0.0-23.99), Europe/Amsterdam DST-correct | same as `sleep_valid_flag` | NaN when `sleep_valid_flag=False` | Wave 1 add 2026-06-12. Wiggers F4 input. Raw fractional hour preserves minute precision (21:30 → 21.5). After-midnight bedtimes appear as 0-12 — handle wrap-around in downstream variance/mean calculations (e.g. add 24 to values < 12 when computing rolling std). |
| `sleep_duration_min` | derived | computed from `sleep_start_gmt` + `sleep_end_gmt` | — | float64 | minutes | same as `sleep_valid_flag` | NaN when `sleep_valid_flag=False` or either timestamp missing | Wave 1 add 2026-06-12. Wiggers F1 (sleep duration ↑ during PEM). For the long-sleep example (2023-02-05 inside crash-006): 951 min. |
| `bedtime_std_7d` | derived | rolling 7-day std of `bedtime_hour_local` | — | float64 | hours | full (≥2 valid prior bedtimes required) | NaN until 2 valid prior bedtimes accumulate; afternoon-flagged nights excluded from the window | Wave 1 add 2026-06-12. Wiggers F4 (bedtime inconsistency → next-day energy). After-midnight wrap handled by adding 24 to values < 12 before the std calculation, so 22:00 / 23:30 / 00:30 has small variance (22.0 / 23.5 / 24.5) instead of being inflated by the 24h discontinuity. Afternoon-start nights (`sleep_start_afternoon_flag=True`) are excluded from the rolling window as aberrant per Layer 2 audit. |
| `sleep_deep_min` | daily_computed | `processed/garmin/sleep_extras_daily.csv` | `sleep_deep_min` | float64 | minutes | 2021-08-16 → today (1713 / 1755 = 98.8%) | NaN on gap | Wave 3 add 2026-06-12. Wiggers F2 (deep-sleep deviation ↔ gevoelscore). |
| `sleep_light_min` | daily_computed | `processed/garmin/sleep_extras_daily.csv` | `sleep_light_min` | float64 | minutes | same | NaN on gap | Wave 3 add 2026-06-12. **No `sleep_rem_min` exists**: Forerunner 245 (Elevate V3 sensor) does not produce REM-stage classification; all non-deep / non-awake sleep aggregates into `sleep_light_min`. |
| `sleep_awake_min` | daily_computed | `processed/garmin/sleep_extras_daily.csv` | `sleep_awake_min` | float64 | minutes | same | NaN on gap | Wave 3 add 2026-06-12. Within-night awake time. |
| `sleep_unmeasurable_min` | daily_computed | `processed/garmin/sleep_extras_daily.csv` | `sleep_unmeasurable_min` | float64 | minutes | same | NaN on gap | Wave 3 add 2026-06-12. Time the device could not classify (off-wrist, motion, sensor dropout). High values → low confidence in the stage breakdown for that night. |
| `respiration_avg_sleep` | daily_computed | `processed/garmin/sleep_extras_daily.csv` | `respiration_avg_sleep` | float64 | breaths/min | 2021-08-16 → today (1704 / 1755 = 97.1%) | NaN on gap | Wave 3 add 2026-06-12. Wiggers G1 (respiration elevation → stuck sympathetic / poor recovery). Sleep-window variant; compare with `respiration_max_24h` for waking-vs-sleep stratification. |
| `respiration_max_sleep` | daily_computed | `processed/garmin/sleep_extras_daily.csv` | `respiration_max_sleep` | float64 | breaths/min | same | NaN on gap | Wave 3 add 2026-06-12. Highest respiration in the sleep window. |
| `respiration_min_sleep` | daily_computed | `processed/garmin/sleep_extras_daily.csv` | `respiration_min_sleep` | float64 | breaths/min | same | NaN on gap | Wave 3 add 2026-06-12. Lowest respiration in the sleep window. |
| `spo2_avg_sleep` | daily_computed | `processed/garmin/sleep_extras_daily.csv` | `spo2_avg_sleep` | float64 | percent (e.g. 92.28) | 2021-08-16 → today (1520 / 1755 = 86.6%) | NaN on gap; lower fill than other sleep extras because SpO2 measurement requires the `Pulse Ox Sleep Mode` toggle and the user did not always have it enabled | Wave 3 add 2026-06-12. Wiggers G4 (deprioritised per Wiggers; included for parallel-extraction cheapness). |
| `spo2_min_sleep` | daily_computed | `processed/garmin/sleep_extras_daily.csv` | `spo2_min_sleep` | int | percent | same | NaN on gap | Wave 3 add 2026-06-12. Lowest SpO2 in the sleep window. |

---

## Section 7B — Garmin physiological extras (UDS-derived: Body Battery, all-day stress, 24h respiration, 24h SpO2)

All columns here propagated from `processed/garmin/uds_extras_daily.csv`
(extracted by [`pipeline/01_extract/garmin_uds_extras.py`](pipeline/01_extract/garmin_uds_extras.py)
from UDS JSON; no FIT parsing). Wave 3 add 2026-06-12.

**Negative-value sentinel policy (added 2026-06-12 per Layer 1 Wiggers
sentinel audit)**: Garmin emits negative integers (-1, -2 for stress
columns; -4, -5 for `bb_during_sleep_value`) as a "no data" sentinel on
some days. These values are physically impossible on the underlying
0-100 scales, so they cannot be real measurements. The build script
filters them to blank via `drop_neg_sentinel()` for the four affected
columns: `all_day_stress_avg`, `awake_stress_avg`, `asleep_stress_avg_uds`,
`bb_during_sleep_value`. *_stress_max values that hit 0 only co-occur
with the negative-avg sentinels they accompany, so the day-level
"no data" condition is already captured by the avg-channel drop and
the max-channel zeros are left raw. Class-3 legitimate zeros (sleep-stage
minutes, BB charge/drain on no-net-change days) are real states and stay.
Two dates (2025-11-19, 2025-11-24) have `sleep_valid_flag=True` but UDS
asleep_stress sentinel — these are real Garmin-internal channel
discrepancies; for those nights analysts should use `stress_mean_sleep`
(FIT-derived) instead.

**Device caveat**: the Forerunner 245 (Elevate V3 sensor) does NOT
produce **nightly HRV Status** — that feature requires the Elevate V4
sensor (Forerunner 265+, fēnix 7, etc.). HRV-bearing FIT messages in
this user's sleep type-49 files are undocumented `unknown_273/274/276`
that the community has not decoded. Wiggers B1-B5 and the HRV-dependent
parts of H1-H5 are hardware-blocked on this device, not extraction-
blocked. See [`methodology/garmin_indicators_audit.md`](methodology/garmin_indicators_audit.md)
§ HRV — hardware blocked.

### Body Battery (11 columns)

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `bb_charged_24h` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `bb_charged_24h` | int | BB units (0-100 scale) | 2021-08-16 → today (1732 / 1755 = 98.7%) | NaN on gap | Total BB recharge over the calendar day. |
| `bb_drained_24h` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `bb_drained_24h` | int | BB units | same | NaN on gap | Total BB drain over the calendar day. Wiggers D4 (BB declines steeply around crashes). |
| `bb_highest` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `bb_highest` | int | BB units | same | NaN on gap | Daily peak BB. Wiggers D3 (higher floor / higher peak → fewer crashes). **Layer 3**: Spearman with `bb_sleep_end_value` = +0.99 on LC frame (n=593); treat as one signal in regression / VAR / CCF (pick `bb_sleep_end_value`). See memory `feedback_definitional_pair_guardrail`. |
| `bb_lowest` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `bb_lowest` | int | BB units | same | NaN on gap | Daily BB floor. Wiggers D3 (BB floor coincides with fewer crashes). |
| `bb_sleep_start_value` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `bb_sleep_start_value` | int | BB units | **first non-null 2024-07-08** → today (667 / 1755 = 38.0%) | NaN unless sleep window AND BB measurement aligned; ALSO structurally absent pre-2024-07-08 (pipeline did not extract earlier) | BB at sleep onset (evening "battery left"). **Coverage start verified 2026-06-14 in Session C** — earlier than `bb_sleep_end_value` because sleep-start uses a different extraction path. |
| `bb_sleep_end_value` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `bb_sleep_end_value` | int | BB units | **first non-null 2024-09-18** → today (593 / 1755 = 33.8%) | NaN unless sleep window AND BB measurement aligned; ALSO structurally absent pre-2024-09-18 (pipeline did not extract earlier) | **Morning BB** = BB at wake-up. **Wiggers D5** (paradoxically high morning BB after overexertion → crash risk). **Coverage start verified 2026-06-14 in Session C** — pre-2024-09-18 boundaries cannot use this column. |
| `bb_during_sleep_value` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `bb_during_sleep_value` | int | BB units | **first non-null 2023-12-18** → today (~861 / 1755 after the 2026-06-12 sentinel filter dropped 2 negative values) | NaN if not aligned **OR** sentinel-filtered (see policy note above). Affected dates: 2024-02-19 (-4 → blank), 2024-07-16 (-5 → blank). Pre-2023-12-18 structurally absent. | BB peak during the sleep window. **Layer 3**: Spearman with `bb_overnight_gain` = +1.00 on LC frame (n=593); rho=1.000 needs definitional-vs-empirical verification (see Update log 2026-06-12 Layer 3). Treat as one signal in regression / VAR / CCF (pick `bb_overnight_gain` for Wiggers D2 alignment). **Coverage start verified 2026-06-14 in Session C**. |
| `bb_overnight_gain` | derived | computed in `pipeline/01_extract/garmin_uds_extras.py` | `bb_sleep_end_value - bb_sleep_start_value` | int | BB units | **first non-null 2024-09-18** → today (matches `bb_sleep_end_value`; 593 / 1755 = 33.8%) | NaN when either input missing; structurally absent pre-2024-09-18 because the Garmin UDS `SLEEPEND` stat type did not exist before then | **Wiggers D2 directly** (BB overnight charge → next-day gevoelscore). Positive = net charge during sleep; negative = drain. **Coverage start verified 2026-06-14 in Session C / D** — root cause is Garmin's two-stage UDS rollout on this FR245, not pipeline lateness: `SLEEPSTART` first emitted 2024-07-08, `SLEEPEND` first emitted 2024-09-18 (same watch, same firmware family across both boundaries). Any pre-vs-post analysis on a pre-2024-09-18 boundary returns NaN here. For analyses that can tolerate a documented proxy (r=0.989 vs truth), use `bb_overnight_gain_proxy` or `bb_overnight_gain_best`. Worked example: [`methodology/intervention_effects_descriptive.md` §2b](methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain). |
| `bb_overnight_gain_proxy` | derived | computed in `pipeline/01_extract/garmin_uds_extras.py` | `bb_highest - bb_sleep_start_value` | int | BB units | **first non-null 2024-07-08** → today (667 / 1755 = 38.0%) | NaN when either `bb_highest` or `bb_sleep_start_value` missing; structurally absent pre-2024-07-08 (same root cause as `bb_overnight_gain`: `SLEEPSTART` only emitted from that date). Saturation flag: when `bb_highest == 100` the proxy floors and may underestimate truth on high-recovery nights (~29 / 593 days in the post-2024-09-18 validation window). | **Documented proxy for `bb_overnight_gain`**, validated on n=593 post-2024-09-18 days where both truth and proxy exist: Pearson r = 0.989, mean residual = +0.63 BB units, median residual = 0, 550 / 564 clean days within ±5 BB units of truth, HIGHEST median timestamp 06:00 local (within ±2 h of SLEEPEND on 543 / 564 clean days). Net analytical gain over `bb_overnight_gain`: 74 days (= 71 bridge days in 2024-07-08 → 2024-09-17 between the two rollouts + 3 post-rollout nights where Garmin emitted `SLEEPSTART` but not `SLEEPEND`: 2025-04-26, 2025-08-24, 2025-12-11). No pre-2024-07-08 boundary recovers data via this proxy. Full validation + caveats in [`methodology/bb_overnight_gain_proxy.md`](methodology/bb_overnight_gain_proxy.md). |
| `bb_overnight_gain_best` | derived | computed in `pipeline/01_extract/garmin_uds_extras.py` | truth where present, else proxy | int | BB units | **first non-null 2024-07-08** → today (667 / 1755 = 38.0%) | NaN only when both `bb_overnight_gain` AND `bb_overnight_gain_proxy` are NaN | **Fused channel** for analyses that want maximum coverage and tolerate proxy provenance for the 74 proxy-source days. Mandatory companion: `bb_overnight_gain_source` (audit which path produced each row). For analyses that need pure-truth provenance (e.g. cross-day Wiggers D2 confirmatory tests), use `bb_overnight_gain` instead. |
| `bb_overnight_gain_source` | derived | computed in `pipeline/01_extract/garmin_uds_extras.py` | `"truth"` / `"proxy"` / `""` | category | enum | matches `bb_overnight_gain_best` non-null coverage (593 `"truth"` + 74 `"proxy"` + 1088 `""` = 1755) | `""` when `bb_overnight_gain_best` is NaN | **Audit channel** — every consumer of `bb_overnight_gain_best` must gate on this for provenance. `"truth"` = `SLEEPEND - SLEEPSTART`; `"proxy"` = `HIGHEST - SLEEPSTART` (71 in the 2024-07-08 → 2024-09-17 bridge + 3 post-rollout SLEEPEND-failure nights: 2025-04-26, 2025-08-24, 2025-12-11). |

**Sub-day BB resolution is unavailable on this corpus**. Per-minute (or any sub-day) Body Battery values do not exist in the Garmin GDPR dump — neither in FIT files (`monitoring_b` carries per-minute stress + HR + respiration but no `body_battery` field; verified 2026-06-14 across 60 stratified-sampled files spanning 2021–2026), nor in UDS JSON (only daily summary stats + 24-h `chargedValue` / `drainedValue` rollups), nor in any `DI-Connect-*` subfolder. Garmin's BB time-series lives only in their internal store, not in the user-facing export. For sub-day arousal dynamics use per-minute `stress_level` (the BB algorithm's primary input) from `monitoring_b` instead; see [`methodology/hrv_proxy_via_stress.md`](methodology/hrv_proxy_via_stress.md) for the stress-as-surrogate framing.

### All-day stress (5 columns)

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `all_day_stress_avg` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `all_day_stress_avg` | int | Garmin stress 0-100 (TOTAL aggregator) | 2021-08-16 → today (~1732 / 1755 after the 2026-06-12 sentinel filter dropped 2 negative values) | NaN on gap **OR** sentinel-filtered (see §7B policy note). Affected dates: 2021-08-16 (-2), 2022-10-28 (-1). | 24-hour mean stress level. Wiggers C2 (high daily stress → worse next-day recharge), C3 (non-linear stress→fatigue relationship). |
| `all_day_stress_max` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `all_day_stress_max` | int | same | same | NaN on gap. *Not sentinel-filtered* — `0` values on the two whole-day-void dates (2021-08-16, 2022-10-28) are left raw because the day is already flagged by the avg-channel sentinel. | 24-hour peak stress. **Layer 3**: Spearman with `awake_stress_max` = +1.00 on LC frame (n=1502); rho=1.000 needs definitional-vs-empirical verification. Treat as one signal in regression / VAR / CCF (pick `all_day_stress_max` for broader frame). See memory `feedback_definitional_pair_guardrail`. |
| `awake_stress_avg` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `awake_stress_avg` | int | same (AWAKE aggregator) | same (~1732 / 1755 after the same sentinel filter) | same dropped dates as `all_day_stress_avg` | Waking-period mean stress; separates daytime sympathetic state from sleep-window stress. |
| `awake_stress_max` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `awake_stress_max` | int | same | same | NaN on gap. Same not-filtered rationale as `all_day_stress_max`. | Waking-period peak stress. |
| `asleep_stress_avg_uds` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `asleep_stress_avg_uds` | int | same (ASLEEP aggregator) | 2021-08-16 → today (~1722 / 1755 after the 2026-06-12 sentinel filter dropped 12 negative values) | NaN on gap **OR** sentinel-filtered. 12 affected dates total: 2 whole-day Pattern A + 10 days where Garmin's UDS asleep_stress channel failed (8 have `sleep_valid_flag=False`, 2 (2025-11-19, 2025-11-24) have valid FIT sleep — these are Garmin internal-channel discrepancies; use `stress_mean_sleep` for those nights). | UDS-aggregated sleep-window mean stress. **Different source from `stress_mean_sleep`** (which is recomputed from raw FIT stress samples by `extract_sleep_stress.py`). Cross-check: they should agree closely; documented divergence usually means sleep-window boundary differences between UDS and FIT extraction. |

### 24h / waking respiration (3 columns)

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `respiration_avg_waking` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `respiration_avg_waking` | float64 | breaths/min | 2021-08-16 → today (1732 / 1755 = 98.7%) | NaN on gap | Waking-period mean respiration rate. Wiggers G1 waking variant. |
| `respiration_max_24h` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `respiration_max_24h` | float64 | breaths/min | same | NaN on gap | 24-hour peak respiration. |
| `respiration_min_24h` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `respiration_min_24h` | float64 | breaths/min | same | NaN on gap | 24-hour minimum respiration. |

### 24h SpO2 (2 columns)

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `spo2_avg_24h` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `spo2_avg_24h` | float64 | percent | 2021-08-16 → today (1688 / 1755 = 96.2%) | NaN on gap; lower fill where Pulse Ox toggle was off | 24-hour mean SpO2. Wiggers G4 (deprioritised). |
| `spo2_min_24h` | daily_computed | `processed/garmin/uds_extras_daily.csv` | `spo2_min_24h` | int | percent | same | NaN on gap | 24-hour minimum SpO2. |

---

## Section 8 — Garmin stress spikes (daytime)

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `max_spike_minutes` | daily_computed | `processed/garmin/daily_max_spike.csv` | `max_spike_minutes` | float64 (nullable int) | minutes of longest stress spike > 75 | 2021-08-16 → today (1.737 days) | NaN on gap | from H02b extraction |

---

## Section 8B — Intraday HR + stress (operationalises Wiggers A4 + C4)

Wave 4 add 2026-06-12. All columns propagated from
`processed/garmin/intraday_hr_stress_daily.csv` (extracted by
[`pipeline/01_extract/garmin_intraday_hr_stress.py`](pipeline/01_extract/garmin_intraday_hr_stress.py)
from `monitoring_b` FIT files using `Monitoring16Resolver` for the
`timestamp_16` rollover, per
[`analyses/garmin_exploration/scripts/fit_utils.py`](analyses/garmin_exploration/scripts/fit_utils.py)).

**Window**: waking minutes only — samples falling inside a sleep
window (per `sleepData.json`) are excluded. Sleep dynamics are covered
separately by `stress_mean_sleep` (§7) and sleep-stage / sleep
respiration / sleep SpO2 columns.

**These columns are not auxiliary indicators; they are the operational
form of Wiggers A4 and C4.** A4 directly: "sustained multi-hour HR
elevation, not a brief spike, marks real overexertion" → tested as
"is `hr_sustained_elevated_flag=True` more common on PEM-onset days
than on calm days?". C4 directly: "after overexertion, stress fails
to drop during rest" → tested as "does `stress_post_peak_time_to_rest_min`
elongate after high-exertion days?".

### A4 — HR sustained elevation (6 columns; v3 locked 2026-06-12)

**Baseline philosophy (v3, locked 2026-06-12 after reviewer critique
on v1 + v2):** Wiggers A4 references "sustained elevation above where
you'd normally be during the day". The reference is therefore the
user's own **typical daytime HR**, not their sleep-derived resting HR.

- `hr_median_waking[d]` = median HR across all waking-window samples
  on day d (the honest "where my HR actually sat today" descriptor;
  fills the missing middle bucket between sleep-derived `resting_hr`
  and noisy peak `max_hr`).
- `hr_daytime_baseline_lagged[d]` = median of `hr_median_waking`
  over the window `[d − 90, d − 30]` — same shape as the v3.2 lagged
  exertion baseline (memory `feedback_use_lagged_exertion_for_pem`).
  The lag-30 buffer ensures the recent push window does not
  contaminate its own reference.
- Threshold for "elevated" = `hr_daytime_baseline_lagged + 20 bpm`
  (offset chosen to clear the natural intra-day spread already
  embedded in the baseline; v2's `+15` was too lenient given the
  baseline now references daytime activity rather than sleep).
- "Sustained" = longest consecutive-minute run ≥ 30 min above threshold.

**Evolution (recorded so the column-name history is reproducible):**
- v1 (commit `98f416b`, REPLACED in same-day commit): threshold =
  `resting_hr + 15`. Cleared by any sedentary-but-awake activity;
  `hr_sustained_elevated_flag=True` on the median day. Flag separated
  nothing.
- v2 (uncommitted, transitional): switched to a 28-day-trailing
  daytime baseline + `+15`. Direction correct; window inconsistent
  with v3.2 lagged convention, offset still on the lenient side.
- v3 (this entry, locked): `[d-90, d-30]` window + `+20` offset.
  At landing: `hr_sustained_elevated_flag=True` on 3.6% of valid
  days (61 / 1694) — credible "real sustained overexertion" rate
  for an ME/CFS context. Baseline is highly stable (median 76,
  p25 74, p75 78).

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `hr_median_waking` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_median_waking` | float64 | bpm | 2021-08-16 → today (1730 / 1755 = 98.6%) | NaN if fewer than 120 waking HR samples that day | Per-day median across all waking-window samples. **Honest descriptor** of where the user's daytime HR sat — not threshold-dependent. Surfacing it lets analyses use it directly as a covariate (e.g. compare gevoelscore vs `hr_median_waking` deviation from `hr_daytime_baseline_lagged`) without having to re-extract from FIT. |
| `hr_daytime_baseline_lagged` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_daytime_baseline_lagged` | float64 | bpm | 2021-08-16 → today (1694 / 1755 = 96.5%) | NaN until ≥ 14 valid `hr_median_waking` days accumulate in the `[d-90, d-30]` window — coverage effectively starts ~2021-11-15 | The personal daytime baseline. Median of `hr_median_waking` over a 60-day window ending 30 days before d. **Same shape as v3.2 lagged exertion baseline** for methodological consistency. |
| `hr_min_above_daytime_baseline_plus_20_waking` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_min_above_daytime_baseline_plus_20_waking` | int | count of distinct waking minutes where HR > `hr_daytime_baseline_lagged` + 20 bpm | same as `hr_daytime_baseline_lagged` (1694 / 1755) | NaN on gap | Per-minute bucketing keeps this robust to varying sample cadence. v3 median = 62 min (was 459 in v1 with the wrong reference). |
| `hr_longest_elevated_run_min_waking` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_longest_elevated_run_min_waking` | int | minutes | same | NaN on gap | Longest consecutive-minute run above threshold. **The primary A4 number** — Wiggers emphasises *sustained* over *count*. v3 median = 10 min. |
| `hr_sustained_elevated_flag` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_sustained_elevated_flag` | bool | True iff `hr_longest_elevated_run_min_waking >= 30` | same | NaN on gap | The categorical A4 surface for cross-tab / stratification. v3: True on 3.6% of valid days. The 30-min "sustained" cutoff is tunable; document if changed. |
| `hr_area_above_daytime_baseline_waking` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_area_above_daytime_baseline_waking` | float64 | bpm⋅min (integral of `HR − hr_daytime_baseline_lagged` over above-threshold minutes) | same | NaN on gap | Captures magnitude × duration jointly. Useful when comparing days where the run length is similar but peak elevation differs. v3 median = 1685 bpm·min. |

### A4 — LC-era-only variants (5 columns; added 2026-06-12)

Mirrors the v3.2 `_lcera` LC-era pattern (see §6 v3.2 LC-era-only
variants). The rolling baseline window draws ONLY from dates `>=
LC_ERA_START` (2022-04-04). Candidate days before LC_ERA_START
have all `_lcera` columns NaN.

**Default for PEM-pacing analyses** (Wiggers A4 framed against LC-era
capacity); use the non-`_lcera` columns above for cross-era trajectory
characterisation (e.g. watching the citalopram-period HR climb in
`hr_daytime_baseline_lagged`'s slow drift).

Effective coverage starts 2022-05-18 — the first date at which the
[d-90, d-30] window contains ≥ 14 in-LC-era days. For d > 2022-07-03
the all-era and `_lcera` baselines are identical (the window doesn't
reach into pre-LC days anyway); the variants only differ during the
~7-week early-LC transition.

`hr_median_waking` itself has no `_lcera` variant — it's a per-day
descriptor, not a derived metric anchored to a baseline window.

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `hr_daytime_baseline_lagged_lcera` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_daytime_baseline_lagged_lcera` | float64 | bpm | 2022-05-18 → today (1463 / 1755 = 83.4%) | NaN before 2022-05-18 (insufficient in-LC-era window history) | LC-era-restricted version of `hr_daytime_baseline_lagged`. |
| `hr_min_above_daytime_baseline_plus_20_waking_lcera` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_min_above_daytime_baseline_plus_20_waking_lcera` | int | minutes | same | NaN on gap | LC-era-restricted version of the all-era counterpart. **Layer 3**: Spearman with `hr_area_above_daytime_baseline_waking_lcera` = +1.00 on LC frame (n=1463); rho=1.000 needs definitional-vs-empirical verification (likely shares numerator with the area integral). Treat as one signal (pick `hr_area_above_daytime_baseline_waking_lcera` for continuous magnitude×duration). See memory `feedback_definitional_pair_guardrail`. |
| `hr_longest_elevated_run_min_waking_lcera` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_longest_elevated_run_min_waking_lcera` | int | minutes | same | NaN on gap | LC-era-restricted version. |
| `hr_sustained_elevated_flag_lcera` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_sustained_elevated_flag_lcera` | bool | True iff `hr_longest_elevated_run_min_waking_lcera >= 30` | same | NaN on gap | LC-era-restricted version. At landing: True on 3.1% of valid days (46 / 1463) — very close to the all-era rate (3.6%) because for most LC-era days the two baselines are identical. |
| `hr_area_above_daytime_baseline_waking_lcera` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `hr_area_above_daytime_baseline_waking_lcera` | float64 | bpm⋅min | same | NaN on gap | LC-era-restricted version. |

### C4 — Stress decay after daily peak (4 columns)

Reference: per-day stress peak (the maximum stress sample in the waking
window) and Garmin's "rest" zone cutoff of 25 (matches the watch's
colour coding).

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `stress_post_peak_drop_avg` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `stress_post_peak_drop_avg` | float64 | Garmin stress 0-100 | 2021-08-16 → today (1721 / 1755 = 98.1%) | NaN if no waking stress samples or no samples in the 60-min post-peak window | Mean stress in the 60 minutes after the daily peak. Lower = better recovery; high = "stuck sympathetic" pattern Wiggers C4 names. |
| `stress_post_peak_time_to_rest_min` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `stress_post_peak_time_to_rest_min` | int | minutes | 2021-08-16 → today (1522 / 1755 = 86.7%) | NaN if no waking stress samples; **NaN if stress never drops below the 25 "rest" threshold within the same calendar day** (interpret NaN as "did not return to rest" — that's the C4-positive case, not a missing measurement) | Minutes from the daily peak until stress drops below 25. **C4-primary number**. The NaN-on-failure semantics inverts the usual rule: high NaN-fraction on a date range is the C4 signature, not a coverage problem. |
| `stress_high_duration_min` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `stress_high_duration_min` | int | minutes | 2021-08-16 → today (1737 / 1755 = 99.0%) | NaN on day with no monitoring_b stress samples | Distinct waking minutes with stress > 75. **Re-uses the H02b daily-max-spike threshold** but extends it from "longest single spike" (§8 `max_spike_minutes`) to "total time in the high zone". |
| `stress_recovery_pct_within_2h` | daily_computed | `processed/garmin/intraday_hr_stress_daily.csv` | `stress_recovery_pct_within_2h` | float64 | percent (negative if stress rose) | 2021-08-16 → today (1526 / 1755 = 86.9%) | NaN if peak occurred too late in the day to have a sample in the [peak + 2h − 15min, peak + 2h + 15min] window | `(peak − stress_at_peak+2h) / peak × 100`. Direct rate-of-recovery metric. Pair with `time_to_rest_min` to distinguish slow-but-complete recovery from fast-then-stall. |

### Section 8C — stress-with-low-motion minute counts (C4b primitive; 11 columns)

**Section preamble**: 9 per-day integer counts of minutes where stress
is elevated AND motion is classified as "low" by Garmin's per-bin
intensity classification, plus 2 respiration-rate companion columns.
Source: [`pipeline/01_extract/stress_low_motion_extract.py`](pipeline/01_extract/stress_low_motion_extract.py)
which parses monitoring_b FIT files. Full methodology + four-input
reasoning in [`methodology/stress_low_motion_primitive.md`](methodology/stress_low_motion_primitive.md);
implementation notes including the §3.1 FIT-data investigation
(per-minute step counts are NOT in monitoring_b — the `intensity`
classification is used instead) live there. Day-validity gate:
≥ 600 in-range stress samples (matches HA11 / H02d).

Construct-validity check (2026-06-15 run): Spearman ρ vs HA11
`u_dip_count` = 0.556 (moderate; same family, information-additive,
not redundant). Spearman ρ between `n_minutes_resp_above_18` and
u_dip_count = 0.044 (orthogonal — respiration adds a genuinely
independent signal).

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `stress_low_motion_min_count_S50_Mstrict` | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | 2021-08-16 → today (1739 / 1755 = 99.1%; ≥ 600-sample gate: 1722 valid) | NaN on days without monitoring_b file; 0 (not NaN) on days below the 600-sample gate | Count of minutes with `stress ≥ 50` AND `intensity == 0` OR no-record. **Sensitivity arm** for the S60_Mlow primary. |
| `stress_low_motion_min_count_S50_Mlow` | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | same | same | Count with `stress ≥ 50` AND `intensity ≤ 1` OR no-record. Sensitivity arm. |
| `stress_low_motion_min_count_S50_Mbelow_mod` | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | same | same | Equivalent to `_Mlow` in v1 (placeholder for future refinement: a separate intensity-class boundary may make this `intensity ≤ 2`). Sensitivity arm. |
| `stress_low_motion_min_count_S60_Mstrict` | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | same | same | Sensitivity arm of the primary. |
| **`stress_low_motion_min_count_S60_Mlow`** | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | same | same | **PRIMARY C4b column.** Count with `stress ≥ 60` (Garmin's "elevated" band) AND `intensity ≤ 1` OR no-record. Distribution on valid days: median 56, mean 67.5, 90th pct 133, max 364. Loaded for the Wiggers C4b hypothesis test. |
| `stress_low_motion_min_count_S60_Mbelow_mod` | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | same | same | Equivalent to primary in v1; placeholder. |
| `stress_low_motion_min_count_S75_Mstrict` | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | same | same | Conservative arm (Garmin's "high" band). |
| `stress_low_motion_min_count_S75_Mlow` | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | same | same | Conservative arm. |
| `stress_low_motion_min_count_S75_Mbelow_mod` | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | same | same | Equivalent to S75_Mlow in v1; placeholder. |
| `n_minutes_resp_above_18` | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | 2021-08-16 → today (1739 / 1755 = 99.1%) | NaN on days without monitoring_b file | Per-day count of minutes where respiration rate > 18 / min (elevated above typical adult-rest range 12-18). Captures motion AND sympathetic arousal. **Orthogonal to u_dip count** (ρ = 0.044) — adds genuinely independent signal for downstream tests. |
| `n_minutes_resp_in_rest_band_10_18` | daily_computed | `processed/garmin/stress_low_motion_minutes.csv` | same | int | minutes | same | same | Per-day count of minutes where 10 ≤ respiration ≤ 18 (normal-rest band). Distribution: median 1217 of ~1440 minutes/day. Use as a "genuinely-restful minutes" baseline; ratio against waking-minute count distinguishes high-quality-rest days from low. |

**Dose-adjustment caveat for consumers** ([`methodology/stress_low_motion_primitive.md` §1.3](methodology/stress_low_motion_primitive.md)):
the raw `stress >= S` thresholds correspond to different underlying
autonomic states across the Citalopram-traject phases (per
[`citalopram_dose_response §5.6`](methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14):
all_day_stress_avg has β = +0.57/mg confirmed dose-response). Any
cross-phase test on these counts MUST apply [`citalopram_phase_stratification §5.B`](methodology/citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests)
dose-adjustment on the predictor side. The primitive itself is
dose-naive by design (reusable across multiple tests).

**v2 future-work** ([`methodology/stress_low_motion_primitive.md` §3.3a](methodology/stress_low_motion_primitive.md)):
sleep-window membership and recorded-activity-session membership are
known additional motion indicators queued for a v2 of this primitive;
not in v1 to avoid pipeline-ordering complications. Until then,
downstream tests should report sleep/awake-conditioned analyses
separately using existing `sleep_start_gmt` / `sleep_end_gmt` columns.

---

## Section 9 — note categorization rollup (presence-conditioned)

⚠️ **All columns in this section are `presence_conditioned_positive_evidence`.**
The gating flag **for this section** is `has_note=True` (the v24
categorisation rollup is derived from the day's note). Other
presence-conditioned sections use different gating flags — §2
(cog/phy/emo loads) gates on `has_intensity_triage=True` (i.e.
`intensity_source != ""`). Always check the section's preamble; do
not assume `has_note` applies universally. Once gated: value 0 on a
note-day is *low-specificity about absence* — see
[methodology/symptom_mention_asymmetry.md](methodology/symptom_mention_asymmetry.md).
`NaN` on a no-note day.

Source: `processed/notes/notes-categorized-v24.csv` (per-day rollup;
v24 = v2 + v2.2 patches + v2.3 patches + v2.4 patches).

| name | class | source column | dtype | range | notes |
|---|---|---|---|---|---|
| `n_clauses` | presence_conditioned | `n_clauses` | float64 (nullable int) | ≥ 0 | number of clauses in the day's note |
| `cat_belasting_cognitief` | presence_conditioned ⚠️ | `cat_belasting_cognitief` | float64 (nullable int) | count of clauses tagged | |
| `cat_belasting_emotioneel` | presence_conditioned ⚠️ | `cat_belasting_emotioneel` | float64 (nullable int) | same | |
| `cat_belasting_fysiek` | presence_conditioned ⚠️ | `cat_belasting_fysiek` | float64 (nullable int) | same | |
| `cat_belasting_gezin` | presence_conditioned ⚠️ | `cat_belasting_gezin` | float64 (nullable int) | same | |
| `cat_belasting_sociaal` | presence_conditioned ⚠️ | `cat_belasting_sociaal` | float64 (nullable int) | same | |
| `cat_medicatie` | presence_conditioned ⚠️ | `cat_medicatie` | float64 (nullable int) | same | |
| `cat_recovery_actie` | presence_conditioned ⚠️ | `cat_recovery_actie` | float64 (nullable int) | same | includes v2.4 patch 5a present-tense rest mentions |
| `cat_symptoom_cognitief` | presence_conditioned ⚠️ | `cat_symptoom_cognitief` | float64 (nullable int) | same | brainfog cluster |
| `cat_symptoom_emotioneel` | presence_conditioned ⚠️ | `cat_symptoom_emotioneel` | float64 (nullable int) | same | per v2 verification: almost always 0 for this user |
| `cat_symptoom_fysiek` | presence_conditioned ⚠️ | `cat_symptoom_fysiek` | float64 (nullable int) | same | broadest physical-symptom bucket; sub-tags in §10 below give finer detail |
| `cat_triggers_extern` | presence_conditioned ⚠️ | `cat_triggers_extern` | float64 (nullable int) | same | corona, griep, infectie |
| `cat_context_neutraal` | presence_conditioned ⚠️ | `cat_context_neutraal` | float64 (nullable int) | same | residual neutral context |
| `state_symptoom_cognitief` | presence_conditioned ⚠️ | `state_symptoom_cognitief` | category | `absent`, `mild`, `present`, `severe` | worst severity for the family that day; `absent` here is itself a presence-conditioned positive ("geen brainfog" was mentioned), distinct from no-mention |
| `state_symptoom_emotioneel` | presence_conditioned ⚠️ | `state_symptoom_emotioneel` | category | same | |
| `state_symptoom_fysiek` | presence_conditioned ⚠️ | `state_symptoom_fysiek` | category | same | |
| `day_dominant_polarity` | presence_conditioned ⚠️ | `day_dominant_polarity` | category | `positive`, `neutral`, `negative`, `mixed` | most common per-clause polarity in the day's note |
| `n_pos_clauses` | presence_conditioned ⚠️ | `n_pos_clauses` | float64 (nullable int) | ≥ 0 | clause-polarity counts |
| `n_neg_clauses` | presence_conditioned ⚠️ | `n_neg_clauses` | float64 (nullable int) | ≥ 0 | |
| `n_mixed_clauses` | presence_conditioned ⚠️ | `n_mixed_clauses` | float64 (nullable int) | ≥ 0 | |
| `n_neutral_clauses` | presence_conditioned ⚠️ | `n_neutral_clauses` | float64 (nullable int) | ≥ 0 | |
| `neutral_forward_looking_flag` | presence_conditioned ⚠️ | aggregated from `notes-categorized-v24-clauses.csv.neutral_forward_looking` | bool | True if any clause in the note was flagged forward-looking pacing-intention | v2.4 patch 5b — see [methodology/symptom_categorization_v24.md](methodology/symptom_categorization_v24.md) |

---

## Section 10 — note `symptoom_fysiek` sub-tags (presence-conditioned)

⚠️ All `presence_conditioned_positive_evidence`. Same gating rule
as §9 (gate on `has_note=True`); see §9 preamble for why this is
section-specific and not a dictionary-wide rule.

Source: aggregated from `processed/notes/notes-categorized-v24-clauses.csv`
to per-day counts via `pipeline/02_label/aggregate_v24_subtypes.py`.

| name | source pattern | range | notes |
|---|---|---|---|
| `cat_sub_hoofdpijn` | clauses with `symptoom_fysiek_subtype` containing `hoofdpijn` | ≥ 0 | head pain cluster (262 clauses corpus-wide) |
| `cat_sub_spier` | `symptoom_fysiek_subtype` contains `spier` | ≥ 0 | muscle / limb cluster (44 clauses corpus-wide) |
| `cat_sub_keel_resp` | contains `keel_respiratoir` | ≥ 0 | throat / respiratory (33 clauses) |
| `cat_sub_koorts` | contains `koorts` | ≥ 0 | fever (10 clauses) |
| `cat_sub_gastro` | contains `gastro` | ≥ 0 | gastrointestinal (8 clauses) |
| `cat_sub_huid` | contains `huid` | ≥ 0 | skin (2 clauses) |
| `cat_sub_neuro` | contains `neuro` | ≥ 0 | tingling, dizziness (3 clauses) |
| `cat_sub_systemisch_vermoeid` | contains `systemisch_vermoeid` | ≥ 0 | general fatigue (384 clauses); includes v2.3 countersignal absent-states |
| `cat_sub_slaap` | contains `slaap` | ≥ 0 | sleep-disturbance mentions (82 clauses) |
| `cat_sub_overig` | contains `overig` | ≥ 0 | catch-all (≈ 47 clauses after v2.3 cleanup) |

---

## Section 11 — timeline events on day

| name | class | source | source column | dtype | units / categories | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `n_events_on_day` | daily_computed | `raw/directus_exports/annotations.yaml` + `processed/manual_triage/triage_events.csv` | derived | float64 (nullable int) | count of span-or-marker entries covering the date | 2021-08-16 → today (events range varies) | 0 when no events | **Coverage caveat (added 2026-06-12)**: `0` is observed-no-event only when `has_calendar_coverage=True` (`date >= 2022-06-17`, the date the user began maintaining the external calendar that feeds `annotations.yaml`). Before that date, `0` may reflect incomplete logging rather than absence of events. Gate on `has_calendar_coverage=True` before interpreting absence. |
| `event_labels` | daily_computed | same | derived | object (string) | semicolon-separated event titles | matches | empty string when 0 events | **may contain personal references; external only** |
| `event_categories` | daily_computed | same | derived | object (string) | semicolon-separated from `{crash, dip, high_intensity, interventie, levensgebeurtenis, medical, trigger, marker}` | matches | empty when 0 events | |
| `in_umbrella` | derived | annotations.yaml | computed | bool | True if covered by a span whose label contains the word `umbrella` (e.g. "PwC reintegratie 2023 (umbrella)", "Citalopram-traject (umbrella, 2024-04 -> ongoing)") | full | False otherwise | matches the explicit user-curated marker per methodology §4. Earlier draft also flagged any `levensgebeurtenis > 14 days` as an umbrella; that arbitrary fallback was removed 2026-06-11. **Descriptive-only (not for analytical use)**: the three umbrella periods are semantically distinct (medication, work reintegration, relational tension) and barely overlap in time, so `in_umbrella` as a single binary is confounded by year (Layer 3 spot-investigation 2026-06-12). **For any correlation / stratification, use the three per-period booleans below.** |
| `umbrella_labels` | derived | same | computed | object (string) | semicolon-separated | matches | empty | |
| `in_citalopram_traject` | derived | annotations.yaml | computed | bool | True if `umbrella_labels` contains the substring `Citalopram-traject` (i.e. covered by "Citalopram-traject (umbrella, 2024-04 -> ongoing)") | full | False otherwise | LC frame: 788 / 1524 True days (51.7%). Spans 2024-04 → ongoing; fully nests `in_relational_spanning_2024`. **Per-period analytical surface added 2026-06-12.** |
| `in_pwc_reintegratie_2023` | derived | annotations.yaml | computed | bool | True if `umbrella_labels` contains the substring `PwC reintegratie 2023` (i.e. covered by "PwC reintegratie 2023 (umbrella)") | full | False otherwise | LC frame: 268 / 1524 True days (17.6%). Spans 2023 calendar year. Zero overlap with the other two umbrellas. |
| `in_relational_spanning_2024` | derived | annotations.yaml | computed | bool | True if `umbrella_labels` contains the substring `Relational-spanning 2024` (i.e. covered by "Relational-spanning 2024 (umbrella)") | full | False otherwise | LC frame: 172 / 1524 True days (11.3%). Spans 2024; **all 172 days are also `in_citalopram_traject=True`** (Relational-spanning sits entirely inside the Citalopram trajectory). When using both as covariates, expect collinearity. |
| `in_naproxen_interventie` | derived | annotations.yaml | computed | bool | True if `umbrella_labels` contains the substring `Naproxen-interventie` (i.e. covered by "Naproxen-interventie (umbrella, 2025-03 -> ongoing, ad-hoc gebruik bij hoofdpijn)") | full | False otherwise | LC frame: 436 / 1524 True days (28.6%). Span 2025-03-27 → ongoing (capped at current timeline end). **All 436 days are also `in_citalopram_traject=True`** (Naproxen umbrella sits entirely inside the Citalopram trajectory; expect collinearity when including both). Note: the umbrella marks the *period during which ad-hoc naproxen use occurs*; the actual ~20 use-days are encoded separately as `naproxen` event labels in `event_labels`. |

---

## Section 12 — PwC work record (2022-09-26 → 2024-02-26 only)

Source: `processed/pwc/reintegration_hours_2022-2024.csv` (derived from
`raw/pwc/reintegratie_willem.xlsx` via `pipeline/01_extract/pwc_reintegration_hours.py`).

| name | class | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|
| `pwc_primary_hours` | daily_computed | `primary_hours` | float64 | hours | 2022-09-26 → 2024-02-26 (240 working-day rows) | NaN outside this window | "primary" = reintegration-target hours |
| `pwc_secondary_hours` | daily_computed | `secondary_hours` | float64 | hours | same | NaN outside | meetings / travel / admin |
| `pwc_total_hours` | daily_computed | `total_hours` | float64 | hours | same | NaN outside | |
| `pwc_illness_flag` | daily_computed | `illness_flag` | bool | True for ziek/niet lekker/corona days in the toelichting | same | NaN outside | regex over `toelichting`; see Q1 muscle-pain absence note in `symptom_mention_asymmetry.md` |
| `pwc_doctor_visit_flag` | daily_computed | `doctor_visit_flag` | bool | bedrijfsarts/casemanager/huisarts visit in toelichting | same | NaN outside | |
| `pwc_amsterdam_flag` | daily_computed | `amsterdam_flag` | bool | "naar amsterdam" / "naar kantoor" | same | NaN outside | reintegration office days |
| `pwc_vacation_flag` | daily_computed | `vacation_flag` | bool | "vakantie" / "vrij" / kerstvakantie etc. | same | NaN outside | |
| `pwc_toelichting` | daily_computed | `toelichting` | object (string) | free text | same | empty outside | **personal data — external only** |

---

## Section 13 — PwC dossier events

Source: `processed/pwc/pwc_dossier_2022-2024.csv` flowed through
`processed/manual_triage/triage_events.csv` via the dossier dispatcher.
Represented in the master as event flags rather than triage_events
rows directly (those are already joined in Section 11).

| name | class | source | dtype | coverage | missingness | notes |
|---|---|---|---|---|---|---|
| `dossier_event_today` | derived | from triage_events.csv where `source=pwc_dossier_2022-2024` | bool | full | False otherwise | True if any dossier-sourced event on the date. **Coverage caveat (added 2026-06-12)**: `False` is observed-no-event only when `has_pwc_dossier_window=True` (2022-03-28 → 2024-04-17, the wachttijd-loondoorbetaling 104w span during which the dossier was maintained). Outside that window, `False` means the dossier wasn't tracked, not that no event happened. Gate on `has_pwc_dossier_window=True` before interpreting absence. |
| `dossier_event_labels` | derived | same | object (string) | full | empty otherwise | semicolon list. **Coverage caveat**: same as `dossier_event_today` — empty string is observed-no-event only when `has_pwc_dossier_window=True`; outside that window, empty means the dossier wasn't tracked. |
| `dossier_event_categories` | derived | same | object (string) | full | empty | subset of `{medical, levensgebeurtenis, marker}` per the dossier review. **Coverage caveat**: same as `dossier_event_today` — empty string is observed-no-event only when `has_pwc_dossier_window=True`; outside that window, empty means the dossier wasn't tracked. |

---

## Section 14 — coverage flags

All `derived`. These exist every day in the master's full range.

| name | dtype | meaning |
|---|---|---|
| `has_score` | bool | True if `gevoelscore` is non-null |
| `has_note` | bool | True if `note_text` is non-empty (mandatory companion to §9 + §10) |
| `has_garmin_uds` | bool | True if any column from `daily_uds.csv` is non-null |
| `has_garmin_sleep` | bool | True if `sleep_valid_flag=True` |
| `has_pwc_log` | bool | True for 2022-09-26 → 2024-02-26 (the PwC log window) |
| `has_pwc_dossier_window` | bool | True for 2022-03-28 → 2024-04-17 (wachttijd 104w span); the period during which dossier events may exist |
| `has_intensity_triage` | bool | True if `intensity_source` is non-empty (includes `bulk_triage_YYYY_no_info`). **Mandatory gating flag** for §2 cog/phy/emo loads, analogous to `has_note` for §9/§10 |
| `has_calendar_coverage` | bool | True for `date >= 2022-06-17` (the date the user began maintaining the external calendar that feeds `annotations.yaml`). **Mandatory gating flag** for §11 `n_events_on_day` and `event_labels` when interpreting absence: `n_events_on_day=0` outside this window may reflect incomplete calendar logging rather than no events. (Added 2026-06-12 per Layer 2 gating-flag audit.) |

---

## Coverage matrix (cross-source)

Use this table to know which signals exist when querying any specific
date range:

| date range | gevoelscore | notes (asymm.) | Garmin UDS | sleep-stress | PwC log | PwC dossier window | intensity reviewed |
|---|---|---|---|---|---|---|---|
| 2021-08-16 → 2022-09-02 | – | – | ✓ | ✓ | – | partial | partial |
| 2022-09-03 → 2022-09-25 | ✓ | – | ✓ | ✓ | – | ✓ | ✓ |
| 2022-09-26 → 2024-02-26 | ✓ | partial | ✓ | ✓ | ✓ | ✓ | ✓ (2022-2024 done) |
| 2024-02-27 → 2024-07-18 | ✓ | partial | ✓ | ✓ | – | partial | ✓ |
| 2024-07-19 → today | ✓ | varies | ✓ | ✓ | – | – | ✓ |

Header semantics: **PwC dossier window** mirrors `has_pwc_dossier_window` (the wachttijd 104w span 2022-03-28 → 2024-04-17), not the count of dossier events on a given date. **intensity reviewed** mirrors `has_intensity_triage` (non-empty `intensity_source`), which includes the `bulk_triage_YYYY_no_info` three-state explicit-absence value — i.e. days the user reviewed and explicitly marked as carrying no load signal. Both are gating flags for downstream presence-conditioned semantics; neither is a "did data exist" cell.

---

## Cross-references

- [methodology/methodology.md](methodology/methodology.md) — research
  methodology (load scale, triage rules, validation lenses).
- [methodology/symptom_mention_asymmetry.md](methodology/symptom_mention_asymmetry.md)
  — the binding rule for §9 + §10 + presence-conditioned semantics.
- [methodology/nightly_attribution.md](methodology/nightly_attribution.md)
  — the binding rule for §5 + §7 nightly attribution.
- [methodology/garmin_indicators_audit.md](methodology/garmin_indicators_audit.md)
  — per-column provenance map for §4-§8 Garmin-derived columns; known
  issues catalogue (push_burden contamination); inventory of
  available-but-unused signals for future expansion.
- [methodology/crash_v2_definition.md](methodology/crash_v2_definition.md)
  — derivation of §3 crash labels (to be moved from
  `garmin/hypotheses/crash_v2-definition/`).
- [methodology/symptom_categorization_v24.md](methodology/symptom_categorization_v24.md)
  — derivation of §9 + §10 categorisation columns.
- [pipeline/03_consolidate/build_unified_dataset.py](pipeline/03_consolidate/build_unified_dataset.py)
  — the script that produces `per_day_master.csv`. Phase B.

---

## Update log

| date | who | change |
|---|---|---|
| 2026-06-11 | initial spec | created during Plan-mode phase A; not yet validated against a built dataset |
| 2026-06-11 | Phase B audit | removed `push_burden_7d` column. The Garmin indicators audit ([methodology/garmin_indicators_audit.md](methodology/garmin_indicators_audit.md)) confirmed the known rolling-baseline-contamination issue. A v3.2 lagged variant (`push_burden_7d_lagged`) exists upstream but is also held back from the master: per the established schema discipline of held-back indicators, we don't surface a known-broken metric even with a caveat, nor pre-commit to its replacement before descriptive analysis motivates the choice. When the need surfaces, the lagged variant can be added cleanly. |
| 2026-06-11 | Phase B refinement | removed a derived bool column with arbitrary 2024-2025 boundaries sourced from a qualitative trajectory framing. The boundaries were neither pre-registered nor data-driven. Any classification of that kind belongs in descriptive-analysis output rather than the schema. If a data-driven indicator emerges later, it joins the dictionary then. |
| 2026-06-11 | Phase B build verified | first build (1755 rows × 87 cols) ran clean on 5-date spot-check; 81 forward-dated rows pruned from `per_day_intensity.csv` source. Date range capped at last_score_date (`max(day_entries.date)`) for reproducibility. |
| 2026-06-12 | Layer 0 audit | renamed CSV column `cat_sub_keel_respiratoir` → `cat_sub_keel_resp` to match the dictionary spec on line 205 (build script now uses a `V24_SUB_CSV_NAME` override to decouple source-key from emitted column name). Reworded coverage-matrix headers to mirror flag semantics ("PwC dossier" → "dossier window", "intensity triage" → "intensity reviewed"); aligned 5 cells with the actual partial-overlap data, including window-2 notes (the user did not write notes during the first 23 days of gevoelscore use). |
| 2026-06-12 | Layer 1 fixes — absent-state | fixed two compounding bugs in `pipeline/03_consolidate/build_unified_dataset.py` so the 104 upstream `symptoom_*=absent` clauses (102 fysiek, 2 cognitief) now surface in the master. Bug A: aggregation used `state_max` defaulting to 0, so absent (sev=0) clauses never updated state; added a separate `state_absent_seen` set. Bug B: emit gated on `sev > 0`, so even fixed aggregation couldn't surface absent; rewrote as three-state (severity → "absent" → ""). Worst-severity wins over absent (matches §9 line 181 semantic). Result: `state_symptoom_fysiek=absent` now appears on 32 days (4.7% of note-days), `state_symptoom_cognitief=absent` on 2 days (0.3%). |
| 2026-06-12 | Layer 1 fixes — dictionary corrections | (1) `crash_episode_id` (§3) clarified: tags both crash-episode days AND single-day dips (108 distinct IDs = 29 crash streaks + 79 dips). (2) `exertion_class` (§6): added `none` as 6th category (≈26.5% of `has_garmin_uds=True` days; distinct from NaN out-of-coverage); flagged that `very_light` does not appear in the current dataset. (3) `effective_exertion_min` and `step_z_30d` (§6): documented ≈22-23% additional NaN within `has_garmin_uds=True` due to 30-day rolling-baseline warmup + post-Garmin-gap recovery. |
| 2026-06-12 | v3.2 lagged exertion added | added 8 v3.2 lagged-baseline exertion columns to the master (1755 rows × 87 → 95 cols): `exertion_class_lagged`, `exertion_rank_composite_lagged` (newly derived in build script), `eff_exertion_rank_lagged`, `step_rank_lagged`, `max_hr_rank_lagged`, `vigorous_min_rank_lagged`, `push_burden_7d_lagged`, `effective_exertion_slope_28d`. Default surface for new analyses (Wiggers hypothesis testing in particular). v3.1 columns (`exertion_class`, `step_z_30d`) retained for HA01b/HA02c reproducibility and now carry explicit "use lagged for new work" notes. Section 6 restructured into v3.1 / v3.2 sub-sections. Methodology cross-references added in [`methodology/garmin_indicators_audit.md`](methodology/garmin_indicators_audit.md), [`methodology/methodology.md`](methodology/methodology.md) §3c, [`wiggers_testable_hypotheses.md`](wiggers_testable_hypotheses.md) Column-choice matrix, and the spec doc. |
| 2026-06-12 | Layer 2 audit — descriptive findings persisted as guardrails | (1) §2 `intensity_source` notes appended with rate-computation caveat: per-quarter `% cog/phy/emo_load notna` rates are non-comparable across quarters when the `_no_info` share differs; honest cross-quarter comparison requires splitting `has_intensity_triage=True` into `_no_info` and context-sufficient subsets. Observed example: 2025Q3 = 74.2% cog-rate vs 2024Q1 = 26.7% cog-rate while absolute cog-assigned counts are 23 vs 24. (2) [`methodology/garmin_indicators_audit.md`](methodology/garmin_indicators_audit.md): documented 2022Q3 coverage gap on v3.1 `step_z_30d` (9.6%) and `effective_exertion_min` (33.7%) within `has_garmin_uds=True` days — separate from the 30-day warmup; likely an upstream `activity_features_daily.csv` extraction discontinuity. (3) [`methodology/nightly_attribution.md`](methodology/nightly_attribution.md): documented Layer 2 derivation check for `sleep_start_afternoon_flag` (Definition A = 144 rows / 8.44%; Definition B at p95 = 1 row / degenerate). |
| 2026-06-12 | Layer 2 schema — `sleep_start_afternoon_flag` added | added derived bool column `sleep_start_afternoon_flag` (§7) to the master. Derivation: True iff `sleep_valid_flag=True` AND `sleep_start_gmt` converted to Europe/Amsterdam (DST-correct via stdlib `zoneinfo.ZoneInfo`) has `hour < 17`. Build script now imports `ZoneInfo` and emits the column in the sleep block. 144 / 1707 valid-sleep nights = 8.44% True at landing. See [`methodology/nightly_attribution.md`](methodology/nightly_attribution.md) §"Afternoon `sleep_start_gmt` values" for co-occurrence with crash labels and top umbrella event_labels. |
| 2026-06-12 | Gating-flag scope correction | the class definition (line 26-30), `has_note` row (§1), §9 preamble, and §10 preamble all previously implied `has_note=True` is the universal gating flag for `presence_conditioned_positive_evidence` columns. Reworded all four spots to make explicit that the gating flag is section-specific: §9 + §10 (v24 categorisation rollup) gate on `has_note`; §2 (cog/phy/emo + intensity_notes load columns) gates on `has_intensity_triage` (= `intensity_source != ""`). Each section's preamble names its own gating flag; readers must not assume `has_note` applies universally. |
| 2026-06-12 | `has_calendar_coverage` added + dossier coverage caveats | added derived bool `has_calendar_coverage` to §14 (True for `date >= 2022-06-17`, the date the user began maintaining the external calendar that feeds `annotations.yaml`). Added coverage caveat to §11 `n_events_on_day` notes: `0` is observed-no-event only inside this window; before that date, `0` may reflect incomplete logging. Added matching coverage caveats to §13 `dossier_event_today` / `_labels` / `_categories` referencing the existing `has_pwc_dossier_window` flag: `False` / empty is observed-no-event only inside the wachttijd window (2022-03-28 → 2024-04-17); outside, the dossier wasn't tracked. Both clarifications follow the same gating-flag discipline already used by §2 and §9/§10. |
| 2026-06-12 | Wave 1 — sleep-derivation columns | added 3 derived columns to §7 from existing `sleep_start_gmt` / `sleep_end_gmt`: `bedtime_hour_local` (DST-correct fractional local hour, Wiggers F4 input), `sleep_duration_min` (Wiggers F1), `bedtime_std_7d` (rolling 7-day std of bedtime, Wiggers F4 — after-midnight wrap handled by `+24` adjustment for values < 12 before std; afternoon-flagged nights excluded). No new extraction, pure derive. Master 97 → 100 cols. Plan: [`.claude/plans/garmin-enrichment-waves.md`](../../.claude/plans/garmin-enrichment-waves.md) Wave 1. |
| 2026-06-12 | Wave 2 — propagate existing-but-unused upstream columns | added 14 columns to §4 and §6 from existing source CSVs (no new extraction). §4 gained 5: `highly_active_sec`, `active_sec`, `is_vigorous_day`, `daily_step_goal`, and derived `steps_above_goal_flag` (`total_steps >= daily_step_goal`). §6 gained 9: 4 v3.1 per-axis classes (`class_axis_A_eff`, `_B_step`, `_C_maxhr`, `_D_vig`), 4 v3.2 lagged per-axis classes (same names + `_lagged`), and `above_baseline_streak`. Supports Wiggers E1 (personal-anchored step threshold), E3 (per-axis comparison + attribution), and E2 (streak as direct creeping-floor count). Master 100 → 114 cols. Plan: [`.claude/plans/garmin-enrichment-waves.md`](../../.claude/plans/garmin-enrichment-waves.md) Wave 2. |
| 2026-06-12 | Activity-features re-extract from 2021-08-16 | extended `ANALYSIS_START` in [`analyses/garmin_exploration/activity-labels/scripts/03_compute_daily_features.py`](analyses/garmin_exploration/activity-labels/scripts/03_compute_daily_features.py) from `date(2022, 9, 3)` to `date(2021, 8, 16)` (Garmin coverage start). Re-ran scripts 03 → 04 → 11, replaced `processed/garmin/activity_features_daily.csv`, rebuilt `per_day_master.csv`. **Result**: 2022Q3 v3.1 + v3.2 coverage gap (previously 9.6% / 33.7% / 0% fill) now 100%; pre-LC healthy baseline (2021-08-16 → 2022-05-06 dx) now accessible — 264 days of `has_garmin_uds=True` with mean `exertion_rank_composite_lagged` = 0.577 (vs train-era 0.698). **Trade-off**: v3.1 rolling-baseline ranks for **2022-09-23 → 2022-10-22** (30 days) shifted because the baseline window `[d-30, d-1]` now reaches into pre-LC training-period data; strict bit-identical HA01b/HA02c reproducibility breaks for those 30 days. Qualitative results expected stable but not verified. Locked policy going forward: every new Garmin extraction starts at 2021-08-16 (per memory `feedback_garmin_reextract_from_2021_08_16`). |
| 2026-06-12 | LC research-era boundary + LC-era-only lagged variants | **(1) `lc_phase` column added to §0 identity** (derived category: `pre_corona` < 2022-03-21, `corona_infection` 2022-03-21 → 2022-04-03, `lc` >= 2022-04-04). The 2022-04-04 boundary is the **research-wide LC start of record** (locked by user 2026-06-12): the Monday after the Fietsweekend Ardennen (2022-04-01 → 2022-04-03), which the user identifies as the trigger / end-of-acute-corona event. Pre-corona boundary 2022-03-21 = first day of the corona-ziek-week (per Training-periode span note). Existing `era` column kept for HA01b/HA02c backward compat but explicitly relabelled as gevoelscore-corpus-driven, not LC-onset-driven. **(2) 11 LC-era-only v3.2 lagged columns added to §6**: `exertion_class_lagged_lcera`, `exertion_rank_composite_lagged_lcera`, 4 axis ranks `_lcera`, 4 per-axis classes `_lcera`, `push_burden_7d_lagged_lcera`. Baseline window restricted to dates >= `LC_ERA_START = 2022-04-04`. For PEM-pacing analyses (Wiggers H1, H3, H5, B4, D5) use the `_lcera` variants; for cross-era trajectory characterisation use the all-era `_lagged` variants. ~82.6% fill within `has_garmin_uds=True` (LC-era window effectively starts 2022-07-03 after the 90-day warmup). **(3) `effective_exertion_slope_28d` not duplicated** — its 28-day window slides fully into LC era within ~4 weeks, so a separate variant would not differ except at the boundary. **(4)** Added 2022-04-04 marker to `hand_curated_spans.yaml` (category `marker`, label "LC-era analysis boundary (Monday after Fietsweekend Ardennen)"); re-ran `merge_calendar_triage.py` to propagate to `annotations.yaml`. Master 114 → 126 cols. |
| 2026-06-12 | Wave 3 — Garmin physiological extras (JSON-side propagation) | added **27 new columns** to the master from two new JSON-source extractors (no FIT parsing). **(1) `pipeline/01_extract/garmin_uds_extras.py`** writes `processed/garmin/uds_extras_daily.csv` with 18 columns from UDSFile_*.json: 8 Body Battery (charged/drained 24h + highest/lowest + sleep-start/sleep-end/during-sleep values + derived overnight gain) for Wiggers D1-D5; 5 all-day stress (TOTAL/AWAKE/ASLEEP aggregator avg+max) for Wiggers C1-C3; 3 respiration 24h/waking and 2 SpO2 24h for Wiggers G1, G4. **(2) `pipeline/01_extract/garmin_sleep_extras.py`** writes `processed/garmin/sleep_extras_daily.csv` with 9 columns from sleepData.json: 4 sleep-stage minutes (deep/light/awake/unmeasurable) for Wiggers F2; 3 sleep-window respiration for Wiggers G1 (sleep variant); 2 sleep-window SpO2 for Wiggers G4. Both extractors propagated into `build_unified_dataset.py` and surfaced in §7 (sleep extras) and new §7B (physiological extras). **HRV explicitly not added — hardware-blocked on Forerunner 245** (Elevate V3 sensor does not produce nightly HRV Status; FIT sleep type-49 files store the relevant data in undocumented `unknown_273/274/276` messages with no community decode available). Wiggers B1-B5 and HRV-dependent H1-H5 remain blocked on this device. Master 126 → 153 cols. Plan: [`.claude/plans/garmin-enrichment-waves.md`](../../.claude/plans/garmin-enrichment-waves.md) Wave 3 (Option A pivot: JSON-side propagation in place of FIT-based extraction). |
| 2026-06-12 | Wave 3 — sentinel filter for Garmin UDS extras | applied negative-value sentinel filter at build time to 4 columns in §7B: `all_day_stress_avg`, `awake_stress_avg`, `asleep_stress_avg_uds`, `bb_during_sleep_value`. Garmin emits `-1`/`-2` (stress) and `-4`/`-5` (BB) as a "no data" sentinel on a handful of dates — physically impossible on the underlying 0-100 scales, so they cannot be real measurements. `drop_neg_sentinel()` helper added to `build_unified_dataset.py`; sentinel-policy preamble added at top of §7B explaining the three sentinel classes (clear negatives, ambiguous zeros, legitimate zeros) and the policy rationale. Total cells affected: 2 (`all_day_stress_avg`), 2 (`awake_stress_avg`), 12 (`asleep_stress_avg_uds`), 2 (`bb_during_sleep_value`) = 18 cells across ~15 unique dates. Two of the asleep_stress dates (2025-11-19, 2025-11-24) have `sleep_valid_flag=True` — these are Garmin-internal channel discrepancies; for those nights analysts should use `stress_mean_sleep` (FIT-derived). |
| 2026-06-12 | Wave 4 — intraday HR + stress (operationalises Wiggers A4 + C4) | added **8 new columns** to the master from new FIT-source extractor `pipeline/01_extract/garmin_intraday_hr_stress.py` walking `monitoring_b` files. Uses the shared `Monitoring16Resolver` (from `fit_utils.py`) to expand `timestamp_16` for HR samples (per-minute monitoring frames carry the rolling 16-bit timestamp, not full datetime). Waking-window only — sleep-window samples excluded. **A4 and C4 are not auxiliary signals; these columns are the operational form of those Wiggers hypotheses** — A4 = "sustained multi-hour HR elevation marks real overexertion" → testable as `hr_sustained_elevated_flag` cross-tab; C4 = "stress fails to drop after overexertion" → testable as `stress_post_peak_time_to_rest_min` elongation. **NaN semantics for `stress_post_peak_time_to_rest_min` inverts the usual rule**: NaN = "stress never returned to rest that day" = the C4-positive case, not a coverage problem. **v1 (this entry's first form) used `resting_hr + 15` as the A4 baseline — superseded same day by v3 entry below; do not reference v1 column names.** Master 153 → 161 cols at v1. Plan: [`.claude/plans/garmin-fit-extraction-feasibility.md`](../../.claude/plans/garmin-fit-extraction-feasibility.md). |
| 2026-06-12 | Wave 4 v3 — A4 baseline reworked (personal daytime baseline + lagged window) | reworked the 4 A4 columns same-day after reviewer critique. v1's `resting_hr + 15` threshold cleared on the median day (459 min above-baseline, 31-min longest run, `hr_sustained_elevated_flag=True` on the median day — the flag separated nothing). v3 fixes both reference and offset: baseline is now `hr_daytime_baseline_lagged` = median of per-day `hr_median_waking` over `[d - 90, d - 30]` (same shape as v3.2 lagged exertion baseline); threshold = baseline + 20. **Two transparency columns added**: `hr_median_waking` (per-day median across waking samples — the honest "where my HR sat" descriptor, fills the missing middle between sleep `resting_hr` and noisy `max_hr`) and `hr_daytime_baseline_lagged` (the rolling reference itself). **Four metric columns renamed and re-computed**: `hr_min_above_baseline_plus_15_waking` → `hr_min_above_daytime_baseline_plus_20_waking`; `hr_area_above_baseline_waking` → `hr_area_above_daytime_baseline_waking`. `hr_longest_elevated_run_min_waking` and `hr_sustained_elevated_flag` keep their names but the threshold semantics change. Distribution at landing: median `hr_min_above_daytime_baseline_plus_20_waking` = 62 (was 459); median `hr_longest_elevated_run_min_waking` = 10 (was 31); `hr_sustained_elevated_flag=True` on 3.6% of valid days (61 / 1694) — credible "real sustained overexertion" rate. Baseline median 76 bpm (p25 74, p75 78) shows the rolling reference is stable. **Net column delta**: 4 v1 cols replaced by 6 v3 cols (2 transparency + 4 metric); master 161 → 163. C4 columns unchanged. Pre-registration draft in `wiggers_testable_hypotheses.md` updated with v3 column names. |
| 2026-06-12 | Wave 4 v3 — A4 LC-era-only `_lcera` variants added | 5 new `_lcera`-suffixed columns added to §8B, mirroring the v3.2 LC-era pattern (see §6 v3.2 LC-era-only variants). Rolling baseline window draws ONLY from dates `>= LC_ERA_START` (2022-04-04). Candidate days before LC_ERA_START have all `_lcera` columns NaN. Effective coverage starts 2022-05-18 (first date at which the [d-90, d-30] window contains ≥ 14 in-LC-era days); 83.4% fill across all-era. Note: for d > 2022-07-03 the all-era and `_lcera` baselines are identical (the window doesn't reach into pre-LC days anyway), so the variants only differ during the ~7-week early-LC transition. **Default for Wiggers PEM-pacing A4 analyses**; the all-era columns remain useful for cross-era trajectory characterisation. `hr_median_waking` is NOT given an `_lcera` variant (per-day descriptor, not anchored to a baseline window). Memory `feedback_use_lagged_exertion_for_pem` updated with the HR `_lcera` columns. `hr_sustained_elevated_flag_lcera=True` on 3.1% of valid days (46 / 1463), very close to the all-era 3.6% — expected, since most LC-era days draw from an identical window. Master 163 → 168 cols. |
| 2026-06-12 | Layer 3 bivariate — guardrails persisted | Layer 3 (bivariate / collinearity / pre-CCF) ran on the full 168-col master against the LC frame (`lc_phase=='lc'`, n=1524) and the LCscore frame (LC + `era in {train, validate}`, n=1372). **Two methodological guardrails landed**: (1) **Five near-identical pairs** (Spearman ≥ +0.97) — `max_hr` × `max_avg_hr_uds` (+0.97), `bb_highest` × `bb_sleep_end_value` (+0.99), and three exact-+1.000 pairs (`all_day_stress_max` × `awake_stress_max`, `bb_during_sleep_value` × `bb_overnight_gain`, `hr_min_above_daytime_baseline_plus_20_waking_lcera` × `hr_area_above_daytime_baseline_waking_lcera`). Each pair documented inline in §5 / §7B / §8B with a preferred column for downstream model inclusion. The three ρ=1.000 pairs need definitional-vs-empirical verification (do they share an identical computation path upstream?) before being declared definitional. Memory: `feedback_definitional_pair_guardrail`. (2) **Crash-day distortion** — dropping `is_crash==True` rows from the headline matrix shifted seven cross-family Spearman correlations by ≥ +0.15: `push_burden_7d_lagged_lcera` × `resting_hr` went from +0.091 (full) → +0.426 (crash-dropped, delta +0.335); analogous large deltas for `effective_exertion_slope_28d` × `resting_hr`, `exertion_rank_composite_lagged_lcera` × `resting_hr`, etc. Memory: `feedback_crash_distortion_sensitivity`. **Operational rule**: every Layer 4+ correlation / CCF result must include a crash-drop sensitivity row in its output. Headline VIF max = 7.61 (`hr_area_above_daytime_baseline_waking_lcera`); condition number = 7.28; no severe multicollinearity outside the five flagged pairs. **B*** delta block: `_lagged` and `_lcera` variants are functionally identical on the LC frame (Δρ = +0.000 across 10 pairs); the LC-era restriction matters at the 2022-05-18 → 2022-07-03 boundary only. Block F pre-registered 20 CCF pairs for Layer 4. |
| 2026-06-12 | Layer 3 spot-investigation — `in_umbrella` split into per-period booleans | Layer 3 Block E showed `in_umbrella=True` median gevoelscore = 5 vs `False` = 4. Spot-investigation (`c:/tmp/layer3_spot_investigate.py`) traced the gap to **year confounding**: `in_umbrella=False` is entirely in 2022–2024 (worse-recovery years), while `in_umbrella=True` is dominated by 2025–2026 (49% of True days). Within-year deltas drop to +0.16 / +0.38 in 2023 / 2024; the headline gap is mostly multi-year year-effect bleeding through. Also: `in_umbrella=False` has 15.82% crash rate vs True 5.02%. **`in_umbrella` flagged as descriptive-only** (note added on row in §11). **Three per-period booleans added** to the build script and §11 as the analytical surface: `in_citalopram_traject` (788 LC days, 2024-04 → ongoing), `in_pwc_reintegratie_2023` (268 LC days, 2023), `in_relational_spanning_2024` (172 LC days, nested entirely inside `in_citalopram_traject`). Substrings match the canonical name prefix in `hand_curated_spans.yaml`; new umbrella periods added later require an explicit entry in `UMBRELLA_FLAGS` in `build_unified_dataset.py`. OR over the three exactly matches the legacy `in_umbrella` (1056 LC days). Master 168 → 171 cols. |
| 2026-06-12 | Layer 3 spot-investigation — `exertion_class_lagged_lcera` light vs none clarified | Layer 3 Block E table showed median gevoelscore 4 for `none` AND `light`, 5 for `moderate` / `heavy` / `very_heavy` (the earlier in-conversation summary that called out `light` as the single lowest class was a misread). Means are essentially monotonic: none 4.28 → light 4.30 → moderate 4.39 → heavy 4.46 → very_heavy 4.59. The mild "low-exertion → low gevoelscore" pattern is **reverse-causal at the daily level**: crash days populate `none` (8.05%) and `light` (9.28%) at 2-3× the rate of `very_heavy` (3.85%), and cat_symptoom_fysiek presence drops from 77.4% (none) to 61.9% (heavy). The lagged-baseline classifier is doing its job. No bug. Reinforces the crash-distortion guardrail above: any PEM-pacing contrast on `exertion_class_lagged_lcera` must include a crash-drop sensitivity row. |
| 2026-06-12 | Naproxen umbrella — 4th per-period boolean | Added `in_naproxen_interventie` to §11. The "Naproxen-interventie" span existed in `hand_curated_spans.yaml` since the Wave-3 curation pass (start 2025-03-27, capped 2026-06-10), but its label lacked the keyword "umbrella" and was therefore invisible to the umbrella detector. **Curation edit**: renamed the YAML label from `Naproxen-interventie (ongoing, ad-hoc gebruik bij hoofdpijn)` to `Naproxen-interventie (umbrella, 2025-03 -> ongoing, ad-hoc gebruik bij hoofdpijn)`; re-ran `merge_calendar_triage.py` to propagate. **Code edit**: added `"in_naproxen_interventie": "Naproxen-interventie"` to `UMBRELLA_FLAGS` in `build_unified_dataset.py`. Boundary verified against `note_text`: first `naprox` mention = 2025-03-27, matches the YAML start exactly. **LC frame counts**: 436 / 1524 True days (28.6%); **all 436 are also `in_citalopram_traject=True`** (nested inside the Citalopram trajectory). The ~20 actual-usage events remain encoded as `naproxen` tags in `event_labels` — independent from the umbrella period. Master 171 → 172 cols. |
