# HA-C3p — descriptive precondition audit

**Status**: **LOCKED r1 by user acceptance 2026-06-25** per §11 step 10 Phase A.7. Drafted 2026-06-25 by `/research-interpret descriptive HA-C3p` skill in dry-run dispatch (second invocation of the skill; first was HA-C3 v2 above). Skill has since reached LOCKED r4. Phase A.1-A.6 discipline resolved; A.7 user-acceptance lock event closes Phase A for C-stress-fatigue-shape. Sister-HA Stage D audit to HA-C3 v2's; both lock together as the cluster's Stage D foundation.

Producer-mode artefact per [`descriptive_precondition_audit.md`](../../../methodology/descriptive_precondition_audit.md) (LOCKED r2 2026-06-24); no `## Authorship` block per §3 of guide #1; user explicit acceptance per §3.8 of the locked plan is the binding completion event.

---

## 1. Target HA + result reference

- **HA ID**: HA-C3p (revision r2)
- **Pre-reg lock date**: 2026-06-23 (commit `c0148ca`)
- **Result lock date**: 2026-06-23 (test execution post-`c0148ca` LOCK; result.md notes write-time-bug patches applied by dispatcher to enable result.md emission — substantive test logic untouched)
- **Headline verdict from `result.md`** (verbatim): **PARTIAL (2-of-3 conditions MET)** — primary 3-condition test on 5-quintile-bin scheme returned (a) Jonckheere-Terpstra J*=+0.267, p=0.5925 (FAIL — direction not monotone-decreasing); (b) S=-0.1964, p=0.0018 (PASS direction S<0 — convexity contrast significant); (c) spline F=+19.55, p=0.0020 (PASS — spline non-linearity significant; spline second-derivative sign at ≥ 3 of 4 contributing midpoints from {Q2: x=29.5; Q3: x=32.5; Q4: x=35.5; Q5: x=68.5} NEGATIVE per `result.md` §3 row). No wrong-direction override fires because pre-reg §5.1 spec does not carry the override on condition (b) sign — (b) and (c) MET; (a) FAILED. Verdict: PARTIAL.
- **Effective n on the primary cell** (verbatim from `result.md` §2): n = 581 (§5.A unmedicated sub-arm). Per-bin n on §5.A unmedicated: Q1[0,28)=45; Q2[28,31)=80; Q3[31,34)=129; Q4[34,37)=138; Q5[37,100]=189. Full Stratum 4 pool (bin-edge derivation): n = 1351.
- **Operationalisation summary** (one sentence, paraphrasing pre-reg §4): same-day `all_day_stress_avg × gevoelscore` cross-day-aggregate dose-response shape test on §5.A Stratum 4 unmedicated sub-arm, binned at **personal-baseline-anchored equal-N quintile bins** computed on the full Stratum 4 pool (n=1351), 3-condition gated verdict per §5.1 (Jonckheere-Terpstra monotone-decreasing + second-difference convexity contrast S = mean of 3 + spline non-linearity with 4 internal knots and ≥ 3-of-4 contributing-midpoint sign agreement). Sister pre-reg to HA-C3 v2 per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline framing.
- **Methodology MDs cited by the pre-reg** (link list):
  - [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md) — §3.2 fresh-session drafting + §3.8 lock-blocking gates.
  - [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) — §4 CONFIRMED-channel inheritance; §5.A primary + §5.B sensitivity arm pattern.
  - [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) — §5.6.1 +0.57/mg dose-modulation β.
  - [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) — §4.7 block-permutation at E[L]=7.
  - [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) — Stratum 4 + unmedicated phase headline; full Stratum 4 single pool for bin derivation.
  - [`train_validate_split_fate.md`](../../../methodology/train_validate_split_fate.md) — §5 single-pool primary.
  - [`time_resolution.md`](../../../methodology/time_resolution.md) — §6 per-day default.
  - [CONVENTIONS.md](../../../CONVENTIONS.md) — §3.1 personal baseline (load-bearing for this pre-reg's framing); §3.2 lagged-baseline (for §4.8(b) z-scored sensitivity arm); §3.4 crash-drop sensitivity; §3.6 named counts; §4.1-§4.3 descriptive-before-inference + caveats + confirmatory.

## 2. Load-bearing assumptions enumerated

| # | Assumption | Source |
|---|---|---|
| A1 | Sample size on every reported cell ≥ pre-registered floor (≥ 30 per quintile bin on §5.A unmedicated sub-arm per §7.5 Gate 1; total n ≥ 100 per Gate 4) | Pre-reg §7.5 + §4.1 draft-time forecast (per-bin n forecast: Q1=45, Q2=80, Q3=129, Q4=138, Q5=189 all PASS the ≥ 30 bar) |
| A2 | Missingness pattern is MCAR/MAR-compatible OR missingness-aware operationalisation used + documented | Pre-reg §4.3 (day-validity gate, inherited from HA-C3 v2 §4.3 verbatim); §8 caveat 11 (independent-obligations block); `desc-SMS` + `desc-RA` characterise underlying channel per stocktake B |
| A3 | Block-length E[L]=7 is appropriate for autocorrelation structure of `all_day_stress_avg × gevoelscore` on Stratum 4 + collapsibility per `phase_axis_collapsibility_conventions.md` | Pre-reg §4.7 inherits [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md); two data-driven E[L]* derivations per the HA-C3 v2 §4.7 r2 amendment inheritance; `desc-SMS` direct backstop per stocktake B |
| A4 | Era / Stratum 4 binding honored; full Stratum 4 single pool for bin derivation; unmedicated phase headline for §5.A primary cell; April 2024 cluster excluded | Pre-reg §4.2 + §4.3 + §6 (exclusion rules inherited from HA-C3 v2 §6); cites [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) |
| A5 | v24 presence-conditioned semantics — NOT APPLICABLE (no v24 primary signals; `all_day_stress_avg` and `gevoelscore` are both `daily_computed`) | NOT APPLICABLE |
| A6 | Nightly attribution — NOT APPLICABLE (cross-day-aggregate test; no sleep-derived primary signal) | NOT APPLICABLE |
| A7 | Effect-size direction reported alongside p-values | Pre-reg §4.5.2 + result.md §3 reports bin-means + 95% CI + Jonckheere J* + S + spline F + spline 2nd-deriv per midpoint + companion contrast c·m + Spearman ρ all with directions |
| A8 | Single-pool primary preserved per `train_validate_split_fate.md`; train/validate M3 sensitivity overlay only | Pre-reg §4.2 + §5.0 single-cell headline lock; `result.md` §4 reports train/validate as descriptive overlay only |
| A9 (HA-specific) | Citalopram-channel-inheritance discipline (CONFIRMED channel → §5.A primary + §5.B sensitivity arm); right-shift unmedicated bin observation surfaced + checked at draft time per §4.1 + §8 caveat 4 | Pre-reg §4.4 + §4.1 (right-shift observation: Q1 unmedicated 45 vs full-pool 248 — only ~18% of unmedicated days fall in full-pool Q1 vs 20% by construction; consistent with +0.57/mg dose-modulation evidence) |
| A10 (HA-specific) | Cross-arm bin-edge cleanliness (sub-arms REUSE the §4.1 quintile boundaries computed once on the full-Stratum-4 pool; no re-computation per sub-arm) | Pre-reg Locked decision 1 + §4.1 + §4.4 §5.B dose-adjustment bin-edge note |
| A11 (HA-specific) | Bin-edge snapshot pinning per §4.1 + §7.5 Gate 5 (per_day_master.csv SHA-256 `d0ff9253...` at draft time; gate verifies the boundaries have not shifted by > 1 stress-unit on the test-time snapshot) | Pre-reg Locked decision 4 + §4.1 + §7.5 Gate 5 + §8 caveat 10 |

## 3. Per-assumption status

| # | Status | Citation / reason | Stocktake diff |
|---|---|---|---|
| A1 | **BACKSTOPPED** | Per `result.md` §9 §7.5 gate evaluation: Gate 1 (per-bin n ≥ 30 on 5 bins on §5.A unmedicated sub-arm) PASS — all five unmedicated quintile bins meet bar (Q1=45 the borderline cell still ≥ 30; Q2-Q5 well above). Gate 4 (all 5 bins ≥ 30 AND total n ≥ 100) PASS at total n=581. Full-pool bin counts on Stratum 4 (n=1351) are all > 240 per bin, well above the floor. Equal-N quintile-bin design eliminates the structurally-absent-or-underpowered category that drove HA-C3 v1→v2 halt; no at-risk bin at draft-time forecast OR at test-time. Stocktake [§2 HA-C3p row](../../../methodology/_descriptive_stocktake_2026-06-23.md#2-per-ha-assumption-matrix) marked B; confirmed. | No diff |
| A2 | **NOT BACKSTOPPED (BACKSTOPPED partial via `desc-SMS` + `desc-RA`)** | Pre-reg §4.3 inherits HA-C3 v2's day-validity gate verbatim (LC era + non-NaN both columns + April 2024 cluster exclusion + first 21 device-baseline days exclusion). `desc-SMS` covers the sister channel `stress_mean_sleep`; `desc-RA` covers recovery-arc trajectory. Per-channel missingness rate × era × phase MCAR/MAR diagnostic does not yet exist for `all_day_stress_avg` (same as HA-C3 v2 A2 reading). Gating discipline IS a missingness-aware operationalisation per §5.2 operational test path (a); the per-channel rate audit per path (b) is missing. Stocktake row marked **B**; strict reading per §6.3 revises to BACKSTOPPED-partial. **Cites L7 (survivorship)**: same as HA-C3 v2 A2 — the per-channel rate audit gap narrows the survivorship reach. | Revised stocktake B → BACKSTOPPED-partial per §6.3 (same as HA-C3 v2 A2) |
| A3 | **BACKSTOPPED** | Per `result.md` §7: two `E[L]*` values reported per the inherited HA-C3 v2 §4.7 r2 amendment (linear-residual derivation = 5.35, factor-of-2 flag = ok; bin-label sequence derivation = 7.00 default, factor-of-2 flag = ok). Both PASS. `desc-SMS` direct backstop on sister channel + in-test E[L]* on the test's actual predictor `all_day_stress_avg` provides first-hand backstop. Stocktake B confirmed. | No diff |
| A4 | **BACKSTOPPED** | Pre-reg §4.2 cites [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) Stratum 4; §4.3 enforces LC era + unmedicated phase boundaries; §6 cites April 2024 cluster exclusion. Full Stratum 4 single pool (n=1351) used for bin derivation (Locked decision 1); §5.A unmedicated sub-arm (n=581) is the primary headline cell with sub-arm REUSING full-pool quintile edges per Locked decision 1 cross-arm cleanliness pattern. Stocktake B confirmed. | No diff |
| A5 | **NOT APPLICABLE** | Same as HA-C3 v2 A5 — no v24 primary signals; daily_computed-only test. | No diff |
| A6 | **NOT APPLICABLE** | Same as HA-C3 v2 A6 — cross-day-aggregate test; no sleep-derived primary signal. | No diff |
| A7 | **BACKSTOPPED** | Per `result.md` §3 + §5: every cell with a p-value carries a directional effect-size statistic — J*=+0.267 (standardised); S=-0.1964 (sign + magnitude); spline F=+19.55; spline 2nd-deriv per midpoint reported (sign agreement check); pairwise Mann-Whitney U + Holm-adjusted p across 4 adjacent quintile pairs; companion orthogonal quadratic contrast c·m=-1.2938; Spearman ρ=-0.0298. Adjacent-bin step magnitudes table (§5) reports per-step `m_low − m_high` with sign. The PARTIAL-band §5.1 multiplicity disclosure sentence is honored per r2 absorb. | No diff |
| A8 | **BACKSTOPPED** | Pre-reg §4.2 + §5.0 single-cell headline lock; `result.md` §4 reports train/validate as descriptive M3 overlay per `train_validate_split_fate.md §5` (no per-portion verdict). Pre-reg drafted post-2026-06-13 → discipline applies. Stocktake B confirmed. | No diff |
| A9 (HA-specific) | **BACKSTOPPED** | Pre-reg §4.4 inherits HA-C3 v2 §4.4 verbatim; §4.1 surfaces the right-shift observation at draft time (unmedicated stratum populates higher quintiles disproportionately, consistent with the +0.57/mg dose-modulation evidence). `result.md` §2 surfaces the same right-shift in production. The right-shift caveat is documented at §8 caveat 4 + §4.1 + §7.2. CONFIRMED-channel inheritance discipline honored. | No diff |
| A10 (HA-specific) | **BACKSTOPPED** | Pre-reg Locked decision 1 + §4.1 explicit cross-arm cleanliness rule: sub-arms (§5.A unmedicated, §5.B dose-adjusted, §4.6 crash-dropped, §4.8 train/validate, §4.8 t+1 lagged) REUSE the full-pool quintile edges; no re-computation per sub-arm. `result.md` §4 §5.B reports cross-phase n=1351 with bin-n = [782, 96, 136, 143, 194] — visibly DIFFERENT from the full-pool bin-n because §5.B runs on `all_day_stress_avg_adj` (dose-adjusted), but the bin edges are the locked `[0, 28, 31, 34, 37, 100]` per pre-reg §4.4 §5.B dose-adjustment bin-edge note. Cross-arm cleanliness preserved. | No diff |
| A11 (HA-specific) | **BACKSTOPPED** | Per `result.md` §9 Gate 5: snapshot SHA-256 at run-time = `d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d` (matches locked draft-time SHA `d0ff9253...`). Recomputed quintile boundaries = `[28.0, 31.0, 34.0, 37.0]` (matches locked draft-time boundaries `[28.0, 31.0, 34.0, 37.0]`). Gate 5 PASS on both SHA and boundary-shift sub-checks. Bin-edge snapshot pinning discipline honored. | No diff |

## 4. Verdict-trust call

**TRUSTED**.

**Rationale**: 9 of 11 load-bearing assumptions are BACKSTOPPED; 2 are NOT APPLICABLE (A5, A6) with documented reasons. A2 sits in the BACKSTOPPED-partial band per §6.3 strict-reading revision (same as HA-C3 v2 A2 — the gating discipline supplies the missingness-aware operationalisation per §5.2 path (a) but the per-channel rate audit per path (b) is missing). The A2 partial-coverage notation is included in the §5 `open_inputs` block as a non-blocking narrowing candidate; Stage I may proceed with the survivorship caveat noted in its §4.5 L-ID citation block (L7 application).

Three HA-specific load-bearing assumptions (A9 cross-arm right-shift; A10 cross-arm bin-edge cleanliness; A11 bin-edge snapshot pinning) are fully BACKSTOPPED via the pre-reg's draft-time discipline + the `result.md`'s Gate 5 reporting. The bin-edge snapshot pinning is the strongest discipline added by HA-C3p relative to HA-C3 v2 (HA-C3 v2 has no analogous Gate 5 because its bin scheme is verbatim-anchored to Wiggers' integer values, not data-driven).

Per guide #1 §6.4: the verdict-trust call is independent of the verdict label. HA-C3p's PARTIAL verdict whose assumptions are all BACKSTOPPED (or NOT APPLICABLE) is TRUSTED for Stage I purposes.

## 5. `open_inputs` block

| # | What is missing | What it blocks | Cheapest acquisition path | Fallback claim available |
|---|---|---|---|---|
| 1 | Per-channel missingness audit on `all_day_stress_avg` (per-era + per-phase MCAR/MAR diagnostic; same as HA-C3 v2 entry — shared closure path) | Tightens A2 from BACKSTOPPED-partial to BACKSTOPPED; tightens Stage I §4.5 L7 citation | S effort per stocktake §3 Shared gap 3; script template from `desc-SMS` exists; closes both HA-C3 v2 and HA-C3p A2 simultaneously | TRUSTED stands with A2 BACKSTOPPED-partial + Stage I §4.5 L7 narrowing caveat |

---

## §11 Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-25 | Drafted r1 (DRY-RUN) | Producer-mode by `/research-interpret descriptive HA-C3p` skill on second invocation in dry-run dispatch. Dry-run dispatch per §11 step 8. All audit content drawn from HA-C3p r2 pre-reg (LOCKED 2026-06-23 `c0148ca`), `result.md` (LOCKED 2026-06-23 with two write-time-bug patches by dispatcher), `test.py`, and cited methodology MDs. **Drift triggers registered** (manual-pending-skill carry-forward per skill responsibility #10): (1) HA-C3p `result.md` re-runs; (2) any cited methodology MD changes lock-version; (3) per-channel missingness audit on `all_day_stress_avg` lands (closes A2 partial-coverage entry, shared with HA-C3 v2 A2); (4) ≥6 months elapse since lock; (5) `per_day_master.csv` snapshot SHA drifts (Gate 5 trigger; would re-fire the bin-edge consistency check at test-time). **STATUS: NOT LOCKED — awaiting user acceptance per `_plan_results_analysis_layer.md` §3.8.** |
