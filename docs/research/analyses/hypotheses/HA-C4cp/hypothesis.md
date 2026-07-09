# HA-C4cp — Personal-baseline SD-anchored sister-pre-reg to HA-C4c (Wiggers C4 "stress doesn't decrease" on personal-baseline-rolling reference)

## Authorship

**Drafted 2026-07-09** by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem.

**Drafting trigger**: OI-033 sister-pre-reg pathway per [`_open_inputs.md`](../../../methodology/_open_inputs.md) OI-033 (surfaced 2026-07-09 Bundle H+ event 4 immediately post-[OI-025 protocol §4](../HA-C4c-stringency-companion/protocol.md#4-step-2-pre-committed-decision-rule) NON-TRIGGER closure) + user Q "lets continue with OI-033 personal-baseline SD-anchored sister-HA pre-reg — parent MD bout_level_recovery_dynamics.md §3.2 extension + full 6-stage cascade if it aspires to actionability; M effort at pre-reg draft time" 2026-07-09. Sister-pre-reg to [HA-C4c r2 LOCKED 2026-07-08](../HA-C4c/hypothesis.md) (the Wiggers-C4 fixed-absolute-threshold arm), analogous to the [HA-C3 v2](../HA-C3/hypothesis.md) → [HA-C3p](../HA-C3p/hypothesis.md) sister-pre-reg pattern that [`actionability_translation.md`](../../../methodology/actionability_translation.md#421-condition-2--cross-operationalisation-independence-inside-the-cluster) guide r3 §4.2.1 condition 2 explicitly cites as the canonical model.

**OI-033 vs OI-025 pathway attribution** (LOAD-BEARING clarification per fresh-session /research-review L4.7 fire absorb): HA-C4cp operationalises the **OI-033 closure pathway** for the cross-op-independence gap surfaced at [Stage A construct-bout-recovery-signal.md §5.6 row-6](../../actionability/construct-bout-recovery-signal.md), NOT the OI-025 Step 2b conditional pathway. **OI-025 pathway was exhausted** at Track B Step 1 Pass 1 execution 2026-07-09 (Bundle H+ event 4, commit `589d93a`) which returned **NON-TRIGGER** per protocol §4 asymmetric-bar rule (f2(T) > 0.30 at T ∈ {30, 60}: f2(30) = 0.5863; f2(60) = 0.3846; f2(120) = 0.1688; f2(180) = 0.1020); consequently OI-025 status transitioned CLOSED-DESCRIPTIVE-ONLY-COMPLETED without triggering any Step 2 pre-registration, and its Step 2b conditional pathway is unreachable. **OI-033 is INDEPENDENT of the stringency-family** (30/60/120/180-min absolute-threshold operand family) that OI-025 exhausted — the SD-anchored operand family HA-C4cp operationalises is a fundamentally different reference-frame construction (personal-baseline-rolling vs fixed-absolute-threshold) per parent MD §3.2.2 + OI-025 protocol §5.4 four-condition independence argument. HA-C4cp inherits the LOAD-BEARING pre-committed operand family + cross-op-independence argument from OI-025 protocol §5.3-§5.4 as OPERAND-FAMILY SPECIFICATION (locked drafting-time discipline preserved) but NOT as a Step 2b triggered pathway.

**Cluster C-bout-substance closure per OI-025 protocol §5.5 CLOSURE PATH** (framing applies via OI-033 pathway now that OI-025 pathway is exhausted): this pre-reg IS the second substantive cluster member for [cluster C-bout-substance](../../synthesis/cluster-C-bout-substance.md). On `result.md` LOCK, cluster C-bout-substance moves from single-member (HA-C4c) to 2-member (HA-C4c + HA-C4cp) and the cross-op-independence gap named at Stage A §5.2 closes at the strict guide §4.2 two-independent-HAs bar — no longer via §4.2.1's gap-named-with-closure-pathway rule.

**Data exposure context** (audit-able): the drafter has seen (a) HA-C4c r2 result summary — PARTIAL magnitude-below-threshold verdict at Cliff's δ = +0.1523, empirical p = 0.0091, on cross-phase-pooled n = 1274 heavy-T-vs-non-heavy-T with the bar (b) missed but (a) cleared; (b) HA-C4c-stringency-companion Pass 1 NON-TRIGGER outcome (f2(T) numeric: {30: 0.5863, 60: 0.3846, 120: 0.1688, 180: 0.1020}) which corroborated at descriptive layer that only the 180-min stringent absolute threshold captures a genuinely tail-rare event; (c) the parent MD §3.2.2 DRAFT-r3 operand family (co-locked with this pre-reg per Bundle H+ event 7). The drafter has NOT computed any HA-C4cp per-day operand values or reference-window statistics on the corpus; those are Stage D descriptive-audit outputs deferred to the run-step per [`hypothesis_lock_process.md §3.9`](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). The HA-C4c PARTIAL verdict enters as a **caveat-class prior** per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) informing HA-C4cp's interpretation; HA-C4cp does NOT pre-commit to a specific magnitude on the SD-anchored operand.

**Locked decisions at draft time** (load-bearing pre-commits per [`hypothesis_lock_process §3.2 step 5`](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) + OI-025 protocol §5.3 pre-committed operand family):

1. **Primary operand**: `bout_n_did_not_return_2sd_day` — per-day count of bouts with `did_not_return_2sd_flag == True` per parent MD [§3.2.2](../../../methodology/bout_level_recovery_dynamics.md#322-personal-baseline-sd-anchored-derivative-operand-family-added-2026-07-09-per-oi-025-protocol-53--oi-033-sister-pre-reg-pathway). Rationale: (i) stringent tail-focused count mirrors HA-C4c's 180-min-cap tail focus but on a personal-baseline-rolling reference frame; (ii) Z=2 corresponds to ~2.5% tail under normality — a genuinely tail-rare event, matching the Wiggers-C4 "atypical for me" reading; (iii) binary rollup is more directly interpretable than the continuous `bout_return_time_z_max_day` for a heavy-T vs non-heavy-T contrast. Selected per user Q "bout_n_did_not_return_2sd_day (recommended)" 2026-07-09.

2. **Primary stratum**: cross-phase-pooled per HA-C4c §4.2 verbatim (default per OI-025 protocol §5.3). Rationale: (a) same reference frame as HA-C4c; the cross-op independence claim is at operand-family level, not stratum level, so stratum inheritance from HA-C4c is the honest sister-pattern; (b) recalibration 0/7 CONFIRMED finding at bout-level per [bout_level_dose_response_calibration §6](../../../methodology/bout_level_dose_response_calibration.md) means cross-phase pooling does not violate per-channel inheritance for bout-level operands at this corpus's bout-level n; (c) larger n provides better power for the SD-anchored operand which will have lower per-day count magnitude than the absolute-threshold operand. Unmedicated-only stratum reported as sensitivity arm per §4.10.

3. **Direction of effect under SUPPORTED**: `bout_n_did_not_return_2sd_day` is HIGHER on heavy-T days than on non-heavy-T days (one-sided elevated, mirroring HA-C4c §4.1). Rationale: same underlying autonomic-dysregulation prior; the personal-baseline SD-anchored operand is a different measurement of "the bout took longer to return than usual for me" but the mechanistic direction is unchanged.

4. **Effect-size bar**: Cliff's delta ≥ +0.20 for SUPPORTED, matching HA-C4c §5.1 two-bar discipline verbatim. Rationale: keeps the sister-pre-reg's SUPPORTED threshold identical to HA-C4c's so the two-cluster-member verdicts can be read at comparable stringency; explicitly does NOT relax the bar to +0.15 despite the operand-family compression argument (per user Q "δ ≥ +0.20 primary, sensitivity at Z=1 (recommended)" 2026-07-09; the sister-pattern discipline wins over compression-of-effects). If this bar produces PARTIAL where HA-C4c produced PARTIAL, that is a genuinely honest 2-member cluster verdict rather than an artefact of relaxed discipline.

5. **Discrimination bar**: empirical one-sided p < 0.05 from the block-permutation null at E[L]=7 days, matching HA-C4c §4.6 verbatim.

6. **Sensitivity Z-threshold**: Z=1 (`bout_n_did_not_return_1sd_day`) as descriptive companion at §4.10; not part of the Holm family per §5.3 (single-cell headline lock discipline). Rationale: gives visibility on whether the SD-anchored family's signal is present at less-stringent Z but does not promote to SUPPORTED on its own.

7. **Continuous SD-anchored companion**: `bout_return_time_z_max_day` re-run at §4.10 as descriptive sensitivity ONLY (continuous outcome; different test shape than the count-based primary; reported for shape-of-signal interpretation).

8. **Reference-window validity gate**: ≥ 30 bouts in `[d-90, d-30]` per parent MD §3.2.2. Days failing the gate route the derivative operand to NaN; the day is excluded from the HA-C4cp primary cell via §4.4 gate. Rationale: matches CONVENTIONS §3.1 personal-baseline discipline for reference-pool validity.

9. **Framework-validity gate**: inherited from parent MD §6 verbatim per parent MD §3.2.2 explicit statement — the HA11 v1 reproduction on `bout_n_fast_recovery_day` is UNCHANGED and remains the operand-family framework-validity gate that HA-C4cp inherits. HA-C4cp does not re-run the framework-validity gate; HA11-bout-redo's landed PARTIAL verdict per [HA11-bout-redo result.md](../HA11-bout-redo/result.md) carries forward as the gate's clearance status per HA-C4c §9.6 inheritance pattern.

10. **Result reporting**: `result.md` will land the HA-C4cp verdict alongside the HA-C4c result.md verdict in the [cluster C-bout-substance §5 Layer 3 substantive coherence pass](../../synthesis/cluster-C-bout-substance.md); per [`internal_synthesis.md`](../../../methodology/internal_synthesis.md) §5 verdict table the joint reading is CONCORDANT / PARTIALLY CONCORDANT / ORTHOGONAL / CONFLICT depending on the two cell verdicts.

### §3.8 gate-verification block (dispatched at DRAFT time, awaiting r2 LOCK per [`hypothesis_lock_process.md` §3.8](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc))

The four [§3.8 lock-blocking gates](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc) status at DRAFT-r1:

1. **Power-calc dispatch** — MET via §8 caveat 1 ([Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design citation; the block-permutation null at E[L]=7 is the within-subject inferential machinery; the §5.1 two-bar SUPPORTED gate determines PASS/PARTIAL/REJECTED; INCONCLUSIVE per §5.2 is the operational definition of "underpowered for this cell").
2. **Multi-comparison discipline** — MET via §5.0 single-cell headline lock (one headline cell: cross-phase-pooled stratum × `bout_n_did_not_return_2sd_day` × heavy-T-vs-non-heavy-T × two-bar SUPPORTED gate per §5.1). Every other arm — Z=1 sensitivity (§4.10), continuous z_max sensitivity (§4.10), unmedicated-only stratum (§4.10), motion-clean-only (§4.10), transient-excluded (§4.10), baseline-invalid-excluded (§4.10), crash-drop (§4.10), reference-window-shorter-lag sensitivity (§4.10) — is descriptive sensitivity ONLY and cannot promote to SUPPORTED. Holm step-down across the sensitivity family at §5.3 provides effective multiplicity control at the SUPPORTED bar.
3. **Register-row pointer** — MET at r2 LOCK-commit (DISPATCHER HANDLES): HA-C4cp is added under the existing [`wiggers_testable_hypotheses.md` Tier 1 C4 row](../../../wiggers_testable_hypotheses.md) as the personal-baseline-anchored sister-test pointer (HA-C4c remains the primary register-row anchor as the Wiggers-verbatim absolute-threshold test). Register-row update is consolidated at r2 LOCK-commit alongside `_open_inputs.md` OI-033 status transition + Stage A §5.6 row-6 pointer update.
4. **Re-audit clean OR §3.6 compression** — pending fresh-session `/research-review` dispatch per user Q "Dispatch both reviews as background subagents this session" 2026-07-09; verdict absorbed at r2 LOCK.

| revision | date | summary |
|---|---|---|
| r1 (DRAFT) | 2026-07-09 | Initial draft at Bundle H+ event 7 co-lock-cycle with parent MD `bout_level_recovery_dynamics.md` §3.2.2 DRAFT-r3 extension. Sister-pre-reg to HA-C4c r2 LOCKED (personal-baseline SD-anchored sister to HA-C4c's fixed-absolute-threshold Wiggers-C4 arm); operand candidates pre-committed at OI-025 protocol §5.3 LOCKED r1 2026-07-09 (Bundle H event 2, commit `a943f31`). Primary operand `bout_n_did_not_return_2sd_day` per parent MD §3.2.2 (`bout.tail_length > subject_lagged_median(d) + 2 × subject_lagged_mad(d)` on `[d-90, d-30]` LC-era lagged reference). Cross-phase-pooled stratum inherited from HA-C4c §4.2 verbatim. Two-bar SUPPORTED gate (block-perm p < 0.05 + Cliff's δ ≥ +0.20) inherited from HA-C4c §5.1 verbatim per user Q "δ ≥ +0.20 primary, sensitivity at Z=1 (recommended)" 2026-07-09. |
| r2 | 2026-07-09 | §3.6-compression r2 absorbing fresh-session /research-review fires per [`reviews/HA-C4cp-2026-07-09.md`](../../../reviews/HA-C4cp-2026-07-09.md) verdict PASS-with-caveats. **Substantive absorbs** (3): (1) L4.7 REQUIRED — Authorship OI-033 vs OI-025 pathway attribution clarified (HA-C4cp operationalises **OI-033 closure pathway**, NOT OI-025 Step 2b conditional pathway which was exhausted at NON-TRIGGER outcome per f2(T) > 0.30 at T ∈ {30, 60}); pre-committed operand family + cross-op-independence argument inherited from OI-025 protocol §5.3-§5.4 as OPERAND-FAMILY SPECIFICATION but NOT as triggered-pathway framing; (2) L4.3 REQUIRED — §5.3 family-membership caveat expanded to load-bearing statement that Z=1 + z_max + primary share reference-window construction (NOT independent); result.md discipline updated to surface §8 caveat 6 alongside Holm output; reference-window-shorter-lag + reference-pool-`did_not_return`-excluded named as the two genuinely independent reference-window-fragility diagnostics; (3) L1.2 + L2.4 REQUIRED — parent MD `bout_level_recovery_dynamics.md` r3 LOCK confirmation at co-lock-commit (parent MD r3 LOCKED 2026-07-09 §3.6 compression on same commit-cycle per fresh-session methodology-review verdict PASS at [`reviews/bout_level_recovery_dynamics-r3-extension-2026-07-09.md`](../../../reviews/bout_level_recovery_dynamics-r3-extension-2026-07-09.md)); operand columns §3.2.2 will be available in `per_day_master.csv` after post-r2-LOCK pipeline extension co-commit-cycle per §3 pipeline-dependency framing. **Optional absorbs** (2): (4) §1 4-cell agreement matrix caveat-class note added per CONVENTIONS §4.2 discipline (matrix is CAVEAT-CLASS framing, NOT joint-verdict claim; joint interpretation deferred to cluster-C-bout-substance §5); (5) cross-reference to construct-bout-recovery-signal.md §5.5 tier-3 forward-validation sketch informational at §9-10 (via §9.1 SUPPORTED cascade tier-3-aspiration language + Cross-references block already present). **Content preserved verbatim from DRAFT-r1**: §1 headline claim + §2 three priors + §3 data sources + §4.1-§4.11 measurement protocol pre-commits + §5.0-§5.4 verdict machinery + §6 exclusion rules + §7 sanity-check ranges + §8 caveats (with caveat 6 emphasis clarified per absorb 2) + §9 verdict-cascade routing (§9.1-§9.6) + §10 detection script architecture pre-commits + Cross-references. **LOCKED 2026-07-09** by §3.6 compression per fresh-session /research-review verdict PASS-with-caveats and mechanical + clarity fires. |

**Status**: **r2 LOCKED 2026-07-09** by §3.6 compression per fresh-session /research-review verdict PASS-with-caveats at [`reviews/HA-C4cp-2026-07-09.md`](../../../reviews/HA-C4cp-2026-07-09.md). Co-locked with parent MD [`bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md) r3 (LOCKED 2026-07-09 §3.6 compression per fresh-session methodology-review verdict PASS at [`reviews/bout_level_recovery_dynamics-r3-extension-2026-07-09.md`](../../../reviews/bout_level_recovery_dynamics-r3-extension-2026-07-09.md)) at Bundle H+ event 7 co-lock-commit. Pipeline extension for parent MD §3.2.2 operand columns (`bout_return_time_z`, `did_not_return_1sd_flag`, `did_not_return_2sd_flag`, `bout_return_time_z_max_day`, `bout_n_did_not_return_1sd_day`, `bout_n_did_not_return_2sd_day`, plus reference-window audit traces `subject_lagged_median_day` / `subject_lagged_mad_day`) is a Stage D descriptive-audit precondition tracked separately from this pre-reg's LOCK per §3 pipeline-dependency framing; lands in post-LOCK co-commit-cycle. Dry-run + result.md dispatched at user tempo per §9 verdict-cascade routing.

---

**Pre-registration drafted 2026-07-09 as r1**, BEFORE any HA-C4cp test run, BEFORE any inspection of `bout_n_did_not_return_2sd_day` per-day values or `subject_lagged_median` / `subject_lagged_mad` reference-window statistics on the corpus. The drafter has HA-C4c's r2 result (PARTIAL magnitude-below-threshold at Cliff's δ = +0.1523, empirical p = 0.0091, cross-phase-pooled n = 1274) as caveat-class context per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), and HA-C4c-stringency-companion Pass 1 NON-TRIGGER outcome (f2(T) monotone descent from 0.5863 to 0.1020) as substantive descriptive-layer corroboration of the Stage I §3 stringent-operand-threshold interpretation. Any change after lock creates HA-C4cp-v2 with r1 archived.

HA-C4cp tests the **Wiggers-C4 "stress doesn't decrease" substantive question** on a personal-baseline-rolling reference frame (per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline discipline + [CONVENTIONS §3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) `_lagged_lcera` window discipline), rather than HA-C4c's fixed-absolute-threshold reference frame (180-min forward cap + `+5` baseline tolerance in raw stress units). The two pre-regs are sister operationalisations of the same Wiggers C4 substantive question at cross-operationalisation-independent operand levels per OI-025 protocol §5.4 four-condition independence argument.

## 1. Claim

Within the LC frame, on the cross-phase-pooled stratum inherited from HA-C4c §4.2, days when the participant's exertion class on T is heavy or very-heavy (`exertion_class_lagged_lcera(T) ∈ {heavy, very_heavy}`) show a HIGHER per-day count of within-day stress bouts whose return-time exceeds the personal `[d-90, d-30]` LC-era lagged reference mean by more than 2 SDs, compared to non-heavy-T days (`exertion_class_lagged_lcera(T) ∈ {none, light, moderate}`).

**Headline cell** (single-cell headline lock per §5.0): cross-phase-pooled stratum × `bout_n_did_not_return_2sd_day` × heavy-T-vs-non-heavy-T × {Mann-Whitney U + Cliff's delta + block-permutation null at E[L]=7} × two-bar SUPPORTED gate per §5.

**Sister-pre-reg pointer**: HA-C4cp is the **personal-baseline-anchored sister** to [HA-C4c r2 LOCKED](../HA-C4c/hypothesis.md) (the **Wiggers-verbatim fixed-absolute-threshold** test of the same Wiggers C4 substantive question). The two pre-regs are sister operationalisations:

| HA-C4c verdict | HA-C4cp verdict | reading |
|---|---|---|
| SUPPORTED | SUPPORTED | strong Wiggers C4; both fixed-absolute AND personal-baseline-rolling operationalisations fire |
| SUPPORTED | REJECTED | signal is anchored to the 180-min absolute threshold, not to atypicality against subject's own recent distribution — Wiggers C4 as a fixed-time-window claim, not a "took longer than usual for me" claim |
| REJECTED | SUPPORTED | signal is on subject's own atypical-return dimension; the fixed-absolute-threshold arm was miscalibrated for this participant's per-minute stress trace |
| REJECTED | REJECTED | informative null on both operationalisations; the substantive Wiggers C4 question does not fire at bout-level on this corpus regardless of operationalisation |
| PARTIAL | any | mixed-signal reading at joint-cluster level; internal-synthesis MD §5 partially-concordant / orthogonal / conflict routing applies |

Each pre-reg's §5 verdict stands on its own; the 2-member cluster reading lives in [cluster-C-bout-substance.md](../../synthesis/cluster-C-bout-substance.md) §5 Layer 3 substantive coherence pass per `internal_synthesis.md`.

**Caveat-class framing note per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)** (per fresh-session /research-review Optional-4 absorb): the 4-cell agreement matrix above is CAVEAT-CLASS framing informing HA-C4cp's verdict-interpretation, NOT a joint-verdict claim and NOT a HA-C4cp §5 pre-commit. Joint interpretation of the two cluster-member verdicts is deferred to [cluster-C-bout-substance.md](../../synthesis/cluster-C-bout-substance.md) §5 per [`internal_synthesis.md`](../../../methodology/internal_synthesis.md) §5 verdict table (CONCORDANT / PARTIALLY CONCORDANT / ORTHOGONAL / CONFLICT verdict routing). HA-C4cp does NOT claim any joint-verdict outcome pre-emptively.

**Direction of effect under SUPPORTED** (HA-C4cp): (a) `bout_n_did_not_return_2sd_day` mean is HIGHER on heavy-T days than on non-heavy-T days; (b) Cliff's delta ≥ +0.20 in the predicted positive direction; (c) empirical one-sided block-permutation p < 0.05.

**Verdict rule** (two-bar SUPPORTED gate): see §5.

## 2. Why we think this

Three priors anchor HA-C4cp:

**(a) Wiggers source — verbatim** (qualitative claim, mechanism-not-operand reading): the Wiggers PDF describes a stuck-sympathetic post-exertion pattern where "stress doesn't decrease, despite resting" — a claim about the participant's within-day stress recovery being **atypical relative to normal**. HA-C4c operationalises "atypical" as "exceeds 180-min absolute cap"; HA-C4cp operationalises "atypical" as "exceeds subject's own recent distribution by 2 SDs". Both are honest operationalisations of the Wiggers verbatim; they differ in reference frame. The qualitative claim is mechanism-bound (autonomic dysregulation → sustained sympathetic tone → longer-than-usual return-time on stress bouts), not reference-frame-bound.

**(b) [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline discipline**: "For any PEM-pacing metric, work with deviations from the participant's own rolling baseline rather than absolute cutoffs. A max HR of 130 is a spike for one PEM patient and a calm afternoon for another." Personal-baseline framing is the project-canonical operationalisation discipline; HA-C4cp is the project-canonical sister to HA-C4c's Wiggers-verbatim absolute-threshold framing. The `[d-90, d-30]` `_lagged_lcera` window per [CONVENTIONS §3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) is the sustained-push-hypothesis lagged-baseline convention; applied to `tail_length` gives a rolling personal reference for how long the subject's bouts usually take to return.

**(c) HA-C4c PARTIAL magnitude-below-threshold verdict as caveat-class prior** per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no): HA-C4c's r2 landed Cliff's δ = +0.1523 with empirical p = 0.0091 on cross-phase-pooled n = 1274 — direction-correct, discrimination bar cleared, effect-size bar (+0.20) missed by −0.05. This is a caveat-class prior informing HA-C4cp's verdict interpretation, NOT a quasi-result promoted to a substantive HA-C4cp output. HA-C4cp's primary §5.1 verdict will formally evaluate whether the personal-baseline-rolling operationalisation produces a comparable pattern. The HA-C4c-stringency-companion NON-TRIGGER outcome (Pass 1 monotone descent of f2(T)) corroborated at descriptive layer that only the 180-min stringent absolute threshold captures a genuinely tail-rare event; the SD-anchored family at Z=2 tests whether the "genuinely tail-rare" reading generalises to a personal-baseline-rolling reference frame. Under SUPPORTED, HA-C4cp shows the pattern also fires on the personal-baseline dimension; under REJECTED, it shows the pattern is anchored to the fixed-absolute-threshold dimension only.

**Sister-test context** (informational; no cross-test prior on the primary verdict is claimed):

- **HA-C4c r2 LOCKED PARTIAL** (2026-07-08; cross-phase-pooled n = 1274; Cliff's δ = +0.1523; p = 0.0091): fixed-absolute-threshold sister; the same substantive question at 180-min forward-cap operationalisation.
- **HA-C4c-stringency-companion NON-TRIGGER** (2026-07-09 Pass 1): descriptive companion at 30/60/120/180-min operand family; corroborated at descriptive layer that stringent-operand-threshold interpretation stands.
- **HA11-bout-redo PARTIAL** (framework-validity level; 2026-06-22): reproduction of HA11 v1 U-dip count signal at bout level on the fast-recovery operand; PARTIAL on the calm-day pool. HA-C4cp inherits the framework-validity gate clearance status per §9.6 (see below).
- **HA-C4 v2 REJECTED at daily-aggregate** (2026-06-15): the daily-aggregate arm of the same substantive question; the bout-level pivot per HA-C4 v2 §9 was to open the within-day resolution. HA-C4cp shares that pivot's motivation.

## 3. Data sources

Inherited from [HA-C4c §3](../HA-C4c/hypothesis.md#3-data-sources) verbatim, with additive column requirements from parent MD §3.2.2:

- Base substrate: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` for per-day columns (heavy-T classification, day-validity flags, phase metadata, sensitivity-arm indicators).
- Per-bout substrate: `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` for `did_not_return_2sd_flag`, `did_not_return_1sd_flag`, `bout_return_time_z`, and the corresponding per-day rollups joined into `per_day_master.csv`.
- Additive columns per parent MD §3.2.2 co-lock at r3: `subject_lagged_median_day`, `subject_lagged_mad_day`, `bout_return_time_z_max_day`, `bout_n_did_not_return_1sd_day`, `bout_n_did_not_return_2sd_day` in `per_day_master.csv`.
- `is_crash` from crash_v2 labels.
- `exertion_class_lagged_lcera` on T per HA-C4c §3.

**Pipeline dependency**: HA-C4cp requires the extended `03_consolidate/build_unified_dataset.py` producing the parent MD §3.2.2 columns. Pipeline extension is a Stage D descriptive-audit precondition tracked separately from this pre-reg's LOCK; pre-reg LOCK does NOT require the pipeline extension to have landed (pre-reg locks the analytical spec, not the pipeline state). Pipeline extension lands in a separate co-commit-cycle post-pre-reg-LOCK.

## 4. Measurement protocol

### 4.1 Operand definition (locked pre-commit per Authorship "Locked decisions" item 1)

**Primary operand**: `bout_n_did_not_return_2sd_day` — per-day count of bouts on day `d` with `did_not_return_2sd_flag == True` per parent MD [§3.2.2](../../../methodology/bout_level_recovery_dynamics.md#322-personal-baseline-sd-anchored-derivative-operand-family-added-2026-07-09-per-oi-025-protocol-53--oi-033-sister-pre-reg-pathway).

The per-bout `did_not_return_2sd_flag(d, i)` fires when `bout_i.tail_length > (subject_lagged_median(d) + 2 × subject_lagged_mad(d))`, where `subject_lagged_median(d)` and `subject_lagged_mad(d)` are the median + `1.4826 × MAD` of the per-bout `tail_length` distribution over the `[d-90, d-30]` lagged LC-era reference pool per parent MD §3.2.2 (bout-level reference, ≥ 30 bouts validity bar, `did_not_return_flag` bouts included in reference as-is, April 2024 cluster excluded). Per parent MD §3.2.2 this operationalises the Wiggers-C4-positive per-event case ("this bout's return-time is atypical for the subject's own recent distribution") on the personal-baseline-rolling reference frame — cross-operationalisation-independent (per OI-025 protocol §5.4) of HA-C4c's fixed-absolute-threshold operationalisation.

The per-day count `bout_n_did_not_return_2sd_day(d)` aggregates these per-bout positives over the day, producing an integer (`0` on valid days with no flagged bouts; NaN on reference-window-invalid days or §3.4-invalid days per the pipeline README).

**Transient handling**: per parent MD §3.1 r2 absorb, transient bouts are INCLUDED in the primary operand without down-weighting (structural determinism inherited from HA-C4c §4.1). HA11-bout-redo's transient-fragility finding acknowledged at §8 caveat 5; HA-C4cp reports the transient-excluded sensitivity arm at §4.10 as a parallel to HA-C4c §4.10.

**Direction-of-effect under SUPPORTED**: `bout_n_did_not_return_2sd_day` is HIGHER on heavy-T days than on non-heavy-T days (one-sided elevated per §1).

### 4.2 Stratum (locked pre-commit per Authorship "Locked decisions" item 2)

**Primary stratum**: cross-phase-pooled per HA-C4c §4.2 verbatim — `citalopram_phase(d) ∈ {unmedicated, buildup, consolidation, afbouw, post_afbouw}` per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification), restricted on the `recovery_phase` axis to sub-phase 4b (`pacing_habit_established`; 2022-11-17 → 2024-04-08) UNION phase 5 (`citalopram_modulated`; 2024-04-09 onward, excluding April 2024 cluster) per [`lc_recovery_phase_axis §3.4b + §3.5`](../../../methodology/lc_recovery_phase_axis.md).

Same rationale as HA-C4c §4.2: (a) the 2024-04-09 `unmedicated → buildup` boundary is not load-bearing for bout-level analyses at this corpus's bout-level n per the recalibration 0/7 CONFIRMED finding ([bout_level_dose_response_calibration §6](../../../methodology/bout_level_dose_response_calibration.md)); (b) pooling gains ~70 day-clusters of n; (c) permissible without §5.A/B/C inheritance violation per recalibration §6 (0/7 features CONFIRMED → Approach A NOT load-bearing → no per-channel inheritance binding for bout-level operands at this n).

**Primary sensitivity arm — unmedicated-only stratum**: `citalopram_phase(d) == unmedicated` only (LC era 2022-04-04 → 2024-04-08, restricted to days `>= 2022-11-17`, excluding April 2024 cluster). Mirrors HA-C4c §4.2 sensitivity arm; reported per §4.10.

### 4.3 Heavy-T eligibility (verbatim from HA-C4c §4.3)

A day `T` is a **heavy-T candidate** if `exertion_class_lagged_lcera(T) ∈ {heavy, very_heavy}`. A day is a **non-heavy-T candidate** if `exertion_class_lagged_lcera(T) ∈ {none, light, moderate}`. Days with missing exertion classification are excluded from the comparison.

**Note vs HA-C4c**: identical eligibility rule. The T-only conditioning (no T-1 union per HA-C4b) is preserved because `bout_n_did_not_return_2sd_day` is a same-day per-day operand.

### 4.4 Day-validity gate (verbatim from HA-C4c §4.4 + additive from parent MD §3.2.2)

A day `T` enters the comparison if all of:

1. `T` is in the LC era (`>= 2022-04-04`) AND in the primary stratum per §4.2.
2. `T` is NOT in the April 2024 cluster (`2024-04-09 → 2024-04-16`).
3. `T` is NOT in the first 21 days of `has_garmin_uds=True` coverage.
4. `T` has computable `bout_n_did_not_return_2sd_day` (i.e. non-NaN per the pipeline day-validity gate: ≥ 600 valid per-minute stress samples on `T` AND `subject_lagged_median(T)` non-NaN per parent MD §3.2.2 reference-window validity bar of ≥ 30 bouts in `[T-90, T-30]`).
5. `T` has computable `exertion_class_lagged_lcera` (i.e. heavy-T classification is non-NaN).

**Reference-window validity impact on left-edge coverage**: the `[T-90, T-30]` reference window requires ≥ 30 bouts on days in that window; days with insufficient in-window bouts (typically the first ~60-90 days of `has_garmin_uds=True` coverage; the coverage-gap 2024-04 window) route the operand to NaN and are excluded via §4.4 gate 4. This is expected to trim ~30-60 days from the left edge of each stratum relative to HA-C4c's primary cell (which does not carry the reference-window gate). Per-arm n reported at result-time; the trim is not expected to materially change the ≥30-per-arm walk-forward gate at §4.7.

### 4.5 Chain-T+1 exclusion (NOT APPLICABLE for HA-C4cp)

Inherits HA-C4c §4.5 verbatim. Same-day per-day count on T only; no T+1 cross-day operand. Informational only.

### 4.6 Statistical machinery (locked pre-commits)

For the primary cell + each sensitivity arm:

1. **Mann-Whitney U statistic** on `bout_n_did_not_return_2sd_day` values: heavy-T arm vs non-heavy-T arm. One-sided (heavy-T > non-heavy-T per §1 directional prediction).
2. **Cliff's delta** as the non-parametric effect size: `delta = (n_heavy>non − n_heavy<non) / (n_heavy × n_non)`. Range [-1, +1]; positive = heavy-T > non-heavy-T.
3. **Block-permutation null at E[L]=7 days**: per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) + parent MD §5.1 inheritance. Permute the binary `is_heavy_T[d]` label sequence in geometric-distributed blocks (mean E[L]=7 days) while keeping the per-day `bout_n_did_not_return_2sd_day` values in their original temporal positions. Empirical one-sided p-value = `(1 + #{U_null >= U_observed}) / (B + 1)` with B = 10,000 null draws.
4. **Cell SUPPORTED** if: empirical p < 0.05 AND Cliff's delta ≥ +0.20 in the predicted positive direction (per §5 verdict rule).

**Seed**: `RANDOM_SEED = 20260709` (HA-C4cp distinct seed; distinct from HA-C4c's `20260623`, HA-C4c-stringency-companion's `20260707`, HA11-bout-redo's `20260622`, HA-C4 v2's `20260618`, HA-C3p's `20260624`, HA-C3 v2's `20260623` — HA-C4cp's seed is drafting-date-anchored per the same convention).

**E[L]\* data-driven companion** + **factor-of-2 flag** per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) + CONVENTIONS §3.6: compute the data-driven `E[L]*` on `bout_n_did_not_return_2sd_day[d]` over the primary stratum; flag if `|E[L]* − 7| / 7 > 0.5`. The flag is descriptive context only (does NOT modify the §5 verdict); per the empirical anchor in parent MD §5.1 r2 absorb (6/7 Stratum-4 cells fire the factor-of-2 flag on HA-P6 channels), the flag is expected to fire and is not a halt trigger.

**Holm step-down across sensitivity arms** (per §5.3): the Holm family is {primary, unmedicated-only sensitivity, motion-clean-only sensitivity, transient-excluded sensitivity, Z=1 sensitivity, z_max continuous sensitivity, reference-window-shorter-lag sensitivity} = 7 cells. Holm cutoffs at α=0.05 across 7 comparisons. The Z=1 and z_max sensitivity arms carry the same-operand-family caveat (all draw on the parent MD §3.2.2 reference window; not fully independent); Holm treats them as separate comparisons per the multi-comparison discipline default. The reference-window-shorter-lag arm is `[d-60, d-30]` (not `[d-90, d-30]`) as a sensitivity per §4.10. Baseline-invalid-excluded + crash-drop are NOT in the Holm family (descriptive variants per CONVENTIONS §3.3 column-duplication discipline + §3.4 audit-hook scope).

### 4.7 Walk-forward gate (n ≥ 30 per arm)

Each cell (primary + each sensitivity arm) must have ≥ 30 heavy-T days AND ≥ 30 non-heavy-T days satisfying §4.4 day-validity. Below 30 on either arm, the cell is **INCONCLUSIVE** per §5.2 (does NOT halt the test).

**Expected n per arm** (anchored on HA-C4c §4.7 counts minus the §4.4 reference-window trim estimate): primary cross-phase-pooled stratum heavy-T n ≈ ~317 − ~30 = ~287; non-heavy-T n ≈ ~569 − ~50 = ~519. Sensitivity-arm n on unmedicated-only ≈ ~247 − ~30 = ~217 heavy-T / ~419 − ~50 = ~369 non-heavy-T. All comfortably clear the ≥30 bar. The motion-clean-only sensitivity arm may be degenerate per HA-C4c §4.7 (99.3% motion-confound corpus property at bout level); if so, routes to INCONCLUSIVE per §4.10.

**Left-edge coverage note**: because the `[d-90, d-30]` reference window excludes the leftmost ~60-90 days of `has_garmin_uds=True` coverage (device-baseline-lag interaction with the window), HA-C4cp's effective LC-era start is ~2022-06-01 rather than 2022-04-04. This is expected and does not violate the primary stratum's `>= 2022-11-17` sub-phase-4b left-edge (the reference-window trim is more restrictive than the stratum's own left edge).

### 4.8 Verdict bands (locked pre-commits per §5)

Inherits from HA-C4c §4.8 (INCONCLUSIVE-aware pattern):

| outcome | condition |
|---|---|
| **SUPPORTED** | both bars met (block-perm p<0.05 + Cliff's delta ≥ +0.20) in predicted positive direction |
| **PARTIAL** | direction-correct AND exactly one bar clears, AND the failure is read against §8 caveats |
| **REJECTED** | direction wrong-sign OR both bars fail OR §4.10 crash-drop sensitivity surfaces direction-flipping |
| **INCONCLUSIVE** | walk-forward gate (§4.7) not met OR §10.4 sanity gates fail |

See §5 for the full bar-by-bar definitions and verdict rule precedence.

### 4.9 Approach A inheritance — SAME analogue-inheritance descriptive companion as HA-C4c §4.9

**Underpowered-NULL framing leads** (verbatim from HA-C4c §4.9): per [`bout_level_dose_response_calibration §6` (r4 LOCKED)](../../../methodology/bout_level_dose_response_calibration.md) + STOCKTAKE §6, the bout-level β recalibration produced 0/7 CONFIRMED at the discriminative bar. Approach A is NOT load-bearing for HA-C4cp at this corpus's bout-level n. The framing discipline preserved at HA-C4c §4.9 five surfaces carries through unchanged.

**Inheritance-by-analogue as descriptive companion**: the closest-analogue feature `bout_n_fast_recovery_day` with buildup-post-CPAP β = −0.056/mg [95% CI −0.145, +0.034] p=0.223 is the inheritance template. Sign-flipped to match HA-C4cp's +1 prior direction on `bout_n_did_not_return_2sd_day` (more failures-to-return-within-tail under elevated sympathetic tone), the template β becomes +0.056/mg. Approach A sensitivity arm (descriptive companion): `bout_n_did_not_return_2sd_day_adj(d) = bout_n_did_not_return_2sd_day(d) − 0.056 × dose_plasma_mg(d)`.

Re-run the §4.6 primary procedure on the dose-adjusted operand; report alongside the primary as a **SENSITIVITY-ARM-ONLY** inheritance, NOT a primary-arm bias-correction. Explicitly marked as **inheritance-by-analogue (descriptive companion under the underpowered-NULL frame)** in the result.md per §8 caveat 3.

**Why this is a descriptive companion, not a load-bearing dose-correction** (anchors the framing; §8 caveat 3 restates load-bearingly): (1) source β is NULL/weakly-consistent per recalibration's underpowered-NULL framing; (2) analogue substitution adds further uncertainty; (3) underpowered-NULL framing cascades to HA-C4cp; (4) CI-crosses-zero β as load-bearing would inject noise into the primary verdict. Sensitivity-of-verdict-to-CI-bounds sub-arm inherits HA-C4c §4.9 machinery verbatim; run at analogue β's CI lower bound (+0.145/mg → −0.145/mg after sign-flip; sign-corrected from `bout_n_fast_recovery_day`'s CI lower) AND upper bound (−0.034/mg → +0.034/mg after sign-flip).

**Note on operand-family compression** (HA-C4cp-specific caveat): the SD-anchored operand family has a different per-day distribution than HA-C4c's fixed-absolute-threshold operand. The analogue β from `bout_n_fast_recovery_day` (also a per-day count but on a different operand definition) is even less directly comparable to HA-C4cp than to HA-C4c — the analogue substitution uncertainty is compounded by the reference-frame-difference at the operand-family level. Reported as a §8 caveat 3 amplification specific to HA-C4cp; the underpowered-NULL framing subsumes this amplification (both source and target are NULL at this n).

### 4.10 Sensitivity arms (descriptive; cannot promote to SUPPORTED)

Per parent MD §3.4 + CONVENTIONS §3.4 + Authorship "Locked decisions" items 6-7:

- **Z=1 sensitivity arm** (per Authorship "Locked decisions" item 6): re-run the §4.6 primary procedure on `bout_n_did_not_return_1sd_day` instead of `bout_n_did_not_return_2sd_day`. Same reference-window definition, same stratum, same statistical machinery. Reported; cannot promote to SUPPORTED. Rationale: gives visibility on whether the SD-anchored family's signal is present at less-stringent Z. If Z=1 arm SUPPORTED but Z=2 primary NOT SUPPORTED, surface as **stringency-boundary finding** (the operand-family signal is present but not tail-focused).
- **Continuous z_max sensitivity arm** (per Authorship "Locked decisions" item 7): re-run the §4.6 primary procedure on `bout_return_time_z_max_day` instead of `bout_n_did_not_return_2sd_day`. Continuous outcome (not a count); the Mann-Whitney U test applies unchanged. Report; cannot promote to SUPPORTED. Rationale: shows whether the signal is on the tail-count dimension or on the per-day max-z dimension (different shape of signal).
- **Reference-window-shorter-lag sensitivity arm**: re-run the §4.6 primary procedure with `subject_lagged_median` and `subject_lagged_mad` computed on `[d-60, d-30]` window instead of `[d-90, d-30]`. Report; cannot promote to SUPPORTED. Rationale: tests whether the primary verdict is robust to the reference-window-length choice per parent MD §3.2.2 alternatives-considered.
- **Unmedicated-only stratum** (per §4.2 secondary): re-run restricted to `citalopram_phase == unmedicated`. Reported; cannot promote to SUPPORTED. If verdict differs from primary, surface as **stratum-fragility finding**.
- **Motion-clean-only arm**: re-aggregate `bout_n_did_not_return_2sd_day` from `per_bout_master.csv` restricted to bouts with `motion_confound_flag == False`. **Anticipated degeneracy** per HA-C4c §4.10 (99.3% motion-confound corpus property); may route to INCONCLUSIVE. If so, reported as **motion-fragility flagged INCONCLUSIVE**.
- **Transient-excluded arm**: restrict to bouts with `transient_flag == False`. **Anticipated fragility** per HA-C4c §4.10 pattern.
- **Baseline-invalid-excluded arm**: restrict to bouts where `baseline_invalid_flag == False`. Expected low-impact descriptive companion per HA-C4c §4.10.
- **Crash-drop sensitivity arm** (CONVENTIONS §3.4): re-run with `is_crash == True` rows dropped from BOTH arms. Same |Δ Cliff's delta| > 0.10 (HA-C4c pattern) OR |Δ pp discrimination| > 5 (HA11-bout-redo pattern) flag rules. If `|Δ Cliff's delta| > 0.20` AND direction flips, route the primary verdict to REJECTED per §5.
- **Reference-pool `did_not_return_flag`-excluded sensitivity arm** (per parent MD §3.2.2 alternatives-considered): re-run with the reference pool excluding bouts where `did_not_return_flag == True`. This tests whether the primary verdict is anchored to the reference-pool inclusion of 180-cap-censored bouts. If verdict differs, surface as **reference-censoring fragility finding**. Per parent MD §3.2.2 rationale (excluding would inflate the derivative flag rate) this arm is anticipated to have a HIGHER flag rate — thus the primary Cliff's δ is anticipated to be LOWER on this arm. Descriptive-companion only.

**Sister-test cross-reference companion** (no statistical machinery, descriptive table): report HA-C4c r2 verdict (PARTIAL magnitude-below-threshold) + HA-C4b v3 verdict (NOT-SUPPORTED motion-filter) + HA11 v1 verdict (SUPPORTED-on-train) + HA11-bout-redo verdict (PARTIAL framework-validity) + HA-C4c-stringency-companion Pass 1 outcome (NON-TRIGGER; f2(T) monotone descent) alongside HA-C4cp primary verdict in the result.md sister-test-table. Per CONVENTIONS §4.4 reviewer-mode discipline: HA-C4cp does NOT claim a cross-test pass conclusion at result-emission time; cross-test interpretation lives in [cluster-C-bout-substance.md](../../synthesis/cluster-C-bout-substance.md) per Stage S₁ internal-synthesis routing.

### 4.11 Per-bout-n reporting discipline (locked per parent MD §6.3 + CONVENTIONS §3.6)

Per parent MD §6.3 + HA-C4c §4.11 inheritance, HA-C4cp's result.md MUST report:

- **Per-arm `n_bouts`**: total bouts in the heavy-T-day pool; total bouts in the non-heavy-T-day pool (cross-phase-pooled stratum); same for the unmedicated-only sensitivity arm.
- **Per-cell decomposition**: `n_did_not_return_2sd_bouts × n_days × n_did_not_return_2sd_bouts_per_day` per-arm.
- **Reference-window audit trace**: per-arm distribution of `subject_lagged_median_day` and `subject_lagged_mad_day` — mean, median, IQR — so the reader can audit the reference-window construction.
- **Reference-window validity failure count**: per-arm count of days routed to NaN via §4.4 gate 4 reference-window shortfall.
- **Named-counts triplet per CONVENTIONS §3.6**: every count phrasing names scheme + unit + source-file (e.g. *"X did-not-return-2SD bouts per `bout_n_did_not_return_2sd_day` count over Y heavy-T days from `per_day_master.csv` cross-phase-pooled stratum"*).

## 5. Pre-registered falsification criterion

### 5.0 Multi-comparison discipline — single-cell headline lock (per Authorship "Mandatory dispatches" + §3.8 gate 2)

HA-C4cp is a **single-cell headline lock**: the headline verdict is the SUPPORTED/PARTIAL/REJECTED/INCONCLUSIVE outcome on the single triple {cross-phase-pooled stratum × `bout_n_did_not_return_2sd_day` × heavy-T-vs-non-heavy-T} per §4.6. All sensitivity arms (Z=1, z_max, reference-window-shorter-lag, unmedicated-only, motion-clean-only, transient-excluded, baseline-invalid-excluded, crash-drop, reference-pool-did-not-return-excluded, Approach A dose-adjusted) are diagnostic / sensitivity ONLY. They are reported in result.md but **none can promote to SUPPORTED on their own**.

### 5.1 Per-cell confirmation bar (applied to the primary cell + each sensitivity arm)

For each cell that meets the §4.7 walk-forward gate (≥ 30 per arm):

**(a) Discrimination**: empirical one-sided p < 0.05 from the block-permutation null at E[L]=7 (per §4.6).

**(b) Effect size**: Cliff's delta ≥ +0.20 in the predicted direction (heavy-T > non-heavy-T).

**Cell SUPPORTED** if BOTH (a) and (b) hold in the predicted positive direction.

### 5.2 Verdict rule (single-operand SUPPORTED/PARTIAL/REJECTED with INCONCLUSIVE handling)

The headline verdict is computed on the primary cell only per §5.0 single-cell headline lock. Verdict bands:

| outcome | condition (primary cell) |
|---|---|
| **SUPPORTED** | both (a) discrimination + (b) effect-size bars met in the predicted positive direction per §5.1 |
| **PARTIAL** | direction-correct AND exactly one of (a) or (b) clears, AND the failed bar is interpreted against §8 caveats |
| **REJECTED** | direction wrong-sign OR both (a) and (b) fail OR §4.10 crash-drop sensitivity surfaces `|Δ Cliff's delta| > 0.20` AND a sign-flip |
| **INCONCLUSIVE** | §4.7 walk-forward gate not met OR §10.4 dry-run sanity gates fail |

**Verdict rule precedence**: INCONCLUSIVE → REJECTED → SUPPORTED → PARTIAL (same as HA-C4c §5.2).

**Honest framing per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)**: HA-C4cp's PARTIAL band is anticipated as a plausible outcome given HA-C4c's r2 landed PARTIAL result (Cliff's δ = +0.1523, missed the +0.20 bar by −0.05). A PARTIAL outcome on HA-C4cp would be a **direction-consistent but magnitude-below-threshold** parallel to HA-C4c's, which at cluster-C-bout-substance level reads as CONCORDANT-BELOW-THRESHOLD (both cells direction-correct, both PARTIAL — the substantive question fires directionally on both operand families but the corpus's effect-size is bounded below the SUPPORTED bar). A SUPPORTED outcome on HA-C4cp (with HA-C4c at PARTIAL) would read as PARTIALLY CONCORDANT — the personal-baseline operationalisation reaches the SUPPORTED threshold that the fixed-absolute-threshold operationalisation missed. A REJECTED outcome on HA-C4cp would read as ORTHOGONAL / CONFLICT depending on direction — the signal is anchored to the fixed-absolute-threshold reference frame only. The verdict rule is structural; applies regardless of which way the (a) / (b) bars actually fall on this corpus.

### 5.3 Holm step-down across sensitivity arms (multiplicity correction; secondary fragility-flag report)

Per §4.6: Holm step-down across the {primary, Z=1 sensitivity, z_max continuous sensitivity, reference-window-shorter-lag, unmedicated-only, motion-clean-only, transient-excluded} family at α=0.05 (7 comparisons). Holm cutoffs at α/7, α/6, α/5, α/4, α/3, α/2, α/1.

The Holm result is REPORTED alongside the uncorrected primary; if the primary survives Holm correction, that's stronger; if it doesn't, that's a multiplicity-fragility flag. The §5.2 hard rule binds the primary verdict from the uncorrected (a)/(b) bars; Holm is secondary report.

**Holm fewer-comparisons disclosure**: if any sensitivity arm returns INCONCLUSIVE (anticipated for motion-clean-only per §4.10 corpus property; possibly for reference-window-shorter-lag if the `[d-60, d-30]` window fails the ≥ 30 bouts validity bar on some days), the Holm step-down family collapses accordingly with explicit annotation. Inherits the disclosure pattern from HA-C4c §5.3 r2 fewer-comparisons absorb.

**Family-membership caveat (LOAD-BEARING per fresh-session /research-review L4.3 absorb)**: the Z=1 and z_max sensitivity arms share the parent MD §3.2.2 reference-window construction with the primary — same `[d-90, d-30]` window, same reference pool, same `subject_lagged_median` + `subject_lagged_mad` scaling. They are NOT fully independent tests; a shared-reference-window construction bias (e.g. `subject_lagged_median` systematically biased on 180-cap-censored `tail_length` distribution) would propagate to all three cells. Holm treats them as separate comparisons per the multi-comparison discipline default, but the **result.md MUST surface §8 caveat 6 prominently alongside the Holm step-down output** — a "Holm passes on Z=2 primary AND Z=1 sensitivity AND z_max continuous sensitivity" reading must NOT be interpreted as independent confirmation of the primary signal; it is instead consistent-reference-window internal-consistency (correlated firings on shared machinery). The reference-window-shorter-lag sensitivity arm is the FIRST INDEPENDENT diagnostic (different window definition); the reference-pool-`did_not_return`-excluded arm at §4.10 is the SECOND (different pool composition). These two arms provide reference-window-fragility diagnostic power that the Z=1 + z_max arms do not.

### 5.4 INCONCLUSIVE bar (per §4.7)

A cell is **INCONCLUSIVE** if either the heavy-T arm OR the non-heavy-T arm has < 30 days satisfying §4.4 day-validity (including the additive reference-window validity gate). INCONCLUSIVE cells DO NOT REFUTE; they yield no (a)/(b) read and are reported as such. If the primary cell is INCONCLUSIVE, the headline verdict is INCONCLUSIVE per §5.2 — HA-C4cp-v2 may be drafted with a different reference-window (e.g. `[d-60, d-30]` promoted to primary if `[d-90, d-30]` produces too much left-edge trim) per §9.

## 6. Exclusion rules (locked)

Inherits from [HA-C4c §6](../HA-C4c/hypothesis.md#6-exclusion-rules-locked) verbatim, PLUS:

- **Reference-window validity**: days where `subject_lagged_median(d)` is NaN (i.e. `[d-90, d-30]` reference pool has < 30 bouts per parent MD §3.2.2 validity bar) are excluded from the primary cell via §4.4 gate 4. These days are coverage-gap not analysable-with-shortfall per parent MD §3.2.2 rationale.
- **Left-edge trim expected**: the leftmost ~60-90 days of `has_garmin_uds=True` coverage (device-baseline-lag interaction with the `[d-90, d-30]` window) are excluded via reference-window shortfall. Combined with the 21-day device-baseline-lag exclusion (HA-C4c §6 inheritance) and the 2022-11-17 sub-phase-4b left edge (HA-C4c §6 inheritance; more restrictive than the reference-window trim), the effective LC-era left edge for HA-C4cp is `>= 2022-11-17` per HA-C4c inheritance — the reference-window trim does not become the binding constraint at the primary stratum.

## 7. Expected effect size if true

**Anchored on**: (i) HA-C4c r2 result summary (PARTIAL at Cliff's δ = +0.1523, empirical p = 0.0091, cross-phase-pooled n = 1274); (ii) parent MD §3.2.2 SD-anchoring rationale (Z=2 corresponds to ~2.5% tail under normality); (iii) the reference-window is subject-relative, so the operand-family compression is expected relative to HA-C4c's absolute-threshold operand.

**Pre-committed sanity-check ranges**:

- **Per-day `bout_n_did_not_return_2sd_day` mean across the primary cross-phase-pooled stratum**: expected in **[0.05, 0.30]** events/day. Anchor: parent MD §3.2.2 Z=2 flag rate ≈ 2.5% under normality × ~3-5 bouts/day average ≈ 0.075-0.125 events/day. The `tail_length` distribution is right-censored + heavy-tailed (piling at 180-min cap) so the actual flag rate at Z=2 on median+MAD-scaled anchor is expected to be higher than the normal-approximation 2.5%; anchor range widened accordingly to [0.05, 0.30]. If the actual mean is outside [0.01, 0.60] (a factor-of-2 deviation), HALT the test per §10.4 sanity-check rule.

- **Per-day `bout_n_did_not_return_2sd_day` median**: expected in **[0, 1]** events (many days will have 0 flagged bouts by construction). If the actual median exceeds 2, HALT (the operand is firing too often to be tail-rare — reference-window calibration concern per parent MD §3.2.2 alternatives-considered).

- **Heavy-T arm mean − non-heavy-T arm mean** (descriptive directional anchor): expected **> 0** under SUPPORTED. Anchor against HA-C4c §7 pattern; the personal-baseline compression is expected to bring the absolute difference DOWN relative to HA-C4c's operand (SD-scaling compresses discrimination), so an absolute-value comparison to HA-C4c's Δ mean is NOT the right frame — the Cliff's δ effect-size scale is the comparable dimension.

- **Cliff's delta under SUPPORTED**: expected in **[+0.20, +0.35]**. Anchor: HA-C4c's landed δ = +0.1523 on the fixed-absolute-threshold operand; the operand-family compression argument predicts Cliff's δ on the personal-baseline-rolling operand to be COMPARABLE or SLIGHTLY LOWER (personal-baseline z-scoring against a rolling reference typically reduces cross-day effect sizes relative to fixed-threshold operands per CONVENTIONS §3.1 personal-baseline discipline observations across the corpus). **At-risk for the +0.20 bar** given HA-C4c missed +0.20 by −0.05; HA-C4cp anticipated to be in similar territory. The +0.20 bar is retained per user Q "δ ≥ +0.20 primary" 2026-07-09 despite this at-risk anchor — the sister-pattern discipline wins over compression-of-effects per Authorship "Locked decisions" item 4 rationale.

- **Block-permutation p-value under SUPPORTED**: expected **< 0.05** at cross-phase-pooled stratum (n ~ 287 heavy-T / ~519 non-heavy-T; comparable to HA-C4c's landed n = 1274 minus the reference-window trim). HA-C4c's landed p = 0.0091 well below 0.05; HA-C4cp anticipated to have adequate power at the SUPPORTED direction if the operand-family compression preserves the discrimination signal.

## 8. Caveats result.md must explicitly acknowledge

1. **Personal-baseline reference-window carries a subject-relative interpretation**: the SD-anchored operand does NOT test "how long is the bout return-time in absolute minutes" but "how much longer than the subject's own recent typical return-time is this bout". A REJECTED verdict on HA-C4cp with HA-C4c at PARTIAL reads as "the signal is anchored to the fixed-absolute-threshold reference frame only, not to atypicality against subject's own distribution". A SUPPORTED verdict reads as "the signal generalises across both operand families". Neither reading claims a substantive Wiggers-C4 disproof or confirmation beyond the operand-specific scope.

2. **HA-C4c PARTIAL calibration discount** (analog to HA-C4c's §8 caveat 2 HA11-bout-redo discount): HA-C4c's landed δ = +0.1523 misses the +0.20 bar by −0.05. HA-C4cp's operand-family compression argument (see §7) predicts a plausibly-similar or lower δ. The PARTIAL band is anticipated as the modal outcome; a SUPPORTED verdict would require the personal-baseline operationalisation to produce a strictly LARGER δ than the fixed-absolute-threshold operationalisation, which is not the modal expectation from CONVENTIONS §3.1 personal-baseline discipline patterns on this corpus.

3. **Approach A inheritance-by-analogue caveat** (inherits from HA-C4c §8 caveat 3 verbatim + amplified per §4.9 last paragraph): the `bout_n_fast_recovery_day` β = −0.056/mg [95% CI −0.145, +0.034] p=0.223 template is NULL/weakly-consistent per recalibration's underpowered-NULL framing; the sign-flip is a fiat directional prior; the analogue substitution uncertainty is amplified for HA-C4cp because the SD-anchored operand family is FURTHER removed from the analogue's operand family than HA-C4c's fixed-absolute-threshold operand. The dose-adjusted sensitivity arm at §4.9 is descriptive companion only; the primary verdict is dose-naive within the underpowered-NULL frame.

4. **Motion-confound corpus property** (inherits from HA-C4c §8 caveat 4): 99.3% motion-confound at bout level per HA11-bout-redo result §4. HA-C4cp's motion-clean-only sensitivity arm anticipated INCONCLUSIVE. Wiggers-C4 "stress doesn't decrease, despite resting" verbatim implies a rest-conditional read; the corpus does not admit a clean rest-conditional operand at bout level; the SD-anchored family does not resolve this caveat — it changes the reference frame for "atypical" but does not filter for motion-clean state.

5. **Transient-fragility inheritance** (inherits from HA-C4c §8 caveat 5): HA11-bout-redo transient-excluded discrimination dropped from +20.26pp to +11.69pp. HA-C4cp likely to see analogous attenuation on `bout_n_did_not_return_2sd_day` under transient exclusion; reported at §4.10 as transient-excluded sensitivity arm.

6. **Reference-window construction dependency** (HA-C4cp-specific): the Z=1 and z_max sensitivity arms share the parent MD §3.2.2 reference-window construction with the primary. If the reference-window calibration itself is off (e.g. `subject_lagged_median` systematically biased on the 180-cap-censored `tail_length` distribution), all three cells inherit the bias. The reference-window-shorter-lag sensitivity arm and reference-pool-`did_not_return`-excluded sensitivity arm at §4.10 are the reference-window-fragility diagnostic companions. The primary verdict is robust to this caveat via the CONVENTIONS §3.1 robust-baseline discipline (median + MAD rather than mean + SD).

7. **Cross-op independence at operand-family level, NOT raw-substrate level** (per OI-025 protocol §5.4 four-condition independence argument, inherited via parent MD §3.2.2): HA-C4c and HA-C4cp both derive from the same Firstbeat-per-minute stress signal via the same bout-detection pipeline. The independence claim binds at the operand-family level (fixed-absolute-threshold vs personal-baseline-rolling). A shared-substrate correlated failure mode (e.g. Firstbeat-input noise at minute resolution per parent MD §2.4) would affect both HAs; the guide r3 §4.2 two-independent-HAs bar closure at cluster C-bout-substance is at the operand-family level.

8. **Reference-window left-edge trim**: the `[d-90, d-30]` window trims ~60-90 days from the leftmost `has_garmin_uds=True` coverage; the primary stratum's `>= 2022-11-17` left edge is more restrictive, so this trim does not become binding at primary, but the sensitivity-arm unmedicated-only stratum inherits the same trim and may lose ~30 days of unmedicated coverage. Reported at result.md per named-counts triplet discipline.

## 9. What we do with each outcome

Verdict → downstream cascade actions (Stage D → I → S₁ → S₂ → A → T cascade if the outcome aspires to actionability):

**9.1 SUPPORTED (both bars cleared on primary cell, direction correct)**

- Stage D descriptive audit companion at `analyses/descriptive/HA-C4cp/descriptive_audit.md` LOCKS with SUPPORTED reference table.
- Stage I interpretation at `analyses/interpretation/HA-C4cp.md` locks; substantive interpretive claim: "the Wiggers-C4 pattern of atypical-for-subject return-times fires directionally + at effect-size threshold on the personal-baseline-rolling operand family, corroborating the fixed-absolute-threshold arm at cross-op-independent operationalisation".
- Stage S₁ [cluster-C-bout-substance.md](../../synthesis/cluster-C-bout-substance.md) LOCK re-consumes; cluster moves from single-member (HA-C4c) to 2-member (HA-C4c + HA-C4cp); joint verdict CONCORDANT (both direction-correct; both cleared at least one bar; the SUPPORTED-on-HA-C4cp × PARTIAL-on-HA-C4c reading is joint-CONCORDANT-with-strength-asymmetry per `internal_synthesis.md` §5).
- Stage S₂ [topic-within-day-recovery.md](../../contextualisation/topic-within-day-recovery.md) LOCK re-consumes; AGREES-on-direction-not-magnitude → AGREES-on-direction-with-strengthened-support.
- Stage A [construct-bout-recovery-signal.md](../../actionability/construct-bout-recovery-signal.md) LOCK re-consumes; §5.2 evidence-layer paragraph updates from "PARTIALLY REACHED (cross-op-independence gap named)" to "REACHED (cross-op-independence gap closed at strict guide §4.2 two-independent-HAs bar)"; §5.6 row-6 OI-033 pointer marks CLOSED-BY-EXECUTION-SUPPORTED; tier-2 licensing standing may promote to tier-3 aspiration if PPV-with-base-rate arithmetic aligns.
- Stage T patient-audience and research-audience translation tracks dispatch per Stage A LOCK; cascade-source bounded qualifier per guide #4 r4 §5.6 mirror-application may or may not carry through in the same form.
- OI-033 CLOSED-BY-EXECUTION-SUPPORTED; register-row Tier 1 C4 entry adds HA-C4cp SUPPORTED alongside HA-C4c PARTIAL as sister-test.
- HA-C4c-v3 NOT triggered (HA-C4c stands as-locked; the sister-pattern is intact per guide r3 §4.2.1 canonical model discipline).

**9.2 PARTIAL (direction-correct; exactly one bar clears; §8 caveats interpret the failed bar)**

- Stage D + Stage I + Stage S₁ LOCK with PARTIAL routing; cluster-C-bout-substance joint verdict likely CONCORDANT-BELOW-THRESHOLD (both direction-correct; both PARTIAL) per internal_synthesis.md §5 verdict table.
- Stage A tier-2 licensing stands; §5.2 evidence-layer paragraph updates to "PARTIALLY REACHED (cross-op-independence gap CLOSED at direction-consistent-below-threshold reading; strict-magnitude-bar not cleared at either operationalisation)"; §5.6 row-6 OI-033 pointer marks CLOSED-BY-EXECUTION-PARTIAL. Tier-3 aspiration NOT triggered.
- OI-033 CLOSED-BY-EXECUTION-PARTIAL; register-row updates parallel to §9.1.
- Substantive interpretive note: HA-C4c PARTIAL + HA-C4cp PARTIAL joint reading is a **corpus-effect-size ceiling finding** — the substantive Wiggers-C4 signal fires directionally on this corpus at bout-level across both operand families, but the corpus's effect-size at bout-level is bounded below the +0.20 SUPPORTED threshold. This is an honest sample-limitation reading, not a Wiggers-C4 disproof.
- HA-C4c-v3 NOT triggered; HA-C4cp-v2 NOT triggered.

**9.3 REJECTED (direction-wrong OR both bars fail OR crash-drop sign-flip)**

- Stage D + Stage I LOCK with REJECTED routing; Stage S₁ cluster-C-bout-substance joint verdict may be ORTHOGONAL (direction-wrong on HA-C4cp with HA-C4c direction-correct) or CONFLICT (both direction-wrong, unlikely per §7 priors).
- Stage A: cross-op-independence gap CLOSURE reading depends on joint verdict shape; ORTHOGONAL is a form of closure (the operand families genuinely test different things), CONFLICT would trigger §6.1 tier downgrade review.
- §5.2 evidence-layer paragraph updates to "REACHED (cross-op-independence gap closed via ORTHOGONAL reading)" or "GAP CLOSED WITH DOWNGRADE (CONFLICT reading; tier-2 → tier-1 review triggered)" per §6.1 conflict rule.
- OI-033 CLOSED-BY-EXECUTION-REJECTED; register-row updates parallel to §9.1 but marks HA-C4cp REJECTED as sister-test outcome. Historical HA-C4c PARTIAL stands.
- Substantive interpretive note: HA-C4c PARTIAL + HA-C4cp REJECTED joint reading is an **operand-family-specific finding** — the signal is anchored to the fixed-absolute-threshold reference frame; the personal-baseline-rolling operationalisation does not fire. This is a substantive cross-operationalisation-independence-diagnostic outcome; the two operationalisations genuinely test different aspects of the Wiggers-C4 claim.
- HA-C4cp-v2 may be drafted with a different reference-window or Z-threshold per §9.5 escalation table if the user judges that the operand-family calibration is off. Reference-window-shorter-lag sensitivity arm result informs whether the `[d-90, d-30]` was the binding calibration choice.

**9.4 INCONCLUSIVE (walk-forward gate not met OR sanity-check HALT)**

- Stage D locks with INCONCLUSIVE routing; Stage I NOT dispatched at INCONCLUSIVE (nothing to interpret).
- Stage S₁ cluster-C-bout-substance NOT re-consumed at INCONCLUSIVE (no new substantive HA added to cluster); cluster stands single-member (HA-C4c only).
- OI-033 status transition: CLOSED-INCONCLUSIVE-WALK-FORWARD-GATE-NOT-MET or CLOSED-INCONCLUSIVE-SANITY-HALT depending on which gate fired.
- HA-C4cp-v2 dispatched at user tempo if reference-window recalibration is possible per §9.5.
- Stage A §5.6 row-6 OI-033 pointer marks CLOSED-INCONCLUSIVE; guide r3 §4.2.1 first-ever-operational-instance-discipline reading needs re-examination — if HA-C4cp-v2 is a plausible route, gap stays future-closeable-via-new-OI; else gap-closeability requires yet another OI.

**9.5 HA-C4cp-v2 escalation table** (triggered under §9.3 REJECTED or §9.4 INCONCLUSIVE with reasonable expectation of recalibration):

| Primary failure | v2 route |
|---|---|
| Reference-window `[d-90, d-30]` too many left-edge trims | v2 primary `[d-60, d-30]` (currently HA-C4cp sensitivity arm; promotable to primary) |
| Z=2 too stringent → per-day count near-zero → INCONCLUSIVE | v2 primary at Z=1 (currently HA-C4cp sensitivity arm; promotable to primary) |
| Signal on `bout_return_time_z_max_day` continuous but not on Z=2 count → HA-C4cp REJECTED | v2 primary `bout_return_time_z_max_day` continuous (Mann-Whitney U on continuous outcome) |
| Reference pool `did_not_return_flag`-inclusion biases the calibration | v2 primary with reference pool `did_not_return_flag`-excluded (currently sensitivity arm) |

Any v2 route drafts a fresh pre-reg per hypothesis_lock_process §3.2; HA-C4cp r1 archived per lock-process discipline.

**9.6 Framework-validity inheritance from parent MD §6**

Regardless of HA-C4cp verdict shape, the parent MD §6 framework-validity gate (HA11 v1 reproduction on `bout_n_fast_recovery_day` on the calm-day pool) stands UNCHANGED. HA-C4cp inherits the gate's clearance status from HA-C4c §9.6 pattern; HA11-bout-redo PARTIAL verdict per [HA11-bout-redo result.md](../HA11-bout-redo/result.md) is the framework-validity reading for HA-C4cp regardless of HA-C4cp's own primary verdict. Per parent MD §3.2.2 explicit statement, the SD-anchored family does NOT modify the primary operand set used by the §6 gate.

## 10. Detection script architecture

Locked pre-commit at drafting time (per [`hypothesis_lock_process.md` §3.2 step 5](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)):

- **Test script**: `docs/research/analyses/hypotheses/HA-C4cp/test.py` (mirrors HA-C4c/test.py structure).
- **Extraction**: reads `bout_n_did_not_return_2sd_day` (and Z=1, z_max, reference-window audit traces) from `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`; joins `exertion_class_lagged_lcera`, `is_crash`, `citalopram_phase`, `has_garmin_uds`, and other §4.4 gate columns.
- **Structural walls** (mirroring HA-C4c-stringency-companion §2.4 four-wall discipline):
  1. Primary operand fixed at `bout_n_did_not_return_2sd_day`; no test-time swap.
  2. Stratum fixed at cross-phase-pooled per §4.2; no test-time swap.
  3. Effect-size bar fixed at +0.20 per §5.1; no test-time relaxation.
  4. Block-permutation E[L]=7, B=10,000, seed=20260709; deterministic reproducibility.
- **Output**: `result-data.json` (headline verdict + primary cell numeric outputs + per-sensitivity-arm outputs + per-arm n counts + reference-window audit traces + Holm step-down results); `result.md` (narrative headline verdict + §8 caveats + downstream cascade routing per §9).
- **Sanity gate 10.4** (dry-run-before-lock discipline per parent MD §5.4): per §7 sanity-check ranges; if per-day `bout_n_did_not_return_2sd_day` mean outside [0.01, 0.60] or median > 2, HALT the primary run and route to §5.4 INCONCLUSIVE per §9.4 pattern.

**Idempotency**: re-running `test.py` with same inputs and same seed produces byte-identical `result-data.json` output. Verified at dry-run per parent MD §5.4 discipline.

**Dry-run report**: `dry-run-report.md` at HA-C4cp folder produced after test.py runs; reports the §7 sanity-check outcomes + walk-forward gate outcomes + operand distribution histograms + reference-window audit trace summaries. Sanity-check-failure at dry-run routes to INCONCLUSIVE per §9.4 pattern.

---

## Cross-references

- **Parent methodology MD**: [`bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md) §3.2.2 (SD-anchored derivative operand family; co-locked with this pre-reg at Bundle H+ event 7 r3).
- **Sister pre-reg (fixed-absolute-threshold arm)**: [HA-C4c](../HA-C4c/hypothesis.md) r2 LOCKED 2026-07-08.
- **OI-025 protocol**: [HA-C4c-stringency-companion protocol §5.3 + §5.4 + §5.5](../HA-C4c-stringency-companion/protocol.md) — source of the pre-committed operand family + cross-op-independence argument + closure-path framing.
- **Framework-validity gate**: [HA11-bout-redo](../HA11-bout-redo/hypothesis.md) + [result.md](../HA11-bout-redo/result.md) — the calm-day pool reproduction gate on `bout_n_fast_recovery_day`; HA-C4cp inherits per §9.6.
- **Stage A construct**: [construct-bout-recovery-signal.md](../../actionability/construct-bout-recovery-signal.md) LOCKED r2 2026-07-09 §5.6 row-6 OI-033 pointer.
- **OI entry**: [`_open_inputs.md`](../../../methodology/_open_inputs.md) OI-033 (surfaced 2026-07-09; transitions to PROTOCOL-LOCKED at this pre-reg's r2 LOCK).
- **Register row**: [`wiggers_testable_hypotheses.md`](../../../wiggers_testable_hypotheses.md) Tier 1 C4 row — updated at r2 LOCK-commit to add HA-C4cp sister-test pointer alongside HA-C4c primary anchor.
- **HA-C3p sister-pre-reg precedent**: [HA-C3p](../HA-C3p/hypothesis.md) — the canonical HA-C3 → HA-C3p personal-baseline sister-pattern the guide r3 §4.2.1 condition 2 explicitly cites.
- **HA-C4c-stringency-companion Pass 1 outcome**: [descriptive_audit.md](../../descriptive/HA-C4c-stringency-companion/descriptive_audit.md) LOCKED r1 2026-07-09 §5.1 Step-2-decision block — NON-TRIGGER outcome corroborating stringent-operand-threshold interpretation as CAVEAT-CLASS per CONVENTIONS §4.2.
- **Downstream cluster + topic + construct + translation cascades**: per §9 above; drift-triggered on result.md LOCK.

---

*Producer-mode pre-reg draft. Awaits fresh-session `/research-review` dispatch (background subagent per user Q "Dispatch both reviews as background subagents this session" 2026-07-09). Reviewer verdict absorbed at r2 LOCK.*
