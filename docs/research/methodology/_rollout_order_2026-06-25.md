# Rollout order — locked 2026-06-25

**Status**: LOCKED 2026-06-25 by user acceptance, per §11 step 10 of
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
(r5 LOCKED). Producer-mode planning artefact (underscore-prefix
convention matching `_synthesis_seed_notes_2026-06-23.md`,
`_descriptive_stocktake_2026-06-23.md`).

This artefact records the locked rollout order across the corpus per
§11 step 10b ("lock the rollout order with one-line rationale per
cluster"). Deviations from the locked order require explicit user
decision in-session per §11 step 10c (not drift).

---

## 1. Locked criteria (per §11 step 10a)

- **Primary criterion**: **by-cluster** (synthesis-coherence first).
  Finish each cluster fully through D → I → S₁ → S₂ → A → T before
  starting the next.
- **Tiebreaker**: **tractability** (single-member clusters before
  multi-member; no-cascade before cascade-source; cascade-source
  before cascade-receiver).
- **Deviation rule**: any deviation from the locked order below
  requires explicit user decision in-session per §11 step 10c. Not
  drift.

## 2. Locked rollout order (initial phases)

### Phase A — C-stress-fatigue-shape promotion to LOCKED

**Rationale**: dry-run already produced 7 + 4 = 11 DRAFT-r1 artefacts
across D → A → T for this cluster (steps 8 + 9). Promoting these to
LOCKED via user-interview on the DEFAULTED slots is the fastest path
to first real LOCKED outputs across the full layer.

**Sub-phases**:
- **A.1**: HA-C3 v2 interpretation.md §4.6 lived-experience prior
  (DEFAULTED-PENDING-USER-INPUT → user-articulated)
- **A.2**: HA-C3p interpretation.md §4.6 lived-experience prior
  (DEFAULTED-PENDING-USER-INPUT → user-articulated)
- **A.3**: cluster-stress-fatigue-shape.md §4.4 coherence-call
  (DEFAULTED-TO-PRESERVE PARTIALLY CONCORDANT → user-confirmed or
  re-cast to CONCORDANT)
- **A.4**: construct-stress-fatigue-monitoring.md §5.9 subject-
  narrative commentary (SKIPPED-AS-DRY-RUN-DEFAULT → user-authored
  OR SKIPPED-WITH-USER-RATIONALE)
- **A.5**: Stage S₂ PROXY-CITED-IN-DRY-RUN entries → full PDF reads
  for production-lock OR user-accepts proxies as production-grade
- **A.6**: Translation patient-audience layperson-test pool
  identification per locked-plan §10.7 deferred resolution OR
  user-accepts Layperson-test-pending as production-state
- **A.7**: Lock all 11 artefacts (or subset accepted) as production
  outputs

### Phase B — C-bout-framework (HA11-bout-redo)

**Rationale**: single-member cluster (tractability tiebreaker);
framework-validity gate that becomes cascade-source for Phase C.
Must precede C-bout-substance per cascade-arrow dependency.

**Sub-phases**: D → I → S₁ on HA11-bout-redo. No S₂ / A / T per
map r3 §3 (C-bout-framework is methodology-validation-only; not a
substantive Wiggers claim).

### Phase C — C-bout-substance (HA-C4c)

**Rationale**: single-member cluster (tractability tiebreaker);
cascade-receiver consuming C-bout-framework's S₁ output per cascade-
arrow language in map r3 §3.

**Sub-phases**: D → I → S₁ (with cascade-arrow precondition from
Phase B) → S₂ on T-within-day-recovery → A on K-bout-recovery-signal
(tier-2; PPV-with-base-rate per §3.10) → T (research + patient).

### Phase D — Reserved cluster activations (conditional)

**Rationale**: phases activate as reserved-slot pre-regs land per
map r3 §3.

- **D.1**: C-h05-successor — activates when HA-H05-successor pre-reg
  is drafted + locked per `hypothesis_lock_process.md` discipline.
- **D.2**: C-hrv-proxy — activates when HA07-proxy + HA08-proxy
  pre-regs are drafted + locked. Per map r3 §3 cluster cell, bundling
  re-confirmation required at PROPOSED-time (the RESERVED-time
  pre-bundling may not survive per-pre-reg lock).

### Phase E — Defer-and-grow (ongoing)

**Rationale**: 24 NOT-BACKSTOPPED HAs per stocktake §9.2 D2 enter
the rollout queue as their Strand-A descriptive backstops land per
defer-and-grow strategy. Each newly-backstopped HA joins the by-
cluster sequence at the cluster it belongs to (per map r3 §3).
Stocktake §3 enumerated the Strand-A extension across 8 deferred
channels; backstops land per producer-mode descriptive sessions
external to this layer's rollout.

## 3. Order summary table

| Order | Phase | Cluster | Members | Cascade | Notes |
|---|---|---|---|---|---|
| 1 | A | C-stress-fatigue-shape | HA-C3 v2, HA-C3p | none | dry-run promotion to LOCKED |
| 2 | B | C-bout-framework | HA11-bout-redo | source | single-member; D + I + S₁ only |
| 3 | C | C-bout-substance | HA-C4c | receiver | single-member; full D → T chain |
| 4 | D.1 | C-h05-successor (reserved) | TBD | TBD | conditional on successor pre-reg lock |
| 5 | D.2 | C-hrv-proxy (reserved) | TBD | TBD | conditional + bundling re-confirm |
| 6+ | E | 24 NOT-BACKSTOPPED HAs | various | per-cluster | enter queue as backstops land |

## 4. Cross-references

- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  §11 step 10 (the binding source for this artefact) + §11 step 11
  (the rollout itself, governed by this artefact's order).
- [`synthesis_structure_map.md`](synthesis_structure_map.md) §3
  cluster table + §4 topic table + §5 construct table (the map this
  rollout operates against).
- [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
  §9 user decisions (D2: defer-and-grow strategy informing Phase E).
- [`research_line_limitations.md`](research_line_limitations.md) — the
  L-IDs every Phase A-D artefact will cite.
- [`.claude/skills/research-interpret/SKILL.md`](../../.claude/skills/research-interpret/SKILL.md)
  — the engine driving each phase.

## 5. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-25 | Locked rollout order | Per §11 step 10 user-interview. Primary criterion: by-cluster. Tiebreaker: tractability. Deviation rule: explicit user decision required. Phase A starts immediately. |
