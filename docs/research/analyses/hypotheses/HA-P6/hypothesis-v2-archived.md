# HA-P6 — Post-crash window distinctive autonomic-recovery shape (Personal-register, descriptive characterisation) — **v2**

## Authorship

**Drafted 2026-06-17 (v2)** by Claude (Opus 4.7 1M) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. v2 is a SUPERSESSION of v1 (LOCKED 2026-06-15, archived at [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md)) per [`hypothesis_lock_process.md §3.9 step 4`](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock): the v1 §10.4 dry-run on 2026-06-17 emitted a HALT verdict at the §7 E[L]\* sanity gate (HALT artefact archived at [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md); v1 implementation archived at [`script-v1-archived.py`](script-v1-archived.py)). v1 produced **no** `result.md`; the HALT diagnosed three named spec-precision issues addressed in this v2.

**Parent artefacts for v2**:
- v1 LOCKED [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md) (2026-06-15-r3, by user acceptance under option-A compression)
- v1 audit [`reviews/HA-P6-2026-06-15.md`](../../../reviews/HA-P6-2026-06-15.md) (fresh-session, REVISION RECOMMENDED → r2 closures absorbed)
- v1 HALT [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md) (2026-06-17, two channels FLAG on §7 sanity gate)
- v1 implementation [`script-v1-archived.py`](script-v1-archived.py) (2026-06-17, faithful to v1 §10 spec)

**The three closures addressed in v2** (named by the v1 test-execution session's report-back):

- **(c) §4.8.1 "pre-crash baseline values" input-pool interpretation** — v1's `sanity_checks()` chose the **concatenation interpretation**: per-channel input was the union of per-episode `[t0-90, t0-30]` LC-era same-phase non-crash baseline values across all 29 episodes, concatenated into one flat array. This produces artificial lag-1 discontinuities at every episode boundary and explains why four of seven channels returned the estimator's default 7 (the ACF of a concatenated mixed-time-source series has no clean cutoff). **v2 commits to interpretation (ii)**: the per-channel pooled-LC daily time series (LC era 2022-04-04 to data-cut, eligible-day filter applied, ordered by date). This matches HA-P7's `estimate_block_length(cc14)` usage at [HA-P7 `test.py` line 763](../HA-P7/test.py) on `cc14 = df.loc[mask_pool, "crash_count_14d"]`. The methodology MD's "Operational consequences" §2 in [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) frames E[L]\* as a property of the time series, not of an analysis subset; v2 is the consistent reading. See §4.8.1 for the v2 specification.

- **(a) §4.8.1 + §7 E[L]\* sanity-check policy refinement** — v1's §7 sanity policy treated the estimator's default 7 (returned as a fallback when the ACF was inconclusive or the closed-form formula degenerated) as PASS, mechanically equivalent to a verified real estimate. This was honest at the level of bytes but not at the level of provenance. v2 replaces the binary FLAG / ok logic with a **three-verdict logic**: **PASS-real** (estimator returned a real value within [3.5, 10.5]; use E[L]=7 default), **PASS-fallback** (estimator could not compute; default 7 used with a methodological flag in result.md naming the fallback reason per channel; proceeds), **FAIL** (estimator returned a real value outside [3.5, 10.5]; per-channel override using the rounded E[L]\* triggers, pre-specified per channel). The override mechanism extends the methodology MD's per-hypothesis-override clause to per-channel-within-a-hypothesis; v2's specification satisfies the MD's three conditions (ACF substantially different from 7; pre-registered before any test run; justified per channel). The MD itself does NOT need updating; v2 fits within the existing override clause. See §4.8.1 override table + §7 sanity logic + §8 autocorrelation-honesty caveat.

- **(b) §4.8.4 per-episode `recovery-completeness` threading** — v1 implementation gap diagnosed by the v1 test session: `run_cell` stored per-episode completeness as a median across episodes (`completeness_median`), not as a per-episode array; `secondary_correlations` hard-coded `completeness = float("nan")` per episode, producing an all-NaN array and n=0 in the §4.8.4 completeness Spearman. v2 specifies: **per-episode completeness is computed and stored as `completeness_per_episode` in the (channel × phase × baseline-arm × t0-anchor) cell during the §4.8.1 trajectory pass**; §4.8.4 reads the array directly. v2 additionally adds: (i) a **denominator-undefined exclusion rule** at §4.5 step 7 (`abs(μ_ch - channel(t0_i)) < ε = 0.5×σ_ch`; episodes with undefined completeness contribute to §1.1 trajectory but not to §1.2 completeness Spearman; their count is reported separately in §6 + §10.1); (ii) explicit **baseline-source disambiguation** at §4.8.4 (the single-cell-lock pooled-LC × Arm-A cell names the §1.1 trajectory-comparison baseline; the per-episode completeness denominator μ_ch is always from the **Arm-B lagged baseline** because Arm-A produces a matched-control trajectory, not a scalar baseline mean).

**Operationalisation choices carried forward from v1 unchanged**:

1. Sub-hypothesis scope (primary descriptive + secondary correlational, no SUPPORTED bar).
2. Channel set (7 channels per §4.1; `n_minutes_resp_above_18` remains queued for HA-P6-v3).
3. Matched-baseline construction (Option C: Arm A matched-deep-trough non-crash days + Arm B lagged personal baseline).
4. §9 observation-shape branches (all four pre-spec'd; the §9 head trigger-phrase binding from v1 r2 is unchanged).
5. Window definitions, t0 anchors, §4.6 detrend binding, §4.7 phase-stratified arm, §4.8.2 recovery-completion-day estimate, §4.8.3 algorithmic shape classifier (six categories, first-match priority).
6. §8 caveats minus the new (a) autocorrelation-honesty bullet and (b) completeness-source-disambiguation bullet added in v2.
7. §6 exclusion rules (with one addition per closure (b): undefined-completeness episodes excluded from §4.8.4 completeness Spearman only).
8. Single-cell headline lock for §9 bullets 7/8 (pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window) from v1 r2.

**Compression decision per [`hypothesis_lock_process.md §3.6`](../../../methodology/hypothesis_lock_process.md#36-re-audit-step-stage-4-of-the-arc)**: v2 closures are mechanical:
- (c) is a definitional pick between two interpretations with cross-reference to a sister test (HA-P7) and a methodology MD's stated framing
- (a) is a numeric-range policy refinement (three verdicts instead of two; per-channel override table with operational integer rounding)
- (b) is a threading-discipline statement + a definitional ε rule + a baseline-source disambiguation sentence

No architectural change (no new statistical machinery; no new SUPPORTED bar; no change to the four locked operationalisation choices; the descriptive-mode framing is unchanged). Per §3.6 acceptability criteria, **re-audit skipped, lock direct**. The v1 fresh-session audit at [`reviews/HA-P6-2026-06-15.md`](../../../reviews/HA-P6-2026-06-15.md) verified v1's architecture; v2 only refines the three closures listed above. The lock-commit message will cite §3.6 compression criteria explicitly.

**Audit recommendation #5 absorption check**: the v1 audit's strengthening recommendation #5 (per-phase minimum-n gate on §9 third-branch propagation) is **NOT** absorbed in v2 — the closures (a) (b) (c) walkthrough did not surface a per-phase n-gate threshold; #5 stays queued for HA-P6-v3 if it materially fires in the v2 test session's per-phase reads. The v1 audit's recommendation #6 (register-row pointer) was executed at v1 lock + will be updated to point at v2 at v2 lock per §3.8 gate 3.

**Status: LOCKED 2026-06-17 by user acceptance under option-A compression per §3.6.** The pre-registration is locked at the state of this file's HEAD on 2026-06-17. Further modifications create HA-P6-v3 with v2 archived per [`hypothesis_lock_process.md §3.9 step 4`](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). The next session writes / revises `script.py` per the v2 closures and runs the v1-defined §10.4 protocol (dry-run → halt-or-go → full run → result.md). **After v2 lock, [`/research-review`](../../../reviews/README.md) must run in a fresh session per [`feedback_pre_reg_writer_role.md`](C:/Users/Gebruiker/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_pre_reg_writer_role.md)**; the review report lands in [`reviews/`](../../../reviews/) at `HA-P6-2026-06-17-v2.md` (or the next available date stamp) with the addendum *"Fresh session — no exposure to the v2 drafting context; doc-only knowledge."*

---

**Pre-registration v2 written 2026-06-17, AFTER the v1 dry-run HALT but BEFORE any post-crash trajectory inspection on the per-channel recovery shape.** Locked at user acceptance. Any subsequent change creates HA-P6-v3.

**This is Layer 1 descriptive characterisation per [CONVENTIONS §2.1](../../../CONVENTIONS.md#21-descriptive-before-inference), NOT a SUPPORTED / NOT-SUPPORTED inferential test.** P6 always produces a trajectory characterisation — the question is *what shape* the post-crash window has. The §5 "findings shape" is what the result.md will REPORT regardless of the actual data; the §9 "observation shape outcomes" are pre-spec'd downstream implications of each finding shape. The v2 closures (a) (b) (c) refine the §4.8.1 / §4.8.4 / §7 machinery; the §1 + §5 + §9 framings are unchanged from v1.

HA-P6 closes the post-crash side of the multi-scale dynamics framing from the [lived-experience braindump](../../../lived_experience_garmin_pacing_2026-06-14.md). The pre-crash side is covered by P2 / HA01b / HA11 / P4 / P5 / HA-C4b; the recovery side has been a gap until now. **P6 is also the load-bearing input to HA-P7's window-length assumption**: if P6 finds the recovery period extends to 14 days or beyond, P7's 14d-recent-crash-density window is empirically validated; if recovery completes within ~5 days and the post-window is a generic gap day, P7's 14d window is a generic period, not a crash-specific one.

## 1. Claim

### 1.1 Primary (descriptive characterisation)

In the LC era (`date >= 2022-04-04`), for each of the 7 channels listed in §4.1, the per-day median + IQR trajectory across days `[t+1, t+5]` after crash_v2 episode-end (t0) **is characterised along three dimensions** (with the matched non-crash trajectory as comparator; "differs from comparator" reads bind to the §9 head operational binding):

- **Depth** — magnitude of the per-channel deviation from the lagged baseline at the minimum
- **Duration** — number of days until the channel returns to within 0.5 SD of the lagged baseline
- **Completeness** — fraction of the lagged-baseline level recovered by t+5

The matched non-crash trajectory is computed in **two parallel arms** (Option C): (a) matched-deep-trough non-crash days (strict RTM control); (b) lagged personal baseline per [CONVENTIONS §3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses). Both arms are reported; concordance across arms increases confidence in the recovery-shape characterisation; divergence is documented as a methodological finding.

### 1.2 Secondary (correlational sub-hypothesis)

For the descriptive characterisation outputs from §1.1, **Spearman correlations are reported with block-bootstrap 95% CIs** between:

- Per-episode recovery-rate (slope on `[t+1, t+5]`) AND same-episode crash duration (days)
- Per-episode recovery-completeness (% return to lagged baseline by t+5, **computed per the §4.5 step 7 formula with the v2 denominator-undefined ε = 0.5×σ_ch rule per channel; episodes with undefined completeness excluded from this correlation only**) AND next-crash interval (days to next crash_v2 episode start)

The secondary is **correlational descriptive only — NO SUPPORTED bar**. Block-bootstrap CIs at the per-channel `E[L]` determined by §4.8.1 (default 7 for PASS-real / PASS-fallback channels; per-channel override for FAIL channels) per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) handle the autocorrelation that would otherwise inflate apparent significance. The secondary's role is to surface whether the recovery-shape characteristics carry information about the broader crash dynamics, not to test a specific predictive claim.

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
- **Episode count**: **29 LC-era crash_v2 episodes** — predicate: contiguous `is_crash == True` runs from `per_day_master.csv` restricted to dates >= 2022-04-04 and <= 2026-06-05; source: `labels_crash_v2.csv` via `per_day_master.csv`. n=29 documented in [`personal_hypotheses.md` P6 register entry caveat 2](../../../personal_hypotheses.md). v1 dry-run confirmed n=29 with the v1 implementation's episode-detection (contiguous-run algorithm); see [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md) for the per-phase split (pooled 29; unmedicated 18; buildup 3; consolidation 6; afbouw 2; post_afbouw 0) and the episode roster (table of 29 rows with start/end/duration/phase/t0 per episode).

**Data-cut unchanged from v1**: as-of-date 2026-06-05. v2 does not advance the as-of-date.

**No FIT extraction required.** All inputs are existing per-day columns in the consolidated master.

## 4. Measurement protocol

### 4.1 Channel set (locked from v1; per-channel E[L] policy added in v2 §4.8.1)

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
- `bb_overnight_gain` is NaN before 2024-09-18 (~64% of LC-era days). For pre-2024-09-18 crash episodes, this channel emits NaN; the trajectory characterisation skips this channel for those episodes. Per-episode n's per channel reported in §10.1 dry-run. v1 dry-run confirmed 5 post-2024-09-18 episodes contribute to this channel.
- `gevoelscore` is the OUTCOME-channel; per [intervention_effects §3b](../../../methodology/intervention_effects_descriptive.md#3b-outcome-channel-contamination-check-gevoelscore), reading its trajectory is methodologically distinct from reading baseline channels. P6 reports `gevoelscore` trajectory as the **outcome-shape companion** (does the felt-state recovery shape match the autonomic-channel recovery shape?), NOT as a sibling baseline channel.
- `stress_low_motion_min_count_S60_Mlow` is the Session E primitive (commit `14a32a3`); 1722 valid days; coverage matches the stress-sample availability.

**v2 per-channel E[L] policy**: see §4.8.1 + §7. Each channel is assigned an E[L] verdict (PASS-real / PASS-fallback / FAIL) at the test-session dry-run; FAIL channels receive a pre-specified integer-rounded override per the §4.8.1 override table.

`n_minutes_resp_above_18` (Session E respiration companion) is queued for v3 (orthogonal to other channels; would add a respiration trajectory arm).

### 4.2 Window definition (locked from v1)

- **Primary window**: `[t+1, t+5]` after `t0` (5 days). Matches the register entry.
- **Sensitivity arm**: `[t+6, t+10]` after `t0` (late-recovery; 5 days). Reports whether recovery has continued or plateaued beyond t+5.
- **Pre-event window for matched-baseline construction**: `[t0 - 90, t0 - 30]` (the standard lagged-personal-baseline window per CONVENTIONS §3.2).

### 4.3 t0 anchor (locked from v1)

- **Primary t0 = crash_v2 episode-end** (first day after the episode where `gevoelscore` returns above the crash_v2 threshold for the episode-end-defining number of consecutive days).
- **Sensitivity t0 = last-below-threshold-day** within the episode (the lowest-felt-state day; if multiple tied days, the last one).
- Both anchors reported; concordance increases confidence; divergence documented as t0-sensitivity finding.

### 4.4 Matched-baseline construction Arm A — matched deep-trough non-crash days (locked from v1)

For each crash episode `i` with episode-end day `t0_i`:

1. **Extract pre-crash trajectory**: gevoelscore on `[t0_i - 10, t0_i - 1]` (10 days before episode-end; covers the in-episode period + a brief pre-episode lead-in).
2. **Find candidate matched days**: LC-era days `d_match` that satisfy ALL of:
   - `d_match` is NOT in any crash_v2 episode within the surrounding `[d_match - 20, d_match + 10]` window
   - gevoelscore trajectory on `[d_match - 10, d_match - 1]` is within ±1 absolute gevoelscore-point of the crash episode's `[t0_i - 10, t0_i - 1]` trajectory at every aligned day (i.e. matched-pair similarity criterion)
   - `d_match` is in the same Citalopram phase as `t0_i` (per §4.7)
3. **If multiple candidates**: pick the one with smallest mean-absolute-deviation from the crash episode's pre-trajectory.
4. **If no candidates within ±1 gevoelscore-point**: relax to ±1.5, ±2 in sensitivity arms; if still no match → flag episode as "no Arm A control available"; that episode contributes only to Arm B.
5. **Matched control trajectory**: per-channel value on `[d_match + 1, d_match + 5]` (mirrors the crash's `[t0_i + 1, t0_i + 5]`).

Arm A is the **strict RTM control**: for each crash episode, the matched non-crash day's recovery trajectory shows what RTM-driven post-trough recovery looks like ABSENT a crash mechanism. If the crash's recovery trajectory matches the Arm-A trajectory, RTM dominates. v1 dry-run reported 27/29 episodes matched within the ±2 tolerance ladder (15 at ±1.0, 12 at ±2.0); v2 retains the same tolerance ladder.

### 4.5 Matched-baseline construction Arm B — lagged personal baseline (locked from v1; v2 step-7 ε rule added)

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
7. **Recovery completeness — per-episode formula + v2 denominator-undefined rule**:
   - Formula: `% return = abs(channel(t0_i + 5) - channel(t0_i)) / abs(μ_ch - channel(t0_i))` — fraction of the deviation from baseline that has been recovered by t+5.
   - **Denominator-undefined rule (v2)**: completeness is **undefined** when `abs(μ_ch - channel(t0_i)) < ε` for `ε = 0.5 × σ_ch` (the threshold is per-channel-aware via σ_ch, so that low-σ channels like `gevoelscore` use a small ε proportional to their natural variability, while high-σ channels like `bb_overnight_gain` use a proportionally larger ε). Episodes with undefined completeness are still included in §1.1 trajectory aggregation (their raw recovery trajectory is informative) but are **excluded from the §4.8.4 completeness Spearman** for the channel where the rule fires (per-channel exclusion; an episode can be undefined-completeness for one channel and well-defined for another).
   - **Reporting**: the per-channel count of undefined-completeness episodes is reported separately in §6 + §10.1, alongside the missing-baseline-eligibility exclusion count (those are separate exclusion categories; an episode can be missing-baseline OR undefined-completeness, but the categories don't overlap because undefined-completeness requires a valid μ_ch).

Arm B is the **standard project-pattern control** matching the rest of the corpus.

### 4.6 CONVENTIONS §3.7 trajectory-detrend sensitivity (binding; locked from v1)

Per [CONVENTIONS §3.7](../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons): for each channel × phase × matched-baseline-arm, report a **detrended sensitivity arm**:

1. Fit a linear trend on the pre-crash baseline window `[t0_i - 90, t0_i - 30]` per channel.
2. Extrapolate the fitted line forward through the post-crash window `[t0_i + 1, t0_i + 5]` (and the late-recovery arm `[t0_i + 6, t0_i + 10]`).
3. Subtract the extrapolated line from both pre and post values.
4. Recompute the per-channel trajectory and the §1.1 depth / duration / completeness metrics on the residuals.
5. **Reading**: if the recovery shape SURVIVES detrending (the trajectory metrics are similar to the raw arm), the post-crash trajectory is genuinely event-driven (the crash); if the trajectory FAILS detrending (becomes a flat residual line), the apparent recovery was just the LC recovery trajectory continuing.

§3.7 binding applies because P6's central comparison is "recovery trajectory" vs "baseline" — structurally a pre-vs-post comparison on the LC frame. The detrend sensitivity is reported per (channel × phase × matched-baseline-arm) cell; the result table is dense but the §3.7 audit hook is firmly engaged.

### 4.7 Phase-stratified arm (descriptive only; locked from v1; v1 dry-run validated)

Per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification), report per-phase verdicts:

| phase | window | n (per v1 dry-run, post Sec-6 buildup CPAP buffer) |
|---|---|---:|
| unmedicated | LC start 2022-04-04 → 2024-04-08 | 18 |
| buildup (post-CPAP-buffer 2024-04-30+) | 2024-04-30 → 2024-06-19 | 3 |
| consolidation (30mg plateau) | 2024-06-20 → 2026-03-19 | 6 |
| afbouw + post-afbouw (merged) | 2026-03-20 → 2026-06-05 | 2 (0 in post_afbouw) |

v1 dry-run confirmed pooled n=29; the per-phase split is as reported above. **Per-phase reporting is descriptive only.** Wide CIs expected for low-n phases (buildup n=3; afbouw n=2); the *shape* differences are the finding, not the magnitude. The pooled-LC headline (the median trajectory aggregated across all 29 episodes) is the headline shape characterisation; per-phase shapes are reported alongside.

**Important per dose-response framework**: P6 caveat 5 in the register narrowed the v3 dose-response finding's impact on P6 specifically — three channels (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`) inherit a recovery-shape calibration concern across the entire Citalopram-traject (2024-04 → ongoing). Per-phase reporting addresses this directly; the §3.7 detrend per phase is the within-phase calibration check.

### 4.8 Statistical machinery — descriptive trajectory + block-bootstrap CIs

#### 4.8.1 Per-channel per-day per-phase trajectory + **v2 data-driven E[L]\* input + override policy**

For each (channel × phase × matched-baseline-arm × detrend-arm) cell:

- Compute per-day median + IQR across the per-episode trajectories at days `[t+1, t+5]` (primary) and `[t+6, t+10]` (sensitivity).
- Compute 95% CIs on the per-day median via **stationary-bootstrap at the per-channel `E[L]`** per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The per-channel `E[L]` is determined at the test session's dry-run per the §7 three-verdict logic + the v2 override table (below). Wilson CIs are NOT used (Wilson assumes i.i.d.; per-episode trajectories on the same channel are not independent across crashes that span the same season / phase / pacing-state).
- Block lengths drawn from Geometric(1/E[L]); `B = 10,000` resamples for headline cells; report percentile CI.
- Individual-event traces (n=29 faint lines) overlaid on the median + IQR band per channel.
- **Per-episode `completeness_per_episode` array stored in the cell during this trajectory pass** (closure (b)); read directly by §4.8.4. The per-episode value is computed per §4.5 step 7 (formula + v2 ε-undefined rule); undefined values are stored as NaN. Per-episode `raw_per_episode`, `z_per_episode`, `control_per_episode`, `completeness_per_episode` are all consistent-shape `(n_episodes, n_days)` (or `(n_episodes,)` for completeness, which is one scalar per episode).

##### v2 data-driven E[L]\* companion — interpretation (closure (c))

The data-driven E[L]\* estimator is run **once per channel** on the **pooled-LC daily time series of that channel**, with eligible-day filter:

- LC era only (`date >= 2022-04-04`, `date <= 2026-06-05`)
- Non-crash days only (`is_crash == False`)
- No same-phase restriction for the pooled-LC headline E[L]\* (the headline is pooled). Per-phase E[L]\* is also computed as a diagnostic with same-phase restriction added; per-phase E[L]\* values are reported in the dry-run but do NOT trigger the §7 override policy (the override policy operates on the pooled-LC E[L]\* per channel only — matches the cross-cell `E[L]` policy where one E[L] per channel is used across all phases for that channel's per-day median CIs).

This is **interpretation (ii)** per [`session-p6-v2-drafting-handoff-2026-06-17.md`](C:/Users/Gebruiker/.claude/plans/session-p6-v2-drafting-handoff-2026-06-17.md) closure (c). Rationale:
- The estimator (`compute_data_driven_block_length` / `estimate_block_length` in [`_utils/inference.py`](../../_utils/inference.py)) operates on the empirical ACF of an ordered time series; concatenating non-adjacent per-episode windows (the v1 interpretation) injects fake lag-1 discontinuities at every concat boundary, producing the "No clear ACF cutoff" / "Closed-form formula degenerate" fallback returns v1 observed for four of seven channels.
- HA-P7 [`test.py` line 763](../HA-P7/test.py) uses interpretation (ii) (`estimate_block_length(cc14)` on the pooled-LC crash_count_14d time series).
- The methodology MD's "Operational consequences" §2 in [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) frames E[L]\* as a property of the time series.
- Per-channel E[L]\* under interpretation (ii) is reproducible from a single ordered series + the estimator's documented procedure; (i) added a project-specific concatenation step not reflected anywhere in the methodology MD.

##### §7 three-verdict logic + per-channel E[L] override table (closure (a))

Replaces v1's binary FLAG / ok in [`script-v1-archived.py`](script-v1-archived.py) `sanity_checks()` with three verdicts. The verdict is assigned per channel based on the pooled-LC E[L]\* under interpretation (ii):

| verdict | trigger condition | per-channel E[L] used in §4.8.1 CIs | result.md flag |
|---|---|---:|---|
| **PASS-real** | estimator returned a numeric value `E[L]*` AND `3.5 <= E[L]* <= 10.5` | 7 (project default) | none — the data-driven companion certifies the default's reasonableness |
| **PASS-fallback** | estimator could not compute (ACF inconclusive, closed-form degenerate, n<30 baseline pool, or other documented fallback reason from `compute_data_driven_block_length`'s `note` field) | 7 (project default) | "PASS-fallback: estimator returned default 7 due to *<note>*; the default is operational, not a data-verified estimate" — surfaced per channel in result.md §3.7 detrend table + the §4.8.1 trajectory CIs |
| **FAIL** | estimator returned a numeric value `E[L]*` AND `E[L]* < 3.5 OR E[L]* > 10.5` | per-channel override per §4.8.1 override table below | "FAIL-override: pooled-LC E[L]\*=<value>; v2 override E[L]=<override> per §4.8.1 table" — surfaced per channel in result.md headline + §3.7 detrend table |

**PASS-fallback proceeds** (does NOT halt). The estimator returning the default 7 is mechanically equivalent to the project default, but its provenance ("estimator could not certify") is named in result.md so the reader does not mistake the fallback for a verified estimate.

**FAIL proceeds with the override** (does NOT halt). The override widens the per-channel CIs honestly per the channel's documented autocorrelation; the alternative (E[L]=7 + caveat) would produce false-conservative CIs that mask the channel's multi-day drift.

**Halt condition** (unchanged from v1): the script halts only on **structural** sanity-check failures — pooled n outside `[25, 35]`, `bb_overnight_gain` zero post-2024-09-18 episodes. The E[L]\* verdict no longer halts; the v2 three-verdict policy is the disposition.

##### Per-channel E[L] override table (closure (a))

Pre-specified at v2 lock. The override value is the integer-rounded `E[L]*` from the test-session dry-run under interpretation (ii) — i.e. the data-driven estimate is the override magnitude. The override is a **policy choice** (round to integer); the empirical magnitude comes from the test session and is reported in result.md alongside the override.

| channel | v2 disposition rule | rationale |
|---|---|---|
| `stress_mean_sleep` | use whichever verdict fires per the three-verdict logic. Expected PASS-real per v1 dry-run (E[L]\*=6.50 under interp (i)); under interp (ii) the daily-series ACF should still be cleanly within range. | dose-confirmed channel; daily-resolution stress signal; ACF expected to decay within a week. |
| `all_day_stress_avg` | if FAIL: **per-channel override E[L] = round(E[L]\*)** | Documented multi-day drift (autonomic-load family; dose-modulated β=+0.57/mg). The v1 (i)-interpretation E[L]\*=22.21 suggested the daily series has long ACF; the (ii)-interpretation should confirm or revise this. Honest CI inflation > false-conservative E[L]=7. |
| `bb_lowest` | use whichever verdict fires. Expected PASS-real under interp (ii) (real daily series; estimator should compute). | Recovery channel; daily-resolution overnight summary. |
| `bb_overnight_gain` | use whichever verdict fires. PASS-fallback likely on pre-2024-09-18 portion of the series (NaN-dominated → estimator may degenerate); the eligible-day filter (non-crash days) should give a smaller-n series for the post-2024-09-18 portion. | Coverage gap is the dominant constraint; the dry-run reports the eligible series length per channel. |
| `resting_hr` | use whichever verdict fires. Expected PASS-real under interp (ii). | Cardiovascular channel; daily-resolution. |
| `gevoelscore` | use whichever verdict fires. PASS-fallback or PASS-real depending on the daily series' ACF structure (the v1 fallback was due to closed-form degeneracy — interpretable as ACF passes through zero too quickly or too slowly to fit the closed-form). | Outcome channel; daily-resolution self-report. |
| `stress_low_motion_min_count_S60_Mlow` | if FAIL: **per-channel override E[L] = round(E[L]\*)** | Documented multi-day-correlated count metric (the Session E primitive); the v1 (i)-interpretation E[L]\*=30.72 suggested very high autocorrelation. The (ii)-interpretation re-derivation under the daily series + non-crash filter is the binding number. Honest CI inflation > false-conservative E[L]=7. |

**Cross-reference to the methodology MD's override clause**: per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) "Decision (proposed; pending user review)", per-hypothesis override is allowed when (i) the metric's empirical autocorrelation crosses zero at a lag substantially different from 7, (ii) the override is pre-registered in the hypothesis file before any test run, (iii) the override is justified in the hypothesis file with a 1-paragraph ACF readout. v2 satisfies all three for the FAIL-channel overrides: (i) the FAIL verdict gates on `|E[L]*-7|/7 > 0.5` which empirically operationalises "substantially different from 7"; (ii) v2 IS the pre-registration vehicle, the override table is locked at v2 lock before the test run; (iii) the test-session result.md will include the per-channel 1-paragraph ACF readout for each FAIL-channel override (the data-driven E[L]\* magnitude + the estimator note + the autocorrelation-class rationale). The methodology MD itself does NOT need updating; v2 fits within the existing clause.

The override extends the MD's per-hypothesis-override grammar to per-channel-within-a-hypothesis. This is a natural generalisation: a multi-channel hypothesis where channels have heterogeneous ACF structures should not be forced to one global E[L] for all channels; the MD's intent (cross-hypothesis comparability + p-hacking guard) is preserved because v2 pre-registers the per-channel policy at lock.

#### 4.8.2 Per-channel recovery-completion-day estimate (locked from v1)

Per channel × phase × matched-baseline-arm: the **median day at which the channel returns to within 0.5 SD of the lagged baseline**. If no episode's trajectory returns within 0.5 SD by t+5, report "not within window" + median residual at t+5. If recovery is complete by t+1 (median trajectory already within 0.5 SD), report "complete by t+1" + median trajectory at t+1.

#### 4.8.3 Per-channel qualitative shape descriptions per phase (locked from v1; algorithmic pre-specs)

For each (channel × phase) cell, classify the median trajectory shape into one of six categories. The classifier operates on the Arm-B lagged-baseline z-scored median trajectory `z_ch(t+k)` for k in {1, 2, 3, 4, 5} (per §4.5 step 6) with first-differences `dz(k) = z_ch(t+k) - z_ch(t+k-1)` for k in {2, 3, 4, 5} and per-day block-bootstrap 95% CIs from §4.8.1. Categories are evaluated in priority order; the FIRST matching category wins:

1. **`no-meaningful-change`** — ALL of (a) per-day median |z_ch(t+k)| < 0.3 for every k in {1..5}, (b) per-day block-bootstrap 95% CI on the median includes 0 on every k in {1..5}, (c) §3.7 detrend residual on the median trajectory has slope |beta| < 0.05 SD/day.

2. **`overshoot-then-settle`** — ALL of (a) the median trajectory CROSSES the lagged baseline within the primary window (a sign-change between `z_ch(t+k)` and `z_ch(t+k+1)` for at least one k in {1..4}), AND (b) the post-crossing absolute z stays < 0.5 for every day from the crossing to t+5 (lands at baseline; does not oscillate back across).

3. **`monotonic-recovery`** — ALL of (a) the first-differences `dz(2), dz(3), dz(4), dz(5)` are sign-consistent (all > 0 if z_ch(t+1) is negative; all < 0 if z_ch(t+1) is positive — i.e. consistent direction toward baseline), AND (b) either |z_ch(t+1)| - |z_ch(t+5)| >= 1.0 (recovers at least 1.0 SD across the window) OR |z_ch(t+5)| < 0.5 (lands within 0.5 SD of baseline by t+5).

4. **`stair-step-recovery`** — ALL of (a) |z_ch(t+1)| - |z_ch(t+5)| >= 0.5 (net progress toward baseline of at least 0.5 SD across the window), AND (b) at least one |dz(k)| < 0.15 (one or more "flat" days mid-window), AND (c) the remaining first-differences are sign-consistent toward baseline (the recovery is interrupted by a flat plateau but resumes; does NOT reverse).

5. **`slow-grind-incomplete`** — ALL of (a) |z_ch(t+5)| < |z_ch(t+1)| (net progress toward baseline), AND (b) |z_ch(t+5)| >= 0.5 (incomplete recovery; still > 0.5 SD from baseline at end of window), AND (c) the cell did not match categories 1-4 above.

6. **`noisy-inconclusive`** — fallback. Fires if (a) the per-day block-bootstrap 95% CI half-width is > 1.0 SD on >= 3 of 5 days, OR (b) none of categories 1-5 match (signature of an oscillating / non-monotonic / non-classifiable trajectory). If a cell is flagged as `noisy-inconclusive` AND condition (a) is satisfied, the cell is annotated `noisy-CI-driven`; if only (b) is satisfied, the cell is annotated `noisy-shape-driven`. Result.md surfaces the annotation alongside the category.

The classifier emits the matched category PER (channel × phase × matched-baseline-arm × detrend-arm × t0-anchor × window-arm) cell in the result CSV; §9 propagations cite the **pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window** headline cell per channel (per the §9 head single-cell lock).

#### 4.8.4 Secondary correlational sub-hypothesis — block-bootstrap CIs + **v2 per-episode completeness threading (closure (b))**

For each channel × phase × matched-baseline-arm × {recovery-rate, recovery-completeness}:

- **Recovery rate**: per-episode slope of the channel's trajectory on `[t+1, t+5]` via OLS on the per-episode z-scored trajectory (`z_per_episode` stored in the cell during §4.8.1).
- **Recovery completeness**: per-episode `completeness_per_episode` value stored in the cell during the §4.8.1 trajectory pass (closure (b)); computed per §4.5 step 7 formula with the v2 ε-undefined rule. **Episodes with undefined completeness (per the §4.5 step 7 ε rule) are excluded from the completeness Spearman for the channel where the rule fires**; their per-channel counts are reported in result.md alongside the n of the Spearman.
- **Per-episode crash duration**: number of `is_crash == True` days in the episode (from contiguous-run detection).
- **Per-episode next-crash interval**: days from `t0` to the next crash_v2 episode start (NaN if no subsequent episode within LC era; reported as right-censored).
- **Spearman correlation** between (recovery-rate, crash-duration) and (recovery-completeness, next-crash-interval), per cell.
- **Block-bootstrap 95% CI** at the per-channel `E[L]` from §4.8.1 (default 7 for PASS-real / PASS-fallback channels; override for FAIL channels). Per-episode resampling within phase; B = 10,000.
- **CI containing 0 → null correlation read**; otherwise report sign + magnitude.
- **No SUPPORTED bar**. This is descriptive correlation, not an inferential test.

##### v2 baseline-source disambiguation for the single-cell-locked completeness Spearman (closure (b))

The single-cell lock for §9 bullets 7/8 is **pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window** per the v1 r2 closure (carried forward unchanged). The Arm-A label names the **§1.1 trajectory-comparison baseline** (matched-deep-trough non-crash days) that the cell's trajectory is reported against. The per-episode `completeness_per_episode` denominator μ_ch is **always from the Arm-B lagged baseline** (Arm-B's `μ_ch` per §4.5 step 5), because:

- Arm A produces a per-episode matched-control **trajectory** (5 days of channel values from `[d_match+1, d_match+5]`), not a per-episode baseline **mean**.
- The §4.5 step 7 completeness formula requires `μ_ch` (a scalar baseline level) and `channel(t0_i)` (a scalar episode-end value). The scalar `μ_ch` is well-defined only from Arm-B (the lagged personal baseline).
- The two arms answer different questions: Arm-A asks "does the post-crash trajectory match RTM-only?"; Arm-B asks "does the post-crash trajectory return to the pre-crash baseline level?". Completeness binds to the Arm-B question by construction.

This disambiguation closes the v1 spec ambiguity flagged by the v1 test session ("the cell is locked but the baseline-source for per-episode completeness is not"). v2 resolves: **all per-episode completeness values use Arm-B μ_ch**, regardless of the cell's named §1.1 baseline-arm. The "pooled-LC × Arm-A × ..." single-cell-lock identifier names the §1.1 trajectory-comparison cell; the §1.2 completeness Spearman uses the per-episode array from that cell, with denominators from Arm-B μ_ch.

---

## 5. Pre-registered findings shape (NOT a falsification criterion; locked from v1)

Per the lock-process MD §3.5 + the handoff §4.5: P6 is descriptive; there is NO SUPPORTED / NOT-SUPPORTED bar. The §5 section enumerates what the **result.md will report regardless of the actual data**:

1. **Per-channel per-day median + IQR + individual-event traces** for each of the 7 channels × {pooled LC, 4 phases} × 2 matched-baseline-arms × 2 detrend-arms × 2 window-arms (primary 5d + late-recovery 5d) × 2 t0-anchors. Result CSV emits one row per (channel, phase, baseline_arm, detrend_arm, window_arm, t0_anchor, day_offset) cell with median, IQR, individual-trace count, and block-bootstrap 95% CI **at the per-channel E[L] determined by the v2 §4.8.1 three-verdict logic**.
2. **Per-channel E[L] verdict + value** (v2 closure (a)): one row per channel naming PASS-real / PASS-fallback / FAIL, the empirical `E[L]*`, the rationale per §4.8.1 override table, and the E[L] value used for that channel's per-day CIs.
3. **Per-channel recovery-completion-day estimate** (§4.8.2): median day to return within 0.5 SD of lagged baseline per channel × phase × matched-baseline-arm.
4. **Per-channel qualitative shape description** (§4.8.3): the classified shape per channel × phase, with the algorithmic priority-order pre-specs applied.
5. **§3.7 detrended sensitivity** per (channel × phase × matched-baseline-arm) cell.
6. **Secondary correlational sub-hypothesis** outputs (§4.8.4): Spearman correlations with block-bootstrap CIs for (recovery-rate, crash-duration) and (recovery-completeness, next-crash-interval) per channel × phase × matched-baseline-arm. **Per-channel undefined-completeness exclusion count** (v2 closure (b)) reported alongside each completeness-Spearman n.
7. **Concordance / divergence reads**: Arm A (matched-deep-trough) vs Arm B (lagged baseline) concordance per (channel × phase) cell. Divergence flagged as methodological finding per §9.
8. **t0-sensitivity concordance**: episode-end-t0 vs last-below-threshold-day-t0 concordance per (channel × phase × matched-baseline-arm) cell. Divergence flagged.

The result.md leads with a per-channel summary table (7 rows × pooled LC × primary-baseline-arm × no-detrend) for headline trajectory readings; the full multi-arm table is in the result CSV. The per-channel E[L] verdict table (#2 above) is reported in the result.md headline section, immediately after the trajectory summary.

---

## 6. Exclusion rules (locked from v1; v2 adds undefined-completeness)

- **Crash episodes outside the LC era** (`t0 < 2022-04-04` OR `t0 > 2026-06-05`) excluded.
- **Crash episodes whose `[t0+1, t0+5]` window extends beyond 2026-06-05 (data-cut)** are reported with truncated trajectories; the late-recovery arm `[t0+6, t0+10]` is reported with available data only.
- **Crash episodes within the 2024-04 boundary cluster** (`t0` in `[2024-04-09, 2024-04-16]`) excluded per [intervention_effects §8.1](../../../methodology/intervention_effects_descriptive.md#81-effective-analyzable-scope-5-of-8-boundaries-usable).
- **Buildup-phase episodes strictly before 2024-04-30** (first 21 days of buildup: 2024-04-09 through 2024-04-29 inclusive) excluded from the phase-stratified buildup arm (CPAP-end confound buffer). Included in the pooled LC headline with flag.
- **Crash episodes lacking lagged-baseline availability** (fewer than 40 of 60 same-phase eligible baseline days) excluded from Arm B; reported separately.
- **Crash episodes lacking matched-deep-trough candidates** (no Arm A match within ±2 gevoelscore-points after sensitivity relaxation) excluded from Arm A; reported separately.
- **Per-channel exclusions**: if a channel value is NaN at any of `[t+1, t+5]` or the lagged-baseline window has < 40 valid same-phase days for that channel, the channel × episode cell is excluded from the trajectory aggregation; reported in the dry-run.
- **Per-channel undefined-completeness exclusions (v2 closure (b))**: episodes with `abs(μ_ch - channel(t0_i)) < ε = 0.5 × σ_ch` for a given channel are excluded from the §4.8.4 completeness Spearman for THAT channel only; they remain included in the §1.1 trajectory aggregation. The per-channel count of undefined-completeness episodes is reported in the dry-run + the result.md §4.8.4 row. The categories don't overlap with missing-baseline (an undefined-completeness episode must have a valid μ_ch + σ_ch by definition).

## 7. Expected shape if hypothesis is true (locked from v1; v2 sanity-check ranges refined)

Qualitative descriptions per channel (sanity-check ranges; not falsification criteria):

- **`stress_mean_sleep` and `all_day_stress_avg`**: median trajectory peaks at t0 (highest deviation from baseline), gradually decays toward baseline over 3-5 days. Recovery-completion-day estimate: t+3 to t+5 in unmedicated phase; possibly delayed in consolidation phase (per the dose-modulation caveat).
- **`bb_lowest`**: median trajectory at minimum on t0 (or t+1 if the floor is hit overnight); gradually rises toward baseline over 1-3 days. Recovery-completion-day estimate: t+1 to t+2.
- **`bb_overnight_gain`**: where available (post-2024-09-18 only), trajectory at minimum on t0+1 (the first night after the episode-end); recovery to baseline over 2-3 days.
- **`resting_hr`**: median trajectory at maximum (highest above baseline) on t0; gradually decays over 2-4 days. Wiggers H5 prediction: HRV-related channel has a longer characteristic lag than HR.
- **`gevoelscore`**: by construction of episode-end definition, gevoelscore returns to above-threshold ON the episode-end day. Trajectory on `[t+1, t+5]` is the *post-recovery* gevoelscore — should remain near or above baseline. Any dip indicates a "stair-step" recovery pattern (partial recovery + relapse).
- **`stress_low_motion_min_count_S60_Mlow`**: per Session E exploration, this channel correlates ρ=0.79 with stress-time channels; trajectory should mirror `all_day_stress_avg`.

### v2 sanity-check verdicts (closure (a))

- **Sanity-check on episode count**: pooled LC n should be ~29 per the register. If pooled n is < 25 after exclusions OR > 35 → **halt** (the episode-detection algorithm may have changed; the dry-run should produce n=29 ± 2). v1 dry-run confirmed n=29.

- **Sanity-check on `E[L]*` per channel** (v2 three-verdict logic; interpretation (ii) — pooled-LC daily time series with eligible-day filter):
  - **PASS-real**: `3.5 <= E[L]* <= 10.5` → proceed with E[L]=7 for that channel; no flag.
  - **PASS-fallback**: estimator could not compute (e.g. ACF inconclusive, closed-form degenerate, n<30 in eligible pool) → proceed with E[L]=7 for that channel; **methodological flag in result.md** naming the fallback reason per channel. Does NOT halt.
  - **FAIL**: `E[L]* < 3.5 OR E[L]* > 10.5` → proceed with the per-channel override per §4.8.1 override table (integer-rounded `E[L]*` for the two `if FAIL` channels: `all_day_stress_avg`, `stress_low_motion_min_count_S60_Mlow`); for the other five channels, FAIL is unexpected under interpretation (ii) — if any of those FAIL, halt + revise spec → HA-P6-v3 (this is a v2-unexpected condition that the v2 spec does not pre-spec a per-channel override for).

- **Sanity-check on `bb_overnight_gain` post-2024-09-18 episode count**: must be ≥ 1. v1 dry-run confirmed 5. If 0 → halt + revise spec → HA-P6-v3.

If the sanity check halts on the dry-run, the spec needs revision BEFORE running the full characterisation. The §10.1 dry-run is the gate.

## 8. Caveats result.md must explicitly acknowledge

- **Regression to the mean (RTM) is the central confound**. Crash days have low gevoelscore by definition; subsequent days regress toward the participant's mean by construction. Arm A (matched-deep-trough non-crash days) is the strict RTM control; if the crash's recovery trajectory matches the Arm-A trajectory on a channel × phase × detrend cell, RTM dominates that cell and the recovery shape is NOT autonomic-specific. **Result.md leads with the Arm A vs crash trajectory comparison per channel — this is the load-bearing read**.

- **n=29 LC-era episodes is sparse**. Per-channel per-day post-crash distributions have wide block-bootstrap CIs by construction. Descriptive characterisation is informative regardless; predictive sub-claims (§4.8.4) need careful framing — the CIs WILL be wide; reporting honestly is the discipline.

- **Power-calc dispatch** (per [hypothesis_lock_process MD §3.2 step 4 / §3.8 gate 1](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)). Power calc inapplicable per Daza 2018 within-subject design (see [Daza 2018 PDF](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) for the within-subject counterfactual framing); additionally, HA-P6 is Layer 1 descriptive characterisation per [CONVENTIONS §2.1](../../../CONVENTIONS.md#21-descriptive-before-inference) with no SUPPORTED bar to power against. The block-bootstrap CIs per §4.8.1 are the inference machinery; their honest width at n=29 is the discipline.

- **Crash_v2 episode boundaries depend on the t0 definition**. The §4.3 t0-sensitivity arm (episode-end-t0 vs last-below-threshold-day-t0) reports concordance; divergence between arms is a t0-sensitivity finding for downstream consumers.

- **Self-reported crash labels** via crash_v2. The label generator (`gevoelscore` self-report) has the same instrument-level bias as P7 caveat 5. Any systematic drift in self-reporting propagates into both the episode boundaries AND the §4.8.4 secondary correlations.

- **Intervention-baseline dose-response broadens P6's caveat** per [P6 register caveat 5](../../../personal_hypotheses.md) (substantively broadened from pre-v3 reading). Three channels (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`) are CONFIRMED dose-modulated; recovery-shape characterisation across the Citalopram-traject (2024-04 → ongoing) inherits a calibration concern on these channels. The §4.7 phase-stratified sensitivity arm + the §3.7 detrend per phase addresses this directly. `respiration_avg_sleep` is REJECTED dose-modulated (not in P6's panel; queued for v3). `resting_hr` is weakly dose-modulated (soft caveat).

- **Channel coverage gaps**. `bb_overnight_gain` starts 2024-09-18 (~64% of LC-era days NaN per [intervention_effects §2b](../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain)). Pre-2024-09-18 crash episodes contribute NaN to this channel; per-channel n's reported. v1 dry-run confirmed 5 post-2024-09-18 episodes contribute.

- **CONVENTIONS §3.7 trajectory-detrend is binding** per §4.6. Without §3.7 detrend, the apparent recovery shape may be the LC recovery trajectory (~10/year → ~2/year crash drop) continuing through the post-crash window. Phase-stratified detrend is the within-phase calibration check.

- **§3.4 inapplicable-to-primary by construction** (added per the [hypothesis_lock_process MD](../../../methodology/hypothesis_lock_process.md) §5 sanity check + the HA-P7 r2 audit-closure pattern). CONVENTIONS §3.4 crash-drop sensitivity binds correlations / regressions on PEM-pacing variables to report results with and without `is_crash == True` rows. **For HA-P6's primary descriptive trajectory characterisation**, §3.4 is **inapplicable by construction**: the trajectory IS computed across crash episodes; dropping `is_crash == True` rows would eliminate the entire test sample. **For the §4.8.4 secondary correlational sub-hypothesis** (recovery-rate vs crash-duration; recovery-completeness vs next-crash-interval), the correlation is at the per-episode-summary level, not per-day; `is_crash` is not a variable in the correlation. **The hook is therefore explicitly dispatched**: inapplicable-to-primary by-construction; inapplicable-to-secondary because the correlation operates on per-episode summary statistics, not per-day observations.

- **Matched-baseline construction (Arm A) is operational, not a gold-standard**. The ±1-gevoelscore-point matching tolerance is an operational choice; sensitivity arms at ±1.5 and ±2 report robustness. The matching does not control for unmeasured factors (life events, seasons, intervention transitions) that may co-occur with crashes; Arm B (lagged baseline) is the project-pattern complement.

- **The pre-crash window** (`t-N` to `t-1`) is explicitly **NOT IN SCOPE** for HA-P6 per the register entry. Pre-crash signals are covered by P2 / HA01b / HA11 / P4 / P5 / HA-C4b.

- **Mechanistic claims about recovery physiology are out of scope**. P6 characterises the *shape*; the *why* is for downstream hypothesis tests.

### v2 caveat: per-channel E[L] override honest autocorrelation framing (closure (a))

- **Two channels are pre-spec'd for per-channel E[L] override on FAIL** (per §4.8.1 override table): `all_day_stress_avg` and `stress_low_motion_min_count_S60_Mlow`. The v1 dry-run under the v1-interpretation produced E[L]\*=22.21 and E[L]\*=30.72 respectively (both far outside [3.5, 10.5]); the v2-interpretation (pooled-LC daily time series, non-crash filter) will produce different numbers but these channels have **documented multi-day drift inherent to their construction**: `all_day_stress_avg` is an autonomic-load aggregate over the day's stress samples; `stress_low_motion_min_count_S60_Mlow` is a daily count metric where consecutive days share a large fraction of their input via the rolling-stress-state. Their daily-resolution ACF should be expected to decay slowly. **The v2 per-channel E[L] override widens these channels' per-day CIs honestly**; the alternative (false-conservative E[L]=7) would understate the channels' autocorrelation and inflate apparent precision. Per-day CIs on these two channels will be visibly wider than the other five channels' CIs in result.md — this is the honest reporting per the methodology MD's "robustness to non-stationarity" weighting.
- **Four channels may produce PASS-fallback** depending on the test session's daily-series ACF: `bb_lowest`, `bb_overnight_gain`, `resting_hr`, `gevoelscore`. The estimator returning the default 7 in PASS-fallback is **operational, not data-verified**; result.md must surface this per channel with the estimator's `note` field (the fallback reason) so the reader does not mistake the default 7 for a certified estimate. v1 dry-run produced PASS-fallback for these four under interpretation (i); the v2 interpretation (ii) should produce real estimates for `bb_lowest`, `resting_hr`, and `gevoelscore` (their daily series have well-defined ACFs); `bb_overnight_gain` may continue to PASS-fallback due to the coverage gap producing a small eligible pool.

### v2 caveat: completeness baseline-source disambiguation (closure (b))

- **The §4.8.4 completeness Spearman binds to Arm-B μ_ch regardless of the cell's named §1.1 baseline-arm**. The single-cell lock for §9 bullets 7/8 is `pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window`; the "Arm-A" label there names the §1.1 trajectory-comparison baseline (matched-deep-trough non-crash days). The per-episode `completeness_per_episode` value computed for the §4.8.4 Spearman uses the **Arm-B lagged baseline** μ_ch + σ_ch (per §4.5 step 5), because the completeness formula requires a scalar baseline level (which Arm-B provides) and Arm-A provides only a 5-day matched-control trajectory. Result.md surfaces this disambiguation in the §4.8.4 row header.
- **Undefined-completeness exclusion is per-channel**: an episode can be undefined-completeness for one channel (`abs(μ_ch - channel(t0_i)) < 0.5 × σ_ch` fires) and well-defined for another. The per-channel count of undefined-completeness episodes is reported alongside the n of the completeness Spearman for that channel. This is separate from the missing-baseline exclusion (an undefined-completeness episode must have a valid Arm-B μ_ch + σ_ch by definition).

## 9. What we do with each observation shape (locked from v1)

The §9 section enumerates pre-spec'd downstream implications per observation shape. **There are no SUPPORTED / NOT-SUPPORTED verdicts**; the result.md produces a trajectory characterisation, and the shape it produces triggers one or more of the following downstream propagations:

**Operational binding for the §9 first-branch trigger** ("statistically-distinguishable median trajectory from matched control"): per channel, the per-day block-bootstrap 95% CI on the median DIFFERENCE (crash trajectory minus matched-control trajectory, computed via the §4.8.1 paired stationary-bootstrap machinery at the **per-channel E[L]** from §4.8.1, B=10000) excludes 0 on **>= 2 of 5 primary-window days**. A sensitivity arm at the stricter **>= 3 of 5 days** threshold is reported alongside. The "channel is statistically distinguishable" predicate is evaluated PER channel; the "≥ 3 of 7 channels" gate in the first bullet then aggregates across channels. The trigger is evaluated only on the pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window cell per channel (per the single-cell lock below).

**Single-cell headline lock for §9 bullets 7 and 8 (secondary correlational propagations)**: the §4.8.4 secondary correlations are computed for every (channel × phase × matched-baseline-arm × detrend-arm) cell, but §9 bullets 7 and 8 fire on ONE pre-specified cell only — **pooled-LC × Arm-A × no-detrend × episode-end-t0 × primary-window**. All other cells are reported but cannot fire §9 bullets 7 or 8 independently. This matches the HA-C4b r2 + HA-P7 r2 single-cell-lock pattern per [hypothesis_lock_process MD §4.2 closure (a)](../../../methodology/hypothesis_lock_process.md#42-layer-3-substantive--multi-comparison-discipline). Cells outside the locked cell that show CI excludes 0 on §4.8.4 are reported in the result CSV under a `secondary_cell_signal` column but flagged as diagnostic-only.

- **Distinct recovery shape across multiple channels (≥ 3 of 7 channels in the pooled LC × Arm-A × no-detrend cell show statistically-distinguishable median trajectory from matched control, per the §9-head operational binding)** → **P6 has characterised a real post-crash signature**. Downstream propagations:
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

- **Spec sanity-check halts on dry-run** (pooled n outside `[25, 35]`; `bb_overnight_gain` zero post-2024-09-18 episodes; any of the five "PASS-real-expected" channels FAIL under interpretation (ii)) → DO NOT run the full characterisation. Document the failure in the dry-run report; revise the spec (creating HA-P6-v3 with audit trail).

## 10. Detection script architecture (locked from v1; v2 modifications to §10.1 + §10.2)

The script is single-stage; no extraction required (labels + per-day channels both in `per_day_master.csv`).

### 10.1 Stage 1 — characterisation script (`HA-P6/script.py`, to be written / revised in next session)

Loads `per_day_master.csv` + derives `is_crash` episode boundaries (contiguous-run detection); applies §4.2 + §4.3 + §4.4 + §4.5 + §4.6 + §4.7 filters per (channel × phase × baseline_arm × detrend_arm × window_arm × t0_anchor) cell; computes per-day median + IQR + block-bootstrap CIs at the **per-channel E[L] from §4.8.1** (§4.8.1) + recovery-completion-day estimates (§4.8.2) + qualitative shape classifications (§4.8.3) + secondary correlations with **per-episode completeness threaded from the cell** (§4.8.4).

**v2 implementation discipline notes for the test-session author**:
- The **`completeness_per_episode` array** must be computed and stored in the cell during the §4.8.1 trajectory pass (not in `secondary_correlations`); the array shape is `(n_eligible_episodes,)`, with NaN for episodes where the v2 ε-undefined rule fires.
- The **per-channel E[L] verdict** is computed once per channel in `sanity_checks()` using `compute_data_driven_block_length` on the **pooled-LC daily series** (interpretation (ii): channel time series, LC era, non-crash filter, no same-phase restriction for the pooled headline). The result is stored in a dict mapping channel → {verdict: PASS-real/PASS-fallback/FAIL, el_star: float-or-NaN, el_used: int, note: str}; the `el_used` value is then threaded into every `run_cell` call for that channel for the per-day CI bootstrapping.
- The **§4.5 step 7 ε rule** is per-channel-aware via σ_ch; `ε = 0.5 * baseline['sigma']` per (channel, episode) cell; per-episode completeness is set to NaN when the denominator falls under ε.
- **Halt conditions** are: pooled n outside [25, 35] (unchanged from v1); bb_overnight_gain zero post-2024-09-18 (unchanged from v1); any of the five "PASS-real-expected" channels (everything except `all_day_stress_avg` and `stress_low_motion_min_count_S60_Mlow`) returning FAIL (new in v2 — would indicate a spec mismatch).
- **No halt** on PASS-fallback for any channel; no halt on FAIL for the two pre-spec'd-override channels (`all_day_stress_avg`, `stress_low_motion_min_count_S60_Mlow`).

Outputs:
- `dry-run-report.md` per §10.2 (replaces the v1 archived dry-run report).
- `result.md` with headline summary table + **per-channel E[L] verdict table** (v2 §5 #2) + per-channel trajectory plots (matplotlib) + per-phase qualitative descriptions + observation-shape outcome propagations per §9.
- `result.csv` with full multi-arm per-day-per-cell trajectory data + per-channel `completeness_per_episode` arrays.
- `result-data.json` with per-cell payload including the v2 per-episode arrays.
- `plots/` folder with per-channel × phase trajectory PNGs (median + IQR band + individual traces).

### 10.2 Dry-run mode (`script.py --dry-run`)

Prints:
- Pooled-LC + per-phase episode counts after §6 exclusions.
- Per-channel × per-phase sample sizes (n episodes contributing to each cell).
- **Per-channel pooled-LC E[L]\* under interpretation (ii)** (v2 closure (c)) with verdict per §4.8.1 three-verdict logic + the estimator's `note` field per channel.
- **Per-channel undefined-completeness episode count** (v2 closure (b)) — separate from missing-baseline counts.
- Sanity-check ranges per §7 (n=29 ± 2 pooled; per-channel timing estimates roughly in expected ranges; E[L]\* per channel within [3.5, 10.5] for the five PASS-real-expected channels).

**If any halt sanity check fails → halt + revise spec → HA-P6-v3.** Halt is now narrower than v1: the two pre-spec'd-override channels (FAIL on `all_day_stress_avg` or `stress_low_motion_min_count_S60_Mlow`) do NOT halt; the other five channels FAILing would halt.

### 10.3 Stage 2 — `result.md`

Headline section: per-channel summary table (7 rows × pooled LC × Arm-A × no-detrend) with median recovery-completion-day-estimate + qualitative shape + concordance vs Arm-A baseline. **Immediately followed by the per-channel E[L] verdict table** per §5 #2: one row per channel naming PASS-real / PASS-fallback / FAIL, the empirical `E[L]*`, the rationale per §4.8.1 override table, and the E[L] value used for that channel's per-day CIs.

Subsequent sections: per-phase tables; matched-baseline-arm comparison tables; §3.7 detrend sensitivity per cell; secondary correlational sub-hypothesis outputs with **per-channel undefined-completeness exclusion counts**; observation-shape outcome propagations per §9.

Caveats section per §8 + the §3.4 inapplicable-to-primary dispatch + the v2 (a) autocorrelation-honesty bullet + the v2 (b) completeness-source-disambiguation bullet.

### 10.4 Run protocol

1. **Dry-run** (`python script.py --dry-run`): prints sample sizes + sanity checks per §7. **If any halt sanity check fails → halt + revise spec → HA-P6-v3.** PASS-fallback and pre-spec'd-override FAILs do NOT halt; the dry-run emits the verdicts and proceeds-ready.
2. **Full run** (`python script.py`): emits `result.md` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-P6-v3 with the v2 result archived (per the project's locked-pre-reg discipline + the [hypothesis_lock_process MD §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock)).

Estimated test script length: ~450 lines (v1 was ~1843 lines including report-emit; the v2 modifications add ~50 lines for completeness threading + the three-verdict E[L] logic + interpretation (ii) input construction, partially offset by simpler binary→ternary in sanity_checks).

---

*Pre-registration v2 drafted 2026-06-17 by Claude (Opus 4.7 1M) in reviewer-mode-with-authorization, in response to the v1 dry-run HALT on 2026-06-17 per [`session-p6-v2-drafting-handoff-2026-06-17.md`](C:/Users/Gebruiker/.claude/plans/session-p6-v2-drafting-handoff-2026-06-17.md). Lock requires user acceptance. Fresh-session [`/research-review`](../../../reviews/README.md) audits v2 after lock per CONVENTIONS §1.2 + [`feedback_pre_reg_writer_role.md`](C:/Users/Gebruiker/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_pre_reg_writer_role.md).*
