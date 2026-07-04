# HA-C3p — interpretation (Stage I)

**Status**: **LOCKED r1 by user acceptance 2026-06-25** per §11 step 10 Phase A.7. Drafted 2026-06-25 by `/research-interpret interpret HA-C3p` skill in dry-run dispatch per §11 step 8 (skill since LOCKED r4). Phase A.2 §4.6 null prior recorded (same as A.1 sister); A.7 user-acceptance lock event closes Phase A. Sister-HA interpretation to HA-C3.md's; both lock together as the cluster's Stage I foundation. Awaiting fresh-session `/research-review` per locked-plan §4 row.

## Authorship

Drafted 2026-06-25 by Claude (Opus 4.7, 1M context) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../CONVENTIONS.md#12-producer-vs-reviewer-mode), via the `/research-interpret interpret HA-C3p` skill invocation in §11 step 8 dry-run dispatch. Authorising user: Willem. Fresh-session `/research-review` peer-check required before LOCK per [`_plan_results_analysis_layer.md`](../../methodology/_plan_results_analysis_layer.md) §4.

---

## 1. Target HA + verdict

- **HA ID**: HA-C3p r2
- **Pre-reg lock date**: 2026-06-23 (commit `c0148ca`)
- **Result lock date**: 2026-06-23
- **Stage D audit lock date**: 2026-06-25 (DRAFT r1, dry-run, pending user acceptance)
- **Headline verdict from `result.md`** (verbatim): **PARTIAL (2-of-3 conditions MET)**
- **Stage D verdict-trust call**: **TRUSTED**
- **Operationalisation summary** (one sentence, copying pre-reg §4): same-day `all_day_stress_avg × gevoelscore` cross-day-aggregate dose-response shape test on §5.A Stratum 4 unmedicated sub-arm, binned at **personal-baseline-anchored equal-N quintile bins** computed on the full Stratum 4 pool (n=1351; bin boundaries `[0, 28, 31, 34, 37, 100]` pinned to snapshot SHA `d0ff9253...`), 3-condition gated verdict per §5.1.
- **Synthesis-structure map cluster**: [C-stress-fatigue-shape](../../methodology/synthesis_structure_map.md#3-cluster-table-s%E2%82%81-pre-registration). Sister HA in cluster: HA-C3 v2.

## 2. What the data shows

§5.A unmedicated sub-arm n=581 (matches HA-C3 v2 primary cell); stress median 34.00; gevoelscore median 4.00. Full Stratum 4 pool n=1351 (used for bin-edge derivation per pre-reg Locked decision 1 cross-arm cleanliness rule).

Unmedicated per-bin distribution: Q1[0,28) n=45 mean=3.822; Q2[28,31) n=80 mean=4.138; Q3[31,34) n=129 mean=4.271; Q4[34,37) n=138 mean=4.290; Q5[37,100] n=189 mean=4.016. Bin-mean trajectory peaks at Q4 (mean 4.290) with monotone-increasing pattern Q1→Q4 and decline at Q5 — descriptively non-monotone (inverted-U-ish shape; peak in upper-mid quintile range).

Adjacent-bin step magnitudes (m_low − m_high): Q1-Q2 = -0.315 (rises); Q2-Q3 = -0.134 (rises); Q3-Q4 = -0.019 (essentially flat); Q4-Q5 = +0.274 (drops). The pattern is rise-to-peak-then-drop — not the SUPPORTED monotone-decreasing with accelerating-decrement direction.

Full Stratum 4 per-bin (descriptive only): Q1 n=248 mean=4.379; Q2 n=253 mean=4.443; Q3 n=294 mean=4.483; Q4 n=251 mean=4.466; Q5 n=305 mean=4.210. Similar inverted-U shape on the full pool.

Right-shift observation per pre-reg §4.1 + §8 caveat 4 (surfaced in `result.md` §2): unmedicated stratum is right-shifted relative to full Stratum 4 pool (Q1 share 7.7% unmed vs 18.4% full pool; Q5 share 32.5% unmed vs 22.6% full pool). Consistent with citalopram's CONFIRMED +0.57/mg `all_day_stress_avg` β per [`citalopram_dose_response_stress_mean_sleep §5.6.1`](../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read). Cross-test validation of the recalibration finding at a different operationalisation level.

Three-condition test results (per `result.md` §3): (a) Jonckheere-Terpstra J*=+0.267, p=0.5925 (FAIL — trend not monotone-decreasing); (b) S = mean(D²_2, D²_3, D²_4) = -0.1964, p=0.0018 (PASS — convexity contrast significant, S<0 direction); (c) spline F=+19.55 (block-permutation p=0.0020; spline 2nd-deriv sign at ≥ 3 of 4 contributing midpoints NEG per `result.md` §3 row notation "3 of 4 midpoints negative"). 2-of-3 MET; no wrong-direction override fires because pre-reg §5.1 spec does not have HA-C3 v2's positive-spline-2nd-deriv-at-majority override structure (HA-C3p's spec treats sign agreement as a PASS condition rather than as a wrong-direction override). Verdict: **PARTIAL (2-of-3 conditions MET)**.

Companion contrast c·m with c=(+2, -1, -2, -1, +2) = -1.2938 (p=0.0008; consistent direction with S). Spearman ρ = -0.0298 (p=0.4738, n=581; opposing-model linear test essentially flat — same value as HA-C3 v2 because same n=581 substrate).

Pairwise adjacent-bin Mann-Whitney with Holm step-down (4 pairs): Q1-Q2 Holm-adj p=0.5333 (no); Q2-Q3 Holm-adj p=0.5333 (no); Q3-Q4 Holm-adj p=0.9106 (no); Q4-Q5 Holm-adj p=0.1029 (no). **None of the adjacent-bin comparisons survive Holm correction at α=0.05** — the bin-mean trajectory's curvature is significant at the contrast/spline level but not at the pairwise-comparison level after multiplicity control.

Sensitivity arms: §5.B dose-adjusted cross-phase (n=1351) REJECTED at 0-of-3; z-scored 28d-lagged sensitivity (n=567) REJECTED at 1-of-3 (p_a=0.9034, p_b=0.0194 PASS, p_c=0.0886 FAIL) — partial concordance with primary on the curvature contrast (b) PASS but no spline support (c); crash-drop sensitivity S(full)=-0.1964 vs S(no-crash)=-0.0331 (n=503) — standardised |Δ S|=0.1771, sign-change=False, FLAG fired (does NOT modify §5.1 verdict). Train/validate M3 overlay: train S=-0.251 (n=482); validate S=+0.011 (n=99) — divergence noted per `train_validate_split_fate.md §5` as descriptive. T+1 lagged: S=-0.222 (n=581).

Stage D verdict-trust call: TRUSTED. A2 BACKSTOPPED-partial (shared with HA-C3 v2 A2; per-channel missingness audit on `all_day_stress_avg` is the shared closure path).

## 3. What the verdict licenses

The verdict licenses **the within-operationalisation partial-positive claim with the 2-of-3 structure preserved**:

> The personal-baseline-anchored 5-quintile-bin operationalisation of the stress→fatigue convex-cost claim — specifically equal-N quintile bins computed on the full Stratum 4 pool (n=1351, snapshot SHA `d0ff9253...`) and applied to the §5.A unmedicated sub-arm via cross-arm-cleanliness re-use of edges — is **PARTIAL on this corpus's Stratum 4 unmedicated primary cell**, with **2 of 3 pre-registered conditions MET**: (b) convexity second-difference contrast S = mean(D²_2, D²_3, D²_4) = -0.1964 PASSED (significantly negative, p=0.0018, direction matches the "accelerating-decrement / concave-down chord" framing); (c) spline non-linearity F=+19.55 PASSED (block-permutation p=0.0020; spline 2nd-deriv sign at 3 of 4 contributing midpoints NEGATIVE per the pre-reg's ≥3-of-4 bar). Condition (a) Jonckheere-Terpstra monotone-decreasing trend FAILED (p=0.5925, n.s.; direction not monotone-decreasing).

Effect-size summary: bin-mean trajectory Q1=3.822 → Q2=4.138 → Q3=4.271 → Q4=4.290 → Q5=4.016 (peak at Q4 = upper-mid quintile range = stress 34-37); convexity statistic S=-0.1964 (significantly negative); spline non-linearity highly significant. The (b) + (c) PASSED + (a) FAILED configuration is the **"non-monotone inverted-U / threshold-pattern alternative shape"** branch per pre-reg §7.4 + §9.3 framings, with HA-C3p's spec treating this as PARTIAL rather than as wrong-direction-override-REJECTED (per the HA-C3 v2 vs HA-C3p spec-difference noted in HA-C3p result.md §6 cross-test reading and in HA-C3p pre-reg §1's 4-cell agreement matrix framing).

Per CONVENTIONS §4.3 confirmatory framing: the test set out to confirm or refute Wiggers' convex-cost direction on the participant's own stress register; the result is a within-operationalisation PARTIAL with the missing condition (a) preserved as informative per guide #2 §5.3 — the curvature exists (per (b) + (c) PASS) but in the inverse-of-monotone-decreasing direction (per (a) FAIL).

Per Stage D TRUSTED: no PROVISIONAL narrowing applies; the licensed claim stands at full strength per the operationalisation's evidence.

## 4. What the verdict does NOT license

Four predictable overclaim shapes per guide #2 §4.4:

1. **PARTIAL does NOT mean "the underlying Wiggers convex-cost hypothesis is partially confirmed."** The 2-of-3 met configuration captures **curvature in the inverse direction** from Wiggers' monotone-convex prediction; PARTIAL is the claim shape that the data has **detectable non-linear structure that is NOT monotone-decreasing**. Collapsing PARTIAL into "weakly SUPPORTED" is the §7.6 anti-pattern (synthesis-as-counting fallacy at the per-HA layer); the missing condition (a) is informative and preserved.

2. **PARTIAL with (b) + (c) PASS does NOT license "the inverted-U / threshold-pattern alternative shape claim is SUPPORTED."** Per pre-reg §8 caveat 5 + §7.4: HA-C3p does NOT pre-commit to an inverted-U alternative claim; promoting that observation to a SUPPORTED-of-inverted-U claim would require a separate §3.2 fresh-session redraft to HA-C3p-v2 (or HA-C3-v3) with the alternative-shape claim as the primary headline cell. The §3 licensed claim stays at "PARTIAL on the convex-cost operationalisation, with (a) FAILED in the non-monotone direction the inverted-U shape would predict" — the inverted-U is **a caveat-class prior informing interpretation, not a substantive output of this artefact**.

3. **PARTIAL does NOT license a causal-mechanism claim** about why the inverted-U shape exists. Curvature detection is descriptive characterisation of mapping shape, not causal mechanism. Candidate mechanisms (sympathetic-arousal-load saturation, conserving-everything-days confound, circadian-clustering confound, etc.) are §4.8 own-research follow-up territory; Stage I records the operationalisation-bound PARTIAL without mechanism overreach.

4. **PARTIAL on this corpus does NOT mean "the same PARTIAL would replicate on any other comparable corpus."** Per the §4.5 L-ID block: L1 single-subject reach bounds the inference; group-level confirmation requires the §4.8 external-research track. **Cluster-level reading is Stage S₁'s job** — HA-C3p PARTIAL + HA-C3 v2 REJECTED is the per-HA evidence the cluster S₁ synthesises; Stage I does not pre-empt the coherence call.

## 4.5 Caveats narrowing the claim (with L-ID citation block)

### 5a. Pre-reg + audit caveats

From pre-reg §8 (14 caveats):
- Power-calc dispatch inapplicable per Daza 2018 (§8 caveat 1).
- Sister-pre-reg framing — HA-C3p tests the underlying convex-shape claim on personal-baseline-anchored bins; HA-C3 v2 tests Wiggers' verbatim 30→40 numerical anchor; 4-cell agreement matrix lives in HA-C3p result.md §6 (§8 caveat 2).
- [CONVENTIONS §3.1](../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline framing — pool-anchored quintile bins; z-scored-vs-rolling-baseline as §4.8(b) sensitivity arm (§8 caveat 3).
- Citalopram-channel inheritance + right-shift unmedicated bin observation (§8 caveat 4); cross-test validation of dose-modulation recalibration.
- HA-C3 v1 partial-pool non-monotone observation as caveat-class prior (§8 caveat 5); HA-C3p does NOT pre-commit to an inverted-U alternative claim.
- n=1 single-subject (§8 caveat 6); operational vs mechanistic (§8 caveat 7); crash-day inclusion structural fragility (§8 caveat 8); no causal-direction inference (§8 caveat 9); bin-edge snapshot pinning per §4.1 Gate 5 (§8 caveat 10); independent-obligations block (§8 caveat 11); drafting context disclosure (§8 caveat 12); Wiggers phrasing qualitative (§8 caveat 13); sister-test cross-references (§8 caveat 14).

From Stage D `descriptive_audit.md` §3 + §5: A2 BACKSTOPPED-partial (shared closure path with HA-C3 v2).

### 5b. L-ID citation block

Per the synthesis-structure map's §3 C-stress-fatigue-shape row L-IDs column: cluster L-IDs = L1, L2, L3, L4, L6, L7 (L5 NA). Stage I cites the subset applying to this HA's primary signals:

> *Cites L1 (single-subject reach)*: this verdict is about one subject's stress-fatigue dose-response shape on the personal-baseline-anchored quintile-bin operationalisation; per Daza 2018 N-of-1 inference reach, PARTIAL here adds one data point to the construct-level question of whether the participant's mapping has detectable curvature, not a settlement of the group-level Wiggers convex-cost claim; cross-operationalisation Stage S₁ reading (alongside HA-C3 v2 sister verdict) + external-literature Stage S₂ positioning are the next-step reach bounds.

> *Cites L2 (era confounds)*: HA-C3p §5.A primary cell ran on Stratum 4 unmedicated only (matches HA-C3 v2 scope per `lc_era_temporal_segmentation.md` Stratum 4 + unmedicated phase). Full Stratum 4 pool (n=1351) was used for bin-edge derivation per Locked decision 1 cross-arm cleanliness, but the **headline verdict cell is unmedicated-only**; cross-phase reading is §5.B descriptive sensitivity arm only (REJECTED 0-of-3; does NOT promote). The right-shift unmedicated bin observation (per pre-reg §4.1 + §8 caveat 4) is itself a cross-phase L2 manifestation: the citalopram dose-modulation compresses the stress range in medicated phases; the unmedicated phase populates higher quintiles disproportionately. This is a substantive cross-test validation of the recalibration finding, but it does NOT promote any cross-phase verdict to primary.

> *Cites L3 (device generations)*: same as HA-C3 v2 — `all_day_stress_avg` is FR245 Elevate-V3-derived Garmin signal; PARTIAL verdict is constrained to within-device-generation reach.

> *Cites L4 (analyst-is-subject)*: HA-C3p was prior-driven by [CONVENTIONS §3.1](../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline discipline + the Wiggers underlying-mechanism reading (per pre-reg §2(a) + §2(b)); per CONVENTIONS §4.3 the test is confirmatory; §4.6 lived-experience-prior reconciliation below records the prior explicitly. L4 mitigation reach per limitations doc r3 §3 L4: fresh-session `/research-review` peer-check (pending post-dry-run); producer-vs-reviewer split honored via reviewer-mode-with-authorization status.

> *L5 (presence-conditioned data layer) NA*: same as HA-C3 v2 — no v24 primary signals; `all_day_stress_avg` and `gevoelscore` daily_computed-only. The map's §3 row marks L5 NA for the cluster; this HA does not trigger L5 independently.

> *Cites L6 (self-reporting)*: same as HA-C3 v2 — `gevoelscore` is the outcome; self-report noise floor applies per L6. Bin-mean differences across HA-C3p quintile bins are particularly small in absolute units (Q1 mean=3.822 vs Q4 mean=4.290 = 0.468 gevoelscore-points across the full bin range; adjacent-bin step magnitudes Q1-Q2=-0.315, Q2-Q3=-0.134, Q3-Q4=-0.019, Q4-Q5=+0.274 all sit within the per-day self-report noise envelope). The PARTIAL verdict's detection of statistically-significant curvature at the contrast/spline level despite all four adjacent-bin Mann-Whitney comparisons failing Holm correction is structurally consistent with **low signal-to-noise per pairwise comparison + cumulative signal across the binned trajectory** — a pattern the L6 self-report noise floor caveat illuminates.

> *Cites L7 (survivorship)*: same gating discipline as HA-C3 v2 (LC era + non-NaN both columns + April 2024 cluster excluded + first-21-days device-baseline-warmup excluded); §5.A unmedicated sub-arm n=581 represents the gated subset. Per-bin n on §5.A: Q1=45 (the borderline cell still meeting the ≥30 bar but smaller-n than other quintile bins); Q2-Q5 well above. The Q1 sub-cell sub-30 risk per `train_validate_split_fate.md`-style discipline does not materialise here (n=45 ≥ 30); but the bin-mean for Q1 (3.822) sits in a thinner cell than the other quintiles, narrowing the L7 confidence on the Q1 anchor point.

## 4.6 Lived-experience prior reconciliation

**STATUS: USER-ARTICULATED 2026-06-25** per §11 step 10 Phase A.2
rollout interview. DEFAULTED-PENDING-USER-INPUT placeholder
superseded; the dry-run default-reading is documented at the end of
this section for traceability but does NOT carry forward.

**The prior** (user verbatim, 2026-06-25): same null prior as
HA-C3 v2 (§4.6 of [`HA-C3.md`](HA-C3.md)). The subject's lived-
experience prior on the Wiggers convex stress-fatigue mapping at
the personal-baseline quintile-bin operationalisation was **null**
— no expectation about the subject's own stress-fatigue mapping in
any binning scheme; no awareness of a pattern from lived experience
prior to the test running. The personal-baseline binning shift did
not produce a separate prior; the subject's null state applied
across both Wiggers-verbatim (HA-C3 v2) and personal-quintile
(HA-C3p) operationalisations of the same construct.

**The verdict** (per §4.3): HA-C3p PARTIAL with 2-of-3 conditions
met; (b) PASS (S = −0.1964, p = 0.0018) + (c) PASS (spline p =
0.0020 with 3-of-4 contributing midpoints negative) detect
curvature; (a) FAIL (Jonckheere-Terpstra p = 0.5925) because the
quintile trajectory peaks at Q4 = inverted-U shape.

**Agreement / divergence**: NOT APPLICABLE in the standard sense
(same reasoning as HA-C3 v2 §4.6). The prior was null — neither
agreement nor divergence between "nothing expected" and the
inverted-U finding can be cleanly asserted. What the §4.6 records
honestly:

- HA-C3p produces the same kind of descriptive discovery as
  HA-C3 v2: inverted-U shape the subject had NOT noticed lived.
- The cross-operationalisation agreement (both HA-C3 v2 + HA-C3p
  detect inverted-U via different binning schemes) is a substantive
  cluster-level finding for Stage S₁ — but it does NOT modify
  either HA's §3 licensed claim individually.
- The Wiggers'-prior framing (the canonical claim from the
  handleiding) WAS the test's prior on both HAs, but the
  *subject's* prior on Wiggers'-direction-for-them was null on
  both. The two priors are distinct; only the subject's null prior
  is recorded here per guide #2 §4.6.

**Implication for §3 licensed claim**: per the guide #2 §4.6 r2
agreement-does-not-strengthen rule + the L4 caveat, the verdict's
licensed claim (per §4.3) stands as the operationalisation-bound
descriptive shape claim (PARTIAL with 2-of-3 structure preserved
+ inverted-U direction). The null prior does NOT modify the §3
licensed claim in either direction.

**Routing**: no cluster-level reconciliation work needed at Stage
S₁ on prior-vs-verdict per this HA specifically. Stage S₁ on
C-stress-fatigue-shape proceeds on the cross-operationalisation
verdict-shape evidence per guide #3 §5.2 coherence-call mapping
(both HA-C3 v2 + HA-C3p detect inverted-U; cluster-level reading
is PARTIALLY CONCORDANT per dry-run §5.2 worked example).

**L4 meta-recursion acknowledgment**: per guide #2 §4.6 closing
paragraph and limitations doc r3 L4: the user articulated the
prior directly in §11 step 10 Phase A.2 interview (2026-06-25); no
Claude-dispatched articulation. The dry-run default-reading
contradicted the user's actual null prior (the same L4-inflation
pattern observed in HA-C3 v2 §4.6); the placeholder mechanism
inflated a prior the subject didn't hold. Future dry-run defaults
should treat "unspecified user prior" as null-prior-default.

**Dry-run default-reading (superseded; recorded for traceability
only)**: at dry-run dispatch the placeholder suggested "the user's
lived-experience prior on the stress→fatigue mapping at the
personal-baseline-anchored quintile-bin operationalisation is most
likely characterised by the expectation that the participant's own
stress range should show a clearer monotone-decreasing relationship
than Wiggers' verbatim numerical anchor allows." This default-
reading was Claude's reasonable-default guess derived from the
session handoff brief's framing ("HA-C3p goes further to see if we
can find the mechanism Wiggers is describing"); the actual user
articulation (2026-06-25) was *null prior*, contradicting the
default. The dispatcher conflated the *researcher's* (Wiggers's)
prior + the *handoff brief's* framing with the *subject's* prior
— an L4-inflation pattern worth documenting for skill r5+
absorption.

## 4.7 Closure-path statement

PARTIAL verdict; closure-path is operational per guide #2 §4.7 for "k-of-N conditions MET" framing.

**Closure-path for the (a) FAIL condition**: condition (a) Jonckheere-Terpstra monotone-decreasing FAILED because the bin-mean trajectory is non-monotone (inverted-U with peak at Q4). The (a) condition would be MET only if the data showed a monotone-decreasing pattern, which the current data does not. **Three operational paths to upgrade the verdict beyond PARTIAL**:

1. **A different bin scheme that resolves the (a) FAIL** — if the inverted-U peak is a binning artefact (e.g., the peak at Q4 disappears under a different bin-edge discipline), a third-sister-HA on rolling-window-baseline bins would test this. **NOT pre-registered**; routing to §4.8 own-research track.

2. **A revised pre-reg with the inverted-U direction as the SUPPORTED hypothesis** — HA-C3p-v2 (or HA-C3-v3) with inverted-U / threshold-pattern as the primary direction-of-effect. Under that pre-reg the (a) condition would be reframed (e.g., "Jonckheere-Terpstra test for inverted-U trend per the umbrella-test discipline"). The current PARTIAL would convert to SUPPORTED under that pre-reg's verdict bar. **Out of scope for current pre-reg**; routing to §4.8 own-research track.

3. **A larger n on the gated cell that converts the non-monotone Q1→Q4 rise into significance** — if the apparent rise from Q1=3.822 to Q4=4.290 is a real monotone-increasing signal (the inverse direction of (a)), more data would let condition (a) reach significance in the **wrong direction**, triggering a different verdict band. **NOT promoted as closure-path**; this is hypothetical-only and routing belongs to §4.8 own-research.

## 4.8 Follow-up suggestions

### Own-research track

- **Third sister-HA on rolling-window-baseline binning** (same as HA-C3 v2 §4.8 own-research entry; shared closure path) — adds a third independent operationalisation to the C-stress-fatigue-shape cluster, tightening Stage S₁ cross-operationalisation reading.

- **HA-C3p-v2 with inverted-U / threshold-pattern as primary direction** — per pre-reg §8 caveat 5 explicit out-of-scope framing; routing per `hypothesis_lock_process.md`.

- **Per-channel missingness audit on `all_day_stress_avg`** — shared closure path with HA-C3 v2 §4.8.

- **Pre-registered descriptive run characterising the inverted-U peak location and width on the participant's distribution** — not a hypothesis test, a descriptive characterisation that would inform any future inverted-U pre-reg's bin-edge and peak-location pre-commitments. S effort.

### External-research track

- **Cohort study of inverted-U / threshold-pattern stress→fatigue mapping in LC / ME/CFS populations at group level** (same as HA-C3 v2 §4.8 external-research entry; L1-scoped because N=1 corpus cannot settle group-level question).

- **Cross-instrumentation comparability study Garmin `all_day_stress_avg` vs subjective-stress-rating** (same as HA-C3 v2 entry; L3-scoped).

- **Group-level test of personal-baseline-vs-absolute-anchor operationalisation choice for stress→fatigue mapping** — does the personal-baseline-anchored framing produce different findings than the absolute-numerical anchor framing at group level? We cannot run this ourselves because **L1** + the operationalisation-choice question requires multiple subjects to disentangle (which framing is more accurate?) from (which framing is more sensitive on a given subject?). Closing this would tighten the project-wide [CONVENTIONS §3.1](../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline discipline's group-level evidence base.

## 4.9 `open_inputs` block

| # | What is missing | What it blocks | Cheapest acquisition path | Fallback claim available |
|---|---|---|---|---|
| 1 | User confirmation of lived-experience prior for HA-C3p (per §4.6) | §4.6 reconciliation completion | One interview question per §8.3 seed in `verdict_to_inference.md` | DEFAULTED-PENDING-USER-INPUT placeholder with one-sentence default-reading |
| 2 | Per-channel missingness audit on `all_day_stress_avg` (shared with HA-C3 v2 entry) | Tightens §4.5 L7 citation | S effort per stocktake §3 Shared gap 3 | TRUSTED stands with L7 narrowing caveat |
| 3 | Stage S₁ cluster-level reading on C-stress-fatigue-shape for the cross-test joint interpretation (HA-C3 v2 REJECTED + HA-C3p PARTIAL agreement matrix) | A complete joint reading of the two sister HAs (currently each Stage I cites the other as cluster cross-reference but does NOT pre-empt cluster coherence) | Stage S₁ session at `/research-interpret synthesise C-stress-fatigue-shape` (next downstream artefact in this dry-run dispatch) | Per-HA Stage I licensed claims stand independently; cross-test joint reading deferred to Stage S₁ |

## 4.10 Cross-references

- HA-C3p r2 [`hypothesis.md`](../hypotheses/HA-C3p/hypothesis.md) and [`result.md`](../hypotheses/HA-C3p/result.md).
- Stage D audit [`descriptive/HA-C3p/descriptive_audit.md`](../descriptive/HA-C3p/descriptive_audit.md).
- Synthesis-structure map [C-stress-fatigue-shape](../../methodology/synthesis_structure_map.md#3-cluster-table-s%E2%82%81-pre-registration) cluster row.
- Sister-HA interpretation [`HA-C3.md`](HA-C3.md) (the Wiggers-verbatim sister; companion Stage I in this dry-run dispatch).
- Forward pointer to Stage S₁: [`synthesis/cluster-stress-fatigue-shape.md`](../synthesis/cluster-stress-fatigue-shape.md).
- Limitations doc cross-refs: [`research_line_limitations.md`](../../methodology/research_line_limitations.md) §3 L1, L2, L3, L4, L6, L7.
- [`_synthesis_seed_notes_2026-06-23.md`](../../methodology/_synthesis_seed_notes_2026-06-23.md) §2 (caveat-class advisory; same flagged-out-of-scope status as HA-C3 v2 §4.10).
- Literature methodology anchors: Daza 2018, CENT 2015, SCRIBE 2016, Natesan 2023.
- [`_plan_results_analysis_layer.md`](../../methodology/_plan_results_analysis_layer.md) §3.10 (Stage I does not cross); §3.11 (own + external tracks); §3.12 (Stage I does not carry commentary; deferred to Stage A K-stress-fatigue-monitoring tier-1).
- CONVENTIONS [§1.2](../../CONVENTIONS.md#12-producer-vs-reviewer-mode); [§3.1](../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds); [§4.3](../../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory).

---

## §10 Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-25 | Drafted r1 (DRY-RUN) | Reviewer-mode-with-authorization by `/research-interpret interpret HA-C3p` skill in dry-run dispatch. Stage D `descriptive_audit.md` (DRAFT r1, dry-run, TRUSTED) consumed as upstream gate per guide #2 §9.2. §4.6 DEFAULTED-PENDING-USER-INPUT. **Drift triggers registered**: (1) HA-C3p `result.md` re-runs; (2) Stage D `descriptive_audit.md` re-examined; (3) cited methodology MD changes lock-version; (4) ≥6 months elapse since lock. **STATUS: NOT LOCKED — awaiting (a) user acceptance + (b) fresh-session `/research-review`.** |
