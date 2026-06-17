# HA-C4 — folder status

**Pre-registration (current)**: [`hypothesis.md`](hypothesis.md) — v1 **DRAFTED 2026-06-17**, awaiting fresh-session `/research-review` audit per [`hypothesis_lock_process.md` §3.4](../../../methodology/hypothesis_lock_process.md#34-audit-step-step-2-of-the-arc).

**Headline cell (drafted, not locked)**: unmedicated phase × 3-channel triad × heavy-T-vs-non-heavy-T × Mann-Whitney + Cliff's delta × block-permutation null E[L]=7 × **pass-2-of-3 verdict rule** applied independently per era.

The three channels (per [`wiggers_test_design_on_chained_regime.md` §C4](../../../methodology/wiggers_test_design_on_chained_regime.md#c4--we-class-3-channel-confirmatory-triad)):

| channel | metric | Wiggers source |
|---|---|---|
| Ch1 (decay, primary) | `stress_post_peak_time_to_rest_min` on T | PDF lines 1140-1141, 1223-1231 |
| Ch2 (walls, secondary) | `stress_high_duration_min` on T | PDF lines 1112-1119 |
| Ch3 (t+1 reactivity, secondary) | `awake_stress_avg` on T+1 | PDF lines 1141-1143 |

## Sister-test context

HA-C4 tests the **pattern-existence** claim ("does post-exertion recovery degrade?"). The sister tests came at the same Wiggers C4 question from different angles:

- **[HA-C4b](../HA-C4b/)**: tested the **crash-precursor** framing on the motion-filter operationalisation (`stress_low_motion_min_count_S60_Mlow` over the 4-day lead-up window). Verdict at v3: **NOT-SUPPORTED** ((a)=40%, (b)=-10pp, (c)=+1.21).
- **[HA11](../HA11-stress-udip/)**: tested the **inverse** signal (within-day stress U-dip count = sharp recovery). Verdict on train: **SUPPORTED** (+22.8pp). The failure-to-dip arm was distribution-bounded zero.

HA-C4 is the direct test of the failure-to-recover signal that HA11's metric structurally couldn't capture, and the descriptive-pattern test that HA-C4b's precursor framing didn't speak to.

## Drafting discipline note

v1 was drafted in the same Claude session that ran HA-C4b v3 (per [`hypothesis_lock_process.md` §3.2 clause](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) allowing shared-context drafting). The data-exposure boundary is documented in the v1 Authorship block: the drafter knows which 10 unmedicated heavy-T days are also crash episodes (from HA-C4b's pool); the drafter has NOT seen HA-C4's specific channel values on individual days. The fresh-session §3.4 audit is the integrity check on §4 / §5 operational choices.

## Test-execution handoff (not yet written; written after lock)

Same pattern as HA-C4b v3's test handoff: paste-into-fresh-session brief, mechanical implementation of `test.py` per §10 of the spec, runs against the locked v1 hypothesis. Will be written after v1 r2 lock.

## Lock arc

| stage | status | session venue |
|---|---|---|
| 1. Draft | DONE (commit pending) | this session (shared-context per §3.2 clause) |
| 2. Audit (§3.4) | pending | **fresh session** (paste audit handoff) |
| 3. Revise r2 (§3.5) | pending | this session continues OR new session |
| 4. Re-audit (§3.6) | optional / compressible | **fresh session** OR compression decision |
| 5. Lock (§3.8) | pending | this session |
| 6. Test execution (§3.9) | pending | **fresh session** (paste test handoff) |
| 7. Result review | pending | this session |
