# Testable hypotheses from the Wiggers smartwatch-pacing handleiding

*For n-of-1 validation against Willem's multi-year Garmin + gevoelscore dataset (with labelled dip and crash episodes).*

---

## How to read this

The handleiding is a collection of *lotgenoten* observations and n-of-1 generalisations. Treat every line below as a **hypothesis to test against your own data**, not as an established fact. Several of them directly contradict, or sharpen, things you've already found — those are the high-value ones, flagged with ⚠️.

**Conventions used below**

- **"Deviation"** = value minus your own rolling personal baseline (e.g. trailing 7–28 day median), not an absolute number. The handleiding repeatedly stresses that absolute values are meaningless across people; for you they're meaningless across *seasons and device changes* too.
- **`t0`** = day of a labelled crash/dip. **`t-n` / `t+n`** = days before/after. The workhorse method for most of these is **peri-event alignment**: stack all crash episodes at `t0`, average each metric across `t-5 … t+5`, and look at the shape.
- **Exertion proxy** = whatever you decide best stands in for "did too much": steps, intensive minutes, an activity flag, calendar load, or a composite.

**Statistical hygiene (you know these, listed so the register is self-contained)**

- ~40 hypotheses here ⇒ **multiple-comparisons risk**. Pre-specify a primary handful (see the shortlist at the end), treat the rest as exploratory, and confirm anything promising with **walk-forward / out-of-sample validation** rather than re-fitting on the whole series.
- Days are **autocorrelated** — don't treat them as independent samples. Use block/seasonal methods or model the autocorrelation explicitly.
- **Regression to the mean** around crashes will manufacture "recovery" effects. Peri-event windows must be read with that in mind.
- **Acute-illness crashes ≠ everyday PEM sags** (your prior finding). Label and analyse them separately everywhere below; several hypotheses (G3, H3, H4) are *about* that separation.
- **Device-baseline lag**: the handleiding notes a watch needs ~3 weeks to learn your baseline, fills gaps with estimates, and that a new sensor shifts stress/HRV readings. Mark device-change points and the first ~3 weeks of any device as suspect.

---

## A. Resting HR & night HR

| ID | Testable hypothesis | Needs | Predicted direction |
|----|--------------------|-------|---------------------|
| A1 | Resting-HR deviation is elevated on and just before crash days | RHR | RHR↑ around `t0`; magnitude scales with exertion proxy |
| A2 | RHR deviates from baseline in **either** direction on bad days, not only upward (handleiding: a *lower* RHR can also follow overexertion) | RHR | `\|RHR − baseline\|` ↑ associates with lower gevoelscore |
| A3 | Night resting HR is elevated on PEM/crash days and the lead-in days | Night RHR | Night RHR↑ from `t-2`, peaks near `t0` |
| A4 | Sustained (multi-hour) RHR elevation, not a brief spike, marks "real" overexertion | Intraday HR | Needs intraday export — flag as not-yet-testable if only daily summaries exist |

## B. HRV

| ID | Testable hypothesis | Needs | Predicted direction |
|----|--------------------|-------|---------------------|
| B1 | A day-over-day night-HRV drop of ≥~10 (units/ms) predicts a crash | Night HRV | ≥10 drop ⇒ raised crash probability `t0`/`t+1`; report sensitivity & specificity for *your* crashes |
| B2 ⚠️ | In PEM, HRV declines over **multiple days even with rest** — not a single-day dip | Night HRV | Monotone-ish HRV decline across the peri-crash window. **Compare against your t+2/t+3 echo finding** (see H1) |
| B3 | A slowly rising 7-day HRV baseline coincides with improving periods | Night HRV (7d avg) | HRV baseline↑ in your low-crash / low-volatility stretches |
| B4 ⚠️ | A **sudden HRV spike is a *negative* leading indicator** (parasympathetic swing), not good news | Night HRV | Large positive HRV outlier ⇒ raised crash/steep-drain risk at `t+1`/`t+2` (counter-intuitive; high value) |
| B5 | HRV can *rise* at the onset of acute illness (distinct from PEM) | Night HRV + illness labels | HRV↑ in the 1–2 days before illness-crash onset |

## C. Stress score (Garmin daytime/night, HRV-derived)

| ID | Testable hypothesis | Needs | Predicted direction |
|----|--------------------|-------|---------------------|
| C1 | Night "orange" (high) stress is elevated on PEM/crash days and lead-in | Night stress (mean or % orange) | Night stress↑ from `t-1`, high at `t0` |
| C2 | High total daily stress predicts **worse next-day recharge** | Daily stress score, overnight BB gain | Stress(`t`)↑ ⇒ BB gain(`t→t+1`)↓ and gevoelscore(`t+1`)↓ |
| C3 ⚠️ | The stress→fatigue relationship is **non-linear/convex** (a 30→40 step costs far more than it looks) | Daily stress, gevoelscore | Marginal effect of stress on gevoelscore increases at higher stress; test with binning / spline, not just linear r |
| C4 | After overexertion, stress fails to drop during rest periods ("stuck sympathetic") | Intraday stress | Needs intraday export; reduced within-day recovery dips on `t+1` |

## D. Body battery (BB)

| ID | Testable hypothesis | Needs | Predicted direction |
|----|--------------------|-------|---------------------|
| D1 ⚠️ | **Absolute BB level is a weak indicator** of gevoelscore (supports your scale-compression view) | BB level, gevoelscore | Low same-day correlation between BB level and gevoelscore |
| D2 | **BB dynamics beat BB level**: overnight net charge / drain rate predict gevoelscore better than the level | BB overnight gain, daytime slope | Overnight gain and shallower drain ⇒ higher gevoelscore; out-predicts D1 |
| D3 | Living "at the top" (higher BB floor) coincides with fewer crashes | BB daily min/mean | Higher BB floor in low-crash stretches |
| D4 | BB declines steeply around crashes and leads the gevoelscore dip | BB daily slope | Steeper drain from `t-1`; test whether slope *leads* the felt dip |
| D5 ⚠️ | Paradoxically **high morning BB after overexertion precedes a crash** (false-energy / swing) | Morning BB + exertion proxy | High morning BB *given* prior-day overexertion ⇒ raised crash risk (BB as sometimes-inverted signal) |

## E. Steps / activity load

| ID | Testable hypothesis | Needs | Predicted direction |
|----|--------------------|-------|---------------------|
| E1 ⚠️ | There is a **personal step threshold** above which crash probability rises sharply (her own: ~1600 fine, ~3000 ⇒ PEM) | Steps, crash labels | Find your breakpoint; dose-response, not linear. Test steps at `t-2`/`t-3` vs crash at `t0` to respect your lag |
| E2 | Rising rolling step average **without** rising crash frequency marks genuine improvement | Steps, crash labels | In improving periods, step avg↑ while crash rate flat/↓ (your "improvement = fewer crashes" metric, cross-checked) |
| E3 | Intensive/active minutes track exertion better than raw steps for you | Intensive minutes vs steps | One predicts crashes more cleanly; compare |

## F. Sleep

| ID | Testable hypothesis | Needs | Predicted direction |
|----|--------------------|-------|---------------------|
| F1 | Longer-than-normal sleep duration is typical during PEM | Sleep duration | Sleep duration↑ on the PEM night(s); test deviation around `t0` |
| F2 | Deep-sleep deviation (too little *or* too much) associates with worse gevoelscore | Deep-sleep minutes | `\|deep-sleep − baseline\|` ↑ ⇒ gevoelscore↓ |
| F3 | Garmin sleep score predicts next-day capacity | Sleep score | Sleep score(`t`) ⇒ gevoelscore(`t+1`) |
| F4 | Bedtime **inconsistency** worsens next-day energy | Bedtime timestamps | Higher bedtime variance ⇒ lower gevoelscore next day (needs timestamps, not just duration) |

## G. Other sensors

| ID | Testable hypothesis | Needs | Predicted direction | Note |
|----|--------------------|-------|---------------------|------|
| G1 | Elevated respiration rate marks "stuck sympathetic"/poor recovery | Respiration rate | Resp↑ on crash days | Needs resp export |
| G2 | Estimated/skin temperature rises around PEM onset (minority: drops) | Temperature | Temp deviates around `t0`; **find your own sign** (n-of-1) | Needs temp; many models lack it |
| G3 ⚠️ | **Low / falling barometric pressure associates with worse gevoelscore and with headache days** | Gevoelscore, headache tag + weather data (external join) | Low/declining pressure ⇒ headache↑, gevoelscore↓ | High value: headache is your master variable, and pressure is free external data |
| G4 | SpO2 dips on exertion in long covid | SpO2 | — | Instrument unreliable on Garmin per handleiding; **deprioritise** |

## H. Mechanism & lead/lag (the decisive tests)

| ID | Testable hypothesis | Needs | Why it matters |
|----|--------------------|-------|----------------|
| H1 ⚠️ | **Wearable signals (HRV/RHR/stress) *lead* the gevoelscore crash**, i.e. give earlier warning than the felt score | All core Garmin + gevoelscore, exertion proxy | The handleiding implies HRV drops "that night or next"; your own finding is a t+2/t+3 *felt* echo. If the wearable leads the felt dip, wearables add genuine predictive value over self-report. If not, they don't — this is the single most important product test |
| H2 ⚠️ | **A meaningful fraction of your crashes are "activity-invisible"**: low steps / no HR spikes, but a gevoelscore crash + night-HRV drop (mental/cognitive PEM) | Steps, HR, HRV, gevoelscore | Quantifies the irreducible-self-report case and the calendar-first argument: if many crashes have no physical wearable signature, the wrist can't see them |
| H3 ⚠️ | **Acute-illness crashes have a different Garmin signature than PEM sags** (e.g. sustained RHR↑ + temp↑ + BB pre-drop the evening before, vs HRV-led + exertion-preceded for PEM) | RHR, temp, BB, HRV, illness vs PEM labels | Validates keeping the two mechanisms separate; a classifier that separates them confirms your prior finding |
| H4 ⚠️ | The **parasympathetic-swing signature** (night HRV↑ + night RHR↓ the night after overexertion) precedes a gevoelscore dip within 1–2 days | Night HRV, night RHR, exertion proxy, gevoelscore | Tests B4/D5 as a concrete detectable pattern; if real, it's a powerful pre-emptive cue that *contradicts* the naive "good numbers = good day" reading |
| H5 | Each metric has a characteristic lag vs the exertion proxy; lags differ by metric | All core metrics, exertion proxy | Cross-correlation per metric. Builds the empirical lag map your product's "PEM window" flag should be based on |

## I. Data-quality / methodology checks (not about your body)

| ID | Check |
|----|-------|
| I1 | Re-run primary results excluding the first ~3 weeks of each device and all imputed/"dotted-line" BB periods; confirm conclusions are stable |
| I2 | Mark device-change points; test for level shifts in stress/HRV across them (sensor change ⇒ baseline jump per handleiding) |
| I3 | Confirm the overlap window: rich Garmin metrics (sleep score, HRV status) only exist from ~2021 / newer models, so the span where they overlap your full gevoelscore streak may be much shorter than the streak itself |

---

## Priority shortlist (run these first)

These six decide product direction; everything else is supporting texture.

1. **H1 — does the wearable lead the felt crash?** If yes, wearables earn their place; if no, your one-tap gevoelscore is already the better instrument.
2. **H2 — how many crashes are activity-invisible?** Direct evidence for cognitive/emotional strain as first-class inputs and for calendar-first sequencing.
3. **H3 — acute illness vs PEM separable in Garmin data?** Confirms your two-mechanism model.
4. **C3 / D1–D2 — non-linearity of stress and level-vs-dynamics of body battery.** Confirms your scale-compression thesis with a second data source.
5. **B4 / H4 — parasympathetic swing as an inverted indicator.** The most counter-intuitive, and if real, the most useful pre-emptive cue.
6. **G3 — barometric pressure × headache.** Cheap external data against your master variable; potentially a strong, easily-explained signal.

---

*Source of claims: Wiggers, "Watch Smart Pacing" handleiding (ME/cvs Vereniging, 07-2025), distilled and re-expressed as hypotheses. Empirical claims are the authors'; the operationalisations and the conflict-flags against your prior analysis are added here for testing.*
