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
| 1 | **Deconditioning / fitness loss** | STRONG (primary confounder) | RHR **UP** ~5-12 bpm; biphasic, front-loaded into **year 1**, plateau well before year 4 | **peak MEASURED only**: real training runs end **2022-03-17** (brief failed 4-run comeback Jun-Jul 2023, none since); VO2Max ~52 at peak. The 52 to 37 decline is **Garmin's inactivity-DECAY MODEL**, not measured (no runs feed it post-2022) | **model curve** anchored at 2022-03 cessation, run as a **sensitivity pair** (literature curve primary; Garmin VO2Max-decay as secondary) | **model-based** (only the peak is measured; §5) |
| 2 | **Citalopram** | STRONG (step) | RHR **DOWN** up to ~8 bpm (Rasmussen 1999), OPPOSITE to LC elevation so it MASKS the signal; persistent step | **`dose_plasma_mg`** + `in_citalopram_traject` (788 days), full coverage | **change-point / dose term** at initiation, not a slope | measurable (in-sample RHR beta to estimate; lit prior -8 bpm) |
| 3 | **Body weight / adiposity / BMI** | STRONG (trend) | RHR UP ~0.3 bpm/BMI unit; **74 kg athlete (2021-22) to ~82 (mid-2023) to 84.7 (2025) to 89 (2026)**, BMI 21.8 to 26.6 | **MEASURED: 56 weigh-ins** in `userBioMetrics.json` (nested `weight` objects); dense 2021-08 to 2022-04, then a **14-month gap** to 2023-06, then sparse | **separate interpolated weight regressor** (see per-kg double-count note, §5) | resolved: measured-but-sparse, LC-onset gap |
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
- Both deconditioning curves (literature + Garmin decay) agree the fitness
  contribution is front-loaded and plateaus by ~year 1, so if RHR tracks
  fitness its rise is front-loaded too; RHR movement after the ~year-1
  plateau is the LC/aging candidate. (The Garmin VO2Max decline 52 to 37
  is that decay model, not a measured fitness trajectory: runs ended
  2022-03.)
- The decomposition has leverage on the **post-year-1 drift and the
  episodic component**, and **no** leverage on the **static level** of the
  year-4 plateau (deconditioning + weight + LC-baseline + aging all raise
  it and cannot be apportioned from RHR alone).

## 4. Proposed decomposition (model form, for approval)

```
RHR(t) = decond_curve(t; cessation=2022-03) # driver 1: MODEL curve (lit primary / Garmin-decay sensitivity), plateau ~yr1
       + b_weight * weight_interp(t)          # driver 3: MEASURED weigh-ins (sparse), interpolated over the gap
       + citalopram_term(t; dose_plasma_mg)   # driver 2, step/dose (DOWN, masks LC)
       + seasonal_phase(t)                     # driver 7, cyclic (day-of-year)
       + aging_slope(t; birthyear=1981)        # driver 9, small
       + LC_residual(t)                        # the signal
       + noise
```

**Deconditioning is a MODEL curve, not measured (design lock).** Real
running fitness data ends at 2022-03 (last training run 2022-03-17); the
VO2Max decline after that is Garmin's inactivity-decay model. So the
fitness term is a **shape prior anchored at cessation**, run as a
**sensitivity pair**: the **literature deconditioning curve** (primary,
weight-independent) and the **Garmin VO2Max-decay curve** (secondary).
Note the Garmin curve is per-kg so it partially re-encodes weight; if used
alongside the separate weight term it mildly double-counts weight, which is
why the literature curve is primary. Both curves agree on the load-bearing
point: **plateau by ~year 1**, so post-year-1 residual is not fitness.
Weight (driver 3) is the one genuinely-**measured** slow confounder and
enters as its own term.

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

- **The fitness DECLINE is modelled, not measured.** Real running fitness
  data ends 2022-03; VO2Max after that is Garmin's decay model, so we have
  a measured PEAK only, not a measured decline. The deconditioning term is
  therefore a model curve either way (§4 sensitivity pair). This is the
  main honest downgrade from an earlier framing that treated VO2Max as a
  measured fitness anchor.
- **The three slow drivers pile into 2022-2023 together.** The weight gain
  (74 to ~82 kg), the VO2Max fast-drop (52 to ~42), and LC onset all fall
  in the same 2022-04 to 2023-06 window, and the weight series has **no
  weigh-ins in exactly that window** (interpolated straight-line). So the
  early rise is where fitness, weight, and LC are MOST collinear and least
  separable; the post-2023 behaviour (VO2Max near-flat, weight sparse) is
  where the residual has more leverage.
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
- **Weight measured but sparse.** 56 weigh-ins, dense 2021-08 to 2022-04
  then a 14-month gap over LC onset then sparse (last 2025-02); the 2026
  value (89 kg) is participant-reported, not in the dump. Interpolation
  over the gap is an assumption.
- n=1. Every attribution is "consistent with", never proof.

## 6. Open inputs (RESOLVED 2026-07-02)

| # | Question | Resolution |
|---|---|---|
| 1 | Weight record / change | **MEASURED: 56 weigh-ins** in `userBioMetrics.json` (nested `weight` objects; an earlier scan missed them). 74 kg athlete (2021-22) to ~82 (mid-2023) to 84.7 (2025) to 89 (2026, participant-reported). Dense early, 14-month gap over LC onset, then sparse. Enters as a separate interpolated regressor |
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
- Garmin fitness + weight source: `DI_CONNECT/DI-Connect-Wellness/97794221_userBioMetrics.json`
  (302 non-null `vo2MaxRunning`, but real-run-fed only through 2022-03;
  **56 `weight` weigh-ins nested as `{weight, sourceType, timestampGMT}`
  objects**, easy to miss with a scalar scan). Run counts from
  `processed/garmin/activities.csv` (last training run 2022-03-17).
