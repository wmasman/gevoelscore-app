# Synthesis-structure map

**Status**: **LOCKED r2 by user acceptance 2026-06-23** (Option γ canonical 4-stage closure per the Wave-5.5 pattern: r1 drafted → fresh-session methodology review REVISION RECOMMENDED → r2 substantive absorb of all 4 required + 8 recommended actions → user acceptance per review's explicit "can plausibly LOCK after absorbing the items in §7 below, without a second fresh-session review pass" allowance per the §3.6-compression analogue for non-blocking r1 fires). Authored 2026-06-23 by Claude under user interview, per §11 step 5 of [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md) (r4 LOCKED 2026-06-23). r1 → r2 absorbed a fresh-session `/research-methodology-review` (verdict REVISION RECOMMENDED, report at [`reviews/methodology-synthesis_structure_map-2026-06-23.md`](../reviews/methodology-synthesis_structure_map-2026-06-23.md)) that caught one substantive structural issue (C-bout-recovery collapses framework-vs-substantive distinction) and three discipline gaps (§3 coherence-reads cross structure-vs-synthesis line; L-ID citation obligation only surfaced in cross-refs; §7 lock-log wording risked conflating user sign-off with peer-review). All four required + all eight recommended actions absorbed in r2. See §7 lock log for per-revision diff.

---

## 1. Purpose

This MD pre-registers the **synthesis structure** that `S₁` / `S₂` /
`A` stages of the results-analysis layer operate on. Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.6, the choice of which HAs cluster together, which clusters feed
which topic, and which topics feed which actionability construct must
be **pre-declared as a layer-wide map** before any S₁ / S₂ / A drafting
begins. Reactive per-cluster declaration during stage execution lets
story-shaping cherry-picks back in; this map is the anti-cherry-pick
discipline at the layer-structural level.

The map can grow per §3.6: new HAs land → new rows are **appended**
with explicit lock entries, never silently merged into existing
clusters. Lock log at §5 tracks every addition / removal / re-scoping.

## 2. Initial scope (per stocktake §9 decisions)

Per [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
§9 (D2 + D3): the map seeds with the **4 HAs ready for Stage D
TRUSTED** (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo). The 24
NOT-BACKSTOPPED HAs are deferred per defer-and-grow strategy — they
enter the map as their descriptive backstops land (per the §11 step
11 rollout cluster-by-cluster discipline). Three additional rows are
**reserved** for successors per stocktake §9 (D1 + D4): HA-H05-successor,
HA07-proxy, HA08-proxy.

**Excluded from the map** per stocktake §9:
- **H03b** — RETIRED (data-resolution limit).
- **S02b** — SHELVED-BLOCKED-BY-S02 (depends on unverified S02
  algorithmic-lag outputs; never ran).
- **H05** — RETIRED (spec-induced trivial distribution).
- **HA07 + HA08 originals** — SUPERSEDED (hardware-blocked; HRV
  absent on FR245; HA07-proxy / HA08-proxy successors take over).

## 3. Cluster table (S₁ pre-registration)

A cluster groups HAs that test overlapping constructs at the same
resolution. `S₁` synthesises a cluster's verdicts into a coherence
call. Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.6 conflict rule, if per-cluster S₁ work reveals the map needs
changing, the skill halts; revision happens in a separate map-revision
session with its own methodology-review.

| Cluster ID | Cluster name | Constituent HAs | Shared construct | Operationalisation overlap note | L-IDs S₁ will need to cite | Literature anchor | Status | Declared |
|---|---|---|---|---|---|---|---|---|
| C-stress-fatigue-shape | Stress-fatigue dose-response shape (daily-aggregate) | HA-C3 v2, HA-C3p | Non-linear stress→fatigue mapping per Wiggers convex-cost claim | **Two independent operationalisations of the same construct.** Both use `all_day_stress_avg × gevoelscore`; HA-C3 v2 uses Wiggers-verbatim 4-bin absolute anchor (30→40), HA-C3p uses personal-baseline quintile bins. The cross-bin-scheme independence (absolute-numerical vs personal-relative binning) is what gives this cluster its evidence-strength as "two independent operationalisations" rather than two-views-on-the-same-cut — preempts the locked-plan §6.3 anti-pattern ("three HAs on the same signal are one piece of evidence, not three"). Sister HAs by explicit pre-reg framing (HA-C3p §1). HA-C3p result.md §6 contains a 4-cell agreement matrix (v2 REJECTED × p PARTIAL = "Wiggers' numbers wrong-for-this-participant but underlying shape IS REAL in the INVERSE direction"); per HA-C3p's own §6 framing this matrix is **caveat-class post-hoc and NOT a substantive output**, so S₁ cites the matrix as descriptive context only and produces its coherence call independently of it. | L1, L2, L3, L4, L6, L7 (L5 NA — no v24 primary signals) | [Wiggers pacing handleiding](../literature/wiggers_pacing_handleiding.pdf) lines 1357-1368 ("Annual Stress Scores" — convex-cost claim) | ACCEPTED | 2026-06-23 |
| C-bout-framework | Bout-level framework-validity | HA11-bout-redo | Whether the bout-extraction operand re-detects HA11 v1's discrimination signal at bout resolution | **NOT a substantive Wiggers claim.** Per HA11-bout-redo §1, this is a methodology-validation check (framework-validity discipline per parent MD §6). Validates that `bout_n_fast_recovery_day` reproduces HA11 v1's +22.8 pp discrimination at bout resolution. S₁ on this cluster reads the verdict as **operand fitness-for-purpose**, NOT as a substantive finding about within-day recovery in PAIS. **Cascade arrow**: this cluster's verdict propagates as a **caveat-class precondition** to C-bout-substance (downstream); it is not a co-equal verdict that S₁ reconciles against C-bout-substance's findings. | L1, L2, L3, L4, L6, L7 (L5 NA) | HA11 v1 [result.md](../analyses/hypotheses/H05/result.md) (+22.8 pp discrimination reference; project-internal anchor since this is a methodology-validation cluster) | ACCEPTED | 2026-06-23 |
| C-bout-substance | Bout-level recovery substance (heavy-T failure-to-return) | HA-C4c | Within-day stress recovery / failure-to-return at bout resolution on heavy-T days | Substantive Wiggers C4 retest at bout resolution. Uses `bout_n_did_not_return_day` per-day count vs `exertion_class_lagged_lcera` heavy-T classifier. **Cross-phase pooled** on citalopram_phase axis (unmedicated + buildup + consolidation + afbouw + post_afbouw), §4.10 unmedicated-only sensitivity arm. S₁ on this cluster MUST consume the C-bout-framework verdict as caveat-class precondition (per cascade arrow above) before reading the C-bout-substance verdict on its own merits. **Era-scope mismatch** with C-bout-framework: C-bout-framework runs unmedicated×train; C-bout-substance runs cross-phase pooled — the asymmetry is structural to each cluster's question, not a confound to reconcile away. | L1, L2, L3, L4, L7 (L5 NA — no v24; L6 NA — gevoelscore not in primary cell) | [Wiggers pacing handleiding](../literature/wiggers_pacing_handleiding.pdf) lines 1140-1141, 1223-1231 ("Walls of Stress", "Stuck in Stress"); adrenaline-lingers mechanism lines 1316-1324 | ACCEPTED | 2026-06-23 |
| C-h05-successor | (Reserved slot) | HA-H05-successor (TBD) | Recovery-time after exertion (Wiggers H05 successor) | Reserved per stocktake §9.1 D1 (H05 RETIRED, successor slot reserved). Successor pre-reg to be drafted via standard pre-reg discipline when spec is sound. **Activation trigger**: a producer-mode pre-reg-drafting session that produces an HA-H05-successor pre-reg with sound spec (per `hypothesis_lock_process.md`); on lock, this row's status moves RESERVED → PROPOSED, then user sign-off → ACCEPTED, then fresh-session methodology-review → LOCKED. | TBD (set at PROPOSED-time) | TBD (set at PROPOSED-time) | RESERVED | 2026-06-23 |
| C-hrv-proxy | (Reserved slot) | HA07-proxy, HA08-proxy (both TBD) | HRV via stress-proxy operationalisation | Reserved per stocktake §9.4 D4 (HA07/HA08 originals SUPERSEDED; proxy successors take over via [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md)). Both successor pre-regs to be drafted via standard pre-reg discipline. **Activation trigger**: producer-mode pre-reg-drafting session(s) that produce HA07-proxy and HA08-proxy pre-regs; on each lock, the row's status moves RESERVED → PROPOSED. **Bundling re-confirmation required**: the pre-bundling of HA07-proxy + HA08-proxy into a single cluster is a forward-looking constellation pre-decision (RESERVED-time); it must be re-confirmed at PROPOSED-time when each successor pre-reg actually lands, since the bundling assumes operationalisation overlap that the pre-regs may or may not deliver. | TBD (set at PROPOSED-time) | [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) + future HRV-in-LC literature (TBD at PROPOSED-time) | RESERVED | 2026-06-23 |

**Note on synthesis-seed notes.** During r1 drafting the map carried
"candidate joint reading" sketches for the two active clusters. Per
the fresh-session methodology-review's R2 finding — the §3.6
structure-vs-synthesis line forbids the map pre-deciding S₁'s
coherence calls — those sketches have been **relocated** to a separate
non-binding artefact: [`_synthesis_seed_notes_2026-06-23.md`](_synthesis_seed_notes_2026-06-23.md).
That file is **advisory only**, not part of the map's structural
pre-registration. S₁ sessions may choose to use those notes as
caveat-class context or to ignore them; either choice is correct.
The map itself records structure, not synthesis.

## 4. Topic table (S₂ pre-registration)

A topic is a construct-level frame for external-literature
contextualisation. `S₂` places the topic's cluster(s) against
published consensus. Topics may fan out from a single cluster or
combine multiple clusters per the user's clustering judgment.

**Topic-to-cluster boundary default**: 1:1 in this initial map, but
per locked-plan §10.2 deferred-question the topic-vs-cluster boundary
is intentionally not pre-decided as a structural rule. Future map
revisions may **merge** clusters into one topic (if external-literature
topic-coherence warrants it) or **fan** a cluster across multiple
topics (if the same cluster speaks to two distinct external-literature
debates). The current 1:1 reflects the small initial scope; do not
read it as a structural answer.

**L-IDs S₂ will need to cite** (per [`research_line_limitations.md`](research_line_limitations.md)
§5): every topic MUST cite L1 + L2 + L4 unconditionally; cite L3, L5,
L6, L7 as they apply per cluster member. Per-topic L-IDs in the table.

| Topic ID | Topic name | Constituent clusters | Construct | External literature topic for S₂ | L-IDs S₂ must cite | Status | Declared |
|---|---|---|---|---|---|---|---|
| T-stress-fatigue-pacing | Stress-fatigue dose-response in PEM-prone populations | C-stress-fatigue-shape | Stress-fatigue dose-response shape | Wiggers pacing handleiding (primary, in [`literature/wiggers_pacing_handleiding.pdf`](../literature/wiggers_pacing_handleiding.pdf)); broader PEM-pacing literature (Appelman 2024 muscle PEM, push-crash research notes); ME/CFS pacing handbooks; energy-envelope literature. | L1, L2, L4 (mandatory) + L3, L6, L7 (apply per C-stress-fatigue-shape signals) | ACCEPTED | 2026-06-23 |
| T-within-day-recovery | Within-day autonomic recovery in PEM-prone populations | C-bout-substance (primary); C-bout-framework as upstream calibration precondition | Bout-level autonomic recovery and failure-to-return | Marques 2023 LC cardiovascular autonomic dysfunction; Mooren 2023 postcovid HRV; Ryabkova 2024 ME/CFS dysautonomia; van Campen 2022 ME/CFS RHR elevated; broader within-day-recovery literature. | L1, L2, L4 (mandatory) + L3, L7 (apply per C-bout-substance signals; L6 NA — no gevoelscore in primary cell) | ACCEPTED | 2026-06-23 |
| T-recovery-time | (Reserved slot) | C-h05-successor | Recovery-time after exertion | Pending H05-successor pre-reg; literature scope TBD at successor lock. | TBD (L1+L2+L4 mandatory; others at PROPOSED-time) | RESERVED | 2026-06-23 |
| T-hrv-in-lc | (Reserved slot) | C-hrv-proxy | HRV-proxy operationalisation in LC | Suh 2023 LC HRV systematic review; Mooren 2023 HRV autonomic dysregulation; Berntson 1997 HRV methods caveats; Shaffer 2017 HRV metrics; pending HA07/HA08 proxy pre-regs. | TBD (L1+L2+L4 mandatory; L3 likely applies for proxy-via-stress; others at PROPOSED-time) | RESERVED | 2026-06-23 |

## 5. Construct table (A pre-registration)

An actionability construct is a daily-life signal that downstream
artefacts may translate (or refuse to translate) into monitoring /
informative-pattern / predictive-use claims per the locked plan §6.5
+ §3.10 hard predictive gate. Tier aspirations below are the **most
the construct could reach if all required evidence lands**; actual
tier at Stage A time depends on §3.10 quality-measures and §6.5
forward-validation discipline.

**L-IDs A will need to cite** (per [`research_line_limitations.md`](research_line_limitations.md)
§5): every construct MUST cite **all seven L-IDs with explicit
applicability-or-NA per limitation**. Actionability is the
downstream-most claim and inherits all systemic context. Per-construct
L-ID notes in the table below indicate which apply substantively vs
NA.

| Construct ID | Construct name | Topics feeding | Tier aspiration | Predictive-claim feasibility (current state) | L-ID notes (all seven cited; NA per limitation) | Status | Declared |
|---|---|---|---|---|---|---|---|
| K-stress-fatigue-monitoring | Stress-fatigue daily monitoring signal | T-stress-fatigue-pacing | **Monitoring (tier-1, §3.10-PPV-exempt)** — descriptive shape only; not a weakened tier-2 claim. Informative-pattern (tier-2) blocked by single-cluster evidence + direction-anomaly with Wiggers' canonical claim. | Predictive-use tier **blocked** at this stage: no forward-validation HA exists; HA-C3 v2 REJECTED + HA-C3p PARTIAL together cap claims at descriptive monitoring (tier-1). A forward-validation HA testing "tomorrow's gevoelscore predictable from today's stress bin" would be needed for tier 2+. Per locked-plan §3.10, tier-1 monitoring claims do not require PPV-with-base-rate. | L1 applies, L2 applies (unmed only), L3 applies (Garmin signal), L4 applies (Wiggers prior), L5 NA (no v24 primary), L6 applies (gevoelscore), L7 applies (gating dropouts) | ACCEPTED | 2026-06-23 |
| K-bout-recovery-signal | Bout-level recovery signal (within-day) | T-within-day-recovery | **Informative-pattern (tier-2, §3.10-PPV-required)** — effect-size demonstrated but small. Predictive-use (tier-3) blocked by §3.10 hard predictive gate. | Predictive-use tier **blocked**: effect sizes (Cliff's δ = +0.120; +20.26 pp discrimination) are modest; bar-failures on both HAs (HA11-bout-redo p-value, HA-C4c effect-size) leave open whether the operand is at corpus detection limits. **Tier-2 requires PPV-with-base-rate per §3.10** — to be computed against crash base rate (~2/year residual per RESEARCH-REPORT §5.2 precedent) at Stage A time. | L1 applies, L2 applies (cross-phase pooled per HA-C4c), L3 applies (bout-derived Garmin), L4 applies (Wiggers prior), L5 NA (no v24), L6 NA (gevoelscore not in primary cell), L7 applies (gating + cross-phase coverage) | ACCEPTED | 2026-06-23 |
| K-recovery-time | (Reserved slot) | T-recovery-time | TBD | Pending H05-successor verdict. | TBD (all seven evaluated at PROPOSED-time per §5 limitations doc binding) | RESERVED | 2026-06-23 |
| K-hrv-proxy | (Reserved slot) | T-hrv-in-lc | TBD | Pending HA07-proxy + HA08-proxy verdicts. | TBD (all seven evaluated at PROPOSED-time) | RESERVED | 2026-06-23 |

## 6. Map growth and revision

Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.6, the map grows by **appending** rows with explicit lock entries.
The three paths:

1. **New HA lands ready** (its descriptive_audit.md is TRUSTED) →
   either joins an existing cluster (if it shares construct +
   operationalisation overlap with the cluster's members per the
   declared "shared construct" cell) or seeds a new cluster (if the
   construct is genuinely new). The choice requires user explicit
   sign-off, not the drafting session's judgment.
2. **In-stage discovery during S₁ work** that the map needs changing
   (an HA belongs in a different cluster; a cluster should be split;
   a topic boundary is wrong) → per §3.6 conflict-resolution rule:
   halt S₁ immediately; log the proposed change to `open_inputs`;
   resume only after a separate producer-mode map-revision session
   updates the map with its own methodology-review pass before re-lock.
3. **Existing-cluster HA re-run with meaningfully different
   operationalisation** (e.g., HA-C3 v3 hypothetically replacing v2
   with a new bin scheme, or HA-C4c v2 with a different heavy-T
   classifier) → the new-version HA inherits the cluster membership
   of its predecessor by default. If the new operationalisation
   meaningfully changes the cluster's shared-construct framing or
   operationalisation-overlap-note cell, the change requires a
   separate producer-mode map-revision session (the §3.7 drift
   policy of the limitations doc is the model). If the
   re-operationalisation is minor (sensitivity-arm-level), the
   cluster cell may be updated in-place with a §7 lock-log entry.
   When in doubt, route through path 2.

**Reserved slot activation** — concrete triggers per slot:

- **C-h05-successor activation**: a producer-mode pre-reg-drafting
  session that produces an `HA-H05-successor/hypothesis.md` with a
  sound spec (per `hypothesis_lock_process.md`) and the user accepts
  the HA. On HA-H05-successor lock, this cluster row's status moves
  RESERVED → PROPOSED; user sign-off → ACCEPTED; fresh-session
  `/research-methodology-review` → LOCKED. The reserved row's
  `Constituent HAs` cell updates from "TBD" to "HA-H05-successor"
  at PROPOSED-time.
- **C-hrv-proxy activation**: producer-mode pre-reg-drafting
  session(s) that produce `HA07-proxy/hypothesis.md` and
  `HA08-proxy/hypothesis.md`. **Bundling re-confirmation required at
  PROPOSED-time** per the §3 cluster-table note: the RESERVED-time
  pre-bundling assumes operationalisation overlap which the actual
  pre-regs may not deliver. If the two successor pre-regs land with
  meaningfully different operationalisations, this row splits into
  two single-HA clusters at PROPOSED-time rather than landing as one.

**General activation discipline**: a reserved row's PROPOSED → LOCKED
sequence is identical to a new-cluster lock (user sign-off → fresh-
session methodology-review → lock), but the RESERVED → PROPOSED
transition is the one that requires structural re-confirmation
(membership, construct framing, operationalisation overlap) — the
prior RESERVED-time pre-decisions are not binding at PROPOSED-time.

## 7. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-23 | Drafted r1 | Producer-mode under user interview. Initial rows seeded as PROPOSED from the four ready HAs per stocktake §9.2 D2 + D3; reserved slots seeded from §9.1 D1 + §9.4 D4. |
| 2026-06-23 | User producer-mode draft-acceptance (not lock) | User accepted all 8 PROPOSED rows as-is per the producer-mode-with-user-interview discipline (CONVENTIONS §1.1). Status of accepted rows transitioned to ACCEPTED. **This is NOT the §3.6 lock event** — the §3.6-mandated discipline is `fresh-session /research-methodology-review` before lock. User draft-acceptance is the producer-mode user-in-the-loop check on row content; fresh-session review is the methodology-MD peer-review check on the doc as a whole. The two are different gates serving different purposes. |
| 2026-06-23 | Fresh-session `/research-methodology-review` | Verdict REVISION RECOMMENDED. Report: [`reviews/methodology-synthesis_structure_map-2026-06-23.md`](../reviews/methodology-synthesis_structure_map-2026-06-23.md). Caught one substantive structural issue (R1: C-bout-recovery collapses framework-validity-vs-substantive distinction; will halt first S₁ session if unfixed) and three discipline gaps (R2: §3 coherence-reads cross structure-vs-synthesis line; R3: L-ID citation obligation only in §8 cross-refs; R4: §7 lock-log wording risks conflating user sign-off with peer-review). Plus eight recommended actions across cluster-cell tightening, topic-vs-cluster boundary, construct-tier framing, reserved-slot lifecycle, and literature anchoring at the cluster level. |
| 2026-06-23 | Revised r1 → r2 | Absorbed all four required + all eight recommended actions. R1: split C-bout-recovery into **C-bout-framework** (HA11-bout-redo; framework-validity) + **C-bout-substance** (HA-C4c; substantive) with explicit cascade-arrow language (framework verdict propagates as caveat-class precondition to substance, not co-equal verdict). R2: relocated §3 coherence-read sketches to non-binding [`_synthesis_seed_notes_2026-06-23.md`](_synthesis_seed_notes_2026-06-23.md); §3 now references the seed-notes file as advisory only. R3: added L-IDs column to all three tables surfacing per-row citation obligation per `research_line_limitations.md` §5; added L-IDs preface paragraph to §4 and §5. R4: tightened this lock log (this entry + the prior user-sign-off entry) to make producer-mode draft-acceptance vs §3.6-mandated peer-review-before-lock distinct events. Plus recommended actions: A1 C-stress-fatigue-shape cell now clarifies HA-C3p §6 4-cell matrix as caveat-class context for S₁ (not co-equal verdict); A2 C-hrv-proxy bundling re-confirmation requirement surfaced; A3 §4 preface on 1:1 topic-cluster default as initial-scope reflection not structural answer; A4 K-stress-fatigue-monitoring tier-1 PPV-exempt explicitly named; A5 §6 reserved-slot activation triggers made concrete per slot; A6 §6 added re-spec-re-run path 3; A7 cluster row literature anchors added (column); A8 C-stress-fatigue-shape cell now invokes the cross-bin-scheme independence as evidence-strength rationale per §6.3 anti-pattern preempt. NOT LOCKED — awaiting user acceptance. |
| 2026-06-23 | **LOCKED r2** | **User acceptance** ("Accept synthesis_structure_map r2 LOCK"). Status of all 5 ACCEPTED + RESERVED rows transitioned to **LOCKED**; reserved slots stay RESERVED at activation status but their RESERVATION is LOCKED. Implementation proceeds to §11 step 6.1 (descriptive_precondition_audit.md guide drafting) + housekeeping per stocktake §9.5 (registry RETIRED / SHELVED / SUPERSEDED marks; reserved-slot pre-reg drafting). **Option γ canonical 4-stage closure** (substantive absorb + LOCK without second review per fresh-session review §1 explicit permission "can plausibly LOCK after absorbing the items in §7 below, without a second fresh-session review pass per the user's existing Option-γ §3.6-compression pattern on the §3 changes that would be substantive vs the §4 changes that are mechanical wording") — same Option-γ pattern established at HA-C4c r2 LOCK Wave 5.5 commit `4e666a2`. |

**r2 LOCKED 2026-06-23**: see entry above for the LOCK closure.

## 8. Cross-references

- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  §3.6 (the layer rule that binds this MD); §3.6 conflict-resolution
  rule (map vs §6.3 per-cluster pre-declaration); §11 step 5 (the
  implementation step that produced it).
- [`research_line_limitations.md`](research_line_limitations.md)
  (the systemic limitations every claim built on this map must cite).
- [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
  §4 (the 4 HAs ready for Stage D TRUSTED that seed this map);
  §9 (the user decisions on stocktake findings that produced the
  reserved-slot list).
- [`_synthesis_seed_notes_2026-06-23.md`](_synthesis_seed_notes_2026-06-23.md)
  (non-binding advisory notes containing the r1-drafted candidate
  joint-reading sketches relocated per the r2 R2 absorption; S₁
  sessions may use them as caveat-class context or ignore them).
- HA pre-regs of the four ready HAs:
  - [`HA-C3/hypothesis.md`](../analyses/hypotheses/HA-C3/hypothesis.md)
    (v2 LOCKED 2026-06-23).
  - [`HA-C3p/hypothesis.md`](../analyses/hypotheses/HA-C3p/hypothesis.md)
    (r1 LOCKED 2026-06-23).
  - [`HA-C4c/hypothesis.md`](../analyses/hypotheses/HA-C4c/hypothesis.md)
    (r1 LOCKED 2026-06-23).
  - [`HA11-bout-redo/hypothesis.md`](../analyses/hypotheses/HA11-bout-redo/hypothesis.md)
    (LOCKED 2026-06-22).
- Parent methodology MDs feeding the clusters:
  - [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md)
    (C-bout-recovery parent).
  - [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)
    (cross-phase pooling discipline for HA-C4c).
  - [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md)
    (reserved C-hrv-proxy cluster's operationalisation basis).
- [`RESEARCH-REPORT.md`](../RESEARCH-REPORT.md) §5.2 (PPV-with-base-
  rate precedent referenced in §5 K-bout-recovery-signal predictive-
  feasibility row).
