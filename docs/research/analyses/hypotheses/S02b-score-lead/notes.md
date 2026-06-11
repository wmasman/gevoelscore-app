# S02b — Score-lead lagged correlation: notes

**Status: REFUTED on the pre-registered bar (criterion c — lag does
not improve over same-day). The rolling-curve T1 lead/lag pattern
from [S02](../S02-score-trajectory/notes.md) does NOT survive
transition to daily-resolution inference with autocorrelation
correction.**

Spec at [hypothesis.md](hypothesis.md). Script at
[compute_lagged.py](compute_lagged.py). CSV at
[lagged_correlation_results.csv](lagged_correlation_results.csv).
Plot at [lagged_correlation_plot.png](lagged_correlation_plot.png).
Execution log at [execution-log.txt](execution-log.txt).
Run 2026-06-07 (same day as the S02 finding it tests).

## Headline

**ρ_lagged primary** (score(t) × avg-stress(t+149d)) = **+0.099,
95% CI [+0.035, +0.203], n=1213, ~14 effective blocks.**

Reads against the locked SUPPORTED bar:

| Criterion | Requirement | Observed | Result |
|---|---|---|---|
| (a) magnitude | `|ρ_lag| ≥ 0.20` | 0.099 | **FAIL** |
| (b) CI excludes 0 | yes | [+0.035, +0.203] | PASS |
| (c) lag improves over same-day | `|ρ_lag| − |ρ_same-day_matched| ≥ 0.10` | +0.099 − +0.097 = +0.002 | **FAIL** |
| (d) expected sign | ρ_lag < 0 (high score → low stress later) | +0.099 | **FAIL** |

**Three of four criteria FAIL.** Verdict: **REFUTED** on criterion
(c) — the lag does not improve over same-day, by the largest margin
of any criterion.

## Pre-committed bar — full reading

Each criterion's number:

- **(a) magnitude.** The lagged ρ is **0.099**, just under half the
  Cohen-moderate bar of 0.20. The effect, if real, is small.
- **(b) CI excludes 0.** The 95% block-bootstrap CI is
  **[+0.035, +0.203]**. It does exclude 0, barely (lower edge at
  +0.035). With 14 effective independent blocks this is meaningful
  — a small effect is statistically detectable — but the upper edge
  reaches +0.203 which means the most-optimistic estimate is barely
  above the (a) bar. (b) being the only PASS in isolation is not
  enough to support the lag hypothesis.
- **(c) lag improves over same-day.** The matched-window same-day ρ
  is **−0.097** (recomputed on the exact 1213-pair window used for
  the lagged test, so the comparison is apples-to-apples). The
  same-day and lagged ρ have **the same absolute magnitude (~0.10)
  but opposite signs**: same-day is in the expected negative
  direction; lagged is positive. The delta `|ρ_lag| − |ρ_sd|` is
  **+0.002** — essentially zero. The lag does not add explanatory
  power over the same-day relationship.
- **(d) expected sign.** ρ_lagged is **positive** (+0.099); the
  pre-committed expected sign for "score leads Garmin" with avg
  stress (worsen-direction) was negative (high score now → low
  stress 149 days later). The actual sign is opposite — at +149d,
  high score today predicts slightly MORE stress 149 days later.
  This is small enough to be sampling noise within the ±0.10 band,
  but it is not the expected sign.

**Verdict logic.** SUPPORTED requires all four. Three FAIL, so
SUPPORTED is out. REFUTED has three explicit conditions; the
matched here is **"lag does not meaningfully improve over same-day"**
(delta = +0.002, far below the 0.05 ceiling for that REFUTED path).
Criterion (d)'s wrong sign at this magnitude is not strong enough
to trigger the "inverse-direction significant" REFUTED path (which
requires |ρ| ≥ 0.20 AND CI excluding 0 — neither here).

## Q2 — Lag vs same-day on the same window

The lagged and same-day correlations have **near-identical magnitude
but opposite signs**:

- Same-day ρ on the matched window: **−0.097** (n=1208, after
  pairwise dropping)
- Lagged ρ at +149d: **+0.099** (n=1213)

This is the headline mechanical finding. At the day-to-day timescale,
the score and avg-stress relationship is small in either direction
and sign-flips as the lag is shifted. **No daily-resolution version
of "score leads Garmin by ~5 months" is detectable** in this user's
data. Whatever produced S02's rolling-curve T1 turnaround-date gap
of 149 days lives in the 90-day-smoothed signal, not in the
day-by-day pairs.

This is itself a methodological finding: **rolling-curve
turnaround-date mismatches do NOT imply daily-resolution lead/lag
signals.** Future reports of T1 in the project should cite this
constraint — the lead pattern is visible at trajectory scale but
not at daily resolution.

## Q3 — Secondary (max-spike +100d)

- ρ_lagged max-spike at +100d: **−0.025, 95% CI [−0.090, +0.033]**.
- ρ_same-day matched: **+0.022** (n=1260).
- Delta: |−0.025| − |+0.022| = +0.003.

The trough-side channel is null in both lag conditions, both
magnitudes < 0.03. No verdict (max-spike is secondary, per §3.6 of
the spec) but the direction of the finding is unambiguous: nothing
detectable at daily resolution for max-spike either. The
"100-day trough-side lead" finding from S02's T1 is also a
rolling-curve-only pattern.

## Q4 — Effective sample size

The pair-window shrinks by 149 days at the peak-side lag (avg
stress) and 100 days at the trough-side lag (max spike):

| condition | n_pairs | n_eff_blocks |
|---|---:|---:|
| avg_stress same-day (full window) | 1359 | 16 |
| avg_stress +149d (lagged window) | 1213 | 14 |
| max_spike same-day (full window) | 1364 | 16 |
| max_spike +100d (lagged window) | 1267 | 15 |

Loss of effective power is small (~1-2 blocks). The "INCONCLUSIVE"
verdict the spec's caveat anticipated is not the outcome here —
the bar is decisively REFUTED on criterion (c). Power was sufficient
to reject; we cannot blame underpowering.

## Q5 — Connection to Wiggers H1

[Wiggers H1](../../wiggers_progress_2026-06-07.md) asks: "Do wearable
signals lead the felt crash?" The Wiggers framing is **wearables
lead score**. S02 found the empirically-OPPOSITE direction (score
leads wearables in rolling-curve turnaround dates), and S02b tested
that empirical direction directly at daily resolution.

**S02b refutes the score-leads-wearables direction at daily
resolution.** This does NOT mean wearables-lead-score (the Wiggers
direction) is supported — S02b did not test that direction. Both
directions remain consistent with "no daily-resolution lead/lag
signal in either direction at all," which is what S02b's secondary
result and the magnitude of all four ρ values (none above |0.10|)
suggests.

**Updating the Wiggers H1 row in
[wiggers_progress_2026-06-07.md](../../wiggers_progress_2026-06-07.md)**:
the H1 status was PARTIAL with note "The S02b lead/lag follow-up is
queued conditional on S02." After S02b: the project's first direct
cross-correlation lag test is **REFUTED at daily resolution in the
empirically-observed direction**. The Wiggers-direction itself
remains untested but the magnitude of all observed lagged ρ values
(|0.025| - |0.099|) suggests that even if a Wiggers-direction test
were run with proper pre-registration, the daily-resolution signal
would likely be small.

**Recommendation for the Wiggers map update**: change H1 status
to "PARTIAL → daily-resolution lead/lag absent in
empirically-observed direction (S02b); Wiggers-direction not
directly tested." The "implicit cross-correlation" interpretation
of the lead-up window tests still applies, but the *direct*
cross-correlation test was run and refuted in one direction.

## What this means for the project

- **S02's T1 trigger result must be re-read with this constraint.**
  S02b is the locked confirmation test for T1; T1 fired on rolling
  curves but the daily-resolution verification refutes. The
  rolling-curve T1 finding remains TRUE as a description of S02's
  turnaround dates, but the CAUSAL/PREDICTIVE interpretation
  ("score leads Garmin therefore the score channel is informative
  ahead of biometric improvement") is NOT supported.
- **S02's rolling-curve T1 paragraph in
  [S02 notes.md](../S02-score-trajectory/notes.md) should be
  cross-referenced to S02b** so future readers don't take T1 as
  evidence of daily-resolution lead/lag.
- **STOCKTAKE.md and synthesis.md** should reflect this. The
  score-leads-Garmin story is a TRAJECTORY-LEVEL pattern only, not
  a daily-resolution one.
- **S02c remains live** (the May 2026 channel divergence). That
  trigger is independent of T1 and S02b does not address it.

## Methodology notes

- **Locked lag values were NOT free-scanned.** The 149d and 100d
  came from S02's algorithm before S02b ran. No grid search over
  lag values. This is the pre-registration discipline that makes
  the REFUTED verdict honest — we did not search for a lag where
  ρ might be larger.
- **Same-day ρ recomputed on matched window** (n=1208 for
  avg_stress, n=1260 for max_spike, slightly less than S02's full
  1359/1364 because the matched window subsets to dates where the
  lagged pair also exists). This is the apples-to-apples comparison
  the spec required for criterion (c). Without this re-computation,
  comparing |ρ_lagged on 1213 pairs| vs |ρ_same-day on 1359 pairs|
  would have been comparing values on different sample windows.
- **Block-bootstrap CI scheme is identical to S02 §3.8.** 90-day
  blocks, 10 000 iter, seeds offset per (channel, lag) combination
  so the four CIs are based on independent bootstrap samples.
- **OLS line on the scatter plot is a visual aid only**, not
  verdict-bearing. The pre-committed test is rank-based (Spearman);
  Pearson-style OLS is shown just so the reader can see whether
  the scatter has a visible upward / downward / flat tilt.
- **The +0.099 vs −0.097 sign-flip across lags is unexpected** and
  was not pre-registered. Documented here for the audit trail; not
  pursued. A follow-up that tests "is there a ~5-month cyclic
  pattern in score-vs-stress?" would need its own pre-registration
  with new lag candidates and its own bar — not S02b-revised.

## Caveats

- **REFUTED means "the locked bar is not met."** It does NOT mean
  "no relationship exists." Both criteria (a) and (c) failed, and
  (a) requires |ρ| ≥ 0.20 which is a Cohen-moderate bar; smaller
  but real lagged relationships are not excluded. They are, however,
  excluded as the basis for the T1 story.
- **The score is ordinal under self-report with brainfog.**
  Day-to-day measurement noise on the score side is non-trivial;
  small lagged-ρ values may be partly noise-attenuated.
- **The +149d / +100d lags are anchor-week-quantum** in S02's
  algorithm. Sensitivity around ±7 days was NOT tested in S02b
  (would be lag-grid inflation). If a follow-up wants to test
  lag sensitivity, that's a new pre-registration.
- **Bootstrap CIs at ~14 blocks are wide and asymmetric.** The
  primary lagged CI [+0.035, +0.203] is skewed toward the upper
  edge (mean 0.099, range 0.168 with 0.064 below mean and 0.104
  above). The bootstrap distribution is somewhat right-skewed; this
  is normal for small-sample rank correlations and doesn't change
  the verdict.

## What this enables

- **A cleaner cross-reference in [S02 notes.md](../S02-score-trajectory/notes.md)**
  for the T1 finding: the trajectory-level pattern stands as a
  trajectory finding; the daily-resolution version is refuted.
- **A first empirical data point for Wiggers H1** — even though
  S02b tested the opposite-of-Wiggers direction.
- **A locked methodological lesson**: rolling-curve
  turnaround-date mismatches CAN appear without daily-resolution
  lead/lag signal. Future trajectory comparisons (S03+?) should
  cite this constraint before claiming daily-resolution
  implications.

## What this does NOT do

- Does not test the Wiggers-direction (wearables-lead-score)
  hypothesis. That remains a separate pre-registration.
- Does not test other lag values. The two locked candidates were
  refuted; a grid search would be free-parameter inflation.
- Does not address the May 2026 perturbation (that is S02c).
- Does not refute the trajectory-level T1 finding from S02 — the
  turnaround dates still differ by 149d and 100d. S02b only refutes
  the daily-resolution interpretation of that pattern.
- Does not establish causation in either direction.

---

*S02b executed 2026-06-07. Spec at [hypothesis.md](hypothesis.md);
pre-committed bar locked before execution; REFUTED outcome reported
faithfully against that bar without drift. Sibling [S02c](../S02c-may2026-divergence/)
addresses S02's T2 trigger separately.*
