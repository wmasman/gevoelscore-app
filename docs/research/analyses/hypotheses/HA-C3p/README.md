# HA-C3p — folder status

**Pre-registration (current)**: [`hypothesis.md`](hypothesis.md) — **drafted 2026-06-23 by Claude (Opus 4.7, 1M context) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default)**. Status: drafted, not locked.

**What this pre-reg is**: the **project-canonical personal-baseline-anchored sister test** to [HA-C3 v2 r1](../HA-C3/hypothesis.md) (the Wiggers-verbatim arm). HA-C3p tests the **underlying convex stress→fatigue shape claim** Wiggers describes (PDF lines 1357-1368, "Annual Stress Scores") on **personal-baseline-anchored equal-N quintile bins** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds), rather than the verbatim 30→40 numerical anchor which HA-C3 v2 tests. The user's framing per the session handoff §1: HA-C3 v2 stays honest against the original Wiggers document; **HA-C3p goes further to see if we can find the mechanism Wiggers is describing besides the numbers she uses**.

**Headline cell (drafted, not locked)**: §5.A unmedicated phase × full Stratum 4 single pool × `all_day_stress_avg` binned at the §4.1 personal-baseline-anchored quintile boundaries (Q1 `[0, 28)`, Q2 `[28, 31)`, Q3 `[31, 34)`, Q4 `[34, 37)`, Q5 `[37, 100]`) × `gevoelscore` bin-mean × {Jonckheere-Terpstra monotone-decreasing test + convexity second-difference contrast `S = (Δ²_2 + Δ²_3 + Δ²_4) / 3` + spline non-linearity test with 4 internal knots at the quintile bin boundaries + spline-second-derivative sign at ≥ 3 of 4 contributing midpoints} × block-permutation null E[L] = 7 × 3-condition gated verdict per [hypothesis.md §5](hypothesis.md#5-pre-registered-falsification-criterion-locked).

## Sister-pre-reg framing — load-bearing for §1 + §9

HA-C3p is drafted as a **sister pre-reg to HA-C3 v2 r1** per the [drafting handoff brief](file:///C:/Users/Gebruiker/.claude/plans/session-HA-C3p-pre-reg-drafting-handoff-2026-06-23.md). The two pre-regs test the same Wiggers C3 substantive question at substantively distinct operationalisation levels:

| HA-C3 v2 verdict | HA-C3p verdict | reading |
|---|---|---|
| SUPPORTED | SUPPORTED | strong Wiggers C3; both numerical anchor AND underlying shape fire |
| SUPPORTED | REJECTED | suspicious bin-edge artefact in v2's Wiggers-verbatim (under-fit by personal-range test) |
| REJECTED | SUPPORTED | convex shape exists on participant's range, but NOT at Wiggers' specific anchors — Wiggers' numbers are wrong-for-this-participant, **underlying shape is real** (the centerpiece "mechanism besides numbers" finding) |
| REJECTED | REJECTED | informative null on both operationalisations |

Each pre-reg's §5 verdict stands on its own; the **4-cell agreement matrix interpretation** lives in HA-C3p's result.md §6 open-questions per the [hypothesis.md Locked decision 5](hypothesis.md#authorship). HA-C3 v2's result.md §6 will cross-link back to HA-C3p's framing at test-execution time. The sister-pre-reg framing does NOT modify either pre-reg's §5 verdict; it is the cross-test reading layered on top of each independent verdict.

## Draft-time bin boundary snapshot — load-bearing for §4.1 + §7.5 Gate 5

The §4.1 quintile bin boundaries are **pre-committed at draft time** per [hypothesis.md Locked decision 4](hypothesis.md#authorship):

- **`per_day_master.csv` SHA-256**: `d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d` (computed 2026-06-23 at draft time)
- **Quintile boundaries**: `[28, 31, 34, 37]` (rounded to integers; `all_day_stress_avg` is int 0-100 per [DATA_DICTIONARY.md §7B](../../../DATA_DICTIONARY.md))
- **Full Stratum 4 pool n**: 1351 days (post-§4.3 gate); per-bin n = [248, 253, 294, 251, 305]
- **§5.A unmedicated sub-arm n**: 581 days (matches v1 dry-run); per-bin n = [45, 80, 129, 138, 189] (REUSING full-pool boundaries per cross-arm cleanliness; all bins ≥ 30 sanity gate)

The §7.5 Gate 5 sanity check at test-execution time will re-compute the quintile boundaries on the test-time snapshot; any > 1 stress-unit shift HALTs the test and requires HA-C3p-v2 with the new snapshot per [hypothesis.md §7.5](hypothesis.md#75-sanity-gate-halt-triggers-at-dry-run).

## Lock arc

Per [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md) 5-stage canonical arc:

| stage | status | venue | output |
|---|---|---|---|
| 1. Draft (§3.2) | DONE 2026-06-23 | producer-mode under authorisation; this folder | THIS COMMIT |
| 2. Audit (§3.4) | pending | fresh session (paste `/research-review docs/research/analyses/hypotheses/HA-C3p/hypothesis.md`) | `docs/research/reviews/HA-C3p-<date>.md` |
| 3. Revise r2 (§3.5) | pending | shared-context with drafting | r2 of `hypothesis.md` |
| 4. Re-audit (§3.6) | pending or compressible | fresh session OR documented compression | `docs/research/reviews/HA-C3p-<date>-v2.md` OR compression note |
| 5. Lock (§3.8) | pending | shared-context | lock-commit + Authorship `Status: LOCKED` + Wiggers C3 register-row pointer added per Locked decision 6 |
| 6. Test execution (§3.9) | pending post-lock | shared-context (test handoff brief) | `test.py` + `result.md` |

## Sister-test context

- **[HA-C3 v2 r1](../HA-C3/)** — the **Wiggers-verbatim sister test** (draft commit `724c814` 2026-06-23). Tests Wiggers' specific 30→40 numerical anchor on `[0,30), [30,40), [40,60), [60,100]` 4-bin scheme. HA-C3p tests the underlying shape mechanism on quintile bins. **Cross-test reading per the §1 4-cell agreement matrix → HA-C3p result.md §6 open-questions**.
- **[HA-C3 v1 archived](../HA-C3/hypothesis-v1-archived.md)** — the 5-bin precedent that HALTed on B1=0 + B5=1 underpower (`a9423af` 2026-06-23). The v1 partial-pool descriptive trajectory (B2-B3-B4 = 3.958 → 4.265 → 3.860) enters HA-C3p as a [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class prior per [hypothesis.md §8 caveat 5](hypothesis.md#8-caveats-resultmd-must-explicitly-acknowledge), informing interpretation without being promoted to a substantive HA-C3p output.
- **[HA-C4 v2](../HA-C4/)** — the daily-aggregate Wiggers C4 sister test. REJECTED 2026-06-18 at triad sum 0/3 (commit `52bddb5`). Substantively distinct claim (recovery-dynamics triad, not same-day shape).
- **[HA11-stress-udip](../HA11-stress-udip/)** — the within-day stress U-dip count test. SUPPORTED on train (+22.8 pp, median signed z = 2.168). Structurally distinct (within-day vs cross-day-aggregate).

## Cross-references

- Sister pre-reg: [`HA-C3/hypothesis.md`](../HA-C3/hypothesis.md) (v2 r1 Wiggers-verbatim arm; draft commit `724c814`).
- v1 archived precedent: [`HA-C3/hypothesis-v1-archived.md`](../HA-C3/hypothesis-v1-archived.md) + [`HA-C3/result-v1-archived.md`](../HA-C3/result-v1-archived.md) (5-bin LOCKED → HALT 2026-06-23 `a9423af`).
- Methodology — citalopram channel inheritance: [`citalopram_phase_stratification.md` §4](../../../methodology/citalopram_phase_stratification.md#4-per-channel-inheritance-rules) (load-bearing for §4.4 §5.A unmedicated headline + §5.B dose-adjusted sensitivity arm pattern).
- Methodology — dose-response β anchor: [`citalopram_dose_response_stress_mean_sleep.md` §5.6.1](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read) (+0.57/mg β for `all_day_stress_avg` used in §5.B dose-adjustment).
- Methodology — block-permutation null: [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) (E[L]=7 anchor + factor-of-2 flag).
- Methodology — full Stratum 4 single pool default: [`train_validate_split_fate.md`](../../../methodology/train_validate_split_fate.md).
- Conventions — personal baseline framing: [`CONVENTIONS.md §3.1`](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) (load-bearing for HA-C3p's quintile-bin operationalisation).
- Conventions — caveat-class framing: [`CONVENTIONS.md §4.2`](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) (load-bearing for v1 partial-pool non-monotone observation treatment).
- Wiggers register: [`wiggers_testable_hypotheses.md` C3 row](../../../wiggers_testable_hypotheses.md#c3--non-linear--convex-stressfatigue) (will be updated at HA-C3p lock per Locked decision 6: HA-C3p as personal-baseline-anchored sister test pointer under the existing C3 row; one register entry per Wiggers source row).
- Hypothesis lock process: [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md).
- Bin boundary derivation script: [`../../../../scripts/compute_HA-C3p_quintile_boundaries.py`](../../../../scripts/compute_HA-C3p_quintile_boundaries.py) (worktree-side at draft time; canonical `test.py` will re-validate at dry-run per §7.5 Gate 5).
- Drafting handoff brief: `C:/Users/Gebruiker/.claude/plans/session-HA-C3p-pre-reg-drafting-handoff-2026-06-23.md`.
