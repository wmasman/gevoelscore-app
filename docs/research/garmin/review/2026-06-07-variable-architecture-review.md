# Reviewer write-up — variable design and inferential apparatus for the Garmin × crash investigation

*Prepared as an independent peer-review piece on the variable architecture of the project. Reviews the dependent variable (`crash_v1`, `crash_v2`, gevoelscore continuous), the independent-variable family (Garmin biometric channels), and the inferential apparatus that links them. Reactions weighted to the project's stated aims: (i) descriptive characterisation of crashes and non-crash eras; (ii) precursor/correlational inference linking biometrics to crash onset; (iii) post-event retrospective indicators surfaced as cards.*

*Author: independent reviewer agent. Date: 2026-06-07. Status: discussion input, not a research-folder artifact — use to refine the variable design in the next phase.*

---

## 1. Scope of this review

What's in scope:

- The construct definitions of the dependent variable (crash_v1, crash_v2, dips, dip clusters, and the underlying gevoelscore 1–6 scale).
- The Garmin-derived independent variables across all H##/HA## tests, including operationalisation choices (aggregation level, baseline construction, threshold type, window length, directionality).
- The inferential apparatus linking the two: the pre-registration discipline, the train/validate split, the locked criterion bar, the sensitivity arms, the multi-comparison defence.

What's deliberately out of scope:

- The notes / clause-categorisation work (referenced where structurally relevant; not reviewed in detail).
- Calendar-context binding (queued, not active in current variable design).
- Implementation correctness of individual scripts.
- The downstream feature-design implications (card concepts, retrospective surfacing).

---

## 2. The dependent variable

### 2.1 What was done

The outcome label is built entirely from a single self-reported integer (gevoelscore, 1–6) collected daily across a 1,372-day window. Three derived constructs:

- **crash_v1** (binary episode): score ≤ 3 for ≥ 2 consecutive days, episodes merged within 3 days. Yields 29 episodes.
- **crash_v2 tier 1** (`crash`): empirically identical to crash_v1 — the pre-registered slow-recovery filter demoted zero episodes on first run and was removed.
- **crash_v2 tier 2** (`dip`): isolated single days with score ≤ 3 flanked by ≥ 4, excluding crash-recovery shadow. Yields 79 events.
- **Dip cluster overlay**: 15 transitive chains of ≥ 2 dips within 7 days (45 of 79 dips covered).

The 1–6 scale is left as a discrete outcome for episode tests and as a continuous(ish) trajectory for stabilisation-arc work (S01 trajectories on Garmin metrics, S02 proposed for the score itself).

### 2.2 Reviewer reaction

**Strengths.**

The construct is **transparently derived from a single source**, deliberately decoupled from any biometric variable, and the threshold choice (`score ≤ 3`) lands at a natural cleavage in the score distribution (80% of days at 4–5, 14% at ≤ 3) — defensible and replicable. The pre-registration discipline around revising v1 (from "personal bottom 15%" to absolute `≤ 3`) was a textbook example of preflight catching a bad spec before lockup. The same applies to the v2 slow-recovery filter being empirically demoted to zero effect and **removed rather than retained as a vanity rule** — that's good practice.

The two-tier (crash + dip) extension is a real epistemic gain. It surfaced a finding the binary v1 framework hid: the validate-era event-scape is dip-dominated, not crash-dominated. The dip:crash ratio change (1.9× → 3.5×) is one of the cleanest single observations in the project.

The empirical confirmation that all v1 episodes have tail_median ∈ {4, 5} is a **positive validation of the acute-condition spec** — v1 already only catches PEM-shape events, regardless of subsequent recovery speed. That's worth a sentence in the synthesis.

**Concerns.**

- **Power is structurally bounded.** 14 train crashes, 15 validate crashes. Every precursor test is asking "does the metric trigger on at least ~9 of 15 events?" With that denominator, a single misclassified episode swings the verdict by 6–7 percentage points. The pre-registered +15 pp bar is sometimes cleared by 1–2 pp (HA10 validate); these results are one differently-classified crash from being refuted.

- **The score is ordinal under cognitive load.** A 1–6 self-report by a participant with brainfog is bounded above by labeller-noise; "the same physical day" could plausibly score 3 vs. 4 on different mornings. The analysis treats the score as ground truth, which is unavoidable — but it should be named when interpreting marginal results. A "discrimination of +16 pp on a 15-pp bar" sits within plausible single-day-relabelling drift.

- **The dip/crash cleavage is a definitional, not biological, line.** Score 4 → 3 → 3 → 4 (two consecutive low days) becomes a crash; score 4 → 3 → 4 → 3 → 4 becomes two dips. The fact that downstream tests (K01, K02, H02b-on-dips) find different behaviour for the two tiers is a real finding — but it's worth surfacing that the cleavage *could have been one day in either direction* and the participant's discrete choice of when to register a "3" matters more than a smooth biological boundary would suggest.

- **`crash_v1` mixes mechanisms.** Stated as a caveat in every result.md, never operationalised away. The notes-driven mechanism categorisation (queued v3 / Goal B) is the natural fix; the autonomic-channel tests are operating on a pooled outcome that probably contains 2–4 distinct mechanisms (PEM crash, infection-driven low, hormonal cluster, depressive episode). Pooled-outcome dilution likely biases every test toward refutation.

- **The score has no pre-illness baseline.** Tracking started 2022-09-03, after LC diagnosis. "Recovery" framing implicitly references a pre-illness state we cannot observe; "stabilisation" framing references the floor of the tracked window. The reframe to stabilisation language is right; the residual asymmetry is worth naming in any descriptive piece.

**Limitations vs. possibilities.**

The structural power constraint is *intrinsic* — no analytical fix will produce more crashes. What's *possible* is mechanism-stratified outcomes (crash_v3 from notes labels) which would let the existing 29 episodes be analysed as 3–4 cleaner subgroups, accepting smaller-N per subgroup but cleaner signal-to-noise per subgroup. That's the highest-leverage methodological move on the outcome side.

The score-trajectory piece (proposed S02) is the natural descriptive complement to the current Garmin-only S01. It costs little and answers the lead/lag question between self-experience and biometric channels.

---

## 3. The independent variables

### 3.1 What was done

Garmin-derived variables tested across H## and HA## families fall into seven physiological channels. The methodological evolution across three generations is:

- **Generation 1** (H01–H05): daily aggregates, rolling 90-day baselines, absolute thresholds, 3-day or 7-day windows, mostly one-sided directionality.
- **Generation 2** (H02b, HA01–HA05): per-minute resolution for stress; per-day percentile-rank composite for activity; still rolling baselines mostly.
- **Generation 3** (HA01b-recomputed, HA06b, HA10, HA11, HA07c family): lagged baselines [d-90, d-30], z-score / relative thresholds, 4d primary + 5d secondary windows, bidirectional + one-sided sensitivity arms, threshold-tier sweeps (1.5/2.0/2.5 σ).

Summary of verdicts under current methodological standards:

| channel | best operationalisation | train | validate |
|---|---|---|---|
| per-minute waking stress | H02b/H02d/HA11 | SUPPORTED (+22 to +32 pp) | refuted |
| nightly RHR z-score | HA06b | SUPPORTED (+18.9 pp) | refuted |
| morning BB peak z-score | HA10 | refuted | SUPPORTED (+16.2 pp, fragile) |
| activity composite | HA01b lagged | refuted | refuted |
| push burden | HA02c lagged | refuted | refuted |
| sleep efficiency | H03 | refuted (Gen 1 only) | refuted (Gen 1 only) |
| BB daily net | H04 | refuted (Gen 1 only) | refuted (Gen 1 only) |

Pre-registered but not yet run: HA07c (sleep-stress mean delta), HA07d (sleep-stress variability), HA08c (sleep-stress slope).

### 3.2 Reviewer reaction

**Strengths.**

The **iteration discipline is genuinely impressive**. Each refinement (per-minute over daily; lagged over rolling; z-score over absolute; 4-5d over 3d; sensitivity arms over single-shot) was motivated by a specific methodological lesson and locked before the next round of tests. The Theme A baseline-contamination fix and the subsequent withdrawal of the HA01b "validate SUPPORTED" headline is a textbook case of pre-commitment discipline catching an artifact before it hardened. The audit trail (re-test pre-registered before any re-run ran, bar held at the original level, doc updates the same session) is exactly how researchers should handle the discovery of a methodological flaw mid-investigation.

The **pre-registration of soft outcomes** that determine downstream priority (HA10 → H04b authorisation) is a sophisticated practice that few academic projects do. Locking what you'd do under each verdict before seeing the verdict eliminates motivated reasoning from the prioritisation step.

The **threshold-tier sweep practice** (1.5/2.0/2.5 σ) is methodologically strong — it surfaces how fragile findings are to threshold choice without requiring a separate sensitivity analysis. HA10's validate finding only-at-1.5σ is *visible* in the result.md's combinations table precisely because the practice forces it to be reported.

The **per-minute stress channel** is the project's deepest investment, and it has produced the strongest train-era signal (H02d bridge × 5d, +31.8 pp). The replication across H02b (3d), H02b/H02d (sentinel handling), HA11 (within-day pattern), and now HA07c family (sleep-restricted) is the right way to triangulate a single physiological construct through multiple operationalisations.

**Concerns.**

- **Channel independence is overstated by the framing, not by the analyses themselves.** Synthesis-level claims like "four train-era SUPPORTED autonomic channels" weight as though the channels are independent samples of nature. They aren't. Per-minute stress, RHR, BB, and sleep-stress all feed each other (BB is `g(stress, sleep, HR)`; sleep stress is sleep-windowed stress). The right framing is "several operationalisations of an underlying autonomic-state construct, mostly confirming train-era signal" — equally interesting but less impressive-sounding. I flagged this in the previous review on HA10 specifically; it applies to the synthesis as a whole.

- **Generation 1 verdicts are methodologically dated.** H01 (daily RHR, rolling baseline, absolute threshold, 7d window) was sub-optimal on three independent axes by current standards. It has never been re-tested at Generation 3. Same applies to H03 (sleep efficiency) and H04 (BB net delta) — though H04's near-miss validate hint did motivate HA10's deeper look. A clean Generation-3 re-test of H01 is cheap and would either close or reopen the most foundational channel.

- **The "primary at the loosest threshold tier" pattern produces fragile headlines.** HA06b train SUPPORTED at 1.5σ but also at 2.0σ — robust. HA11 train SUPPORTED at 1.5σ but degrades at 2.5σ — moderately robust. **HA10 validate SUPPORTED at 1.5σ only — refuted at 2.0σ and 2.5σ.** A real signal should show threshold-monotonic discrimination: as threshold tightens, frequency drops but discrimination holds or rises. HA10 validate shows the opposite — signal sits in the loose-deviation tail. This is the single most fragile headline in the project.

- **The activity-labels v3.1 abstraction is two layers from raw signal.** `exertion_class` aggregates four axes (effective_exertion_min, step_burden, max_hr, vigorous_min) into one per-day binary via percentile rank. The Theme A bug bit this layer hardest precisely because the abstraction averaged away the bug's direct visibility. The fix was correct but the abstraction itself wasn't independently re-evaluated. A per-axis decomposition of HA01b would either confirm the composite or surface a single-axis signal/false-positive the composite hides.

- **Opacity asymmetry across channels.** "Garmin's algorithm is opaque" is named everywhere as a caveat, but it bites differently:
  - Per-minute stress: minimal opacity (raw integer per minute).
  - RHR (HA06b): low (lowest stable HR is a clean construct).
  - Body Battery (HA10): **high** — fused composite of HR, HRV, stress, sleep with undocumented internal calibration that has plausibly drifted across firmware versions.

  The "cross-channel coherence" framing weakens proportionally. HA10 is the most opacity-exposed of the four findings the synthesis leans on.

- **Some channels Garmin records are not tested at all.** Sleep architecture (deep %, REM %, fragmentation count) — H03b stub, blocked behind H04b; the flat-efficiency composite (H03) does *not* close those subcomponents. Respiration rate variability. Nocturnal SpO2. Intra-session intensity profiles. These aren't queued; the project hasn't decided whether they're worth pursuing.

- **The HA11 U-dip detector has parameter degrees of freedom that haven't been pre-justified from external literature.** Unlike "5-minute contiguous spike ≥ 75" (which can be reasoned from H02b's lineage), the U-dip shape has multiple tunable parameters (dip depth, plateau duration, plateau height delta). Pattern detectors are easier to over-fit than aggregate detectors. The pre-registration discipline locks the parameter choice, but the choice itself wasn't externally anchored. Worth a sensitivity check before HA11 enters the synthesis as a load-bearing finding.

**Limitations vs. possibilities.**

Intrinsic limitations:
- FR245 hardware blocks HRV. No within-device fix; only the API-path-C sleep-stress proxy (HA07c family) addresses this and only as a proxy.
- BB algorithm opacity is permanent — even if `unknown_233` is decoded, the *interpretation* of the resulting per-minute number is calibrated to Garmin's internal logic, not to a known physiological standard.
- The shared-input problem (stress feeds BB, etc.) cannot be designed away. It can only be acknowledged and reflected in framing.

Possibilities still on the table:
- Sleep architecture testing (H03b) is cheap, independent of H04b, and the most under-tested clinically-cited PEM mechanism.
- A descriptive cross-channel correlation matrix would empirically anchor the "channels aren't independent" caveat instead of leaving it qualitative.
- Per-axis decomposition of the activity composite (HA01b axes individually).
- Generation-3 re-tests of H01, H02, H04 under the current methodological standard.
- HA10 threshold-monotonicity diagnostic, written explicitly rather than as a footnote.

---

## 4. The inferential apparatus

### 4.1 What was done

The inferential machinery linking outcome and predictor variables:

- **Pre-registration**: each hypothesis gets locked hypothesis.md before data inspection. Audit trail preserved. Spec changes create a new hypothesis (HA01 → HA01b → HA01b-recomputed) rather than silent revisions.
- **Train/validate split**: chronological, 2022-09 → 2023-12 vs 2024-01 → 2026-06. Both halves clear 10-episode minimum.
- **Both-eras rule**: pattern must clear the criterion in *both* train and validate independently to be SUPPORTED. Train-only or validate-only verdicts are reported but constitute an overall REFUTATION.
- **Three-criterion bar** (per H02b lineage, inherited across HA##): (a) frequency ≥ 60%, (b) discrimination ≥ +15 pp over null, (c) median magnitude ≥ pre-set floor. Any one fails → refuted.
- **Null sample**: 200 random non-overlapping reference windows, fixed seed.
- **Sensitivity arms**: one-sided + bidirectional + multiple thresholds reported alongside the primary verdict.
- **Multi-comparison defence**: the held-out validation window is the primary defence; counted-tests honesty is reported in each result.

### 4.2 Reviewer reaction

**Strengths.**

The both-eras rule is **conservative in the right direction for the use-case**. The project's downstream aim is a *feature that runs in late 2026*. A precursor that worked in 2023 but not 2025 would either false-alarm on settled-state days or miss residual crashes silently. The chronological-split conservatism aligns with the use-case conservatism — the harder test is the right test here.

The **escalating audit trail** when the Theme A bug was caught (re-test pre-registered before any re-run, bar held at original level, doc updates in the same session, headline softened honestly) is the gold standard for how a long-running investigation should handle a mid-stream methodological discovery.

The **soft-outcome pre-commits** for downstream prioritisation (HA10 → H04b) eliminate motivated reasoning from gating decisions.

**Concerns.**

- **The chronological split confounds two questions.** It tests "is the precursor present in this dataset?" *and* "does the precursor survive the stabilisation transition?" simultaneously, with a single bar. As I noted in our methodological discussion: era is better treated as a moderator-of-interest than as a generalisation gate. The current "train SUPPORTED, validate refuted, overall refuted" framing buries era-specific findings as failures. An era-as-moderator framing would celebrate them as findings. This is a presentation issue more than an analysis issue, but it shapes how the project's narrative arc reads.

- **The both-eras rule is more stringent than scientific practice normally demands.** It's effectively requiring replication in two populations rather than statistical significance in one. Defensible for the feature-design use-case; but it means the project's "near-zero overall-SUPPORTED" tally undersells how much real signal exists in either era.

- **N=15 per era is power-bounded.** A Fisher's exact / binomial CI on 13/15 vs 141/200 (HA10 validate's headline) runs roughly 60% – 98% on the crash side. The +16.2 pp gap is 1.2 pp above the bar. **None of the result.md files report statistical-significance tests or confidence intervals on the bar-clearance.** Pre-registered bar-clearance is its own discipline, distinct from p-values — but with N this small, a one-line Fisher's exact on the primary 2×2 would be informative and is currently missing.

- **Multi-comparison discipline is good but not exhaustive.** Each test reports its own tests-to-date count (HA10 is the 14th). But within each test, sensitivity arms (3 thresholds × 2 directions × 2 windows = up to 12 combinations) add post-hoc combination harvesting potential. The pre-registration locks the *primary* arm; the all-combinations table inevitably contains some "interesting" arms. The synthesis-level practice of citing 5d-secondary one-sided arms (HA10) as headline-worthy findings goes past what the pre-registration discipline should authorise.

- **The null sample's autocorrelation structure isn't explicitly handled.** Random 4d non-crash windows are drawn from a 1,370-day series with multi-day signal autocorrelation. "Independent" reference windows aren't actually independent — drawing 200 from a 1,370-day pool with 4-day windows means substantial overlap is unavoidable. The verdicts probably aren't materially affected, but the null distribution's effective N is smaller than 200. A block-bootstrap construction would be more rigorous.

**Limitations vs. possibilities.**

The power limit is intrinsic — 29 episodes is what the participant has lived through.

Possibilities:
- Adding Fisher's exact / permutation p-values to all primary verdicts is cheap and would strengthen every result.md.
- Reframing era as a moderator (rather than as a split) in the synthesis narrative would let era-specific findings stand as findings, not failures.
- A pre-registered boundary-sensitivity check on one representative test (HA10 the natural candidate) would address the "the cliff was smooth" critique without redesigning anything.
- A pooled-analysis descriptive arm (ignoring era) reported alongside primary verdicts would surface signal that the both-eras rule masks.

---

## 5. The dependent–independent relationship across research aims

The project has three stated aims; each puts different demands on the variable architecture.

### 5.1 Aim 1 — Descriptive characterisation of crashes and non-crash eras

**Best served by:** S01 stabilisation trajectories, K01 (depth), K02 (duration), the dip-cluster overlay, the notes language analyses, and the proposed S02 score trajectory.

**Reviewer reaction:** This aim is **the project's strongest evidence base**. The "kind of crash changed" theory has been corroborated on ten-plus axes (depth, duration, language severity, day topology, lead-up language, dip:crash ratio, cluster concentration, precursor magnitude, lag length, threshold for triggering). The convergence across independent axes is genuinely impressive and rare in patient-data research. The descriptive arc is the project's most defensible output.

**What could be better:** The descriptive arc references "the stabilisation transition" without an empirically anchored boundary date (S02 would provide this). The dip-cluster overlay surfaces rough-patches but hasn't been characterised against notes or calendar context yet — that's queued work, valid to defer. The mechanism subtyping (crash_v3 from notes) would let the descriptive arc be cut by *kind*, not just by era; that's the highest-leverage descriptive next step.

### 5.2 Aim 2 — Precursor / predictive correlations

**Best served by:** the H## / HA## hypothesis-test family.

**Reviewer reaction:** This aim is where **the project is most conservative and produces the most refutations**. Six channels at Generation-3 standard yield one solid train-era cluster (per-minute stress, RHR, U-dip) and one threshold-fragile validate-era finding (HA10 morning BB peak). Five of those channels' verdicts are read by the synthesis as "the channel is closed for validate-era crashes."

The **conservatism is right for the use-case** but produces a narrative that may *undersell* what's been found. The per-minute stress signal is robust enough across H02b/H02d/HA11 that "train-era crashes have an autonomic-spike precursor" is solidly established at the discrimination level — it's just not validate-stable. The current framing reads this as a failure; an era-moderator framing would read it as a per-era characterisation.

**What could be better:**
- Statistical-significance reporting on primary verdicts (Fisher's exact / permutation).
- Generation-3 re-tests of H01/H03/H04 to close the foundational channels honestly.
- HA10 threshold-monotonicity diagnostic.
- Pooled descriptive arm alongside primary verdicts.
- HA01b per-axis decomposition.

### 5.3 Aim 3 — Post-event retrospective indicators (card concepts)

**Best served by:** H02b train-era retrospective ("there was a 17-minute stress spike on Tuesday afternoon"), HA01b validate-era retrospective (downgraded after Theme A), HA10 validate-era retrospective (reinstated after HA10 validate-SUPPORTED, threshold-fragile).

**Reviewer reaction:** This aim has had the **least systematic methodological scrutiny**. The card framing turns "this metric discriminated against null" into "this metric *explains* this crash." That's a much stronger inference than the discrimination test supports.

A retrospective card built on HA10's +16.2 pp validate signal would fire on 86.7% of crash windows but *also* on 70.5% of random non-crash windows. The participant-facing card would say "your morning BB was unusual in the 4 days before this" — which is *technically* true 86% of crash-time, but is also true 70% of innocent-time. The card has high false-positive volume at the surfacing level. The H02b specificity check engaged with this problem for the train channel; the equivalent work for HA10 hasn't been done.

**What could be better:**
- Specificity checks on every retrospective-card candidate before card.md is written.
- An explicit "card precision / recall" framing rather than "discrimination passes the bar" framing for the surfacing step.
- A defined policy for what a retrospective card *says* in plain language when the underlying signal is +16 pp discrimination (modest), vs. +30 pp (substantial).

This aim is the most **under-instrumented relative to its product-criticality**. The whole research program is upstream of the cards; the cards are where the participant will actually meet the findings. Right now there's no analytical step that translates "discrimination at +16 pp" into "card has X% chance of being right when it fires." That gap should be closed before any card ships.

---

## 6. Synthesised reviewer position

**The project is methodologically more rigorous than most patient-data research I've seen.** The pre-registration discipline, the iterative refinement of operationalisations, the willingness to withdraw findings under cleaner methodology, and the audit-trail preservation are all uncommonly strong.

**The project's chief vulnerabilities are not the analyses themselves but the framing layer.** Where it overstates: channel-independence claims, "first validate-era SUPPORTED" headlines on threshold-fragile findings, "population-level visible" language on n=1, "cross-channel coherence" on channels with shared inputs. Where it understates: era-specific findings dismissed as failures because of the both-eras bar; the per-minute stress channel as a solid within-era characterisation that the validate-era discipline buries.

**The dependent variable is the rate-limiter.** 29 episodes is what the participant has lived through. Every precursor test is sample-bounded by this. Mechanism subtyping (crash_v3 from notes) is the highest-leverage move on the outcome side — it would let the existing 29 episodes be analysed as cleaner subgroups even at the cost of smaller-N per subgroup.

**The independent-variable side has clear next steps**: Generation-3 re-tests of H01/H03/H04; HA10 threshold-monotonicity; HA01b per-axis; HA07c family with backfill-coverage gate; H03b sleep architecture; cross-channel correlation matrix.

**The retrospective-card aim is the most under-instrumented.** Specificity / precision framing is missing where it matters most.

If I had to name one structural shift that would improve the project's coherence across all three aims, it would be **promoting era from a split-variable to a first-class moderator variable in the framing layer**. The "kind of crash changed" narrative is already, in effect, an era-as-moderator story; the methodological framing just hasn't caught up to the narrative framing yet. Reframing this would let train-era findings be read as findings, validate-era findings be read as findings, and the era contrast itself be read as the project's central result — which is what the data is actually saying.

---

*Prepared as discussion input by the independent reviewer agent. Save under `docs/research/garmin/review/` for use in the next research-refinement phase.*
