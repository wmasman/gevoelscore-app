"""Synthetic-data correctness tests for ``analyses/_utils/frame.py``.

Each Tier 1 utility in ``frame.py`` is tested against synthetic data
with known properties. The loader functions (``load_master``,
``load_crash_labels``) are tested only for their error-handling
contract — they read external CSVs that are not part of the repo per
the privacy boundary, so we don't smoke-test their happy path here.

Run with:

    python -m pytest docs/research/analyses/_utils/test_frame.py -v
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pytest

# Make ``frame.py`` importable regardless of how pytest is invoked.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from frame import (  # noqa: E402
    STRATUM_4_START,
    _resolve_data_root,
    crash_drop_sensitivity,
    filter_to_stratum_4,
    load_crash_labels,
    load_master,
    stratum_4_mask,
    z_score_vs_rolling_baseline,
)


# =============================================================================
# z_score_vs_rolling_baseline
# =============================================================================


class TestZScoreVsRollingBaseline:
    """Correctness checks for the rolling-baseline z-score."""

    def test_constant_series_returns_nans(self):
        """A flat series has zero spread; z-score is undefined (NaN)."""
        pd = pytest.importorskip("pandas")
        series = pd.Series(np.full(100, 5.0))
        z = z_score_vs_rolling_baseline(series, window=28)
        # All values are NaN because MAD = 0 (and std = 0 if robust=False)
        assert z.isna().all()

    def test_warm_up_period_is_nan(self):
        """Observations before the lag/window has enough data are NaN."""
        pd = pytest.importorskip("pandas")
        rng = np.random.default_rng(42)
        series = pd.Series(rng.standard_normal(50))
        z = z_score_vs_rolling_baseline(series, window=28, lag=1, min_periods=14)
        # First few observations have insufficient baseline data
        assert z.iloc[0] != z.iloc[0]  # NaN check
        # Later observations have valid z-scores
        assert not np.isnan(z.iloc[-1])

    def test_spike_detected_with_lag_one(self):
        """A clear spike (5 SD above baseline) gets a high z-score with lag=1."""
        pd = pytest.importorskip("pandas")
        rng = np.random.default_rng(42)
        # 100 days of unit-variance baseline; final day spikes to +5
        baseline = rng.standard_normal(100)
        series = pd.Series(np.concatenate([baseline, [5.0]]))
        z = z_score_vs_rolling_baseline(series, window=28, lag=1)
        # The spike day should have a clearly elevated z-score
        assert z.iloc[-1] > 3.0, f"Expected spike z > 3, got {z.iloc[-1]:.3f}"

    def test_non_robust_lag_one_higher_than_lag_zero(self):
        """For NON-robust (mean+std), lag=1 gives higher z than lag=0.

        With non-robust stats, including the spike in its own baseline
        inflates the std, muting the z-score. Lag=1 excludes the spike
        and gives a clean signal. (With robust median+MAD, a single
        outlier barely shifts the median or MAD, so the lag choice
        matters much less — that case is covered by separate tests.)
        """
        pd = pytest.importorskip("pandas")
        rng = np.random.default_rng(42)
        baseline = rng.standard_normal(100)
        series = pd.Series(np.concatenate([baseline, [5.0]]))
        z_lag0 = z_score_vs_rolling_baseline(series, window=28, lag=0, robust=False)
        z_lag1 = z_score_vs_rolling_baseline(series, window=28, lag=1, robust=False)
        assert z_lag1.iloc[-1] > z_lag0.iloc[-1], (
            f"Expected lag=1 z ({z_lag1.iloc[-1]:.3f}) > lag=0 z "
            f"({z_lag0.iloc[-1]:.3f}) under non-robust scoring"
        )

    def test_robust_vs_non_robust(self):
        """Robust (median+MAD) less affected by one outlier in baseline than non-robust (mean+std)."""
        pd = pytest.importorskip("pandas")
        rng = np.random.default_rng(42)
        # 28 normal days + 1 huge outlier in the baseline, then spike on next day
        baseline = rng.standard_normal(28)
        outlier_baseline = np.concatenate([baseline, [100.0]])
        # Spike of +5 after the outlier
        series = pd.Series(np.concatenate([outlier_baseline, [5.0]]))
        z_robust = z_score_vs_rolling_baseline(series, window=29, lag=1, robust=True)
        z_naive = z_score_vs_rolling_baseline(series, window=29, lag=1, robust=False)
        # The 100-outlier inflates non-robust std massively; robust median+MAD less affected
        # So the +5 spike's z-score should be HIGHER under robust scoring
        assert z_robust.iloc[-1] > z_naive.iloc[-1]

    def test_nan_input_propagates(self):
        """NaN values in the input yield NaN z-scores."""
        pd = pytest.importorskip("pandas")
        rng = np.random.default_rng(42)
        arr = rng.standard_normal(100)
        arr[50] = np.nan
        series = pd.Series(arr)
        z = z_score_vs_rolling_baseline(series, window=28, lag=0)
        assert np.isnan(z.iloc[50])

    def test_input_validation(self):
        with pytest.raises(ValueError, match="window"):
            z_score_vs_rolling_baseline(np.zeros(50), window=1)
        with pytest.raises(ValueError, match="lag"):
            z_score_vs_rolling_baseline(np.zeros(50), lag=-1)
        with pytest.raises(ValueError, match="min_periods"):
            z_score_vs_rolling_baseline(np.zeros(50), min_periods=0)

    def test_array_input_returns_array(self):
        """Passing an ndarray returns an ndarray (not a Series)."""
        rng = np.random.default_rng(42)
        arr = rng.standard_normal(100)
        z = z_score_vs_rolling_baseline(arr, window=28, lag=0)
        assert isinstance(z, np.ndarray)
        assert len(z) == 100


# =============================================================================
# crash_drop_sensitivity
# =============================================================================


class TestCrashDropSensitivity:
    """Correctness checks for the crash-drop sensitivity wrapper."""

    def test_no_effect_when_crash_rows_are_random(self):
        """If crash rows are randomly distributed, delta should be small."""
        pd = pytest.importorskip("pandas")
        rng = np.random.default_rng(42)
        df = pd.DataFrame({
            "x": rng.standard_normal(500),
            "y": rng.standard_normal(500),
            "is_crash": rng.random(500) < 0.1,
        })
        result = crash_drop_sensitivity(
            lambda d: float(d["x"].corr(d["y"])), df
        )
        # Random crash days on uncorrelated data; delta should be small
        assert result["abs_delta"] < 0.20
        assert isinstance(result["exceeds_threshold"], bool)

    def test_systematic_effect_flagged(self):
        """A constructed pattern where crashes dominate the signal gets flagged."""
        pd = pytest.importorskip("pandas")
        rng = np.random.default_rng(42)
        # Construct: on crash days, x and y are perfectly negatively correlated
        # On non-crash days, x and y are independent.
        n = 500
        is_crash = rng.random(n) < 0.2
        x = rng.standard_normal(n)
        y = np.where(is_crash, -x, rng.standard_normal(n))
        df = pd.DataFrame({"x": x, "y": y, "is_crash": is_crash})
        result = crash_drop_sensitivity(
            lambda d: float(d["x"].corr(d["y"])), df,
            delta_threshold=0.10,
        )
        # Full frame should show negative correlation; dropped should be near 0
        assert result["full_frame_value"] < 0.0
        assert abs(result["crash_dropped_value"]) < 0.15
        assert result["abs_delta"] > 0.10
        assert result["exceeds_threshold"]

    def test_n_counts_correct(self):
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame({
            "x": np.arange(100),
            "is_crash": [True if i % 10 == 0 else False for i in range(100)],
        })
        result = crash_drop_sensitivity(
            lambda d: float(d["x"].mean()), df
        )
        assert result["n_full"] == 100
        assert result["n_crash"] == 10
        assert result["n_crash_dropped"] == 90

    def test_missing_crash_column_raises_keyerror(self):
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        with pytest.raises(KeyError, match="crash_column"):
            crash_drop_sensitivity(lambda d: 1.0, df)

    def test_all_crash_raises_value_error(self):
        """If dropping crashes leaves < 2 rows, raise."""
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame({"x": [1, 2, 3], "is_crash": [True, True, True]})
        with pytest.raises(ValueError, match="only 0 rows remain"):
            crash_drop_sensitivity(lambda d: 1.0, df)


# =============================================================================
# stratum_4_mask / filter_to_stratum_4
# =============================================================================


class TestStratum4:
    """Correctness checks for the Stratum 4 mask and filter."""

    def test_mask_starts_at_stratum_4_start(self):
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame({
            "date": pd.to_datetime([
                "2022-09-02",  # before Stratum 4 start
                "2022-09-03",  # exact start
                "2022-09-04",  # after start
                "2023-01-01",
                "2026-06-15",
            ]),
        })
        mask = stratum_4_mask(df)
        np.testing.assert_array_equal(mask.to_numpy(), [False, True, True, True, True])

    def test_mask_respects_as_of_date(self):
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame({
            "date": pd.to_datetime([
                "2022-09-03",
                "2024-01-01",
                "2026-06-15",
            ]),
        })
        mask = stratum_4_mask(df, as_of_date="2024-01-01")
        np.testing.assert_array_equal(mask.to_numpy(), [True, True, False])

    def test_filter_returns_new_dataframe(self):
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame({
            "date": pd.to_datetime([
                "2022-09-02",
                "2022-09-03",
                "2023-01-01",
            ]),
            "x": [1, 2, 3],
        })
        result = filter_to_stratum_4(df)
        assert len(result) == 2
        assert list(result["x"]) == [2, 3]
        # Original unchanged
        assert len(df) == 3

    def test_missing_date_column_raises_keyerror(self):
        pd = pytest.importorskip("pandas")
        df = pd.DataFrame({"x": [1, 2, 3]})
        with pytest.raises(KeyError, match="date_column"):
            stratum_4_mask(df)

    def test_stratum_4_start_constant(self):
        """STRATUM_4_START is the canonical 2022-09-03 per MD 1."""
        assert STRATUM_4_START == "2022-09-03"


# =============================================================================
# Loaders (error-handling contract only)
# =============================================================================


class TestLoaders:
    """Test the error-handling contract of the loaders.

    The happy path requires the actual CSVs at ``$GEVOELSCORE_DATA_PATH``
    which are external per the privacy boundary; not smoke-tested here.
    """

    def test_load_master_raises_when_data_path_not_set(self, monkeypatch):
        monkeypatch.delenv("GEVOELSCORE_DATA_PATH", raising=False)
        with pytest.raises(RuntimeError, match="GEVOELSCORE_DATA_PATH is not set"):
            load_master()

    def test_load_master_raises_when_data_path_does_not_exist(self, monkeypatch):
        monkeypatch.setenv("GEVOELSCORE_DATA_PATH", "/nonexistent/path/xyz123")
        with pytest.raises(RuntimeError, match="does not exist"):
            load_master()

    def test_load_crash_labels_raises_when_data_path_not_set(self, monkeypatch):
        monkeypatch.delenv("GEVOELSCORE_DATA_PATH", raising=False)
        with pytest.raises(RuntimeError, match="GEVOELSCORE_DATA_PATH is not set"):
            load_crash_labels()

    def test_resolve_data_root_returns_path_when_set(self, monkeypatch, tmp_path):
        monkeypatch.setenv("GEVOELSCORE_DATA_PATH", str(tmp_path))
        root = _resolve_data_root()
        assert root == tmp_path
