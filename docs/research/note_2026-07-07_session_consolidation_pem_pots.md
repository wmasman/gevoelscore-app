# Research note 2026-07-07: session consolidation + the PEM/POTS reframing

> **Label discipline.** "POTS" here names one of Wiggers' two management threads (the electrolyte-side she takes for the felt within-day stress U-dip), NOT a watch-detectable condition. FR245 is posture-blind, U-dip polarity runs opposite the established POTS HRV signature (vagal withdrawal), and no POTS subtype is trackable to the instrument-bar per [`literature/reviews/pots_operationalisation_wearable_review.md`](literature/reviews/pots_operationalisation_wearable_review.md). See [`methodology/pem_pots_mechanism_framing.md §1.2`](methodology/pem_pots_mechanism_framing.md).

## Authorship

- **Drafted**: 2026-07-07 by Claude (Opus 4.8), producer-mode, under authorization
  from the participant-researcher (repo owner).
- **Status**: **ACCEPTED 2026-07-07.** A consolidation / session-log note. The
  synthesis claims went through the independent fresh-context review
  ([`reviews/pem-pots-reframing-2026-07-07.md`](reviews/pem-pots-reframing-2026-07-07.md),
  MAJOR-REVISIONS folded), accepted by the participant-researcher as the
  [CONVENTIONS section 1.2](CONVENTIONS.md) independent review; the wording below is
  post-review.

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

This note records what a long working session (2026-07-06 to 07) delivered, so it
lands in the research record and the structural additions (catalog, queued-work,
website card) have a single anchor to point back to. Two threads ran: a
**scorecard / phase-axis / site-export analysis batch**, and a **Wiggers-guide
reconciliation that opened a PEM/POTS reframing**.

---

## Part A - the analysis batch (all committed, each with its own findings.md)

| req | commit | one-line result |
|---|---|---|
| **R20** driver-netting overlay | `8875c0b` | Netting the citalopram driver out of the scorecard changes **zero verdicts**; only one scorecard row (HA07c) even uses a beta-carrying channel, and its delta operator makes it dose-immovable. |
| **R19** recovery-phase backdrop | `93de186` | Each scorecard signal's per-phase level + crash-count shape; per-phase discrimination **declined-with-reason** (the only two computable phases are the retired citalopram era-split), keeping it inside single-pool primacy. |
| **R30** confounder bound | `4438764` | The per-phase resting-HR rise is **confounder-dominated** - weight (+3.36) + aging (+1.71) masked by citalopram (-1.04); the illness residual level is flat (~52-53 bpm), no positive phase-level signal identifiable. |
| **R1** fresh lead-up curves | `6fb8407` | Replaced the retired per-era decay / early-vs-late chart fabrications with **real single-pool pooled t-6..t0 curves + null band**. Finding: the departure is **at onset (t0)**, not before - the lead-up sits inside the ordinary-day band even for the SUPPORTED HA07d. Five site chart JSONs emitted; R13 (felt-state timeline) confirmed already shipped. |
| **separability** | `7485c12` | PEM and POTS are **separable, not correlated** (see Part C). |

Method discipline across the batch: every analysis reused already-locked
methodology (citalopram section 5.B, the recovery-phase axis MD, the longrun RHR
model, the R14 machinery), reproduced its inherited numbers as a correctness gate,
stayed single-pool + descriptive, and passed the publication audit before each
push.

---

## Part B - the Wiggers-guide reconciliation

Prompted by the participant re-reading the guide, three read-only sweeps mapped
every heart-rate / HRV / night-stress / sleep / intraday claim to what the project
has already tested, and a fourth thorough re-read extracted the guide statements
comprehensively. Headline reconciliation (single-pool verdicts):

- **Bidirectional night RHR = PEM** (Wiggers): tested (HA06b / H01), **NOT-SUPPORTED**
  single-pool; the lowered-RHR (swing) direction is empirically present later but
  non-discriminative; R30 shows the level rise is confounder-dominated.
- **HRV drop (day-over-day, multi-day, slow-decline-predicts)**: tested via the
  overnight-stress HRV proxy - HA07c / HA08c **NOT-SUPPORTED**, the slow-decline
  *predictive* claim does not hold single-pool; only **HA07d (variability)** is
  SUPPORTED, Tier C.
- **Night orange stress**: the *level* (HA07c) is NOT-SUPPORTED; the *variability*
  (HA07d) is the operative measure.
- **HRV rises at illness onset**: we found the **opposite** at the one COVID-onset
  window (stress up / HRV down); single inseparable event.
- **"Return to blue" / stuck sympathetic**: tested (HA-C4 rejected daily; HA-C4c
  bout-level **PARTIAL** - weak but real).
- **Parasympathetic swing**: components present (HA10 morning-BB, HA11 U-dip); the
  full intraday composite not modelled; HRV-spike device-blocked.
- **Push-crash / cardiac cost**: ran this session, **Cannot resolve** (slightly
  negative).

**The re-read's structural finding**: the catalog is overwhelmingly PEM-framed.
Of ~40 hypotheses it labeled ~26 PEM, 4 both (A2, C4, C4b, G3), 1 POTS (G4), plus
acute-illness (B5) and data-quality (I-block). It found **17 gaps** - the largest
being an entire **missing POTS / orthostatic family**: Wiggers' orthostatic-stress
chapter, the standing / NASA-lean HR test, the U-dip workflow, and the electrolyte
/ salt / compression interventions (including a *testable* one: "water + salt +
compression significantly reduce daytime stress scores") are unrepresented. PEM
gaps too: the sleep-onset-latency precursor, the HR x HRV pattern-table rows 2/3/4,
night HR variability, a second step->HRV dose anchor.

---

## Part C - the PEM/POTS reframing (the new synthesis)

The guide distinguishes two watch-visible mechanisms - **PEM** (load / recovery)
and **POTS / orthostatic** (blood volume / positional) - and treats POTS largely
descriptively, managing it as symptoms wax and wane. We operationalised the split as
**two descriptive watch signals** (methodology:
[`methodology/pem_pots_mechanism_framing.md`](methodology/pem_pots_mechanism_framing.md))
- a within-day **U-dip signal** and an overnight **stress-load signal** - and ran a
descriptive separability analysis
([`analyses/descriptive/pem_pots_separability/findings.md`](analyses/descriptive/pem_pots_separability/findings.md)).

**Label floor (important, corrected 2026-07-07).** These are **signals, not
markers/detectors**: `PEM` / `POTS` name Wiggers' two *management threads* (pacing;
electrolytes), and management is attributed to her, not claimed by us. An early
"POTS-marker / axis" framing over-reached three ways and was walked back - "axis" (peer
review), "POTS marker" (external PubMed review
[`literature/reviews/pots_operationalisation_wearable_review.md`](literature/reviews/pots_operationalisation_wearable_review.md):
no orthostatic precedent, off-polarity, posture-blind), and even "management-relevant"
(participant: it presumes a mechanism our own U-dip null contradicts). The
separability result is unaffected; only the label is capped. See methodology MD
section 1.3 for the full provenance.

Four findings:

1. **Largely distinct** - the POTS and PEM markers are only weakly correlated
   (r = +0.09, 95% CI [0.03, 0.15], sharing under 1% of variance); the CI excludes
   zero, so they are weakly *positive*, not independent, but signature-days are
   mostly one mechanism or the other (169 POTS-only, 219 PEM-only, 77 both). Warrant
   for reading both signals separately.
2. **Suggestively time-varying (era-confounded)** - the POTS U-dip signature is
   stronger in the pre-citalopram pacing-habit phase (4b, 27% of days) than the
   citalopram phase (5, 18.7%). But the 4b/5 boundary IS citalopram onset, so this
   is the retired era-split in another guise (R19 discipline): a suggestive
   descriptive pattern, not a clean time-trend.
3. **PEM days track lower felt-state; POTS days do not** - PEM-only 4.15 vs neither
   4.48 is real (MWU p < 0.0001, d = -0.40) and survives a crash-drop check;
   POTS-only 4.57 is a genuine null (p = 0.19). (The earlier "both together = lowest"
   was **dropped on review** as a crash artefact - the "both" group is 24.7%
   crash-days, and crashes are defined partly on low felt-state.)
4. **Notes can't corroborate POTS** (2 / 246 signature-days carry any
   orthostatic-symptom keyword) - a prospective-logging gap.

All four are descriptive, n=1, wide error, proxy markers, small felt-state
magnitudes. Findings 1-3 are the **post-review** wording - they went through the
independent fresh-context review (MAJOR-REVISIONS-NEEDED, folded), which is why the
separability claim is softened from "not correlated" and the "both = lowest" beat is
gone. See [`reviews/pem-pots-reframing-2026-07-07.md`](reviews/pem-pots-reframing-2026-07-07.md).

---

## Part D - infrastructure landed

- **Clean guide source**: `literature/wiggers_pacing_handleiding.txt` (pdftotext
  -raw -enc UTF-8, 3205 lines, gitignored/local like the PDF); the flawed
  two-column extraction archived alongside as
  `wiggers_pacing_handleiding.layout-2col.archived.txt`. Verbatim quotes going
  forward use the clean file; the catalog's existing verification-log line numbers
  map to the archived two-column version.
- **Site chart JSONs** (R1) on disk in the `wiggers_research_story` checkout;
  register annotations for R4/R23/R35/R32a/R18/R20/R19/R30/R1/R13 sit there for the
  participant to commit from the site side.

---

## Structural additions that flow from this note

1. **Catalog** (`wiggers_testable_hypotheses.md`): add `mechanism` (PEM/POTS/both)
   tags, the verbatim excerpts + result nuance on the existing entries, a POTS /
   orthostatic descriptive cluster, and the new descriptive items. Reviewer-mode
   artefact, drafted under authorization, fresh-session reviewed.
2. **Queued work** (`methodology/queued_work.md`): the 5 new descriptive items
   (pacing-trend, sleep-trajectory-per-phase, wake-later-around-crashes,
   night-typology, graph-replication), the POTS-family write-up, and the
   prospective orthostatic-symptom logging.
3. **Website card**: a PEM/POTS reframing export for the site team (guide
   references + which POTS signals we found and when + the separability read).

---

## The conclusions audit (DONE 2026-07-07)

Per [CONVENTIONS section 1.2](CONVENTIONS.md), an independent **fresh-context**
review cold-read this note, the methodology MD, the separability findings + script,
the catalog edits, and the website card, via the 4-layer checklist -> report at
[`reviews/pem-pots-reframing-2026-07-07.md`](reviews/pem-pots-reframing-2026-07-07.md).
The reviewer was an isolated-context subagent (no exposure to the drafting session);
this is a reasonable equivalent of a fresh session, but not a user-initiated one, so
a final user-initiated confirmation remains optional.

**Verdict: MAJOR-REVISIONS-NEEDED, now folded.** The numbers reproduced exactly, but
three public claims overstated and were corrected: (1) "separable, not correlated" ->
"weakly correlated but largely distinct" (the r CI excludes zero); (2) "both
mechanisms = lowest felt-state" **dropped** (crash-driven / circular per the §3.4
crash-drop check that was missing); (3) the "POTS recedes over time" timing read now
carries the citalopram-onset era-confound inline (not just in a footer). Minors
folded: MWU tests added for the felt-state contrasts, and "axis / family" softened
given the thin u_dip substrate (43% zeros). The reviewer could not verify HA11's
era-handling (relied on for the timing read) - handled by framing the timing read as
era-confounded descriptive variation throughout.

---

## Cross-references

- Analyses: `analyses/descriptive/operationalisation_support/driver_netting_overlay/`
  (R20), `analyses/descriptive/recovery_phase_signal_backdrop/` (R19),
  `analyses/descriptive/recovery_phase_confounder_bound/` (R30),
  `analyses/descriptive/crash_leadup_curves/` (R1),
  `analyses/descriptive/pem_pots_separability/`.
- Methodology: `methodology/pem_pots_mechanism_framing.md`,
  `methodology/hypothesis_retest_triage.md` (R18).
- Guide: `literature/wiggers_pacing_handleiding.txt`; catalog
  `wiggers_testable_hypotheses.md`.
- External register: `wiggers_research_story/site/docs/research-requests.md`.

---

*End of research note (draft).*
