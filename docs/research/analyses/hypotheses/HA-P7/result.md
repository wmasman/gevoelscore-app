# HA-P7 -- result: recent-crash-density predicts crash risk

*Run 2026-06-15 by `test.py` against the locked pre-registration `hypothesis.md` (revision 2026-06-15-r3, status LOCKED). Random seed: 20260615; stationary-bootstrap + block-permutation at E[L] = 7 days per `methodology/permutation_null_block_length.md`.*

## Headline verdict (pooled LC era x W=14 x primary outcome `is_crash at d`)

**Verdict: NOT-SUPPORTED**

- OR (per +1 crash-day in [d-14, d-1]): **1.130 [0.875, 1.266]** (stationary-bootstrap 95% CI at E[L]=7, B = 10000; point from MLE logistic).
- Block-permutation null p-value (one-sided positive): **p = 0.1682** (B = 10000; n_converged = 9878).
- n eligible days (pooled LC era x W=14): **1249** (positives: 27).

Sec 5.1 three-criterion read:

- (a) OR-CI contains 1: **True** (CI INCLUDES 1)
- (b) monotonicity violated under relative-50% gate: **True**
- (c) at least 2 of {W=7, W=14, W=30} CIs contain 1: **True** (3 of 3 contain 1)

## Train / validate split (W=14 primary)

| era | n | OR [95% block-bootstrap CI] | verdict per Sec 5.1 |
|---|---:|---|---|
| pooled LC | 1249 | 1.130 [0.875, 1.266] | NOT-SUPPORTED |
| train | 408 | 1.121 [0.771, 1.312] | NOT-SUPPORTED |
| validate | 841 | 1.015 [0.567, 1.325] | NOT-SUPPORTED |

Per Sec 5.0 single-cell lock, only **pooled LC x W=14 x primary outcome** is the locked headline; train/validate are reported for transparency. The pooled-LC verdict above is the project-level headline.

## Window sensitivity arms (diagnostic per Sec 5.0 -- not promotable)

| W (days) | era | n | OR [95% block-bootstrap CI] | CI contains 1? |
|---:|---|---:|---|---|
| 7 | pooled | 1256 | 0.971 [0.402, 1.303] | yes |
| 7 | train | 415 | 0.918 [0.000, 1.321] | yes |
| 7 | validate | 841 | 0.956 [0.000, 1.606] | yes |
| 14 | pooled | 1249 | 1.130 [0.875, 1.266] | yes |
| 14 | train | 408 | 1.121 [0.771, 1.312] | yes |
| 14 | validate | 841 | 1.015 [0.567, 1.325] | yes |
| 30 | pooled | 1244 | 0.961 [0.790, 1.062] | yes |
| 30 | train | 403 | 0.886 [0.419, 1.025] | yes |
| 30 | validate | 841 | 1.035 [0.797, 1.258] | yes |

Sec 5.1(c) window-CI disagreement count (>= 2 of 3 with CI containing 1 -> criterion (c) holds): pooled = 3; train = 3; validate = 3.

## Phase-stratified sensitivity arms (diagnostic per Sec 5.0 -- not promotable)

| phase | W | era | n | OR [95% block-bootstrap CI] |
|---|---:|---|---:|---|
| unmedicated | 7 | pooled | 501 | 0.804 [0.000, 1.171] |
| unmedicated | 7 | train | 415 | 0.918 [0.000, 1.326] |
| unmedicated | 7 | validate | 86 | 0.000 [0.000, 0.000] |
| unmedicated | 14 | pooled | 494 | 1.084 [0.802, 1.246] |
| unmedicated | 14 | train | 408 | 1.121 [0.772, 1.315] |
| unmedicated | 14 | validate | 86 | 0.853 [0.000, 1.239] |
| unmedicated | 30 | pooled | 489 | 0.843 [0.559, 0.979] |
| unmedicated | 30 | train | 403 | 0.886 [0.456, 1.021] |
| unmedicated | 30 | validate | 86 | 0.576 [0.000, 0.760] |
| buildup | 7 | pooled | 46 | 0.000 [0.000, 0.216] |
| buildup | 7 | validate | 46 | 0.000 [0.000, 0.214] |
| buildup | 14 | pooled | 46 | 0.000 [0.000, 0.004] |
| buildup | 14 | validate | 46 | 0.000 [0.000, 0.001] |
| buildup | 30 | pooled | 46 | 0.000 [0.000, 0.218] |
| buildup | 30 | validate | 46 | 0.000 [0.000, 0.218] |
| consolidation | 7 | pooled | 622 | 1.471 [0.000, 3.595] |
| consolidation | 7 | validate | 622 | 1.471 [0.000, 3.556] |
| consolidation | 14 | pooled | 622 | 1.009 [0.000, 1.896] |
| consolidation | 14 | validate | 622 | 1.009 [0.000, 1.780] |
| consolidation | 30 | pooled | 622 | 1.275 [0.000, 2.129] |
| consolidation | 30 | validate | 622 | 1.275 [0.000, 2.203] |
| afbouw | 7 | pooled | 74 | 1.421 [0.000, 3.868] |
| afbouw | 7 | validate | 74 | 1.421 [0.000, 3.868] |
| afbouw | 14 | pooled | 74 | 1.271 [0.000, 2.828] |
| afbouw | 14 | validate | 74 | 1.271 [0.000, 2.613] |
| afbouw | 30 | pooled | 74 | 1.033 [0.000, 1.855] |
| afbouw | 30 | validate | 74 | 1.033 [0.000, 1.796] |

Per-phase verdicts are **descriptive only** per Sec 5.0 hard rule; they do not promote to SUPPORTED. Buildup includes the Sec 6 CPAP-buffer exclusion (2024-04-09 to 2024-04-29 dropped from buildup-phase arms).

## Binned tabulation (W=14, pooled LC era) with block-bootstrap CIs

| bin | n | k crashes | rate | 95% block-bootstrap CI |
|---:|---:|---:|---|---|
| 0 | 941 | 18 | 0.0191 | [0.0112, 0.0286] |
| 1 | 19 | 0 | 0.0000 | [0.0000, 0.0000] |
| 2 | 159 | 6 | 0.0377 | [0.0126, 0.0677] |
| 3+ | 130 | 3 | 0.0231 | [0.0000, 0.0480] |

Monotonicity (relative-50% gate per Sec 5.1(b)): **VIOLATED** (bins checked: [0, 1, 2, 3]; violations: bin 0 -> bin 1: rate 0.0191 -> 0.0000 (threshold 0.0096)).
Companion CI-overlap test: [0, 1]: 0.0%; [1, 2]: 0.0%; [2, 3]: 73.8% (dominant).

## Sec 4.5.4 covariate sensitivity (secondary logistic adds `gevoelscore_lagged_mean_14d`)

| era | n | beta_crash_count_14d (OR) [95% CI] | beta_gevoel_lag_mean_14d [95% CI] |
|---|---:|---|---|
| pooled | 1249 | 0.941 [0.621, 1.214] | -1.157 [-2.568, 0.138] |
| train | 408 | 1.074 [0.567, 1.713] | -0.283 [-2.608, 2.437] |
| validate | 841 | 0.787 [0.367, 1.172] | -1.585 [-3.830, 0.348] |

**Disambiguation read** (Sec 4.5.4): if beta_1 attenuates toward 0 while beta_2's CI excludes 0, the Sec 4.5.1 primary signal was a proxy for recent low gevoelscore -- the *recovery-debt* mechanism reading is NOT supported beyond the trivial label-density-tracks-gevoelscore reading. If beta_1 survives, the recovery-debt mechanism reading is supported by information beyond gevoelscore trajectory.

## Secondary outcome `any_crash_in_next_4d` (W=14, diagnostic per Sec 5.2)

| era | n | OR [95% block-bootstrap CI] |
|---|---:|---|
| pooled | 1249 | 1.160 [0.944, 1.308] |
| train | 408 | -- |
| validate | 841 | 1.016 [0.650, 1.304] |

## Same-day Spearman rho(crash_count_14d, gevoelscore at d) -- Sec 3.4 venue

| era | n_full | rho_full | n_no_crash | rho_crash_dropped | abs_delta_rho | Sec 3.4 flag |
|---|---:|---:|---:|---:|---:|---|
| pooled | 1249 | -0.1074 | 1222 | -0.1046 | 0.0027 | ok |
| train | 408 | -0.0807 | 396 | -0.0752 | 0.0054 | ok |
| validate | 841 | -0.1059 | 826 | -0.1058 | 0.0001 | ok |

## Sec 4.5.1 data-driven E[L]* companion

Data-driven E[L]* on pooled-LC `crash_count_14d` series: **11.97 days** (project default = 7).
**Factor-of-2 flag fired**: |E[L]* - 7| / 7 > 0.5. Per the methodology MD Sec 2 operational consequence, FLAG for review before locking the verdict.

## Caveats (per hypothesis.md Sec 8 -- must be acknowledged on every read)

1. **Causal-attribution ambiguity is irreducible**. A positive result is consistent with the recovery-debt mechanism AND with a shared underlying cause (stressful period, infection, intervention transition). The design cannot adjudicate.
2. **Selection bias on conditioning**: the eligibility rule `is_crash[d-1] == False` concentrates the analysis on inter-crash gap days. These differ distributionally from arbitrary days.
3. **Self-reported crash labels** (crash_v2 = `gevoelscore <= 3` for >= 2 consecutive days). Single-rater coding; no physiological ground truth.
4. **`gevoelscore` is the SAME instrument** generating both the predictor (`crash_count_14d`) and the outcome (`is_crash at d`). Any systematic drift or mood-state-dependent reporting affects both.
5. **Protocol disturbs the test**. Operational pacing based on recent-crash awareness conflates 'recent-crash-aware-and-protective' vs 'recent-crash-aware-but-still-crashed'.
6. **Phase dose-modulation** of `gevoelscore` per Session C's small detrend-surviving step at 2026-03-20. The per-phase arms address this; the pooled headline does not apply a Sec 5.B dose-adjustment because the predictor is a count.
7. **Sec 3.4 inapplicable-to-primary by construction** (dropping `is_crash` rows would eliminate every positive case); Sec 3.4 is honored on the descriptive same-day Spearman above.
8. **Per-phase ns are small for buildup + afbouw**; pooled-LC is the headline. Per-phase INCONCLUSIVE is expected, not promoted.

---

*Result emitted by `test.py` on the locked pre-registration. Raw result data (bootstrap CIs, beta arrays, per-phase cells) in `result-data.json` alongside this file. Any post-result modification of the spec creates HA-P7-v2 with this v1 archived.*
