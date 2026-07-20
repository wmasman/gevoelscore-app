# Q24 MD-alpha Stage D descriptive audit -- phase-stratified pacing + dose-response

**Status**: **DRAFT r1 2026-07-20**, awaiting fresh-session `/research-methodology-review` before r1 LOCK. See section 16 lock log.

**Anchor MD**: [`methodology/post_heavy_day_pacing_learning.md`](../../methodology/post_heavy_day_pacing_learning.md) (MD-alpha, LOCKED r1 2026-07-16), which extends parent [`methodology/post_heavy_day_compensatory_rest.md`](../../methodology/post_heavy_day_compensatory_rest.md) (LOCKED r1, commit `58b7723`) by adding two stratification axes on the identical trajectory machine.

**Precursor**: [`Q24-mdalpha-precursor-phase-intensity/audit.md`](../Q24-mdalpha-precursor-phase-intensity/audit.md) (LOCKED r1 2026-07-16) -- the data-availability + sample-floor probe this audit executes against.

**Data source**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` (fallback `C:/Users/Gebruiker/Documents/gevoelscore-data`); LC-era stratum n=1524 rows (2022-04-04 to 2026-06-05).

**Random seed**: `20260720` (per-analysis, MD-alpha Stage D).

**Reproducibility**: [`scripts/stage_d_phase_intensity.py`](scripts/stage_d_phase_intensity.py) -- idempotent, no CLI args, single entry point. Imports the parent Wave-1 trajectory machinery verbatim (no re-derivation per MD-alpha section 2). Outputs in [`output/`](output/) (gitignored per `docs/research/**/*.csv`; regenerable): `availability.csv`, `prewindow_levels.csv`, `phase_trajectory_summary.csv`, `rescue_metrics.csv`, `doseresponse_summary.csv`.

**Discipline scope**: CONVENTIONS [`section 2.1`](../../CONVENTIONS.md#21-descriptive-before-inference) descriptive-before-inference + [`section 2.5`](../../CONVENTIONS.md) parsimony (a well-powered-or-underpowered null is a result); [`section 4.2`](../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing; [`section 3.7`](../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) trajectory-detrend. Descriptive-before-theory: NO `resilience_latent_state.md` citation; no latent-state / R(t) / reserve / buffer / envelope-capacity constructs. Findings framed as "does not support" / "consistent with", never "falsifies" / "validates" / a verdict label.

**Cross-refs**: MD-alpha sections 3, 4, 6, 7; parent MD sections 3.5, 4.1, 5.2, 7.1-7.11; precursor sections 2, 3, 5, 8; memories `project_garmin_research_bias_boundary`, `project_rest_day_operand_semantics`.

---

## 1. Authorship

Producer-mode Stage D descriptive audit per CONVENTIONS section 1.1, drafted 2026-07-20 by Claude (Opus 4.8) under user authorisation (Willem). Fresh-session `/research-methodology-review` before r1 LOCK is the peer-review discipline mirror to the two locked `Q24-mdbeta-stageD-*` audits. This audit executes a fully pre-committed design: MD-alpha (LOCKED r1) fixed every operand, window, direction pre-commit, rescue metric, and confound caveat before any Stage D result existed, so nothing here is a post-hoc design choice (descriptive-before-inference preserved at the MD-lock level).

---

## 2. Frame + method summary

**Two arcs on the parent trajectory machine** (all machinery inherited verbatim, MD-alpha section 2):

- **Sub-part 3 -- phase-stratified pacing** (MD-alpha section 3): the `recovery_phase` ordinal axis (`lc_pre_ergo` < `pacing_pre_citalopram_learning` < `pacing_habit_established` < `citalopram_modulated`); each phase's heavy-episode-end trajectory read against its own within-phase matched-ordinary comparator; headline is the late-pair (`pacing_habit_established` + `citalopram_modulated`) vs early-pair (`lc_pre_ergo` + `pacing_pre_citalopram_learning`) |AUC| contrast, plus the section 3.5 rescue metric on the 4-phase axis.
- **Dose-response** (MD-alpha section 4): intensity strata (very_heavy vs heavy episode-end, by last-day `exertion_class_lagged_lcera`) on the compensatory-success pool; |AUC| + slope contrast.

**Inherited machinery** (parent MD, imported not re-derived): episode-end = gap=0 contiguous heavy run last day; matched-ordinary comparator (not heavy + no heavy in [D, D+w] + no crash in [D, D+w] + valid outcome, recomputed per outcome); nine trajectory summary stats (per-d+k mean, delta = trigger - comparator, AUC, slope, peak, RTBT, below-baseline count, variability, first-crossing); `linear_detrend_on_pre` (30d pre-window linear extrapolation subtracted, raw + detrended side-by-side); bootstrap B=10,000, block-length 1, percentile CI [2.5, 97.5]; zero-vs-NaN (never `.fillna(0)`).

**Outcome family** (MD-alpha section 3.2, primary): the four activity axes `total_steps`, `effective_exertion_min`, `vigorous_min`, `active_min` (all direction-sign -1: below phase-matched-ordinary is the compensatory direction, parent section 7.7). Sleep / autonomic / subjective channels are out of primary scope for MD-alpha and not computed here.

**Direction pre-commits**:
- Sub-part 3 (MD-alpha section 3.4): compensation magnitude STRENGTHENS across phases, i.e. `|AUC_late_pair| > |AUC_early_pair|` and Spearman rho of |AUC| on the 4-phase ordinal axis >= +0.50 (rescue-eligible). Opposite-direction findings are sign-inversion findings in their own right, not silently inverted.
- Dose-response (MD-alpha section 4.4): `|AUC_very_heavy| > |AUC_heavy|` (compensation scales with load).

**Windows / overlaps / pools**: windows +3d, +5d, +10d; overlaps strict-clean + inclusive side-by-side (parent section 5.2); pools compensatory-success (primary) + compensatory-failure (sub-arm). Compensatory-success is the primary read for both arcs.

**Sample-floor tiers** (precursor section 5 / parent section 7.10): n >= 10 bootstrap-CI viable; 5 <= n < 10 descriptive-only (point estimate, no CI); 1 <= n <= 4 narrative-only; n = 0 structurally unavailable (emits NaN, never zero).

**Naming discipline** (MD-alpha section 3.6, load-bearing): every sub-part 3 finding is named **phase-stratified**, never "learned-pacing". The `citalopram_modulated` phase is 100% temporally aligned with post-citalopram-onset (2024-04-09); the phase axis bundles behavioural learned-pacing with citalopram-modulation, envelope drift, tactical-Garmin-use improvement, seasonality, and aging (a five-plus-confound bundle, section 11). No design here separates them at n=1.

---

## 3. Availability + sample-floor probe

Reproduced from [`output/availability.csv`](output/availability.csv) + [`output/phase_trajectory_summary.csv`](output/phase_trajectory_summary.csv). All values reproduce the precursor / MD-alpha anchors byte-for-byte (the circularity / reproduction check).

**Corpus**: LC-era rows 1524; gap=0 heavy-episode-ends 314. Both reproduce precursor section 1.

**Heavy-episode-ends per phase** (reproduces MD-alpha section 3.1 + precursor section 2):

| Phase | episode-ends |
|---|---:|
| `lc_pre_ergo` | 19 |
| `pacing_pre_citalopram_learning` | 12 |
| `pacing_habit_established` | 125 |
| `citalopram_modulated` | 158 |
| **All** | **314** |

**Intensity x phase** (reproduces precursor section 3 / MD-alpha section 6.3): heavy 8 / 4 / 70 / 83 = 165; very_heavy 11 / 8 / 55 / 75 = 149.

**Primary-contrast cell counts** (strict-clean, +3d, compensatory-success, per phase; reproduces precursor section 5.1): 6 / 3 / 41 / 59 = 109. Pooled: early-pair n=9, late-pair n=100.

**Sample-floor consequence (load-bearing)**: the two early phases (n=6, n=3) sit below the n=10 bootstrap floor at +3d strict-clean success, and the **early-pair remains below floor even pooled (n=9)**. The late-pair (n=100) is comfortably bootstrap-viable. At +5d the per-phase strict-clean success counts fall to 4 / 2 / 11 / 26 (only the two late phases viable); at +10d to 1 / 0 / 1 / 9 (only `citalopram_modulated` non-trivial, and `pacing_pre_citalopram_learning` = 0, structurally unavailable). Consequently the headline late-vs-early |AUC| contrast has a bootstrap-viable late arm but an early arm that is descriptive-or-narrative at best; the rescue metric (section 6) is undefined at +5d/+10d for outcomes where any phase is n=0.

---

## 4. Level-vs-change companion (mandatory, MD-alpha section 3.5 / precursor section 8)

Pre-window (30d) mean level per phase on all episode-ends, from [`output/prewindow_levels.csv`](output/prewindow_levels.csv). Reproduces precursor section 8 locked numbers byte-for-byte. **This table governs the interpretation of every phase |AUC| contrast below**: a phase |AUC| difference can be an absolute-envelope shift rather than a change in compensation.

| Outcome | `lc_pre_ergo` | `pacing_pre_cital` | `pacing_habit` | `citalopram_mod` | early-pair | late-pair |
|---|---:|---:|---:|---:|---:|---:|
| `total_steps` | 6479.83 | 5499.54 | 5174.43 | 4816.36 | 6100.37 | 4974.52 |
| `effective_exertion_min` | 9.50 | 27.78 | 19.39 | 5.17 | 16.58 | 11.45 |
| `vigorous_min` | 2.17 | 0.58 | 1.25 | 1.04 | 1.55 | 1.14 |
| `active_min` | 117.91 | 92.98 | 93.16 | 91.43 | 108.26 | 92.20 |

**Descriptive read**: `total_steps` pre-window level declines monotonically across phases (6480 -> 4816); the early phases sit on a substantially higher absolute-activity envelope than the late phases. `effective_exertion_min` is non-monotone with a `pacing_pre_citalopram_learning` outlier (27.78) -- a substantive envelope shift, not small-n mean inflation (precursor section 9.7 item 4). `active_min` and `vigorous_min` are near-flat with an early-phase high point. The declining `total_steps` envelope means an early-phase episode-end can drop further below its comparator than a late-phase one can, purely from the higher starting level -- a level-vs-change ambiguity that the phase |AUC| contrast cannot resolve on its own (section 5.3).

---

## 5. Sub-part 3: phase-stratified trajectory contrast

Primary cell: strict-clean, +3d, compensatory-success, raw arm. |AUC| of the delta trajectory (delta = trigger - phase-matched-ordinary), from [`output/phase_trajectory_summary.csv`](output/phase_trajectory_summary.csv). Bootstrap 95% CI on AUC reported where n >= 10; below-floor cells carry no CI.

| Outcome | `lc_pre_ergo` (n=6) | `pacing_pre_cital` (n=3) | `pacing_habit` (n=41) | `citalopram_mod` (n=59) | early-pair (n=9) | late-pair (n=100) |
|---|---:|---:|---:|---:|---:|---:|
| `total_steps` |AUC| | 3212.6 | 299.1 | 201.4 [-1147,1558] | 286.3 [-1039,456] | 3327.3 | **7.5 [-669,657]** |
| `effective_exertion_min` |AUC| | 8.8 | 23.4 | 9.4 [2,18] | 0.3 [-2,1] | 2.5 | 5.4 [2,9] |
| `vigorous_min` |AUC| | 6.5 | 0.3 | 0.2 [-1,0] | 0.3 [-1,-0] | 6.0 | 0.2 [-0,0] |
| `active_min` |AUC| | 28.4 | 15.0 | 2.2 [-29,24] | 0.7 [-17,19] | 35.6 | 3.3 [-11,18] |

(Below-floor cells -- both early phases and the early-pair -- are point estimates without CIs per the sample-floor tier; `pacing_pre_citalopram_learning` at n=3 is narrative-only.)

**5.1 Descriptive observation (headline)**. The MD-alpha section 3.4 pre-commit is `|AUC_late_pair| > |AUC_early_pair|` (compensation strengthens over phases). The observed ordering is the **opposite** on three of four activity outcomes: `total_steps` (early-pair 3327 vs late-pair 7.5), `vigorous_min` (6.0 vs 0.2), and `active_min` (35.6 vs 3.3) all show early-pair |AUC| far exceeding late-pair |AUC|. Only `effective_exertion_min` shows late-pair (5.4) exceeding early-pair (2.5), and there the early-pair AUC sign is positive (+2.5, trigger above comparator), inverted from the compensatory direction. Per MD-alpha section 3.4 this is a **sign-inversion finding reported in its own right**, not silently re-read as support.

**5.2 Descriptive observation (sample-floor)**. The early-pair |AUC| values that drive the ordering rest on below-floor arms: `lc_pre_ergo` n=6 (descriptive-only), `pacing_pre_citalopram_learning` n=3 (narrative-only), early-pair n=9 (below floor, no CI). The single largest number in the table (`total_steps` early-pair |AUC| 3327) is carried almost entirely by the n=6 `lc_pre_ergo` cell (|AUC| 3212). The late-pair |AUC| values (n=100) carry bootstrap CIs, all of which include 0 for `total_steps` ([-669, 657]), `active_min` ([-11, 18]), and `vigorous_min` ([-0, 0]); only `effective_exertion_min` late-pair excludes 0 ([2, 9], positive/inverted). NEEDS-MORE-DATA on the early arm is the binding constraint on any late-vs-early magnitude claim.

**5.3 Descriptive observation (level-vs-change)**. The early > late |AUC| ordering on `total_steps` co-occurs with the monotone-declining pre-window envelope (section 4: early-pair level 6100 vs late-pair 4974). An early-phase episode-end sits ~1100 steps/day higher pre-window and can therefore drop further below its comparator in absolute terms, independent of any change in pacing behaviour. The section 4 companion is exactly the MD-alpha section 3.4 alternative reading made concrete: early-phase compensation magnitude may reflect a higher (and harder-limited) absolute envelope rather than weaker pacing, and late-phase near-zero |AUC| may reflect a lower envelope already close to phase-matched-ordinary. The contrast cannot separate these at Stage D.

---

## 6. Rescue metric (MD-alpha section 3.5)

Spearman rho of |AUC| on the 4-phase ordinal axis [1,2,3,4] + monotonicity-score (fraction of consecutive-phase-pair |AUC| increases, denominator 3), strict-clean success raw arm, from [`output/rescue_metrics.csv`](output/rescue_metrics.csv). Rescue call: rho >= +0.50 rescue-eligible; +0.20 <= rho < +0.50 weak-flag; rho < +0.20 no-rescue; undefined if any phase is missing.

| Window | Outcome | Spearman rho | monotonicity | call |
|---|---|---:|---:|---|
| +3d | `total_steps` | -0.800 | 0.33 | no_rescue |
| +3d | `effective_exertion_min` | -0.400 | 0.33 | no_rescue |
| +3d | `vigorous_min` | -0.400 | 0.33 | no_rescue |
| +3d | `active_min` | -1.000 | 0.00 | no_rescue |
| +5d | `effective_exertion_min` | -0.400 | 0.33 | no_rescue |
| +5d | `total_steps` / `vigorous_min` / `active_min` | -- | -- | undefined (phase n=0) |
| +10d | all four | -- | -- | undefined (phase n=0) |

**Descriptive observation**. At the only fully-defined window (+3d), all four activity outcomes have **negative** Spearman rho on the 4-phase ordinal axis (-0.80 to -1.00): |AUC| magnitude *decreases* across phases, the opposite sign to the section 3.4 rescue-eligibility threshold (rho >= +0.50). No outcome reaches rescue-eligible or weak-flag; the call is **no_rescue on every activity outcome**. Per MD-alpha section 3.5, the 36 raw-only-significant drift-entangled cells from the parent Wave-1 Stage D (section 9.1 caveat 9) are therefore **not rescued as pacing-learning signal** by the phase-stratified read: the cross-phase |AUC| trend does not strengthen in the pre-committed direction. Consistent with sections 5.2-5.3, this non-rescue is itself confounded by the below-floor early arms and the declining absolute envelope, so it does not establish the absence of a pacing-learning component either; it establishes that the four-phase |AUC| trend does not carry it in the pre-committed direction at descriptive-with-CI resolution.

---

## 7. Dose-response arc (MD-alpha section 4)

Intensity strata on the compensatory-success pool, strict-clean, from [`output/doseresponse_summary.csv`](output/doseresponse_summary.csv). Pool n=109 (very_heavy 46, heavy 63) at +3d; the MD-alpha section 4.1 table's 52 / 73 are strict-clean totals (success + failure), 46 / 63 are success-only. Pre-commit: `|AUC_very_heavy| > |AUC_heavy|`.

**+3d raw** |AUC| [bootstrap 95% CI]:

| Outcome | very_heavy (n=46) | heavy (n=63) | ordering |
|---|---|---|---|
| `total_steps` | 838.8 [-1741, 65] | 1738.8 [-2573, -912] | heavy > vh (opposite) |
| `effective_exertion_min` | 6.2 [+0.8, +11.9] | 1.6 [-2.1, +5.9] | vh > heavy, but AUC sign positive (inverted) |
| `vigorous_min` | 1.9 [-2.5, -1.3] | 1.6 [-2.2, -1.1] | vh > heavy (weak, both CIs exclude 0) |
| `active_min` | 0.6 [-20, +19] | 26.0 [-43, -8.5] | heavy > vh (opposite) |

**Descriptive observation**. The section 4.4 severity-scaling pre-commit is not descriptively supported on the primary activity outcomes at +3d. `total_steps` and `active_min` show the **opposite** ordering (heavy-triggered compensatory drop exceeds very_heavy-triggered, and only the heavy arm's CI excludes 0). `vigorous_min` shows a weak in-direction ordering (both arms negative, CIs exclude 0, magnitudes close). `effective_exertion_min` shows very_heavy > heavy but with a **positive** AUC sign (trigger above comparator), a sign-inversion from the compensatory direction. The +5d and +10d panels (n=16 / 5 very_heavy) reproduce the same pattern with wider CIs and, at +10d, below-floor very_heavy / heavy arms (descriptive-only). Per MD-alpha section 4.6 this is a descriptive characterisation, not a between-strata test; the reading axis is the |AUC| magnitude ordering, and it does not scale with load in the pre-committed direction on the primary outcomes.

---

## 8. Overlap-policy + detrend companions

**Overlap policy** (parent section 5.2): strict-clean + inclusive are both in [`output/phase_trajectory_summary.csv`](output/phase_trajectory_summary.csv) (`overlap` column). Inclusive admits more episode-ends into each arm at extended windows (it does not drop episode-ends with an intervening heavy day), which is the only route to non-trivial early-phase coverage at +10d; the strict-clean primary is preferred at +3d where both are viable. Overlap-policy divergence is itself Stage D discipline evidence (precursor section 5 item 5) and is not collapsed.

**Detrend companion** (parent section 7.11 / CONVENTIONS section 3.7): raw + detrended arms are both computed (`arm` column). Per precursor section 6, zero episodes drop from the >=15-valid-pre-window-point rule, so detrended-arm n = raw-arm n across all phase x outcome cells (coverage certified, not the linear-fit stationarity assumption -- given the section 4 monotone `total_steps` pre-window drift, the detrended read inherits the section 4 level-vs-change discipline). The detrended-arm |AUC| reads do not change the section 5-7 descriptive orderings.

---

## 9. Consolidated descriptive observations

1. **The phase-stratified pacing pre-commit is not supported at descriptive-with-CI resolution.** The late-vs-early |AUC| ordering is opposite on 3 of 4 activity outcomes (section 5.1), and the rescue metric is no_rescue with negative Spearman rho on all 4 outcomes at +3d (section 6). The 36 drift-entangled cells do not rescue as pacing-learning signal via the four-phase axis.
2. **The non-support is confounded three ways and cannot establish absence.** Below-floor early arms (early-pair n=9; section 5.2), a monotone-declining absolute-activity envelope (section 4), and the 100% citalopram temporal entanglement (section 11) each independently prevent attributing the negative |AUC| trend to any single mechanism.
3. **Dose-response severity-scaling is not supported on the primary outcomes** (section 7): steps and active-minutes show the opposite ordering, vigorous a weak match, effective-exertion a sign-inversion.
4. **Reproduction anchors all hold**: 1524 rows, 314 episode-ends, 19/12/125/158 phases, 8/4/70/83 + 11/8/55/75 intensity x phase, 6/3/41/59 primary-contrast cells, and the section 4 pre-window levels, all reproduce the locked precursor byte-for-byte.
5. **No verdict is emitted** (CONVENTIONS section 2.1). Whether the negative cross-phase |AUC| trend reflects (i) genuine absence of a compensation-strengthening effect, (ii) the declining absolute envelope, (iii) below-floor early-phase sparsity, or (iv) citalopram-onset entanglement is descriptive-open at Stage D; disambiguation is the MD-alpha section 3.6 downstream-design concern (within-citalopram re-split; pre-citalopram-only companion), not resolved here.

---

## 10. Confound status

- **Citalopram 100% temporal entanglement** (MD-alpha section 3.6): `citalopram_modulated` (n=158 episode-ends) is fully non-overlapping with the three pre-citalopram phases; every late-phase datum is also a post-citalopram-onset datum. The late-vs-early contrast cannot separate learned-pacing from citalopram-modulation. Reported as inherited caveat; the "phase-stratified" naming (never "learned-pacing") is the discipline enforcing this.
- **Five-plus-confound bundle** (MD-alpha section 3.6, memory `project_garmin_research_bias_boundary`): the phase axis conflates behavioural learned-pacing, citalopram, envelope drift, tactical-Garmin-use improvement, seasonality, and aging. No design here separates them at n=1.
- **Envelope drift / level-vs-change** (section 4): the monotone-declining `total_steps` envelope is load-bearing for the section 5 read and cannot be detrended away (the detrend companion inherits the same ambiguity).
- **Sample floor** (section 3): early phases below floor; the headline early-pair below floor even pooled. Reported as NEEDS-MORE-DATA on the early arm.
- **Physical-rest-only** (memory `project_rest_day_operand_semantics`): the activity outcomes measure physical activity only; no cognitive / emotional axis is implied.

---

## 11. Data-validity notes

Activity-outcome coverage is 100% on episode-end days across all phases (precursor section 4.1) and does not fall below the n<5 drop rule at any d+k (precursor section 4.2). The five structurally-unavailable cells flagged by precursor section 5.4 (early-phase / late-phase-failure strict-clean cells at extended windows) appear as NaN panels in the outputs, never zero-imputed (zero-vs-NaN discipline). No `.fillna(0)` anywhere.

---

## 12. Discipline compliance attestations

- **Descriptive-before-inference** (CONVENTIONS section 2.1): no inferential verdicts; bootstrap CIs are descriptive markers; all orderings framed "does not support" / "consistent with", never "falsifies" / "validates".
- **Parsimony** (CONVENTIONS section 2.5): the simplest descriptive read (phase-stratified + intensity-stratified |AUC| on the four activity axes) is reported as-is; the non-support + no-rescue is a result, not a failure, and no more complex model is fit to rescue it.
- **No re-derivation** (MD-alpha section 2): episode-end / comparator / 9-stat / detrend / bootstrap imported verbatim from the parent Wave-1 `audit.py` (sign_flipper_diagnostic.py import precedent); only the phase/intensity pre-filter, the inclusive-overlap variant, the rescue metric, and the level-vs-change companion are added here.
- **Phase-stratified naming** (MD-alpha section 3.6): "learned-pacing" is used nowhere as a finding label; the citalopram entanglement is named at every contrast.
- **Direction pre-commit + sign-inversion** (MD-alpha sections 3.4, 4.4; parent section 7.7): opposite-direction and sign-inverted findings reported in their own right, not silently re-read.
- **Sample-floor / NEEDS-MORE-DATA** (precursor section 5): tier per cell (bootstrap / descriptive / narrative / unavailable); below-floor cells carry no CI; n=0 cells emit NaN.
- **Level-vs-change companion** (MD-alpha section 3.5 / precursor section 8): per-phase pre-window levels reported alongside every |AUC| contrast; reproduces the locked precursor numbers.
- **Detrend companion** (parent section 7.11 / CONVENTIONS section 3.7): raw + detrended side-by-side.
- **Overlap-policy divergence** (parent section 5.2): strict-clean + inclusive both reported; not collapsed.
- **Reproduction / circularity check**: all precursor + MD-alpha anchors reproduced byte-for-byte.
- **Zero-vs-NaN** (parent section 11): never `.fillna(0)`.
- **Descriptive-before-theory** (user 2026-07-17 directive): no `resilience_latent_state.md` citation; no latent-state constructs.
- **No em-dash, no emoji** anywhere in this audit or the script.

---

## 13. Open inputs surfaced for orchestrator / reviewer

1. **Early-arm power**: the phase-stratified headline early arm is below floor even pooled (n=9). No within-corpus acquisition path closes this (the early phases are fixed historical windows). Fallback: report the late-pair alone as a within-late-era descriptive read, or route the early-vs-late question to a design that does not depend on the n=19 + n=12 early pools. Effort: S (report-only).
2. **Citalopram disambiguation**: the section 3.6 within-`citalopram_modulated` re-split (Priority 1) and pre-citalopram-only companion (Priority 2) are the named next arcs; neither is run here. Effort: M each. Blocks any learned-pacing-vs-citalopram interpretation at Stage S1.
3. **Level-vs-change**: the `total_steps` envelope decline is unresolved at Stage D; a level-conditioned or envelope-normalised operand would be a downstream design decision, not a Stage D fix. Effort: M.
4. **prob(heavy at d+k) outcome** (MD-alpha section 3.2): the categorical exertion-class-at-d+k companion outcome is not computed here (continuous activity axes only); a Stage D companion could add it. Effort: S.

---

## 14. Cross-references

- MD-alpha [`post_heavy_day_pacing_learning.md`](../../methodology/post_heavy_day_pacing_learning.md) sections 3 (phase axis, contrast, rescue), 4 (dose-response), 6 (cross-arc confounds), 7 (data-availability hooks).
- Parent [`post_heavy_day_compensatory_rest.md`](../../methodology/post_heavy_day_compensatory_rest.md) sections 3.5, 4.1, 5.2, 7.1-7.11, 11.
- Precursor [`Q24-mdalpha-precursor-phase-intensity/audit.md`](../Q24-mdalpha-precursor-phase-intensity/audit.md) sections 2, 3, 5, 8.
- Parent Wave-1 Stage D [`Q24-post-heavy-trajectory/descriptive_audit.md`](../Q24-post-heavy-trajectory/descriptive_audit.md) section 9.1 caveat 9 (the 36 drift-entangled cells this audit tests for rescue).
- CONVENTIONS sections 2.1, 2.5, 3.7, 4.2.

---

## 15. Lock log

| version | date | change |
|---|---|---|
| r1 DRAFT | 2026-07-20 | Initial producer-mode DRAFT. Executes MD-alpha (LOCKED r1) sub-part 3 phase-stratified pacing + dose-response against the LOCKED r1 precursor operand. Machinery imported verbatim from parent Wave-1 `audit.py` (no re-derivation); added: inclusive-overlap pool variant, phase/intensity pre-filters, section 3.5 rescue metric (Spearman rho + monotonicity), level-vs-change companion. Seed 20260720, B=10,000, block-length 1. Reproduces all precursor anchors byte-for-byte (1524 rows; 314 episode-ends; 19/12/125/158 phases; 8/4/70/83 + 11/8/55/75 intensity x phase; 6/3/41/59 primary-contrast cells; section 4 pre-window levels 6480/5500/5174/4816 total_steps + 9.50/27.78/19.39/5.17 effective_exertion). **Headline (descriptive-only)**: the section 3.4 phase-strengthening pre-commit is not supported -- late-vs-early |AUC| ordering opposite on 3 of 4 activity outcomes, rescue metric no_rescue with negative Spearman rho (-0.80/-0.40/-0.40/-1.00) on all four at +3d; the 36 drift-entangled cells do not rescue via the four-phase axis. Non-support confounded by below-floor early arms (early-pair n=9), monotone-declining absolute envelope, and 100% citalopram temporal entanglement -- does not establish absence. Dose-response severity-scaling not supported on primary outcomes (steps + active-min opposite, vigorous weak, effective-exertion sign-inverted). No verdict emitted. **Awaiting fresh-session `/research-methodology-review` before r1 LOCK.** |

---

*Producer-mode Stage D descriptive audit. Update when (a) the fresh-session review verdict lands and informs r1 LOCK compression, (b) a citalopram-disambiguation companion arc (MD-alpha section 3.6 designs) is authorised, (c) the prob(heavy at d+k) companion outcome is added.*
