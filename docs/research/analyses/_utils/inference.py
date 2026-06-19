"""Shared statistical-inference utilities for HA-numbered hypothesis tests.

Implements the resampling + multiplicity layer of the project's
methodology stack. Frame / data-prep utilities (z-score against personal
baseline, crash-drop sensitivity wrapper, Stratum 4 filter, loaders)
live in ``frame.py`` per the two-module organisation locked 2026-06-15.

Public functions:

1. ``stationary_bootstrap_ci`` --- Politis & Romano (1994) stationary
   bootstrap with random block lengths drawn from a geometric
   distribution (E[L] = 7 days by default per
   ``../../methodology/permutation_null_block_length.md``). Returns the
   95% CI on a user-supplied statistic. Day-resampling layer
   (within-construction-window resampling); distinct from the event-level
   permutation null in ``block_permutation_pvalue`` per the chained-
   regime doc Cross-cutting hygiene section 4 (two-resampling-layers
   distinction).

2. ``compute_data_driven_block_length`` --- companion data-driven
   estimator (Politis-White 2004 with Patton-Politis-White 2009
   correction for the stationary bootstrap). Returns the empirical
   optimum E[L]* and flags a factor-of-2 deviation from the project
   default. Per the methodology MD Open follow-ups + Q13 in
   ``../../methodology/queued_work.md``.

3. ``permutation_pvalue`` --- event-level permutation null at n=29
   crash episodes. The resolution of the null distribution is dominated
   by combinatorics (C(n_crash + n_null, n_crash) is the binding
   constraint, not block length); the day-resampling block-length
   policy from ``stationary_bootstrap_ci`` does NOT apply at this layer.
   Per chained-regime doc Cross-cutting hygiene section 4
   (two-resampling-layers distinction).

4. ``holm_step_down`` --- Holm step-down multiplicity correction on
   N_eff approximately 4 effectively independent channels per
   chained-regime doc Cross-cutting hygiene section 3 +
   ``../../analyses/garmin_exploration/cards/cross-channel-correlation.md``.

Each public function has a companion test in ``test_inference.py``
(synthetic-data correctness check before any HA-test imports it).
The companion tests gate correctness; they are not skipped.
"""

from __future__ import annotations

import numpy as np


__all__ = [
    "stationary_bootstrap_ci",
    "compute_data_driven_block_length",
    "permutation_pvalue",
    "holm_step_down",
]


# -----------------------------------------------------------------------------
# stationary_bootstrap_ci (Politis & Romano 1994)
# -----------------------------------------------------------------------------


def stationary_bootstrap_ci(
    data,
    statistic,
    *,
    n_bootstrap: int = 5000,
    expected_block_length: int = 7,
    confidence_level: float = 0.95,
    random_state: int | None = None,
):
    """Compute bootstrap CI on a statistic using the stationary bootstrap.

    Politis & Romano (1994) stationary bootstrap. Resampled blocks have
    random lengths drawn from a geometric distribution with mean
    ``expected_block_length``; the resampled series is itself stationary
    by construction, which removes the fixed-edge bias of the
    moving-block bootstrap and makes it robust to mild non-stationarity.

    Day-resampling layer per
    ``../../methodology/permutation_null_block_length.md``.

    Parameters
    ----------
    data : array-like or pandas DataFrame
        Time series. 1D array-like (resamples scalar observations) or
        pandas DataFrame (resamples rows; columns are kept aligned at
        each resampled row, preserving cross-column dependence at each
        time point).
    statistic : callable
        Function taking the resampled data (same shape / type as input)
        and returning a scalar.
    n_bootstrap : int, keyword-only
        Number of bootstrap iterations. Default 5000.
    expected_block_length : int, keyword-only
        Mean block length E[L] of the geometric distribution. Default 7
        per CONVENTIONS §3 + methodology MD.
    confidence_level : float, keyword-only
        Two-sided confidence level (e.g. 0.95 -> CI95). Default 0.95.
    random_state : int or None, keyword-only
        Random seed for reproducibility. Default None (non-reproducible).

    Returns
    -------
    dict
        Keys:
        - ``point_estimate`` (float): statistic applied to the original
          data.
        - ``ci_lower`` (float): lower bound of the CI at the chosen
          confidence level.
        - ``ci_upper`` (float): upper bound of the CI.
        - ``bootstrap_distribution`` (ndarray of length n_bootstrap):
          all bootstrap statistic values.

    Raises
    ------
    ValueError
        If ``n < 2``, ``expected_block_length < 1``, ``n_bootstrap < 100``,
        or ``confidence_level`` not in (0, 1).

    Notes
    -----
    Uses circular indexing at the series boundary (resampled blocks
    can wrap from the end to the start). For n >> expected_block_length
    this has negligible effect.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(42)
    >>> series = rng.standard_normal(1000)
    >>> result = stationary_bootstrap_ci(
    ...     series, lambda x: float(x.mean()),
    ...     n_bootstrap=500, random_state=42,
    ... )
    >>> abs(result["point_estimate"]) < 0.1  # near zero
    True
    >>> result["ci_lower"] < 0 < result["ci_upper"]  # CI brackets the truth
    True
    """
    rng = np.random.default_rng(random_state)

    has_pandas_api = hasattr(data, "iloc")

    if has_pandas_api:
        n = len(data)
        data_arr = None
    else:
        data_arr = np.asarray(data)
        n = data_arr.shape[0]

    if n < 2:
        raise ValueError(f"Series too short for bootstrap: n={n}")
    if expected_block_length < 1:
        raise ValueError(
            f"expected_block_length must be >= 1, got {expected_block_length}"
        )
    if n_bootstrap < 100:
        raise ValueError(
            f"n_bootstrap must be >= 100 for stable CI estimates, got {n_bootstrap}"
        )
    if not 0 < confidence_level < 1:
        raise ValueError(
            f"confidence_level must be in (0, 1), got {confidence_level}"
        )

    p = 1.0 / expected_block_length

    point_estimate = float(statistic(data))

    boot_stats = np.empty(n_bootstrap)
    for b in range(n_bootstrap):
        idx = _stationary_bootstrap_indices(n, p, rng)
        if has_pandas_api:
            resampled = data.iloc[idx]
        else:
            resampled = data_arr[idx]
        boot_stats[b] = float(statistic(resampled))

    alpha = (1.0 - confidence_level) / 2.0
    return {
        "point_estimate": point_estimate,
        "ci_lower": float(np.quantile(boot_stats, alpha)),
        "ci_upper": float(np.quantile(boot_stats, 1.0 - alpha)),
        "bootstrap_distribution": boot_stats,
    }


def _stationary_bootstrap_indices(n: int, p: float, rng) -> np.ndarray:
    """Generate indices for one stationary bootstrap resample.

    Internal helper for ``stationary_bootstrap_ci``. Block lengths are
    drawn from Geom(p) with mean 1/p. Indices wrap circularly at the
    series boundary.
    """
    indices = np.empty(n, dtype=np.int64)
    i = 0
    while i < n:
        start = int(rng.integers(0, n))
        block_length = int(rng.geometric(p))
        for j in range(block_length):
            if i >= n:
                break
            indices[i] = (start + j) % n
            i += 1
    return indices


# -----------------------------------------------------------------------------
# compute_data_driven_block_length (Politis-White / Patton-Politis-White)
# -----------------------------------------------------------------------------


def compute_data_driven_block_length(
    series,
    *,
    c: float = 2.0,
    default_block_length: int = 7,
    deviation_flag_factor: float = 0.5,
):
    """Estimate optimal stationary-bootstrap expected block length from data.

    Implements the Politis-White (2004) automatic block-length selection
    with the Patton-Politis-White (2009) correction for the stationary
    bootstrap. Finds the lag M at which the autocorrelation becomes
    statistically insignificant, then derives the optimal E[L] from a
    Bartlett-kernel spectral density estimate.

    Companion to ``stationary_bootstrap_ci``: flags a factor-of-2
    deviation between the data-driven optimum and the project default
    (E[L] = 7), per
    ``../../methodology/permutation_null_block_length.md`` Open
    follow-ups + ``../../methodology/queued_work.md`` Q13.

    Parameters
    ----------
    series : array-like, 1D
        Input time series. NaN values are dropped before estimation.
    c : float, keyword-only
        Threshold constant for autocorrelation significance:
        ``|rho(k)| > c * sqrt(log(n) / n)`` is considered significant.
        Default 2.0 per Politis-White convention.
    default_block_length : int, keyword-only
        Fallback when n is too small, ACF has no clear cutoff, or the
        closed-form formula degenerates. Also the reference value for
        ``flagged_deviation``. Default 7 per the project methodology MD.
    deviation_flag_factor : float, keyword-only
        Flag a factor-of-X deviation:
        ``True`` if ``|E[L]* - default| / default > deviation_flag_factor``.
        Default 0.5 = factor-of-2 deviation per methodology MD Open
        follow-ups.

    Returns
    -------
    dict
        Keys:
        - ``optimal_block_length`` (float): estimated E[L]*, bounded
          between 1.0 and n/4.
        - ``cutoff_lag`` (int or None): the lag M used as ACF
          truncation; ``None`` if no clear cutoff was found.
        - ``flagged_deviation`` (bool): True if the estimate deviates
          from ``default_block_length`` by more than
          ``deviation_flag_factor``.
        - ``autocorrelations`` (ndarray): sample autocorrelations
          rho(0), rho(1), ..., rho(max_lag).
        - ``note`` (str, optional): diagnostic note if estimation fell
          back to the default.

    Notes
    -----
    Uses the Bartlett kernel for spectral density estimation. The
    cutoff-lag rule (Politis-White): smallest m >= 1 such that
    rho(m+1), ..., rho(m+K_n) are all below the significance threshold,
    where K_n = max(5, ceil(log10(n))).

    Examples
    --------
    >>> import numpy as np
    >>> # AR(1) with phi=0.5: theoretical ACF rho(k) = 0.5^k
    >>> rng = np.random.default_rng(42)
    >>> n = 2000
    >>> series = np.zeros(n)
    >>> for t in range(1, n):
    ...     series[t] = 0.5 * series[t-1] + rng.standard_normal()
    >>> result = compute_data_driven_block_length(series)
    >>> result["optimal_block_length"] > 0
    True
    """
    series = np.asarray(series, dtype=float)
    series = series[~np.isnan(series)]
    n = len(series)

    if n < 30:
        return {
            "optimal_block_length": float(default_block_length),
            "cutoff_lag": None,
            "flagged_deviation": False,
            "autocorrelations": np.array([]),
            "note": (
                f"n={n} < 30; insufficient data for reliable estimation; "
                f"returning default {default_block_length}"
            ),
        }

    K_n = max(5, int(np.ceil(np.log10(n))))
    max_lag = max(5 * K_n, K_n + 10)
    max_lag = min(max_lag, n // 4)

    series_centered = series - series.mean()
    var = float((series_centered**2).mean())
    if var == 0:
        return {
            "optimal_block_length": float(default_block_length),
            "cutoff_lag": None,
            "flagged_deviation": False,
            "autocorrelations": np.array([]),
            "note": "Series has zero variance; returning default",
        }

    rhos = np.zeros(max_lag + 1)
    rhos[0] = 1.0
    for k in range(1, max_lag + 1):
        rhos[k] = float((series_centered[:-k] * series_centered[k:]).mean()) / var

    threshold = c * np.sqrt(np.log(n) / n)

    # Politis-White cutoff-lag rule: smallest m >= 1 such that
    # rho(m+1), ..., rho(m+K_n) are all below the threshold.
    M: int | None = None
    for m in range(1, max_lag - K_n + 1):
        window = rhos[m + 1 : m + 1 + K_n]
        if np.all(np.abs(window) < threshold):
            M = m
            break

    if M is None or M == 0:
        # Fallback: smallest lag k >= 1 where |rho(k)| first drops below threshold.
        below = np.where(np.abs(rhos[1:]) < threshold)[0]
        if len(below) > 0:
            M = int(below[0]) + 1
        else:
            return {
                "optimal_block_length": float(default_block_length),
                "cutoff_lag": None,
                "flagged_deviation": False,
                "autocorrelations": rhos,
                "note": (
                    "No clear ACF cutoff (all lags within max_lag are "
                    "significant); returning default"
                ),
            }

    # Patton-Politis-White (2009) formula for the stationary bootstrap:
    #   L* = (2 * G^2 / D_SB)^(1/3) * n^(1/3)
    # where G    = 2 * sum_{k=1}^{2M} lambda(k/M) * k * rho(k)
    # and   D_SB = 2 * (1 + 2 * sum_{k=1}^{2M} lambda(k/M) * rho(k))^2
    # with lambda the Bartlett kernel.
    upper_lag = min(2 * M, max_lag)
    k_range = np.arange(1, upper_lag + 1)
    lambdas = _bartlett_kernel(k_range / M)
    rho_subset = rhos[1 : upper_lag + 1]

    G_hat = float(2.0 * np.sum(lambdas * k_range * rho_subset))
    g_sum = float(1.0 + 2.0 * np.sum(lambdas * rho_subset))
    D_SB = 2.0 * g_sum**2

    if D_SB <= 1e-10 or G_hat == 0.0:
        return {
            "optimal_block_length": float(default_block_length),
            "cutoff_lag": int(M),
            "flagged_deviation": False,
            "autocorrelations": rhos,
            "note": "Closed-form formula degenerate; returning default",
        }

    L_opt_raw = ((2.0 * G_hat**2 / abs(D_SB)) ** (1.0 / 3.0)) * (n ** (1.0 / 3.0))
    L_opt = float(max(1.0, min(L_opt_raw, n / 4)))

    flagged = abs(L_opt - default_block_length) / default_block_length > deviation_flag_factor

    return {
        "optimal_block_length": L_opt,
        "cutoff_lag": int(M),
        "flagged_deviation": flagged,
        "autocorrelations": rhos,
    }


def _bartlett_kernel(x):
    """Bartlett kernel: lambda(x) = 1 - |x| for |x| <= 1, else 0.

    Vectorised: x can be scalar or array.
    """
    return np.maximum(0.0, 1.0 - np.abs(x))


# -----------------------------------------------------------------------------
# permutation_pvalue (event-level permutation per chained-regime §4)
# -----------------------------------------------------------------------------


def permutation_pvalue(
    crash_values,
    null_values,
    *,
    statistic="mean_diff",
    n_permutations: int = 10000,
    alternative: str = "greater",
    random_state: int | None = None,
):
    """Compute a permutation p-value for a discrimination statistic on
    crash-event vs null-event values.

    **Event-level permutation layer** per chained-regime doc
    Cross-cutting hygiene section 4 (two-resampling-layers distinction).
    At n=29 crash episodes (typical project scale), the resolution of
    the null distribution is dominated by combinatorics —
    C(n_crash + n_null, n_crash) is the binding constraint, NOT block
    length. The day-resampling block-length policy from
    ``stationary_bootstrap_ci`` (E[L]=7) does NOT apply at this layer
    because pre-aggregated event values have no within-event temporal
    structure to preserve.

    Parameters
    ----------
    crash_values : array-like
        Pre-aggregated per-event statistics for crash events
        (one value per crash episode; project default n=29 in Stratum 4).
    null_values : array-like
        Pre-aggregated per-event statistics for matched non-crash
        windows (project default n=200 per HA01b protocol).
    statistic : str or callable, keyword-only
        Statistic to compute on (crash_array, null_array). Built-in
        names:

        - "mean_diff" (default): mean(crash) - mean(null)
        - "median_diff": median(crash) - median(null)
        - "mann_whitney_u": Mann-Whitney U with crash as the first
          sample (not standardised; useful for distribution shifts)

        Or a callable ``f(crash_array, null_array) -> float`` for any
        custom discrimination statistic (e.g. fraction-meeting-threshold
        difference in percentage points; Cliff's delta; Jonckheere-
        Terpstra against a stratification; etc.).
    n_permutations : int, keyword-only
        Number of Monte Carlo permutations. Default 10000.
        At n_crash=29 + n_null=200, the exact-enumeration count
        C(229, 29) is astronomical, so Monte Carlo always suffices.
    alternative : str, keyword-only
        Direction of the one-sided test:

        - "greater" (default): p = P(perm_stat >= observed_stat) under H_0
        - "less": p = P(perm_stat <= observed_stat) under H_0
        - "two-sided": p = 2 * min(p_greater, p_less), capped at 1.0

    random_state : int or None, keyword-only
        Random seed for reproducibility. Default None.

    Returns
    -------
    dict
        Keys:

        - ``observed_statistic`` (float): the statistic on the original
          (un-permuted) crash vs null split.
        - ``p_value`` (float): the permutation p-value per
          ``alternative``.
        - ``n_permutations`` (int): the number of Monte Carlo
          iterations actually run.
        - ``alternative`` (str): the requested alternative.
        - ``permutation_distribution`` (ndarray of length
          n_permutations): all permuted statistic values.

    Raises
    ------
    ValueError
        If ``len(crash_values) < 2`` or ``len(null_values) < 2``;
        if ``n_permutations < 100``; if ``alternative`` not in
        ``{"greater", "less", "two-sided"}``; if a string ``statistic``
        is not recognised.

    Notes
    -----
    The minimum achievable p-value is ``1 / n_permutations`` (for the
    one-sided case). At the project default of 10000 permutations, the
    minimum p-value is 0.0001 — adequate for the Holm-on-N_eff=4
    multiplicity threshold of α/4 = 0.0125.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(42)
    >>> # Clear effect: crash values shifted up by 1 SD
    >>> crash = rng.standard_normal(29) + 1.0
    >>> null = rng.standard_normal(200)
    >>> result = permutation_pvalue(
    ...     crash, null,
    ...     statistic="mean_diff",
    ...     n_permutations=5000,
    ...     random_state=42,
    ... )
    >>> result["p_value"] < 0.001
    True

    >>> # Null effect: both groups from the same distribution
    >>> a = rng.standard_normal(29)
    >>> b = rng.standard_normal(200)
    >>> result = permutation_pvalue(a, b, n_permutations=5000, random_state=42)
    >>> 0.01 < result["p_value"] < 0.99  # not extreme
    True
    """
    crash_arr = np.asarray(crash_values, dtype=float)
    null_arr = np.asarray(null_values, dtype=float)

    n_crash = len(crash_arr)
    n_null = len(null_arr)

    if n_crash < 2 or n_null < 2:
        raise ValueError(
            f"Need >= 2 values in each group; got n_crash={n_crash}, n_null={n_null}"
        )
    if n_permutations < 100:
        raise ValueError(
            f"n_permutations must be >= 100 for a stable Monte Carlo "
            f"estimate, got {n_permutations}"
        )
    if alternative not in {"greater", "less", "two-sided"}:
        raise ValueError(
            f"alternative must be one of {{'greater', 'less', 'two-sided'}}, "
            f"got {alternative!r}"
        )

    stat_fn = _resolve_statistic(statistic)

    observed = float(stat_fn(crash_arr, null_arr))

    pooled = np.concatenate([crash_arr, null_arr])
    n_total = n_crash + n_null

    rng = np.random.default_rng(random_state)
    perm_stats = np.empty(n_permutations)
    for b in range(n_permutations):
        idx = rng.permutation(n_total)
        crash_perm = pooled[idx[:n_crash]]
        null_perm = pooled[idx[n_crash:]]
        perm_stats[b] = float(stat_fn(crash_perm, null_perm))

    if alternative == "greater":
        p = float(np.mean(perm_stats >= observed))
    elif alternative == "less":
        p = float(np.mean(perm_stats <= observed))
    else:  # two-sided
        p_g = float(np.mean(perm_stats >= observed))
        p_l = float(np.mean(perm_stats <= observed))
        p = float(min(1.0, 2.0 * min(p_g, p_l)))

    return {
        "observed_statistic": observed,
        "p_value": p,
        "n_permutations": n_permutations,
        "alternative": alternative,
        "permutation_distribution": perm_stats,
    }


def _resolve_statistic(statistic):
    """Resolve a statistic spec (str name or callable) to a callable.

    Internal helper for ``permutation_pvalue``.
    """
    if callable(statistic):
        return statistic
    if statistic == "mean_diff":
        return lambda crash, null: crash.mean() - null.mean()
    if statistic == "median_diff":
        return lambda crash, null: float(np.median(crash) - np.median(null))
    if statistic == "mann_whitney_u":
        return _mann_whitney_u
    raise ValueError(
        f"Unknown statistic name: {statistic!r}. Use one of "
        f"{{'mean_diff', 'median_diff', 'mann_whitney_u'}} or pass a callable."
    )


def _mann_whitney_u(crash, null):
    """Compute Mann-Whitney U with crash as the first sample.

    Returns the U statistic without ties correction or standardisation;
    the permutation null does its own calibration so we don't need the
    normal approximation here.
    """
    n_crash = len(crash)
    n_null = len(null)
    pooled = np.concatenate([crash, null])
    ranks = _rankdata(pooled)
    crash_rank_sum = float(ranks[:n_crash].sum())
    u = crash_rank_sum - n_crash * (n_crash + 1.0) / 2.0
    return u


def _rankdata(a):
    """Rank data with mid-ranks for ties.

    Vendored to avoid a hard scipy dependency for one function.
    """
    a = np.asarray(a, dtype=float)
    n = len(a)
    order = np.argsort(a, kind="mergesort")
    sorted_a = a[order]
    ranks = np.empty(n, dtype=float)
    # Assign ranks; handle ties by averaging.
    i = 0
    while i < n:
        j = i + 1
        while j < n and sorted_a[j] == sorted_a[i]:
            j += 1
        avg_rank = (i + j + 1) / 2.0  # 1-indexed rank
        for k in range(i, j):
            ranks[order[k]] = avg_rank
        i = j
    return ranks


# -----------------------------------------------------------------------------
# holm_step_down (Holm 1979 step-down on N_eff)
# -----------------------------------------------------------------------------


def holm_step_down(
    p_values,
    *,
    n_eff: int = 4,
    alpha: float = 0.05,
):
    """Apply Holm step-down multiplicity correction on N_eff effectively
    independent channels.

    Holm (1979) step-down procedure with the modification that
    multiplicity is corrected at the EFFECTIVE-N level rather than the
    raw test count. For the project's Tier 1 + Tier 2 hypothesis family
    on the 7 underlying primitives with ~3-4 effective independent
    channels per
    ``../../analyses/garmin_exploration/cards/cross-channel-correlation.md``,
    this means per-rank thresholds ``alpha / N_eff``,
    ``alpha / (N_eff - 1)``, ..., ``alpha / 1`` on the ordered p-values.

    Per chained-regime doc Cross-cutting hygiene section 3.

    Holm is uniformly more powerful than Bonferroni-on-N_eff: the
    smallest p-value gets the same threshold (``alpha / N_eff``), but
    the 2nd through N_eff-th smallest get progressively relaxed
    thresholds. Closed-form, deterministic, no permutations.

    Parameters
    ----------
    p_values : array-like of float
        Raw p-values from the test family (e.g. one per Tier 1
        hypothesis). Order doesn't matter — function sorts internally
        and reports back in the input order.
    n_eff : int, keyword-only
        Effective number of independent channels for multiplicity
        correction. Default 4 per the cross-channel-correlation card
        on Stratum 4 data. If ``n_eff > len(p_values)``, the function
        uses ``min(n_eff, len(p_values))`` — never over-corrects
        beyond the test count.
    alpha : float, keyword-only
        Family-wise error rate. Default 0.05.

    Returns
    -------
    dict
        Keys:

        - ``thresholds`` (ndarray): per-test corrected thresholds in
          the original input order (not sorted).
        - ``rejected`` (ndarray of bool): per-test pass / fail at the
          corrected threshold; True means the null is REJECTED (the
          test passed the family-wise correction). Step-down: once a
          test fails, all larger p-values in the family also fail.
        - ``adjusted_p_values`` (ndarray): Holm-adjusted p-values
          (monotone-corrected, capped at 1.0); compare to ``alpha``
          directly for the per-test verdict.
        - ``n_eff_used`` (int): the n_eff actually applied
          ( ``min(n_eff, len(p_values))`` ).

    Raises
    ------
    ValueError
        If ``p_values`` is empty, contains values outside [0, 1],
        ``n_eff < 1``, or ``alpha`` not in (0, 1).

    Notes
    -----
    Holm step-down rule (1-indexed for ease of reference):

    1. Sort p-values smallest -> largest: p_(1) <= p_(2) <= ...
    2. For p_(k) with k = 1..N_eff, threshold = alpha / (N_eff - k + 1).
       For k > N_eff, threshold = alpha (no further penalty).
    3. If p_(k) > threshold_k, then p_(k), p_(k+1), ... all FAIL.

    Adjusted p-values (step-down monotone-corrected):

        p_adj_(k) = max(p_adj_(k-1), (N_eff - k + 1) * p_(k)),
                    capped at 1.

    The thresholds approach and the adjusted-p-values approach give
    identical accept/reject decisions; both are reported.

    Examples
    --------
    >>> import numpy as np
    >>> # Four p-values; smallest just clears alpha/4 = 0.0125
    >>> p = np.array([0.011, 0.04, 0.08, 0.20])
    >>> result = holm_step_down(p, n_eff=4, alpha=0.05)
    >>> result["thresholds"]
    array([0.0125    , 0.01666667, 0.025     , 0.05      ])
    >>> result["rejected"]  # only the smallest clears its threshold
    array([ True, False, False, False])
    """
    p_arr = np.asarray(p_values, dtype=float)

    if len(p_arr) == 0:
        raise ValueError("p_values must be non-empty")
    if np.any(p_arr < 0.0) or np.any(p_arr > 1.0):
        raise ValueError(
            f"p_values must be in [0, 1]; got min={float(p_arr.min())}, "
            f"max={float(p_arr.max())}"
        )
    if n_eff < 1:
        raise ValueError(f"n_eff must be >= 1, got {n_eff}")
    if not 0 < alpha < 1:
        raise ValueError(f"alpha must be in (0, 1), got {alpha}")

    n_input = len(p_arr)
    n_eff_used = min(n_eff, n_input)

    # Sort ascending; track original positions to unsort outputs.
    order = np.argsort(p_arr, kind="mergesort")
    sorted_p = p_arr[order]

    # Per-rank Holm thresholds (0-indexed):
    #   rank 0 (smallest p): alpha / n_eff_used
    #   rank k (k < n_eff_used): alpha / (n_eff_used - k)
    #   rank k (k >= n_eff_used): alpha (no penalty)
    ranked_thresholds = np.empty(n_input)
    for k in range(n_input):
        if k < n_eff_used:
            ranked_thresholds[k] = alpha / (n_eff_used - k)
        else:
            ranked_thresholds[k] = alpha

    # Step-down rejection: pass while sorted_p[k] <= ranked_thresholds[k];
    # at first failure, all subsequent ranks also fail.
    sorted_rejected = np.zeros(n_input, dtype=bool)
    for k in range(n_input):
        if sorted_p[k] <= ranked_thresholds[k]:
            sorted_rejected[k] = True
        else:
            break

    # Adjusted p-values (step-down monotone): p_adj_(k) is max with prev.
    sorted_adjusted = np.empty(n_input)
    prev = 0.0
    for k in range(n_input):
        if k < n_eff_used:
            multiplier = n_eff_used - k
        else:
            multiplier = 1
        candidate = multiplier * sorted_p[k]
        sorted_adjusted[k] = max(prev, candidate)
        prev = sorted_adjusted[k]
    sorted_adjusted = np.minimum(sorted_adjusted, 1.0)

    # Unsort back to original input order.
    thresholds = np.empty(n_input)
    rejected = np.empty(n_input, dtype=bool)
    adjusted_p_values = np.empty(n_input)
    for k, orig_idx in enumerate(order):
        thresholds[orig_idx] = ranked_thresholds[k]
        rejected[orig_idx] = sorted_rejected[k]
        adjusted_p_values[orig_idx] = sorted_adjusted[k]

    return {
        "thresholds": thresholds,
        "rejected": rejected,
        "adjusted_p_values": adjusted_p_values,
        "n_eff_used": int(n_eff_used),
    }
