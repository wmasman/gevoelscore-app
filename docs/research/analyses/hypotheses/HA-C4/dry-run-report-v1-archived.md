# HA-C4 v1 dry-run report — SANITY-GATE FAILURE (HALT)

Emitted by `test.py --dry-run` per locked v1 hypothesis.md §10.4. Headline cell: unmedicated × {Ch1, Ch2, Ch3} × heavy-T-vs-non-heavy-T × Mann-Whitney U + Cliff's δ × block-permutation null E[L]=7 × pass-2-of-3 verdict rule applied within each era. Day-validity per §4.3 (LC era + unmedicated + not April-2024 cluster + non-empty exertion classification + channel-value handling per §4.5/§4.6/§4.7).

## §7.5 sanity-gate failures (1)

- **Channel 3 validate: heavy-T n = 25 < 30** (non-heavy-T n = 58 ✓; per §5.4 both arms must be ≥ 30).

Per v1 §9.5 + §10.4 step 1 + the locked-pre-reg discipline ([`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock)), the full test is NOT run and `result.md` is NOT emitted. The spec must be revised before any further test run; the revision creates HA-C4-v2 with v1 archived as v1.

## Failure analysis

The Channel 3 validate-arm shortfall is **driven by the §4.7 chain-T+1 exclusion** (heavy-T days dropped when T+1 is also heavy):

| Channel 3 validate decomposition | count |
|---|---:|
| Base heavy-T days in validate (matches §7.3 anchor) | 41 |
| − dropped by §4.7 chain-T+1 exclusion (T+1 also heavy) | −16 |
| − dropped: T+1 outside unmedicated phase / in April cluster | 0 |
| − dropped: T+1 has NaN `awake_stress_avg` | 0 |
| **Ch3 validate heavy-T arm size (post-exclusion)** | **25** |

For Channel 3 train: 171 → 54 chain-dropped → 117 (passes ≥ 30 with margin).

The shortfall is real and audit-traceable; it is not a code bug.

## §7.3 anchor arithmetic discrepancy (audit-able spec finding, surfaced by dry-run)

The §7.3 sample-size table in the locked spec asserts:

> | train (2022-09-03 → 2023-12-31, unmedicated) | **206** | 361 |
> | validate (2024-01-01 → 2024-04-08, unmedicated) | 41 | 58 |
> All per-channel × per-era cells comfortably clear the ≥ 30 inconclusive bar. The validate arm is the tightest (heavy-T n = 41) but still above the bar with margin.

The dry-run computes train heavy-T n = **171** (not 206). The 35-day gap is the unmedicated period 2022-04-04 → 2022-09-02 that is in the unmedicated phase but BEFORE the train-era start of 2022-09-03. 206 = 247 (total unmedicated heavy from §7.2) − 41 (validate heavy) was the spec's implicit arithmetic; it overlooked the April-August 2022 buffer (35 heavy-T days). Per-month verification:

- **Apr–Aug 2022 (pre-train buffer)**: 35 heavy-T days (Jun=7, Jul=16, Aug=12)
- **Sep 2022 – Dec 2023 (train era)**: 171 heavy-T days
- **Jan – Apr 2024 (validate era)**: 41 heavy-T days
- **Total**: 35 + 171 + 41 = 247 ✓ (matches §7.2)

The §7.3 train anchor for Ch1/Ch2 is therefore mis-stated by 35 days, AND the §7.3 table does NOT apply the §4.7 chain-T+1 exclusion that Channel 3 specifically requires (the table caption says "comfortably clear" but it was computed pre-chain). Both are audit-traceable spec errors that a v2 rebuild should fix.

**None of this changes the §7.5 sanity-gate verdict** — the gate is "≥ 30 per arm per channel per era after §4.3 + §4.6 + §4.7 exclusions", and Ch3 validate heavy = 25 is the binding failure. Ch1 train (171) and Ch2 train (171) both still pass ≥ 30 with margin, and the full-pool median + Ch1 NaN-fraction gates all PASS exactly on the §7.1 anchors.

## Recommendation for HA-C4-v2

Per the locked-pre-reg discipline, the v2 author chooses among (at least) the following dispositions for the Channel 3 validate INCONCLUSIVE result. The dry-run does NOT force a specific option — the v2 author owns the choice via a fresh-session draft per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc):

**Option A — accept Ch3 validate as INCONCLUSIVE, restate verdict bar accordingly**: per §5.4, INCONCLUSIVE channels do not count toward the triad. The triad effectively reduces in validate to Ch1 + Ch2. The §5.3 verdict rule needs explicit handling for "Ch3 inconclusive in validate while train Ch3 confirmation is possible" — e.g. Ch3 contributes a maximum of 0.5 (train only). v2 §5.3 + §5.4 wording adjustment; no architectural change. This is the most conservative option (no spec-machinery change beyond an explicit § handling rewrite for partial-inconclusive channels).

**Option B — extend the validate window to recover sample size**: per §6 the unmedicated phase ends 2024-04-08; extending is not possible without crossing into the buildup phase (which would re-introduce the citalopram-dose-modulation confound per §4.4). Likely not viable.

**Option C — relax the §4.7 chain-T+1 exclusion for the validate arm only**: drop the chain-T+1 filter for Ch3 (or make it a sensitivity arm only). Per §4.7, the chained-regime adjustment cleans the "day AFTER overdoing it" comparison; relaxing it for validate would re-mix heavy-T-into-heavy-T+1 sequences. Discipline trade-off; v2 author judgement.

**Option D — drop Channel 3 from the v2 triad entirely**: collapse to a 2-channel test (Ch1 + Ch2). The §5.3 pass-2-of-3 rule becomes pass-2-of-2 (requires both channels in both eras for SUPPORTED). This is the most aggressive structural change; should be considered only if Ch3 validate is also INCONCLUSIVE under all sensitivity-relaxations.

**Option E — restate the §7.3 anchor with chain-T+1 exclusion + buffer-corrected counts, lower the §7.5 minimum to a justified ≥ 20 or use a §5.4-style INCONCLUSIVE-aware triad**: the cleanest discipline option — admit the spec error, rebuild §7.3 honestly (Ch3 train n=117, validate n=25 after chain), and choose the inconclusive disposition in §5.4. The new threshold needs power-justification (a |Cliff's δ| of +0.20 detectable at α=0.05 needs roughly 25–30 per arm in a Mann-Whitney; n=25 sits at the edge).

The v2 author should ALSO close the §7.3 arithmetic bug (train Ch1/Ch2 heavy = 171, not 206) regardless of which Ch3 disposition is taken. The §7.5 ±30% tolerance gates still PASS on §7.1 anchors; only the §7.3 sample-size table was mis-computed.

## §7.5 gate 1: full-pool median (±30% of §7.1 reference)

All four anchors computed at r2 from `per_day_master.csv` on the `2022-04-04 ≤ date ≤ 2024-04-08` unmedicated filter (see hypothesis.md §7.1).

| channel | full-pool median | §7.1 ref | tol [±30%] | n_used | n_total | gate |
|---|---:|---:|---|---:|---:|---|
| Ch1 | 81.00 | 81.0 | [56.70, 105.30] | 603 | 736 | PASS |
| Ch1_drop_avg | 61.00 | 61.0 | [42.70, 79.30] | 717 | 736 | PASS |
| Ch2 | 73.00 | 73.0 | [51.10, 94.90] | 724 | 736 | PASS |
| Ch3 | 46.00 | 46.0 | [32.20, 59.80] | 724 | 736 | PASS |

## §7.5 gate 2: per-channel × per-era arm sizes (≥30 each arm)

| channel | era | n_heavy | n_non_heavy | n_total | gate |
|---|---|---:|---:|---:|---|
| Ch1 | train | 171 | 314 | 485 | PASS |
| Ch1 | validate | 41 | 58 | 99 | PASS |
| Ch2 | train | 171 | 311 | 482 | PASS |
| Ch2 | validate | 41 | 58 | 99 | PASS |
| Ch3 | train | 117 | 311 | 428 | PASS |
| Ch3 | validate | 25 | 58 | 83 | FAIL |

## §7.5 gate 3: Ch1 full-pool NaN fraction (per §4.5 + §7.5)

- Observed Ch1 NaN fraction (unmedicated only): **0.1807** (133/736).
- §7.5 sanity range: [0.12, 0.25].
- Semantically per [DATA_DICTIONARY §C4](../../../DATA_DICTIONARY.md#c4--stress-decay-after-daily-peak-4-columns): NaN = 'stress never returned to rest that day' (C4-positive case). The §4.5 1080-min encoding applies in the channel-arm test.

## Next step (HALT branch)

Per the locked-pre-reg discipline (`hypothesis.md` v1 §10.4 + §9.5), the spec must be revised before any further test run; the revision creates HA-C4-v2 with v1 archived. Fresh-session v2-draft per `hypothesis_lock_process.md` §3.2.

