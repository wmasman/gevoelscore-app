# S02b — Score-lead lagged correlation: pre-registered spec

**Pre-registration written 2026-06-07, before `compute_lagged.py` runs
against any data. Locked. Any subsequent change AFTER data inspection
creates `S02b-revised/`; this spec is not edited in place.**

**Status**: pending. **Confirmation test** for S02's T1 finding
(score-leads-Garmin pendulum). Pre-registered support/refute bar
(unlike S02's descriptive piece). Sibling to
[S02c-may2026-divergence](../S02c-may2026-divergence/) addressing
S02's T2 trigger.

---

## 1. Purpose

[S02 §7.2](../S02-score-trajectory/notes.md) found that the score's
algorithmically-picked peak (2023-01-27) and trough (2025-01-10)
occur **before** the corresponding Garmin pendulum extrema:
- vs avg stress: score peak leads by **149 days**
- vs max-spike duration: score trough leads by **100 days**

This was T1 firing on rolling 90-day trajectories. S02b tests whether
**the same lead/lag pattern is statistically supported at daily
resolution with proper autocorrelation handling** — using
pre-committed lag values derived from S02's algorithm rather than
free-scanned from this data.

## 2. Scope

In scope:
- Same-window same-channel daily Spearman ρ between score(t) and
  metric(t + lag) for **pre-committed lag values only** (no
  free-scanned lag search).
- Two channels: avg stress (primary), max-spike minutes (secondary).
- Block-bootstrap CI per S02's §3.8 discipline (90-day blocks,
  10 000 iter).
- Comparison against same-day ρ from S02's §3.8 to test "lag
  improves over same-day."

Out of scope (locked):
- No free-scanned lag search across [-N, +N] days. Lag values are
  fixed at S02's algorithmically-discovered offsets.
- No tests on smoothed/rolling values. Daily raw values only.
- No causation claim. A lagged correlation does not establish
  causation even when supported.
- No mechanism attribution. We measure the pattern, not the cause.

## 3. Methodology — locked

### 3.1 Lag values — pre-committed from S02's §7.1 algorithm

The lag values are **NOT free parameters** chosen post-hoc. They are
outputs of S02's pre-registered algorithm:
- `lag_avg_stress_primary = +149 days` — score peak (2023-01-27)
  leads avg-stress peak (2023-06-25) by 149 d.
- `lag_max_spike_secondary = +100 days` — score trough (2025-01-10)
  leads max-spike trough (2025-04-20) by 100 d.

Reading: `+lag` means "score leads metric by lag days" — at lag = L,
we correlate `score(t)` with `metric(t + L)`. Positive ρ means "high
score now predicts high metric L days later"; for worsen-direction
metrics (stress, max-spike) the expected sign of a score-leads-Garmin
relationship is **negative** (high score now → low stress L days
later, indicating that subjective wellbeing improves before
sympathetic activation drops).

### 3.2 Series construction

- **Score**: daily 1–6 integer from `day_entries.csv`. Same source as
  S02 §3.1.
- **Avg stress**: UDS `allDayStress.aggregatorList[type=TOTAL].
  averageStressLevel`, raw daily, same source as S01 / S02 §3.8.
- **Max spike**: `daily_max_spike.csv` from H02b. Raw daily values
  where `valid=1`.

### 3.3 Lagged pair construction

For each (channel, lag) pair, build aligned series:
- `pair_dates = {d : d ∈ score AND (d + lag) ∈ metric AND d ≥
  2022-09-03 AND (d + lag) ≤ 2026-06-05}`
- `xs = [score(d) for d in pair_dates]`
- `ys = [metric(d + lag) for d in pair_dates]`

Pairwise drop missing on either side. Report n_pairs and
n_excluded.

### 3.4 Statistic + CI

- **Statistic**: Spearman ρ (same as S02 §3.8 — ordinal score
  respected; Pearson would assume interval).
- **Confidence interval**: 95%, moving-block bootstrap, **90-day
  blocks, 10 000 iter, seed = 42 + channel_offset** (same scheme as
  S02 §3.8).
- **Same-day comparison ρ**: re-compute same-day ρ on the same
  pair-window (subset of S02's §3.8 ρ for an apples-to-apples
  same-pair-window comparison).

### 3.5 Pre-committed support/refute bar

Pre-committed before any computation runs. Locked. Two channels;
verdict applies to primary (avg stress) only. Secondary (max-spike)
reported but not verdict-bearing — same Holm-Bonferroni rationale as
S02 §3.8.

**SUPPORTED** (primary) requires BOTH:
- (a) **Magnitude**: `|ρ_lagged_primary| ≥ 0.20` (Cohen-moderate for
  rank correlation; locked threshold matches the S02 §3.8 "co-vary
  detectably" boundary).
- (b) **CI excludes 0**: 95% CI of ρ_lagged primary does not span 0.
- (c) **Lag matters**: `|ρ_lagged_primary| > |ρ_same-day_primary|`
  by ≥ 0.10 (showing the score-leads-Garmin hypothesis is a better
  fit than the same-day hypothesis on the same pair-window).
- (d) **Expected sign**: `ρ_lagged_primary < 0` (score leading means
  high-score predicts low-stress-future for a worsen-direction
  metric).

**REFUTED** (primary) holds if EITHER:
- `|ρ_lagged_primary| < 0.10` AND CI inside ±0.15 — no detectable
  lagged co-variation, OR
- `|ρ_lagged_primary| ≤ |ρ_same-day_primary| + 0.05` — lag does not
  meaningfully improve over same-day (the rolling-curve T1 finding
  doesn't survive at daily resolution), OR
- `ρ_lagged_primary > 0` with CI excluding 0 AND `|ρ| ≥ 0.20` —
  significant in inverse direction; would suggest score-leads-Garmin
  in the WRONG direction (high score predicts MORE stress) which is
  surprising and queues S02c-revised reframe.

**INCONCLUSIVE** otherwise (between the bars).

The bar is **set high deliberately**. S02's rolling-curve T1 was
visible because 90-day smoothing collapses noise; at daily resolution
with autocorrelation-corrected inference, the bar must be high
enough to require a real signal, not smoothing-revealed structure.
If the strict bar refutes, that itself is a finding: **the
rolling-curve T1 lead/lag pattern does not survive transition to
daily-resolution inference**, which would constrain how confidently
the lead/lag story is read in [STOCKTAKE.md](../../STOCKTAKE.md) and
[wiggers_progress_2026-06-07.md](../../wiggers_progress_2026-06-07.md).

### 3.6 Companion tests on the secondary channel

Max-spike at +100d lag is reported with the same metrics but no
verdict applies. The max-spike result is informative for **whether
the trough-side lead is the same shape as the peak-side lead** — if
avg-stress at +149d supports and max-spike at +100d also looks
similar, that's two independent evidence points for the
score-leads-Garmin pattern. If they disagree, the pattern is
single-channel.

## 4. Locked questions notes.md must answer

Each gets a paragraph with the specific number, not a hand-wave.

1. **Does ρ_lagged primary (score × avg-stress at +149d) meet the
   pre-committed SUPPORTED bar?** Report all four criteria (a/b/c/d)
   with their numbers and pass/fail per criterion.
2. **Is ρ_lagged > ρ_same-day on the same pair-window?** Quantify
   the magnitude difference and direction.
3. **Does the secondary (max-spike at +100d) tell the same story?**
   Report ρ + CI + same-day comparison.
4. **What is the effective sample size at +149d lag?** The window
   shrinks by 149 days at the peak-side lag; report n_pairs and
   n_effective_blocks. If the secondary is dramatically more
   powered than the primary, note that.
5. **Connection to Wiggers H1.** This is the project's first direct
   cross-correlation lag test of "do wearables lead self-report"
   per [wiggers_progress_2026-06-07.md](../../wiggers_progress_2026-06-07.md).
   Note Wiggers' framing is the OPPOSITE direction (wearables lead
   score); S02b tests the empirically-observed direction
   (score-leads-wearables). State explicitly which direction was
   supported / refuted for the Wiggers map.

## 5. Outputs

### 5.1 `lagged_correlation_results.csv`

One row per (channel, lag-condition) combination, where lag-condition
∈ {same-day, lagged}:

- `channel` (`avg_stress` | `max_spike_minutes`)
- `role` (`primary` | `secondary`)
- `lag_days` (0 | 149 | 100)
- `n_pairs`
- `n_excluded_metric` (days dropped from metric side)
- `n_effective_blocks`
- `spearman_rho`
- `ci95_lo`, `ci95_hi`
- `criterion_a_mag` (pass/fail for |ρ| ≥ 0.20 — primary only)
- `criterion_b_ci_excl_zero` (pass/fail — primary only)
- `criterion_c_lag_better` (pass/fail for |ρ_lagged| > |ρ_same-day|
  + 0.10 — primary only, applies to lagged row)
- `criterion_d_expected_sign` (pass/fail for ρ < 0 — primary only)
- `verdict` (`SUPPORTED` | `REFUTED` | `INCONCLUSIVE` for primary
  lagged row; blank for other rows)

### 5.2 `lagged_correlation_plot.png`

Two-panel figure:
- **Panel A** — score(t) vs avg-stress(t + 149d): scatter of paired
  values (jittered to resolve overlap on the discrete 1–6 score
  scale), with regression line. Title shows ρ + CI + verdict.
- **Panel B** — score(t) vs max-spike(t + 100d): same as A but for
  the secondary.

Both panels share style. Same-day ρ printed on each panel as a
comparison reference number.

### 5.3 `notes.md`

Sections per established convention:
- Status statement at top with verdict.
- Pre-committed bar reading: each criterion's pass/fail with
  numbers (§4 question 1).
- Lag vs same-day comparison (§4 question 2).
- Secondary channel (§4 question 3).
- Power note (§4 question 4).
- Wiggers H1 connection (§4 question 5).
- Methodology notes.
- Caveats.
- "What this means for the project" — explicit statement of how
  the verdict updates STOCKTAKE / wiggers_progress and S02b's
  status in registry §4b.

## 6. Caveats locked into notes.md

- **The lag values were derived from S02, not S02b.** That is the
  pre-registration discipline at work: S02 found the lag
  algorithmically; S02b tests it on independent inference machinery
  (daily resolution + block bootstrap). It is NOT independent data
  — both S02 and S02b use the same full corpus. The protection
  against motivated reasoning is the pre-committed bar and the
  refusal to free-scan additional lags.
- **Block bootstrap at ~14-15 effective blocks** (the pair-window
  shrinks by 149 days at the peak-side lag, so n_pairs drops from
  S02 §3.8's 1.359 to roughly 1.210, ~13-14 blocks). The CI will be
  wide. The "INCONCLUSIVE" outcome row in §3.5 exists for exactly
  this reason.
- **Discrete 1–6 score against continuous Garmin metrics.** Spearman
  handles this correctly (ranks both); the scatter plot shows ties
  as horizontal bands which is expected.
- **No reverse-direction test.** S02b tests only the
  score-leads-Garmin direction discovered in S02. The
  Garmin-leads-score direction (Wiggers H1's actual prediction) is
  the implicit null — if S02b refutes, that does NOT mean
  Garmin-leads-score is supported; it means neither direction has
  significant lagged daily co-variation. A separate Wiggers-direction
  test would need its own pre-registration.
- **Lag value precision.** S02's algorithm picks anchor-week
  resolution (7-day quantum). The "149 days" reported here is the
  exact day-count between anchor dates (2023-01-27 → 2023-06-25),
  not rounded. Sensitivity to ±7 days around the lag is NOT tested
  in S02b; it would be free-parameter inflation.

## 7. Audit-trail discipline

- This spec is committed BEFORE `compute_lagged.py` runs against any
  data. Same discipline as S02.
- The pre-committed bar is locked here at write-time. If the
  computed result is INCONCLUSIVE, that is reported faithfully — not
  drifted to "supported with caveats."
- Any methodology change AFTER data inspection creates
  `S02b-revised/`.

### 7.1 Prior-knowledge disclosure

What was known before locking S02b's bar:
- **From S02**: the lag values (149d and 100d) and that
  the rolling-curve T1 fired at the locked bar. The direction of the
  lag (score leads) is known.
- **From S02 §3.8**: same-day ρ on the full window is small
  (−0.06 primary, all secondaries null). This is informative for
  setting criterion (c): "lag improves over same-day by ≥ 0.10"
  means lagged ρ must reach magnitude ≥ 0.16 to clear (c) alone,
  but (a) requires ≥ 0.20 so (a) is the binding constraint at
  expected ρ values.
- **From [Wiggers H1 framing](../../wiggers_progress_2026-06-07.md)**:
  the "wearables lead" hypothesis is the standard direction in the
  pacing literature; S02b tests the **opposite** direction observed
  in this user's data. The Wiggers map is updated based on S02b's
  outcome.

What was NOT inspected before locking:
- The actual ρ_lagged numbers (script not yet written, let alone
  run).
- Any pair-window n_pairs / n_effective_blocks at the candidate
  lags.
- The directionality of the lagged ρ (sign).

## 8. Registry update — locked

Once `notes.md` is committed, add one line to
[registry.md §4b](../registry.md):

> - **S02b score-lead lagged correlation**
>   ([S02b-score-lead/notes.md](S02b-score-lead/notes.md), run
>   2026-06-07) — daily-resolution Spearman ρ between score(t) and
>   avg-stress(t + 149d) / max-spike(t + 100d) with block-bootstrap
>   CI; tests whether S02's T1 rolling-curve finding survives at
>   daily resolution with autocorrelation correction. Lags
>   pre-committed from S02's algorithmic turnaround dates, NOT
>   free-scanned. **[Verdict + key number to fill in post-run.]**
>   Connects to Wiggers H1 (the project's first direct
>   cross-correlation lag test).

Synthesis.md update is a separate decision.

## 9. What this does NOT do

- Does not test the Wiggers-direction (wearables-lead-score)
  hypothesis. Only the empirically-observed score-leads-wearables
  direction.
- Does not scan a range of lag values. Two pre-committed lags only.
- Does not establish causation even if supported.
- Does not generalise to other users.
- Does not address the May 2026 perturbation (that is S02c).
- Does not address why the score leads the Garmin pendulum — only
  whether the lead pattern is statistically detectable at daily
  resolution.

---

*Spec written 2026-06-07. Execution pending. Same-day execution
expected.*
