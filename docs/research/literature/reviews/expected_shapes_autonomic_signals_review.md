# What Shape Should We Expect? Non-Linearity in HRV and Autonomic Signals — A Theory Brief for the "Not a Straight Line" Finding

*Evidence retrieved from PubMed (DOIs linked throughout). Purpose: this brief does not hunt for patterns — it asks the opposite question. Before we trust any shape we find in the felt-state↔Garmin data, what shape does the physiology of the autonomic nervous system actually predict we **should** see? The headline descriptive finding of this project — that the felt-state↔Garmin relationship is **shape-not-linear**, and that one of Wiggers' convex stress→fatigue predictions was rejected in its numbers but reappeared as a real **inverted-U** (spline F=28.27, p=0.0002) — is exactly the kind of result that solid theory either supports or undercuts. This brief sets out what theory says, so the finding is anchored in nervous-system science rather than in curve-fitting.*

*Scope note: this is an n=1 instrument-test, not a claim about other patients. "Expected shape" means *physiologically plausible*, not *proven here*. See [[findings-are-provisional]], [[site-is-medium-not-subject]].*

---

## 1. The one-sentence answer

According to PubMed, a **straight line is the wrong default**: across four independent strands of physiology — the measurement properties of HRV itself, the arousal-performance law, the allostatic/exhaustion trajectory of chronic stress, and the autonomic phenotype of ME/CFS — the expected relationship between an autonomic "stress/activation" signal and a felt or functional outcome is **curved, often inverted-U, sometimes non-monotone at both ends**. A near-zero linear correlation is therefore the *predicted* result of measuring a curve with a straight ruler, not evidence of "no relationship." This is the theoretical backing for why this project leans on event-matched, bout-level and phase-by-phase methods instead of a tidy daily Spearman ρ.

Four strands, each of which alone predicts a non-linear shape:

---

## 2. Strand 1 — HRV is *itself* a non-linear readout of autonomic activity (a measurement fact, before any psychology)

This is the most important and most overlooked point, because it means the curve exists **even if the underlying biology were linear**. The metric is bent by construction.

- **The neural→interval map is non-linear at the sinus node.** According to PubMed, the relation linking autonomic agonist concentration to sinus cycle length is *strongly non-linear* in single sinoatrial myocytes, which imposes an **intrinsic rate-dependency** on virtually all time- and frequency-domain HRV indices — i.e. the same change in neural traffic produces a different change in HRV depending on where you start ([Zaza & Lombardi, 2001, *Cardiovasc Res*; DOI](https://doi.org/10.1016/s0008-6363(01)00240-1)). HRV is not a linear voltmeter for "autonomic tone."
- **HRV and heart rate are bound by a non-linear inverse relation, and removing it changes conclusions.** According to PubMed, the non-linear inverse relationship between RR-intervals and heart rate "contributes significantly" to HRV values; applying an explicit heart-rate correction (dividing HRV by mean-RR to a power) *improved* mortality prediction and minimised the spurious HR-coupling ([Pradhapan et al., 2014, *Front Physiol*; DOI](https://doi.org/10.3389/fphys.2014.00208)). Practical implication for us: an HRV-derived channel (and Garmin/Firstbeat "stress" is HRV-derived) partly tracks mean HR through a curve, so its relationship to anything downstream inherits that curvature.
- **Non-linear models fit autonomic dynamics better than linear ones.** A logistic (non-linear) model of RR-interval fluctuations through rest→exercise→recovery outperformed traditional linear HRV summaries in 272 participants ([Castillo-Aguilar et al., 2025, *Sci Rep*; DOI](https://doi.org/10.1038/s41598-025-93654-6)); and HRV is formally a multiscale, multifractal signal whose structure standard linear summaries miss ([Kokosińska et al., 2018, *Physiol Meas*; DOI](https://doi.org/10.1088/1361-6579/aae86d)). (We already hold the methods caveats locally: Berntson 1997, Shaffer & Ginsberg 2017.)

**Takeaway:** any analysis that correlates an HRV-derived signal linearly against a daily outcome is fighting the metric's own geometry. Near-zero ρ is the *expected* artefact. This alone justifies HR-relative and rate-corrected treatment of the stress/HRV channels.

---

## 3. Strand 2 — The arousal–performance law is an inverted-U (Yerkes–Dodson), and its steepness depends on load

The single most established "shape" in the whole arousal literature is **not** a line — it is an inverted-U. Autonomic activation helps a felt/functional outcome up to a point, then degrades it.

- The Yerkes–Dodson inverted-U between arousal and performance reproduces at the neural level: central-thalamic/dopaminergic stimulation **enhances** working memory at low currents and **impairs** it at higher currents — the same dose flipping sign ([Mair et al., 2010, *Dose-Response*; DOI](https://doi.org/10.2203/dose-response.10-017.Mair)).
- Crucially, **the curve's shape depends on task difficulty**: easy tasks peak at high arousal (closer to monotone), hard tasks show the full inverted-U peaking at *medium* arousal ([Sörensen et al., 2022, *PLoS Comput Biol*; DOI](https://doi.org/10.1371/journal.pcbi.1009976)). This predicts **channel- and context-specificity** — exactly the "channel-specific" texture STOCKTAKE §6 reports — rather than one universal curve.
- The inverted-U shows up *with HRV instrumentation*: mental-workload studies find an inverted-U between workload and performance alongside HRV changes ([Fan et al., 2022, *Int J Environ Res Public Health*; DOI](https://doi.org/10.3390/ijerph191912434)), and stress→behaviour modelling is now routinely framed as curvilinear/hormetic (Yerkes–Dodson), even when a given dataset fails to confirm it ([Voigt et al., 2023, *Appl Ergon*; DOI](https://doi.org/10.1016/j.apergo.2023.104161)).

**Takeaway:** a *curved* (non-monotone) relationship linking measured activation to a felt/functional state is the *textbook prediction*, not an anomaly. HA-C3's significant non-monotone curvature is concordant with mainstream arousal theory; the project's job is to characterise *this body's* particular curve — not to over-name it, and not to be surprised that a curve exists.

---

## 4. Strand 3 — HRV/stress responses to real stressors are empirically curvilinear

Beyond theory, when investigators actually fit non-linear terms to HRV-vs-stress data, the curve appears:

- Under combined techno/financial stress, heart rate and HRV responses were explicitly **curvilinear**, not linear, tracking attentional/behavioural disengagement ([Korosec-Serfaty et al., 2022, *Front Neurosci*; DOI](https://doi.org/10.3389/fnins.2022.883431)).
- A second-degree polynomial (a deliberate curve) modelled the HRV-complexity↔motivation relationship during exercise with R≈.82, cross-validated R≈.67 — substantially better than treating it as linear ([Everett et al., 2026, *Psychol Sport Exerc*; DOI](https://doi.org/10.1016/j.psychsport.2026.103182)).

**Takeaway:** the curvilinear treatment is not exotic; it is how this signal is increasingly modelled. This is direct precedent for using spline/polynomial terms (as HA-C3 v2 did) rather than ρ.

---

## 5. Strand 4 — Chronic stress and the *worst* states: why the peak of badness need not sit at the peak of measured activation

This is the strand that speaks most directly to the project's specific, slightly counter-intuitive result — that the **worst felt days do not line up with the highest measured stress** (felt-state peaks in the *mid* stress band; the curvature is non-monotone). Two literatures explain why that is physiologically expected, not paradoxical.

> **A caveat on naming, before this strand.** HA-C3's result is robustly a *significant non-monotone curvature* (three bin-means 3.96 → 4.27 → 3.83; spline F=28.27; flat ρ=−0.03), **not** verified to be a clean single-humped "inverted-U" — with three bins and a near-empty high-stress tail, and a spline whose curvature flips sign, the precise functional form is under-determined. This brief uses "inverted-U" for the *theoretical* prediction; for *our data* the accurate phrase is "non-monotone curvature, peaking at mid-stress." Keeping the two vocabularies separate avoids the theory and the finding appearing to confirm each other by name. (See the companion note's "On the word 'inverted-U'.")

**(a) Both extremes are damaging — the allostatic-load shape is non-monotone.** In the Whitehall II cohort (n=6764), the association between negative-emotional-response to life events and subsequent multi-system physiological dysregulation (allostatic load) was **non-linear: people at *either* extreme — high *or* absent emotional response — had elevated allostatic load** ([Dich et al., 2014, *Psychoneuroendocrinology*; DOI](https://doi.org/10.1016/j.psyneuen.2014.07.001)). Allostatic-load theory frames stress mediators as protective in the short run but harmful when over-used *or* shut off, explicitly a "non-linear network" ([Schulz et al., 2005, *Psychother Psychosom Med Psychol*; DOI](https://doi.org/10.1055/s-2005-866939)). A signal where both the high end and the low/blunted end mark trouble *is* an inverted-U (or U) by construction — a linear correlation cancels it to ~zero.

**(b) The exhaustion trajectory: activation collapses at the worst stage.** In overreaching/overtraining — a clean model of cumulative load — the autonomic progression is staged: first **sympathetic dominance with reduced vagal tone** (a "stress response"), then, at the most maladapted stage, **"total autonomic dystonia" — depression of *both* sympathetic and vagal regulation** ([Kajaia et al., 2017, *Georgian Med News*; PMID 28480859](https://pubmed.ncbi.nlm.nih.gov/28480859/)). Read onto a wearable "stress/activation" index, this predicts that the *very worst* days can show **lower**, not higher, measured activation, because the system's capacity to mount the response is itself blunted — placing peak badness in the *middle* of the activation range. That direction matches HA-C3's non-monotone curvature (felt-state peaking mid-range), and supplies a physiological reason for it.

**(c) The ME/CFS autonomic phenotype is consistent with this.** ME/CFS sits at the depleted end of HRV: markedly **reduced HRV** with **vagal withdrawal and relative sympathetic predominance**, and a *blunted* ability to mount the normal autonomic response to a challenge:
- HRV indices "strikingly decreased" in CFS children vs syncope and control groups, with the normal sympathetic shift on tilt *failing to appear* ([Stewart et al., 1998, *Clin Auton Res*; DOI](https://doi.org/10.1007/BF02267785)).
- CFS/POTS: attenuated vagal baroreflex with potentiated sympathetic vasomotion; HRV "declined progressively … to CFS" ([Stewart, 2000, *Pediatr Res*; DOI](https://doi.org/10.1203/00006450-200008000-00016)).
- Enhanced vagal withdrawal → sympathetic predominance under mild orthostatic stress in CFS ([Wyller et al., 2008, *Ann Noninvasive Electrocardiol*; DOI](https://doi.org/10.1111/j.1542-474X.2007.00202.x)).

These corroborate the project's own Pattern A (the autonomic-load family — resting HR, overnight/daytime stress — elevates in the 4-day pre-crash lead-up): the signal is *there*, but it lives in a depleted, blunted, non-linear regime where a daily linear average is the wrong instrument.

---

## 6. Strand 5 — Why a curve at all, mechanistically: neurovisceral integration

The unifying "why" is the **neurovisceral integration model**: a prefrontal–autonomic network exerts *inhibitory* (negative-feedback) control over the heart; vagally-mediated HRV indexes the integrity of that inhibitory control. When inhibition is intact, the system is flexible and self-regulating; when it is **compromised, negative feedback gives way to positive-feedback loops and disinhibited sympathetic activation** ([Thayer & Lane, 2000, *J Affect Disord*; DOI](https://doi.org/10.1016/s0165-0327(00)00338-4)). Lower resting vagal HRV predicts poorer real-world emotion regulation ([Williams et al., 2015, *Front Psychol*; DOI](https://doi.org/10.3389/fpsyg.2015.00261)). A control system governed by feedback with a flip into positive-feedback runaway is, by its dynamics, **non-linear** — it produces thresholds, saturation and reversals, not straight lines. This is the mechanistic seat of the inverted-U.

---

## 7. What this means concretely for the project's methods

Theory does not just permit the "not a straight line" finding — it *predicts* it, and gives specific guidance:

1. **Expect, and model, curvature.** A near-zero daily ρ on an HRV/stress channel is the *predicted* signature of a real curved relationship, not a null. Spline/polynomial fits (HA-C3 v2) are the theory-appropriate tool. → strengthens [[descriptive-phase2-and-shape-not-linear]] and the `/workings/not-a-straight-line` page.
2. **HR-correct, or at least HR-aware, the HRV/stress channels.** Because HRV carries a built-in non-linear HR term ([Pradhapan 2014](https://doi.org/10.3389/fphys.2014.00208); [Zaza 2001](https://doi.org/10.1016/s0008-6363(01)00240-1)), some apparent felt-state structure may be mean-HR leakage. Worth a sensitivity check on the stress channels.
3. **Don't assume monotone direction.** The worst days plausibly sit at *mid* activation, because the most depleted/exhausted state blunts the very response the wearable measures ([Kajaia 2017](https://pubmed.ncbi.nlm.nih.gov/28480859/); [Dich 2014](https://doi.org/10.1016/j.psyneuen.2014.07.001)). Both tails can mark trouble. This is the honest reading of HA-C3's non-monotone curvature — and a reason to describe the shape, not to name it a clean inverted-U the three bins can't confirm.
4. **Channel- and context-specificity is expected, not noise.** The Yerkes–Dodson curve steepens with load/difficulty ([Sörensen 2022](https://doi.org/10.1371/journal.pcbi.1009976)); different channels should carry different curves. Supports the per-channel, per-phase framing.
5. **Sub-daily resolution matters.** HRV is multiscale/multifractal ([Kokosińska 2018](https://doi.org/10.1088/1361-6579/aae86d)); a daily mean averages the shape away. Backs the "lives finer than daily" / bout-level methods.

---

## 8. Honest limits

- **n=1, instrument-test.** Every "expected shape" here is a population/physiology prior, not proof for this body. A curve being *plausible* does not make this body's particular curve *established*; HA-C3 remains an informative falsification of Wiggers' specific numbers on this participant's stress range, not a law.
- **Garmin "stress" is a proprietary HRV-derived index** (Firstbeat). It inherits HRV's non-linearity (good — that is the point) but also its black-box processing; treat it as "autonomic activation, curved," not a calibrated stressor dose.
- **Some strands are adjacent, not identical.** Overtraining and allostatic-load cohorts are not ME/CFS; arousal-performance studies measure cognitive performance, not felt-state. They license the *expectation* of a non-linear shape; they don't transplant a specific curve.
- **Searches were PubMed-only** and English-language; the inverted-U / Yerkes–Dodson literature is large and this is a purposive, not exhaustive, sample. Two classic primary sources (Yerkes & Dodson 1908; McEwen's foundational allostatic-load papers) predate or sit outside this PubMed pull and are cited here through their modern reviews.

---

## 9. Bottom line

According to PubMed, the felt-state↔autonomic relationship in this project **should not be a straight line, and theory says so four times over**: HRV is a non-linear transform of autonomic activity before any psychology enters; the arousal–performance law is an inverted-U whose shape bends with load; chronic-stress and exhaustion trajectories make *both* extremes pathological and can place the worst state at *mid* activation; and the governing prefrontal–autonomic control loop is dynamically non-linear. The project's "not a straight line" finding — HA-C3's significant non-monotone curvature, felt-state peaking mid-stress — is therefore **what mature autonomic theory predicts** (that a curve exists, not its exact named form), which is the strongest available defence against the charge of pattern-hunting. The right posture is not "we found a curve, how surprising" but "the physiology told us to expect a curve; here is the one this body actually traces, characterised with curve-appropriate, sub-daily, event-matched tools."

---

*Source database: PubMed. Findings paraphrased; consult primary papers (DOIs above) for methods and data. Research synthesis, not medical advice. Companion to `reviews/PEM_HRV_heart_rate_literature_review.md` and `reviews/SYNTHESIS_wearables_autonomic_PEM_research_programme.md`; supports `/workings/not-a-straight-line` on the site. Classic primary sources (Yerkes & Dodson 1908; McEwen 1998 allostatic load) are referenced via their modern reviews and should be cited directly if used formally.*
