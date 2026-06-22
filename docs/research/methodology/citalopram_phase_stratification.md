# Citalopram-phase stratification for downstream tests — methodology framework

**Status**: drafted 2026-06-14 as a producer-mode framework MD per CONVENTIONS §2.2.

This MD operationalises the **downstream consequences** of the
quantified citalopram dose-response finding in
[`citalopram_dose_response_stress_mean_sleep.md`](citalopram_dose_response_stress_mean_sleep.md)
(v3). It is a **framework MD** — it does not run a hypothesis test;
it specifies the stratification + adjustment patterns that future
Wiggers and Personal-register hypothesis MDs should adopt when their
predictor or outcome touches a confirmed-dose-modulated channel.

Cited by every downstream hypothesis MD whose predictor or outcome
uses one of the three v3-CONFIRMED channels (see §3 below). Sibling
to [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)
(LC-phase main partition); this MD adds a *sub-partition* of the LC
era for the medicated-LC sub-eras.

---

## 1. What this MD is, and what it does not

### 1.1 What this MD is

A **framework specification** for how downstream hypothesis tests
should handle the quantified Citalopram dose-response on the three
v3-CONFIRMED channels. Specifically:

- A canonical four-phase Citalopram-traject stratification axis
  (§3).
- Per-channel inheritance rules — which channels need which
  treatment (§4).
- Three downstream-test treatment patterns: per-phase stratification,
  dose-adjusted predictor, and full per-mg β subtraction (§5).
- A pre-registration template for what new hypothesis MDs should
  adopt (§6).
- A worked example (§7).

### 1.2 What this MD does not do

- Does NOT re-derive the dose-response finding. That work lives
  in [`citalopram_dose_response_stress_mean_sleep.md` §5.5-§5.6](citalopram_dose_response_stress_mean_sleep.md#55-v3-amendment--cross-window-corroboration-added-2026-06-14).
- Does NOT extend the dose-response to channels outside the parent
  MD §3 baseline-channel family.
- Does NOT pre-commit to which hypothesis MDs adopt which pattern.
  The choice is per-hypothesis, made at pre-reg time by the
  hypothesis author.
- Does NOT modify CONVENTIONS.md or the parent intervention-effects
  MD. Forward pointers only.

### 1.3 Inheritance bar

This MD inherits the four-input §2.2 reasoning from the v3 dose-response
MD; the per-channel quantified offsets are the empirical anchor and
the SSRI/autonomic literature (Licht 2010, Kemp 2010, Wichniak 2017 —
queued at QUEUED-WORK Tier 3) is the mechanistic anchor. The
framework choice itself is consequence-driven: cross-phase aggregation
on confirmed channels is biased; per-phase or dose-adjusted analysis
is unbiased; downstream hypothesis MDs need a canonical pattern to
adopt.

**Methodological anchor for §5.B**: the dose-adjusted-predictor
technique is the standard *covariate-adjustment for a measured
time-varying confounder* move from observational-causal-inference
(counterfactual framework: Rubin 1974; Pearl 2009). For n-of-1
self-tracked designs specifically, the project anchor is
[Daza 2018](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)
*Methods Inf Med*, which adapts the counterfactual framework to
time-varying confounders in within-subject self-tracking data —
exactly this situation. §5.B operationalises that pattern; this
framework MD's contribution is the per-channel offset table, the
phase axis, and the pre-registration template, not the technique
itself.

---

## 2. The substantive finding being framework-ised

Per [`citalopram_dose_response §5.6.1`](citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read),
the v3 multi-channel test produced a per-channel verdict matrix:

| channel | verdict | buildup post-CPAP β/mg (CI, p) | afbouw β/mg | spring 2025 control β_time |
|---|---|---|---:|---:|
| `stress_mean_sleep` | **CONFIRMED** | +0.43 [+0.16, +0.70], p = 0.001 | +0.25 | −0.023/day (flat) |
| `all_day_stress_avg` | **CONFIRMED** | +0.57 [+0.24, +0.89], p = 0.000 | +0.21 | −0.001/day (flat) |
| `bb_lowest` | **CONFIRMED** | −1.13 [−1.78, −0.49], p = 0.000 | −0.59 | −0.061/day (flat) |
| `resting_hr` | weakly consistent | +0.03 [−0.12, +0.18], p = 0.34 | +0.15 | −0.007/day (flat) |
| `bb_overnight_gain` | partial (no 2024 data) | — | +0.30 (sign mismatch) | +0.159/day (NOT flat) |
| `respiration_avg_sleep` | **REJECTED** | −0.01 [−0.03, +0.01], p = 0.86 | −0.002 | +0.002/day (flat) |

The three CONFIRMED channels each show:

- Sign-concordant β in both phases (afbouw + buildup).
- Buildup CI excludes zero on the prior-direction side.
- Flat spring-2025 control (rules out generic-spring alibi).

The three other channels (resting_hr weak; bb_overnight_gain partial;
respiration_avg_sleep rejected) do NOT inherit the framework's
downstream-treatment requirements.

---

## 3. The four-phase Citalopram-traject stratification

**Cross-axis position**: this MD defines the inner axis (medication-state)
that nests within the LC recovery-phase axis defined by
[`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) §3.5. Tests
crossing more than one citalopram phase OR more than one recovery phase
adopt the 3-layer cross-classification per
[`lc_recovery_phase_axis §1.3`](lc_recovery_phase_axis.md#13-relationship-to-existing-axes--three-layers).
This MD's `unmedicated` phase (LC start 2022-04-04 → 2024-04-08) is
sub-partitioned by the recovery-phase axis into `lc_pre_ergo`,
`pacing_pre_citalopram_learning` (4a), and `pacing_habit_established`
(4b) per `lc_recovery_phase_axis §3.3 + §3.4`; this MD's `buildup` +
`consolidation` + `afbouw` phases all nest within
`lc_recovery_phase_axis §3.5` `citalopram_modulated`. Reciprocal lock-time
cross-citation added 2026-06-19 per the recovery-phase axis r2 lock.

The Citalopram-traject is a sub-partition of the LC era with the
following phases:

| phase | window | prescribed dose | plasma steady-state | days in corpus |
|---|---|---|---:|---:|
| **unmedicated** | LC start (2022-04-04) → 2024-04-08 | 0 mg | 0 mg | ~735 days |
| **buildup** | 2024-04-09 → 2024-06-19 | 0 → 10 → 20 → 30 mg ramp | 0 → 30 mg (PK-smoothed) | 72 days |
| **consolidation** | 2024-06-20 → 2026-03-19 | 30 mg | 30 mg | ~638 days |
| **afbouw** | 2026-03-20 → 2026-06-05 | 30 → 20 → 10 → 8mg ramp | 30 → ~8 mg (PK-smoothed) | 78 days |
| **post-afbouw** | 2026-06-06 → present | (TBD: 8mg ongoing or stopped) | low/zero (TBD) | ongoing |

**Source of truth** for boundary dates:
`$GEVOELSCORE_DATA_PATH/raw/directus_exports/annotations.yaml`
(category: `interventie`, label: "Citalopram fase 1/2/3/4/5/6 …" spans).
Per [`intervention_effects_descriptive §2`](intervention_effects_descriptive.md#2-interventions-in-scope--curated-catalog)
the canonical edit target is `hand_curated_spans.yaml`; `annotations.yaml`
is regenerated and direct edits are silently reverted.

> **Table-text alignment note (2026-06-22)**: Table text aligned to
> `citalopram_phase()` Python helper 2026-06-22; previously had off-by-one
> (afbouw right-edge / post_afbouw left-edge); surfaced by
> `lc_recovery_phase_axis.md` r2-lock d47e0d3 producer-side observation.

**Algorithmic change-point detection not used.** PELT
([Killick et al. 2012](https://www.tandfonline.com/doi/abs/10.1080/01621459.2012.737745))
and Bayesian online change-point ([Adams & MacKay 2007]) are the
state-of-art algorithmic alternatives for deriving phase boundaries;
they are **named-and-rejected** here for one specific reason: the
four-phase boundaries are anchored to documented clinical dose-change
events (Citalopram fase 1/2/3/4/5/6 spans in `hand_curated_spans.yaml`),
which is a stronger anchor than data-driven detection. An algorithmic
sweep could *corroborate* the boundary dates from observed channel
shifts but could not *change* them — and the v3 multi-channel
empirical confirmation (per [§2 table above](#2-the-substantive-finding-being-framework-ised)
and [dose-response §5.5/§5.6](citalopram_dose_response_stress_mean_sleep.md#55-v3-amendment--cross-window-corroboration-added-2026-06-14))
already provides post-hoc validation that the pre-specified boundaries
correspond to real distributional shifts. Per CONVENTIONS §2.2 input 1
discipline, naming the algorithmic alternative is the bar; rejection
with a corpus-specific reason satisfies it.

**Computing the phase for an arbitrary date d**:

```python
def citalopram_phase(d: date) -> str:
    if d < date(2024, 4, 9):
        return "unmedicated"
    if d < date(2024, 6, 20):
        return "buildup"
    if d < date(2026, 3, 20):
        return "consolidation"
    if d < date(2026, 6, 6):
        return "afbouw"
    return "post_afbouw"
```

The hardcoded dates above are appropriate for this *methodology MD
spec* (the boundaries ARE locked here as the canonical values for
the framework); a worked production version of the function should
load the dates from `annotations.yaml` at runtime so a future boundary
refinement updates downstream consumers automatically.

**Computing `dose_plasma_mg(d)` for arbitrary d**: per the canonical
PK formula in [`dose_response §2.3`](citalopram_dose_response_stress_mean_sleep.md#23-pk-smoothed-plasma-proxy-primary-exposure)
+ the buildup/afbouw convolution, with one explicit pre-citalopram
case: **`dose_plasma_mg(d) = 0` for `d < 2024-04-09`** (unmedicated
phase). This is the natural extrapolation of the PK convolution
(initial dose = 0) but is stated explicitly to prevent consumers
from NaN-propagating pre-citalopram dates or treating them as
missing. Under §5.B with this convention, the dose-adjusted
predictor on unmedicated dates reduces to the raw channel value.

**Computing the PK-smoothed plasma dose for an arbitrary date d**:
see [`citalopram_dose_response §2.3`](citalopram_dose_response_stress_mean_sleep.md#23-pk-smoothed-plasma-proxy-primary-exposure)
for the canonical formula; reusable verbatim from the
[`dose_response.py`](../analyses/garmin_exploration/intervention_effects/dose_response.py)
script. Note that the formula assumes the participant arrived at 30mg
steady-state on 2024-06-20 and stayed there until 2026-03-20; for
arbitrary t outside the buildup or afbouw windows this is correct.
For dates inside the buildup or afbouw windows the convolution
captures the smoothed plasma trajectory.

---

## 4. Per-channel inheritance rules

A downstream hypothesis MD whose **predictor or outcome touches one
of the v3-CONFIRMED channels** (§2) MUST adopt one of the three
treatment patterns in §5. Specifically:

| channel | inheritance status | required treatment | rationale |
|---|---|---|---|
| `stress_mean_sleep` | **load-bearing CONFIRMED** | one of §5.A / §5.B / §5.C | dose-modulated at +0.25-0.43 per mg; cross-phase pooling on absolute values is biased |
| `all_day_stress_avg` | **load-bearing CONFIRMED** | one of §5.A / §5.B / §5.C | dose-modulated at +0.21-0.57 per mg; same |
| `bb_lowest` | **load-bearing CONFIRMED** | one of §5.A / §5.B / §5.C | dose-modulated at −0.59 to −1.13 per mg; same |
| `resting_hr` | weak | §5.A (per-phase stratification) recommended as sensitivity arm; not load-bearing | sign-concordant but buildup CI brushes zero |
| `bb_overnight_gain` | partial / non-citalopram dynamics | §5.A as sensitivity arm; calendar-time-dynamic per spring 2025 control | independent non-dose dynamics — needs investigation in a separate MD |
| `respiration_avg_sleep` | REJECTED dose-modulated | no treatment required | informative-by-rejection; use freely |
| any other parent MD §3 baseline channel | not yet tested | no treatment required by this MD; future v3 sweep extension could add | unknown dose-response status |
| `gevoelscore` (outcome channel) | **deliberately out of scope** per parent §3b | not addressed by this MD | gevoelscore is the outcome side; baseline-channel logic does not apply |

**Audit hook**: any new hypothesis MD whose predictor or outcome
references one of the load-bearing CONFIRMED channels and does NOT
adopt one of the §5 treatments must justify the omission in its
caveats section with a one-sentence pointer to this MD.

---

## 5. The three downstream-test treatment patterns

For any test on a load-bearing CONFIRMED channel where the test
spans more than one Citalopram phase, pick **one** of:

### 5.A Per-phase stratification (the default; lowest-risk)

Run the test separately within each phase. Report per-phase results.
Cross-phase concordance is a separate read; the within-phase result
is the primary.

- **Pros**: minimal assumptions; works even if the per-mg β is
  imprecise; phase-specific behaviour is visible.
- **Cons**: shrinks n by ~5× (e.g. 4 of ~5 phases each ~70-700 days);
  power loss; complicates the "single-pool" CONVENTIONS pattern.

**When to use**: when the phase-specific question itself matters
(e.g. "does the pacing protocol's BB floor behave the same under
all four phases?"), OR when the test is being done in a phase that
already has good n (consolidation has ~638 days; the others are
much shorter).

**Optional ±N-day boundary buffer**. For §5.A specifically, a
hypothesis MD may exclude the first N days of each new phase to
let plasma re-equilibrate; 14 days is the citalopram pharmacological
default per [parent MD §4 buffer-sweep rationale](intervention_effects_descriptive.md#4-analysis-shape).
The PK-smoothing of §5.B makes this irrelevant for §5.B because the
plasma trajectory is continuous; per-phase stratification under §5.A
treats phase as a categorical, which is where the buffer choice
arises. The default is no buffer (use the full phase window); the
buffer is a sensitivity arm.

### 5.B Dose-adjusted predictor (recommended for cross-phase tests)

This is the *covariate-adjustment for a measured time-varying
confounder* move from observational-causal-inference (Rubin 1974;
Pearl 2009 counterfactual framework), adapted to n-of-1 self-tracked
designs per [Daza 2018](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)
*Methods Inf Med*. This MD's §5.B contribution is the per-channel
β table + the canonical phase axis, not the technique itself.

Compute a dose-corrected channel:

```python
channel_adj(d) = channel(d) - beta_dose * dose_plasma_mg(d)
```

where `beta_dose` is locked from
[`citalopram_dose_response §5.6.1`](citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read)
(use the **post-CPAP buildup β** since it has tighter CIs:
+0.43 for stress_mean_sleep, +0.57 for all_day_stress_avg, −1.13
for bb_lowest). Use `channel_adj` everywhere the original `channel`
was used. The rolling baseline now operates on a dose-corrected
signal that is stationary across phase boundaries.

**Implicit tradeoff — buildup-β vs afbouw-β**. The buildup β is
prescribed as default because its CIs are tighter, but the choice
has a corpus-specific tradeoff: the buildup β was estimated on a
dose-naive system, which may *overcorrect* a downstream test
running in consolidation or afbouw where the system has adapted to
the drug. The tradeoff is **conservative-against-undercorrection
at the cost of potential overcorrection at steady-state**. For
steady-state-window-only tests (e.g. a consolidation-only test),
the afbouw β is the alternative anchor; it has wider CIs but is
closer in dose-state to the test window. The user has pinned the
buildup-vs-afbouw asymmetry investigation as out-of-scope (per
[§8.4 below](#84-the-buildup-and-afbouw-magnitude-asymmetry-as-a-research-question));
this is a methodological flag for the framework consumer, not an
action item for the framework.

**Temporal-state note on lagged-lcera variants**. The §4 inheritance
table lists `stress_mean_sleep_lagged_lcera` and similar
`_lagged_lcera` variants as load-bearing inputs that adopt the
framework. These variants are NOT yet materialised in
`per_day_master.csv` as of 2026-06-14; the dose-response MD's
[`dose_response.py`](../analyses/garmin_exploration/intervention_effects/dose_response.py)
computes them on the fly. A hypothesis MD adopting §5.B today must
either (a) compute the lagged-lcera variant in-script per [CONVENTIONS
§3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses)
or (b) wait for the pipeline patch (queued; tracked in
`citalopram_dose_response_stress_mean_sleep.md §7`). The framework
itself is unaffected; this is a consumer-side temporal-state caveat.

- **Pros**: preserves single-pool framework; no n loss; the per-mg
  β does the heavy lifting.
- **Cons**: depends on the locked β being correct (the dose-response
  MD has 95% CIs on these, not point estimates); per-mg β is from
  the buildup window which may not be exactly the participant's
  current dose-sensitivity. Mis-specification under-corrects (or
  overcorrects at steady-state — see tradeoff note above) and
  leaves residual phase-effects in the predictor.

**When to use**: cross-phase pooled tests where n is critical and
the β estimate is sufficiently precise (CIs in §5.6.1 are tight
enough for stress and BB channels).

### 5.C Joint dose-and-phase model (most rigorous; highest cost)

Fit the test as a multi-variable model with both the dose-adjusted
predictor (§5.B) AND a phase indicator (§5.A) as covariates. The
phase indicator absorbs any residual phase-effects the dose
adjustment under-fits; the dose-adjusted predictor still does the
within-phase work.

- **Pros**: belt-and-braces; explicitly tests whether dose-adjustment
  captures the phase effect fully (if phase indicator's coefficient
  is non-zero, dose-adjustment is incomplete).
- **Cons**: most parameters; smallest residual df; complicates the
  test machinery.

**When to use**: confirmatory tests with substantial methodological
risk (load-bearing project claims); diagnostic tests that need to
audit whether §5.B is sufficient.

---

## 6. Pre-registration template for new hypothesis MDs

Any new hypothesis MD whose predictor or outcome touches a
load-bearing CONFIRMED channel (see §4) MUST include the following
in its caveats / methodology section:

### Template — Citalopram-phase inheritance caveat

> **N. Citalopram-phase inheritance — quantified by [`citalopram_phase_stratification`](citalopram_phase_stratification.md) + [`citalopram_dose_response §5.6`](citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14).**
> The predictor `[channel name]` is dose-modulated at
> `[β/mg]` per mg of plasma citalopram (v3 2026-06-14 confirmed).
> This hypothesis is tested **using treatment §[5.A | 5.B | 5.C]**
> per [`citalopram_phase_stratification §5`](citalopram_phase_stratification.md).
> Treatment rationale: `[one-sentence reason for the choice]`.
> Within-phase / dose-adjusted results are the primary read;
> cross-phase aggregation without treatment is not.

Filling this template in a hypothesis MD's caveats section satisfies
the §4 audit hook.

**Independent obligations — adopting this framework does NOT relieve
the test of**:

- **Autocorrelation handling** per [CONVENTIONS §3 + Natesan Batley
  2023](../CONVENTIONS.md#3-statistical-hygiene--pre-flight-audit-hooks):
  HAC SE / block bootstrap / effective-N. Dose-adjustment removes
  one confounder; serial dependence in the residuals is a separate
  obligation and a plain-OLS SE on the dose-adjusted predictor is
  still wrong.
- **Crash-drop sensitivity** per [CONVENTIONS §3.4](../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions):
  any Layer 4+ regression on PEM-pacing channels reports a leave-out
  diagnostic. The framework adds dose-adjustment ON TOP of the §3.4
  obligation, it does not replace it.
- **Spike-detecting metrics where applicable** per [CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages):
  if the underlying mechanism is acute arousal, daily-mean
  dose-adjustment may still miss the signal. The framework operates
  at whatever resolution the consumer hypothesis adopts.
- **Trajectory-detrend sensitivity** per [CONVENTIONS §3.7](../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons)
  for raw pre-vs-post tests on the LC frame.

In short: the framework is a *single-confounder fix* (dose), not a
*comprehensive-statistical-hygiene fix*. The CONVENTIONS §3 audit hooks
remain binding alongside §4/§5 of this framework.

---

## 7. Worked example — Personal-register P5b under §5.B

P5b (prevailing rest-stress predicts next-day crash) uses
`stress_mean_sleep` AND `all_day_stress_avg` jointly in its predictor.
Both channels are CONFIRMED. P5b inherits the framework.

### Pre-v3 reading (now obsolete)

P5b caveat 6 (pre-v3): *"the rolling-baseline z-score on
stress_mean_sleep may be miscalibrated for days within ±60 of
2026-03-20; sensitivity arm needed."*

### v3 reading after this framework

P5b caveat 6 (post-v3, now active in [`personal_hypotheses.md`](../personal_hypotheses.md)):
adopt treatment **§5.B (dose-adjusted predictor)** because:

- P5b is a cross-phase test by design (LC era pooled).
- The two channels have tight β CIs.
- Single-pool framework matters for power (P5b is testing a
  differential prediction; n loss from per-phase stratification
  would hurt).

Pre-reg should specify:

```
stress_mean_sleep_adj(d)    = stress_mean_sleep(d)
                              - 0.43 * dose_plasma_mg(d)
all_day_stress_avg_adj(d)   = all_day_stress_avg(d)
                              - 0.57 * dose_plasma_mg(d)
```

Then compute the rolling baseline on `*_adj`, then compute the
stress-with-low-motion count threshold-crossing rate.

**Numerical walkthrough on one day**. Take 2025-08-15 (consolidation
phase, mid-plateau, prescribed 30mg, PK-smoothed plasma at 30mg):

| step | value | source |
|---|---:|---|
| Raw `stress_mean_sleep(2025-08-15)` | 18.3 | `per_day_master.csv` |
| `dose_plasma_mg(2025-08-15)` | 30 mg | PK convolution returns plateau value |
| `β_dose` for stress_mean_sleep | +0.43 / mg | locked from dose-response §5.6.1 |
| Dose attribution | +0.43 × 30 = 12.9 | of the raw 18.3, ~13 points are attributed to citalopram |
| `stress_mean_sleep_adj(2025-08-15)` | 18.3 − 12.9 = **5.4** | the dose-removed signal P5b uses |

Doing the same calculation on 2026-05-01 (afbouw, plasma ~10 mg)
would give `18.3 − 0.43 × 10 = 14.0` — a much higher adjusted value
than the consolidation day, even at the same raw 18.3, because the
afbouw day has less drug-attributable load. Without dose-adjustment,
P5b's z-score would treat these two days as identical when they are
not.

The unmedicated-phase case (e.g. 2023-05-15, `dose_plasma_mg = 0`)
reduces to `stress_mean_sleep_adj = stress_mean_sleep` per §3's
explicit zero-dose convention.

**Sensitivity arm**: §5.A per-phase stratification reported alongside
the §5.B primary, with the §5.C joint model as an audit-check.
Concordance across the three reads = high confidence; divergence =
the §5.B mis-specification flag.

---

## 8. Implications for the project's broader methodology stack

The v3 dose-response finding surfaces three methodological lessons
broader than this framework's scope. Each gets a one-line acknowledgment
+ forward pointer; substantive treatment is queued.

### 8.1 Cross-window replication discipline

The v3 strengthening of the dose-response came from independent
cross-window evidence (afbouw + buildup symmetric + spring 2025
control), not from more machinery on the original window. **Within-
window p-values on n=1 day-level data are high-fragility**; cross-
window concordance is high-information. Future hypothesis tests
should pre-spec cross-window replication arms where the corpus
permits.

**Queued**: a separate framework MD on cross-window replication
patterns, OR an addition to CONVENTIONS §3 as a new audit hook.

### 8.2 Multi-channel "rejection-as-credibility"

The v3 multi-channel sweep produced 3 CONFIRMED + 1 weak + 1 partial
+ 1 REJECTED. The REJECTION of `respiration_avg_sleep` (combined with
the rejection's mechanism-appropriateness: SSRIs don't affect
respiration rate per Wichniak 2017) **earned the confirmations their
credibility** by ruling out a "spring moves everything" artefact.

**Implication**: multi-channel hypothesis families should include
**channels expected to NOT respond** (per mechanism priors) and
report their rejections. Same-direction-everywhere results are less
credible than mixed-direction-with-mechanistic-fit results.

**Queued**: a CONVENTIONS audit-hook addition (§3.x) for
"rejection-channel inclusion in multi-channel hypothesis families".

### 8.3 PK/PD as a first-class corpus axis

The PK-smoothed plasma dose is now a **first-class data axis** on
this corpus, not just an analytical convenience for the dose-response
MD. Any test touching the medicated-LC era can use
`dose_plasma_mg(d)` as a covariate or as the predictor itself.

**Queued**: a `dose_plasma_mg` column added to per_day_master.csv
via `pipeline/03_consolidate/build_unified_dataset.py` (sibling work
to the `*_lagged_lcera_z` columns queued separately). Same pattern
as the existing `lc_phase` column.

### 8.4 The buildup-and-afbouw magnitude asymmetry as a research question

The buildup post-CPAP β is consistently ~1.5-2× larger than the
afbouw β across all three CONFIRMED channels. The dose-response MD
§5.6.5 noted but did not resolve this. Candidate explanations:

- Pharmacological: dose-naive system responds more strongly to a
  novel exposure than steady-state system responds to its reduction
  (SSRI receptor up/down-regulation literature would address).
- Corpus-specific: the participant's LC physiology in 2024 vs 2026
  is different (deeper recovery state in 2026); the same per-mg β
  produces a different absolute effect.
- Methodological: residual CPAP-end effects at 22d buffer; or the
  PK-smoothed dose function under-corrects the buildup more than
  the afbouw.

**Queued**: a separate narrow MD investigating this asymmetry; until
then, this MD recommends using the **buildup β** (tighter CI, larger
magnitude) for §5.B adjustment as the conservative-against-under-
correction choice. The afbouw β is reported in §5.6.1 for transparency.

---

## 9. Status + revision log

**Status**: Drafted 2026-06-14 (v1) as a framework MD per
CONVENTIONS §2.2. Adopts the v3 dose-response findings as the empirical
anchor; specifies downstream-test treatment patterns. Awaiting
adoption by individual hypothesis MDs (the v3 doc-update cascade
already references this framework from P4a, P4b, P5b, P6, P7 caveats
in [`personal_hypotheses.md`](../personal_hypotheses.md) and C4b in
[`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md)).

### Revision log

| version | date | change | source |
|---|---|---|---|
| v1 | 2026-06-14 | Initial draft as a framework MD consolidating the per-channel-quantified dose-response into downstream-test treatment guidance. Spin-off from the v3 dose-response session per the user-direction to "reason about what all the results in intervention effects descriptive + extra research mean for designing methodology and testing plans for Wiggers and personal hypotheses." Framework covers: four-phase Citalopram stratification (§3), per-channel inheritance rules (§4), three treatment patterns (§5), pre-registration template (§6), worked P5b example (§7), broader-methodology-stack implications and queued items (§8). |
| v2 | 2026-06-14 | Post-audit revision per [`reviews/methodology-citalopram_phase_stratification-2026-06-14.md`](../reviews/methodology-citalopram_phase_stratification-2026-06-14.md). Closed 2 substantive + 5 minor + 3 side fires: **I1.1 / L2.1 / L3.5** Daza 2018 counterfactual-framework anchor added to §1.3 + §5.B (covariate-adjustment is the standard observational-causal-inference move, not project-internal); **A1.2** PELT / BCP change-point detection named-and-rejected in §3 with corpus-specific reason; **I3.4** buildup-β vs afbouw-β implicit tradeoff surfaced in §5.B; **L3.1 / B5 + L4.4** "Independent obligations" block added after §6 template covering autocorrelation, §3.4 crash-drop, §3.5 spike-metrics, §3.7 detrend — framework is single-confounder fix, not comprehensive hygiene; **A1.4** optional ±N-day boundary buffer noted for §5.A; **A4.5** explicit `dose_plasma_mg(d) = 0` for pre-2024-04-09 in §3; **Side** lagged-lcera temporal-state caveat in §5.B (variants not yet in `per_day_master.csv`); **Side** numerical walkthrough on 2025-08-15 added to §7 (raw 18.3 → adjusted 5.4); **Side** hardcoded-vs-runtime annotations.yaml load note added to §3. |

### Audit hooks engaged

- [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) — descriptive layer cleared (dose-response v3 multi-channel + cross-window completed before this framework was drafted).
- [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) — four-input reasoning explicit in §1.3.
- [CONVENTIONS §3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) — §5.B's dose-adjusted predictor pattern feeds the rolling-baseline machinery a dose-corrected signal, which preserves the v3.2 `_lagged_lcera` design intent across phase boundaries (instead of forcing per-phase baselines).
- [CONVENTIONS §3.7](../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) — §5.A per-phase stratification is the §3.7 spirit applied to the Citalopram-traject sub-partition.

---

## 10. Cross-references

- **Empirical anchor**: [`citalopram_dose_response_stress_mean_sleep.md` §5.5-§5.6](citalopram_dose_response_stress_mean_sleep.md#55-v3-amendment--cross-window-corroboration-added-2026-06-14)
  — the v3 dose-response findings this framework operationalises.
- **Parent intervention-effects descriptive**: [`intervention_effects_descriptive.md` §8](intervention_effects_descriptive.md#8-findings-session-c-run-2026-06-14)
  — the Layer 1 sweep that produced the candidate.
- **Operational sibling**: [`garmin_pacing_practice.md` §7.4](garmin_pacing_practice.md#74-intervention-period-baseline-calibration--resolved-2026-06-14-across-the-autonomic-load-family)
  — the protocol-side temporal qualifier this framework's
  research-side guidance pairs with.
- **LC-phase main partition**: [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)
  — this framework adds a sub-partition for the medicated-LC era.
- **Downstream consumers (caveat sections actively reference this framework as of 2026-06-14)**:
  - [`personal_hypotheses.md`](../personal_hypotheses.md) P4a caveat 5, P4b caveat 6, P5b caveat 6, P6 caveat 5, P7 caveat 4.
  - [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) C4b caveats.
- **CONVENTIONS anchors**: [`CONVENTIONS.md`](../CONVENTIONS.md) §2.1, §2.2, §3.2, §3.7.
- **QUEUED-WORK Tier 3**: [`QUEUED-WORK.md`](../QUEUED-WORK.md#tier-3-methodological-refinement-deferred)
  — per-channel SSRI/CPAP autonomic literature (Marin 2010, Tantucci
  2003, Licht 2010, Kemp 2010, Wichniak 2017) referenced as the
  mechanistic anchor for the v3 finding; would tighten this MD's
  per-channel inheritance rules if retrieved.
