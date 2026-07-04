# HA01c single-pool cross-check — pre-registration

**Pre-registration written 2026-07-03, before any single-pool test
script was run.** The derived data this test consumes
(`labels_crash_v2.csv`, `activity_features_daily.csv`) is gitignored
and not materialised in the working tree at lock time, so the lock
genuinely precedes any result.

**This is a validation-framework cross-check, NOT a new hypothesis.**
It re-runs the *already-locked* HA01c primary
([../HA01c-effective-exertion-shock/hypothesis.md](../HA01c-effective-exertion-shock/hypothesis.md))
under the single-pool framework
([`../../../methodology/train_validate_split_fate.md`](../../../methodology/train_validate_split_fate.md),
[`../../../methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)).
It changes only the **validation framework** (pooling + null model +
uncertainty), not the claim, measurement, threshold, window, or
direction. Under the HA01c lock clause (hypothesis.md preamble: "any
subsequent change to claim, measurement, threshold, window, or
direction creates an HA01d"), this re-run does **not** create an
HA01d, and it does **not** re-lock or disturb HA01c's on-record
verdict. It is the "re-run a locked pre-reg under the new framework"
move defined in
[`train_validate_split_fate.md §5.7`](../../../methodology/train_validate_split_fate.md)
and [`queued_work.md Q10`](../../../methodology/queued_work.md) — a
descriptive cross-check with no automated re-locking. HA01c is not
currently in Q10's row-list (HA01b, HA02c, HA08, HA11, H05); this
file adds it.

## 1. Purpose

HA01c's locked verdict is "SUPPORTED both eras at rank >= 0.75,
v2-mixed -> SUPPORTED-with-stability-mixed, NOT load-bearing." That
verdict was computed under the retired 2023-12-31 train/validate
split with the both-eras rule and a 200-window sampled null. The
project has since retired the split as primary
([`train_validate_split_fate.md §2`](../../../methodology/train_validate_split_fate.md))
and moved to full-Stratum-4 single-pool inference with a permutation
null + stationary bootstrap CI
([`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)).
The seven scorecard signals were re-run single-pool
([`../../garmin_exploration/cards/trust-panel-export.md`](../../garmin_exploration/cards/trust-panel-export.md));
HA01c was not. This cross-check gives the effective-exertion channel
an honest single-pool number, in the same shape as those seven, so
the downstream site can stop carrying HA01c in the retired two-era
"supported" framing.

## 2. What stays locked vs what changes

### Locked (inherited verbatim from HA01c; changing any -> HA01d)

- Metric: `effective_exertion_rank_lagged`, single axis
- Threshold: rank >= 0.75
- Lead-up window: 4-day, `[C-4, C-3, C-2, C-1]`
- Direction: one-sided elevated
- Per-episode validity: at least 3 of 4 lead-up days have a valid
  rank in [0, 1]
- Crash labels: `crash_v1` tier-1 episodes (29) from
  `labels_crash_v2.csv`

### Changed (the framework swap)

| dimension | HA01c (locked) | this cross-check |
|---|---|---|
| pooling | train (n=14) + validate (n=15), both-eras rule | full pool, all 29 (single-pool primary) |
| null model | 200 sampled non-overlapping 4-day windows | block-bootstrap null, stationary blocks E[L]=7 |
| uncertainty | none (point estimate + 3-criterion bar) | stationary bootstrap 95% CI on discrimination, E[L]=7 |
| block-length check | none | data-driven E[L]* companion + factor-of-2 flag |
| split | primary | optional M3 descriptive overlay only |
| verdict rule | 3-criterion bar x both eras | permutation p primary (see §5) |

## 3. Data sources

- **Crash labels**: `crash_v1` tier-1 `crash` episodes from
  [`../crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv)
  (emitted by
  [`../crash_v2-definition/scripts/apply_crash_v2.py`](../crash_v2-definition/scripts/apply_crash_v2.py)).
  29 episodes; episode start = earliest sub-threshold day per
  `episode_id`.
- **Effective exertion rank (lagged)**:
  `effective_exertion_rank_lagged` column in
  `../../garmin_exploration/activity-labels/output/activity_features_daily.csv`
  (emitted by
  [`../../garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py`](../../garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py)).
  **Path correction**: the original
  [`../HA01c-effective-exertion-shock/test.py`](../HA01c-effective-exertion-shock/test.py)
  reads this from `analyses/activity-labels/output/...`; the pipeline
  now lives under `analyses/garmin_exploration/activity-labels/...`.
  This cross-check uses the current path.
- **Analysis window (Stratum 4)**: 2022-09-03 -> 2026-06-05.
- **No primary split.** The 2023-12-31 boundary is used only for the
  optional M3 overlay in §7.

## 4. Measurement protocol (single-pool)

### 4.1 Per-episode trigger (unchanged from HA01c)

For each crash start `C`: lead-up window `[C-4 .. C-1]`. The episode
triggers if at least one lead-up day has
`effective_exertion_rank_lagged >= 0.75`. Valid iff at least 3 of 4
lead-up days have a valid rank. Episodes failing validity (early-
corpus, inside the ~90-day lagged-baseline warmup) are dropped;
report `n_clean`. Inconclusive if `n_clean < 10`.

### 4.2 Candidate-anchor / background pool

A **candidate anchor** is any date `A` in the analysis window whose
4-day lead-up window is valid (>= 3 of 4 days with a valid rank).
`W(A) = 1` iff any valid lead-up day of `A` has rank >= 0.75. The
**background pool** is all candidate anchors whose lead-up window
does **not** overlap any crash lead-up window (the same "ordinary
window" exclusion the original 200-window null used). The background
trigger rate `p_bg = mean W over the background pool` is the
single-pool analogue of the null-fire rate.

### 4.3 Point estimates

- `p_crash = (# clean crash episodes with W=1) / n_clean`
  (= single-pool sensitivity / recall).
- `p_bg` per §4.2 (expected ~0.605 from the HA01c per-axis
  diagnostic).
- **Discrimination = (p_crash - p_bg) * 100 pp** (single-pool).

### 4.4 Permutation null (primary inference) — block-bootstrap, E[L]=7

Per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)
("permute crash/null labels in blocks drawn from the geometric
E[L]=7 distribution"), implemented as a stationary-block bootstrap of
the anchor labels:

- Order the background pool chronologically.
- For each of `B = 10,000` replicates, draw a pseudo-crash set of
  `n_clean` anchors by stationary-block sampling (random start,
  geometric block length mean 7, consecutive anchors, accumulate to
  `n_clean`, trim), and compute `T* = mean W` over that set.
- `p = (1 + #{T* >= T_obs}) / (B + 1)`, where `T_obs = p_crash`.

Block sampling from the background pool preserves the local
autocorrelation of the trigger series while randomising the
crash/ordinary alignment. Seed `20260703`.

### 4.5 Stationary bootstrap 95% CI on discrimination — E[L]=7

`B = 10,000` replicates. Per replicate: stationary-block resample the
`n_clean` crash-episode W-values (chronological order, E[L]=7) ->
`p_crash*`; stationary-block resample the background pool (E[L]=7) ->
`p_bg*`; `disc* = p_crash* - p_bg*`. Report the 2.5 / 97.5 percentile
CI. The 26-episode arm dominates the width. Seed `20260703`.

### 4.6 Data-driven block-length companion (E[L]*)

Compute the autocorrelation of the daily trigger indicator
`I(d) = 1[rank >= 0.75]` (valid days, date order). Report `E[L]*` =
first lag at which |ACF| falls below the white-noise band
`2 / sqrt(N)`. This is a transparent proxy, **not** the Politis-White
estimator. **Flag for review** if `|E[L]* - 7| / 7 > 0.5` (i.e.
E[L]* < 3.5 or > 10.5), per the block-length MD result template.

### 4.7 Usability metrics (trust-table companion format)

At the single-pool base rate **2.11%** (29 / 1372):
- sensitivity = `p_crash`; specificity = `1 - p_bg`;
- `PPV = b*sens / (b*sens + (1-b)*(1-spec))`, `lift = PPV / b`,
  `b = 0.0211` (also reported at `b = 0.0169`, the validate base);
- tier per the trust-panel rule (Tier C if PPV < 5%).

## 5. Locked verdict rule

**Primary:** single-pool **SUPPORTED** iff the permutation p-value
(§4.4) `< alpha_primary = 0.05`; otherwise **NOT-SUPPORTED**. This
matches the operative bar under which, of the seven scorecard
signals, only HA07d cleared.

**Multiplicity context (reported, not a second gate):** HA01c is the
single-axis re-expression of the exertion channel already represented
on the scorecard by HA01b — **not** a fresh independent comparison.
It therefore does not add to the effective-N (~4) multiplicity
budget. The result reports p against alpha = 0.05 and against the
effective-N Bonferroni alpha ~ 0.0125 for honesty, per
[`primary-verdict-statistics.md`](../../garmin_exploration/cards/primary-verdict-statistics.md).

**Legacy bar (reported, descriptive continuity only):** the original
HA01c 3-criterion bar (freq >= 60%, disc >= +15 pp, median rank on
triggering >= 0.875) is computed on the pooled data and reported, but
does **not** drive the single-pool verdict.

## 6. Decisions flagged for confirm-at-review

Four choices were made against the recommended defaults; the
fresh-session reviewer should confirm or contest each **before the
run**:

1. **Verdict rule = permutation p primary** (§5), not the pooled
   3-criterion bar. Rationale: the single-pool framework mandates
   permutation null + CI; the legacy bar has no significance/CI
   component.
2. **Multiplicity = re-expression of HA01b's channel** (§5), not a
   new independent test. Rationale: same axis, single-axis primary of
   the composite already on the scorecard.
3. **Permutation scheme = block-bootstrap of anchor labels from the
   background pool, stationary blocks E[L]=7** (§4.4), vs the
   alternative circular-rotation permutation. Rationale: closest to
   the MD's "permute labels in blocks drawn from the geometric
   distribution."
4. **Off-scorecard placement** (§8): report as an adjacent companion
   to HA01b, keeping the scorecard at seven and the "1 of 7
   supported" headline stable, vs replacing HA01b or adding an 8th
   signal.

## 7. M3 sensitivity overlay (number, not narrative)

Report train-era (<= 2023-12-31) and validate-era (> 2023-12-31)
discrimination as descriptive numbers only, with no per-era verdict
and no per-era alpha, per
[`train_validate_split_fate.md §5.8`](../../../methodology/train_validate_split_fate.md):
"under the M3 overlay, train-vs-validate divergence is a number, not
a narrative." The overlay answers "is the single-pool verdict robust
to era partition?" It does not answer "does the effect change over
time?" — the n=1 design cannot adjudicate that.

## 8. Outputs

- `result-data.json`: point estimates, permutation p, bootstrap CI,
  E[L]* + flag, usability metrics, legacy-bar values, M3 overlay.
- `result.md`: single-pool verdict in the trust-table companion
  format; explicit note that it is the per-axis sibling of HA01b and
  sits **off** the seven-signal scorecard (pending decision 6.4).
- **Site reconciliation** (separate, downstream): update the stale
  HA01c two-era "supported" row in the site narrative to the
  single-pool verdict.

## 9. Falsification and honest expected outcome

**SUPPORTED** iff permutation p < 0.05 (§5). **NOT-SUPPORTED**
otherwise.

Two parts of the outcome behave differently, and honesty requires
separating them:

- **Usability is robustly poor, regardless of significance.** The
  binding problem is specificity: `p_bg ~ 0.605` gives specificity
  ~ 39.5%, PPV ~ 2-3%, lift ~ 1.06x -> **Tier C**. This follows from
  the background trigger rate alone and does not depend on the
  permutation p. Whatever the verdict, HA01c is not shippable as a
  card, exactly as its own caveats already state.
- **The verdict itself is genuinely uncertain and must not be
  pre-judged.** The per-era Fisher p-values (0.14 train, 0.11
  validate;
  [`primary-verdict-statistics.md`](../../garmin_exploration/cards/primary-verdict-statistics.md))
  were computed per-era on n=11 / n=15 against an iid 200-window
  null. Pooling to n_clean ~ 26 roughly halves the standard error,
  which pushes an iid permutation p well below those per-era values
  (dry synthetic checks put the iid-background pooled p near ~0.02).
  The block-bootstrap null then inflates that back up by an amount
  set entirely by the **real** daily-trigger autocorrelation (the
  E[L]* companion, §4.6). Activity-derived metrics carry weekly
  cycles, so meaningful inflation is plausible. The pooled
  permutation p can therefore land on either side of alpha = 0.05;
  it is **not** a foregone NOT-SUPPORTED. The point of the run is to
  produce that number honestly under the locked framework, not to
  confirm a predicted verdict.

Either way, the single-pool number replaces HA01c's stale two-era
"supported" framing on the site with one computed under the current
framework — which is the actual objective.

## 10. Discipline

- **Fresh-session review before the run.** Per the pre-reg-writer
  role split, this pre-registration is drafted in one session; its
  `/research-review` must be a different session, reading this file +
  the two framework MDs + the checklist cold. The test.py is run
  only after that review.
- **Does not trip the HA01d clause** (§preamble). HA01c's locked
  verdict and its v2 diagnostic stay on record unchanged.
- **No re-lock.** Per Q10, no historical verdict is re-locked by this
  cross-check.

## 11. Compliance checklist (playbook section 9, adapted)

- [x] Lives at `hypotheses/HA01c-single-pool-crosscheck/`
- [x] Locks claim/measurement/threshold/window/direction (inherited)
      + framework BEFORE data (data not materialised at lock time)
- [x] References the single-pool framework MDs + the playbook
- [x] Uses crash_v1 (29 tier-1 episodes)
- [x] Single-pool primary; split demoted to M3 overlay
- [x] Lagged baseline (`effective_exertion_rank_lagged`)
- [x] Relative threshold (rank >= 0.75)
- [x] One-sided elevated direction (inherited)
- [x] Permutation null + stationary bootstrap CI, E[L]=7
- [x] Data-driven E[L]* companion + factor-of-2 flag
- [x] Verdict rule locked (permutation p < 0.05 primary)
- [x] Multiplicity context declared (re-expression of HA01b channel)
- [x] Seed `20260703`, B = 10,000
- [x] Validity floor: >= 3 of 4 lead-up days; rank in [0, 1]
- [x] 3-episode dry-run gate in test.py before full run
- [x] No-go surfaces unchanged (reflective-only; no crash-risk %,
      traffic lights, push notifications)
- [x] Fresh-session review required before run (section 10)
- [x] Does not create HA01d; no historical re-lock

---

*Pre-registration drafted 2026-07-03. Recommended defaults locked
pending fresh-session review of the four decisions in section 6.
Test runs only after that review, and only once the derived data is
materialised.*
