# cluster-stress-fatigue-shape — internal synthesis (Stage S₁)

**Status**: **LOCKED r1 by user acceptance 2026-06-25** per §11 step 10 Phase A.7. Drafted 2026-06-25 by `/research-interpret synthesise C-stress-fatigue-shape` skill in dry-run dispatch per §11 step 8 (skill since LOCKED r4). Phase A.3 §4.4 coherence-call PARTIALLY CONCORDANT user-confirmed (OI-003 closed); A.7 user-acceptance lock event closes Phase A. **First LOCKED Stage S₁ synthesis of the layer.** Awaiting fresh-session `/research-review` per locked-plan §4 row.

## Authorship

Drafted 2026-06-25 by Claude (Opus 4.7, 1M context) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../CONVENTIONS.md#12-producer-vs-reviewer-mode), via the `/research-interpret synthesise cluster-stress-fatigue-shape` skill invocation in §11 step 8 dry-run dispatch. Authorising user: Willem. Fresh-session `/research-review` peer-check required before LOCK per [`_plan_results_analysis_layer.md`](../../methodology/_plan_results_analysis_layer.md) §4 row for `cluster-*.md`.

---

## 4.1 Cluster name + constituent HAs

- **Cluster ID + name** (verbatim from map r3 §3): **C-stress-fatigue-shape** — Stress-fatigue dose-response shape (daily-aggregate).
- **Constituent HAs** (verbatim from map's "Constituent HAs" cell): HA-C3 v2, HA-C3p.
- **Member verdicts** (verbatim from each member's [`interpretation.md`](../interpretation/) §1, which carries verbatim from `result.md`):
  - **HA-C3 v2**: REJECTED (wrong-direction override). Stage D verdict-trust: TRUSTED.
  - **HA-C3p**: PARTIAL (2-of-3 conditions MET). Stage D verdict-trust: TRUSTED.
- **Shared construct** (verbatim from map's "Shared construct" cell): Non-linear stress→fatigue mapping per Wiggers convex-cost claim.
- **Operationalisation-overlap note** (verbatim from map's "Operationalisation overlap note" cell): Two **independent** operationalisations of the same construct. Both use `all_day_stress_avg × gevoelscore`; HA-C3 v2 uses Wiggers-verbatim 4-bin absolute anchor (30→40), HA-C3p uses personal-baseline quintile bins. The cross-bin-scheme independence (absolute-numerical vs personal-relative binning) is what gives this cluster its evidence-strength as "two independent operationalisations" rather than two-views-on-the-same-cut — preempts the locked-plan §6.3 anti-pattern. Sister HAs by explicit pre-reg framing (HA-C3p §1). HA-C3p result.md §6 contains a 4-cell agreement matrix; per HA-C3p's own §6 framing this matrix is **caveat-class post-hoc and NOT a substantive output**, so S₁ cites the matrix as descriptive context only and produces its coherence call independently of it.
- **Cascade-arrow language**: NONE for this cluster (C-stress-fatigue-shape has no upstream cascade-precondition; it is itself stand-alone). The §4.5 §5c cascade-precondition sub-paragraph is omitted accordingly per `internal_synthesis.md` §4.5.

## 4.2 Pre-declared constellation

> *Pre-declared constellation* (per [`synthesis_structure_map.md`](../../methodology/synthesis_structure_map.md#3-cluster-table-s%E2%82%81-pre-registration) §3 row `C-stress-fatigue-shape`, declared 2026-06-23, lock version r3): the cluster groups HA-C3 v2 and HA-C3p on the shared construct **non-linear stress→fatigue mapping per Wiggers convex-cost claim** because the two HAs are **two independent operationalisations of the same construct** (Wiggers-verbatim absolute-numerical bins vs personal-baseline-anchored quintile bins) — the cross-bin-scheme independence is what gives this cluster its evidence-strength as two independent operationalisations rather than two-views-on-the-same-cut, pre-empting the locked-plan §6.3 anti-pattern ("three HAs on the same signal are one piece of evidence, not three"). The constellation was locked at the layer-wide map's §7 lock-log entry 2026-06-24 (r3) and has not changed since. This Stage S₁ session reads the constellation from the map row; it does not propose a constellation change.

## 4.3 Per-HA verdict + interpretation row

| HA | Verdict | Operationalisation | "What the verdict licenses" (from Stage I §3) | "What the verdict does NOT license" | Effect-size summary | L-IDs cited (Stage I §4.5) | Closure-path (Stage I §4.7) |
|---|---|---|---|---|---|---|---|
| HA-C3 v2 | REJECTED (wrong-direction override) | Wiggers-verbatim 4-bin scheme `[0,30), [30,40), [40,60), [60,100]` with pre-committed §7.3 halt-option-A absorber that fired at dry-run (3-bin reduction `{[0,30), [30,40), [40,100]}`); Stratum 4 unmedicated headline | The Wiggers-verbatim 4-bin absolute-numerical operationalisation of the stress→fatigue convex-cost claim is REJECTED on Stratum 4 unmedicated; wrong-direction override fires on condition (c) per the locked verdict bar (positive spline second derivative at majority of contributing midpoints — specifically x=35 NEG and x=70 POS, the 1-of-2 contributing midpoints failing the ≥1-of-2 negative-sign bar). | REJECTED of this operationalisation does NOT license REJECTED of the Wiggers convex-cost claim at construct level (cross-operationalisation reading is cluster-level work); REJECTED with significant curvature signal does NOT license "the mechanism is wrong" (curvature is detected, only its direction at upper portion of bins is inverse-of-predicted); PARTIAL is NOT a defensible re-labeling (wrong-direction override is structural); REJECTED on this corpus does NOT mean group-level rejection (L1). | Bin-mean trajectory (3-bin) B1=3.958 → B2=4.265 → B3'=3.832 (peak at B2 = stress 30-40); convexity statistic S=-0.7403 (significantly negative, p=0.0002); spline non-linearity F=28.27 (p=0.0003); spline 2nd-deriv at x=35 NEG, at x=70 POS (wrong-direction override fires on condition (c)). | L1, L2, L3, L4, L6, L7 (L5 NA) | NA per guide #2 §4.7 — REJECTED verdicts collapse the section. |
| HA-C3p | PARTIAL (2-of-3 conditions MET) | Personal-baseline-anchored 5-quintile-bin scheme `[0, 28, 31, 34, 37, 100]` computed on full Stratum 4 pool (n=1351, snapshot SHA `d0ff9253...`); §5.A unmedicated sub-arm primary cell via cross-arm-cleanliness re-use of edges | The personal-baseline-anchored 5-quintile-bin operationalisation of the stress→fatigue convex-cost claim is PARTIAL on Stratum 4 unmedicated, with 2 of 3 conditions MET: (b) convexity contrast S=-0.1964 PASSED (p=0.0018, S<0 direction); (c) spline F=+19.55 PASSED (p=0.0020; spline 2nd-deriv NEG at 3 of 4 contributing midpoints). Condition (a) Jonckheere-Terpstra monotone-decreasing FAILED (p=0.5925, n.s.; direction not monotone-decreasing). | PARTIAL does NOT mean "Wiggers convex-cost partially confirmed"; the missing (a) captures **curvature in the inverse direction**. PARTIAL with (b)+(c) PASS does NOT license "inverted-U alternative is SUPPORTED" (would require separate pre-reg). PARTIAL does NOT license causal-mechanism claim. PARTIAL on this corpus does NOT mean group-level replication. | Bin-mean trajectory Q1=3.822 → Q2=4.138 → Q3=4.271 → Q4=4.290 → Q5=4.016 (peak at Q4 = stress 34-37); convexity S=-0.1964 (significantly negative); spline non-linearity highly significant. All four adjacent-bin Mann-Whitney comparisons FAIL Holm correction at α=0.05. | L1, L2, L3, L4, L6, L7 (L5 NA) | Operational per guide #2 §4.7 — three paths to upgrade beyond PARTIAL: a different bin scheme; a revised pre-reg with inverted-U as primary direction; a larger n (hypothetical). |

## 4.4 Coherence call

**STATUS: PARTIALLY CONCORDANT (USER-CONFIRMED 2026-06-25** per §11 step 10 Phase A.3 rollout interview. The DEFAULTED-TO-PRESERVE-PENDING-USER-INPUT placeholder is superseded; OI-003 closes. User confirmed the default-to-preserve framing rationale: keep the verdict-band asymmetry visible in §4.6 open-conflicts as a structural observation worth recording, even though the shape-substance agreement is full.**)

**Rationale** (drawn from §4.3 per-HA rows + the map's §3 operationalisation-overlap-note + the LOCKED-r2 `internal_synthesis.md` §5.2 worked example as corrected per the [methodology-internal_synthesis-2026-06-24 review R1](../../reviews/methodology-internal_synthesis-2026-06-24.md)):

Both HAs in the cluster **detect the same inverted-U / concave-down shape** on the stress→fatigue mapping. The agreement is at the shape-detection level: both HA-C3 v2 (S=-0.7403 significantly negative, p=0.0002; spline F=28.27 highly significant) and HA-C3p (S=-0.1964 significantly negative, p=0.0018; spline F=19.55 highly significant) detect curvature in the bin-mean trajectory; both trajectories peak in the mid-stress range and decline at the upper-stress end. The verdict-band asymmetry (REJECTED vs PARTIAL) is **spec-mechanism only**, not shape-substance: HA-C3 v2's pre-reg spec carries a wrong-direction override on condition (c) (positive spline 2nd-deriv at majority of midpoints) that routes the inverse-direction curvature firing to REJECTED; HA-C3p's pre-reg spec does NOT carry that override, letting the (b) + (c) PASS conditions stand and producing PARTIAL on the 2-of-3 count.

Per `internal_synthesis.md` §5.2 r2 worked example (corrected per R1 review): both HAs agree on **direction** (inverse non-linearity, concave / inverted-U shape peaking around mid-stress, NOT Wiggers-monotone-convex) and agree on the **underlying shape detection** (the spline + convexity machinery fires in both). The §4.7a width discipline therefore permits a cluster-level joint claim broader than either individual member's licensed claim (the cross-operationalisation convergence is positive multi-test evidence per Daza 2018) — and that broader joint claim is what §4.7a below records.

Per `internal_synthesis.md` §5.2 r2 alternative worked example: a synthesist could legitimately read this as CONCORDANT rather than PARTIALLY CONCORDANT on the grounds that the verdict-band asymmetry is purely spec-mechanism and the shape-substance is uniformly inverted-U across both HAs. The choice between CONCORDANT and PARTIALLY CONCORDANT for this cluster is a **judgment call the user makes during the §8 interview**. The PARTIALLY-CONCORDANT default-to-preserve reading honours the verdict-band asymmetry as worth recording even when the underlying shape agreement is strong. **CONFLICT is NOT a defensible reading for this cluster on current evidence** — both HAs detect the same shape; no opposite-direction-on-the-construct disagreement exists at the licensed-claim level (per `internal_synthesis.md` §5.3 r2: "no current cluster realises this case" for CONFLICT).

The user-input prompt logged to `_open_inputs.md` OI-003: "Walking the §4.3 per-HA rows: PARTIALLY CONCORDANT (honour the spec-mechanism verdict-band asymmetry) or CONCORDANT (the shape-substance is uniformly inverted-U; verdict-bands differ only on spec, not on direction)?"

## 4.5 Cluster-level caveats narrowing the joint claim (with L-ID citation block)

### 5a. Cluster-level caveats from member interpretations

Both HA-C3 v2 §4.5 and HA-C3p §4.5 carry near-identical pre-reg + audit caveats; Stage S₁ synthesises them rather than duplicating:

- Power-calc dispatch inapplicable per Daza 2018 within-subject design (both members §8 caveat 1).
- n=1 single-subject per [CONVENTIONS §3.1](../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) (both members).
- Citalopram-channel inheritance + right-shift observation: `all_day_stress_avg` CONFIRMED dose-modulated at +0.57/mg; both members run §5.A unmedicated primary + §5.B sensitivity arm pattern; HA-C3p §4.1 surfaces the right-shift unmedicated bin observation as cross-test validation of the dose-modulation recalibration at a different operationalisation level (bin distribution vs mean β).
- Crash-day inclusion structural fragility per CONVENTIONS §3.4; crash-drop FLAG fired on both HAs (informative; does NOT modify §5.1 verdicts).
- Within-subject shape, NOT between-subject prediction (both members).
- No causal-direction inference (both members).
- v2 scope is corpus-stress-range AS-REPRESENTED, NOT abstract Wiggers register (HA-C3 v2 §8 caveat 7); HA-C3p §8 caveat 13 similarly notes Wiggers' phrasing is qualitative and the quintile bins are one operationalisation.
- v1 partial-pool non-monotone trajectory as caveat-class prior informing v2 + HA-C3p interpretations; both pre-regs explicitly out-of-scope for inverted-U alternative claim (would require separate pre-reg).
- Independent-obligations block per `citalopram_phase_stratification §6` (both members handled per §4).
- Drafting-context disclosure + confirmatory-vs-exploratory operational consequence per CONVENTIONS §4.3 (both members).
- HA-C3p §8 caveat 10: bin-edge snapshot pinning per §4.1 Gate 5 (HA-C3p-specific; HA-C3 v2 has no analogous gate because Wiggers-verbatim integer-valued boundaries are not data-driven).

From both members' Stage D `descriptive_audit.md` §5 entries: shared A2 BACKSTOPPED-partial — per-channel missingness audit on `all_day_stress_avg` would tighten the L7 reach at both Stage I + cluster Stage S₁ levels (closure path is shared S-effort run that closes both members' A2 simultaneously).

### 5b. Cluster-level L-ID citation block (binding per limitations doc §5 row for `cluster-*.md`)

Per the synthesis-structure map's §3 [C-stress-fatigue-shape](../../methodology/synthesis_structure_map.md#3-cluster-table-s%E2%82%81-pre-registration) row L-IDs column: **L1, L2, L3, L4, L6, L7 (L5 NA)**. The cluster does NOT span different era strata (both members run Stratum 4 unmedicated only) so no extra L2-era-strata-mismatch citation is triggered beyond the per-HA L2 each interpretation already cited.

> *Cites L1+L2+L4* (cluster-level multi-cite per limitations doc §5 worked-example pattern): this cluster's joint claim about the stress-fatigue mapping shape is **single-subject** (L1 inference reach per Daza 2018 bounds it; cluster-level cross-operationalisation convergence adds one within-subject data point about the construct, not a group-level claim); **both member HAs run on Stratum 4 unmedicated only** (L2 forbids cross-phase pooling without warrant; both members' §5.B cross-phase sensitivity arms are descriptive only and REJECTED 0-of-3 — they do NOT support a cross-phase joint claim); the cluster's coherence call rests on **two prior-driven operationalisations of the Wiggers convex-cost claim** (L4 — analyst-is-subject coupling; both pre-regs were drafted with Wiggers as the explicit prior direction, and the cluster-level shape-detection-with-direction-inversion finding inherits the L4 reach bound per [`research_line_limitations.md`](../../methodology/research_line_limitations.md) §3 L4 caveat).

> *Cites L3 (device generations)*: both members rest on `all_day_stress_avg` FR245 Elevate-V3 Garmin signal; cluster's joint claim is constrained to within-device-generation reach.

> *Cites L6 (self-reporting)*: both members use `gevoelscore` as outcome; the cluster-level claim inherits the self-report noise floor at both HAs. The HA-C3p bin-mean spreads are particularly small in absolute units (0.4-0.5 gevoelscore-points across the full quintile range); the cluster-level shape-detection-at-the-contrast-level despite per-pairwise comparisons failing Holm correction at HA-C3p is the L6-noise-floor manifestation at the cluster reading.

> *Cites L7 (survivorship)*: both members gate on the same §4.3 day-validity discipline (LC era + non-NaN both columns + April 2024 cluster excluded + first-21-days device-baseline-warmup excluded); n=581 on the §5.A unmedicated sub-arm. The cluster's joint claim does not project to days outside the gated subset. Per Stage D `descriptive_audit.md` §5 entries (both members): shared A2 BACKSTOPPED-partial — the per-channel missingness audit on `all_day_stress_avg` would tighten the L7 reach at the cluster level (closes both members' A2 simultaneously).

> *L5 (presence-conditioned data layer) NA*: neither cluster member uses v24-derived columns; both members' §4.5 cite L5 NA; the cluster's joint claim does not trigger L5 independently.

### 5c. Cascade-arrow precondition sub-paragraph

OMITTED: C-stress-fatigue-shape carries no cascade-arrow language in the map's §3 row. The cluster has no upstream cluster precondition; it is stand-alone in the map r3.

## 4.6 Open conflicts preserved with both readings

**STATUS: PARTIALLY CONCORDANT (per §4.4 default).**

Per `internal_synthesis.md` §4.6: when the §4.4 coherence call is PARTIALLY CONCORDANT with substantive disagreement on a qualifier, this section preserves the disagreement. **No auto-resolution.**

**The disagreement preserved**: the two member HAs' verdict-bands differ (REJECTED vs PARTIAL) despite agreement on shape-substance (both detect inverted-U / concave-down curvature). The disagreement is **spec-mechanism only** — HA-C3 v2's pre-reg spec carries a wrong-direction override on condition (c) that routes inverse-direction curvature to REJECTED; HA-C3p's pre-reg spec does not carry that override. This is a **spec-discipline observation worth recording at the cluster level**, not an unresolved substantive conflict on the construct.

**The L4 (analyst-is-subject) acknowledgment**: both pre-regs were drafted by the same subject + analyst with the Wiggers convex-cost claim as the explicit prior direction. The spec-mechanism difference (one with override, one without) was a pre-reg-time choice that affects how the same shape-substance reads as a verdict band; per CONVENTIONS §4.3 the L4 coupling makes this kind of pre-reg-spec choice a substantive output of the analyst's prior structure, not a neutral technical choice. The cluster-level reading records the verdict-band asymmetry as visible-and-recorded rather than silently absorbed.

**Resolution paths (NOT executed at Stage S₁)**:

- **Tie-breaker HA on a third operationalisation** (e.g., rolling-window-baseline binning) per both members' §4.8 own-research follow-up. If the third sister-HA also detects the inverted-U shape, the cluster-level joint claim strengthens at the next Stage S₁ re-examination; if it reverts to monotone, the cluster's reading sharpens differently.
- **Descriptive deep-dive on the bin-mean trajectory shape across both bin schemes** (a `analyses/descriptive/` run that characterises the peak location and width on the participant's distribution, informing any future inverted-U pre-reg's bin-edge pre-commitments per HA-C3p §4.8 own-research entry).
- **Stage S₂ external-literature positioning** at the next downstream stage in this dry-run dispatch (T-stress-fatigue-pacing). The Wiggers-vs-inverted-U direction divergence is exactly what Stage S₂ comparability-and-positioning surface engages with; the cluster-level cross-operationalisation convergence on inverse-direction curvature is the cluster's joint claim feeding Stage S₂.

The cluster's joint claim defaults to "**the construct's stress-fatigue mapping shows curvature in the inverse-of-Wiggers-monotone-convex direction (concave / inverted-U) under both Wiggers-verbatim and personal-baseline-anchored bin schemes, with verdict-band disagreement driven by spec-mechanism handling of wrong-direction firings, not by shape disagreement**" per the PARTIALLY CONCORDANT label; the §4.4 coherence call records this with the spec-mechanism asymmetry preserved as the cluster-internal observation.

## 4.7 What the cluster jointly licenses + does NOT license

### 7a. What the cluster jointly licenses

**The cluster's joint claim** (per §4.7a width discipline + §5.2 worked example):

> The construct of the stress-fatigue dose-response mapping shape, tested on this corpus's Stratum 4 unmedicated cell under two independent operationalisations (Wiggers-verbatim 4-bin absolute-numerical anchor + personal-baseline-anchored 5-quintile-bin), **shows curvature in the inverse direction from Wiggers' monotone-convex prediction** — specifically, a concave / inverted-U shape with bin-mean trajectory peaking around mid-stress (HA-C3 v2 B2 [30,40) bin-mean=4.265; HA-C3p Q3-Q4 [31,37) bin-means=4.271 / 4.290) and declining at upper stress (HA-C3 v2 B3' [40,100] mean=3.832; HA-C3p Q5 [37,100] mean=4.016). The cross-bin-scheme convergence on the inverse-direction curvature finding is positive multi-test evidence per Daza 2018 — the joint claim is broader than either individual member's licensed claim because the two operationalisations are independent (different bin-edge methodologies), narrower than "the Wiggers convex-cost claim is wrong at construct level" (which would require group-level work per L1).

The joint claim is bounded by:
- The cluster's L1 single-subject reach (per §4.5 5b L1 citation).
- The L2 within-Stratum-4-unmedicated phase scope (per §4.5 5b L2 citation; cross-phase reading is §5.B descriptive sensitivity only at both members, REJECTED 0-of-3).
- The L3 within-device-generation reach (per §4.5 5b L3 citation).
- The L4 analyst-is-subject prior coupling (per §4.5 5b L4 citation; Wiggers was the explicit prior at both pre-regs).
- The L6 + L7 self-report noise floor + survivorship-gating discipline (per §4.5 5b L6 + L7 citations).
- The L5 NA confirmation (per §4.5 5b L5 NA).

### 7b. What the cluster jointly does NOT license

Four predictable overclaim shapes per `internal_synthesis.md` §4.7b:

1. **The cluster does NOT license "the construct's mechanism is established."** The cross-operationalisation convergence on inverse-direction curvature is hypothesis-generating prior at most per Daza 2018; the mechanism that explains why the curvature direction is inverse-of-Wiggers (sympathetic-arousal-saturation? conserving-everything-days confound? circadian-clustering? etc.) is a separate question requiring mechanistic study.

2. **The cluster does NOT license "the construct's group-level reach is established."** Per L1 single-subject reach; cluster-level coherence on this N=1 corpus is bounded by Daza 2018 / CENT / SCRIBE / Natesan 2023 N-of-1-to-group reach. The cluster speaks about this subject's stress-fatigue mapping; group-level positioning is Stage S₂'s job (T-stress-fatigue-pacing).

3. **The cluster does NOT license predictive claims.** Per locked-plan §3.10 hard predictive gate; cluster-level coherence does NOT promote any tier. The Stage A K-stress-fatigue-monitoring construct caps at tier-1 monitoring per the map's §5 row (predictive-use blocked; no forward-validation HA pre-registered for this construct).

4. **The cluster does NOT license "the joint claim averages the spec-mechanism verdict-band disagreement."** The PARTIALLY CONCORDANT call preserves the verdict-band asymmetry per §4.6 as a spec-discipline observation; the joint claim names the disagreement-pattern (REJECTED-via-override vs PARTIAL-via-2-of-3-count) rather than papering it over into a "weakly SUPPORTED" or "strongly REJECTED" middle-ground that would collapse the spec-mechanism information.

## 4.8 Follow-up suggestions

### Own-research track

- **Third sister-HA on a rolling-window-baseline binning** (e.g., `stress_z_28d_lagged` quintiles per HA-C3p §4.8(b) sensitivity arm precedent, but as a primary headline cell). Adds a third independent operationalisation to C-stress-fatigue-shape; if the third sister also detects the inverted-U shape, the cluster's joint claim strengthens; if it reverts to monotone, the cluster's PARTIALLY CONCORDANT call sharpens. Pre-reg shape per `hypothesis_lock_process.md` §3.2. **Consolidated from both members' §4.8 own-research entries** — this is the cluster's primary upgrade path.

- **HA-C3-v3 / HA-C3p-v2 with inverted-U / threshold-pattern as primary direction** (both members' pre-regs explicitly out-of-scope per §8 caveats). A pre-reg with inverted-U as the primary direction would convert HA-C3 v2's REJECTED-wrong-direction-override and HA-C3p's PARTIAL-(b)+(c) configurations into SUPPORTED under the new spec's verdict bar. Cluster-level reading at next Stage S₁ would consolidate the three-HA finding.

- **Per-channel missingness audit on `all_day_stress_avg`** (shared with both members' Stage D `descriptive_audit.md` §5 entries; S effort; closes both A2-BACKSTOPPED-partial cells in one run).

- **Descriptive run characterising the inverted-U peak location and width on the participant's distribution** (per HA-C3p §4.8 own-research). Not a hypothesis test; descriptive infrastructure for any future inverted-U pre-reg's bin-edge pre-commitments.

### External-research track

- **Cohort study replicating the inverted-U / threshold-pattern stress→fatigue mapping in LC / ME/CFS populations at group level**. We cannot run this ourselves because **L1 (single-subject reach)** prevents the N=1 corpus from settling the group-level question. The external study would carry pre-registration of an inverted-U-direction alternative hypothesis; minimum n per Daza 2018 + CENT 2015 item 22 generalisability bounds.

- **Cross-instrumentation comparability study Garmin `all_day_stress_avg` vs subjective-stress-rating per Wiggers' handleiding framing**. We cannot run this ourselves because **L3 (device generations)** + the qualitative-and-subjective nature of Wiggers' instrumentation (no specific instrument named); a comparability study would clarify whether the Garmin signal and the Wiggers subjective-rating substrate are measuring the same underlying construct.

- **Group-level test of personal-baseline-vs-absolute-anchor operationalisation choice for stress→fatigue mapping**. We cannot run this ourselves because **L1** + the operationalisation-choice question requires multiple subjects to disentangle "which framing is more accurate" from "which framing is more sensitive on a given subject." Closing this would tighten [CONVENTIONS §3.1](../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline discipline's group-level evidence base.

## 4.9 `open_inputs` block

| # | What is missing | What it blocks | Cheapest acquisition path | Fallback claim available |
|---|---|---|---|---|
| 1 | User judgment-call on coherence-call label (CONCORDANT vs PARTIALLY CONCORDANT — both are defensible readings per `internal_synthesis.md` §5.2 r2; default-to-preserve framing chose PARTIALLY CONCORDANT) | §4.4 coherence call lock; downstream Stage S₂ topic positioning depends on cluster reading | One interview question per §8.2 seed in `internal_synthesis.md` | PARTIALLY CONCORDANT default-to-preserve persists; cluster joint claim per §4.7a stands either way |
| 2 | Third sister-HA on rolling-window-baseline binning (cluster's primary upgrade path per §4.8 own-research) | Tightens cluster coherence call from PARTIALLY CONCORDANT to CONCORDANT if third sister agrees with inverse-direction curvature finding | Pre-reg shape per `hypothesis_lock_process.md` §3.2; full HA cycle (draft + lock + test + Stage D + Stage I) | Cluster PARTIALLY CONCORDANT stands on the two existing operationalisations |
| 3 | Per-channel missingness audit on `all_day_stress_avg` (shared with both members' Stage D) | Tightens §4.5 L7 cluster-level citation | S effort per stocktake §3 Shared gap 3 | Cluster PARTIALLY CONCORDANT stands with L7 narrowing caveat per §4.5 |

## 4.10 Cross-references

- Each member HA's interpretation:
  - [`HA-C3.md`](../interpretation/HA-C3.md) (HA-C3 v2 Stage I, DRAFT r1 dry-run).
  - [`HA-C3p.md`](../interpretation/HA-C3p.md) (HA-C3p Stage I, DRAFT r1 dry-run).
- Synthesis-structure map [C-stress-fatigue-shape](../../methodology/synthesis_structure_map.md#3-cluster-table-s%E2%82%81-pre-registration) §3 cluster row (declared 2026-06-23, lock r3 2026-06-24).
- Map [T-stress-fatigue-pacing](../../methodology/synthesis_structure_map.md#4-topic-table-s%E2%82%82-pre-registration) §4 topic row the cluster feeds (forward pointer for Stage S₂).
- Map [K-stress-fatigue-monitoring](../../methodology/synthesis_structure_map.md#5-construct-table-a-pre-registration) §5 construct row the topic feeds (forward pointer for Stage A — Stage S₁ does NOT cross §3.10).
- Limitations doc cross-refs for cited L-IDs: [`research_line_limitations.md`](../../methodology/research_line_limitations.md) §3 L1, L2, L3, L4, L6, L7; §5 citation requirements row for `cluster-*.md`.
- Non-binding seed notes: [`_synthesis_seed_notes_2026-06-23.md`](../../methodology/_synthesis_seed_notes_2026-06-23.md) §2 — cited as descriptive context (the r1 sketch's framing partially matched + partially mis-characterised the inverse-direction curvature per the methodology-internal_synthesis-2026-06-24 review R1; this Stage S₁ does NOT inherit the sketch's reading as a constraint per `internal_synthesis.md` §7.6 anti-pattern; the sketch's main contribution surfaced here is the explicit "spec-mechanism vs shape-substance" framing the §4.4 rationale paragraph operationalises).
- Literature methodology anchors:
  - [Daza 2018](../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) — primary anchor for Stage S₁'s multi-test synthesis discipline (cited at §4.5 5b L1 + §4.7a cross-operationalisation convergence + §4.8 external-research scoping).
  - [Shamseer / CENT 2015](../../literature/methodology/shamseer_2015_cent_consort_nof1.pdf) — items 21+22 cluster-level limitations and generalisability.
  - [Tate / SCRIBE 2016](../../literature/methodology/tate_2016_scribe_single_case_reporting.pdf) — L4 participant-as-researcher transparency at cluster level.
  - [Natesan 2023](../../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf) — bar for defensible cluster-level coherence-call.
- [CONVENTIONS](../../CONVENTIONS.md) §3.4 crash-drop sensitivity at cluster level (per §5.7 of guide #3 — both members' crash-drop FLAGs fired but did NOT change the cluster reading direction; recorded at §4.5 5a).
- [`_plan_results_analysis_layer.md`](../../methodology/_plan_results_analysis_layer.md) §3.6 conflict-resolution rule; §3.10 hard predictive gate (Stage S₁ does not cross); §3.12 commentary boundary (Stage S₁ does not carry).

---

## §11 Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-25 | Drafted r1 (DRY-RUN) | Reviewer-mode-with-authorization by `/research-interpret synthesise cluster-stress-fatigue-shape` skill in dry-run dispatch. Both member Stage I `interpretation.md` artefacts (HA-C3.md + HA-C3p.md, DRAFT r1 dry-run) consumed as upstream gate per guide #3 §9.2; no cascade-arrow upstream cluster precondition (C-stress-fatigue-shape is stand-alone). §4.4 coherence call DEFAULTED to PARTIALLY CONCORDANT per default-to-preserve framing; user judgment-call between CONCORDANT and PARTIALLY CONCORDANT logged to `_open_inputs.md` OI-003. **Drift triggers registered** (manual-pending-skill): (1) any constituent member's `interpretation.md` re-examined or downgraded; (2) a new HA joins the cluster (per map update — third sister-HA per §4.8 own-research); (3) cited methodology MD changes lock-version (especially [`research_line_limitations.md`](../../methodology/research_line_limitations.md), guides #1+#2, and the Wiggers / CONVENTIONS §3.1 anchors); (4) ≥6 months elapse since lock. **STATUS: NOT LOCKED — awaiting (a) user acceptance + (b) fresh-session `/research-review` per `_plan_results_analysis_layer.md` §4.** |
