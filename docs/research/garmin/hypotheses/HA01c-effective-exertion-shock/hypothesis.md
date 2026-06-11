# HA01c — Effective-exertion shock as crash precursor (per-axis re-formulation of HA01b)

**Pre-registration written 2026-06-07, before any HA01c-specific test
script was run.** Locked per testing playbook
([../../methodology/testing-playbook.md](../../methodology/testing-playbook.md))
section 9 compliance checklist. Any subsequent change to claim,
measurement, threshold, window, or direction creates an HA01d.

HA01c is the **pre-committed follow-up** triggered by the HA01b
per-axis decomposition diagnostic
([../HA01b-per-axis-diagnostic/result.md](../HA01b-per-axis-diagnostic/result.md))
under the playbook's section 5.2 rule: "if exactly ONE axis SUPPORTED
in BOTH eras at the locked bar, pre-register the axis as a new
hypothesis on the single-axis primary." That axis is
`effective_exertion_rank_lagged` (UDS passive intensity-minutes +
recorded activity duration combined into a single per-day metric, then
percentile-ranked against the lagged 30-90-day window).

## 1. Claim

In the **4 days** before a `crash_v1` episode, at least one day's
`effective_exertion_rank_lagged` value is **≥ 0.75** (the "heavy+"
threshold from HA01b's composite). The crash-episode frequency of this
deviation is discriminative against randomly-sampled non-crash windows
in **both train and validate eras independently**.

This is the **per-axis primary** that the HA01b composite obscured.
The composite (`exertion_class_lagged ∈ {heavy, very_heavy}`)
combined 4 axes via MAX-of-ranks and triggered ~78% of the time in
random null windows, diluting discrimination to +3.4 / +1.5 pp.
The single-axis primary triggered only ~60% of the time in null
windows, lifting discrimination to +21.3 / +19.5 pp.

## 2. Why we think this — and why it is NOT a re-run of HA01b

HA01c is **not** a re-test of HA01b. HA01b's pre-registered primary
was the composite `exertion_class_lagged`. That verdict (REFUTED both
eras, +5.8 / +4.0 pp on bundled re-test;
[script 12](../../activity-labels/scripts/12_run_ha_tests_4day_lagged.py))
stays on record. HA01c is a new hypothesis with a different primary,
locked under the playbook's section 2.2 rule ("spec changes create a
new hypothesis ID").

Differences from HA01b's locked spec:

| dimension              | HA01b (composite)                          | HA01c (per-axis)                          |
|---|---|---|
| primary metric         | `exertion_class_lagged ∈ {heavy, very_heavy}` | `effective_exertion_rank_lagged ≥ 0.75` |
| metric construction    | MAX-of-ranks across 4 axes                 | single-axis lagged rank                   |
| trigger                | any 1 of 4 lead-up days is heavy+          | any 1 of 4 lead-up days has rank ≥ 0.75  |
| 3-criterion bar        | (a) freq ≥ 60% (b) disc ≥ +15 pp (c) median n_shock_days ≥ 1 | (a) freq ≥ 60% (b) disc ≥ +15 pp (c) median rank on triggering ≥ 0.875 |
| both-eras requirement  | same                                       | same                                      |

The motivation for HA01c is fully documented in
[HA01b-per-axis-diagnostic/result.md section 5](../HA01b-per-axis-diagnostic/result.md).
HA01c is locked at the SAME rank threshold (0.75) used in the
diagnostic; threshold sensitivity is tested separately in the v2
threshold-monotonicity diagnostic (see section 5 below).

## 3. Data sources

- **Crash labels**: `crash_v1` per registry §2, sourced from
  [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
  Tier-1 `crash` only; dips not included. 29 episodes (14 train,
  15 validate) — playbook section 4.2 default.
- **Effective exertion rank (lagged)**: `effective_exertion_rank_lagged`
  column in
  [`activity-labels/output/activity_features_daily.csv`](../../activity-labels/output/activity_features_daily.csv),
  computed by
  [`11_compute_lagged_baseline.py`](../../activity-labels/scripts/11_compute_lagged_baseline.py).
  Lagged baseline = percentile rank of today's `effective_exertion_min`
  against the 30-90-day prior window (excludes the recent 30 days to
  avoid baseline contamination per Theme A).
- **Analysis window**: 2022-09-03 → 2026-06-05.
- **Train / validate split**: train 2022-09-03 → 2023-12-31
  (14 episodes); validate 2024-01-01 → 2026-06-05 (15 episodes). Same
  as HA01b. Per playbook section 4.3.

## 4. Measurement protocol

### 4.1 Per-day rank trigger

For each calendar date with a valid `effective_exertion_rank_lagged`
value in [0.0, 1.0]: day triggers if rank ≥ **0.75**.

Days with missing lagged baseline (insufficient prior history, inside
the first ~90 days of corpus) are excluded.

### 4.2 Lead-up window (primary, 4-day)

For each crash episode start `C`: lead-up window is `[C-4, C-3, C-2, C-1]`.

Episode triggers if **at least one** of those 4 days has
`effective_exertion_rank_lagged ≥ 0.75`.

### 4.3 Validity

Per episode: at least **3 of 4** lead-up days have a valid lagged
rank value. Matches HA01b's per-axis diagnostic validity rule.

### 4.4 Null sample

200 random non-overlapping 4-day windows from the analysis range;
seed `20260605` per playbook section 4.5. Null windows must not
overlap any crash episode lead-up.

### 4.5 Direction

One-sided elevated (rank ≥ 0.75). The HA01b per-axis diagnostic
result was a positive-discrimination finding (crashes trigger more
often than null); the direction is locked at the diagnostic-finding
direction, not arbitrary.

### 4.6 Locked 3-criterion bar (matches HA01b composite)

A per-era verdict is **SUPPORTED** iff all three pass:

- (a) crash trigger frequency ≥ 60%
- (b) discrimination (crash − null) ≥ +15 pp
- (c) median rank on triggering episodes ≥ 0.875 (halfway from 0.75
  threshold to 1.0)

### 4.7 Both-eras rule

The project-level SUPPORTED verdict requires BOTH train AND validate
to pass the 3-criterion bar (playbook section 4.4 — more stringent
than scientific practice, conservative for the feature use-case).

## 5. v2 threshold-monotonicity diagnostic (co-locked)

Per playbook section 5.1 and the HA01b per-axis diagnostic's
section 6.4 pre-commitment, HA01c is co-locked with a v2
threshold-monotonicity diagnostic that must pass before
effective_exertion is treated as load-bearing in synthesis.

The v2 diagnostic is pre-registered as a sibling folder
[`HA01c-threshold-monotonicity-diagnostic-v2/`](../HA01c-threshold-monotonicity-diagnostic-v2/diagnostic.md).
It tests the discrimination curve across rank thresholds
{0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95} per the locked
five-category shape rule
([../../methodology/threshold-sweep-rescue-criteria-v2.md](../../methodology/threshold-sweep-rescue-criteria-v2.md)).

If HA01c passes the locked bar BUT v2 surfaces a sign-changing or
loose-tail-noise shape, the load-bearing status is withheld pending
threshold refinement. The locked HA01c bar binds; v2 is a stability
check, not a way to rescue or escalate the locked verdict.

## 6. Falsification

HA01c is **REFUTED** if either era fails any of crit (a) / (b) / (c).
HA01c is **SUPPORTED** only if BOTH eras pass all three criteria.

The HA01b per-axis diagnostic found this exact configuration with the
same null sample, same lead-up window, same validity rule, and same
threshold. HA01c re-runs the test as a clean re-formulation with the
per-axis primary explicitly pre-registered.

**Expected outcome (per HA01b per-axis diagnostic result)**: SUPPORTED
in both eras (train +21.3 pp, validate +19.5 pp). However, HA01c is
re-run from scratch as a discipline check: the per-axis diagnostic
was framed as a diagnostic finding, not a re-test verdict. The
playbook section 5.2 requires explicit re-formulation as a separate
hypothesis. The locked bar binds even when intuition predicts the
outcome — if HA01c's re-run produces a different result for any
reason (e.g., null-sample reconstruction yields different draws),
the locked HA01c result is what counts.

## 7. Status

- **Pre-registered**: 2026-06-07
- **Result expected**: after HA01c test.py run (next step pending
  user approval per project workflow)
- **v2 threshold-monotonicity follow-up**: co-locked

## 8. Outputs

If SUPPORTED both eras and v2 passes:
- HA01c result.md
- HA01c v2 diagnostic result.md
- HA01c card.md (separate file per playbook section 2.7; **only if**
  specificity tables pass per playbook section 6.2). Note: HA01b's
  per-axis diagnostic computed a 2.2% posterior per fire for
  effective_exertion at rank ≥ 0.75 — this is the specificity
  problem the v2 threshold-monotonicity diagnostic is designed to
  probe (does a tighter threshold yield acceptable specificity?).

If REFUTED or v2 fails:
- HA01c result.md with the failure mode documented
- No card.md
- HA01b's composite REFUTED verdict stays on record without addition

## 9. Compliance checklist (per playbook section 9, 19 items)

- [x] **Lives at `hypotheses/H##-name/`**: this folder
  (HA01c-effective-exertion-shock) follows the standard structure per
  playbook section 4.7.
- [x] **Locks claim, measurement, threshold, window, direction
  BEFORE data**: HA01c-specific result has NOT been generated yet.
  (The HA01b per-axis diagnostic produced a diagnostic finding, not
  an HA01c verdict.)
- [x] **References playbook**: this entire document.
- [x] **Uses crash_v1**: 29 episodes (14 train, 15 validate); per
  playbook section 4.2 default.
- [x] **Default train/validate split + both-eras rule**: per
  playbook section 4.3 + section 4.4.
- [x] **Lagged baseline**: per playbook section 3.3.
- [x] **Relative thresholds**: rank ≥ 0.75 (rank IS the relative).
- [x] **Primary direction**: one-sided elevated per playbook section
  3.5 (direction locked from the per-axis diagnostic's positive
  result).
- [x] **3-episode dry-run gate**: required in test.py before any full
  run.
- [x] **3-criterion bar**: ≥ 60% / ≥ +15 pp / median rank ≥ 0.875
  (matches HA01b's locked bar).
- [x] **Null sample seed `20260605`, N=200**: per playbook section
  4.5.
- [x] **Validity floors**: ≥ 3 of 4 lead-up days valid; rank value in
  [0, 1].
- [x] **Decision rules → verdict categories per playbook section 2.6**:
  SUPPORTED / REFUTED with both-eras rule applied.
- [x] **Channel-independence acknowledgement**: HA01c uses a single
  axis; the channel non-independence concern from the per-axis
  diagnostic (effective_exertion correlates 0.31-0.69 with the other
  3 axes) is folded into the per-axis diagnostic and informs the
  cross-comparison concern in this hypothesis (HA01c is not
  literally independent of step_burden / vigorous_min validate-only
  findings).
- [x] **Multi-comparison disclosure**: section 6 above + result.md
  when generated.
- [x] **v2 threshold-monotonicity follow-up**: section 5 above
  (co-locked).
- [x] **No-go surfaces flagged**: card.md gate per section 8 (no
  card without specificity-table pass; no crash-risk %, traffic
  lights, push notifications per playbook section 6.6).
- [x] **Hardware constraints**: none specific (effective_exertion is
  UDS daily aggregates + recorded-activity data; no HRV, no
  per-minute body battery dependency, no FR245-blocked metric).
- [x] **Audit trail**: section 2 difference table vs HA01b; the
  per-axis diagnostic's result.md section 7 documents the
  axis-name-mapping and null-sample-construction audit trail that
  HA01c inherits.

## 10. What HA01c would change downstream

If SUPPORTED and v2 passes:
- HA01c becomes the **second project-level SUPPORTED validate-era
  precursor** (after HA10's BB-overnight-recharge result; HA10 was
  the only validate-era precursor SUPPORTED + v2-validated finding
  prior to HA01c).
- Synthesis docs (STOCKTAKE, synthesis.md, addendum) updated with the
  new validate-era precursor.
- The card-craft phase (separate result, per playbook section 2.7)
  applies. Specificity table per playbook section 6.2 is required
  before any card.md is written.
- HA01b composite REFUTED stays on record. HA01c does NOT unlock that
  verdict; it is a separate hypothesis on a different primary.

If REFUTED:
- HA01b composite REFUTED stays on record (unchanged).
- HA01c result documents the per-axis diagnostic finding's
  non-reproducibility; the finding is downgraded from "diagnostic
  finding" to "investigative artefact" per playbook section 2.5
  audit-trail discipline.
- step_burden and vigorous_min validate-only findings remain
  un-promoted (they did not survive both-eras gate even at diagnostic
  level).

---

*HA01c pre-registration locked 2026-06-07 per testing playbook
section 9. Triggered by HA01b per-axis diagnostic finding (both-eras
SUPPORTED on effective_exertion axis at +21.3 / +19.5 pp). Co-locked
with v2 threshold-monotonicity diagnostic.*
