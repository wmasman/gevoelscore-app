# HA01b per-axis decomposition diagnostic — result

**Run date**: 2026-06-07. **Test script**: [test.py](test.py).
**Pre-registration**: [diagnostic.md](diagnostic.md), locked 2026-06-07
per testing playbook
([../../methodology/testing-playbook.md](../../methodology/testing-playbook.md))
section 9 compliance checklist. **Output data**:
[result-data.json](result-data.json).

## TL;DR

The composite `exertion_class` REFUTED verdict was hiding a per-axis
signal. Decomposed into its 4 input axes, **effective_exertion is
SUPPORTED in both eras** at the locked bar (train +21.3 pp, validate
+19.5 pp; freq 80-82%; median rank on triggering 0.88-0.91). Two more
axes (step_burden, vigorous_min) clear the bar in validate only.
max_hr_peak is REFUTED both eras.

The composite control reproduces HA01b's REFUTED both-eras verdict
(+3.4 train, +1.5 validate pp), confirming the per-axis decomposition
is honestly extracting signal the composite obscured.

The locked HA01b composite REFUTED verdict stays on record. This
diagnostic produces a **diagnostic finding**, not a re-test verdict,
per playbook section 5.2. The diagnostic finding triggers HA01c
pre-registration (effective_exertion-as-primary) + v2
threshold-monotonicity diagnostic.

## Section 1: Decision-rule branch

Per [diagnostic.md section 6](diagnostic.md) the per-axis SUPPORTED
count selects the branch.

| era | effective_exertion | step_burden | max_hr_peak | vigorous_min |
|---|---|---|---|---|
| train    | **SUPPORTED** (+21.3) | refuted (crit-c miss) | refuted | refuted (crit-b miss) |
| validate | **SUPPORTED** (+19.5) | **SUPPORTED** (+16.6) | refuted | **SUPPORTED** (+24.6) |

Per-axis SUPPORTED count: 4 (across the 8 axis × era cells).

**Branch selected**: section 6.3 (MULTIPLE axes SUPPORTED).

**Both-eras rule (playbook section 4.4) reduces load-bearing axes to 1**:
- **effective_exertion** clears the bar in both eras and is the only
  axis that survives the both-eras gate.
- step_burden and vigorous_min are SUPPORTED in validate only and
  treated as diagnostic findings, NOT load-bearing.
- max_hr_peak fails in both eras and is decisively REFUTED.

## Section 2: Per-axis result table

All 4 axes × 2 eras (8 cells). Locked bar per
[diagnostic.md section 4.5](diagnostic.md):

- (a) crash trigger frequency >= 60%
- (b) discrimination >= +15 pp above null
- (c) median rank on triggering episodes >= 0.875

### 2.1 effective_exertion (`effective_exertion_rank_lagged`)

| era | n_clean | freq | null_freq | disc | median_rank | crit (a) | crit (b) | crit (c) | verdict |
|---|---:|---:|---:|---:|---:|:-:|:-:|:-:|:-:|
| train    | 11 | 81.8% | 60.5% | **+21.3 pp** | 0.883 | PASS | PASS | PASS | **SUPPORTED** |
| validate | 15 | 80.0% | 60.5% | **+19.5 pp** | 0.909 | PASS | PASS | PASS | **SUPPORTED** |

**Reading**: UDS passive intensity + recorded activity duration
combined. In ~80% of crash lead-ups (both eras) at least one of the
4 lead-up days had effective_exertion in the heavy+ rank (>= 0.75 vs
the lagged baseline). Null rate is 60.5%, so the spread is ~20 pp in
both eras. This is the strongest per-axis signal.

### 2.2 step_burden (`step_rank_lagged`)

| era | n_clean | freq | null_freq | disc | median_rank | crit (a) | crit (b) | crit (c) | verdict |
|---|---:|---:|---:|---:|---:|:-:|:-:|:-:|:-:|
| train    | 11 | 90.9% | 63.5% | +27.5 pp | 0.867 | PASS | PASS | **fail** | refuted |
| validate | 15 | 80.0% | 63.5% | +16.6 pp | 0.875 | PASS | PASS | PASS | **SUPPORTED** |

**Reading**: Total daily steps. Train discrimination is the highest
of any axis × era cell (+27.5 pp) BUT the median rank on triggering
episodes is 0.867, just below the locked 0.875 floor (an 0.008 miss).
This is a fail-by-floor, not a fail-by-discrimination. The locked bar
binds.

### 2.3 max_hr_peak (`max_hr_rank_lagged`)

| era | n_clean | freq | null_freq | disc | median_rank | crit (a) | crit (b) | crit (c) | verdict |
|---|---:|---:|---:|---:|---:|:-:|:-:|:-:|:-:|
| train    | 11 | 81.8% | 74.5% | +7.5 pp | 0.867 | PASS | **fail** | **fail** | refuted |
| validate | 15 | 66.7% | 74.5% | **-7.7 pp** | 0.909 | PASS | **fail** | PASS | refuted |

**Reading**: Daily max HR. Decisively refuted both eras. The validate
era is INVERTED (less likely to trigger before a crash than in a null
window). This makes physiological sense: chronotropic incompetence
in ME/CFS (>85% prevalence per pacing-and-crash-mitigation literature)
blunts the HR response.

### 2.4 vigorous_min (`vigorous_min_rank_lagged`)

| era | n_clean | freq | null_freq | disc | median_rank | crit (a) | crit (b) | crit (c) | verdict |
|---|---:|---:|---:|---:|---:|:-:|:-:|:-:|:-:|
| train    | 11 | 72.7% | 62.0% | +10.7 pp | 0.887 | PASS | **fail** | PASS | refuted |
| validate | 15 | 86.7% | 62.0% | **+24.6 pp** | 0.917 | PASS | PASS | PASS | **SUPPORTED** |

**Reading**: Recorded vigorous-intensity duration. Strong validate-era
spread (+24.6 pp) but train is weak (+10.7 pp, below the +15 pp bar).
Era-split, suggesting the activity-type composition of crash precursors
shifted across the train/validate boundary.

## Section 3: Composite control

Same 200-window null sample, same 4-day lead-up, same `>=2 of 4 days
valid` rule as in script 12
([12_run_ha_tests_4day_lagged.py](../../activity-labels/scripts/12_run_ha_tests_4day_lagged.py)),
but the null sample here excludes only crash lead-up windows (not dip
windows; this diagnostic uses crash_v1 per playbook section 4.2 default).

| era | n_clean | freq | null_freq | disc | median_shock_days | verdict |
|---|---:|---:|---:|---:|---:|:-:|
| train    | 11 | 81.8% | 78.5% | +3.4 pp | 2 | refuted |
| validate | 15 | 80.0% | 78.5% | +1.5 pp | 2 | refuted |

The composite REFUTED verdict reproduces (HA01b-recomputed was
+5.8 train / +4.0 validate on script 12; the small delta reflects the
null-sample-exclusion difference noted above — script 12 also excluded
dip windows; this diagnostic does not, since it uses crash_v1 only).

**Why does the composite REFUTE while effective_exertion SUPPORTS?**
The composite is `exertion_class = heavy+` IF max-rank across 4 axes
>= 0.75. Both crashes and nulls hit this threshold at ~80% rate.
Taking the MAX across 4 axes makes the composite very easy to trigger;
the per-axis signal is diluted in the null distribution. When you ask
"is THIS specific axis elevated," the null rate drops to ~60% and
crashes still hit 80% → discrimination ~+20 pp.

**This is a clean methodological finding** about composite-vs-per-axis
testing. The MAX-rank composite trades sensitivity for over-broad
triggering. Per-axis primaries can be more discriminating.

## Section 4: Cross-axis correlation matrix

Per playbook section 6.1 (channel non-independence). N=1184 days where
all 4 axes have a valid lagged rank.

**Spearman ρ**:

|                    | effective_exertion | step_burden | max_hr_peak | vigorous_min |
|---|---:|---:|---:|---:|
| effective_exertion | 1.000 | 0.437 | 0.624 | 0.692 |
| step_burden        | 0.437 | 1.000 | 0.312 | 0.307 |
| max_hr_peak        | 0.624 | 0.312 | 1.000 | 0.588 |
| vigorous_min       | 0.692 | 0.307 | 0.588 | 1.000 |

**Pearson r** (`result-data.json` for full table): similar magnitudes
(0.30 - 0.69), no axis pair is independent and none is collinear.

**Interpretation**:
- effective_exertion is the "central" axis: highest mean correlation
  with the other 3 (mean ρ ≈ 0.58). This is by construction —
  effective_exertion_min combines UDS intensity-minutes + recorded
  activity duration, which the other 3 axes are inputs into or proxies
  for.
- step_burden is the most independent axis (mean ρ ≈ 0.35 with
  others). Steps capture movement that doesn't always show up in HR
  or vigorous-min (walking-around-the-house steps are step-positive
  but vigorous-zero, HR-stable).
- max_hr_peak and vigorous_min are moderately correlated (ρ = 0.59).

**Effective number of independent comparisons**: With Spearman
correlations 0.31 - 0.69, the effective N is approximately
1 / (1 + average pairwise ρ) × 4 ≈ 2.5 independent axes (not 4). The
multi-comparison concern (section 6 below) is real but bounded.

## Section 5: Decision-rule application (per diagnostic.md section 6)

### 5.1 Branch 6.3 (MULTIPLE axes SUPPORTED) — applies

3 axes hit SUPPORTED in at least one era (effective_exertion in both,
step_burden and vigorous_min in validate only).

Per playbook section 4.4 (both-eras rule): only effective_exertion
survives the both-eras gate. step_burden and vigorous_min are
diagnostic findings only.

### 5.2 Follow-up pre-commitments (per diagnostic.md section 6.4)

Both must complete before effective_exertion can be treated as
load-bearing in synthesis:

1. **HA01c pre-registration** with `effective_exertion_rank_lagged` as
   primary (replacing the composite). Locked at the same 3-criterion
   bar.
2. **v2 threshold-monotonicity diagnostic** per playbook section 5.1
   on effective_exertion across rank thresholds
   {0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95}. Five-category
   shape rule applies.

If both pass, effective_exertion graduates to a load-bearing
validate-era precursor — and becomes the SECOND project-level
SUPPORTED validate-era finding (after HA10's BB-recharge result).

If either fails, the per-axis finding is downgraded to "diagnostic
suggestion" and HA01c is closed without promotion.

## Section 6: Caveats this result must explicitly acknowledge

Per the diagnostic.md section 7 pre-commitments:

### 6.1 The locked HA01b composite verdict is REFUTED both eras

This diagnostic does NOT unlock that verdict. HA01b-as-pre-registered
(on the composite primary) stays REFUTED. The per-axis finding is a
diagnostic suggestion that a re-formulated hypothesis (HA01c, on
effective_exertion-as-primary) may pass. The two are not
interchangeable.

### 6.2 Multi-comparison: 8 verdicts at the locked bar

Naively 8 tests × 5% per-test = expected 0.4 false positives;
P(>=1 false positive) ≈ 33% under independence. But:
- Cross-axis Spearman 0.31-0.69 reduces effective N to ~2.5.
- effective_exertion BOTH-eras conjunction is much stronger than
  any single-era SUPPORTED (compound probability of both eras
  passing under null is much smaller than either era passing alone).
- effective_exertion's +19.5 pp validate is well above the +15 pp
  floor, not a marginal pass.

Honest framing: effective_exertion's both-eras SUPPORTED is well-supported
by the bar itself. step_burden and vigorous_min validate-only are
more vulnerable to the multi-comparison concern and are correctly
labelled "diagnostic findings, not load-bearing."

### 6.3 Channel non-independence (playbook section 6.1)

The 4 axes share underlying physical activity. "4 axes" overstates
independence (effective N ≈ 2.5 per section 4 above). The
correlation table in section 4 is the audit trail for this caveat.

### 6.4 Card specificity (playbook section 6.2)

**Critical for any downstream card framing.** Even though
effective_exertion validate discrimination is +19.5 pp (large in
relative terms), the absolute trigger rates mean:

- Null trigger rate: 60.5% — i.e., ~60% of any 4-day window in the
  analysis range has at least one effective_exertion >= 0.75 day.
- Crash trigger rate: 80%.

Validate-era posterior probability per fire (Bayes):
- Validate window ≈ 887 days, 15 crash episodes → base rate ≈ 1.7%.
- P(trigger | crash) = 0.80; P(trigger | non-crash) ≈ 0.605.
- P(trigger) = 0.605 × 0.983 + 0.80 × 0.017 ≈ 0.609.
- P(crash | trigger) = 0.80 × 0.017 / 0.609 ≈ **2.2% per fire**.

The signal is real (discrimination is real) but a card built on
this primitive would fire roughly **every other day** and only marginally
lift posterior over the 1.7% base rate. NOT shippable as a card
without further refinement (tighter threshold, multi-condition AND,
or temporal aggregation). The HA01c v2 threshold-monotonicity
diagnostic should test whether a higher threshold (e.g., rank >= 0.85
or 0.90) yields better specificity at acceptable sensitivity loss.

### 6.5 No-go surfaces (playbook section 6.6)

Even if HA01c is SUPPORTED and v2 passes, this finding must NOT be
surfaced as:
- "Crash risk percentage" (the 2.2% per-fire posterior is a Bayes
  calculation, not a personal crash-risk forecast).
- Traffic-light alerting on effective_exertion exceeding 0.75 (would
  fire ~60% of days with poor positive-predictive value).
- Push notifications on the metric (anxiety amplification with low
  PPV).
- Automated rest target derived from the rank.

The acceptable surface is reflective-only: timeline annotation of
crossings during after-the-fact review, paired with the gevoelscore
record. This is consistent with the design brief's restrained visual
cues + thumb-first reading-surface placement and the
[pem-pacing-indicators.md](../../pem-pacing-indicators.md) section 5
"What we do not build" rules.

## Section 7: Pre-registration audit trail (per playbook section 2.5)

### 7.1 Axis-name mapping

The diagnostic.md uses descriptive axis labels; the actual CSV columns
(computed by
[11_compute_lagged_baseline.py](../../activity-labels/scripts/11_compute_lagged_baseline.py))
use slightly shorter names. The physical quantities are identical:

| diagnostic.md label             | actual CSV column                  |
|---|---|
| `effective_exertion_min_rank_lagged` | `effective_exertion_rank_lagged` |
| `step_burden_rank_lagged`            | `step_rank_lagged`               |
| `max_hr_peak_rank_lagged`            | `max_hr_rank_lagged`             |
| `vigorous_min_rank_lagged`           | `vigorous_min_rank_lagged`       |

This is a cosmetic-only difference. The test script uses the actual
CSV column names; the result table per-axis section headers use the
short forms. Not a spec change per playbook section 2.2.

### 7.2 Null-sample construction (vs script 12)

This diagnostic uses crash_v1 only (default per playbook section 4.2),
so the null sample excludes only crash lead-up windows. Script 12
(HA01b-recomputed) excluded both crash AND dip lead-up windows
because it was a bundled re-test. This explains the small numeric
difference in the composite control (+3.4 / +1.5 pp here vs
+5.8 / +4.0 pp in script 12); the qualitative verdict (composite
REFUTED both eras) reproduces in both.

### 7.3 Validity rule (>=3 of 4 days valid per axis)

This is more stringent than HA01b's composite validity rule (>=2 of 4
days valid). This is because per-axis validity must hold per-axis;
relaxing to >=2 would let an axis pass on the strength of 2 days that
might not include the actual lead-up shock. With 3 of 4, we keep
~95% of validate-era events.

Train events dropped from 14 to 11 (3 lost to lagged-baseline warmup —
the first crashes of the corpus are inside the first 90 days and
lack a lagged baseline). Validate events: all 15 retained. Documented
in dry-run output.

## Section 8: Synthesis-level implications

### 8.1 Status of HA01b composite REFUTED verdict

Stays on record. Unchanged. The composite primary did not pass the
bar and the per-axis diagnostic does not unlock that verdict per
playbook section 5.2.

### 8.2 New work item triggered: HA01c pre-registration

Effective_exertion as primary, both-eras requirement, v2
threshold-monotonicity diagnostic to follow. Folder
`hypotheses/HA01c-effective-exertion-shock/`.

### 8.3 New work item triggered: v2 threshold-monotonicity diagnostic

Folder `hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/`.
Per playbook section 5.1. Tests rank thresholds
{0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95}. Five-category shape
rule applies. Will inform whether a tighter threshold improves
specificity for card purposes.

### 8.4 Composite construction lesson

For future composites: MAX-rank composites can dilute per-axis signal
in the null distribution. Consider per-axis primary tests in parallel
with the composite, or use a composite construction that conditions
on multiple axes simultaneously (AND-of-axes rather than
MAX-of-ranks).

This is a generalisable lesson about composite-vs-per-axis
pre-registration. Worth a methodology note in the playbook (queued).

### 8.5 Step_burden and vigorous_min validate-only findings

Both pass the validate-era bar but fail the train-era bar. Two
possible framings:
- *Era moderator (playbook section 6.3)*: the activity composition
  of crash precursors shifted between train and validate. Step
  burden was less precursor-discriminating in the early era;
  vigorous activity became more so in the validate era.
- *Multi-comparison artifact*: 8 verdicts at α=0.05 has expected
  ≥1 false positive ~33% under independence.

The both-eras rule blocks both from load-bearing. They are noted in
this diagnostic and not promoted to HA01c-style follow-ups.

## Section 9: Compliance verification (per playbook section 9)

All 19 items in the playbook section 9 compliance checklist were
satisfied per the diagnostic.md section 2 pre-registration. Re-verified
on completion:

- [x] Folder structure: standard `hypotheses/HA01b-per-axis-diagnostic/`
  with diagnostic.md + test.py + result.md + result-data.json
- [x] Pre-registration before data inspection: locked 2026-06-07
- [x] References playbook in all docs
- [x] Crash_v1 used (29 episodes; 14 train, 15 validate)
- [x] Default train/validate split + both-eras rule applied
- [x] Lagged baseline (script 11 columns)
- [x] Relative thresholds (rank >= 0.75; rank IS the relative)
- [x] Primary direction: one-sided elevated (locked before run)
- [x] 3-episode dry-run gate: ran (output above; no pathologies)
- [x] 3-criterion bar at locked thresholds (freq >= 60%, disc >= +15 pp,
  median rank >= 0.875)
- [x] Null sample seed `20260605`, N=200
- [x] Validity floors: >=3 of 4 lead-up days valid per axis
- [x] Decision rules → verdict categories per playbook section 2.6
  (REFUTED/SUPPORTED + diagnostic-finding framing)
- [x] Channel non-independence flagged (section 4 correlation matrix
  + section 6.3 caveat)
- [x] Multi-comparison disclosure: section 6.2
- [x] v2 threshold-monotonicity follow-up: section 5.2 (HA01c)
- [x] No-go surfaces flagged: section 6.5
- [x] Hardware constraints: none specific (UDS daily aggregates only)
- [x] Audit trail for axis-name and null-sample differences: section 7

---

*Result generated 2026-06-07. Diagnostic locked under testing playbook
v1.0.*
