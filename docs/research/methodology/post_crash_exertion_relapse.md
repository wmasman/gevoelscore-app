# Methodology -- post-crash exertion relapse (the "danger window") test

**Status**: **DESIGN, PROPOSED r3** (2026-07-04). Producer-mode methodology
framework for a pre-registered inferential test. Locks the operationalisation
and its four-input reasoning per [CONVENTIONS §2.2](../CONVENTIONS.md) BEFORE
the outcome is inspected. **r2** absorbed the fresh-session methodology review
[`../reviews/methodology-post_crash_exertion_relapse-2026-07-03.md`](../reviews/methodology-post_crash_exertion_relapse-2026-07-03.md)
(ACCEPT-WITH-MINOR-REVISIONS, no-peek HELD): the null, crash-vs-dip control,
and power/multiplicity are constructions, not intentions. **r3** swaps the
primary exposure to a **cardiac-strain** measure to answer the documented
step-count / activity-volume confound ("step count measures how much someone
walks, not how they walk"; the activity axis is only rho~0.42-0.54 with cardiac
strain -- decision d). Backed by the precondition
[`../analyses/descriptive/post_crash_exertion_relapse/precondition.md`](../analyses/descriptive/post_crash_exertion_relapse/precondition.md).
Drafted by Claude (Opus 4.8), for the participant-researcher (repo owner).

> "stress" = Garmin HRV-derived stress score (GSS), not mental stress.
> "Exertion" = **physical** activity/cardiac load, NOT cognitive / emotional /
> orthostatic load (decision g).

## 1. The hypothesis and mechanism

After a crash, the felt-state rebounds in ~2-3 days but the autonomic system
settles over ~2 weeks (R9; autonomic is the slowest channel, Radin 2021).
During that mismatch -- the **danger window**, felt-recovered but
autonomically-unsettled -- the PEM threshold (a **cardiac / HR threshold**,
VT1-class) is transiently **lowered**, so a single **supra-threshold cardiac
exertion spike** is more likely to trip a relapse **than the same-magnitude
spike at baseline**. *Feeling fine is not the same as being recovered.*

## 2. The four inputs (CONVENTIONS §2.2)

Each major decision is justified against **[L] literature**, **[D] this dataset
/ coverage**, **[M] methodology / statistics**, **[P] project fit**.

## 3. Design decisions

### (a) Trigger events: crashes primary, dips as a mechanism control
- **Choice**: t0 = felt-state nadir. **Crashes (n=29) primary**; **dips (n=79)
  a mechanism control**, tested as a formal interaction (§3f-iv), not a
  side-by-side eyeball.
- **[L]** PEM follows exertion; crashes are the PEM-class events. **[D]** HA-P6
  + R9: crashes carry a distinctive post-crash autonomic signature; dips do NOT
  (flat overnight stress). Dip-window peak-exposure is comparable to crash-window
  (precondition §3.2). **[M]** the dip arm is a falsification lever ONLY as a
  slope interaction with base-rate conditioning (§3f-iv). **[P]** matches the
  site's crash-vs-dip framing (R13).

### (b) Felt-recovered gate: `gevoelscore >= 4`
- **Choice**: danger window opens at the first day in t+1..t+10 with
  `gevoelscore >= 4`.
- **[D]** felt-state clusters at 4-5 (p25=4); <=3 = crash/dip zone; coverage is
  not a bottleneck (28/29, 79/79 reach it). **[L]** the felt-fast rebound
  precedes physiological recovery. **[M]** this gate is the ONLY available
  ordering sensor and it is known to lag the autonomic state -- a limitation,
  not a clean guard (§3f-iii). **[P]** the gevoelscore is the ground-truth
  felt-state.

### (c) Danger window: felt-recovery day .. nadir+10
- **Choice**: exertion assessed from the felt-recovery day through nadir+10;
  **7/10/14-day sensitivity band**.
- **[L]** the autonomic-settle window is ~2 weeks (Moore 2023 ~12.7d; Radin
  RHR ~79d). **[D]** ~235 crash danger-window days over 28 windows (precondition
  §3); 10d captures the mismatch without reaching the next ordinary baseline.
  **[M]** longer window trades power for dilution; report the 7/10/14
  sensitivity. **[P]** consistent with R9's ~2-week stress settle.

### (d) Exposure: peak cardiac strain (threshold-crossing) primary; activity-volume comparison; cumulative-strain secondary
- **Choice**: **PRIMARY = the peak single-day `max_hr_rank_lagged_lcera`**
  (peak HR relative to current LC-era capacity, the max single day) in the
  danger window, as a **continuous dose-response with a pre-locked link** (the
  pre-reg fixes the form -- default: relapse-rate monotone in peak rank,
  reported as a rank-slope with CI -- no alternative substituted post-hoc).
  **COMPARISON ARM = `eff_exertion_rank_lagged_lcera`** (activity-volume, the
  HA01c operand). **CUMULATIVE-STRAIN SECONDARY = `hr_area_above_daytime_baseline_waking_lcera`**
  (cardiac-load integral, the dose-accumulation competitor). All lagged,
  era-local ([d-90,d-30], LC-era days).
- **[L]** PEM's evidenced mechanism is single-bout **cardiac** threshold
  suppression (2-day CPET; VT1-as-PEM-threshold; ~24h HRV suppression after one
  crossing), so the faithful threshold-crossing exposure is **peak cardiac
  output relative to current capacity**, not activity volume. This also answers
  a documented confound: **step count / activity volume measures "how much
  someone walks, not how they walk"** (Founder&City 700k-day wearable analysis:
  PEM cases needed ~50% more cardiac work for identical walks; the recommended
  measure is the "cardiac cost of movement," not volume). The cumulative-strain
  arm is the dose-accumulation competitor -- a question the literature flags as
  open (`push crash research.md`).
- **[D]** the confound applies WITHIN-person here: cardiac cost per unit
  activity rises as capacity falls (deconditioning + the low-capacity danger
  window), so an activity-volume exposure under-detects the low-volume cardiac
  threshold-crossings that matter most in the danger window. The two axes
  genuinely diverge: **danger-window day-level rho(max_hr_rank, eff_exertion) =
  +0.42** (precondition §3.4), so the **HR-strain-vs-volume divergence is itself
  an in-sample test of the confound** (if cardiac strain predicts relapse where
  volume does not, "cardiac cost not step count" is confirmed n=1). max_hr_rank
  coverage in danger windows = 235/236; peak distribution median 0.95 (a
  continuous gradient -- the binary is still degenerate at 86%, so the
  continuous peak is used, as for eff_exertion; precondition §3.4).
- **[M]** peak-HR is confound-robust where the HR-integral is NOT:
  `hr_area_above_baseline` sweeps up all-day HR elevation including the resting
  autonomic arousal that IS the danger-window state (conflating exposure with
  the outcome-adjacent state), whereas a peak-HR SPIKE is activity-driven -- so
  max_hr is the cleaner threshold-crossing sensor and `hr_area` is kept only as
  the cumulative-strain secondary (where the conflation is disclosed). The
  continuous form sidesteps HA01c's threshold-monotonicity trap. **Self-cleaning
  caveat**: the [d-90,d-30] baseline self-cleans against the index crash but may
  straddle a neighbouring crash in the dense 2023-24 era -> mask crash/dip days
  from the baseline (un-masked sensitivity).
- **[P]** keeps HA01c's activity operand as the comparison arm (inheritance
  preserved); the peak-vs-integral split maps the cardiac axis onto
  threshold-crossing (primary) vs dose-accumulation (secondary).

### (e) Outcome: new crash OR dip within ~4 days of the spike
- **Choice**: relapse = a new crash/dip within **4 days** of the peak-strain
  day; **3/4/5-day sensitivity band**.
- **[L]** PEM onset is delayed (12-72h+); ~4d fits. **[D]** outcome-*coverage*
  (not values) per 3/4/5-day window is reported in the precondition (coverage,
  no outcome peek). **[M]** the 4d primary is the locked verdict window. **[P]**
  crash/dip labels are the project's event definitions.

### (f) Null + inference -- CONSTRUCTED

- **(i) The baseline reference is a CONSTRUCTED matched comparison.** The
  hypothesis is "more likely than *the same spike at baseline*," so: the
  comparison set is **equal-magnitude peak-strain days OUTSIDE any post-crash
  danger window**, matched on **(1) peak-strain-rank band, (2) deconditioning
  epoch / LC-era stratum, (3) a comparable felt-state trajectory** (so RTM is
  controlled). **The PRIMARY test is the relapse rate of danger-window peaks vs
  matched baseline peaks.** A within-window dose-response is SECONDARY.
- **(ii) The null is EVENT-LEVEL.** With 28 crash windows the relevant n is
  **28 events, not ~1700 days**. The permutation block-permutes the event-level
  danger-window vs matched-baseline labels. The pre-reg reports **(a) the
  day-level ACF of the primary strain metric to justify E[L]=7 or trigger the
  override, and (b) a data-driven E[L]* companion with a factor-of-2 flag**.
- **(iii) Reverse causation -- an irreducible limitation, named.** The ordering
  guard (peak strictly precedes relapse; exclude days already in a descending
  felt-state) covers the crude case but not the subtle one: a **prodromal**
  relapse can suppress activity/HR *before* the felt-state visibly descends, and
  by the design's own premise the felt-state LAGS the autonomic state -- so a
  felt-based exclusion is the wrong sensor. Fix: state this as irreducible; add
  a **sensitivity that also excludes danger-window days whose autonomic channel
  (overnight stress / RHR, the R9 signature) is already trending adverse**;
  treat any residual as a **named directional bias** on the CI.

### (f-iv) Crash-vs-dip as a formal interaction
- **Choice**: a **formal slope interaction** (does the peak-strain-relapse slope
  differ between crashes and dips), NOT two eyeballed verdicts.
- **[M]** (1) **base-rate conditioning**: a dip is milder with a different
  relapse base rate, so "weaker after dips" must be a **slope** difference, not
  a level difference. (2) **power asymmetry stated**: 79 dip windows carry ~2.7x
  the power of 28 crash windows, so effect-on-one / null-on-other is NOT read as
  specificity without accounting for power. (3) **comparable support** confirmed
  (precondition §3.2).

### (g) Scope: physical/cardiac exertion only, with a two-case null-reading
- **Choice**: the exposure is **physical/cardiac** strain; the hypothesis is
  scoped to the physically-visible subset.
- **[L]** "all exertion counts -- cognitive overexertion can crash someone as
  hard as a walk, a step-counter misses it entirely"
  (`pacing-and-crash-mitigation.md`). **[M] two-case null-reading (so scope is
  not immunity)**: (1) a relapse with **no physical/cardiac exposure at all** is
  **out of support** (neutral -- a possible mental-PEM trigger, parked R4); (2)
  an **in-danger-window strain spike that does NOT relapse above the matched
  baseline IS disconfirming** ("the physically-visible danger-window effect is
  not established"). The mental-PEM escape applies ONLY to case (1). **[P]**
  keeps this test clean of R4's unresolved proxies.

## 4. Power, precision, and multiplicity

With **28 event-level units**, a continuous dose-response, n=1, and E[L]~7
autocorrelation, the design is **underpowered for anything but a large effect**.
- **The primary deliverable is an estimate with an honest CI, not a
  reject/accept verdict.** "Cannot resolve" is the **pre-committed default
  reading of a CI that spans the null**; a wide CI is never upgraded to
  "suggestive."
- **The single primary test** is: **peak cardiac strain (`max_hr_rank`) x crash
  arm x 10-day danger window x 4-day relapse window x matched-baseline
  contrast.** Everything else -- the activity-volume comparison arm
  (`eff_exertion`), the cumulative-strain arm (`hr_area`), the dip arm, and the
  3/4/5-day + 7/10/14-day + masked-baseline sensitivities -- is explicitly
  **secondary / comparison / sensitivity**, not promoted to primary if it wins
  (peak-primacy is irrevocable). Effective independent looks ~3-4
  (`permutation_null_block_length.md` §4) must not be silently spent.

## 5. Confounds and guards (pre-register)

1. **Reverse causation** -- §3f-iii (irreducible; felt-gate lags; autonomic
   sensitivity + named directional bias).
2. **RTM / base rate** -- §3f-i (matched felt-state-trajectory reference).
3. **Activity-volume confound** -- decision d (the primary is cardiac strain,
   not step/activity volume; the volume arm is the in-sample confound test).
4. **Pacing is not random** -- exposure is self-selected and near-ubiquitous
   (precondition §3.1); a dose-response question, not a natural experiment.
5. **Independence** -- the cardiac-strain / activity exposures vs the
   `gevoelscore`-based crash/dip outcome are different data sources.
6. **n=1** -- association not causation; single-pool primacy (any over-time
   difference is a number with wide error, never an era verdict).

## 6. Falsification framing

- **Supported**: danger-window peak cardiac strain relapses more than
  matched-baseline peaks (beyond the event-level null), AND the crash-vs-dip
  slope interaction shows autonomic-window-specificity. The strain-vs-volume
  contrast adjudicates the "cardiac cost not volume" confound; peak-vs-cumulative
  adjudicates threshold-crossing vs dose-accumulation.
- **Not supported / honest limit**: no danger-window-vs-baseline difference, or
  no interaction, or a CI spanning the null -> "the physically-visible
  danger-window effect is not established." Given self-selected exposure + n=1 +
  physical-only scope + 28 units, **"cannot resolve" is the honest modal
  outcome** and is publishable.

## 7. Status + open inputs

**DESIGN PROPOSED r3.** For the pre-reg to implement as locked constructions:
the matched-baseline reference set + matching variables (§3f-i); the
event-level permutation + ACF/E[L]* readout (§3f-ii); the crash-vs-dip
interaction model (§3f-iv); the dose-response link (§3d); the autonomic-trend
reverse-causation sensitivity (§3f-iii); the crash/dip baseline masking (§3d).
Note: the null MD's own literature anchor is "deferred" -- E[L]=7 rests on
first-principles + the data-driven companion, not a verified citation. **r3
changes the primary exposure, so the pre-reg's fresh-session review must
re-confirm the exposure choice cold.** Next: pre-registration (reviewer-mode,
drafted + reviewed in different sessions), then the test.

## 8. Cross-references

- Precondition + methodology review (above); HA01c (inherited comparison
  operand); HA-P6 / HA-P7; R9 peri-event-recovery card.
- Literature: `push crash research.md`, `pacing-and-crash-mitigation.md`,
  `reviews/pem_recovery_trajectory_review.md`; the Founder&City 700k-day
  wearable step-count-confound analysis (external, decision d).
- CONVENTIONS §2.2 (four-input), §3.2 (lagged-lcera), §3.5 (no-peek), §3.6
  (named counts); `permutation_null_block_length.md`.
