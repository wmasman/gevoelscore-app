# HA-C4 — folder status

**Pre-registration (current)**: [`hypothesis.md`](hypothesis.md) — **v2 drafted 2026-06-18, NOT YET LOCKED**. Composite-path post-v1-dry-run-halt revision per the v1 dry-run report's "Recommendation for HA-C4-v2" triage section. Three integrated structural changes: §5.3 explicit INCONCLUSIVE handling (Option A) + §7.3 arithmetic rebuild (Option E first half — bug fix only) + new §4.11.3 Ch3 validate sensitivity arm with chain-T+1 relaxed (Option C as descriptive sensitivity, NOT promoted to primary).

**v2 lock arc** (per [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md)):

| stage | status | session venue | output |
|---|---|---|---|
| 1. Draft (§3.2) | **DONE 2026-06-18** | this session (fresh) per composite-path handoff brief at [`.claude/plans/session-c4-v2-draft-handoff-2026-06-18.md`](../../../../../../.claude/plans/session-c4-v2-draft-handoff-2026-06-18.md) | this commit |
| 2. Audit (§3.4) | pending | **fresh session** (paste `/research-review` brief) | `reviews/HA-C4-v2-<date>.md` |
| 3. Revise r2 (§3.5) | pending | shared-context with drafting | revised `hypothesis.md` |
| 4. Re-audit (§3.6) | pending or compress | **fresh session** OR §3.6 compression decision | `reviews/HA-C4-v2-<date>-v2.md` (canonical) |
| 5. Lock (§3.8) | pending | shared-context | LOCK COMMIT + register-row pointer + 4 §3.8 gate confirmations |
| 6. Test execution (§3.9) | pending | **fresh session** | new `test.py` + `result.md` |

**Headline cell (drafted, not locked)**: unmedicated phase × 3-channel triad × heavy-T-vs-non-heavy-T × Mann-Whitney + Cliff's delta × block-permutation null E[L]=7 × **v2 INCONCLUSIVE-aware triad verdict rule** (per-channel: CONFIRMED 1.0 / CONFIRMED-PARTIAL 0.5 / REFUTED 0; triad sum bands: 3.0 SUPPORTED-strong / 2.0-2.5 SUPPORTED / 1.0-1.5 PARTIAL / <1.0 REJECTED).

The three channels (per [`wiggers_test_design_on_chained_regime.md` §C4](../../../methodology/wiggers_test_design_on_chained_regime.md#c4--we-class-3-channel-confirmatory-triad)):

| channel | metric | Wiggers source |
|---|---|---|
| Ch1 (decay, primary) | `stress_post_peak_time_to_rest_min` on T | PDF lines 1140-1141, 1223-1231 |
| Ch2 (walls, secondary) | `stress_high_duration_min` on T | PDF lines 1112-1119 |
| Ch3 (t+1 reactivity, secondary) | `awake_stress_avg` on T+1 (chain-T+1 excluded per §4.7) | PDF lines 1141-1143 |

**Expected v2 outcome on the v1 cell counts** (if Ch1, Ch2 confirm both eras and Ch3 train confirms): triad sum = 1.0 + 1.0 + 0.5 = 2.5 → **SUPPORTED**. Ch3 validate INCONCLUSIVE (n=25) does NOT halt the test in v2; it routes via §5.3 to CONFIRMED-PARTIAL (0.5 contribution) at the channel-aggregation layer.

## Sister-test context

HA-C4 tests the **pattern-existence** claim ("does post-exertion recovery degrade?"). The sister tests came at the same Wiggers C4 question from different angles:

- **[HA-C4b](../HA-C4b/)**: tested the **crash-precursor** framing on the motion-filter operationalisation (`stress_low_motion_min_count_S60_Mlow` over the 4-day lead-up window). Verdict at v3: **NOT-SUPPORTED** ((a)=40%, (b)=-10pp, (c)=+1.21).
- **[HA11](../HA11-stress-udip/)**: tested the **inverse** signal (within-day stress U-dip count = sharp recovery). Verdict on train: **SUPPORTED** (+22.8pp). The failure-to-dip arm was distribution-bounded zero.

HA-C4 is the direct test of the failure-to-recover signal that HA11's metric structurally couldn't capture, and the descriptive-pattern test that HA-C4b's precursor framing didn't speak to.

## v1 archive

**Pre-registration (archived)**: [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md) — **LOCKED 2026-06-17 r2 at commit `da79387`**. Fresh-session [`/research-review` audit](../../../reviews/HA-C4-v1-2026-06-17.md) verdict REVISION RECOMMENDED; 3 substantive fires (L1.4 §7-anchor specificity, L4.4 crash-drop sensitivity, L2.5 shared-context drafting) + 3 minor fires (L3.1, L4.5, L4.7) all absorbed in r2 as mechanical closures. §3.6 re-audit compressed per the criteria. User accepted L2.5 boundary as priced-in + L4.4 closure option (a) sensitivity arm at r2.

**Detection script (archived)**: [`test-v1-archived.py`](test-v1-archived.py) — implements v1's locked r2 spec. **Do NOT execute** against v2 — the v1 §5.3 binary verdict rule will fire HALT on Ch3 validate INCONCLUSIVE; v2 test.py (written in a separate post-v2-lock session per `hypothesis_lock_process.md` §3.9) will implement the v2 INCONCLUSIVE-aware §5.3.

**Dry-run report (archived)**: [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md) — **HALTED at §7.5 gate 2** (Ch3 validate heavy-T n=25 < 30 inconclusive bar; commit `19d33e4`). Surfaced two audit-able spec findings v2 must absorb: the binding sample-size shortfall (closed by v2 §5.3 explicit INCONCLUSIVE handling) AND the §7.3 arithmetic discrepancy (train heavy-T claimed n=206 vs actual n=171; closed by v2 §7.3 rebuild). The "Recommendation for HA-C4-v2" section is the primary source for v2's design.

## v1 status (preserved for audit trail)

v1 was locked but cannot produce a `result.md`. The §7.5 sanity gates fired:

- Channel 3 validate heavy-T arm n = 25 < 30 (binding §5.4 inconclusive-bar / §7.5 gate-2 failure; §4.7 chain-T+1 exclusion dropped 16 of 41 validate heavy-T days).
- Channel 3 train heavy-T arm n = 117 PASS (171 − 54 chain-dropped).
- Distribution-sanity gate 1 (full-pool channel medians within ±30%) PASS.
- Ch1 NaN-fraction sanity gate 3 (within [12%, 25%]) PASS.

Per v1 §10.4 step 1 + §9.5 + locked-pre-reg discipline, the run halted and required v2.

## v1 → v2 history

v2 was drafted 2026-06-18 in a fresh session (per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)) per a composite-path handoff brief identified by a separate fresh-session triage analysis from the v1 dry-run report. The composite path: Option A (explicit INCONCLUSIVE handling in §5.3) + §7.3 arithmetic rebuild (Option E first half — bug fix only) + Option C as §4.11.3 descriptive sensitivity arm (chain-T+1 relaxed Ch3 validate; NOT promoted to primary). The other dispositions (Option B = extend validate window — not viable; Option D = drop Ch3 entirely — too aggressive structural change; Option E second half = lower the §5.4 bar — judged less defensible than INCONCLUSIVE-aware aggregation) were rejected at triage.

## Drafting discipline note

v1 was drafted in the same Claude session that ran HA-C4b v3 (shared-context per `hypothesis_lock_process.md` §3.2 clause); the data-exposure boundary is permanently documented in [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md) §Authorship. v2 was drafted in a fresh session with only the v1 hypothesis.md / test.py / dry-run-report.md / composite-path handoff brief as input — no per-day per-channel values from the v1 test (the v1 full run never executed because of the halt). The §3.2-clause shared-context concern from v1 (user-accepted as priced-in per audit L2.5) remains the documented boundary; v2 does not introduce new exposure to per-day data.

## Test-execution handoff (not yet written; written after v2 lock)

Same pattern as HA-C4b v3's test handoff: paste-into-fresh-session brief, mechanical implementation of `test.py` per §10 of the v2 spec, runs against the locked v2 hypothesis. Will be written after v2 r2 lock (post-audit absorption).
