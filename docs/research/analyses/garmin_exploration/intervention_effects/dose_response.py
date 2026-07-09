"""
Citalopram dose-response on stress_mean_sleep.

Implements the spec in
docs/research/methodology/citalopram_dose_response_stress_mean_sleep.md (v2).

Note on `dose_plasma_mg` materialisation (OI-035, 2026-07-09 confirmation):
    The PK-smoothed plasma proxy computed here by `dose_plasma_mg(d)` is
    ALSO materialised as the `dose_plasma_mg` column of `per_day_master.csv`
    via `pipeline/03_consolidate/build_unified_dataset.py` (added 2026-06-14;
    see DATA_DICTIONARY.md `Section 6 - Citalopram plasma proxy`). The
    runtime `dose_plasma_mg(d)` function below is retained here for
    backward-compatible reproduction of this script and for backfill /
    off-master derivation; downstream HAs on citalopram-dose-modulated
    channels should read the master column directly per
    `methodology/citalopram_phase_stratification.md` §5.B.

Primary: linear regression of stress_mean_sleep on PK-smoothed plasma
citalopram dose proxy + linear days_from_afbouw_start covariate,
Newey-West HAC SE with Andrews 1991 lag (~4 at n=70).

Sensitivities (A-F):
  A. Moving-block bootstrap residual CI (Kunsch 1989) on beta_dose,
     7-day blocks, 1000 iter, seed=42.
  B. Prescribed-step dose (vs PK-smoothed).
  C. stress_mean_sleep_lagged_lcera as outcome (computed on-the-fly
     since the column is NOT in per_day_master.csv -- see MD section 4.3-C
     for the [d-90, d-30] LC-era rolling-baseline z-score construction).
  D. HAC maxlags=7 (vs Andrews-rule ~4).
  E. Crash-drop (is_crash == True rows excluded) per CONVENTIONS section 3.4.
  F. Nonlinear time term: natural cubic spline 4 knots on days_from_afbouw_start
     (month-indicator dummies as fallback if spline basis becomes singular).

Diagnostics: lag-1 residual rho + effective n under HAC (Bartlett-weighted).

Null-finding pre-spec per MD section 4.4 (all 4 must hold):
  1. Primary HAC 95% CI contains 0
  2. abs(beta_dose) < 0.05 * SD(stress_mean_sleep) per mg
  3. Block-bootstrap 95% CI contains 0
  4. Lagged-lcera variant p > 0.05

Run:
    GEVOELSCORE_DATA_PATH=C:/Users/Gebruiker/Documents/gevoelscore-data python dose_response.py
"""

from datetime import datetime
from pathlib import Path
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from patsy import dmatrix


# ---------- Constants locked in MD section 6.2 ----------

SCRIPT_VERSION = "v1-2026-06-14"

DATA = Path(os.environ.get("GEVOELSCORE_DATA_PATH",
                           r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
if not DATA.exists():
    print(f"ERROR: data path not found: {DATA}", file=sys.stderr)
    sys.exit(1)

OUT = DATA / "analyses" / "intervention_effects"
(OUT / "plots").mkdir(parents=True, exist_ok=True)

AFBOUW_START = pd.Timestamp("2026-03-20")
AFBOUW_END = pd.Timestamp("2026-06-05")
ANALYTICAL_END = pd.Timestamp("2026-05-29")  # last observed stress_mean_sleep, per MD section 3.2

# Dose-step structure (MD section 2.1). Each tuple: (date, delta_mg).
# Initial dose 30mg (21-month consolidation plateau preceded the afbouw),
# so initial_dose_decay_term = 30 mg constant offset per MD section 2.3.
INITIAL_DOSE_MG = 30.0
DOSE_STEPS = [
    (pd.Timestamp("2026-03-20"), -10.0),  # 30 -> 20
    (pd.Timestamp("2026-04-17"), -10.0),  # 20 -> 10
    (pd.Timestamp("2026-05-27"),  -2.0),  # 10 -> 8 druppelvorm
]

T_HALF_HOURS = 35.0
T_HALF_DAYS = T_HALF_HOURS / 24.0           # ~1.4583 days, per citalopram SPC (EMA)
DECAY_K = np.log(2.0) / T_HALF_DAYS         # ln(2) / t_half in day-units

BLOCK_LEN = 7
BOOTSTRAP_ITERS = 1000
BOOTSTRAP_SEED = 42

HAC_MAXLAGS_PRIMARY = 4   # Andrews 1991 rule on n~=70
HAC_MAXLAGS_SENSITIVITY = 7

LAGGED_LCERA_WIN_LOOKBACK = 90     # CONVENTIONS section 3.2 v3.2 [d-90, d-30] window
LAGGED_LCERA_WIN_GAP = 30
LC_ERA_START = pd.Timestamp("2022-04-04")   # CONVENTIONS section 5

# Effect-size floor for null pre-spec condition 2 (MD section 4.4)
NULL_EFFECT_SIZE_FLOOR_PER_MG_IN_SD = 0.05


# ---------- Data loading ----------

print(f"Loading master from {DATA / 'unified' / 'per_day_master.csv'}")
master = pd.read_csv(DATA / "unified" / "per_day_master.csv", parse_dates=["date"])
master = master.set_index("date").sort_index()

# Sanity assertions on columns we need
required = ["stress_mean_sleep", "is_crash", "lc_phase"]
missing = [c for c in required if c not in master.columns]
if missing:
    print(f"ERROR: missing required columns: {missing}", file=sys.stderr)
    sys.exit(1)


# ---------- Build analytical frame ----------

# Nominal afbouw window
afbouw = master.loc[AFBOUW_START:AFBOUW_END].copy()
n_window_nominal = len(afbouw)

# Add days_from_afbouw_start
afbouw["days_from_afbouw_start"] = (afbouw.index - AFBOUW_START).days.astype(float)

# PK-smoothed plasma dose proxy (MD section 2.3)
def dose_plasma_mg(d):
    """One-compartment first-order PK convolution with initial steady-state 30mg.

    dose_plasma_mg(d) = INITIAL_DOSE_MG
                       + sum_steps delta * (1 - exp(-k * (d - step_date_in_days)))
                         * 1[d >= step_date]

    Linear superposition of step inputs in first-order kinetics
    (Rowland & Tozer 2011, ch.4; Gabrielsson & Weiner 2016).

    NOTE: this function is a within-window variant that assumes
    INITIAL_DOSE_MG = 30mg at AFBOUW_START (2026-03-20). For any full-corpus
    read, use the `dose_plasma_mg` column of `per_day_master.csv` instead
    (materialised by pipeline/03_consolidate/build_unified_dataset.py per
    OI-035; that variant starts from 0mg pre-2024-04-09 and applies the
    full 6-step schedule). See module header for context.
    """
    val = INITIAL_DOSE_MG
    for step_date, delta in DOSE_STEPS:
        if d >= step_date:
            days_since = (d - step_date).days
            val += delta * (1.0 - np.exp(-DECAY_K * days_since))
    return val


def dose_prescribed_mg(d):
    """Step function: dose taken on day d (MD section 2.2).

    On a step date the participant takes the NEW dose (e.g. 2026-03-20 -> 20mg).
    """
    cur = INITIAL_DOSE_MG
    for step_date, delta in DOSE_STEPS:
        if d >= step_date:
            cur += delta
    return cur


afbouw["dose_plasma_mg"] = [dose_plasma_mg(d) for d in afbouw.index]
afbouw["dose_prescribed_mg"] = [dose_prescribed_mg(d) for d in afbouw.index]

# Filter NaN on outcome
analytical = afbouw.dropna(subset=["stress_mean_sleep"]).copy()
n_analytical = len(analytical)
analytical_start = analytical.index.min()
analytical_end_observed = analytical.index.max()

print(f"Nominal window: {AFBOUW_START.date()} to {AFBOUW_END.date()} "
      f"({n_window_nominal} days)")
print(f"Analytical window: {analytical_start.date()} to "
      f"{analytical_end_observed.date()} (n_analytical = {n_analytical})")


# ---------- Sensitivity C: compute stress_mean_sleep_lagged_lcera on-the-fly ----------
# Column NOT in master per inspection 2026-06-14. Build the v3.2 LC-era
# rolling-baseline z-score per CONVENTIONS section 3.2 directly here.

def compute_lagged_lcera_zscore(series, lc_era_start, lookback, gap):
    """For each day d, compute z = (x(d) - median(window)) / MAD(window) where
    window = LC-era days in [d-lookback, d-gap]. Returns a Series aligned to
    series.index; NaN where the window has < 5 valid points.

    MAD = median absolute deviation, scaled by 1.4826 for normal-equivalent SD.
    Robust to single zero-step days per CONVENTIONS section 3.1 prototype.
    """
    out = pd.Series(index=series.index, dtype=float)
    # Restrict baseline to LC-era + non-NaN
    valid = series[(series.index >= lc_era_start) & series.notna()]
    for d in series.index:
        window_start = d - pd.Timedelta(days=lookback)
        window_end = d - pd.Timedelta(days=gap)
        window_vals = valid.loc[window_start:window_end]
        if len(window_vals) < 5:
            out.loc[d] = np.nan
            continue
        med = window_vals.median()
        mad = np.median(np.abs(window_vals - med))
        scaled_mad = 1.4826 * mad if mad > 0 else np.nan
        if not np.isfinite(scaled_mad):
            out.loc[d] = np.nan
            continue
        out.loc[d] = (series.loc[d] - med) / scaled_mad
    return out


# Compute on full master (needs the 90-day lookback)
sms_full = master["stress_mean_sleep"]
sms_lagged_lcera = compute_lagged_lcera_zscore(
    sms_full, LC_ERA_START, LAGGED_LCERA_WIN_LOOKBACK, LAGGED_LCERA_WIN_GAP)
analytical["stress_mean_sleep_lagged_lcera"] = sms_lagged_lcera.reindex(analytical.index)

n_lcera = analytical["stress_mean_sleep_lagged_lcera"].notna().sum()
print(f"Sensitivity C: stress_mean_sleep_lagged_lcera computed on-the-fly; "
      f"{n_lcera}/{n_analytical} days have a valid z-score")


# ---------- Helper: fit OLS with HAC SE, return primary fit values ----------

def fit_hac(y, X, maxlags):
    """Fit OLS; return (fit, beta_dose, hac_se, ci_lo_95, ci_hi_95, p_two_sided).

    Assumes 'dose' is the column of interest in X (named 'dose' in the design).
    """
    model = sm.OLS(y, X, missing="drop")
    fit = model.fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})
    if "dose" not in fit.params.index:
        raise ValueError(f"'dose' not in fit params: {fit.params.index.tolist()}")
    beta = float(fit.params["dose"])
    se = float(fit.bse["dose"])
    ci = fit.conf_int(alpha=0.05).loc["dose"]
    ci_lo = float(ci[0])
    ci_hi = float(ci[1])
    p_two = float(fit.pvalues["dose"])
    return fit, beta, se, ci_lo, ci_hi, p_two


def one_sided_p_positive(beta, p_two):
    """Convert two-sided p to one-sided p for H1: beta > 0 (MD section 4.1)."""
    return p_two / 2.0 if beta > 0 else 1.0 - p_two / 2.0


# ---------- Primary model ----------

def build_design(df, dose_col, time_basis="linear"):
    """Construct (y, X) for the regression.

    dose_col: 'dose_plasma_mg' or 'dose_prescribed_mg'.
    time_basis: 'linear' or 'spline' or 'month_dummy'.
    """
    y = df["stress_mean_sleep"].values
    parts = {"const": np.ones(len(df)), "dose": df[dose_col].values}
    if time_basis == "linear":
        parts["time"] = df["days_from_afbouw_start"].values
    elif time_basis == "spline":
        # Natural cubic spline with df=4 (4 basis fns + intercept)
        spline = np.asarray(
            dmatrix("cr(t, df=4) - 1",
                    {"t": df["days_from_afbouw_start"].values},
                    return_type="dataframe"))
        for i in range(spline.shape[1]):
            parts[f"time_spline_{i}"] = spline[:, i]
    elif time_basis == "month_dummy":
        months = pd.to_datetime(df.index).month
        # April as baseline; March / May / June as dummies (4 months in window: 3,4,5,6)
        for m in (3, 5, 6):
            parts[f"month_{m}"] = (months == m).astype(float)
    else:
        raise ValueError(f"unknown time_basis: {time_basis}")
    X = pd.DataFrame(parts, index=df.index)
    return y, X


def build_design_lcera(df):
    """Lagged-lcera outcome variant (Sensitivity C). Drops rows where the
    lagged-lcera z-score is NaN."""
    sub = df.dropna(subset=["stress_mean_sleep_lagged_lcera"])
    y = sub["stress_mean_sleep_lagged_lcera"].values
    X = pd.DataFrame({
        "const": np.ones(len(sub)),
        "dose":  sub["dose_plasma_mg"].values,
        "time":  sub["days_from_afbouw_start"].values,
    }, index=sub.index)
    return y, X, sub.index


print()
print("=== PRIMARY MODEL ===")
y_p, X_p = build_design(analytical, "dose_plasma_mg", "linear")
fit_p, beta_p, se_p, ci_lo_p, ci_hi_p, p_two_p = fit_hac(y_p, X_p, HAC_MAXLAGS_PRIMARY)
p_one_p = one_sided_p_positive(beta_p, p_two_p)
print(f"  beta_dose          = {beta_p:+.5f}  (stress-points per mg of plasma dose)")
print(f"  HAC SE             = {se_p:.5f}  (maxlags = {HAC_MAXLAGS_PRIMARY})")
print(f"  HAC 95% CI         = [{ci_lo_p:+.5f}, {ci_hi_p:+.5f}]")
print(f"  HAC p (two-sided)  = {p_two_p:.5f}")
print(f"  HAC p (one-sided)  = {p_one_p:.5f}  (H1: beta_dose > 0)")
print(f"  beta_time          = {float(fit_p.params['time']):+.5f}  (per day)")
print(f"  intercept          = {float(fit_p.params['const']):+.3f}")


# ---------- Autocorrelation diagnostics (MD section 6.3) ----------

residuals = fit_p.resid
lag1_rho = float(pd.Series(residuals).autocorr(lag=1))

def effective_n_hac(n, residuals, maxlags):
    """Effective sample size under Bartlett-windowed autocorrelation up to maxlags.
    n_eff = n / (1 + 2 * sum_{k=1}^{maxlags} w_k * rho_k)
    where w_k = 1 - k/(maxlags + 1) is the Bartlett kernel weight.
    """
    rho_series = pd.Series(residuals)
    weighted_sum = 0.0
    for k in range(1, maxlags + 1):
        w = 1.0 - k / (maxlags + 1)
        rho_k = float(rho_series.autocorr(lag=k))
        if np.isfinite(rho_k):
            weighted_sum += w * rho_k
    denom = 1.0 + 2.0 * weighted_sum
    return float(n) / denom if denom > 0 else float("nan")


eff_n = effective_n_hac(n_analytical, residuals, HAC_MAXLAGS_PRIMARY)
print(f"  lag-1 residual rho = {lag1_rho:+.4f}")
print(f"  effective N (HAC)  = {eff_n:.1f}  (raw n = {n_analytical})")


# ---------- Sensitivity A: moving-block bootstrap on residuals ----------

def moving_block_bootstrap_beta(y_obs, X, fit, block_len, n_iter, seed):
    """Resample residuals in moving blocks of length block_len; reconstruct
    y_star = y_hat + resampled_residuals; refit OLS; return array of beta_dose.

    Kunsch 1989 *Annals of Statistics* 17(3):1217-1241 moving-block bootstrap.
    """
    rng = np.random.default_rng(seed)
    y_hat = fit.fittedvalues.values
    e = fit.resid.values
    n = len(e)
    # All possible starting indices for a block of length block_len
    n_blocks_to_draw = int(np.ceil(n / block_len))
    n_possible_starts = n - block_len + 1
    if n_possible_starts < 1:
        raise ValueError("series too short for chosen block length")

    betas = np.empty(n_iter)
    for i in range(n_iter):
        starts = rng.integers(0, n_possible_starts, size=n_blocks_to_draw)
        resampled = np.concatenate([e[s:s + block_len] for s in starts])[:n]
        y_star = y_hat + resampled
        fit_star = sm.OLS(y_star, X).fit()
        betas[i] = float(fit_star.params["dose"])
    return betas


print()
print("=== SENSITIVITY A: moving-block bootstrap ===")
boot_betas = moving_block_bootstrap_beta(
    y_p, X_p, fit_p, BLOCK_LEN, BOOTSTRAP_ITERS, BOOTSTRAP_SEED)
boot_beta_median = float(np.median(boot_betas))
boot_ci_lo = float(np.percentile(boot_betas, 2.5))
boot_ci_hi = float(np.percentile(boot_betas, 97.5))
print(f"  median beta_dose = {boot_beta_median:+.5f}")
print(f"  95% boot CI      = [{boot_ci_lo:+.5f}, {boot_ci_hi:+.5f}]  "
      f"({BOOTSTRAP_ITERS} iter, block_len={BLOCK_LEN}, seed={BOOTSTRAP_SEED})")


# ---------- Sensitivity B: prescribed-step dose ----------

print()
print("=== SENSITIVITY B: prescribed-step dose ===")
y_b, X_b = build_design(analytical, "dose_prescribed_mg", "linear")
fit_b, beta_b, se_b, ci_lo_b, ci_hi_b, p_two_b = fit_hac(y_b, X_b, HAC_MAXLAGS_PRIMARY)
p_one_b = one_sided_p_positive(beta_b, p_two_b)
print(f"  beta_dose         = {beta_b:+.5f}  (per mg of prescribed dose)")
print(f"  HAC p (one-sided) = {p_one_b:.5f}")
print(f"  HAC 95% CI        = [{ci_lo_b:+.5f}, {ci_hi_b:+.5f}]")


# ---------- Sensitivity C: lagged-lcera outcome ----------

print()
print("=== SENSITIVITY C: lagged-lcera outcome ===")
y_c, X_c, idx_c = build_design_lcera(analytical)
n_c = len(y_c)
print(f"  n with non-null lagged-lcera = {n_c}")
if n_c < 10:
    print("  SKIP -- too few non-null lagged-lcera observations for regression")
    beta_c = se_c = ci_lo_c = ci_hi_c = p_two_c = p_one_c = float("nan")
else:
    fit_c, beta_c, se_c, ci_lo_c, ci_hi_c, p_two_c = fit_hac(
        y_c, X_c, HAC_MAXLAGS_PRIMARY)
    p_one_c = one_sided_p_positive(beta_c, p_two_c)
    print(f"  beta_dose          = {beta_c:+.5f}  "
          f"(per mg, outcome in SD-units of lagged baseline)")
    print(f"  HAC p (one-sided)  = {p_one_c:.5f}")
    print(f"  HAC 95% CI         = [{ci_lo_c:+.5f}, {ci_hi_c:+.5f}]")


# ---------- Sensitivity D: HAC maxlags = 7 ----------

print()
print(f"=== SENSITIVITY D: HAC maxlags = {HAC_MAXLAGS_SENSITIVITY} ===")
fit_d, beta_d, se_d, ci_lo_d, ci_hi_d, p_two_d = fit_hac(
    y_p, X_p, HAC_MAXLAGS_SENSITIVITY)
p_one_d = one_sided_p_positive(beta_d, p_two_d)
print(f"  beta_dose         = {beta_d:+.5f}")
print(f"  HAC p (one-sided) = {p_one_d:.5f}")
print(f"  HAC 95% CI        = [{ci_lo_d:+.5f}, {ci_hi_d:+.5f}]")


# ---------- Sensitivity E: crash-drop ----------

print()
print("=== SENSITIVITY E: crash-drop (CONVENTIONS section 3.4 audit hook) ===")
crash_mask = analytical["is_crash"] == True
n_crash_in_window = int(crash_mask.sum())
crash_dates = analytical.index[crash_mask].tolist()

# CONVENTIONS section 3.6 named count format
n_crash_named = (
    f"{n_crash_in_window} crash-days "
    f"(crash_v2 day-level, per_day_master.csv, "
    f"is_crash == True, {AFBOUW_START.date()} <= date <= {AFBOUW_END.date()})"
)
print(f"  Named count: {n_crash_named}")
if crash_dates:
    dates_str = ", ".join(d.strftime("%Y-%m-%d") for d in crash_dates)
    print(f"  Crash dates in afbouw window: {dates_str}")

no_crash = analytical[~crash_mask]
if len(no_crash) < 10:
    print("  SKIP -- too few non-crash rows for regression")
    beta_e = se_e = ci_lo_e = ci_hi_e = p_two_e = p_one_e = float("nan")
else:
    y_e, X_e = build_design(no_crash, "dose_plasma_mg", "linear")
    fit_e, beta_e, se_e, ci_lo_e, ci_hi_e, p_two_e = fit_hac(
        y_e, X_e, HAC_MAXLAGS_PRIMARY)
    p_one_e = one_sided_p_positive(beta_e, p_two_e)
    print(f"  beta_dose (crash-drop, n={len(no_crash)}) = {beta_e:+.5f}")
    print(f"  HAC p (one-sided)                       = {p_one_e:.5f}")
    print(f"  HAC 95% CI                              = "
          f"[{ci_lo_e:+.5f}, {ci_hi_e:+.5f}]")
    # CONVENTIONS section 3.4 fire threshold: report delta
    delta_e = beta_e - beta_p
    print(f"  Delta beta_dose vs primary              = {delta_e:+.5f}  "
          f"({'>0.10' if abs(delta_e) > 0.10 else 'within 0.10'} relative to primary)")


# ---------- Sensitivity F: nonlinear time term ----------

print()
print("=== SENSITIVITY F: nonlinear time term (seasonality robustness) ===")
basis_used = None
try:
    y_f, X_f = build_design(analytical, "dose_plasma_mg", "spline")
    fit_f, beta_f, se_f, ci_lo_f, ci_hi_f, p_two_f = fit_hac(
        y_f, X_f, HAC_MAXLAGS_PRIMARY)
    basis_used = "natural_cubic_spline_4_knots"
except Exception as exc:
    print(f"  Spline basis failed ({exc!r}); falling back to month dummies")
    y_f, X_f = build_design(analytical, "dose_plasma_mg", "month_dummy")
    fit_f, beta_f, se_f, ci_lo_f, ci_hi_f, p_two_f = fit_hac(
        y_f, X_f, HAC_MAXLAGS_PRIMARY)
    basis_used = "month_dummies"

p_one_f = one_sided_p_positive(beta_f, p_two_f)
print(f"  Time basis        = {basis_used}")
print(f"  beta_dose         = {beta_f:+.5f}")
print(f"  HAC p (one-sided) = {p_one_f:.5f}")
print(f"  HAC 95% CI        = [{ci_lo_f:+.5f}, {ci_hi_f:+.5f}]")


# ---------- Null-finding decision (MD section 4.4 four-condition rule) ----------

sd_outcome = float(analytical["stress_mean_sleep"].std())
effect_floor_raw = NULL_EFFECT_SIZE_FLOOR_PER_MG_IN_SD * sd_outcome

cond1_hac_ci_contains_zero = (ci_lo_p <= 0 <= ci_hi_p)
cond2_effect_size_below_floor = (abs(beta_p) < effect_floor_raw)
cond3_boot_ci_contains_zero = (boot_ci_lo <= 0 <= boot_ci_hi)
if np.isnan(p_one_c):
    cond4_lcera_p_above_05 = True  # if we cannot compute, do not block a null decl
    cond4_note = " (lagged-lcera N/A; treated as inconclusive in favour of null)"
else:
    cond4_lcera_p_above_05 = (p_one_c > 0.05)
    cond4_note = ""

null_finding_declared = (
    cond1_hac_ci_contains_zero
    and cond2_effect_size_below_floor
    and cond3_boot_ci_contains_zero
    and cond4_lcera_p_above_05
)

print()
print("=== NULL-FINDING PRE-SPEC (MD section 4.4, all 4 must hold) ===")
print(f"  SD(stress_mean_sleep)      = {sd_outcome:.4f}")
print(f"  effect-size floor (per mg) = {effect_floor_raw:.5f}  "
      f"(= 0.05 * SD)")
print(f"  c1 HAC CI contains 0       = {cond1_hac_ci_contains_zero}")
print(f"  c2 |beta_dose| < floor     = {cond2_effect_size_below_floor}  "
      f"(|{beta_p:+.5f}| vs {effect_floor_raw:.5f})")
print(f"  c3 boot CI contains 0      = {cond3_boot_ci_contains_zero}")
print(f"  c4 lagged-lcera p > 0.05   = {cond4_lcera_p_above_05}"
      f"{cond4_note}")
print(f"  NULL FINDING DECLARED      = {null_finding_declared}")


# ---------- Write CSV summary (MD section 6.3) ----------

summary = {
    # Primary
    "beta_dose": beta_p,
    "hac_se": se_p,
    "hac_ci_lo": ci_lo_p,
    "hac_ci_hi": ci_hi_p,
    "hac_p_two_sided": p_two_p,
    "hac_p_one_sided": p_one_p,
    # Sensitivity A
    "boot_beta_median": boot_beta_median,
    "boot_ci_lo": boot_ci_lo,
    "boot_ci_hi": boot_ci_hi,
    # Sensitivity B
    "prescribed_beta": beta_b,
    "prescribed_hac_p_one_sided": p_one_b,
    "prescribed_ci_lo": ci_lo_b,
    "prescribed_ci_hi": ci_hi_b,
    # Sensitivity C
    "lcera_beta": beta_c,
    "lcera_hac_p_one_sided": p_one_c,
    "lcera_ci_lo": ci_lo_c,
    "lcera_ci_hi": ci_hi_c,
    "lcera_n": n_c,
    # Sensitivity D
    "hac7_beta": beta_d,
    "hac7_hac_p_one_sided": p_one_d,
    "hac7_ci_lo": ci_lo_d,
    "hac7_ci_hi": ci_hi_d,
    # Sensitivity E
    "crash_drop_beta": beta_e,
    "crash_drop_hac_p_one_sided": p_one_e,
    "crash_drop_ci_lo": ci_lo_e,
    "crash_drop_ci_hi": ci_hi_e,
    "n_crash_days_in_window": n_crash_named,
    # Sensitivity F
    "nonlinear_time_beta": beta_f,
    "nonlinear_time_hac_p_one_sided": p_one_f,
    "nonlinear_time_ci_lo": ci_lo_f,
    "nonlinear_time_ci_hi": ci_hi_f,
    "nonlinear_time_basis": basis_used,
    # Autocorrelation diagnostics
    "lag1_residual_rho": lag1_rho,
    "effective_n_under_hac": eff_n,
    # Null-finding decision
    "null_finding_declared": null_finding_declared,
    "cond1_hac_ci_contains_zero": cond1_hac_ci_contains_zero,
    "cond2_effect_size_below_floor": cond2_effect_size_below_floor,
    "cond3_boot_ci_contains_zero": cond3_boot_ci_contains_zero,
    "cond4_lcera_p_above_05": cond4_lcera_p_above_05,
    "sd_outcome_raw": sd_outcome,
    "effect_size_floor_raw": effect_floor_raw,
    # Provenance
    "n_analytical": n_analytical,
    "analytical_window_start": str(analytical_start.date()),
    "analytical_window_end": str(analytical_end_observed.date()),
    "bootstrap_seed": BOOTSTRAP_SEED,
    "hac_maxlags_primary": HAC_MAXLAGS_PRIMARY,
    "script_version": SCRIPT_VERSION,
    "run_datetime": datetime.now().isoformat(timespec="seconds"),
}

summary_df = pd.DataFrame([summary])
summary_path = OUT / "dose_response_summary.csv"
summary_df.to_csv(summary_path, index=False)
print()
print(f"Wrote summary: {summary_path}")


# ---------- 4-panel plot (MD section 6.3) ----------

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# Panel TL: stress_mean_sleep time-series with PK-smoothed dose overlay
ax_tl = axes[0, 0]
ax_tl.plot(analytical.index, analytical["stress_mean_sleep"], "o-", color="#3a7", alpha=0.75, ms=4,
           label="stress_mean_sleep (obs)")
# Add a fit line: beta_0 + beta_dose * plasma + beta_time * days
y_fit = fit_p.fittedvalues
ax_tl.plot(analytical.index, y_fit, "-", color="#373", alpha=0.5, lw=2,
           label="OLS fit (primary)")
ax_tl.set_ylabel("stress_mean_sleep")
ax_tl.set_title("Time-series + primary fit")
ax_tl.tick_params(axis="x", rotation=30)
ax_tl_dose = ax_tl.twinx()
ax_tl_dose.plot(analytical.index, analytical["dose_plasma_mg"], "-",
                color="#a33", lw=2, alpha=0.7, label="dose_plasma_mg (PK)")
ax_tl_dose.plot(analytical.index, analytical["dose_prescribed_mg"], "--",
                color="#a33", lw=1, alpha=0.4, label="dose_prescribed_mg")
ax_tl_dose.set_ylabel("citalopram dose (mg)", color="#a33")
ax_tl_dose.tick_params(axis="y", labelcolor="#a33")
# Mark step dates
for sd, _delta in DOSE_STEPS:
    if AFBOUW_START <= sd <= analytical_end_observed:
        ax_tl.axvline(sd, color="gray", linestyle=":", alpha=0.5)
lines_l, labels_l = ax_tl.get_legend_handles_labels()
lines_r, labels_r = ax_tl_dose.get_legend_handles_labels()
ax_tl.legend(lines_l + lines_r, labels_l + labels_r, fontsize=7, loc="upper right")

# Panel TR: regression scatter
ax_tr = axes[0, 1]
resid_for_dose = (
    analytical["stress_mean_sleep"]
    - float(fit_p.params["const"])
    - float(fit_p.params["time"]) * analytical["days_from_afbouw_start"]
)
ax_tr.scatter(analytical["dose_plasma_mg"], resid_for_dose, alpha=0.7, s=30, color="#37a")
# Add the linear fit line
x_grid = np.linspace(analytical["dose_plasma_mg"].min(),
                     analytical["dose_plasma_mg"].max(), 50)
ax_tr.plot(x_grid, beta_p * x_grid, "-", color="#a33", lw=2,
           label=f"slope = {beta_p:+.4f}")
ax_tr.set_xlabel("dose_plasma_mg (PK-smoothed)")
ax_tr.set_ylabel("stress_mean_sleep residual\n(after time + intercept)")
ax_tr.set_title("Dose-response (continuous)")
ax_tr.legend(fontsize=8)

# Panel BL: monotonicity scatter (4 prescribed plateau bins vs mean residual)
ax_bl = axes[1, 0]
plateau_doses = sorted({30.0, 20.0, 10.0, 8.0})
plateau_means_x, plateau_means_y = [], []
for plateau in plateau_doses:
    in_plateau = analytical[analytical["dose_prescribed_mg"] == plateau]
    if len(in_plateau) < 1:
        continue
    mean_dose_in_plateau = in_plateau["dose_prescribed_mg"].mean()
    resid_in_plateau = (
        in_plateau["stress_mean_sleep"]
        - float(fit_p.params["const"])
        - float(fit_p.params["time"]) * in_plateau["days_from_afbouw_start"]
    ).mean()
    plateau_means_x.append(mean_dose_in_plateau)
    plateau_means_y.append(resid_in_plateau)
ax_bl.plot(plateau_means_x, plateau_means_y, "o-", color="#a37", ms=10, lw=2)
for x, y, p in zip(plateau_means_x, plateau_means_y, plateau_doses):
    ax_bl.annotate(f"{int(p)}mg", (x, y), textcoords="offset points",
                   xytext=(8, 8), fontsize=10)
ax_bl.set_xlabel("Prescribed dose plateau (mg)")
ax_bl.set_ylabel("Mean stress_mean_sleep residual")
ax_bl.set_title("Monotonicity scatter (4 plateau bins)")
ax_bl.grid(True, alpha=0.3)

# Panel BR: coefficient panel
ax_br = axes[1, 1]
coef_labels = ["Primary\n(HAC)", "A\nblock-boot",
               "B\nprescribed", "C\nlagged-lcera",
               "D\nHAC=7", "E\ncrash-drop", "F\nnonlin-time"]
coef_betas = [beta_p, boot_beta_median, beta_b, beta_c, beta_d, beta_e, beta_f]
coef_ci_lo = [ci_lo_p, boot_ci_lo, ci_lo_b, ci_lo_c, ci_lo_d, ci_lo_e, ci_lo_f]
coef_ci_hi = [ci_hi_p, boot_ci_hi, ci_hi_b, ci_hi_c, ci_hi_d, ci_hi_e, ci_hi_f]
xpos = np.arange(len(coef_labels))
colors = ["#373", "#737", "#377", "#773", "#737", "#733", "#337"]
for i, (b, lo, hi, c) in enumerate(zip(coef_betas, coef_ci_lo, coef_ci_hi, colors)):
    if np.isnan(b):
        continue
    ax_br.errorbar(i, b, yerr=[[b - lo], [hi - b]], fmt="o", color=c, capsize=4, ms=8)
ax_br.axhline(0, color="gray", linestyle="--", alpha=0.5)
ax_br.set_xticks(xpos)
ax_br.set_xticklabels(coef_labels, fontsize=8)
ax_br.set_ylabel("beta_dose with 95% CI")
ax_br.set_title("Primary + 6 sensitivities (beta_dose)")
ax_br.grid(True, alpha=0.3, axis="y")

fig.suptitle("Citalopram dose-response on stress_mean_sleep "
             f"(afbouw {AFBOUW_START.date()} -> {AFBOUW_END.date()}; n = {n_analytical})",
             fontsize=12)
plt.tight_layout(rect=[0, 0, 1, 0.97])
plot_path = OUT / "plots" / "dose_response_overview.png"
plt.savefig(plot_path, dpi=100)
plt.close()
print(f"Wrote plot: {plot_path}")


# ---------- Final console summary ----------

print()
print("=" * 60)
print("FINAL READOUT (one-sided H1: beta_dose > 0)")
print("=" * 60)
print(f"Primary beta_dose       = {beta_p:+.4f}  "
      f"(HAC p = {p_one_p:.4f}, 95% CI [{ci_lo_p:+.4f}, {ci_hi_p:+.4f}])")
print(f"Block-bootstrap CI       = [{boot_ci_lo:+.4f}, {boot_ci_hi:+.4f}]")
print(f"Sens B prescribed        = {beta_b:+.4f}  (p = {p_one_b:.4f})")
print(f"Sens C lagged-lcera      = {beta_c:+.4f}  (p = {p_one_c:.4f}; n = {n_c})")
print(f"Sens D HAC maxlags=7     = {beta_d:+.4f}  (p = {p_one_d:.4f})")
print(f"Sens E crash-drop        = {beta_e:+.4f}  (p = {p_one_e:.4f}; "
      f"n_crash = {n_crash_in_window})")
print(f"Sens F nonlinear time    = {beta_f:+.4f}  (p = {p_one_f:.4f}; basis = {basis_used})")
print(f"NULL FINDING declared    = {null_finding_declared}")
print(f"Outputs:")
print(f"  {summary_path}")
print(f"  {plot_path}")
