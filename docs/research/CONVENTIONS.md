# Research conventions — how we work in `docs/research/`

**Status**: working document. Locked 2026-06-13 from accumulated session
feedback. This file is the binding "how to work" reference for any
research-track session in this repo. It is distinct from
[methodology/methodology.md](methodology/methodology.md), which covers
*what the research artefacts mean*; this file covers *how the work is
organised and what to check before pressing run*.

Read this before:

- proposing a new hypothesis test,
- writing a new analysis script,
- editing a methodology MD,
- summarising or critiquing an existing result,
- pushing to a remote.

Scope: research only. App-engineering work in this repo (auth, Directus,
Fly) is governed by [.claude/conventions.md](../../.claude/conventions.md),
not this file.

---

## 1. The role split

Two distinct Claude-modes operate in this folder. The split is
load-bearing: mixing them collapses the peer-review check that the user
relies on.

### 1.1 Producer mode (Claude writes / edits / runs)

Producer mode applies to **infrastructure and descriptive layers** that
sit upstream of any hypothesis verdict. Claude writes, edits, runs, and
commits these:

- `pipeline/01_extract/` — raw → processed extractors (Garmin FIT, UDS,
  notes, calendar, PwC).
- `pipeline/02_label/` — triage and categorisation scripts.
- `pipeline/03_consolidate/` — `build_unified_dataset.py` and joiners.
- `pipeline/04_visualize/` — timeline rendering.
- `pipeline/audit_for_publication.py` — pre-push privacy gate.
- `DATA_DICTIONARY.md` — column-by-column schema.
- `methodology/*.md` — research methodology, calibration rules,
  operationalisation reasoning.
- `analyses/garmin_exploration/` — taxonomy, FIT exploration, the
  activity-labels spec, baseline-trajectory scripts.
- Descriptive analysis scripts (Layer 1-3 on `per_day_master.csv`) and
  their result docs.

### 1.2 Reviewer mode (Claude reads / critiques / explains, does NOT edit unless asked)

Reviewer mode applies to **hypothesis-test artefacts and synthesis
docs** that carry verdicts. A *different* agent (or the user with that
agent) writes these; Claude is independent peer reviewer:

- `analyses/hypotheses/HA*-*/hypothesis.md` (pre-registrations).
- `analyses/hypotheses/HA*-*/result.md` (verdicts).
- `analyses/hypotheses/HA*-*/test.py` (test scripts that produce a
  verdict).
- `analyses/hypotheses/_registry/` and `registry.md`.
- `RESEARCH-REPORT.md`, `RESEARCH-REPORT-ADDENDUM*.md`,
  `QUEUED-WORK.md`, `wiggers_*.md`.
- Cross-hypothesis `synthesis.md`-style docs.

In reviewer mode the job is:

- explain reported findings in plain terms,
- flag caveats, statistical fragility, multi-comparison concerns,
  methodological issues, overclaiming, missing sanity checks,
- monitor coherence across hypotheses and synthesis updates,
- separate *what the data shows* from *how it is being interpreted*,
- propose what would strengthen the finding (constructive, not just
  adversarial),
- never silently edit a reviewer-mode artefact; if a change is needed,
  recommend it in chat and let the user decide.

Push hardest where claims are strongest: headline verdicts, synthesis
reframes, cross-channel coherence claims.

#### Drafting under reviewer-mode-with-authorization

The default ("Claude does NOT edit reviewer-mode artefacts unless
asked") admits an exception: the user can explicitly authorize Claude
to **draft** a reviewer-mode artefact in a given session. This is the
practical pattern for pre-reg files where the operationalisation has
been worked through in chat — methodology MDs already approved,
register entries verified, constraint structure landed.

When Claude drafts a reviewer-mode artefact under authorization:

- The artefact carries an `## Authorship` block at the top recording
  the drafting session, the authorising user, and the date.
- The artefact is NOT considered locked until the user explicitly
  accepts. Before lock the file may be revised freely.
- After lock, the `/research-review` (or equivalent peer review) must
  run in a **different session** — a new conversation, no shared
  context with the drafting session. The fresh-session reviewer reads
  the artefact and the methodology MDs cold; that is the project's
  standard for peer-review independence on artefacts that Claude
  drafted.
- The review report's "Reviewer mode" line records this with the
  addendum *"Fresh session — no exposure to the drafting context;
  doc-only knowledge."*

This pattern preserves the peer-review check at the **session-context
level** when strict agent-identity separation isn't practical. Same
LLM, different conversation, doc-only knowledge for the reviewer.

Review reports themselves land in [reviews/](reviews/) — a 4-layer
checklist anchored in established standards (SCRIBE 2016, CENT 2015,
STROBE 2007, Daza 2018, WWC 2022 SCED, Natesan Batley 2023) plus
project-specific audit hooks from §3 of this doc. See
[reviews/README.md](reviews/README.md) for the layer structure,
inline-citation rules, and the verdict-must-be-reasoned spec. The
local PDFs of the inherited standards live in
[literature/methodology/](literature/methodology/).

### 1.3 When the split is ambiguous, ask

Edge cases (e.g. a methodology MD that supports a specific hypothesis,
an exploratory script that becomes a result) are decided by the user.
When uncertain, default to reviewer mode and ask.

---

## 2. Discipline gates (must hold before the next thing runs)

These are sequencing rules. They are not negotiable per-session because
they prevent self-confirming pipelines.

### 2.1 Descriptive before inference

Do not propose or start hypothesis testing (HA pre-registration, formal
discrimination tests, statistical inference) until all of:

1. **Data labeling rounds are complete** — per-day intensity triage,
   symptom categorisation refinements, quality reviews.
2. **Descriptive analysis of the consolidated corpus is done** — Layer
   1-3 characterisation, baseline trajectories, sensitivity blocks.
3. **Multi-source consolidation is in `per_day_master.csv`** — gevoelscore,
   per-day intensity, Garmin biometrics, PwC log, dossier events,
   crash/dip labels, v24 clause-level signals.

When a data-quality issue surfaces (e.g. misclassified rows) while a
hypothesis test feels ready, prioritise fixing the labeling layer.
Push back if a hypothesis-test step is proposed while data work is
still open.

### 2.2 Methodology MD before locking a major choice

Every major methodological decision needs a dedicated MD in
[methodology/](methodology/) *before* the choice locks:

- null-model construction (block length, permutation scheme),
- phase-boundary locking,
- train / validate splits,
- operationalisation choice (CCF lag windows, dose-response binning,
  composite weighting),
- validation strategy.

The MD reasons the choice from four inputs:

1. **Best-practices standards** in time-series research, statistics,
   and the relevant subdomain (PEM / autonomic / self-research).
   Anchor to current state of the art, not historical convention.
2. **Established literature** — cited *only* where the reference
   materially supports the choice. Never cite a paper because "they
   did it that way"; cite it because their reasoning, evidence, or
   simulation results bear on the choice. Each citation gets a
   sentence on what it actually contributes.
3. **Our own vision on tradeoffs** — explicit. State which dimension
   is being weighted (reproducibility vs honesty about n, power vs
   Type-I control, simplicity vs per-metric tailoring, etc.) and why.
4. **Our research limitations + objectives** — n=29 crash episodes,
   single subject, observational, multi-source. Decisions that
   ignore these constraints generalise badly.

The MD documents: alternatives considered, strengths/weaknesses of
each, the chosen path with explicit justification, and citations only
where they materially supported the choice.

Picking from a binary list of options in chat without this homework is
exactly the a-priori commitment we are otherwise disciplined against.

Small or clearly-bounded choices (file naming, plot colours, tmp paths)
do NOT need this. Apply only where the choice has cascading downstream
consequences for results.

### 2.3 Audit before push

Before any `git push` to a remote:

```bash
python docs/research/pipeline/audit_for_publication.py
```

- `[PASS]` → push is safe.
- `[FAIL]` → do not push. Investigate each finding. Either anonymise
  the offending file or extend the allowlist with a documented reason,
  then re-run.
- New files in sensitive paths since the last manifest update will
  flag as inventory drift. Either move them external, or — if safe by
  policy — run with `--update-manifest` to refresh the baseline.

### 2.4 Tracking-completeness sweep

Beyond-the-guide work is tracked across several homes that drift if
maintained by accumulation rather than reconciliation. The R36 history is
the cautionary tale: a locked+executed test (`post-crash-exertion-relapse`)
missing from the register entirely, one verdict (C4b) recorded three
conflicting ways, and a not-ready thread (`best-in-the-middle`) with no
queue entry — none caught by per-artefact discipline, all caught only by a
manual sweep. Four legs must stay in sync, with the test index as support:

- **Ledger** — [`personal_hypotheses.md`](personal_hypotheses.md): the `## P#`
  entries + the crosswalk table (P# ↔ site slug ↔ test-id ↔ R#/Q# ↔
  kind/stage). This is the **spine**; reconcile the others against it.
- **Stocktake** — [`STOCKTAKE.md`](STOCKTAKE.md) §2a (state-of-everything).
- **Queue** — [`methodology/queued_work.md`](methodology/queued_work.md) +
  [`QUEUED-WORK.md`](QUEUED-WORK.md) (not-ready work).
- **On-stage** — the site's `data/addendum-register.json` →
  `/workings/beyond-the-guide-register`.
- **Test index** — [`analyses/hypotheses/registry.md`](analyses/hypotheses/registry.md)
  §1a (`register:` provenance tag on every test).

**The invariant.** Every thread appears in the ledger + stocktake; every
not-ready thread (stage `idea`/`scoped`/`parked`) also in the queue; every
site-register item projects from a ledger thread; every hypothesis-test
folder carries a `register:` tag. The membership + numbering rules are
locked in
[`methodology/register_provenance_and_numbering.md`](methodology/register_provenance_and_numbering.md).

**One fact, one home.** A verdict / stat / status lives once (in its
`result.md` or its ledger row); every other home **links or is generated
from** it, never re-states it. Derived views (`kind`/`stage`, the site
export, stocktake summaries) are generated and marked do-not-hand-edit —
hand-authoring them is how drift starts (the C4b verdict recorded three
ways is exactly this failure).

**The gate.** Run the mechanical check before any push that touches the
register system, and periodically:

```bash
python docs/research/pipeline/tracking_completeness.py --site <path-to-site-repo>
```

`[PASS]` (0 errors) is the bar. Hard FAILs — ledger↔crosswalk↔stocktake
drift, an untagged test folder, an invalid/incomplete site register — block.
WARNs (an uncovered test folder, an unexpected guide-extension) want a human
glance; `--strict` promotes them to FAILs for a hook. Wire it beside the §2.3
privacy audit in the pre-push hook once the register system is load-bearing.

### 2.5 Parsimony — simpler model first, escalate only on earned lift

Prefer the simplest model that fits before adding structure. A more
complex model, metric, or latent construct must **out-predict the
simpler read it would replace** to earn its place, and you state that
bar *before* building it, not after. A well-powered null on the simple
model is a result, not a failure; structure that only fits better
in-sample buys overfitting, not insight, and n=1 with a low
residual-event rate cannot support elaborate models (cf. the ~4%
crash-PPV ceiling, K01/K02 small-N brittleness).

**Operationally:** descriptive before inferential (§2.1); a level/scalar
read before a rate/dynamical instrumentation; merge a new idea into the
existing construct before minting a parallel one (§2.4 drift rationale).
Precedent: HA-P7's "any latent accumulator must out-predict lagged
`gevoelscore`" bar; the resilience level-model and its descriptive layer
preceding any return-dynamics/CSD machinery.

---

## 3. Statistical hygiene — pre-flight audit hooks

These are the checks to run before pressing go on an analysis. Each
hook names the thing that goes wrong if you skip it.

### 3.1 Personal baseline, not absolute thresholds

For any PEM-pacing metric, work with deviations from the participant's
own rolling baseline rather than absolute cutoffs. A max HR of 130 is a
spike for one PEM patient and a calm afternoon for another.

- **Single-day metrics**: z-score against a 30-day rolling baseline.
  Median + MAD is preferred (robust to one zero-step day).
  `step_z_30d` is the prototype.
- **Track baselines explicitly**: a rolling-baseline trajectory across
  years is itself meaningful — it exposes envelope shifts the z-score
  cancels out.
- **Detect both PEM mechanisms separately**:
  - *Shock*: single-day z above some threshold (e.g. z ≥ 1.5).
  - *Push-crash*: sustained elevation. Rolling sum of positive z,
    consecutive above-baseline days, or 7-day moving average of z.
- **Lock z-threshold cutoffs to the same values across participants.**
  Let the baseline computation do the personalisation.
- **Sanity-floor exception only**: a small absolute floor to suppress
  noise (e.g. step spike requires steps ≥ 4000) is allowed. Document
  when used. Never use absolutes as classification cutoffs.

### 3.2 Lagged baseline for sustained-push hypotheses

For Wiggers and PEM-pacing analyses on `per_day_master.csv`, prefer
the v3.2 `_lagged` exertion variants over v3.1 — and prefer the
`_lagged_lcera` variant where it exists.

Rationale: the v3.1 `exertion_class` uses a 30-day *trailing* rolling
baseline that includes the candidate day itself. In sustained-push
periods the baseline creeps up with the pushes, so a slow grind
rebases into its own reference frame and stops looking heavy. v3.2
fixes this with a `[d-90, d-30]` window. The `_lcera` variant
additionally restricts the baseline to LC-era days only (dates ≥
2022-04-04), so pre-LC and corona days don't dilute the reference.

- Default to `_lagged_lcera` for PEM-pacing tests (gated on
  `lc_phase == "lc"`).
- Default to `_lagged` for cross-era trajectory work where the baseline
  *should* see pre-LC.
- v3.1 columns (`exertion_class`, `step_z_30d`, `push_burden_7d`) stay
  in the master for backward compatibility with HA01b / HA02c. Do not
  delete them. Do not silently substitute v3.2 in re-runs of those
  tests.

**Audit hook**: if a draft analysis touches `exertion_class`,
`step_z_30d`, `push_burden_7d`, or any non-lagged rank, stop and ask
whether the v3.2 lagged variant is what's meant.

The current canonical column lists live in
[DATA_DICTIONARY.md](DATA_DICTIONARY.md) and are kept current there;
do not maintain a duplicate list here.

### 3.3 One column per definitional pair

Five pairs on `per_day_master.csv` have Spearman ρ ≥ 0.97 on the LC
frame and effectively measure the same construct. Including both sides
inflates VIF, distorts coefficient interpretation, and double-counts
the signal.

Pick **at most one** column per pair when building any regression,
VAR, VIF analysis, or correlation matrix. The current ρ values and
the chosen-side rationale are annotated inline on each affected
column in [DATA_DICTIONARY.md](DATA_DICTIONARY.md) (search for
"feedback_definitional_pair_guardrail"). Default rule of thumb:

- prefer broader frame over narrower (e.g. `all_day_stress_max` over
  `awake_stress_max`),
- prefer delta-framed over level-framed when delta matches the
  hypothesis (e.g. `bb_overnight_gain` over `bb_during_sleep_value`
  for D2),
- prefer magnitude × duration integrals over duration-only when the
  hypothesis is about cumulative burden (e.g.
  `hr_area_above_daytime_baseline_waking_lcera` over
  `hr_min_above_daytime_baseline_plus_20_waking_lcera` for A4).

Surface the dropped column in the methodology of any downstream
result so the choice is auditable.

For the three ρ = 1.000 pairs, run a sanity check before declaring
the relationship strictly definitional: confirm in
`pipeline/03_consolidate/build_unified_dataset.py` (and upstream
extractors) whether the two columns share an identical computation
path. If yes, document as "definitional identity" and consider
dropping one from the master. If no, document the empirical
near-identity as a Layer 3 finding and keep both.

**Audit hook**: if a draft Layer 4 result includes both members of a
near-identical pair, stop and pick one.

### 3.4 Crash-drop sensitivity row on every Layer 4+ correlation

For every Layer 4+ correlation / CCF / regression that touches
PEM-pacing variables, run two frames in parallel:

- Full LC frame (or LCscore),
- Same frame with `is_crash == True` rows dropped.

Report both ρ values. If |Δ| > 0.10, surface as a finding — the crash
days are doing meaningful work and the result table must say so.

Do NOT silently drop crash days as a "cleanup" step. The contrast
itself is informative: on crash days the exertion-HR co-movement is
suppressed or reversed (typically low exertion at the time of the
crash with elevated RHR), which dampens the underlying "more push →
higher resting_hr" signal on the full frame.

Same logic for `is_dip` as a secondary sensitivity if a result is
borderline (n=130 dip-days on LC frame).

**Audit hook**: if a draft Layer 4 result table does not have a
crash-drop sensitivity row, stop and add one.

### 3.5 Spike-detecting metrics over daily averages

For sympathetic-arousal proxies (stress, HR, respiration), prefer
spike / peak / count metrics over daily means. A 5-minute spike of
intense stress in a 24-hour day is dilution-invisible to a daily
mean — and the user's lived-experience report is that exactly that
shape (intense moment in an otherwise calm day) can trigger a crash.

- `minutes with stress ≥ 75 per day` beats `averageStressLevel per
  day`.
- `max HR sample per day` or `count of HR spikes ≥ resting + 30 per
  day` beats `average HR per day`.
- `peak respiration sample` beats `average respiration`.

For body-battery, **per-minute resolution is required** and the
*count* of distinct BB-rise events is meaningful in itself — a day
with multiple distinct recoveries (afternoon nap, deliberate rest
periods) is qualitatively different from a day of continuous drain.
Daily aggregates (HIGHEST/LOWEST/MOSTRECENT) can describe at most
one transition and miss the multi-event story.

### 3.6 Name every count: \<n\> \<unit\> per \<scheme\> in \<file\>

Before stating any count of events (crashes, dips, episodes,
PEM days), name three things in the same sentence:

1. **Labeling scheme** — `crash_v1` vs `crash_v2`, `sub_threshold_dips`,
   etc.
2. **Unit** — day-level rows vs episode-level vs something else.
3. **Source file** — which CSV / table the count came from.

Bare numbers invite conflation across schemes that exist on this
corpus (e.g. `is_crash` day-count vs `crash_episode_id` episode-count
on the same labels). If the count came from an in-session query, also
state the predicate so the user can reproduce it.

Acceptable phrasings:

- "103 crash-days (crash_v2 day-level, `labels_crash_v2.csv`
  `label == 'crash'`)"
- "29 crash-episodes (crash_v2, `labels_crash_v2.csv` unique
  `episode_id` starting with `crash-`)"
- "35 sub-threshold dip-days (`sub_threshold_dips.csv`, `dip_type`
  non-null)"

For crash analyses, prefer episode count for per-event statistics —
consecutive days within an episode are autocorrelated, and treating
them as independent inflates the effective sample size. Use day-count
as a supplementary view.

### 3.7 Trajectory-detrend sensitivity for raw pre-vs-post comparisons

For any pre-vs-post window comparison on the LC corpus that compares
**raw channel values** (not z-scores against a lagged baseline), report
a **detrended sensitivity column alongside the raw test**. The
recovery trajectory documented in [`analyses/hypotheses/registry.md`](analyses/hypotheses/registry.md)
(crash frequency ~10/year in 2023-24 → ~2/year in 2025-26) leaks into
any raw pre-vs-post window comparison straddling its steeper sections;
without detrending, the analyst cannot distinguish an event-driven
step from a trajectory-coincidence step.

Procedure:

1. Fit a linear trend on the pre-window:
   `slope, intercept = np.polyfit(pre_x, pre_values, deg=1)` where
   `pre_x = days-from-event-date`.
2. Extrapolate the fitted line forward through the post-window.
3. Subtract the extrapolated line from both pre and post values.
4. Recompute the test statistic (Mann-Whitney U, t, or whichever) on
   the residuals.
5. Report both the raw `mw_p` (or analogous) and the
   `mw_p_after_linear_detrend` in the same row of the summary CSV.

A step that survives detrending is much more credibly event-driven.
A step that disappears under detrending was the underlying trend
leaking through.

**Scope:**

- **Applies to**: raw pre-vs-post Mann-Whitney / t-test / KS
  comparisons on day-level (or coarser) channels. Worked example:
  [`methodology/intervention_effects_descriptive.md`](methodology/intervention_effects_descriptive.md)
  §4 + §6 (`mw_p_after_linear_detrend` column + the
  `linear_detrend_on_pre` helper).
- **Does NOT apply to**: lagged-baseline z-score comparisons. The
  `_lagged_lcera` family already anchors the reference locally, which
  partly handles slow trend by construction. The baseline-shift
  question across the full trajectory is a separate concern handled
  by the segmented-baseline machinery if findings warrant.
- **Linear-on-pre-window form is conservative-against-event-effects**:
  a single fit on the pre window extrapolated forward gives
  event-effects less wiggle room to show up artificially than
  per-window fits would. Alternative forms (loess on the full window,
  piecewise) may suit specific cases but require a methodology MD
  justifying the choice.

**Audit hook**: any Layer 4+ raw pre-vs-post comparison on the LC
frame that does NOT report a detrended sensitivity is a fire. The
intervention_effects MD is the canonical worked example; the
`linear_detrend_on_pre` helper there is reusable verbatim.

**Empirical validation** (added 2026-06-14 post-Session-C). The
intervention_effects MD's Session C run produced exactly this
column for 31 analytical primary-buffer cells; see
[`methodology/intervention_effects_descriptive.md` §8.2](methodology/intervention_effects_descriptive.md#82-top-findings-at-primary-b14-sorted-by-r_rb).
Of the 7 raw-test findings with `|r_rb| ≥ 0.30`, **two were revealed
as trajectory artifacts** by the detrend column (`stress_mean_sleep`
× 2022-09-22 went from raw p<.001 to detrend p=0.62; `bb_overnight_gain`
× 2026-03-20 went from raw p<.001 to detrend p=0.96). Without §3.7
those would have been reported as event-driven step-changes. The
pattern is not hypothetical.

### 3.8 Boundary-spacing minimum for pre-vs-post window designs

For any analysis that compares pre-vs-post windows around a sequence
of boundary dates with a transition buffer `B`, the **inter-boundary
spacing must satisfy** `boundary_gap ≥ 2·B + min_window_days`. Closer
pairs are structurally unanalyzable: the post-window of one boundary
and the pre-window of the next are both truncated to nothing by
neighbour-truncation.

Procedure when locking a pre-vs-post design:

1. Compute the gap from each boundary to its nearest neighbour:
   `min(d - d_prev, d_next - d)`.
2. For each transition buffer `B` in the sweep, mark boundaries with
   `gap < 2·B + 5` as **structurally unanalyzable** at that buffer.
3. Report unanalyzable boundaries as **NaN rows** in the output CSV
   (with `n_pre`, `n_post` columns showing 0 or negative window-days)
   rather than silently omitting them.
4. If a boundary is unanalyzable at every buffer in the sweep, surface
   this in the findings section as a methodological-limitation finding
   (not just a missing row).

**Worked example**: [`methodology/intervention_effects_descriptive.md`
§2 truncation paragraph + §8.1](methodology/intervention_effects_descriptive.md#81-effective-analyzable-scope-5-of-8-boundaries-usable).
The 2024-04 cluster (Citalopram start 2024-04-09 and CPAP end
2024-04-16, 7 days apart) is structurally unanalyzable at every buffer
`B ∈ {7, 14, 28, 42}`. The pre-vs-post window design cannot resolve
their independent effects; an ITS-style co-modeled regression would
be needed (out of scope of Layer 1 descriptive). Treating the
unanalyzability as a finding rather than a gap is the discipline.

**Scope:**

- **Applies to**: any pre-vs-post window analysis with neighbour
  truncation, especially intervention-effect, regime-change,
  segmentation-validation, and dose-step designs.
- **Does NOT apply to**: continuous-covariate regressions (e.g.
  dose-as-continuous on a single period), or non-windowed designs.
  These have their own degrees-of-freedom constraints but not this
  one.

**Audit hook**: any methodology MD that locks a pre-vs-post window
design with a sequence of boundaries must report the boundary-gap
audit either as a section in the MD or as a column in the output CSV.
Silent dropping of close-spaced boundaries is a fire.

### 3.9 Curated-catalog discipline for heterogeneous annotated categories

When extracting analytical units (boundary dates, period spans,
event-class members) from a category in `annotations.yaml` (or any
heterogeneous annotated source), the catalog **must be curated
explicitly**; "data-driven, not pre-specified" is not enough when the
source category mixes semantically distinct entries.

The fire condition: an `interventie`-category entry, for example,
may be a steady-state therapeutic regime (citalopram), an ad-hoc
reactive use (naproxen-as-needed for hoofdpijn), an administrative
event (verwijzing huisarts), a wachtlijst-overbrugging
(fysiotherapie), or a single-session activity (breathwork). Each has
different step-change semantics — or none at all. Pulling all of
them into a step-change analysis produces noise plus spurious
"findings" on entries that don't represent step-changes at all.

Procedure when pulling from a heterogeneous annotated category:

1. **Inspect the raw list** before locking the catalog. List every
   entry, its dates, its source-document anchor. The user/researcher
   reviews.
2. **Identify the analytical question's semantics** explicitly (what
   shape of intervention this analysis can detect — e.g.
   "steady-state regime onset" excludes ad-hoc and single-session).
3. **Encode curation criteria** in the script. Either an exclude-list
   (substring match on labels, as in the worked example) or an
   include-list (more conservative; explicit allowlist of label
   keywords). Either is acceptable; the choice depends on whether
   "any new entry should auto-include unless excluded" or "any new
   entry should default-exclude unless allowlisted."
4. **Document the rejected entries with reasons** in the methodology
   MD's catalog section (NOT just code comments). The reader of the
   MD must be able to see why each excluded entry was dropped.

**Worked example**: [`methodology/intervention_effects_descriptive.md`
§2 "Excluded by label keyword"](methodology/intervention_effects_descriptive.md#2-interventions-in-scope--curated-catalog)
+ the `EXCLUDE_LABEL_KEYWORDS` substring filter in the script. Five
exclusions documented (`fysiotherapie`, `naproxen`, `breinvoeding`,
`verwijzing`, `breathwork`) with stated reasons; new `interventie`
entries auto-flow unless their label contains an exclude keyword.

**Scope:**

- **Applies to**: any methodology that pulls analytical units from a
  heterogeneous annotated category (`interventie`, `levensgebeurtenis`,
  `high_intensity`, `medical`, etc.).
- **Does NOT apply to**: per-day-master columns, hand-curated span
  files, or analytical-unit lists assembled outside `annotations.yaml`.

**Audit hook**: any methodology MD or script that loads from an
`annotations.yaml` category without an explicit curation criterion
(exclude-list or include-list with documented rationale) is a fire.
The original framing "the catalog is data-driven, not pre-specified"
is insufficient when the source category is heterogeneous; it must be
either "the catalog is data-driven AND the category is verified
homogeneous" or "the catalog is curated via these criteria."

### 3.10 Operationalisation faithful to the data, not just to the description

A column's stated semantics — its DATA_DICTIONARY description, or the
prose in an operationalisation methodology MD — can silently diverge
from what the value actually measures. This is distinct from §3.3 (two
columns colliding): here a *single* column's description is wrong, or an
inferred semantics doesn't hold. Two failure shapes, both observed on
this corpus:

- **Wrong noun.** `bb_during_sleep_value` was documented as "BB peak
  during the sleep window" but is the Garmin `DURINGSLEEP` stat = net
  change across the window (`SLEEPEND − SLEEPSTART`), verified identical
  on all 593 co-occurring days. A downstream "morning reserve" reading
  of it would have been backwards.
- **Inferred semantics that fit N=1 but fail the corpus.**
  `all_day_stress_avg` looked like a `totalStressCount`-weighted mean on
  one spot-checked day; across 1722 days it is a
  `stressIntensityCount`-weighted mean (valid epochs only), and the
  `totalStressCount` weighting fails on 914 days. A single-day check is
  not verification.

Highest-risk columns: any whose semantics were **inferred rather than
officially documented** (Garmin's internal UDS fields, any
reverse-engineered source), and any derived column whose description
names a *kind* of quantity (peak / mean / net-change / count / rate)
that a reader will build on.

Procedure before locking or relying on a column's description:

1. **Trace the computation path.** Read the extractor / build-script
   line that produces the column and confirm the description matches
   what the code actually computes — not what the column *name*
   suggests.
2. **Assert at least one identity or invariant on the whole corpus**,
   not a single day. Partition identities (`TOTAL == AWAKE + ASLEEP`),
   unit identities (`count × 60 == duration_seconds`), and definitional
   identities (`DURINGSLEEP == SLEEPEND − SLEEPSTART`) each pin down a
   distinct claim. State the day-count the identity holds on.
3. **Where the source is undocumented and no identity pins the
   semantics** (e.g. `averageStressLevelIntensity`, `totalStressIntensity`
   — sign conventions differ between aggregators on this corpus), mark
   the column unusable in the dictionary rather than guessing a
   definition. Do not build metrics on it.
4. **Record the verification** in the dictionary row / MD: the identity
   checked, the day-count, and whether the relationship is definitional
   or empirical.

**Worked example**: the 2026-07-15 UDS field-semantics pass —
[DATA_DICTIONARY.md](DATA_DICTIONARY.md) §7B preamble + the
`bb_during_sleep_value` / `all_day_stress_max` / `all_day_stress_avg`
row corrections; two Layer-3 ρ = 1.000 pairs promoted from "needs
verification" to "definitional" by exactly this procedure. The identity
checks are mechanizable (partition / unit / definitional invariants
asserted every build); the "wrong noun" half is not — an identity check
won't flag a mislabelled quantity, so the computation-path read stays a
human/LLM step.

**Scope:**

- **Applies to**: any DATA_DICTIONARY row or operationalisation
  methodology MD, especially inferred-semantics / reverse-engineered
  source fields and derived columns whose description names a
  quantity-kind.
- **Does NOT apply to**: raw pass-through columns whose source field is
  officially documented and whose description quotes that documentation
  verbatim (the description is the source's own).

**Audit hook**: a dictionary row or operationalisation MD that describes
a *kind* of quantity (peak / mean / net-change / count / rate) for an
inferred-semantics field, without a computation-path trace and at least
one corpus identity check, is a fire. A single-day spot-check standing
in for a corpus identity is a fire.

---

## 4. Stay close to the data — defer interpretation

A consistent failure mode in n-of-1 research is overlaying interpretive
framing on layers that should stay raw. These rules keep the
descriptive layer clean enough that fresh statistical work isn't
contaminated by prior reads.

### 4.1 No interpretive marks on raw or descriptive layers

When adding `event_labels` or `annotations.yaml` entries: describe
events that occurred (vacation, illness, intervention). Never imputed
states or reactions ("post-dx stress reaction", "crash recovery
period").

When writing methodology / audit docs: frame device or pipeline
behaviour structurally ("Garmin flags sustained low-motion as sleep
onset"), not interpretively ("user was in a collapse state"). Note
co-occurrence with crash labels as a pattern, not as evidence of
mechanism.

When tempted to add a causal / mechanistic explanation
("SSRI-related bradycardia is plausible", "fitness-driven deep-sleep
HR floor"), check whether the surrounding context (umbrella labels,
era, neighbouring `event_labels`) already conveys the temporal frame.
If yes, do NOT add the imputed mechanism.

Reserve causal claims for explicit hypothesis-testing layers — not for
descriptive or methodology docs.

### 4.2 Caveats yes, a-priori claims no

When sweeping a doc for an unsupported framing (seasonality,
trajectory, mechanism), every occurrence falls into one of two
classes:

- **Caveat-class (KEEP)**: "Distributions are NOT corrected for X" /
  "X is not controlled for in the original analysis" / "absolute
  values are meaningless across X". Honest acknowledgment that X
  exists as an uncorrected confounder. Does not claim X drives
  outcomes.
- **A-priori-class (CUT)**: "Use X-decomposition methods" / "stratify
  by X-phase" / "the post-X stretch". Presupposes X matters before
  any test has run. Lifts X from confounder-acknowledgment to
  analytical basis.

Removing caveats is revisionist (loses the audit trail of what the
original analysis did not control for). Keeping a-priori framing is
data-peeking (builds methodology on a phenomenon that has not been
independently established).

Default to KEEP when uncertain. Revisionism is a worse failure mode
than over-acknowledging caveats.

### 4.3 Prior-driven hypotheses are confirmatory, not exploratory

Data-peeking concern applies when the hypothesis was generated *from*
looking at the data. When a hypothesis has independent prior sources,
in-corpus descriptive observation is *corroboration of a pre-specified
prior*, not *origination of a post-hoc claim*. In that case the test
on the same data can be framed as confirmatory.

Before flagging data-peeking on an n=1 corpus, ask three questions in
order:

1. Would the user have hypothesised this BEFORE looking at the data?
   Evidence: lived experience that pre-dates the analysis, prior
   conversations, prior notes, prior literature reading.
2. Does the hypothesis have published-literature support that
   establishes its plausibility without reference to this corpus?
3. Is there a mechanistic argument that motivates the direction
   independent of any data look?

If any one is yes, the hypothesis is prior-driven. Confirmatory
framing is justified. Walk-forward discipline becomes a nice-to-have
for magnitude calibration, not a credibility requirement.

If all three are no, the hypothesis was genuinely generated post-hoc
and the exploratory caveat applies.

### 4.4 v24 + per_day_intensity are presence-conditioned

The v24 clause CSV is a **presence-conditioned positive evidence
layer**, NOT a symptom-prevalence panel.

Use for:

- categorising days that have notes by what they contain,
- stratifying other independently-defined day-classes (crash
  episodes, PwC ziek-days, Garmin-firing days) by clause content,
- high-specificity precursor flags for hypothesis tests.

Do NOT use for:

- plotting illness trajectories (rate of mentions ≠ prevalence),
- estimating "how often was the user fatigued in 2024 vs 2023"
  (mention rate confounded with note-writing rate),
- validating Garmin nulls (absence of mention is not evidence of
  symptom absence).

For trajectories, use **daily-computed signals** instead —
`gevoelscore` (user logs each day) and Garmin biometric channels
(objective sensor data).

`per_day_intensity` is also presence-conditioned. Its loads derive
from upstream calendar events + notes; a blank `cog_load` doesn't
mean cognitive intensity was zero, it means no signal was found to
assign one. Gate on `intensity_source != ""` before interpreting.
`bulk_triage_*_no_info` = explicit absence by review, distinct from
empty source = not yet triaged.

In `per_day_master.csv`: presence-conditioned columns are NaN when
`has_note == False`, not 0. `has_note` is the mandatory companion to
any v24-derived column.

Full schema in [DATA_DICTIONARY.md](DATA_DICTIONARY.md); the
operational rules above supersede the framing in older memory entries.

---

## 5. Project-wide anchors (read once, then trust)

These anchor every analysis. They live in canonical files; this
section just points at them so a session can warm up without having to
rediscover.

- **Long COVID timeline** — pre_corona < 2022-03-21; corona infection
  2022-03-21 → 2022-04-03; LC ≥ 2022-04-04 (Monday after Fietsweekend
  Ardennen, more factual than the formal dx 2022-05-06). Surfaces as
  `lc_phase` column. Constants:
  - `LC_ERA_START = date(2022, 4, 4)` in
    [pipeline/03_consolidate/build_unified_dataset.py](pipeline/03_consolidate/build_unified_dataset.py#L106),
  - `LCERA_START = date(2022, 4, 4)` in
    [analyses/garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py](analyses/garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py).

- **Default analysis window**: 2022-09-03 → present (post-gevoelscore
  overlap). Pre-2022-09 Garmin data may be referenced for
  baseline-shift / calibration cards, never used as a label source.

- **Garmin extraction window**: every new
  `pipeline/01_extract/garmin_*.py` script sets the start-date filter
  to **2021-08-16** (earliest GDPR-dump date). This covers two real
  gains: pre-LC baseline characterisation, and 2022Q3-Q4 v3.2 lagged
  gap closure. Trade-off accepted: HA01b / HA02c results computed on
  the pre-Wave-3 master will not reproduce bit-identical against the
  rebuilt master. The v3.1 reproducibility shift for those ~30 leading
  days is tolerated.

- **Garmin investigation lives at**
  [analyses/garmin_exploration/](analyses/garmin_exploration/) and
  related folders. Scripts read directly from the GDPR dump at
  `$GEVOELSCORE_DATA_PATH/raw/garmin/`; output CSVs are checked in for
  review and reproducibility.

- **Shared FIT timestamp_16 resolver**:
  [analyses/garmin_exploration/scripts/fit_utils.py](analyses/garmin_exploration/scripts/fit_utils.py),
  `Monitoring16Resolver` class. Import it — never re-implement inline.
  Three things bite if you try: timestamp_16 is FIT-epoch not Unix
  (1989-12-31), fitdecode does not auto-resolve, and the rolling
  reference must update on every resolve.

- **Sources of truth for column lists, near-identical pairs, and
  variant families**: [DATA_DICTIONARY.md](DATA_DICTIONARY.md). When
  in doubt, read the dictionary at the head of the master CSV, not a
  memorised list.

---

## 6. The research workflow at a glance

This is the implicit flow that has emerged across the project. It is
not yet a slash command (see §7); the table here exists so a fresh
session knows where it is in the sequence.

| stage | output | gate to next |
|---|---|---|
| 1. Question | a one-sentence framing | independent prior motivation (lived experience, literature, mechanism) named |
| 2. Labeling | crash/dip labels, v24 clauses, per-day intensity, manual triage | all current rounds complete, no open quality reviews |
| 3. Consolidation | `per_day_master.csv` rebuilt | `pipeline/03_consolidate/build_unified_dataset.py` runs clean |
| 4. Descriptive | Layer 1-3 cards: distributions, baselines, sensitivity blocks | descriptive layer settled; results not contradicted by data-quality flags |
| 5. Methodology MD | a dedicated `methodology/*.md` doc with four-input reasoning (§2.2) | user reviews and accepts the reasoning |
| 6. Pre-registration | `analyses/hypotheses/HA*-*/hypothesis.md` (reviewer mode artefact) | user / producer agent signs off |
| 7. Test | `analyses/hypotheses/HA*-*/test.py` + result data in `$GEVOELSCORE_DATA_PATH/analyses/hypotheses/` (reviewer mode artefact) | test produces a result file Claude can read |
| 8. Result | `analyses/hypotheses/HA*-*/result.md` (reviewer mode artefact) | passes audit hooks §3.1-§3.6 |
| 9. Synthesis | `RESEARCH-REPORT-ADDENDUM*.md`, registry updates (reviewer mode artefact) | passes pre-publication audit §2.3 |
| 10. Push | `python pipeline/audit_for_publication.py` then `git push` | `[PASS]` |

Stages 1-5 are **producer mode** (§1.1). Stages 6-9 are **reviewer
mode** (§1.2). Stage 10 applies to both.

---

## 7. What still needs to land

- **`/research-review` slash command** — built 2026-06-13; walks
  the 4-layer checklist in [reviews/README.md](reviews/README.md)
  against a target doc and produces a dated review report.
- **`/research-methodology-review` slash command** — built
  2026-06-14; sister to `/research-review`. Audits a methodology
  MD against §2.2's four-input bar (best-practices standards,
  literature, tradeoff vision, limitations + objectives) plus
  applicable layer items, with type-A (by-MD-type) and type-B
  (cross-cutting) methodology-specific element checks. Produces a
  dated report at `reviews/methodology-<slug>-YYYY-MM-DD.md`.
- **`/research-methodology` slash command** — scaffolds a *new*
  methodology MD per §2.2 with the four-input reasoning template.
  Not yet built (distinct from the review command).
- **Memory pruning** — done 2026-06-14. Fifteen cluster-A / cluster-B /
  cluster-C / role-split memory files collapsed to four one-line
  pointers in `MEMORY.md`, each pointing back to this doc. Memories
  that stay as-is: lived-experience anchor
  (`project_crash_triggers_user_experience`), tooling references
  (`reference_fit_timestamp16_resolver`, `reference_garmin_research_folder`),
  audit-before-push script gate (`feedback_audit_before_push`),
  held-out-structure framing (`project_garmin_research_bias_boundary`).

---

## 8. Cross-references

- [README.md](README.md) — repo orientation, environment setup, folder
  map, privacy boundary.
- [methodology/methodology.md](methodology/methodology.md) — research
  methodology (load scale, triage rules, work-vs-state lens,
  presence-conditioned framing).
- [methodology/symptom_mention_asymmetry.md](methodology/symptom_mention_asymmetry.md)
  — binding rule for note-derived columns.
- [methodology/nightly_attribution.md](methodology/nightly_attribution.md)
  — binding rule for sleep + RHR dating.
- [methodology/garmin_indicators_audit.md](methodology/garmin_indicators_audit.md)
  — Garmin per-column provenance.
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) — every column with source,
  dtype, missingness, and variable class (daily_computed vs
  presence_conditioned_positive_evidence).
- [.claude/conventions.md](../../.claude/conventions.md) — sister
  document for app-engineering work in this repo. Not in scope here.
