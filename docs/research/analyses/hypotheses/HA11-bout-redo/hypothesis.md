# HA11-bout-redo — Bout-level framework-validity reproduction of HA11 v1's SUPPORTED-on-train U-dip count signal

## Authorship

**Drafted 2026-06-22** by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem.

**Drafting trigger**: the bout-level cascade gate per the [research PM brief 2026-06-19](../../../../../.claude/plans/research-pm-brief-bout-level-recovery-pivot-2026-06-19.md) + the framework-validity discipline in [`methodology/bout_level_recovery_dynamics.md` §6](../../../methodology/bout_level_recovery_dynamics.md#6-framework-validity-discipline-the-mds-own-falsifier) (LOCKED `c57ff3f` 2026-06-21). The parent MD §6 names "any downstream HA pre-reg using this MD's operand must include the HA11 v1 reproduction check as a framework-validity gate"; HA11-bout-redo IS that check, formalised as a standalone HA pre-reg. The bout-extraction pipeline ([`pipeline/02_features/extract_stress_bouts.py`](../../../pipeline/02_features/extract_stress_bouts.py), LOCKED `d5b394c` 2026-06-22) landed yesterday, unblocking this draft.

**Verification log** (anchors the draft on the current state of the methodology + pipeline + HA11 v1 reference):

- Read parent MD `bout_level_recovery_dynamics.md` at worktree commit `c7e25cf`. §6 unchanged from lock-commit `c57ff3f`; §6.1 operand definition `bout_n_fast_recovery_day` (per-day count of bouts with `recovery_half_life ≤ 15 min` AND `tail_length ≤ 45 min`) confirmed verbatim; §6.2 three comparability bars confirmed verbatim; §5.5 unmedicated-stratum restriction confirmed verbatim; §6.3 per-bout-n reporting discipline confirmed verbatim.
- Read pipeline README at worktree commit `c7e25cf`. Column name `bout_n_fast_recovery_day` is the locked operand; emits `0` on valid days with no bouts; emits blank (NaN) on §3.4-invalid days; joined into `per_day_master.csv` via the extended `03_consolidate/build_unified_dataset.py`. The aggregation table confirms the operand definition is byte-identical to MD §6.1.
- Read HA11 v1 result.md at worktree commit `c7e25cf`. Train SUPPORTED at primary 4d × N_std=1.5 × one-sided elevated: **64.3%** crash-episode frequency, **+22.8 pp** discrimination, **median signed z = 2.168** — the reproduction targets the framework-validity gate references.

**Locked decisions at draft time** (the parent MD §6 names but does NOT pre-commit these; this pre-reg surfaces each, operationalises with rationale, and pre-commits at the choice):

1. **Contrast pool**: calm-day pool vs HA11 v1's null-pool reference dates (per HA11 v1 §4.9; n=200 random non-overlapping reference dates, seed `20260605`), z-scored against the participant's own lagged personal baseline per HA11 v1 §4.5. Rationale: this IS HA11 v1's contrast shape (the train SUPPORTED signal was the +22.8 pp discrimination between crash-episode 4d windows vs random non-crash reference 4d windows on z-scored `u_dip_count`); reproducing HA11 v1's signal requires reproducing HA11 v1's contrast, not a heavy-T-vs-calm-day contrast (that is HA-C4c substantive scope, not framework-validity). The "calm-day pool" of the parent MD §6 is operationalised as HA11 v1's null-pool reference dates restricted to the unmedicated stratum × train era, where "calm" inherits HA11 v1's null construction (random non-crash 4d windows satisfying §4.4 day-validity). Alternatives considered + rejected as primary: (a) calm-day pool vs heavy-T-day pool — different framing; this is HA-C4c, not framework-validity; (b) calm-day pool absolute count without contrast — loses the discriminative signal HA11 v1's verdict was built on; absolute counts alone cannot reproduce the +22.8 pp discrimination number.
2. **Comparability bars**: all three §6.2 bars are GATING. Verdict rule: PASSED if all three are met; PARTIAL if exactly two are met; FAILED if ≤1 is met. Rationale: parent MD §6.2 says "all three bars must be met for the framework-validity gate to clear; any single bar failing → framework-validity HALT". Majority-of-3 would relax the parent MD's discipline; this pre-reg honours the parent MD's stated rule. Alternatives considered + rejected as primary: (a) directional gating only with effect-size + p-value as warnings — relaxes the parent MD; (b) majority-of-3 — same; (c) all-three gating but with PARTIAL band reported descriptively — adopted, but the verdict on the framework-validity gate is binary PASSED/PARTIAL/FAILED and only PASSED unblocks HA-C4c without caveat per §9.
3. **Block-permutation E[L]**: E[L]=7 days inherited from [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), per parent MD §5.1 inheritance discipline. HA11-bout-redo reports the data-driven E[L]\* companion on the `bout_n_fast_recovery_day` per-day series with the CONVENTIONS §3.6 factor-of-2 flag per parent MD §5.1; the flag is descriptive context only on the framework-validity verdict (not gating). Rationale: the parent MD §5.1 binds the inheritance; the framework-validity gate operates at day-level on a per-day count, so the day-level E[L]=7 directly applies. Alternatives considered + rejected as primary: (a) re-derive E[L] specifically for `bout_n_fast_recovery_day` — would re-open the block-length question; the parent MD pre-commits the inheritance.
4. **Effect-size operand for comparability**: percentage-point discrimination (pp) as the HEADLINE comparability bar (matching HA11 v1's +22.8 pp), with Cliff's delta on the bout-count distribution reported as a descriptive companion. Rationale: parent MD §6.2 bar 2 names the comparability operand as "discrimination is within ±10pp of HA11 v1's +22.8pp"; the pp gap is the HA11 v1 result.md's headline number and the natural reproduction operand. Cliff's delta is reported for cross-test consistency with parent MD §5.1's general inferential machinery (HA-C4 v2 uses Cliff's delta) but does not enter the §6.2 comparability bars. Alternatives considered + rejected as primary: (a) Cliff's delta alone — does not anchor on HA11 v1's headline number; (b) both as gating — over-constrains, no parent-MD basis.
5. **Crash-drop sensitivity (CONVENTIONS §3.4)**: REPORTED for transparency, NOT GATING. Rationale: CONVENTIONS §3.4 requires the row for Layer 4+ correlations; HA11-bout-redo is a framework-validity gate (methodology-validation, not substantive-correlation), so the strict §3.4 obligation is borderline. Default per the handoff: report for transparency even if not gating. The crash-drop sensitivity arm re-runs the §6.2 bars with `is_crash == True` dropped from both the crash-episode 4d windows and the null reference 4d windows; if |Δ pp discrimination| > 5 pp, surface as a §3.4 finding ("the framework-validity signal is crash-driven, not robust across the broader pool"); the primary verdict per §6.2 is unchanged. Alternatives considered + rejected as primary: (a) crash-drop sensitivity as gating — over-constrains a framework-validity gate; (b) dispatch §3.4 as inapplicable — under-reports for a Layer-4 audit hook the project applies elsewhere; transparency is the right discipline.

**Mandatory dispatches at lock-blocking gate level** (per [`hypothesis_lock_process.md` §3.2 step 4](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)):

- **Power-calc dispatch**: power calc inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design. The block-permutation null at E[L]=7 (per §4.6) is the within-subject inferential machinery; the §5 comparability bars determine the framework-validity verdict rather than asymptotic-power thresholds.
- **Single-cell headline lock**: the headline is the single triple {bout-level test on `bout_n_fast_recovery_day` × unmedicated × train era × calm-day pool (HA11 v1's null-pool reference dates)} evaluated against the three §6.2 comparability bars; sensitivity arms (motion-clean-only, transient-excluded, baseline-invalid-excluded, crash-drop) are diagnostic only and cannot promote to PASSED independently.

**Revision 2026-06-23-r2** (§3.6-compression LOCK absorb per [`hypothesis_lock_process.md` §3.5 + §3.6](../../../methodology/hypothesis_lock_process.md#35-revise-step-stage-3-of-the-arc-r2--the-bulk-of-methodological-strengthening)). Absorbs the fresh-session [audit report](../../../reviews/HA11-bout-redo-2026-06-22.md) (verdict: **PASS with caveats**; commit `69c4f8d`). The audit found no Layer-1 / Layer-2 / Layer-4 fires; one Layer-3 substantive (§4.5 effective n unpinned pre-lock); one Layer-3 minor (σ ≤ 0.5 inheritance from HA11 v1 `u_dip_count` to structurally-different `bout_n_fast_recovery_day` operand). Both items addressable by single-script counts on `per_day_master.csv` per the audit's explicit closure path (NOT spec revision; no architectural change, no falsification-bar change, no new statistical machinery). The four §4 strengthening recommendations are absorbed as inline pins + a §4.5/§4.8 dual-seed cross-reference. Q#3 (motion-clean elevation to PARTIAL-gating) explicitly retained as descriptive-only per audit closure (promoting would break HA11 v1 reference-frame comparability mid-test; the framework-validity question is whether the operand reproduces HA11 v1's signal in HA11 v1's reference frame, not whether it survives an additional filter).

The r2 changes (mechanical, no architectural delta):

- **§4.5 effective n pinned at 70** (closes L3 substantive). Verified by [`scripts/count_HA11_bout_redo_effective_n.py`](../../../../../scripts/count_HA11_bout_redo_effective_n.py) replaying HA11 v1's `build_null_sample` with seed `20260605`, then applying §4.2 (unmedicated) × §4.3 (train) × §4.4 (day-validity) × §4.5/§4.7 (≥ 3-of-4 window coverage). Of the 200 HA11 v1 reference dates, 73 fall in unmed × train; 70 survive the window-coverage gate. Well above the §4.9 walk-forward gate of n ≥ 30. Matches the auditor's ~50-65 estimate.
- **§4.6 σ-skip-threshold inheritance clarified** (closes L3 minor). Empirical σ of `bout_n_fast_recovery_day` across the 413 analysis days in unmed × train: median **0.739**, IQR [0.672, 0.826], range [0.589, 1.026]. HA11 v1 `u_dip_count` on the equivalent pool (480 days): median σ **0.840**, IQR [0.773, 0.899], range [0.633, 1.010]. The bout-count distribution sits modestly below `u_dip_count` (median σ delta −0.10) but stays well above the 0.5 floor — zero low-variability skips occur on either distribution in this pool. The σ ≤ 0.5 threshold is retained verbatim from HA11 v1 on inheritance-consistency grounds (pre-spec'd; not data-driven calibration); the modest empirical downshift is noted but does not trigger threshold recalibration at this lock.
- **§4.5 / §4.8 dual-seed cross-reference** (audit §4 side observation; mechanical wording closure). The seeds are now explicitly cross-referenced inline at the boundary.
- **§10.3 / §10.4 low-variability skip-rate reporting** (audit §4 strengthening recommendation #2). Skip-rate reporting was already in §10.2 / §10.3 per parent MD §6.3 inheritance; no spec change needed beyond the §4.6 clarification above.

**Status**: r2 LOCKED 2026-06-23 by user acceptance.

The four [§3.8 lock-blocking gates](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc) all confirmed at lock:

1. **Power-calc dispatch — MET**. §8 caveat 1 + §4.8 carry the Daza 2018 within-subject design dispatch verbatim. The block-permutation null at E[L]=7 (§4.8) is the within-subject inferential machinery; the §5 three-bar verdict rule determines the framework-validity verdict rather than asymptotic-power thresholds; INCONCLUSIVE cells are sample-size shortfalls per §4.9 walk-forward gate.
2. **Multi-comparison discipline — MET via single-cell headline lock**. Authorship "Mandatory dispatches — Single-cell headline lock" + parent MD §6 framework-validity-gate scope binds the headline to a single triple {bout-level × `bout_n_fast_recovery_day` × unmedicated × train × HA11 v1 calm-day pool} evaluated against the three §5 bars; the four sensitivity arms (§4.10) are diagnostic-only per §9.5 + cannot promote to PASSED.
3. **Register-row pointer — MET via non-supersession**. HA11-bout-redo is a project-original framework-validity test (the methodology-MD-analogue of [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock) dry-run halt per parent MD §6) — it does NOT supersede a register row. The HA11 stress-udip parent row (and HA11 v1's `## Future work — bout-level reproduction` forward pointer) stands. The parent MD §1.3 / §7.1 enabled-row pointer (`bout_level_recovery_dynamics.md` forward-pointing at HA-C4c per the lock-commit) is the substantive register chain; HA11-bout-redo is the framework-validity gate that conditions the chain.
4. **Re-audit clean OR §3.6 compression — MET via compression**. The §3.4 audit was clean on L1 + L2 + L4 + most of L3; one L3 substantive + one L3 minor both addressable by single-script counts on `per_day_master.csv` per the audit's explicit closure path. The r2 changes are mechanical (count pinning + threshold-inheritance clarification + dual-seed cross-reference) with no architectural change, no falsification-bar change, no new statistical machinery — matches the §3.6 compression-acceptability criteria. The audit's verdict explicitly authorises this disposition ("Both are addressable pre-lock by single-script counts on `per_day_master.csv`, NOT by spec revision").

---

## 1. Claim

**Pre-committed (framework-validity gate; NOT a substantive claim about Wiggers C4)**: on calm days (operationalised as HA11 v1's null-pool reference dates per §4.9; restricted to the unmedicated phase × train era) the per-day count `bout_n_fast_recovery_day` (per the parent MD §6.1 operand: bouts with `recovery_half_life ≤ 15 min` AND `tail_length ≤ 45 min`) reproduces HA11 v1's SUPPORTED-on-train signal (`u_dip_count` z-score, +22.8 pp discrimination, median signed z = 2.168) at the comparability bars in §5 (verbatim from parent MD §6.2).

**Headline cell**: unmedicated phase × train era × calm-day pool (HA11 v1 reference dates) × `bout_n_fast_recovery_day` × directional + effect-size (pp discrimination) + p-value comparability bars vs HA11 v1's `u_dip_count` train signal.

**What "reproduces" means here, narrowly**: the bout-level operand, when evaluated as a 4-day primary lead-up z-score against the participant's own lagged baseline (mirroring HA11 v1 §4.5–§4.7 windowing machinery verbatim), generates a discrimination magnitude, direction, and block-permutation p-value comparable to HA11 v1's train-era observed signal at the bars in §5. **It does NOT mean the bout-level operand SUPPORTS or REFUTES HA11 v1's substantive crash-precursor claim** — the framework-validity gate is a methodology-validation step, not a re-run of HA11 v1's substantive test. Substantive HA-C4c testing is downstream per §9.

**Direction of the prediction**: one-sided elevated (more fast-recovery bouts on crash 4d windows than on null reference 4d windows). Rationale: HA11 v1's SUPPORTED-on-train signal was one-sided elevated on `u_dip_count`; the parent MD §6.1 operand is structurally the same shape (sharp recovery + return) read at finer resolution; the prediction direction inherits.

## 2. Why we think this

Three priors anchor the prediction:

1. **HA11 v1 was SUPPORTED on train (+22.8 pp discrimination, median signed z = 2.168)** per [HA11 result.md](../HA11-stress-udip/result.md) headline. The signal exists in the corpus at the within-day-recovery-shape level for the pre-cliff (train) era; it is project-trusted independent evidence that the within-day recovery-shape construct carries crash-precursor information on this corpus in this era.

2. **The bout-level operand `bout_n_fast_recovery_day` is structurally the same shape read at finer resolution.** HA11 v1's U-dip detection (sharp drop + plateau at higher baseline) and the bout-level fast-recovery count (peak + sharp recovery + return to pre-bout baseline) capture the same underlying trajectory shape on the per-minute stress trace — a within-day "sharp transition followed by return" event. Per parent MD §6.1 the 15-min half-life + 45-min tail thresholds describe a structurally equivalent trajectory; the framework-validity gate is a check that the operand re-detects HA11 v1's signal at this resolution-shift.

3. **Framework-validity discipline**: if the bout-level operand cannot reproduce a signal the project already has independent evidence for (HA11 v1 SUPPORTED-on-train) in the conditions where that evidence was generated (unmedicated × train × HA11 v1's null-pool reference dates), the operand is not fit for purpose for the substantive HA-C4c retest. The parent MD §6 names this discipline explicitly as the methodology-MD-analogue of [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock) dry-run halt: failure to reproduce halts the bout-level cascade.

## 3. Data sources

- **`bout_n_fast_recovery_day`** — primary operand. Column in `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`, joined from `$GEVOELSCORE_DATA_PATH/unified/per_bout_aggregations_daily.csv` per the pipeline README. Per-day count of bouts with `recovery_half_life ≤ 15 min` AND `tail_length ≤ 45 min`. Emits `0` on valid days with no qualifying bouts; emits blank (NaN) on §3.4-invalid days. Source: bout-extraction pipeline [`pipeline/02_features/extract_stress_bouts.py`](../../../pipeline/02_features/extract_stress_bouts.py) LOCKED `d5b394c` 2026-06-22.
- **HA11 v1's null-pool reference dates** — calm-day pool. Construction per [HA11 v1 §4.9](../HA11-stress-udip/hypothesis.md#49-null-sample): 200 random non-overlapping reference dates, seed `20260605`, restricted to days satisfying HA11 v1 §4.4 day-validity (≥ 600 valid per-minute stress samples). HA11-bout-redo regenerates this pool via the same seed + validity rule + restricted to the unmedicated × train era subset.
- **`crash_v1` crash labels** — HA11 v1's primary outcome. Source: [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv) per HA11 v1 §3. Used as the crash-episode lead-up window anchor (4-day primary window per HA11 v1 §4.7), inherited verbatim from HA11 v1 for cross-test contrast comparability.
- **`citalopram_phase`** — derivable from date per [`citalopram_phase_stratification.md` §3](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification). Used to restrict the analysis to the unmedicated phase (2022-04-04 → 2024-04-08) per parent MD §5.5 + §6.
- **Day-validity gate**: ≥ 600 valid per-minute stress samples per HA11 v1 §4.4 + parent MD §3.4 (re-used verbatim). Not in first 21 days of `has_garmin_uds=True` coverage per parent MD §3.4 device-baseline-lag rule. Not in April 2024 cluster per `citalopram_phase_stratification`.

**No new FIT-level extraction required.** All inputs are in `per_day_master.csv` (post-pipeline-run `d5b394c`) plus `labels_crash_v2.csv`; HA11 v1's reference-date construction is re-runnable from the seed + the day-validity rule.

## 4. Measurement protocol

### 4.1 Operand definition (locked; verbatim from parent MD §6.1)

`bout_n_fast_recovery_day` = per-day count of bouts with `recovery_half_life ≤ 15 min` AND `tail_length ≤ 45 min`. Thresholds **pre-committed in parent MD §6.1**; inheriting verbatim, NOT re-deriving. Computed by the pipeline `extract_stress_bouts.py` per the parent MD §3 (bout-detection rule) + §4 (per-bout feature set); joined to `per_day_master.csv` as the column `bout_n_fast_recovery_day`.

Per-day semantics per pipeline README: emits `0` on valid days with no qualifying bouts; emits blank (NaN) on §3.4-invalid days. Per parent MD §3.1 r2 absorb, transient bouts are INCLUDED in the primary operand without down-weighting (the framework-validity gate inherits this default).

### 4.2 Stratum: unmedicated phase only (locked per parent MD §5.5 + §6)

Days in the unmedicated phase per [`citalopram_phase_stratification.md` §3](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification): **2022-04-04 ≤ date ≤ 2024-04-08**. Rationale: HA11 v1's SUPPORTED-on-train signal was concentrated in 2022-09-03 → 2023-12-31, fully inside the unmedicated phase (citalopram start 2024-04-09); reproducing HA11 v1's signal requires matching HA11 v1's dose-state.

Cross-phase machinery is OUT OF SCOPE for this pre-reg per parent MD §5.5 ("any downstream HA pre-reg using this MD's operand inherits the framework-validity gate restricted to the unmedicated stratum, regardless of the pre-reg's substantive scope"). Approach A dose-adjustment per parent MD §5.3 applies to HA-C4c, NOT here.

### 4.3 Era: train (locked per HA11 v1 §3)

**2022-09-03 ≤ date ≤ 2023-12-31** — HA11 v1's train era. Rationale: HA11 v1's SUPPORTED signal was on train (not validate); the framework-validity gate asks "does the bout-level operand reproduce HA11 v1's SUPPORTED-on-train signal?" — reproducing requires testing on the era where the signal lives.

Validate-era (HA11 v1's 2024-01-01 → 2026-06-05) reproduction is **NOT in scope** for this framework-validity gate. HA11 v1 validate was REFUTED (−10.7 pp); a bout-level validate test would conflate "does the operand work?" with "is the signal era-specific?" — both questions are interesting but only the train reproduction is the framework-validity check.

### 4.4 Day-validity gate (locked; inherited from HA11 v1 §4.4 + parent MD §3.4)

A day `d` enters the analysis if all four hold:

1. **Coverage**: ≥ 600 valid per-minute stress samples on `d` (HA11 v1 §4.4; inherited verbatim).
2. **Era**: 2022-09-03 ≤ d ≤ 2023-12-31 (train era per §4.3).
3. **Device-baseline lag**: `d` is NOT in the first 21 days of `has_garmin_uds=True` coverage (parent MD §3.4; inherited verbatim).
4. **Citalopram cluster**: `d` is NOT in April 2024 cluster (2024-04-09 → 2024-04-16) per `citalopram_phase_stratification`. (Trivially satisfied for train-era days but explicit for audit-traceability.)

Days failing the gate produce no `bout_n_fast_recovery_day` value (blank in `per_day_master.csv`); they are excluded from the analysis here as well.

### 4.5 Calm-day pool (HA11 v1 reference-date construction; locked)

**Construction**: 200 random non-overlapping reference dates per HA11 v1 §4.9, generated with HA11 v1's seed (`20260605`; distinct from this pre-reg's `RANDOM_SEED = 20260622` used for the block-permutation null in §4.8 — see §4.8 dual-seed note), restricted to days satisfying §4.4 (HA11 v1 §4.4 day-validity is a subset of this pre-reg's §4.4 gate since they share the ≥ 600 sample rule + LC era rule). For HA11-bout-redo specifically, the pool is further restricted to the unmedicated × train era subset (any of the 200 reference dates outside 2022-09-03 → 2023-12-31 are excluded).

**Per-reference-date window**: each reference date `r` defines a 4-day window `[r-3, r]` (mirroring HA11 v1 §4.7 4-day primary lead-up window). For each reference date, the per-day `bout_n_fast_recovery_day` is computed for each of the 4 days in `[r-3, r]`, z-scored against the participant's lagged personal baseline per §4.6, then aggregated via `max signed_z` over the 4-day window per HA11 v1 §4.7.

**Coverage gate per HA11 v1 §4.7**: at least 3 of 4 days in `[r-3, r]` must have a valid `bout_n_fast_recovery_day` value AND a valid (μ, σ) lagged baseline; reference dates failing this are excluded.

**Pre-lock pinned effective n** (r2; per [`scripts/count_HA11_bout_redo_effective_n.py`](../../../../../scripts/count_HA11_bout_redo_effective_n.py); CONVENTIONS §3.6 named count):
**70** reference dates in this pre-reg's stratum (unmedicated × train × satisfying §4.4 day-validity × satisfying the §4.7 ≥ 3-of-4 window-coverage gate), out of 200 generated by HA11 v1's `build_null_sample` with seed `20260605`. Well above the §4.9 walk-forward gate of **n ≥ 30** in the calm-day pool. Detailed counting flow: 200 HA11 v1 reference dates → 73 in unmed × train pre-window-coverage → 70 surviving the window-coverage gate. The script also confirms 480 bout-redo-valid days in the train era, of which 413 have a valid (μ, σ) lagged baseline (zero low-variability skips at the σ ≤ 0.5 floor; 67 insufficient-prior-days skips). Source files: [`udip_counts.csv`](../HA11-stress-udip/) (HA11 v1 day-validity) + [`per_day_master.csv`](../../../) `bout_n_fast_recovery_day` column + [`labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv) (crash-leadup occupied set).

### 4.6 Lagged personal baseline + z-score (locked; inherited verbatim from HA11 v1 §4.5–§4.6)

For each analysis day `d`:

- **Baseline window**: days in `[d-90, d-30]` (60-day window).
- **Baseline μ**: trimmed mean (10/90 cut) of `bout_n_fast_recovery_day` values across the prior days that are themselves valid per §4.4.
- **Baseline σ**: stdev of the same trimmed values.
- **Computed only when ≥ 40 of 60 prior days are valid** per HA11 v1 §4.5.
- **If σ ≤ 0.5 events** the day is flagged *low-variability* and skipped per HA11 v1 §4.5.

**Inheritance-of-σ-floor note** (r2; closes audit L3 minor on operand-specific distribution differences): the σ ≤ 0.5 threshold is inherited verbatim from HA11 v1's `u_dip_count` low-variability skip. `bout_n_fast_recovery_day` is structurally a different count distribution; the pre-lock single-script count (per [`scripts/count_HA11_bout_redo_effective_n.py`](../../../../../scripts/count_HA11_bout_redo_effective_n.py)) confirms the empirical σ on the unmed × train pool sits modestly below HA11 v1's `u_dip_count` σ:

- `bout_n_fast_recovery_day` σ across 413 analysis days: median **0.739** (IQR [0.672, 0.826], range [0.589, 1.026]).
- HA11 v1 `u_dip_count` σ on equivalent 480-day pool: median **0.840** (IQR [0.773, 0.899], range [0.633, 1.010]).
- Median σ delta: **−0.10** (bout-count distribution slightly less variable; both well above the 0.5 floor; **zero** low-variability skips on either distribution in this pool).

The threshold is retained at HA11 v1's 0.5 on **inheritance-consistency grounds** (pre-spec'd; not data-driven calibration). If a future v2 test surfaces materially different operand variability shape (e.g. higher zero-rate in a different stratum pushing many days below 0.5), the threshold may be calibrated to the bout-count distribution at v2 lock-time; for this draft the threshold is held at HA11 v1's value to preserve the framework-validity reference frame.

Per-day z-score per HA11 v1 §4.6:

- `delta(d) = bout_n_fast_recovery_day(d) − μ(d)`
- `z(d) = delta(d) / σ(d)`

### 4.7 Per-window aggregation (locked; inherited verbatim from HA11 v1 §4.7)

For each crash-episode lead-up window (or null reference window):

- **4-day primary window**: `[C-4, C-3, C-2, C-1]` (or `[r-3, r]` for null reference dates `r`).
- **Min valid days**: 3 of 4.
- **Window trigger flag (one-sided elevated, primary)**: `max signed_z ≥ N_std` (N_std = 1.5 per HA11 v1 §4.8 primary tier).

### 4.8 Statistical machinery (locked)

**Per-cell summaries** (computed on the train era × calm-day pool):

- **Crash-episode trigger frequency**: fraction of crash-episode 4d windows in the train era × unmedicated stratum × satisfying coverage gate § 4.5 + 4.7 that trigger (`max signed_z ≥ 1.5` one-sided elevated).
- **Null reference trigger frequency**: fraction of HA11 v1 null reference 4d windows in the train era × unmedicated stratum × satisfying coverage gate § 4.5 + 4.7 that trigger.
- **Discrimination (pp)**: crash-episode trigger frequency MINUS null reference trigger frequency, in percentage points.
- **Median signed z** across triggering crash episodes.

**Inferential statistic — block-permutation null at E[L]=7**:

Project-canonical per parent MD §5.1 + [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). For the framework-validity gate p-value:

1. Take the observed sequence `(date, bout_n_fast_recovery_day[d], is_crash[d])` over the unmedicated × train era.
2. Generate B = 10,000 null draws: for each draw, resample the `is_crash` label sequence via stationary bootstrap with geometric block-length E[L]=7 while keeping `bout_n_fast_recovery_day` values fixed in place.
3. For each null draw, recompute the discrimination (pp) per the procedure above.
4. **Empirical one-sided p-value** = `(1 + #{disc_null ≥ disc_observed}) / (B + 1)`.

**Seed**: `RANDOM_SEED = 20260622` (HA11-bout-redo; distinct from HA11 v1's `20260605` to keep the framework-validity gate's null distribution independently reproducible from HA11 v1's archived null). **Dual-seed cross-reference** (r2): the reference-date construction in §4.5 uses HA11 v1's `20260605` (inherited verbatim, NOT this pre-reg's `20260622`); the block-permutation null here uses this pre-reg's `20260622` (NOT HA11 v1's `20260605`). Implementer note for the next session writing `test.py`: do not conflate the two seeds.

**Cliff's delta** on the per-window `max signed_z` distributions (crash-episode vs null reference) is reported as a descriptive companion (per Authorship "Locked decisions" item 4); does NOT enter the §5 comparability bars.

**E[L]\* data-driven companion** per parent MD §5.1 inheritance: compute the data-driven E[L]\* on the `bout_n_fast_recovery_day[d]` sequence over the train era; flag if `|E[L]* − 7| / 7 > 0.5` per CONVENTIONS §3.6 factor-of-2 flag. The flag is descriptive context only; it does NOT modify the §5 verdict.

### 4.9 Walk-forward gate (n ≥ 30 in calm-day pool)

The framework-validity gate requires ≥ 30 calm-day reference 4d windows in the unmedicated × train era satisfying §4.5 + §4.7 coverage. Below 30, the cell is **INCONCLUSIVE** rather than PASSED/PARTIAL/FAILED, and the framework-validity verdict is reported as INCONCLUSIVE per §9.

Similarly: ≥ 10 crash-episode 4d windows in the unmedicated × train era satisfying coverage (HA11 v1 had 14 train episodes; the bout-extraction day-validity gate plus the unmedicated stratum may drop a small number). Below 10, the cell is INCONCLUSIVE.

### 4.10 Sensitivity arms (descriptive only; cannot promote to PASSED)

Per parent MD §3.4 + parent MD §3.1.1, the framework-validity gate inherits HA11 v1's sensitivity arms where applicable and adds bout-extraction-specific arms:

- **Motion-clean-only arm**: restrict the per-day `bout_n_fast_recovery_day` count to bouts with `motion_confound_flag = False` (per parent MD §3.4 per-bout flag; aggregate equivalent at the day level uses the primitive's convention per parent MD §3.4). Reported alongside the primary; primary keeps motion-confounded bouts per parent MD §3.4 + handoff §5 decision #6. If verdict changes between primary and motion-clean-only, flag as motion-fragility finding.
- **Transient-excluded arm**: restrict the count to bouts with `transient_flag = False` (per parent MD §3.1 r2 absorb; primary INCLUDES transients). If verdict changes, flag as transient-fragility finding.
- **Baseline-invalid-excluded arm**: restrict to bouts where `baseline_invalid_flag = False` (per parent MD §4 NaN semantics). If verdict changes, flag as baseline-validity fragility finding.
- **Crash-drop sensitivity arm** (CONVENTIONS §3.4; per Authorship "Locked decisions" item 5): re-run the §4.8 procedure with `is_crash == True` dropped from both the crash-episode window pool AND any reference-date window that overlaps a crash-episode. Compare crash-dropped discrimination (pp) vs primary discrimination (pp). If `|Δ pp| > 5` flag as a §3.4 finding ("framework-validity signal is crash-driven, not robust"); primary verdict unchanged.

All sensitivity arms are reported in §10.3 result.md template; none can promote to PASSED independently per the single-cell headline-lock discipline.

### 4.11 Per-bout-n reporting discipline (locked per parent MD §6.3 + CONVENTIONS §3.6)

Per parent MD §6.3 r2 absorb, the framework-validity gate's result.md MUST report:

- **Per-arm `n_bouts`**: total bouts in crash-episode 4d windows; total bouts in null reference 4d windows.
- **Per-cell `n_bouts × n_days × n_bouts_per_day`**: `(total_bouts_in_arm, n_days_in_arm, total_bouts / n_days)` for each arm.
- **Named-counts triplet per CONVENTIONS §3.6**: every count phrasing names scheme + unit + source-file (e.g. "1247 bouts per `bout_n_fast_recovery_day` count over 736 unmedicated days from `per_day_master.csv`").

Per-bout n is a derived quantity (depends on per-minute stress trace coverage + bout-extraction rule); under-reporting would obscure the framework-validity gate's effective power.

## 5. Pre-registered falsification criterion

**Quoted verbatim from parent MD §6.2** (per handoff §7 acceptance criterion 3 — NOT paraphrased; NOT re-derived):

> The framework-validity gate is met if the bout-level test on `bout_n_fast_recovery_day` on the unmedicated stratum × train era × calm-day pool (reference dates per HA11 v1 §4.9) shows:
>
> 1. **Directional sign agrees with HA11 v1's +22.8pp train discrimination**: bout-level test on `bout_n_fast_recovery_day` z-score (4-day primary window, one-sided elevated direction, N_std=1.5) shows positive discrimination on train.
> 2. **Effect-size comparability**: bout-level train discrimination is within ±10pp of HA11 v1's +22.8pp, i.e. **≥ +12.8pp**. Wider range (e.g. ±15pp) would admit a verdict that disagrees in magnitude even if it agrees in sign; ±10pp is the standard methodologically-comparable bar in the project.
> 3. **p-value comparability**: empirical p-value on the bout-level train discrimination is below HA11 v1's bar — that is, **p < 0.05** under the block-permutation null at E[L]=7 (per §5.1).
>
> **All three bars must be met** for the framework-validity gate to clear. Any single bar failing → framework-validity HALT.

**Verdict rule (per Authorship "Locked decisions" item 2)**:

| outcome | condition |
|---|---|
| **PASSED** (framework-validity gate clears) | all 3 bars met |
| **PARTIAL** | exactly 2 of 3 bars met |
| **FAILED** (framework-validity HALT) | ≤ 1 of 3 bars met |
| **INCONCLUSIVE** | walk-forward gate (§4.9) not met (n_calm < 30 OR n_crash < 10) |

The verdict band names PASSED / PARTIAL / FAILED are operationally distinct from HA11 v1's three-criterion SUPPORTED bar (HA11 v1 §5 (a) frequency, (b) discrimination, (c) magnitude). Per parent MD §6.2 r2 absorb cross-cite: the §6.2 bars map to HA11 v1's three-criterion set as follows — bar 1 (directional sign) is implicit in HA11 v1's (b); bar 2 (≥ +12.8 pp) is a *comparability band* derived from HA11 v1's *observed* train discrimination (+22.8 pp ±10 pp), NOT from HA11 v1's *locked* SUPPORTED bar (≥ +15 pp); bar 3 (p < 0.05) is *additional* to HA11 v1's criterion set (HA11 v1 uses non-parametric (a)-(c), not p-values). HA11 v1's (c) magnitude criterion is NOT mapped (current discipline per parent MD §6.2: bars 1+2+3 suffice for framework-validity).

## 6. Exclusion rules

- **LC era only**: days before 2022-04-04 excluded.
- **Unmedicated phase only**: days ≥ 2024-04-09 (citalopram start) excluded; cross-phase machinery out of scope per parent MD §5.5.
- **Train era only**: days outside 2022-09-03 → 2023-12-31 excluded; HA11 v1's validate era out of scope per §4.3.
- **April 2024 cluster (2024-04-09 → 2024-04-16)**: structurally unanalysable per `citalopram_phase_stratification`; excluded (trivially redundant with unmedicated phase exclusion).
- **First 21 days of `has_garmin_uds=True` coverage**: device-baseline-lag per parent MD §3.4; excluded.
- **Days with `bout_n_fast_recovery_day` NaN**: per the pipeline §3.4 day-validity gate (≥ 600 valid per-minute stress samples; not in first 21 device-baseline days; not in April 2024 cluster); excluded from the count. The pipeline emits `0` on valid days with no qualifying bouts (NOT NaN); `0` is a valid value entering the count.
- **Days with insufficient lagged baseline** (< 40 of 60 prior days valid per §4.6): excluded from the analysis day (HA11 v1 §4.5).
- **Days flagged `low-variability` (σ ≤ 0.5)**: excluded per HA11 v1 §4.5.
- **Reference-date 4d windows failing coverage** (< 3 of 4 days valid per §4.5 + §4.7): excluded.

## 7. Expected effect size if true

**Per parent MD §6.1**: the bout-level fast-recovery count should fall in a comparable range to HA11 v1's `u_dip_count` (mean ~0.85 events/day per HA11 v1 §7).

**Pre-committed sanity-check ranges**:

- **Per-day `bout_n_fast_recovery_day` mean across the unmedicated stratum**: expected in **[0.4, 1.7]** events/day (HA11 v1's 0.85 × {0.5, 2.0}). If the actual mean is outside this 2x deviation range, HALT the test per §10.4 sanity-check rule and document in result.md; the operand's per-day count distribution deviates from parent MD §6.1's calibration anchor and the framework-validity gate is not interpretable until the operand is reviewed.

- **Per-day `bout_n_fast_recovery_day` median**: expected in **[0, 2]** events (HA11 v1's median was 0 or 1 per the bounded-below distribution at low counts). If the actual median exceeds 5, HALT.

- **Per-day baseline σ across the unmedicated stratum**: expected in **[0.5, 3.0]** per HA11 v1 §7 sanity-check ranges on σ (inherited verbatim). If median baseline σ is < 0.5 the spec is too strict (low-variability flag will catch most days, mirroring HA11 v1's design constraint); if > 3.0 the spec is too loose (one-day fluctuation drowns the signal).

- **Crash-episode trigger frequency under SUPPORTED-equivalent**: expected in **[50%, 80%]** (HA11 v1 train was 64.3%; the bout-level reproduction should fall in a similar range under PASSED).

- **Null reference trigger frequency**: expected in **[30%, 55%]** (HA11 v1 train null was 41.5%; structurally similar under PASSED).

- **Discrimination (pp) under PASSED**: expected in **[+12.8, +35]** (per §5 bar 2: ≥ +12.8 pp; upper bound is HA11 v1's +22.8 pp + reasonable variation).

If any sanity-check fails on the dry-run, HALT and revise the spec per §10.4 (creating HA11-bout-redo-v2). The dry-run is the gate.

## 8. Caveats `result.md` must explicitly acknowledge

1. **Power-calc dispatch**: power calc inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design; the block-permutation null at E[L]=7 (§4.8) is the within-subject inferential machinery. (Per [`hypothesis_lock_process.md` §3.2 step 4](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) mandatory dispatch.)

2. **n=1 single-subject + observational + multi-source caveats per CONVENTIONS §3.1** + [`wiggers_test_design_on_chained_regime.md` Cross-cutting statistical hygiene §1-§4](../../../methodology/wiggers_test_design_on_chained_regime.md#cross-cutting-statistical-hygiene). Personal-baseline thresholds (§4.6 lagged baseline; HA11 v1's σ floor); operand calibrated to the participant's distribution; cross-subject generalisation out of scope.

3. **Framework-validity-NOT-substantive scope**: this pre-reg does NOT make a substantive claim about Wiggers C4. The framework-validity gate is a methodology-validation step that asks "can the operand re-detect the one within-day-recovery-shape signal we already trust on this corpus in this stratum?" A PASSED verdict here means the operand is fit for purpose for HA-C4c; it does NOT validate the operand globally and does NOT prejudge HA-C4c's substantive verdict. A FAILED verdict here halts the bout-level cascade pending operand review; it does NOT refute Wiggers C4 (the daily-aggregate test at HA-C4 v2 was REJECTED, but that is separate; the bout-level cascade's failure mode is "operand not capable" not "claim refuted").

4. **Inheritance-risk caveat**: if HA11 v1's SUPPORTED-on-train signal was era-specific (pre-cliff sympathetic-arousal pattern per HA11 result.md §4) or methodology-specific (the U-dip detection's exact threshold tuning), the comparability may not reproduce even if the bout-level operand is methodologically sound. The framework-validity gate cannot distinguish between "operand failed" and "the signal HA11 v1 detected was U-dip-specific, not within-day-recovery-shape-general". A FAILED verdict triggers operand review per §9; the operand-review session must consider this inheritance-risk possibility explicitly.

5. **Firstbeat-input amplification at minute resolution** (per parent MD §2.4 r2 absorb): the upstream Firstbeat-algorithm-derived stress signal is opaque (closed-source); bout-level analysis at minute resolution SURFACES algorithmic artefacts that daily-aggregate hid. A bout's `peak_height` may reflect HR + respiration spike rather than HRV change; the framework-validity gate is the primary mitigation (if algorithmic noise dominates, the bout-level reproduction will fail). A FAILED verdict is consistent with both "operand failed" and "algorithmic noise dominates"; the result.md must acknowledge this ambiguity.

6. **Pacing-behaviour mask risk** (per parent MD §2.4 r2 absorb): if the within-day stress pattern this participant generates is mediated by active pacing behaviour (the participant uses Garmin stress as a live pacing signal), bout-extraction at finer resolution may not "fix" the daily-aggregate flatness — it may reveal that the pacing behaviour shapes per-bout features too. The framework-validity gate restricted to unmedicated × train × calm-day pool partially insulates against this (the pacing era predates Garmin's heaviest cognitive use), but cannot fully eliminate the risk.

7. **Era restriction is non-negotiable here**: validate-era reproduction is out of scope per §4.3; readers expecting a cross-era validation will not find it in this pre-reg. HA11 v1 validate was REFUTED (−10.7 pp); a bout-level validate test belongs in HA-C4c-validate or an HA11-bout-redo-validate sister pre-reg, not here.

8. **Crash-drop sensitivity is reported but not gating** (per Authorship "Locked decisions" item 5): the framework-validity verdict is the binary PASSED/PARTIAL/FAILED on §5 bars 1+2+3; the crash-drop sensitivity arm is descriptive transparency per CONVENTIONS §3.4.

9. **Pipeline-extraction trust assumption**: this pre-reg assumes the bout-extraction pipeline (`extract_stress_bouts.py` LOCKED `d5b394c`) correctly implements parent MD §3 + §4. The pipeline's 6 inline smoke tests + 5-bout spot-check verification per pipeline README provide audit coverage; result.md should re-confirm the pipeline commit and verification log used.

10. **Multi-comparison**: the framework-validity gate is a single-cell headline lock (one triple: bout-level × unmedicated × train × calm-day pool, against 3 bars in §5). Sensitivity arms (§4.10) are diagnostic only. No multi-cell promotion possible.

## 9. What we do with each outcome

### 9.1 PASSED (all 3 §5 bars met) — framework-validity gate clears

The bout-level operand `bout_n_fast_recovery_day` reproduces HA11 v1's SUPPORTED-on-train signal at directional + effect-size + p-value comparability. The operand is **fit for purpose** for the substantive HA-C4c retest.

**Downstream actions**:

- **HA-C4c drafting UNBLOCKS** (no caveat). HA-C4c may inherit the parent MD's operand + Approach A dose-adjustment + cross-phase machinery per parent MD §5.3.
- **The methodology MD remains LOCKED** at its current state.
- **The bout-extraction pipeline remains LOCKED** at `d5b394c`.
- **No revision to HA11 v1.** HA11 v1's SUPPORTED-on-train verdict stands; HA11-bout-redo is a sister test, not a re-run.

### 9.2 PARTIAL (exactly 2 of 3 §5 bars met) — framework-validity gate partial

The bout-level operand reproduces 2 of 3 comparability bars. The most likely PARTIAL configurations and their interpretation:

- **Bars 1+2 met, bar 3 fails (p ≥ 0.05)**: discrimination magnitude is comparable but block-permutation null indicates the signal is not statistically distinguishable. Possible operand under-power at bout-level; possible block-length mis-calibration (check E[L]\* companion).
- **Bars 1+3 met, bar 2 fails (discrimination < +12.8 pp)**: the bout-level operand detects a directional + statistically-significant signal but at smaller magnitude. The operand is partially fit; HA-C4c verdict-magnitudes may be attenuated.
- **Bars 2+3 met, bar 1 fails (negative direction)**: unlikely under priors; if observed, the bout-level operand detects an OPPOSITE-direction signal. This would suggest fundamental operand mis-specification.

**Downstream actions on PARTIAL**:

- **HA-C4c drafting UNBLOCKS with explicit calibration caveat**. The HA-C4c pre-reg must carry a §8 caveat naming the PARTIAL framework-validity verdict + which specific bar failed + what that implies for HA-C4c's interpretability. HA-C4c's verdict-magnitudes are interpreted with a calibration discount.
- **The methodology MD remains LOCKED** but the parent MD §6 framework-validity gate's record now carries the PARTIAL verdict at this pre-reg's reproduction.
- **No revision to HA11 v1.**
- **Optionally**: an operand-refinement session may be authorised to re-tune `bout_n_fast_recovery_day` thresholds (the 15 / 45 in parent MD §6.1) and re-run a v2 of this pre-reg. NOT required; PARTIAL does not halt the cascade.

### 9.3 FAILED (≤ 1 of 3 §5 bars met) — bout-level cascade HALTS

The bout-level operand cannot reproduce HA11 v1's SUPPORTED-on-train signal at the comparability bars. The operand is NOT fit for purpose for the substantive HA-C4c retest.

**Downstream actions on FAILED**:

- **HA-C4c drafting is BLOCKED.** Per parent MD §6.3: "no downstream substantive HA test runs on this MD's operand."
- **The parent methodology MD's status reverts to "available but not load-bearing" pending revision.** A v2 of [`bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md) must be drafted re-thinking the bout-detection rule (parent MD §3) OR the operand-threshold choice (parent MD §6.1 thresholds 15 / 45) OR both.
- **The bout-extraction pipeline LOCK at `d5b394c` is not invalidated**, but the consumed operand `bout_n_fast_recovery_day` may be re-defined in the methodology MD v2; the pipeline may need a corresponding update.
- **HA11 v1 is unchanged.** HA11 v1's SUPPORTED-on-train verdict at U-dip-count level stands as historical record; the FAILED bout-level reproduction is a finding about the bout-level operationalisation, not about HA11 v1.
- **The FAILED verdict is itself a finding** per parent MD §6.3 + CONVENTIONS §4.2: within-day recovery dynamics on this corpus cannot be operand-ised in the way parent MD pre-committed. Report in result.md as the framework-validity verdict; the substantive Wiggers-C4-at-bout-level question is left structurally untestable until the operand is revised.

### 9.4 INCONCLUSIVE (walk-forward gate §4.9 fails)

Calm-day reference pool n < 30 OR crash-episode pool n < 10 in the unmedicated × train era after coverage filtering. The framework-validity gate cannot be evaluated at adequate power.

**Downstream actions on INCONCLUSIVE**:

- **HA-C4c drafting is HELD** pending re-evaluation of the calm-day pool construction (e.g. relax the day-validity gate to recover power; expand the random-reference-date pool beyond 200; mark as a separate v2 of this pre-reg).
- **The methodology MD remains LOCKED.**
- **HA-C4c may be drafted with a HOLD caveat** if the user wishes to proceed knowing the framework-validity gate has not been evaluated.

### 9.5 Sensitivity-arm divergence (per §4.10)

- **Motion-clean-only arm verdict differs from primary**: flag as motion-fragility finding. Report both verdicts; the primary verdict remains the headline per the single-cell headline-lock discipline.
- **Transient-excluded arm verdict differs from primary**: flag as transient-fragility finding.
- **Baseline-invalid-excluded arm verdict differs from primary**: flag as baseline-validity fragility finding.
- **Crash-drop sensitivity surfaces |Δ pp| > 5**: surface as a CONVENTIONS §3.4 finding ("framework-validity signal is crash-driven"); primary verdict unchanged.

None of the sensitivity arms can promote the verdict above PARTIAL or FAILED; the headline is the primary.

### 9.6 Spec sanity-check fails on dry-run (per §7 + §10.4)

If the per-day `bout_n_fast_recovery_day` mean is outside [0.4, 1.7] OR median outside [0, 5] OR baseline σ outside [0.5, 3.0], DO NOT run the full test. Document in dry-run report; revise the spec creating HA11-bout-redo-v2 with this pre-reg archived as v1.

## 10. Detection script architecture

### 10.1 Stage 1 — data (already done)

All inputs are in place post-pipeline-run `d5b394c`:

- `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` carries `bout_n_fast_recovery_day` joined from `per_bout_aggregations_daily.csv`.
- `crash_v2-definition/labels_crash_v2.csv` carries `crash_v1` labels per HA11 v1 §3.
- HA11 v1's reference-date pool is re-runnable from seed `20260605` + the day-validity rule.

**Pre-flight pipeline-trust check**: re-confirm `extract_stress_bouts.py --smoke-tests` PASS at commit `d5b394c` before running the test.

### 10.2 Stage 2 — test (`HA11-bout-redo/test.py`, written post-lock in a separate session)

**Two-stage design** mirroring HA11 v1's pattern:

**Stage 2a (data preparation)**:
- Load `per_day_master.csv`; filter to unmedicated phase × train era × §4.4 day-validity.
- Compute lagged personal baseline (μ, σ) per day per §4.6; apply low-variability skip + insufficient-baseline-prior skip per HA11 v1 §4.5.
- Compute per-day z-score per §4.6.
- Regenerate HA11 v1's null-pool reference dates (200 with seed `20260605`), restrict to unmedicated × train era subset; compute per-reference-date 4d window z-aggregation per §4.7.
- Identify crash-episode 4d windows in the unmedicated × train era per HA11 v1 §4.7; compute per-episode 4d window z-aggregation.

**Stage 2b (framework-validity gate evaluation)**:
- Compute trigger frequencies (crash-episode, null-reference) and discrimination (pp) per §4.8 per-cell summary.
- Compute block-permutation p-value at E[L]=7, B=10,000 draws, seed `20260622` per §4.8.
- Compute Cliff's delta on per-window `max signed_z` distributions (descriptive companion).
- Compute data-driven E[L]\* on `bout_n_fast_recovery_day[d]` over train; flag factor-of-2 per parent MD §5.1.
- Evaluate §5 verdict rule: PASSED / PARTIAL / FAILED / INCONCLUSIVE.

**Stage 2c (sensitivity arms per §4.10)**: re-run Stage 2b on motion-clean-only, transient-excluded, baseline-invalid-excluded, crash-drop arms.

**Companion descriptives**:
- Per-bout-n reporting per §4.11 (per-arm `n_bouts`, per-cell `n_bouts × n_days × n_bouts_per_day`).
- Per-day `bout_n_fast_recovery_day` distribution summary (mean, median, IQR, full range) per §7 sanity-check.
- Per-arm NaN fractions (low-variability skip rate, insufficient-baseline skip rate).
- Per-arm bout-count distribution (mean per-day, max per-day, count of zero-bout days).

**Dry-run mode** (`--dry-run`): prints sample sizes per arm (crash-episode 4d windows, null reference 4d windows, days satisfying §4.4); per-day `bout_n_fast_recovery_day` mean + median + σ summaries per §7; first-3-episodes z-windows for sanity-check (mirroring HA11 v1 pattern). **HALT** on §7 sanity-check failure per §10.4.

### 10.3 Stage 3 — `result.md` template

Reports in order:

1. **Headline verdict block** at top: framework-validity gate verdict (PASSED / PARTIAL / FAILED / INCONCLUSIVE) + §5 bar-by-bar breakdown (bar 1 directional, bar 2 effect-size pp, bar 3 p-value) + downstream implication (HA-C4c UNBLOCKED / UNBLOCKED-with-caveat / BLOCKED / HELD).
2. **Per-bar table**: each bar's observed value + comparability target + pass/fail.
3. **Per-arm summary table**: crash-episode arm + null reference arm + trigger frequency + discrimination (pp) + Cliff's delta + Mann-Whitney-style p-values + block-permutation p-value + n_episodes / n_reference / n_bouts per arm per §4.11.
4. **Companion descriptives**: per-day distribution, sanity-check pass/fail, E[L]\* companion + factor-of-2 flag, low-variability skip rate, insufficient-baseline skip rate.
5. **Sensitivity arms section** per §4.10: motion-clean-only verdict, transient-excluded verdict, baseline-invalid-excluded verdict, crash-drop sensitivity (|Δ pp|).
6. **Pipeline-trust block**: re-confirm `extract_stress_bouts.py` commit + smoke-test PASS at run-time.
7. **Verification log**: parent MD commit at test-time + HA11 v1 result.md commit at test-time + pipeline commit at test-time (mirrors this draft's Authorship verification log; ensures the test was run against the current state of the methodology + pipeline).
8. **Caveats per §8** (all 10 prominently surfaced; the framework-validity-NOT-substantive scope caveat at top alongside the headline verdict).
9. **Downstream actions per §9** (PASSED / PARTIAL / FAILED / INCONCLUSIVE branch as actually fired).

### 10.4 Run protocol

1. **Dry-run** (`python test.py --dry-run`): prints sample sizes, per-day distribution summary, first-3-episodes z-windows. **HALT triggers**:
   - **§4.9 walk-forward gate**: n_calm < 30 OR n_crash < 10 → INCONCLUSIVE; document + return without full-run.
   - **§7 sanity-check gates** (any of):
     - mean `bout_n_fast_recovery_day` outside [0.4, 1.7]
     - median outside [0, 5]
     - baseline σ outside [0.5, 3.0]
     → HALT + revise spec creating HA11-bout-redo-v2.
2. **Full run** (`python test.py`): emits `result.md` + `result-data.json` directly into this folder.
3. **No iteration on the spec after dry-run passes.** Post-dry-run revisions create v2 with v1 archived per the project's locked-pre-reg discipline.

---

*Pre-registration drafted 2026-06-22 by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Status: drafted, not locked. Next stage: fresh-session audit per [`/research-review docs/research/analyses/hypotheses/HA11-bout-redo/hypothesis.md`](../../../../../.claude/commands/research-review.md) before lock per [`hypothesis_lock_process.md` §3.4](../../../methodology/hypothesis_lock_process.md#34-audit-step-step-2-of-the-arc).*
