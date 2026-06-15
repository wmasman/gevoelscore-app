# HA-C4b — folder status

**Pre-registration**: [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md) — locked 2026-06-15 commit `80607e4`, **halted at dry-run** 2026-06-15.

**Dry-run report**: [`dry-run-report.md`](dry-run-report.md) — sanity gates failed per §7 + §10.4.

**Detection script**: [`test.py`](test.py) — implements the locked spec; not re-runnable against v1.

## Status

v1 is locked but cannot produce a `result.md`. The §7 sanity gates fired:

- consolidation x train n = 0 (by phase-boundary construction; consolidation starts 2024-06-20, train ends 2023-12-31 — the locked headline cell is unsatisfiable for train).
- consolidation x validate n = 5 (below the §5.3 / §7 threshold of 10 after exertion-conditioning + §4.3 1b.i + §6 buildup-buffer).
- unmedicated median primary = 78 (outside the §7 anchor range [15, 60]; calibration miss — the anchor was bound to a definitional cousin's distribution rather than the exact column being measured).

Per §10.4 step 1 + §9 branching, the locked-pre-reg discipline halts the run and requires v2.

## v2 drafting options

Three structural paths surfaced at the halt:

1. **Move the headline to unmedicated phase.** Unmedicated has 8 train + 2 validate eligible crashes — meets the n >= 10 bar on the combined train arm. Strongest scientifically (early peek shows a discriminative lead-up profile on the 2023-02-04 episode at z = +3.7 on the day before crash). Cost: shifts the Wiggers-C4 question from the dose-stable consolidation phase (where citalopram is supposed to make the "stuck sympathetic" pattern *less* likely) to the unmedicated phase (where it should be most visible). Different question, different prior, defensible re-frame.

2. **Lock the headline to validate-only consolidation.** Accept n = 5, drop the both-eras requirement. Cost: explicit pre-registration of a lower n threshold + acknowledgment that statistical power is gone; the test becomes near-descriptive.

3. **Pool train + validate inside consolidation.** n = 5 episodes total. Cost: still underpowered, with the additional confound that the train/validate split's purpose (independent replication) is abandoned.

Plus an orthogonal calibration fix that v2 inherits regardless of which path is picked: the §7 anchor range [15, 60] was inherited from a definitional cousin's distribution; the actual column's median is 78. v2's §7 ranges must anchor to the exact column's descriptive card (see [`methodology/hypothesis_lock_process.md` §5](../../../methodology/hypothesis_lock_process.md#5-sanity-check-questions-before-lock) calibration-anchor row).

## Next action

Open a fresh agent session for v2 drafting per [`methodology/hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc). The drafting session's first task is to pick one of the three structural paths above (or surface a fourth). The v2 pre-reg lives at `hypothesis.md` in this folder when drafted; v1 stays archived at `hypothesis-v1-archived.md` for the audit trail.
