# Methodology review: Heavy-day crash-risk prediction — rest-adjacency + streak-length as predictors of crash-in-window (methodology/heavy_day_crash_risk_prediction.md)

**Target**: [../methodology/heavy_day_crash_risk_prediction.md](../methodology/heavy_day_crash_risk_prediction.md)
**Target commit**: `8d9a118` (2026-07-16 08:55, "research/interpret/push-crash: methodology MD r2 (review absorbed) + review report"); working tree clean at review time for the target file
**Reviewer mode**: Claude (independent methodology peer reviewer per CONVENTIONS §1.2; producer-mode MD under §2.2 four-input bar). Fresh session — no exposure to the drafting context; doc-only knowledge.
**Review date**: 2026-07-16

---

## 1. What the MD specifies

The MD is a **predictive-categorical operand definition** covering two Q24-adjacent tests on the LC-era stratum: (§3) rest-adjacency around a heavy episode — bidirectional (rest-before + rest-after) at K ∈ {1, 2, 3} — as a predictor of crash occurrence in the +5d post-episode-end window; and (§4) consecutive-heavy-days streak length binned to L_bin ∈ {1, 2, 3, 4+} as a predictor of the same crash-in-5d outcome. Both tests inherit the parent Q24 MD [`post_heavy_day_compensatory_rest.md`](../methodology/post_heavy_day_compensatory_rest.md) LOCKED r1 (`58b7723`) machinery verbatim: stratum, heavy-day definition, unit-of-analysis (episode-end gap=0, n=314), crash outcome column (`is_crash` → `crash_in_5d`), overlap policies, and the anchor to the parent §3.5 compensatory-success/failure pool-split. New operand families: (a) `rest_day_p25` (personal 30d rolling p25 on total_steps) primary + `rest_day_class` (exertion_class ∈ {none, light}) sensitivity per CONVENTIONS §3.3 definitional-pair discipline; (b) streak-length bins with 4+ merging for statistical viability. Statistical machinery: Fisher's exact + Wilson CIs + bootstrap B=10,000 + Cochran-Armitage trend test (streak-length only) + RANDOM_SEED=20260716. The MD reframes Q24 sub-part 5 from parent §1.3 "unfalsifiable counterfactual" to "testably-predictive-associational" (§1.3, load-bearing) and pre-commits six confound classes as caveat-class per §4.2. Downstream artefacts blocked on r2 lock: Stage D descriptive audit for these predictive-categorical outcomes, and any subsequent Stage H pre-registrations. Notably, §6.6 already surfaces an exploratory 2×2 that shows likely sign-inversion on both directions (RR = 1.57 rest-after, RR = 1.86 rest-before), which the endogeneity confound in §3.9 explicitly anticipates.

---

## 2. What fired and why

### Spine — §2.2 four-input bar (inherits from CONVENTIONS §2.2)

#### I1 — Best-practices standards

- **I1.1 — State-of-art for observational-associational binary-outcome-with-binary-exposure on n=1 not named [substantive].** The §3 rest-adjacency 2×2 with risk ratio + Fisher's exact test is a classical epidemiological pattern; the state-of-art for observational inference under endogenous exposure is either **modified-Poisson regression with robust SE for binary outcome** (Zou 2004 *Am J Epidemiol*, log-binomial for RR) or, more directly for the exposure-choice endogeneity the §3.9 confound names, **inverse-probability-of-treatment weighting (IPTW) with propensity estimation on observed pre-exposure covariates** (Hernán & Robins *Causal Inference: What If*, chs. 12-15). The MD explicitly rejects propensity matching in §3.5-adjacent territory but the rejection is implicit (inherited from parent §4.3 n=1 fragility argument) rather than named + rejected here. This isn't demanding IPTW at n=1 — it likely does fail on this corpus — but naming the state-of-art + rejecting-with-reason closes the I1.2 silence. Analogous fire to the parent MD's I1.1 fire re ITS.

- **I1.2 — Cochran-Armitage trend test named + reference cited materially [pass].** §4.5 explicitly names Cochran-Armitage as the appropriate small-sample ordinal-exposure × binary-outcome trend test and cites Armitage 1955. This is the §2.2 discipline cleared for the §4 machinery. Better than the §3 handling.

- **I1.3 — Small-sample inference (Fisher's exact + Wilson + bootstrap) well-motivated [pass].** §3.6 explicitly names the small-sample-appropriate machinery (Fisher's exact, Wilson score CI, bootstrap B=10,000) with reasoning tied to the ~46 crash-in-5d episodes across 314 total. This is the corpus-fit-to-method discipline the §2.2 bar wants.

- **I1.4 — Risk ratio only; no adjusted OR or absolute-risk-difference framing [minor].** §3.5 reports RR + RD + Wilson CIs per arm. The MD does not name the **modified Poisson / log-binomial regression** alternative that yields RR with robust SE and admits covariate adjustment — useful if a future Stage H pre-reg wanted to adjust for the streak-length × era confound (§5 confound 3) or the streak-length × intensity confound (§5 confound 2) directly. A one-line pointer that adjusted RR via log-binomial is the natural extension when a specific confound needs adjusting closes the I1.2-shape silence.

#### I2 — Established literature

- **I2.1 — Rest-day-choice endogeneity framing well-argued but under-cited [substantive].** §3.9 confound 1 (rest-because-felt-bad enriches rest-adjacent arm with crash-prone episodes) is the mechanism the §6.6 exploratory 2×2 already surfaces as the likely explanation for the observed sign-inversion. This is exactly the pattern the epidemiological literature calls **confounding by indication** (Salas et al. 2001; Kyriacou & Lewis 2016 *JAMA*) — a foundational confound in observational pharmacoepidemiology where treatment choice is driven by the underlying condition being treated. The framing is right; the literature anchor is absent. Adding "confounding-by-indication (Salas 2001; Kyriacou & Lewis 2016)" as the named literature construct — one sentence in §3.9 confound 1 — closes I2.1 without changing the operand.

- **I2.2 — Wiggers push-crash framing cited without material anchor for the streak-length dose-response reading [minor].** §4.4 invokes "cumulative-load model + Wiggers push-crash framing" as the mechanistic prior for `longer streaks → higher crash rate`. The Wiggers cite is at the framing-level not the operationalisation-level (per §2.2 the standard is "each citation gets a sentence on what it actually contributes"). A more material anchor for the dose-response reading would be the sports-science load-injury literature (**Gabbett 2016 *Br J Sports Med*** on the acute:chronic workload ratio — RR increases sharply when acute-load exceeds chronic-load by a threshold factor). One sentence in §4.4 citing Gabbett's ACWR RR framework as the mechanistic prior for a dose-response of load-streak on adverse-outcome closes the fire.

- **I2.3 — Rolling-sum-predictor autocorrelation flag correctly anchored to HA-P7 [pass, non-trivial].** §4.7 anticipatorily cites HA-P7 verdict-review + `hypothesis_lock_process.md §4.6` for the rolling-sum-predictor factor-of-2 flag pattern. This is precisely the §4.6 anticipatory-drafting-note discipline the lock-process MD wants for any rolling-sum predictor — HA-P7 §8 did NOT anticipate this flag and needed a workaround verdict-review. §4.7 does anticipate it, and additionally argues (correctly) that the per-episode-end unit-of-analysis largely deflects the concern. Exemplary handling of a foreseen review trigger; a good example for future MDs.

- **I2.4 — Chu 2018 24-72h PEM-peak window cited materially at §3.2 [pass].** The K=3 primary rationale explicitly ties to the parent MD's Chu-anchored window ladder, correctly transferring the mechanistic anchor to the rest-adjacency-window choice. Material cite.

#### I3 — Tradeoff vision

- **I3.1 — Definitional-pair (p25 primary + class sensitivity) explicit [pass].** §3.1 explicitly names the two rest-day operands, their axes (steps-only vs 4-axis composite), and pre-commits pick-one-per-analysis discipline per CONVENTIONS §3.3. §6.1 shows the two operands diverge in rate (26.5% vs 47.5%) and the divergence is framed as "genuine operational-definition difference" not a data-quality issue — this is the tradeoff-vision discipline done right.

- **I3.2 — K-ladder tradeoff explicit + symmetric between before/after [pass].** §3.2 + §3.3 tests K ∈ {1, 2, 3} in both directions with pre-committed rationale for keeping the K-symmetric (asymmetric K would confound directionality with window-tightness). Good.

- **I3.3 — Streak-length bin merging (4+) tradeoff explicit [pass].** §4.1 spells out why the sub-bins at 6+d are merged (n=1 each; no formal test can distinguish 6d vs 8d vs 10d). Ordinal ranking preserved without over-claiming resolution. Solid.

- **I3.4 — All-episodes pool vs strict-clean tradeoff explicit [pass, non-trivial].** §3.9 confound 4 + §3.10 explicitly name the all-episodes pool as primary (n=314) and strict-clean (n=52 at +5d) as sensitivity with the rationale that rest-adjacency is a well-defined per-episode property that doesn't require overlap-clean filtering. Divergence between primary and sensitivity 1 named as a substantive finding (identifies whether overlap-density confounds the rest-adjacency signal). Contrast with the parent MD which locked strict-clean as primary — this deliberate departure is well-argued.

- **I3.5 — Direction pre-commit (§3.7, §4.4) explicit + acknowledges endogeneity may drive sign-inversion [pass, non-trivial].** §3.7 pre-commits rest-adjacency → lower crash rate as the reading axis but §3.9 confound 1 explicitly names the endogeneity mechanism that would produce sign-inversion. §3.7 last sentence and §6.6 note pre-commit *the discipline*: pre-committed direction stands even when exploratory data shows the opposite; Stage D reports rigorously as sign-inversion, does not silently flip. This is exemplary reviewer-mode-with-authorization discipline — the pre-commit exists *before* the data-look, and the data-look confirms the confound was correctly anticipated.

- **I3.6 — Compensatory-failure sub-arm reuse tradeoff implicit [minor].** §3.9 confound 3 + §5 caveat 6 name the circularity with parent Q24 MD §3.5 pool-split (this MD's outcome IS the parent's pool-split axis, read from a different angle). The prose ("There is no circularity of test-statistic — this MD asks what predicts pool-membership; the parent asks what the trajectory looks like within each pool") is correct in the narrow test-statistic sense: the two MDs run structurally different tests (predictor-of-membership vs trajectory-within-pool). But the reporting-discipline addendum ("shared sample means findings must not be doubly-invoked as independent evidence") could be pushed further — the two arcs will produce a joint interpretive package where the choice of what to call the primary finding vs the secondary finding matters for headline reporting. One sentence in §5 caveat 6 stating that any Stage S1 synthesis must pick one MD as headline per Q24 sub-part and cite the other as complementary would close the door pre-emptively per parent MD I3.6 handling of the compensatory-success/failure pool split.

#### I4 — Research limitations + objectives

- **I4.1 — n=1 acknowledged; sample-size floor explicit per bin [pass].** §4.1 explicitly caveats the 4+ merging (n=22) and §4.6 acknowledges wide CIs at the 4+ bin. §3.6 explicitly acknowledges cell-count drops in the 2×2 contingency at n < 10 corners.

- **I4.2 — LC recovery trajectory acknowledged but not with §3.7 detrend hook [substantive].** §5 confound 7 inherits parent Q24 MD §10 caveat 8 (envelope-drift asymmetry) and prescribes an era-stratified sensitivity arm. §6.4 confirms empirically that 2026 has a notably higher rate of L=3 and L=4+ episodes (30.6% vs 8-11% baseline), directly relevant to §4 streak-length tests. **BUT**: the parent MD's §7.11 detrend absorption (added as pre-lock revision per parent MD review) is not mirrored here. The §3.7 detrend audit hook applies to raw pre-vs-post comparisons on the LC frame; the §3 + §4 tests here are **categorical predictor-outcome contingency tests**, not raw pre-vs-post windowed means, so the §3.7 hook does NOT literally apply. This is why the MD correctly does not import §7.11 verbatim. **However**: the era-stratified sensitivity in §5 confound 3 + confound 7 handles the same underlying envelope-drift concern via a different mechanism (stratification rather than detrending). A one-sentence clarification in §5 confound 7 that "the §3.7 CONVENTIONS detrend hook does not apply to categorical-outcome contingency tests; the era-stratified companion is the drift-correction analogue for this MD" would close the audit-trail question a reviewer of the Stage D result would otherwise ask. Not a fire on the analysis choice, a fire on the *documentation* of why §3.7 wasn't imported.

- **I4.3 — Descriptive-vs-inferential objective explicit [pass].** §1.2 explicitly disavows Stage H pre-registration ("per-HA pre-regs draft after Stage D descriptive audit results land"). §3.6 + §4.5 explicitly frame the effect-size bars as descriptive markers, not p-value verdicts, per CONVENTIONS §2.1.

- **I4.4 — Observational-not-experimental design acknowledged pervasively [pass, non-trivial].** §3.8 explicitly disavows causal claims for both null and positive findings ("no causal claim is made regardless of Stage D outcome"). §4.4 same for the streak-length direction pre-commit. §1.3 explicitly separates the causal reading (unfalsifiable per parent MD) from the predictive-associational reading (testable). This is the load-bearing reframing per §1.3 and the discipline is maintained.

- **I4.5 — Retrospective coding of `exertion_class_lagged_lcera` not directly acknowledged [minor].** Same soft caveat as parent MD I4.5 — the heavy-day class labels are computed retrospectively from a `[d-90, d-30]` reference window, so the "streak of heavy days" the participant experienced in real-time was against a different class label than the analytical class label. Worth one sentence noting the retrospective-vs-experienced distinction, but not load-bearing since the analytical framing is post-hoc predictive-associational.

### Layer 1 — Discipline gates (inherits from CONVENTIONS §2.1, §4.1-§4.3)

- **L1.1 — §2.1 descriptive-before-inference [pass].** §1.2 explicitly disavows pre-reg framing; §3.6 + §4.5 explicitly frame effect-size bars as descriptive markers per §2.1. §6.6 data-availability numbers cite "descriptive-only-with-CI reads" discipline.

- **L1.2 — §4.1 no interpretive marks [pass, non-trivial].** §3.5 uses the neutral term "rest-adjacent" rather than mechanistically-loaded terms like "compensatory rest choice"; the MD carefully separates the rest-day operand (observable behaviour) from any imputed mechanism (why the participant rested). §4.4 uses "cumulative-load-dose predictor" as an operand-name-not-mechanism.

- **L1.3 — §4.2 caveats vs a-priori [pass].** §3.9 + §5 confounds are all framed in caveat-class mode ("acknowledged as an uncorrected confounder; none is claimed to drive the outcome a-priori"). §3.7 direction pre-commits are labeled as "the pre-committed reading axis; opposite-direction findings are reported as sign-inversions" — same discipline as parent MD §7.7. §6.6 exploratory 2×2 is explicitly framed as "data-availability numbers only; no verdict" — critical given the sign-inversion pattern already visible.

- **L1.4 — §4.3 prior-driven framing [pass].** The Q24.5 sub-part reframing has strong prior sources (parent Q24 MD's descriptive framing of the same episodes) so confirmatory framing is appropriate; the MD stays predictive-associational, not causal — the framing is correctly conservative.

### Layer 2 — Observational n=1 (inherits from Daza 2018)

- **L2.1 — Within-subject counterfactual framing stated [pass].** §3.8 explicitly states the predictive-associational claim is compatible with three interpretations including endogenous rest-choice; the counterfactual reading (what if the participant hadn't rested?) is explicitly declined per §1.3. Clean.

- **L2.2 — Stationarity assumption acknowledged where it bites [substantive-partial].** §5 confound 7 (envelope-drift asymmetry) partially addresses this — it flags that rest-adjacency prevalence may drift across the corpus and pre-commits an era-stratified sensitivity arm. The §6.4 empirical confirmation (2026's higher L=3/L=4+ rate) is direct evidence the concern bites at §4. But the underlying assumption — that the 2×2 contingency contents are exchangeable across the 4-year LC-era stratum — is not made fully explicit at §3.5 or §4.3. The era-stratified sensitivity is the right response, but the stationarity assumption should be named at the primary-contrast level. One sentence at §3.5 stating "the primary contrast pools across the full LC-era; stationarity of the rest-adjacency × crash contingency across the era is a substantive assumption partially addressed by §5 confound 7" closes L2.2.

- **L2.3 — Calendar-time vs subject-time framing clear [pass].** LC-era stratum locked per parent inheritance; §6.4 gives explicit calendar-year cross-tab for streak-length.

- **L2.4 — Data provenance traceable [pass].** Every operand traces to `per_day_master.csv` columns; §2 pointer table explicitly names the crash source (`is_crash` propagated from `labels_crash_v2.csv` via `build_unified_dataset.py`); §6.1 explicitly names the LC-era coverage (100% for total_steps). The data-availability probe date (2026-07-16) is named. Best-in-class provenance handling.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

- **L3.1 — Autocorrelation handling [pass, partial].** §3.6 explicitly names bootstrap with block length = 1 for episode-level resampling under strict-clean policy; §3.10 sensitivity 2 explicitly names block length ≥ 5 for inclusive policy. §4.5 mirrors the same discipline for the streak-length test. §4.7 anticipatorily addresses the rolling-window-predictor structural autocorrelation via HA-P7 precedent + data-driven E[L]* diagnostic if longer streaks cluster in time. Solid handling; more explicit than the parent MD's initial L3.1 substantive fire (which was closed in parent §7.10 review absorption).

- **L3.2 — CONVENTIONS §3.7 detrend audit hook applicability [not applicable, redirected — see I4.2].** §3.7 audit hook targets raw pre-vs-post *window-mean* comparisons; the §3 + §4 tests here are categorical contingency tests where the outcome is binary crash-in-window (not a windowed mean). The era-stratified sensitivity arm (§5 confound 3 + 7) is the drift-correction analogue for the categorical test family. Not a fire on the analysis; a fire on the documentation of why §3.7 wasn't imported (see I4.2).

- **L3.3 — Multiplicity [pass].** §3.5 primary contrast has 3 K values × 2 directions = 6 cells per operand; §4.3 has 4 bins × 1 outcome = 4 cells; sensitivity arms multiply further. §3.6 explicitly notes descriptive-with-CI reads at Stage D per CONVENTIONS §2.1 with the parent MD's project-canonical single-cell headline lock + Holm step-down pattern deferred to Stage H per-HA pre-reg. Cleaner handling than the parent MD's L3.3 fire (which needed pre-lock absorption).

- **L3.4 — Level vs trend [not applicable — pass].** §4 test is inherently ordinal-trend (Cochran-Armitage); §3 test is binary-vs-binary. The level-vs-trend concern that binds continuous-outcome tests doesn't bind here.

- **L3.5 — State-of-art naming [substantive-partial — see I1.1].** The confounding-by-indication + log-binomial-regression state-of-art anchors are not named. Analogous to the parent MD's ITS-not-named fire; the descriptive framing partially absolves it but naming the state-of-art + explicitly deferring closes the audit trail.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3)

- **L4.1 — §3.1 personal baseline [pass, non-trivial].** §3.1 explicitly cites CONVENTIONS §3.1 personal-baseline discipline for the primary rest-day operand (`total_steps < 30d rolling p25`). The p25 percentile choice is well-motivated as "personal 30-day rolling baseline" rather than absolute cutoff; the sensitivity operand (`exertion_class ∈ {none, light}`) uses the project-canonical class boundary as the coarser alternative. Best-in-class Layer 4 handling.

- **L4.2 — §3.2 lagged-lcera variant [pass].** Heavy-day trigger inherits `exertion_class_lagged_lcera` per parent MD §2.2; sensitivity rest-day operand also uses `exertion_class_lagged_lcera ∈ {none, light}`. Consistent.

- **L4.3 — §3.3 definitional-pair discipline [pass, non-trivial].** §3.1 explicitly names the two rest-day operands as a definitional pair with the "pick primary + sensitivity; do not report both as independent evidence" pre-commit per CONVENTIONS §3.3. §6.1 empirically shows the two operands diverge in rate (26.5% vs 47.5%) with the divergence framed as substantive not a bug.

- **L4.4 — §3.4 crash-drop sensitivity [not applicable, redirected].** The outcome IS crash-in-window; the operand is not a correlation on PEM-pacing variables. Standard §3.4 sensitivity doesn't apply.

- **L4.5 — §3.5 spike-detecting metrics [not applicable].** No autonomic proxies in this MD's operand family.

- **L4.6 — §3.6 named counts [pass, non-trivial].** §2 pointer table + §6 data-availability audit hooks + §6.6 2×2 tables all follow the "n / unit / scheme / file" triplet discipline exactly. The named-count in §6.6 "34/202 = 16.8%" is the model form for the CONVENTIONS §3.6 triplet.

- **L4.7 — §3.7 detrend hook [not applicable, redirected — see I4.2 + L3.2].** Not a raw-mean pre-vs-post design; the era-stratified sensitivity in §5 confound 7 is the analogue.

- **L4.8 — §3.10 operationalisation faithful to data [pass, non-trivial].** §6 data-availability audit hooks reproduce every count against `per_day_master.csv` with the LC-era stratum filter (verified independently by this reviewer against the source CSV — see §5 verification below); the streak-length distribution in §6.2 reproduces Stage -1 audit §4 byte-identically; the 2×2 tables in §6.6 reproduce independently (verified: 100/12/168/34 for rest-after-3; 105/11/163/35 for rest-before-3 — both match target §6.6 exactly). This is CONVENTIONS §3.10 discipline done right — computation-path traced, corpus identity asserted, day-count named.

### Side observations

- **Side** — §3.4's tabular anchor (crash-rate on strict-clean at +3d = 16/125 = 12.8%; at +5d = 9/52 = 17.3%) is inherited from parent Stage D r4 §3 exactly. The target then uses "17.3% at +5d" as rationale for +5d as primary window for this MD, but the target's own primary pool (all-episodes n=314) has crash-in-5d rate = 46/314 = 14.6% (per §6.7). The +5d "17.3% strongest" justification anchors on the strict-clean sample, not the primary pool used here. Not a fire — the choice of +5d over +3d is also motivated by the parent MD's window ladder — but the reasoning would be tighter if §3.4 explicitly stated "+5d primary is inherited from parent MD's window ladder; the 17.3% strict-clean signal + 14.6% all-episodes signal both anchor the sample viability."

- **Side** — §6.6 note "Interpretive discipline" paragraph correctly frames the sign-inversion as anticipated by §3.9 endogeneity, and correctly commits to reporting the pre-committed direction anyway. This is exemplary discipline; worth flagging as a **positive** side observation for other MD drafters to model.

- **Side** — §7 compression discipline mirrors parent MD §12 verbatim; §8 lock log has one row with a comprehensive change description. Slightly light on r1 iteration history relative to parent MD's three lock-log rows, but the parent MD had three separate pre-lock revisions while this MD has one. Not a fire.

- **Side** — §9 cross-references list is thorough. Missing: could reference sister MD [`post_heavy_day_pacing_learning.md`](../methodology/post_heavy_day_pacing_learning.md) which is drafted in parallel per §1.1 mention but not in §9. Trivial completeness gap.

- **Side** — §4.7 explicitly names §4.6 of `hypothesis_lock_process.md` as anticipatory-drafting-note discipline. This is the exact §4.6 pattern the lock-process MD wants for future rolling-sum predictors; the target correctly disarms the concern by arguing the episode-end unit-of-analysis deflects it. This is textbook §4.6 anticipatory handling.

---

## 3. What does not fire (selective)

Non-trivial passes worth naming:

- **I3.5 — pre-committed direction discipline in the face of exploratory sign-inversion.** §3.7 + §6.6 note handle a delicate methodological situation with textbook discipline: the exploratory 2×2 in §6.6 already shows the pre-committed direction is likely wrong, and the endogeneity confound in §3.9 explicitly anticipates why. The MD's response — "the pre-committed direction stands as the reading axis; Stage D reports rigorously as sign-inversion, does not silently flip" — is exactly what CONVENTIONS §4.2 caveat-vs-a-priori discipline wants. Silent-flip would be data-peeking; declining-to-look would be denial; the MD does neither. Best-in-class handling of a difficult case.

- **L4.6 — named-counts discipline throughout §6.** Every count in §6.1-§6.7 carries the scheme + unit + source-file triplet per CONVENTIONS §3.6. The 2×2 tables in §6.6 have per-cell counts + risk ratios with the arithmetic shown ("34/202 = 16.8%"). This is the reproducibility discipline the corpus depends on.

- **I2.3 — HA-P7 rolling-sum-predictor precedent anticipatorily transferred.** §4.7 correctly imports the HA-P7 verdict-review + `hypothesis_lock_process.md §4.6` template as a foreseen review trigger. The MD then argues (correctly) that the episode-end unit-of-analysis largely deflects the concern because streak_length becomes a single per-episode value rather than a rolling emission. This is anticipatory-drafting-note discipline done right.

- **L4.1 + L4.3 — personal baseline + definitional-pair on the rest-day operand.** The p25 primary + class sensitivity operand pair is a clean CONVENTIONS §3.1 + §3.3 implementation; the empirical divergence at §6.1 (26.5% vs 47.5%) is correctly framed as a substantive operational-definition difference not a bug.

- **§1.3 reframing discipline — causal vs predictive-associational cleanly separated.** The MD explicitly names both readings, adopts only the testable one, and preserves the distinction across §3.8 (positive finding compatible with three interpretations including endogeneity), §3.9 (endogeneity as caveat-class), and §5 (extended confound list). The reframing is load-bearingly maintained throughout — see §5 below.

- **L4.8 (§3.10 faithful-to-data) fully passes.** All §6 data-availability numbers reproduce byte-identically against `per_day_master.csv` on the LC-era stratum. Independent verification: total_steps rest_p25 count = 404, heavy episode-ends gap=0 = 314, streak-length bins {188, 77, 27, 22}, 2×2 tables in §6.6 all match. The MD's own §6 probe date (2026-07-16) is the same date as this review — reproducibility is perfect.

---

## 4. What would strengthen this MD

Concrete revisions, each named + rationale + expected effect:

1. **Add one sentence to §3.9 confound 1 naming "confounding-by-indication" (Salas 2001; Kyriacou & Lewis 2016) as the epidemiological literature construct.** Current wording is mechanism-accurate but literature-anchor-absent. **Inherits**: §2.2 I2 material-citation discipline. **Expected effect**: closes I2.1 substantive fire; ties the §6.6 exploratory sign-inversion finding to a decades-old epidemiological pattern that Stage D readers can immediately place, rather than framing it as a novel corpus-specific observation. Adds a single citation without changing operand or analysis.

2. **Add one sentence to §5 confound 7 clarifying that CONVENTIONS §3.7 detrend hook does not literally apply to categorical-outcome contingency tests; the era-stratified sensitivity arm is the drift-correction analogue for this MD.** Current wording inherits the parent MD's envelope-drift caveat but doesn't explicitly close the audit-trail question "why not import §7.11 detrend?" **Inherits**: parent MD §7.11 audit-trail; CONVENTIONS §3.7 scope statement. **Expected effect**: closes I4.2 + L3.2 substantive-partial documentation fire; makes explicit why the parent MD's pre-lock §7.11 absorption isn't mirrored here. Reviewer of Stage D result won't have to re-derive this reasoning.

3. **Add §3.5 or §3.6 sentence naming modified-Poisson / log-binomial regression as the state-of-art extension when covariate adjustment is needed, with an explicit "deferred to Stage H pre-reg if a specific confound needs adjusting" pointer.** Current MD reports RR + RD + CIs; the state-of-art for RR estimation with covariate adjustment is log-binomial or modified-Poisson (Zou 2004). Naming it + deferring closes the silence per §2.2 discipline. **Inherits**: §2.2 I1 best-practices-standards discipline. **Expected effect**: closes I1.1 + L3.5 substantive-partial state-of-art-not-named fires. Signals that Fisher's exact + Wilson at Stage D is deliberate descriptive simplification.

4. **Add §5 confound 6 (circularity) one-sentence reporting-discipline extension: any Stage S1 synthesis must pick one MD as headline per Q24 sub-part.** Current wording ("shared sample means findings must not be doubly-invoked as independent evidence") is right but leaves the reporting mechanics open. Making explicit that Stage S1 picks headline vs complementary avoids double-invocation at the synthesis level. **Inherits**: parent MD I3.6 compensatory-success/failure-pool handling pattern. **Expected effect**: closes I3.6 minor fire.

5. **Add one sentence to §3.5 explicitly naming the stationarity assumption at the primary-contrast level.** Currently the stationarity concern is addressed at §5 confound 7 (era-stratified sensitivity arm) but not named at §3.5 where the primary contrast is defined. Explicit language: "The primary contrast pools across the full LC-era; stationarity of the rest-adjacency × crash contingency across the 4-year era is a substantive assumption partially addressed by §5 confound 7 (era-stratified sensitivity arm) and §5 confound 3 (streak-length × era cross-tab)." **Inherits**: Daza 2018 stationarity discipline; parent MD L2.2 pattern. **Expected effect**: closes L2.2 substantive-partial fire.

6. **Add one sentence to §4.4 citing Gabbett 2016 (acute:chronic workload ratio) as the mechanistic prior for the streak-length dose-response reading, in place of or alongside the current Wiggers cite.** Current MD invokes Wiggers at framing-level; Gabbett's ACWR framework is a direct sports-science operationalisation of the "cumulative load → adverse outcome" mechanism the streak-length dose-response test targets. **Inherits**: §2.2 I2 material-citation discipline. **Expected effect**: closes I2.2 minor fire; anchors the streak-length test to a specific quantitative literature tradition beyond project-internal Wiggers.

7. **Add sister MD [`post_heavy_day_pacing_learning.md`](../methodology/post_heavy_day_pacing_learning.md) to §9 cross-references.** Currently only mentioned at §1.1; §9 cross-refs list is otherwise thorough. Trivial completeness fix. **Expected effect**: closes minor Side observation.

8. **(Optional; not required for lock)** Add a §6.8 or §7 anticipatory subsection acknowledging that any Stage H pre-reg on the §3 rest-adjacency test where the Stage D descriptive read confirms sign-inversion **must draft with the sign-inversion as the pre-committed direction** (rather than trying to preserve the original §3.7 pre-commit at Stage H). This closes a Stage H drafting-discipline question that will otherwise surface at the next session boundary. Not lock-blocking but useful anticipatory-drafting-note per `hypothesis_lock_process.md §4.6` pattern.

---

## 5. Verdict

**DEFENSIBLE with revision** — the MD is a rigorous predictive-categorical-arc extension of the parent Q24 MD machinery with best-in-class handling of two delicate methodological situations (the §1.3 causal-vs-predictive reframing and the §3.9 endogeneity-anticipated-and-confirmed sign-inversion pattern at §6.6), but three substantive-partial fires require one-sentence pre-lock revisions: (a) I1.1 + L3.5 state-of-art (confounding-by-indication + log-binomial regression) not named, (b) I4.2 + L3.2 documentation of why CONVENTIONS §3.7 detrend hook was not imported (categorical-outcome tests use era-stratified sensitivity as the analogue), and (c) L2.2 stationarity assumption not named at the primary-contrast level. Fold in per parent MD's §3.6 compression discipline (mechanical clarifications + cross-cites + one-line pre-commits); architecture stands as drafted. The reframing from parent §1.3 "unfalsifiable counterfactual" to this MD's §1.3 "testably-predictive-associational" is load-bearingly maintained throughout; the endogeneity confound (§3.9) treatment is sufficient at the caveat-class level given the disciplined pre-commit-and-report-as-sign-inversion approach at §6.6; the circularity with parent §3.5 is not a fatal issue but warrants one sentence at §5 confound 6 pinning the Stage S1 synthesis reporting discipline.

---

## Methodology

This methodology review walks CONVENTIONS §2.2 four-input bar plus the applicable items from the 4-layer checklist defined in [../reviews/README.md](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

Plus the state-of-art literature specific to this methodology question (named in Section 2's I1 / I2 / L3 cells with material citation): Zou 2004 *Am J Epidemiol* (modified Poisson regression for RR with binary outcome, state-of-art extension for covariate-adjusted RR); Salas et al. 2001 + Kyriacou & Lewis 2016 *JAMA* (confounding-by-indication, the epidemiological literature construct for the §3.9 endogeneity mechanism); Gabbett 2016 *Br J Sports Med* (acute:chronic workload ratio, mechanistic prior for the streak-length dose-response reading); Armitage 1955 (Cochran-Armitage trend test, materially cited at §4.5); HA-P7 verdict-review + `hypothesis_lock_process.md §4.6` (anticipatorily transferred at §4.7 for the rolling-sum-predictor structural autocorrelation flag pattern).

Project-specific audit hooks from [../CONVENTIONS.md](../CONVENTIONS.md) §2.2 (four-input bar), §2.1 / §3 / §4 (discipline gates + audit hooks that apply to methodology choices). CONVENTIONS §3.10 operationalisation-faithful-to-data is fully passed via independent verification of every §6 data-availability number against `per_day_master.csv` on 2026-07-16 (LC-era stratum n=1524; rest_day_p25 count = 404; heavy episode-ends gap=0 = 314; streak-length bins {188, 77, 27, 22}; 2×2 tables at §6.6 match byte-identically). Structural comparison drawn against parent [`post_heavy_day_compensatory_rest.md`](../methodology/post_heavy_day_compensatory_rest.md) LOCKED r1 (`58b7723`; parent MD review [`methodology-post_heavy_day_compensatory_rest-2026-07-15.md`](methodology-post_heavy_day_compensatory_rest-2026-07-15.md)) — inheritance done cleanly with no re-derivation of parent machinery; sister MD [`post_heavy_day_pacing_learning.md`](../methodology/post_heavy_day_pacing_learning.md) (drafted in parallel; not a review target here) covers the phase-stratified + dose-response trajectory arc complementary to this MD's predictive-categorical arc.
