# HA-C4b — Stress-with-low-motion minute count as crash precursor (Wiggers C4 + motion filter)

## Authorship

**Drafted 2026-06-15** by Claude (Opus 4.6) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. Drafting session had shared context with Session E (the [`stress_low_motion_primitive` MD](../../../methodology/stress_low_motion_primitive.md) + the extraction script) and Session D (the [`citalopram_phase_stratification` framework](../../../methodology/citalopram_phase_stratification.md)); pre-reg follows the [HA11 pre-reg pattern](../HA11-stress-udip/hypothesis.md).

**Status**: drafted, not locked. Lock requires explicit user acceptance. After lock, [`/research-review`](../../../reviews/README.md) must run in a fresh session (no shared drafting-session context); the review report lands in [`reviews/`](../../../reviews/) with the addendum *"Fresh session — no exposure to the drafting context; doc-only knowledge."*

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

### 4.3 Day validity

A day is **valid for HA-C4b** if **all** of:

1. The primitive's stress-sample day-validity gate passes (≥ 600 in-range stress samples; the `valid` flag from the extraction is 1).
2. The exertion-conditioning rule (§4.2) is satisfied.
3. The day has a `crash_v2` label (i.e. is not a censored day).

Days failing any of these are flagged and excluded from the test sample. Report fractions.

### 4.4 Citalopram phase-stratified treatment (per §5.B framework, locked)

The primary test is **per-phase stratified** ([phase_stratification §5.A](../../../methodology/citalopram_phase_stratification.md#5a-per-phase-stratification-the-default-lowest-risk)) — separate sub-test within each of the 4 LC-era Citalopram phases:

| phase | window | n estimate (heavy-exertion subset) |
|---|---|---|
| unmedicated | LC start 2022-04-04 → 2024-04-08 | ~50-100 |
| buildup | 2024-04-09 → 2024-06-19 | ~10-20 |
| consolidation (30mg plateau) | 2024-06-20 → 2026-03-19 | ~80-150 |
| afbouw + post-afbouw | 2026-03-20 → 2026-06-05 | ~10-20 |

Per-phase n's are estimates; actual counts gate at §10.1 dry-run.

**Rationale for per-phase rather than dose-adjusted-predictor (§5.B) primary**: dose-adjustment of a COUNT metric is non-trivial — `β_dose = +0.57/mg` (the all_day_stress_avg confirmed coefficient) acts on per-minute stress values, not on per-day counts. To apply §5.B properly the threshold would need to shift per-day (`S_adj(d) = 60 + 0.57 × dose_plasma_mg(d)`), requiring a re-extraction of the primitive. **For HA-C4b v1 the per-phase test is the primary**; a dose-adjusted-threshold sensitivity arm is queued as future work (would require a §5.B-aware re-extraction).

**Buildup + afbouw + post-afbouw n is small** (~10-30 each). For buildup specifically, the 2024-04 boundary-collision per [intervention_effects_descriptive §8.1](../../../methodology/intervention_effects_descriptive.md#81-effective-analyzable-scope-5-of-8-boundaries-usable) makes the first ~22 days of the phase confounded with CPAP-end. Apply [phase_stratification §5.A's optional ±N-day boundary buffer](../../../methodology/citalopram_phase_stratification.md#5a-per-phase-stratification-the-default-lowest-risk) — exclude buildup days before 2024-04-30 (the first 22 days of buildup). Report buildup separately as "buildup post-CPAP-buffer". The 9-day post-afbouw window before data-cut is too short for an independent test; merge with afbouw or report as descriptive-only.

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

### 4.9 Null sample

200 random non-overlapping reference dates per phase, same construction + seed (`20260605`) as HA06b / HA10 / HA11. Per-window null trigger flag computed exactly as in §4.7. Only days satisfying §4.3 validity (same phase, eligible exertion class) AND §4.5 baseline-availability are eligible as reference dates.

Per-phase null sample size: 200 reference dates ÷ 4 phases = 50 per phase minimum. If a phase has fewer than 100 eligible non-crash heavy-exertion days, reduce its null sample size to `min(50, n_eligible / 2)` and report the reduction.

### 4.10 Sensitivity ladder report

Report the §5 falsification criterion (a)(b)(c) for **all 9 stress × motion columns**, not just the primary. The headline verdict comes from `S60_Mlow`; the others are sensitivity arms. A finding that fires only at `S60_Mlow` but not at the surrounding cells is buffer-dependent and weaker; a finding that fires across most cells of the ladder is robust.

Within-row monotonicity in S (S=50 ≥ S=60 ≥ S=75 frequency) and across-motion-classes monotonicity (strict ≤ low ≤ below_mod frequency) must hold; violations are bugs and require investigation before the headline verdict locks.

### 4.11 Secondary descriptive outcomes

For each calendar day `d` in the test sample:

1. **Same-day gevoelscore correlation**: Spearman(stress_low_motion_min_count_S60_Mlow, gevoelscore) per phase + pooled LC era. Median count per gevoelscore value. Report split by era (train vs validate) AND by Citalopram phase. **Descriptive only; no SUPPORTED bar.**
2. **HA11 construct-disambiguation**: For each crash episode in the lead-up, flag (HA-C4b fires, HA11 fires) — produce a 2×2 contingency. If HA-C4b fires on episodes HA11 does not (the "off-diagonal" cell), document those specific episodes — the within-day motion filter is doing analytical work distinct from the within-day shape pattern.
3. **Respiration-companion sensitivity**: For each crash episode where HA-C4b fires, report whether `n_minutes_resp_above_18` in the lead-up is also above its lagged baseline (z > 0). If HA-C4b fires AND respiration is also elevated, the apparent "low motion" minutes may have been motion-or-arousal-confounded; if HA-C4b fires AND respiration is NOT elevated, the signal is more credibly "genuine sympathetic at rest". This is a methodological sensitivity, not a verdict.

## 5. Pre-registered falsification criterion

Identical three-criterion bar shape to H02b / HA01b / HA06b / H02d / HA10 / HA11, applied **per phase** with the headline verdict at the **consolidation phase** (largest n):

**(a) Frequency**: at least **60%** of consolidation-phase crash episodes have `max signed_z ≥ N_std` (one-sided primary) in their lead-up window.

**(b) Discrimination**: the consolidation-phase crash-episode frequency from (a) is at least **15 percentage points higher** than the consolidation-phase null-sample frequency.

**(c) Magnitude**: the median `max signed_z` across consolidation-phase crash episodes is at least **N_std / 2** (0.75 / 1.0 / 1.25 for N_std = 1.5 / 2.0 / 2.5 respectively).

Any one of (a), (b), (c) failing on the consolidation phase at the primary tier (N_std = 1.5) in either train or validate → **headline refuted for the consolidation phase**.

**Per-phase secondary verdicts**:
- Unmedicated phase: same (a)(b)(c) bar; reported as independent confirmation if it agrees with consolidation, OR as concerning divergence if it does not.
- Buildup-post-CPAP-buffer + afbouw: low power (n < 30); report (a)(b)(c) descriptively but no SUPPORTED bar at the primary tier.

**Inconclusive bars**:
- If consolidation has fewer than 10 clean crash episodes per train or validate window after exclusions → **inconclusive on consolidation** at that window. Re-evaluation possible after additional crashes accumulate.
- If unmedicated has fewer than 5 clean crash episodes → **inconclusive on unmedicated**; verdict carried by consolidation alone.

**Bidirectional sensitivity arm**: report `|z| ≥ N_std` per the same three-criterion bar. Do NOT redefine the headline verdict on this arm; report honestly as a secondary diagnostic.

## 6. Exclusion rules

- Days with fewer than 600 valid per-minute stress samples are excluded (insufficient coverage; same as HA11).
- Days not satisfying the §4.2 exertion-conditioning rule are excluded (NOT in test sample; the test is on the heavy-exertion-conditioned subset only — this is the C4 spec).
- Days where the lagged-same-phase baseline σ ≤ 5 minutes are flagged *low-variability* and excluded.
- Days where fewer than 40 of 60 prior same-phase valid days are available are excluded (insufficient baseline).
- **Buildup phase days before 2024-04-30** (first 22 days of buildup phase) are excluded from the test sample (CPAP-end confound per [intervention_effects_descriptive §8.1](../../../methodology/intervention_effects_descriptive.md#81-effective-analyzable-scope-5-of-8-boundaries-usable)). Report buildup separately as "buildup post-CPAP-buffer".
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
- **Construct relation to HA11 is moderate** (ρ = 0.556). HA-C4b SUPPORTED while HA11 NOT-SUPPORTED on the same episodes would be a notable construct-divergence finding; HA-C4b NOT-SUPPORTED while HA11 SUPPORTED would suggest the motion filter is filtering out signal rather than noise.
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

- **Construct-disambiguation against HA11 differs from primary headline**:
  - HA-C4b SUPPORTED on episodes HA11 NOT-SUPPORTED → the motion filter IS the discriminative refinement. Document those specific episodes. This is the strongest construct-validation result for the lived-experience pacing trigger.
  - HA11 SUPPORTED on episodes HA-C4b NOT-SUPPORTED → the within-day SHAPE pattern dominates the within-day CONCURRENCE pattern. The motion filter may be FILTERING OUT signal rather than noise. Document; consider relaxing the motion filter in HA-C4c.
  - Concordant on episodes → both are valid precursor metrics; report ρ at the episode level (not just the day level).

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
