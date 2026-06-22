# Phase-axis collapsibility conventions — pooling rules for the LC recovery-phase axis

*Producer-mode methodology MD per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-helps-the-user-build-the-research-artefact). Drafted 2026-06-22 as r1; r2 absorbs + LOCK 2026-06-22 per [`hypothesis_lock_process.md §3.6`](hypothesis_lock_process.md) compression (audit verdict PASS-with-caveats; mechanical r2; no architectural change).*

---

## Authorship

**Drafted 2026-06-22** by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-helps-the-user-build-the-research-artefact). Authorising user: user (name redacted per `audit_for_publication.py` discipline).

**Drafting-session context**: directly follows the [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) **r2 LOCK 2026-06-19** (`d47e0d3`). User observation in main session 2026-06-22 (post-lock-wave reflection): the axis MD specifies the 6-phase structure but does NOT specify which phases can be **pooled** for an HA pre-reg or descriptive analysis. Pooling decisions are recurring (e.g. "pool 4a+4b → 4 when sub-phase n is too tight"; "pool 4+5 → unified pacing+medication era when channel isn't dose-modulated"); without a documented convention each consumer re-invents the discipline, with corresponding risk of data-driven back-doors leaking into the choice. PM-confirmed 2026-06-22 via AskUserQuestion: (a) **hypothesis-driven only** as the collapse trigger (no data-driven decision pathway), (b) new dedicated methodology MD location (not a v2 of `lc_recovery_phase_axis.md` — keep the axis MD clean as the axis spec, host the collapsibility discipline here).

**Status**: **r2 LOCKED 2026-06-22** per [CONVENTIONS §2.2 + §2.3](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) audit hooks + [`hypothesis_lock_process.md §3.6`](hypothesis_lock_process.md) compression. Fresh-session methodology audit completed 2026-06-22 ([`reviews/phase_axis_collapsibility_conventions-2026-06-22.md`](../reviews/phase_axis_collapsibility_conventions-2026-06-22.md) at commit `1f940ef`); verdict PASS-with-caveats; §3.6 compression applied because all r2 absorbs are mechanical (no architectural shift; 3-tier + hard boundary preserved; no new claim; all 3 user-locked decisions verified honored). r2 absorbs closed the 4 mechanical audit fires (L2 §6.4 wording, L4 §6.1 named-counts cross-ref, PE.4 §3.5 placement forward-pointer, PE.3 verification of §3.5 "illustrative, not exhaustive" framing) and added reciprocal-cite paragraphs to [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) §6.7 + [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md) §1. Governed by CONVENTIONS §2.2 + §2.3 (methodology MD carve-out per [`hypothesis_lock_process.md §0`](hypothesis_lock_process.md), not the HA lock process).

---

## Citation status

Runs on **first-principles methodological reasoning + established project conventions**. No new external literature anchors required — the discipline this MD codifies is fully derivable from the project's existing anchored conventions:

- [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) (descriptive-before-inference),
- [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) (caveats vs a-priori),
- [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory) (prior-driven hypotheses are confirmatory),
- [`lc_era_temporal_segmentation.md §4`](lc_era_temporal_segmentation.md) (anti-data-driven-boundary-tuning),
- [`citalopram_phase_stratification.md §5`](citalopram_phase_stratification.md#5-the-three-downstream-test-treatment-patterns) (the three treatment patterns: per-phase / dose-adjusted / per-mg subtraction),
- [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) (the 6-phase axis this MD governs).

**Inherited project-canonical anchors** (already fetched + cited in upstream MDs; not duplicated here):

- SCRIBE 2016, CENT 2015, STROBE 2007, Daza 2018, WWC 2022 SCED, Natesan Batley 2023 — anchored via `CONVENTIONS §1.2` + `reviews/README.md`.
- The v3 dose-response confirmation on 3 CONFIRMED-citalopram channels — anchored via [`citalopram_dose_response_stress_mean_sleep.md §5.6`](citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14).

**Deferred-but-named honestly**: if a future fetch surfaces an SCED / observational-cohort meta-paper on pooling-discipline in within-subject longitudinal designs (candidate: a Daza-family follow-up, a single-case meta-analytic review), this MD's §5.2 row can absorb it without architectural change. The methodological reasoning stands independently on the inherited anchors.

---

## 1. What this MD is, and what it does not

### 1.1 Is

A **collapsibility convention** for the [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) 6-phase axis (phases 1, 2, 3, 4a, 4b, 5). Specifies a 3-tier hierarchy of *pooling moves that ARE available to HA pre-regs and descriptive analyses* + one hard boundary that is *NEVER* pooled. The trigger for choosing a tier is **hypothesis-driven only** (per PM 2026-06-22): the analyst chooses a tier from the structural shape of the hypothesis-channel pair, not from any in-data signal.

Sits **downstream** of `lc_recovery_phase_axis.md` (the axis spec) and **orthogonal** to the inner citalopram axis (governed by [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)). Treatment patterns for CONFIRMED-citalopram channels (§5.A/B/C) inherit from the citalopram stratification MD without modification.

### 1.2 Is not

- **NOT a re-derivation of the 6-phase axis.** `lc_recovery_phase_axis.md` is the source-of-truth for the phase structure + the per-phase warrants. This MD downstream-consumes that structure.
- **NOT a binding gate on every HA pre-reg.** Per [`lc_era_temporal_segmentation §6`](lc_era_temporal_segmentation.md), HA pre-regs *opt in* to the recovery-phase axis. Pre-regs that don't adopt the axis don't need these conventions; pre-regs that do adopt the axis must declare a tier + justification in their `§3 Data sources` block.
- **NOT a replacement for `citalopram_phase_stratification §5`.** The three treatment patterns (§5.A per-phase / §5.B dose-adjusted / §5.C per-mg subtraction) for CONFIRMED-citalopram channels are inherited verbatim into Tier B's channel-sensitivity rule. This MD adds the pooling-trigger discipline above them.
- **NOT a data-driven decision tool.** The trigger for collapse is structural (hypothesis-shape + channel-sensitivity + n-adequacy); no in-data signal is consulted to choose a tier. This is the binding discipline anchor per CONVENTIONS §4.2 + `lc_era_temporal_segmentation §4`.
- **NOT a modification of cross-reference MDs.** `lc_recovery_phase_axis.md`, `citalopram_phase_stratification.md`, `lc_era_temporal_segmentation.md`, `citalopram_dose_response_stress_mean_sleep.md` remain unchanged by this r1 draft; reciprocal-cite paragraphs are queued for lock-time (§8).

### 1.3 Cross-axis position — three layers (inherited from `lc_recovery_phase_axis §1.3`)

| layer | axis | source-of-truth MD | this MD's role |
|---|---|---|---|
| Outer | Data-given strata (pre-illness / acute / LC) | [`lc_era_temporal_segmentation.md §1`](lc_era_temporal_segmentation.md) | hard boundary inherited (§2.4) |
| **Middle** | **LC recovery-phase axis** | [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) | **this MD governs how the middle axis is pooled** |
| Inner | Citalopram dose-state | [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md) | Tier B inherits §5.A/B/C verbatim |

The collapsibility conventions operate *within the middle layer*. Cross-classification with the inner citalopram axis is preserved per the existing three-layer factorability per `lc_recovery_phase_axis §1.3`.

---

## 2. The 3-tier hierarchy + hard boundary

Four pooling positions are documented. Tiers A, B, C are *available* moves with hypothesis-driven conditions; the hard boundary is *never* a pooling move.

| tier | pool | resulting unit | available when | binding cross-MD constraint |
|---|---|---|---|---|
| **A — within-pacing safe pool** | 4a + 4b | phase 4 `pacing_pre_citalopram` (564 days) | hypothesis insensitive to phase-4-internal habit-formation variation; OR per-sub-phase n insufficient | none beyond §3 conditions |
| **B — citalopram-corrected pool** | 4 (or 4a+4b separately) + 5 | unified pacing+medication era | channel not in CONFIRMED-citalopram set; OR §5.A/B/C correction applied; OR hypothesis insensitive to dose | CONFIRMED-citalopram channels REQUIRE one of `citalopram_phase_stratification §5.A/B/C` |
| **C — full LC pool (Stratum 4)** | 3 + 4 (with or without 4a/4b split, or Tier-A pooled) + 5 | Stratum 4 (data-given) | hypothesis treats LC era as a whole; OR pre-LC vs LC contrast (Stratum 4 IS the LC stratum); OR lived-experience pacing-onset / medication-onset not expected to alter the channel | inherits as canonical default per `lc_era_temporal_segmentation §1` |
| **HARD BOUNDARY** | phase 1 ↔ 2 ↔ LC era (phases 3-5) | NOT POOLED | **never** — these are data-given strata per `lc_era_temporal_segmentation §1`; pooling across them is a category error (healthy / acute-viral / chronic illness) | binding; no conditions justify this collapse |

**Default canonicals** (per the project's existing conventions, inherited):

- **Tier C is the project-canonical default** for HA pre-regs that adopt the recovery-phase axis but don't specifically need within-LC sub-structure (per `lc_era_temporal_segmentation §1` Stratum 4 IS the primary analytic surface). HA pre-reg authors who want sub-structure escalate down to Tier B, Tier A, or no-collapse.
- **No-collapse (6-phase axis) is the canonical for descriptive work that specifically asks about within-LC clinical heterogeneity** (e.g. `recovery_arc` v2 per `lc_recovery_phase_axis §6.2`).
- Hard boundary applies in all cases regardless of tier.

Worked mixed-tier examples illustrating these collapse conditions in practice are at §3.5 (after the per-tier discipline subsections).

---

## 3. Per-tier discipline + binding rules

### 3.1 Tier A — within-pacing safe pool

**Pool**: sub-phases `pacing_pre_citalopram_learning` (4a; 2022-09-22 → 2022-11-17, 56 days) + `pacing_habit_established` (4b; 2022-11-17 → 2024-04-09, ~508 days) → phase 4 `pacing_pre_citalopram` (564 days). The pool re-creates the r1 working name of phase 4 *before* the §7b operationalisation interview split it into 4a + 4b at `lc_recovery_phase_axis.md` r2 lock 2026-06-19.

**Hypothesis-driven collapse conditions** (ANY of the three suffices):

1. **Hypothesis-shape insensitivity**: the hypothesis does NOT bind to within-phase-4 lived-experience habit-formation variation (e.g. a hypothesis testing cross-phase 3 ↔ 4 ↔ 5 dynamics, where the 4a/4b boundary is downstream of the structural question).
2. **n-adequacy**: per-sub-phase n is insufficient for the hypothesis's inferential goal. Sub-phase 4a is 56 days (per `lc_recovery_phase_axis §5.4` bullet 2 tight-n caveat); for hypotheses requiring per-phase bootstrap CIs at any reasonable width, the 4a cell is a binding constraint.
3. **Structural insensitivity to pacing-habit timing**: the hypothesis is about a construct that lived-experience pacing-habit timing should not affect (e.g. a Garmin-only sensor channel with no pacing-modulated mechanism).

**Default**: non-collapsed (use 4a + 4b as separate cells) is the default. Tier A collapse is the documented exception; the HA pre-reg's `§3 Data sources` block states which condition triggers the collapse + names the resulting pooled unit as "phase 4 `pacing_pre_citalopram` (4a+4b pooled)".

**Cross-citation**: `lc_recovery_phase_axis §3.4` parent definition + §3.4a / §3.4b sub-definitions.

### 3.2 Tier B — citalopram-corrected pool

**Pool**: phase 4 (or 4a + 4b separately under no-Tier-A) + phase 5 `citalopram_modulated` → unified pacing+medication era.

**Hypothesis-driven collapse conditions** (ANY of the three suffices):

1. **Channel not CONFIRMED-citalopram**: the channel is NOT in the v3-CONFIRMED set (`stress_mean_sleep` / `all_day_stress_avg` / `bb_lowest` per [`citalopram_dose_response_stress_mean_sleep §5.6`](citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14)). Non-CONFIRMED channels have no documented dose-response on this corpus, so the dose effect is not structurally bias-relevant to the cross-medication pooling.
2. **§5.A/B/C treatment applied**: the analysis explicitly applies one of [`citalopram_phase_stratification §5.A` (per-phase stratification)](citalopram_phase_stratification.md#5a-per-phase-stratification-the-default-lowest-risk), [`§5.B` (dose-adjusted predictor)](citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests), or [`§5.C` (per-mg full subtraction)](citalopram_phase_stratification.md#5c-joint-dose-and-phase-model-most-rigorous-highest-cost). The treatment removes the dose-driven structural bias by construction; pooling is then legitimate on the dose-corrected signal.
3. **Structural dose-insensitivity**: the hypothesis is structurally insensitive to dose effects (e.g. a correlation between two non-dose-modulated channels; a per-bout shape feature that doesn't load on the autonomic-load channels). The dose effect's presence on other channels in the dataset is then a red herring for the specific hypothesis.

**Channel-sensitivity rule (BINDING)**:

> A CONFIRMED-citalopram channel (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`) in a Tier B pool REQUIRES one of `citalopram_phase_stratification §5.A / §5.B / §5.C` treatment patterns. Pool-without-correction on these channels is a fire on this MD's discipline.

The audit hook is the same one already binding via `citalopram_phase_stratification §4` per-channel inheritance — Tier B does not add a new rule, it *names the place* where the rule applies. The HA pre-reg's `§3 Data sources` block (or methodology section) states which §5.A/B/C pattern is adopted and why; per the existing `citalopram_phase_stratification §6` pre-registration template.

**Cross-citation**: `citalopram_phase_stratification §3` (the 4-phase citalopram axis nested within phase 5) + §5 (the three treatment patterns) + `citalopram_dose_response_stress_mean_sleep §5.6` (the empirical β values that define CONFIRMED status).

### 3.3 Tier C — full LC pool (Stratum 4)

**Pool**: phase 3 `lc_pre_ergo` (~171 days) + phase 4 (with or without 4a/4b sub-split, or pooled per Tier A) + phase 5 `citalopram_modulated` (~787 days) → Stratum 4. This IS the data-given LC stratum per [`lc_era_temporal_segmentation §1`](lc_era_temporal_segmentation.md#1-data-given-strata-background-not-a-methodological-choice); Tier C is the **project-canonical default** in the strict sense — every HA pre-reg that does not adopt within-LC sub-structure is operating at Tier C by default.

**Hypothesis-driven collapse conditions** (ANY of the three suffices):

1. **LC-as-whole framing**: the hypothesis treats LC era as a unit (e.g. "Is `resting_hr` elevated in LC vs pre-illness baseline?"). Sub-structuring within LC is downstream of the structural question; Tier C is the right pool.
2. **Pre-LC vs LC contrast**: the hypothesis is about Stratum 1 (pre-illness) vs Stratum 4 (LC); by construction Tier C IS the analytic surface for the LC arm. (Stratum 2 acute infection is too short / categorically different and is held out per §2.4 hard boundary.)
3. **Pacing- and medication-onset structural insensitivity**: the hypothesis is about a construct that the lived-experience pacing-onset and medication-onset should not alter — Tier C pooling is then the parsimonious choice.

**Cross-citation**: `lc_era_temporal_segmentation §1` (data-given Stratum 4 definition) + `lc_recovery_phase_axis §1.3` (Stratum 4 IS the analytic surface for the recovery-phase axis).

**Tier C + Tier B interaction**: Tier C *includes* the Tier B pool (4+5 ⊂ 3+4+5). A Tier C analysis on a CONFIRMED-citalopram channel inherits the §5.A/B/C requirement transitively — the citalopram dose effect doesn't disappear when phase 3 is added to the pool. The Tier B channel-sensitivity rule binds at Tier C as well.

### 3.4 HARD BOUNDARY — never collapse phase 1 ↔ phase 2 ↔ LC era

**Pool**: phase 1 `pre_illness_healthy` (2021-08-16 → 2022-03-20, ~217 days) + phase 2 `acute_infection` (2022-03-21 → 2022-04-03, 14 days) + LC era (phases 3-5, 2022-04-04 → present).

**NEVER COLLAPSED.** These cross the data-given strata boundaries per [`lc_era_temporal_segmentation §1`](lc_era_temporal_segmentation.md#1-data-given-strata-background-not-a-methodological-choice). The strata are defined by clinical events (COVID infection 2022-03-21; LC start 2022-04-04 "Monday after Fietsweekend Ardennen") and represent **categorically distinct illness states**: pre-illness healthy / acute-viral / chronic-LC. Pooling across them mixes constructs (healthy autonomic regulation vs acute-viral disruption vs chronic LC patterns); the resulting pooled estimate is uninterpretable as a coherent quantity.

**No conditions exist that justify this collapse.** Cross-stratum analyses use the strata AS STRATA (Stratum 1 vs Stratum 4 contrast, Stratum 1 baseline reference, etc.), NEVER as a pool. This is consistent with `lc_era_temporal_segmentation §1`'s framing that the boundaries are data-given (not a methodological choice); the same logic applies to the pooling-non-availability — it is not a discipline choice, it is a category-error preventive.

**Cross-citation**: `lc_era_temporal_segmentation §1` (data-given strata) + `lc_era_temporal_segmentation §4` (anti-data-driven-boundary discipline, applied here in its dual: anti-pooling-across-data-given-strata).

### 3.5 Mixed-tier examples (illustrative, not exhaustive)

The conditions above can compose. The table below illustrates representative hypothesis-channel shapes and the recommended pooling; these are examples for orientation, not a per-HA pre-reg lookup.

| hypothesis shape | recommended pooling | tier mix |
|---|---|---|
| "Does `bb_overnight_gain` (non-CONFIRMED-citalopram) recover differently after crashes in unmedicated vs medicated LC?" | Pool 4a+4b → 4, then stratify 4 vs 5 | Tier A + no Tier B (cross-stratify, not collapse, on the medication dimension) |
| "Does `stress_mean_sleep` (CONFIRMED-citalopram) show a phase-4 habit-formation discontinuity at 2022-11-17?" | Use 4a vs 4b explicitly; phase 4 cannot collapse | No Tier A (testing the within-4 boundary itself) |
| "Is `resting_hr` Stratum-4-elevated vs pre-illness baseline?" | Pool 3+4a+4b+5 → Stratum 4; compare to phase 1 | Tier C; hard boundary respected by stratification (not pool) |
| "Does any HA-* test on `all_day_stress_avg` survive validate-era?" | Stratify 5 by `citalopram_phase` per §5.A; pool 4a+4b → 4 vs 5 (per §5.A within-phase reading) | Tier A + Tier B with §5.A correction |
| "Pre-illness vs LC era comparison on `bb_lowest`" | Stratum 1 vs Stratum 4 (Tier C); §5.B dose-adjustment on the Stratum 4 arm | Tier C + Tier B §5.B correction (CONFIRMED channel inside Stratum 4) |
| "Does within-night autonomic recovery shape differ across LC era?" | Use the 6-phase axis non-collapsed (or Tier A for n-adequacy) | No Tier B/C collapse (within-LC sub-structure IS the question) |

---

## 4. Alternatives considered

| label | proposal | verdict | reason |
|---|---|---|---|
| **(a)** | No conventions (status quo) — let each HA pre-reg + descriptive analysis make its own pooling decisions ad-hoc | rejected | Ad-hoc pooling decisions accumulate data-driven back-doors: when each consumer re-invents the discipline, the temptation to consult the data ("does the per-sub-phase median look different?") to decide whether to pool is corrosive. Conventions documented in advance prevent this drift. |
| **(b)** | Data-driven collapse allowed — adopt an empirical-invisibility test (e.g. "pool if the per-sub-phase channel medians are within tolerance ε") as the trigger | rejected per PM 2026-06-22 | The data-driven trigger violates [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) (data-peeking via the back door of "empirical invisibility") AND [`lc_era_temporal_segmentation §4`](lc_era_temporal_segmentation.md) (anti-data-driven-boundary-tuning). Even an empirical-invisibility test is a hypothesis evaluation on the same data; reusing it to decide pooling-then-test creates a self-confirming pipeline. Hypothesis-driven only is the disciplined choice. |
| **(c)** | Per-channel collapsibility rules (channel-specific tables defining allowed pools) | rejected | Over-specification. The channel-sensitivity question is already handled at the citalopram-channel level by `citalopram_phase_stratification §4-§5`; encoding per-channel collapsibility tables for every channel in the corpus duplicates that work for marginal benefit. HA pre-regs already declare channel + tier in their `§3 Data sources` block; the per-channel rule is implicit in the channel-sensitivity rule of Tier B. |
| **(d)** | Always-stratify (no collapse ever; the 6-phase axis is the only valid resolution) | rejected | Ignores legitimate cases where (i) per-sub-phase n is too short for the inferential goal (4a is 56 days), (ii) the hypothesis is structurally insensitive to the sub-phase distinction. Always-stratify forces tight CIs onto every analysis even when the structural question is at a coarser resolution; the cost is paid in power loss without an offsetting credibility gain. |
| **(e) — CHOSEN** | 3-tier hierarchy (A within-pacing / B citalopram-corrected / C full LC) + hard boundary (phases 1↔2↔LC era never pooled), with **hypothesis-driven only** collapse triggers | proposed | Honours `lc_era_temporal_segmentation §6` per-pre-reg warrant discipline (each tier's conditions are documented; the HA pre-reg justifies its tier choice in `§3 Data sources`); preserves `citalopram_phase_stratification §5` channel-sensitivity rule via Tier B binding; preserves the data-given hard boundary; eliminates data-driven back-doors via the hypothesis-driven only trigger; provides a citable canonical convention for HA pre-regs and descriptive analyses without over-specifying. |

---

## 5. Four-input reasoning

Per [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice), the four-input bar binds.

### 5.1 Best-practices standards

- **Pooling discipline in single-case stratified designs is hypothesis-driven by orthodoxy.** Per WWC 2022 SCED standards + SCRIBE 2016 (anchored via `CONVENTIONS §1.2`), phase-pooling decisions in single-subject longitudinal designs are pre-registered structural choices, not in-data-tuned. The standard requires (a) the analytic unit be operationally distinguishable; (b) pooling decisions be documented before any test runs; (c) the resulting estimates carry per-phase n + within-phase autocorrelation handling.
- **Anti-data-driven-boundary-tuning is the dual of anti-data-driven-pooling.** Per `lc_era_temporal_segmentation §4` + `citalopram_phase_stratification §3`, both prior MDs reject PELT / change-point detection in favor of event-anchored boundaries. The dual (rejecting data-driven *pooling*) follows from the same reasoning: an empirical-invisibility test (used to justify pooling) is itself a data-driven boundary decision in another form. This MD's hypothesis-driven only trigger preserves the discipline both MDs already adopted.
- **Per-channel inheritance via the dose-modulation framework is the established treatment** for the citalopram dimension. `citalopram_phase_stratification §4` + Daza 2018 (counterfactual framework for n-of-1 time-varying confounders, anchored via that MD's §1.3 + §5.B) supply the per-channel inheritance rules; this MD does not duplicate them, it names the place (Tier B) where they apply.

### 5.2 Established literature

**Inherited project-canonical anchors** (already fetched + cited upstream; not re-fetched here):

- `CONVENTIONS §1.2` — SCRIBE 2016, CENT 2015, STROBE 2007, WWC 2022, Natesan Batley 2023.
- `citalopram_phase_stratification §1.3` + §5.B — Daza 2018 *Methods Inf Med* counterfactual framework for time-varying confounders in n-of-1 self-tracked data.
- `lc_era_temporal_segmentation §5.1` — observational-cohort stratification orthodoxy (deferred-but-named honestly in that MD; the orthodoxy informs both the original strata + the pooling discipline derived from them).

**Deferred-but-named honestly**: a Daza-family follow-up or single-case meta-analytic review on pooling discipline specifically (vs the more common stratification literature) would tighten §5.2. Candidate fetch targets:

- Follow-ups to Daza 2018 *Methods Inf Med* on n-of-1 pooling-discipline (the 2018 paper covers covariate-adjustment; a follow-up specifically on phase-pool decisions would anchor this MD's hypothesis-driven trigger).
- WWC 2022 SCED standards Appendix on phase-pooling decisions (the Appendix may already cover the discipline; a focused re-read would confirm).

The methodological reasoning above does not depend on these landings; queue at `QUEUED-WORK.md` Tier 3 per `lc_recovery_phase_axis §8` open-followup pattern.

### 5.3 Our own vision on tradeoffs

| dimension | (a) no conventions | (b) data-driven trigger | (d) always-stratify | (e) CHOSEN — 3-tier + hard boundary, hypothesis-driven only |
|---|---|---|---|---|
| Risk of data-driven back-doors | high (each consumer re-invents discipline) | high (back-door is *built into* the trigger) | low (no pooling = no back-door) | low (hypothesis-driven trigger is structural, pre-data) |
| Compatibility with CONVENTIONS §4.2 (caveats vs a-priori) | mixed (ad-hoc per consumer) | violated (data-driven trigger leaks a-priori commitments) | aligned | aligned (collapse decisions are pre-data structural choices) |
| Compatibility with `lc_era_temporal_segmentation §4` (anti-data-driven-boundary) | mixed | violated (empirical-invisibility test IS data-driven boundary in another form) | aligned | aligned (the dual of anti-data-driven-boundary is anti-data-driven-pooling, here adopted) |
| Power preservation when sub-phase n is tight | varies by consumer | varies | none (forced stratification on 4a's 56 days = wide CIs always) | Tier A available with hypothesis-driven justification when 4a's n is structurally insufficient |
| Channel-sensitivity preservation on CONFIRMED-citalopram | varies by consumer | varies | trivially aligned (no pool) | aligned via Tier B channel-sensitivity rule (binding §5.A/B/C requirement) |
| Hard-boundary preservation (no cross-stratum pool) | varies by consumer | data-driven trigger could in principle pool 1+2+3 if their medians line up | aligned (no pool) | aligned (hard boundary is structural; no condition justifies the collapse) |
| Cross-HA comparability (do two pre-regs use the same pooling?) | low (each invents) | low (data-trigger varies by epoch) | high (one rule) | high (4 tier slots; each pre-reg names its tier) |
| Cost to HA pre-reg authors | low (no discipline) | low (mechanical trigger) | medium (no choice; forced fine resolution) | medium (one-line justification per tier choice in `§3 Data sources`) |

**Tradeoff summary**: the chosen position pays a small cost in HA-pre-reg-author overhead (one-line tier + justification) and gains data-driven-back-door immunity + cross-HA comparability + channel-sensitivity preservation. The hypothesis-driven trigger is the load-bearing choice; it ports the well-anchored anti-data-driven-boundary discipline (already in `lc_era_temporal_segmentation §4` for boundaries) to the dual question of pooling.

### 5.4 Our research limitations + objectives

- **n=1 single-subject design**: the hypothesis-driven discipline relies on the HA pre-reg author honestly classifying their hypothesis-channel pair. There is no third-party adjudication; the discipline is enforced via the audit hook (the `§3 Data sources` block must state the tier + justification, which a fresh-session reviewer can audit). For load-bearing project claims, the conventional audit pass + a reciprocal-cite to this MD is the protocol.
- **Some edge cases may not fit cleanly**: a hypothesis-channel pair that is partially Tier B (channel is CONFIRMED-citalopram) but structurally Tier C (pre-LC vs LC scope) requires the §5.B treatment applied to the LC arm only (per `citalopram_phase_stratification §5.B`'s zero-dose convention for pre-citalopram dates), AND the hard-boundary stratification of Stratum 1 vs Stratum 4. The mixed-tier example table (§2.5) covers this case; future edge cases should be flagged explicitly in the pre-reg + considered for a v2 amendment to this MD if a class of cases emerges.
- **Sub-phase 4a's tight n (56 days)** interacts directly with Tier A's n-adequacy condition. Per `lc_recovery_phase_axis §5.4` bullet 2, 4a's 56-day n widens IQR + bootstrap CIs by construction. Tier A's collapse-when-n-tight condition gives HA pre-regs a documented path to pool 4a + 4b when the hypothesis's inferential goal cannot tolerate the wide CIs; the path is documented (not ad-hoc) and pre-data (not post-hoc empirical-invisibility-driven).
- **Long-memory inheritance via the citalopram dimension**: per `lc_recovery_phase_axis §5.4` last bullet + §6.6 (block-aware bootstrap discipline), CONFIRMED-citalopram channels on long pools (Tier B or Tier C) inherit the long-memory structure surfaced in `recovery_arc/findings.md`. Pooling decisions interact with block-bootstrap E[L]\* choices: a Tier C pool on a CONFIRMED channel must run block-bootstrap with E[L]\* widened beyond the project default E[L]=7. The block-aware bootstrap discipline lives in `lc_recovery_phase_axis §6.6`; this MD doesn't duplicate it but flags the interaction.

**Objectives served**:

1. **Eliminate data-driven back-doors in pooling decisions** by anchoring the trigger to the hypothesis structure, not the data.
2. **Preserve the per-channel citalopram-correction discipline** via Tier B's binding §5.A/B/C requirement.
3. **Preserve the data-given hard boundary** via §3.4's never-pool rule.
4. **Provide cross-HA comparability** via the 4-tier slot vocabulary.
5. **Document the n-adequacy escape valve** (Tier A) without making it default; default remains no-collapse for descriptive work, Tier C for HA pre-regs that don't adopt within-LC sub-structure.

---

## 6. Operational consequences

### 6.1 HA pre-reg adoption pattern (opt-in, per `lc_era_temporal_segmentation §6`)

HA pre-regs that opt into the [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) 6-phase axis MUST declare in their `§3 Data sources` block:

- which **tier** they adopt (Tier A / Tier B / Tier C / no-collapse / mixed),
- the **hypothesis-driven condition** (one of §3.1.1-3 for Tier A, §3.2.1-3 for Tier B, §3.3.1-3 for Tier C) that triggers the collapse,
- for Tier B on a CONFIRMED-citalopram channel: which **§5.A/B/C treatment pattern** is applied + the `citalopram_phase_stratification §6` template reference,
- per [CONVENTIONS §3.6](../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file) named-counts discipline, the **n per tier-cell named explicitly** (e.g. "phase 4 = `pacing_pre_citalopram_learning` n_days=56 + `pacing_habit_established` n_days=508; pooled-Tier-A n_days=564"; or "Tier B pool n_days=1295 = phase 4 564 + phase 5 ~787"; or "Tier C pool n_days≈1466 = phase 3 171 + phase 4 564 + phase 5 ~787"). The per-tier n surfaces both the pooled cell and its components so reviewers can audit the pool's component n and the resulting analytic-unit n in one read.

HA pre-regs that do NOT opt into the recovery-phase axis (default per `lc_era_temporal_segmentation §3`) operate at Stratum 4 by inheritance from `lc_era_temporal_segmentation §1`; these pre-regs are unaffected by this MD.

### 6.2 Descriptive analysis adoption pattern

Descriptive analyses (Layer 1-3 per `CONVENTIONS §2.1` + `analyses/descriptive/README.md`) adopting the recovery-phase axis:

- **Tier C (full Stratum 4)** is the default for descriptive analyses that don't specifically need within-LC sub-structure (e.g. pre-LC vs LC contrasts).
- **No-collapse (6-phase)** is the default for descriptive analyses that DO ask about within-LC clinical heterogeneity (e.g. `recovery_arc` v2 per `lc_recovery_phase_axis §6.2`).
- **Tier A / Tier B** are opt-in with a one-line justification in the analysis's methodology block.

### 6.3 Inheritance from `citalopram_phase_stratification §5.A/B/C`

Tier B's channel-sensitivity rule binds without modification of the upstream MD. The per-channel inheritance table at `citalopram_phase_stratification §4` is the source-of-truth for which channels require correction; this MD inherits that table by reference. A CONFIRMED-citalopram channel pooled at Tier B without an §5.A/B/C treatment is a fire on `citalopram_phase_stratification §4` AND on this MD's §3.2 channel-sensitivity rule; either audit hook surfaces the fire.

### 6.4 Interaction with bout-level cascade

Bout-level HA pre-regs ([`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) + downstream HA11-bout-redo, HA-C4c, opportunistic A4 / C1 / C4b / H4) opt into the 6-phase recovery-phase axis from [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) **independently of** their cross-phase dose-handling choice (the bout-level MD's [§5.3](bout_level_recovery_dynamics.md) Approaches A / B / C: A = subtract-shift; B = per-bout dose covariate; C = stratify-and-meta-analyse). The two decisions are orthogonal: the recovery-axis opt-in selects the *phase stratification surface*; §5.3 Approach A/B/C selects the *per-bout dose-handling pattern at cross-phase scope*. When a bout-level HA opts INTO the recovery-phase axis, this MD's collapsibility tiers apply to its phase-stratified analyses (Tier B + the channel-sensitivity rule on CONFIRMED-citalopram channels still binds). The collapsibility conventions inherit through that opt-in:

- bout-level HA pre-regs that adopt this MD's recovery-phase axis declare tier per §6.1;
- bout-level features on CONFIRMED-citalopram channels (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`) at Tier B require the §5.A/B/C treatment per the channel-sensitivity rule;
- the [`bout_level_dose_response_calibration.md`](bout_level_dose_response_calibration.md) sub-MD's bout-level β values are the right β to use in §5.B treatment at bout-level (vs the daily-aggregate β in `citalopram_dose_response §5.6.1`).

### 6.5 Per-day master `recovery_phase` column impact

No new column added by this MD. The `recovery_phase` column queued at `lc_recovery_phase_axis §6.5` is sufficient — tier choices are pre-reg-level / analysis-level declarations, not row-level annotations. Queryability of the 6-phase axis is the column's existing role; pooling is a query / groupby choice on top of the column, not a column transformation.

### 6.6 Coverage of `lc_era_temporal_segmentation` operational consequences

This MD's tier vocabulary slots into `lc_era_temporal_segmentation §7` operational consequences without conflict:

- `§7.3` per-pre-reg stratification text — the default "Primary stratum: LC with gevoelscore + crash labels" corresponds to Tier C in this MD's vocabulary;
- `§7.6` as-of-date convention — applies to all tiers (the right-edge of Stratum 4 advances over time; tier choices don't alter this).

---

## 7. Status + lock-blocking gates

**r2 LOCKED 2026-06-22** per `CONVENTIONS §2.2 + §2.3` audit hooks + `hypothesis_lock_process.md §3.6` compression. Fresh-session audit completed 2026-06-22 ([`reviews/phase_axis_collapsibility_conventions-2026-06-22.md`](../reviews/phase_axis_collapsibility_conventions-2026-06-22.md) at commit `1f940ef`), verdict PASS-with-caveats. §3.6 compression applied because the four r2 absorbs are mechanical (no architectural shift; the 3-tier + hard-boundary structure preserved; no new claim; all 3 user-locked decisions honored).

### 7.1 Lock-blocking gates (the lock-commit message MUST confirm each)

1. **Four-input bar surfaced** (CONVENTIONS §2.2): all four §5 inputs visibly addressed (best-practices standards, established literature, tradeoff vision, research limitations + objectives).
2. **All 3 tiers + hard boundary documented with conditions**: each of §3.1 (Tier A), §3.2 (Tier B), §3.3 (Tier C), §3.4 (hard boundary) has explicit collapse conditions / never-pool justification.
3. **Cross-axis inheritance from `citalopram_phase_stratification §5.A/B/C` documented**: Tier B's channel-sensitivity rule binds the §5.A/B/C requirement on CONFIRMED-citalopram channels.
4. **Cross-citation to `lc_recovery_phase_axis.md` + `lc_era_temporal_segmentation.md`** (reciprocal-cite paragraphs added to those MDs at lock-commit per the lock-time pattern from `d47e0d3`).
5. **`audit_for_publication.py` clean** (CONVENTIONS §2.3) at the lock-commit.

### 7.2 Hard discipline rules for THIS session (r1 drafter) — *honored at r1 commit; preserved as historical record for reference at lock-time*

- **End at r1 + commit. Do NOT self-audit.** Fresh-session reviewer reads cold per CONVENTIONS §1.2 reviewer-mode-with-authorization fresh-session discipline.
- **Do NOT lock in this session.** Lock requires the audit output to land first, in a separate drafter session.
- **Do NOT modify cross-reference MDs** (`lc_recovery_phase_axis.md`, `citalopram_phase_stratification.md`, `lc_era_temporal_segmentation.md`, `citalopram_dose_response_stress_mean_sleep.md`). Reciprocal-cite paragraphs are lock-time edits.
- **Do NOT pre-author what the audit should find.** The producer documents reasoning honestly + lets the four-input bar speak for itself; the auditor finds the fires.
- **Do NOT relitigate user-confirmed decisions.** Hypothesis-driven only collapse trigger (PM-confirmed 2026-06-22) + new MD location (not v2 of `lc_recovery_phase_axis.md`) are locked inputs.

---

## 8. Open follow-ups

1. **Reciprocal-cite paragraph in `lc_recovery_phase_axis.md`** — **LANDED 2026-06-22 at this lock-commit** as §6.7 "Collapsibility position", pointing at this MD's §3 hierarchy + §3.2 channel-sensitivity rule.
2. **Reciprocal-cite paragraph in `lc_era_temporal_segmentation.md` §1** — **LANDED 2026-06-22 at this lock-commit** as a new paragraph after the existing "Sub-segmentation position", pointing at this MD's §3.4 hard-boundary discipline as the dual of the data-given strata.
3. **Reciprocal-cite paragraph in `citalopram_phase_stratification.md` §5** — queued for separate session (optional cross-ref; not lock-blocking). Will point at this MD's Tier B as the consumer of the §5.A/B/C patterns.
4. **STOCKTAKE.md entry** — queued for separate session per `STOCKTAKE.md §8` trigger "New methodology MD locked". Includes §5 methodology structural map + §6 synthesis + §8 revision log refresh.
5. **`descriptive/README.md §5` index entry** — queued for separate session; adds this MD to the methodology-MD index alongside `lc_recovery_phase_axis.md` + `citalopram_phase_stratification.md`.
6. **HA-pre-reg authoring template update in `hypothesis_lock_process.md §3.2.4`** (queued if the discipline matures into a project-canonical pattern across ≥2 HA pre-regs) — adding a default-text line for the tier declaration in `§3 Data sources`.
7. **Literature fetch for the deferred-but-named §5.2 candidates** (Daza-family pooling-discipline follow-up; WWC 2022 SCED Appendix on phase-pooling) — queue at `QUEUED-WORK.md` Tier 3. On landing, r2 absorbs at §5.2 via `hypothesis_lock_process.md §3.6` mechanical compression.
8. **v2 amendment trigger**: if a new class of edge-case hypothesis-channel pairs emerges that doesn't fit cleanly into the 4-tier slot vocabulary, a v2 amendment expands the hierarchy. Documented here so the audit hook is visible.

---

## 9. Cross-references

- [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) — the 6-phase axis this MD governs (r2 LOCKED 2026-06-19 `d47e0d3`); §1.3 three-layer position; §3 per-phase warrants; §5.4 limitations (4a tight-n, long-memory inheritance); §6.5 `recovery_phase` column; §6.6 block-aware bootstrap discipline; §8 open follow-ups pattern.
- [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md) — §1 data-given strata (source of the §3.4 hard boundary); §4 anti-data-driven-boundary discipline (dual of this MD's anti-data-driven-pooling); §6 sub-boundary criteria (opt-in pattern inherited); §7.6 as-of-date convention.
- [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md) — §3 the four-phase citalopram axis (nested within phase 5); §4 per-channel inheritance (binding via §3.2 channel-sensitivity rule); §5.A/B/C the three treatment patterns (Tier B inheritance source); §6 pre-registration template.
- [`citalopram_dose_response_stress_mean_sleep.md`](citalopram_dose_response_stress_mean_sleep.md) — §5.6 the CONFIRMED-citalopram channel list (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`) used in Tier B channel-sensitivity rule.
- [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) — downstream consumer (§6.4 interaction).
- [`bout_level_dose_response_calibration.md`](bout_level_dose_response_calibration.md) — bout-level β source for §5.B treatment at bout-level resolution.
- [`hypothesis_lock_process.md §1`](hypothesis_lock_process.md) — methodology MD carve-out (this MD governed by CONVENTIONS §2.2 + §2.3, not the HA lock process).
- [`CONVENTIONS.md`](../CONVENTIONS.md) §1.1 (producer-mode discipline), §2.1 (descriptive-before-inference), §2.2 (four-input bar), §2.3 (audit before push), §3.6 (named counts), §4.2 (caveats vs a-priori), §4.3 (prior-driven hypotheses are confirmatory).
- [`STOCKTAKE.md`](../STOCKTAKE.md) — refresh trigger at lock-commit.
- [`descriptive/README.md`](../analyses/descriptive/README.md) — §5 methodology-MD index (lock-time addition).

---

*Drafted 2026-06-22 by Claude (Opus 4.7) in producer-mode under user authorisation. r1 drafted in fresh session 2026-06-22 (commit `1282d9b`); fresh-session methodology audit by independent session 2026-06-22 (commit `1f940ef`; verdict PASS-with-caveats; §3.6 compression eligible). r2 absorbs + LOCK by separate drafter session 2026-06-22.*
