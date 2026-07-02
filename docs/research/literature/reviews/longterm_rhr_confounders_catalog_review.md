# What Drives Resting Heart Rate Over the Long Term? An External, Literature-Gated Catalog of Candidate Multi-Year RHR Confounders

*Evidence retrieved from PubMed/PMC and web literature search (DOIs linked throughout). Purpose: this review supplies the a-priori, literature-determined catalog of things that move RESTING HEART RATE (RHR) over the LONG TERM (months to years), so that a multi-year wearable RHR trend can have its non-Long-COVID components modeled out only where the literature genuinely supports a driver. It is built BLIND to the project's own RHR curve so the confounder set is literature-gated, not fitted. For each candidate it states DIRECTION, MAGNITUDE (bpm where available), TIMESCALE, and whether the driver is a plausible multi-YEAR TREND term or a cyclic/noise term.*

**No-project-data line.** This review reads NO project n=1 data. Every number below is from published population/physiology literature. It is the external prior against which a multi-year RHR trend will be interpreted, not evidence from this body.

**Scope boundary (do not re-derive).** Two large confounders are covered by SEPARATE reviews and are only cross-referenced here, not re-derived: (1) cardiorespiratory fitness / training / detraining / deconditioning, in [`training_bradycardia_detraining_rhr_review.md`](training_bradycardia_detraining_rhr_review.md); and (2) the deconditioning-vs-disease question. THIS review covers every OTHER long-term RHR driver. Where a candidate touches fitness (weight, non-exercise activity), it is treated as the confounder in its own right and the reader is pointed to the fitness review for the training axis.

---

## The catalog (deliverable 1, the key output)

Support labels: **strong** = multiple human studies / meta-analytic or large-cohort backing and a clear mechanism; **moderate** = consistent but smaller / fewer / more indirect; **weak** = sparse or mechanism-only; **contested** = studies disagree in sign or size. Trend-vs-cyclic is the load-bearing column: it says whether the driver can masquerade as a slow multi-year drift (must-model-out) or averages away over a year (cyclic/noise).

| # | Confounder | Support | Direction on RHR | Magnitude (bpm) | Timescale | Multi-year TREND driver, or cyclic/noise? |
|---|---|---|---|---|---|---|
| 1 | **Aging** | strong | Lowers, then plateaus in adulthood (RHR falls from childhood into adulthood; near-flat across mid-adulthood) | Small: on the order of ~1.5 bpm per decade lower in adult cross-sections; life-course RHR decreases then plateaus | Decades | **Weak trend term** over a few years (near-flat in adulthood). Real but very slow; small over a multi-year window. |
| 2 | **Body weight / adiposity / BMI** | strong | Higher weight raises RHR; weight loss lowers it | ~0.3 bpm lower per 1 kg/m2 lower BMI (life-course); intervention weight loss lowers RHR ~5 bpm (modest loss) up to ~11 bpm (bariatric) | Months to years (tracks the weight trajectory) | **STRONG trend driver.** Weight change is slow and monotonic-ish, so it aliases directly onto a multi-year RHR trend. Must model out. |
| 3 | **Citalopram / SSRIs** | strong (citalopram-on-RHR); mixed (HRV) | **Citalopram LOWERS resting HR** | **Up to ~8 bpm lower** (citalopram, large ECG safety dataset) | Onset over weeks; persists while on drug; a step/level change at initiation | **STRONG trend/step driver.** A drug started partway through the record imposes a persistent downward level shift. Must model out (as a change-point). |
| 4a | **Beta-blockers** | strong | Lower RHR | Large: commonly ~10-15 bpm lower at rest (dose-dependent) | Persists while on drug | **STRONG step driver** IF present. Candidate to check for exposure, not assumed. |
| 4b | **Thyroid medication / thyroid state** | strong | Hyperthyroid or over-replacement raises RHR; hypothyroid or under-replacement lowers it | ~10-20 bpm shift across the hypo/hyper range | Weeks to months after a thyroid-state or dose change | **STRONG driver IF thyroid status changes.** See also #11. Candidate to check. |
| 4c | **Stimulants (incl. some ADHD meds, decongestants, high nicotine)** | moderate | Raise RHR | Variable, few bpm to >10 acutely | Acute-to-subacute; persistent only with chronic use | Trend driver only if chronic exposure changes. Candidate to check. |
| 5 | **Seasonality / ambient temperature** | strong | Winter higher, summer lower | ~2 bpm peak-to-trough (population), min ~July, max ~January (N. hemisphere) | Annual cycle | **CYCLIC, not a trend.** Averages out over full years; a within-year confounder / phase term, not a multi-year drift. Model as seasonal term, not trend. |
| 6 | **Alcohol (habitual)** | moderate | Raises RHR (esp. nocturnal) | ~+3 bpm nocturnal during regular-drinking phase vs abstinent (moderate intake); dose-dependent | Days (reversible) to as-long-as intake persists | **Trend driver IF drinking level changes over the record; otherwise cyclic/level.** Model out only if a sustained intake change occurred. |
| 7 | **Chronic sleep duration / debt** | moderate | Short/poor sleep associates with higher RHR | Few bpm across sleep-quality contrasts; night-to-night coupling weak-to-moderate | Days (state) to chronic if sleep pattern shifts | **Mostly noise / weak trend.** Only a trend driver if a durable sleep-pattern change occurred. Otherwise short-term variance. |
| 8 | **Chronic psychological / life stress** (ACTUAL emotional stress, NOT a wearable "stress score") | weak-to-moderate, contested | Sustained stress tends to raise basal HR; effect is small and entangled with mood | Small (a few bpm at most on basal HR); direction can blunt/flatten rather than simply raise | Weeks to months | **Weak/uncertain trend driver.** Carry as a caveat, do not over-weight. Distinct from any device "stress" metric (see note). |
| 9 | **Non-exercise physical activity (steps / NEAT)** | moderate | More habitual activity associates with lower HR-per-step / lower RHR | Direction clear; bpm attribution to RHR imprecise (entangled with fitness) | Months (habit level) | **Trend driver, but largely the fitness axis.** Overlaps #cross-ref training review; model via the fitness channel, avoid double-counting. |
| 10a | **Caffeine (habitual)** | moderate | Acute rise; **habitual RHR effect blunted by tolerance** | Small/negligible on habitual resting HR once tolerant | Acute; chronic effect small | **Mostly noise.** Not a credible multi-year trend driver unless intake changes drastically. |
| 10b | **Nicotine / smoking** | strong | Smoking raises RHR; cessation lowers it | ~10-13 bpm lower during abstinence vs smoking | Acute per-cigarette; a step change at quit/start | **STRONG step driver IF smoking status changes.** Otherwise a stable offset. Candidate to check. |
| 11 | **Clinical drivers: thyroid dysfunction, anemia / iron status, other systemic illness** | strong | Hyperthyroid/anemia raise RHR; hypothyroid lowers | Thyroid ~10-20 bpm across range; anemia raises RHR (compensatory tachycardia), magnitude scales with severity | Months (as the condition evolves/resolves) | **STRONG driver IF a condition is present/changing.** Episodic, not smooth; model as event/period if documented. Candidate to check. |
| 12 | **Wearable measurement / device artifact** | moderate-to-strong (as a caution) | Can bias either way; firmware/algorithm/device-generation changes shift the estimate | Resting MAE ~2 bpm at rest; systematic per-device biases and firmware-version effects documented | Step changes at firmware/device swaps; slow skin-perfusion seasonality | **REAL multi-year confounder.** Device/firmware changes can create spurious step or drift. Must be controlled (hold device constant, log firmware). |
| 13 | **Menstrual cycle** (sex-specific) | strong (where applicable) | Luteal phase higher than menstrual/follicular | ~2-4 bpm luteal-vs-menstrual (e.g. +3.8 bpm mid-luteal) | ~Monthly cycle | **CYCLIC, sex-dependent.** Not a multi-year trend; a within-month oscillation. Flag as applicable only to menstruating participants. |

---

## Per-confounder synthesis (with citations)

### 1. Aging: real but very slow; near-flat in adulthood

According to PubMed, a life-course cohort followed the same individuals' RHR on 8 occasions from age 6 to 69 (MRC National Survey of Health and Development, N=4,779, ~26,000 observations) and found **mean RHR decreases with increasing age and plateaus in adulthood** ([O'Hare et al., 2018, *JAMA Pediatr*; DOI](https://doi.org/10.1001/jamapediatrics.2017.5525)). Consumer-scale cross-sections put the adult age slope near ~1.5 bpm lower per decade (Health eHeart Study, reported via wearable-cohort literature). **Read for a multi-year trend:** over a few years within adulthood, aging contributes at most ~a fraction of a bpm and is essentially flat, so it is a real but negligible trend term on this timescale. Keep as a low-weight covariate, not a primary confounder.

### 2. Body weight / adiposity / BMI: strong, slow, must model out

The same life-course cohort found **-0.30 bpm per 1 kg/m2 higher conditional BMI change** across the life course ([O'Hare et al., 2018, *JAMA Pediatr*; DOI](https://doi.org/10.1001/jamapediatrics.2017.5525)). Intervention studies confirm the direction and give the magnitude: an aerobic-exercise weight-loss program lowered RHR by **-4.8 bpm** even in lower-than-expected weight-loss responders ([King et al., 2009, *Br J Sports Med*; DOI](https://doi.org/10.1136/bjsm.2009.065557)); a diet-plus-activity follow-up lowered seated RHR by **~5-8.5 bpm** ([Doucet et al., 1999, *Obes Res*; DOI](https://doi.org/10.1002/j.1550-8528.1999.tb00415.x)); and surgically-induced weight loss (mean -28.6 kg, no training) lowered RHR by **-11.3 bpm** ([Onofre et al., 2021, *Obes Surg*; DOI](https://doi.org/10.1007/s11695-021-05782-3)). **Read for a multi-year trend:** body-weight trajectories move slowly and roughly monotonically over months-to-years, so weight change aliases almost perfectly onto a multi-year RHR trend. **This is a strong must-model-out confounder.** (Some of its effect is mediated through fitness; see the training review to avoid double-counting.)

### 3. Citalopram / SSRIs: LOWERS RHR, up to ~8 bpm (the participant's initiation is a step change)

This is the single most decision-relevant pharmacological confounder because the participant started citalopram partway through the record. The direction and magnitude are established in the sister review: a large prospective+retrospective ECG safety analysis (>6,000 ECGs, 1,789 citalopram patients) found the **only consistent cardiac effect of citalopram was a small heart-rate REDUCTION of up to ~8 bpm**, with no effect on conduction intervals (Rasmussen et al., 1999, *J Clin Psychopharmacol*; see [`ssri_citalopram_hrv_review.md`](ssri_citalopram_hrv_review.md)). A small resting bradycardia is the most reproducible autonomic fingerprint of citalopram. The HRV side is mixed and design-dependent (Fiani 2023 meta-analysis; Kemp 2016), also detailed in that sister review. **Read for a multi-year trend: a persistent downward LEVEL/step shift of up to ~8 bpm from the initiation date onward. This is a strong must-model-out confounder and should be handled as a change-point at drug start, not a smooth slope.** Direction is DOWN, which matters: it works OPPOSITE to any Long-COVID-attributable RHR elevation and would mask part of it if not modeled.

### 4. Other cardioactive exposures: candidates to check, not assumed

- **Beta-blockers** lower resting HR substantially (commonly ~10-15 bpm at rest, dose-dependent); a clear, large step driver where present. Candidate exposure to check.
- **Thyroid state / thyroid medication** shifts RHR by roughly 10-20 bpm across the hypo-to-hyper range; hyperthyroidism raises HR ~20 bpm above normal across 24h, hypothyroidism lowers it ~10-20 bpm ([Klein & Danzi, 2007, *Circulation*; DOI](https://doi.org/10.1161/CIRCULATIONAHA.106.678326)). See also #11.
- **Stimulants** (some ADHD medications, sympathomimetic decongestants) raise RHR; relevant only as a persistent trend term if chronic use starts/stops.

**Read:** each is a strong or moderate driver IF the exposure is present and changes; treat as a-priori candidates to check against the participant's medication history, not as assumed active confounders.

### 5. Seasonality / ambient temperature: CYCLIC, not a trend

The landmark wearable evidence is a retrospective longitudinal cohort of **92,457 adults** wearing wrist trackers (~33 million daily RHR values). It found **RHR seasonality with a minimum in July and a maximum in January** (Northern hemisphere), a small but significant seasonal swing on the order of ~2 bpm ([Quer et al., 2020, *PLoS One*; DOI](https://doi.org/10.1371/journal.pone.0227709)). **Read for a multi-year trend: this is a CYCLIC (annual) term, not a trend driver.** Over full years it averages out; it only biases a trend if the record starts and ends in different seasons or is unevenly sampled across the year. Model it as a seasonal/phase covariate, not a slope. This is the cleanest example of a confounder that must NOT be treated as a trend.

### 6. Alcohol (habitual): moderate; a trend driver only if intake level changes

A prospective smartwatch study (40 healthy adults, structured baseline / exposure / post-exposure design) found moderate alcohol intake raised **nocturnal resting HR by +3.0 bpm** (63.6 to 66.6 bpm) during the drinking phase, with rapid normalization on cessation ([Strüven et al., 2025, *Nutrients*; DOI](https://doi.org/10.3390/nu17091470)). **Read:** the effect is real and reversible on a days scale. It becomes a multi-year TREND confounder only if the participant's habitual drinking LEVEL changed durably over the record; a stable drinking habit is a level offset, and episodic drinking is short-term variance. Model out only if a sustained intake change is documented.

### 7. Chronic sleep duration / quality: mostly noise, weak trend

Sleep and resting HR are coupled but the coupling is weak-to-moderate and mostly short-term. A multiple N-of-1 study in police officers found bidirectional but weak-to-moderate, participant-inconsistent associations between wearable sleep and resting HRV/HR ([de Vries et al., 2022, *Sensors*; DOI](https://doi.org/10.3390/s23010332)); an HRV-sleep study similarly tied poorer sleep to autonomic shifts under stress load ([Chalmers et al., 2022, *Int J Environ Res Public Health*; DOI](https://doi.org/10.3390/ijerph19095770)). **Read:** night-to-night sleep is largely a short-term variance source on RHR, not a smooth multi-year driver. It becomes a weak trend term only if a durable sleep-pattern change occurred (e.g. chronic insomnia onset). Otherwise treat as noise, not trend.

### 8. Chronic psychological / life stress: weak/contested; and a NAMING CAUTION

**Naming caution (kept explicit):** "psychological / life stress" here means ACTUAL sustained emotional or life stress, measured by validated instruments (e.g. Perceived Stress Scale) or life-events. This is DISTINCT from any wearable "stress score," which is an HRV-derived device index, not a measure of felt emotional stress. The two must never be conflated in this project's framing. (Consistent with the project convention that a Garmin "stress" score is an HRV-derived measure, not mental stress.)

On the actual construct: evidence that sustained psychological stress moves BASAL resting HR is weaker and more contested than intuition suggests. A working-population study (SWEET, N up to 1,002, 5-day ECG) found that **high/extreme chronic stress ALONE produced only a limited increase in basal HR**, and that the clearer HR-circadian effects appeared only when depressive symptoms were also present; chronic stress by itself did not robustly move night-time RMSSD ([Lutin et al., 2022, *Front Psychiatry*; DOI](https://doi.org/10.3389/fpsyt.2022.1022298)). **Read:** carry chronic psychological stress as a small, uncertain, caveat-level trend driver (a few bpm at most on basal HR, direction not always simply upward), not a strong must-model-out term. Do not inflate it.

### 9. Non-exercise physical activity (steps / NEAT): real, but largely the fitness axis

Habitual daily activity tracks cardiac metrics: in the All of Us wearable cohort, a "daily heart rate per step" metric (average daily HR divided by steps) correlated with fitness and cardiovascular outcomes, i.e. more habitual activity maps to a more favorable HR profile ([Master et al. / All of Us DHRPS, 2025, *J Am Heart Assoc*; DOI](https://doi.org/10.1161/JAHA.124.036801)); large longitudinal All of Us wearable analyses further show activity metrics carry stable disease associations over 1-year windows ([Fulda et al., 2026, *medRxiv* preprint; DOI](https://doi.org/10.64898/2026.01.29.26344899)). **Read:** habitual activity level is a genuine slow driver, but its RHR effect runs largely through cardiorespiratory fitness, which is the SEPARATE fitness review's territory. Model it via the fitness channel to avoid double-counting; do not add an independent NEAT trend term on top of the fitness term without justification.

### 10. Caffeine and nicotine: split verdict

- **Caffeine (habitual):** the acute pressor/HR effect is real, but **habitual users develop cardiovascular tolerance**, so chronic caffeine has little persistent effect on resting HR at a stable intake (habituation literature; overnight abstinence largely restores sensitivity). **Read: mostly noise, not a multi-year trend driver** unless habitual intake changes drastically.
- **Nicotine / smoking:** strong and directional. Resting HR is **~10-13 bpm lower during smoking abstinence than during smoking as usual** (13.4 bpm lower without NRT, 10.4 with NRT) ([Herbec et al., 2020, *Nicotine Tob Res*; DOI](https://doi.org/10.1093/ntr/ntaa021)). **Read: a strong STEP driver IF smoking status changes** (quit or start) during the record; a stable smoking habit is a fixed offset. Candidate to check.

### 11. Clinical drivers: thyroid, anemia, systemic illness: strong where present

Thyroid dysfunction is one of the largest reversible RHR levers: hyperthyroidism raises HR ~20 bpm across 24h, hypothyroidism lowers it ~10-20 bpm, and restoring euthyroid state reverses it ([Klein & Danzi, 2007, *Circulation*; DOI](https://doi.org/10.1161/CIRCULATIONAHA.106.678326)). Anemia / low iron drives compensatory tachycardia; low iron storage and mild anemia are documented alongside elevated standing HR in autonomic-intolerance cohorts ([Jarjour & Jarjour, 2013, *Clin Auton Res*; DOI](https://doi.org/10.1007/s10286-013-0198-6)). **Read:** these are strong drivers IF a condition is present or changing, but they act as EPISODES/PERIODS (onset, treatment, resolution) rather than smooth slopes. Model as event/period covariates where documented; carry as a-priori candidates to check against labs/history. (Note: these overlap Long COVID itself, which can produce dysautonomia; iron/thyroid status must be checked to avoid attributing a treatable clinical shift to Long COVID.)

### 12. Wearable measurement / device artifact: a REAL multi-year confounder

Consumer wearables measure RHR reasonably well at rest (mean absolute error ~2 bpm), but the estimate is NOT guaranteed stable across years. Manufacturers use proprietary optical-to-HR algorithms that **change with firmware updates**, and studies frequently fail to report firmware version, producing reproducibility problems; device-generation and per-device systematic biases are documented, and legacy Garmin optical data specifically has been flagged for systematic bias in autonomic estimation (2025 consumer-wearable validation literature; guide-to-consumer-wearables reviews). **Read: device/firmware/algorithm changes can inject spurious STEP changes or slow drift into a multi-year wearable RHR trend, independent of physiology.** This is a genuine trend confounder and must be controlled by holding the device constant, logging firmware, and treating device/firmware swaps as candidate change-points. (See the sister device-validity review [`wearable_validity_lc_mecfs_review.md`](wearable_validity_lc_mecfs_review.md) for in-population validity.)

### 13. Menstrual cycle (sex-specific): CYCLIC, flag where applicable

A prospective wearable study (91 women, 274 ovulatory cycles, wrist PPG during sleep) found **pulse rate ~3.8 bpm higher in the mid-luteal phase than the menstrual phase**, and ~2.1 bpm higher in the fertile window, robust to confounders ([Shilaih et al., 2017, *Sci Rep*; DOI](https://doi.org/10.1038/s41598-017-01433-9)). **Read: a within-month CYCLIC oscillation (~2-4 bpm), not a multi-year trend.** It is sex-dependent and applies only to menstruating participants; where applicable, treat as a monthly phase term. It averages out over long windows and does not produce trend, but can add structured monthly variance.

---

## Short synthesis: what MUST be modeled out of a multi-year RHR trend

**The must-model-out set (STRONG and slow/trending or step-like enough to alias onto a multi-year trend):**

1. **Body weight / adiposity change**: strong, slow, monotonic-ish; ~0.3 bpm per BMI unit, up to ~11 bpm across large weight change. The prototypical multi-year RHR trend confounder.
2. **Citalopram initiation**: persistent DOWNWARD step of up to ~8 bpm from the start date; opposite in sign to a Long-COVID rise, so it masks rather than mimics. Model as a change-point.
3. **Device / firmware / algorithm changes**: can inject spurious steps or drift into the wearable estimate itself; hold device constant, log firmware, treat swaps as change-points.
4. **Any changing cardioactive exposure** (beta-blockers, thyroid medication/thyroid state, smoking status, chronic stimulants): each a strong step/level driver of 10-20 bpm IF the exposure changes; a-priori candidates to check against medication and clinical history.
5. **Changing clinical state** (thyroid dysfunction, anemia/iron): strong but episodic; model as periods where documented; must be checked so a treatable clinical shift is not misattributed to Long COVID.

**Cyclic or within-year terms (model as phase/season, NOT as trend):**

- **Seasonality** (~2 bpm, min July / max January): annual cycle, averages out over full years; only biases a trend under uneven seasonal sampling.
- **Menstrual cycle** (~2-4 bpm luteal-vs-menstrual, sex-specific): monthly cycle, no trend contribution.

**Mostly noise / weak / conditional (do not inflate):**

- **Aging**: real but ~flat in adulthood over a few years; low-weight covariate.
- **Alcohol, chronic sleep, habitual caffeine**: mostly short-term variance; each becomes a trend term ONLY if the habitual LEVEL changed durably over the record.
- **Chronic psychological stress (the real construct, not a device score)**: weak and contested for basal RHR; carry as a caveat, a few bpm at most.
- **Non-exercise activity**: real, but runs mostly through the fitness axis (separate review); avoid double-counting.

**One-line deliverable:** over a multi-year wearable RHR trend, the confounders slow or step-like enough to genuinely alias onto the trend, and therefore that MUST be modeled out, are **body-weight change, citalopram initiation (down, up to ~8 bpm), device/firmware changes, and any changing cardioactive drug or clinical (thyroid/anemia) state**; seasonality and the menstrual cycle are **cyclic** terms to be modeled as phase not trend; aging, alcohol, sleep, caffeine, and real psychological stress are **weak or conditional** and should not be inflated.

---

## Honest flags where evidence is thin or contested

- **Chronic psychological stress on BASAL resting HR is weaker than folk intuition.** The best working-population evidence found chronic stress alone barely moved basal HR; the effect emerged mainly with co-present depressive symptoms ([Lutin et al., 2022; DOI](https://doi.org/10.3389/fpsyt.2022.1022298)). Do not treat sustained stress as a strong RHR trend driver, and never substitute a wearable "stress score" for it.
- **Alcohol's LONG-TERM (as opposed to acute/nocturnal) resting-HR effect is under-quantified.** The cited +3 bpm is an acute, reversible nocturnal effect ([Strüven et al., 2025; DOI](https://doi.org/10.3390/nu17091470)); whether a stable habitual intake produces a persistent daytime-RHR offset over years is less cleanly established.
- **Non-exercise activity's independent RHR contribution is hard to separate from fitness.** The activity literature is largely fitness- and outcome-focused; attributing specific bpm to steps/NEAT net of fitness is imprecise.
- **Device drift magnitude over years is not cleanly calibrated.** The confound is real (firmware/algorithm/device-generation effects are documented) but no retrieved study gives a clean "bpm of drift per firmware version" figure; treat it qualitatively as a change-point risk, not a calibrated coefficient.
- **Aging slope in adulthood is small and cohort-dependent** (~1.5 bpm/decade cross-sectionally; life-course curves plateau), so its multi-year contribution is minor and should not be over-fit.
- **Beta-blocker / stimulant magnitudes here are stated from general pharmacology, not a single retrieved trial**, and are offered as candidate-to-check drivers rather than precisely-cited coefficients.
- Purposive (not systematic) PubMed/PMC + web search, run 2026-06-30 to 2026-07-02. Landmark-and-representative papers, not an exhaustive review.

---

## Proposed `/reading` block (citable sources)

```
/reading
- O'Hare C, Kuh D, Hardy R (2018). "Association of Early-Life Factors With Life-Course Trajectories of Resting Heart Rate: More Than 6 Decades of Follow-up." JAMA Pediatr 172(4):e175525. PMID 29435577, DOI 10.1001/jamapediatrics.2017.5525. Life-course RHR decreases then plateaus in adulthood; -0.30 bpm per 1 kg/m2 conditional BMI change. Anchors AGING (slow/flat) and WEIGHT (slow trend).
- Onofre T, et al. (2021). "Assessment of Cardiorespiratory and Metabolic Responses in Women with Obesity After Surgically Induced Weight Loss." Obes Surg 32(2):318-324. PMID 34780025, DOI 10.1007/s11695-021-05782-3. Bariatric weight loss (-28.6 kg, no training) lowered RHR -11.3 bpm. Upper-bound weight-loss RHR magnitude.
- King NA, et al. (2009). "Beneficial effects of exercise: shifting the focus from body weight to other markers of health." Br J Sports Med 43(12):924-7. PMID 19793728, DOI 10.1136/bjsm.2009.065557. Weight-loss/exercise lowered RHR -4.8 bpm. Mid-range weight magnitude.
- Doucet E, et al. (1999). "Physical activity and low-fat diet ... following weight loss." Obes Res 7(4):323-33. PMID 10440588, DOI 10.1002/j.1550-8528.1999.tb00415.x. Diet+activity lowered seated RHR ~5-8.5 bpm. Weight-loss magnitude corroboration.
- Rasmussen SL, et al. (1999). "Cardiac safety of citalopram ..." J Clin Psychopharmacol 19(5):407-15. (See ssri_citalopram_hrv_review.md for full cite.) Citalopram's only consistent cardiac effect: HR reduction up to ~8 bpm. THE citalopram-on-RHR anchor: direction DOWN, step change at initiation.
- Klein I, Danzi S (2007). "Thyroid disease and the heart." Circulation 116(15):1725-35. PMID 17923583, DOI 10.1161/CIRCULATIONAHA.106.678326. Thyroid state shifts RHR ~10-20 bpm across hypo/hyper range; reversible. Anchors thyroid (drug/clinical) driver.
- Quer G, Gouda P, Galarnyk M, Topol EJ, Steinhubl SR (2020). "Inter- and intraindividual variability in daily resting heart rate ... 92,457 adults." PLoS One 15(2):e0227709. PMID 32023264, DOI 10.1371/journal.pone.0227709. Wearable RHR seasonality: min July, max January, ~2 bpm. THE seasonality-is-cyclic anchor.
- Strüven A, et al. (2025). "The Impact of Alcohol on Sleep Physiology: ... Nocturnal Resting Heart Rate Using Smartwatch Technology." Nutrients 17(9):1470. PMID 40362779, DOI 10.3390/nu17091470. Moderate alcohol raised nocturnal RHR +3 bpm, reversible. Alcohol magnitude/timescale.
- Herbec A, et al. (2020). "Decrease in Resting Heart Rate ... to Verify Abstinence From Smoking." Nicotine Tob Res 22(8):1424-1427. PMID 31971595, DOI 10.1093/ntr/ntaa021. Smoking abstinence lowered RHR 10.4-13.4 bpm. Nicotine/smoking step-driver anchor.
- Lutin E, et al. (2022). "The cumulative effect of chronic stress and depressive symptoms affects heart rate in a working population." Front Psychiatry 13:1022298. PMID 36311512, DOI 10.3389/fpsyt.2022.1022298. Chronic stress ALONE barely moved basal HR; effect needed co-present depressive symptoms. The "don't inflate psychological stress" anchor.
- Shilaih M, et al. (2017). "Pulse Rate Measurement During Sleep Using Wearable Sensors, and its Correlation with the Menstrual Cycle Phases." Sci Rep 7(1):1294. PMID 28465583, DOI 10.1038/s41598-017-01433-9. Mid-luteal pulse +3.8 bpm vs menstrual. Menstrual-cycle cyclic anchor (sex-specific).
- de Vries HJ, et al. (2022). "Wearable-Measured Sleep and Resting Heart Rate Variability as an Outcome of and Predictor for Subjective Stress." Sensors 23(1):332. PMID 36616929, DOI 10.3390/s23010332. Weak/inconsistent sleep-RHR coupling. Sleep-is-mostly-noise anchor.
- All of Us DHRPS (2025). "Daily Heart Rate per Step: A Wearables Metric Associated With Cardiovascular Disease ... All of Us Research Program." J Am Heart Assoc, DOI 10.1161/JAHA.124.036801. Habitual activity maps to HR profile via fitness. Non-exercise-activity / fitness-axis anchor.
```

---

*Source databases: PubMed/PMC and web literature search. Findings paraphrased; consult primary papers (DOIs above) for methods and data. Research synthesis, not medical advice. Sister to [`training_bradycardia_detraining_rhr_review.md`](training_bradycardia_detraining_rhr_review.md) (fitness / detraining axis, cross-referenced not re-derived), [`ssri_citalopram_hrv_review.md`](ssri_citalopram_hrv_review.md) (citalopram HRV / mechanism), and [`wearable_validity_lc_mecfs_review.md`](wearable_validity_lc_mecfs_review.md) (device validity in-population). No project n=1 data was read in producing this catalog.*

*Claude (Opus 4.8) literature review, for the participant-researcher (repo owner).*
