# RHR long-term-trend driver ledger

**Status**: design artefact (Stage-D planning), open inputs RESOLVED
2026-07-02. The literature-gated, a-priori confounder set for the
multi-year resting-HR (RHR) trend decomposition. This ledger enumerates
every candidate long-term driver of RHR, records whether the literature
supports it, whether the project data can measure or proxy it, and how it
enters the model. It is assembled **before** the long-term RHR trajectory
is characterised, so the confounder set is literature-determined, not
fitted to the curve. Drafted 2026-07-02 by Claude (Opus 4.8) under
producer-mode authorization, for the participant-researcher (repo owner).

> ## Scope + discipline
>
> This is a **design / planning** artefact, not an inference. It commits
> the confounder set and the model form **before** the RHR outcome trend
> is examined. No long-term RHR trend, slope, or LC-vs-baseline contrast
> is computed or inspected here. The data facts used below are
> **driver / confounder measurability checks** (weight, VO2Max, device),
> NOT any RHR value. "Stress" anywhere in this project = Garmin's
> HRV-derived stress score (GSS), NOT mental stress; item 8 below is a
> DIFFERENT construct (real psychological stress as an RHR confounder) and
> is labelled as such.

## 1. Purpose

The participant was a heavily-training endurance athlete until an acute
COVID infection (2022-03) after which training essentially ceased and
Long COVID (LC) began (LC onset 2022-04-04). Over the ~4 years since, the
wearable RHR has drifted. The hypothesis under investigation: a large part
of that multi-year drift may be **deconditioning** (loss of the athletic
base) plus other **literature-supported confounders**, not LC disease per
se. The goal is to **model out** every literature-supported long-term RHR
driver and inspect the **LC-attributable residual**, with the collinearity
limits stated up front.

## 2. The literature-gated confounder set (open inputs resolved)

Sourced from three external reviews (each reads no project data):
- [`../../literature/reviews/training_bradycardia_detraining_rhr_review.md`](../../literature/reviews/training_bradycardia_detraining_rhr_review.md)
- [`../../literature/reviews/deconditioning_vs_disease_longrun_rhr_review.md`](../../literature/reviews/deconditioning_vs_disease_longrun_rhr_review.md)
- [`../../literature/reviews/longterm_rhr_confounders_catalog_review.md`](../../literature/reviews/longterm_rhr_confounders_catalog_review.md)

Measurability reflects checks of `per_day_master.csv` and the Garmin GDPR
dump (`DI_CONNECT/DI-Connect-Wellness/*bioMetrics*`) on 2026-07-02.

| # | Driver | Lit rating | Direction / magnitude / timescale | Project-data handle | Model term | Status |
|---|---|---|---|---|---|---|
| 1 | **Deconditioning / fitness loss** | STRONG (primary confounder) | RHR **UP** ~5-12 bpm; biphasic, front-loaded into **year 1**, plateau well before year 4 | **MEASURED: Garmin VO2Max series, 302 pts 2021-08 to 2026-05** (peak ~52 early-2022, ~42 by 2023, 37 by 2026); cessation 2022-03 | **VO2Max regressor** (measured fitness anchor), replaces the literature-only curve | **measured** (post-cessation estimation caveat, §5) |
| 2 | **Citalopram** | STRONG (step) | RHR **DOWN** up to ~8 bpm (Rasmussen 1999), OPPOSITE to LC elevation so it MASKS the signal; persistent step | **`dose_plasma_mg`** + `in_citalopram_traject` (788 days), full coverage | **change-point / dose term** at initiation, not a slope | measurable (in-sample RHR beta to estimate; lit prior -8 bpm) |
| 3 | **Body weight / adiposity / BMI** | STRONG (trend) | RHR UP ~0.3 bpm/BMI unit; participant reports **large gradual gain to 89 kg / 1.83 m (BMI 26.6)**, athlete baseline lower | **NO Garmin trajectory** (weight null in biometrics; single stale 84.7 kg). Partly captured by VO2Max-per-kg | **folded into the VO2Max term** (per-kg VO2Max integrates weight gain) | resolved: unmeasured-as-trajectory, collinear (see §5) |
| 4 | **Device / firmware change** | STRONG (artefact step) | spurious step/drift in the estimate | **same Forerunner 245 throughout** (participant-confirmed; single-device dump) | none needed | **resolved: no device step** |
| 5 | **Changing cardioactive exposure** (beta-blocker, thyroid med, smoking) | STRONG **IF** it changes | large step | participant reports **none** (occasional painkillers only; non-smoker) | none | **resolved: absent** |
| 6 | **Changing clinical state** (thyroid, anemia/iron) | STRONG but episodic | ~10-20 bpm if present | participant reports **no diagnoses/treatments** | none | **resolved: absent** |
| 7 | **Seasonality / ambient temperature** | CYCLIC (not trend) | ~2 bpm, min ~July / max ~January | **`date`** (derive day-of-year) | annual **phase** term, not a trend | measurable |
| 8 | **Chronic psychological / life stress** (REAL psych stress, NOT the Garmin stress score) | WEAK / conditional | modest, uncertain | no direct handle (notes/annotations only) | not a trend term; noted | weak, not-to-inflate |
| 9 | **Aging** | WEAK over 4 y | small per decade | **birth year 1981** (age ~40 to ~45 over the window) | small linear age slope | **resolved: include (small)** |
| 10 | **Menstrual cycle** | CYCLIC, sex-dependent | ~2-4 bpm | **male** (participant-confirmed) | N/A | **resolved: dropped** |
| 11 | **Alcohol** | WEAK / conditional | modest unless large change | none | not modelled unless a large change is reported | weak, not-to-inflate |
| 12 | **Habitual caffeine / nicotine** | WEAK | modest | none | not modelled | weak, not-to-inflate |
| 13 | **Non-exercise activity (steps / NEAT)** | WEAK / conditional | modest | steps + activity columns present | optional covariate | measurable, low priority |

## 3. The key discriminator (from the deconditioning-vs-disease review)

On a **static** RHR value, deconditioning and LC disease are **not
separable** (both raise RHR, and they co-occur and reinforce). Leverage
comes **only** from trajectory **shape and timing**:

- A **pure-deconditioning** RHR rise is front-loaded into year 1 and
  **plateaus well before year 4**. So any RHR movement **still ongoing at
  year 3-4**, or any **episodic / provocation-linked** structure, is
  **NOT deconditioning** (it is LC-disease or aging).
- The measured VO2Max series lets us test this directly: VO2Max fell fast
  in year 1 (52 to ~42) then declined slowly (42 to 37, 2023 to 2026). If
  RHR tracks VO2Max, its rise should likewise be front-loaded; RHR
  movement decoupled from the (near-flat, slowly-declining) later VO2Max
  is the LC/aging candidate.
- The decomposition has leverage on the **post-year-1 drift and the
  episodic component**, and **no** leverage on the **static level** of the
  year-4 plateau (deconditioning + weight + LC-baseline + aging all raise
  it and cannot be apportioned from RHR alone).

## 4. Proposed decomposition (model form, for approval)

```
RHR(t) = f_fitness( VO2Max(t) )          # drivers 1 + 3 combined: measured per-kg fitness
       + citalopram_term(t; dose_plasma_mg)   # driver 2, step/dose (DOWN, masks LC)
       + seasonal_phase(t)                     # driver 7, cyclic (day-of-year)
       + aging_slope(t; birthyear=1981)        # driver 9, small
       + LC_residual(t)                        # the signal
       + noise
```

Drivers 4, 5, 6, 10 are resolved absent/N/A and drop out. Drivers 8, 11,
12, 13 are literature-weak and not modelled as trend terms (13 optional).

- The **LC-attributable residual** = observed RHR minus the measured
  fitness term, the citalopram term, the seasonal phase, and the age
  slope.
- **Read the residual for**: (a) drift persisting past year ~1-2 beyond
  the VO2Max fast-drop / plateau; (b) episodic structure aligned to
  crashes / recoveries; (c) the citalopram-era behaviour once its step is
  removed (recalling citalopram MASKS an LC elevation).
- **Falsification of the deconditioning-dominant hypothesis**: if RHR
  keeps rising materially **after VO2Max has stopped falling fast** (post
  year 1-2), or shows structured episodic residual, deconditioning does
  NOT dominate and the residual carries a real LC/aging component.
  Conversely, if RHR is fully absorbed by the fitness + confounder terms
  (flat residual), the long-run RHR drift is largely nuisance.

## 5. Collinearity + measurement limits (stated before any fit)

- **VO2Max entangles fitness and weight.** Garmin VO2Max is per-kg, so the
  reported weight gain (to BMI 26.6) mechanically lowers it. Using VO2Max
  as the fitness regressor therefore **folds deconditioning and adiposity
  into one measured term** (drivers 1 + 3). This is a feature for
  isolating the LC residual, but it means the model **cannot separate
  "lost cardiorespiratory fitness" from "gained weight"** as distinct RHR
  causes; they enter as one cardiometabolic-fitness axis.
- **Post-cessation VO2Max reliability.** Garmin estimates VO2Max from
  runs with HR + GPS. With training largely ceased post-2022, later VO2Max
  values may rest on sparse or degraded input and may lag or freeze. The
  VO2Max anchor is the best available direct fitness signal but is not a
  gold-standard lab measure; sensitivity to its later-period reliability
  must be reported.
- **Slow-driver collinearity.** Deconditioning/weight (via VO2Max),
  LC-baseline shift, and aging are all slow and monotonic over the same
  window: their slow components are collinear and the model **cannot
  uniquely apportion the static drift** among them. Only the shape/timing
  (front-loading vs post-year-1 persistence) and the episodic part are
  identifiable.
- **No measured weight trajectory.** Weight is absent from the dump as a
  series (single stale value). Its effect is carried only indirectly
  through per-kg VO2Max; a standalone weight covariate is not available.
- n=1. Every attribution is "consistent with", never proof.

## 6. Open inputs (RESOLVED 2026-07-02)

| # | Question | Resolution |
|---|---|---|
| 1 | Weight record / change | Large gradual gain to **89 kg / 1.83 m (BMI 26.6)**; **no Garmin trajectory** (only a stale 84.7 kg); carried via per-kg VO2Max |
| 2 | Device change | **Same Forerunner 245 throughout**; no device step |
| 3 | Beta-blocker / thyroid med / smoking | **None** (occasional painkillers only; non-smoker) |
| 4 | Thyroid / anemia diagnosis or treatment | **None** |
| 5 | Birth year (aging term) | **1981** (age ~40 to ~45 over the window) |
| 6 | Sex (menstrual term) | **Male**; menstrual term dropped |

## 7. Cross-references

- The three literature reviews (§2).
- [`../garmin_exploration/cards/driver-ledger.md`](../garmin_exploration/cards/driver-ledger.md)
  — the existing project driver ledger (R15/R16/R20); reconcile the
  citalopram term with its confirmed dose-response.
- [`../descriptive/training_load_coverage/precondition.md`](../descriptive/training_load_coverage/precondition.md)
  — training-cessation coverage (fitness-term anchor).
- [`../hypotheses/peri-event-covid/result.md`](../hypotheses/peri-event-covid/result.md)
  — the R23 result that motivated this thread (raw RHR equivocation).
- Garmin VO2Max source: `DI_CONNECT/DI-Connect-Wellness/97794221_userBioMetrics.json`
  (302 non-null `vo2MaxRunning`); weight null therein.
