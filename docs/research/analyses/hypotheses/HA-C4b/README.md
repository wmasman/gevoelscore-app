# HA-C4b — folder status

**Pre-registration (current)**: [`hypothesis.md`](hypothesis.md) — v3 **r2 LOCKED 2026-06-17** (drafted 2026-06-16; audit absorbed r2 2026-06-16; amended 2026-06-17 with `gesprek-met-M` mapping; §8.x cut 2026-06-17 per user option B; locked by user acceptance 2026-06-17). Fresh-session `/research-review` audit completed ([report](../../../reviews/HA-C4b-v3-2026-06-16.md), verdict PASS-with-caveats); all five Section-4 items closed in r2 (audit items 1-4 as wording-tightenings; item 5 originally absorbed as §8.x locked date-anchor sub-block then CUT per user direction "let's do B and not waste time on data interpretation; first we should run the tests" — the descriptive context now lives at the result.md interpretation layer rather than as a spec-locked artefact). r2 substantive content: empirical 2023-02-04 coverage check (confirmed pathological pattern Q3=8; §4.3 rationale rewritten as honest override-as-trade-off); audit Layer 2.5 substantive concern named in §8; §3.3 discipline-stretch acknowledgment in Authorship; verdict-invariant pacing-behaviour qualitative caveat per §9. **Headline cell UNCHANGED** from v2 (`unmedicated × pooled × S60_Mlow × N_std=1.5 × primary 4d × one-sided elevated`); §5.1 byte-identical with v2. Lock signal awaits explicit user acceptance + commit message naming the four §3.8 gate confirmations.

**Test handoff for the v3 run-session**: [`session-c4b-v3-test-handoff-2026-06-16.md`](../../../../../../.claude/plans/session-c4b-v3-test-handoff-2026-06-16.md) — paste-into-fresh-session brief for implementing the v3 `test.py` + running the §10.4 protocol + emitting v3 `result.md`.

## v2 archive

**Pre-registration (archived)**: [`hypothesis-v2-archived.md`](hypothesis-v2-archived.md) — locked 2026-06-16 commit `2417043` (relock to unmedicated pooled, r2 closures, fresh-session audit PASS-with-caveats). Test session executed 2026-06-16 in a fresh agent context per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock); the v2 lock-session was contaminated with v1 per-episode z-scores so the v2 run handed off to a clean context.

**Detection script (archived as v2 artefact)**: [`test.py`](test.py) — implements v2. Will be renamed `test-v2-archived.py` at v3 lock; the v3 test-session writes a new `test.py` per the v3 spec.

**Dry-run report (v2 artefact)**: [`dry-run-report.md`](dry-run-report.md) — v2 dry-run output. Will be renamed `dry-run-report-v2-archived.md` at v3 lock.

**Result (v2)**: [`result.md`](result.md) + [`result-data.json`](result-data.json) — v2 verdict **INCONCLUSIVE** (2026-06-16, commit `83a64b2`). v2 dry-run sanity gates passed at n = 10 (1b.i only); the full run applied §4.3 1b.ii (wake-window quartile-coverage) and dropped one train episode (`2023-02-04`, the highest-z episode in the train arm) → pooled n = 9 < §5.3 bar (n ≥ 10). Per v2 §9 INCONCLUSIVE branch: no SUPPORTED claim; descriptive companions reported. The v2 result.md "Critical methodological finding" block surfaced the §10.2 dry-run / full-run gate asymmetry as the v3 trigger.

## v1 archive

**Pre-registration (archived)**: [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md) — locked 2026-06-15 commit `80607e4`, **halted at dry-run** 2026-06-15.

**Dry-run report (archived)**: [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md) — sanity gates failed per v1 §7 + §10.4.

**Detection script (archived)**: [`test-v1-archived.py`](test-v1-archived.py) — implements v1's locked spec; do NOT execute (its dry-run prints first-3-episodes per phase × era including unmedicated, which is the v2 headline phase and would contaminate any same-context v2 test implementation).

## v1 status (preserved for audit trail)

v1 was locked but cannot produce a `result.md`. The §7 sanity gates fired:

- consolidation x train n = 0 (by phase-boundary construction; consolidation starts 2024-06-20, train ends 2023-12-31 — the locked headline cell is unsatisfiable for train).
- consolidation x validate n = 5 (below the §5.3 / §7 threshold of 10 after exertion-conditioning + §4.3 1b.i + §6 buildup-buffer).
- unmedicated median primary = 78 (outside the §7 anchor range [15, 60]; calibration miss — the anchor was bound to a definitional cousin's distribution rather than the exact column being measured).

Per §10.4 step 1 + §9 branching, the locked-pre-reg discipline halts the run and requires v2.

## v2 drafting options

Three structural paths surfaced at the halt:

1. **Move the headline to unmedicated phase.** Unmedicated has 8 train + 2 validate eligible crashes — meets the n >= 10 bar on the combined train arm. Strongest scientifically (early peek shows a discriminative lead-up profile on the 2023-02-04 episode at z = +3.7 on the day before crash). Cost: shifts the Wiggers-C4 question from the dose-stable consolidation phase (where citalopram is supposed to make the "stuck sympathetic" pattern *less* likely) to the unmedicated phase (where it should be most visible). Different question, different prior, defensible re-frame.

2. **Lock the headline to validate-only consolidation.** Accept n = 5, drop the both-eras requirement. Cost: explicit pre-registration of a lower n threshold + acknowledgment that statistical power is gone; the test becomes near-descriptive.

3. **Pool train + validate inside consolidation.** n = 5 episodes total. Cost: still underpowered, with the additional confound that the train/validate split's purpose (independent replication) is abandoned.

Plus two orthogonal fixes that v2 inherits regardless of which structural path is picked:

1. **§7 calibration-anchor fix.** The §7 anchor range [15, 60] was inherited from a definitional cousin's distribution; the actual column's median is 78. v2's §7 ranges must anchor to the exact column's descriptive card (see [`methodology/hypothesis_lock_process.md` §5](../../../methodology/hypothesis_lock_process.md#5-sanity-check-questions-before-lock) calibration-anchor row).

2. **§3 labels CSV path fix** (caught in HA-P7's audit per `reviews/HA-P7-2026-06-15.md` side-fix #5; queued in [`methodology/hypothesis_lock_process.md` §8.3](../../../methodology/hypothesis_lock_process.md#83-open-follow-ups-post-v11)). v1-archived §3 cites `crash_v2-definition/labels_crash_v2.csv` as the labels source; the file at that in-repo path is the *definition MD*, not the labels CSV. The labels CSV lives external at `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv` per the privacy boundary. v2's §3 (and §4.5 where it's also cited in v1) must point to the external path, with the in-repo `crash_v2-definition/definition.md` cited separately for the scheme. v1-archived is NOT being edited — the locked-pre-reg discipline holds; this fix lands in v2 only. First worked example of the new §3.5 side-fix propagation discipline being **absorbed by an already-archived sibling's v2 drafting** rather than retro-fixed as a standalone v2 (the queue path is supplanted when an unrelated v2 is already required).

## v1 → v2 history

v2 was drafted 2026-06-15 in a fresh session (per [`methodology/hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)) picking structural path 1 above (move headline to unmedicated phase, pooled across train + validate). The fresh-session [`/research-review` audit](../../../reviews/HA-C4b-v2-2026-06-15.md) verdict was PASS with caveats; all three caveats closed in r2 as wording-only sentence additions; v2 LOCKED 2026-06-16 commit `2417043`. Test session ran in another fresh agent context that day (the lock-session being contaminated with v1 per-episode z-scores).
