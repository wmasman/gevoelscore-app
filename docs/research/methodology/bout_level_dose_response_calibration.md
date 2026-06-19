# Bout-level citalopram dose-response calibration — methodology

*Producer-mode methodology sub-MD per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafted 2026-06-19 as r1 alongside parent [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md). Pending fresh-session audit per [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) before lock.*

---

## Authorship

**Drafted 2026-06-19** by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem.

**Drafting trigger**: parent MD [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) §5.4 committed to a bout-level β re-calibration as a load-bearing methodological component (handoff §1 item 6 + decision #7 sub-resolution). Rather than assume the daily-aggregate β coefficients from [`citalopram_dose_response_stress_mean_sleep.md §5.6.1`](citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read) (+0.43/mg for `stress_mean_sleep`, +0.57/mg for `all_day_stress_avg`, −1.13/mg for `bb_lowest`) extend linearly to per-bout features, the calibration is re-run independently per feature. This sub-MD locks the recalibration spec.

**Structural choice — sub-MD over appendix**: per parent §5.4, the recalibration is its own auditable unit. Keeps the parent MD's operand definition tight; surfaces this calibration's independent substantive finding (does citalopram act on stress *dynamics* differently than on stress *level*?) as a separate research result. Matches the project pattern of spinning off [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md) from [`citalopram_dose_response_stress_mean_sleep.md`](citalopram_dose_response_stress_mean_sleep.md).

**Locked decisions at draft time** (structural pre-commits, not data-driven):

1. **Same three-pronged spec as parent dose-response MD** (afbouw 2026 primary + buildup 2024 post-CPAP-buffer + spring 2025 control). Inherits the parent's PK-smoothed plasma exposure, Newey-West HAC SE, block-bootstrap sensitivity, prescribed-step sensitivity, lagged-lcera sensitivity, crash-drop sensitivity, nonlinear-time sensitivity. **One spec per feature, fit independently.**
2. **Per-bout features in scope**: the five primary recovery-dynamics features from [`bout_level_recovery_dynamics.md` §4](bout_level_recovery_dynamics.md): `peak_height`, `pre_bout_baseline`, `recovery_half_life`, `decay_slope`, `AUC_above_baseline`. Plus the per-day aggregations `bout_count_day` + `bout_n_fast_recovery_day` (because they are the operand the downstream framework-validity gate runs on).
3. **Day-level vs bout-level fit**: the regression is run at **bout level** for the per-bout features (predictor = `dose_plasma_mg` at day-of-bout; outcome = per-bout feature value), with day-level clustering / day-level random effect to absorb within-day correlation. The per-day aggregations (`bout_count_day` etc.) are fit at day-level mirroring the parent MD spec exactly.
4. **Per-feature β coefficients become the inheritance defaults** for [`bout_level_recovery_dynamics.md` §5.3 Approach A](bout_level_recovery_dynamics.md). The downstream HA pre-regs using Approach A use the **buildup post-CPAP β** (tighter CI per parent MD pattern); afbouw β reported for transparency.
5. **Independent substantive finding framed honestly per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)**: the recalibration's per-feature β pattern (does citalopram act more on `peak_height` than `recovery_half_life`? more on `level` than `dynamics`?) is a research finding in its own right. The finding is reported here (when the calibration runs); it informs but does not gate the parent MD's lock.

**Status**: **r2 LOCKED 2026-06-19** per [CONVENTIONS §2.2 + §2.3](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) audit hooks + [`hypothesis_lock_process.md §3.6`](hypothesis_lock_process.md) compression. Fresh-session audit ([`reviews/bout_level_recovery_dynamics-2026-06-19.md`](../reviews/bout_level_recovery_dynamics-2026-06-19.md), single report covering parent + sub-MD) verdict PASS-with-caveats. The recalibration itself does not run until pipeline construction (a separate downstream session per [`bout_level_recovery_dynamics.md` §7.4](bout_level_recovery_dynamics.md)). Co-locked with parent [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) at the same commit.

---

## 1. What this sub-MD asks, and what it does not

### 1.1 The question

Does citalopram modulate **per-bout recovery-dynamics features** in a graded dose-dependent way? If so, what are the per-feature β coefficients (per mg of plasma citalopram) that downstream HA pre-regs should use to dose-adjust per-bout features under [`bout_level_recovery_dynamics.md` §5.3 Approach A](bout_level_recovery_dynamics.md)?

### 1.2 What this sub-MD does NOT do

- **Does NOT re-derive the daily-aggregate finding.** The daily-aggregate dose-response is locked in [`citalopram_dose_response_stress_mean_sleep.md §5.6`](citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14). This sub-MD is the focused per-bout follow-up.
- **Does NOT extend the dose-response to channels outside the bout-level feature family.** The five primary recovery-dynamics features in [`bout_level_recovery_dynamics.md` §4](bout_level_recovery_dynamics.md) + the two per-day bout aggregations are the scope.
- **Does NOT lock the bout-detection rule.** That lives in [`bout_level_recovery_dynamics.md` §3](bout_level_recovery_dynamics.md). This sub-MD inherits it verbatim; any change to the bout-detection rule invalidates the per-feature β estimates here.
- **Does NOT pre-commit which HA pre-regs adopt the recalibration.** Per [`citalopram_phase_stratification.md` §4](citalopram_phase_stratification.md#4-per-channel-inheritance-rules) — the per-channel inheritance status (load-bearing CONFIRMED vs weak vs REJECTED) is the inheritance trigger. This sub-MD produces the per-feature evidence; per-feature inheritance status is named in §6 of this sub-MD.
- **Does NOT relax the bout-level operand framework-validity gate.** [`bout_level_recovery_dynamics.md` §6](bout_level_recovery_dynamics.md) restricts framework-validity to unmedicated × train × calm-days; that restriction stands regardless of what this sub-MD finds. The cross-phase substantive question is what this sub-MD informs.

### 1.3 Inherited substantive caveats

- **LC recovery trajectory confound** (per parent MD §1.3) carries forward. The afbouw and buildup windows overlap a multi-year LC recovery slope; the linear `days_from_<window>_start` covariate absorbs the local slope inside each regression. The per-feature β estimates are "consistent with a dose-graded modulation of recovery-dynamics on the per-bout feature, after absorbing the local LC-recovery slope", NOT isolated pharmacological causation.
- **Other confounds co-varying with the afbouw window** (seasonality, Breinvoeding) per parent MD §1.3 carry forward. The spring 2025 control + the symmetric buildup test are the principal sensitivity arms.
- **CPAP-end at 2024-04-16 inside buildup** — addressed via the post-CPAP-buffer spec per [`citalopram_dose_response_stress_mean_sleep.md §5.5.2`](citalopram_dose_response_stress_mean_sleep.md#552-post-cpap-buffer-spec-s2-row) (drop first 22 days of buildup; the post-CPAP buildup window is 2024-05-01 → 2024-06-19, n ≈ 50 days). The "parent MD" antecedent in earlier drafts was ambiguous between this MD's local-parent (`bout_level_recovery_dynamics.md`) and the upstream-parent dose-response MD; the upstream-parent dose-response MD is meant — `bout_level_recovery_dynamics.md` has no §5.5.2 of equivalent semantics (r2 absorb 2026-06-19, audit L2 minor antecedent clarification).
- **Bout sparsity per day** (~3-8 bouts/day; some days zero) means the per-bout regression has a non-uniform observation rate across days. The day-level random effect / clustering absorbs within-day correlation; the day-level n drives effective sample size (not bout-level n). At ~70 days per window × ~5 bouts/day ≈ 350 bouts/window but effective n ≈ 70 day-clusters per window. The CI estimates reflect this.

### 1.4 Framing — confirmatory per [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory)

The bout-level dose-response question is downstream of the confirmed daily-aggregate dose-response (parent dose-response MD §5.6 v3 CONFIRMED on three channels). The mechanism prior carries forward verbatim:

1. **Lived-experience prior** (unchanged from parent dose-response MD §1.4 item 1).
2. **Mechanism prior** (unchanged from parent §1.4 item 3): SSRI → serotonergic-autonomic regulation → measurable on stress channels.
3. **Empirical prior on this corpus**: the parent dose-response v3 finding establishes that the same per-minute stress substrate that bout-level features derive from IS dose-modulated at the daily-aggregate level. The bout-level recalibration asks the *finer-resolution* version of that question.

Per [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory), confirmatory framing is justified.

### 1.5 Four-input bar at the sub-MD layer (r2 absorb 2026-06-19, audit L1 MEDIUM)

Per [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice), the four-input bar binds at the sub-MD layer too — not only by inheritance from the parent dose-response MD or from [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) §2. The audit (L1.1 + L1.3) flagged that best-practices were implicit by inheritance + structured trade-off vision was absent. This subsection makes both explicit.

#### 1.5.1 Best-practices standards

- **Linear mixed-effects regression with day-level random intercept + cluster-robust SE** is the standard n-of-1 self-tracked counterfactual-inference pattern per [Daza 2018](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) (referenced via [`citalopram_phase_stratification §1.3`](citalopram_phase_stratification.md#13-the-anchor-claim-the-finding-this-framework-implements)). The day-cluster absorbs within-day correlation across bouts; cluster-robust SE handles heteroskedasticity across days without specifying the within-day correlation structure parametrically.
- **Per-feature independent regressions** (rather than joint multivariate / partial-pooling) is the project-canonical pattern at the daily-aggregate layer (parent dose-response MD §4.6 multi-channel runs are per-channel independent regressions reported alongside Holm step-down companions). Inheriting the same pattern at per-bout layer preserves discipline-coherence + interpretability per feature.
- **Three-pronged spec** (afbouw primary + buildup post-CPAP secondary + spring 2025 control) inherits verbatim from [`citalopram_dose_response_stress_mean_sleep.md §5`](citalopram_dose_response_stress_mean_sleep.md#5-the-five-pronged-spec-locked) and is the project's anchor for citalopram dose-response identification in within-subject observational data.

#### 1.5.2 Established literature

- The parent dose-response MD's literature anchors carry forward verbatim (Daza 2018 named above; PK/PD pharmacokinetics for SSRI plasma half-life modelled per [`citalopram_dose_response_stress_mean_sleep.md §2.3`](citalopram_dose_response_stress_mean_sleep.md#23-pk-smoothed-plasma-proxy-primary-exposure)).
- **Per-bout dose-response calibration literature is honestly downgraded to deferred-but-named** — no direct n-of-1 anchor for per-event recovery-feature dose calibration exists in the project's literature folder. Candidate anchors (queued for fetch via `_pending_literature_fetch.md`): Stanley/Buchheit/Plews 2013 on per-event HRV-recovery features (per parent MD §2.2 deferral). The methodology stands on the established daily-aggregate dose-response literature applied at finer-resolution operand.

#### 1.5.3 Tradeoff vision

Three alternatives to the chosen specification:

| dimension | linear-extension assumption (no recalibration) | **per-feature independent fit (CHOSEN)** | joint multivariate with shrinkage |
|---|---|---|---|
| Power | high (uses daily-aggregate β at full daily-aggregate n) | medium (per-feature n at bout level; effective n ≈ 70 day-clusters/window) | medium-high (cross-feature pooling) |
| Interpretability per feature | low (β assumed identical to daily) | high (per-feature β with own CI) | medium (per-feature shrunken toward joint mean) |
| Robustness to feature-specific dose-response heterogeneity | low (assumes uniform) | high (each feature has its own β) | medium (shrinkage biases toward joint mean even if feature β differs) |
| Audit-defensibility for downstream Approach A inheritance | low (assumption unaudited) | high (per-feature CIs auditable) | medium (shrinkage prior is itself a choice) |
| Cost / complexity | none (re-uses daily β) | low (parent MD's spec form re-applied) | medium-high (Bayesian or partial-pooling machinery) |
| n=1 single-subject suitability | poor (linearity-of-extension is the question) | good | good but adds prior choice |

**Per-feature independent fit wins on robustness + audit-defensibility + interpretability** at moderate cost. Linear-extension (no recalibration) is the substantive null this sub-MD exists to falsify or confirm; assuming it is what the sub-MD's question rejects on first principles. Joint-with-shrinkage is the principled alternative if cross-feature pooling were known to help, but the n=1 design + the substantive-finding question "does citalopram act differently on level vs dynamics?" makes per-feature independence the right framing — shrinkage would bias the level-vs-dynamics read.

The implicit handling at §3.7 (Holm step-down across the 5 per-bout features as descriptive overlay) is the multiplicity-companion to per-feature independence; per-pre-reg multiplicity discipline is deferred to downstream HA pre-regs per parent MD §5.2 (PM-confirmed 2026-06-19).

#### 1.5.4 Research limitations + objectives

- **Per-bout n is the binding constraint**. ~70 days × ~5 bouts/day ≈ 350 bouts/window, but effective n ≈ 70 day-clusters per window after cluster-robust SE. CIs are wider than daily-aggregate CIs proportionally.
- **Model-form assumptions**: linear additive dose effect per feature (no Emax / hill curve); compound-symmetry day-level random intercept (no within-day AR(1) at primary; §3.3 Sensitivity H adds the AR(1) alternative). Both surfaced at §3.1 + §7 caveats.
- **Firstbeat-input opacity inherits from parent MD §2.4** (r2-absorbed at parent): per-bout features at minute resolution AMPLIFY Firstbeat-algorithm-derived artefacts that daily aggregate smooths. A CONFIRMED per-feature β is a statement about the per-minute-trace operand's dose-modulation, not autonomic-recovery physiology directly (§7 caveat 4 carries this verbatim at this MD).
- **Cross-bout independence assumption within day is rejected** by the day-cluster framing — bouts within a day share day-state. Block-bootstrap (Sensitivity A) at 7-day blocks per [`permutation_null_block_length.md`](permutation_null_block_length.md) preserves the day as the resampling unit; within-day bout structure rides intact.

**Specific objectives the sub-MD serves**: produce per-feature β + 95% CI for the 5 per-bout primary features + 2 per-day bout aggregations, suitable for direct inheritance by [`bout_level_recovery_dynamics.md §5.3 Approach A`](bout_level_recovery_dynamics.md) at downstream HA pre-reg lock time; produce the independent substantive level-vs-dynamics read per §5.5; produce the per-feature inheritance assignment per §6 (which features Approach A dose-adjusts at lock vs uses dose-naive).

---

## 2. The per-bout features in scope

Per [`bout_level_recovery_dynamics.md` §4](bout_level_recovery_dynamics.md), the five primary recovery-dynamics features:

| feature | unit | prior expected sign (higher plasma → ?) | admits `_lagged_lcera` variant? | rationale |
|---|---|---|---|---|
| `peak_height` | Garmin 0-100 | **+1** (higher plasma → higher peak) | **yes** — `peak_height_lagged_lcera = peak_height − μ_peak,lcera_lagged(d)` | inherits direction from daily-aggregate `all_day_stress_avg` and `stress_mean_sleep` CONFIRMED-positive; per-bout peak should track per-day mean's dose-response. Lagged-lcera variant is well-defined (per-day mean of peak_height on `[d-90, d-30]` LC-era days) |
| `pre_bout_baseline` | Garmin 0-100 | **+1** (higher plasma → higher baseline) | **yes** — same construction as peak_height | same mechanism as above; baseline stress sits higher under elevated serotonergic tone. Lagged-lcera variant well-defined |
| `recovery_half_life` | minutes | **+1** (higher plasma → slower recovery) | **yes** — `recovery_half_life_lagged_lcera = recovery_half_life − μ_halflife,lcera_lagged(d)` | mechanism: elevated sympathetic tone slows parasympathetic re-engagement → longer half-life. Wiggers' "stuck sympathetic" + the inherited dose-modulation evidence on stress channels both point this way. Lagged-lcera variant well-defined |
| `decay_slope` | stress/min (negative) | **+1** in absolute value (higher plasma → less negative slope) | **no** — feature is itself a derivative; per [CONVENTIONS §3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) lagged-baseline pattern applies to LEVEL features, not slopes. Sensitivity C reports as N/A for decay_slope; raw value used as primary | mechanism: slower recovery = shallower decay; same mechanism as half-life. Implementation: report β on absolute value of slope (less negative = closer to zero under higher plasma) |
| `AUC_above_baseline` | stress·min | **+1** (higher plasma → larger AUC) | **yes** — `AUC_above_baseline_lagged_lcera = AUC_above_baseline − μ_AUC,lcera_lagged(d)`; integrates per-day mean AUC | composite: higher peak + slower recovery → larger area. Should track the most strongly. Lagged-lcera variant well-defined (integral of a level feature is itself a level-like feature) |

And the two per-day bout aggregations:

| aggregation | unit | prior expected sign | admits `_lagged_lcera` variant? | rationale |
|---|---|---|---|---|
| `bout_count_day` | int | **+1** (higher plasma → more bouts) | **yes** — `bout_count_day_lagged_lcera = bout_count_day − μ_count,lcera_lagged(d)` | higher baseline sympathetic tone → more frequent 60-crossings; mechanism is the same that drives `peak_height` directional prior. Per-day count is itself level-like; lagged variant well-defined |
| `bout_n_fast_recovery_day` | int | **−1** (higher plasma → fewer fast-recovery bouts) | **yes** — analogous construction; mirrors HA11 v1's u_dip_count lagged-lcera pattern | mechanism: SSRI-induced slower recovery → fewer bouts meeting the `recovery_half_life ≤ 15 min` AND `tail_length ≤ 45 min` thresholds. **This is the framework-validity operand**; its dose-modulation is a SECONDARY check that the framework-validity gate's reference frame is internally consistent. (The gate itself is restricted to unmedicated stratum per parent §6.) |

**Per-feature lagged-lcera variant admission column added at r2 (2026-06-19, audit L3 MEDIUM)**: pins which features admit Sensitivity C (lagged-lcera variant) per [CONVENTIONS §3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses). `decay_slope` is the sole non-admitter (derivative feature, not level); §3.4 null-finding pre-spec condition 4 collapses to three conditions for `decay_slope` accordingly (the four-condition pre-spec from §3.4 applies for the six features that admit the variant).

**The prior expected signs are PRE-SPECIFIED**. A confirmed β in the predicted direction strengthens the dose-response framework; a β in the unexpected direction (or null) is a diagnostic finding about which features citalopram does/does not modulate. Per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), both directions are interpretable; the predicted direction is the prior-consistent reading.

---

## 3. Analysis specification (the locking section)

Inherits the spec form of [`citalopram_dose_response_stress_mean_sleep.md §4`](citalopram_dose_response_stress_mean_sleep.md#4-analysis-specification-the-locking-section) verbatim where applicable; per-feature variations explicitly named.

### 3.1 Primary model (per feature)

For each per-bout feature `f` ∈ {peak_height, pre_bout_baseline, recovery_half_life, decay_slope, AUC_above_baseline}, fit a linear mixed-effects regression at the bout-level:

```
f(bout_i, d) = β_0 + β_dose * dose_plasma_mg(d) + β_time * days_from_window_start(d) + u_d + ε(bout_i, d)
```

where:
- `f(bout_i, d)` is the per-bout feature value for bout `i` on day `d`,
- `dose_plasma_mg(d)` is the PK-smoothed plasma exposure per [`citalopram_dose_response_stress_mean_sleep.md §2.3`](citalopram_dose_response_stress_mean_sleep.md#23-pk-smoothed-plasma-proxy-primary-exposure),
- `days_from_window_start(d)` is the linear time covariate per parent dose-response MD,
- `u_d ~ N(0, σ²_day)` is a day-level random intercept absorbing within-day correlation across bouts,
- `ε(bout_i, d) ~ N(0, σ²)` is the residual.

**Window**: same windows as parent dose-response MD spec — afbouw 2026 primary (2026-03-20 → 2026-06-05), buildup 2024 post-CPAP-buffer (2024-05-01 → 2024-06-19), spring 2025 control (2025-03-20 → 2025-06-05).

**Pre-specified hypothesis** (per §2 expected signs + §1.4 confirmatory framing):

- H0: β_dose = 0
- H1: β_dose has the §2 expected sign

One-sided test, α = 0.05, per feature.

For the per-day aggregations `bout_count_day` and `bout_n_fast_recovery_day`, the regression collapses to day-level (no bout-level random effect; just the standard parent-MD form):

```
agg(d) = β_0 + β_dose * dose_plasma_mg(d) + β_time * days_from_window_start(d) + ε(d)
```

### 3.2 Standard errors

For bout-level fits (5 per-bout features): **cluster-robust standard errors at the day level**. Mirrors Newey-West HAC at the day-resolution for the day-level fits; for bout-level fits the day-cluster is the analogue. Use `cov_type='cluster'` with `cluster_groups=date`.

For day-level fits (2 per-day aggregations): **Newey-West HAC** per parent MD §4.2 verbatim, with Andrews 1991 lag selection.

Both yield 95% CIs + one-sided p-values per feature × per window.

### 3.3 Sensitivity sweeps (per feature)

Inherits the sensitivity-sweep structure from parent dose-response MD §4.3 verbatim:

- **Sensitivity A — block bootstrap** at 7-day blocks, 1000 iterations. Resampling at the day level (preserving within-day bout structure inside each resampled block).
- **Sensitivity B — prescribed-step dose representation** (substitute `dose_prescribed_mg` for `dose_plasma_mg`).
- **Sensitivity C — lagged-lcera variant of the feature** as outcome, where the feature has a lagged-lcera analogue (e.g. `peak_height_lagged_lcera` if computed; the lagged-lcera baseline is computed per-feature at the day-mean-of-feature level). For features without a sensible lagged-lcera variant (e.g. `decay_slope`), the sensitivity column is reported as "N/A — feature does not admit standard lagged-baseline variant; raw value used as primary".
- **Sensitivity D — alternative HAC / cluster lag**: report a tighter and a looser variant.
- **Sensitivity E — crash-drop** (CONVENTIONS §3.4 audit hook): re-fit with `is_crash == True` rows dropped from the day pool.
- **Sensitivity F — nonlinear time term**: 4-knot natural cubic spline on `days_from_window_start` replacing the linear time covariate.
- **Sensitivity G (bout-level specific)** — exclude motion-confounded bouts (`motion_confound_flag == True`). The primary includes all bouts per [`bout_level_recovery_dynamics.md` §3.4](bout_level_recovery_dynamics.md); this sensitivity arm tests whether the dose-response is motion-driven.
- **Sensitivity H (bout-level specific, r2 absorb 2026-06-19, audit L3 MEDIUM)** — within-day AR(1) residual structure as alternative covariance specification. The §3.1 primary uses compound-symmetry (day-level random intercept absorbs the day-mean shift component of within-day correlation, but NOT the autocorrelation component if consecutive bouts within a day share state beyond day-mean — e.g. a heavy-T morning followed by a slower-recovery afternoon means bouts share "today is heavy-T" state). Sensitivity H re-fits each per-bout feature regression with AR(1) residual structure within day-blocks (alongside the day-level random intercept; specifically: `vc_formula={'AR1': '0 + C(date)'}` or equivalent via `MixedLM` with `cov_struct=AR(1)` on time-ordered within-day bout sequence) and reports whether β estimates + 95% CIs shift meaningfully relative to compound-symmetry. Headline retains compound-symmetry; H is descriptive overlay. **Estimability caveat**: within-day bout n ≈ 3-8; the AR(1) parameter is noisy per day-block. If the per-day AR(1) parameter cannot be reliably estimated, Sensitivity H reports as "diagnostic-only — within-day n too small for stable AR(1) estimation; CIs compared narratively rather than statistically tested for difference". Directly addresses §7 caveat 1 ("A different covariance structure could shift the CIs") at sensitivity-arm level.

**Visual companion — monotonicity scatter** (per parent MD §4.3): 4-point plot per feature with the four prescribed-dose plateau values on the x-axis and the per-plateau residuals on the y-axis. Same construction as parent MD; one panel per feature for the at-a-glance read.

### 3.4 Pre-spec for null finding (per feature)

A **null finding** on feature `f` is declared if and only if all four conditions hold:

1. Primary cluster-robust 95% CI for `β_dose(f)` fully contains zero (in afbouw OR buildup post-CPAP — whichever the headline assignment names; see §3.5).
2. |β_dose(f)| < 0.05 × SD(f) per mg of plasma (effect-size gating; same form as parent MD §4.4 condition 2 at per-feature SD scale).
3. Block-bootstrap (Sensitivity A) 95% CI also contains zero.
4. The lagged-lcera variant (Sensitivity C, if applicable) p-value > 0.05.

Any one condition failing → not a null finding; the read moves to effect-size + caveats interpretation per §5.

### 3.5 Headline assignment for the inheritance defaults

For each feature, the **buildup post-CPAP β is the headline inheritance default** per [`citalopram_phase_stratification.md §5.B`](citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests) implicit tradeoff (tighter CIs from a dose-naive system → conservative-against-undercorrection at the cost of potential overcorrection at steady-state). Afbouw β reported for transparency.

The afbouw + buildup post-CPAP + spring 2025 control verdicts ALL feed into the per-feature inheritance status assignment (§6 of this MD):
- **CONFIRMED**: sign-concordant β in afbouw + buildup; buildup CI excludes zero in prior direction; flat spring 2025 control.
- **weakly consistent**: sign-concordant but buildup CI brushes zero.
- **partial**: only one of afbouw/buildup has data or fits.
- **REJECTED**: sign-discordant OR both CIs cross zero.

Per-feature inheritance status determines which features [`bout_level_recovery_dynamics.md` §5.3 Approach A](bout_level_recovery_dynamics.md) actually dose-adjusts vs leaves un-adjusted.

### 3.6 Asymmetric sub-phase contribution (caveat)

Same as parent MD §4.5: the 8mg sub-phase has only ~2 fully observed days at the 8mg steady-state plateau. Bout-level analysis amplifies this: ~2 days × ~5 bouts/day = ~10 bouts at 8mg steady-state. Surface in script output per feature; the regression's leverage at bout-level is dominantly on the 30→20→10 transitions. The 8mg plateau contributes minimally and that contribution should be visible in the residual diagnostics.

### 3.7 What this analysis does not include

- No correction for multiple comparisons across the 7 per-feature × per-window fits. Each feature × window is its own pre-spec'd hypothesis with a pre-specified expected sign; family-wise multiplicity is conceptually present but the parent MD §4.6 disclosure pattern carries: each test is on a distinct mechanistically-meaningful feature, not a multiple-comparison fishing expedition. Holm step-down across the 5 per-bout features per window IS reported as a secondary descriptive overlay (mirrors parent MD's Holm pattern for the multi-channel run).
- No mediator analysis (does dose modulate `recovery_half_life` *via* `peak_height`?). Out of scope for this MD; queued as a separate methodology follow-up if the per-feature pattern surfaces a mediator candidate.
- No fitted-curve PK/PD model (Emax / hill / etc.). Linear-in-dose by §3.1 per parent MD §4.1 reasoning; same trade-offs.

---

## 4. The recalibration output schema

The recalibration emits a structured result file (per-feature × per-window × per-sensitivity) suitable for inheritance by downstream HA pre-regs. Schema:

```
feature, window, spec, n_bouts, n_days, beta_dose, beta_dose_lo95, beta_dose_hi95, p_value, sign_match_prior, verdict
```

where:
- `feature` ∈ {peak_height, pre_bout_baseline, recovery_half_life, decay_slope, AUC_above_baseline, bout_count_day, bout_n_fast_recovery_day}
- `window` ∈ {afbouw_2026, buildup_post_cpap_2024, spring_2025_control}
- `spec` ∈ {primary, sens_A_block_bootstrap, sens_B_prescribed_step, sens_C_lagged_lcera, sens_D_alt_lag, sens_E_crash_drop, sens_F_nonlinear_time, sens_G_motion_clean, sens_H_within_day_ar1}
- `verdict` ∈ {CONFIRMED, weakly_consistent, partial, REJECTED, NULL}

The "headline inheritance β" per feature is the row with `window = buildup_post_cpap_2024 AND spec = primary`. Downstream HA pre-regs using Approach A read those rows directly.

---

## 5. What the finding informs

### 5.1 If β_dose has prior-expected sign and survives sensitivity (per feature)

The feature is CONFIRMED dose-modulated. Its β coefficient is the inheritance default for [`bout_level_recovery_dynamics.md` §5.3 Approach A](bout_level_recovery_dynamics.md). Downstream HA pre-regs using Approach A on this feature apply the dose-adjustment per §5.B pattern.

**Per-feature substantive finding** (independent of inheritance): a CONFIRMED β on `recovery_half_life` would be the first n=1 demonstration on this corpus that citalopram modulates recovery *dynamics*, not just stress *level*. The substantive finding deserves its own paragraph in the result.md when the calibration runs.

### 5.2 If null per §3.4 pre-spec (per feature)

The feature is NOT dose-modulated detectably under this analytical design (n=1, 5 features × 3 windows × bout-level n=10s-100s).

Three reads remain open per parent MD §5.2 pattern:
- The daily-aggregate dose-response on the source channel (stress-related daily channels) does NOT propagate to this per-bout feature — the level vs dynamics separation is real and citalopram acts on level but not dynamics for THIS feature.
- A real effect exists but is below the bout-level detection floor.
- The PK-smoothed assumption is materially wrong for this feature.

A NULL finding on `recovery_half_life` specifically (the most direct dynamics feature) is a NOTABLE substantive finding: it would say citalopram modulates stress level but NOT recovery dynamics on this corpus.

### 5.3 If β_dose has unexpected sign (counter-prior direction)

Per parent MD §5.3 pattern: surface candidate exogenous explanations against `annotations.yaml` events in the window; treat as a data-quality + confound diagnostic before treating as a finding. The mechanism prior is sufficiently strong (citalopram → serotonergic tone → autonomic load) that a sign-reversal needs the diagnostic before the verdict.

### 5.4 Per-feature inheritance assignment for [`bout_level_recovery_dynamics.md` §5.3 Approach A](bout_level_recovery_dynamics.md)

The five per-bout features partition into:

- **Load-bearing CONFIRMED features**: Approach A dose-adjustment applied with the buildup post-CPAP β as inheritance default.
- **Weakly-consistent features**: §5.A per-phase stratification recommended as sensitivity arm in downstream pre-regs; not load-bearing for cross-phase tests.
- **NULL / REJECTED features**: dose-adjustment NOT applied; the feature is dose-naive on this corpus and can be used freely across phases.

Per [`citalopram_phase_stratification.md §4`](citalopram_phase_stratification.md#4-per-channel-inheritance-rules) the audit-hook applies: downstream HA pre-regs whose predictor or outcome references a CONFIRMED bout-level feature MUST adopt Approach §5.A / §5.B / §5.C from the parent framework. The per-feature inheritance status is what triggers that obligation.

### 5.5 The independent substantive finding — dynamics vs level

The recalibration's per-feature β pattern can be read across the feature set:

- If all 5 features show CONFIRMED dose-response in the same direction → citalopram acts uniformly across level + dynamics; the daily-aggregate β extends as a uniform multiplier.
- If `peak_height` + `pre_bout_baseline` CONFIRMED but `recovery_half_life` + `decay_slope` NULL → citalopram acts on **level** (where the system sits) but NOT on **dynamics** (how fast it recovers). Substantively novel.
- If `recovery_half_life` + `decay_slope` CONFIRMED but `peak_height` + `pre_bout_baseline` NULL → citalopram acts on **dynamics** (recovery speed) but NOT on **level** (peak amplitude). Also substantively novel; suggests SSRI modulates recovery without changing baseline arousal threshold.
- Mixed patterns → reported honestly.

The pattern is an independent research finding; it is reported in this sub-MD's result section (when the calibration runs) and propagates back to inform [`citalopram_phase_stratification.md` §2](citalopram_phase_stratification.md#2-the-substantive-finding-being-framework-ised) (the substantive-finding table expands with per-bout-feature rows).

---

## 6. Per-feature inheritance assignment (will be filled at result-time)

This section will be populated by the recalibration result and locked into this sub-MD as r2. The table below is the empty schema; row entries populate after the calibration script runs.

| feature | verdict | buildup post-CPAP β (CI95, p) | afbouw β | spring 2025 control β_time | Approach A inheritance? |
|---|---|---|---|---|---|
| `peak_height` | (TBD) | (TBD) | (TBD) | (TBD) | (TBD) |
| `pre_bout_baseline` | (TBD) | (TBD) | (TBD) | (TBD) | (TBD) |
| `recovery_half_life` | (TBD) | (TBD) | (TBD) | (TBD) | (TBD) |
| `decay_slope` | (TBD) | (TBD) | (TBD) | (TBD) | (TBD) |
| `AUC_above_baseline` | (TBD) | (TBD) | (TBD) | (TBD) | (TBD) |
| `bout_count_day` | (TBD) | (TBD) | (TBD) | (TBD) | (TBD) |
| `bout_n_fast_recovery_day` | (TBD) | (TBD) | (TBD) | (TBD) | (TBD) |

Once filled, the table becomes the inheritance source for [`bout_level_recovery_dynamics.md` §5.3 Approach A](bout_level_recovery_dynamics.md). Downstream HA pre-regs cite this table directly.

---

## 7. Caveats

Per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no):

1. **The recalibration's β estimates are conditional on the §3.1 mixed-effects specification.** A different covariance structure (e.g. AR(1) within-day residuals instead of compound symmetry) could shift the CIs. Downstream pre-regs should treat the headline β as the locked point estimate but recognise the CI width is conditional on specification choice.
2. **Bout-level n is much smaller than day-level n.** ~70 days × ~5 bouts/day ≈ 350 bouts/window, but effective n ≈ 70 day-clusters per window after cluster-robust SE. CIs are wider than the parent MD's daily-aggregate CIs proportionally. The per-feature β precision will be the binding constraint on Approach A's downstream usefulness.
3. **Per-feature β inherits parent MD §1.3 confound stack.** LC recovery trajectory, seasonality, Breinvoeding, CPAP-end. Same mitigations (linear time covariate, three-pronged test) carry forward; not re-stated per feature.
4. **The recalibration runs at bout-level features that did not exist at parent MD §5.5 / §5.6 time.** Per [CONVENTIONS §4.1](../CONVENTIONS.md#41-no-interpretive-marks-on-raw-or-descriptive-layers), the per-bout features are operational descriptions of the per-minute trace; they are NOT mechanistic measurements. A CONFIRMED β on `recovery_half_life` is a statement about the per-minute-trace operand's dose-modulation, not directly about autonomic-recovery physiology.
5. **Approach A's downstream usefulness depends on the recalibration β being correct.** A wrong β under-corrects (or overcorrects). The downstream HA pre-regs using Approach A should pre-spec the sensitivity of their verdict to the upper/lower CI bounds of the relevant β (per parent MD §8 caveat 3). If the verdict swings under the CI range, the recalibration's precision needs improvement before the inheritance is load-bearing.
6. **n=1 single-subject + observational + multi-source.** Inherits parent MD §1.3 caveat verbatim. The recalibration's β estimates describe THIS participant's per-bout dose-response; cross-subject generalisation is out of scope.

---

## 8. Status + revision log

**Status**: **r2 LOCKED 2026-06-19** per [CONVENTIONS §2.2 + §2.3](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) + [`hypothesis_lock_process.md §3.6`](hypothesis_lock_process.md) compression. Audit ([`reviews/bout_level_recovery_dynamics-2026-06-19.md`](../reviews/bout_level_recovery_dynamics-2026-06-19.md)) verdict PASS-with-caveats; r2 absorbs are mechanical. Co-locked with parent at this commit. The recalibration itself does not run until pipeline construction (separate downstream session).

### Revision log

| version | date | change |
|---|---|---|
| r1 | 2026-06-19 | Initial draft as sub-MD spun off from [`bout_level_recovery_dynamics.md` §5.4](bout_level_recovery_dynamics.md). Five per-bout primary features + two per-day aggregations in scope. Three-pronged spec inherited from parent dose-response MD (afbouw / buildup post-CPAP / spring 2025 control). Mixed-effects regression at bout-level with day-cluster SE; per-day aggregations at day-level via Newey-West HAC. §6 inheritance table is the empty schema; populates at result-time. |
| r2 | 2026-06-19 | §3.6-compression r2 absorbing audit fires. Sub-MD absorbs (4): (11) §1.5 standalone four-input bar added with §1.5.1 best-practices / §1.5.2 literature deferred-but-named / §1.5.3 tradeoff vision table {linear-extension / per-feature independent (CHOSEN) / joint with shrinkage} / §1.5.4 limitations + objectives [L1 MEDIUM]; (12) §1.3 caveat 3 "parent MD §5.5.2" antecedent clarified to upstream `citalopram_dose_response_stress_mean_sleep §5.5.2` (not local-parent `bout_level_recovery_dynamics`) [L2 minor]; (13) §3.3 Sensitivity H added (within-day AR(1) residual structure as alternative covariance specification; diagnostic-only when within-day n too small for stable AR(1)) + §4 schema spec list extended [L3 MEDIUM]; (14) §2 features table extended with `admits _lagged_lcera variant?` column per feature (`decay_slope` only non-admitter as derivative feature; §3.4 null-finding pre-spec collapses to three conditions for `decay_slope`) [L3 MEDIUM]. **LOCKED** 2026-06-19 at co-lock-commit. |

---

## 9. Cross-references

- [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) — parent MD; §5.4 committed this sub-MD; §5.3 Approach A inherits the recalibration's β coefficients.
- [`citalopram_dose_response_stress_mean_sleep.md §5.6`](citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) — daily-aggregate dose-response v3 multi-channel results; methodological template this sub-MD inherits + per-channel verdict pattern this sub-MD's §6 mirrors at per-bout layer.
- [`citalopram_phase_stratification.md` §4 + §5](citalopram_phase_stratification.md#4-per-channel-inheritance-rules) — framework MD this sub-MD's §6 inheritance assignment feeds.
- [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md) — parent Layer-1 sweep; the per-feature recalibration is the same shape of test at finer-resolution operand.
- [`permutation_null_block_length.md`](permutation_null_block_length.md) — block-length anchor (E[L]=7 days) inherited verbatim.
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) — the downstream HA pre-reg lock arc that uses this sub-MD's inheritance table.
- [CONVENTIONS §1.1, §2.2, §3, §4.1-§4.3](../CONVENTIONS.md) — producer-mode + four-input bar + audit hooks + interpretive discipline.

---

*Producer-mode methodology sub-MD. Update when the recalibration script runs and the §6 inheritance table is populated (r2 absorption + lock); when a downstream HA pre-reg's verdict-sensitivity to the recalibration β surfaces a precision-improvement need (then the recalibration runs again with refined spec, creating r3 with r2 archived).*
