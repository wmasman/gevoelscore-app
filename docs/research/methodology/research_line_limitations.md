# Research-line limitations

**Status**: **LOCKED r3**, producer-mode. Authored 2026-06-23 by
Claude under user interview, per §11 step 4 of
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
(r4 LOCKED 2026-06-23). LOCKED 2026-06-23 by user acceptance. r1 → r2
absorbed same-session sanity-check and self-review; r2 → r3 absorbed
a fresh-session `/research-methodology-review` (verdict REVISION
RECOMMENDED, report at
[`reviews/methodology-research_line_limitations-2026-06-23.md`](../reviews/methodology-research_line_limitations-2026-06-23.md))
that caught one substantive factual bug (L7 Example 3 channel-vs-
derivative conflation) and three framing concerns (L4 future-tense
drift, §5 boundary-case under-acknowledgment, §8 vapor-mechanism)
the same-session self-review missed. r3 absorbed all four required
+ six recommended findings; no second-pass review per user decision.
See §8 lock log for the per-revision diff.

---

## 1. Purpose

This document enumerates the **systemic limitations of the research
line**. Systemic limitations apply across the entire corpus and shape
the inference reach of *every* finding the layer produces. They are
distinct from per-HA caveats (which sit inside individual
[`analyses/interpretation/`](../analyses/interpretation/) artefacts and
are tied to that operationalisation): a per-HA caveat is "this HA's
verdict has this specific narrowing"; a systemic limitation is "every
verdict in this research line carries this narrowing because of how
the research line is set up."

The binding rule the layer enforces:

> **Per-topic contextualisation MDs and per-construct actionability
> MDs MUST cite the relevant limitations from this doc.** They are not
> free to invent or omit limitations independently. New systemic
> limitations get added via the same producer-mode lock process as
> other methodology MDs.

Per-stage requirements: see §5 below.

## 1.5 Scope and exclusions

**In scope.** Systemic limitations of the *research line* — limitations
that apply across all findings the layer produces because of how the
research line itself is set up (single subject, era boundaries, device
constraints, analyst-is-subject coupling, data-layer semantics,
self-reporting, survivorship).

**Out of scope.**
- **Per-HA caveats** — these live in each HA's
  [`hypothesis.md`](../analyses/hypotheses/) §8 and propagate into
  `interpretation.md` artefacts. Per-HA caveats are tied to that
  operationalisation; systemic limitations apply regardless of
  operationalisation.
- **Layer-process limitations** — limitations introduced by the
  results-analysis layer itself (e.g., the
  [`/research-interpret`](_plan_results_analysis_layer.md#7-the-skill--research-interpret)
  skill's interview-engine choices). Those belong in the
  [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  itself. **Caveat**: the producer-vs-reviewer split's imperfect
  blinding (drafter and fresh-session reviewer are the same LLM model
  with different session contexts, not different agents) is a
  borderline case — it's a layer-process choice but its *consequence*
  is an L4 manifestation. L4's mitigation caveat surfaces this; the
  layer-process exclusion is *not* a free pass on the blinding limit.
- **Infrastructure limitations** — data-pipeline bugs, extraction-
  script issues, methodology MD revisions. These are
  [`garmin_indicators_audit.md`](garmin_indicators_audit.md) territory.
- **External-research limitations** — limitations of the *published
  literature* this corpus is compared against. Those are captured per-
  topic in [`analyses/contextualisation/topic-*.md`](../analyses/contextualisation/)
  artefacts.

The seven limitations in §3 are intended to be **exhaustive for the
in-scope category as of 2026-06-23**. Adding new in-scope systemic
limitations follows §6.

## 2. Why this is a layer-level binding rule

Without this doc, every topic or construct artefact would re-state the
systemic limitations from memory — inconsistently or, worse, omit some.
A central, citable enumeration:

- gives readers (the subject, a clinician, a fellow PAIS patient, an
  external researcher) the same systemic context for every finding;
- forces the layer's outputs to be commensurate across constructs;
- routes new limitations (when they surface) into a single lock
  process instead of being silently absorbed into one artefact's
  caveat list;
- aligns with [STROBE](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf)
  §12d (limitations are a required reporting element of observational
  research) and [CENT-N-of-1](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf)
  item 21 (limitations stated explicitly for N-of-1 designs).

**Alternatives considered.** The natural alternative is exhaustive
per-HA caveat lists carrying every systemic limitation, restated per
artefact. That alternative was rejected for three reasons:
(a) drift — without a single source of truth, the per-HA restatements
diverge over time and inconsistencies emerge;
(b) omission — systemic limitations get accidentally left out of
artefacts whose author didn't have them top-of-mind;
(c) review burden — every artefact's caveat list becomes load-bearing
prose that must be re-reviewed each lock cycle. Centralising the
systemic limitations here moves the review burden to *this* MD and
lets downstream artefacts cite-by-reference, which is the cheaper
discipline.

Per-HA caveats remain valid and required at their level. This doc does
not replace them; it sits underneath and applies independently.

## 3. The seven systemic limitations

Each limitation below has the same shape:

- **What** — one-paragraph statement.
- **Why it matters** — the consequence for inference reach.
- **Project-specific manifestation** — how this limitation actually
  shows up in this corpus.
- **Forbids** — claims the limitation rules out.
- **Permits** — what can still be claimed honestly.
- **Where it must be cited** — which downstream artefact types must
  explicitly invoke this limitation.
- **Literature anchor** — where N-of-1 standards bound the inference
  reach.

---

### L1. Single-subject reach

**What.** The research line studies one subject (N=1). All findings
are about that subject; group-level inference is bounded by the
N-of-1-to-group reach that the published N-of-1 standards establish.

**Why it matters.** Statistical inference about populations requires
N > 1 by definition. An N-of-1 study can establish facts about its
subject and can be a hypothesis-generating prior or a confirming
observation for group-level work — but it cannot, on its own, settle
questions about "people like me."

**Project-specific manifestation.** Single subject (the project's
author). Coverage: LC era 2022-04-04 onwards ≈ 1500 days (per
[`lc_phase_descriptive.md`](lc_phase_descriptive.md) snapshot table);
Stratum 4 (primary analytic surface) 2022-09-03 onwards ≈ 1390 days.
The corpus is dense longitudinally and structurally absent cross-
sectionally.

**Forbids.**
- Claims about "PAIS patients in general" derived from this corpus
  alone.
- Generalisation beyond the inference-reach bounds set by Daza 2018,
  CENT-N-of-1, Natesan 2023, WWC SCED standards.
- Treating this corpus's findings as a refutation of group-level
  published consensus (the corpus is one observation against many).

**Permits.**
- Claims about this subject across this time window.
- Use as a hypothesis-generating prior for group-level work
  (per Daza 2018 N-of-1 framing).
- Convergence-with-consensus claims when this subject's finding agrees
  with group-level evidence (the corpus *adds* a data point, but does
  not *settle*).

**Where it must be cited.**
- Every `topic-*.md` contextualisation MD's §3 comparability check.
- Every `construct-*.md` actionability MD at tier-2+.
- Every translation-stage artefact's honest-uncertainty section.

**Literature anchor.**
[`literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf`](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf);
[`shamseer_2015_cent_consort_nof1.pdf`](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf);
[`natesan_2023_nof1_evidence_reporting_systematic_review.pdf`](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf);
[`wwc_2022_standards_handbook_v5_0.pdf`](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf).

---

### L2. Era confounds

**What.** The corpus spans multiple eras that differ on dimensions the
subject cannot rerun under controlled conditions: COVID variants,
vaccination history, medication phases, life circumstances. Eras are
not interchangeable; aggregating across them requires explicit
warrant.

**Why it matters.** A trend across eras may reflect any of: a real
within-subject change, a confound that shifted at an era boundary, or
both. The corpus cannot, without extra structure, distinguish these.

**Project-specific manifestation.** Era stratification per
[`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md):

- **Stratum 1**: pre-corona, `lc_phase == 'pre_corona'`, dates
  < 2022-03-21. Garmin-only coverage Aug 2021 → Mar 2022 (single
  winter + shoulder cycle; illness-state × season confound by
  construction per `lc_era_temporal_segmentation.md` §1 caveat).
- **Stratum 2**: acute corona infection, `lc_phase == 'corona_infection'`,
  2022-03-21 → 2022-04-03 (14 days, Garmin only, too short for most
  analyses on its own).
- **Stratum 3**: LC-pre-gevoelscore, `lc_phase == 'lc'` AND no
  gevoelscore, 2022-04-04 → 2022-09-02.
- **Stratum 4**: LC-with-gevoelscore-and-crash-labels,
  `lc_phase == 'lc'` AND has gevoelscore, 2022-09-03 onwards.
  **Primary analytic surface** for Wiggers pre-regs.

**Strata are HARD BOUNDARIES** per
[`phase_axis_collapsibility_conventions.md`](phase_axis_collapsibility_conventions.md)
§3.4 — pooling across them mixes healthy / acute-viral / chronic-
illness states and the pooled estimate is uninterpretable as a coherent
quantity. The collapsibility conventions provide 3 within-LC tiers for
hypothesis-driven pooling of recovery-phase axis (per
[`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md)) sub-phases
when warranted; no data-driven collapse pathway exists.

**Within-Stratum-4 sub-segmentation** (added 2026-06-19): the
[`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) MD §3.3-§3.5
provides recovery-phase sub-phases (4a + 4b) with M1 lived-experience +
M2 documented-confounder warrant framework. Citalopram phase
stratification is in [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md).

**Medication phases inside Stratum 4**: unmedicated (2022-09-03 →
2024-04-08) → citalopram (2024-04-09 onwards). The "2024-04 cluster"
contains two intervention events 7 days apart — citalopram start
2024-04-09 AND CPAP end 2024-04-16 — and is structurally unanalyzable
at every buffer per [CONVENTIONS §3.8](../CONVENTIONS.md#38-boundary-spacing-minimum-for-pre-vs-post-window-designs)
+ [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md)
§8.1. It is excluded from most primary HA analyses.

**Forbids.**
- Aggregating across hard-boundary strata (Stratum 1 / 2 / 3 / 4).
  Pooling here is a category error per `phase_axis_collapsibility_conventions.md`.
- Aggregating across medicated vs unmedicated Stratum 4 without
  explicit warrant + per-phase reporting + the
  `citalopram_phase_stratification.md` §5 correction discipline.
- Treating "all LC era" as homogeneous (Strata 3 + 4 are not
  interchangeable; nor are Stratum 4 unmedicated vs medicated).
- Reading a multi-year trend as a within-subject change when an era
  boundary or intervention lies inside the window.

**Permits.**
- Within-era / within-phase claims (especially within Stratum 4
  unmedicated, the primary surface).
- Hypothesis-driven pooling across recovery-phase sub-phases per the
  3-tier collapsibility framework in
  `phase_axis_collapsibility_conventions.md`.
- Cross-era descriptive contrasts (e.g., Garmin-only Stratum 1 vs
  Strata 3/4) with explicit season + illness-state confound
  attribution.
- Sub-segmentation inside Stratum 4 with declared methodological
  warrant per [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)
  (M1 / M2 / M3 sub-segments) or via the recovery-phase axis.

**Where it must be cited.**
- Every `interpretation.md` whose HA uses multi-era or multi-phase
  data.
- Every `cluster-*.md` that synthesises HAs across different era
  strata or medication phases.
- Every `topic-*.md` contextualisation MD's comparability check.
- Every `construct-*.md` actionability MD (the actionable claim is
  only as valid as the era it was tested in).

**Literature anchor.**
[STROBE §16](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf)
(report confounders considered; quantify if controlled-for) crossed
with project-internal era methodology
([`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md),
[`phase_axis_collapsibility_conventions.md`](phase_axis_collapsibility_conventions.md),
[`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md),
[`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)).

---

### L3. Device generations

**What.** Wearable signals are device-specific. Garmin firmware
versions, model changes, and underlying algorithm updates can shift
the semantics of derived signals (stress, body battery, RHR, HRV
proxies) without changing the column name in the corpus.

**Why it matters.** A "stress_mean_sleep" value from one device
generation may not be commensurate with the same column from a later
generation. Calibration drift accumulates silently.

**Project-specific manifestation.** Forerunner 245 (FR245) with
Elevate V3 sensor across the corpus. No hardware upgrade has occurred
yet within the analyzed window. Future device upgrades would trigger
this limitation immediately. Some signals are absent on FR245
entirely:
- **HRV** — no direct HRV channel. Substitute operationalisations
  (HA07c, HA08c, HA07d) already ran using sleep-stress as the HRV
  proxy per [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md). The
  original HA07 + HA08 are **SUPERSEDED** by these proxy operationalisations
  per [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
  §9.4 (decision D4); the HA07-proxy / HA08-proxy successor slots
  reserved in the §11 step 5 synthesis-structure map continue that
  adaptation as pre-reg successors to the SUPERSEDED originals.
- **REM sleep** — `sleep_rem_min` does not exist (Elevate V3 produces
  no REM-stage classification); all non-deep / non-awake sleep
  aggregates into `sleep_light_min` per [`DATA_DICTIONARY.md`](../DATA_DICTIONARY.md)
  §sleep_light_min note.

**Forbids.**
- Treating signal values across device generations as identical
  without explicit reconciliation.
- Claims about absolute signal values (vs within-device-generation
  relative changes).
- Cross-device-generation longitudinal trend claims without explicit
  calibration evidence.

**Permits.**
- Within-device-generation analysis (the entirety of the current
  corpus).
- Within-device-generation longitudinal trends.
- Use of derived signals whose Garmin definition is stable (the
  consolidate pipeline's `garmin_indicators_audit.md` documents
  per-column provenance).

**Where it must be cited.**
- Every `interpretation.md` whose HA uses Garmin-derived signals
  (almost all of them).
- Every `topic-*.md` that compares to group-level wearable studies
  using different device generations.

**Literature anchor.**
[`literature/nelson_2020_wrist_wearable_hr_guidelines.pdf`](../literature/nelson_2020_wrist_wearable_hr_guidelines.pdf)
(consumer-wearable HR measurement reporting standards).

---

### L4. Analyst-is-subject

**What.** The researcher (Willem) is also the study participant. The
two roles cannot be separated; the researcher cannot blind themselves
to their own data; introspection enters at every stage.

**Why it matters.** Standard experimental controls (blinding,
between-arm allocation, intent-to-treat) are not available. Selection
effects in what gets tested are real: hypotheses are formed partly
from lived experience. Lived experience also enters as a *substantive
data layer* (era boundaries, crash labels, intervention timing) that
no external observer could provide.

**Project-specific manifestation.** The project's author drafted the
corpus (notes, triage), curated the methodology MDs, drafts the HAs,
co-authors the result interpretations with Claude (an LLM assistant).
The producer-vs-reviewer split in
[`CONVENTIONS.md`](../CONVENTIONS.md) §1 exists partially to mitigate:
producer-mode artefacts (descriptive, methodology, infrastructure) are
Claude-edited; reviewer-mode artefacts (HA result, synthesis,
interpretation) get fresh-session peer review.
[CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory)
makes prior-driven hypotheses confirmatory, not exploratory, to honour
this honestly.

**Crucial mitigation caveat: the LLM-assistant is not a substitute
for external peer review.** Claude is part of the drafting pipeline
as much as the reviewing pipeline; it has no independent identity
across "drafting session" vs "fresh-session reviewer" beyond the
session-context boundary itself. The fresh-session-review discipline
puts a hard line through shared session-state, which is a real check
— but it is not equivalent to an external researcher with a different
training set, different lived experience, and structurally different
incentives. **As of 2026-06-23 no external researcher has reviewed
any artefact in this corpus.** The L4 mitigation reach is exactly the
session-context-boundary depth of the fresh-session discipline plus
the producer-vs-reviewer-mode split's role-typed work routing. The
listed external-review pathways (external-research follow-ups per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.11; future group-level researchers reading translation artefacts
per Stage T) are L4's *planned future mitigation*, not its current
state.

**Meta-recursion note.** The L4 mitigation caveat above was authored
by the same agent (Claude) that L4 is about. The recursion is itself
an L4 manifestation: drafter-is-also-self-mitigation-author. Partial
mitigations: (a) the present fresh-session reviewer reading this
caveat cold and accepting or rejecting its honesty (the r2 → r3
review caught a precursor of this — the original r2 framing drifted
into aspirational future-tense, which a fresh-session pass corrected);
(b) the user (the project's author + study subject) reads the caveat
each lock cycle and can reject self-serving framings. Neither
mitigation breaks the recursion; both bound it.

**Forbids.**
- Claims that depend on blinding or arm-allocation being possible.
- Treating user-prior-driven hypotheses as exploratory (per
  CONVENTIONS §4.3 they are confirmatory and constrained accordingly).
- Treating the researcher's interpretation as objective-by-distance —
  it is informed-by-proximity instead.

**Permits.**
- Subject-as-coder transparency: lived-experience priors enter
  artefacts explicitly (per the §6.2 interpretation outline §6
  "lived-experience prior reconciliation").
- Lived experience as substantive data where the analyst's
  introspection is the only available source (era qualitative
  boundaries; symptom phenomenology; crash narratives).
- The fresh-session review discipline acts as the imperfect-but-real
  external check.

**Where it must be cited.**
- Every `interpretation.md` whose §6 lived-experience prior is
  non-empty.
- Every `cluster-*.md` whose synthesis depends on the researcher's
  lived judgment of which HAs cluster.
- Every `construct-*.md` actionability MD at tier-2+ where lived
  experience drove the tier-aspiration choice.

**Literature anchor.**
[`literature/methodology/tate_2016_scribe_single_case_reporting.pdf`](../literature/methodology/tate_2016_scribe_single_case_reporting.pdf)
(SCRIBE item on participant-as-researcher transparency in single-case
designs).

---

### L5. Presence-conditioned data layer

**What.** A substantial portion of the corpus's derived signals come
from triaged notes via the v24 categorisation. These signals are
**presence-conditioned positive evidence**, not prevalence panels:
absence of a category in a day's notes does not mean the symptom was
absent; it means it was not written about.

**Why it matters.** Treating presence-conditioned signals as
prevalence indicators produces systematic underreporting of symptoms
on days with light/short notes and apparent overreporting on days
with rich notes. The signal's semantics are about what got mentioned,
not what was experienced.

**Project-specific manifestation.** v24 categorisation per
[`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md).
Affected columns include `cat_*`, `state_*`, `day_dominant_polarity`,
and the `per_day_intensity` loads (loads are presence-conditioned
because they were assigned by reading what was written). The
descriptive programme uses these as positive-evidence overlays, not
as prevalence panels.

**Usage in the HA corpus** (per
[`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
§7): no HA in the current corpus runs a *primary* test on a v24-
derived signal. Where v24 signals do appear in HAs (e.g., HA-C4b v3
§8 pacing-behaviour confounder caveat; various `cat_belasting_*` /
`state_symptoom_*` caveats in older HAs) they enter as descriptive
companion / caveat class. The presence-conditioned semantics rule
binds those usages too — caveat-class citation must respect the
asymmetry, not import prevalence framing.

**Forbids.**
- Prevalence claims from v24-derived signals (e.g., "the subject
  experienced X N% of days").
- Absence-as-evidence-of-non-symptom reasoning on v24-derived
  signals.
- HA test designs whose primary predictor or outcome is a
  presence-conditioned v24 signal interpreted as prevalence (per the
  descriptive-companion-only discipline).

**Permits.**
- Presence-conditioned positive-evidence claims ("on days where X was
  mentioned, Y also tended to be mentioned").
- Descriptive shape of mention counts conditional on mention.
- Use of v24 signals as caveats or sensitivity arms in HAs whose
  primary uses `daily_computed` channels.

**Where it must be cited.**
- Every `interpretation.md` whose HA uses any v24-derived signal,
  even as a sensitivity arm.
- Every `cluster-*.md` whose synthesis touches a v24-derived
  construct.
- Every translation-stage artefact (research-audience and patient-
  audience) where a v24-derived finding might be misread as
  prevalence by an audience untrained in the asymmetry.

**Literature anchor.** Primarily internal — the
[`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md) MD is
the binding source. The broader principle (presence-conditioned text
data ≠ prevalence-of-experience) is a generic discipline in qualitative-
to-quantitative coding work without a single canonical external
citation; the closest analogue is the social-science literature on
diary-study missingness asymmetry (no curated reference in
`literature/` at this revision; flagged for follow-up acquisition per
[`_pending_literature_fetch.md`](_pending_literature_fetch.md) pattern).

---

### L6. Self-reporting

**What.** The `gevoelscore` signal — the daily subjective
"how-am-I-doing" entry — is self-reported. It is affected by
interoception, mood, time-of-entry, recall artefacts, and the
situational context at entry-time.

**Why it matters.** Self-report data has well-documented systematic
biases: end-of-day reporters smooth over rough mid-days; mood at entry
colours retrospective judgment; introspection accuracy varies by
person and condition. PAIS specifically is associated with
interoceptive disturbance; the subject's self-report is potentially
*especially* noisy compared to general-population self-reporting.

**Project-specific manifestation.** `gevoelscore` (1-10 daily scale
since 2022-09-03 = Stratum 4 start). Used as both predictor and
outcome across the HA corpus. No second-reporter validation; no
across-time-of-day reliability data.

**Forbids.**
- Treating `gevoelscore` as an objective biomarker.
- Claiming reliability or test-retest stability without measurement.
- Using `gevoelscore` differences smaller than the subject's likely
  noise floor (a single point on the 1-10 scale may not be
  meaningful even when statistically significant).
- Cross-subject comparison claims (n/a in this single-subject design
  but principle holds for future N-of-1 federations).

**Permits.**
- Within-subject longitudinal use, with the noise floor caveat
  declared.
- Use as the subjective ground-truth for outcomes whose objective
  measurement is not available.
- Coupling with objective wearable signals as a methodological
  triangulation pattern (this is what most HAs do).

**Where it must be cited.**
- Every `interpretation.md` whose HA uses `gevoelscore` as predictor
  or outcome (most of the corpus).
- Every translation-stage artefact whose patient-audience track
  could be read as "your daily score = your true state."

**Literature anchor.**
[`literature/moshe_2021_smartphone_wearable_depression_anxiety.pdf`](../literature/moshe_2021_smartphone_wearable_depression_anxiety.pdf)
(self-report-vs-wearable reliability in mental health contexts;
analogous to PAIS self-report-vs-Garmin reliability);
[`literature/obrien_2023_lc_episodic_disability_qualitative.pdf`](../literature/obrien_2023_lc_episodic_disability_qualitative.pdf)
(LC episodic-disability qualitative work; interoceptive disturbance
context for PAIS self-report). Direct citation of self-report
reliability standards in PAIS-adjacent populations is sparse;
flagged for follow-up literature acquisition per
`_pending_literature_fetch.md` pattern.

---

### L7. Survivorship

**What.** Only days where data was collected appear in the corpus.
Missingness is not random for some signals: rough days may miss the
Garmin-charge window; days where the subject was hospitalised or off-
grid have no wearable signal; days where notes weren't written have
no v24 layer; days where `gevoelscore` wasn't entered have no
outcome.

**Why it matters.** Analytical n is not corpus calendar n. A
correlation computed on days-with-data may not generalise to days-
without-data — and if missingness correlates with the variable of
interest (e.g., rough days = missing wearable), the correlation is
biased in a known direction.

**Project-specific manifestation.** Calendar days: LC era 2022-04-04 →
present ≈ 1500 (per `lc_phase_descriptive.md` snapshot); Stratum 4
(primary surface) 2022-09-03 → present ≈ 1390. HA-specific gates drop
substantial fractions in specific cases:

- *Example 1*: HA-C3 unmedicated primary runs on ≈ 581 days
  (essentially full Stratum-4 unmedicated window after exclusion of
  the 2024-04 cluster + a small number of NaN drops on
  `all_day_stress_avg` / `gevoelscore`). Drop: ~3 of ~584. Mild.
- *Example 2*: HA-C4 v2 chain-T+1 rule dropped 16 of 41 validate
  heavy-T days (~39% dropout of the heavy-T cell), triggering the
  Ch3 validate INCONCLUSIVE n=25 routing. Substantial; the routing
  exists because the gate's missingness was load-bearing.
- *Example 3*: the `respiration_avg_sleep_lagged_lcera_z` **derivative**:
  ~23% fill on Stratum 4 (per DATA_DICTIONARY `*_lagged_lcera_z` table).
  The 77% missingness is **structural to the lagged-baseline window
  construction**, NOT the device — the source `respiration_avg_sleep`
  channel itself has ~97.1% fill (1704/1755 days per DATA_DICTIONARY
  §sleep_extras_daily). The derivative requires baseline values from a
  `[d-90, d-30]` window restricted to LC-era days; that construction
  lops off all pre-LC days and any day inside a 90-day Garmin gap,
  regardless of source-channel coverage. This is a methodology-derived
  L7 manifestation (per the lagged-baseline discipline in DATA_DICTIONARY
  §lagged_lcera variants), not an L3 device-generation manifestation.
  Naming the upstream correctly matters: addressing this dropout means
  revisiting the baseline-window choice, not the wearable.

Missingness patterns vary by signal:

- `gevoelscore`: subject-controlled; missing on days the subject
  didn't enter.
- Garmin nightly signals: missing if no wear during the night.
- Notes-derived signals: missing if no notes that day.
- Hospitalisation / off-grid windows: missing on essentially all
  signal classes.

**Forbids.**
- Treating analytical n as if it were the corpus calendar n.
- Cross-era trend claims without missingness audit
  (per-era missingness can confound trend perception).
- Claims about "no event on day X" when day X is missing data on
  the relevant signal.
- Aggregating across signals without checking joint missingness
  (a 1000-day-each correlation between two signals computed
  pairwise-complete may overstate density).

**Permits.**
- Explicit missingness-aware analysis (declared in HA pre-reg §4).
- Per-signal coverage audits (already part of the descriptive
  programme).
- MCAR/MAR-compatible missingness handling per the §6.1 audit
  checklist of [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md).

**Where it must be cited.**
- Every `interpretation.md` whose HA has non-trivial gating (most of
  the corpus).
- Every `cluster-*.md` whose member HAs have different effective ns
  (the synthesis is only as strong as the smallest member's
  effective coverage).
- Every longitudinal-trend claim in any stage.

**Literature anchor.**
[`literature/methodology/vonelm_2007_strobe_observational_checklist.pdf`](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf)
§13a (participants reported at each stage; missingness reporting in
observational studies).

---

## 4. The seven limitations summarised

| ID | Limitation | Primary corpus manifestation |
|---|---|---|
| L1 | Single-subject reach | One subject; ~1500 LC-era days; ~1390 Stratum 4 days |
| L2 | Era confounds | Strata 1–4 HARD BOUNDARIES; Stratum 4 primary; unmedicated → citalopram 2024-04-09; 2024-04 cluster (citalopram + CPAP-end 7 days apart) excluded |
| L3 | Device generations | FR245 (Elevate V3) entire corpus; no direct HRV (proxy via sleep stress runs); no REM-stage signal |
| L4 | Analyst-is-subject | Researcher = participant; producer-vs-reviewer split mitigates partially; LLM-assistant is *not* a substitute for external peer review |
| L5 | Presence-conditioned data layer | v24 categorisation; `cat_*`/`state_*`/`per_day_intensity`; no HA uses v24 as primary signal but caveat-class usage applies |
| L6 | Self-reporting | `gevoelscore` daily subjective 1-10; no second-reporter validation |
| L7 | Survivorship | Analytical n ≠ calendar n; gate-driven dropouts; per-signal missingness varies (some structural to L3) |

## 5. How downstream artefacts cite this doc

The binding rule from §1 applies as follows:

| Artefact type | Citation requirement |
|---|---|
| `descriptive_audit.md` | Cite L5 and L7 explicitly where the audit's checklist depends on them (the §6.1 v24-presence-conditioning item maps to L5; the §6.1 missingness item maps to L7). |
| `interpretation.md` | Cite every limitation that touches the HA's primary signals or operationalisation. List by L-ID with one-sentence project-specific application. |
| `cluster-*.md` | Cite every limitation that touches any cluster member; also cite L2 if cluster members are from different era strata. |
| `topic-*.md` | **MUST cite L1, L2, L4 unconditionally** (every topic-level positioning sits inside the single-subject + era-stratified + analyst-is-subject envelope). Cite L3, L5, L6, L7 as they apply. |
| `construct-*.md` (actionability) | **MUST cite all seven, with explicit applicability-or-NA per limitation** (actionability is the downstream-most claim and inherits all systemic context). |
| Translation artefacts | Patient-audience track translates the *applicable* limitations into plain-language honest-uncertainty wording per §6.6 of the plan. Research-audience track keeps the L-IDs as cross-references. |

A citation is *not* a copy-paste of the limitation's full statement.
It is a one-line acknowledgment with the L-ID and one sentence on how
this limitation applies to *this artefact's specific claim*. Examples:

> *Per-HA interpretation citing L2*:
> Cites L2 (era confounds): this HA spans Stratum 4 unmedicated only;
> the cross-era projection to medicated Stratum 4 is out of scope.

> *Per-HA interpretation citing L7*:
> Cites L7 (survivorship): the n=581 effective coverage represents
> ~42% of Stratum 4 calendar days; results do not generalise to
> Garmin-coverage-gap days.

> *Cross-cutting multi-cite at the cluster level* (e.g. a `cluster-*.md`
> synthesising HAs whose members touch crash days, era boundaries, and
> lived-experience priors):
> Cites L1+L2+L4: this cluster's joint claim is single-subject
> (L1 inference reach per Daza 2018 bounds it); all member HAs run on
> Stratum 4 unmedicated only (L2 forbids cross-phase pooling without
> warrant; none added here); the cluster's coherence call relied on
> lived-experience-prior reconciliation of a discordant HA pair
> (L4 — recorded transparently per the synthesis guide §6.3).

**The four ready HAs as a boundary case.** The four HAs ready for
Stage D TRUSTED (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo) were
locked **on or one day before** this MD's draft date — HA-C3 v2,
HA-C3p, HA-C4c on 2026-06-23 (same day); HA11-bout-redo on 2026-06-22.
They are coeval with this MD, not pre-existing in any meaningful sense.
Their `hypothesis.md` §8 "Caveats" sections already cover the
substantive content of L1/L2/L3/L6 in non-L-ID language (e.g. HA-C3 v2
§8.2 "n=1 single-subject caveats per CONVENTIONS §3.1"; §8.3
"Citalopram-phase confound + chosen mitigation"; §8.4 "Crash-day
inclusion structural fragility"; §8.5 "Within-subject shape, NOT
between-subject prediction"). The choice to NOT retroactively add
L-ID labels to those §8 sections is a **separation-of-concerns choice**
(pre-regs declare operationalisation; interpretations declare what
verdicts mean given systemic context), **not** a hard "we cannot edit
locked pre-regs" constraint.

The discipline going forward:
- Their downstream `interpretation.md` artefacts (drafted in §11 step 8
  dry-run + step 11 rollout) DO cite this doc per the §5 table above
  with explicit L-IDs.
- The systemic limitations enter the layer's pipeline at the
  *interpretation* stage. That is the intended discipline.
- **Future HAs pre-registered after this MD locks SHOULD cite the
  applicable L-IDs in their `hypothesis.md` §8 caveats section** so
  the citation enters at pre-reg time. The four ready HAs sit exactly
  at the boundary of the rule; they fall under the interpretation-
  stage discipline because the pre-regs were drafted before this MD
  existed (by hours, not weeks) and rewriting their §8 sections to
  use L-IDs would unhelpfully blur the producer-vs-reviewer split
  that locked them.

## 6. Adding a new systemic limitation

If a future session identifies a systemic limitation not enumerated
above (e.g., a newly-discovered confound, a methodological change
that introduces a new category of caveat), it gets added via the
same producer-mode lock process used for this doc:

1. Producer-mode drafting session: extend §3 with a new L-section
   following the seven-field shape (What / Why / Manifestation /
   Forbids / Permits / Where cited / Literature anchor).
2. Update §4 summary table and §5 citation requirement table.
3. Update §3.9 of [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
   if the new limitation needs the layer-rule itself adjusted (rare).
4. **Update [`methodology/README.md`](README.md)** "Read these in
   order" list if the L-section count or the doc's relative position
   in the read-order changes.
5. Fresh-session `/research-methodology-review`.
6. User explicit acceptance to lock.
7. Per §3.7 drift policy: the lock-version increment triggers
   re-examination of every artefact that cited an outdated version,
   producing CONFIRMED-NO-CHANGE entries or REVISED artefacts.

Limitations are **append-only** in practice — removing a limitation
should be exceptional and requires the same producer-mode drafting +
fresh-session review process, with a documented rationale for why
the limitation no longer applies (e.g., new methodology resolves a
prior systemic concern).

## 7. Drift triggers for this doc

Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.7, this MD is re-examined under any of:

**Generic triggers (from plan §3.7).**

- A cited methodology MD changes lock-version
  (e.g., [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md)
  is updated, which would propagate to L5).
- 6-month cadence (default).

**Project-specific triggers (added at this MD's drafting).**

- **New intervention event** lands in the corpus (new medication start
  or stop, new therapy initiation, hospitalisation cluster) — triggers
  L2 revisit; may need a new sub-phase added to
  [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)
  or a parallel intervention-phase MD.
- **Device upgrade** (e.g., FR245 → FR255 or Fenix 7) — triggers L3
  immediately; existing within-device-generation analysis remains
  valid but the upgrade-day becomes a new hard boundary; calibration-
  reconciliation discipline kicks in.
- **v24 categorisation version bump** (v25 dictionary lands) —
  triggers L5; presence-conditioned semantics rule continues to bind
  but the categorisation phrase dictionary changes.
- **New COVID infection / vaccination event** — triggers L2 revisit;
  new acute-infection or post-vaccination window may need a sub-
  stratum.
- **N-of-1 standards literature** gains a new reference of moderate-
  or-higher relevance — triggers L1.
- **Layperson test failure during translation** (per §11 step 9d)
  exposes that one of the limitations is poorly translatable to the
  patient audience — triggers a §6.6 translation-guide revisit AND
  potential re-wording of the offending L-section in this MD.

Re-examination outcomes per §3.7: CONFIRMED-NO-CHANGE (timestamped
log entry below) or REVISED (new version of this MD under the same
lock process, prior version archived).

## 8. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-23 | Drafted r1 | Producer-mode under user interview; initial seven limitations per `_plan_results_analysis_layer.md` §3.9. NOT LOCKED. |
| 2026-06-23 | Revised r1 → r2 | Same-session sanity-check + self-review at user request. Fixes: E1 citalopram date 2024-04-08 → 2024-04-09; E2 2024-04 cluster expanded to citalopram + CPAP-end; E3-E4 Stratum 1/2 boundaries corrected; E5 day counts (1363 → ~1500 LC / ~1390 Stratum 4); E6 subject name neutralised; E7 added refs to `lc_recovery_phase_axis.md`, `phase_axis_collapsibility_conventions.md`, `citalopram_phase_stratification.md`, `intervention_effects_descriptive.md`; E8 L3 HRV-proxy framed as already-run. Additions: §1.5 scope-and-exclusions; §2 alternatives-considered paragraph; L4 LLM-not-substitute-for-external-review caveat; L5 companion/caveat usage acknowledgment; L7 worked examples; §5 retroactive-citation guidance; §7 six project-specific drift triggers. NOT LOCKED. |
| 2026-06-23 | Fresh-session `/research-methodology-review` | Verdict REVISION RECOMMENDED. Report: [`reviews/methodology-research_line_limitations-2026-06-23.md`](../reviews/methodology-research_line_limitations-2026-06-23.md). Caught one substantive factual bug (L7 Example 3 channel-vs-derivative conflation; the source channel is ~97% fill, not ~23%) and three framing concerns (L4 future-tense drift; §5 boundary-case under-acknowledgment; §8 vapor-mechanism). Confirmed-good: doc architecture, §1+§1.5+§2 reasoning, L1/L2/L3-REM/L5/L6 sections, §4-§7 structure, §9 cross-references. |
| 2026-06-23 | Revised r2 → r3 | Absorbed all four fresh-session-review required actions: R1 fixed L7 Example 3 (re-attributed to lagged-baseline window construction, not FR245); R2 tightened L4 caveat closing sentence (future-tense aspiration → present-tense "no external researcher has ever reviewed any artefact in this corpus"); R3 reframed §5 four-ready-HAs guidance as separation-of-concerns choice (with HA-C3 v2 §8 caveats cited concretely); R4 disclosed §8 downstream-citation table dependency on not-yet-built `/research-interpret --drift-check` skill. Plus six recommended actions: A1 L4 meta-recursion paragraph; A2 §1.5 layer-process exclusion caveat acknowledging L4 borderline; A3 §6 added README-index-update step (also separately landed in methodology/README.md); A4 L5 follow-up routed through `_pending_literature_fetch.md`; A5 §5 third example (cross-cutting L1+L2+L4 cite); A6 this entry. Also: L3 SUPERSEDED framing for HA07/HA08 originals per stocktake D4. |
| 2026-06-23 | **LOCKED r3** | User acceptance ("i accept"). Implementation proceeds to §11 step 5 (synthesis_structure_map.md) per `_plan_results_analysis_layer.md`. |

### Downstream-citation count (tracked after lock)

Once this MD locks, every `interpretation.md`, `cluster-*.md`,
`topic-*.md`, `construct-*.md`, and translation artefact that cites
an L-ID gets recorded here, so that any future revision of this MD
(per §7 drift triggers) can compute downstream impact:

| L-ID | Citing artefacts (count) | Last cited |
|---|---|---|
| L1 | 4 | `analyses/translation/{research-audience,patient-audience}/{construct-stress-fatigue-monitoring,topic-stress-fatigue-pacing}.md` §5.5 (Stage T dry-run; DRAFT r1; 2026-06-25) |
| L2 | 4 | `analyses/translation/{research-audience,patient-audience}/{construct-stress-fatigue-monitoring,topic-stress-fatigue-pacing}.md` §5.5 (Stage T dry-run; DRAFT r1; 2026-06-25) |
| L3 | 4 | `analyses/translation/{research-audience,patient-audience}/{construct-stress-fatigue-monitoring,topic-stress-fatigue-pacing}.md` §5.5 (Stage T dry-run; DRAFT r1; 2026-06-25) |
| L4 | 4 | `analyses/translation/{research-audience,patient-audience}/{construct-stress-fatigue-monitoring,topic-stress-fatigue-pacing}.md` §5.5 (Stage T dry-run; DRAFT r1; 2026-06-25) |
| L5 | 4 (cited as NA) | `analyses/translation/{research-audience,patient-audience}/{construct-stress-fatigue-monitoring,topic-stress-fatigue-pacing}.md` §5.5 (Stage T dry-run; DRAFT r1; 2026-06-25 — L5 NA preserved per source binding) |
| L6 | 4 | `analyses/translation/{research-audience,patient-audience}/{construct-stress-fatigue-monitoring,topic-stress-fatigue-pacing}.md` §5.5 (Stage T dry-run; DRAFT r1; 2026-06-25) |
| L7 | 4 | `analyses/translation/{research-audience,patient-audience}/{construct-stress-fatigue-monitoring,topic-stress-fatigue-pacing}.md` §5.5 (Stage T dry-run; DRAFT r1; 2026-06-25) |

**Note on counts**: counts are at the translation-artefact-file granularity (one increment per file that cites the L-ID via §5.5 rendering). All four Stage T dry-run track-files cite L1+L2+L3+L4+L6+L7 (L5 NA preserved per source binding). When upstream-source counts are added (Stage A construct §5.11, Stage S₂ topic §4.7, Stage S₁ cluster §4.5b, Stage I HA-C3 / HA-C3p §4.5b, Stage D §5 audit entries citing L5 + L7), the count totals will grow accordingly; the current counts reflect only the Stage T dry-run propagation per skill responsibility #11. The upstream-source increments are deferred to source-artefact lock events (currently DRAFT-r1 dry-run; not yet locked) to maintain count-integrity per upstream-source LOCKED status as the discipline gate.

**Tracking-mechanism status (current limitation).** The intended
mechanism is the `/research-interpret` skill's `--drift-check` helper
per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§7 skill responsibility 6. **That skill does not yet exist** — it is
built in plan §11 step 7, which is downstream of step 4 that produced
this MD. Until the skill lands, the table is maintained **manually**
by the drafter of each downstream artefact: when an
`interpretation.md` / `cluster-*.md` / `topic-*.md` / `construct-*.md` /
translation MD locks with L-ID citations, the drafting session
increments the relevant count rows above and updates "Last cited" to
the artefact path. The §11 step 7 skill landing will replace this
manual discipline with the automated `--drift-check` mechanism.

---

## 9. Cross-references

- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  §3.9 (the layer rule that binds this doc) and §11 step 4 (the
  implementation step that produced it); §3.11 (follow-up research
  suggestions referenced from L4 mitigation caveat).
- [`CONVENTIONS.md`](../CONVENTIONS.md) §3.8 (boundary-spacing
  minimum for pre-vs-post window designs; binding for the 2024-04
  cluster exclusion in L2); §4.3 (prior-driven hypotheses
  confirmatory; supports L4); §5 timeline anchors (LC era / Stratum
  4 dates).
- [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)
  (era methodology; primary input for L2 stratum boundaries).
- [`phase_axis_collapsibility_conventions.md`](phase_axis_collapsibility_conventions.md)
  (HARD-BOUNDARY rule for the strata; primary L2 binding for the
  forbids/permits split).
- [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) (within-
  Stratum-4 sub-phases 4a + 4b; recovery-phase axis L2 sub-segmentation).
- [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)
  (medication-phase stratification framework; L2 medicated/unmedicated
  binding).
- [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md)
  (intervention-event handling; 2024-04 cluster exclusion logic for
  L2).
- [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md)
  (v24 presence-conditioning; primary input for L5).
- [`nightly_attribution.md`](nightly_attribution.md) (sleep/recovery
  signal attribution; relevant to L3 + L7).
- [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) (resolves the
  HRV gap of L3 for FR245).
- [`garmin_indicators_audit.md`](garmin_indicators_audit.md) (per-column
  provenance; relevant to L3).
- [`lc_phase_descriptive.md`](lc_phase_descriptive.md) (LC-era day-
  count snapshot table; source for the ~1500 LC-era days figure in
  L1 + L7).
- [`DATA_DICTIONARY.md`](../DATA_DICTIONARY.md) (sleep-channel coverage
  fractions; source for L3 REM-stage absence and L7
  `respiration_avg_sleep` example).
- [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
  (§9 user decisions on stocktake findings; §9.4 hardware-blocked HA
  routing; example of L3 manifestation).
- Literature anchors:
  [`literature/methodology/`](../literature/methodology/) — Daza 2018,
  CENT-N-of-1, SCRIBE, Natesan 2023, WWC SCED, STROBE;
  [`literature/`](../literature/) — Moshe 2021, O'Brien 2023, Nelson
  2020.
