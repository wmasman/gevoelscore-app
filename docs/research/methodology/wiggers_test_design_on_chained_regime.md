# Wiggers test design on the chained crash regime

*Methodology for faithful testing of Wiggers' smartwatch-pacing hypotheses on the personal n=1 corpus. Drafted 2026-06-12.*

---

## Aim

This document is the bridge between **what Wiggers actually claimed** (captured verbatim with line refs in the [verification log of `wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md)) and **how we faithfully test each claim on this corpus** (the per-hypothesis pre-reg files in [`../analyses/hypotheses/`](../analyses/hypotheses/)).

It is **not**:

- A pre-registration. Each hypothesis still gets its own pre-reg file with sample size, alpha, train/validate split, primary vs secondary metrics, and walk-forward setup.
- A re-derivation of the HRV-proxy framing. That lives in [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md); this doc inherits the conclusion and the constraints.
- A re-derivation of the crash labels. Those are locked in [`../analyses/hypotheses/crash_v2-definition/definition.md`](../analyses/hypotheses/crash_v2-definition/definition.md).

It **is**:

- The taxonomy of statistical methods we use, with one method per Wiggers claim type ("operationalization class").
- The faithfulness rubric per class — when is a test correctly targeting the Wiggers claim, and when has it drifted.
- The corpus-specific adjustments needed because crashes on this dataset are **chained**, not isolated events (62% of crash episodes chain within 14 days; only 1 of 29 is isolated by a 30-day rule).
- The hypothesis → class assignment for all 23 testable + 11 partial Wiggers hypotheses.
- Worked-example anchors for the six hypotheses already source-verified (A1, A4, C3, C4, H1, H5).

The single load-bearing principle:

> **Faithfulness has three layers**: paraphrase, operationalization, statistical method. A perfectly verified paraphrase can still produce an infidel test if the statistical method is misaligned. This doc holds the operationalization → statistical-method link.

---

## Faithfulness — the three layers

| layer | what it is | where it lives | example for A1 |
|---|---|---|---|
| 1. Paraphrase | "What did Wiggers actually say?" | [verification log](../wiggers_testable_hypotheses.md#source-verification-log) | *"I'm already unhappy with a resting heart rate that's 5–10 beats higher. I have really thoroughly overdone it when my resting heart rate is a 100 bpm instead of 60 for hours."* (PDF lines 165-177) |
| 2. Operationalization | "What testable claim does this become on our master columns?" | this doc + the pre-reg variable mapping in [`../wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) | RHR(t0) elevation scales monotonically with exertion(t-1 or t-2) when stratified by ordinal exertion quartile |
| 3. Statistical method | "What test answers that claim with appropriate power and correction?" | this doc (canonical method per class) + per-hypothesis pre-reg | Jonckheere-Terpstra ordinal test; alpha 0.05 with Bonferroni correction across the four primary tests; walk-forward train (2022-09-03 → 2023-12-31) / validate (2024-01-01 → today) |

An "unfaithful" test fails at any layer. The verification log handles drift at layer 1; this doc handles drift at layer 2 and 3.

---

## Corpus geometry — why "chained regime" appears in the title

The 29 crash episodes in `labels_crash_v2.csv` are **not** independent point events:

- **62% chain within 14 days** of another crash episode (per the crash_v2 definition + Layer 3 descriptive run; see [`../methodology/crash_episode_prolonged.md`](crash_episode_prolonged.md)).
- **Only 1 of 29 crashes is "isolated"** by a 30-day rule. The 30-day isolation gate is therefore not a viable analytical filter on this corpus.
- 79 dips chain into 15 dip clusters using a 7-day rule (per the crash_v2 locked spec).

The standard pre-registered approach in the smartwatch-pacing literature assumes crashes are independent events at `t0`, with clean `t-N … t+N` peri-event windows that do not overlap. On this corpus that assumption is violated for the majority of crash episodes — the `t-3` day of crash N+1 is often the `t+1` or `t+2` day of crash N.

This forces three changes that propagate through every operationalization class:

1. **Peri-event windows must declare an overlap policy.** Options: drop chain-internal days from the window; mark chain position as a covariate; restrict primary tests to the small isolated-crash subset (n ≤ 5).
2. **Within-day metrics (A4, C4) are less affected** because they describe state at `t0` independent of `t±N` neighbours. They remain the cleanest tests on this corpus.
3. **Long-window CCF lag profiles need within-baseline-window enforcement.** Comparing a 2023 t-3 to a 2025 t0 conflates PEM signature with multi-year baseline drift.

Per-class adjustments are documented in each class section below.

---

## The four operationalization classes

Every faithfully-testable Wiggers claim falls into one of four operationalization classes. The class assignment determines the canonical statistical method.

### Class 1: CCF lead-lag (CCF)

**When it applies**: Wiggers claims that metric X *responds to* exertion over time, or that one metric *leads* another in time. The directional claim is what is being tested, not a same-day association.

**Hypotheses in this class**: A3 (night RHR peri-event), H1 (wearable leads gevoelscore crash), H5 (per-metric lag profile), parts of B1-B5 (under proxy framing), parts of H2, H3.

**Canonical statistical method**:

1. Compute first-differenced series for both predictor and outcome (stationarity).
2. Restrict to the long-covid era (`lc_phase == "lc"`, dates ≥ 2022-04-04) per [[project_lc_era_boundaries]]. Drop the corona-infection window (2022-03-21 to 2022-04-03).
3. Compute cross-correlation function across lags `-10 … +10` days.
4. Report `argmax-ρ` (lag at which correlation peaks) and the peak-ρ value.
5. Bootstrap CI on `argmax-ρ` per channel (1000 resamples, block bootstrap with block length = autocorrelation decay time ~7 days).
6. **Direction confirmation**: predictor leads outcome iff `argmax-ρ` is at a strictly negative lag with peak-ρ outside the bootstrap CI for shuffled-permutation null.

**Faithfulness rubric**:

| element | faithful when | drifted when |
|---|---|---|
| Series stationarity | first-differenced or detrended | raw rolling-baseline series (autocorrelation manufactures spurious peak-ρ) |
| Window | ±10 days minimum | shorter than the longest claimed Wiggers lag (HRV: "several days"; PDF lines 925-928) |
| Direction inference | from `argmax-ρ` sign + bootstrap CI | from arbitrary lag-0 correlation magnitude |
| Multiple-channel comparison | per-metric independently, plus an explicit ordering test if H5-style | combining channels into a single composite and reporting one peak-ρ |

**Chained-regime adjustment**:

- Use block bootstrap (block length ~7 days) to capture within-episode autocorrelation.
- Mark days inside a multi-day crash episode separately. Report CCF with and without chain-internal days dropped as a sensitivity row per [[feedback_crash_distortion_sensitivity]].
- For H5 ordering tests specifically: the ordering claim is robust to chaining (it's about relative lag, not absolute lag magnitude). Chaining mostly affects single-channel lag CI width, not the ordering inference.

**Worked example**: H5 ordering test (see § Worked-example anchors).

### Class 2: Within-event same-day (WE)

**When it applies**: Wiggers claims that on a specific day-class (crash day, post-overexertion day, etc.) the metric looks like Z. The claim is about state at `t0` conditional on a day-classification, not about cross-time leading.

**Hypotheses in this class**: A4 (sustained HR elevation on overexertion days), C4 (stress decay + walls + t+1 reactivity after heavy exertion), G1 (respiration on crash days), F1 (sleep duration on PEM nights), parts of D5.

**Canonical statistical method**:

1. Define the day-classification (binary or ordinal). Use the v3.2 lagged columns per [[feedback_use_lagged_exertion_for_pem]]: `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` for "overexertion day"; `is_crash` for "crash day"; etc.
2. Compute the metric of interest at `t0` (or `t+1` if Wiggers specifies next-day reactivity, e.g. C4 secondary).
3. Stratified comparison: metric distribution on the classified day-class vs the complement.
4. Test: Mann-Whitney U (non-parametric, robust to autocorrelation) for the primary; report median + IQR per stratum.
5. Effect size: Cliff's delta (ordinal effect size) or Cohen's d depending on metric distribution.
6. **Walk-forward gate**: any positive primary result must replicate at α=0.10 on the validate era (2024-01-01 → today) before being claimed.

**Faithfulness rubric**:

| element | faithful when | drifted when |
|---|---|---|
| Day-classification | uses Wiggers' own framing where possible (e.g. "heavy exertion" → exertion_class_lagged_lcera ∈ {heavy, very_heavy}; "crash" → is_crash); lagged column for PEM-pacing per memory | uses raw same-day exertion (no lag) when Wiggers explicitly references "the activity you did just before you rested" (lag) |
| Metric timestamp | matches the day Wiggers describes (e.g. C4 primary is same-day decay; C4 t+1 secondary is next-day reactivity) | uses an averaged-over-window metric when Wiggers describes a same-day state |
| Test family | non-parametric (Mann-Whitney / Wilcoxon) | linear regression with normality assumption violated by crash-day skew |
| Multiple-metric expansion | when Wiggers cites multiple temporal signatures (e.g. C4 = decay + walls + t+1), test all three as a confirmatory triad | testing only the primary and ignoring source-named secondaries |

**Chained-regime adjustment**:

- Within-event metrics are minimally affected by chaining — the metric at `t0` describes that day independently.
- One sensitivity row: report the test result restricting to non-chained `t0` days vs all `t0` days. If the effect inflates dramatically on the non-chained subset (small n!) flag it as exploratory.
- For C4 walls test specifically: if a crash episode spans days T and T+1, only T contributes a "walls" observation (the T+1 walls observation is an intra-episode continuation, not an independent event).

**Worked example**: A4 sustained HR + C4 three-channel triad (see § Worked-example anchors).

### Class 3: Dose-response ordinal (DR)

**When it applies**: Wiggers claims that higher *dose* of one metric produces higher (or lower) *response* in another. The claim is monotonic but not necessarily linear; ordinal stratification respects this.

**Hypotheses in this class**: A1 (RHR scales with exertion dose), E1 (personal step threshold), D5 conditional (P(crash | high morning BB ∧ overexertion)), parts of B4, parts of H2.

**Canonical statistical method**:

1. Define the dose variable. Default: `exertion_rank_composite_lagged_lcera` (continuous 0-1) stratified into quartiles, OR `exertion_class_lagged_lcera` directly if the categorical ladder fits.
2. Define the response variable (RHR deviation, gevoelscore, crash probability).
3. **Primary test**: Jonckheere-Terpstra for ordered alternatives. Tests `H_0: F_1 = F_2 = … = F_k` against `H_1: F_1 ≤ F_2 ≤ … ≤ F_k` (monotonic ordered).
4. Report median response per dose stratum + Hodges-Lehmann shifts between adjacent strata.
5. Effect size: τ (Kendall) for the dose-response slope as a robust monotonic association measure.
6. **Walk-forward gate**: ordering must replicate in the validate era (any reversal between adjacent strata in the validate era flags brittleness).

**Faithfulness rubric**:

| element | faithful when | drifted when |
|---|---|---|
| Dose stratification | uses ordinal levels Wiggers herself names (e.g. A1 "5-10 bpm" / "100 vs 60" ladder); for unspecified ladders use quartile cuts on a lagged exertion column | uses two-sample test ("heavy vs not") when the source claim is graded |
| Direction | tested against the ordered alternative (Jonckheere-Terpstra) | tested against the omnibus alternative (Kruskal-Wallis) — that's a different claim |
| Lag | uses the exertion column at the lag the source claims (Wiggers' RHR claim is "just before you rested" = same-day; E1 is t-2/t-3) | uses same-day exertion when Wiggers specifies a lag |
| Linearity | NOT assumed; the test rejects linearity is a feature when Wiggers' ladder is convex | testing with Pearson r alone (forces linear interpretation) |

**Chained-regime adjustment**:

- Dose-response is minimally affected by chaining at the per-day-vs-dose level — each day still has a valid dose value regardless of its chain context.
- Exception: when the *response* is a crash-incidence measure (E1, D5), chaining inflates the response distribution because chain-internal days have higher base-rate crash probability. Mitigation: report two versions — all `t0` days, and only "first-day-of-episode" days (n ≤ 29). The latter is the chain-deflated estimate.

**Worked example**: A1 Jonckheere-Terpstra dose-response (see § Worked-example anchors).

### Class 4: Non-linearity (NL)

**When it applies**: Wiggers claims that the effect of metric X on metric Y is *not linear* — typically convex (small changes at high X cost more than at low X) or piecewise (a breakpoint above which effects shift).

**Hypotheses in this class**: C3 (stress→fatigue convex), parts of D1-D2 (level vs dynamics), E1 (step breakpoint can also be modelled here).

**Canonical statistical method**:

1. Define predictor and outcome on the same-day or specified-lag basis.
2. Fit a natural cubic spline regression with 3-5 interior knots placed at predictor quantiles (4 knots default, ensures degrees-of-freedom budget for the autocorrelated sample).
3. Report the **marginal effect plot**: dY/dX as a function of X, with 95% CI from the spline coefficient covariance.
4. **Primary test**: likelihood-ratio test comparing the spline fit against a linear-only fit. Rejection of the linear null = non-linearity confirmed.
5. Secondary: binned mean comparison at Wiggers-named bin edges (e.g. C3 at 0-20/20-30/30-40/40-60/60+) with bootstrap CIs per bin.
6. **Walk-forward gate**: the spline fit on the train era must approximate the spline fit on the validate era (visually, in marginal-effect plots; quantitatively, via knot-coefficient overlap).

**Faithfulness rubric**:

| element | faithful when | drifted when |
|---|---|---|
| Functional form | spline (data-driven shape) with marginal-effect plot | pre-specifying a quadratic or power function unless Wiggers names that shape |
| Linearity rejection test | likelihood ratio vs linear-only model | reporting just the spline coefficients without the linear comparison |
| Bin edges | Wiggers-anchored where named (C3: 30/40 edge is explicit); otherwise data-quantile | arbitrary equal-width bins when the source uses convex-step framing |
| Marginal-effect interpretation | reported per X-range with CIs | aggregated single-number "non-linear by p<0.05" without showing the shape |

**Chained-regime adjustment**:

- Non-linearity tests use all days regardless of chain status — the same X→Y shape applies whether t0 is chain-internal or not.
- Sensitivity row: re-fit the spline with chain-internal days dropped, compare the marginal-effect plot shape. If the shape changes substantially, the non-linearity is driven by chain-clustering rather than the dose-response itself.

**Worked example**: C3 stress→fatigue spline (see § Worked-example anchors).

---

## The structural rule: HRV-proxy substitution

This rule is **orthogonal to the four classes** — it modifies how each class applies when the Wiggers claim references HRV directly.

### When it applies

Any Wiggers claim that references HRV in the literal sense (B1-B5; HRV-dependent parts of H1, H2, H3, H4, H5). Per the descriptive characterisation in [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) § 7.1-7.3 and the audit verdict in [`garmin_indicators_audit.md`](garmin_indicators_audit.md) § HRV, the FR245 / Elevate V3 sensor does not produce HRV Status directly, but `stress_mean_sleep` is a candidate HRV-proxy channel on descriptive grounds (episode-level crash signal Cohen's d = +0.90; r = +0.342 with `resting_hr`, R² = 0.117 → substantial non-HR variance).

### The substitution

Use `stress_mean_sleep` (sleep-window mean of Garmin's Firstbeat stress score) as the candidate HRV-proxy channel wherever Wiggers references HRV directly. The same operationalization-class machinery applies, with the metric substituted. **Channel selection (single vs multi)** is a per-hypothesis pre-reg choice, not a methodology constant — descriptive evidence supports both as legitimate framings, and the held-out validation that resolves the question is properly run inside a pre-reg.

**Examples**:

- Wiggers B1 ("≥10 HRV-point drop predicts PEM") → CCF lead-lag on `stress_mean_sleep(t)` deviation vs `is_crash(t+1)`, with the threshold calibrated from descriptive characterisation (not Wiggers' "10 points" anchor — that's in HRV units, not stress units).
- Wiggers H4 ("HRV spike + RHR drop = parasympathetic swing") → composite WE test on `bb_sleep_end_value` high + `bb_drained_24h` high (BB-anchored framing). The BB pattern is **source-grounded**: Wiggers' parasympathetic swing chapter (PDF lines 1431-1457) directly cites the BB-drop signature, independent of any HRV+RHR claim. `stress_mean_sleep` enters as secondary HRV-proxy channel; `resting_hr` is exploratory.

### Five pre-reg-file constraints inherited

Every B-block + HRV-dependent H pre-reg file MUST include these constraints, mirroring the version at [`../wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) § Pre-reg-file constraints for partial-via-proxy:

1. **Explicit proxy framing**: each pre-reg states "this test is on the `stress_mean_sleep` proxy, not on HRV proper."
2. **Descriptive effect-size anchor**: effect-size thresholds anchor on the descriptive Cohen's d = +0.90 (episode-level same-day reference from Check 7.3), not on RMSSD-anchored literature.
3. **Validation framework**: per [`train_validate_split_fate.md`](train_validate_split_fate.md), the descriptive characterisation is in-sample within Stratum 4. New B-block and HRV-dependent H pre-regs use full Stratum 4 as a single pool for primary inference. The historical 2023-12-31 split is NOT used as primary for new pre-regs; it remains as a reproducibility artefact for HA01b / HA02c. An optional M3 descriptive overlay (train-era vs validate-era) may be reported but cannot be used to claim a per-portion verdict, and any divergence is framed as a number, not a narrative (see Cross-cutting statistical hygiene §2).
4. **Channel selection is a per-hypothesis pre-reg choice**: descriptive r = +0.342 between `stress_mean_sleep` and `resting_hr` shows the channels are distinct enough (R² = 0.117 → ~88% of sleep-stress variance is non-HR) that single-vs-multi-channel framing is a legitimate per-pre-reg decision. Do NOT lock framing globally in this methodology doc.
5. **No literal HRV claim**: pre-reg conclusions defend the proxy-tested claim ("sleep-stress elevates around crashes"), not Wiggers' verbatim claim ("HRV drops before PEM"). Specific Wiggers UI anchors (e.g. "≥10 HRV-point drop") do not translate to stress units; calibrate the proxy threshold from descriptive characterisation.

### Effect-size interpretation

Per [`hrv_proxy_via_stress.md` § 4](hrv_proxy_via_stress.md), the descriptive proxy strength on this corpus:

- Episode-level Cohen's d = +0.90 (CI95 [+1.51, +8.22]) — same-day crash characterisation.
- Day-level Cohen's d = +1.03 (autocorrelation-inflated; episode-level is the cleaner anchor).
- Pearson r = +0.342 with `resting_hr`; R² = 0.117 → ~88% of `stress_mean_sleep` variance is not HR-driven (Check 7.2).

Pre-reg primary tests should be **directional**, not classifier-like. The descriptive characterisation supports "does the proxy detect the direction Wiggers claims?" not "can we predict next-day crashes from this proxy?" — the latter is a held-out classifier question that belongs in a pre-reg, not in this methodology doc.

---

## Cross-cutting statistical hygiene

The following apply to **every** class and every pre-reg, not just the HRV-proxy ones. Items 1-4 are binding methodology decisions documented in dedicated MDs; later items are inherited from prior memory + descriptive analyses.

1. **Stratification — primary analytic surface.** All Wiggers pre-regs run on **Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 → as-of-date)** per [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md). Other data-given strata (pre-corona, corona-infection, LC-pre-gevoelscore) are not analytic surfaces for these pre-regs because the required signal coexistence (gevoelscore + Garmin + notes + crash labels) does not hold there. Sub-segmentation inside Stratum 4 is introduced only under M1 (hypothesis-driven), M2 (methodological / confounder), or M3 (descriptive sensitivity overlay) per that MD, with the warrant stated in the pre-reg file before any test runs. Every pre-reg names its **as-of-date** for the right-edge of Stratum 4; new data accruing after lock does not trigger re-runs unless explicitly queued.

2. **Validation framework — single pool primary.** Per [`train_validate_split_fate.md`](train_validate_split_fate.md): new Wiggers pre-regs use the full Stratum 4 as a single pool for primary inference. The historical 2023-12-31 split is preserved as a reproducibility artefact only (HA01b, HA02c kept; columns `is_train_era` / `is_validate_era` kept in the master). Pre-regs may report train-era vs validate-era discrimination as an optional M3 descriptive overlay, but cannot claim per-portion verdicts, cannot apply per-portion α thresholds, and **must frame any divergence as a number, not a narrative** — divergence is a robustness-of-primary check, not evidence for any specific generative story. Effect-strengthening-over-time (the deleted trajectory story), stabilisation, label-precision drift, behavioural adaptation, measurement drift, season / life-event imbalance, and sampling variation at n=14 vs n=15 are all plausible drivers that a single-subject observational design cannot adjudicate. The overlay answers "is the primary single-pool verdict robust to era partition?" — it does NOT answer "does the effect change over time?".

3. **Multiple-comparisons correction.** With 23 testable + 11 partial = 34 hypotheses but only ~3-4 effectively independent channels per [cross-channel-correlation.md](../analyses/garmin_exploration/cards/cross-channel-correlation.md), the effective N for family-wise α control is **N_eff ≈ 4** (not 7 and not 34). **Primary correction**: Holm step-down on N_eff. Holm gives a free power uplift over Bonferroni-on-N_eff on the second and subsequent ordered p-values (closed-form, deterministic, decoupled from block-length policy, uniformly more powerful than Bonferroni under any dependence structure). For the smallest p-value, Holm and Bonferroni-on-N_eff are identical. **Queued descriptive overlay**: Westfall-Young step-down on the same primitives, reported as descriptive context (uses the joint permutation distribution to absorb correlation structure directly). WY is NOT used to relax the primary verdict threshold; it is reported side-by-side as a descriptive bound on "how much less conservative the correlation-aware test would be". The N_eff estimate itself comes from cross-channel-correlation analysis on Stratum 4 data; bootstrapping a CI on N_eff is a queued sensitivity check.

4. **Autocorrelation — two resampling layers.** Block-length policy and event-level permutation are distinct objects with different validity arguments and different n-driven caveats:
   - **Day-resampling layer** (within the construction window of each event, e.g. the 7-day pre-crash window): stationary bootstrap with E[L] = 7 days per [`permutation_null_block_length.md`](permutation_null_block_length.md); data-driven companion estimator for confirmation; pre-registered override rule for metric-specific ACF deviation.
   - **Event-level permutation layer** (crash / null label assignment at n=29): the resolution of the null distribution is dominated by combinatorics (C(29, k) is the binding constraint, not block length). Block-length policy applies to the day-resampling layer that lives inside each event's window; it does NOT apply to the event-level permutation itself.
   - **Finite-sample coverage caveat**: bootstrap consistency is asymptotic. At n=29 episodes, 95% CI nominal coverage may be materially below 95% in practice. A calibration simulation on synthetic data with known truth (queued) would let us put an honest number on actual coverage at our n. Until then, CI widths are reported as-computed with the asymptotic caveat made explicit in result files.

5. **Regression to the mean (RTM) around crashes.** Any peri-event window will manufacture "recovery" effects from RTM alone. Mitigation: compare the peri-event shape against a permutation null where `t0` is randomly relabelled; the Wiggers-claimed shape must exceed the RTM null.

6. **Crash-distortion sensitivity row.** Per [[feedback_crash_distortion_sensitivity]]: any correlation result must include a sensitivity row showing the result with crash days excluded. Effect inflation > 0.4 on the dropped subset = flag as crash-dominated.

7. **Acute-illness vs PEM separation.** Per H3 and [[project_lc_era_boundaries]]: acute-illness-onset days (from `triage_events.csv` `categorie=ziek` tags) have a different Garmin signature than PEM sags. Pre-regs that include both must stratify or run separately.

8. **Device-baseline lag.** First ~21 days of `has_garmin_uds=True` coverage are suspect (watch needs ~3 weeks to learn baseline per Wiggers PDF lines 99-106). Drop or down-weight in primary tests; sensitivity row including them.

9. **z-scores vs personal rolling baseline** per [[feedback_relative_not_absolute]]. Default rolling window is 28 days unless the hypothesis specifies otherwise.

10. **Lagged exertion columns** per [[feedback_use_lagged_exertion_for_pem]]. Use v3.2 `*_lagged_lcera` for PEM analyses. v3.1 unlagged columns stay for HA01b/HA02c reproducibility only.

---

## Hypothesis → class assignment

The complete map. Status legend mirrors [`../wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md): ✅ testable, ⚠️ partial, ❌ blocked.

### A. Resting HR & night HR

| ID | Class | Notes |
|---|---|---|
| A1 ✅ | DR (primary) + CCF (secondary exploratory) | source-verified, see Worked example |
| A2 ✅ | DR (signed via `\|RHR − baseline\|` ordinal stratification) | bidirectional claim — abs-deviation as predictor |
| A3 ✅ | CCF | lead-lag from `t-2`, direction confirmation via peak-ρ |
| A4 ✅ | WE | source-verified, see Worked example |

### B. HRV — all via single-channel `stress_mean_sleep` proxy

| ID | Class | Notes |
|---|---|---|
| B1 ⚠️ | CCF | spike detection in `stress_mean_sleep` proxy → crash at `t+1`; threshold calibrated from descriptive run |
| B2 ⚠️ | CCF | rolling 7d trend slope across peri-event window; directional only |
| B3 ⚠️ | CCF | rolling 28d baseline trajectory vs rolling 28d crash rate |
| B4 ⚠️ | DR (outlier framing) | conditional contingency: negative-outlier sleep-stress ∧ prior overexertion → crash at `t+1`/`t+2` |
| B5 ⚠️ | WE | conditional on illness-onset labels (separate from PEM crashes per H3) |

### C. Stress score

| ID | Class | Notes |
|---|---|---|
| C1 ✅ | CCF + WE secondary | `stress_mean_sleep` as proxy for "night orange"; peri-event from `t-1` |
| C2 ✅ | CCF (two-stage) | stress(t) → BB gain(t→t+1) → gevoelscore(t+1) |
| C3 ✅ | NL | source-verified, see Worked example |
| C4 ✅ | WE (3-channel triad) | source-verified, see Worked example |

### D. Body Battery

| ID | Class | Notes |
|---|---|---|
| D1 ✅ | NL (level effects) | Wiggers expects WEAK same-day r; the non-linearity claim is "level alone is a weak signal" |
| D2 ✅ | WE (dynamics > level) | side-by-side regression of gevoelscore on level cols vs dynamics cols; effect-size comparison |
| D3 ✅ | CCF | rolling 28d BB-floor vs rolling 28d crash rate |
| D4 ✅ | CCF | BB drain slope across `t-3 … t0` leads gevoelscore |
| D5 ⚠️ | DR (conditional contingency) | P(crash \| high morning BB ∧ overexertion); 33.8% fill constrains sample |

### E. Steps / activity load

| ID | Class | Notes |
|---|---|---|
| E1 ⚠️ | DR + NL (breakpoint) | dose-response with explicit breakpoint detection; respect t-2/t-3 lag |
| E2 ✅ | CCF | rising rolling steps + non-rising rolling crash rate = "genuine improvement" |
| E3 ✅ | WE | side-by-side effect sizes / AUC across the 4 axes |

### F. Sleep

| ID | Class | Notes |
|---|---|---|
| F1 ✅ | WE | sleep duration deviation on PEM nights |
| F2 ✅ | NL (bidirectional) | both directions of deep-sleep deviation predict gevoelscore drop |
| F3 ❌ | — | blocked: skipped per user (sleep score not in sleepData.json) |
| F4 ✅ | WE | bedtime SD predicts next-day gevoelscore |

### G. Other sensors

| ID | Class | Notes |
|---|---|---|
| G1 ✅ | WE | respiration on crash days (sleep variant) + waking variant |
| G2 ❌ | — | blocked: skin temperature sensor absent on FR245 |
| G3 ⚠️ | WE (external) | barometric pressure × gevoelscore; depends on external KNMI join |
| G4 ✅ | WE | SpO2 on crash days; deprioritised per Wiggers (instrument unreliable) |

### H. Mechanism & lead/lag

| ID | Class | Notes |
|---|---|---|
| H1 ⚠️ | CCF (proxy-substituted) | source-verified, see Worked example |
| H2 ⚠️ | WE (composite) | "activity-invisible" defined as joint criterion: low steps ∧ low max_hr ∧ no sustained_elevated_flag ∧ stress_mean_sleep outlier |
| H3 ⚠️ | WE (classifier) | logistic / RF on pre-day signatures, illness vs PEM; reduced separability without HRV+temp |
| H4 ⚠️ | WE (BB-anchored composite) | reclassified BLOCKED → PARTIAL 2026-06-13 on combined source + descriptive grounds. BB-anchored framing is source-grounded (parasympathetic swing chapter, PDF lines 1431-1457 cite the BB-drop pattern directly); `stress_mean_sleep` enters as secondary proxy; `resting_hr` exploratory. Channel selection is a per-pre-reg choice |
| H5 ⚠️ | CCF (ordering test) | source-verified, see Worked example |

### I. Methodology checks (cross-cutting)

| ID | Class | Notes |
|---|---|---|
| I1 ✅ | sensitivity row | re-run primary tests excluding first 21 days of Garmin coverage |
| I2 — N/A | — | no device change in this dump |
| I3 ✅ | already documented | column coverage in DATA_DICTIONARY |

**Summary**: 23 testable + 11 partial + 2 blocked (matching the register's summary table). Class breakdown:

| class | testable count | partial count |
|---|---|---|
| CCF | 6 ✅ | 6 ⚠️ |
| WE | 9 ✅ | 4 ⚠️ |
| DR | 2 ✅ | 2 ⚠️ |
| NL | 4 ✅ | 1 ⚠️ |
| sensitivity / cross-cutting | 2 ✅ | 0 |
| **total** | **23** | **13** (some hypotheses sit in two classes) |

---

## Worked-example anchors

The six source-verified hypotheses. Each anchor shows: source paraphrase → operationalization → statistical method → faithfulness verdict. Cross-references the verification log for the verbatim Wiggers quotes.

### A1 — DR class

**Wiggers paraphrase** (verification log entry A1): RHR deviation elevates during crash episodes; magnitude scales with exertion dose. Source: PDF lines 165-177 + 308-315.

**Operationalization**:
- Predictor: `exertion_rank_composite_lagged_lcera` (continuous 0-1), stratified into quartiles.
- Outcome: `resting_hr` deviation from rolling 28d median.
- Lag: predictor at `t-1` (Wiggers' "just before you rested" framing).
- Day-restriction: long-covid era only (`lc_phase == "lc"`).

**Statistical method**: Jonckheere-Terpstra ordered test on RHR-deviation distribution stratified by exertion quartile. Primary test at `t0`; exploratory secondary on peri-event `t-3 … t+3` cells.

**Pre-reg specifics to be added per-hypothesis**:
- Sample size: n = 1188 LC-era days (per DATA_DICTIONARY).
- Alpha: 0.05 Bonferroni-corrected against the 4 primary tests across A-block.
- Walk-forward: train 2022-09-03 → 2023-12-31, validate 2024-01-01 → today; quartile ordering must replicate at α=0.10 on validate.
- Sensitivity rows: crash-day drop per [[feedback_crash_distortion_sensitivity]]; isolated-crash-only subset (n ≤ 5) flagged as exploratory.

**Faithfulness verdict (from verification log)**: KEPT the dose-scaling and direction sub-claims; DROPPED the "just before crash days" precursor framing (that was OUR extrapolation, not Wiggers; belongs with B4/D5/H4 instead).

### A4 — WE class

**Wiggers paraphrase**: Sustained multi-hour RHR elevation, not a brief spike, marks real overexertion. Source: PDF lines 168-172, 243-247, 250-256, 257-261 + Flack at 527-554.

**Operationalization**:
- Day-classification: `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on `t-1`.
- Primary outcome: `hr_sustained_elevated_flag_lcera` (bool, longest run ≥ 30 min above `hr_daytime_baseline_lagged_lcera + 20 bpm`).
- Continuous outcome: `hr_longest_elevated_run_min_waking_lcera` (minutes).
- Transparency columns: `hr_median_waking`, `hr_daytime_baseline_lagged_lcera`.

**Statistical method**: Mann-Whitney on `hr_longest_elevated_run_min_waking_lcera` distribution, heavy-prior-day vs non-heavy-prior-day. Cliff's delta as ordinal effect size. Cross-tab on the flag for the binary version.

**Pre-reg specifics**:
- Threshold attribution: +20 bpm offset is Flack-via-Wiggers (PDF lines 527-554), NOT pure convention. Document this in the methods section.
- Sensitivity ladder (per verification log): duration {30, 60, 120 min} × offset {+10, +20, +30 bpm}. If the primary fires only at +20/30 min but not at surrounding cells, the result is brittle.
- Smoothing caveat: Garmin per-minute HR is 2-min averaged at source (PDF lines 257-261). The "30 min sustained" framing = "30 min of sustained-after-Garmin-smoothing".

**Faithfulness verdict**: KEPT the multi-hour-vs-brief-spike distinction (exact match). +20 bpm threshold is Flack-via-Wiggers sourced; 30 min duration is operational convention (Wiggers uses "hours" framing).

### C3 — NL class

**Wiggers paraphrase**: The stress→fatigue relationship is non-linear/convex; a day with stress=40 is much more tiring than stress=30. Source: PDF lines 1357-1368.

**Operationalization**:
- Predictor: `all_day_stress_avg` (TOTAL aggregator, 0-100).
- Outcome: `gevoelscore` (1-10).
- Bin edges: 0-20, 20-30, 30-40, 40-60, 60+ (anchored on Wiggers' 30/40 example).
- Day-restriction: long-covid era.

**Statistical method**:
- Primary: natural cubic spline regression `gevoelscore = f(all_day_stress_avg)` with 4 interior knots at quantile cuts.
- Likelihood-ratio test vs linear-only fit (rejection = non-linearity confirmed).
- Secondary: binned mean comparison at Wiggers-anchored bin edges with bootstrap CIs per bin.
- Marginal-effect plot: dY/dX as function of X with 95% CI.

**Pre-reg specifics**:
- Walk-forward gate: spline fit on train must approximate spline fit on validate (visual + knot-coefficient overlap).
- Sensitivity row: chain-internal day drop; if spline shape changes substantially, flag the non-linearity as chain-driven.

**Faithfulness verdict**: VERBATIM MATCH. The "30 → 40 step costs more than it looks" framing is taken directly from Wiggers' Annual Stress Scores section. The bin edges are partly Wiggers-anchored (30/40 edge is explicit) and partly OUR choice (other edges).

### C4 — WE class (3-channel confirmatory triad)

**Wiggers paraphrase**: After overexertion, stress fails to drop during rest periods. The claim has three temporal scales: same-day decay failure, walls-of-orange sustained-high, and next-day stress-spike reactivity. Source: PDF lines 1112-1119, 1140-1143, 1223-1231, 1306-1314.

**Operationalization** (three-channel triad):
- Day-classification: `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T.
- **Channel 1 (decay, primary)**: `stress_post_peak_time_to_rest_min` on T. NaN value = "did not return to rest that day" = C4-positive case. Also `stress_post_peak_drop_avg`.
- **Channel 2 (walls, secondary)**: `stress_high_duration_min` on T (Wiggers' "complete walls of orange" framing).
- **Channel 3 (t+1 reactivity, secondary)**: `awake_stress_avg` on T+1.

**Statistical method**: Mann-Whitney per channel, heavy-T vs non-heavy-T. Cliff's delta per channel. Triad rule per verification log: pass-2-of-3 channels = C4 confirmed; pass-1-of-3 = partial; pass-0-of-3 = rejected.

**Pre-reg specifics**:
- Walk-forward gate per channel; the triad rule applies independently in train and validate.
- Sensitivity: chain-T+1 days (where T+1 is itself a crash day) handled per § Class 2 chained-regime adjustment.

**Faithfulness verdict**: KEPT primary decay metric. EXPANDED to add walls + t+1 reactivity per source — the original single-metric operationalization missed two source-named channels.

### H1 — CCF class (with HRV-proxy substitution)

**Wiggers paraphrase**: HRV (specifically) leads the gevoelscore crash by "that night or next." Wiggers' explicit predictive claim is HRV-specific. Source: PDF lines 916-934, 956-964, 1014-1018, 1448-1457.

**Operationalization** (proxy-substituted):
- **Wiggers-faithful proxy channel**: `stress_mean_sleep` deviation vs personal rolling baseline (HRV-proxy on descriptive grounds per [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md)).
- **Wiggers-extension channels**: `bb_overnight_gain`, `resting_hr` deviation.
- Outcome: `gevoelscore` (the "felt" crash).
- Channel selection (single vs multi) is a per-pre-reg choice; descriptive r = +0.342 between `stress_mean_sleep` and `resting_hr` shows the channels are distinct enough that the framing question is legitimate per-hypothesis.

**Statistical method**: cross-correlation lag profiles per channel on first-differenced series, lags -10 … +10 days. Peak-ρ per channel + bootstrap CI. Direction confirmation: peak-ρ at strictly negative lag = channel leads gevoelscore.

**Pre-reg specifics**:
- Effect-size anchor: descriptive episode-level Cohen's d = +0.90 (same-day reference); lead-lag effect-size will be smaller.
- Walk-forward discipline: descriptive characterisation is in-sample; held-out validation on the 2024-01-01+ era required before publishing a directional claim.
- Mental PEM concession (PDF lines 1448-1457) supports H2 (activity-invisible crashes) as Wiggers' own H1 limitation — cite this in H2's pre-reg, NOT as an objection to H1.
- Non-HRV channel framing: testing whether `bb_overnight_gain` / `resting_hr` lead gevoelscore is OUR derivation, not a literal Wiggers prediction. Pre-reg frames it as an extension of the Wiggers framework, not a literal claim.

**Faithfulness verdict (from verification log)**: PARTIAL. Wiggers' predictive claim is HRV-specific. The proxy makes the literal HRV-leading test approximately testable; non-HRV channels are our extension. Also: Wiggers' own multi-day HRV lag (lines 925-928) means "exertion → HRV (slow) → gevoelscore (slower)" is the implied chain, not "HRV detected something pre-exertion".

### H5 — CCF class (ordering test)

**Wiggers paraphrase**: Each metric has a characteristic lag vs exertion; lags differ by metric. Implicit ordering: BB/stress (same/next day) ≤ RHR (hours-to-day) < HRV (multi-day cumulative). Source: PDF lines 168-172, 925-928, 1141-1143, 1433-1438.

**Operationalization**:
- Predictor: `exertion_rank_composite_lagged_lcera` (continuous, first-differenced).
- Channels: `bb_overnight_gain`, `stress_mean_sleep` (HRV-proxy), `resting_hr`, `gevoelscore` — all first-differenced.

**Statistical method**:
- Per-channel CCF on lags -10 … +10 days; `argmax-ρ` per channel.
- Bootstrap CI on `argmax-ρ` per channel (block bootstrap, block length 7 days).
- **Ordering test** (the new addition per verification log): test the prediction `argmax-CCF-lag(bb_overnight_gain) ≤ argmax-CCF-lag(stress_mean_sleep) ≤ argmax-CCF-lag(resting_hr)`. If confirmed at the ordering level, Wiggers' pattern is reproduced even if absolute lag values differ from her implicit values.

**Pre-reg specifics**:
- Mental-vs-physical PEM stratification (per verification log + PDF lines 1448-1457): if `cog_load` from `per_day_intensity.csv` triage is available, stratify physical-load vs cognitive-load PEM events as a sub-test. Wiggers' multi-day HRV lag may apply to physical PEM but not cognitive PEM (where she says "that night or the following night").
- Walk-forward: the ordering must replicate in the validate era (any ordering reversal = brittleness flag).

**Faithfulness verdict**: FAITHFUL. The implicit Wiggers ordering is reproduced. Enrichment: pre-reg-able as an ordering confirmation check, stronger test than "each metric has some lag".

---

## What pre-regs add beyond this doc

This methodology doc fixes the test design at the **operationalization → statistical method** level. Each per-hypothesis pre-reg file in [`../analyses/hypotheses/`](../analyses/hypotheses/) is responsible for the next level of specificity:

| concern | level set in this doc | level set in pre-reg |
|---|---|---|
| Operationalization class | yes | confirmed |
| Statistical method (test family) | yes | confirmed; test parameters tuned to hypothesis |
| Predictor / outcome columns | hint via assignment table | locked per hypothesis |
| Day-restriction (lc era, etc.) | yes (default lc) | confirmed; any deviation justified |
| Sample size + power | no | yes — power analysis on the n=29 episode count or n=1188 day count |
| Alpha level | hint (Bonferroni-corrected for primaries) | locked per hypothesis with correction family declared |
| Validation framework | single-pool primary on Stratum 4 per [`train_validate_split_fate.md`](train_validate_split_fate.md) | confirmed; optional M3 overlay if warranted, per-pre-reg M1/M2/M3 sub-segmentation if warranted |
| Train/validate split (legacy) | preserved for HA01b/HA02c reproducibility; not primary for new pre-regs | n/a for new pre-regs; legacy verdicts unchanged |
| Block-length policy | stationary bootstrap E[L]=7 days per [`permutation_null_block_length.md`](permutation_null_block_length.md) | confirmed; per-hypothesis override only via pre-registered rule |
| Multiplicity correction | Holm step-down on N_eff ≈ 4 (free uplift over Bonferroni-on-N_eff) | confirmed; WY queued as descriptive overlay |
| Primary vs secondary metrics | hint for verified hypotheses | locked per hypothesis |
| Walk-forward replication threshold | hint (α=0.10 typical) | locked per hypothesis |
| Sensitivity rows | yes (crash-drop, isolated-only, chain-internal-drop) | confirmed + any hypothesis-specific additions |
| Stop / continue rule | no | locked per hypothesis |
| Result narrative template | no | yes — the result.md template per hypothesis folder |

---

## Open methodological questions

These are real questions that affect how future pre-regs are written but are not gating the immediate work:

1. **Validation framework for the HRV proxy.** Per [`train_validate_split_fate.md`](train_validate_split_fate.md), the held-out-validation question is resolved at the framework level: new B-block pre-regs use full Stratum 4 as a single pool. The HRV-proxy descriptive characterisation in [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) § 7.1-7.3 was in-sample (Cohen's d = +0.90 on crash episodes; r = +0.342 vs `resting_hr`), and the single-pool framework is the standard within-subject validation pattern for this regime. The first B-block pre-reg author still commits to a channel-selection choice (single vs multi) per constraint #4 of § The structural rule, and may report a train-vs-validate descriptive M3 overlay (number, not narrative). See [`queued_work.md`](queued_work.md) Q7 (HeartMath-paired validation) for the orthogonal external-calibration approach.

2. **Autonomic fragmentation (`stress_stdev_sleep`) under non-additive operationalizations.** Per [`queued_work.md`](queued_work.md) Q8: the narrow joint-logistic test answered NO (incremental AUC ≈ 0 over `stress_mean_sleep`). Still open: lag profile, peri-event time-course, within-night structure, non-linear forms. If a Wiggers-related autonomic-fragmentation claim becomes pre-reg-relevant, the broader operationalisations need to be tested. Currently not pre-reg-relevant.

3. **Cross-source label visual reproduction.** Per [`queued_work.md`](queued_work.md) Q9: reproducing Wiggers' "No-PEM vs with-PEM" same-person plots on this corpus would be cross-source label validation (Wiggers' Garmin-pattern labels vs our self-report `crash_v2` labels). Descriptive-layer task. Not gated by this doc but would strengthen every downstream pre-reg by showing the labels track real physiological events.

4. **Parasympathetic-swing labels do not exist.** H4 reclassification to PARTIAL leans on the BB-anchored signature as primary (source-grounded: Wiggers' parasympathetic swing chapter, PDF lines 1431-1457, cites the BB-drop pattern directly). The RHR-side of Wiggers' literal "high HRV + very low HR" diagnostic pattern (PDF lines 1027-1037) is testable only with HRV. Resolving the literal-Wiggers H4 requires either (a) a manual labelling pass of candidate parasympathetic-swing nights (HRV-proxy negative outlier → "good" felt day → crash day at t+1/t+2) or (b) a HRV-enabled device to test the literal HRV signature. Both deferred.

5. **Chained-regime adjustment per class is documented but not battle-tested.** Each class section above proposes specific chained-regime sensitivity rows; the first pre-reg that runs them will reveal whether the adjustments are sufficient or need refinement. Treat this as exploratory until at least two CCF tests + two WE tests have run with the sensitivity rows reported.

---

## Cross-references

- [`../wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) — the register that this doc operationalises; source verification log for verbatim Wiggers quotes per hypothesis.
- [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) — the proxy framing, empirical numbers, and decision options that this doc inherits.
- [`garmin_indicators_audit.md`](garmin_indicators_audit.md) § HRV — the audit-level verdict that authorises the partial unblock.
- [`../literature/wiggers_pacing_handleiding.pdf`](../literature/wiggers_pacing_handleiding.pdf) (local-only, gitignored) — the source document; PDF line refs in this doc map to the `pdftotext -layout` extraction.
- [`queued_work.md`](queued_work.md) — Q7 (HeartMath-paired validation), Q8 (autonomic-fragmentation broader), Q9 (cross-source visual reproduction); the methodological follow-ups this doc references.
- [`methodology.md`](methodology.md) — broader research methodology (PwC + gevoelscore + Garmin cross-validation lens).
- [`../analyses/hypotheses/crash_v2-definition/definition.md`](../analyses/hypotheses/crash_v2-definition/definition.md) — locked crash + dip definitions; the labels every pre-reg here uses.
- [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md) — Stratum 4 as primary analytic surface; data-given vs methodological sub-segmentation; M1/M2/M3 warrant for any sub-boundary.
- [`permutation_null_block_length.md`](permutation_null_block_length.md) — stationary bootstrap E[L]=7 day-resampling layer; pre-registered override rule; event-level-permutation layer distinct.
- [`train_validate_split_fate.md`](train_validate_split_fate.md) — single-pool primary; historical 2023-12-31 split as reproducibility artefact; optional M3 descriptive overlay; HA01b train-vs-validate divergence framing as number-not-narrative.
- [`_pending_literature_fetch.md`](_pending_literature_fetch.md) — queued literature acquisition for citations currently deferred in the three MDs above.
- [[feedback_relative_not_absolute]], [[feedback_use_lagged_exertion_for_pem]], [[feedback_crash_distortion_sensitivity]], [[feedback_no_interpretive_marks]], [[project_lc_era_boundaries]], [[feedback_methodology_decisions_documented_reasoning]], [[feedback_caveats_vs_apriori]] — user memory entries that constrain choices throughout this doc.
