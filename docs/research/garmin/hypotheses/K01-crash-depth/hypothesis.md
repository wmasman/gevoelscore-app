# K01 — Crash depth shifted across recovery eras

**Pre-registration written 2026-06-05, before any data was inspected
for this test.** Locked. Any subsequent change creates a K01b.

**Thread**: K## (kind-of-crash) hypotheses, per
[kind-of-crash-investigation.md](../kind-of-crash-investigation.md).
This is the first direct test of the era-shift theory that synthesis
+ H02 + H02b have made plausible indirectly.

## 1. Claim

The **nadir** (minimum gevoelscore during the episode) of `crash_v1`
episodes occurring in 2024-onwards is on average **higher (less deep)**
than the nadir of episodes occurring in 2022–2023. The shift is real
enough to be visible at the median, not just on average.

## 2. Why we think this

- The user has independently confirmed they are in real recovery
  (~10/year crashes → ~2/year), saved as project memory.
- H02 train showed a stress precursor that's absent in validate;
  H02b train cleared the bar; the spike-magnitude landscape itself
  compressed across the cliff. These all hint at "the kind of crash
  changed."
- If the kind changed, the depths likely changed too. A residual
  crash that survives improved pacing may be qualitatively different
  in severity, not just frequency.
- Cheapest possible direct test — no Garmin data, no new analysis
  infrastructure, just the gevoelscore episodes already detected.

## 3. Data sources

- `day_entries.date` + `day_entries.score` from Directus.
- `crash_v1` episodes per registry §2.
- **Analysis window**: 2022-09-03 → 2026-06-05.
- **Era split**: train era (= "early") 2022-09-03 → 2023-12-31;
  validate era (= "late") 2024-01-01 → 2026-06-05. Same dates as
  H01–H04 train/validate split.
- This is **not** a predictive test — there is no train/validate
  split in the methodological sense. The dates are just the natural
  era boundary surfaced by the preflight.

## 4. Measurement protocol

For each `crash_v1` episode:

1. Identify all calendar dates within the episode's span
   `[start, end]` that have a recorded score.
2. **Episode nadir** = the minimum score across those dates.
3. Each episode is tagged as "early" (start ≤ 2023-12-31) or "late"
   (start ≥ 2024-01-01).

For each era:
4. Compute median nadir, mean nadir, IQR, range.

**Permutation test for the era difference**:

5. Compute observed `delta_median = median(late) - median(early)`.
6. Repeat 10.000 times: randomly shuffle the era labels across all
   episodes, recompute `delta_median_shuffled`.
7. **Empirical p-value** = fraction of shuffles where
   `delta_median_shuffled ≥ delta_median_observed`. Reports
   whether the observed era shift is larger than chance reshuffling
   would produce.

## 5. Pre-registered falsification criterion

The hypothesis is **supported** if **both** hold:

a. **Magnitude**: `median(late nadir) − median(early nadir) ≥ 0.3`
   (on the 1–6 scale, 0.3 is a meaningful but not extreme shift).

b. **Robustness**: empirical p-value from the permutation test
   ≤ **0.10** (one-sided: only counting shuffles where late ≥ early
   by ≥ observed delta). With small samples (14 early, 15 late),
   0.10 is a defensible threshold; insisting on 0.05 would be
   underpowered.

Either failing → **refuted**.

If we have fewer than 8 episodes per era → **inconclusive**.

## 6. Exclusion rules

- **Episodes with no recorded score on any of their constituent days**
  are excluded. (Shouldn't happen given how episodes are constructed,
  but defensive.)
- No other exclusions. K01 deliberately uses all crashes as-is, no
  Garmin-data filters.

## 7. Expected if hypothesis is true

Rough sanity-checks for `result.md`:

- Early median nadir: ~2 (most early crashes bottom at 2 or 3)
- Late median nadir: ~3 (late crashes mostly bottom at 3)
- delta ≈ 0.5–1.0 points
- Permutation p-value < 0.05

If we see late median LOWER than early (i.e. crashes got deeper),
that's a different finding and worth reporting — but would falsify
this hypothesis as stated.

## 8. Caveats `result.md` must explicitly acknowledge

- **Small samples**: 14 early + 15 late episodes. The permutation
  test handles small-sample uncertainty better than parametric tests
  but cannot make the underlying data richer. Findings here are
  suggestive, not conclusive.
- **Score-interpretation drift was ruled out** by user confirmation
  (recovery is real), but residual concerns: a score-3 in 2026 may
  not feel identical to a score-3 in 2022, even if the user thinks
  they're using the scale consistently.
- **Late era includes only 4 episodes after 2024** (2 in 2025, 2 in
  2026); most of the 15 late episodes are still in 2024. The "era"
  comparison is really "2022–23 vs 2024 with a small 2025+ tail."
  K01b in a year or two with more late data would tighten this.
- **`crash_v1` mixes mechanisms** — the depth shift could be
  driven by one subtype changing (e.g. infection-precipitated
  crashes becoming less severe) while others stay the same.

## 9. What we do with each outcome

- **Supported (a + b pass)** → direct evidence the kind-of-crash
  theory is correct. Updates synthesis. Increases prior on K02
  (duration) and K03 (symptom profile). Card-design implication:
  recovery-arc card can include "crashes have gotten less deep,
  median X → Y."
- **Refuted (a fails)** → crashes are roughly the same depth in
  both eras. The era shift is in *frequency* only, not severity.
  Worth knowing — narrows the kind-of-crash theory to a
  frequency claim.
- **Suggestive (a passes, b fails)** → observed direction matches
  but the small sample can't rule out chance. Report and move on;
  don't claim support.
- **Inverse (late median lower)** → crashes have gotten *deeper*.
  Unexpected. Would warrant a careful look at whether this is real
  or driven by 1–2 deep outliers in the late era.

---

*Pre-registration locked 2026-06-05. Next: `test.py`.*
