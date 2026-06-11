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
  - `presence_conditioned_positive_evidence` ⚠️ — exists only when a
    note exists on the date; value > 0 is positive evidence, value = 0
    on a note-day is *low-specificity* about absence, `NaN` on a
    no-note day. See
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
| `era` | derived | computed from `date` | — | category | `pre_score` (< 2022-09-03), `train` (2022-09-03 → 2023-12-31), `validate` (2024-01-01 → today) | full | never null | matches existing crash_v2 era split — pre-registered before the validate-era data came in, so the boundary is methodologically defensible |

---

## Section 1 — subjective state (gevoelscore + note)

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `gevoelscore` | daily_computed | `raw/directus_exports/day_entries.json` | `score` | float64 (nullable int) | 1-10 (in practice 1-6 dense, 7-10 sparse) | 2022-09-03 → today | NaN when no entry that day | the primary subjective signal |
| `has_note` | derived | computed | — | bool | True when `note_text` is non-empty | full | never null | **mandatory companion** to every presence-conditioned column |
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
| `intensity_source` | daily_computed | `processed/manual_triage/per_day_intensity.csv` | `source` | category | `consolidation_YYYY-MM-DD`, `bulk_triage_YYYY_YYYY-MM-DD`, `bulk_triage_YYYY_no_info`, `manual_*`, `triage_notes_classified`, `pwc_cross_validation_2026-06-11` | matches `per_day_intensity.csv` | empty string when not in source (= not yet triaged); a non-empty value is the **mandatory companion** to interpret cog/phy/emo loads | `*_no_info` is presence-conditioned **explicit absence** (user reviewed, found no load-bearing material). Distinct from empty source (= unreviewed) |
| `intensity_notes` | presence_conditioned ⚠️ | `processed/manual_triage/per_day_intensity.csv` | `notes` | object (string) | free text | matches | empty string when no notes | **personal data — external only**; same gating rule as cog/phy/emo |

---

## Section 3 — research-derived crash labels

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `is_crash` | daily_computed | `processed/crash_labels/labels_crash_v2.csv` | `is_crash` (or derived from `label`) | bool | True if day inside a v2 crash episode | 2022-09-03 → today | False outside any episode | see [methodology/crash_v2_definition.md](methodology/crash_v2_definition.md) |
| `is_dip` | daily_computed | `processed/crash_labels/labels_crash_v2.csv` | `is_dip` (or derived) | bool | True if day is a v2 isolated single-day dip | 2022-09-03 → today | False otherwise | |
| `crash_episode_id` | daily_computed | `processed/crash_labels/labels_crash_v2.csv` | `episode_id` | object (string) | episode identifier (e.g. `EP_2023_06_05`) | matches | empty when not in an episode | groups multi-day crashes |
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

---

## Section 5 — Garmin heart rate

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `resting_hr` | daily_computed | `processed/garmin/daily_uds.csv` | `resting_hr` | float64 | bpm | 2021-08-16 → today (1731 of 1755 days) | NaN on FIT-gap day; Garmin's algorithmic RHR is passed through directly (no sanity filter — observed range is 47-65 bpm with 0 outliers, see [methodology/garmin_indicators_audit.md](methodology/garmin_indicators_audit.md)) | **nightly attribution applies** — Garmin computes RHR during sleep; the value is attributed to the wake-up date. See [methodology/nightly_attribution.md](methodology/nightly_attribution.md) |
| `min_hr` | daily_computed | `processed/garmin/daily_uds.csv` | `min_hr` | float64 | bpm | same | NaN on gap | |
| `max_hr` | daily_computed | `processed/garmin/daily_uds.csv` | `max_hr` | float64 | bpm | same | NaN on gap | |
| `max_avg_hr_uds` | daily_computed | `processed/garmin/daily_uds.csv` | `max_avg_hr` | float64 | bpm | same | NaN on gap | Garmin UDS "max-of-averages" metric (max value across averaging windows) — NOT a daily mean. Use cautiously; the daily true mean is not in UDS. |

---

## Section 6 — Garmin exertion features (engineered)

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `exertion_class` | daily_computed | `processed/garmin/activity_features_daily.csv` | `exertion_class` | category | `very_light`, `light`, `moderate`, `heavy`, `very_heavy` | 2021-08-16 → today (1.754 days) | NaN on gap | v3.1 spec, 4-axis percentile rank against rolling personal baseline; see `analyses/garmin_exploration/exertion-class-definition.md` |
| `effective_exertion_min` | daily_computed | `processed/garmin/activity_features_daily.csv` | `effective_exertion_min` | float64 | minutes | same | NaN on gap | |
| `step_z_30d` | daily_computed | `processed/garmin/activity_features_daily.csv` | `step_z_30d` | float64 | z-score of daily steps vs 30d rolling baseline | same | NaN on gap | step-based; do not interpret as a generic "intensity z-score" — earlier draft renamed it from the misleading `intensity_z_score` proxy |

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

---

## Section 8 — Garmin stress spikes (daytime)

| name | class | source | source column | dtype | units | coverage | missingness | notes |
|---|---|---|---|---|---|---|---|---|
| `max_spike_minutes` | daily_computed | `processed/garmin/daily_max_spike.csv` | `max_spike_minutes` | float64 (nullable int) | minutes of longest stress spike > 75 | 2021-08-16 → today (1.737 days) | NaN on gap | from H02b extraction |

---

## Section 9 — note categorization rollup (presence-conditioned)

⚠️ **All columns in this section are `presence_conditioned_positive_evidence`.**
Gate on `has_note=True` before interpreting. Value 0 on a note-day is
*low-specificity about absence* — see
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

⚠️ All `presence_conditioned_positive_evidence`. Same gating rules
as §9.

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
| `n_events_on_day` | daily_computed | `raw/directus_exports/annotations.yaml` + `processed/manual_triage/triage_events.csv` | derived | float64 (nullable int) | count of span-or-marker entries covering the date | 2021-08-16 → today (events range varies) | 0 when no events | |
| `event_labels` | daily_computed | same | derived | object (string) | semicolon-separated event titles | matches | empty string when 0 events | **may contain personal references; external only** |
| `event_categories` | daily_computed | same | derived | object (string) | semicolon-separated from `{crash, dip, high_intensity, interventie, levensgebeurtenis, medical, trigger, marker}` | matches | empty when 0 events | |
| `in_umbrella` | derived | annotations.yaml | computed | bool | True if covered by a span whose label contains the word `umbrella` (e.g. "PwC reintegratie 2023 (umbrella)", "Citalopram-traject (umbrella, 2024-04 -> ongoing)") | full | False otherwise | matches the explicit user-curated marker per methodology §4. Earlier draft also flagged any `levensgebeurtenis > 14 days` as an umbrella; that arbitrary fallback was removed 2026-06-11. |
| `umbrella_labels` | derived | same | computed | object (string) | semicolon-separated | matches | empty | |

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
| `dossier_event_today` | derived | from triage_events.csv where `source=pwc_dossier_2022-2024` | bool | full | False otherwise | True if any dossier-sourced event on the date |
| `dossier_event_labels` | derived | same | object (string) | full | empty otherwise | semicolon list |
| `dossier_event_categories` | derived | same | object (string) | full | empty | subset of `{medical, levensgebeurtenis, marker}` per the dossier review |

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

---

## Coverage matrix (cross-source)

Use this table to know which signals exist when querying any specific
date range:

| date range | gevoelscore | notes (asymm.) | Garmin UDS | sleep-stress | PwC log | PwC dossier | intensity triage |
|---|---|---|---|---|---|---|---|
| 2021-08-16 → 2022-09-02 | – | – | ✓ | ✓ | – | – | – |
| 2022-09-03 → 2022-09-25 | ✓ | partial | ✓ | ✓ | – | ✓ | – |
| 2022-09-26 → 2024-02-26 | ✓ | partial | ✓ | ✓ | ✓ | ✓ | ✓ (2022-2024 done) |
| 2024-02-27 → 2024-07-18 | ✓ | partial | ✓ | ✓ | – | ✓ | ✓ |
| 2024-07-19 → today | ✓ | varies | ✓ | ✓ | – | – | ✓ |

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
| 2026-06-11 | Phase B audit | removed `push_burden_7d` column. The Garmin indicators audit ([methodology/garmin_indicators_audit.md](methodology/garmin_indicators_audit.md)) confirmed the known rolling-baseline-contamination issue. A v3.2 lagged variant (`push_burden_7d_lagged`) exists upstream but is also held back from the master: per the established schema discipline (same reasoning as `stabilisation_period`), we don't surface a known-broken metric even with a caveat, nor pre-commit to its replacement before descriptive analysis motivates the choice. When the need surfaces, the lagged variant can be added cleanly. |
| 2026-06-11 | Phase B refinement | removed `stabilisation_period` column. Initial draft had it as a bool True for 2024-01-01 → 2025-06-30 sourced from a fuzzy user-trajectory memory note ("pendulum settling across 2023→2025"). The boundaries were neither pre-registered nor data-driven — they were post-hoc qualitative guesses. The honest classification of a stabilisation period belongs in descriptive-analysis output (e.g. a threshold on `gevoelscore_rolling_std_90d`) rather than in the schema. If a data-driven stabilisation indicator emerges later, it joins the dictionary then. |
| 2026-06-11 | Phase B build verified | first build (1755 rows × 89 cols) ran clean on 5-date spot-check; 81 forward-dated rows pruned from `per_day_intensity.csv` source. Date range capped at last_score_date (`max(day_entries.date)`) for reproducibility. |
