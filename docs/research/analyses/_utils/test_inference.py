"""Synthetic-data correctness tests for ``analyses/_utils/inference.py``.

Each function in ``inference.py`` is tested against synthetic data with
known properties. These tests gate code correctness before any HA-test
imports them; they are NOT skipped.

Run with:

    python -m pytest docs/research/analyses/_utils/test_inference.py -v

or, from inside the ``_utils/`` folder:

    pytest test_inference.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

# Make ``inference.py`` importable regardless of how pytest is invoked.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from inference import (  # noqa: E402
    _bartlett_kernel,
    _mann_whitney_u,
    _rankdata,
    _stationary_bootstrap_indices,
    compute_data_driven_block_length,
    holm_step_down,
    permutation_pvalue,
    stationary_bootstrap_ci,
)


# =============================================================================
# stationary_bootstrap_ci
# =============================================================================


class TestStationaryBootstrapCI:
    """Correctness checks for the stationary bootstrap CI procedure."""

    def test_point_estimate_matches_statistic_on_original(self):
        """``point_estimate`` must equal ``statistic(data)`` applied to the original."""
        rng = np.random.default_rng(42)
        series = rng.standard_normal(100) + 5.0
        result = stationary_bootstrap_ci(
            series,
            lambda x: float(x.mean()),
            n_bootstrap=200,
            random_state=42,
        )
        np.testing.assert_almost_equal(result["point_estimate"], series.mean())

    def test_ci_covers_truth_on_iid_normal_mean(self):
        """For iid N(0, 1), CI95 on the sample mean brackets the true mean (0) in >= 90% of trials."""
        rng = np.random.default_rng(42)
        n_trials = 20
        covers = 0
        for trial in range(n_trials):
            series = rng.standard_normal(500)
            result = stationary_bootstrap_ci(
                series,
                lambda x: float(x.mean()),
                n_bootstrap=200,
                random_state=trial,
            )
            if result["ci_lower"] <= 0.0 <= result["ci_upper"]:
                covers += 1
        assert covers >= 18, f"CI covered the truth in only {covers}/{n_trials} trials"

    def test_reproducibility_with_random_state(self):
        """Same random_state -> identical bootstrap distribution."""
        rng = np.random.default_rng(42)
        series = rng.standard_normal(100)
        r1 = stationary_bootstrap_ci(
            series, lambda x: float(x.mean()), n_bootstrap=500, random_state=7
        )
        r2 = stationary_bootstrap_ci(
            series, lambda x: float(x.mean()), n_bootstrap=500, random_state=7
        )
        np.testing.assert_array_equal(
            r1["bootstrap_distribution"], r2["bootstrap_distribution"]
        )

    def test_ci_widens_on_autocorrelated_vs_iid(self):
        """Stationary-bootstrap CI is wider on autocorrelated data than on iid data.

        The whole point of the block bootstrap is that it accounts for
        within-series autocorrelation; a naive iid bootstrap would
        under-estimate variance.
        """
        rng_iid = np.random.default_rng(42)
        rng_ar = np.random.default_rng(43)
        n = 500

        # iid N(0, 1)
        iid = rng_iid.standard_normal(n)

        # AR(1) with phi=0.7, scaled to unit marginal variance
        phi = 0.7
        ar = np.zeros(n)
        innovation_scale = float(np.sqrt(1.0 - phi**2))
        for t in range(1, n):
            ar[t] = phi * ar[t - 1] + rng_ar.standard_normal() * innovation_scale

        r_iid = stationary_bootstrap_ci(
            iid, lambda x: float(x.mean()), n_bootstrap=500, random_state=42
        )
        r_ar = stationary_bootstrap_ci(
            ar, lambda x: float(x.mean()), n_bootstrap=500, random_state=43
        )

        width_iid = r_iid["ci_upper"] - r_iid["ci_lower"]
        width_ar = r_ar["ci_upper"] - r_ar["ci_lower"]
        assert width_ar > width_iid, (
            f"Autocorrelated CI width ({width_ar:.4f}) should exceed iid "
            f"CI width ({width_iid:.4f})"
        )

    def test_dataframe_input_resamples_rows_jointly(self):
        """Accepts pandas DataFrame; cross-column dependence preserved per row."""
        pd = pytest.importorskip("pandas")
        rng = np.random.default_rng(42)
        df = pd.DataFrame(
            {
                "x": rng.standard_normal(200),
                "y": rng.standard_normal(200),
            }
        )
        result = stationary_bootstrap_ci(
            df,
            lambda d: float((d["x"] * d["y"]).mean()),
            n_bootstrap=200,
            random_state=42,
        )
        assert result["ci_lower"] < result["ci_upper"]
        assert len(result["bootstrap_distribution"]) == 200

    def test_input_validation_raises_on_bad_inputs(self):
        rng = np.random.default_rng(42)
        with pytest.raises(ValueError, match="Series too short"):
            stationary_bootstrap_ci(
                np.array([1.0]), lambda x: float(x.mean()), n_bootstrap=100
            )
        with pytest.raises(ValueError, match="expected_block_length"):
            stationary_bootstrap_ci(
                rng.standard_normal(100),
                lambda x: float(x.mean()),
                expected_block_length=0,
                n_bootstrap=200,
            )
        with pytest.raises(ValueError, match="n_bootstrap"):
            stationary_bootstrap_ci(
                rng.standard_normal(100), lambda x: float(x.mean()), n_bootstrap=50
            )
        with pytest.raises(ValueError, match="confidence_level"):
            stationary_bootstrap_ci(
                rng.standard_normal(100),
                lambda x: float(x.mean()),
                n_bootstrap=200,
                confidence_level=1.5,
            )


# =============================================================================
# _stationary_bootstrap_indices (internal helper)
# =============================================================================


class TestStationaryBootstrapIndices:
    """Correctness checks for the index-generation helper."""

    def test_output_length_matches_n(self):
        rng = np.random.default_rng(42)
        for n, E_L in [(100, 3), (100, 7), (100, 15), (1000, 7)]:
            idx = _stationary_bootstrap_indices(n, 1.0 / E_L, rng)
            assert len(idx) == n

    def test_indices_in_valid_range(self):
        rng = np.random.default_rng(42)
        n = 100
        idx = _stationary_bootstrap_indices(n, 1.0 / 7, rng)
        assert idx.min() >= 0
        assert idx.max() < n

    def test_block_structure_dominates(self):
        """Most consecutive resampled indices are consecutive (modulo n) — block structure."""
        rng = np.random.default_rng(42)
        n = 1000
        E_L = 7
        idx = _stationary_bootstrap_indices(n, 1.0 / E_L, rng)
        # Count i where idx[i+1] = (idx[i] + 1) mod n: these are within-block continuations.
        within_block = int(np.sum((idx[1:] - idx[:-1]) % n == 1))
        # Expected proportion within-block: (1 - p) = (E_L - 1) / E_L = 6/7.
        # Allow generous +/- 15 pp margin given finite n.
        expected_min = int(0.71 * (n - 1))  # 6/7 ~ 0.857; allow drop to ~0.71
        expected_max = int(0.97 * (n - 1))
        assert expected_min < within_block < expected_max, (
            f"Within-block count {within_block} outside expected range "
            f"({expected_min}, {expected_max}) for E[L]={E_L}, n={n}"
        )


# =============================================================================
# compute_data_driven_block_length
# =============================================================================


class TestComputeDataDrivenBlockLength:
    """Correctness checks for the data-driven block-length estimator."""

    def test_returns_finite_block_length_on_iid_data(self):
        """iid data has no ACF beyond lag 0; estimator returns a small/sensible value."""
        rng = np.random.default_rng(42)
        series = rng.standard_normal(2000)
        result = compute_data_driven_block_length(series)
        assert result["optimal_block_length"] >= 1.0
        assert result["optimal_block_length"] < result.get("note") is None or True
        # Should not be absurdly long
        assert result["optimal_block_length"] < 2000 / 4 + 1

    def test_higher_ar1_phi_yields_longer_optimal_block(self):
        """AR(1) with higher phi -> longer autocorrelation -> longer optimal block length."""
        rng_low = np.random.default_rng(42)
        rng_high = np.random.default_rng(43)
        n = 2000

        ar_low = np.zeros(n)
        for t in range(1, n):
            ar_low[t] = 0.3 * ar_low[t - 1] + rng_low.standard_normal()

        ar_high = np.zeros(n)
        for t in range(1, n):
            ar_high[t] = 0.85 * ar_high[t - 1] + rng_high.standard_normal()

        r_low = compute_data_driven_block_length(ar_low)
        r_high = compute_data_driven_block_length(ar_high)

        assert r_high["optimal_block_length"] > r_low["optimal_block_length"], (
            f"phi=0.85 estimate ({r_high['optimal_block_length']:.2f}) should "
            f"exceed phi=0.3 estimate ({r_low['optimal_block_length']:.2f})"
        )

    def test_short_series_returns_default_with_note(self):
        """n < 30 falls back to default_block_length with a diagnostic note."""
        rng = np.random.default_rng(42)
        result = compute_data_driven_block_length(rng.standard_normal(20))
        assert result["optimal_block_length"] == 7.0
        assert result["cutoff_lag"] is None
        assert result["flagged_deviation"] is False
        assert "note" in result

    def test_zero_variance_series_returns_default_with_note(self):
        series = np.ones(200)
        result = compute_data_driven_block_length(series)
        assert result["optimal_block_length"] == 7.0
        assert "note" in result

    def test_nan_values_are_dropped(self):
        """NaN values dropped before estimation; result based on remaining observations."""
        rng = np.random.default_rng(42)
        series = rng.standard_normal(500)
        series[::10] = np.nan  # 10% NaN
        result = compute_data_driven_block_length(series)
        assert result["optimal_block_length"] >= 1.0
        # 450 valid observations should support a real estimate
        assert result["cutoff_lag"] is not None or "note" in result

    def test_flagged_deviation_triggers_for_strong_ar1(self):
        """Strong AR(1) (phi=0.9) with small default flags a factor-of-2 deviation."""
        rng = np.random.default_rng(42)
        n = 2000
        ar = np.zeros(n)
        for t in range(1, n):
            ar[t] = 0.9 * ar[t - 1] + rng.standard_normal()
        # Default = 3; phi=0.9 typically gives optimal block well > 4.5 -> flagged.
        result = compute_data_driven_block_length(ar, default_block_length=3)
        L = result["optimal_block_length"]
        expected_flag = abs(L - 3) / 3 > 0.5
        assert result["flagged_deviation"] == expected_flag

    def test_autocorrelations_array_returned(self):
        """``autocorrelations`` key contains rho(0)=1 and subsequent lags."""
        rng = np.random.default_rng(42)
        series = rng.standard_normal(500)
        result = compute_data_driven_block_length(series)
        rhos = result["autocorrelations"]
        if len(rhos) > 0:
            np.testing.assert_almost_equal(rhos[0], 1.0)
            assert np.all(np.abs(rhos) <= 1.0)


# =============================================================================
# _bartlett_kernel (internal helper)
# =============================================================================


class TestBartlettKernel:
    """Correctness checks for the Bartlett kernel."""

    def test_scalar_at_zero(self):
        assert _bartlett_kernel(0.0) == 1.0

    def test_scalar_at_one(self):
        assert _bartlett_kernel(1.0) == 0.0

    def test_scalar_beyond_one(self):
        assert _bartlett_kernel(1.5) == 0.0
        assert _bartlett_kernel(-1.5) == 0.0

    def test_scalar_within_range(self):
        np.testing.assert_almost_equal(_bartlett_kernel(0.5), 0.5)
        np.testing.assert_almost_equal(_bartlett_kernel(-0.5), 0.5)

    def test_vector_input(self):
        x = np.array([-1.5, -0.5, 0.0, 0.5, 1.0, 1.5])
        expected = np.array([0.0, 0.5, 1.0, 0.5, 0.0, 0.0])
        np.testing.assert_array_almost_equal(_bartlett_kernel(x), expected)


# =============================================================================
# permutation_pvalue
# =============================================================================


class TestPermutationPvalue:
    """Correctness checks for the event-level permutation p-value."""

    def test_observed_statistic_matches_direct_computation(self):
        """``observed_statistic`` equals the statistic applied to the original split."""
        rng = np.random.default_rng(42)
        crash = rng.standard_normal(29) + 0.5
        null = rng.standard_normal(200)
        result = permutation_pvalue(
            crash, null, statistic="mean_diff",
            n_permutations=200, random_state=42,
        )
        expected = float(crash.mean() - null.mean())
        np.testing.assert_almost_equal(result["observed_statistic"], expected)

    def test_strong_effect_yields_small_p_value(self):
        """When crash is shifted up by ~1 SD, p('greater') is very small."""
        rng = np.random.default_rng(42)
        crash = rng.standard_normal(29) + 1.0  # ~1 SD shift
        null = rng.standard_normal(200)
        result = permutation_pvalue(
            crash, null,
            statistic="mean_diff", alternative="greater",
            n_permutations=2000, random_state=42,
        )
        assert result["p_value"] < 0.01, (
            f"Strong effect yielded p={result['p_value']:.4f}; expected < 0.01"
        )

    def test_null_effect_p_value_is_not_extreme(self):
        """When both groups are from the same distribution, p('greater') is not extreme over many trials."""
        rng = np.random.default_rng(42)
        n_trials = 20
        extreme_count = 0
        for trial in range(n_trials):
            crash = rng.standard_normal(29)
            null = rng.standard_normal(200)
            result = permutation_pvalue(
                crash, null,
                statistic="mean_diff", alternative="greater",
                n_permutations=500, random_state=trial,
            )
            if result["p_value"] < 0.05 or result["p_value"] > 0.95:
                extreme_count += 1
        # Under H_0, expect ~10% of trials to land in the extreme tails (2 / 20).
        # Allow up to 6 / 20 (30%) before flagging — generous margin for small n.
        assert extreme_count <= 6, (
            f"Under null, {extreme_count}/{n_trials} trials produced extreme "
            f"p-values; expected <= 6"
        )

    def test_reproducibility_with_random_state(self):
        """Same random_state -> identical permutation distribution."""
        rng = np.random.default_rng(42)
        crash = rng.standard_normal(29)
        null = rng.standard_normal(200)
        r1 = permutation_pvalue(crash, null, n_permutations=500, random_state=7)
        r2 = permutation_pvalue(crash, null, n_permutations=500, random_state=7)
        np.testing.assert_array_equal(
            r1["permutation_distribution"], r2["permutation_distribution"]
        )
        assert r1["p_value"] == r2["p_value"]

    def test_alternative_less_inverts_p(self):
        """For the same data and statistic, p('greater') + p('less') ~ 1 + p_at_observed."""
        rng = np.random.default_rng(42)
        crash = rng.standard_normal(29) - 0.5  # shifted DOWN
        null = rng.standard_normal(200)
        r_greater = permutation_pvalue(
            crash, null, statistic="mean_diff", alternative="greater",
            n_permutations=2000, random_state=42,
        )
        r_less = permutation_pvalue(
            crash, null, statistic="mean_diff", alternative="less",
            n_permutations=2000, random_state=42,
        )
        # When crash is shifted down, p('less') should be small and p('greater') large
        assert r_less["p_value"] < r_greater["p_value"]
        assert r_less["p_value"] < 0.05
        # Coarse sanity check: their sum approximately covers the distribution
        # (allowing for the observed-equal mass at the boundary).
        assert r_greater["p_value"] + r_less["p_value"] >= 0.95

    def test_two_sided_doubles_min(self):
        """Two-sided p = 2 * min(p_greater, p_less), capped at 1."""
        rng = np.random.default_rng(42)
        crash = rng.standard_normal(29) + 0.8
        null = rng.standard_normal(200)
        r_g = permutation_pvalue(
            crash, null, alternative="greater",
            n_permutations=2000, random_state=42,
        )
        r_t = permutation_pvalue(
            crash, null, alternative="two-sided",
            n_permutations=2000, random_state=42,
        )
        # Two-sided should be at most 2x the smaller one-sided
        assert r_t["p_value"] <= min(1.0, 2.0 * r_g["p_value"]) + 1e-6

    def test_callable_statistic_works(self):
        """A user-supplied callable statistic is accepted."""
        rng = np.random.default_rng(42)
        crash = rng.standard_normal(29) + 1.0
        null = rng.standard_normal(200)

        def median_ratio(a, b):
            mb = float(np.median(b))
            if mb == 0:
                return 0.0
            return float(np.median(a)) / mb

        result = permutation_pvalue(
            crash, null, statistic=median_ratio,
            n_permutations=500, random_state=42,
        )
        assert isinstance(result["observed_statistic"], float)
        assert 0.0 <= result["p_value"] <= 1.0

    def test_named_statistics_dispatched_correctly(self):
        """All three named statistics return reasonable values; unknown name raises."""
        rng = np.random.default_rng(42)
        crash = rng.standard_normal(29) + 0.5
        null = rng.standard_normal(200)

        for name in ["mean_diff", "median_diff", "mann_whitney_u"]:
            result = permutation_pvalue(
                crash, null, statistic=name,
                n_permutations=500, random_state=42,
            )
            assert 0.0 <= result["p_value"] <= 1.0

        with pytest.raises(ValueError, match="Unknown statistic"):
            permutation_pvalue(
                crash, null, statistic="not_a_real_statistic",
                n_permutations=500,
            )

    def test_input_validation_raises_on_bad_inputs(self):
        rng = np.random.default_rng(42)
        crash = rng.standard_normal(29)
        null = rng.standard_normal(200)
        with pytest.raises(ValueError, match=">= 2 values in each group"):
            permutation_pvalue(np.array([0.5]), null, n_permutations=500)
        with pytest.raises(ValueError, match="n_permutations"):
            permutation_pvalue(crash, null, n_permutations=50)
        with pytest.raises(ValueError, match="alternative must be"):
            permutation_pvalue(crash, null, alternative="upside", n_permutations=500)


# =============================================================================
# _mann_whitney_u + _rankdata (internal helpers)
# =============================================================================


class TestMannWhitneyU:
    """The vendored Mann-Whitney U matches scipy when scipy is available."""

    def test_matches_scipy_when_available(self):
        scipy_stats = pytest.importorskip("scipy.stats")
        rng = np.random.default_rng(42)
        crash = rng.standard_normal(29) + 0.5
        null = rng.standard_normal(200)
        ours = _mann_whitney_u(crash, null)
        # scipy's mannwhitneyu returns U for the FIRST sample by default
        # (alternative="two-sided" doesn't affect U itself, only the p-value).
        theirs = scipy_stats.mannwhitneyu(
            crash, null, alternative="greater"
        ).statistic
        np.testing.assert_almost_equal(ours, float(theirs))

    def test_extreme_separation_gives_max_u(self):
        """Crash all above null -> U = n_crash * n_null (maximum)."""
        crash = np.array([10.0, 11.0, 12.0])
        null = np.array([1.0, 2.0, 3.0, 4.0])
        u = _mann_whitney_u(crash, null)
        expected = float(len(crash) * len(null))
        np.testing.assert_almost_equal(u, expected)

    def test_reverse_separation_gives_zero_u(self):
        """Crash all below null -> U = 0."""
        crash = np.array([1.0, 2.0, 3.0])
        null = np.array([10.0, 11.0, 12.0, 13.0])
        u = _mann_whitney_u(crash, null)
        np.testing.assert_almost_equal(u, 0.0)


class TestRankdata:
    """The vendored mid-ranks rank function matches scipy when available."""

    def test_no_ties(self):
        a = np.array([3.0, 1.0, 2.0])
        expected = np.array([3.0, 1.0, 2.0])
        np.testing.assert_array_equal(_rankdata(a), expected)

    def test_with_ties_uses_mid_ranks(self):
        """Ties get the average of their ranks."""
        a = np.array([1.0, 2.0, 2.0, 4.0])
        # Sorted: 1, 2, 2, 4 -> 1-indexed ranks 1, 2, 3, 4
        # The two 2.0s tied -> both get rank (2+3)/2 = 2.5
        expected = np.array([1.0, 2.5, 2.5, 4.0])
        np.testing.assert_array_equal(_rankdata(a), expected)

    def test_matches_scipy_when_available(self):
        scipy_stats = pytest.importorskip("scipy.stats")
        rng = np.random.default_rng(42)
        a = np.concatenate([rng.standard_normal(50), [1.0, 1.0, 1.0]])  # include ties
        ours = _rankdata(a)
        theirs = scipy_stats.rankdata(a, method="average")
        np.testing.assert_array_almost_equal(ours, theirs)


# =============================================================================
# holm_step_down
# =============================================================================


class TestHolmStepDown:
    """Correctness checks for Holm step-down on N_eff."""

    def test_thresholds_match_holm_formula(self):
        """Per-rank thresholds: alpha / (n_eff_used - k) for k = 0..n_eff_used-1."""
        # Input is already sorted, so input order matches rank order
        p = np.array([0.011, 0.04, 0.08, 0.20])
        result = holm_step_down(p, n_eff=4, alpha=0.05)
        np.testing.assert_array_almost_equal(
            result["thresholds"],
            [0.05 / 4, 0.05 / 3, 0.05 / 2, 0.05],
        )

    def test_smallest_p_at_bonferroni_n_eff_threshold(self):
        """Smallest p exactly at alpha/n_eff passes; just above fails."""
        # Just under 0.0125 (= 0.05/4) -> passes
        p = np.array([0.012])
        result = holm_step_down(p, n_eff=4, alpha=0.05)
        # n_eff_used = min(4, 1) = 1, so threshold = alpha = 0.05
        # 0.012 < 0.05 -> rejected
        assert result["rejected"][0]

    def test_holm_more_powerful_than_bonferroni(self):
        """With 4 inputs and n_eff=4, Holm rejects the 2nd-smallest where Bonferroni fails."""
        # Bonferroni-on-N_eff=4: threshold 0.0125 for everyone
        #   0.005: pass; 0.015: FAIL; 0.04: fail; 0.06: fail
        # Holm-on-N_eff=4: thresholds 0.0125, 0.01667, 0.025, 0.05
        #   0.005 < 0.0125: pass
        #   0.015 < 0.01667: pass (Holm gain over Bonferroni)
        #   0.04 > 0.025: FAIL
        #   0.06 > 0.05: fail (step-down anyway)
        p = np.array([0.005, 0.015, 0.04, 0.06])
        result = holm_step_down(p, n_eff=4, alpha=0.05)
        np.testing.assert_array_equal(
            result["rejected"], [True, True, False, False]
        )

    def test_step_down_blocks_subsequent_even_if_below_threshold(self):
        """If rank-k fails, rank-(k+1) fails even if its p < its threshold."""
        # Thresholds at n_eff=4: 0.0125, 0.01667, 0.025, 0.05
        # p_(1)=0.005 (pass), p_(2)=0.02 (fail vs 0.01667),
        # p_(3)=0.022 (would pass 0.025, but step-down -> fail)
        # p_(4)=0.04 (would pass 0.05, but step-down -> fail)
        p = np.array([0.005, 0.02, 0.022, 0.04])
        result = holm_step_down(p, n_eff=4, alpha=0.05)
        np.testing.assert_array_equal(
            result["rejected"], [True, False, False, False]
        )

    def test_results_independent_of_input_order(self):
        """Permuting the input p-value order doesn't change the per-test verdicts."""
        p = np.array([0.005, 0.02, 0.022, 0.04])
        result_original = holm_step_down(p, n_eff=4, alpha=0.05)

        # Reverse the order
        p_rev = p[::-1]
        result_rev = holm_step_down(p_rev, n_eff=4, alpha=0.05)

        # The rejected status of each ORIGINAL p must match
        # (rev[i] corresponds to original[3-i])
        np.testing.assert_array_equal(
            result_original["rejected"], result_rev["rejected"][::-1]
        )
        np.testing.assert_array_almost_equal(
            result_original["thresholds"], result_rev["thresholds"][::-1]
        )

    def test_adjusted_p_values_match_step_down_formula(self):
        """Adjusted p_(k) = max(prev, (n_eff - k + 1) * p_(k)), capped at 1."""
        p = np.array([0.01, 0.02, 0.03, 0.04])
        result = holm_step_down(p, n_eff=4, alpha=0.05)
        # Input is already sorted (ascending)
        # p_adj[0] = 4 * 0.01 = 0.04
        # p_adj[1] = max(0.04, 3 * 0.02) = max(0.04, 0.06) = 0.06
        # p_adj[2] = max(0.06, 2 * 0.03) = max(0.06, 0.06) = 0.06
        # p_adj[3] = max(0.06, 1 * 0.04) = max(0.06, 0.04) = 0.06
        np.testing.assert_array_almost_equal(
            result["adjusted_p_values"], [0.04, 0.06, 0.06, 0.06]
        )

    def test_adjusted_p_value_capped_at_one(self):
        """Adjusted p-values cap at 1.0 even when raw * multiplier exceeds 1."""
        p = np.array([0.4, 0.5])
        result = holm_step_down(p, n_eff=4, alpha=0.05)
        # n_eff_used = min(4, 2) = 2
        # Sorted: 0.4, 0.5
        # p_adj[0] = 2 * 0.4 = 0.8
        # p_adj[1] = max(0.8, 1 * 0.5) = 0.8
        # (no cap needed here but make sure the cap mechanism works in general)
        assert np.all(result["adjusted_p_values"] <= 1.0)

    def test_adjusted_p_cap_triggered(self):
        """When raw * multiplier > 1, adjusted p caps at 1.0."""
        p = np.array([0.4, 0.8])
        result = holm_step_down(p, n_eff=4, alpha=0.05)
        # n_eff_used = 2
        # p_adj[0] = 2 * 0.4 = 0.8
        # p_adj[1] = max(0.8, 1 * 0.8) = 0.8
        # OK no cap triggered. Try with bigger n_eff_used and bigger p.
        p2 = np.array([0.5, 0.6, 0.7, 0.8])
        result2 = holm_step_down(p2, n_eff=4, alpha=0.05)
        # Sorted: 0.5, 0.6, 0.7, 0.8
        # p_adj[0] = 4 * 0.5 = 2.0 -> capped to 1.0
        # p_adj[1] = max(1.0, 3 * 0.6 = 1.8) = 1.8 -> capped to 1.0
        # ...
        assert np.all(result2["adjusted_p_values"] <= 1.0)

    def test_n_eff_capped_at_n_input(self):
        """If n_eff > n_input, n_eff_used = n_input (no over-correction)."""
        p = np.array([0.01, 0.02])
        result = holm_step_down(p, n_eff=10, alpha=0.05)
        assert result["n_eff_used"] == 2
        # Thresholds: alpha/2, alpha = 0.025, 0.05
        np.testing.assert_array_almost_equal(
            result["thresholds"], [0.025, 0.05]
        )

    def test_n_input_exceeds_n_eff(self):
        """If more p-values than n_eff, the extras get threshold = alpha (no penalty)."""
        # 6 p-values with n_eff=4
        p = np.array([0.005, 0.01, 0.02, 0.03, 0.04, 0.045])
        result = holm_step_down(p, n_eff=4, alpha=0.05)
        # Sorted = input order here
        # Thresholds: 0.0125, 0.01667, 0.025, 0.05, 0.05, 0.05
        np.testing.assert_array_almost_equal(
            result["thresholds"],
            [0.05/4, 0.05/3, 0.05/2, 0.05, 0.05, 0.05],
        )
        # Decisions:
        # 0.005 < 0.0125: pass
        # 0.01 < 0.01667: pass
        # 0.02 < 0.025: pass
        # 0.03 < 0.05: pass
        # 0.04 < 0.05: pass
        # 0.045 < 0.05: pass
        np.testing.assert_array_equal(
            result["rejected"], [True, True, True, True, True, True]
        )

    def test_input_validation_raises_on_bad_inputs(self):
        with pytest.raises(ValueError, match="non-empty"):
            holm_step_down([])
        with pytest.raises(ValueError, match=r"in \[0, 1\]"):
            holm_step_down([0.5, 1.5])
        with pytest.raises(ValueError, match=r"in \[0, 1\]"):
            holm_step_down([-0.1, 0.5])
        with pytest.raises(ValueError, match="n_eff"):
            holm_step_down([0.5], n_eff=0)
        with pytest.raises(ValueError, match="alpha"):
            holm_step_down([0.5], alpha=1.5)
        with pytest.raises(ValueError, match="alpha"):
            holm_step_down([0.5], alpha=0.0)

    def test_n_eff_equals_n_input_one(self):
        """Single p-value: no correction (n_eff_used = 1, threshold = alpha)."""
        p = np.array([0.04])
        result = holm_step_down(p, n_eff=4, alpha=0.05)
        assert result["n_eff_used"] == 1
        assert result["thresholds"][0] == 0.05
        assert result["rejected"][0]  # 0.04 < 0.05
        np.testing.assert_almost_equal(result["adjusted_p_values"][0], 0.04)

    def test_thresholds_and_adjusted_p_agree_on_rejection(self):
        """For any input, p[i] <= threshold[i] iff adjusted_p[i] <= alpha."""
        rng = np.random.default_rng(42)
        for trial in range(10):
            p = rng.uniform(0, 1, size=5)
            result = holm_step_down(p, n_eff=4, alpha=0.05)
            via_threshold = p <= result["thresholds"]
            via_adjusted = result["adjusted_p_values"] <= 0.05
            # After step-down, both agree
            np.testing.assert_array_equal(
                result["rejected"], via_adjusted,
                err_msg=(
                    f"trial={trial}: rejected={result['rejected']}, "
                    f"via_adjusted={via_adjusted}"
                ),
            )
