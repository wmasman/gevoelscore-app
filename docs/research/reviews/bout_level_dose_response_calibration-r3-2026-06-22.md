# Review: Bout-level citalopram dose-response recalibration r3 — populated §6 inheritance table + result.md (custom 4-layer + PE.1-4)

**Targets**:
- Sub-MD: [`docs/research/methodology/bout_level_dose_response_calibration.md`](../methodology/bout_level_dose_response_calibration.md) — §6 populated table + §8 r3 status + r3 revision-log entry, at commit `d9c6fa4`.
- result.md: [`docs/research/analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration/result.md`](../analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration/result.md) (Authorship + §1-§8), at commit `d9c6fa4`.
- run.py: [`docs/research/analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration/run.py`](../analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration/run.py) (1211 lines), at commit `d9c6fa4`.
- External CSV (gitignored): `$GEVOELSCORE_DATA_PATH/unified/bout_level_dose_response_calibration_results.csv` — 189 data rows × 11 columns.
- STOCKTAKE.md §6 architectural-implications paragraph at commit `4589965` (Wave 3.5 refresh).

**Reviewer mode**: Claude (Opus 4.7) fresh-session producer-mode audit, NO shared drafting context per [CONVENTIONS §1.2](../CONVENTIONS.md). The recalibration was executed by a separate parallel-dispatched session; this audit reads cold.
**Authorising user**: Willem.
**Review date**: 2026-06-22.
**Skill not used**: `/research-review` is reviewer-mode-artefact only. The recalibration r3 is a producer-mode artefact (methodology MD + descriptive run), so this audit carries the 4-layer + PE.1-4 structure directly per the parent project pattern (`reviews/bout_level_recovery_dynamics-2026-06-19.md` + `reviews/phase_axis_collapsibility_conventions-2026-06-22.md`).

---

## §1 What the data shows (plain restatement)

The recalibration fit each of 7 features × 3 windows × 9 specs = **189 cells** per sub-MD §3 + §4. The headline empirical claim: at the §3.4 four-condition discriminative bar applied with buildup-post-CPAP as headline inheritance default per §3.5, **0 of 7 features reach CONFIRMED**. Three features land **weakly_consistent** at buildup-headline (`recovery_half_life`, `AUC_above_baseline`, `bout_n_fast_recovery_day`); four land **NULL** at buildup-headline (`peak_height`, `pre_bout_baseline`, `decay_slope`, `bout_n_per_day`).

**Per-feature buildup post-CPAP β (headline inheritance default per sub-MD §3.5; verbatim from CSV row `spec=primary`)**:

| feature | buildup β | CI95 | p | n_bouts | n_days | verdict |
|---|---:|---|---:|---:|---:|---|
| `peak_height` | −0.029 | [−0.937, +0.878] | 0.949 | 142 | 49 | NULL |
| `pre_bout_baseline` | +0.244 | [−0.399, +0.887] | 0.457 | 139 | 48 | NULL |
| `recovery_half_life` | +1.096 | [−0.217, +2.410] | 0.102 | 139 | 48 | weakly_consistent |
| `decay_slope` | +0.019 | [−0.060, +0.098] | 0.644 | 112 | 47 | NULL |
| `AUC_above_baseline` | +52.4 | [−49.5, +154.3] | 0.314 | 139 | 48 | weakly_consistent |
| `bout_n_per_day` | −0.020 | [−0.121, +0.081] | 0.698 | 50 | 50 | NULL (afbouw separately significant in wrong direction) |
| `bout_n_fast_recovery_day` | −0.056 | [−0.145, +0.034] | 0.223 | 50 | 50 | weakly_consistent |

**One substantive observation**: `bout_n_per_day` afbouw primary β=**−0.102 [−0.202, −0.002] p=0.045** sign-discordant with the +1 prior; CSV shows sign-discordance at all 7 sens cells (primary + 6 sens specs) for `bout_n_per_day × afbouw`; 5 of those 7 cells also have p<0.05 (primary + sens_B + sens_D + sens_E + sens_F), 2 do not (sens_A bootstrap p=0.068 + sens_C lagged-lcera p=0.084). Sub-MD §6 + commit message + STOCKTAKE §6 framing as "robust across 6 of 7" is the **count if "robust" means sign-discordance with p<0.10**; the more conservative p<0.05 count is 5/7 (sign-discordance alone is 7/7). Worth precision per L4.6.

**Architectural implication** (from STOCKTAKE §6 paragraph at lines 182-188 of `4589965`): Approach A relegated to sensitivity-arm status for downstream HA pre-regs at this corpus's bout-level n; HA-C4c primary becomes dose-naive; phase 5 ↔ phase 6 collapse permissible for bout-level work without §5.A/B/C inheritance violation; daily-aggregate CONFIRMED-citalopram channel binding remains intact (the recalibration says nothing at that layer).

**Interpretive frame** (per result.md §4 + sub-MD §6 net inheritance summary + STOCKTAKE §6): the level-vs-dynamics dichotomy of sub-MD §5.5 is NOT cleanly supported; the binding constraint is **bout-level n (~49 day-clusters/window in buildup-post-CPAP, ~75-78 in afbouw)**, not feature-by-feature heterogeneity. The verdict is the **underpowered-NULL framing** — "we cannot demonstrate per-bout dose-modulation at this n", NOT "we have demonstrated dose-naivety".

This §1 restatement preserves the underpowered-NULL nuance per [CONVENTIONS §4.2](../CONVENTIONS.md). The empirical claim ("0/7 CONFIRMED at the discriminative bar at this corpus n") is held distinct from the interpretive frame ("bout-level n is the binding constraint at this corpus, not citalopram bout-level pharmacology").

---

## §2 What fired and why

### Layer 1 — Universal reporting (SCRIBE 2016, STROBE 2007; CONVENTIONS §2.1, §2.2)

**L1.1 — Underpowered-NULL nuance preserved (PASS-with-strong-evidence).** The 0/7-CONFIRMED finding is reported in result.md §4 + sub-MD §6 net inheritance summary + STOCKTAKE §6 paragraph all with the explicit framing that "bout-level n is the binding constraint, not feature-by-feature heterogeneity". STOCKTAKE §6 line 182 uses the load-bearing phrase: *"The finding is properly framed as an underpowered-NULL at n≈49 day-clusters per window, NOT a definitive claim about citalopram's bout-level pharmacology."* Result.md §4 final paragraph: *"The honest verdict: the bout-level n is binding (effective n ≈ 49 day-clusters in buildup), and the per-bout features do not detect dose-modulation at the headline-precision the buildup window admits."* Sub-MD §8 r3 revision-log entry repeats this verbatim. Three-place framing-discipline consistency: clean. **This is the L4.7 big-call passing.**

**L1.2 — Result.md per-feature numerics vs CSV mismatches (MEDIUM-MAGNITUDE FIRE).** Operationalised measures (β, CI, p) should be defined with source-file traceability per CONVENTIONS §2.1; the CSV is the source-of-truth. Three mismatches between result.md §3 per-feature paragraphs and the CSV:

- **`recovery_half_life` afbouw β mismatch**: CSV row `recovery_half_life × afbouw_2026 × primary` says β=**+0.957** [−0.350, +2.264] p=0.151. Result.md §3 says β=**+0.564** [−0.213, +1.342] p=0.155. Neither the β nor the CI matches CSV. Sub-MD §6 table cell says β=**+0.564** [−0.213, +1.342] p=0.155 (matches result.md but NOT CSV). The mismatch is **substantive** (β differs by +0.39 min/mg ≈ 70% relative); the CI lower bound differs by +0.14 and upper bound by +0.92. Worth investigation: the +0.564 figure does not appear anywhere in the CSV's `recovery_half_life × afbouw_2026 × *` rows. (Closest CSV match: `recovery_half_life × buildup_post_cpap_2024 × sens_D_alt_lag` β=0.925 — also doesn't match; the +0.564 is unaccounted-for in the on-disk CSV.) Two-place inconsistency: result.md §3 ↔ sub-MD §6 agree with each other but BOTH disagree with the CSV. The §3.5 verdict (weakly_consistent) doesn't change under either β, so the inheritance assignment is unaffected; but the numeric mis-report is L1.2-blocking-for-traceability.

- **`AUC_above_baseline` afbouw β SIGN-FLIP**: CSV row `AUC_above_baseline × afbouw_2026 × primary` says β=**−20.5** [−112.2, +71.2] p=0.661 **`sign_match_prior=False`**. Result.md §3 paragraph for `AUC_above_baseline` says β=**+27.7** [−97.6, +153.1] p=0.661 explicitly framed as **"Sign-concordant with prior (+1) in BOTH windows"**. Sub-MD §6 table cell says β=**+27.7** [−97.6, +153.1] p=0.661 sign-concordant. The CSV says afbouw `AUC_above_baseline` is SIGN-**DIS**CORDANT with the +1 prior; result.md + §6 table say it's sign-concordant. This is a **substantive flip-of-direction misreport at two places** (result.md + §6). The buildup direction (+52.4) IS sign-concordant per CSV — so the buildup-headline verdict weakly_consistent stands — but the dynamics-vs-level read in result.md §4 implicitly leans on the "BOTH-windows-sign-concordant" framing on `AUC_above_baseline` to argue the composite-feature pattern, and that argument loses force if afbouw is actually sign-discordant. The CSV's sens A bootstrap CI for afbouw `AUC_above_baseline` is [−134.4, +54.8] also negative point estimate; sens_E crash-drop is β=−18.8 also negative; sens_D alt_lag β=−81.7 negative-significant-direction. Five of seven afbouw sens cells are sign-discordant; only sens_B + sens_F flip to positive. The dominant direction in afbouw on `AUC_above_baseline` IS negative, the OPPOSITE of result.md's claim. **Substantive misreport.**

- **`pre_bout_baseline` afbouw β minor mismatch**: CSV β=+0.452 [−0.059, +0.963] p=0.083. Result.md §3 + §6 table both say β=+0.452 [−0.059, +0.963] p=0.083. **Match.** (My earlier worry was unfounded.)

- **n_days minor inconsistencies**: result.md §1 windows table says afbouw n_days=78 + buildup n_days=50. CSV per-bout cells show n_days=49 for `peak_height × buildup`, 47-48 for other buildup per-bout features (day-clusters with at least one bout AND non-null dose); per-day aggregations are 50 + 77 (the 50 + 78 figures are days-in-window before bout-presence filtering — defensible but the result.md table cell does not distinguish n_days-in-window from effective day-cluster n that the cluster-robust SE uses). Result.md §3 `peak_height` paragraph also conflates: "buildup β = -0.029/mg" cites n=49 day-clusters which matches `peak_height × buildup × primary` n_days=49 — consistent on that row. Sub-MD §6 table and STOCKTAKE §6 paragraph use "n≈49 day-clusters/window" which is the right (effective) number. Magnitude **minor** (~1-3 day-cluster difference across features); the underpowered-NULL framing holds either way.

**L1.3 — Analysis method named with parameters (PASS).** Sub-MD §3.1 + result.md §1 + run.py docstring all name: 7 features × 3 windows × 9 specs = 189 cells; OLS with cluster-robust SE on date for bout-level (Daza-2018-anchored day-cluster analogue of MixedLM with random intercept; explicitly documented at run.py docstring decision #1); Newey-West HAC with Andrews 1991 lag selection for per-day. Both spec layers traceable.

**L1.4 — Confounders enumerated (PASS).** Sub-MD §1.3 caveat stack carried into result.md §7 caveat 3 verbatim: LC recovery trajectory, seasonality, Breinvoeding, CPAP-end at 2024-04-16. Mitigations named (linear time covariate; three-window spec; post-CPAP buffer; spring 2025 control).

**L1.5 — Limitations stated separately from results (PASS).** Result.md §7 has 8 caveats; sub-MD §7 has 6; result.md §7 explicitly notes session-specific learnings #7-#8 are new. The "bout-level recalibration is a precision question, not a substantive question, at this n" caveat (result.md §7.7) is the load-bearing limitation, properly separated from the result narrative.

**L1.6 — Analysis frame named (PASS).** Bout-level for the 5 per-bout features; day-level for the 2 per-day aggregations; cross-phase scope (afbouw + buildup post-CPAP + spring 2025 control) per sub-MD §1.5; not framework-validity restricted (which would be unmedicated × train per parent MD §6). Sub-MD §6 introductory paragraph + result.md §1 windows table both explicit.

### Layer 2 — Observational n=1 (Daza 2018, Personal Science; CONVENTIONS §4.3, §5)

**L2.1 — Counterfactual framing explicit (PASS-with-caveat).** Sub-MD §1.3 caveat ("the per-feature β estimates are 'consistent with a dose-graded modulation of recovery-dynamics on the per-bout feature, after absorbing the local LC-recovery slope', NOT isolated pharmacological causation") inherits into result.md §7 caveat 3. Result.md §3 per-feature paragraphs frame β as "/mg" within-subject (correct), but two sub-MD §1.3 caveats — that the β is a *partial-derivative on a within-window dose gradient* not a population-level dose-response — could be re-stated explicitly in result.md §3 for reader clarity. **Minor**; the framing is correct, the prose could surface it.

**L2.2 — Stationarity acknowledged (PASS).** Three-window spec mitigates non-stationarity. Linear time covariate absorbs local slope. Result.md §7 caveat 3 carries the assumption forward.

**L2.3 — Calendar-time vs subject-time (PASS).** Sub-MD §3.1 windows = calendar-time. Result.md §1 windows table dates match sub-MD §3.1 verbatim (afbouw 2026-03-20 → 2026-06-05; buildup post-CPAP 2024-05-01 → 2024-06-19; spring 2025 control 2025-03-20 → 2025-06-05). All three match the parent dose-response MD §5 pattern.

**L2.4 — Data provenance traceable to script + dump version (PASS).** Result.md Authorship block names: `per_bout_master.csv` extracted at pipeline commit `d5b394c`; recalibration ran at `d9c6fa4`; seed `20260622`. run.py header docstring repeats. CSV path explicit + env-var pattern documented.

**L2.5 — Held-out structure framing (NO FIRE EXPECTED — confirmed irrelevant).** The recalibration is a within-window dose-response fit, not a precursor-test against a held-out era. Sub-MD §1.4 framing is confirmatory-not-exploratory; the held-out-structure boundary is not in play.

**L2.6 — Prior motivation named per CONVENTIONS §4.3 (PASS).** Sub-MD §1.4 confirmatory framing carried verbatim into result.md §7. Result.md §3 per-feature paragraphs cite the §2 expected-sign prior + the §3.4 null pre-spec + the §3.5 verdict bands without retreating to exploratory framing when the verdicts came in mostly NULL. **This is the L4.8 prior-driven-confirmatory check passing.**

### Layer 3 — Time-series specific (Natesan Batley 2023, WWC 2022, CENT 2015; CONVENTIONS §3.2, `permutation_null_block_length.md`)

**L3.1 — Autocorrelation addressed (PASS).** Day-level cluster-robust SE for the per-bout fits (run.py `_fit_ols_cluster`); Newey-West HAC for per-day fits (run.py `_fit_ols_hac` with Andrews 1991 default lag). Not silent i.i.d. The Sensitivity H within-day AR(1) was reported diagnostic-only per sub-MD §3.3 fallback wording — within-day n ≈ 3-8 bouts/day too small for stable AR(1) estimation; this is the honest fallback rather than a workaround.

**L3.2 — Lag-carryover (PASS).** Sub-MD §3.3 sens C lagged-lcera variant reported per feature: 6 features admit it, `decay_slope` does not. CSV verifies: `decay_slope × * × sens_C_lagged_lcera` rows all carry `feature_does_not_admit_lagged_lcera` note + N/A. Lagged-lcera computation per run.py decision #4: per-day mean of feature over [d-90, d-30] LC-era restricted (LC start 2022-04-04). Implementation matches CONVENTIONS §3.2 verbatim.

**L3.3 — Multiple testing (PASS-with-caveat).** Sub-MD §3.7 + result.md §5 Holm step-down table covers the 5 per-bout features per window as descriptive overlay (3 windows × 5 features × 2 substantive windows = 10 cells; control window N/A). No per-bout feature rejects at α=0.05 in either window after Holm correction (consistent with the per-feature NULL/weakly-consistent verdicts). The full multiplicity surface (189 cells) is explicitly NOT family-wise corrected per CONVENTIONS §3.6 + parent §5.2 deferral; this is acceptable. **Minor caveat**: the per-day aggregations are excluded from the Holm family per run.py docstring decision #6; the Holm table in result.md §5 should explicitly note this (it does not). Mechanical r2 absorb opportunity.

**L3.4 — Block-permutation null block length documented (PASS).** Sub-MD §3.3 sens A inherits stationary bootstrap E[L]=7 from `permutation_null_block_length.md` per parent MD §5.1. Result.md §1 verifies: "sens A block bootstrap E[L]=7, 1000 iter". run.py imports `stationary_bootstrap_ci` from the project utility module and calls with `expected_block_length=7`. Verified.

**L3.5 — Trend vs level claim separated (PASS-with-substantive-observation).** Sub-MD §3.1 model form has dose × feature (level relationship) + linear time covariate (trend absorber); not conflated. Result.md §3 per-feature paragraphs read β as dose-modulation, not trend. **But**: result.md §4 paragraph 3 ("the afbouw `bout_n_per_day` signal is reported as a substantive observation in §4") frames the afbouw `bout_n_per_day` β=−0.102 as "higher plasma → fewer bouts overall" (level reading) or "within-window time-trend that the linear covariate fails to absorb" (trend reading) — both candidate readings open. The Sens F nonlinear-time-spline result for afbouw `bout_n_per_day` (β=−0.196 [−0.325, −0.066] p=0.003) is **not** surfaced in result.md §4's two-reading exposition, which is a notable omission because **if the nonlinear-time spline absorbs more of the within-window time-trend AND the dose-β GETS LARGER (more negative)**, the second candidate reading (within-window time-trend confound) is LESS supported — sens_F STRENGTHENS the dose-causal reading rather than weakens it. This is L3.5-discriminating-evidence that the dose reading edges ahead of the time-trend reading; surfacing the sens_F result is a constructive close in §4. **MEDIUM** — not a verdict-changing concern, but the result.md §4 "two readings open" framing is more conservative than the data warrants given sens_F.

### Layer 4 — Project-specific audit hooks (CONVENTIONS §3, §4)

**L4.1 — Personal baseline (NO FIRE EXPECTED — confirmed irrelevant).** For dose-response, the predictor IS already standardised (mg of plasma); the outcome is on feature's native unit. No §3.1 rolling-baseline-z-score discipline applies here.

**L4.2 — `_lagged_lcera` variant (PASS).** Sub-MD §3.3 sens C tested per feature where applicable; verified in CSV. Run.py decision #4 documents the implementation cleanly.

**L4.3 — One column per definitional pair (PASS).** 5 per-bout features + 2 per-day aggregations = 7 fits. No near-identical-pair duplication. The 2 per-day aggregations (`bout_n_per_day`, `bout_n_fast_recovery_day`) are distinct operands (different threshold semantics).

**L4.4 — Crash-drop sensitivity row (PASS-with-medium-observation).** CSV `sens_E_crash_drop` row present for each feature × non-control window. Verified |Δβ| threshold computation in run.py: `0.10 * np.std(y, ddof=1)`. No cell exceeds threshold per the verdict-cells of sens_E rows (all "exceeds=False"). **Medium observation**: result.md §4 paragraph 3 reports "Sens E (crash-drop) on afbouw bout_n_per_day shows β = −0.067/mg with |Δβ| = 0.035 < 0.10·SD threshold = 0.060". The CSV says `bout_n_per_day × afbouw × sens_E_crash_drop`: β=**−0.108** (not −0.067), |Δβ|=0.0054 (not 0.035), threshold=0.10·SD=0.1131 (not 0.060). The result.md narrative's specific numbers do **not** match the CSV; the verdict (does-not-fire-crash-distortion-flag) is the same under either set of numbers, but the L1.2 traceability fire propagates here. **Minor magnitude** at the verdict level (does not change the no-flag conclusion); **medium** at the audit-trail level (the prose narrative cites numbers that aren't in the CSV).

**L4.5 — Spike-detecting metric vs daily averages (NO FIRE EXPECTED — confirmed).** Bout-level β is per-bout by construction (spike-detecting); per-day β is daily-average. Both reported.

**L4.6 — Counts named with scheme + unit + source file (PASS-with-caveat).** Each β reported with scheme (mg of plasma), unit (feature's native unit per sub-MD §2), source (the CSV row populated via run.py). The "robust across 6 of 7 sensitivity specs" framing on `bout_n_per_day` afbouw sign-discordance (sub-MD §6 + commit message + STOCKTAKE §6 paragraph) is **imprecise**: CSV shows 7/7 sens cells (primary + 6 sens) sign-discordant; 5/7 also at p<0.05; the "6/7" figure is between these two natural counts and is not directly derivable from the CSV. **Minor**: re-derive the count + state the threshold ("sign-discordant + p < 0.10 across 6 of 7"; or "sign-discordant across all 7 specs with p < 0.05 on 5/7"). Mechanical r4 absorb opportunity if substantive.

**L4.7 — Caveat-class vs a-priori-class framing on the 0/7-CONFIRMED finding (PASS-with-strong-evidence — THE BIG ONE).** This is the audit's load-bearing L4.7 check. The framing discipline holds **clean across all three artefacts**:

- **result.md §4 framing**: *"at bout-level n=49 day-clusters in buildup-post-CPAP and n=78 in afbouw, NONE of the per-bout features achieve CONFIRMED dose-modulation"* + *"the binding constraint is bout-level n (~49 day-clusters/window), not feature-by-feature dose-response heterogeneity"* + *"The recalibration produces NULL/weakly-consistent verdicts across the board because the bout-level CIs are wide relative to the underlying signal at this corpus's n. The parent dose-response MD's daily-aggregate +0.57/mg `all_day_stress_avg` β does NOT cleanly propagate to per-bout features at this resolution — but the parent finding remains intact at its own (daily) layer."*

- **Sub-MD §6 net inheritance summary**: *"No feature reaches CONFIRMED at the buildup-headline precision. Approach A is NOT load-bearing for any downstream HA pre-reg at this r3 lock."* + dynamics-vs-level read explicitly disclaimed: *"the data pattern does NOT cleanly support the level-vs-dynamics dichotomy"*; *"the honest reading is bout-level n is the binding constraint at this corpus"*.

- **Sub-MD §8 r3 revision log**: *"Dynamics-vs-level read inconclusive at this bout-level n (≈49 day-clusters in buildup-post-CPAP); the binding constraint is precision, not feature-by-feature heterogeneity."* Plus the explicit conditional: "the §6 table now stable until any future recalibration session triggers an r4 absorb".

- **STOCKTAKE §6 architectural-implications paragraph (lines 182-188)**: *"The finding is properly framed as an underpowered-NULL at n≈49 day-clusters per window, NOT a definitive claim about citalopram's bout-level pharmacology — at this corpus's per-window n, β coefficients cannot cross the sub-MD §3.4 four-condition discriminative bar. If a future expanded corpus or revised bout-detection rule materially changes per-window n, the recalibration re-runs (sub-MD §8 r4 trigger)."*

- **Sub-MD §6 §6.last-paragraph "(§5.5)" sub-section**: *"the data pattern does NOT cleanly support the level-vs-dynamics dichotomy"* + the substantive read explicitly downgraded.

Five-place framing-discipline consistency (result.md §3 per-feature paragraphs each reach NULL or weakly_consistent with the conditional language preserved; result.md §4 articulates the bout-n binding constraint; sub-MD §6 inheritance summary explicit; sub-MD §8 r3 entry repeats; STOCKTAKE §6 paragraph the cross-cutting cement). This is the strongest L4.7 evidence I've seen in the project review folder; the caveat-vs-a-priori discipline is reinforced at five distinct surfaces and never slips to "we've demonstrated citalopram is dose-naive at bout-level".

**L4.8 — Prior-driven hypothesis framed as confirmatory (PASS).** Sub-MD §1.4 + §2 expected signs are pre-specified at lock time r2. Result.md does NOT retreat to exploratory framing despite mostly-NULL verdicts; the verdicts are reported against the pre-spec'd priors per CONVENTIONS §4.3. **But see L4.7-§3.5 verdict-rule note below**: the verdict-rule application for `bout_n_per_day` buildup-headline (NULL despite sign-discordance) is a §3.5 verdict-rule interpretation question worth surfacing — see §4 Recommendation #2.

### Plan-effectiveness dimension (PE.1-4 per `STOCKTAKE.md §7` canonicalised pattern from the 2026-06-22 collapsibility audit)

#### PE.1 — Handoff §-coverage (PASS)

Walk of execution handoff §2.1-2.4 required artefacts:

| handoff requirement | landed artefact | present / partial / missing |
|---|---|---|
| §2.1 `run.py` at the spec path | `docs/research/analyses/descriptive/operationalisation_support/bout_level_dose_response_calibration/run.py` (1211 lines) | **present** + docstring documents all 8 design decisions + 4 anti-patterns avoided per handoff §3 |
| §2.2 CSV at `$GEVOELSCORE_DATA_PATH/unified/bout_level_dose_response_calibration_results.csv` | 189 data rows + 1 header verified via direct CSV read; schema matches sub-MD §4 verbatim (11 columns) | **present** + correct row count |
| §2.3 result.md with 8 sections (Authorship + §1-§8) | result.md exists with `## Authorship`, `## §1 What was run`, `## §2 What landed in the CSV`, `## §3 Per-feature headline`, `## §4 The dynamics-vs-level read`, `## §5 Inheritance assignments`, `## §6 Open questions`, `## §7 Caveats`, `## §8 Reproducibility checklist` | **present** + all 8 sections + Cross-references section as bonus |
| §2.4 sub-MD §6 table populated + §8 r3 entry | Sub-MD §6 table populated with 7 rows of values + net inheritance summary + dynamics-vs-level read; §8 status updated to r3 LANDED; §8 revision-log r3 row added | **present** + producer-mode authorisation note included |

**PE.1 verdict**: **PASS-PE** — all 4 required artefacts landed; no missing-section fires.

#### PE.2 — User-locked decisions honored (PASS)

Walk of execution handoff §3 — 9 decisions to surface:

| decision (handoff §3) | run.py / result.md evidence | verdict |
|---|---|---|
| **(1) Library** | run.py docstring decision #1: OLS + cluster-robust SE on date (Daza-2018-anchored day-cluster equivalent of MixedLM day-level random intercept) for bout-level fits; HAC for per-day fits | **PASS** — explicit + cross-cites MD §3.2 |
| **(2) Cluster-robust SE form** | run.py `_fit_ols_cluster`: `model.fit(cov_type="cluster", cov_kwds={"groups": groups})` | **PASS** — exact statsmodels API documented |
| **(3) Block-bootstrap implementation** | run.py imports `stationary_bootstrap_ci` from project `inference` module; calls with `expected_block_length=7, n_bootstrap=1000, random_state=SEED` | **PASS** — inherited from project utility per handoff |
| **(4) `decay_slope` direction handling** | run.py docstring decision #2: β fit on RAW SIGNED slope; prior +1 means less-negative under higher plasma; no sign flip; `PRIOR_SIGN["decay_slope"] = +1` | **PASS** — equivalence reasoning explicit |
| **(5) AR(1) feasibility (sens H)** | run.py docstring decision #3: diagnostic-only per MD fallback; emits `diagnostic_only_within_day_n_too_small_for_stable_AR1` in verdict cell; all CSV `sens_H_within_day_ar1` rows confirm | **PASS** — honest fallback per MD pre-spec |
| **(6) Lagged-lcera variant** | run.py docstring decision #4 + `compute_lagged_lcera_reference` function: per-day mean of feature on `[d-90, d-30]` LC-era days; LC start 2022-04-04; minimum 5 LC-era days for valid reference | **PASS** — matches CONVENTIONS §3.2 + sub-MD §2 |
| **(7) Crash-drop sensitivity** | run.py docstring decision #5 + sens_E rows: drops `is_crash == True` rows from day-pool; |Δβ| > 0.10 × SD(feature) threshold per CONVENTIONS §3.4; threshold computation visible in CSV note column | **PASS** — implementation correct |
| **(8) Holm step-down scope** | run.py docstring decision #6: family = 5 per-bout features PER window; 3 windows → 3 Holm families; per-day aggregations excluded; verified in result.md §5 Holm table | **PASS** — matches handoff intent |
| **(9) Per-day aggregation column name mapping** | run.py docstring decision #7: MD-spec name `bout_count_day` → pipeline-actual `bout_n_per_day`; mapping cited in sub-MD §6 table row label + result.md §1 features bullet | **PASS** — documented; no silent rename |

**PE.2 verdict**: **PASS-PE** — all 9 user-locked decisions honored with documented call-sites; no decision-violation fires.

#### PE.3 — Scope creep (PASS)

Walk of execution handoff §5 anti-list:

- **Did not run pipeline extraction**: `per_bout_master.csv` re-used at `d5b394c`; not re-extracted. Compliant.
- **Did not write per_bout_master.csv to repo**: data lives external per GEVOELSCORE_DATA_PATH; result CSV also external. Compliant.
- **Did not embed per-feature raw data values in result.md / sub-MD**: result.md §2 sample-read shows 3 rows of aggregated statistics only (β + CI + p + n_bouts + n_days); no per-bout raw values. Compliant.
- **Did not push to remote**: working tree clean per `git status --short` at audit-time (will be re-checked before commit). Compliant.
- **Did not perform the audit**: this report is the audit, run in a separate fresh-session session per CONVENTIONS §1.2. Compliant by definition.
- **Did not pre-author HA-C4c content**: result.md §6 open-questions paragraph names HA-C4c implications but does not pre-author HA-C4c hypothesis text. Compliant.
- **Did not silently rename columns**: the `bout_count_day` → `bout_n_per_day` mapping is documented at three surfaces (run.py docstring #7 + sub-MD §6 table row label + result.md §1 features bullet). Compliant.

**One in-intent scope-addition observation, NOT a creep fire**: result.md is 8 sections; the handoff §2.3 specifies 8 sections (Authorship + §1-§8). The result.md adds a final "Cross-references" section beyond the 8 named — defensible (matches project pattern of cross-ref tail in `result.md` + `methodology/*.md` artefacts; the deferred-honesty pattern for traceability). Not creep.

**PE.3 verdict**: **PASS-PE** — no scope creep; one defensible in-intent addition (Cross-references tail).

#### PE.4 — Gap analysis (PASS-with-medium-observations)

Walk of execution handoff §2 + §6 verification list — things specified but possibly not delivered:

- **189 rows in CSV**: verified via direct read. 189 data rows + 1 header. Matches 7 × 3 × 9 exactly. N/A markers present for inapplicable cells (sens G for per-day; sens C for decay_slope; control-window dose-cells). Compliant.
- **Verdict cells in CSV**: per the handoff, the CSV `verdict` column should carry the per-cell verdict (the run.py `_make_row` puts a free-text note in this column, not the formal CONFIRMED/NULL/etc. verdict; the formal verdict is injected ONLY on the `buildup_post_cpap_2024 × primary` row per run.py main(); other rows' `verdict` column carries the spec-specific note like `block_bootstrap_day_blocks_EL7_1000iter`). This is an **intentional choice** (the formal verdict is per-feature, not per-cell), but the schema column name `verdict` is overloaded for two purposes (per-cell note + per-feature verdict at the headline row). **Minor PE.4 observation**: schema column-name semantics could be clearer; e.g. a separate `feature_verdict_at_headline_row` column or renaming `verdict` → `note_or_verdict`. Mechanical r4 absorb.
- **Result.md §3 per-feature numerics traceability**: see L1.2 above — three mismatches between result.md §3 narrative and CSV source-of-truth. **MEDIUM** PE.4 fire because the numerics-as-stated are part of the handoff §2.3 expected deliverable; the prose was not faithfully tracking the CSV.
- **Sub-MD §6 table numerics traceability**: same as above for `recovery_half_life` afbouw + `AUC_above_baseline` afbouw cells. **MEDIUM** PE.4 fire.
- **§3.4 NULL pre-spec walked per feature**: result.md §3 walks the 4-condition NULL pre-spec for `peak_height`, `pre_bout_baseline`, `decay_slope` (with 3-condition collapse for decay_slope per sub-MD §2 r2 absorb), `bout_n_per_day`. Compliant.
- **§3.5 verdict-rule application walked per feature**: implicit in result.md §3 verdict assignments + run.py `assign_verdict` function. The verdict-rule's ORDER OF CHECKS (NULL pre-spec first vs sign-discordance first) is **not explicit in sub-MD §3.5**; run.py chose NULL-first. For `bout_n_per_day` at buildup-headline this produces NULL (correct under NULL-first); under sign-discordance-first it would be REJECTED. The afbouw signal at p<0.05 makes the afbouw cell a REJECTED candidate under sign-discordance-first. Sub-MD §3.5 says: *"REJECTED: sign-discordant OR both CIs cross zero"*. The "OR" reads as "either condition suffices" — but NULL is defined separately at §3.4. The rule-precedence question is undocumented. **MEDIUM** PE.4 observation: handoff §3 didn't name this; it's a downstream sub-MD §3.5 wording precision issue (see §4 recommendation #2). For `bout_n_per_day` afbouw the result.md choice (NULL at buildup-headline + sign-discordant flag at afbouw + cross-cite as substantive observation requiring HA pre-reg sensitivity arm) is the **defensible** choice; the L4.7 framing-discipline holds; the rule-precedence question is a methodology-precision opportunity not a verdict error.

**PE.4 verdict**: **PASS-PE-with-medium** — no architectural omissions; one column-name-semantics observation + one verdict-rule-precedence observation + the L1.2 traceability mismatches on numerics propagate into PE.4 as MEDIUM gap-fires. The structural deliverable is intact; the numerics-prose-vs-CSV discrepancies are the load-bearing PE.4 concern.

**Plan-effectiveness rollup verdict**: **PASS-PE** at PE.1 (handoff coverage) + PE.2 (all 9 decisions honored) + PE.3 (no scope creep); **PASS-PE-with-medium** at PE.4 (numerics traceability between result.md narrative + sub-MD §6 cells + CSV source-of-truth has three mismatches that propagate from L1.2). The MEDIUM PE.4 magnitude reflects that the verdict-level conclusions hold under either set of numbers, but the audit-trail discipline is the load-bearing concern.

---

## §3 What does not fire (selective, non-trivial passes)

- **Schema fidelity at the CSV layer**: 189 rows × 11 columns exact match to sub-MD §4 LOCKED schema. The schema column list (`feature, window, spec, n_bouts, n_days, beta_dose, beta_dose_lo95, beta_dose_hi95, p_value, sign_match_prior, verdict`) is implemented verbatim. N/A semantics consistent: sens C for `decay_slope`, sens G for per-day aggregations, all sens specs for `spring_2025_control` (where dose-variance is zero by design). The schema-versus-implementation discipline is exemplary.

- **L4.7 underpowered-NULL framing discipline at five surfaces**: the caveat-class-vs-a-priori-class boundary holds clean at result.md §3 + result.md §4 + sub-MD §6 net inheritance + sub-MD §8 r3 entry + STOCKTAKE §6 paragraph. This is the strongest L4.7 framing-discipline evidence in the project review folder — five distinct surfaces reinforce the "underpowered-NULL at this n, NOT definitive dose-naivety" claim. The architectural implications paragraph in STOCKTAKE §6 explicitly conditions all four implications on the underpowered-NULL framing (and would invert if a future expanded corpus changed per-window n). The cross-cutting framing is internally coherent and externally publishable.

- **Three-place architectural-implications consistency** (STOCKTAKE §6 ↔ sub-MD §6 ↔ result.md §6): the four architectural implications named in STOCKTAKE §6 lines 184-188 (HA-C4c primary dose-naive; phase 5 ↔ phase 6 collapse permissible for bout-level work without §5.A/B/C violation; 4 things NOT relaxed; cross-test pass methodological-design-shaping relevance) all match the result.md §6 open-questions wording for downstream HA pre-regs + sub-MD §6 net inheritance summary. No contradiction across the three artefacts.

- **Verdict-rule application correctness for the 6 non-`bout_n_per_day` features**: walked the §3.5 rule backward from each assigned verdict to the (afbouw, buildup, control) trio in the CSV; verdicts are internally consistent with the rule for the 6 features that are NOT sign-discordant at headline. The verdict-rule precedence question only fires on `bout_n_per_day` (see §4 recommendation #2); 6/7 features are unambiguous.

- **Confirmatory-not-exploratory discipline preservation despite mostly-NULL verdicts**: result.md does not retreat to exploratory framing when the verdicts came in mostly NULL. The pre-spec'd priors are reported as the reference frame; NULL/weakly-consistent are reported as the verdicts against that frame. CONVENTIONS §4.3 prior-driven-confirmatory discipline holds.

- **run.py docstring documents all 8 design decisions + 4 anti-patterns avoided**: the handoff §3 + §8 enumerated 9 decisions to surface + 4 anti-patterns; run.py docstring decision list maps cleanly. Audit-trail discipline at the script layer is the best I've seen in the `analyses/descriptive/` folder.

- **Sub-MD §3-§5 spec unchanged**: producer-mode r3 edit honored the discipline that only §6 (designed-to-absorb-result) + §8 (status-log) are eligible for r3 modification. §3-§5 LOCKED spec stayed byte-stable. Verified via `git show --stat d9c6fa4` (3 files changed; sub-MD changes localized to §6 table + §8 entries).

- **Sens A bootstrap CI honesty on `recovery_half_life` buildup**: CI [−13.47, +22.64] is enormous (n=49 day-clusters drives huge bootstrap variance). Result.md §3 `recovery_half_life` paragraph honestly says "n=49 day-clusters drives huge bootstrap variance" rather than papering over the inflation. CONVENTIONS §3.6 named-counts discipline at work; the result.md doesn't pretend the bootstrap CI is informative.

---

## §4 What would strengthen this finding

Concrete, named, ordered by leverage:

1. **(result.md §3 + sub-MD §6 + L1.2 fire absorb) Three-place numerics reconciliation between result.md §3 narrative, sub-MD §6 table cells, and CSV source-of-truth**. Specifically:
   - **`recovery_half_life` afbouw β**: CSV says +0.957 [−0.350, +2.264] p=0.151. result.md §3 + sub-MD §6 say +0.564 [−0.213, +1.342] p=0.155. Re-derive from CSV + update both surfaces. The verdict (weakly_consistent) doesn't change.
   - **`AUC_above_baseline` afbouw β SIGN-FLIP**: CSV says β=**−20.5** sign-discordant. result.md §3 + sub-MD §6 say β=**+27.7** sign-concordant. Re-derive from CSV + update both surfaces; the dynamics-vs-level read in result.md §4 needs a one-sentence revision because the "sign-concordant in BOTH windows" framing on `AUC_above_baseline` is unsupported by the CSV. The buildup-headline verdict (weakly_consistent) still holds (buildup β=+52.4 IS sign-concordant), but the cross-window-coherence argument loses force.
   - **`bout_n_per_day` afbouw sens_E numerics**: result.md §4 paragraph 3 cites β=−0.067 |Δβ|=0.035 threshold=0.060; CSV says β=−0.108 |Δβ|=0.005 threshold=0.113. Re-derive from CSV + update. The crash-distortion-flag conclusion (does-not-fire) holds.
   - **Expected effect**: closes L1.2 and PE.4 fires; the audit-trail discipline is restored; verdicts are unchanged. Mechanical r4 absorb (see §5 recommendation).

2. **(sub-MD §3.5 + L4.8 + PE.4 verdict-rule-precedence observation) Document the §3.5 verdict-rule precedence — NULL pre-spec checked first vs sign-discordance checked first**. The run.py implementation chose NULL-first; for `bout_n_per_day` at buildup-headline this produces NULL (the chosen verdict) rather than REJECTED (which the literal §3.5 "REJECTED: sign-discordant" reading would produce). The NULL-first reading is defensible — when the dose-β is statistically indistinguishable from zero, "sign of the noise" is the wrong lens for verdict assignment — but the rule-precedence is not in the sub-MD §3.5 text. Add a one-sentence precedence note: *"Verdict precedence: §3.4 NULL pre-spec is checked first; only if NULL pre-spec fails does the rule fall through to CONFIRMED / weakly_consistent / partial / REJECTED."* This pins the implementation choice as the spec choice. **Expected effect**: closes a methodology-precision question that would re-surface on any future sub-MD recalibration; preserves the chosen verdict assignments. Mechanical r4 absorb.

3. **(result.md §4 sens_F absorb) Surface the sens_F nonlinear-time results that ARE significant**. CSV shows `recovery_half_life × buildup × sens_F` β=+3.84 [+0.32, +7.36] p=0.032 (CONFIRMED-direction at p<0.05) + `AUC_above_baseline × buildup × sens_F` β=+335.95 [+152.8, +519.1] p=0.0003 (CONFIRMED-direction at p<0.001) + `bout_n_per_day × afbouw × sens_F` β=−0.196 [−0.325, −0.066] p=0.003 (sign-discordant + p<0.01). The sens_F nonlinear-time-spline absorbs MORE within-window time-trend variance; the dose-β under sens_F is the MORE-confound-adjusted estimate. The fact that several features show SIGNIFICANT effects under sens_F (vs NULL under linear time) is **L3.5-discriminating evidence** that the linear time covariate may be under-fitting the within-window trend, and the dose-causal signal may be larger than the headline-spec admits. result.md §4 should surface the sens_F results in one paragraph: "Three sens_F cells reach p<0.05 under nonlinear time spline that the linear-time primary does not: `recovery_half_life` buildup (β=+3.84 p=0.032), `AUC_above_baseline` buildup (β=+335.95 p=0.0003), `bout_n_per_day` afbouw (β=−0.196 p=0.003). Two interpretations open: (a) the linear time covariate under-fits the within-window trend, dose-causal signal is larger than headline admits; (b) the spline overfits a noisy 47-50-day window. The headline-spec compound-symmetry + linear-time pre-commit holds the load-bearing verdicts; the sens_F results add nuance worth surfacing in downstream HA-C4c framing." **Expected effect**: closes the L3.5 observation; strengthens the substantive read; does NOT change the headline verdicts (sens_F is sensitivity-arm by design). **Medium leverage** — substantively informative without changing any verdict assignment.

4. **(sub-MD §6 + commit message + STOCKTAKE §6) Re-derive the "6 of 7 sensitivity specs" count for `bout_n_per_day` afbouw sign-discordance**. CSV verifies: 7/7 sens cells sign-discordant (primary + sens_A + sens_B + sens_C + sens_D + sens_E + sens_F); 5/7 also at p<0.05 (sens_A bootstrap p=0.068 + sens_C lagged-lcera p=0.084 are the 2 NOT at p<0.05). The "6 of 7" framing is between these two natural counts. **Recommendation**: either (a) state "sign-discordant across all 7 sens specs; p<0.05 on 5 of 7"; or (b) name the precise threshold ("sign-discordant + p<0.10 across 6 of 7"). Mechanical r4 absorb. **Expected effect**: closes L4.6 named-counts-discipline precision concern.

5. **(L3.3 Holm note) Result.md §5 Holm table — explicitly note per-day aggregations excluded from Holm family** per run.py docstring decision #6. Currently the table caption says "across the 5 per-bout features per window" but a reader walking the table might miss why `bout_n_per_day` + `bout_n_fast_recovery_day` are absent from the Holm rows. Add a one-sentence footnote. Mechanical r4 absorb.

6. **(L2.1 counterfactual framing) Result.md §3 per-feature paragraphs — explicit within-subject within-window partial-derivative framing**. The β "/mg" is correct; surfacing in one sentence per paragraph that the β is a within-window partial-derivative-of-feature-on-dose (not a population-level dose-response) would foreclose a misread by a future reader walking the §3 paragraphs without the §1.3 + §7.3 caveat stack. Cosmetic; mechanical r4 absorb.

The six items above are all **mechanical r4 absorb scope** per `hypothesis_lock_process.md §3.6` compression criteria for methodology MDs (pattern matches the `bout_level_recovery_dynamics r2 lock` + `phase_axis_collapsibility_conventions r2 absorb` precedents — both absorbed L1-L4 fires mechanically without architectural revision). **None change any §6 inheritance assignment.** All 7 features keep their assigned verdicts under the recommendations above. **None change the STOCKTAKE §6 architectural-implications paragraph framing.** The recommended changes are precision improvements within the underpowered-NULL framing, not framing revisions.

**No r4 substantive trigger** from the audit. The r3 stands at the verdict + inheritance + architectural-implications layers; r4 is an absorb-only compression cycle.

---

## §5 Verdict

**PASS-with-caveats** — the recalibration's spec implementation, sensitivity sweeps, verdict assignments, inheritance table population, and (most load-bearingly) the underpowered-NULL framing discipline across result.md §3-§4 + sub-MD §6 + sub-MD §8 + STOCKTAKE §6 (five-place L4.7 consistency) all read clean against both the content audit (L1-L4) and the plan-effectiveness dimension (PE.1-3); the highest-priority residual is three L1.2 numerics-traceability mismatches between result.md §3 narrative, sub-MD §6 table cells, and the CSV source-of-truth (specifically: `recovery_half_life` afbouw β, `AUC_above_baseline` afbouw β SIGN-FLIP, `bout_n_per_day` afbouw sens_E numerics) which propagate as MEDIUM PE.4 gap-fires; none change any §6 inheritance assignment or the STOCKTAKE §6 architectural-implications paragraph framing; all 9 user-locked execution decisions honored at PE.2; r4 absorb is mechanical (3 numerics reconciliations + 1 §3.5 verdict-rule precedence note + 1 sens_F surfacing + 1 Holm footnote + 1 §3 framing one-liner) per `hypothesis_lock_process.md §3.6` compression criteria.

---

## Methodology

This review walks the 4-layer audit framework defined in this session's handoff
([`session-bout-level-beta-recalibration-r3-audit-handoff-2026-06-22.md`](file:///C:/Users/Gebruiker/.claude/plans/session-bout-level-beta-recalibration-r3-audit-handoff-2026-06-22.md)),
adapted from [`reviews/README.md`](README.md) for the producer-mode methodology-MD-r3-population audit
per [CONVENTIONS §2.2](../CONVENTIONS.md) four-input bar discipline, PLUS the plan-effectiveness audit dimension (PE.1-4) per the canonicalised
project pattern from the 2026-06-22 collapsibility audit ([`reviews/phase_axis_collapsibility_conventions-2026-06-22.md`](phase_axis_collapsibility_conventions-2026-06-22.md)).

Skill not used: `/research-review` is for reviewer-mode artefacts; the recalibration r3 is producer-mode (methodology MD §6 population + descriptive run output).
`/research-methodology-review` is not yet implemented per `/research-review` skill docs.

4-layer inheritance:
- **Layer 1** — SCRIBE 2016 items 3-5, 14, 18, 22-24 ([Tate et al., PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/)); STROBE 2007 items 6, 12, 13 ([../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf)); [CONVENTIONS §2.1, §2.2](../CONVENTIONS.md).
- **Layer 2** — Daza 2018 ([../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)); Personal Science (Wolf et al., Meth Inf Med 2017); [CONVENTIONS §4.3, §5](../CONVENTIONS.md).
- **Layer 3** — Natesan Batley et al. 2023 ([../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf)); WWC 2022 SCED ([../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf)); CENT 2015 ([../literature/methodology/shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf)); [CONVENTIONS §3.2](../CONVENTIONS.md); [`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md).
- **Layer 4** — Project-specific audit hooks from [CONVENTIONS §3 + §4](../CONVENTIONS.md).
- **PE.1-4** — Canonicalised project pattern per [`STOCKTAKE.md §7 "Plan-effectiveness audit dimension"`](../STOCKTAKE.md); first appearance in [`reviews/phase_axis_collapsibility_conventions-2026-06-22.md`](phase_axis_collapsibility_conventions-2026-06-22.md).

Methodology-MD lock framework from [`hypothesis_lock_process.md §1`](../methodology/hypothesis_lock_process.md) (carve-out: methodology MDs are governed by CONVENTIONS §2.2 + §2.3, not the HA lock process); r4 compression criteria from [`hypothesis_lock_process.md §3.6`](../methodology/hypothesis_lock_process.md).
