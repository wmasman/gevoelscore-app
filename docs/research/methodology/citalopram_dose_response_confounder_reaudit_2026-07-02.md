# Citalopram dose-response: slow-confounder re-audit

**Status**: producer-mode confounder re-audit (2026-07-02). Resolves the
PRIORITY flag raised in
[`confounder_exposure_triage.md` §3](confounder_exposure_triage.md) against
the slow-confounder set catalogued in
[`../analyses/longrun_rhr_trend/driver_ledger.md`](../analyses/longrun_rhr_trend/driver_ledger.md).
Skeptical independent re-audit: the task is to determine whether the three
CONFIRMED citalopram dose-response betas SURVIVE weight, deconditioning,
aging, and season, or are confounded by them.

> **GSS guardrail**: "stress" everywhere below = Garmin's HRV-derived stress
> score (GSS), NOT mental or psychological stress. The three channels under
> audit are `stress_mean_sleep` (GSS averaged over the sleep window),
> `all_day_stress_avg` (GSS averaged over the waking day), and `bb_lowest`
> (Body Battery nadir).

---

## 1. The triage concern being resolved

[`confounder_exposure_triage.md`](confounder_exposure_triage.md) flagged the
citalopram dose-response as **NEEDS-AUDIT, PRIORITY**. The stated worry: over
the medicated era, prescribed dose, continued weight gain, and the
deconditioning tail all co-trend, so the confirmed betas
(`stress_mean_sleep` +0.43/mg, `all_day_stress_avg` +0.57/mg, `bb_lowest`
-1.13/mg, per
[`citalopram_dose_response_stress_mean_sleep.md` §5.6.1](citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read))
"may partly absorb weight/fitness co-trends, just as the RHR aging term
over-absorbed."

The claim under audit (three CONFIRMED per-mg-plasma betas):

| channel | buildup post-CPAP beta/mg | HAC 95% CI | p |
|---|---:|---|---:|
| `stress_mean_sleep` | +0.43 | [+0.16, +0.70] | 0.001 |
| `all_day_stress_avg` | +0.57 | [+0.24, +0.89] | 0.000 |
| `bb_lowest` | -1.13 | [-1.78, -0.49] | 0.000 |

The load-bearing beta is the **buildup post-CPAP window** (2024-05-01 to
2024-06-19, 50 days after dropping the first 22 days for CPAP
equilibration), because it has the tightest CIs and is what §5.B locks for
downstream dose-correction. The afbouw window (2026-03-20 to 2026-06-05, 78
days) supplies the sign-concordant second half.

**Reproduction check.** The buildup betas were re-fit from
`per_day_master.csv` (via the same PK convolution and dose+time HAC model as
[`buildup_check.py`](../analyses/garmin_exploration/intervention_effects/buildup_check.py)):
`stress_mean_sleep` +0.429 [+0.156, +0.702], `all_day_stress_avg` +0.565
[+0.242, +0.888], `bb_lowest` -1.134 [-1.783, -0.486]. These match the
published values to three decimals. The audit proceeds on a faithful
reproduction, not a re-narration.

---

## 2. The five audit questions

### Q1. Estimation-window exposure: how far do the slow confounders actually move?

The betas are estimated over a **50-day buildup window** and a **78-day
afbouw window**. Slow confounders move on year scales, so the question is
how much they move inside those short windows.

**Weight** (the one genuinely-measured slow confounder). Interpolated from
the 56 weigh-ins in `userBioMetrics.json`. The decisive fact:

- Last real weigh-in before the buildup: **2023-09-12 (81.5 kg)**.
- Next real weigh-in: **2025-02-16 (84.7 kg)**.
- The entire buildup window (2024-04-09 to 2024-06-19) sits inside a
  **17-month weigh-in gap**, so buildup weight is a straight-line
  interpolation at ~0.006 kg/day.
- Interpolated weight movement over the buildup window: **+0.43 kg** (full
  72-day window) / **+0.30 kg** (the 50-day S2 estimation window).
- Interpolated weight movement over the afbouw window (bracketed by the
  2025-02-16 measured 84.7 kg and the 2026 participant-reported ~89 kg
  anchor): **+0.41 kg**.

**Deconditioning tail.** Per
[`driver_ledger.md` §2-§3](../analyses/longrun_rhr_trend/driver_ledger.md),
the deconditioning RHR rise is front-loaded into year 1 and plateaus well
before year 4 (training ceased 2022-03-17). The buildup window is in
**year 2** of the LC era; the afbouw is in **year 4**. Both windows sit on
the plateau. Deconditioning contribution over either window: **~0**.

**Aging.** Per driver_ledger, <=0.3 bpm/yr on RHR. Over 50-78 days that is
**+0.04 to +0.06 bpm** on the RHR scale. GSS and Body Battery are not RHR,
but even taking the RHR magnitude as an order-of-magnitude ceiling, this is
a rounding error over these windows.

**Season.** Deferred to Q3 (the flat-dose control is the clean seasonal
bound). Both windows are spring-to-early-summer.

**Bounding each confounder against the dose effect.** The dose effect over
the buildup swing (plasma 0 to ~30 mg) is `beta/mg * 30 mg`:
`stress_mean_sleep` +12.9, `all_day_stress_avg` +17.1, `bb_lowest` -33.9
channel-units. Using an **empirically-estimated** weight-to-channel coupling
(regress each channel on interpolated weight over the full corpus with a
linear time control; the driver_ledger only gives weight -> RHR, not
weight -> GSS/BB, so the coupling is estimated here):

| channel | est. beta_weight (units/kg) | weight move over buildup | weight contribution | dose effect | weight as % of dose |
|---|---:|---:|---:|---:|---:|
| `stress_mean_sleep` | +0.20 | +0.30 kg | +0.06 | +12.9 | 0.5% |
| `all_day_stress_avg` | +0.48 | +0.30 kg | +0.14 | +17.1 | 0.8% |
| `bb_lowest` | -0.15 | +0.30 kg | -0.04 | -33.9 | 0.1% |

**Read.** Every slow confounder's movement over the estimation window is
negligible against the dose effect: weight contributes under 1% of the dose
effect on all three channels; deconditioning is ~0; aging is a rounding
error. The confounders simply do not move enough inside a 50-78 day window
to fake a +12.9 / +17.1 / -33.9 channel swing. **The slow confounders are
negligible against the dose effect over the estimation windows.**

### Q2. Sign-concordance: can a monotonic slow confounder or season produce sign-concordant per-mg betas across a dose-up and a dose-down window?

The betas are **per mg of plasma citalopram**, and they are sign-concordant:
positive on the GSS channels and negative on `bb_lowest` in BOTH the buildup
(dose UP) and afbouw (dose DOWN) windows.

The geometry: because the regressor is plasma mg, a same-sign per-mg beta in
both phases means the CHANNEL moves in OPPOSITE directions in the two
windows (buildup GSS goes up as dose rises; afbouw GSS comes down as dose
falls):

| channel | buildup channel move (dose UP) | afbouw channel move (dose DOWN) |
|---|---:|---:|
| `stress_mean_sleep` | +12.9 | -5.4 |
| `all_day_stress_avg` | +16.9 | -4.6 |
| `bb_lowest` | -34.0 | +12.9 |

Now consider a monotonic slow confounder (weight up, aging up,
deconditioning up) or a common seasonal shape. Both windows are
spring-to-summer, so **season and the monotonic confounders trend the SAME
direction in both windows**. Dose, however, moves UP in buildup and DOWN in
afbouw. A confounder aliased into `beta_dose` would therefore be divided by a
positive dose-change in one window and a negative dose-change in the other,
yielding **opposite-sign** per-mg betas across the two phases. The observed
betas are the SAME sign in both phases. A common monotonic confounder or a
common seasonal shape **cannot** produce that pattern.

The fact that both windows are spring-to-summer does NOT cancel this; it
strengthens it. If season were the driver, the SAME seasonal rise in both
springs against opposite dose directions would give opposite-sign betas. It
does not. **Sign-concordance rules out season and any common monotonic
slow-confounder as the source of the betas.** (The flat-dose control in Q3
closes the residual "spring itself" loophole directly.)

### Q3. Flat-dose control: would weight/deconditioning/aging still trend during a flat-dose window?

The spring-2025 control window has flat dose (30 mg consolidation
throughout) at the SAME calendar slot. If weight/deconditioning/aging/season
were driving the GSS and BB channels, they would STILL trend during this
flat-dose window, because none of those confounders are switched off by the
dose being constant. The flat-dose `beta_time` is therefore a **direct upper
bound on the total non-dose calendar-time movement** (weight + season +
deconditioning-tail + aging combined).

Reproduced from `per_day_master.csv`, buildup-calendar-aligned window
(2025-04-09 to 2025-06-19, matching
[`buildup_check.py`](../analyses/garmin_exploration/intervention_effects/buildup_check.py)
S3):

| channel | flat-dose beta_time/day | 95% CI | window-span (non-dose move) | dose effect (buildup) |
|---|---:|---|---:|---:|
| `stress_mean_sleep` | -0.023 | [-0.064, +0.019] | -1.6 | +12.9 |
| `all_day_stress_avg` | -0.001 | [-0.041, +0.039] | -0.1 | +17.1 |
| `bb_lowest` | -0.061 | [-0.132, +0.010] | -4.3 | -33.9 |

(These reproduce the MD's reported spring-2025 `beta_time` of -0.023 /
-0.001 / -0.061 exactly. An afbouw-calendar-aligned 2025 window gives a
larger `bb_lowest` slope of -0.134/day / -10.3 span; even at that pessimistic
end it is under a third of the dose-driven move, and its CI does not
approach the dose effect.)

**Read.** During a flat-dose window at the same calendar slot, with weight,
deconditioning-tail, aging, and season all still present, the total
calendar-time movement is small (GSS channels essentially flat; `bb_lowest`
worst-case -4 to -10 units of drift) and its CI brushes or contains zero on
the GSS channels. This bounds the combined slow-confounder + season
contribution well below the dose-driven move (+12.9 / +17.1 / -33.9).
**The flat-dose control empirically bounds the slow-confounder contribution
to a small fraction of the dose effect, and it does so on the same channels
whose dose betas are confirmed.**

### Q4. Empirical re-fit: does the dose beta survive an interpolated-weight term (and/or a time term)?

The published buildup model is already `channel ~ const + dose + time`, so
it already contains a linear time covariate. I re-fit three specs over the
50-day S2 window:

- **A (published)**: `channel ~ const + dose + time`
- **B (audit)**: `channel ~ const + dose + time + weight_interp`
- **C (audit)**: `channel ~ const + dose + weight_interp` (drop time)

| channel | A beta_dose | B beta_dose (+weight) | C beta_dose (weight, no time) |
|---|---:|---:|---:|
| `stress_mean_sleep` | +0.429 [+0.156, +0.702] | +0.429 [+0.156, +0.702] | +0.429 [+0.156, +0.702] |
| `all_day_stress_avg` | +0.565 [+0.242, +0.888] | +0.565 [+0.242, +0.888] | +0.565 [+0.242, +0.888] |
| `bb_lowest` | -1.134 [-1.783, -0.486] | -1.134 [-1.783, -0.486] | -1.134 [-1.783, -0.486] |

The dose beta is **unchanged to three decimals** whether interpolated weight
is added or not, and whether time is present or not. The dose survives.

**The honest collinearity caveat (as instructed).** Over the buildup window,
interpolated weight is an almost-perfectly-straight line (it is interpolated
between the 2023-09 and 2025-02 anchors that bracket the whole window), so it
is nearly collinear with the linear `time` covariate. Measured directly:
`corr(dose, time) = +0.638` and `corr(dose, weight) = +0.638` are IDENTICAL,
because over this window interpolated-weight IS a linear function of time.
Consequently the weight term carries no information the `time` term did not
already carry, which is exactly why adding it moves nothing. This is not
weak evidence that weight is harmless; it is the strong structural point:
**the published model's `time` covariate already absorbs the entire
monotonic slow-confounder bundle (weight + deconditioning-tail + aging),
because all of them are monotonic-linear over these short windows and hence
collinear with time.** The dose beta is what is left AFTER that bundle is
removed. The dose and time are themselves only partially collinear
(corr +0.64, not +1.0) because the PK-smoothed dose is a curved staircase,
not a straight ramp; that curvature is what lets the regression identify the
dose beta separately from the linear time/weight/aging trend. Weight is
therefore not separately identifiable from time here, and I do not
over-interpret the weight coefficient itself (spec C's implied
+1.97/+8.58/-4.99 per-kg is an artefact of weight standing in for the whole
time trend). The load-bearing result is that dose is unmoved.

### Q5. The honest residual: does removing only dose leave the other slow confounders uncorrected in a long-horizon claim?

Yes, and this must be stated cleanly. There are two different claims and
they have different confounder status:

1. **"The dose BETA is sound."** SURVIVES. Estimated over 50-78 day windows
   where the slow confounders barely move (Q1), sign-concordant in a way a
   monotonic/seasonal confounder cannot fake (Q2), bounded by a flat-dose
   same-slot control (Q3), and unmoved by an explicit weight term (Q4). The
   short windows are what neutralise the slow confounders.

2. **"The dose-corrected channel is clean of all confounders over the full
   era."** NOT established, and the §5.B correction does not claim it. The
   §5.B correction is `channel_adj(d) = channel(d) - beta_dose *
   dose_plasma_mg(d)`, applied over the WHOLE consolidation era. It removes
   ONLY the dose component. Over the full 2022-2026 era, weight rose ~74 to
   ~89 kg (~15 kg), the deconditioning tail resolved over year 1, and aging
   accrued ~4 years. Those confounders are still in `channel_adj`. So any
   LONG-HORIZON claim that consumes the dose-corrected channel (a cross-era
   absolute-level contrast, a multi-year drift attribution) inherits the
   UNCORRECTED weight + deconditioning-tail + aging drift. `channel_adj` is
   dose-clean, not confounder-clean.

The distinction is the whole audit in one line: the confounders are
negligible over the 50-78 day ESTIMATION windows (so the beta is sound), but
they are NOT negligible over the multi-year era where `channel_adj` is
consumed (so a long-horizon claim on `channel_adj` still owes the other slow
confounders their own correction). This is the same lesson the RHR work
learned: short lagged-baseline tests are immune; long absolute-level claims
are exposed.

---

## 3. Verdict

**STANDS-WITH-CAVEAT.**

The three CONFIRMED citalopram dose-response betas (`stress_mean_sleep`
+0.43/mg, `all_day_stress_avg` +0.57/mg, `bb_lowest` -1.13/mg) **survive the
slow confounders**. The dose-response finding is not confounded by weight,
deconditioning, aging, or season.

**What specifically neutralises the confound** (short windows + controls):

- **Short estimation windows.** The betas live in a 50-day buildup window
  and a 78-day afbouw window. Interpolated weight moves only +0.30 kg
  (buildup) / +0.41 kg (afbouw); deconditioning is ~0 (both windows are past
  the year-1 plateau); aging is a rounding error. Each contributes under 1%
  of the dose effect (Q1).
- **Sign-concordance** across a dose-up and a dose-down window rules out any
  common monotonic or seasonal confounder, which would give opposite-sign
  per-mg betas (Q2).
- **The flat-dose spring-2025 same-slot control** directly bounds the total
  non-dose calendar movement to a small fraction of the dose effect, on the
  same channels (Q3).
- **The explicit re-fit** with an interpolated-weight term leaves the dose
  beta unchanged to three decimals; the published `time` covariate already
  absorbs the monotonic slow-confounder bundle (Q4).

**The CAVEAT** (Q5): this verdict is about the dose BETA and the SHORT
estimation windows. It does NOT certify the §5.B dose-corrected channel as
clean of all confounders over the FULL era. Removing only the dose component
leaves weight (~15 kg over the era), the deconditioning tail, and aging
uncorrected in `channel_adj`. Any long-horizon or cross-era claim that
consumes `channel_adj` must still correct those slow confounders separately.
The beta is robust; the corrected channel is dose-clean, not
confounder-clean.

---

## 4. Recommended triage update

Update [`confounder_exposure_triage.md` §3](confounder_exposure_triage.md):
move the **citalopram dose-response (the BETA)** from NEEDS-AUDIT to
**audited-robust** against the slow-confounder set, with this file as the
evidence. Rationale: the betas are estimated over 50-78 day windows where the
slow confounders are negligible, and they survive an explicit weight re-fit,
a flat-dose control, and the sign-concordance test.

Do NOT close the whole line item. Add a residual sub-flag:
**any LONG-HORIZON / cross-era claim that consumes the §5.B dose-corrected
channel (`channel_adj`) remains NEEDS-AUDIT for the OTHER slow confounders
(weight, deconditioning-tail, aging), which the dose-only correction does not
remove.** That residual is the same class the RHR long-run work belongs to,
and it should be audited when and where such a claim is actually made, not
pre-emptively.

Net: the citalopram dose-response BETA is escalated OUT of the priority
audit queue (robust); the dose-corrected-channel-over-the-full-era usage is
left as a scoped residual flag for the consumer of `channel_adj`.

---

## 5. Named counts (CONVENTIONS §3.6)

- 56 weigh-ins (raw weight entries, `userBioMetrics.json`, nested
  `weight.weight` grams, 2021-08-13 to 2025-02-16).
- 0 weigh-ins (raw weight entries, `userBioMetrics.json`, inside the buildup
  window 2024-04-09 <= date <= 2024-06-19; the window sits in a 17-month
  measured-weight gap 2023-09-12 to 2025-02-16, weight interpolated).
- 50 analytical days (`stress_mean_sleep` non-null, `per_day_master.csv`,
  buildup S2 window 2024-05-01 <= date <= 2024-06-19).
- 78 analytical days (`stress_mean_sleep` non-null, `per_day_master.csv`,
  spring-2025 flat-dose control 2025-03-20 <= date <= 2025-06-05;
  72 days for the buildup-calendar-aligned 2025-04-09 to 2025-06-19 variant).
- 3 channels CONFIRMED (`stress_mean_sleep`, `all_day_stress_avg`,
  `bb_lowest`; the audit target set).

---

## 6. Cross-references

- [`confounder_exposure_triage.md`](confounder_exposure_triage.md) : the
  PRIORITY flag this file resolves (§3 NEEDS-AUDIT list; §4 recommended
  action).
- [`citalopram_dose_response_stress_mean_sleep.md` §5.5-§5.6](citalopram_dose_response_stress_mean_sleep.md#55-v3-amendment--cross-window-corroboration-added-2026-06-14)
  : the confirmed betas + cross-window controls under audit.
- [`citalopram_phase_stratification.md` §5.B](citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests)
  : the `channel_adj = channel - beta_dose * dose_plasma_mg` correction
  whose long-horizon residual is scoped in Q5.
- [`../analyses/longrun_rhr_trend/driver_ledger.md`](../analyses/longrun_rhr_trend/driver_ledger.md)
  : the slow-confounder set and magnitudes (weight ~0.32 bpm/kg on RHR,
  deconditioning plateau by year 1, aging <=0.3 bpm/yr).
- [`../analyses/garmin_exploration/intervention_effects/buildup_check.py`](../analyses/garmin_exploration/intervention_effects/buildup_check.py),
  [`dose_response.py`](../analyses/garmin_exploration/intervention_effects/dose_response.py)
  : the fitting scripts reproduced for this audit.

---

**Authorship**: Claude (Opus 4.8) producer-mode confounder re-audit, for the
participant-researcher (repo owner).
