# What Does an Acute Viral Infection Do to the Autonomic Wearable Signal? — A Cited Predicted-Direction Anchor for the Peri-Event COVID Check (R23)

*Evidence retrieved from PubMed/PMC (DOIs linked throughout). Purpose: this brief fixes the **predicted direction** of a pre-registered single-event peri-event test BEFORE the data is looked at, so the test stays **confirmatory, not data-fishing**. R23 asks whether the project's overnight autonomic factor (overnight Garmin GSS / body-battery / resting HR triad) visibly moved during the subject's ~14-day acute COVID infection of 2022-03. To pre-register a direction credibly, that direction must come from INDEPENDENT literature, which is what this review supplies. It anchors [`../../methodology/peri_event_known_event_check.md`](../../methodology/peri_event_known_event_check.md) **§6** and **decision (e)** (the tiered moved / ambiguous / moved-unexpected criterion).*

*Scope note: this is an n=1 instrument-test. "Predicted direction" means **what the population/physiology literature says an acute febrile viral infection does to these channels** — NOT what is proven for this body. The project's own n=1 data is NOT cited here as evidence; this review is the external prior the data is tested against. See [[findings-are-provisional]], [[site-is-medium-not-subject]].*

*Distinct from the three sister reviews: [`expected_shapes_autonomic_signals_review.md`](expected_shapes_autonomic_signals_review.md) (CHRONIC PEM curve shape / non-linearity), [`wearable_validity_lc_mecfs_review.md`](wearable_validity_lc_mecfs_review.md) (R24, in-population device validity), `ssri_citalopram_hrv_review.md` (R29). THIS review = the **ACUTE infection signature** during the days-to-2-weeks acute phase — a different topic from all three.*

---

## 1. Predicted-direction verdict (RQ1) — load-bearing, stated up top

Based on articles retrieved from PubMed, the acute phase of a febrile viral infection drives a **sympathetic-dominant, vagally-withdrawn** autonomic state, and this maps cleanly and consistently onto the three R23 factor channels. The single most explicit source is Natarajan 2020 (Fitbit, n=2745 COVID cases), which states the signature directly: **"Respiration rate and heart rate are typically elevated by illness, while HRV is decreased"** ([Natarajan et al., 2020, *npj Digit Med*; DOI](https://doi.org/10.1038/s41746-020-00363-7)).

| R23 channel | Primitive | Predicted direction during acute infection | Strength |
|---|---|---|---|
| **HA06b** `resting_hr` (resting heart rate) | overnight/resting HR | **UP** (elevated) | **Strong** — direct, multi-cohort wearable evidence |
| **HA07c** `sleep_stress_mean` (HRV-derived Garmin GSS, NOT mental stress) | overnight "stress" score | **UP** (elevated) — because GSS is an inverse HRV transform, and **HRV is decreased** in acute infection | **Moderate-strong** — direct on HRV; one inferential step (HRV↓ ⇒ GSS↑) |
| **HA10** `morning_bb_peak` (overnight recovery / body-battery) | overnight recovery | **DOWN** (suppressed) — body-battery is built from the same RHR + HRV/stress inputs and moves inversely to load | **Moderate** — inferred from the RHR↑/HRV↓ inputs that drive the BB algorithm; no study validates BB itself in acute infection |

**Composite prediction (the anchor for decision (e)):** an acute viral infection pushes the factor **toward the "high autonomic load" pole — resting HR up, HRV down (therefore Garmin GSS up), overnight recovery / body-battery down.** This is the pre-specified predicted direction; the "MOVED" tier of decision (e) is the predicted-direction tail of the matched-window null.

The mechanistic warrant is standard and prior to this corpus: febrile illness raises core temperature and inflammatory cytokine load, which elevate sinus rate and withdraw cardiac vagal tone, reducing HRV ([Gholami et al., 2012, *Shock*; DOI](https://doi.org/10.1097/SHK.0b013e318240b4be) — endotoxemic systemic inflammation reduces HRV by uncoupling the cardiac pacemaker from cholinergic neural control). The COVID-specific wearable cohorts (§2) confirm the same direction in the exact device class and resolution R23 uses.

---

## 2. The directly-relevant evidence (wearable infection-detection cohorts)

This is the body of literature that matches R23's situation most exactly: consumer wrist/finger wearables, daily/overnight resolution, acute respiratory viral infection, with the direction of movement reported.

- **Resting HR rises pre-symptomatically and at symptom onset (COVID).** In 32 COVID-19 cases from a ~5300-person cohort, Mishra/Snyder showed **elevations in resting heart rate** (relative to personal baseline) detectable in 81% of cases, often at or before symptom onset; the real-time alarm was built on **"extreme elevations in resting heart rate relative to the individual baseline"** ([Mishra et al., 2020, *Nat Biomed Eng*; DOI](https://doi.org/10.1038/s41551-020-00640-6)). Direction: **RHR up.** Resolution: daily/overnight RHR vs personal baseline — exactly R23's resolution.
- **The full triad direction, stated explicitly (COVID).** In 2745 COVID-positive subjects, **respiration rate and heart rate are elevated, HRV is decreased** during active infection; physiological signs alone predicted illness on a given day at AUC 0.77 ([Natarajan et al., 2020, *npj Digit Med*; DOI](https://doi.org/10.1038/s41746-020-00363-7)). Direction: **RHR up, HRV down** — the composite. This is the cleanest single citation for the whole RQ1 verdict.
- **HRV falls / its circadian pattern is disrupted around infection (COVID, Apple Watch).** In the Mount Sinai Warrior Watch study, the circadian amplitude of SDNN (an HRV metric) differed significantly in the 7 days around a COVID diagnosis vs uninfected periods, and changed at first symptom ([Hirten et al., 2021, *J Med Internet Res*; DOI](https://doi.org/10.2196/26107)). Direction: **HRV disturbed/reduced**, on the same wrist-device class. Note: the effect is on the *circadian pattern* of HRV, not a simple level shift — relevant to RQ2 below.
- **Resting HR rises with influenza-like illness, detectable at population scale from daily aggregates (influenza).** Across ~47,000 consistent Fitbit users, **elevated RHR and increased sleep** tracked CDC influenza-like-illness rates closely (state-level correlations 0.84–0.97) ([Radin et al., 2020, *Lancet Digit Health*; DOI](https://doi.org/10.1016/S2589-7500(19)30222-5)). Direction: **RHR up** (plus a sleep-duration change), from **daily RHR + sleep aggregates** — generalises the signature beyond COVID to febrile viral illness broadly.

**One vaccination-challenge corroboration (same direction, controlled trigger).** When the immune system is acutely activated by mRNA vaccination — a clean, dated inflammatory perturbation — the Oura cohort showed, on the night after the second dose, **increased resting heart rate, increased skin-temperature deviation, and decreased HRV and deep sleep** ([Mason et al., 2022, *Vaccines*, TemPredict; DOI](https://doi.org/10.3390/vaccines10020264)). This is not an infection, but it reproduces the predicted RHR↑/HRV↓ direction under a known-onset inflammatory stimulus, and shows the **recovery/sleep channel (HA10 analogue) suppressed** — the one channel the infection cohorts cover least directly.

---

## 3. Daily-aggregate detectability (RQ2) — does the signature show up at R23's resolution?

**Verdict: YES — the signature is detectable at daily / overnight-aggregate resolution; R23's design choice is validated, with one qualification.** Every directly-relevant source above operates at exactly the resolution R23 uses:

- Mishra 2020 and Radin 2020 both build their detectors on **daily resting HR vs personal baseline** — they do not require intraday/per-minute data to see the RHR rise ([Mishra; DOI](https://doi.org/10.1038/s41551-020-00640-6); [Radin; DOI](https://doi.org/10.1016/S2589-7500(19)30222-5)). Radin in particular recovers the signal from **nightly aggregates** of RHR and sleep.
- Natarajan 2020 reports the elevated-HR / decreased-HRV signature from **device-summarised daily metrics** ([DOI](https://doi.org/10.1038/s41746-020-00363-7)).

**Qualification (matches R23's §6 resolution caveat and the window-max companion in decision (d)):** the HRV signal in particular can express as a **change in the overnight/circadian pattern** rather than a flat 14-day mean shift ([Hirten 2021; DOI](https://doi.org/10.2196/26107)). And because the acute febrile phase is short (a few days) inside a 14-day window, a **single-day peak / spike metric can move more than the 14-day mean** — which is precisely why R23 (d) carries a window-max companion alongside the window-mean. So: daily-aggregate resolution is sufficient to *detect* the signature in this literature, but a mean over the full 14-day window may *dilute* a short acute spike — supporting both R23's primary daily-aggregate design and its spike/peak hedge.

---

## 4. The blunting / non-monotone caveat (RQ3) — how strong is it, honestly?

**Verdict: the caveat is REAL and physiologically grounded, but it is a SEVERITY-tier phenomenon (severe sepsis / critical illness), and the honest reading is that it is a MODERATE caveat for a mild-to-moderate home-recovered infection — strong enough to justify R23's tiered (not one-sided) criterion, but NOT strong enough to predict that the signal will actually invert in this case.**

The supporting evidence:

- **Mechanistic blunting is established.** Under systemic inflammation, the cardiac pacemaker becomes **hyporesponsive to cholinergic (vagal) stimulation**, partially **uncoupling the pacemaker from autonomic neural control** — which both reduces HRV *and* means the measured signal no longer faithfully tracks neural traffic ([Gholami et al., 2012, *Shock*; DOI](https://doi.org/10.1097/SHK.0b013e318240b4be)). At the extreme, the readout decouples from the underlying drive.
- **Severity deepens HRV suppression rather than reversing it (in the direction-of-load sense).** In ICU sepsis patients, HRV (SDNN, total power, LF) was **more reduced in non-survivors than survivors**, and low SDNN independently predicted mortality ([de Castilho et al., 2017, *PLoS One*; DOI](https://doi.org/10.1371/journal.pone.0180060)). Read onto the factor: greater severity = HRV *further* suppressed = factor pushed *further* toward the high-load pole, not flipped back.

**How to weigh this for R23.** The two pieces point in subtly different directions, and the honest synthesis matters for decision (e):
1. For **HRV/RHR level**, severity mostly *deepens* the predicted-direction move (de Castilho) — so for a mild-to-moderate infection the predicted high-load-pole direction is the safe bet.
2. The genuine **non-monotone / blunting** risk is narrower: at the most depleted point the measured signal can **decouple** from neural drive (Gholami), so a wearable's *derived* index (Garmin GSS / body-battery, which assume a normal HRV↔autonomic mapping) could **flatten or read paradoxically** exactly when the body is most stressed. This is a measurement-validity blunting, not a true autonomic reversal.

This is why R23's decision (e) is correctly **tiered** (MOVED / AMBIGUOUS / MOVED-UNEXPECTED) rather than strictly one-sided: a blunted or in-band result at the deepest point is a *physiologically expected shape*, not a failed test. But the caveat should not be over-weighted — the dominant, well-evidenced expectation for a home-recovered acute infection is the high-autonomic-load move; blunting is the documented-but-less-likely tail that the tiered criterion exists to catch. The companion chronic-curve review's "total autonomic dystonia" strand ([`expected_shapes_autonomic_signals_review.md`](expected_shapes_autonomic_signals_review.md) Strand 4) describes the same depletion-blunts-the-signal phenomenon from the chronic-exhaustion side; this acute review's contribution is that the blunting evidence is **severity-gated** and therefore a *moderate*, not a *strong*, caveat for a single mild-to-moderate event.

---

## 5. Reader synthesis (one paragraph)

Based on articles retrieved from PubMed, the acute phase of a febrile viral infection produces a **clear, consistent, daily-detectable autonomic signature in exactly the wearable-channel class R23 uses**: resting heart rate **up**, HRV **down** (hence the HRV-derived Garmin overnight "stress" score **up**), and overnight recovery / body-battery **down** — a coherent move toward the "high autonomic load" pole, reported directly in COVID Fitbit cohorts (Natarajan; Mishra), an influenza-scale Fitbit study (Radin), an Apple-Watch COVID cohort (Hirten), and a controlled vaccination challenge (Mason/TemPredict). This is the **pre-registered predicted direction** for R23's decision (e). The signature is recoverable from **daily/overnight aggregates** — R23 does not need intraday data to detect it — though a short acute spike inside a 14-day window can be diluted by a 14-day mean, vindicating R23's window-max companion. The one honest hedge is a **severity-gated blunting caveat**: at the most depleted point, systemic inflammation can decouple the cardiac pacemaker from neural control so that a *derived* wearable index flattens or reads paradoxically; this is real but is an ICU/sepsis-tier phenomenon, so for a mild-to-moderate home-recovered infection it is a **moderate** caveat — strong enough to justify the tiered criterion, not strong enough to predict an actual inversion. Net: pre-register the high-autonomic-load direction; keep the tiered criterion; treat blunting as the documented minority tail.

---

## 6. Honest limits

- **PubMed/PMC-only, English-language, purposive (not exhaustive) search**, run 2026-06-30. The wearable-infection-detection field is large; this is the landmark-paper core, not a systematic review.
- **No study validates Garmin's specific Firstbeat GSS or body-battery transform in acute infection.** The HA07c (GSS↑) and HA10 (body-battery↓) directions are **inferred** from the validated underlying inputs (HRV↓, RHR↑) that those proprietary indices are built from — one inferential step beyond the direct evidence. The R24 sister review ([`wearable_validity_lc_mecfs_review.md`](wearable_validity_lc_mecfs_review.md)) already flags that these derived indices are the least-validated channel; that caveat carries here. The strongest *direct* channel is RHR (HA06b).
- **The device generation differs.** The cited cohorts use Fitbit / Apple Watch / Oura; the subject's device is a Garmin FR245 with no direct HRV channel (factor is the GSS proxy per [`../../methodology/hrv_proxy_via_stress.md`](../../methodology/hrv_proxy_via_stress.md)). The *direction* generalises; the exact magnitude/calibration does not.
- **The blunting evidence is severity-mismatched.** Gholami 2012 is a rat endotoxemia model and de Castilho 2017 is ICU sepsis — both more severe than a home-recovered acute COVID infection. They license the *expectation that blunting is possible at the extreme*, not a prediction that it will occur in a mild-to-moderate case. Weighted as a moderate caveat accordingly.
- **n=1 contextualises only.** None of this proves the factor moved in this subject; it fixes the direction the (still-unseen) R23 contrast will be tested against. The no-outcome-peek contract is preserved — this review reads no project data.

---

## 7. Proposed `/reading` block (citable sources)

```
/reading
- Natarajan A, Su H-W, Heneghan C (2020). "Assessment of physiological signs associated with COVID-19 measured using wearable devices." npj Digit Med 3:156. PMID 33299095, DOI 10.1038/s41746-020-00363-7. — The cleanest single statement of the composite acute-infection signature: respiration rate and heart rate elevated, HRV decreased, in 2745 COVID cases; the load-bearing RQ1 citation.
- Mishra T, et al. (Snyder MP) (2020). "Pre-symptomatic detection of COVID-19 from smartwatch data." Nat Biomed Eng 4:1208-1220. PMID 33208926, DOI 10.1038/s41551-020-00640-6. — Resting HR elevated vs personal baseline at/before symptom onset (81% of cases); direct support for RHR-up at R23's daily-vs-personal-baseline resolution (RQ1 + RQ2).
- Radin JM, Wineinger NE, Topol EJ, Steinhubl SR (2020). "Harnessing wearable device data to improve state-level real-time surveillance of influenza-like illness in the USA." Lancet Digit Health 2:e85-e93. PMID 33334565, DOI 10.1016/S2589-7500(19)30222-5. — Elevated RHR + increased sleep track influenza-like illness from nightly aggregates across ~47k Fitbit users; generalises the signature beyond COVID and validates daily-aggregate detectability (RQ2).
- Hirten RP, et al. (2021). "Use of Physiological Data From a Wearable Device to Identify SARS-CoV-2 Infection..." J Med Internet Res 23:e26107. PMID 33529156, DOI 10.2196/26107. — HRV (SDNN circadian pattern) disturbed in the 7 days around COVID diagnosis on an Apple Watch; same wrist-device class, and shows HRV change can be circadian-pattern not flat-mean (RQ1 + RQ2 qualification).
- Mason AE, et al. (Smarr BL) (2022). "Metrics from Wearable Devices as Candidate Predictors of Antibody Response Following Vaccination against COVID-19 (Second TemPredict Study)." Vaccines 10:264. PMID 35214723, DOI 10.3390/vaccines10020264. — Controlled inflammatory challenge (mRNA dose 2) reproduces RHR up, HRV down, deep-sleep/recovery down on Oura; corroborates direction incl. the recovery channel under a known-onset trigger.
- de Castilho FM, et al. (2017). "Heart rate variability as predictor of mortality in sepsis: a prospective cohort study." PLoS One 12:e0180060. PMID 28654692, DOI 10.1371/journal.pone.0180060. — HRV (SDNN/total power) more reduced with greater severity in ICU sepsis; supports RQ3 (severity deepens the high-load move) and bounds the blunting caveat as severity-gated.
- Gholami M, et al. (Mani AR) (2012). "Endotoxemia is associated with partial uncoupling of cardiac pacemaker from cholinergic neural control in rats." Shock 37:219-227. PMID 22249221, DOI 10.1097/SHK.0b013e318240b4be. — Mechanistic basis for both the HRV drop and the RQ3 blunting caveat: severe systemic inflammation uncouples the pacemaker from vagal control, so a derived index can decouple at the extreme.
```

---

*Source database: PubMed/PMC. Findings paraphrased; consult primary papers (DOIs above) for methods and data. Research synthesis, not medical advice. Anchors [`../../methodology/peri_event_known_event_check.md`](../../methodology/peri_event_known_event_check.md) §6 + decision (e). Companion to [`expected_shapes_autonomic_signals_review.md`](expected_shapes_autonomic_signals_review.md) (chronic curve shape) and [`wearable_validity_lc_mecfs_review.md`](wearable_validity_lc_mecfs_review.md) (R24 in-population device validity) — this review is the ACUTE infection signature, a distinct topic from both. No project n=1 data was read in producing this anchor (R23 no-outcome-peek contract).*
