# HA-C4cp r2 dry-run report — sanity gates PASS

Emitted by `test.py --dry-run` per LOCKED r2 hypothesis.md §10.4. **Headline cell**: cross-phase-pooled stratum × `bout_n_did_not_return_2sd_day` × heavy-T-vs-non-heavy-T × {Mann-Whitney U + Cliff's δ + block-permutation null at E[L]=7} × two-bar SUPPORTED gate per §5.1 (block-perm p<0.05 + Cliff's δ ≥ +0.20). Day-validity per §4.4 (LC-era + sub-phase 4b/5 stratum + not April 2024 cluster + not first 21 device-baseline days + non-NaN `bout_n_did_not_return_2sd_day` [enforces reference-window validity per parent MD §3.2.2 ≥ 30-bout bar] + non-NaN `exertion_class_lagged_lcera`).

- Primary stratum non-NaN `bout_n_did_not_return_2sd_day` days: **1274**
- Heavy-T days: **465**
- Non-heavy-T days: **809**

**Stratum reproduction**: 1274 = 465 heavy + 809 non-heavy reproduces HA-C4c r2 result.md §3 headline arm-sum byte-identically on the parent operand determinism check (Gate 4 below). The 15-day reference-window-shortfall trim from the 1289-day pre-gate candidate documented in [descriptive_audit.md §1](../../descriptive/HA-C4cp/descriptive_audit.md#1-scope) as "corpus growth" is descriptively-reclassified here: those 15 non-heavy-T days pass HA-C4c's day-validity but fail HA-C4cp's additive reference-window validity gate per §4.4 gate 4. This is the pre-committed §4.4 left-edge-trim behavior; the trim does NOT block the walk-forward gate at §4.7 (both arms comfortably ≥ 30).

## Sanity gates per §10.4

| gate | description | observed | HALT threshold | result |
|---|---|---:|---|---|
| 1 | walk-forward n per arm (§4.7) | 465 heavy / 809 non-heavy | ≥ 30 per arm | **PASS** |
| 2 | per-day mean HALT window (§10.4 wider anchor) | 0.4765 | inside [0.01, 0.60] | **PASS** |
| 2 (informational) | per-day mean narrower anchor (§7) | 0.4765 | inside [0.05, 0.30] | outside (informational only; not a HALT) |
| 3 | per-day median HALT rule (§10.4) | 0.0000 | ≤ 2.0 | **PASS** |
| 3 (informational) | per-day median expected anchor (§7) | 0.0000 | inside [0, 1] | inside |
| 4 | parent operand determinism check (`bout_n_did_not_return` mean on primary stratum) | 0.6444 | 0.6444 (frozen HA-C4c-vintage) OR ~0.6485 (current corpus) | **PASS** (byte-identical to HA-C4c result.md target) |

**Auxiliary spot-check** (first 3 heavy-T days on primary stratum):

- 2022-11-20: `bout_n_did_not_return_2sd_day = 2`
- 2022-11-21: `bout_n_did_not_return_2sd_day = 1`
- 2022-11-23: `bout_n_did_not_return_2sd_day = 2`

**Auxiliary**: reference-window shortfall days on stratum (§4.4 gate 4 fires) = 15. These are 15 non-heavy-T days at the left edge of the sub-phase-4b stratum where the `[d-90, d-30]` lagged reference pool has < 30 bouts per parent MD §3.2.2 validity bar. Documented as expected per pre-reg §4.4 left-edge-trim discipline.

## DRY-RUN VERDICT: PASS — proceed with full run

Per HA-C4cp §10.4: all four dry-run sanity gates PASS. No HALT triggered. Walk-forward gate has adequate power (n=1274 well above the ≥30-per-arm bar). Parent operand determinism check confirms the pipeline extension at Bundle H+ event 8 (`521e9fe`) reproduces HA-C4c r2 result.md byte-identically on the frozen 1274-day HA-C4c-vintage stratum. **Full test authorized** per the dispatcher's dry-run gate.

## Cross-references

- [`hypothesis.md`](hypothesis.md) r2 LOCKED 2026-07-09 §10.4 sanity-gate HALT discipline + §7 pre-committed sanity ranges.
- [`test.py`](test.py) `dry_run_gates()` function (implements the four gates above).
- [`../../descriptive/HA-C4cp/descriptive_audit.md`](../../descriptive/HA-C4cp/descriptive_audit.md) LOCKED r1 2026-07-14 §5 walk-forward gate + §6 coverage summary (1289 pre-gate candidate; the 15-day-shortfall reclassification above is a small refinement to the Stage D audit's "corpus growth" framing at §1 — surfaced here but does NOT trigger a Stage D r1 → r2 revision because the descriptive claim stands modulo pandas-vs-`test.py`-filter precision differences).
- [`../HA-C4c/result.md`](../HA-C4c/result.md) LOCKED r2 for parent operand determinism target 0.6444.
- Parent MD [`bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md) §3.2.2 for reference-window construction + ≥ 30-bout validity bar.
