# Q24 post-heavy-day trajectory descriptive audit — Stage D Wave 1

**Status**: **LOCKED r2 2026-07-15** post fresh-session `/research-review` absorption (verdict **PASS with caveats** at [`../../../reviews/Q24-post-heavy-trajectory-2026-07-15.md`](../../../reviews/Q24-post-heavy-trajectory-2026-07-15.md)). Six substantive absorbs applied (see §12 lock log). Producer-mode artefact per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs) + [§2.1 descriptive-before-inference](../../../CONVENTIONS.md#21-descriptive-before-inference). Any downstream Stage H per-HA pre-registration draws on §5 branch verdicts + §6.3 sign-consistent survivor list here.

**Wave 1 scope**: combined intensity trigger (heavy ∪ very_heavy) × strict-clean overlap only × both compensatory-success (primary) and compensatory-failure (sub-arm) pools per [Q24 MD §3.5](../../../methodology/post_heavy_day_compensatory_rest.md#35-crash-adjacency-handling-compensatory-success-vs-compensatory-failure-split); all three windows (+3d, +5d, +10d); ~20 outcomes per [Q24 MD §6](../../../methodology/post_heavy_day_compensatory_rest.md#6-outcome-operand-families); raw + trajectory-detrended arms side-by-side per [Q24 MD §7.11](../../../methodology/post_heavy_day_compensatory_rest.md#711-trajectory-detrend-sensitivity-per-conventions-37-envelope-drift-confound); B=10,000 bootstrap per [Q24 MD §7.10](../../../methodology/post_heavy_day_compensatory_rest.md#710-null-hypothesis-inference-machinery-bootstrap--permutation--multiplicity); §8 four-branch decision-tree verdicts per autonomic channel × window × pool. Intensity-stratified arms + inclusive-overlap arm + Stage H pre-reg drafting **deferred to Wave 2**.

**Reproducibility**: [`scripts/audit.py`](scripts/audit.py) + [`scripts/detrend.py`](scripts/detrend.py) idempotent against `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. `RANDOM_SEED = 20260715`; bootstrap draws reproducible. Wall-clock: **~163s** on the reference environment.

---

## 1. Authorship

Drafted 2026-07-15 by Claude (Opus 4.7) in producer-mode subagent under user delegation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem. Faithful execution of [`post_heavy_day_compensatory_rest.md`](../../../methodology/post_heavy_day_compensatory_rest.md) LOCKED r1 2026-07-15 (commit `58b7723`); no design deviation from Q24 MD's locked definitions. Ambiguities encountered during execution are surfaced in §10 for orchestrator review.

**Verification log**:
- Read Q24 MD LOCKED r1 (`58b7723`) — §1-§14 in full; every operand + window + overlap policy + summary statistic + decision-tree branch + detrend rule traced to specific MD sections.
- Read [`sleep_metrics.md`](../../../methodology/sleep_metrics.md) r1 — sleep-operand catalogue; §6.2 sleep-family formulas + coverage inherited.
- Read [`intervention_effects_descriptive.md`](../../../methodology/intervention_effects_descriptive.md) — `linear_detrend_on_pre` helper (§6 script) adapted to per-day trajectory in [`detrend.py`](scripts/detrend.py).
- Read [`Q24-precursor-heavy-day-structure/audit.md`](../Q24-precursor-heavy-day-structure/audit.md) LOCKED r1 — Stage -1 structural findings; every Wave 1 pool count reproduces the audit's clean-sample figures.
- Read [`methodology-post_heavy_day_compensatory_rest-2026-07-15.md`](../../../reviews/methodology-post_heavy_day_compensatory_rest-2026-07-15.md) — the reviewer report that shaped Q24 MD §7.10, §7.11, and §10.8 additions.
- Read [`build_unified_dataset.py`](../../../pipeline/03_consolidate/build_unified_dataset.py) coverage figures — verified 26 required columns present at Q24-MD-consistent LC-era coverage.

No modification of `per_day_master.csv` or any file outside `Q24-post-heavy-trajectory/`. No commit, no dispatch of further subagents.

---

## 2. Frame + method summary

**Stratum** (Q24 MD §2.1): LC-era only (`lc_phase == 'lc'`, `date >= 2022-04-04`). N = **1524 days** (matches Q24 MD §2.2 + Stage -1 audit §1).

**Heavy-day definition** (Q24 MD §2.2, inherited from HA-C4c): `exertion_class_lagged_lcera ∈ {heavy, very_heavy}`. LC-era: **532 heavy days** (34.9% of LC-era, 256 very_heavy + 276 heavy-only + 70 missing/gap days).

**Unit of analysis** (Q24 MD §3.1): **episode-end (gap=0 contiguous)**. Total episode-ends on LC-era stratum: **314** (matches Stage -1 audit §4 exactly).

**Intensity trigger, Wave 1**: **combined only** (Q24 MD §2.2 primary). Intensity-stratified arms (very_heavy_only, heavy_only per Q24 MD §9) deferred to Wave 2.

**Overlap policy, Wave 1**: **strict-clean only** (Q24 MD §5.2). An episode-end at D qualifies if no other heavy day falls in `[D+1, D+w]`. Inclusive policy deferred to Wave 2.

**Windows** (Q24 MD §5.1): **+3d + +5d primary; +10d extended** (all three read in Wave 1). +14d dropped per Q24 MD §5.1.

**Comparator** (Q24 MD §4.1): matched-ordinary day = (a) not a heavy day, (b) no heavy day in `[D_ord, D_ord + w]`, (c) no crash day in `[D_ord, D_ord + w]`, (d) valid outcome data at every d+k in `[D_ord + 1, D_ord + w]`. **Per-outcome recomputed** per Q24 MD §4.2.

**Pool split** (Q24 MD §3.5): among strict-clean episode-ends, split into:
- **compensatory-success (primary)**: no crash in `[D+1, D+w]`.
- **compensatory-failure (sub-arm)**: crash in `[D+1, D+w]`.

Both reported side-by-side; no pre-registered inferential test compares the two at Stage D (Q24 MD §3.5).

**Trajectory summary statistics** (Q24 MD §7.1-§7.9): per (outcome, window, pool, raw/detrended) cell, nine statistics — per-day mean + CI, mean-trajectory difference vector Δ(k), AUC, slope, peak-location k*, peak magnitude, RTBT (censored at w+1), below-baseline day count (direction-signed per §7.7), trajectory variability, first-crossing day.

**Trajectory-detrend companion** (Q24 MD §7.11): per-episode 30d pre-window linear extrapolation; comparator arm uses each comparator day's own pre-window (paired-detrend semantics); episodes with <15 valid pre-window points flagged NaN and dropped from the detrended arm for that outcome. Raw + detrended reported side-by-side.

**Bootstrap** (Q24 MD §7.10): B = 10,000 per-episode resampling, block length = 1 (strict-clean episode-ends approximately independent), percentile-CI [2.5, 97.5]. No permutation nulls at Stage D. Comparator arm resampled per-day at the same B.

**Multiplicity** (Q24 MD §7.10): descriptive-only at Stage D; no correction applied. Per-cell verdicts (§5 below) NOT corrected across the 5 channels × 3 windows × 2 pools = 30 cells. Per-channel branch reporting per Q24 MD §8.3 explicitly rejects compression.

**§8 decision-tree operationalisation** (Q24 MD §8.1): peak-based decay per channel per window per pool: **`|Δ(w)| / |Δ(k*)| < 0.5`**, evaluated on **raw** delta trajectories (detrend companion reported for fragility flag per §7.11 escalation rule but not the primary branch input). Autonomic channels (5): `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`, `hr_median_waking`, `sleep_hr_avg_spo2`. Subjective channel: `gevoelscore`. Branch assignment per Q24 MD §8.2 (BOTH decay / ONLY autonomic decays / ONLY subjective decays / NEITHER decays).

---

## 3. Pool sample sizes

Per [`output/compensatory_pool_sizes.csv`](output/compensatory_pool_sizes.csv):

| window | compensatory-success (primary) | compensatory-failure (sub-arm) | strict-clean total |
|---:|---:|---:|---:|
| **+3d** | **109** | **16** | 125 |
| **+5d** | **43** | **9** | 52 |
| **+10d** | **11** | **1** | 12 |

**Reproduction check**: strict-clean totals per window (125 / 52 / 12) reproduce Stage -1 audit §5 combined `Post-window CLEAN` cell counts **byte-identically** — the compensatory-success + -failure split partitions the same episode-ends the Stage -1 audit surfaced.

**Sub-arm sample-size discipline per Q24 MD §3.5**: any window where the compensatory-failure pool falls below n=10 is flagged as **narrative-only sub-arm** (no bootstrap-CI trajectory report). This applies at **+10d (n=1)** absolutely; the single-episode trajectory is reported in the outputs but no branch verdict is defensible. **+5d (n=9)** is on the borderline — bootstrap CIs are computed but interpreted with the wide-CI caveat. **+3d (n=16)** is comfortably above the threshold.

**Crash-in-window rate on strict-clean episode-ends**: 16/125 = **12.8%** at +3d; 9/52 = **17.3%** at +5d; 1/12 = **8.3%** at +10d. The overall LC-era crash rate is 103/1524 = 6.8% (Stage -1 audit §1) — the trigger-day-following crash rate is roughly **2×** the corpus baseline at the primary windows. Descriptively-substantive observation for the Q24.5 unfalsifiable counterfactual anchor; interpretation deferred (see §7).

---

## 4. Trajectory summary tables

Structured summary of the top-line trajectory findings per outcome group. Full 236-row table lives in [`output/trajectory_summary.csv`](output/trajectory_summary.csv); per-day mean + CI + delta at every k in [`output/per_day_trajectories.csv`](output/per_day_trajectories.csv). All values reported here are **raw** unless the `[det]` marker is present.

**Reading convention**: AUC signed (post-trigger cumulative delta vs matched-ordinary); CI is bootstrap 95% percentile per Q24 MD §7.10; `k*` = peak-location; `p_mag` = peak magnitude; `fcd` = first-crossing day (`w+1` if censored); n_t = trigger-arm episode count; n_c = comparator-arm day count (per-outcome per Q24 MD §4.2). **Bold AUC** = bootstrap 95% CI excludes zero (descriptive marker; NOT a p-value verdict per Q24 MD §7.10 no-inferential-tests-at-Stage-D).

### 4.1 Activity outcomes (Q24 MD §6.1) — compensatory-success pool

Direction pre-commit per Q24 MD §7.7: activity outcomes physiologically-meaningful direction is **negative** (fewer than matched-ordinary = compensatory response).

| outcome | window | n_t | n_c | AUC | AUC 95% CI | k\* | p_mag | fcd |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| total_steps | +3d | 109 | 308 | **−1356** | [−2054, −665] | 3 | 620 | 1 |
| total_steps | +5d | 43 | 189 | **−3865** | [−5455, −2290] | 5 | 1010 | 1 |
| total_steps | +10d | 11 | 104 | **−15316** | [−20523, −9955] | 10 | 2124 | 1 |
| effective_exertion_min | +3d | 109 | 327 | **+3.55** | [+0.25, +7.17] | 2 | 1.87 | 2 |
| effective_exertion_min | +5d | 43 | 204 | +0.69 | [−4.62, +6.77] | 2 | 1.62 | 6 |
| effective_exertion_min | +10d | 11 | 105 | **−23.08** | [−30.94, −14.70] | 10 | 3.72 | 1 |
| vigorous_min | +3d | 109 | 310 | **−1.72** | [−2.28, −1.21] | 2 | 0.68 | 1 |
| vigorous_min | +5d | 43 | 191 | **−4.26** | [−5.53, −3.07] | 3 | 0.98 | 1 |
| vigorous_min | +10d | 11 | 104 | **−14.51** | [−17.95, −11.24] | 8 | 1.87 | 1 |
| active_min | +3d | 109 | 310 | **−15.27** | [−29.76, −0.97] | 2 | 8.35 | 1 |
| active_min | +5d | 43 | 191 | **−47.26** | [−75.28, −19.33] | 3 | 12.34 | 1 |
| active_min | +10d | 11 | 104 | **−228.95** | [−327.50, −126.13] | 10 | 34.60 | 1 |

**Read**: activity-side compensation is unambiguous at strict-clean episode-ends. `total_steps`, `vigorous_min`, `active_min` all show negative-direction AUC with tight CIs at every window, peak-magnitude scaling by window size, and first-crossing day of 1 (immediate divergence from matched-ordinary). The `effective_exertion_min` composite tells a **more nuanced story**: at +3d and +5d the AUC is near-zero or slightly positive (peak k* on the sign-inverted side at k=2), which is a definitional-pair signal (§6.1 discipline) — the composite axis catches a different signal than the raw activity minute-counts. **All four channels are trajectory-confound-suspect at +3d/+5d/+10d under §7.11** (see §6 below); the compensatory pattern is real but its magnitude is amplified by envelope drift.

### 4.2 Sleep architecture (Q24 MD §6.2 Family A) — compensatory-success pool

Direction pre-commits: `sleep_duration_min` + `sleep_deep_min` + `sleep_rem_min` = positive (compensatory rebound); `sleep_awake_min` = positive (cost); `sleep_efficiency_tib` = negative (cost).

| outcome | window | n_t | n_c | AUC | AUC 95% CI | k\* | p_mag |
|---|---:|---:|---:|---:|---|---:|---:|
| sleep_duration_min | +3d | 109 | 296 | **+74.15** | [+40.11, +107.45] | 2 | 32.74 |
| sleep_duration_min | +5d | 43 | 178 | **+180.0** | [+107.6, +252.8] | 4 | 41.11 |
| sleep_duration_min | +10d | 11 | 84 | **+279.1** | [+72.9, +464.2] | 5 | 45.86 |
| sleep_deep_min | +3d | 109 | 299 | **−23.85** | [−42.87, −4.77] | 2 | 12.36 |
| sleep_deep_min | +5d | 43 | 187 | +11.72 | [−16.10, +40.14] | 5 | 12.98 |
| sleep_deep_min | +10d | 11 | 104 | **+308.3** | [+149.3, +522.1] | 10 | 44.87 |
| sleep_rem_min | +3d | 109 | 283 | +12.90 | [−11.42, +38.44] | 1 | 12.02 |
| sleep_rem_min | +5d | 43 | 174 | −25.20 | [−87.67, +34.65] | 5 | 12.61 |
| sleep_rem_min | +10d | 11 | 91 | **−139.6** | [−240.9, −39.3] | 6 | 20.85 |
| sleep_awake_min | +3d | 109 | 299 | +1.62 | [−1.87, +5.34] | 1 | 1.89 |
| sleep_awake_min | +5d | 43 | 187 | +2.79 | [−4.68, +9.99] | 4 | 1.85 |
| sleep_awake_min | +10d | 11 | 104 | **−11.24** | [−21.34, −0.90] | 10 | 2.87 |
| sleep_efficiency_tib | +3d | 109 | 292 | −0.001 | [−0.006, +0.005] | 3 | 0.005 |
| sleep_efficiency_tib | +5d | 43 | 177 | −0.001 | [−0.011, +0.010] | 1 | 0.004 |
| sleep_efficiency_tib | +10d | 11 | 84 | +0.016 | [−0.010, +0.041] | 10 | 0.007 |
| sleep_light_min | +3d | 109 | 299 | **+89.19** | [+54.44, +123.37] | 2 | 33.63 |

**Read**: sleep duration compensation is the cleanest signal of the audit — `sleep_duration_min` AUC positive with CI excluding zero at all three windows (+74 / +180 / +279 min cumulative). `sleep_light_min` accounts for most of the duration increase at +3d (AUC +89 min). `sleep_deep_min` inverts sign between +3d (−24 min, CI excludes zero) and +10d (+308 min, CI excludes zero) — a genuine within-window direction reversal, though the +10d n=11 sits at the extended-window threshold. `sleep_rem_min` and `sleep_awake_min` are flat at primary windows and drift at +10d. `sleep_efficiency_tib` is near-zero at every window — the extra sleep is not more efficient, just longer. **All positive sleep_duration_min and sleep_light_min signals are trajectory-confound-suspect at +3d/+5d under §7.11**; the duration-rebound direction survives detrending at zero-magnitude (see §6).

### 4.3 Sleep autonomic + day autonomic (Q24 MD §6.2 Family D + day-scoped) — compensatory-success pool

Direction pre-commits: `stress_mean_sleep` + `all_day_stress_avg` + `hr_median_waking` + `sleep_hr_avg_spo2` = positive (cost); `bb_lowest` = negative (cost).

| outcome | window | n_t | n_c | AUC | AUC 95% CI | k\* | p_mag | fcd |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| stress_mean_sleep | +3d | 109 | 296 | −0.74 | [−3.18, +1.75] | 2 | 1.07 | 4 |
| stress_mean_sleep | +5d | 43 | 178 | −4.16 | [−9.84, +1.92] | 2 | 2.29 | 2 |
| stress_mean_sleep | +10d | 11 | 84 | +14.90 | [−28.85, +50.99] | 9 | 4.06 | 11 |
| all_day_stress_avg | +3d | 109 | 310 | −1.06 | [−3.74, +1.56] | 1 | 0.81 | 4 |
| all_day_stress_avg | +5d | 43 | 191 | **−6.68** | [−12.74, −0.13] | 1 | 1.84 | 6 |
| all_day_stress_avg | +10d | 11 | 104 | **−33.14** | [−54.75, −8.54] | 10 | 5.35 | 6 |
| bb_lowest | +3d | 109 | 310 | −0.02 | [−4.62, +4.62] | 1 | 1.82 | 4 |
| bb_lowest | +5d | 43 | 191 | **+13.60** | [+2.76, +24.03] | 5 | 4.95 | 2 |
| bb_lowest | +10d | 11 | 104 | **+76.00** | [+35.09, +112.18] | 10 | 12.20 | 1 |
| hr_median_waking | +3d | 109 | 308 | **+3.51** | [+1.36, +5.66] | 2 | 1.64 | 2 |
| hr_median_waking | +5d | 43 | 191 | +2.59 | [−2.00, +7.48] | 4 | 1.07 | 6 |
| hr_median_waking | +10d | 11 | 104 | +5.83 | [−7.15, +18.20] | 8 | 1.71 | 11 |
| sleep_hr_avg_spo2 | +3d | 109 | 266 | **+2.30** | [+0.26, +4.34] | 1 | 1.17 | 1 |
| sleep_hr_avg_spo2 | +5d | 43 | 152 | +2.53 | [−2.27, +7.42] | 1 | 0.88 | 6 |
| sleep_hr_avg_spo2 | +10d | 11 | 61 | −6.62 | [−22.90, +9.09] | 10 | 2.60 | 11 |

**Read**: primary autonomic + day autonomic panel is **mixed** on the compensatory-success pool.
- `hr_median_waking` and `sleep_hr_avg_spo2` fire in the pre-committed +1 direction at +3d (both AUC CI excludes zero) — elevated overnight/waking HR at day-after-heavy. HR persistence directly aligns with Radin 2024 nightly-HR persistence per Q24 MD §6.2 anchor.
- `stress_mean_sleep` and `all_day_stress_avg` **invert sign** vs the pre-committed direction: the day-after-heavy autonomic-stress trajectory is *lower* than matched-ordinary (with `all_day_stress_avg` AUC CI excluding zero on the negative side at +5d and +10d). Per Q24 MD §7.7, this is a sign-inversion finding in its own right, not a null.
- `bb_lowest` flips direction across the window ladder: near-zero at +3d, **positive-signed** (higher BB reserve than matched-ordinary) at +5d and +10d with CIs excluding zero. Since the pre-commit direction was negative-signed (cost of heavy load = depressed BB), this is another sign-inversion.

Two candidate readings for the sign-inversion pattern (both descriptive-only per CONVENTIONS §4.2 caveat-class):
1. **Compensatory-behaviour-visible-in-autonomic-metrics**: the compensatory-success pool = episode-ends that successfully avoided a crash in-window; the participant's post-heavy pacing behaviour (which is *not* observed here but is implicit in the pool definition) may have driven `stress_mean_sleep` + `all_day_stress_avg` *below* matched-ordinary — a self-selected rest response.
2. **Trajectory-confound**: the raw autonomic signals are dominated by envelope drift; the sign-inversion may reverse under detrending. Checked: `all_day_stress_avg` at +5d is trajectory-confound-suspect (raw CI excludes zero, detrended CI does not; see §6). `bb_lowest` at +5d and +10d also detrend-fragile.

### 4.4 Sensitivity operands (Q24 MD §6.2.3) — compensatory-success pool

| outcome | window | n_t | n_c | AUC | AUC 95% CI | k\* | p_mag |
|---|---:|---:|---:|---:|---|---:|---:|
| sleep_efficiency_staged | +3d | 109 | 280 | +0.005 | [−0.001, +0.010] | 3 | 0.005 |
| sleep_efficiency_staged | +5d | 43 | 169 | +0.011 | [−0.003, +0.024] | 4 | 0.005 |
| sleep_efficiency_staged | +10d | 11 | 81 | +0.032 | [+0.009, +0.056] | 10 | 0.006 |
| spo2_avg_sleep | +3d | 109 | 198 | +0.10 | [−0.30, +0.51] | 3 | 0.24 |
| spo2_avg_sleep | +5d | 43 | 87 | −0.11 | [−1.05, +0.75] | 3 | 0.42 |
| spo2_avg_sleep | +10d | 11 | 27 | **−8.06** | [−12.48, −3.52] | 10 | 1.87 |
| asleep_stress_max_uds | +3d | 109 | 303 | +1.83 | [−4.87, +8.68] | 3 | 2.98 |
| asleep_stress_max_uds | +5d | 43 | 185 | **−19.86** | [−33.92, −5.93] | 3 | 6.09 |
| asleep_stress_max_uds | +10d | 11 | 94 | **−66.45** | [−109.26, −24.58] | 10 | 9.06 |

**Read**: `asleep_stress_max_uds` (arousal-peak proxy) mirrors the `stress_mean_sleep` sign-inversion pattern at +5d and +10d — post-heavy nights show *lower* peak arousal than matched-ordinary, with CIs excluding zero. This is convergence-across-two-independent-arousal-channels (mean-of-sleep-window from FIT + max-of-sleep-window from UDS aggregator) — descriptively strengthens reading 1 above (compensatory-behaviour-visible-in-autonomic). Also: `spo2_avg_sleep` shows a substantive negative-direction AUC at +10d only, but n=11 sits at the extended-window bound.

### 4.5 `bb_overnight_gain` at +3d only (Q24 MD §6.2.1)

| outcome | window | pool | n_t | n_c | AUC | AUC 95% CI |
|---|---:|---|---:|---:|---:|---|
| bb_overnight_gain | +3d | compensatory_success | 109 (46 valid) | 147 | −0.42 | [−9.49, +8.47] |
| bb_overnight_gain | +3d | compensatory_failure | 16 (0 valid) | 147 | — | — |
| bb_overnight_gain_frac | +3d | compensatory_success | 109 (46 valid) | 147 | −0.11 | [−0.26, +0.03] |
| bb_overnight_gain_frac | +3d | compensatory_failure | 16 (0 valid) | 147 | — | — |

**Read**: at 38.9% LC-era coverage, only 46 of 109 compensatory-success episode-ends have valid `bb_overnight_gain` at every d+k in +3d; **zero of 16 compensatory-failure episodes have valid data** (data-availability drops to zero on the failure sub-arm at the +3d post-window intersection). The success-pool AUC is small-magnitude and CI-crossing-zero at +3d; the ceiling-corrected `bb_overnight_gain_frac` variant shows a slightly stronger negative direction (AUC −0.11 CI [−0.26, +0.03]) but still consistent with zero at 95%. **Flagged descriptive-only-with-CI per Q24 MD §6.2.1 sparse-availability discipline**.

### 4.6 Subjective (Q24 MD §6.3)

Direction pre-commit per Q24 MD §7.7: `gevoelscore` cost direction is **negative** (worse than matched-ordinary).

| pool | window | n_t | n_c | AUC | AUC 95% CI | k\* | p_mag | fcd |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| compensatory-success | +3d | 109 | 242 | **−0.47** | [−0.83, −0.12] | 2 | 0.22 | 1 |
| compensatory-success | +5d | 43 | 128 | −0.78 | [−1.57, +0.04] | 1 | 0.38 | 1 |
| compensatory-success | +10d | 11 | 42 | +0.16 | [−1.72, +1.98] | 7 | 0.37 | 11 |
| compensatory-failure | +3d | 16 | 242 | **−3.77** | [−4.84, −2.77] | 2 | 1.42 | 1 |
| compensatory-failure | +5d | 9 | 128 | **−5.33** | [−7.17, −3.51] | 2 | 1.20 | 1 |
| compensatory-failure | +10d | 1 | 42 | — | — | — | — | — |

**Read**: the subjective channel firmly signals cost-of-heavy-load in the pre-committed negative direction at +3d for the compensatory-success pool (AUC −0.47 CI [−0.83, −0.12]) and dramatically stronger for the compensatory-failure sub-arm (AUC −3.77 at +3d, −5.33 at +5d, CI far from zero on both). The subjective response magnitude on the failure pool is **~8× the success pool magnitude at +3d** and **~7× at +5d** — the felt-state trajectory clearly separates the two pools at both primary windows.

---

## 5. §8 decision-tree branch verdicts

Per Q24 MD §8.1 peak-based decay operationalisation: for each (autonomic channel × window × pool), a channel "decays" when `|Δ(w)| / |Δ(k*)| < 0.5` on the **raw** delta trajectory. Subjective channel (`gevoelscore`) receives its own decay screen per Q24 MD §8.1. Branches assigned per Q24 MD §8.2.

Full matrix in [`output/branch_verdicts.csv`](output/branch_verdicts.csv).

**Preamble on inherited fragility** (added in r2 per review absorption): §5 branch verdicts are computed on **raw** delta trajectories per Q24 MD §8.1 interpretive extension (see §10 item 6). This means the branches **inherit §6 detrend-fragility unconditionally** — any branch verdict whose underlying raw trajectory is in §6.1's detrend-erasing set is running on a signal that does not survive the §7.11 sensitivity read. Readers MUST cross-reference §6 for the detrend-status of each channel's underlying raw trajectory before treating a §5 branch verdict as independent evidence. The `[frag]` annotation on cells below flags each (channel × window × pool) whose raw AUC CI excludes zero but detrended CI does not; `[surface]` flags the failure-pool cells where the reverse holds (detrend surfaces the signal); un-annotated cells are "neither-sig" at raw AUC and therefore the decay verdict is computed on a raw trajectory not distinguishable from zero at the outcome level (which does not preclude a peak-based decay verdict but does mean the branch is not itself an independent-evidence signal).

### 5.1 Compensatory-success pool (primary)

| channel | +3d | +5d | +10d |
|---|---|---|---|
| stress_mean_sleep | **BOTH decay** | **BOTH decay** | **BOTH decay** |
| all_day_stress_avg | **BOTH decay** | ONLY subjective decays `[frag]` | ONLY subjective decays `[frag]` |
| bb_lowest | ONLY subjective decays | ONLY subjective decays `[frag]` | ONLY subjective decays `[frag]` |
| hr_median_waking | ONLY subjective decays `[frag]` | **BOTH decay** | **BOTH decay** |
| sleep_hr_avg_spo2 | ONLY subjective decays `[frag]` | **BOTH decay** | **BOTH decay** |

`[frag]` = raw AUC CI excludes zero AND detrended CI does not (per §6.1); branch computed on a raw trajectory that does not survive §7.11 sensitivity. Un-annotated cells with **BOLD** verdicts are cells whose raw AUC CI does not exclude zero at the outcome-level (neither-sig at §6 accounting) — the decay verdict is a shape-of-trajectory read on a trajectory whose overall level is not distinguishable from zero.

**Read**: the subjective decay screen fires at every primary + extended window on the compensatory-success pool (`gevoelscore` decays are the shared "yes" in every cell above). Autonomic decays are **channel-heterogeneous**:
- **`stress_mean_sleep` decays at all three windows** — most literature-concordant panel per Radin/Germain two-clock reading; both clocks re-converge to near-zero within the observation window.
- **`hr_median_waking` and `sleep_hr_avg_spo2` decay at +5d + +10d but NOT +3d** — delayed autonomic decay after prompt subjective decay; classical two-clock-with-slow-autonomic pattern at +3d, resolving into BOTH-decay at longer windows. Radin 2024 nightly-HR-persistence pattern would predict this shape.
- **`bb_lowest` and `all_day_stress_avg` do not decay at +5d / +10d despite their signs being inverted at raw AUC**. The peak-based screen flags them as "sustained" because `|Δ(k*)|` is at k=5 and k=10 (window edge = peak); recovery-not-yet-begun. These are the **ONLY subjective decays** branches — Q24 MD §8.2 pathway = "literature-inversion anomaly on channel c: felt-state recovers but autonomic axis c sustained; look for confounds first (measurement drift, medication, sleep architecture change)". Both fall out as detrend-fragile per §6 below.

**Channel-disagreement** at each primary window is the substantive finding per Q24 MD §8.3 cross-channel discipline:
- **+3d**: 2 channels BOTH-decay (`stress_mean_sleep`, `all_day_stress_avg`), 3 channels ONLY-subjective-decays (`bb_lowest`, `hr_median_waking`, `sleep_hr_avg_spo2`). Split 2:3.
- **+5d**: 3 channels BOTH-decay (`stress_mean_sleep`, `hr_median_waking`, `sleep_hr_avg_spo2`), 2 channels ONLY-subjective-decays (`all_day_stress_avg`, `bb_lowest`). Split 3:2.
- **+10d**: same 3:2 split as +5d (extended-window; descriptive-only per Q24 MD §5.1).

The autonomic-recovery-signal-carrying axis is **not uniform across the 5 channels**; the HR-window channels (waking + overnight) show the delayed-decay pattern the literature would predict, and the daytime-BB-floor channel (`bb_lowest`) diverges from the pattern.

### 5.2 Compensatory-failure pool (sub-arm)

| channel | +3d | +5d | +10d |
|---|---|---|---|
| stress_mean_sleep | NEITHER decays | NEITHER decays `[surface]` | ONLY autonomic decays |
| all_day_stress_avg | NEITHER decays | ONLY autonomic decays `[surface]` | ONLY autonomic decays |
| bb_lowest | NEITHER decays | NEITHER decays `[surface]` | ONLY autonomic decays |
| hr_median_waking | NEITHER decays | NEITHER decays | ONLY autonomic decays |
| sleep_hr_avg_spo2 | NEITHER decays `[surface]` | NEITHER decays `[surface]` | ONLY autonomic decays |

`[surface]` = raw AUC CI does not exclude zero BUT detrended CI does (per §6.2); the raw-arm branch verdict here is running on a raw trajectory that hides a signal only visible after detrending — the branch reading understates the underlying signal. Un-annotated cells are neither-sig at both arms.

**Sample-size discipline**: at **+10d n=1**, the branch verdicts above are **NOT DEFENSIBLE** per Q24 MD §3.5 (<10 threshold) — reported for output-completeness only. At +5d n=9 the CIs are wide; at +3d n=16 the branches are the most reliable.

**Read**: on the compensatory-failure sub-arm, the **subjective channel does NOT decay** at any window. This is the direct empirical anchor of the Q24.5 unfalsifiable-counterfactual sub-part: on the days where the participant's post-heavy trajectory was interrupted by a crash, the felt-state trajectory shows **sustained** worseness through the observation window rather than the decay pattern observed on the compensatory-success pool. The autonomic channels at +3d and +5d are also sustained (NEITHER decays); at +10d (n=1, not defensible) the autonomic channels flip to ONLY-autonomic-decays but the single-episode trajectory carries no interpretive weight.

**Substantive descriptive finding**: **the compensatory-success vs -failure pool trajectory contrast on `gevoelscore` is the clearest signal in the entire Wave 1 output.** Success pool subjective decays at every window; failure pool subjective sustains at every window. Descriptive-only per Q24 MD §3.5 no-pre-registered-inferential-test discipline, but this is the load-bearing empirical anchor for the Q24.5 sub-part interpretation.

---

## 6. Detrend-fragility findings per Q24 MD §7.11

Per Q24 MD §7.11 escalation rule: any (outcome, window, pool) where the raw trajectory has AUC CI excluding zero but the detrended CI does not (or vice versa) is flagged **trajectory-confound-suspect**. Detrend arm uses per-episode 30d pre-window linear extrapolation subtracted from post-window observations; comparator arm detrended paired-wise per Q24 MD §7.11.

**Total cells** (outcome × window × pool at raw+detrended arm pair): 118. **Detrend-fragility count: 44**.
- Cells where raw AUC CI excludes zero: 43.
- Cells where detrended AUC CI excludes zero: 15.
- Detrend-fragility XOR: **44** — meaning **36 cells** (raw significant but detrend not) + **8 cells** (detrend significant but raw not).

**By window**: 14 at +3d, 18 at +5d, 12 at +10d. Detrend-fragility affects every window comparably.
**By pool**: 29 on compensatory-success, 15 on compensatory-failure.

### 6.1 Detrend-erasing cells (raw sig → detrend not sig, 36 total) — headline set

| outcome | window | pool | raw AUC (CI) | detrend AUC (CI) |
|---|---:|---|---|---|
| total_steps | +3d | success | **−1356** [−2054, −665] | −776 [−1625, +106] |
| total_steps | +5d | success | **−3865** [−5455, −2290] | −1965 [−4183, +173] |
| total_steps | +10d | success | **−15316** [−20523, −9955] | −4595 [−10955, +2724] |
| total_steps | +5d | failure | **−5416** [−8890, −1975] | −3482 [−8240, +333] |
| vigorous_min | +3d | success | **−1.72** [−2.28, −1.21] | −0.73 [−1.74, +0.29] |
| vigorous_min | +5d | success | **−4.26** [−5.53, −3.07] | −1.06 [−3.82, +1.44] |
| vigorous_min | +10d | success | **−14.51** [−17.95, −11.24] | +4.30 [−6.38, +14.30] |
| active_min | +3d | success | **−15.27** [−29.76, −0.97] | −12.44 [−29.74, +4.61] |
| active_min | +10d | success | **−228.9** [−327.5, −126.1] | −81.4 [−215.3, +67.5] |
| sleep_duration_min | +3d | success | **+74.15** [+40.11, +107.45] | +7.84 [−30.77, +46.06] |
| sleep_duration_min | +5d | success | **+180.0** [+107.6, +252.8] | +75.5 [−13.3, +161.9] |
| sleep_duration_min | +10d | success | **+279.1** [+72.9, +464.2] | +5.73 [−265.6, +287.5] |
| sleep_deep_min | +3d | success | **−23.85** [−42.87, −4.77] | −16.07 [−36.13, +4.04] |
| sleep_light_min | +3d | success | **+89.19** [+54.44, +123.37] | +14.98 [−28.05, +58.50] |
| sleep_light_min | +5d | success | **+201.6** [+132.8, +267.0] | +50.8 [−41.2, +141.5] |
| sleep_rem_min | +10d | success | **−139.6** [−240.9, −39.3] | −36.1 [−184.4, +113.0] |
| bb_lowest | +5d | success | **+13.60** [+2.76, +24.03] | +3.90 [−7.18, +14.88] |
| bb_lowest | +10d | success | **+76.00** [+35.09, +112.18] | −1.88 [−44.11, +38.46] |
| all_day_stress_avg | +5d | success | **−6.68** [−12.74, −0.13] | −1.71 [−8.33, +5.05] |
| all_day_stress_avg | +10d | success | **−33.14** [−54.75, −8.54] | −0.23 [−27.05, +27.61] |
| hr_median_waking | +3d | success | **+3.51** [+1.36, +5.66] | −1.80 [−4.27, +0.71] |
| sleep_hr_avg_spo2 | +3d | success | **+2.30** [+0.26, +4.34] | +1.01 [−1.39, +3.39] |
| asleep_stress_max_uds | +5d | success | **−19.86** [−33.92, −5.93] | −0.75 [−18.63, +17.18] |
| asleep_stress_max_uds | +10d | success | **−66.45** [−109.26, −24.58] | −7.36 [−81.64, +67.26] |
| spo2_avg_sleep | +10d | success | **−8.06** [−12.48, −3.52] | −2.35 [−6.73, +2.46] |
| gevoelscore | +3d | success | **−0.47** [−0.83, −0.12] | −0.03 [−0.48, +0.41] |
| ... (10 more cells; see [`output/trajectory_summary.csv`](output/trajectory_summary.csv)) | | | | |

### 6.2 Detrend-surfacing cells (raw not sig → detrend sig, 8 total)

| outcome | window | pool | raw AUC (CI) | detrend AUC (CI) |
|---|---:|---|---|---|
| effective_exertion_min | +3d | failure | +5.07 [−1.83, +13.46] | **−31.64** [−66.93, −4.58] |
| effective_exertion_min | +5d | failure | +1.95 [−7.75, +13.41] | **−65.12** [−158.78, −4.82] |
| sleep_efficiency_tib | +5d | failure | −0.001 [−0.019, +0.015] | **−0.016** [−0.032, −0.003] |
| stress_mean_sleep | +5d | failure | +11.50 [−6.28, +37.01] | **+21.29** [+6.24, +40.95] |
| all_day_stress_avg | +5d | failure | +9.63 [−6.20, +30.18] | **+16.74** [+4.54, +29.30] |
| bb_lowest | +5d | failure | −4.69 [−20.51, +11.50] | **−27.61** [−47.76, −8.81] |
| sleep_hr_avg_spo2 | +3d | failure | +4.57 [−2.28, +12.39] | **+8.11** [+1.99, +14.86] |
| sleep_hr_avg_spo2 | +5d | failure | +6.71 [−5.66, +23.01] | **+13.34** [+3.91, +24.22] |

**Read**: the 8-cell detrend-surfacing set clusters heavily on the **compensatory-failure sub-arm**. On the failure pool, envelope drift *masks* real event-triggered signals; on the success pool, envelope drift *creates* apparent signals that don't survive detrending. This is a **substantive descriptive finding** per Q24 MD §7.11: the same LC recovery trajectory (crash rate 10/y → 2/y per Q24 MD §10.8) that inflates the compensatory-success pool's activity-and-sleep signals is also *suppressing* real autonomic-cost signals on the compensatory-failure sub-arm, because failure-pool episodes are concentrated in the higher-crash-rate era (2023-2024 corpus half) where the underlying autonomic-stress baseline was already elevated. All 8 detrend-surfacing failure-pool cells point in the pre-committed direction (stress + HR *up*, BB *down*, efficiency *down*, effective_exertion *down*) — direction-consistent with the compensatory-failure reading, only visible after removing envelope drift.

### 6.3 Interpretive load per Q24 MD §7.11 escalation rule

Q24 MD §7.11: "any Stage H pre-registration on a raw-trajectory finding that does not survive detrending must justify why the raw reading carries more weight than the detrended reading."

**36 raw-only findings** (in the detrend-erasing set, §6.1) are trajectory-confound-suspect — see §9.1 caveat 9 for the drift-entanglement reframe of this set (raw = upper bound on the compensatory response; detrended = lower bound; neither cleanly separates nuisance drift from compensatory-behaviour-improvement drift). **8 detrend-only findings** (§6.2) are trajectory-confound-suspect in the opposite direction — envelope drift was hiding them. **Neither set overturns Stage D descriptive verdicts on its own**; both flag Stage H pre-reg targets that must be justified against the detrended reading before advancing.

**Trajectory-confound-surviving cells** — those where raw AND detrended AUC CIs both exclude zero — number **7** total when counted by "both arms significant". Empirically these split into two categorically different classes on CSV verification:

**Class A: 5 sign-consistent Stage-H-candidate survivors** (raw AND detrended AUC CI exclude zero AND same sign):

| outcome | window | pool | direction | raw AUC (CI) | detrend AUC (CI) |
|---|---:|---|---|---|---|
| total_steps | +3d | compensatory_failure | negative | **−2539** [−3850, −1178] | **−2741** [−5190, −464] |
| sleep_awake_min | +3d | compensatory_failure | positive | **+11.61** [+2.95, +21.95] | **+10.26** [+3.03, +18.64] |
| sleep_efficiency_tib | +3d | compensatory_failure | negative | **−0.018** [−0.037, −0.003] | **−0.018** [−0.033, −0.006] |
| gevoelscore | +3d | compensatory_failure | negative | **−3.77** [−4.84, −2.77] | **−1.86** [−2.97, −0.61] |
| gevoelscore | +5d | compensatory_failure | negative | **−5.33** [−7.17, −3.51] | **−3.16** [−4.70, −1.60] |

These 5 cells are the robust core — compensatory-response signals whose *direction* AND *significance* survive both raw and detrended reads, and whose magnitude therefore does NOT depend on the drift-entanglement disambiguation (§9.1 caveat 9). They are the defensible seed set for Stage H pre-reg drafting in Wave 2.

**Empirical observation to preserve**: **all 5 sign-consistent survivors cluster on the compensatory-failure sub-arm** (4 at +3d, 1 at +5d — `gevoelscore`). This concentration is itself substantive: on the failure pool, envelope drift was *masking* real event-triggered signals (per §6.2 read); the detrend companion surfaces them. The success pool, by contrast, has **zero sign-consistent survivors** at Wave 1 sample sizes — every success-pool cell that shows raw AUC CI excluding zero either fails to reach detrended significance (raw-only-sig, §6.1) or sign-flips under detrending (see Class B). This is directly informative for Q24.5 counterfactual interpretation.

**Class B: 2 sign-flip diagnostic cells** (raw AND detrended AUC CI both exclude zero, but in OPPOSITE directions):

| outcome | window | pool | raw AUC (CI) | detrend AUC (CI) |
|---|---:|---|---|---|
| effective_exertion_min | +3d | compensatory_success | **+3.55** [+0.25, +7.17] | **−6.49** [−12.88, −0.47] |
| spo2_avg_sleep | +3d | compensatory_failure | **+1.01** [+0.01, +2.03] | **−1.36** [−2.49, −0.19] |

**These sign-flippers are NOT dismissible artefacts AND NOT Stage H seeds.** They require diagnostic investigation before either dismissal or elevation. Raw and detrended pointing opposite directions typically means the raw signal and underlying drift are strongly co-varying in ways not yet understood — the detrend operation is removing a component that dominates the raw effect and flips it sign. `effective_exertion_min` at +3d success was already flagged in §4.1 as a "nuanced story" (definitional-pair signal); the sign-flip under detrending materially strengthens that caveat. `spo2_avg_sleep` at +3d failure is a novel diagnostic surface for Wave 2. **Wave 2 open item: diagnostic investigation of the 2 sign-flippers** (probe per-episode raw + pre-window overlays; check whether the flip is driven by a small subset of episodes or by a systematic drift-magnitude interaction; do NOT seed Stage H pre-regs on these cells until the flip mechanism is understood).

---

## 7. §3.5 pool-comparison read (compensatory-success vs compensatory-failure)

Per Q24 MD §3.5, the two pools answer **structurally different questions**. Wave 1 reports the raw pool contrast per outcome without an inferential test (per Q24 MD §3.5 no-pre-registered-inferential-test-at-Stage-D discipline). The contrast is directly informative for the Q24.5 unfalsifiable-counterfactual sub-part.

### 7.1 Subjective channel — clearest empirical anchor

At +3d, the raw subjective trajectory magnitude ratio is **failure:success ≈ 8:1** (AUC −3.77 vs −0.47). At +5d, **failure:success ≈ 7:1** (AUC −5.33 vs −0.78). At +10d the failure pool has n=1, not defensible.

Per §5 branch verdicts: subjective decays at every window on the success pool; sustains at every window on the failure pool. **The pool that crashes shows a sustained-worseness subjective trajectory; the pool that does not crash shows a decaying subjective trajectory**. Read together, this is descriptively substantive at the participant-experience level.

**Descriptive-only interpretation** (per CONVENTIONS §4.2 caveat-class): the compensatory-success pool = episode-ends followed by no crash in-window; the compensatory-failure sub-arm = episode-ends followed by a crash in-window. By construction, crash-day gevoelscore values are lower than non-crash-day values (crash-v2 is derived from gevoelscore per project convention). **This means the failure-pool AUC being ~8× larger than success-pool AUC is partly definitional**: the failure pool contains days with crash-defining low gevoelscore values inside the observation window. The finding is not spurious — the pool split is by design the counterfactual anchor — but the *magnitude* of the failure-vs-success subjective contrast reflects the crash-definition circularity to some extent, not purely a shape-of-trajectory difference. **Descriptively worth surfacing for Wave 2 orchestrator review**: whether a matched-subjective-decay-magnitude comparator (matching failure-pool comparators to success-pool comparators on baseline gevoelscore drift) would meaningfully change the failure-vs-success magnitude ratio.

### 7.2 Autonomic channels — divergent sign patterns

At +3d, +5d, and +10d, the compensatory-failure sub-arm's autonomic-load channels (`stress_mean_sleep`, `all_day_stress_avg`, `sleep_hr_avg_spo2`, `hr_median_waking`) trend in the pre-committed +1 direction (elevated) while the compensatory-success pool's same channels trend in the *inverse* direction (depressed vs matched-ordinary). Under detrending (§6.2), the failure-pool autonomic-elevated signal is stronger than the raw reading (envelope drift was suppressing it). On the success pool, the raw autonomic-depressed signal is largely trajectory-confound-suspect (envelope drift was creating it; §6.1).

**Combined descriptive read**: after detrending, the two pools show **substantively different post-heavy autonomic patterns** — the failure pool shows the physiologically-predicted post-heavy autonomic-load elevation (in the pre-committed direction); the success pool shows a near-null-or-inverted post-heavy autonomic trajectory. Descriptive-only; no pre-registered inferential contrast between the two pools per Q24 MD §3.5.

### 7.3 Activity channels — direction-agreement with magnitude difference

Both pools show negative activity-side AUC (fewer steps, less exertion, fewer vigorous minutes after heavy episode-end) with the failure pool typically showing **~2× the success-pool magnitude** at +3d/+5d. This is direction-agreement — post-heavy activity drop is not specific to whether the trajectory ends in a crash — but the failure pool's larger drop is consistent with either (a) more severe post-heavy-load lived-experience prompting more rest, or (b) crash-in-window forcing greater inactivity through the observation window. Descriptive-only per Q24 MD §7.11 escalation rule; the failure-pool activity signals are trajectory-confound-suspect at +5d/+10d.

### 7.4 Sleep channels — direction-agreement

Both pools show positive `sleep_duration_min` AUC at +3d/+5d (extra sleep after heavy episode-end); the failure pool magnitude is slightly higher at +3d (~101 min vs +74 min success) but the direction and shape are similar. Both are trajectory-confound-suspect per §6.

---

## 8. Data-validity notes

Per Q24 MD §11 zero-vs-NaN + explicit-missing-data-reporting discipline. Per-outcome per-day n_valid trigger + comparator counts live in [`output/per_day_trajectories.csv`](output/per_day_trajectories.csv). No `.fillna(0)` applied at any point in the pipeline; missing observations remain missing.

**Coverage per outcome at compensatory-success trigger arm, +3d window** (day 1 of the post-window, of n=109 total episodes):

| outcome | n_valid | coverage |
|---|---:|---:|
| effective_exertion_min | 109 | 100.0% |
| total_steps | 106-107 | ~98% |
| vigorous_min, active_min, all_day_stress_avg, bb_lowest | 107 | 98% |
| hr_median_waking | 105-106 | ~97% |
| asleep_stress_max_uds | 104-106 | ~96% |
| sleep_duration_min, sleep_deep_min, sleep_light_min, sleep_awake_min, sleep_efficiency_tib | 103-106 | ~95-97% |
| stress_mean_sleep | 103-105 | ~95-96% |
| sleep_rem_min, sleep_efficiency_staged | 101-104 | ~93-95% |
| gevoelscore | 103-104 | ~95% |
| sleep_hr_avg_spo2 | 98-100 | ~90-92% |
| spo2_avg_sleep | 90-94 | ~83-86% |
| **bb_overnight_gain, bb_overnight_gain_frac** | **42-46** | **~39-42%** |

**Descriptive-only-with-CI flags per Q24 MD §11** (any operand with <50% coverage at a given window is flagged):
- `bb_overnight_gain` + `bb_overnight_gain_frac` at +3d (~40% coverage; already sensitivity-tier per Q24 MD §6.2.1).

**Comparator pool sizes** per outcome × window are recomputed per Q24 MD §4.2. Matched-ordinary comparator pools (per-outcome, shared across success + failure pools since the comparator pool is defined outcome-wise not pool-wise) range from ~198 (`spo2_avg_sleep`, 83% base coverage) to ~327 (`effective_exertion_min`, 98% base coverage) at +3d; shrink to ~87-204 at +5d; ~27-105 at +10d. Sparse-availability outcomes (`bb_overnight_gain` + `bb_overnight_gain_frac`) sit at n_c=147 at +3d per Q24 MD §6.2.1 discipline.

**Detrended-arm episode drop-out per Q24 MD §7.11** (episodes with <15 valid pre-window points): minor. On +3d success pool, detrended n=103-107 vs raw n=103-107 (near-identical); only sparse-coverage outcomes (`bb_overnight_gain`) drop meaningfully (n=45 detrended vs n=46 raw at +3d success).

**Compensatory-failure sub-arm data-validity gotcha**: at +3d, **zero of 16 failure-pool episodes** have complete post-window `bb_overnight_gain` data. The sub-arm cannot be read on Family E operands at Wave 1 sample sizes.

---

## 9. Confound status per Q24 MD §10

Walking the 8 pre-committed caveats and noting which are RELEVANT to observed Wave 1 findings vs which are STRUCTURAL-only.

| # | Caveat | Wave 1 status |
|---:|---|---|
| 1 | 2026 heavy-rate elevation (47.4% vs 34-35% baseline) | **RELEVANT** — the trajectory-detrend fragility findings (§6) span both 2022-2025 and 2026 episodes. Per Q24 MD §10 item 1, a sensitivity trajectory excluding 2026 is worth adding in Wave 2 if the finding survives detrending. |
| 2 | Multi-axis heavy-day composition | **STRUCTURAL** — Wave 1 uses combined-primary trigger; axis-dominance stratification is deferred to Wave 2. |
| 3 | Baseline drift (lagged reference) | **RELEVANT** — envelope drift is precisely what §7.11 detrending addresses; the 44 detrend-fragility cells directly evidence baseline drift's load on Wave 1 raw findings. |
| 4 | Deconditioning floor effect | **PARTIALLY RELEVANT** — the compensatory-success pool's autonomic sign-inversion (§4.3) may partly reflect a floor effect where post-heavy autonomic-load has already saturated; the detrend companion partially controls for this. |
| 5 | Citalopram-era vs non-citalopram-era | **STRUCTURAL** — Wave 1 pools across dose-state; per Q24 MD §10 item 5, a strong Stage D finding motivates Q24 sub-part 3 authorship. The `stress_mean_sleep` BOTH-decay pattern at all three windows on the success pool is a candidate finding for that follow-up (Citalopram is known to lower `stress_mean_sleep` per intervention_effects_descriptive.md §8). |
| 6 | Small extended-window samples (n=12 at +10d) | **RELEVANT** — Wave 1 +10d bootstrap CIs are wide; all +10d verdicts explicitly descriptive-only. Compensatory-failure pool +10d n=1 = NOT DEFENSIBLE per Q24 MD §3.5. |
| 7 | Intensity-stratified sample floor (n=19 at +5d) | **STRUCTURAL** — intensity stratification deferred to Wave 2. |
| 8 | Envelope-drift asymmetry (L2.2 stationarity) in comparator pool | **RELEVANT — ESCALATED (r2)**. Matched-ordinary comparator draws from full LC-era. The 36 detrend-erasing cells (§6.1) are directly the envelope-drift signal Q24 MD §10 item 8 predicted; the 8 detrend-surfacing cells (§6.2) are the same confound in the opposite direction on the failure pool. **Wave 1 empirical fragility count 44/118 crosses Q24 MD §10 item 8's finding-specific escalation threshold** — era-stratified comparator sensitivity is therefore **no longer a generic Wave 2 candidate; it is a triggered escalation per the Q24 MD §10.8 rule**. Concrete trigger for the era-stratified companion arm (calendar-year comparator match): **before Stage H pre-reg drafting on any of the 5 sign-consistent survivors in §6.3 that touch autonomic channels** (currently zero, since all 5 survivors are activity/sleep/subjective — but the rule is now armed and will fire immediately when the survivor set changes at Wave 2 re-run). Q24 MD §10 item 8 remains the escalation-rule authority. |

**Findings-specific caveat additions per Q24 MD §7.11 escalation rule**: every detrend-erasing cell in §6.1 receives a **trajectory-confound-suspect** flag as a finding-specific caveat. Downstream Stage H pre-registration on any of those cells must justify why the raw reading carries more weight than the detrended reading.

### 9.1 Caveat 9 — drift-entanglement reframe of the detrend companion (r2, user-endorsed 2026-07-15)

**Detrending removes multiple sources of drift, not just nuisance drift.** The 4-year LC-era window (2022-04 → 2026-06) that Wave 1 pools across mixes multiple time-varying components on the pre-window `linear_detrend_on_pre` operation per §7.11 (inherited from sister [`intervention_effects_descriptive.md`](../../../methodology/intervention_effects_descriptive.md)):

- disease natural history (LC progression / recovery across years)
- citalopram modulation (started 2024-04-09; midway through the corpus)
- deconditioning (baseline exertion capacity shifts)
- aging (4 years)
- long-cycle seasonality
- **learned-pacing / compensatory-behaviour improvement — the very construct Q24 sub-part 1 is trying to measure**

The `linear_detrend_on_pre` operation is **agnostic across these components** — it removes them all bundled together, because a per-episode 30d pre-window linear fit cannot distinguish disease-drift from citalopram-drift from pacing-improvement-drift.

This creates a genuine interpretive ambiguity for the detrend-fragile findings surfaced in §6:

- **Raw findings should be read as an upper bound on the compensatory response** (includes all time-associated variance, including any pacing-improvement drift).
- **Detrended findings as a lower bound** (excludes all time-associated variance, including the pacing-learning signal Q24 sub-part 3 is meant to answer).
- **The truth is between the two**.

**Applied to Wave 1**: the 36 raw-only-significant cells (per §6.1 detrend-fragility count) **should NOT be dismissed as "not real."** They are **drift-entangled** — Wave 1 alone cannot distinguish nuisance drift from compensatory-behaviour-improvement drift without running Q24 sub-part 3 (phase-stratification: does the compensatory response strengthen across LC phases / calendar epochs? if yes, the drift being detrended out is partly the target signal). This provides an explicit motivating link: **Wave 1 → Q24 sub-part 3 disambiguation**. The 36 drift-entangled cells are candidates for sub-part 3 investigation, not dismissible artefacts.

The 5 sign-consistent survivors from §6.3 are the robust core — they are compensatory-response signals whose *magnitude and direction* do NOT depend on the disambiguation (both raw and detrended arms agree). Everything raw-only in §6.1 is drift-entangled at Wave 1 sample sizes and passes to sub-part 3 as a candidate signal, not to a Stage H dismissal pile.

**Interaction with the era-stratified escalation (caveat 8 above)**: era-stratified comparator sensitivity attacks the drift-entanglement from the comparator-side; the detrend companion attacks it from the trigger-side. Neither on its own resolves the ambiguity; sub-part 3 phase-stratification of the trigger response is the design-level disambiguator.

---

## 10. Open inputs surfaced for orchestrator review

**None of the below overturn Q24 MD locked design decisions.** Each item is a Wave-1-produced observation that warrants orchestrator/user disposition before Wave 2 dispatches.

1. **§3.5 sub-arm sample size at +10d is n=1** — Q24 MD §3.5 policy is "narrative single-case reads only, not a bootstrap-CI trajectory". The current audit computes bootstrap CIs on n=1 (which by construction yield degenerate zero-width CIs) then emits them; the branch verdicts at +10d compensatory-failure are output but flagged NOT DEFENSIBLE. Suggested Wave 2 refinement: skip bootstrap for sub-arms with n<10 and emit only per-day mean without CI (or omit the row entirely). Minor cosmetic issue.

2. **Compensatory-success sign-inversion on `stress_mean_sleep` + `all_day_stress_avg` + `bb_lowest`** — the pre-committed +1 direction (cost = elevated) inverts on the success pool at raw values. Per Q24 MD §7.7 this is a sign-inversion finding in its own right, not a null. **Two candidate readings** (§4.3) — compensatory-behaviour-visible or trajectory-confound. Under detrending most of the inversion evaporates (§6.1), which pushes the interpretive weight toward trajectory-confound. Worth surfacing to orchestrator: whether Wave 2 should add a "self-reported pacing intensity on d+1" companion column (if any exists in the corpus) to disambiguate the compensatory-behaviour reading from the trajectory-confound reading. Descriptive-only; no design-of-Wave-1 change.

3. **Failure-pool subjective magnitude includes crash-definition circularity** (§7.1) — the ~8× magnitude ratio of failure-vs-success subjective AUC at +3d partly reflects the fact that failure-pool days *contain* crash-defining low gevoelscore values by construction. The subjective contrast is not spurious (the pool split is designed to answer the counterfactual question) but the magnitude comparison against success-pool inherits some circularity. **Wave 2 candidate refinement**: a matched-subjective-baseline sensitivity arm (matching failure-pool comparators to success-pool comparators on baseline gevoelscore drift). Not a design change to Q24 MD; a Wave-2-scope decision.

4. **`bb_overnight_gain` zero-coverage at +3d compensatory-failure sub-arm** (§4.5, §8) — none of the 16 failure-pool episodes have complete post-window bb_overnight_gain data. This is a hard limit of the sparse channel × the small sub-arm intersection. The audit emits NaN summaries for that cell rather than misleading zero-CIs. No design change needed.

5. **Trajectory-detrend n-loss for detrended arm is minimal** (§8) — the 30d pre-window is dense enough that few episodes drop out under §7.11's <15-valid-point rule. Confirms Q24 MD §7.11's 30d + 15-point choice is well-calibrated for the LC-era corpus.

6. **Q24 MD §8.1 peak-based decay screen operates on RAW delta trajectories** — the MD does not explicitly say raw or detrended, but the primary reading pathway (which the §8.2 branch verdicts hang on) is naturally the raw trajectory since the detrend companion is the §7.11 sensitivity read. Wave 1 audit follows this pathway explicitly. If orchestrator disagrees, the branch verdicts can be trivially re-run on detrended trajectories from the same output CSVs. **Interpretive extension surfaced for orchestrator review**: whether §8 branches should be computed on both raw AND detrended trajectories and reported side-by-side (my Wave 1 execution reports raw-only per plain reading of Q24 MD §8.1 rationale).

7. **Q24 MD §7.9 first-crossing-day operationalisation** — the MD says "first d+k where Δ(k) falls outside the matched-ordinary arm's bootstrap 95% CI". This is operationalised as "first k where the delta-CI (bootstrap on `trigger − comparator`) itself excludes zero", which is equivalent under the delta framing but not literally what §7.9 wrote (it mentioned the matched-ordinary arm's CI specifically). The two are mathematically equivalent at 95% percentile-CI construction and unbiased estimators. **Interpretive extension surfaced for orchestrator review** — the equivalent operationalisation was chosen because a per-day CI on `comparator` alone doesn't test whether `trigger` diverges from it; the delta-CI does.

---

## 11. Cross-references

- **Q24 methodology MD**: [`../../../methodology/post_heavy_day_compensatory_rest.md`](../../../methodology/post_heavy_day_compensatory_rest.md) LOCKED r1 2026-07-15 (commit `58b7723`) — THE authoritative source for every design decision executed here.
- **Sleep operand catalogue**: [`../../../methodology/sleep_metrics.md`](../../../methodology/sleep_metrics.md) r1 2026-07-15 (commit `914745b`) — sleep-family formulas + LC-era coverage.
- **Stage -1 audit**: [`../Q24-precursor-heavy-day-structure/audit.md`](../Q24-precursor-heavy-day-structure/audit.md) LOCKED r1 2026-07-15 — structural findings + episode definitions; every Wave 1 pool count reproduces the audit §5 clean-sample figures.
- **Q24 MD review report**: [`../../../reviews/methodology-post_heavy_day_compensatory_rest-2026-07-15.md`](../../../reviews/methodology-post_heavy_day_compensatory_rest-2026-07-15.md) — reviewer report that shaped Q24 MD §7.10 + §7.11 + §10.8 pre-lock additions.
- **Sister detrend precedent**: [`../../../methodology/intervention_effects_descriptive.md`](../../../methodology/intervention_effects_descriptive.md) §6 `linear_detrend_on_pre` — the pre-vs-post median-diff helper that Q24 MD §7.11 adapts to per-day trajectory.
- **Pipeline consolidator**: [`../../../pipeline/03_consolidate/build_unified_dataset.py`](../../../pipeline/03_consolidate/build_unified_dataset.py) — column formulas for derived outcomes; consumed via `per_day_master.csv`.
- **CONVENTIONS anchors**: [§1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs) producer-mode; [§2.1](../../../CONVENTIONS.md#21-descriptive-before-inference) descriptive-before-inference; [§3.7](../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) trajectory-detrend audit hook; [§4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class discipline; [§5](../../../CONVENTIONS.md#5-project-wide-anchors-read-once-then-trust) zero-vs-NaN discipline.
- **Precedent Stage D audit MD**: [`../HA-C4cp/descriptive_audit.md`](../HA-C4cp/descriptive_audit.md) LOCKED r1 — structural precedent for producer-mode Stage D audit MD tone + reference-window audit-trace + pool-comparison read.

---

## 12. Lock log

| version | date | change |
|---|---|---|
| r2 (this) | 2026-07-15 | Fresh-session `/research-review` verdict **PASS with caveats** at [`../../../reviews/Q24-post-heavy-trajectory-2026-07-15.md`](../../../reviews/Q24-post-heavy-trajectory-2026-07-15.md) (139 lines). Six substantive absorbs applied (patches 1-6): (1) §6.3 arithmetic corrected from "7 survivors" to "5 sign-consistent Stage-H-candidate survivors + 2 sign-flip diagnostic cells requiring Wave 2 investigation" (L4 fire #1; load-bearing for Stage H seeding). (2) NEW §9.1 caveat 9 drift-entanglement reframe (user-endorsed framing 2026-07-15): raw = upper bound; detrended = lower bound; truth between; 36 drift-entangled cells are candidates for Q24 sub-part 3 disambiguation, NOT dismissible artefacts. Provides explicit Wave 1 → sub-part 3 motivating link. (3) §4-§8 `n_c` column corrections after CSV verification (L4 fire #2; downstream statistical-power reasoning unaffected; only tabulated n_c figures wrong; ~2× undercount confirmed and fixed against CSV `n_comparator_days` column). (4) §5 branch verdicts cross-annotated with §6 detrend fragility via preamble + per-cell `[frag]` / `[surface]` footnotes (L3.5; prevents over-weighting the Radin 2024 delayed-HR-decay reading given the underlying raw trajectories' §6.1 fragility status). (5) §9 caveat 8 era-stratified comparator sensitivity escalated from generic Wave 2 candidate to triggered escalation per Q24 MD §10.8 rule (L2.2; 44/118 fragility crosses the threshold). (6) §12 lock log + status header update. STATUS transitions: LOCKED r1 → LOCKED r2. Wave 2 open items logged: diagnostic investigation of 2 sign-flippers (`effective_exertion_min` +3d success + `spo2_avg_sleep` +3d failure); Q24 sub-part 3 phase-stratification (now with explicit motivating link per §9.1); intensity-stratified + inclusive-overlap arms; Stage H pre-reg drafting on the 5 sign-consistent survivors (all on compensatory-failure sub-arm at +3d/+5d, activity + sleep + subjective channels). |
| r1 | 2026-07-15 | Initial lock. Wave 1 Stage D descriptive audit against Q24 MD LOCKED r1 2026-07-15 (commit `58b7723`); combined intensity trigger × strict-clean overlap × both compensatory-success (n=109/43/11 at +3d/+5d/+10d) and compensatory-failure (n=16/9/1) pools; ~20 outcomes across activity + sleep architecture + sleep autonomic + day autonomic + sensitivity + subjective; 9 trajectory summary statistics per (outcome × window × pool × raw-or-detrended) with bootstrap 95% CIs (B=10,000, per-episode block-length-1 resampling, `RANDOM_SEED = 20260715`); §7.11 linear pre-window trajectory detrend adapted from `intervention_effects_descriptive.md` per per-episode 30d pre-window + 15-valid-point minimum; §8 four-branch decision-tree verdicts per (5 autonomic channels × 3 windows × 2 pools). Top-line findings: subjective decays at every window on the success pool + sustains at every window on the failure pool; autonomic channels show heterogeneous decay across the 5 channels (2:3 split at +3d, 3:2 split at +5d and +10d on success pool); 44 of 118 (outcome × window × pool) cells show detrend-fragility per §7.11 escalation rule (36 raw-only-sig + 8 detrend-only-sig), heavily clustered on the compensatory-success pool at +5d/+10d; sample-size discipline per Q24 MD §3.5 applied at +10d compensatory-failure (n=1 → NOT DEFENSIBLE flag). Intensity-stratified arms + inclusive overlap policy + Stage H pre-reg drafting deferred to Wave 2. Wall-clock: ~163s. Fresh-session `/research-review` NOT dispatched at Stage D per lock (Wave 1 producer-mode audit landing; reviewer-mode audit recommended before any Wave 2 Stage H pre-reg drafting reads §5 branch verdicts). Wave 2 candidates surfaced in §10 (intensity-stratified arms, inclusive overlap, era-stratified comparator sensitivity per Q24 MD §10 item 8, matched-subjective-baseline sensitivity for pool contrast on gevoelscore). **Drift triggers**: (1) Q24 MD r1→r2 revision → Wave 1 outputs re-consumed via pipeline re-run; (2) `per_day_master.csv` corpus growth beyond +10% of current n=1524 → sanity re-check at Wave 2 dispatch time; (3) Q24 MD §7.11 detrend method revision → detrend.py re-implementation + re-run; (4) any Stage H pre-reg draft against a §5 branch verdict → fresh-session `/research-review` on this Stage D audit MD before pre-reg lock. |
