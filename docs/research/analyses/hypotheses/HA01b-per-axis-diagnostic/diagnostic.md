# HA01b per-axis decomposition diagnostic

**Pre-registration locked 2026-06-07** per the user-locked Option A
testing playbook
([methodology/testing-playbook.md](../../methodology/testing-playbook.md)).
This diagnostic follows the playbook's compliance checklist (§9)
and the per-axis decomposition protocol (§5.2).

**Criteria source**: this diagnostic locks its own
per-axis-specific criteria below; v2 threshold-monotonicity
criteria
([threshold-sweep-rescue-criteria-v2.md](../../methodology/threshold-sweep-rescue-criteria-v2.md))
apply downstream if any axis is found SUPPORTED at the locked bar.

## 1. What this diagnostic evaluates

**Test under diagnostic**: HA01b (activity-shock precursor; 4-day
lead-up window; `exertion_class_lagged ∈ {heavy, very_heavy}` as
trigger). HA01b's locked verdict under Theme A's lagged baseline is
**REFUTED both eras** (train +5.8 pp, validate +4.0 pp).

The composite metric `exertion_class` is the MAX percentile rank
across four input axes:
- `effective_exertion_min_rank_lagged` (UDS passive intensity +
  recorded activity duration)
- `step_burden_rank_lagged` (total daily steps)
- `max_hr_peak_rank_lagged` (daily max HR)
- `vigorous_min_rank_lagged` (recorded vigorous-intensity duration)

The peer review §3 flagged that this composite "averaged away" the
Theme A baseline-contamination bug's direct visibility and could be
hiding a per-axis signal.

**Diagnostic question**: If HA01b had been pre-registered on each
individual axis as primary (rather than on the composite), would
any single axis have produced a SUPPORTED verdict under the same
locked bar?

## 2. Playbook compliance (per §9 checklist)

- [x] **Lives at `hypotheses/H##-name/`**: this folder
  (HA01b-per-axis-diagnostic) follows the standard structure per
  playbook §4.7.
- [x] **Locks claim, measurement, threshold, window, direction
  BEFORE data**: this document locks the per-axis test before
  per-axis fine-grid data is inspected. (Composite verdict already
  inspected per Theme A bundled re-test; per-axis is the new
  surface.)
- [x] **References playbook**: this entire document.
- [x] **Uses crash_v1**: 29 episodes (14 train, 15 validate); per
  playbook §4.2 default.
- [x] **Default train/validate split + both-eras rule**: per
  playbook §4.3 + §4.4 — train 2022-09-03 → 2023-12-31, validate
  2024-01-01 → 2026-06-05. (Diagnostic, so the both-eras rule
  applies per-axis: each axis is SUPPORTED only if it clears the
  bar in both eras.)
- [x] **Lagged baseline**: per playbook §3.3 — `_rank_lagged`
  columns already computed by
  [`11_compute_lagged_baseline.py`](../../activity-labels/scripts/11_compute_lagged_baseline.py).
- [x] **Relative thresholds**: per playbook §3.4 — rank ≥ 0.75
  (same as HA01b composite; rank IS the relative threshold).
- [x] **Primary direction**: per playbook §3.5 — one-sided
  elevated (shocks = high values; this matches HA01b composite
  direction).
- [x] **3-episode dry-run gate**: locked below in §5.
- [x] **3-criterion bar**: ≥ 60% frequency / ≥ +15 pp
  discrimination / median magnitude ≥ floor (matches HA01b's
  locked bar).
- [x] **Null sample seed `20260605`, N=200**: per playbook §4.5.
- [x] **Validity floors**: per playbook §4.6 — same per-day
  rank-availability rules as HA01b.
- [x] **Decision rules → verdict categories per playbook §2.6**:
  locked in §6 below; uses SUPPORTED/REFUTED at the per-axis
  level, with per-axis SUPPORTED producing a "diagnostic finding"
  (not a project-level SUPPORTED).
- [x] **Channel-independence acknowledgement**: §7 below per
  playbook §6.1.
- [x] **Multi-comparison disclosure**: §7 below per playbook §7.2.
- [x] **v2 threshold-monotonicity follow-up if SUPPORTED**:
  per playbook §5.1, locked in §6 below.
- [x] **No-go surfaces flagged**: §7 below per playbook §6.6 —
  any SUPPORTED axis must not be surfaced as "crash risk
  percentage" or other forbidden patterns.
- [x] **Hardware constraints**: none specific (HA01b operates on
  UDS daily aggregates + recorded-activity data; no HRV
  dependency).

This diagnostic is the first to be locked under the consolidated
testing playbook. It is the playbook's compliance reference case.

## 3. Data sources

- **Crash labels**: `crash_v1` from
  [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
- **Per-axis lagged ranks**: from
  [`activity-labels/output/activity_features_daily.csv`](../../activity-labels/output/activity_features_daily.csv)
  after the
  [`11_compute_lagged_baseline.py`](../../activity-labels/scripts/11_compute_lagged_baseline.py)
  augmentation. Each axis has its own
  `*_rank_lagged` column.
- **Analysis window + train/validate split**: same as HA01b
  (train 2022-09-03 → 2023-12-31, 14 episodes; validate
  2024-01-01 → 2026-06-05, 15 episodes).

## 4. Measurement protocol

### 4.1 Per-axis trigger

For each axis A ∈ {effective_exertion_min, step_burden, max_hr_peak,
vigorous_min}, define:

- Per-day axis trigger: `A_rank_lagged ≥ 0.75` (matches HA01b's
  composite "heavy+" threshold per axis).
- Episode trigger (one-sided elevated, primary): at least one day
  in the lead-up window has `A_rank_lagged ≥ 0.75`.

### 4.2 Lead-up windows

Same as HA01b:
- **4-day primary**: `[C-4, C-3, C-2, C-1]`.
- **5-day secondary**: `[C-5, C-4, C-3, C-2, C-1]`.

### 4.3 Validity

- Per episode: at least 3 of 4 lead-up days have valid
  `A_rank_lagged` (matches HA01b validity rule).
- Days with missing lagged baseline (insufficient prior history,
  inside the first ~90 days of corpus) excluded.

### 4.4 Null sample

200 random non-overlapping 4-day windows; seed `20260605`. Same
construction as HA01b. The null sample is shared across all 4 axes
(same windows, different per-axis trigger evaluations).

### 4.5 Per-axis verdict

For each axis × era (4 × 2 = 8 verdicts):

- Crash trigger frequency
- Null trigger frequency
- Discrimination (crash − null, pp)
- Median magnitude on triggering episodes (% above the locked
  0.75 threshold among triggering days)

Apply locked 3-criterion bar:
- (a) crash trigger frequency ≥ 60%
- (b) discrimination ≥ +15 pp above null
- (c) median rank on triggering episodes ≥ 0.875 (halfway from
  the 0.75 threshold to 1.0)

SUPPORTED if all three pass; REFUTED otherwise.

### 4.6 Composite control

As a control, also re-compute HA01b's composite verdict using the
same per-episode profiles. Confirms reproducibility of the locked
Theme A bundled re-test verdict (HA01b-recomputed REFUTED both
eras at +5.8 / +4.0 pp).

### 4.7 Cross-axis correlation matrix

Per playbook §6.1 (channel-independence honest framing): report
the Pearson and Spearman correlation matrix of the 4 axes
(`*_rank_lagged` values across all valid days). Quantifies the
"4 axes overstates independence" caveat.

## 5. 3-episode dry-run gate (per playbook §2.3)

Before running the full per-axis test, print first 3 train and
first 3 validate episodes' per-day per-axis rank values. Confirms:
- Per-axis ranks span [0, 1] as expected
- No axis has pathological all-zero or all-one values across the
  sample
- Each axis's trigger rate on the sample is in a sane range
  (e.g. 0-100%)

If the dry-run surfaces a pathology, the per-axis spec needs
review BEFORE the full run.

## 6. Pre-committed decision rules (per playbook §5.2)

### 6.1 If NO axis SUPPORTED at the locked bar

Confirms HA01b's REFUTED verdict. The per-axis decomposition shows
no single-axis signal hidden by the composite. **No follow-up
required.** The diagnostic finding: the composite's REFUTED
verdict was honest; no axis carries a precursor signal the
composite missed.

### 6.2 If exactly ONE axis SUPPORTED at +15 pp

**Diagnostic finding, NOT load-bearing.** Per playbook §5.2:
- The axis is flagged as a candidate for a new pre-registered
  hypothesis (HA01c) on truly new data OR with additional
  validation.
- The synthesis-level "HA01b REFUTED" stays on record.
- Before any load-bearing claim, the axis must:
  1. Be re-pre-registered as HA01c with the single-axis primary
     locked (NOT the composite).
  2. Pass v2 threshold-monotonicity diagnostic per playbook §5.1
     (replacing the rank-based primary with a fine grid of rank
     thresholds, e.g. 0.50, 0.60, ..., 0.95).
  3. Pass specificity tables per playbook §6.2 before any card
     implication.

### 6.3 If MULTIPLE axes SUPPORTED

Stronger signal but still diagnostic. The cross-axis correlation
matrix (§4.7) determines whether this is genuinely multi-channel
or one shared underlying signal:
- High correlation between SUPPORTED axes → the "multiple SUPPORTED"
  is one signal counted multiple times; treat as single finding
  for the HA01c follow-up.
- Low correlation → genuinely independent axis signals; the
  composite's REFUTED verdict becomes surprising (why didn't the
  max-rank catch any of them?) and merits deeper investigation
  before HA01c.

In either case, multi-comparison concern (§7 below) is
quantified honestly.

### 6.4 v2 threshold-monotonicity if SUPPORTED

Any per-axis verdict that hits SUPPORTED at the locked bar must
additionally pass a v2 threshold-monotonicity diagnostic before
the axis is treated as load-bearing in synthesis. The v2
diagnostic uses the same fine-grid approach but with rank
thresholds instead of N_std (e.g. rank ≥ 0.50, 0.60, 0.70, 0.75,
0.80, 0.85, 0.90, 0.95).

## 7. Caveats `result.md` must explicitly acknowledge

Per playbook §7.2 multi-comparison disclosure:

- **Family-wise false-positive rate**: testing 4 axes at the locked
  bar means the family-wise expected ≥ 1 SUPPORTED under the null
  is > 5%. The exact rate depends on cross-axis correlation; the
  cross-axis correlation matrix (§4.7) lets us estimate the
  effective number of independent comparisons. If correlations are
  high (e.g. > 0.7), the effective N is closer to 1-2 and the
  false-positive concern is bounded. If low, it's closer to 4.

- **Channel non-independence** (per playbook §6.1): the 4 axes
  share underlying physical activity. "4 axes" overstates
  independence; the result.md must use language that respects
  this.

- **The locked HA01b verdict is REFUTED both eras**; the per-axis
  diagnostic does NOT unlock this verdict. Any SUPPORTED axis is
  a diagnostic finding, NOT a re-test verdict.

- **Specificity caveat (per playbook §6.2)**: even a SUPPORTED
  axis would not be a predictive card. Posterior probability per
  fire must be computed before any card implication.

- **Multi-comparison context** (per playbook §7.2): this is the
  20th pre-registered hypothesis/diagnostic in the H##/HA## series.
  Most have refuted; the multi-comparison concern at the project
  level is real but the held-out validate window has been doing
  its defensive work.

## 8. What this produces

- `result-data.json`: per-axis discrimination table (4 axes × 2
  eras × 2 windows = 16 entries) + composite control verdict +
  cross-axis correlation matrix + per-axis trigger directional
  split.
- `result.md`: locked verdicts per axis, framing per §6 decision
  rules, multi-comparison disclosure, cross-axis correlation
  reporting.
- If any axis is SUPPORTED at the locked bar: a follow-up entry
  in QUEUED-WORK for HA01c pre-registration AND for v2
  threshold-monotonicity diagnostic on that axis.

## 9. Outputs

This diagnostic does NOT produce a new SUPPORTED/REFUTED verdict
at the project level; it produces a "diagnostic finding" that
informs whether HA01c is worth pre-registering. The locked HA01b
REFUTED verdict stays on record.

---

*Pre-registration locked 2026-06-07 per the testing playbook §9
compliance checklist. This is the first diagnostic to be locked
under the consolidated playbook.*
