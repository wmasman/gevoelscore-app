# HA-P6 — Post-crash window distinctive autonomic-recovery shape (Personal-register, descriptive characterisation)

## Authorship

**Drafted 2026-06-15** by Claude (Opus 4.6) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. Drafted in the same session that drafted [HA-C4b](../HA-C4b/hypothesis.md) (locked at `80607e4`) and [HA-P7](../HA-P7/hypothesis.md) (locked at `7f1ecc8`); shared context includes the [hypothesis_lock_process MD](../../../methodology/hypothesis_lock_process.md) the C4b + P7 retrospective produced. Pre-reg follows the [HA11 pre-reg pattern](../HA11-stress-udip/hypothesis.md) with **descriptive-mode adaptations** per the [P6 drafting handoff](C:/Users/Gebruiker/.claude/plans/session-p6-prereg-handoff-2026-06-15.md): §5 reframed as "Pre-registered findings shape" (not falsification criterion); §9 reframed as "What we do with each observation shape" (not verdict branching).

The drafting was performed under the operationalisation-precision walkthrough per the lock-process MD §3.2. Four load-bearing operationalisation choices were locked interactively before drafting:

1. **Sub-hypothesis scope**: keep BOTH the descriptive primary AND the correlational secondary from the register entry (recovery shape ↔ crash duration + next-crash interval). The secondary is correlational-only (no SUPPORTED bar); reported with block-bootstrap CIs per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) to address the autocorrelation pattern that fired BLOCKING on HA-P7.
2. **Channel set**: 7 channels per handoff recommendation — `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`, `bb_overnight_gain` (where available; coverage gap pre-2024-09-18 per [intervention_effects §2b](../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain)), `resting_hr`, `gevoelscore`, `stress_low_motion_min_count_S60_Mlow` (the Session E primitive). `n_minutes_resp_above_18` queued for v2.
3. **Matched-baseline construction**: Option C — BOTH matched-deep-trough non-crash days AND lagged personal baseline (CONVENTIONS §3.2 pattern). Report both; concordance increases confidence; divergence is a methodological finding.
4. **§9 observation-shape branches**: all four pre-spec'd with specific downstream implications (distinct shape across channels; shape matches matched-baseline = RTM dominates; phase-specific detrend failure; per-channel timing differences).

Plus the handoff defaults (5d primary window `[t+1, t+5]` + sensitivity arm `[t+6, t+10]`; t0 = episode-end primary + last-below-threshold-day sensitivity; pooled headline + per-phase descriptive).

**Status**: drafted, not locked. Lock requires explicit user acceptance. After lock, [`/research-review`](../../../reviews/README.md) must run in a fresh session (no shared drafting-session context); the review report lands in [`reviews/`](../../../reviews/) with the addendum *"Fresh session — no exposure to the drafting context; doc-only knowledge."*

---

**Pre-registration written 2026-06-15, BEFORE any trajectory inspection on the per-channel post-crash recovery shape.** Locked at user acceptance. Any subsequent change creates HA-P6-v2.

**This is Layer 1 descriptive characterisation per [CONVENTIONS §2.1](../../../CONVENTIONS.md#21-descriptive-before-inference), NOT a SUPPORTED / NOT-SUPPORTED inferential test.** P6 always produces a trajectory characterisation — the question is *what shape* the post-crash window has. The §5 "findings shape" is what the result.md will REPORT regardless of the actual data; the §9 "observation shape outcomes" are pre-spec'd downstream implications of each finding shape.

HA-P6 closes the post-crash side of the multi-scale dynamics framing from the [lived-experience braindump](../../../lived_experience_garmin_pacing_2026-06-14.md). The pre-crash side is covered by P2 / HA01b / HA11 / P4 / P5 / HA-C4b; the recovery side has been a gap until now. **P6 is also the load-bearing input to HA-P7's window-length assumption**: if P6 finds the recovery period extends to 14 days or beyond, P7's 14d-recent-crash-density window is empirically validated; if recovery completes within ~5 days and the post-window is a generic gap day, P7's 14d window is a generic period, not a crash-specific one.

## 1. Claim

### 1.1 Primary (descriptive characterisation)

In the LC era (`date >= 2022-04-04`), for each of the 7 channels listed in §4.1, the per-day median + IQR trajectory across days `[t+1, t+5]` after crash_v2 episode-end (t0) **differs in shape** from a matched non-crash trajectory on at least one of three dimensions:

- **Depth** — magnitude of the per-channel deviation from the lagged baseline at the minimum
- **Duration** — number of days until the channel returns to within 0.5 SD of the lagged baseline
- **Completeness** — fraction of the lagged-baseline level recovered by t+5

The matched non-crash trajectory is computed in **two parallel arms** (Option C): (a) matched-deep-trough non-crash days (strict RTM control); (b) lagged personal baseline per [CONVENTIONS §3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses). Both arms are reported; concordance across arms increases confidence in the recovery-shape characterisation; divergence is documented as a methodological finding.

### 1.2 Secondary (correlational sub-hypothesis)

For the descriptive characterisation outputs from §1.1, **Spearman correlations are reported with block-bootstrap 95% CIs** between:

- Per-episode recovery-rate (slope on `[t+1, t+5]`) AND same-episode crash duration (days)
- Per-episode recovery-completeness (% return to lagged baseline by t+5) AND next-crash interval (days to next crash_v2 episode start)

The secondary is **correlational descriptive only — NO SUPPORTED bar**. Block-bootstrap CIs at `E[L] = 7` days per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) handle the autocorrelation that would otherwise inflate apparent significance. The secondary's role is to surface whether the recovery-shape characteristics carry information about the broader crash dynamics, not to test a specific predictive claim.

### 1.3 Tertiary (descriptive late-recovery sensitivity arm)

Same shape characterisation as §1.1, applied to days `[t+6, t+10]`. Reports whether the recovery has continued beyond t+5 OR has plateaued. Descriptive only.

---

## 2. Why we think this

- **Lived experience prior**. From the [lived-experience braindump](../../../lived_experience_garmin_pacing_2026-06-14.md): *"and just after a crash?"* is explicitly raised as an underexplored timescale. The multi-scale dynamics framing (*"strings of crashes, response to a previous longer period of ineffective pacing"*) motivates examining what happens AFTER a crash, not just before. P6 closes this gap.
- **PEM recovery-debt mechanism**. The biological story: PEM recovery is a multi-day autonomic re-equilibration process; recovery completeness plausibly mediates next-crash risk. If a crash is followed by partial-only recovery, the post-crash window itself becomes an elevated-risk window. This mechanism predicts P7's positive direction; P6 is its descriptive sibling.
- **Wiggers H5 — lag order** ([wiggers_testable_hypotheses.md#h5](../../../wiggers_testable_hypotheses.md#h5--each-metric-has-a-characteristic-lag-vs-exertion-lags-differ-by-metric), PDF lines 925-928): *"HRV drops after several days of overexertion ... even if the person rested well immediately after."* Implies a multi-day post-event autonomic tail with channel-specific characteristic lags. P6's per-channel timing characterisation (§1.1 duration) is the descriptive sibling of Wiggers H5.
- **Aitken et al. 2026** supports wearable signals as lagging indicators of subjective state (queued in [`_pending_literature_fetch.md`](../../../methodology/_pending_literature_fetch.md)).
- **Sibling project context**. The project has documented dose-confirmed responses on `stress_mean_sleep`, `all_day_stress_avg`, and `bb_lowest` per [citalopram_dose_response §5.6](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14). The recovery-shape question intersects with this: per-channel recovery shape may differ across Citalopram phases as a downstream consequence of the dose-response. The phase-stratified sensitivity arm in §4.7 addresses this.
- **Cheapest test in the queue alongside P7**. No FIT extraction; uses existing per-day columns + crash labels.

## 3. Data sources

- **Crash labels**: `crash_v2` scheme defined in [`crash_v2-definition/definition.md`](../crash_v2-definition/definition.md); the labels CSV `labels_crash_v2.csv` lives at `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv` (gitignored external data path) and is propagated into `per_day_master.csv` as the `is_crash` boolean column by the [`build_unified_dataset.py`](../../../pipeline/03_consolidate/build_unified_dataset.py) pipeline. Episode-level boundaries (start, end, duration) are derived from contiguous `is_crash == True` runs.
- **Per-day channels**: from `per_day_master.csv`. The 7 channels in §4.1.
- **Phase membership**: `dose_plasma_mg` column in `per_day_master.csv` (PK-smoothed per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification)); phase derivable from the date via the `citalopram_phase(d)` function in that MD §3.
- **Analysis window**: LC era pooled (no train/validate split — descriptive characterisation does not need held-out validation per the [hypothesis_lock_process MD](../../../methodology/hypothesis_lock_process.md)). Per-phase n estimates given in §4.7.
- **Episode count**: **29 LC-era crash_v2 episodes** — predicate: contiguous `is_crash == True` runs from `per_day_master.csv` restricted to dates >= 2022-04-04 and <= 2026-06-05; source: `labels_crash_v2.csv` via `per_day_master.csv`. n=29 documented in [`personal_hypotheses.md` P6 register entry caveat 2](../../../personal_hypotheses.md).

**No FIT extraction required.** All inputs are existing per-day columns in the consolidated master.

## 4. Measurement protocol

### 4.1 Channel set (locked)

Seven channels per phase, ordered by mechanism family:

| channel | dose-response status | family |
|---|---|---|
| `stress_mean_sleep` | CONFIRMED dose-modulated (β=+0.43/mg in buildup post-CPAP) | autonomic-load |
| `all_day_stress_avg` | CONFIRMED dose-modulated (β=+0.57/mg; strongest channel) | autonomic-load |
| `bb_lowest` | CONFIRMED dose-modulated (β=-1.13/mg) | recovery |
| `bb_overnight_gain` | partial (no buildup data; coverage starts 2024-09-18) | recovery |
| `resting_hr` | weak (consistent direction, near-significance) | cardiovascular |
| `gevoelscore` | outcome-channel (per [intervention_effects §3b](../../../methodology/intervention_effects_descriptive.md#3b-outcome-channel-contamination-check-gevoelscore)) — outcome contamination check | felt-state |
| `stress_low_motion_min_count_S60_Mlow` | indirectly dose-modulated (raw stress threshold) | autonomic-load (concurrence pattern) |

**Channel coverage caveats** (apply per phase):
- `bb_overnight_gain` is NaN before 2024-09-18 (~64% of LC-era days). For pre-2024-09-18 crash episodes, this channel emits NaN; the trajectory characterisation skips this channel for those episodes. Per-episode n's per channel reported in §10.1 dry-run.
- `gevoelscore` is the OUTCOME-channel; per [intervention_effects §3b](../../../methodology/intervention_effects_descriptive.md#3b-outcome-channel-contamination-check-gevoelscore), reading its trajectory is methodologically distinct from reading baseline channels. P6 reports `gevoelscore` trajectory as the **outcome-shape companion** (does the felt-state recovery shape match the autonomic-channel recovery shape?), NOT as a sibling baseline channel.
- `stress_low_motion_min_count_S60_Mlow` is the Session E primitive (commit `14a32a3`); 1722 valid days; coverage matches the stress-sample availability.

`n_minutes_resp_above_18` (Session E respiration companion) is queued for v2 (orthogonal to other channels; would add a respiration trajectory arm).

### 4.2 Window definition (locked)

- **Primary window**: `[t+1, t+5]` after `t0` (5 days). Matches the register entry.
- **Sensitivity arm**: `[t+6, t+10]` after `t0` (late-recovery; 5 days). Reports whether recovery has continued or plateaued beyond t+5.
- **Pre-event window for matched-baseline construction**: `[t0 - 90, t0 - 30]` (the standard lagged-personal-baseline window per CONVENTIONS §3.2).

### 4.3 t0 anchor (locked)

- **Primary t0 = crash_v2 episode-end** (first day after the episode where `gevoelscore` returns above the crash_v2 threshold for the episode-end-defining number of consecutive days).
- **Sensitivity t0 = last-below-threshold-day** within the episode (the lowest-felt-state day; if multiple tied days, the last one).
- Both anchors reported; concordance increases confidence; divergence documented as t0-sensitivity finding.

### 4.4 Matched-baseline construction Arm A — matched deep-trough non-crash days (locked)

For each crash episode `i` with episode-end day `t0_i`:

1. **Extract pre-crash trajectory**: gevoelscore on `[t0_i - 10, t0_i - 1]` (10 days before episode-end; covers the in-episode period + a brief pre-episode lead-in).
2. **Find candidate matched days**: LC-era days `d_match` that satisfy ALL of:
   - `d_match` is NOT in any crash_v2 episode within the surrounding `[d_match - 20, d_match + 10]` window
   - gevoelscore trajectory on `[d_match - 10, d_match - 1]` is within ±1 absolute gevoelscore-point of the crash episode's `[t0_i - 10, t0_i - 1]` trajectory at every aligned day (i.e. matched-pair similarity criterion)
   - `d_match` is in the same Citalopram phase as `t0_i` (per §4.7)
3. **If multiple candidates**: pick the one with smallest mean-absolute-deviation from the crash episode's pre-trajectory.
4. **If no candidates within ±1 gevoelscore-point**: relax to ±1.5, ±2 in sensitivity arms; if still no match → flag episode as "no Arm A control available"; that episode contributes only to Arm B.
5. **Matched control trajectory**: per-channel value on `[d_match + 1, d_match + 5]` (mirrors the crash's `[t0_i + 1, t0_i + 5]`).

Arm A is the **strict RTM control**: for each crash episode, the matched non-crash day's recovery trajectory shows what RTM-driven post-trough recovery looks like ABSENT a crash mechanism. If the crash's recovery trajectory matches the Arm-A trajectory, RTM dominates.

### 4.5 Matched-baseline construction Arm B — lagged personal baseline (locked)

For each crash episode `i`:

1. **Lagged-baseline window**: `[t0_i - 90, t0_i - 30]` per CONVENTIONS §3.2.
2. **Restrict to LC-era days** (`_lagged_lcera` discipline): exclude pre-2022-04-04 days from the baseline window.
3. **Restrict to same-phase days** per [phase_stratification §5.A](../../../methodology/citalopram_phase_stratification.md#5a-per-phase-stratification-the-default-lowest-risk).
4. **Restrict to non-crash days within the baseline window** (exclude `is_crash == True` days).
5. **Compute per-channel baseline statistics**:
   - **Baseline median** (μ_ch): trimmed mean (10/90 cut) of the channel's value across eligible baseline days.
   - **Baseline SD** (σ_ch): stdev of the same trimmed values.
   - Computed only when ≥ 40 of 60 eligible baseline days are valid AND same-phase.
6. **Per-channel z-score recovery shape**: `z_ch(t0_i + k) = (channel(t0_i + k) - μ_ch) / σ_ch` for k ∈ {1, 2, 3, 4, 5}.
7. **Recovery completeness**: `% return = abs(channel(t0_i + 5) - channel(t0_i)) / abs(μ_ch - channel(t0_i))` — fraction of the deviation from baseline that has been recovered by t+5.

Arm B is the **standard project-pattern control** matching the rest of the corpus.

### 4.6 CONVENTIONS §3.7 trajectory-detrend sensitivity (binding)

Per [CONVENTIONS §3.7](../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons): for each channel × phase × matched-baseline-arm, report a **detrended sensitivity arm**:

1. Fit a linear trend on the pre-crash baseline window `[t0_i - 90, t0_i - 30]` per channel.
2. Extrapolate the fitted line forward through the post-crash window `[t0_i + 1, t0_i + 5]` (and the late-recovery arm `[t0_i + 6, t0_i + 10]`).
3. Subtract the extrapolated line from both pre and post values.
4. Recompute the per-channel trajectory and the §1.1 depth / duration / completeness metrics on the residuals.
5. **Reading**: if the recovery shape SURVIVES detrending (the trajectory metrics are similar to the raw arm), the post-crash trajectory is genuinely event-driven (the crash); if the trajectory FAILS detrending (becomes a flat residual line), the apparent recovery was just the LC recovery trajectory continuing.

§3.7 binding applies because P6's central comparison is "recovery trajectory" vs "baseline" — structurally a pre-vs-post comparison on the LC frame. The detrend sensitivity is reported per (channel × phase × matched-baseline-arm) cell; the result table is dense but the §3.7 audit hook is firmly engaged.

### 4.7 Phase-stratified arm (descriptive only)

Per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification), report per-phase verdicts:

| phase | window | n estimate (crash episodes) |
|---|---|---|
| unmedicated | LC start 2022-04-04 → 2024-04-08 | ~10-15 |
| buildup (post-CPAP-buffer 2024-04-30+) | 2024-04-30 → 2024-06-19 | ~1-3 |
| consolidation (30mg plateau) | 2024-06-20 → 2026-03-19 | ~10-15 |
| afbouw + post-afbouw (merged) | 2026-03-20 → 2026-06-05 | ~1-3 |

Per-phase n's are estimates; actual counts gate at the §10.1 dry-run.

**Per-phase reporting is descriptive only.** Wide CIs expected for low-n phases; the *shape* differences are the finding, not the magnitude. The pooled-LC headline (the median trajectory aggregated across all 29 episodes) is the headline shape characterisation; per-phase shapes are reported alongside.

**Important per dose-response framework**: P6 caveat 5 in the register narrowed the v3 dose-response finding's impact on P6 specifically — three channels (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`) inherit a recovery-shape calibration concern across the entire Citalopram-traject (2024-04 → ongoing). Per-phase reporting addresses this directly; the §3.7 detrend per phase is the within-phase calibration check.

### 4.8 Statistical machinery — descriptive trajectory + block-bootstrap CIs (locked)

#### 4.8.1 Per-channel per-day per-phase trajectory

For each (channel × phase × matched-baseline-arm × detrend-arm) cell:

- Compute per-day median + IQR across the per-episode trajectories at days `[t+1, t+5]` (primary) and `[t+6, t+10]` (sensitivity).
- Compute 95% CIs on the per-day median via **stationary-bootstrap at `E[L] = 7` days** per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). Wilson CIs are NOT used (Wilson assumes i.i.d.; per-episode trajectories on the same channel are not independent across crashes that span the same season / phase / pacing-state).
- Block lengths drawn from Geometric(1/7); `B = 10,000` resamples; report percentile CI.
- **Data-driven `E[L]*` companion** per the methodology MD's "Operational consequences" §2: compute the data-driven block-length estimator on each channel's pre-crash baseline values within the pooled LC eligible-episode pool. **Report rule**: if `|E[L]* − 7| / 7 > 0.5` (outside `[3.5, 10.5]` days) for any channel, **flag for review before locking the finding shapes**.
- Individual-event traces (n=29 faint lines) overlaid on the median + IQR band per channel.

#### 4.8.2 Per-channel recovery-completion-day estimate

Per channel × phase × matched-baseline-arm: the **median day at which the channel returns to within 0.5 SD of the lagged baseline**. If no episode's trajectory returns within 0.5 SD by t+5, report "not within window" + median residual at t+5. If recovery is complete by t+1 (median trajectory already within 0.5 SD), report "complete by t+1" + median trajectory at t+1.

#### 4.8.3 Per-channel qualitative shape descriptions per phase

For each (channel × phase) cell, classify the median trajectory shape as one of: `monotonic-recovery`, `stair-step-recovery`, `overshoot-then-settle`, `slow-grind-incomplete`, `no-meaningful-change`, `noisy-inconclusive`. **Pre-spec for `no-meaningful-change` classification**: ALL of (a) per-day median deviation from lagged baseline < 0.3 SD for all 5 days, (b) per-day block-bootstrap CI overlap with baseline > 50%, (c) §3.7 detrend residual flat.

#### 4.8.4 Secondary correlational sub-hypothesis (block-bootstrap CIs)

For each channel × phase × matched-baseline-arm × {recovery-rate, recovery-completeness}:

- **Recovery rate**: per-episode slope of the channel's trajectory on `[t+1, t+5]` via OLS.
- **Recovery completeness**: per-episode `% return to lagged baseline by t+5` (per §4.5 formula).
- **Per-episode crash duration**: number of `is_crash == True` days in the episode (from contiguous-run detection).
- **Per-episode next-crash interval**: days from `t0` to the next crash_v2 episode start (NaN if no subsequent episode within LC era; reported as right-censored).
- **Spearman correlation** between (recovery-rate, crash-duration) and (recovery-completeness, next-crash-interval), per cell.
- **Block-bootstrap 95% CI** at `E[L] = 7` days per the methodology MD. Per-episode resampling within phase; B = 10,000.
- **CI containing 0 → null correlation read**; otherwise report sign + magnitude.
- **No SUPPORTED bar**. This is descriptive correlation, not an inferential test.

---

## 5. Pre-registered findings shape (NOT a falsification criterion)

Per the lock-process MD §3.5 + the handoff §4.5: P6 is descriptive; there is NO SUPPORTED / NOT-SUPPORTED bar. The §5 section enumerates what the **result.md will report regardless of the actual data**:

1. **Per-channel per-day median + IQR + individual-event traces** for each of the 7 channels × {pooled LC, 4 phases} × 2 matched-baseline-arms × 2 detrend-arms × 2 window-arms (primary 5d + late-recovery 5d) × 2 t0-anchors. Result CSV emits one row per (channel, phase, baseline_arm, detrend_arm, window_arm, t0_anchor, day_offset) cell with median, IQR, individual-trace count, and block-bootstrap 95% CI.
2. **Per-channel recovery-completion-day estimate** (§4.8.2): median day to return within 0.5 SD of lagged baseline per channel × phase × matched-baseline-arm.
3. **Per-channel qualitative shape description** (§4.8.3): the classified shape per channel × phase, with the `no-meaningful-change` pre-spec applied.
4. **§3.7 detrended sensitivity** per (channel × phase × matched-baseline-arm) cell.
5. **Secondary correlational sub-hypothesis** outputs (§4.8.4): Spearman correlations with block-bootstrap CIs for (recovery-rate, crash-duration) and (recovery-completeness, next-crash-interval) per channel × phase × matched-baseline-arm.
6. **Concordance / divergence reads**: Arm A (matched-deep-trough) vs Arm B (lagged baseline) concordance per (channel × phase) cell. Divergence flagged as methodological finding per §9.
7. **t0-sensitivity concordance**: episode-end-t0 vs last-below-threshold-day-t0 concordance per (channel × phase × matched-baseline-arm) cell. Divergence flagged.

The result.md leads with a per-channel summary table (7 rows × pooled LC × primary-baseline-arm × no-detrend) for headline trajectory readings; the full multi-arm table is in the result CSV.

---

## 6. Exclusion rules

- **Crash episodes outside the LC era** (`t0 < 2022-04-04` OR `t0 > 2026-06-05`) excluded.
- **Crash episodes whose `[t0+1, t0+5]` window extends beyond 2026-06-05 (data-cut)** are reported with truncated trajectories; the late-recovery arm `[t0+6, t0+10]` is reported with available data only.
- **Crash episodes within the 2024-04 boundary cluster** (`t0` in `[2024-04-09, 2024-04-16]`) excluded per [intervention_effects §8.1](../../../methodology/intervention_effects_descriptive.md#81-effective-analyzable-scope-5-of-8-boundaries-usable).
- **Buildup-phase episodes strictly before 2024-04-30** (first 21 days of buildup: 2024-04-09 through 2024-04-29 inclusive) excluded from the phase-stratified buildup arm (CPAP-end confound buffer). Included in the pooled LC headline with flag.
- **Crash episodes lacking lagged-baseline availability** (fewer than 40 of 60 same-phase eligible baseline days) excluded from Arm B; reported separately.
- **Crash episodes lacking matched-deep-trough candidates** (no Arm A match within ±2 gevoelscore-points after sensitivity relaxation) excluded from Arm A; reported separately.
- **Per-channel exclusions**: if a channel value is NaN at any of `[t+1, t+5]` or the lagged-baseline window has < 40 valid same-phase days for that channel, the channel × episode cell is excluded from the trajectory aggregation; reported in the dry-run.

## 7. Expected shape if hypothesis is true

Qualitative descriptions per channel (sanity-check ranges; not falsification criteria):

- **`stress_mean_sleep` and `all_day_stress_avg`**: median trajectory peaks at t0 (highest deviation from baseline), gradually decays toward baseline over 3-5 days. Recovery-completion-day estimate: t+3 to t+5 in unmedicated phase; possibly delayed in consolidation phase (per the dose-modulation caveat).
- **`bb_lowest`**: median trajectory at minimum on t0 (or t+1 if the floor is hit overnight); gradually rises toward baseline over 1-3 days. Recovery-completion-day estimate: t+1 to t+2.
- **`bb_overnight_gain`**: where available (post-2024-09-18 only), trajectory at minimum on t0+1 (the first night after the episode-end); recovery to baseline over 2-3 days.
- **`resting_hr`**: median trajectory at maximum (highest above baseline) on t0; gradually decays over 2-4 days. Wiggers H5 prediction: HRV-related channel has a longer characteristic lag than HR.
- **`gevoelscore`**: by construction of episode-end definition, gevoelscore returns to above-threshold ON the episode-end day. Trajectory on `[t+1, t+5]` is the *post-recovery* gevoelscore — should remain near or above baseline. Any dip indicates a "stair-step" recovery pattern (partial recovery + relapse).
- **`stress_low_motion_min_count_S60_Mlow`**: per Session E exploration, this channel correlates ρ=0.79 with stress-time channels; trajectory should mirror `all_day_stress_avg`.

**Sanity-check on episode count**: pooled LC n should be ~29 per the register. If pooled n is < 25 after exclusions OR > 35 → flag for review (the episode-detection algorithm may have changed; the dry-run should produce n=29 ± 2).

**Sanity-check on `E[L]*`**: if any channel's data-driven block-length estimator falls outside `[3.5, 10.5]` → flag for review per the methodology MD.

If sanity check fails on the dry-run, the spec needs review BEFORE running the full characterisation. The §10.1 dry-run is the gate.

## 8. Caveats result.md must explicitly acknowledge

- **Regression to the mean (RTM) is the central confound**. Crash days have low gevoelscore by definition; subsequent days regress toward the participant's mean by construction. Arm A (matched-deep-trough non-crash days) is the strict RTM control; if the crash's recovery trajectory matches the Arm-A trajectory on a channel × phase × detrend cell, RTM dominates that cell and the recovery shape is NOT autonomic-specific. **Result.md leads with the Arm A vs crash trajectory comparison per channel — this is the load-bearing read**.

- **n=29 LC-era episodes is sparse**. Per-channel per-day post-crash distributions have wide block-bootstrap CIs by construction. Descriptive characterisation is informative regardless; predictive sub-claims (§4.8.4) need careful framing — the CIs WILL be wide; reporting honestly is the discipline.

- **Crash_v2 episode boundaries depend on the t0 definition**. The §4.3 t0-sensitivity arm (episode-end-t0 vs last-below-threshold-day-t0) reports concordance; divergence between arms is a t0-sensitivity finding for downstream consumers.

- **Self-reported crash labels** via crash_v2. The label generator (`gevoelscore` self-report) has the same instrument-level bias as P7 caveat 5. Any systematic drift in self-reporting propagates into both the episode boundaries AND the §4.8.4 secondary correlations.

- **Intervention-baseline dose-response broadens P6's caveat** per [P6 register caveat 5](../../../personal_hypotheses.md) (substantively broadened from pre-v3 reading). Three channels (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`) are CONFIRMED dose-modulated; recovery-shape characterisation across the Citalopram-traject (2024-04 → ongoing) inherits a calibration concern on these channels. The §4.7 phase-stratified sensitivity arm + the §3.7 detrend per phase addresses this directly. `respiration_avg_sleep` is REJECTED dose-modulated (not in P6's panel; queued for v2). `resting_hr` is weakly dose-modulated (soft caveat).

- **Channel coverage gaps**. `bb_overnight_gain` starts 2024-09-18 (~64% of LC-era days NaN per [intervention_effects §2b](../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain)). Pre-2024-09-18 crash episodes contribute NaN to this channel; per-channel n's reported.

- **CONVENTIONS §3.7 trajectory-detrend is binding** per §4.6. Without §3.7 detrend, the apparent recovery shape may be the LC recovery trajectory (~10/year → ~2/year crash drop) continuing through the post-crash window. Phase-stratified detrend is the within-phase calibration check.

- **§3.4 inapplicable-to-primary by construction** (added per the [hypothesis_lock_process MD](../../../methodology/hypothesis_lock_process.md) §5 sanity check + the HA-P7 r2 audit-closure pattern). CONVENTIONS §3.4 crash-drop sensitivity binds correlations / regressions on PEM-pacing variables to report results with and without `is_crash == True` rows. **For HA-P6's primary descriptive trajectory characterisation**, §3.4 is **inapplicable by construction**: the trajectory IS computed across crash episodes; dropping `is_crash == True` rows would eliminate the entire test sample. **For the §4.8.4 secondary correlational sub-hypothesis** (recovery-rate vs crash-duration; recovery-completeness vs next-crash-interval), the correlation is at the per-episode-summary level, not per-day; `is_crash` is not a variable in the correlation. **The hook is therefore explicitly dispatched**: inapplicable-to-primary by-construction; inapplicable-to-secondary because the correlation operates on per-episode summary statistics, not per-day observations.

- **Matched-baseline construction (Arm A) is operational, not a gold-standard**. The ±1-gevoelscore-point matching tolerance is an operational choice; sensitivity arms at ±1.5 and ±2 report robustness. The matching does not control for unmeasured factors (life events, seasons, intervention transitions) that may co-occur with crashes; Arm B (lagged baseline) is the project-pattern complement.

- **The pre-crash window** (`t-N` to `t-1`) is explicitly **NOT IN SCOPE** for HA-P6 per the register entry. Pre-crash signals are covered by P2 / HA01b / HA11 / P4 / P5 / HA-C4b.

- **Mechanistic claims about recovery physiology are out of scope**. P6 characterises the *shape*; the *why* is for downstream hypothesis tests.

## 9. What we do with each observation shape

The §9 section enumerates pre-spec'd downstream implications per observation shape. **There are no SUPPORTED / NOT-SUPPORTED verdicts**; the result.md produces a trajectory characterisation, and the shape it produces triggers one or more of the following downstream propagations:

- **Distinct recovery shape across multiple channels (≥ 3 of 7 channels in the pooled LC × Arm-A × no-detrend cell show statistically-distinguishable median trajectory from matched control)** → **P6 has characterised a real post-crash signature**. Downstream propagations:
  - Update the [`crash_episode_descriptive.md`](../../../methodology/crash_episode_descriptive.md) MD with the empirical per-channel timing estimates from §4.8.2.
  - Emit a per-channel timing table (channel × phase × recovery-completion-day-estimate) for downstream hypothesis-test mechanism-matching.
  - Inform HA-P7's window-length assumption: if the median recovery-completion-day-estimate across channels falls within `[3, 5]` days, P7's 14d window is a *generic period covering recovery* + further; if it extends to 7-10+ days, P7's 14d window is *recovery-specific*.

- **Recovery shape matches matched-baseline (Arm A median trajectory) on the majority of (channel × phase) cells** → **RTM dominates; no autonomic-specific recovery signature distinguishable from generic-low-score-day recovery**. Downstream propagations:
  - P7's 14d window assumption is empirically validated as a *generic recovery period*, NOT a crash-specific one. The recovery-debt mechanism claim in P7's caveat 1 weakens (a NOT-SUPPORTED P7 verdict would have an additional explanation here).
  - The lived-experience "the days after a crash feel different" framing has limited empirical support at the autonomic-channel level. Document for the [garmin_pacing_practice.md](../../../methodology/garmin_pacing_practice.md) operational protocol.
  - Channel-specific exceptions (cells where the crash trajectory IS distinguishable from RTM) are flagged as individual findings worth follow-up.

- **Recovery shape fails §3.7 detrend on consolidation only (the consolidation-phase trajectory disappears under detrending; unmedicated and afbouw phases survive)** → **the consolidation-phase apparent recovery was the LC trajectory leaking through; the unmedicated baseline characterisation is the truthful one**. Downstream propagations:
  - The consolidation-phase recovery-completion-day estimates per channel are NOT useable as priors for downstream tests; only the unmedicated estimates are trustworthy.
  - The buildup-vs-afbouw asymmetry hypothesis being explored in [phase_stratification §8.4](../../../methodology/citalopram_phase_stratification.md#84-the-buildup-and-afbouw-magnitude-asymmetry-as-a-research-question) gains a documentation point: dose-state matters for the recovery-shape characterisation.
  - The §4.6 detrend per phase is the load-bearing read; the result.md leads with this when this finding pattern emerges.

- **Per-channel timing differences observed (≥ 2 channels show recovery-completion-day estimates differing by ≥ 2 days, e.g. bb_lowest recovers in 2 days while stress_mean_sleep recovers in 5)** → **flag for downstream mechanism-matching**. Downstream propagations:
  - Future hypothesis tests with a specific mechanism claim should pick the channel whose recovery timing matches the claimed mechanism (per Wiggers H5).
  - Update [`methodology/time_resolution.md` §2.3](../../../methodology/time_resolution.md) with per-channel timing notes — the situational-multi-day-window category gets per-channel timing anchors.
  - The recovery-completion-day table per channel becomes a reference asset for the project, queued for citation in subsequent pre-regs.

- **Arm A and Arm B baselines diverge substantially** (concordance < 50% of (channel × phase) cells) → **methodological finding worth documentation**. Document in §9 of the result.md; possibly investigate which arm is more trustworthy on this corpus + flag for the [hypothesis_lock_process MD](../../../methodology/hypothesis_lock_process.md) as a project-pattern question.

- **t0-sensitivity arms (episode-end vs last-below-threshold-day) diverge substantially** → **t0 definition matters**. Report which anchor produces the stronger / cleaner shape per channel. The crash_v2 episode-end definition might need refinement (queued for crash_v3).

- **Secondary correlational sub-hypothesis (§4.8.4) finds OR (CI excludes 0) on recovery-rate ↔ crash-duration** → **recovery shape carries information about same-episode dynamics**. Document; emit for the downstream P7 covariate-sensitivity (§4.5.4 of HA-P7) as a candidate non-`crash_count_14d` covariate.

- **Secondary correlational sub-hypothesis (§4.8.4) finds OR on recovery-completeness ↔ next-crash-interval** → **recovery debt is empirically supported**. Document; this is the strongest single result HA-P6 can produce, because it directly addresses the §1.2 secondary sub-hypothesis's predictive intent. Inform P7's recovery-debt-vs-shared-cause caveat 1 disambiguation.

- **Spec sanity-check fails on dry-run** (pooled n outside `[25, 35]`; any channel's `E[L]*` outside `[3.5, 10.5]`; bb_overnight_gain has zero post-2024-09-18 episodes) → DO NOT run the full characterisation. Document the failure in the dry-run report; revise the spec (creating HA-P6-v2 with audit trail).

## 10. Detection script architecture

The script is single-stage; no extraction required (labels + per-day channels both in `per_day_master.csv`).

### 10.1 Stage 1 — characterisation script (`HA-P6/script.py`, to be written in next session after audit)

Loads `per_day_master.csv` + derives `is_crash` episode boundaries (contiguous-run detection); applies §4.2 + §4.3 + §4.4 + §4.5 + §4.6 + §4.7 filters per (channel × phase × baseline_arm × detrend_arm × window_arm × t0_anchor) cell; computes per-day median + IQR + block-bootstrap CIs (§4.8.1) + recovery-completion-day estimates (§4.8.2) + qualitative shape classifications (§4.8.3) + secondary correlations (§4.8.4).

Outputs:
- `result.md` with headline summary table + per-channel trajectory plots (matplotlib) + per-phase qualitative descriptions + observation-shape outcome propagations per §9.
- `result.csv` with full multi-arm per-day-per-cell trajectory data.
- `plots/` folder with per-channel × phase trajectory PNGs (median + IQR band + individual traces).

### 10.2 Dry-run mode (`script.py --dry-run`)

Prints:
- Pooled-LC + per-phase episode counts after §6 exclusions.
- Per-channel × per-phase sample sizes (n episodes contributing to each cell).
- Data-driven `E[L]*` per channel (pooled LC) — flag if outside `[3.5, 10.5]`.
- Sanity-check ranges per §7 (n=29 ± 2 pooled; per-channel timing estimates roughly in expected ranges).

**If any sanity check fails → halt + revise spec → HA-P6-v2.**

### 10.3 Stage 2 — `result.md`

Headline section: per-channel summary table (7 rows × pooled LC × Arm-A × no-detrend) with median recovery-completion-day-estimate + qualitative shape + concordance vs Arm-A baseline.

Subsequent sections: per-phase tables; matched-baseline-arm comparison tables; §3.7 detrend sensitivity per cell; secondary correlational sub-hypothesis outputs; observation-shape outcome propagations per §9.

Caveats section per §8 + the §3.4 inapplicable-to-primary dispatch.

### 10.4 Run protocol

1. **Dry-run** (`python script.py --dry-run`): prints sample sizes + sanity checks per §7. **If sanity check fails → halt + revise spec → HA-P6-v2.**
2. **Full run** (`python script.py`): emits `result.md` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-P6-v2 with the v1 result archived (per the project's locked-pre-reg discipline + the [hypothesis_lock_process MD §3.8](../../../methodology/hypothesis_lock_process.md)).

Estimated test script length: ~400 lines (Python + statsmodels + scipy + matplotlib).

---

*Pre-registration drafted 2026-06-15 by Claude in reviewer-mode-with-authorization in the same session that drafted + locked [HA-C4b/hypothesis.md](../HA-C4b/hypothesis.md) (commit `80607e4`) and [HA-P7/hypothesis.md](../HA-P7/hypothesis.md) (commit `7f1ecc8`), and produced the [hypothesis_lock_process.md](../../../methodology/hypothesis_lock_process.md) retrospective. Lock requires user acceptance. Fresh-session `/research-review` audits after lock per CONVENTIONS §1.2.*
