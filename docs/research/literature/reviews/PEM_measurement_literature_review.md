# Measuring Post-Exertional Malaise: Instruments, Provocation Protocols, and the "Ground-Truth" Problem — A State-of-the-Art Literature Review

*Primary evidence retrieved from PubMed (DOI links included); definitional/guideline context supplemented where noted. Focus: how PEM is defined and operationalised across ME/CFS and Long COVID (with cross-condition comparisons), spanning patient-reported instruments, exercise-provocation/objective protocols, and emerging ecological/digital capture. This review is deliberately methodological — it asks how well we can label "a PEM episode happened," because every downstream detection, prediction, pacing, or wearable study depends on that label.*

---

## 1. The headline: why this is the load-bearing review

Across the earlier strands (wearables, the HRV/autonomic signature, pacing), one problem kept resurfacing: there is **no biomarker and no objective gold standard for PEM**, so almost everything rests on how PEM is defined and measured. The state of play, in three lines:

- **Patient-reported instruments are the de facto standard, and the best of them are psychometrically sound** — chiefly the DePaul Symptom Questionnaire PEM module (DSQ-PEM) — but they capture *recalled, characteristic* PEM, not a specific episode in time.
- **Objective provocation (the two-day CPET) gives a reproducible physiological signature in ME/CFS**, but it is burdensome, potentially harmful, a 24-hour-apart snapshot, and does not generalise to Long COVID.
- **Real-time, ecological, wearable-based capture of an actual PEM episode is essentially absent** — the single biggest measurement gap, and the one that most directly blocks the wearable-detection programme.

The unifying theme is a **mismatch of timescales**: PEM is a delayed, fluctuating, multi-day phenomenon, while our instruments are either retrospective questionnaires or single-timepoint lab tests. Closing that mismatch is the core methodological opportunity.

---

## 2. The definitional substrate — why PEM is hard to measure

Measurement inherits the instability of the definition. PEM is the delayed, disproportionate exacerbation of symptoms after physical, cognitive, emotional or orthostatic exertion, with prolonged (often >24 h) recovery — but the exact operational criteria differ across case definitions (Fukuda, Canadian Consensus Criteria, International Consensus Criteria, the IOM/NAM 2015 "SEID" criteria, and NICE 2021), and this directly changes who is counted.

The clearest demonstration: in a Dutch post-COVID cohort scored with the DSQ-2, **52.7% met the Fukuda criteria for ME/CFS while fewer met stricter definitions** — the same patients, different labels depending on the instrument's operational thresholds ([Cornelissen et al., 2024, *J Transl Med*; DOI](https://doi.org/10.1186/s12967-024-04979-1)). Self-report alone is unreliable as a substitute for criterion-based assessment: among Long COVID patients, only ~71% who said they had ME/CFS actually met criteria, while ~40% who said they did *not* nevertheless met them — over- and under-identification in both directions ([Jason & Dorri, 2022, *Neurol Int*; DOI](https://doi.org/10.3390/neurolint15010001)). And PEM has only recently become *mandatory* for diagnosis (it is central to the IOM 2015 and NICE 2021 frameworks), which means older cohorts were assembled without requiring the very feature this review is about — a confound when reading the historical literature.

**Implication for your work:** any PEM label must state which case definition and which instrument/threshold produced it, or it is not comparable across studies.

---

## 3. Patient-reported instruments — the de facto standard

This is the most developed measurement strand, dominated by the DePaul instruments.

**The DePaul Symptom Questionnaire (DSQ)** was developed and factor-validated by Jason and colleagues; exploratory and confirmatory factor analyses yield a stable structure in which **post-exertional malaise emerges as its own distinct factor** alongside neurocognitive and neuroendocrine/autonomic/immune dysfunction ([Brown & Jason, 2014, *Fatigue*; DOI](https://doi.org/10.1080/21641846.2014.928014)). Crucially, the DSQ measures PEM on **two axes — frequency and severity** — rather than mere presence, which is what allows threshold-based scoring.

**Psychometric performance is good where general fatigue scales fail.** Comparing the DSQ against the Multidimensional Fatigue Inventory-20 and RAND SF-36 in ME/CFS, the generic fatigue scales showed problematic ceiling effects and questionable reliability, whereas the DSQ had excellent internal reliability and minimal ceiling, and the **PEM subscale discriminated patients from controls and predicted ceiling effects on the other measures**; a PEM-subscale score around 20 optimally separated patients from controls ([Murdock et al., 2016, *Qual Life Res*; DOI](https://doi.org/10.1007/s11136-016-1406-3)).

**Standardised scoring thresholds exist.** A commonly applied DSQ-PEM rule requires symptoms that are moderate-to-very-severe **at least half the time**, *plus* symptom worsening after minimal effort, *plus* a recovery period exceeding 24 hours — a concrete, reproducible operationalisation ([Twomey et al., 2020, *J Pain Symptom Manage*; DOI](https://doi.org/10.1016/j.jpainsymman.2020.02.012)).

**The instrument family has been extended and translated**, supporting multi-site and international use: a validated short form (DSQ-SF) in German with good reliability and a one-factor structure ([Froehlich et al., 2021, *Medicina*; DOI](https://doi.org/10.3390/medicina57070646)); a large dual-sample German validation of the DSQ-PEM (general population n=2,263; post-COVID n=1,448) showing excellent internal consistency and known-group validity ([Kuczyk et al., 2025, *Front Psychiatry*; DOI](https://doi.org/10.3389/fpsyt.2025.1647040)); and the DSQ-2 used for case-definition scoring and symptom clustering ([Cornelissen et al., 2024; DOI](https://doi.org/10.1186/s12967-024-04979-1)).

**Alternative structured instruments** are emerging — e.g. the **Munich Berlin Symptom Questionnaire (MBSQ)** with scoring sheets that rapidly evaluate several ME/CFS case definitions at once, validated in paediatric and adult post-COVID patients ([Peo et al., 2023, *Eur J Pediatr*; DOI](https://doi.org/10.1007/s00431-023-05351-z)) — and condition-specific PEM tools such as the **Leeds PESE Questionnaire** used to track episodes in Long COVID pacing programmes ([Godfrey et al., 2024, *J Clin Med*; DOI](https://doi.org/10.3390/jcm14010097)). A Long COVID PROMs review concluded that, for the PEM domain specifically, the **DSQ-PEM is the instrument of choice**, to be paired with separate validated tools for fatigue, sleep, cognition and mood ([Ejalonibu et al., 2024, *J Patient Rep Outcomes*; DOI](https://doi.org/10.1186/s41687-024-00773-1)).

**The limitation that matters for your programme:** these instruments measure *trait-like, recalled* PEM over weeks or months. They are excellent for cohort definition and case ascertainment, but they do **not** timestamp an individual crash — so they cannot, on their own, supply the per-episode "ground-truth" label a wearable-detection study needs.

---

## 4. Provocation and objective measurement

If questionnaires capture recalled PEM, provocation protocols attempt to *elicit and physiologically measure* it.

**The two-day CPET** is the most objective approach: a maximal cardiopulmonary exercise test repeated 24 hours later, exploiting the fact that ME/CFS patients cannot reproduce day-1 performance on day 2 (declines in workload, oxygen uptake, heart rate and ventilatory/anaerobic-threshold measures), interpreted as a physiological signature of the provoked post-exertional state ([Keller et al., 2024, *J Transl Med*; DOI](https://doi.org/10.1186/s12967-024-05410-5); severity grading in [van Campen et al., 2020, *Healthcare*; DOI](https://doi.org/10.3390/healthcare8030192)). Its measurement strengths are objectivity and reproducibility; its weaknesses are severe for this use case — it is **burdensome, can itself trigger a prolonged crash (an ethical and dropout problem), provides only a 24-hour-apart snapshot, and does not reproduce in Long COVID**, where a two-day CPET found no day-2 difference despite most patients reporting PEM ([Gattoni et al., 2024, *Respir Physiol Neurobiol*; DOI](https://doi.org/10.1016/j.resp.2024.104362)).

**Submaximal provocation** is a gentler alternative used in the Gulf War Illness literature (e.g. cycling at a fixed % of heart-rate reserve), which reliably elicits delayed symptom exacerbation in a subset — confirming PEM can be provoked but also that not everyone shows it ([Lindheimer et al., 2019, *Int J Psychophysiol*; DOI](https://doi.org/10.1016/j.ijpsychro.2019.11.008)).

**A measurement insight that should shape any protocol:** *when* you measure decides *what* you find. A meta-analysis of pain-related PEM showed effect sizes were substantially larger when symptoms were measured **8–72 hours after exercise (d ≈ 0.71) than at 0–2 hours (d ≈ 0.32)** — capturing the delayed peak is essential, and measuring too early underestimates PEM ([Barhorst et al., 2022, *Pain Med*; DOI](https://doi.org/10.1093/pm/pnab308)). This is a direct argument for multi-day post-exertion sampling rather than immediate post-test assessment.

---

## 5. Real-time, ecological and digital capture — the gap

This is where the literature thins to near-nothing, and the absence is itself the finding.

Targeted PubMed searching for ecological momentary assessment (EMA), digital symptom diaries, or wearable/accelerometer-based capture of PEM returned essentially **no validated studies that timestamp a spontaneous PEM episode in free-living conditions**. The closest existing practice is the **symptom-and-activity diary** embedded in pacing programmes (e.g. the Leeds PESE Questionnaire administered weekly; daily activity logs), which records episode counts but at coarse temporal resolution and by recall ([Parker et al., 2023, *J Med Virol*; DOI](https://doi.org/10.1002/jmv.28373); [Godfrey et al., 2024; DOI](https://doi.org/10.3390/jcm14010097)).

There is also early evidence that PEM has a **detectable temporal structure** that an ecological method could exploit: a retrospective analysis found that new or atypical "warning-signal" symptoms (most often mood changes) preceded baseline symptom exacerbation in ~14% of ME/CFS patients — implying a measurable prodrome that real-time monitoring might catch ([Ghali et al., 2021, *J Clin Med*; DOI](https://doi.org/10.3390/jcm10112517)). Combined with the delayed-peak timing from Section 4, this points to what an ecological PEM measure would need: **continuous or high-frequency sampling across multiple days around an exertion event, anchored to a patient-confirmed symptom report.** No retrieved study has yet delivered this — which is precisely the methodological niche connecting this review to the wearable-HRV gap identified earlier.

---

## 6. PEM beyond ME/CFS — measurement across conditions

Applying the same instruments across conditions reveals both the portability of the tools and the definition-dependence of the results.

In **Long COVID**, the DSQ-PEM is widely deployed: 58.7% of one Long COVID cohort met ME/CFS PEM thresholds ([Twomey et al., 2022, *Phys Ther*; DOI](https://doi.org/10.1093/ptj/pzac005)), and DSQ-based scoring underlies the prevalence and clustering work above. In **chronic cancer-related fatigue**, the DSQ-PEM plus an open-ended post-exercise questionnaire identified PEM in up to a third of a small sample — extending the construct (and its measurement) beyond the post-infectious family ([Twomey et al., 2020, *J Pain Symptom Manage*; DOI](https://doi.org/10.1016/j.jpainsymman.2020.02.012)). In **fibromyalgia and ME/CFS**, standardized-exercise provocation confirmed a measurable pain component of PEM ([Barhorst et al., 2022; DOI](https://doi.org/10.1093/pm/pnab308)). The consistent lesson is that **the same instrument yields different PEM rates depending on the case definition and threshold applied**, so cross-condition comparisons require harmonised criteria — and **Q fever fatigue syndrome remains unmeasured for PEM with any validated instrument**, a continuing blank spot.

---

## 7. Evidence summary table

| Study | Measurement approach | Population | Contribution to measuring PEM |
|---|---|---|---|
| Brown & Jason 2014 | DSQ (factor analysis) | ME/CFS | PEM emerges as a distinct, validated factor; frequency × severity scoring |
| Murdock 2016 | DSQ vs MFI-20/SF-36 | ME/CFS + controls | DSQ-PEM discriminates patients; avoids ceiling effects; cutoff ≈20 |
| Twomey 2020 | DSQ-PEM + maximal exercise | Cancer-related fatigue | Explicit scoring rule (severity + minimal-effort trigger + >24 h recovery) |
| Froehlich 2021 | DSQ-SF (German) | ME/CFS | Validated short form; good reliability, one-factor |
| Kuczyk 2025 | DSQ-PEM (German) | Gen pop n=2,263; PCC n=1,448 | Large-scale psychometric validation; known-group validity |
| Cornelissen 2024 | DSQ-2 + clustering | Post-COVID | Case-definition dependence (52.7% Fukuda vs fewer stricter) |
| Jason & Dorri 2022 | Validated ME/CFS + PEM questionnaires | Long COVID | Self-report unreliable vs criteria (over- and under-identification) |
| Peo 2023 | Munich Berlin Symptom Questionnaire | Paediatric/adult PCC | Structured multi-criteria diagnostic instrument |
| Ejalonibu 2024 | PROMs review | Long COVID | Recommends DSQ-PEM as PEM instrument of choice |
| Keller 2024 | 2-day CPET | ME/CFS | Objective, reproducible provoked PEM signature |
| Gattoni 2024 | 2-day CPET | Long COVID | Negative — objective signature does not generalise |
| Lindheimer 2019 | Submaximal provocation | Gulf War Illness | Gentler elicitation; PEM in a subset |
| Barhorst 2022 | Standardized exercise + meta-analysis | ME/CFS + FM | Measurement *timing* matters (8–72 h > 0–2 h) |
| Ghali 2021 | Retrospective records | ME/CFS | PEM has a measurable prodrome ("warning signals") |
| Godfrey 2024 / Parker 2023 | Leeds PESE Questionnaire + diaries | Long COVID | Episode-count tracking in practice (coarse, recall-based) |
| Twomey 2022 | DSQ-PEM | Long COVID | 58.7% meet PEM thresholds; cross-condition portability |

---

## 8. Critical appraisal — what a good PEM measure would need

- **Timescale match.** The dominant tools are retrospective (questionnaires) or single-snapshot (CPET); PEM is delayed and multi-day. The Barhorst timing data and the Ghali prodrome data both argue for **high-frequency sampling across several days around exertion.**
- **Episode-level labelling.** Trait-level instruments establish that a person *has* PEM; they don't mark *when an episode occurs.* A defensible per-episode label likely needs **patient-confirmed symptom reports (EMA) as the anchor**, with physiological/behavioural streams layered on.
- **Definition transparency.** Every PEM rate is contingent on case definition and threshold; studies must report both, and ideally score multiple definitions (as MBSQ and DSQ-2 allow).
- **Provocation has an ethics ceiling.** Maximal two-day CPET can itself harm patients and drive dropout, and fails in Long COVID — limiting its use as a routine ground-truth generator. Naturalistic capture is the more humane and more generalisable target.
- **Construct portability with caution.** The DSQ-PEM travels across Long COVID, cancer-related fatigue and fibromyalgia, but identical instruments give different rates by definition — and QFS remains entirely unmeasured.
- **Self-report ≠ criteria.** Diagnosis-by-self-label is unreliable; instruments with explicit scoring rules are required.

---

## 9. Bottom line

Measuring PEM is the weakest link on which the entire post-infectious wearables/pacing research programme depends, and the literature splits cleanly: **patient-reported instruments are mature and psychometrically sound** (the DSQ-PEM is the field's reference tool, with validated short forms, translations and explicit scoring thresholds), and **objective provocation via the two-day CPET is reproducible in ME/CFS** but burdensome, potentially harmful, snapshot-only, and non-generalising to Long COVID. The decisive gap is the **absence of any validated real-time, ecological, or wearable-based method that timestamps a spontaneous PEM episode** — even though both the delayed-peak timing data and the existence of a measurable prodrome suggest such a method is feasible. The clear next step, and the one that unlocks the detection/prediction and pacing-trial questions raised in the earlier reviews, is an **EMA-anchored, multi-day, high-frequency PEM-capture protocol** that pairs patient-confirmed symptom reports with continuous physiological and activity data — supplying, for the first time, a per-episode ground-truth label.

---

*Primary source database: PubMed; findings synthesised and paraphrased (consult originals via the DOI links for full methods and data). Definitional/guideline context (IOM/NAM 2015, NICE NG206 2021) noted for completeness. This is a research synthesis, not medical advice.*
