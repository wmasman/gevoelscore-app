# Heavy-day crash-risk prediction: rest-adjacency + streak-length as predictors of crash-in-window

*Producer-mode methodology MD per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafted 2026-07-16 as r1; LOCKED r1 2026-07-16 post-review absorption per [`docs/research/reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md`](../reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md).*

---

## Authorship

**Drafted 2026-07-16** by Claude (Opus 4.7) in producer-mode subagent under user delegation per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem. Fresh-session `/research-methodology-review` before lock is the discipline mirror to the parent MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) (LOCKED r1 2026-07-15).

**Drafting trigger**: Q24 sub-part 5 ("does resting prevent crashes?") was framed by [Q24 MD §1.3](post_heavy_day_compensatory_rest.md#13-q24-sub-parts-covered) as an unfalsifiable counterfactual and left out of scope. User surfaced 2026-07-16 a **specific operationalisation** — *rest-day-adjacency around heavy episodes predicts crash rate in a fixed +K window* — that is testably predictive on the corpus (rest-day presence is observable, crash occurrence is observable, the association is measurable). Together with the consecutive-heavy-days-streak → crash-risk direction (cumulative-load-dose predictor) this MD frames both predictive-categorical outcome tests. Sister MD [`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md) (drafted in parallel) covers the trajectory-based outcomes (Q24 sub-part 3 + dose-response pacing) in a separate arc.

**Status**: **LOCKED r1 2026-07-16 post-review absorption.** Producer-mode artefact per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations); fresh-session methodology review absorbed inline from [`docs/research/reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md`](../reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md) (DEFENSIBLE with revision). Stage D descriptive audit for §3 rest-adjacency + §4 streak-length now unblocked against this LOCKED r1 operand.

---

## 1. Purpose and scope

### 1.1 What this MD covers

Two predictive-categorical tests on the LC-era corpus, both taking crash occurrence in a fixed post-episode window as the outcome (binary; `is_crash` column):

1. **Q24 sub-part 5 reframed — rest-adjacency around heavy episodes as a crash-rate predictor** (bidirectional: rest-before and rest-after the heavy episode).
2. **Consecutive-heavy-days-streak length as a crash-rate predictor** (cumulative-load-dose reading; single ordinal exposure).

Both tests share stratum, heavy-day definition, unit-of-analysis, and comparator machinery with the parent Q24 MD; this MD extends the inherited machinery to categorical crash-occurrence outcomes rather than continuous trajectory outcomes.

### 1.2 What this MD does not cover

- **Q24 sub-parts 1 + 4**: activity + sleep + autonomic trajectory outcomes on the compensatory-success pool. Covered in the parent MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1 (commit `58b7723`).
- **Q24 sub-part 3 + dose-response pacing trajectory**: phase-stratified reads + intensity dose-response on continuous outcomes. Covered in the sister MD [`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md), drafted in parallel on 2026-07-16.
- **Q24 sub-part 2**: within-day shape. Blocked on per-minute Garmin extraction; out of scope structurally.
- **Any Stage H pre-registration**: this MD locks operand + machinery; per-HA pre-regs draft after Stage D descriptive audit results land, in a downstream session under reviewer-mode-with-authorization.

### 1.3 Reframing note: Q24 sub-part 5 from unfalsifiable to testably predictive

[Q24 MD §1.3](post_heavy_day_compensatory_rest.md#13-q24-sub-parts-covered) marked sub-part 5 ("does resting prevent crashes?") as an **unfalsifiable counterfactual** and out of scope. That framing is correct for the causal reading of the question — no counterfactual "same episode without rest" exists at n=1. The reframing this MD adopts is not a re-opening of the causal claim; it is a distinct question about the same episodes:

- **Causal claim (unfalsifiable)**: rest-day-adjacency *caused* the absence of crash. Requires a counterfactual and is out of reach at n=1.
- **Predictive-associational claim (testably predictive on this corpus)**: rest-day-adjacency around a heavy episode is *associated with* crash rate in a fixed post-episode window. The association is measurable — two arms (rest-adjacent vs rest-absent) yield two crash rates; the risk ratio has a confidence interval; a null hypothesis can be defined.

The two readings are structurally distinct. This MD tests only the predictive-associational reading. Interpretation of any Stage D finding under this MD stays predictive-descriptive, not causal — a positive association is compatible with (a) rest lowering crash risk, (b) participant felt bad pre-heavy and both rested *and* was crash-vulnerable (endogenous choice; see §3.9), or (c) unobserved confounder. The distinction is preserved in all §7 caveat framing.

**Same discipline for the streak-length test in §4**: dose-response of streak length on crash rate is predictive-associational, not a causal claim about cumulative load causing crashes. The observational structure of the corpus does not support the causal reading; interpretation stays predictive.

### 1.4 Relation to sibling infrastructure

- **Parent Q24 MD** [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1: stratum, unit-of-analysis (episode-end gap=0), heavy-day definition, comparator machinery, pool-split framework. This MD inherits verbatim; §2 below is pointer-only.
- **Sister MD** [`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md) (drafted in parallel): trajectory-based outcomes for sub-part 3 + dose-response. Complementary arc; both MDs load-share on the parent MD's machinery.
- **Stage -1 audit** [`analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md`](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md) LOCKED r1: episode-length distribution (§4 — max 10d, 60% single-day, 22 episodes at 4+d) + heavy-rate-by-year cross-tab.
- **Stage D descriptive audit r4** [`analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md`](../analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md) LOCKED r4: parent-MD Wave 1 results. §3 pool sample sizes give the crash-in-window base-rate anchor (16/125 = 12.8% at +3d) that this MD's predictive tests read against.
- **HA-P7** [`analyses/hypotheses/HA-P7/`](../analyses/hypotheses/HA-P7/) — predictive-classifier precedent (rolling-crash-count → crash; NOT-SUPPORTED at r1). Structural-autocorrelation flag from HA-P7's E[L]* factor-of-2 review ([`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md)) transfers to §4 streak-length as a rolling-window predictor.
- **HA01c** [`analyses/hypotheses/HA01c-effective-exertion-shock/`](../analyses/hypotheses/HA01c-effective-exertion-shock/) — predictive-classifier precedent for effective-exertion-shock → crash.
- **CONVENTIONS**: §1.2 producer-mode, §2.1 descriptive-before-inference, §3.6 named-counts, §4.2 caveat-class framing, §5 zero-vs-NaN.

---

## 2. Inherited design (pointers to parent Q24 MD)

Every design element in this section is inherited from parent Q24 MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1 verbatim. No re-derivation. This section exists as a pointer table so the operand hooks below are readable without opening the parent MD.

| Element | Value | Source in parent Q24 MD |
|---|---|---|
| Stratum | LC-era only (`lc_phase == 'lc'`, `date >= 2022-04-04`), n=1524 | [Q24 MD §2.1](post_heavy_day_compensatory_rest.md#21-stratum) |
| Heavy-day definition | `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` | [Q24 MD §2.2](post_heavy_day_compensatory_rest.md#22-heavy-day-definition-locked-inherited) |
| Unit of analysis | Episode-end (gap=0 contiguous) | [Q24 MD §3.1](post_heavy_day_compensatory_rest.md#31-primary-episode-end-gap0-contiguous) |
| Episode-count | 314 gap=0 episode-ends on LC-era | [Stage -1 §4](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md#4-episode-structure--three-gap-tolerances) |
| Crash-outcome column | `is_crash` (boolean, LC-era total = 103; source `labels_crash_v2.csv` via `build_unified_dataset.py`) | [Q24 MD §3.5](post_heavy_day_compensatory_rest.md#35-crash-adjacency-handling-compensatory-success-vs-compensatory-failure-split) |
| Outcome window | Primary +5d (crash occurrence in `[D+1, D+5]` where D is episode-end) | [Q24 MD §5.1](post_heavy_day_compensatory_rest.md#51-window-ladder-locked-from-audit-63); sample n=52 strict-clean at +5d |
| Overlap policy | Strict-clean primary; inclusive as sensitivity | [Q24 MD §5.2](post_heavy_day_compensatory_rest.md#52-overlap-policies-both-reported-side-by-side-from-audit-64) |
| Multiplicity | Descriptive-only at Stage D; per-cell reads | [Q24 MD §7.10](post_heavy_day_compensatory_rest.md#710-null-hypothesis-inference-machinery-bootstrap--permutation--multiplicity) |

**Named-count discipline per [CONVENTIONS §3.6](../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file)**: all crash counts in this MD refer to `crash_v2` day-level rows (`is_crash == True` in `per_day_master.csv`, propagated from `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv`) unless otherwise stated. Episode counts refer to `gap=0` contiguous heavy-day runs where the heavy definition is per §2 above.

---

## 3. Sub-part 5: Rest-adjacency → crash risk (bidirectional)

### 3.1 Rest-day operand — primary + sensitivity (definitional-pair per [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair))

**Primary**: `rest_day_p25(d) = total_steps[d] < rolling_percentile_25(total_steps, window=30d, min_periods=15)`

- Anchored to a **personal 30-day rolling baseline** rather than an absolute cutoff, in the spirit of [CONVENTIONS §3.1](../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) (personal-baseline discipline).
- Adapts to participant's own recent activity envelope; addresses the LC-era baseline-drift concern inherited from parent Q24 MD §10 caveat 3 (2026 heavy-rate elevation, baseline drift).
- The 30d rolling window matches the pre-window used by the parent MD's trajectory-detrend companion ([Q24 MD §7.11](post_heavy_day_compensatory_rest.md#711-trajectory-detrend-sensitivity-per-conventions-37-envelope-drift-confound)); consistent-envelope discipline.
- `total_steps` LC-era coverage: 100.0% at daily row-level (structural for Garmin-instrumented days).

**Sensitivity**: `rest_day_class(d) = exertion_class_lagged_lcera[d] ∈ {none, light}`

- Categorical class already in `per_day_master.csv`; the coarser project-canonical definition of a low-load day.
- Definitional-pair-adjacent to the primary; both operationalise "low activity day" but from different axes (steps only vs the 4-axis composite class).
- Definitional-pair per [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair): pick primary + sensitivity; do not report both as independent evidence.

### 3.2 Rest-AFTER-heavy window

For each heavy-episode-end at day D (per §2 unit-of-analysis), the rest-AFTER indicator is:

`rest_after_K(D) = any(rest_day(d) for d in [D+1, D+K])`

K values tested at Stage D: **K = 1, 2, 3**. `K = 3` is the primary rest-after-K value; K=1 + K=2 are reported as sensitivity ladder (does the association vary with tightness of the adjacency window?).

**Rationale for K=3 as primary**: matches the [Q24 MD §5.1](post_heavy_day_compensatory_rest.md#51-window-ladder-locked-from-audit-63) primary trajectory window (+3d) and the Chu 2018 24-72h PEM-peak window that anchors the parent MD's window ladder. Rest within 72h of the heavy episode is the most physiologically-relevant adjacency; K=1 and K=2 are tightness sensitivity companions.

### 3.3 Rest-BEFORE-heavy window

For each heavy episode, let `D_start` = first day of the episode (episode's start, not end). The rest-BEFORE indicator is:

`rest_before_K(D_start) = any(rest_day(d) for d in [D_start - K, D_start - 1])`

K values tested at Stage D: **K = 1, 2, 3**. Same K-ladder as §3.2 for symmetry.

**Rationale for K-symmetry**: pre-committed to keep rest-before + rest-after tests structurally comparable. A finding that only fires in one direction (only rest-before matters, or only rest-after matters) is itself a substantive descriptive finding; asymmetric K definitions would confound directionality with window-tightness.

### 3.4 Outcome — crash occurrence in +5d window post-episode-end

`crash_in_5d(D) = any(is_crash[d] for d in [D+1, D+5])` where D is the heavy-episode-end (per §2).

**Anchored to parent Q24 MD §3.5 pool-split**: the compensatory-failure sub-arm in the parent's Stage D r4 audit ([`descriptive_audit.md` §3](../analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md)) is exactly `crash_in_5d == True`. This MD's outcome IS the parent MD's pool-split axis, read from a different angle:

- **Parent MD**: split episodes into compensatory-success (`crash_in_5d == False`) vs compensatory-failure (`crash_in_5d == True`); read trajectory shape within each pool.
- **This MD**: predict which pool an episode falls into from rest-adjacency (§3.5) or streak length (§4.3).

The two questions are complementary, not competing (see §3.9).

**Sample-size anchor from parent Stage D r4 §3** (crash-in-window rate on strict-clean episode-ends):

| Window | Compensatory-success | Compensatory-failure | Total strict-clean | Crash-rate on strict-clean |
|---:|---:|---:|---:|---:|
| +3d | 109 | 16 | 125 | 12.8% |
| +5d | 43 | 9 | 52 | 17.3% |
| +10d | 11 | 1 | 12 | 8.3% |

Corpus baseline crash rate (LC-era) is 103/1524 = **6.8%** ([Stage -1 audit §1](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md#1-corpus-summary)); the trigger-day-following crash rate is roughly **2×** the corpus baseline at primary windows. Descriptive anchor; interpretation is inherited from parent Stage D r4 §7.

**+5d as primary window for this MD** (not +3d): the +5d window is where the crash-rate signal is strongest (17.3% at +5d vs 12.8% at +3d in the strict-clean sample) and where the compensatory-failure sub-arm sample size is still workable (n=9 at strict-clean; the full-episode sample used in this MD is n=314, so cell counts are usable). Sub-arm sample sizes for this MD's tests are derived in §6 data-availability numbers.

### 3.5 Primary contrast — 2×2 contingency and risk ratio

For each `K ∈ {1, 2, 3}` × direction ∈ {before, after}:

**2×2 contingency**: (`rest_K` presence: True/False) × (`crash_in_5d`: True/False), computed over the full 314 heavy-episode-end pool (all-episodes pool, not restricted to strict-clean overlap — see §3.10 for the overlap-policy sensitivity).

**Primary reported statistics** per (K, direction) cell:

- Crash rate on rest-adjacent heavy-episodes: `P(crash_in_5d = True | rest_K = True)`
- Crash rate on rest-absent heavy-episodes: `P(crash_in_5d = True | rest_K = False)`
- Risk ratio (RR): rate_rest_adjacent / rate_rest_absent
- Risk difference (RD): rate_rest_adjacent − rate_rest_absent
- Wilson 95% CI on each per-arm rate
- Bootstrap 95% CI on RR (per §3.6 machinery)

**Stationarity assumption at the primary-contrast level**: the primary contrast pools across the full LC-era stratum (n=314 heavy-episode-ends spanning 2022-04-04 → 2026-06-05). Stationarity of the rest-adjacency × crash contingency across the 4-year era is a substantive assumption partially addressed by §5 confound 7 (era-stratified sensitivity arm) and §5 confound 3 (streak-length × era cross-tab); the §6 data-availability audit hook is the empirical check. Non-stationarity of rest-day prevalence, crash-rate baseline, or the joint distribution is a caveat-class concern per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), not a correction pre-committed at this MD level.

### 3.6 Statistical framing

**Small-sample-appropriate inference**: the compensatory-failure sub-arm has ~46 crash-in-5d episodes across the full 314-episode pool (see §6 data-availability numbers); per-cell counts in the 2×2 contingency can drop to n < 10 in a corner cell. Standard machinery:

- **Fisher's exact test** for the 2×2 contingency (small-sample-appropriate; no asymptotic assumption).
- **Bootstrap null** (B = 10,000; episode-level resampling; block length = 1 per parent MD §7.10 argument that episode-ends are approximately independent under the strict-clean policy; see §3.10 for the inclusive-policy sensitivity where a different block length is required).
- **RANDOM_SEED = 20260716** for reproducibility.
- **Wilson score CI** on each per-arm rate (small-sample-appropriate for proportions).

**Effect-size bar for descriptive-with-CI reads at this MD level**: risk-ratio CI excluding 1.0. This is a descriptive marker, NOT a p-value verdict — per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) descriptive-before-inference discipline, Stage D descriptive audits report CIs without inferential-verdict framing. Any downstream Stage H pre-registration draws its own falsification bar per [`hypothesis_lock_process.md`](hypothesis_lock_process.md) discipline.

**State-of-art for RR estimation with covariate adjustment**: Fisher's exact + Wilson score CI is the small-sample-appropriate primary read at this MD level; the state-of-art extension for covariate-adjusted RR estimation is **log-binomial regression** or **modified-Poisson regression with robust SE** (Zou 2004 *Am J Epidemiol*, "A modified Poisson regression approach to prospective studies with binary data"). Named + deferred: the natural Stage H extension when a specific confound (e.g. streak-length × era per §5 confound 3, or streak-length × intensity per §5 confound 2) needs direct adjustment is a log-binomial fit; not pre-committed at this MD level per the descriptive-only framing (§3.8, §4.5). Silence on this state-of-art would leave the reader without an audit-trail for why the simpler Fisher's + Wilson pair is the deliberate primary at Stage D.

### 3.7 Direction pre-commit

Both rest-before and rest-after: **rest-adjacency → LOWER crash rate**.

- **Rest-after direction**: hypothesised as compensatory response; rest in the +K window post-episode allows recovery envelope to buffer against crash-in-5d.
- **Rest-before direction**: hypothesised as pacing-preparation; rest in the −K window pre-episode leaves envelope higher entering the heavy day, reducing exhaustion-driven crash risk.

Both directions are the pre-committed reading axis; opposite-direction findings (rest-adjacent → HIGHER crash rate) are reported as sign-inversions per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) — a substantive finding in its own right, not a sign flip of the expected axis. Under the endogeneity confound in §3.9 the sign-inversion is a plausible outcome (rest-because-felt-bad is enriched for crash-vulnerable episodes), so the test is genuinely bidirectional in what it can surface.

### 3.8 Discipline — descriptive predictive-only

This MD tests a **predictive-associational** claim (§1.3), NOT a causal one. Interpretation of any Stage D finding stays predictive:

- A positive finding (rest-adjacent → lower crash rate, RR CI < 1.0) is compatible with: (a) rest genuinely lowers crash risk in the window; (b) unobserved third factor (e.g. participant felt fine pre-heavy → both rested less and was less crash-vulnerable, biasing the rest-adjacent arm toward crash-prone episodes — a sign-inversion mechanism); (c) chance in a small-sample corpus.
- A null or sign-inversion finding does NOT falsify the causal reading of "rest prevents crashes"; it falsifies the specific predictive-associational operationalisation on this corpus.

No causal claim is made regardless of Stage D outcome.

### 3.9 Confound pre-commit

Per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing. Each is acknowledged as an uncorrected confounder; none is claimed to drive the outcome a-priori.

1. **Rest-day-choice endogeneity** (primary confound): rest-day-adjacency is observational, not experimentally-manipulated. The participant may have chosen to rest **because they felt bad** — pre-heavy fatigue → rest-before-heavy chosen → participant enters heavy day already vulnerable → higher crash risk in +5d. The comparator group (rest-absent) is then enriched for episodes where the participant felt fine, biasing the "rest prevented crash" reading toward **NO effect**, or toward sign-inversion where rest-adjacent shows HIGHER crash rate. Directionality of the endogeneity is asymmetric between rest-before and rest-after (see item 2). **Epidemiological literature construct**: this mechanism is the pattern known in observational pharmacoepidemiology as **confounding-by-indication** (Salas et al. 2001; Kyriacou & Lewis 2016 *JAMA*) — treatment choice (rest vs no-rest) is driven by the underlying condition being treated (felt-bad pre-heavy). Naming the pattern per [CONVENTIONS §2.2](../CONVENTIONS.md#22-required-inputs) I2 discipline; ties the §6.6 exploratory sign-inversion to a decades-old epidemiological framing.

2. **Directionality of endogeneity — rest-before vs rest-after**: hardest for rest-BEFORE-heavy (the participant may have rested strategically before the heavy episode because they anticipated the load, but may also have rested because they felt bad). Rest-AFTER-heavy is **less endogenous** in direction — the heavy day is complete before the rest-day decision is made; subsequent rest is more forward-looking recovery than pre-episode illness signalling. If rest-before shows sign-inversion and rest-after shows the predicted direction, that pattern is consistent with the endogeneity asymmetry rather than a rest-prevents-crash mechanism.

3. **Circularity with parent Q24 MD §3.5 pool-split**: parent MD splits strict-clean episode-ends into compensatory-success vs compensatory-failure by `crash_in_5d`. This MD's outcome IS `crash_in_5d`. There is **no circularity of test-statistic** — this MD asks what predicts pool-membership; the parent asks what the trajectory looks like within each pool. But the shared sample means findings from the two MDs must not be doubly-invoked as independent evidence. **Reporting discipline**: any Stage D finding from this MD that fires on the same episode set as a parent MD Stage D finding cites the parent explicitly + notes the shared sample.

4. **All-episodes pool vs strict-clean pool** (see §3.10): this MD's primary contrast uses the full 314-episode pool (all gap=0 episode-ends) rather than the parent MD's strict-clean subset (n=125 at +3d, n=52 at +5d). Rationale: (a) rest-adjacency is a per-episode property that does not require the strict-clean overlap filter to be well-defined; (b) using the full pool preserves sample size for the crash-in-window contingency, which is the load-bearing measurement. Sensitivity: report the strict-clean subset as a companion arm at Stage D — divergence between all-episodes and strict-clean reads is a substantive finding (it identifies whether overlap-density confounds the rest-adjacency signal).

5. **Baseline-drift on the rest-day operand**: primary rest-day operand uses `personal 30d rolling-baseline percentile 25`. Inherits the baseline-drift caveat from parent Q24 MD §10 caveat 3 — the personal baseline is itself drifting across the LC era. Interpretation of the rest-day operand is relative-to-recent-past, not absolute. Sensitivity operand (`exertion_class_lagged_lcera ∈ {none, light}`, §3.1) uses a slower-drifting reference (lagged [d-90, d-30] baseline per parent MD §2.2) and is a robustness check on drift sensitivity.

6. **Envelope-drift asymmetry across the corpus** (parent Q24 MD §10 caveat 8): the LC-era corpus has drifting crash rate (~10/year 2023-2024 → ~2/year 2025-2026). Rest-adjacency prevalence may also drift (participant's rest-day frequency may have changed over the era; see §6 data-availability numbers). Reporting: an era-stratified sensitivity arm (rest-adjacency × crash-in-5d cross-tab restricted to same-year episodes) is a Stage D companion for the primary contrast. Escalation-to-caveat rule per parent MD §10 caveat 8 applies.

### 3.10 Overlap-policy sensitivity

Parent Q24 MD §5.2 locks strict-clean + inclusive as side-by-side arms for trajectory reads. For this MD's predictive tests:

- **Primary contrast**: all-episodes pool (n=314). No overlap-clean filter applied at the trigger side. Rationale: the rest-adjacency indicator + crash-in-5d outcome are well-defined regardless of other heavy days in the +K rest-window or the +5d crash-window.
- **Sensitivity 1 (strict-clean)**: restrict to episode-ends with no other heavy day in `[D+1, D+5]` (the parent MD's strict-clean at +5d, n=52). Removes overlap contamination in the crash-outcome window.
- **Sensitivity 2 (inclusive with block-appropriate null)**: full 314-episode pool with block-permutation null block length ≥ 5 (matching the +5d outcome window per parent MD §7.10 inclusive-policy machinery).

Divergence between primary and sensitivity 1 identifies whether overlap contamination is confounding the rest-adjacency signal. Divergence between primary and sensitivity 2 identifies whether autocorrelation in the null construction changes the effect-size CI materially.

---

## 4. Consecutive-heavy-days-streak length → crash risk

### 4.1 Streak-length operand

`streak_length(D_end) = |{contiguous heavy days ending at D_end}|` where D_end is the heavy-episode-end (per §2 unit-of-analysis; gap=0 contiguous definition inherited from parent MD).

**Streak-length bins**: `L_bin ∈ {1, 2, 3, 4+}` (four-level ordinal exposure).

- **`1`**: single-day heavy episodes (n=188 per [Stage -1 §4](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md#4-episode-structure--three-gap-tolerances)).
- **`2`**: two-day heavy episodes (n=77).
- **`3`**: three-day heavy episodes (n=27).
- **`4+`**: four-or-more-day heavy episodes (n=22, merged; the 4d/5d/6d/7d/8d/10d sub-bins have 12/6/1/1/1/1 respectively, so per-sub-bin analysis is not viable).

Merging at 4+ is the disciplined choice for statistical viability: no formal test can distinguish 6d vs 8d vs 10d with 1 episode each; the merged bin preserves ordinal ranking without over-claiming resolution.

### 4.2 Outcome — crash occurrence in +5d window after streak ends

Same as §3.4: `crash_in_5d(D_end) = any(is_crash[d] for d in [D_end+1, D_end+5])`.

Same rationale as §3.4 (parent MD Stage D r4 §3 pool-split anchor); +5d is the primary window because the crash-rate signal is strongest and the sample viability holds.

### 4.3 Primary contrast — crash rate by streak-length bin

For each `L_bin ∈ {1, 2, 3, 4+}`:

- Crash rate: `P(crash_in_5d = True | L_bin)` on the 314-episode pool.
- Wilson 95% CI per bin.

### 4.4 Direction pre-commit

**Longer streaks → higher crash rate** (dose-response of cumulative load on crash risk).

Mechanistic anchor: cumulative-load model + Wiggers push-crash framing; a 4-day heavy streak represents more cumulative load than a 1-day heavy episode and (under the dose-response reading) should carry higher post-episode crash risk. This is the pre-committed reading axis; a monotonic-decreasing pattern (shorter streaks → higher crash rate) would be a sign-inversion, reported as a substantive finding per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no).

### 4.5 Statistical framing

- **Wilson score CI** on each per-bin rate (small-sample-appropriate).
- **Cochran-Armitage trend test** on the ordinal 4-bin × binary-outcome contingency. Cochran-Armitage is the appropriate small-sample trend test for ordinal exposure on a binary outcome (references: Armitage 1955; standard biostatistical practice for dose-response on binary outcomes).
- **Bootstrap null** (B = 10,000; episode-level resampling; RANDOM_SEED = 20260716). Under the all-episodes primary pool the resampling unit is the episode; block length = 1 for strict-clean sensitivity companion, block length ≥ 5 for inclusive sensitivity companion (matches §3.10 machinery).
- **Effect-size bar for descriptive-with-CI reads at this MD level**: monotone increasing across bins with all-bin Wilson CIs distinct at extremes (1 vs 4+). Descriptive marker, not p-value verdict per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference).

### 4.6 Sample constraint

From [Stage -1 §4](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md#4-episode-structure--three-gap-tolerances): 188 single-day episodes (60%), 77 two-day (25%), 27 three-day (9%), 22 four-plus (7%). The 4+ bin merges all longer streaks; per-sub-bin at 6+d has only 4 episodes.

**Formal-test resolution**: the Cochran-Armitage trend test on the 4-bin ladder is defensible; per-bin descriptive reads at bins {1, 2, 3, 4+} are viable; per-sub-bin reads at 6+d are narrative-only. Crash-rate CIs at bin 4+ will be wide given n=22; interpretive discipline respects the wide-CI caveat.

### 4.7 Rolling-window-predictor structural-autocorrelation flag

Per [`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md) and the HA-P7 precedent ([HA-P7 verdict-review](../analyses/hypotheses/HA-P7/verdict-review.md)), any rolling-window predictor at window W ≥ 10 typically trips the E[L]* factor-of-2 flag under [`permutation_null_block_length.md`](permutation_null_block_length.md) machinery — the lag-1 autocorrelation of a rolling sum at window W approaches (W−1)/W by construction.

**Streak-length as a rolling-window predictor**: streak_length is technically a "rolling identifier" of contiguous heavy-day runs, not a true rolling sum. However, the day-level construction of streak_length has structural autocorrelation across consecutive days (day D and day D+1 within the same streak share streak_length identity by definition). At the episode-end unit-of-analysis this MD adopts, the per-episode streak_length is a **single value per episode-end**, not a rolling-window emission — the autocorrelation concern is mostly deflected by the unit-of-analysis choice.

**Pre-commitment for Stage D**: block length = 1 for episode-level resampling is defensible under the episode-end unit (per parent MD §7.10 argument). If the Stage D descriptive audit surfaces evidence that longer streaks cluster in time (e.g. multiple 4+d streaks within a 30d window), the data-driven E[L]* diagnostic per [`permutation_null_block_length.md §2`](permutation_null_block_length.md) is computed as a companion. If E[L]* ≥ 2× the locked block length of 1, the finding is flagged per HA-P7 §4.6 closure template: (a) cite structural clustering; (b) re-run at E[L]* block; (c) verify verdict robustness across block-length arms.

This is a foreseen review trigger, named per [`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md) anticipatory-drafting-note discipline.

---

## 5. Cross-arc confounds specific to §3 + §4

Per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing. Extends parent Q24 MD §10 caveats to the §3 + §4 predictive tests.

1. **Rest-day-choice endogeneity** (§3.9 item 1 + item 2): rest-day-adjacency is observational; the endogeneity biases the direction reported per §3.9. **Not corrected** in the primary read; caveat-class.

2. **Streak-length ↔ intensity confound**: do longer streaks contain a higher fraction of very_heavy days on average? A monotonic streak-length-crash relationship may be confounded by intensity (longer streaks → more very_heavy → higher crash rate not because of length per se but because of intensity accumulation). §6 data-availability numbers include the streak-length × intensity cross-tab. **Stage D handling**: report streak-length × crash-rate contrast alongside a intensity-adjusted companion (streak-length crash-rate restricted to streaks where fraction-very-heavy ≤ some cutoff, or intensity as a stratifier per parent MD §9).

3. **Streak-length ↔ era confound**: are longer streaks more common in specific years? Parent Q24 MD §10 caveat 1 flags 2026 heavy-rate elevation (47.4% partial-year vs ~34-35% baseline). §6 data-availability numbers include the streak-length × era cross-tab. **Stage D handling**: era-stratified sensitivity arm on the streak-length contrast (report crash-rate-by-bin excluding 2026, in parallel with primary all-era report). Same escalation-to-caveat rule as parent MD §10 caveat 1.

4. **Baseline-drift on the rest-day operand**: §3.9 item 5. Personal 30d rolling p25 drifts across the LC era; sensitivity operand (`exertion_class ∈ {none, light}`) is a robustness check.

5. **Rolling-sum-predictor autocorrelation flag** for streak-length as a rolling-window construct (§4.7): the E[L]* factor-of-2 flag from HA-P7 precedent applies. Foreseen review trigger; not corrected at MD level; Stage D descriptive-time diagnostic per [`permutation_null_block_length.md §2`](permutation_null_block_length.md).

6. **Circularity with parent Q24 MD §3.5 pool-split** (§3.9 item 3): shared sample with parent MD; findings must not be doubly-invoked. Reporting discipline: any Stage D finding cites the parent MD explicitly + notes the shared sample. **Any Stage S1 synthesis must pick one of {this MD, parent Q24 MD} as headline per Q24 sub-part and cite the other as complementary — the two are NOT independent evidence at Stage S1 level given the shared crash-in-5d outcome sample.**

7. **Envelope-drift asymmetry across the corpus** (parent Q24 MD §10 caveat 8): inherited. Reporting: era-stratified sensitivity for both the §3 rest-adjacency and §4 streak-length contrasts (see also confound 3 above for the streak-length × era angle).

   **CONVENTIONS §3.7 detrend hook — does-not-apply-redirected-to-analogue documentation**: parent Q24 MD §7.11 imports the [CONVENTIONS §3.7](../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) trajectory-detrend audit hook because its outcome family is raw-mean pre-vs-post windowed trajectories on continuous channels (parent §7.1-§7.9 nine trajectory-summary stats). This MD's outcome family is **binary crash occurrence** (`crash_in_5d`, a binary outcome per §3.4 / §4.2) with **binary-or-ordinal exposure** (rest-adjacent yes/no per §3.5; streak-length bin per §4.3). The CONVENTIONS §3.7 detrend machinery — subtract a linear pre-window fit from both trigger and comparator arms to remove smooth envelope drift — is **not directly applicable to a binary-outcome contingency test**: there is no "windowed mean" on a binary outcome whose pre-episode slope can be linearly extrapolated and subtracted at the per-episode level. **The era-stratified sensitivity arm (confound 7 above + confound 3 for the streak-length × era angle) is the analogue mechanism for the same underlying envelope-drift concern** — same concern (baseline-shift across the 4-year LC era), different statistical machinery (stratification of the contingency table by era rather than detrending of a continuous outcome). Per CONVENTIONS §3.7 concern, era-stratification is the equivalent drift-correction test for the categorical-outcome test family. Documented explicitly here so a Stage D reviewer does not need to re-derive why the parent MD's pre-lock §7.11 absorption is not mirrored in this MD.

---

## 6. Data availability audit hooks

Per [CONVENTIONS §3.6](../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file) named-count discipline. All numbers below reproduced by running an idempotent data-availability probe against `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` on 2026-07-16 with the LC-era stratum filter (`date >= 2022-04-04`, n=1524 rows).

### 6.1 Rest-day distribution across corpus

| Rest-day operand | Definition | LC-era rest-day count | Rest-day rate |
|---|---|---:|---:|
| Primary (`rest_day_p25`) | `total_steps < 30d rolling p25` (min_periods=15) | **404** | **26.5%** |
| Sensitivity (`rest_day_class`) | `exertion_class_lagged_lcera ∈ {none, light}` | **724** | **47.5%** |

The two operands diverge substantially in rate (~27% vs ~48%); the divergence identifies genuine operational-definition difference, not a data-quality flag. Primary is stricter (personal-baseline-relative); sensitivity is coarser (project-canonical class boundary). Both are load-bearing in different ways; the divergence is a foreseen sensitivity axis, not a bug.

**Note on `exertion_class` distribution** (LC-era n=1524):

| Class | n | rate |
|---|---:|---:|
| none | 372 | 24.4% |
| light | 352 | 23.1% |
| moderate | 198 | 13.0% |
| heavy | 276 | 18.1% |
| very_heavy | 256 | 16.8% |
| NaN | 70 | 4.6% |

Reproduces [Stage -1 audit §1](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md#1-corpus-summary) heavy + very_heavy + NaN counts; light + none + moderate breakdown is new to this MD.

### 6.2 Streak-length distribution (extends Stage -1 §4)

`gap=0` contiguous heavy-episode counts on LC-era, n=314 episodes total:

| L_bin | n | rate |
|---|---:|---:|
| 1 | 188 | 59.9% |
| 2 | 77 | 24.5% |
| 3 | 27 | 8.6% |
| 4+ | 22 | 7.0% |

Sub-bins within 4+ (for context, not for §4 primary bins):

| L | n |
|---:|---:|
| 4 | 12 |
| 5 | 6 |
| 6 | 1 |
| 7 | 1 |
| 8 | 1 |
| 10 | 1 |

Reproduces Stage -1 §4 exactly.

### 6.3 Streak-length × intensity cross-tab

Per-episode intensity fingerprint (fraction of episode's days that are `very_heavy`):

| L_bin | n episodes | mean vh_frac | median vh_frac | mean vh_count |
|---|---:|---:|---:|---:|
| 1 | 188 | 0.436 | 0.000 | 0.436 |
| 2 | 77 | 0.481 | 0.500 | 0.961 |
| 3 | 27 | 0.519 | 0.667 | 1.556 |
| 4+ | 22 | 0.538 | 0.550 | 2.636 |

**Interpretive discipline**: mean vh_frac is only mildly monotonically increasing with L_bin (0.44 → 0.48 → 0.52 → 0.54), so the streak-length × intensity confound is real but not extreme. Median vh_frac shows more variation (0 at L=1, 0.5 at L=2, 0.67 at L=3) driven by the L=1 bin's high count of heavy-only single-day episodes. Mean vh_count grows roughly linearly with L_bin (as expected mechanically). Stage D intensity-adjusted companion (§5 confound 2) uses this cross-tab as the anchor.

### 6.4 Streak-length × era cross-tab

`gap=0` heavy episodes by year × L_bin:

| Year | n episodes | L=1 | L=2 | L=3 | L=4+ |
|---|---:|---:|---:|---:|---:|
| 2022 | 44 | 26 | 11 | 2 | 5 |
| 2023 | 87 | 59 | 20 | 5 | 3 |
| 2024 | 81 | 50 | 23 | 4 | 4 |
| 2025 | 66 | 37 | 14 | 9 | 6 |
| 2026 (partial Jan-Jun) | 36 | 16 | 9 | 7 | 4 |

**Interpretive discipline**: the 2026 partial year has a notably higher rate of L=3 and L=4+ episodes relative to total (7+4 out of 36 = 30.6%, vs 8-11% in 2023 and 2024). This aligns with parent Q24 MD §10 caveat 1 (2026 heavy-rate elevation) and confirms the era-confound for §4 streak-length tests. Stage D era-stratified sensitivity arm (§5 confound 3) is the required companion.

### 6.5 Rest-adjacent heavy-episode counts (before + after)

For all 314 heavy-episode-ends on LC-era, rest-adjacency prevalence by K and direction:

| K | Rest-AFTER (primary p25) | Rest-BEFORE (primary p25) | Rest-AFTER (sensitivity class) | Rest-BEFORE (sensitivity class) |
|---:|---:|---:|---:|---:|
| 1 | 127 / 314 (40.4%) | 108 / 314 (34.4%) | 233 / 314 (74.2%) | 234 / 314 (74.5%) |
| 2 | 171 / 314 (54.5%) | 152 / 314 (48.4%) | 268 / 314 (85.4%) | 265 / 314 (84.4%) |
| 3 | 202 / 314 (64.3%) | 198 / 314 (63.1%) | 283 / 314 (90.1%) | 286 / 314 (91.1%) |

**Interpretive discipline**: rest-adjacent prevalence is high under both operands, especially the sensitivity (class-based) operand (90%+ at K=3). This means the rest-absent comparator arm at K=3 primary has n = 314 − 202 = **112 episodes**; the primary contrast has plenty of statistical resolution. The sensitivity operand at K=3 leaves only 314 − 283 = 31 rest-absent episodes; per-cell counts in the 2×2 contingency will be tight at K=3 under the sensitivity operand.

### 6.6 Rest-adjacency × crash-in-5d 2×2 (primary operand, K=3)

For all 314 heavy-episode-ends, using primary rest-day operand (p25) and K=3:

**Rest-AFTER-3 × crash-in-5d**:

| | crash-5d False | crash-5d True | Total |
|---|---:|---:|---:|
| rest_after_3 False | 100 | 12 | 112 |
| rest_after_3 True | 168 | 34 | 202 |
| Total | 268 | 46 | 314 |

- Crash rate on rest-after-adjacent: 34/202 = **16.8%**
- Crash rate on rest-after-absent: 12/112 = **10.7%**
- RR (rest-after-adjacent / rest-after-absent) = 16.8 / 10.7 = **1.57**

**Rest-BEFORE-3 × crash-in-5d**:

| | crash-5d False | crash-5d True | Total |
|---|---:|---:|---:|
| rest_before_3 False | 105 | 11 | 116 |
| rest_before_3 True | 163 | 35 | 198 |
| Total | 268 | 46 | 314 |

- Crash rate on rest-before-adjacent: 35/198 = **17.7%**
- Crash rate on rest-before-absent: 11/116 = **9.5%**
- RR (rest-before-adjacent / rest-before-absent) = 17.7 / 9.5 = **1.86**

**Interpretive discipline** (data-availability numbers only; no verdict): both directions show **sign-inversion relative to the §3.7 pre-committed direction** (rest-adjacent shows HIGHER crash rate in both directions). This is exactly the endogeneity pattern the §3.9 confound anticipates — rest-because-felt-bad enriches the rest-adjacent arm with crash-prone episodes. The Stage D descriptive audit will confirm sample-size stability + Wilson CIs + Fisher's exact test statistics; this MD-level data-availability sketch is not a verdict.

**Note on why to report the pre-committed direction anyway**: per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) and [`hypothesis_lock_process.md`](hypothesis_lock_process.md) discipline, pre-committed directions are locked *before* looking at the data. The §3.7 pre-commit stands as the reading axis even though the exploratory data-availability probe surfaces a probable sign-inversion. Stage D will confirm rigorously and report the finding as a sign-inversion, not silently flip the direction.

### 6.7 Crash-rate baseline anchor

From parent Stage D r4 §3 (inherited): crash-in-5d rate on strict-clean episode-ends = 9/52 = **17.3%** at +5d. Corpus baseline (LC-era) crash rate = 103/1524 = **6.8%**.

On the all-episodes pool this MD uses (n=314), crash-in-5d rate = 46/314 = **14.6%** — approximately 2× the corpus baseline, consistent with parent MD's compensatory-failure rate.

### 6.8 Anticipatory Stage H drafting-discipline note re sign-inversion pre-commit

Per [`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md) anticipatory-drafting-note discipline (same pattern §4.7 uses for the HA-P7 rolling-sum-predictor structural-autocorrelation flag). §6.6 exploratory data-availability probe surfaces a probable sign-inversion on both rest-adjacency directions (RR = 1.57 rest-after, RR = 1.86 rest-before) relative to the §3.7 pre-committed direction (rest-adjacent → LOWER crash rate). §3.9 confound 1 explicitly anticipates this pattern as the confounding-by-indication mechanism (rest-because-felt-bad enriches the rest-adjacent arm with crash-prone episodes).

**Anticipatory closure pathway**: if Stage D descriptive audit confirms the §6.6 exploratory sign-inversion — the rest-adjacent → HIGHER crash rate pattern, rather than the §3.7 pre-committed direction — any subsequent Stage H pre-registration on this test **must draft with sign-inversion as the pre-committed direction**. Reversing the direction pre-commit post-Stage-D without formal r-revision at this MD level would violate [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) descriptive-before-inference. Two acceptable closure paths:

- **(a)** Stage H drafts with the anti-committed direction (rest-adjacent → HIGHER crash rate) as primary, cites §3.9 endogeneity as the interpretive-caveat, and treats the mechanism-not-effect reading as the Stage H falsifier.
- **(b)** Stage D triggers a pre-Stage-H MD r2 revision that formally flips the §3.7 direction pre-commit; the r2 revision goes through fresh-session review before any Stage H pre-reg drafts.

Either closure preserves the descriptive-before-inference gate. The pattern to avoid: silently absorbing the Stage D sign-inversion into a Stage H pre-reg whose direction pre-commit reads as if it had always been the sign-inverted direction — that is data-driven-pre-commit, not descriptive-before-inference.

---

## 7. Compression and lock discipline

Producer-mode methodology MD per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). Lock discipline follows parent MD [`post_heavy_day_compensatory_rest.md` §12](post_heavy_day_compensatory_rest.md#12-compression-and-lock-discipline):

1. **Draft (this file, r1)**: producer-mode subagent draft with all inherited machinery propagated from parent Q24 MD LOCKED r1 (commit `58b7723`) + Stage -1 audit LOCKED r1 + Stage D descriptive audit LOCKED r4. Two new operand families defined (rest-adjacency + streak-length as crash-rate predictors); reframing of Q24.5 from unfalsifiable to testably predictive.
2. **Fresh-session `/research-methodology-review`**: reviewer-mode session (different Claude session, cold context) audits this MD against the CONVENTIONS §2.2 four-input bar + applicable 4-layer checklist items. Produces reviewer report at `docs/research/reviews/methodology-heavy_day_crash_risk_prediction-YYYY-MM-DD.md`.
3. **r2 lock with §3.6 compression**: reviewer fires absorbed inline per parent MD's compression discipline (mechanical clarifications, cross-cites, caveat additions); architectural changes escalate to r2-with-design-change and re-review.
4. **Stage D descriptive audit runs against r2-locked operand**: no Stage D output until the operand is locked.

**Compression rule** (inherited from parent MD): reviewer absorption at r2 is *mechanical* (clarifications, cross-cites, added caveats) NOT architectural (design changes). Any architectural change forces re-review before lock.

---

## 8. Lock log

| version | date | change |
|---|---|---|
| r1 | 2026-07-16 | Initial DRAFTED status. Producer-mode methodology MD for Q24 sub-part 5 (reframed from unfalsifiable to testably predictive rest-adjacency → crash-rate association) + consecutive-heavy-days-streak → crash-rate association. Inherits stratum + heavy-day definition + unit-of-analysis + comparator + pool-split machinery from parent Q24 MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1 (commit `58b7723`). New operand definitions: (a) `rest_day_p25` primary + `rest_day_class` sensitivity per [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair) definitional-pair discipline; (b) `streak_length` binned to `{1, 2, 3, 4+}` at episode-end unit. Primary outcome: `crash_in_5d` (episode-end + 5d window on `is_crash` column). Primary window: +5d (matches parent MD strict-clean +5d crash-rate signal of 17.3%). Statistical machinery: Fisher's exact + Wilson CIs + bootstrap B=10,000 + Cochran-Armitage trend test (streak-length) + RANDOM_SEED=20260716. Foreseen review trigger: rolling-window-predictor structural-autocorrelation flag per HA-P7 precedent + [`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md). Six confound classes pre-committed as caveat-class per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) (rest-day-choice endogeneity dominant; streak-length × intensity + × era confounds; baseline-drift on rest-day operand; rolling-sum-predictor autocorrelation; circularity with parent MD §3.5). Data-availability audit hooks §6 confirm sample viability: 314 episode-ends × 46 crash-in-5d gives a 14.6% base rate on the all-episodes pool; rest-adjacency prevalence 40-64% under primary p25 operand at K=1-3; streak-length bins 188/77/27/22 across L={1, 2, 3, 4+}. Sub-part 5 REFRAMED from Q24 MD §1.3 unfalsifiable framing to testably-predictive framing per §1.3 above; framing distinction load-bearing throughout §3.8. Awaiting fresh-session `/research-methodology-review` before lock. |
| r1 LOCKED | 2026-07-16 | Fresh-session methodology review absorbed from [`docs/research/reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md`](../reviews/methodology-heavy_day_crash_risk_prediction-2026-07-16.md) (verdict: DEFENSIBLE with revision). Five surgical patches applied per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations) compression discipline (mechanical clarifications only, no architectural change; causal-vs-predictive-associational framing per §1.3 preserved throughout). **Patch 1** (§3.5, review L2.2 substantive-partial): added stationarity-assumption paragraph at the primary-contrast level naming the 4-year LC-era pooling as a substantive assumption partially addressed by §5 confound 7 (era-stratified sensitivity) + §5 confound 3 (streak-length × era cross-tab); caveat-class per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) not correction pre-committed. **Patch 2** (§3.9 confound 1 + §3.6, review I2.1 + I1.1 + L3.5 substantive-partial): added confounding-by-indication epidemiological citation (Salas 2001; Kyriacou & Lewis 2016 *JAMA*) as the literature construct for the rest-day-choice endogeneity mechanism at §3.9 confound 1; added log-binomial / modified-Poisson regression state-of-art (Zou 2004 *Am J Epidemiol*) at §3.6 as the natural Stage H extension for covariate-adjusted RR estimation. **Patch 3** (§5 confound 7, review I4.2 + L3.2 substantive-partial): added does-not-apply-redirected-to-analogue documentation for CONVENTIONS §3.7 trajectory-detrend audit hook — binary-outcome contingency tests have no windowed-mean to detrend, so era-stratified sensitivity (§5 confound 7 + confound 3) is the analogue drift-correction mechanism; documents explicitly why parent MD's §7.11 pre-lock absorption is not mirrored here. **Patch 4** (§5 confound 6, review I3.6 minor): added Stage-S1-synthesis reporting-discipline closure — Stage S1 synthesis must pick one of {this MD, parent Q24 MD} as headline per Q24 sub-part and cite the other as complementary (shared crash-in-5d outcome sample means the two are NOT independent evidence at Stage S1 level). **Patch 5** (new §6.8, discretionary user-endorsed): added anticipatory Stage H drafting-discipline note re sign-inversion pre-commit — if Stage D confirms §6.6 exploratory sign-inversion, subsequent Stage H pre-reg must (a) draft with sign-inversion as pre-committed direction citing §3.9 endogeneity as interpretive-caveat, OR (b) trigger a pre-Stage-H MD r2 revision formally flipping §3.7 direction pre-commit; either closure preserves the descriptive-before-inference gate. Pattern to avoid: silently absorbing Stage D sign-inversion into a Stage H pre-reg whose direction pre-commit reads as if always sign-inverted. Preserved byte-identically: §1 purpose + scope + reframing note, §2 inheritance table, §3.1-§3.4 operand definitions + K-ladder + outcome, §3.7 direction pre-commit, §3.8 predictive-only discipline, §4 streak-length arc, §5 confounds 1-5, §6.1-§6.7 data-availability audit hooks (all counts, all 2×2 tables), §7 compression-and-lock discipline, §9 cross-references. **STATUS**: LOCKED r1 2026-07-16 post-review absorption. Stage D descriptive audit for §3 rest-adjacency + §4 streak-length is now unblocked. |

---

## 9. Cross-references

- Parent Q24 MD [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md) LOCKED r1 (commit `58b7723`) — inherited stratum, heavy-day definition, unit-of-analysis (episode-end gap=0), comparator (matched-ordinary), pool-split machinery (§3.5 compensatory-success vs compensatory-failure), overlap policies (§5.2), null-machinery discipline (§7.10), envelope-drift caveat (§10 caveat 8).
- Sister MD [`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md) (drafted in parallel 2026-07-16) — Q24 sub-part 3 phase-stratification + dose-response trajectory outcomes; complementary arc to this MD's categorical-outcome arc.
- [Stage -1 audit `analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md`](../analyses/descriptive/Q24-precursor-heavy-day-structure/audit.md) LOCKED r1 — episode-length distribution (§4), heavy-rate-by-year (§2), corpus summary (§1). Data-availability numbers in §6 reproduce §4 exactly.
- [Stage D descriptive audit r4 `analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md`](../analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md) LOCKED r4 — compensatory-failure sub-arm sample sizes (§3), crash-in-window base-rate anchor (16/125 at +3d; 9/52 at +5d).
- [`analyses/hypotheses/HA-P7/`](../analyses/hypotheses/HA-P7/) — predictive-classifier precedent (rolling-crash-count → crash; NOT-SUPPORTED). Rolling-sum-predictor structural-autocorrelation flag surfaced at result-review time per [`hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md) — transferred anticipatorily to §4.7 streak-length machinery.
- [`analyses/hypotheses/HA01c-effective-exertion-shock/`](../analyses/hypotheses/HA01c-effective-exertion-shock/) — predictive-classifier precedent for exertion-shock → crash.
- [`methodology/hypothesis_lock_process.md §4.6`](hypothesis_lock_process.md) — rolling-sum-predictor structural-autocorrelation factor-of-2 flag anticipatory-drafting-note discipline.
- [`methodology/permutation_null_block_length.md`](permutation_null_block_length.md) — E[L] block-length machinery + data-driven E[L]* diagnostic; §4.7 streak-length inherits.
- [CONVENTIONS §1.2, §2.1, §3.1, §3.3, §3.6, §4.2, §5](../CONVENTIONS.md) — producer-mode + descriptive-before-inference + personal-baseline + definitional-pair + named-counts + caveat-class + zero-vs-NaN discipline.

---

*Producer-mode methodology MD. Update when (a) the fresh-session review verdict lands and informs r2 compression, (b) Stage D descriptive audit results land (per-cell contingency + risk ratio + trend test outputs), (c) a downstream per-HA pre-registration draws the operand into an inferential test.*
