# The symptom-mention asymmetry and the variable-class taxonomy

**Status**: locked 2026-06-11. The framing in this document supersedes
the earlier "asymmetric semantic" language in `methodology.md` §3a; the
two are reconciled here.

This document defines **how to interpret note-derived columns** in
`per_day_master.csv` and **which columns are safe for which analytic
shape**. It is binding for every analyst working with the unified
dataset.

---

## The rule (one paragraph)

The user's day-entry notes are written as free-form reflection, not as
a structured symptom log. Therefore:

> **A mention of a symptom on a date is high-specificity positive
> evidence that the user noticed and chose to write about the symptom
> on that date. Absence of a mention is NOT evidence of absence**.
> Absence-of-mention has at least five distinct causes; only one of
> them is "the symptom was actually absent".

## The five causes of absence

When `cat_symptoom_cognitief = 0` (or any other note-derived count is
zero) on a given date, the underlying reality could be any of:

1. **Symptom was not present** (the analyst's natural reading).
2. **Symptom was present but the user did not consider it worth
   writing about** (mild, routine, or already-known).
3. **Symptom was present but another topic crowded the note** (a big
   day-event displaced symptom inventory).
4. **Symptom was present but routine — habituation makes it invisible
   to the writer**.
5. **The user simply did not write that day** (`has_note=False`; the
   count is undefined, not zero).

Only cause #1 supports treating zero-mention as zero-symptom. Causes
#2-#4 are *systematic* (i.e. they distort prevalence rates downward).
Cause #5 makes the column undefined entirely.

---

## The reframe — what the v24 layer IS

**v24 is a presence-conditioned positive evidence layer, not a
symptom-prevalence panel.**

| v24 excels at (use it) | v24 cannot do (do NOT use it) |
|---|---|
| **Categorising days that have notes** by what those notes contain (subtype, polarity, load category). | **Plotting illness trajectories.** A drop in mentions in 2025 vs 2023 could mean less brainfog, OR less writing, OR brainfog became routine. The trajectory is not the prevalence. |
| **Stratifying other independently-defined day-classes** (crash episodes, PwC ziek-days, Garmin-firing days, per_day_intensity-loaded days) by clause content. *"Of the 29 crashes, how many notes mention brainfog within 3 days before?"* is a fair v24 question. | **Estimating prevalence over time** (e.g. "how often was the user fatigued in 2024 vs 2023") from notes alone. Mention-rate is confounded with note-writing-rate. |
| **Providing high-specificity precursor flags** for hypothesis tests. *"A mention of muscle-pain on day T as positive evidence to test elevated crash-risk at T+1..T+3"* — fine. | **Validating Garmin nulls.** Absence of mention in lead-up days does NOT corroborate "no symptom" — the night Garmin saw something, the user may simply not have written. |

---

## For trajectories, use daily-computed signals instead

Trajectories must be built on signals that exist on **every calendar
date** in the coverage window, regardless of whether a note was
written. These are the trajectory-grade columns:

- **`gevoelscore`** — user logs it directly each day. `has_score=False`
  means the user didn't open the app that day, not "score zero". The
  S02 score-trajectory work uses this as a trajectory spine.
- **Garmin biometric channels** — every Garmin-coverage day
  (2021-08-16 →). `daily_uds.csv`, `activity_features_daily.csv`,
  `sleep_stress_nightly.csv`, `daily_max_spike.csv`. Objective sensor
  measurement; `has_garmin_uds=False` means a FIT-file gap, not
  inactivity. The S01 stabilisation-trajectory work uses these.
- **Coverage flags** (`has_score`, `has_garmin_uds`, etc.) — defined
  every day, computed from the above.

These columns are typed `daily_computed` in the data dictionary.

### Per_day_intensity is ALSO presence-conditioned (added 2026-06-11)

A subtle but important correction: `per_day_intensity` (cog/phy/emo
loads) might *look* like a daily-computed signal because the user runs
bulk triage rounds across all days, but the load values themselves are
derived from upstream calendar events + day-notes. **If a day has no
calendar event and no informative note content, no load can be
assigned.** A blank `cog_load` does NOT mean cog intensity was zero —
it means no signal was found to assign one.

Three states distinguished by the `intensity_source` column:

| state | what it means | use as trajectory? |
|---|---|---|
| loads ∈ {1, 2, 3} | positive evidence — user identified intensity on that axis from event/note material | yes, as positive label |
| loads blank, `intensity_source = bulk_triage_YYYY_no_info` | **explicit absence by review**: user reviewed the day, found no specific load-bearing material to identify | low-specificity absence — could be truly no intensity, OR no identifiable signal in the upstream material |
| loads blank, `intensity_source` empty | not yet triaged | true missing |

**Gating rule analogous to `has_note=True`**: for any analysis using
`cog_load`/`phy_load`/`emo_load`, gate on `intensity_source != ""`. The
`bulk_triage_*_no_info` rows then function like "geen hoofdpijn" in
the notes layer — a presence-conditioned absence-mention, not the same
as "the symptom was not there".

Trajectory rate questions ("what fraction of triaged days in 2023 were
`cog_load ≥ 2` vs 2024?") need this gating to be interpretable. Plotted
without gating, a per_day_intensity trajectory conflates "fewer loads"
with "less triaging coverage" — the same confound as v24 mention-rate
in disguise.

---

## The variable-class taxonomy

Every column in `per_day_master.csv` belongs to one of two classes:

### `daily_computed`

- Exists every day in its coverage window.
- Absence-of-value means out-of-coverage (sensor gap / user didn't log
  the app that day), NOT under-reporting.
- Trajectory-style analysis can use this column as a spine.
- Examples: `gevoelscore`, `total_steps`, `resting_hr`,
  `exertion_class`, `is_crash`, `is_dip`, `pwc_primary_hours`.

### `presence_conditioned_positive_evidence`

- Exists only when an upstream signal exists — either a written note
  (for v24-derived columns) or a load-bearing event/note (for
  per_day_intensity loads).
- `value ≥ 1` is high-specificity positive evidence.
- `value = 0` (or blank with explicit-review flag) is **low-specificity
  about absence** — see the five-cause list above.
- `value = NaN` on a day with no upstream signal; the column is
  undefined.
- Trajectory analyses must NOT use this column directly without
  gating.
- Stratify-by-content analyses are the canonical use; filter to the
  appropriate companion flag first:
  - `has_note=True` for v24-derived columns
  - `intensity_source != ""` for per_day_intensity loads
- Examples:
  - v24-derived: `cat_symptoom_cognitief`, `cat_sub_spier`,
    `cat_medicatie`, `state_symptoom_fysiek`, `day_dominant_polarity`,
    `neutral_forward_looking_flag`.
  - per_day_intensity-derived: `cog_load`, `phy_load`, `emo_load`,
    `intensity_notes`.

---

## Operationalisation in `per_day_master.csv`

1. **Two companion flags, one per presence-conditioned source family**:
   - `has_note=True` is the mandatory gate for any `cat_*` /
     `state_*` / `day_dominant_polarity` / `n_*_clauses` /
     `neutral_forward_looking_flag` column. Without the gate, a zero
     reads as "no symptom present" instead of "not asked".
   - `intensity_source != ""` is the mandatory gate for any
     `cog_load` / `phy_load` / `emo_load` / `intensity_notes` column.
     Without the gate, a blank reads as "no intensity" instead of "no
     upstream signal to assign one".

2. **Presence-conditioned columns are stored as `NaN` on days without
   their upstream signal**, not as 0. Pandas treats `NaN` as missing
   in default aggregations — this is the correct behaviour for the
   asymmetric semantic. Storing 0 would silently fold "no signal
   identified" into "signal absent".

3. **`bulk_triage_YYYY_no_info` is informative absence, not true
   missing.** The `intensity_source` column distinguishes the three
   cases (loaded / reviewed-no-info / not-triaged). Reviewed-no-info
   functions as a presence-conditioned absence-mention — analogous to
   "geen hoofdpijn" being a positive evidence of mention but
   low-specificity about state. Do NOT collapse it silently into "load
   = 0"; surface it explicitly via the source column.

4. **The data dictionary entry for every presence-conditioned column
   carries a ⚠️ marker** with a one-sentence pointer to this document.

---

## Worked examples (right vs wrong use)

### Right use of v24-derived columns

- *"Of the 29 crash episodes, what fraction have notes mentioning
  brainfog within the 3 days before episode start?"* — Filters to
  has_note=True days, counts positive evidence. Even if some lead-up
  days had brainfog without mention, the answer here is a *lower
  bound* on the brainfog-precursor rate, which is interpretable.

- *"Among crash days that have notes, what is the dominant clause
  polarity distribution?"* — Stratifying a day-class (crash) by
  content. Conditional on writing, the polarity is well-defined.

- *"Stratify gevoelscore-4 days by `cat_symptoom_cognitief ≥ 1`: how
  does the gevoelscore-5 transition rate the next day compare?"* —
  Uses the mention as a positive label, daily_computed gevoelscore as
  the trajectory spine.

### Wrong use of v24-derived columns

- *"Brainfog prevalence in 2024 was X% (mean of `cat_symptoom_cognitief
  > 0` over all days)."* — Conflates write-rate with prevalence.
  Forbidden.

- *"In 2025 the user had less muscle pain (cat_sub_spier dropped from
  X to Y mentions per month)."* — Could equally mean less writing or
  habituation. Trajectory claim from a presence-conditioned column.
  Forbidden.

- *"On the day before a crash, `cat_symptoom_cognitief = 0`,
  therefore no brainfog."* — Treats absence-of-mention as evidence of
  absence. Forbidden.

- *"Garmin RHR was elevated on day T but the note has no symptom
  mention, so the RHR signal must be noise."* — Validates a Garmin
  measurement against a presence-conditioned absence. Forbidden.

---

## Cross-references

- [`methodology.md`](methodology.md) §3a — the original interpretation
  rule (kept as a paragraph + link here, after the Phase B unified
  dataset lands).
- [`symptom_categorization_v24.md`](symptom_categorization_v24.md) —
  the v2 → v2.4 categorisation chain that produces the presence-
  conditioned columns.
- [`../DATA_DICTIONARY.md`](../DATA_DICTIONARY.md) — column-by-column
  classification.
- [`nightly_attribution.md`](nightly_attribution.md) — the dating rule
  for nightly Garmin data; separate concern from this document but
  shares the operational discipline of explicit-decision-before-join.
