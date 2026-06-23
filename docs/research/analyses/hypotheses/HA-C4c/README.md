# HA-C4c — folder status

**Pre-registration (current)**: [`hypothesis.md`](hypothesis.md) — **drafted 2026-06-23 by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs)**. Status: drafted, not locked.

**What this pre-reg is**: the **cascade-resuming substantive Wiggers C4 retest at bout-level resolution** per the enabled-at-lock register row in [`bout_level_recovery_dynamics.md` §1.3](../../../methodology/bout_level_recovery_dynamics.md#13-wiggers-register-rows-this-md-enables-at-lock--narrow) (parent MD LOCKED `c57ff3f` 2026-06-21). Tests whether the per-day operand `bout_n_did_not_return_day` (per-day count of bouts where stress fails to return to baseline within 180 minutes of peak per parent MD §3.2) is systematically higher on heavy-T days than on non-heavy-T days, in the cross-phase-pooled stratum (phase 5 + phase 6), with the unmedicated-only stratum as a primary sensitivity arm for cross-test consistency with HA11-bout-redo. Single-operand verdict: SUPPORTED / PARTIAL / REJECTED / INCONCLUSIVE per the INCONCLUSIVE-aware verdict-rule pattern collapsed from [HA-C4 v2 §5.3](../HA-C4/hypothesis.md#53-triad-verdict-rule-v2-rewritten-with-explicit-inconclusive-handling) to single-operand shape.

**Headline cell (drafted, not locked)**: cross-phase-pooled stratum (phase 5 `pacing_habit_established` UNION phase 6 `citalopram_modulated`) × `bout_n_did_not_return_day` × heavy-T-vs-non-heavy-T × Mann-Whitney U + Cliff's delta + block-permutation null at E[L]=7 × {(a) p < 0.05 + (b) Cliff's delta ≥ +0.20 in predicted positive direction}.

## Cascade context — load-bearing for §8 caveats

HA-C4c is drafted with four cascade-context findings baked into §8 caveats per the [drafting handoff brief](file:///C:/Users/Gebruiker/.claude/plans/session-HA-C4c-pre-reg-drafting-handoff-2026-06-23.md):

1. **HA11-bout-redo PARTIAL framework-validity** (commit `6e06d12`): bars 1+2 PASS at +20.26 pp / median signed z 2.410; bar 3 FAIL at p=0.2609 on the n_calm=70/n_crash=11 stratum. The bout-level operand is *partially fit for purpose*; HA-C4c verdict-magnitudes carry a calibration discount per HA11-bout-redo §9.2. Captured in §8 caveat 2.
2. **β-recalibration r4 0/7 CONFIRMED LOCKED** (commit `fb97d1c`): Approach A is NOT load-bearing at this corpus's bout-level n; **HA-C4c primary outcome is dose-naive** + cross-phase pooling permissible per [STOCKTAKE §6 architectural-implications paragraph](../../../STOCKTAKE.md#6-cross-section-synthesis). Captured in §8 caveat 3 + §4.9 (Approach A relegated to sensitivity arm with inheritance-by-analogue framing).
3. **99.3% motion-confound corpus property** (4285/4317 bouts carry `motion_confound_flag=True` per HA11-bout-redo result §4): the entire HA-C4c operand inherits this; "rest-stress" semantics operationalise against the motion-tagged bout pool. Captured in §8 caveat 4 + §4.10 motion-clean-only sensitivity arm (anticipated INCONCLUSIVE).
4. **Transient-fragility** (HA11-bout-redo's transient-excluded discrimination drops to +11.69 pp): primary INCLUDES transients per parent MD §3.1 r2 absorb; transient-excluded variant is the §4.10 sensitivity arm. Captured in §8 caveat 5.

## Lock arc

Per [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md) 5-stage canonical arc:

| stage | status | venue | output |
|---|---|---|---|
| 1. Draft (§3.2) | DONE 2026-06-23 | producer-mode under authorisation; this folder | THIS COMMIT |
| 2. Audit (§3.4) | pending | fresh session (paste `/research-review docs/research/analyses/hypotheses/HA-C4c/hypothesis.md`) | `docs/research/reviews/HA-C4c-<date>.md` |
| 3. Revise r2 (§3.5) | pending | shared-context with drafting | r2 of `hypothesis.md` |
| 4. Re-audit (§3.6) | pending or compressible | fresh session OR documented compression | `docs/research/reviews/HA-C4c-<date>-v2.md` OR compression note |
| 5. Lock (§3.8) | pending | shared-context | lock-commit + Authorship `Status: LOCKED` + Wiggers C4 register-row pointer added |
| 6. Test execution (§3.9) | pending post-lock | shared-context (test handoff brief) | `test.py` + `result.md` |

## Sister-test context

- **[HA-C4 v2](../HA-C4/)** — the daily-aggregate Wiggers C4 test. REJECTED 2026-06-18 at triad sum 0/3 (commit `52bddb5`); Channel 1's `stress_post_peak_drop_avg` companion SUPPORTED on BOTH eras + Channel 1 + Channel 2 primary SUPPORTED on validate. The within-day signal IS detectable at finer resolution; HA-C4c is the bout-level operationalisation per HA-C4 v2 §9 REJECTED branch.
- **[HA-C4b v3](../HA-C4b/)** — the motion-filter crash-precursor test. NOT-SUPPORTED on the per-episode framing. A SUPPORTED-here-NOT-SUPPORTED-at-HA-C4b shape is consistent with the protective-rather-than-predictive alternative reading from HA-C4b v3 §9 (the pattern exists but isn't a per-episode crash precursor because the participant uses Garmin as a live pacing signal).
- **[HA11-stress-udip](../HA11-stress-udip/)** — the v1 sister whose SUPPORTED-on-train signal (+22.8 pp, median signed z = 2.168) is the U-dip count — the *inverse* of HA-C4c's `did_not_return` operand at bout level. The two operands triangulate the same Wiggers C4 claim from opposite sides at bout resolution.
- **[HA11-bout-redo](../HA11-bout-redo/)** — the framework-validity gate. PARTIAL 2026-06-23 (commit `6e06d12`); bars 1+2 PASS / bar 3 FAIL. Unblocks HA-C4c drafting with explicit calibration caveat per §9.2; HA-C4c §8 caveat 2 carries the calibration discount.

## Cross-references

- Parent methodology MD: [`bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md) (LOCKED `c57ff3f` 2026-06-21).
- Sub-MD (β recalibration): [`bout_level_dose_response_calibration.md`](../../../methodology/bout_level_dose_response_calibration.md) (r4 LOCKED `fb97d1c` 2026-06-23 with §6 inheritance table populated 0/7 CONFIRMED).
- Pipeline that produces `bout_n_did_not_return_day`: [`pipeline/02_features/extract_stress_bouts.py`](../../../pipeline/02_features/extract_stress_bouts.py) + [`pipeline/02_features/README.md`](../../../pipeline/02_features/README.md) (LOCKED `d5b394c` 2026-06-22).
- HA11-bout-redo framework-validity reference: [`HA11-bout-redo/result.md`](../HA11-bout-redo/result.md) (PARTIAL 2026-06-23 `6e06d12`).
- HA-C4 v2 daily-aggregate reference: [`HA-C4/result.md`](../HA-C4/result.md) (REJECTED 2026-06-18 `52bddb5`).
- Wiggers register entry: [`wiggers_testable_hypotheses.md` C4 row](../../../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic) (will be updated at HA-C4c lock per §3.8 gate 3).
- Hypothesis lock process: [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md).
- Drafting handoff brief: `C:/Users/Gebruiker/.claude/plans/session-HA-C4c-pre-reg-drafting-handoff-2026-06-23.md`.
