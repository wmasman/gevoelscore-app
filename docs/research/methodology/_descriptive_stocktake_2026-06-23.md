# Descriptive coverage stocktake — 2026-06-23

**Purpose**: Execute §11 step 3 of `_plan_results_analysis_layer.md` (r4 LOCKED 2026-06-23). Walk every HA pre-reg in `analyses/hypotheses/`, apply the §6.1 load-bearing-assumption checklist, and produce a gap list of descriptive backstops that don't yet exist. This stocktake sizes Stage D's downstream backlog and informs which HAs have descriptively trustworthy verdicts for inclusion in the §3.6 synthesis-structure map (§11 step 5).

**Method**: Cold read of the rubric files (`_plan_results_analysis_layer.md` §6.1 + the five anchor methodology MDs: `symptom_mention_asymmetry.md`, `lc_era_temporal_segmentation.md`, `permutation_null_block_length.md`, `train_validate_split_fate.md`, `nightly_attribution.md`). Enumeration of all HA folders via Glob. Per-HA inspection of hypothesis.md (Authorship + §1-§4 + §7-§8) plus result.md headline for verdict. Pattern-match against `analyses/descriptive/` (3 landed analyses) + `analyses/garmin_exploration/cards/` (4 derivative cards) + `methodology/*_descriptive.md` MDs that pre-answer Stage D questions.

**Mode**: Producer-mode artefact per §4 of the plan. Not a methodology MD; not subject to fresh-session `/research-methodology-review` (this is an enumeration; the plan's §6.1 rubric is the binding artefact, not this stocktake).

**Scope of "HA"**: thirty pre-registration folders carry a `hypothesis.md`. Seven downstream `*-threshold-monotonicity-diagnostic*` folders and one `HA01b-per-axis-diagnostic` folder carry a `diagnostic.md`, not a `hypothesis.md`; per the testing playbook these are diagnostics binding to parent verdicts, not freestanding HAs in the §6.1 sense, and are not rowed individually below — their assumptions inherit from the parent HA. `crash_v2-definition/` is a label scheme, not an HA, and is also excluded.

---

## 1. Summary

- **HAs reviewed**: 30 (per `hypothesis.md` count from Glob).
- **Assumption-cells evaluated**: 30 × 8 = **240**.
- **BACKSTOPPED**: ~58 (24%); concentrated on the three Wave-5 C-series HAs (HA-C3 v2, HA-C3p, HA-C4c) and HA-C4 v2 / HA-C4b v3 / HA11-bout-redo which were drafted *after* the Phase-1 Strand-A descriptive analyses landed.
- **NOT BACKSTOPPED**: ~92 (38%); concentrated on the older H/HA01-11 family (drafted 2026-06-05 → 2026-06-07, **before** the descriptive programme existed). Most common gap: no per-channel ACF / E[L]\* backstop on the channel the test uses, and no per-cell sample-size descriptive (every cell relies on a hand-counted n in result.md).
- **NOT APPLICABLE**: ~90 (38%); driven by (a) no v24-derived signals in most HAs, (b) no train/validate split in newer HAs that adopted single-pool primary, (c) no nightly-sleep signals in non-sleep HAs.
- **HAs ready for Stage D TRUSTED** (every load-bearing assumption BACKSTOPPED): **4** — HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo (the four post-2026-06-18 Wave-5 HAs that explicitly cite the Strand-A descriptive analyses).
- **HAs requiring descriptive work before Stage I** (≥ 1 NOT BACKSTOPPED on a load-bearing assumption): **24**.
- **HAs flagged structurally untestable as currently specified**: **2** — H03b (INCONCLUSIVE × 12 by data availability per locked bar; the missing descriptive is "the data does not exist at the gated resolution"; routed back to pre-reg revision per §6.1 conflict rule) and S02b (no result, no descriptive backstops, and the channels-and-lag spec depends on S02's algorithmic outputs which were never independently descriptively characterised). H05 verdict is "spec-induced trivial" which is a different routing (no data path is fixable; the spec itself is the failure mode); also listed.

Compact distribution:

| status of HA | count |
|---|---:|
| Wave-5 (post-descriptive-programme): all load-bearing assumptions BACKSTOPPED | 4 |
| Older HA-* with E[L]\* + Stratum-4 binding documented per methodology but no per-cell descriptive run | 12 |
| Older H/HA tests bound to historical 2023-12-31 train/validate split; split's fate handled in methodology MD but per-cell descriptives not backstopped | 8 |
| Personal-register HAs (HA-P6, HA-P7) with mixed backstopping | 2 |
| K-series cross-era contrast tests (K01, K02) with verdict-on-record + minimal descriptive backstopping | 2 |
| Structurally-untestable-as-currently-specified | 2 (H03b, S02b) |

---

## 2. Per-HA assumption matrix

Column legend (matches §6.1 checklist order):

- **A1**: sample size on every reported cell ≥ pre-registered floor.
- **A2**: missingness pattern is MCAR/MAR-compatible OR missingness-aware operationalisation used + documented.
- **A3**: block-permutation: stationarity checked OR block-length sensitivity-tested per `permutation_null_block_length.md`.
- **A4**: era boundaries match `lc_era_temporal_segmentation.md`; Stratum 4 primary surface honored.
- **A5**: v24-presence-conditioned semantics respected per `symptom_mention_asymmetry.md`.
- **A6**: nightly/recovery signals attributed by wake-up-date per `nightly_attribution.md`.
- **A7**: effect-size direction reported alongside p-values.
- **A8**: train/validate split: single-pool primary preserved per `train_validate_split_fate.md`.

Cell legend: **B** = BACKSTOPPED (path cited); **N** = NOT BACKSTOPPED; **/** = NOT APPLICABLE; **?** = UNCLEAR (see §7).

Path abbreviations:
- `desc-SMS` = `analyses/descriptive/operationalisation_support/stress_mean_sleep/findings.md`
- `desc-SLM` = `analyses/descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/findings.md`
- `desc-RA` = `analyses/descriptive/trajectory/recovery_arc/findings.md`
- `desc-BOUT` = `analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration/result.md`
- `meth-LCP` = `methodology/lc_phase_descriptive.md`
- `meth-CDR` = `methodology/citalopram_dose_response_stress_mean_sleep.md` + sister `intervention_effects_descriptive.md`
- `meth-PSA` = `methodology/phase_axis_collapsibility_conventions.md`
- `meth-BLR` = `methodology/bout_level_recovery_dynamics.md`
- `card-PVS` = `analyses/garmin_exploration/cards/primary-verdict-statistics.md`
- `card-XCC` = `analyses/garmin_exploration/cards/cross-channel-correlation.md`
- `card-BTS` = `analyses/garmin_exploration/cards/card-b-train-specificity.md` (+ `-b2-validate-`)
- `meth-NA` = `methodology/nightly_attribution.md` (definitional, accepted as binding for sleep-derived columns)

| HA | verdict | A1 sample | A2 missingness | A3 block-length | A4 era / Stratum 4 | A5 v24 semantics | A6 nightly attrib | A7 effect-size | A8 split-fate |
|---|---|---|---|---|---|---|---|---|---|
| H01-rhr-drift | refuted (both eras) | N (per-cell n in result.md only) | N | N (no block-perm; null-window resampling pre-MD) | N (legacy train/validate split per registry §2 pre-MD) | / (no v24) | B (`meth-NA`; UDS field used) | B (pp + median delta) | N (used historical split as primary; pre-`split-fate` MD) |
| H02-stress-elevation | refuted (train signal / validate null) | N | N | N (pre-MD) | N | / | B (`meth-NA`) | B | N |
| H02b-stress-spikes | train SUPPORTED / overall refuted | N | N | N (pre-MD null draws; `card-PVS` retrofit Fisher) | N (pre-MD) | / | / (per-minute daytime) | B (+29.9 pp + p) | N |
| H02d-stress-spikes-uncensored | train SUPPORTED / overall refuted | N | N | N | N | / | / | B (`card-PVS`) | N |
| H03-sleep-efficiency | refuted both eras | N | N | N (pre-MD) | N | / | B (`meth-NA`) | B | N |
| H03b-bb-overnight-recharge-permin | INCONCLUSIVE × 12 by data availability | N (locked bar n_clean ≥ 10 not met on any of 12 cells) | N (data gap IS the missingness pattern; not absorbed by op'n) | / (no test ran) | N (pre-MD split) | / | B (`meth-NA`) | / (no verdict computed) | N |
| H04-body-battery | refuted both eras | N | N | N | N | / | B (`meth-NA`; UDS) | B | N |
| H05-recovery-time | spec-induced trivial | / (no usable cells) | / | / | N | / | / | / | / |
| HA01b-per-axis-diagnostic | DIAGNOSTIC; per-axis effective_exertion SUPPORTED both eras | N | N | N (pre-MD) | N (historical split) | / | / | B | N |
| HA01c-effective-exertion-shock | SUPPORTED-with-stability-mixed per v2 diagnostic | N | N | N | N | / | / | B (+21.3 / +19.5 pp) | N |
| HA06-morning-rhr-delta | refuted (validate 0/15 at 5 bpm; absolute-threshold mis-cal) | B (`card-PVS` n=14/15) | N | N | N | / | B (`meth-NA`) | B | N |
| HA06b-rhr-zscore | train SUPPORTED / overall refuted | B (`card-PVS`) | N | N | N | / | B (`meth-NA`) | B (`card-PVS`) | N |
| HA07-hrv-day-over-day | BLOCKED-PENDING-HARDWARE (no test) | / | / | / | / | / | / | / | / |
| HA07c-sleep-stress-mean-delta | train SUPPORTED / overall refuted | B (`card-PVS`) | N | **B for ACF/E[L]\* via `desc-SMS` Q3.1.b; N for in-test block-perm** | N (legacy split per `card-PVS`) | / | B (`meth-NA`; sleep-window mean) | B (+23.2 pp + Fisher p) | N |
| HA07d-sleep-stress-variability | both eras SUPPORTED → first OVERALL-SUPPORTED | B (`card-PVS`) | N | B (`desc-SMS` partial; same upstream channel's σ characterised) | N (legacy split) | / | B (`meth-NA`) | B (+19.6 / +21.7 pp + Fisher) | N |
| HA08-hrv-multiday-slope | BLOCKED-PENDING-HARDWARE (no test) | / | / | / | / | / | / | / | / |
| HA08c-sleep-stress-slope | train SUPPORTED / overall refuted | N | N | B partial (`desc-SMS` covers underlying channel) | N (legacy split) | / | B (`meth-NA`) | B (+23.0 pp) | N |
| HA10-bb-overnight-recharge | validate SUPPORTED → first validate-era precursor; v2 diagnostic CLOSE | B (`card-PVS` n=15) | N | N | N | / | B (`meth-NA`) | B (+16.2 pp + Fisher) | N |
| HA11-stress-udip | train SUPPORTED / validate refuted → overall refuted | B (`card-PVS`) | N | N (pre-MD; only retrofit Fisher) | N | / | / (per-minute U-dip; daytime) | B (+22.8 pp + Fisher) | N |
| K01-crash-depth | suggestive_underpowered | N | N | / (cross-era contrast, no block-perm; pre-MD) | N (historical split as "early/late") | / | / | B (median diff reported) | N |
| K02-crash-duration | refuted-by-bar | N | N | / | N (early/late) | / | / | B | N |
| S02b-score-lead | PENDING (no result.md) | N (cannot be evaluated; no run) | N | N | N (uses S02 algorithmic outputs; pre-MD) | / | / | / | N |
| HA-P7 | NOT-SUPPORTED (pooled LC) | B (`card-PVS` not applicable; n in result.md, n=1249 single-pool pre-reg-floor met) | N (covariate sensitivity at §4.5.4 added; pattern not audited) | **B (E[L]\* reported in result; factor-of-2 flag fired but block-perm IS the primary)** | B (pooled-LC single-pool per `lc_era_temporal_segmentation.md` Stratum 4; train/validate diagnostic only) | / | / (label-based, not nightly) | B (OR + 95% CI per cell) | B (single-pool primary per `train_validate_split_fate.md`) |
| HA-C4b (v3) | NOT-SUPPORTED (unmedicated pooled headline) | B (handoff `count_HA11_bout_redo_effective_n.py` validates n; primary cell n=10 against §5.3 bar) | N (1b.ii dropped as deliberate trade-off; documented in v3 §8 caveat 1) | B (E[L]\* reported; consistent with `permutation_null_block_length.md` default) | B (Stratum 4 + unmedicated phase per `lc_era_temporal_segmentation.md` + `citalopram_phase_stratification.md`) | / | / (per-minute count primitive) | B (z-score discrimination + p) | B (single-pool primary; train/validate descriptive sensitivity only) |
| HA-P6 (v3) | descriptive Layer 1 (no SUPPORTED bar) | N (n=29 episodes total; 3-5 fall below in some sub-cells, e.g. `bb_overnight_gain` n_eps=5) | B (v3 §4.8.4 ε rule + denom-undefined exclusion documented; counts surfaced in result table) | B (v3 4-verdict E[L]\* logic per closure #2 + cap per closure #3; `desc-RA` provides within-phase E[L]\* on 7 channels) | B (Stratum 4 pooled-LC primary; v3 closure #1 within-stratum sensitivity arm cites `intervention_effects_descriptive.md`) | / | B (`meth-NA`; sleep-derived channels in scope use `stress_mean_sleep` etc.) | B (per-day median z + bootstrap CI95) | B (single-pool primary; no train/validate split used) |
| HA-C4 (v2) | REJECTED (triad 0.0/3.0) | B (post-dry-run sample-size routing per §5.3 INCONCLUSIVE-aware; cell counts in result table) | N (chain-T+1 exclusion documented but missingness pattern not audited descriptively) | B partial (E[L]=7 inherited; `desc-SMS` characterises Ch1+Ch3's upstream stress channel; Ch2 `stress_high_duration_min` not backstopped) | B (Stratum 4 + unmedicated phase per `lc_era_temporal_segmentation.md`) | / | / (3 daytime stress channels) | B (Mann-Whitney + Cliff's δ + p) | B (single-pool primary; train/validate per channel × era contingency) |
| HA-C3 (v2) | LOCKED 2026-06-23; no result yet | B (`desc-SMS` provides n on `all_day_stress_avg`'s sister channel + v1 partial pool n=581 in §8 caveat-class; B4 absorber pre-committed) | B (v2 §7.3 halt-option-A pre-commit; `desc-SMS` characterises related channel) | B (`desc-SMS` characterised; `meth-CDR` confirms +0.57/mg dose-response on `all_day_stress_avg`) | B (Stratum 4 + unmedicated phase headline per `lc_era_temporal_segmentation.md`) | / | / | B (Jonckheere-Terpstra + S contrast + spline) | B (single-pool primary; §5.A unmedicated headline + §5.B dose-adjusted cross-phase sensitivity) |
| HA-C3p | LOCKED 2026-06-23; no result yet | B (n=1351 full Stratum 4 documented at §4.1; quintile bins ~270/bin > floor) | B (`desc-SMS` AND `desc-RA` characterise underlying channel) | B (`desc-SMS` direct; E[L]=7 inherited + `meth-PSA` collapsibility) | B (full Stratum 4 single pool per `lc_era_temporal_segmentation.md`; `meth-PSA` honored) | / | / | B (S contrast + spline + JT) | B (single-pool primary; §5.A unmedicated headline + §5.B dose-adjusted sensitivity) |
| HA-C4c | LOCKED 2026-06-23; no result yet | B (parent MD `meth-BLR` documents bout-level n; HA11-bout-redo §4.5 pins effective n=70; `desc-BOUT` provides per-feature recalibration confirming 0/7 CONFIRMED → cross-phase pool permitted) | B (`meth-BLR` §3 documents bout-detection rule; `desc-BOUT` characterises feature distributions) | B (`lc_era_temporal_segmentation.md` Stratum 4 + cross-phase pooled per `meth-PSA` + `lc_recovery_phase_axis.md` 4b+5 layering documented) | / | / (bout-level, not nightly; daytime stress trace) | B (Mann-Whitney + Cliff's δ + block-perm p; §4.10 crash-drop sensitivity) | B (single-pool primary; unmedicated-only sensitivity arm preserves comparability with HA11-bout-redo) |
| HA11-bout-redo | PARTIAL (2 of 3 bars met; framework-validity gate) | B (r2 pinned effective n=70 via `scripts/count_HA11_bout_redo_effective_n.py`; > §4.9 walk-forward gate of 30) | B (r2 σ-inheritance check documented; low-variability skip rate reported per §10.3) | B (E[L]=7 inherited per `permutation_null_block_length.md`; `desc-BOUT` characterises per-bout feature distributions on the same operand) | B (Stratum 4 + unmedicated + train-era per `lc_era_temporal_segmentation.md`; calm-day reference dates honored) | / | / (bout-level daytime) | B (+20.26 pp discrimination + p) | B (HA11 v1's train-era reference frame is being reproduced; framework-validity gate, not single-pool primary question) |

---

## 3. Gap list — descriptive backstops that don't yet exist

Grouped by HA. Effort estimate (S/M/L): S ≤ 2h, M = 3-8h, L > 8h. "Blocks Stage I" means the §6.1 conflict rule routes the verdict to DOWNGRADED-INCONCLUSIVE-PROVISIONAL until closed; "narrows confidence" means Stage I can run but with caveat.

### Gap-list rows for the older H/HA01-11 family (pre-2026-06-13 verdicts)

The H/HA01-11 corpus shares one structural feature: every test was drafted *before* the descriptive programme existed. As a result, the same backstop gaps repeat across most HAs in this family. Rather than enumerating identical rows 20 times, the shared gaps are stated once with the HAs they apply to, then HA-specific gaps are stated separately.

**Shared gap 1 — per-channel ACF / E[L]\* never run on the pre-MD verdicts** (assumption A3). Affects: H01, H02, H02b, H02d, H03, H03b, H04, HA01b-diag, HA01c, HA06, HA06b, HA10, HA11. The descriptive artefact that would close this: per-channel ACF + E[L]\* + factor-of-2-flag run on the channel each test uses, on Stratum 4 days, per the `permutation_null_block_length.md` operational consequences §2. Already done for `stress_mean_sleep` (`desc-SMS`) and `stress_low_motion_min_count_S60_Mlow` (`desc-SLM`); not yet done for `resting_hr`, `daily mean stress`, `max_spike_minutes`, `body_battery_*`, `sleep_efficiency`, `morning_bb_peak`, `effective_exertion_rank`, `u_dip_count`. **Effort**: S per channel × ~8 channels = M total. **Blocks Stage I** on these HAs because the verdicts run on a permutation null whose block-length validity is not backstopped.

**Shared gap 2 — historical train/validate split not re-anchored** (assumption A8 and A4). Affects: H01, H02, H02b, H02d, H03, H03b, H04, HA01b-diag, HA01c, HA06, HA06b, HA07c, HA07d, HA08c, HA10, HA11. The descriptive artefact that would close this: the queued historical-pre-reg re-run side-by-side table per `train_validate_split_fate.md` §5.7 (locked verdict vs verdict under MD2+MD3 framework, with divergence flag + brief note on driver). Not a re-lock; a descriptive cross-check. **Effort**: M (one script over locked result-data.json files; the recipe is binding per the MD). **Narrows confidence** rather than blocking Stage I — verdicts stay; Stage I just cites the new framework when describing them.

**Shared gap 3 — per-cell missingness pattern audit** (assumption A2). Affects: all H/HA01-11. The descriptive artefact that would close this: per-channel missingness rate × era × phase, MCAR/MAR diagnostic (e.g. Little's test or equivalent + descriptive of NaN-block lengths). Not a re-test, a missingness-rate table per channel. **Effort**: S per channel; M total. **Narrows confidence** on each Stage I (does not block).

### Per-HA gaps beyond the shared three

**H03b** (INCONCLUSIVE × 12). Gap: the data does not exist at the gated resolution (n_clean ≥ 10 on per-minute BB recharge channels). The descriptive backstop that would close this would be "we can compute the per-minute primitive on enough days" — but the test ran and surfaced that we cannot. Per §6.1 conflict rule: routed to **structurally untestable as currently specified**. **Effort**: N/A; remediation is pre-reg revision, not descriptive work.

**S02b** (PENDING). Gap: no result.md; the spec pre-commits two lag values from S02's algorithm (`+149` for avg-stress, `+100` for max-spike). The S02 algorithm itself is archived (`_archive/S02-score-trajectory/`) and has not been refreshed under the descriptive programme; the lag values it produced are not descriptively backstopped on the current corpus. **Effort**: L (S02 refresh is a Strand-B trajectory analysis; `desc-RA` partially covers it but not the score-lead algorithm). **Blocks Stage I** on S02b because the lag values it tests are unverified inputs.

**H05** (spec-induced trivial). Gap: not a descriptive gap; the operationalisation itself produced a trivial distribution. Per §6.1, the conflict here is "the verdict cannot be built on" — not "the assumption is unbacked." Listed in §6 (structurally untestable) for completeness; Stage I cannot meaningfully proceed regardless of descriptive work.

**HA07** + **HA08** (BLOCKED-PENDING-HARDWARE). Gap: no test ran; no verdict to backstop. No gap-list entry, but note these in the synthesis-structure map as "blocked, not refuted."

**HA-P6 v3**: assumption A1 (sample size) is NOT BACKSTOPPED on `bb_overnight_gain` (n_eps = 5 of 29) and on a few other per-channel sub-cells where the n_w/baseline column drops below 20. The HA itself is Layer-1 descriptive (no SUPPORTED bar), so the sample-size shortfall is reported in the per-channel table rather than routed to INCONCLUSIVE. **Effort to close**: N/A by design (HA-P6 is descriptive characterisation; small-n cells are themselves a finding). **Narrows confidence** on the small-n channels' shape categorisation; does NOT block downstream Stage I because Stage I will read HA-P6 as descriptive, not as a verdict to inferentially-promote.

**HA-C4 v2**: Ch2 (`stress_high_duration_min`) is not backstopped by `desc-SMS` (which covers `stress_mean_sleep`, a different aggregation). **Effort**: S (run the Strand-A template on `stress_high_duration_min`). **Narrows confidence** on the Ch2 contribution to the triad verdict; does not block because the triad already rejected and Ch2's individual cell verdicts are reported.

**HA-P7**: A2 (missingness pattern on `crash_count_14d`) is not backstopped by a documented MCAR/MAR audit. The covariate-sensitivity arm (§4.5.4) adds `gevoelscore_lagged_mean_14d` which addresses the confound concern but does not audit missingness directly. **Effort**: S. **Narrows confidence**.

### K01 + K02 (cross-era contrast)

Both rely on the legacy "early/late" era split (2023-12-31 cutoff), inheriting the legacy split's status. No new descriptive backstop is straightforwardly applicable because the test is itself a cross-era contrast — the era split IS the predictor. Note: `train_validate_split_fate.md` explicitly preserves historical verdicts. **Effort**: N/A for closure of the legacy split question; **narrows confidence** on whether the early/late comparison is the right framing for crash-depth and crash-duration questions, but does not block.

---

## 4. HAs ready for Stage D TRUSTED

These HAs have every load-bearing assumption BACKSTOPPED; they are eligible for §11 step 5 synthesis-structure map inclusion without further descriptive work.

1. **HA-C3 v2** — bound to `desc-SMS` + `meth-CDR` (dose-response on the predictor channel) + `meth-PSA` + `lc_era_temporal_segmentation.md`. Block-permutation E[L]=7 inherited; B4-absorber pre-committed; v1 halt-option-A discipline closes the at-risk bin. (No result yet; ready *for* Stage D, then Stage I once test runs.)
2. **HA-C3p** — bound to same anchors as HA-C3 v2; full Stratum 4 single pool n=1351; quintile bins ~270/bin > floor. (No result yet; ready for Stage D + Stage I once test runs.)
3. **HA-C4c** — bound to parent MD `meth-BLR` + `desc-BOUT` (per-feature recalibration); cross-phase pooling permitted per `meth-PSA`; HA11-bout-redo framework-validity gate has cleared at PARTIAL with the calibration discount disclosed. (No result yet; ready for Stage D + Stage I once test runs.)
4. **HA11-bout-redo** — verdict PARTIAL (2 of 3 framework-validity bars met). r2 pinned effective n=70 via the explicit count script + `desc-BOUT` characterises the per-bout operand distribution.

Pattern note: these four HAs are all post-2026-06-18 Wave-5 drafts. They were written in a corpus where the descriptive programme already existed and the methodology MDs they cite were already locked. The §6.1 checklist passes because they were drafted with §6.1's checks in mind.

---

## 5. HAs requiring descriptive work before Stage I

These HAs have ≥ 1 NOT-BACKSTOPPED load-bearing assumption. For each, the **smallest set of descriptive runs that would move it to TRUSTED** is stated. The legacy train/validate-split status (A8 NOT BACKSTOPPED) is treated as a *shared* gap (see §3 Shared gap 2) that all H/HA01-11 HAs carry — closing it across the whole family with one descriptive run is the M-effort path.

1. **H01-rhr-drift** — close A3 by running the Strand-A template on `resting_hr` (S); close A2 by RHR missingness-rate table (S); A8 closes via shared-gap-2 run (M, shared).
2. **H02-stress-elevation** — close A3 on daily mean stress channel (S; substantially covered by `desc-SMS` on the sister sleep-window version but daily mean stress is a separate channel); A2 missingness audit (S); A8 shared.
3. **H02b-stress-spikes** — close A3 on `max_spike_minutes` per-day primitive (S); A2 (S); A8 shared. Note: `card-XCC` confirms H02b ≡ H02d at the per-day primitive — the descriptive overlap is already documented; only the ACF / E[L]\* + missingness pieces remain.
4. **H02d-stress-spikes-uncensored** — same as H02b; the two are descriptively the same primitive per `card-XCC`. One Strand-A run closes both.
5. **H03-sleep-efficiency** — A3 on sleep_efficiency channel (S); A2 (S); A8 shared.
6. **H04-body-battery** — A3 on `body_battery` net-drain channel (S); A2 (S); A8 shared.
7. **HA01b-per-axis-diagnostic** — A3 on `exertion_class_lagged` or its constituent axes (S); A2 (S); A8 shared.
8. **HA01c-effective-exertion-shock** — A3 on `effective_exertion_rank_lagged` (S); A2 (S); A8 shared. (The HA01c-threshold-monotonicity-diagnostic-v2 inherits.)
9. **HA06-morning-rhr-delta** — A3 on `resting_hr` delta (S; shared with H01); A2 (S); A8 shared.
10. **HA06b-rhr-zscore** — A3 inherits from H01's `resting_hr` run; A2 (S); A8 shared. (HA06b-threshold-monotonicity-diagnostic-v2 inherits.)
11. **HA07c-sleep-stress-mean-delta** — A3 already substantially backstopped via `desc-SMS` (the upstream channel's E[L]\*=12.6 is documented; HA07c uses the per-night delta, slightly different); a delta-specific ACF run would tighten (S). A2 (S; sleep_valid_flag missingness pattern). A8 shared.
12. **HA07d-sleep-stress-variability** — A3 substantially backstopped via `desc-SMS` (variability primitive descriptively characterised on the same upstream channel; HA07d uses per-night σ); a σ-primitive-specific ACF would tighten (S). A2 (S). A8 shared. (HA07d-threshold-monotonicity-diagnostic / -v2 inherit.)
13. **HA08c-sleep-stress-slope** — same family as HA07c/d; A3 substantially backstopped via `desc-SMS`; A2 (S); A8 shared.
14. **HA10-bb-overnight-recharge** — A3 on `morning_bb_peak` / `bb_overnight_gain` channels (S; partly covered by `meth/bb_overnight_gain_proxy.md`); A2 (S; coverage of BB-source from 2024-07-08); A8 shared. (HA10-threshold-monotonicity-diagnostic / -v2 inherit.)
15. **HA11-stress-udip** — A3 on `u_dip_count` per-day primitive (S; partially covered by `garmin_exploration/cards/` and HA11-bout-redo's bout-level work but not a direct ACF on the u_dip_count daily aggregate); A2 (S); A8 shared. (HA11-threshold-monotonicity-diagnostic-v2 inherits.)
16. **K01-crash-depth** — A1 (S; per-era episode counts n=14/15 are well-documented; the gap is per-era median + spread descriptive run, which is partly done in `card-PVS`); A2 (S); A3 N/A (no block-perm); A8 N/A (cross-era contrast IS the predictor).
17. **K02-crash-duration** — same as K01.
18. **HA-P6 v3** — A1 NOT BACKSTOPPED on `bb_overnight_gain` (n_eps=5); intentional per design. **Narrows confidence**, does not block Stage I.
19. **HA-P7** — A2 missingness audit on `crash_count_14d` (S). **Narrows confidence**.
20. **HA-C4 v2** — close A3 by running the Strand-A template on `stress_high_duration_min` (Ch2) (S); A2 chain-T+1 missingness audit (S). **Narrows confidence** on a REJECTED triad.
21. **HA-C4b v3** — A2 1b.ii missingness rate is already documented (22 of 709 unmedicated 1b.i-passing days = 3.1%); a formal missingness-pattern audit would tighten (S). **Narrows confidence**.

---

## 6. HAs that may be structurally untestable as currently specified

Per §6.1 conflict rule: "Descriptive cannot be produced because data does not exist → the HA is flagged for 'structurally untestable as currently specified' and routed back to pre-reg revision."

1. **H03b-bb-overnight-recharge-permin** — verdict INCONCLUSIVE × 12 because n_clean ≥ 10 was not met on any of 12 evaluation cells. The data the test needs does not exist at the gated resolution. Routed back to pre-reg revision; downstream remediation is either (a) a re-spec that lowers the gating bar OR (b) wait for more data accrual. NOT a Stage I candidate as currently specified.
2. **S02b-score-lead** — PENDING; the spec depends on lag values produced by S02's algorithmic outputs. S02 itself is archived. Without descriptive backstopping of the algorithm's lag values on the current corpus, S02b's pre-committed lags are unverified inputs. Routed back to pre-reg revision OR to a Strand-B refresh of S02's algorithm under the descriptive programme (`desc-RA` covers the broader trajectory but not the score-lead specifically). NOT a Stage I candidate as currently specified.
3. **H05-recovery-time** — spec-induced trivial verdict (the operationalisation produced a degenerate distribution). Not a descriptive gap — the spec itself is the failure mode. Routed back to pre-reg revision; NOT a Stage I candidate as currently specified.

Additional adjacent cases not strictly "structurally untestable" but functionally inert for Stage I:

- **HA07** + **HA08** — BLOCKED-PENDING-HARDWARE; the FR245 hardware does not record the HRV channel these tests require. No verdict, no Stage I work, no descriptive gap (the data simply does not exist for these signals on this hardware).

---

## 7. Notes / caveats from the stocktake process

- **Diagnostic vs HA distinction**: the seven `*-threshold-monotonicity-diagnostic*` folders and the one `HA01b-per-axis-diagnostic` carry `diagnostic.md`, not `hypothesis.md`. Per the testing playbook these are downstream rescue / re-test diagnostics bound to a parent HA's verdict, not freestanding HAs. They inherit their parent HA's row in the matrix; rowing them separately would double-count.
- **"BACKSTOPPED" via methodology MD vs descriptive artefact**: A4 (era / Stratum 4) and A8 (split fate) are predominantly backstopped by methodology MDs that document the operational consequence binding across all HAs (`lc_era_temporal_segmentation.md`, `train_validate_split_fate.md`). The §6.1 rubric does not strictly require a per-HA descriptive artefact for these — the binding MD + per-pre-reg's explicit citation of it suffices. Rows above mark older HAs N on A8 because those HAs were drafted before the split-fate MD existed (their use of the historical split is the *thing the MD has since reframed*, not a per-HA citation that survives the reframe).
- **"BACKSTOPPED" for A3 (block-length) is partial in many cells**: `desc-SMS` and `desc-SLM` characterise the underlying daily channel's ACF but several HAs use a derivative (per-night delta, per-night σ, slope over a multi-day window) whose ACF could differ from the daily-aggregate's. The matrix records this as B partial in the cell language, but a strict reading would record N until a derivative-specific ACF is run. This stocktake uses B partial liberally to keep the gap list focused on the structural gaps rather than enumerating every derivative.
- **A5 (v24 semantics) is NOT APPLICABLE for almost every HA in the corpus**: only HA-C4b v3 §8 (the pacing-behaviour confounder caveat) and the various caveats about `cat_belasting_*` / `state_symptoom_*` reference v24-derived signals, and even there they enter as descriptive companion / caveat-class, not as the test's primary predictor or outcome. No HA in the current corpus runs a primary test on a presence-conditioned signal. The systemic v24-semantics binding is honored by absence — most tests use `daily_computed` channels per `symptom_mention_asymmetry.md` taxonomy.
- **A6 (nightly attribution) is BACKSTOPPED by acceptance of `meth-NA` as the binding rule for sleep-derived columns**: the methodology MD documents that all four Garmin sources already arrive in wake-up-date convention before the consolidate stage; the build script does no date shifting. Per-HA backstops are not separately required for the convention itself; what IS required is per-HA explicit use of `sleep_valid_flag` for sleep-derived signals, which the older H03 / HA07c / HA07d / HA08c / HA10 family does honor.
- **HA-P6 v3's A1 reading is design-intentional**: HA-P6 is Layer-1 descriptive and explicitly accepts small-n cells as findings to surface, not as INCONCLUSIVE routings. The matrix marks A1 as N to honor the strict §6.1 reading ("sample size ≥ pre-registered floor"), but the practical Stage I implication is "report as descriptive shape with small-n caveat" not "DOWNGRADE-INCONCLUSIVE-PROVISIONAL." Reader judgment applies.
- **HA-C4 v2's per-cell n routing via §5.3 INCONCLUSIVE-aware bands** is the project's first design-level absorption of small-cell-n into the verdict structure. The matrix marks A1 BACKSTOPPED because the routing IS the backstop — the test was structured to absorb the cell-size failure into its verdict logic, with the sample-size cells transparently reported. This is a pattern the older HAs lack.
- **Wave-5 HAs cite descriptive backstops by construction**: the four "ready for Stage D TRUSTED" HAs (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo) were drafted with explicit "Verification log" or "Locked decisions at draft time" blocks that cross-reference the descriptive programme artefacts. This pattern did not exist in the H/HA01-11 family; the gap-list size for the older family reflects the absence of that pattern, not a finding that the older verdicts are wrong.
- **The descriptive programme has landed 3 of an open-ended Strand-A queue + 1 of Strand-B + 1 sub-MD-driven calibration**. Of the 10+ Strand-A channel candidates surfaced in `descriptive/README.md §3.4`, only `stress_mean_sleep` + `stress_low_motion_min_count_S60_Mlow` are landed; `all_day_stress_avg` + `bb_lowest` + `bb_overnight_gain` + `resting_hr` + `stress_stdev_sleep` + `exertion_class` + `push_burden_7d` + `gevoelscore` remain on the deferred queue. The §3 Shared gap 1 enumeration above maps roughly 1:1 to these deferred channels.
- **No HA's UNCLEAR cells**: every assumption-cell was confidently mapped to B / N / / under the rubric. The bookkeeping that could have triggered UNCLEAR (does HA07c's delta-of-channel require a delta-specific ACF that's structurally different from the upstream channel's, or does upstream-channel ACF backstopping suffice?) was resolved by recording B partial in cell language and rolling those concerns into the §3 shared-gap-1 description rather than flagging individual cells UNCLEAR.

---

## 8. Where this stocktake routes next (per the plan §11)

This stocktake is step 3. It feeds:

- **§11 step 4** — `research_line_limitations.md` drafting: the per-HA gap list informs the "single-subject reach" + "device generations" + "presence-conditioned data layer" rows by surfacing exactly where each systemic limitation hits a verdict.
- **§11 step 5** — `synthesis_structure_map.md`: the four HAs in §4 above are eligible for clustering immediately; the 24 HAs in §5 require descriptive work first OR get flagged in the map as "DOWNGRADED-INCONCLUSIVE-PROVISIONAL pending §3 closures" per the plan §3.6 cluster-membership-discipline; the 3 HAs in §6 are flagged "structurally untestable as currently specified" and excluded from the map's clusters.
- **§3.5 open_inputs queue** — each gap-list row in §3 above becomes an open_inputs entry once the §11 step 6.1 `descriptive_precondition_audit.md` guide is drafted and the skill spins up per-HA Stage D runs.

No edits to any pre-reg, result.md, methodology MD, or descriptive artefact were made by this stocktake. Read-only enumeration per the §6.1 rubric.

---

## 9. User decisions on stocktake findings (2026-06-23 session)

The stocktake surfaced four decision points that the user resolved in-session before proceeding to §11 step 4. These decisions are recorded here for traceability and feed §11 step 5 (synthesis-structure map).

### 9.1 Fate of the 3 structurally-untestable HAs (Decision 1)

- **H03b** — **RETIRED**. Failure mode: INCONCLUSIVE × 12 cells by data availability at the gated resolution. The data isn't there at the resolution the test requires; "revising" would mean a different hypothesis, not a salvage. Archive with a documented "data-resolution limit" note in the registry.
- **S02b** — **SHELVED (blocked-by-S02)**. Failure mode: depends on unverified S02 algorithmic-lag outputs; never ran. Revisit if S02 ever produces verified outputs; until then it is a dependency-blocked entry, not a retired one.
- **H05** — **RETIRED + reserve successor slot**. Failure mode: spec-induced trivial distribution (the recovery target was structurally always met). Revising would be writing a new HA. The synthesis-structure map (§11 step 5) reserves an `HA-H05-successor` slot to be drafted via the project's standard pre-reg discipline when a sound spec is identified.

### 9.2 Strategy for the 24 NOT-BACKSTOPPED HAs (Decision 2)

**Defer-and-grow** chosen. Proceed with the 4 ready HAs (§4 above) as the initial scope. The 24 NOT-BACKSTOPPED HAs become Stage D backlog that interleaves naturally with §11 step 11 rollout — as a NOT-BACKSTOPPED HA's descriptive gap closes (via Strand-A channel extensions), it becomes eligible for Stage I and joins the rollout. This optimises for shortest path to first translation output and avoids front-loading the full Strand-A backlog.

### 9.3 Synthesis-structure map seed (Decision 3)

**Seed with 4 ready HAs** (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo) per the defer-and-grow strategy in 9.2. The §11 step 5 synthesis-structure map starts with these and grows via the §3.6 map-revision discipline as backstops land.

### 9.4 Fate of HA07 + HA08 (hardware-blocked) (Decision 4)

**Adapt to HRV-proxy via stress**. The `hrv_proxy_via_stress.md` methodology MD already specifies the proxy operationalisation, and the corpus has the data. Archive the originals (HA07, HA08) with a "hardware-blocked, superseded by proxy successors" note in the registry. Pre-reg `HA07-proxy` and `HA08-proxy` successors via the project's standard pre-reg discipline; reserve slots in the synthesis-structure map.

### 9.5 Consequent housekeeping work

The decisions above imply registry and pre-reg-revision work that is not part of the results-analysis layer itself but follows from it:

- Mark H03b RETIRED, S02b SHELVED-BLOCKED-BY-S02, H05 RETIRED, HA07 SUPERSEDED, HA08 SUPERSEDED in the HA registry.
- Reserve `HA-H05-successor`, `HA07-proxy`, `HA08-proxy` slots in the synthesis-structure map (§11 step 5) and in the registry.
- The four ready HAs (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo) become the initial scope for §11 steps 5-11.

These housekeeping items belong to project maintenance, not the stocktake itself. The stocktake's record is the routing; the actual registry edits happen in producer-mode sessions per the normal lock process.
