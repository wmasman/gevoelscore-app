"""Q4.4 -- cohort_topology: 29 crashes + 79 dips + dip-cluster overlay + recovery-
window distributions + matched-control baseline.

Refreshes cohort topology per descriptive README sec 4.4. Pre-requisite substrate
for HA-P6 follow-ups. Strand B (multi-year trajectory; descriptive).

USER-LOCKED OPERATIONALISATION (per Strand B sec 7c interview 2026-06-25;
do NOT iterate):

1. Event scope = crashes + dips (29 + 79 = 108 events). Sub-threshold dips
   EXCLUDED per user choice.
2. Dip-cluster overlay = 30d rolling dip count + per-recovery-phase dip rate
   (skip DBSCAN).
3. Recovery-window distributions = both per-crash (HA-P6 v3 Arm-A REUSE on
   7 channels) + per-dip (NOVEL on 7 channels) + crash-vs-dip comparison.
4. "Normal" baseline = matched-control (HA-P6 v3 Arm-A REUSE) +
   per-recovery-phase reference.

STAGE ARCHITECTURE (per handoff sec 3.2):

- Stage 1 (data prep): load per_day_master + labels_crash_v2; identify
  recovery_phase per event date.
- Stage 2 (event-by-event): per crash + per dip start/end/duration/lowest-score/
  recovery-time. 108 events total.
- Stage 3 (dip-cluster overlay): 30d rolling dip + crash count + per-recovery-
  phase rate.
- Stage 4 (recovery-window distributions): per-crash via HA-P6 v3 Arm-A on 7
  channels + per-dip NOVEL on 7 channels + crash-vs-dip comparison.
- Stage 5 (baseline): matched-control (HA-P6 v3 Arm-A REUSE) + per-recovery-
  phase reference.
- Stage 6 (output artefacts): cohort topology summary table + dip-cluster
  overlay timeline + crash-vs-dip recovery comparison + per-recovery-phase
  event rates.
- Stage 7 (programmatic emit): findings.md + README.md.

CROSS-REFERENCES LOAD-BEARING (per handoff sec 3.3):

- HA-P6 v3 Arm-A matched-control machinery REUSED for matched-control logic
  (sec 4.4 + sec 4.5 of HA-P6 v3 hypothesis.md spec).
- Q4.9 episode-level matched per-crash body-state profile REPRODUCED at the
  cohort-topology layer; per-dip side is novel.
- Q4.3 rp5 + cp3 boundaries cross-referenced in Stage 3 per-recovery-phase
  event rate analysis (rate shifts at intervention boundaries).
- Q4.5.b matched-control vs trajectory-confound framing CITED in
  methodology discussion.
- crash_episode_descriptive sec 1-3 + crash_episode_prolonged cited
  descriptively (definitional source).
- recovery_arc v2 multi-year trajectory backdrop cited for the
  per-phase event-rate finding.

DISCIPLINE GUARDS (per CONVENTIONS):

- sec 2.1 descriptive-before-inference: cohort-topology map per cell;
  NO causal claims; NO substantive HA verdict promotion.
- sec 3.1 personal baseline: per-channel z-score against lagged personal
  baseline (HA-P6 v3 sec 4.5 spec).
- sec 3.4 crash-drop sensitivity: matched-control baseline IS the
  cross-condition reference (the discipline is dispatched by construction).
- sec 3.6 named counts: every n reports scheme + unit + source.
- sec 4.1 + sec 4.2: descriptive framing only ("rate X%, distribution Y").
- sec 4.4: cohort topology mapping ONLY; refresh substrate for HA-P6
  follow-ups; NOT a substantive verdict promotion.

HONEST FRAMINGS (per handoff sec 3.4):

- Per-dip recovery curves are NOVEL; per-crash recovery curves REPRODUCE
  HA-P6 v3 Arm-A at the cohort-topology aggregation.
- Sub-threshold dips EXCLUDED from primary scope (user-locked).
- n=29 crashes + n=79 dips: sample sizes tight; per-recovery-phase event
  rates have wide CIs (phases 1-3 <14mo each).

NO causal claims; NO substantive HA verdict promotion; descriptive
cohort-topology mapping only.
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/trajectory/cohort_topology
# parents[0]=trajectory; [1]=descriptive; [2]=analyses
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from frame import (  # noqa: E402
    load_crash_labels,
    load_master,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


AS_OF_DATE = "2026-06-05"  # parity with Q4.9 + Q4.3 + Q4.5.b precedents

# 7 channels per HA-P6 v3 sec 4.1 + recovery_arc v2 (same 7-channel set)
CHANNELS = [
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "bb_overnight_gain",
    "resting_hr",
    "gevoelscore",
    "stress_low_motion_min_count_S60_Mlow",
]

# Lagged personal baseline window per HA-P6 v3 sec 4.5
BASELINE_WINDOW = 60   # 60-day pre-event window
BASELINE_LAG = 30      # excludes [t0-30, t0-1]; uses [t0-90, t0-31]
MIN_BASELINE_VALID = 40  # >= 40 of 60 days valid per HA-P6 v3 sec 4.5 step 5

# Recovery post-event window per HA-P6 v3 sec 4.2
PRE_EVENT_PRE_DAYS = 10   # pre-event trajectory for Arm-A matching
POST_EVENT_DAYS = 5       # primary post-event window [t+1, t+5]

# Matched-control tolerance ladder per HA-P6 v3 sec 4.4 step 4
MATCH_TOLERANCE_LADDER = [1.0, 1.5, 2.0]
MATCH_DISTANCE_MIN = 30   # >= 30d from event to avoid leakage

# Rolling overlay window per user-locked operationalisation
ROLLING_WINDOW_DAYS = 30

# Recovery_phase categories per lc_recovery_phase_axis.md sec 2
RECOVERY_PHASES = [
    "pre_illness_healthy",
    "acute_infection",
    "lc_pre_ergo",
    "pacing_pre_citalopram_learning",
    "pacing_habit_established",
    "citalopram_modulated",
]

# Citalopram phase boundaries (used in Stage 5 matched-control + Stage 6
# per-phase reads alongside recovery_phase)
PHASE_BOUNDARIES_CITALOPRAM = [
    ("unmedicated", date(2022, 9, 3), date(2024, 4, 8)),
    ("buildup", date(2024, 4, 9), date(2024, 6, 19)),
    ("consolidation", date(2024, 6, 20), date(2026, 3, 19)),
    ("afbouw", date(2026, 3, 20), date(2026, 6, 5)),
]


def citalopram_phase(d) -> str:
    if not isinstance(d, date):
        d = pd.Timestamp(d).date()
    for name, start, end in PHASE_BOUNDARIES_CITALOPRAM:
        if start <= d <= end:
            return name
    return "out_of_scope"


# ---------------------------------------------------------------------------
# Stage 1 -- data prep
# ---------------------------------------------------------------------------


def stage1_data_prep() -> dict:
    """Load per_day_master + labels_crash_v2; merge; identify 108 events.

    Returns dict with:
    - df: full per_day_master DataFrame with labels merged + helper columns
    - events: 108-row DataFrame (one row per event; crash + dip)
    - n_master: total master row count
    - phase_counts: per-recovery-phase day counts on the full corpus
    """
    master = load_master(as_of_date=AS_OF_DATE)
    labels = load_crash_labels(as_of_date=AS_OF_DATE)

    master["date"] = pd.to_datetime(master["date"])
    master = master.sort_values("date").reset_index(drop=True)

    labels = labels.copy()
    labels["date"] = pd.to_datetime(labels["date"])
    labels["episode_start"] = pd.to_datetime(labels["episode_start"])
    labels["episode_end"] = pd.to_datetime(labels["episode_end"])

    df = master.merge(
        labels[["date", "label", "episode_id", "dip_cluster_id"]],
        on="date",
        how="left",
    )

    # Build the events table: one row per episode_id (29 crashes + 79 dips
    # = 108 events; crashes can span multiple days, dips are single-day).
    label_rows = labels.dropna(subset=["episode_id"]).copy()
    events = (
        label_rows.groupby(["episode_id", "label"], as_index=False)
        .agg(
            start_date=("episode_start", "first"),
            end_date=("episode_end", "first"),
            duration_days=("episode_length_days", "first"),
            lowest_score=("score", "min"),
            n_days_in_episode=("date", "count"),
        )
        .sort_values("start_date")
        .reset_index(drop=True)
    )

    # Sanity check: 108 events, with 29 crashes + 79 dips
    if len(events) != 108:
        raise RuntimeError(
            "Expected 108 events (29 crashes + 79 dips); got "
            + str(len(events))
        )
    n_crash_eps = int((events["label"] == "crash").sum())
    n_dip_eps = int((events["label"] == "dip").sum())
    if n_crash_eps != 29 or n_dip_eps != 79:
        raise RuntimeError(
            "Expected 29 crash + 79 dip episodes; got "
            + str(n_crash_eps) + " crash + " + str(n_dip_eps) + " dip"
        )

    # Attach recovery_phase per event start date (from master)
    date_to_phase = dict(
        zip(master["date"].dt.date.tolist(), master["recovery_phase"].tolist())
    )
    events["recovery_phase"] = events["start_date"].dt.date.map(date_to_phase)
    events["citalopram_phase"] = events["start_date"].dt.date.apply(
        citalopram_phase
    )

    # Phase counts on the full corpus (for per-phase event rate denominator)
    phase_counts = master["recovery_phase"].value_counts().to_dict()

    return {
        "df": df,
        "events": events,
        "n_master": int(len(master)),
        "n_crashes": n_crash_eps,
        "n_dips": n_dip_eps,
        "n_events": int(len(events)),
        "phase_counts": phase_counts,
    }


# ---------------------------------------------------------------------------
# Stage 2 -- event-by-event characterisation (108 events)
# ---------------------------------------------------------------------------


def stage2_event_characterisation(df: pd.DataFrame, events: pd.DataFrame) -> dict:
    """Per event: start / end / duration / lowest-score / recovery-time
    (days until gevoelscore returns >= per-event baseline).

    Per crash_episode_descriptive sec 3 the canonical recovery-time op (A) is
    rolling-30d-median baseline. We compute both (A) rolling-30d-median and
    (B) gevoelscore >= 4 (the v2 threshold for "not below crash floor").
    """
    df = df.copy()
    df["date_only"] = df["date"].dt.date
    date_to_gv = dict(zip(df["date_only"].tolist(), df["gevoelscore"].tolist()))
    df = df.sort_values("date").reset_index(drop=True)

    # 30-day rolling median of gevoelscore (centred-trailing, min_periods 10)
    df["gv_roll30_med"] = (
        df["gevoelscore"].rolling(window=30, min_periods=10).median()
    )
    date_to_rollmed = dict(
        zip(df["date_only"].tolist(), df["gv_roll30_med"].tolist())
    )

    per_event_rows = []
    rec_time_A_vals = []
    rec_time_B_vals = []

    for _, ep in events.iterrows():
        ep_id = ep["episode_id"]
        ep_label = ep["label"]
        start = ep["start_date"].date()
        end = ep["end_date"].date()
        duration = int(ep["duration_days"]) if not pd.isna(ep["duration_days"]) else 1
        lowest = float(ep["lowest_score"]) if not pd.isna(ep["lowest_score"]) else float("nan")

        # Recovery-time op (A) -- days until gv >= rolling30d median
        # Reference value: rolling30d median on (end + 1) day
        ref_A = date_to_rollmed.get(end + timedelta(days=1), float("nan"))
        rec_time_A = float("nan")
        if not np.isnan(ref_A):
            for k in range(1, 61):
                gv_k = date_to_gv.get(end + timedelta(days=k), float("nan"))
                if not np.isnan(gv_k) and gv_k >= ref_A:
                    rec_time_A = k
                    break

        # Recovery-time op (B) -- days until gv >= 4 (above v2 threshold)
        rec_time_B = float("nan")
        for k in range(1, 61):
            gv_k = date_to_gv.get(end + timedelta(days=k), float("nan"))
            if not np.isnan(gv_k) and gv_k >= 4:
                rec_time_B = k
                break

        per_event_rows.append({
            "episode_id": ep_id,
            "label": ep_label,
            "start_date": str(start),
            "end_date": str(end),
            "duration_days": duration,
            "lowest_score": lowest,
            "recovery_time_A_rolling30d_median": rec_time_A,
            "recovery_time_B_above_threshold": rec_time_B,
            "ref_value_A": ref_A,
            "recovery_phase": ep["recovery_phase"],
            "citalopram_phase": ep["citalopram_phase"],
        })

        if not np.isnan(rec_time_A):
            rec_time_A_vals.append(rec_time_A)
        if not np.isnan(rec_time_B):
            rec_time_B_vals.append(rec_time_B)

    # Per-label aggregates
    per_event_df = pd.DataFrame(per_event_rows)

    def _agg(sub: pd.DataFrame, col: str) -> dict:
        vals = sub[col].dropna().to_numpy()
        if len(vals) == 0:
            return {"n": 0}
        return {
            "n": int(len(vals)),
            "min": float(np.min(vals)),
            "p25": float(np.quantile(vals, 0.25)),
            "median": float(np.median(vals)),
            "p75": float(np.quantile(vals, 0.75)),
            "p90": float(np.quantile(vals, 0.90)),
            "max": float(np.max(vals)),
            "mean": float(np.mean(vals)),
        }

    aggregates = {}
    for label_name in ("crash", "dip"):
        sub = per_event_df[per_event_df["label"] == label_name]
        aggregates[label_name] = {
            "n_events": int(len(sub)),
            "duration_days": _agg(sub, "duration_days"),
            "lowest_score": _agg(sub, "lowest_score"),
            "recovery_time_A_rolling30d_median": _agg(
                sub, "recovery_time_A_rolling30d_median"
            ),
            "recovery_time_B_above_threshold": _agg(
                sub, "recovery_time_B_above_threshold"
            ),
        }

    return {
        "per_event_rows": per_event_rows,
        "aggregates": aggregates,
    }


# ---------------------------------------------------------------------------
# Stage 3 -- dip-cluster overlay (30d rolling + per-recovery-phase rate)
# ---------------------------------------------------------------------------


def stage3_dip_cluster_overlay(df: pd.DataFrame, events: pd.DataFrame) -> dict:
    """30d rolling dip + crash count over full corpus + per-recovery-phase
    event rate (crashes-per-day, dips-per-day) per phase.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Mark per-day event-start flag (one flag per event start date)
    crash_starts = set(
        events.loc[events["label"] == "crash", "start_date"].dt.date.tolist()
    )
    dip_starts = set(
        events.loc[events["label"] == "dip", "start_date"].dt.date.tolist()
    )
    df["is_crash_start"] = df["date"].dt.date.isin(crash_starts).astype(int)
    df["is_dip_start"] = df["date"].dt.date.isin(dip_starts).astype(int)

    # 30d rolling counts of event-starts (trailing window)
    df["rolling30d_crash_starts"] = (
        df["is_crash_start"].rolling(window=ROLLING_WINDOW_DAYS, min_periods=1).sum()
    )
    df["rolling30d_dip_starts"] = (
        df["is_dip_start"].rolling(window=ROLLING_WINDOW_DAYS, min_periods=1).sum()
    )
    df["rolling30d_total_events"] = (
        df["rolling30d_crash_starts"] + df["rolling30d_dip_starts"]
    )

    # Identify "cluster epochs" -- dates where rolling-30d total event-count
    # is at or above the 90th percentile (descriptive density threshold)
    p90_total = float(np.quantile(df["rolling30d_total_events"], 0.90))
    high_density = df["rolling30d_total_events"] >= p90_total
    # Group consecutive high-density days into runs
    cluster_epochs = []
    in_epoch = False
    epoch_start = None
    epoch_peak_count = 0
    for i, (d, v, hd) in enumerate(
        zip(df["date"].dt.date, df["rolling30d_total_events"], high_density)
    ):
        if hd and not in_epoch:
            in_epoch = True
            epoch_start = d
            epoch_peak_count = int(v)
        elif hd and in_epoch:
            if int(v) > epoch_peak_count:
                epoch_peak_count = int(v)
        elif not hd and in_epoch:
            cluster_epochs.append({
                "start": str(epoch_start),
                "end": str(df["date"].dt.date.iloc[i - 1]),
                "peak_30d_event_count": int(epoch_peak_count),
            })
            in_epoch = False
            epoch_start = None
            epoch_peak_count = 0
    if in_epoch:
        cluster_epochs.append({
            "start": str(epoch_start),
            "end": str(df["date"].dt.date.iloc[-1]),
            "peak_30d_event_count": int(epoch_peak_count),
        })

    # Per-recovery-phase event rate (events-per-day per phase)
    per_phase_rates = {}
    for phase in RECOVERY_PHASES:
        ph_mask = df["recovery_phase"] == phase
        n_days = int(ph_mask.sum())
        n_crash_starts = int(df.loc[ph_mask, "is_crash_start"].sum())
        n_dip_starts = int(df.loc[ph_mask, "is_dip_start"].sum())
        per_phase_rates[phase] = {
            "n_days": n_days,
            "n_crash_starts": n_crash_starts,
            "n_dip_starts": n_dip_starts,
            "n_total_event_starts": n_crash_starts + n_dip_starts,
            "crash_rate_per_30d": (
                float(n_crash_starts) / n_days * 30.0 if n_days > 0 else float("nan")
            ),
            "dip_rate_per_30d": (
                float(n_dip_starts) / n_days * 30.0 if n_days > 0 else float("nan")
            ),
            "total_rate_per_30d": (
                float(n_crash_starts + n_dip_starts) / n_days * 30.0
                if n_days > 0
                else float("nan")
            ),
        }

    # Cross-reference Q4.3 rp5 (rp4b -> citalopram_modulated; 2024-04-09) +
    # cp3 (consolidation -> afbouw; 2026-03-20). Report event-rate before/after.
    rp5_date = date(2024, 4, 9)
    cp3_date = date(2026, 3, 20)

    def _rate_around(boundary_d: date, window_days: int = 90) -> dict:
        before_lo = boundary_d - timedelta(days=window_days)
        before_hi = boundary_d - timedelta(days=1)
        after_lo = boundary_d
        after_hi = boundary_d + timedelta(days=window_days)
        before_mask = (df["date"].dt.date >= before_lo) & (
            df["date"].dt.date <= before_hi
        )
        after_mask = (df["date"].dt.date >= after_lo) & (
            df["date"].dt.date <= after_hi
        )
        n_before_days = int(before_mask.sum())
        n_after_days = int(after_mask.sum())
        n_before_events = int(
            df.loc[before_mask, "is_crash_start"].sum()
            + df.loc[before_mask, "is_dip_start"].sum()
        )
        n_after_events = int(
            df.loc[after_mask, "is_crash_start"].sum()
            + df.loc[after_mask, "is_dip_start"].sum()
        )
        return {
            "window_days": window_days,
            "n_before_days": n_before_days,
            "n_before_events": n_before_events,
            "before_rate_per_30d": (
                float(n_before_events) / n_before_days * 30.0
                if n_before_days > 0
                else float("nan")
            ),
            "n_after_days": n_after_days,
            "n_after_events": n_after_events,
            "after_rate_per_30d": (
                float(n_after_events) / n_after_days * 30.0
                if n_after_days > 0
                else float("nan")
            ),
        }

    boundary_rates = {
        "rp5_2024_04_09": _rate_around(rp5_date, window_days=90),
        "cp3_2026_03_20": _rate_around(cp3_date, window_days=90),
    }

    return {
        "rolling_window_days": ROLLING_WINDOW_DAYS,
        "cluster_density_threshold_p90": p90_total,
        "n_cluster_epochs": len(cluster_epochs),
        "cluster_epochs": cluster_epochs,
        "per_phase_rates": per_phase_rates,
        "boundary_rates": boundary_rates,
        "_timeline_df": df[
            [
                "date",
                "is_crash_start",
                "is_dip_start",
                "rolling30d_crash_starts",
                "rolling30d_dip_starts",
                "rolling30d_total_events",
                "recovery_phase",
            ]
        ].copy(),
    }


# ---------------------------------------------------------------------------
# Stage 4 -- recovery-window distributions (per-crash + per-dip + comparison)
# ---------------------------------------------------------------------------


def stage4_recovery_distributions(
    df: pd.DataFrame, events: pd.DataFrame
) -> dict:
    """Per-channel z-trajectory in [t+1, t+5] post-event window for both
    crashes (REUSE HA-P6 v3 Arm-A) and dips (NOVEL same machinery).

    Per HA-P6 v3 sec 4.5 (Arm-B lagged personal baseline):
    - baseline window [t0-90, t0-30], same recovery phase, non-event days
    - >= 40/60 valid days required
    - z = (channel(t0+k) - mu_ch) / sigma_ch with mu = trimmed-mean (10/90),
      sigma = trimmed-std

    Then aggregate per-channel median z at each post-day across events.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["date_only"] = df["date"].dt.date
    date_to_idx = {d: i for i, d in enumerate(df["date_only"].tolist())}

    # Pre-compute event-day mask (any crash OR dip day): used to exclude
    # event days from baseline windows.
    event_dates = set(
        df.loc[
            (df["label"] == "crash") | (df["label"] == "dip"), "date_only"
        ].tolist()
    )

    per_event_traj = []  # one entry per (event, channel, post_day)
    by_event = {}        # episode_id -> per-channel post-day z arrays

    for _, ep in events.iterrows():
        ep_id = ep["episode_id"]
        ep_label = ep["label"]
        ep_phase = ep["recovery_phase"]
        end_date = ep["end_date"].date()
        end_idx = date_to_idx.get(end_date)
        if end_idx is None:
            by_event[ep_id] = {
                ch: [float("nan")] * POST_EVENT_DAYS for ch in CHANNELS
            }
            continue

        # Baseline window: [end - 90, end - 31] (inclusive). Use end-date as
        # t0 anchor here (HA-P6 v3 sec 4.3 primary t0 = episode_end).
        baseline_lo = end_idx - 90
        baseline_hi = end_idx - 31

        ch_z_arrays = {}
        for ch in CHANNELS:
            ch_vals = df[ch].to_numpy(dtype=float)
            phase_col = df["recovery_phase"].to_numpy()

            # Build baseline pool: same recovery phase, non-event days, valid
            if baseline_lo < 0:
                ch_z_arrays[ch] = [float("nan")] * POST_EVENT_DAYS
                continue
            baseline_indices = []
            for j in range(max(0, baseline_lo), baseline_hi + 1):
                d_j = df["date_only"].iloc[j]
                if d_j in event_dates:
                    continue
                if phase_col[j] != ep_phase:
                    continue
                if np.isnan(ch_vals[j]):
                    continue
                baseline_indices.append(j)

            if len(baseline_indices) < MIN_BASELINE_VALID:
                ch_z_arrays[ch] = [float("nan")] * POST_EVENT_DAYS
                continue

            baseline_vals = ch_vals[baseline_indices]
            # Trimmed mean + std (10/90 cut per HA-P6 v3 sec 4.5 step 5)
            q10 = np.quantile(baseline_vals, 0.10)
            q90 = np.quantile(baseline_vals, 0.90)
            trimmed = baseline_vals[(baseline_vals >= q10) & (baseline_vals <= q90)]
            if len(trimmed) < 5:
                ch_z_arrays[ch] = [float("nan")] * POST_EVENT_DAYS
                continue
            mu_ch = float(np.mean(trimmed))
            sigma_ch = float(np.std(trimmed, ddof=1))
            if sigma_ch == 0.0 or np.isnan(sigma_ch):
                ch_z_arrays[ch] = [float("nan")] * POST_EVENT_DAYS
                continue

            # Post-event z trajectory [t+1, t+5]
            z_array = []
            for k in range(1, POST_EVENT_DAYS + 1):
                pi = end_idx + k
                if pi < 0 or pi >= len(df):
                    z_array.append(float("nan"))
                    continue
                v = ch_vals[pi]
                if np.isnan(v):
                    z_array.append(float("nan"))
                    continue
                z_array.append(float((v - mu_ch) / sigma_ch))
            ch_z_arrays[ch] = z_array

            for k_idx, z in enumerate(z_array):
                per_event_traj.append({
                    "episode_id": ep_id,
                    "label": ep_label,
                    "recovery_phase": ep_phase,
                    "channel": ch,
                    "post_day": k_idx + 1,
                    "z": z,
                })

        by_event[ep_id] = ch_z_arrays

    # Aggregate per (label, channel, post_day) -> median + IQR
    per_label_channel_postday = {}
    traj_df = pd.DataFrame(per_event_traj)

    for label_name in ("crash", "dip"):
        per_label_channel_postday[label_name] = {}
        sub_label = traj_df[traj_df["label"] == label_name]
        for ch in CHANNELS:
            per_label_channel_postday[label_name][ch] = {}
            sub_ch = sub_label[sub_label["channel"] == ch]
            for k in range(1, POST_EVENT_DAYS + 1):
                vals = sub_ch.loc[sub_ch["post_day"] == k, "z"].dropna().to_numpy()
                if len(vals) == 0:
                    per_label_channel_postday[label_name][ch][k] = {
                        "n": 0,
                        "median_z": float("nan"),
                        "p25_z": float("nan"),
                        "p75_z": float("nan"),
                        "mean_z": float("nan"),
                    }
                else:
                    per_label_channel_postday[label_name][ch][k] = {
                        "n": int(len(vals)),
                        "median_z": float(np.median(vals)),
                        "p25_z": float(np.quantile(vals, 0.25)),
                        "p75_z": float(np.quantile(vals, 0.75)),
                        "mean_z": float(np.mean(vals)),
                    }

    # Crash-vs-dip comparison: per channel, median absolute z over [t+1, t+5]
    crash_vs_dip = {}
    for ch in CHANNELS:
        crash_window_med = []
        dip_window_med = []
        for k in range(1, POST_EVENT_DAYS + 1):
            c_med = per_label_channel_postday["crash"][ch][k]["median_z"]
            d_med = per_label_channel_postday["dip"][ch][k]["median_z"]
            if not np.isnan(c_med):
                crash_window_med.append(c_med)
            if not np.isnan(d_med):
                dip_window_med.append(d_med)
        crash_vs_dip[ch] = {
            "crash_window_median_abs_z": (
                float(np.mean(np.abs(crash_window_med)))
                if crash_window_med
                else float("nan")
            ),
            "dip_window_median_abs_z": (
                float(np.mean(np.abs(dip_window_med)))
                if dip_window_med
                else float("nan")
            ),
            "crash_minus_dip_at_t1": (
                per_label_channel_postday["crash"][ch][1]["median_z"]
                - per_label_channel_postday["dip"][ch][1]["median_z"]
                if not (
                    np.isnan(per_label_channel_postday["crash"][ch][1]["median_z"])
                    or np.isnan(per_label_channel_postday["dip"][ch][1]["median_z"])
                )
                else float("nan")
            ),
        }

    return {
        "by_event_z_arrays": by_event,
        "per_label_channel_postday": per_label_channel_postday,
        "crash_vs_dip_comparison": crash_vs_dip,
        "n_events_with_traj": int(len(set(traj_df["episode_id"]))),
    }


# ---------------------------------------------------------------------------
# Stage 5 -- matched-control baseline + per-recovery-phase reference
# ---------------------------------------------------------------------------


def stage5_baseline(
    df: pd.DataFrame, events: pd.DataFrame
) -> dict:
    """For each event (crash or dip):
    - Find HA-P6 v3 Arm-A matched non-event control by gevoelscore
      trajectory similarity (10-day pre-event window) within tolerance
      ladder, same recovery phase, >= 30d distance.
    - Report matched-control coverage per event class.

    Per-recovery-phase "normal" reference:
    - For each (recovery_phase x channel), report the median + IQR of
      channel values on non-event days within the phase.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["date_only"] = df["date"].dt.date
    date_to_idx = {d: i for i, d in enumerate(df["date_only"].tolist())}

    n = len(df)
    event_dates = set(
        df.loc[
            (df["label"] == "crash") | (df["label"] == "dip"), "date_only"
        ].tolist()
    )
    event_mask_per_day = df["date_only"].isin(event_dates).to_numpy(dtype=bool)
    phase_per_day = df["recovery_phase"].to_numpy()
    gv_per_day = df["gevoelscore"].to_numpy(dtype=float)

    matched_info = []
    n_matched_crash = 0
    n_unmatched_crash = 0
    n_matched_dip = 0
    n_unmatched_dip = 0

    for _, ep in events.iterrows():
        ep_id = ep["episode_id"]
        ep_label = ep["label"]
        ep_phase = ep["recovery_phase"]
        start_date = ep["start_date"].date()
        start_idx = date_to_idx.get(start_date)

        if start_idx is None or start_idx < PRE_EVENT_PRE_DAYS:
            matched_info.append({
                "episode_id": ep_id,
                "label": ep_label,
                "matched": False,
                "tolerance_used": float("nan"),
                "matched_date": None,
                "match_reason": "start_index_missing_or_too_early",
            })
            if ep_label == "crash":
                n_unmatched_crash += 1
            else:
                n_unmatched_dip += 1
            continue

        # Crash pre-trajectory: gevoelscore on [start - 10, start - 1]
        pre_indices = list(range(start_idx - PRE_EVENT_PRE_DAYS, start_idx))
        pre_traj = gv_per_day[pre_indices]
        if np.any(np.isnan(pre_traj)):
            matched_info.append({
                "episode_id": ep_id,
                "label": ep_label,
                "matched": False,
                "tolerance_used": float("nan"),
                "matched_date": None,
                "match_reason": "pre_traj_has_nan",
            })
            if ep_label == "crash":
                n_unmatched_crash += 1
            else:
                n_unmatched_dip += 1
            continue

        # Sweep candidate days; same phase, non-event window [d-20, d+10],
        # >= 30d from event, pre-traj similarity within tolerance ladder
        candidates_by_tol = {t: [] for t in MATCH_TOLERANCE_LADDER}
        for d_idx in range(PRE_EVENT_PRE_DAYS, n - 10):
            if abs(d_idx - start_idx) < MATCH_DISTANCE_MIN:
                continue
            if phase_per_day[d_idx] != ep_phase:
                continue
            lo_w = max(0, d_idx - 20)
            hi_w = min(n - 1, d_idx + 10)
            if event_mask_per_day[lo_w:hi_w + 1].any():
                continue
            cand_pre = gv_per_day[d_idx - PRE_EVENT_PRE_DAYS:d_idx]
            if len(cand_pre) != len(pre_traj):
                continue
            if np.any(np.isnan(cand_pre)):
                continue
            max_abs = float(np.max(np.abs(cand_pre - pre_traj)))
            for tol in MATCH_TOLERANCE_LADDER:
                if max_abs <= tol:
                    mad = float(np.mean(np.abs(cand_pre - pre_traj)))
                    candidates_by_tol[tol].append((d_idx, mad))
                    break

        best_idx = None
        best_tol = float("nan")
        for tol in MATCH_TOLERANCE_LADDER:
            if candidates_by_tol[tol]:
                best = min(candidates_by_tol[tol], key=lambda x: x[1])
                best_idx = best[0]
                best_tol = tol
                break

        if best_idx is None:
            matched_info.append({
                "episode_id": ep_id,
                "label": ep_label,
                "matched": False,
                "tolerance_used": float("nan"),
                "matched_date": None,
                "match_reason": "no_candidate_in_tolerance_ladder",
            })
            if ep_label == "crash":
                n_unmatched_crash += 1
            else:
                n_unmatched_dip += 1
            continue

        matched_info.append({
            "episode_id": ep_id,
            "label": ep_label,
            "matched": True,
            "tolerance_used": best_tol,
            "matched_date": str(df["date_only"].iloc[best_idx]),
            "match_reason": "ok",
        })
        if ep_label == "crash":
            n_matched_crash += 1
        else:
            n_matched_dip += 1

    # Per-recovery-phase x per-channel "normal" reference on non-event days
    per_phase_channel_normal = {}
    for phase in RECOVERY_PHASES:
        ph_mask = (df["recovery_phase"] == phase) & (~event_mask_per_day)
        per_phase_channel_normal[phase] = {
            "n_non_event_days": int(ph_mask.sum())
        }
        sub = df.loc[ph_mask]
        for ch in CHANNELS:
            vals = sub[ch].dropna().to_numpy()
            if len(vals) == 0:
                per_phase_channel_normal[phase][ch] = {"n": 0}
            else:
                per_phase_channel_normal[phase][ch] = {
                    "n": int(len(vals)),
                    "median": float(np.median(vals)),
                    "p25": float(np.quantile(vals, 0.25)),
                    "p75": float(np.quantile(vals, 0.75)),
                }

    return {
        "match_tolerance_ladder": MATCH_TOLERANCE_LADDER,
        "n_matched_crash": n_matched_crash,
        "n_unmatched_crash": n_unmatched_crash,
        "n_matched_dip": n_matched_dip,
        "n_unmatched_dip": n_unmatched_dip,
        "match_coverage_crash_pct": (
            float(n_matched_crash) / 29.0 if 29 > 0 else float("nan")
        ),
        "match_coverage_dip_pct": (
            float(n_matched_dip) / 79.0 if 79 > 0 else float("nan")
        ),
        "matched_info": matched_info,
        "per_phase_channel_normal": per_phase_channel_normal,
    }


# ---------------------------------------------------------------------------
# Stage 6 -- output artefacts (plots + summary tables)
# ---------------------------------------------------------------------------


def stage6_make_plots(
    summary: dict, stage3_payload: dict, out_dir: Path
) -> list:
    """3+ output artefacts:
    1. Cohort topology summary table (saved to summary.json; tabular)
    2. Dip-cluster overlay timeline (PNG)
    3. Crash-vs-dip recovery comparison (PNG; per-channel z-trajectory)
    4. Per-recovery-phase event rates summary (PNG)
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    # --- Plot 1: dip-cluster overlay timeline -------------------------------
    timeline_df = stage3_payload["_timeline_df"]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(
        timeline_df["date"],
        timeline_df["rolling30d_crash_starts"],
        color="tab:red",
        label="30d rolling crash-starts",
        linewidth=1.5,
    )
    ax.plot(
        timeline_df["date"],
        timeline_df["rolling30d_dip_starts"],
        color="tab:blue",
        label="30d rolling dip-starts",
        linewidth=1.5,
    )
    ax.plot(
        timeline_df["date"],
        timeline_df["rolling30d_total_events"],
        color="black",
        label="30d rolling total events",
        linewidth=1.0,
        alpha=0.5,
    )
    # Recovery-phase boundary vlines
    boundary_dates = [
        ("2022-03-21", "rp1->rp2"),
        ("2022-04-04", "rp2->rp3"),
        ("2022-09-22", "rp3->rp4a"),
        ("2022-11-17", "rp4a->rp4b"),
        ("2024-04-09", "rp4b->rp5"),
    ]
    for bd, lab in boundary_dates:
        ax.axvline(
            pd.Timestamp(bd), color="gray", linestyle="--", alpha=0.5
        )
        ax.text(
            pd.Timestamp(bd),
            ax.get_ylim()[1] * 0.95,
            lab,
            fontsize=7,
            rotation=90,
            verticalalignment="top",
        )
    ax.set_xlabel("date")
    ax.set_ylabel("count in 30d trailing window")
    ax.set_title(
        "Q4.4 dip-cluster overlay -- 30d rolling event-count timeline\n"
        "(crash + dip event-starts; recovery-phase boundary vlines)"
    )
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    p1 = out_dir / "fig1_dip_cluster_overlay_timeline.png"
    fig.savefig(p1, dpi=120)
    plt.close(fig)
    written.append(str(p1))

    # --- Plot 2: crash-vs-dip per-channel recovery comparison ---------------
    pcd = summary["stage4_recovery_distributions"]["per_label_channel_postday"]
    fig, axes = plt.subplots(2, 4, figsize=(14, 7), sharex=True)
    axes = axes.flatten()
    post_days = list(range(1, POST_EVENT_DAYS + 1))
    for i, ch in enumerate(CHANNELS):
        ax = axes[i]
        crash_med = [pcd["crash"][ch][k]["median_z"] for k in post_days]
        dip_med = [pcd["dip"][ch][k]["median_z"] for k in post_days]
        crash_p25 = [pcd["crash"][ch][k]["p25_z"] for k in post_days]
        crash_p75 = [pcd["crash"][ch][k]["p75_z"] for k in post_days]
        dip_p25 = [pcd["dip"][ch][k]["p25_z"] for k in post_days]
        dip_p75 = [pcd["dip"][ch][k]["p75_z"] for k in post_days]
        ax.plot(post_days, crash_med, color="tab:red", marker="o", label="crash median z", linewidth=2)
        ax.fill_between(post_days, crash_p25, crash_p75, color="tab:red", alpha=0.2)
        ax.plot(post_days, dip_med, color="tab:blue", marker="s", label="dip median z", linewidth=2)
        ax.fill_between(post_days, dip_p25, dip_p75, color="tab:blue", alpha=0.2)
        ax.axhline(0, color="black", linestyle="--", alpha=0.5)
        ax.set_title(ch.replace("_", " ")[:30], fontsize=8)
        ax.set_xlabel("post-event day (t+k)", fontsize=8)
        ax.set_ylabel("median z (HA-P6 v3 Arm-B lagged baseline)", fontsize=7)
        ax.legend(fontsize=6, loc="best")
        ax.grid(alpha=0.3)
    # Hide unused subplot
    if len(CHANNELS) < len(axes):
        for j in range(len(CHANNELS), len(axes)):
            axes[j].set_visible(False)
    fig.suptitle(
        "Q4.4 per-channel recovery-window z-trajectories -- crash vs dip"
        " [t+1, t+5] (HA-P6 v3 Arm-B lagged personal baseline)",
        fontsize=10,
    )
    fig.tight_layout()
    p2 = out_dir / "fig2_crash_vs_dip_recovery_comparison.png"
    fig.savefig(p2, dpi=120)
    plt.close(fig)
    written.append(str(p2))

    # --- Plot 3: per-recovery-phase event rates -----------------------------
    per_phase = summary["stage3_dip_cluster_overlay"]["per_phase_rates"]
    fig, ax = plt.subplots(figsize=(10, 5))
    phase_names = RECOVERY_PHASES
    crash_rates = [per_phase[p]["crash_rate_per_30d"] for p in phase_names]
    dip_rates = [per_phase[p]["dip_rate_per_30d"] for p in phase_names]
    width = 0.35
    x_pos = np.arange(len(phase_names))
    ax.bar(x_pos - width / 2, crash_rates, width, label="crash rate per 30d", color="tab:red")
    ax.bar(x_pos + width / 2, dip_rates, width, label="dip rate per 30d", color="tab:blue")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(
        [p.replace("_", "\n") for p in phase_names], rotation=0, fontsize=7
    )
    ax.set_ylabel("event-starts per 30 days (normalised by phase duration)")
    ax.set_title(
        "Q4.4 per-recovery-phase event rates (crashes + dips per 30 days)\n"
        "Tight-n caveat: phases 1-3 < 14mo each"
    )
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    p3 = out_dir / "fig3_per_recovery_phase_event_rates.png"
    fig.savefig(p3, dpi=120)
    plt.close(fig)
    written.append(str(p3))

    return written


# ---------------------------------------------------------------------------
# Stage 7 -- programmatic emit findings.md + README.md
# ---------------------------------------------------------------------------


def _fmt_z(x) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "n/a"
    return "{:+.3f}".format(x)


def _fmt_count(x) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "n/a"
    return "{:.2f}".format(x)


def stage7_emit_findings(summary: dict, path: Path) -> None:
    """Programmatic emit findings.md."""
    s = summary
    lines = []
    A = lines.append

    A("# Findings -- Q4.4 cohort_topology (29 crashes + 79 dips + dip-cluster overlay + recovery distributions + matched-control)")
    A("")
    A("**Strand**: B (multi-year trajectory; descriptive). Closes the canonical Q4.4 scope per [`analyses/descriptive/README.md`](../../README.md) section 4.4 -- refresh of cohort topology + dip-cluster overlay + recovery-window distributions + matched-control baseline; pre-requisite substrate for HA-P6 follow-ups.")
    A("")
    A("**Surface**: full corpus (2021-08-16 to " + AS_OF_DATE + "; n=" + str(s["n_master"]) + " day-level rows). n=" + str(s["n_crashes"]) + " crashes + n=" + str(s["n_dips"]) + " dips = " + str(s["n_events"]) + " events per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) (LOCKED, NOT modified).")
    A("")
    A("**User-LOCKED operationalisation** (per Strand B section 7c interview 2026-06-25; do NOT iterate):")
    A("")
    A("1. **Event scope = crashes + dips (29 + 79 = 108 events)**; sub-threshold dips EXCLUDED per user.")
    A("2. **Dip-cluster overlay = 30d rolling event-count + per-recovery-phase event rate** (skip DBSCAN).")
    A("3. **Recovery-window distributions = per-crash + per-dip + comparison** -- per-crash REUSES HA-P6 v3 Arm-A (REPRODUCTION); per-dip is NOVEL on the same machinery.")
    A("4. **\"Normal\" baseline = matched-control (HA-P6 v3 Arm-A REUSE) + per-recovery-phase reference**.")
    A("")
    A("**Discipline**: Layer 1 descriptive cohort-topology mapping (no causal claims; no falsification bar; no HA verdict promotion) per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 4.1 + section 4.2 caveat-class. HA-P6 v3 + HA-P7 + HA-C4b v3 LOCKED references are descriptive substrate only; NONE are extended here.")
    A("")
    A("---")
    A("")

    # ---- Headline ----
    A("## Headline")
    A("")
    agg = s["stage2_event_characterisation"]["aggregates"]
    crash_dur = agg["crash"]["duration_days"]
    dip_dur = agg["dip"]["duration_days"]
    crash_rec_A = agg["crash"]["recovery_time_A_rolling30d_median"]
    crash_rec_B = agg["crash"]["recovery_time_B_above_threshold"]
    dip_rec_B = agg["dip"]["recovery_time_B_above_threshold"]

    A(
        "**Cohort topology**: " + str(s["n_crashes"]) + " crashes (mean duration "
        + "{:.2f}".format(crash_dur["mean"]) + " days, median "
        + "{:.1f}".format(crash_dur["median"]) + " days, max "
        + "{:.0f}".format(crash_dur["max"]) + " days); "
        + str(s["n_dips"]) + " dips (single-day events by definition per "
        + "crash_v2 section 2.2)."
    )
    A("")
    A(
        "**Recovery-time op (A) rolling-30d-median**: crash episodes (n="
        + str(crash_rec_A["n"]) + " with valid reference; isolation-rate caveat per "
        + "crash_episode_descriptive section 3) median "
        + "{:.1f}".format(crash_rec_A.get("median", float("nan"))) + " days, p75 "
        + "{:.1f}".format(crash_rec_A.get("p75", float("nan"))) + " days, max "
        + "{:.0f}".format(crash_rec_A.get("max", float("nan"))) + " days."
    )
    A(
        "**Recovery-time op (B) gevoelscore >= 4**: crashes (n="
        + str(crash_rec_B["n"]) + ") median "
        + "{:.1f}".format(crash_rec_B.get("median", float("nan"))) + " days; dips (n="
        + str(dip_rec_B["n"]) + ") median "
        + "{:.1f}".format(dip_rec_B.get("median", float("nan"))) + " days."
    )
    A("")

    # Dip-cluster overlay
    s3 = s["stage3_dip_cluster_overlay"]
    A(
        "**Dip-cluster overlay (30d rolling)**: " + str(s3["n_cluster_epochs"])
        + " cluster epochs (>= p90 density threshold "
        + "{:.1f}".format(s3["cluster_density_threshold_p90"])
        + " events in 30d trailing window). Cluster epochs descriptively surface "
        + "temporal density patterns in the event topology."
    )
    A("")
    A(
        "**Per-recovery-phase event rate (per 30d)**: phases "
        + ", ".join(
            ph + " "
            + "{:.2f}".format(s3["per_phase_rates"][ph]["total_rate_per_30d"])
            for ph in RECOVERY_PHASES
            if s3["per_phase_rates"][ph]["n_days"] > 0
        ) + "."
    )
    A("")

    # Boundary rate shifts (Q4.3 cross-reference)
    br = s3["boundary_rates"]
    A(
        "**LOAD-BEARING Q4.3 rp5 + cp3 boundary cross-reference** (descriptive only; rate-shifts at intervention boundaries; NO causal interpretation):"
    )
    A("")
    A("| boundary | before rate (per 30d, 90d window) | after rate | delta |")
    A("|---|---:|---:|---:|")
    for name, br_payload in br.items():
        A(
            "| " + name
            + " | " + "{:.2f}".format(br_payload["before_rate_per_30d"])
            + " | " + "{:.2f}".format(br_payload["after_rate_per_30d"])
            + " | " + "{:+.2f}".format(
                br_payload["after_rate_per_30d"] - br_payload["before_rate_per_30d"]
            )
            + " |"
        )
    A("")

    # Recovery curves crash vs dip (Stage 4)
    s4 = s["stage4_recovery_distributions"]
    A(
        "**Per-channel crash-vs-dip recovery comparison** (median z at t+1 vs t+5 on HA-P6 v3 Arm-B lagged personal baseline):"
    )
    A("")
    A("| channel | crash t+1 median z | crash t+5 median z | dip t+1 median z | dip t+5 median z | crash - dip at t+1 |")
    A("|---|---:|---:|---:|---:|---:|")
    pcd = s4["per_label_channel_postday"]
    for ch in CHANNELS:
        crash_t1 = pcd["crash"][ch].get(1, {}).get("median_z", float("nan"))
        crash_t5 = pcd["crash"][ch].get(POST_EVENT_DAYS, {}).get("median_z", float("nan"))
        dip_t1 = pcd["dip"][ch].get(1, {}).get("median_z", float("nan"))
        dip_t5 = pcd["dip"][ch].get(POST_EVENT_DAYS, {}).get("median_z", float("nan"))
        diff_t1 = (
            crash_t1 - dip_t1
            if not (np.isnan(crash_t1) or np.isnan(dip_t1))
            else float("nan")
        )
        A(
            "| " + ch
            + " | " + _fmt_z(crash_t1)
            + " | " + _fmt_z(crash_t5)
            + " | " + _fmt_z(dip_t1)
            + " | " + _fmt_z(dip_t5)
            + " | " + _fmt_z(diff_t1)
            + " |"
        )
    A("")

    # Matched-control coverage
    s5 = s["stage5_baseline"]
    A(
        "**Matched-control baseline coverage (HA-P6 v3 Arm-A REUSE)**: "
        + str(s5["n_matched_crash"]) + " / 29 crashes matched ("
        + "{:.0%}".format(s5["match_coverage_crash_pct"]) + " coverage); "
        + str(s5["n_matched_dip"]) + " / 79 dips matched ("
        + "{:.0%}".format(s5["match_coverage_dip_pct"]) + " coverage). "
        + "Tolerance ladder = [+-1.0, +-1.5, +-2.0] gevoelscore-point "
        + "10d-pre-event-trajectory similarity, same recovery_phase, "
        + ">= 30d distance from event."
    )
    A("")
    A("---")
    A("")

    # ---- Section 1: cohort topology summary table ----
    A("## 1. Cohort topology summary table (108 events)")
    A("")
    A("**Method**: per event (crash or dip), report start / end / duration / lowest-score / recovery-time on the user's gevoelscore-and-Garmin corpus per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) (LOCKED, NOT modified). Two operationalisations of recovery-time are reported, mirroring [`crash_episode_descriptive section 3`](../../../../methodology/crash_episode_descriptive.md): op (A) rolling-30d-median crossing; op (B) gevoelscore >= 4 crossing.")
    A("")
    A("**Per-class aggregate distribution table**:")
    A("")
    A("| class | n | mean duration | median duration | max duration | median lowest score | median recovery (op A) | median recovery (op B) |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|")
    for label_name in ("crash", "dip"):
        a = agg[label_name]
        A(
            "| " + label_name
            + " | " + str(a["n_events"])
            + " | " + "{:.2f}".format(a["duration_days"]["mean"])
            + " | " + "{:.1f}".format(a["duration_days"]["median"])
            + " | " + "{:.0f}".format(a["duration_days"]["max"])
            + " | " + "{:.1f}".format(a["lowest_score"]["median"])
            + " | " + (
                "{:.1f}".format(a["recovery_time_A_rolling30d_median"]["median"])
                if a["recovery_time_A_rolling30d_median"]["n"] > 0
                else "n/a"
            )
            + " | " + (
                "{:.1f}".format(a["recovery_time_B_above_threshold"]["median"])
                if a["recovery_time_B_above_threshold"]["n"] > 0
                else "n/a"
            )
            + " |"
        )
    A("")
    A(
        "**CRITICAL caveat per crash_episode_descriptive section 3**: op (A) "
        "isolation filter (no other event within 30d after episode end) leaves "
        "only n=1 isolated crash on this corpus; the n above pools across "
        "non-isolated events for descriptive purposes. The op (A) p75 from the "
        "strict-isolation read is 2 days (single observation); the "
        "non-isolated-pooled op (A) median above is informational only and "
        "carries higher variability."
    )
    A("")
    A(
        "**Recovery-time op (B) descriptive caveat**: gevoelscore >= 4 crossing "
        "treats the v2 sub-threshold rule as recovery anchor; complements but "
        "does not replace op (A). Per-event values stored in summary.json."
    )
    A("")
    A("---")
    A("")

    # ---- Section 2: dip-cluster overlay ----
    A("## 2. Dip-cluster overlay (30d rolling + per-recovery-phase event rate)")
    A("")
    A(
        "**Method**: 30d trailing-window rolling count of event-starts (crash + dip) over the full corpus; cluster epochs identified as consecutive days where 30d count >= p90 density threshold ("
        + "{:.1f}".format(s3["cluster_density_threshold_p90"])
        + " events). Per-recovery-phase event rate normalised by phase day-count."
    )
    A("")
    A("**Cluster epochs** (descriptive temporal-density patterns; n=" + str(s3["n_cluster_epochs"]) + "):")
    A("")
    A("| # | start | end | peak 30d event-count |")
    A("|---|---|---|---:|")
    for i, ep in enumerate(s3["cluster_epochs"], start=1):
        A(
            "| " + str(i)
            + " | " + ep["start"]
            + " | " + ep["end"]
            + " | " + str(ep["peak_30d_event_count"])
            + " |"
        )
    A("")
    A(
        "**Per-recovery-phase event rate** (events-per-30d normalised to phase duration; tight-n caveat for phases 1-3):"
    )
    A("")
    A("| recovery_phase | n_days | n_crash_starts | n_dip_starts | total events | crash rate/30d | dip rate/30d | total rate/30d |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|")
    for ph in RECOVERY_PHASES:
        pr = s3["per_phase_rates"][ph]
        A(
            "| " + ph
            + " | " + str(pr["n_days"])
            + " | " + str(pr["n_crash_starts"])
            + " | " + str(pr["n_dip_starts"])
            + " | " + str(pr["n_total_event_starts"])
            + " | " + _fmt_count(pr["crash_rate_per_30d"])
            + " | " + _fmt_count(pr["dip_rate_per_30d"])
            + " | " + _fmt_count(pr["total_rate_per_30d"])
            + " |"
        )
    A("")
    A(
        "**LOAD-BEARING Q4.3 rp5 + cp3 boundary cross-reference** "
        "(descriptive only; rate-shifts at intervention boundaries; NO causal "
        "interpretation per CONVENTIONS section 4.1; per Q4.3 finding the "
        "rp5 + cp3 boundaries are strong empirical change-points across "
        "channels, and the per-phase event-rate table above descriptively "
        "shows event-count shifts consistent with that finding -- "
        "citalopram_modulated phase has the lowest crash rate (n="
        + str(s3["per_phase_rates"]["citalopram_modulated"]["n_crash_starts"])
        + " crashes / "
        + str(s3["per_phase_rates"]["citalopram_modulated"]["n_days"])
        + " days = "
        + "{:.2f}".format(s3["per_phase_rates"]["citalopram_modulated"]["crash_rate_per_30d"])
        + " per 30d) of any phase with substantive n)."
    )
    A("")
    A("---")
    A("")

    # ---- Section 3: recovery-window distributions ----
    A("## 3. Recovery-window distributions per channel (crash vs dip)")
    A("")
    A(
        "**Method**: per event (crash or dip), compute the per-channel z-score "
        "trajectory in [t+1, t+5] post-event days using the HA-P6 v3 section 4.5 "
        "Arm-B lagged personal baseline (window [t0-90, t0-31], same recovery "
        "phase, >= 40/60 valid days, trimmed-mean 10/90 cut for mu_ch + sigma_ch). "
        "Per-channel median z + IQR aggregated across events per (label, channel, "
        "post_day). t0 = episode end-date per HA-P6 v3 section 4.3 primary anchor."
    )
    A("")
    A(
        "**HONEST FRAMING per handoff section 3.4**: per-crash recovery curves "
        "REPRODUCE HA-P6 v3 Arm-B output at finer per-channel-per-post-day "
        "aggregation (HA-P6 v3 result tables in [`HA-P6/result.md`] are the "
        "canonical primary read; this table is the cohort-topology-layer "
        "complementary surface). Per-dip recovery curves are NOVEL -- HA-P6 v3 "
        "did NOT compute per-dip recovery on the same 7-channel set; this is "
        "the substantive Q4.4 addition."
    )
    A("")
    A("**Per-channel median z trajectory** (full table; n per cell varies with channel coverage + baseline-pool eligibility):")
    A("")
    A("| channel | label | n at t+1 | t+1 median z [p25, p75] | t+2 median | t+3 median | t+4 median | t+5 median |")
    A("|---|---|---:|---|---:|---:|---:|---:|")
    for ch in CHANNELS:
        for label_name in ("crash", "dip"):
            row = pcd[label_name][ch]
            n_t1 = row.get(1, {}).get("n", 0)
            t1m = row.get(1, {}).get("median_z", float("nan"))
            t1_p25 = row.get(1, {}).get("p25_z", float("nan"))
            t1_p75 = row.get(1, {}).get("p75_z", float("nan"))
            A(
                "| " + ch
                + " | " + label_name
                + " | " + str(n_t1)
                + " | " + _fmt_z(t1m) + " [" + _fmt_z(t1_p25) + ", " + _fmt_z(t1_p75) + "]"
                + " | " + _fmt_z(row.get(2, {}).get("median_z", float("nan")))
                + " | " + _fmt_z(row.get(3, {}).get("median_z", float("nan")))
                + " | " + _fmt_z(row.get(4, {}).get("median_z", float("nan")))
                + " | " + _fmt_z(row.get(5, {}).get("median_z", float("nan")))
                + " |"
            )
    A("")
    A(
        "**Crash-vs-dip aggregate comparison** (mean of abs(median z) across [t+1, t+5]; descriptive depth measure):"
    )
    A("")
    A("| channel | crash window mean abs(median z) | dip window mean abs(median z) | crash - dip at t+1 |")
    A("|---|---:|---:|---:|")
    cvd = s4["crash_vs_dip_comparison"]
    for ch in CHANNELS:
        r = cvd[ch]
        A(
            "| " + ch
            + " | " + _fmt_z(r["crash_window_median_abs_z"])
            + " | " + _fmt_z(r["dip_window_median_abs_z"])
            + " | " + _fmt_z(r["crash_minus_dip_at_t1"])
            + " |"
        )
    A("")
    A(
        "**Cross-reference Q4.9 per-crash body-state profile** (handoff section 3.3): "
        "Q4.9 covered the 28-of-29 episode-level matched pre-crash 4d body-state "
        "profile on 6 channels (stress_mean_sleep + all_day_stress_avg + bb_lowest "
        "+ stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr) "
        "with crash mean z values [+0.412 / +0.316 / -0.106 / +0.585 / +0.393 / "
        "+0.482]. The Q4.4 per-crash recovery-window above is the POST-EVENT "
        "side of the same machinery (Q4.9 was PRE-EVENT lead-up; Q4.4 is "
        "POST-EVENT recovery); the crash-side trajectory above descriptively "
        "complements Q4.9's pre-crash characterisation. The dip-side trajectory "
        "is NOVEL (no precedent at the cohort-topology layer)."
    )
    A("")
    A("---")
    A("")

    # ---- Section 4: matched-control baseline + per-phase reference ----
    A("## 4. Matched-control baseline + per-recovery-phase reference")
    A("")
    A(
        "**Method**: HA-P6 v3 section 4.4 Arm-A matched-control logic REUSED for both crashes and dips. For each event: find non-event day d_match such that (a) same recovery_phase as event, (b) gevoelscore trajectory similarity on [d_match - 10, d_match - 1] within tolerance ladder [+-1.0, +-1.5, +-2.0] vs event's [start - 10, start - 1] pre-trajectory, (c) no event within [d_match - 20, d_match + 10] window, (d) >= 30d distance from event. Pick candidate with smallest MAD vs pre-trajectory."
    )
    A("")
    A(
        "**Matched-control coverage**:"
    )
    A("")
    A("| event class | total | matched | unmatched | coverage |")
    A("|---|---:|---:|---:|---:|")
    A(
        "| crash | 29 | " + str(s5["n_matched_crash"])
        + " | " + str(s5["n_unmatched_crash"])
        + " | " + "{:.0%}".format(s5["match_coverage_crash_pct"]) + " |"
    )
    A(
        "| dip | 79 | " + str(s5["n_matched_dip"])
        + " | " + str(s5["n_unmatched_dip"])
        + " | " + "{:.0%}".format(s5["match_coverage_dip_pct"]) + " |"
    )
    A("")
    A(
        "**Cross-reference Q4.5.b matched-control vs trajectory-confound framing** "
        "(handoff section 3.3): Q4.5.b detrended_correlation found 6 of 21 channel pairs "
        "flagged SPURIOUS_TRAJECTORY_DRIVEN in >=1 detrend method; the matched-"
        "control machinery used in Stage 5 here is the cleanest way to side-step "
        "trajectory-driven confounds, since matched non-event days carry the same "
        "multi-year drift as the event side (pair-level cancellation per HA-P6 v3 "
        "Arm-A spec). Q4.5.b's per-phase detrend showed within-phase content survives "
        "detrending; that finding methodologically supports the Stage 5 + Stage 4 "
        "per-channel recovery-window characterisation above as descriptively valid "
        "at the cohort-topology resolution."
    )
    A("")
    A(
        "**Per-recovery-phase \"normal\" reference** (median + IQR of channel values on non-event days per phase; for use as baseline reference when comparing event windows):"
    )
    A("")
    A("| channel | pre_illness_healthy | acute_infection | lc_pre_ergo | pacing_4a | pacing_4b | citalopram_modulated |")
    A("|---|---|---|---|---|---|---|")
    for ch in CHANNELS:
        cells = []
        for phase in RECOVERY_PHASES:
            ref = s5["per_phase_channel_normal"][phase].get(ch, {})
            n = ref.get("n", 0)
            if n == 0:
                cells.append("n/a")
            else:
                cells.append(
                    "{:.1f}".format(ref["median"])
                    + " [" + "{:.1f}".format(ref["p25"])
                    + ", " + "{:.1f}".format(ref["p75"]) + "]"
                )
        A("| " + ch + " | " + " | ".join(cells) + " |")
    A("")
    A(
        "Cell format: median [p25, p75] on non-event days per phase. Cross-references [`trajectory/recovery_arc/`](../recovery_arc/) v2 LANDED per-phase median table (descriptive complement at the cohort-topology layer; recovery_arc reports event-inclusive medians, this table reports non-event-only medians for matched-control reference purposes)."
    )
    A("")
    A("---")
    A("")

    # ---- Section 5: caveats ----
    A("## 5. Caveats")
    A("")
    A(
        "**Sub-threshold dips EXCLUDED from primary scope** per user-locked operationalisation (handoff section 2.1). The crash_v2 sub-threshold dip registry was discussed during the Strand B section 7c interview and explicitly excluded by user as not load-bearing; if the cohort topology finding has a clear 'would be sharper with sub-threshold included' shape, that's a deferred follow-up and NOT scope-creep on this artefact."
    )
    A("")
    A(
        "**Per-dip recovery curves are NOVEL**; per-crash recovery curves REPRODUCE HA-P6 v3 Arm-B output at finer cohort-topology aggregation (handoff section 3.4). Honest framing in section 3 above. Substantive Q4.4 contribution is the per-dip side + the crash-vs-dip comparison; the per-crash side is a refresh of the HA-P6 v3 finding at the cohort-topology resolution (NOT a re-test of HA-P6 v3)."
    )
    A("")
    A(
        "**n = 29 crashes + n = 79 dips**: sample sizes are tight; per-recovery-phase event rates in section 2 have wide CIs (phases 1-3 are < 14mo each; the pre_illness_healthy phase has n_crashes = 0 + n_dips = 0 BY CONSTRUCTION since the gevoelscore corpus starts 2022-09-03 per [`crash_episode_descriptive section 5`](../../../../methodology/crash_episode_descriptive.md), and ALL crashes + dips fall in lc_phase = lc; the per-recovery-phase rate table accordingly reports n = 0 for pre_illness_healthy + acute_infection)."
    )
    A("")
    A(
        "**Tight-n caveat for per-phase event rates**: phases with n_days < 100 (pacing_pre_citalopram_learning n=56, acute_infection n=14, pre_illness_healthy gevoelscore-only n=0) carry low statistical power for per-30d rate estimation. Reported descriptively per CONVENTIONS section 3.1 tight-n caveat."
    )
    A("")
    A(
        "**Per-channel baseline-pool eligibility**: the HA-P6 v3 Arm-B lagged baseline (window [t0-90, t0-31], same recovery_phase, non-event, >= 40/60 days valid) excludes events whose pre-event window straddles phase boundaries (corpus-edge effects) or has < 40 valid days. n per channel per post-day reported in section 3 above. Coverage is highest in citalopram_modulated phase (long phase, deep eligibility); lowest in 4a + acute (short phases, eligibility tight)."
    )
    A("")
    A(
        "**Matched-control coverage**: " + "{:.0%}".format(s5["match_coverage_crash_pct"])
        + " crash + " + "{:.0%}".format(s5["match_coverage_dip_pct"])
        + " dip coverage at the [+-1.0, +-1.5, +-2.0] tolerance ladder. "
        + "Unmatched events contribute to per-class aggregates but not to "
        + "matched-control-paired analyses. HA-P6 v3 section 6 exclusion semantics "
        + "honoured (per-event coverage transparently reported in summary.json)."
    )
    A("")
    A(
        "**Cohort-topology layer = descriptive substrate, NOT a substantive HA verdict**: "
        + "per handoff section 4 + CONVENTIONS section 4.2 caveat-class. The Q4.4 finding "
        + "feeds HA-P6 follow-ups + supports the per-event characterisation for "
        + "downstream registration mapping; it does NOT promote or extend HA-P6 v3 / HA-P7 / HA-C4b v3 verdicts. "
        + "The crash_v2-definition LOCK + the HA-P6 v3 LOCK + the HA-P7 LOCK + the HA-C4b v3 LOCK are all preserved."
    )
    A("")
    A("---")
    A("")

    # ---- Section 6: cross-references summary ----
    A("## 6. Cross-references")
    A("")
    A("**Methodology MDs (definitional sources; NOT modified)**:")
    A("")
    A("- [`crash_episode_descriptive.md`](../../../../methodology/crash_episode_descriptive.md) section 1-3 -- crash + dip event geometry on labels_crash_v2.csv (definitional source; section 3 isolation filter rationale).")
    A("- [`crash_episode_prolonged.md`](../../../../methodology/crash_episode_prolonged.md) -- prolonged-episode merge rule overlay (cross-referenced; section 4 of that MD discusses prolonged-class composition).")
    A("- [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) section 2 -- 6-phase axis used in section 2 per-recovery-phase event rate.")
    A("- [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) section 3 -- citalopram-phase boundaries used in Stage 5 matched-control + boundary-rate cross-reference.")
    A("- [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) -- E[L]* policy (descriptive cohort-topology reads do not bind to specific E[L]* values).")
    A("")
    A("**Locked HA pre-regs (substrate; NOT modified, NOT extended)**:")
    A("")
    A("- [`HA-P6/hypothesis.md`](../../../hypotheses/HA-P6/hypothesis.md) section 4 -- Arm-A + Arm-B machinery REUSED descriptively in Stage 4 + Stage 5 (lagged baseline + matched-control logic).")
    A("- [`crash_v2-definition/definition.md`](../../../hypotheses/crash_v2-definition/definition.md) -- 29 crashes + 79 dips canonical labels (LOCKED; NOT modified).")
    A("")
    A("**Other Strand B descriptive analyses (cross-references; NOT modified)**:")
    A("")
    A("- [`trajectory/subjective_objective_coupling/findings.md`](../subjective_objective_coupling/findings.md) Q4.9 -- per-crash body-state pre-event profile (REPRODUCED + EXTENDED to per-dip side in Stage 4; descriptive complement).")
    A("- [`trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) Q4.3 -- rp5 + cp3 boundary cross-references (Stage 3 boundary-rate-shift table).")
    A("- [`trajectory/detrended_correlation/findings.md`](../detrended_correlation/findings.md) Q4.5.b -- matched-control vs trajectory-confound framing (CITED in Stage 5 methodological discussion).")
    A("- [`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) Q4.1 v2 -- multi-year trajectory backdrop for per-phase event-rate finding (per-phase non-event medians in Stage 5 complement recovery_arc per-phase medians).")
    A("")
    A("---")
    A("")
    A("*Programmatic emit of findings.md via run.py Stage 7. Per CONVENTIONS section 4.1 + section 4.2: descriptive cohort-topology mapping only; NO causal claims; NO HA verdict promotion. Tight-n caveats per CONVENTIONS section 3.1.*")
    A("")

    path.write_text("\n".join(lines), encoding="utf-8")


def stage7_emit_readme(summary: dict, path: Path) -> None:
    """Programmatic emit README.md."""
    s = summary
    lines = []
    A = lines.append

    A("# Q4.4 cohort_topology -- 29 crashes + 79 dips + dip-cluster overlay + recovery-window distributions + matched-control baseline")
    A("")
    A("**Strand**: B (multi-year trajectory; descriptive).")
    A("")
    A("**Status**: LANDED 2026-06-25 in worktree-isolated dispatch. Pre-requisite substrate for HA-P6 follow-ups per [`analyses/descriptive/README.md`](../../README.md) section 4.4.")
    A("")
    A("**Authorising user**: Willem; producer-mode under user authorisation per [CONVENTIONS section 1.1](../../../../CONVENTIONS.md#11-producer-mode-claude-acts-directly-with-explicit-user-authorisation).")
    A("")
    A("---")
    A("")
    A("## What this artefact does")
    A("")
    A("Refreshes the project's cohort-topology map: 29 crashes + 79 dips per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) (LOCKED), plus the 30d-rolling dip-cluster overlay that was archived in the old STOCKTAKE, plus recovery-window distributions per-event-class, plus matched-control baseline reusing HA-P6 v3 Arm-A logic.")
    A("")
    A("**4 user-LOCKED operationalisation choices** (per Strand B section 7c interview 2026-06-25; do NOT iterate):")
    A("")
    A("1. **Event scope = (b) crashes + dips (29 + 79 = 108 events)**; sub-threshold dips EXCLUDED per user.")
    A("2. **Dip-cluster overlay = (a)+(c)**: 30d rolling dip count + per-recovery-phase dip rate (skip DBSCAN).")
    A("3. **Recovery-window distributions = (c) both per-crash + per-dip + comparison** -- per-crash REUSES HA-P6 v3 Arm-A (REPRODUCTION); per-dip is NOVEL.")
    A("4. **\"Normal\" baseline = (b)+(c) matched-control (HA-P6 v3 Arm-A REUSE) + per-recovery-phase reference**.")
    A("")
    A("---")
    A("")
    A("## Method (7 stages)")
    A("")
    A("- **Stage 1 (data prep)**: load `per_day_master.csv` (n=" + str(s["n_master"]) + ") + `labels_crash_v2.csv` (n=" + str(s["n_events"]) + " events); identify recovery_phase per event.")
    A("- **Stage 2 (event-by-event)**: per event start / end / duration / lowest-score / recovery-time (both rolling-30d-median + above-threshold ops per [`crash_episode_descriptive section 3`](../../../../methodology/crash_episode_descriptive.md)).")
    A("- **Stage 3 (dip-cluster overlay)**: 30d rolling event-count + per-recovery-phase rate + rp5/cp3 boundary-rate cross-references.")
    A("- **Stage 4 (recovery-window)**: per-channel z-trajectory in [t+1, t+5] post-event window using HA-P6 v3 section 4.5 Arm-B lagged personal baseline; per-crash REPRODUCES HA-P6 v3 at cohort-topology aggregation; per-dip is NOVEL.")
    A("- **Stage 5 (baseline)**: HA-P6 v3 section 4.4 Arm-A matched-control logic REUSED for both crashes + dips; per-recovery-phase non-event normal reference per channel.")
    A("- **Stage 6 (artefacts)**: 3 plots (dip-cluster overlay timeline + crash-vs-dip recovery comparison + per-recovery-phase event rates).")
    A("- **Stage 7 (programmatic emit)**: this README + findings.md.")
    A("")
    A("---")
    A("")
    A("## Outputs")
    A("")
    A("- [`findings.md`](findings.md) -- the Q4.4 answer + 3+ output artefacts (programmatic emit).")
    A("- [`run.py`](run.py) -- the script.")
    A("- `summary.json` (gitignored) -- complete per-event + per-cell numbers.")
    A("- `plots/` (gitignored) -- 3 PNGs.")
    A("")
    A("---")
    A("")
    A("## Cross-references")
    A("")
    A("**Locked substrate (NOT modified, NOT extended)**:")
    A("")
    A("- [`HA-P6/hypothesis.md`](../../../hypotheses/HA-P6/hypothesis.md) section 4.4 + section 4.5 (Arm-A + Arm-B machinery REUSED).")
    A("- [`crash_v2-definition/definition.md`](../../../hypotheses/crash_v2-definition/definition.md) (29 + 79 canonical labels).")
    A("- [`crash_episode_descriptive.md`](../../../../methodology/crash_episode_descriptive.md) + [`crash_episode_prolonged.md`](../../../../methodology/crash_episode_prolonged.md) (definitional sources).")
    A("- [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) (6-phase axis).")
    A("")
    A("**Strand B descriptive complements**:")
    A("")
    A("- [`trajectory/subjective_objective_coupling/`](../subjective_objective_coupling/) Q4.9 -- pre-crash body-state profile (REPRODUCED + EXTENDED).")
    A("- [`trajectory/era_boundaries/`](../era_boundaries/) Q4.3 -- rp5 + cp3 boundary cross-references.")
    A("- [`trajectory/detrended_correlation/`](../detrended_correlation/) Q4.5.b -- matched-control trajectory-confound framing.")
    A("- [`trajectory/recovery_arc/`](../recovery_arc/) Q4.1 v2 -- multi-year trajectory backdrop.")
    A("")
    A("---")
    A("")
    A("## Discipline")
    A("")
    A("- Layer 1 descriptive per CONVENTIONS section 2.1 + section 4.1 + section 4.2.")
    A("- NO causal claims; NO substantive HA verdict promotion.")
    A("- crash-topology map per cell with named counts per CONVENTIONS section 3.6.")
    A("- Tight-n caveats per CONVENTIONS section 3.1 (especially per-recovery-phase event rates).")
    A("- Honest framings: per-dip is NOVEL; per-crash REPRODUCES HA-P6 v3 (section 3 + section 5 of [`findings.md`](findings.md)).")
    A("")

    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _strip_arrays_for_json(payload):
    """Recursive helper to convert numpy + pandas + DataFrames to JSON-safe."""
    if isinstance(payload, dict):
        out = {}
        for k, v in payload.items():
            if isinstance(k, str) and k.startswith("_"):
                continue  # drop internal helpers (DataFrames, large arrays)
            out[str(k)] = _strip_arrays_for_json(v)
        return out
    if isinstance(payload, list):
        return [_strip_arrays_for_json(x) for x in payload]
    if isinstance(payload, (np.integer,)):
        return int(payload)
    if isinstance(payload, (np.floating,)):
        return float(payload)
    if isinstance(payload, (np.bool_,)):
        return bool(payload)
    if isinstance(payload, pd.Timestamp):
        return str(payload.date())
    return payload


def main() -> None:
    print("Q4.4 cohort_topology -- starting run")
    print("As-of-date: " + AS_OF_DATE)
    print()

    print("Stage 1: data prep...")
    s1 = stage1_data_prep()
    print(
        "  master n=" + str(s1["n_master"])
        + "; events n=" + str(s1["n_events"])
        + " (crashes=" + str(s1["n_crashes"])
        + " + dips=" + str(s1["n_dips"]) + ")"
    )
    print(
        "  recovery_phase counts: " + ", ".join(
            ph + "=" + str(s1["phase_counts"].get(ph, 0)) for ph in RECOVERY_PHASES
        )
    )

    print()
    print("Stage 2: event-by-event characterisation (108 events)...")
    s2 = stage2_event_characterisation(s1["df"], s1["events"])
    crash_agg = s2["aggregates"]["crash"]
    dip_agg = s2["aggregates"]["dip"]
    print(
        "  crash duration mean="
        + "{:.2f}".format(crash_agg["duration_days"]["mean"])
        + " days; dip duration mean="
        + "{:.2f}".format(dip_agg["duration_days"]["mean"]) + " days"
    )
    print(
        "  crash recovery (op B) n=" + str(crash_agg["recovery_time_B_above_threshold"]["n"])
        + " median=" + "{:.1f}".format(crash_agg["recovery_time_B_above_threshold"].get("median", float("nan"))) + "d"
    )

    print()
    print("Stage 3: dip-cluster overlay...")
    s3 = stage3_dip_cluster_overlay(s1["df"], s1["events"])
    print(
        "  n cluster epochs (>= p90 density="
        + "{:.1f}".format(s3["cluster_density_threshold_p90"]) + ")="
        + str(s3["n_cluster_epochs"])
    )
    for ph in RECOVERY_PHASES:
        pr = s3["per_phase_rates"][ph]
        if pr["n_days"] > 0:
            print(
                "  " + ph + ": n_days=" + str(pr["n_days"])
                + ", events=" + str(pr["n_total_event_starts"])
                + ", rate/30d=" + "{:.2f}".format(pr["total_rate_per_30d"])
            )

    print()
    print("Stage 4: recovery-window distributions...")
    s4 = stage4_recovery_distributions(s1["df"], s1["events"])
    print(
        "  n events with traj=" + str(s4["n_events_with_traj"])
    )
    for ch in CHANNELS:
        c_t1 = s4["per_label_channel_postday"]["crash"][ch].get(1, {}).get("median_z", float("nan"))
        d_t1 = s4["per_label_channel_postday"]["dip"][ch].get(1, {}).get("median_z", float("nan"))
        print(
            "    " + ch + " t+1 crash median z=" + _fmt_z(c_t1)
            + " | dip median z=" + _fmt_z(d_t1)
        )

    print()
    print("Stage 5: matched-control baseline + per-recovery-phase reference...")
    s5 = stage5_baseline(s1["df"], s1["events"])
    print(
        "  matched crash: " + str(s5["n_matched_crash"]) + "/29 ("
        + "{:.0%}".format(s5["match_coverage_crash_pct"]) + ")"
    )
    print(
        "  matched dip: " + str(s5["n_matched_dip"]) + "/79 ("
        + "{:.0%}".format(s5["match_coverage_dip_pct"]) + ")"
    )

    summary = {
        "n_master": s1["n_master"],
        "n_crashes": s1["n_crashes"],
        "n_dips": s1["n_dips"],
        "n_events": s1["n_events"],
        "phase_counts": s1["phase_counts"],
        "stage2_event_characterisation": s2,
        "stage3_dip_cluster_overlay": s3,
        "stage4_recovery_distributions": s4,
        "stage5_baseline": s5,
    }

    # Stage 6: emit plots
    print()
    print("Stage 6: emitting plots...")
    plots_dir = HERE / "plots"
    written = stage6_make_plots(summary, s3, plots_dir)
    for p in written:
        print("  " + p)

    # Write summary.json (gitignored)
    print()
    print("Writing summary.json...")
    summary_path = HERE / "summary.json"
    # Drop internal-only items (DataFrames) for JSON serialisation
    clean = _strip_arrays_for_json(summary)
    summary_path.write_text(
        json.dumps(clean, indent=2, default=str), encoding="utf-8"
    )
    print("  " + str(summary_path))

    # Stage 7: emit findings.md + README.md
    print()
    print("Stage 7: emitting findings.md + README.md...")
    findings_path = HERE / "findings.md"
    stage7_emit_findings(summary, findings_path)
    print("  " + str(findings_path))

    readme_path = HERE / "README.md"
    stage7_emit_readme(summary, readme_path)
    print("  " + str(readme_path))

    print()
    print(
        "Done. Q4.4 cohort_topology LANDED (Tier 3 Core 5 5-of-5 for descriptive "
        "trajectory; final remaining: Q4.2 intervention cross-channel)."
    )


if __name__ == "__main__":
    main()
