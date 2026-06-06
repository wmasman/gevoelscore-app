# Pacing, pacing indicators, and crash mitigation — a research note

*Builds on two earlier documents: the n-of-1 findings (`gevoelsscore-dashboard-findings.md`) and the literature scan (`pais-pem-literature-review.md`). This note covers what is known about (1) pacing strategies, (2) the indicators people use to pace, (3) naproxen / anti-inflammatories for blunting crashes, and (4) other ways to reduce crash depth — and closes with what all of this could mean for the app.*

> **Not medical advice.** Much of §3 and §4 concerns medication and self-management with real risks. Claude is not a doctor. Drug choices — naproxen especially — should be made with a physician. Throughout, "evidence" ranges from formal trials to expert opinion to patient anecdote; each is labelled, because they are not equal.

---

## 0. Where this starts from

Two things from the earlier work frame everything below. First, our own data already shows a person who **paces well**: the cost of activity lands as a ~1-point headache-led sag 48–72h later, not a crash, and there were zero windows of three consecutive activity days. Second, the literature reframed the deep ≤2 "floor-crashes" not as a clean second mechanism but as a **spectrum of immune/sickness-response flares** — some external infection, some endogenous (cytokine-driven sickness behaviour, mast-cell, latent-virus reactivation, exertion- or stress-triggered). That second point matters here, because it gives an anti-inflammatory like naproxen a coherent mechanistic target (§3).

So the practical question this note serves is narrow and useful: *given that pacing is already happening, what reduces the depth and length of the bad days that still get through?*

---

## 1. Pacing strategies — what is known

**Pacing is the consensus, evidence-based management approach** for ME/CFS and Long COVID, and since the 2021 NICE guideline overhaul it is essentially *the* recommended strategy. NICE now explicitly says **do not offer graded exercise therapy (GET)**, and that people should **stay within their energy limit and not push through symptoms**. CBT is positioned only as an adjunct for coping, not a cure. This was a reversal of the 2007 guidance and reflects the recognition that PEM makes "push through it" actively harmful.

The organising idea is the **energy envelope**: a finite daily budget of physical, cognitive, *and* emotional energy. Pacing means deliberately operating inside it. The distinctions that matter:

- **Quota / time-contingent vs. symptom-contingent.** The old GET model is quota-contingent ("do X today regardless of how you feel," with fixed weekly increases). Pacing flips this to **symptom-contingent**: activity is guided by symptoms and capacity that day, and you stop *before* strain, not after. (A purely time-contingent variant — fixed activity/rest intervals regardless of symptoms — is sometimes used to impose structure, but the symptom-led version dominates in PEM.)
- **Finding a baseline.** Pacing starts by establishing a sustainable baseline of activity that does *not* trigger PEM — often by cutting current activity substantially — then holding it. The baseline can drift up or down over time; it is discovered, not prescribed.
- **Breaking the boom–bust (push–crash) cycle.** The core failure mode is doing a lot on a good day and crashing for several after. Pacing trades peak output for consistency.
- **Pre-emptive and "aggressive"/"radical" rest.** Rest *before* feeling tired, and rest *in advance* of a known demand (a trip, an event). "Aggressive rest" in its strict sense is genuine sensory rest — flat, dark, quiet, no screens — not just sitting down.
- **All exertion counts, not just physical.** Cognitive load (concentration, reading, fast conversation), emotional stress, and orthostatic load (being upright) all draw on the same envelope and can each trigger PEM. The brain uses ~20% of the body's energy; cognitive overexertion can crash someone as hard as a walk. This is the single most under-appreciated point and the one a step-counter misses entirely.
- **The "4 P's" (from occupational therapy):** *Prioritise* (spend energy on what matters), *Plan* (sequence demanding tasks with recovery around them), *Pace* (break tasks up, rest between), *Position* (do tasks seated/recumbent to cut orthostatic cost). Practical tactics: pre-make meals, ask for help, schedule low-energy days after unavoidable big ones.

**Evidence quality, honestly stated.** Pacing is endorsed by guidelines and strongly supported by patient-reported outcomes and clinical consensus, and structured-pacing and heart-rate-monitor studies show it is feasible, acceptable, and associated with fewer/less severe crashes and better function. But it is a management strategy, not a cure, the trial base is modest, and the right envelope is highly individual. Its goal is explicitly to *minimise* PEM, not eliminate it.

---

## 2. The indicators people use to pace

Pacing only works if you can *see* the envelope. Two families of indicator are used, and the strongest practice combines them.

### Physiological (objective)

- **Heart-rate ceiling.** The most established tool. The idea is to keep HR below an individual threshold (the ventilatory/anaerobic threshold, VT1) above which the body shifts toward anaerobic metabolism and PEM risk rises. Ways people set it:
  - **Gold standard:** VT1 measured directly on a CPET.
  - **Age formula:** `(220 − age) × 0.6` (or × 0.5 if more severely affected), since the threshold in ME/CFS sits abnormally low.
  - **Workwell's accessible rule:** **7-day average resting HR + 15 bpm.** Conservative and needs no lab.
  - Caveat: **>85% of people with ME/CFS have *chronotropic incompetence*** — a blunted HR response — so HR can under-report exertion; this is partly why HRV and symptoms are needed alongside it.
- **Heart-rate variability (HRV) / "readiness."** Low HRV reflects the sympathetic-dominant, low-vagal-tone state typical of these conditions. Morning HRV is used as a daily "battery meter," and — per the 2025 wearable study in the literature review — HRV stays suppressed for ~24h after crossing VT1, which is the basis for treating VT1 as a *PEM threshold* and for HR-alarm pacing.
- **Step count / activity load** as a rough proxy, useful mainly for spotting boom-bust patterns rather than real-time control.

### Wearables and apps people actually use

- **Visible** (app + optional Polar-based armband) is purpose-built for energy-limiting illness rather than fitness: continuous HR, a daily **"stability/pace" score**, and a **"PacePoints"** budget the user spends across the day. It is the closest existing product to this project's intent.
- **Garmin "Body Battery"**, **Oura** (readiness/HRV/sleep), **Whoop** (strain/recovery), **Apple Watch**, and **Polar** chest straps (most accurate HR for alarms) are all repurposed by patients. Garmin is specifically relevant because it's already in the project's v2 plan.
- A 2025 survey of wearable use in complex chronic illness reports users find them genuinely helpful for pacing, with the usual caveats about accuracy and the mental load of constant monitoring.

### Subjective (what the person feels)

- **Symptom and energy self-ratings** (our gevoelsscore is exactly this), fatigue scales, and **"spoon theory"** as a shared budgeting language.
- **Activity/symptom diaries** to connect what was done to what followed — the only way to surface a *delayed* cost.
- Tracking **"payback"** (the next-day or 2–3-day cost) explicitly, since the delay defeats intuition.

**The key point for us:** objective and subjective indicators fail in opposite directions. HR/HRV catches physical and orthostatic load in real time but is blind to cognitive/emotional exertion and to symptom *content*; the self-rating catches meaning and the non-physical triggers but only registers the cost *after* it lands. Combining them — the subjective score as the labelled ground truth, the wearable as the leading edge — is the design opportunity (see §5).

---

## 3. Naproxen and anti-inflammatories for crash mitigation

This is the part with the widest gap between *rationale* and *proof*, so it's worth separating the two.

**The mechanistic rationale is real and fits our §4 finding.** If the deep crashes are substantially endogenous sickness-behaviour flares — pro-inflammatory cytokines (IL-1β, TNF-α, IL-6) and neuroinflammation driving the fever-feeling, sore throat, malaise — then a drug that damps inflammation has a coherent target. Neuroinflammation researcher Jarred Younger has argued explicitly that "people with PEM should be exploring anti-inflammatory approaches in different ways, especially those agents demonstrated to cross the blood–brain barrier," and that anti-inflammatories for PEM deserve formal clinical trials. The post-exertion muscle-injury and metabolite findings point the same way.

**The formal evidence is thin and unimpressive.** There are **no proven pharmacological treatments that prevent or reduce PEM**, and naproxen/NSAIDs have not been validated for it in trials. Clinically, the candid summary from the Solve ME/CFS Initiative is that for ME/CFS pain "the problem with NSAIDs is that they usually don't work" well. So naproxen sits on rationale and anecdote, not evidence.

**What the anecdotal / expert-practice layer reports** (patient and clinician reports, *not* trials — treat as hypotheses):

- A useful framing is **"PEM shielder" vs "PEM reliever"**: some agents seem to help only if taken *before* exertion (prophylaxis), others only *after* (rescue). Timing may matter more than the drug.
- **Naproxen** ~250 mg twice daily appears in patient regimens (sometimes alongside a nightly antihistamine); some report meaningful benefit, others little. **Ibuprofen** is the most commonly cited OTC NSAID that some find reduces PEM. One writer reported **acetaminophen/paracetamol (Tylenol)** seeming to prevent or shorten their PEM (explicitly "a sample of 1").
- Stronger anti-inflammatory tactics used pre-event include **prednisone ~20 mg taken ~4h before** a known demand (reported as effective by some but wearing off after 6–8h, and unsuitable for ongoing use), and combinations of an anti-inflammatory + antihistamine + curcumin redosed through a flare.

**Risks and caveats — important, because this is the request's headline.**

- NSAIDs (naproxen, ibuprofen) carry real harms with regular use: **GI ulceration and bleeding, reflux** (patients in these very threads report giving themselves acid reflux from chronic naproxen — hence "always take with food" and stomach-protection advice), **kidney impairment**, **cardiovascular risk**, and interactions (e.g. with SSRIs, raising bleeding risk — relevant given the SSRI in our intervention history).
- Naproxen **retains sodium and water**. One patient frames this as *helpful* for their orthostatic intolerance (keeps fluid on board for blood volume); but it's the same reason NSAIDs raise blood pressure and strain the kidneys. Double-edged.
- Acetaminophen avoids the GI/renal profile but has its own ceiling and liver limits.

**Honest verdict.** Naproxen for crashes is a *plausible, physician-supervised experiment*, not an established treatment: good mechanistic fit with the endogenous-flare model, thin formal evidence, mixed anecdote, and non-trivial risks that argue for the lowest effective use and medical oversight — and for testing the *timing* (shield vs. relieve) deliberately rather than dosing blind. This is precisely the kind of question an n-of-1 dataset like ours can actually probe (§5).

---

## 4. Other ways to reduce crash depth

Beyond pacing and anti-inflammatories, the measures with the most support or use:

**Rest, applied early and deliberately.** The strongest non-drug lever is **acting at the first sign** — pre-emptive and aggressive rest (flat, dark, quiet, screen-free) at the earliest warning rather than pushing on. Because PEM is delayed, the window to blunt it is often *before* the full crash arrives. Radical rest banked *before* an unavoidable demand also reduces the subsequent hit.

**Cognitive and sensory rest.** Treating mental and sensory input as part of the same budget — reducing screens, noise, light, decisions, and conversation during and after exertion. For many, cognitive rest is as important as physical rest and is routinely neglected.

**Orthostatic measures (for the POTS/OI component).** Since being upright is itself a load, reducing orthostatic stress lowers crash risk: **salt loading (~6–10 g/day), fluids (~2–3 L/day), compression garments (20–30 mmHg, abdominal + legs)**, and doing tasks seated or recumbent. These expand and retain blood volume and are well supported for orthostatic intolerance specifically. (Note the interaction with the NSAID salt-retention point above — and that salt loading needs medical sign-off if blood pressure or kidneys are a concern.)

**Mast-cell / antihistamine approach.** Given the mast-cell strand in §4 of the literature review, some patients with histamine-type symptoms benefit from **combined H1 + H2 antihistamines** (e.g. fexofenadine + famotidine); a treated cohort reported symptom resolution in ~29% and improvement across most symptoms — though notably *not* the dysautonomia, which runs on a different mechanism. Low-risk to trial under guidance.

**Low-dose naltrexone (LDN).** The best-supported *drug* option here, though still preliminary: a 2025 systematic review/meta-analysis of observational studies (no RCTs yet) found a **moderate effect on fatigue and a large effect on pain**, with PEM and energy measures also favouring LDN; a retrospective ME/CFS series had ~74% self-reporting benefit. Generally well tolerated. RCTs are pending, so this is "promising, unproven."

**Other anecdotal supports** (limited/no trial evidence, individual): **Mestinon/pyridostigmine** (~45 mg TID) to raise the PEM threshold; **CoQ10** (~400 mg pre-activity) and **D-ribose** (pre-activity) as "shielders" for some.

**Foundations that lower the baseline crash rate.** Protecting **restorative sleep**, identifying and avoiding personal triggers, and deliberately shifting toward parasympathetic (vagal) tone — slow breathing, calm routines — are widely recommended to make the whole system less crash-prone, even if their per-episode effect is modest.

**Principle across all of these:** the leverage is in **early detection + early response**. Almost everything above works better as prevention or first-sign intervention than as rescue once a deep crash is underway.

---

## 5. What this means for the app

Pulling §§1–4 back to the project, three implications:

**1. The product's job is detection and timing, not prescription.** The user already paces well, so marginal pacing advice adds little. The real value is (a) surfacing the *delayed* cost the person can't intuit, and (b) flagging the early window when rest or a shield is still useful. This fits the manifest principle exactly: *present conclusions, don't make decisions*. The app should never tell someone to take naproxen; it can show them that bad days cluster 48–72h after high-load days, and let them act.

**2. The subjective score is the label that makes any indicator or intervention legible.** Everything in §2 and §3 hinges on connecting an input (load, a drug, salt, rest) to a delayed outcome. The gevoelsscore *is* that outcome variable, with rare 100% coverage. A wearable HR/HRV layer (v2, Garmin) becomes the *leading* indicator the score can't be on its own; the score remains the ground truth that tells you which HR/HRV pattern actually precedes *your* bad day.

**3. The highest-value feature this research points to: a lightweight "what I tried" log feeding an n-of-1 read.** If the user can tag interventions (rested early, took naproxen, salt-loaded, etc.) with timing, the dataset can — carefully, descriptively — test the **shielder-vs-reliever** question for *this person*: does naproxen taken at the first headache sign shorten the sag or the recovery time vs. matched untried days? Does early rest reduce crash depth? This is exactly what the literature can't answer for an individual and what a complete daily time series can at least explore. It must be framed as personal pattern-finding, hedged for confounding (the §3 caveats from the findings doc — regression to the mean, seasonality, reverse causation), and never as proof — but it turns the app from a diary into a personal experiment platform, which is the project's deeper ambition.

The natural sequencing: the existing score + tags already support a manual intervention/recovery-time read (Tier 2). The naproxen/mitigation question gets genuinely interesting at **Tier 3**, once the Garmin layer can corroborate "was this an exertion-flare or an external infection?" and time the leading edge.

---

## Sources

**Pacing & guidelines**

- NICE. *ME/CFS: diagnosis and management (NG206), 2021* — recommendations (do not offer GET; energy management/pacing). [nice.org.uk](https://www.nice.org.uk/guidance/ng206/chapter/recommendations)
- Sanal-Hayes NEM, et al. *A scoping review of 'Pacing' for management of ME/CFS: lessons for the long COVID pandemic.* 2023. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10576275/)
- Clague-Baker N, et al. *Pacing with a heart rate monitor for people with ME/CFS and long COVID: a feasibility study.* Fatigue, 2025. [Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/21641846.2025.2565103)
- Long COVID Physio. *Pacing.* [longcovid.physio](https://longcovid.physio/pacing)
- American ME and CFS Society. *Pacing.* [ammes.org](https://ammes.org/pacing/)
- RTHM. *Pacing for ME/CFS: the energy envelope method* and *Cognitive pacing for brain fog.* [rthm.com](https://www.rthm.com/resources/blogs/pacing-me-cfs)

**Pacing indicators & heart-rate / wearables**

- Workwell Foundation. *Pacing with a heart rate monitor to minimize PEM in ME/CFS and long COVID* (RHR + 15 rule; chronotropic incompetence). [workwellfoundation.org](https://workwellfoundation.org/pacing-with-a-heart-rate-monitor-to-minimize-post-exertional-malaise-pem-in-me-cfs-and-long-covid/)
- Solve ME/CFS Initiative. *Using a heart rate monitor to prevent PEM.* [solvecfs.org](https://solvecfs.org/using-a-heart-rate-monitor-to-prevent-post-exertional-malaise-in-me-cfs/)
- Ruijgt C, et al. *Wearable HRV monitoring identifies autonomic dysfunction and thresholds for PEM in Long COVID.* medRxiv preprint, 2025 (not peer-reviewed). [medRxiv](https://www.medrxiv.org/content/10.1101/2025.03.18.25320115v1)
- Visible / Make Visible — pacing app & armband. [makevisible.com](https://www.makevisible.com/) · ME Association review [meassociation.org.uk](https://meassociation.org.uk/2024/04/visible-the-pacing-app-for-people-with-me-cfs-and-long-covid/)
- *Wearable technology in the management of complex chronic illness: survey results.* 2025. [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12541780/)

**Naproxen / anti-inflammatories & PEM-mitigation practice**

- Health Rising (Cort Johnson). *Post-Exertional Malaise Busters for ME/CFS, FM and Long COVID — Take II* (Younger quote; shielder-vs-reliever; naproxen/ibuprofen/Tylenol/prednisone/Mestinon/CoQ10 reports — patient/expert anecdote). [healthrising.org](https://www.healthrising.org/blog/2022/09/05/post-exertional-malaise-pem-chronic-fatigue-fibromyalgia-long-covid/)
- Solve ME/CFS Initiative. *Treatment FYI: Controlling Pain* (NSAIDs "usually don't work"). [solvecfs.org](https://solvecfs.org/treatment-fyi-controlling-pain/)

**Other mitigations (OI, mast cell, LDN, rest)**

- *Antihistamines improve cardiovascular and other symptoms of long-COVID attributed to mast cell activation* (fexofenadine + famotidine). 2023. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10388239/)
- *Salt supplementation in the management of orthostatic intolerance (VVS and POTS).* Autonomic Neuroscience, 2021. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1566070221001363)
- RTHM. *Salt & fluid loading for POTS.* [rthm.com](https://www.rthm.com/resources/blogs/salt-fluid-loading-pots)
- *Effect of low dose naltrexone for long COVID: a systematic review & meta-analysis.* 2025 (observational; no RCTs). [medRxiv](https://www.medrxiv.org/content/10.1101/2025.09.09.25335451v1.full) · [MDPI](https://www.mdpi.com/2673-8112/5/12/198)
- *Aggressive Rest Therapy / radical rest* — ME and More. [meandmore.net](https://www.meandmore.net/blog/aggressive-rest-therapy-art-and-aggressive-resting)

*Prepared June 2026 for the gevoelsscore project. Pacing and the NICE position are well established; the HRV/PEM-threshold and LDN findings are early-stage; the naproxen/anti-inflammatory material is mechanistic rationale plus patient/expert anecdote, not trial evidence — and any medication change belongs with a physician.*
