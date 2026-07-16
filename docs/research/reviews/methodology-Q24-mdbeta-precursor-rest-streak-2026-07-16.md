# Methodology review: Q24 MD-beta precursor rest-adjacency + streak-length descriptive audit

**Target artefact**: [`analyses/descriptive/Q24-mdbeta-precursor-rest-streak/audit.md`](../analyses/descriptive/Q24-mdbeta-precursor-rest-streak/audit.md) DRAFTED r1 2026-07-16 (producer-mode Stage -1 descriptive audit extension per [CONVENTIONS section 1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs)).

**Review type**: Producer-mode methodology-adjacent review — 4-layer checklist walk per [`reviews/README.md`](README.md) plus MD-beta-specific structural checks.

**Reviewer**: fresh-session Claude (Opus 4.7) under user delegation. Cold context; read target + companion script + parent MD-beta LOCKED r1 + grandparent Q24 MD LOCKED r1 + sister Stage -1 audit + CONVENTIONS sections 1-5 + reviews/README from disk.

**Discipline**: reviewer-mode per [CONVENTIONS section 1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations); NO edits to target audit, MD-beta, or CONVENTIONS. Verdict for producer-mode artefact per this doc's section 5.

---

## 1. What the data shows

Empirical claims made by the target audit, plain restate (interpretive framing separated in section 2):

1. **Reproducibility floor (audit sections 2-6, 13.1)**: audit's re-run of MD-beta sections 6.1-6.5 on `per_day_master.csv` reproduces every count byte-for-byte — 404 rest-day-primary + 724 rest-day-sensitivity, 188/77/27/22 streak-length bins, 12-cell rest-adjacent prevalence grid, streak x intensity + streak x era cross-tabs. Companion script `scripts/audit.py` produces all 12 output CSVs deterministically.

2. **12-cell primary contrast (audit section 7)**: under primary NaN-drop discipline, 11 of 12 K x direction x operand cells show RR > 1.0 (rest-adjacent HIGHER crash rate than rest-absent, opposite of MD-beta section 3.7 pre-committed direction). Only K=1 rest-before sensitivity matches pre-commit (RR = 0.87). At K=3 primary rest-after RR = 1.54; K=3 primary rest-before RR = 1.83.

3. **NaN-handling deviation (audit section 7 + 13.2)**: audit's primary NaN-drop gives RR = 1.54 rest-after + 1.83 rest-before at K=3 primary; companion `_naneqfalse.csv` reproduces MD-beta section 6.6 draft (RR = 1.57 + 1.86) byte-for-byte via NaN-coerced-to-False.

4. **Rest-before vs rest-after asymmetry (audit section 7.3)**: primary-operand rest-before RR exceeds rest-after RR at every K (deltas +0.12, +0.34, +0.29; mean +0.25). Direction is compatible with MD-beta section 3.9 item 2 endogeneity-asymmetry prediction.

5. **Era-stratified instability (audit section 9)**: K=3 primary rest-after RR by year: 2022 = 1.08, 2023 = 2.02, 2024 = 1.56, 2025 = 0.78, 2026 = 0.57. Whole-corpus sign-inversion is driven primarily by 2023-2024; 2025-2026 flip toward the MD-beta section 3.7 pre-committed direction.

6. **Intensity-stratified instability (audit section 10)**: K=3 primary rest-after RR by episode-end intensity: heavy = 2.07, very_heavy = 0.96. Whole-corpus sign-inversion is driven primarily by heavy-terminal episodes; very_heavy-terminal episodes show no inversion.

7. **Overlap-policy divergence (audit section 11)**: K=3 primary rest-after on the strict-clean subset (n=51, matching parent Stage D r4 n=52 minus one NaN drop) gives RR = 0.37 — a full sign-flip from the all-episodes RR = 1.54. Rest-absent arm on strict-clean is n=8 with 3 crash-in-5d events (Wilson CI [13.7, 69.4]).

8. **Streak-length x crash (audit section 8)**: all-episodes pool crash rate by L_bin {1, 2, 3, 4+} = 14.9% / 13.0% / 18.5% / 13.6% — flat, not monotone-increasing per MD-beta section 4.4 pre-committed direction. Strict-clean subset is too small at L in {2, 3, 4+} for descriptive interpretation (n <= 6 per bin).

9. **Era-stratified streak-length (audit section 12)**: 2023 + 2024 exhibit the MD-beta section 4.4 pre-committed direction at small sub-cell n; 2025-2026 do not. Same era-boundary as section 9.

10. **Six reviewer-concerns surfaced (audit section 13.9)**: NaN discipline, era-stratified vs pooled reporting, intensity-stratified vs pooled reporting, overlap-policy sensitivity flip, streak-length flat dose-response, and a compound-confound-stack question re MD-beta r2.

---

## 2. What fired and why

Layer-grouped fires with quote citations, magnitude, and absorb-vs-escalate signal.

### Layer 1 — Universal reporting (SCRIBE 2016; STROBE 2007)

**L1.1 Operationalisation traceability — PASSES with high confidence.** Audit section 5 header "Frame" line names stratum + heavy-day definition + unit-of-analysis + rest-day operand definitions with source-file cross-refs; audit section 2 restates rest-day operands verbatim from MD-beta section 3.1; the `scripts/audit.py` companion reproduces every emitted CSV. Named-count discipline per CONVENTIONS section 3.6 is followed throughout (e.g. audit section 1 table row "Crash days | 103 (crash_v2, day-level, `labels_crash_v2.csv`)").

**L1.2 Deviation-from-parent-MD documentation — PASSES.** The NaN-discipline divergence from MD-beta section 6.6 draft is surfaced explicitly at audit section 7 opening paragraph + audit section 13.2, with both the primary NaN-drop CSV and the companion NaN-as-False CSV preserved. This is the model of how to document a producer-mode divergence per [CONVENTIONS section 4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no): the deviation is quantified (2-4 episodes per cell; RR moves 0.02-0.03; sign never changes), attributed to the discipline choice (CONVENTIONS zero-vs-NaN citation), and the companion reproduction is preserved. Absorb signal: safe for r1 lock.

**L1.3 Anchor citations — PASSES.** Confounding-by-indication citation (Salas 2001; Kyriacou & Lewis 2016 *JAMA*) is cited correctly at audit sections 7.2 + 9.3 as anchor for the endogeneity mechanism — inherits from MD-beta section 3.9 item 1 without re-derivation.

**L1.4 CONVENTIONS "section 5" citation — MINOR FIRE (mechanical clarification absorb).** The audit cites "CONVENTIONS section 5" repeatedly for zero-vs-NaN discipline (audit sections 2, 6, 7, 13.2, 13.9). Reading CONVENTIONS.md directly, section 5 is "Project-wide anchors" (LC timeline, default analysis window, Garmin extraction start, FIT resolver, DATA_DICTIONARY pointer). The presence-conditioned NaN-vs-zero discipline lives at CONVENTIONS section 4.4 (`v24 + per_day_intensity are presence-conditioned`), specifically the paragraph "In `per_day_master.csv`: presence-conditioned columns are NaN when `has_note == False`, not 0." Whether "section 5" is a stale-numbering artefact or a shorthand for the anchor-list, the citation is not resolvable to a specific paragraph in the current CONVENTIONS. **Recommend**: r2 clarify the citation target (either point at section 4.4 explicitly, or state the discipline inline without citation since the CONVENTIONS text does not have a dedicated zero-vs-NaN section for continuous columns like `total_steps` or class columns like `exertion_class_lagged_lcera`). Not blocking; the underlying NaN-drop-vs-NaN-as-False decision is defensible on its own merits (any observed True in a truncated window still returns True; window truncation + no True observed returns NaN; standard missing-data hygiene).

### Layer 2 — Observational n=1 (Daza 2018)

**L2.1 Counterfactual framing — PASSES.** Audit section 7.2 explicitly names the three alternative interpretations of the 11/12 sign-inversion (genuine sign-inversion under endogeneity; chance sampling in n=314 with 14.6% base rate; unobserved confounder) and states that Stage -1 does not distinguish between them. Predictive-associational framing per MD-beta section 1.3 is preserved throughout — no causal language leaks in.

**L2.2 Stationarity assumption — SUBSTANTIVE FIRE (architectural escalate to reviewer, absorb-eligible for MD-beta author).** Audit section 9 surfaces era-stratified RR values (2022=1.08, 2023=2.02, 2024=1.56, 2025=0.78, 2026=0.57) that **empirically stress MD-beta section 3.5's stationarity assumption** to the point where the pooled-contrast reading changes its interpretation. Audit section 13.9 concern 2 correctly asks: "given the strong era-instability (section 9), is pooling still defensible? MD-beta section 3.5 stationarity assumption paragraph acknowledges pooling as a substantive assumption; section 9 empirical evidence tests that assumption and finds it does not hold." This is exactly the reviewer-facing question this fire raises. Audit does the right thing by framing this as caveat-class (section 9.2) per CONVENTIONS section 4.2 and citing MD-beta section 5 confound 7 as the analogue drift-correction mechanism — but the magnitude of the era-instability (2x inversion in 2023 vs 0.57 in 2026 partial) is large enough that the reviewer needs to make an explicit MD-beta-r2 call. See section 4 below for the load-bearing recommendation.

**L2.3 Data provenance traceability — PASSES.** All CSV outputs are named + written to `output/`; script path is cited; `RANDOM_SEED = 20260716` is declared even though not exercised at Stage -1 (correct discipline — sets up Stage D reproducibility without over-claiming Stage -1 use).

### Layer 3 — Time-series specific (Natesan Batley 2023 autocorrelation; WWC 2022; CENT 2015)

**L3.1 Autocorrelation implications for downstream Stage D block-length choice — PASSES with minor comment.** MD-beta section 4.7 anticipates the rolling-window-predictor structural-autocorrelation flag from HA-P7 precedent; audit does not re-derive this at Stage -1 (correct scope) but section 5's mention of era-clustering (2025-2026 sub-elevation in L=3 + L=4+ episodes) implicitly gives an anchor for the Stage D E[L]* diagnostic per MD-beta section 4.7 pre-commit. Not a fire.

**L3.2 Multiple-testing across the 12-cell grid — MINOR COMMENT (absorb-eligible).** The 12-cell grid runs 12 RR comparisons on the same n=314 episode pool. Audit section 7 correctly frames this as descriptive-with-Wilson-CI (not a p-value verdict) per CONVENTIONS section 2.1, and MD-beta section 3.6 pre-commits the small-sample-appropriate machinery for the primary + sensitivity cells at Stage D. Nothing at Stage -1 needs flagging. But the audit's own section 13.3 headline "11 of 12 cells show sign-inversion" reads slightly stronger than the descriptive-with-CI framing warrants: 12 cells that share n=314 with definitional-pair discipline (primary + sensitivity of same K x direction share 62-77% of episode identifiers via the 26.5% vs 47.5% rest-day-rate overlap) means the 12 cells are far from independent tests. Recommend r2 add a one-sentence caveat that "11 of 12 cells" is a descriptive count on non-independent cells (primary + sensitivity of same K x direction are a definitional pair per CONVENTIONS section 3.3; the 12 cells are 6 K x direction pairs each with primary + sensitivity variant), not a 11-out-of-12-independent-tests read.

### Layer 4 — Project-specific audit hooks (CONVENTIONS sections 3-4)

**L4.1 Definitional-pair discipline per CONVENTIONS section 3.3 — PASSES.** Audit section 2 explicitly names the primary + sensitivity rest-day operands as a definitional pair per MD-beta section 3.1. Audit section 7.4 correctly notes that the single match-pre-commit cell (K=1 rest-before sensitivity, RR = 0.87) is NOT independent evidence — it is one member of a definitional pair with K=1 rest-before primary (RR = 1.34). This is exactly the discipline CONVENTIONS section 3.3 requires. Audit section 13.3 restates the discipline at findings-summary level.

**L4.2 Caveat-class vs a-priori framing per CONVENTIONS section 4.2 — PASSES.** Every substantive finding at audit sections 7-12 uses caveat-class language ("descriptive-with-CI observation UNDER the confounding-by-indication caveat", "caveat-class finding for any downstream Stage H pre-registration", "descriptive-with-CI framing"). No a-priori language leaks in — the era-stratified sign-inversion at sections 9-9.2 is framed as an empirical stress on the stationarity assumption, not as a claim that era-drift drives the outcome.

**L4.3 Named-count discipline per CONVENTIONS section 3.6 — PASSES.** Every count in the audit specifies scheme + unit + source file (e.g. audit section 1 table: "103 (crash_v2, day-level, `labels_crash_v2.csv`)"; audit section 8.1 row-total check reproduces the 46 / 314 = 14.6% base rate byte-for-byte against MD-beta section 6.7; audit section 8.2 reproduces the strict-clean n=52 + 9 / 52 = 17.3% against parent Stage D r4 section 3).

**L4.4 Intensity-stratified confound framing per MD-beta section 5 confound 2 — SUBSTANTIVE FIRE (architectural escalate to reviewer).** Audit section 10 surfaces heavy end_class RR = 2.07 vs very_heavy end_class RR = 0.96 — a stratification-level effect nearly as large as the era-stratification effect at section 9. Audit section 10.2 correctly frames this as "caveat-class finding for any downstream Stage H pre-registration" per CONVENTIONS section 4.2, and section 10.3 correctly extends MD-beta section 5 confound 2's Stage D machinery to the rest-adjacency arc. But MD-beta section 5 confound 2 pre-commits intensity as **sensitivity** for the streak-length arc — it does NOT pre-commit intensity as sensitivity for the rest-adjacency arc, and it does NOT pre-commit intensity stratification as **primary** at any level. The audit's finding is that intensity-instability is comparable in magnitude to era-instability, which raises the same reviewer question as L2.2: does MD-beta need r2 revision to pre-commit intensity-stratification as primary for the rest-adjacency arc? See section 4 below.

**L4.5 Overlap-policy sensitivity per MD-beta section 3.10 — PASSES with caveat correctly-surfaced.** Audit section 11 reports the strict-clean flip (RR = 0.37 vs all-episodes RR = 1.54) with the small-cell caveat explicit and appropriate: section 11 header notes "the rest-absent arm has n=8 with 3 crash-in-5d events (Wilson CI [13.7, 69.4] -- very wide). The 3/8 = 37.5% rate on the rest-absent arm is an outlier driven by tiny cell size (the corpus-baseline rest-absent rate on all-episodes is 10.9%); the strict-clean flip may be an artefact of the small comparator arm rather than a genuine overlap-policy effect." Audit section 11.2 correctly cites MD-beta section 3.10 for the pre-committed reporting discipline. The flip is not over-interpreted; the reviewer-concern flagged at audit section 13.9 concern 4 is correctly-framed ("is this a genuine overlap-contamination effect or a small-cell artefact?").

**L4.6 Streak-length flat-not-monotone framing per MD-beta section 4.4 — PASSES.** Audit section 8.3 correctly notes "MD-beta section 4.4 pre-committed direction (longer streaks -> HIGHER crash rate, dose-response of cumulative load) is NOT visible in the descriptive-with-CI read; the observed pattern is closer to flat than dose-response, and neither monotone-increasing nor monotone-decreasing." This is descriptive-with-CI framing without a-priori-claim leakage; the audit does NOT recast the flat pattern as evidence for a revised-direction pre-commit, which would violate CONVENTIONS section 2.1 descriptive-before-inference. Audit section 12 era-stratified breakdown correctly notes 2023 + 2024 match the pre-committed direction at small sub-cell n and 2025 + 2026 do not — this is honest reporting under caveat-class framing, not a data-driven-pre-commit.

**L4.7 Anticipatory §6.8 discipline — PASSES.** Audit section 13.8 correctly cites MD-beta section 6.8's pre-committed sign-inversion-closure pathway (options (a) Stage H drafts with anti-committed direction citing endogeneity, or (b) trigger pre-Stage-H MD r2 that flips section 3.7 direction pre-commit). The audit does NOT silently absorb the sign-inversion into a revised direction; it surfaces the closure question for the downstream Stage H reviewer. This is the exact discipline MD-beta section 6.8 specifies.

**L4.8 CONVENTIONS section 3.7 detrend does-not-apply-redirect — PASSES.** Audit section 9.2 correctly cites MD-beta section 5 confound 7's explicit documentation that era-stratification IS the analogue for the binary-outcome detrend mechanism. This is the load-bearing citation that keeps the reviewer from asking "why isn't the trajectory-detrend audit hook applied here?" — the answer is inherited from MD-beta's r1 patch 3 (which absorbed the same fire from the MD-beta review).

**L4.9 Discipline concerns list at audit section 13.9 — PASSES.** The six reviewer-concerns are well-formed, cite the specific section that surfaced each concern, and are actionable at either Stage D or MD-beta-r2. Concern 6 explicitly asks the load-bearing MD-beta-r2 question ("whether the operand family is Stage-H-viable at all, or whether MD-beta needs r2 revision that pre-commits era + intensity stratification as primary rather than sensitivity") — this is exactly the escalation point that requires an explicit reviewer call.

---

## 3. What does not fire (selective)

Non-trivial passes worth stating positively:

- **Reproducibility floor**: byte-for-byte match against MD-beta sections 6.1-6.5 across ~40 emitted numbers is stronger than the typical Stage -1 audit reproduces. Companion script emits both NaN-drop and NaN-as-False CSVs to make the deviation from MD-beta section 6.6 auditable at the raw-CSV level, not just at the audit-MD narrative level.
- **Anticipatory sign-inversion discipline**: MD-beta section 6.8's pre-committed closure pathway is threaded through audit sections 7.2, 9.3, 13.8. The audit does not silently absorb the sign-inversion into a data-driven revised direction pre-commit — a common Stage -1 failure mode this audit avoids.
- **Confound-2 restraint at Stage -1**: audit section 8.4 correctly notes that intensity as a confound for the streak-length arc is a foreseen Stage D concern per MD-beta but "does not have an observed effect to modulate at Stage -1" (because the streak-length pattern is flat, not monotone). Restraint from claiming intensity-adjustment is needed when there is no monotone signal to adjust away.
- **Small-cell noise handling**: audit section 11 (strict-clean n=8 rest-absent arm) + audit section 8.2 (strict-clean L=3 n=4) + audit section 12 (per-year L=4+ cells) all correctly refuse to interpret at tight-cell resolution. Section 13.8 Stage-D-readiness assessment correctly names which cells are viable vs underpowered.
- **Definitional-pair rigor on the K=1 rest-before sensitivity match-pre-commit cell**: audit sections 7.4 + 13.3 both correctly note that the single "matches pre-commit" cell is one half of a definitional pair with the K=1 rest-before primary cell (inverted at RR = 1.34), not an independent counter-example to the sign-inversion pattern.

---

## 4. What would strengthen this finding

Concrete + named. Each recommendation states expected effect.

### 4.1 (Load-bearing) MD-beta r2 recommendation on era + intensity stratification

**Recommendation**: MD-beta section 3 needs r2 revision that upgrades era-stratification AND intensity-stratification from sensitivity (current MD-beta section 5 confounds 3 + 7 caveat-class) to **primary pre-commit for the rest-adjacency arc**, based on the audit's empirical findings.

**Rationale**:

- **Era-stratification empirically breaks the stationarity assumption**. MD-beta section 3.5 (added in r1 review patch 1) explicitly names stationarity across the 4-year LC-era pooling as a "substantive assumption partially addressed by section 5 confound 7 (era-stratified sensitivity)". The audit's section 9 finding (RR = 2.02 in 2023, RR = 0.57 in 2026 partial — a 3.5x swing in relative-risk direction) is not partial-addressment territory; it is a *rejected assumption* at the descriptive-with-CI level. Pooling across a 4-year era where the joint distribution of rest-adjacency + crash-in-5d moves this much is not defensible as primary — it is defensible only as an era-averaged read on a caveat-class-flagged operand.
- **Intensity-stratification empirically breaks the confound-2 sensitivity framing**. MD-beta section 5 confound 2 currently pre-commits intensity as a Stage D sensitivity arm for the **streak-length arc only**. The audit's section 10 finding (heavy end_class RR = 2.07 vs very_heavy end_class RR = 0.96) shows intensity-instability is comparable in magnitude to era-instability for the **rest-adjacency arc**. That the same confound families gate two different arms in the same MD is architecturally significant; upgrading intensity to a primary pre-commit stratifier for the rest-adjacency arc keeps MD-beta's confound framework internally consistent.
- **The strict-clean flip (audit section 11) does NOT force r2 revision**. RR = 0.37 vs RR = 1.54 is a large divergence but rests on a rest-absent arm of n=8 with 3 crash events; the audit correctly frames this as "may be an artefact of the small comparator arm rather than a genuine overlap-policy effect". MD-beta section 3.10 sensitivity 1 already pre-commits strict-clean as sensitivity companion; no r2 change needed here.
- **The flat streak-length dose-response (audit section 8) does NOT force r2 revision on section 4.4 direction pre-commit**. The pattern is flat, not sign-inverted; MD-beta section 4.4 pre-committed direction is "longer streaks -> HIGHER crash rate", so a flat pattern is a null observation not a sign-inversion. Stage D Cochran-Armitage on n=46 events will formally test; the audit correctly restrains from pre-empting the Stage D result. No r2 change needed on the streak-length direction pre-commit.

**Two acceptable r2 revision paths**:

- **(r2 Path A, minimum patch)**: MD-beta section 5 confound 7 upgraded from "era-stratified sensitivity arm is a Stage D companion" to "era-stratified contrast is Stage D primary; pooled contrast reported as a caveat-class robustness read". Similarly MD-beta section 5 confound 2 upgraded to cover the rest-adjacency arc: "intensity-stratified contrast (heavy vs very_heavy end_class) is Stage D primary for the rest-adjacency arc; pooled contrast reported as caveat-class". The rest of MD-beta stays byte-for-byte identical; this is a mechanical clarification patch consistent with MD-beta section 7 compression discipline (mechanical clarifications, not architectural change).
- **(r2 Path B, deeper patch)**: MD-beta section 3.5 primary-contrast paragraph is amended to specify era + intensity as **required stratifiers at Stage D**, with the pooled read explicitly demoted to a supplementary caveat-class observation. This is closer to an architectural change (design of the primary contrast); per MD-beta section 7 compression rule this may require fresh-session re-review before r2 lock.

**Recommend Path A** as the smaller-magnitude change that captures the descriptive-with-CI finding without introducing architectural revision at r2. Path B is the cleaner design but forces re-review; Path A can absorb inline per the compression discipline.

**Expected effect on Stage D readiness**: Path A r2 revision unblocks Stage D with a defensible primary contrast (era-and-intensity-stratified rest-adjacency RR reads), with the pooled read demoted to caveat-class-only. Without this r2, the Stage D pooled read carries an unresolved empirical-stress on MD-beta section 3.5 that the pooled RR = 1.54 headline cannot address.

### 4.2 (Mechanical clarification, absorb) Fix CONVENTIONS "section 5" citation

Per L1.4 above, the audit's "CONVENTIONS section 5" citations for zero-vs-NaN discipline do not resolve to a dedicated CONVENTIONS section. Recommend r2 audit revision either:

- point at CONVENTIONS section 4.4 (`v24 + per_day_intensity are presence-conditioned`) with an explicit note that the NaN discipline applies analogously to `total_steps` (Garmin non-collection days) and `exertion_class_lagged_lcera` (bootstrap-window + gap days) even though CONVENTIONS section 4.4 is scoped to v24 + per_day_intensity, OR
- state the discipline inline ("NaN in either operand means missing observation, not zero rest-day-signal; NaN-drop preserves the missing-vs-negative distinction; NaN-as-False companion CSV documented for byte-for-byte reproduction of MD-beta section 6.6"). No CONVENTIONS citation needed if the underlying rationale is stated.

**Expected effect**: closes the audit-trail on the discipline choice without introducing a stale-reference risk in future r-revisions of CONVENTIONS.

### 4.3 (Mechanical clarification, absorb) Non-independence caveat on "11 of 12 cells" headline

Per L3.2 above, add a one-sentence caveat to audit sections 7.4 + 13.3 that the 12 cells are 6 K x direction pairs each with primary + sensitivity variant (definitional pair per CONVENTIONS section 3.3), so "11 of 12 cells inverted" reflects non-independent tests on a shared episode pool. This is a descriptive-count read, not an 11-out-of-12-independent-observations read.

**Expected effect**: prevents downstream synthesis (Stage S1 or Stage H pre-reg) from over-reading the "11 of 12" headline as if it were an independent-tests majority.

### 4.4 (Optional, discretionary) Descriptive check on rest-day frequency drift by era

MD-beta section 3.9 confound 6 notes "rest-adjacency prevalence may also drift (participant's rest-day frequency may have changed over the era)". The audit's section 6 rest-adjacent prevalence table is pooled across the era; a per-year rest-adjacency prevalence table at K=3 primary rest-after would sharpen the section 9 interpretation. If the 2025-2026 rest-adjacency prevalence rate on episode-ends is substantially different from the 2023-2024 rate, that would independently corroborate the joint-distribution shift the section 9 RR-flip implies.

**Expected effect**: separates the "rest genuinely became protective in 2025-2026" reading from the "rest-taking behaviour envelope shifted" reading at descriptive resolution. Not blocking for r1 lock; discretionary Stage D companion.

---

## 5. Verdict

**DEFENSIBLE with revision.**

The audit is a high-quality Stage -1 descriptive audit extension that reproduces MD-beta sections 6.1-6.5 byte-for-byte, correctly documents its NaN-discipline deviation from MD-beta section 6.6 with a companion CSV preserved, uses caveat-class framing consistently, and surfaces exactly the reviewer-concerns a downstream Stage H needs. The findings at audit sections 9 (era-stratified sign-inversion) and 10 (intensity-stratified sign-inversion) are strong enough to warrant an MD-beta r2 revision that upgrades era-stratification and intensity-stratification from sensitivity to primary pre-commit for the rest-adjacency arc (see section 4.1 above, Path A recommended as the mechanical-clarification-tier absorb). Mechanical clarifications on the CONVENTIONS section 5 citation (section 4.2) and the "11 of 12" independence caveat (section 4.3) are absorb-tier and do not block r1 lock. No BLOCKING issue found; the audit is safe to lock at r1 as-is with the understanding that MD-beta r2 revision follows in a downstream session.

---

## Methodology footer

This review walks the 4-layer checklist defined in [`reviews/README.md`](README.md), which inherits from:

- **Layer 1**: SCRIBE 2016 items 3-5, 14, 18, 22-24 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/)); STROBE 2007 items 6, 12, 13 ([literature/methodology/vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf)).
- **Layer 2**: Daza 2018 self-tracked n-of-1 counterfactual ([literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)); Personal Science norms.
- **Layer 3**: Natesan Batley et al. 2023 systematic review ([literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf)); WWC 2022 SCED handbook v5.0; CENT 2015 (Shamseer et al.).
- **Layer 4**: [CONVENTIONS.md](../CONVENTIONS.md) sections 3.1 (personal baseline), 3.3 (definitional pair), 3.6 (named counts), 4.2 (caveat-class), 4.4 (presence-conditioned NaN discipline as analogue for the audit's zero-vs-NaN framing), plus MD-beta section 3.9 confounding-by-indication + section 6.8 anticipatory closure pathway + section 5 confounds 2, 3, 7 discipline hooks.

Confounding-by-indication epidemiological anchor: Salas M et al. 2001; Kyriacou DN & Lewis RJ 2016 *JAMA* (both cited by MD-beta section 3.9 confound 1 and re-cited by target audit sections 7.2 + 9.3).

**Reviewer discipline**: fresh-session; cold context; read target audit + companion `scripts/audit.py` + MD-beta LOCKED r1 + grandparent Q24 MD LOCKED r1 + sister Stage -1 audit + CONVENTIONS + reviews/README from disk. NO edits to target audit, MD-beta, or CONVENTIONS. Spot-checked `output/rest_adjacency_by_era.csv` and `output/overlap_policy_sensitivity_2x2.csv` against audit narrative claims (both reproduce the audit's cited RR + n values).
