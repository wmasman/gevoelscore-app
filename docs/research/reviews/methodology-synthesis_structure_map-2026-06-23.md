# Methodology review — synthesis_structure_map.md (r1, 2026-06-23)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the drafting session. Fresh session — no exposure to the drafting context; doc-only knowledge.
**Target**: `docs/research/methodology/synthesis_structure_map.md` (r1, 2026-06-23, ACCEPTED rows, NOT LOCKED).
**Review date**: 2026-06-23
**Standards applied**: CONVENTIONS §1.2 (reviewer-mode discipline), §2.2 (four-input bar), §3 (statistical-hygiene audit hooks where they bear), §4 (caveats-vs-a-priori, prior-driven hypotheses, presence-conditioning), §7 (cross-references); the locked plan `_plan_results_analysis_layer.md` r4 §3.6 (the layer rule that binds), §6.3 (per-cluster pre-declaration), §3.10 (predictive-quality measures), §3.11 (follow-up suggestions), §11 step 5 (the implementation step); `research_line_limitations.md` r3 §5 (citation-requirement table); the four ready HAs' pre-regs (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo); the parent methodology MDs (`bout_level_recovery_dynamics.md`, `citalopram_phase_stratification.md`, `hrv_proxy_via_stress.md`).

---

## 1. Overall verdict

**REVISION RECOMMENDED.** The map is structurally sound and the four-input reasoning is fit for a layer-wide pre-registration of this shape. It correctly enforces the §3.6 anti-cherry-pick discipline by appending-with-lock-entries, faithfully seeds from the stocktake §9 decisions, and surfaces enough of the upstream architecture (parent MDs, HA pre-regs, stocktake) to be auditable cold. However, several rows under-surface load-bearing distinctions that S₁ / S₂ / A guides will need to operate on, and one §3-§4 section drifts into a synthesis-pre-decision that the §3.6 conflict-resolution rule reserves for stage execution. None of the findings is blocking in the sense of requiring a re-draft; all are absorbable as targeted in-place fixes plus one §3 framing change. The map can plausibly LOCK after absorbing the items in §7 below, without a second fresh-session review pass (per the user's existing Option-γ §3.6-compression pattern on the §3 changes that would be substantive vs the §4 changes that are mechanical wording).

---

## 2. Four-input bar findings (CONVENTIONS §2.2)

The map is a layer-wide pre-registration MD specified by the locked plan §3.6, so its §2.2 obligations are met by being *the* methodology MD for the structural-pre-registration choice; it inherits its four-input reasoning from `_plan_results_analysis_layer.md` §3.6 (which itself went through the §11 step 1 fresh-session review). What this MD itself owes is the four-input reasoning for the *initial seeding choice* (which HAs cluster, which topics, which constructs), not for the §3.6 layer rule itself.

| Input | Verdict | Reasoning |
|---|---|---|
| **Best-practices standards** | PARTIAL | The §3.6 layer rule it implements is itself best-practice (pre-register structural choices before stage execution), correctly inherited from the locked plan. But the map does not explicitly name the standards that bind cluster-membership reasoning at the synthesis level (no SCRIBE / CENT / WWC anchor; no Daza 2018 reference for the N-of-1-cluster-constellation problem). The seeded clusters are reasoned by *operationalisation-overlap analogy to the HAs' pre-reg framing*, which is project-internal best-practice but not externally anchored. Acceptable as a producer-mode pre-registration map (not all map rows need to bear external citations) but the omission should be acknowledged. |
| **Established literature** | PARTIAL | Topic-cell entries cite published-literature references (Wiggers handleiding for T-stress-fatigue-pacing; Marques 2023 + Mooren 2023 + Ryabkova 2024 + van Campen 2022 for T-within-day-recovery; Suh 2023 + Mooren 2023 + Berntson 1997 + Shaffer 2017 for the reserved T-hrv-in-lc). Literature is named at the topic row, but **none of the cluster rows reference literature**, even where a cluster's shared-construct cell makes a substantive claim that an external reference would discipline (e.g., the §3 "inverted-U / threshold-like rather than monotone-convex" advisory reading would benefit from a citation that grounds the inverted-U shape as a real construct, not a project-internal post-hoc framing). |
| **Tradeoff vision** | PASS | The map is honest about its tradeoffs at §6 (defer-and-grow vs upfront-full-map; the §3.6 conflict-resolution rule that halts S₁ rather than allowing in-flight map edits). §2 correctly cross-refs the defer-and-grow choice to stocktake §9.2 D2. |
| **Research limitations + objectives** | PARTIAL | The map's §2 names that 24 HAs are "deferred per defer-and-grow strategy"; that addresses the limitations-driven sequencing. But the systemic L1-L7 limitations from `research_line_limitations.md` r3 are listed only in §8 cross-refs, NOT integrated into the cluster / topic / construct row reasoning. Per `research_line_limitations.md` §5 citation-requirement table, **cluster-*.md MUST cite every limitation that touches any cluster member; topic-*.md MUST cite L1+L2+L4 unconditionally; construct-*.md MUST cite all seven with explicit applicability-or-NA**. The map is a layer-wide pre-registration of those downstream artefacts; it should at least surface that the downstream artefacts will inherit those citation obligations. Currently the limitations doc is bottom-of-page cross-reference only. |

**Net four-input bar**: PARTIAL across two inputs (best-practices, literature) and PARTIAL across the limitations input, with PASS on tradeoff vision. The PARTIALs are absorbable as targeted additions; no re-draft needed.

---

## 3. Per-table findings

### 3.1 Cluster table

**C-stress-fatigue-shape (HA-C3 v2 + HA-C3p)**. Boundary call is defensible. The two HAs are explicit sister pre-regs by their own §1 framing — HA-C3p's Authorship paragraph names HA-C3 v2 as the Wiggers-verbatim arm and HA-C3p as the personal-baseline sister, with a 4-cell agreement matrix at HA-C3p §1 explicitly framed as a cross-test reading. The shared construct cell ("non-linear stress→fatigue mapping per Wiggers convex-cost claim") is faithful to both HAs' §1 claims. The operationalisation-overlap note ("Independent operationalisations of the same construct") is correctly framed — both use the same substrate (`all_day_stress_avg` × `gevoelscore`) but Wiggers-verbatim 4-bin absolute anchor vs personal-quintile 5-bin. **Concern #1 (see §5.1)**: the framing "independent operationalisations of the same construct" is *the user's chosen framing* per HA-C3p §1 + Locked decision 5, and is *project-canonical* per CONVENTIONS §3.1. But the map cell does not surface that the cross-test agreement-matrix logic (the 4-cell SUPPORTED × SUPPORTED / SUPPORTED × REJECTED / REJECTED × SUPPORTED / REJECTED × REJECTED) is itself a synthesis structure that overlaps with §3.6's S₁ coherence-call structure. A reader of the cluster row alone cannot tell whether the S₁ coherence call IS the 4-cell agreement matrix, or whether the 4-cell matrix is a different artefact (per HA-C3p Locked decision 5 it lives in HA-C3p's result.md §6, which is the *result* layer, not the synthesis layer). This is unresolved structurally: when S₁ runs on this cluster, does it duplicate / supersede / cite the result-layer agreement matrix? The map should specify.

**C-bout-recovery (HA-C4c + HA11-bout-redo)**. Boundary call is more contentious. **Concern #2 (see §4.2)**: HA11-bout-redo is explicitly a **framework-validity gate** — its §1 Claim opens "*Pre-committed (framework-validity gate; NOT a substantive claim about Wiggers C4)*", and its §1 second paragraph reinforces "*It does NOT mean the bout-level operand SUPPORTS or REFUTES HA11 v1's substantive crash-precursor claim*". HA-C4c is the **substantive Wiggers C4 retest** — its title and §1 explicitly so. The map's shared-construct cell ("Within-day stress recovery / failure-to-return at bout resolution") and operationalisation-overlap note ("Same operand family ... HA11-bout-redo is the framework-validity gate ... HA-C4c is the substantive test") *correctly identify* the framework-vs-substance distinction. But the cluster *bundles* them under a single "shared construct" label that flattens the distinction at the S₁ coherence-call level. The map records the cascade ("HA-C4c §8 caveat 2 inherits HA11-bout-redo's PARTIAL framework-validity verdict") but does not flag that S₁'s coherence call on this cluster will need to treat the two verdicts asymmetrically: a PARTIAL on HA11-bout-redo means "the operand reproduces HA11 v1 within tolerance" (a methodology check), while a PARTIAL on HA-C4c means "the Wiggers C4 substantive claim is direction-correct-but-effect-or-significance-fails" (a substantive verdict). These are not commensurable along the same coherence axis. **Concern #3 (see §5.2)**: era-scope asymmetry. HA-C4c §4.2 is cross-phase pooled (`{unmedicated, buildup, consolidation, afbouw, post_afbouw}`); HA11-bout-redo §4.2 is unmedicated-only-locked-per-parent-MD-§5.5. The map cell does not surface this. HA-C4c includes an unmedicated-only sensitivity arm explicitly for cross-test comparability with HA11-bout-redo, but the primary cells of the two HAs are on different era-strata pools. S₁ coherence call needs to know which cells it is comparing.

**C-h05-successor (RESERVED)**. The reserved-slot framing is faithful to stocktake §9.1 D1 + the §6 lifecycle. Acceptable.

**C-hrv-proxy (RESERVED, HA07-proxy + HA08-proxy both TBD)**. The reserved-slot framing is faithful to stocktake §9.4 D4. **Concern #4 (see §5.3)**: putting both HA07-proxy and HA08-proxy in the same reserved cluster pre-decides their constellation before either pre-reg exists. The other reserved slot (C-h05-successor) reserves a single HA slot; this one reserves a slot already pre-bundling two HAs. The §3.6 lifecycle is "RESERVED → PROPOSED → ACCEPTED → LOCKED", and at the PROPOSED step the user signs off on the constellation. But here the constellation is partially pre-decided at RESERVED: "HA07-proxy and HA08-proxy will be in the same cluster." If at pre-reg time the two proxy HAs turn out to operationalise meaningfully different constructs (day-over-day vs multi-day slope, per HA07 vs HA08), the §3.6 conflict-resolution rule would route through a separate map-revision session. Worth flagging here rather than discovering it later.

### 3.2 Topic table

**T-stress-fatigue-pacing**. Construct cell is faithful. Literature row is reasonable (Wiggers handleiding + Appelman 2024 + ME/CFS pacing handbooks + energy-envelope literature). **Concern #5 (see §5.4)**: topic-to-cluster is 1:1 (one cluster feeds one topic). The locked plan §10.2 explicitly defers "topic-vs-cluster boundary" to drafting time of `external_contextualisation.md`. The map's current 1:1 default is sensible for an initial map, but the map should *surface* that future revisions may merge clusters into a single topic or fan a cluster to multiple topics. Currently §4's table-cell pattern reads as if 1:1 is the structural answer, not the defer-to-future-question answer.

**T-within-day-recovery**. Construct cell is faithful. Literature row is well-chosen for the construct. Same 1:1 concern as T-stress-fatigue-pacing.

**T-recovery-time (RESERVED)** + **T-hrv-in-lc (RESERVED)**. Both correctly stated as pending HA-pre-reg landing. Acceptable.

### 3.3 Construct table

**K-stress-fatigue-monitoring**. Tier-aspiration "monitoring (descriptive shape); informative-pattern blocked by single-cluster evidence and direction-anomaly with Wiggers' canonical claim" is reasonable. The §3.10 hard-predictive-gate framing is correctly invoked ("Predictive-use tier blocked at this stage"). The named pathway to tier-2+ ("a forward-validation HA testing 'tomorrow's gevoelscore predictable from today's stress bin'") is concrete enough to be actionable. **Concern #6 (see §5.5)**: per locked-plan §3.10, tier-2-or-above claims MUST report PPV + base rate + plain-language frame. The map says "informative-pattern blocked by single-cluster evidence and direction-anomaly". It does not say what the *fallback* tier looks like in PPV-with-base-rate terms at *monitoring* tier. Monitoring is tier-1, which §3.10 does not require PPV for — so this is technically fine. But the map should be explicit that monitoring is the §3.10-PPV-exempt tier; otherwise a downstream reader could infer that "monitoring (descriptive shape)" is some weakened form of tier-2 that escaped the §3.10 requirement.

**K-bout-recovery-signal**. Tier-aspiration "informative-pattern (effect-size demonstrated but small); predictive-use blocked by §3.10 hard gate" is reasonable. The predictive-feasibility cell correctly identifies "PPV-with-base-rate per §3.10 would need computation against crash base rate (~2/year residual per RESEARCH-REPORT §5.2 precedent)". Same §3.10 framing concern as K-stress-fatigue-monitoring: the informative-pattern claim does eventually require PPV per §3.10 (informative is tier-2 in the actionability translation table at locked plan §6.5). The map records this correctly.

**K-recovery-time (RESERVED)** + **K-hrv-proxy (RESERVED)**. Both correctly stated as pending. Acceptable.

---

## 4. Cluster-by-cluster findings

### 4.1 C-stress-fatigue-shape — boundary correct, framing under-specified

The cluster's two HAs (HA-C3 v2, HA-C3p) genuinely share the construct the cluster cell claims: non-linear stress→fatigue mapping per Wiggers' convex-cost claim. The shared substrate (`all_day_stress_avg` × `gevoelscore`) and the shared statistical machinery (Jonckheere-Terpstra + convexity contrast + spline non-linearity, both 3-condition gated) are operationalisation-overlap evidence that does not reduce to "tests of the same column" — they are two *independent* operationalisations of the convex-shape claim, one Wiggers-verbatim-anchored, one personal-baseline-anchored.

Whether they are "*independent* operationalisations" in the stronger sense locked plan §6.3 cares about (where "independent tests of the same construct" is much stronger evidence than "tests running on the same signal") is borderline. They share the substrate channel but differ in the bin scheme; per HA-C3p §1, the 4-cell agreement matrix between the two operationalisations is itself the cross-test evidence. The drafter has chosen "independent operationalisations of the same construct" framing, which I read as the right call — but the cluster cell should be more explicit that the *cross-bin-scheme* independence is what gives the cluster its evidence-strength, not the *cross-substrate* independence. Per locked-plan §6.3 anti-pattern: "three HAs running on the same signal are one piece of evidence, not three" — the cluster cell should preempt that reading.

### 4.2 C-bout-recovery — framework-vs-substance distinction is collapsed

The cluster cell ("Within-day stress recovery / failure-to-return at bout resolution") and operationalisation-overlap note ("Same operand family ... HA11-bout-redo is the framework-validity gate ... HA-C4c is the substantive test") do *name* the distinction, but the cluster *bundles* the two HAs as if S₁ will produce one coherence call across them. Per HA11-bout-redo §1 self-framing, its PARTIAL verdict is a methodology check (does the bout-level operand reproduce HA11 v1's SUPPORTED-on-train signal within ±10pp + direction + permutation-p?), not a substantive claim about within-day recovery. Per HA-C4c §1 self-framing, its (yet-to-run) verdict will be a substantive claim about Wiggers C4 (do heavy-T days produce more `did_not_return` bouts than non-heavy-T days?).

S₁'s coherence-call shapes per locked plan §6.3 are CONCORDANT / PARTIALLY CONCORDANT / CONFLICT / ORTHOGONAL. None of these maps cleanly onto a (framework-validity, substantive-test) pair. A PARTIAL on HA11-bout-redo (framework reproduces with caveats) plus a PARTIAL on HA-C4c (substantive direction-correct-but-effect-fails) is not naturally CONCORDANT (the verdict labels mean different things on different axes); it's not CONFLICT either; ORTHOGONAL is structurally closest but misses that the framework-validity verdict is a *gating precondition* for the substantive claim, not a co-equal co-finding.

The map cell records the cascade dependency ("HA-C4c §8 caveat 2 inherits HA11-bout-redo's PARTIAL framework-validity verdict"). What it does not do is route the S₁ guide on what coherence call to produce when one cluster member is a framework gate and the other is a substantive test. This is a real S₁-execution problem that the synthesis guide (#6.3) will hit on its first draft against this map. **This should be either**: (a) two separate clusters (C-bout-framework-validity for HA11-bout-redo; C-bout-recovery-substantive for HA-C4c), with HA11-bout-redo's verdict feeding HA-C4c's cluster as a precondition not a co-finding; OR (b) a single cluster as drafted, but with the cluster cell explicitly naming that S₁'s coherence call on this cluster treats HA11-bout-redo's PARTIAL as a *calibration-discount caveat propagated forward*, not as a co-equal verdict to be reconciled with HA-C4c's verdict on the same construct. The drafter likely intended (b), but the map does not state it. This is a required action.

The era-scope asymmetry (HA-C4c cross-phase primary + unmedicated-only sensitivity arm; HA11-bout-redo unmedicated-only parent-MD-locked) is a separate concern that compounds: when S₁ asks "do these two HAs reach the same conclusion on the same construct on the same data?", the answer for the primary cells is "no, because the data is different." HA-C4c's unmedicated-only sensitivity arm exists precisely to allow apples-to-apples comparison with HA11-bout-redo, but the map does not surface that the apples-to-apples comparison happens on a *sensitivity arm of one HA*, not on either HA's *primary cell*.

### 4.3 C-h05-successor — fine as reserved

No active constituent HAs; the reserved-slot framing is faithful to stocktake §9.1 D1. Acceptable.

### 4.4 C-hrv-proxy — pre-decision concern at reserved level

Reserving the slot is the right call per stocktake §9.4 D4. Pre-bundling HA07-proxy + HA08-proxy as the cluster's constituent HAs *before either pre-reg exists* is the concern. The cluster's "shared construct" cell ("HRV via stress-proxy operationalisation") is consistent with `hrv_proxy_via_stress.md` framing, but the parent MD describes HRV-proxy as enabling *multiple* downstream HAs that may operationalise differently (HA07 day-over-day vs HA08 multi-day-slope). Worth flagging that the constellation choice is forward-looking and should be re-confirmed when each successor pre-reg lands.

---

## 5. Cross-cutting concerns

### 5.1 The HA-C3 cross-test 4-cell matrix lives at HA-C3p result.md §6, not at S₁

Per HA-C3p Locked decision 5: "**HA-C3p result.md §6 open-questions** carries the 4-cell agreement matrix with HA-C3 v2 (not a separate cross-test reviews/ doc)". This is *cross-test interpretation at the result layer*. The synthesis-structure map's C-stress-fatigue-shape cluster places S₁ at the *synthesis layer*, downstream of both result.md files. The relationship between the result-layer 4-cell matrix and S₁'s synthesis-layer coherence call is not specified. Two possibilities:

- S₁ inherits / cites the 4-cell matrix as already-done cross-test reading, and the S₁ coherence call is the matrix's reading translated into CONCORDANT / PARTIALLY CONCORDANT / CONFLICT / ORTHOGONAL language.
- S₁ produces its own coherence call independently and the 4-cell matrix is descriptive context only.

The map does not specify. The cluster cell should clarify. (Recommended action; not required.)

### 5.2 §3 "Coherence read for active clusters" is borderline-pre-decision

§3's "Coherence read for active clusters" paragraph offers candidate joint readings for both active clusters with "S₁ session will make the actual call; this is not pre-decided here" disclaimers. The disclaimers are doing real work — they keep the map structural-only. But the actual candidate readings *are* substantive:

- C-stress-fatigue-shape: "the participant's stress-fatigue mapping has detectable curvature, but inverted-U / threshold-like rather than monotone-convex. Wiggers' direction (monotone-decreasing) does not match; Wiggers' mechanism (curvature/non-linearity) does."
- C-bout-recovery: "operand is fit-for-purpose; effect sizes are modest at the corpus's detection limits, consistent with the bimodal arousal pattern Cluster A hints at."

These are joint-claim sketches with directional content. They draw on the v1 partial-pool finding (B2→B3→B4 = 3.958 → 4.265 → 3.860) which both HA-C3 v2 and HA-C3p frame as **caveat-class prior** per CONVENTIONS §4.2 ("Caveats yes, a-priori claims no"). HA-C3 v2 explicitly does NOT pre-commit to an inverted-U claim ("v2 does not pre-commit to any inverted-U or threshold-pattern alternative claim" per §1). HA-C3p explicitly does NOT pre-commit either ("HA-C3p does NOT pre-commit to an inverted-U / threshold-pattern alternative claim" per §1, Locked decision 1 area).

The map's §3 candidate reading surfaces the inverted-U framing **before either test has run**, in a section titled "Coherence read for active clusters" of a methodology MD that S₁ will read as authoritative structural pre-registration. This is borderline data-peeking-by-other-means: even with the "S₁ session will make the actual call" disclaimer, the candidate-reading text plants the framing in the synthesis-layer's pre-registration MD. A downstream S₁ session reading this map cold *will* read the candidate reading and *will* be primed by it; that's why the candidate reading exists, to inform future work. But the structural-pre-registration MD is not the right place for joint-claim-sketches; the right place is `open_inputs` or a separate pre-S₁ "hypothesised joint readings to evaluate" document that S₁ explicitly evaluates against the data.

**Recommended action**: move §3's "Coherence read for active clusters" paragraph either (a) out of this MD entirely into an `open_inputs` block tagged "S₁ candidate joint readings to evaluate"; or (b) into a clearly-fenced "PRIOR JOINT-READING SKETCHES — caveat-class only, do not propagate into S₁ verdict language" section with stronger fencing than the current "S₁ session will make the actual call" sentence. The §3.6 conflict-resolution rule says the map should record *structure*, not *synthesis*; the candidate readings cross that line even when hedged. This is required action #2.

### 5.3 The two reserved-slot constellation pre-decisions are asymmetric

C-h05-successor reserves a slot for one TBD HA. C-hrv-proxy reserves a slot for two TBD HAs already bundled. The asymmetry is justified by stocktake §9.4 D4 framing ("both successor pre-regs to be drafted via standard pre-reg discipline"), but the user accepting "both HA07-proxy and HA08-proxy will cluster together" before either pre-reg exists is a structural pre-decision that the §3.6 RESERVED → PROPOSED lifecycle should re-confirm at PROPOSED-time, not inherit from RESERVED-time. Worth surfacing in §6 lifecycle text. (Recommended action; not required.)

### 5.4 Topic-to-cluster 1:1 default needs an explicit "future revisions may merge / fan" note

Per locked-plan §10.2, the topic-vs-cluster boundary is deferred to drafting of `external_contextualisation.md`. The map's current 1:1 default needs an explicit note that future revisions can merge clusters into a single topic (if external-literature topic-coherence warrants it) or fan a cluster across multiple topics (if the same cluster speaks to two distinct external-literature debates). Currently §4's table reads as definitionally 1:1. (Recommended action; not required.)

### 5.5 Tier aspirations vs §3.10 hard predictive gate

Both active constructs (K-stress-fatigue-monitoring, K-bout-recovery-signal) correctly invoke §3.10 hard predictive gate in their predictive-feasibility cells. K-stress-fatigue-monitoring aspires only to monitoring tier (tier-1, §3.10-PPV-exempt). K-bout-recovery-signal aspires to informative-pattern (tier-2, §3.10-PPV-required). The map records the PPV-with-base-rate requirement explicitly for the bout-recovery cell. But it does not explicitly state that the monitoring tier is the §3.10-PPV-exempt tier; a downstream reader could mis-infer that monitoring is a weakened tier-2 claim. (Recommended action; not required.)

### 5.6 Limitations citation requirement not surfaced in row reasoning

Per `research_line_limitations.md` r3 §5 citation-requirement table, downstream artefacts cluster-*.md, topic-*.md, construct-*.md have explicit L-ID citation obligations (cluster-*.md cites every limitation touching any cluster member; topic-*.md MUST cite L1+L2+L4 unconditionally; construct-*.md MUST cite all seven with explicit applicability-or-NA per limitation). The map currently lists `research_line_limitations.md` in §8 cross-refs only. For a layer-wide pre-registration map of cluster / topic / construct rows, the citation obligation should be surfaced at the *row* level (or at minimum at the table header / preface paragraph), so that S₁ / S₂ / A guides drafted from this map carry the obligation forward. Currently a guide-author reading the map cluster table alone would not know that L-ID citation is a downstream requirement. (Required action #3.)

---

## 6. What the map does not yet address

- **The framework-validity-vs-substantive distinction at the cluster level** (§4.2 above). C-bout-recovery bundles a framework gate with a substantive test; S₁ does not know whether to treat HA11-bout-redo's PARTIAL as a co-finding or as a calibration-discount caveat.
- **The era-scope asymmetry inside C-bout-recovery** (§4.2 above). HA-C4c cross-phase primary vs HA11-bout-redo unmedicated-only primary; the apples-to-apples comparison happens on a sensitivity arm of one HA, not a primary cell of either. S₁ needs to know which cells it is reconciling.
- **The S₁-vs-HA-C3p-result-§6 relationship** (§5.1 above). The 4-cell agreement matrix exists at result layer per HA-C3p Locked decision 5; the map's S₁ on the same cluster doesn't say whether it inherits / supersedes / cites that matrix.
- **The reserved-slot trigger conditions** beyond "drafted via standard pre-reg discipline" are not concrete. What event activates HA-H05-successor? A new spec for the recovery-time measure? A descriptive backstop becoming available? Stocktake §9 D1 says "to be drafted via the project's standard pre-reg discipline when a sound spec is identified"; the map should inherit that framing explicitly into §6 reserved-slot-activation language.
- **Cluster-membership rule when an existing-cluster HA gets re-run with a meaningfully different operationalisation** (e.g., HA-C3 v3 if v2 HALTs). The §6 "New HA lands ready" path describes new-HA landing; it does not describe re-runs of an existing-cluster HA under a different op. By the §3.6 conflict-resolution rule this would trigger a map-revision session, but the §6 text doesn't make that explicit.
- **The lock log honesty bar (§7 below, item 10)**: the user-sign-off entry in §7 lock log does not capture that fresh-session review is *the actual* §3.6-mandated discipline (not just an additional gate). The lock log reads "awaiting fresh-session `/research-methodology-review`" which is correct, but the user-sign-off entry calls itself "[user] accepted all PROPOSED rows as-is" — which suggests acceptance of substance, not acceptance pending peer review. The fresh-session review IS the §3.6-mandated peer-review check; the user-sign-off is the producer-mode draft-acceptance before peer review, not a substitute for it. The lock log should be clearer that the in-session user sign-off was draft-acceptance, NOT lock; lock happens only after fresh-session review absorption.

---

## 7. Required actions (must fix before lock)

1. **C-bout-recovery cluster cell — explicitly route the framework-validity-vs-substantive distinction to S₁ behaviour.** Either split into two clusters (C-bout-framework-validity for HA11-bout-redo; C-bout-recovery-substantive for HA-C4c, with HA11-bout-redo's verdict cited as a precondition not a co-finding) OR keep as one cluster but add explicit text in the operationalisation-overlap-note cell stating that S₁'s coherence call treats HA11-bout-redo's PARTIAL verdict as a calibration-discount caveat propagated forward into HA-C4c's interpretation, NOT as a co-equal verdict for reconciliation. The current cell describes the cascade but does not specify how S₁ should consume it. Without this, the first S₁ session on this cluster will halt-and-route-back-through-§3.6 immediately.

2. **§3 "Coherence read for active clusters" — re-frame or relocate.** The candidate joint readings (especially "inverted-U / threshold-like rather than monotone-convex" for C-stress-fatigue-shape) cross the structure-vs-synthesis line that §3.6 reserves. Either relocate to an `open_inputs`-tagged "S₁ candidate joint readings to evaluate" block, OR strongly fence as "PRIOR JOINT-READING SKETCHES — caveat-class only" with explicit non-propagation language stronger than the current "S₁ session will make the actual call" disclaimer. The §3.6 rule is "the map records structure, not synthesis"; the current §3 paragraph straddles that line.

3. **Surface the `research_line_limitations.md` r3 §5 L-ID citation obligation at the map-table level**, not just §8 cross-refs. Either add a preface paragraph to §3 / §4 / §5 stating that downstream cluster / topic / construct artefacts inherit the L-ID citation requirement per the limitations doc §5 table, OR add a row to each table cell noting the applicable L-IDs (e.g., "L1+L2+L3+L6 apply; L5 NA; L7 applies"). Without this, S₁ / S₂ / A guide drafters reading the map cold will not know the citation obligation exists.

4. **§7 lock-log honesty.** Update the user-sign-off entry's wording from "User accepted all PROPOSED rows as-is" to make explicit that this was *producer-mode draft-acceptance prior to peer review*, NOT lock. The fresh-session-review-before-lock discipline is the §3.6-mandated peer-review check, not an additional optional gate. The current wording could read as if the user sign-off is the substantive lock event and the fresh-session review is a courtesy.

---

## 8. Recommended actions (should consider)

1. C-stress-fatigue-shape cluster cell — clarify the relationship between S₁'s synthesis-layer coherence call and the HA-C3p result.md §6 4-cell agreement matrix. State explicitly: does S₁ inherit / cite the matrix, or does S₁ produce its coherence call independently with the matrix as descriptive context?

2. C-hrv-proxy reserved-slot — flag that the pre-bundling of HA07-proxy + HA08-proxy into one cluster is a forward-looking constellation pre-decision that should be re-confirmed at PROPOSED-time when each successor pre-reg lands, not inherited from RESERVED-time.

3. Topic-to-cluster 1:1 default — add a §4 preface note that future revisions may merge clusters into one topic or fan a cluster across multiple topics, per locked-plan §10.2's deferred question. Current 1:1 reads as structural answer, not defer-to-future-question.

4. K-stress-fatigue-monitoring construct cell — explicitly state that monitoring is the §3.10-PPV-exempt tier-1, not a weakened tier-2. Prevents misreading.

5. §6 reserved-slot lifecycle — make the activation triggers concrete. What event activates HA-H05-successor (a new spec? a descriptive backstop?)? Currently §6 references "via the same pre-reg discipline" which is correct but underspecified.

6. §6 lifecycle — add a path for an existing-cluster HA being re-run with a meaningfully different operationalisation (e.g., HA-C3 v3). The current §6 text describes new-HA-landing and in-stage-S₁-discovery; it does not describe re-spec-re-run.

7. Cluster row literature anchors — even one external citation per active cluster, where one materially supports the cluster-membership reasoning, would strengthen §2.2's "established literature" input. Currently literature lives only at the topic row.

8. C-stress-fatigue-shape operationalisation-overlap-note — clarify that the cross-bin-scheme independence (Wiggers-verbatim vs personal-quintile) is what gives the cluster its evidence-strength as "two independent operationalisations", to preempt the locked-plan §6.3 anti-pattern reading ("three HAs on the same signal are one piece of evidence, not three").

---

## 9. What is fine as-is

- The map's overall architecture (§1 purpose, §2 initial scope, three tables, §6 map growth, §7 lock log, §8 cross-references) is the right shape for a layer-wide pre-registration MD.
- The seeding from stocktake §9 (4 ready HAs + 3 reserved slots; 4 explicit exclusions) is faithful to the stocktake's user decisions.
- The §3.6 layer-rule binding is correctly invoked at §1 + §3 preface + §6 + §8.
- The §3.10 hard-predictive-gate framing is correctly applied to both active constructs' predictive-feasibility cells.
- The exclusion list at §2 ("Excluded from the map per stocktake §9") accurately captures H03b RETIRED + S02b SHELVED-BLOCKED-BY-S02 + H05 RETIRED + HA07/HA08 SUPERSEDED.
- The cross-references in §8 are comprehensive and link the map correctly back to the plan, the limitations doc, the stocktake, the four HA pre-regs, and the parent methodology MDs.
- The §6 map-growth language correctly distinguishes the two new-row paths (new HA lands ready vs in-stage S₁ discovery) and routes the latter through the §3.6 conflict-resolution rule.
- The user-explicit-sign-off requirement on cluster-membership choices (§6 path 1: "The choice requires user explicit sign-off, not the drafting session's judgment") correctly inherits the producer-mode-with-user-interview discipline from CONVENTIONS §1.1.
