# Specificity tables — methodology spec

**Locked 2026-06-07** per testing playbook §6.2 ("Card specificity /
posterior probability"). Required output before any card.md can be
drafted. Tier 2 peer-review action item from
[QUEUED-WORK.md §Card specificity](../../QUEUED-WORK.md).

## 1. Scope

For each load-bearing primary anchor (currently HA07d, HA10, H02b),
compute the **specificity table**: discrimination magnitude, recall,
precision, F1, and posterior probability per fire under the
appropriate per-era base rate.

Output: `card-b-train-specificity.md` (for the train-era retrospective
card) and `card-b2-validate-specificity.md` (for the validate-era
retrospective card). These docs **must be written before card.md
drafts** and are the gate per playbook §2.7 (card-craft rule).

## 2. Why this matters (the discipline)

The hypothesis-test 3-criterion bar (frequency ≥ 60%, discrimination
≥ +15 pp, magnitude ≥ floor) confirms the metric is **measurably
different in crash lead-ups vs random windows**. It does NOT confirm
that the metric is a good *predictive card*. A card that fires on
65% of all days while only marginally lifting posterior crash
probability over base rate would create false-alarm fatigue without
informative warning.

The card framing must use **posterior-probability language**, not
**discrimination-magnitude language**. STOCKTAKE §4 b2 first
surfaced this lesson; this doc operationalises it.

## 3. Definitions

A **card fires on day D** if the metric trigger occurred in the
trailing K-day window `[D-K, D-1]` where K is the lead-up window
of the underlying hypothesis (4 days for HA07d/HA10, 3 days for
H02b).

For each anchor × era:

- **Recall** = P(card fires | crash on day D) = `frac_event` from
  result-data.json (the hypothesis-test's crash trigger rate).

- **Null fire rate** = P(card fires | random day D) ≈ `frac_null`
  from result-data.json (the 200-window null sample). Approximates
  the population per-day fire rate under the simplifying assumption
  that random days are representative.

- **Base rate** = P(crash on day D | random day D) = `n_crashes /
  n_days_in_era_window`.

- **Precision** (= posterior per fire) = P(crash on day D | card
  fires on day D) computed by Bayes:
  ```
  Precision = (Recall × BaseRate) / (Recall × BaseRate +
              NullFire × (1 − BaseRate))
  ```

- **F1** = 2 × Precision × Recall / (Precision + Recall).

- **Lift** = Precision / BaseRate. How much the card multiplies the
  prior crash probability when it fires.

## 4. Era day counts (locked)

Per playbook §4.3 train/validate split:

| era | start | end | days | crash_v1 count | base rate |
|---|---|---|---:|---:|---:|
| **train** | 2022-09-03 | 2023-12-31 | **485** | **14** | **2.89%** |
| **validate** | 2024-01-01 | 2026-06-05 | **887** | **15** | **1.69%** |

## 5. Anchors to compute (locked 2026-06-07)

### 5.1 Card (b) train-era retrospective

Primary anchor: **H02b train** (3d primary, max contiguous stress
≥ 75 ≥ 5min duration ≥ 10 min delta).

Secondary (corroborating) anchors at the locked primary arm:
- **HA06b train** (4d N_std=1.5 bidirectional — but permanently
  demoted by v2 Cat 4 CLOSE; specificity reported for completeness
  but not used for card framing)
- **HA11 train** (4d N_std=1.5 one-sided elevated)
- **HA07c train** (4d N_std=1.5 one-sided elevated)
- **HA08c train** (4d N_std=1.5 one-sided elevated)
- **HA07d train** (4d N_std=1.5 bidirectional)
- **H02d train bridge × 5d** (bridge stress spike sentinel-corrected
  5d arm)

### 5.2 Card (b2) validate-era retrospective

Primary anchor: **HA07d validate** (4d N_std=1.5 bidirectional;
also the project's only overall-SUPPORTED + v2-validated finding).

Secondary (corroborating) anchor:
- **HA10 validate** (4d N_std=1.5 bidirectional; v2 RESCUE Cat 3).

## 6. Reporting requirements per locked spec (QUEUED-WORK Card
specificity)

For each anchor × era table row, report:

- **n_clean** (number of clean crash episodes evaluated)
- **frac_event** (recall)
- **frac_null** (null fire rate)
- **discrimination_pp** (the bar metric — already in result.md)
- **median_magnitude** (the c-criterion metric)
- **Precision** (posterior per fire)
- **Lift** (precision / base rate)
- **F1**
- **Implications for card text** (one-sentence interpretation)

Plus a sensitivity arm: precision computed at three base-rate
scenarios (`base × 0.5`, `base × 1`, `base × 2`) so the card framing
is honest about base-rate uncertainty.

## 7. Card-text implications template

Three calibration tiers based on lift × precision combination:

| Lift | Precision | Card-text implication |
|---|---|---|
| ≥ 5× and Precision ≥ 30% | "When this card fires, crash probability is meaningfully elevated; the metric is informative for next-N-day awareness" |
| 2-5× and Precision 5-30% | "When this card fires, crash probability is slightly elevated; reflective use only, no automated alerting" |
| < 2× or Precision < 5% | "Card fires too broadly to be informative as a forward signal; suitable only for retrospective annotation of confirmed crashes" |

The third tier is the playbook §6.6 no-go boundary: do not surface
as crash-risk %, traffic light, or push notification.

## 8. No-go list cross-reference (per playbook §6.6)

Even if a card passes the lift/precision bar, the following are
NOT permitted regardless:

- Crash risk percentages (e.g., "12% crash risk today")
- Traffic-light alerting on a single metric trigger
- Push notifications
- Recovery-score framing
- Automated rest-target derived from the metric
- Age-predicted HR zones
- Time-contingent escalation

The acceptable surface is reflective-only: timeline annotation
during after-the-fact review.

## 9. Output files

- `card-b-train-specificity.md` — table for card (b) anchors
- `card-b2-validate-specificity.md` — table for card (b2) anchors

Both written to `docs/research/garmin/cards/` (new folder).

## 10. Compliance with playbook §9 checklist

- [x] Locks methodology BEFORE computation
- [x] References playbook §6.2 + §6.6 + §2.7
- [x] Uses locked era day counts and base rates
- [x] Pre-commits which anchors and arms to report
- [x] Pre-commits reporting structure (precision/recall/F1/lift)
- [x] Pre-commits card-text implication tiers
- [x] No new hypothesis test; this is a derivative computation
  over locked result-data.json files. No null seed needed (no new
  null draws).

---

*Spec locked 2026-06-07. Computation script implements §3 formulas;
output cards reflect the locked tiers in §7.*
