# Wiggers hypotheses — progress map as of 2026-06-23

*Successor to [wiggers_progress_2026-06-08.md](wiggers_progress_2026-06-08.md).
15-day gap; four substantively material updates land in this snapshot,
plus an architectural methodology lock for the bout-level cascade.*

1. **HA-C3 r2 HALT-on-dry-run** (`a9423af`, 2026-06-23). The Tier 1
   Wiggers C3 convex-stress→fatigue test halted on §7.5 Gate 1: the
   participant's `all_day_stress_avg` distribution has **B1 [0,20)
   n = 0** on the unmedicated × Stratum-4 pool. This is the centerpiece
   of this snapshot — a **corpus-property scope finding**, not a
   falsification: the distribution structurally never reaches the
   low-stress register Wiggers' general C3 claim assumes. Across the
   three populated bins (B2-B4) the descriptive trajectory is
   **non-monotone with a peak at stress 30-40** and a decline at
   40-60 — informally inconsistent with the simple monotone-convex
   pattern, informally consistent with an inverted-U / threshold
   pattern. v2 redraft path is clear: collapse B1 into B2 → `[0, 30)`,
   preserve the Wiggers PDF-1357 30→40 anchor at the new B2-B3
   boundary.

2. **HA11-bout-redo r2 TESTED → PARTIAL** (`6e06d12`, 2026-06-23). The
   bout-level operand `bout_n_fast_recovery_day` reproduces HA11 v1's
   train discrimination cleanly at **+20.26 pp vs HA11 v1's +22.8 pp**
   (within 2.6 pp; median signed z 2.410 vs 2.168). Bars 1+2 PASS
   (direction + magnitude); Bar 3 FAILS at block-permutation p = 0.2609
   under stationary bootstrap E[L] = 7. This is properly read as
   **magnitude-validates-instrument, power-limited at this corpus's
   n_calm = 70 / n_crash = 11 stratum** — not a methodology failure.
   Cascade gate per pre-reg §9.2: HA-C4c drafting UNBLOCKS with an
   explicit calibration caveat. Two sensitivity-arm findings carry
   forward: transient-fragility (drop transient bouts → disc falls to
   +11.69 pp, below Bar 2) and motion-clean-only INCONCLUSIVE because
   **99.3% of all 4,317 bouts carry `motion_confound_flag = True`** —
   a structural corpus property with implications for any future
   rest-stress framing.

3. **HA-C4 v2 REJECTED at daily aggregate** (`52bddb5`, test-executed
   2026-06-18). The 3-channel stress-decay triad returns triad sum
   **0.0 / 3.0**. The per-cell pattern is methodologically informative:
   Ch1 + Ch2 validate cells PASS the locked bars; train cells REFUTE;
   Ch1 alternative metric `stress_post_peak_drop_avg` SUPPORTED on
   BOTH eras (+0.210 train / +0.364 validate). The signal IS there;
   the **daily aggregate is the wrong instrument for a
   within-day-decay-shape claim**. Bout-level pivot is the
   methodological response; not a refutation of Wiggers' underlying
   claim.

4. **HA-C4b v3 NOT-SUPPORTED** (`df05e83`, test-executed 2026-06-17).
   The motion-filter-with-stress-elevation crash-precursor
   operationalisation does NOT predict crashes on the pooled
   unmedicated subset. Two alternative readings stay open per v3 §9:
   PROTECTIVE-rather-than-PREDICTIVE (the participant acts on the
   rest-stress trigger and prevents the crashes), and
   emotionally/cognitively-triggered crashes with incidental physical
   exertion in the lead-up (a primitive-gap, not a signal-gap).

Plus the **β-recalibration r4 LOCK** (`fb97d1c`, 2026-06-23) — bout-level
dose-response for citalopram: 0 of 7 features CONFIRMED at the
buildup-headline precision. Framed honestly as **underpowered-NULL at
n ≈ 49-78 day-clusters per window**, not a definitive claim about
citalopram's bout-level pharmacology. Architectural consequence: HA-C4c
primary outcome is dose-naive at this corpus; Approach A relegated
from headline to sensitivity-arm.

Cross-link for the non-Wiggers cross-cutting view: [STOCKTAKE §2d](STOCKTAKE.md#2d-tested-with-result)
(per-verdict table), [§6](STOCKTAKE.md#6-cross-section-synthesis)
(cross-cutting synthesis), [§7](STOCKTAKE.md#7-open-follow-ups--actionable-next-steps)
(next-steps queue). This document carries the Wiggers-lens reading on
top of those numbers; it does not duplicate them.

---

## How to read this map

The 6-status taxonomy from
[wiggers_progress_2026-06-08.md](wiggers_progress_2026-06-08.md) is
inherited verbatim:

- **TESTED — direct.** Operationalised as Wiggers describes (same
  physiological construct, same measurement intent).
- **TESTED — proxy.** Different measurement addressing the same
  physiological question (typically because the original signal is
  unavailable on FR245 hardware).
- **PARTIAL.** Some aspect addressed but not the full claim.
- **QUEUED.** Pre-registered but not yet run, or queued in
  `STOCKTAKE.md §7`.
- **NOT ADDRESSED.** No test run; no pre-registration locked.
- **BLOCKED.** Cannot be tested with available data/hardware on the
  current participant device.
- **INCONCLUSIVE-BY-DATA.** Pre-registered, run, but the locked
  inconclusive-cutoff binds because of data-availability gaps.

Two new status labels are added in this snapshot for the Wave-4 events
that do not cleanly fit the existing taxonomy:

- **HALT-ON-DRY-RUN.** Pre-reg LOCKED but §7.5 sanity gates failed at
  the locked spec in a way the spec's pre-committed halt-option could
  not absorb; the test did not execute beyond the dry-run and the
  resolution is a v2 spec revision per
  [`hypothesis_lock_process.md`](methodology/hypothesis_lock_process.md)
  §3.9 + §10.4 step 3. Applied to HA-C3 r2.
- **PARTIAL-CASCADE-UNBLOCK.** A framework-validity test cleared
  direction + magnitude bars but failed the statistical-significance
  bar at the present sample size; cascade gate unblocks for downstream
  pre-regs with an explicit calibration caveat naming the failing bar.
  Applied to HA11-bout-redo r2.

Where a Wiggers hypothesis is flagged ⚠️ in the source (high-value /
counter-intuitive / contradicts a prior finding), that flag is preserved.

---

## Priority shortlist (Wiggers' top six) — current status

Wiggers explicitly names six tests as decisive for product direction.
This row is the most important reading of the whole map; it carries
forward 2026-06-08 with the Wave-3/4 changes folded in.

| Wiggers ID | Question | Status as of 2026-06-23 |
|---|---|---|
| **H1 ⚠️** | Do wearable signals lead the felt crash? | **PARTIAL via proxy; Wiggers-direction lag test still untested.** Unchanged since 2026-06-08. S02b refuted the empirically-observed score-leads-Garmin direction at daily resolution. No new direct lag execution in this window. |
| **H2 ⚠️** | How many crashes are "activity-invisible"? | **PARTIAL.** Unchanged structural framing. HA-C4b v3 NOT-SUPPORTED (§9 second-branch reading: §4.2-admitted crashes may be disproportionately emotionally/cognitively triggered with incidental physical exertion) refines the H2 framing: a formal H2 count would now have to bridge the physical-exertion vs cognitive/emotional split. Primitive for cognitive/emotional load remains queued. |
| **H3 ⚠️** | Acute-illness vs PEM crashes separable in Garmin? | **NOT ADDRESSED.** Unchanged since 2026-06-08. Gated on crash_v3 from notes. |
| **C3 / D1 / D2** | Non-linearity of stress; level-vs-dynamics for BB | **C3: HALT-ON-DRY-RUN at r2 (NEW since 2026-06-08); D1 + D2 unchanged.** HA-C3 r2 LOCKED 2026-06-23 (`de22b68`) → test-executed same day (`a9423af`) → HALT on §7.5 Gate 1 (B1 [0,20) n = 0, B5 [60,100] n = 1; §7.3 halt-option-A pre-commit absorbed only B5 not B1). v2 redraft queued. D1 PARTIAL via H04 BB-net-delta (refuted); D2 BLOCKED-PENDING-FIT-DECODE (H03b INCONCLUSIVE × 12). |
| **B4 / H4 ⚠️** | Parasympathetic-swing as an inverted indicator | **TESTED — proxy, SUPPORTED with framing-softened-on-independence (unchanged headline); H4 framing now also informed by recovery_arc v2 afbouw reversal on CONFIRMED-citalopram channels.** The 2026-06-08 cross-channel collapse (HA10 ≡ −HA07c at ρ = −0.922) still binds. New context: `recovery_arc` v2 (2026-06-22 `8feae6a`) §5.A sub-stratification within citalopram-modulated phase 5 surfaces **afbouw reversal** — `all_day_stress_avg` buildup 28.5 → consolidation 31 → afbouw 34 (returns to pre-medication 4b baseline); `bb_lowest` buildup 26 → consolidation 22 → afbouw 15 (goes LOWER than 4b). The BB-anchored H4 composite is built on these channels; the citalopram benefit on this signal cluster is reversible during dose reduction. A future H4 pre-reg invoking the BB-anchored composite inherits the afbouw reversal as substantive context. |
| **G3 ⚠️** | Barometric pressure × headache | **NOT ADDRESSED.** Unchanged since 2026-06-08. PARKED per `STOCKTAKE §7` Q18 KNMI external-data dependency. |

**Of Wiggers' six product-decisive tests**, the changes since 2026-06-08
are: **C3 has now LANDED at the dry-run stage** (and surfaced a
substantive corpus-property finding even before primary execution); H4
gains substantive context from the afbouw reversal finding; H1, H2, H3,
G3 are unchanged. The 2026-06-08 reading that the project's effective
channel count for the parasympathetic-swing cluster is closer to 1 + 1
than 3 still holds; the new finding is that the autonomic-load cluster
loses its citalopram-era recovery during afbouw, so any forward H4
pre-reg invoking the BB-anchored composite has to declare its
phase-stratum explicitly.

---

## Section-by-section progress

### A. Resting HR & night HR

| Wiggers | Status | What changed since 2026-06-08 |
|---|---|---|
| A1: RHR elevated on/before crashes | TESTED — direct (Tier 2 with stop-rule) | Unchanged. |
| A2: RHR deviates either direction | TESTED — direct | Unchanged. |
| A3: Night RHR elevated from t-2 onwards | TESTED — direct | Unchanged. |
| A4: Sustained multi-hour RHR elevation | BLOCKED — no intraday HR analysis run (operationalised at register level Wave 4 v3; no HA pre-reg yet) | Unchanged at the test layer. The bout-level recovery-dynamics MD (LOCKED 2026-06-21 `c57ff3f`) is now available as cross-channel infrastructure if a future A4 pre-reg wants to extend the operand to per-bout HR features. |

### B. HRV — PARTIAL via `stress_mean_sleep` proxy

| Wiggers | Status | What changed since 2026-06-08 |
|---|---|---|
| B1: Day-over-day HRV drop ≥ 10 predicts crash | TESTED — proxy (Tier 2 with stop-rule) | Unchanged at the verdict layer (HA07c train SUPPORTED / validate REFUTED; family exhausted across HA07c + H02b + the still-pending B1 pre-reg if it locks). New context: `stress_mean_sleep` is one of the 3 CONFIRMED-citalopram channels (β = +0.43/mg per `citalopram_dose_response_stress_mean_sleep.md §5.6.1`); HA07c forward citations now require explicit phase acknowledgement per `STOCKTAKE §6` "citalopram-as-confound for HA07c" paragraph. |
| B2 ⚠️: HRV declines multi-day even with rest | TESTED — proxy | Unchanged (HA08c train SUPPORTED / validate REFUTED). |
| B3: Rising 7d HRV baseline = improving | NOT ADDRESSED | Unchanged. |
| **B4 ⚠️: Sudden HRV spike is a NEGATIVE leading indicator** | TESTED — proxy, SUPPORTED (framing softened — unchanged headline) | Unchanged headline. The 2026-06-08 collinearity audit still binds (HA10 ≡ −HA07c; HA07d-HA07c +0.501). |
| B5: HRV rises at acute-illness onset | BLOCKED + NOT ADDRESSED | Unchanged. |

**B-block synthesis (Wiggers-lens reading carried forward).** All
B-block claims have proxy support at the daily aggregate via
`stress_mean_sleep` (Cohen's d = +0.90 episode-level). The
bout-level β recalibration of `stress_mean_sleep`-adjacent features
(2026-06-22 `d9c6fa4` → r4 LOCK `fb97d1c`) returns **0 / 7 CONFIRMED**
at the per-bout layer. The honest framing per `STOCKTAKE §6`: this is
**underpowered-NULL at n ≈ 49-78 day-clusters per window**, NOT a
definitive claim about citalopram's bout-level pharmacology. For the
Wiggers B-block: the daily-aggregate proxy support stands; the
bout-level confirmation is not achievable at the present per-window n.
This is a corpus-size constraint, not a methodological problem with the
B-block proxy framing.

### C. Stress score

| Wiggers | Status | What changed since 2026-06-08 |
|---|---|---|
| C1: Night high-stress elevated on/before crashes | TESTED — proxy | Unchanged headline (HA07c). |
| C2: High daily stress predicts worse next-day recharge | NOT ADDRESSED | Unchanged. |
| **C3 ⚠️: Stress→fatigue relationship is non-linear/convex** | **HALT-ON-DRY-RUN (NEW Wave 4 status)** | r2 LOCKED 2026-06-23 (`de22b68`) → test-executed (`a9423af`) → HALT on §7.5 Gate 1 (B1 [0,20) n = 0 + B5 [60,100] n = 1; §7.3 halt-option-A pre-commit addressed only B5 not B1). Substantive observations from the dry-run descriptive partial-pool run: non-monotone trajectory across populated bins (B2 → B3 → B4: gevoelscore mean 3.958 → 4.265 → 3.860). **See HA-C3 B1-absent synthesis section below.** |
| **C4: Stress fails to drop during rest** | **REJECTED at daily-aggregate (NEW Wave 4 status); bout-level pivot in flight** | v1 LOCKED 2026-06-17 (`da79387`) → dry-run halted on Ch3 validate n = 25 < 30 → v2 LOCKED 2026-06-18 (`b0f38a7`) → test-executed 2026-06-18 (`52bddb5`). Triad sum 0.0 / 3.0. Ch1 + Ch2 validate SUPPORTED; train REFUTED; Ch3 train wrong-direction; Ch3 validate INCONCLUSIVE. Ch1 alternative `stress_post_peak_drop_avg` SUPPORTED on BOTH eras (+0.210 / +0.364). **See HA-C4 closure synthesis section below.** |
| **C4b: C4 with motion filter** | **NOT-SUPPORTED (Wave 3 status; carried forward)** | v3 LOCKED 2026-06-17 (`32ba3b9`) → test-executed (`df05e83`). Pooled n = 10; (a) 40% FAIL, (b) -10pp FAIL, (c) +1.21 PASS. Two alternative readings stay open per v3 §9: PROTECTIVE-not-PREDICTIVE; emotionally/cognitively-triggered crashes. **See HA-C4b closure synthesis section below.** |

### D. Body battery

| Wiggers | Status | What changed since 2026-06-08 |
|---|---|---|
| D1 ⚠️: Absolute BB level is a weak indicator | PARTIAL | Unchanged. |
| D2: BB dynamics beat BB level | BLOCKED-PENDING-FIT-DECODE | Unchanged. |
| D3: Higher BB floor in low-crash stretches | NOT ADDRESSED | Unchanged at the HA-pre-reg layer. `recovery_arc` v2 (2026-06-22) descriptively characterises `bb_lowest` on the 6-phase axis: phase 5 reaches the corpus maximum at 22 (citalopram-modulated minimum elevation) but sub-stratification surfaces the afbouw reversal (buildup 26 → consolidation 22 → afbouw 15). A future D3 HA pre-reg would inherit this descriptive context. |
| D4: BB declines steeply around crashes | PARTIAL | Unchanged. |
| **D5 ⚠️: Paradoxically HIGH morning BB precedes a crash** | TESTED — direct, validate SUPPORTED (fragile) | Unchanged headline. |

### E. Steps / activity load

Unchanged across the board since 2026-06-08. E1 NOT ADDRESSED, E2
PARTIAL, E3 TESTED — direct (HA01c locked + HA01c v2 mixed).

### F. Sleep

Unchanged across the board since 2026-06-08. F1-F4 all NOT ADDRESSED
or BLOCKED. Sleep-channel coverage remains thin.

### G. Other sensors

Unchanged across the board since 2026-06-08. G1, G2 NOT ADDRESSED;
**G3 ⚠️** PARKED per `STOCKTAKE §7` Q18; G4 DEPRIORITISED PER SOURCE.

### H. Mechanism & lead/lag

| Wiggers | Status | What changed since 2026-06-08 |
|---|---|---|
| **H1 ⚠️: Wearable signals lead the felt crash** | PARTIAL + first direct lag test REFUTED | Unchanged at the test layer. |
| **H2 ⚠️: Activity-invisible crashes** | PARTIAL | HA-C4b v3 §9 second-branch reading refines H2 framing (cognitive/emotional triggers may explain a non-trivial fraction of `crash_v2` episodes the physical-exertion gate admits). A formal H2 count remains queued. |
| **H3 ⚠️: Acute-illness vs PEM separable in Garmin?** | NOT ADDRESSED | Unchanged. |
| **H4 ⚠️: Parasympathetic-swing precedes dip 1-2 days** | TESTED — proxy, SUPPORTED on direction; framing softened on independence (unchanged headline) | New substantive context: `recovery_arc` v2 §5.A surfaces afbouw reversal on `all_day_stress_avg` + `bb_lowest` (the BB-anchored composite's home channels). A future H4 HA pre-reg invoking the BB-anchored composite inherits the afbouw reversal as load-bearing context — the swing signature interpreted at consolidation differs from interpreted at afbouw because the underlying channels themselves shift across the citalopram-dose axis. |
| H5: Each metric has a characteristic lag | PARTIAL (Tier 2 with descriptive prereq queued as Q15) | Unchanged. |

### I. Data-quality / methodology checks

| Wiggers | Status | What changed since 2026-06-08 |
|---|---|---|
| I1: Re-run excluding first ~3 weeks of each device | NOT ADDRESSED | Unchanged. |
| I2: Mark device-change points | NOT ADDRESSED | Unchanged. |
| I3: Confirm rich-metrics overlap window | PARTIAL → SHARPENED 2026-06-07 (H03b) | Unchanged. |

---

## Synthesis: bout-level cascade arc

The bout-level cascade — the methodological response to HA-C4 v2's
daily-aggregate REJECTED outcome — landed end-to-end in this 15-day
window:

- **`bout_level_recovery_dynamics.md` + `bout_level_dose_response_calibration.md`
  co-LOCKED** 2026-06-21 (`c57ff3f`). Narrow lock scope at HA11 + C4;
  A4/C1/C4b/H4 enabled-on-request via `9ddfafb` register forward-pointers.
- **Bout-extraction pipeline LANDED** 2026-06-22 (`d5b394c`). 4,317
  bouts across 1,479 valid days; 22.8% did-not-return, 22.1% transient,
  16.1% sleep-bouts, 62.7% multi-peak; 5 new per-day aggregations added
  to `per_day_master.csv`.
- **HA11-bout-redo r1 drafted** 2026-06-22 (`8421657`) → **r2 LOCKED**
  2026-06-23 (`5c71aa0` + footer fix `b5bf0f8`) → **test-executed
  2026-06-23** (`6e06d12`) → **PARTIAL**.
- **β-recalibration r3 LANDED** 2026-06-22 (`d9c6fa4`) → **r4 LOCKED**
  2026-06-23 (`fb97d1c`) → 0 / 7 CONFIRMED at the discriminative bar.

**Wiggers-lens reading of HA11-bout-redo PARTIAL.** The bout-level
operand `bout_n_fast_recovery_day` reproduces HA11 v1's signal
magnitude cleanly: +20.26 pp vs HA11 v1's +22.8 pp reference (within
2.6 pp); median signed z 2.410 vs 2.168. Both magnitude-comparability
bars (direction + ≥ +12.8 pp) PASS cleanly. What fails is the
block-permutation p (p = 0.2609, vs the 0.05 bar), driven by
sample-size constraints at n_calm = 70 / n_crash = 11. **This validates
Wiggers' implied within-day-shape claim at magnitude** but is
**power-limited at the corpus's bout-level stratum**, not a
methodology failure. The +20.26 observed discrimination sits at the
74th percentile of the bootstrap null distribution; a 3× larger
crash-arm would clear bar 3 by a wide margin. The honest framing per
[HA11-bout-redo result.md §6](analyses/hypotheses/HA11-bout-redo/result.md):
*magnitude-validates-instrument, power-limited at this stratum n*.

**Three sensitivity-arm Wiggers-relevant findings carry into HA-C4c
framing**:

1. **Transient-fragility.** Dropping the 22% of bouts flagged as
   transient drops discrimination from +20.26 pp to +11.69 pp — below
   the bar-2 threshold of +12.8 pp. A non-trivial fraction of the
   reproduction signal lives in transient bouts. The Wiggers C4 claim
   is qualitatively about sustained rest-stress, not transient
   excursions; a "bout" as the LOCKED detection rule extracts is
   broader than what Wiggers' implicit operand probably implies.
   Downstream HA pre-regs must pre-spec their transient inclusion
   choice.

2. **Motion-clean-only INCONCLUSIVE: 99.3% motion-confound.** 4,285 of
   4,317 bouts (99.3%) carry `motion_confound_flag = True`. Filtering
   to motion-clean bouts collapses every analysis day below the σ > 0.5
   variability floor → 0 analysis days survive. This is a structural
   corpus property at the LOCKED detection thresholds, not a test bug.
   **Wiggers-lens implication**: Wiggers' C4 / C4b language about
   "rest-stress" assumes a clean motion-free operand. On this corpus,
   that operand is hard to construct at the bout-extraction layer. Any
   future bout-level analysis claiming rest-stress semantics — whether
   Wiggers-anchored or otherwise — has to acknowledge that bouts as
   currently extracted ARE motion-tagged events, and the rest-stress
   operand requires either a relaxed bout-detection threshold or a
   per-bout motion-proxy recalibration.

3. **Cascade gate UNBLOCKS for HA-C4c with calibration caveat.** Per
   HA11-bout-redo pre-reg §9.2: HA-C4c drafting proceeds, but the
   HA-C4c §8 caveats MUST carry an explicit calibration caveat naming
   bar 3 (block-permutation p) as the failing bar with the verbatim
   observed values (disc = +20.26 pp; p = 0.2609 vs 0.05 threshold).
   HA-C4c's substantive verdict-magnitudes are interpreted with a
   calibration discount: the operand can reproduce HA11 v1's signal
   magnitude but the present sample size cannot statistically
   distinguish it from the block-permutation null.

---

## Synthesis: HA-C3 B1-absent finding (centerpiece)

**Wiggers C3 verbatim claim** (PDF lines 1357-1368, Annual Stress
Scores): *"If you've paid attention to your own stress scores, you
might know that a day with a score of 40 is much more tiring than a
day with a score of 30. Such a step appears very small on the graph,
but it isn't. This graph shows a kind of stair step."* The implied
claim is a **convex** stress → fatigue mapping across the full stress
range, anchored at the 30 → 40 stair-step.

**Spec.** HA-C3 r2 LOCKED 2026-06-23 (`de22b68`; audit at `8f3f269`
PASS-with-caveats; r2 absorb via §3.6 compression). Headline cell:
unmedicated × Stratum 4 × `all_day_stress_avg` binned at
{B1[0,20), B2[20,30), B3[30,40), B4[40,60), B5[60,100]} ×
`gevoelscore` bin-mean × {Jonckheere-Terpstra monotonicity +
second-difference convexity contrast + natural-cubic-spline
non-linearity} × block-permutation null at E[L] = 7 × 3-condition
gated verdict. **The 30 → 40 anchor was preserved verbatim at the
B3-B4 boundary** in the locked spec.

**Dry-run outcome.** §7.5 Gate 1 (per-bin n ≥ 30) failed on B1 and B5:

| bin | label | n | bin-mean gevoelscore |
|---|---|---:|---:|
| B1 | [0, 20) | **0** | NA |
| B2 | [20, 30) | 95 | 3.958 |
| B3 | [30, 40) | 385 | 4.265 |
| B4 | [40, 60) | 100 | 3.860 |
| B5 | [60, 100] | 1 | 1.000 |

**The B1 zero-population was not forecast at lock.** The B5 underpower
was forecast (§7.2 named B5 as most-at-risk for the < 30 gate; §7.3
halt-option-A pre-committed widening B4 to absorb B5). The B1 boundary
was not anticipated — the participant's `all_day_stress_avg`
distribution structurally never falls below 20 (stress median 34;
pool n 581). Per [`hypothesis_lock_process.md`](methodology/hypothesis_lock_process.md)
§3.9 + §10.4 step 3 (no iteration on the spec after dry-run; any
post-dry-run revision creates a v2), the agent correctly halted
instead of executing on a spec the data cannot support.

**Wiggers-lens framing: corpus-property scope, not falsification.**
The B1 absence is NOT a falsification of Wiggers' C3 claim; it is a
**corpus-coverage finding about which slice of Wiggers' claim this
n=1 can test**. Wiggers' general claim spans a stress range
(0 → 60+); this n=1 corpus structurally covers only the middle 3 of 5
register-verbatim bins (B2 + B3 + B4). The participant simply does
not have low-stress days (B1) in this analytic pool, and has only one
day in the top-stress register (B5). The convex-acceleration "barely
felt at the bottom, severe at the top" pattern Wiggers describes
cannot be tested at the bottom on this corpus; the top is a single
observation. **This is a substantive participant-data finding** about
how Wiggers' general framing translates (or doesn't) to a specific
person's stress distribution, NOT a methodological failure of the
HA-C3 spec or a verdict on Wiggers' claim.

**Descriptive trajectory across the 3 populated bins.** Per
[HA-C3 result.md §5](analyses/hypotheses/HA-C3/result.md), the
informal-only descriptive reading (pre-reg verdict NOT computed):

| bin → bin | gevoelscore mean change |
|---|---|
| B2 (3.958) → B3 (4.265) | **+0.307** (worse than B2) |
| B3 (4.265) → B4 (3.860) | **−0.405** (better than B3) |
| B4 (3.860) → B5 (1.000) | +2.860 (n = 1; uninterpretable) |

The trajectory across the 3 populated bins is **non-monotone with a
peak at stress 30-40 and a decline at stress 40-60**. Informally
inconsistent with the simple monotone-convex pattern Wiggers' claim
implies. Informally consistent with EITHER REJECTED-via-no-monotone-
relationship (pre-reg §7.4 "no monotone relationship at all → REJECTED
via condition (a) failure") OR an inverted-U / threshold pattern that
Wiggers' claim shape did not anticipate.

**Why the gevoelscore-peak-at-30-40 reading is interesting on its own
terms.** The 30 → 40 boundary Wiggers' claim anchors is exactly where
the participant's gevoelscore is at its worst on this corpus. If the
v2 redraft confirms this non-monotonicity at the formal verdict layer,
the substantive read would be that Wiggers' stair-step framing
captures the qualitative observation that the 30 → 40 step is
discriminating, but in the **wrong direction**: above 40, the
participant's gevoelscore improves rather than continuing to
deteriorate. Candidate mechanism reads (post-hoc; for v2 framing): the
high-stress days may reflect a particular activity-or-coping mode
distinct from the unstructured mid-stress days; or, the stress score
itself may saturate at the high end on this corpus in a way that
decouples from the felt experience. Neither is testable at v2 alone;
both are worth carrying forward to the cross-test interpretation pass.

**v2 redraft path.** Collapse B1 into B2 → new bin scheme
`[0, 30), [30, 40), [40, 60), [60+]`, **preserving the Wiggers
PDF-1357 30 → 40 anchor** at the new B2-B3 boundary. The 3 populated
bins of the r2 spec become the 3 bins of the v2 spec (with B5
absorbed into B4 per §7.3 halt-option-A). v2 will formally test what
those 3 bins say.

---

## Synthesis: Wiggers C4 closure status

HA-C4 lineage:

- v1 LOCKED 2026-06-17 r2 `da79387` → dry-run HALTED on Ch3 validate
  n = 25 < 30 sanity bar.
- v2 fresh-session draft 2026-06-18 with §5.3 INCONCLUSIVE-aware
  verdict rule + §7.3 arithmetic rebuild + §4.11.3 chain-relaxed
  sensitivity arm.
- v2 r2 LOCKED 2026-06-18 (`b0f38a7`) → test-executed 2026-06-18
  (`52bddb5`) → **REJECTED at daily-aggregate level** (triad sum
  0.0 / 3.0; v2 §5.3 INCONCLUSIVE-aware bands).

**Per-cell pattern is methodologically informative.** Per
[HA-C4 result.md §5.1+§5.2](analyses/hypotheses/HA-C4/result.md):

| channel | train | validate | per-channel verdict |
|---|---|---|---|
| Ch1 (`stress_post_peak_time_to_rest_min`) | REFUTED (δ = +0.056, p = 0.18) | **SUPPORTED** (δ = +0.238, p = 0.0245) | REFUTED |
| Ch2 (`stress_high_duration_min`) | REFUTED (δ = +0.193, p = 0.0004 — narrow miss on δ bar) | **SUPPORTED** (δ = +0.356, p = 0.0015) | REFUTED |
| Ch3 (`awake_stress_avg` on T+1) | REFUTED (δ = −0.080, p = 0.85 wrong-direction) | INCONCLUSIVE (n = 25 < 30) | REFUTED |

And the Ch1 alternative metric `stress_post_peak_drop_avg` (Ch1's
within-day decay companion):

| era | δ | p | verdict |
|---|---:|---:|---|
| train | +0.210 | 0.0009 | **SUPPORTED** |
| validate | +0.364 | 0.0012 | **SUPPORTED** |

**Wiggers-lens framing: daily-aggregate-wrong-instrument, not
refutation of the underlying claim.** The validate-era SUPPORTED
pattern on Ch1 + Ch2, plus the both-eras SUPPORTED on the Ch1
alternative `stress_post_peak_drop_avg`, says the **underlying signal
IS detectable**. The triad-aggregate REJECTED says the
**daily-aggregate operationalisation collapses the within-day decay
shape** into a per-day median that the participant's days don't
discriminate cleanly. HA-C4 v2's REJECTED verdict at daily-aggregate
is NOT a refutation of Wiggers' substantive C4 claim ("stress fails to
drop during rest after overexertion"); it is a finding that the
operational instrument is wrong-grain for a within-day-recovery-shape
claim. The bout-level pivot
([`bout_level_recovery_dynamics.md`](methodology/bout_level_recovery_dynamics.md))
is the methodological response.

**HA-C4c is the substantive bout-level retest.** Cascade-gated on
HA11-bout-redo passing framework-validity. The HA11-bout-redo PARTIAL
verdict (2 of 3 bars met; bar 3 power-limited at n_calm = 70) means
**HA-C4c drafting proceeds with calibration caveat** rather than
being halted. The framing arc is:

> daily-aggregate REJECTED (wrong instrument) → bout-level
> framework-validity PARTIAL (right instrument, power-limited at this
> stratum) → HA-C4c substantive retest with calibration discount.

This is one continuous methodological arc, not three separate
verdicts. The Wiggers C4 claim has not been refuted on this n=1
corpus; it has been re-located to a resolution where the
participant's bout-level n imposes a calibration discount on any
verdict it can produce.

---

## Synthesis: Wiggers C4b closure status

HA-C4b v3 lineage:

- v1 LOCKED 2026-06-15 → dry-run halted (`HA-C4b/hypothesis-v1-archived.md`).
- v2 LOCKED 2026-06-16 → INCONCLUSIVE 2026-06-16 (`83a64b2`) on
  spec-design asymmetry between dry-run and full-run §4.3 1b.ii gates.
- **v3 LOCKED** 2026-06-17 (`32ba3b9`) → **test-executed 2026-06-17**
  (`df05e83`) → **NOT-SUPPORTED**.

**Headline numbers** (per [HA-C4b result.md](analyses/hypotheses/HA-C4b/result.md)):
unmedicated × pooled train+validate × `stress_low_motion_min_count_S60_Mlow`
× N_std = 1.5 × primary 4d × one-sided elevated. n_clean = 10
(8 train + 2 validate, with 2023-02-04 restored after v3's §4.3 1b.ii
drop). (a) 40% **FAIL** (vs ≥ 60% bar); (b) −10pp **FAIL** (vs ≥ +15pp
bar); (c) +1.21 PASS (vs ≥ 0.75 bar).

**v3 §9 NOT-SUPPORTED branch holds two alternative readings open**:

1. **The lived rest-stress trigger may be PROTECTIVE rather than
   PREDICTIVE.** The participant operationally uses the rest-stress
   trigger (per [`garmin_pacing_practice.md` §3.3](methodology/garmin_pacing_practice.md))
   and may successfully prevent the crashes the precursor test would
   have caught. The locked-pre-reg test cannot discriminate this
   reading from "no signal exists" because the protocol disturbs the
   test by construction.

2. **§4.2-admitted crashes may be disproportionately emotionally /
   cognitively triggered with incidental physical exertion** in the
   lead-up window. The corpus has partial proxies
   (`cat_belasting_emotioneel`, `cat_belasting_cognitief`,
   `state_symptoom_emotioneel`, `state_symptoom_cognitief`) with the
   DATA_DICTIONARY §9 sparsity caveats; v3 does not use them in
   §4.2 conditioning. A future primitive would need to bridge this.

**Combined with HA11-bout-redo's 99.3% motion-confound finding.** The
HA-C4b daily count uses minutes-where-stress-high-AND-motion-low; the
HA11-bout-redo bout-level analysis finds that bouts as extracted are
99.3% motion-tagged. Both findings point in the same direction: on
this corpus at the present operationalisation thresholds, a clean
rest-stress operand is structurally hard to construct. **Wiggers'
qualitative C4 / C4b language about "rest"-stress assumes a degree of
motion-clean separation that this participant's per-minute trace does
not provide at the locked operationalisations.** This is a
corpus-property finding affecting how Wiggers' rest-stress framework
translates downstream, not a refutation of the framework itself.

---

## Synthesis: Wiggers B-block proxy framing status

The B-block (HRV) hypotheses remain PARTIAL via the `stress_mean_sleep`
proxy on descriptive grounds (Cohen's d = +0.90 episode-level;
established 2026-06-13; carried forward unchanged). What's new in this
window:

**β-recalibration r4 LOCKED 2026-06-23 (`fb97d1c`): 0 of 7 features
CONFIRMED at the discriminative bar.** The bout-level dose-response
recalibration of `stress_mean_sleep`-adjacent per-bout features
(peak_height, pre_bout_baseline, recovery_half_life, decay_slope,
AUC_above_baseline) plus 2 per-day aggregations (bout_n_per_day,
bout_n_fast_recovery_day) on the 3-window spec (buildup-post-CPAP
n = 49 day-clusters; afbouw 2026 n = 78; spring 2025 control flat dose)
returns:

| verdict | features |
|---|---|
| CONFIRMED | (none) |
| weakly_consistent | recovery_half_life, AUC_above_baseline, bout_n_fast_recovery_day |
| NULL | peak_height, pre_bout_baseline, decay_slope, bout_n_per_day |

**Wiggers-lens reading: underpowered-NULL, not a definitive claim
about citalopram's bout-level pharmacology.** The honest framing per
[STOCKTAKE §6](STOCKTAKE.md#6-cross-section-synthesis) "underpowered-NULL"
paragraph: at this corpus's per-window bout-level n, β coefficients
cannot cross the sub-MD §3.4 four-condition discriminative bar
regardless of underlying signal strength. The recalibration documents
that **Approach A (per-feature dose-adjustment) is NOT load-bearing
for downstream HA pre-regs at this corpus's bout-level n**, NOT that
citalopram has no bout-level effect. The parent dose-response finding
(`stress_mean_sleep` daily-aggregate β = +0.43/mg p = 0.001;
`all_day_stress_avg` β = +0.57/mg p = 0.0003) remains intact at the
daily layer.

**For the Wiggers B-block specifically.** Wiggers' HRV-derived
autonomic-load claims have proxy support at the daily aggregate
(d = +0.90; SUPPORTED-direction on the B1-B5 family). The bout-level
confirmation that would extend this support to a within-day-resolution
operand is not achievable at the current corpus's per-window n. This
is a **corpus-size constraint, not a methodological problem with the
B-block proxy framing**. If a future expanded corpus or revised
bout-detection rule materially changes per-window n, the recalibration
re-runs (sub-MD §8 r4 trigger); the B-block proxy framing inherits
the new precision.

**Architectural consequence for HA-C4c primary**: dose-naive. The
2024-04-09 citalopram-axis boundary between phase 5
(`pacing_habit_established`) and phase 6 (`citalopram_modulated`) is
NOT load-bearing for bout-level analyses at the current corpus n.
Pooling phase 5 + phase 6 for bout-level work gains ~70 more
day-clusters without inheritance violations per
[`phase_axis_collapsibility_conventions.md`](methodology/phase_axis_collapsibility_conventions.md) §3 Tier B.

---

## Synthesis: Wiggers H1-H5 mechanism + lead/lag status

No new H-block test executions since 2026-06-08. The 2026-06-08
verdict map carries forward:

- **H1**: PARTIAL via proxy (HRV-Status hardware-blocked on FR245);
  S02b refuted the empirically-observed score-leads-Garmin direction;
  the Wiggers-direction wearables-lead-score lag test at daily
  resolution remains untested. Unchanged.

- **H2**: PARTIAL. Refined framing inherited from HA-C4b v3 §9
  second-branch (cognitive/emotional triggers as a candidate
  explanation for crashes the physical-exertion gate admits).
  A formal count of activity-invisible crashes per Wiggers H2
  remains queued.

- **H3**: NOT ADDRESSED. Gated on crash_v3 from notes. Unchanged.

- **H4**: TESTED — proxy, SUPPORTED on direction (B4/D5/H4 cluster).
  Framing softened on independence per the 2026-06-08 collinearity
  audit (HA10 ≡ −HA07c; HA07d-HA07c +0.501). **New substantive
  context for any future H4 pre-reg**: `recovery_arc` v2 (2026-06-22
  `8feae6a`) §5.A surfaces afbouw reversal on the CONFIRMED-citalopram
  channels which are the BB-anchored composite's home channels —
  `all_day_stress_avg` buildup 28.5 → consolidation 31 → afbouw 34
  (returns to pre-medication 4b baseline); `bb_lowest` buildup 26 →
  consolidation 22 → afbouw 15 (goes LOWER than pacing-4b). The
  citalopram benefit on the H4 composite's home channels is
  **reversible during dose reduction**. A future H4 pre-reg invoking
  the BB-anchored composite has to declare its phase-stratum
  explicitly (afbouw cells will read systematically differently than
  consolidation cells).

- **H5**: PARTIAL (Tier 2 with Q15 descriptive prereq queued).
  Unchanged.

---

## Synthesis: Wiggers G3 barometric pressure

**UNCHANGED since 2026-06-08.** PARKED per
[STOCKTAKE §7](STOCKTAKE.md#7-open-follow-ups--actionable-next-steps)
Q18 KNMI external-data dependency; no new work in this window. Out of
active scope while Tier 1 (C3 + C4) progresses.

---

## What stays unchanged from 2026-06-08

The following Wiggers register rows have no material update in this
window. Listed explicitly to prevent inferring change where there
isn't any:

- All of A (A1 + A2 + A3 unchanged at TESTED — direct; A4 unchanged
  at BLOCKED at the HA-test layer, with the bout-level recovery-dynamics
  MD now available as cross-channel infrastructure for a future A4
  pre-reg).
- B-block verdict headlines (HA07c, HA08c, HA07d unchanged; new
  context is the underpowered-NULL framing of the bout-level
  recalibration, not a verdict change).
- C1 (TESTED — proxy via HA07c, unchanged).
- C2 (NOT ADDRESSED).
- D1, D2, D4, D5 (PARTIAL / BLOCKED / PARTIAL / SUPPORTED-fragile;
  unchanged at the test layer; D3 inherits new descriptive context
  from `recovery_arc` v2 on `bb_lowest` afbouw reversal but no HA
  pre-reg).
- All of E (E1 NOT ADDRESSED; E2 PARTIAL; E3 TESTED — direct via
  HA01c locked + HA01c v2 mixed; unchanged).
- All of F (F1-F4 NOT ADDRESSED or BLOCKED; sleep-channel coverage
  remains thin; unchanged).
- All of G (G1, G2, G4 unchanged; G3 PARKED unchanged).
- All of H except H4 framing context (H1 PARTIAL + first direct lag
  test REFUTED; H2 PARTIAL with HA-C4b §9 second-branch refining
  framing; H3 NOT ADDRESSED; H5 PARTIAL).
- All of I (I1, I2, I3 unchanged).

---

## Project-state cross-link

**Programme state.** Bout-level cascade resuming with HA-C4c as the
next substantive Wiggers-touching pre-reg (cascade-resuming with
calibration-caveat framing baked in per HA11-bout-redo §9.2 +
β-recalibration r4 dose-naive-primary framing). HA-C3 v2 redraft is a
small spec revision queued in parallel (independent of the bout-level
cascade). Three Phase-1 descriptive analyses landed in this window
(stress_mean_sleep `84b9801` 2026-06-18; recovery_arc v2 `8feae6a`
2026-06-22; stress_low_motion `4318a77` 2026-06-22), all of which
inform Wiggers-adjacent framing without producing new Wiggers
verdicts. Methodology scaffolding MDs LOCKED in this window:
`lc_recovery_phase_axis.md` (`d47e0d3` 2026-06-19, 6-phase axis +
4a/4b sub-boundary); `bout_level_recovery_dynamics.md` +
`bout_level_dose_response_calibration.md` (co-LOCKED `c57ff3f`
2026-06-21); `phase_axis_collapsibility_conventions.md` (`ab356d8`
2026-06-22).

For the non-Wiggers cross-cutting view:
[STOCKTAKE §2d](STOCKTAKE.md#2d-tested-with-result) (verdicts table),
[§6](STOCKTAKE.md#6-cross-section-synthesis) (cross-cutting synthesis),
[§7](STOCKTAKE.md#7-open-follow-ups--actionable-next-steps) (next-steps queue).

---

## Next Wiggers-touching dispatches queued

1. **HA-C4c pre-reg drafting** — cascade-resuming. The substantive
   bout-level Wiggers C4 retest. §8 caveats must carry the calibration
   caveat per HA11-bout-redo §9.2 (bar 3 powering-shortfall named
   verbatim: disc = +20.26 pp; p = 0.2609 vs 0.05). Primary outcome is
   dose-naive at this corpus per β-recalibration r4. Phase 5 + phase 6
   poolable for bout-level work without inheritance violations per
   collapsibility conventions §3 Tier B. The motion-clean 99.3%
   structural finding + transient-fragility carry forward as
   pre-spec-locked sensitivity arms.

2. **HA-C3 v2 redraft** — small spec revision per
   [`hypothesis_lock_process.md`](methodology/hypothesis_lock_process.md)
   §10.4 step 3. Collapse B1 [0,20) into B2 → `[0, 30)` low-stress
   bin; preserve Wiggers PDF-1357 30 → 40 anchor at new B2-B3
   boundary; absorb B5 into B4 per §7.3 halt-option-A. The
   non-monotone descriptive trajectory (gevoelscore peak at stress
   30-40 declining at 40-60) is the data-pattern v2 will formally
   test. Drafting-session independent of bout-level cascade.

3. **HA11-bout-redo v3 (OPTIONAL; not currently queued)** — if HA-C4c
   finds the calibration caveat too binding, an operand-refinement
   re-tuning the 15-min / 45-min bout-detection thresholds in parent
   MD §6.1 is available. PARTIAL does NOT halt the cascade per
   HA11-bout-redo §9.2; v3 is conditional on downstream demand only.
   Flagged here for visibility, not for action.

---

*Map compiled 2026-06-23 by Claude (Opus 4.7 1M) in producer-mode
under user authorisation per [CONVENTIONS §1.1](CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default).
Authorising user: Willem. Reads against the Wiggers source register
([wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md))
and the current state of
[docs/research/analyses/hypotheses/](analyses/hypotheses/) +
[docs/research/analyses/descriptive/](analyses/descriptive/) +
[docs/research/methodology/](methodology/). Snapshot in time; will
need refreshing as HA-C4c lands, as HA-C3 v2 dispatches, as the
cross-test interpretation pass fires, and as the deferred H1
Wiggers-direction lag test / G3 KNMI join / F-family sleep dimensions
eventually get pre-registered.*
