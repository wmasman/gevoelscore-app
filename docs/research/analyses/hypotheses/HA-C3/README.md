# HA-C3 — folder status

**Pre-registration (current)**: [`hypothesis.md`](hypothesis.md) — **v2 r1 drafted, not locked** (2026-06-23). Producer-mode draft under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default) per fresh-session handoff brief `session-HA-C3-v2-redraft-handoff-2026-06-23.md`. v2 is the post-HALT spec revision after v1 r2 test-execution HALTed on §7.5 Gate 1 (B1 [0,20) n = 0 structurally absent; B5 [60,100] n = 1). Per [`hypothesis_lock_process §10.4 step 3`](../../../methodology/hypothesis_lock_process.md#104-five-stage-arc-iteration-policy) ("any post-dry-run revision creates v2"), v2 is the required response.

**v1 lineage**: v1 r1 drafted 2026-06-22 → v1 r2 LOCKED 2026-06-23 (commit `de22b68`) → v1 r2 test-executed 2026-06-23 (commit `a9423af`) → **HALT on §7.5 Gate 1**. v1 artefacts archived at [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md), [`test-v1-archived.py`](test-v1-archived.py), [`result-v1-archived.md`](result-v1-archived.md), [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md).

**Headline cell (v2; drafted, not locked)**: unmedicated phase × full Stratum 4 single pool × `all_day_stress_avg` binned at **(0-30, 30-40, 40-60, 60+)** × `gevoelscore` × **3-condition gated verdict**: (a) Jonckheere-Terpstra monotone-decreasing trend + (b) second-difference contrast convex (`S = (Δ²_2 + Δ²_3) / 2 < 0`) + (c) natural-cubic-spline non-linearity with 3 internal knots + ≥ 2 of 3 segment-midpoint negative spline-second-derivative × block-permutation null E[L] = 7. **v2 §7.3 halt-option-A pre-committed for B4** (widen B3 to absorb B4 automatically if B4 n < 30 at dry-run; closes the v1 halt-mismatch rough edge).

**Verdict bands** (3-condition gated): 3-of-3 met = **SUPPORTED**; 2-of-3 = **PARTIAL**; ≤ 1-of-3 OR any wrong-direction firing = **REJECTED**.

**Lock arc** (per [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md)):

| stage | status | session venue | output |
|---|---|---|---|
| 1. Draft v2 r1 (§3.2) | **DONE 2026-06-23** | fresh worktree-isolated session per handoff brief | THIS COMMIT |
| 2. Audit v2 (§3.4) | pending | **fresh session** via `/research-review docs/research/analyses/hypotheses/HA-C3/hypothesis.md` | `docs/research/reviews/HA-C3-v2-<date>.md` |
| 3. Revise v2 r2 (§3.5) | pending | shared-context with drafting (acceptable) | revised `hypothesis.md` |
| 4. Re-audit v2 (§3.6) | pending | **fresh session** OR compressed per §3.6 criteria | (n/a if compressed) |
| 5. Lock v2 (§3.8) | pending | shared-context | lock commit + register-row pointer update |
| 6. Test execution v2 (§3.9) | pending | fresh session post-lock | new `test.py` + `result.md` |

**v1 lock arc completed** (for audit traceability): v1 r1 drafted 2026-06-22 → audit v1 fresh-session report `8f3f269` (PASS with caveats) → v1 r2 absorbed audit per §3.6-compression → v1 r2 LOCKED 2026-06-23 `de22b68` → v1 r2 test-executed 2026-06-23 `a9423af` → **HALT on §7.5 Gate 1** → v2 redraft this commit per §10.4 step 3.

## Sister-test context

HA-C3 tests Wiggers' **C3 verbatim claim** (PDF lines 1357-1368: "a day with a score of 40 is much more tiring than a day with a score of 30 — a step appears very small on the graph, but it isn't"). The sister Tier-1 Wiggers test ([HA-C4 v2](../HA-C4/)) is at a different claim shape and has been tested:

| sibling | claim shape | verdict |
|---|---|---|
| [HA-C4 v2](../HA-C4/) | post-exertion recovery dynamics (3-channel triad: decay / walls / t+1 reactivity) | REJECTED at daily-aggregate 2026-06-18 (commit `52bddb5`) |
| [HA11](../HA11-stress-udip/) | within-day stress U-dip count (the *inverse* signal — calm-day signal) | SUPPORTED on train (+22.8pp) |
| **HA-C3 v2** (drafted, not locked) | **cross-day shape of stress→fatigue function** (convex / accelerating decrement) on the corpus-stress-range AS-REPRESENTED per §8 caveat 7 | pending |

HA-C3 is the direct test of the cross-day-aggregate-mapping-shape claim that the recovery-dynamics and within-day-shape sister tests structurally cannot speak to.

## Drafting discipline note (v2)

v2 r1 was drafted in a worktree-isolated session 2026-06-23 with the drafter HAVING seen the v1 partial-pool descriptives (pool n = 581, stress median 34, gevoelscore median 4, populated-bins trajectory v1 B2-B3-B4 = 3.958 → 4.265 → 3.860 per v1 result.md / dry-run-report.md). Per the v2 Authorship block "Data exposure context" disclosure + §8 caveat 9 + §8 caveat 11, the v2 bin scheme is the minimum-viable v1-HALT response with the v1 partial-pool trajectory treated as a **caveat-class prior per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), NOT promoted to a v2 substantive output**. v2 inherits the substantive question (Wiggers' verbatim C3 convex claim) unchanged from v1; v2 revises only the operationalisation for testability under the corpus's stress-distribution property.

## Test-execution handoff (not yet written; written after v2 lock)

Same pattern as HA-C4 v2's test handoff: paste-into-fresh-session brief, mechanical implementation of `test.py` per §10 of the v2 spec (including the automatic §7.3 halt-option-A absorption on B4 if dry-run shows n < 30), runs against the locked v2 hypothesis. Will be written after v2 lock (post-audit absorption).
