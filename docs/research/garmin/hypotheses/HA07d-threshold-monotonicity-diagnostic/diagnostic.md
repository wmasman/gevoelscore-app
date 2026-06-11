# HA07d threshold-monotonicity diagnostic — pre-registration

**Pre-registration written 2026-06-07 in response to the HA10
threshold-monotonicity diagnostic CLOSE verdict.** HA10's
diagnostic closed because the bidirectional primary's
discrimination peak landed at N_std=1.75 instead of inside the
locked rescue window [1.0, 1.5]. The project methodology playbook
now requires this diagnostic on any test where the primary verdict
SUPPORTED at the loosest threshold tier and where the synthesis-
level framing leans on the verdict as load-bearing.

**HA07d is the project's first overall-SUPPORTED test** (train AND
validate both SUPPORTED at primary 4d bidirectional N_std=1.5).
HA07d is the SOLE load-bearing validate-era anchor after HA10's
diagnostic CLOSE. **HA07d must therefore pass the same
threshold-monotonicity diagnostic** before its overall-SUPPORTED
finding is treated as the project's central result in synthesis-
level docs.

This diagnostic is a positive control: HA07d's locked verdicts
showed SUPPORTED at multiple threshold tiers already (train at
N_std=1.5 AND 2.0; validate at N_std=1.5 with one-sided lowered
extending to +28.5 pp at N_std=2.0). A clean diagnostic should
confirm robust shape across the fine grid. A CLOSE verdict would
materially undermine the project's overall-SUPPORTED claim.

The diagnostic produces a rescue/close/ambiguous label per era for
HA07d's bidirectional primary. The locked primary verdict
(SUPPORTED both eras at +19.6 / +21.7 pp) stays on record
regardless of the diagnostic outcome — pre-registration discipline.
The diagnostic informs synthesis framing only.

## Honesty caveat on pre-registration timing

HA07d's discrimination values at N_std = 1.5 / 2.0 / 2.5 have
already been computed and inspected. A strict pre-registration on
the same N_std grid would be tainted by that prior inspection.

This diagnostic therefore pre-registers two things that are NOT
direct restatements of values already seen:

1. **Shape criteria** (peak location, decay ratios, Spearman
   monotonicity, sign-changes count) — testable claims about the
   SHAPE of the discrimination-vs-threshold curve, independent of
   the specific N_std=1.5 value.

2. **Fine-grid intermediate values** at N_std ∈ {0.5, 0.75, 1.0,
   1.25, 1.75, 2.25, 2.75, 3.0, 3.5, 4.0} — these have not been
   computed for HA07d and are genuinely unseen.

Same locked criteria as the [HA10 diagnostic](../HA10-threshold-monotonicity-diagnostic/diagnostic.md)
are applied to both eras (per project methodology playbook). The
criteria were locked in the HA10 diagnostic before HA07d was
pre-registered — i.e. the rescue/close shape thresholds were
fixed by the HA10 case and inherit no HA07d-specific adjustment.

## 1. Data sources

- Identical to HA07d: per-night sleep stress STDEV from
  [sleep_stress_extract/sleep_stress_nightly.csv](../../scripts/sleep_stress_extract/sleep_stress_nightly.csv)
  (1707 valid nights). Same lagged baseline machinery, same null
  sample seed `20260605`, same lead-up windowing.
- Same N_std grid as the HA10 diagnostic: 13 tiers from 0.5 to 4.0.

## 2. Measurement protocol

Identical to the HA10 diagnostic but with sleep stress STDEV night-
over-night delta as the primitive (per HA07d hypothesis.md). For
each N_std tier:

- Crash trigger frequency (per era).
- Null trigger frequency.
- Discrimination (crash − null, pp).
- Median magnitude on triggering crashes.
- Verdict under the locked HA07d bar.

For three direction modes: bidirectional (HA07d's locked primary),
one-sided elevated, one-sided lowered.

## 3. Shape statistics

Computed for each (era, direction) pair, identical to HA10
diagnostic:

- **Peak N_std** and value.
- **Decay-from-peak**: discrimination at peak+0.5 / peak value.
- **Spearman rho (N_std, discrimination)**: monotonicity test.
- **Sign-changes count**: discrimination sign changes across grid.

## 4. Pre-committed rescue / close / ambiguous criteria

Same criteria as the HA10 diagnostic (project methodology
playbook), applied independently to HA07d train AND validate
4d bidirectional primary verdicts.

### RESCUE (HA07d's era-specific primary was robust)

All of:

- **Peak at N_std ∈ [1.0, 1.5]** (signal is broad-tail, not
  loose-tail).
- **Discrimination ≥ +10 pp at N_std = 2.0** (gentle decline).
- **Discrimination ≥ +5 pp at N_std = 2.5** (signal survives into
  strict tier).
- **Spearman rho ≤ −0.3** (monotonically declining).
- **Sign-changes count ≤ 1** (no non-monotonic peaks).

### CLOSE (HA07d's era-specific primary was loose-tail noise)

Any of:

- **Peak at N_std > 1.5** or **< 0.75** (signal not centered in
  expected window).
- **Discrimination < +5 pp at N_std = 2.0** (cliff).
- **Discrimination < 0 pp at N_std = 2.5** (signal reverses).
- **Spearman rho > −0.1** (not monotonic).
- **Sign-changes count ≥ 2** (bumpy / non-monotonic).

### AMBIGUOUS

Default if neither rescue nor close criteria fully met.

## 5. Stakes per era

### If validate-era passes RESCUE

HA07d's locked overall-SUPPORTED status remains the project's
central finding. Card (b2) ships anchored on HA07d validate; the
sole-load-bearing-anchor framing established after the HA10
diagnostic stays in place. Validate-era picture is robust.

### If validate-era closes per locked rule

This would be **a material finding requiring substantial doc
revision**. HA07d's locked verdict stays on record per
pre-registration discipline, but:
- The project would have **NO load-bearing validate-era anchor**
  after both HA10 and HA07d-validate close.
- Card (b2) loses its anchor; cannot ship.
- The era-as-moderator narrative weakens (era reversal would
  hold on the train-supported side only).
- The validate-era picture would revert to "precursor-invisible
  on all clean-methodology tests" — same conclusion as before
  HA10 and HA07d landed.

### If train-era passes RESCUE

HA07d remains the seventh train-era SUPPORTED finding under clean
methodology. The train-era six-channel convergence narrative
continues.

### If train-era closes per locked rule

HA07d train SUPPORTED stays on record. Train framing demotes
HA07d from "load-bearing" to "consistent with other train
findings on the sleep-stress channel". HA07c / HA08c remain
robust train-era findings on the same channel. The
six-train-channels narrative stays.

## 6. Process

Same as the HA10 diagnostic — pre-register locked criteria
before fine grid is computed; run test.py; apply locked rule;
write result.md; propagate to synthesis-level docs per the
rescue/close outcome.

## 7. What this produces

- `result-data.json` with full 13-tier × 3-direction × 2-era table.
- ASCII discrimination-vs-threshold curves.
- Pre-committed verdict per era for HA07d's bidirectional
  primary.
- Registry §4b entry; synthesis update per locked rule.

---

*Pre-registration locked 2026-06-07. Same null seed `20260605` as
HA07d. Outcome binds the framing in STOCKTAKE / synthesis /
addendum / pem-pacing-indicators per the rescue/close criteria.*
