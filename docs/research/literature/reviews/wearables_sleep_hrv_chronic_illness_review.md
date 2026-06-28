# Consumer Wrist-Worn Wearables for Sleep and Heart-Rate-Variability Monitoring in Chronic-Illness Self-Management: A State-of-the-Art Literature Review

*Evidence retrieved from PubMed. All cited articles include DOI links. Search conducted June 2026; literature dominated by 2020–2025 publications.*

---

## 1. Scope and method

This review synthesises peer-reviewed evidence on commercial, wrist-worn wearables (Garmin, Fitbit, Apple Watch, Polar, Oura, WHOOP and similar) used to track **sleep** and **heart rate variability (HRV)** — alongside related physiological signals (resting/exercise heart rate, SpO₂, step count) — in **patients living with chronic illness**. Sources were identified through structured PubMed searches combining device terms (Garmin, Fitbit, "consumer wearable," smartwatch), signal terms (sleep, heart rate variability), and population terms (patients, chronic disease, self-management, plus specific conditions). Thirteen representative, on-topic articles were selected spanning device-validation studies, disease-specific applications, and clinical-readiness reviews.

**An upfront caveat, stated plainly:** the precise four-way intersection the brief asks for — *Garmin specifically × HRV × chronic-illness self-management × patient outcomes* — is sparsely populated. The actual literature has three honest characteristics worth keeping in view throughout:

1. **Fitbit dominates**, not Garmin. Garmin typically appears as one device among several in validation or feasibility work, rarely as the standalone intervention.
2. **Validation and feasibility outnumber outcomes.** Most studies ask "is the signal accurate?" or "will patients wear it?" — far fewer ask "did using it change disease management or clinical outcomes?"
3. **HRV is the least-validated of the signals.** Sleep *staging* and exercise HRV remain the weakest measurements in patient populations, a point that recurs across the evidence.

---

## 2. How accurate are these devices? (Validation evidence)

Accuracy is the foundation everything else rests on, and the picture is mixed by signal type.

The most directly relevant validation study assessed six devices — including the **Garmin Forerunner 245** — against polysomnography (PSG) and ECG in 53 healthy adults. According to PubMed, two-state sleep detection (sleep vs wake) was reasonably good across all devices (Garmin: 89% agreement, κ = 0.35), but multi-state sleep-*stage* classification was poor for every device, with Garmin among the weakest (50% agreement, κ = 0.25). The authors concluded the devices are valid for timing and duration of sleep but not yet for specific sleep stages ([Miller et al., 2022, *Sensors*; DOI](https://doi.org/10.3390/s22166317)).

This finding is corroborated at the meta-analytic level. A meta-analysis of 24 studies (798 participants) covering Fitbit, Garmin, WHOOP, Apple Watch and others found statistically significant deviations from PSG across total sleep time, sleep efficiency, sleep latency and wake-after-sleep-onset — concluding that wrist-worn trackers are useful for general pattern tracking but not reliable substitutes for PSG on key parameters ([Lee et al., 2025, *J Clin Sleep Med*; DOI](https://doi.org/10.5664/jcsm.11460)).

For **heart rate specifically**, accuracy is considerably better. In coronary rehabilitation patients exercising on a cycle ergometer, the **Garmin Forerunner 35** showed excellent correlation with ECG and was one of only three devices (with Apple Watch and Mio) the authors felt able to recommend for cardiac patients ([Heyken et al., 2021, *Georgian Med News*; DOI not indexed — PMID 34365430](https://pubmed.ncbi.nlm.nih.gov/34365430/)).

**SpO₂ is a cautionary tale.** In COPD patients during pulmonary rehabilitation, both the Apple Watch Series 7 and **Garmin Vivosmart 4** misestimated oxygen saturation — overestimating when true SpO₂ was below 95% and underestimating above it — leading the authors to advise *against* using these devices to monitor oxygenation during rehab ([Støve et al., 2023, *Respir Care*; DOI](https://doi.org/10.4187/respcare.10760)). This matters because hypoxemia detection is exactly where a COPD patient might most want to trust a device.

**The recurring pattern:** simple cardiovascular signals (resting/exercise HR, step count) validate well; the clinically richer signals (sleep staging, SpO₂, and — by extension and by under-study — HRV) do not yet meet a standard that would support unsupervised clinical decisions.

---

## 3. Application in chronic-illness populations

Here the evidence moves from "does it work on the bench" to "does it work in patients," organised by condition.

### Neurodegenerative disease
A device-validation-in-patients study deployed the Fitbit Charge 4 against PSG in patients with **Huntington's disease**, then continued home monitoring for seven nights. Sleep-stage and heart-rate agreement were generally good (intraclass correlations 0.79–0.96; mean HR error ~1.2 bpm), though wake-after-sleep-onset and awakenings were poorly captured — a known weakness amplified by HD's involuntary movements. The authors saw genuine potential for long-term home sleep monitoring as part of symptom management ([Doheny et al., 2024, *J Clin Sleep Med*; DOI](https://doi.org/10.5664/jcsm.11098)).

### Recurrent major depression
One of the strongest *outcome-oriented* studies followed people with recurrent major depressive disorder wearing Fitbit devices for a median of 541 days. According to PubMed, greater night-to-night variability in sleep duration and timing, more fragmentation and lower efficiency all predicted worse depression outcomes; modelling suggested that improving sleep *consistency* could reduce population relapse risk by up to ~22%. This is a rare example of wearable-derived sleep features being linked to a hard clinical endpoint (relapse) rather than just described ([Matcham et al., 2024, *J Affect Disord*; DOI](https://doi.org/10.1016/j.jad.2024.07.136)).

### Long COVID / dysautonomia
The HEARTLOC feasibility protocol is notable as one of the few studies using **HRV as an active intervention target** rather than a passive metric. It pairs a Polar chest-strap and wrist-worn Fitbit to deliver HRV biofeedback (slow diaphragmatic breathing) to Long COVID patients with palpitations/dizziness suggestive of autonomic dysregulation ([Corrado et al., 2022, *BMJ Open* protocol; DOI](https://doi.org/10.1136/bmjopen-2022-066044)). As a protocol, it signals direction of travel more than proven benefit.

### Heart failure
A scoping review of smartwatches in heart failure (13 studies, 1,171 patients) found HR and step counts moderately accurate — including **Garmin Vivofit** (concordance 0.89–0.92) — while calorimetry was unreliable. More interestingly, activity data tracked NYHA functional class, which is notoriously subjective, suggesting wearables could add objectivity to HF severity assessment and outpatient management. Adherence was high in research settings (~91%) but device ownership in the HF population was low (10–50%) ([Fabien et al., 2025, *ESC Heart Fail*; DOI](https://doi.org/10.1002/ehf2.15226)).

### Oncology
A large systematic review (199 studies, 18,513 patients) mapped wearables across prognostication, treatment monitoring and rehabilitation in cancer, with Garmin the third-most-common brand (7% of studies) after ActiGraph and Fitbit. Adherence exceeded 80% in roughly three-quarters of studies that reported it ([Chow et al., 2024, *Oncologist*; DOI](https://doi.org/10.1093/oncolo/oyad305)). A focused lung-cancer review (12 studies, including Garmin) found commercial trackers improved activity levels, quality of life and physical function versus usual care, while cautioning that heterogeneous implementation limits firm conclusions ([Bahadori & Hosseini, 2024, *Lung Cancer*; DOI](https://doi.org/10.1016/j.lungcan.2024.108026)).

The CARDIOCARE protocol is one of the clearest **Garmin-centred** chronic-disease studies: it uses the **Garmin Venu SQ** plus a Polar H10 sensor within an eHealth platform to monitor older breast-cancer patients and build a predictive model for chemotherapy-induced cardiotoxicity (target n = 750) ([Sacco et al., 2025, *JMIR Res Protoc*; DOI](https://doi.org/10.2196/63455)).

---

## 4. Clinical readiness: what the field's own reviewers say

Two synthesis pieces capture the consensus position. A review of consumer wearable sleep trackers concluded the technology has matured from crude sleep/wake detection toward more granular health assessment, but explicitly called on professional societies to develop guidelines for practical clinical use before these tools are folded into care plans ([Chiang & Khosla, 2023, *Sleep Med Clin*; DOI](https://doi.org/10.1016/j.jsmc.2023.05.005)). A cardiology commentary framed smartwatches as a fast-growing but double-edged development — significant potential to reshape the cardiologist–patient relationship, but real concerns about data trustworthiness, workflow integration, sustained patient engagement, privacy and socioeconomic disparities ([Lima et al., 2022, *Am J Cardiol*; DOI](https://doi.org/10.1016/j.amjcard.2022.06.020)).

---

## 5. Synthesis: evidence summary table

| Study | Device(s) | Population | Signal(s) | Design | Key finding |
|---|---|---|---|---|---|
| Miller 2022 | Garmin Forerunner 245, Apple, Polar, Oura, WHOOP, Somfit | Healthy adults (n=53) | Sleep, HR, HRV | Validation vs PSG/ECG | Good for sleep timing/duration; poor for sleep staging across all devices |
| Lee 2025 | Fitbit, Garmin, WHOOP, Apple, others | Mixed (24 studies, n=798) | Sleep | Meta-analysis vs PSG | Significant deviations on TST, efficiency, latency, WASO; not PSG-equivalent |
| Heyken 2021 | Garmin Forerunner 35 + 6 others | Coronary rehab patients (n=35) | HR | Validation vs ECG | Garmin, Apple, Mio recommended; others less accurate |
| Støve 2023 | Garmin Vivosmart 4, Apple Watch 7 | COPD (n=36) | SpO₂ | Validation vs oximeter | Both misestimated SpO₂; advised against rehab use |
| Doheny 2024 | Fitbit Charge 4 | Huntington's disease (n=10) | Sleep, HR | Validation + home monitoring | Good sleep/HR agreement; poor on WASO/awakenings; home monitoring feasible |
| Matcham 2024 | Fitbit | Recurrent MDD (n=393) | Sleep | Longitudinal observational (~541 days) | Sleep irregularity predicts relapse; consistency could cut risk ~22% |
| Corrado 2022 | Fitbit + Polar strap | Long COVID (n=30) | HRV | Feasibility protocol | HRV biofeedback as intervention target for dysautonomia |
| Fabien 2025 | Garmin Vivofit, Fitbit, others | Heart failure (13 studies, n=1,171) | HR, activity | Scoping review | HR/steps moderately accurate; activity tracks NYHA class; low device ownership |
| Chow 2024 | ActiGraph, Fitbit, Garmin, others | Oncology (199 studies, n=18,513) | Activity, HR | Systematic review | Broad utility; adherence >80% in most studies |
| Bahadori 2024 | Fitbit, Garmin, Apple, Samsung, Polar | Lung cancer (12 studies) | Activity | Systematic review | Improved activity, QoL, function vs usual care |
| Sacco 2025 | Garmin Venu SQ + Polar H10 | Older breast-cancer patients (target n=750) | HR, activity | Prospective protocol | Garmin-based cardiotoxicity prediction model |
| Chiang 2023 | Consumer sleep trackers (incl. HRV-capable) | General/clinical | Sleep, HRV | Narrative review | Maturing; needs professional-society guidelines |
| Lima 2022 | Smartwatches (Apple, Fitbit, Samsung) | Cardiovascular | HR, rhythm, BP, sleep | Review/commentary | Promise tempered by trust, workflow, equity, privacy concerns |

---

## 6. Critical appraisal and gaps

**What the evidence supports well.** Wrist-worn wearables reliably capture resting and exercise heart rate, step count and gross sleep duration in patient populations. Adherence is generally high in research settings (often >80–90%). Activity and sleep-regularity metrics show genuine, sometimes outcome-linked, signal — the depression-relapse and heart-failure NYHA findings are the clearest examples of clinical value.

**What it does not yet support.** Three weaknesses are consistent across the corpus:

- **Sleep staging and HRV remain under-validated**, especially in patients whose conditions perturb movement, autonomic tone or the PPG signal itself (e.g., Huntington's, arrhythmia, COPD desaturation). HRV in particular is frequently mentioned as a *capability* but rarely rigorously validated against ECG-derived HRV in a chronic-disease cohort.
- **The self-management loop is rarely closed.** Most studies stop at measurement or feasibility. Few demonstrate that giving patients (or clinicians) the data changes behaviour, treatment decisions or hard outcomes. The brief's emphasis on *managing* chronic illness is exactly where the evidence is thinnest.
- **Garmin-specific evidence is limited.** Despite the brief's framing, Garmin is rarely the primary, standalone tool; Fitbit is the de facto research workhorse. CARDIOCARE is a welcome exception but is still a protocol.

**Cross-cutting concerns** repeatedly flagged: data trustworthiness and false alerts, integration into clinical workflow, sustained engagement (novelty decay), low device ownership in older/sicker populations, privacy, and socioeconomic access disparities.

---

## 7. Recommendations for future work

1. **Condition-specific HRV validation** against ECG in the actual target population, not healthy adults — the generalisation from healthy cohorts is currently doing too much work.
2. **Closed-loop self-management trials**: randomised designs where wearable data feeds back into patient behaviour or clinician decisions, measured against clinical endpoints (relapse, exacerbation, hospitalisation, QoL).
3. **Head-to-head Garmin evaluations** if Garmin is the platform of interest, since most transferable evidence is Fitbit-derived and device firmware/algorithms are not interchangeable.
4. **Equity and adherence reporting** as standard, given the consistent ownership/access gaps in older and chronically ill populations.

---

## 8. Bottom line

Consumer wrist-worn wearables are credible for **heart rate, activity and gross sleep tracking** in chronic-illness patients, and early signals link wearable-derived sleep *regularity* to meaningful outcomes (depression relapse, heart-failure functional status). They are **not yet dependable for sleep staging, SpO₂ in COPD, or — most relevant to this brief — validated HRV in disease populations**, and the field has largely not demonstrated that the data actually improves self-management. Garmin specifically is under-represented relative to Fitbit. The technology is maturing faster than the evidence and the guidelines, which is the central tension reviewers themselves keep naming.

---

*Source database: PubMed. This review synthesises and paraphrases findings from the cited articles; consult the original papers (DOI links above) for full methods and data. Not legal or medical advice.*
