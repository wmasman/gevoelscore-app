# Testable hypotheses from the Wiggers smartwatch-pacing handleiding

*For n-of-1 validation against Willem's multi-year Garmin + gevoelscore dataset (with labelled dip and crash episodes).*

---

## How to read this

The handleiding is a collection of *lotgenoten* observations and n-of-1 generalisations. Treat every line below as a **hypothesis to test against your own data**, not as an established fact. Several of them directly contradict, or sharpen, things you've already found — those are the high-value ones, flagged with ⚠️.

**Conventions used below**

- **"Deviation"** = value minus your own rolling personal baseline (e.g. trailing 7–28 day median), not an absolute number. The handleiding repeatedly stresses that absolute values are meaningless across people; for you they're meaningless across *seasons and device changes* too.
- **`t0`** = day of a labelled crash/dip. **`t-n` / `t+n`** = days before/after. The workhorse method for most of these is **peri-event alignment**: stack all crash episodes at `t0`, average each metric across `t-5 … t+5`, and look at the shape.
- **Exertion proxy** = whatever you decide best stands in for "did too much": steps, intensive minutes, an activity flag, calendar load, or a composite. **For tests on `per_day_master.csv`, use the v3.2 lagged columns** (see Column choice below); v3.1 columns (`exertion_class`, `step_z_30d`) stay in the master for reproducibility of HA01b/HA02c only.

**Column choice for `per_day_master.csv` (locked 2026-06-12)**

| hypothesis-need | v3.2 column to use | notes |
|---|---|---|
| Continuous exertion proxy for scaling / correlation / lag-profile (A1, H1, H3, H5) | `exertion_rank_composite_lagged` | float 0-1 |
| Threshold "did too much" for overexertion stratification (B4, D5, H2, H4) | `exertion_class_lagged` in `{heavy, very_heavy}` | categorical |
| Steps-specific threshold or trend (E1, E2) | `step_rank_lagged` and `effective_exertion_slope_28d` | dose-response, creeping floor |
| Per-axis comparison "which axis predicts best" (E3) | `step_rank_lagged`, `eff_exertion_rank_lagged`, `max_hr_rank_lagged`, `vigorous_min_rank_lagged` | side-by-side |
| Activity-invisible crash detection (H2) | low `step_rank_lagged` + low `max_hr_rank_lagged` + crash | combine |
| Sustained-elevation push count (E2, H4 supporting) | `push_burden_7d_lagged` | int 0-7 |
| Body Battery level / dynamics (D1, D3) | `bb_highest`, `bb_lowest` | int 0-100 |
| Overnight Body Battery gain (D2) | `bb_overnight_gain` (= `bb_sleep_end_value - bb_sleep_start_value`) | int; 33.8% fill (only when sleep+BB align) |
| Body Battery drain rate around crashes (D4) | `bb_drained_24h` | int |
| Morning Body Battery after overexertion (D5) | `bb_sleep_end_value` | int; 33.8% fill |
| All-day stress total (C2, C3) | `all_day_stress_avg`, `all_day_stress_max` | int 0-100; TOTAL aggregator |
| Waking vs sleep stress separation (C1, C2) | `awake_stress_avg`, `asleep_stress_avg_uds` (cross-check vs `stress_mean_sleep`) | int 0-100 |
| Sleep duration / stages (F1, F2) | `sleep_duration_min`, `sleep_deep_min`, `sleep_light_min`, `sleep_awake_min` | minutes |
| Bedtime inconsistency (F4) | `bedtime_std_7d` | hours |
| Respiration during sleep + waking (G1) | `respiration_avg_sleep`, `respiration_max_sleep`; `respiration_avg_waking`, `respiration_max_24h` | breaths/min |
| SpO2 (G4, deprioritised) | `spo2_avg_sleep`, `spo2_min_sleep`, `spo2_avg_24h`, `spo2_min_24h` | percent |
| **A4 — sustained HR elevation operationalised** | `hr_sustained_elevated_flag` (bool, longest run ≥ 30 min above `hr_daytime_baseline_lagged + 20` bpm), `hr_longest_elevated_run_min_waking` (minutes), `hr_area_above_daytime_baseline_waking` (bpm⋅min), plus transparency cols `hr_median_waking` + `hr_daytime_baseline_lagged` | per-minute bins over waking window only; baseline = lagged `[d-90, d-30]` median of `hr_median_waking` (same shape as v3.2 lagged exertion) |
| **C4 — stress-decay-after-peak operationalised** | `stress_post_peak_time_to_rest_min` (primary; NaN = "did not return to rest that day" = C4-positive), `stress_post_peak_drop_avg`, `stress_recovery_pct_within_2h`, `stress_high_duration_min` | minutes / Garmin 0-100 |

**HRV-dependent hypotheses are hardware-blocked on this dataset.** The Forerunner 245 (Elevate V3 sensor) does not produce nightly HRV Status; FIT sleep type-49 files store the relevant data in undocumented `unknown_273/274/276` messages with no community decode. **B1, B2, B3, B4, B5** (all of category B), and the **HRV-dependent parts of H1, H2, H3, H4, H5**, cannot be tested on this corpus. See [`methodology/garmin_indicators_audit.md`](methodology/garmin_indicators_audit.md) § HRV — hardware blocked. Only a device upgrade (Forerunner 265+, fēnix 7, etc.) would unblock these going forward; existing data remains untestable for HRV.

Source: [`methodology/garmin_indicators_audit.md`](methodology/garmin_indicators_audit.md) § Rule for new analyses; [`analyses/garmin_exploration/activity-labels/spec/severity_spec.md`](analyses/garmin_exploration/activity-labels/spec/severity_spec.md) § Lagged baseline.

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

## Pre-registration draft — variable mapping per hypothesis (locked 2026-06-12)

**Purpose**: this section names, per hypothesis, the **specific
master columns** intended as the predictor / outcome / covariate(s)
when the hypothesis is formally pre-registered in
[`docs/research/analyses/hypotheses/`](analyses/hypotheses/). It is
the bridge between Wiggers' handleiding language ("RHR deviation",
"exertion proxy", "sustained elevation") and the operational columns
in `per_day_master.csv`.

This is a **pre-registration draft**, not the formal pre-reg. When
each hypothesis lands in the hypothesis folder it gets its own
locked spec (with sample size, baseline-window choice, primary vs
secondary tests, alpha, etc.). The draft here pins down only the
column-selection layer.

Status legend:
- ✅ testable now on `per_day_master.csv` (1755 rows × 161 cols).
- ⚠️ partially testable — the columns exist but the test as Wiggers
  states it is degraded (e.g. an HRV-paired version stays blocked).
- ❌ blocked — primary signal not present in this dataset. Document
  the blocker and move on; do not pre-register.

Conventions:
- "deviation" = column value minus a rolling personal baseline. The
  master does not pre-compute deviations; analyses compute them from
  the raw column at the windowing stage they choose.
- "lead/lag" = peri-event alignment around `is_crash=True` days.
- "exertion proxy" defaults to `exertion_class_lagged_lcera` (PEM)
  or `exertion_rank_composite_lagged_lcera` (continuous) per the
  [use-lagged-exertion-for-pem memory](C:/Users/Gebruiker/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_use_lagged_exertion_for_pem.md).

### A. Resting HR & night HR

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| A1 | `resting_hr` deviation vs rolling 28d median | `is_crash` (peri-event window) | peri-event alignment at `t-3 … t+3`; stratify magnitude by `exertion_rank_composite_lagged_lcera` quartile | ✅ |
| A2 | `\|resting_hr − rolling_28d_median\|` | `gevoelscore` | correlation; allow both-direction deviation | ✅ |
| A3 | `resting_hr` (already sleep-derived per Garmin) | `is_crash` / `gevoelscore` | peri-event alignment from `t-2` | ✅ |
| A4 | `hr_sustained_elevated_flag` (primary categorical), `hr_longest_elevated_run_min_waking` (primary continuous), `hr_area_above_daytime_baseline_waking` (magnitude × duration); covariates / transparency: `hr_median_waking`, `hr_daytime_baseline_lagged` | `is_crash` next-day / current-day | cross-tab on the flag; regression on the continuous variants; A4 baseline = `[d-90, d-30]` lagged median of `hr_median_waking` + 20 bpm offset (v3 locked 2026-06-12; v1's resting_hr + 15 threshold was superseded same day for being too lenient) | ✅ (operationalised Wave 4 v3) |

### B. HRV — ALL BLOCKED on this device

| ID | blocker | status |
|---|---|---|
| B1, B2, B3, B4, B5 | Nightly HRV not produced by Forerunner 245 / Elevate V3. FIT sleep type-49 messages `unknown_273/274/276` carry undocumented data; community decode does not exist. Only an Elevate V4 device upgrade would unblock forward data. See `methodology/garmin_indicators_audit.md` § HRV — hardware blocked. | ❌ |

Do not pre-register B1-B5 on this corpus. Note them in the hypothesis
folder as device-blocked so the reasoning survives.

### C. Stress score

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| C1 | `stress_mean_sleep` (FIT-derived sleep mean) as proxy for "night orange"; secondary: `stress_high_duration_min` during waking-window peri-event window | `is_crash` from `t-1` | peri-event alignment | ✅ — "% orange specifically" would need a finer FIT re-walk; proxy is adequate for v1 |
| C2 | `all_day_stress_avg` (TOTAL aggregator) | `bb_overnight_gain` (paired-night) AND `gevoelscore` next-day | two-stage correlation | ✅ |
| C3 | `all_day_stress_avg` (binned at 0-20, 20-30, 30-40, 40-60, 60+) | `gevoelscore` | binned mean comparison or natural-spline regression; **NOT linear correlation** (the hypothesis itself rejects linearity) | ✅ |
| C4 | `stress_post_peak_time_to_rest_min` (primary; NaN-on-failure = positive case), `stress_post_peak_drop_avg` (secondary), conditioned on `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T | within-day decay metric — no separate outcome needed; the column IS the outcome | stratified comparison: time-to-rest on heavy days vs non-heavy days | ✅ (operationalised Wave 4) |

### D. Body Battery

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| D1 | `bb_highest`, `bb_lowest` (same-day, absolute levels) | `gevoelscore` | same-day correlation; Wiggers expects WEAK correlation | ✅ |
| D2 | `bb_overnight_gain` (= `bb_sleep_end_value − bb_sleep_start_value`); fallback `bb_charged_24h − bb_drained_24h` when overnight-gain is NaN (33.8% fill) | `gevoelscore` same-day; secondary: out-predicts D1 | side-by-side regression of `gevoelscore` on D1 columns vs D2 columns; compare effect sizes | ✅ |
| D3 | rolling 28d mean of `bb_lowest` | rolling 28d crash rate (`is_crash` mean) | rolling-window correlation across the validate era | ✅ |
| D4 | `bb_drained_24h` slope across `t-3 … t0` | `is_crash` at `t0` | peri-event drain trajectory | ✅ |
| D5 ⚠️ | `bb_sleep_end_value` (morning BB at wake), conditional on `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on `t-1` | `is_crash` at `t0` and `t0+1` | conditional contingency: P(crash \| high morning BB ∧ prior-day overexertion) vs base rate | ✅ (the cleanest single test; 33.8% fill on the morning BB column constrains sample size) |

### E. Steps / activity load

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| E1 ⚠️ | `step_rank_lagged` at `t-2`, `t-3`; secondary: raw `total_steps`; covariate: `steps_above_goal_flag` (personal-anchor proxy) | `is_crash` at `t0` | dose-response / breakpoint regression; respect the lag (Wiggers expects steps at t-2/t-3 → crash at t0) | ✅ |
| E2 | `effective_exertion_slope_28d` (positive slope = rising trajectory) + `above_baseline_streak` | rolling 28d crash rate | "rising steps without rising crashes" = positive slope AND non-rising rolling crash rate over the same window | ✅ |
| E3 | side-by-side: `step_rank_lagged`, `vigorous_min_rank_lagged`, `eff_exertion_rank_lagged`, `max_hr_rank_lagged` | `is_crash` | compare effect sizes / AUC across the 4 axes | ✅ |

### F. Sleep

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| F1 | `sleep_duration_min` deviation vs rolling 28d median | `is_crash` (sleep on the PEM night) | peri-event window | ✅ |
| F2 | `sleep_deep_min` deviation (and absolute value) | `gevoelscore` next-day | regression; allow both-direction effect | ✅ |
| F3 | (Garmin sleep score) | — | — | ❌ skipped per user; not in `sleepData.json`, FIT-side unverified, low marginal leverage given F1+F2+F4 |
| F4 | `bedtime_std_7d` | `gevoelscore` next-day | regression / lag-1 correlation | ✅ |

### G. Other sensors

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| G1 | `respiration_avg_sleep` AND `respiration_max_24h` (sleep + waking variants both) | `is_crash` (sleep variant); `gevoelscore` (waking variant) | peri-event window | ✅ |
| G2 | (skin temperature) | — | — | ❌ blocked — sensor not on fr245 |
| G3 ⚠️ | (barometric pressure, external KNMI join) | `gevoelscore`; secondary: count of `cat_sub_hoofdpijn > 0` days | once external data is fetched | ⚠️ deferred-external (no Garmin column) |
| G4 | `spo2_avg_sleep`, `spo2_min_sleep` (sleep variants); secondary: `spo2_avg_24h`, `spo2_min_24h` | `gevoelscore` | peri-event window | ✅ — included for completeness; Wiggers deprioritised |

### H. Mechanism & lead/lag — fully or partially blocked

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| H1 ⚠️ | wearable channel without HRV: `bb_overnight_gain` + `stress_mean_sleep` + `resting_hr` deviation; HRV-leading is the original Wiggers claim, not testable | `gevoelscore` (the "felt" crash) | cross-correlation lag profiles per metric | ⚠️ — HRV-leading test stays blocked; the wearable-vs-gevoelscore latency comparison is testable on non-HRV signals only |
| H2 ⚠️ | "activity-invisible" defined as `step_rank_lagged < 0.3` AND `max_hr_rank_lagged < 0.3` AND no `hr_sustained_elevated_flag` | `is_crash` | fraction of crashes meeting the activity-invisible criterion | ⚠️ — Wiggers names HRV-drop on the same days as a confirming signal; without HRV the test gives a lower bound on the activity-invisible fraction |
| H3 ⚠️ | `resting_hr`, `bb_charged_24h`/`bb_drained_24h`, `respiration_avg_sleep` — pre-crash signatures; outcome: pre-labeled illness vs PEM | classifier (logistic / RF) trained on the per-day vectors | testable on the labeled subset; HRV + temp would have been the discriminative signals per Wiggers, both blocked | ⚠️ — partial; expect reduced separability |
| H4 ⚠️ | (night HRV↑ + night `resting_hr`↓ together after `exertion_class_lagged_lcera ∈ heavy`) | `is_crash` at T+1, T+2 | parasympathetic-swing signature requires HRV | ❌ — RHR-only version is too weak; do not pre-register without HRV |
| H5 ⚠️ | per-metric cross-correlation vs `exertion_rank_composite_lagged_lcera` | each metric's lag profile | cross-correlation per: `resting_hr`, `stress_mean_sleep`, `bb_overnight_gain`, `gevoelscore` | ⚠️ — full lag map per Wiggers includes HRV; partial map without it |

### I. Data-quality / methodology

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| I1 | re-run any primary test excluding the first 21 days of `has_garmin_uds=True` coverage | same outcome as the original test | sensitivity comparison | ✅ |
| I2 | no device change in this dump — fr245 / serial 3377851255 throughout 2021-08-16 → today | — | — | N/A on this dataset |
| I3 | confirm overlap: gevoelscore from 2022-09-03, Garmin metrics from 2021-08-16, rich metrics (sleep stages, BB stat list) from various dates onward | per-column `coverage` in DATA_DICTIONARY | already documented per column | ✅ already done — see DATA_DICTIONARY § per-column coverage |

### Summary: what survives, what doesn't

| category | testable count | blocked count | partial count |
|---|---|---|---|
| A | 4 | 0 | 0 |
| B | 0 | 5 | 0 |
| C | 4 | 0 | 0 |
| D | 5 | 0 | 0 |
| E | 3 | 0 | 0 |
| F | 3 | 1 (F3 — skipped) | 0 |
| G | 2 | 1 (G2 hardware) | 1 (G3 external) |
| H | 0 | 1 (H4) | 4 |
| I | 2 | 0 | 0 (I2 N/A) |
| **total** | **23** | **8** | **5** |

23 hypotheses are pre-registration-ready on the current 161-column
master. 5 more are partially testable (with documented caveats). 8
are blocked and should be marked as such — not pre-registered — in
the hypothesis folder.

---

*Source of claims: Wiggers, "Watch Smart Pacing" handleiding (ME/cvs Vereniging, 07-2025), distilled and re-expressed as hypotheses. Empirical claims are the authors'; the operationalisations and the conflict-flags against your prior analysis are added here for testing.*
