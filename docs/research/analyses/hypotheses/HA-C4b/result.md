# HA-C4b v2 — Result: stress-with-low-motion minute count as crash precursor (unmedicated pooled headline)

**Headline verdict (unmedicated phase × train+validate POOLED × `stress_low_motion_min_count_S60_Mlow` × N_std=1.5 × primary 4d × one-sided elevated): INCONCLUSIVE**

Single-cell lock per v2 §5.0; no other cell can promote. Data: [result-data.json](result-data.json). Companion: [dry-run-report.md](dry-run-report.md).

## Critical methodological finding — §4.3 1b.ii drops one train episode below the §5.3 bar

The v2 §10.2 spec-sanity-gate at dry-run **passed** with pooled-unmedicated n = 10 (8 train + 2 validate) because the dry-run applied §4.3 1b.i only (the strict in-range stress-sample count gate ≥ 900). Once the full run additionally applied §4.3 1b.ii (the wake-window quartile-coverage gate ≥ 50 samples per quartile, using sleep-window-aware quartile boundaries with fixed-time fallback), **one train episode dropped out**, taking the pooled cell to n = 9 — below the §5.3 inconclusive bar (n ≥ 10).

**The dropped episode is `2023-02-04`** — the unmedicated train arm's highest-z episode. Its 4-day lead-up included `2023-02-03` with `max_signed_z = +3.73` (dry-run printout, before 1b.ii applied). The episode itself or one of its lead-up days failed the §4.3 1b.ii wake-window quartile-coverage check; the full run's `episode_profile` therefore returns insufficient lead-up for this episode and excludes it from the pooled-headline pool.

**Structural reading**: the v2 §10.2 sanity gate is asymmetric with the full run's gate. The dry-run defaults to 1b.i-only for speed (the §4.3 1b.ii quartile-coverage cache takes ~5-15 min to build from FIT files); the full run applies 1b.ii. The spec did not anticipate that a sanity-passing pool could drop below the §5.3 bar between the two gating regimes. This is a v2 spec-design observation; the test still ran per the locked protocol and landed INCONCLUSIVE per v2 §5.3. Per v2 §9 INCONCLUSIVE branch:

> Halt the test; revise via v3 if a recoverable operationalisation change exists, otherwise descriptive companions become the only output. No SUPPORTED claim.

**No SUPPORTED claim is made.** The result below reports the descriptive companions (per §9). A v3 revision is a user decision; candidate paths include (a) requiring the dry-run sanity gate to apply 1b.ii (slow but symmetric with the full run); (b) revisiting whether the §4.3 1b.ii quartile-coverage gate is necessary for the LC-era unmedicated phase at all (the §5 NaN-policy / day-validity gate in `stress_low_motion_primitive.md` only requires the 600-sample gate); (c) accepting the INCONCLUSIVE verdict and reading the descriptive companions as the operational signal. **The choice is the user's; no v3 is auto-triggered.**

**Per-episode visibility caveat**: writing this result.md is a test-session activity, allowed to see per-episode z-scores (the contamination boundary in [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock) is between drafting/locking and running). Surfacing the dropped episode and its z-value here is the honest report of which evidence the locked discipline excluded.

## v1 → v2 relock disclosure (per v2 §8 caveat)

The headline cell was relocked from `consolidation × both-eras` (v1) to `unmedicated × train+validate pooled` (v2) AFTER v1's dry-run halt (2026-06-15). The relock honoured the locked-pre-reg discipline (v1 archived at [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md); v2 drafted in a fresh session per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) with per-episode z-scores held out from the v2 drafting session), but introduces a researcher-degrees-of-freedom concern: the corpus's available cells were known at v2 drafting time (the eligible-n table from v1's dry-run report), and the pooled-unmedicated cell was selected partly because it was the only above-bar cell available on the corpus.

The within-test discipline against this concern: §5.0 single-cell lock + descriptive companion treatment of all other arms (other phases, train-only / validate-only subsets, LOO drops, N_std tiers, secondary 5d, bidirectional). The inferential defence: the stationary-bootstrap null at E[L]=7 from §4.9. The upstream defence for future pre-regs: the `hypothesis_lock_process.md` v1.2 §5 row (structural-completeness + EXACT-column anchor) that v2 closes.

Independent of this concern, **v2's pooled headline is structurally NOT a both-eras finding** in the project's HA-family sense. The HA11/HA06b/HA10 family pattern of independent train + validate verdicts is abandoned for this hypothesis; v2 pools train (n=8) + validate (n=2) within the unmedicated phase to clear the §5.3 n≥10 bar. The compensating mechanism is the descriptive directional-consistency companion on the train-only and validate-only subsets (below). See v2 §8 caveat 2.

## Headline numbers (unmedicated × pooled × `stress_low_motion_min_count_S60_Mlow` × N_std=1.5 × primary 4d × one-sided elevated)

Cell INCONCLUSIVE: n_clean = 9 (pre-§4.5: 9); did not clear v2 §5.3 bar (n ≥ 10).

## Train-only / validate-only descriptive companions (pre-declared INCONCLUSIVE per v2 §5.3; reported for directional consistency only)

| subset | n_clean | (a) rate | median max_signed_z |
|---|---:|---:|---:|
| train-only unmedicated | 7 | 42.9% | +1.41 |
| validate-only unmedicated | 2 | 0.0% | -0.43 |

### Validate-only unmedicated per-episode (n = 2)

| episode date | max_signed_z | max|z| | triggered (one-sided ≥1.5) |
|---|---:|---:|---|
| 2024-01-12 | -1.08 | 1.62 | no |
| 2024-02-15 | +0.21 | 1.47 | no |

## Episode-level leave-one-out (LOO) fragility check (§4.11.5)

Skipped — headline cell was INCONCLUSIVE.

## Companion-phase descriptive cells (pre-declared INCONCLUSIVE per v2 §5.3)

Phases other than unmedicated have train arms empty by phase-boundary construction (train ends 2023-12-31; consolidation/buildup/afbouw start ≥ 2024-04-09). Only validate arms are reported; none promotes to SUPPORTED.

| phase × era | n_pre_§4.5 | n_clean | (a) rate | median max_signed_z |
|---|---:|---:|---:|---:|
| consolidation × validate | 5 | 2 | 50.0% | +1.48 |
| buildup × validate | 2 | 0 | — | — |
| afbouw × validate | 2 | 0 | — | — |

## Sensitivity ladder (unmedicated × pooled × 6 unique cols × 3 N_std tiers × primary 4d × one-sided)

Per v2 §4.10 + stress_low_motion_primitive §3.2: 6 unique columns + 3 identical-by-construction duplicates (`Mbelow_mod` ≡ `Mlow` at same S threshold; duplicates emitted to result-data.json but not tabulated here). Threshold-monotonicity check: at the same motion class, S=50 ≥ S=60 ≥ S=75 in firing rate (per primitive §8.3). Verdicts diagnostic only; none promotes to SUPPORTED per §5.0.

| col | N_std=1.5 | N_std=2.0 | N_std=2.5 |
|---|---|---|---|
| S50_Mstrict | INCONC (n=9) | INCONC (n=9) | INCONC (n=9) |
| S50_Mlow | INCONC (n=9) | INCONC (n=9) | INCONC (n=9) |
| S60_Mstrict | INCONC (n=9) | INCONC (n=9) | INCONC (n=9) |
| S60_Mlow | INCONC (n=9) | INCONC (n=9) | INCONC (n=9) |
| S75_Mstrict | INCONC (n=9) | INCONC (n=9) | INCONC (n=9) |
| S75_Mlow | INCONC (n=9) | INCONC (n=9) | INCONC (n=9) |

## Headline cell sensitivity arms (transparency only, no SUPPORTED promotion)

| arm | n_clean | verdict | (a) | disc_pp | med_z |
|---|---:|---|---:|---:|---:|
| 4d_primary_bidirectional | 9 | inconclusive | 66.7% | — | — |
| 5d_secondary_one_sided_elevated | 9 | inconclusive | 33.3% | — | — |
| 5d_secondary_bidirectional | 9 | inconclusive | 77.8% | — | — |

## E[L]* data-driven block length (unmedicated pool)

- E[L]* = 3.30; default E[L] = 7; factor-of-2 flag: YES — verdict requires re-evaluation at E[L]*.

## §4.11 secondary descriptive outcomes

### Same-day Spearman (PRIMARY_COL vs gevoelscore) with §3.4 crash-drop sensitivity

| phase | era | n_full | ρ_full | n_no_crash | ρ_no_crash | |Δρ| |
|---|---|---:|---:|---:|---:|---:|
| unmedicated | train | 460 | -0.027 | 399 | +0.071 | 0.098 |
| unmedicated | validate | 92 | +0.098 | 79 | +0.023 | 0.075 |
| buildup | train | 0 | — | 0 | — | — |
| buildup | validate | 64 | +0.118 | 58 | +0.115 | 0.003 |
| consolidation | train | 0 | — | 0 | — | — |
| consolidation | validate | 605 | +0.026 | 591 | +0.029 | 0.004 |
| afbouw | train | 0 | — | 0 | — | — |
| afbouw | validate | 72 | +0.210 | 68 | +0.194 | 0.016 |

### v2 Spearman on pooled-unmedicated heavy-exertion-conditioned subset (headline cell's universe)

- n = 340, ρ = +0.070

### Construct-disambiguation 2×2 (HA-C4b primary vs sibling)

**vs `stress_high_duration_min`** (ρ = 0.79):

| phase | era | both_fire | primary_only (HA-C4b only) | sibling_only | neither | n_eval |
|---|---|---:|---:|---:|---:|---:|
| unmedicated | train | 3 | 0 | 1 | 3 | 7 |
| unmedicated | validate | 0 | 0 | 0 | 2 | 2 |
| buildup | validate | 0 | 0 | 0 | 0 | 0 |
| consolidation | validate | 0 | 1 | 0 | 1 | 2 |
| afbouw | validate | 0 | 0 | 0 | 0 | 0 |

**vs `u_dip_count`** (ρ = 0.556):

| phase | era | both_fire | primary_only (HA-C4b only) | sibling_only | neither | n_eval |
|---|---|---:|---:|---:|---:|---:|
| unmedicated | train | 0 | 0 | 0 | 0 | 0 |
| unmedicated | validate | 0 | 0 | 0 | 0 | 0 |
| buildup | validate | 0 | 0 | 0 | 0 | 0 |
| consolidation | validate | 0 | 0 | 0 | 0 | 0 |
| afbouw | validate | 0 | 0 | 0 | 0 | 0 |

### Respiration-companion sensitivity (§4.11.4)

Among crash episodes where HA-C4b primary fires (one-sided ≥1.5), did `n_minutes_resp_above_18` also show z > 0 in the lead-up?

| phase | era | primary_fired_resp_elev | primary_fired_resp_normal |
|---|---|---:|---:|
| unmedicated | train | 3 | 0 |
| unmedicated | validate | 0 | 0 |
| buildup | validate | 0 | 0 |
| consolidation | validate | 1 | 0 |
| afbouw | validate | 0 | 0 |

## Caveats (v2 §8 acknowledged)

- **v1 → v2 relock disclosure**. The headline cell was relocked from `consolidation × both-eras` (v1) to `unmedicated × train+validate pooled` (v2) after v1's dry-run halt; researcher-degrees-of-freedom concern from the relock is acknowledged (the corpus's available cells were known at v2 drafting time, and the pooled-unmedicated cell was selected partly because it was the only above-bar cell available). Surfaced in the introduction block above.
- **No cross-era independent replication for v2's headline cell**. v2 pools train (n=8) + validate (n=2) within unmedicated to clear the n ≥ 10 bar; the HA11-family both-eras-independent rule is abandoned for this hypothesis. The compensating mechanism is the descriptive directional-consistency companion on the train-only (n=8) and validate-only (n=2) subsets reported above. **Not a full substitute** for independent verdicts.
- **Power-calc dispatch**. Power calculation is inapplicable per Daza 2018 within-subject design — the n-of-1 corpus does not have separate treatment and control arms in the sense classical power calculations require. The block-permutation null at E[L]=7 (§4.9) is the within-subject inferential machinery; the §5.1 (a)+(b)+(c) gates determine SUPPORTED / NOT-SUPPORTED rather than a power-thresholded p-value.
- **Unmedicated = pre-citalopram corpus, not 'no medication overall'**. The participant was unmedicated for SSRI in 2022-04 → 2024-04 but had other lived-experience interventions in that window (CPAP started 2024-01-10 — the last ~3 months of unmedicated; daily pacing protocols evolved; PEM-pacing practice was being established). The unmedicated headline is 'no SSRI' not 'no intervention'. §4.2 exertion-conditioning and §4.5 phase-stratified baseline absorb most of this, but it is residual context.
- **Garmin stress is partly motion-sensitive**; the motion filter and respiration-companion sensitivity above are the within-test checks.
- **Garmin `intensity` classification has an 81% gap**; minutes without an explicit intensity record default to 'low motion' (generous; per stress_low_motion_primitive §3.3a).
- **Citalopram dose-modulates the underlying stress channel** (per `citalopram_dose_response_stress_mean_sleep.md §5.6` multi-channel confirmation: 30 mg plasma suppresses raw stress by ~12-17 points). Per-phase treatment is the dose-confound control; raw count magnitudes not directly comparable across phases. v2's unmedicated phase headline is the cleanest test ground precisely because the suppression cascade is absent.
- **The `below_moderate` motion class is identical-by-construction to `low_or_below`** in this corpus; the 9-column ladder effectively reduces to 6 unique columns.
- **Exertion-conditioning shrinks n** sharply; per-phase verdicts outside unmedicated × pooled may be inconclusive on low-n phases (reflected in the consolidation / buildup / afbouw companion table above).
- **Construct ρ vs `stress_high_duration_min` = 0.79** — close sibling; the construct-disambiguation 2×2 above is the empirical test of whether the motion filter does analytical work.
- **The participant is operationally using the rest-stress trigger** (per `garmin_pacing_practice.md §3.3`); the protocol disturbs the test. NOT-SUPPORTED reads may indicate a PROTECTIVE-rather-than-PREDICTIVE trigger; SUPPORTED reads survive despite the disturbance.
- **`crash_v2` mixes mechanisms**; multi-mechanism crash population dilutes any one-mechanism precursor signal.
- **Multi-comparison defence**: the §5.0 single-cell discipline + the stationary-bootstrap null at E[L]=7 are the inferential machinery; descriptive companions never promote per §5.2.
- **The bootstrap RD/OR CIs are computed against the stationary-bootstrap null distribution** (varying p_null with fixed observed p_crash); this captures null-side variability only. A fuller joint-bootstrap CI would require resampling crash episodes as well; deferred (inherited from v1 §8).
- **§4.11.5 LOO boundary-fragility**: an empty load-bearing list is NOT 'no fragility detected' — it is a boundary-distance signal indicating k is not exactly at the 60% gate boundary. Restated in the LOO section above.

