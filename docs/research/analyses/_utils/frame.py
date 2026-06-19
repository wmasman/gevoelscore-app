"""Shared frame / data-prep utilities for HA-numbered hypothesis tests.

Implements the data-prep + sensitivity-wrapper layer of the project's
methodology stack. Resampling + multiplicity utilities live in
``inference.py`` per the two-module organisation locked 2026-06-15.

Tier 1 functions (this module):

1. ``z_score_vs_rolling_baseline`` --- compute z-scores against a
   personal rolling baseline (default robust median + MAD, window=28
   days, no lag). Per CONVENTIONS §3.1: PEM-pacing metrics use
   deviations from personal baseline, not absolute thresholds.
2. ``crash_drop_sensitivity`` --- compute a statistic on the full frame
   AND with ``is_crash == True`` rows dropped; flag if
   ``|delta| > 0.10``. Per CONVENTIONS §3.4 + pre-reg constraint 7.
3. ``filter_to_stratum_4`` / ``stratum_4_mask`` --- filter / mask
   Stratum 4 rows (LC with gevoelscore + crash labels, 2022-09-03 →
   as-of-date). Single source of truth for Stratum 4 per MD 1.
4. ``load_master`` / ``load_crash_labels`` --- canonical loader
   functions that resolve ``$GEVOELSCORE_DATA_PATH`` and apply the
   as-of-date convention from MD 1 §7.

Tier 2 lazy-expansion utilities (peri-event window stacker,
match-pair-finder, standardised effect-size functions, sensitivity-
ladder runner) are NOT pre-created; they land here when the first
HA-test imports them.

Each public function has a companion test in ``test_frame.py``
(synthetic-data correctness check before any HA-test imports it).
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np


__all__ = [
    "z_score_vs_rolling_baseline",
    "crash_drop_sensitivity",
    "stratum_4_mask",
    "filter_to_stratum_4",
    "load_master",
    "load_crash_labels",
    "STRATUM_4_START",
]


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


STRATUM_4_START = "2022-09-03"
"""Left edge of Stratum 4 per MD 1 (gevoelscore corpus start)."""


# -----------------------------------------------------------------------------
# z_score_vs_rolling_baseline (CONVENTIONS §3.1)
# -----------------------------------------------------------------------------


def z_score_vs_rolling_baseline(
    series,
    *,
    window: int = 28,
    lag: int = 0,
    robust: bool = True,
    min_periods: int | None = None,
):
    """Compute z-scores against a rolling personal baseline.

    Per CONVENTIONS §3.1: PEM-pacing metrics work in deviations from
    the participant's own rolling baseline rather than absolute cutoffs.
    Default robust median + MAD is preferred (one-zero-step day is not
    rebased by a single outlier).

    Parameters
    ----------
    series : pandas Series or array-like
        Input time series.
    window : int, keyword-only
        Rolling window length in observations. Default 28 per
        CONVENTIONS §3.1 default.
    lag : int, keyword-only
        Lag (in observations) between the current point and the end of
        the baseline window:

        - ``lag=0`` (default): trailing window ``[t-window+1, t]``
          includes the current point in the baseline; standard for
          plain z-scoring.
        - ``lag=1``: trailing window ``[t-window, t-1]`` excludes the
          current point. Useful when the z-score should compare the
          current point to a baseline that does not include it
          (matters most for non-robust statistics, where a same-day
          outlier inflates the std and mutes the z; with robust
          statistics the choice matters less because a single outlier
          barely shifts the median or MAD).
        - ``lag > 1``: explicit gap (e.g. ``lag=30`` gives
          ``[t-window-29, t-30]``, analogous to the ``_lagged_lcera``
          column construction in ``pipeline/02_label/``).

    robust : bool, keyword-only
        If True, use median + MAD (×1.4826 for normal-equivalence). If
        False, use mean + std. Default True per CONVENTIONS §3.1.
    min_periods : int or None, keyword-only
        Minimum non-NaN observations in window for a valid z-score.
        Default ``max(1, window // 2)``. Observations before this
        threshold (or with all-NaN windows) yield NaN.

    Returns
    -------
    pandas Series or ndarray
        Z-scores in the same type as the input. Observations with too
        few baseline observations, with zero baseline spread, or in
        the lag warm-up period yield NaN.

    Notes
    -----
    Default uses TRAILING window (no look-ahead). For lagged-baseline
    PEM-pacing tests on the LC frame, prefer the pre-computed
    ``*_lagged_lcera`` columns in ``per_day_master.csv`` per CONVENTIONS
    §3.2 — those use a ``[d-90, d-30]`` window with LC-era-only days.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> rng = np.random.default_rng(42)
    >>> # Baseline of 0, then a spike to 5
    >>> series = pd.Series(np.concatenate([rng.standard_normal(100), [5.0]]))
    >>> z = z_score_vs_rolling_baseline(series, window=28, lag=1)
    >>> z.iloc[-1] > 3  # last point is a clear spike
    True
    """
    try:
        import pandas as pd
    except ImportError:  # pragma: no cover
        pd = None

    is_pandas = pd is not None and isinstance(series, pd.Series)

    if is_pandas:
        index = series.index
        arr = series.to_numpy(dtype=float)
    else:
        arr = np.asarray(series, dtype=float)
        index = None

    n = len(arr)
    if window < 2:
        raise ValueError(f"window must be >= 2, got {window}")
    if lag < 0:
        raise ValueError(f"lag must be >= 0, got {lag}")
    if min_periods is None:
        min_periods = max(1, window // 2)
    if min_periods < 1:
        raise ValueError(f"min_periods must be >= 1, got {min_periods}")

    z = np.full(n, np.nan)

    for t in range(n):
        # Window covers [t - window + 1 - lag, t - lag] inclusive
        end = t - lag + 1  # exclusive
        start = end - window  # inclusive
        if end <= 0:
            continue  # warm-up
        start = max(0, start)
        window_vals = arr[start:end]
        window_vals = window_vals[~np.isnan(window_vals)]
        if len(window_vals) < min_periods:
            continue

        if robust:
            centre = float(np.median(window_vals))
            mad = float(np.median(np.abs(window_vals - centre)))
            if mad == 0.0:
                continue  # zero spread; z-score undefined
            spread = mad * 1.4826  # normal-equivalence scaling
        else:
            centre = float(window_vals.mean())
            spread = float(window_vals.std(ddof=1))
            if spread == 0.0:
                continue

        if np.isnan(arr[t]):
            continue
        z[t] = (arr[t] - centre) / spread

    if is_pandas:
        return pd.Series(z, index=index, name=getattr(series, "name", None))
    return z


# -----------------------------------------------------------------------------
# crash_drop_sensitivity (CONVENTIONS §3.4)
# -----------------------------------------------------------------------------


def crash_drop_sensitivity(
    stat_fn,
    df,
    *,
    crash_column: str = "is_crash",
    delta_threshold: float = 0.10,
):
    """Compute a statistic on full frame AND with crash rows dropped.

    Per CONVENTIONS §3.4 + pre-reg constraint 7: every Layer 4+
    correlation / CCF / regression on PEM-pacing variables reports the
    result with ``is_crash == True`` rows dropped alongside the
    full-frame result. ``|delta| > 0.10`` is surfaced as a finding
    (the crash days are doing systematic work; on this corpus the
    exertion × resting_hr Spearman swings from ~+0.0 to ~+0.4 when
    crash days drop).

    Parameters
    ----------
    stat_fn : callable
        Function taking a DataFrame and returning a scalar (e.g. a
        correlation, regression coefficient, or discrimination value).
    df : pandas DataFrame
        Input data; must contain the ``crash_column``.
    crash_column : str, keyword-only
        Column name flagging crash days. Default "is_crash".
    delta_threshold : float, keyword-only
        Threshold above which the absolute delta is surfaced as a
        finding. Default 0.10 per CONVENTIONS §3.4.

    Returns
    -------
    dict
        Keys:

        - ``full_frame_value`` (float): statistic on the full frame.
        - ``crash_dropped_value`` (float): statistic with crash rows
          dropped.
        - ``delta`` (float): full_frame_value − crash_dropped_value.
        - ``abs_delta`` (float): ``|delta|``.
        - ``exceeds_threshold`` (bool): True if ``abs_delta >
          delta_threshold``.
        - ``n_full`` (int): number of rows in the full frame.
        - ``n_crash_dropped`` (int): number of rows after dropping
          crash days.
        - ``n_crash`` (int): number of crash days dropped.

    Raises
    ------
    KeyError
        If ``crash_column`` is not in ``df.columns``.
    ValueError
        If after dropping crash rows, < 2 rows remain (statistic
        cannot be meaningfully computed).

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> rng = np.random.default_rng(42)
    >>> df = pd.DataFrame({
    ...     "x": rng.standard_normal(200),
    ...     "y": rng.standard_normal(200),
    ...     "is_crash": rng.random(200) < 0.1,
    ... })
    >>> result = crash_drop_sensitivity(
    ...     lambda d: float(d["x"].corr(d["y"])), df,
    ... )
    >>> "delta" in result and "exceeds_threshold" in result
    True
    """
    if crash_column not in df.columns:
        raise KeyError(
            f"crash_column {crash_column!r} not in DataFrame columns: "
            f"{list(df.columns)[:10]}..."
        )

    crash_mask = df[crash_column].astype(bool)
    df_dropped = df[~crash_mask]

    n_full = int(len(df))
    n_crash_dropped = int(len(df_dropped))
    n_crash = n_full - n_crash_dropped

    if n_crash_dropped < 2:
        raise ValueError(
            f"After dropping crash rows, only {n_crash_dropped} rows "
            f"remain; statistic cannot be meaningfully computed"
        )

    full_value = float(stat_fn(df))
    dropped_value = float(stat_fn(df_dropped))
    delta = full_value - dropped_value

    return {
        "full_frame_value": full_value,
        "crash_dropped_value": dropped_value,
        "delta": float(delta),
        "abs_delta": float(abs(delta)),
        "exceeds_threshold": bool(abs(delta) > delta_threshold),
        "n_full": n_full,
        "n_crash_dropped": n_crash_dropped,
        "n_crash": n_crash,
    }


# -----------------------------------------------------------------------------
# Stratum 4 filter / mask (MD 1)
# -----------------------------------------------------------------------------


def stratum_4_mask(
    df,
    *,
    date_column: str = "date",
    as_of_date=None,
):
    """Boolean mask for Stratum 4 rows in a DataFrame.

    Stratum 4 = LC with gevoelscore + crash labels, ``2022-09-03 →
    as_of_date``. Per ``../../methodology/lc_era_temporal_segmentation.md``.

    Parameters
    ----------
    df : pandas DataFrame
        Must contain ``date_column``.
    date_column : str, keyword-only
        Name of the date column. Default "date".
    as_of_date : str / pandas Timestamp / None, keyword-only
        Right edge of Stratum 4 (inclusive). If None, no upper bound
        is applied — caller takes everything from STRATUM_4_START to
        the most recent row. Pre-regs MUST state their as-of-date per
        MD 1 §7 (the as-of-date convention).

    Returns
    -------
    pandas Series of bool
        Mask the same length as ``df``; True for rows in Stratum 4.

    Raises
    ------
    KeyError
        If ``date_column`` is not in ``df.columns``.
    """
    import pandas as pd

    if date_column not in df.columns:
        raise KeyError(
            f"date_column {date_column!r} not in DataFrame columns: "
            f"{list(df.columns)[:10]}..."
        )

    dates = pd.to_datetime(df[date_column])
    start = pd.Timestamp(STRATUM_4_START)
    mask = dates >= start
    if as_of_date is not None:
        end = pd.Timestamp(as_of_date)
        mask = mask & (dates <= end)
    return mask


def filter_to_stratum_4(
    df,
    *,
    date_column: str = "date",
    as_of_date=None,
):
    """Filter DataFrame to Stratum 4 rows.

    Thin wrapper around :func:`stratum_4_mask`. Returns a new DataFrame
    with only rows in Stratum 4; does not modify the original.
    """
    return df[stratum_4_mask(df, date_column=date_column, as_of_date=as_of_date)].copy()


# -----------------------------------------------------------------------------
# Loaders (MD 1 §7 as-of-date convention)
# -----------------------------------------------------------------------------


def _resolve_data_root() -> Path:
    """Resolve ``$GEVOELSCORE_DATA_PATH``; raise a clear error if not set."""
    raw = os.environ.get("GEVOELSCORE_DATA_PATH", "")
    if not raw:
        raise RuntimeError(
            "GEVOELSCORE_DATA_PATH is not set. Add it to your .env or "
            "shell environment per CONVENTIONS §5; default value is "
            "C:/Users/Gebruiker/Documents/gevoelscore-data."
        )
    root = Path(raw)
    if not root.exists():
        raise RuntimeError(
            f"GEVOELSCORE_DATA_PATH={raw!r} does not exist."
        )
    return root


def load_master(
    *,
    as_of_date=None,
    stratum_4_only: bool = False,
):
    """Load ``per_day_master.csv`` with the as-of-date convention applied.

    Per MD 1 §7: every Wiggers pre-reg states its data-cut date. This
    loader enforces that convention by accepting an ``as_of_date``
    parameter; new data accruing after the pre-reg locks does not
    propagate into re-runs unless explicitly queued.

    Parameters
    ----------
    as_of_date : str / pandas Timestamp / None, keyword-only
        Right edge of the loaded data (inclusive). If None, loads
        everything (NOT recommended for pre-reg runs — pre-regs must
        state their as-of-date).
    stratum_4_only : bool, keyword-only
        If True, apply :func:`filter_to_stratum_4` after loading.
        Default False (loads all strata; caller filters as needed).

    Returns
    -------
    pandas DataFrame
        ``per_day_master.csv`` with the date column parsed as datetime
        and optionally filtered by as-of-date / Stratum 4.

    Raises
    ------
    RuntimeError
        If ``GEVOELSCORE_DATA_PATH`` is not set or doesn't exist, or if
        the master CSV is not found at the expected path.
    """
    import pandas as pd

    root = _resolve_data_root()
    path = root / "unified" / "per_day_master.csv"
    if not path.exists():
        raise RuntimeError(
            f"per_day_master.csv not found at {path}. Build with "
            f"pipeline/03_consolidate/build_unified_dataset.py first."
        )
    df = pd.read_csv(path, parse_dates=["date"])
    if as_of_date is not None:
        end = pd.Timestamp(as_of_date)
        df = df[df["date"] <= end].copy()
    if stratum_4_only:
        df = filter_to_stratum_4(df, as_of_date=as_of_date)
    return df


def load_crash_labels(*, as_of_date=None):
    """Load ``labels_crash_v2.csv`` with the as-of-date convention applied.

    Parameters
    ----------
    as_of_date : str / pandas Timestamp / None, keyword-only
        Right edge of the loaded data (inclusive). If None, loads all
        labels.

    Returns
    -------
    pandas DataFrame
        Crash-v2 labels with the date column parsed as datetime and
        optionally filtered by as-of-date.

    Raises
    ------
    RuntimeError
        If ``GEVOELSCORE_DATA_PATH`` is not set, or the labels CSV is
        not found at the expected path.
    """
    import pandas as pd

    root = _resolve_data_root()
    path = root / "processed" / "crash_labels" / "labels_crash_v2.csv"
    if not path.exists():
        raise RuntimeError(
            f"labels_crash_v2.csv not found at {path}."
        )
    df = pd.read_csv(path, parse_dates=["date"])
    if as_of_date is not None:
        end = pd.Timestamp(as_of_date)
        df = df[df["date"] <= end].copy()
    return df
