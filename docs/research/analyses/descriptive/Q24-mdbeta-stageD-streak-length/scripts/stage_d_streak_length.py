"""Q24 MD-beta Stage D descriptive audit -- streak-length arc under LOCKED r2.

Reproduces every count, every per-bin crash rate + Wilson 95% CI, every
Cochran-Armitage trend test statistic + two-sided p-value, every per-bin
bootstrap 95% CI on crash rate + risk ratio, and every E[L]* rolling-window
autocorrelation diagnostic in the sibling descriptive_audit.md.

Anchor: docs/research/methodology/heavy_day_crash_risk_prediction.md LOCKED r2
2026-07-17. Section 4 executes the streak-length arc as a cumulative-load-dose
predictor of crash-in-5d on the 314-episode all-episodes pool with L_bin in
{1, 2, 3, 4+}.

Statistical machinery per MD-beta section 4.5:

    - Wilson score 95% CI on per-bin crash rate.
    - Cochran-Armitage trend test on the ordinal 4-bin x binary-outcome
      contingency; row_scores = [1, 2, 3, 4]; two-sided p-value reported for
      completeness, NOT verdict per CONVENTIONS section 2.1.
    - Bootstrap 95% CI on per-bin crash rate: B = 10000 episode-level
      resamples, block length = 1 primary, seed = 20260716.
    - Bootstrap null on Cochran-Armitage: B = 10000 permutations of L_bin
      labels within the episode-end pool, block length = 1.

E[L]* rolling-window autocorrelation diagnostic per MD-beta section 4.7 +
HA-P7 sensitivity_block_length precedent + permutation_null_block_length.md
section 2:

    - Compute the lag-1 autocorrelation of the day-level streak_length
      sequence on the LC-era stratum.
    - Compute E[L]* via the pragmatic Politis-White-style estimator:
      L_hat = 1 + 2 * sum of significant ACF lags (|rho_h| outside the
      Bartlett band 2/sqrt(n)).
    - Flag if E[L]* >= 2x the locked block length of 1.
    - Probe: do multiple 4+ streaks cluster within a 30d window?

Sample viability per MD-beta section 4.6: L=1 n=188, L=2 n=77, L=3 n=27,
L=4+ n=22. Crash-in-5d rate on pool = 46/314 = 14.6%. All four bins pass
the informal Wilson-viable floor of 10 exposed per arm; L=4+ Wilson CI will
be wide.

Discipline: Stage D descriptive audit only per CONVENTIONS section 2.1;
descriptive-with-CI framing, no verdicts, no inferential closure. Direction
pre-commit per MD-beta section 4.4: longer streaks -> HIGHER crash rate
(dose-response). Sign-inversion or non-monotonicity reported as substantive
descriptive finding.

Circularity with parent Q24 MD section 3.5 pool-split per MD-beta section 5
confound 6: shared crash-in-5d outcome sample. Report + do NOT double-invoke
as independent evidence.

Idempotent + re-runnable. Outputs land in ../output/.
"""
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.proportion import proportion_confint


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DATA_PATH = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    "C:/Users/Gebruiker/Documents/gevoelscore-data",
))
INPUT = DATA_PATH / "unified" / "per_day_master.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEAVY_CLASSES = {"heavy", "very_heavy"}
CRASH_WINDOW = 5
RANDOM_SEED = 20260716
BOOTSTRAP_B = 10000
ALPHA = 0.05
LOCKED_BLOCK_LENGTH = 1

# Era boundary per MD-beta section 5 confound 7 revision.
CITAL_BOUNDARY = pd.Timestamp("2024-04-09")

# Sample floor per user Option B (informal).
WILSON_VIABLE_FLOOR = 10

# L_bin ordinal scores per MD-beta section 4.5 Cochran-Armitage row_scores.
L_BINS = ["1", "2", "3", "4+"]
L_BIN_SCORES = [1, 2, 3, 4]


# ---------------------------------------------------------------------------
# Data loading + operand construction
# ---------------------------------------------------------------------------

def load_lc_stratum():
    """Load per_day_master.csv, filter to LC-era, add operand columns.

    Adds:
      is_heavy, is_very_heavy, is_crash, year, era.
    """
    df = pd.read_csv(INPUT, parse_dates=["date"])
    df = df[df["lc_phase"] == "lc"].copy().reset_index(drop=True)
    df["is_heavy"] = df["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)
    df["is_very_heavy"] = df["exertion_class_lagged_lcera"] == "very_heavy"
    df["is_crash"] = df["is_crash"].fillna(False).astype(bool)
    df["year"] = df["date"].dt.year

    diffs = df["date"].diff().dt.days.dropna()
    if not (diffs == 1).all():
        gap_count = int((diffs != 1).sum())
        raise RuntimeError(
            f"LC-era rows not contiguous by day; {gap_count} gap(s) detected."
        )

    df["era"] = np.where(df["date"] < CITAL_BOUNDARY, "pre_cital", "post_cital")

    return df


# ---------------------------------------------------------------------------
# Episode construction (gap=0 contiguous heavy runs)
# ---------------------------------------------------------------------------

def build_episodes(df):
    """Emit one row per gap=0 heavy episode.

    Columns:
      episode_id, D_start, D_end, streak_length, L_bin (1/2/3/4+),
      year_end, end_class (heavy / very_heavy),
      era (pre_cital / post_cital), vh_count, vh_frac,
      crash_in_5d (bool), crash_window_full (bool),
      D_end_idx (integer position in the LC-era frame).
    """
    n = len(df)
    heavy = df["is_heavy"].values
    vh = df["is_very_heavy"].values
    episodes = []
    ep_id = 0
    i = 0
    while i < n:
        if not heavy[i]:
            i += 1
            continue
        ep_id += 1
        start = i
        while i + 1 < n and heavy[i + 1]:
            i += 1
        end = i
        length = end - start + 1
        vh_count = int(vh[start:end + 1].sum())
        vh_frac = vh_count / length
        end_row = df.iloc[end]
        end_class = "very_heavy" if bool(end_row["is_very_heavy"]) else "heavy"
        d_start = df.iloc[start]["date"]
        d_end = df.iloc[end]["date"]

        c_lo = end + 1
        c_hi = min(end + CRASH_WINDOW, n - 1)
        if c_lo > n - 1:
            crash_in_5d = False
            crash_window_full = False
        else:
            crash_slice = df.iloc[c_lo:c_hi + 1]["is_crash"]
            crash_in_5d = bool(crash_slice.any())
            crash_window_full = (c_hi - c_lo + 1) == CRASH_WINDOW

        era = "pre_cital" if d_end < CITAL_BOUNDARY else "post_cital"

        if length >= 4:
            l_bin = "4+"
        else:
            l_bin = str(length)

        record = {
            "episode_id": ep_id,
            "D_start": d_start,
            "D_end": d_end,
            "D_end_idx": end,
            "streak_length": length,
            "L_bin": l_bin,
            "year_end": int(end_row["year"]),
            "end_class": end_class,
            "era": era,
            "vh_count": vh_count,
            "vh_frac": vh_frac,
            "crash_in_5d": crash_in_5d,
            "crash_window_full": crash_window_full,
        }
        episodes.append(record)
        i = end + 1

    return pd.DataFrame(episodes)


# ---------------------------------------------------------------------------
# Statistical machinery
# ---------------------------------------------------------------------------

def wilson_ci(k, n):
    """Wilson 95% CI via statsmodels."""
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    lo, hi = proportion_confint(k, n, alpha=ALPHA, method="wilson")
    return (k / n, float(lo), float(hi))


def bootstrap_rate_ci(k, n, B=BOOTSTRAP_B, seed=RANDOM_SEED):
    """Bootstrap 95% CI on a proportion via episode-level resampling.

    Percentile 2.5 / 97.5. Block length = 1 per MD-beta section 4.5. Not the
    Wilson score CI; a companion resampling-based CI to complement Wilson.
    """
    if n == 0:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    rates = np.empty(B)
    prob_true = k / n
    for b in range(B):
        # Direct binomial draw is the block-length-1 bootstrap on a bag of
        # independent 0/1 flags with a fixed marginal rate; equivalent to
        # resampling n episodes with replacement.
        draw = rng.binomial(n, prob_true)
        rates[b] = draw / n
    lo, hi = np.percentile(rates, [2.5, 97.5])
    return (float(lo), float(hi))


def bootstrap_rate_ci_from_flags(crash_flags, B=BOOTSTRAP_B, seed=RANDOM_SEED):
    """Bootstrap 95% CI on a proportion by resampling the underlying flags.

    Block length = 1 per MD-beta section 4.5. Preferred over the
    bootstrap_rate_ci variant when we already have per-episode crash flags,
    because it resamples the empirical distribution rather than the fitted
    binomial parameter.
    """
    crash_flags = np.asarray(crash_flags, dtype=bool)
    n = len(crash_flags)
    if n == 0:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    rates = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, size=n)
        rates[b] = crash_flags[idx].mean()
    lo, hi = np.percentile(rates, [2.5, 97.5])
    return (float(lo), float(hi))


def cochran_armitage_trend(bin_labels, crash_flags, row_scores):
    """Compute the Cochran-Armitage linear-score trend statistic on an
    ordinal-exposure x binary-outcome contingency.

    Formula (Armitage 1955): Z = T / sqrt(Var(T)), where
      T = sum_i (score_i - score_bar) * (a_i - E[a_i | R_i, N, k])
    with a_i = number of positive outcomes in row i, N_i = row totals, N =
    grand total, k = column-1 total (total positives).

    Standard form (equivalent):
      Numerator N = sum_i score_i * (a_i * (N - N_i) - (k - a_i) * N_i) / N
                  or (simpler) N = sum_i score_i * a_i * N - k * sum_i score_i * N_i
      Variance and Z as in Armitage.

    Returns (Z_statistic, two_sided_p_value).
    """
    from scipy.stats import norm

    bin_labels = np.asarray(bin_labels)
    crash_flags = np.asarray(crash_flags, dtype=bool)
    n_total = len(crash_flags)
    if n_total == 0:
        return float("nan"), float("nan")
    k_total = int(crash_flags.sum())
    p_bar = k_total / n_total
    q_bar = 1.0 - p_bar

    # Row totals per L_bin.
    row_scores_arr = np.asarray(row_scores, dtype=float)
    N_i = np.zeros(len(row_scores_arr))
    a_i = np.zeros(len(row_scores_arr))
    for idx, bin_lab in enumerate(L_BINS):
        mask = (bin_labels == bin_lab)
        N_i[idx] = mask.sum()
        a_i[idx] = crash_flags[mask].sum()

    if N_i.sum() == 0 or k_total == 0 or k_total == n_total:
        return float("nan"), float("nan")

    # Cochran-Armitage per Agresti/Armitage:
    # T = sum_i s_i * (a_i - N_i * p_bar)
    # Var(T) = p_bar * q_bar * (sum_i N_i * s_i^2 - (sum_i N_i * s_i)^2 / N)
    T = float(np.sum(row_scores_arr * (a_i - N_i * p_bar)))
    numer_var = np.sum(N_i * row_scores_arr ** 2) - (
        np.sum(N_i * row_scores_arr) ** 2 / n_total
    )
    var_T = p_bar * q_bar * numer_var
    if var_T <= 0:
        return float("nan"), float("nan")
    Z = T / math.sqrt(var_T)
    p_two_sided = 2 * (1.0 - norm.cdf(abs(Z)))
    return float(Z), float(p_two_sided)


def permutation_null_ca(bin_labels, crash_flags, row_scores,
                         B=BOOTSTRAP_B, seed=RANDOM_SEED):
    """Permutation null on the Cochran-Armitage Z statistic.

    Permutes the L_bin labels within the episode-end pool B times and
    computes Z each round. Returns the two-sided permutation p-value and
    the observed Z + null-quantiles (2.5 / 97.5 / 50).

    Block length = 1 per MD-beta section 4.5 primary; the null preserves the
    marginal crash rate but destroys the exposure-outcome association.
    """
    bin_labels = np.asarray(bin_labels)
    crash_flags = np.asarray(crash_flags, dtype=bool)
    n = len(crash_flags)
    Z_obs, _ = cochran_armitage_trend(bin_labels, crash_flags, row_scores)
    if math.isnan(Z_obs):
        return {
            "Z_observed": float("nan"),
            "p_permutation_two_sided": float("nan"),
            "null_Z_lo_2p5": float("nan"),
            "null_Z_median": float("nan"),
            "null_Z_hi_97p5": float("nan"),
            "B": B,
        }
    rng = np.random.default_rng(seed)
    null_Zs = np.empty(B)
    for b in range(B):
        perm_labels = rng.permutation(bin_labels)
        Z_b, _ = cochran_armitage_trend(perm_labels, crash_flags, row_scores)
        null_Zs[b] = Z_b
    valid = null_Zs[~np.isnan(null_Zs)]
    if len(valid) < 100:
        p_perm = float("nan")
        lo, med, hi = float("nan"), float("nan"), float("nan")
    else:
        p_perm = float((np.abs(valid) >= abs(Z_obs)).mean())
        lo, med, hi = np.percentile(valid, [2.5, 50, 97.5])
    return {
        "Z_observed": float(Z_obs),
        "p_permutation_two_sided": p_perm,
        "null_Z_lo_2p5": float(lo),
        "null_Z_median": float(med),
        "null_Z_hi_97p5": float(hi),
        "B": B,
    }


# ---------------------------------------------------------------------------
# E[L]* rolling-window autocorrelation diagnostic
# ---------------------------------------------------------------------------

def day_level_streak_length(df):
    """Emit the day-level streak_length sequence on the LC-era stratum.

    For each day in the LC-era frame: streak_length[d] = length of the
    contiguous heavy run that d belongs to if d is heavy, else 0. This is
    the rolling-identifier form of the streak variable; the per-episode-end
    values are a downsample.
    """
    n = len(df)
    heavy = df["is_heavy"].values
    seq = np.zeros(n, dtype=int)
    i = 0
    while i < n:
        if not heavy[i]:
            i += 1
            continue
        start = i
        while i + 1 < n and heavy[i + 1]:
            i += 1
        end = i
        length = end - start + 1
        seq[start:end + 1] = length
        i = end + 1
    return seq


def estimate_block_length(x, max_lag=60):
    """Pragmatic data-driven E[L]* estimator.

    Politis-White-style: L_hat = 1 + 2 * sum_{h=1..H} rho_h,
    where H is the first h at which |rho_h| falls below the Bartlett band
    2 / sqrt(n). Same estimator as HA-P7 test.py section
    `estimate_block_length` (cited in MD-beta section 4.7 as the HA-P7
    precedent). Returns E[L]* as a float.

    Note: E[L]* here estimates the effective correlation length (Neff),
    matching the [`permutation_null_block_length.md`] section 2 confirmatory
    estimator that flags when E[L]* differs from the locked block length by
    more than a factor of 2.
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 30:
        return float("nan")
    xc = x - x.mean()
    var = (xc ** 2).sum()
    if var == 0:
        return float("nan")
    band = 2.0 / math.sqrt(n)
    rhos = []
    for h in range(1, min(max_lag, n - 1) + 1):
        rho = (xc[:-h] * xc[h:]).sum() / var
        if abs(rho) < band:
            break
        rhos.append(rho)
    if not rhos:
        return 1.0
    return float(1.0 + 2.0 * sum(rhos))


def lag1_autocorrelation(x):
    """Lag-1 autocorrelation coefficient."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return float("nan")
    xc = x - x.mean()
    var = (xc ** 2).sum()
    if var == 0:
        return float("nan")
    return float((xc[:-1] * xc[1:]).sum() / var)


def streak_clustering_probe(episodes, window_days=30):
    """Probe: how often do multiple L=4+ streaks fall within a rolling
    window_days window?

    Emits a summary: n_pairs_within_30d, n_4plus_total, dates_of_4plus.
    """
    four_plus = episodes[episodes["L_bin"] == "4+"].copy()
    four_plus = four_plus.sort_values("D_end").reset_index(drop=True)
    dates = list(four_plus["D_end"])
    n_pairs = 0
    pair_details = []
    for a in range(len(dates)):
        for b in range(a + 1, len(dates)):
            delta = (dates[b] - dates[a]).days
            if delta <= window_days:
                n_pairs += 1
                pair_details.append((dates[a], dates[b], delta))
            else:
                break
    return {
        "n_4plus_total": len(four_plus),
        "n_pairs_within_30d": n_pairs,
        "pair_details": pair_details,
        "dates_of_4plus": [str(d.date()) for d in dates],
    }


# ---------------------------------------------------------------------------
# Reporting scaffold
# ---------------------------------------------------------------------------

def _era_filter(episodes, era):
    if era == "ALL":
        return episodes
    return episodes[episodes["era"] == era]


def _per_bin_stats(episodes, era_label):
    """Per-L_bin crash rate + Wilson CI + bootstrap CI + Fisher-vs-baseline.

    Returns one row per L_bin.
    """
    sub = _era_filter(episodes, era_label)
    sub = sub[sub["crash_window_full"] == True]
    rows = []
    base_n = len(sub)
    base_k = int(sub["crash_in_5d"].sum())
    for bin_lab in L_BINS:
        s = sub[sub["L_bin"] == bin_lab]
        n = len(s)
        k = int(s["crash_in_5d"].sum())
        rate, wilson_lo, wilson_hi = wilson_ci(k, n)
        boot_lo, boot_hi = bootstrap_rate_ci_from_flags(
            s["crash_in_5d"].astype(bool).values,
        )
        floor_pass = n >= WILSON_VIABLE_FLOOR
        rows.append({
            "cell": f"L_bin_{bin_lab}_era_{era_label}",
            "era": era_label,
            "L_bin": bin_lab,
            "L_bin_score": L_BIN_SCORES[L_BINS.index(bin_lab)],
            "n_episodes": n,
            "n_crashes": k,
            "crash_rate": rate,
            "crash_rate_wilson_lo": wilson_lo,
            "crash_rate_wilson_hi": wilson_hi,
            "crash_rate_boot_lo": boot_lo,
            "crash_rate_boot_hi": boot_hi,
            "wilson_viable_floor_pass": floor_pass,
            "pool_n_this_era": base_n,
            "pool_k_this_era": base_k,
            "pool_rate_this_era": (base_k / base_n) if base_n else float("nan"),
        })
    return pd.DataFrame(rows)


def per_bin_by_era(episodes):
    """Section 3 headline + Section 4 era-stratified per-bin crash rates."""
    frames = []
    for era_label in ["ALL", "pre_cital", "post_cital"]:
        frames.append(_per_bin_stats(episodes, era_label))
    out = pd.concat(frames, ignore_index=True)
    out.to_csv(OUTPUT_DIR / "per_bin_crash_rate.csv", index=False)
    return out


def cochran_armitage_by_era(episodes):
    """Section 3.2 + Section 4.3: Cochran-Armitage trend per era."""
    rows = []
    for era_label in ["ALL", "pre_cital", "post_cital"]:
        sub = _era_filter(episodes, era_label)
        sub = sub[sub["crash_window_full"] == True]
        Z, p = cochran_armitage_trend(
            sub["L_bin"].values,
            sub["crash_in_5d"].astype(bool).values,
            L_BIN_SCORES,
        )
        # Permutation null companion.
        perm = permutation_null_ca(
            sub["L_bin"].values,
            sub["crash_in_5d"].astype(bool).values,
            L_BIN_SCORES,
        )
        rows.append({
            "cell": f"cochran_armitage_era_{era_label}",
            "era": era_label,
            "n_episodes": int(len(sub)),
            "n_crashes": int(sub["crash_in_5d"].sum()),
            "Z_asymptotic": Z,
            "p_asymptotic_two_sided": p,
            "Z_permutation_observed": perm["Z_observed"],
            "p_permutation_two_sided": perm["p_permutation_two_sided"],
            "null_Z_lo_2p5": perm["null_Z_lo_2p5"],
            "null_Z_median": perm["null_Z_median"],
            "null_Z_hi_97p5": perm["null_Z_hi_97p5"],
            "permutation_B": perm["B"],
            "row_scores": ",".join(str(s) for s in L_BIN_SCORES),
        })
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "cochran_armitage_trend.csv", index=False)
    return df


def intensity_stratified(episodes):
    """Section 5: streak-length crash rate stratified by vh_frac.

    Cutoff: vh_frac <= 0.5 vs vh_frac > 0.5. Emits per-bin crash rate on
    each stratum; also emits a Cochran-Armitage trend per stratum.
    """
    rows = []
    strata = [
        ("low_vh_frac_le_05", episodes[episodes["vh_frac"] <= 0.5]),
        ("high_vh_frac_gt_05", episodes[episodes["vh_frac"] > 0.5]),
    ]
    for stratum_label, sub in strata:
        sub = sub[sub["crash_window_full"] == True]
        for bin_lab in L_BINS:
            s = sub[sub["L_bin"] == bin_lab]
            n = len(s)
            k = int(s["crash_in_5d"].sum())
            rate, wilson_lo, wilson_hi = wilson_ci(k, n)
            boot_lo, boot_hi = bootstrap_rate_ci_from_flags(
                s["crash_in_5d"].astype(bool).values,
            )
            rows.append({
                "cell": f"L_bin_{bin_lab}_{stratum_label}",
                "stratum": stratum_label,
                "L_bin": bin_lab,
                "n_episodes": n,
                "n_crashes": k,
                "crash_rate": rate,
                "crash_rate_wilson_lo": wilson_lo,
                "crash_rate_wilson_hi": wilson_hi,
                "crash_rate_boot_lo": boot_lo,
                "crash_rate_boot_hi": boot_hi,
                "wilson_viable_floor_pass": n >= WILSON_VIABLE_FLOOR,
            })
        # Trend per stratum
        Z, p = cochran_armitage_trend(
            sub["L_bin"].values,
            sub["crash_in_5d"].astype(bool).values,
            L_BIN_SCORES,
        )
        rows.append({
            "cell": f"CA_trend_{stratum_label}",
            "stratum": stratum_label,
            "L_bin": "trend",
            "n_episodes": int(len(sub)),
            "n_crashes": int(sub["crash_in_5d"].sum()),
            "crash_rate": float("nan"),
            "crash_rate_wilson_lo": Z,
            "crash_rate_wilson_hi": p,
            "crash_rate_boot_lo": float("nan"),
            "crash_rate_boot_hi": float("nan"),
            "wilson_viable_floor_pass": True,
        })
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "intensity_stratified.csv", index=False)
    return df


def data_availability_reproductions(episodes):
    """Section 1.2 + 1.3 + 1.4 byte-for-byte MD-beta reproductions.

    Emits three CSVs:
      md_beta_6_2_streak_distribution.csv   -- MD-beta 6.2 byte-for-byte
      md_beta_6_3_streak_intensity.csv      -- MD-beta 6.3 byte-for-byte
      md_beta_6_4_streak_era.csv            -- MD-beta 6.4 byte-for-byte
    """
    # 6.2 streak distribution
    rows = []
    total = len(episodes)
    for bin_lab in L_BINS:
        n = int((episodes["L_bin"] == bin_lab).sum())
        rows.append({
            "L_bin": bin_lab,
            "n": n,
            "rate": n / total if total else float("nan"),
        })
    rows.append({"L_bin": "total", "n": total, "rate": 1.0})
    # sub-bins within 4+ for context
    for L in [4, 5, 6, 7, 8, 10]:
        n = int((episodes["streak_length"] == L).sum())
        rows.append({"L_bin": f"sub_L_{L}", "n": n, "rate": float("nan")})
    df_dist = pd.DataFrame(rows)
    df_dist.to_csv(OUTPUT_DIR / "md_beta_6_2_streak_distribution.csv", index=False)

    # 6.3 streak x intensity
    rows = []
    for bin_lab in L_BINS:
        s = episodes[episodes["L_bin"] == bin_lab]
        rows.append({
            "L_bin": bin_lab,
            "n_episodes": len(s),
            "mean_vh_frac": float(s["vh_frac"].mean()) if len(s) else float("nan"),
            "median_vh_frac": float(s["vh_frac"].median()) if len(s) else float("nan"),
            "mean_vh_count": float(s["vh_count"].mean()) if len(s) else float("nan"),
        })
    df_int = pd.DataFrame(rows)
    df_int.to_csv(OUTPUT_DIR / "md_beta_6_3_streak_intensity.csv", index=False)

    # 6.4 streak x era (by year)
    rows = []
    years = sorted(episodes["year_end"].unique())
    for year in years:
        s = episodes[episodes["year_end"] == year]
        row = {"year": int(year), "n_episodes": len(s)}
        for bin_lab in L_BINS:
            row[f"L_{bin_lab}"] = int((s["L_bin"] == bin_lab).sum())
        rows.append(row)
    # totals row
    row_total = {"year": "total", "n_episodes": len(episodes)}
    for bin_lab in L_BINS:
        row_total[f"L_{bin_lab}"] = int((episodes["L_bin"] == bin_lab).sum())
    rows.append(row_total)
    df_era = pd.DataFrame(rows)
    df_era.to_csv(OUTPUT_DIR / "md_beta_6_4_streak_era.csv", index=False)

    return df_dist, df_int, df_era


def preflight_probe(episodes):
    """Section 1.5: per-bin sample-floor viability."""
    rows = []
    for era_label in ["ALL", "pre_cital", "post_cital"]:
        sub = _era_filter(episodes, era_label)
        sub = sub[sub["crash_window_full"] == True]
        for bin_lab in L_BINS:
            s = sub[sub["L_bin"] == bin_lab]
            n = len(s)
            k = int(s["crash_in_5d"].sum())
            floor_pass = n >= WILSON_VIABLE_FLOOR
            rows.append({
                "family": "per_bin_crash_rate",
                "cell": f"L_bin_{bin_lab}_era_{era_label}",
                "n_episodes_available": n,
                "n_crashes": k,
                "wilson_viable_floor_pass": floor_pass,
            })
    for stratum_label in ["low_vh_frac_le_05", "high_vh_frac_gt_05"]:
        if stratum_label == "low_vh_frac_le_05":
            sub = episodes[episodes["vh_frac"] <= 0.5]
        else:
            sub = episodes[episodes["vh_frac"] > 0.5]
        sub = sub[sub["crash_window_full"] == True]
        for bin_lab in L_BINS:
            s = sub[sub["L_bin"] == bin_lab]
            n = len(s)
            k = int(s["crash_in_5d"].sum())
            floor_pass = n >= WILSON_VIABLE_FLOOR
            rows.append({
                "family": "intensity_stratified",
                "cell": f"L_bin_{bin_lab}_{stratum_label}",
                "n_episodes_available": n,
                "n_crashes": k,
                "wilson_viable_floor_pass": floor_pass,
            })
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "preflight_sample_floor.csv", index=False)
    return df


def el_star_diagnostic(df, episodes):
    """Section 6: E[L]* rolling-window autocorrelation diagnostic.

    Computes:
      - lag-1 autocorrelation of day-level streak_length on LC-era stratum
      - E[L]* via Politis-White-style ACF-summation estimator
      - Comparison to locked block length = 1
      - Clustering probe: multiple L=4+ within 30d rolling window
    """
    seq = day_level_streak_length(df)
    rho_1 = lag1_autocorrelation(seq)
    el_star = estimate_block_length(seq, max_lag=60)
    factor_of_2 = (el_star / LOCKED_BLOCK_LENGTH) if not math.isnan(el_star) else float("nan")
    flag = (el_star >= 2 * LOCKED_BLOCK_LENGTH) if not math.isnan(el_star) else False

    cluster = streak_clustering_probe(episodes, window_days=30)

    rows = [{
        "n_days_lc_stratum": len(seq),
        "day_level_streak_length_mean": float(seq.mean()),
        "day_level_streak_length_max": int(seq.max()),
        "day_level_streak_length_zero_frac": float((seq == 0).mean()),
        "lag1_autocorrelation": rho_1,
        "E_L_star": el_star,
        "locked_block_length": LOCKED_BLOCK_LENGTH,
        "factor_vs_locked": factor_of_2,
        "flag_factor_of_2_or_more": flag,
        "n_4plus_episodes_total": cluster["n_4plus_total"],
        "n_4plus_pairs_within_30d": cluster["n_pairs_within_30d"],
    }]
    df_out = pd.DataFrame(rows)
    df_out.to_csv(OUTPUT_DIR / "el_star_diagnostic.csv", index=False)

    # Persist the pair details separately for the cluster probe reproducibility.
    if cluster["pair_details"]:
        pair_rows = [
            {"pair_a": str(a.date()), "pair_b": str(b.date()), "days_apart": d}
            for (a, b, d) in cluster["pair_details"]
        ]
    else:
        pair_rows = [{"pair_a": "none", "pair_b": "none", "days_apart": -1}]
    pd.DataFrame(pair_rows).to_csv(
        OUTPUT_DIR / "el_star_4plus_pair_details.csv", index=False,
    )

    # Also persist dates-of-4plus for the audit body.
    pd.DataFrame({"date_4plus": cluster["dates_of_4plus"]}).to_csv(
        OUTPUT_DIR / "el_star_4plus_dates.csv", index=False,
    )

    return df_out, cluster


def _stationary_bootstrap_indices(n, expected_block_len, rng):
    """Politis-Romano stationary-bootstrap index array of length n.

    Block length drawn from geometric distribution with mean
    expected_block_len; wrap-around continuation at ends. Mirrors the
    HA-P7 test.py convention.
    """
    if expected_block_len <= 1:
        return rng.integers(0, n, size=n)
    p = 1.0 / expected_block_len
    idx = np.empty(n, dtype=np.int64)
    i = 0
    while i < n:
        start = int(rng.integers(0, n))
        # Geometric block length (mean = expected_block_len).
        L = int(rng.geometric(p))
        L = max(1, L)
        L = min(L, n - i)
        for j in range(L):
            idx[i + j] = (start + j) % n
        i += L
    return idx


def per_bin_bootstrap_at_el_star(episodes, el_star,
                                  B=BOOTSTRAP_B, seed=RANDOM_SEED):
    """Section 6.5 sensitivity companion: per-bin bootstrap CI on crash rate
    at E[L]*-block-length stationary bootstrap.

    Rounds the E[L]* to the nearest integer for the geometric-mean parameter
    of the stationary bootstrap. When E[L]* < 2, falls back to block
    length = 1 (independent resampling).

    Since the per-episode-end unit-of-analysis compresses per-day
    streak-length identity into a single value per episode, the E[L]* block
    is applied at the episode-level index array; the resampled index
    sequence is a stationary-bootstrap draw over the episode-end pool
    ordered by D_end.
    """
    sub = episodes[episodes["crash_window_full"] == True].copy()
    sub = sub.sort_values("D_end").reset_index(drop=True)
    el_int = max(1, int(round(el_star)))
    rng = np.random.default_rng(seed)
    rows = []
    for bin_lab in L_BINS:
        s = sub[sub["L_bin"] == bin_lab]
        n = len(s)
        k = int(s["crash_in_5d"].sum())
        rate = k / n if n else float("nan")
        if n == 0:
            rows.append({
                "cell": f"L_bin_{bin_lab}_boot_at_el_star",
                "L_bin": bin_lab,
                "n_episodes": n,
                "n_crashes": k,
                "crash_rate": rate,
                "el_star_used": el_int,
                "crash_rate_boot_lo": float("nan"),
                "crash_rate_boot_hi": float("nan"),
            })
            continue
        # Get the D_end-ordered position of each episode in the bin, then
        # stationary-bootstrap resample.
        flags = s["crash_in_5d"].astype(bool).values
        rates_boot = np.empty(B)
        for b in range(B):
            idx = _stationary_bootstrap_indices(n, el_int, rng)
            rates_boot[b] = flags[idx].mean()
        lo, hi = np.percentile(rates_boot, [2.5, 97.5])
        rows.append({
            "cell": f"L_bin_{bin_lab}_boot_at_el_star",
            "L_bin": bin_lab,
            "n_episodes": n,
            "n_crashes": k,
            "crash_rate": rate,
            "el_star_used": el_int,
            "crash_rate_boot_lo": float(lo),
            "crash_rate_boot_hi": float(hi),
        })
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "per_bin_boot_at_el_star.csv", index=False)
    return df


def per_bin_rr_vs_L1(episodes, era_label="ALL"):
    """Companion: per-bin RR (vs L=1 as reference) with bootstrap 95% CI.

    Emitted for descriptive-with-CI readability alongside the per-bin
    crash-rate table; not a Cochran-Armitage substitute.
    """
    sub = _era_filter(episodes, era_label)
    sub = sub[sub["crash_window_full"] == True]
    ref = sub[sub["L_bin"] == "1"]
    ref_flags = ref["crash_in_5d"].astype(bool).values
    ref_rate = ref_flags.mean() if len(ref) else float("nan")
    rows = []
    rng = np.random.default_rng(RANDOM_SEED)
    for bin_lab in L_BINS:
        s = sub[sub["L_bin"] == bin_lab]
        s_flags = s["crash_in_5d"].astype(bool).values
        n = len(s)
        k = int(s_flags.sum())
        rate = k / n if n else float("nan")
        rr_point = (rate / ref_rate) if ref_rate and ref_rate > 0 else float("nan")

        # Bootstrap RR via joint resampling of both arms (independent
        # since arms are non-overlapping episodes).
        boot_rr = np.empty(BOOTSTRAP_B)
        for b in range(BOOTSTRAP_B):
            ref_idx = rng.integers(0, len(ref_flags), size=len(ref_flags)) if len(ref_flags) else np.array([], dtype=int)
            s_idx = rng.integers(0, len(s_flags), size=len(s_flags)) if len(s_flags) else np.array([], dtype=int)
            ref_r = ref_flags[ref_idx].mean() if len(ref_idx) else float("nan")
            s_r = s_flags[s_idx].mean() if len(s_idx) else float("nan")
            if ref_r and ref_r > 0:
                boot_rr[b] = s_r / ref_r
            else:
                boot_rr[b] = float("nan")
        valid = boot_rr[~np.isnan(boot_rr)]
        if len(valid) >= 100:
            rr_lo, rr_hi = np.percentile(valid, [2.5, 97.5])
        else:
            rr_lo, rr_hi = float("nan"), float("nan")

        rows.append({
            "cell": f"L_bin_{bin_lab}_RR_vs_L1_era_{era_label}",
            "L_bin": bin_lab,
            "n_episodes": n,
            "n_crashes": k,
            "crash_rate": rate,
            "reference_L_bin": "1",
            "reference_rate": ref_rate,
            "risk_ratio_vs_L1": rr_point,
            "risk_ratio_boot_lo": float(rr_lo),
            "risk_ratio_boot_hi": float(rr_hi),
            "risk_ratio_boot_valid_rounds": int(len(valid)),
        })
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "per_bin_rr_vs_L1.csv", index=False)
    return df


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    df = load_lc_stratum()
    print(f"[stratum] LC-era rows: {len(df)}")
    print(f"[stratum] heavy: {int(df['is_heavy'].sum())} "
          f"(vh={int(df['is_very_heavy'].sum())}); "
          f"crash: {int(df['is_crash'].sum())}")

    episodes = build_episodes(df)
    print(f"[episodes] gap=0 heavy episodes: {len(episodes)}")
    print(f"[episodes] L_bin: "
          + ", ".join(
              f"{b}: {int((episodes['L_bin'] == b).sum())}" for b in L_BINS
          ))
    print(f"[episodes] end_class heavy: "
          f"{int((episodes['end_class'] == 'heavy').sum())}; "
          f"very_heavy: {int((episodes['end_class'] == 'very_heavy').sum())}")
    print(f"[episodes] era pre_cital: "
          f"{int((episodes['era'] == 'pre_cital').sum())}; "
          f"post_cital: {int((episodes['era'] == 'post_cital').sum())}")
    print(f"[episodes] crash_in_5d True: "
          f"{int(episodes['crash_in_5d'].sum())} / {len(episodes)} "
          f"({int(episodes['crash_in_5d'].sum())/len(episodes):.3%})")

    # Persist the episode table for audit hooks.
    episodes.to_csv(OUTPUT_DIR / "episode_table.csv", index=False)

    # MD-beta 6.2 / 6.3 / 6.4 byte-for-byte reproductions.
    dist, intens, era_ct = data_availability_reproductions(episodes)
    print("[md_beta_6_2] streak distribution:")
    print(dist.to_string(index=False))
    print("\n[md_beta_6_3] streak x intensity:")
    print(intens.to_string(index=False))
    print("\n[md_beta_6_4] streak x era:")
    print(era_ct.to_string(index=False))

    # Preflight sample-floor probe.
    preflight = preflight_probe(episodes)
    print(f"\n[preflight] {len(preflight)} cells; "
          f"pass: {int(preflight['wilson_viable_floor_pass'].sum())}; "
          f"fail: {int((~preflight['wilson_viable_floor_pass']).sum())}")
    fails = preflight[~preflight["wilson_viable_floor_pass"]]
    if len(fails):
        print("[preflight] Failing cells:")
        print(fails.to_string(index=False))

    # Per-bin crash rate + Wilson + bootstrap.
    per_bin = per_bin_by_era(episodes)
    print("\n[per_bin_crash_rate] era=ALL headline:")
    print(per_bin[per_bin["era"] == "ALL"].to_string(index=False))

    # Cochran-Armitage trend test.
    ca = cochran_armitage_by_era(episodes)
    print("\n[cochran_armitage] trend by era:")
    print(ca[["cell", "n_episodes", "n_crashes",
             "Z_asymptotic", "p_asymptotic_two_sided",
             "p_permutation_two_sided"]].to_string(index=False))

    # Per-bin RR vs L=1 reference (era-pooled only).
    rr_ref = per_bin_rr_vs_L1(episodes, era_label="ALL")
    print("\n[per_bin_rr_vs_L1] era=ALL:")
    print(rr_ref[["cell", "n_episodes", "n_crashes",
                  "crash_rate", "risk_ratio_vs_L1",
                  "risk_ratio_boot_lo", "risk_ratio_boot_hi"]].to_string(index=False))

    # Intensity-adjusted companion.
    intens_strat = intensity_stratified(episodes)
    print("\n[intensity_stratified] per-bin rate on low + high vh_frac:")
    print(intens_strat.to_string(index=False))

    # E[L]* diagnostic.
    el_diag, cluster = el_star_diagnostic(df, episodes)
    print("\n[el_star_diagnostic] rolling-window autocorrelation:")
    print(el_diag.to_string(index=False))
    el_star_val = float(el_diag["E_L_star"].iloc[0])
    if el_diag["flag_factor_of_2_or_more"].iloc[0]:
        print(f"[el_star_diagnostic] FLAG: E[L]* = {el_star_val:.3f} >= 2 * "
              f"{LOCKED_BLOCK_LENGTH}; computing per-bin bootstrap at "
              f"E[L]*-block-length as sensitivity companion per HA-P7 4.6 template.")
        boot_at_el = per_bin_bootstrap_at_el_star(episodes, el_star_val)
        print("\n[per_bin_boot_at_el_star]:")
        print(boot_at_el.to_string(index=False))
    print(f"[el_star_diagnostic] n_4plus dates: {cluster['dates_of_4plus']}")
    if cluster["pair_details"]:
        print(f"[el_star_diagnostic] {len(cluster['pair_details'])} "
              f"L=4+ pairs within 30d:")
        for (a, b, d) in cluster["pair_details"]:
            print(f"    {a.date()} <-> {b.date()} ({d}d apart)")

    print(f"\n[write] outputs in {OUTPUT_DIR}")
    for f in sorted(OUTPUT_DIR.glob("*.csv")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
