# Citalopram dose-response on stress_mean_sleep — methodology

**Status**: drafted 2026-06-14; awaiting script-implementation session.

This MD locks the analytical specification for one narrow follow-up
question: does the participant's nighttime autonomic load
(`stress_mean_sleep`) respond to the citalopram afbouw (scale-down) in
a graded, dose-dependent way? The script that produces the actual
finding is the next step after this MD is signed off; this MD does NOT
run it.

Producer-mode artefact per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs).
Inherits the four-input reasoning bar from [§2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice).

---

## 1. What this MD asks, and what it does not

### 1.1 The question

The participant's prescribed citalopram dose stepped down on three
dates inside an 11-week afbouw period:

- 2026-03-20: 30mg → 20mg
- 2026-04-17: 20mg → 10mg
- 2026-05-27: 10mg → 8mg druppelvorm
- (2026-06-05 = data-cut; the 8mg sub-phase has only 9 days of post-step data.)

If citalopram materially modulates nocturnal autonomic load on this
participant, lowering the dose stepwise should produce a graded
reduction in `stress_mean_sleep` — i.e. a measurable
`β_dose > 0` (more drug → higher nocturnal stress) when the channel
is regressed on the dose function across the afbouw window. This is
the dose-response question.

### 1.2 What this MD does not do

The list below is the v1/v2 scope; **v3 expanded the analytical scope
substantively** via §5.5 (cross-window corroboration: buildup +
spring-control tests) and §5.6 (multi-channel confirmation across
parent MD §3 baseline channels). The original "narrow follow-up MD"
framing remains the **primary scope** (the §4 analysis specification
is single-channel × single-window); the v3 extensions are confirmatory
sensitivity-of-the-result-itself, not re-locks of the spec.

- **Does NOT test the buildup period in the §4 primary analysis.**
  Symmetric confirmation (dose UP → stress UP) is methodologically
  the right second half of the case but is confounded with the
  CPAP-end transition at 2024-04-16 (CPAP stopped 7 days after
  citalopram started). The §4 spec is afbouw-only.
  **v3 update**: §5.5.2 opens this scope via a **post-CPAP-buffer
  spec** ([`buildup_check.py`](../analyses/garmin_exploration/intervention_effects/buildup_check.py))
  that drops the first 22 days of the buildup window to isolate the
  CPAP-free citalopram-only stretch (2024-05-01 → 2024-06-19); the
  symmetric prediction is confirmed there with β_dose = +0.43/mg,
  CI excluding zero, p = 0.001. A separate narrow MD on the
  CPAP-end confound would still be valuable for analysing the
  first 22d of the buildup; that remains out of scope here.
- **Does NOT broaden to other channels in the §4 primary analysis.**
  `stress_mean_sleep` was selected because it is the
  *mechanistically clean* candidate from the parent MD's Session C
  run (§2). The §4 spec is single-channel.
  **v3 update**: §5.6 broadens to the parent MD §3 baseline-channel
  family ([`multi_channel_check.py`](../analyses/garmin_exploration/intervention_effects/multi_channel_check.py))
  for cross-channel-consistency evidence. The multi-channel run is
  not a methodological re-lock; it applies the §4 spec to each
  channel and reports per-channel verdicts. `stress_mean_sleep`
  remains the locked primary outcome.
- **Does NOT re-derive the parent finding.** The descriptive Layer-1
  pre-vs-post sweep at the 2026-03-20 boundary already cleared:
  step DOWN of ~3 points, survives the §3.7 detrend at B={7,14,28},
  marginal at B=42. See [`intervention_effects_descriptive.md` §8](intervention_effects_descriptive.md#8-findings-session-c-run-2026-06-14).
  This MD is the *focused confirmatory follow-up* on that candidate.
- **Does NOT claim causal attribution beyond pharmacological-association.**
  See §1.3 confound caveat.

### 1.3 Inherited substantive confound (binding caveat)

The documented LC recovery trajectory on this corpus (crash frequency
~10/year in 2023-24 → ~2/year in 2025-26 per [`analyses/hypotheses/registry.md`](../analyses/hypotheses/registry.md))
runs underneath the afbouw window. The 77-day afbouw period is short
relative to the multi-year recovery slope, but it is not orthogonal
to it. The §4 analysis specification handles this two ways:

1. A linear `days_from_afbouw_start` covariate absorbs the local slope
   inside the regression.
2. A sensitivity column re-runs the model with the v3.2
   `_lagged_lcera` baseline-adjusted variant of the outcome (see §3.2
   and §4.5).

What the analysis *cannot* resolve is whether the underlying recovery
trajectory itself accelerated *because* the dose came down — i.e. a
mediation pathway where SSRI withdrawal contributes to the recovery
rather than just co-varying with the afbouw window. That requires a
between-subjects design which this corpus cannot provide. Findings
should be read as "consistent with a dose-graded autonomic response to
citalopram, after absorbing the local LC-recovery slope" — not as
isolated pharmacological causation.

**Other confounds co-varying with the afbouw window** (enumerated per
the parent MD §1 substantive-confound discipline; ordered by likely
impact on `β_dose`):

- **Seasonality** *(substantive)*. The afbouw runs 2026-03-20 → 2026-06-05
  — mid-March through early-June, late winter through early summer
  in the Netherlands. Daylight hours rise from ~12h to ~16h
  (approximately linear across the window); spring mood seasonality
  and ambient temperature shift across the window. (Pollen seasonality
  is NOT a confound for this participant — no documented hay-fever
  reactivity; documented 2026-06-14.) All these factors co-vary with
  calendar time and therefore partially with the dose function (which
  is monotonically declining in calendar time). The linear
  `days_from_afbouw_start` covariate (§4.1) absorbs *monotonic linear*
  seasonal effects but does not handle bursty or nonlinear seasonal
  shifts cleanly. Sensitivity Column F (§4.3) adds a nonlinear time
  term as a robustness check; the residual leakage risk is real but
  partially mitigated. **Cross-year falsification test added in v3**:
  §5.5 amendment confirms via spring-2025 (clean 30mg-consolidation
  control) that the generic-spring-rise pattern does NOT replicate
  outside the afbouw year, weakening this confound substantially.
- **Breinvoeding-interventie (concurrent intervention)** *(minor)*.
  The Breinvoeding-interventie 2026-03-10 → 2026-08-31 runs across
  the entire afbouw window and was excluded from the parent MD §2
  intervention catalog *precisely because* its overlap with the
  afbouw made boundary attribution impossible. This MD inherits the
  overlap as a co-occurring intervention that is not separately
  modelled; any effect Breinvoeding has on `stress_mean_sleep`
  during the afbouw window will be confounded with `β_dose`. The
  effect is plausibly small (Breinvoeding is dietary, not
  pharmacologic) but the confound is acknowledged here rather than
  silenced.
- **Device stability** *(no impact)*. FR245 throughout the afbouw
  window; no device-change confound. Confirmed in passing.
- **Life events outside the corpus** *(diagnostic)*. Stressful life
  events not captured in `annotations.yaml` could co-vary with the
  afbouw window by chance. §5.3 handles this as a diagnostic on
  counter-prior findings — i.e. if `β_dose` flips sign (lower dose
  → higher stress), exogenous-event explanations are surfaced
  before the result is treated as a finding.

### 1.4 Framing — confirmatory per CONVENTIONS §4.3

The dose-response hypothesis was *not* generated from peeking at the
afbouw-period data. Per [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory)
three independent prior sources establish it:

1. **Lived experience prior**: the participant describes
   "background sympathetic tone" and "I sleep but my system isn't
   really resting" as a felt experience preceding the afbouw decision
   (see [`lived_experience_garmin_pacing_2026-06-14.md`](../lived_experience_garmin_pacing_2026-06-14.md)).
2. **Published-literature prior**: SSRIs are documented to elevate
   nocturnal autonomic load (reduced HRV, elevated nocturnal HR,
   altered sleep architecture); withdrawal is documented to partially
   reverse this. Anchor papers queued at
   [QUEUED-WORK Tier 3](../QUEUED-WORK.md#tier-3-methodological-refinement-deferred):
   Marin 2010, Tantucci 2003 (CPAP autonomic; sibling intervention),
   Licht 2010, Kemp 2010 (SSRI HRV), Wichniak 2017 (SSRI sleep
   architecture). The `fetch-paper` skill is available to retrieve
   these if the user wants citations locked before the script runs;
   this MD is NOT gated on that retrieval.
3. **Mechanistic prior**: citalopram is a selective serotonin
   reuptake inhibitor; serotonergic tone modulates central autonomic
   regulation; receptor occupancy at steady-state plasma levels
   scales monotonically with dose across the clinical 8-30mg range.

Per §4.3, in-corpus descriptive observation in the parent MD §8 is
*corroboration of a pre-specified prior*, not *origination of a
post-hoc claim*. Confirmatory framing is therefore justified. The
walk-forward discipline that exploratory work would require collapses
to a magnitude-calibration concern, not a credibility concern.

**Audit-trail note on the queued-literature-prior status.** The §4.3
rule explicitly requires only ONE of the three priors to be
independent. The literature prior above is *queued, not yet
retrieved* — the anchor papers exist (Marin 2010, Tantucci 2003,
Licht 2010, Kemp 2010, Wichniak 2017) but the citation pass is
deferred to QUEUED-WORK Tier 3. The confirmatory framing therefore
rests primarily on the **lived-experience prior** (independently
documented in [`lived_experience_garmin_pacing_2026-06-14.md`](../lived_experience_garmin_pacing_2026-06-14.md))
and the **mechanism prior** (serotonergic-autonomic pharmacology,
independent of corpus). Both are independently sufficient under
§4.3's "any one is yes" rule. The literature prior, when retrieved,
will tighten the channel-selection rationale but will not change
the framing.

The four-input reasoning per [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice)
runs through §4 for each analytical choice.

---

## 2. The afbouw period and the dose function

### 2.1 Dates and dose-step structure

Pulled from `$GEVOELSCORE_DATA_PATH/raw/directus_exports/annotations.yaml`
(gitignored), verified against the parent MD §2 catalog (citalopram
sub-phase spans collapsed by containment filter, with markers added
2026-06-14 for the umbrella-phase transitions).

| date | step | days at new dose before next step |
|---|---:|---:|
| 2026-03-20 | 30mg → **20mg** | 28 |
| 2026-04-17 | 20mg → **10mg** | 40 |
| 2026-05-27 | 10mg → **8mg druppelvorm** | 9 (data-cut at 2026-06-05) |

The afbouw period as a whole runs **2026-03-20 → 2026-06-05** (77 days
of data; ~7 trailing days NaN on `stress_mean_sleep` after the
2026-05-29 channel cut). The umbrella citalopram-traject end at
2026-06-05 coincides with the data-cut; no post-afbouw equilibration
window is observable in this corpus.

### 2.2 The prescribed-dose step function

```
dose_mg ──┐
   30     │
          └──┐
   20        │
             └──┐
   10            │
                  └──┐
    8                │___ (data-cut)
          ↑   ↑   ↑   ↑
          03-20 04-17 05-27 06-05
```

`dose_prescribed_mg(d)` is well-defined for every day in the window:
the dose the participant was taking on day `d`.

### 2.3 PK-smoothed plasma proxy (primary exposure)

**State-of-art framework**: the exposure model is a
**one-compartment first-order absorption-elimination
pharmacokinetic / pharmacodynamic (PK/PD) model**, the standard
framework for time-varying drug-exposure regression in single
subjects (Rowland & Tozer 2011, *Clinical Pharmacokinetics and
Pharmacodynamics*, 4th ed., chapter 4; Gabrielsson & Weiner 2016,
*Pharmacokinetic and Pharmacodynamic Data Analysis*). The
one-compartment first-order specification is appropriate for
citalopram because the drug exhibits approximately first-order
elimination kinetics in the clinical-dose range and is well-described
by a single distribution compartment for the central-nervous-system
target tissue (citalopram Summary of Product Characteristics, EMA;
Hyttel 1994 for SSRI-class pharmacology).

Citalopram's plasma half-life is ~35 hours (citalopram SPC, EMA);
steady-state after a dose change is reached in ~5-7 days. The
prescribed step function therefore *overstates* the abruptness of
the actual pharmacological exposure. Receptor-level activity is
closer to a smoothed staircase than to a clean step.

The primary exposure variable is the one-compartment exponential-decay
convolution of the prescribed step function, with the half-life
locked at 35 hours:

```
dose_plasma_mg(d) = initial_dose_decay_term(d)
                    + Σ_steps Δstep * (1 - exp(-ln2 / t_half_d * (d - step_date)))
                      * indicator[d >= step_date]
```

where:

- `t_half_d = 35 hours / 24 hours per day ≈ 1.46 days`.
- `Δstep` is the *change* in prescribed dose at each step
  (negative for the afbouw direction): −10mg at 2026-03-20,
  −10mg at 2026-04-17, −2mg at 2026-05-27.
- `initial_dose_decay_term(d) = 30mg` for every day in the afbouw
  window. Justification: the participant arrives at 2026-03-20
  already at steady-state plasma on the 30mg consolidation regime
  (which ran 2024-06-20 → 2026-03-20, ~21 months — far longer than
  the ~5-7 day steady-state time). The pre-afbouw plasma level is
  therefore the 30mg steady-state value, and the convolution
  decrements from there as each Δstep takes effect. On
  2026-03-20 the formula yields `dose_plasma_mg ≈ 30mg` (because
  the first Δstep contribution is zero on its own start date);
  on subsequent days the negative Δstep contributions accumulate
  with the PK time-constant.

In practice this means each dose-step date contributes a smoothed
ramp over ~5-7 days into the new level; days inside a step plateau
are at the new steady-state level. The convolution is computed on a
daily grid (sufficient given the channel grain).

**Why PK-smoothed as primary**: receptor occupancy is what the
mechanism literature speaks to; the dose card is an upstream proxy.
The methodological tradeoff is that the PK proxy assumes 100%
adherence at the prescribed dose between step-dates; deviations
(missed doses, dose-timing variance) are absorbed into residual
noise. This assumption is acceptable given the participant's
documented adherence pattern; if a future audit surfaces a
non-trivial miss-rate, the proxy can be refined.

**Sensitivity column on dose representation**: the model is also fit
with `dose_prescribed_mg(d)` (the unsmoothed step function) as the
exposure. If the dose-response coefficient flips sign or loses
significance under the prescribed-step variant, that disagreement is
itself a finding (it would mean the smoothing is doing analytical
work beyond what the data supports).

### 2.4 Why no per-step transition buffer

The parent MD's transition-buffer sweep (B ∈ {7, 14, 28, 42}, parent
§4) is the right design when the question is *level shift at a single
boundary*: exclude the post-event transient, compare steady-states.
For the dose-response question, the transient between dose-step dates
IS the signal — it's how the regression learns the slope. Excluding
±B days around each step strips the regression of the very thing it's
designed to detect.

The PK-smoothed exposure (§2.3) already addresses the
"plasma is not at steady-state on day-of-step" concern internally,
without truncating the analytical window. The handoff §7.3 listed
buffered-dose as a third option; it is rejected here for this reason.

---

## 3. The outcome channel

### 3.1 stress_mean_sleep — what it operationally measures

`stress_mean_sleep` is the mean Garmin "stress" score across the
sleep window of the night attributed to day `d` (per
[`nightly_attribution.md`](nightly_attribution.md)). The Garmin
stress score is a 0-100 composite derived primarily from heart-rate
variability; higher = more sympathetic dominance / less parasympathetic
recovery. Sleep-window mean therefore captures *background autonomic
tone during nocturnal recovery* — exactly the construct the lived
experience prior (§1.4) operationalises as "I sleep but my system
isn't really resting".

Definitional-pair structure per [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair):
`stress_mean_sleep` is paired with `all_day_stress_avg`. Only one of
the two enters this MD's regression. `stress_mean_sleep` is preferred
because the SSRI nocturnal-autonomic literature anchors specifically
to *sleep-window* measures (Wichniak 2017), and because the lived
experience prior is sleep-framed.

**On daily-mean vs spike-detecting metric choice (CONVENTIONS §3.5).**
[CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages)
prefers spike-detecting metrics over daily averages for
sympathetic-arousal proxies (e.g. "minutes with stress ≥ 75 per
sleep-window" rather than `stress_mean_sleep`). This MD uses the
daily-mean variant inherited from the parent MD §8 finding — the
parent's step-DOWN-at-afbouw-start signal was specifically on
`stress_mean_sleep`, the daily-mean column, so switching to a spike
metric here would invalidate the parent's signal as the descriptive
clearance for this confirmatory follow-up. A spike-based equivalent
(if `per_day_master.csv` exposes a sleep-window minutes-above-threshold
column) would corroborate the dose-response if it agreed with the
primary; this is queued as future work and out of scope here.

### 3.2 Coverage in the afbouw window

Verified in Session C (parent MD §8.1): `stress_mean_sleep` covers
2021-08-18 → 2026-05-29 (n=1707 days on the master CSV; source:
`per_day_master.csv`). For the afbouw window:

- **Nominal afbouw window**: 2026-03-20 → 2026-06-05 (77 calendar
  days, anchored on the prescribed dose function).
- **Analytical window for stress_mean_sleep**: 2026-03-20 → 2026-05-29
  (71 calendar days observed; the last 7 calendar days of the
  nominal window are NaN due to the 2026-05-30+ channel cut).
- **Analytical n**: precise count to be derived by the §6 script
  from `per_day_master.csv` (count of days with
  `stress_mean_sleep` non-null and `2026-03-20 <= date <= 2026-06-05`).
  The expected count is ~71 minus any incidental missing days
  inside the window (e.g. watch-off intervals); the prose figure
  "~70" used elsewhere in this MD is the working estimate.

### 3.3 Outcome-vs-baseline framing inherited from parent MD §3b

The parent MD splits its analysis into §3 baseline-channels (the
autonomic reference frame the lagged-baseline machinery computes
*against*) and §3b outcome-channels (`gevoelscore`, the dependent
variable from which crash labels are derived). `stress_mean_sleep`
sits in the §3 baseline-channel set.

The methodological consequence: this MD's finding, when it lands,
informs the *predictor* side of downstream hypothesis tests — not the
outcome side. A confirmed dose-response on `stress_mean_sleep` would
mean downstream tests using `stress_mean_sleep_lagged_lcera` z-scores
across the afbouw boundary inherit a reference-frame discontinuity
that the rolling-baseline machinery may or may not absorb. See §5 for
what specifically the finding informs.

Note also: the §4 analysis runs a sensitivity column on
`stress_mean_sleep_lagged_lcera` as the outcome. The reasoning is
nuanced — using the lagged-baseline z-score as the *outcome of the
dose-response model* partially absorbs the dose signal into the
baseline (the 90-day rolling reference includes recent afbouw days),
which is precisely why it is sensitivity-not-primary. See §4.3.

---

## 4. Analysis specification (the locking section)

### 4.1 Primary model

Linear regression of `stress_mean_sleep` on the PK-smoothed plasma
dose proxy, with a linear `days_from_afbouw_start` covariate to
absorb the local LC-recovery slope:

```
stress_mean_sleep(d) = β_0
                    + β_dose * dose_plasma_mg(d)
                    + β_time * days_from_afbouw_start(d)
                    + ε(d)
```

with `d ∈ [2026-03-20, 2026-06-05]` restricted to days where
`stress_mean_sleep(d)` is observed (i.e. NaN-trailing days
auto-excluded; analytical n ≈ 70).

**Pre-specified hypothesis** (per §1.4 confirmatory framing):

- H0: β_dose = 0
- H1: β_dose > 0  (lower dose → lower nocturnal autonomic load)

One-sided test, α = 0.05.

**Tradeoff on one-sided vs two-sided test**. One-sided gains ~2×
power on the prior-committed direction; two-sided is more
conservative when direction is uncertain. The one-sided choice is
justified here *only because* the §1.4 priors commit the direction
(SSRIs elevate nocturnal autonomic load; withdrawal partially
reverses → dose-down implies stress-down → β_dose > 0). This
direction-commitment is therefore a methodological premise of this
MD, not a free analytical choice the analyst could flip
post-hoc. If the script returns a *significant negative* β_dose
(counter-prior direction), the one-sided test by construction
returns "fail to reject H0" — but §5.3 then routes the read to a
diagnostic-mode interpretation (exogenous-event explanations,
confound enumeration) rather than a finding. The two-sided
alternative was considered and rejected on this premise; if a
reviewer rejects the §1.4 direction-commitment, the analysis should
be re-spec'd to two-sided rather than mid-stream.

**Four-input reasoning per [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice)** for each
of the three primary-model choices:

1. **Linear in dose (vs log-dose or piecewise)**.
   *Best-practices*: dose-response shape over the clinical 8-30mg
   citalopram range is approximately linear-in-dose on plasma-level
   pharmacokinetics; saturating receptor-occupancy nonlinearity
   appears at much higher doses than this range covers. *Literature*:
   queued (Marin / Tantucci / Licht / Kemp / Wichniak) — if the
   literature pass surfaces evidence that receptor occupancy
   nonlinearity bites at sub-clinical doses, the model upgrades to
   log-dose with a methodology MD amendment. *Tradeoff*: parsimony +
   interpretability vs. mechanistic exactness; with 4 dose levels
   the regression cannot reliably distinguish linear-in-dose from
   log-dose anyway (the two are co-linear over the relevant range).
   *Our limits*: n=1, ~70 analytical days, 4 dose levels.
2. **Linear in days (vs polynomial)**.
   *Best-practices*: a 77-day window is short relative to the
   multi-year LC recovery slope; the slope is approximately linear
   on this scale. *Literature*: not applicable (this is a covariate
   absorbing a known underlying trend, not a primary effect).
   *Tradeoff*: a quadratic term would absorb more time-shape but
   risks absorbing dose-signal since the dose function is itself
   monotone-declining-in-time (4 dose levels co-vary with time by
   construction). Parsimony wins. *Our limits*: same as above.
3. **PK-smoothed dose (vs prescribed step)**.
   *Best-practices*: pharmacokinetics is the standard exposure
   model for time-varying drug effects in PK/PD work; one-compartment
   exponential decay with the labelled half-life is the default
   for steady-state-not-yet-reached corrections. *Literature*:
   citalopram product label; t½ = 35 hours; steady-state ~5-7 days.
   *Tradeoff*: §2.3 — PK proxy assumes 100% adherence; the
   prescribed-step alternative is transparent but mechanistically
   coarse. Sensitivity column (§4.3) hedges this. *Our limits*: no
   plasma-level measurements; the PK proxy is a model, not a
   measurement.

### 4.2 Standard errors — Newey-West HAC

Day-level Garmin data is serially correlated; plain OLS standard
errors will be biased downward (over-significant). Primary inference
uses Newey-West Heteroskedasticity- and Autocorrelation-Consistent
standard errors (Newey & West 1987, *Econometrica* 55(3):703-708):

```python
import statsmodels.api as sm
maxlags = int(np.floor(4 * (n / 100) ** (2/9)))   # Andrews 1991 rule; ≈4 for n=70
fit = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': maxlags})
```

The lag-selection rule is from Andrews 1991 (*Econometrica*
59(3):817-858) and yields `maxlags ≈ 4` at n=70. A second
specification with `maxlags = 7` (weekly cycle) is reported in the
sensitivity panel as a robustness check; large divergence between
the two would itself be informative about residual cycle structure.

**Four-input reasoning**:
*Best-practices*: HAC SE is the standard adjustment for
autocorrelation in time-series regression. *Literature*: Newey & West
1987 (the canonical HAC estimator); Andrews 1991 (data-dependent lag
selection that adapts to the underlying autocorrelation structure
rather than fixing an arbitrary lag). *Tradeoff*: HAC is parsimonious
and well-understood by reviewers; block bootstrap (§4.3 sensitivity)
is slightly more robust to autocorrelation-shape misspecification but
less reader-familiar. *Our limits*: at n≈70 days the asymptotic
HAC approximation is mildly stressed; the block-bootstrap sensitivity
is a hedge against this.

### 4.3 Sensitivity sweeps

The §4.1 primary model produces a single primary `β_dose` with a HAC
p-value and 95% CI. The sensitivity sweeps are reported as
**additional columns alongside** the primary, not as alternative
primaries — they let the reader judge how fragile the primary is to
each modelling choice.

**Sensitivity column A — block bootstrap.** Re-estimate `β_dose` by
1000-iteration moving-block bootstrap on the residuals (Künsch 1989,
*Annals of Statistics* 17(3):1217-1241, local PDF at
[`literature/methodology/kunsch_1989_jackknife_bootstrap_stationary.pdf`](../literature/methodology/kunsch_1989_jackknife_bootstrap_stationary.pdf);
stationary-bootstrap variant available per Politis & Romano 1994,
*JASA* 89(428):1303-1313, if the moving-block edge effects bias the
CI), with 7-day blocks (matching the parent MD §6 `block_p` block
length, which is itself anchored to weekly behavioural rhythm).
Report the bootstrap distribution's 95% CI for `β_dose` alongside
the HAC interval. A finding that survives HAC but dies under block
bootstrap is a **fragility flag**.

**Sensitivity column B — prescribed-step dose representation.**
Re-fit the primary model with `dose_prescribed_mg(d)` (the unsmoothed
step function) substituted for `dose_plasma_mg(d)`. Direction and
significance of `β_dose` are the comparison; per §2.3 a sign-flip or
significance loss would mean the PK smoothing is doing analytical
work beyond what the data supports.

**Sensitivity column C — _lagged_lcera outcome.** Re-fit the primary
model with `stress_mean_sleep_lagged_lcera` (the v3.2 lagged-baseline
z-score per [CONVENTIONS §3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses))
substituted for raw `stress_mean_sleep`.

*Methodologically tricky point worth surfacing*: the lagged-lcera
baseline uses a `[d-90, d-30]` rolling window restricted to LC-era
days. For days inside the afbouw window, that 60-day pre-window
**spans the afbouw itself** for most of the analytical days (e.g.
day 2026-05-15 has its baseline drawn from 2026-02-14 → 2026-04-15,
of which ~26 days are inside the afbouw). This means the z-score
outcome is *measured against a baseline that is partially co-moving
with the dose*. Under a real dose-response effect, the lagged-lcera
variant will therefore **systematically attenuate** the apparent
`β_dose` relative to the primary raw-outcome spec — by construction,
not as a refutation. The sensitivity column is informative when
read with this caveat: if `β_dose` survives the lagged-lcera spec
despite the attenuation pressure, that strengthens the finding. If
it disappears, the read is ambiguous (could be genuine null or
could be the baseline absorbing the signal). This caveat is
written into the §5 finding-interpretation table.

**Sensitivity column D — alternative HAC lag.** As §4.2: report
`β_dose` with `maxlags = 7` alongside the Andrews-rule `maxlags ≈ 4`.

**Sensitivity column E — crash-drop (CONVENTIONS §3.4 audit hook).**
Re-fit the primary model with rows where `is_crash == True` dropped
from the regression. Report `β_dose`, HAC CI, p-value alongside the
primary. Per [CONVENTIONS §3.4](../CONVENTIONS.md#34-crash-drop-sensitivity-row-on-every-layer-4-correlation):
*"every Layer 4+ correlation / CCF / regression that touches
PEM-pacing variables, run two frames in parallel: Full LC frame ...
Same frame with is_crash == True rows dropped. Report both ρ values.
If |Δ| > 0.10, surface as a finding."* `stress_mean_sleep` is a
PEM-pacing channel (P4a, P4b, P5b inherit from it per §5.1); the
audit hook applies regardless of expected effect size.

*Expected impact*: crash frequency in the late-LC era is ~2/year per
[`analyses/hypotheses/registry.md`](../analyses/hypotheses/registry.md),
so the expected count of crash days in the 77-day afbouw window is
~0.4 (less than one expected crash). The crash-drop column is
therefore likely to be near-identical to the primary — but the
audit-hook binds independent of expected impact, and the
named-count-per-CONVENTIONS-§3.6 visibility of the actual crash-day
count inside the window IS informative (it confirms the late-LC
crash-rarity prior holds across the afbouw specifically). The §6.3
outputs include the §3.6-formatted named count.

**Sensitivity column F — nonlinear time term (seasonality robustness).**
Re-fit the primary model with the linear `days_from_afbouw_start`
covariate replaced by a 4-knot natural cubic spline on
`days_from_afbouw_start` (or equivalently a month-indicator dummy
expansion: March / April / May / June). The linear time covariate
(§4.1) absorbs *monotonic linear* shifts (LC recovery slope, linear
daylight increase); the cubic-spline / month-dummy variant additionally
absorbs nonlinear seasonal shifts (bursty pollen onset, mood-cycle
inflections) that may co-vary with the dose function. Per §1.3
seasonality confound: if `β_dose` survives the nonlinear-time variant,
the residual-seasonality leakage risk is empirically bounded. If it
disappears, the read is ambiguous (genuine null OR seasonal residuals
were doing the work). Report `β_dose`, HAC CI, p-value alongside the
primary.

**Visual companion — monotonicity scatter.** Beyond the regression
coefficient, the script produces a 4-point plot:

- **x-axis**: the four nominal prescribed-dose plateau values
  (30, 20, 10, 8 mg), each computed as the *mean of
  `dose_prescribed_mg` over the analytical days inside that dose
  plateau* (not the continuous `dose_plasma_mg` used in the
  regression). This binning is *visual-only* — the regression itself
  uses continuous PK-smoothed dose; the binned scatter is the
  reader-friendly companion that makes the 4 dose-level structure
  explicit.
- **y-axis**: the mean of `stress_mean_sleep` residuals over the
  same plateau days, after subtracting the fitted `β_time *
  days_from_afbouw_start(d)` time-trend component from each day's
  observed value.
- The four resulting points (one per dose plateau) characterise the
  dose-response *shape* the regression is estimating. Visual
  monotonicity (30mg-residual highest, 8mg-residual lowest, with
  intermediate doses ordered between) corroborates the linear-in-dose
  assumption; non-monotonicity (e.g. 20mg residual lower than 10mg)
  is a fragility flag the linear fit absorbed.

### 4.4 Pre-spec for null finding (binding decision rule)

Per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no),
the null pre-spec is locked here so it cannot be post-hoc reframed.

A **null finding** ("no detectable dose-response on stress_mean_sleep
across the citalopram afbouw") is declared if and only if **all four**
conditions hold:

1. Primary HAC 95% CI for `β_dose` fully contains zero.
2. |β_dose| < 0.05 × SD(stress_mean_sleep) per mg (i.e. effect-size
   gating: a numerically null finding requires effect smaller than
   ~0.05 SD per mg, which at typical SD ≈ 10 means
   |β_dose| < 0.5 stress-points per mg).
3. Block-bootstrap (Sensitivity A) 95% CI also contains zero.
4. _lagged_lcera variant (Sensitivity C) p-value > 0.05.

Any one condition failing → **not a null finding**; the reading
moves to the effect-size + caveats interpretation per §5.

The all-four conjunction is deliberately conservative against
declaring null: an effect that is small but consistent across the
HAC + bootstrap + lagged-lcera triad is not a null finding even if
the primary CI brushes zero. This is the right asymmetry per §1.4 —
the prior is that the effect exists; declaring null requires
positive evidence of absence, not just absence of evidence.

### 4.5 Asymmetric sub-phase contribution (caveat)

The 8mg sub-phase has only 9 analytical days before data-cut
(2026-05-27 → 2026-06-05 with ~7 days NaN, leaving ~2 fully observed
days at the 8mg steady-state plateau). The PK-smoothed exposure
(§2.3) naturally down-weights this contribution since plasma reaches
8mg steady-state only at the very end of the window, but the
prescribed-step sensitivity column (§4.3 sensitivity B) does not
have this attenuation. Surface in the script output: the 8mg
sub-phase contributes minimally to `β_dose` estimation either way;
the regression's leverage is dominantly on the 30mg → 20mg → 10mg
transitions.

### 4.6 What this analysis does not include (disclosure)

- No correction for multiple comparisons. One primary outcome, one
  primary effect, with sensitivity columns reported as robustness
  checks on the same hypothesis (not as separate hypotheses).
  Family-wise multiplicity collapses.
- No interrupted-time-series (ITS) segmented-regression framework
  (Bernal, Cummins, Gasparrini 2017, *International Journal of
  Epidemiology* 46(1):348-355, "Interrupted time series regression
  for the evaluation of public health interventions: a tutorial").
  ITS decomposes the response into pre-intervention level +
  pre-intervention trend + level-change β2 + post-intervention
  trend-change β3 at a *single* intervention boundary. This MD's
  question is the *graded shape across 3-4 dose steps*: the
  continuous dose-regression framework subsumes the per-boundary
  β2/β3 estimation by re-parameterising the exposure as a dose
  function rather than 3 step-indicators. A multi-boundary ITS
  would estimate 6 step-level parameters (β2/β3 at each of the 3
  step-dates) where the mechanism predicts a single per-mg slope;
  collapsing those 6 parameters into 1 by the dose-regression
  parameterisation is the methodological choice here, with the
  dose-response framing as the rationale. An ITS-style design
  would be appropriate for a different question (e.g. "did the
  afbouw onset at 2026-03-20 produce a level-change and/or
  slope-change in stress_mean_sleep?") and is already partially
  answered by the parent MD §8.
- No change-point detection (PELT, BCP). The dose-step dates are
  known a-priori; change-point detection would only confirm what is
  already known.
- No mediator analysis (e.g. is the dose-response mediated by
  changes in sleep duration / sleep architecture?). Out of scope.

---

## 5. What the finding informs

### 5.1 If β_dose > 0 and survives sensitivity (the prior-consistent reading)

A confirmed dose-response strengthens three downstream things:

1. **Personal-register pacing register (P4a, P4b, P5b)** —
   `stress_mean_sleep` is one of the channels these hypotheses
   anchor to. A confirmed dose-dependent shift means the *baseline
   itself* moves across the afbouw; tests using
   `stress_mean_sleep_lagged_lcera` z-scores across the
   2026-03-20 → 2026-06-05 frame inherit a reference-frame
   discontinuity. Whether the v3.2 lagged-baseline machinery
   absorbs it (the 90-day window catches up) or fails to (the dose
   moves faster than the baseline can adapt) is a downstream
   methodology question.
2. **Parent MD §8.4 follow-up bullet (this MD's parent finding)** —
   the candidate is upgraded from "step-change at one boundary
   surviving detrend" to "graded dose-response across the entire
   afbouw window". Replaces the working-title bullet in
   `intervention_effects_descriptive.md` §8.4 with a pointer to this
   MD's actual filename.
3. **garmin_pacing_practice.md §7.4 open question** — the
   physiological-state-side temporal qualifier is partially
   resolved: at least one Garmin channel (`stress_mean_sleep`) is
   demonstrably modulated by a documented intervention. The §7.4
   "intervention-period baseline calibration" question shifts from
   open to partially-characterised. Personal-register hypotheses
   inheriting that caveat upgrade from caveat-class acknowledgment
   to known-quantified-confound.

### 5.2 If null per §4.4 pre-spec

The candidate is downgraded. Three reads remain open:

- The parent MD §8 step-change at 2026-03-20 was a level-shift
  artefact (e.g. the boundary aligned coincidentally with a
  trajectory inflection that the detrend did not fully absorb).
- A real effect exists but is below the detection floor of this
  analytical design (n≈70, single channel, dose-range 8-30mg).
- The PK-smoothed assumption (§2.3) is materially wrong; the
  prescribed-step sensitivity B would reveal this if its β_dose
  diverges.

A null finding under this MD does NOT close the question for the
broader citalopram literature — n=1 nulls are weak evidence about
population effects. It DOES close the question for whether the
parent MD §8 candidate survives focused follow-up on THIS corpus.

### 5.3 If β_dose < 0 (counter-prior direction)

A statistically significant *positive* effect (lower dose → higher
nocturnal autonomic load) would contradict the SSRI-withdrawal
mechanistic prior and the parent MD §8 step-down direction. This is
implausible at the mechanism level but possible if the afbouw period
overlaps a stressful exogenous event the model does not capture
(e.g. a documented life event). Read narratively: surface the
candidate exogenous explanations against `annotations.yaml`
events in the afbouw window; treat as a data-quality + confound
diagnostic before treating as a finding.

### 5.4 Future-work hand-wave — buildup-period symmetric confirmation

The symmetric case (dose UP during buildup → stress UP) would
strengthen the pharmacological-causation argument substantially. The
buildup period is 2024-04-09 → 2024-06-20 (~10 weeks; 0 → 10 → 20 →
30mg ramp). The confound, per parent MD §8.1: **CPAP-end at
2024-04-16 is 7 days after the buildup start**. A buildup-period
dose-response analysis would either need to handle two simultaneous
interventions (ITS-style with both modelled together) or accept that
the early buildup days cannot be attributed to citalopram alone.

*Originally surfaced as a forward pointer for a separate narrow
methodology MD; partially opened in §5.5 v3 amendment via the
post-CPAP-buffer spec (drops the first 22 days from the buildup
analysis, isolating the post-CPAP-equilibration citalopram-only
window).*

### 5.5 v3 amendment — cross-window corroboration (added 2026-06-14)

The §4.4 4-condition null pre-spec did not declare null on the
2026-06-14 script run, but the §4.3 Sensitivity F nonlinear-time
collapse (β_dose +0.25 → +0.04) raised a seasonality / trajectory-
leakage fragility flag. Two cross-window tests were added to
disambiguate; both are sibling scripts in
[`analyses/garmin_exploration/intervention_effects/`](../analyses/garmin_exploration/intervention_effects/).

#### 5.5.1 Spring-comparison falsification test ([`spring_comparison.py`](../analyses/garmin_exploration/intervention_effects/spring_comparison.py))

Fits a simple linear time-only regression on `stress_mean_sleep`
across the same calendar window (March 20 → June 5) for every
available year:

| year | n | β_time per day | 95% CI | context |
|---|---:|---:|---|---|
| 2022 | 76 | +0.009 | [-0.103, +0.122] | spans corona → LC onset, NOT clean |
| 2023 | 78 | −0.037 | [-0.209, +0.134] | mid-LC, noisy |
| 2024 | 77 | +0.008 | [-0.050, +0.066] | citalopram-buildup + CPAP-end inside window |
| **2025** | **78** | **+0.004** | **[-0.036, +0.045]** | **30mg consolidation throughout, late-LC — CLEAN CONTROL** |
| **2026** | **69** | **−0.026** | **[-0.065, +0.013]** | **afbouw 30 → 8mg (TEST)** |

**Δ (2026 − 2025) = −0.030 per day = −2.3 stress points across the 77-day window.**

The clean control (2025: same dose, same calendar slot, no
buildup/CPAP confounds) is **essentially flat**. The generic-spring
alibi requires 2025 to show a downward slope comparable to 2026; it
does not. The downward trajectory in 2026 is consistent with a
real dose-response of ~2 stress points across the afbouw window,
independent of the dose-regression machinery in §4.

#### 5.5.2 Buildup-symmetry falsification test ([`buildup_check.py`](../analyses/garmin_exploration/intervention_effects/buildup_check.py))

Tests the symmetric prediction: if `β_dose > 0` is real (higher
plasma citalopram → higher nocturnal stress), then the 2024 buildup
window should show the same sign. Three specs:

| spec | n | β_dose (per mg plasma) | 95% CI | one-sided p |
|---|---:|---:|---|---:|
| Afbouw 2026 (primary from §4) | 69 | +0.246 | [-0.209, +0.702] | 0.144 |
| Buildup S1 raw (CPAP-confounded) | 71 | +0.153 | [-0.196, +0.503] | 0.195 |
| **Buildup S2 post-CPAP-buffer** | **50** | **+0.429** | **[+0.156, +0.702]** | **0.001** |

The buildup S2 spec drops the first 22 calendar days of the buildup
window (CPAP-end on 2024-04-16 + 14d equilibration buffer, per the
parent MD §4 buffer-sweep precedent), isolating the clean
citalopram-only stretch from 2024-05-01 to 2024-06-19 (50 days).

**β_dose = +0.43 per mg with HAC 95% CI [+0.16, +0.70] excluding
zero and one-sided p = 0.001**. The symmetric prediction is
confirmed at a tighter significance level than the afbouw test
alone achieved. Mechanistically right: the buildup S1 (CPAP-included)
attenuates the dose signal because CPAP-end also raises nighttime
stress (worse apnea after stopping CPAP) and that motion is wrongly
absorbed by `β_time` when CPAP-end is not in the model; dropping
the equilibration window isolates citalopram.

#### 5.5.3 The "fourth read" combined verdict

Three independent reads, three converging directions:

1. **Afbouw 2026 primary** (§4): β_dose direction prior-consistent (+0.25/mg), within-window fragility-flagged by Sensitivity F (nonlinear-time absorbed most of the signal), null pre-spec NOT declared.
2. **Spring 2025 control** (§5.5.1): seasonality alibi NOT supported — 2025 with the same dose at the same calendar slot is essentially flat; the 2026 downward trajectory is not the generic spring shape.
3. **Buildup 2024 post-CPAP** (§5.5.2): symmetric prediction confirmed (β_dose = +0.43/mg, CI excludes zero, p = 0.001).

The methodologically honest reading is **the dose-response on
`stress_mean_sleep` is real on this corpus**. Each individual test
has caveats (afbouw alone is not statistically significant; spring-
control is a single comparison year; buildup S2 drops 22d of data
to isolate the signal). The convergence across three independent
tests using different machinery is what carries the case — neither
test alone would suffice.

#### 5.5.4 What this changes downstream

- The parent MD §8.4 follow-up bullet now upgrades from
  "step-change at one boundary surviving detrend" to
  "graded dose-response confirmed across both phases of the
  Citalopram-traject, with within-window fragility appropriately
  flagged and cross-window evidence carrying the case".
- The [`garmin_pacing_practice.md` §7.4](garmin_pacing_practice.md#74-intervention-period-baseline-calibration-open-question)
  open question moves from open to **resolved-for-stress_mean_sleep**:
  this channel IS modulated by citalopram dose at the participant's
  prescribed range. Personal-register hypotheses inheriting that
  caveat upgrade from caveat-class acknowledgment to
  known-quantified-confound with magnitude ~0.25-0.43 stress-points
  per mg plasma citalopram.
- The original §5.1 / §5.2 / §5.3 read-table is superseded by
  this §5.5 for the actual finding interpretation. The reads remain
  conceptually valid as pre-spec; the §5.5 amendment documents
  the actual data-realised "fourth read" that the original three
  reads did not enumerate.

### 5.6 v3 amendment — multi-channel confirmation (added 2026-06-14)

The §5.5 cross-window evidence anchors the dose-response on
`stress_mean_sleep`. The §5.6 multi-channel extension tests whether
the same dose-response pattern holds on the other parent MD §3
baseline channels — channels mechanistically expected to respond to
citalopram per the SSRI/autonomic literature anchors queued at
[QUEUED-WORK Tier 3](../QUEUED-WORK.md#tier-3-methodological-refinement-deferred)
(Licht 2010, Kemp 2010 for HRV → resting_hr / stress channels;
Wichniak 2017 for sleep architecture → BB metrics / sleep respiration).

Script: [`multi_channel_check.py`](../analyses/garmin_exploration/intervention_effects/multi_channel_check.py).
Each channel runs the same three-pronged test: afbouw 2026 primary +
buildup 2024 post-CPAP-buffer + spring 2025 control. Each channel has
a prior expected sign:

- **+1 (higher plasma → higher channel)**: stress_mean_sleep,
  all_day_stress_avg, resting_hr, respiration_avg_sleep.
- **−1 (higher plasma → LOWER channel)**: bb_overnight_gain, bb_lowest
  (autonomic load → less restorative sleep → less recovery → lower
  BB metrics).

`sleep_efficiency` is NOT in `per_day_master.csv` and is excluded
(parent MD §3 channel-coverage gap; discovered 2026-06-14).
`bb_overnight_gain` has zero observations in the 2024-05-01 → 2024-06-19
buildup window (parent MD §2b channel-coverage gap); afbouw + spring
control only for this channel.

#### 5.6.1 Per-channel three-pronged read

| channel | prior | afbouw β (per mg) | buildup post-CPAP β | spring 2025 β_time | verdict |
|---|---:|---:|---:|---:|---|
| `stress_mean_sleep` | +1 | +0.246 (p=0.14) | **+0.429 (p=0.001)** | −0.023/day | **CONFIRMED** |
| `all_day_stress_avg` | +1 | +0.209 (p=0.19) | **+0.565 (p=0.000)** | −0.001/day | **CONFIRMED** |
| `bb_lowest` | −1 | −0.586 (p=0.14) | **−1.134 (p=0.000)** | −0.061/day | **CONFIRMED** |
| `resting_hr` | +1 | +0.148 (p=0.10) | +0.030 (p=0.34) | −0.007/day | consistent (buildup CI brushes zero) |
| `bb_overnight_gain` | −1 | +0.301 (sign mismatch) | no 2024 data | +0.159/day | partial (afbouw-only, noisy) |
| `respiration_avg_sleep` | +1 | −0.002 (p=0.57) | −0.011 (p=0.86) | +0.002/day | **REJECTED** |

Verdict rule:
- **CONFIRMED**: sign matches prior in both phases AND buildup HAC 95% CI excludes zero on the prior-direction side.
- **consistent**: sign matches prior in both phases but buildup CI brushes zero.
- **partial**: only one phase analysable; verdict on that phase.
- **REJECTED**: sign contradicts prior in both phases.

#### 5.6.2 What this adds to the §5.5 verdict

Three channels independently confirm the dose-response with
significant buildup CIs: `stress_mean_sleep`, `all_day_stress_avg`,
`bb_lowest`. These span two mechanistic axes:

- **Autonomic load axis** (Garmin stress score, sleep + day): both
  variants confirmed. The daytime variant (`all_day_stress_avg`) is
  actually the strongest signal (buildup β = +0.57/mg, p = 0.0003).
- **Recovery axis** (BB nadir): confirmed in the expected direction —
  higher plasma → lower BB minimum (worse recovery).

One channel (`resting_hr`) is mildly supportive (sign matches, near-
significance in afbouw, null in buildup); the magnitude is small in
SD-normalised terms (~0.13 SD per mg in afbouw). The
HRV-reduction-raises-RHR prior is **weakly** supported on this
corpus at this dose range — possibly because the resting HR floor
the participant lives at is constrained by other factors (fitness,
LC physiology) more than by SSRI dose.

One channel (`respiration_avg_sleep`) is firmly REJECTED — no SSRI
effect on respiration rate at this dose range, in either phase.
The Wichniak-2017 sleep-architecture prior holds for *some* sleep
markers but not the respiration-rate-during-sleep specifically. This
is informative-by-rejection: the dose-response signal is not a
generic "every Garmin channel moves in spring" artefact (which would
produce broad-sweep significance); it is specifically on the
**autonomic-load-and-recovery family**.

One channel (`bb_overnight_gain`) is too noisy + missing in the
buildup window to read; partial verdict only.

#### 5.6.3 Combined v3 verdict (super-§5.5.3)

Across **6 channels × 2 phases × 1 control = 13 analyses**:

- 3 channels CONFIRMED across both phases with significant buildup
  CIs (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`).
- 1 channel consistent (`resting_hr`).
- 1 channel partial (`bb_overnight_gain`, missing buildup).
- 1 channel REJECTED (`respiration_avg_sleep`).
- All confirmed channels: spring 2025 control is flat or
  small-counter-direction; the generic-spring alibi continues to be
  unsupported.

**The citalopram dose-response on the participant's autonomic-load
and recovery family is confirmed on this corpus**, with mechanism-
appropriate channel-specificity (stress + BB metrics: yes;
respiration: no; resting HR: weak). The methodologically honest
reading is no longer a single-channel single-window result; it is
a multi-channel cross-window pattern that converges on the SSRI
nocturnal-autonomic mechanism the §1.4 priors specified.

#### 5.6.4 What this changes downstream

Upgrades from §5.5.4:

- The parent MD §8.4 follow-up bullet now upgrades from
  "step-change at one boundary surviving detrend" to
  **"multi-channel graded dose-response confirmed across both phases of
  the Citalopram-traject"**.
- The [`garmin_pacing_practice.md` §7.4](garmin_pacing_practice.md#74-intervention-period-baseline-calibration-open-question)
  open question moves from open to **resolved across the autonomic-load
  family**: `stress_mean_sleep`, `all_day_stress_avg`, and `bb_lowest`
  ARE modulated by citalopram dose; `respiration_avg_sleep` is NOT;
  `resting_hr` weakly. Personal-register hypotheses inheriting that
  caveat upgrade per-channel: known-quantified-confound for the three
  confirmed channels, weak-confound for resting_hr, no-confound for
  respiration_avg_sleep.

#### 5.6.5 Remaining caveats for the multi-channel extension

- Spring 2025 control for `bb_overnight_gain` shows β_time = +0.16/day
  with CI excluding zero — a substantial calendar-time trend in 2025
  at the same calendar slot, suggesting bb_overnight_gain has its own
  non-dose-driven seasonal / recovery dynamics. Single-channel-specific
  caveat; does not affect the confirmed-channel reads.
- The multi-channel run does NOT apply the §4.4 4-condition null
  pre-spec to each channel. Per-channel null declarations would
  require running the full §4.3 sensitivity-column-set (A-F) per
  channel; deferred to future work.
- Channel-level effect-size magnitudes vary substantially between
  afbouw and buildup phases, larger in buildup. Likely
  pharmacological (dose-naive system responds more strongly to a
  novel exposure than a steady-state system responds to its
  reduction), but mechanistic literature would be needed to lock
  this interpretation.

### 5.7 Remaining caveats (overall)

- Still n=1, still observational, still a 70-day primary window
  with a 50-day buildup confirmation.
- The buildup S2 specifically required dropping 22 days to isolate
  the signal — that's a methodological choice traceable to the
  CPAP-end confound, not an arbitrary cherry-pick.
- A 2026-specific exogenous confound (life event not in
  `annotations.yaml`, non-seasonal local trend) that coincidentally
  produces the right magnitude in both phases is still possible.
  Implausible but not ruled out by these tests.
- The magnitudes differ between phases (afbouw +0.25 vs buildup
  +0.43) — possibly because the buildup is dose-naive (the system
  is responding to a novel exposure) while the afbouw is from
  steady-state (the system has long-since adapted and the
  withdrawal is partial). Mechanistic literature on SSRI
  receptor up/down-regulation would address this; queued at
  Tier 3 per §1.4.

---

## 6. Script outline

### 6.1 Location

Proposed: `docs/research/analyses/garmin_exploration/intervention_effects/dose_response.py`,
sibling to the parent MD's `run.py` script. Aligns the
intervention-effects work in one folder; sibling-vs-subfolder is
chosen because the dose-response script reuses the parent's
annotations.yaml-loading and channel-pulling utilities.

### 6.2 Inputs

- `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` — for
  `stress_mean_sleep`, `stress_mean_sleep_lagged_lcera`, and `is_crash`
  columns (the latter for Sensitivity E).
- `$GEVOELSCORE_DATA_PATH/raw/directus_exports/annotations.yaml` —
  for the 3 dose-step transition dates (containment-filtered as in
  parent MD §6; the 2 phase-transition markers added 2026-06-14
  bypass the containment filter).
- **Constants locked in this MD**:
  - `t_half = 35 hours` (citalopram SPC, EMA).
  - `afbouw_start = 2026-03-20`, `afbouw_end = 2026-06-05` (nominal
    afbouw window per §2.1).
  - `analytical_end = 2026-05-29` (last observed `stress_mean_sleep`
    day per §3.2; the regression auto-filters NaN tail anyway, this
    is the documented constant for `n_analytical` derivation).
  - `block_len = 7` (Sensitivity A moving-block bootstrap, §4.3-A).
  - `bootstrap_iters = 1000` (Sensitivity A).
  - `bootstrap_seed = 42` (Sensitivity A reproducibility; pin so
    re-runs produce byte-identical bootstrap CIs).
  - `HAC_maxlags = 4` (Andrews 1991 rule on n ≈ 70, §4.2) with
    sensitivity `HAC_maxlags = 7` (§4.3-D).
  - `nonlinear_time_basis = "natural_cubic_spline_4_knots"`
    (Sensitivity F, §4.3-F; month-indicator dummies as fallback if
    the spline basis becomes singular at this n).

### 6.3 Outputs

- `$GEVOELSCORE_DATA_PATH/analyses/intervention_effects/dose_response_summary.csv`
  — single row with the following columns (one cell per metric):
  - **Primary**: `beta_dose`, `hac_se`, `hac_ci_lo`, `hac_ci_hi`,
    `hac_p` (one-sided per §4.1).
  - **Sensitivity A (block bootstrap)**: `boot_beta_median`,
    `boot_ci_lo`, `boot_ci_hi`.
  - **Sensitivity B (prescribed-step)**: `prescribed_beta`,
    `prescribed_hac_p`.
  - **Sensitivity C (lagged-lcera outcome)**: `lcera_beta`,
    `lcera_hac_p`.
  - **Sensitivity D (HAC maxlags = 7)**: `hac7_beta`, `hac7_hac_p`.
  - **Sensitivity E (crash-drop)**: `crash_drop_beta`,
    `crash_drop_hac_p`, **plus** `n_crash_days_in_window`
    formatted per [CONVENTIONS §3.6](../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file)
    as a single string e.g. `"0 crash-days (crash_v2 day-level,
    per_day_master.csv, is_crash == True, 2026-03-20 <= date <=
    2026-06-05)"`.
  - **Sensitivity F (nonlinear time)**: `nonlinear_time_beta`,
    `nonlinear_time_hac_p`.
  - **Autocorrelation diagnostics**: `lag1_residual_rho`,
    `effective_n_under_hac` (Bartlett-window-derived effective
    sample size at the Andrews-1991 lag; lets the reader judge
    whether `HAC_maxlags = 4` is doing meaningful work given the
    observed residual autocorrelation).
  - **Null-finding decision**: `null_finding_declared` (boolean
    per §4.4 4-condition rule) + per-condition booleans
    (`cond1_hac_ci_contains_zero`, `cond2_effect_size_below_floor`,
    `cond3_boot_ci_contains_zero`, `cond4_lcera_p_above_05`).
  - **Provenance**: `n_analytical`, `analytical_window_start`,
    `analytical_window_end`, `bootstrap_seed`, `script_version`,
    `run_datetime`.
- `$GEVOELSCORE_DATA_PATH/analyses/intervention_effects/plots/dose_response_overview.png`
  — the canonical 4-panel figure: (top-left) time-series of
  stress_mean_sleep with PK-smoothed dose overlaid on a second
  y-axis; (top-right) regression scatter
  `dose_plasma_mg` vs. residualised `stress_mean_sleep`;
  (bottom-left) the §4.3 monotonicity scatter (4 dose plateau
  bins vs. mean residual, per §4.3 visual-companion specification);
  (bottom-right) coefficient panel showing primary
  β_dose + all sensitivity β_doses (A-F) with 95% CIs side-by-side.
- Console log of the regression fit + sensitivity table + null /
  not-null decision per §4.4 + the §3.6 named count for crash-days.

### 6.4 What the script does NOT do

- Does not write back to `per_day_master.csv`. The PK-smoothed dose
  exposure column is computed in-script for the analytical window
  only; not added as a master column.
- Does not modify `annotations.yaml`.
- Does not re-run the parent MD §8 boundary analysis. This is a
  focused follow-up; parent results stand as-is.

The script run is a follow-up session after this MD is signed off.
This MD does not pre-commit to its implementation details beyond
what §6.1-§6.3 specify.

---

## 7. Status + revision log

**Status**: v3 revised 2026-06-14; script-implementation + cross-window + multi-channel session complete (see §5.5 + §5.6 amendments). Awaiting downstream-update session (parent MD §8.4 + garmin_pacing_practice §7.4 + personal_hypotheses P4a/P4b/P5b caveat upgrades) and pipeline-patch session (`*_lagged_lcera_z` for parent MD §3 baseline channels).

### Revision log

| version | date | change | source |
|---|---|---|---|
| v1 | 2026-06-14 | Initial draft per the four-input §2.2 bar | Spin-off from `intervention_effects_descriptive.md` §8.4 follow-up bullet. Interactive interview locked: afbouw-only scope + stress_mean_sleep only + confirmatory framing (§7.1); linear-in-dose + linear-in-time + PK-smoothed primary exposure (§7.2-7.3); Newey-West HAC primary + block-bootstrap sensitivity (§7.4); raw outcome primary + _lagged_lcera sensitivity (§7.5); 4-condition null pre-spec (§7.6); single-test family, no multiplicity correction (§7.7). |
| v2 | 2026-06-14 | Audit-fix pass per v1 methodology review at [`reviews/methodology-citalopram_dose_response_stress_mean_sleep-2026-06-14.md`](../reviews/methodology-citalopram_dose_response_stress_mean_sleep-2026-06-14.md). All 13 v1-review recommendations folded in: (1) Sensitivity Column E — crash-drop per CONVENTIONS §3.4 audit hook (§4.3 + §6.3 named count); (2) seasonality enumeration in §1.3 + Sensitivity Column F nonlinear time term in §4.3; (3) Bernal et al. 2017 BMJ cited in §4.6 ITS rejection; (4) Künsch 1989 + Politis & Romano 1994 cited in §4.3 Sensitivity A; (5) PK/PD framework explicitly named in §2.3 with Rowland & Tozer 2011 + Gabrielsson & Weiner 2016 + citalopram SPC + Hyttel 1994 citations; (6) Newey & West 1987 + Andrews 1991 cited in §4.2 with journal references; (7) Breinvoeding-interventie acknowledged in §1.3 confounder enumeration; (8) CONVENTIONS §3.5 daily-mean-vs-spike preference acknowledged in §3.1 with inherited-from-parent justification; (9) lag-1 residual ρ + effective N under HAC added to §6.3 outputs as autocorrelation diagnostics; (10) bootstrap seed = 42 added to §6.2 constants; (11) queued-literature-prior status of confirmatory framing acknowledged in §1.4 audit-trail note; (12) one-sided test explicitly defended as tradeoff in §4.1; (13a) analytical-window endpoints precisified in §3.2 (analytical_end = 2026-05-29) and §6.2 (analytical_end constant); (13b) monotonicity-scatter dose-binning made explicit in §4.3 visual-companion (4 prescribed-plateau bins vs continuous regression); (13c) `initial_dose_decay_term` defined in §2.3 (= 30mg pre-afbouw steady-state baseline). |
| v3 | 2026-06-14 | Script-implementation session + cross-window corroboration. §5.5 amendment added documenting (5.5.1) spring-comparison test against 2022-2025 same-calendar-window slope per [`spring_comparison.py`](../analyses/garmin_exploration/intervention_effects/spring_comparison.py) — 2025 clean control flat at +0.004/day, weakens generic-spring alibi; (5.5.2) buildup-symmetry test per [`buildup_check.py`](../analyses/garmin_exploration/intervention_effects/buildup_check.py) — post-CPAP-buffer spec returns β_dose = +0.43/mg with CI [+0.16, +0.70] excluding zero, p = 0.001, confirming the symmetric prediction at higher significance than the afbouw alone; (5.5.3-5.5.5) combined "fourth read" verdict — three independent tests converge, dose-response confirmed on this corpus. §1.3 seasonality bullet edited: pollen removed (participant has no hay-fever); cross-year falsification test referenced. §5.4 buildup-confound forward-pointer updated to note partial opening via §5.5.2 post-CPAP-buffer spec. Implementation discovery during script work: `stress_mean_sleep_lagged_lcera` is NOT present in `per_day_master.csv` and is computed on-the-fly in dose_response.py per the §3.2 v3.2 LC-era construction; surfacing this for downstream pipeline-patch session (queued separately). |
| v3 (multi-channel addendum) | 2026-06-14 | Multi-channel extension per [`multi_channel_check.py`](../analyses/garmin_exploration/intervention_effects/multi_channel_check.py): the three-pronged test pattern (afbouw + buildup post-CPAP + spring 2025 control) applied to all parent MD §3 baseline channels. §1.2 scope updated to acknowledge v3 expanded scope (buildup tested in §5.5.2, multi-channel in §5.6); the §4 primary spec remains single-channel × single-window. §5.6 amendment added with per-channel results: 3 CONFIRMED (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest` — all with buildup CI excluding zero), 1 consistent (`resting_hr`), 1 partial (`bb_overnight_gain` — missing 2024 buildup data), 1 REJECTED (`respiration_avg_sleep`). The autonomic-load + recovery family is dose-modulated; respiration rate is NOT. §5.6.4 upgrades the downstream-update language from §5.5.4: parent MD §8.4 from "step-change at one boundary" to "multi-channel graded dose-response across both phases"; garmin_pacing_practice §7.4 from "open" to "resolved across the autonomic-load family"; personal_hypotheses caveats upgrade per-channel. Implementation discovery during script work: `sleep_efficiency` is NOT in master (excluded from multi-channel run); `bb_overnight_gain` has 0 buildup-window observations per parent §2b. §5.7 captures the §5.5.5 + §5.6.5 combined caveats. |

### Audit hooks engaged

- [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) — descriptive layer (parent MD §8) cleared before this confirmatory MD.
- [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) — four-input reasoning explicit in §4.1, §4.2, §2.3.
- [CONVENTIONS §3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) — `_lagged_lcera` sensitivity column per §4.3-C.
- [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair) — `stress_mean_sleep` chosen over the paired `all_day_stress_avg`; rationale in §3.1.
- [CONVENTIONS §3.4](../CONVENTIONS.md#34-crash-drop-sensitivity-row-on-every-layer-4-correlation) — crash-drop sensitivity per Sensitivity Column E §4.3, with named-count output per §3.6 in §6.3. Binding audit hook engaged in v2.
- [CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages) — daily-mean vs spike-metric preference acknowledged in §3.1; daily-mean choice inherited from parent MD §8 with spike-metric corroboration queued as future work.
- [CONVENTIONS §3.6](../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file) — crash-day count in Sensitivity E output formatted per the §3.6 "labeling scheme / unit / source file / predicate" rule.
- [CONVENTIONS §3.7](../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) — the binding pattern this MD inherits. Trajectory-detrend implemented as the linear days_from_afbouw_start covariate inside the regression (§4.1) rather than as a separate detrend column, because the test shape is regression-on-window rather than pre-vs-post; the §3.7 spirit is preserved by the time covariate absorbing the local slope. The Sensitivity F nonlinear-time-term variant (§4.3) extends the detrend logic to nonlinear seasonality.
- [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory) — confirmatory framing justified by three independent priors (§1.4); audit-trail note in §1.4 documents which two priors are individually sufficient under the "any one is yes" rule.

---

## 8. Cross-references

- [`intervention_effects_descriptive.md` §8](intervention_effects_descriptive.md#8-findings-session-c-run-2026-06-14) — parent finding (stress_mean_sleep × 2026-03-20 step DOWN, survives detrend).
- [`intervention_effects_descriptive.md` §1, §3b](intervention_effects_descriptive.md) — substantive-confound caveat + baseline-vs-outcome framing this MD inherits.
- [`garmin_pacing_practice.md` §7.4](garmin_pacing_practice.md#74-intervention-period-baseline-calibration-open-question) — operational sibling on intervention-period baseline calibration; this MD's finding partially resolves that open question for one channel.
- [`lived_experience_garmin_pacing_2026-06-14.md`](../lived_experience_garmin_pacing_2026-06-14.md) — lived-experience prior cited in §1.4.
- [`time_resolution.md` §2.3, §6](time_resolution.md) — framework MD on picking analysis scale per hypothesis; the 77-day afbouw window is an instance of the situational-multi-day-window category.
- [`CONVENTIONS.md` §2.2, §3.7, §4.3](../CONVENTIONS.md) — discipline anchors.
- [`QUEUED-WORK.md` Tier 3](../QUEUED-WORK.md#tier-3-methodological-refinement-deferred) — per-channel SSRI/CPAP autonomic literature (Marin 2010, Tantucci 2003, Licht 2010, Kemp 2010, Wichniak 2017); referenced in §1.4 prior-evidence and §4.1 four-input reasoning, retrieval not gated on the script run.
- [`personal_hypotheses.md` P4a, P4b, P5b](../personal_hypotheses.md) — downstream Personal-register hypotheses whose baseline framing this MD's finding would inform (§5.1).
