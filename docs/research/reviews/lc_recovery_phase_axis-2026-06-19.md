# Review: LC recovery-phase axis methodology MD (lc_recovery_phase_axis)

**Target**: [`docs/research/methodology/lc_recovery_phase_axis.md`](../methodology/lc_recovery_phase_axis.md) (r1, untracked).
**§7b operationalisation block**: captured in handoff §2.2 (locked 2026-06-19 user session); audited alongside MD body.
**Reviewer mode**: Claude (independent peer reviewer per [CONVENTIONS §1.2](../CONVENTIONS.md) + §2.2). *Fresh session — no exposure to the drafting context; doc-only knowledge.*
**Review date**: 2026-06-19.

---

## 1. What the MD proposes

The MD specifies a 3-layer phase-axis architecture for the corpus: an outer data-given stratification inherited verbatim from [`lc_era_temporal_segmentation.md §1`](../methodology/lc_era_temporal_segmentation.md), a **new middle "LC recovery-phase" axis** sub-segmenting the LC era into 5 phases (or 6 if §7b unlocks a sub-boundary), and an orthogonal inner citalopram dose-state axis nested within phase 5 per [`citalopram_phase_stratification.md §3`](../methodology/citalopram_phase_stratification.md). Phases 1 (`pre_illness_healthy`) and 2 (`acute_infection`) inherit verbatim from the data-given outer axis; phases 3 (`lc_pre_ergo`) and 4 (`pacing_pre_citalopram`) are new M1 lived-experience warrants anchored to documented intervention dates; phase 5 (`citalopram_modulated`) is an M2 documented-confounder warrant anchored to the v3 multi-channel dose-response in [`citalopram_dose_response_stress_mean_sleep.md §5.6`](../methodology/citalopram_dose_response_stress_mean_sleep.md). The MD becomes the default substrate for descriptive work where phase stratification is informative, and is opt-in for HA pre-regs per the [`lc_era_temporal_segmentation §6`](../methodology/lc_era_temporal_segmentation.md) sub-boundary criteria. The §7b operationalisation interview (locked 2026-06-19 in a separate user session) adds a within-phase-4 sub-boundary `pacing_habit_established` at **2022-09-22 + 56 days = 2022-11-17** under an M1 lived-experience warrant ("8 weeks of ergotherapy where I learned the basic principles and got into the habit"). The MD includes a §6.1 recommendation to compute both [`citalopram_phase_stratification §5.A`](../methodology/citalopram_phase_stratification.md) (per-phase stratification) and §5.B (dose-adjusted predictor) as parallel sensitivity rows for any phase-5 cell on a CONFIRMED-citalopram channel.

The empirical claim is descriptive: this axis is the substrate, not a hypothesis test. The interpretive claim is that lived-experience + intervention-evidence sub-segmentation of the LC era is a defensible default frame for descriptive analyses where the within-LC heterogeneity is the substantive question — which the recovery_arc v1 four-phase axis at [`analyses/descriptive/trajectory/recovery_arc/findings.md`](../analyses/descriptive/trajectory/recovery_arc/findings.md) confirms is informative (the four-channel acute-infection + LC-pre-gevoelscore + Stratum-4 medians are distinct across the corpus). The §7b operationalisation falsifiability hook is honestly Layer 1: "the 8-week boundary's discriminative power on per-sub-phase channel medians is itself testable in descriptive Layer 1 (recovery_arc v2 sensitivity arm)".

---

## 2. What fired and why

### Layer 1 — Four-input bar (inherits from [CONVENTIONS §2.2](../CONVENTIONS.md))

**L1.1 Best-practices standards — pass with one minor observation.** §5.1 names four standards (SCED stratification orthodoxy via WWC 2022 / SCRIBE 2016 / Natesan Batley 2023; time-varying-confounder framework via Daza 2018; event-anchored-not-data-driven principle inherited from [`lc_era_temporal_segmentation §4`](../methodology/lc_era_temporal_segmentation.md) + [`citalopram_phase_stratification §3`](../methodology/citalopram_phase_stratification.md); per-segment-warrant requirement from [`lc_era_temporal_segmentation §6`](../methodology/lc_era_temporal_segmentation.md)). Each citation names the criterion it imposes. **Minor observation, not a fire**: the §7b operationalisation 8-week sub-boundary at 2022-11-17 is **duration-based** (56 days post-ergo-start), not event-anchored to a documented external event on that date. The MD's standards-row asserts the event-anchored-not-data-driven principle as universal; the M1 warrant for §7b is lived-experience-anchored ("after 8 weeks, pacing got into a rhythm"), which the [`lc_era_temporal_segmentation §2`](../methodology/lc_era_temporal_segmentation.md) M1 class explicitly admits, but the principle-as-stated in §5.1 ("phase boundaries should be event-anchored, not data-driven") does not visibly carve out lived-experience-anchoring as a distinct sub-case. The r2 absorb should clarify that M1 lived-experience boundaries are event-anchored to *the lived report itself*, not to an external date-stamped event — i.e. the §7b 2022-11-17 boundary is M1-defensible but reads as duration-based on first read.

**L1.2 Established literature — pass.** §5.2 cleanly downgrades ME/CFS-specific anchors (Goudsmit 2012, Davis 2021, Larun 2017) to "deferred-but-named" per the [CONVENTIONS §2.2](../CONVENTIONS.md) deferred-honesty pattern. The framework reasoning does not depend on them. Inherited project-canonical anchors (Daza 2018, SCED standards) are appropriately scoped via the citing methodology MDs.

**L1.3 Tradeoffs — pass with strong evidence.** §5.3 surfaces the tradeoff as an 8-row × 5-column comparison table covering five dimensions of analytical risk + structural coverage across four alternatives. The trade-off summary explicitly names the complexity-vs-fidelity dimension being weighted. This is the strongest §5.3 in the methodology folder reviewed today.

**L1.4 Research limitations + objectives — fire (one substantive omission, see L4.1 below).** §5.4 enumerates five honest limits (n=1, uneven per-phase durations, fuzzy §7b boundary, 2024-04 collision, afbouw in-progress). The omission is that §5.4 does NOT name the long-memory implication for phase-stratified bootstrap CIs that the recovery_arc v1 findings already surfaced (6/7 Stratum-4 cells fire factor-of-2 E[L]\* flag per [`recovery_arc/findings.md §2`](../analyses/descriptive/trajectory/recovery_arc/findings.md) + the related caveat §5.10). This is the highest-priority residual on the MD; full treatment under L4.1.

### Layer 2 — Cross-axis consistency

**L2.1 + L2.2 — pass.** §1.3's 3-layer axis architecture accurately describes the nesting; phases 1 + 2 are inherited verbatim from [`lc_era_temporal_segmentation §1`](../methodology/lc_era_temporal_segmentation.md) (pre_corona 2021-08-16 → 2022-03-20; corona_infection 2022-03-21 → 2022-04-03). Boundary dates match side-by-side.

**L2.3 — pass.** §3.5 phase-5 M2 warrant cites β values that match [`citalopram_dose_response_stress_mean_sleep §5.6`](../methodology/citalopram_dose_response_stress_mean_sleep.md) verbatim: `stress_mean_sleep` β=+0.43/mg p=0.001, `all_day_stress_avg` β=+0.57/mg p=0.000, `bb_lowest` β=−1.13/mg p=0.000. Cross-referenced to the v3 multi-channel run on three CONFIRMED channels per the same source.

**L2.4 — pass.** Phase-4 left boundary 2022-09-22 (ergotherapie start) + phase-4 right boundary 2024-04-09 (citalopram buildup start) match [`intervention_effects_descriptive §3`](../methodology/intervention_effects_descriptive.md) + [`intervention_effects §2`](../methodology/intervention_effects_descriptive.md) tables. Ergo end ~2022-12-22 is appropriately described as approximate and as an event-overlay inside phase 4, not a phase boundary.

**L2.5 — pass.** §3.6 2024-04 boundary-collision treatment matches [`intervention_effects §8.1`](../methodology/intervention_effects_descriptive.md) + §8.3: 7-day proximity, structurally unanalyzable in the pre-vs-post window design, route to ITS-or-matched-window per §8.3. The MD honestly does not attempt to disentangle.

**L2.6 + side observation — substantive minor fire on phase-5 afbouw sub-axis endpoint.** §2 note on phase-5 sub-axis says "`afbouw` 2026-03-20 → 2026-06-04, ~76 days; `post_afbouw` 2026-06-05 → present but currently empty in the corpus". §3.5 sub-axis paragraph repeats: "post-afbouw begins 2026-06-05". The canonical inner-axis source-of-truth [`citalopram_phase_stratification §3`](../methodology/citalopram_phase_stratification.md) defines `afbouw` as `[2026-03-20, 2026-06-05]` (78 days, inclusive) and the `citalopram_phase()` Python function returns `"afbouw"` for `d < date(2026, 6, 6)` and `"post_afbouw"` for `d >= 2026-06-06`. This MD therefore introduces a **one-day off-by-one against the inner-axis source-of-truth** at the afbouw / post-afbouw boundary. The MD conflates "corpus end is 2026-06-04" (which is correct per [STOCKTAKE §1](../STOCKTAKE.md)) with "post-afbouw begins 2026-06-05" (which contradicts [`citalopram_phase_stratification §3`](../methodology/citalopram_phase_stratification.md) where post-afbouw begins 2026-06-06). Either the inner-axis MD is wrong (lock-blocking gate §7.1 criterion 4 reciprocal-citation work would surface it) or this MD's r2 should align to 2026-06-06. Mechanical fix; minor magnitude (out-of-corpus phase has zero rows either way).

**L2.6 garmin_pacing_practice §2 Origins cross-check — pass.** [`garmin_pacing_practice §2`](../methodology/garmin_pacing_practice.md) frames the pacing protocol as "emerged and evolved over time" with no sharp transition. The §7b 8-week M1 warrant ("8 weeks of ergotherapy where I learned the basic principles and got into the habit; gradual improvement during this window" + "After 8 weeks, pacing got into a rhythm") is internally consistent with that framing — the boundary is a *threshold of habit-establishment*, not a *moment of transition*. The `pacing_habit_established` naming is more precise than the MD r1 working name `pacing_effective` because the user explicitly flagged "still mediated in effectiveness by outside forces, but the overall habit was established". The naming rename is correct; the absorb is mechanical.

### Layer 3 — Operationalisation integrity

**L3.1 — pass.** Each new phase (3, 4, 5) has a §3 entry with warrant class + warrant body + boundary endpoints + per-test usage hint. The §7b sub-phases (4a `pacing_pre_citalopram_learning` + 4b `pacing_habit_established`) carry M1 lived-experience warrants in the handoff §2.2 operationalisation block. All five new warrants are stated; none are auto-inherited.

**L3.2 — pass with the M1 lived-experience qualifier flagged at L1.1.** Phase 3 right (2022-09-22), phase 4 right (2024-04-09), phase 5 left (2024-04-09), and phase 5 right (2026-06-04) are all event-anchored to documented dates in canonical source MDs. The §7b sub-boundary at 2022-11-17 is duration-based (56 days post-ergo-start); this is M1-defensible per [`lc_era_temporal_segmentation §2`](../methodology/lc_era_temporal_segmentation.md) ("a specific hypothesis predicts a change-point" where the hypothesis is the user's lived-experience report), but the r2 absorb should flag this distinction explicitly so a future reader doesn't read the boundary as data-driven on first pass.

**L3.3 — pass.** §6.1 "both §5.A and §5.B as parallel sensitivity rows" is faithful to the [`citalopram_phase_stratification §5`](../methodology/citalopram_phase_stratification.md) treatment patterns. §5.A applies at the inner-axis level (per-citalopram-phase cells within phase 5); §5.B applies at the channel level (dose-adjusted predictor on the CONFIRMED channels). Parallel computation surfaces concordance-or-divergence as the substantive descriptive finding per the MD's framing. **Side observation**: the §6.1 paragraph could read more clearly if it stated explicitly that §5.A here means *per-citalopram-phase stratification inside phase 5*, not per-recovery-phase (which is implicit but not stated). Minor; r2 wording.

**L3.4 — pass.** §6.4 HA opt-in pattern reads cleanly against [`lc_era_temporal_segmentation §6`](../methodology/lc_era_temporal_segmentation.md) — per-pre-reg warrant statement + this MD's §3 supplies the warrant text for the cited phase. The worked example (HA on `bb_lowest` across `pacing_pre_citalopram` vs `citalopram_modulated` citing §3.5 M2 warrant) is concrete.

**L3.5 §7b operationalisation block — pass.** The 8-week rule is justifiable as M1 lived-experience warrant (the user's report names the duration explicitly). The `pacing_habit_established` naming is honest (does not overclaim effectiveness; explicitly defers to "still mediated in effectiveness by outside forces"). The falsifiability hook ("the 8-week boundary's discriminative power on per-sub-phase channel medians is itself testable in descriptive Layer 1 (recovery_arc v2 sensitivity arm)") is honestly Layer 1 — no causal claim, only descriptive distinguishability. **One observation, not a fire**: the falsifiability hook frames testability via recovery_arc v2 (a descriptive analysis), which means a "fails to discriminate" finding in recovery_arc v2 would invite a §7b re-interview / sub-boundary withdrawal. The hook honestly admits a revision path without committing to one — appropriate for Layer 1.

### Layer 4 — Project-specific audit hooks (inherits from [CONVENTIONS §3, §4](../CONVENTIONS.md))

**L4.1 — substantive fire (highest priority).** §5.4 does NOT name the long-memory implication that the recovery_arc v1 landing already surfaced. Per [`recovery_arc/findings.md §2.1-§2.7`](../analyses/descriptive/trajectory/recovery_arc/findings.md) and §5.10 caveat, **6 of 7 Stratum-4 cells fire the factor-of-2 E[L]\* flag** (E[L]\* in {12.6, 15.1, 18.2 [implied by M=18], 21.1, 29.2, 29.8}) — meaning the per-day autocorrelation length in Stratum 4 is 2-4× the project default E[L]=7. Phase-stratified bootstrap CIs on this MD's phases 4 (~564 days) and 5 (~787 days) inherit this long-memory regime, and iid bootstrap CIs would systematically under-cover. §6 operational consequences prescribe "median + IQR + bootstrap CI per phase × channel" without specifying that the bootstrap MUST be block-aware at the per-phase E[L]\* per the [`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md) discipline (which is cited from recovery_arc/findings.md §2 and elsewhere). The MD's §5.4 should name this and §6 should prescribe the block-bootstrap discipline. This is the single highest-leverage residual on the MD; closure is a one-paragraph §5.4 addition + a one-sentence §6.1 / §6.2 prescription.

**L4.2 — minor fire (CONVENTIONS §3.6 named-counts discipline).** The MD §2 table reports durations in days (~217, 14, ~171, ~564, ~787) without naming the count triplet (scheme + unit + source file) per [CONVENTIONS §3.6](../CONVENTIONS.md). The §3 per-phase entries also do not state per-phase n explicitly. The recovery_arc/findings.md per-channel × per-phase table is the canonical answer (n in `per_day_master.csv` is given per cell). r2 absorb opportunity: add an n column to the §2 table sourced from `per_day_master.csv` row counts per phase, or add a per-phase n line to each §3 entry. Magnitude minor; the duration-in-days is a reasonable proxy and the cross-ref to recovery_arc surfaces the n; but the §3.6 phrasing convention is not yet honored.

**L4.3 — pass.** §1.1 + §1.2 are unambiguous about descriptive-substrate-not-hypothesis. §7b falsifiability hook is honestly Layer 1 (descriptive distinguishability, not causal claim). §6 operational consequences prescribe adoption patterns without pre-committing any downstream test's verdict. The MD is clean against [CONVENTIONS §4.2](../CONVENTIONS.md) caveats-vs-apriori discipline.

**L4.4 — pass.** No SUPPORTED / REJECTED marks anywhere in the MD. §6 prescribes adoption patterns descriptively without pre-committing verdicts.

---

## 3. What does not fire (selective)

- **§5.3 trade-off table is the strongest in the methodology folder.** 8 rows × 5 columns covering five dimensions of analytical risk + two of structural coverage across four alternatives. The "complexity cost vs descriptive-substrate fidelity" tradeoff is named explicitly. Non-trivial pass on a layer that routinely under-delivers in producer-mode MDs.

- **§4 alternatives table.** Six alternatives (a-f) named-and-judged with one-sentence rationale each. The PELT / change-point rejection in (c) cites the same circular-self-confirmation reasoning as the citalopram MD's parallel rejection — internally coherent across the methodology family. The (e) one-phase-per-intervention rejection is honest about the 2024-04 collision making intervention-driven axes structurally unworkable.

- **2024-04 boundary-collision (§3.6) handled honestly.** The MD does not attempt to disentangle CPAP-end from citalopram-start. Routes to the right downstream method per [`intervention_effects §8.3`](../methodology/intervention_effects_descriptive.md) (ITS or matched-window) without committing to it. The 7-day-window-tail caveat is correctly scoped to phase 4's right edge.

- **Authorship block + lock-blocking gate enumeration (§7.1) cleanly separated.** §7.1's five lock-blocking criteria are concretely scoped + each criterion's r1 status is named. The hard discipline rules (§7.2) correctly prohibit self-audit + pre-authoring §7b — which is exactly the discipline that produced this fresh-session review under [CONVENTIONS §1.2](../CONVENTIONS.md).

- **§7b operationalisation block (handoff §2.2) reads clean against the M1 discipline.** Lived-experience warrant is direct quote; the naming rename `pacing_effective → pacing_habit_established` was user-driven for precision; the falsifiability hook is Layer-1-honest. The interview-completed-in-separate-session discipline preserves the [CONVENTIONS §1.2](../CONVENTIONS.md) reviewer-mode-with-authorization peer-review check at the session-context level (here applied to a methodology MD's operationalisation gate rather than a hypothesis pre-reg lock arc).

---

## 4. What would strengthen this MD

Concrete, named, ordered by leverage:

1. **§5.4 add a long-memory bullet** (closes L4.1). Suggested wording: *"Long memory in Stratum 4 (recovery_arc v1 finding: 6/7 channels fire factor-of-2 E[L]\* flag; per-phase E[L]\* in [12, 30] vs project default 7). Any phase-stratified bootstrap CI on phases 4 + 5 MUST use block-bootstrap at the per-phase E[L]\* per [`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md); iid bootstrap CIs would systematically under-cover."* — and add a one-sentence corresponding requirement to §6.1 / §6.2.

2. **§7b absorb mechanical — propagate `pacing_pre_citalopram_learning` + `pacing_habit_established`** through §2 table, §2.1 `lc_recovery_phase()` helper, §3.4 phase 4 warrant, §3 add a §3.4b sub-section. The §7b operationalisation block in handoff §2.2 carries the locked output verbatim — drop it into §3.4b under "Phase 4 sub-boundary (added 2026-06-19 per §7b operationalisation interview)" and update §2.1 helper to return `"pacing_pre_citalopram_learning"` for `2022-09-22 <= d < 2022-11-17` and `"pacing_habit_established"` for `2022-11-17 <= d < 2024-04-09`. Resolves §7.1 criterion 3 + §7.1 criterion 2 simultaneously for phase 4b.

3. **§5.1 + §3.4b clarify that M1 lived-experience boundaries are event-anchored to the lived report** (closes L1.1 / L3.2 observations). Suggested wording: *"M1 lived-experience boundaries are event-anchored to the lived-experience report itself (per [`lc_era_temporal_segmentation §2`](../methodology/lc_era_temporal_segmentation.md) M1 class); the date is calculated from a documented anchor event + a duration named in the lived report. Distinct from data-driven boundaries (PELT / change-point on the channel under test) which the project rejects."*

4. **§3 / §2 table add per-phase n** (closes L4.2). One column per phase with day-level row count from `per_day_master.csv`; the recovery_arc/findings.md per-channel × per-phase n's can be cited as the source.

5. **§2 + §3.5 fix afbouw / post-afbouw boundary off-by-one** (closes L2.6 minor fire). Either update this MD to align with [`citalopram_phase_stratification §3`](../methodology/citalopram_phase_stratification.md) (`post_afbouw` begins 2026-06-06), OR audit-trail the divergence as a deliberate one-day reframe in this MD's §2 note. Note that the citalopram MD's `citalopram_phase()` Python function returns `"afbouw"` for `d < date(2026, 6, 6)` — i.e. afbouw is `[2026-03-20, 2026-06-05]` inclusive. The corpus end is 2026-06-04 (no post-afbouw data exists either way; the boundary is naming-only at present).

6. **§6.1 wording clarification** (minor L3.3 polish). State explicitly that "§5.A" here means *per-citalopram-phase stratification inside phase 5*, not per-recovery-phase, so a reader who lands on §6.1 without §1.3 context doesn't misread.

7. **§7.1 criterion 4 reciprocal citation queue** is already named at lock-time. When this MD locks, [`citalopram_phase_stratification.md`](../methodology/citalopram_phase_stratification.md) and [`lc_era_temporal_segmentation.md`](../methodology/lc_era_temporal_segmentation.md) should cross-link back to this MD's recovery-phase-axis layer. Standard lock-time edit.

---

## 5. Verdict

**PASS-with-caveats** — the highest-priority residual is L4.1 (the long-memory implication for phase-stratified bootstrap CIs that recovery_arc v1 already surfaced is missing from §5.4 / §6); seven concrete strengthening items are mechanical r2 absorb work, all compatible with lock after r2 + the queued reciprocal-citation lock-time edits. The MD's framework reasoning, cross-axis nesting, per-phase warrant discipline, §5.3 tradeoff surface, §7b operationalisation, and Layer 4 framing-discipline checks are all clean. No blocking architectural fires; the §7b operationalisation gate (§7.1 criterion 3) is cleared by the handoff §2.2 locked output, and the remaining lock-blocking gates are mechanical to confirm in r2.

---

## Methodology

This review walks the 4-layer audit framework defined in this session's handoff
([`session-lc-recovery-phase-axis-methodology-audit-handoff-2026-06-19.md`](file:///C:/Users/Gebruiker/.claude/plans/session-lc-recovery-phase-axis-methodology-audit-handoff-2026-06-19.md)),
adapted from [`reviews/README.md`](README.md) for the methodology-MD case
per [CONVENTIONS §2.2](../CONVENTIONS.md) four-input bar discipline.

Project-specific audit hooks from [CONVENTIONS §3 + §4](../CONVENTIONS.md);
methodology-MD lock framework from
[`hypothesis_lock_process.md §0`](../methodology/hypothesis_lock_process.md)
(carve-out: methodology MDs are governed by CONVENTIONS §2.2 + §2.3, not the
HA lock process).

Cross-references read cold for this audit: [`lc_era_temporal_segmentation.md`](../methodology/lc_era_temporal_segmentation.md), [`citalopram_phase_stratification.md`](../methodology/citalopram_phase_stratification.md), [`intervention_effects_descriptive.md`](../methodology/intervention_effects_descriptive.md), [`garmin_pacing_practice.md`](../methodology/garmin_pacing_practice.md), [`citalopram_dose_response_stress_mean_sleep.md`](../methodology/citalopram_dose_response_stress_mean_sleep.md) §5.6, [`STOCKTAKE.md`](../STOCKTAKE.md) §1, [`recovery_arc/findings.md`](../analyses/descriptive/trajectory/recovery_arc/findings.md), [`reviews/README.md`](README.md), and [CONVENTIONS.md](../CONVENTIONS.md) §1.1-§1.2 / §2.1-§2.3 / §3 / §4.
