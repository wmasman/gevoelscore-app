# HA06 — Result: bidirectional nightly RHR delta as crash precursor

**Primary verdict (4d window, N=5 bpm, bidirectional): REFUTED in
both eras.** Validate-era refutation is decisive (0 of 15 crashes
trigger). Train-era shows a positive direction (+13.9 pp
discrimination, +3.49 bpm median magnitude) but fails the 60%
frequency bar at 21.4%.

The result extends the consistent pattern across the H##/HA## series:
no waking-hour-derivable Garmin signal has produced a clean
validate-era precursor under methodologically clean pre-registration.
This is now true across the RHR channel (H01 + HA06), the stress
channel (H02 + H02b + H02d × 4 arms), and the activity-shock channel
(HA01 + HA01b lagged + HA02c).

No `card.md`. Data: [result-data.json](result-data.json).

## Headline numbers

| | train | validate |
|---|---:|---:|
| crash episodes (clean) | 14 | 15 |
| crash episodes triggering (\|delta\| ≥ 5 bpm) | 3 (21.4%) | 0 (0.0%) |
| null windows triggering | 15 (7.5%) | 15 (7.5%) |
| **discrimination (pp)** | **+13.9** | **−7.5** |
| median max-\|delta\| (bpm) | 3.49 | 1.63 |
| crit (a) freq ≥ 60% | fail | fail |
| crit (b) disc ≥ +15 pp | fail (close, +13.9) | fail |
| crit (c) median ≥ 2.5 bpm | **PASS** | fail |
| **verdict** | **refuted** | **refuted** |

## Sensitivity arm — one-sided (classical Workwell direction)

| | train | validate |
|---|---:|---:|
| crash episodes triggering (delta ≥ +5 bpm) | 2 (14.3%) | 0 (0.0%) |
| discrimination (pp) | +6.8 | −7.5 |
| verdict | refuted | refuted |

**Bidirectional excess over one-sided (train):** +7.1 pp — the
parasympathetic-swing contribution is real but small in absolute
terms (1 extra triggering episode of 14).

## What the numbers say

**1. Validate-era refutation is decisive.** Zero of 15 validate crashes
show *any* RHR deviation ≥ 5 bpm in their 4-day lead-up. This is not a
close miss; it is a complete absence of the signal HA06 was designed
to detect. The N=10 and N=15 sensitivity thresholds yield 0% / 0% for
*both* crash and null windows — the participant's nightly RHR is too
stable for those thresholds to be meaningful at all (median magnitude
is 1.63 bpm; the bar of 5 bpm is already at the practical ceiling).

**2. Train-era result is suggestive but does not clear the bar.** Three
of 14 train crashes (21.4%) trigger, with a +13.9 pp lift over the
7.5% null rate — meaningful direction, close to but not at the
+15 pp discrimination bar, and well below the 60% frequency criterion.
The median max-|delta| in train is 3.49 bpm, which passes the
magnitude criterion (≥ 2.5 bpm = N/2). So the train signal is
directionally consistent with the bidirectional hypothesis but not
strong enough to claim a precursor at the pre-registered bar.

**3. The bidirectional design caught one extra train triggering event
beyond the one-sided arm.** The parasympathetic-swing contribution to
the train bar is +7.1 pp (one extra of 14 episodes). This is
non-zero, but with only 3 triggering events total the directionality
split (2 elevated, 1 lowered) is underpowered to make a strong claim
either way. The swing pattern Wiggers documented is *present* in the
data but is not a dominant signal for this participant's crashes.

**4. RHR magnitudes are smaller than the pre-registered thresholds
assumed.** Wiggers' "5-10 al ontevreden" floor turned out to be at the
upper end of what this participant's RHR varies by. Her own data
shows daily RHR moves of 5-10 bpm; this participant's lagged-baseline-
relative deviation is typically 1-3 bpm. The pre-registered bar was
calibrated to a person with more RHR variability than this one.

**5. Pre-registration discipline held.** The thresholds were locked
before any test ran. The dry-run print verified the data shape but
did not change the spec. The result is honestly reported regardless
of how it falls.

## Cross-channel comparison

HA06 joins a now-substantial list of pre-registered waking-hour-
signal tests that have failed to produce a clean validate-era
precursor under the lagged-baseline / cleanest-methodology bar:

| channel | test | verdict | source |
|---|---|---|---|
| RHR (7-day mean, one-sided, rolling baseline) | H01 | refuted both eras | [H01](../H01-rhr-drift/result.md) |
| **RHR (nightly, 4d/5d bidirectional, lagged baseline)** | **HA06** | **refuted both eras** | this result |
| Daily-avg stress | H02 | train: direction; validate: null | [H02](../H02-stress-elevation/result.md) |
| Stress spike (3d, rolling) | H02b | train SUPPORTED; validate near-miss | [H02b](../H02b-stress-spikes/result.md) |
| Stress spike (4d / 5d × {imputed, bridge}) | H02d × 4 arms | bridge × 5d train +31.8 pp project-strongest; validate refuted all 4 arms | [H02d](../H02d-stress-spikes-uncensored/result.md) |
| Sleep efficiency | H03 | refuted both eras | [H03](../H03-sleep-efficiency/result.md) |
| Body-battery net delta | H04 | refuted both eras (validate near-miss +13.3 pp) | [H04](../H04-body-battery/result.md) |
| Activity shock (3d) | HA01 | refuted both eras | [HA01](../../activity-labels/output/ha_results.md) |
| Activity shock (4d, rolling) | HA01b | train refuted; validate originally SUPPORTED, withdrawn | [HA01b](../../activity-labels/output/ha_results_4day.md) |
| Activity shock (4d, lagged) | HA01b-recomputed | refuted both eras | [bundled re-test](../../activity-labels/output/ha_results_4day_lagged.md) |
| Push burden (4d, lagged) | HA02c | refuted both eras | [bundled re-test](../../activity-labels/output/ha_results_4day_lagged.md) |

**Eleven pre-registered tests** across four channels, on data
captured at three time-resolutions (per-minute, per-night, per-day),
have now run on this participant's full corpus under
methodologically clean pre-registration. **None has produced a
validate-era precursor.** The only SUPPORTED-overall test in the
project remains a counterfactual: H02b train SUPPORTED in isolation
(refuted overall by validate); H02d bridge × 5d train SUPPORTED in
isolation (refuted overall by validate); HA01b initially reported
SUPPORTED but withdrawn after Theme A.

## Caveats per §8

- **Chronotropic incompetence**: >85% of ME/CFS patients have a
  blunted HR response (Workwell's own caveat). HA06 REFUTED here is
  *consistent with* "the HR channel is blunted for this participant"
  — not necessarily "overnight recharge is fine." HA07 (day-over-day
  HRV drop ≥ 10 ms) is the natural follow-up because HRV is less
  subject to chronotropic blunting; it tests the same overnight-
  recharge mechanism through a different physiological signal.
- **Medication-shift confound (Wiggers)**: not formally pre-checked.
  Visual inspection of the per-episode RHR + baseline values in the
  dry-run did not surface a step-shift consistent with a medication
  change. Worth a follow-up check if HA06b is ever considered.
- **Watch-off coverage gap**: not a factor here. Night coverage is
  99.4% train, 98.6% validate — essentially complete. The refutation
  is not driven by missing data.
- **`crash_v1` mixes mechanisms.** Same caveat as all prior precursor
  tests. The dry-run showed clear per-episode heterogeneity in delta
  magnitudes (e.g., 2022-09-30 had max|delta| of only 1.39 bpm at 4d
  while 2022-09-03 had 5.35 bpm) but the population-level frequency
  is what governs the bar.
- **Multi-comparison.** HA06 is the 12th pre-registered hypothesis
  in the H##/HA## series and the 11th to refute (or be partial /
  withdrawn) on validate. The held-out validate window has done its
  defensive work: it is genuinely hard to find a clean validate-era
  precursor in the data we have.
- **Same-day overlap with H02d / HA01b**: not analysed here because
  the validate-era trigger count is 0. The cross-mechanism
  convergence question becomes moot when nothing triggers.

## Wiggers-pdf-specific findings

The lived-experience patterns from Wiggers' pdf that motivated HA06's
design changes are present in the data but not dominant:

- **Bidirectional pattern (parasympathetic-swing)**: present but
  small. Train added one extra triggering event over the one-sided
  arm (+7.1 pp contribution). Of the 3 train triggering events,
  2 were elevated (classical Workwell direction) and 1 was lowered
  (swing). The pattern is real but not the dominant signal.
- **Lowest stable nightly HR field**: confirmed appropriate. Garmin's
  `restingHeartRate` field maps cleanly to the bottom of the
  night-sleep-HR graph and is what Wiggers' framing points at.
- **Multi-day window** (4-5 days): both windows produced the same
  verdicts (refuted) at the same thresholds. The lag profile that
  H02d and HA01b's exploratory analysis identified does not transfer
  to the RHR channel for this participant.
- **Magnitude calibration**: the pre-registered thresholds (5/10/15
  bpm) were drawn from Wiggers' own RHR-variability range and the
  Workwell rule. **For this participant, those thresholds are
  effectively unreachable** — typical max-|delta| sits at 1.6-3.5 bpm
  across both eras. Future HA06b on truly new data would need
  participant-specific threshold calibration (a priori, blinded to
  outcome) before re-running.

## What this changes

1. **The RHR channel is now closed for this participant.** H01 (one-
   sided, rolling baseline, 7d) and HA06 (bidirectional, lagged
   baseline, 4d/5d) both refuted. The RHR signal does not carry a
   clean precursor under any of the operationalisations we have
   pre-registered.
2. **The waking-hour Garmin signal space is now exhausted under
   clean methodology.** Eleven pre-registered tests across four
   channels, all refuted on validate. The direction shifts firmly to
   overnight recovery via H04b (per-minute Body Battery decode).
3. **HA07 (day-over-day HRV drop ≥ 10 ms) becomes the immediate
   follow-up.** HRV is less subject to chronotropic incompetence
   than HR and tests the same overnight-recharge mechanism. If HA07
   also refutes, the validate-era is precursor-invisible in every
   waking-hour-derivable signal we have access to, and the case for
   H04b's per-minute BB decoding (the gate for H03b overnight
   recharge) becomes the strongest remaining lead.
4. **The D7 single-mechanism-two-regimes reframe loses another
   candidate anchor.** HA06 was the strongest external-evidence
   candidate to provide the empirical stake. It does not. The
   reframe is not falsified but remains supported by literature
   parsimony only; the empirical anchor has not yet been provided
   by any test in our pre-registered series.
5. **The Wiggers pdf input remains valuable methodologically.** The
   bidirectional design caught a real-but-small parasympathetic-swing
   signal in train; the lowest-stable-nightly-HR framing was
   confirmed. The pdf's prior calibrations (5-10 bpm RHR floor) are
   well-aligned with the threshold-dynamics literature but do not
   match this participant's actual RHR variability — which is itself
   informative.

## What we do next

Per QUEUED-WORK.md C.1 § "What we do with each outcome":

> Refuted in both windows → the RHR channel is closed for this
> participant. Combined with all prior refutations, this is the 6th
> pre-registered test on the autonomic-channel family (broadly) to
> refute, and the direction shifts firmly to overnight recovery via
> H04b. HA07 (HRV channel) is the natural follow-up; if HA07 also
> refutes, the validate-era is precursor-invisible in every
> waking-hour-derivable signal we have access to.

Next on queue: **HA07 — day-over-day HRV drop ≥ 10 ms** (the
*vermoeidheidskliniek* rule), per QUEUED-WORK.md autonomic-channel
sibling hypotheses §. Uses the same UDS data source (nightly HRV
field), the same lagged baseline construction, the same bar.

After HA07 — regardless of outcome — bundle the doc-level updates
into addendum + STOCKTAKE + synthesis + indicators doc + registry to
reflect HA06 (+ HA07 if it runs).

---

*Test run 2026-06-07. Pre-registration locked 2026-06-07 at
[hypothesis.md](hypothesis.md). 3-episode dry-run printed before the
full run per methodology lesson. Seed `20260605` matches scripts
08/09/12.*
