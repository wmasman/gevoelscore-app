# `trajectory/era_boundaries/` -- README

**Strand B (multi-year trajectory) descriptive analysis** -- methodological backstop providing DESCRIPTIVE justification for the project's era/phase boundaries vs data-driven candidates. Closes Q4.3 per [`descriptive/README.md`](../../README.md) sec 4.3.

## Research question

Per descriptive README sec 4.3: 'pre-LC / Stratum 4 / phase boundaries are operational; what's the descriptive justification for those boundaries vs alternatives?'

**CRITICAL USER FRAMING** (per handoff sec 1): recovery-phase boundaries ARE the lived-experience reference per [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) sec 3.3-3.5. Data-driven candidates compared AGAINST recovery-phase boundaries; NO round-date alternatives needed.

## User-LOCKED operationalisation (per Strand B sec 7c interview 2026-06-25; do NOT iterate)

1. **12 boundaries**: 6 recovery-phase + 5 citalopram-phase + 1 historical 2023-12-31 train/validate split.
2. **Method = both**: per-boundary distribution-shift tests (KS + mean-shift + cumulative; +-30d window) + data-driven change-point detection (binary segmentation; documented choice; see Stage 3 docstring).
3. **7 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr + gevoelscore.
4. **Alternatives = data-driven only**, compared AGAINST recovery-phase boundaries as lived-experience reference (proximity tolerance +-21d = 3 * E[L]=7).

## Method (6-stage architecture per handoff sec 3.2)

- **Stage 1 (data prep)**: load per_day_master; restrict to 7 channels; identify recovery_phase + citalopram_phase + historical-split membership per row.
- **Stage 2 (per-boundary distribution-shift tests)**: for each of 12 boundaries x 7 channels = 84 cells, compute KS p-value (permutation null) + mean-shift + cumulative-shift over +-30d window each side; descriptive shift_detected flag at `(KS p < 0.05) OR (|Cohen's d| > 0.5)`.
- **Stage 3 (data-driven change-point detection)**: binary segmentation per channel on the 28d-rolling median (min-segment 60d; max-depth 12; reduction-threshold 5%). Method choice documented at the run.py docstring per handoff sec 6 acceptance criterion 7.
- **Stage 4 (proximity comparison)**: per data-driven candidate, find nearest recovery-phase boundary; flag CONFIRMED-by-data (within +-21d) vs NOVEL-data-driven.
- **Stage 5 (3 output artefacts)**: per-boundary descriptive justification table + data-driven candidate map + per-recovery-phase-boundary defensibility chart.
- **Stage 6 (programmatic emit)**: findings.md + README.md.

## Headline (descriptive only; NO causal claims; NO HA verdict promotion; NO boundary-change recommendation; user-owned decision per [[feedback_methodology_decisions_documented_reasoning]])

- Per-boundary distribution-shift: 6 of 12 boundaries show shift on >=4 of 7 channels (strong); 3 on 2-3 (moderate); 3 on <2 (weak/inconclusive).
- Data-driven candidates: 108 total; 18 CONFIRMED-by-data (within +-21d of recovery-phase boundary); 90 NOVEL-data-driven (not within +-21d; may reflect channel-specific dynamics).
- Recovery-phase boundary 7-channel sensitivity arm: 5 of 6 recovery-phase boundaries have >=1 channel discriminating (Stage 2 reproduces + extends the lc_recovery_phase_axis sec 7b 4a->4b single-channel-discrimination finding to the wider boundary set).

Full per-boundary x per-channel tables in [`findings.md`](findings.md); machine-readable data in `summary.json` (gitignored).

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- 6-stage analysis script; emits `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup of all 6 stages with cross-references + limitations (programmatic emit per the Write-tool harness heuristic on the literal filename 'findings')
- [`summary.json`](summary.json) -- machine-readable per-stage results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- coverage plots (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-04 corpus + 2026-06-25 analysis**. Closes Q4.3 (methodological backstop; previously had no home in any artefact per descriptive README sec 4.3). **Tier 3 Strand B 3rd of 5 LANDED** (Q4.9 LANDED `0290627`; Q4.6 LANDED `3e03b98`; Q4.3 this; remaining: Q4.5.b + Q4.4 + Q4.2 per user-chosen dependency order).

Refresh when:
1. A new recovery-phase or citalopram-phase boundary lands (e.g. post_afbouw boundary 2026-06-06 becomes in-corpus).
2. A new methodology MD revises any of the 12 CURRENT boundary dates (rerun against the updated dates).
3. Corpus right edge advances by >=90 days AND any HA pre-reg using a phase-stratified design is about to spin up (Stage 2 rolling 28d evidence shifts as new data accrues).

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`); sec 4.3 'Era-boundary descriptive justification' -- this analysis closes it.
- **lc_recovery_phase_axis sec 7b** (LOAD-BEARING; resting_hr 4a->4b finding REPRODUCED + EXTENDED): [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md).
- **Q4.9 subjective <-> objective coupling**: [`trajectory/subjective_objective_coupling/findings.md`](../subjective_objective_coupling/findings.md) -- per-channel pre-crash elevation pattern descriptively contextualises Stage 2 boundary-window reads on the same channels.
- **Q4.6 coverage_overview**: [`trajectory/coverage_overview/findings.md`](../coverage_overview/findings.md) -- some recovery-phase 1/2/3 boundaries in 2021-2022 have limited gevoelscore coverage; flagged honestly.
- **recovery_arc v2 sec 5.A** afbouw-reversal: [`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) -- the 3 CONFIRMED-citalopram channels' Stage 2 shifts at cp3 (consolidation -> afbouw) are descriptively consistent with the LOCKED afbouw-reversal direction (the recovery_arc v2 substantive verdict is NOT extended here).
- **Methodology MDs**: [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) + [`lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) + [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) + [`train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) + [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) + [`CONVENTIONS.md`](../../../../CONVENTIONS.md).
- **Upstream pipeline**: `per_day_master.csv` (7 channel columns + date + recovery_phase + citalopram_phase via dose_plasma_mg) <- `pipeline/03_consolidate/build_unified_dataset.py`.

## Discipline guards (per CONVENTIONS)

- **sec 2.1 descriptive-before-inference**: NO causal claims; NO falsification bar; NO HA verdict promotion. All LOCKED HA references descriptive corroboration only.
- **sec 3.1 personal baseline**: window distributions per channel +-30d each side of boundary.
- **sec 3.6 named counts**: every n in findings.md tables names scheme + unit.
- **sec 4.1 + sec 4.2 caveat-class**: descriptive framing only; observations reported as 'boundary X shows shift on Z of 7 channels'; NO promotion to 'boundary X is unjustified'.
- **sec 4.3**: data-driven change-point detection is exploratory; candidates descriptively surfaced + proximity to recovery-phase boundaries flagged; NO pre-commitment of any candidate as a 'better' boundary.
- **handoff sec 4 hard constraints**: NO HA artefact modifications; NO methodology MD modifications; NO per_day_master.csv modifications; NO iteration on the 4 user-locked operationalisation choices; NO boundary-change recommendation; user-owned decision per [[feedback_methodology_decisions_documented_reasoning]].
