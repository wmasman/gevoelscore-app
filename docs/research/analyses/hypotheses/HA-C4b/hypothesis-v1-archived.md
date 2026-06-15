# HA-C4b — Stress-with-low-motion minute count as crash precursor (Wiggers C4 + motion filter)

## Authorship

**Drafted 2026-06-15** by Claude (Opus 4.6) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. Drafting session had shared context with Session E (the [`stress_low_motion_primitive` MD](../../../methodology/stress_low_motion_primitive.md) + the extraction script) and Session D (the [`citalopram_phase_stratification` framework](../../../methodology/citalopram_phase_stratification.md)); pre-reg follows the [HA11 pre-reg pattern](../HA11-stress-udip/hypothesis.md).

**Revision 2026-06-15-r1** (same session, post-viz). Three changes absorbed from the [stress_low_motion_viz session findings](C:/Users/Gebruiker/Documents/gevoelscore-data/analyses/stress_low_motion_viz/viz-notes.md) BEFORE the fresh-session audit gate ran (per CONVENTIONS §1.2 the pre-reg may be revised freely until lock):
- **§4.3 wake-window coverage gate added** (1b.i and 1b.ii sub-gates). The viz Family A 2024-11-26 case showed the HA11-inherited 600-sample gate admits days with multi-hour device-off gaps; HA-C4b strictens to ≥ 900 total + per-quartile coverage to ensure comparable per-day coverage.
- **§4.11 construct-disambiguation reordered**. The viz Family D2a finding showed ρ(primary, `stress_high_duration_min`) = 0.79 — a closer sibling than HA11's `u_dip_count` (ρ = 0.556). The motion-filter-doing-analytical-work question is more critically tested against `stress_high_duration_min`; that sibling becomes the PRIMARY disambiguation, with `u_dip_count` repositioned to SECONDARY. The original ρ = 0.556 construct-validity finding stands as the closest WITHIN-DAY-SHAPE sibling check.
- **§4.11 u_dip_count gap note added**. HA11's source CSV last extracted 2026-06-07; days 2026-06-08+ in `per_day_master.csv` have `u_dip_count == ""`. Since the validate window ends 2026-06-05, this does NOT affect HA-C4b's test sample but is documented for downstream consumers.

**Revision 2026-06-15-r2** (same session, post-audit). Six changes absorbed from the [fresh-session `/research-review` audit report at `docs/research/reviews/HA-C4b-2026-06-15.md`](../../../reviews/HA-C4b-2026-06-15.md) (verdict: REVISION RECOMMENDED). The audit ran post-r1 on commit `aec1312` in a fresh session with doc-only knowledge; the report's "What would strengthen this finding" list is implemented in this r2:
- **§4.9 null sample replaced** with stationary-bootstrap permutation null at `E[L] = 7` per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) (closes L3.1 / L3.4 substantive Layer-3 fires). HA11 family null inherited the pre-MD random-non-overlapping-reference-date construction; HA-C4b is post-MD and adopts the canonical default. Data-driven `E[L]*` companion + factor-of-2 flag rule added per the MD's operational consequences §2.
- **§5.0 multi-comparison discipline added** as a hard rule: the headline locks on a single pre-specified cell (consolidation × `S60_Mlow` × `N_std = 1.5` × primary 4d × one-sided); all other 9-column × 3-tier × 4-phase × {primary, secondary} × {one-sided, bidirectional} arms are diagnostic / sensitivity ONLY, no independent SUPPORTED bar. Closes L3.3 substantive Layer-3 fire.
- **§4.11.1 Spearman crash-drop sensitivity row added** per CONVENTIONS §3.4 binding audit hook (closes L4.4 Layer-4 minor fire). Reports ρ on full sample AND with `is_crash == True` dropped; `|Δρ| > 0.10` flagged.
- **§4.10 sensitivity ladder rewritten** to acknowledge 6 unique columns + 3 identical-by-construction duplicate columns (the M=below_mod placeholder per [stress_low_motion_primitive §3.2](../../../methodology/stress_low_motion_primitive.md)); closes L4.3 Layer-4 minor fire per CONVENTIONS §3.3.
- **Side observation date arithmetic fixed**: buildup CPAP-end buffer is 21 days (not 22) — "first 21 days of buildup: 2024-04-09 through 2024-04-29 inclusive"; eligibility is "strictly before 2024-04-30" — updated in §4.4 + §6.
- **Side observation afbouw label clarified**: §4.4 table row relabelled "afbouw (post-afbouw merged, see prose)" to remove ambiguity in the merge.

The 5th audit recommendation ("anchor the post-viz revision's cited values in the repo") is acknowledged but not addressed in this revision — the viz-notes.md at `$GEVOELSCORE_DATA_PATH/analyses/stress_low_motion_viz/viz-notes.md` remains external to the audit-able tree. The cited ρ values (0.79 and 0.556) ARE reproducible from a single script run; queued as a separate documentation task for the next pre-reg-touching commit.

**Revision 2026-06-15-r3** (same session, pre-lock interpretability augmentation). Per seasoned-peer-review sanity check + user direction:
- **§5.1 (b-interp) added**: report Risk Difference (RD) and Odds Ratio (OR) with bootstrap 95% CIs alongside the (b) 15pp gate, plus a worked-example interpretation block. This is an interpretability augmentation for external readers, NOT a new falsification conjunct (the (a)+(b)+(c) bar is unchanged). Uses the same B = 10,000 stationary-bootstrap resamples already specified in §4.9. Closes the community-standard external-interpretability gap identified in the sanity check.

**Status: LOCKED 2026-06-15 by user acceptance.** The pre-registration is locked at the state of revision r3 (this file's HEAD). Further modifications create HA-C4b-v2 with v1 archived. The next session writes `test.py` + runs + emits `result.md` per §10.

---

**Pre-registration written 2026-06-15, BEFORE any test run on the new primitive's discrimination against `is_crash`.** Locked at user acceptance. Any subsequent change creates an HA-C4b-v2.

HA-C4b tests Wiggers' "stuck sympathetic / walls of orange" pattern ([Wiggers C4, PDF lines 1140-1143, 1223-1231](../../../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic)) refined with the participant's lived **motion filter** ([garmin_pacing_practice §3.3](../../../methodology/garmin_pacing_practice.md#33-stress-when-at-rest)): elevated Garmin stress *while concurrent body motion is low* — discriminates true sympathetic-arousal-while-at-rest from motion-artefact stress readings.

**HA-C4b is the first test in the project to consume:** (a) the Session E `stress_low_motion_min_count_*` primitive ([extracted 2026-06-15](../../../pipeline/01_extract/stress_low_motion_extract.py)); (b) the Session D [citalopram_phase_stratification §5.B](../../../methodology/citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests) dose-adjustment framework. Validates the build-and-test loop established by Sessions D + E.

## 1. Claim

In the **4 days** before a `crash_v2` episode (primary) and the **5 days** before a `crash_v2` episode (secondary), conditioned on `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T OR T-1, at least one day's `stress_low_motion_min_count_S60_Mlow` deviates from its lagged personal baseline by `(count − μ) / σ ≥ N_std` (N_std locked in §4.8; one-sided ELEVATED direction). The crash-episode frequency of this deviation is discriminative against randomly-sampled non-crash windows in **both train and validate windows independently**.

A bidirectional sensitivity arm reports the `|z| ≥ N_std` result. The primary direction is one-sided elevated (more stress-low-motion minutes = more sympathetic-while-at-rest events = pre-crash precursor) per Wiggers C4's "walls of orange" framing.

Secondary descriptive outcomes:
- Same-day correlation between `stress_low_motion_min_count_S60_Mlow` and `gevoelscore` (Spearman; descriptive only; no SUPPORTED bar).
- Construct-disambiguation against HA11's `u_dip_count` on the same lead-up windows (does HA-C4b fire on episodes HA11 does not, and vice versa?).
- Respiration-companion sensitivity: report whether episodes that fire on the primary ALSO have elevated `n_minutes_resp_above_18` in the lead-up (suggesting motion-or-arousal that the intensity filter may have missed).

## 2. Why we think this

- **Wiggers documents the C4 "stuck sympathetic" pattern in detail** in *Smartwatch Pacing* (2025-07). PDF lines 1140-1143 + 1223-1231 frame it as stress failing to drop during rest after overexertion. Wiggers' framing is post-exertion-conditioned, which is preserved here via the exertion-conditioning rule.
- **The motion filter is the participant's lived-experience refinement** ([garmin_pacing_practice §3.3](../../../methodology/garmin_pacing_practice.md#33-stress-when-at-rest)). The participant operationally reads "elevated stress WHILE BODY IS NOT MOVING" — not "elevated stress alone" — because Garmin stress is partly motion-sensitive ([hrv_proxy_via_stress §2](../../../methodology/hrv_proxy_via_stress.md#2-how-garmin-stress-is-derived)) and minutes with concurrent steps may inflate stress without sympathetic arousal.
- **Construct validity already established on the primitive**. Session E's validation showed:
  - ρ(`stress_low_motion_min_count_S60_Mlow`, HA11's `u_dip_count`) = **0.556** — moderate; same construct family (sympathetic-while-at-rest), not redundant; the primitive carries information HA11 does not.
  - ρ(`n_minutes_resp_above_18`, `u_dip_count`) = **0.044** — orthogonal; the respiration companion adds genuinely independent signal.
  - Threshold ordering monotonic across all 9 sensitivity cells.
  - Spot-check 2026-03-20 (citalopram afbouw start): 124 primary-col minutes vs ~56 median, consistent with the dose-response cascade.
- **Multiple sibling SUPPORTED autonomic-deviation precursors on this corpus**: H02b stress spike count (train), H02d sentinel-corrected spike (train), HA06b RHR z-score (train), HA10 morning BB peak (validate-era SUPPORTED). A within-day-pattern + motion-filter test on a primitive that has 0.556 construct-relation to the closest within-day sibling (HA11) is the obvious next test.
- **C4b's primitive is dose-modulated** per [citalopram_dose_response §5.6](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14). The pre-reg adopts the [phase_stratification §5.B treatment](../../../methodology/citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests) so the dose-response confound does not contaminate the test. This is the first project test to operationally apply that framework end-to-end.

## 3. Data sources

- **Crash labels**: `crash_v2` from [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv). HA-C4b uses crash_v2 (not crash_v1 like HA11) because crash_v2 is now the project default and the dose-response narrowing emphasised it.
- **Predictor primitive**: 9 stress×motion count columns + 2 respiration companions in `per_day_master.csv`, extracted by [`pipeline/01_extract/stress_low_motion_extract.py`](../../../pipeline/01_extract/stress_low_motion_extract.py) per [`methodology/stress_low_motion_primitive.md`](../../../methodology/stress_low_motion_primitive.md). 1739 days covered (1722 valid via the ≥ 600-stress-sample gate).
- **Exertion class**: `exertion_class_lagged_lcera` column in `per_day_master.csv` (built from [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md)'s exertion-class definition with the `_lagged_lcera` rolling-baseline pattern per [CONVENTIONS §3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses)). Values: `{none, light, moderate, heavy, very_heavy}`.
- **Citalopram phase + plasma dose**: `dose_plasma_mg` column in `per_day_master.csv` (PK-smoothed per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification)); phase derivable from the date via the `citalopram_phase(d)` function in that MD §3.
- **HA11 sibling for construct disambiguation**: `u_dip_count` column from [HA11's udip_counts.csv](../HA11-stress-udip/udip_counts.csv) (joined on `date`).
- **Analysis window + train/validate split**: same as HA11 / HA06b / HA10 (train 2022-09-03 → 2023-12-31; validate 2024-01-01 → 2026-06-05). Total `crash_v2` episodes in scope and the heavy-exertion-conditioned subset are reported at the §10.1 dry-run gate; estimated 100-200 days in the conditioned subset across the LC era.

## 4. Measurement protocol

### 4.1 Predictor primitive — `stress_low_motion_min_count_S60_Mlow` (locked)

Definition per [`methodology/stress_low_motion_primitive.md` §4](../../../methodology/stress_low_motion_primitive.md):

> Per-day integer count of minutes on day `d` where `stress(t) >= 60` AND Garmin's per-bin `intensity ≤ 1` (sedentary or low active) OR no `intensity` record covers minute `t`.

The primitive's full operationalisation (FIT-walk pattern, per-minute joining of `stress_level` + `monitoring` messages with bisect-based "most-recent-or-current" intensity lookup, day-validity gate ≥ 600 in-range stress samples) is locked in the methodology MD §3-§5 and implemented in [`extract_stress_low_motion_minutes.csv`](../../../pipeline/01_extract/stress_low_motion_extract.py). No re-derivation in this pre-reg.

### 4.2 Exertion-conditioning rule (locked)

For each day `d`:

- Read `exertion_class_lagged_lcera` on day `d` (the day being evaluated) and day `d − 1`.
- A day is **C4b-eligible** if `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on **`d` OR `d − 1`** (union, not intersection — either day being heavy is sufficient to qualify `d` as "post-exertion" per Wiggers C4's framing).
- Days where `exertion_class_lagged_lcera` is missing on both `d` and `d − 1` are flagged *insufficient-exertion-data* and excluded.

This restricts the test sample to the "after overexertion" condition that Wiggers C4 specifies.

### 4.3 Day validity (revised post-viz 2026-06-15)

A day is **valid for HA-C4b** if **all** of:

1. The primitive's stress-sample day-validity gate passes (≥ 600 in-range stress samples; the `valid` flag from the extraction is 1). **HA11 inherits this 600 gate; HA-C4b strengthens it (see 1b).**
1b. **Wake-window coverage strictness** (HA-C4b-specific gate, added 2026-06-15 post-viz). The Session E validation gate (≥ 600 samples) is permissive: per the [stress_low_motion_viz session](C:/Users/Gebruiker/Documents/gevoelscore-data/analyses/stress_low_motion_viz/viz-notes.md) Family A 2024-11-26 case, a day with a **9-hour mid-day stress gap** passed the 600-sample gate at 662 samples — but its primary count of 0 is ambiguous between "genuinely quiet wake-period" vs "device off during the active part of the day". For HA-C4b a stricter gate applies:
   - **(1b.i) Total in-range samples ≥ 900** (stricter than HA11's 600) — catches partial-day device-off cases.
   - **(1b.ii) Wake-window quartile coverage**: when `sleep_start_gmt` and `sleep_end_gmt` are both available, divide the day's non-sleep period into 4 equal-length quartiles. Each quartile must contain ≥ 50 in-range stress samples. When sleep boundaries are NOT available, fall back to fixed-time quartiles `[06:00-12:00, 12:00-18:00, 18:00-22:00, 22:00-02:00]` (local time), each ≥ 50 samples.
   - Days failing 1b.i OR 1b.ii are flagged *wake-coverage-insufficient* and excluded. Report fractions.
2. The exertion-conditioning rule (§4.2) is satisfied.
3. The day has a `crash_v2` label (i.e. is not a censored day).

Days failing any of these are flagged and excluded from the test sample. Report fractions.

**Why HA-C4b strictens beyond HA11**: HA-C4b's predictor is a **count-of-low-motion-minutes** that defaults "no record" minutes to "low motion" per §3.2 of the primitive MD. A day with extensive device-off coverage during the wake period would systematically under-count the primary (because device-off minutes do not contribute stress samples at all, not even to the no-record-default low-motion class). This biases the test in two directions: low counts on partial-coverage days look like "rest days" but are really "missing-data days", and the lagged baseline includes those biased-low days, lowering μ and inflating future z-scores. The wake-window gate ensures the comparison is on **comparable coverage** across days.

### 4.4 Citalopram phase-stratified treatment (per §5.B framework, locked)

The primary test is **per-phase stratified** ([phase_stratification §5.A](../../../methodology/citalopram_phase_stratification.md#5a-per-phase-stratification-the-default-lowest-risk)) — separate sub-test within each of the 4 LC-era Citalopram phases:

| phase | window | n estimate (heavy-exertion subset) |
|---|---|---|
| unmedicated | LC start 2022-04-04 → 2024-04-08 | ~50-100 |
| buildup | 2024-04-09 → 2024-06-19 | ~10-20 |
| consolidation (30mg plateau) | 2024-06-20 → 2026-03-19 | ~80-150 |
| afbouw (post-afbouw merged, see prose) | 2026-03-20 → 2026-06-05 | ~10-20 |

Per-phase n's are estimates; actual counts gate at §10.1 dry-run.

**Rationale for per-phase rather than dose-adjusted-predictor (§5.B) primary**: dose-adjustment of a COUNT metric is non-trivial — `β_dose = +0.57/mg` (the all_day_stress_avg confirmed coefficient) acts on per-minute stress values, not on per-day counts. To apply §5.B properly the threshold would need to shift per-day (`S_adj(d) = 60 + 0.57 × dose_plasma_mg(d)`), requiring a re-extraction of the primitive. **For HA-C4b v1 the per-phase test is the primary**; a dose-adjusted-threshold sensitivity arm is queued as future work (would require a §5.B-aware re-extraction).

**Buildup + afbouw + post-afbouw n is small** (~10-30 each). For buildup specifically, the 2024-04 boundary-collision per [intervention_effects_descriptive §8.1](../../../methodology/intervention_effects_descriptive.md#81-effective-analyzable-scope-5-of-8-boundaries-usable) makes the first ~21 days of the phase confounded with CPAP-end. Apply [phase_stratification §5.A's optional ±N-day boundary buffer](../../../methodology/citalopram_phase_stratification.md#5a-per-phase-stratification-the-default-lowest-risk) — exclude buildup days **strictly before** 2024-04-30 (the first 21 days of buildup: 2024-04-09 through 2024-04-29). Report buildup separately as "buildup post-CPAP-buffer". The 9-day post-afbouw window before data-cut is too short for an independent test; **merge into afbouw** (table label below: "afbouw (post-afbouw merged, see prose)") rather than reporting as a separate phase.

The **headline verdict** is the **consolidation-phase verdict** (largest n, longest plateau, dose-state stable). Unmedicated is the secondary independent confirmation. Buildup-post-CPAP-buffer + afbouw report as low-power complements.

### 4.5 Lagged personal baseline (per CONVENTIONS §3.2)

For each valid day `d`:

- Baseline window: days in `[d − 90, d − 30]` (60-day window).
- **Baseline restricted to LC-era days only** (`_lagged_lcera` discipline per [CONVENTIONS §3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses)) — exclude pre-2022-04-04 days from the baseline window even when `d − 30` reaches into pre-LC dates.
- **Baseline restricted to days in the same Citalopram phase as `d`** — exclude prior days that are in a different phase. This enforces the per-phase discipline locked in §4.4 inside the baseline construction as well as the test sample. Days early in a phase with insufficient same-phase prior days are flagged *insufficient-baseline* and excluded.
- **Baseline restricted to days valid per §4.3** — exclude prior days that were insufficient-coverage or missing exertion-conditioning data.
- **Baseline mean (μ)**: trimmed mean (10/90 cut) of `stress_low_motion_min_count_S60_Mlow` values across the prior days that satisfy the above filters.
- **Baseline std (σ)**: stdev of the same trimmed values.
- Computed only when ≥ 40 of 60 eligible prior days are valid AND same-phase.
- If σ ≤ 5 minutes — i.e. the baseline is essentially flat — flag the day as *low-variability* and skip it in the test. Report fraction.

### 4.6 Per-day z-scored count

For each valid day `d` with both `stress_low_motion_min_count_S60_Mlow(d)` and a defined (μ, σ) pair:

- `delta(d) = stress_low_motion_min_count_S60_Mlow(d) − μ(d)`
- `z(d) = delta(d) / σ(d)`
- `|z(d)| = abs(z(d))`

### 4.7 Per-episode lead-up profile

Identical to HA11 / HA06b / HA10:

- 4-day primary lead-up: [C-4, C-3, C-2, C-1].
- 5-day secondary lead-up: [C-5, C-4, C-3, C-2, C-1].
- Min valid days: 3 of 4 for primary; 4 of 5 for secondary.
- Episode trigger flag (one-sided elevated, primary): `max_signed_z ≥ N_std`.
- Bidirectional sensitivity arm: `max |z| ≥ N_std`.
- Record direction of max-|z| day and all signed z values.

### 4.8 Threshold N_std

Three pre-registered thresholds, consistent with HA06b / HA10 / HA11:

| Tier | N_std | Anchor |
|---|---:|---|
| Primary | **1.5** | mild-to-moderate deviation |
| Secondary | **2.0** | classical outlier threshold |
| Sensitivity check | **2.5** | strict |

The **primary tier (N_std = 1.5) determines the headline verdict**; secondary and sensitivity check are reported alongside.

### 4.9 Null sample — stationary bootstrap with E[L] = 7 (revised post-audit 2026-06-15)

**Revised from inherited HA11/HA06b/HA10 random-non-overlapping-reference-date construction** per the [`/research-review` audit 2026-06-15](../../../reviews/HA-C4b-2026-06-15.md) Layer-3 substantive finding [L3.1 / L3.4]. The original HA11-family null machinery predates the project-default block-permutation policy in [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) and was silent on within-window serial dependence. HA-C4b is a new pre-reg post-MD and adopts the canonical default.

#### 4.9.1 Project-default null machinery (locked)

Per [`permutation_null_block_length.md` "Operational consequences" §2](../../../methodology/permutation_null_block_length.md):

- **Stationary-bootstrap permutation null** with **expected block length `E[L] = 7` days** as the project-wide default. Block lengths drawn from a geometric distribution with mean `E[L]`.
- **Block-permute the crash / null episode labels** across the per-phase eligible pool (preserving within-block dependence of the predictor time-series).
- **B = 10,000 resamples** for the headline; B = 1,000 for the sensitivity-ladder diagnostics.
- **Random seed**: `20260615` (HA-C4b-specific, distinct from HA11's `20260605` because the resampling machinery is different — fresh seed to avoid spurious cross-test correlation in the null draws).

For each (phase × N_std tier × window B/sensitivity column) cell evaluated:
- Compute the observed crash-episode trigger frequency on the actual labels (per §4.7).
- Repeat B times: draw a stationary-bootstrap relabeling of the per-day `is_crash` time series (block lengths ~ Geometric(1/7)); recompute the trigger frequency under the relabeled sample; record.
- p-value = fraction of B null draws where the bootstrap trigger frequency ≥ observed trigger frequency.

#### 4.9.2 Data-driven block-length confirmation (companion)

Per the methodology MD's "data-driven confirmation step is the safeguard against this default being wrong for a specific metric": **report `E[L]*`** — the data-driven estimated block length for the primary column's autocorrelation structure across the consolidation-phase eligible-day pool — alongside the headline `E[L] = 7` result.

- Compute `E[L]*` via the canonical empirical-ACF-based automatic block-length estimator (specific algorithm queued in [`_pending_literature_fetch.md`](../../../methodology/_pending_literature_fetch.md); first-principles fallback implementation if not yet landed).
- **Report rule**: if `|E[L]* − 7| / 7 > 0.5` (i.e. `E[L]*` is outside `[3.5, 10.5]` days), **flag for review before locking the verdict** per the methodology MD. The flag is a hard halt on the headline; the verdict requires re-evaluation at `E[L]*` with the user's approval.

#### 4.9.3 Why this matters

The audit's L3.1 / L3.4 concern: under correlated lead-up windows, the random-non-overlapping-reference-date null underestimates the null trigger frequency, inflating apparent discrimination. The §5 (b) 15-percentage-point margin under the stationary-bootstrap null may compress materially. The block-permutation null preserves within-block autocorrelation in the resampled crash-vs-non-crash labels, restoring the null's calibration.

This adoption simultaneously satisfies the [`citalopram_phase_stratification.md` §6 "Independent obligations"](../../../methodology/citalopram_phase_stratification.md#6-pre-registration-template-for-new-hypothesis-mds) binding that framework adopters engage autocorrelation handling — HA-C4b is a framework adopter via §4.4 and was previously silent on this obligation.

#### 4.9.4 Per-phase eligibility for the null

Only days satisfying §4.3 validity AND §4.5 baseline-availability are eligible as block-permutation inputs. Per-phase eligible pool sizes are reported at the §10.1 dry-run gate; the stationary bootstrap operates within the per-phase eligible pool (no cross-phase resampling).

### 4.10 Sensitivity ladder report (revised post-audit 2026-06-15)

**Revised from 9-column-as-independent-arms framing** per the [`/research-review` audit 2026-06-15](../../../reviews/HA-C4b-2026-06-15.md) Layer-4 finding [L4.3]. The 9-column ladder reduces to **6 unique columns in v1** because the M=below_mod definition is currently identical to M=low (per [`methodology/stress_low_motion_primitive.md` §3.2](../../../methodology/stress_low_motion_primitive.md) — `any_below_moderate` is a placeholder slot for future refinement and currently emits identical values to `low_or_below`). Listing 3 M=below_mod columns as independent sensitivity arms would violate [CONVENTIONS §3.3 "one column per definitional pair"](../../../CONVENTIONS.md#33-one-column-per-definitional-pair).

The sensitivity ladder is therefore reported as **6 unique columns + 3 identical-by-construction duplicate columns**:

| stress threshold | motion class | column name | unique or duplicate |
|---:|---|---|---|
| 50 | strict | `stress_low_motion_min_count_S50_Mstrict` | unique |
| 50 | low | `stress_low_motion_min_count_S50_Mlow` | unique |
| 50 | below_mod | `stress_low_motion_min_count_S50_Mbelow_mod` | **identical-by-construction to `_Mlow` in v1** |
| 60 | strict | `stress_low_motion_min_count_S60_Mstrict` | unique |
| **60** | **low** | **`stress_low_motion_min_count_S60_Mlow`** | **unique — HEADLINE CELL** |
| 60 | below_mod | `stress_low_motion_min_count_S60_Mbelow_mod` | **identical-by-construction to `_Mlow` in v1** |
| 75 | strict | `stress_low_motion_min_count_S75_Mstrict` | unique |
| 75 | low | `stress_low_motion_min_count_S75_Mlow` | unique |
| 75 | below_mod | `stress_low_motion_min_count_S75_Mbelow_mod` | **identical-by-construction to `_Mlow` in v1** |

Per the §5.2 multi-comparison discipline, only the headline cell drives the SUPPORTED verdict; the other 5 unique columns are diagnostic sensitivity arms. The 3 identical-by-construction duplicate columns are emitted into the result CSV for completeness but **are not counted as independent sensitivity arms** (the result.md table caption explicitly states this).

**Within-row monotonicity check (per-day count level)**: for each phase × era, the **per-day median qualifying-minute count** must satisfy S=50 ≥ S=60 ≥ S=75 at each motion class; the trigger-frequency (the §5.1 (a) numerator) inherits this monotonicity by construction (lower threshold → ≥ counts → ≥ frequency at the same N_std), but the per-day count is the more fundamental check. **Across-motion-classes monotonicity**: strict ≤ low ≤ below_mod (the M=below_mod row equals M=low by construction in v1).

Violations of either monotonicity are bugs and require investigation before the headline verdict locks.

### 4.11 Secondary descriptive outcomes

For each calendar day `d` in the test sample:

1. **Same-day gevoelscore correlation**: Spearman(stress_low_motion_min_count_S60_Mlow, gevoelscore) per phase + pooled LC era. Median count per gevoelscore value. Report split by era (train vs validate) AND by Citalopram phase. **Descriptive only; no SUPPORTED bar.**

   **Crash-drop sensitivity row** (added post-audit 2026-06-15 per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions) audit hook): for each Spearman cell (phase × era), report ρ TWICE — once on the full eligible sample, once with `is_crash == True` rows dropped. Surface `|Δρ| > 0.10` as a finding (the correlation was driven materially by crash days, not by the broader distributional relationship). The §3.4 audit hook applies because `stress_low_motion_min_count_S60_Mlow` is a PEM-pacing variable and the §4.11.1 Spearman is a Layer-4 same-day correlation.

2. **Construct-disambiguation against `stress_high_duration_min`** (PRIMARY sibling — added post-viz revision 2026-06-15). Per the [stress_low_motion_viz session findings](C:/Users/Gebruiker/Documents/gevoelscore-data/analyses/stress_low_motion_viz/viz-notes.md) Family D2a, Spearman ρ between the primary column and `stress_high_duration_min` = **0.79** — the closest sibling in the per_day_master.csv. The Family B4a time-series visualisation showed the two lines track closely on the twin axes; **most day-to-day variance is shared.** This raises the critical disambiguation question: **is the motion filter actually doing analytical work, or is the all-day stress-time count sufficient?** For each crash episode in the lead-up:
   - Flag (HA-C4b fires, `stress_high_duration_min` ≥ its own lagged-baseline-z threshold) → 2×2 contingency.
   - The "off-diagonal" cells are the load-bearing reads:
     - HA-C4b fires AND `stress_high_duration_min` does NOT → the motion-filter refinement caught an episode the all-day-stress-time-count missed. **This is the strongest empirical case for the motion filter as a discriminative refinement.**
     - `stress_high_duration_min` fires AND HA-C4b does NOT → the motion filter filtered OUT a real precursor signal; the motion-filter refinement may be overly restrictive. **This is the strongest empirical case against the motion filter.**
   - Concordant on episodes → the motion filter is incremental, not essential; the all-day-stress-time-count is sufficient.

3. **Construct-disambiguation against HA11's `u_dip_count`** (SECONDARY sibling — original intent, post-viz repositioned to secondary). Per Session E validation, ρ(primary, u_dip_count) = **0.556** — moderate; same construct family. The disambiguation question is distinct from #2: u_dip_count picks up within-day SHAPE patterns (pre-dip-post temporal trajectory), HA-C4b picks up within-day CONCURRENCE patterns (stress + low motion at same moment). For each crash episode in the lead-up, flag (HA-C4b fires, HA11 fires) — 2×2 contingency. The off-diagonal episodes are documented for cross-construct understanding.
   - **Note**: HA11's `udip_counts.csv` last extraction was 2026-06-07 (per viz-notes follow-up); days 2026-06-08+ in the master have `u_dip_count == ""`. Since the validate window ends 2026-06-05, this gap does NOT affect HA-C4b's test sample.

4. **Respiration-companion sensitivity**: For each crash episode where HA-C4b fires, report whether `n_minutes_resp_above_18` in the lead-up is also above its lagged baseline (z > 0). If HA-C4b fires AND respiration is also elevated, the apparent "low motion" minutes may have been motion-or-arousal-confounded; if HA-C4b fires AND respiration is NOT elevated, the signal is more credibly "genuine sympathetic at rest". This is a methodological sensitivity, not a verdict.

## 5. Pre-registered falsification criterion

### 5.0 Multi-comparison discipline — single-cell headline lock (added post-audit 2026-06-15)

**Revised from implicit-discipline original** per the [`/research-review` audit 2026-06-15](../../../reviews/HA-C4b-2026-06-15.md) Layer-3 substantive finding [L3.3]. The original §5 phrased the headline as "consolidation phase × N_std primary tier" and reported the other 9-column × 3-tier × 4-phase cells "alongside", which left room for narrative-level upgrading.

**HA-C4b's headline locks on a SINGLE pre-specified cell**:

> Consolidation phase × `S60_Mlow` column × `N_std = 1.5` × primary 4-day lead-up × one-sided elevated direction.

**Hard rule**: ALL OTHER cells in the family (3 stress thresholds × 3 motion classes × 3 N_std tiers × 4 phases × {primary 4d, secondary 5d} × {one-sided, bidirectional}) are **diagnostic / sensitivity arms ONLY**. They are reported in the result.md, but **none of them can promote to a SUPPORTED verdict on their own**. The headline verdict is the single-cell verdict, full stop.

If the result.md narrative wants to invoke a sensitivity-arm verdict ("the unmedicated phase also fired"), it does so as a *diagnostic finding* that informs the headline's *robustness* or *generalisability* — not as a SUPPORTED claim in its own right. This is the project pattern for multi-arm sensitivity ladders: lock the headline cell, the rest are descriptive.

### 5.1 Three-criterion bar (applied to the single locked headline cell)

Identical three-criterion bar shape to H02b / HA01b / HA06b / H02d / HA10 / HA11, applied **to the single locked cell** (consolidation × S60_Mlow × N_std=1.5 × primary 4d × one-sided):

**(a) Frequency**: at least **60%** of consolidation-phase crash episodes have `max signed_z ≥ 1.5` (one-sided) in their lead-up window.

**(b) Discrimination**: the consolidation-phase crash-episode frequency from (a) is at least **15 percentage points higher** than the consolidation-phase **stationary-bootstrap-null frequency** (per §4.9 — block-permutation null at `E[L] = 7`, NOT the inherited random-reference-date null).

**(b-interp) Effect-size reporting (added r3 2026-06-15 for external interpretability).** Criterion (b) is a risk-difference gate at 15pp; the same underlying `p_crash` vs `p_null` discrimination is reported in two community-standard formulations alongside the gate:

- **Risk difference (RD)**: `RD = p_crash − p_null`. Already gated at ≥ 0.15 by criterion (b). Report point estimate + bootstrap 95% CI from the same B = 10,000 stationary-bootstrap resamples specified in §4.9.
- **Odds ratio (OR)**: `OR = (p_crash / (1 − p_crash)) / (p_null / (1 − p_null))`. Report point estimate + bootstrap 95% CI. **Reporting threshold (not a separate falsification conjunct)**: at the §5 (b) gate of `RD = 0.15` with a typical `p_null ∈ [0.10, 0.20]`, the equivalent OR ranges 2.15 to 3.00. An OR < 1.5 with 95% CI containing 1 alongside an apparently-passing RD would be suspect — flag for review.

**Interpretation, worked example**. Suppose the consolidation-phase headline gives `p_null = 0.12` and `p_crash = 0.35` (illustrative; not a prediction):
- RD = 0.35 − 0.12 = **0.23** (23 percentage points; passes the 15pp gate comfortably)
- OR = (0.35 / 0.65) / (0.12 / 0.88) = 0.538 / 0.136 = **3.95** (crash-episode odds are ~4× higher than null odds)
- Reading: "When a heavy-exertion-conditioned crash episode occurs in the consolidation phase, its 4-day lead-up contains a `stress_low_motion_min_count_S60_Mlow` z ≥ 1.5 deviation about 35% of the time, vs ~12% in matched non-crash null windows. The odds of seeing the deviation in a crash lead-up are roughly four times the odds in a null window."

The OR and RD are reported alongside the §5.1 (a)(b)(c) verdicts on the locked headline cell. They are **interpretability augmentation, not additional falsification conjuncts** — the (a)+(b)+(c) bar is what determines SUPPORTED / NOT-SUPPORTED.

**(c) Magnitude**: the median `max signed_z` across consolidation-phase crash episodes is at least **0.75** (N_std / 2 = 1.5 / 2).

Any one of (a), (b), (c) failing at the locked headline cell in either train or validate → **headline refuted**.

### 5.2 Diagnostic / sensitivity arms (no independent SUPPORTED bar)

- **N_std = 2.0 and N_std = 2.5 tiers** applied to the same consolidation × S60_Mlow × primary 4d × one-sided cell: reported as **fragility checks**. A finding that fires at N_std = 1.5 but NOT at 2.0 is fragile-to-threshold; one that fires across all three tiers is robust. None of these promote independently.
- **Other 8 stress × motion cells** at N_std = 1.5: reported as sensitivity-ladder diagnostics for **threshold-monotonicity** (§4.10) and to distinguish whether the motion filter is doing analytical work.
- **Other 3 phases** (unmedicated, buildup-post-CPAP-buffer, afbouw): reported as descriptive companion verdicts. Unmedicated agreement with consolidation = **independent-confirmation** descriptive read. Unmedicated divergence = **concerning-divergence** descriptive read. Neither shifts the headline.
- **Secondary 5d lead-up** + **bidirectional sensitivity arm**: reported as transparency arms. None promote to a SUPPORTED verdict on their own.

### 5.3 Inconclusive bar

- If consolidation has fewer than 10 clean crash episodes per train or validate window after exclusions → **inconclusive on the headline cell** at that window. Re-evaluation possible after additional crashes accumulate.

## 6. Exclusion rules

- Days with fewer than 600 valid per-minute stress samples are excluded (insufficient coverage; same as HA11).
- Days not satisfying the §4.2 exertion-conditioning rule are excluded (NOT in test sample; the test is on the heavy-exertion-conditioned subset only — this is the C4 spec).
- Days where the lagged-same-phase baseline σ ≤ 5 minutes are flagged *low-variability* and excluded.
- Days where fewer than 40 of 60 prior same-phase valid days are available are excluded (insufficient baseline).
- **Buildup phase days strictly before 2024-04-30** (first 21 days of buildup phase: 2024-04-09 through 2024-04-29 inclusive) are excluded from the test sample (CPAP-end confound per [intervention_effects_descriptive §8.1](../../../methodology/intervention_effects_descriptive.md#81-effective-analyzable-scope-5-of-8-boundaries-usable)). Report buildup separately as "buildup post-CPAP-buffer".
- **2024-04-09 to 2024-04-16** (the structurally-unanalyzable 2024-04 boundary cluster per same reference) are excluded from all phase tests.
- **Days in the lead-up window of a confirmed crash episode** are excluded from the null sample (avoid contamination of the null distribution with crash-precursor minutes).

## 7. Expected effect size if hypothesis is true

- 60-80% of consolidation-phase crash episodes have `max signed_z ≥ 1.5` in the 4-day lead-up (mirroring the HA06b / HA10 / HA11 family expectation).
- Null sample rate: 7-20% (one-sided Gaussian tail expectation ~6.7% per day; max over 4 days inflates this).
- Median `max signed_z`: 1.5-2.5.
- **Sanity check on primitive distribution**: per [Session E validation](../../../methodology/stress_low_motion_primitive.md#8-validation-plan), the median `stress_low_motion_min_count_S60_Mlow` on valid days is 56, 90th pct 133, max 364. Within a phase, expect the median to shift per dose-response: ~30-45 unmedicated, ~60-70 consolidation, ~50-60 afbouw (rough estimates; the test does not lock these but flags violations).
- **Sanity check on σ**: if median per-phase baseline σ is < 5 events → spec is too strict (low-variability flag will catch most days). If median σ is > 40 events → spec is too loose (one-day fluctuation drowns the signal).

If either sanity check fails on the dry-run, the spec needs review BEFORE running the full test. The §10.1 dry-run is the gate.

## 8. Caveats `result.md` must explicitly acknowledge

- **Garmin stress is partly motion-sensitive** ([hrv_proxy_via_stress §2](../../../methodology/hrv_proxy_via_stress.md#2-how-garmin-stress-is-derived)). The motion filter is meant to address this; the construct-disambiguation against HA11 + the respiration-companion sensitivity are the within-test checks. None of these prove the filter actually isolates pure-autonomic events.
- **The Garmin `intensity` classification has an 81% gap** ([stress_low_motion_primitive §3.1](../../../methodology/stress_low_motion_primitive.md)). Minutes without an explicit intensity record default to "low motion"; this is generous. The respiration-companion sensitivity is the within-test check on whether the gap days are over-counting. The methodology MD §3.3a queues a v2 with sleep-window + recorded-activity-file companions to address this directly.
- **Citalopram dose-modulates the underlying stress channel** per [citalopram_dose_response §5.6](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14). HA-C4b's per-phase treatment is the dose-confound control; cross-phase aggregation without the per-phase split would be wrong. The per-phase verdicts are NOT directly comparable on raw count magnitudes — only on the `(z, frequency)` precursor-signal level.
- **The `below_moderate` motion class is currently identical to `low_or_below`** ([stress_low_motion_primitive §3.2](../../../methodology/stress_low_motion_primitive.md)). The S{50,60,75}_Mbelow_mod columns will produce identical results to the corresponding S_Mlow columns by construction. The 9-column ladder effectively reduces to 6 unique columns in v1.
- **Exertion-conditioning shrinks n**. Heavy-exertion-day subset is estimated 100-200 days LC-era pooled; per-phase n's are smaller. Per-phase headline verdicts may be inconclusive on the low-n phases (buildup, afbouw).
- **Construct relations to sibling channels are heterogeneous** (per the viz-notes Family D2a/D2b/Session E validation):
  - vs `stress_high_duration_min`: **ρ = 0.79** (close sibling; "minutes-in-high-stress" cousin). The primary disambiguation question is whether the motion filter adds analytical value beyond the all-day-stress-time-count. **The most empirically critical disambiguation** because if ρ is this high, the motion filter may not be discriminative on its own.
  - vs `u_dip_count` (HA11): ρ = 0.556 (within-day SHAPE sibling; information-additive).
  - vs `stress_mean_sleep` (the load-bearing dose-response anchor channel): **ρ = 0.15** (essentially independent at day-scale). Primary IS dose-modulated by the same mechanism but measures different aspect (all-day stress-at-rest burden vs sleep-window-mean stress level).
  HA-C4b SUPPORTED while `stress_high_duration_min` does NOT discriminate on the same episodes = strongest empirical case for the motion-filter refinement. HA-C4b NOT-SUPPORTED while `stress_high_duration_min` discriminates = motion filter may be filtering OUT signal. Documented per-episode in §4.11 / §9.
- **The participant has been operationally using the rest-stress trigger** per [garmin_pacing_practice §3.3](../../../methodology/garmin_pacing_practice.md#33-stress-when-at-rest) — protocol DISTURBS the test. If the participant successfully acts on rest-stress (early bed, active rest), the downstream crash may be prevented, and the test conflates protocol-positive-with-action vs protocol-positive-with-pushed-through. The protocol's lived stabilisation in recent months also matches the consolidation phase, which is where the headline verdict lives. Document this; do NOT redefine the verdict.
- **`crash_v2` mixes mechanisms** (per the standard cross-test caveat). A multi-mechanism crash population dilutes any one-mechanism precursor signal.
- **Multi-comparison**. HA-C4b is the next pre-registered hypothesis in the HA series. The held-out validate window is the primary defence; the per-phase split adds a phase-multiplicity concern that the consolidation-headline + unmedicated-confirmation pattern is meant to address.
- **Buildup-vs-afbouw asymmetry** per [phase_stratification §8.4](../../../methodology/citalopram_phase_stratification.md#84-the-buildup-and-afbouw-magnitude-asymmetry-as-a-research-question). The β_dose was estimated on the buildup window; if the actual stress-low-motion-count dose-response is asymmetric, the per-phase baselines may carry residual phase-mediated shifts. Out of scope for HA-C4b v1; queued for the asymmetry-investigation MD.

## 9. What we do with each outcome

The outcome space is per-phase × {SUPPORTED, NOT-SUPPORTED, INCONCLUSIVE}. The headline is the consolidation-phase verdict at the primary N_std tier in both train and validate independently. Branching:

- **Consolidation SUPPORTED in both train AND validate windows** (primary 4d at N_std = 1.5; (a)+(b)+(c) all pass) → **fourth project-level SUPPORTED-in-both finding** (after HA10 stands alone on validate; HA06b + H02b + H02d are train-only). The lived-experience pacing trigger is empirically validated AT the consolidation dose-state. The §5.B framework is operationally demonstrated. Then: `card.md` for a rest-stress-aware retrospective card concept. If unmedicated also SUPPORTED → the signal is dose-state-invariant; strong claim. If unmedicated NOT-SUPPORTED → the signal is consolidation-specific; document the asymmetry as evidence for the buildup-vs-afbouw asymmetry hypothesis being explored ([phase_stratification §8.4](../../../methodology/citalopram_phase_stratification.md#84-the-buildup-and-afbouw-magnitude-asymmetry-as-a-research-question)).

- **Consolidation train SUPPORTED, validate NOT-SUPPORTED** → train-era pattern that does NOT replicate. Caveats: a recently-evolved pacing protocol may have changed the trigger's predictive utility; document specifically. Suggest follow-up: re-run on the recent 6-month window only (post-protocol-stabilisation per [garmin_pacing_practice §2 temporal qualifier](../../../methodology/garmin_pacing_practice.md#temporal-qualifier--this-protocol-is-a-recent-stabilisation-not-a-constant)).

- **Consolidation train NOT-SUPPORTED, validate SUPPORTED** → second validate-era SUPPORTED finding (after HA10). Notable because it would imply that motion-filtered sympathetic-at-rest events became precursor-discriminating only after some change (medication, protocol, baseline shift). Investigate.

- **Consolidation NOT-SUPPORTED in both windows** → motion-filtered stress-elevated-minute count does NOT carry crash-precursor signal at the population level. **The motion filter is doing analytical work** if the corresponding HA11 secondary descriptive outcome shows HA11 fires on episodes HA-C4b does not (or vice versa); the rest-stress trigger is real but not directly precursor-discriminative on its own. The lived protocol's value may be PROTECTIVE (the participant acts on the trigger and prevents the crash) rather than PREDICTIVE — flag as a follow-up question for the [garmin_pacing_practice MD](../../../methodology/garmin_pacing_practice.md) to address. **Strongly recommend** writing the result.md with the protocol-protective hypothesis as the primary alternative reading.

- **Construct-disambiguation against `stress_high_duration_min` differs from primary headline** (PRIMARY sibling per §4.11.2, ρ = 0.79):
  - HA-C4b fires AND `stress_high_duration_min` does NOT discriminate on the same episodes → **the motion-filter refinement caught episodes the all-day-stress-time-count missed**. This is the strongest empirical case for the motion filter as a discriminative refinement. Worth documenting the specific episodes — they have the most analytical value for follow-up.
  - `stress_high_duration_min` discriminates AND HA-C4b does NOT on the same episodes → the motion filter is **filtering OUT real precursor signal**; the all-day-stress-time-count is the better discriminator. The motion-filter refinement may be overly restrictive. Strong case to test HA-C4c with a relaxed motion definition (e.g., intensity ≤ 2 instead of ≤ 1, or removing the no-record default).
  - Concordant on episodes → motion filter is **incremental, not essential**; the all-day-stress-time-count is sufficient. The pacing protocol's "stress at rest" framing may be experientially salient but not analytically distinct from "high stress time" period.
- **Construct-disambiguation against HA11's u_dip_count differs from primary headline** (SECONDARY sibling per §4.11.3, ρ = 0.556):
  - HA-C4b fires AND HA11 NOT-SUPPORTED on the same episodes → the within-day CONCURRENCE pattern (stress + low motion at same moment) discriminates episodes the within-day SHAPE pattern (pre-dip-post trajectory) misses. Document specific episodes.
  - HA11 SUPPORTED AND HA-C4b NOT on same episodes → the SHAPE pattern carries precursor information the CONCURRENCE pattern misses; they're complementary, not redundant.
  - Concordant on episodes → both within-day metrics carry similar precursor signal; report joint ρ at episode level.

- **Respiration-companion sensitivity differs from primary headline**:
  - HA-C4b SUPPORTED + respiration above_18 ALSO elevated in lead-up → the "low motion" minutes may have been motion-or-arousal-confounded; the result is consistent with sympathetic arousal but the motion filter alone did not isolate it. Document; consider the v2 sleep+activity companion as a tightening.
  - HA-C4b SUPPORTED + respiration above_18 NOT elevated → signal is more credibly "genuine sympathetic at rest" minutes. The strongest reading.
  - HA-C4b NOT-SUPPORTED + respiration above_18 elevated in some lead-ups → the count metric is missing the arousal signal that respiration is picking up; queue an HA-C4c test on the respiration companion as predictor.

- **Sensitivity ladder shows non-monotonicity** (S=50 < S=60 frequency, or strict > low frequency) → **bug or extreme baseline shift**. Halt the test; investigate before publishing the verdict. Could indicate the threshold's per-phase appropriateness is wrong (e.g. S=60 is below the consolidation-phase baseline median and effectively counts all minutes, while S=75 picks the genuine spikes).

- **Spec sanity-check fails on dry-run** (per-phase n < 10 in consolidation; median primitive distribution outside expected range; median σ outside [5, 40]) → DO NOT run the full test. Document the failure in the dry-run report; revise the spec (creating HA-C4b-v2 with audit trail).

- **The 2024-04 boundary-collision causes most buildup episodes to fall in the excluded window** → buildup-phase verdict becomes inconclusive by design. Report as such; do not retroactively narrow the buildup-buffer to recover power. The exclusion was pre-registered for a reason.

## 10. Detection script architecture

The extraction is already complete (Session E). HA-C4b adds Stage 2 — the precursor test on the cached primitive.

### 10.1 Stage 1 — primitive (already done)

[`pipeline/01_extract/stress_low_motion_extract.py`](../../../pipeline/01_extract/stress_low_motion_extract.py) emits `processed/garmin/stress_low_motion_minutes.csv` with the 11 columns documented in the methodology MD §4 + §4b. Already merged into `per_day_master.csv` (commit `14a32a3`). No re-extraction needed for HA-C4b.

### 10.2 Stage 2 — test (`HA-C4b/test.py`, to be written in C.6-equivalent session)

Loads `per_day_master.csv`, joins HA11's `udip_counts.csv` for the construct-disambiguation secondary, applies §4.2-§4.5 filtering + lagged baseline construction, computes per-day z + per-episode `max signed_z`, evaluates §5 falsification criterion per phase + per N_std tier + per sensitivity-ladder column.

Same lagged-baseline machinery as HA06b / HA10 / HA11; same null-seed (`20260605`); same `--dry-run` mode that prints first-3-episodes per phase × era to confirm spec sanity before the full evaluation runs.

### 10.3 Stage 3 — `result.md`

Reports per-phase × per-tier × per-ladder-column verdict. Headline verdict block at top (consolidation-phase, N_std = 1.5, primary 4d, one-sided). Per-phase tables. Construct-disambiguation against HA11. Respiration-companion sensitivity. Caveats per §8.

### 10.4 Run protocol

1. **Dry-run** (`python test.py --dry-run`): prints sample sizes per phase × era; checks sanity per §7. **If sanity check fails → halt + revise spec → HA-C4b-v2.**
2. **Full run** (`python test.py`): emits `result.md` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-C4b-v2 with the v1 result archived (per the project's locked-pre-reg discipline).

---

*Pre-registration drafted 2026-06-15 by Claude in reviewer-mode-with-authorization. Lock requires user acceptance. Fresh-session `/research-review` audits after lock.*
