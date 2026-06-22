# HA-C3 — Non-linear / convex stress→fatigue mapping (Tier 1 Wiggers)

## Authorship

**Drafted 2026-06-22** by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default). Authorising user: Willem. **Fresh-session drafting per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)** per the session handoff brief at `C:/Users/Gebruiker/.claude/plans/session-HA-C3-pre-reg-drafting-handoff-2026-06-22.md`.

**Drafting trigger**: Tier-1 Wiggers completion. HA-C3 is the **only Tier 1 Wiggers row without an HA-folder** per the [register Priority shortlist](../../../wiggers_testable_hypotheses.md#tier-1--source-verified-verbatim--no-family-history-priority-pre-regs). Its sister Tier-1 entry, [HA-C4 v2](../HA-C4/hypothesis.md), was pre-registered, locked, tested, and REJECTED at the daily-aggregate level (commit `52bddb5`). HA-C3 tests a structurally distinct claim — function *shape* (convex stress→fatigue mapping), not recovery dynamics — and is testable now without pipeline dependency (column infrastructure ready per register).

**Drafting-session context**: this drafter has read end-to-end the C3 register row + verification log (PDF lines 1357-1368), the C3 column-mapping in the pre-reg-draft section, the modern-template pre-reg [HA-C4 v2](../HA-C4/hypothesis.md) (shape reference only — claim-distinct), [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) §3-§5 (THE binding rule for `all_day_stress_avg`), [`citalopram_dose_response_stress_mean_sleep.md §5.6`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) (β = +0.57/mg CONFIRMED dose-modulation on `all_day_stress_avg`), [`train_validate_split_fate.md`](../../../methodology/train_validate_split_fate.md) (full Stratum 4 single pool default), [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) (E[L]=7 default), [`time_resolution.md`](../../../methodology/time_resolution.md) §6 (mechanism-driven scale; C3 register-defaulted to per-day), [`hypothesis_lock_process.md`](../../../methodology/hypothesis_lock_process.md) §3.2 + §3.8 lock gates, and [CONVENTIONS](../../../CONVENTIONS.md) §1.1, §2.1, §3.4, §3.6, §4.1-§4.3. The drafter has NOT inspected the joint distribution of `all_day_stress_avg` × `gevoelscore` on this corpus — descriptive bin-means are deferred to the dry-run stage per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).

**Data exposure context** (audit-able): the drafter has descriptive knowledge of `all_day_stress_avg` coverage (~1732 / 1755 = 98.7%; range 0-100 integer per DATA_DICTIONARY §7B) and `gevoelscore` coverage (~1126 / 1755 since 2022-09-03; range 1-10 nullable int per DATA_DICTIONARY §1). No knowledge of the joint bin-mean trajectory, no knowledge of the per-bin n or per-bin median. The convexity contrast, bin specification, and verdict bar are pre-committed before any joint-distribution inspection.

**Locked decisions at draft time** (load-bearing pre-commits; surfaced explicitly per the handoff brief §3 + per [`hypothesis_lock_process §3.2 step 5`](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)):

1. **Citalopram approach for `all_day_stress_avg`** — **§5.A per-phase stratification as the PRIMARY**, with the unmedicated phase as the headline pool; **§5.B dose-adjusted predictor as a CROSS-PHASE SENSITIVITY ARM** reported alongside (not promoted to primary). Rationale: the C3 claim is about the *shape of the within-subject stress→fatigue function*, which is well-defined within any single phase (per [`citalopram_phase_stratification §5.A`](../../../methodology/citalopram_phase_stratification.md#5a-per-phase-stratification-the-default-lowest-risk)). The unmedicated phase (2022-04-04 → 2024-04-08, ~735 days) is the Wiggers-prior-aligned headline because the participant's lived-experience phrasing predates citalopram. §5.B as sensitivity is the appropriate test of *invariance*: if the shape claim is structural to the participant's stress-fatigue mapping, the dose-adjusted curve should be convex too. §5.C unmedicated-only restriction is dispatched as "§5.A primary IS effectively unmedicated-only at the headline level" — the §5.A framing makes the secondary phases reportable as descriptive replication rather than discarded.

2. **Bin specification** — inherit the register pre-reg draft verbatim: `0-20, 20-30, 30-40, 40-60, 60+` (left-inclusive intervals; right-open except 60+ which is closed-above). Rationale: bin boundaries align with the Wiggers source-verified anchor (PDF 1357-1368: "a day with a score of 40 is much more tiring than a day with a score of 30 — a step appears very small on the graph, but it isn't"). The 30→40 boundary IS the verbatim Wiggers step; the asymmetric 40-60 width (vs 0-20 / 20-30 / 30-40 width-of-10) is intentional — the upper-tail register is sparser on Garmin daily stress (the descriptive distribution shows median in the 30s-40s per DATA_DICTIONARY annotations; reproducing the full descriptive distribution at dry-run per §7.5 below). The 60+ open-top bin captures the rare upper tail where the convex-cost prediction is sharpest.

3. **Convexity contrast vector** — the primary convexity test uses the **second-difference contrast on bin-means** of `gevoelscore`. If bin-means are `(m1, m2, m3, m4, m5)` ordered low-to-high stress, the second differences are `Δ²_i = m_{i+1} - 2·m_i + m_{i-1}` for i ∈ {2,3,4}. **Convex shape (SUPPORTED direction)**: gevoelscore decreases at an *accelerating* rate as stress rises (per the Wiggers stair-step framing) → the second-differences are systematically negative. Operational test statistic: **mean of the three second-differences `(Δ²_2 + Δ²_3 + Δ²_4) / 3`**, one-sided test against the null that the mean second-difference is ≥ 0. Significance via block-permutation null at E[L]=7. **Companion**: the contrast vector `c = (+1, +2, 0, -2, -1)` (sums to 0; orthogonal to the linear contrast) is a single-degree-of-freedom convexity score; report alongside the second-difference test for transparency. Justification for the second-difference primary: it is the textbook discretisation of the second derivative — the precise mathematical operationalisation of "marginal effect increases at higher stress". The handoff §3 candidate `(+1, -1, -1, -1, +2)` is rejected as it does not cleanly separate convexity from a single high-tail spike.

4. **Spline knot placement** — natural cubic spline regression with **4 knots placed at the bin boundaries (20, 30, 40, 60)**, NOT at quintiles. Rationale: knot-at-bin-boundary preserves cross-reference between the primary (binned-mean second-difference) and the secondary (spline non-linearity) tests; an internal-quintile knot placement would make the secondary test independent of the primary in a way that complicates joint interpretation. The non-linearity p-value comes from the chi-squared test on the spline's non-linear-term coefficients (the F-test on the difference between linear-only model and full-spline model). Companion: **report the spline curvature visually** at result.md time (a plot of the predicted spline against the bin-mean step function with 95% pointwise CI on both).

5. **Era split treatment** — full Stratum 4 single pool per [`train_validate_split_fate.md`](../../../methodology/train_validate_split_fate.md) is the primary. The 2023-12-31 train/validate split is reported as an **M3 descriptive overlay** in result.md (per-era bin-means plotted side-by-side; per-era second-difference test computed but reported as descriptive context, NOT as per-portion verdicts). Rationale: the C3 shape claim is structural-within-subject; the M3 overlay surfaces whether the shape is stable across the time-axis without committing to per-era confirmatory verdicts.

6. **Crash-drop sensitivity** — per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions) mandatory for any Layer-4+ Spearman/regression on PEM-pacing channels. **Crashes are KEPT in the primary** pool (the convex-cost claim should hold across all days, including crash days where the highest-stress bins are most populated). **Crash-drop sensitivity arm** re-runs the second-difference test with `is_crash == True` dropped; |Δ mean-second-difference| flagged if it crosses the convex/concave sign boundary. Rationale: the C3 mechanism is expected to be strongest near crash days (high-stress bins disproportionately contain crash days); a strong dependence of the verdict on crash-day inclusion is informative-for-interpretation per the §3.4 hook's purpose, not verdict-modifying.

7. **Block-permutation null block length** — inherit E[L]=7 per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). Data-driven `E[L]*` companion estimator computed on the `gevoelscore` residual series (residuals from the binned-mean fit); factor-of-2 flag fires if `|E[L]* - 7| / 7 > 0.5`. Per the methodology MD, the flag fires only on SUPPORTED verdicts; for PARTIAL or REJECTED, descriptive context only.

8. **Same-day vs lagged contrast** — **same-day mapping is primary** (Wiggers' verbatim claim is same-day stress vs same-day fatigue per the PDF 1357-1368 verbatim "a day with a score of 40 is much more tiring than a day with a score of 30"). **t+1 lagged variant as descriptive sensitivity arm** — same convexity test on `gevoelscore[T+1]` vs `all_day_stress_avg[T]` bins — reported for cross-test alignment with PEM-pacing hypotheses (HA-C4, HA-P7). Not promoted to primary.

**Status**: drafted, not locked.

---

**Pre-registration drafted 2026-06-22 as v1**, BEFORE any test run, BEFORE any inspection of the joint `all_day_stress_avg` × `gevoelscore` distribution beyond the marginal coverage stats in DATA_DICTIONARY. Any change after lock creates HA-C3-v2 with v1 archived as v1.

HA-C3 tests Wiggers' **"the stress→fatigue relationship is non-linear/convex — a 30→40 step costs more than it looks"** claim, source-verified verbatim per the register [C3 verification log](../../../wiggers_testable_hypotheses.md#c3--non-linear--convex-stressfatigue) batch 2 2026-06-12 (PDF lines 1357-1368, Annual Stress Scores section).

## 1. Claim

Within the LC frame and within the unmedicated phase (2022-04-04 → 2024-04-08), the **marginal effect of `all_day_stress_avg` on `gevoelscore` increases in magnitude as `all_day_stress_avg` rises**. The stress→fatigue function is **convex** (more precisely: monotone-decreasing with an accelerating decrement — gevoelscore drops by more per stress-unit at higher bins than at lower bins).

**Headline cell**: unmedicated phase × full Stratum 4 single pool × `all_day_stress_avg` binned at (0-20, 20-30, 30-40, 40-60, 60+) × `gevoelscore` bin-mean × {monotonicity test + convexity second-difference contrast + spline non-linearity test} × block-permutation null E[L]=7 × 3-condition gated verdict per §5.

**Direction of effect under SUPPORTED**: (a) monotone-decreasing bin-means (high-stress bins have LOWER gevoelscore); (b) accelerating decrement (the bin-mean step from 30-40 to 40-60 is LARGER in magnitude than the step from 0-20 to 20-30; quantified as the mean of three second-differences `(Δ²_2 + Δ²_3 + Δ²_4) / 3 < 0`); (c) spline non-linearity term significant with shape visually consistent with convexity.

**Verdict rule** (3-condition gated): see §5.

## 2. Why we think this

**The Wiggers paraphrase** is source-verified verbatim (per the register's [C3 verification log](../../../wiggers_testable_hypotheses.md#c3--non-linear--convex-stressfatigue) batch 2 2026-06-12). Three priors anchor this test:

**(a) Wiggers source — verbatim**: *"Your annual stress overview includes a stress score line. If you've paid attention to your own stress scores, you might know that a day with a score of 40 is much more tiring than a day with a score of 30. Such a step appears very small on the graph, but it isn't. This graph shows a kind of stair step. This person has overexerted themselves and their health is deteriorating as a result."* (PDF lines 1357-1368). The "stair-step" framing — sub-linear-looking small step costing more than its visual size — is the exact convexity claim this test operationalises. The 30→40 boundary IS the verbatim Wiggers anchor.

**(b) Lived experience on this corpus**: the participant has long described "the higher you are, the harder the next step costs you" pattern in the operational pacing protocol (per [`garmin_pacing_practice.md`](../../../methodology/garmin_pacing_practice.md) — though no explicit P-entry yet pre-registers this as a Personal-register hypothesis; HA-C3 tests the Wiggers verbatim, not a personal extension). The lived-experience prior is the convexity direction, not a specific functional form.

**(c) The CONFIRMED dose-response on `all_day_stress_avg` establishes channel signal-bearing causality**: the v3 multi-channel dose-response analysis ([`citalopram_dose_response_stress_mean_sleep.md §5.6`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14)) confirmed `all_day_stress_avg` as dose-modulated at +0.57/mg buildup-post-CPAP β (p = 0.0003, CI [+0.24, +0.89]) — the strongest dose-response signal across the multi-channel sweep. This establishes that `all_day_stress_avg` is a causally-modifiable channel on this corpus — it responds to an external intervention in the expected direction, which is necessary (though not sufficient) for it to carry a substantive within-subject mapping to `gevoelscore`. The dose-response evidence is independent of HA-C3's shape claim and is invoked here as a *signal-integrity prior*, not as part of the convexity argument.

**Sister-test context** (informational; no cross-test prior on convexity is claimed):

- **HA-C4 v2 REJECTED at daily-aggregate** (commit `52bddb5`; the 3-channel post-exertion-recovery triad did not survive the daily-aggregate test). C3 is a DIFFERENT claim — it is about the *same-day stress→fatigue mapping function shape*, not about the post-exertion-recovery dynamics. HA-C4's REJECTION does NOT prejudice HA-C3: a convex mapping can be true even if the recovery-dynamics channels collapse at daily resolution.
- **HA11 SUPPORTED on train** (within-day stress U-dip count). HA11 operates at within-day resolution; HA-C3 at per-day-aggregate resolution. The HA11 finding speaks to *within-day shape*, which is structurally distinct from HA-C3's *cross-day shape across stress bins*. Cross-reference only, no prior import.

## 3. Data sources

- **Predictor column**: `all_day_stress_avg` (24-hour mean stress score from Garmin UDS-extras; integer 0-100; TOTAL aggregator). Per [DATA_DICTIONARY.md §7B](../../../DATA_DICTIONARY.md), coverage ~1732 / 1755 (98.7%) after the 2026-06-12 negative-sentinel filter. Source: `processed/garmin/uds_extras_daily.csv`. **Dose-modulation status**: CONFIRMED at +0.57/mg per [`citalopram_dose_response §5.6.1`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read); load-bearing for §4.4 citalopram approach choice below.

- **Outcome column**: `gevoelscore` (daily subjective state score; nullable int 1-10, in practice 1-6 dense, 7-10 sparse). Per [DATA_DICTIONARY.md §1](../../../DATA_DICTIONARY.md#section-1--subjective-state-gevoelscore--note), coverage 2022-09-03 → today (~1126 days as of drafting). Source: `raw/directus_exports/day_entries.json`.

- **Phase derivation**: `citalopram_phase(d)` per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification); unmedicated boundary at 2024-04-08 inclusive.

- **PK-smoothed dose for §5.B sensitivity arm**: `dose_plasma_mg(d)` per [`citalopram_dose_response §2.3`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#23-pk-smoothed-plasma-proxy-primary-exposure) + the buildup/afbouw convolution; `dose_plasma_mg(d) = 0` for `d < 2024-04-09` per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification).

- **`is_crash` (for §4.6 crash-drop sensitivity arm)**: from crash_v2 labels per `analyses/hypotheses/crash_v2-definition/definition.md`.

**No new extraction required.** Both columns are already in `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` per the register's [C3 column-mapping row](../../../wiggers_testable_hypotheses.md#c-stress-score) (status: ✅).

## 4. Measurement protocol

### 4.1 Bin specification (locked)

The predictor `all_day_stress_avg` is binned into 5 categories with **left-inclusive, right-exclusive intervals (except 60+ which is closed-above)**:

| bin id | label | range | rationale |
|---|---|---|---|
| B1 | low | `[0, 20)` | sub-stair-step baseline |
| B2 | mid-low | `[20, 30)` | last sub-stair-step bin before the verbatim Wiggers 30→40 anchor |
| B3 | mid | `[30, 40)` | the lower side of the verbatim Wiggers 30→40 anchor |
| B4 | mid-high | `[40, 60)` | the upper side of the verbatim Wiggers 30→40 anchor extended to 60; asymmetric width-of-20 absorbs the sparser upper-tail register |
| B5 | high | `[60, 100]` | rare upper tail where the convex-cost prediction is sharpest |

**Boundary discipline**: bin edges are at integer stress-unit values matching the Wiggers verbatim 30→40 step; not data-driven, not quintile-anchored. The verbatim alignment is the load-bearing justification (per [`hypothesis_lock_process §5`](../../../methodology/hypothesis_lock_process.md#5-sanity-check-questions-before-lock) trigger-phrase-binding rule: the natural-language anchor "30 → 40 step" is bound to the operational B3 → B4 step here).

**Pre-flight check** (§7.5 sanity gate 1 below): the descriptive distribution of `all_day_stress_avg` on the unmedicated pool is reported at dry-run; **HALT if any of the 5 bins has < 30 observations** (the cell is structurally underpowered for the bin-mean comparison). Below this threshold, redraft as HA-C3-v2 with revised bins per [`hypothesis_lock_process §3.9`](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).

### 4.2 Stratum + pool (locked)

**Primary pool**: full Stratum 4 single pool per [`train_validate_split_fate.md`](../../../methodology/train_validate_split_fate.md) — `date >= 2022-04-04` (LC era start) AND `date <= 2024-04-08` (unmedicated phase end per §4.4 below). **Train/validate split is NOT used as a primary verdict surface**; see §4.5 below for the M3 descriptive overlay.

### 4.3 Day-validity gate (locked)

A day `T` enters the comparison if:

1. `T` is in the LC era (`date >= 2022-04-04`).
2. `T` is in the unmedicated phase (`date <= 2024-04-08`) for the primary; secondary §5.B sensitivity arm extends to all phases.
3. `T` is NOT in the April 2024 cluster (`2024-04-09 → 2024-04-16`) per [`citalopram_phase_stratification`](../../../methodology/citalopram_phase_stratification.md) (structural exclusion).
4. `T` has a non-NaN `all_day_stress_avg` value (excludes the sentinel-filtered dates per DATA_DICTIONARY §7B).
5. `T` has a non-NaN `gevoelscore` value (this excludes the 2022-04-04 → 2022-09-02 sub-window where gevoelscore was not yet logged — the **gevoelscore coverage gates the analysis**: the effective unmedicated-AND-gevoelscore pool starts 2022-09-03 → 2024-04-08, approximately 583 days before further exclusions).

**Expected post-gate pool size** (descriptive estimate from coverage stats, not pre-inspected joint distribution): on the order of 550-580 days. Confirmed at dry-run.

### 4.4 Citalopram phase treatment (locked — §5.A primary per the Locked decisions block; load-bearing)

`all_day_stress_avg` is a **CONFIRMED load-bearing dose-modulated channel** per [`citalopram_phase_stratification §4`](../../../methodology/citalopram_phase_stratification.md#4-per-channel-inheritance-rules) (β = +0.57/mg buildup-post-CPAP; cross-phase pooling on absolute values is biased). The framework MD's §4 audit hook requires the pre-reg to adopt one of §5.A / §5.B / §5.C; silence is not an option.

**Primary approach**: **§5.A per-phase stratification** with the **unmedicated phase as the HEADLINE pool**. Rationale (also surfaced in the Locked decisions block):

- The C3 claim is about the *shape of the within-subject stress→fatigue function*. Shape is well-defined within any single phase per [`citalopram_phase_stratification §5.A`](../../../methodology/citalopram_phase_stratification.md#5a-per-phase-stratification-the-default-lowest-risk).
- The unmedicated phase (2022-04-04 → 2024-04-08, ~735 days of which ~583 have gevoelscore) is the Wiggers-prior-aligned headline because the participant's lived-experience phrasing pre-dates citalopram.
- Avoids the +0.57/mg dose-modulation contaminating bin boundaries: a 40-stress-unit day at 30mg plasma is "really" a ~23-stress-unit day at 0mg plasma; pooling without adjustment would mis-classify medicated days into the wrong bin.

**Secondary (descriptive sensitivity, NOT promoted to primary verdict)**:

- **§5.A within-consolidation replication**: if consolidation phase (~638 days, of which ~600 have gevoelscore at the §4.3 gate) has ≥ 30 observations in each of the 5 bins, replicate the convexity test within consolidation. **Reported as descriptive context only**: a SUPPORTED-within-unmedicated AND SUPPORTED-within-consolidation reading is "the convexity shape is structural-within-subject across both phases"; a SUPPORTED-within-unmedicated AND REFUTED-within-consolidation reading is "the convexity shape is medication-state-dependent" (substantively interesting but does NOT modify the primary verdict).

- **§5.B dose-adjusted-predictor cross-phase test**: compute `all_day_stress_avg_adj(d) = all_day_stress_avg(d) - 0.57 × dose_plasma_mg(d)` per [`citalopram_phase_stratification §5.B`](../../../methodology/citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests) using the locked buildup-post-CPAP β. Re-bin and re-run the convexity test on the cross-phase pool (LC era through afbouw). **Reported as descriptive cross-phase replication**: invariance of the convex shape to the dose-adjustment is supportive of the structural claim; sign-flip of the convexity statistic is a §5.B mis-specification flag per the framework MD's tradeoff note.

**§5.C unmedicated-only restriction dispatch**: §5.A primary already IS effectively unmedicated-only at the headline level. §5.C is the same headline reading as §5.A with the cross-phase sensitivity layer dropped; we adopt §5.A's superset-framing so the secondary phases remain reportable as descriptive replication rather than discarded.

**Per-phase sample minimums**: each phase × 5-bin contingency requires ≥ 30 observations per bin to produce a descriptive bin-mean. Below this, the phase's read is **INCONCLUSIVE per §5.4** (mirrors HA-C4 v2 §5.4 inconclusive-bar pattern); INCONCLUSIVE does NOT halt the primary unmedicated test, only blocks reporting the secondary phase's bin-mean trajectory.

### 4.5 Statistical machinery (locked)

#### 4.5.1 Primary tests — three conditions (all on the unmedicated pool)

For the unmedicated × 5-bin × `gevoelscore` bin-mean trajectory `(m1, m2, m3, m4, m5)`:

**Condition (a) — Monotone decreasing**: **Jonckheere-Terpstra one-sided test** for monotone-decreasing trend across bins. H0: no trend across bins; H1: bins ordered B1 → B5 show monotone-decreasing `gevoelscore` distributions. Test statistic: standard Jonckheere-Terpstra `J*` standardised by the null SD; one-sided p-value via block-permutation at E[L]=7 (per §4.7 below). **Pass condition**: empirical one-sided p < 0.05 in the decreasing direction.

**Condition (b) — Convexity second-difference contrast**: compute the three second-differences of bin-means `Δ²_i = m_{i+1} - 2·m_i + m_{i-1}` for i ∈ {2, 3, 4}. The convexity statistic is the **mean** `S = (Δ²_2 + Δ²_3 + Δ²_4) / 3`. Under SUPPORTED (gevoelscore convexly decreasing in stress-bin) `S < 0` systematically. **One-sided block-permutation test at E[L]=7**: H0: `E[S] = 0`; H1: `E[S] < 0`. Empirical p-value computed from the null distribution of `S` under block-permutation of the `(date, all_day_stress_avg)` label sequence (keeping `gevoelscore` fixed in place); B = 10,000 resamples. **Pass condition**: empirical one-sided p < 0.05 AND `S < 0` (correct direction).

**Companion contrast vector for transparency**: report `c · m` where `c = (+1, +2, 0, -2, -1)` (single-degree-of-freedom convexity score, sum-to-zero, orthogonal to the linear contrast `(-2, -1, 0, +1, +2)`). Not part of the §5 verdict bar; reported in result.md.

**Condition (c) — Spline non-linearity test**: natural cubic spline regression of `gevoelscore = f(all_day_stress_avg)` with **4 internal knots placed at the bin boundaries (20, 30, 40, 60)**. Compare the full-spline model against the linear-only model via an F-test on the difference in residual sum of squares (degrees of freedom = number of non-linear basis terms = 3 for a natural cubic spline with 4 internal knots). **Pass condition**: F-test p < 0.05 AND visual inspection of the spline confirms convexity (concave-down with negative slope, equivalently: monotone-decreasing with negative second derivative across the support). Visual gating is operationalised via the **sign of the spline's second derivative at the bin midpoints**: pass requires negative second derivative at ≥ 3 of 5 bin midpoints. Reported as a numerical check, not subjective visual approval.

#### 4.5.2 Secondary descriptive outcomes (no verdict weight)

- **Bin-mean table** + 95% CI per bin (stationary bootstrap at E[L]=7 per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)) + per-bin n. The descriptive table is the read a human can interpret without inferential machinery; the §5 verdict is the formal closure.
- **Pairwise Mann-Whitney across adjacent bins** (B1↔B2, B2↔B3, B3↔B4, B4↔B5) with Holm step-down correction. Reports which specific bin-pair carries the discrimination; descriptive only. Note: 4 adjacent comparisons → Holm cutoffs α/4, α/3, α/2, α/1 at α = 0.05.
- **Companion contrast** `c · m` value with `c = (+1, +2, 0, -2, -1)` per §4.5.1 condition (b) note.
- **Linear correlation Spearman ρ** between `all_day_stress_avg` (continuous) and `gevoelscore` (continuous). **Reported as a sanity-check companion ONLY**: per the register, the C3 hypothesis *itself rejects linearity*; a positive-Spearman-but-failing-convexity result would mean "the relationship is roughly monotone-but-linear-or-concave" — i.e. against C3. The linear Spearman is the *opposing model* in disguise; reported for falsification-discipline.

### 4.6 Crash-drop sensitivity arm (locked; per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions))

Re-run the three primary tests (Jonckheere-Terpstra, second-difference contrast, spline non-linearity) with `is_crash == True` dropped from the unmedicated pool. Report the second-difference statistic `S` both on the full pool and on the crash-dropped pool. **Flag if `|Δ S|` crosses the convex/concave sign boundary** (i.e. full-pool `S < 0` but crash-dropped `S ≥ 0`, or vice versa). Per the §3.4 hook's purpose, the dependence is **informative-for-interpretation but does NOT modify the primary verdict** per §5: the C3 mechanism is expected to be strongest near crash days, so a strong crash-dependence is consistent with the claim (not against it).

**Sign-boundary flag firing** is the operationalisation of "the channel's signal is crash-driven" per §3.4 — surfaced in result.md as a finding for interpretation, alongside the primary verdict.

### 4.7 Block-permutation null at E[L] = 7 (locked, inherits from [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md))

For both Conditions (a) and (b) of §4.5.1, the empirical null distribution is generated by stationary bootstrap of the binary bin-label sequence:

1. Take the observed `(date, bin_label[d], gevoelscore[d])` tuples for the era-filtered unmedicated pool, sorted by date.
2. Generate B = 10,000 null draws: for each draw, resample the `bin_label` assignment via stationary bootstrap (geometric-distributed block lengths with mean E[L] = 7) while keeping `gevoelscore` fixed in temporal position. This preserves the within-`gevoelscore` autocorrelation and breaks the bin-label → gevoelscore relationship.
3. For each null draw, recompute (a) the Jonckheere-Terpstra `J*` and (b) the mean second-difference `S`. Build the empirical null distributions for each.
4. Empirical one-sided p-values: `p_a = (1 + #{J*_null <= J*_observed}) / (B + 1)` (one-sided decreasing); `p_b = (1 + #{S_null <= S_observed}) / (B + 1)` (one-sided convex).

**Seed**: `RANDOM_SEED = 20260622` (HA-C3 v1 seed; distinct from HA-C4 v2's `20260618` and HA-C4 v1's `20260617`).

**E[L]\* companion + factor-of-2 flag**: data-driven `E[L]*` estimator computed on the residuals from the linear `gevoelscore ~ all_day_stress_avg` fit (post-Z-score-of-residual ACF); flag if `|E[L]* - 7| / 7 > 0.5`. Per the methodology MD, the flag fires only on SUPPORTED verdicts; for PARTIAL or REJECTED, descriptive context only.

**Note on resampling target**: the permutation acts on the bin-label sequence (which inherits the temporal autocorrelation of `all_day_stress_avg` via its derivation), NOT on the `gevoelscore` sequence. This is the standard pattern for block-permutation under autocorrelated covariates: keep the outcome's serial structure intact and randomise the predictor's structural relationship to it.

### 4.8 Sensitivity arms reported alongside the primary (no verdict weight)

- **§4.4 §5.B dose-adjusted cross-phase**: per §4.4 above; report bin-means + convexity test on the cross-phase pool with the dose-adjusted predictor.
- **§4.4 within-consolidation replication**: per §4.4 above; report bin-means + convexity test within consolidation.
- **§4.6 crash-drop arm**: per §4.6 above.
- **Train+validate M3 overlay**: bin-means + second-difference statistic computed separately for train (2022-09-03 → 2023-12-31) and validate (2024-01-01 → 2024-04-08) sub-windows of the unmedicated pool. Reported as descriptive side-by-side; no per-portion verdict per [`train_validate_split_fate.md §5`](../../../methodology/train_validate_split_fate.md). **The overlay answers "is the primary single-pool verdict robust to era partition?" — NOT "does the convex shape change over time?"** per the train/validate fate MD's §5 number-not-narrative discipline.
- **§4.6 same-day vs t+1 lagged variant**: compute the same primary three conditions but with `gevoelscore[T+1]` as outcome (the same `all_day_stress_avg[T]` as predictor). Reported as descriptive cross-test alignment with PEM-pacing hypotheses; not promoted to primary.

### 4.9 Operationalisation choices (per pre-reg constraint #9; one sentence per dimension)

Per the Wiggers register's B-block + H-block constraint #9 (which applies generally to formal pre-regs):

- **Window selection**: per-day single-cell (the claim is about the *same-day* mapping); justified by C3's claim shape that has no temporal-window dimension.
- **Signal reduction**: predictor `all_day_stress_avg` is binned into 5 categories per §4.1 (the claim's "step appears very small on the graph, but it isn't" is *about* the step boundary); outcome `gevoelscore` stays continuous (the gevoelscore granularity 1-10 is already coarse).
- **Threshold choice**: bin boundaries are at the Wiggers-verbatim integer steps (0, 20, 30, 40, 60), NOT data-driven quintiles or equal-width 20-unit bins; justified by the source-verified anchor.
- **Test family**: Jonckheere-Terpstra monotonicity (rank-based, distribution-free) + second-difference contrast (the discrete analogue of the second derivative — the precise mathematical operationalisation of "marginal effect increases") + natural cubic spline (continuous-domain confirmation companion). Robust + distribution-free + shape-aware.
- **Verdict shape**: 3-condition gated SUPPORTED with PARTIAL fallback (2-of-3); REJECTED otherwise. Not a binary p-bar.
- **Temporal structure**: per-day same-day mapping; no temporal collapse beyond per-day default per [`time_resolution.md §6`](../../../methodology/time_resolution.md#6-the-discipline-rule).
- **Multi-channel**: single-channel test (Wiggers' C3 source claim is specifically about the daily-aggregate stress score → felt-fatigue mapping, not about a composite stress channel).
- **Functional form**: explicit convexity test via the second-difference contrast and the spline non-linearity test; the test *does NOT assume linearity* — it tests *against* linearity as the null.
- **Effect-size grounding**: bin-mean deltas between adjacent bins (in gevoelscore units 1-10) as the effect-size unit; the absolute deltas tell the human-interpretable size of the convex cost. Reference scale: the gevoelscore SD on the unmedicated pool (reported at dry-run for context).

## 5. Pre-registered falsification criterion (locked)

### 5.0 Multi-comparison discipline — single-cell headline lock

HA-C3 has **ONE headline verdict cell**: the unmedicated × 5-bin × `gevoelscore` × 3-condition gated outcome per §5.1 below. Every other arm — secondary phases (§4.4), dose-adjusted cross-phase (§4.8), crash-drop sensitivity (§4.6), t+1 lagged (§4.8), train/validate M3 overlay (§4.8) — is **descriptive sensitivity ONLY** and CANNOT promote to SUPPORTED on its own. Per [`hypothesis_lock_process §4.2`](../../../methodology/hypothesis_lock_process.md#42-layer-3-substantive--multi-comparison-discipline) Option (a) single-cell headline lock.

### 5.1 Verdict bar — 3-condition gated (locked)

A condition is **MET** when its test statistic passes the §4.5.1 pass condition (one-sided empirical p < 0.05 AND correct direction; for condition (c) additionally the spline-second-derivative sign check at ≥ 3 of 5 bin midpoints).

A condition is **NOT MET** when either: (i) the test p-value fails the bar, OR (ii) the test statistic is in the wrong direction (e.g. monotone-increasing rather than decreasing for condition (a); convex-up `S > 0` for condition (b); positive spline second derivative for condition (c)).

| outcome | condition status | verdict |
|---|---|---|
| (a) MET AND (b) MET AND (c) MET | all 3 met | **SUPPORTED** |
| Exactly 2 of {(a), (b), (c)} MET | 2-of-3 | **PARTIAL** |
| 0 or 1 of {(a), (b), (c)} MET | ≤1-of-3 | **REJECTED** |
| Any of the 3 conditions is in the WRONG DIRECTION (regardless of p-value) | wrong-direction firing | **REJECTED** |

**Wrong-direction-overrides-2-of-3 clause**: if condition (a) shows monotone-INCREASING (gevoelscore RISES with stress bin) the claim is structurally falsified regardless of whether (b) and (c) reach significance; reports REJECTED. Same logic for (b) `S > 0` (concave rather than convex) and (c) positive spline second derivative.

### 5.2 Inconclusive bar

A condition that cannot be evaluated because of structural sample-size shortfall (e.g. a bin has < 30 observations after §4.3) routes to **INCONCLUSIVE** for that condition. The 3-condition verdict is computed treating INCONCLUSIVE conditions as NOT MET for the SUPPORTED/PARTIAL/REJECTED count. **The dry-run sanity gate at §7.5 catches this case before the full run**: if any bin has < 30 observations, the test HALTS and a v2 redraft with revised bins is required.

## 6. Exclusion rules (locked)

- **LC era only**: days before `2022-04-04` are excluded (per [`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md)).
- **Unmedicated phase only (primary)**: days `>= 2024-04-09` are excluded from the primary unmedicated headline. Secondary §4.4 sensitivity arms include other phases.
- **April 2024 cluster (`2024-04-09 → 2024-04-16`)**: structurally unanalysable per [`citalopram_phase_stratification`](../../../methodology/citalopram_phase_stratification.md); excluded from all arms.
- **First 21 days of `has_garmin_uds=True` coverage**: per [Wiggers register I1](../../../wiggers_testable_hypotheses.md#i-data-quality--methodology-checks-not-about-your-body), the watch's first ~3 weeks are baseline-warmup-suspect. Sensitivity arm: re-run the primary with the first-21-days-dropped sub-pool; reported in result.md as descriptive companion only.
- **Pre-gevoelscore days (`< 2022-09-03`)**: the LC era starts 2022-04-04 but `gevoelscore` is NaN on those early LC days; §4.3 gate 5 absorbs this via the NaN-drop on `gevoelscore`.
- **Sentinel-filtered `all_day_stress_avg` dates** (the 2 dates the 2026-06-12 negative-sentinel filter dropped per DATA_DICTIONARY §7B): excluded via §4.3 gate 4.
- **Days with NaN on either column**: excluded via §4.3 gates 4-5.

## 7. Expected effect size if hypothesis is true

### 7.1 Bin-mean trajectory under SUPPORTED

Under SUPPORTED, the bin-mean `gevoelscore` trajectory across bins B1 → B5 should be:

- **Monotone decreasing**: `m1 > m2 > m3 > m4 > m5` (with monotonicity that need not be strict at each step but the Jonckheere-Terpstra trend must be significant per §5.1 (a)).
- **Convex (accelerating decrement)**: the step from B3 to B4 (mid → mid-high, across the Wiggers verbatim 30 → 40 boundary) is the load-bearing one; under SUPPORTED, `(m3 - m4)` is larger in magnitude than `(m1 - m2)` AND larger than `(m2 - m3)`. The (B4 → B5) step (mid-high → high) is expected to be the largest of all if SUPPORTED.

**Sanity-check expected ranges** (not pre-specified bin values, just envelope expectations the dry-run reads against):

- `m1` (low stress, 0-20): in the 5-7 range on the 1-10 gevoelscore scale (Garmin stress < 20 = "calm" → felt-OK days).
- `m5` (high stress, 60+): in the 2-4 range (Garmin stress > 60 = "stressed all day" → felt-bad days).
- Absolute spread `m1 - m5`: in the 2-5 gevoelscore-unit range (the convex-cost claim implies the spread exists, the convexity test answers *how* it accumulates).
- Mean second-difference `S` (per §4.5.1 (b)): expected in the range `[-0.5, -0.05]` if SUPPORTED (negative, but small in magnitude because gevoelscore varies on a 1-10 integer scale).

### 7.2 Sanity-check expected sample sizes

From the §4.3 gate calculation: the unmedicated-AND-gevoelscore pool starts 2022-09-03 → 2024-04-08, approximately 583 days before further exclusions (April 2024 cluster has only 0 days in this range — it's already past 2024-04-08; sentinel-filter drops ~0-1 dates). Expected effective n ≈ 555-580 days.

**Expected per-bin n on the unmedicated pool**: the descriptive marginal of `all_day_stress_avg` on this corpus is median in the 30s-40s per DATA_DICTIONARY annotations. A reasonable distribution expectation: B1 (0-20) ~50-100 days; B2 (20-30) ~150-200; B3 (30-40) ~150-200; B4 (40-60) ~100-150; B5 (60+) ~20-80. **The 60+ bin is the most-at-risk for the < 30 sanity gate per §4.1 + §5.2**; this is the load-bearing dry-run sanity check.

### 7.3 Sample-size sanity gates (§7.5 below)

The per-bin n must be ≥ 30 on the unmedicated pool for all 5 bins to produce a fully-resolved 3-condition test. If only the high bin (B5) falls below 30:

- **Halt option A** (preferred per the convexity claim's structure): redraft as HA-C3-v2 with B4 widened to absorb B5 (e.g. `[40, 100]` becomes the single high-stress bin); the convexity test reduces to 4 bins with 2 second-differences. The cost is the loss of the high-stress-tail-most-extreme reading where the convex cost is sharpest — explicit trade-off documented.
- **Halt option B**: continue with B5 INCONCLUSIVE per §5.2; the 3-condition test runs on the 4-bin reduction; report B5 descriptively. **NOT preferred**: drops the load-bearing high-tail reading.

The choice between A and B is a v2-time user decision; v1 HALTs at dry-run if the gate fires and reports the count.

### 7.4 Expected verdict-distribution shape

If the Wiggers C3 verbatim is **true** on this corpus, expect: **SUPPORTED** (all three conditions met). If the relationship is **monotone but linear**, expect: PARTIAL (condition (a) MET, (b) and (c) NOT MET). If the relationship is **monotone but concave** (decelerating decrement — opposite of C3), expect: REJECTED via the wrong-direction clause on (b). If there is **no monotone relationship at all** (e.g. flat or U-shaped), expect: REJECTED via condition (a) failure.

### 7.5 Sanity gate (HALT triggers at dry-run)

- **Gate 1 — sample size**: each of the 5 bins on the unmedicated pool has ≥ 30 observations. **HALT if any bin has < 30**; route to §7.3 halt option choice via v2 redraft.
- **Gate 2 — distribution sanity**: `all_day_stress_avg` median on the unmedicated pool falls in a plausible range. **HALT if the median is outside [20, 60]** (the descriptive expectation is in the 30s-40s; outside this range suggests a pipeline error or sentinel-filter regression). Per [`hypothesis_lock_process §5`](../../../methodology/hypothesis_lock_process.md#5-sanity-check-questions-before-lock) the §7-anchor-against-exact-column rule binds: this gate cites the `all_day_stress_avg` column's descriptive distribution at dry-run.
- **Gate 3 — gevoelscore overall distribution sanity**: `gevoelscore` median on the unmedicated pool falls in [3, 6] (the descriptive 1-10 scale with median typically in the 4-5 range per DATA_DICTIONARY §1 "in practice 1-6 dense"). **HALT if outside [3, 6]**.
- **Gate 4 — power-density**: across the 5 bins, at least 3 bins have ≥ 30 observations AND the total n ≥ 100 on the unmedicated pool. **HALT if total n < 100** (structural underpowering of the contrast).

If Gate 1, 2, 3, or 4 fails at dry-run → HALT → revise spec → HA-C3-v2 per [`hypothesis_lock_process §3.9`](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). **The dry-run report names the failing gate(s) explicitly.**

## 8. Caveats `result.md` must explicitly acknowledge

1. **Power-calc dispatch** (per [`hypothesis_lock_process §3.8 gate 1`](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc)): power calculation is **inapplicable per Daza 2018 within-subject design** ([Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) *Methods Inf Med*) — the n-of-1 corpus does not have separate treatment and control arms in the classical sense. The block-permutation null at E[L]=7 (§4.7) is the within-subject inferential machinery; the §5.1 3-condition gated verdict determines SUPPORTED/PARTIAL/REJECTED rather than asymptotic-power thresholds. INCONCLUSIVE per §5.2 is the operational definition of "underpowered for this cell" rather than a separate power computation.

2. **n=1 single-subject caveats** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-population-norm): thresholds in §5.1 (p < 0.05, second-difference sign, spline second-derivative sign at ≥ 3 of 5 midpoints) are calibrated against the participant's distribution. The block-permutation null is the within-subject inferential anchor; the 3-condition verdict band is the within-subject decision rule. No cross-subject generalisation is claimed.

3. **Citalopram-phase confound + chosen mitigation** per [`citalopram_phase_stratification §6`](../../../methodology/citalopram_phase_stratification.md#6-pre-registration-template-for-new-hypothesis-mds): the predictor `all_day_stress_avg` is dose-modulated at +0.57/mg per mg of plasma citalopram (v3 2026-06-14 confirmed). This hypothesis is tested **using treatment §5.A** per [`citalopram_phase_stratification §5`](../../../methodology/citalopram_phase_stratification.md#5-the-three-downstream-test-treatment-patterns). Treatment rationale: the C3 shape claim is well-defined within any single phase; the unmedicated phase is the Wiggers-prior-aligned headline because the participant's lived-experience phrasing predates citalopram. Within-phase results (primary unmedicated + secondary consolidation) are the primary read; cross-phase aggregation without treatment is not. The §5.B dose-adjusted predictor is reported as a cross-phase sensitivity arm per §4.4.

4. **Crash-day inclusion structural fragility** (per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions) + the audit-hook on this corpus where exertion × resting_hr Spearman swings from ~0 to ~+0.4 when crash-days drop): the convex-cost shape is expected to be **strongest on crash days** (high-stress bins disproportionately contain crash days); the §4.6 crash-drop sensitivity arm reports `S` on both the full pool and the crash-dropped pool. **A sign-boundary flag firing (full-pool `S < 0` but crash-dropped `S ≥ 0`) is informative for interpretation** — it means the convex cost is concentrated in the crash-day sub-pool rather than uniformly distributed across the unmedicated days. This does NOT modify the §5 verdict per the §3.4 hook design; it is surfaced as a finding for downstream interpretation.

5. **Within-subject shape, NOT between-subject prediction**: the convex stress→fatigue claim is about the **within-subject mapping** on this participant's corpus. No claim is made about how the shape generalises across people; the participant's per-day stress-to-fatigue function being convex is consistent with cross-subject heterogeneity in the mapping shape. Per the Wiggers register's framing, "absolute values are meaningless across people; for you they're meaningless across seasons and device changes too".

6. **No causal-direction inference**: the test answers "does the gevoelscore-vs-stress-bin mapping have a convex shape?" — it does NOT answer "does stress *cause* fatigue?" or "does fatigue *cause* stress?". The same-day correlation has neither a temporal-precedence anchor nor a counterfactual-intervention design (per [`citalopram_dose_response`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) the citalopram-traject IS a within-subject intervention on the stress channel, which the §4.4 §5.B sensitivity arm leverages — but the primary §5.A unmedicated test does not have a within-day intervention design). Per [CONVENTIONS §4.1-§4.3](../../../CONVENTIONS.md#4-statistical-discipline) the test is a *descriptive characterisation of the mapping shape*, not a causal mechanism claim.

7. **Wiggers' phrasing is qualitative**: the verbatim source "a day with a score of 40 is much more tiring than a day with a score of 30" + "stair step" is qualitative. Our binning (0-20, 20-30, 30-40, 40-60, 60+) is one operationalisation of the stair-step framing; the verbatim does not specify these exact bins (per the [verification log](../../../wiggers_testable_hypotheses.md#c3--non-linear--convex-stressfatigue) note "the binning is OUR choice, not Wiggers'"). A REJECTED verdict on these specific bins does not falsify the qualitative Wiggers framing universally; it falsifies it on **this specific operationalisation** per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no).

8. **Independent-obligations block** (per [`citalopram_phase_stratification §6`](../../../methodology/citalopram_phase_stratification.md#6-pre-registration-template-for-new-hypothesis-mds) "Independent obligations" — adopting §5.A does NOT relieve the test of):
   - **Autocorrelation handling**: handled via §4.7 block-permutation at E[L]=7 + data-driven E[L]\* companion.
   - **Crash-drop sensitivity** per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions): handled via §4.6.
   - **Spike-detecting metrics where applicable** per [CONVENTIONS §3.5](../../../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages): the C3 claim is structurally about the daily-aggregate stress channel (Wiggers' "annual stress overview score line"); the per-day-mean operationalisation IS the source-faithful read. **No spike-companion required.** Spike-companion testing belongs to HA-C4 / HA-C4b / HA11 which are within-day shape tests; HA-C3 is the cross-day-aggregate shape test.
   - **Trajectory-detrend sensitivity** per [CONVENTIONS §3.7](../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons): not applicable — this is not a pre-vs-post comparison.

9. **Drafting context disclosure**: this v1 was drafted in a fresh worktree-isolated session 2026-06-22 per the handoff brief. The drafter has not inspected the joint `all_day_stress_avg` × `gevoelscore` distribution beyond the marginal coverage stats per DATA_DICTIONARY (per the Authorship block "Data exposure context" disclosure). Per [`hypothesis_lock_process §3.2`](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) drafting permitted; the audit step is a separate fresh-session pass.

10. **Sister-test cross-references** (informational): HA-C4 v2 REJECTED at daily-aggregate (recovery-dynamics triad collapsed at daily resolution); HA11 SUPPORTED on train (within-day U-dip count). HA-C3's primary cell is structurally distinct from both: shape-of-cross-day-aggregate-mapping, not within-day-recovery and not within-day-dynamics. No prior import.

## 9. What we do with each outcome

### 9.1 SUPPORTED (3 of 3 conditions MET)

The Wiggers C3 verbatim claim is **empirically confirmed on this corpus**: same-day `all_day_stress_avg` maps onto `gevoelscore` with a monotone-decreasing AND convex shape. **Downstream implications**:

- **High-stress days carry disproportionate cost**: a 30→40 stress step costs more gevoelscore than a 20→30 step, in line with the Wiggers verbatim. Analytical consequence: stress-budgeting models for pacing-behaviour analyses should treat the high-stress register as carrying convex (not linear) cost; budget-allocation heuristics that linearly weight stress-units are mis-specified for this participant.
- **Cross-test reading**: the convex shape is consistent with the autonomic-dysregulation-as-load-amplifier reading from the H02b stress-spike count + HA06b RHR z-score + HA11 U-dip count SUPPORTED-on-train cluster. The same-day mapping shape would join those four as the cross-day-aggregate complement of the within-day-shape sister channels.
- **No causal direction claim** per §8 caveat 6; the convex *mapping* is established, the convex *mechanism* (stress causes fatigue convexly, vs fatigue causes stress convexly, vs both reflect a third variable convexly) is left for downstream investigation.

### 9.2 PARTIAL (2 of 3 conditions MET)

The C3 claim shows partial signal. Three operationally distinguishable PARTIAL configurations:

- **(a) + (b) MET, (c) NOT MET**: monotone + second-difference convex, but the natural-spline non-linearity test fails. The convexity is detectable at the bin-aggregate resolution but not at the continuous-domain spline resolution — likely because the discretisation amplifies a noisy underlying continuous mapping. The convex-cost reading is *partially supported*; downstream interpretation is "the bin-step framing of Wiggers' verbatim is detectable but the continuous-domain claim is not."

- **(a) + (c) MET, (b) NOT MET**: monotone + spline non-linear, but the second-difference contrast fails. The spline detects non-linearity but the specific shape is not cleanly convex via the bin-second-difference test — possibly the shape is convex in some regions and concave in others (a "wavy" non-linearity). Report the spline shape descriptively; downstream interpretation is "non-linear-but-not-cleanly-convex" — the C3 claim is partially confirmed in that the linear-only model is rejected, but the specific convex framing is not.

- **(b) + (c) MET, (a) NOT MET**: convex second-difference AND spline non-linear, but the monotonicity test fails. **This configuration is structurally suspect** — if the mapping is not monotone, the convexity test is interpreting noise as convex shape. Report descriptively but flag the configuration as inferentially-unstable; downstream interpretation is "the mapping is non-monotone in a way the contrast machinery is picking up as convex" — likely needs a v2 redraft with different operationalisation.

PARTIAL is descriptively informative but does NOT carry the SUPPORTED-bar weight for downstream pacing-behaviour analytic claims.

### 9.3 REJECTED (≤ 1 of 3 conditions MET; or any wrong-direction firing)

The C3 verbatim claim is NOT empirically confirmed on this corpus at the chosen operationalisation. Three distinguishable REJECTED configurations:

- **Wrong-direction (a) firing**: gevoelscore RISES with stress bin (monotone-increasing). This would be substantively surprising and likely indicates a data-direction issue (e.g. gevoelscore-coding inverted at some sub-window); investigate before treating as a research finding.

- **Wrong-direction (b) firing**: `S > 0` (concave / decelerating decrement). Substantive interpretation: the stress→fatigue mapping is monotone-decreasing but the decrement is *largest in the low-to-mid stress register and smaller at high stress* — i.e. the *opposite* of the Wiggers stair-step. Downstream implication: a "law of diminishing returns" on stress-cost on this corpus, where the first stress-units cost the most felt-fatigue and additional stress-units add proportionally less. This would be informative against the Wiggers C3 verbatim and toward a different cost-shape model.

- **0 or 1 conditions MET, no wrong-direction firing**: the mapping is roughly linear-or-flat. Downstream interpretation: the linear Spearman ρ (§4.5.2 companion) is the appropriate descriptive read; the Wiggers stair-step framing does not operationalise cleanly at the daily-aggregate resolution on this corpus.

REJECTED is informative against the Wiggers C3 verbatim; would mean linear-or-near-linear stress→fatigue mapping on this corpus at the daily-aggregate resolution. **Cross-reference downstream**: HA-C3 REJECTED + HA-C4 v2 REJECTED would mean the Wiggers C-family at daily-aggregate is exhaustively-tested-and-not-supported on this corpus, which is itself a substantive finding. A bout-level reframing (analogous to HA-C4c queued in the methodology MDs) would be the next-resolution operationalisation.

### 9.4 Sensitivity-arm divergences (descriptive interpretation, no verdict modification)

- **§4.4 §5.B dose-adjusted cross-phase signals convex while primary unmedicated signals REJECTED**: the convex shape is medication-modulated; the dose-adjusted predictor recovers the shape that the unmedicated phase alone could not. Substantively interesting; surface as a finding for downstream investigation. Does NOT promote to SUPPORTED.

- **§4.4 within-consolidation replication signals convex while primary unmedicated signals REJECTED**: similar to above; the shape is medication-state-dependent. Reportable; does NOT promote.

- **§4.6 crash-drop sign-boundary flag fires**: the convex cost is crash-driven. Per §8 caveat 4, this is informative-for-interpretation per the §3.4 hook design.

- **§4.8 train+validate M3 overlay divergence**: per [`train_validate_split_fate.md §5`](../../../methodology/train_validate_split_fate.md), "divergence is a number, not a narrative." Report the per-era second-difference values without interpretive overlay; the design cannot adjudicate effect-strengthening-over-time vs sampling variation.

- **§4.8 t+1 lagged variant signals convex while same-day primary signals REJECTED**: the convex cost is t+1 displaced. Substantively interesting; surface as a finding for cross-test alignment with HA-C4 and HA-P7. Does NOT promote.

### 9.5 Dry-run halt (per §7.5)

- **Gate 1 (per-bin n < 30) fails**: HALT + redraft per §7.3 halt option A or B per user choice.
- **Gate 2 (distribution sanity on `all_day_stress_avg`) fails**: HALT + investigate pipeline / sentinel-filter regression; redraft if data state requires.
- **Gate 3 (distribution sanity on `gevoelscore`) fails**: HALT + investigate gevoelscore export pipeline.
- **Gate 4 (total n < 100) fails**: HALT + redraft with widened phase scope (e.g. §5.B dose-adjusted cross-phase becomes primary). Substantive structural change.

## 10. Detection script architecture

### 10.1 Stage 1 — data (already done)

Both columns are in `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. No new extraction needed.

### 10.2 Stage 2 — test (`HA-C3/test.py`, to be written post-lock in a separate session)

The script:

1. Loads `per_day_master.csv`.
2. Applies §4.3 day-validity gate (LC era + unmedicated phase + April 2024 cluster exclusion + non-NaN both columns).
3. Bins `all_day_stress_avg` per §4.1 (5 left-inclusive bins).
4. Runs §7.5 sanity gates 1-4 at dry-run → HALT on failure.
5. Computes the three primary conditions per §4.5.1:
   - (a) Jonckheere-Terpstra one-sided trend test.
   - (b) Second-difference contrast `S` + one-sided block-permutation null at E[L]=7 (B = 10,000).
   - (c) Natural-cubic-spline regression with 4 knots at (20, 30, 40, 60); F-test on non-linearity; spline-second-derivative sign at bin midpoints.
6. Computes the §4.5.2 secondary descriptive outcomes (bin-mean + CI, pairwise Mann-Whitney + Holm, companion contrast, Spearman ρ).
7. Computes the §4.6 crash-drop sensitivity (re-run primary on `is_crash == True`-dropped pool; sign-boundary flag).
8. Computes the §4.8 sensitivity arms (§5.B dose-adjusted cross-phase, within-consolidation replication if n ≥ 30 per bin, train+validate M3 overlay, t+1 lagged variant).
9. Computes the §4.7 data-driven E[L]\* + factor-of-2 flag.
10. Applies the §5.1 3-condition verdict bar → SUPPORTED / PARTIAL / REJECTED.
11. Emits `result.md` + `result-data.json` per §10.3 template.

**Seed**: `RANDOM_SEED = 20260622` (HA-C3 v1).

### 10.3 Stage 3 — `result.md` template

Reports the §5.1 verdict at top (one cell: the 3-condition outcome + SUPPORTED/PARTIAL/REJECTED band), followed by:

- The per-bin descriptive table (n, bin-mean, 95% CI, mean second-difference, spline non-linearity F-stat + p).
- Per-condition (a)/(b)/(c) outcomes (statistic value, empirical p, pass/fail).
- The §4.5.2 secondary descriptive outcomes (pairwise Mann-Whitney + Holm; linear Spearman ρ as opposing-model sanity check).
- The §4.6 crash-drop sensitivity table (full vs crash-dropped second-difference; sign-boundary flag status).
- The §4.4 secondary phase reads (consolidation replication; §5.B dose-adjusted cross-phase) — descriptive only, no verdict.
- The §4.8 sensitivity arms (train+validate M3 overlay per-era; t+1 lagged variant; first-21-days-dropped per §6 device-baseline-warmup).
- The §4.7 data-driven E[L]\* + factor-of-2 flag status.
- Caveats per §8 (all 10).
- The §7.5 dry-run gate results table (which gates fired or passed).

### 10.4 Run protocol

1. **Dry-run** (`python test.py --dry-run`): prints per-bin sample sizes + descriptive distribution of `all_day_stress_avg` and `gevoelscore` on the unmedicated pool + the §7.5 sanity gate evaluations. **If any of Gate 1-4 fails → HALT + revise spec → HA-C3-v2.**
2. **Full run** (`python test.py`): emits `result.md` + `result-data.json` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-C3-v2 with the v1 spec archived.

### 10.5 Reproducibility

- `RANDOM_SEED = 20260622` locked at draft time.
- B = 10,000 block-permutation resamples for all permutation p-values.
- Stationary bootstrap (geometric-distributed block lengths with mean E[L] = 7) for CI per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md).
- Holm step-down at α = 0.05 for the pairwise Mann-Whitney secondary (per §4.5.2).
- All inputs sourced from `per_day_master.csv`; no derived in-script columns beyond bin label assignment and the `_adj` dose-adjusted column for §5.B sensitivity.

---

*Pre-registration drafted 2026-06-22 by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default) per the session handoff brief `session-HA-C3-pre-reg-drafting-handoff-2026-06-22.md`. **Status: drafted, not locked.** The fresh-session [§3.4 audit](../../../reviews/) is the next stage of the lock arc per [`hypothesis_lock_process.md §3.4`](../../../methodology/hypothesis_lock_process.md#34-audit-step-step-2-of-the-arc). Lock requires user acceptance + audit clearance + the four §3.8 gate confirmations (power-calc dispatch + single-cell headline lock + register-row pointer + re-audit-clean-or-compressed).*
