# HA-C3 v2 — interpretation (Stage I)

**Status**: **LOCKED r1 by user acceptance 2026-06-25** per §11 step 10 Phase A.7. Drafted 2026-06-25 by `/research-interpret interpret HA-C3` skill in dry-run dispatch per §11 step 8 (skill since LOCKED r4). Phase A.1 §4.6 null prior recorded (user verbatim "I did not know what to expect. I was not aware of any pattern myself."); A.7 user-acceptance lock event closes Phase A. **First LOCKED Stage I interpretation of the layer.** Awaiting fresh-session `/research-review` per locked-plan §4 row for reviewer-mode-with-authorization artefacts (review queued for Phase A post-lock per established Option-γ pattern).

## Authorship

Drafted 2026-06-25 by Claude (Opus 4.7, 1M context) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../CONVENTIONS.md#12-producer-vs-reviewer-mode), via the `/research-interpret interpret HA-C3` skill invocation in §11 step 8 dry-run dispatch. Authorising user: Willem (dry-run framing — user reviews artefact post-session). Fresh-session `/research-review` peer-check required before LOCK per [`_plan_results_analysis_layer.md`](../../methodology/_plan_results_analysis_layer.md) §4 row for `interpretation.md`.

---

## 1. Target HA + verdict

- **HA ID**: HA-C3 v2 r2
- **Pre-reg lock date**: 2026-06-23 (commit `2a0b0df`)
- **Result lock date**: 2026-06-23
- **Stage D audit lock date**: 2026-06-25 (DRAFT r1, dry-run, pending user acceptance)
- **Headline verdict from `result.md`** (verbatim, no relabeling): **REJECTED (wrong-direction override)**
- **Stage D verdict-trust call** (verbatim from `descriptive_audit.md` §4): **TRUSTED**
- **Operationalisation summary** (one sentence, copying pre-reg §4): same-day `all_day_stress_avg × gevoelscore` cross-day-aggregate dose-response shape test on Stratum 4 unmedicated cell, binned at Wiggers-verbatim 4-bin scheme (`[0,30), [30,40), [40,60), [60,100]`) with pre-committed §7.3 halt-option-A absorber that fired at dry-run (B4 [60,100] n=1 absorbed into B3' [40,100]; 3-bin reduction), 3-condition gated verdict per §5.1.
- **Synthesis-structure map cluster**: [C-stress-fatigue-shape](../../methodology/synthesis_structure_map.md#3-cluster-table-s%E2%82%81-pre-registration) (per map r3 §3 cluster row, declared 2026-06-23). Sister HA in cluster: HA-C3p.

## 2. What the data shows

Descriptive paraphrase, no claim language per CONVENTIONS §4.1.

Primary unmedicated pool n=581; stress median 34.00; gevoelscore median 4.00. Original 4-bin descriptive (pre-§7.3 absorption): B1[0,30) n=95 bin-mean=3.958; B2[30,40) n=385 bin-mean=4.265; B3[40,60) n=100 bin-mean=3.860; B4[60,100] n=1 bin-mean=1.000. §7.3 halt-option-A fired as pre-committed (B4 underpower → absorbed into B3). 3-bin reduction descriptive (post-absorption): B1[0,30) n=95 mean=3.958; B2[30,40) n=385 mean=4.265; B3'[40,100] n=101 mean=3.832.

Three-condition test results: Jonckheere-Terpstra J*=+0.481, one-sided block-permutation p=0.6742 (n.s.; the J* sign is positive, which under this test's coding indicates a non-monotone-decreasing trend — i.e., the trend test does not detect the predicted monotone decrease). Convexity second-difference S = m_3 − 2·m_2 + m_1 = -0.7403, one-sided block-permutation p=0.0002 (significant; S<0 direction matches the convexity-spec "accelerating-decrement" SUPPORTED direction). Spline non-linearity F=+28.27 (block-permutation p=0.0003; significant); spline-second-derivative at midpoint x=35 = -0.00151 (NEG); at midpoint x=70 = +0.00000 (POS — counted as POS per pre-reg §5.1 "positive spline second derivative at majority of midpoints" wrong-direction override clause).

Companion contrast c·m with c=(+1,−2,+1) = -0.7403, p=0.0002 (consistent direction with S). Spearman ρ = -0.0298 (n.s., p=0.4738) — the opposing-model linear test essentially flat.

Pairwise adjacent-bin Mann-Whitney with Holm step-down (2 pairs post-absorption): B1-B2 Holm-adj p=0.0089 (rejected); B2-B3' Holm-adj p=0.0030 (rejected). Both adjacent-bin differences statistically detectable in non-zero direction.

Sensitivity arms: §5.B dose-adjusted cross-phase (n=1351) REJECTED at 0-of-3; within-consolidation §5.A replication REJECTED (wrong-direction). §4.6 crash-drop: S(full)=-0.7403 (n=581) vs S(no-crash)=-0.1473 (n=503); standardised |Δ S|=0.6427; sign-change=False; FLAG fired but does NOT modify §5.1 verdict per §3.4 / §4.6. §4.8 train/validate M3 overlay: train S=-0.8754 (n=482, bin-n=[77, 312, 93]); validate S=-0.0563 (n=99, bin-n=[18, 73, 8]); divergence reported per `train_validate_split_fate.md §5` as descriptive only. §4.8 t+1 lagged: S=-0.6236 (n=581).

Stage D verdict-trust call: TRUSTED. A2 BACKSTOPPED-partial (per-channel missingness audit on `all_day_stress_avg` is the closure path; not blocking).

## 3. What the verdict licenses

The verdict licenses **the within-operationalisation negative claim with wrong-direction-override structure**:

> The Wiggers-verbatim 4-bin absolute-numerical operationalisation of the stress→fatigue convex-cost claim — specifically the (0-30, 30-40, 40-60, 60+) bin scheme preserving Wiggers' 30→40 numerical anchor at the B2-B3 boundary, with §7.3 halt-option-A pre-committed B4 absorption that fired at dry-run producing the 3-bin reduction (0-30, 30-40, 40-100) — is **REJECTED on this corpus's Stratum 4 unmedicated primary cell**, with the wrong-direction override firing on condition (c) per the locked verdict bar (positive spline second derivative at majority of contributing midpoints — specifically, x=35 NEG and x=70 POS, the 1-of-2 contributing midpoints failing the ≥ 1-of-2 negative-sign-agreement bar).

Effect-size summary: bin-mean trajectory (3-bin reduction) B1=3.958 → B2=4.265 → B3'=3.832 (peak at B2 = stress 30-40); convexity statistic S=-0.7403 (significantly negative, p=0.0002, consistent with curvature in the data); spline non-linearity highly significant (F=28.27, p=0.0003) but the spline's second-derivative-sign check at the upper midpoint x=70 returns POS, indicating the curvature is **opposite to the Wiggers-predicted convex direction at the upper-stress portion of the bin scheme**.

The licensed claim is bounded by the operationalisation: REJECTED of this specific 4-bin Wiggers-verbatim scheme (with the post-§7.3 3-bin reduction). Per CONVENTIONS §4.3 confirmatory framing: the test set out to confirm or refute Wiggers' verbatim convex-cost direction on this corpus; the result is a within-operationalisation REJECTED with the wrong-direction signal preserved as part of the claim shape (per guide #2 §5.2 worked example).

Per Stage D TRUSTED: no PROVISIONAL narrowing applies; the licensed claim stands at full strength per the operationalisation's evidence.

## 4. What the verdict does NOT license

Four predictable overclaim shapes addressed explicitly per guide #2 §4.4:

1. **REJECTED does NOT mean "the underlying Wiggers convex-cost hypothesis is false."** The operationalisation may be inadequate; a different bin-scheme operationalisation might detect the predicted signal. Sister HA-C3p (per the synthesis-structure map's C-stress-fatigue-shape cluster) tests the same construct on personal-baseline-anchored quintile bins and produces a different verdict-band (PARTIAL, with (b) + (c) PASSED detecting curvature). The cluster-level cross-operationalisation reading is Stage S₁'s job per the map's `C-stress-fatigue-shape` row; this Stage I artefact does NOT pre-empt that reading. **Note**: per [`_synthesis_seed_notes_2026-06-23.md`](../../methodology/_synthesis_seed_notes_2026-06-23.md) §2 the r1 map-drafter sketched a candidate inverted-U joint reading; that sketch is **caveat-class advisory only**, not a substantive input to this artefact's §3 licensed claim per the seed-notes' own §5 self-description and guide #2 §7.4 anti-pattern.

2. **REJECTED with significant curvature signal (S<0 + spline F significant) does NOT license "the proposed mechanism (curvature in the dose-response) is wrong."** S<0 and spline F>0 with p<0.05 mean the test detected curvature in the data; the wrong-direction override fires on the **direction** of the curvature at the upper portion of the bin scheme, not on its existence. Correlation in the inverse-of-predicted direction is not mechanism-rejection; it is hypothesis-generating prior for a different cost-shape model (e.g., inverted-U / threshold pattern; per pre-reg §8 caveat 9 the v1 partial-pool non-monotone trajectory was a caveat-class prior informing v2 interpretation — NOT a substantive v2 output). Mechanism reasoning belongs to Stage S₁ + Stage S₂ via cross-operationalisation and external-literature positioning; Stage I records the operationalisation-bound REJECTED without mechanism overreach.

3. **REJECTED is its own claim shape with the wrong-direction-override sub-claim preserved**; per guide #2 §5.2: "the licensed claim respects the verdict's internal structure" — the override-clause IS the claim shape, not a noise term to bracket away. PARTIAL is NOT a defensible re-labeling for this verdict (the pre-reg §5.1 spec carries the override as a structural rule, not a tunable; re-labeling would violate guide #2 §7.9 anti-pattern).

4. **REJECTED on this corpus does NOT mean "the test would have rejected on any other comparable corpus."** Per the §4.5 L-ID block below: L1 single-subject reach bounds the inference reach; group-level confirmation requires the §4.8 external-research track.

## 4.5 Caveats narrowing the claim (with L-ID citation block)

### 5a. Pre-reg + audit caveats (carry-forward from upstream)

From pre-reg §8 (the pre-reg's own self-declared narrowing):
- Power-calc dispatch inapplicable per Daza 2018 within-subject design (§8 caveat 1).
- n=1 single-subject caveats per CONVENTIONS §3.1 (§8 caveat 2).
- Citalopram-channel inheritance: `all_day_stress_avg` dose-modulated at +0.57/mg; §5.A unmedicated primary + §5.B sensitivity arm pattern (§8 caveat 3).
- Crash-day inclusion structural fragility per CONVENTIONS §3.4 (§8 caveat 4); the §4.6 crash-drop flag fired (informative for interpretation; does NOT modify §5.1 verdict).
- Within-subject shape, NOT between-subject prediction (§8 caveat 5).
- No causal-direction inference (§8 caveat 6).
- v2 scope is corpus-stress-range AS-REPRESENTED, NOT Wiggers' abstract register range (§8 caveat 7).
- Wiggers' phrasing is qualitative; v2's specific binning is one operationalisation (§8 caveat 8).
- v1 partial-pool non-monotone trajectory as caveat-class prior informing v2 interpretation (§8 caveat 9).
- Independent-obligations block per `citalopram_phase_stratification §6` (§8 caveat 10).
- Drafting-context disclosure + confirmatory-vs-exploratory operational consequence per CONVENTIONS §4.3 (§8 caveat 11): substantive Wiggers C3 convex-shape question stays confirmatory; v2 operationalisation choice (4-bin scheme post-v1-HALT) is exploratory-with-caveat per corpus-conditional redraft trigger.
- Sister-test cross-references including HA-C3p personal-baseline sister (§8 caveat 12).

From Stage D `descriptive_audit.md` §3 + §5: A2 BACKSTOPPED-partial (per-channel missingness audit on `all_day_stress_avg` is the closure path); narrows the L7 survivorship reach at this Stage I per the audit's §5 entry.

### 5b. L-ID citation block (binding per limitations doc §5 row for `interpretation.md`)

Per the synthesis-structure map's §3 [C-stress-fatigue-shape](../../methodology/synthesis_structure_map.md#3-cluster-table-s%E2%82%81-pre-registration) row L-IDs column: cluster L-IDs = L1, L2, L3, L4, L6, L7 (L5 NA). Stage I cites the subset applying to this HA's primary signals:

> *Cites L1 (single-subject reach)*: this verdict is about one subject's stress-fatigue dose-response shape on the Wiggers-verbatim 4-bin operationalisation; per Daza 2018 N-of-1 inference reach, REJECTED here does not refute the Wiggers convex-cost claim at the group level; cross-operationalisation reading at Stage S₁ + external-literature positioning at Stage S₂ are the next-step reach bounds.

> *Cites L2 (era confounds)*: HA-C3 v2 primary cell ran on Stratum 4 unmedicated only (2022-09-03 → 2024-04-08 with April 2024 cluster excluded); the verdict does not project to the medicated Stratum 4 sub-phase per the locked pre-reg §4 scope. §5.B dose-adjusted cross-phase sensitivity arm (descriptive only, REJECTED 0-of-3) is consistent with the within-Stratum-4-unmedicated bounding.

> *Cites L3 (device generations)*: `all_day_stress_avg` is FR245 Elevate-V3-derived Garmin signal; the REJECTED verdict is constrained to within-device-generation reach; cross-device-generation projection requires explicit calibration evidence per limitations doc §3 L3.

> *Cites L4 (analyst-is-subject)*: HA-C3 v2 was prior-driven by the Wiggers handbook reading (PDF lines 1357-1368 verbatim convex-cost claim per the §1 register-anchor); per CONVENTIONS §4.3 the test is confirmatory; the §4.6 lived-experience-prior reconciliation below records the prior explicitly. L4 mitigation reach per limitations doc r3 §3 L4 caveat: fresh-session `/research-review` peer-check (pending post-dry-run); producer-vs-reviewer split honored via this artefact's reviewer-mode-with-authorization status.

> *L5 (presence-conditioned data layer) NA*: HA-C3 v2 uses no v24 primary signals; `all_day_stress_avg` and `gevoelscore` are both `daily_computed` per `symptom_mention_asymmetry.md` taxonomy. The map's §3 row marks L5 NA for the C-stress-fatigue-shape cluster; this HA does not trigger L5 independently. NA reason: no v24-derived columns anywhere in the primary or sensitivity-arm chain.

> *Cites L6 (self-reporting)*: `gevoelscore` is the outcome; the verdict inherits the self-report noise floor described in limitations doc L6 (1-10 daily subjective scale; potentially heightened interoceptive-disturbance noise in PAIS populations). Bin-mean differences across bins are small in absolute units (0.4-0.5 gevoelscore points between adjacent bins) and sit within the per-day self-report noise envelope; the wrong-direction override on condition (c) at the x=70 midpoint sits inside this noise envelope, which the §4.7 external-literature positioning should engage with.

> *Cites L7 (survivorship)*: the n=581 effective coverage on the unmedicated primary cell represents the gated subset of Stratum 4 unmedicated calendar days after §4.3 day-validity gates (LC era + non-NaN both columns + April 2024 cluster excluded + first-21-days device-baseline-warmup excluded). The verdict does not project to days outside the gated subset. The Stage D audit's A2 BACKSTOPPED-partial reading flags that a per-channel missingness audit on `all_day_stress_avg` would tighten the L7 reach narrowing; until that audit lands, the L7 citation here remains "gating-discipline-bounded" rather than "fully audit-backed".

## 4.6 Lived-experience prior reconciliation

**STATUS: USER-ARTICULATED 2026-06-25** per §11 step 10 Phase A.1
rollout interview. DEFAULTED-PENDING-USER-INPUT placeholder
superseded; the dry-run default-reading is documented at the end of
this section for traceability but does NOT carry forward.

**The prior** (user verbatim, 2026-06-25): *"I did not know what to
expect. I was not aware of any pattern myself."* The subject's
lived-experience prior on the Wiggers convex stress-fatigue mapping
for this corpus was **null** — no specific expectation about the
shape; no awareness of a pattern from lived experience prior to the
test running.

**The verdict** (per §4.3): HA-C3 v2 REJECTED with wrong-direction
override; bin-mean trajectory non-monotone peaking at the 30-40
junction; concave / inverted-U shape direction-of-failure.

**Agreement / divergence**: NOT APPLICABLE in the standard sense.
The prior was null — neither agreement nor divergence between
"nothing expected" and the inverted-U finding can be cleanly
asserted. What the §4.6 records honestly:

- The verdict produces a substantive descriptive finding (inverted-U
  shape) that the subject had NOT noticed lived.
- This is **discovery via test** rather than confirmation of a lived
  prior. The L4 (analyst-is-subject) coupling is structurally
  weaker for this HA than for prior-driven HAs where the subject's
  prior matched what the pre-reg tested.
- The Wiggers'-prior framing (the canonical claim from the
  handleiding lines 1357-1368) WAS the test's prior — but the
  *subject's* prior on whether Wiggers' would hold for them was
  null. The two priors are distinct; only the subject's null prior
  is recorded here per guide #2 §4.6.

**Implication for §3 licensed claim**: per the guide #2 §4.6 r2
agreement-does-not-strengthen rule + the L4 caveat, the verdict's
licensed claim (per §4.3) stands as the operationalisation-bound
descriptive shape claim. The null prior does NOT modify the §3
licensed claim in either direction (no strengthening, no
narrowing). The honest reading: this is a finding the subject did
not anticipate, which makes the §3 licensed claim closer to genuine
within-subject descriptive discovery rather than prior-confirmation.

**Routing**: no cluster-level reconciliation work needed at Stage
S₁ for the prior-vs-verdict pair on this HA specifically (since
there's no divergent prior to reconcile). Stage S₁ on
C-stress-fatigue-shape proceeds on the verdict-shape evidence
alone per the guide #3 §5.2 coherence-call mapping.

**L4 meta-recursion acknowledgment**: per guide #2 §4.6 closing
paragraph and limitations doc r3 L4: the user articulated the
prior directly in §11 step 10 Phase A.1 interview (2026-06-25);
no Claude-dispatched articulation. The previous DEFAULTED-PENDING-
USER-INPUT placeholder from the dry-run is documented at the end
of this section for traceability per L4 transparency discipline.

**Dry-run default-reading (superseded; recorded for traceability
only)**: at dry-run dispatch the placeholder suggested "the user's
lived-experience prior on the stress→fatigue mapping at this
corpus is most likely characterised by the awareness that 'very-
low-stress days are often conserving-everything days where the
gevoelscore was lower than a simple monotone-decreasing
relationship would suggest.'" This default-reading was Claude's
reasonable-default guess; the actual user articulation
(2026-06-25) was *null prior*, contradicting the default. The
contradiction is itself informative about L4: the dispatcher's
plausible-sounding default differed materially from the subject's
actual lived state. Future dry-run defaults should treat
"unspecified user prior" as null-prior-default rather than
inverted-U-guess-default to avoid this L4 inflation pattern.

## 4.7 Closure-path statement

REJECTED verdict; closure-path is **NA** per guide #2 §4.7 (the section header is required for uniformity but the content collapses for REJECTED / SUPPORTED verdicts).

(For reader-traceability: the candidate "upgrade path" — if the user wanted to know what would convert the REJECTED into a PARTIAL or SUPPORTED — is not a closure-path question for this verdict; it is a §4.8 own-research follow-up question, addressed below.)

## 4.8 Follow-up suggestions (own-research + external-research tracks)

### Own-research track

- **Third sister-HA on a rolling-window-baseline binning** (e.g., `stress_z_28d_lagged` quintiles per the HA-C3p §4.8(b) sensitivity arm precedent, but as a primary headline cell). Per guide #2 §4.8 own-research example: a third sister-HA with a different bin-edge methodology (rolling-window-baseline rather than pool-anchored quintile or Wiggers-verbatim absolute) would add a third independent operationalisation to the C-stress-fatigue-shape cluster, tightening Stage S₁'s cross-operationalisation reading. Pre-reg shape: same `all_day_stress_avg × gevoelscore` substrate; same Stratum 4 unmedicated headline; same 3-condition verdict bar; bin scheme = rolling-baseline z-score quintiles. Routing: `hypothesis_lock_process.md` §3.2 fresh-session drafting.

- **Pre-reg for HA-C3-v3 with inverted-U / threshold-pattern alternative claim as PRIMARY** (per pre-reg §8 caveat 9 explicit framing: "promoting the v1 trajectory observation to a SUPPORTED-of-inverted-U claim would require a different pre-reg — a §3.2 fresh-session redraft to HA-C3-v3 with the alternative-shape claim as the primary"). HA-C3 v2's REJECTED + wrong-direction override is the trigger this pre-reg would cite as its motivation; the new pre-reg would test the inverted-U direction on the corpus with explicit pre-commitment to peak-location bounds and inverted-U-specific contrast machinery.

- **Per-channel missingness audit on `all_day_stress_avg`** (per Stage D `descriptive_audit.md` §5 `open_inputs` entry; closes both HA-C3 v2 and HA-C3p A2 in one S-effort run). Not a sister-HA pre-reg; a descriptive infrastructure run that tightens the L7 reach at the next Stage I re-examination.

### External-research track

- **Cohort study replicating the inverted-U / threshold-pattern stress→fatigue mapping in LC / ME/CFS populations** at group level. We cannot run this ourselves because **L1 (single-subject reach)** prevents the N=1 corpus from settling the group-level question; Daza 2018 N-of-1 inference reach bounds the current verdict to "one subject's data point" against the group-level Wiggers convex-cost claim. The external study would carry pre-registration of an inverted-U-direction alternative hypothesis (with peak-location operationalised per population subgroup if appropriate); minimum n per Daza 2018 + CENT 2015 item 22 generalisability statement bounds.

- **Cross-instrumentation comparability study**: Garmin `all_day_stress_avg` (24-hour HRV-derived sympathetic-arousal index) vs Wiggers' subjective-stress-rating-from-handbook framing. We cannot run this ourselves because **L3 (device generations)** + the fact that Wiggers' handleiding does not name a specific instrument for the stress register (the handbook is qualitative-and-subjective in operationalisation); a comparability study would clarify whether the Garmin signal and the Wiggers subjective-rating substrate are measuring the same underlying construct, which is the load-bearing question for whether HA-C3 v2's REJECTED on the Garmin signal speaks to the Wiggers claim on the subjective-rating substrate.

## 4.9 `open_inputs` block

| # | What is missing | What it blocks | Cheapest acquisition path | Fallback claim available |
|---|---|---|---|---|
| 1 | User confirmation of lived-experience prior for HA-C3 v2 (per §4.6) | §4.6 reconciliation completion at Stage I | One interview question per the §8.3 seed in `verdict_to_inference.md` (in a non-dry-run session) | DEFAULTED-PENDING-USER-INPUT placeholder with one-sentence default-reading (no narrowing of §3 licensed claim) |
| 2 | Per-channel missingness audit on `all_day_stress_avg` | Tightens §4.5 L7 citation from "gating-discipline-bounded" to "fully audit-backed"; shared closure with HA-C3p Stage D `open_inputs` | S effort per stocktake §3 Shared gap 3; script template from `desc-SMS` exists | TRUSTED stands with L7 narrowing caveat at Stage I per Stage D `descriptive_audit.md` §5 |

## 4.10 Cross-references

- HA-C3 v2 r2 [`hypothesis.md`](../hypotheses/HA-C3/hypothesis.md) and [`result.md`](../hypotheses/HA-C3/result.md).
- Stage D audit [`descriptive/HA-C3/descriptive_audit.md`](../descriptive/HA-C3/descriptive_audit.md).
- Synthesis-structure map [C-stress-fatigue-shape](../../methodology/synthesis_structure_map.md#3-cluster-table-s%E2%82%81-pre-registration) cluster row (declared 2026-06-23, lock r3 2026-06-24).
- Sister-HA interpretation [`HA-C3p.md`](HA-C3p.md) (companion Stage I artefact in this dry-run dispatch).
- Forward pointer to Stage S₁: [`synthesis/cluster-stress-fatigue-shape.md`](../synthesis/cluster-stress-fatigue-shape.md) (next downstream artefact in this dry-run dispatch).
- Limitations doc cross-refs for cited L-IDs: [`research_line_limitations.md`](../../methodology/research_line_limitations.md) §3 L1, L2, L3, L4, L6, L7; §5 citation requirements row for `interpretation.md`.
- [`_synthesis_seed_notes_2026-06-23.md`](../../methodology/_synthesis_seed_notes_2026-06-23.md) §2 (caveat-class advisory, cited in §4 overclaim #1 as flagged-out-of-scope per guide #2 §7.4-by-analogy).
- Literature methodology anchors: [Daza 2018](../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) (N-of-1 inference reach, cited at §4.5 L1); CENT 2015 (items 21+22 generalisability statement, cited at §4.8 external-research); SCRIBE 2016 (L4 participant-as-researcher transparency); Natesan 2023 (defensibility bar for single-case verdict-to-claim translation).
- [`_plan_results_analysis_layer.md`](../../methodology/_plan_results_analysis_layer.md) §3.10 hard predictive gate (Stage I does not cross; predictive claims live at Stage A); §3.11 follow-up tracks (§4.8 implements); §3.12 commentary boundary (Stage I does not carry; deferred to Stage A K-stress-fatigue-monitoring tier-1).
- CONVENTIONS [§1.2](../../CONVENTIONS.md#12-producer-vs-reviewer-mode) reviewer-mode-with-authorization discipline + Authorship block; [§4.3](../../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory) confirmatory framing for prior-driven HAs.

---

## §10 Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-25 | Drafted r1 (DRY-RUN) | Reviewer-mode-with-authorization by `/research-interpret interpret HA-C3` skill in dry-run dispatch per §11 step 8. Stage D `descriptive_audit.md` (DRAFT r1, dry-run, TRUSTED) consumed as upstream gate per guide #2 §9.2 — proceeded normally (TRUSTED unblocks). §4.6 lived-experience-prior DEFAULTED-PENDING-USER-INPUT per dry-run framing. **Drift triggers registered** (manual-pending-skill per skill responsibility #10): (1) HA-C3 v2 `result.md` re-runs; (2) Stage D `descriptive_audit.md` re-examined; (3) cited methodology MD changes lock-version (especially [`research_line_limitations.md`](../../methodology/research_line_limitations.md) since L-ID citations propagate); (4) ≥6 months elapse since lock. **STATUS: NOT LOCKED — awaiting (a) user acceptance + (b) fresh-session `/research-review` per [`_plan_results_analysis_layer.md`](../../methodology/_plan_results_analysis_layer.md) §4 row for `interpretation.md`.** |
