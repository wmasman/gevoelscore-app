# Findings -- coverage_overview Strand B Q4.6

**Question** (per [`descriptive/README.md` sec 4.6](../../README.md)): When does which Garmin signal become available? What missingness patterns matter for hypothesis design?

**LOAD-BEARING INFRASTRUCTURE foundation** for future HA pre-regs + remaining Tier 3 Strand B topics. Per descriptive README sec 4.6 the gap this analysis closes: 'coherent coverage-overview analysis that any HA pre-reg can cite for this column is available from date X with coverage Y%'.

**User-LOCKED operationalisation per Strand B sec 7c interview 2026-06-25** (do NOT iterate):
1. **Channel scope = all per_day_master columns** (201 enumerated; skips per-minute / per-bout which have own MDs).
2. **Coverage metric = both day-level + 28d rolling** (binary 'available?' + 'stable coverage?').
3. **Date-range slicing = continuous + per-recovery-phase** (6 phases per [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md)).
4. **Missingness pattern = full** (descriptive + block-length + MCAR/MAR diagnostic via Welch-style chi-square; method choice documented at the Stage 5 docstring in [`run.py`](run.py)).

**Discipline anchors** (CONVENTIONS): sec 2.1 descriptive-before-inference (no causal claims, no HA verdict promotion); sec 3.3 NO pre-commitment of MCAR/MAR readings for HAs not yet pre-spec'd (this diagnostic is descriptive infrastructure ONLY); sec 4.1 + 4.2 no interpretive marks; pipeline-vs-documentation drift honestly surfaced per [[feedback_flag_contradictions]] (extends Q3.8 push_burden_7d pattern across all columns).

---

## 1. Headline

**201 columns enumerated**; **200 present in `per_day_master.csv`**; **1 documented but absent from master** (pipeline-vs-doc drift). Total of 1754 day-level rows in the corpus (2021-08-16 to 2026-06-04).

**Coverage span** (first available dates across families):
- **Earliest coverage starts 2021-08-16** (Garmin extract start; covers UDS daily activity + heart rate + sleep stress + phys extras + activity rank base).
- **gevoelscore corpus starts 2022-09-03** (DATA_DICTIONARY sec 1).
- **bb_overnight_gain truth starts 2024-09-18** (Garmin SLEEPEND UDS rollout on FR245 per [`bb_overnight_gain_proxy.md`](../../../../methodology/bb_overnight_gain_proxy.md)); proxy bridges 2024-07-08 -> 2024-09-17 (74 day net).
- **PwC log window 2022-09-26 -> 2024-02-26** (sec 12).
- **dose_plasma_mg = 0 pre-2024-04-09** (citalopram buildup start; always-populated channel).

**Missingness diagnostic verdict counts**: reject_MCAR = 89; fail_to_reject_MCAR = 0; skipped = 45; no_test = 67. **MNAR-suspect channels (descriptive flag only)**: 49.

**Pipeline-vs-documentation drift** (extends Q3.8 push_burden_7d finding per [[feedback_flag_contradictions]]): 7 channels surface drift (column absent from master despite DATA_DICTIONARY entry, OR first-available date drifts >30 days from documented start). See Section 6 for the full listing; the Q3.8 finding (v3.1 push_burden_7d documented in CONVENTIONS sec 3.2 but dropped per audit MD 2026-06-11 item 2) is reproduced + extended.

---

## 2. Stage 1 -- column family enumeration

Column family taxonomy per DATA_DICTIONARY sec 0-14 + sec 7B + sec 8B-E. Per-family channel counts (in master vs documented-but-absent):

| family | n_in_master | n_documented_absent |
|---|---:|---:|
| 0_identity | 5 | 0 |
| 10_notes_subtypes_fysiek | 10 | 0 |
| 11_timeline_events | 9 | 0 |
| 12_pwc_log | 8 | 0 |
| 13_pwc_dossier | 3 | 0 |
| 14_coverage_flags | 8 | 0 |
| 1_subjective | 2 | 0 |
| 2_manual_triage | 5 | 0 |
| 3_crash_labels | 5 | 0 |
| 4_garmin_daily_activity | 9 | 0 |
| 5_garmin_heart_rate | 4 | 0 |
| 6_citalopram_plasma | 1 | 0 |
| 6_garmin_exertion_v3_1 | 7 | 1 |
| 6_garmin_exertion_v3_2_lagged | 13 | 0 |
| 6_garmin_exertion_v3_2_lcera | 11 | 0 |
| 6_garmin_exertion_v3_2_z | 6 | 0 |
| 7B_garmin_phys_extras_BB | 11 | 0 |
| 7B_garmin_phys_extras_respiration_24h | 3 | 0 |
| 7B_garmin_phys_extras_spo2_24h | 2 | 0 |
| 7B_garmin_phys_extras_stress | 5 | 0 |
| 7_garmin_sleep_stress | 18 | 0 |
| 8B_intraday_A4 | 11 | 0 |
| 8B_intraday_C4 | 4 | 0 |
| 8C_stress_low_motion | 11 | 0 |
| 8D_udip | 1 | 0 |
| 8E_bout_level | 5 | 0 |
| 8_garmin_spikes | 1 | 0 |
| 9_notes_categorization | 22 | 0 |

Each channel pegged to its DATA_DICTIONARY section. The `bb_overnight_gain` family inherits the 4-column `{bb_overnight_gain, _proxy, _best, _source}` audit-chain per [`bb_overnight_gain_proxy.md` sec 4.1](../../../../methodology/bb_overnight_gain_proxy.md). The `stress_low_motion_min_count_*` family inherits the Session E lock per [`stress_low_motion_primitive.md`](../../../../methodology/stress_low_motion_primitive.md).

---

## 3. Stage 2 -- day-level coverage headlines

Per-channel first/last-available dates + total % coverage + continuity flag (continuity_flag = `pct_in_window >= 0.80` where window = [first, last]). Channels NOT in master skipped.

| channel | family | first | pct_total | last | continuity |
|---|---|---|---:|---|---|
| `above_baseline_streak` | 6_garmin_exertion_v3_2_lagged | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `active_sec` | 4_garmin_daily_activity | 2021-08-16 | 98.9% | 2026-05-29 | YES |
| `all_day_stress_avg` | 7B_garmin_phys_extras_stress | 2021-08-17 | 98.7% | 2026-05-29 | YES |
| `all_day_stress_avg_lagged_lcera_z` | 6_garmin_exertion_v3_2_z | 2022-05-08 | 83.7% | 2026-05-29 | YES |
| `all_day_stress_max` | 7B_garmin_phys_extras_stress | 2021-08-16 | 98.8% | 2026-05-29 | YES |
| `asleep_stress_avg_uds` | 7B_garmin_phys_extras_stress | 2021-08-17 | 98.2% | 2026-05-29 | YES |
| `awake_stress_avg` | 7B_garmin_phys_extras_stress | 2021-08-17 | 98.7% | 2026-05-29 | YES |
| `awake_stress_max` | 7B_garmin_phys_extras_stress | 2021-08-16 | 98.8% | 2026-05-29 | YES |
| `bb_charged_24h` | 7B_garmin_phys_extras_BB | 2021-08-17 | 98.7% | 2026-05-29 | YES |
| `bb_drained_24h` | 7B_garmin_phys_extras_BB | 2021-08-17 | 98.7% | 2026-05-29 | YES |
| `bb_during_sleep_value` | 7B_garmin_phys_extras_BB | 2023-12-18 | 49.1% | 2026-05-29 | YES |
| `bb_highest` | 7B_garmin_phys_extras_BB | 2021-08-17 | 98.7% | 2026-05-29 | YES |
| `bb_lowest` | 7B_garmin_phys_extras_BB | 2021-08-17 | 98.7% | 2026-05-29 | YES |
| `bb_lowest_lagged_lcera_z` | 6_garmin_exertion_v3_2_z | 2022-05-17 | 82.6% | 2026-05-29 | YES |
| `bb_overnight_gain` | 7B_garmin_phys_extras_BB | 2024-09-18 | 33.8% | 2026-05-29 | YES |
| `bb_overnight_gain_best` | 7B_garmin_phys_extras_BB | 2024-07-08 | 38.0% | 2026-05-29 | YES |
| `bb_overnight_gain_lagged_lcera_z` | 6_garmin_exertion_v3_2_z | 2024-10-22 | 32.1% | 2026-05-29 | YES (delta -56d vs doc 2024-12-17) |
| `bb_overnight_gain_proxy` | 7B_garmin_phys_extras_BB | 2024-07-08 | 38.0% | 2026-05-29 | YES |
| `bb_overnight_gain_source` | 7B_garmin_phys_extras_BB | 2024-07-08 | 38.0% | 2026-05-29 | YES |
| `bb_sleep_end_value` | 7B_garmin_phys_extras_BB | 2024-09-18 | 33.8% | 2026-05-29 | YES |
| `bb_sleep_start_value` | 7B_garmin_phys_extras_BB | 2024-07-08 | 38.0% | 2026-05-29 | YES |
| `bedtime_hour_local` | 7_garmin_sleep_stress | 2021-08-18 | 97.3% | 2026-05-29 | YES |
| `bedtime_std_7d` | 7_garmin_sleep_stress | 2021-08-19 | 99.8% | 2026-06-04 | YES |
| `bout_max_peak_height_day` | 8E_bout_level | 2022-04-04 | 84.3% | 2026-06-04 | YES |
| `bout_n_did_not_return` | 8E_bout_level | 2022-04-04 | 84.7% | 2026-06-04 | YES |
| `bout_n_fast_recovery_day` | 8E_bout_level | 2022-04-04 | 84.7% | 2026-06-04 | YES (delta +231d vs doc 2021-08-16) |
| `bout_n_per_day` | 8E_bout_level | 2022-04-04 | 84.7% | 2026-06-04 | YES |
| `bout_total_AUC_day` | 8E_bout_level | 2022-04-04 | 84.5% | 2026-06-04 | YES |
| `cat_belasting_cognitief` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_belasting_emotioneel` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_belasting_fysiek` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_belasting_gezin` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_belasting_sociaal` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_context_neutraal` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_medicatie` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_recovery_actie` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_sub_gastro` | 10_notes_subtypes_fysiek | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_sub_hoofdpijn` | 10_notes_subtypes_fysiek | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_sub_huid` | 10_notes_subtypes_fysiek | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_sub_keel_resp` | 10_notes_subtypes_fysiek | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_sub_koorts` | 10_notes_subtypes_fysiek | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_sub_neuro` | 10_notes_subtypes_fysiek | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_sub_overig` | 10_notes_subtypes_fysiek | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_sub_slaap` | 10_notes_subtypes_fysiek | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_sub_spier` | 10_notes_subtypes_fysiek | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_sub_systemisch_vermoeid` | 10_notes_subtypes_fysiek | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_symptoom_cognitief` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_symptoom_emotioneel` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_symptoom_fysiek` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `cat_triggers_extern` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `class_axis_A_eff` | 6_garmin_exertion_v3_1 | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `class_axis_A_eff_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-10-25 | 96.0% | 2026-06-04 | YES |
| `class_axis_A_eff_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2022-06-13 | 82.8% | 2026-06-04 | YES |
| `class_axis_B_step` | 6_garmin_exertion_v3_1 | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `class_axis_B_step_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-10-25 | 96.0% | 2026-06-04 | YES |
| `class_axis_B_step_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2022-06-13 | 82.8% | 2026-06-04 | YES |
| `class_axis_C_maxhr` | 6_garmin_exertion_v3_1 | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `class_axis_C_maxhr_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-10-25 | 96.0% | 2026-06-04 | YES |
| `class_axis_C_maxhr_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2022-06-13 | 82.8% | 2026-06-04 | YES |
| `class_axis_D_vig` | 6_garmin_exertion_v3_1 | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `class_axis_D_vig_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-10-25 | 96.0% | 2026-06-04 | YES |
| `class_axis_D_vig_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2022-06-13 | 82.8% | 2026-06-04 | YES |
| `cog_load` | 2_manual_triage | 2022-04-01 | 20.4% | 2026-06-03 | no |
| `crash_episode_id` | 3_crash_labels | 2022-09-03 | 10.4% | 2026-05-21 | no |
| `daily_step_goal` | 4_garmin_daily_activity | 2021-08-16 | 98.9% | 2026-05-29 | YES |
| `date` | 0_identity | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `day_dominant_polarity` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `day_of_week` | 0_identity | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `dip_type` | 3_crash_labels | 2022-11-05 | 2.0% | 2026-06-03 | no |
| `dose_plasma_mg` | 6_citalopram_plasma | 2021-08-16 | 100.0% | 2026-06-04 | YES (delta -967d vs doc 2024-04-09) |
| `dossier_event_categories` | 13_pwc_dossier | 2022-03-28 | 3.9% | 2024-01-29 | no |
| `dossier_event_labels` | 13_pwc_dossier | 2022-03-28 | 3.9% | 2024-01-29 | no |
| `dossier_event_today` | 13_pwc_dossier | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `eff_exertion_rank_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-10-25 | 96.0% | 2026-06-04 | YES |
| `eff_exertion_rank_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2022-06-13 | 82.8% | 2026-06-04 | YES |
| `effective_exertion_min` | 6_garmin_exertion_v3_1 | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `effective_exertion_slope_28d` | 6_garmin_exertion_v3_2_lagged | 2021-09-06 | 98.8% | 2026-06-04 | YES |
| `emo_load` | 2_manual_triage | 2022-09-14 | 9.4% | 2026-06-04 | no |
| `era` | 0_identity | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `event_categories` | 11_timeline_events | 2021-08-16 | 95.9% | 2026-06-04 | YES |
| `event_labels` | 11_timeline_events | 2021-08-16 | 95.9% | 2026-06-04 | YES |
| `exertion_class` | 6_garmin_exertion_v3_1 | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `exertion_class_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-10-25 | 96.0% | 2026-06-04 | YES (delta +70d vs doc 2021-08-16) |
| `exertion_class_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2022-06-13 | 82.8% | 2026-06-04 | YES |
| `exertion_rank_composite_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-10-25 | 96.0% | 2026-06-04 | YES |
| `exertion_rank_composite_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2022-06-13 | 82.8% | 2026-06-04 | YES |
| `gevoelscore` | 1_subjective | 2022-09-03 | 78.2% | 2026-06-04 | YES |
| `has_calendar_coverage` | 14_coverage_flags | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `has_garmin_sleep` | 14_coverage_flags | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `has_garmin_uds` | 14_coverage_flags | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `has_intensity_triage` | 14_coverage_flags | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `has_note` | 14_coverage_flags | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `has_pwc_dossier_window` | 14_coverage_flags | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `has_pwc_log` | 14_coverage_flags | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `has_score` | 14_coverage_flags | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `highly_active_sec` | 4_garmin_daily_activity | 2021-08-16 | 98.9% | 2026-05-29 | YES |
| `hr_area_above_daytime_baseline_waking` | 8B_intraday_A4 | 2021-09-29 | 96.6% | 2026-06-04 | YES |
| `hr_area_above_daytime_baseline_waking_lcera` | 8B_intraday_A4 | 2022-05-18 | 83.4% | 2026-06-04 | YES |
| `hr_daytime_baseline_lagged` | 8B_intraday_A4 | 2021-09-29 | 96.6% | 2026-06-04 | YES (delta +44d vs doc 2021-08-16) |
| `hr_daytime_baseline_lagged_lcera` | 8B_intraday_A4 | 2022-05-18 | 83.4% | 2026-06-04 | YES |
| `hr_longest_elevated_run_min_waking` | 8B_intraday_A4 | 2021-09-29 | 96.6% | 2026-06-04 | YES |
| `hr_longest_elevated_run_min_waking_lcera` | 8B_intraday_A4 | 2022-05-18 | 83.4% | 2026-06-04 | YES |
| `hr_median_waking` | 8B_intraday_A4 | 2021-08-16 | 98.6% | 2026-06-04 | YES |
| `hr_min_above_daytime_baseline_plus_20_waking` | 8B_intraday_A4 | 2021-09-29 | 96.6% | 2026-06-04 | YES |
| `hr_min_above_daytime_baseline_plus_20_waking_lcera` | 8B_intraday_A4 | 2022-05-18 | 83.4% | 2026-06-04 | YES |
| `hr_sustained_elevated_flag` | 8B_intraday_A4 | 2021-09-29 | 96.6% | 2026-06-04 | YES |
| `hr_sustained_elevated_flag_lcera` | 8B_intraday_A4 | 2022-05-18 | 83.4% | 2026-06-04 | YES |
| `in_citalopram_traject` | 11_timeline_events | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `in_naproxen_interventie` | 11_timeline_events | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `in_pwc_reintegratie_2023` | 11_timeline_events | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `in_relational_spanning_2024` | 11_timeline_events | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `in_umbrella` | 11_timeline_events | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `intensity_notes` | 2_manual_triage | 2022-01-01 | 76.5% | 2026-06-04 | YES |
| `intensity_source` | 2_manual_triage | 2022-01-01 | 88.7% | 2026-06-04 | YES |
| `is_crash` | 3_crash_labels | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `is_dip` | 3_crash_labels | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `is_sub_threshold_dip` | 3_crash_labels | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `is_vigorous_day` | 4_garmin_daily_activity | 2023-12-13 | 51.1% | 2026-05-29 | YES |
| `lc_phase` | 0_identity | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `max_avg_hr_uds` | 5_garmin_heart_rate | 2021-08-16 | 98.8% | 2026-05-29 | YES |
| `max_hr` | 5_garmin_heart_rate | 2021-08-16 | 98.8% | 2026-05-29 | YES |
| `max_hr_rank_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-10-25 | 94.8% | 2026-05-29 | YES |
| `max_hr_rank_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2022-06-13 | 81.6% | 2026-05-29 | YES |
| `max_spike_minutes` | 8_garmin_spikes | 2021-08-17 | 99.0% | 2026-06-04 | YES |
| `min_hr` | 5_garmin_heart_rate | 2021-08-16 | 98.8% | 2026-05-29 | YES |
| `moderate_min` | 4_garmin_daily_activity | 2021-08-16 | 98.9% | 2026-05-29 | YES |
| `n_clauses` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `n_events_on_day` | 11_timeline_events | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `n_minutes_resp_above_18` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `n_minutes_resp_in_rest_band_10_18` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `n_mixed_clauses` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `n_neg_clauses` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `n_neutral_clauses` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `n_pos_clauses` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `neutral_forward_looking_flag` | 9_notes_categorization | 2022-10-18 | 39.1% | 2026-06-04 | no |
| `note_text` | 1_subjective | 2022-10-18 | 39.1% | 2026-06-04 | no (delta +45d vs doc 2022-09-03) |
| `phy_load` | 2_manual_triage | 2022-04-01 | 15.8% | 2026-06-03 | no |
| `push_burden_7d_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `push_burden_7d_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `pwc_amsterdam_flag` | 12_pwc_log | 2022-09-26 | 13.6% | 2024-02-26 | no |
| `pwc_doctor_visit_flag` | 12_pwc_log | 2022-09-26 | 13.6% | 2024-02-26 | no |
| `pwc_illness_flag` | 12_pwc_log | 2022-09-26 | 13.6% | 2024-02-26 | no |
| `pwc_primary_hours` | 12_pwc_log | 2022-09-26 | 13.5% | 2024-02-26 | no |
| `pwc_secondary_hours` | 12_pwc_log | 2023-03-07 | 1.8% | 2024-01-30 | no |
| `pwc_toelichting` | 12_pwc_log | 2022-09-26 | 12.7% | 2024-02-26 | no |
| `pwc_total_hours` | 12_pwc_log | 2022-09-26 | 13.6% | 2024-02-26 | no |
| `pwc_vacation_flag` | 12_pwc_log | 2022-09-26 | 13.6% | 2024-02-26 | no |
| `recovery_phase` | 0_identity | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `respiration_avg_sleep` | 7_garmin_sleep_stress | 2021-08-18 | 97.1% | 2026-05-29 | YES |
| `respiration_avg_sleep_lagged_lcera_z` | 6_garmin_exertion_v3_2_z | 2022-05-09 | 23.0% | 2026-05-29 | no |
| `respiration_avg_waking` | 7B_garmin_phys_extras_respiration_24h | 2021-08-17 | 98.7% | 2026-05-29 | YES |
| `respiration_max_24h` | 7B_garmin_phys_extras_respiration_24h | 2021-08-17 | 98.7% | 2026-05-29 | YES |
| `respiration_max_sleep` | 7_garmin_sleep_stress | 2021-08-18 | 97.1% | 2026-05-29 | YES |
| `respiration_min_24h` | 7B_garmin_phys_extras_respiration_24h | 2021-08-17 | 98.7% | 2026-05-29 | YES |
| `respiration_min_sleep` | 7_garmin_sleep_stress | 2021-08-18 | 97.1% | 2026-05-29 | YES |
| `resting_hr` | 5_garmin_heart_rate | 2021-08-16 | 98.7% | 2026-05-29 | YES |
| `resting_hr_lagged_lcera_z` | 6_garmin_exertion_v3_2_z | 2022-05-09 | 78.1% | 2026-05-21 | YES |
| `sleep_awake_min` | 7_garmin_sleep_stress | 2021-08-17 | 97.7% | 2026-05-29 | YES |
| `sleep_deep_min` | 7_garmin_sleep_stress | 2021-08-17 | 97.7% | 2026-05-29 | YES |
| `sleep_duration_min` | 7_garmin_sleep_stress | 2021-08-18 | 97.3% | 2026-05-29 | YES |
| `sleep_end_gmt` | 7_garmin_sleep_stress | 2021-08-16 | 98.9% | 2026-05-29 | YES |
| `sleep_light_min` | 7_garmin_sleep_stress | 2021-08-17 | 97.7% | 2026-05-29 | YES |
| `sleep_start_afternoon_flag` | 7_garmin_sleep_stress | 2021-08-18 | 97.3% | 2026-05-29 | YES |
| `sleep_start_gmt` | 7_garmin_sleep_stress | 2021-08-16 | 98.9% | 2026-05-29 | YES |
| `sleep_unmeasurable_min` | 7_garmin_sleep_stress | 2021-08-17 | 97.7% | 2026-05-29 | YES |
| `sleep_valid_flag` | 7_garmin_sleep_stress | 2021-08-16 | 100.0% | 2026-06-04 | YES |
| `spo2_avg_24h` | 7B_garmin_phys_extras_spo2_24h | 2021-08-16 | 96.2% | 2026-05-29 | YES |
| `spo2_avg_sleep` | 7_garmin_sleep_stress | 2021-08-17 | 86.7% | 2026-05-29 | YES |
| `spo2_min_24h` | 7B_garmin_phys_extras_spo2_24h | 2021-08-16 | 96.2% | 2026-05-29 | YES |
| `spo2_min_sleep` | 7_garmin_sleep_stress | 2021-08-17 | 86.7% | 2026-05-29 | YES |
| `state_symptoom_cognitief` | 9_notes_categorization | 2023-01-31 | 2.6% | 2026-06-03 | no |
| `state_symptoom_emotioneel` | 9_notes_categorization | 2023-09-19 | 0.1% | 2024-11-09 | no |
| `state_symptoom_fysiek` | 9_notes_categorization | 2022-10-18 | 27.1% | 2026-06-04 | no |
| `step_rank_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-10-25 | 94.8% | 2026-05-29 | YES |
| `step_rank_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2022-06-13 | 81.6% | 2026-05-29 | YES |
| `step_z_30d` | 6_garmin_exertion_v3_1 | 2021-09-05 | 97.6% | 2026-05-29 | YES |
| `steps_above_goal_flag` | 4_garmin_daily_activity | 2021-08-16 | 98.7% | 2026-05-29 | YES |
| `stress_high_duration_min` | 8B_intraday_C4 | 2021-08-17 | 99.0% | 2026-06-04 | YES |
| `stress_low_motion_min_count_S50_Mbelow_mod` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `stress_low_motion_min_count_S50_Mlow` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `stress_low_motion_min_count_S50_Mstrict` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `stress_low_motion_min_count_S60_Mbelow_mod` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `stress_low_motion_min_count_S60_Mlow` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `stress_low_motion_min_count_S60_Mstrict` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `stress_low_motion_min_count_S75_Mbelow_mod` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `stress_low_motion_min_count_S75_Mlow` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `stress_low_motion_min_count_S75_Mstrict` | 8C_stress_low_motion | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `stress_mean_sleep` | 7_garmin_sleep_stress | 2021-08-18 | 97.3% | 2026-05-29 | YES |
| `stress_mean_sleep_lagged_lcera_z` | 6_garmin_exertion_v3_2_z | 2022-05-08 | 82.4% | 2026-05-29 | YES |
| `stress_post_peak_drop_avg` | 8B_intraday_C4 | 2021-08-17 | 98.1% | 2026-06-04 | YES |
| `stress_post_peak_time_to_rest_min` | 8B_intraday_C4 | 2021-08-19 | 86.8% | 2026-06-04 | YES |
| `stress_recovery_pct_within_2h` | 8B_intraday_C4 | 2021-08-19 | 87.0% | 2026-06-04 | YES |
| `stress_stdev_sleep` | 7_garmin_sleep_stress | 2021-08-18 | 97.3% | 2026-05-29 | YES |
| `total_calories` | 4_garmin_daily_activity | 2021-08-16 | 98.9% | 2026-05-29 | YES |
| `total_steps` | 4_garmin_daily_activity | 2021-08-16 | 98.7% | 2026-05-29 | YES |
| `u_dip_count` | 8D_udip | 2021-08-16 | 99.1% | 2026-06-04 | YES |
| `umbrella_labels` | 11_timeline_events | 2023-03-06 | 60.1% | 2026-06-04 | YES |
| `vigorous_min` | 4_garmin_daily_activity | 2021-08-16 | 98.9% | 2026-05-29 | YES |
| `vigorous_min_rank_lagged` | 6_garmin_exertion_v3_2_lagged | 2021-10-25 | 96.0% | 2026-06-04 | YES |
| `vigorous_min_rank_lagged_lcera` | 6_garmin_exertion_v3_2_lcera | 2022-06-13 | 82.8% | 2026-06-04 | YES |

---

## 4. Stage 3 -- 28d rolling coverage + stable-epoch flag

Per-channel rolling-coverage descriptors: n_stable_days = days where 28d rolling >= 80%; n_inflections = transitions across threshold; longest_stable_run captures the longest contiguous stable-epoch span.

| channel | n_stable_days | longest_stable_run_days | n_inflections | continuity |
|---|---:|---:|---:|---|
| `above_baseline_streak` | 1727 | 1727 | 1 | YES |
| `active_sec` | 1726 | 1726 | 2 | YES |
| `all_day_stress_avg` | 1726 | 1726 | 2 | YES |
| `all_day_stress_avg_lagged_lcera_z` | 1466 | 1466 | 2 | YES |
| `all_day_stress_max` | 1726 | 1726 | 2 | YES |
| `asleep_stress_avg_uds` | 1703 | 1369 | 4 | YES |
| `awake_stress_avg` | 1726 | 1726 | 2 | YES |
| `awake_stress_max` | 1726 | 1726 | 2 | YES |
| `bb_charged_24h` | 1726 | 1726 | 2 | YES |
| `bb_drained_24h` | 1726 | 1726 | 2 | YES |
| `bb_during_sleep_value` | 876 | 876 | 2 | YES |
| `bb_highest` | 1726 | 1726 | 2 | YES |
| `bb_lowest` | 1726 | 1726 | 2 | YES |
| `bb_lowest_lagged_lcera_z` | 1445 | 1445 | 2 | YES |
| `bb_overnight_gain` | 597 | 597 | 2 | YES |
| `bb_overnight_gain_best` | 673 | 673 | 2 | YES |
| `bb_overnight_gain_lagged_lcera_z` | 566 | 566 | 2 | YES |
| `bb_overnight_gain_proxy` | 673 | 673 | 2 | YES |
| `bb_overnight_gain_source` | 673 | 673 | 2 | YES |
| `bb_sleep_end_value` | 597 | 597 | 2 | YES |
| `bb_sleep_start_value` | 673 | 673 | 2 | YES |
| `bedtime_hour_local` | 1702 | 1368 | 4 | YES |
| `bedtime_std_7d` | 1727 | 1727 | 1 | YES |
| `bout_max_peak_height_day` | 1435 | 757 | 7 | YES |
| `bout_n_did_not_return` | 1452 | 757 | 5 | YES |
| `bout_n_fast_recovery_day` | 1452 | 757 | 5 | YES |
| `bout_n_per_day` | 1452 | 757 | 5 | YES |
| `bout_total_AUC_day` | 1452 | 757 | 5 | YES |
| `cat_belasting_cognitief` | 242 | 120 | 20 | no |
| `cat_belasting_emotioneel` | 242 | 120 | 20 | no |
| `cat_belasting_fysiek` | 242 | 120 | 20 | no |
| `cat_belasting_gezin` | 242 | 120 | 20 | no |
| `cat_belasting_sociaal` | 242 | 120 | 20 | no |
| `cat_context_neutraal` | 242 | 120 | 20 | no |
| `cat_medicatie` | 242 | 120 | 20 | no |
| `cat_recovery_actie` | 242 | 120 | 20 | no |
| `cat_sub_gastro` | 242 | 120 | 20 | no |
| `cat_sub_hoofdpijn` | 242 | 120 | 20 | no |
| `cat_sub_huid` | 242 | 120 | 20 | no |
| `cat_sub_keel_resp` | 242 | 120 | 20 | no |
| `cat_sub_koorts` | 242 | 120 | 20 | no |
| `cat_sub_neuro` | 242 | 120 | 20 | no |
| `cat_sub_overig` | 242 | 120 | 20 | no |
| `cat_sub_slaap` | 242 | 120 | 20 | no |
| `cat_sub_spier` | 242 | 120 | 20 | no |
| `cat_sub_systemisch_vermoeid` | 242 | 120 | 20 | no |
| `cat_symptoom_cognitief` | 242 | 120 | 20 | no |
| `cat_symptoom_emotioneel` | 242 | 120 | 20 | no |
| `cat_symptoom_fysiek` | 242 | 120 | 20 | no |
| `cat_triggers_extern` | 242 | 120 | 20 | no |
| `class_axis_A_eff` | 1727 | 1727 | 1 | YES |
| `class_axis_A_eff_lagged` | 1662 | 1662 | 1 | YES |
| `class_axis_A_eff_lagged_lcera` | 1431 | 1431 | 1 | YES |
| `class_axis_B_step` | 1727 | 1727 | 1 | YES |
| `class_axis_B_step_lagged` | 1662 | 1662 | 1 | YES |
| `class_axis_B_step_lagged_lcera` | 1431 | 1431 | 1 | YES |
| `class_axis_C_maxhr` | 1727 | 1727 | 1 | YES |
| `class_axis_C_maxhr_lagged` | 1662 | 1662 | 1 | YES |
| `class_axis_C_maxhr_lagged_lcera` | 1431 | 1431 | 1 | YES |
| `class_axis_D_vig` | 1727 | 1727 | 1 | YES |
| `class_axis_D_vig_lagged` | 1662 | 1662 | 1 | YES |
| `class_axis_D_vig_lagged_lcera` | 1431 | 1431 | 1 | YES |
| `cog_load` | 0 | 0 | 0 | no |
| `crash_episode_id` | 0 | 0 | 0 | no |
| `daily_step_goal` | 1726 | 1726 | 2 | YES |
| `date` | 1727 | 1727 | 1 | YES |
| `day_dominant_polarity` | 242 | 120 | 20 | no |
| `day_of_week` | 1727 | 1727 | 1 | YES |
| `dip_type` | 0 | 0 | 0 | no |
| `dose_plasma_mg` | 1727 | 1727 | 1 | YES |
| `dossier_event_categories` | 0 | 0 | 0 | no |
| `dossier_event_labels` | 0 | 0 | 0 | no |
| `dossier_event_today` | 1727 | 1727 | 1 | YES |
| `eff_exertion_rank_lagged` | 1662 | 1662 | 1 | YES |
| `eff_exertion_rank_lagged_lcera` | 1431 | 1431 | 1 | YES |
| `effective_exertion_min` | 1727 | 1727 | 1 | YES |
| `effective_exertion_slope_28d` | 1711 | 1711 | 1 | YES |
| `emo_load` | 0 | 0 | 0 | no |
| `era` | 1727 | 1727 | 1 | YES |
| `event_categories` | 1595 | 1187 | 7 | YES |
| `event_labels` | 1595 | 1187 | 7 | YES |
| `exertion_class` | 1727 | 1727 | 1 | YES |
| `exertion_class_lagged` | 1662 | 1662 | 1 | YES |
| `exertion_class_lagged_lcera` | 1431 | 1431 | 1 | YES |
| `exertion_rank_composite_lagged` | 1662 | 1662 | 1 | YES |
| `exertion_rank_composite_lagged_lcera` | 1431 | 1431 | 1 | YES |
| `gevoelscore` | 1349 | 1349 | 1 | YES |
| `has_calendar_coverage` | 1727 | 1727 | 1 | YES |
| `has_garmin_sleep` | 1727 | 1727 | 1 | YES |
| `has_garmin_uds` | 1727 | 1727 | 1 | YES |
| `has_intensity_triage` | 1727 | 1727 | 1 | YES |
| `has_note` | 1727 | 1727 | 1 | YES |
| `has_pwc_dossier_window` | 1727 | 1727 | 1 | YES |
| `has_pwc_log` | 1727 | 1727 | 1 | YES |
| `has_score` | 1727 | 1727 | 1 | YES |
| `highly_active_sec` | 1726 | 1726 | 2 | YES |
| `hr_area_above_daytime_baseline_waking` | 1688 | 1688 | 1 | YES |
| `hr_area_above_daytime_baseline_waking_lcera` | 1457 | 1457 | 1 | YES |
| `hr_daytime_baseline_lagged` | 1688 | 1688 | 1 | YES |
| `hr_daytime_baseline_lagged_lcera` | 1457 | 1457 | 1 | YES |
| `hr_longest_elevated_run_min_waking` | 1688 | 1688 | 1 | YES |
| `hr_longest_elevated_run_min_waking_lcera` | 1457 | 1457 | 1 | YES |
| `hr_median_waking` | 1727 | 1727 | 1 | YES |
| `hr_min_above_daytime_baseline_plus_20_waking` | 1688 | 1688 | 1 | YES |
| `hr_min_above_daytime_baseline_plus_20_waking_lcera` | 1457 | 1457 | 1 | YES |
| `hr_sustained_elevated_flag` | 1688 | 1688 | 1 | YES |
| `hr_sustained_elevated_flag_lcera` | 1457 | 1457 | 1 | YES |
| `in_citalopram_traject` | 1727 | 1727 | 1 | YES |
| `in_naproxen_interventie` | 1727 | 1727 | 1 | YES |
| `in_pwc_reintegratie_2023` | 1727 | 1727 | 1 | YES |
| `in_relational_spanning_2024` | 1727 | 1727 | 1 | YES |
| `in_umbrella` | 1727 | 1727 | 1 | YES |
| `intensity_notes` | 1004 | 277 | 55 | YES |
| `intensity_source` | 1502 | 1427 | 3 | YES |
| `is_crash` | 1727 | 1727 | 1 | YES |
| `is_dip` | 1727 | 1727 | 1 | YES |
| `is_sub_threshold_dip` | 1727 | 1727 | 1 | YES |
| `is_vigorous_day` | 882 | 882 | 2 | YES |
| `lc_phase` | 1727 | 1727 | 1 | YES |
| `max_avg_hr_uds` | 1726 | 1726 | 2 | YES |
| `max_hr` | 1726 | 1726 | 2 | YES |
| `max_hr_rank_lagged` | 1661 | 1661 | 2 | YES |
| `max_hr_rank_lagged_lcera` | 1426 | 1426 | 2 | YES |
| `max_spike_minutes` | 1727 | 1727 | 1 | YES |
| `min_hr` | 1726 | 1726 | 2 | YES |
| `moderate_min` | 1726 | 1726 | 2 | YES |
| `n_clauses` | 242 | 120 | 20 | no |
| `n_events_on_day` | 1727 | 1727 | 1 | YES |
| `n_minutes_resp_above_18` | 1727 | 1727 | 1 | YES |
| `n_minutes_resp_in_rest_band_10_18` | 1727 | 1727 | 1 | YES |
| `n_mixed_clauses` | 242 | 120 | 20 | no |
| `n_neg_clauses` | 242 | 120 | 20 | no |
| `n_neutral_clauses` | 242 | 120 | 20 | no |
| `n_pos_clauses` | 242 | 120 | 20 | no |
| `neutral_forward_looking_flag` | 242 | 120 | 20 | no |
| `note_text` | 242 | 120 | 20 | no |
| `phy_load` | 0 | 0 | 0 | no |
| `push_burden_7d_lagged` | 1727 | 1727 | 1 | YES |
| `push_burden_7d_lagged_lcera` | 1727 | 1727 | 1 | YES |
| `pwc_amsterdam_flag` | 0 | 0 | 0 | no |
| `pwc_doctor_visit_flag` | 0 | 0 | 0 | no |
| `pwc_illness_flag` | 0 | 0 | 0 | no |
| `pwc_primary_hours` | 0 | 0 | 0 | no |
| `pwc_secondary_hours` | 0 | 0 | 0 | no |
| `pwc_toelichting` | 0 | 0 | 0 | no |
| `pwc_total_hours` | 0 | 0 | 0 | no |
| `pwc_vacation_flag` | 0 | 0 | 0 | no |
| `recovery_phase` | 1727 | 1727 | 1 | YES |
| `respiration_avg_sleep` | 1702 | 1368 | 4 | YES |
| `respiration_avg_sleep_lagged_lcera_z` | 299 | 236 | 6 | no |
| `respiration_avg_waking` | 1726 | 1726 | 2 | YES |
| `respiration_max_24h` | 1726 | 1726 | 2 | YES |
| `respiration_max_sleep` | 1702 | 1368 | 4 | YES |
| `respiration_min_24h` | 1726 | 1726 | 2 | YES |
| `respiration_min_sleep` | 1702 | 1368 | 4 | YES |
| `resting_hr` | 1726 | 1726 | 2 | YES |
| `resting_hr_lagged_lcera_z` | 1278 | 400 | 12 | YES |
| `sleep_awake_min` | 1702 | 1368 | 4 | YES |
| `sleep_deep_min` | 1702 | 1368 | 4 | YES |
| `sleep_duration_min` | 1702 | 1368 | 4 | YES |
| `sleep_end_gmt` | 1726 | 1726 | 2 | YES |
| `sleep_light_min` | 1702 | 1368 | 4 | YES |
| `sleep_start_afternoon_flag` | 1702 | 1368 | 4 | YES |
| `sleep_start_gmt` | 1726 | 1726 | 2 | YES |
| `sleep_unmeasurable_min` | 1702 | 1368 | 4 | YES |
| `sleep_valid_flag` | 1727 | 1727 | 1 | YES |
| `spo2_avg_24h` | 1674 | 1367 | 6 | YES |
| `spo2_avg_sleep` | 1358 | 293 | 68 | YES |
| `spo2_min_24h` | 1674 | 1367 | 6 | YES |
| `spo2_min_sleep` | 1358 | 293 | 68 | YES |
| `state_symptoom_cognitief` | 0 | 0 | 0 | no |
| `state_symptoom_emotioneel` | 0 | 0 | 0 | no |
| `state_symptoom_fysiek` | 20 | 15 | 6 | no |
| `step_rank_lagged` | 1661 | 1661 | 2 | YES |
| `step_rank_lagged_lcera` | 1426 | 1426 | 2 | YES |
| `step_z_30d` | 1711 | 1711 | 2 | YES |
| `steps_above_goal_flag` | 1726 | 1726 | 2 | YES |
| `stress_high_duration_min` | 1727 | 1727 | 1 | YES |
| `stress_low_motion_min_count_S50_Mbelow_mod` | 1727 | 1727 | 1 | YES |
| `stress_low_motion_min_count_S50_Mlow` | 1727 | 1727 | 1 | YES |
| `stress_low_motion_min_count_S50_Mstrict` | 1727 | 1727 | 1 | YES |
| `stress_low_motion_min_count_S60_Mbelow_mod` | 1727 | 1727 | 1 | YES |
| `stress_low_motion_min_count_S60_Mlow` | 1727 | 1727 | 1 | YES |
| `stress_low_motion_min_count_S60_Mstrict` | 1727 | 1727 | 1 | YES |
| `stress_low_motion_min_count_S75_Mbelow_mod` | 1727 | 1727 | 1 | YES |
| `stress_low_motion_min_count_S75_Mlow` | 1727 | 1727 | 1 | YES |
| `stress_low_motion_min_count_S75_Mstrict` | 1727 | 1727 | 1 | YES |
| `stress_mean_sleep` | 1702 | 1368 | 4 | YES |
| `stress_mean_sleep_lagged_lcera_z` | 1441 | 1368 | 4 | YES |
| `stress_post_peak_drop_avg` | 1718 | 1370 | 3 | YES |
| `stress_post_peak_time_to_rest_min` | 1375 | 284 | 41 | YES |
| `stress_recovery_pct_within_2h` | 1441 | 503 | 33 | YES |
| `stress_stdev_sleep` | 1702 | 1368 | 4 | YES |
| `total_calories` | 1726 | 1726 | 2 | YES |
| `total_steps` | 1726 | 1726 | 2 | YES |
| `u_dip_count` | 1727 | 1727 | 1 | YES |
| `umbrella_labels` | 1016 | 765 | 3 | YES |
| `vigorous_min` | 1726 | 1726 | 2 | YES |
| `vigorous_min_rank_lagged` | 1662 | 1662 | 1 | YES |
| `vigorous_min_rank_lagged_lcera` | 1431 | 1431 | 1 | YES |

---

## 5. Stage 4 -- per-recovery-phase coverage summary

Per-channel coverage % per recovery phase (6 phases per [`lc_recovery_phase_axis.md` sec 2](../../../../methodology/lc_recovery_phase_axis.md)). Cell format: `pct (n_avail/n_total)`.

| channel | pre_illness_healthy | acute_infection | lc_pre_ergo | pacing_pre_citalopram_learning | pacing_habit_established | citalopram_modulated |
|---|---|---|---|---|---|---|
| `above_baseline_streak` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `active_sec` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (778/787) |
| `all_day_stress_avg` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `all_day_stress_avg_lagged_lcera_z` | 0% (0/217) | 0% (0/14) | 75% (128/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `all_day_stress_max` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `asleep_stress_avg_uds` | 100% (216/217) | 100% (14/14) | 94% (160/171) | 95% (53/56) | 100% (508/509) | 98% (771/787) |
| `awake_stress_avg` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `awake_stress_max` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `bb_charged_24h` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `bb_drained_24h` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `bb_during_sleep_value` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 22% (110/509) | 95% (751/787) |
| `bb_highest` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `bb_lowest` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `bb_lowest_lagged_lcera_z` | 0% (0/217) | 0% (0/14) | 64% (109/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `bb_overnight_gain` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 0% (0/509) | 75% (593/787) |
| `bb_overnight_gain_best` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 0% (0/509) | 85% (667/787) |
| `bb_overnight_gain_lagged_lcera_z` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 0% (0/509) | 72% (563/787) |
| `bb_overnight_gain_proxy` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 0% (0/509) | 85% (667/787) |
| `bb_overnight_gain_source` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 0% (0/509) | 85% (667/787) |
| `bb_sleep_end_value` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 0% (0/509) | 75% (593/787) |
| `bb_sleep_start_value` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 0% (0/509) | 85% (667/787) |
| `bedtime_hour_local` | 99% (215/217) | 100% (14/14) | 92% (158/171) | 95% (53/56) | 98% (500/509) | 97% (767/787) |
| `bedtime_std_7d` | 99% (214/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `bout_max_peak_height_day` | 0% (0/217) | 0% (0/14) | 92% (157/171) | 95% (53/56) | 99% (505/509) | 97% (764/787) |
| `bout_n_did_not_return` | 0% (0/217) | 0% (0/14) | 93% (159/171) | 95% (53/56) | 99% (506/509) | 98% (768/787) |
| `bout_n_fast_recovery_day` | 0% (0/217) | 0% (0/14) | 93% (159/171) | 95% (53/56) | 99% (506/509) | 98% (768/787) |
| `bout_n_per_day` | 0% (0/217) | 0% (0/14) | 93% (159/171) | 95% (53/56) | 99% (506/509) | 98% (768/787) |
| `bout_total_AUC_day` | 0% (0/217) | 0% (0/14) | 93% (159/171) | 95% (53/56) | 99% (506/509) | 97% (765/787) |
| `cat_belasting_cognitief` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_belasting_emotioneel` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_belasting_fysiek` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_belasting_gezin` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_belasting_sociaal` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_context_neutraal` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_medicatie` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_recovery_actie` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_sub_gastro` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_sub_hoofdpijn` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_sub_huid` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_sub_keel_resp` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_sub_koorts` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_sub_neuro` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_sub_overig` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_sub_slaap` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_sub_spier` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_sub_systemisch_vermoeid` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_symptoom_cognitief` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_symptoom_emotioneel` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_symptoom_fysiek` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `cat_triggers_extern` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `class_axis_A_eff` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_A_eff_lagged` | 68% (147/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_A_eff_lagged_lcera` | 0% (0/217) | 0% (0/14) | 59% (101/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_B_step` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_B_step_lagged` | 68% (147/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_B_step_lagged_lcera` | 0% (0/217) | 0% (0/14) | 59% (101/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_C_maxhr` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_C_maxhr_lagged` | 68% (147/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_C_maxhr_lagged_lcera` | 0% (0/217) | 0% (0/14) | 59% (101/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_D_vig` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_D_vig_lagged` | 68% (147/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `class_axis_D_vig_lagged_lcera` | 0% (0/217) | 0% (0/14) | 59% (101/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `cog_load` | 0% (0/217) | 21% (3/14) | 3% (5/171) | 11% (6/56) | 27% (137/509) | 26% (206/787) |
| `crash_episode_id` | 0% (0/217) | 0% (0/14) | 5% (9/171) | 12% (7/56) | 19% (99/509) | 9% (67/787) |
| `daily_step_goal` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (778/787) |
| `date` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `day_dominant_polarity` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `day_of_week` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `dip_type` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 2% (1/56) | 1% (6/509) | 4% (28/787) |
| `dose_plasma_mg` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `dossier_event_categories` | 0% (0/217) | 43% (6/14) | 1% (2/171) | 2% (1/56) | 12% (59/509) | 0% (0/787) |
| `dossier_event_labels` | 0% (0/217) | 43% (6/14) | 1% (2/171) | 2% (1/56) | 12% (59/509) | 0% (0/787) |
| `dossier_event_today` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `eff_exertion_rank_lagged` | 68% (147/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `eff_exertion_rank_lagged_lcera` | 0% (0/217) | 0% (0/14) | 59% (101/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `effective_exertion_min` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `effective_exertion_slope_28d` | 90% (196/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `emo_load` | 0% (0/217) | 0% (0/14) | 1% (1/171) | 4% (2/56) | 10% (49/509) | 14% (113/787) |
| `era` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `event_categories` | 100% (217/217) | 100% (14/14) | 65% (112/171) | 100% (56/56) | 97% (496/509) | 100% (787/787) |
| `event_labels` | 100% (217/217) | 100% (14/14) | 65% (112/171) | 100% (56/56) | 97% (496/509) | 100% (787/787) |
| `exertion_class` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `exertion_class_lagged` | 68% (147/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `exertion_class_lagged_lcera` | 0% (0/217) | 0% (0/14) | 59% (101/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `exertion_rank_composite_lagged` | 68% (147/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `exertion_rank_composite_lagged_lcera` | 0% (0/217) | 0% (0/14) | 59% (101/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `gevoelscore` | 0% (0/217) | 0% (0/14) | 11% (19/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `has_calendar_coverage` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `has_garmin_sleep` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `has_garmin_uds` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `has_intensity_triage` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `has_note` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `has_pwc_dossier_window` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `has_pwc_log` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `has_score` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `highly_active_sec` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (778/787) |
| `hr_area_above_daytime_baseline_waking` | 80% (173/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `hr_area_above_daytime_baseline_waking_lcera` | 0% (0/217) | 0% (0/14) | 69% (118/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `hr_daytime_baseline_lagged` | 80% (173/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `hr_daytime_baseline_lagged_lcera` | 0% (0/217) | 0% (0/14) | 69% (118/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `hr_longest_elevated_run_min_waking` | 80% (173/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `hr_longest_elevated_run_min_waking_lcera` | 0% (0/217) | 0% (0/14) | 69% (118/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `hr_median_waking` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (507/509) | 99% (777/787) |
| `hr_min_above_daytime_baseline_plus_20_waking` | 80% (173/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `hr_min_above_daytime_baseline_plus_20_waking_lcera` | 0% (0/217) | 0% (0/14) | 69% (118/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `hr_sustained_elevated_flag` | 80% (173/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `hr_sustained_elevated_flag_lcera` | 0% (0/217) | 0% (0/14) | 69% (118/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `in_citalopram_traject` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `in_naproxen_interventie` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `in_pwc_reintegratie_2023` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `in_relational_spanning_2024` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `in_umbrella` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `intensity_notes` | 36% (79/217) | 93% (13/14) | 63% (107/171) | 93% (52/56) | 85% (432/509) | 84% (659/787) |
| `intensity_source` | 36% (79/217) | 93% (13/14) | 65% (112/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `is_crash` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `is_dip` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `is_sub_threshold_dip` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `is_vigorous_day` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 23% (118/509) | 99% (778/787) |
| `lc_phase` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `max_avg_hr_uds` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `max_hr` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `max_hr_rank_lagged` | 68% (147/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `max_hr_rank_lagged_lcera` | 0% (0/217) | 0% (0/14) | 54% (92/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `max_spike_minutes` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `min_hr` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `moderate_min` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (778/787) |
| `n_clauses` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `n_events_on_day` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `n_minutes_resp_above_18` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `n_minutes_resp_in_rest_band_10_18` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `n_mixed_clauses` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `n_neg_clauses` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `n_neutral_clauses` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `n_pos_clauses` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `neutral_forward_looking_flag` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `note_text` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 25% (14/56) | 48% (244/509) | 54% (427/787) |
| `phy_load` | 0% (0/217) | 21% (3/14) | 2% (4/171) | 5% (3/56) | 20% (103/509) | 21% (165/787) |
| `push_burden_7d_lagged` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `push_burden_7d_lagged_lcera` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `pwc_amsterdam_flag` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 66% (37/56) | 40% (202/509) | 0% (0/787) |
| `pwc_doctor_visit_flag` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 66% (37/56) | 40% (202/509) | 0% (0/787) |
| `pwc_illness_flag` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 66% (37/56) | 40% (202/509) | 0% (0/787) |
| `pwc_primary_hours` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 66% (37/56) | 39% (200/509) | 0% (0/787) |
| `pwc_secondary_hours` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 6% (32/509) | 0% (0/787) |
| `pwc_toelichting` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 61% (34/56) | 37% (189/509) | 0% (0/787) |
| `pwc_total_hours` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 66% (37/56) | 40% (202/509) | 0% (0/787) |
| `pwc_vacation_flag` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 66% (37/56) | 40% (202/509) | 0% (0/787) |
| `recovery_phase` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `respiration_avg_sleep` | 99% (215/217) | 100% (14/14) | 93% (159/171) | 95% (53/56) | 98% (500/509) | 97% (763/787) |
| `respiration_avg_sleep_lagged_lcera_z` | 0% (0/217) | 0% (0/14) | 16% (28/171) | 0% (0/56) | 10% (49/509) | 42% (327/787) |
| `respiration_avg_waking` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `respiration_max_24h` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `respiration_max_sleep` | 99% (215/217) | 100% (14/14) | 93% (159/171) | 95% (53/56) | 98% (500/509) | 97% (763/787) |
| `respiration_min_24h` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (778/787) |
| `respiration_min_sleep` | 99% (215/217) | 100% (14/14) | 93% (159/171) | 95% (53/56) | 98% (500/509) | 97% (763/787) |
| `resting_hr` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (776/787) |
| `resting_hr_lagged_lcera_z` | 0% (0/217) | 0% (0/14) | 74% (127/171) | 95% (53/56) | 96% (490/509) | 89% (699/787) |
| `sleep_awake_min` | 100% (216/217) | 100% (14/14) | 94% (160/171) | 95% (53/56) | 99% (504/509) | 97% (766/787) |
| `sleep_deep_min` | 100% (216/217) | 100% (14/14) | 94% (160/171) | 95% (53/56) | 99% (504/509) | 97% (766/787) |
| `sleep_duration_min` | 99% (215/217) | 100% (14/14) | 92% (158/171) | 95% (53/56) | 98% (500/509) | 97% (767/787) |
| `sleep_end_gmt` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (778/787) |
| `sleep_light_min` | 100% (216/217) | 100% (14/14) | 94% (160/171) | 95% (53/56) | 99% (504/509) | 97% (766/787) |
| `sleep_start_afternoon_flag` | 99% (215/217) | 100% (14/14) | 92% (158/171) | 95% (53/56) | 98% (500/509) | 97% (767/787) |
| `sleep_start_gmt` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (778/787) |
| `sleep_unmeasurable_min` | 100% (216/217) | 100% (14/14) | 94% (160/171) | 95% (53/56) | 99% (504/509) | 97% (766/787) |
| `sleep_valid_flag` | 100% (217/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `spo2_avg_24h` | 100% (217/217) | 100% (14/14) | 88% (150/171) | 91% (51/56) | 98% (500/509) | 96% (756/787) |
| `spo2_avg_sleep` | 98% (213/217) | 100% (14/14) | 80% (137/171) | 82% (46/56) | 88% (450/509) | 84% (660/787) |
| `spo2_min_24h` | 100% (217/217) | 100% (14/14) | 88% (150/171) | 91% (51/56) | 98% (500/509) | 96% (756/787) |
| `spo2_min_sleep` | 98% (213/217) | 100% (14/14) | 80% (137/171) | 82% (46/56) | 88% (450/509) | 84% (660/787) |
| `state_symptoom_cognitief` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 3% (17/509) | 4% (28/787) |
| `state_symptoom_emotioneel` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 0% (1/509) | 0% (1/787) |
| `state_symptoom_fysiek` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 23% (13/56) | 36% (184/509) | 35% (279/787) |
| `step_rank_lagged` | 68% (147/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (776/787) |
| `step_rank_lagged_lcera` | 0% (0/217) | 0% (0/14) | 54% (92/171) | 96% (54/56) | 100% (509/509) | 99% (776/787) |
| `step_z_30d` | 91% (197/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (776/787) |
| `steps_above_goal_flag` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (776/787) |
| `stress_high_duration_min` | 100% (216/217) | 100% (14/14) | 95% (162/171) | 95% (53/56) | 100% (509/509) | 99% (783/787) |
| `stress_low_motion_min_count_S50_Mbelow_mod` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `stress_low_motion_min_count_S50_Mlow` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `stress_low_motion_min_count_S50_Mstrict` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `stress_low_motion_min_count_S60_Mbelow_mod` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `stress_low_motion_min_count_S60_Mlow` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `stress_low_motion_min_count_S60_Mstrict` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `stress_low_motion_min_count_S75_Mbelow_mod` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `stress_low_motion_min_count_S75_Mlow` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `stress_low_motion_min_count_S75_Mstrict` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `stress_mean_sleep` | 99% (215/217) | 100% (14/14) | 92% (158/171) | 95% (53/56) | 98% (500/509) | 97% (767/787) |
| `stress_mean_sleep_lagged_lcera_z` | 0% (0/217) | 0% (0/14) | 73% (125/171) | 95% (53/56) | 98% (500/509) | 97% (767/787) |
| `stress_post_peak_drop_avg` | 98% (212/217) | 93% (13/14) | 94% (160/171) | 95% (53/56) | 99% (504/509) | 99% (779/787) |
| `stress_post_peak_time_to_rest_min` | 89% (193/217) | 93% (13/14) | 78% (133/171) | 88% (49/56) | 83% (421/509) | 91% (713/787) |
| `stress_recovery_pct_within_2h` | 78% (170/217) | 93% (13/14) | 85% (146/171) | 79% (44/56) | 88% (447/509) | 90% (706/787) |
| `stress_stdev_sleep` | 99% (215/217) | 100% (14/14) | 92% (158/171) | 95% (53/56) | 98% (500/509) | 97% (767/787) |
| `total_calories` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (778/787) |
| `total_steps` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (776/787) |
| `u_dip_count` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (783/787) |
| `umbrella_labels` | 0% (0/217) | 0% (0/14) | 0% (0/171) | 0% (0/56) | 53% (268/509) | 100% (787/787) |
| `vigorous_min` | 100% (217/217) | 100% (14/14) | 95% (162/171) | 96% (54/56) | 100% (509/509) | 99% (778/787) |
| `vigorous_min_rank_lagged` | 68% (147/217) | 100% (14/14) | 100% (171/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |
| `vigorous_min_rank_lagged_lcera` | 0% (0/217) | 0% (0/14) | 59% (101/171) | 100% (56/56) | 100% (509/509) | 100% (787/787) |

Recovery_arc v2 phase definitions cited; per the axis MD sec 5.4 + sec 3.4a, the pre-illness healthy baseline is ~13 months (217 days); the acute_infection phase is 14 days; the pacing_pre_citalopram_learning sub-phase 4a is 56 days (tight-n caveat); the pacing_habit_established sub-phase 4b is ~508 days; citalopram_modulated phase 5 is ~787 days. Per the README [trajectory/recovery_arc/findings.md](../recovery_arc/findings.md) v2 LANDED 2026-06-22, the bb_overnight_gain channel has data ONLY in phase 5 of the 6 phases (5/6 phases empty); gevoelscore has data ONLY in phases 3 (partial, last 19 days) + 4a + 4b + 5 (phases 1+2 entirely empty by construction).

---

## 6. Stage 5 -- missingness pattern characterisation

### 6.1 Gap statistics

Per-channel gap statistics computed within first-to-last-available window. Gap = consecutive NaN run. The full per-channel gap-length distribution lives in [`summary.json`](summary.json) (gitignored); the headline visualisation is at [`plots/missingness_diagnostic.png`](plots/missingness_diagnostic.png) (gitignored).

### 6.2 MCAR/MAR diagnostic

**Method choice** (documented per handoff sec 2 choice 4 'agent picks defensible method + documents choice'): Welch-style chi-square aggregation on per-channel missingness patterns. For each channel C, the test compares the mean of every OTHER numeric channel between rows where C is missing vs observed; sums chi-square contributions over informative comparison channels; tests against chi-square distribution with dof = # informative comparisons. Significance threshold alpha = 0.05.

**Rationale**: Little's original MCAR test (Little 1988) assumes multivariate Gaussian; our channel mix is integer + continuous + ordinal + bool, so a non-parametric Welch-style variant is more defensible. The chi-square aggregation captures the same intuition (missingness depends on other variables) without assuming Gaussianity. Limitations: skip-criterion (n_observed >= 30 AND n_missing >= 30 AND >= 10 obs per comparison channel) suppresses verdicts on always-populated channels (correct) and on very-sparse channels (also correct, but reduces coverage of the diagnostic).

**Verdict counts** (across all enumerated channels):
- `reject_MCAR` (89 channels): missingness depends on other channels (i.e. MAR or MNAR; descriptive flag only).
- `fail_to_reject_MCAR` (0 channels): no evidence the missingness depends on other channels at alpha = 0.05.
- `skipped_insufficient_n` (45) + `skipped_no_informative_comparison_channels` (0): test could not run.
- `no_test` (67): non-numeric channel (string / categorical / bool); skipped by design.

**Critical disclaimer per CONVENTIONS sec 3.3**: these are DESCRIPTIVE infrastructure observations; they do NOT pre-commit any specific HA pre-reg to an MCAR/MAR/MNAR assumption on any specific channel. HA pre-regs do their own MAR-vs-MNAR reasoning per their specific question. The MCAR/MAR diagnostic here is a starting point for HA-pre-reg authors to investigate further, not a verdict.

### 6.3 MNAR-suspect channels (descriptive flag only)

Heuristic flags channels where: (a) first-available date is >30 days later than the DATA_DICTIONARY-documented start, OR (b) the 28d rolling coverage has >4 inflection points (signal goes in and out repeatedly). These are descriptive flags ONLY; not a verdict on any specific HA's missingness assumption.

| channel | reasons |
|---|---|
| `bout_max_peak_height_day` | rolling_coverage_unstable:7_inflections |
| `bout_n_did_not_return` | rolling_coverage_unstable:5_inflections |
| `bout_n_fast_recovery_day` | first_available_later_than_documented:231d; rolling_coverage_unstable:5_inflections |
| `bout_n_per_day` | rolling_coverage_unstable:5_inflections |
| `bout_total_AUC_day` | rolling_coverage_unstable:5_inflections |
| `cat_belasting_cognitief` | rolling_coverage_unstable:20_inflections |
| `cat_belasting_emotioneel` | rolling_coverage_unstable:20_inflections |
| `cat_belasting_fysiek` | rolling_coverage_unstable:20_inflections |
| `cat_belasting_gezin` | rolling_coverage_unstable:20_inflections |
| `cat_belasting_sociaal` | rolling_coverage_unstable:20_inflections |
| `cat_context_neutraal` | rolling_coverage_unstable:20_inflections |
| `cat_medicatie` | rolling_coverage_unstable:20_inflections |
| `cat_recovery_actie` | rolling_coverage_unstable:20_inflections |
| `cat_sub_gastro` | rolling_coverage_unstable:20_inflections |
| `cat_sub_hoofdpijn` | rolling_coverage_unstable:20_inflections |
| `cat_sub_huid` | rolling_coverage_unstable:20_inflections |
| `cat_sub_keel_resp` | rolling_coverage_unstable:20_inflections |
| `cat_sub_koorts` | rolling_coverage_unstable:20_inflections |
| `cat_sub_neuro` | rolling_coverage_unstable:20_inflections |
| `cat_sub_overig` | rolling_coverage_unstable:20_inflections |
| `cat_sub_slaap` | rolling_coverage_unstable:20_inflections |
| `cat_sub_spier` | rolling_coverage_unstable:20_inflections |
| `cat_sub_systemisch_vermoeid` | rolling_coverage_unstable:20_inflections |
| `cat_symptoom_cognitief` | rolling_coverage_unstable:20_inflections |
| `cat_symptoom_emotioneel` | rolling_coverage_unstable:20_inflections |
| `cat_symptoom_fysiek` | rolling_coverage_unstable:20_inflections |
| `cat_triggers_extern` | rolling_coverage_unstable:20_inflections |
| `day_dominant_polarity` | rolling_coverage_unstable:20_inflections |
| `event_categories` | rolling_coverage_unstable:7_inflections |
| `event_labels` | rolling_coverage_unstable:7_inflections |
| `exertion_class_lagged` | first_available_later_than_documented:70d |
| `hr_daytime_baseline_lagged` | first_available_later_than_documented:44d |
| `intensity_notes` | rolling_coverage_unstable:55_inflections |
| `n_clauses` | rolling_coverage_unstable:20_inflections |
| `n_mixed_clauses` | rolling_coverage_unstable:20_inflections |
| `n_neg_clauses` | rolling_coverage_unstable:20_inflections |
| `n_neutral_clauses` | rolling_coverage_unstable:20_inflections |
| `n_pos_clauses` | rolling_coverage_unstable:20_inflections |
| `neutral_forward_looking_flag` | rolling_coverage_unstable:20_inflections |
| `note_text` | first_available_later_than_documented:45d; rolling_coverage_unstable:20_inflections |
| `respiration_avg_sleep_lagged_lcera_z` | rolling_coverage_unstable:6_inflections |
| `resting_hr_lagged_lcera_z` | rolling_coverage_unstable:12_inflections |
| `spo2_avg_24h` | rolling_coverage_unstable:6_inflections |
| `spo2_avg_sleep` | rolling_coverage_unstable:68_inflections |
| `spo2_min_24h` | rolling_coverage_unstable:6_inflections |
| `spo2_min_sleep` | rolling_coverage_unstable:68_inflections |
| `state_symptoom_fysiek` | rolling_coverage_unstable:6_inflections |
| `stress_post_peak_time_to_rest_min` | rolling_coverage_unstable:41_inflections |
| `stress_recovery_pct_within_2h` | rolling_coverage_unstable:33_inflections |

---

## 7. Stage 6 -- output artefacts

Three artefacts emitted per descriptive README sec 4.6 + handoff sec 3.2 Stage 6 expectations:

1. **Coverage timeline chart** -- [`plots/coverage_timeline.png`](plots/coverage_timeline.png) (gitignored). Channel x date heatmap; green = non-NaN; white = NaN; rows grouped by family; phase boundaries shaded.
2. **Per-recovery-phase coverage summary table** -- [`plots/per_phase_coverage_heatmap.png`](plots/per_phase_coverage_heatmap.png) (gitignored) + markdown table in Section 5 above.
3. **Missingness diagnostic report** -- [`plots/missingness_diagnostic.png`](plots/missingness_diagnostic.png) (gitignored). 3-panel: gap-length distribution per channel + MCAR verdict counts + MNAR-suspect channels.

---

## 8. Pipeline-vs-documentation drift findings

Per [[feedback_flag_contradictions]] discipline + extending Q3.8 push_burden_7d finding across all enumerated columns. Drift = either column absent from master despite DATA_DICTIONARY entry, or first-available date drifts >30 days from documented start.

**Found 7 channels with drift** (full table below). Notably:

- `push_burden_7d` (un-lagged v3.1) is absent from master per audit MD 2026-06-11 item 2 (rolling-baseline contamination drop); CONVENTIONS sec 3.2 still says it stays in master. This is the Q3.8 [push_burden_7d/findings.md](../../operationalisation_support/push_burden_7d/findings.md) finding that motivated extending the pattern.
- Several documented columns may be absent from master entirely OR first-available may not match the DATA_DICTIONARY-claimed start date.
- The bb_overnight_gain truth/proxy/best/source 4-channel audit trail per [`bb_overnight_gain_proxy.md`](../../../../methodology/bb_overnight_gain_proxy.md) is fully present and reflects the 2-stage UDS rollout.

Full drift listing (all detected):

| channel | observed | documented | delta or note |
|---|---|---|---|
| `note_text` | first 2022-10-18 | doc 2022-09-03 | delta +45 days |
| `push_burden_7d` | absent from master | doc: 2021-08-16 | DROPPED from master per audit MD 2026-06-11 item 2 (rolling-baseline contamination); v3.2 _lagged variant present. |
| `exertion_class_lagged` | first 2021-10-25 | doc 2021-08-16 | delta +70 days |
| `bb_overnight_gain_lagged_lcera_z` | first 2024-10-22 | doc 2024-12-17 | delta -56 days |
| `dose_plasma_mg` | first 2021-08-16 | doc 2024-04-09 | delta -967 days |
| `hr_daytime_baseline_lagged` | first 2021-09-29 | doc 2021-08-16 | delta +44 days |
| `bout_n_fast_recovery_day` | first 2022-04-04 | doc 2021-08-16 | delta +231 days |

**Honest framing per CONVENTIONS sec 4.2 caveats discipline**: this drift listing is the descriptive infrastructure-mapping complement to any future stocktake refresh effort. NOT a verdict on whether the documentation is wrong vs the pipeline; surfaced for follow-up.

---

## 9. Cross-references load-bearing

Per handoff sec 3.3:

- **DATA_DICTIONARY column-level documentation** ([`docs/research/DATA_DICTIONARY.md`](../../../../DATA_DICTIONARY.md)) -- column-family enumeration source; pipeline-vs-doc drift evaluated against this source.
- **`bb_overnight_gain_proxy.md` coverage bridge** ([`methodology/bb_overnight_gain_proxy.md`](../../../../methodology/bb_overnight_gain_proxy.md)) -- LOAD-BEARING: bb_overnight_gain truth coverage starts 2024-09-18; proxy bridges 2024-07-08 -> 2024-09-17 (71 days) + 3 post-rollout SLEEPEND-failure nights (74 days net). The 4-channel audit trail (truth, proxy, best, source) inherits to downstream HA pre-regs per the proxy MD sec 4.1 discipline rules.
- **`stress_low_motion_primitive.md` Session E lock** ([`methodology/stress_low_motion_primitive.md`](../../../../methodology/stress_low_motion_primitive.md)) -- stress_low_motion family coverage 99.1% raw + 1722 valid days post the ≥600-sample gate. Coverage characterisation in Section 5 + Section 6 reflects this lock.
- **`garmin_indicators_audit.md` known-issues catalog** ([`methodology/garmin_indicators_audit.md`](../../../../methodology/garmin_indicators_audit.md)) -- cross-referenced per-channel for known issues (calibration drift, sensor failures, primitive rule changes). The audit MD's 2026-06-11 item 2 push_burden_7d drop motivates Section 8's drift extension across all columns. HRV hardware-blocked on FR245 noted (B1-B5 + HRV-dependent H-block tests blocked).
- **`lc_recovery_phase_axis.md` 6-phase definitions** ([`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md)) -- per-phase summary table (Section 5) uses the 6-phase axis verbatim; per axis MD sec 5.4 the pre-illness healthy baseline is 217 days; recovery_arc v2 cited for the 5/6-empty bb_overnight_gain + phases 1+2-empty gevoelscore precedents.
- **`lc_era_temporal_segmentation.md` Stratum 4 boundary** ([`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md)) -- Stratum 4 starts 2022-09-03; outcome-side coverage anchor.
- **`recovery_arc` v2 findings cross-reference** ([`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md)) -- v2 LANDED 2026-06-22; phase-coverage cross-references inherit the 6-phase axis + the bb_overnight_gain / gevoelscore coverage gaps explicitly named there.
- **`push_burden_7d/findings.md` Q3.8 drift precedent** ([`operationalisation_support/push_burden_7d/findings.md`](../../operationalisation_support/push_burden_7d/findings.md)) -- the CONVENTIONS sec 3.2 / audit MD contradiction surfaced there is reproduced + extended across all columns in Section 8.
- **`bb_overnight_gain/findings.md` Q3.5 coverage-discipline precedent** ([`operationalisation_support/bb_overnight_gain/findings.md`](../../operationalisation_support/bb_overnight_gain/findings.md)) -- truth-only window analytic discipline carried forward.
- **CONVENTIONS** ([`CONVENTIONS.md`](../../../../CONVENTIONS.md)): sec 2.1 (descriptive-before-inference); sec 3.2 (lagged-baseline discipline / where Q3.8 drift entered); sec 3.3 (no pre-commitment of MCAR/MAR readings for HAs not yet pre-spec'd; binding on the Stage 5 verdict scope); sec 4.1-4.4 (no interpretive marks; caveats vs a-priori; prior-driven hypotheses are confirmatory).

---

## 10. Limitations

1. **No substantive HA verdict promotion**: this analysis is Layer 1 descriptive infrastructure-mapping ONLY (per CONVENTIONS sec 2.1 + sec 4.1); any future HA pre-reg that cites this analysis must apply its own missingness reasoning per its specific question.
2. **MCAR/MAR diagnostic is descriptive** (per CONVENTIONS sec 3.3); it does NOT pre-commit any HA pre-reg's missingness assumption. The diagnostic flags reject_MCAR vs fail_to_reject_MCAR across channels for HA-pre-reg authors' investigation.
3. **Welch-style chi-square is a non-parametric variant** of Little 1988; assumes informative-comparison channels carry mean differences but not necessarily covariance differences. The documented choice is defensible for the mixed-dtype master.
4. **MNAR-suspect heuristic** is a descriptive flag (>30-day first-available drift OR >4 rolling inflections); not a verdict. Many flagged channels have legitimate sensor-rollout reasons (e.g. bb_sleep_end_value 2024-09-18) that are documented in DATA_DICTIONARY and not actually MNAR.
5. **Stable-epoch threshold = 28d rolling >= 80%** (user-locked choice 2); other thresholds may yield different inflection counts; the threshold choice is documented.
6. **Per-recovery-phase per-channel n** can be very small for phases 2 + 4a (14 + 56 days respectively); coverage percentages in those phases are honest but noisier than long-phase cells.

*Generated programmatically by [`run.py`](run.py) from [`summary.json`](summary.json) (gitignored per `docs/research/**/*.json`). To refresh: ``python run.py``.*
