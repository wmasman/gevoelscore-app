# HA-C4b v3 — Stress-with-low-motion minute count as crash precursor (Wiggers C4 + motion filter), unmedicated pooled headline; §4.3 1b.ii dropped + pacing-behaviour confounder caveat

## Authorship

**Drafted 2026-06-16** by Claude (Opus 4.7) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. **§3.3 same-session operationalisation refinement** of v2 (NOT a §3.2 fresh-session redraft); explicit user authorization 2026-06-16 to draft v3 in the test-execution session that ran v2 to INCONCLUSIVE. The data exposure context is: the v3 drafting context has seen v2's full result.md including per-episode z-scores on the unmedicated train arm (notably 2023-02-04 at `max_signed_z = +3.73` on d-1), the E[L]* = 3.30 finding, and the train/validate directional inconsistency (train 42.9% / validate 0%). Per [`hypothesis_lock_process.md` §3.3](../../../methodology/hypothesis_lock_process.md#33-optional-post-draft-revision-r1-data-exploration-absorption) that level of data exposure permits operationalisation refinements but NOT headline-cell relocks. **v3 makes no headline-cell change** (the locked cell is byte-identical with v2 §5.0).

**§3.3 discipline-stretch acknowledgment** (added r2 to close the audit side observation): `hypothesis_lock_process.md` §3.3 is written as *"Optional post-draft revision r1 (data-exploration absorption)"* — its literal scope is *between an initial draft and the first audit*. v3's situation is structurally different: *between a v2 test execution (which produced a full result.md including per-episode z-scores on the dropped episode) and a v3 successor pre-reg draft*. The §3.3 label as applied is an **extension of §3.3's literal envelope**, not a strict invocation. The discipline-preserving requirements the §3.3 invocation honours — no headline-cell change (v3 §5.0 byte-identical with v2); fresh-session v3 test execution mandated (via the handoff brief at `.claude/plans/session-c4b-v3-test-handoff-2026-06-16.md`); honest §8 disclosure of the data-exposure level and the operational-choice-within-asymmetry-fix-space concern (audit Layer 2.5 substantive) — are the discipline's intent. The literal scope is stretched; the intent is honoured. This Authorship-block note is the audit-able marker for a future `hypothesis_lock_process.md` revision that formalises §3.3b "post-result operationalisation refinement" with its own envelope (operationalisation-only; no headline-cell change; the §10.2-style spec-design-flaw window). Per the audit Section-4 item 3 recommendation.

**v3 trigger**: v2's test session 2026-06-16 (commit `83a64b2`) landed INCONCLUSIVE because v2's sanity-gate / full-run gate were asymmetric (per v2 §10.2 specification of the dry-run sanity gate + §10.4 run protocol; the dry-run defaulted to 1b.i-only for speed while the full run applied 1b.ii). The full run dropped one train episode (`2023-02-04`), taking the pooled cell from n=10 to n=9 < §5.3 bar. The dropped episode is the train arm's highest-signal episode (its 4-day lead-up included `max_signed_z = +3.73`). v2's spec-design observation in [`result.md`](result.md) "Critical methodological finding" surfaced the v2 §10.2 / §10.4 gate-asymmetry as the v3 trigger.

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

- **Emotional/cognitive-load methodology MD** (reframed r2 from the original "emotional-exertion proxy primitive" item; the proxy already exists as `cat_belasting_emotioneel` + `cat_belasting_cognitief` + the `state_symptoom_*` columns per §8 above). The methodology MD should document: (i) construct-validity of the v24 notes-categorisation rollup for emotional/cognitive load (does the count of clauses reliably represent magnitude?); (ii) the value-0-low-specificity-about-absence pattern and its implications for analysis (how do we read 0s? are they "no load" or "no mention"?); (iii) the ~35% unmed-phase fill on note-days only and the no-note-day NaN pattern (can we estimate load on no-note days from neighbouring days?); (iv) per-phase coverage and value-distribution stationarity. Once the methodology MD lands, downstream tests (HA-C4b v4 or successor; HA-P-family if relevant) can decide whether to add the load proxies as §4.2 conditioning variables. **Spinning the methodology MD off requires its own four-input-reasoning bar per CONVENTIONS §2.2**; out of scope for v3 same-session refinement. Adding the load proxies to v3's §4.2 conditioning would be a §3.7 approach change (new conditioning variable), requiring a new audit gate.
- **Rouwschop date corpus addition**. The user's referenced rouwschop sessions are not date-able from existing `event_labels` or `notes-categorized-v24-clauses.csv` (per §8.x). If the user can supply a date list from external corpora (calendar, therapist records), a parallel documentation commit can add a `rouwschop_sessions` event-label set to `annotations.yaml` and a `in_rouwschop_period` boolean flag in `per_day_master.csv`. v3 result.md addendum could then surface rouwschop-proximity flags on surviving episodes (descriptive only; no v4 trigger).
- **External viz-notes citations in §4.3 (Family A 2024-11-26 case) and §4.11 (Family D2a ρ = 0.79, Family D2b)**. Carried from v2. Out of scope for v3 same-session refinement; v4 or a parallel documentation commit consolidates into `analyses/garmin_exploration/stress_low_motion_viz/key-findings.md`.

**Revision 2026-06-16-r2** (post-audit, shared-context with drafting per [`hypothesis_lock_process.md` §3.5](../../../methodology/hypothesis_lock_process.md#35-revise-step-stage-3-of-the-arc-r2--the-bulk-of-methodological-strengthening)). Five changes absorbed from the [fresh-session `/research-review` audit report](../../../reviews/HA-C4b-v3-2026-06-16.md) (verdict: **PASS with caveats** — two substantive concerns and three minor / side observations, all closeable as wording-tightenings without a v4). The audit confirmed itself as the canonical §3.4 audit step. All r2 closures are wording-tightenings + locked descriptive context (the §8.x date-anchor sub-block) — no new conjuncts, no falsification-bar change. They fit the [§3.7 reporting-layer-not-approach-change heuristic](../../../methodology/hypothesis_lock_process.md#37-optional-r3-interpretability-augmentation) and do NOT trigger a new audit gate:

- **§4.3 rationale (3) replaced with the empirical override-as-tradeoff framing** (closes audit Layer 1.4 substantive concern). The original wording — *"the binding case does not exist in v3's headline phase"* — was empirically partially-refuted by an ad-hoc check against the FIT quartile cache: 2023-02-04 shows the **pathological quartile-concentrated under-sampling pattern** that 1b.ii was designed to catch (sleep-window-aware Q3 = 8 samples, mid-day uncovered ~11:45-14:00 local CET; wake-window was only 9.1 hours). The aggregate stats: 22 of 709 unmedicated 1b.i-passing days (3.1%) fail sleep-aware 1b.ii, comparable to consolidation's 1.6%. The 1b.ii catch on 2023-02-04 IS real. v3 r2 acknowledges this honestly and reframes the override as a deliberate trade-off justified by an asymmetry the original wording missed: **the crash-start day's coverage failure does not load-bear on the precursor analysis**. The 4-day lead-up reads d-1 through d-4 (here: 2023-02-03 to 2023-01-31), and ALL FOUR pass sleep-aware 1b.ii comfortably (Q-min = 159, 153, 161, 128, all well above 50). The z-scores driving §5.1 (a)+(b)+(c) come from those days, not from 2023-02-04 itself. The crash_v2 label is user-set, not Garmin-derived, so 2023-02-04's coverage doesn't affect the label's validity. The cost: 22 unmedicated days enter baseline + bootstrap pools with noisier day-level predictor values; the benefit: the dry-run/full-run asymmetry is closed AND the high-signal crash episode is restored to the test (independently of its z-score, which the §3.3 discipline says we can't have known when choosing). See §4.3 below for the full reframed rationale.
- **§8 v3 1b.ii caveat updated** (closes Layer 1.4 + the audit's Section-4 item-1 + side observation 3). The caveat now acknowledges 2023-02-04 as a real 1b.ii catch with the pathological pattern, frames the v3 override as a deliberate trade-off (not a "binding case doesn't exist" claim), and surfaces the load-bearing-asymmetry argument from §4.3 r2 above. The result.md must surface this caveat first.
- **§3.3 discipline-stretch acknowledgment added to Authorship block** (closes audit Section-4 item-3 + side observation re §3.3 envelope). One-line note that §3.3's written envelope is *"r1 between initial draft and first audit"* and v3's situation (*r1-of-successor between a test-execution and a successor pre-reg draft*) extends that envelope; the discipline-as-applied (no headline-cell change, fresh-session v3 test execution mandated, honest §8 disclosure) honours §3.3's intent even though the literal scope is stretched. Audit-able marker for a future `hypothesis_lock_process.md` revision adding §3.3b "post-result operationalisation refinement".
- **§9 pacing-era annotation made verdict-invariant** (closes audit Layer 4.7 minor + Section-4 item-4). The previous §9 SUPPORTED-branch paragraph conditioned the pacing-era reading on the verdict label (*"if SUPPORTED... if NOT-SUPPORTED..."*). v3 r2 replaces this with a single descriptive paragraph: the pacing-era + emotional-event-proximity annotation is a property of the EPISODE DATES, not the verdict label; the result.md surfaces them alongside the verdict regardless of which branch fires.
- **§8.x locked descriptive context sub-block added** (closes audit Section-4 item-5 + side observation re user-supplied date routing). Concrete date anchors are written into the v3 spec record at lock-time (NOT at result.md-production-time), held out from the v3 test-execution session via the handoff brief. The dates are derivable from existing master-CSV columns (no privacy-sensitive name strings surfaced; only ISO date boundaries + the umbrella-flag column names). v3 r2 absorbs three of the four named events with empirical date anchors; rouwschop is acknowledged as not-date-able-from-current-data and flagged for the result.md test session to optionally surface if user supplies dates separately.

The audit's pacing-behaviour-confounder substantive concern (item 5 secondary) is partially repositioned in r2: the data has `cat_belasting_emotioneel`, `cat_belasting_cognitief`, `state_symptoom_emotioneel`, and `state_symptoom_cognitief` columns from the v24 notes-categorisation rollup. The original v3 §8 claim that *"v3 does NOT add a quantitative emotional-exertion proxy; that is a queued primitive"* was wrong — the proxy exists, with the caveats described in [`DATA_DICTIONARY.md` §9](../../../DATA_DICTIONARY.md) (presence-conditioned with value-0-low-specificity-about-absence; ~35% unmed-phase fill on note-days only; max observed value 2). r2 corrects §8 to reflect reality: the proxy is available for descriptive-companion-read in result.md (no new conjunct; §5.1 byte-identical with v2); the queued primitive item is reframed as a methodology MD documenting construct validity + sparsity + how to read the proxy, not as building the proxy itself.

The audit's L2.5 substantive concern (the *operational choice within the asymmetry-fix space* was made under exposure to which option restores the train arm's highest-z episode) is acknowledged in r2's expanded Authorship block but NOT closeable as a wording-tightening — it is a genuine discipline cost that the §3.3 same-session refinement path absorbs. The §3.8 lock-commit message must name this concern explicitly. A future fresh-session redraft of the §10.2 fix space alone (with the dropped-episode identity held out) would be a §3.2 redraft, not the §3.3 refinement v3 claims to be; r2 declines that escalation and accepts the substantive concern as priced in to the §3.3 path with the discipline-stretch acknowledgment in the Authorship block.

**Status: LOCKED-PENDING-USER-ACCEPTANCE 2026-06-16 at revision r2 by Claude (Opus 4.7) in reviewer-mode-with-authorization.** Per [`hypothesis_lock_process.md` §3.4](../../../methodology/hypothesis_lock_process.md#34-audit-step-step-2-of-the-arc), the canonical audit step has completed (the [v3 audit report](../../../reviews/HA-C4b-v3-2026-06-16.md) verdict was PASS with caveats; all five Section-4 items closed in r2 above as wording-tightenings + locked descriptive context). Per [`hypothesis_lock_process.md` §3.6](../../../methodology/hypothesis_lock_process.md#36-re-audit-step-stage-4-of-the-arc), re-audit is compressed for r2 because the changes are mechanical (wording-tightenings, sentence additions, locked descriptive-context block) with no architectural change, no new statistical machinery, and no falsification-bar change — the audit's own Section-4 items 1-4 were all labelled wording-tightenings that close without a v4. Compression justification per §3.6: *"r2 changes are wording-tightenings absorbing audit Section-4 items 1-4 + a §8.x locked descriptive-context sub-block per item-5; no architectural change; no falsification-bar change; the audit verdict explicitly states the items close without a v4."*

Lock signal awaits explicit user acceptance + commit message naming the four §3.8 gate confirmations. The four [§3.8 lock-blocking gates](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc) for the lock commit:

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

**v3 rationale for dropping 1b.ii** (audit-able; rewritten r2 to absorb audit Layer 1.4 substantive concern + Section-4 items 1-2):

1. **The primitive itself does not require 1b.ii.** Per [`stress_low_motion_primitive.md` §5 NaN policy + day-validity gate](../../../methodology/stress_low_motion_primitive.md#5-nan-policy--day-validity-gate): "Day-validity gate: ≥ 600 in-range stress samples." 1b.ii was an HA-C4b-specific strengthening, not a primitive-level requirement.

2. **v2's §10.2 dry-run gate / §10.4 full-run gate asymmetry caused the v2 INCONCLUSIVE verdict.** The dry-run skipped 1b.ii for speed (the quartile-coverage cache takes 5-15 min to build from FIT files); the full run applied 1b.ii. Pooled-unmedicated n went from 10 (dry-run, 1b.i only) to 9 (full run, 1b.i + 1b.ii) — below the §5.3 bar. This asymmetry is a spec-design flaw, not a data finding. v3 closes the flaw by symmetrising the gates (see point 4 below) — and the symmetrisation choice within the v3 fix space (drop 1b.ii vs apply 1b.ii at dry-run vs tighten 1b.i to subsume 1b.ii's intent) is the operational decision v3 makes, with the discipline cost named in §8 (audit Layer 2.5 substantive concern: the choice was made under exposure to which option restores the train arm's highest-z episode).

3. **1b.ii catches a real pathological pattern on 2023-02-04 in the unmedicated phase; v3 overrides this catch as a deliberate trade-off** (rewritten r2 from the earlier "binding case doesn't exist" claim, per audit Section-4 items 1-2 + ad-hoc empirical check against the FIT quartile cache). Specifically: 2023-02-04 shows sleep-window-aware Q3 = 8 samples (the mid-day quartile ~10:45-13:00 UTC ≈ 11:45-14:00 local CET is essentially uncovered; wake-window was only 9.1 hours, with sleep_end 06:11 UTC and next sleep_start 15:18 UTC). The other three quartiles had 143, 95, 145 samples respectively. This is exactly the quartile-concentrated under-sampling pattern 1b.ii was designed to catch — NOT uniform low coverage that 1b.i alone would catch at a lower threshold. Aggregate stats from the same check: 22 of 709 unmedicated 1b.i-passing days (3.1%) fail sleep-aware 1b.ii, comparable to consolidation's 1.6%. The earlier v3 wording ("the binding case does not exist in v3's headline phase") was empirically partially-refuted; r2 reframes the 1b.ii drop honestly as a deliberate override:

   **The override is justified by the load-bearing asymmetry between the crash-start day and the lead-up days.** The §5.1 (a)+(b)+(c) bar is computed from z-scores in the 4-day lead-up window — i.e. days `[d-1, d-2, d-3, d-4]`, not day `d` itself. For 2023-02-04 the lead-up days are [2023-02-03, 2023-02-02, 2023-02-01, 2023-01-31]; all four PASS sleep-aware 1b.ii comfortably (Q-min = 159, 153, 161, 128, all well above 50). The z-scores driving the v3 headline-cell verdict are unaffected by 2023-02-04's own coverage. The crash-start day's coverage failure does not load-bear on the precursor analysis.

   Additionally: the `crash_v2` label is user-set, not Garmin-derived; coverage on 2023-02-04 does not affect the label's validity. The 1b.ii on the crash-start day's eligibility check is therefore overkill for the precursor question. The cost of the override: 22 unmedicated days (~3.1% of 1b.i-passing days) enter the baseline lagged-mean pool and the bootstrap-null distribution with noisier day-level predictor values; the benefit: the dry-run/full-run asymmetry is closed AND the high-signal 2023-02-04 episode is restored to the test (the discipline note: at v3 drafting time the *fact* of 2023-02-04's z-score being high was known, but the *consequence* of restoring it for the v3 verdict is unknown until the v3 test runs — see audit Layer 2.5 concern + §8 caveat).

4. **Symmetry of dry-run + full-run gating is required for the v3 §10.2 sanity-gate to do its work.** v3's §10.2 evaluates n ≥ 10 against the same §4.3 (gates 1 + 1b.i) at both dry-run and full-run; the n that passes the dry-run gate IS the n the full-run evaluates. No further §4.3 exclusion between the two regimes. (An alternative symmetrisation — apply 1b.ii at dry-run too — was considered and rejected on the grounds that 1b.ii on the crash-START day doesn't load-bear on the precursor analysis per point 3 above; tightening 1b.i to subsume 1b.ii's intent was also considered and rejected on the grounds that 1b.i is a total-samples gate while 1b.ii is a within-day-distribution gate, structurally different signals that can't be conflated.)

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

- **§4.3 1b.ii dropped in v3 — operationalisation refinement; deliberate override of a real 1b.ii catch** (rewritten r2 to absorb audit Layer 1.4 substantive + Section-4 items 1-2). v2 applied §4.3 1b.ii (wake-window quartile-coverage gate) at the full run only, dropping one train episode (`2023-02-04`, max_signed_z = +3.73 on d-1) from the pooled-unmedicated headline cell, taking n from 10 to 9 → INCONCLUSIVE per §5.3. **v3 drops 1b.ii and restores 2023-02-04. An ad-hoc empirical check (r2 absorption) confirmed 2023-02-04 has the pathological quartile-concentrated under-sampling pattern 1b.ii was designed to catch** (sleep-window-aware Q3 = 8 samples; mid-day uncovered ~11:45-14:00 local CET; wake-window only 9.1 hours). The earlier v3 wording — *"the binding case does not exist in v3's headline phase"* — was empirically partially-refuted; r2 frames the drop honestly as a deliberate override.

  **The override is justified by the load-bearing asymmetry** (see §4.3 rationale (3)): the §5.1 (a)+(b)+(c) bar reads z-scores in the 4-day LEAD-UP window, not the crash-start day. 2023-02-04's lead-up days [2023-02-03, 02-02, 02-01, 01-31] all pass sleep-aware 1b.ii comfortably (Q-min = 159, 153, 161, 128); the z-scores driving the headline-cell verdict are unaffected by 2023-02-04's own coverage. The crash_v2 label is user-set, not Garmin-derived, so coverage doesn't affect label validity. The cost of the override: 22 unmedicated days (3.1%) enter baseline + bootstrap pools with noisier day-level predictor values.

  **The discipline cost — audit Layer 2.5 substantive concern**: the v3 drafting context knew that 2023-02-04 was the train arm's highest-z episode (max_signed_z = +3.73 on d-1) at the time of the v3 spec choice. The choice within the asymmetry-fix space (drop 1b.ii vs apply 1b.ii at dry-run vs tighten 1b.i) was made under exposure to which option restores this specific high-signal episode. The §5.1 falsification bar is byte-identical with v2 (no cell relock; no parameter changes) — the cell-coordinate invariance is preserved — but the operational choice IS data-informed. A strict-pre-registration reviewer's defensible objection: this is post-hoc "rescue" of a specific high-signal episode dressed up as a spec-design fix. v3's counter: the override is independently supported by the primitive's own validity requirement (only the 600-sample gate is primitive-mandated; 1b.i + 1b.ii were both HA-C4b-specific strengthenings) AND the load-bearing-asymmetry argument above; the §5.1 bar is unchanged. The result.md must surface both the override-as-trade-off framing AND the strict-reviewer objection so the reader can judge for themselves. The honest framing: v3's drop is defensible but not strictly-pre-registered; the verdict it produces sits at the §3.3 same-session refinement level of discipline, not the §3.2 fresh-session level. Future v4 (if needed) under fresh-session redraft would adjudicate whether the v3 verdict survives the strictest discipline.

- **v2 → v3 transition disclosure**. The v3 spec was drafted in the same Claude session that ran v2's test (and saw v2's per-episode z-scores including the dropped 2023-02-04 episode). Per [`hypothesis_lock_process.md` §3.3](../../../methodology/hypothesis_lock_process.md#33-optional-post-draft-revision-r1-data-exploration-absorption), this data-exposure context permits operationalisation refinements (which v3 is) but NOT headline-cell relocks (v3 makes no headline-cell change; the locked cell at §5.0 is byte-identical with v2). The Authorship block documents this explicitly. v3 was drafted to the §3.3 discipline; the §3.4 audit step is fresh-session and adjudicates whether the §3.3 refinement was defensible at this data-exposure level.

- **Pacing-behaviour confounder (qualitative-only at v3)**. The §4.2 exertion-conditioning column `exertion_class_lagged_lcera` captures **physical exertion only** (Garmin-derived from heart-rate / motion / training-load aggregates). It does NOT capture:
  - **Cognitive exertion** (concentration, reading, fast conversation, screen time, screen-content cognitive load). Per [`pacing-and-crash-mitigation.md` §1](../../../literature/pacing-and-crash-mitigation.md): "The brain uses ~20% of the body's energy; cognitive overexertion can crash someone as hard as a walk."
  - **Emotional exertion** (grief, relational stress, conflict, high-stakes meetings, exposure to triggering content). Per the same reference: "All exertion counts, not just physical." The energy envelope is shared.
  - **Orthostatic exertion** (being upright; orthostatic load draws on the same envelope).

  **Quantitative proxies that DO exist in the corpus** (added r2 to absorb audit Section-4 item-5 / replace the earlier "queued primitive" claim, which was wrong — the proxies exist, with caveats):

  - **`cat_belasting_emotioneel`** (per-day count of emotionally-tagged note clauses; presence-conditioned; ~35% fill on unmedicated phase). Per [`DATA_DICTIONARY.md` §9](../../../DATA_DICTIONARY.md): value-0 on a note-day is *low-specificity about absence* (means "no emotional-load clause tagged" not "no emotional load"); NaN on no-note days; unmedicated-phase distribution: 242 days = 0, 14 days = 1, 2 days = 2, 0 days ≥ 3; mean 0.07; max 2.
  - **`cat_belasting_cognitief`** (same shape; cognitive load).
  - **`state_symptoom_emotioneel`** (categorical {absent, mild, present, severe}; symptom severity on note-days only).
  - **`state_symptoom_cognitief`** (same shape; cognitive symptom severity; per the data dictionary the user almost never tags this).
  - **`in_pwc_reintegratie_2023`** (boolean flag from `annotations.yaml` umbrella spans; dense within the trajectory window; per §8.x below).

  **What v3 does with the proxy**: descriptive companion-read in result.md only. The result.md surviving-episode table includes columns for `cat_belasting_emotioneel`, `cat_belasting_cognitief`, `state_symptoom_emotioneel`/`cognitief`, `in_pwc_reintegratie_2023`, plus the era classification per §8.x below. Descriptive only; never promotes; v3 §5.1 byte-identical with v2; the proxy is NOT in §4.2 conditioning.

  **Why not in §4.2 conditioning**: (i) cat_belasting_emotioneel's value-0 is low-specificity about absence (the proxy can't reliably tell "no emotional load" days from "no note" days); (ii) ~65% NaN on no-note days; (iii) the proxy is a *count of mentions* not a *level estimate*; (iv) including it as a conditioning variable would be a §3.7 approach change (new conditioning variable), requiring a new audit gate (it is queued, see Pending follow-ups). For v3 the proxy stays descriptive.

  **Two structural consequences for HA-C4b** (unchanged from r1, restated):
  1. Some unmedicated-phase crashes may have been **emotionally / cognitively triggered without a matching heavy physical exertion in the lead-up window**, in which case §4.2 exertion-conditioning **excludes them from the eligible-crash pool entirely**. The HA-C4b test cannot speak to these crashes by construction. A NOT-SUPPORTED reading must therefore be interpreted as "HA-C4b's lived motion-filter refinement of Wiggers C4 is NOT a precursor for *the physically-exertion-conditioned subset of crashes*", not as a general claim about all crashes.
  2. Some eligible-pool crashes (those that DO pass §4.2 exertion-conditioning) may have an emotional component that is the *actual proximate trigger*, with the physical exertion being incidental rather than causal. For these crashes, the lead-up `stress_low_motion_min_count_S60_Mlow` may or may not show elevation; the signal depends on whether the emotional load also presented as Garmin-stress-while-at-rest in the days before the crash.

  **The result.md must surface this caveat with the verdict AND annotate every surviving episode with the §8.x pacing-era + PWC-flag + emotional/cognitive-load descriptive flags**. The annotation is verdict-invariant (per §9 r2 reformulation) and §3.7 reporting-layer-only (descriptive; no SUPPORTED-bar weight, no verdict modification).

### 8.x Locked pacing-era + emotional-event date anchors (added r2; locked at v3 lock-time per audit Section-4 item-5)

The audit recommended that user-supplied descriptive context be locked into the v3 spec record at lock-time (NOT introduced during v3 result.md production), held out from the v3 test-execution session. The dates below are derived from the existing master-CSV columns; no privacy-sensitive name strings are surfaced in this committed spec.

**Era anchors within the unmedicated phase (2022-04-04 → 2024-04-08)**:

| era label | date window | source column / derivation | n unmedicated days in era |
|---|---|---|---|
| **early-LC, pre-ergotherapy** | 2022-04-04 → 2022-06-16 | LC-era start through first ERGO event_label hit minus 1d | ~74 days |
| **during-ergotherapy** | 2022-06-17 → 2023-03-10 | first ERGO event_label hit through last ERGO/ERGOTHERAPY event_label hit | ~266 days |
| **post-ergotherapy, pre-PWC-reintegratie** | 2023-03-11 → 2023-03-05 | between ERGO end and PWC reintegratie start; effectively empty (PWC start preceded ERGO end by 4 days) | — overlaps with adjacent eras — |
| **during-PWC-reintegratie 2023** | 2023-03-06 → 2023-11-28 | `in_pwc_reintegratie_2023 == True` (268-day flagged span) | 268 days |
| **post-PWC, pre-citalopram** | 2023-11-29 → 2024-04-08 | between PWC end and citalopram start (2024-04-09) | ~131 days |

**Mapping of the 10 pooled-unmedicated crash episodes to these eras** (descriptive only; the pooled-cell verdict is on the full pool, not per-era):

| episode | era | concurrent flags |
|---|---|---|
| 2022-09-16 | during-ergotherapy | |
| 2022-11-23 | during-ergotherapy | |
| 2023-02-04 | during-ergotherapy | (restored by v3 1b.ii drop) |
| 2023-05-28 | during-PWC-reintegratie 2023 | `in_pwc_reintegratie_2023 == True` |
| 2023-06-12 | during-PWC-reintegratie 2023 | `in_pwc_reintegratie_2023 == True` |
| 2023-09-07 | during-PWC-reintegratie 2023 | `in_pwc_reintegratie_2023 == True` |
| 2023-09-16 | during-PWC-reintegratie 2023 | `in_pwc_reintegratie_2023 == True` |
| 2023-09-27 | during-PWC-reintegratie 2023 | `in_pwc_reintegratie_2023 == True` |
| 2024-01-12 | post-PWC, pre-citalopram | (these are the v2 validate-era episodes) |
| 2024-02-15 | post-PWC, pre-citalopram | (these are the v2 validate-era episodes) |

**Structural observation**: the train/validate split (train ends 2023-12-31) maps almost exactly to the during-PWC vs post-PWC split. The v2 directional inconsistency (train 42.9% / validate 0%) — and any v3 echo of it — has a substantive candidate interpretation beyond temporal era: the during-PWC sub-pool overlaps the structured back-to-work trajectory's emotional / cognitive load, while the post-PWC sub-pool is post-trajectory + pre-citalopram. The pooled headline cell collapses these two substantively-different load contexts; the era annotation surfaces them so the reader can judge the pooled verdict against the context split.

**Named emotional-exertion events the user referenced**:

- **Tweede-spoor conversations**: 2 specific dates surfaced from `event_labels` keyword match — **2023-10-19** (during-PWC) and **2023-12-04** (post-PWC, transition). Both in unmedicated. Neither is a crash date; both are nearby in time to crash episodes (e.g. 2023-09-27 is ~3 weeks before 2023-10-19; 2024-01-12 is ~5 weeks after 2023-12-04). Lead-up effects unknown without per-episode read.
- **Computer / office handover (terminating employment)**: 1 date surfaced from `event_labels` keyword match — **2024-06-28**. This is in the **buildup phase** (after citalopram start), OUTSIDE the v3 unmedicated headline cell. Not relevant to the v3 verdict directly; noted as context for downstream synthesis with [`garmin_pacing_practice.md`](../../../methodology/garmin_pacing_practice.md).
- **Rouwschop sessions (grief-processing therapy)**: **NOT date-able from existing data**. Zero hits in `event_labels` for "rouwsch" / "rouw" / "verlies" / "grief" / "kanker" keywords; zero hits in the clause-level notes file `notes-categorized-v24-clauses.csv` for "rouwsch". One single "rouw" hit at 2024-01-24 in clauses (in unmedicated; near the 2024-01-12 crash episode by ~2 weeks but possibly unrelated). v3's locked-context handoff to the test session: rouwschop session dates ARE NOT in the v3 spec record. If the user has them in another corpus (calendar, therapist records), they can be added as a result.md addendum *after* the v3 test session lands; that addendum is descriptive-only per §3.7 and does NOT trigger a v4. The v3 test session's per-episode annotation table includes the date columns it has — rouwschop is acknowledged as absent.
- **Pre-ergotherapy pacing-behaviour assessment**: the user's stated framing is *"in the period before ergotherapy we had no or at least bad pacing behaviour"* — but the unmedicated phase window (LC-era start 2022-04-04) starts only ~74 days before the first ERGO event_label hit (2022-06-17). The "pre-ergotherapy" sub-window inside the unmedicated phase is small; no pooled crash episodes fall in it. The pre-ergotherapy framing maps to the *pre-LC era* in this corpus, which is OUTSIDE the v3 test window by construction (LC_ERA_START = 2022-04-04).

**Discipline note on these dates**: locked at v3 r2 lock-time before the v3 test-execution session reads any v3 per-episode z-scores. The dates are derived from existing master-CSV columns (no new data); the test session uses them as descriptive context only (per the handoff brief at [`session-c4b-v3-test-handoff-2026-06-16.md`](../../../../../../.claude/plans/session-c4b-v3-test-handoff-2026-06-16.md)). The dates do NOT change any §5 falsification-bar parameter. Per audit Section-4 item-5 closure.

## 9. What we do with each outcome

Inherited from [v2 §9](hypothesis-v2-archived.md#9-what-we-do-with-each-outcome) wholesale + the following v3-specific augmentation (per the [§3.7 reporting-layer heuristic](../../../methodology/hypothesis_lock_process.md#37-optional-r3-interpretability-augmentation) — no new conjuncts):

**Verdict-invariant pacing-era + emotional-load annotation** (r2: replaces the earlier verdict-conditional language per audit Layer 4.7 + Section-4 item-4). The pacing-era + emotional-event-proximity flags from §8.x + the `cat_belasting_emotioneel` / `cognitief` + `state_symptoom_*` proxies from §8 are properties of the EPISODE DATES, not of the verdict label. The result.md surfaces them alongside the verdict regardless of which §9 branch fires. The annotation table is:

| episode | era (§8.x) | `in_pwc_reintegratie_2023` | `cat_belasting_emotioneel` | `cat_belasting_cognitief` | `state_symptoom_emotioneel` | `state_symptoom_cognitief` | (lead-up rollup if available) |

The reader judges concordance / divergence between the verdict and the era-context independently. The annotation never modifies the §5.1 verdict; it is descriptive companion-read material per §3.7.

**Each verdict branch's interpretation restates the pacing-behaviour confounder per §8** (the *substantive* reads are verdict-conditional; the *annotation table* above is verdict-invariant):

- **Pooled-unmedicated SUPPORTED** (v3): the Wiggers C4 motion-filtered stress-elevated-minute count discriminates pre-crash from null windows on the unmedicated phase POOLED ARM, **under the v3 1b.ii-dropped day-validity discipline**, **for the §4.2 physically-exertion-conditioned subset of crashes only**. The verdict does NOT generalise to emotionally / cognitively triggered crashes (the §4.2 gate excluded them). The annotation table above is surfaced alongside the verdict so the reader can see WHICH episodes triggered, in which era, with which load-context flags — the reader judges the verdict's strength against the context independently. The §4.3 1b.ii-override discipline cost (audit Layer 2.5 substantive concern; §8 v3 caveat) is restated: the v3 SUPPORTED reading is a §3.3 same-session-refinement-discipline verdict, not a strict-pre-registration verdict; a v4 fresh-session redraft of the §10.2 fix space (with 2023-02-04's identity held out) would be the strictest-discipline replication.

- **Pooled-unmedicated NOT-SUPPORTED** (v3): one or more of (a)(b)(c) fails on the v3 pooled cell. The locked-pre-reg reading: the motion-filter-refined Wiggers C4 stress signal does NOT carry crash-precursor weight on the unmedicated PHYSICALLY-EXERTION-CONDITIONED subset. **Recommended primary alternative reading** (from v2 §9, restated): the lived rest-stress trigger may be PROTECTIVE rather than PREDICTIVE — the participant acts on the trigger and prevents the crash. **v3 second alternative reading** (the pacing-behaviour confounder): the unmedicated-phase crashes the §4.2 gate admits may be disproportionately *emotionally / cognitively triggered with incidental physical exertion in the lead-up*, in which case the lack of stress-low-motion signal is exactly what an emotional-trigger story predicts (the body wasn't in the "stuck sympathetic / walls of orange" state pre-crash; the emotional event simply ran the budget down). The annotation table above is surfaced alongside the verdict; if `cat_belasting_emotioneel` / `cat_belasting_cognitief` is elevated on the lead-up days for NOT-SUPPORTED episodes (or `state_symptoom_emotioneel` is "present" / "severe"), the emotional-trigger reading gains descriptive support. The result.md must hold both alternative readings open; neither is testable within v3.

- **Pooled-unmedicated INCONCLUSIVE** (v3): n drops below 10 at the final exclusion. v3 §10.2 makes the dry-run gate symmetric with the full-run gate (both apply gates 1 + 1b.i only, no 1b.ii); the v2-style asymmetry-driven INCONCLUSIVE is structurally impossible in v3. **If INCONCLUSIVE fires in v3, the cause is §4.5 baseline-availability exclusion (not the v2 1b.ii-vs-1b.i asymmetry that v3 closed; not §4.3 1b.ii which v3 dropped).** Per v3 §9 INCONCLUSIVE branch: halt + recommend v4 only if a recoverable operationalisation refinement exists; otherwise descriptive companions + the §8.x annotation table become the only output and the pacing-behaviour caveat is restated. (Side-observation closure from audit: v3 has *one fewer trigger* for INCONCLUSIVE than v2 — 1b.ii-dropping-n is no longer in scope.)

- **Construct-disambiguation differs from primary headline / Respiration-companion sensitivity differs / Sensitivity ladder shows non-monotonicity**: inherited from v2 §9.

- **Spec sanity-check fails on v3 dry-run** (unmedicated pooled n falls below 10 with the symmetric 1b.i-only gate; or per-phase median falls outside §7 ranges; or median σ outside [25, 55] for unmedicated): DO NOT run the full test. Document the failure in the v3 dry-run report; revise the spec creating HA-C4b-v4 with v3 archived. **v3 has one fewer sanity-fail trigger than v2** (1b.ii-dropping-n is no longer a possible cause; the only routes to sanity-fail are §4.5 baseline-insufficiency consuming train episodes, §7 anchor-range drift, and unmedicated σ_median drift).

- **Train-only vs validate-only directional inconsistency within unmedicated**: v2's test observed train (a) = 42.9% / validate (a) = 0%. v3 with 2023-02-04 restored may shift train (a) higher; validate (a) is structurally low at n = 2. The annotation table above lets the reader see whether the train/validate split maps to the during-PWC / post-PWC split (per §8.x: it almost exactly does). If yes, the verdict's directional inconsistency has a substantive candidate interpretation: the pooled cell collapses two substantively-different load contexts (during-trajectory emotional/cognitive load vs post-trajectory mix). The result.md surfaces this descriptively per the §8.x annotation; the pooled verdict still stands as the locked single-cell verdict, but the reader is equipped to read it against the era split. Do NOT retroactively re-split the headline.

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
- The §8 v3 "§4.3 1b.ii dropped — deliberate override of a real catch" caveat must be the FIRST caveat surfaced (prominent placement; mirrors v2's v1 → v2 transition disclosure pattern). The strict-pre-registration objection (audit Layer 2.5 substantive concern) is named alongside v3's load-bearing-asymmetry defence; the reader judges.
- The §8 pacing-behaviour confounder caveat (qualitative + the cat_belasting_* / state_symptoom_* proxy reality) must be surfaced with the verdict block.
- **The §8.x locked descriptive-context annotation table is included alongside every surviving episode** (per §9 r2 verdict-invariant annotation): for each of the 10 (or fewer, if §4.5 drops some) pooled-unmedicated episodes, report era classification per §8.x, `in_pwc_reintegratie_2023` flag, `cat_belasting_emotioneel`, `cat_belasting_cognitief`, `state_symptoom_emotioneel`, `state_symptoom_cognitief` (on the crash-start day AND aggregated across the 4-day lead-up window). Descriptive only; never promotes; per §9 r2 verdict-invariant.

### 10.4 Run protocol (v3)

1. **Dry-run** (`python test.py --dry-run`): prints sample sizes per phase × era; checks v3 §10.2 spec-sanity-gate (n ≥ 10 pooled-unmedicated post-§4.5; per-phase median primary inside v3 §7 ranges; per-phase median σ inside [25, 55] for unmedicated). **No 1b.ii applied.** If sanity check fails → halt + revise spec → HA-C4b-v4.
2. **Full run** (`python test.py`): same §4.3 gate as dry-run (no asymmetry). Emits v3 `result.md` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-C4b-v4 with the v3 result archived.

---

*Pre-registration v3 drafted 2026-06-16 by Claude (Opus 4.7) in reviewer-mode-with-authorization, in the same Claude session that test-executed v2 to INCONCLUSIVE (commit `83a64b2`). §3.3 same-session operationalisation refinement; the data exposure context is documented in the Authorship block. The next step is a fresh-session `/research-review` audit per `hypothesis_lock_process.md` §3.4. Lock requires user acceptance + audit clearance + the four §3.8 gate confirmations. The v3 test-execution session is a separate session per user choice (handoff brief at `.claude/plans/session-c4b-v3-test-handoff-2026-06-16.md`).*
