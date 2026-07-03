# Methodology -- post-crash exertion relapse (the "danger window") test

**Status**: **DESIGN, PROPOSED r2** (2026-07-03). Producer-mode methodology
framework for a pre-registered inferential test. Locks the operationalisation
and its four-input reasoning per [CONVENTIONS §2.2](../CONVENTIONS.md) BEFORE
the outcome is inspected. **r2 absorbs the fresh-session methodology review**
[`../reviews/methodology-post_crash_exertion_relapse-2026-07-03.md`](../reviews/methodology-post_crash_exertion_relapse-2026-07-03.md)
(ACCEPT-WITH-MINOR-REVISIONS, no-peek HELD, 3 MAJOR): the null, the crash-vs-dip
control, and the power/multiplicity statement are now **constructions, not
intentions**. Backed by the precondition
[`../analyses/descriptive/post_crash_exertion_relapse/precondition.md`](../analyses/descriptive/post_crash_exertion_relapse/precondition.md).
The pre-reg (reviewer-mode) implements the constructions below. Drafted by
Claude (Opus 4.8), for the participant-researcher (repo owner).

> "stress" = Garmin HRV-derived stress score (GSS), not mental stress.
> "Exertion" = **physical** activity load (`eff_exertion`), NOT cognitive /
> emotional / orthostatic load (decision g).

## 1. The hypothesis and mechanism

After a crash, the felt-state rebounds in ~2-3 days but the autonomic system
settles over ~2 weeks (R9; autonomic is the slowest channel, Radin 2021).
During that mismatch -- the **danger window**, felt-recovered but
autonomically-unsettled -- the PEM threshold is transiently **lowered**, so a
single **supra-threshold physical exertion spike** is more likely to trip a
relapse **than the same-magnitude spike at baseline**. *Feeling fine is not the
same as being recovered.*

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
  (flat overnight stress). Dip-window peak-exposure (median 0.92) is comparable
  to crash-window (0.93), so the arms span comparable support (precondition
  §3.2). **[M]** the dip arm is a falsification lever ONLY as a slope
  interaction with base-rate conditioning (§3f-iv). **[P]** matches the site's
  crash-vs-dip framing (R13).

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
  RHR ~79d). **[D]** 236 crash danger-window days over 28 windows (precondition
  §3); 10d captures the mismatch without reaching into the next ordinary
  baseline, and gives ~8 usable exposure days/window after the recovery gate.
  **[M]** longer window trades power for dilution; report the 7/10/14
  sensitivity. **[P]** consistent with R9's ~2-week stress settle.

### (d) Exposure: continuous peak (threshold-crossing) primary; cumulative secondary
- **Choice**: **PRIMARY = the peak single-day `eff_exertion_rank_lagged_lcera`**
  (the max single day, locked definition) in the danger window, as a
  **continuous dose-response with a pre-locked link** (the pre-reg fixes the
  functional form -- default: relapse-rate as a monotone function of peak rank,
  reported as a rank-slope with CI -- and NO alternative link is substituted
  post-hoc; this closes the functional-form degree of freedom, review finding
  3). **SECONDARY = cumulative load** (count of shock-days / summed rank) as a
  competing predictor. Baseline: lagged, era-local ([d-90,d-30], LC-era days).
- **[L]** PEM's evidenced mechanism is **single-bout threshold suppression**
  (2-day CPET; VT1-as-PEM-threshold). The cumulative model is clinical-inference
  -only and **no study has pitted the two against each other** (`push crash
  research.md`) -- so peak is primary (evidenced) and **the cumulative arm is
  the genuinely novel contribution**: a cumulative-wins result would be a new
  (n=1, un-generalisable) datapoint on a question the literature flags as open.
  **[D]** a binary ">=1 day >=0.75" exposure is **degenerate** (86% exposed;
  precondition §3.1); the continuous peak (0.60-1.00, median 0.93) restores
  contrast. **[M]** lagged-lcera measures a spike **relative to current LC-era
  capacity** -- essential because the envelope shrank sharply over the LC era
  (~15kg / VO2Max 52->37); a fixed baseline mis-scales, a naive rolling one
  rebases into the ramp (§3.2). **Self-cleaning caveat (review finding 5)**: the
  [d-90,d-30] window closes >=20d before the *index* nadir, so the index crash
  cannot contaminate it; BUT in the dense 2023-24 era (~10 crashes/yr, ~30-40d
  apart) the 60-day window can straddle a *neighbouring* crash and deflate the
  reference (inflating the index rank). Fix: **mask crash/dip days out of the
  baseline computation**, and report the un-masked version as a sensitivity.
  **[P]** inherits HA01c's operand (SUPPORTED, load-bearing withheld on
  threshold-monotonicity -- the continuous form sidesteps that trap).

### (e) Outcome: new crash OR dip within ~4 days of the spike
- **Choice**: relapse = a new crash/dip within **4 days** of the peak-exertion
  day; **3/4/5-day sensitivity band**.
- **[L]** PEM onset is delayed (12-72h+); ~4d fits. **[D]** outcome-*coverage*
  (not values) per 3/4/5-day window is reported in the precondition (a coverage
  count, no outcome peek). **[M]** report the sensitivity band; the 4d primary
  is the locked verdict window. **[P]** crash/dip labels are the project's
  event definitions.

### (f) Null + inference -- CONSTRUCTED (review finding 4, MAJOR)

- **(i) The baseline reference is a CONSTRUCTED matched comparison, not an
  adjective.** The hypothesis is "more likely than *the same spike at
  baseline*," so the baseline must be built: the comparison set is
  **equal-magnitude peak-exertion days OUTSIDE any post-crash danger window**,
  matched on **(1) peak-rank band, (2) deconditioning epoch / LC-era stratum,
  (3) a comparable felt-state trajectory** (so RTM is controlled -- relapse is
  common after any low day, so the reference must condition on a comparable
  felt-state, not just a comparable peak). **The PRIMARY test is the relapse
  rate of danger-window peaks vs matched baseline peaks.** A within-window
  dose-response is SECONDARY: it does not by itself answer "more than baseline."
- **(ii) The null is EVENT-LEVEL.** With 28 crash windows the relevant n is
  **28 events, not ~1700 days** (`permutation_null_block_length.md` §4 flags
  exactly this). The permutation block-permutes the **event-level danger-window
  vs matched-baseline labels**. The pre-reg reports **(a) the day-level ACF of
  `eff_exertion_rank_lagged_lcera` to justify E[L]=7 or trigger the override,
  and (b) a data-driven E[L]* companion with a factor-of-2 flag** (the override
  rule requires this; the E[L]=7 default is not adopted blind).
- **(iii) Reverse causation -- an irreducible limitation, named.** The
  ordering guard (peak strictly precedes relapse; exclude days already in a
  descending felt-state) covers the crude case. It does NOT close the subtle
  one: a **prodromal** relapse can suppress exertion *before* the felt-state
  visibly descends, and by the design's own premise the felt-state LAGS the
  autonomic state -- so a felt-based exclusion is the wrong sensor for a brewing
  relapse. Fix: state this as a limitation the design cannot fully remove; add a
  **sensitivity that also excludes danger-window days whose autonomic channel
  (overnight stress / RHR, the R9 signature) is already trending adverse**; if
  unavailable for some days, treat the residual as a **named directional bias**
  on the CI (it deflates the exposed group's apparent innocence, inflating the
  contrast).

### (f-iv) Crash-vs-dip as a formal interaction (review finding 6, MAJOR)
- **Choice**: NOT two eyeballed verdicts. The contrast is a **formal slope
  interaction**: does the peak-relapse *slope* differ between crashes and dips?
- **[M]** (1) **base-rate conditioning**: a dip is a milder event with a
  different post-event relapse base rate, so "weaker after dips" must be a
  **slope** difference, not a level difference. (2) **power asymmetry stated**:
  79 dip windows carry ~2.7x the power of 28 crash windows, so
  "effect-on-crashes / null-on-dips" (or vice versa) is NOT read as specificity
  without accounting for power -- an underpowered crash arm showing an effect
  while a better-powered dip arm does not is exactly what noise + a small true
  effect produces. (3) **comparable support confirmed**: dip-window peak median
  0.92 vs crash 0.93 (precondition §3.2), so the slopes are compared over
  overlapping exposure ranges.

### (g) Scope: physical exertion only, with a two-case null-reading (review finding 7)
- **Choice**: the exposure is **physical** (`eff_exertion`); the hypothesis is
  scoped to the physically-visible subset.
- **[L]** "all exertion counts -- cognitive overexertion can crash someone as
  hard as a walk, a step-counter misses it entirely"
  (`pacing-and-crash-mitigation.md`). **[M] the two-case null-reading rule (so
  scope is not immunity)**: (1) a relapse with **no physical exposure at all**
  is **out of the test's support** (neutral -- a possible mental-PEM trigger the
  measure never saw; the parked R4); (2) an **in-danger-window physical spike
  that does NOT relapse above the matched baseline IS disconfirming** and is
  reported as "the physically-visible danger-window effect is not established."
  The mental-PEM escape applies ONLY to case (1), never to case (2). **[P]**
  keeps this test clean of R4's unresolved proxies.

## 4. Power, precision, and multiplicity (review finding 8, MAJOR -- in the body)

With **28 event-level units**, a continuous dose-response, n=1, and E[L]~7
autocorrelation, the design is **underpowered for anything but a large effect**.
Therefore:
- **The primary deliverable is an estimate with an honest CI, not a
  reject/accept verdict.** "Cannot resolve" is the **pre-committed default
  reading of a CI that spans the null** -- not a post-hoc consolation, and a
  wide CI is never upgraded to "suggestive."
- **Multiplicity / the single primary test.** The verdict is the CI of **ONE**
  test: **peak exposure x crash arm x 10-day danger window x 4-day relapse
  window x matched-baseline contrast**. Everything else -- the cumulative arm,
  the dip arm, and the 3/4/5-day + 7/10/14-day + masked-baseline sensitivities
  -- is explicitly **secondary / sensitivity**, not promoted to primary if it
  wins (review finding 1: peak-primacy is irrevocable). The effective number of
  independent looks (~3-4, `permutation_null_block_length.md` §4) must not be
  silently spent.

## 5. Confounds and guards (pre-register)

1. **Reverse causation** -- §3f-iii (irreducible; felt-gate lags; autonomic
   sensitivity + named directional bias).
2. **RTM / base rate** -- §3f-i (matched felt-state-trajectory reference).
3. **Pacing is not random** -- exposure is self-selected and near-ubiquitous
   (precondition §3.1); this is a dose-response question, not a natural
   experiment.
4. **Independence** -- `eff_exertion` (activity) vs `gevoelscore`-based
   crash/dip labels are different data sources; no shared-construct circularity.
5. **n=1** -- association not causation; single-pool primacy (any over-time
   difference is a number with wide error, never an era verdict).

## 6. Falsification framing

- **Supported**: danger-window peaks relapse more than matched-baseline peaks
  (beyond the event-level null), AND the crash-vs-dip slope interaction shows
  the effect is autonomic-window-specific (base-rate + power conditioned). The
  peak-vs-cumulative contrast adjudicates the mechanism.
- **Not supported / honest limit**: no danger-window-vs-baseline difference, or
  no crash-vs-dip slope interaction, or a CI spanning the null -> "the
  physically-visible danger-window effect is not established." Given
  self-selected exposure + n=1 + physical-only scope + 28 units, **"cannot
  resolve" is the honest modal outcome** and is publishable.

## 7. Status + open inputs

**DESIGN PROPOSED r2** (review absorbed). Remaining for the pre-reg to
implement as locked constructions: the matched-baseline reference set + its
matching variables (§3f-i); the event-level permutation + ACF/E[L]* readout
(§3f-ii); the crash-vs-dip interaction model (§3f-iv); the dose-response link
(§3d); the autonomic-trend reverse-causation sensitivity (§3f-iii). Note: the
null's own literature anchor (`permutation_null_block_length.md`) is itself
"deferred" -- the E[L]=7 choice rests on first-principles + the data-driven
companion, not a verified citation (transparency item). Next: pre-registration
(reviewer-mode-with-authorization, drafted + reviewed in different sessions),
then the test.

## 8. Cross-references

- Precondition + methodology review (above); HA01c (inherited operand); HA-P6 /
  HA-P7; R9 peri-event-recovery card.
- Literature: `push crash research.md`, `pacing-and-crash-mitigation.md`,
  `reviews/pem_recovery_trajectory_review.md`.
- CONVENTIONS §2.2 (four-input), §3.2 (lagged-lcera), §3.5 (no-peek), §3.6
  (named counts); `permutation_null_block_length.md`.
