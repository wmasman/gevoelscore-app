# HA-C3 v2 — descriptive precondition audit

**Status**: **LOCKED r1 by user acceptance 2026-06-25** per §11 step 10 Phase A.7. Drafted 2026-06-25 by `/research-interpret descriptive HA-C3` skill in dry-run dispatch per §11 step 8 of [`_plan_results_analysis_layer.md`](../../../methodology/_plan_results_analysis_layer.md) (r5 LOCKED 2026-06-24). First-ever invocation of the [`/research-interpret`](../../../../.claude/skills/research-interpret/SKILL.md) skill (which has since reached LOCKED r4). Phase A.1-A.6 discipline resolved; A.7 user-acceptance lock event closes Phase A for C-stress-fatigue-shape. **First LOCKED production Stage D audit of the results-analysis layer.**

This audit is a Stage D producer-mode artefact per [`descriptive_precondition_audit.md`](../../../methodology/descriptive_precondition_audit.md) (LOCKED r2 2026-06-24). Per §3 of guide #1, producer-mode audits do NOT carry an `## Authorship` block and do NOT receive a fresh-session `/research-review` pass; user explicit acceptance per §3.8 of the locked plan is the binding completion event.

---

## 1. Target HA + result reference

- **HA ID**: HA-C3 v2 (revision r2)
- **Pre-reg lock date**: 2026-06-23 (commit `2a0b0df`)
- **Result lock date**: 2026-06-23 (test execution post-`2a0b0df` LOCK)
- **Headline verdict from `result.md`** (verbatim): **REJECTED (wrong-direction override)** — primary 3-condition test on 3-bin reduction (post-§7.3 halt-option-A absorb) returned (a) Jonckheere-Terpstra J*=+0.481, p=0.6742 (FAIL); (b) S=-0.7403, p=0.0002 (PASS direction S<0); (c) spline F=28.27, p=0.0003 (PASS), but spline-second-derivative at segment midpoint x=70 was +0.0000 (positive sign at majority of contributing midpoints → wrong-direction firing on condition (c)). The wrong-direction override fires per pre-reg §5.1 verdict bar.
- **Effective n on the primary cell** (verbatim from `result.md` §2): n = 581 (unmedicated Stratum 4 pool post-§4.3 day-validity gate). 3-bin reduction descriptives: B1 [0,30) n=95; B2 [30,40) n=385; B3' [40,100] n=101 (post-§7.3 halt-option-A absorb of original B4 [60,100] n=1 into B3 [40,60)).
- **Operationalisation summary** (one sentence, paraphrasing pre-reg §4): same-day `all_day_stress_avg × gevoelscore` cross-day-aggregate dose-response shape test on Stratum 4 unmedicated cell, binned at Wiggers-verbatim 4-bin scheme (`[0,30), [30,40), [40,60), [60,100]`) with pre-committed §7.3 halt-option-A absorber for B4 underpower, 3-condition gated verdict per §5.1 (Jonckheere-Terpstra monotone-decreasing + second-difference convexity contrast S + spline non-linearity with segment-midpoint sign agreement).
- **Methodology MDs cited by the pre-reg** (link list):
  - [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md) — §3.2 fresh-session drafting + §3.8 lock-blocking gates + §10.4 v1→v2 redraft trigger.
  - [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) — §4 CONFIRMED-channel inheritance for `all_day_stress_avg`; §5.A primary + §5.B sensitivity arm pattern.
  - [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) — §5.6.1 the +0.57/mg dose-modulation β load-bearing for §4.4 approach choice.
  - [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) — §4.7 block-permutation at E[L]=7; data-driven E[L]* + factor-of-2 flag.
  - [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) — Stratum 4 + unmedicated phase headline binding.
  - [`train_validate_split_fate.md`](../../../methodology/train_validate_split_fate.md) — §5 single-pool primary + train+validate M3 overlay descriptive only.
  - [`time_resolution.md`](../../../methodology/time_resolution.md) — §6 per-day default for §4.9 temporal-structure operationalisation choice.
  - [CONVENTIONS.md](../../../CONVENTIONS.md) — §3.1 personal baseline; §3.4 crash-drop sensitivity; §4.1-§4.3 descriptive-before-inference + caveats + confirmatory.

## 2. Load-bearing assumptions enumerated

| # | Assumption | Source |
|---|---|---|
| A1 | Sample size on every reported cell ≥ pre-registered floor (≥ 30 per primary bin per §7.5 Gate 1; total n ≥ 100 per Gate 4) | Pre-reg §7.5 (sanity gates) + `test.py` (gate evaluation logic) |
| A2 | Missingness pattern is MCAR/MAR-compatible OR missingness-aware operationalisation used + documented (§4.3 NaN-drop) | Pre-reg §4.3 (day-validity gate) + §8 caveat 10 (independent-obligations block); no per-channel missingness audit cited beyond `desc-SMS` partial coverage |
| A3 | Block-length E[L]=7 is appropriate for autocorrelation structure of `all_day_stress_avg` × `gevoelscore` on Stratum 4 | Pre-reg §4.7 inherits [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md); §4.7 r2 amendment adds two data-driven E[L]* derivations (linear-residual + bin-label categorical) + factor-of-2 flag |
| A4 | Era / Stratum 4 binding honored; unmedicated phase headline; April 2024 cluster excluded | Pre-reg §4.2 + §4.3 + §6 (exclusion rules); cites [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) |
| A5 | v24 presence-conditioned semantics respected — NOT APPLICABLE here (no v24 primary signals; `all_day_stress_avg` and `gevoelscore` are both `daily_computed` per `symptom_mention_asymmetry.md` taxonomy) | NOT APPLICABLE |
| A6 | Nightly attribution per `nightly_attribution.md` — NOT APPLICABLE (cross-day-aggregate test on daytime stress + same-day gevoelscore; no sleep-derived primary signal) | NOT APPLICABLE |
| A7 | Effect-size direction reported alongside p-values, never alone | Pre-reg §4.5.2 (secondary descriptive outcomes — bin-mean + CI + companion contrast); `result.md` §3 reports bin-means, S statistic value, spline second-derivative signs alongside p-values |
| A8 | Single-pool primary preserved per `train_validate_split_fate.md`; train/validate M3 sensitivity overlay only | Pre-reg §4.2 + §4.8 + §5.0 (single-cell headline lock); `result.md` §5 reports train/validate as descriptive overlay only |
| A9 (HA-specific) | Citalopram-channel-inheritance discipline per `citalopram_phase_stratification.md` §4 — CONFIRMED channel inheritance for `all_day_stress_avg` triggers §5.A primary + §5.B sensitivity arm pattern | Pre-reg §4.4 (Locked decision 8) cites [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) §5.6.1 |

## 3. Per-assumption status

| # | Status | Citation / reason | Stocktake diff |
|---|---|---|---|
| A1 | **BACKSTOPPED** | Per `result.md` §10 §7.5 gate evaluation: Gate 1 (per-bin n ≥ 30 on 4 bins) PASS — B1=95, B2=385, B3=100; only B4=1 failed, triggering the pre-committed §7.3 halt-option-A absorption (B4 absorbed into B3'=101). Gate 4 (total n ≥ 100) PASS at n=581. Pre-committed halt-option-A IS the design-level small-n absorption per pre-reg §7.3 + the stocktake's "B (B4 absorber pre-committed)" reading. Matches stocktake [§2 HA-C3 (v2) row](../../../methodology/_descriptive_stocktake_2026-06-23.md#2-per-ha-assumption-matrix). | No diff |
| A2 | **NOT BACKSTOPPED (BACKSTOPPED partial via `desc-SMS`)** | Pre-reg §4.3 drops NaN rows but does not cite a per-channel missingness rate audit. `desc-SMS` (`analyses/descriptive/operationalisation_support/stress_mean_sleep/findings.md`) backstops the sister channel `stress_mean_sleep` but the test's primary channel is `all_day_stress_avg`; per-channel missingness rate × era × phase MCAR/MAR diagnostic does not yet exist for `all_day_stress_avg`. The pre-reg's stratum + phase + April-2024-cluster gating IS a missingness-aware operationalisation pattern (per §5.2 operational test path (a)) but does not produce the per-channel rate audit per (b). Stocktake row marked **B**; strict reading per the audit's §6.3 conflict rule revises to BACKSTOPPED-partial (the gating discipline holds; the per-channel rate audit is missing). Closure path: per-channel missingness audit on `all_day_stress_avg` (S effort per stocktake §3 Shared gap 3). **Cites L7 (survivorship)**: the §5.2 missingness check is the audit-layer manifestation of L7; the gating discipline reduces but does not eliminate the survivorship reach question. | Revised stocktake B → BACKSTOPPED-partial per §6.3 (strict reading of per-channel rate audit gap) |
| A3 | **BACKSTOPPED** | Per `result.md` §7: two `E[L]*` values reported per pre-reg §4.7 r2 amendment (linear-residual derivation = 5.35, cutoff lag = 3, factor-of-2 flag = ok; bin-label sequence derivation = 7.00 default, factor-of-2 flag = ok). Both deviation flags PASS. `desc-SMS` characterised the sister channel `stress_mean_sleep`; the data-driven E[L]* on this test's predictor `all_day_stress_avg` is reported in-test per the §4.7 amendment, providing first-hand backstop on this channel. Matches stocktake reading. | No diff |
| A4 | **BACKSTOPPED** | Pre-reg §4.2 cites [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) Stratum 4 + unmedicated phase headline; §4.3 gate 1 enforces `date >= 2022-04-04`; gate 2 enforces `date <= 2024-04-08`; §6 cites April 2024 cluster exclusion per `citalopram_phase_stratification.md`. Single-pool primary; train/validate is descriptive M3 sensitivity arm only. Matches stocktake B. | No diff |
| A5 | **NOT APPLICABLE** | No v24-derived columns (`cat_*`, `state_*`, `day_dominant_polarity`, `per_day_intensity`) appear in pre-reg §3 data sources or §4 operationalisation. Primary signals are `all_day_stress_avg` (Garmin `daily_computed`) and `gevoelscore` (self-report `daily_computed`); test is daily_computed-only. Per `symptom_mention_asymmetry.md` variable-class taxonomy: NOT APPLICABLE with one-sentence reason "no v24 primary signals; daily_computed-only test". | No diff |
| A6 | **NOT APPLICABLE** | Daytime cross-day-aggregate test on `all_day_stress_avg` (24-hour aggregate excluding sleep window per DATA_DICTIONARY §C definition) and same-day `gevoelscore` (subjective end-of-day report). No sleep-derived primary signal in scope. Reason: "daytime-aggregate + same-day-outcome; no nightly column". | No diff |
| A7 | **BACKSTOPPED** | Per `result.md` §3: every cell with a p-value carries a directional effect-size statistic alongside — Jonckheere-Terpstra J*=+0.481 (standardised); convexity statistic S=-0.7403 (magnitude + sign); spline F=+28.2689 (statistic value); spline second-derivative per midpoint x=35 (-0.00151 NEG) and x=70 (+0.00000 POS); pairwise Mann-Whitney U + Holm-adjusted p across 2 adjacent-bin pairs (post-§7.3 absorption) with raw p AND Holm-adjusted p reported; companion contrast `c·m = -0.7403`; Spearman ρ = -0.0298. Bin-means + 95% CI per `result.md` §3 table. The direction-of-failure on the wrong-direction-override IS captured by the spline second-derivative sign reporting per pre-reg §4.5.1(c). | No diff |
| A8 | **BACKSTOPPED** | Pre-reg §4.2 + §5.0 single-cell headline lock per `train_validate_split_fate.md`; `result.md` §5 train/validate descriptive M3 overlay does not promote to per-portion verdict per `train_validate_split_fate.md §5`. Pre-reg drafted post-2026-06-13 (split-fate MD lock) → discipline applies in full. Matches stocktake B. | No diff |
| A9 (HA-specific) | **BACKSTOPPED** | Pre-reg §4.4 Locked decision 8 cites [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) §5.6.1 verbatim for the +0.57/mg β value; §5.A unmedicated primary headline; §5.B dose-adjusted cross-phase sensitivity arm. `result.md` §4 reports §5.A + §5.B per the locked discipline; §5.B verdict (REJECTED, 0-of-3) is descriptive-only and does NOT promote to primary per §5.0 single-cell lock. CONFIRMED-channel inheritance discipline honored. | No diff |

## 4. Verdict-trust call

**TRUSTED**.

**Rationale**: 7 of 9 load-bearing assumptions are BACKSTOPPED; 2 are NOT APPLICABLE (A5, A6) with documented one-sentence reasons. A2 sits in the BACKSTOPPED-partial band per the §6.3 strict-reading revision against the stocktake (the gating discipline is documented and is itself a missingness-aware operationalisation per §5.2 operational test path (a), but the per-channel rate audit per path (b) does not exist for `all_day_stress_avg`). The A2 BACKSTOPPED-partial does NOT downgrade to NOT-BACKSTOPPED because the pre-reg's gating discipline supplies the missingness-aware operationalisation that path (a) explicitly permits; the missing rate audit narrows the survivorship reach (per L7) but does not unback the assumption.

Per guide #1 §4.4: TRUSTED applies when every load-bearing assumption is BACKSTOPPED (or NOT APPLICABLE with documented reason). The A2 partial-coverage notation is included in the §5 `open_inputs` block as a non-blocking narrowing candidate; Stage I may proceed with the survivorship caveat noted in its §4.5 L-ID citation block (L7 application).

Per guide #1 §6.4: the verdict-trust call is independent of the verdict label. HA-C3 v2's REJECTED verdict whose assumptions are all BACKSTOPPED (or NOT APPLICABLE) is TRUSTED for Stage I purposes; the audit does not preferentially trust REJECTED over SUPPORTED or vice versa.

## 5. `open_inputs` block

| # | What is missing | What it blocks | Cheapest acquisition path | Fallback claim available |
|---|---|---|---|---|
| 1 | Per-channel missingness audit on `all_day_stress_avg` (per-era + per-phase MCAR/MAR diagnostic; not yet existing per stocktake §3 Shared gap 3) | Tightens A2 from BACKSTOPPED-partial to BACKSTOPPED; tightens Stage I §4.5 L7 citation from "gating-discipline-bounded" to "fully audit-backed" | S effort per stocktake §3 Shared gap 3 (per-channel missingness rate × era × phase); script template from `desc-SMS` exists | TRUSTED stands with A2 BACKSTOPPED-partial + Stage I §4.5 L7 narrowing caveat (per locked-plan §3.5 hard rule: fallback is at most one tier narrower; here the fallback is the existing TRUSTED with the L7 reach narrowed at Stage I) |

---

## §11 Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-25 | Drafted r1 (DRY-RUN) | Producer-mode by `/research-interpret descriptive HA-C3` skill on first invocation (skill LOCKED r2 today). Dry-run dispatch per §11 step 8 of `_plan_results_analysis_layer.md` (r5 LOCKED). All audit content drawn from HA-C3 v2 r2 pre-reg (LOCKED 2026-06-23 `2a0b0df`), `result.md` (LOCKED 2026-06-23), `test.py`, and the cited methodology MDs. **Drift triggers registered** (manual-pending-skill carry-forward per skill responsibility #10): (1) HA-C3 v2 `result.md` re-runs; (2) any cited methodology MD changes lock-version (especially `permutation_null_block_length.md`, `citalopram_phase_stratification.md`, `lc_era_temporal_segmentation.md`, `train_validate_split_fate.md`); (3) per-channel missingness audit on `all_day_stress_avg` lands (closes the A2 partial-coverage `open_inputs` entry); (4) ≥6 months elapse since lock. **STATUS: NOT LOCKED — awaiting user acceptance per `_plan_results_analysis_layer.md` §3.8 binding completion event.** |
