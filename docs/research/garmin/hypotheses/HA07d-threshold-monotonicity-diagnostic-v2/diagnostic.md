# HA07d threshold-monotonicity diagnostic v2

**Pre-registration locked 2026-06-07** per the user-locked Option C
tightened, following the v1 CLOSE both-eras verdict on HA07d
bidirectional primary that revealed the v1 criteria themselves
had a methodological defect.

**Criteria source**: [v2 methodology document](../../methodology/threshold-sweep-rescue-criteria-v2.md).
This diagnostic does NOT lock its own criteria; it references the
v2 methodology document directly.

## 1. What this diagnostic re-evaluates

**Test under diagnostic**: HA07d (night-over-night delta of sleep
stress STDEV z-score; locked OVERALL-SUPPORTED at primary 4d
bidirectional N_std=1.5 — train +19.6 pp, validate +21.7 pp).

**Previous v1 outcome**: CLOSE both eras per the v1 criteria
(peak at N_std=1.75 outside rescue window in both; train Spearman
near-zero with 4 sign changes — genuinely bumpy curve consistent
with train autonomic-volatility hypothesis but failing v1
monotonicity test; validate Spearman positive — rising-with-
threshold shape that v1 criteria penalise even though
qualitatively maximally robust with discrimination sustained at
+19 to +31 pp across N_std=1.0 through 4.0).

Synthesis-level framing demoted HA07d to non-load-bearing in both
eras. The project effectively returned to "no load-bearing
overall-SUPPORTED test." Card (b2) lost its sole anchor.

**v2 question**: Under the v2 five-category shape rule, do
HA07d's bidirectional primary curves fall into PASS categories
(canonical decline / stable plateau / rising-late-peak) or FAIL
categories (bumpy / loose-tail noise) — assessed independently
per era?

## 2. Data sources and machinery

Identical to HA07d v1 diagnostic. Same fine N_std grid [0.5 →
4.0, 13 tiers]. Same input data: sleep_stress_nightly.csv (1707
valid nights). Same null sample seed `20260605`. Same lagged
baseline machinery, same 4d primary lead-up window.

The v1 result-data.json contains the fine-grid values for both
eras. The v2 diagnostic reads those values and applies the v2
criteria without re-running the test.

## 3. v2 verdict logic

Apply [v2 methodology §3](../../methodology/threshold-sweep-rescue-criteria-v2.md#3-the-five-category-shape-rule)
per era independently. Each era gets its own RESCUE / CLOSE /
AMBIGUOUS verdict.

## 4. Test-specific notes

- HA07d was tested in BOTH eras at v1 primary (validate
  SUPPORTED, train SUPPORTED); v2 evaluates both.
- HA07d's locked verdicts remain on record regardless of v2
  outcomes.
- **Empirical expectation per the v2 criteria logic**:
  - Validate bidirectional: discrimination sustained +19 to +31
    pp across wide threshold range; positive Spearman because
    signal-to-noise rises at strict thresholds. Likely matches
    **Category 2 — Stable plateau** OR **Category 3 — Rising /
    late-peak**. Likely RESCUE.
  - Train bidirectional: 4 sign changes; discrimination drops
    below zero at N_std=3.5 (−0.9 pp). Matches **Category 4 —
    Bumpy with sign changes**. Likely CLOSE.
- These expectations are pre-registered for honest tracking, NOT
  to bind the v2 verdict — the v2 criteria are applied as
  written; the empirical reality determines outcome.

## 5. Pre-registered restoration / demotion actions

### If validate RESCUE under v2

- HA07d validate restored to **sole load-bearing validate-era
  anchor** for card (b2).
- Synthesis-level "no load-bearing validate-era precursor" framing
  reverts; era-as-moderator narrative restores with HA07d as the
  single-channel anchor for the era reversal.
- Card (b2) ship pathway unblocks, conditional on separately-
  completed specificity tables.
- If HA10 also v2-RESCUES, HA10 becomes corroborating-fragile
  secondary; if not, HA07d carries validate alone.

### If validate CLOSE under v2

- Validate demotion becomes permanent.
- Project narrative permanently absorbs "no load-bearing
  validate-era precursor under canonical methodology."
- Card (b2) cannot ship as anchored.

### If train RESCUE under v2

- HA07d train restored to load-bearing train-era anchor on
  the sleep-stress channel.
- HA07c / HA08c / HA07d together restore the three-primitive-
  same-channel finding.

### If train CLOSE under v2

- Train demotion permanent.
- Six train-channel narrative reads as "five channels + sleep-
  stress channel with mean-and-slope SUPPORTED (HA07c, HA08c)
  but variability primitive (HA07d) demoted under v2."
- Train autonomic-volatility hypothesis still observable in
  HA07d's V1 result data even if formally CLOSE under v2.

### Era-asymmetric outcomes

If train CLOSE but validate RESCUE: HA07d validate becomes sole
validate-era load-bearing anchor; train HA07d non-load-bearing.
The era reversal narrative shifts to "validate has anchor;
train's volatility shape is documented in v1 result data but not
load-bearing on this channel."

## 6. Outputs

- `result-data.json` — shape category match per era, RESCUE /
  CLOSE / AMBIGUOUS per era, comparison to v1 verdicts.
- `result.md` — verdict statement per era, synthesis-framing
  implications.

Result.md produced after ALL FOUR v2 diagnostics run.

---

*Locked 2026-06-07. The user-locked Option C requires both eras
evaluated under v2; HA07d cannot have a partial v2 verdict
(e.g. only validate evaluated). Both era verdicts are part of
the v2 diagnostic output.*
