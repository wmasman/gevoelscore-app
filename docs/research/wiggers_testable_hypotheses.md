# Testable hypotheses from the Wiggers smartwatch-pacing handleiding

*For n-of-1 validation against Willem's multi-year Garmin + gevoelscore dataset (with labelled dip and crash episodes).*

---

## How to read this

The handleiding is a collection of *lotgenoten* observations and n-of-1 generalisations. Treat every line below as a **hypothesis to test against your own data**, not as an established fact. Several of them directly contradict, or sharpen, things you've already found — those are the high-value ones, flagged with ⚠️.

**Conventions used below**

- **Framing**: all tests below are within-subject counterfactual comparisons against the participant's own rolling baseline, not against a population. The framework is Daza 2018 (*Methods of Information in Medicine*); see [`methodology/wiggers_test_design_on_chained_regime.md`](methodology/wiggers_test_design_on_chained_regime.md) for the chained-regime adjustments.
- **"Deviation"** = value minus your own rolling personal baseline (e.g. trailing 7–28 day median), not an absolute number. The handleiding repeatedly stresses that absolute values are meaningless across people; for you they're meaningless across *seasons and device changes* too.
- **`t0`** = day of a labelled crash/dip. **`t-n` / `t+n`** = days before/after. The workhorse method for most of these is **peri-event alignment**: stack all crash episodes at `t0`, average each metric across `t-5 … t+5`, and look at the shape.
- **Exertion proxy** = whatever you decide best stands in for "did too much": steps, intensive minutes, an activity flag, calendar load, or a composite. **For tests on `per_day_master.csv`, use the v3.2 lagged columns** (see Column choice below); v3.1 columns (`exertion_class`, `step_z_30d`) stay in the master for reproducibility of HA01b/HA02c only.
- **Analysis scale** = picked per hypothesis from the mechanism's natural timescale, per [`methodology/time_resolution.md` §6](methodology/time_resolution.md). The pre-flight scale-sanity check is proposed in [`time_resolution.md` §7](methodology/time_resolution.md) but is not yet adopted as a CONVENTIONS audit hook. Default scale per cluster on this register (any pre-reg may override with documented mechanism reasoning):
  - **A1, A2, A3** — per-day (RHR + nightly attribution, gevoelscore co-movement). **A4** — per-minute (within-day sustained-elevation; operationalised via Wave 4 cols in [DATA_DICTIONARY §8B](DATA_DICTIONARY.md)).
  - **B1-B5** — per-day (sleep-window mean stress as HRV proxy; nightly attribution). B2 trend slope ⇒ situational multi-day window (7d).
  - **C1, C2, C3** — per-day (24h stress aggregator). **C4, C4b** — per-minute (within-day stress decay + walls + t+1 reactivity + motion filter).
  - **D1, D2, D3, D5** — per-day (BB daily aggregates + overnight gain). **D4** — situational multi-day window (slope across `t-3..t0`).
  - **E1** — situational multi-day window (predictor at `t-2`, `t-3`). **E2** — lagged reference frame (28d slope on `effective_exertion_slope_28d`). **E3** — per-day (side-by-side per-axis comparison).
  - **F1, F2, F3, F4** — per-day (sleep nightly attribution). F4's bedtime variance is a 7d-rolling derivative.
  - **G1-G4** — per-day. G3 (pressure × headache) gains a per-day-or-finer choice once external data lands per [`queued_work.md`](methodology/queued_work.md) Q18.
  - **H1, H2, H3, H4, H5** — situational multi-day windows (peri-event alignment, CCF lag profiling). Window lengths anchored to mechanism (PEM recovery tail, HRV multi-day cumulative drop), NOT a generic "weekly" grain.
  - **I1, I2, I3** — per-day (data-quality checks on coverage; not scale-bound).

**Column choice for `per_day_master.csv` (locked 2026-06-12)**

| hypothesis-need | v3.2 column to use | notes |
|---|---|---|
| Continuous exertion proxy for scaling / correlation / lag-profile (A1, H1, H3, H5) | `exertion_rank_composite_lagged_lcera` | float 0-1; `_lcera` per CONVENTIONS §3.2 for PEM-pacing tests on the LC frame |
| Threshold "did too much" for overexertion stratification (B4, D5, H2, H4) | `exertion_class_lagged_lcera` in `{heavy, very_heavy}` | categorical; `_lcera` per CONVENTIONS §3.2 for PEM-pacing tests on the LC frame |
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

**HRV-dependent hypotheses are partially testable via a `stress_mean_sleep` proxy on descriptive grounds (updated 2026-06-13).** The Forerunner 245 (Elevate V3 sensor) does not produce nightly HRV Status, but Garmin "stress" is computed by the same Firstbeat algorithm from the same R-R interval signal; during sleep the multivariate composite collapses toward its HRV-derived component. **Descriptive characterisation on this corpus** (see [`methodology/hrv_proxy_via_stress.md`](methodology/hrv_proxy_via_stress.md) Checks 7.1-7.3; raw run results in [`analyses/garmin_exploration/hrv_proxy_validation/result-table.txt`](analyses/garmin_exploration/hrv_proxy_validation/result-table.txt)): `stress_mean_sleep` is elevated around crash episodes (episode-level Cohen's d = +0.90; mean stress-unit difference +4.66 with CI95 [+1.51, +8.22] on the mean difference, not on d itself) and shares ~12% of variance with `resting_hr` (Pearson r = +0.342, R² = 0.117 → ~88% of sleep-stress variance is not HR-driven). On these descriptive grounds, **B1-B5 and H4 move from BLOCKED to PARTIAL**; **HRV-dependent parts of H1, H2, H3, H5 stay PARTIAL** with `stress_mean_sleep` added as a candidate HRV-proxy channel. Channel selection (single-channel vs multi-channel proxy framing) is a **pre-reg choice** to be resolved by held-out pre-registered analysis, not a methodology constant. See [`methodology/garmin_indicators_audit.md`](methodology/garmin_indicators_audit.md) § HRV for the audit verdict that authorises the reclassification. A device upgrade (Forerunner 265+, fēnix 7, etc.) would unblock direct HRV from the upgrade date onward; existing data remains testable only via the proxy.

Source: [`methodology/garmin_indicators_audit.md`](methodology/garmin_indicators_audit.md) § Rule for new analyses; [`analyses/garmin_exploration/activity-labels/spec/severity_spec.md`](analyses/garmin_exploration/activity-labels/spec/severity_spec.md) § Lagged baseline.

**Statistical hygiene (you know these, listed so the register is self-contained)**

- ~40 hypotheses here ⇒ **multiple-comparisons risk**. Pre-specify a primary handful (see the shortlist at the end), treat the rest as exploratory, and confirm anything promising with **walk-forward / out-of-sample validation** rather than re-fitting on the whole series.
- Days are **autocorrelated** — don't treat them as independent samples. Use block bootstrap or model the autocorrelation explicitly.
- **Crash-drop sensitivity row**: every Layer 4+ correlation / CCF / regression on PEM-pacing variables reports the result with `is_crash == True` rows dropped alongside the full-frame result. Per CONVENTIONS §3.4 + [[feedback_crash_distortion_sensitivity]]: |Δ ρ| > 0.10 = surface as a finding (on this corpus the exertion × resting_hr Spearman swings from ~+0.0 to ~+0.4 when crash days are dropped — the crash days do systematic work). The contrast itself is informative.
- **Regression to the mean** around crashes will manufacture "recovery" effects. Peri-event windows must be read with that in mind.
- **Acute-illness crashes ≠ everyday PEM sags** (your prior finding). Label and analyse them separately everywhere below; several hypotheses (G3, H3, H4) are *about* that separation.
- **Device-baseline lag**: the handleiding notes a watch needs ~3 weeks to learn your baseline, fills gaps with estimates, and that a new sensor shifts stress/HRV readings. Mark device-change points and the first ~3 weeks of any device as suspect.

---

## A. Resting HR & night HR

| ID | Testable hypothesis | Needs | Predicted direction |
|----|--------------------|-------|---------------------|
| A1 | Resting-HR deviation is elevated during crash episodes; magnitude scales with exertion dose | RHR | RHR↑ at `t0`; magnitude scales with exertion proxy (source-verified 2026-06-12 — see verification log) |
| A2 | RHR deviates from baseline in **either** direction on bad days, not only upward (handleiding: a *lower* RHR can also follow overexertion) | RHR | `\|RHR − baseline\|` ↑ associates with lower gevoelscore |
| A3 | Night resting HR is elevated on PEM/crash days and the lead-in days | Night RHR | Night RHR↑ from `t-2`, peaks near `t0` |
| A4 | Sustained (multi-hour) RHR elevation, not a brief spike, marks "real" overexertion | Intraday HR | Needs intraday export — flag as not-yet-testable if only daily summaries exist. **Future work — bout-level analysis would benefit**: bout-level recovery dynamics on the HR channel would extend A4's occurrence + duration framing (`hr_sustained_elevated_flag`, `hr_longest_elevated_run_min_waking`) with within-bout *recovery shape* (per-bout peak HR, HR-recovery half-life, decay slope). See [`methodology/bout_level_recovery_dynamics.md`](methodology/bout_level_recovery_dynamics.md) — operand is locked for stress channel; an A4 HA pre-reg invoking it would extend the operand to HR channel with documented operand adaptation. Available infrastructure, not auto-enabled. |

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
| C1 | Night "orange" (high) stress is elevated on PEM/crash days and lead-in | Night stress (mean or % orange) | Night stress↑ from `t-1`, high at `t0`. **Future work — bout-level analysis would benefit**: bout-level within-sleep recovery would resolve the dynamic structure the daily-aggregate `stress_mean_sleep` proxy collapses. See [`methodology/bout_level_recovery_dynamics.md`](methodology/bout_level_recovery_dynamics.md) — operand applies to within-night stress at the bout level (a C1 HA pre-reg invoking it would restrict to bouts where `bout_during_sleep_flag = True`). Available infrastructure, not auto-enabled. |
| C2 | High total daily stress predicts **worse next-day recharge** | Daily stress score, overnight BB gain | Stress(`t`)↑ ⇒ BB gain(`t→t+1`)↓ and gevoelscore(`t+1`)↓ |
| C3 ⚠️ | The stress→fatigue relationship is **non-linear/convex** (a 30→40 step costs far more than it looks) | Daily stress, gevoelscore | Marginal effect of stress on gevoelscore increases at higher stress; test with binning / spline, not just linear r |
| C4 | After overexertion, stress fails to drop during rest periods ("stuck sympathetic") | Intraday stress | Needs intraday export; reduced within-day recovery dips on `t+1`. **Formal pre-reg LOCKED 2026-06-18 v2 r2 at [`analyses/hypotheses/HA-C4/hypothesis.md`](analyses/hypotheses/HA-C4/hypothesis.md)** (v1 LOCKED 2026-06-17 → dry-run HALTED on Ch3 validate n=25 < 30 → v2 fresh-session draft 2026-06-18 with §5.3 INCONCLUSIVE-aware verdict rule + §7.3 arithmetic rebuild + §4.11.3 chain-relaxed sensitivity arm → fresh-session §3.4 audit PASS-with-caveats → r2 four side-obs closures → §3.6 compression). 3-channel confirmatory triad (decay / walls / t+1 reactivity) with INCONCLUSIVE-aware verdict bands (3.0 strong / 2.0-2.5 SUPPORTED / 1.0-1.5 PARTIAL / <1.0 REJECTED). **v2 test-executed 2026-06-18 → REJECTED at daily-aggregate level** (triad sum = 0.0; Ch1 + Ch2 validate SUPPORTED but train REFUTED; Ch3 train wrong-direction; Ch3 validate INCONCLUSIVE; commit `52bddb5`). Channel 1's `stress_post_peak_drop_avg` companion SUPPORTED on BOTH eras at +0.210 / +0.364 — hint of within-day recovery signal that daily aggregate collapsed. **Bout-level reframing landed via HA-C4c**: [`methodology/bout_level_recovery_dynamics.md`](methodology/bout_level_recovery_dynamics.md) + sub-MD [`methodology/bout_level_dose_response_calibration.md`](methodology/bout_level_dose_response_calibration.md) co-LOCKED 2026-06-21 `c57ff3f`; **HA-C4c r2 LOCKED 2026-06-23** `4e666a2` (Option γ canonical 4-stage) → **tested 2026-06-23 → PARTIAL** at [`analyses/hypotheses/HA-C4c/result.md`](analyses/hypotheses/HA-C4c/result.md) `a69a8ed`. Configuration: bar (a) discrimination PASS (p=0.0001) + bar (b) effect-size FAIL (Cliff's δ=+0.120 vs threshold ≥+0.20); direction positive (heavy-T > non-heavy-T). **Inverse failure-mode vs HA11-bout-redo's PARTIAL** — HA11-bout-redo at n=70/11 had magnitude PASS + p FAIL; HA-C4c at cross-phase-pooled n=465/809 has p PASS + magnitude FAIL. The materially-larger n removed HA11-bout-redo's power-shortfall constraint, exposing a weak-effect-but-real positive pattern (per HA-C4c §9.2 PARTIAL second configuration); the substantive Wiggers C4 reading at bout resolution is a positive but small-magnitude effect, below the pre-committed +0.20 small-to-medium threshold. **Sensitivity arms**: unmedicated-only (n=183/323) REJECTED at δ=+0.059 (stratum-fragility per §9.5 — cross-phase pooling is doing analytical work); motion-clean-only REJECTED at near-zero δ (32/4317 bouts motion-clean — 99.3% corpus-property reaffirmation per §8 caveat 4); transient-excluded + baseline-invalid-excluded both PARTIAL (consistent); crash-drop PARTIAL with |Δ δ|=0.015 (CLEAN per CONVENTIONS §3.4); Approach A all 3 sub-arms PARTIAL (no β-precision-fragility). Holm step-down primary + transient-excluded both Holm-rejected at adj_p=0.0004. v2 daily-aggregate REJECTED verdict + HA-C4c bout-level PARTIAL verdict coexist (per HA-C4c §8 caveat 9). |
| C4b | C4 with **motion filter**: condition the rest-stress signal on concurrent low motion (discriminates true sympathetic-arousal-during-rest from motion-artefact stress) | Intraday stress + intraday steps | Per-day count of stress-with-low-motion minutes elevated before crashes vs matched non-crash heavy-exertion days. **Future work — bout-level analysis would benefit**: HA-C4b v3 NOT-SUPPORTED on the per-day count headline (2026-06-17). Bout-level reframing could discriminate within the same C4b primitive — "many short bouts" vs "few sustained bouts" produce the same per-day minute-count but different per-bout feature distributions; the C4b v3 §9 NOT-SUPPORTED branch's alternative readings (PROTECTIVE-not-PREDICTIVE OR emotionally-triggered crashes) might be discriminable via per-bout features the per-day count cannot resolve. See [`methodology/bout_level_recovery_dynamics.md`](methodology/bout_level_recovery_dynamics.md) — operand composes with [`stress_low_motion_primitive.md`](methodology/stress_low_motion_primitive.md) via the per-bout `motion_confound_flag` field. Available infrastructure, not auto-enabled. |

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
| H1 ⚠️ | **Wearable signals (HRV/RHR/stress) *lead* the gevoelscore crash**, i.e. give earlier warning than the felt score | All core Garmin + gevoelscore, exertion proxy | The handleiding implies HRV drops "that night or next"; your own finding is a t+2/t+3 *felt* echo. If the wearable leads the felt dip, wearables add genuine predictive value over self-report. If not, they don't — this is the single most important product test. **Source verification (batch 3)**: Wiggers' explicit predictive claim is HRV-specific (blocked on FR245); the Mental PEM concession (PDF lines 1448-1457) explicitly supports H2 (activity-invisible crashes) as Wiggers' own H1 limitation. See verification log |
| H2 ⚠️ | **A meaningful fraction of your crashes are "activity-invisible"**: low steps / no HR spikes, but a gevoelscore crash + night-HRV drop (mental/cognitive PEM) | Steps, HR, HRV, gevoelscore | Quantifies the irreducible-self-report case and the calendar-first argument: if many crashes have no physical wearable signature, the wrist can't see them |
| H3 ⚠️ | **Acute-illness crashes have a different Garmin signature than PEM sags** (e.g. sustained RHR↑ + temp↑ + BB pre-drop the evening before, vs HRV-led + exertion-preceded for PEM) | RHR, temp, BB, HRV, illness vs PEM labels | Validates keeping the two mechanisms separate; a classifier that separates them confirms your prior finding |
| H4 ⚠️ | The **parasympathetic-swing signature** (night HRV↑ + night RHR↓ the night after overexertion) precedes a gevoelscore dip within 1–2 days | Night HRV, night RHR, exertion proxy, gevoelscore | Tests B4/D5 as a concrete detectable pattern; if real, it's a powerful pre-emptive cue that *contradicts* the naive "good numbers = good day" reading. **Future work — bout-level analysis would benefit**: per-bout characterisation could isolate the parasympathetic swing event vs steady-state, which the BB-anchored composite (currently daily-aggregate) cannot resolve. See [`methodology/bout_level_recovery_dynamics.md`](methodology/bout_level_recovery_dynamics.md) — operand applies at the post-exertion swing-night level (an H4 HA pre-reg invoking it would extend the operand to a parasympathetic-swing-bout signature, with `decay_slope` direction reversed under swing semantics). Available infrastructure, not auto-enabled. |
| H5 | Each metric has a characteristic lag vs the exertion proxy; lags differ by metric | All core metrics, exertion proxy | Cross-correlation per metric. Builds the empirical lag map your product's "PEM window" flag should be based on. **Source verification (batch 3)**: Wiggers' implicit lag order is BB/stress (same/next day) ≤ RHR (hours-to-day) < HRV (multi-day cumulative). Pre-reg can test the predicted ordering as a confirmation check, not just compute lags. See verification log |

## I. Data-quality / methodology checks (not about your body)

| ID | Check |
|----|-------|
| I1 | Re-run primary results excluding the first ~3 weeks of each device and all imputed/"dotted-line" BB periods; confirm conclusions are stable |
| I2 | Mark device-change points; test for level shifts in stress/HRV across them (sensor change ⇒ baseline jump per handleiding) |
| I3 | Confirm the overlap window: rich Garmin metrics (sleep score, HRV status) only exist from ~2021 / newer models, so the span where they overlap your full gevoelscore streak may be much shorter than the streak itself |

---

## Priority shortlist (set by verification × family-history criteria)

*Priority re-tiered 2026-06-14, replacing the 2026-06-13 intersection rule. The 2026-06-13 rule used artifact-baseline descriptive numbers for A1 + B1 (HA01b validate +17.3 pp at v3.1 rolling baseline; on the v3.2 lagged baseline HA01b-recomputed is REFUTED both eras at +5.8 / +4.0 pp per [`REJECTED.md`](REJECTED.md)). The new criteria:*

- *Tier 1 = source-verified verbatim AND no related HA-test family history. Pre-reg can lock without the family-history acknowledgement constraint.*
- *Tier 2 = source-verified AND has related HA-test family history. Pre-reg MUST include constraint 8 (prior test family acknowledgement) + an explicit stop-rule per the family.*
- *Tier 3 = needs descriptive prereq before any pre-reg (external data, reframing, source verification).*

*Parallel register: [`personal_hypotheses.md`](personal_hypotheses.md) for hypotheses with independent priors (lived experience + literature + mechanism). Different validation discipline — descriptive characterisation, no held-out required, forward-collected data as natural validation.*

*Validation framework for all tiers: full Stratum 4 single pool per [`methodology/train_validate_split_fate.md`](methodology/train_validate_split_fate.md); block-length policy per [`methodology/permutation_null_block_length.md`](methodology/permutation_null_block_length.md); multiplicity correction is Holm step-down on N_eff ≈ 4 per [`methodology/wiggers_test_design_on_chained_regime.md`](methodology/wiggers_test_design_on_chained_regime.md) § Cross-cutting statistical hygiene.*

### Tier 1 — source-verified verbatim + no family history (priority pre-regs)

| ID | why | class | column infrastructure |
|---|---|---|---|
| **C3** (non-linear stress → fatigue) | source-verified VERBATIM (PDF 1357-1368); 30 → 40 stress step costs more than it looks. **Two sister pre-regs LOCKED 2026-06-23**: (a) **HA-C3 v2 r2 LOCKED `2a0b0df`** ([`analyses/hypotheses/HA-C3/hypothesis.md`](analyses/hypotheses/HA-C3/hypothesis.md)) — Wiggers-verbatim test; 4-bin spec `[0,30), [30,40), [40,60), [60+]` preserving Wiggers 30→40 anchor at new B2-B3 boundary (post-HALT redraft after v1 r2 LOCKED `de22b68` → tested `a9423af` → HALT on §7.5 Gate 1 B1 [0,20) n=0 structurally absent + B5 n=1 per §10.4 step 3); v2 r1 drafted `724c814` → audit PASS-with-caveats `e2bca27` → r2 §3.6-compression `2a0b0df` (4 mechanical wording absorbs: §8 c12 sister-test extension naming HA-C3p + §1 STROBE-Item-12 forward-ref + §8 c11 op-consequence note + §7.4 caveat-class tightening); v1 artefacts archived `-v1-archived.*`. (b) **HA-C3p r2 LOCKED `c0148ca`** ([`analyses/hypotheses/HA-C3p/hypothesis.md`](analyses/hypotheses/HA-C3p/hypothesis.md)) — **personal-baseline sister pre-reg per CONVENTIONS §3.1** (project-canonical complement to v2's Wiggers-verbatim); equal-N quintile bins on full Stratum 4 (Q1 [0,28) / Q2 [28,31) / Q3 [31,34) / Q4 [34,37) / Q5 [37,100] per per_day_master snapshot SHA `d0ff9253`); tests the underlying convex-shape claim Wiggers describes on the participant's actual stress range; r1 drafted `4db3b30` → audit PASS-with-caveats `6bf21f7` → r2 §3.6-compression `c0148ca`. **4-cell agreement matrix** between HA-C3 v2 and HA-C3p defines the cross-test reading (lives in HA-C3p result.md §6 open-questions). Both share §4.5 3-condition gated verdict + §5.A unmedicated-headline + §5.B dose-adjusted cross-phase sensitivity per [`citalopram_phase_stratification §4`](methodology/citalopram_phase_stratification.md#4-per-channel-inheritance-rules) CONFIRMED-channel inheritance for `all_day_stress_avg`. Test execution is separate post-lock sessions. | NL | `all_day_stress_avg`, `gevoelscore` ready |
| **C4** (3-channel stress decay triad) | source-verified; Wave 4 operationalised; decay + walls + t+1 reactivity all three channels measurable. **HA-C4 v2 r2 LOCKED 2026-06-18** (`b0f38a7`) → tested 2026-06-18 (`52bddb5`) → **REJECTED at triad-aggregation level** (validate Ch1+Ch2 SUPPORTED; train REFUTED; daily-aggregate is wrong instrument for within-day-recovery claim — see [`reviews/HA-C4-v2-2026-06-18.md`](reviews/HA-C4-v2-2026-06-18.md) + [`analyses/hypotheses/HA-C4/result.md`](analyses/hypotheses/HA-C4/result.md)). **Bout-level pivot landed via HA-C4c sister pre-reg**: **HA-C4c r2 LOCKED 2026-06-23** `4e666a2` (Option γ canonical 4-stage: r1 `d59352c` → audit REVISION-RECOMMENDED `5f79bd1` → r2 substantive absorb `310e145` → fresh-session re-audit clean → LOCK) → **tested 2026-06-23 → PARTIAL** at [`analyses/hypotheses/HA-C4c/result.md`](analyses/hypotheses/HA-C4c/result.md) `a69a8ed`. Configuration: bar (a) discrimination PASS (p=0.0001, n_heavy=465 / n_non_heavy=809 cross-phase-pooled) + bar (b) effect-size FAIL (Cliff's δ=+0.120 vs threshold ≥+0.20, 95% CI [+0.064, +0.178]); direction positive (heavy-T > non-heavy-T). **Inverse failure-mode vs HA11-bout-redo PARTIAL** — the materially-larger cross-phase-pooled n removed HA11-bout-redo's bar-3 power-shortfall constraint, exposing a real but small-magnitude effect (weak-effect-but-real positive pattern per §9.2 second config). Unmedicated-only stratum (n=183/323) REJECTED at δ=+0.059 — stratum-fragility per §9.5 (cross-phase pooling is load-bearing for the substantive signal). Motion-clean-only REJECTED at near-zero δ — 99.3% motion-confound corpus-property reaffirmation per §8 caveat 4 (32/4317 bouts motion-clean; signal lives entirely in motion-tagged bouts). Transient-excluded + baseline-invalid-excluded both PARTIAL consistent; crash-drop |Δ δ|=0.015 CLEAN; Approach A all 3 sub-arms PARTIAL (no β-precision-fragility). Holm step-down primary + transient-excluded Holm-rejected at adj_p=0.0004. v2 daily-aggregate REJECTED + HA-C4c bout-level PARTIAL coexist (per §8 caveat 9). | WE | `stress_post_peak_time_to_rest_min`, `stress_high_duration_min`, `awake_stress_avg` ready; `bout_n_did_not_return_day` per-day ready; pipeline `extract_stress_bouts.py` `d5b394c` smoke-tests PASS at run-time |

### Tier 2 — source-verified + family history requires acknowledgement

| ID | why (class) | family history | stop rule (per constraint 8) |
|---|---|---|---|
| **A1** (RHR dose-scaling with exertion; demoted from Tier 1 on 2026-06-14) | source-verified (PDF 165-177, 308-315); Jonckheere-Terpstra ordinal test on quartiles is a genuinely different operationalisation from the shock-detection HA01 family. Class: DR | HA01 / HA01b / HA01b-recomputed / HA02 / HA02b / HA02c all NULL on lagged baseline ([`REJECTED.md`](REJECTED.md)); HA01c SUPPORTED both eras but diagnostic AMBIGUOUS, load-bearing withheld | if A1 NULLs, no further A-block dose-response variants on this corpus without new independent prior (A1 is the last legitimate ordinal-dose-response operationalisation of Wiggers' RHR dose-scaling claim) |
| **A4** (sustained multi-hour RHR elevation) | source-verified; Wave 4 v3 operationalised; Flack-via-Wiggers threshold anchor (+20 bpm × 30 min). Class: WE | sensitivity ladder duration × offset cells already defined; no direct family overlap | none (operationalisation is novel relative to HA01-HA02c shock-detection framings) |
| **B1** (single-day proxy spike → crash at t+1; demoted from Tier 1 on 2026-06-14) | source verification queued (Bucket B.1 of execution plan); spike-detection operationalisation is tighter than HA07c's mean-delta and looser than H02b's per-minute count. Class: CCF | HA07c (sleep-stress-mean delta) NULL both eras; H02b (per-minute stress spike count) train SUPPORTED + validate near-miss, overall NULL — `stress_mean_sleep` family has been tested twice ([`REJECTED.md`](REJECTED.md)) | if B1 NULLs, the `stress_mean_sleep` proxy-family is exhaustively tested (HA07c + H02b + B1 = three operationalisations of the same column family with three different temporal granularities) |
| **H5** (per-metric lag-profile ordering BB/stress ≤ RHR < HRV) | source-verified; ordering claim robust to chaining. Class: CCF | partial — the `lag_profile_report.md` activity-labels output covers HA01 exertion axes only; per-channel autonomic lag profiling missing (queued as Q15 in [`methodology/queued_work.md`](methodology/queued_work.md)) | none directly; per-channel lag profiling (Q15) is the descriptive prereq |

### Tier 3 — descriptive pass needed BEFORE pre-reg

| ID | why descriptive first | descriptive work needed |
|---|---|---|
| **G3** (barometric pressure × headache) | **parked 2026-06-14 — see [`methodology/queued_work.md`](methodology/queued_work.md) Q18 for the two-path workflow (KNMI external vs Garmin on-device) + descriptive prereqs.** Out of active scope while Tier 1 (C3 + C4 first; A1 + B1 with revised priors) progresses. | join pressure data (path 1 or 2 per Q18), characterise correlation with `gevoelscore` + `cat_sub_hoofdpijn`, run crash-distortion sensitivity row per [[feedback_crash_distortion_sensitivity]] |
| **H1** (Wiggers-faithful: HRV leads gevoelscore crash) | source-verified PARTIAL; the Wiggers-faithful arm is HRV-specific (blocked on FR245). The non-HRV extension (any wearable signal leads crash) is supported by the HA01b 4-day lag finding, but that's our extension not Wiggers — belongs in the Personal register, not as a Tier 1 Wiggers promotion | (a) HRV-enabled device for the Wiggers-faithful arm, or (b) accept that the non-HRV arm is a Personal-register P-entry, not a Wiggers H1 promotion |
| **H4** (parasympathetic swing) | source-grounded BB-anchored framing + descriptive d = +0.47 on `stress_stdev_sleep`. But [cross-channel-correlation.md](analyses/garmin_exploration/cards/cross-channel-correlation.md) shows HA10 (morning BB peak) ≡ −HA07c (sleep stress mean) at ρ = −0.922 — the "BB-specific signal" framing assumes a channel independence the data refute | reframe H4's operational test around the BB-stress collinearity: which composite of the joint autonomic-state signal captures the parasympathetic-swing pattern Wiggers describes? Descriptive pass needed before any pre-reg |

### Out of priority (available for opportunistic pre-regs)

A2, A3, B2-B5, C1, C2, D1-D5, E1-E3, F1, F2, F4, G1, G4, H2 (counting), H3 (illness/PEM classifier) — weaker source-verification + no descriptive support yet. Move to a higher tier only when (a) source verification confirms a verbatim Wiggers claim AND (b) descriptive evidence emerges on this corpus.

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

The bridge from this column-selection layer to the **statistical method per Wiggers claim type** (CCF lead-lag / within-event / dose-response / non-linearity) lives in
[`methodology/wiggers_test_design_on_chained_regime.md`](methodology/wiggers_test_design_on_chained_regime.md).
That methodology doc holds the four operationalization classes,
the faithfulness rubric per class, and the chained-regime adjustments
that propagate through every pre-reg downstream.

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
| A1 | `resting_hr` deviation vs rolling 28d median | `is_crash` (peri-event window) | **primary**: RHR deviation at `t0` stratified by `exertion_rank_composite_lagged_lcera` quartile (Jonckheere-Terpstra dose-response). **secondary (exploratory)**: peri-event alignment `t-3 … t+3` — Wiggers does not explicitly claim a t-3…t-1 RHR precursor; precursor claims belong with B4/D5/H4 (parasympathetic swing). See verification log | ✅ |
| A2 | `\|resting_hr − rolling_28d_median\|` | `gevoelscore` | correlation; allow both-direction deviation | ✅ |
| A3 | `resting_hr` (already sleep-derived per Garmin) | `is_crash` / `gevoelscore` | peri-event alignment from `t-2` | ✅ |
| A4 | **for PEM-pacing**: `hr_sustained_elevated_flag_lcera` (primary categorical), `hr_longest_elevated_run_min_waking_lcera` (primary continuous), `hr_area_above_daytime_baseline_waking_lcera`. **for cross-era trajectory**: drop `_lcera` suffix. Transparency: `hr_median_waking`, `hr_daytime_baseline_lagged[_lcera]` | `is_crash` next-day / current-day | cross-tab on the flag; regression on the continuous variants; A4 baseline = `[d-90, d-30]` lagged median of `hr_median_waking` + 20 bpm offset (v3 locked 2026-06-12; v1's resting_hr + 15 threshold was superseded same day for being too lenient) | ✅ (operationalised Wave 4 v3) |

### B. HRV — PARTIAL via `stress_mean_sleep` proxy on descriptive grounds (revised 2026-06-13)

**Framing**: HRV Status is hardware-blocked on FR245 / Elevate V3.
The `stress_mean_sleep` column is HRV-correlated under the Firstbeat
algorithm (sleep-window collapses the multivariate composite toward
HRV-derived component). **Descriptive characterisation** confirms the
proxy direction: episode-level Cohen's d = +0.90 with mean stress-unit
difference +4.66, CI95 [+1.51, +8.22] on the mean difference (not on
d itself; d has no reported CI in the descriptive run) on crash
episodes; Pearson r = +0.342 with `resting_hr` (R² = 0.117 → the two
channels are substantially distinct). Each B-hypothesis below
uses `stress_mean_sleep` as the candidate HRV-proxy channel.
Channel selection (single vs multi) is a per-hypothesis pre-reg
choice. See
[`methodology/hrv_proxy_via_stress.md`](methodology/hrv_proxy_via_stress.md)
for derivation and limits.

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| B1 | `stress_mean_sleep(t) − rolling_28d_median` spike (proxy for "HRV drop"); spike threshold calibrated from descriptive characterisation (Wiggers' "≥10 HRV points" doesn't translate to stress units) | `is_crash(t)` and `is_crash(t+1)` | peri-event window around crash_v2 episode starts; sensitivity + specificity at the calibrated threshold | ⚠️ — testable via proxy; literal "HRV-point drop" anchor not reproducible |
| B2 ⚠️ | rolling 7d `stress_mean_sleep` mean across `t-7 … t-1` peri-event window; trend slope per day | `is_crash` episode start at `t` | regression: slope of rolling mean vs crash start; report direction + magnitude. Wiggers-faithful direction: monotone rising rolling stress (= proxy for monotone falling rolling HRV) | ⚠️ — testable via proxy; directional only |
| B3 | rolling 28d `stress_mean_sleep` baseline trajectory (falling = improving per the proxy inverse) | rolling 28d crash rate (`is_crash` mean) | rolling-window correlation; report as descriptive trend within the LC era, NOT as an analytical era split | ⚠️ — testable via proxy; absolute-HRV anchor lost |
| B4 ⚠️ | `stress_mean_sleep` negative outlier (= HRV positive outlier proxy, the parasympathetic-swing signature) conditional on `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on `t-1` | `is_crash` at `t+1` and `t+2` | conditional contingency: P(crash given negative-outlier sleep-stress ∧ prior-day overexertion) vs base rate. Composite signature also tracked in H4 | ⚠️ — testable via proxy; B4 is the "outlier" framing, H4 is the "composite" framing |
| B5 | same proxy as B1, conditional on illness labels (acute-illness-onset days from `triage_events.csv` `categorie=ziek` or similar tag) | `is_crash` at `t` (illness-onset day) | conditional contingency: does sleep-stress drop (proxy for HRV rise) before illness onset, distinct from the rise-before-crash pattern? | ⚠️ — testable via proxy; depends on cleanly-labeled illness-onset days |

**Pre-reg-file constraints (all B-block — apply identically to HRV-dependent parts of H1/H2/H3/H4/H5)**:

1. **Explicit proxy framing**: each pre-reg file MUST state "this test is on the `stress_mean_sleep` proxy, not on HRV proper."
2. **Descriptive effect-size anchor**: episode-level Cohen's d = +0.90; mean stress-unit difference +4.66, CI95 [+1.51, +8.22] on the mean difference (d itself has no reported CI in the descriptive run). This is the same-day reference for power planning. Smaller effect sizes expected for lead-lag claims.
3. **Validation framework**: per [`methodology/train_validate_split_fate.md`](methodology/train_validate_split_fate.md), new pre-regs use full Stratum 4 (LC with gevoelscore + crash labels, per [`methodology/lc_era_temporal_segmentation.md`](methodology/lc_era_temporal_segmentation.md)) as a single pool for primary inference. The historical 2023-12-31 train / validate split is preserved as reproducibility artefact for HA01b / HA02c only — NOT used as primary for new pre-regs. An optional M3 descriptive overlay (train-era vs validate-era discrimination) may be reported, but cannot claim per-portion verdicts; under the overlay, train-vs-validate divergence is a number, not a narrative.
4. **Channel selection is a per-hypothesis pre-reg choice**: descriptive r = +0.342 between `stress_mean_sleep` and `resting_hr` shows the channels are distinct enough that single-vs-multi-channel framing is a legitimate hypothesis-by-hypothesis choice. Do NOT lock framing globally.
5. **Wiggers UI anchors do not translate**: specific HRV-unit thresholds (e.g. "≥10 HRV-point drop") are calibrated from descriptive characterisation on the proxy scale.
6. **No literal HRV claim**: pre-reg conclusions defend the proxy-tested claim ("sleep-stress elevates around crashes"), not Wiggers' verbatim claim ("HRV drops before PEM").
7. **Crash-drop sensitivity row**: per CONVENTIONS §3.4 and [[feedback_crash_distortion_sensitivity]], the pre-reg's result table includes the discrimination / correlation / dose-response statistic computed with `is_crash == True` rows dropped alongside the full-frame statistic; |Δ| > 0.10 is surfaced as a finding rather than buried in a sensitivity appendix. The exertion × resting_hr Spearman swings from ~+0.0 to ~+0.4 when crash days drop on this corpus — the failure mode is real for any test touching the exertion or RHR signal families.
8. **Prior test family acknowledgement**: if the hypothesis touches a signal family with existing HA-test verdicts in [`REJECTED.md`](REJECTED.md), the pre-reg includes a section citing the relevant entries and explaining why this specific operationalisation is informative beyond what the family already tested. "Different statistical method on the same signal" or "different baseline construction" are legitimate; "let's try another variant after the last one failed" is not. Tier 2 entries in the priority shortlist (A1, B1) carry an explicit stop-rule in their pre-reg per the shortlist's stop-rule column.
9. **Operationalisation precision**: the pre-reg's operationalisation walks the [chained-regime doc](methodology/wiggers_test_design_on_chained_regime.md)'s per-class faithfulness rubric AND the elegant-vs-coarse dimensions: window selection (ACF-derived or sensitivity-laddered, not fixed-by-convention); signal reduction (continuous where the signal is continuous); threshold choice (sensitivity ladder, not single τ); test family (robust, distribution-free); verdict shape (shape + CI, not binary pp-bar only); temporal structure (preserved, not collapsed); multi-channel (triad or composite where the source claim spans channels); functional form (explicit linearity test, not assumed); effect-size grounding (standardised effect size + descriptive reference). Documented in the pre-reg's "Operationalisation choices" section with a one-sentence justification per dimension.

### C. Stress score

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| C1 | `stress_mean_sleep` (FIT-derived sleep mean) as proxy for "night orange"; secondary: `stress_high_duration_min` during waking-window peri-event window | `is_crash` from `t-1` | peri-event alignment | ✅ — "% orange specifically" would need a finer FIT re-walk; proxy is adequate for v1 |
| C2 | `all_day_stress_avg` (TOTAL aggregator) | `bb_overnight_gain` (paired-night) AND `gevoelscore` next-day | two-stage correlation | ✅ |
| C3 | `all_day_stress_avg` (binned at 0-20, 20-30, 30-40, 40-60, 60+) | `gevoelscore` | binned mean comparison or natural-spline regression; **NOT linear correlation** (the hypothesis itself rejects linearity) | ✅ |
| C4 | **primary**: `stress_post_peak_time_to_rest_min` (NaN-on-failure = C4-positive), `stress_post_peak_drop_avg`. **secondary (walls)**: `stress_high_duration_min` on T (Wiggers: "complete walls of orange"). **secondary (t+1 reactivity)**: `awake_stress_avg` on T+1 (Wiggers: "the day after you've done too much you can see stress spikes much faster, despite resting"). All conditioned on `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T | within-day decay (primary) + within-day walls + next-day reactivity | stratified comparison on each metric: heavy days vs non-heavy days | ✅ (operationalised Wave 4; expanded 2026-06-12 to add walls + t+1 per source — see verification log) |
| C4b | **primary**: `stress_low_motion_min_count_S60_Mlow` (per-day count of minutes where `stress >= 60` AND Garmin intensity-class ≤ 1, OR no intensity record covers the minute); conditioned on `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T or T-1. Per-minute step counts are NOT in monitoring_b — see [`methodology/stress_low_motion_primitive.md` §3.1](methodology/stress_low_motion_primitive.md). Spec text revised 2026-06-15 (was "`steps_per_minute <= 5`"). | `is_crash` at t+1 (primary); dip secondary | frequency comparison: heavy-exertion crash vs heavy-exertion non-crash days; Wilson CI + Cohen's d; sensitivity ladder on {stress 50/60/75} × {strict/low/below_mod motion class} = 9 columns; respiration companion columns (`n_minutes_resp_above_18`, `n_minutes_resp_in_rest_band_10_18`) as orthogonal covariates | 🆕 primitive extracted 2026-06-15 (Session E); methodology + extraction script live; **v3 LOCKED 2026-06-17 commit `32ba3b9`; test-executed 2026-06-17 commit `df05e83` → NOT-SUPPORTED** on the locked headline cell (unmedicated × train+validate pooled × S60_Mlow × N_std=1.5 × primary 4d × one-sided elevated). Pooled n=10 (8 train + 2 validate); (a) 40% FAIL, (b) -10pp FAIL, (c) +1.21 PASS; train-only (a)=50%, validate-only (a)=0%; LOO k=4 below boundary; 0 load-bearing. See [`HA-C4b/result.md`](analyses/hypotheses/HA-C4b/result.md). v3 §9 NOT-SUPPORTED branch holds two alternatives open: lived rest-stress trigger may be PROTECTIVE-not-PREDICTIVE; or admitted crashes may be emotionally/cognitively triggered (the v3 §8 pacing-behaviour confounder). v2 archived at [`HA-C4b/hypothesis-v2-archived.md`](analyses/hypotheses/HA-C4b/hypothesis-v2-archived.md) (v2 INCONCLUSIVE at 2026-06-16 commit `83a64b2`; dry-run/full-run gate asymmetry was the v3 trigger). v1 locked + dry-run halted 2026-06-15, archived at [`HA-C4b/hypothesis-v1-archived.md`](analyses/hypotheses/HA-C4b/hypothesis-v1-archived.md). Per v3 §3.8 gate 3 the register row is generic at the headline-cell level — non-supersession across v2 → v3 (folder pointer, not revision pointer); the operational anchor + caveats below are not superseded. |

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

### H. Mechanism & lead/lag — PARTIAL under proxy framing on descriptive grounds (revised 2026-06-13)

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| H1 ⚠️ | **Wiggers-faithful proxy channel**: `stress_mean_sleep` deviation vs personal rolling baseline (HRV-proxy on descriptive grounds, d = +0.90 episode-level). **Wiggers-extension channels**: `bb_overnight_gain`, `resting_hr` deviation. Channel selection (single vs multi) is a pre-reg choice | `gevoelscore` (the "felt" crash) | cross-correlation lag profiles per metric: peak-ρ lag for each channel; significance via permutation. Stationarity: first-difference series before CCF | ⚠️ — Wiggers' literal HRV-Status-leading claim is tested via the stress proxy (descriptive d = +0.90 anchor; literal HRV-unit anchor not reproducible) |
| H2 ⚠️ | "activity-invisible" defined as `step_rank_lagged < 0.3` AND `max_hr_rank_lagged < 0.3` AND no `hr_sustained_elevated_flag`; confirming signal under proxy: `stress_mean_sleep` outlier on same day | `is_crash` | fraction of crashes meeting the activity-invisible criterion AND showing sleep-stress outlier as confirming signal (Wiggers Mental PEM claim PDF lines 1448-1457) | ⚠️ — proxy upgrades the "HRV-drop on same days" subclause to a stress-derived sleep-stress spike test |
| H3 ⚠️ | `resting_hr`, `bb_charged_24h`/`bb_drained_24h`, `respiration_avg_sleep`, **`stress_mean_sleep`** (added as HRV proxy) — pre-crash signatures; outcome: pre-labeled illness vs PEM | classifier (logistic / RF) trained on the per-day vectors | testable on the labeled subset; sleep-stress proxy partially fills the HRV-discriminative role per Wiggers; temp still blocked | ⚠️ — partial; expect reduced separability vs Wiggers' full HRV + temp signature |
| H4 ⚠️ | **Primary (BB-anchored composite — source-grounded)**: `bb_sleep_end_value` high + `bb_drained_24h` high after `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on `t-1`. Wiggers' parasympathetic swing chapter (PDF lines 1431-1457) directly cites the BB-drop pattern, so the BB-anchored framing is source-grounded independent of any RHR claim. **Secondary (proxy)**: `stress_mean_sleep` negative outlier (= HRV positive outlier proxy per B4) on the swing night. **Exploratory**: `resting_hr` ↓ on the swing night | `is_crash` at `t+1` and `t+2` | conditional contingency on the composite signature; sensitivity + specificity | ⚠️ — was BLOCKED; reclassified PARTIAL 2026-06-13 on descriptive + source grounds. Composite framing leans on BB columns (Wiggers-cited) and the stress proxy (descriptive crash-shift). Pre-reg should not claim Wiggers' literal HRV+RHR signature is being tested — only a BB-anchored analogue with sleep-stress as HRV proxy. Channel selection is a pre-reg choice |
| H5 ⚠️ | per-metric cross-correlation vs `exertion_rank_composite_lagged_lcera` | each metric's lag profile | cross-correlation per: `resting_hr`, `stress_mean_sleep` (HRV proxy), `bb_overnight_gain`, `gevoelscore`. Stationarity: first-difference. Bootstrap CI on lag-of-peak-ρ per channel | ⚠️ — full lag map per Wiggers includes HRV; the proxy `stress_mean_sleep` substitutes for HRV. Lag profile for HRV-proxy is a research finding even if it differs from Wiggers' implicit ordering |

### I. Data-quality / methodology

| ID | predictor(s) | outcome | test method | status |
|---|---|---|---|---|
| I1 | re-run any primary test excluding the first 21 days of `has_garmin_uds=True` coverage | same outcome as the original test | sensitivity comparison | ✅ |
| I2 | no device change in this dump — fr245 / serial 3377851255 throughout 2021-08-16 → today | — | — | N/A on this dataset |
| I3 | confirm overlap: gevoelscore from 2022-09-03, Garmin metrics from 2021-08-16, rich metrics (sleep stages, BB stat list) from various dates onward | per-column `coverage` in DATA_DICTIONARY | already documented per column | ✅ already done — see DATA_DICTIONARY § per-column coverage |

### Summary: what survives, what doesn't (revised 2026-06-13)

| category | testable count | blocked count | partial count |
|---|---|---|---|
| A | 4 | 0 | 0 |
| B | 0 | 0 | **5** (was 5 blocked; unblocked via `stress_mean_sleep` proxy on descriptive grounds 2026-06-13) |
| C | 4 | 0 | 0 |
| D | 5 | 0 | 0 |
| E | 3 | 0 | 0 |
| F | 3 | 1 (F3 — skipped) | 0 |
| G | 2 | 1 (G2 hardware) | 1 (G3 external) |
| H | 0 | 0 | **5** (was 1 blocked + 4 partial; H4 reclassified to partial via BB-anchored source-grounded composite 2026-06-13) |
| I | 2 | 0 | 0 (I2 N/A) |
| **total** | **23** | **2** | **11** |

23 hypotheses are pre-registration-ready on the current 161-column
master. 11 more are partially testable (5 B-block via the
`stress_mean_sleep` proxy on descriptive grounds; 5 H-block via mixed
proxy + non-HRV channels; 1 G3 pending external KNMI data). Only 2
remain blocked: F3 (Garmin sleep score, skipped per user) and G2
(skin temperature, sensor not present on FR245). See
[`methodology/hrv_proxy_via_stress.md`](methodology/hrv_proxy_via_stress.md)
for the proxy framing and
[`methodology/garmin_indicators_audit.md`](methodology/garmin_indicators_audit.md)
§ HRV for the audit verdict that authorises the B-block + H4 reclassification.

**Pre-reg-file constraints for partial-via-proxy hypotheses (B1-B5, H1, H2, H3, H4, H5):**

1. **Explicit proxy framing**: each pre-reg file must state that the
   test is on the `stress_mean_sleep` proxy, not on HRV proper.
2. **Descriptive effect-size anchor**: episode-level Cohen's d = +0.90;
   mean stress-unit difference +4.66, CI95 [+1.51, +8.22] on the mean
   difference (d itself has no reported CI in the descriptive run).
   This is the same-day reference for power planning. Smaller effect
   sizes expected for lead-lag claims.
3. **Validation framework**: per [`methodology/train_validate_split_fate.md`](methodology/train_validate_split_fate.md),
   new pre-regs use full Stratum 4 as a single pool for primary
   inference; the historical 2023-12-31 split is preserved as
   reproducibility artefact for HA01b / HA02c only. Optional M3
   descriptive overlay (train-era vs validate-era) may be reported
   but cannot claim per-portion verdicts; under the overlay,
   train-vs-validate divergence is a number, not a narrative.
4. **Channel selection is a per-hypothesis pre-reg choice**: descriptive
   r = +0.342 between `stress_mean_sleep` and `resting_hr` shows the
   channels are distinct enough that single-vs-multi-channel framing
   is a legitimate hypothesis-by-hypothesis choice. Do NOT lock framing
   globally.
5. **Wiggers UI anchors do not translate**: specific HRV-unit thresholds
   (e.g. "≥10 HRV-point drop") are calibrated from descriptive
   characterisation on the proxy scale.
6. **No literal HRV claim**: pre-reg conclusions defend the
   proxy-tested claim, not Wiggers' verbatim claim.
7. **Crash-drop sensitivity row**: per CONVENTIONS §3.4 and
   [[feedback_crash_distortion_sensitivity]], the pre-reg's result
   table includes the discrimination / correlation / dose-response
   statistic computed with `is_crash == True` rows dropped alongside
   the full-frame statistic; |Δ| > 0.10 is surfaced as a finding.
   The exertion × resting_hr Spearman swings from ~+0.0 to ~+0.4 when
   crash days drop on this corpus.
8. **Prior test family acknowledgement**: if the hypothesis touches a
   signal family with existing HA-test verdicts in
   [`REJECTED.md`](REJECTED.md), the pre-reg includes a section citing
   the relevant entries and explaining why this specific
   operationalisation is informative beyond what the family already
   tested. Tier 2 entries (A1, B1) carry an explicit stop-rule in their
   pre-reg per the shortlist's stop-rule column.
9. **Operationalisation precision**: the pre-reg's operationalisation
   walks the [chained-regime doc](methodology/wiggers_test_design_on_chained_regime.md)'s
   per-class faithfulness rubric AND the elegant-vs-coarse dimensions:
   window selection (ACF-derived or sensitivity-laddered); signal
   reduction (continuous where the signal is continuous); threshold
   choice (sensitivity ladder, not single τ); test family (robust,
   distribution-free); verdict shape (shape + CI, not binary pp-bar
   only); temporal structure (preserved, not collapsed); multi-channel
   (triad or composite where the source claim spans channels);
   functional form (explicit linearity test, not assumed); effect-size
   grounding (standardised effect size + descriptive reference).
   Documented in the pre-reg's "Operationalisation choices" section
   with a one-sentence justification per dimension.

---

## Source verification log

Started 2026-06-12; updated as paraphrases are verified against `docs/research/literature/wiggers_pacing_handleiding.pdf` (local-only, gitignored). Hypotheses without a verification entry have not yet been source-checked.

Line numbers refer to the `pdftotext -layout` extraction at `C:\tmp\wiggers_pacing_handleiding.txt` (86-page PDF, 2257 lines).

### A1 — RHR during crash episodes; dose-scaling

**Verified 2026-06-12, batch 1.**

Wiggers passages:
- *"This could mean the activity you did just before you rested was too much. Sometimes your heart rate drops to your correct resting heart rate after a few minutes, but if you've pushed yourself much too far, it can take hours. I'm already unhappy with a resting heart rate that's 5–10 beats higher. I have really thoroughly overdone it when my resting heart rate is a 100 bpm instead of 60 for hours."* (PDF lines 165-177)
- *"If it's higher or lower than normal, it could be a sign that you've done too much or are experiencing a PEM."* (PDF lines 308-315, Nighttime heart rate)

Findings:
- **DROPPED** "just before crash days" framing from the original A1 description. The precursor framing was OUR extrapolation from the false-energy passage (PDF lines 117-126), which is about HRV/parasympathetic swing, not RHR. Precursor claims belong with B4/D5/H4.
- **KEPT** RHR-elevation-responds-to-exertion direction (the CCF/regression sub-claim) — directly sourced (PDF lines 165-177).
- **KEPT** dose-scaling (Jonckheere-Terpstra sub-claim) — directly sourced via Wiggers' personal ladder: 5-10 bpm = "unhappy", 100 vs 60 = "thoroughly overdone".
- Bidirectional RHR claim (*"a lower RHR can also be a signal... happens immediately after too much movement"*, PDF lines 192-197) is correctly preserved in A2 as a separate hypothesis.
- Peri-event `t-3 … t+3` window kept as **exploratory** secondary, not as a primary Wiggers-claim test.

### A4 — Sustained multi-hour RHR elevation marks real overexertion

**Verified 2026-06-12, batch 1.**

Wiggers passages:
- *"Sometimes your heart rate drops to your correct resting heart rate after a few minutes, but if you've pushed yourself much too far, it can take hours."* (PDF lines 168-172)
- *"the resting heart rate remained too high all day"* (PDF lines 243-247, shower example)
- *"The heart rate and stress remained high for hours despite lying down and trying to relax. After two hours of this, the person felt very grumpy and exhausted."* (PDF lines 250-256)
- *"The Garmin heart rate graph shows the average over two minutes. That's why you won't find high peaks in your Garmin heart rate overview."* (PDF lines 257-261)
- A. Flack (cited by Wiggers, PDF lines 527-554, ref: https://paradoxfloss.gumroad.com/l/belowthethreshold): *"limit your heart rate to no more than 15-20 points above your resting heart rate."*

Findings:
- **KEPT** the multi-hour-vs-brief-spike distinction — exact match (PDF lines 168-172, 250-256).
- **THRESHOLD ORIGIN**: `+20 bpm` cutoff is Flack-via-Wiggers (PDF lines 527-554), not pure researcher convention. The "15-20 points above RHR" rule is Flack's; we use the upper end. Mark this in any methodology footnote.
- **DURATION CONVENTION**: `30 min` is operational convention; Wiggers consistently uses "hours" / "all day" framing. **Sensitivity ladder recommended in pre-reg**: duration {30, 60, 120 min} × offset {+10, +20, +30 bpm}. If A4 only fires at +20 bpm / 30 min but not at the surrounding cells, the result is brittle.
- **SMOOTHING CAVEAT**: Garmin per-minute HR is already 2-min averaged at source (PDF lines 257-261). The "30 min sustained" framing is therefore "30 min of sustained-after-Garmin-smoothing", not raw beat-level sustained. Note this in the methodology.

### B1 — Day-over-day HRV drop predicts crash (proxy-substituted to sleep-stress)

**Verified 2026-06-14, batch 4 (single-entry).**

Wiggers passages:
- *"The dutch fatigue clinic is said to maintain that a decrease of 10 HRV points compared to the previous day could indicate PEM."* (PDF lines 920-924, Decreasing HRV section). The literal "10 HRV points" threshold is **Dutch-fatigue-clinic-via-Wiggers, not pure Wiggers convention**.
- *"With PEM, you often see that HRV drops after several days of overexertion. This happens even if the person rested well immediately after the overexertion."* (PDF lines 924-928). Distinguishes the multi-day drop (closer to B2) from the single-day drop (B1).
- *"It's helpful to click the 'Overnight Averages' button in your 4-week overview. This will help you see if your HRV suddenly drops significantly. This can help you predict whether you're going to have a PEM or determine whether it would be wise to take it easier."* (PDF lines 956-964, Overnight Averages section). The explicit predictive claim that anchors B1's "predicts a crash at t / t+1" framing.
- *"If your HRV slowly decreases and you know you've been demanding a lot from your body for a while, you can also take that as a sign to take it easier."* (PDF lines 965-969). Supplementary; speaks to the slow-decrease pattern (closer to B2 / B3) rather than the single-day drop.
- *"Your average overnight HRV shows you how the previous day impacted your health. It can fluctuate significantly."* (PDF lines 916-919). Establishes the day-over-day comparison frame Wiggers uses throughout the HRV chapter.

Findings:
- **KEPT** day-over-day single-day-drop framing — directly sourced (PDF lines 920-924). B1's "single-day proxy spike → crash at t+1" matches Wiggers' "decrease of 10 HRV points compared to the previous day could indicate PEM".
- **KEPT** the predictive claim — Wiggers' explicit "can help you predict whether you're going to have a PEM" (PDF lines 962-964) directly motivates B1's t+1 outcome framing.
- **KEPT** same-day plus next-day outcome (B1 tests both `is_crash(t)` and `is_crash(t+1)`) — Wiggers' framing covers both "indicate PEM" (same-day detection: lines 920-924) and "predict whether you're going to have a PEM" (next-day prediction: lines 956-964).
- **DROPPED** the literal "≥10 HRV points" threshold — explicitly noted in B1's register row and in the proxy constraint blocks (constraint #5 "Wiggers UI anchors do not translate"). The anchor is in HRV-point units (Garmin's normalised HRV scale), not in `stress_mean_sleep` units; threshold must be calibrated from descriptive characterisation on the proxy scale. The "10" magnitude itself is Dutch-fatigue-clinic-via-Wiggers (lines 920-924), not a Wiggers-derived number, and does not translate dimensionally to the proxy scale.
- **EXPANDED** proxy substitution — Wiggers' claim is HRV-specific; B1 tests via `stress_mean_sleep` (descriptive-grounded proxy per [`methodology/hrv_proxy_via_stress.md`](methodology/hrv_proxy_via_stress.md)). The PARTIAL classification of B1 in the register reflects that the literal Wiggers HRV claim cannot be tested on FR245.
- **EXPANDED** crash labels — Wiggers uses "PEM" as the outcome; B1 uses `is_crash` (crash_v2) as the operational outcome. The label-source asymmetry between self-report (crash_v2) and Wiggers' Garmin-pattern-derived PEM labels is the cross-source-validation question queued as Q9 in [`methodology/queued_work.md`](methodology/queued_work.md).

Side notes:
- **Multi-day-drop pattern is B2, not B1**: Wiggers' "drops after several days of overexertion" (PDF lines 924-928) describes a multi-day decline that maps to B2 (monotone HRV decline across peri-crash window), not B1 (single-day drop). B1 verification kept tight to the single-day-drop claim per its register row.
- **Dutch fatigue clinic anchor provenance**: the "10 HRV points" threshold has a clinical origin (Dutch fatigue clinic; specific clinic name not given in the Wiggers PDF). Worth noting in the B1 pre-reg's source-anchoring section that the magnitude anchor is borrowed not Wiggers-original. The same clinic citation appears in the H1 verification log entry; both H1 and B1 share this Wiggers passage but operationalise different aspects of it (H1: leading-vs-coincident question; B1: single-day-drop magnitude calibration).
- **Family-history acknowledgement (per constraint 8)**: B1 pre-reg must cite [REJECTED.md](REJECTED.md) rows `HA07c` (sleep stress mean delta NULL both eras under proxy framing) and `H02b` (per-minute spike count, train SUPPORTED + validate near-miss, overall NULL by both-eras rule) as the prior `stress_mean_sleep` family tests. B1 is the third operationalisation on the same column family with the third temporal granularity (sleep-window daily spike vs HA07c's daily mean-delta vs H02b's per-minute count). The Tier 2 stop-rule already names this exhaustive-three condition.

### C3 — Non-linear / convex stress→fatigue

**Verified 2026-06-12, batch 2.**

Wiggers passages:
- *"Your annual stress overview includes a stress score line. If you've paid attention to your own stress scores, you might know that a day with a score of 40 is much more tiring than a day with a score of 30. Such a step appears very small on the graph, but it isn't. This graph shows a kind of stair step. This person has overexerted themselves and their health is deteriorating as a result."* (PDF lines 1357-1368, Annual Stress Scores)

Findings:
- **VERBATIM MATCH**. The "30 → 40 step costs more than it looks" framing in our hypothesis is taken directly from Wiggers' Annual Stress Scores section. No drift.
- **KEPT** operationalization unchanged: binned mean comparison (0-20, 20-30, 30-40, 40-60, 60+) and/or natural-spline regression on `gevoelscore = f(all_day_stress_avg)`. The pre-reg already explicitly rejects linear correlation, matching Wiggers' stair-step framing.
- **CONFIRMED outcome variable**: Wiggers' claim is `stress → fatigue` (tiring), so `gevoelscore` is the correct outcome (gevoelscore captures felt tiredness/sickness, monotonically inverted vs Wiggers' "tiring").
- The stair-step framing is qualitative in Wiggers — she does not specify spline knots or bin edges. Our binning (0-20, 20-30, 30-40, 40-60, 60+) is a reasonable operationalization but is OUR choice, not Wiggers'.

### C4 — Stress fails to drop during rest periods after overexertion ("stuck sympathetic")

**Verified 2026-06-12, batch 2.**

Wiggers passages:
- *"Going so far beyond your limits that your resting heart rate remains elevated and your stress level doesn't decrease for a long time & PEM"* (PDF lines 1140-1141, Walls of Stress causes list)
- *"The day after you've done too much you can see stress spikes much faster, despite resting"* (PDF lines 1141-1143, same list)
- *"Stuck in Stress. When you've done something and then lie down, you want to see blue again. Sometimes, usually when your nervous system is a bit unstable due to, for example, PEM or low blood volume, your stress remains high. The activity you did was probably too disruptive for how you were feeling at the time."* (PDF lines 1223-1231)
- *"It would be great if living a calmer life, pacing yourself better, and doing more relaxing things would instantly give you days full of blue. Unfortunately, that's not how it works. Usually, you have to take it easy for a while before your body finds its peace again."* (PDF lines 1306-1314)
- Adrenaline-lingers mechanism: *"Our theory is that the body produces too much adrenaline when overdoing things. Especially if you overdo it every day. It lingers for a long time."* (PDF lines 1316-1324)

Findings:
- **KEPT** primary metric `stress_post_peak_time_to_rest_min` — within-day post-peak recovery time is the central C4 claim, directly sourced (PDF lines 1140-1141, 1223-1231).
- **EXPANDED** to add **walls-of-stress** secondary: `stress_high_duration_min` on T captures the "complete walls of orange" pattern Wiggers describes (PDF lines 1112-1119) — a sustained-high-state metric distinct from decay-after-peak. Single-metric C4 missed this.
- **EXPANDED** to add **t+1 reactivity** secondary: `awake_stress_avg` on T+1 conditional on heavy exertion on T tests the explicit Wiggers claim *"the day after you've done too much you can see stress spikes much faster, despite resting"* (PDF lines 1141-1143). The original C4 only tested same-day decay.
- The adrenaline-lingers mechanism (PDF lines 1316-1324) is Wiggers' explanation, not a test — captured here as background, not as a separate hypothesis.
- C4 walls + t+1 reactivity push the metric coverage from 1 channel to 3 channels for the same underlying claim. Pre-registration should treat them as a confirmatory triad: pass-2-of-3 = C4 confirmed; pass-1-of-3 = partial; pass-0-of-3 = rejected.

### C4b — Stress-with-low-motion minute count (C4 with motion filter)

**Added 2026-06-14. NOT source-verified against the PDF** — this is a refinement of C4 with the participant's operational motion filter, not a separate Wiggers paraphrase. The Wiggers prior is C4's; the motion filter is the participant's contribution.

Origin:

- C4 (PDF lines 1140-1141, 1223-1231) covers "stress fails to drop during rest after overexertion" via stress-decay-failure metrics. C4b adds a **motion filter** to discriminate true sympathetic-arousal-during-rest from motion-artefact stress readings (Garmin stress is partly motion-sensitive; minutes with concurrent steps may inflate the stress signal without indicating sympathetic arousal).
- The motion filter is drawn from the participant's operational protocol (per [`methodology/garmin_pacing_practice.md` §3.3](methodology/garmin_pacing_practice.md#33-stress-when-at-rest)): the live rest-stress trigger requires both elevated stress AND clear-rest concurrency, not stress elevation alone.
- C4b was originally drafted as `personal_hypotheses.md` P5a; routed here 2026-06-14 per user-direction for unambiguous placement. Rationale: Wiggers C4 is the dominant prior; the motion filter is an operational refinement on the same shape, not a distinct theoretical claim.

Relationship to C4:

- Both test the same Wiggers claim ("stress fails to drop during rest after overexertion").
- C4 measures via stress-decay-failure aggregates (`stress_post_peak_time_to_rest_min` + walls + t+1 reactivity, conditioned on heavy exertion).
- C4b measures via per-minute count of stress-with-low-motion concurrence (also conditioned on heavy exertion).
- If C4b discriminates AND C4 does not, the motion filter is the relevant operational refinement. If both discriminate equally, the motion filter is incremental rather than essential. If only C4 discriminates, motion-coincident stress (regardless of motion-confound) is the discriminative signal.

Operational anchor:

- Predictor: per-day count of minutes with `stress >= 60` AND `intensity <= 1` (Garmin's sedentary/low classification) OR no intensity record. Primary column `stress_low_motion_min_count_S60_Mlow`, on T conditional on `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T or T-1.
- Outcome: `is_crash` at t+1 (primary); dip secondary.
- Sample: LC era (`date >= 2022-04-04`), heavy-exertion-conditioned subset.
- Sensitivity ladder: {stress threshold 50, 60, 75} × {strict_sedentary, low_or_below, any_below_moderate} = 9 columns. Plus respiration companion columns (`n_minutes_resp_above_18`, `n_minutes_resp_in_rest_band_10_18`) as orthogonal covariates.
- Sources: monitoring_b FIT files already parsed for HA11. **Primitive extracted 2026-06-15 (Session E)** by [`pipeline/01_extract/stress_low_motion_extract.py`](pipeline/01_extract/stress_low_motion_extract.py); methodology + four-input reasoning + FIT-data investigation (why per-minute steps were NOT used) in [`methodology/stress_low_motion_primitive.md`](methodology/stress_low_motion_primitive.md). Construct-validity check: Spearman ρ vs HA11 u_dip_count = 0.556 (moderate; information-additive, not redundant).
- **Dose-adjustment caveat for cross-phase tests**: per [`methodology/citalopram_phase_stratification.md §5.B`](methodology/citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests) C4b's raw stress threshold corresponds to different autonomic states across Citalopram-traject phases (β_dose for `all_day_stress_avg` = +0.57/mg p=0.0003 confirmed). Cross-phase aggregation requires §5.B treatment on the predictor side; the primitive itself is dose-naive by design.

Caveats (anticipated, to be locked at pre-reg time):

- Stress threshold and motion threshold are operational choices; the sensitivity ladder is the discipline that prevents threshold-cherry-picking.
- Heavy-exertion conditioning shrinks n. LC-era heavy-exertion-day subset estimated 100-200 days.
- Protocol calibration recently stabilised — per [`methodology/garmin_pacing_practice.md` §2 temporal qualifier](methodology/garmin_pacing_practice.md#temporal-qualifier--this-protocol-is-a-recent-stabilisation-not-a-constant), rest-stress as a behavioural rule is most consistent in the most recent months. Earlier LC-era days reflect partial / less-stable protocol; predictor is *cleaner* in recent periods.
- Intervention-baseline dose-response — quantified by [`citalopram_dose_response §5.6`](methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) (v3 2026-06-14). *Substantive revision of the earlier Session C reading.* The v3 multi-channel test CONFIRMED both stress channels as dose-modulated: `stress_mean_sleep` buildup post-CPAP β = +0.43/mg (p = 0.001), `all_day_stress_avg` β = +0.57/mg (p = 0.0003) — the latter is the strongest signal in the multi-channel sweep. **For C4b specifically — substantively strengthened**: the predictor combines both `all_day_stress_avg` and `stress_mean_sleep` with motion; the rolling-baseline rest-stress threshold uses these stress channels. **C4b inherits a jointly-confirmed-dose-response caveat on both stress channels** across the entire Citalopram-traject (2024-04 → ongoing), not just the 2026-03-20 boundary. At 30mg plasma the stress-with-low-motion threshold sits ~12-17 stress-points higher than at 0mg. **Required (no longer optional) sensitivity arm at pre-reg**: stratify C4b tests by Citalopram-traject phase (pre-2024-04 unmedicated, 2024-04 → 2024-06 buildup, 2024-06 → 2026-03 consolidation 30mg-plateau, 2026-03 → present afbouw), OR apply a per-mg-plasma offset to the absolute stress values before the threshold-crossing count. Within-phase C4b tests remain interpretable; cross-phase aggregation requires the dose-adjustment.
- Protocol disturbs the test: if the participant successfully acts on rest-stress (early bed via evening rule, [`garmin_pacing_practice.md` §5.3](methodology/garmin_pacing_practice.md#53-evening-rule)), downstream crash may be prevented. Sensitivity stratification by protocol-stable period would help.
- Self-reported crash labels via crash_v2.

Onward work (not gating credibility):

- Stress-with-motion-bin primitive extraction from monitoring_b.
- Joint analysis with HA11 (which uses U-dip count without motion filter) — does adding motion filter sharpen HA11's discrimination?
- Joint with C4's three primary metrics — does motion-filtered metric add incremental information beyond stress-decay-failure?
- M1 sub-boundary on protocol-stabilised period (per [`methodology/lc_era_temporal_segmentation.md` §6](methodology/lc_era_temporal_segmentation.md#6-criteria-for-adding-a-sub-boundary-in-a-specific-pre-reg)).

Not in scope:

- **Prevailing** (non-exertion-conditioned) rest-stress with time-of-day amplification — that is `personal_hypotheses.md` P5b, which is the broader-than-Wiggers extension. P5b stays in the Personal register because its scope genuinely extends beyond Wiggers' C4.
- HRV-derived sub-components (FR245 lacks HRV).
- Real-time intervention.

### H1 — Wearable signals lead the gevoelscore crash

**Verified 2026-06-12, batch 3.**

Wiggers passages:
- *"Your average overnight HRV shows you how the previous day impacted your health."* (PDF lines 916-918, HRV status)
- *"The dutch fatigue clinic is said to maintain that a decrease of 10 HRV points compared to the previous day could indicate PEM. With PEM, you often see that HRV drops after several days of overexertion. This happens even if the person rested well immediately after the overexertion."* (PDF lines 920-934)
- *"It's helpful to click the 'Overnight Averages' button in your 4-week overview. This will help you see if your HRV suddenly drops significantly. This can help you predict whether you're going to have a PEM or determine whether it would be wise to take it easier."* (PDF lines 956-964, the explicit predictive claim)
- *"Higher increases and decreases than normal indicate that you have overexerted."* (PDF lines 1014-1018, HRV and night Resting Heart Rate graph)
- **Mental PEM concession**: *"Too much mental activity, such as working on your laptop or writing, often goes undetected in your Garmin, but excessive mental activity can still cause PEM. It will also cause your HRV to drop that night or the following night. So, be aware that your Garmin can't warn you about everything."* (PDF lines 1448-1457)

Findings:
- **PREDICTIVE CLAIM IS HRV-SPECIFIC**: Wiggers' explicit "predict whether you're going to have a PEM" claim (PDF lines 956-964) refers specifically to HRV — the signal we are hardware-blocked on. For non-HRV signals (RHR, stress, BB), Wiggers describes them as retrospective (RHR "took hours") or co-incident with the felt state, not leading.
- **OUR H1 IS SOFTER THAN WIGGERS' EXPLICIT CLAIM**: testing whether `bb_overnight_gain` / `stress_mean_sleep` / `resting_hr` lead the gevoelscore crash is OUR derivation from Wiggers' general pacing-data argument, not a direct Wiggers prediction. Pre-reg should frame H1-without-HRV as an extension of the Wiggers framework rather than a literal test of her claim.
- **MENTAL PEM CONCESSION SUPPORTS H2**: Wiggers explicitly admits Garmin misses mental PEM (PDF lines 1448-1457). This is the source-grounded justification for our H2 (activity-invisible crashes) — H2 is the *expected* failure mode of H1 in the Wiggers framework, not an objection to it. Cite this passage in H2's pre-reg.
- **WIGGERS-RECOMMENDED HRV LAG THRESHOLD**: 10-point overnight HRV drop = PEM precursor (PDF lines 920-924, "Dutch fatigue clinic"). Not testable on this corpus but worth recording as the operational anchor for any future HRV-enabled work.
- **WIGGERS' OWN MULTI-DAY HRV LAG**: *"HRV drops after several days of overexertion"* (PDF lines 925-928) means HRV is itself slow — leading the felt crash, but lagging the exertion. Important nuance: a "wearable leads gevoelscore" finding could still mean "exertion → HRV (slow) → gevoelscore (slower)", not "HRV detected something before exertion did".

### H5 — Each metric has a characteristic lag vs exertion; lags differ by metric

**Verified 2026-06-12, batch 3.**

Wiggers passages establishing the implicit lag order:
- RHR: *"if you've pushed yourself much too far, it can take hours"* (PDF lines 168-172) — hours-to-day
- Stress (next-day reactivity): *"The day after you've done too much you can see stress spikes much faster, despite resting"* (PDF lines 1141-1143) — same-to-next-day
- Body Battery: *"This person expended a lot of energy on the first day shown in the images. The body battery line drops quite steeply, and the next day she has more orange in her nighttime."* (PDF lines 1433-1438) — same-to-next-day
- HRV: *"HRV drops after several days of overexertion. This happens even if the person rested well immediately after the overexertion."* (PDF lines 925-928) — multi-day cumulative

Findings:
- **IMPLICIT LAG ORDER**: BB / stress (same-next day) ≤ RHR (hours-to-day) < HRV (multi-day cumulative). Wiggers does not state this as one explicit ordering hypothesis, but it is the consensus implication of her observations across chapters.
- **PRE-REG-ABLE AS AN ORDERING TEST**: rather than reporting per-metric lags independently, the pre-reg can specify the **expected ordering** as a confirmation check. If `argmax-CCF-lag(bb_overnight_gain)` ≤ `argmax-CCF-lag(stress_mean_sleep)` ≤ `argmax-CCF-lag(resting_hr)`, the Wiggers pattern is confirmed at the ordering level even if absolute lag values differ from Wiggers'. Stronger test than "each metric has some lag".
- **MENTAL PEM EXCEPTION** (PDF lines 1448-1457): for mental-load PEM, Wiggers says HRV drops *"that night or the following night"* — same-to-next day, not multi-day. The lag may therefore depend on PEM type (mental vs physical exertion). If the corpus has mental-load events separately tagged (via `cog_load` from per_day_intensity triage), the lag-profile analysis could stratify physical vs cognitive PEM as a sub-test.

### Side findings (batches 1, 2, 3)

- **Activity Scale endorsement** (PDF lines 174-186): Wiggers names the OT energy-points "Activity Scale" as a corroborating data stream to RHR. *"This makes it easier to get an idea of your heart rate throughout the day and how activities affect it."* Directly parallels `per_day_intensity.csv` (`cog_load` / `phy_load` / `emo_load`) triage; adds Wiggers-citation support to the per-day-intensity methodology.
- **No-PEM vs with-PEM example plots** (PDF lines 1106-1110): Wiggers explicitly shows that the same person looks different on PEM vs non-PEM days. Validates our crash/non-crash stratification approach across all hypotheses.
- **Body Battery 70-80% floor as pacing target** (PDF lines 1380-1397): *"You might feel better and be able to keep your chronic illness more stable if you manage to stay at least above 70-80% body battery and preferably above 100%."* Directly relevant to D3 ("Living at the top, higher BB floor coincides with fewer crashes") — the 70-80% threshold is a specific Wiggers number worth citing in D3's pre-reg.
- **Adrenaline-lingers as the false-energy mechanism** (PDF lines 1316-1330): mechanism behind B4 (HRV spike) / D5 (high morning BB after overexertion) / H4 (parasympathetic swing). **Confirmed in batch 3** — Parasympathetic swing chapter (PDF lines 1431-1457) directly cites the swing pattern with the adrenaline-lingering as background mechanism. *"You may more easily experience high stress peaks during the day. So you might wake up in the morning with a high body battery, but you might also suddenly see very low blue lines in the middle of the day."* (PDF lines 1433-1444) — D5's "high morning BB after overexertion → crash" claim is verbatim Wiggers.
- **"Daily Resilience" pacing app** (PDF lines 1621-1644): Jens Hansen's 1-5 daily score combining BB+RHR vs the past 30 days' baseline. Essentially a packaged version of our `is_crash` / `is_dip` 2-tier labelling using two Garmin signals. **Cross-validation opportunity**: same-day correspondence between Daily Resilience scores and our gevoelscore-derived labels would be a second cross-source label-validation angle on top of Q9 in queued_work.md. Not in scope here but worth noting as a future research question.
- **Parasympathetic swing operational signature** (PDF lines 1027-1037): Wiggers' explicit pattern recognition table includes *"5. High HRV and very low HR: a sign of parasympathetic swing."* Direct operational signature for H4. **Without HRV** we can only test the "very low HR" half (which Wiggers also flags at PDF lines 192-197 as overexertion-related — captured by A2). RHR-only H4 is what the current pre-reg has, status ❌. This passage confirms why HRV is needed: it's the SECOND mandatory component of the diagnostic pattern. H4 stays blocked.
- **"Singing seated" worked example** (PDF lines 1463-1494, annotated graph): the only specific n=1 example Wiggers gives of the parasympathetic swing. Signature: HRV peak day → HRV drop + RHR rise for several days, with a "small PEM" felt 1-2 days later. Useful as the operational footprint to compare against if/when HRV becomes available.
- **Personal pattern-recognition as valid n-of-1 inference** (PDF lines 1570-1610, electrolytes-and-U-dip example): Wiggers documents her own pattern-detection workflow: notice repeated co-occurrence, hypothesise mechanism, intervene, confirm. This is the implicit Wiggers methodology our project mirrors — useful as a methodological citation when framing why n-of-1 with rolling baselines is defensible.

---

*Source of claims: Wiggers, "Watch Smart Pacing" handleiding (ME/cvs Vereniging, 07-2025), distilled and re-expressed as hypotheses. Empirical claims are the authors'; the operationalisations and the conflict-flags against your prior analysis are added here for testing.*
