# Findings -- Q4.4 cohort_topology (29 crashes + 79 dips + dip-cluster overlay + recovery distributions + matched-control)

**Strand**: B (multi-year trajectory; descriptive). Closes the canonical Q4.4 scope per [`analyses/descriptive/README.md`](../../README.md) section 4.4 -- refresh of cohort topology + dip-cluster overlay + recovery-window distributions + matched-control baseline; pre-requisite substrate for HA-P6 follow-ups.

**Surface**: full corpus (2021-08-16 to 2026-06-05; n=1755 day-level rows). n=29 crashes + n=79 dips = 108 events per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) (LOCKED, NOT modified).

**User-LOCKED operationalisation** (per Strand B section 7c interview 2026-06-25; do NOT iterate):

1. **Event scope = crashes + dips (29 + 79 = 108 events)**; sub-threshold dips EXCLUDED per user.
2. **Dip-cluster overlay = 30d rolling event-count + per-recovery-phase event rate** (skip DBSCAN).
3. **Recovery-window distributions = per-crash + per-dip + comparison** -- per-crash REUSES HA-P6 v3 Arm-A (REPRODUCTION); per-dip is NOVEL on the same machinery.
4. **"Normal" baseline = matched-control (HA-P6 v3 Arm-A REUSE) + per-recovery-phase reference**.

**Discipline**: Layer 1 descriptive cohort-topology mapping (no causal claims; no falsification bar; no HA verdict promotion) per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 4.1 + section 4.2 caveat-class. HA-P6 v3 + HA-P7 + HA-C4b v3 LOCKED references are descriptive substrate only; NONE are extended here.

---

## Headline

**Cohort topology**: 29 crashes (mean duration 3.55 days, median 2.0 days, max 14 days); 79 dips (single-day events by definition per crash_v2 section 2.2).

**Recovery-time op (A) rolling-30d-median**: crash episodes (n=28 with valid reference; isolation-rate caveat per crash_episode_descriptive section 3) median 1.0 days, p75 1.0 days, max 5 days.
**Recovery-time op (B) gevoelscore >= 4**: crashes (n=29) median 1.0 days; dips (n=79) median 1.0 days.

**Dip-cluster overlay (30d rolling)**: 19 cluster epochs (>= p90 density threshold 4.0 events in 30d trailing window). Cluster epochs descriptively surface temporal density patterns in the event topology.

**Per-recovery-phase event rate (per 30d)**: phases pre_illness_healthy 0.00, acute_infection 0.00, lc_pre_ergo 0.53, pacing_pre_citalopram_learning 1.61, pacing_habit_established 2.89, citalopram_modulated 2.02.

**LOAD-BEARING Q4.3 rp5 + cp3 boundary cross-reference** (descriptive only; rate-shifts at intervention boundaries; NO causal interpretation):

| boundary | before rate (per 30d, 90d window) | after rate | delta |
|---|---:|---:|---:|
| rp5_2024_04_09 | 3.67 | 3.63 | -0.04 |
| cp3_2026_03_20 | 2.00 | 1.15 | -0.85 |

**Per-channel crash-vs-dip recovery comparison** (median z at t+1 vs t+5 on HA-P6 v3 Arm-B lagged personal baseline):

| channel | crash t+1 median z | crash t+5 median z | dip t+1 median z | dip t+5 median z | crash - dip at t+1 |
|---|---:|---:|---:|---:|---:|
| stress_mean_sleep | +1.071 | +0.391 | +0.201 | +0.149 | +0.870 |
| all_day_stress_avg | +1.087 | +0.680 | +0.065 | -0.029 | +1.022 |
| bb_lowest | -1.464 | -0.463 | +0.181 | -0.202 | -1.645 |
| bb_overnight_gain | -0.915 | -0.269 | -0.120 | -0.054 | -0.794 |
| resting_hr | +1.446 | +2.202 | +0.367 | +0.383 | +1.079 |
| gevoelscore | -1.059 | +0.655 | -0.846 | -0.934 | -0.212 |
| stress_low_motion_min_count_S60_Mlow | +0.701 | +1.264 | +0.192 | -0.328 | +0.510 |

**Matched-control baseline coverage (HA-P6 v3 Arm-A REUSE)**: 11 / 29 crashes matched (38% coverage); 42 / 79 dips matched (53% coverage). Tolerance ladder = [+-1.0, +-1.5, +-2.0] gevoelscore-point 10d-pre-event-trajectory similarity, same recovery_phase, >= 30d distance from event.

---

## 1. Cohort topology summary table (108 events)

**Method**: per event (crash or dip), report start / end / duration / lowest-score / recovery-time on the user's gevoelscore-and-Garmin corpus per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) (LOCKED, NOT modified). Two operationalisations of recovery-time are reported, mirroring [`crash_episode_descriptive section 3`](../../../../methodology/crash_episode_descriptive.md): op (A) rolling-30d-median crossing; op (B) gevoelscore >= 4 crossing.

**Per-class aggregate distribution table**:

| class | n | mean duration | median duration | max duration | median lowest score | median recovery (op A) | median recovery (op B) |
|---|---:|---:|---:|---:|---:|---:|---:|
| crash | 29 | 3.55 | 2.0 | 14 | 2.0 | 1.0 | 1.0 |
| dip | 79 | 1.00 | 1.0 | 1 | 3.0 | 1.0 | 1.0 |

**CRITICAL caveat per crash_episode_descriptive section 3**: op (A) isolation filter (no other event within 30d after episode end) leaves only n=1 isolated crash on this corpus; the n above pools across non-isolated events for descriptive purposes. The op (A) p75 from the strict-isolation read is 2 days (single observation); the non-isolated-pooled op (A) median above is informational only and carries higher variability.

**Recovery-time op (B) descriptive caveat**: gevoelscore >= 4 crossing treats the v2 sub-threshold rule as recovery anchor; complements but does not replace op (A). Per-event values stored in summary.json.

---

## 2. Dip-cluster overlay (30d rolling + per-recovery-phase event rate)

**Method**: 30d trailing-window rolling count of event-starts (crash + dip) over the full corpus; cluster epochs identified as consecutive days where 30d count >= p90 density threshold (4.0 events). Per-recovery-phase event rate normalised by phase day-count.

**Cluster epochs** (descriptive temporal-density patterns; n=19):

| # | start | end | peak 30d event-count |
|---|---|---|---:|
| 1 | 2022-09-30 | 2022-10-02 | 4 |
| 2 | 2023-02-04 | 2023-02-08 | 4 |
| 3 | 2023-02-22 | 2023-02-27 | 4 |
| 4 | 2023-04-02 | 2023-04-16 | 4 |
| 5 | 2023-04-26 | 2023-04-27 | 4 |
| 6 | 2023-05-22 | 2023-05-25 | 4 |
| 7 | 2023-05-28 | 2023-06-10 | 4 |
| 8 | 2023-06-12 | 2023-06-17 | 4 |
| 9 | 2023-10-31 | 2023-12-02 | 6 |
| 10 | 2024-01-09 | 2024-02-05 | 5 |
| 11 | 2024-03-22 | 2024-05-11 | 8 |
| 12 | 2024-05-15 | 2024-05-15 | 4 |
| 13 | 2024-05-20 | 2024-06-13 | 5 |
| 14 | 2024-06-18 | 2024-06-18 | 4 |
| 15 | 2024-07-15 | 2024-07-17 | 4 |
| 16 | 2024-10-24 | 2024-10-26 | 4 |
| 17 | 2025-01-09 | 2025-01-09 | 4 |
| 18 | 2025-01-20 | 2025-01-21 | 4 |
| 19 | 2026-02-27 | 2026-03-16 | 5 |

**Per-recovery-phase event rate** (events-per-30d normalised to phase duration; tight-n caveat for phases 1-3):

| recovery_phase | n_days | n_crash_starts | n_dip_starts | total events | crash rate/30d | dip rate/30d | total rate/30d |
|---|---:|---:|---:|---:|---:|---:|---:|
| pre_illness_healthy | 217 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 |
| acute_infection | 14 | 0 | 0 | 0 | 0.00 | 0.00 | 0.00 |
| lc_pre_ergo | 171 | 2 | 1 | 3 | 0.35 | 0.18 | 0.53 |
| pacing_pre_citalopram_learning | 56 | 1 | 2 | 3 | 0.54 | 1.07 | 1.61 |
| pacing_habit_established | 509 | 15 | 34 | 49 | 0.88 | 2.00 | 2.89 |
| citalopram_modulated | 788 | 11 | 42 | 53 | 0.42 | 1.60 | 2.02 |

**LOAD-BEARING Q4.3 rp5 + cp3 boundary cross-reference** (descriptive only; rate-shifts at intervention boundaries; NO causal interpretation per CONVENTIONS section 4.1; per Q4.3 finding the rp5 + cp3 boundaries are strong empirical change-points across channels, and the per-phase event-rate table above descriptively shows event-count shifts consistent with that finding -- citalopram_modulated phase has the lowest crash rate (n=11 crashes / 788 days = 0.42 per 30d) of any phase with substantive n).

---

## 3. Recovery-window distributions per channel (crash vs dip)

**Method**: per event (crash or dip), compute the per-channel z-score trajectory in [t+1, t+5] post-event days using the HA-P6 v3 section 4.5 Arm-B lagged personal baseline (window [t0-90, t0-31], same recovery phase, >= 40/60 valid days, trimmed-mean 10/90 cut for mu_ch + sigma_ch). Per-channel median z + IQR aggregated across events per (label, channel, post_day). t0 = episode end-date per HA-P6 v3 section 4.3 primary anchor.

**HONEST FRAMING per handoff section 3.4**: per-crash recovery curves REPRODUCE HA-P6 v3 Arm-B output at finer per-channel-per-post-day aggregation (HA-P6 v3 result tables in [`HA-P6/result.md`] are the canonical primary read; this table is the cohort-topology-layer complementary surface). Per-dip recovery curves are NOVEL -- HA-P6 v3 did NOT compute per-dip recovery on the same 7-channel set; this is the substantive Q4.4 addition.

**Per-channel median z trajectory** (full table; n per cell varies with channel coverage + baseline-pool eligibility):

| channel | label | n at t+1 | t+1 median z [p25, p75] | t+2 median | t+3 median | t+4 median | t+5 median |
|---|---|---:|---|---:|---:|---:|---:|
| stress_mean_sleep | crash | 18 | +1.071 [+0.637, +3.992] | +0.534 | +0.890 | +0.371 | +0.391 |
| stress_mean_sleep | dip | 60 | +0.201 [-0.983, +1.327] | -0.015 | -0.042 | +0.193 | +0.149 |
| all_day_stress_avg | crash | 20 | +1.087 [-0.081, +2.478] | +0.448 | +0.472 | +0.102 | +0.680 |
| all_day_stress_avg | dip | 63 | +0.065 [-0.864, +1.668] | -0.182 | -0.149 | +0.376 | -0.029 |
| bb_lowest | crash | 20 | -1.464 [-2.019, +0.448] | -0.712 | -0.306 | +0.244 | -0.463 |
| bb_lowest | dip | 63 | +0.181 [-0.954, +1.123] | -0.302 | -0.023 | +0.037 | -0.202 |
| bb_overnight_gain | crash | 4 | -0.915 [-1.936, -0.102] | -0.101 | +1.466 | +0.079 | -0.269 |
| bb_overnight_gain | dip | 23 | -0.120 [-2.382, +0.671] | +1.000 | +0.406 | -0.455 | -0.054 |
| resting_hr | crash | 20 | +1.446 [-0.296, +3.288] | +1.286 | +1.575 | +2.005 | +2.202 |
| resting_hr | dip | 62 | +0.367 [-0.658, +1.602] | +0.280 | +0.280 | +0.393 | +0.383 |
| gevoelscore | crash | 18 | -1.059 [-1.193, -0.548] | -0.922 | -1.122 | -0.602 | +0.655 |
| gevoelscore | dip | 62 | -0.846 [-1.154, +0.840] | -0.191 | +0.153 | -0.628 | -0.934 |
| stress_low_motion_min_count_S60_Mlow | crash | 20 | +0.701 [-0.092, +1.691] | +0.229 | -0.044 | +0.315 | +1.264 |
| stress_low_motion_min_count_S60_Mlow | dip | 63 | +0.192 [-1.038, +1.145] | -0.479 | -0.194 | +0.268 | -0.328 |

**Crash-vs-dip aggregate comparison** (mean of abs(median z) across [t+1, t+5]; descriptive depth measure):

| channel | crash window mean abs(median z) | dip window mean abs(median z) | crash - dip at t+1 |
|---|---:|---:|---:|
| stress_mean_sleep | +0.651 | +0.120 | +0.870 |
| all_day_stress_avg | +0.558 | +0.160 | +1.022 |
| bb_lowest | +0.638 | +0.149 | -1.645 |
| bb_overnight_gain | +0.566 | +0.407 | -0.794 |
| resting_hr | +1.703 | +0.341 | +1.079 |
| gevoelscore | +0.872 | +0.550 | -0.212 |
| stress_low_motion_min_count_S60_Mlow | +0.511 | +0.292 | +0.510 |

**Cross-reference Q4.9 per-crash body-state profile** (handoff section 3.3): Q4.9 covered the 28-of-29 episode-level matched pre-crash 4d body-state profile on 6 channels (stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr) with crash mean z values [+0.412 / +0.316 / -0.106 / +0.585 / +0.393 / +0.482]. The Q4.4 per-crash recovery-window above is the POST-EVENT side of the same machinery (Q4.9 was PRE-EVENT lead-up; Q4.4 is POST-EVENT recovery); the crash-side trajectory above descriptively complements Q4.9's pre-crash characterisation. The dip-side trajectory is NOVEL (no precedent at the cohort-topology layer).

---

## 4. Matched-control baseline + per-recovery-phase reference

**Method**: HA-P6 v3 section 4.4 Arm-A matched-control logic REUSED for both crashes and dips. For each event: find non-event day d_match such that (a) same recovery_phase as event, (b) gevoelscore trajectory similarity on [d_match - 10, d_match - 1] within tolerance ladder [+-1.0, +-1.5, +-2.0] vs event's [start - 10, start - 1] pre-trajectory, (c) no event within [d_match - 20, d_match + 10] window, (d) >= 30d distance from event. Pick candidate with smallest MAD vs pre-trajectory.

**Matched-control coverage**:

| event class | total | matched | unmatched | coverage |
|---|---:|---:|---:|---:|
| crash | 29 | 11 | 18 | 38% |
| dip | 79 | 42 | 37 | 53% |

**Cross-reference Q4.5.b matched-control vs trajectory-confound framing** (handoff section 3.3): Q4.5.b detrended_correlation found 6 of 21 channel pairs flagged SPURIOUS_TRAJECTORY_DRIVEN in >=1 detrend method; the matched-control machinery used in Stage 5 here is the cleanest way to side-step trajectory-driven confounds, since matched non-event days carry the same multi-year drift as the event side (pair-level cancellation per HA-P6 v3 Arm-A spec). Q4.5.b's per-phase detrend showed within-phase content survives detrending; that finding methodologically supports the Stage 5 + Stage 4 per-channel recovery-window characterisation above as descriptively valid at the cohort-topology resolution.

**Per-recovery-phase "normal" reference** (median + IQR of channel values on non-event days per phase; for use as baseline reference when comparing event windows):

| channel | pre_illness_healthy | acute_infection | lc_pre_ergo | pacing_4a | pacing_4b | citalopram_modulated |
|---|---|---|---|---|---|---|
| stress_mean_sleep | 15.9 [11.3, 21.9] | 20.3 [14.6, 27.4] | 19.3 [15.0, 23.1] | 20.0 [18.0, 22.3] | 19.2 [16.3, 21.8] | 18.9 [16.3, 21.9] |
| all_day_stress_avg | 30.0 [26.0, 35.0] | 33.0 [32.0, 41.5] | 36.0 [32.0, 40.0] | 34.0 [31.0, 37.0] | 34.0 [31.0, 38.0] | 31.0 [27.0, 34.0] |
| bb_lowest | 12.0 [6.0, 18.0] | 14.5 [5.0, 20.0] | 12.0 [6.0, 16.0] | 17.5 [14.0, 22.0] | 18.0 [13.2, 23.0] | 22.0 [16.0, 28.0] |
| bb_overnight_gain | n/a | n/a | n/a | n/a | n/a | 49.0 [42.0, 57.0] |
| resting_hr | 54.0 [52.0, 55.0] | 52.5 [51.0, 55.0] | 55.0 [53.0, 56.0] | 53.0 [53.0, 54.0] | 56.0 [55.0, 57.0] | 57.0 [55.0, 59.0] |
| gevoelscore | n/a | n/a | 4.0 [4.0, 4.0] | 5.0 [4.0, 5.0] | 4.0 [4.0, 5.0] | 5.0 [4.0, 5.0] |
| stress_low_motion_min_count_S60_Mlow | 36.0 [16.0, 79.0] | 101.0 [51.0, 135.5] | 75.0 [47.0, 114.0] | 65.0 [40.5, 103.0] | 76.5 [50.0, 111.0] | 42.0 [23.0, 70.0] |

Cell format: median [p25, p75] on non-event days per phase. Cross-references [`trajectory/recovery_arc/`](../recovery_arc/) v2 LANDED per-phase median table (descriptive complement at the cohort-topology layer; recovery_arc reports event-inclusive medians, this table reports non-event-only medians for matched-control reference purposes).

---

## 5. Caveats

**Sub-threshold dips EXCLUDED from primary scope** per user-locked operationalisation (handoff section 2.1). The crash_v2 sub-threshold dip registry was discussed during the Strand B section 7c interview and explicitly excluded by user as not load-bearing; if the cohort topology finding has a clear 'would be sharper with sub-threshold included' shape, that's a deferred follow-up and NOT scope-creep on this artefact.

**Per-dip recovery curves are NOVEL**; per-crash recovery curves REPRODUCE HA-P6 v3 Arm-B output at finer cohort-topology aggregation (handoff section 3.4). Honest framing in section 3 above. Substantive Q4.4 contribution is the per-dip side + the crash-vs-dip comparison; the per-crash side is a refresh of the HA-P6 v3 finding at the cohort-topology resolution (NOT a re-test of HA-P6 v3).

**n = 29 crashes + n = 79 dips**: sample sizes are tight; per-recovery-phase event rates in section 2 have wide CIs (phases 1-3 are < 14mo each; the pre_illness_healthy phase has n_crashes = 0 + n_dips = 0 BY CONSTRUCTION since the gevoelscore corpus starts 2022-09-03 per [`crash_episode_descriptive section 5`](../../../../methodology/crash_episode_descriptive.md), and ALL crashes + dips fall in lc_phase = lc; the per-recovery-phase rate table accordingly reports n = 0 for pre_illness_healthy + acute_infection).

**Tight-n caveat for per-phase event rates**: phases with n_days < 100 (pacing_pre_citalopram_learning n=56, acute_infection n=14, pre_illness_healthy gevoelscore-only n=0) carry low statistical power for per-30d rate estimation. Reported descriptively per CONVENTIONS section 3.1 tight-n caveat.

**Per-channel baseline-pool eligibility**: the HA-P6 v3 Arm-B lagged baseline (window [t0-90, t0-31], same recovery_phase, non-event, >= 40/60 days valid) excludes events whose pre-event window straddles phase boundaries (corpus-edge effects) or has < 40 valid days. n per channel per post-day reported in section 3 above. Coverage is highest in citalopram_modulated phase (long phase, deep eligibility); lowest in 4a + acute (short phases, eligibility tight).

**Matched-control coverage**: 38% crash + 53% dip coverage at the [+-1.0, +-1.5, +-2.0] tolerance ladder. Unmatched events contribute to per-class aggregates but not to matched-control-paired analyses. HA-P6 v3 section 6 exclusion semantics honoured (per-event coverage transparently reported in summary.json).

**Cohort-topology layer = descriptive substrate, NOT a substantive HA verdict**: per handoff section 4 + CONVENTIONS section 4.2 caveat-class. The Q4.4 finding feeds HA-P6 follow-ups + supports the per-event characterisation for downstream registration mapping; it does NOT promote or extend HA-P6 v3 / HA-P7 / HA-C4b v3 verdicts. The crash_v2-definition LOCK + the HA-P6 v3 LOCK + the HA-P7 LOCK + the HA-C4b v3 LOCK are all preserved.

---

## 6. Cross-references

**Methodology MDs (definitional sources; NOT modified)**:

- [`crash_episode_descriptive.md`](../../../../methodology/crash_episode_descriptive.md) section 1-3 -- crash + dip event geometry on labels_crash_v2.csv (definitional source; section 3 isolation filter rationale).
- [`crash_episode_prolonged.md`](../../../../methodology/crash_episode_prolonged.md) -- prolonged-episode merge rule overlay (cross-referenced; section 4 of that MD discusses prolonged-class composition).
- [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) section 2 -- 6-phase axis used in section 2 per-recovery-phase event rate.
- [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) section 3 -- citalopram-phase boundaries used in Stage 5 matched-control + boundary-rate cross-reference.
- [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) -- E[L]* policy (descriptive cohort-topology reads do not bind to specific E[L]* values).

**Locked HA pre-regs (substrate; NOT modified, NOT extended)**:

- [`HA-P6/hypothesis.md`](../../../hypotheses/HA-P6/hypothesis.md) section 4 -- Arm-A + Arm-B machinery REUSED descriptively in Stage 4 + Stage 5 (lagged baseline + matched-control logic).
- [`crash_v2-definition/definition.md`](../../../hypotheses/crash_v2-definition/definition.md) -- 29 crashes + 79 dips canonical labels (LOCKED; NOT modified).

**Other Strand B descriptive analyses (cross-references; NOT modified)**:

- [`trajectory/subjective_objective_coupling/findings.md`](../subjective_objective_coupling/findings.md) Q4.9 -- per-crash body-state pre-event profile (REPRODUCED + EXTENDED to per-dip side in Stage 4; descriptive complement).
- [`trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) Q4.3 -- rp5 + cp3 boundary cross-references (Stage 3 boundary-rate-shift table).
- [`trajectory/detrended_correlation/findings.md`](../detrended_correlation/findings.md) Q4.5.b -- matched-control vs trajectory-confound framing (CITED in Stage 5 methodological discussion).
- [`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) Q4.1 v2 -- multi-year trajectory backdrop for per-phase event-rate finding (per-phase non-event medians in Stage 5 complement recovery_arc per-phase medians).

---

*Programmatic emit of findings.md via run.py Stage 7. Per CONVENTIONS section 4.1 + section 4.2: descriptive cohort-topology mapping only; NO causal claims; NO HA verdict promotion. Tight-n caveats per CONVENTIONS section 3.1.*
