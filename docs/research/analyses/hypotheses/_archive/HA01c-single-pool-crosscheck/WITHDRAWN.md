# WITHDRAWN — HA01c single-pool cross-check (drafted 2026-07-03, withdrawn 2026-07-04)

This pre-registration + test.py were drafted to give HA01c a single-pool
verdict under the MD2+MD3 framework. They are **withdrawn, not run**, for
two independent reasons surfaced by the two cold reviews
([`../../../reviews/hypothesis-HA01c-single-pool-crosscheck-2026-07-03.md`](../../../reviews/hypothesis-HA01c-single-pool-crosscheck-2026-07-03.md),
[`../../../reviews/methodology-HA01c-single-pool-crosscheck-implementation-2026-07-03.md`](../../../reviews/methodology-HA01c-single-pool-crosscheck-implementation-2026-07-03.md)):

1. **Redundant.** The single-pool HA01c verdict already exists, committed:
   [`../../descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../../descriptive/operationalisation_support/single_pool_reanchor/findings.md)
   (commit `958bfe2`, 2026-06-30) — disc **+19.6 pp**, permutation
   **p = 0.0290** (E[L]=7), verdict **SUPPORTED**, CONVERGE both eras.
   Load-bearing stays WITHHELD pending the v2 threshold-monotonicity
   diagnostic. The original scoping premise ("HA01c has no single-pool
   verdict") was wrong: it read the 7-signal scorecard (which carries
   HA01b, not HA01c) instead of the R14 re-anchor (12 HAs, incl. HA01c).

2. **Method-divergent.** The drafted test built a *block-bootstrap
   permutation null* (blocks applied to the p-value). The project's
   established framework ([`../../_utils/inference.py`](../../_utils/inference.py),
   two-resampling-layers rule) uses an *event-level* permutation for the
   p-value, and reserves the E[L]=7 block length for the *stationary
   bootstrap CI only*. So the "characterize E[L]* to move the marginal
   p=0.029" motivation was mistaken: E[L] governs the CI width, not the
   permutation p that drives the verdict.

**One real open item remains (low-stakes, CI-only):** R14 findings.md
(§ Limitations) notes the data-driven E[L]* for the `effective_exertion`
channel was never characterised on Stratum 4. If pursued, use the shared
`compute_data_driven_block_length` in `inference.py` on that channel's
daily trigger series — it refines HA01c's (already very wide) bootstrap
CI, not the verdict. Do NOT re-run this crosscheck to get it.

The `pre-registration.md` + `test.py` here are preserved verbatim as the
audit trail. See [[reference_single_pool_verdicts_live_in_r14_reanchor]].
