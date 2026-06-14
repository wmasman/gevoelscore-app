# Activity-vs-PEM hypotheses — HA01, HA02, HA05

**Pre-registration locked 2026-06-06 before any crash-vs-activity
analysis runs.** Falsification criteria match H02b's bar shape
(strict three-criterion test, both train and validate must clear).

## Locked params (shared)
- **Crash labels**: `crash_v1` (= `crash_v2` tier-1), 29 episodes.
- **Dip labels** (for HA05): `crash_v2` tier-2, 79 isolated dips.
- **Lead-up window**: `[start - 3, start - 1]` (3 days before episode).
  Same as H02b.
- **Null sample**: 200 random 3-day windows disjoint from any crash
  lead-up, same seed `20260605` as H02b.
- **Train/validate split**: train 2022-09-03 → 2023-12-31
  (14 crashes); validate 2024-01-01 → 2026-06-05 (15 crashes).
  Both halves required for "supported" verdict.
- **Inclusive criteria for episodes**: ≥ 2 valid feature days in
  lead-up (matches H02b §6).

## HA01 — Single-day exertion shock precedes crashes

### Claim
In the 3 days before a crash, at least one day has
`exertion_class ∈ {heavy, very_heavy}` (a shock day) more often
than in non-crash 3-day windows. The acute-shock mechanism:
"you went hard one day → PEM crash followed."

### Metric
For each episode (or null window) `d`:
- `n_shock_days = |{x ∈ [d-3, d-1] : exertion_class(x) ∈ {heavy, very_heavy}}|`
- Range 0–3.
- `has_shock = (n_shock_days ≥ 1)` boolean.

### Falsification criteria (all three required, both windows)
- **(a) Frequency**: ≥ 60% of crash lead-ups have `has_shock = True`.
- **(b) Discrimination**: crash-window frequency from (a) is at
  least +15 pp higher than null-window frequency.
- **(c) Magnitude**: median `n_shock_days` across crashes ≥ 1,
  lower quartile ≥ 0.

Refuted if any of (a)(b)(c) fails in either train or validate.

### Why this is testable
~34% of all days in the corpus are heavy or very_heavy (per v3.1
distribution). Random 3-day windows therefore have ~70% chance of
containing at least one such day by chance. The discrimination
test asks: do crash lead-ups exceed that baseline by ≥15 pp?

## HA02 — Push burden precedes crashes

### Claim
In the 3 days before a crash, the **max** `push_burden_7d` over
the lead-up exceeds a pre-registered threshold more often than in
null windows. The push-crash mechanism: "you pushed sustained
over recent days → crash."

### Metric
For each episode (or null window) `d`:
- `max_push_7d = max(push_burden_7d) over [d-3, d-1]`
- `has_push = (max_push_7d ≥ 3)` boolean.

The threshold `3` corresponds to having pushed (rank ≥ 0.75) on
at least 3 days out of any 7-day window in the lead-up. This is
~p75 of the empirical push_burden_7d distribution (median is 2)
and was chosen blinded to crash labels.

### Falsification criteria (all three required, both windows)
- **(a) Frequency**: ≥ 60% of crash lead-ups have
  `has_push = True`.
- **(b) Discrimination**: crash-window frequency from (a) is at
  least +15 pp higher than null-window frequency.
- **(c) Magnitude**: median `max_push_7d` across crashes ≥ 3,
  lower quartile ≥ 2.

### Why push_burden_7d not push_burden_class
Per sensitivity_report.md, the binned `push_burden_class very_heavy`
was brittle (Jaccard 0.04-0.32 across reasonable parameter
variations). The raw count `push_burden_7d` (0-7) is stable
(Spearman rank correlation 0.95+ across baseline windows). HA02
tests the raw count.

## HA05 — Same precursors are weaker for dips than crashes

### Claim
Both HA01 and HA02 metrics show weaker discrimination on
`crash_v2` tier-2 `dip` events than on `crash_v1` (tier-1)
crashes. Tests whether exertion shock / sustained push is
specifically a crash trigger vs a generic bad-day trigger.

### Metric
Re-run HA01 and HA02 with dip dates as reference events instead
of crash starts. Same null sample, same criteria. Then compute:
- `discrimination_ratio = discrim_crash / discrim_dip`
  separately for HA01 and HA02 metrics.

### Falsification criteria
**Supported** if **both** of the following hold:
- (a) `discrimination_ratio ≥ 2` for HA01 in train window (crashes
  show ≥ 2× the activity-shock discrimination of dips).
- (b) `discrimination_ratio ≥ 2` for HA02 in train window.

Validate-window calculation reported descriptively but not
required for verdict (matching the H02b-on-dips precedent where
the validate convergence is itself the finding).

### Why ratio not absolute thresholds
HA05 is a comparative test. The relevant question is "is exertion
*more* of a crash thing than a dip thing?", not whether either
crosses absolute bars. Mirrors how H02b-on-dips was interpreted.

## Caveats acknowledged

- **HA01 has high base-rate**: 34% of days are heavy or
  very_heavy, so random 3-day windows commonly contain at least
  one. If crashes also have ~70% baseline, criterion (a)
  trivially passes but (b) is the harder test.
- **Crash labels mix mechanisms**: per crash_v2's findings, 4+10
  crashes show no spike precursor. Activity shock may be the
  trigger for some crashes but not others. A null verdict
  doesn't mean exertion never causes PEM; it means the metric
  doesn't capture the mechanism for this person at this
  resolution.
- **Multiple comparisons**: HA01 + HA02 + HA05 = 4 distinct tests
  (HA01-train, HA02-train, HA01-validate, HA02-validate;
  HA05 derived). Inflation manageable but report alongside.
- **Lead-up window choice**: 3 days matches H02b. PEM literature
  suggests 12-72h delay; 3 days fits within that.
- **Activity classification is itself blinded**: cutoffs in
  severity_spec.md v3.1 were locked from distribution alone, no
  crash labels considered. Spec v3.1 robustness verified.

## What we do with each outcome

- **HA01 + HA02 both supported in train + validate**: First
  exertion-precursor activity card concept supported. Build
  retrospective card for crashes with exertion-shock or push-
  burden context.
- **HA01 supported, HA02 not**: acute shock mechanism active but
  push-crash not visible at this resolution. Card concept
  retains shock-only framing.
- **HA02 supported, HA01 not**: push-crash mechanism active;
  flag sustained pushing pattern.
- **Both refuted in train**: activity at daily resolution does
  not predict crashes for this person. Useful negative result;
  may justify revisiting at finer (per-hour) resolution.
- **Train-supported, validate-refuted**: matches H02b's
  "kind of crash changed" multi-year pattern. Activity precursors
  evident in the train era, absent in the validate era. Card supports
  retrospective framing for pre-2024 crashes.
- **HA05 supported**: crashes-vs-dips distinct in activity
  precursor signature. Strengthens crash_v2 tier separation.
- **HA05 refuted**: activity precursors are bad-day-generic, not
  crash-specific. Mirrors H02b-on-dips dip-tier-is-heterogeneous
  finding.

---

## HA01b / HA02b / HA05b — Same tests, wider lead-up window

**Pre-registered 2026-06-06, after seeing HA01/HA02 refuted at
3-day window.** Motivated by participant's experiential evidence
(saved to project memory) that PEM lag is typically:
- Day T: trigger
- Day T+1: still ok ("immediate day after")
- Day T+2 to T+3: crash sets in (= `crash_start` in our data)
- Day T+4+: deepens

This puts the trigger 2-3 days before `crash_start` in the typical
case, occasionally further back. The 3-day window [D-3, D-2, D-1]
captures the typical case but misses longer lags.

**This is theory-driven, not post-hoc rescue**: the wider window is
motivated by the participant's reported lag pattern, not by
inspection of the failed HA01/HA02 result. (Same dynamic as H02
→ H02b coming from "intense moments" framing.)

### Locked changes
- **Lead-up window**: `[D-4, D-3, D-2, D-1]` (4 days). D-1 kept
  in window — if it truly doesn't contribute, the test will show
  that. We don't bake the participant's "D-1 is typically ok"
  assumption into the window definition.
- **All other params unchanged**: same null sample, same seed,
  same criteria bar (a) ≥60% / (b) ≥+15 pp / (c) magnitude.
- **Metric range**: HA01b shock count is now 0-4 (vs 0-3); HA02b
  max_push_7d still over a 4-day lead-up.
- **Criterion C — HA01b**: median n_shock_days ≥ 1 (unchanged),
  lower-q ≥ 0 (unchanged).
- **Criterion C — HA02b**: median max_push_7d ≥ 3 (unchanged),
  lower-q ≥ 2 (unchanged).

### Expected effect of wider window on base rates
With 34% of days as heavy+very_heavy, the null base rate for "any
shock day in N days" rises:
- 3 days: P(shock) ≈ 1 - 0.66³ ≈ 71% (HA01 found 68.5%)
- 4 days: P(shock) ≈ 1 - 0.66⁴ ≈ 81%

So criterion (a) gets easier (lower bar relative to base rate)
but criterion (b) gets harder (less room to clear +15 pp). The
real test is (b) discrimination.

### Verdict interpretation
- **HA01b/HA02b supported in train + validate**: lag is real and
  detectable at 4-day resolution. The crash precursor exists, we
  were just looking with the wrong window in HA01/HA02.
- **HA01b/HA02b refuted but with positive +pp direction**: signal
  is present but weak; lag may need finer-resolution analysis or
  cumulative-load framing.
- **HA01b/HA02b refuted with ~0 or negative discrimination**:
  consistent with HA01/HA02 finding — activity at any reasonable
  daily-aggregate lag does not predict residual crashes.

---

*Pre-registration locked 2026-06-06. Scripts: `08_run_ha_tests.py`
(3-day), `09_run_ha_tests_4day.py` (4-day).*
