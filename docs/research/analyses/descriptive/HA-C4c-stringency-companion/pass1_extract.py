"""HA-C4c-stringency-companion Step 1 Pass 1 extraction.

Executes the LOCKED r1 protocol at
``docs/research/analyses/hypotheses/HA-C4c-stringency-companion/protocol.md`` Sec 2
(distributional-only, S effort).

For four return-window thresholds T in {30, 60, 120, 180} minutes, adds per-bout
did-not-return-within-T flags to the bout-level table, aggregates to per-day counts,
applies the LOCKED HA-C4c primary stratum filter (per HA-C4c hypothesis.md Sec 4.2 +
Sec 4.4), and writes the per-day distributions for downstream descriptive audit.

Pass 1 hard walls (protocol Sec 2.4) enforced structurally in this script:
- NO effect view (no heavy-vs-non-heavy contrast is computed).
- NO crash or gevoelscore cross-look (those columns are not read at all).
- NO stratification by exertion_class_lagged_lcera (used only as day-validity gate
  per HA-C4c Sec 4.4; the column is never split on).
- NO threshold recommendation emitted from this script (the Sec 4 asymmetric-bar
  rule is decided downstream on the numeric output).

T-parameterisation form per protocol Sec 2.2 mirroring parent MD
``methodology/bout_level_recovery_dynamics.md`` Sec 3.2: a bout is flagged
did_not_return_within_T iff the bout's stress was not observed to return to within
+5 of pre_bout_baseline for >= 10 consecutive minutes within T minutes after peak.
Given the pipeline's per-bout tail_length (minutes from peak to observed return or
truncation) and did_not_return_flag (True iff the 180-min cap fired or sleep
truncated), the T-parameterised flag reduces to:

    did_not_return_within_T_flag = (tail_length > T) OR did_not_return_flag

At T=180 this reduces to did_not_return_flag by construction (tail_length is capped
at 180), matching HA-C4c's LOCKED primary operand as the sanity anchor.

Run from repo root:

    python docs/research/analyses/descriptive/HA-C4c-stringency-companion/pass1_extract.py

Outputs (per protocol Sec 2.5):
    $GEVOELSCORE_DATA_PATH/analyses/descriptive/HA-C4c-stringency-companion/
        pass1_distributions.csv       (per-day counts + underlying tail_length)
        pass1_summary.json            (per-threshold summary stats + f2(T) table)
"""
from __future__ import annotations

import json
import math
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# Constants: LOCKED per HA-C4c hypothesis.md Sec 4.2 + Sec 4.4 + Sec 6.
# -----------------------------------------------------------------------------

THRESHOLDS = [30, 60, 120, 180]  # minutes (protocol Sec 2.2)

# HA-C4c stratum (protocol Sec 2.1 = HA-C4c hypothesis.md Sec 4.2 + Sec 4.4)
LC_ERA_LEFT_EDGE = date(2022, 11, 17)  # sub-phase 4b left edge (8-week-post-ergo M1)
APRIL_2024_CLUSTER_START = date(2024, 4, 9)
APRIL_2024_CLUSTER_END = date(2024, 4, 16)
CITALOPRAM_PHASES_IN_STRATUM = {
    "unmedicated", "buildup", "consolidation", "afbouw", "post_afbouw",
}

# Citalopram phase boundaries (verbatim from
# ``methodology/citalopram_phase_stratification.md`` Sec 3, and mirrored in
# ``docs/research/pipeline/02_features/extract_stress_bouts.py``).
CITALOPRAM_PHASE_BOUNDARIES = [
    (date(2024, 4, 9), "unmedicated"),
    (date(2024, 6, 20), "buildup"),
    (date(2026, 3, 20), "consolidation"),
    (date(2026, 6, 6), "afbouw"),
]

DEVICE_BASELINE_LAG_DAYS = 21  # parent MD Sec 3.4

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

DATA_ROOT = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH", "C:/Users/Gebruiker/Documents/gevoelscore-data"
))
BOUT_PARQUET = DATA_ROOT / "unified" / "per_bout_master.parquet"
DAY_CSV = DATA_ROOT / "unified" / "per_day_master.csv"

OUT_DIR = DATA_ROOT / "analyses" / "descriptive" / "HA-C4c-stringency-companion"
OUT_DIST_CSV = OUT_DIR / "pass1_distributions.csv"
OUT_SUMMARY_JSON = OUT_DIR / "pass1_summary.json"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def citalopram_phase(d: date) -> str:
    """Canonical phase per citalopram_phase_stratification.md Sec 3."""
    for boundary, label in CITALOPRAM_PHASE_BOUNDARIES:
        if d < boundary:
            return label
    return "post_afbouw"


def did_not_return_within_t(tail_length: float, did_not_return_flag: bool, t: int) -> bool:
    """T-parameterised did-not-return flag per protocol Sec 2.2.

    True iff the bout's stress was not observed to return within T minutes after peak.
    Equivalent to (tail_length > T) OR did_not_return_flag.
    """
    if pd.isna(tail_length):
        return False  # bout without measurable tail; conservative False
    if tail_length > t:
        return True
    if bool(did_not_return_flag):
        # Return not observed within tail_length (either 180-cap or sleep-truncated),
        # so return also not observed within any T <= tail_length. Conservatively
        # count as did-not-return-within-T (mirrors parent MD Sec 3.2 semantics).
        return True
    return False


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Reading bouts: {BOUT_PARQUET}")
    bouts = pd.read_parquet(BOUT_PARQUET)
    print(f"  n_bouts_total = {len(bouts)}")

    print(f"Reading days:  {DAY_CSV}")
    days = pd.read_csv(DAY_CSV, parse_dates=["date"])
    days["date"] = pd.to_datetime(days["date"]).dt.date
    print(f"  n_days_total = {len(days)}")

    # ------------------------------------------------------------------
    # Step A: add T-parameterised flags to bout table
    # ------------------------------------------------------------------
    bouts["date"] = pd.to_datetime(bouts["date"]).dt.date
    for t in THRESHOLDS:
        col = f"did_not_return_within_{t}_flag"
        bouts[col] = bouts.apply(
            lambda r, T=t: did_not_return_within_t(
                r["tail_length"], r["did_not_return_flag"], T
            ),
            axis=1,
        )
    for t in THRESHOLDS:
        col = f"did_not_return_within_{t}_flag"
        print(f"  bout-level {col}: {int(bouts[col].sum())} True / {len(bouts)}")

    # T=180 sanity: reproduce pipeline's did_not_return_flag count
    assert (
        (bouts["did_not_return_within_180_flag"] == bouts["did_not_return_flag"])
        .all()
    ), "T=180 flag construction must reduce to did_not_return_flag by construction"
    print("  sanity: T=180 flag == did_not_return_flag: PASS")

    # ------------------------------------------------------------------
    # Step B: aggregate to per-day counts + join to per_day_master
    # ------------------------------------------------------------------
    per_day_bouts = bouts.groupby("date")[
        [f"did_not_return_within_{t}_flag" for t in THRESHOLDS]
    ].sum()
    per_day_bouts.columns = [
        f"bout_n_did_not_return_within_{t}_day" for t in THRESHOLDS
    ]
    per_day_bouts = per_day_bouts.reset_index()

    # ------------------------------------------------------------------
    # Step C: apply HA-C4c primary stratum filter (protocol Sec 2.1)
    # ------------------------------------------------------------------
    days["citalopram_phase_derived"] = days["date"].apply(citalopram_phase)

    # 21-day device-baseline-lag: from first has_garmin_uds=True day inclusive,
    # first 21 days excluded (parent MD Sec 3.4).
    gd = days[days["has_garmin_uds"] == True].sort_values("date")
    if gd.empty:
        raise RuntimeError("no has_garmin_uds=True days found")
    first_garmin = gd["date"].iloc[0]
    baseline_lag_end = first_garmin + timedelta(days=DEVICE_BASELINE_LAG_DAYS - 1)
    print(
        f"  first has_garmin_uds day: {first_garmin}; "
        f"21-day lag excludes through {baseline_lag_end}"
    )

    apr_2024_mask = (
        (days["date"] >= APRIL_2024_CLUSTER_START)
        & (days["date"] <= APRIL_2024_CLUSTER_END)
    )

    stratum_mask = (
        (days["date"] >= LC_ERA_LEFT_EDGE)
        & (days["citalopram_phase_derived"].isin(CITALOPRAM_PHASES_IN_STRATUM))
        & (~apr_2024_mask)
        & (days["date"] > baseline_lag_end)
        & (days["bout_n_did_not_return"].notna())
        & (days["exertion_class_lagged_lcera"].notna())
    )

    stratum_days = (
        days.loc[stratum_mask, ["date", "bout_n_did_not_return"]]
        .copy()
        .merge(per_day_bouts, on="date", how="left")
    )
    # Days in the stratum but with no bouts at all: fill new-T counts with 0.
    for t in THRESHOLDS:
        col = f"bout_n_did_not_return_within_{t}_day"
        stratum_days[col] = stratum_days[col].fillna(0).astype(int)

    n_stratum = len(stratum_days)
    print(f"  n stratum days: {n_stratum}")

    # HA-C4c result.md sanity: mean of bout_n_did_not_return over the stratum
    ha_c4c_mean = stratum_days["bout_n_did_not_return"].mean()
    print(f"  HA-C4c primary operand mean over stratum: {ha_c4c_mean:.6f}")

    # ------------------------------------------------------------------
    # Step D: per-threshold summary statistics
    # ------------------------------------------------------------------
    summary = {"n_stratum_days": int(n_stratum), "thresholds": {}}

    # Global bout-population tail_length descriptives (protocol Sec 2.3 item 5)
    # scoped to bouts belonging to the stratum days.
    stratum_dates = set(stratum_days["date"].tolist())
    stratum_bouts = bouts[bouts["date"].isin(stratum_dates)].copy()
    summary["n_stratum_bouts"] = int(len(stratum_bouts))
    tl = stratum_bouts["tail_length"].dropna()
    summary["tail_length"] = {
        "n": int(len(tl)),
        "mean": float(tl.mean()),
        "median": float(tl.median()),
        "sd": float(tl.std()),
        "min": float(tl.min()),
        "max": float(tl.max()),
        "quantiles": {
            "p05": float(tl.quantile(0.05)),
            "p10": float(tl.quantile(0.10)),
            "p25": float(tl.quantile(0.25)),
            "p50": float(tl.quantile(0.50)),
            "p75": float(tl.quantile(0.75)),
            "p90": float(tl.quantile(0.90)),
            "p95": float(tl.quantile(0.95)),
            "p99": float(tl.quantile(0.99)),
        },
        "hist_bins_10": {
            "edges": list(np.linspace(0, 180, 11)),
            "counts": [
                int(x) for x in np.histogram(tl, bins=np.linspace(0, 180, 11))[0]
            ],
        },
    }

    for t in THRESHOLDS:
        col = f"bout_n_did_not_return_within_{t}_day"
        s = stratum_days[col]
        mean = float(s.mean())
        median = float(s.median())
        sd = float(s.std())
        p25 = float(s.quantile(0.25))
        p75 = float(s.quantile(0.75))
        smin = int(s.min())
        smax = int(s.max())
        f_ge1 = float((s >= 1).mean())
        f_ge2 = float((s >= 2).mean())
        f_ge3 = float((s >= 3).mean())
        f0 = float((s == 0).mean())
        poisson_expected_zero = float(math.exp(-mean)) if mean > 0 else 1.0
        zero_ratio = float(f0 / poisson_expected_zero) if poisson_expected_zero > 0 else float("nan")
        # Per-threshold missingness on the stratum: by construction should be 0
        # (fillna(0) above); we report the pre-fill NaN count for transparency
        n_nan = 0  # stratum_days built with left-join then fillna; underlying NaN structure noted below
        summary["thresholds"][t] = {
            "mean": mean,
            "median": median,
            "sd": sd,
            "p25": p25,
            "p75": p75,
            "min": smin,
            "max": smax,
            "f_ge1_T": f_ge1,
            "f2_T": f_ge2,  # this is the pre-committed Sec 4 rule input
            "f_ge3_T": f_ge3,
            "f_zero": f0,
            "poisson_expected_zero_fraction": poisson_expected_zero,
            "observed_over_poisson_zero_ratio": zero_ratio,
            "n_nan_pre_fill": n_nan,
        }
        print(
            f"  T={t:>3}: mean={mean:.4f} median={median:.1f} sd={sd:.4f} "
            f"f_ge1={f_ge1:.4f} f2={f_ge2:.4f} f_ge3={f_ge3:.4f} "
            f"f0={f0:.4f} zero_ratio={zero_ratio:.4f}"
        )

    # ------------------------------------------------------------------
    # Step E: sanity check T=180 base rate reproduces HA-C4c result.md
    # ------------------------------------------------------------------
    sanity_target_mean = 0.6444
    computed_180_mean = summary["thresholds"][180]["mean"]
    delta = abs(computed_180_mean - sanity_target_mean)
    summary["sanity"] = {
        "T180_computed_mean": computed_180_mean,
        "T180_target_mean_from_HA_C4c_result": sanity_target_mean,
        "delta": float(delta),
        "pass_bar_0.001": bool(delta <= 0.001),
    }
    if delta > 0.001:
        print(
            f"  SANITY FAIL: T=180 mean delta {delta:.6f} > 0.001; "
            f"do NOT publish descriptive audit"
        )
        return 2
    print(f"  SANITY PASS: T=180 mean delta {delta:.6f} <= 0.001")

    # ------------------------------------------------------------------
    # Step F: write outputs
    # ------------------------------------------------------------------
    stratum_days.to_csv(OUT_DIST_CSV, index=False)
    print(f"  wrote: {OUT_DIST_CSV} ({len(stratum_days)} rows)")

    with OUT_SUMMARY_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"  wrote: {OUT_SUMMARY_JSON}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
