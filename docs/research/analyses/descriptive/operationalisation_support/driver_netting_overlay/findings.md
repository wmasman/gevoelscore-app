# Findings - R20 driver-netting overlay (net-of-citalopram re-read of the scorecard)

**Strand A operationalisation-support analysis** - applies the locked section 5.B
dose-adjusted-predictor recipe from
[`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md)
as a **descriptive overlay** on the R14 single-pool verdicts. Producer-mode
assembly for site request **R20** ("net-of-drivers re-read"), scoped by the R18
triage [`methodology/hypothesis_retest_triage.md`](../../../../methodology/hypothesis_retest_triage.md)
section 4, which reduced R20 to "overlay numbers on the driver-exposed rows;
none changes a verdict". Drafted 2026-07-06 by Claude (Opus 4.8), producer-mode,
for the participant-researcher (repo owner).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

**Discipline binding**: Layer 1 descriptive overlay per
[CONVENTIONS section 2.1](../../../../CONVENTIONS.md). This applies an
already-locked framework (the section-5.B dose-adjustment); it does NOT lock a
new methodology choice (no section 2.2 event) and does NOT re-lock any HA verdict
(the locked `result.md` files are unchanged, as are the R14 single-pool verdicts).
Overlay numbers are reported as **numbers, not narrative**. The netted figure is a
transparency layer: the claim is only that a driver-netted number does not flip a
NOT-SUPPORTED row to SUPPORTED, nor unseat the one SUPPORTED row.

**Reproducibility**: [`run.py`](run.py) imports the R14 operand machinery verbatim
from the sibling [`single_pool_reanchor/run.py`](../single_pool_reanchor/run.py),
so the RAW single-pool column below reproduces
[`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md)
**byte-for-byte** (a built-in correctness gate). The only new quantity is the
netted column, computed by injecting a section-5.B adjusted channel into the
master and dispatching it through the same low-level trigger builders the locked
operands use. Full Stratum 4 single pool (2022-09-03 to 2026-06-05, n_days=1372,
n_crash_episodes=29); block-permutation null E[L]=7, B=10,000, perm/bootstrap seed
`20260624`; null windows seeded `20260605`.

---

## 1. Headline

**Netting the citalopram driver out of the scorecard changes zero verdicts, and
the load-bearing rows are numerically immovable.** Three facts, in order of
strength:

1. **Only one of the seven scorecard rows even uses a channel carrying a locked
   citalopram beta.** That row is HA07c (`stress_mean_sleep`, the one CONFIRMED
   mean channel that appears in a scorecard operand). The other four
   driver-exposed rows (H02b, HA11, HA10, HA06b) are *family-adjacent*: their
   channels (`max_spike_minutes`, `u_dip_count`, `bb_highest`, `resting_hr`) are
   NOT among the three CONFIRMED dose-modulated mean channels, so there is no
   per-mg coefficient to subtract. There is very little dose exposure in the
   scorecard to net in the first place.
2. **On the CONFIRMED channel, the netting is immovable.** HA07c's dose-netted
   discrimination is **+10.8 pp, identical to the raw +10.8 pp to two decimals**
   (delta = +0.000 pp): the section-5.B correction did not flip a single trigger,
   so the CI and permutation p are byte-identical too. Its off-scorecard sibling
   HA08c (same channel, slope operator) is likewise identical at the point
   estimate (+13.4 pp; CI moves less than 0.4 pp). Both are **difference
   operators** (night-over-night delta / trailing-5d slope), and a slowly-varying
   dose contributes essentially nothing to a day-over-day difference.
3. **The one SUPPORTED row does not rest on a dose-modulated channel.** HA07d is
   on the stress *variability* (stdev) channel: mean-shift-invariant by
   construction, empirically citalopram-flat (buildup delta +0.08), no beta to
   subtract. It is unnettable-and-robust.

The R18 triage predicted "overlay-only, no verdict change". R20 confirms that with
computed numbers and sharpens it: the scorecard barely touches a dose-modulated
channel at all, and where it does, the delta-operator structure makes it
dose-immovable.

---

## 2. The overlay table

Net recipe (section 5.B): `channel_adj(d) = channel(d) - beta * dose_plasma_mg(d)`,
with `beta` the locked buildup beta and `dose_plasma_mg` the canonical
per_day_master PK-smoothed plasma proxy (0 unmedicated, ramped over buildup, 30mg
plateau in consolidation, ramped down over afbouw). "raw" reproduces R14; "netted"
is the overlay. `disc pp` = crash-minus-null trigger-rate discrimination in
percentage points; the pre-reg SUPPORTED bar needs disc >= +15 pp (crit b) among
its three criteria.

| row | scorecard | channel | operator | beta (per mg) | raw disc pp (CI95) | netted disc pp (CI95) | delta | verdict raw -> netted |
|---|---|---|---|---:|---:|---:|---:|---|
| **HA07c** | yes | `stress_mean_sleep` | delta, signed z | **+0.43** (CONFIRMED) | +10.8 [-22.5, +20.7] | +10.8 [-22.5, +20.7] | **+0.0** | NOT-SUPPORTED -> NOT-SUPPORTED |
| HA08c | no (sibling) | `stress_mean_sleep` | 5d slope, signed z | **+0.43** (CONFIRMED) | +13.4 [-20.7, +22.3] | +13.4 [-21.1, +22.4] | **+0.0** | NOT-SUPPORTED -> NOT-SUPPORTED |
| **HA06b** | yes | `resting_hr` | level, \|z\| | +0.03 (weak, n.s.) | +6.7 [-18.7, +17.9] | +8.5 [-18.7, +18.7] | +1.8 | NOT-SUPPORTED -> NOT-SUPPORTED |
| **HA07d** | yes | `stress_stdev_sleep` | delta, \|z\| | none (variability) | +19.7 [-18.1, +17.0] | -- (unnettable) | -- | SUPPORTED (unchanged) |
| **H02b** | yes | `max_spike_minutes` | count delta, threshold | none | +3.5 [-21.2, +21.7] | -- (unnettable) | -- | NOT-SUPPORTED (unchanged) |
| **HA11** | yes | `u_dip_count` | level, signed z | none | +16.8 [-22.4, +20.4] | -- (unnettable) | -- | NOT-SUPPORTED (unchanged) |
| **HA10** | yes | `bb_highest` | level, \|z\| | none | +4.1 [-16.5, +16.8] | -- (unnettable) | -- | NOT-SUPPORTED (unchanged) |

The seven scorecard rows are HA07c, H02b, HA11, HA10, HA06b, HA07d, and HA01b
(HA01b is NOT driver-exposed - activity/exertion is not citalopram-modulated - so
it carries no netting and is omitted here; its raw single-pool verdict
NOT-SUPPORTED stands). HA08c is off-scorecard and shown as a same-channel sibling.

---

## 3. Reading the three tiers

### 3.1 Tier 1 - CONFIRMED channel, dose-immovable (HA07c; sibling HA08c)

HA07c is the only scorecard operand that touches a locked-beta channel. Its
operand is `max signed z over the 4-day lead-up of the night-over-night delta of
stress_mean_sleep`. The section-5.B correction subtracts `0.43 * dose_plasma_mg`
from the channel; the night-over-night delta of that correction is
`0.43 * (dose_plasma_mg(d) - dose_plasma_mg(d-1))`, which is **exactly 0 on every
unmedicated and consolidation day** (flat dose) and small on the roughly 150
buildup / afbouw ramp days. On this crash-plus-null window set the correction did
not push a single max-z across the 1.5 trigger threshold: every trigger bit is
unchanged, so `frac_crash` (0.600), `frac_null` (0.492), the discrimination
(+10.8 pp), the bootstrap CI, and the permutation p (0.2148) are all identical to
the raw single-pool run. HA08c (trailing-5d OLS slope, also a difference operator)
behaves the same way - point estimate identical at +13.4 pp, with a sub-0.4-pp CI
wobble that confirms the netting is "live" but immaterial. **Difference operators
on a slowly-varying dose are structurally insulated from the dose confounder.**
Both stay NOT-SUPPORTED (crit b fails: disc below +15 pp).

### 3.2 Tier 2 - weak / non-significant beta, level operator (HA06b)

HA06b (`resting_hr`, bidirectional |z| on the level) carries only the weakly
consistent, non-significant citalopram beta (+0.03/mg, CI spans 0). Applied as a
sensitivity, it moves the discrimination by +1.8 pp (from +6.7 to +8.5 pp) - and
notably **upward**, because a level operator (unlike a difference operator) does
take the dose level directly, and netting is not guaranteed to weaken a signal.
The verdict is unchanged: +8.5 pp is still far below the +15 pp bar, still
NOT-SUPPORTED. Two caveats keep this in proportion: (a) the beta is
non-significant, so this is "even applying the weak point estimate, nothing
flips"; (b) resting_hr's real confounder is not citalopram but the slow
deconditioning / weight / aging drift owned by R30, and HA06b's operand already
z-scores against a [d-90, d-30] lagged local baseline that detrends anything
slower than about 60 days, absorbing most of that drift before the operand sees
it.

### 3.3 Tier 3 - no beta, not directly nettable (HA07d, H02b, HA11, HA10)

These four rows use channels that are not among the three CONFIRMED
dose-modulated mean channels, so there is no per-mg coefficient to subtract:

- **HA07d** (`stress_stdev_sleep`, the only SUPPORTED row): a *variability*
  channel. It is mean-shift-invariant by construction (subtracting any smooth
  mean shift, dose-driven or otherwise, from the underlying series does not change
  the standard deviation of its night-over-night deltas), and it was empirically
  citalopram-flat (buildup delta +0.08). The scorecard's single green light rests
  on no dose-modulated channel.
- **H02b** (`max_spike_minutes`): a per-minute spike-count. Dose modulates the
  stress *mean level*, not the within-day count of spike-minutes; `all_day_stress_avg`
  carries a beta but is a different channel and does not appear in this operand.
- **HA11** (`u_dip_count`): a count of within-day low-motion U-dips. Same logic -
  dose modulates the mean level, not the dip count.
- **HA10** (`bb_highest`): the morning body-battery peak. The CONFIRMED
  body-battery channel is `bb_lowest` (the overnight floor, beta -1.13/mg), a
  different channel; there is no beta for the morning peak, and borrowing the
  floor's coefficient for the peak would be wrong.

All four raw verdicts stand.

---

## 4. What this closes for the driver-ledger loop

- **R20 delivered as a transparency layer, not a re-scoring.** Zero of the seven
  scorecard verdicts change under the section-5.B dose-adjustment. The R18 triage
  called this outcome in advance; R20 backs it with computed numbers.
- **The scorecard's dose exposure is smaller than the "five driver-exposed rows"
  framing suggested.** Only one scorecard row (HA07c) is directly nettable; three
  more are family-adjacent with no coefficient, and the fifth (HA06b) carries only
  a non-significant beta. So most of the driver-ledger concern was already
  structural rather than empirical.
- **The one SUPPORTED signal is confirmed driver-robust by numbers, not just
  reasoning.** HA07d does not touch a dose-modulated channel; HA07c and HA08c (the
  rows that DO touch one) are immovable under netting.
- **Handoff to R30.** The absolute-level slow-confounder surface for `resting_hr`
  (and stress / body-battery levels along the recovery-phase strip) is a different
  question from this binary crash-discrimination overlay and remains R30's; R20
  netted only the citalopram driver.

---

## 5. Caveats per CONVENTIONS section 4.1 + section 4.2

- **Descriptive overlay, no causal claim** (section 4.1). The netted numbers
  characterise the same locked operand evaluated on a dose-adjusted channel; they
  do not claim a causal structure. No falsification bar is introduced here.
- **No re-lock** (train_validate_split_fate.md section 5.7 spirit). The locked HA
  `result.md` files and the R14 single-pool verdicts are unchanged; this overlay
  adds numbers, not verdicts.
- **Verdicts, not effect sizes.** The overlay claim is that netting does not flip
  a NOT-SUPPORTED row to SUPPORTED nor unseat the SUPPORTED row. A netted point
  estimate can still shift (HA06b: +1.8 pp); the shift stays within-verdict.
- **beta choice** (section 5.B). The buildup beta (+0.43 for stress_mean_sleep,
  the tighter-CI anchor) is used per the framework default; the framework's
  buildup-vs-afbouw magnitude asymmetry is a flagged, out-of-scope tradeoff and
  does not affect this overlay's conclusion (HA07c is immovable regardless of the
  beta magnitude, because its delta operator zeroes the correction on flat-dose
  days).
- **Weak-beta sensitivity is illustrative.** HA06b's +0.03/mg is non-significant;
  its netted number is shown to demonstrate that even a live level-operator
  netting does not change the verdict, not to assert a real dose effect on RHR.
- **n=1 throughout; single-pool primacy.** Any era or dose-phase difference is a
  number with wide error, never a verdict.

---

## 6. Verification log

- **Raw-column reproduction gate**: all seven raw single-pool disc_pp reproduce
  [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md)
  exactly (HA07c +10.8, HA08c +13.4, HA06b +6.7, HA07d +19.7, H02b +3.5,
  HA11 +16.8, HA10 +4.1). The R20 harness imports the R14 operand functions
  directly, so any drift would surface as a raw-column mismatch.
- **Netted betas**: stress_mean_sleep +0.43/mg (CONFIRMED buildup beta),
  resting_hr +0.03/mg (weak sensitivity), per
  `citalopram_phase_stratification.md` section 2. `dose_plasma_mg` read from the
  canonical per_day_master column (0 nulls across 1372 Stratum-4 days;
  0 unmedicated / 30 consolidation / ramped in buildup + afbouw).
- **Surface**: full Stratum 4 single pool, 2022-09-03 to 2026-06-05, n_days=1372,
  n_crash_episodes=29. Null windows n=200 (4d and 3d leadups) seeded `20260605`;
  block-permutation null + stationary bootstrap CI at E[L]=7, B=10,000, seed
  `20260624`.
- **Netted deltas (disc pp)**: HA07c +0.000, HA08c +0.000 (point estimate),
  HA06b +1.795. No verdict changes.
- **Operand-source path**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`
  + `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv`.
- **Machine-readable**: `result-data.json` (gitignored per the
  `docs/research/**/*.json` rule).

---

## 7. Cross-references

- **Framework applied**: [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md)
  section 2 (per-channel confirmed betas) + section 5.B (dose-adjusted predictor).
- **Empirical anchor for the betas**: `methodology/citalopram_dose_response_stress_mean_sleep.md`
  section 5.6 (v3 multi-channel confirmation).
- **Raw single-pool source (reproduced here)**: [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md)
  (R14).
- **Scope + prediction**: [`methodology/hypothesis_retest_triage.md`](../../../../methodology/hypothesis_retest_triage.md)
  section 4 (R18; "R20 reduces to overlay numbers").
- **Slow-confounder surface (handed off, not netted here)**: `analyses/longrun_rhr_trend/`
  and site R30.
- **Scorecard verdicts + tiers**: `analyses/garmin_exploration/cards/trust-panel-export.md`,
  `cards/primary-verdict-statistics.md`.
- **Site register R20** (this deliverable); R14 / R18 / R30. External repo
  `wiggers_research_story`, `docs/research-requests.md`.

---

*End of findings.*
