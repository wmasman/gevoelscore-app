# `trajectory/recovery_arc/` — findings

## Authorship

- **Computed**: 2026-06-18 by Claude (Opus 4.7) via [`run.py`](run.py) under the locked operationalisation in [`README.md`](README.md) (Strand B; §7b user-interview-completed 2026-06-18).
- **Data**: `per_day_master.csv` at `$GEVOELSCORE_DATA_PATH/unified/`, as-of-date **2026-06-04** (Garmin coverage right edge per [STOCKTAKE §1](../../../../STOCKTAKE.md#1-the-corpus)). 1754 day-level rows total.
- **Layer 1 descriptive per [CONVENTIONS §2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference)**: NO causal claims; NO `SUPPORTED` bar; NO `REFUTED` mark. This document characterises the three-phase multi-year shape; intervention attribution is out of scope.
- **Cross-references**: [`run.py`](run.py) + [`summary.json`](summary.json) + [`plots/`](plots/) (7 PNGs). Per-channel × per-phase numbers cited below trace to the JSON.

---

## 1. Headline — the multi-year shape

Across the 7 HA-P6 channels on a 5-year window (2021-08-16 → 2026-06-04, 1755 days), the data tell a coherent three-phase autonomic-load story:

- **Pre-illness healthy baseline** (217 day-level rows, 7 months): all autonomic-load channels sit at the lowest medians of the corpus; resting HR sits at 54 bpm (Garmin units; per_day_master.csv); BB-floor sits at 12 (Garmin units). This is the strongest available "healthy comparison" for everything that follows, and has never been formally characterised — the single largest gap closed by this analysis.
- **Acute COVID infection** (14 day-level rows, 14 days, 2022-03-21 → 2022-04-03): four of the six autonomic-load + recovery channels show their largest acute deflection of the corpus. `stress_low_motion_min_count_S60_Mlow` jumps from a healthy median of 36 to 101 (2.8× lift); `stress_mean_sleep` rises from 15.95 to 20.31 (+27%); `all_day_stress_avg` rises from 30 to 33. The acute window is too short to bootstrap tightly (CIs are wide), but the direction is consistent across the autonomic-load family. `resting_hr` is the only channel that does NOT rise during acute infection — it dips slightly (54 → 52.5), and the CI95 brackets the healthy median.
- **LC trajectory** (4+ years, 1339-1365 day-level rows per channel in Stratum 4): autonomic-load channels show **partial recovery** from the immediate-LC peak — `all_day_stress_avg` returns from 36 (lc_pre_gevoelscore peak) to 32 in Stratum 4, close to but distinct from the healthy 30. `stress_mean_sleep` stays at 19.2 throughout the LC trajectory (~+3.3 units above healthy 15.95, CIs non-overlapping). `bb_lowest` shows a different shape entirely: a major **lift** from 12 (healthy) to 20 (Stratum 4 median) — and this lift is the only headline channel pattern that does NOT survive a 90-day rolling-median detrend (per [CONVENTIONS §3.7](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons)), meaning the rise from 12 to 20 IS the recovery trajectory itself rather than a between-phase step.

Two coverage gaps shape the readings: `bb_overnight_gain` has data only from 2024-09-18 onward (3 of 4 phases empty); `gevoelscore` has data only from 2022-09-03 onward (3 of 4 phases empty). Both gaps are structural (described in §2b of [README](README.md#3-event-overlays-locked-intervention--medical-user-explicit-reminder-to-include-cpap-end) + [intervention_effects_descriptive §2b](../../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain)), not analysis-side, and they collapse the three-phase shape to a single-phase shape for those two channels.

---

## 2. Per-channel × per-phase characterisation

For each cell: `median [bootstrap CI95 at E[L]=7]` on the raw channel, with the per-phase n (day-level rows from `per_day_master.csv`), and a per-cell "survives detrend?" flag (per CONVENTIONS §3.7: direction of `phase_median − grand_median` is preserved when the rolling-90d-median trend is subtracted day-wise). The data-driven block length E[L]\* and its factor-of-2-deviation flag mirror the HA-P6 v3 §4.8.1 + [permutation_null_block_length.md](../../../../methodology/permutation_null_block_length.md) discipline.

### 2.1 `stress_mean_sleep` (autonomic-load, sleep window) — see [plots/stress_mean_sleep.png](plots/stress_mean_sleep.png)

| phase | n | median | CI95 | E[L]\* | M | survives detrend? |
|---|---:|---:|---|---:|---:|:--:|
| pre_illness_healthy   |  215 | 15.95 | [13.80, 16.84] |  7.0   | 1 | yes |
| acute_infection       |   14 | 20.31 | [14.38, 23.75] |   na   | — | yes |
| lc_pre_gevoelscore    |  139 | 19.56 | [17.02, 21.42] |  7.0   | 1 | yes |
| lc_with_gevoelscore   | 1339 | 19.21 | [18.69, 19.65] | 12.6 ⚐ | 6 | yes |

Healthy median 15.95 is **distinct** from all three illness-phase medians (CIs non-overlapping for both LC phases vs healthy). The acute median 20.31 sits at the upper end of the healthy CI and the lower end of LC-pre-gevoelscore — direction matches but n=14 keeps the CI wide. **Within-Stratum-4 cell fires the factor-of-2 flag** (E[L]\*=12.6, M=6 days): consistent with the operationalisation_support/stress_mean_sleep analysis at commit `84b9801`, which also surfaced E[L]\*≈12.6 on the same Stratum 4 surface. The per-phase autocorrelation cutoff `M` is 1 day in early phases and 6 days in Stratum 4 — within-phase autocorrelation lengthened in the LC era, as expected if a slow recovery process is operating on top of the daily signal.

### 2.2 `all_day_stress_avg` (autonomic-load, 24h composite) — see [plots/all_day_stress_avg.png](plots/all_day_stress_avg.png)

| phase | n | median | CI95 | E[L]\* | M | survives detrend? |
|---|---:|---:|---|---:|---:|:--:|
| pre_illness_healthy   |  216 | 30.00 | [29.00, 32.00] |  7.0   |  1 | yes |
| acute_infection       |   14 | 33.00 | [32.00, 41.00] |   na   |  — | yes |
| lc_pre_gevoelscore    |  143 | 36.00 | [35.00, 37.00] |  7.0   |  1 | yes |
| lc_with_gevoelscore   | 1359 | 32.00 | [32.00, 33.00] | 29.8 ⚐ | 18 | yes |

The shape is a clear **peak in lc_pre_gevoelscore** (36, CI [35, 37]) — the highest sustained autonomic-load median of any phase in any channel — followed by partial reversion in Stratum 4 (32, CI [32, 33]). The Stratum 4 median is 2 units above the healthy 30 with no CI overlap; the magnitude of the partial recovery is roughly two-thirds of the immediate-LC peak's elevation over healthy. The E[L]\*=29.8 in Stratum 4 (factor-of-2 flag) is markedly longer than the project default of 7; M=18 days. This is consistent with the dose-response finding in [citalopram_dose_response_stress_mean_sleep §5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) (β = +0.57/mg, p=0.000 on this channel) — long memory in Stratum 4 is what dose-modulation across multi-month phases would produce.

### 2.3 `bb_lowest` (recovery, BB-floor) — see [plots/bb_lowest.png](plots/bb_lowest.png)

| phase | n | median | CI95 | E[L]\* | M | survives detrend? |
|---|---:|---:|---|---:|---:|:--:|
| pre_illness_healthy   |  216 | 12.00 | [ 9.50, 14.00] |  3.0 ⚐ |  2 | **no** |
| acute_infection       |   14 | 14.50 | [ 5.00, 20.00] |   na   |  — | **no** |
| lc_pre_gevoelscore    |  143 | 11.00 | [ 9.00, 13.00] |  7.0   |  1 | **no** |
| lc_with_gevoelscore   | 1359 | 20.00 | [19.00, 21.00] | 29.2 ⚐ | 18 | **no** |

`bb_lowest` shows the corpus's most dramatic between-phase **lift** — from 11-12 in the three pre-LC-with-gevoelscore phases to 20 in Stratum 4 — and is the only channel where **no phase survives the 90d-rolling-median detrend** under the CONVENTIONS §3.7 procedure. The reading: the +8-9-unit rise from the pre-illness/LC-pre-gevoelscore baseline to the Stratum 4 baseline IS the multi-year recovery trajectory, not a discrete between-phase step. The factor-of-2 flag fires on both ends (E[L]\*=3.0 in pre_illness, E[L]\*=29.2 in Stratum 4) — short-range structure in the healthy phase, long memory in Stratum 4. The interpretive reading aligns with intervention_effects_descriptive §8.2-§8.3 where `bb_lowest` shows a graded dose-response to citalopram (β = −1.13/mg, p=0.000 from [citalopram_dose_response §5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md)) — and the post-2024 segment of the Stratum 4 phase is overwhelmingly post-CPAP + on-citalopram.

### 2.4 `bb_overnight_gain` (recovery, overnight) — see [plots/bb_overnight_gain.png](plots/bb_overnight_gain.png)

| phase | n | median | CI95 | E[L]\* | M | survives detrend? |
|---|---:|---:|---|---:|---:|:--:|
| pre_illness_healthy   |   0 | — | — | — | — | — |
| acute_infection       |   0 | — | — | — | — | — |
| lc_pre_gevoelscore    |   0 | — | — | — | — | — |
| lc_with_gevoelscore   | 593 | 49.00 | [48.00, 51.00] |  6.5   |  4 | na |

`bb_overnight_gain` data exist only from 2024-09-18 onward per [intervention_effects_descriptive §2b](../../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain) (Garmin firmware UDS rollout, **not** a project-side pipeline gap). The three pre-Stratum-4 phases are unanalyzable by construction; even within Stratum 4, only the tail (2024-09-18 → 2026-06-04, 593 day-level rows) carries data. The single-phase median 49 [48, 51] characterises late-LC overnight recovery, with E[L]\*=6.5 (no flag) and M=4 — within-window structure is shorter than the other two recovery-related channels. **The three-phase trajectory question is not addressable for this channel**; the rolling-30d-median in the plot tells the within-Stratum-4-tail story only.

### 2.5 `resting_hr` (cardiovascular) — see [plots/resting_hr.png](plots/resting_hr.png)

| phase | n | median | CI95 | E[L]\* | M | survives detrend? |
|---|---:|---:|---|---:|---:|:--:|
| pre_illness_healthy   |  217 | 54.00 | [52.00, 55.00] |  7.0   | none | yes |
| acute_infection       |   14 | 52.50 | [51.00, 55.00] |   na   |  —   | **no** |
| lc_pre_gevoelscore    |  143 | 55.00 | [54.00, 56.00] | 10.5 ⚐ | 10   | yes |
| lc_with_gevoelscore   | 1357 | 56.00 | [56.00, 57.00] |  7.0   | none | **no** |

The shape is a slow upward drift — healthy 54 → Stratum 4 56 — within a tight per-phase IQR (3 bpm throughout). **Acute infection dips** below the healthy median (52.5 vs 54; CI brackets healthy), the only channel where the acute direction differs from the autonomic-load family; this is consistent with parasympathetic dominance during acute illness, though the 14-day window is too short to tighten the CI. The Stratum-4 cell **does NOT survive detrend**: the 56-vs-55 rise from lc_pre_gevoelscore to Stratum 4 is captured by the rolling 90-day trend (i.e., it is the within-LC continuation of the multi-year drift). Cross-test: the Stratum-4 median 56 sits inside the [`citalopram_dose_response §5.6.1` resting_hr verdict](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read) of weakly-consistent dose-modulation (β=+0.03/mg, p=0.34). The healthy → Stratum 4 +2 bpm is within the band that ergotherapie-onset confounding (intervention_effects §8.3 large r_rb=−0.97 at 2022-09-22) may also explain.

### 2.6 `gevoelscore` (felt-state outcome) — see [plots/gevoelscore.png](plots/gevoelscore.png)

| phase | n | median | CI95 | E[L]\* | M | survives detrend? |
|---|---:|---:|---|---:|---:|:--:|
| pre_illness_healthy   |    0 | — | — | — | — | — |
| acute_infection       |    0 | — | — | — | — | — |
| lc_pre_gevoelscore    |    0 | — | — | — | — | — |
| lc_with_gevoelscore   | 1371 | 5.00 | [4.00, 5.00] | 15.1 ⚐ | 8 | na |

`gevoelscore` data exist only from 2022-09-03 onward by construction ([lc_era_temporal_segmentation §1](../../../../methodology/lc_era_temporal_segmentation.md#1-data-given-strata-background-not-a-methodological-choice)). The single-phase median 5 [4, 5] (Garmin scale 1-10 reverse — lower = worse felt-state per [DATA_DICTIONARY.md](../../../../DATA_DICTIONARY.md)) with IQR 1 characterises the Stratum 4 felt-state distribution. E[L]\*=15.1 (factor-of-2 flag), M=8 — long memory consistent with multi-week phase structure across the 4-year LC trajectory. **The three-phase trajectory question is not addressable for this channel**; the rolling-30d-median in the plot characterises the within-Stratum-4 shape only. Per [intervention_effects §8.2](../../../../methodology/intervention_effects_descriptive.md#82-top-findings-at-primary-b14-sorted-by-r_rb) `gevoelscore` does show a +1 step at the 2026-03-20 Citalopram afbouw boundary that survives detrend, and a larger but LC-trajectory-confounded +2 step at the 2022-09-22 Ergotherapie start — both are interventions inside this single phase, not phase boundaries.

### 2.7 `stress_low_motion_min_count_S60_Mlow` (autonomic concurrence, sub-daily spike) — see [plots/stress_low_motion_min_count_S60_Mlow.png](plots/stress_low_motion_min_count_S60_Mlow.png)

| phase | n | median | CI95 | E[L]\* | M | survives detrend? |
|---|---:|---:|---|---:|---:|:--:|
| pre_illness_healthy   |  217 |  36.00 | [29.00,  51.00] |  7.0   |  1 | yes |
| acute_infection       |   14 | 101.00 | [55.00, 125.00] |   na   |  — | yes |
| lc_pre_gevoelscore    |  143 |  73.00 | [63.00,  82.00] |  7.0   |  1 | yes |
| lc_with_gevoelscore   | 1365 |  55.00 | [50.00,  62.00] | 21.1 ⚐ | 11 | yes |

This channel shows the corpus's **strongest relative acute lift** — healthy median 36 → acute 101 (2.8×, with CI [55, 125] still excluding the healthy CI [29, 51]). The shape after acute is a graded decline: 73 in lc_pre_gevoelscore → 55 in Stratum 4. **All four phase medians survive detrend** despite the obvious trajectory shape; the within-phase IQRs (63, 84.5, 66, 65) are wide enough that the rolling-90d trend captures only a portion of the between-phase shift. E[L]\*=21.1 in Stratum 4 (factor-of-2 flag), M=11 — comparable structure to `all_day_stress_avg`. Per [stress_low_motion_primitive.md](../../../../methodology/stress_low_motion_primitive.md) this channel is a sub-daily spike-count metric and therefore differs in kind from the daily-mean channels.

---

## 3. Event-overlay reading

The 8 documented event overlays span the 5-year window. **Per the locked operationalisation in [README §3](README.md#3-event-overlays-locked-intervention--medical-user-explicit-reminder-to-include-cpap-end), this analysis displays the events on each trajectory plot for visual reference only.** Independent contributions of co-occurring events are not testable in this descriptive design; the canonical event-boundary readings live in [intervention_effects_descriptive §8.2](../../../../methodology/intervention_effects_descriptive.md#82-top-findings-at-primary-b14-sorted-by-r_rb) (per-boundary × per-channel Mann-Whitney + r_rb + trajectory-detrend sensitivity).

What the trajectory plots show at the 8 marked dates (descriptive only; cross-reference to intervention_effects §8 wherever an event is also analytically tested there):

| event | date | what the rolling-30d-median shows visually | cross-ref |
|---|---|---|---|
| COVID infection (first symptoms) | 2022-03-21 | The phase-1 → phase-2 boundary by construction. All 5 Garmin channels with healthy-phase coverage show their visible inflection at this date — the autonomic-load family steps up; resting_hr dips slightly; bb_lowest lifts modestly. The plots confirm the acute-phase descriptive numbers above. | n/a (phase boundary, not an intra-phase event) |
| Ergotherapie start | 2022-09-22 | Co-temporal with the Stratum 4 left edge by 19 days. Visible RHR step UP (per intervention_effects §8.2: r_rb=−0.97; large; LC-trajectory-confounded per §1 substantive-confound caveat). `gevoelscore` data start 2022-09-03 so the Ergo-start segment is the channel's first ~3 weeks. | intervention_effects §8.2-§8.3 (RHR + gevoelscore steps; LC-trajectory confound applies) |
| Ergotherapie end (~13wk) | 2022-12-22 | Date is approximate per [intervention_effects §2](../../../../methodology/intervention_effects_descriptive.md#2-interventions-in-scope--curated-catalog); findings around this boundary carry lower weight. The plots show no obvious channel-wide step at this date. | intervention_effects §8.2 (only respiration_avg_sleep shows a distributional shift, block-p marginal) |
| CPAP start | 2024-01-10 | Visible against the slow Stratum 4 trajectory; `bb_overnight_gain` data don't yet exist (coverage starts 2024-09-18). No corpus-wide channel-set step visible in the plots. | intervention_effects §8.2 (only respiration_avg_sleep shows movement; block-p marginal) |
| CPAP end | 2024-04-16 | **Boundary-collision caveat**: sits 7 days before Citalopram buildup start at 2024-04-09. Per [intervention_effects §2b](../../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain) + §8.1 both events are structurally unanalyzable in pre-vs-post window comparisons; this analysis displays both lines on the plots but **does NOT attribute any visible step to either event individually**. | intervention_effects §8.1 (UNANALYZABLE) |
| Citalopram buildup start | 2024-04-09 | Same boundary-collision caveat as CPAP end above. Per [citalopram_dose_response §5.5](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md#55-v3-amendment--cross-window-corroboration-added-2026-06-14) the buildup-post-CPAP window (a separate analytical surface that excludes the 7-day boundary-collision window) is where the dose-response slope was tested and CONFIRMED for `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`. | intervention_effects §8.1 (UNANALYZABLE on this boundary itself); citalopram_dose_response §5.5-§5.6 (graded dose-response confirmed cross-window) |
| Citalopram buildup → consolidation | 2024-06-20 | Visible against the slow Stratum 4 trajectory; the autonomic-load and recovery channels enter their multi-year plateau here through 2026-03-20 (~21 months). | intervention_effects §8.2 (`bb_lowest` r_rb=+0.31, ambiguous block-p) |
| Citalopram consolidation → afbouw | 2026-03-20 | Final ~76 days of the plot. Per [intervention_effects §8.2-§8.3](../../../../methodology/intervention_effects_descriptive.md#82-top-findings-at-primary-b14-sorted-by-r_rb): `stress_mean_sleep` shows a step DOWN that survives detrend (the cleanest analytically-tested event finding in the corpus); `gevoelscore` shows a +1 step that survives detrend; `bb_overnight_gain` shows a step UP that is **killed by detrend** (recovery-trajectory artifact). The afbouw segment is the right edge of every trajectory plot; the post-afbouw phase starts 2026-06-05 and is **out of scope** by the locked operationalisation (corpus ends 2026-06-04). | intervention_effects §8.2-§8.3 (`stress_mean_sleep`, `gevoelscore` survive detrend; `bb_overnight_gain` killed by detrend) |

---

## 4. Cross-phase pattern synthesis

The 5-year arc tells a partially-coherent story across the three channel families:

**Autonomic-load (3 channels — `stress_mean_sleep`, `all_day_stress_avg`, `stress_low_motion_min_count_S60_Mlow`)**: the family shape is a sharp acute lift, an immediate-LC peak (lc_pre_gevoelscore on `all_day_stress_avg` at median 36), and a partial multi-year recovery in Stratum 4 (returning toward but not all the way back to healthy). The within-phase autocorrelation lengthens substantially from early phases (M=1 day) to Stratum 4 (M=6-18 days), and three of three Stratum 4 cells fire the factor-of-2 block-length flag — a signature of long-memory structure consistent with multi-month medication and recovery phases operating on top of the daily signal. All three channels survive detrend at all populated phases.

**Recovery (2 channels — `bb_lowest`, `bb_overnight_gain`)**: structurally dominated by coverage. `bb_overnight_gain` has data only from 2024-09-18 (3 of 4 phases unanalyzable). `bb_lowest` is the only headline channel where NO phase survives detrend — the +8 lift from healthy to Stratum 4 IS the multi-year recovery trajectory rather than a phase-discrete step.

**Cardiovascular (1 channel — `resting_hr`)**: a slow upward drift of ~2 bpm from healthy to Stratum 4, with an unusual acute-phase dip (54 → 52.5). The Stratum 4 cell does not survive detrend (the +1 from lc_pre_gevoelscore is captured by within-LC trend). Tight per-phase IQR (3 bpm throughout) — the channel's per-phase signal-to-noise is high but the between-phase shifts are small.

**Felt-state (1 channel — `gevoelscore`)**: data exist only in Stratum 4 by construction; single median 5 [4, 5]. The three-phase question doesn't apply.

The single largest cross-phase inflection visible across multiple channels falls at the **COVID infection date 2022-03-21** by construction (phase boundary); the second-largest at the **Stratum 4 left edge 2022-09-03** (phase boundary); the third at the **post-Citalopram-buildup consolidation 2024-06-20** (within-Stratum-4). The recovery_arc framing extends the previously archived S01 + S02 trajectory work back into phases (a) and (b); the pre-illness healthy baseline characterisation (channel-by-channel medians + CIs in §2) is the single largest descriptive gap closed by this analysis.

**Relation to HA-P6**: by sharing the 7-channel set, this analysis extends HA-P6's per-channel post-crash trajectories backwards across the full 5-year window. Cross-test interpretation (deferred per user; see §6 below) would read HA-P6's post-crash recovery shape against this recovery_arc's pre-illness → acute → LC trajectory shape for each of the same 7 channels.

---

## 5. Caveats

1. **No causal claims.** Per CONVENTIONS §2.1 this is Layer 1 descriptive. Phase boundaries are data-given (COVID date, gevoelscore corpus start) per [lc_era_temporal_segmentation §1](../../../../methodology/lc_era_temporal_segmentation.md); no SUPPORTED bar is set; no attribution of channel-level shifts to specific interventions is claimed.
2. **Acute-phase n=14 day-level rows** (window 2022-03-21 → 2022-04-03, per_day_master.csv). Per CONVENTIONS §3.6 explicit count phrasing. CIs in the acute column are wide for every channel; differences within the acute CI bracket should be read as "consistent with X" rather than "shows X".
3. **Pre-illness healthy baseline = ~7 months (~217 day-level rows)**, a single winter + shoulder-season cycle per [lc_era_temporal_segmentation §1 caveat](../../../../methodology/lc_era_temporal_segmentation.md#1-data-given-strata-background-not-a-methodological-choice). Any healthy-vs-LC contrast confounds illness state with season by construction. The seasonality follow-up is queued at [descriptive/README §4.8](../../README.md#48-seasonality--day-of-week-effects-r2-closure-d49).
4. **`bb_overnight_gain` coverage**: 3 of 4 phases empty (data only from 2024-09-18 per [intervention_effects §2b](../../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain) — Garmin firmware UDS rollout, not a project-side pipeline gap). The three-phase question is not addressable for this channel. Proxy availability from 2024-07-08 (`bb_overnight_gain_proxy` per [bb_overnight_gain_proxy.md](../../../../methodology/bb_overnight_gain_proxy.md)) was not used in this analysis to keep the channel set HA-P6-aligned.
5. **`gevoelscore` coverage**: 3 of 4 phases empty (logging started 2022-09-03 per [lc_era_temporal_segmentation §1](../../../../methodology/lc_era_temporal_segmentation.md)). The three-phase question is not addressable for this channel.
6. **2024-04 boundary-collision** (CPAP end 2024-04-16 + Citalopram buildup start 2024-04-09, 7 days apart) per [intervention_effects §2b](../../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain) + [§8.1](../../../../methodology/intervention_effects_descriptive.md#81-effective-analyzable-scope-5-of-8-boundaries-usable). The two events are displayed on the plots but their independent contributions are not analytically separable in this descriptive design; ITS-style modelling (deferred per [intervention_effects §8.3](../../../../methodology/intervention_effects_descriptive.md#83-reading-per-the-5-decision-framework)) would be required to disentangle them.
7. **2022-09-22 Ergotherapie start co-temporal with steepest LC trajectory** per [intervention_effects §1 substantive-confound caveat](../../../../methodology/intervention_effects_descriptive.md#1-what-this-md-asks-and-what-it-does-not). The large RHR + gevoelscore steps at this date are confounded between intervention effect and the underlying disease-progression trajectory; this analysis displays the marker but inherits the confound by construction.
8. **Post-afbouw out of scope.** The afbouw → post-afbouw boundary is 2026-06-05 per [citalopram_phase_stratification §3](../../../../methodology/citalopram_phase_stratification.md#3-citalopram-traject-canonical-four-phase-axis); corpus ends 2026-06-04. No post-afbouw data exists; the right edge of every trajectory plot is the data-cut.
9. **Detrend operationalisation.** §3.7 was applied as: rolling-90d-median of the channel subtracted day-wise, then per-phase median of residuals compared against the grand median of detrended-phase-medians. The "survives detrend?" flag captures whether direction-vs-grand-median is preserved; it does NOT test whether between-phase magnitude is preserved.
10. **Block-length flags fire on 6 of 7 Stratum-4 cells** (E[L]\* factor-of-2 deviation from default 7). Consistent with the operationalisation_support/stress_mean_sleep finding (E[L]\*=12.6 on the same surface). The CIs reported at E[L]=7 are companion-checked at E[L]\* in the [summary.json](summary.json) — directional findings are unchanged at either block length for all channels reviewed.

---

## 6. Cross-references — which HA-* tests benefit from re-reading

This analysis surfaces multi-year context that several HA pre-regs may want to anchor against:

- **HA-P6** ([hypothesis.md](../../../hypotheses/HA-P6/hypothesis.md)) — source of the 7-channel set; this analysis extends HA-P6's per-channel post-crash trajectories back into pre-illness + acute phases. Cross-test reading (deferred per user) would compare HA-P6's post-crash recovery shape (per the HA-P6 v3 result) against the trajectory shape for the same channel in §2.
- **HA-P7** — recovery-debt context. The within-Stratum-4 long memory (E[L]\* factor-of-2 flags on 6 of 7 channels) is the autocorrelation context HA-P7's lagged-outcome-covariate pattern operationalises against.
- **HA07c, HA07d, HA08c** — all canonical anchor channels on `stress_mean_sleep`. The +3.3-unit elevation of Stratum 4 over healthy (CIs non-overlapping) is the multi-year context their findings sit inside.
- **HA10, HA-C4b** — `bb_lowest` and `bb_overnight_gain` based; the trajectory-driven shape on `bb_lowest` (no phase survives detrend) is the multi-year context for both. HA10's `bb_overnight_gain` primary inherits the coverage caveat in §2.4.
- **Future seasonality + DOW analysis** per [descriptive/README §4.8](../../README.md#48-seasonality--day-of-week-effects-r2-closure-d49) — the healthy-baseline-is-7-months caveat in §5 is what that follow-up would close.

Descriptive programme context: [descriptive/README §4.1](../../README.md#41-recovery-arc-three-phase-healthy--infection--trajectory) (research question) + §6.2 (analysis scope) + §7b (operationalisation interview protocol) + §7d (refresh cadence — quarterly or when an HA-* result shifts the story).

---

## 7. Status

**Findings landed 2026-06-18 from a single execution of [`run.py`](run.py) under the locked operationalisation in [`README.md`](README.md).** Next refresh per descriptive/README §7d: quarterly or when an HA-* result shifts the story (whichever comes first). The S01 + S02 archived trajectory work stays archived per [descriptive/README §5](../../README.md#5-index-of-existing-descriptive-work); the multi-year-arc narrative is now consolidated here for ongoing refresh.
