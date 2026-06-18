# HA-C4 v2 dry-run report — sanity gates 1 + 3 PASS (gate 2: 1 cell(s) routed to INCONCLUSIVE per spec 5.4)

Emitted by `test.py --dry-run` per locked v2 hypothesis.md §10.4. Headline cell: unmedicated × {Ch1, Ch2, Ch3} × heavy-T-vs-non-heavy-T × Mann-Whitney U + Cliff's δ × block-permutation null E[L]=7 × v2 INCONCLUSIVE-aware verdict bands per §5.3. Day-validity per §4.3 (LC era + unmedicated + not April-2024 cluster + non-empty exertion classification + channel-value handling per §4.5/§4.6/§4.7).

**v2 disposition of sub-30 cells**: per locked v2 §5.4 + §5.3, any channel × era cell with n < 30 per arm routes to INCONCLUSIVE at the per-channel aggregation layer (CONFIRMED-PARTIAL if the other era is SUPPORTED, else REFUTED). Sub-30 cells DO NOT halt the test. Only distribution-sanity gates 1 + 3 halt on failure.

## §7.5 gate 2: cells routed to INCONCLUSIVE (descriptive, not halt)

- Ch3 validate: heavy n=25, non-heavy n=58 (MIN_ARM_N=30) -> INCONCLUSIVE per spec 5.4

## §7.5 gate 1: full-pool median (±30% of §7.1 reference)

All four anchors computed from `per_day_master.csv` on the `2022-04-04 ≤ date ≤ 2024-04-08` unmedicated filter (see hypothesis.md §7.1).

| channel | full-pool median | §7.1 ref | tol [±30%] | n_used | n_total | gate |
|---|---:|---:|---|---:|---:|---|
| Ch1 | 81.00 | 81.0 | [56.70, 105.30] | 603 | 736 | PASS |
| Ch1_drop_avg | 61.00 | 61.0 | [42.70, 79.30] | 717 | 736 | PASS |
| Ch2 | 73.00 | 73.0 | [51.10, 94.90] | 724 | 736 | PASS |
| Ch3 | 46.00 | 46.0 | [32.20, 59.80] | 724 | 736 | PASS |

## §7.5 gate 2 (v2 routing): per-channel × per-era arm sizes

Per v2 §5.4 + §5.3, cells with n < 30 per arm route to INCONCLUSIVE (NOT halt). v2 §7.3 anchors (chain-T+1-corrected): Ch1/Ch2 train n=171, validate n=41; Ch3 train n=117 (171 − 54 chain-dropped), Ch3 validate n=25 (41 − 16 chain-dropped). Non-heavy-T arms: train n=361, validate n=58.

| channel | era | n_heavy | n_non_heavy | n_total | gate routing |
|---|---|---:|---:|---:|---|
| Ch1 | train | 171 | 314 | 485 | PASS |
| Ch1 | validate | 41 | 58 | 99 | PASS |
| Ch2 | train | 171 | 311 | 482 | PASS |
| Ch2 | validate | 41 | 58 | 99 | PASS |
| Ch3 | train | 117 | 311 | 428 | PASS |
| Ch3 | validate | 25 | 58 | 83 | INCONCLUSIVE (per §5.4) |

## §4.11.3 chain-relaxed Ch3 validate sensitivity cell (v2 NEW)

Per v2 §4.11.3, descriptive sensitivity arm computing the Ch3 validate cell with the §4.7 chain-T+1 exclusion **relaxed for the heavy-T arm only**. Non-heavy-T arm is byte-identical to the Ch3 primary validate cell (the §4.7 chain rule was always heavy-T-only by construction). Descriptive only; does NOT modify the §5.3 verdict per §4.11.3.

- Ch3_chain_relaxed validate: n_heavy=40, n_non_heavy=58 (expected per §7.3 anchors: n_heavy=41, n_non_heavy=58).

## §7.5 gate 3: Ch1 full-pool NaN fraction (per §4.5 + §7.5)

- Observed Ch1 NaN fraction (unmedicated only): **0.1807** (133/736).
- §7.5 sanity range: [0.12, 0.25].
- Semantically per [DATA_DICTIONARY §C4](../../../DATA_DICTIONARY.md#c4--stress-decay-after-daily-peak-4-columns): NaN = 'stress never returned to rest that day' (C4-positive case). The §4.5 1080-min encoding applies in the channel-arm test.

## Next step (PASS branch)

Sanity gates 1 + 3 passed; the full test runs after the dry-run inside the same `python test.py` invocation, emitting `result.md` + `result-data.json`. Per §10.4 step 3: **no iteration on the spec after the dry-run passes** — any post-dry-run revision creates HA-C4-v3.

