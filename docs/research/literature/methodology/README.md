# Methodology standards and references

This subfolder holds **research-methodology source documents** —
reporting standards, statistical references, and SCED-community
literature — that the project's research conventions inherit from.

These are distinct from the substantive subject-matter literature
in [`..`](..) (PEM mechanism, pacing literature, HRV norms, etc.).
The files here document *how* we report, not *what* we are
studying.

The review checklist in [`../../reviews/`](../../reviews/) and the
conventions in [`../../CONVENTIONS.md`](../../CONVENTIONS.md) cite
these files at the layer headers so reports are defensible
independent of project-internal documentation.

## Index

| file | what it is | how we use it |
|---|---|---|
| [tate_2016_scribe_single_case_reporting.pdf](tate_2016_scribe_single_case_reporting.pdf) (NOT YET DOWNLOADED — cite via [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/)) | SCRIBE 2016 — Single-Case Reporting Guideline In BEhavioural interventions. Tate, Perdices, Rosenkoetter et al. 26-item checklist for SCED reports. | Layer 1 of the review checklist inherits items 3-5, 14, 18, 22-24 (pre-specification, measures with defined properties, analysis plan, limitations, applicability). SCRIBE explicitly does not cover non-intervention work; we adapt structure, not scope. |
| [shamseer_2015_cent_consort_nof1.pdf](shamseer_2015_cent_consort_nof1.pdf) + [shamseer_2015_cent_consort_nof1_bmj.pdf](shamseer_2015_cent_consort_nof1_bmj.pdf) | CENT 2015 — CONSORT Extension for N-of-1 Trials. Shamseer, Sampson, Bukutu et al. Extends 14 of the 25 CONSORT items + carryover/washout/ordering. | Layer 3 inherits the explicit treatment of carryover and ordering effects. CENT assumes randomised crossover; we do not randomise, but lag-carryover is structurally identical and the framing transfers. |
| [vonelm_2007_strobe_observational_checklist.pdf](vonelm_2007_strobe_observational_checklist.pdf) | STROBE 2007 — Strengthening the Reporting of Observational Studies in Epidemiology. 22-item checklist for cohort / case-control / cross-sectional. | Layer 1 inherits items 6 (participants), 12 (statistical methods including confounder handling and sensitivity analyses), 13 (descriptive data). STROBE assumes population-level; we adapt the items that survive at n=1. |
| [daza_2018_self_tracked_n_of_1_counterfactual.pdf](daza_2018_self_tracked_n_of_1_counterfactual.pdf) | Daza 2018, Methods of Information in Medicine — Causal Analysis of Self-tracked Time Series Data Using a Counterfactual Framework for N-of-1 Trials. | Layer 2 inherits the counterfactual framing, the stationarity assumption check, the calendar-time vs subject-time distinction, and the explicit treatment of carryover/onset/decay in self-tracked observational time series. The most directly relevant published framework for the shape of this corpus. |
| [natesan_2023_nof1_evidence_reporting_systematic_review.pdf](natesan_2023_nof1_evidence_reporting_systematic_review.pdf) | Natesan Batley et al. 2023, Translational Psychiatry — Evidence and reporting standards in N-of-1 medical studies: a systematic review. n=115 articles audited against WWC SCED standards. | Layer 3 inherits the headline finding: **83.8% of n-of-1 medical studies ignored autocorrelation; 65.8% failed distributional assumptions; only 4/115 (3.48%) met all WWC SCED evidence standards**. This is the field-wide failure mode our checklist must specifically catch. |
| [wwc_2022_standards_handbook_v5_0.pdf](wwc_2022_standards_handbook_v5_0.pdf) | What Works Clearinghouse Standards Handbook v5.0 (2022). U.S. Department of Education. Standards for evaluating single-case research evidence. | Layer 3 inherits the SCED-evidence-level framing referenced by Natesan Batley 2023. We don't use WWC's intervention-effect framing directly (we have no intervention phases), but the data-analytic standards transfer. |
| [carlstein_1986_subseries_variance.pdf](carlstein_1986_subseries_variance.pdf) | Carlstein 1986 — block bootstrap foundational paper. | Layer 3 — referenced from `../../methodology/permutation_null_block_length.md` for block length under serial dependence. |
| [kunsch_1989_jackknife_bootstrap_stationary.pdf](kunsch_1989_jackknife_bootstrap_stationary.pdf) | Künsch 1989 — moving-block bootstrap for stationary observations. | Layer 3 — referenced from `../../methodology/permutation_null_block_length.md` for the stationary-bootstrap variant. |
| [chung_romano_2013_permutation_tests.pdf](chung_romano_2013_permutation_tests.pdf) | Chung & Romano 2013 — exchangeability conditions for valid permutation tests. | Layer 3 — referenced from `../../methodology/permutation_null_block_length.md` for permutation-test validity under temporal dependence. |

## Why standards we did not adopt are still cited

We cite externally even where the standard does not cleanly map (e.g.
SCRIBE's prototypical-design taxonomy, CENT's randomisation items)
because the *structural reasoning* of those standards informs how we
adapted Layer 1-3. A reviewer evaluating one of our reports should be
able to see what we inherited, what we did not, and why — independent
of project-internal docs.

## Gaps

- **No checklist exists** for observational n=1 time-series with
  continuous biometric channels. SCRIBE is intervention-only; CENT is
  randomised-crossover; STROBE is population-level; WWC is SCED
  intervention-effect. The closest published framework is Daza 2018,
  which is a framework rather than a checklist.
- **QuantifyMe** ([PMC5948910](https://pmc.ncbi.nlm.nih.gov/articles/PMC5948910/),
  Taylor et al. 2018, *Sensors*) is precedent for an automated SCED
  platform but not a reporting standard; not downloaded.
- **Personal Science** community norms (Wolf et al., Meth Inf Med
  2017 focus theme) are cited via Wikipedia / the Personal Science
  Manifesto rather than a paper PDF; not downloaded.

If a SCRIBE-equivalent for observational n=1 time-series emerges, add
it here and update the layer headers in [`../../reviews/README.md`](../../reviews/README.md)
and [`../../CONVENTIONS.md`](../../CONVENTIONS.md).
