# Wearable biometrics as predictors and characterisers of post-exertional malaise: an n-of-1 investigation in Long COVID stabilisation

*A research report on the Garmin × gevoelscore × notes correlation analyses, written 2026-06-05.*

> **Update:** an addendum covering work between 2026-06-06 and 2026-06-06 — the locking of a revised crash definition (crash_v2), a re-run of H02b against a new sub-threshold dip tier, a re-tagging of the original specificity check with crash_v2 labels, and a locked protocol for decoding the undocumented FIT message `unknown_233` — is published as a companion document at [RESEARCH-REPORT-ADDENDUM.md](RESEARCH-REPORT-ADDENDUM.md). The findings sharpen but do not contradict the conclusions below. The original report is preserved unchanged.

---

## Abstract

**Background.** Post-exertional malaise (PEM) is the cardinal feature of myalgic encephalomyelitis / chronic fatigue syndrome (ME/CFS) and a major component of Long COVID. The 2021 NICE guidelines and subsequent literature endorse pacing as the consensus management strategy and discourage graded exercise therapy. Wearable biometrics — heart rate, heart rate variability, stress estimation, sleep tracking — are widely repurposed by patients for pacing support, but evidence of their predictive validity in real-world self-management is thin. This report describes an intensive n-of-1 investigation of wearable signals as predictors and characterisers of PEM-like crash episodes in a single Long COVID patient, drawing on ~5 years of continuous Garmin Forerunner 245 data, ~3.7 years of overlapping subjective tracking (gevoelscore), and rich free-text notes.

**Methods.** Eleven hypotheses were tested under strict pre-registration discipline: four precursor hypotheses on daily-aggregate biometric signals (resting heart rate, average stress, sleep efficiency, body battery net delta), one on per-minute stress-spike duration, one descriptive recovery-time hypothesis, two crash-kind hypotheses (depth and duration era shifts), one trajectory-characterisation analysis, and two clause-level notes-language analyses. Crash episodes were defined operationally as runs of ≥ 2 consecutive days with gevoelscore ≤ 3 (the "crash_v1" definition), with episodes within 3 days merged. A null-sample design controlled for baseline rates; an episode-balanced train/validate split (2022-09-03 to 2023-12-31; 2024-01-01 to 2026-06-05) tested for generalisation across the recovery transition.

**Results.** Twenty-nine crash episodes were identified. Daily-aggregate biometric signals were largely uninformative as crash precursors; only the per-minute stress-spike duration metric cleared all three pre-registered criteria, and only in the train window. Sub-day-level signal compression (peak stress spike: 13.2 min in mid-2023 → 5.8 min in early 2025) tracked an overall stabilisation arc visible across multiple metrics. Late-era crashes (2024 onwards) were categorically different from early-era crashes in seven independent directions: less frequent, shallower nadir, shorter duration, more severe symptom signature, more often paired with caregiving context, more often "mixed-day topology" (positive content embedded in the crash day), and preceded by less symptom-warning language. A specificity check showed that ~42% of randomly-selected non-crash 3-day windows also fired the spike-precursor criterion, of which approximately 55% had identifiable real-life correlates (near-misses, proximity to crashes, or workout activity) and 45% were unexplained.

**Conclusion.** For this person, in this dataset, **daily-aggregate wearable signals are closed as a precursor channel for residual (post-stabilisation) crashes**. Cross-hypothesis integration provides strong evidence that crashes have qualitatively shifted across the stabilisation transition, not merely become less frequent. The findings argue against a predictive-alert feature design (positive predictive value would be ~4% at residual-crash base rates) and for retrospective-narrative features: a stabilisation-arc card, per-crash spike-precursor retrospectives, and crash-day-signature characterisation. The work also yielded methodological lessons on pre-registration discipline in n-of-1 designs with small integer-valued metrics, and identified a refined "crash_v2" definition (incorporating sub-threshold dips) as the most promising next step.

---

## 1. Introduction

### 1.1. Long COVID and post-exertional malaise

Long COVID — also termed post-acute sequelae of SARS-CoV-2 (PASC) — affects an estimated 5–15% of acute COVID-19 survivors and overlaps substantially with myalgic encephalomyelitis / chronic fatigue syndrome (ME/CFS). The defining symptom of both conditions is **post-exertional malaise (PEM)**: a delayed worsening of symptoms (typically 12–72 hours) following physical, cognitive, or emotional exertion that, importantly, exceeds an individual-specific energy envelope. PEM is qualitatively distinct from ordinary fatigue: it does not respond to rest in the way training-induced fatigue does, it persists for days or weeks, and the threshold that triggers it is often invisible until exceeded.

The 2021 NICE guideline overhaul (NG206) for ME/CFS reversed prior recommendations of graded exercise therapy, instead endorsing **pacing** — operating within the individual's energy envelope to avoid triggering PEM — as the consensus management strategy [^1]. This was reinforced by Workwell Foundation guidance, the Long COVID Physio collective, and patient-led organisations [^2][^3]. Cognitive behavioural therapy was repositioned only as an adjunct for coping, not a cure.

### 1.2. Wearable biometrics in chronic-illness self-management

Patients with ME/CFS and Long COVID have widely adopted consumer wearables — Garmin, Polar, Whoop, Oura, Apple Watch, and the purpose-built Visible app — to support pacing through heart rate monitoring [^4][^5]. The most established approach is the Workwell heart rate ceiling: keep daily resting heart rate within ~15 bpm of the rolling baseline; treat the anaerobic threshold as a PEM-risk threshold. A 2025 wearable HRV study found HRV suppression persists ~24 hours after crossing the ventilatory threshold (VT1), supporting the use of HRV-based recovery indicators in conjunction with HR [^6].

Despite this widespread use, the evidence base for the *predictive* validity of wearable signals in real-world chronic-illness self-management remains modest. Most studies focus on population-level associations or short-term controlled exercise tests; comparatively little work characterises whether these signals predict, accompany, or merely correlate with PEM episodes in longitudinal home-monitoring data.

### 1.3. Research context

The participant in this study is a 47-year-old man diagnosed with Long COVID on 2026-05-06, with symptoms preceding the diagnosis by an unknown interval. He has worn a Garmin Forerunner 245 continuously since 2021-08-16 (98.8% coverage to date) and has maintained a daily subjective journal ("gevoelscore" — a 1–6 scale capturing how he feels) with ~100% coverage since 2022-09-03 and free-text notes alongside the score on ~50% of days. By the participant's self-report, the journey across 2022–2025 has been one of progressive recovery: episode frequency dropped from approximately 10–11 per year in 2023–2024 to approximately 2 per year in 2025–2026. This recovery is multi-factorial: pacing skill, the fading of external pressures (work reintegration, relationship transitions, acceptance of chronic illness), and possibly pharmacological interventions (an SSRI dose adjustment is mentioned in notes).

The combination of long-duration, high-coverage objective wearable data with a near-complete subjective record and free-text notes is unusually rich for n-of-1 ME/CFS / Long COVID research. The participant maintains the gevoelscore app's source code and is also the participant — eliminating IRB-equivalent participant-consent ambiguity but introducing the standard reflexivity caveats of self-research.

### 1.4. Research aims and key questions

This investigation has four primary aims:

1. **To test whether wearable biometric signals predict PEM crashes in this individual at daily resolution**, using the established pacing-literature indicators (RHR, stress, sleep, body-battery composite).
2. **To test whether sub-daily signals — specifically per-minute stress-spike characteristics — predict crashes** where daily aggregates do not, motivated by the participant's lived-experience claim that brief intense moments can trigger crashes.
3. **To characterise the recovery / stabilisation trajectory** quantitatively across the available data window, distinguishing genuine recovery from artefacts of changed self-monitoring discipline.
4. **To test whether residual (post-stabilisation) crashes are qualitatively different** from pre-stabilisation crashes — the "kind of crash changed" theory — across multiple independent axes (depth, duration, biometric signature, language).

A secondary aim was to derive design implications for the gevoelscore app's planned insight-card features, distinguishing card concepts that are empirically supported from those that would mislead the user.

---

## 2. Hypotheses

Eleven hypotheses were pre-registered before data inspection. Each was assigned a designator (H## for precursor hypotheses, K## for kind-of-crash hypotheses, S## for stabilisation arc) and a strict falsification criterion. Hypothesis files (`docs/research/garmin/hypotheses/*/hypothesis.md`) contain the full pre-registration; this section summarises the claim and underpinning for each.

### 2.1. Precursor hypotheses

**H01 — Resting heart rate drift before crashes.** Claim: In the 7 days before a crash, this participant's daily RHR is elevated above his rolling 90-day baseline. Underpinning: Workwell Foundation pacing rule ("RHR + 15 bpm") is the most established lay-friendly pacing indicator and rests on the consistent observation in ME/CFS of autonomic dysregulation persisting before and during PEM episodes [^2].

**H02 — Sustained stress elevation before crashes.** Claim: In the 3 days before a crash, the daily mean Garmin stress level (a Firstbeat-Analytics-derived 0–100 metric driven by HRV) is elevated above baseline. Underpinning: HRV-based stress measures capture sympathetic-vagal imbalance characteristic of pre-PEM states [^6].

**H02b — Per-minute stress spike duration before crashes.** Claim: In the 3 days before a crash, the maximum contiguous duration of intense stress samples (≥ 75, lasting ≥ 5 minutes) is elevated above baseline. Underpinning: The participant reported a strong personal experience that intense moments embedded within otherwise calm days can trigger crashes — a pattern that daily-mean stress, by construction, smooths away.

**H03 — Sleep efficiency drop before crashes.** Claim: In the 7 nights before a crash, sleep efficiency (computed as total sleep time divided by total in-bed time from Garmin's sleep-staging output) drops at least 5 percentage points below baseline. Underpinning: Sleep dysregulation is one of the most consistently cited PEM precursors in the ME/CFS / Long COVID literature [^1][^7].

**H04 — Body battery net drain elevated before crashes.** Claim: In the 3 days before a crash, the daily net body-battery delta (charged value minus drained value) is more negative than baseline. Underpinning: Garmin's body battery is a closed-source composite of HR + HRV + stress + sleep and is the single number most directly aligned with the pacing literature's "energy envelope" concept.

### 2.2. Descriptive and kind-of-crash hypotheses

**H05 — Recovery time characterisation after crashes.** Descriptive: After each crash episode ends, characterise the distribution of recovery times (days until score returns to within 1 point of pre-crash baseline). No predictive criterion; the goal is foundation data for a per-crash recovery-comparison card.

**K01 — Crash depth shifted across recovery eras.** Claim: The minimum score within each episode (the "nadir") is higher (less severe) in late-era (2024-onwards) crashes than in early-era (2022–2023) crashes. Underpinning: If the participant has truly stabilised, residual crashes plausibly differ in severity, not just frequency. The depth axis is the cleanest test.

**K02 — Crash duration shifted across eras.** Claim: The calendar span of crash episodes is shorter in the late era. Same recovery rationale, orthogonal axis.

### 2.3. Trajectory and language analyses

**S01 — Stabilisation trajectories.** Descriptive, no formal hypothesis: characterise the rolling-90-day means of four metrics (RHR, average stress, sleep efficiency, max stress-spike duration) across the full Garmin window, to visualise the participant's framing of "the pendulum settling".

**Notes-language analyses (Goal A and A.5 v1/v2).** Exploratory: identify lexical and category-level patterns in the participant's free-text notes that distinguish crash days, lead-up days, and non-crash days, with comparison across recovery eras. A three-layer model was developed (categories → modifiers for negation/severity → clause-level polarity), applied deterministically via a curated phrase dictionary.

### 2.4. Pre-registration discipline

Each hypothesis was pre-registered in a `hypothesis.md` file before the test script was written or any data inspected for that hypothesis. The pre-registration specified the operational metric, lead-up window, baseline window, null-sample design, exclusion rules, and the specific falsification criterion. Two procedural lessons were learned during execution and applied to subsequent hypotheses (see §5.4).

---

## 3. Methodology

### 3.1. Data sources

**Subjective data** (n=1, daily): `day_entries` collection in the Directus instance backing the gevoelscore app. Fields: date, score (1–6), free-text note. Coverage: 2022-09-03 → 2026-06-05; 1,372 entries with score; 686 with non-empty note.

**Objective data** (n=1, multi-resolution): Garmin GDPR data export covering 2021-08-16 → 2026-06-04. 98.8% daily coverage. Data parsed:

- **Daily aggregates** from `DI_CONNECT/DI-Connect-Aggregator/UDSFile_*.json`: `restingHeartRate`, `allDayStress.aggregatorList[TOTAL].averageStressLevel`, `bodyBattery.chargedValue`, `bodyBattery.drainedValue`.
- **Sleep records** from `DI_CONNECT/DI-Connect-Wellness/*_sleepData.json`: `deepSleepSeconds`, `lightSleepSeconds`, `remSleepSeconds`, `awakeSleepSeconds`, `unmeasurableSeconds`, `sleepWindowConfirmationType`.
- **Per-minute stress samples** extracted from 7,888 monitoring-type FIT files via the `fitdecode` Python library. ~1,400 stress samples per day after deduplication.
- **Activity records** from `user@example.com_0_summarizedActivities.json`: 404 logged activities with start time, type, duration, heart-rate statistics.

Total Garmin payload: ~128 MB compressed; full inventory documented in [docs/research/garmin/README.md](garmin/README.md).

### 3.2. Operational definitions

**crash_v1** (locked 2026-06-05 after preflight inspection): A *crash episode* is a maximal run of ≥ 2 consecutive `day_entries` with `score ≤ 3`, with episodes whose endpoints fall within 3 calendar days of each other merged into a single episode dated to the start of the first run. Twenty-nine episodes were identified in the analysis window. This definition was the result of a one-step revision: the initially-proposed "personal bottom 15% of scores" rule was abandoned during preflight because the heavy clustering of scores at the integer value 4 caused the percentile threshold to land on a tied value, capturing ~50% of days. The locked absolute threshold (score ≤ 3) captures 13.9% of days, closer to the original intent.

**Train and validate windows.** Because of the recovery cliff (see §4.1), a time-proportional 70/30 train/validate split would have placed only ~3 of the 29 episodes in the validate window, rendering it statistically useless. The locked split is instead **episode-balanced**: train 2022-09-03 → 2023-12-31 (14 episodes), validate 2024-01-01 → 2026-06-05 (15 episodes). This means the recovery transition itself sits inside the validate window, providing a strong test for whether putative precursor signals generalise across the change in physiological state.

**Lead-up windows.** Per-hypothesis: H01 used 7 days; H02, H02b, H04 used 3 days; H03 used 7 nights. The choice was guided by literature: RHR signals tend to be slower-moving (multi-day rolling), stress signals are more reactive (day-by-day), sleep is night-by-night.

**Baseline window for precursor hypotheses.** 90 days ending one lead-up window before the episode. Trimmed mean (drop top and bottom 10 percent) used to compute the baseline value, reducing sensitivity to outlier days such as acute illness or atypical events.

### 3.3. Statistical design

**Null-sample design for precursor hypotheses.** For each precursor hypothesis, the same window-based metric was computed for the participant's actual crash episodes *and* for 200 randomly-selected reference dates whose lead-up windows were disjoint from any crash episode's lead-up days (random seed: 20260605, fixed for reproducibility). The crash-window rate and the null-window rate were compared to compute the **discrimination** metric (crash rate minus null rate, in percentage points).

**Three-criterion falsification.** Each precursor hypothesis required three independent criteria to be satisfied in both train and validate windows for the hypothesis to be declared *supported*:

- **Criterion (a) — Frequency:** at least 60% of crash episodes show the metric above the pre-registered threshold.
- **Criterion (b) — Discrimination:** the crash-window rate exceeds the null-window rate by at least 15 percentage points.
- **Criterion (c) — Magnitude:** the median delta is at least a pre-registered minimum, and the lower (or upper, depending on direction) quartile crosses zero.

This combination protects against a single criterion driving a "support" call by chance.

**Permutation tests for kind-of-crash hypotheses.** K01 and K02 used 10,000 random label permutations to compute empirical p-values for observed era differences in nadir and span. A p-value threshold of ≤ 0.10 was pre-registered, defensible given the small sample (14 vs 15 episodes).

**Notes-language analysis.** A three-layer deterministic categoriser was developed:

1. **Layer 1 (categories)**: substring matching against an 11-category Dutch phrase dictionary (categories such as `belasting_fysiek`, `symptoom_fysiek`, `recovery_actie`, `triggers_extern`, etc.) curated using the "LLM as cartographer" pattern — the dictionary was drafted by an LLM (Claude Opus) from explicit prompt files held under version control, then reviewed and edited by the participant before deterministic application.
2. **Layer 2 (modifiers)**: negation (`geen`, `niet`, `zonder`) and severity (`lichte`, `hele dag`, `ernstige`) detected within a 3-word window before each symptom-category phrase, producing four symptom states: absent / mild / present (default) / severe.
3. **Layer 3 (polarity)**: clause-level positive/negative valence (`leuk`, `fijn`, `goed` vs `matig`, `slecht`, `vervelend`), with clauses containing both markers classified as mixed.

Multi-labelling permitted at the category level. Clause segmentation used Dutch punctuation and conjunction-based splitting.

### 3.4. Tools, reproducibility, software

All analyses run in Python 3.14 with `fitdecode` 0.11 for FIT parsing, `matplotlib` 3.10 for figures. No external machine-learning libraries were used; the deterministic categoriser is bespoke. Random seeds fixed at 20260605 for all stochastic operations (null sampling, permutation tests). All scripts and intermediate artefacts are checked into the gevoelscore-app repository under `docs/research/`, organised per hypothesis. Each hypothesis folder contains:

- `hypothesis.md` (pre-registration, written first)
- `fetch_day_entries.mjs` (Directus data fetcher)
- `test.py` (analysis script)
- `result.md` (verdict and discussion, written after running)
- `result-data.json` (structured numerical outputs)
- Optional `*.png` figures

The dictionary v2 used in the notes analysis lives at `docs/research/notes/02-categorize-clauses/category_dictionary_v2.md`; its prompt artefact at `docs/research/notes/02-categorize-clauses/prompts/category_dictionary_seed_v2.yaml`.

### 3.5. Limitations of the n-of-1 design

This is a single-subject study. The findings characterise one participant's biometric-symptom relationship and cannot be extrapolated to the Long COVID population without further work. The participant is also the principal investigator, raising the standard reflexivity concerns of self-research. Multiple statistical comparisons across hypotheses inflate the chance of false-positive findings; the held-out validate window and the pre-registration discipline are the principal protections. The Garmin algorithms (especially the proprietary stress and body-battery composites) are closed-source and may have changed across firmware versions during the data window; investigation of Garmin's public-facing communications (see §5.4) suggests no major algorithmic overhaul to the relevant signals on the Forerunner 245 during 2022–2026, but small calibration shifts cannot be ruled out.

---

## 4. Results

### 4.1. Crash counts and stabilisation cliff

Twenty-nine crash_v1 episodes were identified across the 2022-09-03 → 2026-06-05 analysis window. Annual distribution:

| year | episodes | note |
|------|---------:|------|
| 2022 | 5 | partial year (~4 months of tracking) |
| 2023 | 9 | |
| 2024 | 11 | peak |
| 2025 | **2** | full year |
| 2026 | 2 | partial year (~5 months) |

The drop from ~10–11 episodes per year in 2023–2024 to ~2 per year in 2025–2026 is the **stabilisation cliff** — the participant's primary self-reported recovery finding, confirmed at the labelled-event level. Subsequent analyses (S01, §4.3 below) show that the underlying physiological transition was smoother than this annual breakdown suggests, taking roughly 12–18 months across 2023–2024 rather than a single-date discontinuity.

### 4.2. Daily-aggregate precursor tests (H01–H04)

All four precursor hypotheses tested on daily aggregates were refuted under the pre-registered criteria. Key findings:

| hypothesis | window | crash rate | null rate | discrimination | median delta | verdict |
|---|---|---:|---:|---:|---:|---|
| H01 RHR drift | train | 8% | 9% | −1.2 pp | +0.5 bpm | refuted |
| H01 RHR drift | validate | **0%** | 9% | **−9.5 pp** | **−1.0 bpm** | refuted |
| H02 avg stress | train | 43% | 17% | +25.9 pp | +2.7 stress | refuted (crit a fails) |
| H02 avg stress | validate | 13% | 17% | −3.7 pp | −0.2 stress | refuted |
| H03 sleep efficiency | train | 0% | 0% | 0 pp | −0.002 | refuted |
| H03 sleep efficiency | validate | 0% | 0% | 0 pp | −0.004 | refuted |
| H04 body battery | train | 14% | 20% | −5.7 pp | −2.8 BB | refuted |
| H04 body battery | validate | 33% | 20% | +13.3 pp | −3.0 BB | refuted (close) |

Three observations of substance:

(i) **H02's train window showed a real directional signal** — 79% of train-era crash episodes had elevated lead-up stress, median +2.7 stress points, discrimination +25.9 pp — but did not clear the strict 60%-at-threshold criterion. The same metric was flat in the validate window.

(ii) **H01's validate window showed RHR slightly *lower* in lead-up than baseline** (median −1.0 bpm), contradicting the Workwell-rule prediction. This is consistent with a participant whose pacing has eliminated load-precipitated crashes, leaving residual crashes that do not stress the autonomic system in HR-visible ways.

(iii) **H04 was the only test where the validate window showed any positive directional hint** (discrimination +13.3 pp, just below the +15 pp bar). The hint may point at HRV, which is a body-battery input but was not tested directly; we have not extracted per-day HRV from the FIT files.

### 4.3. Per-minute spike precursor: H02b

H02b extracted per-minute stress samples from 7,888 monitoring-type FIT files. For each crash episode, the maximum contiguous duration of high stress (samples ≥ 75 lasting ≥ 5 minutes) was computed for each of the 3 days in the lead-up window, with the per-episode metric being the maximum across those 3 days. The result:

| window | n | crash rate (≥ +10 min) | null rate | discrimination | median delta | verdict |
|---|---:|---:|---:|---:|---:|---|
| **train** | 14 | **71%** | 41% | **+29.9 pp** | **+16.2 min** | **SUPPORTED** |
| validate | 15 | 33% | 41% | −8.2 pp | +6.7 min | refuted |

Train cleared all three pre-registered criteria — the only fully supported precursor window in the investigation. The pattern is biologically interpretable: in early-era crashes, lead-up days contained a sustained ≥ 5-minute high-stress spike approximately 16 minutes longer than the participant's typical max-spike day. Per-episode breakdown (table in [H02b/result.md](garmin/hypotheses/H02b-stress-spikes/result.md)) shows 10 of 14 train-era crashes had lead-up max-spike durations between 22 and 56 minutes, against a typical baseline of 11–16 minutes.

A subsequent **trajectory analysis** ([H02b/trajectory-notes.md](garmin/hypotheses/H02b-stress-spikes/trajectory-notes.md)) computed the same discrimination metric on rolling 12-month windows anchored monthly. The result is a smooth decline from peak discrimination (+31.8 pp, anchor August 2023) to near zero by mid-2024 — the spike-precursor signal does not vanish at a cliff but fades gradually over approximately 12 months.

A **specificity check** ([H02b/specificity-check.md](garmin/hypotheses/H02b-stress-spikes/specificity-check.md)) examined the 42% of non-crash null-sample windows that also fired the spike criterion (83 of 200 windows). Categorisation:

| tag | count | % of false positives |
|---|---:|---:|
| unexplained | 37 | 45% |
| near-miss (score = 3 in/around window) | 32 | 39% |
| close-to-crash (within ±14 days, outside 3-day lead-up) | 28 | 34% |
| activity-induced (workout ≥ 30 min on peak day) | 15 | 18% |

The 39% near-miss subgroup is particularly informative: these are days where the participant's score reached 3 but did not satisfy the 2-consecutive-day crash_v1 threshold. The spike metric is genuinely detecting strain that did not escalate to a full crash, suggesting that crash_v1 may be operationally too strict and that a **sub-threshold "dip" definition (crash_v2)** could recover meaningful additional signal.

### 4.4. Recovery descriptive analyses

**H05 (recovery time) returned a spec-induced trivial result.** The pre-registered recovery target (within 1 point of pre-episode baseline) was structurally met on the day after every episode's end day, because by construction the day after an episode end has score > 3 (otherwise the merge rule would have extended the episode). All 25 measurable episodes recovered in 0 days. This is a finding about the protocol, not the recovery. A revised "H05b" with a sustained-recovery target (two consecutive days at or above pre-episode baseline) is queued.

**S01 (stabilisation trajectories)** computed 90-day rolling trimmed means of four metrics across the full Garmin window, anchored every 7 days. The most striking finding is in the maximum daily stress-spike duration:

| anchor date | max-spike (min) | avg stress | RHR (bpm) | sleep eff. |
|---|---:|---:|---:|---:|
| 2021-11-14 (pre-LC) | 10.5 | 32.6 | 55.1 | 0.987 |
| 2022-06-12 (early dx) | 10.4 | 36.2 | 54.9 | 0.990 |
| 2023-08-06 (peak) | **13.2** | 35.4 | 55.2 | 0.993 |
| 2025-04-27 (trough) | **5.8** | **29.1** | 57.8 | 0.995 |
| 2026-05-31 (recent) | 11.4 | 33.7 | **60.8** | 0.992 |

The max-spike duration metric halved from peak to trough; the average stress baseline fell ~7 points across the same window. **Sleep efficiency was flat throughout** (98.7%–99.5%). The May 2026 anchor shows a recent uptick on three of four metrics (RHR at its highest point in the whole window), suggesting a recent perturbation worth attending to in clinical follow-up.

### 4.5. Kind-of-crash era hypotheses (K01, K02)

**K01 (crash depth shift).** Median nadir across episodes shifted from 2 (early era, 14 episodes) to 3 (late era, 15 episodes); mean shift was +0.67 on the 1–6 scale. Categorical finding: **three early-era crashes reached the rock-bottom score of 1, while no late-era crash did**. Permutation test p-value = 0.28 — failing the pre-registered ≤ 0.10 threshold because the nadir variable takes only three integer values (1, 2, 3), making the median brittle in a small sample. Verdict: *suggestive but underpowered*. Direction is unambiguous; statistical confirmation requires more episodes.

**K02 (crash duration shift).** Median span shifted by only 0.5 days (early 2.5, late 2.0), but the **mean span dropped from 4.64 to 2.53 days**. The categorical finding: 5 of 14 early-era crashes lasted ≥ 5 days (including 9, 11, and 14-day spans); only 1 of 15 late-era crashes did (a 7-day episode in February 2024). Permutation p = 0.095, narrowly clearing the bar; but the median criterion failed by 0.5 days. Verdict: *refuted on the strict bar*, with a strong tail-collapse finding the median did not capture. Same lesson as K01: small integer-valued metrics with mass-on-the-minimum break median-based tests.

### 4.6. Notes-language analyses

Three rounds of notes analysis were run:

**Goal A (word frequency).** Single-word frequency analysis of the 686 notes, comparing crash-day, lead-up-day, and non-crash-day vocabularies. Key findings: `hoofdpijn` ("headache") appears in 78% of crash notes; the words `koorts` (fever) and `keelpijn` (sore throat) are 8.7× and 5.4× more common on crash days respectively, indicating an infection-triggered crash subtype; the word `emotioneel` is 4.7× more common on crash days; family members' names appear more often in lead-up than crash days, suggesting a caregiving-load lead-up signature.

**Goal A.5 v1 (clause categorisation).** An 11-category Dutch phrase dictionary was built using the LLM-as-cartographer pattern. Each note was segmented into clauses (median 11 words per note, ~3.5 clauses), and each clause was assigned one or more categories via substring matching. Per-day category presence was computed and compared across groups. **Headline finding: late-era crash days were 22% paired with `belasting_gezin` (family/caregiving) context, vs 0% in early era**; late-era crash days were 25% paired with cognitive symptoms (brainfog), vs 11% early.

**Goal A.5 v2 (three-layer model).** v1's category-only model conflated negation ("geen hoofdpijn" — *no headache*) with presence and discarded self-rating words ("matig" — *mediocre*) to the residual neutral category. v2 added modifier (negation + severity) and polarity (clause-level positive/negative) layers. Two new findings:

- **`symptoom_fysiek` state severity shifted dramatically across eras** on crash days: severe-state from 4% (early) to 22% (late), a +18 percentage point shift. Late crashes are 5× more likely to include severe physical-symptom language even though crashes are 5× less frequent.
- **Late-era crash days are 50% positive-dominant by clause polarity** (vs 11% early). Verification of 16 such days ([notes/02/verification-late-positive.md](notes/02-categorize-clauses/verification-late-positive.md)) confirmed this is a real "mixed-day topology" finding, not active reframing or measurement noise: late crashes are increasingly embedded in days that also contain functional and positive content (within-day improvements, social moments, recovery actions). The crashes are **less totalizing**.

A small bug surfaced during verification: the polarity layer does not apply the negation handling that the symptom layer does. Clauses like "het is echt niet fijn" ("it really is not nice") fire `polarity_positive` because "fijn" matches. Estimated effect: 1–2 of 16 positive-dominant crash days are partly false-positive. The fix (apply 3-word negation window to polarity markers as well) is queued as dictionary v3.

### 4.7. The cumulative kind-of-crash finding

Across the eleven hypotheses, **seven directional findings independently support the theory that residual crashes are qualitatively different from pre-stabilisation crashes**, with no contradictions:

| axis | source | direction (early → late) |
|---|---|---|
| Stress precursor (daily avg) | H02 | yes → no |
| Stress precursor (per-minute spike) | H02b | yes (supported) → weaker |
| Crash depth | K01 | shallower (no score-1 episodes) |
| Crash duration | K02 | shorter (long-tail collapse 5→1) |
| Symptom severity language | notes v2 | severe-state +18 pp |
| Day topology | notes v2 | mixed +39 pp |
| Lead-up language | notes v2 | less warning, more cognitive |

None of these findings individually clears its strict pre-registered bar in isolation (H02b train comes closest, fully clearing but with a refuted validate window). The cumulative weight, however, is strong: seven independent measurements all point the same direction. The residual (post-stabilisation) crashes are fewer, shallower, shorter, more severe in their physical-symptom signature, more often paired with caregiving context, increasingly embedded in mixed days rather than totalizing them, and preceded by less symptom-warning language with more cognitive-load mentions.

---

## 5. Discussion

### 5.1. Interpretation of the seven-axis pattern

The "kind of crash changed" finding has two compatible mechanistic readings:

**Reading 1 — mechanism shift.** The participant's pre-stabilisation crashes were partly precipitated by sympathetic-overload accumulation that the daily-aggregate stress signal could see. As pacing skill matured and external pressures abated, the load-precipitated crashes stopped happening. The residual 2025+ crashes are triggered by mechanisms that the daily-aggregate signals cannot see — cognitive load, sleep dysregulation in dimensions not captured by efficiency, mast-cell activation, hormonal cycle, or external viral reactivation. The K## findings (depth, duration) are consistent with these residual crashes being a smaller, sharper subtype.

**Reading 2 — threshold compression.** The participant's overall physiological response to stressors has scaled down with recovery. Pre-stabilisation, a moderately stressful 3-day stretch might push average stress from 30 to 38 (visible signal); post-stabilisation, the same psychological stretch might only push it from 25 to 28 (invisible at our threshold). The signal hasn't changed kind; the magnitude has shrunk into our measurement noise.

The S01 trajectories (§4.3) and H02b trajectory (§4.3) provide direct evidence for Reading 2 — the typical spike duration fell from 13.2 min to 5.8 min, and the discrimination metric fell from +31.8 pp to near-zero, both gradually over 12–18 months. But the categorical findings (zero score-1 nadirs in the late era; 80% drop in long-crash tail; appearance of `belasting_gezin` in late crash days where it was absent in early ones) are harder to explain by pure threshold compression and point at Reading 1.

We propose both readings hold partial responsibility, and we cannot distinguish them definitively without intervention data (the eventual "shielder-vs-reliever" question; see §7.5).

### 5.2. Why daily aggregates fail and what that means

The four daily-aggregate precursor tests (H01–H04) returned null verdicts despite testing well-established pacing indicators. This is not, in our view, a failure of the indicators in general but rather a finding specific to this participant in this time window:

- The participant has chronotropic incompetence to some degree (typical in ME/CFS [^2]), reducing the magnitude of HR-visible exertion response.
- The participant is well-paced enough that load-precipitated crashes — the type that daily aggregates would catch — are no longer the dominant residual subtype.
- The remaining crash subtypes (per Reading 1 above) are mechanistically invisible to the metrics we tested.

For the application's design, this argues against features built on daily-aggregate "warning" patterns. The positive predictive value of any such alert, even computing optimistically from H02b's train-window evidence, is ~4% at the residual-crash base rate of ~2 per year. A predictive alert card would be wrong 24 times out of 25.

### 5.3. The mixed-day topology finding

The single most novel finding of the investigation, in our view, is the **mixed-day topology shift** (notes v2: +39 pp positive-dominant late vs early). Late-era crash days increasingly contain functional, positive, social, or restorative content alongside the crash. This is not active reframing (writing about the good parts of a bad day as compensatory effort) but a structural change in how a "crash day" looks. The participant has phone calls, takes walks, attends to family — and *also* has the crash. The crash no longer consumes the whole day.

This is a meaningful recovery indicator that is unlike anything the pacing literature explicitly characterises. The pacing literature focuses on energy envelopes and triggers; the recovery literature focuses on symptom resolution. The mixed-day topology speaks to a different dimension — the *integration* of crashes into ongoing life rather than their *displacement* of ongoing life. We propose this as a candidate concept for further n-of-1 study and a strong candidate for app-level surfacing as a recovery-narrative finding ("your crashes are increasingly embedded in days where good things also happen — your body is finding edges").

### 5.4. Methodological lessons

Five lessons learned across the investigation that we propose generalise to other n-of-1 wearable-correlation studies:

1. **Pre-register on both median AND mean** when the metric takes few distinct integer values with mass on the minimum. K01 (nadirs: 3 values, 60% at 2) and K02 (spans: most = 2 days) both showed clean directional shifts in the mean that the pre-registered median criterion did not capture. The brittleness is statistical, not substantive.

2. **Run a dry inspection of 3-5 episodes' computed values before locking a spec.** H03 ran with a confirmation-type whitelist that excluded 73% of valid nights, producing 2 usable train episodes. H05 ran with a recovery target that was structurally always met. Both bugs would have surfaced in a 5-minute hand inspection.

3. **Naming-clash hazards in rich-output scripts.** When per-category and per-symptom-state keys share a "_present" suffix, dictionary overwrites silently corrupt summary statistics. Prefix disambiguation prevents this.

4. **The same script can carry two different definitions of "dominant" polarity.** A loose `pos > neg` and a strict `pos > neg AND pos > neu` rule yielded 50% vs 0% on the same data. Inconsistencies of this kind only surface during verification.

5. **Always look at the actual clauses behind a striking statistic** before publishing or building. The verification step on the 50%-positive-dominant late crash finding reframed it from "active reframing" to "mixed-day topology" — a different and more useful interpretation.

Two additional infrastructural choices that paid off:

- **Pre-registration as committed-to-disk markdown files** (one per hypothesis) created a clear record of what was claimed before testing and made it impossible to silently move the goalposts.
- **The LLM-as-cartographer pattern with explicit prompt YAMLs** (adapted from the programmeerprobeer/tvoo_backend convention) kept the dictionary construction reproducible and auditable: the prompt that produced the categorisation map is itself a versioned artefact under `docs/research/notes/02-categorize-clauses/prompts/`.

### 5.5. Limitations

Beyond the n=1 caveats noted in §3.5, three additional limitations bear emphasis:

- **Garmin firmware drift cannot be fully ruled out.** Public investigation of Garmin's release notes for the Forerunner 245 over 2022–2026 shows no documented major overhaul of the stress or body-battery algorithms; the official position (per a Garmin moderator response on a 2024 forum thread) is that algorithms are stable but baselines may reset on firmware update. If firmware changes were the explanation for the H02b compression finding, we would expect step-changes at update dates rather than the smooth 12–18 month decline we observe. We accept the smooth-decline shape as more consistent with real physiological change than algorithmic drift, but small calibration shifts cannot be excluded entirely.
- **Notes coverage is uneven across years** (18% in 2022, 71% in 2024 peak, 44% in 2026). The language-analysis findings are computed as rates per note, not absolute counts, which controls for coverage at the aggregate level. But qualitative interpretations — particularly the era comparison in §4.6 — may partly reflect what the participant happened to write more or less about in each phase, not pure shifts in lived experience.
- **The recent May 2026 perturbation** in three of four S01 trajectory metrics (RHR climbing to its highest value in the data window, stress and spike duration rebounding) was not characterised quantitatively beyond the 90-day rolling mean. It may represent a meaningful change in state that deserves its own focused analysis when more data accumulates.

---

## 6. Implications for application design

The investigation was conducted in service of the gevoelscore app's planned "insight cards" feature. The findings sharpen which card concepts have empirical support and which would mislead the user. Three tiers:

**Tier 1 — Strong evidence, ready to prototype.** Concepts backed by multi-axis findings:

- A **stabilisation-arc card** showing the multi-year recovery trajectory across crash frequency, stress baseline, spike duration, and the categorical kind-of-crash findings. Backed by seven directional findings.
- A **per-crash spike-precursor retrospective card** for pre-2024 crashes. H02b train-window evidence is strong enough that surfacing "around date X there was a Y-minute stress spike on day Z — what was happening?" would be correct 71% of the time on historical crashes.
- A **crash-day signature card** drawing on the notes v2 categorisation to describe each crash by the categories that appeared (physical / cognitive symptoms, emotional load, family context, recovery actions).
- A **mixed-day topology card** for the late-era recovery framing.
- A **recent-perturbation awareness card** surfacing the May 2026 uptick as awareness (not alarm).

**Tier 2 — Promising, more work needed.**

- A retrospective spike card for new (validate-era) crashes, framed honestly as "we see a notable spike that day but the pattern is less consistent than it used to be."
- Caregiving-context tagging on late-era crashes (waits on the tagging-suggestion feature).
- A sleep-as-protector framing card ("your sleep efficiency has stayed stable through this whole journey"), which honestly reports what the H03 null finding tells us.

**Tier 3 — Candidates pending further research.**

- Body-battery intra-day rise / drop detection cards (requires decoding the undocumented FIT message type 233, or live Garmin Connect API).
- The shielder-vs-reliever experiment cards (require an `interventie` category in the notes dictionary, plus a working H05b recovery-time metric).

**Concepts NOT to build.**

- A predictive "you might crash tomorrow" alert card. Positive predictive value ~4% at residual-crash base rates; would generate persistent false alarms.
- A daily Garmin tile dashboard. The daily-aggregate signals do not predict residual crashes; presenting them as actionable would mislead.
- A sleep-as-warning card. Sleep efficiency was null across crashes, lead-ups, and non-crash days.
- A daily-average stress alert. The daily-avg signal was train-only positive and is now in the noise floor.

---

## 7. Future work

### 7.1. crash_v2 — distinguishing real crashes from dips

The most promising single follow-up from this investigation is a refinement of the crash definition itself. The H02b specificity check identified that ~39% of false-positive spike-firing windows correspond to days where the participant's score reached 3 but the crash_v1 2-consecutive-day rule was not satisfied — sub-threshold "dip" events that the participant logged as noticeable but the operational definition discarded.

We propose a `crash_v2` operational definition that distinguishes three event classes:

- **`crash`**: ≥ 2 consecutive days with score ≤ 3 (the current crash_v1).
- **`dip`**: an isolated day with score ≤ 3 that does not extend into a crash.
- **`vague_low`**: a day with score = 4 preceded or followed by a `dip` or `crash` day — capturing the "yellow zone" of approaching but not entering a low state.

Adopting crash_v2 would approximately double the labelled event set (current 29 episodes → estimated 50–60 if dips are included), tightening every K## comparison and providing additional resolution for downstream tests. The cost is operational: every existing hypothesis would need its labels updated, and the train/validate split rebalanced.

### 7.2. H02d — extended lead-up window for spike precursor

The H02b specificity check also identified that 34% of false-positive spike-firing windows are within ±14 days of an actual crash episode but outside the 3-day lead-up window. The spike-precursor signal may extend further than we tested. An H02d hypothesis with a 7- or 10-day lead-up window is queued.

### 7.3. H04b — body-battery intra-day decoding

Body-battery is exposed in the GDPR dump only as daily aggregates (chargedValue, drainedValue, three timestamped HIGHEST/LOWEST/MOSTRECENT points). The participant has identified that *within-day BB rise events* (corresponding to naps, deliberate rest, restorative moments) and *sharp drop events* (corresponding to discrete stress moments) are conceptually meaningful but cannot be tested with daily data. Per-minute body battery is likely encoded in the undocumented FIT message type 233 (`unknown_233`), which the broader FIT-reverse-engineering community has not mapped. A focused decoding effort is queued.

### 7.4. H05b — recovery time with sustained-recovery target

The H05 pre-registered recovery target (within 1 point of pre-crash baseline) was structurally always met. A revised target (≥ 2 consecutive days at or above pre-crash baseline) is queued.

### 7.5. The shielder-vs-reliever experiment

The pacing literature's open question — whether interventions (naproxen, low-dose naltrexone, antihistamine combinations, salt-loading, prophylactic rest) function as "shielders" (taken before exertion to blunt PEM) or "relievers" (taken during a crash to shorten it) — is the eventual ambition of this work. It requires:

- An `interventie` category in the notes dictionary (planned dictionary v3 / v4).
- A working H05b recovery-time metric.
- Sufficient instance counts of each intervention to permit comparison.

We anticipate this experiment becoming feasible during the participant's continued tracking, with first analyses possible in 2027 if intervention tracking starts in 2026.

### 7.6. Notes dictionary v3 — polarity-marker negation

A small but real fix: the v2 polarity layer does not apply the 3-word negation window that the symptom layer does, causing "het is echt niet fijn" to fire `polarity_positive`. Estimated to affect 1–2 false-positive classifications per analysis run. Cheap to fix.

---

## 8. Conclusion

In this n-of-1 investigation across ~5 years of wearable data and ~3.7 years of overlapping daily subjective tracking, **daily-aggregate wearable signals were found to be uninformative as crash precursors** for this Long COVID patient at the post-stabilisation stage. Sub-day-level signals (per-minute stress spike duration) carried real and discriminative information about pre-stabilisation crashes but lost that information across the 2023–2024 recovery transition. Concurrently, the *kind* of crash the participant experiences has shifted across seven independent axes, with residual crashes being fewer, shallower, shorter, more severe in their physical-symptom signature, more often paired with caregiving context, increasingly embedded in mixed days rather than totalizing them, and preceded by less symptom-warning language.

For app design, this argues against predictive-alert features and for retrospective-narrative features that help the participant *see* the multi-axis recovery story across his data. Of these, a stabilisation-arc card carrying the seven-axis finding and a mixed-day topology card surfacing the late-era recovery framing emerge as the highest-confidence candidates.

Methodologically, the investigation surfaced lessons on pre-registration discipline in small-sample integer-valued metrics, on the importance of dry inspection before spec lock, and on the value of looking at actual data behind every striking statistic. The "LLM as cartographer" pattern — using a language model to draft a deterministic phrase dictionary that is then committed to version control and applied by plain code — proved a sound compromise between LLM flexibility and reproducible analytical rigour.

The proposed `crash_v2` refinement (incorporating sub-threshold dips) is the most promising single next step and would tighten every existing analysis while approximately doubling the labelled-event set. The longer-term ambition is the shielder-vs-reliever intervention experiment that this entire investigation lays the groundwork for.

---

## References

[^1]: National Institute for Health and Care Excellence (NICE). *Myalgic encephalomyelitis (or encephalopathy) / chronic fatigue syndrome: diagnosis and management.* NG206, 2021. https://www.nice.org.uk/guidance/ng206

[^2]: Workwell Foundation. *Pacing with a heart rate monitor to minimize post-exertional malaise (PEM) in ME/CFS and Long COVID.* https://workwellfoundation.org/pacing-with-a-heart-rate-monitor/

[^3]: Long COVID Physio. *Pacing.* https://longcovid.physio/pacing

[^4]: Solve M.E. *Using a heart rate monitor to prevent post-exertional malaise in ME/CFS.* https://solvecfs.org/

[^5]: *Wearable technology in the management of complex chronic illness: survey results.* PMC, 2025. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12541780/

[^6]: Ruijgt C, et al. *Wearable HRV monitoring identifies autonomic dysfunction and thresholds for PEM in Long COVID.* medRxiv preprint, 2025. https://www.medrxiv.org/content/10.1101/2025.03.18.25320115v1

[^7]: Sanal-Hayes NEM, et al. *A scoping review of 'pacing' for management of ME/CFS: lessons for the long COVID pandemic.* 2023. https://pmc.ncbi.nlm.nih.gov/articles/PMC10576275/

**Internal project documents referenced:**

- [docs/research/garmin/README.md](garmin/README.md) — Garmin GDPR dump inventory and FIT file classification.
- [docs/research/garmin/hypotheses/registry.md](garmin/hypotheses/registry.md) — Hypothesis registry with status of all tests.
- [docs/research/garmin/hypotheses/synthesis.md](garmin/hypotheses/synthesis.md) — Living synthesis document.
- [docs/research/garmin/hypotheses/00-crash_v1-counts/counts.md](garmin/hypotheses/00-crash_v1-counts/counts.md) — Preflight definition lock.
- [docs/research/garmin/hypotheses/H01-rhr-drift/](garmin/hypotheses/H01-rhr-drift/) through [H05-recovery-time/](garmin/hypotheses/H05-recovery-time/) — Individual hypothesis test artefacts.
- [docs/research/garmin/hypotheses/H02b-stress-spikes/specificity-check.md](garmin/hypotheses/H02b-stress-spikes/specificity-check.md) — Specificity audit of the spike precursor.
- [docs/research/garmin/hypotheses/S01-stabilisation-trajectories/notes.md](garmin/hypotheses/S01-stabilisation-trajectories/notes.md) — Trajectory analysis.
- [docs/research/garmin/hypotheses/K01-crash-depth/result.md](garmin/hypotheses/K01-crash-depth/result.md) and [K02-crash-duration/result.md](garmin/hypotheses/K02-crash-duration/result.md) — Kind-of-crash tests.
- [docs/research/notes/01-language-around-crashes/notes-summary.md](notes/01-language-around-crashes/notes-summary.md) — Initial word-frequency analysis.
- [docs/research/notes/02-categorize-clauses/category_dictionary_v2.md](notes/02-categorize-clauses/category_dictionary_v2.md) — Locked three-layer notes-language dictionary.
- [docs/research/notes/02-categorize-clauses/categories-analysis-v2.md](notes/02-categorize-clauses/categories-analysis-v2.md) — Clause-level analysis results.
- [docs/research/notes/02-categorize-clauses/verification-late-positive.md](notes/02-categorize-clauses/verification-late-positive.md) — Mixed-day-topology verification.
- [docs/research/STOCKTAKE.md](STOCKTAKE.md) — Compact research stocktake snapshot.

**Project domain documents:**

- [docs/app_brief_gevoelscore.md](../app_brief_gevoelscore.md) — gevoelscore app brief.
- [docs/research/pacing-and-crash-mitigation.md](pacing-and-crash-mitigation.md) — Pacing and crash mitigation research note (literature review + the shielder-vs-reliever framing).
- [docs/research/pais-pem-literature-review.md](pais-pem-literature-review.md) — Literature scan on PAIS/PEM mechanisms.
- [docs/research/import-feature-sketch.md](import-feature-sketch.md) — The cartographer-not-driver principle for LLM-assisted research.

---

*Report compiled 2026-06-05 from individual hypothesis result files and synthesis. Living document — will be revised as `crash_v2`, H02d, H04b, H05b, and dictionary v3 mature.*
