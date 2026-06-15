# HA-P7 — Recent-crash-density predicts elevated crash risk (Personal-register, recovery-debt hypothesis)

## Authorship

**Drafted 2026-06-15** by Claude (Opus 4.6) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. Drafted in the same session that produced [HA-C4b's pre-reg](../HA-C4b/hypothesis.md); shared context includes Sessions C/D/E and the [citalopram_phase_stratification framework](../../../methodology/citalopram_phase_stratification.md). Pre-reg follows the [HA11 pre-reg pattern](../HA11-stress-udip/hypothesis.md) and the sibling [HA-C4b structure](../HA-C4b/hypothesis.md).

The drafting was performed under the operationalisation-precision walkthrough specified in the [P7 drafting handoff](C:/Users/Gebruiker/.claude/plans/session-p7-prereg-handoff-2026-06-15.md). Three load-bearing operationalisation choices were locked interactively before drafting:

1. **Eligibility + primary-outcome framing**: Option A from the interview. Eligibility is `is_crash at d-1 == False` (yesterday is a gap day); primary outcome is `is_crash at d` (today potentially crashes). Resolves the register-table inconsistency where "d not in episode" excluded the outcome `is_crash at d` by construction.
2. **Train/validate split + phase stratification**: HA11 family split (train 2022-09-03 → 2023-12-31; validate 2024-01-01 → 2026-06-05) + pooled LC era headline + phase-stratified sensitivity arms.
3. **Density encoding + null pre-spec**: Continuous logistic regression (OR + 95% CI) as primary statistical machinery + binned tabulation (`crash_count_14d ∈ {0, 1, 2, 3+}`) with Wilson CIs as descriptive companion + 3-criterion null pre-spec.

**Status**: drafted, not locked. Lock requires explicit user acceptance. After lock, [`/research-review`](../../../reviews/README.md) must run in a fresh session (no shared drafting-session context); the review report lands in [`reviews/`](../../../reviews/) with the addendum *"Fresh session — no exposure to the drafting context; doc-only knowledge."*

---

**Pre-registration written 2026-06-15, BEFORE any logistic-regression fit on the recent-crash-density predictor against `is_crash`.** Locked at user acceptance. Any subsequent change creates an HA-P7-v2.

HA-P7 tests the **recovery-debt prediction** from the participant's lived experience ([lived-experience braindump](../../../lived_experience_garmin_pacing_2026-06-14.md): *"crash risk is increased in a period with multiple crashes. Things we have to test empirically"*) — that the count of crash-days in the preceding 14-day window predicts elevated probability of a new crash today, on top of any baseline risk.

**HA-P7 is the project's first Personal-register inferential hypothesis test** (P1-P5b are autonomic-channel hypotheses; P6 is descriptive; P7 is the cheapest test in the queue using only crash labels). It is also the first project hypothesis where the **predictor and outcome both derive from the same instrument** (`gevoelscore` → `crash_v2` labels) — the §1.3 causal-ambiguity caveat is irreducible.

## 1. Claim

In both **train** (2022-09-03 → 2023-12-31) and **validate** (2024-01-01 → 2026-06-05) windows independently, on a day `d` in the LC era where `is_crash at d-1 == False` (gap day yesterday), the logistic odds ratio for `crash_count_14d = count(is_crash) over [d-14, d-1]` predicting `is_crash at d` satisfies: **OR > 1 with 95% CI excluding 1**, AND the binned per-day rate is monotonically non-decreasing across `crash_count_14d ∈ {0, 1, 2, 3+}`.

The directional claim is one-sided positive (more recent crash-days → higher next-day crash risk) per the lived-experience prior + the PEM recovery-debt mechanism.

A bidirectional sensitivity arm reports the |OR − 1| result for transparency. The primary direction is one-sided positive per §1's framing.

**Secondary descriptive outcomes**:
- **Window sensitivity ladder**: same test repeated with `crash_count_7d` and `crash_count_30d`. The 14d is the primary; 7d/30d are sensitivity arms. A directional finding that holds across all three window-arms is robust; one that fires only at 14d is window-fragile.
- **Citalopram phase-stratified sensitivity** (per the [phase_stratification §3 axis](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification)): same test repeated within each of the 4 LC-era phases (unmedicated / buildup / consolidation / afbouw + post-afbouw). The pooled-LC verdict is the headline; per-phase verdicts are descriptive. The phase stratification addresses P7 caveat 4 — `gevoelscore` (and hence `crash_v2` labels derived from it) is mildly dose-modulated per [intervention_effects §8](../../../methodology/intervention_effects_descriptive.md#8-findings-session-c-run-2026-06-14)'s small detrend-surviving step at 2026-03-20.
- **Same-day gevoelscore correlation**: Spearman correlation between `crash_count_14d` and `gevoelscore at d` on eligible (gap-day-d-1) days. Descriptive only; no SUPPORTED bar.

## 2. Why we think this

- **Lived experience prior**. From the [lived-experience braindump](../../../lived_experience_garmin_pacing_2026-06-14.md): *"some intuitive ideas are that crash risk is increased in a period with multiple crashes. Things we have to test empirically."* Explicit, user-stated, framed as needing empirical test. Per [CONVENTIONS §4.3](../../../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory), this counts as a lived-experience prior that supports confirmatory framing.
- **PEM recovery-debt mechanism**. The biological story: PEM (post-exertional malaise) recovery is multi-day; if recovery from a recent crash is incomplete, the participant enters subsequent days with reduced envelope and elevated vulnerability. Recent-crash burden accumulates as recovery debt that elevates next-crash probability.
- **Literature partial**. Wiggers does not specifically claim recent-crash-density elevates next-crash risk. Broader chronic-illness pacing literature on cumulative load + recovery debt (queued in [`_pending_literature_fetch.md`](../../../methodology/_pending_literature_fetch.md)) supports the directional intuition without operationalising it.
- **Sibling project context**. The project has documented a multi-channel autonomic-precursor signature on crashes (H02b spike count, HA06b RHR z-score, HA10 morning BB peak, HA11 within-day U-dip events). HA-P7 tests a different *type* of precursor: **a labels-based behavioural-history pattern, not an autonomic state**. If supported, it complements the autonomic precursors with a context layer ("you're in a vulnerable period").
- **Cheapest end-to-end test in the queue**. No FIT extraction, no per-minute parsing, no methodology-MD blockers. Closes the shortest path between "no verdict" and "verdict landed".

## 3. Data sources

- **Crash labels**: `crash_v2` from [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv), surfaced as the `is_crash` boolean column in `per_day_master.csv`.
- **Phase membership**: `dose_plasma_mg` column in `per_day_master.csv` (PK-smoothed per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification)); phase derivable from the date via the `citalopram_phase(d)` function in that MD §3.
- **gevoelscore for secondary correlation**: `gevoelscore` column in `per_day_master.csv`.
- **Analysis window + train/validate split**: same as HA11 / HA06b / HA10 / HA-C4b (train 2022-09-03 → 2023-12-31, validate 2024-01-01 → 2026-06-05). Total eligible (gap-day-d-1) days estimated at ~700-1000 LC-era pooled; per-phase n estimates given in §4.4.

**No FIT extraction required.** All inputs are existing per-day columns in the consolidated master.

## 4. Measurement protocol

### 4.1 Predictor — `crash_count_W` (locked)

For each LC-era day `d` (`date >= 2022-04-04`), and for each window length `W ∈ {7, 14, 30}`:

```
crash_count_W(d) = sum(is_crash[d - W : d - 1])
                 = number of crash-days in the W-day window before d
```

- Window is exclusive of `d` (we are predicting `d`'s outcome from prior days only).
- Window is **inclusive on both ends of `[d - W, d - 1]`** — so for `W = 14`, the window is `d-14, d-13, …, d-1` (14 days).
- Each crash-day counts as 1 toward the density. A 5-day crash episode contributes 5 to the count; a 1-day crash contributes 1. This is the register's chosen weighting — dense periods are weighted by duration, not by event count.
- **Primary window**: `W = 14`. Mechanistically anchored to typical PEM-recovery tail per the register's directional claim. **Sensitivity windows**: `W = 7` and `W = 30`, reported alongside but not driving the headline.

### 4.2 Eligibility rule (locked, Option A from interview)

A day `d` is **eligible for HA-P7** if **all** of:

1. `d` is in the LC era (`d >= 2022-04-04`).
2. **`is_crash at d - 1 == False`** — yesterday is a gap day (NOT inside a crash episode). This is the load-bearing eligibility rule per the Option A locking. The rule does NOT exclude days where `d` itself is a crash-start (Option A explicitly allows `d` to be a new-crash-start, which is the primary outcome).
3. `d` has a valid `is_crash` label (i.e. is inside the `crash_v2` coverage window — not censored).
4. The 14-day primary window `[d - 14, d - 1]` is fully within the `crash_v2` coverage window. (Sensitivity windows have their own coverage requirements — see §6 exclusion rules.)

Days failing any of these are excluded from the test sample. Report fractions per cause.

**Eligibility rule's implications**:
- `d` itself MAY be `is_crash == True` (i.e. a new crash starts at `d`). This is the primary outcome event.
- `d` MAY be in the *middle* of an extended episode iff yesterday `d-1` was somehow a gap day — by definition this cannot happen for `crash_v2` episodes (which require ≥ 2 consecutive low-gevoelscore days). So in practice, eligible days where `is_crash at d == True` are crash-start days.

### 4.3 Outcome — `is_crash at d` (primary; locked)

For each eligible day `d`:

- **Primary outcome**: `is_crash at d` (boolean). This is the "new crash starts at d" event under the §4.2 eligibility rule (since yesterday was a gap day).
- **Secondary outcome**: `any_crash_in_next_3d(d) = any(is_crash[d : d + 3])` — covers d, d+1, d+2, d+3 (4-day forward window). Broader; captures "is the immediate forward window dangerous". Reported as descriptive companion; the SUPPORTED bar is on the primary.

### 4.4 Phase-stratified sensitivity arms (per phase_strat §3)

In addition to the **pooled LC-era headline** (the verdict-driving test), report the same test repeated within each of the 4 Citalopram-traject phases:

| phase | window | n eligible (estimated) | n-headline-quality |
|---|---|---|---|
| unmedicated | LC start 2022-04-04 → 2024-04-08 | ~500-650 | full power |
| buildup | 2024-04-09 → 2024-06-19 (with 2024-04 cluster buffer per §6) | ~20-40 | likely inconclusive (low power) |
| consolidation (30mg plateau) | 2024-06-20 → 2026-03-19 | ~550-700 | full power |
| afbouw + post-afbouw | 2026-03-20 → 2026-06-05 | ~50-70 | borderline |

Per-phase n's are estimates; actual counts gate at the §10.1 dry-run.

**The headline verdict is the pooled LC-era result.** Per-phase verdicts are descriptive — phase-specific n's are smaller than HA11 family per-test conventions; INCONCLUSIVE is expected for buildup and possibly afbouw. The phase-stratified read addresses P7 caveat 4 (`gevoelscore` is mildly dose-modulated; crash rates may shift across phases) — if the pooled LC-era result is dominated by a single phase or contradicts other phases, that's a methodological flag.

**No §5.B dose-adjustment is applied to the predictor**. The predictor is a count of crash-days, not a Garmin channel value; the §5.B covariate-adjustment framework operates at the per-mg-plasma level on continuous channels. Phase-stratification is the appropriate handling.

### 4.5 Statistical machinery (locked: continuous logistic + binned tabulation + 3-criterion null)

#### 4.5.1 Primary: continuous logistic regression

For each window `W ∈ {7, 14, 30}` and each phase + the pooled LC era:

```
logit(P(is_crash at d == 1)) = β_0 + β_1 * crash_count_W(d)
```

- Fit on all eligible days (§4.2).
- Report `OR = exp(β_1)`, 95% Wald CI on OR, p-value (one-sided positive).
- **Headline verdict comes from the W=14 pooled LC-era logistic**.

#### 4.5.2 Companion descriptive: binned tabulation

For the primary window `W = 14` (and reported descriptively for 7d / 30d):

| crash_count_W bin | n eligible days | n with is_crash at d == True | rate | Wilson 95% CI |
|---|---|---|---|---|
| 0 | ... | ... | ... | ... |
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |
| 3+ | ... | ... | ... | ... |

- Wilson CIs because the rates are likely small and bins may be small.
- The bin rates should be **monotonically non-decreasing** across bins 0 → 1 → 2 → 3+ (within a 5 percentage-point tolerance) if the recovery-debt mechanism is real.

#### 4.5.3 Null sample (for the discrimination check)

Logistic regression already provides an internal null comparison (the H0: β_1 = 0). No external null sample is needed for the primary headline.

For the binned tabulation's discrimination check, the *implicit* null is the bin-0 cell rate (i.e. the baseline crash rate on eligible gap-day-d-1 days with no recent crashes in the window). Higher-bin rates are compared against bin-0 rate, not against a randomly-drawn null sample.

### 4.6 Phase-stratified per-phase tests

Repeat §4.5.1 + §4.5.2 within each phase, with eligibility restricted to dates within the phase boundary + the §6 exclusion buffer for the 2024-04 boundary cluster. Per-phase n's may be insufficient for a full bar — surface as INCONCLUSIVE where so.

## 5. Pre-registered falsification criterion (3-criterion null pre-spec)

Locked from the user-confirmed `## Authorship` decision-3. The hypothesis is **NOT-SUPPORTED in the pooled LC-era headline** if **ALL of (a), (b), (c)** hold:

**(a) Continuous logistic OR CI fails to discriminate**: in the pooled LC-era `W=14` logistic regression, the 95% Wald CI on OR contains 1.

**(b) Binned monotonicity violated**: in the pooled LC-era `W=14` binned tabulation, the per-bin rate is NOT monotonically non-decreasing across {0, 1, 2, 3+} within a 5-percentage-point tolerance. Specifically: for any consecutive pair of bins (`i, i+1`), `rate(i+1) < rate(i) - 0.05` constitutes monotonicity-violation.

**(c) Window-sensitivity disagrees**: AT LEAST 2 of the 3 window arms (7d / 14d / 30d) have ORs with 95% CI containing 1.

If ALL of (a) + (b) + (c) hold → **NOT-SUPPORTED at the pooled LC-era headline**.

If only (a) but not (b) or (c) → **inconclusive on the magnitude** but the directional signal is present in companion arms; report as INCONCLUSIVE.

If (a) does not hold (OR CI excludes 1) AND (b) holds (monotonicity holds) AND fewer than 2 windows disagree → **SUPPORTED at the pooled LC-era headline**.

**Inconclusive bars**:
- If pooled LC-era eligible n is fewer than 200 → **inconclusive** (low power; expected n is ~700-1000, so this would indicate a coverage-issue).
- If any single bin (0, 1, 2, 3+) has fewer than 5 days in the pooled LC-era → that bin is reported descriptively but excluded from the monotonicity check (criterion b).

**Bidirectional sensitivity arm**: report the same test with the OR direction flipped (negative-only). If the data show recent-crash-density REDUCES next-crash risk (counter-prior direction), document honestly; do NOT redefine the headline verdict on the bidirectional arm.

## 6. Exclusion rules

- Days outside the LC era (`d < 2022-04-04`) are excluded.
- Days where `is_crash at d - 1 == True` are excluded from the test sample (§4.2 eligibility).
- Days where the W-day window `[d - W, d - 1]` is not fully within the `crash_v2` coverage window are excluded for that W. (Different W's may exclude different days at the LC-onset edge.)
- Days where the `is_crash at d` label is missing are excluded.
- **Buildup-phase days before 2024-04-30 (first 22 days of buildup) are excluded** (CPAP-end confound buffer per [intervention_effects §8.1](../../../methodology/intervention_effects_descriptive.md#81-effective-analyzable-scope-5-of-8-boundaries-usable)). The exclusion applies in the phase-stratified sensitivity arms; the pooled LC-era headline INCLUDES these days but flags them.
- **2024-04-09 to 2024-04-16 (boundary cluster)** is excluded from BOTH the pooled headline AND the phase-stratified arms (structurally unanalyzable per same reference).

## 7. Expected effect size if hypothesis is true

- **OR per crash-day in W=14 window**: 1.15-1.40 per additional crash-day in the window. A density of 3+ crash-days yields ~1.5-3× elevated risk relative to 0-density baseline.
- **Bin-0 baseline rate** (eligible days with no recent crashes in W=14): ~2-5% per day (LC-era pooled crash rate ÷ episode-length-adjustment).
- **Bin-3+ elevated rate**: ~5-15% per day.
- **Sanity check on bin distribution**: bin-0 should dominate (most eligible days have 0 recent crashes), and the distribution should taper. If bin-3+ has more than 20% of eligible days, the eligibility rule may be admitting more dense-period days than expected → flag for review.
- **Sanity check on logistic convergence**: if any window's logistic regression fails to converge (e.g. complete separation in a bin) → flag for review; the bin-0/bin-3+ rates may need a Bayesian prior or a Firth correction.

If either sanity check fails on the dry-run, the spec needs review BEFORE running the full test. The §10.1 dry-run is the gate.

## 8. Caveats `result.md` must explicitly acknowledge

- **Causal-attribution ambiguity is the central concern** (per P7 register caveat 1). A positive result is consistent with BOTH:
  - The "recovery-debt mechanism" (incomplete recovery → elevated vulnerability)
  - A "shared underlying cause" (a stressful period — heavy life events, infection, intervention transition — causes BOTH the recent crashes AND today's elevated risk)
  
  The design CANNOT adjudicate between these two stories. Result.md must surface this prominently; any causal claim about "recovery debt" beyond mere association is overclaiming. Future sensitivity covariates on documented life-events / interventions could partly mitigate but do not resolve.

- **Selection bias on conditioning**. Excluding within-episode days (via the §4.2 eligibility on `d-1` being a gap day) concentrates the analysis on inter-crash gap days. These days have systematically different distributional properties than pure baseline days (e.g. they may follow crash periods, so post-crash recovery dynamics are baked into the sample). The comparison is "gap-day-with-recent-crashes" vs "gap-day-without-recent-crashes", not "any-day" vs "any-day-with-recent-crashes".

- **Self-reported crash labels** via crash_v2. crash_v2's definition requires `gevoelscore ≤ 3 for ≥ 2 consecutive days`; any noise / inconsistency in the gevoelscore self-report propagates into the labels. Single-rater coding; no ground-truth physiological confirmation.

- **gevoelscore is mildly dose-modulated** per [intervention_effects §8](../../../methodology/intervention_effects_descriptive.md#8-findings-session-c-run-2026-06-14) (small detrend-surviving step at 2026-03-20). The crash-label threshold-crossing rate may shift across Citalopram phases. The phase-stratified sensitivity arm in §4.4 addresses this; the pooled headline does NOT apply a §5.B-style dose-adjustment because the predictor is a count, not a continuous value. If the per-phase OR is heterogeneous, the dose-modulation may be doing analytical work.

- **gevoelscore is the SAME instrument generating both predictor and outcome**. Both `crash_count_14d` and `is_crash at d` derive from the same per-day score. Any systematic instrument-level bias (e.g. drift, mood-state-dependent reporting) affects predictor and outcome together. This is a fundamental limitation of self-report-only designs and cannot be addressed within this test.

- **Protocol disturbs the test**. The participant operationally pacings based on recent-crash awareness. If the protocol successfully translates "I've had crashes recently → I'll act more protectively" into "no crash today", the test CONFLATES recent-crash-aware-and-acting-protectively (which prevents the crash) vs recent-crash-aware-but-pushing-through (which still has a crash). A NOT-SUPPORTED finding may indicate the protocol IS protective and prevented the crashes that would have shown the recovery-debt signal — flag this as the protocol-protective alternative reading. A SUPPORTED finding means the recent-crash-density is predictive on top of any protective protocol effect, which is the harder claim to substantiate.

- **Window length is operationally locked, not data-derived**. The 14d primary is mechanistically anchored to typical PEM-recovery tail, not derived from this corpus's data. Sensitivity arms (7d, 30d) provide robustness; if the directional finding holds across all three, the window-choice fragility is bounded.

- **Multi-comparison**. HA-P7 is the second Personal-register pre-registered hypothesis after HA-C4b. The HA family has 15+ tests; the held-out validate window is the primary defence against multi-comparison inflation.

- **No Garmin channel covariates**. P7's predictor is labels-only. A future P7-variant could add Garmin-channel covariates (e.g. "crash density + average BB lowest over the same window") but is out of scope for v1. The labels-only test is the cheapest path to a verdict on the recovery-debt mechanism alone.

- **Per-phase ns are small for buildup + afbouw**. Per-phase headline verdicts are not the design's target; pooled-LC headline is the headline. Buildup and afbouw verdicts will likely be INCONCLUSIVE; report as such, do not retroactively narrow the phase boundaries to recover power.

## 9. What we do with each outcome

The outcome space is the pooled LC-era headline result, with per-phase + per-window companion verdicts.

- **Pooled LC-era SUPPORTED in both train AND validate windows** (criterion (a) excluded; OR > 1 with 95% CI excluding 1; criterion (b) monotonicity holds; criterion (c) fewer than 2 windows disagree) → **first Personal-register inferential SUPPORTED finding**. The recovery-debt prediction is empirically validated. **But the causal interpretation remains ambiguous** (§8 caveat 1); the result.md headline must lead with "consistent with recovery-debt OR shared-cause", not "recovery debt confirmed". 
  - **Downstream propagation**: the [garmin_pacing_practice.md](../../../methodology/garmin_pacing_practice.md) operational protocol gains an empirically-grounded "recent-crash burden" awareness layer; potentially a watch-face card concept showing rolling 14-day crash density.
  - **If phase-stratified arm shows asymmetry** (e.g. consolidation has tighter CI than unmedicated): document the asymmetry as evidence for the buildup-vs-afbouw asymmetry question being explored in [phase_stratification §8.4](../../../methodology/citalopram_phase_stratification.md#84-the-buildup-and-afbouw-magnitude-asymmetry-as-a-research-question).
  - **If the SUPPORTED result is window-fragile** (only 14d fires, 7d + 30d do not): the recovery-debt window-length is narrower than expected. Document; consider HA-P7b with a finer-grained window ladder ({7, 10, 14, 17, 21d}).

- **Pooled LC-era train SUPPORTED, validate NOT-SUPPORTED** → train-era pattern that does NOT replicate. Possible explanations to document:
  - The recently-evolved pacing protocol (most consistent in recent months per [garmin_pacing_practice §2 temporal qualifier](../../../methodology/garmin_pacing_practice.md#temporal-qualifier--this-protocol-is-a-recent-stabilisation-not-a-constant)) may have translated "recent-crash awareness" into protective action, reducing the validate-era's recovery-debt signal.
  - The Citalopram-traject dose-modulation may have stabilised the validate-era gevoelscore distribution, reducing the magnitude of the underlying recovery-debt signal.
  - Document both as candidate explanations; the result.md does NOT pick one.

- **Pooled LC-era train NOT-SUPPORTED, validate SUPPORTED** → second validate-era SUPPORTED Personal-register finding (after the eventual HA-C4b result if it falls that way). Notable because it would imply that recent-crash burden became a predictor only after some change. Investigate: protocol stabilisation? Citalopram phase transitions? Document as a hypothesis-generating finding for HA-P7c.

- **Pooled LC-era NOT-SUPPORTED in both windows** → recent-crash burden does NOT predict next-day crash risk at the population level. **Two readings**:
  - "**No recovery-debt mechanism on this corpus**" — the recovery-debt prediction is empirically refuted. Document; close the recovery-debt hypothesis on this corpus.
  - "**The pacing protocol is protective and prevents the crashes that would have demonstrated the recovery-debt signal**" — the protocol's lived practice has internalised the recent-crash awareness and the participant successfully acts protectively. The NOT-SUPPORTED finding is then evidence FOR the protocol's effectiveness, not against the recovery-debt mechanism.
  - The result.md must surface BOTH readings prominently; do NOT favor one without explicit user reflection.

- **Continuous OR significant but binned monotonicity violated** (criterion (a) excluded, criterion (b) holds) → the relationship is non-linear or non-monotonic at the bin level. Possible: very-high-density days (3+) saturate the protective response. Report descriptively; consider HA-P7b with a tighter bin ladder.

- **Window arms disagree** (criterion (a) excluded, criterion (c) holds — only 14d fires but 7d and 30d do not) → window-fragile finding. Possible: 7d is too short to capture full recovery-debt; 30d is too long and conflates with phase-of-life signals. Document; consider HA-P7b with a finer window ladder.

- **Per-phase verdicts contradict pooled-LC headline** → phase-specific effect that the pooling obscures. Document; potential follow-up: P7b with phase-stratified primary.

- **Spec sanity-check fails on dry-run** (per-phase n < 200 in pooled; bin-3+ > 20% of eligible days; logistic non-convergence) → DO NOT run the full test. Document the failure in the dry-run report; revise the spec (creating HA-P7-v2 with audit trail).

## 10. Detection script architecture

The extraction is trivial (labels-only). HA-P7's test script is the lightest in the project.

### 10.1 No Stage 1 — primitive already in `per_day_master.csv`

`is_crash` is already in `per_day_master.csv` via the existing `labels_crash_v2.csv` → `build_unified_dataset.py` flow. No new extraction required.

### 10.2 Stage 2 — test (`HA-P7/test.py`, to be written in next session after audit)

Loads `per_day_master.csv`, computes `crash_count_W` per eligible day for `W ∈ {7, 14, 30}`, applies §4.2 eligibility, derives `dose_plasma_mg` → phase membership, runs the §4.5 logistic regression + §4.6 binned tabulation per phase + pooled, evaluates §5 falsification criterion per train/validate × per phase × per window.

Same `--dry-run` mode as HA11 / HA-C4b: prints first-3-episodes (or first-3-crash-starts in the eligible sample) per phase × era to confirm spec sanity before the full evaluation runs.

### 10.3 Stage 3 — `result.md`

Headline verdict block at top (pooled LC-era, W=14, primary). Train/validate split table. Per-window sensitivity arm table. Per-phase sensitivity arm table. Binned tabulation with Wilson CIs. Same-day gevoelscore correlation (descriptive). Caveats per §8.

### 10.4 Run protocol

1. **Dry-run** (`python test.py --dry-run`): prints eligible n per phase × era; bin distribution; checks sanity per §7. **If sanity check fails → halt + revise spec → HA-P7-v2.**
2. **Full run** (`python test.py`): emits `result.md` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-P7-v2 with the v1 result archived (per the project's locked-pre-reg discipline).

Estimated test script length: ~200 lines (Python + statsmodels + scipy).

---

*Pre-registration drafted 2026-06-15 by Claude in reviewer-mode-with-authorization in the same session that drafted [HA-C4b/hypothesis.md](../HA-C4b/hypothesis.md). Lock requires user acceptance. Fresh-session `/research-review` audits after lock per CONVENTIONS §1.2.*
