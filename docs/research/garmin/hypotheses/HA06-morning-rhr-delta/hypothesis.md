# HA06 — Bidirectional nightly resting-HR delta as crash precursor

**Pre-registration written 2026-06-07, before any data was inspected for
this test.** Locked. Any subsequent change creates an HA06b.

HA06 is the next pre-registered precursor test after Theme A refuted
HA01b on the lagged baseline (2026-06-06) and H02d closed the stress
channel for validate-era crashes across all four arms (2026-06-06). It
is the only remaining waking-hour-adjacent candidate before the
direction shifts to overnight recovery via H04b.

HA06 is **not** a re-run of H01. H01 used a 7-day lead-up window
against a 90-day rolling baseline ending 7 days before each episode,
tested one-sided (`RHR > baseline + 3 bpm`), refuted in both
train and validate. HA06's design differs on four locked dimensions:
window (4 + 5 day), baseline construction (lagged per Theme A),
threshold range (5 / 10 / 15 bpm), and **direction (bidirectional)**.
The bidirectional change is motivated by lived-experience input from
Laure Wiggers' *Smartwatch Pacing* pdf (2025-07) describing the
parasympathetic-swing pattern, and is independently consistent with
H01's previously-puzzling validate-era result, which showed slight
inversion (RHR *lower* in lead-up than baseline).

## 1. Claim

In the **4 days** before a `crash_v1` episode (primary) and the
**5 days** before a `crash_v1` episode (secondary), at least one
day's nightly resting heart rate deviates from its lagged personal
baseline by **|RHR − baseline| ≥ N bpm** (N locked below). The
crash-episode frequency of this deviation is discriminative against
randomly-sampled non-crash windows in **both train and validate
windows independently**.

The bidirectional formulation catches both the classical elevated-RHR
pattern (Workwell's "RHR + 10-15 bpm" rule, mechanism: insufficient
overnight autonomic recharge after exertion) AND the
parasympathetic-swing pattern (Wiggers: paradoxical LOW RHR + HIGH
HRV on the night after a heavy day, mechanism: autonomic over-correction
that LOOKS like recovery but predicts continued dysregulation).

## 2. Why we think this

- **Strongest external evidence in the pacing literature.** Bateman
  Horne Center's "back to baseline next morning?" is the central
  practitioner heuristic; Workwell Foundation's morning RHR + 10-15 bpm
  rule is the most-cited operational threshold; Ruijgt/Wüst/Janssen
  2025 ([medRxiv preprint](https://www.medrxiv.org/content/10.1101/2025.03.18.25320115v1.full),
  127 long COVID + 21 controls, the only multi-day continuous HRV/RHR
  dataset in the field) found that HRV stays suppressed for 24h after
  exercise in patients vs 3-6h in controls. The mechanism (overnight
  autonomic recharge) is physiologically sharper than the
  daily-average measurements that H01-H04 used.
- **H01's validate-window result is consistent with bidirectional
  signal.** H01 tested one-sided `RHR > baseline + 3 bpm` and found
  validate REFUTED with slight inversion: RHR was on average ~1 bpm
  *lower* in the 7-day lead-up than the 90-day baseline. The one-sided
  test counts that as "no signal," but it is exactly the
  parasympathetic-swing direction Wiggers describes. HA06's bidirectional
  test treats it as a candidate signal in its own right and reports the
  directionality split.
- **Theme A discipline now applies to RHR baseline.** The 30-day
  rolling RHR baseline that H01 used has the same contamination
  failure mode as Theme A identified for activity ranks: the candidate
  region overlaps with the reference. HA06 inherits the Theme A fix
  (lagged 30-90-day window) and reports the result honestly whether
  SUPPORTED or REFUTED.
- **Lived-experience prior.** Wiggers' pdf documents 5-10 bpm RHR
  deviation as her own threshold for being "ontevreden" with a day,
  which matches Workwell's "RHR + 10-15" lower bound. Two independent
  sources of operational threshold N — well-aligned.

## 3. Data sources

- **Crash labels**: `crash_v1` per registry §2, sourced from
  [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
  Tier-1 `crash` only; dips not included.
- **Nightly resting heart rate**: Garmin UDS `restingHeartRate`
  field, sourced from `UDSFile_*.json` under
  `C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Aggregator\`.
  Same field and extraction logic as H01 (verified).
- **Analysis window**: 2022-09-03 → 2026-06-05.
- **Train / validate split**: train 2022-09-03 → 2023-12-31 (14
  episodes); validate 2024-01-01 → 2026-06-05 (15 episodes). Same as
  H01-H04 / H02b / H02d / HA01-HA01b.

## 4. Measurement protocol

### 4.1 Per-day nightly RHR

For each calendar date with a UDS entry containing `restingHeartRate`
∈ [1, 200]: record as that day's nightly RHR. The UDS field is
Garmin's lowest stable HR during the prior sleep window (per Garmin
docs); validated against Wiggers' "bottom of the night-sleep-HR
graph" framing.

Days without a UDS entry, with `restingHeartRate == 0`, or with
clearly-invalid values outside [30, 130] (preserves room for
chronic-illness ranges; Wiggers cites baselines from 44 to 65 bpm
across her own data) are dropped.

### 4.2 Lagged personal baseline (per Theme A)

For each day `d`:

- Baseline window: days in `[d-90, d-30]` (60-day window ending 30
  days before `d`, excluding the recent candidate region).
- Baseline statistic: **trimmed mean** with 10/90 cut. (RHR is
  approximately normally distributed and not zero-heavy, so trimmed
  mean is more appropriate than percentile rank.)
- Minimum prior valid days: **40 of 60**. Below this, baseline is
  undefined for `d`.

### 4.3 Per-day delta

For each day `d` with both nightly RHR and a defined lagged baseline:

- `delta(d) = RHR(d) − baseline_lagged(d)` (signed; can be negative)
- `|delta(d)| = abs(delta(d))` (unsigned; primary metric)
- Sign label: `elevated` if delta ≥ N, `lowered` if delta ≤ −N,
  `neutral` otherwise.

### 4.4 Per-episode lead-up profile

For each crash episode dated `D`:

- **Primary lead-up window** = `[D − 4, D − 1]` (4 days).
- **Secondary lead-up window** = `[D − 5, D − 1]` (5 days).
- For each day in the lead-up with defined delta: record `delta(d)`,
  `|delta(d)|`, sign label.
- **Episode max |delta|** = max of `|delta(d)|` across valid lead-up
  days (per window).
- **Episode trigger flag (bidirectional, primary)** =
  `max |delta| ≥ N`.
- **Episode sign of trigger (when triggered)** = sign label of the
  triggering day (or signs of multiple triggering days if more than
  one).

### 4.5 Threshold N

Three pre-registered thresholds, evaluated independently:

| Tier | N | Source |
|---|---:|---|
| Primary | **5 bpm** | Wiggers' *"5-10 al ontevreden"* lower bound |
| Secondary | **10 bpm** | Workwell's "RHR + 10-15" lower bound |
| Sensitivity check | **15 bpm** | Workwell's upper bound; bar-tightening |

The **primary tier (5 bpm) determines the headline verdict**;
secondary and sensitivity check are reported alongside but do not
move the verdict label.

### 4.6 Null sample

200 randomly-selected reference dates from the analysis window, each
with a 4-day (primary) or 5-day (secondary) lead-up disjoint from
any crash episode's lead-up. For each null reference: compute
episode trigger flag exactly as in §4.4. Same null sample
construction as scripts 08/09/12 (HA01 / HA01b / HA02c) for direct
comparability. Seed `20260605` (matches H02 / H02b / H02d / HA01).

### 4.7 Sensitivity arm — one-sided "elevated only"

Run the entire pipeline a second time with the trigger flag changed
from `|delta| ≥ N` to `delta ≥ N` (one-sided, classical Workwell
direction). Report alongside the primary bidirectional verdict.

- If primary supports and one-sided refutes → parasympathetic-swing
  days are doing the work; report as "bidirectional SUPPORTED with
  swing-signal dependence."
- If both support → classical Workwell pattern dominates; report as
  "bidirectional SUPPORTED, swing-signal does not change verdict."
- If primary refutes → one-sided result is informational only.

### 4.8 Directionality split

For each SUPPORTED window, report:

- Fraction of triggering episodes where the triggering day is
  `elevated` (delta ≥ N).
- Fraction `lowered` (delta ≤ −N).
- Fraction with both directions present in the same lead-up window
  (rare; report if ≥ 5%).

## 5. Pre-registered falsification criterion

Identical three-criterion bar shape to H02b / HA01b / H02d.
Evaluated **independently** for the primary (4-day) and secondary
(5-day) windows. The **primary window determines the overall
verdict.**

Within each window, the hypothesis is **supported** if and only if
**all three** hold in **both** the train window and the validate
window independently:

**(a) Frequency**: at least **60%** of crash episodes have
`max |delta| ≥ N` in their lead-up window.

**(b) Discrimination**: the crash-episode frequency from (a) is at
least **15 percentage points higher** than the null-sample
frequency.

**(c) Magnitude**: the median `max |delta|` across crash episodes is
at least **N/2 bpm** (2.5 / 5 / 7.5 for N = 5 / 10 / 15
respectively).

Any one of (a), (b), (c) failing in either train or validate of the
primary tier (5 bpm) → **refuted**.

If we have fewer than 10 clean crash episodes per window after
exclusions → **inconclusive**.

The sensitivity arm (§4.7) and the secondary 5-day window are
reported with the same a/b/c numbers but do not move the verdict
label. They inform what we do next.

## 6. Exclusion rules

- **Episode requires ≥ 3 valid lead-up days out of 4** for the
  primary window (and ≥ 4 of 5 for the secondary).
- **Episode requires defined lagged baseline** on at least the same
  3 of 4 (or 4 of 5) days.
- **Days with `restingHeartRate` undefined or outside [30, 130] bpm**
  are excluded from both baseline and lead-up.
- **Episodes whose lead-up overlaps another crash episode's day(s)**
  are excluded from primary, reported separately.

## 7. Expected effect size if hypothesis is true

Rough sanity-checks for `result.md`:

- 60-80% of crash episodes have `max |delta| ≥ 5 bpm` in the 4-day
  lead-up (Wiggers' "5-10" floor predicts most heavy days cross
  this).
- Null sample rate: 25-45% (random 4-day windows have some
  probability of containing one elevated or lowered RHR day by
  natural variation).
- Median `max |delta|`: 5-10 bpm.
- If crash rate ≥ 95% and null rate ≥ 85% → metric is over-inflated
  by the bidirectional + multi-day combination; flag and consider
  whether |delta| ≥ N is too generous.
- Directionality split prediction: train-era likely mostly elevated
  (matches H02 train stress-spike pattern, classical Workwell);
  validate-era likely mixed or skewed toward lowered (consistent
  with H01's slight inversion + parasympathetic-swing story).

## 8. Caveats `result.md` must explicitly acknowledge

- **Chronotropic incompetence**: >85% of ME/CFS patients have a
  blunted HR response (Workwell's own caveat). If HA06 REFUTES, the
  honest reading is "the HR channel is blunted, not that overnight
  recharge is fine." HA07 (day-over-day HRV drop) is the natural
  follow-up using a different physiological signal.
- **Medication-shift confound (Wiggers)**: starting hartslag-
  verlagende medicatie shifts RHR baselines. The participant's
  current medication history through the analysis window has not
  been pre-checked for this protocol. If the analysis surfaces a
  step-shift in baseline RHR that aligns with a known medication
  change, the lagged baseline may be partly absorbing it; flag in
  `result.md`.
- **Watch-off coverage gap**: nights with the watch off do not
  contribute to RHR. Report night-coverage rate for each era.
- **`crash_v1` mixes mechanisms**. Same caveat as all prior
  precursor tests. Per-episode breakdown in `result.md`.
- **Multi-comparison.** HA06 is the 9th pre-registered hypothesis
  in the H##/HA## series (H01-H05, H02b, H02d, HA01-HA02b, HA01b-
  HA02c, HA06). The held-out validate window is the primary
  defence; we note this in `result.md`. The HA06 family (HA07-HA12)
  is queued separately and will be evaluated under its own
  pre-registrations.
- **Same-day overlap with H02d / HA01b**. If HA06 supports at 4d,
  cross-reference: for each SUPPORTED crash, was the triggering
  RHR-deviation day also a heavy-exertion day (HA01b's
  `exertion_class_lagged ∈ {heavy, very_heavy}`) or a high-stress-
  spike day (H02d bridge)? Convergence informs the
  single-mechanism-two-regimes reframe (D7).

## 9. What we do with each outcome

- **Supported in both windows** (primary 4d, both train + validate)
  → **first overall-SUPPORTED precursor of the project under clean
  methodology** (HA01b's original SUPPORTED status was withdrawn
  per Theme A; H02b and H02d are both train-only supported).
  Provides the empirical anchor for the D7 single-mechanism-two-
  regimes reframe. Compare against the directionality split: if
  validate-era is predominantly `lowered` (parasympathetic-swing
  pattern), this also explains H01's validate inversion as real
  signal, not noise. Then `card.md`: morning-RHR awareness card
  with two-direction framing.
- **Train supported, validate refuted** → same shape as H02b /
  H02d. Pre-cliff era had an RHR precursor; residual era does not.
  Combined with H02b/d, RHR is now a third stress-channel test
  consistent on the train/validate asymmetry.
- **Train refuted, validate supported** → unusual; would suggest
  the residual eventscape has an RHR pattern that the pre-cliff
  era lacked. Investigate the directionality split (likely
  parasympathetic-swing-driven). Pre-register HA06b on truly new
  data before claiming a stable validate-era precursor.
- **Refuted in both windows** → the RHR channel is closed for this
  participant. Combined with all prior refutations, this is the
  6th pre-registered test on the autonomic-channel family
  (broadly) to refute, and the direction shifts firmly to
  overnight recovery via H04b. HA07 (HRV channel) is the natural
  follow-up; if HA07 also refutes, the validate-era is
  precursor-invisible in every waking-hour-derivable signal we
  have access to.
- **Primary refutes but sensitivity arm differs** → report
  honestly; do not redefine the headline verdict on the sensitivity
  arm's result. Document for HA06b consideration on new data.
- **Inconclusive** → unlikely given H01's coverage rate, but if
  baseline-window-defined day counts fall below 10/window, debug
  and re-run.

---

*Pre-registration locked 2026-06-07. Next: implement `extract_rhr.py`
(field validation + inline; no separate extraction step needed,
reusing H01's pattern) and `test.py` (parallel evaluation at 4d
primary / 5d secondary, sensitivity arm running alongside primary,
3-episode dry-run printed before the full run).*
