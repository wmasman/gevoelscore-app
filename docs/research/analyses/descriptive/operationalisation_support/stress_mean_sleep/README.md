# `stress_mean_sleep` — operationalisation-support descriptive analysis

**Strand**: A (operationalisation support; template-driven; no operationalisation interview required per [`descriptive/README.md`](../../README.md) §7b).

## Research question

Operationalisation-support descriptive characterisation of `stress_mean_sleep` on Stratum 4, answering Q3.1.a–i per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) §3.1 (LOCKED 2026-06-18 r3, commit `ccbd12e`). First Phase-1 first-analysis under the locked programme; the channel is the most-cited CONFIRMED-citalopram-modulated channel (+0.43/mg p=0.001 buildup post-CPAP per v3 dose-response), load-bearing for HA07c / HA07d / HA08c and the project's strongest crash-vs-normal signal.

## Method

- **Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 → 2026-06-05; n=1339 sleep-valid days out of 1372 S4 days).
- **Phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) §3 (unmedicated / buildup / consolidation / afbouw).
- **Delegate**: Q3.1.a (distribution shape) delegates to [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) and **extends** with skewness / kurtosis / MAD / heavy-tail flag (material gap in the delegate target).
- **Delegate**: Q3.1.h (outliers + calibration-drift) cross-references [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md); no calibration events catalogued for this channel.
- **Computed directly from `per_day_master.csv`**: Q3.1.b (Politis-White E[L]\*), Q3.1.c (per-phase base rates), Q3.1.d (phase-stratified medians vs locked +0.43/mg dose-response), Q3.1.e (near-identity check |ρ|≥0.92), Q3.1.f (crash-vs-normal Cohen's d + stationary-bootstrap CI E[L]=7 + crash-drop sensitivity §3.4), Q3.1.g (spike-primitive availability), Q3.1.i (covariate-sensitivity readiness for future HA pre-regs).
- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) (`compute_data_driven_block_length`, `stationary_bootstrap_ci`).
- **No causal claims, no falsification bar** per [CONVENTIONS §2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

## Result

Headline (see [`findings.md`](findings.md) for the full answers Q3.1.a–i):

`stress_mean_sleep` on Stratum 4 is a **heavily right-skewed, autocorrelation-dense daily channel** (skew=+2.72, excess kurtosis=+15.5; **data-driven E[L]\*=12.6 — factor-of-2 above the project default**, flag fires per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)). The **citalopram-window phase medians are nearly flat** (range 17.04 → 20.20 across four phases; consolidation − unmedicated = −0.44, within MAD) — the locked +0.43/mg dose-response slope is a **within-buildup-window effect**, **not a between-phase steady-state level shift**. Crash-vs-normal separation is robust (episode-level Cohen's d=+0.91; bootstrap CI95 on mean diff [+1.58, +8.40] stress units; day-level CI is robust across E[L]=7 and E[L]=13 block-length choices, widths differ by only +5%). **One new near-identity pair surfaces**: `asleep_stress_avg_uds` (Pearson r=+0.929) — not in the existing cross-channel-correlation card's 7-channel panel.

## Files

- [`README.md`](README.md) — this file
- [`run.py`](run.py) — descriptive computation; outputs `summary.json` + `plots/*.png`
- [`findings.md`](findings.md) — writeup covering Q3.1.a–i + figures/tables
- [`summary.json`](summary.json) — machine-readable per-question results
- [`plots/`](plots/) — 5 PNGs: distribution, phase-stratified violins, trajectory-with-phases, crash-vs-normal, ACF

## Status

**Current as of 2026-06-18; revised same day per fresh-session `/research-review`** (verdict PASS with caveats; report at [`reviews/descriptive-stress_mean_sleep-2026-06-18.md`](../../../reviews/descriptive-stress_mean_sleep-2026-06-18.md); L3.4 substantive + four minor + three side-observation closures applied). Refresh when:
1. Stratum 4 right edge advances by ≥30 days AND any HA pre-reg on this channel is about to spin up.
2. A new citalopram-phase boundary lands (e.g. post-afbouw enters analytic scope).
3. The Politis-White E[L]\* shifts by another factor of 2 from current 12.6.
4. The `asleep_stress_avg_uds` near-identity pair gets propagated into the cross-channel-correlation card's 7-channel panel (would update Q3.1.e cross-reference).

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`)
- **HA-* tests that this analysis anchors**: HA07c (sleep-stress mean), HA07d (sleep-stress stdev), HA08c (sleep-stress slope). Any future HA pre-reg using `stress_mean_sleep` as predictor must cite this analysis for the descriptive substrate and adopt one of [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) §5.A / §5.B / §5.C treatments.
- **Existing artefacts referenced**: [`garmin_exploration/hrv_proxy_validation/`](../../../analyses/garmin_exploration/hrv_proxy_validation/) (Q3.1.f current-corpus refresh; aligns), [`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) (Q3.1.e; one new pair surfaced).
- **Methodology MDs**: `lc_phase_descriptive.md`, `citalopram_phase_stratification.md`, `citalopram_dose_response_stress_mean_sleep.md`, `permutation_null_block_length.md`, `garmin_indicators_audit.md`, `lc_era_temporal_segmentation.md`.
- **Upstream pipeline**: `per_day_master.csv` ← `pipeline/03_consolidate/build_unified_dataset.py` ← `processed/garmin/sleep_stress_nightly.csv` ← `garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`. `labels_crash_v2.csv` per locked `crash_v2-definition`.
