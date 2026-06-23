# HA-C3 r2 RESULT: HALT (sanity gate failure)

## Authorship

Drafted 2026-06-23 by Claude (Opus 4.7 1M) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default). Authorising user: Willem. Pre-reg r2 LOCKED 2026-06-23 at commit `de22b68`. Test commit: `(this-commit)`. Status: **LANDED**.

**Test-session context**: this `test.py` was implemented and run in a FRESH Claude session per the post-lock discipline of [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). The drafter has now seen the joint distribution; result.md is the first post-lock artefact emitted.

**HALT outcome**: the §7.5 dry-run sanity gates failed at the configuration pre-committed at r2 lock. Per §3.9 dry-run halt discipline + the locked r2 spec, the full test was **NOT** executed beyond the dry-run; verdict is HALT and the §7.3 halt-option resolution is documented below for the v2 redraft.

## §1 What was tested

**Headline cell** (per pre-reg §1 + §5.0): unmedicated (full LC era through 2024-04-08) × full Stratum 4 single pool × `all_day_stress_avg` binned at {B1[0,20), B2[20,30), B3[30,40), B4[40,60), B5[60,100]} × `gevoelscore` bin-mean × {Jonckheere-Terpstra monotone + second-difference convexity contrast S + spline non-linearity} × block-permutation null at E[L]=7 × 3-condition gated verdict per §5.1.

**Wiggers C3 verbatim claim** (PDF lines 1357-1368, Annual Stress Scores section): the stress → fatigue relationship is non-linear / convex — a 30 → 40 stress step costs more gevoelscore than a 20 → 30 step. Tested as the bin-mean trajectory should be **monotone-decreasing** AND **convex** (accelerating decrement at higher stress bins).

**3-condition gated verdict per §5.1**:

| outcome | condition status | verdict |
|---|---|---|
| (a) MET AND (b) MET AND (c) MET | 3-of-3 | **SUPPORTED** |
| Exactly 2-of-3 MET | 2-of-3 | **PARTIAL** |
| ≤1-of-3 MET | 0/1-of-3 | **REJECTED** |
| Any wrong-direction firing | override | **REJECTED** |

## §2 Data + descriptives

Primary unmedicated pool: n = **581**. Stress median: **34.00**. Gevoelscore median: **4.00**.

| bin | label | n | bin-mean gevoelscore | bin-median |
|---|---|---:|---:|---:|
| B1 | B1[0,20) | 0 | NA | NA |
| B2 | B2[20,30) | 95 | 3.958 | 4.00 |
| B3 | B3[30,40) | 385 | 4.265 | 4.00 |
| B4 | B4[40,60) | 100 | 3.860 | 4.00 |
| B5 | B5[60,100] | 1 | 1.000 | 1.00 |

## §3 Primary test result

**HALT**: primary test was not executed because the §7.5 sanity gates failed at the pre-committed bin specification. Per §3.9 dry-run halt discipline + locked r2 §7.5 + §10.4 step 1, no primary statistics were computed.

**Halt-option resolution (for v2 redraft)**:

- **Gate 1 fired on TWO bins**: B1 [0,20) has **n = 0** and B5 [60,100] has **n = 1** (against the §7.5 ≥30 bar). The B5 underpower was forecast at lock per §7.2 ('B5 is the most-at-risk for the < 30 sanity gate'); the B1 underpower (n = 0) was NOT forecast — the descriptive distribution shows `all_day_stress_avg` never falls below 20 on the unmedicated pool (stress median 34, pool n 581).
- **§7.3 halt-option-A pre-committed default**: widen B4 to absorb B5. **This addresses B5 but NOT B1**.
- **B1-handling is OUT OF LOCKED SCOPE**: the locked r2 §7.3 pre-commitment is sole-B5; the B1 zero-population failure mode is not absorbed by either halt-option-A or halt-option-B as documented. Per §3.9 + §10.4 step 3, **any post-dry-run spec revision creates HA-C3-v2 with v1/r2 archived**. The v2 redraft must address the B1 boundary directly (e.g. collapse B1 into B2 to form a `[0, 30)` low-stress bin), preserving the Wiggers-verbatim 30→40 anchor at the B3-B4 boundary.

**Halt detail (machine-readable)**: Sanity gates failed in ways not absorbed by §7.3 halt-option-A: Gate 1 (per-bin n >= 30): bins below threshold: [('B1', 0), ('B5', 1)]; spec 7.3 halt-option-A pre-committed only for sole-B5 failure; other failures require v2 spec redraft.

## §4 Sensitivity arms (descriptive, no verdict weight)

Sensitivity arms not executed because the primary test halted on §7.5 sanity gates. Per §3.9 the v2 redraft re-executes sensitivity arms after the spec is revised.

## §5 Bin-by-bin descriptive characterisation

Per pre-reg §10.3, the bin-by-bin descriptive characterisation is reported even on halt. With B1 (n=0) and B5 (n=1) structurally underpopulated, the **interpretable trajectory is across bins B2 → B3 → B4 only**:

| bin | n | bin-mean gevoelscore | adjacent step (low − this) |
|---|---:|---:|---:|
| B1 | 0 | NA | — |
| B2 | 95 | 3.958 | — |
| B3 | 385 | 4.265 | -0.307 |
| B4 | 100 | 3.860 | +0.405 |
| B5 | 1 | 1.000 | +2.860 |

**Descriptive read (qualifier: 3-bin support only; pre-reg verdict NOT computed)**: across B2 → B3 → B4 the bin-mean trajectory is 3.958 → 4.265 → 3.860 — **non-monotone** at the descriptive level (B3 mean rises above B2 before B4 drops below B2). The pre-reg §7.4 expectation under SUPPORTED is monotone-decreasing B1 → B5; with only B2-B4 visible AND the B2-B3-B4 sub-trajectory non-monotone, the convexity question is moot at the locked 5-bin spec. The B5 (60+) single observation (gevoelscore = 1) is informally consistent with the SUPPORTED-direction tail but cannot be tested (n=1).

*This descriptive read is consistent with pre-reg §7.4 'no monotone relationship at all (e.g. flat or U-shaped) → REJECTED via condition (a) failure' AT THE VISIBLE-BINS LEVEL — but the formal §5.1 verdict is HALT (not REJECTED), because B1's structural absence means the locked 5-bin spec cannot be tested in the form locked.*

## §6 §4.7 E[L]* report (factor-of-2 flag)

Not run (primary halted).

## §7 Caveats (per pre-reg §8)

1. **Power-calc dispatch**: power calculation is **inapplicable per Daza 2018** ([within-subject n-of-1 design](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)). Block-permutation null at E[L]=7 is the within-subject inferential machinery; the 3-condition gated verdict is the decision rule.
2. **n=1 single-subject**: thresholds (p<0.05; S<0; spline 2nd-deriv negative at ≥3 of 4 midpoints) calibrated to the participant's distribution. No cross-subject generalisation claimed.
3. **Citalopram-channel inheritance**: `all_day_stress_avg` is CONFIRMED dose-modulated at +0.57/mg. Primary uses §5.A per-phase stratification (unmedicated headline); §5.B dose-adjusted is cross-phase sensitivity. Reported §4 above.
4. **Crash-day inclusion fragility**: crashes KEPT in primary; crash-drop arm flagged if |Δ S| > 0.10 standardised OR sign-change. Reported §4 above (per CONVENTIONS §3.4).
5. **Within-subject SHAPE, not between-subject prediction**: the convex stress→fatigue claim is about THIS participant's mapping across days; no cross-person generalisation.
6. **No causal-direction inference**: test answers "does the mapping have a convex shape?", not "does stress CAUSE fatigue?".
7. **Wiggers' phrasing is qualitative**: the (0-20, 20-30, 30-40, 40-60, 60+) binning is OUR operationalisation per the verification log; a REJECTED verdict at these specific bins does NOT universally falsify the qualitative "stair-step" framing.
8. **Independent obligations** (per `citalopram_phase_stratification` §6): autocorrelation (§4.7) + crash-drop (§4.6) + spike-companion (N/A; HA-C3 is the cross-day-aggregate test) + trajectory-detrend (N/A; this is not a pre-vs-post comparison).
9. **Test-session context**: this test was executed in a FRESH Claude session per `hypothesis_lock_process.md` §3.9.
10. **Sister-test cross-references**: HA-C4 v2 REJECTED at daily-aggregate (recovery-dynamics triad); HA11 SUPPORTED on train (within-day U-dip count). HA-C3's primary cell (cross-day-aggregate shape) is structurally distinct from both.

## §8 Reproducibility checklist

- **Script**: `docs/research/analyses/hypotheses/HA-C3/test.py`
- **Environment variable**: `GEVOELSCORE_DATA_PATH` (default: `C:\Users\Gebruiker\Documents\gevoelscore-data`)
- **Seed**: `RANDOM_SEED = 20260622`
- **Bootstrap**: B = 10000 stationary-bootstrap draws per condition; E[L] = 7 (geometric block length)
- **Regenerate command**: `python docs/research/analyses/hypotheses/HA-C3/test.py`
- **Dependencies**: numpy, scipy (for `CubicSpline`, `mannwhitneyu`, `spearmanr`, `f.sf`); project utility `docs/research/analyses/_utils/inference.py` for `compute_data_driven_block_length` + `holm_step_down`.
- **Spec commit**: `de22b68` (LOCKED 2026-06-23)
- **Halt artefact**: `dry-run-report.md` co-emitted; `summary.json` contains the per-bin sample sizes + gate-result detail. Full result-data not emitted because the primary did not execute.

---

*test.py run with `RANDOM_SEED = 20260622`, `BOOTSTRAP_E_L = 7`, B = 10000 draws per condition. Source: `per_day_master.csv` from `$GEVOELSCORE_DATA_PATH`. Spec commit: `de22b68`.*
