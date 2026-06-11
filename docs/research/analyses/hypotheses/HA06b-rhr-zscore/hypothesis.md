# HA06b — Z-score bidirectional RHR delta as crash precursor (relative-threshold variant of HA06)

**Pre-registration written 2026-06-07, before any z-scored RHR data
was inspected for this test.** Locked. Any subsequent change creates
an HA06c.

HA06b is **not** a re-cut of HA06. HA06 stays as-locked (already
run, REFUTED both eras, validate decisively at 0/15 triggering at
5 bpm). HA06b is a new pre-registration on the same data that
addresses a methodological gap surfaced by HA06's result:

**The absolute bpm thresholds in HA06 (5 / 10 / 15) were calibrated
to Wiggers' (lotgenoten lived-experience) and Workwell's (clinical
practice) populations, whose nightly RHR variability is materially
larger than this participant's.** HA06's median max-|delta| of 1.6
bpm in validate and 3.5 bpm in train indicates that the typical
day-to-day deviation from the lagged baseline is well below the
5 bpm threshold floor. The 10 and 15 bpm sensitivity checks were
vacuous (0% / 0% on both crash and null windows).

This is the same shape of methodological re-test as Theme A: an
independently-motivated correction to a mis-calibrated spec, with
the audit trail dated **before** the re-run. The locked
participant-feedback principle
[`relative_not_absolute`](../../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_relative_not_absolute.md)
explicitly endorses z-scores / personal-baseline deviations over
absolute thresholds; HA06 partially followed this principle
(the delta-from-baseline part was relative) but the threshold N
itself was absolute. HA06b fully follows the principle.

## 1. Claim

In the **4 days** before a `crash_v1` episode (primary) and the
**5 days** before a `crash_v1` episode (secondary), at least one
day's nightly resting heart rate deviates from its lagged personal
baseline by **|RHR − baseline_μ| / baseline_σ ≥ N_std** (N_std
locked below). The crash-episode frequency of this deviation is
discriminative against randomly-sampled non-crash windows in **both
train and validate windows independently**.

The bidirectional formulation (same as HA06) catches both classical
elevated-RHR and parasympathetic-swing (lowered) patterns. The only
substantive change from HA06 is the threshold: `N_std` (multiples of
the participant's own RHR variability) instead of `N` (absolute bpm).

## 2. Why we think this

- **HA06 result revealed the threshold mis-calibration.** Median
  max-|delta| in HA06 was 1.6-3.5 bpm; thresholds of 5/10/15 bpm
  were too coarse to register the participant's actual signal
  variability. HA06b's z-score normalization scales the threshold to
  this participant's own RHR distribution.
- **The locked
  [`relative_not_absolute`](../../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_relative_not_absolute.md)
  feedback memory** says explicitly: *"For PEM-pacing metrics in
  this project, always use z-scores or deviations from personal
  baseline, not absolute thresholds."* HA06 partially followed this;
  HA06b fully follows it.
- **HA06 train showed a directional positive signal** (+13.9 pp
  discrimination, 21.4% frequency, close to but not at the bar).
  Some genuine signal is present in the train era; the question is
  whether normalizing by personal variability lifts it across the
  bar. **The expected effect is modest** — even with z-score
  normalization, the validate side may still refute because validate
  median max-|delta| is so small (1.6 bpm) that even a tight
  baseline std (~1-2 bpm) yields z ~ 0.8-1.6, below the 1.5 primary
  threshold for most validate episodes.
- **RHR is approximately Gaussian within a person**, so z-score is
  the natural variability normalization. Percentile rank (HA06b-Option-B
  in QUEUED-WORK family) is methodologically equivalent for this data
  but less interpretable for HR.

## 3. Data sources

Identical to HA06:

- **Crash labels**: `crash_v1` from
  [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
- **Nightly RHR**: Garmin UDS `restingHeartRate`. Same field, same
  path, same dedup logic as H01 and HA06.
- **Analysis window + train/validate split**: same as HA06.

## 4. Measurement protocol

### 4.1 Per-day nightly RHR

Identical to HA06 §4.1. Values outside [30, 130] dropped.

### 4.2 Lagged personal baseline (per Theme A)

For each day `d`:

- Baseline window: days in `[d-90, d-30]` (60-day window, ending 30
  days before `d`). Identical to HA06.
- **Baseline mean (μ)**: trimmed mean with 10/90 cut (same as HA06).
- **Baseline std (σ)**: standard deviation of the **same trimmed
  prior-value list** used for the mean. Computed only when ≥ 40 of
  60 prior days are valid (same min as HA06). If σ ≤ 0.5 bpm — i.e.
  the baseline is essentially flat — flag the day as
  *low-variability* and skip it in the test (avoids division by
  near-zero noise; report fraction of such days).

### 4.3 Per-day z-scored delta

For each day `d` with both nightly RHR and a defined (μ, σ) pair:

- `delta(d) = RHR(d) − μ(d)` (signed; bpm)
- `z(d) = delta(d) / σ(d)` (signed; std-units)
- `|z(d)| = abs(z(d))` (unsigned; primary metric)
- Sign label: `elevated` if z ≥ N_std, `lowered` if z ≤ −N_std,
  `neutral` otherwise.

### 4.4 Per-episode lead-up profile

Same as HA06 §4.4 but using `|z|` and `signed z` instead of `|delta|`
and `signed delta`. Episode trigger flag (bidirectional, primary):
`max |z| ≥ N_std`.

### 4.5 Threshold N_std

Three pre-registered thresholds:

| Tier | N_std | Two-tail fraction (Gaussian) | Anchor |
|---|---:|---:|---|
| Primary | **1.5** | ~13.4% | mild-to-moderate deviation; matches "heavy" in severity_spec rank (top 15%) on a relative basis |
| Secondary | **2.0** | ~4.6% | classical "outlier" threshold; matches "very heavy" in severity_spec (top 5%) on a relative basis |
| Sensitivity check | **2.5** | ~1.2% | strict; only catches extreme deviations |

The **primary tier (N_std = 1.5) determines the headline verdict**;
secondary and sensitivity check are reported alongside.

### 4.6 Null sample

200 random non-overlapping reference dates, same construction +
seed (`20260605`) as HA06. Per-window null trigger flag computed
exactly as in §4.4.

### 4.7 Sensitivity arm — one-sided "elevated only"

Same as HA06 §4.7 but using signed z ≥ N_std (not |z|).

### 4.8 Directionality split

Same as HA06 §4.8 but on z-scored deltas.

## 5. Pre-registered falsification criterion

Identical three-criterion bar shape to HA06 / H02b / HA01b / H02d:

**(a) Frequency**: at least **60%** of crash episodes have
`max |z| ≥ N_std` in their lead-up window.

**(b) Discrimination**: the crash-episode frequency from (a) is at
least **15 percentage points higher** than the null-sample frequency.

**(c) Magnitude**: the median `max |z|` across crash episodes is at
least **N_std / 2** (0.75 / 1.0 / 1.25 for N_std = 1.5 / 2.0 / 2.5
respectively).

Any one of (a), (b), (c) failing in either train or validate of the
primary tier (N_std = 1.5) → **refuted**.

If we have fewer than 10 clean crash episodes per window after
exclusions → **inconclusive**.

## 6. Exclusion rules

Same as HA06 §6, with one addition:

- **Days where baseline σ ≤ 0.5 bpm** are flagged *low-variability*
  and excluded from the lead-up (to avoid z-score blow-up under
  near-flat baselines). Fraction reported in `result.md`.

## 7. Expected effect size if hypothesis is true

- 60-80% of crash episodes have `max |z| ≥ 1.5` in the 4-day lead-up.
- Null sample rate: 13-25% (Gaussian-tail expectation under no
  signal is ~13.4% per day; max over 4 days inflates this).
- Median `max |z|`: 1.5-2.5.
- Directionality split prediction: validate-era likely still
  skewed toward `lowered` (consistent with HA06's lowered-direction
  signal and Wiggers' parasympathetic-swing pattern); train-era
  mixed.
- If crash rate ≥ 95% and null rate ≥ 85% → metric is over-inflated
  by the bidirectional + multi-day combination; flag and consider
  whether N_std = 1.5 is too loose.

## 8. Caveats `result.md` must explicitly acknowledge

All of HA06 §8 carries over. One additional caveat:

- **Z-score discipline**: this is a methodologically-motivated
  re-test of the same data with a relative-threshold variant of the
  same hypothesis. It is NOT an independent test. Per the locked
  multi-comparison discipline, the held-out validate window is the
  primary defence; HA06b's result must be interpreted alongside
  HA06's. If HA06 refutes but HA06b supports, the supported claim
  is "RHR deviation scaled by personal variability is precursor-
  predictive" — not "RHR is precursor-predictive in general."

## 9. What we do with each outcome

- **Supported in both windows** (primary 4d, both train + validate)
  → **first overall-SUPPORTED precursor of the project under clean
  methodology after Theme A withdrew HA01b**. The relative-threshold
  framing matters; future autonomic-channel tests (HA07, HA08, HA10)
  should pre-register relative thresholds from the start. The D7
  single-mechanism-two-regimes reframe gains its empirical anchor
  through scaled-RHR rather than absolute RHR. Then `card.md`:
  variability-aware morning-RHR awareness card.
- **Train supported, validate refuted** → same pattern as H02b /
  H02d. Absolute thresholds were too coarse, relative thresholds
  reveal a train-era signal that did not survive the cliff. RHR
  channel is closed for residual era under either threshold scaling.
- **Train refuted, validate supported** → unusual; would suggest
  the residual eventscape has a personal-variability RHR pattern
  that the absolute test missed AND that the pre-cliff era lacked.
  Investigate carefully before claiming.
- **Refuted in both windows** → RHR channel is doubly closed (under
  both absolute and relative scaling). Even after participant-
  specific variability normalization, no signal. The case for HA07
  (HRV channel, less subject to chronotropic incompetence) becomes
  stronger; the case for H04b (per-minute BB decode → H03b overnight
  recharge) becomes the strongest remaining lead.
- **Primary refutes but sensitivity arm differs** → report honestly;
  do not redefine the headline verdict on the sensitivity arm's
  result. Document for HA06c consideration on new data.

---

*Pre-registration locked 2026-06-07. Same test-script pattern as HA06
with z-score computation added; same `--dry-run` mode; same null
seed.*
