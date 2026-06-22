# HA11-bout-redo — folder status

**Pre-registration (current)**: [`hypothesis.md`](hypothesis.md) — **drafted 2026-06-22 by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs)**. Status: drafted, not locked.

**What this pre-reg is**: the bout-level cascade's **framework-validity gate** per [`methodology/bout_level_recovery_dynamics.md` §6](../../../methodology/bout_level_recovery_dynamics.md#6-framework-validity-discipline-the-mds-own-falsifier) (LOCKED `c57ff3f` 2026-06-21). It is a methodology-validation test: can the bout-level operand `bout_n_fast_recovery_day` reproduce HA11 v1's SUPPORTED-on-train signal (`u_dip_count` z-score, +22.8 pp discrimination on train) at the parent MD's §6.2 comparability bars, restricted to unmedicated × train era × HA11 v1's null-pool reference dates? Verdict bands: PASSED (all 3 bars) → HA-C4c drafting unblocks; PARTIAL (2 of 3) → HA-C4c drafting unblocks with calibration caveat; FAILED (≤1 of 3) → bout-level cascade HALTS + parent MD reverts to "available but not load-bearing".

**Headline cell (drafted, not locked)**: unmedicated phase × train era × calm-day pool (HA11 v1 reference dates, seed `20260605`, restricted to 2022-09-03 → 2023-12-31) × `bout_n_fast_recovery_day` × {directional + effect-size pp + p-value} comparability bars vs HA11 v1's `u_dip_count` train signal.

## Lock arc

Per [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md) 5-stage canonical arc:

| stage | status | venue | output |
|---|---|---|---|
| 1. Draft (§3.2) | DONE 2026-06-22 | producer-mode under authorisation; this folder | THIS COMMIT |
| 2. Audit (§3.4) | pending | fresh session (paste `/research-review docs/research/analyses/hypotheses/HA11-bout-redo/hypothesis.md`) | `docs/research/reviews/HA11-bout-redo-<date>.md` |
| 3. Revise r2 (§3.5) | pending | shared-context with drafting | r2 of `hypothesis.md` |
| 4. Re-audit (§3.6) | pending or compressible | fresh session OR documented compression | `docs/research/reviews/HA11-bout-redo-<date>-v2.md` OR compression note |
| 5. Lock (§3.8) | pending | shared-context | lock-commit + Authorship `Status: LOCKED` |
| 6. Test execution (§3.9) | pending post-lock | shared-context (test handoff brief) | `test.py` + `result.md` |

## Sister-test context

- **[HA11-stress-udip](../HA11-stress-udip/)** — the v1 sister whose SUPPORTED-on-train signal (+22.8 pp, median signed z = 2.168) is the reproduction target. HA11-bout-redo does NOT supersede HA11 v1; both operationalisations coexist (per HA11 v1's `## Future work — bout-level reproduction` section added 2026-06-19).
- **[HA-C4 v2](../HA-C4/)** — the daily-aggregate Wiggers C4 test whose REJECTED verdict (2026-06-18) drove the bout-level pivot per [`research-pm-brief-bout-level-recovery-pivot-2026-06-19.md`](../../../../../.claude/plans/research-pm-brief-bout-level-recovery-pivot-2026-06-19.md).
- **HA-C4c** — the substantive bout-level Wiggers C4 retest. Not yet drafted; drafting is gated on this pre-reg's PASSED verdict per §9.

## Cross-references

- Parent methodology MD: [`bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md) (LOCKED `c57ff3f` 2026-06-21).
- Pipeline that produces `bout_n_fast_recovery_day`: [`pipeline/02_features/extract_stress_bouts.py`](../../../pipeline/02_features/extract_stress_bouts.py) + [`pipeline/02_features/README.md`](../../../pipeline/02_features/README.md) (LOCKED `d5b394c` 2026-06-22).
- HA11 v1 result.md (reproduction target): [`HA11-stress-udip/result.md`](../HA11-stress-udip/result.md).
- Hypothesis lock process: [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md).
- Drafting handoff brief: `C:/Users/Gebruiker/.claude/plans/session-HA11-bout-redo-pre-reg-drafting-handoff-2026-06-22.md`.
