# Permutation null + bootstrap CI block-length policy

*Methodology decision drafted 2026-06-13 per [[feedback_methodology_decisions_documented_reasoning]]. Open until user review.*

## Citation status

This MD currently runs on first-principles reasoning only. The canonical statistical-methodology references in this area (stationary bootstrap, automatic block-length selection, permutation tests under dependence) have **not** been read or verified in our literature folder. Candidate refs are listed in [`_pending_literature_fetch.md`](_pending_literature_fetch.md) as a fetch-and-verify task for a future agent. Until those refs land, the literature row of the four-input reasoning is honestly downgraded to "deferred". The methodological reasoning stands on its own and does not depend on any specific paper.

---

## Aim

Decide the **block-length policy** for resampling-based inference (permutation null tests + bootstrap CIs) on Wiggers pre-reg discrimination statistics across our daily-resolution physiological + subjective signals.

This is the core methodological knob for any pre-reg whose verdict depends on a permutation p-value or bootstrap CI. The handover left it as "~7 days from ACF decay" with two alternatives (lock globally vs per-hypothesis derive). This MD does the homework from first principles.

## Decision (proposed; pending user review)

**Use the stationary bootstrap with expected block length E[L] = 7 days as the project-wide default.** Block lengths drawn from a geometric distribution with mean E[L]. Apply the same E[L] policy to permutation null tests (permute crash/null labels in blocks drawn from the same distribution).

**Per-hypothesis override allowed only when**: (i) the metric's empirical autocorrelation (computed over Stratum 4 days, see [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)) crosses zero at a lag substantially different from 7 (e.g. < 3 or > 14 days at lag |corr| < 0.1), AND (ii) the override is pre-registered in the hypothesis file before any test run, AND (iii) the override is justified in the hypothesis file with a 1-paragraph ACF readout.

**Run a data-driven block-length estimator as a confirmatory companion**, not as the primary policy. Report its estimated E[L]* in the result file. If E[L]* differs from 7 by more than a factor of 2, flag for review before locking the verdict.

**Do not use fixed-block (deterministic block length) bootstrap as primary**; reserve it for sensitivity comparison if needed.

## Alternatives considered

| label | proposal | verdict | reason |
|---|---|---|---|
| **(a) original** | Lock fixed-block bootstrap with L = 7 days globally | rejected as primary | Fixed-block resampling assumes stationarity, which the LC era may violate (gradual adaptation, treatment-induced drift). A fixed boundary at block edges introduces an edge bias that the random-length stationary bootstrap removes by construction. |
| **(b) original** | Derive per-hypothesis from each metric's ACF | rejected as default | Researcher degrees of freedom: per-hypothesis tuning is a soft form of p-hacking unless pre-registered with a strict rule. Also breaks cross-hypothesis comparability. |
| **(c) CHOSEN** | Stationary bootstrap (random block lengths, geometric mean 7) globally + data-driven confirmation + strict override rule | proposed | Stationary bootstrap is robust to mild non-stationarity by construction (random lengths remove fixed-edge bias). The data-driven companion gives an objective check on our 7-day default. The override rule (gated on ACF-derived threshold + pre-registration) closes the p-hacking door. |
| **(d)** | Variance-estimation block length L ∝ n^(1/3) | rejected as default | At our n ≈ 1700 LC days, this gives L ≈ 12 days. Plausible but derived for variance estimation rather than hypothesis testing under dependence. |
| **(e)** | Subsampling | rejected for primary | Wider applicability than bootstrap but loses efficiency relative to bootstrap when bootstrap regularity conditions hold. Reserve for cases where bootstrap consistency is in doubt for a specific test statistic. |

## Four-input reasoning

### 1. Best-practices standards

- **Block bootstrap is the orthodoxy for inference on autocorrelated time series.** The question is which variant (fixed-block / stationary / circular / tapered), not whether to use blocks. Plain (non-block) bootstrap is invalid for dependent data.
- **Stationary bootstrap with random block lengths** is preferred over fixed-block bootstrap when the time series may have mild non-stationarity, because:
  - The resampled series is itself stationary by construction, which simplifies asymptotic theory.
  - Random block lengths remove the bias that fixed-block introduces at arbitrary block boundaries.
  - The geometric block-length distribution interpolates smoothly across different lag dependencies, which matters when the true ACF length is unknown.
  These properties matter for our setting: LC-era physiological data has gradual drift, uncertain ACF length across metrics, and varying stationarity by signal.
- **Automatic block-length selection is a solved problem** for resampling under dependence: data-driven procedures based on the empirical ACF of the test statistic give an estimated optimal block length that minimises MSE. Modern empirical practice runs such a procedure as a check on any chosen block length, even when a domain default is also used.
- **Permutation null tests under dependence require block-permutation** (permute blocks of the data, not individual observations) to preserve within-block dependence. The same block-length policy that informs the bootstrap CI applies to the permutation null.

### 2. Literature where it materially supports the choice

**Deferred** (see Citation status above). Candidate references queued in [`_pending_literature_fetch.md`](_pending_literature_fetch.md): the original stationary-bootstrap paper, the automatic block-length-selection procedure with its corrected formula, the canonical n^(1/k) block-length-rule papers, and asymptotic-validity results for permutation tests under dependence.

### 3. Tradeoffs

| dimension | fixed-block L=7 (a) | per-hypothesis tuning (b) | stationary E[L]=7 + data-driven confirm + override rule (c, CHOSEN) |
|---|---|---|---|
| Researcher degrees of freedom | low | high (unless pre-reg-gated) | low (override rule binds it) |
| Cross-hypothesis comparability | high | low | high |
| Robustness to non-stationarity | poor (fixed blocks bias at edges) | depends | strong (random lengths) |
| Audit-defensibility | medium (one knob, not derived) | low (per-hypothesis knobs) | high (one knob, derived from confirmation step + ACF) |
| Implementation complexity | low | high (rerun per-hypothesis) | medium (need data-driven estimator) |
| Sensitivity to E[L] choice | high | n/a | low (random-length resampling is less sensitive to mean length than fixed-block is to L) |
| Aligned with [[feedback_caveats_vs_apriori]] | yes (no a-priori claim baked in) | no (per-hypothesis pre-reg risks tuning) | yes (override is gated + must be pre-reg'd) |

The weighting we apply: cross-hypothesis comparability and researcher-degrees-of-freedom control dominate. Both push toward a global default with a strictly gated override path. Robustness-to-non-stationarity is a tiebreaker that picks stationary over fixed-block.

### 4. Our research limitations + objectives

- **n ≈ 1700 LC days, 29 crash episodes, 14 train / 15 validate.** Sufficient for asymptotic bootstrap consistency at the metric level; tight for permutation null tests at the crash-event level, where the relevant n is 29.
- **Multi-metric corpus**: ≈ 7 primary primitives (H02b, HA11, HA06b, HA07c, HA07d, HA10, HA01-axes), with cross-channel ρ up to 0.92 ([cross-channel-correlation.md](../analyses/garmin_exploration/cards/cross-channel-correlation.md)). Effective independent-channel count ≈ 3-4. The Bonferroni multiplicity context is set by effective N ≈ 4, giving α ≈ 0.0125; only H02d/H02b clears at p = 0.011.
- **Single-subject** — no second source of replication except across-time (see [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)).
- **ACF varies by metric**: RHR has ~5-10 day decay; sleep-stress shorter; activity-derived metrics show weekly cycles. The single-default policy bets that the average is close enough; the confirmation step is the empirical check on that bet.
- **Why E[L] = 7 and not 5 or 12**: empirical ACF observations for daily physiological signals typically decay within a week; n^(1/k) family rules give a defensible range from ~4 (for k=5, distribution estimation) to ~12 (for k=3, variance estimation) at our n; 7 sits in the middle of this range and matches the dominant weekly cycle in activity-derived metrics. The data-driven confirmation step is the safeguard against this default being wrong for a specific metric.
- **Objective**: descriptive characterisation under the descriptive-before-inference principle. We are not chasing the most powerful test; we are chasing the most defensible test.

## Operational consequences

1. Add to [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) § Cross-cutting statistical hygiene: project-wide bootstrap default is stationary bootstrap, E[L] = 7 days. Pre-reg files cite this MD.
2. Result template for any new pre-reg includes:
   - Discrimination point estimate
   - Stationary bootstrap 95% CI at E[L] = 7
   - Permutation null p-value at E[L] = 7
   - Data-driven estimated E[L]* for the same metric
   - Flag if |E[L]* − 7| / 7 > 0.5 (factor-of-2 deviation)
3. Already-locked verdicts (HA01b, HA02c, HA08, HA11, H05) keep their original block treatment for their original verdict. Re-running them under stationary-E[L]=7 is a queued sensitivity exercise (Q-entry in [`queued_work.md`](queued_work.md)), not a re-lock.
4. Effective-N-of-channels considerations from [cross-channel-correlation.md](../analyses/garmin_exploration/cards/cross-channel-correlation.md) inform the **multiplicity correction** layer, which is separate from block-length policy. Multiplicity correction sits in [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md), not here.
5. The Personal register ([`personal_hypotheses.md`](../personal_hypotheses.md)) is descriptive only and does not run permutation null tests. This MD does not bind P-entries.

## Open follow-ups

- **Data-driven block-length estimator implementation**: pure-Python implementation needed. Off-the-shelf options exist in standard statistical packages; we will document the source if we adopt one, or implement from the formula if not. Decision deferred to first pre-reg that needs it.
- **Tapered block bootstrap** could reduce bias further at small n. Not adopted because the bias reduction is marginal for our use case and adds complexity. Revisit if the data-driven confirmation step flags a problem.
- **Long-memory check**: standard bootstrap consistency assumes short-range dependence. If any metric shows long-memory (via R/S analysis or DFA), the bootstrap consistency argument weakens. Not currently a concern but flag for any new physiological metric added to the corpus.
- **Computation cost**: B = 10,000 bootstrap resamples × 7 primitives × 29 crash events per primitive. Should be sub-minute on a modern laptop. If it isn't, profile before approximating.

## Cross-references

- Decision discipline: [[feedback_methodology_decisions_documented_reasoning]], [[feedback_caveats_vs_apriori]], [[feedback_descriptive_before_inference]]
- Companion methodology MDs: [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md), [`train_validate_split_fate.md`](train_validate_split_fate.md)
- Evidence informing this decision: [primary-verdict-statistics.md](../analyses/garmin_exploration/cards/primary-verdict-statistics.md) (n per era), [cross-channel-correlation.md](../analyses/garmin_exploration/cards/cross-channel-correlation.md) (effective N of channels)
- Affected docs: [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) (pre-reg-file constraint cross-reference), [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) (statistical hygiene section)
- Citation fetch task: [`_pending_literature_fetch.md`](_pending_literature_fetch.md)
