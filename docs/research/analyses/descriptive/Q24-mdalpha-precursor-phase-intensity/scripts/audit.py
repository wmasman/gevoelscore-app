"""Q24 MD-alpha precursor: phase-stratified + intensity-stratified data-availability audit.

Descriptive Stage -1 audit extension of parent Q24 precursor
(../Q24-precursor-heavy-day-structure/audit.md). Answers the MD-alpha
(post_heavy_day_pacing_learning.md LOCKED r1 2026-07-16) section 7
data-availability audit hooks upfront before Stage D execution:

  7.1 heavy-episode-end counts per recovery_phase
  7.2 intensity x phase cross-tab
  7.3 per-outcome coverage per phase per-k (k=0..10)
  7.4 per-outcome coverage per intensity stratum per-k
  7.5 per-contrast cell n values after strict-clean overlap + pool split +
      per-outcome validity + detrended-arm 15-valid-pre-point rule

Inheritance-only: all inherited machinery (LC-era filter, heavy definition,
episode-end unit at gap=0, matched-ordinary comparator, windows, overlap
policy, pool split) points at parent Q24 methodology MD
(post_heavy_day_compensatory_rest.md LOCKED r1) plus parent Stage -1 audit
(sibling folder ../Q24-precursor-heavy-day-structure/audit.md LOCKED r1).

Outputs are written to ../output/ and consumed by the sibling audit.md
descriptive card. Script is idempotent and re-runnable.

Frame: LC-era stratum (lc_phase == 'lc'), matches parent Stage -1 audit
n=1524 rows and combined episode-ends n=314.
"""
import os
from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_SEED = 20260716  # unused for descriptive audit; declared per parent Stage -1 convention

DATA_PATH = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    "C:/Users/Gebruiker/Documents/gevoelscore-data",
))
INPUT = DATA_PATH / "unified" / "per_day_master.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEAVY_CLASSES = {"heavy", "very_heavy"}

# MD-alpha section 3.1 phase axis (4 buckets, ordered).
PHASE_ORDER = [
    "lc_pre_ergo",
    "pacing_pre_citalopram_learning",
    "pacing_habit_established",
    "citalopram_modulated",
]

# MD-alpha section 3.2 activity outcome family (verbatim from parent MD section 6.1).
# active_sec is converted to active_min = active_sec / 60 at compute time.
ACTIVITY_OUTCOMES_RAW = [
    "total_steps",
    "effective_exertion_min",
    "vigorous_min",
    "active_sec",
]
# Coverage / mean tables report active_min as the reader-facing outcome name.
OUTCOME_REPORT_NAMES = {
    "total_steps": "total_steps",
    "effective_exertion_min": "effective_exertion_min",
    "vigorous_min": "vigorous_min",
    "active_sec": "active_min",  # active_sec / 60
}

# Parent MD windows (section 5.1); MD-alpha inherits.
WINDOWS = [3, 5, 10]

# Overlap policies (parent MD section 5.2). Strict-clean = no other heavy in [+1, +w];
# inclusive = all episode-ends retained.
OVERLAP_POLICIES = ["strict_clean", "inclusive"]

# Pool split (parent MD section 3.5). Compensatory-success = no crash in [+1, +w];
# compensatory-failure = crash in [+1, +w].
POOLS = ["compensatory_success", "compensatory_failure"]

# Parent MD section 7.11 detrended-arm eligibility rule.
DETREND_PRE_WINDOW_DAYS = 30
DETREND_MIN_VALID_POINTS = 15

# Intensity strata for section 7.4 (MD-alpha).
INTENSITY_STRATA = ["combined", "heavy_only", "very_heavy_only"]


def load_lc_stratum():
    df = pd.read_csv(INPUT, parse_dates=["date"])
    df = df[df["lc_phase"] == "lc"].copy().reset_index(drop=True)
    df["is_heavy"] = df["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)
    df["is_heavy_only"] = df["exertion_class_lagged_lcera"] == "heavy"
    df["is_very_heavy"] = df["exertion_class_lagged_lcera"] == "very_heavy"
    df["is_crash"] = df["is_crash"].fillna(False).astype(bool)
    # Report-facing active_min derived from active_sec (parent MD 6.1 convention).
    df["active_min"] = df["active_sec"] / 60.0
    return df


def label_episode_ends_gap0(df, mask_col):
    """Return integer indices of episode-end days (last day of a contiguous heavy run)
    under the supplied mask column. gap=0 contiguous per parent Stage -1 audit section 4.
    """
    heavy_mask = df[mask_col].values
    n = len(df)
    ends = []
    i = 0
    while i < n:
        if not heavy_mask[i]:
            i += 1
            continue
        # extend while contiguous heavy
        j = i
        while j + 1 < n and heavy_mask[j + 1]:
            j += 1
        ends.append(j)
        i = j + 1
    return np.array(ends, dtype=int)


def last_day_class(df, end_idx):
    """Intensity class label on the episode-end day itself."""
    val = df["exertion_class_lagged_lcera"].iloc[end_idx]
    return val


# ------------- section 2: phase episode counts (MD-alpha 3.1 / 7.1) -------------


def phase_episode_counts(df):
    ends_combined = label_episode_ends_gap0(df, "is_heavy")
    rows = []
    phase_col = df["recovery_phase"].values
    date_col = df["date"].values
    for phase in PHASE_ORDER:
        mask = np.array([phase_col[i] == phase for i in ends_combined])
        rows.append({
            "phase": phase,
            "n_episode_ends_combined_gap0": int(mask.sum()),
        })
    total = int(len(ends_combined))
    rows.append({"phase": "all_lc_era", "n_episode_ends_combined_gap0": total})
    return pd.DataFrame(rows), ends_combined


# ------------- section 3: intensity x phase cross-tab (MD-alpha 6.3 / 7.2) -------------


def intensity_phase_crosstab(df, ends_combined):
    rows = []
    for end_idx in ends_combined:
        rows.append({
            "phase": df["recovery_phase"].iloc[end_idx],
            "intensity_last_day": df["exertion_class_lagged_lcera"].iloc[end_idx],
        })
    cross = pd.DataFrame(rows)
    # Fixed cell order for reproducibility.
    tab = cross.pivot_table(index="intensity_last_day", columns="phase",
                            aggfunc=len, fill_value=0)
    # Force ordered columns / rows.
    tab = tab.reindex(columns=PHASE_ORDER, fill_value=0)
    tab = tab.reindex(index=["heavy", "very_heavy"], fill_value=0)
    tab["all_phases"] = tab.sum(axis=1)
    total_row = pd.DataFrame([tab.sum(axis=0).values],
                             columns=tab.columns, index=["all_intensities"])
    out = pd.concat([tab, total_row])
    out.index.name = "intensity_last_day"
    return out.reset_index()


# ------------- section 4: per-outcome per-phase per-k coverage (MD-alpha 7.3) -------------


def coverage_per_phase(df, ends_combined, k_max=10):
    """For each (phase, outcome, k in 0..k_max), report n_episode_ends whose day+k
    row has a non-null value on the outcome column.
    Missing = NaN per CONVENTIONS section 5 zero-vs-NaN discipline. No fillna(0).
    """
    n_rows = len(df)
    rows = []
    for phase in PHASE_ORDER:
        phase_ends = [i for i in ends_combined if df["recovery_phase"].iloc[i] == phase]
        n_phase_ends = len(phase_ends)
        for outcome_raw in ACTIVITY_OUTCOMES_RAW:
            report_name = OUTCOME_REPORT_NAMES[outcome_raw]
            src_col = "active_min" if outcome_raw == "active_sec" else outcome_raw
            for k in range(k_max + 1):
                n_valid = 0
                for end_idx in phase_ends:
                    target = end_idx + k
                    if target >= n_rows:
                        continue
                    val = df[src_col].iloc[target]
                    if pd.notna(val):
                        n_valid += 1
                rows.append({
                    "phase": phase,
                    "outcome": report_name,
                    "k": k,
                    "n_episode_ends_in_phase": n_phase_ends,
                    "n_valid_outcome_at_d_plus_k": n_valid,
                    "n_nan_outcome_at_d_plus_k": n_phase_ends - n_valid,
                })
    return pd.DataFrame(rows)


# ------------- section 5: strict-clean + pool split sample floors (MD-alpha 7.5) -------------


def compute_strict_clean_mask(df, ends_combined, window):
    """Return boolean array indicating which episode-ends satisfy strict-clean overlap:
    no other heavy day in [end+1, end+window] (using combined heavy mask per parent
    section 5.2 + parent Stage -1 audit section 5 cross-stratum rule).
    """
    heavy_mask = df["is_heavy"].values
    n = len(df)
    out = []
    for end_idx in ends_combined:
        clean = True
        for k in range(1, window + 1):
            j = end_idx + k
            if j >= n:
                # window runs off the end of the corpus -> not strict-clean
                clean = False
                break
            if heavy_mask[j]:
                clean = False
                break
        out.append(clean)
    return np.array(out, dtype=bool)


def compute_pool_masks(df, ends_combined, window):
    """Return (success_mask, failure_mask) arrays per parent MD section 3.5.
    Compensatory-success: no crash in [end+1, end+window].
    Compensatory-failure: crash in [end+1, end+window].
    Episode-ends whose window runs past the corpus end are excluded from both
    (undefined pool assignment).
    """
    crash_mask = df["is_crash"].values
    n = len(df)
    success = []
    failure = []
    for end_idx in ends_combined:
        end_of_window = end_idx + window
        if end_of_window >= n:
            success.append(False)
            failure.append(False)
            continue
        crash_in_win = False
        for k in range(1, window + 1):
            if crash_mask[end_idx + k]:
                crash_in_win = True
                break
        success.append(not crash_in_win)
        failure.append(crash_in_win)
    return np.array(success, dtype=bool), np.array(failure, dtype=bool)


def strict_clean_pool_floors(df, ends_combined):
    """MD-alpha section 7.5 deliverable.
    Per (phase x window x overlap x pool) cell: n_episode_ends surviving the filters.
    """
    rows = []
    phase_of_end = np.array([df["recovery_phase"].iloc[i] for i in ends_combined])
    for window in WINDOWS:
        clean_mask = compute_strict_clean_mask(df, ends_combined, window)
        succ_mask, fail_mask = compute_pool_masks(df, ends_combined, window)
        for overlap in OVERLAP_POLICIES:
            for pool in POOLS:
                if pool == "compensatory_success":
                    pool_mask = succ_mask
                else:
                    pool_mask = fail_mask
                if overlap == "strict_clean":
                    combined_mask = clean_mask & pool_mask
                else:
                    # inclusive: no strict-clean filter, only pool
                    combined_mask = pool_mask
                for phase in PHASE_ORDER:
                    phase_mask = phase_of_end == phase
                    n = int((combined_mask & phase_mask).sum())
                    rows.append({
                        "phase": phase,
                        "window_days": window,
                        "overlap_policy": overlap,
                        "pool": pool,
                        "n_episode_ends": n,
                        "below_n10_descriptive_floor": bool(n < 10),
                    })
    return pd.DataFrame(rows)


# ------------- section 6: detrended-arm sample floors (MD-alpha 7.5 detrend clause) -------------


def detrended_arm_floors(df, ends_combined):
    """Parent MD section 7.11: episode retains detrended-arm eligibility only if the
    30d pre-window has at least 15 valid data points on the outcome column.
    Report per (phase, outcome) the number of episodes satisfying that rule.
    """
    n_rows = len(df)
    rows = []
    for phase in PHASE_ORDER:
        phase_ends = [i for i in ends_combined if df["recovery_phase"].iloc[i] == phase]
        n_phase_ends = len(phase_ends)
        for outcome_raw in ACTIVITY_OUTCOMES_RAW:
            report_name = OUTCOME_REPORT_NAMES[outcome_raw]
            src_col = "active_min" if outcome_raw == "active_sec" else outcome_raw
            n_pass = 0
            for end_idx in phase_ends:
                # 30d pre-window: [end_idx - 30, end_idx - 1] inclusive
                pre_start = max(0, end_idx - DETREND_PRE_WINDOW_DAYS)
                pre_end = end_idx  # exclusive
                if pre_end - pre_start < DETREND_MIN_VALID_POINTS:
                    continue
                pre_vals = df[src_col].iloc[pre_start:pre_end]
                if pre_vals.notna().sum() >= DETREND_MIN_VALID_POINTS:
                    n_pass += 1
            rows.append({
                "phase": phase,
                "outcome": report_name,
                "n_episode_ends_in_phase": n_phase_ends,
                "n_episodes_detrend_eligible": n_pass,
                "n_episodes_detrend_dropped": n_phase_ends - n_pass,
                "pre_window_days": DETREND_PRE_WINDOW_DAYS,
                "min_valid_points_required": DETREND_MIN_VALID_POINTS,
            })
    return pd.DataFrame(rows)


# ------------- section 7: intensity-stratum per-outcome coverage (MD-alpha 7.4) -------------


def intensity_stratum_coverage(df, ends_combined, k_max=10):
    """Per (intensity_stratum, outcome, k) coverage on episode-ends. Intensity is
    read on the episode-end day itself (last-day class per MD-alpha section 6.3).
    """
    n_rows = len(df)
    rows = []
    intensity_of_end = np.array([df["exertion_class_lagged_lcera"].iloc[i] for i in ends_combined])
    for stratum in INTENSITY_STRATA:
        if stratum == "combined":
            stratum_mask = np.ones(len(ends_combined), dtype=bool)
        elif stratum == "heavy_only":
            stratum_mask = intensity_of_end == "heavy"
        else:  # very_heavy_only
            stratum_mask = intensity_of_end == "very_heavy"
        stratum_ends = ends_combined[stratum_mask]
        n_stratum_ends = len(stratum_ends)
        for outcome_raw in ACTIVITY_OUTCOMES_RAW:
            report_name = OUTCOME_REPORT_NAMES[outcome_raw]
            src_col = "active_min" if outcome_raw == "active_sec" else outcome_raw
            for k in range(k_max + 1):
                n_valid = 0
                for end_idx in stratum_ends:
                    target = end_idx + k
                    if target >= n_rows:
                        continue
                    val = df[src_col].iloc[target]
                    if pd.notna(val):
                        n_valid += 1
                rows.append({
                    "intensity_stratum": stratum,
                    "outcome": report_name,
                    "k": k,
                    "n_episode_ends_in_stratum": n_stratum_ends,
                    "n_valid_outcome_at_d_plus_k": n_valid,
                    "n_nan_outcome_at_d_plus_k": n_stratum_ends - n_valid,
                })
    return pd.DataFrame(rows)


# ------------- section 8: per-phase pre-window mean levels (MD-alpha 3.5) -------------


def pre_window_levels(df, ends_combined):
    """For each (phase, outcome) report the mean pre-window (30d) level averaged
    over episode-ends in that phase. Supports MD-alpha section 3.5 level-vs-change
    discipline (report per-phase pre-window mean levels alongside AUC magnitudes).
    NaN cells reported as NaN; not zero-imputed per CONVENTIONS section 5.
    """
    rows = []
    for phase in PHASE_ORDER:
        phase_ends = [i for i in ends_combined if df["recovery_phase"].iloc[i] == phase]
        n_phase_ends = len(phase_ends)
        for outcome_raw in ACTIVITY_OUTCOMES_RAW:
            report_name = OUTCOME_REPORT_NAMES[outcome_raw]
            src_col = "active_min" if outcome_raw == "active_sec" else outcome_raw
            per_episode_means = []
            for end_idx in phase_ends:
                pre_start = max(0, end_idx - DETREND_PRE_WINDOW_DAYS)
                pre_end = end_idx  # exclusive; day-of-episode-end not in pre-window
                pre_vals = df[src_col].iloc[pre_start:pre_end]
                if pre_vals.notna().sum() == 0:
                    per_episode_means.append(np.nan)
                else:
                    per_episode_means.append(pre_vals.mean())
            arr = np.array(per_episode_means, dtype=float)
            n_with_pre = int(np.sum(~np.isnan(arr)))
            phase_mean = float(np.nanmean(arr)) if n_with_pre > 0 else float("nan")
            phase_median = float(np.nanmedian(arr)) if n_with_pre > 0 else float("nan")
            rows.append({
                "phase": phase,
                "outcome": report_name,
                "n_episode_ends_in_phase": n_phase_ends,
                "n_episodes_with_valid_pre_window": n_with_pre,
                "pre_window_mean_across_episodes": phase_mean,
                "pre_window_median_across_episodes": phase_median,
                "pre_window_days": DETREND_PRE_WINDOW_DAYS,
            })
    return pd.DataFrame(rows)


# ------------- main -------------


def main():
    df = load_lc_stratum()
    print(f"[stratum] LC-era rows: {len(df)}; heavy days: {int(df['is_heavy'].sum())}; "
          f"very_heavy: {int(df['is_very_heavy'].sum())}")

    # 1. Phase episode counts (MD-alpha 3.1 / 7.1)
    phase_counts, ends_combined = phase_episode_counts(df)
    phase_counts.to_csv(OUTPUT_DIR / "phase_episode_counts.csv", index=False)
    print(f"[phase counts] episode-ends combined gap=0 total: {len(ends_combined)}")

    # 2. Intensity x phase cross-tab (MD-alpha 6.3 / 7.2)
    cross = intensity_phase_crosstab(df, ends_combined)
    cross.to_csv(OUTPUT_DIR / "phase_intensity_crosstab.csv", index=False)

    # 3. Per-phase per-outcome per-k coverage (MD-alpha 7.3)
    per_out_cov = coverage_per_phase(df, ends_combined, k_max=10)
    per_out_cov.to_csv(OUTPUT_DIR / "phase_per_outcome_coverage.csv", index=False)

    # 4. Strict-clean + pool split floors (MD-alpha 7.5)
    floors = strict_clean_pool_floors(df, ends_combined)
    floors.to_csv(OUTPUT_DIR / "phase_strict_clean_pool_floors.csv", index=False)

    # 5. Detrended-arm floors (MD-alpha 7.5 detrend clause / parent MD 7.11)
    detrend = detrended_arm_floors(df, ends_combined)
    detrend.to_csv(OUTPUT_DIR / "phase_detrended_arm_floors.csv", index=False)

    # 6. Intensity-stratum per-outcome coverage (MD-alpha 7.4)
    intensity_cov = intensity_stratum_coverage(df, ends_combined, k_max=10)
    intensity_cov.to_csv(OUTPUT_DIR / "intensity_stratum_per_outcome_coverage.csv", index=False)

    # 7. Per-phase pre-window level table (MD-alpha 3.5)
    pre_levels = pre_window_levels(df, ends_combined)
    pre_levels.to_csv(OUTPUT_DIR / "phase_pre_window_levels.csv", index=False)

    print("\n[write] outputs in", OUTPUT_DIR)
    for f in sorted(OUTPUT_DIR.glob("*.csv")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
