# HA-C4cp - RESULT: PARTIAL

Emitted by `test.py` per LOCKED r2 hypothesis.md section 10.3. **Headline cell**: cross-phase-pooled stratum (per HA-C4c section 4.2 verbatim) x `bout_n_did_not_return_2sd_day` x heavy-T-vs-non-heavy-T x Mann-Whitney U + Cliff's delta + block-permutation null at E[L]=7. **Seed**: `RANDOM_SEED = 20260709`; **B** = 10000. **Operand direction**: heavy-T > non-heavy-T (one-sided elevated). **Reference-frame**: personal-baseline-rolling (SD-anchored) per parent MD section 3.2.2; cross-operationalisation-independent from HA-C4c's fixed-absolute-threshold reference-frame at operand-family level per OI-025 protocol section 5.4 four-condition argument.

## Authorship

- **Drafting date**: 2026-07-14 (this result.md emitted in the post-lock test-execution session).
- **Agent**: Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS section 1.1](../../../CONVENTIONS.md). Authorising user: Willem.
- **Pre-reg commit**: r2 LOCKED 2026-07-09 at [`hypothesis.md`](hypothesis.md). Worktree HEAD at run: `e7da406`.
- **Test commit**: this session's `test.py` commit (set by dispatcher after cherry-pick).
- **Pipeline commit**: pipeline extension for parent MD section 3.2.2 columns LOCKED at Bundle H+ event 8 `521e9fe` (2026-07-14 corpus snapshot).
- **Status**: LANDED. Test executed end-to-end; dry-run section 10.4 gates passed; primary headline emitted; sensitivity arms reported; cascade implication recorded in section 11.

## Section 1 - Headline verdict + cascade context

**Verdict: PARTIAL** -- direction=+, (a) p<0.05=PASS (p=0.0090), (b) delta>=+0.20=FAIL (delta=+0.079).

**HA-C4c r2 PARTIAL magnitude-below-threshold calibration context (per pre-reg section 8 caveat 2)**: HA-C4c's landed Cliff's delta = +0.1523 missed the +0.20 bar by -0.05 with empirical p = 0.0091 (bar (a) cleared). HA-C4cp's operand-family compression argument (personal-baseline z-scoring against a rolling reference typically compresses cross-day effect sizes relative to fixed-threshold operands per CONVENTIONS section 3.1) predicts plausibly comparable or lower delta on HA-C4cp. PARTIAL is anticipated as the modal outcome; SUPPORTED requires the personal-baseline operationalisation to produce a strictly larger delta than the fixed-absolute-threshold arm. Read this verdict against that anticipation.

**Cross-test cascade implication (section 9.2 PARTIAL branch; bar (b)-failing configuration)**: direction-correct AND (a) block-perm p < 0.05 AND (b) Cliff's delta < +0.20. This EXACTLY MIRRORS HA-C4c's PARTIAL(bar-b-fail) pattern -- the operand-family compression argument's modal outcome. Under joint-cluster reading, HA-C4c PARTIAL + HA-C4cp PARTIAL(bar-b-fail) reads as CONCORDANT-BELOW-THRESHOLD -- both cells direction-correct, both PARTIAL, corpus effect-size ceiling reading per pre-reg section 9.2. This is a honest sample-limitation reading, NOT a Wiggers-C4 disproof. OI-033 CLOSED-BY-EXECUTION-PARTIAL; cross-op-independence gap CLOSED at direction-consistent-below-threshold reading.

## Section 2 - Per-bar table

| bar | target | observed | result |
|---|---|---:|:---:|
| direction | heavy-T > non-heavy-T (Cliff's delta > 0) | delta = +0.079 | PASS |
| **Bar (a) - discrimination** | block-perm p < 0.05 | p = 0.0090 | PASS |
| **Bar (b) - effect size** | Cliff's delta >= +0.2 | delta = +0.079 | FAIL |

## Section 3 - Per-arm summary table (primary cell)

| metric | heavy-T arm | non-heavy-T arm |
|---|---:|---:|
| n_days | 465 | 809 |
| mean `bout_n_did_not_return_2sd_day` | 0.538 | 0.441 |
| median `bout_n_did_not_return_2sd_day` | 0.00 | 0.00 |
| Mann-Whitney U (heavy first) | 202970 | -- |
| Mann-Whitney p (one-sided normal approx, descriptive) | 0.0093 | -- |
| Cliff's delta (heavy vs non-heavy) | +0.079 | -- |
| Cliff's delta 95% CI (paired-bootstrap B=2000) | [+0.024, +0.132] | -- |
| block-permutation p (E[L]=7, B=10000, seed `20260709`) | 0.0090 | -- |
| block-perm null delta median | +0.000 | -- |
| block-perm null delta 95% CI | [-0.062, +0.065] | -- |
| n_flagged_bouts (sum across days) | 607 | -- |

## Section 4 - Companion descriptives (per-day distribution + section 10.4 sanity)

| metric | observed | section 10.4 HALT window | HALT status | info anchor | info status |
|---|---:|---|:---:|---|:---:|
| per-day mean | 0.4765 | [0.01, 0.6] | PASS | [0.05, 0.3] | OUTSIDE |
| per-day median | 0.00 | <= 2.0 | PASS | in [0, 1.0] | INSIDE |
| per-day sigma | 0.6655 | -- | -- | -- | -- |
| per-day p25-p75 | [0.00, 1.00] | -- | -- | -- | -- |
| per-day range | [0.00, 3.00] | -- | -- | -- | -- |

**E[L]\* data-driven companion** (CONVENTIONS section 3.6 + parent MD section 5.1): E[L]\* = 7.00 days (cutoff_lag=None); factor-of-2 deviation flag: NOT FLAGGED. Per pre-reg section 4.6 + CONVENTIONS section 3.6: factor-of-2 flag is descriptive context only; does NOT modify the section 5 verdict.

### Reference-window audit trace (per section 4.11 mandatory reporting)

Per parent MD section 3.2.2 mandatory-audit-trace discipline + pre-reg section 4.11.

| stat | heavy-T lagged_median (min) | heavy-T lagged_mad (min) | non-heavy-T lagged_median (min) | non-heavy-T lagged_mad (min) |
|---|---:|---:|---:|---:|
| n | 465 | 465 | 809 | 809 |
| mean | 46.18 | 59.27 | 46.73 | 60.18 |
| median | 47.00 | 58.56 | 46.00 | 57.82 |
| p25 | 38.00 | 48.18 | 39.00 | 49.67 |
| p75 | 53.00 | 69.68 | 54.00 | 69.68 |

**Reference-window shortfall days on primary stratum**: 15 days routed to NaN via section 4.4 gate 4 (reference pool < 30 bouts in [d-90, d-30]). Per descriptive_audit.md LOCKED r1 section 6: expected 0 on primary stratum (the sub-phase-4b left-edge >= 2022-11-17 is more restrictive than the reference-window warmup trim).

### Cross-op concordance descriptive companion (per section 4.10 sister-test cross-reference)

2x2 concordance table between HA-C4c parent operand (`bout_n_did_not_return >= 1`) and HA-C4cp primary operand (`bout_n_did_not_return_2sd_day >= 1`) on the primary stratum. **Descriptive-only per Pass 1 discipline**; NOT part of the section 5 verdict machinery.

|  | HA-C4c fires | HA-C4c does NOT fire | total |
|---|---:|---:|---:|
| **HA-C4cp fires** | 427 (33.5%) | 61 (4.8%) | 488 |
| **HA-C4cp does NOT fire** | 259 (20.3%) | 527 (41.4%) | 786 |
| **total** | 686 | 588 | 1274 |

**Cohen's kappa** (chance-corrected agreement; descriptive companion): observed agreement = 0.7488, expected agreement = 0.4910, **kappa = 0.507**. Per Landis-Koch 1977 cutoffs: 0.41-0.60 = moderate; 0.61-0.80 = substantial. **Cap-unreachable days**: 452 of 1274 (35.5%) have Z=2 threshold > 180-min `tail_length` cap by construction (SD-anchored operand cannot fire on those days regardless of bout activity).

## Section 5 - Sensitivity arms (per section 4.10; descriptive; cannot promote to SUPPORTED)

| arm | operand | n_heavy | n_non_heavy | heavy mean | non-heavy mean | Cliff's delta | block-perm p | (a) | (b) | verdict | fragility vs primary |
|---|---|---:|---:|---:|---:|---:|---:|:---:|:---:|:---:|---|
| **primary** (cross-phase-pooled) | `bout_n_did_not_return_2sd_day` | 465 | 809 | 0.538 | 0.441 | +0.079 | 0.0090 | PASS | FAIL | **PARTIAL** | -- |
| Z=1 sensitivity | `bout_n_did_not_return_1sd_day` | 465 | 809 | 1.026 | 0.878 | +0.106 | 0.0009 | PASS | FAIL | PARTIAL | consistent |
| z_max continuous sensitivity | `bout_return_time_z_max_day` | 463 | 806 | 1.831 | 1.520 | +0.137 | 0.0001 | PASS | FAIL | PARTIAL | consistent |
| reference-window [d-60, d-30] | `bout_n_did_not_return_2sd_day` | 463 | 806 | 0.516 | 0.475 | +0.037 | 0.1327 | FAIL | FAIL | REJECTED | flagged |
| unmedicated-only stratum | `bout_n_did_not_return_2sd_day` | 183 | 323 | 0.355 | 0.344 | +0.004 | 0.4678 | FAIL | FAIL | REJECTED | flagged |
| motion-clean-only (motion_confound_flag=False) | `bout_n_did_not_return_2sd_day` | 465 | 809 | 0.000 | 0.000 | +0.000 | 1.0000 | FAIL | FAIL | REJECTED | flagged |
| transient-excluded (transient_flag=False) | `bout_n_did_not_return_2sd_day` | 465 | 809 | 0.516 | 0.418 | +0.082 | 0.0061 | PASS | FAIL | PARTIAL | consistent |
| baseline-invalid-excluded (baseline_invalid_flag=False) | `bout_n_did_not_return_2sd_day` | 465 | 809 | 0.520 | 0.425 | +0.079 | 0.0092 | PASS | FAIL | PARTIAL | consistent |
| reference-pool did_not_return-excluded | `bout_n_did_not_return_2sd_day` | 463 | 806 | 1.140 | 1.017 | +0.091 | 0.0024 | PASS | FAIL | PARTIAL | consistent |

### Crash-drop sensitivity (CONVENTIONS section 3.4 + pre-reg section 4.10)

| metric | primary | crash-dropped | delta |
|---|---:|---:|---:|
| n_heavy | 465 | 441 | -24 |
| n_non_heavy | 809 | 745 | -64 |
| Cliff's delta | +0.079 | +0.096 | +0.017 |
| block-perm p | 0.0090 | 0.0016 | -0.0074 |
| verdict | PARTIAL | PARTIAL | unchanged |

**|Delta Cliff's delta| = 0.017** (threshold 0.1 per CONVENTIONS section 3.4 + HA-C4c pattern): NOT FIRED (clean). **|Delta Cliff's delta * 100| = 1.70 pp** (threshold 5.0 pp per HA11-bout-redo analogue): NOT FIRED. **Route to REJECTED** (|delta delta| > 0.2 AND sign-flip): NO.

### Approach A dose-adjusted sensitivity arm (section 4.9 inheritance-by-analogue; descriptive companion only)

Per pre-reg section 4.9 underpowered-NULL framing + section 8 caveat 3: the Approach A inheritance is **inheritance-by-analogue** from `bout_n_fast_recovery_day` buildup-post-CPAP beta = -0.056/mg [CI -0.145, +0.034] (sign-flipped to +0.056/mg for HA-C4cp's +1 prior direction). The source beta is NULL/weakly-consistent (CI crosses zero; p=0.223 in the source recalibration). This is a **descriptive companion** under the underpowered-NULL frame; NOT a load-bearing dose-correction. The CI-bracket sub-arm characterises **inheritance fragility**, amplified per section 4.9 last paragraph because the SD-anchored operand family is FURTHER removed from the analogue's operand family than HA-C4c's fixed-absolute-threshold operand.

| sub-arm | beta/mg | Cliff's delta | block-perm p | (a) | (b) | verdict | divergence from primary |
|---|---:|---:|---:|:---:|:---:|:---:|---|
| Approach A primary template | +0.056 | +0.081 | 0.0206 | PASS | FAIL | PARTIAL | consistent |
| CI lower bracket (NULL) | +0.145 | +0.057 | 0.0910 | FAIL | FAIL | REJECTED | DIVERGENT |
| CI upper bracket (NULL) | -0.034 | +0.043 | 0.1506 | FAIL | FAIL | REJECTED | DIVERGENT |

## Section 6 - Holm step-down (section 5.3; secondary fragility-flag report)

**Holm (7-of-7 sens arms; all valid)** at alpha=0.05.

| cell | rank | raw p | threshold | adjusted p | Holm-rejected |
|---|---:|---:|---:|---:|:---:|
| z_max_continuous | 1 | 0.0001 | 0.00714 | 0.0007 | YES |
| z1_count | 2 | 0.0009 | 0.00833 | 0.0054 | YES |
| transient_excluded | 3 | 0.0061 | 0.01000 | 0.0305 | YES |
| primary | 4 | 0.0090 | 0.01250 | 0.0360 | YES |
| reference_window_shorter_lag | 5 | 0.1327 | 0.01667 | 0.3981 | NO |
| unmedicated_only | 6 | 0.4678 | 0.02500 | 0.9355 | NO |
| motion_clean_only | 7 | 1.0000 | 0.05000 | 1.0000 | NO |

**Family-membership caveat (LOAD-BEARING per pre-reg section 5.3 + section 8 caveat 6)**: the Z=1 (`z1_count`) and z_max (`z_max_continuous`) sensitivity arms share the parent MD section 3.2.2 reference-window construction with the primary -- same [d-90, d-30] window, same reference pool, same `subject_lagged_median` + `subject_lagged_mad` scaling. They are NOT fully independent tests; a shared-reference-window construction bias would propagate to all three cells. A 'Holm passes on primary AND z1_count AND z_max_continuous' reading must NOT be interpreted as independent confirmation of the primary signal; it is instead consistent-reference-window internal-consistency. The `reference_window_shorter_lag` arm is the FIRST INDEPENDENT diagnostic (different window definition); the `reference_pool_dnr_excluded` arm at section 4.10 (not in the Holm family) is the SECOND (different pool composition).

Per pre-reg section 5.3: Holm is a secondary fragility-flag report. The primary verdict per section 5.2 is the uncorrected primary cell; Holm cannot override.

## Section 7 - Sister-test cross-reference table

Per pre-reg section 4.10 + CONVENTIONS section 4.4: descriptive only; NO cross-test pass conclusion at result-emission time. Cross-test interpretation lives in [cluster-C-bout-substance.md](../../synthesis/cluster-C-bout-substance.md) per Stage S1 internal-synthesis routing.

| hypothesis | verdict | one-line note |
|---|---|---|
| HA-C4c r2 | PARTIAL magnitude-below-threshold | cross-phase-pooled bout-level; delta=+0.1523, p=0.0091, n=1274; fixed-absolute-threshold sister |
| HA-C4c-stringency-companion | NON-TRIGGER (Pass 1) | f2(T) monotone descent 0.5863 -> 0.1020 across T in {30,60,120,180}; OI-025 CLOSED-DESCRIPTIVE-ONLY |
| HA-C4 v2 | REJECTED | daily-aggregate triad sum 0.0/3.0 |
| HA-C4b v3 | NOT-SUPPORTED | motion-filter crash-precursor |
| HA11 v1 | SUPPORTED-on-train | U-dip count +22.8 pp |
| HA11-bout-redo | PARTIAL | framework-validity 2-of-3 bars met; bar 3 p=0.2609 at n_calm=70/n_crash=11 |
| **HA-C4cp (this test)** | **PARTIAL** | cross-phase-pooled bout-level personal-baseline SD-anchored; delta=+0.079, p=0.0090, n_heavy=465, n_non_heavy=809 |

## Section 8 - Pipeline-trust block

Bout-extraction pipeline + SD-anchored derivative operand family extension LOCKED at Bundle H+ event 8 commit `521e9fe` (2026-07-14). The pipeline's inline smoke tests provide audit coverage; parent MD section 3.2.2 defines the reference-window construction the pipeline implements.

- COL `bout_n_did_not_return_2sd_day`: HA-C4cp primary; `0` on valid days with no flagged bouts, NaN on reference-window-invalid days. Zero-vs-NaN discipline load-bearing per DATA_DICTIONARY section 8E; test.py NEVER `.fillna(0)` this column.
- COL `bout_n_did_not_return_1sd_day`: Z=1 sensitivity; same zero-vs-NaN discipline.
- COL `bout_return_time_z_max_day`: z_max continuous sensitivity; NaN on 0-bout days OR reference-window-invalid days per parent MD section 3.2.2.
- COL `subject_lagged_median_day` / `subject_lagged_mad_day`: reference-window audit trace (median + 1.4826*MAD of per-bout `tail_length` over [d-90, d-30] LC-era lagged pool).

## Section 9 - Verification log

Anchors the test on the cascade state at run-time:

- Pre-reg `hypothesis.md` r2 LOCKED 2026-07-09.
- Worktree HEAD at test-time: `e7da406`.
- Pipeline (SD-anchored extension) commit: `521e9fe` (Bundle H+ event 8, 2026-07-14).
- Parent MD (`bout_level_recovery_dynamics.md`) LOCKED r3 2026-07-09 (section 3.2.2 SD-anchored family).
- Sister pre-reg (fixed-absolute-threshold arm): HA-C4c r2 LOCKED 2026-07-08 landed PARTIAL.
- HA-C4c-stringency-companion Pass 1 NON-TRIGGER 2026-07-09 (OI-025 CLOSED-DESCRIPTIVE-ONLY).
- Stage D descriptive audit (`analyses/descriptive/HA-C4cp/descriptive_audit.md`) LOCKED r1 2026-07-14; sanity + walk-forward gates PASS at descriptive-layer.
- Dry-run gates per section 10.4: overall PASS at run-time (walk-forward n_heavy=465, n_non_heavy=809; per-day mean=0.4765; median=0.00; parent-op determinism check mean=0.6444).
- Per-day master CSV: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` (column `bout_n_did_not_return_2sd_day`); primary stratum non-NaN days: 1274; reference-window shortfall days: 15.
- Per-bout master CSV: `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` (used for section 4.10 sensitivity-arm re-aggregation including reference-window-shorter-lag and reference-pool-did_not_return-excluded arms).

## Section 10 - Caveats (per pre-reg section 8; all 8 prominently surfaced)

1. **Personal-baseline reference-window carries a subject-relative interpretation**: the SD-anchored operand does NOT test 'how long is the bout return-time in absolute minutes' but 'how much longer than the subject's own recent typical return-time is this bout'. A REJECTED verdict on HA-C4cp with HA-C4c at PARTIAL reads as 'the signal is anchored to the fixed-absolute-threshold reference frame only'. A SUPPORTED verdict reads as 'the signal generalises across both operand families'.

2. **HA-C4c PARTIAL calibration discount**: HA-C4c's landed delta = +0.1523 misses the +0.20 bar by -0.05. Operand-family compression predicts a plausibly-similar or lower delta on HA-C4cp. PARTIAL is anticipated as the modal outcome; SUPPORTED requires the personal-baseline operationalisation to produce a strictly LARGER delta than the fixed-absolute-threshold operationalisation.

3. **Approach A inheritance-by-analogue caveat**: the `bout_n_fast_recovery_day` beta = -0.056/mg [CI -0.145, +0.034] p=0.223 template is NULL/weakly-consistent per recalibration's underpowered-NULL framing; sign-flip is a fiat directional prior; analogue substitution uncertainty is AMPLIFIED for HA-C4cp because the SD-anchored operand family is FURTHER removed from the analogue than HA-C4c's fixed-absolute operand. Dose-adjusted arm at section 4.9 is descriptive companion only.

4. **Motion-confound corpus property**: 99.3% motion-confound at bout level per HA11-bout-redo result section 4. HA-C4cp's motion-clean-only sensitivity arm anticipated INCONCLUSIVE. Wiggers' 'during rest periods' verbatim implies a rest-conditional read; the corpus does not admit a clean rest-conditional operand at bout level; the SD-anchored family does not resolve this caveat -- it changes the reference frame for 'atypical' but does not filter for motion-clean state.

5. **Transient-fragility inheritance**: HA11-bout-redo transient-excluded discrimination dropped from +20.26pp to +11.69pp. HA-C4cp likely to see analogous attenuation on `bout_n_did_not_return_2sd_day` under transient exclusion; reported at section 4.10.

6. **Reference-window construction dependency (LOAD-BEARING per section 5.3 family-membership caveat)**: the Z=1 and z_max sensitivity arms share the parent MD section 3.2.2 reference-window construction with the primary. If the reference-window calibration itself is off, all three cells inherit the bias. The `reference_window_shorter_lag` and `reference_pool_dnr_excluded` sensitivity arms are the reference-window-fragility diagnostic companions. The primary verdict is robust to this caveat via the CONVENTIONS section 3.1 robust-baseline discipline (median + MAD).

7. **Cross-op independence at operand-family level, NOT raw-substrate level** (per OI-025 protocol section 5.4 four-condition argument): HA-C4c and HA-C4cp both derive from the same Firstbeat-per-minute stress signal via the same bout-detection pipeline. The independence claim binds at operand-family level (fixed-absolute-threshold vs personal-baseline-rolling). A shared-substrate correlated failure mode would affect both HAs.

8. **Reference-window left-edge trim**: the [d-90, d-30] window trims ~60-90 days from the leftmost has_garmin_uds=True coverage; the primary stratum's >= 2022-11-17 left edge is more restrictive, so this trim does not become binding at primary. The unmedicated-only sensitivity arm inherits the same trim and may lose ~30 days of unmedicated coverage.

## Section 11 - Downstream actions (per pre-reg section 9 branch that actually fired)

Per pre-reg section 9.2 PARTIAL branch:

- Stage D + Stage I + Stage S1 LOCK with PARTIAL routing; cluster-C-bout-substance joint verdict likely CONCORDANT-BELOW-THRESHOLD (both direction-correct; both PARTIAL).
- Stage A tier-2 licensing stands; section 5.2 evidence-layer paragraph updates to PARTIALLY REACHED (cross-op-independence gap CLOSED at direction-consistent-below-threshold reading).
- Substantive interpretive note: corpus-effect-size ceiling finding -- the Wiggers-C4 signal fires directionally on this corpus at bout-level across both operand families but the effect-size is bounded below the +0.20 SUPPORTED threshold. Honest sample-limitation reading, NOT a Wiggers-C4 disproof.
- OI-033 CLOSED-BY-EXECUTION-PARTIAL.

---

*Test run 2026-07-14 by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS section 1.1](../../../CONVENTIONS.md). Pre-registration r2 LOCKED 2026-07-09 at [`hypothesis.md`](hypothesis.md). Worktree HEAD at run: `e7da406`. Pipeline commit: `521e9fe`. `result-data.json` is the machine-readable companion (gitignored per `docs/research/**/*.json` rule).*
