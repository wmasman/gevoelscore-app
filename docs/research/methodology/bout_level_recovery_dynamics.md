# Bout-level recovery dynamics — operand definition

*Producer-mode methodology MD per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafted 2026-06-19 as r1; pending fresh-session audit per [`/research-methodology-review`](../../../.claude/commands/research-methodology-review.md) before lock.*

---

## Authorship

**Drafted 2026-06-19** by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem.

**Drafting trigger**: [HA-C4 v2 LOCKED 2026-06-18](../analyses/hypotheses/HA-C4/hypothesis.md) was test-executed 2026-06-18 → **REJECTED** at the daily-aggregate level (triad sum = 0.0 / 3.0; commit `52bddb5`). The cross-channel reading: Channel 1's `stress_post_peak_drop_avg` companion SUPPORTED on both eras at +0.210 / +0.364, and Channel 1 + Channel 2 primary SUPPORTED on validate (n=41), but the train-era headline cells were REFUTED (n=171 / 171). Channel 3 train was wrong-direction. The pattern is consistent with the daily aggregate masking what Wiggers describes as a recovery-DYNAMICS claim. Sister tests: [HA-C4b v3](../analyses/hypotheses/HA-C4b/result.md) NOT-SUPPORTED on motion-filter crash-precursor; [HA11](../analyses/hypotheses/HA11-stress-udip/result.md) SUPPORTED-on-train (within-day stress U-dip count, +22.8 pp discrimination, median signed z = 2.168).

Per [HA-C4 v2 §9 REJECTED branch](../analyses/hypotheses/HA-C4/hypothesis.md): *"C4 mechanism would need different operationalisation (e.g. bout-level recovery curves)"*. This MD locks that operationalisation.

**Locked decisions at draft time** (per the handoff brief; structural pre-commits, not data-driven):

1. **Narrow lock scope**: enables [Wiggers C4](../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic) + HA11 only at lock; other Wiggers register rows named as enabled-on-request candidates in §7 with educated-assessment forward-pointers in their register entries (not auto-enabled).
2. **Cross-phase scope IS in scope** (handoff §1 item 5). The MD opens the per-bout citalopram-dose-covariate door; pre-commits Approach A (bout-level dose-adjusted predictor mirroring [`citalopram_phase_stratification §5.B`](citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests)) as the headline; documents Approaches B + C as sensitivity arms (§5).
3. **Bout-level β re-calibration COMMITTED as a sub-MD** at [`bout_level_dose_response_calibration.md`](bout_level_dose_response_calibration.md) (handoff §1 item 6 + decision #7 sub-resolution). Structural choice: sub-MD over appendix because the recalibration is an auditable independent substantive finding (does citalopram act on dynamics differently than on level?) and a load-bearing inheritance for any downstream HA pre-reg using cross-phase scope. Keeps this MD's operand definition tight.
4. **Framework-validity discipline is load-bearing** (handoff §1 item 3): any downstream HA pre-reg using this MD's operand must include the HA11 v1 reproduction check; failure to reproduce halts the substantive cascade. The check is restricted to the unmedicated stratum to preserve HA11 v1's calibration baseline (§6).
5. **Producer-mode discipline**: this MD does not pre-author the HA11-bout-redo or HA-C4c pre-regs (those are downstream sessions per [`hypothesis_lock_process.md` §3.2](hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)); it names the operand and the framework-validity gate.

**Status**: drafted r1, NOT LOCKED. Lock requires the §3.6 fresh-session audit per [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) — review report at `reviews/methodology-bout_level_recovery_dynamics-YYYY-MM-DD.md` to be produced by `/research-methodology-review` in a fresh session before lock.

---

## 1. Scope and shared-infrastructure framing

### 1.1 What this MD is

An **operand definition** for *bout-level recovery dynamics* on per-minute Garmin stress (`monitoring_b` FIT files, resolved via [`fit_utils.py`](../analyses/garmin_exploration/scripts/fit_utils.py)). The MD locks: what a bout is (peak-detection + return-window), the per-bout feature set, the unit-of-analysis blocking rule, the framework-validity gate, and the cross-phase dose-handling approach. Downstream HA pre-regs (HA11-bout-redo + HA-C4c) inherit these as canonical defaults.

### 1.2 What this MD is NOT

- **NOT a hypothesis pre-reg.** No substantive falsification criterion for "stuck sympathetic" or "U-dip" claims is locked here; those live in the per-HA pre-regs that depend on this MD ([`hypothesis_lock_process.md`](hypothesis_lock_process.md) governs those).
- **NOT a pipeline extraction spec.** The MD names what `pipeline/02_features/extract_stress_bouts.py` must produce; the script's construction is a separate downstream session.
- **NOT a re-derivation of HA-C4 v2's daily-aggregate verdict.** v2's REJECTED is the historical record; this MD's operand is the next-resolution operationalisation, not a retroactive fix to v2.
- **NOT a Wiggers-register row-by-row rewrite.** Each Wiggers row keeps its own register entry, its own verdict, and its own falsifier per the *one-row-one-HA* discipline. This MD enables specific rows at lock (§1.3); other rows are named as enabled-on-request candidates but are NOT pre-decided here.

### 1.3 Wiggers register rows this MD enables at lock — narrow

Per the handoff §1 item 4 (user-affirmed narrow scope), the lock-commit forward-points only:

- **[Wiggers C4](../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic)** — substantive Wiggers C4 retest at bout-level resolution becomes possible via downstream HA-C4c. The C4 register row is updated at lock-commit to forward-point at this MD as available infrastructure.
- **[HA11 (within-day stress U-dip)](../analyses/hypotheses/HA11-stress-udip/hypothesis.md)** — framework-validity reproduction check (HA11-bout-redo) becomes possible via downstream HA11-bout-redo pre-reg. HA11 is a project-original test of Wiggers' lived-experience within-day pattern (not a register-row), so the forward-pointer lives in HA11's hypothesis folder, NOT in `wiggers_testable_hypotheses.md`.

### 1.4 Enabled-on-request candidates (named, NOT auto-enabled)

Per the educated-assessment outputs (§9 of this MD + register-row forward-pointers in `wiggers_testable_hypotheses.md`), these rows could benefit from bout-level analysis but are NOT auto-enabled at lock. Downstream HA pre-regs on these rows may invoke this MD explicitly; the register entries forward-point to this MD as available infrastructure without pre-committing operand definitions:

| Wiggers row | mechanism within scope | benefit estimate |
|---|---|---|
| **A4** (sustained multi-hour RHR elevation) | per-minute HR runs already operationalised via `hr_sustained_elevated_flag_lcera` family; bout-level HR-recovery dynamics is a natural refinement | medium — the current "flag + longest run" operationalisation captures occurrence + duration, not within-bout recovery shape; bout-level adds shape information |
| **C1** (night orange stress elevated on PEM days) | within-night stress dynamics; this MD's operand applies at night-window resolution | medium — current proxy operationalisation collapses the sleep window to one mean; per-bout within-sleep recovery would resolve the dynamic structure |
| **C4b** (motion-filter crash-precursor) | per-minute stress + motion concurrence; already at per-minute resolution but framed as a per-day count | medium — bout-level reframing could discriminate between "many short bouts" vs "few sustained bouts" in the same per-day count |
| **H4** (parasympathetic swing) | per-bout characterisation could isolate the swing event vs steady-state | medium — current BB-anchored composite is daily-aggregate; bout-level could surface the swing-night structure |

### 1.5 Relation to existing resolution-scale conventions

Per [`time_resolution.md` §6](time_resolution.md#6-the-discipline-rule), the analysis scale must match the mechanism's natural timescale. Daily aggregate (§2.2 of that MD) was the default for HA-C4 v2 under the cluster-default heuristic in [`wiggers_testable_hypotheses.md` "Analysis scale"](../wiggers_testable_hypotheses.md). The HA-C4 v2 REJECTED verdict surfaces that within-day recovery dynamics is the right scale for Wiggers C4's recovery-dynamics claim. This MD's per-bout features sit at a **finer scale than any existing per-day default** in the project (per `time_resolution.md` §2.1 per-minute substrate → per-bout aggregation); the bout is itself a derived unit, not a calendar unit. Trade-offs are §2 of this MD.

---

## 2. Why bout-level (the four-input bar)

Per [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice), the four-input bar binds. Literature row is partially deferred (queued in [`_pending_literature_fetch.md`](_pending_literature_fetch.md) for autonomic-recovery / HRV-recovery-half-life references); the methodological reasoning does not depend on any specific paper landing.

### 2.1 Best-practices standards

- **Within-subject recovery-curve methodology is the orthodoxy for autonomic-recovery research.** The dominant operationalisation in exercise physiology + HRV-recovery literature is per-event recovery-shape characterisation (peak, decay rate, AUC above baseline), not per-day aggregation of recovery state. The standard claim shape — "system X recovers in time τ after stressor Y" — operates at event-level by construction; daily aggregation discards the temporal structure that the claim is *about*.
- **Per-event recovery features have established interpretations.** `recovery_half_life`, `decay_slope` (linear or exponential fit), `AUC above baseline` are the canonical features. The exercise-physiology anchor — see e.g. Stanley/Buchheit 2013 *Cardiac parasympathetic reactivation following exercise* (queued for retrieval) — uses HRV recovery half-life as a fitness/autonomic-resilience index at per-event resolution. The autonomic-load construct Wiggers' C4 names ("stress fails to drop") is the same construct read inverted (slow recovery = stuck sympathetic).
- **Bout-detection rules are well-trodden.** Peak-detection + return-window rules with explicit threshold parameters + minimum-separation rules are standard in respiration-event detection (apnea/hypopnea scoring), exercise-set detection (HR-based interval analysis), and stress-spike characterisation in smartphone-passive-sensing studies. The discipline is well-defined; the per-corpus calibration is the choice.

### 2.2 Established literature

**Partially deferred.** Anchor candidates (to be fetched + verified):

- **Stanley, Peake, Buchheit 2013** *Cardiac parasympathetic reactivation following exercise: implications for training prescription.* Sports Medicine 43:1259-1277. Canonical reference for HRV-recovery-half-life as an autonomic-resilience index at per-event resolution.
- **Buchheit 2014** *Monitoring training status with HR measures: do all roads lead to Rome?* Frontiers in Physiology 5:73. Methodological framework for per-event HR recovery features in athlete monitoring; transfers directly to non-athlete autonomic-recovery questions.
- **Plews et al. 2013** *Training adaptation and heart rate variability in elite endurance athletes: opening the door to effective monitoring.* Sports Medicine 43:773-781. Within-subject HRV-baseline + recovery framework.
- **Smartphone-passive-sensing recovery literature** (queued; awaits a fetch pass). Per-event recovery-shape from continuous passive sensing in chronic-illness populations is the closest match for this project's data substrate.

These references will tighten the operand-feature selection rationale when retrieved but do not gate the framework choice. The methodological reasoning below stands independently.

### 2.3 Tradeoff vision

The trade-off bar pits bout-level against three alternatives:

| dimension | daily aggregate (HA-C4 v2 default) | continuous time-series modelling | event-only analysis | **bout-level (CHOSEN)** |
|---|---|---|---|---|
| Captures recovery-dynamics shape | NO — collapsed to scalar | YES — but interpretation opaque | NO — event presence, not shape | YES — per-bout feature vector |
| Interpretability | high (one number per day) | low (model coefficients) | medium (count of events) | medium (per-feature semantics) |
| Statistical power | high (n=days) | high (n=minutes; autocorrelation-managed) | low (n=events; sparse) | medium (n=bouts; ~3-8 per day) |
| Match to Wiggers' verbatim claim | weak (HA-C4 v2 REJECTED demonstrates) | over-spec'd | weak (HA11 U-dip is event-count, not shape) | strong (Wiggers names "stress doesn't decrease for a long time" — a *recovery time* claim) |
| Compositionality with existing primitives | high | low | medium | high (per-bout features compose with per-day aggregates) |
| n=1 single-subject suitability | corpus-rich but mechanism-blind | mechanism-flexible but reads in-sample | corpus-thin | corpus-rich AND mechanism-shaped |

**Bout-level wins on the central dimension** (Wiggers claim shape match) and is competitive on power and interpretability. The HA-C4 v2 REJECTED verdict is the empirical case that daily aggregate masks the signal: Channel 1's `drop_avg` SUPPORTED on both eras (a per-event recovery-amount aggregated to daily mean) is a hint that the per-event level carries information the daily collapse loses on the primary `time_to_rest_min` metric.

### 2.4 Research limitations + objectives

- **n=1 single-subject observational design.** Per [CONVENTIONS §3.1](../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds), all thresholds calibrate to the participant's distribution; cross-subject generalisation is out of scope. Bout-detection thresholds (§3) are calibrated to this corpus.
- **Garmin-specific measurement constraints**, per [`hrv_proxy_via_stress.md` §2 + §6](hrv_proxy_via_stress.md#2-how-garmin-stress-is-derived):
  - The 24h stress score has motion-gaps (the algorithm declines to score during exercise); bouts that span motion-gaps are explicit edge cases (§3.4).
  - Device-baseline lag (~3 weeks per Wiggers PDF lines 99-106) means the first 21 days of `has_garmin_uds=True` coverage are suspect; bout-detection inherits this caveat at the day-level (§3.4).
  - The Firstbeat algorithm is opaque; the per-bout features are *operational* (they describe the surface trace) rather than *mechanistic* (they don't decompose RMSSD vs HF vs LF inputs).
- **Specific objectives the operand serves**:
  1. **Substantive C4 retest at bout-level resolution** (downstream HA-C4c). Operand must capture Wiggers' "stress doesn't decrease for a long time" claim at the resolution that claim is actually about.
  2. **Framework-validity reproduction of HA11 v1's SUPPORTED-on-train signal** (downstream HA11-bout-redo). Operand must be capable of reproducing a within-day recovery-shape signal that the project already has independent evidence for. This is the load-bearing falsifier on the methodology itself (§6).
  3. **Per-bout dose-response re-calibration** (sub-MD [`bout_level_dose_response_calibration.md`](bout_level_dose_response_calibration.md)). Operand features are inputs to the recalibration; without bout-level extraction the recalibration cannot run.
  4. **Composability with the existing per-minute primitives** ([`stress_low_motion_primitive.md`](stress_low_motion_primitive.md)) so that future HA pre-regs can combine bout-level features with the motion-filter framework without re-extraction.

---

## 3. Bout definition (the load-bearing operationalisation)

A **bout** is a within-day period of elevated stress with a defined start, peak, and end, derived from the per-minute `stress_level` trace per `monitoring_b` FIT files.

### 3.1 Peak-detection rule (locked pre-commits)

The peak-detection rule is **pre-committed** per [`hypothesis_lock_process.md` §3.8 gate 2](hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc) discipline applied here (single-cell headline lock at the methodology level: the operand definition does NOT support multiple parallel detector parameterisations as primary).

**Onset condition** (bout starts at minute `t_onset`):
- `stress(t_onset) ≥ 60` AND `stress(t_onset - 1) < 60` (upward crossing of the threshold), AND
- `stress(t)` was `< 50` for at least 10 of the 15 minutes in `[t_onset - 20, t_onset - 5]` (the pre-bout window must be non-elevated — i.e. the bout is not a continuation of a previous bout).

**Threshold value (60)** is anchored on Garmin's stress-zone documentation (40-60 = medium; 60-80 = high; 80+ = very high; see [DATA_DICTIONARY.md §7B](../DATA_DICTIONARY.md)). The 60-crossing is the "elevation onto medium-high" event Wiggers' "walls of orange" framing names. **The 60 anchor is reused from [HA-C4b's `S60_Mlow` primitive](stress_low_motion_primitive.md) verbatim** for cross-test consistency — the bout-level operand and the motion-filter primitive must share their stress threshold for joint analyses to be coherent.

**Pre-bout-non-elevated window (10 of 15 below 50)** ensures the bout is a discrete elevation event, not a continuation of an already-elevated state. The 50 cutoff (one Garmin tier below the 60 onset) is the standard hysteresis-band pattern in event-detection (separation between onset and pre-state thresholds prevents threshold-bounce false positives).

**Peak minute** (`t_peak`): the minute of maximum `stress(t)` within `[t_onset, t_onset + 120]`. The 120-minute forward window is the maximum plausible single-bout duration before the return-window rule is applied (§3.2); bouts whose stress monotonically rises past minute 120 are by construction multi-bout and §3.3's minimum-separation rule applies.

**Minimum-separation rule**: consecutive bouts must be separated by ≥ 60 minutes between `t_end(bout_k)` and `t_onset(bout_{k+1})`. Mirrors [HA11 §4.3](../analyses/hypotheses/HA11-stress-udip/hypothesis.md) U-dip sliding-window discipline.

**Within-bout minimum duration** (between `t_onset` and `t_peak`): ≥ 5 minutes. Bouts that peak immediately at onset are flagged as `transient_flag` and reported but down-weighted in the operand (they may represent algorithm-side noise rather than physiologic events).

#### 3.1.1 Alternatives considered + why rejected as primary

- **Threshold = 75 (Garmin's "very-high" cutoff)**: more conservative, fewer bouts per day. Rejected as primary because the n_bouts-per-day distribution becomes too thin for daily-level aggregation; the framework-validity HA11 check (§6) is harder to power. Reported as sensitivity arm `S75` in downstream pre-regs.
- **Threshold derived from personal lagged baseline** (`stress > μ_lagged + 1.5σ_lagged`): personalises but introduces a non-stationary detector. Rejected as primary because cross-bout comparability within a single day becomes harder to interpret; the lagged-personal-baseline pattern enters the OPERAND inside the per-bout features (§4 — `pre_bout_baseline`), not at the detector layer.
- **Onset threshold without hysteresis** (`stress(t) ≥ 60` alone): noisier; the 50-floor pre-window is the standard hysteresis fix. Rejected as primary on standard event-detection grounds.

### 3.2 Return-window rule (locked pre-commits)

A bout ends at the first minute `t_end ∈ [t_peak + 5, t_peak + 180]` where either:

(a) `stress(t)` returns to within `+5` of the pre-bout baseline (per §3.3) for ≥ 10 consecutive minutes, OR

(b) the 180-minute forward cap fires (no return-to-baseline within 3 hours of peak).

If (b) fires, the bout is flagged `did_not_return_flag = True`. This is the Wiggers-C4-positive case (analogous to HA-C4 v2 Channel 1's `stress_post_peak_time_to_rest_min` NaN-as-positive encoding per [HA-C4 §4.5](../analyses/hypotheses/HA-C4/hypothesis.md#45-nan-as-positive-encoding-for-channel-1-locked-verbatim-from-v1)): per-bout it means "this bout's recovery exceeded the observation window", which is direct evidence of stuck sympathetic.

**Edge case — bout spans sleep/wake**: if `t_peak` is during the waking window and the return-window cap would land inside the sleep window, the bout is truncated at sleep onset with `truncated_at_sleep_flag = True`. Per-bout features are still computed but `tail_length` is interpreted as a lower bound. Downstream pre-regs should report `truncated_at_sleep` frequency per arm.

**Edge case — bout truncated by day boundary**: bouts spanning calendar-day boundaries (e.g. an evening bout that continues past midnight) are attributed to the day of `t_peak`. Per-bout features computed on the full bout window regardless of calendar-day boundary.

#### 3.2.1 Alternatives considered + why rejected as primary

- **Return to within `+0` of baseline** (full return): more conservative; longer `tail_length`. Rejected as primary because the per-minute Garmin trace has ±1-3 point noise around any baseline (per [`hrv_proxy_via_stress.md` §2.4](hrv_proxy_via_stress.md#24-the-sleep-window-collapses-the-composite)); the `+5` tolerance is the noise floor.
- **Fixed 60-minute window post-peak** (no return condition): simpler but loses Wiggers' "stress doesn't decrease" signal. Rejected as primary; reported as sensitivity arm `fixed_60min`.
- **Return condition based on rate-of-change** (e.g. dStress/dt below threshold): captures "plateau" semantics but is sensitive to the per-minute noise. Rejected as primary; can be derived post-hoc from the per-bout time series if a downstream pre-reg needs it.

### 3.3 Baseline reference for the bout (locked pre-commits)

**Pre-bout local baseline** (`pre_bout_baseline`): mean of `stress(t)` over `t ∈ [t_onset - 30, t_onset - 5]`, restricted to valid minutes (stress in `[1, 100]`). Computed with at least 15 of the 25 minutes valid; otherwise the bout is flagged `baseline_invalid` and dropped from features that depend on `pre_bout_baseline`.

**Rationale**: the local-baseline framing matches Wiggers' "rest periods" language — the bout's baseline is the immediately preceding rest state, not a day-average or personal-baseline-from-distant-history. The per-bout recovery is measured against the state the participant was in just before the elevation, which is what the lived experience reads as "did the rest period work?".

**Sensitivity arm — lagged personal baseline**: each per-bout feature computed against `pre_bout_baseline_lagged_lcera(d)` (the participant's personal baseline for stress at the relevant time-of-day band, computed on the `[d-90, d-30]` window restricted to LC-era days per [CONVENTIONS §3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses)). Reported alongside the primary. If the verdict depends on the baseline choice, surface as a baseline-fragility finding.

**Why local-baseline wins as primary**: the lagged-personal-baseline framing is the right reference frame for *daily aggregate trajectory* questions (per `time_resolution.md` §2.4), but for *within-day recovery dynamics* the immediately-preceding rest state is the natural reference frame. The within-day recovery shape is what Wiggers' claim is about; the cross-day trajectory enters elsewhere (HA-P6, recovery_arc).

### 3.4 Edge cases + motion-confound handling (locked pre-commits)

**Motion-confound flag** (`motion_confound_flag` per bout): set to True if any minute in `[t_onset, t_end]` overlaps with Garmin intensity-class ≥ moderate, per the `motion_proxy` operationalisation in [`stress_low_motion_primitive.md` §3.2](stress_low_motion_primitive.md). The per-bout feature set is computed regardless of motion confound; the flag is reported per bout. Downstream pre-regs can include or exclude motion-confounded bouts as their own sensitivity arms.

**Primary verdict policy** (locked pre-commit per handoff §5 decision #6): the **primary operand includes all bouts** (motion-confounded + motion-clean). The motion-clean-only restriction is the standard sensitivity arm. Rationale: Wiggers' C4 verbatim claim ("stress doesn't decrease, despite resting") does include the conditional "despite resting", but the C4b motion-filter operationalisation has already been tested (HA-C4b v3 NOT-SUPPORTED) and the framework-validity HA11 v1 reproduction (§6) uses bouts without motion filtering. Including all bouts in the primary keeps the framework-validity gate's reference frame consistent.

**Day-validity gate**: a day `d` enters the bout dataset if:
- ≥ 600 valid per-minute stress samples on `d` (mirrors [HA11 §4.4](../analyses/hypotheses/HA11-stress-udip/hypothesis.md#44-day-validity) coverage gate),
- `d` is in the LC era (`d ≥ 2022-04-04`),
- `d` is NOT in the first 21 days of `has_garmin_uds=True` coverage (device-baseline lag per Wiggers PDF lines 99-106),
- `d` is NOT in the April 2024 cluster (structurally unanalysable per [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)).

Days failing the gate produce no bouts; the day-level row in the per-bout dataset records `n_bouts = NaN` (distinct from `n_bouts = 0`, which means "valid day, no bouts detected").

**Multi-peak bouts**: if `stress(t)` within `[t_onset, t_end]` shows multiple local maxima exceeding `peak_height − 10`, the bout is flagged `multi_peak_flag = True`. The primary `peak_height` is the global maximum; the multi-peak count is reported as a descriptive companion. Downstream pre-regs may treat multi-peak bouts as a separate stratum.

### 3.5 Naming convention

Per-bout columns in the per-bout dataset: `bout_<feature>` (e.g. `bout_peak_height`, `bout_recovery_half_life`). Per-day aggregations derived from per-bout columns: `bout_<feature>_<aggregation>_<window>` (e.g. `bout_recovery_half_life_median_day`, `bout_n_above_baseline_count_day`). Snake_case; consistent with [DATA_DICTIONARY.md](../DATA_DICTIONARY.md) patterns.

---

## 4. Per-bout feature set (the operand)

The per-bout dataset has one row per detected bout. Locked feature set (downstream HA pre-regs may add features as sensitivity arms but cannot remove these defaults):

| feature | definition | unit | range | NaN semantics |
|---|---|---|---|---|
| `bout_id` | composite key: `<date>_<bout_index>` where bout_index is 1-based within the day | string | — | always populated |
| `date` | calendar date of `t_peak` | date | — | always populated |
| `t_onset` | timestamp of bout onset per §3.1 | datetime | — | always populated |
| `t_peak` | timestamp of peak minute per §3.1 | datetime | — | always populated |
| `t_end` | timestamp of bout end per §3.2 | datetime | — | always populated |
| `peak_height` | `stress(t_peak)` | Garmin 0-100 | [60, 100] | always populated (else not a bout per §3.1) |
| `peak_minute` | minute-of-day of `t_peak` (0-1439) | int | [0, 1439] | always populated |
| `pre_bout_baseline` | mean of `stress(t)` over `[t_onset - 30, t_onset - 5]` per §3.3 | Garmin 0-100 | [0, 60) | NaN if < 15 valid minutes in window (`baseline_invalid` flag set) |
| `peak_minus_baseline` | `peak_height − pre_bout_baseline` | Garmin 0-100 | (0, 100] | NaN propagates from `pre_bout_baseline` |
| `recovery_half_life` | minutes from `t_peak` to the first minute where `stress(t) ≤ pre_bout_baseline + (peak_height − pre_bout_baseline) / 2` for ≥ 5 consecutive minutes | minutes | [0, 180) | NaN if `pre_bout_baseline` NaN; equals 180 if half-recovery not reached within the 180-min cap (`did_not_half_recover_flag`) |
| `tail_length` | `t_end − t_peak` in minutes per §3.2 | minutes | [5, 180] | 180 with `did_not_return_flag = True` if return condition not met within cap |
| `decay_slope` | linear regression slope of `stress(t)` on `t` over `[t_peak, t_end]`, in stress-points per minute | stress/min | (−∞, 0] | NaN if `t_end − t_peak < 10` minutes (insufficient data for slope) |
| `AUC_above_baseline` | sum over `t ∈ [t_onset, t_end]` of `max(0, stress(t) − pre_bout_baseline)` in stress·minutes | stress·min | [0, ~10000] | NaN propagates from `pre_bout_baseline` |
| `motion_confound_flag` | True if any minute in `[t_onset, t_end]` has motion-proxy ≥ moderate per §3.4 | bool | {True, False} | always populated |
| `did_not_return_flag` | True if §3.2 return condition not met within 180-min cap | bool | {True, False} | always populated |
| `did_not_half_recover_flag` | True if `recovery_half_life` cap fired | bool | {True, False} | always populated |
| `baseline_invalid_flag` | True if §3.3 baseline computation failed validity | bool | {True, False} | always populated |
| `truncated_at_sleep_flag` | True if §3.2 sleep-boundary truncation fired | bool | {True, False} | always populated |
| `multi_peak_flag` | True if §3.4 multi-peak condition fired | bool | {True, False} | always populated |
| `transient_flag` | True if `t_peak − t_onset < 5 minutes` per §3.1 | bool | {True, False} | always populated |
| `bout_during_sleep_flag` | True if `t_peak` falls within the sleep window per [`nightly_attribution.md`](nightly_attribution.md) | bool | {True, False} | always populated |

**Comparability across bouts within a day vs across days**: per-bout features are locally referenced (against `pre_bout_baseline`, which is bout-specific). This makes within-day cross-bout comparisons interpretable (same trace, drifting reference) and cross-day comparisons interpretable after dose-adjustment (§5). Raw cross-day comparison without dose-adjustment is **discouraged for cross-phase tests** per [`citalopram_phase_stratification.md` §4](citalopram_phase_stratification.md#4-per-channel-inheritance-rules) — `peak_height` and `pre_bout_baseline` inherit the load-bearing dose-modulation caveat from `all_day_stress_avg` / `stress_mean_sleep` (the parent channels) and require Approach A / B / C treatment per §5.

**Citalopram-phase metadata** joined per bout (from `dose_plasma_mg(d)` per [`citalopram_phase_stratification.md` §3](citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification)):
- `dose_plasma_mg` (float; 0 for pre-citalopram dates)
- `citalopram_phase` ∈ {unmedicated, buildup, consolidation, afbouw, post_afbouw}
- `is_unmedicated` (bool)

**Derived per-day aggregations** (produced as part of the per-bout pipeline, joined to `per_day_master.csv`):

| column | aggregation | use |
|---|---|---|
| `bout_count_day` | count of bouts per day | counterpart to HA11's `u_dip_count`; framework-validity reference |
| `bout_recovery_half_life_median_day` | median `recovery_half_life` over bouts per day | per-day operand for slow-recovery distribution comparison |
| `bout_tail_length_p75_day` | 75th-percentile `tail_length` over bouts per day | sensitive to the slow-recovery tail (Wiggers C4 verbatim) |
| `bout_AUC_above_baseline_sum_day` | sum of `AUC_above_baseline` over bouts per day | cumulative within-day load |
| `bout_n_did_not_return_day` | count of bouts with `did_not_return_flag = True` per day | direct count of Wiggers C4-positive within-day events |
| `bout_n_fast_recovery_day` | count of bouts with `recovery_half_life ≤ 15 min` AND `tail_length ≤ 45 min` per day | HA11-bout-redo framework-validity reference (the "fast-recovery bout" operand; thresholds calibrated in §6.1) |

The per-day aggregations are the joinable surface for downstream HA pre-regs. The per-bout dataset itself remains accessible for any pre-reg needing the within-day distribution.

---

## 5. Inferential framework

### 5.1 Unit of analysis + blocking rule

**Bouts are NOT independent within a day** (consecutive bouts share day-state — autonomic, behavioural, pharmacological). **Days are NOT independent across the corpus** (day-level autocorrelation at E[L]=7 per [`permutation_null_block_length.md`](permutation_null_block_length.md)). The blocking rule must respect both.

**Locked**: bootstrap **days as blocks**, preserving within-day bout structure. Each bootstrap resample draws blocks of consecutive days (stationary bootstrap, geometric block-length with E[L]=7 days) and includes all bouts on those days verbatim. Per-bout features are observations *within* the day-block; the day-block is the unit of resampling.

**E[L] anchor** inherits from [`permutation_null_block_length.md`](permutation_null_block_length.md) at the day level. Bout-level autocorrelation within a day is handled by keeping bouts intact within their day-block; the day-level stationary bootstrap at E[L]=7 absorbs cross-day autocorrelation. **The MD does NOT introduce a new E[L] anchor for bouts**; the existing day-level anchor is the right unit because the analytical question is about day-level recovery state (the per-bout features aggregate to per-day descriptors for any cross-day comparison).

**Data-driven E[L]\* companion** per [`permutation_null_block_length.md`](permutation_null_block_length.md) inherits: any downstream pre-reg reports the data-driven E[L]\* on the per-day operand under test + factor-of-2 flag. Per [`hypothesis_lock_process.md` §4.6](hypothesis_lock_process.md#46-result-time--rolling-sum-predictor-structural-autocorrelation-factor-of-2-flag), rolling-sum-of-bouts predictors are anticipated to inflate E[L]\* structurally; downstream pre-regs using such predictors should pre-emptively cite §4.6 in their §8.

### 5.2 Multiple-comparison discipline

Bout-level analysis multiplies the cell count: across phases × across features × across thresholds, a single hypothesis test naively explodes the multiplicity surface. This MD **does NOT pre-commit the multiplicity correction rule** for downstream HA pre-regs — that is a per-pre-reg decision per [`hypothesis_lock_process.md` §3.2](hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) and per [`wiggers_test_design_on_chained_regime.md` Cross-cutting statistical hygiene §3](wiggers_test_design_on_chained_regime.md#cross-cutting-statistical-hygiene). The standard project-canonical pattern is **single-cell headline lock + Holm step-down across companions as secondary report**; downstream pre-regs should adopt that pattern by default and depart only with explicit justification.

This MD's contribution at the multiplicity layer: surface that the per-bout feature set (§4) has 6 per-day aggregations and 8 per-bout features. Downstream pre-regs should pre-commit ONE primary operand among these and treat the rest as sensitivity arms.

### 5.3 Cross-phase scope position (load-bearing) — Approach A as headline

Per the handoff §1 item 5 (user-affirmed) + §5 decision #7, cross-phase analysis IS in scope. The MD opens the per-bout dose-covariate door. Three approaches were evaluated against the §2.2 four-input bar:

#### Approach A — bout-level dose-adjusted predictor (CHOSEN as headline)

Mirrors [`citalopram_phase_stratification.md §5.B`](citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests) at the per-bout layer. For each per-bout feature in the feature set, compute the dose-adjusted variant:

```
peak_height_adj(bout)            = peak_height(bout)           − β_peak * dose_plasma_mg(d)
pre_bout_baseline_adj(bout)      = pre_bout_baseline(bout)     − β_baseline * dose_plasma_mg(d)
recovery_half_life_adj(bout)     = recovery_half_life(bout)    − β_halflife * dose_plasma_mg(d)
decay_slope_adj(bout)            = decay_slope(bout)           − β_slope * dose_plasma_mg(d)
AUC_above_baseline_adj(bout)     = AUC_above_baseline(bout)    − β_AUC * dose_plasma_mg(d)
```

The β coefficients per feature are locked from the **bout-level β recalibration** in [`bout_level_dose_response_calibration.md`](bout_level_dose_response_calibration.md) (sub-MD; §5.4 below). The recalibration runs the dose-response on each per-bout feature independently in the buildup post-CPAP window (mirroring the parent MD's `S2 post-CPAP-buffer` spec). The resulting β coefficients are the inheritance defaults for downstream HA pre-regs using cross-phase scope.

**Pros**: preserves single-pool framework; no n loss from phase stratification; matches the project-canonical dose-handling pattern.

**Cons**: depends on the β estimate being correct (the sub-MD provides 95% CIs); per-mg β is from the buildup window which may not be exactly the participant's current dose-sensitivity (per [`citalopram_phase_stratification.md §5.B`](citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests) implicit tradeoff). Mis-specification under-corrects at non-steady-state windows.

#### Approach B — bout-level dose as per-bout covariate in inferential model (sensitivity arm)

Mixed-effects model with `bout_feature ~ heavy_T_indicator + citalopram_dose_mg + (1|day) + ...` where the day-level random effect absorbs within-day correlation. Standard cross-phase pooling at the per-bout layer.

**Pros**: most flexible; least up-front pre-commits.

**Cons**: assumes linear additive dose effect on the feature + correct covariance structure for within-day bout correlation; the dose-feature interaction can co-vary with heavy_T (a heavy-T day in afbouw has different dose than a heavy-T day in consolidation) and partial-out is fragile at n=1.

#### Approach C — stratify bouts by citalopram phase, meta-analyse (sensitivity arm)

Run the bout-level test within each of unmedicated / buildup / consolidation / afbouw per [`citalopram_phase_stratification.md §3`](citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification); meta-combine across strata. Closest to the daily-aggregate phase-stratification pattern at bout resolution.

**Pros**: discipline-conservative; no β-dependence; per-phase behaviour visible.

**Cons**: possibly underpowered at buildup/afbouw transitions (n ≈ 70 days each); the buildup phase has the CPAP-end confound that the post-CPAP buffer subset (~50 days) addresses for the daily-aggregate calibration but is more demanding at bout-level since bouts are sparser than days.

#### Four-input justification for Approach A as headline

- **Best-practices standards**: covariate-adjustment for a measured time-varying confounder is the standard observational-causal-inference move (Rubin 1974; Pearl 2009; Daza 2018 for n-of-1 self-tracked designs). The project anchor [Daza 2018](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) adapts the counterfactual framework to time-varying confounders in within-subject self-tracking data.
- **Established literature**: the daily-aggregate covariate-adjustment pattern is already locked in [`citalopram_phase_stratification.md §5.B`](citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests). Inheriting the same pattern at the per-bout layer keeps the methodology stack coherent.
- **Tradeoff vision**: Approach A maximises power (no n-loss) and discipline-coherence (matches existing pattern). Approach B's mixed-effects machinery is harder to audit and introduces covariance-structure choices that the n=1 design cannot empirically validate. Approach C is the discipline-conservative fallback but under-uses the dose-information the recalibration sub-MD produces. A is the right primary; B + C as sensitivity arms cover the assumption-fragility surface.
- **Research limitations + objectives**: n=1 corpus needs every observation; per-bout sparsity (~3-8 bouts/day; ~20-50 bouts/phase × n_days) makes per-phase stratification expensive. The recalibration sub-MD provides the β estimates with 95% CIs; the cost of A's β-dependence is bounded by those CIs. The tradeoff is acceptable.

**The downstream HA pre-regs inherit Approach A as headline**; they can add B + C as further sensitivity arms but cannot relax this default. Specific exception: the framework-validity HA11 v1 reproduction check (§6) is restricted to the unmedicated stratum (where `dose_plasma_mg = 0` by §3 of `citalopram_phase_stratification.md`); under that restriction, A / B / C collapse to the raw unadjusted operand. The cross-phase scope decision applies to substantive cross-phase tests, NOT to the framework-validity gate.

### 5.4 Upstream calibration — bout-level β recalibration is pre-committed (sub-MD)

Per the handoff §1 item 6 + decision #7 sub-resolution, the daily-aggregate β coefficients in [`citalopram_dose_response_stress_mean_sleep.md §5.6.1`](citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read) (+0.43/mg for `stress_mean_sleep`, +0.57/mg for `all_day_stress_avg`, −1.13/mg for `bb_lowest`) were calibrated on **daily-aggregate stress channels**. The bout-level features in §4 are not these channels — they are derived from the same per-minute substrate but at a different resolution and with different mathematical structure. Linear extension of the daily β to per-bout features is an assumption, not a derivation.

**The recalibration is committed as a sub-MD** at [`bout_level_dose_response_calibration.md`](bout_level_dose_response_calibration.md). The sub-MD fits the dose-response on each per-bout feature independently (`peak_height`, `pre_bout_baseline`, `recovery_half_life`, `decay_slope`, `AUC_above_baseline`) using the same three-pronged spec as the parent dose-response MD (afbouw primary + buildup post-CPAP + spring 2025 control). The resulting β coefficients are the inheritance defaults for §5.3 Approach A.

**Why sub-MD over appendix in this MD**:
- Keeps the operand definition (this MD) tight and auditable on its own terms.
- Surfaces the recalibration as its own auditable unit — the recalibration produces an independent substantive finding (does citalopram act on dynamics differently than on level?) and that finding should not be buried inside an operand-definition MD.
- Matches the project pattern: [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md) was spun off from [`citalopram_dose_response_stress_mean_sleep.md`](citalopram_dose_response_stress_mean_sleep.md) for the same reason.
- The sub-MD lands in the SAME drafting session as this MD (per the cascade resource estimate in the handoff §11); both r1 → both audited (potentially in the same audit session, or in sister audits) → both locked.

**Independent substantive finding from the recalibration** (per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) — honestly framed): if the per-feature β coefficients differ systematically from the daily-aggregate β (e.g. citalopram acts strongly on `peak_height` but weakly on `recovery_half_life`), that is a research finding in its own right about whether citalopram modulates *level* of autonomic arousal vs *dynamics* of recovery. This finding lands inside the recalibration sub-MD; it informs but does not gate this MD's lock.

### 5.5 Framework-validity restriction under cross-phase scope

The §6 framework-validity check on HA11 v1 is **restricted to the unmedicated stratum** (LC era start 2022-04-04 → 2024-04-08). Rationale:

- HA11 v1 was tested on `crash_v1` events spanning the LC era; the SUPPORTED-on-train signal was concentrated in 2022-09-03 → 2023-12-31, which is fully inside the unmedicated phase (citalopram start 2024-04-09).
- The framework-validity gate asks "does the bout-level operand reproduce HA11 v1's signal at directional + effect-size + p-value comparability?" — that question is well-defined only when the dose-state matches HA11 v1's. Reproducing HA11 v1 in a medicated phase would require disentangling dose-effect from operand-fidelity, which conflates the framework-validity question with a substantive question.
- Cross-phase reproduction of the HA11 signal IS a SUBSTANTIVE finding for HA-C4c (does bout-level fast-recovery count differ between calm-day and heavy-T-day in medicated phases?), not a framework-validity gate.

**Pre-commit**: any downstream HA pre-reg using this MD's operand inherits the **framework-validity gate restricted to the unmedicated stratum**, regardless of the pre-reg's substantive scope. This is the load-bearing methodological inheritance for HA11-bout-redo specifically; HA-C4c may have additional framework-validity sub-gates per its own pre-reg but cannot relax this one.

---

## 6. Framework-validity discipline (the MD's own falsifier)

This is the methodology-MD-analogue of [`hypothesis_lock_process.md` §3.9](hypothesis_lock_process.md#39-run-step-post-lock) (dry-run halt discipline). The methodology MD itself cannot be falsified by a substantive hypothesis test; it can be falsified by demonstrating that the operand fails to reproduce a signal the project has independent evidence for. The HA11 v1 SUPPORTED-on-train U-dip count signal IS that independent evidence.

### 6.1 The discipline

Any downstream HA pre-reg using this MD's operand must include the **HA11 v1 reproduction check as a framework-validity gate**. The check:

> With the §3 locked bout-detection rule + the §4 `bout_n_fast_recovery_day` feature, the per-day count on calm days (per [HA11 §4](../analyses/hypotheses/HA11-stress-udip/hypothesis.md#4-measurement-protocol) reference dates from the null pool) reproduces HA11 v1's SUPPORTED-on-train signal at the directional + effect-size + p-value comparability bars below.

**The `bout_n_fast_recovery_day` operand definition**: per-day count of bouts with `recovery_half_life ≤ 15 min` AND `tail_length ≤ 45 min`. The thresholds (15 / 45) are pre-committed here based on:
- The HA11 v1 U-dip event-rate distribution (mean ~0.85 events/day per [HA11 §7.B](../analyses/hypotheses/HA11-stress-udip/hypothesis.md#7-expected-effect-size-if-hypothesis-is-true) — the bout-level fast-recovery count should fall in a comparable range to be informative).
- The within-bout recovery shape: a 15-min half-life with 45-min tail describes a "sharp recovery followed by complete return" — structurally the same trajectory HA11 v1's U-dip detection captures (sharp drop + plateau at higher baseline, read inverted at the bout level: sharp recovery + return to pre-bout baseline).

### 6.2 Comparability bars (pre-committed)

The framework-validity gate is met if the bout-level test on `bout_n_fast_recovery_day` on the unmedicated stratum × train era × calm-day pool (reference dates per HA11 v1 §4.9) shows:

1. **Directional sign agrees with HA11 v1's +22.8pp train discrimination**: bout-level test on `bout_n_fast_recovery_day` z-score (4-day primary window, one-sided elevated direction, N_std=1.5) shows positive discrimination on train.
2. **Effect-size comparability**: bout-level train discrimination is within ±10pp of HA11 v1's +22.8pp, i.e. **≥ +12.8pp**. Wider range (e.g. ±15pp) would admit a verdict that disagrees in magnitude even if it agrees in sign; ±10pp is the standard methodologically-comparable bar in the project.
3. **p-value comparability**: empirical p-value on the bout-level train discrimination is below HA11 v1's bar — that is, **p < 0.05** under the block-permutation null at E[L]=7 (per §5.1).

**All three bars must be met** for the framework-validity gate to clear. Any single bar failing → framework-validity HALT.

### 6.3 Halt rule

If the framework-validity gate fails:

- **No downstream substantive HA test runs on this MD's operand.** HA-C4c is not interpretable if the operand cannot reproduce a signal we have independent evidence for; running HA-C4c anyway would conflate a substantive result with an operand-failure mode.
- **This methodology MD is revised** (creating v2), and the substantive cascade halts until v2 clears its own framework-validity gate.
- **The halt is itself a finding** — it surfaces that within-day recovery dynamics on this corpus cannot be operand-ised in the way this MD pre-committed. Per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), the halt is reported as the framework-validity verdict; the substantive question (does Wiggers C4 hold at bout-level?) is left structurally untestable until the operand is revised.

This is structurally analogous to the [HA-C4 v1 dry-run HALT 2026-06-17](../analyses/hypotheses/HA-C4/hypothesis-v1-archived.md) at §7.5 gate 2 — locked-pre-reg discipline working as designed. The framework-validity halt is the methodology-MD-level mirror.

### 6.4 What "framework-validity" does and does not mean

- **Does mean**: the operand is capable of detecting a within-day recovery-shape signal that the project has independent evidence for, when applied to the dataset and population (unmedicated stratum × train era × calm days) where that evidence was generated.
- **Does NOT mean**: the operand is "validated" against ground truth (no ground truth exists for "stuck sympathetic" at bout-level resolution).
- **Does NOT mean**: the operand will reproduce HA11 v1's signal in OTHER conditions (validate era; medicated phases; heavy-T days). Failure to reproduce in those conditions is interpretable as substantive finding (era-specific, dose-specific, exertion-specific), not as operand failure.

The discipline is narrow on purpose. It asks: "can this operand re-detect the one within-day-recovery-shape signal we already trust?" If yes, downstream substantive tests are interpretable; if no, they aren't.

---

## 7. Cross-references and downstream cascade

### 7.1 Wiggers register rows this MD enables at lock (narrow scope)

Per §1.3 + handoff §1 item 4:

- **[Wiggers C4](../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic)**: the register row is updated at lock-commit to forward-point at this MD as available infrastructure for downstream HA-C4c. The existing HA-C4 v2 → REJECTED pointer stays in the register row; the bout-level forward-pointer is additive (does not supersede HA-C4 v2's verdict at daily-aggregate level — that verdict stands as the historical record for daily-aggregate operationalisation).
- **[HA11 (within-day stress U-dip)](../analyses/hypotheses/HA11-stress-udip/hypothesis.md)**: forward-pointer lives in HA11's hypothesis.md as a `## Future work` section pointing at this MD + naming HA11-bout-redo as the framework-validity downstream pre-reg. HA11 is not a Wiggers register row, so no `wiggers_testable_hypotheses.md` update.

### 7.2 Enabled-on-request candidates (named per §1.4; NOT auto-enabled)

The register entries for A4, C1, C4b, H4 receive a forward-pointer `→ bout-level analysis would benefit; see [`bout_level_recovery_dynamics.md`](methodology/bout_level_recovery_dynamics.md)` per the educated-assessment work (handoff §1 item 7 + §5 decision #9). Per §9 of this MD the rationale per row:

- **A4**: per-bout HR-recovery dynamics would refine `hr_sustained_elevated_flag`'s occurrence+duration framing with within-bout recovery shape.
- **C1**: per-bout within-sleep recovery would resolve the dynamic structure the daily-aggregate `stress_mean_sleep` proxy collapses.
- **C4b**: bout-level reframing could discriminate "many short bouts" vs "few sustained bouts" — currently merged at the per-day count level.
- **H4**: per-bout characterisation could isolate the parasympathetic swing event vs steady-state.

These forward-pointers do NOT pre-commit operand definitions for those rows; downstream HA pre-regs on these rows must invoke this MD explicitly + may extend its operand if needed (e.g. an HR-channel bout-detection variant for A4).

### 7.3 HA pre-regs that will depend on this MD

The downstream cascade per handoff §11:

1. **HA11-bout-redo** (next-after-this-MD-and-pipeline pre-reg): framework-validity reproduction check (§6); restricted to unmedicated per §5.5 + §6.
2. **HA-C4c** (later pre-reg): substantive Wiggers C4 retest at bout-level. Cross-phase per §5.3 Approach A (headline). Multiple per-feature primary candidates possible (median `recovery_half_life`; `tail_length` 75th-pct; `n_did_not_return`); the per-pre-reg single-cell-headline-lock discipline applies.

Other downstream HA pre-regs on the §1.4 candidates come later, register-row-by-register-row, only when an authoring session for that row opens.

### 7.4 Pipeline stage forward-pointer

The per-bout dataset is produced by `pipeline/02_features/extract_stress_bouts.py` (to be built after this MD locks). The script's responsibilities:

- Read `monitoring_b` FIT files via the shared [`Monitoring16Resolver`](../analyses/garmin_exploration/scripts/fit_utils.py) — never re-implement inline.
- Detect bouts per §3.
- Compute per-bout features per §4.
- Join `dose_plasma_mg(d)` + `citalopram_phase(d)` + `is_unmedicated(d)` per [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md).
- Emit `per_bout_master.csv` (gitignored; lives in `$GEVOELSCORE_DATA_PATH`) + `per_bout_master.parquet` (faster downstream load).
- Emit the per-day aggregations table (per §4) joined to `per_day_master.csv` via the existing consolidation step.

**Out of scope for the script**: any inference / hypothesis test. The script is a producer-mode extractor; tests live in their per-HA folders.

### 7.5 Other methodology MDs this MD depends on

- [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) — Garmin stress derivation; sleep-window collapse; motion-gap handling.
- [`permutation_null_block_length.md`](permutation_null_block_length.md) — day-level E[L]=7 stationary bootstrap; inherited verbatim for §5.1.
- [`stress_low_motion_primitive.md`](stress_low_motion_primitive.md) — motion-proxy operationalisation reused for §3.4 `motion_confound_flag`.
- [`time_resolution.md`](time_resolution.md) — scale-choice discipline; §6 of that MD's mechanism-driven-scale rule is what authorises bout-level here.
- [`citalopram_dose_response_stress_mean_sleep.md`](citalopram_dose_response_stress_mean_sleep.md) — daily-aggregate β baseline + the methodological pattern (afbouw / buildup-post-CPAP / spring-2025-control) the bout-level recalibration sub-MD inherits.
- [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md) — four-phase axis + Approach §5.A/B/C framework; §5.3 of this MD applies the same framework at the per-bout layer.
- [`nightly_attribution.md`](nightly_attribution.md) — sleep-window attribution for §3.2 sleep-boundary truncation + §4 `bout_during_sleep_flag`.
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) — the downstream HA pre-reg lock arc; named here so the cascade order is auditable.

### 7.6 Sister methodology MD (sub-MD)

[`bout_level_dose_response_calibration.md`](bout_level_dose_response_calibration.md) — bout-level β re-calibration per §5.4. Drafted in the same session as this MD (r1 of both lands together).

---

## 8. Caveats

Per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), caveats are honestly framed: they acknowledge what is uncorrected or unresolved without pre-emptively immunising against findings.

1. **Bout-detection thresholds are calibration choices, not derived constants.** The §3.1 + §3.2 + §3.3 thresholds (60-onset, 50-floor, 60-min separation, 5-point return tolerance, 180-min cap, 30-min pre-bout window) are pre-committed structural choices. The choice surface is large; a different threshold set could produce a different bout count and per-feature distribution. The sensitivity arms (§3.1.1 + §3.2.1 + §3.3) hedge the headline against the most plausible alternatives; the framework-validity gate (§6) is the empirical check on whether the choice produces an operand that re-detects a signal we trust. If the framework-validity gate clears at the headline choice but fails at a sensitivity-arm choice (e.g. S75 threshold), that's a robustness-of-operand finding, not a fatal flaw.

2. **The recovery_half_life feature has a hard cap at 180 min** (the §3.2 return-window cap). Bouts whose half-recovery exceeds 180 min are coded as 180 with `did_not_half_recover_flag = True`. This is the bout-level analogue of HA-C4 v2 Channel 1's NaN-as-positive encoding. Downstream pre-regs reporting `recovery_half_life` distributions must explicitly report the cap-hit frequency per arm; a difference in cap-hit frequency between arms IS a finding in its own right (the C4-positive case is more common after heavy-T) and should not be silenced by the cap.

3. **The dose-adjustment in Approach A depends on the recalibration β being correct.** The sub-MD provides 95% CIs on the per-feature β; downstream pre-regs using Approach A should report the sensitivity of their verdict to the upper / lower CI bounds of the relevant β. If the verdict swings under the CI range, that's a β-precision finding the recalibration sub-MD should be informed of.

4. **n=1 single-subject + observational + multi-source.** Per [`wiggers_test_design_on_chained_regime.md` Cross-cutting statistical hygiene §1-§4](wiggers_test_design_on_chained_regime.md#cross-cutting-statistical-hygiene), every project pre-reg inherits these. Bout-level analysis does not relax them. The per-bout features are *operational* descriptions of the Garmin trace; they are not mechanistic measurements of autonomic state. Findings on the operand are findings about the trace, not about the underlying physiology.

5. **The framework-validity gate is restricted to unmedicated × train era × calm days** (§5.5 + §6). The gate's pass/fail status does NOT speak to operand fidelity in OTHER conditions; reproduction of HA11 in validate era / medicated phases / heavy-T days is substantive, not framework-validity. A reader who expects the framework-validity gate to be a global validation will be disappointed; the gate is narrow on purpose.

6. **Within-day bout count is bounded above** by daily structure (waking hours / sleep architecture / activity timing). Some days will have many bouts (~5-8); some will have few (~1-2); some will have zero (true calm days). The downstream `bout_n_fast_recovery_day` feature has a floor at zero by construction — z-score against a lagged baseline is bounded below; per HA11's experience (§4.5) the lagged σ flat-floor is a real failure mode at bout-level too. Pre-regs using the count must include the same low-variability flag handling.

7. **Motion-confounded bouts are kept in primary.** Per §3.4 (handoff §5 decision #6). Wiggers C4's verbatim wording includes "despite resting", which has been operationally tested via HA-C4b (NOT-SUPPORTED). Keeping motion-confounded bouts in primary preserves the framework-validity gate's reference frame (HA11 v1 did not filter motion). Downstream pre-regs that want the Wiggers-verbatim "rest" framing should add motion-clean-only as a sensitivity arm explicitly; the primary verdict on this MD's operand will include motion. Disagreement between primary and motion-clean-only IS a finding about whether the bout-level signal is motion-driven.

---

## 9. Educated assessment of non-enabled Wiggers register rows

Per handoff §1 item 7 + §5 decision #9, this section records the methodology MD writer's educated assessment of which Wiggers register rows would benefit from bout-level analysis. The forward-pointer updates to the affected register-row documentation (per §10 commit plan) reference this section as their rationale.

The assessment scans the Wiggers register sections A-I (per `wiggers_testable_hypotheses.md`); judges each row on (1) does the row's mechanism operate at within-day recovery resolution? (2) would bout-level analysis improve on the current operationalisation? (3) is the row test-able at bout-level given this MD's operand?

### 9.1 Rows judged "would benefit" (forward-pointers added)

- **A4** (sustained multi-hour RHR elevation). The current `hr_sustained_elevated_flag` + `hr_longest_elevated_run_min_waking` family is bout-shaped already (an elevated run IS a bout-like construct on the HR channel); the bout-level framework here adds per-bout *recovery* features that the current operationalisation does not capture. A bout-level HR-channel variant (peak HR, recovery half-life on HR, decay slope on HR) would be a natural sister to this MD's stress-channel operand. **Forward-pointer rationale**: bout-level recovery dynamics would extend A4's occurrence+duration framing with within-bout recovery shape on the HR channel.
- **C1** (night orange stress elevated on PEM days). Currently tested via the `stress_mean_sleep` proxy (per [HA11 secondary § + `wiggers_testable_hypotheses.md` C1 row](../wiggers_testable_hypotheses.md#c-stress-score-garmin-daytimennight-hrv-derived)), which collapses the within-sleep stress dynamic to one mean. Bout-level within-sleep recovery shape would resolve the structure the mean collapses. **Forward-pointer rationale**: bout-level recovery dynamics would resolve the within-sleep decay question C1 tests at daily-aggregate.
- **C4b** (motion-filter crash-precursor). Currently operationalised as a per-day count of stress-with-low-motion minutes; HA-C4b v3 NOT-SUPPORTED on the headline. Bout-level reframing could discriminate between "many short bouts" vs "few sustained bouts" in the same per-day count; the HA-C4b v3 §9 NOT-SUPPORTED branch's alternative reading (PROTECTIVE-not-PREDICTIVE OR emotionally-triggered crashes) might be discriminable via per-bout features that the per-day count cannot resolve. **Forward-pointer rationale**: bout-level features would discriminate within the C4b primitive at finer resolution than the per-day count.
- **H4** (parasympathetic swing). Currently operationalised as a BB-anchored composite (per `wiggers_testable_hypotheses.md` H4 row); bout-level per-event characterisation could isolate swing events from steady-state. **Forward-pointer rationale**: bout-level per-event characterisation could isolate the swing event the daily-aggregate composite cannot resolve.

### 9.2 Rows judged "weak benefit" or "not bout-level" (no forward-pointer)

- **A1, A2, A3** (RHR dose-scaling, bidirectional deviation, peri-event night RHR): dose-response / peri-event framings; not within-day recovery dynamics.
- **B1-B5** (HRV / proxy stress claims): mostly multi-day or per-night aggregate. B4's "sudden HRV spike" could marginally benefit from per-bout characterisation but the current proxy operationalisation collapses to per-night already; bout-level adds little.
- **C2, C3** (daily stress → next-day recharge, non-linear stress → fatigue): daily aggregate by construction.
- **D1-D5** (BB-level / BB-dynamics / morning BB after overexertion): daily aggregate or peri-event; per-bout BB analysis is blocked on H04b path C (per-minute BB not yet extracted).
- **E1-E3** (steps / activity load): dose-response or cumulative; not bout-shaped.
- **F1-F4** (sleep duration / deep-sleep / sleep score / bedtime variance): sleep-window aggregates.
- **G1-G4** (respiration / temperature / pressure / SpO2): mostly daily aggregate or external join.
- **H1, H2, H3, H5** (wearable-leads-felt / activity-invisible / illness-vs-PEM classifier / lag profile): peri-event or cross-channel CCF; per-bout features could enter as additional CCF channels but the framing is multi-day not bout-shape.

### 9.3 Forward-pointer plan (per §10 commit)

Add a one-line `## Future work — bout-level analysis` note (or equivalent column-edit) to the §9.1 rows in `wiggers_testable_hypotheses.md`, pointing at this MD as available infrastructure. The note carries the one-line rationale verbatim from §9.1. Does NOT pre-author the would-be pre-reg for the row; future authors invoke the methodology MD when they pre-reg.

---

## 10. Status + revision log

**Status**: drafted r1 2026-06-19. NOT LOCKED. Awaiting fresh-session `/research-methodology-review` audit per [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice).

### Revision log

| version | date | change |
|---|---|---|
| r1 | 2026-06-19 | Initial draft as producer-mode methodology MD post-HA-C4 v2 REJECTED. Narrow lock scope (C4 + HA11 only), cross-phase IS in scope with Approach A headline, bout-level β re-calibration committed as sub-MD ([`bout_level_dose_response_calibration.md`](bout_level_dose_response_calibration.md)), framework-validity gate via HA11 v1 reproduction restricted to unmedicated stratum × train era × calm days. Educated assessment + forward-pointers for A4 / C1 / C4b / H4 in §9. |

---

## 11. Cross-references

- [CONVENTIONS §1.1, §2.2, §3.1-§3.7, §4.1-§4.3](../CONVENTIONS.md) — producer-mode + four-input bar + audit hooks + interpretive discipline.
- [HA-C4 v2 hypothesis.md](../analyses/hypotheses/HA-C4/hypothesis.md) + [result.md](../analyses/hypotheses/HA-C4/result.md) — the daily-aggregate verdict that drove the bout-level pivot.
- [HA11 hypothesis.md](../analyses/hypotheses/HA11-stress-udip/hypothesis.md) + [result.md](../analyses/hypotheses/HA11-stress-udip/result.md) — the SUPPORTED-on-train signal that the framework-validity gate references.
- [HA-C4b v3 hypothesis.md](../analyses/hypotheses/HA-C4b/hypothesis.md) + [result.md](../analyses/hypotheses/HA-C4b/result.md) — sister motion-filter test; NOT-SUPPORTED; bout-level reframing is named as enabled-on-request candidate in §9.1.
- [`bout_level_dose_response_calibration.md`](bout_level_dose_response_calibration.md) — sub-MD with bout-level β recalibration per §5.4.
- [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md), [`permutation_null_block_length.md`](permutation_null_block_length.md), [`stress_low_motion_primitive.md`](stress_low_motion_primitive.md), [`time_resolution.md`](time_resolution.md), [`citalopram_dose_response_stress_mean_sleep.md`](citalopram_dose_response_stress_mean_sleep.md), [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md), [`nightly_attribution.md`](nightly_attribution.md), [`hypothesis_lock_process.md`](hypothesis_lock_process.md), [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) — methodology MDs this MD depends on (§7.5).
- [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) — Wiggers register; C4 row + A4 / C1 / C4b / H4 rows receive forward-pointers per §10 commit plan.
- [`personal_hypotheses.md`](../personal_hypotheses.md) — sibling register; no direct forward-pointer from this MD (HA11 is project-original, not a Personal-register P-entry).

---

*Producer-mode methodology MD. Update when (a) the framework-validity gate's result lands and informs whether the operand stands or needs revision, (b) the recalibration sub-MD's per-feature β coefficients land and inform Approach A's headline numbers, (c) a downstream HA pre-reg surfaces an operand refinement.*
