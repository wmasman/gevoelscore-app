# Descriptive precondition audit — Stage D guide

**Status**: **LOCKED r2** by user acceptance 2026-06-24. r1 authored
2026-06-24 by a fresh agent per §11 step 6.1 of
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
(r5 LOCKED 2026-06-24). r1 → r2 absorbed a fresh-session
`/research-methodology-review` (verdict REVISION RECOMMENDED, report
at [`reviews/methodology-descriptive_precondition_audit-2026-06-24.md`](../reviews/methodology-descriptive_precondition_audit-2026-06-24.md))
that caught three required actions (L-ID citation tension between
§2 and limitations doc r3 §5; label-count + plan §3.5 violation
around the structurally-untestable fourth label; figures/ vs plots/
naming collision) and ten recommended actions. All 13 absorbed in
r2; user accepted r2 directly (no second-pass review per established
pattern). Implementation proceeds to §11 step 6.2 (guide #2
`verdict_to_inference.md`).

This guide is the first of six binding methodology MDs for the
results-analysis layer. It governs **Stage D** (descriptive
precondition audit): the per-HA artefact that backstops a verdict's
load-bearing assumptions before any interpretation is built on it. It
sits between the HA's locked `result.md` and Stage I's
`interpretation.md`, and it refuses to mark a verdict TRUSTED when an
assumption the test relies on has no descriptive evidence behind it.

---

## 1. Purpose

> **Before any interpretation is built on a verdict, prove the
> verdict's load-bearing assumptions held.**

Statistical interpretation piggybacks silently on assumptions: block-
length validity, era integrity, sample-size adequacy, missingness
pattern, presence-conditioned semantics for v24 derivatives,
distributional shape where tests are non-rank-based, nightly
attribution for sleep-derived signals, train/validate split discipline
where a split is used. When an assumption is silently violated, the
verdict is **structurally untrustworthy** — independently of the
internal logic of the test that produced it. Stage D exists so that
Stage I never operates on a verdict whose load-bearing assumptions are
unbacked.

The Stage D artefact is **not a re-test**. It does not re-run the HA.
It does not produce a new verdict on the underlying hypothesis. It
does one job: enumerate the test's load-bearing assumptions, walk
each one against existing descriptive evidence (or the absence
thereof), and emit a verdict-trust call —
**TRUSTED / DOWNGRADED-INCONCLUSIVE-PROVISIONAL /
REQUIRES-DESCRIPTIVE-WORK / STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED** —
that Stage I will read as a gate.

**Precondition: the `/research-interpret` skill must land first.**
This guide specifies *what* a Stage D audit must do; it does not
specify *how* the skill produces one. Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§11 step 7, the `/research-interpret` skill is built after the six
guides (this guide is #1 of six). **No Stage D audit artefact can be
drafted before §11 step 7 lands** — this guide alone is necessary
but not sufficient. The §9 agent-instruction outline below is the
skill's brief; the skill build (step 7) operationalises it.

**Where Stage D sits in the layer.** Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3 stage-map: `D → I → S₁ → S₂ → A → T`. Stage I refuses to start on
an HA whose `descriptive_audit.md` is missing or whose verdict-trust
call is REQUIRES-DESCRIPTIVE-WORK. Stage D is the layer's first
discipline gate; every downstream stage inherits its precondition
discipline.

**What Stage D does NOT do.**
- It does not produce commentary (§3.12 commentary lives at Stage A
  and Stage T patient-audience-track only; Stage D outputs carry no
  commentary).
- It does not produce predictive-quality measures (PPV / base-rate
  framing per §3.10 is Stage A territory; Stage D measures only
  assumption-backstop status).
- It does not invent caveats post-hoc. Stage D reads what the HA's
  pre-reg and methodology MDs declared to be load-bearing and checks
  whether each declared assumption has descriptive backing.

**Alternatives considered** (per CONVENTIONS §2.2 four-input bar
item 3: tradeoff vision). The natural alternative is to fold the
descriptive backstop check into each HA's `result.md` § as a self-
audit. That was rejected for two reasons: (a) self-audit by the same
session that ran the test is structurally weaker than a separate
audit-artefact step (same-session blind spots — the limitations doc's
L4 mitigation reach applies); (b) per-HA self-audit makes
commensurability across HAs harder — the same eight-item checklist
applied uniformly across the corpus is the cheap commensurate
discipline. A second alternative — folding everything into the
stocktake without a per-HA audit-artefact step — was rejected because
the stocktake is a precedent run; per-HA audits inherit and refine,
but the stocktake cannot stay in lockstep with HAs that re-lock or
add operationalisations. The per-HA audit-artefact pattern matches
the limitations doc and synthesis-structure map shape: one MD per
binding decision, lock log per revision.

## 2. Inputs

The audit MUST load and use the following inputs, in this order:

1. **The target HA's locked `hypothesis.md`** — in particular §1 /
   §2 (predicted-direction claim), §4 (operationalisation), §7
   (locked-decisions block where present), §8 (caveats). The pre-reg
   declares which assumptions the test rests on; the audit checks
   each against descriptive evidence.
2. **The target HA's locked `result.md`** — the headline verdict, the
   per-cell n that was reported, any §-routing language the result
   used (e.g., HA-C4 v2's §5.3 INCONCLUSIVE-aware triad routing).
   The audit checks against what was actually reported, not what was
   intended.
3. **The methodology MDs the hypothesis cites** — in particular the
   five that bind the §5 checklist below:
   [`permutation_null_block_length.md`](permutation_null_block_length.md),
   [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md),
   [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md),
   [`nightly_attribution.md`](nightly_attribution.md),
   [`train_validate_split_fate.md`](train_validate_split_fate.md).
   These declare the operational tests the audit MUST apply per
   assumption type.
4. **The HA's `test.py`** — to enumerate which assumptions the code
   path actually relies on, not just which the prose claims. Prose-
   declared assumptions and code-relied assumptions can drift; the
   audit cross-checks.
5. **The corpus's existing descriptive artefacts** — `analyses/descriptive/`
   (per-channel ACF / E[L]\* runs, missingness audits, trajectory
   analyses), `analyses/garmin_exploration/cards/` (per-verdict
   statistics, cross-channel correlations), and the
   `methodology/*_descriptive.md` MDs (e.g.
   [`lc_phase_descriptive.md`](lc_phase_descriptive.md),
   [`intervention_effects_descriptive.md`](intervention_effects_descriptive.md))
   that pre-answer Stage D questions for whole channel families.
6. **The stocktake**
   [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md) —
   for HAs in the stocktake's per-HA matrix (§2), the precedent
   assumption-cell assignment (B / N / / per A1-A8) is the starting
   point for the audit; the audit confirms or revises but does not
   silently diverge.

The audit MUST cite the layer-level
[`research_line_limitations.md`](research_line_limitations.md) at the
two structural points where the §5 checklist depends on its L-IDs:

- **§5.2 (A2 missingness) cites L7** (survivorship) — the missingness
  check is the audit-layer manifestation of the L7 systemic limitation.
- **§5.5 (A5 v24 presence-conditioned) cites L5** (presence-conditioned
  data layer) — the v24 check is the audit-layer manifestation of L5.

This is per [`research_line_limitations.md`](research_line_limitations.md)
§5 row for `descriptive_audit.md`: *"Cite L5 and L7 explicitly where
the audit's checklist depends on them (the §6.1 v24-presence-
conditioning item maps to L5; the §6.1 missingness item maps to L7)."*

Beyond L5 + L7, the audit does not cite further L-IDs in its own
output — the broader systemic citation discipline (L1 + L2 + L4
mandatory at topic-level, all-seven at construct-level) attaches to
downstream reviewer-mode artefacts (interpretation, synthesis,
contextualisation, actionability, translation), not to the audit
artefact. The audit is producer-mode infrastructure backstopping the
HA's load-bearing assumptions; the limitations citations downstream
build on what the audit established.

## 3. Output

The audit produces exactly one artefact per HA:

```
docs/research/analyses/descriptive/HA-XX/descriptive_audit.md
```

**Folder convention.** One folder per HA, named with the HA's exact
registry ID (e.g. `HA-C3`, `HA-C4c`, `HA11-bout-redo`, `HA-P7`). For
HAs with sister-HA companion structure (e.g. HA-C3 v2 + HA-C3p, where
HA-C3p is the personal-baseline sister to HA-C3 v2's Wiggers-verbatim
operationalisation), each HA gets its own audit folder; sister-HAs
are not merged into one audit. For HAs with revision history (e.g.
HA-C3 v1 superseded by v2), the audit covers the **currently locked**
revision; superseded revisions do not receive audits unless explicitly
requested.

**Naming convention.** The artefact is always `descriptive_audit.md`.
No version suffix on filename; revision history lives in the file's
own lock log (per §11 below).

**Optional plots subfolder.**

```
docs/research/analyses/descriptive/HA-XX/plots/
```

The artefact MAY accumulate supporting plots here (per-channel ACF
plots, missingness heatmaps, per-cell n bar charts). Plots are
optional — most audits will not need them — but when they exist they
live under the HA-XX folder, not in the broader `descriptive/`
hierarchy. The plots are audit-class context; they do not stand on
their own and they do not propagate to Stage I. The `plots/` naming
matches sibling-consistent existing descriptive analyses
(`analyses/descriptive/operationalisation_support/.../plots/`,
`analyses/descriptive/trajectory/.../plots/`).

**Mode.** The artefact is **producer-mode** per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§4 (producer/reviewer split table). It is drafted by Claude under
user interview via the `/research-interpret descriptive HA-XX` skill
invocation. It does NOT receive a fresh-session `/research-review`
pass — it is an audit, not a verdict, and the producer-mode discipline
plus user explicit acceptance per §3.8 completion criteria is the
binding completion event.

## 4. Section outline for the produced `descriptive_audit.md`

The artefact MUST contain five sections in this order. Each section's
operational guidance follows.

### 4.1 Section 1 — Target HA + result reference

Mechanically copy from the HA's pre-reg + result:

- HA ID (e.g. `HA-C3 v2`), pre-reg lock date, result lock date.
- Headline verdict from `result.md` (verbatim; no re-labeling).
- Effective n on the primary cell (verbatim from `result.md`; do not
  recompute).
- Operationalisation summary (one sentence, copying §4 of the
  pre-reg).
- Methodology MDs cited by the pre-reg (link list).

This section is a header, not analysis. Its purpose is to fix the
target so the rest of the audit is unambiguous about which artefacts
it audits.

### 4.2 Section 2 — Load-bearing assumptions enumerated

One row per assumption. Each row carries:

- **Assumption** — one-sentence statement (e.g. "Block-length E[L]=7
  is appropriate for the autocorrelation structure of
  `all_day_stress_avg` on Stratum 4").
- **Source** — which doc/section declared this assumption to be
  load-bearing. Three valid sources, in order of authority:
  1. **Pre-reg §X** — the HA's `hypothesis.md` declared the
     assumption.
  2. **Methodology MD §Y** — a binding methodology MD declared it
     for the channel class / test type (e.g.
     `permutation_null_block_length.md` §1 for any HA running
     block-permutation).
  3. **`test.py` line range** — the code path relies on the
     assumption even when prose did not declare it explicitly. Audit
     MUST surface these cases.

The enumeration MUST include the eight checklist items in §5 below;
HA-specific assumptions beyond the eight (e.g. cross-phase pooling
discipline for HA-C4c per
[`phase_axis_collapsibility_conventions.md`](phase_axis_collapsibility_conventions.md))
are appended as additional rows.

### 4.3 Section 3 — Per-assumption status

For each row in §2, exactly one of three status labels:

- **BACKSTOPPED** — the assumption has descriptive evidence behind it
  on the cells the test actually used. The row MUST cite the path of
  the descriptive artefact and (when the artefact does not exhaust the
  cells) name the cells it covers. "BACKSTOPPED via methodology MD"
  (e.g. A4 era-Stratum-4 binding) is acceptable when the MD documents
  the operational consequence binding across all HAs and the pre-reg
  explicitly cites it. "BACKSTOPPED partial" is permitted when the
  artefact covers the underlying channel but the test uses a
  derivative (per the stocktake §7 "B partial" convention) — the row
  MUST name what the partial coverage entails.
- **NOT BACKSTOPPED** — descriptive evidence is missing, or the
  artefact that would close the assumption does not exist. The row
  MUST name what artefact would close it and what its acquisition
  path is (per §5's operational tests below). This row maps directly
  to an entry in the §4.5 `open_inputs` block.
- **NOT APPLICABLE** — the assumption does not apply to this HA (e.g.
  A5 v24-presence-conditioned semantics is NOT APPLICABLE for any HA
  whose primary signals are `daily_computed` per
  [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md)
  taxonomy; A8 split-fate is NOT APPLICABLE for HAs that use
  single-pool primary). The row MUST name the reason (one sentence).

**Hard rule on the BACKSTOPPED label.** A BACKSTOPPED status MUST cite
a specific path. "BACKSTOPPED by inspection of result.md" is forbidden
— that is the anti-pattern §7 explicitly rules out ("The test ran,
therefore the assumptions held"). The descriptive evidence must exist
as a separate artefact (descriptive run, methodology MD, garmin-card
analysis); citing the test's own result is circular.

### 4.4 Section 4 — Verdict-trust call

Exactly one of **four labels**, with rationale paragraph:

- **TRUSTED** — every load-bearing assumption is BACKSTOPPED (or NOT
  APPLICABLE with documented reason). Stage I may proceed.
- **DOWNGRADED-INCONCLUSIVE-PROVISIONAL** — at least one load-bearing
  assumption is NOT BACKSTOPPED, AND the gap is closable (the
  artefact that would close it can be produced; it just does not
  exist yet). Stage I MAY proceed under explicit user acceptance of
  the PROVISIONAL flag (per §6 conflict rules below), with the
  interpretation flagged accordingly and the claim narrowed at most
  one tier per plan §3.5 "always at most one tier narrower than the
  claim being blocked." The expected path is to close the descriptive
  gap first; PROVISIONAL is the fallback when the user accepts the
  inference under explicit narrower-claim discipline.
- **REQUIRES-DESCRIPTIVE-WORK** — at least one load-bearing
  assumption is NOT BACKSTOPPED, AND the cheapest acquisition path is
  meaningful work (the audit's §4.5 names the work). Stage I is
  blocked until the gap closes; the audit explicitly refuses to mark
  TRUSTED.
- **STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED** — at least one
  load-bearing assumption is NOT BACKSTOPPED **because the data the
  test would need does not exist** (e.g. H03b's INCONCLUSIVE × 12 by
  n_clean ≥ 10 not met at the gated resolution). The §4.5
  `open_inputs` block is still required and names the unblock pathway
  (revise pre-reg, retire, or shelve-blocked per stocktake §9.1 D1
  decision-precedent). Stage I is blocked until the pre-reg is
  revised, retired, or unblocked. See §6.2 for routing detail.

### 4.5 Section 5 — `open_inputs` block

Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.5, every NOT-BACKSTOPPED row in §3 maps to one entry here. Each
entry MUST name:

1. **What is missing** — the descriptive artefact, the
   methodology-MD section, or the per-cell run that does not exist.
   Use specific paths and column names; do not say "more descriptive
   work."
2. **What it is blocking** — typically Stage I on this HA; sometimes
   downstream Stage S₁ on a cluster the HA participates in (per the
   synthesis-structure map at
   [`synthesis_structure_map.md`](synthesis_structure_map.md)).
3. **Cheapest acquisition path** — which script under
   `analyses/descriptive/` to run, or which new script to write, with
   effort estimate (S ≤ 2h, M = 3-8h, L > 8h per the stocktake §3
   convention). When the path is a `/fetch-paper` call for a missing
   literature anchor, name the reference and route to
   [`_pending_literature_fetch.md`](_pending_literature_fetch.md).
4. **Fallback claim available without it** — always at most one tier
   narrower than the claim being blocked, per
   [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
   §3.5 "Hard rule" on no-silent-degradation. If no fallback is
   available, name that explicitly.

The skill aggregates these entries across all per-HA audits into the
layer-wide `docs/research/methodology/_open_inputs.md` queue. The
audit's per-HA entries are the source rows; the queue is the
aggregate.

## 5. The load-bearing-assumption checklist

The audit MUST tick (BACKSTOPPED / NOT BACKSTOPPED / NOT APPLICABLE)
each of the following eight items. The eight cover the
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§6.1 sketch verbatim; each item below names its binding methodology
MD and the one-sentence operational test that the artefact-drafter
will apply.

### 5.1 A1 — Sample size

> **Sample size on every reported cell ≥ pre-registered floor.**

**Binding doc.** The HA's own `hypothesis.md` §4 (operationalisation
floor) or §7 (locked-decisions block where present).

**Operational test.** For every cell `result.md` reports a per-cell
statistic on, check that the cell's n is ≥ the floor the pre-reg
declared. Where the pre-reg uses INCONCLUSIVE-aware routing (e.g.
HA-C4 v2 §5.3), the routing IS the backstop — the audit marks
BACKSTOPPED and names the routing.

**BACKSTOPPED looks like.** "n=581 effective on the unmedicated
primary cell ≥ pre-reg §4.1 floor of n=200, per `result.md` Table 2".

**NOT BACKSTOPPED looks like.** "n=5 episodes on `bb_overnight_gain`
sub-cell, below the pre-reg's implicit n ≥ 20 floor; no design-level
small-n absorption per pre-reg §X."

**NOT APPLICABLE looks like.** "HA is Layer-1 descriptive (HA-P6 v3);
the per-channel small-n is itself the finding, not a sample-size
failure" — but only when the pre-reg explicitly declared this design.

### 5.2 A2 — Missingness pattern

> **Missingness pattern is MCAR/MAR-compatible with the test, OR a
> missingness-aware operationalisation was used and is documented.**

**Cites L7 (survivorship)** from
[`research_line_limitations.md`](research_line_limitations.md). The
missingness check is the audit-layer manifestation of the L7
systemic limitation (only days where data was collected appear in
analytical n; missingness is not random for some signals). Every A2
finding gets recorded with explicit L7 attribution in the audit's §3
row: "A2 BACKSTOPPED — cites L7 (survivorship): [artefact-path]
shows per-channel missingness rate within MCAR/MAR-compatible
bounds."

**Binding doc.** Pre-reg §4 (operationalisation) plus the
checklist's missingness-audit expectation plus
[`research_line_limitations.md`](research_line_limitations.md) §3 L7
(systemic survivorship binding). No single project-internal
methodology MD covers missingness universally beyond L7; the audit
checks against the pre-reg's documented handling and the corpus's
missingness-rate descriptives where they exist.

**Operational test.** Either (a) the pre-reg documents the
missingness-aware path (e.g. HA-P6 v3 §4.8.4 ε rule + denom-undefined
exclusion); OR (b) the descriptive artefact backstopping this HA
includes a missingness-rate readout per channel × era × phase showing
no systematic bias against the cells the test reports on; OR (c) the
test's gating mechanism is itself the missingness handler and is
documented.

**Typical NOT BACKSTOPPED case.** The pre-reg dropped NaN rows
without documenting the per-channel missingness rate. The audit
flags this and routes to a per-channel missingness audit (S effort
per channel per stocktake §3 Shared gap 3).

### 5.3 A3 — Block-length validity for permutation / bootstrap

> **For block-permutation tests: stationarity assumption checked or
> block-length sensitivity-tested per
> [`permutation_null_block_length.md`](permutation_null_block_length.md).**

**Binding doc.**
[`permutation_null_block_length.md`](permutation_null_block_length.md).
The MD specifies stationary bootstrap with E[L] = 7 days as project-
wide default, with a data-driven E[L]\* confirmation and a factor-of-
2 deviation flag.

**Operational test.** For any HA whose verdict depends on a
permutation p-value or bootstrap CI: either (a) the result.md reports
E[L]\* alongside E[L]=7 and the deviation flag did not fire; OR (b) a
per-channel ACF / E[L]\* descriptive run on the test's primary
channel exists in `analyses/descriptive/` and is cited by the
pre-reg's §4. "BACKSTOPPED partial" is permitted when the ACF run
exists for the upstream channel and the test uses a derivative
(per-night delta, per-night σ, slope over multi-day window) whose ACF
could differ — the audit names what derivative-specific work would
tighten.

**Typical NOT APPLICABLE case.** The HA does not run a permutation or
bootstrap test (e.g. cross-era contrast tests K01 / K02, descriptive
Layer-1 HAs like HA-P6).

### 5.4 A4 — Era / Stratum-4 binding

> **For era-stratified tests: era boundaries match
> [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md);
> Stratum 4 primary surface honored.**

**Binding doc.**
[`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)
plus
[`phase_axis_collapsibility_conventions.md`](phase_axis_collapsibility_conventions.md)
where the HA pools across phases inside Stratum 4.

**Operational test.** The pre-reg's primary stratum is Stratum 4
(post-2022-09-03 LC-with-gevoelscore); sub-segmentation within
Stratum 4 carries an M1/M2/M3 warrant per §6 of the era-segmentation
MD; cross-phase pooling on the citalopram-phase axis cites the
collapsibility conventions §3.4 tier (A / B / C) the pre-reg invokes.
HAs drafted before
[`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)
locked (the H/HA01-11 family) are typically NOT BACKSTOPPED on A4
because they used the historical 2023-12-31 train/validate split as
primary; per stocktake §3 Shared gap 2 these are closable via the
queued historical-pre-reg re-run cross-check (M effort, shared).

### 5.5 A5 — v24 presence-conditioned semantics

> **For v24-derived signals: presence-conditioned semantics respected
> per
> [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md); no
> prevalence claim made on a presence-conditioned signal.**

**Cites L5 (presence-conditioned data layer)** from
[`research_line_limitations.md`](research_line_limitations.md). The
v24 check is the audit-layer manifestation of the L5 systemic
limitation (v24 categorisation produces presence-conditioned positive
evidence, not prevalence panels; absence ≠ negative). Every A5
finding gets recorded with explicit L5 attribution in the audit's §3
row: "A5 BACKSTOPPED — cites L5 (presence-conditioned): the HA uses
[v24-column-name] only as descriptive companion, not as primary
predictor or outcome; no prevalence-claim language in result.md."

**Binding doc.**
[`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md) plus
[`research_line_limitations.md`](research_line_limitations.md) §3 L5
(systemic v24-presence-conditioning binding).

**Operational test.** If the HA uses any `cat_*` / `state_*` /
`day_dominant_polarity` / `per_day_intensity` column, the audit
verifies that prevalence-claim language is absent from `result.md`
per the asymmetry MD's forbidden-use list (no "brainfog prevalence in
202X was N%", no "absence of mention = absence of symptom"). The
audit also verifies that companion-flag gating (`has_note=True` for
v24-derived, `intensity_source != ""` for per_day_intensity) is
applied where the column appears as a predictor or outcome. v24
signals appearing as descriptive companion / caveat class are still
in scope — the asymmetry binds caveat-class usage too, per the
research-line-limitations MD's L5 manifestation note.

**Typical NOT APPLICABLE case.** The HA's primary signals are all
`daily_computed` per the asymmetry MD's variable-class taxonomy
(most of the HA corpus per stocktake §1 distribution: ~38% of cells
are A5 NOT APPLICABLE). The audit marks NOT APPLICABLE with the
one-sentence reason "no v24 primary signals; daily_computed-only
test".

**L-ID surface.** When this assumption is NOT APPLICABLE, the Stage I
artefact still inherits no L5 citation obligation. When this
assumption is BACKSTOPPED with v24 usage present (even as caveat
class), the Stage I artefact MUST cite
[`research_line_limitations.md`](research_line_limitations.md) L5
per its §5 citation requirements.

### 5.6 A6 — Nightly attribution

> **For nightly/recovery signals: wake-up-date attribution per
> [`nightly_attribution.md`](nightly_attribution.md).**

**Binding doc.**
[`nightly_attribution.md`](nightly_attribution.md).

**Operational test.** If the HA uses any sleep-derived column
(`stress_mean_sleep`, `sleep_efficiency`, `morning_bb_peak`,
`bb_overnight_gain`, `sleep_duration_min`, RHR-via-UDS, etc.), the
audit verifies that the column attributes to the wake-up date (the
nightly-attribution MD documents that all four Garmin sources arrive
in wake-up-date convention before the consolidate stage; the build
script does no date shifting). Per-HA backstops are not separately
required for the convention itself; what IS required is per-HA
explicit use of `sleep_valid_flag` (or the equivalent gating column)
for sleep-derived signals, which the audit verifies in `test.py`.

**Typical NOT APPLICABLE case.** Daytime-only tests (per-minute
daytime stress, daily activity aggregates, bout-level features). The
audit marks NOT APPLICABLE with the one-sentence reason
"daytime-only; no nightly column".

### 5.7 A7 — Effect-size direction reporting

> **Effect-size direction reported alongside p-values, never alone.**

**Binding doc.**
[CONVENTIONS.md](../CONVENTIONS.md) §2.1 (descriptive before
inference) and the project's standing pre-reg discipline of paired
point-estimate + CI + p reporting.

**Operational test.** For every cell `result.md` reports a p-value
on, the audit verifies a directional effect size (Cliff's δ,
percentage-point discrimination, median delta, OR with CI95,
S-contrast, JT statistic, etc.) appears alongside. A p-value without
a paired effect size is NOT BACKSTOPPED; the audit names the missing
report and routes to result-data.json re-extraction (typically S
effort, the data is already in the result-data file).

**Why this is binding.** A p-value without effect-size direction
collapses "the test detected something" with "the something has the
predicted sign and meaningful magnitude" — these are different
claims. Stage I cannot translate verdict → inference without the
direction; this is the lowest-cost discipline a result.md can carry.

### 5.8 A8 — Train / validate split fate

> **Where train/validate split was used: per
> [`train_validate_split_fate.md`](train_validate_split_fate.md),
> single-pool primary preserved.**

**Binding doc.**
[`train_validate_split_fate.md`](train_validate_split_fate.md).

**Operational test.** If the HA was drafted after 2026-06-13 (when
the split-fate MD locked), the audit verifies single-pool primary is
used and any train/validate report is descriptive M3 sensitivity
overlay only (no per-portion confirmatory verdict, no per-portion α).
If the HA is from the H/HA01-11 family (drafted before 2026-06-13),
the historical 2023-12-31 split is the HA's primary by design per
stocktake §3 Shared gap 2; the audit marks NOT BACKSTOPPED with the
one-sentence note that the closure path is the queued historical-pre-
reg cross-check (M effort, shared across the H/HA01-11 family). For
historical HAs the NOT BACKSTOPPED status is **narrows confidence,
not blocks Stage I** per stocktake §3 Shared gap 2 — Stage I may
proceed but the interpretation MUST cite the legacy-split status.

**Typical NOT APPLICABLE case.** Cross-era contrast tests (K01, K02)
whose predictor IS the era split; the split-fate MD does not bind
these because the split is not used as a validation framework.

### 5.9 Optional HA-specific rows

The eight items above are the floor, not the ceiling. HA-specific
load-bearing assumptions get appended:

- **Cross-phase pooling discipline** for HAs that pool across
  citalopram-phase axis (per
  [`phase_axis_collapsibility_conventions.md`](phase_axis_collapsibility_conventions.md)
  and
  [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)).
- **Framework-validity gate** for HAs that depend on a parent HA's
  validation passing (e.g. HA-C4c depends on HA11-bout-redo's
  framework-validity gate having cleared).
- **Recovery-phase axis sub-segmentation** for HAs invoking
  [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) sub-phases
  (4a / 4b).
- **Bout-level operand validity** for HAs using bout-extracted
  features per
  [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md).

Each HA-specific row follows the same shape: assumption statement,
source (pre-reg / methodology MD / test.py), status (BACKSTOPPED /
NOT BACKSTOPPED / NOT APPLICABLE) with cited artefact / missing
artefact, operational test.

## 6. Conflict rules

The audit MUST apply the following conflict rules when assumption
status and verdict status interact:

### 6.1 Descriptive contradicts the test's assumption

> Verdict is downgraded to INCONCLUSIVE-PROVISIONAL. No interpretation
> may be built on it until the descriptive issue is resolved.

Three resolution paths:

1. **New test under a corrected operationalisation.** The HA is
   re-run with the assumption-honoring path; new verdict locks; new
   audit runs.
2. **New operationalisation pre-reg.** The HA is superseded or
   paralleled by a sister HA whose operationalisation respects the
   assumption (e.g. HA-C3 v2 paralleled by HA-C3p, which tests the
   same underlying construct via personal-baseline quintile binning
   when the Wiggers-verbatim absolute-numerical anchor in v2 produces
   a wrong-direction signal — sister-HA architecture per the
   synthesis-structure map's C-stress-fatigue-shape cluster).
3. **User accepts narrower claim.** The user explicitly accepts a
   tier-narrower interpretation under the PROVISIONAL flag. The
   Stage I artefact carries the PROVISIONAL marker and the
   `open_inputs` entry remains open.

The audit does not choose between these; it routes the conflict and
the user picks the path.

### 6.2 Descriptive cannot be produced because data does not exist

> The HA is flagged for "structurally untestable as currently
> specified" and routed back to pre-reg revision, retirement, or
> shelve-blocked-by-dependency.

**Who flags it.** The audit's Stage 4 verdict-trust call surfaces it
as the **fourth verdict-trust label** named in §4.4
(STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED). The audit does NOT
mark it TRUSTED, DOWNGRADED-INCONCLUSIVE-PROVISIONAL, or
REQUIRES-DESCRIPTIVE-WORK — those three labels assume the data could
in principle exist.

**Where it gets routed.** Three concrete pathways:

1. **Pre-reg revision** — the HA's pre-reg is re-opened under
   producer-mode pre-reg-drafting discipline (per
   `hypothesis_lock_process.md` where it exists, or the project's
   standing pre-reg discipline); a revised pre-reg lowers the gating
   bar OR re-frames the operationalisation OR waits for data
   accrual.
2. **Retire** — if the data cannot exist (e.g. H05's spec-induced
   trivial distribution; the operationalisation itself is the failure
   mode), the HA is marked RETIRED in the registry per stocktake
   §9.1. A successor slot may be reserved in
   [`synthesis_structure_map.md`](synthesis_structure_map.md)
   pending a re-spec.
3. **Shelve-blocked-by-dependency** — if the data cannot exist
   *yet* because an upstream artefact's outputs are unverified (e.g.
   S02b depends on S02's algorithmic-lag outputs which were never
   independently descriptively characterised), the HA is marked
   SHELVED-BLOCKED in the registry per stocktake §9.1 D1.

**What the audit's status becomes.** The verdict-trust call reads
"STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED — routed to [path]"
with the routing destination named explicitly.

**`open_inputs` entry still required** (per plan §3.5 hard rule:
"every refusal-to-proceed produces an `open_inputs` entry"). For a
structurally-untestable HA, the §4.5 block contains a **terminal-
state entry** naming what would unblock the HA — not a descriptive
artefact (none can close a structural impossibility), but the
**unblock pathway itself** (revised pre-reg spec, replacement HA, or
upstream-dependency landing). Format:

> *open_inputs entry (terminal-state, structurally-untestable):*
> What is missing: a pre-reg whose operationalisation does not run
> into [the specific structural failure mode].
> What it blocks: the entire HA's progression to Stage I; the row
> in the synthesis-structure map either RESERVES a successor slot
> or excludes the HA.
> Acquisition path: pre-reg revision per
> `hypothesis_lock_process.md` (re-spec); OR retirement with
> successor slot per stocktake §9.1; OR dependency landing if
> shelve-blocked.
> Fallback claim available: none — this HA produces no claim until
> unblocked.

The terminal-state entry distinguishes "structurally untestable"
from "REQUIRES-DESCRIPTIVE-WORK" (where the open_inputs entry names
a closable descriptive artefact). Both produce an `open_inputs`
entry; their entries differ in what closes them.

### 6.3 Audit disagrees with the stocktake's per-HA matrix

> The audit may revise the stocktake's B / N / / assignment, but
> MUST surface the revision explicitly.

The stocktake (§2 of
[`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md))
is a precedent run of this checklist; the audit may find a more
recent descriptive artefact has landed that closes a stocktake-N row,
or that a stocktake-B row was generous on a derivative-specific point
the strict reading would mark partial — the stocktake's §7 self-note
explicitly flags this risk ("the audit may legitimately mark a
stocktake-B row as N if a derivative-specific check the stocktake's
B-partial liberalism let slide fails on strict reading"). Either
revision MUST appear in **§3 (the per-assumption status assignment
table)** of the audit with a one-sentence diff against the stocktake.
The §4 verdict-trust call inherits the §3 revision; it does not
re-state it.

### 6.4 Audit verdict-trust call vs verdict label

> The verdict-trust call is independent of the verdict label.

A REJECTED verdict whose assumptions are all BACKSTOPPED is TRUSTED
(Stage I can build the "what the verdict licenses" reading on it).
A SUPPORTED verdict whose A3 block-length is NOT BACKSTOPPED is
DOWNGRADED-INCONCLUSIVE-PROVISIONAL. The audit does NOT preferentially
trust REJECTED over SUPPORTED or vice versa; it audits assumptions,
not conclusions.

## 7. Anti-patterns explicitly forbidden

The following moves are forbidden in any audit:

### 7.1 "The test ran, therefore the assumptions held"

The most common failure mode of an unguided audit. The fact that
`test.py` produced a result.md does not backstop any assumption —
permutation tests produce p-values even when block-length is wrong;
mean-comparison tests produce point estimates even when the
missingness pattern is biased. The audit MUST cite a separate
descriptive artefact for every BACKSTOPPED row.

### 7.2 Single-cell descriptive cited as global backstop

Citing a single descriptive plot as evidence the assumption held
globally when it only shows one cell. Example: an ACF run on
Stratum-4-unmedicated cells does not backstop a HA that pools
unmedicated + citalopram phases — the audit MUST verify the
descriptive covers the cells the test reports on, not a subset.

### 7.3 Post-hoc descriptive backstop

Backstopping an assumption with a descriptive artefact that was
generated **after** the test and whose generation peeked at the
test's per-day values. The artefact's lock date is the discriminator:
if the artefact locked after the test ran AND its scope was chosen in
response to the test's output, the artefact is contaminated and
cannot backstop. The audit MUST name lock dates when citing
descriptive artefacts and refuse to use post-hoc-and-peeking
artefacts.

### 7.4 Re-interpreting the verdict in the audit

The audit does NOT re-read the verdict. It does NOT say "the
REJECTED is actually a PARTIAL" or "this SUPPORTED should be
narrowed". Verdict re-reading is Stage I's job. The audit's job ends
at the verdict-trust call.

### 7.5 Silent assumption-list editing

The audit does NOT add or remove load-bearing assumptions to fit the
verdict it would like to certify. Every row in §2 of the audit MUST
map to a pre-reg / methodology-MD / test.py source. If the audit
believes an additional assumption is load-bearing that the pre-reg
did not declare, it adds it with `test.py` as the source and surfaces
the prose-vs-code drift — but the addition is transparent, not
silent.

### 7.6 Marking TRUSTED to avoid blocking Stage I

The audit MUST refuse to mark TRUSTED when any load-bearing
assumption is NOT BACKSTOPPED. The skill (per §9 below) enforces
this refusal at the agent level. If the user wants Stage I to
proceed under DOWNGRADED-INCONCLUSIVE-PROVISIONAL, that is an
explicit user-accept-PROVISIONAL action recorded in the audit's lock
log — not a silent TRUSTED.

### 7.7 Citing the limitations doc instead of producing the backstop

The
[`research_line_limitations.md`](research_line_limitations.md) L5 +
L7 entries name systemic limitations; they do not backstop the per-
HA descriptive evidence those limitations apply to. An audit citing
"L7 — survivorship per limitations doc" as a BACKSTOPPED A2 row is
forbidden; the L-ID citation is the Stage I obligation, not the
Stage D backstop.

## 8. Interview-prompt seeds

The `/research-interpret descriptive HA-XX` skill drives the audit as
an interview. Three required seeds the skill MUST ask the user:

### 8.1 Load-bearing assumption identification

> "Which assumptions in this HA's §4 do you read as load-bearing?"

**Use.** Opens §2 of the audit. The user names the assumptions they
believe the test rests on; the skill cross-checks against `test.py`
and the cited methodology MDs and surfaces additions (where code
relies on an assumption prose did not declare) or subtractions
(where the user's reading is more conservative than the code path
requires). The interview is **not** the skill autonomously
enumerating; the user has lived knowledge of the operationalisation's
intent that no audit-by-code can recover.

### 8.2 Per-assumption coverage check

> "For [assumption], does the descriptive artefact at [path] cover
> the same cells the test reports? If not, what's the gap?"

**Use.** Drives §3 of the audit. The skill presents the candidate
backstop (from the stocktake's precedent assignment or from a fresh
glob of `analyses/descriptive/`) and the user confirms whether the
cells match. Mismatches become "BACKSTOPPED partial" entries with
named gaps, or NOT BACKSTOPPED entries with the gap closure path
named.

### 8.3 Post-hoc contamination check

> "Did this descriptive artefact exist before the test ran, or was
> it generated to backstop?"

**Use.** Surfaces the §7.3 anti-pattern. For every BACKSTOPPED row,
the skill verifies the descriptive artefact's lock date precedes the
HA's test run date (or the artefact's scope was not chosen in
response to the test's outputs). When the artefact post-dates the
test, the skill flags it and the user decides whether the artefact's
scope is independent of the test's outputs (acceptable) or
contaminated (forbidden — the row reverts to NOT BACKSTOPPED).

### 8.4 Optional seed — verdict-trust call confirmation

> "Given the eight checklist rows, do you accept TRUSTED / DOWNGRADED-
> INCONCLUSIVE-PROVISIONAL / REQUIRES-DESCRIPTIVE-WORK as the audit's
> verdict-trust call?"

**Use.** Confirms §4. This is a confirmation seed, not a discovery
seed — by the time the skill reaches it, the §3 ticks should
mechanically determine the call. The user's explicit acceptance is
the binding completion event per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.8.

## 9. Agent-instruction outline

This section is what `/research-interpret descriptive HA-XX`
(produced in §11 step 7 of the plan) will codify into its skill
behavior. The skill MUST follow these phases in order:

### 9.1 Load

The skill loads (in order): the HA's locked `hypothesis.md`,
`result.md`, and `test.py`; the methodology MDs the pre-reg cites
(at minimum the five §5 anchors plus any HA-specific MDs); the
stocktake's per-HA matrix row in
[`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
where present; candidate descriptive artefacts under
`analyses/descriptive/`. The skill MUST refuse to proceed if any of
`hypothesis.md`, `result.md`, or `test.py` is missing.

**Fail-safe**: if the stocktake cites a candidate descriptive
artefact path that no longer exists at load time (the path was
re-organised, the artefact was archived, etc.), the skill defaults
that assumption-cell to **NOT BACKSTOPPED** and writes an
`open_inputs` entry naming the missing path. The skill does NOT
silently degrade to "BACKSTOPPED via stocktake precedent" when the
underlying artefact has moved or been removed.

### 9.2 Extract

The skill extracts the pre-reg's declared load-bearing assumptions
(from §1 / §4 / §7 / §8), the code-path-relied assumptions from
`test.py` (resampling scheme, gating columns, effective-n routine),
and the methodology-MD-bound assumptions (which of the eight §5
items apply). Prose-vs-code drift is surfaced as an explicit list
feeding the §8.1 interview seed.

### 9.3 Interview

The skill walks the §8 seeds in order — §8.1 (assumption
identification), §5 checklist walk under §8.2 + §8.3 per row, §8.4
(verdict-trust confirmation). The skill MUST NOT autonomously fill
any §2 / §3 row without user confirmation; it is an interview engine,
not an autonomous auditor.

### 9.4 Produce

The skill drafts `analyses/descriptive/HA-XX/descriptive_audit.md`
following the §4 outline. All five sections are filled; §4.5 carries
one `open_inputs` entry per NOT BACKSTOPPED row (zero entries when
all rows are BACKSTOPPED / NOT APPLICABLE).

### 9.5 Refuse-to-mark-TRUSTED gate

The skill MUST refuse to write "TRUSTED" in §4.4 if any §3 row is
NOT BACKSTOPPED. User override to REQUIRES-DESCRIPTIVE-WORK or
DOWNGRADED-INCONCLUSIVE-PROVISIONAL is recorded in the lock log per
§11.

### 9.6 Acceptance + drift-trigger registration

Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.8, "user explicitly accepts" is the binding completion event. On
acceptance: the status header transitions to LOCKED with a lock-log
entry; §4.5 entries propagate to the layer-wide `_open_inputs.md`
queue; Stage I becomes eligible (TRUSTED unblocks; PROVISIONAL
unblocks under explicit user acceptance of the flag; REQUIRES-
DESCRIPTIVE-WORK blocks). Per §3.7 drift policy, the skill registers
two re-examination triggers at lock time — underlying HA's
`result.md` re-runs, OR a cited methodology MD changes lock-version
— so the six-monthly cadence check can surface re-examination
candidates.

**Drift-trigger registration is manual-pending-skill.** Until the
§11 step 7 `/research-interpret` skill lands, drift-trigger
registration is maintained by hand: the audit's §11 lock log carries
a "Drift triggers registered" line naming the two trigger conditions,
and a future drift-check pass walks the lock logs of every audit to
identify HAs whose triggers have fired. This parallels the
limitations doc §8 downstream-citation-count manual-tracking pattern
(also pending the skill).

## 10. Cross-references

- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  — §6.1 (the spec brief this guide implements); §3.5 (missing-inputs
  flagging as first-class); §3.7 (drift and replication policy);
  §3.8 (stopping and completion criteria); §11 step 6.1 (the
  implementation step that produced this guide).
- [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
  — the precedent run of the §5 checklist across 30 HAs; §4 (the
  four HAs ready for Stage D TRUSTED that future audits inherit as
  framework); §3 (the gap list the audits' `open_inputs` entries
  feed); §9 (user decisions on stocktake findings shaping registry
  and reserved-slot work).
- [`synthesis_structure_map.md`](synthesis_structure_map.md) — the
  pre-registered map declaring which HAs cluster downstream; the §4.5
  open_inputs entries name what Stage S₁ work the audit unblocks.
- [`research_line_limitations.md`](research_line_limitations.md) —
  §5 citation requirements; L5 (presence-conditioned data layer)
  binds the §5.5 v24 check; L7 (survivorship) binds the §5.1 +
  §5.2 sample-size and missingness checks. The audit does not cite
  L-IDs in its own artefact; Stage I inherits the citation
  obligation per the limitations doc's §5 table.
- [`permutation_null_block_length.md`](permutation_null_block_length.md)
  — §5.3 A3 binding.
- [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)
  — §5.4 A4 binding; M1/M2/M3 sub-segmentation warrant framework.
- [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md) —
  §5.5 A5 binding; v24-presence-conditioned semantics rule.
- [`nightly_attribution.md`](nightly_attribution.md) — §5.6 A6
  binding; wake-up-date convention.
- [`train_validate_split_fate.md`](train_validate_split_fate.md) —
  §5.8 A8 binding; single-pool primary discipline.
- [`phase_axis_collapsibility_conventions.md`](phase_axis_collapsibility_conventions.md)
  — §5.9 cross-phase pooling discipline for HAs invoking
  citalopram-phase axis.
- [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)
  — §5.9 medicated/unmedicated phase binding.
- [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) — §5.9
  recovery-phase axis sub-segmentation (4a / 4b).
- [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md)
  — §5.9 bout-level operand validity for bout-extracted feature HAs.
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) — §6.2
  pre-reg-revision routing for structurally-untestable HAs.
- [CONVENTIONS.md](../CONVENTIONS.md) — §1 (role split); §2.1
  (descriptive before inference); §2.3 (audit-before-push privacy
  gate; Stage D audit artefacts accumulate under `analyses/` and are
  subject to this gate at push time, inherited from the general
  research-folder discipline); §3 (statistical-hygiene audit
  hooks); §4.1-§4.3 (descriptive-before-inference, no interpretive
  marks, caveats vs a-priori, prior-driven hypotheses as
  confirmatory).
- Literature methodology anchors (cited by downstream Stage I but
  surfaced here for completeness):
  [`literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf`](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf);
  [`literature/methodology/shamseer_2015_cent_consort_nof1.pdf`](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf);
  [`literature/methodology/tate_2016_scribe_single_case_reporting.pdf`](../literature/methodology/tate_2016_scribe_single_case_reporting.pdf);
  [`literature/methodology/vonelm_2007_strobe_observational_checklist.pdf`](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf).

## 11. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-24 | Drafted r1 | Producer-mode by fresh agent per §11 step 6.1 of [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md) (r5 LOCKED). The agent invented five items beyond the §6.1 spec (fourth verdict-trust label STRUCTURALLY-UNTESTABLE; §6.3 audit-disagrees-with-stocktake conflict rule; §6.4 verdict-trust-independent-of-verdict-label principle; four added anti-patterns §7.4-§7.7; phased §9 agent-instruction breakdown). User accepted three interpretation choices (figures subfolder naming; PROVISIONAL → Stage-I unblock policy; optional fourth interview seed). |
| 2026-06-24 | Fresh-session `/research-methodology-review` | Verdict REVISION RECOMMENDED. Report: [`reviews/methodology-descriptive_precondition_audit-2026-06-24.md`](../reviews/methodology-descriptive_precondition_audit-2026-06-24.md). Three required actions: R1 (L-ID citation tension — §2 said "audit does not cite L-IDs" but limitations doc r3 §5 requires L5+L7); R2 (label-count contradiction §4.4 three vs §6.2 four; plus §6.2 violated plan §3.5 by skipping open_inputs on structurally-untestable); R3 (figures/ → plots/ rename for sibling consistency). Ten recommended actions: alternatives-considered paragraph; §6.3 diff moves to §3; HA-C3 v1→v2 example swap to v2+HA-C3p; §9.1 fail-safe for missing stocktake-cited paths; §9.6 manual-pending-skill; §4.4 PROVISIONAL narrower-claim discipline cite; §3 audit-before-push note; §7.7-merge option (declined); stocktake §7 cite; skill-precondition note. Confirmed-good: §1 purpose framing; six §2 inputs; §3 folder/naming convention; §4 five-section outline mapping; §4.3 hard rule on BACKSTOPPED label; eight §5 checklist items; §6.4 invention; §7.1-§7.3 anti-pattern implementations; §8.4 optional seed; §9.2 prose-vs-code drift surfacing. |
| 2026-06-24 | Revised r1 → r2 | All three required actions absorbed: R1 — §2 reframed to require L5 + L7 citation per limitations doc r3 §5 row, with §5.2 + §5.5 explicitly citing the L-IDs in their operational tests; R2 — §4.4 now lists four labels including STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED with the open_inputs terminal-state entry required; §6.2 updated to require an open_inputs terminal-state entry naming the unblock pathway; R3 — figures/ renamed to plots/ globally with sibling-consistency citation. All ten recommended actions absorbed: alternatives-considered paragraph in §1; §6.3 diff relocated to §3 layer; HA-C3 example swapped to v2+HA-C3p sister-HA pattern; §9.1 fail-safe added for missing stocktake-cited descriptive paths; §9.6 explicitly framed as manual-pending-skill; §4.4 PROVISIONAL cross-references plan §3.5 narrower-claim discipline; §10 cross-refs add CONVENTIONS §2.3 audit-before-push gate; §6.3 cites stocktake §7 self-note on B-partial liberalism; §1 adds skill-precondition note ("no Stage D audit artefact can be drafted before §11 step 7 lands"); §7.7 merge declined (defensible as standalone). |
| 2026-06-24 | **LOCKED r2** | User acceptance ("i accept"). Status of all sections LOCKED. Implementation proceeds to §11 step 6.2 (guide #2 `verdict_to_inference.md`). No second-pass review per established Option-γ pattern matching plan / limitations / map / commentary-layer LOCKs. |
