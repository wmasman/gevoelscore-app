"""Shared statistical-inference utilities for HA-numbered hypothesis tests.

This module is **empty pending C.2-C.4** of the Wiggers Tier 1 execution plan
(``C:/Users/Gebruiker/.claude/plans/wiggers-tier1-execution-plan-2026-06-14.md``).

The three functions to land here:

1. ``stationary_bootstrap_ci(...)`` --- stationary bootstrap with E[L] = 7 days
   per ``methodology/permutation_null_block_length.md``. Returns the 95% CI on
   the discrimination / correlation / dose-response statistic. Day-resampling
   layer (within-construction-window resampling), distinct from the event-level
   permutation null in (2). See chained-regime doc Cross-cutting hygiene
   section 4 for the two-resampling-layers distinction.

2. ``block_permutation_pvalue(...)`` --- event-level permutation null at n=29
   crash episodes per chained-regime doc Cross-cutting hygiene section 4.
   Returns the one-sided p-value. Combinatorics-dominated regime
   (C(29, k) is the binding constraint, not block length).

3. ``holm_step_down(p_values, n_eff=4, alpha=0.05)`` --- Holm step-down
   multiplicity correction on N_eff approximately 4 effectively independent
   channels per chained-regime doc Cross-cutting hygiene section 3 and
   ``analyses/garmin_exploration/cards/cross-channel-correlation.md``.
   Returns adjusted p-values + per-test pass / fail at the chosen alpha.

Each function gets a companion test in ``test_inference.py`` (synthetic-data
correctness check before any HA-test imports it). The companion tests gate
correctness; they are not skipped.

When any of these functions land, update this docstring to remove the
'pending' framing and replace with usage examples per function.
"""
