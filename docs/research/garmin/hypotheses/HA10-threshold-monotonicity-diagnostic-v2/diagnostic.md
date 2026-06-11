# HA10 threshold-monotonicity diagnostic v2

**Pre-registration locked 2026-06-07** per the user-locked Option C
tightened, following the v1 CLOSE verdict on HA10 validate
bidirectional and the discovery that the v1 criteria themselves
had a methodological defect.

**Criteria source**: [v2 methodology document](../../methodology/threshold-sweep-rescue-criteria-v2.md).
This diagnostic does NOT lock its own criteria; it references the
v2 methodology document directly. Any criteria revision must
happen in the v2 methodology document, not here.

## 1. What this diagnostic re-evaluates

**Test under diagnostic**: HA10 (morning Body Battery peak z-score,
locked validate-era SUPPORTED at +16.2 pp, 4d primary
bidirectional, N_std=1.5).

**Previous v1 outcome**: CLOSE per the v1 criteria (peak at
N_std=1.75 outside rescue window [1.0, 1.5]; other shape criteria
mostly passed). Synthesis-level framing demoted HA10 to
non-load-bearing. Card (b2) anchor reference dropped.

**v2 question**: Under the v2 five-category shape rule, does HA10
validate-era bidirectional primary fall into a PASS category
(canonical decline / stable plateau / rising-late-peak) or a FAIL
category (bumpy / loose-tail noise)?

## 2. Data sources and machinery

Identical to HA10 v1 diagnostic. Same fine N_std grid [0.5, 0.75,
1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0]. Same
input data: morning HIGHEST BB anchor 03:00-10:00 local from UDS,
1670 valid days. Same null sample seed `20260605`. Same lagged
baseline machinery, same 4d primary lead-up window.

No data inspection occurs between the v1 diagnostic and v2 — the
fine-grid values are already in v1's result-data.json. The v2
diagnostic reads those numbers and applies the v2 criteria
without re-running the test.

## 3. v2 verdict logic (per methodology document)

Apply the five-category rule from [v2 methodology §3](../../methodology/threshold-sweep-rescue-criteria-v2.md#3-the-five-category-shape-rule)
to HA10's validate-era bidirectional discrimination curve.

The verdict is RESCUE if any of categories 1, 2, 3 match. CLOSE if
any of categories 4, 5 match and no PASS category matches. CLOSE
also if multiple categories match across the PASS/FAIL boundary.

## 4. Test-specific notes

- HA10 was tested in **validate era only** for SUPPORTED status
  at v1 primary; train era refuted at v1 primary. The v2
  diagnostic applies to validate. Train discrimination curve is
  reported descriptively only.
- HA10's locked verdict remains on record per pre-registration
  discipline regardless of v2 outcome.
- HA10 v2 outcome determines whether HA10 is restored to a
  corroborating-but-fragile secondary anchor for card (b2) or
  remains permanently demoted.

## 5. Pre-registered restoration / demotion actions

### If RESCUE under v2

- Synthesis-level framing restores HA10 to **corroborating
  secondary anchor for the validate-era picture** (not primary,
  because HA10's one-sided arm robustness is what passes — see
  v1 result.md).
- Card (b2) framing may reference HA10's elevated direction as
  descriptive context.
- The "non-load-bearing" framing in STOCKTAKE / synthesis /
  addendum / Wiggers progress reverts to "load-bearing under v2
  criteria (peak-location was a v1 criteria defect)."
- v2 RESCUE only restores load-bearing status if specificity
  tables are also completed for the underlying test.

### If CLOSE under v2

- v1 demotion becomes permanent.
- Synthesis-level framing keeps HA10 as non-load-bearing.
- The methodology lesson: v2 captured what v1 missed correctly;
  HA10 genuinely is fragile across robust-signal shape categories.

### If AMBIGUOUS under v2

- HA10 stays demoted per the v2 default rule. Flagged for
  case-by-case methodological review.

## 6. Outputs

- `result-data.json` — shape category match per era, RESCUE /
  CLOSE / AMBIGUOUS verdict, comparison to v1 verdict.
- `result.md` — verdict statement, synthesis-framing
  implications, locked verdict status confirmation.

The result.md will be produced after ALL FOUR v2 diagnostics run
(per the v2 methodology §5 atomic synthesis-update protocol).

## 7. Companion diagnostics

This diagnostic is one of four locked v2 diagnostics. All four
must run before synthesis is updated:

- HA10-threshold-monotonicity-diagnostic-v2 (this document).
- HA07d-threshold-monotonicity-diagnostic-v2.
- HA06b-threshold-monotonicity-diagnostic-v2.
- HA11-threshold-monotonicity-diagnostic-v2.

---

*Locked 2026-06-07. Criteria source is the v2 methodology
document; this diagnostic references that document and does not
lock its own criteria. Atomic synthesis update enforced.*
