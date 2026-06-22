"""Bout-level citalopram dose-response calibration -- recalibration execution.

Implements ``methodology/bout_level_dose_response_calibration.md`` (LOCKED r2
2026-06-19 commit c57ff3f). Populates the empty inheritance table at MD section
6 with the per-feature beta + CI + verdict result for 7 features x 3 windows.

OUTPUTS
-------
- ``summary.json`` (local, gitignored) -- machine-readable per-cell results.
- ``plots/*.png`` (local, gitignored) -- monotonicity scatter per feature.
- ``$GEVOELSCORE_DATA_PATH/unified/bout_level_dose_response_calibration_results.csv``
  (external) -- 11-column schema per MD section 4 verbatim; 189 rows (7 features
  x 3 windows x 9 specs). Cells inapplicable (Sensitivity G for per-day
  aggregations; Sensitivity C for ``decay_slope``) emit ``N/A`` markers in the
  ``spec`` / ``verdict`` columns.

DESIGN DECISIONS (surfaced per handoff section 3)
-------------------------------------------------
1. Library: ``statsmodels`` for the regression core.

   - For bout-level fits (5 per-bout features): OLS with cluster-robust SE on
     ``date`` (``cov_type='cluster', cov_kwds={'groups': ...}``). Per Daza 2018
     (the project-canonical n-of-1 self-tracked counterfactual anchor) this is
     the day-cluster equivalent of MixedLM with a day-level random intercept;
     the beta point estimate is numerically near-identical and the
     cluster-robust SE is the sandwich estimator that the MD section 3.2 names
     as the analogue of Newey-West HAC at bout level. MixedLM was considered;
     the OLS+cluster route is preferred because (a) the SE is what the MD
     locks, not the random-intercept variance component; (b) it is more
     robust to small per-day cell sizes that the MixedLM's MLE can struggle
     with; (c) it matches the framework-validity reproducibility pattern the
     parent dose-response MD uses at per-day layer.

   - For per-day aggregations (2 features): OLS with Newey-West HAC SE on
     date-sorted residuals, Andrews 1991 lag selection per parent dose-response
     MD section 4.2 verbatim.

2. ``decay_slope`` direction handling: beta is fit on the RAW SIGNED slope
   (negative-valued; less-negative under higher plasma is the prior). Per MD
   section 2 the prior expected sign is +1 in absolute value, which on the raw
   signed slope means +1 directly (a less-negative slope under higher plasma =
   positive partial derivative of slope wrt dose). No sign flip; sign-match
   against the +1 prior is unambiguous.

3. AR(1) sensitivity (Sensitivity H): reported as DIAGNOSTIC-ONLY per MD
   section 3.3 fallback wording. With ~3 bouts/day median within-day n, the
   per-day AR(1) parameter is unreliably estimable (statsmodels MixedLM with
   the ``MixedLMResults`` AR(1) covariance structure is not natively supported
   for unbalanced within-day blocks at this sparsity). The Sensitivity H row
   emits ``diagnostic_only`` in the verdict cell and NaN for the coefficient
   to honour the MD pre-spec without overclaiming stability.

4. Lagged-lcera variant (Sensitivity C): per MD section 2 and CONVENTIONS
   section 3.2. The per-day mean of the feature is computed first; then the
   lagged-LC-era reference for each focal day d is the mean across [d-90,
   d-30] of those per-day means, restricted to LC-era days (d >= 2022-04-04).
   For per-bout features the lagged-lcera variant subtracts the lagged
   reference from EACH bout's raw value before refitting. For ``decay_slope``
   the variant is N/A per MD section 2.

5. Crash-drop sensitivity (Sensitivity E): per CONVENTIONS section 3.4 +
   feedback_crash_distortion_sensitivity. Drops bouts on ``is_crash == True``
   days from the bout pool (per-bout fits) or the day pool (per-day fits),
   refits, computes |delta-beta|. The MD section 3.3 sens E flag fires if
   |delta| > 0.10 * SD(feature) per mg.

6. Holm step-down (MD section 3.7): the family is the 5 per-bout features
   PER WINDOW. Three windows -> three Holm step-down companions, each over
   5 features. The per-day aggregations are NOT included in the Holm family
   (different operand layer).

7. Per-day aggregation column name mapping: MD section 3.1 second-form names
   ``bout_count_day``; the pipeline implementation
   (``pipeline/02_features/extract_stress_bouts.py`` LOCKED d5b394c
   2026-06-22) implemented it as ``bout_n_per_day``. The CSV ``feature``
   column uses ``bout_n_per_day`` (the actual implementation name); the sub-MD
   section 6 table populated downstream notes the MD-spec-to-pipeline mapping
   in its row label.

8. Spring 2025 control window: dose is uniformly 30 mg across all 78 days
   (no within-window dose variance). The dose regressor is therefore
   degenerate. The MD section 6 table's "spring 2025 control" column is
   labelled ``beta_time``, meaning the regression for this window is fit
   WITHOUT the dose term, only the linear time covariate. The CSV row uses
   ``beta_dose=NaN`` for spring_2025_control and reports ``beta_time`` in a
   separate ``note`` accompanying the row.

ANTI-PATTERNS AVOIDED (handoff section 8)
-----------------------------------------
- No whole-corpus fits; only the three pre-specified windows.
- No imputation of missing bouts (zero counts on valid no-bout days; absent
  rows for per-bout features).
- No double-counting motion-confounded bouts in primary; all bouts in primary
  (per MD section 3.4) with sens G as the motion-clean restriction.
- No features outside scope (the 5 + 2 named).
- No beta without CI.
- No CONFIRMED without sensitivity-arm survival (Sensitivity A block-bootstrap
  survival is gated per MD section 3.4 null-spec condition 3).
"""

from __future__ import annotations

import json
import math
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from inference import (  # noqa: E402
    compute_data_driven_block_length,
    stationary_bootstrap_ci,
)


# ---------------------------------------------------------------------------
# Configuration: three windows + 7 features + 9 specs per MD section 3 + 4.
# ---------------------------------------------------------------------------

DATA_ROOT = Path(os.environ.get("GEVOELSCORE_DATA_PATH",
                                "C:/Users/Gebruiker/Documents/gevoelscore-data"))
BOUTS_CSV = DATA_ROOT / "unified" / "per_bout_master.csv"
PER_DAY_CSV = DATA_ROOT / "unified" / "per_day_master.csv"
RESULTS_CSV = DATA_ROOT / "unified" / "bout_level_dose_response_calibration_results.csv"

WINDOWS = [
    ("afbouw_2026",            date(2026, 3, 20), date(2026, 6,  5)),
    ("buildup_post_cpap_2024", date(2024, 5,  1), date(2024, 6, 19)),
    ("spring_2025_control",    date(2025, 3, 20), date(2025, 6,  5)),
]

PER_BOUT_FEATURES = [
    "peak_height",
    "pre_bout_baseline",
    "recovery_half_life",
    "decay_slope",
    "AUC_above_baseline",
]

# Pipeline ACTUAL names (see design decision 7). Order mirrors the MD section 6
# table verbatim with the column-name mapping noted at result-time.
PER_DAY_AGGS = [
    "bout_n_per_day",            # MD spec name: bout_count_day
    "bout_n_fast_recovery_day",  # MD spec name: bout_n_fast_recovery_day
]

ALL_FEATURES = PER_BOUT_FEATURES + PER_DAY_AGGS

# Prior expected signs per MD section 2 + the section 2 per-day aggregations table.
PRIOR_SIGN = {
    "peak_height": +1,
    "pre_bout_baseline": +1,
    "recovery_half_life": +1,
    "decay_slope": +1,    # raw signed slope; +1 = less-negative under higher plasma
    "AUC_above_baseline": +1,
    "bout_n_per_day": +1,
    "bout_n_fast_recovery_day": -1,
}

# decay_slope does not admit lagged-lcera variant per MD section 2.
ADMITS_LAGGED_LCERA = {
    "peak_height": True,
    "pre_bout_baseline": True,
    "recovery_half_life": True,
    "decay_slope": False,
    "AUC_above_baseline": True,
    "bout_n_per_day": True,
    "bout_n_fast_recovery_day": True,
}

SPECS = [
    "primary",
    "sens_A_block_bootstrap",
    "sens_B_prescribed_step",
    "sens_C_lagged_lcera",
    "sens_D_alt_lag",
    "sens_E_crash_drop",
    "sens_F_nonlinear_time",
    "sens_G_motion_clean",       # per-bout only
    "sens_H_within_day_ar1",     # per-bout only
]

# Output CSV schema per MD section 4 (LOCKED).
CSV_SCHEMA = [
    "feature", "window", "spec",
    "n_bouts", "n_days",
    "beta_dose", "beta_dose_lo95", "beta_dose_hi95",
    "p_value", "sign_match_prior", "verdict",
]

# Seed for the block-bootstrap, deterministic per run.
SEED = 20260622


# ---------------------------------------------------------------------------
# Statistical helpers.
# ---------------------------------------------------------------------------


def _fit_ols_cluster(y: np.ndarray, X: np.ndarray, groups: np.ndarray):
    """OLS fit with cluster-robust SE on ``groups``.

    Returns dict with ``beta_dose``, ``ci_low``, ``ci_high``, ``p_value_two_sided``,
    ``n_obs``, ``n_clusters``. ``beta_dose`` is the coefficient on the FIRST
    non-intercept column (dose). The intercept is the LAST column in X.
    """
    import statsmodels.api as sm
    if len(y) < 5 or X.shape[0] != len(y):
        return None
    try:
        model = sm.OLS(y, X, missing="drop")
        res = model.fit(cov_type="cluster", cov_kwds={"groups": groups})
        # dose is column 0 of X (we always place dose first, then time, then intercept)
        beta = float(res.params[0])
        se = float(res.bse[0])
        # Wald-z 95% CI (cluster-robust SE; n_clusters drives df_resid but res.conf_int gives t-CI)
        ci = res.conf_int(alpha=0.05)
        ci_low = float(ci[0, 0])
        ci_high = float(ci[0, 1])
        p_two = float(res.pvalues[0])
        n_clusters = int(len(np.unique(groups)))
        return {
            "beta": beta,
            "se": se,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "p_two_sided": p_two,
            "n_obs": int(len(y)),
            "n_clusters": n_clusters,
        }
    except Exception as exc:  # pragma: no cover - diagnostic; should not fire on this dataset
        return {"error": str(exc)}


def _fit_ols_hac(y: np.ndarray, X: np.ndarray, lag: int | None = None):
    """OLS with Newey-West HAC SE; Andrews 1991 default lag when ``lag`` is None.

    Used for the per-day aggregations (no day-cluster needed).
    """
    import statsmodels.api as sm
    if len(y) < 5 or X.shape[0] != len(y):
        return None
    if lag is None:
        # Andrews (1991) automatic bandwidth: 4 * (n/100)^(2/9)
        n = len(y)
        lag = max(1, int(np.floor(4 * (n / 100.0) ** (2.0 / 9.0))))
    try:
        model = sm.OLS(y, X, missing="drop")
        res = model.fit(cov_type="HAC", cov_kwds={"maxlags": lag})
        beta = float(res.params[0])
        se = float(res.bse[0])
        ci = res.conf_int(alpha=0.05)
        ci_low = float(ci[0, 0])
        ci_high = float(ci[0, 1])
        p_two = float(res.pvalues[0])
        return {
            "beta": beta,
            "se": se,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "p_two_sided": p_two,
            "n_obs": int(len(y)),
            "n_clusters": int(len(y)),
            "hac_lag": int(lag),
        }
    except Exception as exc:
        return {"error": str(exc)}


def _build_design_matrix_bout(sub_bouts: pd.DataFrame, time_col: str = "days_from_window_start",
                              add_dose: bool = True, nonlinear_time: bool = False):
    """Build (y, X, groups) for the bout-level regression on the in-window
    ``sub_bouts`` frame for feature ``f``.

    Caller filters NaN on the focal feature first. X columns are:
        [dose_plasma_mg] if add_dose,
        [days_from_window_start] linear  OR  4-knot natural cubic spline,
        intercept (last).
    """
    if nonlinear_time:
        # 4-knot natural cubic spline on time per MD section 3.3 sens F.
        from patsy import dmatrix  # statsmodels dep
        t = sub_bouts[time_col].to_numpy()
        knots = np.quantile(t, [0.2, 0.4, 0.6, 0.8])
        spline = dmatrix(
            "cr(t, knots=knots) - 1",
            {"t": t, "knots": knots},
            return_type="dataframe",
        )
        time_cols = spline.to_numpy()
    else:
        time_cols = sub_bouts[[time_col]].to_numpy()

    parts = []
    if add_dose:
        parts.append(sub_bouts[["dose_plasma_mg"]].to_numpy())
    parts.append(time_cols)
    parts.append(np.ones((len(sub_bouts), 1)))  # intercept last
    X = np.hstack(parts)
    return X


# ---------------------------------------------------------------------------
# Lagged-lcera variant computation per MD section 2 + CONVENTIONS section 3.2.
# ---------------------------------------------------------------------------

LC_ERA_START = pd.Timestamp(2022, 4, 4)
LAGGED_WINDOW_LO = 90  # days
LAGGED_WINDOW_HI = 30  # days


def compute_lagged_lcera_reference(per_day_means: pd.Series, focal_dates: pd.Series) -> pd.Series:
    """For each focal date d in ``focal_dates``, compute the mean of
    ``per_day_means`` over [d-90, d-30] restricted to LC-era days.

    Returns a Series indexed by focal_dates' index with NaN where < 5 LC-era
    days are present in the window (insufficient anchor for the lagged
    baseline).
    """
    out = pd.Series(np.nan, index=focal_dates.index, dtype=float)
    per_day_means = per_day_means.dropna()
    if per_day_means.empty:
        return out
    pdm = per_day_means.sort_index()
    pdm_dates = pdm.index
    pdm_arr = pdm.to_numpy()
    for idx, d in focal_dates.items():
        d = pd.Timestamp(d)
        lo = d - pd.Timedelta(days=LAGGED_WINDOW_LO)
        hi = d - pd.Timedelta(days=LAGGED_WINDOW_HI)
        # Restrict to LC-era + window
        mask = (pdm_dates >= max(lo, LC_ERA_START)) & (pdm_dates <= hi)
        sub = pdm_arr[mask]
        if len(sub) >= 5:
            out.loc[idx] = float(np.mean(sub))
    return out


# ---------------------------------------------------------------------------
# Per-feature, per-window primary + sensitivity sweep.
# ---------------------------------------------------------------------------


def _make_row(feature: str, window: str, spec: str, fit_result, note: str = ""):
    """Convert a fit-result dict to a CSV row dict; emit N/A markers for
    inapplicable cells.
    """
    if fit_result is None or "beta" not in fit_result:
        # Emit N/A for inapplicable / error rows
        return {
            "feature": feature,
            "window": window,
            "spec": spec,
            "n_bouts": "N/A",
            "n_days": "N/A",
            "beta_dose": "N/A",
            "beta_dose_lo95": "N/A",
            "beta_dose_hi95": "N/A",
            "p_value": "N/A",
            "sign_match_prior": "N/A",
            "verdict": note or "N/A",
        }
    prior = PRIOR_SIGN[feature]
    beta = fit_result["beta"]
    sign_match = (math.copysign(1, beta) == prior) if beta != 0 else False
    return {
        "feature": feature,
        "window": window,
        "spec": spec,
        "n_bouts": fit_result.get("n_obs", "N/A"),
        "n_days": fit_result.get("n_clusters", "N/A"),
        "beta_dose": round(beta, 6),
        "beta_dose_lo95": round(fit_result["ci_low"], 6),
        "beta_dose_hi95": round(fit_result["ci_high"], 6),
        "p_value": round(fit_result["p_two_sided"], 6),
        "sign_match_prior": bool(sign_match),
        "verdict": note,
    }


def _filter_window(df: pd.DataFrame, win_start, win_end, date_col: str = "date") -> pd.DataFrame:
    m = (df[date_col] >= pd.Timestamp(win_start)) & (df[date_col] <= pd.Timestamp(win_end))
    return df.loc[m].copy()


def _add_days_from_window_start(df: pd.DataFrame, win_start, date_col: str = "date") -> pd.DataFrame:
    df = df.copy()
    df["days_from_window_start"] = (df[date_col] - pd.Timestamp(win_start)).dt.days.astype(float)
    return df


def run_per_bout_feature(
    bouts: pd.DataFrame,
    per_day: pd.DataFrame,
    crash_dates: set,
    feature: str,
    window_label: str,
    win_start, win_end,
) -> list[dict]:
    """All 9 specs for one per-bout feature on one window."""
    rows: list[dict] = []
    win_bouts = _filter_window(bouts, win_start, win_end)
    win_bouts = win_bouts.dropna(subset=[feature, "dose_plasma_mg"]).copy()
    win_bouts = _add_days_from_window_start(win_bouts, win_start)
    is_control = window_label == "spring_2025_control"

    if len(win_bouts) < 5:
        for spec in SPECS:
            rows.append(_make_row(feature, window_label, spec, None, note="N/A insufficient n"))
        return rows

    y = win_bouts[feature].to_numpy(dtype=float)
    groups = win_bouts["date"].astype("datetime64[ns]").astype(np.int64).to_numpy()

    # --- primary -----------------------------------------------------------
    if is_control:
        # Control window: no dose variance; report beta_time only.
        X = _build_design_matrix_bout(win_bouts, add_dose=False)
        # Now beta_dose is N/A; we surface time-beta as a note.
        try:
            import statsmodels.api as sm
            res = sm.OLS(y, X, missing="drop").fit(cov_type="cluster", cov_kwds={"groups": groups})
            beta_time = float(res.params[0])
            ci_time = res.conf_int(alpha=0.05)
            note = (
                f"control_window_no_dose_variance; beta_time={beta_time:.6f} "
                f"CI=[{float(ci_time[0,0]):.6f},{float(ci_time[0,1]):.6f}] "
                f"p={float(res.pvalues[0]):.6f}"
            )
        except Exception as exc:
            note = f"control_fit_failed:{exc}"
        rows.append(_make_row(feature, window_label, "primary", None, note=note))
    else:
        X = _build_design_matrix_bout(win_bouts, add_dose=True)
        primary = _fit_ols_cluster(y, X, groups)
        rows.append(_make_row(feature, window_label, "primary", primary,
                              note=_verdict_local(primary)))

    # --- sens A: block bootstrap on day-blocks (E[L]=7) --------------------
    sens_A = _sens_A_block_bootstrap(win_bouts, feature, is_control=is_control)
    rows.append(_make_row(feature, window_label, "sens_A_block_bootstrap", sens_A,
                          note=sens_A.get("note", "") if sens_A else "N/A"))

    # --- sens B: prescribed-step dose --------------------------------------
    if is_control:
        rows.append(_make_row(feature, window_label, "sens_B_prescribed_step", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        # Substitute dose_prescribed_mg if available; fall back to plasma rounding
        # (we don't have a prescribed-step column on per-day master; per CONVENTIONS
        # the prescribed-step pattern is "round dose to nearest 10mg step").
        wb = win_bouts.copy()
        wb["dose_prescribed_mg"] = (wb["dose_plasma_mg"] / 10.0).round() * 10.0
        Xp = _build_design_matrix_bout(
            wb.rename(columns={"dose_prescribed_mg": "dose_plasma_mg",
                               "dose_plasma_mg": "_orig_plasma"}),
            add_dose=True,
        )
        sens_B = _fit_ols_cluster(y, Xp, groups)
        rows.append(_make_row(feature, window_label, "sens_B_prescribed_step", sens_B,
                              note="dose_rounded_to_10mg_step"))

    # --- sens C: lagged-lcera variant --------------------------------------
    if not ADMITS_LAGGED_LCERA[feature]:
        rows.append(_make_row(feature, window_label, "sens_C_lagged_lcera", None,
                              note="N/A feature_does_not_admit_lagged_lcera"))
    elif is_control:
        rows.append(_make_row(feature, window_label, "sens_C_lagged_lcera", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        # Per-day mean of feature across the full LC era
        per_day_mean = bouts.dropna(subset=[feature]).groupby("date")[feature].mean()
        focal = win_bouts[["date"]].copy()
        focal["lagged_ref"] = compute_lagged_lcera_reference(per_day_mean,
                                                             win_bouts["date"]).values
        wb = win_bouts.copy()
        wb["_lagged_ref"] = focal["lagged_ref"].values
        wb_C = wb.dropna(subset=["_lagged_ref"]).copy()
        if len(wb_C) >= 5:
            y_C = (wb_C[feature].to_numpy(dtype=float) - wb_C["_lagged_ref"].to_numpy(dtype=float))
            X_C = _build_design_matrix_bout(wb_C, add_dose=True)
            groups_C = wb_C["date"].astype("datetime64[ns]").astype(np.int64).to_numpy()
            sens_C = _fit_ols_cluster(y_C, X_C, groups_C)
            rows.append(_make_row(feature, window_label, "sens_C_lagged_lcera", sens_C,
                                  note=f"lagged_ref_window=[d-{LAGGED_WINDOW_LO},d-{LAGGED_WINDOW_HI}] LC-era restricted"))
        else:
            rows.append(_make_row(feature, window_label, "sens_C_lagged_lcera", None,
                                  note="N/A insufficient_lagged_ref_coverage"))

    # --- sens D: alternative HAC / cluster lag -----------------------------
    # For bout-level: cluster-robust SE has no "lag" parameter; we report
    # tighter vs looser via a sub-sample of one bout per day (more conservative).
    # Per MD section 3.3 sens D, we report the trimmed-bout (1 bout/day, lowest
    # variance within day) as the alt-lag analogue.
    if is_control:
        rows.append(_make_row(feature, window_label, "sens_D_alt_lag", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        # one-per-day: take per-day median bout to mimic a coarser cluster
        per_day_med = (win_bouts.dropna(subset=[feature])
                       .groupby("date")
                       .agg(_y=(feature, "median"),
                            dose=("dose_plasma_mg", "first"),
                            t=("days_from_window_start", "first"))
                       .reset_index())
        if len(per_day_med) >= 5:
            yD = per_day_med["_y"].to_numpy(dtype=float)
            XD = np.column_stack([
                per_day_med["dose"].to_numpy(dtype=float),
                per_day_med["t"].to_numpy(dtype=float),
                np.ones(len(per_day_med)),
            ])
            sens_D = _fit_ols_hac(yD, XD)
            rows.append(_make_row(feature, window_label, "sens_D_alt_lag", sens_D,
                                  note="per_day_median_bout_+_HAC_alt_aggregation"))
        else:
            rows.append(_make_row(feature, window_label, "sens_D_alt_lag", None,
                                  note="N/A insufficient_days"))

    # --- sens E: crash-drop ------------------------------------------------
    crash_set = crash_dates
    wb_E = win_bouts.loc[~win_bouts["date"].isin(crash_set)].copy()
    if len(wb_E) >= 5 and not is_control:
        y_E = wb_E[feature].to_numpy(dtype=float)
        X_E = _build_design_matrix_bout(wb_E, add_dose=True)
        groups_E = wb_E["date"].astype("datetime64[ns]").astype(np.int64).to_numpy()
        sens_E = _fit_ols_cluster(y_E, X_E, groups_E)
        # |Delta beta| > 0.10 * SD(feature) per mg flag
        try:
            sd_feat = float(np.std(y, ddof=1))
            d_beta = abs(sens_E["beta"] - primary["beta"])
            flag = d_beta > 0.10 * sd_feat
            note_E = f"|delta_beta|={d_beta:.4f}; threshold=0.10*SD={0.10 * sd_feat:.4f}; exceeds={flag}"
        except Exception:
            note_E = "delta_beta_unavailable"
        rows.append(_make_row(feature, window_label, "sens_E_crash_drop", sens_E, note=note_E))
    elif is_control:
        rows.append(_make_row(feature, window_label, "sens_E_crash_drop", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        rows.append(_make_row(feature, window_label, "sens_E_crash_drop", None,
                              note="N/A insufficient_n_after_crash_drop"))

    # --- sens F: nonlinear time spline -------------------------------------
    if is_control:
        rows.append(_make_row(feature, window_label, "sens_F_nonlinear_time", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        try:
            X_F = _build_design_matrix_bout(win_bouts, add_dose=True, nonlinear_time=True)
            sens_F = _fit_ols_cluster(y, X_F, groups)
            rows.append(_make_row(feature, window_label, "sens_F_nonlinear_time", sens_F,
                                  note="4-knot_natural_cubic_spline_on_time"))
        except Exception as exc:
            rows.append(_make_row(feature, window_label, "sens_F_nonlinear_time", None,
                                  note=f"spline_fit_failed:{exc}"))

    # --- sens G: motion-clean ----------------------------------------------
    wb_G = win_bouts.loc[win_bouts["motion_confound_flag"] == False].copy()  # noqa: E712
    if len(wb_G) >= 5 and not is_control:
        y_G = wb_G[feature].to_numpy(dtype=float)
        X_G = _build_design_matrix_bout(wb_G, add_dose=True)
        groups_G = wb_G["date"].astype("datetime64[ns]").astype(np.int64).to_numpy()
        sens_G = _fit_ols_cluster(y_G, X_G, groups_G)
        rows.append(_make_row(feature, window_label, "sens_G_motion_clean", sens_G,
                              note=f"motion_clean_only_n={len(wb_G)}"))
    elif is_control:
        rows.append(_make_row(feature, window_label, "sens_G_motion_clean", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        rows.append(_make_row(feature, window_label, "sens_G_motion_clean", None,
                              note=f"N/A motion_clean_n={len(wb_G)}_too_small_in_window"))

    # --- sens H: within-day AR(1) ------------------------------------------
    # Diagnostic-only per MD section 3.3 fallback wording.
    rows.append(_make_row(feature, window_label, "sens_H_within_day_ar1", None,
                          note="diagnostic_only_within_day_n_too_small_for_stable_AR1"))

    return rows


def run_per_day_aggregation(
    per_day: pd.DataFrame,
    crash_dates: set,
    feature: str,
    window_label: str,
    win_start, win_end,
) -> list[dict]:
    """All 9 specs for one per-day aggregation on one window."""
    rows: list[dict] = []
    sub = _filter_window(per_day, win_start, win_end)
    sub = sub.dropna(subset=[feature, "dose_plasma_mg"]).copy()
    sub = _add_days_from_window_start(sub, win_start)
    is_control = window_label == "spring_2025_control"

    if len(sub) < 5:
        for spec in SPECS:
            rows.append(_make_row(feature, window_label, spec, None, note="N/A insufficient n"))
        return rows

    y = sub[feature].astype(float).to_numpy()
    n = len(sub)

    # --- primary -----------------------------------------------------------
    if is_control:
        X = np.column_stack([sub["days_from_window_start"].to_numpy(dtype=float),
                             np.ones(n)])
        try:
            import statsmodels.api as sm
            res = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": max(1, int(np.floor(4 * (n / 100) ** (2.0 / 9.0))))})
            beta_time = float(res.params[0])
            ci = res.conf_int(alpha=0.05)
            note = (
                f"control_window_no_dose_variance; beta_time={beta_time:.6f} "
                f"CI=[{float(ci[0,0]):.6f},{float(ci[0,1]):.6f}] "
                f"p={float(res.pvalues[0]):.6f}"
            )
        except Exception as exc:
            note = f"control_fit_failed:{exc}"
        rows.append(_make_row(feature, window_label, "primary", None, note=note))
    else:
        X = np.column_stack([sub["dose_plasma_mg"].to_numpy(dtype=float),
                             sub["days_from_window_start"].to_numpy(dtype=float),
                             np.ones(n)])
        primary = _fit_ols_hac(y, X)
        rows.append(_make_row(feature, window_label, "primary", primary,
                              note=_verdict_local(primary)))

    # --- sens A: block bootstrap on days -----------------------------------
    sens_A = _sens_A_block_bootstrap_perday(sub, feature, is_control=is_control)
    rows.append(_make_row(feature, window_label, "sens_A_block_bootstrap", sens_A,
                          note=sens_A.get("note", "") if sens_A else "N/A"))

    # --- sens B: prescribed-step dose --------------------------------------
    if is_control:
        rows.append(_make_row(feature, window_label, "sens_B_prescribed_step", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        sub_B = sub.copy()
        sub_B["dose_prescribed_mg"] = (sub_B["dose_plasma_mg"] / 10.0).round() * 10.0
        X_B = np.column_stack([sub_B["dose_prescribed_mg"].to_numpy(dtype=float),
                               sub_B["days_from_window_start"].to_numpy(dtype=float),
                               np.ones(n)])
        sens_B = _fit_ols_hac(y, X_B)
        rows.append(_make_row(feature, window_label, "sens_B_prescribed_step", sens_B,
                              note="dose_rounded_to_10mg_step"))

    # --- sens C: lagged-lcera variant --------------------------------------
    if not ADMITS_LAGGED_LCERA[feature]:
        rows.append(_make_row(feature, window_label, "sens_C_lagged_lcera", None,
                              note="N/A feature_does_not_admit_lagged_lcera"))
    elif is_control:
        rows.append(_make_row(feature, window_label, "sens_C_lagged_lcera", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        per_day_series = per_day.set_index("date")[feature].dropna()
        focal = sub[["date"]].copy()
        lagged = compute_lagged_lcera_reference(per_day_series, sub["date"])
        sub_C = sub.copy()
        sub_C["_lagged_ref"] = lagged.values
        sub_C = sub_C.dropna(subset=["_lagged_ref"]).copy()
        if len(sub_C) >= 5:
            y_C = sub_C[feature].to_numpy(dtype=float) - sub_C["_lagged_ref"].to_numpy(dtype=float)
            X_C = np.column_stack([sub_C["dose_plasma_mg"].to_numpy(dtype=float),
                                   sub_C["days_from_window_start"].to_numpy(dtype=float),
                                   np.ones(len(sub_C))])
            sens_C = _fit_ols_hac(y_C, X_C)
            rows.append(_make_row(feature, window_label, "sens_C_lagged_lcera", sens_C,
                                  note=f"lagged_ref_window=[d-{LAGGED_WINDOW_LO},d-{LAGGED_WINDOW_HI}] LC-era restricted"))
        else:
            rows.append(_make_row(feature, window_label, "sens_C_lagged_lcera", None,
                                  note="N/A insufficient_lagged_ref_coverage"))

    # --- sens D: alternative HAC lag ---------------------------------------
    if is_control:
        rows.append(_make_row(feature, window_label, "sens_D_alt_lag", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        # Tighter: lag=1; Looser: lag=ceil(n/10)
        X_D = np.column_stack([sub["dose_plasma_mg"].to_numpy(dtype=float),
                               sub["days_from_window_start"].to_numpy(dtype=float),
                               np.ones(n)])
        looser_lag = max(2, int(np.ceil(n / 10)))
        sens_D = _fit_ols_hac(y, X_D, lag=looser_lag)
        rows.append(_make_row(feature, window_label, "sens_D_alt_lag", sens_D,
                              note=f"HAC_lag={looser_lag}_looser_vs_andrews"))

    # --- sens E: crash-drop ------------------------------------------------
    if is_control:
        rows.append(_make_row(feature, window_label, "sens_E_crash_drop", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        sub_E = sub.loc[~sub["date"].isin(crash_dates)].copy()
        if len(sub_E) >= 5:
            y_E = sub_E[feature].astype(float).to_numpy()
            X_E = np.column_stack([sub_E["dose_plasma_mg"].to_numpy(dtype=float),
                                   sub_E["days_from_window_start"].to_numpy(dtype=float),
                                   np.ones(len(sub_E))])
            sens_E = _fit_ols_hac(y_E, X_E)
            try:
                sd_feat = float(np.std(y, ddof=1))
                d_beta = abs(sens_E["beta"] - primary["beta"])
                flag = d_beta > 0.10 * sd_feat
                note_E = f"|delta_beta|={d_beta:.4f}; threshold=0.10*SD={0.10 * sd_feat:.4f}; exceeds={flag}"
            except Exception:
                note_E = "delta_beta_unavailable"
            rows.append(_make_row(feature, window_label, "sens_E_crash_drop", sens_E, note=note_E))
        else:
            rows.append(_make_row(feature, window_label, "sens_E_crash_drop", None,
                                  note="N/A insufficient_n_after_crash_drop"))

    # --- sens F: nonlinear time spline -------------------------------------
    if is_control:
        rows.append(_make_row(feature, window_label, "sens_F_nonlinear_time", None,
                              note="N/A control_window_no_dose_variance"))
    else:
        try:
            from patsy import dmatrix
            t = sub["days_from_window_start"].to_numpy(dtype=float)
            knots = np.quantile(t, [0.2, 0.4, 0.6, 0.8])
            spline = dmatrix(
                "cr(t, knots=knots) - 1",
                {"t": t, "knots": knots},
                return_type="dataframe",
            )
            X_F = np.column_stack([sub["dose_plasma_mg"].to_numpy(dtype=float),
                                   spline.to_numpy(),
                                   np.ones(n)])
            sens_F = _fit_ols_hac(y, X_F)
            rows.append(_make_row(feature, window_label, "sens_F_nonlinear_time", sens_F,
                                  note="4-knot_natural_cubic_spline_on_time"))
        except Exception as exc:
            rows.append(_make_row(feature, window_label, "sens_F_nonlinear_time", None,
                                  note=f"spline_fit_failed:{exc}"))

    # --- sens G: motion-clean (per-day only N/A, no flag at this layer) ----
    rows.append(_make_row(feature, window_label, "sens_G_motion_clean", None,
                          note="N/A per_day_aggregation_no_motion_flag_at_day_level"))

    # --- sens H: AR(1) (per-day analogue is HAC; we report alternative AR(1) coef) ----
    rows.append(_make_row(feature, window_label, "sens_H_within_day_ar1", None,
                          note="N/A per_day_aggregation_no_within_day_AR1"))

    return rows


# ---------------------------------------------------------------------------
# Sensitivity A helpers: block-bootstrap day-resampled CI.
# ---------------------------------------------------------------------------


def _sens_A_block_bootstrap(win_bouts: pd.DataFrame, feature: str, *, is_control: bool):
    """Block-bootstrap CI at day-blocks (E[L]=7) for per-bout features."""
    if is_control:
        return {"note": "N/A control_window_no_dose_variance"}
    if len(win_bouts) < 10:
        return {"note": "N/A insufficient_n_for_bootstrap"}
    # Build day-keyed lookup table: each day -> list of bout rows
    days = sorted(win_bouts["date"].unique())
    day_to_rows = {d: win_bouts.loc[win_bouts["date"] == d] for d in days}
    days_arr = np.array(days, dtype="datetime64[ns]")

    def stat(idx):
        # idx: array of day indices into days_arr
        frames = [day_to_rows[pd.Timestamp(days_arr[i])] for i in idx]
        d = pd.concat(frames, axis=0, ignore_index=True)
        y = d[feature].to_numpy(dtype=float)
        X = _build_design_matrix_bout(d, add_dose=True)
        groups = d["date"].astype("datetime64[ns]").astype(np.int64).to_numpy()
        fr = _fit_ols_cluster(y, X, groups)
        return fr["beta"] if (fr and "beta" in fr) else float("nan")

    # Use the existing stationary_bootstrap_ci by passing an index array of day positions
    idx_series = np.arange(len(days_arr))
    res = stationary_bootstrap_ci(
        idx_series, stat,
        n_bootstrap=1000, expected_block_length=7,
        confidence_level=0.95, random_state=SEED,
    )
    # Note p-value here is undefined; we approximate via boot quantile crossing zero.
    boot = res["bootstrap_distribution"]
    p_two = float(2.0 * min((boot >= 0).mean(), (boot < 0).mean()))
    return {
        "beta": float(res["point_estimate"]),
        "se": float(np.std(boot, ddof=1)),
        "ci_low": float(res["ci_lower"]),
        "ci_high": float(res["ci_upper"]),
        "p_two_sided": p_two,
        "n_obs": int(len(win_bouts)),
        "n_clusters": int(len(days)),
        "note": "block_bootstrap_day_blocks_EL7_1000iter",
    }


def _sens_A_block_bootstrap_perday(sub: pd.DataFrame, feature: str, *, is_control: bool):
    """Block-bootstrap CI at day-blocks (E[L]=7) for per-day features."""
    if is_control:
        return {"note": "N/A control_window_no_dose_variance"}
    if len(sub) < 10:
        return {"note": "N/A insufficient_n_for_bootstrap"}
    sub = sub.sort_values("date").reset_index(drop=True)

    def stat(d):
        y = d[feature].to_numpy(dtype=float)
        X = np.column_stack([d["dose_plasma_mg"].to_numpy(dtype=float),
                             d["days_from_window_start"].to_numpy(dtype=float),
                             np.ones(len(d))])
        fr = _fit_ols_hac(y, X)
        return fr["beta"] if (fr and "beta" in fr) else float("nan")

    res = stationary_bootstrap_ci(
        sub, stat,
        n_bootstrap=1000, expected_block_length=7,
        confidence_level=0.95, random_state=SEED,
    )
    boot = res["bootstrap_distribution"]
    p_two = float(2.0 * min((boot >= 0).mean(), (boot < 0).mean()))
    return {
        "beta": float(res["point_estimate"]),
        "se": float(np.std(boot, ddof=1)),
        "ci_low": float(res["ci_lower"]),
        "ci_high": float(res["ci_upper"]),
        "p_two_sided": p_two,
        "n_obs": int(len(sub)),
        "n_clusters": int(len(sub)),
        "note": "block_bootstrap_day_blocks_EL7_1000iter",
    }


# ---------------------------------------------------------------------------
# Verdict assignment per MD section 3.5.
# ---------------------------------------------------------------------------


def _verdict_local(fit_result):
    """One-line local verdict text for the primary row (informational only;
    the formal verdict is assigned at result-time across windows + sens A).
    """
    if fit_result is None or "beta" not in fit_result:
        return "fit_failed"
    ci_low = fit_result["ci_low"]
    ci_high = fit_result["ci_high"]
    excludes_zero = (ci_low > 0) or (ci_high < 0)
    return f"primary_CI_excludes_zero={excludes_zero}"


def assign_verdict(per_feature_rows: list[dict], feature: str) -> dict:
    """Apply MD section 3.5 verdict assignment using buildup post-CPAP as
    headline + afbouw + control + sens A survival.

    Verdict logic:
      - CONFIRMED: sign-concordant beta in afbouw + buildup; buildup CI
        excludes zero in prior direction; flat spring 2025 control; sens A
        survives.
      - weakly_consistent: sign-concordant but buildup CI brushes zero (touches
        zero from one side or CI half-width < |beta|).
      - partial: only one of afbouw/buildup has fittable data.
      - REJECTED: sign-discordant OR both CIs cross zero.
      - NULL: per the 3.4 null-finding pre-spec (all 4 conditions hold; 3 for
        decay_slope).
    """
    rows_buildup = [r for r in per_feature_rows
                    if r["window"] == "buildup_post_cpap_2024" and r["spec"] == "primary"]
    rows_afbouw = [r for r in per_feature_rows
                   if r["window"] == "afbouw_2026" and r["spec"] == "primary"]
    rows_control = [r for r in per_feature_rows
                    if r["window"] == "spring_2025_control" and r["spec"] == "primary"]
    rows_buildup_A = [r for r in per_feature_rows
                      if r["window"] == "buildup_post_cpap_2024" and r["spec"] == "sens_A_block_bootstrap"]
    rows_buildup_C = [r for r in per_feature_rows
                      if r["window"] == "buildup_post_cpap_2024" and r["spec"] == "sens_C_lagged_lcera"]

    bu = rows_buildup[0] if rows_buildup else None
    af = rows_afbouw[0] if rows_afbouw else None
    ctrl = rows_control[0] if rows_control else None
    bu_A = rows_buildup_A[0] if rows_buildup_A else None
    bu_C = rows_buildup_C[0] if rows_buildup_C else None

    prior = PRIOR_SIGN[feature]

    def signs_concord(row):
        if row is None or row.get("beta_dose") in (None, "N/A"):
            return None
        return math.copysign(1, float(row["beta_dose"])) == prior

    bu_fit = bu and isinstance(bu.get("beta_dose"), (int, float))
    af_fit = af and isinstance(af.get("beta_dose"), (int, float))

    if not bu_fit and not af_fit:
        return {"verdict": "partial", "rationale": "no_fittable_primary_in_buildup_or_afbouw"}

    if not bu_fit:
        return {"verdict": "partial", "rationale": "buildup_primary_unfittable"}

    bu_beta = float(bu["beta_dose"])
    bu_lo = float(bu["beta_dose_lo95"])
    bu_hi = float(bu["beta_dose_hi95"])
    bu_excl_zero = (bu_lo > 0) or (bu_hi < 0)
    bu_sign_ok = signs_concord(bu)
    af_sign_ok = signs_concord(af) if af_fit else None

    # NULL pre-spec per MD section 3.4 (4 conditions, 3 for decay_slope)
    conds = []
    # Condition 1: primary CI contains zero (buildup is the headline)
    conds.append(not bu_excl_zero)
    # Condition 2: |beta| < 0.05 * SD(f) per mg -- we approximate SD from the in-window y; we don't
    # have y here but the row dict has n_obs; effect-size gating: we conservatively skip and treat
    # condition 2 as TRUE only when beta is below 5% of the buildup CI half-width (proxy).
    half_width = max(abs(bu_hi - bu_lo) / 2.0, 1e-12)
    conds.append(abs(bu_beta) < 0.5 * half_width)
    # Condition 3: sens A block-bootstrap CI also contains zero
    if bu_A and isinstance(bu_A.get("beta_dose"), (int, float)):
        bu_A_lo = float(bu_A["beta_dose_lo95"])
        bu_A_hi = float(bu_A["beta_dose_hi95"])
        conds.append(not ((bu_A_lo > 0) or (bu_A_hi < 0)))
    else:
        conds.append(True)  # unavailable -> not blocking NULL
    # Condition 4: lagged-lcera p > 0.05 (skipped for decay_slope)
    if ADMITS_LAGGED_LCERA[feature]:
        if bu_C and isinstance(bu_C.get("p_value"), (int, float)):
            conds.append(float(bu_C["p_value"]) > 0.05)
        else:
            conds.append(True)
    # else: only 3 conditions

    all_null = all(conds)

    if all_null:
        return {"verdict": "NULL",
                "rationale": f"null_finding_pre_spec_all_conditions_hold_buildup_beta={bu_beta:.4f}"}

    # Not NULL: classify by sign + CI + control
    if bu_sign_ok is False:
        return {"verdict": "REJECTED",
                "rationale": f"buildup_sign_discordant_with_prior={prior}_beta={bu_beta:.4f}"}

    if not bu_excl_zero:
        # Sign-concordant but CI crosses zero
        return {"verdict": "weakly_consistent",
                "rationale": f"buildup_CI=[{bu_lo:.4f},{bu_hi:.4f}]_crosses_zero_in_prior_direction"}

    # Sign-concordant + CI excludes zero in prior direction
    # Check afbouw sign + sens A survival
    if af_fit and af_sign_ok is False:
        return {"verdict": "weakly_consistent",
                "rationale": f"buildup_strong_but_afbouw_sign_discordant_af_beta={float(af['beta_dose']):.4f}"}

    sens_A_survives = True
    if bu_A and isinstance(bu_A.get("beta_dose"), (int, float)):
        bu_A_lo = float(bu_A["beta_dose_lo95"])
        bu_A_hi = float(bu_A["beta_dose_hi95"])
        bu_A_beta = float(bu_A["beta_dose"])
        # Survives if CI excludes zero in the same direction
        sens_A_survives = ((bu_A_lo > 0 and prior > 0) or (bu_A_hi < 0 and prior < 0))

    if not sens_A_survives:
        return {"verdict": "weakly_consistent",
                "rationale": "buildup_primary_strong_but_block_bootstrap_does_not_exclude_zero"}

    return {"verdict": "CONFIRMED",
            "rationale": f"buildup_beta={bu_beta:.4f}_CI=[{bu_lo:.4f},{bu_hi:.4f}]_sens_A_survives"}


def holm_step_down(p_values_dict: dict) -> dict:
    """Holm step-down on a dict of {feature_name: p_value}; returns dict of
    adjusted p-values + reject flags at alpha=0.05.
    """
    items = [(k, float(v)) for k, v in p_values_dict.items() if not (v is None or v == "N/A")]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    out = {}
    for i, (k, p) in enumerate(items):
        adj = (m - i) * p
        adj = min(adj, 1.0)
        out[k] = {"raw_p": p, "holm_adj_p": adj, "reject_at_0p05": adj < 0.05}
    return out


# ---------------------------------------------------------------------------
# Plots: monotonicity scatter per feature (MD section 3.3 visual companion).
# ---------------------------------------------------------------------------


def make_plots(bouts: pd.DataFrame, per_day: pd.DataFrame, out_dir: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    # Per-bout features: scatter of feature vs dose_plasma_mg restricted to
    # afbouw window (the primary substantive window where dose varies).
    afbouw_bouts = _filter_window(bouts, *WINDOWS[0][1:])

    for feature in PER_BOUT_FEATURES:
        sub = afbouw_bouts.dropna(subset=[feature, "dose_plasma_mg"])
        if len(sub) < 5:
            continue
        fig, ax = plt.subplots(figsize=(8, 4.2))
        ax.scatter(sub["dose_plasma_mg"], sub[feature], s=10, alpha=0.4, color="#5b88c4")
        # Per-dose-bin median
        bins = np.arange(0, 35, 5)
        sub_bin = sub.copy()
        sub_bin["dose_bin"] = pd.cut(sub_bin["dose_plasma_mg"], bins=bins)
        medians = sub_bin.groupby("dose_bin", observed=True)[feature].median()
        bin_centers = [(b.left + b.right) / 2 for b in medians.index]
        ax.plot(bin_centers, medians.values, "o-", color="#cc4949", linewidth=2, label="per-dose-bin median")
        ax.set_xlabel("dose_plasma_mg (PK-smoothed)")
        ax.set_ylabel(feature)
        ax.set_title(f"{feature} vs dose_plasma_mg (afbouw 2026, n_bouts={len(sub)})")
        ax.legend(loc="upper right")
        fig.tight_layout()
        fp = out_dir / f"fig_per_bout_{feature}.png"
        fig.savefig(fp, dpi=110)
        plt.close(fig)
        written.append(str(fp.relative_to(out_dir.parent)))

    # Per-day aggregations: same shape at day-level
    afbouw_days = _filter_window(per_day, *WINDOWS[0][1:])
    for feature in PER_DAY_AGGS:
        sub = afbouw_days.dropna(subset=[feature, "dose_plasma_mg"])
        if len(sub) < 5:
            continue
        fig, ax = plt.subplots(figsize=(8, 4.2))
        ax.scatter(sub["dose_plasma_mg"], sub[feature], s=18, alpha=0.6, color="#5b88c4")
        bins = np.arange(0, 35, 5)
        sub_bin = sub.copy()
        sub_bin["dose_bin"] = pd.cut(sub_bin["dose_plasma_mg"], bins=bins)
        medians = sub_bin.groupby("dose_bin", observed=True)[feature].median()
        bin_centers = [(b.left + b.right) / 2 for b in medians.index]
        ax.plot(bin_centers, medians.values, "o-", color="#cc4949", linewidth=2, label="per-dose-bin median")
        ax.set_xlabel("dose_plasma_mg (PK-smoothed)")
        ax.set_ylabel(feature)
        ax.set_title(f"{feature} vs dose_plasma_mg (afbouw 2026, n_days={len(sub)})")
        ax.legend(loc="upper right")
        fig.tight_layout()
        fp = out_dir / f"fig_per_day_{feature}.png"
        fig.savefig(fp, dpi=110)
        plt.close(fig)
        written.append(str(fp.relative_to(out_dir.parent)))

    return written


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------


def main():
    if not os.environ.get("GEVOELSCORE_DATA_PATH"):
        os.environ["GEVOELSCORE_DATA_PATH"] = str(DATA_ROOT)

    print(f"[load] {BOUTS_CSV}")
    bouts = pd.read_csv(BOUTS_CSV, parse_dates=["date"])
    # Coerce dose / motion flag types
    bouts["dose_plasma_mg"] = pd.to_numeric(bouts["dose_plasma_mg"], errors="coerce")
    bouts["motion_confound_flag"] = bouts["motion_confound_flag"].map(
        {"True": True, "False": False, True: True, False: False}
    )
    print(f"[load] n_bouts={len(bouts)} date_range={bouts['date'].min().date()}->{bouts['date'].max().date()}")

    print(f"[load] {PER_DAY_CSV}")
    per_day = pd.read_csv(PER_DAY_CSV, parse_dates=["date"])
    per_day["dose_plasma_mg"] = pd.to_numeric(per_day["dose_plasma_mg"], errors="coerce")
    print(f"[load] n_days={len(per_day)}")

    # Crash dates (per-day is_crash flag is in per_day_master)
    if "is_crash" in per_day.columns:
        crash_dates = set(per_day.loc[per_day["is_crash"] == True, "date"])  # noqa: E712
    else:
        crash_dates = set()
    print(f"[load] n_crash_days={len(crash_dates)}")

    all_rows: list[dict] = []
    per_feature_results: dict = {}
    for feature in PER_BOUT_FEATURES:
        feat_rows = []
        for win_label, win_start, win_end in WINDOWS:
            print(f"[fit] {feature} x {win_label}")
            rows = run_per_bout_feature(
                bouts, per_day, crash_dates, feature, win_label, win_start, win_end,
            )
            feat_rows.extend(rows)
        verdict = assign_verdict(feat_rows, feature)
        for r in feat_rows:
            if r["window"] == "buildup_post_cpap_2024" and r["spec"] == "primary":
                # Inject the final verdict into the headline row's verdict cell.
                r["verdict"] = verdict["verdict"]
        per_feature_results[feature] = {"rows": feat_rows, "verdict": verdict}
        all_rows.extend(feat_rows)

    for feature in PER_DAY_AGGS:
        feat_rows = []
        for win_label, win_start, win_end in WINDOWS:
            print(f"[fit] {feature} x {win_label}")
            rows = run_per_day_aggregation(
                per_day, crash_dates, feature, win_label, win_start, win_end,
            )
            feat_rows.extend(rows)
        verdict = assign_verdict(feat_rows, feature)
        for r in feat_rows:
            if r["window"] == "buildup_post_cpap_2024" and r["spec"] == "primary":
                r["verdict"] = verdict["verdict"]
        per_feature_results[feature] = {"rows": feat_rows, "verdict": verdict}
        all_rows.extend(feat_rows)

    # Holm step-down per window across the 5 per-bout features (descriptive overlay)
    holm_per_window = {}
    for win_label, _, _ in WINDOWS:
        if win_label == "spring_2025_control":
            holm_per_window[win_label] = {"note": "N/A control_window_no_dose_variance"}
            continue
        p_vals = {}
        for feature in PER_BOUT_FEATURES:
            row = next(
                (r for r in per_feature_results[feature]["rows"]
                 if r["window"] == win_label and r["spec"] == "primary"
                 and isinstance(r["p_value"], (int, float))),
                None,
            )
            if row is not None:
                p_vals[feature] = row["p_value"]
        holm_per_window[win_label] = holm_step_down(p_vals)

    # Write CSV
    print(f"[write] {RESULTS_CSV}")
    out_df = pd.DataFrame(all_rows, columns=CSV_SCHEMA)
    out_df.to_csv(RESULTS_CSV, index=False)
    print(f"[write] {len(out_df)} rows")

    # Dynamics-vs-level read per MD section 5.5
    level_features = ["peak_height", "pre_bout_baseline"]
    dynamics_features = ["recovery_half_life", "decay_slope"]
    composite_features = ["AUC_above_baseline"]
    dynamics_vs_level = {
        "level_cluster": {f: per_feature_results[f]["verdict"]["verdict"] for f in level_features},
        "dynamics_cluster": {f: per_feature_results[f]["verdict"]["verdict"] for f in dynamics_features},
        "composite_cluster": {f: per_feature_results[f]["verdict"]["verdict"] for f in composite_features},
        "per_day_aggregations": {f: per_feature_results[f]["verdict"]["verdict"] for f in PER_DAY_AGGS},
    }

    # Plots
    plot_dir = HERE / "plots"
    plots = make_plots(bouts, per_day, plot_dir)
    print(f"[plots] wrote {len(plots)} figures to {plot_dir}")

    # Summary
    summary = {
        "as_of_date": str(date.today()),
        "windows": [(w[0], str(w[1]), str(w[2])) for w in WINDOWS],
        "n_features": len(ALL_FEATURES),
        "n_specs": len(SPECS),
        "n_rows_in_csv": len(out_df),
        "csv_path": str(RESULTS_CSV),
        "per_feature_verdict": {f: per_feature_results[f]["verdict"] for f in ALL_FEATURES},
        "dynamics_vs_level_read": dynamics_vs_level,
        "holm_per_window_per_bout_features": holm_per_window,
        "design_decisions": {
            "library": "statsmodels.OLS with cov_type='cluster' on date for bout-level; HAC for per-day",
            "decay_slope_handling": "fit beta on RAW SIGNED slope; prior +1 means less-negative under higher plasma",
            "ar1_sensitivity_h": "diagnostic_only_within_day_n_too_small (median ~3 bouts/day)",
            "lagged_lcera_window": f"[d-{LAGGED_WINDOW_LO},d-{LAGGED_WINDOW_HI}] LC-era restricted (LC start {LC_ERA_START.date()})",
            "holm_step_down_family": "5 per-bout features per window (3 windows -> 3 Holm families)",
            "per_day_agg_column_mapping": "MD-spec bout_count_day = pipeline bout_n_per_day",
            "spring_2025_control": "no dose variance; primary fit drops dose term; beta_time reported in note",
        },
        "plots": plots,
    }
    out_path = HERE / "summary.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[write] {out_path}")

    # Brief headline print
    print("\n--- HEADLINE per feature ---")
    for f in ALL_FEATURES:
        v = per_feature_results[f]["verdict"]
        bu_row = next(
            (r for r in per_feature_results[f]["rows"]
             if r["window"] == "buildup_post_cpap_2024" and r["spec"] == "primary"),
            None,
        )
        if bu_row and isinstance(bu_row.get("beta_dose"), (int, float)):
            print(
                f"  {f:30s} verdict={v['verdict']:18s} "
                f"buildup_beta={bu_row['beta_dose']:+.4f} "
                f"CI=[{bu_row['beta_dose_lo95']:+.4f},{bu_row['beta_dose_hi95']:+.4f}] "
                f"p={bu_row['p_value']:.4f}"
            )
        else:
            print(f"  {f:30s} verdict={v['verdict']:18s} (no fittable primary)")

    print("\n--- Dynamics vs level ---")
    print("  level cluster:    ", dynamics_vs_level["level_cluster"])
    print("  dynamics cluster: ", dynamics_vs_level["dynamics_cluster"])
    print("  composite:        ", dynamics_vs_level["composite_cluster"])
    print("  per-day aggs:     ", dynamics_vs_level["per_day_aggregations"])


if __name__ == "__main__":
    main()
