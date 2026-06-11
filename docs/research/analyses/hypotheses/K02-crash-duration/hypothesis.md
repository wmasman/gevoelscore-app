# K02 — Crash duration shifted across recovery eras

**Pre-registration written 2026-06-05, before any data was inspected
for this test.** Locked.

**Thread**: K## (kind-of-crash) hypotheses. Second cheap era-shift
test, complementing K01 (depth).

## 1. Claim

The **calendar-day span** of `crash_v1` episodes occurring in
2024-onwards is on average **shorter** than the span of episodes
occurring in 2022–2023. The shift is real enough to be visible at
the median.

## 2. Why we think this

- Same kind-of-crash framing as K01. If recovery has changed the
  *kind* of crash, duration is one of the most plausible axes for
  the shift to appear on.
- K01 found a clear directional but-not-statistically-decisive
  depth shift (early median nadir = 2, late = 3; permutation p =
  0.28). K02 is the orthogonal axis: not how deep but how long.
- Cheap and shares all infrastructure with K01.

## 3. Data sources

- Identical to K01.
- `span` for an episode = `(episode.end - episode.start).days + 1`
  in calendar days (inclusive of both endpoints).

## 4. Measurement protocol

For each `crash_v1` episode:

1. Compute `span_days = (end - start).days + 1`.
2. Tag as early (start ≤ 2023-12-31) or late (start ≥ 2024-01-01).

For each era:
3. Median, mean, IQR, range, max.

**Permutation test for era difference**:

5. Compute `delta_median = median(late span) - median(early span)`.
   (For this test, **negative is supportive** since the hypothesis
   is that late spans are shorter.)
6. 10.000 random shuffles of era labels. Empirical one-sided p-value
   = fraction of shuffles where `delta_median_shuffled ≤
   delta_median_observed`.
7. Same seed (`20260605`).

## 5. Pre-registered falsification criterion

The hypothesis is **supported** if **both** hold:

a. **Magnitude**: `median(early span) − median(late span) ≥ 1` day
   (late episodes shorter by at least a calendar day on the median).

b. **Robustness**: empirical p-value ≤ **0.10** (one-sided: only
   counting shuffles where the late median is at least observed-delta
   smaller than the early median).

Either failing → **refuted** (or "suggestive_underpowered" if
direction matches but p fails, mirroring K01's verdict scheme).

If we have fewer than 8 episodes per era → **inconclusive**.

## 6. Exclusion rules

None. All `crash_v1` episodes counted.

## 7. Expected if hypothesis is true

Sanity checks for `result.md`:

- Early median span: 3–5 days (from preflight, span distribution
  shows 19 of 29 episodes are 2 days but several are 8–14 days)
- Late median span: 2–3 days
- delta ≥ 1 day
- Permutation p ≤ 0.10

If late median is *longer*, that's the inverse finding and would
refute as stated.

## 8. Caveats `result.md` must explicitly acknowledge

- **Span is a coarse metric.** A 2-day crash that's deep and a 2-day
  crash that's shallow get equal weight. K01 + K02 together give two
  axes of the same picture; either alone is partial.
- **Same small-sample / integer-scale brittleness** as K01. Span
  takes more distinct values than nadir (more like 2–14) so the
  median should be less brittle, but the sample size limitation
  remains.
- **`crash_v1` merge rule (3-day window)** influences span directly:
  two short crashes 3 days apart get merged into one longer
  "episode." If the user's crash topology shifted (e.g. clusters →
  isolated), the span metric reflects that, not pure single-crash
  length. This is a feature not a bug for measuring the *experience*
  of a crash period, but it should be noted.

## 9. What we do with each outcome

- **Supported** → with K01 also directionally supportive, the
  kind-of-crash theory has a second body of supporting evidence on
  a different axis. Updates synthesis.
- **Refuted** → spans are basically the same. The recovery shift
  is in depth (K01) and frequency (preflight) but not duration.
  Worth knowing.
- **Suggestive_underpowered** → like K01; report and move on.
- **Inverse** (late longer) → late crashes are deeper-but-shorter or
  shallower-but-longer (with K01 result), suggesting a topology
  shift more than a uniform improvement. Interesting finding.

---

*Pre-registration locked 2026-06-05. Next: `test.py`.*
