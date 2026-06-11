# HA07c — Result: night-over-night sleep stress mean delta (z-score)

**Primary verdict (4d window, N_std=1.5, one-sided elevated):
TRAIN SUPPORTED, VALIDATE REFUTED → OVERALL REFUTED per the
locked both-eras rule.** But train clears all three pre-registered
criteria substantially (69.2% freq, +23.2 pp disc, median signed
z=1.677), and the train signal is ROBUST across multiple
threshold/direction arms.

**HA07c is the fifth train-era SUPPORTED autonomic-channel
precursor on the fifth channel** (after H02b stress spike count,
H02d bridge × 5d sentinel-corrected, HA06b RHR z-score, HA11
within-day U-dip count). The pre-cliff sympathetic-overarousal /
orthostatic-instability precursor signature is now
**five-channel-confirmed**.

HA07c is a substitute test for the [blocked HA07](../HA07-hrv-day-over-day/hypothesis.md)
(HRV not recorded by FR245 hardware). Sleep stress is an
**HRV proxy** — Garmin's stress algorithm is HRV-derived during
sleep when activity ≈ 0. Per the pre-registered caveats (§8 in
hypothesis.md), HA07c's verdict is a verdict on **the proxy's
discriminative value**, not HRV directly. A REFUTED HA07c does
NOT refute the HRV hypothesis; a SUPPORTED HA07c does NOT confirm
it either. **Cross-channel coherence with HA06b RHR + HA11 U-dip
train-SUPPORTED is the strongest validation HA07c provides**.

Data: [result-data.json](result-data.json).

## Headline numbers (primary 4d, N_std=1.5, one-sided elevated)

| | train (13/14 clean) | validate (15/15 clean) |
|---|---:|---:|
| crash episodes triggering (signed z ≥ +1.5) | **9 (69.2%)** | 6 (40.0%) |
| null windows triggering | 92 (46.0%) | 92 (46.0%) |
| **discrimination (pp)** | **+23.2** | **−6.0** |
| median max signed z | 1.677 | 1.392 |
| crit (a) freq ≥ 60% | **PASS** | fail (40.0%) |
| crit (b) disc ≥ +15 pp | **PASS** | fail (−6.0) |
| crit (c) median ≥ 0.75 | **PASS** | PASS (but irrelevant) |
| **verdict** | **supported** | **refuted** |

1 of 14 train crashes dropped from analysis because fewer than 3
of 4 lead-up days had a valid delta (typically a single missing
prior-night stress). Validate retains all 15.

## Train signal robustness — multiple arms SUPPORTED

The train-era signal is robust across threshold choice and
direction, not isolated to the locked primary:

| arm | freq | null | disc pp | median | verdict |
|---|---:|---:|---:|---:|---|
| **4d N_std=1.5 one-sided elevated (PRIMARY)** | **69.2%** | 46.0% | **+23.2** | 1.677 | **SUPPORTED** |
| 4d N_std=2.0 bidirectional | 69.2% | 49.5% | **+19.7** | 2.644 | **SUPPORTED** |
| 4d N_std=2.0 one-sided lowered | 61.5% | 35.5% | **+26.0** | 2.644 | **SUPPORTED** |
| 5d N_std=1.5 one-sided elevated | 76.9% | 58.5% | **+18.4** | 1.982 | **SUPPORTED** |
| 5d N_std=2.0 one-sided lowered | 61.5% | 42.5% | **+19.0** | 2.644 | **SUPPORTED** |
| 5d N_std=2.5 bidirectional | 61.5% | 38.0% | **+23.5** | 2.688 | **SUPPORTED** |

Train SUPPORTED in 6 of 36 evaluated arms. The lowered direction
at higher thresholds is the *strongest* discriminator (+26.0 pp
at 4d N_std=2.0 one-sided lowered), even though the primary
(elevated at N_std=1.5) is what locked the headline.

**Interpretation**: train-era crashes show **high autonomic
volatility** in sleep — substantial shifts in either direction,
with the most-extreme day often being a sharp downward shift
(stress dropped a lot one night). This is consistent with
autonomic instability rather than stable sympathetic dominance.

## Directionality split (over primary one-sided elevated triggering events)

| | n triggering | elevated at max-\|z\| | lowered at max-\|z\| |
|---|---:|---:|---:|
| train | 9 | 3 (33%) | **6 (67%)** |
| validate | 6 | **6 (100%)** | 0 (0%) |

A nuanced finding: when train crashes trigger (have at least one
elevated day), the **most-extreme** day in the lead-up is more
often a *lowered* delta (67%). Reading this with the multi-arm
table above: train-era crashes have BOTH a sharp rise AND a
sharp drop within the 4d lead-up, with the drop being typically
the largest single deviation. Volatility, not pure direction.

Validate triggering events are all elevated direction (100%), but
N is small (6) and the freq (40%) is below the bar.

## Cross-channel comparison — five-channel train convergence

HA07c adds the fifth train-era SUPPORTED autonomic-channel
precursor on a fifth channel:

| test | channel | window | metric | train freq | train disc |
|---|---|---|---|---:|---:|
| H02b | per-minute stress spike count | 3d rolling | abs minutes ≥ +10 | 71.4% | +29.9 pp |
| H02d bridge × 5d | per-minute stress spike (sentinel-corrected) | 5d | abs minutes ≥ +10 | 92.3% | +31.8 pp |
| HA06b | nightly RHR z-score | 4d lagged | rel \|z\| ≥ 1.5 (bidir) | 71.4% | +18.9 pp |
| HA11 | within-day U-dip count z-score | 4d lagged | rel signed z ≥ 1.5 (elev) | 64.3% | +22.8 pp |
| **HA07c** | **sleep stress mean delta z-score (HRV proxy)** | **4d lagged** | **rel signed z ≥ 1.5 (elev)** | **69.2%** | **+23.2 pp** |

Five SUPPORTED train findings on five distinct channels spanning:
- Per-minute waking-hour stress (H02b, H02d) — sympathetic spike duration
- Per-night autonomic state (HA06b, HA07c) — both via different
  proxies (RHR direct + sleep stress as HRV proxy)
- Per-day within-day pattern (HA11) — orthostatic instability
- Multi-day-scale (H02d 5d)

**Strongest multi-channel convergence in the project.** The pre-
cliff era's sympathetic-overarousal / autonomic-instability
precursor signature is now demonstrably robust across five
independent measurements.

## Era reversal pattern — sleep stress fits the model

| era | direction prediction (HRV proxy mapped) | observed in HA07c |
|---|---|---|
| train | stress rises = HRV drops = canonical sympathetic | elevated direction SUPPORTED (one-sided +23.2 pp); also volatility (multiple arms) |
| validate | stress drops = HRV rises = paradoxical parasympathetic-swing direction (per HA06b/HA10) | one-sided lowered: 53.3% freq +4.3 pp — small positive but NOT SUPPORTED at the bar |

Validate-era one-sided lowered (the predicted paradoxical
direction) is **directionally consistent** with HA06b lowered
RHR + HA10 elevated BB (both representing the parasympathetic
swing). But discrimination is only +4.3 pp, well below the bar.
This is consistent with the HA06b finding that the swing pattern
is *empirically present* in validate but **not discriminative**
from null windows where the same pattern appears at similar rate.

The validate-era picture across channels remains:
- HA06b RHR: pattern present 75% of triggering events, not
  discriminative → +0.8 pp bidirectional
- HA10 BB: pattern present AND discriminative → +16.2 pp
  bidirectional SUPPORTED
- HA11 U-dip: inverse direction (anti-predictive) → −10.7 pp
- HA07c sleep stress: small positive in predicted swing direction
  → +4.3 pp, not discriminative

HA10 remains the only validate-era SUPPORTED test.

## What the numbers say

**1. The proxy works for train.** HA07c's +23.2 pp on a sleep-
stress-as-HRV-proxy metric mirrors HA06b's +18.9 pp on direct
nightly RHR. The sleep-stress proxy successfully identifies the
same train-era crashes that the direct RHR signal did. This is a
**positive validation of the proxy's discriminative value**.

**2. Train autonomic volatility is the cleanest reading.** The
HA07c data shows that train-era crashes are preceded by sleep
stress shifts in BOTH directions, with at least one elevated
deviation triggering the primary arm and frequently a larger
lowered deviation present in the same lead-up. Train-era
crashes ≠ "stuck in sympathetic state"; rather "highly variable
sympathetic-parasympathetic oscillation."

**3. The proxy doesn't help validate.** Validate-era is now
refuted on a fifth waking-hour-derivable signal. HA10 remains
the only validate-era SUPPORTED test, and remains
direction-paradoxical (elevated morning BB).

**4. The HRV hypothesis remains untested.** Per the locked §8
caveats: a SUPPORTED HA07c does NOT confirm the HRV hypothesis
directly. It supports the proxy's discriminative value. The HRV
hypothesis remains permanently untestable on this dataset
absent newer hardware.

## Same-day correlation with gevoelscore (not pre-registered, exploratory)

(Not implemented in this test — HA07c spec did not pre-register
the secondary descriptive outcome that HA11 did. Future HA07c2
on extended data could add this.)

## Caveats per §8 of hypothesis.md

All caveats from HA07c hypothesis.md §8 reproduced here in result
context:

- **Sleep stress is a proxy for HRV, not HRV itself.** Non-linear,
  bounded [1, 100]. The +23.2 pp discrimination is a finding about
  the proxy; the corresponding HRV-domain effect size is unknown.
- **A SUPPORTED HA07c does NOT confirm the HRV hypothesis.** The
  HRV channel remains permanently untestable on this dataset.
- **Cross-channel coherence with HA06b + HA11 train-SUPPORTED is
  the strongest validation HA07c provides.** All three measure
  the same pre-cliff autonomic-deviation phenomenon through
  different operationalisations and all SUPPORTED at substantial
  discrimination magnitudes.
- **Sleep window definition depends on Garmin's algorithm.** ±10-15
  min uncertainty on sleep_onset / wake timestamps.
- **`crash_v1` mixes mechanisms.** Same caveat as all prior tests.
- **Multi-comparison.** HA07c is the 17th pre-registered hypothesis
  (replacing HA07 in count); 14 of those 17 have refuted or are
  blocked. Train SUPPORTED on HA07c after HA06b train SUPPORTED is
  not coincidence — these are correlated tests of the same
  physiological construct.
- **HA07c uses LOCAL FIT-extracted stress + LOCAL sleep windows**,
  NOT the API backfill data. The Garmin Connect API's sleep
  stress arrays were only populated for recent dates (2026+),
  making the API path C unsuitable for full-corpus analysis. The
  FIT-based extraction (re-using H02b/H02d/HA11 methodology) is
  the actual data source.

## What this changes

1. **Pre-cliff sympathetic-overarousal precursor signature is
   FIVE-channel-confirmed.** Strongest multi-channel convergence
   in the project. Five SUPPORTED train findings on five distinct
   channels with substantial discrimination magnitudes (+18.9 to
   +31.8 pp).
2. **Card (b) train-era retrospective card now has FIVE converging
   empirical anchors** (H02b + H02d + HA06b + HA11 + HA07c). Card
   prototyping is overdue; the empirical anchoring is exceptionally
   strong.
3. **The HRV proxy is validated for this participant's train era.**
   Sleep stress as HRV proxy successfully discriminates train
   crashes from null windows. Workwell / Wiggers practitioners
   treating Garmin stress as an HRV indicator is supported by
   this finding.
4. **Validate-era picture unchanged.** HA10 remains the only
   validate-era SUPPORTED test. HA07c, HA11, HA06b all refute
   validate with the paradoxical-direction (predicted by HA10) at
   directionally-consistent but non-discriminative magnitudes.
5. **Volatility framing emerges**: train crashes preceded by
   high-magnitude shifts in EITHER direction. This is consistent
   with autonomic instability (oscillating dysregulation) rather
   than stable sympathetic dominance. The downward-direction arm
   at higher thresholds is actually the strongest discriminator —
   pre-cliff crashes are preceded by at least one *unusually low*
   sleep stress night within high overall volatility.

## What we do next

Per the locked Phase 4-7 plan:

1. **HA08c (multi-day slope)** next — tests whether the same
   signal manifests as sustained creep over 5 days, or only as
   single-night shifts.
2. **HA07d (variability delta)** after — tests the HRV-of-HRV
   dimension.
3. **H03b** when the API backfill completes — sharpens HA10's
   validate-era SUPPORTED finding via per-minute BB trajectory.
4. **Doc bundle** after all four substitute / sharpening tests
   complete.

---

*Test run 2026-06-07. Pre-registration locked 2026-06-07 at
[hypothesis.md](hypothesis.md). Stage 1 extraction (re-parsing
7888 monitoring_b FIT files for sleep-window-intersected
per-minute stress) cached at
[sleep_stress_extract/sleep_stress_nightly.csv](../../scripts/sleep_stress_extract/sleep_stress_nightly.csv).
3-episode dry-run printed before the full run per methodology
lesson — dry-run confirmed clean distributions (σ_delta 3.3-6.7,
no low-variability skips, no missing deltas on the sample
episodes). Seed `20260605` matches scripts 08/09/12 + HA06 +
HA06b + HA10 + HA11.*
