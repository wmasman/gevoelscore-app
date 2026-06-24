# Single-pool re-anchor cross-check (R14, Shared gap 2)

**Strand A operationalisation-support analysis** — Strand-A methodology-execution variant per [`descriptive/README.md`](../../README.md) §3 + §6.1. Executes the **binding recipe** from [`methodology/train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) §5.7 (descriptive cross-check; locked verdicts UNCHANGED).

## Authorship

- **Drafted**: 2026-06-24 by Claude (Opus 4.7), producer-mode under user authorisation per [CONVENTIONS §1.1](../../../../CONVENTIONS.md#11-producer-mode-claude-drafts--edits-under-user-authorization).
- **Authorising user**: user.
- **Dispatching artefact**: [`session-R14-single-pool-reanchor-handoff-2026-06-24.md`](file:///C:/Users/Gebruiker/.claude/plans/session-R14-single-pool-reanchor-handoff-2026-06-24.md).
- **Mode**: descriptive cross-check, not re-lock; locked HA verdict files (`result.md`) UNCHANGED per [`train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) §5.7 bullets 6-8.

## Research question

For each historical HA pre-reg locked under the 2023-12-31 train/validate split, **is the primary single-pool verdict robust to era partition?** I.e. when the same operand is evaluated on the full Stratum 4 single pool (per the new MD2 + MD3 framework), does the verdict converge with or diverge from the locked split-era verdict?

This is **NOT** "does the effect change over time?" — the single-subject observational design cannot answer that. Per [`train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) §5.7 bullet 8 ("number, not narrative"): train-vs-validate divergence is reported as a descriptive number, not interpreted as evidence for any specific generative story.

## Programme placement

Closes **Shared gap 2** from the [`methodology/_descriptive_stocktake_2026-06-23.md`](../../../../methodology/_descriptive_stocktake_2026-06-23.md) §3 enumeration: the assumption-cell A8 "single-pool primary preserved per `train_validate_split_fate.md`" was NOT BACKSTOPPED for 16 HAs in the older H/HA01-11 family. Closing this descriptive cell (closing it on at least N of those 16 HAs) potentially unlocks those HAs' eligibility for Stage D TRUSTED in the [`methodology/synthesis_structure_map.md`](../../../../methodology/synthesis_structure_map.md) (LOCKED r2 2026-06-23) — pending user-owned review per [`train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) §5.7 bullet 7.

## Method

For each in-scope HA:

1. **Read its `hypothesis.md`** — extract the operand definition + the locked operationalisation (window, baseline, threshold, exclusions). The cross-check honours the hypothesis's own operand definitions without re-engineering them.
2. **Read its `result.md`** — extract the locked verdict + the per-era headline numbers (per-era n, discrimination pp, effect-size).
3. **Re-load the operand** from `per_day_master.csv` at the **full Stratum 4 single pool** (2022-09-03 → 2026-06-05; standard Stratum 4 day-validity gates per [`lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md)). For HAs whose operand requires per-minute data not in per_day_master (HA11), the per-day proxy column already aggregated into the master is used; this is documented per-HA in the findings.
4. **Re-run the discrimination** at single-pool:
   - Compute the same operand the locked HA used.
   - Compute crash-vs-normal day-level or window-level comparison (matching the HA's locked unit; per-day vs per-window vs per-episode).
   - Apply block-permutation null at **E[L]=7, B=10000, seed `20260624`** per [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) (project default).
   - Compute **stationary bootstrap 95% CI** on the discrimination statistic.
5. **Record verdict under single-pool**: SUPPORTED / NOT-SUPPORTED / INCONCLUSIVE per the HA's own §5 verdict rule, evaluated on single-pool numbers only. Locked verdict files are NOT modified per §5.7 bullet 6.
6. **Compare to locked verdict** + **flag divergence** + **name plausible drivers descriptively** per §5.7 bullet 7 examples (block scheme / single-pool vs split / multiplicity threshold / finite-sample variability / direction-reversal cancellation).

Shared inference helpers from [`analyses/_utils/inference.py`](../../../_utils/inference.py) are reused; no duplication.

## Scope

**Primary scope (6 HAs)** per handoff §2.3 + stocktake §5:
- **HA01b-recomputed** (lagged-baseline corrected exertion shock; canonical example per §5.7 bullet 8 footnote)
- **HA07c** (sleep stress mean delta; largest era-divergence in the SUPPORTED-on-train family)
- **HA07d** (sleep stress variability; only canonical both-eras-SUPPORTED test)
- **HA08c** (sleep stress slope)
- **HA10** (BB overnight recharge; only DIRECTIONALITY-REVERSAL test)
- **HA11** (within-day stress U-dip count)

**Stretch scope (effort-permitting)** — additional HAs from the stretch list:
- **H01** (RHR drift; refuted both eras)
- **H02b** (stress spikes; train SUPPORTED / overall refuted)
- **H04** (body battery; refuted both eras)
- **HA06b** (RHR z-score; train SUPPORTED / overall refuted)
- **HA01c** (effective-exertion-shock; SUPPORTED both eras AT locked τ=0.75; WITHHELD)

Deferred / out-of-scope per stocktake §9: H03b (RETIRED), H05 (RETIRED), HA07/HA08 (SUPERSEDED-by-proxy), S02b (SHELVED-BLOCKED-BY-S02), H02 (SUPERSEDED by H02b), H02d (SUPERSEDED-by-equivalence-to-H02b), HA06 (SUPERSEDED by HA06b), K01/K02 (cross-era contrast — split IS the predictor).

See `findings.md` §5 for the per-HA deferred-with-reason list.

## Outputs

- `findings.md` — the writeup: §1 headline; §2 side-by-side table; §3 per-HA narrative; §4 aggregate summary; §5 deferred; §6 synthesis-map implications; §7 caveats; §8 verification log.
- `result-data.json` — machine-readable per-HA single-pool numbers (gitignored per `docs/research/**/*.json` rule).
- `run.py` — the script that produces both.

## Hard constraints (binding per handoff §3 + §5.7 bullets 6-8)

- Locked HA result.md files are NOT modified.
- methodology MDs are NOT modified.
- `per_day_master.csv` is NOT modified.
- No framework is pre-committed as "correct" — the cross-check reports divergence; user decides.
- Single-pool verdicts are NOT promoted to SUPPORTED on their own — they are descriptive cross-check overlays.
- The HA01b legacy +17.3 pp validate divergence is NOT anchored on per §5.7 bullet 8 (v3.1 rolling-baseline artefact; the recomputed lagged-baseline version is canonical).
- Train-vs-validate divergence is reported as a **number, not a narrative** per §5.7 bullet 8.

## Status

- **Cross-check executed**: 2026-06-24.
- **Findings written**: `findings.md`.
- **Locked verdict files**: UNCHANGED per §5.7 bullet 6.
- **User-owned decisions on any follow-up**: a separate session per §5.7 bullet 7.

## Cross-references

- Binding recipe: [`methodology/train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) §5.7
- Discipline binding on framing: [`methodology/train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) §5.8
- Block-length policy: [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md)
- Stratum 4 definition: [`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md)
- Programme stocktake (Shared gap 2 origin): [`methodology/_descriptive_stocktake_2026-06-23.md`](../../../../methodology/_descriptive_stocktake_2026-06-23.md) §3 + §5
- HA registry (locked-verdict cross-references): [`REJECTED.md`](../../../../REJECTED.md) + [`analyses/hypotheses/registry.md`](../../../hypotheses/registry.md)
- Discipline binding on findings.md: [CONVENTIONS](../../../../CONVENTIONS.md) §2.1, §3.4, §4.1, §4.2
- Folder shape precedent: [`analyses/descriptive/operationalisation_support/stress_mean_sleep/`](../stress_mean_sleep/)
