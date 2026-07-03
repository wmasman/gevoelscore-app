# Methodology -- post-crash exertion relapse (the "danger window") test

**Status**: **DESIGN, PROPOSED** (2026-07-03). Producer-mode methodology
framework for a pre-registered inferential test. Locks the operationalisation
and its four-input reasoning per [CONVENTIONS §2.2](../CONVENTIONS.md) BEFORE
the outcome is inspected. Backed by the descriptive precondition
[`../analyses/descriptive/post_crash_exertion_relapse/precondition.md`](../analyses/descriptive/post_crash_exertion_relapse/precondition.md).
Requires a fresh-session `/research-methodology-review` before the pre-reg
locks. Drafted by Claude (Opus 4.8), for the participant-researcher (repo
owner).

> "stress" anywhere here = Garmin HRV-derived stress score (GSS), not mental
> stress. "Exertion" = **physical** activity load (`eff_exertion`), NOT
> cognitive / emotional / orthostatic load (see decision g).

## 1. The hypothesis and mechanism

After a crash, the felt-state rebounds in ~2-3 days but the autonomic system
settles over ~2 weeks (R9; the autonomic channel is the slowest to recover,
Radin 2021). During that mismatch -- the **danger window**, felt-recovered but
autonomically-unsettled -- the PEM threshold is transiently **lowered**, so a
single **supra-threshold physical exertion spike** is more likely to trip a
relapse than the same spike at baseline. This is the pacing rationale,
quantified: *feeling fine is not the same as being recovered.*

## 2. The four inputs (CONVENTIONS §2.2)

Each major decision below is justified against: **[L] literature**,
**[D] this dataset / coverage**, **[M] methodology / statistics**, **[P]
project fit**.

## 3. Design decisions

### (a) Trigger events: crashes primary, dips as a mechanism control
- **Choice**: t0 = felt-state nadir. **Crashes (n=29) primary**; **dips (n=79)
  a mechanism control.**
- **[L]** PEM follows exertion; crashes are the PEM-class events. **[D]** HA-P6
  + R9: crashes carry a distinctive post-crash autonomic signature (4/7
  channels distinguishable from matched controls); dips do NOT (flat overnight
  stress). **[M]** the dip arm is a falsification lever: if premature exertion
  raises relapse after crashes but NOT after dips, the mechanism is
  autonomic-window-specific, not "any low day." **[P]** matches the site's
  crash-vs-dip framing (R13).

### (b) Felt-recovered gate: `gevoelscore >= 4`
- **Choice**: the danger window opens at the first day in t+1..t+10 with
  `gevoelscore >= 4`.
- **[D]** the felt-state clusters at 4-5 (p25=4); <=3 is the crash/dip zone;
  >=4 = "back to normal for this body." **[L]** the felt-fast rebound is the
  literature-expected symptom recovery preceding physiological recovery.
  **[M]** coverage is not a bottleneck (28/29 crashes, 79/79 dips reach it;
  precondition §3). **[P]** the gevoelscore is the project's ground-truth
  felt-state.

### (c) Danger window: felt-recovery day .. nadir+10
- **Choice**: exertion is assessed from the felt-recovery day through nadir+10.
- **[L]** the autonomic-settle window is ~2 weeks (Moore 2023 ~12.7d recovery;
  Radin RHR ~79d, so 10d is a conservative inner window). **[M]** a longer
  window trades power for dilution; 10d captures the mismatch without reaching
  into the next ordinary baseline. **[P]** consistent with R9's ~2-week stress
  settle.

### (d) Exposure: continuous peak (threshold-crossing) primary; cumulative secondary
- **Choice**: **PRIMARY = the peak single-day `eff_exertion_rank_lagged_lcera`
  in the danger window, as a continuous dose-response** (threshold-crossing
  model). **SECONDARY = cumulative load** (count of shock-days / summed rank)
  as a competing predictor (dose-accumulation model). Baseline is **lagged,
  era-local** ([d-90,d-30], LC-era days).
- **[L]** PEM's demonstrated mechanism is **single-bout threshold suppression**
  (2-day CPET, Workwell/Keller/Lien; VT1-as-PEM-threshold, ~24h HRV
  suppression after one crossing). The cumulative "dose-accumulation" model is
  *clinical inference, never physiologically measured* (`push crash
  research.md`), and no study has pitted the two against each other -- so peak
  is primary (the evidenced mechanism) and cumulative is a genuinely novel
  competing arm. **[D]** the precondition (§3.1) found a binary ">=1 day
  >=0.75" exposure is **degenerate** (86% exposed, no contrast); the peak is a
  continuous 0.60-1.00 gradient (median 0.93) that restores contrast. **[M]**
  the lagged-lcera baseline measures a spike **relative to current LC-era
  capacity**, which is essential because the exertion envelope shrank sharply
  over the LC era (the deconditioning finding: ~15kg / VO2Max 52->37); a fixed
  baseline would mis-scale, a naive rolling one would rebase into the ramp
  (CONVENTIONS §3.2). It is self-cleaning against crash contamination (the
  [d-90,d-30] window reaches back before the crash). A continuous dose also
  dodges HA01c's threshold-monotonicity trap. **[P]** inherits HA01c's locked
  operand (`eff_exertion_rank_lagged` shock, SUPPORTED, load-bearing withheld
  on exactly that monotonicity ambiguity), refining it to the danger-window
  conditional.

### (e) Outcome: new crash OR dip within ~4 days of the spike
- **Choice**: relapse = a new crash/dip within **4 days** of the peak-exertion
  day; **3/4/5-day sensitivity band**.
- **[L]** PEM onset is **delayed** (12-72h+), so a same-day outcome would miss
  it and a long window would over-capture ordinary fluctuation; ~4d fits.
  **[M]** report the sensitivity band, not a single window. **[P]** the
  crash/dip labels are the project's event definitions.

### (f) Null + inference
- **Choice**: dose-response of relapse on peak exertion, with a
  **block-permutation / stationary-bootstrap null at E[L] ~ 7**
  ([`permutation_null_block_length.md`](permutation_null_block_length.md)); a
  **base-rate / regression-to-the-mean reference** (relapse is common after
  any low day) is mandatory; a **reverse-causation ordering guard** (the
  exertion peak must strictly precede the relapse, and days already sliding
  into a relapse must not be counted as the exposure).
- **[M]** autocorrelation is heavy (E[L]~7 across this corpus); a naive test
  over-rejects. RTM and reverse causation are the two ways a spurious
  "recover -> push -> relapse" rhythm appears (`pacing-and-crash-mitigation.md`
  flags both). **[P]** single-pool primacy: any over-time difference is a
  number with wide error, never an era verdict.

### (g) Scope: physical exertion only
- **Choice**: the exposure is **physical** (`eff_exertion`); the hypothesis is
  scoped to the physically-visible subset.
- **[L]** "all exertion counts -- cognitive overexertion can crash someone as
  hard as a walk, and a step-counter misses it entirely"
  (`pacing-and-crash-mitigation.md`). **[D]** the mental/emotional/orthostatic
  channels are sparse / absent (the parked R4). **[M]** a relapse with **no
  physical spike is expected noise** (a possible mental-PEM trigger), NOT
  evidence against the hypothesis -- this asymmetry must be stated so a null is
  read correctly. **[P]** keeps this test clean of R4's unresolved proxies.

## 4. Confounds and guards (pre-register these)

1. **Reverse causation.** A brewing relapse can itself suppress exertion (low
   exertion -> crash), or feeling-good days cluster with not-crashing. Guard:
   strict peak-before-relapse ordering; exclude days already inside a
   descending felt-state.
2. **Regression to the mean / base rate.** Relapse is common after any low
   day; the null must be the RTM/base-rate reference, not a naive comparison.
3. **Pacing is not random.** The participant paces on some signals, so the
   exposure is self-selected; the exposure is near-ubiquitous (precondition
   §3.1), so this is a *dose-response* question, not a clean natural
   experiment. State it.
4. **Independence.** The exertion measure (`eff_exertion`, activity data) is a
   different data source from the outcome (`gevoelscore`-based crash/dip
   labels) -- no shared-construct circularity.
5. **n=1, association not causation.** Every result is "consistent with,"
   never proof; CIs are wide (29 crashes); nothing generalises.

## 5. Falsification framing

- **Supported**: peak exertion in the danger window shows a dose-response with
  relapse (beyond the RTM/base-rate null), AND the effect is present for
  crashes but weaker/absent for dips (autonomic-window-specific). The
  threshold-crossing (peak) vs dose-accumulation (cumulative) contrast
  adjudicates the mechanism.
- **Not supported / honest limit**: no dose-response beyond RTM, or
  indistinguishable crash-vs-dip -> the physically-visible danger-window effect
  is not established. Given the pacing self-selection + n=1 + the physical-only
  scope, an honest "cannot resolve" is a valid, publishable outcome.

## 6. Status + open inputs

**DESIGN PROPOSED.** Open inputs (precondition §5): user lock on the decisions
(a)-(g); the RTM/base-rate null construction (decision f); the
reverse-causation ordering guard (decision f/confound 1). Next: fresh-session
`/research-methodology-review`, then the pre-registration (reviewer-mode-with-
authorization, drafted + reviewed in different sessions), then the test.

## 7. Cross-references

- Precondition [`../analyses/descriptive/post_crash_exertion_relapse/precondition.md`](../analyses/descriptive/post_crash_exertion_relapse/precondition.md).
- HA01c [`../analyses/hypotheses/HA01c-effective-exertion-shock/hypothesis.md`](../analyses/hypotheses/HA01c-effective-exertion-shock/hypothesis.md)
  (inherited operand); HA-P6 / HA-P7 (recovery shape / debt); R9
  peri-event-recovery card.
- Literature: `push crash research.md`, `pacing-and-crash-mitigation.md`,
  `reviews/pem_recovery_trajectory_review.md`.
- CONVENTIONS §2.2 (four-input), §3.2 (lagged-lcera baseline), §3.5 (no-peek),
  §3.6 (named counts); `permutation_null_block_length.md`.
