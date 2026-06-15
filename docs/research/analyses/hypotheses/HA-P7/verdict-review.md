# HA-P7 verdict review — post-result factor-of-2 flag review

*Written 2026-06-15 by Claude under reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). The locked pre-registration [`hypothesis.md`](hypothesis.md) (LOCKED 2026-06-15 commit `7f1ecc8` r3) is not modified by this review; the locked verdict in [`result.md`](result.md) is preserved verbatim. This file documents the post-result review of the factor-of-2 flag that the locked test.py emitted, per the operational consequence in [`methodology/permutation_null_block_length.md` §2](../../../methodology/permutation_null_block_length.md).*

## 1. The flag

[`result.md`](result.md) Sec 4.5.1 emitted:

> Data-driven E[L]* on pooled-LC `crash_count_14d` series: **11.97 days** (project default = 7).
> Factor-of-2 flag fired: |E[L]* - 7| / 7 > 0.5. Per the methodology MD Sec 2 operational consequence, FLAG for review before locking the verdict.

Per [`methodology/permutation_null_block_length.md` §2](../../../methodology/permutation_null_block_length.md), this is a procedural halt — the verdict cannot lock until the divergence is reviewed.

## 2. Structural explanation for E[L]* > E[L]

The predictor under test is `crash_count_14d` — the count of `is_crash == True` days in the 14-day window ending the day before the index day. **This is a rolling sum.** A rolling sum at window W has the structural property that day `d` and day `d+1` share `(W-1)/W = 13/14 ~ 93%` of their input days; the lag-1 autocorrelation of a rolling-sum series approaches 1 as the smoothing window expands.

The data-driven block-length estimator ([`test.py:estimate_block_length`](test.py); Politis & White 2004 style) measures the autocorrelation structure to recommend a block length that captures the dependence. On `crash_count_14d`, the rolling-sum structural autocorrelation is dominant, and the estimator recommends E[L]* ~ 12 days — comparable to the W = 14 smoothing window itself.

**This divergence is structural, not a sampling artefact.** Any rolling-sum predictor at W = 14 will yield E[L]* in the same neighbourhood. The locked spec's default E[L] = 7 is from the project-wide [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) anchor, which targets the day-level autocorrelation of *raw* time series in this corpus; rolling-sum predictors structurally exceed it.

The same review will apply to any future HA-family pre-reg whose predictor is a `crash_count_Wd` rolling sum. Worth a methodology MD note for future pre-regs.

## 3. Robustness of the locked verdict to longer E[L]

The locked verdict at E[L] = 7 (from [`result.md`](result.md)) is NOT-SUPPORTED on all three Sec 5.1 criteria:

- (a) OR CI 1.130 [0.875, 1.266] contains 1: **True**
- (b) monotonicity violated under relative-50% gate: **True**
- (c) at least 2 of {W=7, W=14, W=30} CIs contain 1: **True** (3 of 3)
- Block-permutation p (one-sided positive) at E[L] = 7: 0.1682

**The sensitivity addendum [`sensitivity_block_length.py`](sensitivity_block_length.py) re-runs the headline cell at three block lengths** (7, 12, 14) with B = 2000 stationary-bootstrap CIs + B = 2000 block-permutation nulls per cell. Raw output in [`sensitivity_block_length.json`](sensitivity_block_length.json):

| E[L] | OR    | 95% CI            | CI contains 1 | p (one-sided positive) |
|-----:|-------|-------------------|---------------|-----------------------:|
| 7    | 1.130 | [0.866, 1.266]    | YES           | 0.1676                 |
| 12   | 1.130 | [0.902, 1.268]    | YES           | 0.2864                 |
| 14   | 1.130 | [0.897, 1.266]    | YES           | 0.3199                 |

**Reads**:

- **OR point estimate** is invariant to E[L] by construction (MLE logistic does not depend on the bootstrap block length). All three rows confirm 1.130.
- **CI** is essentially flat across E[L] = 7, 12, 14 — the headline CI [0.875, 1.266] in [`result.md`](result.md) (at the locked B = 10,000) is reproduced to ~0.01 precision at B = 2000; at longer E[L] the CI bounds drift by < 0.04 on the lower bound and < 0.01 on the upper bound. **CI contains 1 at all three E[L] values.** The NOT-SUPPORTED bar (a) holds.
- **Permutation p-value increases monotonically** with E[L] (0.17 -> 0.29 -> 0.32). This is the theoretically-predicted direction: longer block lengths preserve more autocorrelation in the null sample, widening the null distribution of the observed beta and making the observed beta less surprising under the null. The null reading **strengthens** at the data-driven E[L]* ~ 12.
- **No criterion (a), (b), (c) flips** — the NOT-SUPPORTED verdict at the locked E[L] = 7 is structurally robust to the factor-of-2 flag.

## 4. Review conclusion

The factor-of-2 flag is **explained by the rolling-sum structure of the predictor** (§2) and **does not invalidate the verdict** (§3). The locked NOT-SUPPORTED verdict at E[L] = 7 holds and is preserved verbatim in [`result.md`](result.md).

**The verdict is cleared to lock.** No modification to [`result.md`](result.md) is required; this review document is the audit trail of the §1 flag's resolution.

## 5. Caveat for future HA-family pre-regs with rolling-sum predictors

The next pre-reg that uses a `crash_count_Wd` (or any rolling-sum predictor at non-trivial W) should anticipate this pattern at the operationalisation-precision interview stage:

- E[L]* will likely exceed E[L] = 7 by a factor related to W.
- The factor-of-2 flag will likely fire at lock-time inference.
- The review will likely follow this same template (structural explanation + robustness sensitivity + verdict-cleared-to-lock).

A short note has been queued for [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) §2 to acknowledge the rolling-sum exception. See [§8.3 follow-ups in `methodology/hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md#83-open-follow-ups-post-v11) for the queue entry.

## 6. Status

**Verdict status**: NOT-SUPPORTED (per [`result.md`](result.md) Sec 5.1; reviewed and cleared at this document).

**Lock status**: Awaiting explicit user acceptance per [`methodology/hypothesis_lock_process.md` §3.8](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc). The lock-commit message must confirm:

1. Power-calc dispatch present in pre-reg §8 (already in locked hypothesis.md §8).
2. Single-cell headline lock per Sec 5.0 (already in locked hypothesis.md §5.0).
3. Register-row pointer to be added at lock in [`personal_hypotheses.md`](../../../personal_hypotheses.md) P7 entry (queued; this is an open follow-up from [`hypothesis_lock_process.md` §8.3](../../../methodology/hypothesis_lock_process.md#83-open-follow-ups-post-v11)).
4. Re-audit completed clean OR compression decision documented per §3.6 (the original lock used option-A compression; this verdict lock inherits the same compression with the §6 follow-up note).

When the user signals lock, the lock commit applies the register-row pointer + the verdict-lock status update.

---

*Review drafted 2026-06-15. Awaiting lock signal.*
