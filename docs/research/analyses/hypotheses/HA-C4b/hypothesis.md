# HA-C4b v3 — Stress-with-low-motion minute count as crash precursor (Wiggers C4 + motion filter), unmedicated pooled headline; §4.3 1b.ii dropped + pacing-behaviour confounder caveat

## Authorship

**Drafted 2026-06-16** by Claude (Opus 4.7) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. **§3.3 same-session operationalisation refinement** of v2 (NOT a §3.2 fresh-session redraft); explicit user authorization 2026-06-16 to draft v3 in the test-execution session that ran v2 to INCONCLUSIVE. The data exposure context is: the v3 drafting context has seen v2's full result.md including per-episode z-scores on the unmedicated train arm (notably 2023-02-04 at `max_signed_z = +3.73` on d-1), the E[L]* = 3.30 finding, and the train/validate directional inconsistency (train 42.9% / validate 0%). Per [`hypothesis_lock_process.md` §3.3](../../../methodology/hypothesis_lock_process.md#33-optional-post-draft-revision-r1-data-exploration-absorption) that level of data exposure permits operationalisation refinements but NOT headline-cell relocks. **v3 makes no headline-cell change** (the locked cell is byte-identical with v2 §5.0).

**v3 trigger**: v2's test session 2026-06-16 (commit `83a64b2`) landed INCONCLUSIVE because the §10.2 dry-run sanity-gate (1b.i only) passed at pooled n = 10 but the full run applied §4.3 1b.ii (wake-window quartile-coverage gate) and dropped one train episode (`2023-02-04`), taking the pooled cell to n = 9 < §5.3 bar. The dropped episode is the train arm's highest-signal episode (its 4-day lead-up included `max_signed_z = +3.73`). v2's spec-design observation in [`result.md`](result.md) "Critical methodological finding" surfaced the §10.2-gate / full-run-gate asymmetry as the v3 trigger.

v2 archived at [`hypothesis-v2-archived.md`](hypothesis-v2-archived.md) (locked at commit `2417043` 2026-06-16, test-executed at commit `83a64b2` 2026-06-16, INCONCLUSIVE verdict at [`result.md`](result.md)). v1 stays archived at [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md). v3 cites both as audit-able predecessors.

**v3 deltas from v2** (localised; v3 inherits everything else wholesale):

- **§4.3 day-validity gate 1b.ii (wake-window quartile coverage) DROPPED.** v3 retains §4.3 (1) the primitive stress-sample gate ≥ 600 (the HA11-family valid flag) and (1b.i) the strict in-range-samples-per-day gate ≥ 900. v3 drops 1b.ii entirely. Rationale: (i) the [`stress_low_motion_primitive.md` §5 NaN-policy](../../../methodology/stress_low_motion_primitive.md#5-nan-policy--day-validity-gate) only requires the 600-sample gate; v2's 1b.i + 1b.ii are HA-C4b-specific strengthenings that the primitive itself does not mandate. (ii) v2's §10.2 dry-run sanity-gate ran 1b.i-only (because the 1b.ii quartile-coverage cache takes 5-15 min to build from FIT files); the full run then applied 1b.ii and dropped one train episode below the §5.3 bar. This dry-run / full-run asymmetry is a spec-design flaw, not a data finding. v3 closes the flaw by removing the gate that caused the asymmetry. (iii) 1b.ii was originally inherited from v1's r1 post-viz revision to address a Family A 2024-11-26 visualization-driven concern about partial-day coverage; that concern's binding case is in the consolidation phase, NOT the unmedicated headline phase. v3's unmedicated-headline cell is not exposed to the case 1b.ii was designed to catch.
- **§10.2 spec-sanity-gate symmetrised.** v3 §10.2 now applies identical §4.3 (gates 1 + 1b.i, no 1b.ii) at both dry-run and full-run. The n that passes the dry-run gate is the n the full run will evaluate. No further §4.3 exclusion happens between the two regimes.
- **§4.11.5 LOO and §5 falsification bar UNCHANGED** byte-identical with v2. The headline cell remains `unmedicated × train+validate pooled × S60_Mlow × N_std=1.5 × primary 4d × one-sided elevated`; the §5.1 (a)+(b)+(c) bar applies; the n ≥ 10 §5.3 inconclusive bar applies; the §4.11.5 LOO check applies.
- **§7 sanity ranges UNCHANGED.** v3 inherits v2 §7's raw per-phase card medians (76 / 35 / 38 / 63) with ±20% tolerance + the [25, 55] unmedicated σ range. The §10.2 gate evaluates against these ranges as in v2.
- **§8 new caveat — pacing-behaviour confounder.** The §4.2 `exertion_class_lagged_lcera` column captures *physical* exertion (Garmin-derived). It does NOT capture *cognitive* exertion (concentration, reading, fast conversation) or *emotional* exertion (grief, relational-stress, conflict, high-stakes meetings). Per [`literature/pacing-and-crash-mitigation.md` §1](../../../literature/pacing-and-crash-mitigation.md): "All exertion counts, not just physical. Cognitive load... emotional stress, and orthostatic load (being upright) all draw on the same envelope and can each trigger PEM. The brain uses ~20% of the body's energy; cognitive overexertion can crash someone as hard as a walk. This is the single most under-appreciated point and the one a step-counter misses entirely." For HA-C4b, this means: (a) some unmedicated-phase crashes may have been *emotionally triggered* without a matching heavy physical exertion in the lead-up window, in which case §4.2 exertion-conditioning **excludes them from the eligible-crash pool entirely**; (b) some unmedicated-phase crashes that ARE eligible may have an emotional component that is the actual proximate trigger, with the physical-exertion conditioning being incidental. The pacing-behaviour temporal context further sharpens this: (i) pre-ergotherapy era — physical/cognitive pacing was poor or absent; crashes are easier to attribute to overdoing; (ii) post-ergotherapy era — physical/cognitive pacing improved substantially; physically-attributable crashes should decrease in this era; (iii) emotional-exertion-rich periods — high-emotional-load events (e.g. rouwschop sessions, the day of office computer handover, PWC reintegration trajectory conversations, tweede-spoor conversations) impose load the participant cannot pace via Garmin-visible signals; crashes following these events look indistinguishable in `stress_low_motion_min_count_S60_Mlow` from physically-attributable crashes when the body actually was at rest. The result.md must surface this caveat with the locked verdict and (where the user supplies approximate dates) annotate the surviving episodes with pacing-era + emotional-event-proximity descriptive flags for the human reader. v3 does NOT add a quantitative emotional-exertion proxy; that is a queued primitive (see [Pending follow-ups](#pending-follow-ups-queued-per-35-propagation-discipline)).
- **§9 outcome interpretation augmented** with the pacing-behaviour-confounder reading for each verdict branch (per the [§3.7 reporting-layer heuristic](../../../methodology/hypothesis_lock_process.md#37-optional-r3-interpretability-augmentation) — no new conjuncts, no SUPPORTED-bar promotion; restated interpretation only).

**v3 inherits the following sections from v2 verbatim** (cited but not restated below; read v2-archived for the locked content):
- §2 Why we think this — Wiggers C4 framing + unmedicated phase rationale + sibling SUPPORTED-precursor evidence + Session E construct validity. The mechanistic case for the unmedicated phase as the test ground is unchanged.
- §4.1 Predictor primitive (`stress_low_motion_min_count_S60_Mlow`).
- §4.2 Exertion-conditioning rule.
- §4.3 Day validity — **gates 1 + 1b.i ONLY** (gate 1b.ii dropped in v3 per the delta above).
- §4.4 Citalopram phase-stratified treatment, including the v2 headline-verdict sentence (unmedicated pooled headline).
- §4.5 Lagged personal baseline.
- §4.6 Per-day z-score.
- §4.7 Per-episode lead-up profile.
- §4.8 Threshold N_std tiers.
- §4.9 Null sample — stationary bootstrap with E[L] = 7, B = 10,000.
- §4.10 Sensitivity ladder (6 unique columns + 3 duplicates).
- §4.11 Secondary descriptive outcomes (same-day Spearman with crash-drop sensitivity, construct-disambiguation 2×2, respiration-companion sensitivity, v2-specific pooled-unmedicated exertion-conditioned Spearman).
- §4.11.5 Episode-level leave-one-out fragility check.
- §5 Pre-registered falsification criterion (including §5.0 single-cell lock, §5.1 (a)+(b)+(c) bar, §5.2 diagnostic arms, §5.3 inconclusive bar at n ≥ 10).
- §6 Exclusion rules.
- §7 Expected effect size / sanity ranges.

### Pending follow-ups (queued per §3.5 propagation discipline)

- **Emotional-exertion proxy primitive**. The pacing-behaviour confounder is currently qualitative-only. A future methodology MD could spin off a per-day emotional-exertion proxy from the gevoelscore notes/tags corpus (text-based signals for grief / conflict / meeting-density / etc.) and a downstream test could layer the proxy into §4.2 as an additional conditioning variable. Out of scope for v3. Queue rationale: building a defensible emotional-exertion proxy requires its own methodology MD + four-input reasoning + measurement validation; the existing exertion-conditioning column is physical-only by construction. Adding it to v3 would be a §3.7 approach change (new conditioning variable), requiring a new audit gate.
- **External viz-notes citations in §4.3 (Family A 2024-11-26 case) and §4.11 (Family D2a ρ = 0.79, Family D2b)**. Carried from v2. Out of scope for v3 same-session refinement; v4 or a parallel documentation commit consolidates into `analyses/garmin_exploration/stress_low_motion_viz/key-findings.md`.

**Status: DRAFTED 2026-06-16 by Claude (Opus 4.7) in reviewer-mode-with-authorization. NOT YET LOCKED.** Per [`hypothesis_lock_process.md` §3.4](../../../methodology/hypothesis_lock_process.md#34-audit-step-step-2-of-the-arc) the next step is a **fresh-session `/research-review` audit** against this v3 draft. Lock signal awaits user acceptance after the audit completes. The four [§3.8 lock-blocking gates](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc) are pre-stated for the auditor:

1. **Power-calc dispatch present in §8** — inherited from v2 (Daza 2018 within-subject design citation; block-permutation null at E[L]=7 named as the within-subject inferential machinery).
2. **Single-cell headline lock** — §5.0 inherited verbatim from v2 (`unmedicated × train+validate pooled × S60_Mlow × N_std=1.5 × primary 4d × one-sided elevated`).
3. **Register-row pointer** — [`wiggers_testable_hypotheses.md` C4b row](../../../wiggers_testable_hypotheses.md) was updated at v2 lock to point at this folder; v2 → v3 succession is a same-folder refinement and does NOT require a new register-row pointer (the register row points at the folder, not at a specific revision). Non-supersession confirmation: the C4b register row remains generic at the headline-cell level; v3 inherits the v2 headline cell unchanged; no register update needed at v3 lock.
4. **Re-audit completed clean** — pending. The fresh-session `/research-review` (§3.4) is the canonical audit step for v3. Compression of the re-audit (§3.6) is NOT acceptable for v3 because the v2 → v3 transition involves a §10.2 sanity-gate revision (operationalisation refinement, but with implications for run-protocol symmetry); a fresh-session reviewer should verify the §10.2 revision closes the asymmetry without introducing a new one.

Further modifications create HA-C4b-v4 with v3 archived per the locked-pre-reg discipline. The next session (after lock) writes the v3 `test.py` + runs + emits the v3 `result.md` per §10. **The v3 test-execution session must be a fresh session** because this drafting session is itself the v2 test-execution session (already contaminated with v2's per-episode z-scores on the unmedicated headline phase). The handoff brief for the v3 test session is at [`.claude/plans/session-c4b-v3-test-handoff-2026-06-16.md`](../../../../../../.claude/plans/session-c4b-v3-test-handoff-2026-06-16.md) (drafted alongside this v3 spec).

---

**Pre-registration drafted 2026-06-16, BEFORE any v3 test run.** v2's result.md (which this drafting session has read end-to-end) informs §4.3 1b.ii drop justification + §8 caveat additions but does NOT inform any §5 falsification-bar parameter or the §5.0 headline cell. Locked at user acceptance after the §3.4 fresh-session audit. Any subsequent change creates HA-C4b-v4.

HA-C4b tests Wiggers' "stuck sympathetic / walls of orange" pattern refined with the participant's lived **motion filter**: elevated Garmin stress *while concurrent body motion is low*. v3 is a §3.3 operationalisation refinement of v2 that closes the §10.2 dry-run / full-run gate-asymmetry (drops §4.3 1b.ii) and surfaces the pacing-behaviour confounder explicitly in §8 + §9 (qualitative only; no new conjunct).

## 1. Claim

Inherited from [v2 §1](hypothesis-v2-archived.md#1-claim) verbatim. v3 headline cell remains: **unmedicated phase × train + validate pooled × `stress_low_motion_min_count_S60_Mlow` × N_std=1.5 × primary 4-day lead-up × one-sided elevated direction.**

## 2. Why we think this

Inherited from [v2 §2](hypothesis-v2-archived.md#2-why-we-think-this) wholesale.

## 3. Data sources

Inherited from [v2 §3](hypothesis-v2-archived.md#3-data-sources) verbatim. v2's labels-CSV-path correction stands; v2's per-phase descriptive-card anchor stands.

## 4. Measurement protocol

### 4.1 Predictor primitive (locked, inherited verbatim from v2)

Inherited from [v2 §4.1](hypothesis-v2-archived.md#41-predictor-primitive--stress_low_motion_min_count_s60_mlow-locked-inherited-from-v1-r3) verbatim.

### 4.2 Exertion-conditioning rule (locked, inherited verbatim from v2)

Inherited from [v2 §4.2](hypothesis-v2-archived.md#42-exertion-conditioning-rule-locked-inherited-from-v1-r3) verbatim. A day is C4b-eligible if `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on `d` OR `d − 1` (union).

**v3 caveat surfacing** (the rule is unchanged; the caveat at §8 is new): `exertion_class_lagged_lcera` is built from Garmin-derived physical exertion only. Crashes with primarily emotional or cognitive triggers may either fail this gate (and drop out of the eligible-crash pool) or pass it incidentally (because the participant happened to also do physical exertion in the lead-up). v3 does not change the gate; v3 names the confounder explicitly in §8 + §9.

### 4.3 Day validity (REVISED in v3 — gate 1b.ii DROPPED)

Inherits from [v2 §4.3](hypothesis-v2-archived.md#43-day-validity-locked-inherited-from-v1-r3-post-viz) with the following revision:

**v3 gates retained**:
1. **Gate 1**: primitive stress-sample gate ≥ 600 samples (the HA11-family `valid` flag).
2. **Gate 1b.i**: total in-range samples per day ≥ 900 (the HA-C4b-specific strengthening introduced in v1 r1).
3. **Gate 2**: §4.2 exertion-conditioning satisfied (on `d` OR `d − 1`).
4. **Gate 3**: day has a `crash_v2` label (for inclusion as a crash episode).

**v3 gate DROPPED**:
- **Gate 1b.ii (wake-window quartile coverage)**: removed. v2's 1b.ii required ≥ 50 in-range stress samples in each of 4 wake-window quartiles (sleep-window-aware or fixed-time fallback). v3 drops this gate entirely.

**v3 rationale for dropping 1b.ii** (audit-able):

1. **The primitive itself does not require 1b.ii.** Per [`stress_low_motion_primitive.md` §5 NaN policy + day-validity gate](../../../methodology/stress_low_motion_primitive.md#5-nan-policy--day-validity-gate): "Day-validity gate: ≥ 600 in-range stress samples." 1b.ii was an HA-C4b-specific strengthening, not a primitive-level requirement.

2. **v2's §10.2 dry-run gate / full-run gate asymmetry caused the v2 INCONCLUSIVE verdict.** The dry-run skipped 1b.ii for speed (the quartile-coverage cache takes 5-15 min to build from FIT files); the full run applied 1b.ii. Pooled-unmedicated n went from 10 (dry-run, 1b.i only) to 9 (full run, 1b.i + 1b.ii) — below the §5.3 bar. This asymmetry is a spec-design flaw, not a data finding. v3 closes the flaw by removing 1b.ii.

3. **1b.ii was originally introduced by v1 r1 to address a visualisation-driven concern in the consolidation phase, NOT the unmedicated phase.** v1 r1's post-viz revision strengthened §4.3 because the stress_low_motion_viz session showed a Family A 2024-11-26 case (consolidation phase) where partial-day coverage produced misleading per-day predictor values. The unmedicated phase has substantially denser FIT coverage than consolidation (participant was wearing the watch more continuously pre-citalopram; the consolidation-era partial-coverage pattern is largely absent in unmedicated). The 1b.ii gate's binding case does not exist in v3's headline phase.

4. **Symmetry of dry-run + full-run gating is required for the §10.2 sanity-gate to do its work.** v3's §10.2 evaluates n ≥ 10 against the same §4.3 (gates 1 + 1b.i) at both dry-run and full-run; the n that passes the dry-run gate IS the n the full-run evaluates. No further §4.3 exclusion between the two regimes.

**v3 1b.i strict gate retained as the day-validity bar.** Gate 1b.i (≥ 900 samples) is more permissive than 1b.ii (which required 4 × ≥ 50 = ≥ 200 minimum, distributed across all wake quartiles) but stricter than gate 1 alone (≥ 600). The 1b.i level is sufficient to filter genuinely under-sampled days without imposing the quartile-distribution requirement that creates the asymmetry. v3 retains 1b.i unchanged from v2.

### 4.4 Citalopram phase-stratified treatment (locked, inherited verbatim from v2)

Inherited from [v2 §4.4](hypothesis-v2-archived.md#44-citalopram-phase-stratified-treatment-per-5b-framework-locked--v2-headline-verdict-sentence-update) verbatim.

### 4.5 Lagged personal baseline (locked, inherited verbatim from v2)

Inherited from [v2 §4.5](hypothesis-v2-archived.md#45-lagged-personal-baseline-per-conventions-32-locked-inherited-from-v1-r3) verbatim.

### 4.6 Per-day z-scored count (locked, inherited verbatim from v2)

Inherited from [v2 §4.6](hypothesis-v2-archived.md#46-per-day-z-scored-count-locked-inherited-from-v1-r3) verbatim.

### 4.7 Per-episode lead-up profile (locked, inherited verbatim from v2)

Inherited from [v2 §4.7](hypothesis-v2-archived.md#47-per-episode-lead-up-profile-locked-inherited-from-v1-r3) verbatim.

### 4.8 Threshold N_std (locked, inherited verbatim from v2)

Inherited from [v2 §4.8](hypothesis-v2-archived.md#48-threshold-n_std-locked-inherited-from-v1-r3) verbatim. Primary 1.5 / secondary 2.0 / sensitivity 2.5. Primary tier (N_std = 1.5) determines the v3 headline verdict.

### 4.9 Null sample — stationary bootstrap with E[L] = 7 (locked, inherited verbatim from v2)

Inherited from [v2 §4.9](hypothesis-v2-archived.md#49-null-sample--stationary-bootstrap-with-el--7-locked-inherited-from-v1-r3) verbatim.

**v3 E[L]\* observational note** (no spec change): v2's test run observed `E[L]* = 3.30` (vs default 7), tripping the factor-of-2 flag. Per the [methodology MD operational consequences](../../../methodology/permutation_null_block_length.md), the factor-of-2 flag means the result requires re-evaluation at E[L]* before locking the verdict. In v2 the verdict was INCONCLUSIVE (not eligible for SUPPORTED-bar promotion regardless of block length), so the E[L]* flag was descriptive context. In v3, the same factor-of-2 flag rule applies: if the v3 test run produces a SUPPORTED verdict and `E[L]* < 3.5` (factor-of-2 below the 7 default), a sensitivity re-run at the observed E[L]* must be performed before the verdict locks. The v3 spec does not pre-commit to which way to handle a SUPPORTED-at-default-but-not-at-E[L]* result; that is a §3.7 reporting-layer decision the result.md handles.

### 4.10 Sensitivity ladder report (locked, inherited verbatim from v2)

Inherited from [v2 §4.10](hypothesis-v2-archived.md#410-sensitivity-ladder-report-locked-inherited-from-v1-r3) verbatim.

### 4.11 Secondary descriptive outcomes (locked, inherited verbatim from v2)

Inherited from [v2 §4.11](hypothesis-v2-archived.md#411-secondary-descriptive-outcomes-locked-inherited-from-v1-r3) verbatim, including the v2-specific Spearman on the pooled-unmedicated heavy-exertion-conditioned subset.

#### 4.11.5 Episode-level leave-one-out (LOO) fragility check (locked, inherited verbatim from v2)

Inherited from [v2 §4.11.5](hypothesis-v2-archived.md#4115-episode-level-leave-one-out-loo-fragility-check-v2-specific-added-2026-06-15) verbatim, including the r2 boundary-fragility note.

## 5. Pre-registered falsification criterion

Inherited from [v2 §5](hypothesis-v2-archived.md#5-pre-registered-falsification-criterion) verbatim. §5.0 single-cell lock unchanged; §5.1 (a)+(b)+(c) bar unchanged; §5.2 diagnostic arms unchanged; §5.3 inconclusive bar at n ≥ 10 unchanged.

## 6. Exclusion rules (locked, inherited verbatim from v2)

Inherited from [v2 §6](hypothesis-v2-archived.md#6-exclusion-rules-locked-inherited-from-v1-r3) verbatim.

## 7. Expected effect size if hypothesis is true (locked, inherited verbatim from v2)

Inherited from [v2 §7](hypothesis-v2-archived.md#7-expected-effect-size-if-hypothesis-is-true-v2-re-anchored) verbatim. Per-phase raw-card medians: unmedicated 76 / buildup 35 / consolidation 38 / afbouw 63. Tolerance: ±20% for v3 §10.2 gate. Unmedicated lagged-baseline σ expected in [25, 55].

## 8. Caveats `result.md` must explicitly acknowledge

Inherited from [v2 §8](hypothesis-v2-archived.md#8-caveats-resultmd-must-explicitly-acknowledge) wholesale + the following v3-specific additions:

- **§4.3 1b.ii dropped in v3 — operationalisation refinement, not signal-fitting**. v2 applied §4.3 1b.ii (wake-window quartile-coverage gate) at the full run only, causing one train episode (`2023-02-04`, max_signed_z = +3.73 on d-1) to drop from the pooled-unmedicated headline cell, taking n from 10 to 9 → INCONCLUSIVE per §5.3. v3 drops 1b.ii based on the operational reasoning at §4.3 above (primitive doesn't require it; v1 r1 introduced it for a consolidation-phase concern that doesn't bind in unmedicated; the dry-run / full-run asymmetry it created is a spec-design flaw). The result.md must acknowledge that the v3 retains `2023-02-04` in the eligible pool because of the v3 1b.ii drop, and that this is a material discipline question: a strict reviewer might object that the drop was post-hoc "rescue" of a specific high-signal episode. v3's defence: the drop is justified by the spec-design asymmetry (a methodological flaw, not a data-driven choice) and by the primitive's own validity requirement (only 600-sample gate). The result.md should restate this defence prominently when reporting the v3 verdict.

- **v2 → v3 transition disclosure**. The v3 spec was drafted in the same Claude session that ran v2's test (and saw v2's per-episode z-scores including the dropped 2023-02-04 episode). Per [`hypothesis_lock_process.md` §3.3](../../../methodology/hypothesis_lock_process.md#33-optional-post-draft-revision-r1-data-exploration-absorption), this data-exposure context permits operationalisation refinements (which v3 is) but NOT headline-cell relocks (v3 makes no headline-cell change; the locked cell at §5.0 is byte-identical with v2). The Authorship block documents this explicitly. v3 was drafted to the §3.3 discipline; the §3.4 audit step is fresh-session and adjudicates whether the §3.3 refinement was defensible at this data-exposure level.

- **Pacing-behaviour confounder (qualitative-only at v3)**. The §4.2 exertion-conditioning column `exertion_class_lagged_lcera` captures **physical exertion only** (Garmin-derived from heart-rate / motion / training-load aggregates). It does NOT capture:
  - **Cognitive exertion** (concentration, reading, fast conversation, screen time, screen-content cognitive load). Per [`pacing-and-crash-mitigation.md` §1](../../../literature/pacing-and-crash-mitigation.md): "The brain uses ~20% of the body's energy; cognitive overexertion can crash someone as hard as a walk."
  - **Emotional exertion** (grief, relational stress, conflict, high-stakes meetings, exposure to triggering content). Per the same reference: "All exertion counts, not just physical." The energy envelope is shared.
  - **Orthostatic exertion** (being upright; orthostatic load draws on the same envelope).

  **Pacing-behaviour temporal context** (qualitative; dates approximate, to be supplied by user during v3 result.md review):
  - **Pre-ergotherapy era**: physical / cognitive pacing was poor or absent. Crashes in this era are more easily attributable to overdoing on the physical / cognitive side. Approximate timing: early in the LC journey, before the participant began structured ergotherapy.
  - **Post-ergotherapy era**: physical / cognitive pacing improved substantially. Crashes in this era should be less attributable to physically-paceable overdoing; emotionally / orthostatically driven crashes remain.
  - **Emotional-exertion-rich periods**: specific high-emotional-load events that the participant could not pace via Garmin-visible signals. Named events (approximate dates TBD): rouwschop sessions (grief-processing therapy), the day of office computer handover (terminating employment), PWC reintegration trajectory conversations, tweede-spoor conversations. Crashes following these events look indistinguishable in `stress_low_motion_min_count_S60_Mlow` from physically-attributable crashes when the body actually was at rest during the lead-up.

  **Two structural consequences for HA-C4b**:
  1. Some unmedicated-phase crashes may have been **emotionally / cognitively triggered without a matching heavy physical exertion in the lead-up window**, in which case §4.2 exertion-conditioning **excludes them from the eligible-crash pool entirely**. The HA-C4b test cannot speak to these crashes by construction. A NOT-SUPPORTED reading must therefore be interpreted as "HA-C4b's lived motion-filter refinement of Wiggers C4 is NOT a precursor for *the physically-exertion-conditioned subset of crashes*", not as a general claim about all crashes.
  2. Some eligible-pool crashes (those that DO pass §4.2 exertion-conditioning) may have an emotional component that is the *actual proximate trigger*, with the physical exertion being incidental rather than causal. For these crashes, the lead-up `stress_low_motion_min_count_S60_Mlow` may or may not show elevation; the signal depends on whether the emotional load also presented as Garmin-stress-while-at-rest in the days before the crash.

  **The result.md must surface this caveat with the verdict and (where the user supplies approximate dates) annotate the surviving episodes with pacing-era + emotional-event-proximity descriptive flags for the human reader.** The annotation is a §3.7 reporting-layer addition (descriptive only, no SUPPORTED-bar weight, no verdict modification); v3 does NOT include it as a falsification conjunct.

  **A quantitative emotional-exertion proxy is queued as a future primitive**, not in scope for v3. See [Pending follow-ups](#pending-follow-ups-queued-per-35-propagation-discipline) above.

## 9. What we do with each outcome

Inherited from [v2 §9](hypothesis-v2-archived.md#9-what-we-do-with-each-outcome) wholesale + the following v3-specific augmentation (per the [§3.7 reporting-layer heuristic](../../../methodology/hypothesis_lock_process.md#37-optional-r3-interpretability-augmentation) — no new conjuncts):

**Each verdict branch's interpretation restates the pacing-behaviour confounder per §8:**

- **Pooled-unmedicated SUPPORTED** (v3): the Wiggers C4 motion-filtered stress-elevated-minute count discriminates pre-crash from null windows on the unmedicated phase POOLED ARM, **under the v3 1b.ii-dropped day-validity discipline**, **for the §4.2 physically-exertion-conditioned subset of crashes only**. The verdict does NOT generalise to emotionally / cognitively triggered crashes (the §4.2 gate excluded them). v3 SUPPORTED reading: "for crashes the physical-exertion-conditioning admits to the test, the motion-filtered stress signal is a precursor in the unmedicated phase." Companion-read with pacing-era annotations: if v3 surviving episodes cluster in the pre-ergotherapy era (when physical pacing was poor), the SUPPORTED reading aligns with "poor physical pacing → physical exertion → motion-filtered stress lead-up → crash"; if they cluster in the post-ergotherapy era OR in emotional-exertion-rich periods, the SUPPORTED reading requires more careful interpretation — the physical-exertion-conditioning may be incidental and the actual trigger may be emotional / cognitive.

- **Pooled-unmedicated NOT-SUPPORTED** (v3): one or more of (a)(b)(c) fails on the v3 pooled cell. The locked-pre-reg reading: the motion-filter-refined Wiggers C4 stress signal does NOT carry crash-precursor weight on the unmedicated PHYSICALLY-EXERTION-CONDITIONED subset. **Recommended primary alternative reading** (from v2 §9, restated): the lived rest-stress trigger may be PROTECTIVE rather than PREDICTIVE — the participant acts on the trigger and prevents the crash. **v3 second alternative reading** (new per the pacing-behaviour confounder): the unmedicated-phase crashes the §4.2 gate admits to the test may be disproportionately *emotionally / cognitively triggered with incidental physical exertion in the lead-up*, in which case the lack of stress-low-motion signal is exactly what an emotional-trigger story predicts (the body wasn't in the "stuck sympathetic / walls of orange" state pre-crash; the emotional event simply ran the budget down). The result.md must hold both alternative readings open; neither is testable within v3.

- **Pooled-unmedicated INCONCLUSIVE** (v3): n drops below 10 at the final exclusion. v3 §10.2 makes the dry-run gate symmetric with the full-run gate (both apply 1b.i only); if INCONCLUSIVE fires in v3, the cause is a §4.5 baseline-availability exclusion (not the v2 1b.ii-vs-1b.i asymmetry). Per v3 §9 INCONCLUSIVE branch: halt + recommend v4 only if a recoverable operationalisation refinement exists; otherwise descriptive companions become the only output and the pacing-behaviour caveat is restated.

- **Construct-disambiguation differs from primary headline / Respiration-companion sensitivity differs / Sensitivity ladder shows non-monotonicity**: inherited from v2 §9.

- **Spec sanity-check fails on v3 dry-run** (unmedicated pooled n falls below 10 with the symmetric 1b.i-only gate; or per-phase median falls outside §7 ranges; or median σ outside [25, 55] for unmedicated): DO NOT run the full test. Document the failure in the v3 dry-run report; revise the spec creating HA-C4b-v4 with v3 archived.

- **Train-only vs validate-only directional inconsistency within unmedicated**: v2's test observed train (a) = 42.9% / validate (a) = 0%. v3 with 2023-02-04 restored may shift train (a) higher; validate (a) is structurally low at n = 2. The result.md interprets directional inconsistency per v2 §9 + the pacing-behaviour confounder: if the inconsistency aligns with pacing-era (e.g. train arm clusters in pre-ergotherapy poor-pacing era, validate arm clusters in post-ergotherapy / emotional-exertion period), this is supportive evidence that the underlying mechanism is pacing-era-dependent.

## 10. Detection script architecture

Inherited from [v2 §10](hypothesis-v2-archived.md#10-detection-script-architecture) wholesale + the following v3 operational updates:

### 10.1 Stage 1 — primitive (already done)

Unchanged from v2.

### 10.2 Stage 2 — test (`HA-C4b/test.py`, to be REWRITTEN post-lock for v3)

The v3 test.py replaces v2's at the top-level slot. v2's `test.py` (commit `83a64b2`) will be renamed `test-v2-archived.py` at v3 lock; the v3 test-execution session writes a new `test.py` per the v3 spec.

**v3 operational deltas from v2's test.py**:

1. **§4.3 1b.ii dropped**. v3 test.py does NOT build the wake-window quartile-coverage cache. The `passes_quartile_gate` function (and all related FIT-cache walking code) is removed. v3 day-eligibility check uses gate 1 + gate 1b.i + §4.2 exertion-conditioning + the §6 exclusions; no 1b.ii.

2. **§10.2 spec-sanity-gate symmetric**. v3 dry-run applies the SAME day-eligibility as the full run (gate 1 + gate 1b.i, no 1b.ii). The n that passes the dry-run gate is the n the full run evaluates. The `--use-quartile-cache` flag is removed.

3. **Headline cell evaluation, LOO, sensitivity ladder, secondary outcomes**: all UNCHANGED from v2's test.py. Inherit verbatim.

4. **Run protocol** (§10.4): same shape as v2; no quartile-cache build step.

### 10.3 Stage 3 — `result.md`

Same v2 layout (single headline block; train-only / validate-only directional-consistency companions; LOO range + load-bearing list + boundary-fragility note; companion-phase descriptive cells; sensitivity ladder; E[L]* companion; §4.11 descriptive outcomes; v3 caveats per §8).

**v3-specific result.md additions**:
- The §8 v3 "1b.ii dropped — operationalisation refinement" caveat must be the FIRST caveat surfaced (prominent placement; mirrors v2's v1 → v2 transition disclosure pattern).
- The §8 pacing-behaviour confounder caveat must be surfaced with the verdict block.
- If the user has supplied approximate pacing-era + emotional-event dates, the result.md should annotate each surviving episode with pacing-era + emotional-event-proximity flags (descriptive only; no verdict weight).

### 10.4 Run protocol (v3)

1. **Dry-run** (`python test.py --dry-run`): prints sample sizes per phase × era; checks v3 §10.2 spec-sanity-gate (n ≥ 10 pooled-unmedicated post-§4.5; per-phase median primary inside v3 §7 ranges; per-phase median σ inside [25, 55] for unmedicated). **No 1b.ii applied.** If sanity check fails → halt + revise spec → HA-C4b-v4.
2. **Full run** (`python test.py`): same §4.3 gate as dry-run (no asymmetry). Emits v3 `result.md` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-C4b-v4 with the v3 result archived.

---

*Pre-registration v3 drafted 2026-06-16 by Claude (Opus 4.7) in reviewer-mode-with-authorization, in the same Claude session that test-executed v2 to INCONCLUSIVE (commit `83a64b2`). §3.3 same-session operationalisation refinement; the data exposure context is documented in the Authorship block. The next step is a fresh-session `/research-review` audit per `hypothesis_lock_process.md` §3.4. Lock requires user acceptance + audit clearance + the four §3.8 gate confirmations. The v3 test-execution session is a separate session per user choice (handoff brief at `.claude/plans/session-c4b-v3-test-handoff-2026-06-16.md`).*
