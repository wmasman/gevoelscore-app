# Hypothesis re-test triage: what actually moves under the reframe (R18)

**Status**: producer-mode **assembly** for site request **R18**, which *governs
scope* for the scorecard / driver-ledger reframe cluster (R14 / R19 / R20). Its job
is to make the **short list of genuine re-runs** explicit and auditable, so
"we did not redo everything" is a documented decision, not a gap. Synthesis of
existing closed results, not new analysis. Drafted 2026-07-06 by Claude (Opus 4.8),
producer-mode, for the participant-researcher (repo owner).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

## 1. The three failure modes (per hypothesis)

For each scorecard hypothesis, does the descriptive backdrop disturb its verdict?

- **(a) split-dependent** -- did the verdict lean on the retired 2023-12-31
  train/validate contrast? **Resolved for all seven**: the scorecard verdicts in
  `cards/trust-panel-export.md` are already the **single-pool** re-run (R14, all 29
  crashes, permutation null + bootstrap CI). So flag (a) fires nowhere; the
  train/validate contrast survives only as an optional descriptive overlay
  ("a number, not a narrative").
- **(b) driver-exposed** -- does the signal touch an *established* driver not yet
  netted out? The load-bearing CONFIRMED citalopram-dose-modulated channels are the
  three **means**: `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`
  (`methodology/citalopram_phase_stratification.md` sections 2/4; mandatory
  correction only on those). `resting_hr` is additionally slow-confounder-exposed
  (deconditioning / weight / aging; R30).
- **(c) shape-assuming** -- did the test assume a monotone / linear felt-to-signal
  relation that the shape-not-linear finding calls into question? **N/A for the
  scorecard**: these are binary crash *discriminators* (mostly bidirectional /
  outlier framings), not felt-state regressions. Flag (c) applies to the
  felt-to-stress *curve* (HA-C3), which is a separate, non-scorecard hypothesis
  handled by R21 / R22.

## 2. The triage table

`action` in {no-change, overlay-only, needs-rerun}. `overlay-only` = report the
driver-netted number as an overlay (R20) but the verdict does not change, because
the signal is already NOT-SUPPORTED and driver-netting can only widen CIs / weaken a
signal, never rescue a null.

| hypothesis | construct | single-pool verdict | rests on | flags | action |
|---|---|---|---|---|---|
| **HA07d** | sleep stress **variability** (stdev delta, bidir) | **SUPPORTED** (PPV 2.71%, lift 1.28x, Tier C) | single-pool discrimination on the **stdev** channel | none load-bearing -- **NOT a CONFIRMED (mean) channel**; stdev is mean-shift-invariant and was citalopram-flat (buildup delta +0.08) | **no-change** |
| HA07c | sleep stress **mean** delta (elevated) | NOT-SUPPORTED | single-pool discrimination on `stress_mean_sleep` | (b) CONFIRMED-driver-exposed | overlay-only |
| H02b | per-minute stress-spike count (3d) | NOT-SUPPORTED | single-pool discrimination on all-day stress spikes | (b) driver-exposed (stress family) | overlay-only |
| HA11 | within-day U-dip count | NOT-SUPPORTED | single-pool discrimination on `stress_low_motion` | (b) driver-adjacent (stress family, not CONFIRMED-3) | overlay-only |
| HA10 | morning BB peak z (bidir) | NOT-SUPPORTED | single-pool discrimination on morning body-battery | (b) driver-adjacent (BB family) | overlay-only |
| HA06b | RHR z-score (bidir) | NOT-SUPPORTED | single-pool discrimination on `resting_hr` | (b) weak-citalopram + slow-confounder-exposed (R30) | overlay-only |
| HA01b | exertion-class lead-up (heavy/very-heavy) | NOT-SUPPORTED | single-pool discrimination on activity/exertion | none (activity is not citalopram-modulated) | **no-change** |
| HA01c | single-axis effective-exertion shock (off-scorecard) | SUPPORTED, not load-bearing (Tier C, ~1-in-45) | single-pool R14 re-anchor; withheld on threshold-monotonicity | none load-bearing (activity) | no-change |
| C4b / HA-C4b | rest-stress low-motion minute count | NOT-SUPPORTED (v3, n=10) | the "n=9 genuinely-open" concern was a spec-design asymmetry that v3 closed by restoring 2023-02-04 (n=10) | resolved | **honest-close** (off-scorecard) |

## 3. The headline: the short list of genuine re-runs is empty

**No scorecard hypothesis requires a re-run.** Concretely:

- **flag (a) fires nowhere** -- the scorecard is already single-pool (R14).
- **the NOT-SUPPORTED rows cannot be rescued** by driver-netting (it only widens
  CIs), so their driver-exposure is at most an **overlay** (R20), never a verdict
  change.
- **the one SUPPORTED signal, HA07d, is driver-robust** -- it lives on the sleep
  stress *variability* (stdev) channel, which is NOT one of the three load-bearing
  CONFIRMED (mean) channels, is mean-shift-invariant by construction, and was
  empirically citalopram-flat. So the scorecard's single green light does **not**
  rest on a medication-modulated channel and holds under the reframe. (A net-of-driver
  overlay via R20 would *confirm* this, but is not required to hold the verdict.)
- **C4b is honest-close**, not open: HA-C4b v3 resolved the n=9 spec-asymmetry to a
  NOT-SUPPORTED verdict at n=10; it is off the seven-signal scorecard.

This is the expected and honest outcome R18 was built to produce: **most rows are
no-change or overlay-only; zero are needs-rerun.** The scorecard is **stable under
the single-pool + driver-ledger reframe** -- the reframe changes the *framing* (era
verdicts demoted to overlays, signals read along the recovery-phase axis) without
disturbing a single crash-discrimination verdict.

## 4. What this scopes for the downstream cluster

- **R14** (single-pool verdicts): done; this triage confirms nothing else flipped.
- **R19** (per-phase descriptive read): a descriptive backdrop, not a re-verdict --
  proceed as description, no re-run gated by this triage.
- **R20** (net-of-drivers re-read): **DELIVERED 2026-07-06** as an overlay in
  [`analyses/descriptive/operationalisation_support/driver_netting_overlay/findings.md`](../analyses/descriptive/operationalisation_support/driver_netting_overlay/findings.md).
  Zero verdicts change, and the result is sharper than "overlay on five rows":
  only **one** scorecard row (HA07c) uses a channel with a locked citalopram beta,
  and its delta operator makes it **dose-immovable** (netted disc identical to raw
  to two decimals, delta +0.0 pp); the sibling HA08c behaves the same; HA06b (weak
  non-significant beta) moves +1.8 pp and stays NOT-SUPPORTED; the other three
  driver-exposed rows (H02b, HA11, HA10) have no per-mg coefficient at all. R20 is
  confirmed a transparency layer, not a re-scoring.
- **R30** (net-of-slow-confounders per-phase levels): still warranted for the
  `resting_hr` + stress/BB *absolute levels* on the recovery-phase strip (a
  different surface from the binary scorecard), unchanged by this triage.

## 5. Caveats

- This triages **verdicts**, not effect sizes: an overlay-only row's netted number
  can still shift the point estimate; the triage claim is only that it does not flip
  NOT-SUPPORTED to SUPPORTED.
- HA07d's driver-robustness rests on the variability-vs-mean distinction plus the
  observed citalopram-flatness of the stdev channel; an R20 overlay would make it a
  computed confirmation rather than a reasoned one. Flagged, not blocking.
- n=1 throughout; single-pool primacy (any era difference is a number with wide
  error, never a verdict).

## 6. Cross-references

- Verdicts + tiers: `analyses/garmin_exploration/cards/trust-panel-export.md`,
  `cards/primary-verdict-statistics.md` (R2 / R14 / R31).
- Driver ledger: `methodology/citalopram_phase_stratification.md` (CONFIRMED
  channels + mandatory-correction rule), `analyses/longrun_rhr_trend/` (slow
  confounders), site R15 / R20 / R30.
- C4b: `analyses/hypotheses/HA-C4b/result.md`; STOCKTAKE.md.
- Channel behaviour under citalopram: STOCKTAKE.md (intervention_cross_channel,
  seasonality_dow) -- stress_stdev_sleep buildup delta +0.08 (flat).
- Site register R18 (this deliverable), R14 / R19 / R20 / R30; the retired split
  `methodology/train_validate_split_fate.md`. External repo `wiggers_research_story`.
