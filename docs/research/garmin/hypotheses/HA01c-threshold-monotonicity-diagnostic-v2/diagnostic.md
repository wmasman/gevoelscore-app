# HA01c v2 threshold-monotonicity diagnostic

**Pre-registration locked 2026-06-07** per the user-locked Option A
testing playbook
([../../methodology/testing-playbook.md](../../methodology/testing-playbook.md)).
This diagnostic follows the playbook's compliance checklist (§9)
and the v2 threshold-monotonicity protocol (§5.1) using the locked
five-category shape rule
([../../methodology/threshold-sweep-rescue-criteria-v2.md](../../methodology/threshold-sweep-rescue-criteria-v2.md)).

**Criteria source**: the locked v2 five-category shape rule.

## 1. What this diagnostic evaluates

**Test under diagnostic**: HA01c (effective_exertion shock; 4-day
lead-up window; `effective_exertion_rank_lagged ≥ 0.75` as the locked
primary). HA01c's pre-registered verdict at rank ≥ 0.75 is locked
separately; this diagnostic does NOT change that locked verdict.

**Diagnostic question**: How does HA01c's discrimination curve behave
across a fine grid of rank thresholds {0.50, 0.60, 0.70, 0.75, 0.80,
0.85, 0.90, 0.95}? Is the locked-threshold (0.75) result a stable
point on a monotone curve, or a single-threshold artifact?

The v2 protocol applies the locked five-category shape rule:

- **Cat 1** canonical decline (peak at low threshold, monotone decline)
- **Cat 2** stable plateau (flat across mid-range thresholds)
- **Cat 3** rising / late-peak (peak at higher threshold, monotone rise)
- **Cat 4** bumpy with sign-changes (zero-crossings in meaningful range)
- **Cat 5** loose-tail noise (sub-floor magnitudes)

Cat 1, 2, 3 → RESCUE (the locked-threshold result is a stable
point on a coherent curve).
Cat 4, 5 → CLOSE (the locked-threshold result is a single-threshold
artifact; the locked verdict's load-bearing status is withheld).

## 2. Playbook compliance (per §9 checklist)

- [x] **Lives at `hypotheses/H##-name/`**: this folder
  (HA01c-threshold-monotonicity-diagnostic-v2) follows playbook
  §4.7.
- [x] **Locks claim, measurement, threshold, window, direction
  BEFORE data**: this document locks the v2 threshold sweep BEFORE
  the HA01c locked-threshold test.py runs and BEFORE any
  fine-grid threshold data is computed.
- [x] **References playbook**: this entire document + locked v2
  criteria doc.
- [x] **Uses crash_v1**: 29 episodes (14 train, 15 validate); per
  playbook §4.2 default.
- [x] **Default train/validate split + both-eras rule**: per
  playbook §4.3 + §4.4 — train and validate are evaluated
  independently; the v2 shape rule applies per-era.
- [x] **Lagged baseline**: per playbook §3.3.
- [x] **Relative thresholds**: rank thresholds {0.50, 0.60, 0.70,
  0.75, 0.80, 0.85, 0.90, 0.95} (rank IS the relative).
- [x] **Primary direction**: one-sided elevated (matches HA01c).
- [x] **3-episode dry-run gate**: locked in §5 below.
- [x] **3-criterion bar**: per HA01c at each threshold point in the
  sweep (≥ 60% freq, ≥ +15 pp disc, median rank ≥ threshold + 0.125
  scaled to the threshold under test — see §4.4 below).
- [x] **Null sample seed `20260605`, N=200**: per playbook §4.5.
  Same null sample as HA01b per-axis diagnostic and HA01c.
- [x] **Validity floors**: ≥ 3 of 4 lead-up days valid per playbook
  §4.6.
- [x] **Decision rules → verdict categories per playbook §2.6**:
  RESCUE / CLOSE applied per five-category shape rule (locked v2
  criteria doc).
- [x] **Channel-independence acknowledgement**: same single axis as
  HA01c (effective_exertion); independence within-channel is
  acknowledged via the per-axis diagnostic correlation matrix.
- [x] **Multi-comparison disclosure**: 8 threshold-points × 2 eras =
  16 evaluations; the v2 shape rule is precisely designed to control
  this multi-comparison concern (any threshold-by-threshold "best
  pick" without shape coherence is rejected).
- [x] **v2 threshold-monotonicity follow-up**: this IS the v2
  follow-up; no further nesting.
- [x] **No-go surfaces flagged**: §7 below per playbook §6.6.
- [x] **Hardware constraints**: none specific.
- [x] **Audit trail**: this is the 5th v2 diagnostic in the v2 round
  (after HA10, HA07d, HA06b, HA11). The same v2 protocol applies as
  to the others. v2 criteria are locked separately and unchanged.

## 3. Data sources

Identical to HA01c and the HA01b per-axis diagnostic:

- **Crash labels**: `crash_v1` from
  [`labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
- **Effective-exertion lagged rank**:
  `effective_exertion_rank_lagged` from
  [`activity_features_daily.csv`](../../activity-labels/output/activity_features_daily.csv).
- **Analysis window + split**: same as HA01c.

## 4. Measurement protocol

### 4.1 Threshold grid (locked)

Eight threshold points:
- **τ ∈ {0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95}**

The "meaningful range" for the v2 shape rule is **[0.50, 0.95]**
(all 8 points; rank is bounded in [0, 1] and rank ≥ 0.50 is the
"above-median" half). 0.75 is the locked HA01c threshold for
reference.

### 4.2 Per-threshold evaluation

For each τ:
- Per-day trigger: `effective_exertion_rank_lagged ≥ τ`.
- Per-episode trigger: at least 1 of 4 lead-up days triggers.
- Compute discrimination: P(trigger | crash) − P(trigger | null), pp.

Produces a discrimination curve disc(τ) for each era (train,
validate).

### 4.3 Five-category shape rule application

Per locked v2 criteria doc, compute for each era:

- **peak τ**: argmax disc(τ) over the meaningful range
- **peak_disc**: max disc(τ) over the meaningful range
- **sign-changes**: zero-crossings of disc(τ) within [1.0 raw, 3.0
  raw] — but rank thresholds are not raw N_std; the rank analog is
  [0.60, 0.90] (the mid-band excluding the extremes). Sign-changes
  counted in [0.60, 0.90].
- **shape categorisation** per Cat 1-5 rules.

### 4.4 v2 verdict bar (per locked five-category criteria)

- **Cat 1 (canonical decline)**: peak in [0.50, 0.70], monotone
  decline beyond peak, peak_disc ≥ **+7 pp** at any threshold ≥ 0.75
  (i.e., the floor that the locked criteria doc raised for Cat 1).
- **Cat 2 (stable plateau)**: disc(τ) ranges over ≤ 5 pp across the
  meaningful range, all values ≥ +5 pp.
- **Cat 3 (rising / late-peak)**: peak at τ ≥ 0.80, monotone rise to
  peak, peak_disc ≥ +15 pp (HA01c's locked threshold), 0 sign-changes
  in [0.60, 0.90].
- **Cat 4 (bumpy with sign-changes)**: ≥ 1 sign-change in [0.60,
  0.90].
- **Cat 5 (loose-tail noise)**: peak_disc < +5 pp.

Cat 1, 2, 3 → **RESCUE** (HA01c locked verdict stands as
load-bearing).
Cat 4, 5 → **CLOSE** (HA01c locked verdict is honest at the locked
threshold but does NOT graduate to load-bearing without further
work).

### 4.5 Null sample

Same null sample as HA01c and HA01b per-axis (seed `20260605`,
N=200, non-overlapping 4-day windows excluding crash lead-up).

### 4.6 Validity

Per-episode validity: ≥ 3 of 4 lead-up days with valid lagged rank.

## 5. 3-episode dry-run gate (per playbook §2.3)

Before running the full sweep, print first 3 train and first 3
validate episodes' per-day rank values at all 8 thresholds (visualises
which thresholds trigger which days). Confirms:
- Threshold grid spans the expected per-day rank values (no
  pathological all-trigger or no-trigger across thresholds).
- The lagged rank values per episode are consistent with the HA01b
  per-axis diagnostic dry-run.

If the dry-run surfaces a pathology, the v2 spec is reviewed BEFORE
the full sweep.

## 6. Pre-committed decision rules (per playbook §5.1 + locked v2
criteria)

### 6.1 If both eras RESCUE (Cat 1, 2, or 3)

HA01c locked verdict graduates to load-bearing. Synthesis docs
(STOCKTAKE, synthesis.md, addendum, registry) updated with the
SUPPORTED both-eras + v2-validated verdict.

If specificity tables also pass per playbook §6.2 (a separate
required step before card.md), HA01c card.md is drafted per playbook
§2.7 (2-3 candidate variants, design-brief tone, no em-dashes).

### 6.2 If one era RESCUE, other era CLOSE

**Mixed**. The both-eras rule (playbook §4.4) blocks load-bearing.
HA01c stays "SUPPORTED-with-stability-mixed" — honest but not
load-bearing.

### 6.3 If both eras CLOSE (Cat 4 or 5)

HA01c is recorded as "SUPPORTED at locked threshold but
threshold-fragile." Same status as the HA06b case in the prior v2
round. Load-bearing is withheld pending threshold refinement or
further data.

### 6.4 v3 escape hatch (strictly bounded per locked v2 criteria
§v3)

Three conditions must hold:
1. Cat 4 close failure occurs at exactly 1 era (not both)
2. The 1 era's close failure is by exactly 1 sign-change (not ≥ 2)
3. The other era is RESCUE Cat 1/2/3 unambiguously

Even if all three hold, the result is still "CLOSE both-eras-mixed";
v3 does NOT auto-rescue, it only allows a future threshold refinement
attempt with a tighter pre-registered scope. Per locked v2 criteria
§v3 ("strictly bounded escape hatch — does not rescue, only allows
future refinement").

## 7. Caveats `result.md` must explicitly acknowledge

Per playbook §7.2 and §6.1:

- **Channel non-independence** (per playbook §6.1): single-axis
  diagnostic; within-axis monotonicity is the test.
- **Locked HA01c verdict binds**: this diagnostic does NOT change
  the locked-threshold result; it only stamps it RESCUE / CLOSE.
- **Multi-comparison context**: 8 thresholds × 2 eras = 16
  evaluations. The v2 shape rule is precisely the multi-comparison
  control (no "pick the best threshold" without shape coherence).
- **Specificity caveat (playbook §6.2)**: even if RESCUE, the HA01c
  posterior-per-fire at the locked 0.75 threshold is ~2.2% (computed
  in HA01b per-axis diagnostic result.md §6.4) — barely above the
  1.7% base rate. The v2 diagnostic does NOT address specificity
  directly; if a higher threshold (e.g., 0.90) shows acceptable
  discrimination AND better specificity at lower trigger rates, that
  is a finding for card.md design, not for the locked HA01c verdict.
- **No-go surfaces (playbook §6.6)**: even RESCUE does not unlock
  push notifications, traffic lights, crash-risk percentages, or
  any forbidden surface. Card design is reflective-only.

## 8. Outputs

- `result-data.json`: 8-threshold × 2-era discrimination table + shape
  categorisation per era + sign-change count + peak τ + peak_disc.
- `result.md`: per-era verdict per the locked five-category rule,
  shape rationale, multi-comparison context, specificity reminder.

## 9. Status

- **Pre-registered**: 2026-06-07
- **Triggered by**: HA01b per-axis diagnostic finding (effective_exertion
  both-eras SUPPORTED at locked threshold)
- **Result expected**: after HA01c locked-threshold test runs AND
  this v2 diagnostic runs (sequential; HA01c result locks before v2
  result evaluates)

---

*HA01c v2 threshold-monotonicity diagnostic pre-registration locked
2026-06-07 per testing playbook §9. Uses the same five-category
shape rule that HA10/HA07d/HA06b/HA11 used in the prior v2 round.*
