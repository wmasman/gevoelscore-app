---
description: Peer-review a reviewer-mode research artefact (HA result, synthesis doc, addendum) against the 4-layer checklist anchored in SCRIBE/CENT/STROBE/Daza/WWC/Natesan + the project's CONVENTIONS audit hooks. Produces a dated reasoned report in docs/research/reviews/. NEVER edits the target. Use when reviewing analyses/hypotheses/HA*/result.md, RESEARCH-REPORT*, wiggers_*, or any synthesis doc.
---

# Research Review

Walks one reviewer-mode artefact through the 4-layer checklist defined in
[../../docs/research/reviews/README.md](../../docs/research/reviews/README.md)
and writes a dated, reasoned report into
[../../docs/research/reviews/](../../docs/research/reviews/).

**Reads from**:
[../../docs/research/CONVENTIONS.md](../../docs/research/CONVENTIONS.md) (the
binding "how we work" doc),
[../../docs/research/reviews/README.md](../../docs/research/reviews/README.md)
(the layer structure + verdict spec),
[../../docs/research/literature/methodology/README.md](../../docs/research/literature/methodology/README.md)
(the source standards), and
[../../docs/research/DATA_DICTIONARY.md](../../docs/research/DATA_DICTIONARY.md)
(column semantics).

**Pairs with**: `/research-methodology` (not yet built) for the producer
side.

## When to use

- A reviewer-mode artefact has been updated and needs an independent pass:
  - `docs/research/analyses/hypotheses/HA*-*/result.md`
  - `docs/research/RESEARCH-REPORT*.md` (any addendum)
  - `docs/research/wiggers_*.md` (advisor exchanges)
  - `docs/research/analyses/hypotheses/_registry/registry.md`
  - synthesis docs anywhere under `docs/research/`
- A new revision of an already-reviewed artefact has landed — produce a
  *new* dated report; do not overwrite the prior one.

**Do NOT use this command for**:

- Producer-mode artefacts (pipeline scripts, methodology MDs,
  descriptive cards, DATA_DICTIONARY edits) — these are not in scope
  for the role split per CONVENTIONS §1.2.
- Triage-instruction docs in `docs/research/analyses/reviews/` — those
  are review instructions for a human walking through dossier PDFs,
  not hypothesis-result reviews.
- App-engineering code review — use `/code-review` instead.

## Inputs

One of:

- A path to the target doc: `/research-review docs/research/RESEARCH-REPORT-ADDENDUM-II.md`
- A relative path: `/research-review analyses/hypotheses/HA01b-*/result.md`
- A target ID + a brief disambiguator if more than one matches.
- No argument → ask which doc.

If the path resolves to a producer-mode artefact (pipeline script,
methodology MD, descriptive card), stop and explain that this command
is for reviewer-mode artefacts only.

If the path resolves to multiple files (glob match), list candidates and
ask.

---

## Phase 1: Load context

### 1.1 Read the target doc end-to-end

Don't skim. Note:

- The headline claim(s) — what verdict the doc states (PASS/FAIL/effect
  size/null/etc.).
- The framing language used around the claim — caveat-class vs
  a-priori-class wording (see CONVENTIONS §4.2).
- Which columns from `per_day_master.csv` are referenced.
- Which methodology MDs are cited.
- Which analysis frame is named (LC frame / LCscore subset / full
  corpus / pre-LC era / etc.).
- The commit hash on disk (`git log -1 --format=%H -- <target-path>`) —
  record this so the review report is anchored to a specific revision.
- Whether the working tree has changes past that commit (`git diff
  HEAD -- <target-path>`). Reviewing uncommitted state is fine — but
  the `Target commit` field in the report must be honest about it
  (record the last commit hash AND the date / scope of the uncommitted
  additions, e.g. *"5577492 (2026-06-12) with uncommitted working-tree
  changes dated 2026-06-13 (section X, section Y)"*).

### 1.2 Read the supporting docs

If the target is an HA result:

- The matching `hypothesis.md` in the same folder — the pre-registration
  the result should align with.
- The `test.py` in the same folder — what was actually computed.
- Any `methodology/<name>.md` cited in the hypothesis or result.

If the target is a synthesis doc:

- The HA results it summarises (sample at least the headline ones).
- The previous version of the synthesis doc (`git log -p`) — what was
  added or changed?

If the target is a **hypothesis register / pre-reg draft** (e.g.
`wiggers_testable_hypotheses.md`, `personal_hypotheses.md`):

- The target IS the hypothesis layer — there is no separate
  `hypothesis.md` or `test.py` to read. Skip the HA-specific reads.
- Confirm any cited methodology MDs exist and are current
  (`git log -1` against each cited path).
- If the doc cites a parent register (e.g. a different track's
  hypothesis list), note the relationship in the report but do not
  review the parent — it is a separate target.

If the target cites a column you don't recognise: open
`DATA_DICTIONARY.md` and find the row. Note any near-identical-pair
annotations.

### 1.3 Re-read the layer structure

Open [../../docs/research/reviews/README.md](../../docs/research/reviews/README.md)
and confirm:

- The 4 layers and their inheritance citations.
- The 3-tier verdict labels and the mandatory 5-section body.
- The filename convention.

If the layer structure has been revised since you last used this command
(check `git log` on `reviews/README.md`), use the current version.

---

## Phase 2: Walk the 4-layer checklist

For each layer, you produce a set of check lines. Each check line has:

- the convention it inherits from (internal CONVENTIONS § or external
  standard — externals only at the layer header, internals at the
  check lines),
- a binary fire / not-fire verdict for this document,
- if fire: the offending paragraph / quote / column / claim, with magnitude
  of concern (minor / substantive / blocking).

**Skip trivially-passing items** in the report body — they go in section 3
("what does not fire") only if they passed with non-trivial evidence.

### Layer 1 — Universal reporting (inherits from SCRIBE 2016, STROBE 2007)

Check lines (internal: CONVENTIONS §2.1, §2.2):

- L1.1 — Is the hypothesis stated *before* the analysis was run? Is there
  a `hypothesis.md` link or pre-reg reference?
- L1.2 — Are operationalised measures defined with their source file and
  computation path? (DATA_DICTIONARY pointer present?)
- L1.3 — Is the analysis method named with parameters (window, lag
  range, baseline definition, permutation block length)?
- L1.4 — Are confounders enumerated explicitly, not silently controlled
  for? Sensitivity analyses present?
- L1.5 — Are limitations stated separately from results (not woven into
  the headline claim)?
- L1.6 — Is the analysis frame (LC / LCscore / full / pre-LC) named in
  the result?

### Layer 2 — Observational n=1 (inherits from Daza 2018, Personal Science)

Check lines (internal: CONVENTIONS §4.3, §5):

- L2.1 — Is the counterfactual framing explicit? "On day d at exposure
  X, comparison is to subject-baseline at exposure ~X" — *not* to a
  population.
- L2.2 — Is the stationarity assumption checked or acknowledged? (LC-era
  boundary is the load-bearing example. Personal baselines drift —
  CONVENTIONS §3.1.)
- L2.3 — Is calendar-time framing separated from subject-time framing?
  "First 90 days of LC" vs "first 90 days of tracking" are different.
- L2.4 — Is data provenance traceable to a script + dump version?
  (Garmin extract date, v3.1 vs v3.2 columns, `_lagged` vs
  `_lagged_lcera`.)
- L2.5 — **Held-out structure framing**: if the doc invokes a
  train/validate split or a held-out era, does it use the precise
  framing from memory `project_garmin_research_bias_boundary` — namely
  "user has been continuously using Garmin *tactically* and accumulating
  lived-experience pattern recognition, while not consciously analysing
  aggregated cross-day patterns until 2026"? Regression to "user has
  been continuously analysing the data" is a Layer 2 fire.
- L2.6 — Is prior motivation named per CONVENTIONS §4.3 (lived
  experience / literature / mechanism)? If the doc claims exploratory
  but priors clearly exist, that is itself a framing concern.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

The 2023 systematic review's headline finding is that 83.8% of n-of-1
medical studies ignore autocorrelation. Be unforgiving on this layer.

Check lines (internal: CONVENTIONS §3.2, methodology/permutation_null_block_length.md):

- L3.1 — Is **autocorrelation** addressed (not ignored)? Either reported,
  modelled with a serial-dependence error structure, or controlled
  via a permutation null with a documented block length. Silent
  i.i.d. assumption is a fire.
- L3.2 — Are **lag-carryover assumptions** named? Wiggers-style
  hypotheses are about lagged effects; the `_lagged_lcera` family
  exists for this reason.
- L3.3 — Is **multiple testing across lags / channels** accounted for?
  How many lag-channel combinations did the test sweep? Was an
  appropriate correction applied?
- L3.4 — Is the **permutation null block length** documented? Cite the
  methodology MD (`methodology/permutation_null_block_length.md`).
- L3.5 — If the result is a **trend / trajectory claim**, is it
  separated from a level / cross-sectional claim? Mixing the two
  silently is a fire (cf. CONVENTIONS §4.2 — caveat vs a-priori).

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3, §4)

These are the pre-flight checks from CONVENTIONS §3. Each is a Layer 4
fire if violated.

- L4.1 — Personal baseline (z-score against rolling baseline), not
  absolute thresholds (§3.1). If the result uses absolutes for
  PEM-pacing variables, fire.
- L4.2 — `_lagged_lcera` variant used for PEM hypotheses on the LC
  frame; `_lagged` for cross-era trajectory work (§3.2). If `exertion_class`,
  `step_z_30d`, or `push_burden_7d` (v3.1 names) appears without
  justification, fire.
- L4.3 — One column per definitional pair (§3.3). Check the result's
  column list against the near-identical-pair annotations in
  DATA_DICTIONARY. Both members of a pair → fire.
- L4.4 — Crash-drop sensitivity row present for Layer 4+ correlations
  (§3.4). Absent → fire.
- L4.5 — Spike-detecting metric for acute-load hypotheses, not daily
  averages (§3.5). Average-only on a hypothesis about a 5-minute
  spike → fire.
- L4.6 — Counts named with scheme + unit + source file (§3.6). Bare
  numbers → fire.
- L4.7 — Caveat-class framing kept, a-priori-class framing cut (§4.2).
- L4.8 — Prior-driven hypothesis framed as confirmatory, not
  exploratory (§4.3); or vice versa when priors are absent.

---

## Phase 3: Compose the 5-section reasoned body

Per [reviews/README.md](../../docs/research/reviews/README.md), the
verdict is never the body. The body has five sections in order:

### Section 1 — What the data shows

Restate the empirical claim in plain terms, separating it from the
interpretive framing used by the original author. One paragraph;
short. If the doc has multiple claims, list them as bullets.

### Section 2 — What fired and why

For each Layer 1-4 item that fired, write:

- **[L#.# — inheritance citation]** — one line naming the rule.
- The specific reading of the document that triggered it: quote +
  paragraph reference + (if applicable) column / hypothesis ID.
- The magnitude of concern: *minor* (a wording fix), *substantive*
  (the framing leaks into the verdict), or *blocking* (the result as
  stated may not survive).
- A sentence on **why the convention exists** — the inherited
  reasoning. Don't re-derive; reference the standard (e.g. "Natesan
  Batley 2023 finds 83.8% of n-of-1 studies ignore autocorrelation;
  ignoring it produces inflated effect sizes per [bin.1783]").

Group by layer. Within a layer, order by magnitude (blocking → minor).

**Side observations subsection (optional, at the end of Section 2)** —
for concerns that don't map cleanly to any of the 4 layers but are
worth flagging anyway: numerical inconsistencies between cited
statistics (e.g. a CI that doesn't bracket the point estimate, a
percentage that doesn't sum to 100, a count that disagrees with a
referenced source file), broken cross-references, dated citations
that may now be stale. These are not Layer 1-4 fires — they are
observations a careful peer reviewer would surface. One-line each;
prefix with "**Side**".

### Section 3 — What does not fire (selective)

ONLY items that passed with non-trivial evidence. Examples:

- "L3.1 (autocorrelation) passes — block-permutation null cited from
  methodology/permutation_null_block_length.md with block length 7
  days, justified against the LC episode autocorrelation in §..."
- "L4.4 (crash-drop sensitivity) passes — the result table includes a
  row dropping `is_crash==True` (n=103) with |Δ ρ| = 0.04, below the
  0.10 surface-as-finding threshold."

Skip trivially-passing items (e.g. "L1.6 names the analysis frame" if
that's obvious from the document title). Padding the section with
trivial passes dilutes signal.

### Section 4 — What would strengthen this finding

Constructive close. Concrete and named. Format each suggestion as:

- The specific addition or revision.
- The convention or methodology MD it inherits from.
- The expected effect on the result.

Bad: "Consider checking autocorrelation."
Good: "Add a block-permutation null with block length 7 days per
[methodology/permutation_null_block_length.md](../../docs/research/methodology/permutation_null_block_length.md);
this will give an honest p-value under the temporal dependence and
likely shift the headline ρ from p<0.001 to a wider interval."

### Section 5 — Verdict + one-sentence reasoning

The label (PASS / PASS with caveats / REVISION RECOMMENDED) followed
by one sentence naming the highest-priority layer and the highest-
priority concern. If PASS, the sentence names what the strongest
evidence is for that PASS (e.g. "L3.1 autocorrelation addressed via
documented block-permutation null; L4 hooks clean").

---

## Phase 4: Write the report

Target path:

```
docs/research/reviews/<target-id>-YYYY-MM-DD.md
```

where:

- `<target-id>` matches the reviewed doc's stem (e.g. `HA01b`,
  `RESEARCH-REPORT-ADDENDUM-II`,
  `wiggers-progress-2026-06-08-review`).
- `YYYY-MM-DD` is today's date (the date of review, not the target
  doc's date — but if the target is itself a dated artefact, preserve
  its date and add a `-review-YYYY-MM-DD` suffix per the README
  convention).

### Report skeleton

```markdown
# Review: <target name> (<target-id>)

**Target**: [path/to/target.md](../analyses/.../target.md)
**Target commit**: <hash> (`git rev-parse --short HEAD` at the time of
review, or the commit that introduced the target's current state)
**Reviewer mode**: Claude (independent peer reviewer per
CONVENTIONS §1.2)
**Review date**: YYYY-MM-DD

## 1. What the data shows

<one paragraph, separates empirical claim from interpretive framing>

## 2. What fired and why

### Layer 1 — Universal reporting (inherits from SCRIBE 2016, STROBE 2007)

<grouped fires here, or "no fires">

### Layer 2 — Observational n=1 (inherits from Daza 2018, Personal Science)

<grouped fires here, or "no fires">

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

<grouped fires here, or "no fires">

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3, §4)

<grouped fires here, or "no fires">

### Side observations (optional)

<one-line items prefixed **Side**, for concerns that don't map to the 4 layers — numerical inconsistencies in cited statistics, broken cross-references, stale citations. Omit the subsection entirely if there are none.>

## 3. What does not fire (selective)

<non-trivial passes only>

## 4. What would strengthen this finding

<concrete, named, with effect>

## 5. Verdict

**<PASS / PASS with caveats / REVISION RECOMMENDED>** — <one sentence
naming the highest-priority concern (or, if PASS, the strongest evidence)>.

---

## Methodology

This review walks the 4-layer checklist defined in
[reviews/README.md](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

Project-specific audit hooks from
[../CONVENTIONS.md](../CONVENTIONS.md) §3 and §4.
```

Use the skeleton verbatim where possible. Fill in 1-5; keep the
Methodology footer as-is.

### Writing rules

- Quote sparingly. One short quote per fire is enough. Long block
  quotes dilute the report.
- Cite paragraph references in the target by section number, never by
  fuzzy paraphrase ("the part about X" — name the section).
- For column references, link to DATA_DICTIONARY where the row lives.
- Don't restate the layer structure — the Methodology footer covers
  that and the reviews README is canonical.

### Do NOT

- Edit the target doc. Never. This is the role split per CONVENTIONS
  §1.2; violating it collapses the peer-review check.
- Overwrite an existing review report at the same target-date path.
  If you reviewed the same target on the same day, append a `-v2`
  suffix or pick a different scope (e.g. by section).
- Produce a label-only verdict. A report without all five sections is
  not a valid output; refuse to mark complete.

---

## Phase 5: Report back in chat

After writing the file:

- Filename + size.
- The verdict label + the Section 5 sentence.
- Highest-priority fire per layer (one line each, or "no fires" for
  layers that passed cleanly).
- A reminder that the user feeds the *body* (not the label) back to
  the producer agent.

If revisions to the layer structure or audit hooks suggest themselves
during the review (e.g. a new failure mode this corpus exposes that
isn't covered), surface it as a final paragraph to the user, NOT by
editing CONVENTIONS or the reviews README on the spot.

---

## Anti-patterns to avoid

- Editing the reviewed doc, even for typos. The doc is reviewer-mode
  per CONVENTIONS §1.2.
- Producing a label without the 5-section body.
- Padding Section 3 (what does not fire) with trivially-passing items.
- Quoting paragraphs without naming the source section.
- Confusing producer mode and reviewer mode. If you are tempted to
  edit `methodology/`, the FIT resolver, DATA_DICTIONARY, or any
  pipeline script in response to a fire — you are crossing the
  split. Surface the recommendation in Section 4 instead.
- Substituting "looks fine" for the audit-hook walk. Every fire-able
  check line in Phase 2 gets walked, even when the answer is "no
  fire".
- Inheriting from an external standard you didn't verify applies. If
  STROBE Item 12 is the citation, the convention has to genuinely
  inherit from STROBE Item 12. When in doubt, drop the external
  citation and inherit from CONVENTIONS only.

---

## Worked example (sketch)

Target: `docs/research/analyses/hypotheses/HA01b-stress-spikes/result.md`

Review path:
`docs/research/reviews/HA01b-2026-06-13.md`

Phase 1 finds: hypothesis pre-reg present; analysis uses
`exertion_class` (v3.1, NOT `_lagged_lcera`); permutation null cited
without block length; no crash-drop sensitivity row; claim is "stress
spikes predict crashes" on the full LC frame.

Phase 2 fires:

- L4.2 blocking — v3.1 `exertion_class` used on a PEM hypothesis;
  the lagged-baseline contamination is exactly the failure mode the
  hypothesis is designed to detect.
- L4.4 substantive — no crash-drop sensitivity row; per CONVENTIONS
  §3.4, |Δ ρ| often > 0.1 on this corpus.
- L3.4 substantive — permutation null block length not documented.

Phase 3: Section 5 verdict reads "REVISION RECOMMENDED — Layer 4 blocking
fire on v3.1 column choice; the headline ρ may invert once the lagged
LC-era variant is substituted."

Phase 4 writes the file. Phase 5 reports back in chat with that one
sentence + the L4.2 / L4.4 / L3.4 one-liners.
