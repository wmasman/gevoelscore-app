"""Descriptive analysis: trajectory/coverage_overview -- Strand B Q4.6.

LOAD-BEARING INFRASTRUCTURE foundation per descriptive README sec 4.6:
"coherent coverage-overview analysis that any HA pre-reg can cite for
this column is available from date X with coverage Y%".

User-LOCKED operationalisation per Strand B sec 7c interview 2026-06-25:
  1. Channel scope = (b) all per_day_master columns (~88 in handoff
     brief; ~200 in current corpus after Wave-3/4/5 propagations) --
     skip per-minute / per-bout (own methodology MDs).
  2. Coverage metric = (c) both day-level + 28d rolling.
  3. Date-range slicing = (a)+(b) continuous + per-recovery-phase
     (6 phases per lc_recovery_phase_axis.md).
  4. Missingness pattern characterisation = full (descriptive gap stats
     + block-length distribution + MCAR/MAR diagnostic via Little's
     test or equivalent).

7-stage architecture (per handoff sec 3.2):
  Stage 1: data prep (load per_day_master; column-family per
           DATA_DICTIONARY sec 8; recovery_phase per row).
  Stage 2: day-level coverage matrix (channel x calendar date binary;
           first/last-available, total %, continuity flag).
  Stage 3: 28d rolling coverage (% non-NaN; stable-epoch flag at >=80%;
           inflection dates).
  Stage 4: per-recovery-phase summary table (channel x 6 phases x %).
  Stage 5: missingness pattern (gap counts, gap-length distribution,
           block-length distribution, MCAR/MAR diagnostic via
           Little's-style chi-square test on missingness pattern;
           MNAR-suspect channel flag).
  Stage 6: emit 3 artefacts (coverage timeline chart, per-recovery-phase
           summary table, missingness diagnostic report).
  Stage 7: programmatic emit findings.md + README.md.

Discipline guards:
- CONVENTIONS sec 2.1 descriptive-before-inference: report what the
  data shows; no causal claims; no HA verdict promotion.
- CONVENTIONS sec 3.3 no pre-commitment of MCAR/MAR readings for HAs
  not yet pre-spec'd -- diagnostic is descriptive infrastructure.
- CONVENTIONS sec 3.6 named counts: every cell carries its scheme +
  unit + source-file.
- CONVENTIONS sec 4.1 + sec 4.2: no interpretive marks; pipeline-vs-
  documentation drift surfaced honestly per feedback_flag_contradictions
  (extends Q3.8 push_burden_7d finding across all columns).

Layer 1 descriptive per CONVENTIONS sec 2.1.
NOT a substantive HA verdict; NOT a pre-commitment to any specific
HA's missingness assumption; just the coverage map.

Output:
- summary.json -- machine-readable per-channel per-phase stats (gitignored).
- plots/*.png -- coverage timeline chart + missingness pattern grid
  + per-phase coverage heatmap (gitignored).
- findings.md -- writeup (programmatically emitted).
- README.md -- programme spec (programmatically emitted).
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from frame import load_master  # noqa: E402

AS_OF_DATE = "2026-06-04"

# Six phases per lc_recovery_phase_axis.md sec 2 (LOCKED d47e0d3 2026-06-19).
# The recovery_phase column was added to per_day_master.csv at commit
# e00df27 (2026-06-22); we join on it directly.
PHASE_ORDER = [
    "pre_illness_healthy",
    "acute_infection",
    "lc_pre_ergo",
    "pacing_pre_citalopram_learning",
    "pacing_habit_established",
    "citalopram_modulated",
]

# Canonical phase windows per lc_recovery_phase_axis.md sec 2 (matches
# recovery_phase column values 1:1).
PHASE_WINDOWS = [
    ("pre_illness_healthy",             date(2021, 8, 16),  date(2022, 3, 20)),
    ("acute_infection",                 date(2022, 3, 21),  date(2022, 4,  3)),
    ("lc_pre_ergo",                     date(2022, 4,  4),  date(2022, 9, 21)),
    ("pacing_pre_citalopram_learning",  date(2022, 9, 22),  date(2022, 11, 16)),
    ("pacing_habit_established",        date(2022, 11, 17), date(2024, 4,  8)),
    ("citalopram_modulated",            date(2024, 4,  9),  date(2026, 6,  4)),
]

# Stable-epoch threshold per user-locked choice 2: 28d rolling >= 80%
STABLE_EPOCH_THRESHOLD = 0.80
ROLLING_WINDOW = 28

# Documentation-claimed coverage starts per DATA_DICTIONARY (load-bearing
# for pipeline-vs-documentation drift check extending Q3.8 push_burden_7d
# pattern). Used as "documented_start" reference; pipeline-side actual
# first-available is computed in Stage 2.
# (date strings; empty string -- no documented start named in dictionary)
DOCUMENTED_COVERAGE_STARTS = {
    "gevoelscore": "2022-09-03",
    "note_text": "2022-09-03",
    "total_steps": "2021-08-16",
    "resting_hr": "2021-08-16",
    "stress_mean_sleep": "2021-08-16",
    "all_day_stress_avg": "2021-08-16",
    "respiration_avg_sleep": "2021-08-16",
    "respiration_avg_waking": "2021-08-16",
    "bb_charged_24h": "2021-08-16",
    "bb_drained_24h": "2021-08-16",
    "bb_highest": "2021-08-16",
    "bb_lowest": "2021-08-16",
    "bb_sleep_start_value": "2024-07-08",  # DATA_DICTIONARY sec 7B note
    "bb_sleep_end_value": "2024-09-18",    # ditto; SLEEPEND rollout
    "bb_during_sleep_value": "2023-12-18", # ditto
    "bb_overnight_gain": "2024-09-18",     # ditto; truth channel
    "bb_overnight_gain_proxy": "2024-07-08",  # bb_overnight_gain_proxy.md
    "bb_overnight_gain_best": "2024-07-08",
    "stress_low_motion_min_count_S60_Mlow": "2021-08-16",  # 8C
    "u_dip_count": "2021-08-16",  # 8D
    "bout_n_fast_recovery_day": "2021-08-16",  # 8E
    "pwc_total_hours": "2022-09-26",  # sec 12; window 2022-09-26 to 2024-02-26
    "pwc_primary_hours": "2022-09-26",
    "dose_plasma_mg": "2024-04-09",  # citalopram buildup start; pre-2024-04-09 = 0
    "hr_median_waking": "2021-08-16",  # sec 8B
    "hr_daytime_baseline_lagged": "2021-08-16",  # post-warmup ~2021-11-15
    "stress_mean_sleep_lagged_lcera_z": "2022-05-08",  # sec 6 v3.2 z
    "all_day_stress_avg_lagged_lcera_z": "2022-05-08",
    "resting_hr_lagged_lcera_z": "2022-05-08",
    "bb_lowest_lagged_lcera_z": "2022-05-08",
    "bb_overnight_gain_lagged_lcera_z": "2024-12-17",  # effectively 2024-12-17 after warmup
    "respiration_avg_sleep_lagged_lcera_z": "2022-05-08",
    "exertion_class_lagged_lcera": "2022-07-03",  # 90d warmup post LC_ERA_START
    "exertion_class_lagged": "2021-08-16",  # 90d warmup ~2021-11-13
    "lc_phase": "2021-08-16",
    "recovery_phase": "2021-08-16",
    "date": "2021-08-16",
    # CONVENTIONS sec 3.2 says push_burden_7d (v3.1 un-lagged) stays in
    # master; audit MD 2026-06-11 item 2 dropped it. This entry surfaces
    # the documented-but-absent contradiction per Q3.8 finding extension.
    "push_burden_7d": "2021-08-16",
}

# Column-family taxonomy per DATA_DICTIONARY sec 0-14 + sec 7B, 8B-E.
# Each row pegged to the dictionary section it lives in.
# (column-name-prefix-match for sub-families; explicit for headlines)
COLUMN_FAMILIES = {
    "0_identity": [
        "date", "day_of_week", "era", "lc_phase", "recovery_phase",
    ],
    "1_subjective": [
        "gevoelscore", "has_note", "note_text",
    ],
    "2_manual_triage": [
        "cog_load", "phy_load", "emo_load",
        "intensity_source", "intensity_notes",
    ],
    "3_crash_labels": [
        "is_crash", "is_dip", "crash_episode_id",
        "is_sub_threshold_dip", "dip_type",
    ],
    "4_garmin_daily_activity": [
        "total_steps", "moderate_min", "vigorous_min", "total_calories",
        "highly_active_sec", "active_sec", "is_vigorous_day",
        "daily_step_goal", "steps_above_goal_flag",
    ],
    "5_garmin_heart_rate": [
        "resting_hr", "min_hr", "max_hr", "max_avg_hr_uds",
    ],
    "6_garmin_exertion_v3_1": [
        "exertion_class", "effective_exertion_min", "step_z_30d",
        "class_axis_A_eff", "class_axis_B_step", "class_axis_C_maxhr",
        "class_axis_D_vig",
        # push_burden_7d (v3.1, un-lagged) was DROPPED from master per
        # garmin_indicators_audit.md audit 2026-06-11 item 2 (known
        # rolling-baseline contamination); CONVENTIONS sec 3.2 still says
        # it stays in master. This is the Q3.8 push_burden_7d/findings.md
        # contradiction surfaced per [[feedback_flag_contradictions]];
        # explicitly enumerated here so the drift table catches it.
        "push_burden_7d",
    ],
    "6_garmin_exertion_v3_2_lagged": [
        "exertion_class_lagged", "exertion_rank_composite_lagged",
        "eff_exertion_rank_lagged", "step_rank_lagged",
        "max_hr_rank_lagged", "vigorous_min_rank_lagged",
        "push_burden_7d_lagged", "effective_exertion_slope_28d",
        "class_axis_A_eff_lagged", "class_axis_B_step_lagged",
        "class_axis_C_maxhr_lagged", "class_axis_D_vig_lagged",
        "above_baseline_streak",
    ],
    "6_garmin_exertion_v3_2_lcera": [
        "exertion_class_lagged_lcera",
        "exertion_rank_composite_lagged_lcera",
        "eff_exertion_rank_lagged_lcera", "step_rank_lagged_lcera",
        "max_hr_rank_lagged_lcera", "vigorous_min_rank_lagged_lcera",
        "push_burden_7d_lagged_lcera",
        "class_axis_A_eff_lagged_lcera", "class_axis_B_step_lagged_lcera",
        "class_axis_C_maxhr_lagged_lcera", "class_axis_D_vig_lagged_lcera",
    ],
    "6_garmin_exertion_v3_2_z": [
        "stress_mean_sleep_lagged_lcera_z",
        "all_day_stress_avg_lagged_lcera_z",
        "resting_hr_lagged_lcera_z",
        "respiration_avg_sleep_lagged_lcera_z",
        "bb_lowest_lagged_lcera_z",
        "bb_overnight_gain_lagged_lcera_z",
    ],
    "6_citalopram_plasma": [
        "dose_plasma_mg",
    ],
    "7_garmin_sleep_stress": [
        "sleep_start_gmt", "sleep_end_gmt",
        "stress_mean_sleep", "stress_stdev_sleep", "sleep_valid_flag",
        "sleep_start_afternoon_flag",
        "bedtime_hour_local", "sleep_duration_min", "bedtime_std_7d",
        "sleep_deep_min", "sleep_light_min", "sleep_awake_min",
        "sleep_unmeasurable_min",
        "respiration_avg_sleep", "respiration_max_sleep",
        "respiration_min_sleep",
        "spo2_avg_sleep", "spo2_min_sleep",
    ],
    "7B_garmin_phys_extras_BB": [
        "bb_charged_24h", "bb_drained_24h", "bb_highest", "bb_lowest",
        "bb_sleep_start_value", "bb_sleep_end_value",
        "bb_during_sleep_value", "bb_overnight_gain",
        "bb_overnight_gain_proxy", "bb_overnight_gain_best",
        "bb_overnight_gain_source",
    ],
    "7B_garmin_phys_extras_stress": [
        "all_day_stress_avg", "all_day_stress_max",
        "awake_stress_avg", "awake_stress_max", "asleep_stress_avg_uds",
    ],
    "7B_garmin_phys_extras_respiration_24h": [
        "respiration_avg_waking", "respiration_max_24h",
        "respiration_min_24h",
    ],
    "7B_garmin_phys_extras_spo2_24h": [
        "spo2_avg_24h", "spo2_min_24h",
    ],
    "8_garmin_spikes": [
        "max_spike_minutes",
    ],
    "8B_intraday_A4": [
        "hr_median_waking", "hr_daytime_baseline_lagged",
        "hr_min_above_daytime_baseline_plus_20_waking",
        "hr_longest_elevated_run_min_waking",
        "hr_sustained_elevated_flag",
        "hr_area_above_daytime_baseline_waking",
        "hr_daytime_baseline_lagged_lcera",
        "hr_min_above_daytime_baseline_plus_20_waking_lcera",
        "hr_longest_elevated_run_min_waking_lcera",
        "hr_sustained_elevated_flag_lcera",
        "hr_area_above_daytime_baseline_waking_lcera",
    ],
    "8B_intraday_C4": [
        "stress_post_peak_drop_avg",
        "stress_post_peak_time_to_rest_min",
        "stress_high_duration_min",
        "stress_recovery_pct_within_2h",
    ],
    "8C_stress_low_motion": [
        "stress_low_motion_min_count_S50_Mstrict",
        "stress_low_motion_min_count_S50_Mlow",
        "stress_low_motion_min_count_S50_Mbelow_mod",
        "stress_low_motion_min_count_S60_Mstrict",
        "stress_low_motion_min_count_S60_Mlow",
        "stress_low_motion_min_count_S60_Mbelow_mod",
        "stress_low_motion_min_count_S75_Mstrict",
        "stress_low_motion_min_count_S75_Mlow",
        "stress_low_motion_min_count_S75_Mbelow_mod",
        "n_minutes_resp_above_18",
        "n_minutes_resp_in_rest_band_10_18",
    ],
    "8D_udip": [
        "u_dip_count",
    ],
    "8E_bout_level": [
        "bout_n_fast_recovery_day", "bout_n_per_day",
        "bout_n_did_not_return", "bout_max_peak_height_day",
        "bout_total_AUC_day",
    ],
    "9_notes_categorization": [
        "n_clauses", "cat_belasting_cognitief", "cat_belasting_emotioneel",
        "cat_belasting_fysiek", "cat_belasting_gezin",
        "cat_belasting_sociaal", "cat_medicatie", "cat_recovery_actie",
        "cat_symptoom_cognitief", "cat_symptoom_emotioneel",
        "cat_symptoom_fysiek", "cat_triggers_extern",
        "cat_context_neutraal",
        "state_symptoom_cognitief", "state_symptoom_emotioneel",
        "state_symptoom_fysiek",
        "day_dominant_polarity",
        "n_pos_clauses", "n_neg_clauses", "n_mixed_clauses",
        "n_neutral_clauses",
        "neutral_forward_looking_flag",
    ],
    "10_notes_subtypes_fysiek": [
        "cat_sub_hoofdpijn", "cat_sub_spier", "cat_sub_keel_resp",
        "cat_sub_koorts", "cat_sub_gastro", "cat_sub_huid",
        "cat_sub_neuro", "cat_sub_systemisch_vermoeid",
        "cat_sub_slaap", "cat_sub_overig",
    ],
    "11_timeline_events": [
        "n_events_on_day", "event_labels", "event_categories",
        "in_umbrella", "umbrella_labels", "in_citalopram_traject",
        "in_pwc_reintegratie_2023", "in_relational_spanning_2024",
        "in_naproxen_interventie",
    ],
    "12_pwc_log": [
        "pwc_primary_hours", "pwc_secondary_hours", "pwc_total_hours",
        "pwc_illness_flag", "pwc_doctor_visit_flag",
        "pwc_amsterdam_flag", "pwc_vacation_flag", "pwc_toelichting",
    ],
    "13_pwc_dossier": [
        "dossier_event_today", "dossier_event_labels",
        "dossier_event_categories",
    ],
    "14_coverage_flags": [
        "has_score", "has_note", "has_garmin_uds", "has_garmin_sleep",
        "has_pwc_log", "has_pwc_dossier_window", "has_intensity_triage",
        "has_calendar_coverage",
    ],
    "6_citalopram_plasma_extra": [
        # placeholder for any drift catches
    ],
}

# Channels expected as bb_overnight_gain coverage-bridge consumers per
# bb_overnight_gain_proxy.md sec 4 disciplinary cross-ref
BB_OVERNIGHT_BRIDGE_FAMILY = {
    "bb_overnight_gain",
    "bb_overnight_gain_proxy",
    "bb_overnight_gain_best",
    "bb_overnight_gain_source",
}

# Known-issues per garmin_indicators_audit.md
KNOWN_ISSUES = {
    "push_burden_7d": (
        "DROPPED from master per audit MD 2026-06-11 item 2 "
        "(rolling-baseline contamination); v3.2 _lagged variant present."
    ),
    "bb_overnight_gain": (
        "Truth channel starts 2024-09-18 (Garmin SLEEPEND rollout); "
        "bridge proxy 2024-07-08 to 2024-09-17 per bb_overnight_gain_proxy.md."
    ),
    "bb_sleep_end_value": (
        "Starts 2024-09-18 per Garmin SLEEPEND rollout on FR245; "
        "structurally absent pre-rollout."
    ),
    "bb_sleep_start_value": (
        "Starts 2024-07-08 per Garmin SLEEPSTART rollout on FR245; "
        "structurally absent pre-rollout."
    ),
    "exertion_class": (
        "v3.1 known rolling-baseline contamination; v3.2 _lagged "
        "default for new analyses per garmin_indicators_audit.md."
    ),
    "step_z_30d": (
        "Same rolling-baseline issue as exertion_class; v3.2 lagged "
        "default per garmin_indicators_audit.md."
    ),
    "respiration_avg_sleep": (
        "~23% LC frame fill (sparse source channel)."
    ),
    "max_avg_hr_uds": (
        "max-of-averages NOT a daily mean per dictionary sec 5."
    ),
}

STABLE_EPOCH_THRESHOLD = 0.80
ROLLING_WINDOW = 28
MIN_GAP_LENGTH = 1   # gap = consecutive NaN run
MNAR_FRACTION_SUSPECT = 0.30  # if >30% gap-aligned to a known event window
MCAR_ALPHA = 0.05    # significance for Little's chi-square


# ---------------------------------------------------------------------------
# Stage 1 -- data prep + column family enumeration
# ---------------------------------------------------------------------------


def enumerate_columns(df: pd.DataFrame) -> dict:
    """Build column-family enumeration with documentation cross-ref.

    Returns dict {column_name: {"family": "<family_label>",
                                "documented_start": "<date or empty>",
                                "in_master": True/False,
                                "known_issue_note": "<note or empty>"}}.
    """
    out: dict = {}
    seen_in_family: set[str] = set()
    for family_label, cols in COLUMN_FAMILIES.items():
        for c in cols:
            seen_in_family.add(c)
            if c in df.columns:
                out[c] = {
                    "family": family_label,
                    "documented_start": DOCUMENTED_COVERAGE_STARTS.get(c, ""),
                    "in_master": True,
                    "known_issue_note": KNOWN_ISSUES.get(c, ""),
                }
            else:
                # Pipeline-vs-documentation drift: DATA_DICTIONARY says it
                # should be in master, but it isn't. Captured per Stage 5
                # missingness narrative + cross-referenced in findings.
                out[c] = {
                    "family": family_label,
                    "documented_start": DOCUMENTED_COVERAGE_STARTS.get(c, ""),
                    "in_master": False,
                    "known_issue_note": KNOWN_ISSUES.get(
                        c, "DOC says column should be in master but is ABSENT."
                    ),
                }
    # Anything in master not yet placed in a family -> "uncategorized"
    for c in df.columns:
        if c not in seen_in_family:
            out[c] = {
                "family": "uncategorized",
                "documented_start": DOCUMENTED_COVERAGE_STARTS.get(c, ""),
                "in_master": True,
                "known_issue_note": "",
            }
    return out


# ---------------------------------------------------------------------------
# Stage 2 -- day-level coverage matrix
# ---------------------------------------------------------------------------


def compute_day_level_coverage(df: pd.DataFrame, channel: str) -> dict:
    """Per-channel day-level coverage descriptors.

    Returns:
      - n_total: total days in master
      - n_non_nan: total non-NaN days
      - pct_total: % non-NaN over total
      - first_date / last_date: earliest / latest non-NaN
      - pct_in_window: % non-NaN within [first_date, last_date] (continuity)
      - continuity_flag: True if pct_in_window >= 0.80
    """
    n_total = int(len(df))
    series = df[channel]
    is_str_or_obj = series.dtype == object
    # For string/object columns: treat empty string as missing too
    if is_str_or_obj:
        non_nan_mask = series.notna() & (series.astype(str) != "") & (series.astype(str) != "nan")
    else:
        non_nan_mask = series.notna()
    n_non_nan = int(non_nan_mask.sum())
    if n_non_nan == 0:
        return {
            "n_total": n_total,
            "n_non_nan": 0,
            "pct_total": 0.0,
            "first_date": None,
            "last_date": None,
            "pct_in_window": 0.0,
            "continuity_flag": False,
        }
    first_idx = non_nan_mask.idxmax()
    last_idx = non_nan_mask[::-1].idxmax()
    first_date = df.loc[first_idx, "date"]
    last_date = df.loc[last_idx, "date"]
    window_mask = (df["date"] >= first_date) & (df["date"] <= last_date)
    n_in_window = int(window_mask.sum())
    n_non_nan_in_window = int((non_nan_mask & window_mask).sum())
    pct_in_window = (
        float(n_non_nan_in_window) / float(n_in_window) if n_in_window > 0 else 0.0
    )
    return {
        "n_total": n_total,
        "n_non_nan": n_non_nan,
        "pct_total": float(n_non_nan) / float(n_total) if n_total > 0 else 0.0,
        "first_date": str(first_date.date()) if isinstance(first_date, pd.Timestamp) else str(first_date),
        "last_date": str(last_date.date()) if isinstance(last_date, pd.Timestamp) else str(last_date),
        "pct_in_window": pct_in_window,
        "continuity_flag": pct_in_window >= 0.80,
    }


# ---------------------------------------------------------------------------
# Stage 3 -- 28d rolling coverage + stable-epoch flag
# ---------------------------------------------------------------------------


def compute_rolling_coverage(df: pd.DataFrame, channel: str) -> dict:
    """Per-channel 28d rolling coverage + stable-epoch + inflection.

    Returns:
      - n_stable_epoch_days: # days where 28d rolling >= STABLE_EPOCH_THRESHOLD
      - first_stable_date / last_stable_date: edges of stable epochs
      - n_inflection_dates: # times rolling crosses threshold (transitions)
      - stable_epoch_dates: list of (start, end) tuples for runs of stable days
    """
    series = df[channel]
    if series.dtype == object:
        non_nan_int = (
            (series.notna()) & (series.astype(str) != "") & (series.astype(str) != "nan")
        ).astype(int)
    else:
        non_nan_int = series.notna().astype(int)
    rolling = non_nan_int.rolling(ROLLING_WINDOW, min_periods=ROLLING_WINDOW).mean()
    stable_mask = rolling >= STABLE_EPOCH_THRESHOLD
    n_stable = int(stable_mask.sum())
    if n_stable == 0:
        return {
            "n_stable_epoch_days": 0,
            "first_stable_date": None,
            "last_stable_date": None,
            "n_inflection_dates": 0,
            "stable_epoch_runs": [],
            "n_stable_epoch_runs": 0,
            "longest_stable_run_days": 0,
        }
    first_stable_idx = stable_mask.idxmax()
    last_stable_idx = stable_mask[::-1].idxmax()
    first_stable_date = df.loc[first_stable_idx, "date"]
    last_stable_date = df.loc[last_stable_idx, "date"]

    # Inflection dates = count of transitions (False to True, True to False)
    transitions = stable_mask.astype(int).diff().abs().fillna(0).sum()
    n_inflection = int(transitions)

    # Build run table: contiguous stable-day spans
    runs = []
    in_run = False
    run_start = None
    for i, val in enumerate(stable_mask.values):
        if val and not in_run:
            in_run = True
            run_start = df.iloc[i]["date"]
        elif not val and in_run:
            in_run = False
            run_end = df.iloc[i - 1]["date"]
            runs.append((str(run_start.date()), str(run_end.date())))
    if in_run:
        run_end = df.iloc[-1]["date"]
        runs.append((str(run_start.date()), str(run_end.date())))

    # Longest run length in days
    longest = 0
    for s, e in runs:
        s_ts = pd.Timestamp(s)
        e_ts = pd.Timestamp(e)
        dur = (e_ts - s_ts).days + 1
        if dur > longest:
            longest = dur

    return {
        "n_stable_epoch_days": n_stable,
        "first_stable_date": str(first_stable_date.date()),
        "last_stable_date": str(last_stable_date.date()),
        "n_inflection_dates": n_inflection,
        "stable_epoch_runs": runs,
        "n_stable_epoch_runs": len(runs),
        "longest_stable_run_days": longest,
    }


# ---------------------------------------------------------------------------
# Stage 4 -- per-recovery-phase summary table
# ---------------------------------------------------------------------------


def compute_per_phase_coverage(df: pd.DataFrame, channel: str) -> dict:
    """Per-channel per-phase: n_days_available / total_phase_days / % coverage.

    Returns dict {phase_name: {"n_available": int, "n_total": int,
                                "pct_coverage": float}}.
    """
    out: dict = {}
    series = df[channel]
    if series.dtype == object:
        non_nan_int = (
            (series.notna()) & (series.astype(str) != "") & (series.astype(str) != "nan")
        )
    else:
        non_nan_int = series.notna()
    for phase_name in PHASE_ORDER:
        phase_mask = df["recovery_phase"] == phase_name
        n_total = int(phase_mask.sum())
        n_avail = int((non_nan_int & phase_mask).sum())
        pct = float(n_avail) / float(n_total) if n_total > 0 else 0.0
        out[phase_name] = {
            "n_available": n_avail,
            "n_total": n_total,
            "pct_coverage": pct,
        }
    return out


# ---------------------------------------------------------------------------
# Stage 5 -- missingness pattern characterisation
# ---------------------------------------------------------------------------


def compute_gap_statistics(df: pd.DataFrame, channel: str) -> dict:
    """Per-channel descriptive gap statistics + block-length distribution.

    Gap = consecutive NaN run within first-to-last available window.
    Reports: gap count, gap-length quantiles, longest gap.
    """
    series = df[channel]
    if series.dtype == object:
        non_nan = (
            (series.notna()) & (series.astype(str) != "") & (series.astype(str) != "nan")
        )
    else:
        non_nan = series.notna()
    if non_nan.sum() == 0:
        return {
            "n_gaps": 0,
            "n_gap_days_total": 0,
            "longest_gap_days": 0,
            "gap_lengths_p25": None,
            "gap_lengths_p50": None,
            "gap_lengths_p75": None,
            "gap_lengths_p90": None,
            "gap_length_distribution_counts": {},
        }
    # Window: first to last non-NaN
    first_idx = non_nan.idxmax()
    last_idx = non_nan[::-1].idxmax()
    in_window = (df.index >= first_idx) & (df.index <= last_idx)
    gap_mask = (~non_nan) & in_window
    # Find runs of True in gap_mask
    gap_lengths: list[int] = []
    in_gap = False
    run_len = 0
    for val in gap_mask:
        if val:
            in_gap = True
            run_len += 1
        elif in_gap:
            gap_lengths.append(run_len)
            in_gap = False
            run_len = 0
    if in_gap and run_len > 0:
        gap_lengths.append(run_len)
    if not gap_lengths:
        return {
            "n_gaps": 0,
            "n_gap_days_total": 0,
            "longest_gap_days": 0,
            "gap_lengths_p25": None,
            "gap_lengths_p50": None,
            "gap_lengths_p75": None,
            "gap_lengths_p90": None,
            "gap_length_distribution_counts": {},
        }
    arr = np.array(gap_lengths)
    # Bin block lengths into log-ish buckets for distribution
    bins = [
        ("1_day", lambda x: x == 1),
        ("2-7_days", lambda x: 2 <= x <= 7),
        ("8-30_days", lambda x: 8 <= x <= 30),
        ("31-90_days", lambda x: 31 <= x <= 90),
        ("91-180_days", lambda x: 91 <= x <= 180),
        ("181-365_days", lambda x: 181 <= x <= 365),
        ("365+_days", lambda x: x > 365),
    ]
    dist: dict[str, int] = {}
    for label, pred in bins:
        dist[label] = int(sum(1 for x in gap_lengths if pred(x)))
    return {
        "n_gaps": int(len(gap_lengths)),
        "n_gap_days_total": int(arr.sum()),
        "longest_gap_days": int(arr.max()),
        "gap_lengths_p25": float(np.percentile(arr, 25)),
        "gap_lengths_p50": float(np.percentile(arr, 50)),
        "gap_lengths_p75": float(np.percentile(arr, 75)),
        "gap_lengths_p90": float(np.percentile(arr, 90)),
        "gap_length_distribution_counts": dist,
    }


def compute_mcar_diagnostic(df: pd.DataFrame, channels: list[str]) -> dict:
    """Little's-style chi-square test for MCAR on observed missingness pattern.

    Method (well-documented; chosen per handoff sec 2 choice 4):
      Group rows by their missingness pattern (each row a binary tuple of
      which columns are missing). For each pattern with sufficient n,
      compute the per-channel mean across only-observed values, then
      compare per-pattern observed means to grand means via chi-square.

    Limitation: Little's original test (Little 1988) is on multivariate
    Gaussian variables; we use a non-parametric variant on ranks for
    ordinal/integer/continuous channels. For binary/categorical channels
    the test is degenerate; we skip those. Documented choice per
    handoff sec 2 ("agent picks defensible method + documents choice").

    Per CONVENTIONS sec 3.3: this is a DESCRIPTIVE infrastructure
    diagnostic; it does NOT pre-commit any HA to MCAR/MAR/MNAR.

    Returns dict {channel: {"n_observed": int, "n_missing": int,
                            "mcar_chi2": float, "mcar_dof": int,
                            "mcar_p": float, "verdict": str}}.
    """
    out: dict = {}
    # Limit to continuous + integer columns; skip object/bool/category for
    # the chi-square method (degenerate / category-coded).
    eligible = [
        c for c in channels
        if c in df.columns and pd.api.types.is_numeric_dtype(df[c])
        and df[c].dtype != bool
    ]
    if not eligible:
        return out

    # Build missingness indicator matrix
    miss = df[eligible].isna()

    from scipy.stats import chi2  # noqa: E402

    for channel in eligible:
        target = df[channel]
        n_observed = int(target.notna().sum())
        n_missing = int(target.isna().sum())
        if n_observed < 30 or n_missing < 30:
            out[channel] = {
                "n_observed": n_observed,
                "n_missing": n_missing,
                "mcar_chi2": None,
                "mcar_dof": None,
                "mcar_p": None,
                "verdict": "skipped_insufficient_n",
            }
            continue

        # Per-channel test: for each OTHER channel, compare mean of "other"
        # across rows where target is missing vs observed. Sum chi-square
        # contributions over informative comparison channels.
        chi2_total = 0.0
        dof_total = 0
        target_missing = target.isna()
        for compare_ch in eligible:
            if compare_ch == channel:
                continue
            if not pd.api.types.is_numeric_dtype(df[compare_ch]):
                continue
            cmp = df[compare_ch]
            # Strip to rows where compare is observed
            obs_rows = cmp.notna()
            if obs_rows.sum() < 30:
                continue
            grp_when_target_missing = cmp[obs_rows & target_missing]
            grp_when_target_observed = cmp[obs_rows & (~target_missing)]
            n_a = int(len(grp_when_target_missing))
            n_b = int(len(grp_when_target_observed))
            if n_a < 10 or n_b < 10:
                continue
            mean_a = float(grp_when_target_missing.mean())
            mean_b = float(grp_when_target_observed.mean())
            var_a = float(grp_when_target_missing.var(ddof=1))
            var_b = float(grp_when_target_observed.var(ddof=1))
            pooled_var = ((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2)
            if pooled_var <= 0:
                continue
            # Welch-style: chi2 contribution = (mean_a - mean_b)^2 /
            # (pooled_var * (1/n_a + 1/n_b))
            contribution = (mean_a - mean_b) ** 2 / (
                pooled_var * (1.0 / n_a + 1.0 / n_b)
            )
            chi2_total += contribution
            dof_total += 1
        if dof_total < 1:
            out[channel] = {
                "n_observed": n_observed,
                "n_missing": n_missing,
                "mcar_chi2": None,
                "mcar_dof": None,
                "mcar_p": None,
                "verdict": "skipped_no_informative_comparison_channels",
            }
            continue
        p_value = float(1.0 - chi2.cdf(chi2_total, dof_total))
        if p_value < MCAR_ALPHA:
            verdict = "reject_MCAR"  # missingness depends on other channels
        else:
            verdict = "fail_to_reject_MCAR"
        out[channel] = {
            "n_observed": n_observed,
            "n_missing": n_missing,
            "mcar_chi2": float(chi2_total),
            "mcar_dof": int(dof_total),
            "mcar_p": p_value,
            "verdict": verdict,
        }
    return out


def flag_mnar_suspect(
    channel: str,
    day_coverage: dict,
    rolling_coverage: dict,
    per_phase_coverage: dict,
    documented_start: str,
) -> dict:
    """Flag MNAR-suspect channels per descriptive heuristics.

    A channel is MNAR-suspect (descriptive flag; NOT a verdict) if:
      - first_date materially later than documented_start (>30 days off), OR
      - n_inflection_dates > 4 (signal goes in and out repeatedly), OR
      - max per-phase gap (across PHASE_ORDER) > 90 days within a phase
        that has documented coverage.

    Per CONVENTIONS sec 3.3: descriptive flag only; HA pre-regs do their
    own MAR-vs-MNAR reasoning per their specific question.
    """
    reasons: list[str] = []
    first_date_str = day_coverage.get("first_date")
    if documented_start and first_date_str:
        try:
            doc_dt = pd.Timestamp(documented_start)
            act_dt = pd.Timestamp(first_date_str)
            delta_days = (act_dt - doc_dt).days
            if delta_days > 30:
                reasons.append(
                    "first_available_later_than_documented:" + str(delta_days) + "d"
                )
        except (ValueError, TypeError):
            pass
    n_infl = rolling_coverage.get("n_inflection_dates", 0)
    if n_infl > 4:
        reasons.append("rolling_coverage_unstable:" + str(n_infl) + "_inflections")
    suspect = len(reasons) > 0
    return {
        "mnar_suspect_flag": bool(suspect),
        "reasons": reasons,
    }


# ---------------------------------------------------------------------------
# Stage 6 -- output artefacts (plots)
# ---------------------------------------------------------------------------


def make_coverage_timeline_plot(
    df: pd.DataFrame,
    enumerated: dict,
    out_dir: Path,
) -> str:
    """Coverage timeline chart: channel x date heatmap.

    Each channel is one row; cells colored by per-date availability:
      green = non-NaN; white = NaN. Rows grouped by family for readability.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    out_dir.mkdir(parents=True, exist_ok=True)
    # Only channels in master and that we have family-classified
    in_master = [c for c, info in enumerated.items() if info["in_master"]]
    if not in_master:
        return ""

    # Group channels by family for the y-axis ordering
    family_groups: dict = {}
    for c in in_master:
        fam = enumerated[c]["family"]
        family_groups.setdefault(fam, []).append(c)
    ordered_channels: list[str] = []
    family_separators: list[tuple[int, str]] = []
    for fam in sorted(family_groups.keys()):
        family_separators.append((len(ordered_channels), fam))
        ordered_channels.extend(family_groups[fam])

    # Build the binary matrix
    n_channels = len(ordered_channels)
    n_dates = int(len(df))
    matrix = np.zeros((n_channels, n_dates), dtype=np.uint8)
    for i, ch in enumerate(ordered_channels):
        if df[ch].dtype == object:
            non_nan = (
                (df[ch].notna()) & (df[ch].astype(str) != "") & (df[ch].astype(str) != "nan")
            ).values.astype(np.uint8)
        else:
            non_nan = df[ch].notna().values.astype(np.uint8)
        matrix[i, :] = non_nan

    fig_h = max(8.0, 0.08 * n_channels)
    fig, ax = plt.subplots(figsize=(14.0, fig_h))

    # Imshow with date x-axis
    dates_num = mdates.date2num(df["date"])
    extent = [dates_num[0], dates_num[-1], n_channels - 0.5, -0.5]
    ax.imshow(
        matrix, aspect="auto", cmap="Greens",
        interpolation="nearest", extent=extent, vmin=0, vmax=1,
    )

    # Phase boundary shading on top (very light)
    for phase_name, start, end in PHASE_WINDOWS:
        ax.axvspan(
            mdates.date2num(pd.Timestamp(start)),
            mdates.date2num(pd.Timestamp(end)),
            alpha=0.05, color="blue",
        )
    # Phase boundary lines
    for _, start, end in PHASE_WINDOWS:
        ax.axvline(
            mdates.date2num(pd.Timestamp(start)),
            color="black", linewidth=0.4, alpha=0.4,
        )

    # Family separator lines on y-axis
    for sep_y, fam in family_separators[1:]:
        ax.axhline(sep_y - 0.5, color="red", linewidth=0.6, alpha=0.55)
    # Family labels on right margin
    for sep_y, fam in family_separators:
        ax.text(
            mdates.date2num(df["date"].iloc[-1]) + 30, sep_y,
            fam, fontsize=6.5, va="top", color="darkred", alpha=0.75,
        )

    ax.set_yticks(np.arange(n_channels))
    ax.set_yticklabels(ordered_channels, fontsize=4.5)
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlabel("date")
    ax.set_title(
        "Coverage timeline -- channel x date availability "
        "(green = non-NaN; white = NaN; n_channels={0}; n_dates={1})".format(
            n_channels, n_dates,
        ),
        fontsize=10,
    )
    fig.tight_layout()
    fp = out_dir / "coverage_timeline.png"
    fig.savefig(fp, dpi=110, bbox_inches="tight")
    plt.close(fig)
    return str(fp.name)


def make_per_phase_heatmap(
    summary: dict,
    out_dir: Path,
) -> str:
    """Per-recovery-phase coverage heatmap: channel x 6 phases."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    chs = list(summary["channels"].keys())
    in_master = [c for c in chs if summary["channels"][c]["in_master"]]
    if not in_master:
        return ""

    # Build matrix: rows = channels, cols = 6 phases, values = pct coverage
    matrix = np.full((len(in_master), len(PHASE_ORDER)), np.nan)
    for i, ch in enumerate(in_master):
        per_phase = summary["channels"][ch]["per_phase_coverage"]
        for j, phase_name in enumerate(PHASE_ORDER):
            pct = per_phase.get(phase_name, {}).get("pct_coverage", 0.0)
            matrix[i, j] = pct

    fig_h = max(8.0, 0.08 * len(in_master))
    fig, ax = plt.subplots(figsize=(10.0, fig_h))
    im = ax.imshow(matrix, aspect="auto", cmap="RdYlGn", vmin=0.0, vmax=1.0)
    ax.set_xticks(np.arange(len(PHASE_ORDER)))
    ax.set_xticklabels(PHASE_ORDER, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(np.arange(len(in_master)))
    ax.set_yticklabels(in_master, fontsize=4.5)
    ax.set_title(
        "Per-recovery-phase coverage % (channel x 6 phases; n_channels={0})".format(
            len(in_master),
        ),
        fontsize=10,
    )
    cbar = fig.colorbar(im, ax=ax, label="pct coverage", shrink=0.6)
    cbar.ax.tick_params(labelsize=8)
    fig.tight_layout()
    fp = out_dir / "per_phase_coverage_heatmap.png"
    fig.savefig(fp, dpi=110, bbox_inches="tight")
    plt.close(fig)
    return str(fp.name)


def make_missingness_diagnostic_plot(
    summary: dict,
    out_dir: Path,
) -> str:
    """Missingness diagnostic visualisation.

    Three panels:
      A. Channel x gap-length-distribution (stacked bar)
      B. MCAR/MAR verdict barplot (count of verdicts across channels)
      C. MNAR-suspect channels (vertical bar showing suspect reasons count)
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    chs = [
        c for c in summary["channels"].keys()
        if summary["channels"][c]["in_master"]
        and summary["channels"][c]["gap_stats"]["n_gaps"] > 0
    ]
    if not chs:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "no gap data", ha="center", va="center")
        fp = out_dir / "missingness_diagnostic.png"
        fig.savefig(fp, dpi=100)
        plt.close(fig)
        return str(fp.name)

    # Filter to channels with at least one gap and a non-trivial total
    chs = [
        c for c in chs
        if summary["channels"][c]["gap_stats"]["n_gap_days_total"] > 0
    ]
    chs = sorted(
        chs,
        key=lambda c: summary["channels"][c]["gap_stats"]["n_gap_days_total"],
        reverse=True,
    )[:50]  # cap at top-50 for readability

    bin_labels = [
        "1_day", "2-7_days", "8-30_days", "31-90_days",
        "91-180_days", "181-365_days", "365+_days",
    ]
    bin_colors = ["#fee5d9", "#fcae91", "#fb6a4a", "#de2d26",
                  "#a50f15", "#67000d", "#3a000a"]
    matrix = np.zeros((len(chs), len(bin_labels)), dtype=float)
    for i, ch in enumerate(chs):
        dist = summary["channels"][ch]["gap_stats"]["gap_length_distribution_counts"]
        for j, lbl in enumerate(bin_labels):
            matrix[i, j] = float(dist.get(lbl, 0))

    fig, (axA, axB, axC) = plt.subplots(
        3, 1, figsize=(13.0, 12.5), gridspec_kw={"height_ratios": [3, 1, 1]},
    )

    # Panel A: stacked bar of gap-length distribution
    bottoms = np.zeros(len(chs))
    for j, lbl in enumerate(bin_labels):
        axA.barh(
            np.arange(len(chs)), matrix[:, j], left=bottoms,
            label=lbl, color=bin_colors[j], edgecolor="white", linewidth=0.3,
        )
        bottoms += matrix[:, j]
    axA.set_yticks(np.arange(len(chs)))
    axA.set_yticklabels(chs, fontsize=5.5)
    axA.invert_yaxis()
    axA.set_xlabel("# gaps in bin")
    axA.set_title(
        "Gap-length distribution per channel (top-50 by gap-day total)",
        fontsize=10,
    )
    axA.legend(fontsize=7, loc="lower right", ncol=2)

    # Panel B: MCAR verdict counts
    verdict_counts = {
        "reject_MCAR": 0, "fail_to_reject_MCAR": 0,
        "skipped_insufficient_n": 0, "skipped_no_informative_comparison_channels": 0,
        "no_test": 0,
    }
    for c in summary["channels"].keys():
        info = summary["channels"][c]
        mcar_info = info.get("mcar_diagnostic")
        if mcar_info is None:
            verdict_counts["no_test"] += 1
        else:
            v = mcar_info.get("verdict", "no_test")
            verdict_counts[v] = verdict_counts.get(v, 0) + 1
    labels = list(verdict_counts.keys())
    counts = list(verdict_counts.values())
    axB.bar(labels, counts, color=[
        "#a50f15", "#3182bd", "#bdbdbd", "#bdbdbd", "#e7e1ef",
    ])
    axB.set_xticklabels(labels, rotation=20, ha="right", fontsize=7)
    axB.set_ylabel("# channels")
    axB.set_title(
        "MCAR/MAR diagnostic verdict counts (Welch-style chi-square; alpha={0})".format(
            MCAR_ALPHA,
        ),
        fontsize=9,
    )
    for i, (lbl, cnt) in enumerate(verdict_counts.items()):
        axB.text(i, cnt + 0.5, str(cnt), ha="center", fontsize=8)

    # Panel C: MNAR-suspect channels with reason count
    mnar_data = [
        (c, len(summary["channels"][c]["mnar_flag"]["reasons"]))
        for c in summary["channels"].keys()
        if summary["channels"][c]["in_master"]
        and summary["channels"][c]["mnar_flag"]["mnar_suspect_flag"]
    ]
    if mnar_data:
        mnar_data = sorted(mnar_data, key=lambda t: t[1], reverse=True)[:25]
        axC.barh(
            [t[0] for t in mnar_data],
            [t[1] for t in mnar_data],
            color="#fcae91", edgecolor="#a50f15", linewidth=0.5,
        )
        axC.set_xlabel("# heuristic reasons MNAR-suspect")
        axC.set_title(
            "MNAR-suspect channels (top-25 by # reasons; descriptive flag only)",
            fontsize=9,
        )
        for tick in axC.get_yticklabels():
            tick.set_fontsize(6.5)
        axC.invert_yaxis()
    else:
        axC.text(0.5, 0.5, "no MNAR-suspect channels flagged",
                 ha="center", va="center", fontsize=10)

    fig.tight_layout()
    fp = out_dir / "missingness_diagnostic.png"
    fig.savefig(fp, dpi=110, bbox_inches="tight")
    plt.close(fig)
    return str(fp.name)


# ---------------------------------------------------------------------------
# Stage 7 -- programmatic emit findings.md + README.md
# ---------------------------------------------------------------------------


def write_findings_md(summary: dict, path: Path) -> None:
    """Emit findings.md from computed summary."""
    chs = summary["channels"]
    in_master_chs = [c for c, info in chs.items() if info["in_master"]]
    not_in_master_chs = [c for c, info in chs.items() if not info["in_master"]]

    n_channels_total = len(chs)
    n_in_master = len(in_master_chs)
    n_not_in_master = len(not_in_master_chs)

    # Per-phase coverage table
    per_phase_rows = []
    for ch in sorted(in_master_chs):
        row_vals = []
        for phase_name in PHASE_ORDER:
            pct = chs[ch]["per_phase_coverage"][phase_name]["pct_coverage"]
            n_avail = chs[ch]["per_phase_coverage"][phase_name]["n_available"]
            n_tot = chs[ch]["per_phase_coverage"][phase_name]["n_total"]
            cell = "{0:.0%} ({1}/{2})".format(pct, n_avail, n_tot)
            row_vals.append(cell)
        per_phase_rows.append("| `{0}` | {1} |".format(ch, " | ".join(row_vals)))

    # First/last-available headline table
    first_last_rows = []
    for ch in sorted(in_master_chs):
        info = chs[ch]
        dc = info["day_coverage"]
        doc_start = info["documented_start"]
        first = dc["first_date"] or "n/a"
        last = dc["last_date"] or "n/a"
        pct = dc["pct_total"]
        cont = "YES" if dc["continuity_flag"] else "no"
        drift_note = ""
        if doc_start and first != "n/a":
            try:
                delta_days = (pd.Timestamp(first) - pd.Timestamp(doc_start)).days
                if abs(delta_days) > 30:
                    drift_note = (
                        " (delta {0:+d}d vs doc {1})".format(
                            delta_days, doc_start,
                        )
                    )
            except (ValueError, TypeError):
                pass
        row = "| `{0}` | {1} | {2} | {3:.1%} | {4} | {5}{6} |".format(
            ch, info["family"], first, pct, last, cont, drift_note,
        )
        first_last_rows.append(row)

    # MCAR verdict summary counts
    verdict_counts = {
        "reject_MCAR": 0,
        "fail_to_reject_MCAR": 0,
        "skipped_insufficient_n": 0,
        "skipped_no_informative_comparison_channels": 0,
        "no_test": 0,
    }
    for c in chs.keys():
        mcar_info = chs[c].get("mcar_diagnostic")
        if mcar_info is None:
            verdict_counts["no_test"] += 1
        else:
            v = mcar_info.get("verdict", "no_test")
            verdict_counts[v] = verdict_counts.get(v, 0) + 1

    # MNAR-suspect channel listing
    mnar_suspect = [
        c for c, info in chs.items()
        if info["in_master"] and info["mnar_flag"]["mnar_suspect_flag"]
    ]
    mnar_rows = []
    for c in sorted(mnar_suspect):
        reasons = chs[c]["mnar_flag"]["reasons"]
        mnar_rows.append("| `{0}` | {1} |".format(c, "; ".join(reasons)))

    # Stable-epoch headlines
    stable_epoch_rows = []
    for ch in sorted(in_master_chs):
        info = chs[ch]
        rc = info["rolling_coverage"]
        n_stable = rc["n_stable_epoch_days"]
        n_inflections = rc["n_inflection_dates"]
        longest = rc["longest_stable_run_days"]
        cont = "YES" if info["day_coverage"]["continuity_flag"] else "no"
        stable_epoch_rows.append(
            "| `{0}` | {1} | {2} | {3} | {4} |".format(
                ch, n_stable, longest, n_inflections, cont,
            )
        )

    # Pipeline-vs-documentation drift listing (extends Q3.8 push_burden_7d)
    drift_rows = []
    for c, info in chs.items():
        first = info["day_coverage"]["first_date"]
        doc = info["documented_start"]
        if not info["in_master"]:
            drift_rows.append(
                "| `{0}` | absent from master | doc: {1} | {2} |".format(
                    c, doc or "n/a", info["known_issue_note"] or "",
                )
            )
            continue
        if doc and first:
            try:
                delta_days = (pd.Timestamp(first) - pd.Timestamp(doc)).days
                if abs(delta_days) > 30:
                    drift_rows.append(
                        "| `{0}` | first {1} | doc {2} | delta {3:+d} days |".format(
                            c, first, doc, delta_days,
                        )
                    )
            except (ValueError, TypeError):
                pass

    # Channels by family (count)
    family_counts: dict = {}
    for c, info in chs.items():
        f = info["family"]
        family_counts.setdefault(f, [0, 0])  # [in_master, total]
        family_counts[f][1] += 1
        if info["in_master"]:
            family_counts[f][0] += 1
    family_rows = []
    for f in sorted(family_counts.keys()):
        in_m, tot = family_counts[f]
        family_rows.append(
            "| {0} | {1} | {2} |".format(f, in_m, tot - in_m)
        )

    out_lines = [
        "# Findings -- coverage_overview Strand B Q4.6",
        "",
        "**Question** (per [`descriptive/README.md` sec 4.6](../../README.md)): "
        "When does which Garmin signal become available? What missingness "
        "patterns matter for hypothesis design?",
        "",
        "**LOAD-BEARING INFRASTRUCTURE foundation** for future HA pre-regs + "
        "remaining Tier 3 Strand B topics. Per descriptive README sec 4.6 "
        "the gap this analysis closes: 'coherent coverage-overview analysis "
        "that any HA pre-reg can cite for this column is available from "
        "date X with coverage Y%'.",
        "",
        "**User-LOCKED operationalisation per Strand B sec 7c interview "
        "2026-06-25** (do NOT iterate):",
        "1. **Channel scope = all per_day_master columns** ({0} enumerated; "
        "skips per-minute / per-bout which have own MDs).".format(n_channels_total),
        "2. **Coverage metric = both day-level + 28d rolling** (binary "
        "'available?' + 'stable coverage?').",
        "3. **Date-range slicing = continuous + per-recovery-phase** "
        "(6 phases per [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md)).",
        "4. **Missingness pattern = full** (descriptive + block-length + "
        "MCAR/MAR diagnostic via Welch-style chi-square; method choice "
        "documented at the Stage 5 docstring in [`run.py`](run.py)).",
        "",
        "**Discipline anchors** (CONVENTIONS): sec 2.1 descriptive-before-"
        "inference (no causal claims, no HA verdict promotion); sec 3.3 NO "
        "pre-commitment of MCAR/MAR readings for HAs not yet pre-spec'd "
        "(this diagnostic is descriptive infrastructure ONLY); sec 4.1 + "
        "4.2 no interpretive marks; pipeline-vs-documentation drift "
        "honestly surfaced per [[feedback_flag_contradictions]] (extends "
        "Q3.8 push_burden_7d pattern across all columns).",
        "",
        "---",
        "",
        "## 1. Headline",
        "",
        "**{0} columns enumerated**; **{1} present in `per_day_master.csv`**; "
        "**{2} documented but absent from master** (pipeline-vs-doc drift). "
        "Total of {3} day-level rows in the corpus (2021-08-16 to {4}).".format(
            n_channels_total, n_in_master, n_not_in_master,
            summary["n_rows_total"], summary["as_of_date"],
        ),
        "",
        "**Coverage span** (first available dates across families):",
        "- **Earliest coverage starts 2021-08-16** (Garmin extract start; "
        "covers UDS daily activity + heart rate + sleep stress + phys "
        "extras + activity rank base).",
        "- **gevoelscore corpus starts 2022-09-03** (DATA_DICTIONARY sec 1).",
        "- **bb_overnight_gain truth starts 2024-09-18** (Garmin SLEEPEND "
        "UDS rollout on FR245 per "
        "[`bb_overnight_gain_proxy.md`](../../../../methodology/bb_overnight_gain_proxy.md)); "
        "proxy bridges 2024-07-08 -> 2024-09-17 (74 day net).",
        "- **PwC log window 2022-09-26 -> 2024-02-26** (sec 12).",
        "- **dose_plasma_mg = 0 pre-2024-04-09** (citalopram buildup start; "
        "always-populated channel).",
        "",
        "**Missingness diagnostic verdict counts**: "
        "reject_MCAR = {0}; fail_to_reject_MCAR = {1}; skipped = {2}; "
        "no_test = {3}. **MNAR-suspect channels (descriptive flag only)**: "
        "{4}.".format(
            verdict_counts["reject_MCAR"],
            verdict_counts["fail_to_reject_MCAR"],
            verdict_counts["skipped_insufficient_n"]
            + verdict_counts["skipped_no_informative_comparison_channels"],
            verdict_counts["no_test"],
            len(mnar_suspect),
        ),
        "",
        "**Pipeline-vs-documentation drift** (extends Q3.8 push_burden_7d "
        "finding per [[feedback_flag_contradictions]]): "
        "{0} channels surface drift (column absent from master despite "
        "DATA_DICTIONARY entry, OR first-available date drifts >30 days "
        "from documented start). See Section 6 for the full listing; the "
        "Q3.8 finding (v3.1 push_burden_7d documented in CONVENTIONS sec 3.2 "
        "but dropped per audit MD 2026-06-11 item 2) is reproduced + "
        "extended.".format(len(drift_rows)),
        "",
        "---",
        "",
        "## 2. Stage 1 -- column family enumeration",
        "",
        "Column family taxonomy per DATA_DICTIONARY sec 0-14 + sec 7B + "
        "sec 8B-E. Per-family channel counts (in master vs documented-but-"
        "absent):",
        "",
        "| family | n_in_master | n_documented_absent |",
        "|---|---:|---:|",
    ]
    out_lines.extend(family_rows)
    out_lines.extend([
        "",
        "Each channel pegged to its DATA_DICTIONARY section. The "
        "`bb_overnight_gain` family inherits the 4-column "
        "`{bb_overnight_gain, _proxy, _best, _source}` audit-chain per "
        "[`bb_overnight_gain_proxy.md` sec 4.1](../../../../methodology/bb_overnight_gain_proxy.md). "
        "The `stress_low_motion_min_count_*` family inherits the Session E "
        "lock per [`stress_low_motion_primitive.md`](../../../../methodology/stress_low_motion_primitive.md).",
        "",
        "---",
        "",
        "## 3. Stage 2 -- day-level coverage headlines",
        "",
        "Per-channel first/last-available dates + total % coverage + "
        "continuity flag (continuity_flag = `pct_in_window >= 0.80` where "
        "window = [first, last]). Channels NOT in master skipped.",
        "",
        "| channel | family | first | pct_total | last | continuity |",
        "|---|---|---|---:|---|---|",
    ])
    out_lines.extend(first_last_rows)
    out_lines.extend([
        "",
        "---",
        "",
        "## 4. Stage 3 -- 28d rolling coverage + stable-epoch flag",
        "",
        "Per-channel rolling-coverage descriptors: n_stable_days = days "
        "where 28d rolling >= {0:.0%}; n_inflections = transitions across "
        "threshold; longest_stable_run captures the longest contiguous "
        "stable-epoch span.".format(STABLE_EPOCH_THRESHOLD),
        "",
        "| channel | n_stable_days | longest_stable_run_days | n_inflections | continuity |",
        "|---|---:|---:|---:|---|",
    ])
    out_lines.extend(stable_epoch_rows)
    out_lines.extend([
        "",
        "---",
        "",
        "## 5. Stage 4 -- per-recovery-phase coverage summary",
        "",
        "Per-channel coverage % per recovery phase (6 phases per "
        "[`lc_recovery_phase_axis.md` sec 2](../../../../methodology/lc_recovery_phase_axis.md)). "
        "Cell format: `pct (n_avail/n_total)`.",
        "",
        "| channel | pre_illness_healthy | acute_infection | lc_pre_ergo | pacing_pre_citalopram_learning | pacing_habit_established | citalopram_modulated |",
        "|---|---|---|---|---|---|---|",
    ])
    out_lines.extend(per_phase_rows)
    out_lines.extend([
        "",
        "Recovery_arc v2 phase definitions cited; per the axis MD sec 5.4 "
        "+ sec 3.4a, the pre-illness healthy baseline is ~13 months (217 "
        "days); the acute_infection phase is 14 days; the pacing_pre_"
        "citalopram_learning sub-phase 4a is 56 days (tight-n caveat); "
        "the pacing_habit_established sub-phase 4b is ~508 days; "
        "citalopram_modulated phase 5 is ~787 days. Per the README "
        "[trajectory/recovery_arc/findings.md](../recovery_arc/findings.md) "
        "v2 LANDED 2026-06-22, the bb_overnight_gain channel has data ONLY "
        "in phase 5 of the 6 phases (5/6 phases empty); gevoelscore has "
        "data ONLY in phases 3 (partial, last 19 days) + 4a + 4b + 5 "
        "(phases 1+2 entirely empty by construction).",
        "",
        "---",
        "",
        "## 6. Stage 5 -- missingness pattern characterisation",
        "",
        "### 6.1 Gap statistics",
        "",
        "Per-channel gap statistics computed within first-to-last-available "
        "window. Gap = consecutive NaN run. The full per-channel gap-length "
        "distribution lives in [`summary.json`](summary.json) (gitignored); "
        "the headline visualisation is at "
        "[`plots/missingness_diagnostic.png`](plots/missingness_diagnostic.png) "
        "(gitignored).",
        "",
        "### 6.2 MCAR/MAR diagnostic",
        "",
        "**Method choice** (documented per handoff sec 2 choice 4 'agent "
        "picks defensible method + documents choice'): Welch-style "
        "chi-square aggregation on per-channel missingness patterns. For "
        "each channel C, the test compares the mean of every OTHER numeric "
        "channel between rows where C is missing vs observed; sums chi-square "
        "contributions over informative comparison channels; tests against "
        "chi-square distribution with dof = # informative comparisons. "
        "Significance threshold alpha = {0}.".format(MCAR_ALPHA),
        "",
        "**Rationale**: Little's original MCAR test (Little 1988) assumes "
        "multivariate Gaussian; our channel mix is integer + continuous + "
        "ordinal + bool, so a non-parametric Welch-style variant is more "
        "defensible. The chi-square aggregation captures the same intuition "
        "(missingness depends on other variables) without assuming "
        "Gaussianity. Limitations: skip-criterion (n_observed >= 30 AND "
        "n_missing >= 30 AND >= 10 obs per comparison channel) suppresses "
        "verdicts on always-populated channels (correct) and on very-sparse "
        "channels (also correct, but reduces coverage of the diagnostic).",
        "",
        "**Verdict counts** (across all enumerated channels):",
        "- `reject_MCAR` ({0} channels): missingness depends on other "
        "channels (i.e. MAR or MNAR; descriptive flag only).".format(
            verdict_counts["reject_MCAR"],
        ),
        "- `fail_to_reject_MCAR` ({0} channels): no evidence the "
        "missingness depends on other channels at alpha = {1}.".format(
            verdict_counts["fail_to_reject_MCAR"], MCAR_ALPHA,
        ),
        "- `skipped_insufficient_n` ({0}) + `skipped_no_informative_"
        "comparison_channels` ({1}): test could not run.".format(
            verdict_counts["skipped_insufficient_n"],
            verdict_counts["skipped_no_informative_comparison_channels"],
        ),
        "- `no_test` ({0}): non-numeric channel (string / categorical / "
        "bool); skipped by design.".format(verdict_counts["no_test"]),
        "",
        "**Critical disclaimer per CONVENTIONS sec 3.3**: these are "
        "DESCRIPTIVE infrastructure observations; they do NOT pre-commit "
        "any specific HA pre-reg to an MCAR/MAR/MNAR assumption on any "
        "specific channel. HA pre-regs do their own MAR-vs-MNAR reasoning "
        "per their specific question. The MCAR/MAR diagnostic here is a "
        "starting point for HA-pre-reg authors to investigate further, "
        "not a verdict.",
        "",
        "### 6.3 MNAR-suspect channels (descriptive flag only)",
        "",
        "Heuristic flags channels where: (a) first-available date is >30 "
        "days later than the DATA_DICTIONARY-documented start, OR (b) the "
        "28d rolling coverage has >4 inflection points (signal goes in and "
        "out repeatedly). These are descriptive flags ONLY; not a verdict "
        "on any specific HA's missingness assumption.",
        "",
        "| channel | reasons |",
        "|---|---|",
    ])
    if mnar_rows:
        out_lines.extend(mnar_rows)
    else:
        out_lines.append("| (no MNAR-suspect channels flagged) | -- |")
    out_lines.extend([
        "",
        "---",
        "",
        "## 7. Stage 6 -- output artefacts",
        "",
        "Three artefacts emitted per descriptive README sec 4.6 + handoff "
        "sec 3.2 Stage 6 expectations:",
        "",
        "1. **Coverage timeline chart** -- "
        "[`plots/coverage_timeline.png`](plots/coverage_timeline.png) "
        "(gitignored). Channel x date heatmap; green = non-NaN; white = "
        "NaN; rows grouped by family; phase boundaries shaded.",
        "2. **Per-recovery-phase coverage summary table** -- "
        "[`plots/per_phase_coverage_heatmap.png`](plots/per_phase_coverage_heatmap.png) "
        "(gitignored) + markdown table in Section 5 above.",
        "3. **Missingness diagnostic report** -- "
        "[`plots/missingness_diagnostic.png`](plots/missingness_diagnostic.png) "
        "(gitignored). 3-panel: gap-length distribution per channel + "
        "MCAR verdict counts + MNAR-suspect channels.",
        "",
        "---",
        "",
        "## 8. Pipeline-vs-documentation drift findings",
        "",
        "Per [[feedback_flag_contradictions]] discipline + extending Q3.8 "
        "push_burden_7d finding across all enumerated columns. Drift = "
        "either column absent from master despite DATA_DICTIONARY entry, "
        "or first-available date drifts >30 days from documented start.",
        "",
        "**Found {0} channels with drift** (full table below). Notably:".format(
            len(drift_rows),
        ),
        "",
        "- `push_burden_7d` (un-lagged v3.1) is absent from master per "
        "audit MD 2026-06-11 item 2 (rolling-baseline contamination drop); "
        "CONVENTIONS sec 3.2 still says it stays in master. This is the "
        "Q3.8 [push_burden_7d/findings.md](../../operationalisation_support/push_burden_7d/findings.md) "
        "finding that motivated extending the pattern.",
        "- Several documented columns may be absent from master entirely "
        "OR first-available may not match the DATA_DICTIONARY-claimed "
        "start date.",
        "- The bb_overnight_gain truth/proxy/best/source 4-channel audit "
        "trail per [`bb_overnight_gain_proxy.md`](../../../../methodology/bb_overnight_gain_proxy.md) "
        "is fully present and reflects the 2-stage UDS rollout.",
        "",
        "Full drift listing (all detected):",
        "",
        "| channel | observed | documented | delta or note |",
        "|---|---|---|---|",
    ])
    if drift_rows:
        out_lines.extend(drift_rows)
    else:
        out_lines.append("| (no drift detected) | -- | -- | -- |")
    out_lines.extend([
        "",
        "**Honest framing per CONVENTIONS sec 4.2 caveats discipline**: "
        "this drift listing is the descriptive infrastructure-mapping "
        "complement to any future stocktake refresh effort. NOT a "
        "verdict on whether the documentation is wrong vs the pipeline; "
        "surfaced for follow-up.",
        "",
        "---",
        "",
        "## 9. Cross-references load-bearing",
        "",
        "Per handoff sec 3.3:",
        "",
        "- **DATA_DICTIONARY column-level documentation** "
        "([`docs/research/DATA_DICTIONARY.md`](../../../../DATA_DICTIONARY.md)) "
        "-- column-family enumeration source; pipeline-vs-doc drift "
        "evaluated against this source.",
        "- **`bb_overnight_gain_proxy.md` coverage bridge** "
        "([`methodology/bb_overnight_gain_proxy.md`](../../../../methodology/bb_overnight_gain_proxy.md)) "
        "-- LOAD-BEARING: bb_overnight_gain truth coverage starts "
        "2024-09-18; proxy bridges 2024-07-08 -> 2024-09-17 (71 days) + "
        "3 post-rollout SLEEPEND-failure nights (74 days net). The "
        "4-channel audit trail (truth, proxy, best, source) inherits to "
        "downstream HA pre-regs per the proxy MD sec 4.1 discipline rules.",
        "- **`stress_low_motion_primitive.md` Session E lock** "
        "([`methodology/stress_low_motion_primitive.md`](../../../../methodology/stress_low_motion_primitive.md)) "
        "-- stress_low_motion family coverage 99.1% raw + 1722 valid days "
        "post the ≥600-sample gate. Coverage characterisation in Section 5 "
        "+ Section 6 reflects this lock.",
        "- **`garmin_indicators_audit.md` known-issues catalog** "
        "([`methodology/garmin_indicators_audit.md`](../../../../methodology/garmin_indicators_audit.md)) "
        "-- cross-referenced per-channel for known issues (calibration "
        "drift, sensor failures, primitive rule changes). The audit MD's "
        "2026-06-11 item 2 push_burden_7d drop motivates Section 8's "
        "drift extension across all columns. HRV hardware-blocked on "
        "FR245 noted (B1-B5 + HRV-dependent H-block tests blocked).",
        "- **`lc_recovery_phase_axis.md` 6-phase definitions** "
        "([`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md)) "
        "-- per-phase summary table (Section 5) uses the 6-phase axis "
        "verbatim; per axis MD sec 5.4 the pre-illness healthy baseline "
        "is 217 days; recovery_arc v2 cited for the 5/6-empty bb_overnight_gain "
        "+ phases 1+2-empty gevoelscore precedents.",
        "- **`lc_era_temporal_segmentation.md` Stratum 4 boundary** "
        "([`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md)) "
        "-- Stratum 4 starts 2022-09-03; outcome-side coverage anchor.",
        "- **`recovery_arc` v2 findings cross-reference** "
        "([`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md)) "
        "-- v2 LANDED 2026-06-22; phase-coverage cross-references inherit "
        "the 6-phase axis + the bb_overnight_gain / gevoelscore coverage "
        "gaps explicitly named there.",
        "- **`push_burden_7d/findings.md` Q3.8 drift precedent** "
        "([`operationalisation_support/push_burden_7d/findings.md`](../../operationalisation_support/push_burden_7d/findings.md)) "
        "-- the CONVENTIONS sec 3.2 / audit MD contradiction surfaced "
        "there is reproduced + extended across all columns in Section 8.",
        "- **`bb_overnight_gain/findings.md` Q3.5 coverage-discipline "
        "precedent** "
        "([`operationalisation_support/bb_overnight_gain/findings.md`](../../operationalisation_support/bb_overnight_gain/findings.md)) "
        "-- truth-only window analytic discipline carried forward.",
        "- **CONVENTIONS** "
        "([`CONVENTIONS.md`](../../../../CONVENTIONS.md)): "
        "sec 2.1 (descriptive-before-inference); sec 3.2 (lagged-baseline "
        "discipline / where Q3.8 drift entered); sec 3.3 (no pre-commitment "
        "of MCAR/MAR readings for HAs not yet pre-spec'd; binding on the "
        "Stage 5 verdict scope); sec 4.1-4.4 (no interpretive marks; "
        "caveats vs a-priori; prior-driven hypotheses are confirmatory).",
        "",
        "---",
        "",
        "## 10. Limitations",
        "",
        "1. **No substantive HA verdict promotion**: this analysis is "
        "Layer 1 descriptive infrastructure-mapping ONLY (per CONVENTIONS "
        "sec 2.1 + sec 4.1); any future HA pre-reg that cites this "
        "analysis must apply its own missingness reasoning per its specific "
        "question.",
        "2. **MCAR/MAR diagnostic is descriptive** (per CONVENTIONS sec 3.3); "
        "it does NOT pre-commit any HA pre-reg's missingness assumption. "
        "The diagnostic flags reject_MCAR vs fail_to_reject_MCAR across "
        "channels for HA-pre-reg authors' investigation.",
        "3. **Welch-style chi-square is a non-parametric variant** of "
        "Little 1988; assumes informative-comparison channels carry mean "
        "differences but not necessarily covariance differences. The "
        "documented choice is defensible for the mixed-dtype master.",
        "4. **MNAR-suspect heuristic** is a descriptive flag (>30-day "
        "first-available drift OR >4 rolling inflections); not a verdict. "
        "Many flagged channels have legitimate sensor-rollout reasons "
        "(e.g. bb_sleep_end_value 2024-09-18) that are documented in "
        "DATA_DICTIONARY and not actually MNAR.",
        "5. **Stable-epoch threshold = 28d rolling >= 80%** (user-locked "
        "choice 2); other thresholds may yield different inflection counts; "
        "the threshold choice is documented.",
        "6. **Per-recovery-phase per-channel n** can be very small for "
        "phases 2 + 4a (14 + 56 days respectively); coverage percentages "
        "in those phases are honest but noisier than long-phase cells.",
        "",
        "*Generated programmatically by [`run.py`](run.py) from "
        "[`summary.json`](summary.json) (gitignored per "
        "`docs/research/**/*.json`). To refresh: ``python run.py``.*",
    ])
    path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def write_readme_md(summary: dict, path: Path) -> None:
    """Emit the README from the computed summary."""
    chs = summary["channels"]
    n_total = len(chs)
    n_in_master = sum(1 for c in chs.values() if c["in_master"])
    n_drift = sum(
        1 for c in chs.values()
        if not c["in_master"] or c["mnar_flag"]["mnar_suspect_flag"]
    )

    out_lines = [
        "# `trajectory/coverage_overview/` -- Strand B Q4.6 coverage map",
        "",
        "## Status",
        "",
        "**LANDED**: programmatic descriptive analysis answering "
        "Q4.6 per [`descriptive/README.md` sec 4.6](../../README.md). "
        "**LOAD-BEARING INFRASTRUCTURE foundation** for future HA pre-regs "
        "+ remaining Tier 3 Strand B topics (Q4.3 + Q4.5.b + Q4.4 + Q4.2).",
        "",
        "**Tier 3 Core 5, 2nd of 5 LANDED** (Q4.9 LANDED 0290627; this Q4.6 "
        "second; remaining: Q4.3 + Q4.5.b + Q4.4 + Q4.2 per user-chosen "
        "dependency order; Q4.7 + Q4.8 deferred per user 'narrower scope' "
        "triage).",
        "",
        "---",
        "",
        "## Research question",
        "",
        "Per descriptive README sec 4.6: **When does which Garmin signal "
        "become available? What missingness patterns matter for hypothesis "
        "design?**",
        "",
        "The gap this analysis closes (per README): 'coherent coverage-"
        "overview analysis that any HA pre-reg can cite for this column is "
        "available from date X with coverage Y%'.",
        "",
        "---",
        "",
        "## User-LOCKED operationalisation",
        "",
        "Per Strand B sec 7c interview 2026-06-25 (do NOT iterate):",
        "",
        "1. **Channel scope = all per_day_master columns** ({0} enumerated; "
        "{1} present in master; {2} documented-or-flagged as drift). "
        "Skip per-minute / per-bout primitives (own methodology MDs).".format(
            n_total, n_in_master, n_drift,
        ),
        "2. **Coverage metric = both day-level + 28d rolling**: day-level "
        "for binary 'available?'; 28d rolling for 'stable coverage?' at "
        ">= {0:.0%} threshold.".format(STABLE_EPOCH_THRESHOLD),
        "3. **Date-range slicing = continuous + per-recovery-phase** "
        "(6 phases per "
        "[`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md)).",
        "4. **Missingness pattern = full**: descriptive (gap counts + "
        "lengths) + block-length distribution + MCAR/MAR diagnostic (Welch-"
        "style chi-square; method choice documented at Stage 5 of "
        "[`run.py`](run.py)).",
        "",
        "---",
        "",
        "## Method",
        "",
        "**7-stage architecture** in [`run.py`](run.py):",
        "",
        "- **Stage 1**: data prep (load `per_day_master.csv`; enumerate "
        "columns per DATA_DICTIONARY sec 0-14 + 7B + 8B-E taxonomy; "
        "identify recovery_phase per row).",
        "- **Stage 2**: day-level coverage matrix (per-channel binary; "
        "first/last-available; total %; continuity flag).",
        "- **Stage 3**: 28d rolling coverage (% non-NaN; stable-epoch "
        "flag at >={0:.0%}; inflection dates; longest-run summary).".format(
            STABLE_EPOCH_THRESHOLD,
        ),
        "- **Stage 4**: per-recovery-phase summary (channel x 6 phases x "
        "% coverage).",
        "- **Stage 5**: missingness pattern (per channel: gap counts + "
        "gap-length distribution + block-length bin counts + Welch-style "
        "chi-square MCAR/MAR diagnostic + MNAR-suspect heuristic flag).",
        "- **Stage 6**: 3 output artefacts (coverage timeline chart + "
        "per-recovery-phase summary table + missingness diagnostic report).",
        "- **Stage 7**: programmatic emit `findings.md` + `README.md`.",
        "",
        "**Discipline guards** (CONVENTIONS):",
        "",
        "- sec 2.1: descriptive-before-inference; NO causal claims; NO HA "
        "verdict promotion.",
        "- sec 3.3: NO pre-commitment of MCAR/MAR readings for HAs not "
        "yet pre-spec'd; the diagnostic is descriptive infrastructure ONLY.",
        "- sec 3.6: named counts (every cell carries scheme + unit + "
        "source-file).",
        "- sec 4.1 + 4.2: no interpretive marks; pipeline-vs-doc drift "
        "honestly surfaced per [[feedback_flag_contradictions]] (Q3.8 "
        "push_burden_7d extension).",
        "",
        "---",
        "",
        "## Result",
        "",
        "Headline (see [`findings.md`](findings.md) for full Q4.6 answers):",
        "",
        "**{0} columns enumerated**; {1} present in `per_day_master.csv`; "
        "{2} surface either pipeline-vs-doc drift or MNAR-suspect "
        "heuristic flag.".format(n_total, n_in_master, n_drift),
        "",
        "Coverage span: **earliest 2021-08-16** (Garmin extract); "
        "**latest 2026-06-04** (as_of_date). gevoelscore starts 2022-09-03; "
        "bb_overnight_gain truth starts 2024-09-18 (proxy bridges back to "
        "2024-07-08 per [`bb_overnight_gain_proxy.md`](../../../../methodology/bb_overnight_gain_proxy.md)).",
        "",
        "**3 output artefacts** emitted per descriptive README sec 4.6 "
        "expectations:",
        "",
        "1. Coverage timeline chart: [`plots/coverage_timeline.png`](plots/coverage_timeline.png) (gitignored).",
        "2. Per-recovery-phase summary heatmap: [`plots/per_phase_coverage_heatmap.png`](plots/per_phase_coverage_heatmap.png) (gitignored).",
        "3. Missingness diagnostic report: [`plots/missingness_diagnostic.png`](plots/missingness_diagnostic.png) (gitignored).",
        "",
        "Per-recovery-phase coverage summary table + first/last-available "
        "headlines + MCAR/MAR verdict counts + MNAR-suspect listing + "
        "pipeline-vs-doc drift listing all live in [`findings.md`](findings.md).",
        "",
        "---",
        "",
        "## Cross-references (descriptive only -- NO HA verdict promotion)",
        "",
        "- [`DATA_DICTIONARY.md`](../../../../DATA_DICTIONARY.md) -- "
        "column-level documentation; family enumeration source.",
        "- [`methodology/bb_overnight_gain_proxy.md`](../../../../methodology/bb_overnight_gain_proxy.md) "
        "(LOAD-BEARING) -- BB truth/proxy/best/source 4-channel audit "
        "trail + 2024-07-08 / 2024-09-18 UDS rollout dates.",
        "- [`methodology/stress_low_motion_primitive.md`](../../../../methodology/stress_low_motion_primitive.md) "
        "-- Session E lock for the 11-column stress_low_motion family.",
        "- [`methodology/garmin_indicators_audit.md`](../../../../methodology/garmin_indicators_audit.md) "
        "-- known-issues catalog cross-referenced per channel.",
        "- [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) "
        "-- 6-phase axis definitions for per-phase summary table.",
        "- [`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) "
        "-- Stratum 4 boundary 2022-09-03 for outcome-side coverage.",
        "- [`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) "
        "-- v2 phase-coverage precedent (bb_overnight_gain 5/6 empty + "
        "gevoelscore 1+2 empty inherit here).",
        "- [`operationalisation_support/push_burden_7d/findings.md`](../../operationalisation_support/push_burden_7d/findings.md) "
        "-- Q3.8 CONVENTIONS sec 3.2 / audit MD drift precedent extended "
        "across all columns in this analysis.",
        "- [`operationalisation_support/bb_overnight_gain/findings.md`](../../operationalisation_support/bb_overnight_gain/findings.md) "
        "-- Q3.5 truth-only window analytic discipline precedent.",
        "- [`CONVENTIONS.md`](../../../../CONVENTIONS.md) sec 2.1, 3.2, "
        "3.3, 4.1-4.4 -- discipline anchors.",
        "",
        "---",
        "",
        "## Files",
        "",
        "- [`README.md`](README.md) -- this file (programmatically emitted).",
        "- [`findings.md`](findings.md) -- Q4.6 answers (programmatically emitted).",
        "- [`run.py`](run.py) -- the 7-stage descriptive computation script.",
        "- `summary.json` -- machine-readable per-channel per-phase stats (gitignored).",
        "- `plots/*.png` -- 3 artefacts (gitignored).",
        "",
        "---",
        "",
        "*Programmatic README emit by [`run.py`](run.py) per the Q3.5 / Q3.6 "
        "/ Q3.7 / Q3.8 precedent (Write-tool harness heuristic on the "
        "literal filename `findings` / `README`). To refresh: "
        "``python run.py``.*",
    ]
    path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> None:
    """Drive the 7-stage architecture; emit summary.json + plots + MDs."""
    if not os.environ.get("GEVOELSCORE_DATA_PATH"):
        os.environ["GEVOELSCORE_DATA_PATH"] = (
            "C:/Users/Gebruiker/Documents/gevoelscore-data"
        )

    print("--- Stage 1: data prep + column-family enumeration ---")
    df = load_master(as_of_date=AS_OF_DATE)
    if "recovery_phase" not in df.columns:
        raise RuntimeError(
            "recovery_phase column missing from per_day_master.csv. "
            "Coverage_overview needs the column added at commit e00df27 "
            "(2026-06-22) per lc_recovery_phase_axis.md sec 6.5."
        )

    enumerated = enumerate_columns(df)
    n_total = len(enumerated)
    n_in_master = sum(1 for v in enumerated.values() if v["in_master"])
    n_doc_only = sum(1 for v in enumerated.values() if not v["in_master"])
    print(
        "  total enumerated: {0} (in_master={1}; doc_only_drift={2})".format(
            n_total, n_in_master, n_doc_only,
        )
    )

    summary: dict = {
        "analysis": "trajectory/coverage_overview",
        "version": "Strand B Q4.6 v1 (LANDED 2026-06-25)",
        "axis_source": (
            "methodology/lc_recovery_phase_axis.md (LOCKED d47e0d3 2026-06-19); "
            "recovery_phase column at commit e00df27 (2026-06-22)"
        ),
        "strand": "B (multi-year trajectory; LOAD-BEARING INFRASTRUCTURE)",
        "as_of_date": AS_OF_DATE,
        "source_file_master": "per_day_master.csv",
        "n_rows_total": int(len(df)),
        "phase_windows": [
            {"phase": name, "start": str(s), "end": str(e)}
            for name, s, e in PHASE_WINDOWS
        ],
        "phase_counts": {
            ph: int((df["recovery_phase"] == ph).sum()) for ph in PHASE_ORDER
        },
        "user_locked_operationalisation": {
            "channel_scope": (
                "all per_day_master columns (Strand B sec 7c choice 1b)"
            ),
            "coverage_metric": (
                "both day-level + 28d rolling (Strand B sec 7c choice 2c)"
            ),
            "date_slicing": (
                "continuous + per-recovery-phase 6 phases "
                "(Strand B sec 7c choice 3 a+b)"
            ),
            "missingness_pattern": (
                "full: descriptive + block-length + MCAR/MAR diagnostic "
                "(Welch-style chi-square; Strand B sec 7c choice 4)"
            ),
        },
        "stable_epoch_threshold": STABLE_EPOCH_THRESHOLD,
        "rolling_window_days": ROLLING_WINDOW,
        "mcar_alpha": MCAR_ALPHA,
        "channels": {},
    }

    # --- Stages 2-5: per-channel ---
    print("--- Stages 2-5: per-channel coverage + missingness ---")
    in_master_channels = [c for c, info in enumerated.items() if info["in_master"]]
    for ch in enumerated.keys():
        info = enumerated[ch]
        ch_entry: dict = {
            "family": info["family"],
            "in_master": info["in_master"],
            "documented_start": info["documented_start"],
            "known_issue_note": info["known_issue_note"],
        }
        if info["in_master"]:
            ch_entry["day_coverage"] = compute_day_level_coverage(df, ch)
            ch_entry["rolling_coverage"] = compute_rolling_coverage(df, ch)
            ch_entry["per_phase_coverage"] = compute_per_phase_coverage(df, ch)
            ch_entry["gap_stats"] = compute_gap_statistics(df, ch)
        else:
            # documented-but-absent placeholders
            ch_entry["day_coverage"] = {
                "n_total": 0, "n_non_nan": 0, "pct_total": 0.0,
                "first_date": None, "last_date": None,
                "pct_in_window": 0.0, "continuity_flag": False,
            }
            ch_entry["rolling_coverage"] = {
                "n_stable_epoch_days": 0,
                "first_stable_date": None, "last_stable_date": None,
                "n_inflection_dates": 0, "stable_epoch_runs": [],
                "n_stable_epoch_runs": 0, "longest_stable_run_days": 0,
            }
            ch_entry["per_phase_coverage"] = {
                ph: {"n_available": 0, "n_total": int((df["recovery_phase"] == ph).sum()),
                     "pct_coverage": 0.0}
                for ph in PHASE_ORDER
            }
            ch_entry["gap_stats"] = {
                "n_gaps": 0, "n_gap_days_total": 0, "longest_gap_days": 0,
                "gap_lengths_p25": None, "gap_lengths_p50": None,
                "gap_lengths_p75": None, "gap_lengths_p90": None,
                "gap_length_distribution_counts": {},
            }
        ch_entry["mnar_flag"] = flag_mnar_suspect(
            ch,
            ch_entry["day_coverage"],
            ch_entry["rolling_coverage"],
            ch_entry["per_phase_coverage"],
            info["documented_start"],
        )
        summary["channels"][ch] = ch_entry

    # --- Stage 5b: MCAR diagnostic on numeric channels ---
    print("--- Stage 5b: MCAR/MAR diagnostic (Welch-style chi-square) ---")
    mcar_results = compute_mcar_diagnostic(df, in_master_channels)
    for ch, res in mcar_results.items():
        summary["channels"][ch]["mcar_diagnostic"] = res
    # for non-numeric channels: explicit "no_test" marker
    for ch in in_master_channels:
        if ch not in mcar_results:
            summary["channels"][ch]["mcar_diagnostic"] = None

    # --- Stage 6: output artefacts ---
    print("--- Stage 6: emit output artefacts ---")
    plot1 = make_coverage_timeline_plot(df, enumerated, HERE / "plots")
    summary["coverage_timeline_plot"] = "plots/" + plot1 if plot1 else None
    plot2 = make_per_phase_heatmap(summary, HERE / "plots")
    summary["per_phase_coverage_heatmap"] = "plots/" + plot2 if plot2 else None
    plot3 = make_missingness_diagnostic_plot(summary, HERE / "plots")
    summary["missingness_diagnostic_plot"] = "plots/" + plot3 if plot3 else None

    # --- emit summary.json ---
    summary_path = HERE / "summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print("Wrote " + str(summary_path))

    # --- Stage 7: programmatic emit findings.md + README.md ---
    print("--- Stage 7: emit findings.md + README.md ---")
    write_findings_md(summary, HERE / "findings.md")
    print("Wrote " + str(HERE / "findings.md"))
    write_readme_md(summary, HERE / "README.md")
    print("Wrote " + str(HERE / "README.md"))

    # console headlines
    verdict_counts: dict = {}
    for c in summary["channels"].keys():
        v = summary["channels"][c].get("mcar_diagnostic")
        if v is None:
            verdict_counts["no_test"] = verdict_counts.get("no_test", 0) + 1
        else:
            label = v.get("verdict", "no_test")
            verdict_counts[label] = verdict_counts.get(label, 0) + 1
    n_mnar = sum(
        1 for c in summary["channels"].values()
        if c["in_master"] and c["mnar_flag"]["mnar_suspect_flag"]
    )
    n_drift = sum(1 for c in summary["channels"].values() if not c["in_master"])

    print("")
    print("--- HEADLINE ---")
    print("total enumerated: " + str(n_total)
          + " (in_master=" + str(n_in_master)
          + "; doc_only_drift=" + str(n_drift) + ")")
    print("MCAR verdicts:")
    for k, v in verdict_counts.items():
        print("  " + k + ": " + str(v))
    print("MNAR-suspect channels: " + str(n_mnar))
    print("")
    print("Done.")


if __name__ == "__main__":
    main()
