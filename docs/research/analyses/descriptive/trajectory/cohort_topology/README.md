# Q4.4 cohort_topology -- 29 crashes + 79 dips + dip-cluster overlay + recovery-window distributions + matched-control baseline

**Strand**: B (multi-year trajectory; descriptive).

**Status**: LANDED 2026-06-25 in worktree-isolated dispatch. Pre-requisite substrate for HA-P6 follow-ups per [`analyses/descriptive/README.md`](../../README.md) section 4.4.

**Authorising user**: Willem; producer-mode under user authorisation per [CONVENTIONS section 1.1](../../../../CONVENTIONS.md#11-producer-mode-claude-acts-directly-with-explicit-user-authorisation).

---

## What this artefact does

Refreshes the project's cohort-topology map: 29 crashes + 79 dips per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) (LOCKED), plus the 30d-rolling dip-cluster overlay that was archived in the old STOCKTAKE, plus recovery-window distributions per-event-class, plus matched-control baseline reusing HA-P6 v3 Arm-A logic.

**4 user-LOCKED operationalisation choices** (per Strand B section 7c interview 2026-06-25; do NOT iterate):

1. **Event scope = (b) crashes + dips (29 + 79 = 108 events)**; sub-threshold dips EXCLUDED per user.
2. **Dip-cluster overlay = (a)+(c)**: 30d rolling dip count + per-recovery-phase dip rate (skip DBSCAN).
3. **Recovery-window distributions = (c) both per-crash + per-dip + comparison** -- per-crash REUSES HA-P6 v3 Arm-A (REPRODUCTION); per-dip is NOVEL.
4. **"Normal" baseline = (b)+(c) matched-control (HA-P6 v3 Arm-A REUSE) + per-recovery-phase reference**.

---

## Method (7 stages)

- **Stage 1 (data prep)**: load `per_day_master.csv` (n=1755) + `labels_crash_v2.csv` (n=108 events); identify recovery_phase per event.
- **Stage 2 (event-by-event)**: per event start / end / duration / lowest-score / recovery-time (both rolling-30d-median + above-threshold ops per [`crash_episode_descriptive section 3`](../../../../methodology/crash_episode_descriptive.md)).
- **Stage 3 (dip-cluster overlay)**: 30d rolling event-count + per-recovery-phase rate + rp5/cp3 boundary-rate cross-references.
- **Stage 4 (recovery-window)**: per-channel z-trajectory in [t+1, t+5] post-event window using HA-P6 v3 section 4.5 Arm-B lagged personal baseline; per-crash REPRODUCES HA-P6 v3 at cohort-topology aggregation; per-dip is NOVEL.
- **Stage 5 (baseline)**: HA-P6 v3 section 4.4 Arm-A matched-control logic REUSED for both crashes + dips; per-recovery-phase non-event normal reference per channel.
- **Stage 6 (artefacts)**: 3 plots (dip-cluster overlay timeline + crash-vs-dip recovery comparison + per-recovery-phase event rates).
- **Stage 7 (programmatic emit)**: this README + findings.md.

---

## Outputs

- [`findings.md`](findings.md) -- the Q4.4 answer + 3+ output artefacts (programmatic emit).
- [`run.py`](run.py) -- the script.
- `summary.json` (gitignored) -- complete per-event + per-cell numbers.
- `plots/` (gitignored) -- 3 PNGs.

---

## Cross-references

**Locked substrate (NOT modified, NOT extended)**:

- [`HA-P6/hypothesis.md`](../../../hypotheses/HA-P6/hypothesis.md) section 4.4 + section 4.5 (Arm-A + Arm-B machinery REUSED).
- [`crash_v2-definition/definition.md`](../../../hypotheses/crash_v2-definition/definition.md) (29 + 79 canonical labels).
- [`crash_episode_descriptive.md`](../../../../methodology/crash_episode_descriptive.md) + [`crash_episode_prolonged.md`](../../../../methodology/crash_episode_prolonged.md) (definitional sources).
- [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) (6-phase axis).

**Strand B descriptive complements**:

- [`trajectory/subjective_objective_coupling/`](../subjective_objective_coupling/) Q4.9 -- pre-crash body-state profile (REPRODUCED + EXTENDED).
- [`trajectory/era_boundaries/`](../era_boundaries/) Q4.3 -- rp5 + cp3 boundary cross-references.
- [`trajectory/detrended_correlation/`](../detrended_correlation/) Q4.5.b -- matched-control trajectory-confound framing.
- [`trajectory/recovery_arc/`](../recovery_arc/) Q4.1 v2 -- multi-year trajectory backdrop.

---

## Discipline

- Layer 1 descriptive per CONVENTIONS section 2.1 + section 4.1 + section 4.2.
- NO causal claims; NO substantive HA verdict promotion.
- crash-topology map per cell with named counts per CONVENTIONS section 3.6.
- Tight-n caveats per CONVENTIONS section 3.1 (especially per-recovery-phase event rates).
- Honest framings: per-dip is NOVEL; per-crash REPRODUCES HA-P6 v3 (section 3 + section 5 of [`findings.md`](findings.md)).
