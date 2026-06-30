# Findings - net-of-drivers descriptive residual re-read (R20 + R16 collapsed)

**Strand A operationalisation-support analysis.** This is a **Layer-1
descriptive residual re-read** of the Wiggers scorecard signals with the
one correction-licensed driver (citalopram) modelled out on its confirmed
channels. It is built as an overlay on the locked single_pool_reanchor
recipe (same operands, same n=29 Stratum-4 pool, same block-permutation
null E[L]=7, B=10,000, stationary-bootstrap CI, seeds 20260605 / 20260624).
The site shows each verdict as the **RESIDUAL** read with the established
driver removed.

**This is NOT a verdict re-lock.** Locked `result.md` files are UNCHANGED.
Discipline: CONVENTIONS §2.1 (descriptive-before-inference) +
train_validate_split_fate.md §5.7 number-not-narrative. No git / no audit /
no push; the site repo and locked result.md are not touched.

**The one licensed driver: citalopram, on CONFIRMED channels only**, per
[`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md)
§2 (CONFIRMED matrix) + §5.A/B/C, and
[`phase_axis_collapsibility_conventions.md`](../../../../methodology/phase_axis_collapsibility_conventions.md)
Tier B (which inherits §5.A/B/C verbatim). The §5.B dose-adjusted predictor
is applied: `channel_adj(d) = channel(d) - beta * dose_plasma_mg(d)`, then the
single-pool discrimination is re-run on the adjusted channel.

| confirmed channel | beta / mg | source |
|---|---:|---|
| `stress_mean_sleep` | +0.43 | dose_response §5.6.1 buildup post-CPAP |
| `all_day_stress_avg` | +0.57 | dose_response §5.6.1 buildup post-CPAP |
| `bb_lowest` | -1.13 | dose_response §5.6.1 buildup post-CPAP |

"stress" throughout = Garmin HRV-derived GSS (autonomic), **not** mental stress.

---

## 1. Dose series - AVAILABLE (wiring present)

The §5.B correction needs a per-day `dose_plasma_mg(d)` PK-smoothed plasma
series. **It exists and is fully materialised** in
`$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` as column
`dose_plasma_mg` (column 200):

- non-null **1372 / 1372** days in Stratum 4 (no gaps).
- range **0.0 - 30.0 mg**; 585 days at 0mg (unmedicated), 787 days > 0.
- spot-checks match the §3 phase trajectory exactly: 2023-05-15 = 0,
  2024-05-15 (mid-buildup) = 19.9, 2024-06-20 (consolidation start) = 20.0,
  2025-08-15 (plateau) = 30.0, 2026-05-01 (afbouw) = 10.0, 2026-06-01 = 8.2.

Note: `citalopram_phase_stratification.md §8.3` lists the `dose_plasma_mg`
column as QUEUED for `per_day_master.csv`. That note is **stale** - the
column has since landed and is the same PK convolution the dose-response
script produces. The wiring is present; no fabrication was needed.

---

## 2. Per-signal raw vs netted table

Deliverable shape: `{signal, raw_pp, ci, netted:[{driver, corrected_pp, ci,
method}] | null, status}`. Driver = citalopram on every netted row. All raw
numbers reproduce the locked single_pool_reanchor (HA07c +10.8, HA08c +13.4,
H02b +3.5, HA11 +16.8, HA10 +4.1, HA06b +6.7, HA01b +5.1, HA07d +19.7) -
confirming the overlay reuses the recipe faithfully.

| signal | channel | raw pp (CI95) | netted pp (CI95) | driver | method | status |
|---|---|---:|---:|---|---|---|
| **HA07c** | stress_mean_sleep | +10.8 [-22.5, +20.7] | **+10.8 [-22.5, +20.7]** | citalopram | exact §5.B, delta-primitive | netted (NOT-SUPPORTED) |
| **HA08c** | stress_mean_sleep (slope) | +13.4 [-20.7, +22.3] | **+13.4 [-21.1, +22.4]** | citalopram | exact §5.B, slope-primitive | netted (NOT-SUPPORTED) |
| **H02b** | max_spike_minutes | +3.5 [-21.2, +21.7] | **+2.5 [-22.1, +22.5]** | citalopram | §5.B APPROXIMATION (see §3) | netted (NOT-SUPPORTED) |
| **HA11** | u_dip_count (S_pre>=40 gate) | +16.8 [-22.4, +20.4] | **null** | citalopram | gate-correction NOT WIREABLE (see §3) | raw only (NOT-SUPPORTED) |
| HA07d (sensitivity) | stress_stdev_sleep | +19.7 [-18.1, +17.0] | +18.7 [-17.5, +16.3] | citalopram | §5.B on variance primitive; ~no change | sensitivity (SUPPORTED) |
| **HA10** | bb_HIGHEST | +4.1 [-16.5, +16.8] | -- | -- | not a confirmed channel | complicates (NOT-SUPPORTED) |
| **HA06b** | resting_hr | +6.7 [-18.7, +17.9] | -- | -- | not confirmed (weak) | complicates (NOT-SUPPORTED) |
| **HA01b** | exertion_class_lagged | +5.1 [-14.7, +13.3] | -- | -- | pacing, not citalopram | complicates (NOT-SUPPORTED) |

**Direction of motion** (honest read): where the correction actually bites
(H02b), the residual moves **toward null** (+3.5 -> +2.5) and the CI
**widens**, exactly as expected - removing dose-driven inflation makes the
signal weaker, not stronger. The delta/slope primitives (HA07c, HA08c) are
near-**invariant** to the correction by construction of a slow-moving dose
(empirical-given-this-PK-trajectory, not an algebraic identity; see §3). No netted
number became stronger; none crossed into SUPPORTED. Every confirmed-channel
signal was ALREADY single-pool NOT-SUPPORTED, and the correction leaves it
NOT-SUPPORTED.

---

## 3. Method note (§5.B) + per-signal wiring detail

### 3.1 §5.B dose-adjusted predictor

For each confirmed channel, `channel_adj(d) = channel(d) - beta *
dose_plasma_mg(d)` is computed over the whole master, then the locked
operand (delta / slope / threshold) is re-extracted on the adjusted column,
then the single-pool discrimination is re-run unchanged (same null set, same
E[L]=7, same B=10,000, same seeds). Per §3 zero-dose convention,
`dose_plasma_mg = 0` on unmedicated days, so `channel_adj = channel` there;
the correction acts only on the 787 medicated days.

### 3.2 HA07c / HA08c - exact correction, but near-invariant (slow-moving dose)

Both ride `stress_mean_sleep` as a continuous level, so the §5.B correction
is **exact and clean**. But the operands are a **night-over-night delta**
(HA07c) and a **trailing-5d slope** (HA08c), each z-scored against a lagged
baseline of deltas/slopes. Subtracting `beta * dose(d)` shifts the level,
but plasma dose moves slowly day-to-day, so `delta(channel_adj) =
delta(channel) - beta*delta(dose) ~= delta(channel)`, and the same shift hits
both the value and its baseline. The discrimination is therefore numerically
near-identical to raw (HA07c +10.8 -> +10.8 unchanged; HA08c +13.4 -> +13.4,
CI widens marginally [-20.7,+22.3] -> [-21.1,+22.4], p 0.1464 -> 0.1477). This
is the honest result: **a level-acting dose correction barely touches a
rate-of-change primitive**. The verdict was and remains NOT-SUPPORTED.

### 3.3 H02b - APPROXIMATION flag (unit + spike mismatch)

H02b's single-pool operand rides **`max_spike_minutes`** (a stress-spike
DURATION metric, minutes), not `all_day_stress_avg` directly. The +0.57/mg
beta is the `all_day_stress_avg` **DAILY-MEAN** beta (stress points per mg).
Applying it to a minutes metric is therefore a **double approximation**:
(a) daily-mean beta applied to a spike metric (the flag the brief calls out),
AND (b) a unit mismatch (points/mg subtracted from a minutes quantity). The
**direction** is right (remove dose-driven inflation), the **magnitude** is
indicative only. Result: +3.5 -> +2.5 (toward null), CI widens, p 0.4458 ->
0.4861. Marked APPROXIMATION; not a precise residual.

### 3.4 HA11 - gate rides stress, but correction NOT WIREABLE from master

HA11's S_pre>=40 precondition gate does ride the Garmin stress channel
(citalopram inflates stress -> the gate passes more often at higher dose ->
u_dip_count inflates). BUT the single-pool operand uses the **pre-computed
daily `u_dip_count` column**, which already has the S_pre>=40 **per-minute**
gate baked in at extraction. Dose-correcting the gate would require
re-detecting U-dips on a **dose-corrected per-minute stress series** - and
`per_day_master.csv` holds only daily aggregates (no per-minute / intraday
stress series exists). Subtracting a stress-LEVEL beta from an event COUNT is
dimensionally meaningless. **The correction is genuinely not wireable at the
gate from the master**; HA11 is reported raw-only (+16.8, NOT-SUPPORTED) with
this wiring gap stated. (Exact spec for a future fix: re-run U-dip detection
with `S_pre_adj(t) = S_pre(t) - 0.43*dose_plasma_mg(d)` on the per-minute
stress series, then recompute the daily count - requires the minute-level
stress export, not present in the master.)

### 3.5 HA07d - variance-primitive sensitivity (expect ~no change)

`stress_stdev_sleep` is a within-night standard deviation (a variance
primitive). A level-acting dose subtraction barely moves a variance; the
night-over-night delta of a std is near-invariant to a per-day level shift.
Run as a sensitivity only: +19.7 -> +18.7 (barely moves), stays SUPPORTED.
**Not a load-bearing netted number** - reported for completeness per the
brief's instruction to run it and expect ~no change. Confirmed: ~no change.

### 3.6 Complicates rows (raw only; correction NOT licensed)

| signal | channel | raw pp (CI95) | why complicates |
|---|---|---:|---|
| **HA10** | bb_HIGHEST | +4.1 [-16.5, +16.8] | rides bb_HIGHEST, **not** the CONFIRMED bb_lowest; different primitive, no licensed beta |
| **HA06b** | resting_hr | +6.7 [-18.7, +17.9] | resting_hr is weakly-consistent only (§2: +0.03/mg, p=0.34) - NOT confirmed; no correction licensed |
| **HA01b** | exertion_class_lagged | +5.1 [-14.7, +13.3] | pacing / exertion channel; not citalopram-modulated; correction never faked on a complicates channel |

No correction was faked on any complicates channel. `bb_lowest` IS confirmed
(-1.13/mg), but **no scorecard signal in this set rides bb_lowest** - HA10
rides bb_HIGHEST, a distinct channel - so the licensed bb_lowest beta has no
signal to apply to here.

---

## 4. Privacy statement

This analysis operates entirely on derived daily-aggregate physiological
primitives (Garmin GSS stress means/stdevs/counts, body-battery levels,
resting HR, exertion class, U-dip counts) and a PK-smoothed citalopram plasma
proxy, all already present in the project's `per_day_master.csv`. No raw
notes, no gevoelscore text, no minute-level location/biometric streams, and
no third-party identifiers are read or emitted. The output is N=1
single-subject descriptive statistics (discrimination percentage points and
CIs) on the participant's own corpus. No external data source is contacted.

---

## 5. Count-triples per CONVENTIONS §3.6

Per-signal named counts (n_crash_clean / n_null_clean after min-valid
gating; identical raw vs netted because dose-correction does not change
missingness):

| signal | n_crash | n_null | frac_crash (raw->net) | frac_null (raw->net) |
|---|---:|---:|---|---|
| HA07c | 25 | 189 | 0.600 -> 0.600 | 0.492 -> 0.492 |
| HA08c | 25 | 197 | 0.560 -> 0.560 | 0.426 -> 0.426 |
| H02b | 26 | 200 | 0.500 -> 0.500 | 0.465 -> 0.475 |
| HA11 | 24 | 171 | 0.583 (raw only) | 0.415 (raw only) |
| HA07d (sens) | 25 | 189 | 0.880 -> 0.880 | 0.683 -> 0.693 |
| HA10 | 26 | 199 | 0.769 | 0.729 |
| HA06b | 26 | 195 | 0.615 | 0.549 |
| HA01b | 28 | 200 | 0.821 | 0.770 |

Pool: full Stratum-4 single pool, **n_crash_episodes = 29**,
n_days = 1372, 2022-09-03 to 2026-06-05. Null sample target n=200 per
leadup-length (4d n=200, 3d n=200; per-signal effective n lower after
min-valid gating, shown above).

---

## 6. Verification log

- **Recipe reuse**: imports `single_pool_reanchor/run.py` as a module
  (`spr`); reuses `load_master`, `load_crash_episodes`, `_index_master`,
  `build_null_dates`, `evaluate_ha`, and the per-signal evaluators
  (`eval_HA07c/HA08c/H02b/HA11/HA07d/HA10/HA06b/HA01b_recomputed`) verbatim.
  Only `apply_dose_correction` (the §5.B subtraction on the channel column)
  is new.
- **Raw reproduction check**: every raw disc_pp equals the locked
  single_pool_reanchor value (HA07c +10.8, HA08c +13.4, H02b +3.5, HA11
  +16.8, HA07d +19.7, HA10 +4.1, HA06b +6.7, HA01b +5.1) -> overlay wiring
  verified correct.
- **Dose series**: `dose_plasma_mg` column, 1372/1372 non-null, [0, 30] mg,
  585 zero / 787 positive; trajectory matches §3 phases on spot-checks.
- **Confirmed betas**: stress_mean_sleep +0.43, all_day_stress_avg +0.57,
  bb_lowest -1.13 (citalopram_phase_stratification §2 / §5.6.1, buildup
  post-CPAP per §5.B).
- **Block length E[L]**: 7. **B (bootstrap/perm)**: 10,000.
  **Bootstrap/perm seed**: 20260624. **Null sample seed**: 20260605.
  **N_std primary**: 1.5. **Leadup**: 4d (HA07c/HA08c/HA11/HA10/HA06b/HA01b/
  HA07d), 3d (H02b).
- **As-of-date**: 2026-06-05. **Stratum-4 start**: 2022-09-03.
- **Inference helpers**: `analyses/_utils/inference.py`
  (`stationary_bootstrap_ci`, `permutation_pvalue`).
- **Run timestamp (UTC)**: 2026-06-30T14:41:21Z.
- **Source paths**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` +
  `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv`.
- **Locked `result.md` files**: UNCHANGED. This is a descriptive residual
  overlay, not a re-lock. No git / no audit / no push performed.
- **Machine-readable output**: `result-data.json` (gitignored per
  `docs/research/**/*.json` rule).

---

## 7. Caveats per CONVENTIONS §4.1 + §4.2

- **Descriptive residual re-read, no causal claim** (§4.1). The netted
  numbers characterise the same operand on a dose-corrected channel; they do
  NOT assert that citalopram causes the residual or that the residual is the
  "true" crash signal.
- **Single-confounder fix only** (citalopram_phase_stratification §6
  "independent obligations"). Dose-adjustment removes one measured
  time-varying confounder; serial dependence, crash-drop sensitivity, and
  spike-resolution obligations are NOT discharged by this overlay and are not
  re-run here (they live in the locked HA verdicts).
- **Crash-drop on the betas themselves** (§3.4 disclosure pointer): the
  +0.43/+0.57/-1.13 dose-response betas are regressions on PEM-pacing channels,
  so their own §3.4 crash-drop sensitivity is owned upstream by
  `citalopram_dose_response_stress_mean_sleep.md` (the dose-response MD), not by
  this overlay. This overlay applies the locked betas; it does not re-estimate
  them, so the crash-drop diagnostic on the betas is cited there, not repeated here.
- **Buildup-beta choice** (§5.B tradeoff): the buildup post-CPAP beta has
  tighter CIs but was estimated on a dose-naive system and may overcorrect at
  steady-state. Since the corrections here barely move the delta/slope
  primitives anyway, this tradeoff is not load-bearing for the conclusions.
- **Netted CIs widen** relative to raw wherever the correction acts (visible
  on HA08c, H02b, HA07d) - reported as such.
- **HA11 gate correction is genuinely unwireable** from the master (§3.4);
  the +16.8 raw is the only available number for HA11 at this layer.
- **H02b is an approximation** (§3.3), not a precise residual.
- **Locked verdicts unchanged**; user-owned decision on any follow-up.

---

*End of findings.*
