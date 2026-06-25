# `trajectory/coverage_overview/` -- Strand B Q4.6 coverage map

## Status

**LANDED**: programmatic descriptive analysis answering Q4.6 per [`descriptive/README.md` sec 4.6](../../README.md). **LOAD-BEARING INFRASTRUCTURE foundation** for future HA pre-regs + remaining Tier 3 Strand B topics (Q4.3 + Q4.5.b + Q4.4 + Q4.2).

**Tier 3 Core 5, 2nd of 5 LANDED** (Q4.9 LANDED 0290627; this Q4.6 second; remaining: Q4.3 + Q4.5.b + Q4.4 + Q4.2 per user-chosen dependency order; Q4.7 + Q4.8 deferred per user 'narrower scope' triage).

---

## Research question

Per descriptive README sec 4.6: **When does which Garmin signal become available? What missingness patterns matter for hypothesis design?**

The gap this analysis closes (per README): 'coherent coverage-overview analysis that any HA pre-reg can cite for this column is available from date X with coverage Y%'.

---

## User-LOCKED operationalisation

Per Strand B sec 7c interview 2026-06-25 (do NOT iterate):

1. **Channel scope = all per_day_master columns** (201 enumerated; 200 present in master; 50 documented-or-flagged as drift). Skip per-minute / per-bout primitives (own methodology MDs).
2. **Coverage metric = both day-level + 28d rolling**: day-level for binary 'available?'; 28d rolling for 'stable coverage?' at >= 80% threshold.
3. **Date-range slicing = continuous + per-recovery-phase** (6 phases per [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md)).
4. **Missingness pattern = full**: descriptive (gap counts + lengths) + block-length distribution + MCAR/MAR diagnostic (Welch-style chi-square; method choice documented at Stage 5 of [`run.py`](run.py)).

---

## Method

**7-stage architecture** in [`run.py`](run.py):

- **Stage 1**: data prep (load `per_day_master.csv`; enumerate columns per DATA_DICTIONARY sec 0-14 + 7B + 8B-E taxonomy; identify recovery_phase per row).
- **Stage 2**: day-level coverage matrix (per-channel binary; first/last-available; total %; continuity flag).
- **Stage 3**: 28d rolling coverage (% non-NaN; stable-epoch flag at >=80%; inflection dates; longest-run summary).
- **Stage 4**: per-recovery-phase summary (channel x 6 phases x % coverage).
- **Stage 5**: missingness pattern (per channel: gap counts + gap-length distribution + block-length bin counts + Welch-style chi-square MCAR/MAR diagnostic + MNAR-suspect heuristic flag).
- **Stage 6**: 3 output artefacts (coverage timeline chart + per-recovery-phase summary table + missingness diagnostic report).
- **Stage 7**: programmatic emit `findings.md` + `README.md`.

**Discipline guards** (CONVENTIONS):

- sec 2.1: descriptive-before-inference; NO causal claims; NO HA verdict promotion.
- sec 3.3: NO pre-commitment of MCAR/MAR readings for HAs not yet pre-spec'd; the diagnostic is descriptive infrastructure ONLY.
- sec 3.6: named counts (every cell carries scheme + unit + source-file).
- sec 4.1 + 4.2: no interpretive marks; pipeline-vs-doc drift honestly surfaced per [[feedback_flag_contradictions]] (Q3.8 push_burden_7d extension).

---

## Result

Headline (see [`findings.md`](findings.md) for full Q4.6 answers):

**201 columns enumerated**; 200 present in `per_day_master.csv`; 50 surface either pipeline-vs-doc drift or MNAR-suspect heuristic flag.

Coverage span: **earliest 2021-08-16** (Garmin extract); **latest 2026-06-04** (as_of_date). gevoelscore starts 2022-09-03; bb_overnight_gain truth starts 2024-09-18 (proxy bridges back to 2024-07-08 per [`bb_overnight_gain_proxy.md`](../../../../methodology/bb_overnight_gain_proxy.md)).

**3 output artefacts** emitted per descriptive README sec 4.6 expectations:

1. Coverage timeline chart: [`plots/coverage_timeline.png`](plots/coverage_timeline.png) (gitignored).
2. Per-recovery-phase summary heatmap: [`plots/per_phase_coverage_heatmap.png`](plots/per_phase_coverage_heatmap.png) (gitignored).
3. Missingness diagnostic report: [`plots/missingness_diagnostic.png`](plots/missingness_diagnostic.png) (gitignored).

Per-recovery-phase coverage summary table + first/last-available headlines + MCAR/MAR verdict counts + MNAR-suspect listing + pipeline-vs-doc drift listing all live in [`findings.md`](findings.md).

---

## Cross-references (descriptive only -- NO HA verdict promotion)

- [`DATA_DICTIONARY.md`](../../../../DATA_DICTIONARY.md) -- column-level documentation; family enumeration source.
- [`methodology/bb_overnight_gain_proxy.md`](../../../../methodology/bb_overnight_gain_proxy.md) (LOAD-BEARING) -- BB truth/proxy/best/source 4-channel audit trail + 2024-07-08 / 2024-09-18 UDS rollout dates.
- [`methodology/stress_low_motion_primitive.md`](../../../../methodology/stress_low_motion_primitive.md) -- Session E lock for the 11-column stress_low_motion family.
- [`methodology/garmin_indicators_audit.md`](../../../../methodology/garmin_indicators_audit.md) -- known-issues catalog cross-referenced per channel.
- [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) -- 6-phase axis definitions for per-phase summary table.
- [`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary 2022-09-03 for outcome-side coverage.
- [`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) -- v2 phase-coverage precedent (bb_overnight_gain 5/6 empty + gevoelscore 1+2 empty inherit here).
- [`operationalisation_support/push_burden_7d/findings.md`](../../operationalisation_support/push_burden_7d/findings.md) -- Q3.8 CONVENTIONS sec 3.2 / audit MD drift precedent extended across all columns in this analysis.
- [`operationalisation_support/bb_overnight_gain/findings.md`](../../operationalisation_support/bb_overnight_gain/findings.md) -- Q3.5 truth-only window analytic discipline precedent.
- [`CONVENTIONS.md`](../../../../CONVENTIONS.md) sec 2.1, 3.2, 3.3, 4.1-4.4 -- discipline anchors.

---

## Files

- [`README.md`](README.md) -- this file (programmatically emitted).
- [`findings.md`](findings.md) -- Q4.6 answers (programmatically emitted).
- [`run.py`](run.py) -- the 7-stage descriptive computation script.
- `summary.json` -- machine-readable per-channel per-phase stats (gitignored).
- `plots/*.png` -- 3 artefacts (gitignored).

---

*Programmatic README emit by [`run.py`](run.py) per the Q3.5 / Q3.6 / Q3.7 / Q3.8 precedent (Write-tool harness heuristic on the literal filename `findings` / `README`). To refresh: ``python run.py``.*
