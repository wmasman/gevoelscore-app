# Pending: fetch + verify statistical-methodology literature

*Created 2026-06-13 to track unverified citations stripped from the three methodology MDs (`lc_era_temporal_segmentation.md`, `permutation_null_block_length.md`, `train_validate_split_fate.md`). Self-contained brief for a future agent. Underscore-prefixed filename signals "auxiliary, not active methodology".*

---

## TL;DR for the executing agent

The three methodology MDs above each have a `## Citation status` block stating that the canonical references have **not** been read or verified, and the literature row of the four-input reasoning has been honestly downgraded to "deferred". The methodological reasoning stands on its own; what is missing is the literature row.

Your job: locate, verify, and save the candidate papers below; then update the methodology MDs with verified citations and a short statement of what each paper materially adds. **Do not modify the methodological substance of the three MDs** — only the citation status block and the literature subsection.

You can run this work in parallel for the three MDs; the papers list is partly shared between them.

---

## Discipline reminders (read before starting)

1. **Cite only where the reference materially supports the choice.** "X used 7-day blocks" is not enough; "X proves consistency of stationary bootstrap under α-mixing with E[L] = O(n^(1/3))" is. If a candidate paper turns out to support the choice only weakly or only by inference, do **not** add it as a citation; note this in the verification log instead.
2. **Do not cite from secondary sources** (blog posts, lecture notes, Wikipedia, ChatGPT/Claude summaries). The citation chain must end at the primary source you have read.
3. **Do not invent claims that the paper does not make.** If you cannot find the supporting sentence in the paper, do not cite it. Add the paper to the "verified but not load-bearing" list.
4. **If the canonical paper is unobtainable**, look for the equivalent claim in a textbook the project can buy or that is open-access (Lahiri 2003 is the textbook spine for resampling under dependence; Politis-Romano-Wolf 1999 is the subsampling spine). Document the substitution; do not silently swap a textbook chapter for the original paper.
5. **Do not change methodological substance.** The proposed decisions in the three MDs (stationary bootstrap E[L]=7; no default sub-segmentation of Stratum 4; train/validate split fate per MD 3) are owned by the user. Your job is to ground the literature row of each MD, not to second-guess the choice.
6. **No personal-data leakage**: the methodology MDs themselves do not contain personal data, so editing them is safe. The literature PDFs you download contain no personal data and may be saved into `docs/research/literature/methodology/` (a new subfolder).

---

## Where to save acquired PDFs

Create the subfolder if it does not exist:

```
docs/research/literature/methodology/
```

Filename convention follows the existing literature folder (`<lastname>_<year>_<topic>.pdf`, all lowercase, underscores not spaces). Examples:

- `politis_romano_1994_stationary_bootstrap.pdf`
- `patton_politis_white_2009_automatic_block_length_correction.pdf`
- `hall_horowitz_jing_1995_blocking_rules.pdf`
- `carlstein_1986_subseries_variance.pdf`
- `kunsch_1989_jackknife_bootstrap_stationary.pdf`
- `chung_romano_2013_permutation_tests.pdf`
- `kratochwill_2013_sced_standards.pdf`
- `bergmeir_benitez_2012_cv_time_series.pdf`

If the paper is a textbook (Lahiri 2003, Politis-Romano-Wolf 1999, Saltelli 2008), include only the relevant chapter PDF, not the whole book; filename: `<lastname>_<year>_<chapter_topic>.pdf`.

Add a row to [`docs/research/literature/README.md`](../literature/README.md) (if it does not exist, create the section "Statistical methodology") with one line per paper: title, authors, year, journal, brief topic.

---

## Where to look for each paper (in order of likelihood)

1. **Author's homepage / institutional repository** — the most common open-access source for statistical methodology papers.
2. **arXiv** — for papers ≥ 1990s; many methodology papers were posted there as preprints.
3. **JSTOR** (annals, JASA, biometrika historical issues) — usually requires institutional access; check if your environment has it.
4. **Project Euclid** — open-access for Annals of Statistics (sometimes), Annals of Probability, etc.
5. **Google Scholar** — final fallback; click through to the most authoritative open-access link.
6. **Library proxy** — if user has institutional access, mention this and ask.

Do **not** download from sci-hub or other piracy sources; if a paper requires institutional access and is not available open-access, flag it in the verification log and proceed without that citation.

---

## How to integrate a verified citation back into the methodology MD

For each verified paper, edit the relevant MD's `## Citation status` block and the `### Literature where it materially supports the choice` subsection:

### Step 1: in the Citation status block

Move the paper from "deferred" to "verified" with a one-line summary:

```markdown
## Citation status

**Verified (2026-MM-DD)**:
- Politis & Romano (1994) — read; supports stationary bootstrap as primary; cited in § 2.2 below.

**Deferred / not yet acquired**:
- Carlstein (1986) — see [`_pending_literature_fetch.md`](_pending_literature_fetch.md)
```

### Step 2: in the literature subsection

Replace the "Deferred" placeholder text with the actual citation table. Use this exact column structure (matches the style used elsewhere in the methodology folder):

```markdown
| citation | what it materially adds | how we apply it |
|---|---|---|
| Politis & Romano (1994), *The stationary bootstrap*, **Journal of the American Statistical Association** 89(428): 1303-1313 | [Replace with what you actually verified the paper says, NOT what the candidate-claim column below says] | [Replace with the specific use in our MD] |
```

**Do not copy the candidate-claim column verbatim from the table below**. The candidate-claim is what we suspect the paper adds; you must replace it with what you have read in the paper.

### Step 3: leave a verification log entry

At the bottom of this file (`_pending_literature_fetch.md`), add a row to the verification log:

```markdown
| paper | verified date | section/page checked | claim verified | citation added to |
|---|---|---|---|---|
| Politis & Romano 1994 | 2026-MM-DD | § 3 p.1308 | "stationary bootstrap consistency under α-mixing" — verified | permutation_null_block_length.md § 2 |
```

---

## Candidate paper list

Below: for each candidate paper, the citation as best-guessed from training-data memory, the MD that wants to cite it, the candidate-claim (what we suspect it adds), and where to look. **The citations may be inexact; verify all metadata against the actual paper.**

### For `permutation_null_block_length.md`

#### P1. Politis & Romano (1994), *The stationary bootstrap*

- **Candidate citation**: D.N. Politis & J.P. Romano, "The stationary bootstrap", **Journal of the American Statistical Association** 89(428): 1303-1313 (December 1994).
- **Candidate claim**: introduces the stationary bootstrap with random block lengths drawn from a geometric distribution; proves consistency under α-mixing conditions; the resampled series is itself stationary by construction.
- **What to verify**: § 2 (the construction), § 3 (consistency theorem under α-mixing), and that the construction does NOT require the original series to be stationary at the boundary (the key advantage over moving-block).
- **Where to look**: D.N. Politis homepage (UC San Diego); JSTOR; Google Scholar.
- **MD section using it**: `permutation_null_block_length.md` § 4.1 (Best-practices standards), § 4.2 (Literature).

#### P2. Patton, Politis & White (2009), Correction note

- **Candidate citation**: A. Patton, D.N. Politis, H. White, "Correction to 'Automatic block-length selection for the dependent bootstrap' by D. Politis and H. White", **Econometric Reviews** 28(4): 372-375 (2009).
- **Candidate claim**: corrected formula for automatic block-length selection; without the correction, the original Politis-White (2004) procedure overstates the optimal block length.
- **What to verify**: the corrected formula vs the original; the dependence-on-spectral-density-estimator detail; whether implementations in standard packages use the corrected version.
- **Where to look**: A. Patton homepage (Duke / UNC); H. White's homepage / archive; Econometric Reviews journal site.
- **MD section using it**: `permutation_null_block_length.md` § 4.1, § 4.2; this is the citation behind "data-driven confirmation companion".

#### P3. Hall, Horowitz & Jing (1995), *On blocking rules for the bootstrap with dependent data*

- **Candidate citation**: P. Hall, J.L. Horowitz, B.-Y. Jing, "On blocking rules for the bootstrap with dependent data", **Biometrika** 82(3): 561-574 (September 1995).
- **Candidate claim**: derives the n^(1/k) family of optimal block-length rules; k=3 for bias estimation, k=4 for variance estimation, k=5 for distribution estimation.
- **What to verify**: the formula for the optimal block length; the regularity conditions assumed; whether the rule applies to fixed-block or generalises to stationary.
- **Where to look**: Biometrika archive (Oxford Academic); J.L. Horowitz homepage; Google Scholar.
- **MD section using it**: `permutation_null_block_length.md` § 4.2; sanity-check for our E[L] = 7 default.

#### P4. Carlstein (1986), *Subseries variance estimation*

- **Candidate citation**: E. Carlstein, "The use of subseries values for estimating the variance of a general statistic from a stationary sequence", **Annals of Statistics** 14(3): 1171-1179 (September 1986).
- **Candidate claim**: original derivation of L ∝ n^(1/3) for variance estimation under stationarity.
- **What to verify**: the derivation; the stationarity assumption; the explicit form of the n^(1/3) result.
- **Where to look**: Project Euclid (Annals of Statistics open-access for older issues); JSTOR.
- **MD section using it**: `permutation_null_block_length.md` § 4.2; cited as background for the n^(1/k) range.

#### P5. Künsch (1989), *Moving-block bootstrap*

- **Candidate citation**: H.R. Künsch, "The jackknife and the bootstrap for general stationary observations", **Annals of Statistics** 17(3): 1217-1241 (September 1989).
- **Candidate claim**: introduces the moving-block bootstrap; establishes consistency under stationarity.
- **What to verify**: the construction; the stationarity assumption; what fails under non-stationarity.
- **Where to look**: Project Euclid; JSTOR.
- **MD section using it**: `permutation_null_block_length.md` § Alternatives considered (option (a), rejected).

#### P6. Chung & Romano (2013), *Permutation tests under dependence*

- **Candidate citation**: E. Chung & J.P. Romano, "Exact and asymptotically robust permutation tests", **Annals of Statistics** 41(2): 484-507 (2013).
- **Candidate claim**: asymptotic validity of permutation tests under dependence when blocks are chosen consistently with the ACF structure.
- **What to verify**: the conditions under which permutation-with-blocks remains asymptotically valid; specifically whether α-mixing conditions are required.
- **Where to look**: Project Euclid (Annals of Statistics); J.P. Romano homepage (Stanford).
- **MD section using it**: `permutation_null_block_length.md` § 4.1 (justifies block-permutation null).

#### P7. Lahiri (2003), *Resampling Methods for Dependent Data*

- **Candidate citation**: S.N. Lahiri, *Resampling Methods for Dependent Data*, Springer Series in Statistics, Springer, 2003.
- **Candidate claim**: textbook treatment of all block-bootstrap variants, including stationary, moving-block, circular, tapered. Spine reference for the area.
- **What to verify**: chapter on stationary bootstrap (likely Ch. 2 or 3); chapter on block-length selection (likely Ch. 7); chapter on permutation under dependence if covered.
- **Where to look**: Springer Link (institutional access common); chapter PDFs may be open if user has access.
- **MD section using it**: `permutation_null_block_length.md` general background; cite if a specific claim from the textbook is load-bearing.

### For `lc_era_temporal_segmentation.md`

#### S1. Kratochwill et al. (2013), SCED standards

- **Candidate citation**: T.R. Kratochwill, J.H. Hitchcock, R.H. Horner, J.R. Levin, S.L. Odom, D.M. Rindskopf, W.R. Shadish, "Single-Case Intervention Research Design Standards", **Remedial and Special Education** 34(1): 26-38 (2013).
- **Candidate claim**: three-demonstrations-of-effect standard for single-case research; explicit guidance that demonstrations across **time** are acceptable in observational designs.
- **What to verify**: the three-demonstrations requirement; the language on time-block replication; any explicit caveat about observational vs interventional contexts.
- **Where to look**: Sage Journals (Remedial and Special Education); T.R. Kratochwill homepage (Wisconsin); What Works Clearinghouse standards document (2017 revision) for the codified version.
- **MD section using it**: `lc_era_temporal_segmentation.md` § 5.1, § 5.2; supports M3 (sensitivity replication overlay).

#### S2. Bergmeir & Benítez (2012), Time-series CV

- **Candidate citation**: C. Bergmeir & J.M. Benítez, "On the use of cross-validation for time series predictor evaluation", **Information Sciences** 191: 192-213 (2012).
- **Candidate claim**: shows that random K-fold CV inflates performance for autocorrelated time series; time-block CV is preferred for honest evaluation.
- **What to verify**: the simulation results; the recommended block-CV variant; whether the conclusions apply to inference (hypothesis testing) as well as prediction.
- **Where to look**: Elsevier (Information Sciences); C. Bergmeir homepage (Monash); arXiv.
- **MD section using it**: `lc_era_temporal_segmentation.md` § 5.1; secondary justification for contiguous-calendar-block sensitivity if M3 is invoked.

#### S3. Saltelli et al. (2008), Global Sensitivity Analysis textbook

- **Candidate citation**: A. Saltelli, M. Ratto, T. Andres, F. Campolongo, J. Cariboni, D. Gatelli, M. Saisana, S. Tarantola, *Global Sensitivity Analysis: The Primer*, Wiley, 2008.
- **Candidate claim**: sensitivity analysis discipline: vary one assumption at a time, report distributions, do not collapse to passed/failed verdict.
- **What to verify**: the canonical "one-at-a-time" framing; the distinction between local and global sensitivity; whether the textbook addresses time-block sensitivity specifically (probably not — but the general principle applies).
- **Where to look**: Wiley Online; library copies common.
- **MD section using it**: `lc_era_temporal_segmentation.md` § 5.1 (sensitivity-analysis framing).

#### S4. What Works Clearinghouse SCED standards (2017)

- **Candidate citation**: What Works Clearinghouse, *Standards Handbook, Version 4.1*, Institute of Education Sciences, U.S. Department of Education, 2017 (or latest version). Standards for single-case research are codified in this handbook.
- **Candidate claim**: codified standards for evaluating single-case research evidence quality.
- **What to verify**: section on single-case design (likely Ch. 4 or 5); the threshold for "Meets standards" vs "Meets standards with reservations" vs "Does not meet standards".
- **Where to look**: IES website (open-access PDF); ies.ed.gov/ncee/wwc.
- **MD section using it**: `lc_era_temporal_segmentation.md` § 5.1; codified version of Kratochwill et al.

### For `train_validate_split_fate.md` (not yet written; this MD will be drafted with the same citation discipline)

#### T1. Shamseer et al. (2015), CONSORT extension for n-of-1 trials

- **Candidate citation**: L. Shamseer, M. Sampson, C. Bukutu, C.H. Schmid, J. Nikles, R. Tate, B.C. Johnston, et al., "CONSORT extension for reporting N-of-1 trials (CENT) 2015: Explanation and elaboration", **Journal of Clinical Epidemiology** 76: 18-46 (2016) [also: BMJ 2015].
- **Candidate claim**: reporting standards for n-of-1 trials; explicit guidance on pre-registration, randomisation, replication; relevance to observational longitudinal single-subject work is partial (the n-of-1 trial is interventional).
- **What to verify**: the CONSORT-extension items; the language on pre-registration and held-out validation; the applicability to observational single-subject designs (likely indirect).
- **Where to look**: BMJ / J Clinical Epidemiology; CONSORT website (consort-statement.org).
- **MD section using it**: `train_validate_split_fate.md` § Best-practices standards; cited for pre-registration discipline.

#### T2. Lillie et al. (2011), n-of-1 trials methodology

- **Candidate citation**: E.O. Lillie, B. Patay, J. Diamant, B. Issell, E.J. Topol, N.J. Schork, "The n-of-1 clinical trial: the ultimate strategy for individualizing medicine?", **Personalized Medicine** 8(2): 161-173 (2011).
- **Candidate claim**: framing of n-of-1 trials and within-subject inference; relevance to observational longitudinal work via the within-subject inference framework.
- **What to verify**: the within-subject inference framing; explicit treatment of replication-across-time; any discussion of held-out validation.
- **Where to look**: Future Medicine; PubMed (PMC may have open-access).
- **MD section using it**: `train_validate_split_fate.md` (if MD 3 reasons about within-subject inference).

---

## Notes on candidate-paper quality before you fetch

- **Verified-by-many vs verified-by-author-claim**: P1 (Politis-Romano 1994) is among the most-cited statistical methodology papers; the construction is real and matches my training-data memory closely. The risk of mis-citation on the **construction** is low; the risk on **specific section numbers or quoted phrases** is higher.
- **Candidate citations with high mis-cite risk**: P2 (Patton-Politis-White 2009 — exact title, page numbers); S4 (WWC handbook — version number drifts); T1 (Shamseer et al. — primary publication venue may be BMJ or J Clin Epidemiol; cross-published).
- **Strongest candidates if you only have time for three**: P1 + P2 + S1. Together they cover stationary bootstrap (primary methodological choice), block-length selection (the empirical-check step), and SCED replication (the framing for sensitivity overlay).

---

## What to do if a paper is unobtainable

1. Note in the verification log: paper attempted, source(s) tried, why unobtainable (paywall, lost archive, etc.).
2. Look for a high-quality secondary source that IS obtainable (textbook chapter, review article) that explicitly cites the original with a quoted claim. Then cite the secondary source with the original as the chain reference (e.g. "Politis & Romano (1994), as cited in Lahiri (2003) Ch. 3").
3. If no defensible chain exists, drop the citation entirely. The methodological reasoning in the MD does not depend on it.
4. Do not cite the paper as if you have read it when you have not.

---

## Verification log

(Empty. Fill in as you verify.)

| paper | verified date | section/page checked | claim verified | citation added to | notes |
|---|---|---|---|---|---|

---

## Fetch log (2026-06-13)

**Distinct from the verification log above.** Fetch log = "PDF acquired locally". Verification log = "paper read, specific claim found, citation added to MD". The four PDFs below are acquired but **not** yet read; no citations have been added to any methodology MD.

| paper | fetch date | route used | local path | notes |
|---|---|---|---|---|
| P6 Chung & Romano 2013 | 2026-06-13 | arXiv 1304.5939 (Green OA per Unpaywall) | [`../literature/methodology/chung_romano_2013_permutation_tests.pdf`](../literature/methodology/chung_romano_2013_permutation_tests.pdf) | arXiv preprint version — final Annals of Statistics version may differ in section numbering. Verify quotes against the AoS final version before citing if section/page references matter. |
| T1 Shamseer et al. 2015 | 2026-06-13 | Europe PMC (PMC5058423) — BMJ direct curl was anti-bot-blocked | [`../literature/methodology/shamseer_2015_cent_consort_nof1.pdf`](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf) | This is the BMJ Statement only. The longer J Clin Epidemiol Explanation & Elaboration (Shamseer et al. 2016, *J Clin Epidemiol* 76:18-46, DOI 10.1016/j.jclinepi.2015.05.004) is also OA per Unpaywall but not yet fetched. |
| S4 WWC Standards Handbook v5.0 | 2026-06-13 | IES.ed.gov direct (open-access US government doc) | [`../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf`](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf) | August 2022, revised December 2022. SCED standards are integrated into the main handbook, not separately published, per IES landing page. |
| S4 WWC Standards Handbook v4.1 | 2026-06-13 | IES.ed.gov direct | [`../literature/methodology/wwc_2020_standards_handbook_v4_1.pdf`](../literature/methodology/wwc_2020_standards_handbook_v4_1.pdf) | The version this file actually cites by name in § S4. Kept alongside v5.0 in case the brief's claim references v4.1-specific section numbers; **delete one of the two after verification**. |

### Not fetched

| paper | reason | OA-database evidence | recommended next step |
|---|---|---|---|
| P1 Politis & Romano 1994 (JASA) | Closed, no preprint | Unpaywall `is_oa: false`, 0 OA locations | Author reprint request (D.N. Politis, math.ucsd.edu) OR Lahiri 2003 Ch. 2-3 substitute |
| P2 Patton, Politis & White 2009 (Econometric Reviews) | Closed, no preprint | Unpaywall `is_oa: false`, 0 OA locations | Author reprint request (A. Patton, Duke) OR cite via Politis-Romano-Wolf 1999 Ch. for the corrected formula |
| P3 Hall, Horowitz & Jing 1995 (Biometrika) | Closed, no preprint | Unpaywall `is_oa: false`, 0 OA locations | Author reprint request (J.L. Horowitz, Northwestern) OR cite via Lahiri 2003 textbook |
| P4 Carlstein 1986 (Annals of Statistics) | Project Euclid Imperva Incapsula anti-bot blocks `curl` even though paper is Bronze-OA | Unpaywall `is_oa: true`, only OA URL is the blocked Project Euclid one | **Download in a browser**: [Project Euclid direct PDF](https://projecteuclid.org/journals/annals-of-statistics/volume-14/issue-3/The-Use-of-Subseries-Values-for-Estimating-the-Variance-of/10.1214/aos/1176350057.pdf) |
| P5 Künsch 1989 (Annals of Statistics) | Same as P4 — Project Euclid Incapsula | Unpaywall `is_oa: true`, blocked OA URL only | **Download in a browser**: [Project Euclid direct PDF](https://projecteuclid.org/journals/annals-of-statistics/volume-17/issue-3/The-Jackknife-and-the-Bootstrap-for-General-Stationary-Observations/10.1214/aos/1176347265.pdf) |
| P7 Lahiri 2003 *Resampling Methods for Dependent Data* (Springer) | Textbook — per this file's own rule, only specific chapter PDF, not whole book | n/a — chapter-level fetch is not automatable | Manual: Springer Link via institutional access; the relevant chapter is Ch. 2 (block bootstrap) or Ch. 3 (stationary bootstrap) |
| S1 Kratochwill et al. 2013 (Remedial Special Education) | Closed, no preprint | Unpaywall `is_oa: false`, 0 OA locations | The WWC Standards Handbook v4.1 (S4, fetched) is the codified version of the same SCED-standards content. Likely substitute. |
| S2 Bergmeir & Benítez 2012 (Information Sciences) | Closed, no preprint | Unpaywall + Semantic Scholar both `CLOSED`, 0 OA locations | Author reprint request (C. Bergmeir, Monash) — they often share. Or substitute with a later Bergmeir paper if OA |
| S3 Saltelli et al. 2008 textbook (Wiley) | Textbook — chapter-level fetch | n/a | Manual: Wiley Online via institutional access |
| T2 Lillie et al. 2011 (Personalized Medicine) | Closed, no preprint | Unpaywall `is_oa: false`, 0 OA locations; PMC search returns no hit for the DOI | Author reprint request (N.J. Schork) OR substitute the n-of-1 framing with Shamseer 2015 (T1, fetched) — that already lays out the within-subject inference framework |

**Method note for future fetch attempts**: per the project's [`fetch-paper` skill](../../../.claude/commands/fetch-paper.md), the most useful single trick is the Europe PMC API: `https://europepmc.org/api/getPdf?pmcid=PMC<id>` — bypasses PMC's JavaScript proof-of-work challenge and the Akamai/Incapsula walls on MDPI, BMJ direct, etc. It does **not** help for Project Euclid (Imperva) or for papers without a PMC ID.

---

## Cross-references

- Methodology MDs awaiting verified citations:
  - [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)
  - [`permutation_null_block_length.md`](permutation_null_block_length.md)
  - [`train_validate_split_fate.md`](train_validate_split_fate.md) (pending)
- Citation discipline: [[feedback_methodology_decisions_documented_reasoning]]
- Literature folder layout: [`docs/research/literature/`](../literature/) — add `methodology/` subfolder
