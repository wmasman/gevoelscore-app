"""
Trajectory linear-detrend helper for the Q24 post-heavy trajectory audit.

Adapts the `linear_detrend_on_pre` helper from
`docs/research/methodology/intervention_effects_descriptive.md` §6
(pre-vs-post median-diff pattern) to the per-day trajectory contrast
required by Q24 methodology MD §7.11.

Method (per Q24 MD §7.11):
- For each anchor day D (heavy episode-end or matched-ordinary D_ord) and
  each outcome operand `o`, fit `y = a + b*t` (t = days-from-D) on the
  outcome column `o` over the 30-day pre-window `[D-30, D-1]`.
- Extrapolate the fitted trend through the post-window `[D+1, D+w]`.
- Subtract the extrapolated baseline from the observed values at each d+k
  to produce a detrended trajectory value per k.

Insufficient-pre-window handling (Q24 MD §7.11):
- If <15 valid data points exist in the 30d pre-window (50% coverage over
  30 days), the episode's detrend is flagged NaN across all k in the
  post-window and the episode drops from the detrended arm for that
  outcome only. Raw-arm inclusion is unaffected.

Producer-mode helper per CONVENTIONS §1.1. No inference; pure numerical
transform. Zero-vs-NaN discipline: never `.fillna(0)`; missing pre-window
data yields NaN detrended output.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# Q24 MD §7.11: 30d pre-window inherited from parent MD reference-window
# pattern per bout_level_recovery_dynamics.md §3.2.2
PRE_WINDOW_DAYS = 30

# Q24 MD §7.11: minimum valid pre-window points to fit a trend
# (50% coverage over 30 days = 15 points)
MIN_PRE_POINTS = 15


def linear_detrend_on_pre_trajectory(
    series: pd.Series,
    anchor_date: pd.Timestamp,
    window_days: int,
    pre_window_days: int = PRE_WINDOW_DAYS,
    min_pre_points: int = MIN_PRE_POINTS,
) -> np.ndarray:
    """
    Compute detrended values at d+1, ..., d+window_days for a single anchor.

    Parameters
    ----------
    series : pd.Series
        Outcome column indexed by date (pd.Timestamp). May contain NaNs.
    anchor_date : pd.Timestamp
        The anchor day D (heavy episode-end or matched-ordinary comparator).
    window_days : int
        Post-window length w. Detrended values are returned for k=1..w.
    pre_window_days : int
        Pre-window length for fitting the linear trend (default 30 per
        Q24 MD §7.11).
    min_pre_points : int
        Minimum valid data points required in the pre-window to accept
        the fit (default 15 = 50% of 30d per Q24 MD §7.11).

    Returns
    -------
    np.ndarray of shape (window_days,)
        Detrended values at k=1..window_days. All-NaN if the pre-window
        has fewer than `min_pre_points` valid observations, or if the
        observed value at a given k is NaN.
    """
    # Pre-window slice: [D-pre_window_days, D-1]
    pre_start = anchor_date - pd.Timedelta(days=pre_window_days)
    pre_end = anchor_date - pd.Timedelta(days=1)
    pre = series.loc[pre_start:pre_end].dropna()

    if len(pre) < min_pre_points:
        # Insufficient pre-window; return all-NaN per Q24 MD §7.11
        return np.full(window_days, np.nan)

    # Fit linear trend on pre-window (x = days-from-D, negative for pre days)
    pre_x = np.array([(idx - anchor_date).days for idx in pre.index], dtype=float)
    slope, intercept = np.polyfit(pre_x, pre.values, deg=1)

    # Post-window observed values at k=1..w
    post_start = anchor_date + pd.Timedelta(days=1)
    post_end = anchor_date + pd.Timedelta(days=window_days)
    post_dates = pd.date_range(post_start, post_end, freq="D")

    detrended = np.full(window_days, np.nan)
    for i, d_k in enumerate(post_dates):
        if d_k in series.index:
            obs = series.loc[d_k]
            if pd.notna(obs):
                k = (d_k - anchor_date).days  # 1..w
                trend_at_k = slope * k + intercept
                detrended[i] = obs - trend_at_k
    return detrended


def raw_trajectory(
    series: pd.Series,
    anchor_date: pd.Timestamp,
    window_days: int,
) -> np.ndarray:
    """
    Extract raw values at d+1, ..., d+window_days.

    Missing dates or NaN observations remain NaN per zero-vs-NaN
    discipline (CONVENTIONS §5). Never `.fillna(0)`.
    """
    post_start = anchor_date + pd.Timedelta(days=1)
    post_end = anchor_date + pd.Timedelta(days=window_days)
    post_dates = pd.date_range(post_start, post_end, freq="D")

    raw = np.full(window_days, np.nan)
    for i, d_k in enumerate(post_dates):
        if d_k in series.index:
            obs = series.loc[d_k]
            if pd.notna(obs):
                raw[i] = obs
    return raw
