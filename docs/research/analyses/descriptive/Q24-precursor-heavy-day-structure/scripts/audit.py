"""Q24 precursor: heavy-day structural audit.

Descriptive audit of the heavy-day corpus structure to inform Q24
methodology-MD design decisions (unit of analysis, window length,
overlap policy, drift caveats).

Outputs are written to ../output/ and consumed by the sibling audit.md
descriptive card. This script is idempotent and re-runnable.

Frame: LC-era stratum (lc_phase == 'lc'), matches HA-C4c/HA-C4cp stratum.
Heavy-day definition: exertion_class_lagged_lcera in {heavy, very_heavy}.
"""
import os
from pathlib import Path
import pandas as pd
import numpy as np

DATA_PATH = Path(os.environ.get("GEVOELSCORE_DATA_PATH", "C:/Users/Gebruiker/Documents/gevoelscore-data"))
INPUT = DATA_PATH / "unified" / "per_day_master.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEAVY_CLASSES = {"heavy", "very_heavy"}
GAP_TOLERANCES = [0, 1, 2]  # contiguous / <=1 gap / <=2 gap
OVERLAP_WINDOWS = [3, 5, 10, 14]  # days-before and days-after to check

# Intensity stratifications applied to episode + overlap structural metrics.
# Each key -> the mask-column name to use for "is_heavy" in downstream logic.
INTENSITY_STRATA = {
    "combined": "is_heavy",              # heavy OR very_heavy (union) -- primary
    "heavy_only": "is_heavy_only",       # heavy class value only (excludes very_heavy)
    "very_heavy_only": "is_very_heavy",  # very_heavy only
}


def load_lc_stratum():
    df = pd.read_csv(INPUT, parse_dates=["date"])
    df = df[df["lc_phase"] == "lc"].copy().reset_index(drop=True)
    df["is_heavy"] = df["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)
    df["is_heavy_only"] = df["exertion_class_lagged_lcera"] == "heavy"
    df["is_very_heavy"] = df["exertion_class_lagged_lcera"] == "very_heavy"
    df["is_crash"] = df["is_crash"].fillna(False).astype(bool)
    return df


def counts_by_year_quarter(df):
    rows = []
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)
    for period_col, label in [("year", "year"), ("quarter", "quarter")]:
        agg = df.groupby(period_col).agg(
            days_total=("date", "count"),
            heavy_days=("is_heavy", "sum"),
            very_heavy_days=("is_very_heavy", "sum"),
            heavy_rate=("is_heavy", "mean"),
        ).reset_index()
        agg["period_type"] = label
        agg = agg.rename(columns={period_col: "period"})
        rows.append(agg)
    return pd.concat(rows, ignore_index=True)


def counts_by_recovery_phase(df):
    if "recovery_phase" not in df.columns:
        return pd.DataFrame()
    return df.groupby("recovery_phase", dropna=False).agg(
        days_total=("date", "count"),
        heavy_days=("is_heavy", "sum"),
        very_heavy_days=("is_very_heavy", "sum"),
        heavy_rate=("is_heavy", "mean"),
    ).reset_index()


def rolling_rate(df, window_days=90):
    daily = df.set_index("date")["is_heavy"].astype(float)
    roll = daily.rolling(f"{window_days}D").mean()
    out = pd.DataFrame({"date": roll.index, "heavy_rate_90d": roll.values})
    return out


def threshold_drift(df):
    """Track eff_exertion_rank_lagged_lcera value at the heavy cutoff.

    On days that ARE heavy, what is the lowest rank observed? The
    'heavy' cutoff should be stable at rank~0.75 if the lagged-baseline
    is stationary. Drift shows up as the min-rank-on-heavy-days trending.
    """
    if "eff_exertion_rank_lagged_lcera" not in df.columns:
        return pd.DataFrame()
    heavy_days = df[df["is_heavy"]].copy()
    heavy_days["year_quarter"] = heavy_days["date"].dt.to_period("Q").astype(str)
    drift = heavy_days.groupby("year_quarter").agg(
        heavy_n=("date", "count"),
        rank_min=("eff_exertion_rank_lagged_lcera", "min"),
        rank_median=("eff_exertion_rank_lagged_lcera", "median"),
        rank_p25=("eff_exertion_rank_lagged_lcera", lambda x: x.quantile(0.25)),
        rank_p75=("eff_exertion_rank_lagged_lcera", lambda x: x.quantile(0.75)),
    ).reset_index()
    return drift


def label_episodes(df, gap_tolerance, mask_col="is_heavy"):
    """Assign an episode_id to runs of heavy days separated by <=gap_tolerance non-heavy days.

    Returns a copy of df with columns: episode_id_gap{N}, episode_last_day_gap{N}.
    episode_id is NaN on non-heavy days.
    """
    heavy_mask = df[mask_col].values
    n = len(df)
    ep_id = np.full(n, np.nan)
    ep_last = np.zeros(n, dtype=bool)
    current_id = 0
    i = 0
    while i < n:
        if not heavy_mask[i]:
            i += 1
            continue
        # start of a new episode
        current_id += 1
        # extend while heavy or within gap_tolerance non-heavy days
        j = i
        last_heavy_idx = i
        while j < n:
            if heavy_mask[j]:
                last_heavy_idx = j
                j += 1
            else:
                # look ahead: is there a heavy day within gap_tolerance?
                lookahead_end = min(j + gap_tolerance + 1, n)
                found = False
                for k in range(j, lookahead_end):
                    if heavy_mask[k]:
                        found = True
                        break
                if found:
                    j += 1  # skip the non-heavy day, keep going
                else:
                    break
        # label all heavy days in [i, last_heavy_idx] as this episode
        for k in range(i, last_heavy_idx + 1):
            if heavy_mask[k]:
                ep_id[k] = current_id
        ep_last[last_heavy_idx] = True
        i = last_heavy_idx + 1
    out = df.copy()
    out[f"episode_id_gap{gap_tolerance}"] = ep_id
    out[f"episode_last_day_gap{gap_tolerance}"] = ep_last
    return out


def episode_stats(df, gap_tolerance):
    ep_col = f"episode_id_gap{gap_tolerance}"
    heavy_only = df[df[ep_col].notna()].copy()
    lengths_days = heavy_only.groupby(ep_col).size()  # count of heavy days per episode
    # episode span = last_heavy_date - first_heavy_date + 1 (includes gap-tolerated non-heavy days)
    spans = heavy_only.groupby(ep_col)["date"].agg(["min", "max"])
    spans["span_days"] = (spans["max"] - spans["min"]).dt.days + 1
    return {
        "gap_tolerance": gap_tolerance,
        "n_episodes": int(lengths_days.count()),
        "n_single_day_episodes": int((lengths_days == 1).sum()),
        "n_multi_day_episodes": int((lengths_days > 1).sum()),
        "single_day_rate": float((lengths_days == 1).mean()),
        "heavy_days_in_lengths_hist": lengths_days.value_counts().sort_index().to_dict(),
        "span_days_median": float(spans["span_days"].median()),
        "span_days_mean": float(spans["span_days"].mean()),
        "span_days_p90": float(spans["span_days"].quantile(0.90)),
        "span_days_max": int(spans["span_days"].max()),
    }


def overlap_density(df, window_days, mask_col="is_heavy"):
    """For each heavy day, does another heavy day sit within [-window, +window]?

    Two independent checks (pm_window and post_window scanned separately
    so a preceding heavy day cannot short-circuit the post-window scan):
    - has_other_heavy_in_pm_window: any other heavy day in [-window, +window]
    - has_other_heavy_in_post_window: any heavy day in [+1, +window]
    """
    dates = df["date"].values
    heavy_mask = df[mask_col].values
    heavy_indices = np.where(heavy_mask)[0]
    n = len(df)
    other_in_window = 0
    other_after = 0
    for idx in heavy_indices:
        d0 = dates[idx]
        # scan +-window bidirectionally
        pm_hit = False
        for j in range(n):
            if j == idx or not heavy_mask[j]:
                continue
            delta = (dates[j] - d0) / np.timedelta64(1, "D")
            if -window_days <= delta <= window_days:
                pm_hit = True
                break
        if pm_hit:
            other_in_window += 1
        # scan post-window only (forward)
        post_hit = False
        for j in range(idx + 1, n):
            delta = (dates[j] - d0) / np.timedelta64(1, "D")
            if delta > window_days:
                break
            if heavy_mask[j] and 1 <= delta <= window_days:
                post_hit = True
                break
        if post_hit:
            other_after += 1
    n_heavy = len(heavy_indices)
    return {
        "window_days": window_days,
        "n_heavy_total": int(n_heavy),
        "n_heavy_with_other_in_pm_window": int(other_in_window),
        "n_heavy_with_other_in_post_window": int(other_after),
        "share_with_other_in_pm_window": float(other_in_window / max(n_heavy, 1)),
        "share_with_other_in_post_window": float(other_after / max(n_heavy, 1)),
        "n_heavy_clean_pm_window": int(n_heavy - other_in_window),
        "n_heavy_clean_post_window": int(n_heavy - other_after),
    }


def cross_stratum_overlap_density(df, trigger_mask_col, scan_mask_col, window_days):
    """For each trigger-mask day, is any scan-mask day in [+1, +window]?

    Enables asymmetric checks: e.g. trigger on very_heavy but scan for any
    heavy day (combined) in the post-window -- the actionable question for
    Q24's intensity-stratified sensitivity arm ("if we trigger only on
    very_heavy, how many episodes survive a strict no-heavy-in-post-window
    filter?").
    """
    dates = df["date"].values
    trigger_mask = df[trigger_mask_col].values
    scan_mask = df[scan_mask_col].values
    trigger_indices = np.where(trigger_mask)[0]
    n = len(df)
    contaminated = 0
    for idx in trigger_indices:
        d0 = dates[idx]
        for j in range(idx + 1, n):
            delta = (dates[j] - d0) / np.timedelta64(1, "D")
            if delta > window_days:
                break
            if scan_mask[j] and 1 <= delta <= window_days:
                contaminated += 1
                break
    n_trigger = len(trigger_indices)
    return {
        "trigger": trigger_mask_col,
        "scan": scan_mask_col,
        "window_days": window_days,
        "n_trigger_days": int(n_trigger),
        "n_contaminated_post": int(contaminated),
        "share_contaminated_post": float(contaminated / max(n_trigger, 1)),
        "n_clean_post": int(n_trigger - contaminated),
    }


def episode_overlap_density(df, gap_tolerance, window_days, mask_col="is_heavy"):
    """For each episode's last-day, does another heavy day sit in [+1, +window]?"""
    last_col = f"episode_last_day_gap{gap_tolerance}"
    heavy_mask = df[mask_col].values
    dates = df["date"].values
    last_day_mask = df[last_col].values
    last_day_indices = np.where(last_day_mask)[0]
    contaminated_post = 0
    for idx in last_day_indices:
        d0 = dates[idx]
        for j in range(idx + 1, len(df)):
            delta = (dates[j] - d0) / np.timedelta64(1, "D")
            if delta > window_days:
                break
            if heavy_mask[j]:
                contaminated_post += 1
                break
    n_eps = len(last_day_indices)
    return {
        "gap_tolerance": gap_tolerance,
        "window_days": window_days,
        "n_episodes": int(n_eps),
        "n_episodes_with_next_heavy_in_post_window": int(contaminated_post),
        "share_contaminated_post": float(contaminated_post / max(n_eps, 1)),
        "n_episodes_clean_post_window": int(n_eps - contaminated_post),
    }


def main():
    df = load_lc_stratum()
    print(f"[stratum] LC-era rows: {len(df)}; heavy days: {int(df['is_heavy'].sum())}; very_heavy: {int(df['is_very_heavy'].sum())}")

    # 1. Counts by year / quarter
    counts_yq = counts_by_year_quarter(df)
    counts_yq.to_csv(OUTPUT_DIR / "counts_by_year_quarter.csv", index=False)

    # 2. Counts by recovery phase
    counts_rp = counts_by_recovery_phase(df)
    if not counts_rp.empty:
        counts_rp.to_csv(OUTPUT_DIR / "counts_by_recovery_phase.csv", index=False)

    # 3. Rolling 90-day rate
    roll = rolling_rate(df, window_days=90)
    roll.to_csv(OUTPUT_DIR / "rolling_heavy_rate_90d.csv", index=False)

    # 4. Threshold drift
    drift = threshold_drift(df)
    if not drift.empty:
        drift.to_csv(OUTPUT_DIR / "threshold_drift_by_quarter.csv", index=False)

    # 5. Episode structure under 3 gap tolerances -- run for each intensity stratum.
    # Combined = union of heavy + very_heavy (primary); heavy_only + very_heavy_only
    # allow post-hoc contrast against the combined trajectory reads.
    episode_summary_rows = []
    df_with_eps = df.copy()
    for stratum_label, mask_col in INTENSITY_STRATA.items():
        # rename per-stratum episode columns to avoid collision across strata
        for gap in GAP_TOLERANCES:
            df_with_eps = label_episodes(df_with_eps, gap, mask_col=mask_col)
            # move the columns aside under stratum-tagged names so all three
            # strata can co-exist in df_with_eps for later per-stratum lookups
            df_with_eps[f"episode_id_gap{gap}_{stratum_label}"] = df_with_eps[f"episode_id_gap{gap}"]
            df_with_eps[f"episode_last_day_gap{gap}_{stratum_label}"] = df_with_eps[f"episode_last_day_gap{gap}"]
            stats = episode_stats(df_with_eps, gap)
            stats["stratum"] = stratum_label
            episode_summary_rows.append({k: v for k, v in stats.items() if k != "heavy_days_in_lengths_hist"})
            # length histogram to its own CSV (per stratum + per gap)
            hist = pd.DataFrame(list(stats["heavy_days_in_lengths_hist"].items()),
                                columns=["episode_length_days", "n_episodes"])
            hist["stratum"] = stratum_label
            hist.to_csv(OUTPUT_DIR / f"episode_length_hist_gap{gap}_{stratum_label}.csv", index=False)
    pd.DataFrame(episode_summary_rows).to_csv(OUTPUT_DIR / "episode_summary.csv", index=False)

    # 6. Overlap density (per heavy day) -- per stratum
    overlap_rows = []
    for stratum_label, mask_col in INTENSITY_STRATA.items():
        for win in OVERLAP_WINDOWS:
            row = overlap_density(df, win, mask_col=mask_col)
            row["stratum"] = stratum_label
            overlap_rows.append(row)
    pd.DataFrame(overlap_rows).to_csv(OUTPUT_DIR / "overlap_density_per_heavy_day.csv", index=False)

    # 7. Episode-level overlap -- per stratum
    # Restore per-stratum episode label columns to the generic name before each call
    # since episode_overlap_density looks for episode_last_day_gap{N}.
    episode_overlap_rows = []
    for stratum_label, mask_col in INTENSITY_STRATA.items():
        for gap in GAP_TOLERANCES:
            df_with_eps[f"episode_last_day_gap{gap}"] = df_with_eps[f"episode_last_day_gap{gap}_{stratum_label}"]
            for win in OVERLAP_WINDOWS:
                row = episode_overlap_density(df_with_eps, gap, win, mask_col=mask_col)
                row["stratum"] = stratum_label
                episode_overlap_rows.append(row)
    pd.DataFrame(episode_overlap_rows).to_csv(OUTPUT_DIR / "overlap_density_per_episode.csv", index=False)

    # 7b. Cross-stratum overlap: very_heavy-triggered, combined-scanned.
    # Actionable for the intensity-stratified sensitivity arm: if we ONLY
    # trigger on very_heavy days, how many survive a strict no-heavy-in-post-
    # window filter (where "heavy" means the combined heavy+very_heavy set)?
    cross_rows = []
    for win in OVERLAP_WINDOWS:
        cross_rows.append(cross_stratum_overlap_density(df, "is_very_heavy", "is_heavy", win))
        cross_rows.append(cross_stratum_overlap_density(df, "is_heavy_only", "is_heavy", win))
    pd.DataFrame(cross_rows).to_csv(OUTPUT_DIR / "overlap_density_cross_stratum.csv", index=False)

    # 8. Emit condensed summary for the audit.md card
    summary = {
        "n_lc_days": len(df),
        "date_min": str(df["date"].min().date()),
        "date_max": str(df["date"].max().date()),
        "n_heavy": int(df["is_heavy"].sum()),
        "n_very_heavy": int(df["is_very_heavy"].sum()),
        "heavy_rate": float(df["is_heavy"].mean()),
        "n_crash_days": int(df["is_crash"].sum()),
        "exertion_class_missingness": int(df["exertion_class_lagged_lcera"].isna().sum()),
    }
    pd.DataFrame([summary]).to_csv(OUTPUT_DIR / "corpus_summary.csv", index=False)

    print("\n[write] outputs in", OUTPUT_DIR)
    for f in sorted(OUTPUT_DIR.glob("*.csv")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
