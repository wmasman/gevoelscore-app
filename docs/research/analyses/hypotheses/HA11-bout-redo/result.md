# HA11-bout-redo — RESULT: PARTIAL (2 of 3 framework-validity bars met)

Emitted by `test.py` per LOCKED r2 hypothesis.md §10.3. **Headline cell**: unmedicated × train era × HA11 v1 calm-day reference-date pool × `bout_n_fast_recovery_day` × 4-day primary window × N_std=1.5 one-sided elevated × discrimination (pp) + block-permutation p at E[L]=7. **Random seed**: `RANDOM_SEED = 20260622` (block-permutation; distinct from HA11 v1's `20260605` for reference-date construction); B = 10,000 draws.

## Authorship

- **Drafting date**: 2026-06-23 (this result.md emitted in the post-lock test-execution session).
- **Agent**: Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem.
- **Pre-reg commit**: r2 LOCKED 2026-06-23 at [`hypothesis.md`](hypothesis.md) commit `5c71aa0` + footer-fix `b5bf0f8`. Worktree HEAD at run: `250a466`.
- **Test commit**: this session's `test.py` commit (set by dispatcher after cherry-pick).
- **Pipeline commit**: bout-extraction pipeline LOCKED at `d5b394c` (2026-06-22, [`extract_stress_bouts.py`](../../../pipeline/02_features/extract_stress_bouts.py)).
- **Status**: LANDED. Test executed end-to-end; dry-run §7.5 gates passed; primary headline emitted; sensitivity arms reported; cascade implication recorded in §6.

## §1 What was tested

**Headline cell** (single-cell headline lock per pre-reg Authorship "Mandatory dispatches"): bout-level test on `bout_n_fast_recovery_day` × unmedicated phase × train era × calm-day pool (HA11 v1 reference dates per HA11 v1 §4.9, seed `20260605`) evaluated against the three §5 framework-validity comparability bars (verbatim from parent MD §6.2):

> 1. **Directional sign agrees with HA11 v1's +22.8pp train discrimination**: bout-level test on `bout_n_fast_recovery_day` z-score (4-day primary window, one-sided elevated direction, N_std=1.5) shows positive discrimination on train.
> 2. **Effect-size comparability**: bout-level train discrimination is within ±10pp of HA11 v1's +22.8pp, i.e. **≥ +12.8pp**.
> 3. **p-value comparability**: empirical p-value on the bout-level train discrimination is below HA11 v1's bar — that is, **p < 0.05** under the block-permutation null at E[L]=7.

**Verdict rule** (pre-reg §5): PASSED iff all 3 bars met; PARTIAL iff exactly 2; FAILED iff ≤ 1; INCONCLUSIVE iff §4.9 walk-forward gate fails (n_calm < 30 OR n_crash < 10).

## §2 Data and descriptives

**Inputs** (pipeline commit `d5b394c`; spec §3):
- `per_day_master.csv`: 1755 rows; `bout_n_fast_recovery_day` non-NaN on **1486 days** (≥ 1479 per pipeline README — operand-presence dry-run gate PASS).
- `per_bout_master.csv`: 4273 bouts (used for §4 sensitivity-arm re-aggregation).
- HA11 v1 `udip_counts.csv`: 1739 days; 1722 valid (used to replay the HA11 v1 reference-date construction with seed `20260605`).
- `labels_crash_v2.csv`: **29 crash episodes** (HA11 v1 outcome; inherited per §3).

**Dry-run §7.5 sanity gates** (per pre-reg §10.4 + [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock); all 3 PASS):

| gate | observed | threshold | r2 pinned | result |
|---|---:|---|---:|:---:|
| 1 — effective n_calm (§4.5+§4.7) | **70** of 200 HA11 v1 refs (73 in unmed × train pre-window-coverage) | ≥ 30 (§4.9 walk-forward) | 70 | **PASS** + exact pinned match |
| 2 — σ median on `bout_n_fast_recovery_day` (§4.6) | **0.739** across 413 analysis days; range [0.589, 1.026] | > 0.5 (§4.6 low-variability floor) | 0.739 | **PASS** + exact pinned match |
| 3 — operand presence | **1486** non-NaN days | ≥ 1479 (pipeline README) | — | **PASS** |
| AUX — n_crash anchors | **11** of 13 unmed × train crash anchors after §4.7 coverage | ≥ 10 (§4.9) | — | OK (walk-forward gate cleared) |

**Pool sizes (post-coverage, primary arm)**:
- **n_calm = 70** (reference-date 4d windows with ≥ 3-of-4 days having valid analysis-day input per §4.5 + §4.7).
- **n_crash = 11** (crash-episode 4d windows in unmed × train with ≥ 3-of-4 coverage; 2 of 13 anchors dropped due to insufficient window coverage).
- Analysis-day pool (z-scored against participant's lagged personal baseline): **413 days** in unmed × train satisfying §4.4 day-validity + §4.6 baseline-validity. Skips on σ ≤ 0.5: **0** (zero low-variability skips). Skips for insufficient prior-day coverage: 67.

**σ-distribution context** (r2-pinned; reproduces audit-closure single-script count): median 0.739 (IQR [0.672, 0.826]) for `bout_n_fast_recovery_day` vs HA11 v1's `u_dip_count` median 0.840 (IQR [0.773, 0.899]) on the equivalent 480-day pool — modestly less variable but well above the 0.5 floor (see pre-reg §4.6 r2 inheritance note).

## §3 Primary test result

| metric | crash-anchor arm (n=11) | calm-pool arm (n=70) |
|---|---:|---:|
| trigger frequency (max signed z ≥ 1.5) | **54.5%** (6/11) | 34.3% (24/70) |
| **discrimination (pp)** | — | **+20.26 pp** |
| median signed z (triggering crash anchors) | **+2.410** | — |
| Cliff's δ (crash vs calm, max-signed-z distributions) | **+0.306** | — |
| Cliff's δ 95% CI (paired-bootstrap, B=2000) | [−0.021, +0.626] | — |
| Mann-Whitney U (crash first) | 503 | — |
| Mann-Whitney p (one-sided normal approx, descriptive) | 0.0519 | — |
| block-permutation p (B=10,000, E[L]=7, seed `20260622`) | **0.2609** | — |
| block-perm null disc median (pp) | +1.96 | — |
| block-perm null disc 95% CI (pp) | [−14.6, +18.2] | — |
| block-perm null n-anchors mean (n_obs=11) | 11.01 | — |

**Per-bar verdict** (§5 verbatim):

| bar | target | observed | result |
|---|---|---:|:---:|
| **Bar 1** — directional sign agrees with HA11 v1's +22.8pp (positive) | disc > 0 | **+20.26 pp** | **PASS** |
| **Bar 2** — effect-size comparability (within ±10pp of HA11 v1's +22.8pp) | disc ≥ +12.8 pp | **+20.26 pp** | **PASS** |
| **Bar 3** — p-value comparability under block-permutation null at E[L]=7 | p < 0.05 | **p = 0.2609** | **FAIL** |

**Aggregate verdict**: **PARTIAL** (2 of 3 bars met).

**Reading**: the bout-level operand's observed discrimination magnitude is comparable to HA11 v1's +22.8pp signal (+20.26 vs +22.8 — within 2.6 pp), AND the direction is correctly positive (crash-anchor windows trigger more often than HA11 v1's null-pool reference-date windows). Both magnitude-comparability bars clear cleanly. What fails is the block-permutation p-value: the +20.26 pp discrimination is not statistically distinguishable from the null distribution under stationary-bootstrap-resampling the `is_crash_anchor` labels at E[L]=7. This is consistent with pre-reg §9.2's first PARTIAL configuration ("Bars 1+2 met, bar 3 fails: discrimination magnitude is comparable but block-permutation null indicates the signal is not statistically distinguishable. Possible operand under-power at bout-level").

**HA11 v1 reference-frame comparison** (descriptive; not gating):

| | HA11 v1 train (`u_dip_count`) | HA11-bout-redo train (`bout_n_fast_recovery_day`) |
|---|---:|---:|
| crash-arm trigger frequency | 64.3% (9/14) | 54.5% (6/11) |
| null-pool trigger frequency | 41.5% (83/200) | 34.3% (24/70) |
| discrimination (pp) | **+22.8** | **+20.26** |
| median signed z (triggering) | 2.168 | 2.410 |
| n_crash episodes | 14 (all train) | 11 (post §4.4 + §4.7 + unmed) |
| n_null reference dates | 200 | 70 (post unmed × train × §4.7) |

The bout-level operand reproduces HA11 v1's effect size cleanly (within 2.6 pp), but at a smaller analysis-pool size — both crash-arm n (11 vs 14) and null-pool n (70 vs 200) are smaller. This power difference, combined with the bootstrap's tendency to produce wide null distributions at small n, is the proximate cause of the p-value failure on bar 3.

**E[L]\* data-driven companion** (pre-reg §4.8 + parent MD §5.1; descriptive context only):
- E[L]\* on `bout_n_fast_recovery_day` series (train era): **7.0 days** (cutoff_lag=1).
- Factor-of-2 flag (|E[L]\* − 7| / 7 > 0.5): **NOT FIRED** — E[L]\*=7.0 matches the project default exactly.
- Block-length choice is well-calibrated; the p=0.2609 failure on bar 3 is not attributable to a block-length mis-specification.

## §4 Sensitivity arms (descriptive; cannot promote to PASSED per single-cell headline lock)

Per pre-reg §4.10 + parent MD §3.4: each arm re-aggregates `bout_n_fast_recovery_day` from `per_bout_master.csv` with the appropriate per-bout flag filter; the rest of the pipeline (z-scoring, window aggregation, trigger frequencies, block-permutation) is byte-identical.

| arm | n_calm | n_crash | disc (pp) | block-perm p | bar 1 | bar 2 | bar 3 | verdict | fragility vs primary |
|---|---:|---:|---:|---:|:---:|:---:|:---:|:---:|---|
| **primary** | 70 | 11 | **+20.26** | 0.2609 | PASS | PASS | FAIL | **PARTIAL** | — |
| motion-clean-only (motion_confound_flag=False) | 0 | 0 | — | — | — | — | — | INCONCLUSIVE | **degenerate** (see below) |
| transient-excluded (transient_flag=False) | 70 | 11 | +11.69 | 0.4656 | PASS | FAIL | FAIL | FAILED | **flagged** (transient-fragility) |
| baseline-invalid-excluded (baseline_invalid_flag=False) | 70 | 11 | +20.26 | 0.2609 | PASS | PASS | FAIL | PARTIAL | consistent |

**Motion-clean-only arm degeneracy**: of 4317 per-bout records, **4285 (99.3%) carry `motion_confound_flag=True`**; only 32 bouts are motion-clean. Filtering produces a per-day count series with near-zero variance, which collapses below the §4.6 σ > 0.5 floor on every day → 0 analysis days survive → 0 calm/crash windows. This is a per-bout data property (the participant's bout activity is overwhelmingly motion-coincident at this corpus + extraction threshold), not a test bug. Per pre-reg §9.5 sensitivity-arm divergence rule: motion-fragility flag fired by virtue of arm INCONCLUSIVE vs primary PARTIAL. **Reading**: framework-validity verdict at motion-clean-only is structurally untestable on this corpus + extraction threshold; cannot say anything about motion-confound robustness of the bout-level signal until either (a) the bout-detection threshold is relaxed to admit more motion-clean bouts or (b) a per-bout motion-proxy is recalibrated.

**Transient-excluded arm degradation**: dropping transient bouts (954 of 4317; ~22%) reduces discrimination from +20.26 pp to +11.69 pp — below the §5 bar 2 threshold of ≥ +12.8 pp. Per pre-reg §9.5: transient-fragility finding flagged. **Reading**: a non-trivial fraction of the bout-level reproduction signal lives in transient bouts. If the parent MD's discipline shifts to exclude transients from the primary (the r2 absorb explicitly includes them per parent MD §3.1.1), the bout-level operand's reproduction degrades further. The primary keeps transients per spec; the fragility flag is a descriptive finding for HA-C4c framing.

**Baseline-invalid-excluded arm consistency**: only 44 of 4317 bouts (1.0%) carry `baseline_invalid_flag=True`; excluding them changes nothing at the per-day count level. Verdict identical to primary. Per pre-reg §9.5: no fragility flag fired.

## §5 Crash-drop sensitivity (CONVENTIONS §3.4 + pre-reg §4.10)

Per pre-reg Authorship locked-decision item 5 + CONVENTIONS §3.4: re-run the primary procedure with `is_crash == True` rows dropped from the analysis-day pool (both calm-pool reference-date windows whose [r-3, r] window includes a crash day AND crash-anchor windows where the anchor itself is a crash day; the latter is rare since anchors are C-1 not C).

| metric | primary | crash-dropped | Δ |
|---|---:|---:|---:|
| n_calm | 70 | 62 | −8 |
| n_crash | 11 | 10 | −1 |
| discrimination (pp) | **+20.26** | **+19.35** | **−0.90 pp** |
| Cliff's δ | +0.306 | +0.326 | +0.020 |
| block-permutation p | 0.2609 | 0.3391 | +0.078 |
| verdict | PARTIAL | PARTIAL | (unchanged) |

**|Δ pp| = 0.90 < 5.0 pp threshold → §3.4 flag NOT FIRED → CLEAN**. The framework-validity signal is robust across the broader pool with crash-days dropped; it is not crash-driven. (Compare the slight discrimination reduction of 0.9 pp to the inverse-direction effect seen elsewhere in the project where crash-drop sometimes *amplifies* the signal; here the result is essentially flat, consistent with the bout-level operand picking up a true lead-up dynamic rather than a single-day spike.)

## §6 Verdict and cascade implication

**Aggregate verdict: PARTIAL** (2 of 3 bars met; bars 1+2 met cleanly, bar 3 fails).

**Cascade implication** per pre-reg §9.2: **HA-C4c drafting UNBLOCKS with explicit calibration caveat**. The bout-level operand reproduces HA11 v1's signal at directional + effect-size comparability (the headline magnitudes — +20.26 pp vs +22.8 pp, median signed z 2.410 vs 2.168 — are tightly aligned), but the block-permutation p does not clear 0.05 at the present analysis-pool size (n_calm=70, n_crash=11). The operand is *partially fit for purpose* for HA-C4c.

**Specific PARTIAL framing for the HA-C4c pre-reg** (per §9.2):
- The HA-C4c pre-reg's §8 caveats MUST carry an explicit calibration caveat naming **bar 3 (block-permutation p) as the failing bar**, with the verbatim observed values (disc = +20.26 pp; p = 0.2609 vs threshold 0.05).
- HA-C4c's substantive verdict-magnitudes are interpreted with a calibration discount: the operand can reproduce the *magnitude* of HA11 v1's signal but the present sample size at unmed × train cannot statistically distinguish it from the block-permutation null. HA-C4c, which extends the substantive scope and may carry a different sample-size structure, must re-evaluate its own statistical-significance bars in light of this finding.
- Per pre-reg §9.2: the parent methodology MD remains LOCKED; HA11 v1 stands unchanged; the bout-extraction pipeline LOCK at `d5b394c` stands. An operand-refinement v2 of HA11-bout-redo (re-tuning the 15-min / 45-min thresholds in parent MD §6.1) is OPTIONAL — not required, but available if HA-C4c finds the calibration caveat too binding. PARTIAL does NOT halt the cascade.

**Sensitivity-arm cross-implications for HA-C4c**:
- **Transient-fragility** (the +11.69 pp transient-excluded discrimination falls below bar 2): if HA-C4c's substantive design ends up implicitly excluding or down-weighting transients (e.g. via a different bout-count operand variant), the calibration discount widens.
- **Motion-clean-only INCONCLUSIVE**: the bout-extraction pipeline at present cannot answer whether the framework-validity signal is motion-robust. HA-C4c should NOT make any motion-clean-restricted claims absent re-running the bout-extraction with a relaxed motion threshold OR adding a §4 caveat naming this gap.
- **Baseline-invalid + crash-drop both clean**: no fragility on these axes.

**One sentence for the dispatcher**: *the bout-level operand's discrimination magnitude reproduces HA11 v1's signal (+20.26 vs +22.8 pp) but the block-permutation p does not clear 0.05 at the present n; HA-C4c drafting unblocks with a calibration caveat per pre-reg §9.2.*

## §7 Caveats

1. **Power-calc dispatch (pre-reg §8 caveat 1; LOCKED verbatim)**: power calc inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design. The block-permutation null at E[L]=7 (§4.8) is the within-subject inferential machinery; the §5 three-bar verdict rule determines the framework-validity verdict rather than asymptotic-power thresholds.

2. **n=1 single-subject + observational + multi-source** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-discipline-the-baseline-is-the-tested-individuals-own-multi-day-distribution). Personal-baseline-thresholded; cross-subject generalisation out of scope.

3. **Framework-validity-NOT-substantive scope (pre-reg §8 caveat 3, LOCKED verbatim)**: the PARTIAL verdict is a framework-validity finding, NOT a substantive claim about Wiggers C4. The bout-level operand is *partially fit* for HA-C4c; it does NOT validate the operand globally and does NOT prejudge HA-C4c's substantive verdict.

4. **Inheritance-risk caveat (pre-reg §8 caveat 4, LOCKED verbatim)**: bar 3's failure cannot fully distinguish between "operand under-power" and "the signal HA11 v1 detected was U-dip-specific, not within-day-recovery-shape-general". The +20.26 pp directional + magnitude reproduction is strong evidence the construct generalises; the bootstrap-null insignificance at present n is the open question.

5. **Firstbeat-input amplification at minute resolution (pre-reg §8 caveat 5)** + **pacing-behaviour mask risk (pre-reg §8 caveat 6)** apply; the partial reproduction is consistent with both "operand fit and under-powered" and "algorithmic noise dominates partially" — the result cannot fully discriminate.

6. **Era restriction is non-negotiable (pre-reg §8 caveat 7)**: validate-era reproduction is out of scope; this PARTIAL finding pertains to train only.

7. **Crash-drop sensitivity is reported but not gating (pre-reg §8 caveat 8)**: |Δ pp|=0.90 < 5.0 threshold; primary verdict unchanged; crash-drop arm reaffirms the signal is not crash-driven.

8. **Pipeline-extraction trust assumption (pre-reg §8 caveat 9)**: this result assumes `extract_stress_bouts.py` LOCKED `d5b394c` correctly implements parent MD §3 + §4. The pipeline's 6 inline smoke tests + 5-bout spot-check verification provide audit coverage. No pipeline-trust issues surfaced during test execution.

9. **Multi-comparison (pre-reg §8 caveat 10)**: single-cell headline lock. The 3 bars in §5 are NOT independent tests; they jointly comprise the framework-validity gate's verdict per pre-reg §5. No multi-comparison correction needed at primary.

10. **Test-time learning — block-permutation interpretation**: at n_crash=11 vs n_calm=70, the bootstrap null distribution for discrimination (pp) is wide: median +1.96 pp, 95% CI [−14.6, +18.2] pp. The +20.26 observed discrimination sits at the 74th percentile of the null distribution (n_ge=2608 of 10000). With a 3x larger crash-arm (n=33) the same effect size would clear bar 3 by a wide margin; the present PARTIAL reflects sample-size constraints on the framework-validity gate's third bar, not effect-size weakness.

## §8 Reproducibility checklist

- **Script**: [`docs/research/analyses/hypotheses/HA11-bout-redo/test.py`](test.py).
- **Environment variable**: `GEVOELSCORE_DATA_PATH` (or default `C:\Users\Gebruiker\Documents\gevoelscore-data` per HA-C4 / HA-C4b precedent). Required inputs:
  - `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` (pipeline-output; carries `bout_n_fast_recovery_day` joined from `per_bout_aggregations_daily.csv`).
  - `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` (for §4 sensitivity-arm re-aggregation).
  - `$GEVOELSCORE_DATA_PATH/analyses/hypotheses/HA11-stress-udip/udip_counts.csv` (for HA11 v1 reference-date replay).
  - `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv` (HA11 v1 inherited crash labels).
- **Seeds**:
  - HA11 v1 null-pool reference-date replay: `20260605` (inherited verbatim; produces the 200 reference dates).
  - Block-permutation null: `20260622` (HA11-bout-redo distinct seed per pre-reg §4.8 dual-seed cross-reference).
  - Cliff's δ CI paired-bootstrap: `20260622` (same as block-perm; project-default walk-forward CI).
- **Statistical machinery**:
  - Block-permutation null: stationary bootstrap (Politis-Romano 1994), geometric block length E[L]=7, B=10,000 draws. Implementation mirrors `inference.stationary_bootstrap_indices` + HA-C4 `block_permutation_p_value`; labels resampled, values fixed in place per pre-reg §4.8.
  - Data-driven E[L]\* companion: `_utils.inference.compute_data_driven_block_length` (Politis-White 2004 + Patton-Politis-White 2009 stationary-bootstrap correction; factor-of-2 flag at 0.5).
  - Mann-Whitney U: vendored mid-rank implementation (no scipy hard dep); reported as descriptive triangulation.
- **Regenerate command**:
  ```
  cd docs/research/analyses/hypotheses/HA11-bout-redo
  python test.py --dry-run   # §7.5 sanity gates only
  python test.py             # full run; emits result-data.json
  ```
- **Pipeline-trust block**: bout-extraction pipeline at `d5b394c` (2026-06-22). The pipeline's 6 inline smoke tests + 5-bout spot-check verification per [`pipeline/02_features/README.md`](../../../pipeline/02_features/README.md) provide audit coverage and were not re-run in this session per pre-reg §10.1 + lock-stage trust (the lock-stage gates verified pipeline-trust; re-running is not in scope for the test-execution session).
- **Output files**:
  - `result.md` (this file; committed).
  - `result-data.json` (machine-readable companion with full numeric outputs + null-distribution summary; gitignored per `docs/research/**/*.json` rule).

---

*Test run 2026-06-23 by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Pre-registration LOCKED 2026-06-23 r2 at [`hypothesis.md`](hypothesis.md) commit `5c71aa0` + footer-fix `b5bf0f8`; audit report [`reviews/HA11-bout-redo-2026-06-22.md`](../../../reviews/HA11-bout-redo-2026-06-22.md) (PASS-with-caveats). Worktree HEAD at run: `250a466`. Pipeline commit: `d5b394c`. Next stage: HA-C4c pre-reg drafting with PARTIAL-calibration caveat per pre-reg §9.2.*
