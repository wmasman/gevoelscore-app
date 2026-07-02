# Handoff back to the site: R23 (COVID check) + R12 (deconditioning leg)

**Status**: Stage-T (translation-to-audience) handoff from the research team
back to the site (`wiggers_research_story`). Reports what was found for two
register requests and, critically, **how to present it honestly**. Drafted
2026-07-02 by Claude (Opus 4.8), producer-mode, for the participant-researcher
(repo owner). Everything below is aggregated / date-free and privacy-safe.

Answers: [`research-requests.md`](../../../wiggers_research_story/site/docs/research-requests.md)
R23 (COVID known-event check), the **deconditioning leg of R12**
(structurally-different-body inferential test), and feeds R15 (driver ledger)
and R17 (measurement regime).

---

## 1. R23 - did the watch catch the COVID infection? YES (with one honest nuance)

**Deliverable:** the pre-registered peri-event test ran. Verdict **MOVED**:
the overnight autonomic factor (anchor `stress_mean_sleep`) sat at the
high-autonomic-load pole during the 14-day COVID window, at the **99.2nd
percentile** of the ordinary-fortnight null (one-sided p-analogue **0.0077**,
effect ~0.86 SD). This is the external corroboration `three-things` / Link 1
promised: the watch's factor moved for an independently-known event.

**How to present it (honest nuance the copy must carry):** the move is
**partial-coherence**, not a clean 3-for-3. Of the three factor channels,
`stress_mean_sleep` (up) and `bb_highest` (down) moved as predicted, but
**`resting_hr` did not rise on the raw scale** - it only rose after removing a
pre-illness downward trend. That is **explained, not a failure** (see §2): the
participant was at his athletic resting-HR floor right before COVID, which
masks an infection rise on the raw scale. Suggested framing: *"the watch's
overnight autonomic factor moved significantly during the infection (external
corroboration), carried by the stress and body-battery channels; resting heart
rate was masked by the participant's peak fitness at the time."*

**Caveat for the copy:** n=1, single event; the window abuts LC onset
(2022-04-04), so this is *"the factor departed baseline around the infection /
LC-onset hinge,"* never *"the infection caused it."* A clean MOVED softens
nothing that was over-promised; it delivers Link 1's lightest-leaned-on check.

Note: the register's R23 source line cites `cohort_topology/findings.md` for
the factor definition. That was a register error, corrected during the work:
the factor is the cross-channel autonomic-state cluster
(`analyses/garmin_exploration/cards/cross-channel-correlation.md`), not the
recovery-topology work. Please use the corrected source.

## 2. R12 deconditioning leg - can we separate "lost fitness" from Long COVID?

R12 asks whether the healthy-to-LC body change survives controlling for
**deconditioning** (among other confounds). We investigated the resting-HR
arc directly. The honest answer has two halves:

**(a) Direction: deconditioning does NOT dominate the multi-year RHR rise.**
This is ROBUST. Resting HR rises through the whole LC period and is still
rising at year 4 (recent slope ~1.6 bpm/yr), which is the OPPOSITE of the
deconditioning shape (fitness loss is front-loaded and plateaus by ~year 1).
We tested this adversarially: even a physiologically-unjustified
never-plateauing deconditioning curve cannot absorb the rise, and aging is
bounded to a minor role (resting-HR aging is ~0 to at most 0.3 bpm/yr in this
age band). So the rise is **not just deconditioning**.

**(b) Magnitude: the Long-COVID residual is SUGGESTIVE, not established.**
After modelling out deconditioning, weight, citalopram, seasonality, and
aging, a residual RHR rise of ~+1.2 bpm/yr remains post-2023 - but its
confidence interval is wide (**~[0.6, 1.9] bpm/yr**) and its significance is
**fragile**: dropping a single year (2024) makes it cross zero, and it is
sensitive to the (sparsely measured) weight trajectory. So we **cannot put a
clean number on the LC part**.

**How to present it (this is the load-bearing honesty for R12):** the
"structurally different body" claim is supported **in direction** but **not
cleanly quantified**. Suggested framing: *"the rise isn't just lost fitness -
deconditioning finishes in the first year, and the body kept drifting after
that - but with one person and a few years of data, we can't put a precise
number on the Long-COVID part."* Do NOT ship a single headline bpm figure as
if it were solid. And note: **resting HR is normal in absolute terms** (~61
bpm) - the signal is entirely in the trend-shape, not in an abnormal value, so
avoid any "alarmingly high heart rate" framing.

## 3. Driver-ledger updates (feeds R15 / `data/drivers.json`)

| Driver | Prior status | New status + one-line finding |
|---|---|---|
| **fitness / deconditioning** | `un-examined` | **examined, bounded**: does not dominate the RHR trend (front-loaded, plateaus ~year 1); the residual is not explained by it. Fitness DECLINE is modelled, not measured (last real run 2022-03; VO2Max after that is Garmin's decay estimate). |
| **weight** | (implicit) | **bounded, measured**: 56 real weigh-ins, ~74 kg athlete to 89 kg now; RHR effect ~0.32 bpm/kg (matches literature). A real slow driver, sparsely sampled (14-month gap over LC onset). |
| **aging** | (implicit) | **bounded, minor**: resting-HR aging ~0 to <=0.3 bpm/yr at age 40-45; too small to explain the trend. |
| **measurement-regime** (R17) | artifact-candidate | **device unchanged throughout** (same Forerunner 245), so no device step; VO2Max real-run-fed only through 2022-03. |
| **citalopram** | confirmed dose-response | RHR effect in-sample ~-1.1 bpm at 30 mg (DOWN, as literature predicts); it MASKS an LC elevation. See §4. |

## 4. One flag for the research backlog (not the site): re-audit the citalopram dose-response

The confirmed citalopram dose-response (R16/R20; stress + `bb_lowest`) has the
**same collinearity structure** we just uncovered for RHR: over 2024+, dose,
continued weight gain, and the deconditioning tail all co-trend. So the
confirmed betas may partly absorb weight/fitness co-trends. This does not
change what the site ships now, but the dose-response should be re-audited
against the confounder set before it is leaned on harder. See
[`methodology/confounder_exposure_triage.md`](methodology/confounder_exposure_triage.md).
Reassuringly, the **crash-precursor scorecard signals do NOT need re-testing**
(they use short-horizon lagged baselines, demonstrated ~98% immune to the slow
confounders), so this is a targeted flag, not a site-wide caveat.

## 5. Sources (research-side, for the /workings and /reading layers)

- R23: [`analyses/hypotheses/peri-event-covid/`](analyses/hypotheses/peri-event-covid/)
  (pre-registration, test, result + the §12 follow-up annotation).
- R12 deconditioning leg: [`analyses/longrun_rhr_trend/`](analyses/longrun_rhr_trend/)
  (driver ledger, decomposition, findings) and its skeptical review
  [`reviews/longrun-rhr-decomposition-2026-07-02.md`](reviews/longrun-rhr-decomposition-2026-07-02.md).
- Literature (for `/reading`): training-bradycardia / detraining, deconditioning-vs-disease,
  long-term RHR confounder catalog, resting-HR aging magnitude, acute-viral-infection
  autonomic signature - all in [`literature/reviews/`](literature/reviews/).
