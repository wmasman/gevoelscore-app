# HA-C3 — folder status

**Pre-registration (current)**: [`hypothesis.md`](hypothesis.md) — **v1 drafted, not locked** (2026-06-22). Producer-mode draft under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default) per fresh-session handoff brief `session-HA-C3-pre-reg-drafting-handoff-2026-06-22.md`. Tier-1 Wiggers completion per the [register Priority shortlist](../../../wiggers_testable_hypotheses.md#tier-1--source-verified-verbatim--no-family-history-priority-pre-regs) — HA-C3 was the only Tier-1 Wiggers row without an HA-folder.

**Headline cell (drafted, not locked)**: unmedicated phase × full Stratum 4 single pool × `all_day_stress_avg` binned at (0-20, 20-30, 30-40, 40-60, 60+) × `gevoelscore` × **3-condition gated verdict**: (a) Jonckheere-Terpstra monotone-decreasing trend + (b) second-difference contrast convex (`S < 0`) + (c) natural-cubic-spline non-linearity with convex-direction second-derivative sign × block-permutation null E[L]=7.

**Verdict bands** (3-condition gated): 3-of-3 met = **SUPPORTED**; 2-of-3 = **PARTIAL**; ≤ 1-of-3 OR any wrong-direction firing = **REJECTED**.

**Lock arc** (per [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md)):

| stage | status | session venue | output |
|---|---|---|---|
| 1. Draft (§3.2) | **DONE 2026-06-22** | fresh session per handoff brief | THIS COMMIT |
| 2. Audit (§3.4) | pending | **fresh session** via `/research-review docs/research/analyses/hypotheses/HA-C3/hypothesis.md` | `docs/research/reviews/HA-C3-<date>.md` |
| 3. Revise r2 (§3.5) | pending | shared-context with drafting (acceptable) | revised `hypothesis.md` |
| 4. Re-audit (§3.6) | pending | **fresh session** OR compressed per §3.6 criteria | (n/a if compressed) |
| 5. Lock (§3.8) | pending | shared-context | lock commit + register-row pointer update |
| 6. Test execution (§3.9) | pending | fresh session post-lock | new `test.py` + `result.md` |

## Sister-test context

HA-C3 tests Wiggers' **C3 verbatim claim** (PDF lines 1357-1368: "a day with a score of 40 is much more tiring than a day with a score of 30 — a step appears very small on the graph, but it isn't"). The sister Tier-1 Wiggers test ([HA-C4 v2](../HA-C4/)) is at a different claim shape and has been tested:

| sibling | claim shape | verdict |
|---|---|---|
| [HA-C4 v2](../HA-C4/) | post-exertion recovery dynamics (3-channel triad: decay / walls / t+1 reactivity) | REJECTED at daily-aggregate 2026-06-18 (commit `52bddb5`) |
| [HA11](../HA11-stress-udip/) | within-day stress U-dip count (the *inverse* signal — calm-day signal) | SUPPORTED on train (+22.8pp) |
| **HA-C3** (drafted, not locked) | **cross-day shape of stress→fatigue function** (convex / accelerating decrement) | pending |

HA-C3 is the direct test of the cross-day-aggregate-mapping-shape claim that the recovery-dynamics and within-day-shape sister tests structurally cannot speak to.

## Drafting discipline note

v1 was drafted in a worktree-isolated session 2026-06-22 with the drafter having read end-to-end the register C3 row + verification log + the modern HA-C4 v2 template (shape reference only — HA-C3's claim is structurally distinct) + the binding methodology MDs (`citalopram_phase_stratification`, `citalopram_dose_response_stress_mean_sleep`, `train_validate_split_fate`, `permutation_null_block_length`, `time_resolution`, `hypothesis_lock_process`, `CONVENTIONS`). The drafter has NOT inspected the joint `all_day_stress_avg` × `gevoelscore` distribution beyond the marginal coverage stats per `DATA_DICTIONARY.md` (per the Authorship block "Data exposure context" disclosure). The §4.4 citalopram approach choice (§5.A primary), the §4.1 bin specification (register-verbatim), the §4.5.1 (b) convexity contrast vector (second-difference primary), the §4.5.1 (c) spline knot placement (at bin boundaries), and the §5.1 3-condition verdict bar are pre-committed before any joint-distribution inspection.

## Test-execution handoff (not yet written; written after v1 lock)

Same pattern as HA-C4 v2's test handoff: paste-into-fresh-session brief, mechanical implementation of `test.py` per §10 of the v1 spec, runs against the locked v1 hypothesis. Will be written after v1 lock (post-audit absorption).
