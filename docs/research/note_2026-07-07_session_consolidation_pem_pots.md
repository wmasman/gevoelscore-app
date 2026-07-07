# Research note 2026-07-07: session consolidation + the PEM/POTS reframing

## Authorship

- **Drafted**: 2026-07-07 by Claude (Opus 4.8), producer-mode, under authorization
  from the participant-researcher (repo owner).
- **Status**: **DRAFT - NOT LOCKED.** A consolidation / session-log note. The
  synthesis claims below (esp. the PEM/POTS separability reframing) are producer
  drafts pending a **fresh-session** peer review per
  [CONVENTIONS section 1.2](CONVENTIONS.md) before they are relied on downstream
  (website, catalog lock).

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
descriptively, noting it waxes and wanes as symptoms are managed. We operationalised
the split with proxy markers (methodology:
[`methodology/pem_pots_mechanism_framing.md`](methodology/pem_pots_mechanism_framing.md),
draft) - POTS-signature = within-day stress **U-dip**; PEM-signature = overnight
stress load - and ran a descriptive separability analysis
([`analyses/descriptive/pem_pots_separability/findings.md`](analyses/descriptive/pem_pots_separability/findings.md)).
Four findings:

1. **Separable, not correlated** - r(POTS, PEM markers) = +0.09; signature-days are
   mostly one mechanism or the other (169 POTS-only, 219 PEM-only, 77 both). Warrant
   for a two-axis catalog, not a taxonomy preference.
2. **Time-varying** - the POTS U-dip signature is stronger in the pre-citalopram
   pacing-habit era (4b, 27% of days) and recedes into the citalopram era (5,
   18.7%), matching HA11 and "comes and goes as symptoms change."
3. **POTS days are NOT lower in felt-state** (POTS-only 4.57 ~ neither 4.48); the
   **PEM** marker tracks lower gevoelscore (4.15), lowest when both co-occur (4.03).
   The orthostatic pattern is "dysregulated but not necessarily feeling bad"; the
   PEM load is what coincides with feeling worse.
4. **Notes can't corroborate POTS** (2 / 246 signature-days carry any
   orthostatic-symptom keyword) - a prospective-logging gap.

All four are descriptive, n=1, wide error, proxy markers, small felt-state
magnitudes - these are the claims the fresh-session review must push hardest on
before they go public.

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

## What needs the fresh-session review (the conclusions audit)

Per [CONVENTIONS section 1.2](CONVENTIONS.md), a **different session** cold-reads:
this note, the methodology MD, the separability findings, and (once drafted) the
catalog edits + website card, via the 4-layer checklist in `reviews/`. Push hardest
on: the separability headline ("PEM and POTS carry felt-state differently"), R30's
"confounder-dominated," R1's "departure at onset," and the u_dip-as-POTS-proxy
validity. R20 / R19 are lower-risk (overlays on already-reviewed locked verdicts /
descriptive backdrop).

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
